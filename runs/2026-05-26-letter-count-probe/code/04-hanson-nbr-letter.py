#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04-hanson-nbr-letter.py --- Block 4 of the 2026-05-26 letter-count probe.

Purpose
-------
Frequentist NBR Hanson-scaling comparator under three response variants:

  (1) y = inscription_count(city)              --- matches 2026-05-21 talk-prep.
  (2) y = sum letter_count_conservative(city)  --- new.
  (3) y = sum letter_count_interpretive(city)  --- new.

For each variant: fit NegativeBinomial(y ~ const + log(Hanson pop)); run a
1,000-replicate row-resample bootstrap; emit beta_pop with 95 % CI and
overlap diagnostics.

Verdict flag 2 (spec §"Verdict thresholds")
-------------------------------------------
"No meaningful change":  point estimate of one variant's beta_pop falls
                         inside the other variant's 95 % CI.
"Material change":       no overlap between the 95 % CI of the inscription-
                         count variant and EITHER letter-mass variant.

Inputs
------
runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet

Outputs
-------
outputs/tables/nbr-summary.csv          --- per-variant beta_pop + 95 % CI,
                                             alpha (dispersion), n cities.
outputs/tables/nbr-bootstrap-betas.csv  --- columns one per variant; rows
                                             are bootstrap replicates.
outputs/figures/fig-04a-nbr-forest.png  --- forest plot, three rows, with
                                             Hanson 2021 and Carleton 2025
                                             reference annotations.
outputs/figures/fig-04b-nbr-scatter-grid.png --- 3-panel scatter (log-log)
                                             with fitted line + CI band per
                                             variant; same cities, different
                                             y-axes.

Reproducibility
---------------
RANDOM_SEED = 20260526
N_BOOTSTRAP = 1,000

Date
----
2026-05-26
"""

from __future__ import annotations

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

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
INPUT_PATH = RUN_DIR / "data" / "lire-filtered-with-letters.parquet"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"

for d in (FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)

N_BOOTSTRAP = 1_000
RANDOM_SEED = 20260526
RNG = np.random.default_rng(RANDOM_SEED)

# Published comparators (for the figure annotation).
HANSON_2021 = {"beta": 0.672, "ci_lo": 0.588, "ci_hi": 0.756, "label": "Hanson 2021"}
CARLETON_2025 = {"beta_lo": 0.3, "beta_hi": 0.5, "label": "Carleton 2025"}

FIG_SIZE_WIDE = (12.0, 6.75)
DPI = 200

VARIANTS = [
    {"key": "inscription",
     "label": "inscription count",
     "letter_col": None},   # weight = 1.0
    {"key": "letter_cons",
     "label": "letter total (conservative)",
     "letter_col": "letter_count_conservative"},
    {"key": "letter_intr",
     "label": "letter total (interpretive)",
     "letter_col": "letter_count_interpretive"},
]


# ---------------------------------------------------------------------------
def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def aggregate_to_cities(df: pd.DataFrame, letter_col: str | None) -> pd.DataFrame:
    """Aggregate row-level corpus to per-city response.

    If `letter_col` is None, response = inscription_count. Otherwise,
    response = sum(letter_col).

    Returns DataFrame with columns: urban_context_city, response,
    urban_context_pop_est, log_pop, log_response (NaN where response == 0).
    """
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    sub = df.loc[~rome & has_hanson].copy()

    if letter_col is None:
        agg_kwargs = {
            "response": ("urban_context_city", "size"),
            "urban_context_pop_est": ("urban_context_pop_est", "first"),
        }
    else:
        agg_kwargs = {
            "response": (letter_col, "sum"),
            "urban_context_pop_est": ("urban_context_pop_est", "first"),
        }
    agg = sub.groupby("urban_context_city").agg(**agg_kwargs).reset_index()

    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    # log_response: NaN for zero-response cities; only used by the OLS comparator.
    with np.errstate(divide="ignore"):
        agg["log_response"] = np.log(agg["response"].replace(0, np.nan))
    return agg


def fit_nbr(cities: pd.DataFrame) -> dict:
    """Fit NBR: response ~ const + log_pop, joint MLE on alpha."""
    y = cities["response"].to_numpy(dtype=float)
    X = sm.add_constant(cities[["log_pop"]].to_numpy(dtype=float))
    model = NegativeBinomial(y, X)
    fit = model.fit(disp=False, maxiter=500)
    return {
        "beta_const": float(fit.params[0]),
        "beta_pop": float(fit.params[1]),
        "se_pop": float(fit.bse[1]),
        "alpha": float(fit.params[2]),
        "llf": float(fit.llf),
        "n": int(len(cities)),
        "n_zero_response": int((cities["response"] == 0).sum()),
    }


def fit_ols_loglog(cities: pd.DataFrame) -> dict:
    """OLS comparator: log(response) ~ const + log(pop); drops zero-response."""
    sub = cities.dropna(subset=["log_response"]).copy()
    y = sub["log_response"].to_numpy(dtype=float)
    X = sm.add_constant(sub[["log_pop"]].to_numpy(dtype=float))
    fit = sm.OLS(y, X).fit()
    return {
        "beta_const": float(fit.params[0]),
        "beta_pop": float(fit.params[1]),
        "se_pop": float(fit.bse[1]),
        "r2": float(fit.rsquared),
        "n": int(len(sub)),
        "n_dropped_zero": int(len(cities) - len(sub)),
    }


def bootstrap_nbr(rows_df: pd.DataFrame, letter_col: str | None,
                  n_reps: int = N_BOOTSTRAP) -> tuple[np.ndarray, np.ndarray]:
    """Row-resample bootstrap of NBR (const, beta_pop) pairs.

    Resamples per-row corpus with replacement; re-aggregates per city; refits.
    """
    sub_rows = rows_df.copy()
    n_rows = len(sub_rows)
    print(f"  bootstrap NBR ({letter_col or 'unit'}): {n_reps} reps on {n_rows:,} rows")
    consts = np.full(n_reps, np.nan, dtype=float)
    betas = np.full(n_reps, np.nan, dtype=float)

    city_arr = sub_rows["urban_context_city"].to_numpy()
    pop_arr = sub_rows["urban_context_pop_est"].to_numpy(dtype=float)
    if letter_col is None:
        # Unit weights; we use a column of ones materialised once.
        weight_arr = np.ones(n_rows, dtype=float)
    else:
        weight_arr = sub_rows[letter_col].to_numpy(dtype=float)

    for b in range(n_reps):
        idx = RNG.integers(0, n_rows, size=n_rows)
        boot = pd.DataFrame({
            "urban_context_city": city_arr[idx],
            "urban_context_pop_est": pop_arr[idx],
            "weight": weight_arr[idx],
        })
        agg = (
            boot.groupby("urban_context_city")
            .agg(
                response=("weight", "sum"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
            )
            .reset_index()
        )
        agg["log_pop"] = np.log(agg["urban_context_pop_est"])
        try:
            y = agg["response"].to_numpy(dtype=float)
            X = sm.add_constant(agg[["log_pop"]].to_numpy(dtype=float))
            fit = NegativeBinomial(y, X).fit(disp=False, maxiter=500)
            consts[b] = float(fit.params[0])
            betas[b] = float(fit.params[1])
        except Exception:
            consts[b] = np.nan
            betas[b] = np.nan
        if (b + 1) % 200 == 0:
            print(
                f"    .. {b + 1}/{n_reps}; current 95 % CI on beta = "
                f"[{np.nanpercentile(betas[:b+1], 2.5):.3f}, "
                f"{np.nanpercentile(betas[:b+1], 97.5):.3f}]"
            )
    n_failed = int(np.isnan(betas).sum())
    print(f"  bootstrap complete; {n_failed} non-converged replicates")
    return consts, betas


def render_forest(point_results: list[dict],
                  boot_betas_dict: dict[str, np.ndarray]) -> Path:
    """Forest plot: one row per variant, with Hanson 2021 + Carleton 2025
    reference bands annotated.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Hanson 2021 reference band.
    ax.axvspan(HANSON_2021["ci_lo"], HANSON_2021["ci_hi"], color="#bbbbbb",
               alpha=0.30, label="Hanson 2021 95 % CI")
    ax.axvline(HANSON_2021["beta"], color="#666666", linewidth=1.0,
               linestyle=":", label=f"Hanson 2021 beta = {HANSON_2021['beta']:.3f}")
    ax.axvspan(CARLETON_2025["beta_lo"], CARLETON_2025["beta_hi"],
               color="#f4d35e", alpha=0.20,
               label=f"Carleton 2025 headline range [{CARLETON_2025['beta_lo']:.1f}, "
                     f"{CARLETON_2025['beta_hi']:.1f}]")

    colours = ["#264653", "#e76f51", "#2a9d8f"]
    y_positions = np.arange(len(point_results))
    for i, (pt, colour) in enumerate(zip(point_results, colours)):
        key = pt["key"]
        betas = boot_betas_dict[key]
        ci_lo = float(np.nanpercentile(betas, 2.5))
        ci_hi = float(np.nanpercentile(betas, 97.5))
        ax.plot([ci_lo, ci_hi], [i, i], color=colour, linewidth=3, alpha=0.65)
        ax.scatter([pt["beta_pop"]], [i], color=colour, s=80, zorder=5)
        ax.text(
            ci_hi + 0.02, i,
            f"beta = {pt['beta_pop']:.3f}  95 % CI [{ci_lo:.3f}, {ci_hi:.3f}]  "
            f"alpha = {pt['alpha']:.2f}",
            va="center", fontsize=9,
        )
    ax.set_yticks(y_positions)
    ax.set_yticklabels([r["label"] for r in point_results], fontsize=10)
    ax.set_xlabel("beta_pop  (NBR slope on log Hanson population)")
    ax.set_title(
        "Hanson scaling exponent: inscription count vs letter mass\n"
        "(3-variant NBR fit, 1 000-rep row-resample bootstrap)",
        fontsize=12,
    )
    ax.set_xlim(0.2, 1.4)
    ax.invert_yaxis()
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "fig-04a-nbr-forest.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  forest -> {out.relative_to(PROJECT_ROOT)}")
    return out


def render_scatter_grid(point_results: list[dict],
                        ols_results: list[dict],
                        boot_consts_dict: dict[str, np.ndarray],
                        boot_betas_dict: dict[str, np.ndarray],
                        city_tables: list[pd.DataFrame]) -> Path:
    """3-panel log-log scatter with fitted line + bootstrap CI band, one per
    variant. y-axes differ but x-axis is shared (log Hanson population).
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharex=True)
    colours = ["#264653", "#e76f51", "#2a9d8f"]
    for ax, pt, ols, boot_const, boot_beta, cities, colour in zip(
        axes, point_results, ols_results,
        [boot_consts_dict[r["key"]] for r in point_results],
        [boot_betas_dict[r["key"]] for r in point_results],
        city_tables, colours,
    ):
        log_pop = cities["log_pop"].to_numpy()
        log_resp = cities["log_response"].to_numpy()
        non_nan = ~np.isnan(log_resp)
        ax.scatter(log_pop[non_nan], log_resp[non_nan], s=12, alpha=0.30,
                   color=colour, edgecolor="none")
        xs = np.linspace(np.nanmin(log_pop), np.nanmax(log_pop), 200)
        mask = ~np.isnan(boot_const) & ~np.isnan(boot_beta)
        lines = boot_const[mask, None] + boot_beta[mask, None] * xs[None, :]
        band_lo = np.percentile(lines, 2.5, axis=0)
        band_hi = np.percentile(lines, 97.5, axis=0)
        ax.fill_between(xs, band_lo, band_hi, color=colour, alpha=0.20)
        ys = pt["beta_const"] + pt["beta_pop"] * xs
        ax.plot(xs, ys, color=colour, linewidth=1.8,
                label=f"NBR  beta = {pt['beta_pop']:.3f}")
        ys_ols = ols["beta_const"] + ols["beta_pop"] * xs
        ax.plot(xs, ys_ols, color="#444444", linewidth=1.2, linestyle="--",
                label=f"OLS  beta = {ols['beta_pop']:.3f}  R^2 = {ols['r2']:.2f}")
        ax.set_xlabel("log(Hanson population)")
        ax.set_ylabel(f"log({pt['label']})")
        ax.set_title(f"{pt['label']}\n(n = {pt['n']:,} cities; "
                     f"{ols['n_dropped_zero']} dropped for OLS)",
                     fontsize=10)
        ax.legend(loc="lower right", fontsize=8)
    fig.suptitle(
        "Hanson log-log scatter under three response variants",
        fontsize=12, y=1.02,
    )
    fig.tight_layout()
    out = FIG_DIR / "fig-04b-nbr-scatter-grid.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  scatter grid -> {out.relative_to(PROJECT_ROOT)}")
    return out


def annotate_flag2(ci_a: tuple[float, float], pt_b: float,
                   ci_b: tuple[float, float], pt_a: float) -> str:
    """Verdict-flag-2 evaluation for one pair of variants."""
    # Does pt_b fall inside ci_a? Does pt_a fall inside ci_b?
    b_inside_a = ci_a[0] <= pt_b <= ci_a[1]
    a_inside_b = ci_b[0] <= pt_a <= ci_b[1]
    # CI overlap?
    overlap = max(0.0, min(ci_a[1], ci_b[1]) - max(ci_a[0], ci_b[0]))
    no_overlap = overlap == 0.0
    if b_inside_a and a_inside_b:
        return "FLAG-2 NO-CHANGE (each point inside other's 95 % CI)"
    if no_overlap:
        return "FLAG-2 MATERIAL (no CI overlap)"
    return "FLAG-2 MODEST (CIs overlap but a point sits outside the other CI)"


def main():
    if not INPUT_PATH.exists():
        sys.exit(f"FATAL: input parquet not found at {INPUT_PATH}; run 01 first.")

    df = pd.read_parquet(INPUT_PATH)
    print(f"Loaded {len(df):,} rows.")

    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    rows_for_boot = df.loc[~rome & has_hanson].copy()
    print(f"  Rome-excluded + Hanson-matched rows: {len(rows_for_boot):,}")

    # Point estimates per variant.
    point_results = []
    ols_results = []
    city_tables = []
    boot_consts_dict = {}
    boot_betas_dict = {}

    for v in VARIANTS:
        print(f"\n=== variant: {v['key']} ({v['label']}) ===")
        cities = aggregate_to_cities(df, v["letter_col"])
        print(f"  cities: {len(cities):,}  "
              f"({int((cities['response'] == 0).sum())} with zero response)")
        nbr = fit_nbr(cities)
        ols = fit_ols_loglog(cities)
        print(f"  NBR : beta_pop = {nbr['beta_pop']:.4f}  "
              f"se = {nbr['se_pop']:.4f}  alpha = {nbr['alpha']:.3f}")
        print(f"  OLS : beta_pop = {ols['beta_pop']:.4f}  R^2 = {ols['r2']:.4f}  "
              f"(n={ols['n']:,}; {ols['n_dropped_zero']} dropped for log(0))")
        boot_consts, boot_betas = bootstrap_nbr(rows_for_boot, v["letter_col"])
        boot_consts_dict[v["key"]] = boot_consts
        boot_betas_dict[v["key"]] = boot_betas
        nbr["key"] = v["key"]
        nbr["label"] = v["label"]
        nbr["ci_lo"] = float(np.nanpercentile(boot_betas, 2.5))
        nbr["ci_hi"] = float(np.nanpercentile(boot_betas, 97.5))
        point_results.append(nbr)
        ols_results.append(ols)
        city_tables.append(cities)

    # ----------------------------------- summary tables
    summary = pd.DataFrame([
        {
            "variant": r["key"],
            "label": r["label"],
            "n_cities": r["n"],
            "n_zero_response": r["n_zero_response"],
            "beta_pop": r["beta_pop"],
            "se_pop": r["se_pop"],
            "alpha": r["alpha"],
            "ci_lo_2p5": r["ci_lo"],
            "ci_hi_97p5": r["ci_hi"],
        }
        for r in point_results
    ])
    summary.to_csv(TBL_DIR / "nbr-summary.csv", index=False, float_format="%.4f")

    boot_tbl = pd.DataFrame({r["key"]: boot_betas_dict[r["key"]] for r in point_results})
    boot_tbl.to_csv(TBL_DIR / "nbr-bootstrap-betas.csv", index=False, float_format="%.4f")

    print("\nNBR summary:")
    print(summary.to_string(index=False))

    # ----------------------------------- verdict flag 2
    print("\nFLAG 2 (Hanson beta CI overlap):")
    pr_i, pr_c, pr_p = point_results
    print("  inscription vs letter_conservative: " + annotate_flag2(
        (pr_i["ci_lo"], pr_i["ci_hi"]), pr_c["beta_pop"],
        (pr_c["ci_lo"], pr_c["ci_hi"]), pr_i["beta_pop"]))
    print("  inscription vs letter_interpretive: " + annotate_flag2(
        (pr_i["ci_lo"], pr_i["ci_hi"]), pr_p["beta_pop"],
        (pr_p["ci_lo"], pr_p["ci_hi"]), pr_i["beta_pop"]))

    # ----------------------------------- figures
    render_forest(point_results, boot_betas_dict)
    render_scatter_grid(point_results, ols_results,
                        boot_consts_dict, boot_betas_dict, city_tables)

    print("\nDone.")


if __name__ == "__main__":
    main()
