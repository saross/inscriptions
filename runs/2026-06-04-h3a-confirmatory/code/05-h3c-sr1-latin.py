#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05-h3c-sr1-latin.py --- Latin-frame counterparts of H3c (residual spatial
autocorrelation) and SR1 (OLS log-log Hanson comparator).

Decision-36 consequence: the Latin-speaking-provinces frame is the new
first-class hypothesis-testing frame (amendment-gated under OSF Amendment 02,
not yet lodged). This script finalises the cross-sectional track under that
frame as a NO-RE-FIT EXTENSION: the Latin H3a posterior already exists
(idata-latin.nc, blind-run Sensitivity B), so we only:

  - SR1 (Latin): OLS log-log regression of per-city date-window
    inscription_count on Hanson population across the 817 Latin cities --- the
    exact `ols_loglog` method from 02-h3a-fit.py, pointed at the Latin frame.
  - H3c (Latin): Pearson residuals from the Latin posterior, Moran's I via k-NN
    row-standardised weights (libpysal) at k = 5, 8 (primary), 10, with
    999-permutation conditional inference (esda) on the posterior-mean
    residuals PLUS the posterior distribution of Moran's I across draws --- the
    exact method from 04-h3c.py, pointed at the Latin frame + Latin posterior.

Confirmatory rule (H3c): Moran's I > 0 at p < 0.05 in >= 2 of {5, 8, 10}.

Methodology is mirrored EXACTLY from the empire-frame run for comparability;
the only changes are the input parquet (Latin) and the input posterior
(Latin). Everything is labelled PRELIMINARY --- pending OSF Amendment 02.

Inputs
------
runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc   (Latin posterior)
data/processed/city_level_for_h3a_latin.parquet           (817 Latin cities)

The Latin frame already carries per-city median coordinates (longitude,
latitude) inherited unchanged from the primary frame --- the same
median-coordinate choice the empire H3c used --- so no coordinate
recomputation is required.

Outputs
-------
runs/2026-06-04-h3a-confirmatory/outputs/h3c-latin-results.json
runs/2026-06-04-h3a-confirmatory/outputs/sr1-latin-results.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-05, Decision-36 follow-up brief.
"""

from __future__ import annotations

import json
import sys
import warnings

import arviz as az
import numpy as np
import pandas as pd
from libpysal.weights import KNN
from esda.moran import Moran

import h3a_common as H

warnings.filterwarnings("ignore")

# --- H3c settings (identical to 04-h3c.py) --------------------------------
K_VALUES = [5, 8, 10]
PRIMARY_K = 8
N_PERMUTATIONS = 999
N_POSTERIOR_I_DRAWS = 2_000   # draws used for the posterior I distribution
RANDOM_SEED = 20_260_604

# Empire-frame comparators (read from this run's committed JSON outputs;
# re-stated here only for the in-report contrast, not used in any computation).
EMPIRE_SR1_SLOPE = 0.2839922030003124
EMPIRE_H3C_VERDICT = "not-supported"


def pearson_resids_all_draws(idata: az.InferenceData,
                             y: np.ndarray) -> np.ndarray:
    """Return (S, C) Pearson residuals across all posterior draws.

    Identical to 04-h3c.py: r = (y - mu) / sqrt(mu + mu^2 / phi), with
    mu = exp(log_mu) and phi the NBR dispersion, per posterior draw.
    """
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    alpha = post["dispersion"].values.reshape(-1)
    mu = np.exp(log_mu)
    var = mu + mu ** 2 / alpha[:, None]
    return (y[None, :] - mu) / np.sqrt(var)


def ols_loglog(cities: pd.DataFrame) -> dict:
    """OLS log-log coefficient: log(count) ~ log(pop). Hanson/SR1 comparator.

    Identical to 02-h3a-fit.py::ols_loglog. Hanson, Ortman & Lobo 2017 /
    Hanson 2021 report a population scaling exponent (beta = 0.672 in prereg).
    This is the direct frequentist comparator on the same per-city data
    (unweighted OLS on logs).
    """
    x = cities["log_pop"].to_numpy(dtype=float)
    yv = np.log(cities["inscription_count"].to_numpy(dtype=float))
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
    yhat = X @ coef
    ss_res = float(((yv - yhat) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    # Standard error of the slope.
    n = len(x)
    sigma2 = ss_res / (n - 2)
    sxx = float(((x - x.mean()) ** 2).sum())
    se_slope = float(np.sqrt(sigma2 / sxx))
    return {
        "intercept": float(coef[0]),
        "slope": float(coef[1]),
        "slope_se": se_slope,
        "slope_ci95": [float(coef[1] - 1.96 * se_slope),
                       float(coef[1] + 1.96 * se_slope)],
        "r_squared": r2,
        "n": n,
        "hanson_2021_beta": 0.672,
    }


def run_h3c(idata: az.InferenceData, cities: pd.DataFrame) -> dict:
    """H3c on the Latin frame --- mirrors 04-h3c.py::main exactly."""
    y = cities["inscription_count"].to_numpy(dtype=float)
    coords = cities[["longitude", "latitude"]].to_numpy(dtype=float)

    r_all = pearson_resids_all_draws(idata, y)     # (S, C)
    r_mean = r_all.mean(axis=0)                     # posterior-mean residual
    print(f"[05-h3c] residuals: {r_all.shape[0]} draws x {r_all.shape[1]} cities")

    rng = np.random.default_rng(RANDOM_SEED)
    sub_idx = rng.choice(r_all.shape[0],
                         size=min(N_POSTERIOR_I_DRAWS, r_all.shape[0]),
                         replace=False)

    per_k = {}
    n_pass = 0
    for k in K_VALUES:
        w = KNN.from_array(coords, k=k)
        w.transform = "r"
        # Conditional permutation inference on the posterior-mean residual.
        mi = Moran(r_mean, w, permutations=N_PERMUTATIONS, two_tailed=False)
        I_obs = float(mi.I)
        p_sim = float(mi.p_sim)        # one-sided (greater) permutation p
        z_sim = float(mi.z_sim)
        passes = (I_obs > 0) and (p_sim < 0.05)
        if passes:
            n_pass += 1

        # Posterior distribution of Moran's I.
        I_draws = np.empty(len(sub_idx))
        for i, s in enumerate(sub_idx):
            I_draws[i] = Moran(r_all[s], w, permutations=0,
                               two_tailed=False).I
        I_lo, I_med, I_hi = (float(x) for x in
                             np.percentile(I_draws, [2.5, 50, 97.5]))
        frac_above0 = float((I_draws > 0).mean())

        per_k[str(k)] = {
            "moran_I_posterior_mean_resid": I_obs,
            "p_sim_one_sided": p_sim,
            "z_sim": z_sim,
            "expected_I": float(mi.EI),
            "passes_rule": passes,
            "posterior_I_2.5pct": I_lo,
            "posterior_I_50pct": I_med,
            "posterior_I_97.5pct": I_hi,
            "posterior_frac_above_0": frac_above0,
        }
        print(f"[05-h3c] k={k:>2}: I={I_obs:+.4f} p_sim={p_sim:.4f} "
              f"z={z_sim:+.3f} pass={passes} | posterior I "
              f"[{I_lo:+.4f}, {I_med:+.4f}, {I_hi:+.4f}] "
              f"frac>0={frac_above0:.3f}")

    confirmatory_pass = n_pass >= 2
    verdict = "supported" if confirmatory_pass else "not-supported"

    # Three-case interpretive guardrail at primary k = 8 (identical to 04-h3c).
    k8 = per_k[str(PRIMARY_K)]
    frac8 = k8["posterior_frac_above_0"]
    ci8_crosses_zero = (k8["posterior_I_2.5pct"] < 0 < k8["posterior_I_97.5pct"])
    if confirmatory_pass and frac8 >= 0.95:
        case = "Case 1 -- clean replication (rule passes; >=95% of k=8 draws above 0)"
    elif confirmatory_pass and ci8_crosses_zero:
        case = ("Case 2 -- permutation-significant but posterior-sensitive "
                "(rule passes; 95% posterior interval of I_s at k=8 crosses 0)")
    elif confirmatory_pass and frac8 < 0.50:
        case = ("Case 3 -- confirmatory rule passes without substantive support "
                "(rule passes; <50% of k=8 draws above 0)")
    elif confirmatory_pass:
        case = ("rule passes; k=8 posterior 50-95% above 0 and CI does not "
                "straddle 0 -- between Case 1 and Case 2, reported with reasoning")
    else:
        case = "confirmatory rule does NOT pass (<2 of {5,8,10} significant)"

    result = {
        "frame": "latin (817 cities / 39 provinces)",
        "status": "PRELIMINARY -- pending OSF Amendment 02 (Decision 36 amendment-gate)",
        "confirmatory_rule": "Moran's I > 0 at p < 0.05 in >= 2 of {5, 8, 10}",
        "n_k_passing": n_pass,
        "verdict": verdict,
        "interpretive_case_k8": case,
        "primary_k": PRIMARY_K,
        "n_permutations": N_PERMUTATIONS,
        "n_posterior_I_draws": int(len(sub_idx)),
        "n_cities": int(len(cities)),
        "n_provinces": int(cities["province"].nunique()),
        "per_k": per_k,
        "hanson_2021_reference": {
            "residual_moran_I": 0.046, "z": 4.571, "p": "<0.0001",
            "raw_count_moran_I": -0.006,
        },
        "empire_frame_comparator": {
            "verdict": EMPIRE_H3C_VERDICT,
            "source": "runs/2026-06-04-h3a-confirmatory/outputs/h3c-results.json",
        },
    }
    print(f"[05-h3c] verdict: {verdict} ({n_pass}/3 k-values pass)")
    print(f"[05-h3c] interpretive case (k=8): {case}")
    return result


def main() -> int:
    out_dir = H.RUN_DIR / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    cities = pd.read_parquet(H.LATIN_PARQUET)
    n_cities = int(len(cities))
    n_prov = int(cities["province"].nunique())
    print(f"[05] Latin frame: {n_cities:,} cities, {n_prov} provinces")

    # HARD-STOP: realised Latin city count must be exactly 817.
    if n_cities != 817:
        print(f"[05] HARD-STOP: Latin city count {n_cities} != 817. Halting.")
        return 1

    # Coordinates must be present (no recomputation needed if so).
    if cities[["longitude", "latitude"]].isna().any().any():
        print("[05] HARD-STOP: missing per-city coordinates in Latin frame. "
              "Halting (coordinate recomputation not implemented here --- the "
              "Latin frame is expected to inherit primary median coordinates).")
        return 1

    idata = az.from_netcdf(str(out_dir / "idata-latin.nc"))

    # ===================================================================
    # SR1 (Latin): OLS log-log Hanson comparator.
    # ===================================================================
    sr1 = ols_loglog(cities)
    sr1_out = {
        "frame": "latin (817 cities / 39 provinces)",
        "status": "PRELIMINARY -- pending OSF Amendment 02 (Decision 36 amendment-gate)",
        "method": "OLS log-log: log(inscription_count) ~ log(urban_context_pop_est), "
                  "unweighted, per-city (identical to 02-h3a-fit.py::ols_loglog)",
        "ols_loglog": sr1,
        "contrasts": {
            "hanson_2021_beta": 0.672,
            "empire_frame_slope": EMPIRE_SR1_SLOPE,
            "empire_frame_source":
                "runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json"
                " (primary.ols_loglog.slope)",
        },
    }
    print(f"[05-sr1] OLS log-log slope={sr1['slope']:.4f} "
          f"(SE {sr1['slope_se']:.4f}; 95% CI "
          f"[{sr1['slope_ci95'][0]:.4f}, {sr1['slope_ci95'][1]:.4f}]); "
          f"R^2={sr1['r_squared']:.4f}; n={sr1['n']}")
    print(f"[05-sr1]   vs Hanson 0.672 and vs empire {EMPIRE_SR1_SLOPE:.4f}")
    (out_dir / "sr1-latin-results.json").write_text(json.dumps(sr1_out, indent=2))
    print(f"[05-sr1]   -> {out_dir / 'sr1-latin-results.json'}")

    # ===================================================================
    # H3c (Latin): residual spatial autocorrelation.
    # ===================================================================
    h3c = run_h3c(idata, cities)
    (out_dir / "h3c-latin-results.json").write_text(json.dumps(h3c, indent=2))
    print(f"[05-h3c]   -> {out_dir / 'h3c-latin-results.json'}")

    print("[05] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
