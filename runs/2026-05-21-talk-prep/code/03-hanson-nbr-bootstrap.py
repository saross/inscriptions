#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03-hanson-nbr-bootstrap.py --- Block 3 of the RAC-TRAC 2026 talk-prep run.

Purpose
-------
Frequentist Hanson-scaling comparator for slide #6: fit a negative-binomial
regression (NBR) of per-city inscription count on log urban population, with
a 1,000-replicate row-resample bootstrap 95% CI on the population coefficient.
Compares to:

  Hanson 2021         beta = 0.672, 95% CI [0.588, 0.756]   (554 sites, ex-Rome)
  Carleton et al 2025 beta in [0.3, 0.5] across the headline epigraphy spec;
                      epigraphy-no-zeros variant beta ~ 0.68

Both are OLS log-log specifications in the published comparators. The
preregistration (§4) specifies a Bayesian within-between (Mundlak) NBR; this
frequentist NBR is the empire-wide simpler comparator we present
"preliminary, post-lodgement; the preregistered analysis is forthcoming".

Critical-friend statistical notes (surfaced before commit)
----------------------------------------------------------
1. **NBR vs OLS log-log**: Hanson 2021 reports OLS log-log; the slope is
   the scaling exponent. NBR with log-population predictor and log link
   estimates the same exponent on the log-mean scale: log E[y] = a + b * log(pop)
   <=> E[y] proportional-to pop^b. We report BOTH to make the comparison
   transparent to the LIRE-creator audience in the room.
2. **Sample**: 1,044 Hanson-matched cities, Rome-excluded; all with N >= 1
   inscription (no structural zeros). The prereg's "~815" was a stale
   2024-notebook Latin-province subset --- see CITY_COUNT_NOTE in
   01-filter-and-prep.py. Per Shawn's 2026-05-21 decision: use the broader
   text-spec-faithful sample.
3. **Zero-count cities**: not represented in the LIRE parquet's per-row
   join (every LIRE row has an inscription; cities with 0 LIRE inscriptions
   simply don't appear). The full Hanson catalogue with 0-count cities is
   out of scope for this talk's frequentist comparator --- they are by
   construction included in the prereg's Bayesian H3a NBR which will see a
   different sample (and is itself a stretch goal for Block 4b).
4. **alpha estimation**: we use statsmodels.discrete.NegativeBinomial which
   jointly estimates the regression coefficients AND the dispersion alpha
   by MLE. This is the current best-practice choice vs the older
   GLM(family=NegativeBinomial(alpha=1)) shortcut.
5. **Bootstrap design**: we bootstrap by resampling inscription rows (with
   replacement), then re-aggregating to cities. This matches the 2024
   notebook's cell 197 and propagates within-city sampling variability;
   it does not perturb the city population estimates (treated as fixed).
   A city-level bootstrap is a separable robustness check, deferred.

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet  (from Block 1)

Outputs
-------
runs/2026-05-21-talk-prep/outputs/figures/fig-06-nbr-bootstrap.png
runs/2026-05-21-talk-prep/outputs/tables/nbr-summary.csv
runs/2026-05-21-talk-prep/outputs/tables/nbr-bootstrap-beta.csv

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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import NegativeBinomial

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Paths and constants
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

N_BOOTSTRAP = 1_000
RANDOM_SEED = 20_260_521
RNG = np.random.default_rng(RANDOM_SEED)

# Published comparators (for the figure annotation).
HANSON_2021 = {"beta": 0.672, "ci_lo": 0.588, "ci_hi": 0.756, "label": "Hanson 2021"}
CARLETON_2025 = {"beta_lo": 0.3, "beta_hi": 0.5, "epigraphy_no_zeros": 0.68,
                 "label": "Carleton et al. 2025"}

FIG_SIZE_WIDE = (12.0, 6.75)
DPI = 200


# ---------------------------------------------------------------------------
# Rome / city aggregation helpers
# ---------------------------------------------------------------------------
def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def aggregate_to_cities(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate the row-level filtered corpus to one row per Hanson-city.

    Returns a DataFrame with columns:
      urban_context_city          city name (toponym; the aggregation key)
      inscription_count           N inscriptions in this city under the prereg
                                  filter (Rome-excluded; no min-N gate)
      urban_context_pop_est       Hanson 2016 urban-area population estimate
                                  (joined into LIRE at row level by the LIRE
                                  team; constant per city given how the join
                                  was performed)
      log_pop                     natural log of urban_context_pop_est
      log_count                   natural log of inscription_count (for the
                                  OLS-log-log comparator)
      province                    modal province per city (informational)
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
    # Verify pop estimate is constant per city (sanity).
    pop_unique = sub.groupby("urban_context_city")["urban_context_pop_est"].nunique()
    n_inconsistent = int((pop_unique > 1).sum())
    if n_inconsistent > 0:
        print(
            f"[block-3] WARNING: {n_inconsistent} cities have multiple pop "
            "estimates across rows. Taking the first; investigate before "
            "preregistered analysis."
        )

    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    agg["log_count"] = np.log(agg["inscription_count"])
    return agg


# ---------------------------------------------------------------------------
# Model fits
# ---------------------------------------------------------------------------
def fit_nbr(cities: pd.DataFrame) -> dict:
    """Fit NBR: inscription_count ~ const + log_pop, joint MLE on alpha.

    Returns dict with beta_pop, se_pop, alpha, llf, n.
    """
    y = cities["inscription_count"].to_numpy(dtype=float)
    X = sm.add_constant(cities[["log_pop"]].to_numpy(dtype=float))
    model = NegativeBinomial(y, X)
    fit = model.fit(disp=False, maxiter=500)
    return {
        "beta_const": float(fit.params[0]),
        "beta_pop": float(fit.params[1]),
        "se_pop": float(fit.bse[1]),
        "alpha": float(fit.params[2]),  # dispersion (over-dispersion param)
        "llf": float(fit.llf),
        "n": int(len(cities)),
    }


def fit_ols_loglog(cities: pd.DataFrame) -> dict:
    """OLS log(count) ~ log(pop) --- the Hanson-2021 comparator spec."""
    y = cities["log_count"].to_numpy(dtype=float)
    X = sm.add_constant(cities[["log_pop"]].to_numpy(dtype=float))
    model = sm.OLS(y, X)
    fit = model.fit()
    return {
        "beta_const": float(fit.params[0]),
        "beta_pop": float(fit.params[1]),
        "se_pop": float(fit.bse[1]),
        "r2": float(fit.rsquared),
        "n": int(len(cities)),
    }


def bootstrap_nbr(rows_df: pd.DataFrame, n_reps: int = N_BOOTSTRAP) -> np.ndarray:
    """Row-resample bootstrap of NBR beta_pop.

    Resamples the per-row corpus (Rome-excluded, Hanson-joined) with
    replacement; re-aggregates to cities; refits NBR. Cities that the
    resample doesn't draw simply drop from that replicate.

    Returns
    -------
    np.ndarray of length n_reps; entries are beta_pop estimates.
    """
    sub_rows = rows_df.copy()
    n_rows = len(sub_rows)
    print(f"[block-3] bootstrap NBR: {n_reps} replicates on {n_rows:,} rows")
    betas = np.full(n_reps, np.nan, dtype=float)

    # Pre-materialise the join inputs.
    city_arr = sub_rows["urban_context_city"].to_numpy()
    pop_arr = sub_rows["urban_context_pop_est"].to_numpy(dtype=float)

    for b in range(n_reps):
        idx = RNG.integers(0, n_rows, size=n_rows)
        boot = pd.DataFrame({
            "urban_context_city": city_arr[idx],
            "urban_context_pop_est": pop_arr[idx],
        })
        # Re-aggregate
        agg = (
            boot.groupby("urban_context_city")
            .agg(
                inscription_count=("urban_context_city", "size"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
            )
            .reset_index()
        )
        agg["log_pop"] = np.log(agg["urban_context_pop_est"])
        try:
            y = agg["inscription_count"].to_numpy(dtype=float)
            X = sm.add_constant(agg[["log_pop"]].to_numpy(dtype=float))
            fit = NegativeBinomial(y, X).fit(disp=False, maxiter=500)
            betas[b] = float(fit.params[1])
        except Exception:
            betas[b] = np.nan  # non-convergence; rare
        if (b + 1) % 100 == 0:
            print(f"    .. {b + 1}/{n_reps} done; "
                  f"current 95% CI = "
                  f"[{np.nanpercentile(betas[:b+1], 2.5):.3f}, "
                  f"{np.nanpercentile(betas[:b+1], 97.5):.3f}]")
    n_failed = int(np.isnan(betas).sum())
    print(f"[block-3] bootstrap complete; {n_failed} non-converged replicates")
    return betas


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
def render_scatter_with_band(
    cities: pd.DataFrame,
    nbr_point: dict,
    ols_point: dict,
    boot_betas: np.ndarray,
) -> Path:
    """log-log scatter + NBR fitted line + bootstrap β band annotation."""
    fig, ax = plt.subplots(figsize=FIG_SIZE_WIDE)
    log_pop = cities["log_pop"].to_numpy()
    log_count = cities["log_count"].to_numpy()
    ax.scatter(
        log_pop, log_count, alpha=0.35, s=18, color="C0",
        edgecolor="none", label=f"{len(cities)} cities (Rome ex.)",
    )
    # NBR fitted line on the log E[y] scale.
    xs = np.linspace(log_pop.min(), log_pop.max(), 200)
    ys_nbr = nbr_point["beta_const"] + nbr_point["beta_pop"] * xs
    ax.plot(
        xs, ys_nbr, color="C3", linewidth=1.8,
        label=(f"NBR fit  beta_pop = {nbr_point['beta_pop']:.3f}  "
               f"(95% CI [{np.nanpercentile(boot_betas, 2.5):.3f}, "
               f"{np.nanpercentile(boot_betas, 97.5):.3f}])"),
    )
    # OLS log-log line.
    ys_ols = ols_point["beta_const"] + ols_point["beta_pop"] * xs
    ax.plot(
        xs, ys_ols, color="C2", linewidth=1.5, linestyle="--",
        label=(f"OLS log-log  beta_pop = {ols_point['beta_pop']:.3f}  "
               f"(R^2 = {ols_point['r2']:.3f})"),
    )
    # Reference: Hanson 2021 beta = 0.672.
    ax.axhline(np.nan)  # no-op anchor
    ax.set_xlabel("log(Hanson 2016 urban population)")
    ax.set_ylabel("log(LIRE inscription count)")
    ax.set_title(
        f"Hanson-scaling fit on date-window-filtered LIRE counts "
        f"(N = {len(cities):,} Hanson cities, Rome excluded)",
        fontsize=12,
    )
    # Comparator panel.
    txt = (
        "Comparators (published):\n"
        f"  Hanson 2021         beta = {HANSON_2021['beta']:.3f} "
        f"[{HANSON_2021['ci_lo']:.3f}, {HANSON_2021['ci_hi']:.3f}]\n"
        f"  Carleton et al. 2025  beta in [{CARLETON_2025['beta_lo']:.1f}, "
        f"{CARLETON_2025['beta_hi']:.1f}]; no-zeros ~ {CARLETON_2025['epigraphy_no_zeros']:.2f}"
    )
    ax.text(
        0.02, 0.98, txt, transform=ax.transAxes, fontsize=9, va="top",
        bbox={"facecolor": "white", "edgecolor": "grey", "alpha": 0.85},
    )
    ax.text(
        0.99, 0.02,
        "preliminary, post-lodgement; the preregistered analysis is forthcoming",
        transform=ax.transAxes, fontsize=8, alpha=0.6, ha="right",
    )
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.2)
    out = FIG_DIR / "fig-06-nbr-bootstrap.png"
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-3]   -> {out}")
    return out


def mirror_to_talk_dir(paths: list[Path]) -> None:
    for p in paths:
        dest = TALK_FIG_DIR / p.name
        shutil.copy2(p, dest)
        print(f"[block-3]   mirrored -> {dest}")


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[block-3] HALT: filtered parquet missing at {DATA_PATH}.")
        return 1
    df = pd.read_parquet(DATA_PATH)
    print(f"[block-3] loaded {len(df):,} rows")

    # Subset to the Block-3 sample: ex-Rome, has Hanson pop estimate.
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    rows_for_nbr = df.loc[~rome & has_hanson].copy()
    print(f"[block-3] Block-3 row sample: {len(rows_for_nbr):,} inscriptions "
          f"(ex-Rome, has Hanson pop)")

    cities = aggregate_to_cities(df)
    print(f"[block-3] aggregated to {len(cities):,} cities")
    print(f"[block-3] city N stats: "
          f"min={cities['inscription_count'].min()}, "
          f"max={cities['inscription_count'].max()}, "
          f"median={cities['inscription_count'].median():.0f}")

    nbr_point = fit_nbr(cities)
    ols_point = fit_ols_loglog(cities)
    print(f"\n[block-3] POINT ESTIMATES")
    print(f"    NBR  beta_pop = {nbr_point['beta_pop']:.4f}   "
          f"se = {nbr_point['se_pop']:.4f}   alpha = {nbr_point['alpha']:.4f}   "
          f"n = {nbr_point['n']}")
    print(f"    OLS  beta_pop = {ols_point['beta_pop']:.4f}   "
          f"se = {ols_point['se_pop']:.4f}   R^2 = {ols_point['r2']:.4f}   "
          f"n = {ols_point['n']}")

    boot_betas = bootstrap_nbr(rows_for_nbr, n_reps=N_BOOTSTRAP)
    ci_lo = float(np.nanpercentile(boot_betas, 2.5))
    ci_hi = float(np.nanpercentile(boot_betas, 97.5))
    ci_med = float(np.nanmedian(boot_betas))
    print(f"\n[block-3] BOOTSTRAP NBR beta_pop")
    print(f"    median = {ci_med:.4f}")
    print(f"    95% CI = [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"    point  = {nbr_point['beta_pop']:.4f}")
    print(f"\n[block-3] COMPARATORS (published)")
    print(f"    Hanson 2021         beta = {HANSON_2021['beta']:.3f} "
          f"[{HANSON_2021['ci_lo']:.3f}, {HANSON_2021['ci_hi']:.3f}]")
    print(f"    Carleton et al 2025 beta in [{CARLETON_2025['beta_lo']:.1f}, "
          f"{CARLETON_2025['beta_hi']:.1f}]; no-zeros ~ "
          f"{CARLETON_2025['epigraphy_no_zeros']:.2f}")

    # Persist tables.
    pd.DataFrame([
        {"model": "NBR", **nbr_point, "boot_ci_lo": ci_lo, "boot_ci_hi": ci_hi,
         "boot_median": ci_med},
        {"model": "OLS_loglog", **ols_point, "boot_ci_lo": np.nan,
         "boot_ci_hi": np.nan, "boot_median": np.nan},
    ]).to_csv(TBL_DIR / "nbr-summary.csv", index=False)
    pd.DataFrame({"bootstrap_beta_pop": boot_betas}).to_csv(
        TBL_DIR / "nbr-bootstrap-beta.csv", index=False,
    )

    # Figure.
    fig_paths = [render_scatter_with_band(cities, nbr_point, ols_point, boot_betas)]
    mirror_to_talk_dir(fig_paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
