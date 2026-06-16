#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
d11_hanson_me.py — §5 sensitivity D11: Hanson-population measurement-error.
==========================================================================

Preregistered §5 sensitivity (prereg §5 line 352; Decision 26/B9; audit item D11):
re-fit the H3a within-between (Mundlak) NBR with a lognormal measurement-error (ME)
layer on Hanson population, σ_pop ∈ {0.1, 0.2, 0.3}, and report f_within per σ_pop.
Material divergence from the no-ME primary is flagged descriptively (NOT an amendment
trigger — prereg §5; I7 in the obligations audit).

Implementation — EXACTLY the preregistered ME (prereg §5):
  ``log_pop_c ~ Normal(log_pop_observed_c, σ_pop)``  (a Berkson-style prior centred
  on the observed value; NOT a structural EIV hyperprior — faithful to the prereg
  notation). The latent log-population is informed by both this prior and the count
  likelihood. The Mundlak components are recomputed FROM THE LATENT log_pop each draw
  (province mean via a row-normalised membership matrix), so both the within deviation
  and the between mean carry the population uncertainty — the point of the sensitivity.
  Otherwise identical to the primary: non-centred province intercepts, NBR likelihood,
  the same f_within = Var(β_within·within)/Var(log μ).

Material-divergence rule (prereg §5): the f_within 95% CI shifting by more than 50% of
the primary-result CI width (primary width 0.125 → threshold 0.0625) under any σ_pop is
flagged as a limitation; it does NOT trigger an amendment (preregistered exploratory).

Anchor: the no-ME primary f_within (runs/2026-06-04-h3a-confirmatory) is read and
reported alongside; σ_pop → 0 would reproduce it.

Run: PRIMARY 1,044-city frame, σ ∈ {0.1,0.2,0.3}. Sapphire (MCMC). Convergence
reported honestly; a §5 sensitivity is accepted-with-caveat at marginal R̂ per the
project's established exploratory treatment.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-16.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

ROOT = Path("/home/shawn/Code/inscriptions")
PRIMARY_PARQUET = ROOT / "data/processed/city_level_for_h3a.parquet"
H3A_RESULTS = ROOT / "runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json"
OUT_DIR = ROOT / "runs/2026-06-16-s5-sensitivities/outputs"

SIGMAS = [0.1, 0.2, 0.3]
N_TUNE, N_DRAW, N_CHAINS, TARGET_ACCEPT = 4_000, 2_000, 4, 0.95
SEED = 20_260_616


def province_mean_matrix(province_idx: np.ndarray, n_prov: int) -> np.ndarray:
    """Row-normalised (n_prov × n_city) membership matrix M; M @ x = province means."""
    n = len(province_idx)
    m = np.zeros((n_prov, n))
    m[province_idx, np.arange(n)] = 1.0
    return m / m.sum(axis=1, keepdims=True)


def build_me_model(cities: pd.DataFrame, sigma_pop: float) -> pm.Model:
    y = cities["inscription_count"].to_numpy(dtype=int)
    x_obs = cities["log_pop"].to_numpy(dtype=float)
    pidx = cities["province_idx"].to_numpy(dtype=int)
    n_prov = int(pidx.max() + 1)
    mmat = province_mean_matrix(pidx, n_prov)

    with pm.Model() as model:
        # Preregistered ME: latent log-pop ~ Normal(observed, σ_pop) (Berkson form).
        log_pop_true = pm.Normal("log_pop_true", mu=x_obs, sigma=sigma_pop, shape=len(x_obs))

        # Mundlak components recomputed from the latent population.
        prov_mean = pm.math.dot(mmat, log_pop_true)          # (n_prov,)
        between = prov_mean[pidx]
        within = pm.Deterministic("within_true", log_pop_true - between)

        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        alpha_prov_raw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0, shape=n_prov)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * alpha_prov_raw)
        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)
        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)

        log_mu = pm.Deterministic(
            "log_mu", alpha_0 + alpha_prov[pidx] + beta_within * within + beta_between * between)
        pm.NegativeBinomial("y", mu=pm.math.exp(log_mu), alpha=dispersion, observed=y)
    return model


def f_within(idata: az.InferenceData) -> np.ndarray:
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    beta_w = post["beta_within"].values.reshape(-1)
    within = post["within_true"].values.reshape(n, -1)
    contrib = beta_w[:, None] * within
    return contrib.var(axis=1, ddof=0) / log_mu.var(axis=1, ddof=0)


def summarise(draws: np.ndarray) -> dict:
    lo, med, hi = (float(x) for x in np.percentile(draws, [2.5, 50, 97.5]))
    verdict = ("supported" if lo > 0.10 else "evidence-against" if hi < 0.10 else "inconclusive")
    return {"median": med, "ci_lo": lo, "ci_hi": hi,
            "p_gt_005": float((draws > 0.05).mean()),
            "p_gt_010": float((draws > 0.10).mean()),
            "p_gt_020": float((draws > 0.20).mean()), "verdict": verdict}


def convergence(idata: az.InferenceData) -> dict:
    summ = az.summary(idata, var_names=["alpha_0", "beta_within", "beta_between",
                                        "sigma_prov", "inv_dispersion"])
    return {"max_rhat": float(summ["r_hat"].max()),
            "min_ess_bulk": float(summ["ess_bulk"].min()),
            "n_divergences": int(idata.sample_stats["diverging"].sum()),
            "rhat_argmax": str(summ["r_hat"].idxmax())}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cities = pd.read_parquet(PRIMARY_PARQUET)
    primary_f = json.loads(H3A_RESULTS.read_text())["primary"]["f_within_unweighted"]
    print(f"anchor: no-ME primary f_within = {primary_f.get('median'):.3f} "
          f"[{primary_f.get('ci_lo'):.3f}, {primary_f.get('ci_hi'):.3f}]", flush=True)

    results = {"frame": "primary (1,044-city Hanson)", "no_me_primary": primary_f,
               "sampling": {"tune": N_TUNE, "draw": N_DRAW, "chains": N_CHAINS,
                            "target_accept": TARGET_ACCEPT, "seed": SEED},
               "sigma_pop": {}}
    for sig in SIGMAS:
        t0 = time.time()
        print(f"\n=== σ_pop = {sig} ===", flush=True)
        model = build_me_model(cities, sig)
        with model:
            idata = pm.sample(draws=N_DRAW, tune=N_TUNE, chains=N_CHAINS,
                              target_accept=TARGET_ACCEPT, random_seed=SEED,
                              progressbar=False, return_inferencedata=True)
        fw = summarise(f_within(idata))
        conv = convergence(idata)
        results["sigma_pop"][str(sig)] = {"f_within": fw, "convergence": conv,
                                          "secs": round(time.time() - t0, 1)}
        print(f"  f_within = {fw['median']:.3f} [{fw['ci_lo']:.3f}, {fw['ci_hi']:.3f}] "
              f"({fw['verdict']}); R̂max {conv['max_rhat']:.4f}, ESS {conv['min_ess_bulk']:.0f}, "
              f"div {conv['n_divergences']}  ({results['sigma_pop'][str(sig)]['secs']}s)", flush=True)

    # Material-divergence flag (prereg §5): CI shift > 50% of primary CI width.
    prim_lo, prim_hi = primary_f["ci_lo"], primary_f["ci_hi"]
    prim_w = prim_hi - prim_lo
    thresh = 0.5 * prim_w
    flags = {}
    for sig in SIGMAS:
        fw = results["sigma_pop"][str(sig)]["f_within"]
        shift = max(abs(fw["ci_lo"] - prim_lo), abs(fw["ci_hi"] - prim_hi))
        flags[str(sig)] = {"ci_shift": round(shift, 4), "material": bool(shift > thresh)}
    results["material_divergence"] = {"primary_ci_width": round(prim_w, 4),
                                      "threshold_50pct": round(thresh, 4),
                                      "per_sigma": flags,
                                      "any_material": any(f["material"] for f in flags.values())}
    (OUT_DIR / "d11-hanson-me-results.json").write_text(json.dumps(results, indent=1))
    print(f"\nmaterial divergence (any σ): {results['material_divergence']['any_material']}")
    print(f"wrote → {OUT_DIR}/d11-hanson-me-results.json")


if __name__ == "__main__":
    main()
