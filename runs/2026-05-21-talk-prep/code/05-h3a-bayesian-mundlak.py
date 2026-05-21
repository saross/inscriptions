#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05-h3a-bayesian-mundlak.py --- Block 4b (further stretch) of the
RAC-TRAC 2026 talk-prep run.

Purpose
-------
Bayesian within-between (Mundlak) negative-binomial regression of per-city
inscription count on Hanson 2016 urban population, with the population
predictor decomposed into a province-mean component and a within-province
deviation. Reports the binding H3a estimand:

  f_within = Var(beta_within * (log_pop_c - log_pop_province_mean[c]))
             / Var(log E[inscriptions_c])

computed per posterior draw and reported as a posterior distribution. The
prereg's three-way verdict on f_within is reported as preliminary
(post-lodgement) for the talk:

  Supported:        posterior 95% CI on f_within wholly above 0.10
  Evidence against: wholly below 0.10
  Inconclusive:     straddles 0.10

Plus the posterior-probability ladder P(f_within > 0.05), P(>0.10), P(>0.20).

Spec (preregistration-draft.md, lines 212-247)
----------------------------------------------
  y_c ~ NegativeBinomial(mu_c, dispersion)
  log(mu_c) = alpha_0 + alpha_province[c]
              + beta_within  * (log_pop_c - log_pop_province_mean[c])
              + beta_between * log_pop_province_mean[c]

  Priors (weakly-informative, preregistered):
    alpha_0      ~ Normal(0, 5)
    beta_within  ~ Normal(0, 1)
    beta_between ~ Normal(0, 1)
    alpha_prov   ~ Normal(0, sigma_prov)
    sigma_prov   ~ HalfNormal(1)
    1/dispersion ~ HalfNormal(1)

Sample
------
1,044 Hanson cities Rome-excluded (per Shawn's 2026-05-21 decision; text-spec
faithful per prereg §3, not the prereg's "~815" which inherited a stale
Latin-province filter --- see runs/2026-05-21-talk-prep/code/
01-filter-and-prep.py CITY_COUNT_NOTE).

Convergence gates (per prereg §4):
  - R-hat < 1.01 on all parameters
  - ESS_bulk >= 400 per chain on key parameters
  - 0 divergences

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet  (from Block 1)

Outputs
-------
runs/2026-05-21-talk-prep/outputs/figures/fig-06b-h3a-mundlak.png
runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv
runs/2026-05-21-talk-prep/outputs/tables/h3a-posterior-summary.csv

Mirrored to planning/conference-talk-rac-trac-2026/figures/.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-21, on Shawn's brief.
"""

from __future__ import annotations

import shutil
import sys
import warnings
from pathlib import Path

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = RUN_DIR / "data" / "lire-filtered.parquet"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"
TALK_FIG_DIR = PROJECT_ROOT / "planning" / "conference-talk-rac-trac-2026" / "figures"

for d in (FIG_DIR, TBL_DIR, TALK_FIG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Sampling settings (per prereg-style diagnostics).
# Initial run had R-hat = 1.0100 (exactly at the prereg's < 1.01 strict gate);
# 0 divergences, ESS_bulk = 1,060. Bumping tune from 1,000 -> 3,000 to nudge
# R-hat unambiguously under the gate (per Shawn's 2026-05-21 decision).
N_WARMUP = 3_000
N_SAMPLE = 2_000
N_CHAINS = 4
RANDOM_SEED = 20_260_521

FIG_SIZE_WIDE = (12.0, 7.5)
DPI = 200


# ---------------------------------------------------------------------------
# Data prep
# ---------------------------------------------------------------------------
def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def build_city_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to one row per Hanson-city (Rome-excluded) and attach the
    Mundlak components (province-mean log_pop, within-province deviation).
    """
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
    agg = agg.dropna(subset=["province"]).copy()  # require province assignment
    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    # Province-mean log_pop (averaged across the cities IN that province in
    # our sample --- the Mundlak centring).
    prov_means = agg.groupby("province")["log_pop"].transform("mean")
    agg["log_pop_prov_mean"] = prov_means
    agg["log_pop_within"] = agg["log_pop"] - prov_means
    # Province index for the random-intercept lookup.
    province_codes = pd.Categorical(agg["province"])
    agg["province_idx"] = province_codes.codes
    return agg, list(province_codes.categories)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def fit_mundlak(cities: pd.DataFrame, n_provinces: int) -> az.InferenceData:
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    log_pop_within = cities["log_pop_within"].to_numpy(dtype=float)
    log_pop_prov_mean = cities["log_pop_prov_mean"].to_numpy(dtype=float)
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
            + beta_within * log_pop_within
            + beta_between * log_pop_prov_mean
        )
        mu = pm.math.exp(log_mu)
        pm.Deterministic("log_mu", log_mu)

        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)

        print(f"[block-4b] sampling NUTS: warmup={N_WARMUP}, draws={N_SAMPLE}, "
              f"chains={N_CHAINS} ...")
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


# ---------------------------------------------------------------------------
# f_within estimand
# ---------------------------------------------------------------------------
def compute_f_within(idata: az.InferenceData, cities: pd.DataFrame) -> np.ndarray:
    """Compute f_within per posterior draw.

    f_within = Var(beta_within * within_dev) / Var(log E[insc])
    where:
      within_dev = log_pop_c - log_pop_province_mean[c]   (city-level data)
      log E[insc_c] = alpha_0 + alpha_prov[c] + beta_within * within_dev
                                              + beta_between * prov_mean

    Variances are computed unweighted across cities, per prereg §4.

    Returns an array of f_within draws (shape: n_chains * n_draws).
    """
    post = idata.posterior
    n_chains = post.sizes["chain"]
    n_draws = post.sizes["draw"]

    within_dev = cities["log_pop_within"].to_numpy(dtype=float)
    log_mu = post["log_mu"].values.reshape(n_chains * n_draws, -1)  # (D, C)
    beta_w = post["beta_within"].values.reshape(-1)                 # (D,)

    # Per-draw contribution from within-dev to log_mu (additive component):
    # beta_within * within_dev_c   --- but this varies by draw via beta_w only;
    # within_dev is fixed across draws.
    contrib_within = beta_w[:, None] * within_dev[None, :]          # (D, C)

    # Unweighted variance across cities per draw:
    var_num = contrib_within.var(axis=1, ddof=0)                    # (D,)
    var_den = log_mu.var(axis=1, ddof=0)                            # (D,)
    f_within = var_num / var_den
    return f_within


def verdict_from_ci(ci_lo: float, ci_hi: float, threshold: float = 0.10) -> str:
    """Three-way verdict per prereg §4 H3a decision rule."""
    if ci_lo > threshold:
        return "supported"
    if ci_hi < threshold:
        return "evidence-against"
    return "inconclusive"


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def render_figure(idata: az.InferenceData, cities: pd.DataFrame,
                  f_within_draws: np.ndarray, summary: dict) -> Path:
    fig, axes = plt.subplots(2, 2, figsize=FIG_SIZE_WIDE)
    post = idata.posterior

    # (0,0) beta_within posterior + beta_between
    ax = axes[0, 0]
    bw = post["beta_within"].values.flatten()
    bb = post["beta_between"].values.flatten()
    ax.hist(bw, bins=40, color="C0", alpha=0.65,
            label=f"beta_within  median = {np.median(bw):.3f}")
    ax.hist(bb, bins=40, color="C3", alpha=0.45,
            label=f"beta_between median = {np.median(bb):.3f}")
    ax.axvline(np.median(bw), color="C0", linewidth=1)
    ax.axvline(np.median(bb), color="C3", linewidth=1)
    ax.axvline(0, color="grey", linestyle="--", linewidth=0.8)
    ax.set_xlabel("coefficient value (log-count scale)")
    ax.set_ylabel("posterior density")
    ax.set_title("Mundlak coefficients", fontsize=11)
    ax.legend(loc="upper right", fontsize=8)

    # (0,1) f_within posterior with 0.10 threshold + ladder
    ax = axes[0, 1]
    ax.hist(f_within_draws, bins=50, color="C2", alpha=0.7)
    f_med = float(np.median(f_within_draws))
    f_lo, f_hi = np.percentile(f_within_draws, [2.5, 97.5])
    ax.axvspan(f_lo, f_hi, color="C2", alpha=0.15)
    ax.axvline(f_med, color="C2", linewidth=1.5,
               label=f"posterior median = {f_med:.3f}")
    ax.axvline(0.10, color="black", linestyle="--", linewidth=1.2,
               label="prereg threshold 0.10")
    ax.set_xlabel(r"$f_{within}$")
    ax.set_ylabel("posterior density")
    verdict = verdict_from_ci(float(f_lo), float(f_hi))
    ax.set_title(
        rf"$f_{{within}}$ posterior  --- 95% CI [{f_lo:.3f}, {f_hi:.3f}]  ---"
        f"  verdict (preliminary): **{verdict}**",
        fontsize=10,
    )
    ax.legend(loc="upper right", fontsize=8)

    # (1,0) f_within posterior-probability ladder
    ax = axes[1, 0]
    p_05 = float((f_within_draws > 0.05).mean())
    p_10 = float((f_within_draws > 0.10).mean())
    p_20 = float((f_within_draws > 0.20).mean())
    bars = ax.bar(["P(f > 0.05)", "P(f > 0.10)", "P(f > 0.20)"],
                  [p_05, p_10, p_20], color="C2", alpha=0.75)
    for b, v in zip(bars, [p_05, p_10, p_20]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}",
                ha="center", fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("posterior probability")
    ax.set_title("Posterior-probability ladder", fontsize=11)

    # (1,1) observed vs posterior-predicted scatter
    ax = axes[1, 1]
    log_mu_draws = post["log_mu"].values.reshape(-1, len(cities))
    pred_med = np.median(np.exp(log_mu_draws), axis=0)
    pred_lo = np.percentile(np.exp(log_mu_draws), 2.5, axis=0)
    pred_hi = np.percentile(np.exp(log_mu_draws), 97.5, axis=0)
    obs = cities["inscription_count"].to_numpy(dtype=float)
    ax.errorbar(
        obs, pred_med,
        yerr=[pred_med - pred_lo, pred_hi - pred_med],
        fmt="o", markersize=2.5, alpha=0.3, ecolor="lightgrey", color="C0",
    )
    lo = max(0.5, min(obs.min(), pred_med.min()))
    hi = max(obs.max(), pred_med.max())
    ax.plot([lo, hi], [lo, hi], color="black", linewidth=1, linestyle="--",
            label="y = x")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("observed inscription count")
    ax.set_ylabel("posterior median predicted count")
    ax.set_title(
        f"Posterior predictive check  ({len(cities):,} cities)", fontsize=11,
    )
    ax.legend(loc="upper left", fontsize=8)

    diag = (
        f"NUTS: chains={N_CHAINS}, warmup={N_WARMUP}, draws={N_SAMPLE}  ---  "
        f"max R-hat = {summary['max_rhat']:.4f} (gate < 1.01); "
        f"min ESS_bulk = {summary['min_ess_bulk']:.0f} (gate >= 400); "
        f"divergences = {summary['n_divergences']}"
    )
    fig.suptitle(
        "H3a Bayesian within-between (Mundlak) NBR --- preliminary "
        "post-lodgement results",
        fontsize=12, y=0.99,
    )
    fig.text(0.50, 0.01, diag, ha="center", fontsize=8, alpha=0.7)
    fig.text(
        0.99, 0.01,
        "preliminary, post-lodgement; the preregistered analysis is forthcoming",
        ha="right", fontsize=8, alpha=0.6,
    )

    out = FIG_DIR / "fig-06b-h3a-mundlak.png"
    fig.tight_layout(rect=(0, 0.025, 1, 0.965))
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-4b]   -> {out}")
    return out


def mirror_to_talk_dir(paths: list[Path]) -> None:
    for p in paths:
        dest = TALK_FIG_DIR / p.name
        shutil.copy2(p, dest)
        print(f"[block-4b]   mirrored -> {dest}")


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[block-4b] HALT: filtered parquet missing at {DATA_PATH}.")
        return 1
    df = pd.read_parquet(DATA_PATH)
    print(f"[block-4b] loaded {len(df):,} rows")

    cities, provinces = build_city_frame(df)
    n_prov = len(provinces)
    print(f"[block-4b] city sample: {len(cities):,} cities; {n_prov} provinces")

    idata = fit_mundlak(cities, n_provinces=n_prov)

    # Convergence
    summ_df = az.summary(idata, var_names=["alpha_0", "beta_within",
                                            "beta_between", "sigma_prov",
                                            "dispersion"])
    print("\n[block-4b] POSTERIOR SUMMARY (key parameters):")
    print(summ_df.to_string())

    max_rhat = float(summ_df["r_hat"].max())
    min_ess_bulk = float(summ_df["ess_bulk"].min())
    sample_stats = idata.sample_stats
    n_div = int(sample_stats["diverging"].sum())

    # f_within
    f_within = compute_f_within(idata, cities)
    f_med = float(np.median(f_within))
    f_lo, f_hi = (float(x) for x in np.percentile(f_within, [2.5, 97.5]))
    p_05 = float((f_within > 0.05).mean())
    p_10 = float((f_within > 0.10).mean())
    p_20 = float((f_within > 0.20).mean())
    verdict = verdict_from_ci(f_lo, f_hi)

    print(f"\n[block-4b] f_within posterior")
    print(f"    median  = {f_med:.4f}")
    print(f"    95% CI  = [{f_lo:.4f}, {f_hi:.4f}]")
    print(f"    P(f > 0.05) = {p_05:.4f}")
    print(f"    P(f > 0.10) = {p_10:.4f}")
    print(f"    P(f > 0.20) = {p_20:.4f}")
    print(f"    preliminary verdict: {verdict}")
    print(f"\n[block-4b] CONVERGENCE")
    print(f"    max R-hat       = {max_rhat:.4f}   (gate: < 1.01)")
    print(f"    min ESS_bulk    = {min_ess_bulk:.0f}   (gate: >= 400)")
    print(f"    divergences     = {n_div}")

    summary = {
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_div,
        "f_within_median": f_med,
        "f_within_ci_lo": f_lo,
        "f_within_ci_hi": f_hi,
        "p_f_gt_005": p_05,
        "p_f_gt_010": p_10,
        "p_f_gt_020": p_20,
        "verdict": verdict,
        "n_cities": len(cities),
        "n_provinces": n_prov,
        "n_chains": N_CHAINS,
        "n_warmup": N_WARMUP,
        "n_sample": N_SAMPLE,
    }
    pd.DataFrame([summary]).to_csv(TBL_DIR / "h3a-summary.csv", index=False)
    summ_df.to_csv(TBL_DIR / "h3a-posterior-summary.csv")

    fig_paths = [render_figure(idata, cities, f_within, summary)]
    mirror_to_talk_dir(fig_paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
