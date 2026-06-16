#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
d12_scaling_residual.py — §5 sensitivity D12: scaling-residual analysis for H3a.
================================================================================

Preregistered §5 sensitivity (prereg §5; audit item D12): "compute per-city residuals
from a fitted power-law `inscriptions ∝ population^β`; re-run H3a on residuals. Tests
whether the Hanson-population correlation survives scaling-controlled analysis."

Construction (documented design choices — flag for Shawn if a different reading is
intended):
  Stage 1 — POOLED power-law: a single global negative-binomial scaling (consistent
            with H3a's NBR family, no province structure):
              insc_c ~ NB(exp(a + β · log_pop_c), φ).
  Stage 2 — SAMOC-style log-scale residual (the settlement-scaling convention; all
            cities have ≥ 1 inscription so the log is defined):
              r_c = log(insc_c) − (â + β̂ · log_pop_c)   (â, β̂ = posterior medians).
  Stage 3 — re-run the H3a within-between (Mundlak) partition on the residual as a
            GAUSSIAN response (residuals are continuous, not counts):
              r_c ~ Normal(α0 + α_prov[c] + β_within·within_c + β_between·between_c, σ).
            Report β_within (does within-province population STILL predict the
            over/under-production residual after the global scaling is removed?), its
            P(>0), and a residual variance-share f_within analogue
            Var(β_within·within)/Var(fitted). If β_within's CI excludes 0, the
            within-province Hanson signal SURVIVES scaling control.

Interpretation note: because the pooled β already absorbs the common pop slope, a
non-zero residual β_within means the WITHIN-province slope exceeds the pooled slope —
i.e. extra within-province structure beyond the global law. A residual β_within ≈ 0
means the global scaling captured the relationship.

Primary frame (1,044-city Hanson). Sapphire (MCMC, both stages cheap).
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
SEED = 20_260_616


def fit_pooled_scaling(cities: pd.DataFrame) -> tuple[float, float, dict]:
    """Stage 1: pooled NBR power-law insc ~ NB(exp(a + β log_pop), φ). Returns
    (a_median, beta_median, summary)."""
    y = cities["inscription_count"].to_numpy(dtype=int)
    lp = cities["log_pop"].to_numpy(dtype=float)
    lp_c = lp - lp.mean()                      # centre for sampling; fold back into a
    with pm.Model():
        a_c = pm.Normal("a_c", mu=0.0, sigma=5.0)
        beta = pm.Normal("beta", mu=0.0, sigma=1.0)
        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        mu = pm.math.exp(a_c + beta * lp_c)
        pm.NegativeBinomial("y", mu=mu, alpha=1.0 / inv_disp, observed=y)
        idata = pm.sample(draws=1500, tune=2000, chains=4, target_accept=0.95,
                          random_seed=SEED, progressbar=False, return_inferencedata=True)
    post = idata.posterior
    beta_med = float(post["beta"].median())
    a_c_med = float(post["a_c"].median())
    a_med = a_c_med - beta_med * lp.mean()     # uncentre
    summ = az.summary(idata, var_names=["a_c", "beta", "inv_dispersion"])
    return a_med, beta_med, {"beta_median": beta_med, "a_median": a_med,
                             "max_rhat": float(summ["r_hat"].max()),
                             "min_ess_bulk": float(summ["ess_bulk"].min())}


def fit_residual_partition(cities: pd.DataFrame, resid: np.ndarray) -> dict:
    """Stage 3: Gaussian within-between (Mundlak) partition of the scaling residual."""
    within = cities["log_pop_within"].to_numpy(dtype=float)
    between = cities["log_pop_prov_mean"].to_numpy(dtype=float)
    pidx = cities["province_idx"].to_numpy(dtype=int)
    n_prov = int(pidx.max() + 1)
    with pm.Model():
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        araw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0, shape=n_prov)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * araw)
        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)
        sigma = pm.HalfNormal("sigma", sigma=1.0)
        fitted = pm.Deterministic(
            "fitted", alpha_0 + alpha_prov[pidx] + beta_within * within + beta_between * between)
        pm.Normal("r", mu=fitted, sigma=sigma, observed=resid)
        idata = pm.sample(draws=1500, tune=2000, chains=4, target_accept=0.95,
                          random_seed=SEED, progressbar=False, return_inferencedata=True)
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    bw = post["beta_within"].values.reshape(-1)
    fit = post["fitted"].values.reshape(n, -1)
    contrib = bw[:, None] * within[None, :]
    f_within = contrib.var(axis=1, ddof=0) / fit.var(axis=1, ddof=0)
    bw_lo, bw_med, bw_hi = (float(x) for x in np.percentile(bw, [2.5, 50, 97.5]))
    fwl, fwm, fwh = (float(x) for x in np.percentile(f_within, [2.5, 50, 97.5]))
    summ = az.summary(idata, var_names=["alpha_0", "beta_within", "beta_between", "sigma", "sigma_prov"])
    return {
        "beta_within": {"median": bw_med, "ci_lo": bw_lo, "ci_hi": bw_hi,
                        "p_gt_0": float((bw > 0).mean()),
                        "survives_scaling_control": bool(bw_lo > 0 or bw_hi < 0)},
        "residual_f_within": {"median": fwm, "ci_lo": fwl, "ci_hi": fwh},
        "convergence": {"max_rhat": float(summ["r_hat"].max()),
                        "min_ess_bulk": float(summ["ess_bulk"].min()),
                        "n_divergences": int(idata.sample_stats["diverging"].sum())},
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cities = pd.read_parquet(PRIMARY_PARQUET)
    primary = json.loads(H3A_RESULTS.read_text())["primary"]
    prim_fw = primary["f_within_unweighted"]
    prim_beta_w = primary["betas"].get("beta_within", {}) if "betas" in primary else {}
    print(f"primary f_within = {prim_fw['median']:.3f} [{prim_fw['ci_lo']:.3f},{prim_fw['ci_hi']:.3f}]",
          flush=True)

    t0 = time.time()
    print("Stage 1: pooled power-law NBR ...", flush=True)
    a_med, beta_med, scaling = fit_pooled_scaling(cities)
    print(f"  pooled β = {beta_med:.3f}, a = {a_med:.3f} "
          f"(R̂ {scaling['max_rhat']:.4f})", flush=True)

    lp = cities["log_pop"].to_numpy(dtype=float)
    y = cities["inscription_count"].to_numpy(dtype=float)
    resid = np.log(y) - (a_med + beta_med * lp)        # SAMOC log-scale residual

    print("Stage 3: Gaussian within-between partition of residuals ...", flush=True)
    part = fit_residual_partition(cities, resid)
    bw = part["beta_within"]
    print(f"  residual β_within = {bw['median']:.3f} [{bw['ci_lo']:.3f},{bw['ci_hi']:.3f}], "
          f"P(>0)={bw['p_gt_0']:.3f}, survives={bw['survives_scaling_control']}; "
          f"residual f_within = {part['residual_f_within']['median']:.3f}", flush=True)

    out = {
        "frame": "primary (1,044-city Hanson)",
        "construction": "pooled NBR power-law -> SAMOC log-residual -> Gaussian within-between",
        "primary_h3a_f_within": prim_fw,
        "primary_h3a_beta_within": prim_beta_w,
        "stage1_pooled_scaling": scaling,
        "residual_partition": part,
        "secs": round(time.time() - t0, 1),
    }
    (OUT_DIR / "d12-scaling-residual-results.json").write_text(json.dumps(out, indent=1))
    print(f"\nwrote → {OUT_DIR}/d12-scaling-residual-results.json  ({out['secs']}s)")


if __name__ == "__main__":
    main()
