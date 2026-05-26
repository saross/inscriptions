#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05-within-province-variance-partition.py --- Block 5 of the 2026-05-26
letter-count probe.

Purpose
-------
Frequentist Mundlak within-between variance partition under three response
variants:

  (1) y = inscription_count(city)
  (2) y = sum letter_count_conservative(city)
  (3) y = sum letter_count_interpretive(city)

Model spec (frequentist analogue of the prereg's Bayesian Mundlak NBR for
H3a, with random province intercepts replaced by no province-level random
effect --- the variance attributable to log-population can still be
decomposed cleanly between within and between components even in a fixed-
effects spec):

  log E[y_c] = a_0 + beta_within  * (log_pop_c - log_pop_prov_mean[c])
                  + beta_between * log_pop_prov_mean[c]

  f_within = (beta_within  * sd(log_pop_c - log_pop_prov_mean[c]))^2
             / [ (beta_within  * sd(log_pop_c - log_pop_prov_mean[c]))^2
               + (beta_between * sd(log_pop_prov_mean[c]))^2 ]

Why a frequentist analogue rather than the full Bayesian Mundlak NBR? This
is a probe, not a preregistered fit. If letter-count materially shifts the
within-share, Stage 3 inherits the unit choice and the full Bayesian Mundlak
is rerun on the chosen unit. If the partitions agree across units, we have
the flag-3 verdict already.

Verdict flag 3 (spec §"Verdict thresholds")
-------------------------------------------
"No meaningful change":  within-share shift < 2 pp from inscription-count
                         baseline.
"Material change":       shift > 5 pp.
"Modest":                2 pp <= shift <= 5 pp.

Bootstrap
---------
500-replicate row-resample bootstrap on f_within per variant. Bootstrap CI
on the within-share is compared against the inscription-count point estimate
to apply the verdict rule.

Inputs
------
runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet

Outputs
-------
outputs/tables/variance-partition.csv    --- per-variant beta_within,
                                              beta_between, f_within point
                                              + 95 % CI.
outputs/figures/fig-05-variance-partition-bars.png  --- three stacked bars
                                              with bootstrap CIs.

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

N_BOOTSTRAP = 500
RANDOM_SEED = 20260526
RNG = np.random.default_rng(RANDOM_SEED)

VARIANTS = [
    {"key": "inscription",
     "label": "inscription count",
     "letter_col": None},
    {"key": "letter_cons",
     "label": "letter total (conservative)",
     "letter_col": "letter_count_conservative"},
    {"key": "letter_intr",
     "label": "letter total (interpretive)",
     "letter_col": "letter_count_interpretive"},
]


def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def aggregate_with_mundlak(df: pd.DataFrame, letter_col: str | None
                           ) -> pd.DataFrame | None:
    """Aggregate to per-city + add log-pop within/between columns."""
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    has_prov = df["province"].notna()
    sub = df.loc[~rome & has_hanson & has_prov].copy()

    if letter_col is None:
        agg_kwargs = {
            "response": ("urban_context_city", "size"),
            "urban_context_pop_est": ("urban_context_pop_est", "first"),
            "province": ("province", lambda x: x.mode()[0] if len(x.mode()) else None),
        }
    else:
        agg_kwargs = {
            "response": (letter_col, "sum"),
            "urban_context_pop_est": ("urban_context_pop_est", "first"),
            "province": ("province", lambda x: x.mode()[0] if len(x.mode()) else None),
        }
    agg = sub.groupby("urban_context_city").agg(**agg_kwargs).reset_index()
    agg = agg.dropna(subset=["province"])
    if len(agg) == 0:
        return None

    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    # Province-mean log population.
    prov_mean = agg.groupby("province")["log_pop"].mean()
    agg["log_pop_prov_mean"] = agg["province"].map(prov_mean)
    agg["log_pop_within"] = agg["log_pop"] - agg["log_pop_prov_mean"]
    return agg


def fit_mundlak_nbr(cities: pd.DataFrame) -> dict:
    """Fit NBR with within + between decomposition."""
    y = cities["response"].to_numpy(dtype=float)
    # Predictors: const, beta_within, beta_between.
    X = sm.add_constant(
        cities[["log_pop_within", "log_pop_prov_mean"]].to_numpy(dtype=float)
    )
    fit = NegativeBinomial(y, X).fit(disp=False, maxiter=500)
    beta_within = float(fit.params[1])
    beta_between = float(fit.params[2])
    sd_within = float(cities["log_pop_within"].std(ddof=1))
    sd_between = float(cities["log_pop_prov_mean"].std(ddof=1))
    var_within = (beta_within * sd_within) ** 2
    var_between = (beta_between * sd_between) ** 2
    f_within = var_within / (var_within + var_between) if (var_within + var_between) > 0 else np.nan
    return {
        "beta_within": beta_within,
        "beta_between": beta_between,
        "sd_log_pop_within": sd_within,
        "sd_log_pop_between": sd_between,
        "var_within": var_within,
        "var_between": var_between,
        "f_within": f_within,
        "n": int(len(cities)),
        "alpha": float(fit.params[3]),
    }


def bootstrap_partition(rows_df: pd.DataFrame, letter_col: str | None,
                        n_reps: int = N_BOOTSTRAP) -> np.ndarray:
    """Row-resample bootstrap of f_within."""
    n_rows = len(rows_df)
    print(f"  bootstrap variance-partition ({letter_col or 'unit'}): "
          f"{n_reps} reps on {n_rows:,} rows")
    f_within_boot = np.full(n_reps, np.nan, dtype=float)
    cols_to_keep = ["urban_context_city", "urban_context_pop_est", "province"]
    if letter_col is not None:
        cols_to_keep.append(letter_col)
    src = rows_df[cols_to_keep].reset_index(drop=True)

    for b in range(n_reps):
        idx = RNG.integers(0, n_rows, size=n_rows)
        boot = src.iloc[idx].copy()
        # Aggregate.
        if letter_col is None:
            agg = boot.groupby("urban_context_city").agg(
                response=("urban_context_city", "size"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
                province=("province", lambda x: x.mode()[0] if len(x.mode()) else None),
            ).reset_index()
        else:
            agg = boot.groupby("urban_context_city").agg(
                response=(letter_col, "sum"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
                province=("province", lambda x: x.mode()[0] if len(x.mode()) else None),
            ).reset_index()
        agg = agg.dropna(subset=["province"])
        if len(agg) < 30:
            continue
        agg["log_pop"] = np.log(agg["urban_context_pop_est"])
        prov_mean = agg.groupby("province")["log_pop"].mean()
        agg["log_pop_prov_mean"] = agg["province"].map(prov_mean)
        agg["log_pop_within"] = agg["log_pop"] - agg["log_pop_prov_mean"]
        try:
            res = fit_mundlak_nbr(agg)
            f_within_boot[b] = res["f_within"]
        except Exception:
            pass
        if (b + 1) % 100 == 0:
            print(f"    .. {b + 1}/{n_reps}; "
                  f"current 95 % CI on f_within = "
                  f"[{np.nanpercentile(f_within_boot[:b+1], 2.5):.3f}, "
                  f"{np.nanpercentile(f_within_boot[:b+1], 97.5):.3f}]")
    n_failed = int(np.isnan(f_within_boot).sum())
    print(f"  bootstrap complete; {n_failed} non-converged replicates")
    return f_within_boot


def annotate_flag3(shift_pp: float) -> str:
    a = abs(shift_pp)
    if a < 2.0:
        return f"FLAG-3 NO-CHANGE (shift = {shift_pp:+.2f} pp; < 2 pp)"
    if a > 5.0:
        return f"FLAG-3 MATERIAL (shift = {shift_pp:+.2f} pp; > 5 pp)"
    return f"FLAG-3 MODEST (shift = {shift_pp:+.2f} pp; in [2, 5] pp)"


def main():
    if not INPUT_PATH.exists():
        sys.exit(f"FATAL: input parquet not found at {INPUT_PATH}; run 01 first.")

    df = pd.read_parquet(INPUT_PATH)
    print(f"Loaded {len(df):,} rows.")

    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    has_prov = df["province"].notna()
    rows_for_boot = df.loc[~rome & has_hanson & has_prov].copy()
    print(f"  Rome-excluded + Hanson-matched + province-known rows: {len(rows_for_boot):,}")

    results = []
    boot_arrays = {}
    for v in VARIANTS:
        print(f"\n=== variant: {v['key']} ({v['label']}) ===")
        cities = aggregate_with_mundlak(df, v["letter_col"])
        if cities is None:
            sys.exit("FATAL: aggregation returned no rows.")
        point = fit_mundlak_nbr(cities)
        print(f"  n_cities = {point['n']:,}  alpha = {point['alpha']:.3f}")
        print(f"  beta_within  = {point['beta_within']:+.4f}  "
              f"(sd log_pop_within  = {point['sd_log_pop_within']:.4f})")
        print(f"  beta_between = {point['beta_between']:+.4f}  "
              f"(sd log_pop_prov   = {point['sd_log_pop_between']:.4f})")
        print(f"  f_within (point) = {100.0 * point['f_within']:.2f} %")
        boot = bootstrap_partition(rows_for_boot, v["letter_col"])
        point["key"] = v["key"]
        point["label"] = v["label"]
        point["ci_lo"] = float(np.nanpercentile(boot, 2.5))
        point["ci_hi"] = float(np.nanpercentile(boot, 97.5))
        results.append(point)
        boot_arrays[v["key"]] = boot

    summary = pd.DataFrame([
        {
            "variant": r["key"],
            "label": r["label"],
            "n_cities": r["n"],
            "beta_within": r["beta_within"],
            "beta_between": r["beta_between"],
            "var_within": r["var_within"],
            "var_between": r["var_between"],
            "f_within_pct": 100.0 * r["f_within"],
            "f_within_ci_lo_pct": 100.0 * r["ci_lo"],
            "f_within_ci_hi_pct": 100.0 * r["ci_hi"],
        }
        for r in results
    ])
    summary.to_csv(TBL_DIR / "variance-partition.csv", index=False,
                   float_format="%.4f")

    print("\nVariance-partition summary:")
    print(summary.to_string(index=False))

    inscription_f = 100.0 * results[0]["f_within"]
    print("\nFLAG 3 (within-province variance-partition shift from inscription baseline):")
    for r in results[1:]:
        shift = 100.0 * r["f_within"] - inscription_f
        print(f"  {r['label']:34s}: " + annotate_flag3(shift))

    # ----------------------------------- figure
    fig, ax = plt.subplots(figsize=(10, 5))
    colours = ["#264653", "#e76f51", "#2a9d8f"]
    xs = np.arange(len(results))
    f_within_vals = [100.0 * r["f_within"] for r in results]
    ci_lo_vals = [100.0 * r["ci_lo"] for r in results]
    ci_hi_vals = [100.0 * r["ci_hi"] for r in results]
    err_lo = np.array(f_within_vals) - np.array(ci_lo_vals)
    err_hi = np.array(ci_hi_vals) - np.array(f_within_vals)
    ax.bar(xs, f_within_vals, yerr=[err_lo, err_hi], color=colours, alpha=0.75,
           capsize=6, edgecolor="black", linewidth=0.6)
    for i, (val, lo, hi) in enumerate(zip(f_within_vals, ci_lo_vals, ci_hi_vals)):
        ax.text(i, val + 1.5, f"{val:.1f} %\n[{lo:.1f}, {hi:.1f}]",
                ha="center", fontsize=9)
    ax.set_xticks(xs)
    ax.set_xticklabels([r["label"] for r in results], fontsize=10)
    ax.set_ylabel("f_within  (within-province share of log E[y] variance, %)")
    ax.set_title(
        "Within-province variance partition under three response variants\n"
        "(frequentist Mundlak NBR; 500-rep row-resample bootstrap)",
        fontsize=11,
    )
    ax.set_ylim(0, max(70, max(ci_hi_vals) + 10))
    ax.axhline(inscription_f, color="grey", linestyle=":", alpha=0.5,
               label=f"inscription baseline ({inscription_f:.1f} %)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "fig-05-variance-partition-bars.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"\n  figure -> {out.relative_to(PROJECT_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
