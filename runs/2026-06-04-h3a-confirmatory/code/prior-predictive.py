#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prior-predictive.py --- Step 0 of the H3a confirmatory run.

Draw S_pp = 1,000 parameter sets from the preregistered priors, simulate
per-city inscription counts from the PREDICTOR MATRIX ONLY (no observed y),
compute the data-shaped thresholds (count_cap_p99, tail_count_bound), run the
prior-sanity gate, and COMMIT the thresholds to a sidecar BEFORE any posterior
fit (design artefact §2).

Model (prereg §3 / design artefact §1):
  y_c ~ NegativeBinomial(mu_c, dispersion)
  log(mu_c) = a0 + a_prov[c]
              + b_within  * within_dev_c
              + b_between * prov_mean_c
  a0 ~ N(0,5); b_within ~ N(0,1); b_between ~ N(0,1)
  a_prov ~ N(0, sigma_prov); sigma_prov ~ HalfNormal(1)
  1/dispersion ~ HalfNormal(1)

Prior-sanity gate (design artefact §2): median simulated per-city count must
lie within [0.1, 1e4]; otherwise HARD-STOP (priors revisited + amendment).

Inputs
------
data/processed/city_level_for_h3a.parquet  (PRIMARY predictor matrix)

Outputs
-------
runs/2026-06-04-h3a-confirmatory/outputs/prior-predictive-thresholds.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-04, blind-run brief.
"""

from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

import h3a_common as H

# Prior-predictive simulation settings (design artefact §2).
S_PP = 1_000
RANDOM_SEED = 20_260_604  # confirmatory-run seed (distinct from talk-prep)

# Prior-sanity gate bounds (design artefact §2): median per-city count.
SANITY_MEDIAN_LO = 0.1
SANITY_MEDIAN_HI = 1.0e4


def simulate_prior_predictive(cities: pd.DataFrame, n_provinces: int,
                              rng: np.random.Generator) -> np.ndarray:
    """Simulate S_PP x C prior-predictive counts from the priors + predictors.

    Uses ONLY the predictor matrix (within_dev, prov_mean, province_idx). No
    observed counts enter. Returns array shape (S_PP, C).
    """
    within_dev = cities["log_pop_within"].to_numpy(dtype=float)
    prov_mean = cities["log_pop_prov_mean"].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)
    C = len(cities)

    sims = np.empty((S_PP, C), dtype=np.int64)
    for s in range(S_PP):
        a0 = rng.normal(0.0, 5.0)
        b_within = rng.normal(0.0, 1.0)
        b_between = rng.normal(0.0, 1.0)
        sigma_prov = abs(rng.normal(0.0, 1.0))           # HalfNormal(1)
        a_prov = rng.normal(0.0, sigma_prov, size=n_provinces)
        inv_disp = abs(rng.normal(0.0, 1.0))             # HalfNormal(1) on 1/alpha
        # Guard against a degenerate 1/dispersion ~ 0 draw (alpha -> inf).
        alpha = 1.0 / max(inv_disp, 1e-6)

        log_mu = (a0 + a_prov[province_idx]
                  + b_within * within_dev + b_between * prov_mean)
        # Clip log_mu to avoid float overflow in exp for absurd prior draws
        # (this only affects the simulated counts' upper tail, which the cap
        # exists to characterise; it does not touch the posterior fit).
        mu = np.exp(np.clip(log_mu, -50.0, 50.0))

        # NegBin parameterised as Var = mu + mu^2/alpha. numpy's negative
        # binomial uses (n, p) with mean n(1-p)/p and var mean/p. Map:
        #   n = alpha, p = alpha / (alpha + mu)  =>  mean = mu,
        #   var = mu + mu^2/alpha  (matches pymc's NegativeBinomial(mu, alpha)).
        p = alpha / (alpha + mu)
        p = np.clip(p, 1e-12, 1.0 - 1e-12)
        sims[s] = rng.negative_binomial(alpha, p)
    return sims


def main() -> int:
    if not H.PRIMARY_PARQUET.exists():
        print(f"[prior-pred] HARD-STOP: primary parquet missing at "
              f"{H.PRIMARY_PARQUET}. Run 01-data-prep.py first.")
        return 1
    cities = pd.read_parquet(H.PRIMARY_PARQUET)
    n_prov = int(cities["province_idx"].max()) + 1
    print(f"[prior-pred] primary frame: {len(cities):,} cities, "
          f"{n_prov} provinces")

    rng = np.random.default_rng(RANDOM_SEED)
    sims = simulate_prior_predictive(cities, n_prov, rng)
    print(f"[prior-pred] simulated {sims.shape[0]} draws x {sims.shape[1]} "
          "cities (predictor-only)")

    flat = sims.reshape(-1).astype(float)
    count_cap_p99 = float(np.percentile(flat, 99.0))
    tail_count_bound = float(np.percentile(flat, 99.9))
    ppc_mean_ref = float(flat.mean())
    median_per_city = float(np.median(flat))

    print(f"[prior-pred] count_cap_p99      = {count_cap_p99:.2f} (99th pct)")
    print(f"[prior-pred] tail_count_bound   = {tail_count_bound:.2f} (99.9th pct)")
    print(f"[prior-pred] ppc_mean_ref       = {ppc_mean_ref:.2f}")
    print(f"[prior-pred] median per-city    = {median_per_city:.4f} "
          f"(sanity gate [{SANITY_MEDIAN_LO}, {SANITY_MEDIAN_HI}])")

    sanity_pass = SANITY_MEDIAN_LO <= median_per_city <= SANITY_MEDIAN_HI
    if not sanity_pass:
        print("[prior-pred] HARD-STOP: prior-predictive median per-city count "
              "is ABSURD (outside the sanity gate). Priors must be revisited + "
              "amendment filed before any confirmatory fit. Halting.")
        thresholds = {
            "status": "SANITY_FAIL",
            "median_per_city": median_per_city,
            "sanity_gate": [SANITY_MEDIAN_LO, SANITY_MEDIAN_HI],
        }
        out = H.RUN_DIR / "outputs" / "prior-predictive-thresholds.json"
        out.write_text(json.dumps(thresholds, indent=2))
        return 1

    thresholds = {
        "status": "OK",
        "s_pp": S_PP,
        "random_seed": RANDOM_SEED,
        "n_cities": int(len(cities)),
        "n_provinces": n_prov,
        "count_cap_p99": count_cap_p99,
        "tail_count_bound": tail_count_bound,
        "ppc_mean_ref": ppc_mean_ref,
        "prior_predictive_median_per_city": median_per_city,
        "prior_predictive_max": float(flat.max()),
        "sanity_gate": [SANITY_MEDIAN_LO, SANITY_MEDIAN_HI],
        "sanity_pass": True,
        "derivation": (
            "count_cap_p99 = 99th pct of prior-predictive per-city counts "
            "across all draws x cities; tail_count_bound = 99.9th pct; "
            "predictor-only (no observed y); committed before posterior fit."
        ),
    }
    out = H.RUN_DIR / "outputs" / "prior-predictive-thresholds.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(thresholds, indent=2))
    print(f"[prior-pred]   -> {out}")
    print("[prior-pred] prior-sanity gate PASSED. Thresholds committed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
