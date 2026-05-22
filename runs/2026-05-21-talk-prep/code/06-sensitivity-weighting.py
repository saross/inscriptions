#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06-sensitivity-weighting.py --- Phase A.1 of the RAC-TRAC 2026 talk-prep run.

Purpose
-------
Three-weighting f_within sensitivity (preregistered §5 exploratory):
re-fit the primary Mundlak NBR and compute the within-province
population-attributable variance fraction under three weightings of the
city contribution:

  (1) Unweighted (the primary; same as 05-h3a-bayesian-mundlak.py)
  (2) Population-weighted (w_c = population_c)
  (3) Inscription-weighted (w_c = inscription_count_c)

Preregistered decision rule (prereg §5):
  "Material divergence: if the spread across the three weighted variants
  exceeds half the primary unweighted posterior 95 % CI width, this is
  flagged as a limitation."

So compute:
  - Primary unweighted CI = [0.240, 0.366] (from 05); half-width = 0.063
  - For each variant: posterior median; report whether the spread
    (max-median - min-median across the three) exceeds 0.063.

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet

Outputs
-------
runs/2026-05-21-talk-prep/outputs/tables/sensitivity-weighting-summary.csv
runs/2026-05-21-talk-prep/outputs/tables/sensitivity-weighting-draws.csv

Author / Date
-------------
Claude (Opus 4.7), 2026-05-21, on Shawn's brief.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
DATA_PATH = RUN_DIR / "data" / "lire-filtered.parquet"
TBL_DIR = RUN_DIR / "outputs" / "tables"
TBL_DIR.mkdir(parents=True, exist_ok=True)

N_WARMUP = 3_000
N_SAMPLE = 2_000
N_CHAINS = 4
RANDOM_SEED = 20_260_521

# Primary unweighted CI from 05 run (for the material-divergence check).
PRIMARY_CI_LO = 0.240
PRIMARY_CI_HI = 0.366
PRIMARY_CI_HALF_WIDTH = (PRIMARY_CI_HI - PRIMARY_CI_LO) / 2.0  # 0.063


def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def build_city_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    sub = df.loc[~rome & has_hanson].copy()
    agg = (
        sub.groupby("urban_context_city")
        .agg(
            inscription_count=("urban_context_city", "size"),
            urban_context_pop_est=("urban_context_pop_est", "first"),
            province=("province",
                      lambda x: x.mode()[0] if not x.mode().empty else np.nan),
        )
        .reset_index()
    )
    agg = agg.dropna(subset=["province"]).copy()
    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    prov_means = agg.groupby("province")["log_pop"].transform("mean")
    agg["log_pop_prov_mean"] = prov_means
    agg["log_pop_within"] = agg["log_pop"] - prov_means
    pcodes = pd.Categorical(agg["province"])
    agg["province_idx"] = pcodes.codes
    return agg, list(pcodes.categories)


def fit_mundlak(cities: pd.DataFrame, n_provinces: int) -> az.InferenceData:
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    lp_within = cities["log_pop_within"].to_numpy(dtype=float)
    lp_prov_mean = cities["log_pop_prov_mean"].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)

    with pm.Model() as model:
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        alpha_prov_raw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0,
                                    shape=n_provinces)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * alpha_prov_raw)
        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)
        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)

        log_mu = (
            alpha_0
            + alpha_prov[province_idx]
            + beta_within * lp_within
            + beta_between * lp_prov_mean
        )
        mu = pm.math.exp(log_mu)
        pm.Deterministic("log_mu", log_mu)
        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)

        print(f"[block-6] sampling NUTS: warmup={N_WARMUP}, draws={N_SAMPLE}, "
              f"chains={N_CHAINS}")
        idata = pm.sample(
            draws=N_SAMPLE,
            tune=N_WARMUP,
            chains=N_CHAINS,
            random_seed=RANDOM_SEED,
            progressbar=False,
            target_accept=0.95,
            return_inferencedata=True,
        )
    return idata


def weighted_var(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Weighted variance along the last axis.

    values, weights: shape (..., n_cities). Weights need not be normalised.
    Returns: shape (...,) — weighted variance per row.
    """
    w_sum = weights.sum(axis=-1, keepdims=True)
    mean_w = (values * weights).sum(axis=-1, keepdims=True) / w_sum
    diff_sq = (values - mean_w) ** 2
    var_w = (diff_sq * weights).sum(axis=-1) / w_sum.squeeze(-1)
    return var_w


def compute_three_weightings(idata: az.InferenceData,
                              cities: pd.DataFrame) -> dict:
    """Compute f_within under three weightings; return draws + summary."""
    post = idata.posterior
    n_chains = post.sizes["chain"]
    n_draws = post.sizes["draw"]
    n_cities = len(cities)
    D = n_chains * n_draws

    within_dev = cities["log_pop_within"].to_numpy(dtype=float)         # (C,)
    population = cities["urban_context_pop_est"].to_numpy(dtype=float)  # (C,)
    inscriptions = cities["inscription_count"].to_numpy(dtype=float)    # (C,)
    log_mu = post["log_mu"].values.reshape(D, n_cities)                  # (D, C)
    beta_w = post["beta_within"].values.reshape(-1)                      # (D,)

    contrib_within = beta_w[:, None] * within_dev[None, :]                # (D, C)

    # Equal weights (unweighted) — recompute as a check that we match 05's f_within
    w_eq = np.ones(n_cities, dtype=float)
    w_eq_b = np.broadcast_to(w_eq, (D, n_cities))
    var_num_eq = weighted_var(contrib_within, w_eq_b)
    var_den_eq = weighted_var(log_mu, w_eq_b)
    f_unw = var_num_eq / var_den_eq

    # Population-weighted
    w_pop = np.broadcast_to(population, (D, n_cities))
    var_num_pop = weighted_var(contrib_within, w_pop)
    var_den_pop = weighted_var(log_mu, w_pop)
    f_popw = var_num_pop / var_den_pop

    # Inscription-weighted
    w_insc = np.broadcast_to(inscriptions, (D, n_cities))
    var_num_insc = weighted_var(contrib_within, w_insc)
    var_den_insc = weighted_var(log_mu, w_insc)
    f_inscw = var_num_insc / var_den_insc

    def summarise(draws: np.ndarray) -> dict:
        return {
            "median": float(np.median(draws)),
            "ci_lo": float(np.percentile(draws, 2.5)),
            "ci_hi": float(np.percentile(draws, 97.5)),
            "p_gt_005": float((draws > 0.05).mean()),
            "p_gt_010": float((draws > 0.10).mean()),
            "p_gt_020": float((draws > 0.20).mean()),
        }

    s_unw = summarise(f_unw)
    s_pop = summarise(f_popw)
    s_insc = summarise(f_inscw)

    medians = np.array([s_unw["median"], s_pop["median"], s_insc["median"]])
    median_spread = float(medians.max() - medians.min())
    material_divergence = median_spread > PRIMARY_CI_HALF_WIDTH

    return {
        "draws": {
            "f_within_unw": f_unw,
            "f_within_pop_w": f_popw,
            "f_within_insc_w": f_inscw,
        },
        "summary": {
            "unweighted": s_unw,
            "population_weighted": s_pop,
            "inscription_weighted": s_insc,
            "median_spread": median_spread,
            "primary_ci_half_width": PRIMARY_CI_HALF_WIDTH,
            "material_divergence": material_divergence,
        },
    }


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[block-6] HALT: filtered parquet missing at {DATA_PATH}.")
        return 1
    df = pd.read_parquet(DATA_PATH)
    print(f"[block-6] loaded {len(df):,} rows")

    cities, provinces = build_city_frame(df)
    print(f"[block-6] aggregated to {len(cities):,} cities; {len(provinces)} provinces")

    idata = fit_mundlak(cities, n_provinces=len(provinces))

    result = compute_three_weightings(idata, cities)
    summary = result["summary"]

    print("\n[block-6] THREE-WEIGHTING f_within RESULTS")
    for key in ("unweighted", "population_weighted", "inscription_weighted"):
        s = summary[key]
        print(f"  {key:24}  median = {s['median']:.4f}   "
              f"95% CI [{s['ci_lo']:.4f}, {s['ci_hi']:.4f}]   "
              f"P(f > 0.20) = {s['p_gt_020']:.4f}")
    print(f"  median spread across variants : {summary['median_spread']:.4f}")
    print(f"  primary CI half-width         : {summary['primary_ci_half_width']:.4f}")
    print(f"  material divergence flagged   : "
          f"{'YES' if summary['material_divergence'] else 'no'}")

    # Persist summary
    rows = []
    for key in ("unweighted", "population_weighted", "inscription_weighted"):
        s = summary[key]
        rows.append({"variant": key, **s})
    pd.DataFrame(rows).to_csv(
        TBL_DIR / "sensitivity-weighting-summary.csv", index=False)
    # Persist draws (concatenated)
    pd.DataFrame({
        "f_within_unweighted": result["draws"]["f_within_unw"],
        "f_within_population_weighted": result["draws"]["f_within_pop_w"],
        "f_within_inscription_weighted": result["draws"]["f_within_insc_w"],
    }).to_csv(TBL_DIR / "sensitivity-weighting-draws.csv", index=False)

    # Also save divergence + spread as a separate "decision" row
    pd.DataFrame([{
        "primary_ci_lo_05": PRIMARY_CI_LO,
        "primary_ci_hi_05": PRIMARY_CI_HI,
        "primary_ci_half_width": PRIMARY_CI_HALF_WIDTH,
        "median_spread_three_weighting": summary["median_spread"],
        "material_divergence": summary["material_divergence"],
        "decision": ("FLAG_AS_LIMITATION"
                     if summary["material_divergence"]
                     else "ROBUST_UNDER_WEIGHTING_SENSITIVITY"),
    }]).to_csv(TBL_DIR / "sensitivity-weighting-decision.csv", index=False)
    print(f"\n[block-6] wrote summary, draws, and decision tables")
    return 0


if __name__ == "__main__":
    sys.exit(main())
