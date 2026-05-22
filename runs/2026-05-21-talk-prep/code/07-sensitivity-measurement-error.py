#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07-sensitivity-measurement-error.py --- Phase A.2 of the RAC-TRAC 2026
talk-prep run.

Purpose
-------
Hanson-population measurement-error sensitivity (preregistered §5):
re-fit the Mundlak NBR with a normal measurement-error model on the
Hanson population predictor at sigma_pop in {0.1, 0.2, 0.3}.

Per the preregistration:
    log_pop_c ~ Normal(log_pop_observed_c, sigma_pop)

The latent log_pop_c then enters the Mundlak split (province-mean +
within-deviation). The Mundlak components are recomputed *within the
model* from the latent log_pop values so that sampling captures the
full uncertainty.

Preregistered decision rule (prereg §5):
    "Material divergence from the primary H3a result (posterior 95 %
    CI on f_within shifts by more than 50 % of its primary-result
    width under any sigma_pop) is flagged as a limitation."

Primary unweighted CI from 05: [0.240, 0.366]; width = 0.126;
50 % of that = 0.063. If the f_within posterior 95 % CI under any
sigma_pop shifts by more than 0.063 (in either bound) from the
primary, flag as material divergence.

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet

Outputs
-------
runs/2026-05-21-talk-prep/outputs/tables/sensitivity-measurement-error-summary.csv
runs/2026-05-21-talk-prep/outputs/tables/sensitivity-measurement-error-decision.csv

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

SIGMA_POP_GRID = [0.1, 0.2, 0.3]

# Primary unweighted f_within CI from 05 (for material-divergence check).
PRIMARY_CI_LO = 0.240
PRIMARY_CI_HI = 0.366
PRIMARY_CI_WIDTH = PRIMARY_CI_HI - PRIMARY_CI_LO       # 0.126
PRIMARY_CI_SHIFT_THRESHOLD = PRIMARY_CI_WIDTH / 2.0    # 0.063


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
    pcodes = pd.Categorical(agg["province"])
    agg["province_idx"] = pcodes.codes
    return agg, list(pcodes.categories)


def build_averaging_matrix(province_idx: np.ndarray,
                            n_provinces: int) -> np.ndarray:
    """Construct an (n_provinces, n_cities) averaging matrix M such that
    M @ x  =  per-province means of x (a city-indexed vector).

    Row k has 1 / n_k in positions where the city belongs to province k.
    """
    n_cities = len(province_idx)
    M = np.zeros((n_provinces, n_cities), dtype=float)
    counts = np.bincount(province_idx, minlength=n_provinces).astype(float)
    for c, k in enumerate(province_idx):
        M[k, c] = 1.0 / counts[k]
    return M


def fit_mundlak_with_mem(cities: pd.DataFrame,
                          n_provinces: int,
                          sigma_pop: float) -> az.InferenceData:
    """Mundlak NBR with measurement error on log(population).

    Generative model:
      log_pop_latent[c] ~ Normal(log_pop_observed[c], sigma_pop)
      log_pop_prov_mean[k] = average of log_pop_latent over cities in province k
      log_pop_within[c]    = log_pop_latent[c] - log_pop_prov_mean[province[c]]
      log_mu[c] = alpha_0 + alpha_prov[province[c]]
                  + beta_within * log_pop_within[c]
                  + beta_between * log_pop_prov_mean[province[c]]
      y[c] ~ NegBin(mu[c], dispersion)

    sigma_pop is FIXED (sensitivity parameter), not estimated.
    """
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    log_pop_obs = cities["log_pop"].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)
    n_cities = len(cities)

    M = build_averaging_matrix(province_idx, n_provinces)  # (P, C)

    with pm.Model() as model:
        # Measurement-error layer on log(population).
        log_pop_latent = pm.Normal(
            "log_pop_latent", mu=log_pop_obs, sigma=sigma_pop, shape=n_cities,
        )

        # Province means of the latent log_pop (recomputed each draw).
        log_pop_prov_mean = pm.math.dot(M, log_pop_latent)        # (P,)
        log_pop_prov_mean_per_city = log_pop_prov_mean[province_idx]  # (C,)
        log_pop_within = log_pop_latent - log_pop_prov_mean_per_city  # (C,)

        # Regression coefficients (preregistered priors).
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
            + beta_within * log_pop_within
            + beta_between * log_pop_prov_mean_per_city
        )
        mu = pm.math.exp(log_mu)
        pm.Deterministic("log_mu", log_mu)
        pm.Deterministic("log_pop_within", log_pop_within)
        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)

        print(f"[block-7] sampling NUTS @ sigma_pop = {sigma_pop}: "
              f"warmup={N_WARMUP}, draws={N_SAMPLE}, chains={N_CHAINS}")
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


def compute_f_within(idata: az.InferenceData) -> np.ndarray:
    """f_within per draw on the MEM-fitted posterior.

    Numerator: per-draw variance of beta_within * log_pop_within across cities.
    Denominator: per-draw variance of log_mu across cities.
    Both unweighted.
    """
    post = idata.posterior
    n_chains = post.sizes["chain"]
    n_draws = post.sizes["draw"]
    D = n_chains * n_draws

    beta_w = post["beta_within"].values.reshape(-1)                   # (D,)
    lp_within = post["log_pop_within"].values.reshape(D, -1)          # (D, C)
    log_mu = post["log_mu"].values.reshape(D, -1)                     # (D, C)

    contrib = beta_w[:, None] * lp_within                              # (D, C)
    var_num = contrib.var(axis=1, ddof=0)
    var_den = log_mu.var(axis=1, ddof=0)
    return var_num / var_den


def summarise_posterior(idata: az.InferenceData, f_within: np.ndarray) -> dict:
    summ = az.summary(idata, var_names=[
        "alpha_0", "beta_within", "beta_between", "sigma_prov", "dispersion",
    ])
    f_lo, f_hi = (float(x) for x in np.percentile(f_within, [2.5, 97.5]))
    return {
        "f_within_median": float(np.median(f_within)),
        "f_within_ci_lo": f_lo,
        "f_within_ci_hi": f_hi,
        "f_within_ci_width": f_hi - f_lo,
        "p_f_gt_005": float((f_within > 0.05).mean()),
        "p_f_gt_010": float((f_within > 0.10).mean()),
        "p_f_gt_020": float((f_within > 0.20).mean()),
        "max_rhat": float(summ["r_hat"].max()),
        "min_ess_bulk": float(summ["ess_bulk"].min()),
        "n_divergences": int(idata.sample_stats["diverging"].sum()),
    }


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[block-7] HALT: filtered parquet missing at {DATA_PATH}.")
        return 1
    df = pd.read_parquet(DATA_PATH)
    cities, provinces = build_city_frame(df)
    n_prov = len(provinces)
    print(f"[block-7] {len(cities):,} cities; {n_prov} provinces")

    rows = []
    for sigma_pop in SIGMA_POP_GRID:
        print(f"\n[block-7] === sigma_pop = {sigma_pop} ===")
        idata = fit_mundlak_with_mem(cities, n_prov, sigma_pop=sigma_pop)
        f_within = compute_f_within(idata)
        summ = summarise_posterior(idata, f_within)

        # Material divergence: shift in either CI bound vs primary > threshold
        shift_lo = abs(summ["f_within_ci_lo"] - PRIMARY_CI_LO)
        shift_hi = abs(summ["f_within_ci_hi"] - PRIMARY_CI_HI)
        max_shift = max(shift_lo, shift_hi)
        material = max_shift > PRIMARY_CI_SHIFT_THRESHOLD

        row = {
            "sigma_pop": sigma_pop,
            **summ,
            "primary_ci_lo": PRIMARY_CI_LO,
            "primary_ci_hi": PRIMARY_CI_HI,
            "shift_ci_lo": shift_lo,
            "shift_ci_hi": shift_hi,
            "max_shift": max_shift,
            "shift_threshold_50pc_width": PRIMARY_CI_SHIFT_THRESHOLD,
            "material_divergence": material,
            "decision": ("FLAG_AS_LIMITATION"
                         if material else "ROBUST_AT_THIS_SIGMA_POP"),
        }
        rows.append(row)

        print(f"  f_within median = {summ['f_within_median']:.4f}   "
              f"95% CI [{summ['f_within_ci_lo']:.4f}, {summ['f_within_ci_hi']:.4f}]")
        print(f"  CI width: {summ['f_within_ci_width']:.4f}   "
              f"max shift from primary: {max_shift:.4f}   "
              f"threshold: {PRIMARY_CI_SHIFT_THRESHOLD:.4f}")
        print(f"  P(f > 0.20) = {summ['p_f_gt_020']:.4f}")
        print(f"  R-hat = {summ['max_rhat']:.4f}   "
              f"min ESS_bulk = {summ['min_ess_bulk']:.0f}   "
              f"divergences = {summ['n_divergences']}")
        print(f"  decision: {row['decision']}")

    out_df = pd.DataFrame(rows)
    out_df.to_csv(TBL_DIR / "sensitivity-measurement-error-summary.csv",
                   index=False)
    print(f"\n[block-7] wrote summary across "
          f"{len(SIGMA_POP_GRID)} sigma_pop levels")

    # Overall decision
    any_material = bool(out_df["material_divergence"].any())
    print(f"\n[block-7] OVERALL DECISION (across sigma_pop grid)")
    print(f"  Any sigma_pop produces material divergence? "
          f"{'YES' if any_material else 'no'}")
    pd.DataFrame([{
        "any_material_divergence": any_material,
        "overall_decision": ("FLAG_AS_LIMITATION"
                              if any_material
                              else "ROBUST_UNDER_MEASUREMENT_ERROR_SENSITIVITY"),
        "sigma_pop_grid": str(SIGMA_POP_GRID),
        "primary_ci_lo": PRIMARY_CI_LO,
        "primary_ci_hi": PRIMARY_CI_HI,
        "shift_threshold": PRIMARY_CI_SHIFT_THRESHOLD,
    }]).to_csv(TBL_DIR / "sensitivity-measurement-error-decision.csv",
                index=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
