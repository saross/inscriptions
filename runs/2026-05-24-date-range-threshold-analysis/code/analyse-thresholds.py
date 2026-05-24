#!/usr/bin/env python3
"""
analyse-thresholds.py
=====================

Date-range threshold analysis for LIRE v3.0. Generates:

1. Fine-grained histogram of date_range (1-year bins, 0-300y) with reference
   lines at 1, 5, 10, 25, 50, 100, 200 years.
2. Sub-50y zoom histogram (1-year bins, 0-50y).
3. Log-scale full histogram (1-year bins, 0-2060y).
4. Threshold count tables (between- and cumulative-thresholds), saved CSV.
5. Inscription-type breakdown at cutoffs < 1, < 5, < 10, < 25, < 50, < 100, all.
   Both absolute counts and within-cutoff percentages.
6. Stacked-bar figure: % composition by inscription type at each cutoff.
7. Median date-range by type.
8. ΔT (Williams 2012 σ) by cutoff: mean date-range standard deviation under
   uniform-within-interval assumption.

Inputs: archive/data-2026-04-22/LIRE_v3-0.parquet (182 853 records)
Outputs: outputs/figures/*.png at 150 dpi; outputs/tables/*.csv

Companion documents:
- planning/h2.1-mixture-model-problem-explained-2026-05-24.md
- planning/h2.1-follow-up-candidates-2026-05-24.md

Author / date: Claude Opus 4.7 (1M context), 2026-05-24.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# Paths
DATA_PATH = Path("/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet")
RUN_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = RUN_ROOT / "outputs" / "figures"
TBL_DIR = RUN_ROOT / "outputs" / "tables"


# Reference thresholds (editorial-slab anchors)
SLAB_LINES = [1, 5, 10, 25, 50, 100, 200, 300]

# Cutoff thresholds for cumulative-under-threshold counts
CUTOFFS = [1, 5, 10, 25, 50, 100, 200, 300]

# Between-threshold bins
BETWEEN_BINS = [0, 1, 5, 10, 25, 50, 100, 200, 300]


def load_lire() -> pd.DataFrame:
    """Load LIRE v3.0; compute date_range; check sanity."""
    lire = pd.read_parquet(DATA_PATH)
    # No nulls in not_before/not_after per v3.0 (verified separately).
    lire["date_range"] = lire["not_after"] - lire["not_before"]
    # No negative ranges in v3.0 (cleaned).
    assert (lire["date_range"] >= 0).all(), "Unexpected negative date_range"
    return lire


def make_simplified_type(t: pd.Series) -> pd.Series:
    """Group the ~22 raw type_of_inscription_auto categories into 8 broader
    families for visualisation. Returns a Categorical with stable ordering."""
    mapping = {
        "epitaph": "epitaph (funerary)",
        "votive inscription": "votive",
        "identification inscription": "identification",
        "owner/artist inscription": "identification",
        "honorific inscription": "honorific",
        "building/dedicatory inscription": "building/dedicatory",
        "mile-/leaguestone": "mile-/leaguestone",
        "military diploma": "military diploma",
        "boundary inscription": "boundary",
        "acclamation": "acclamation",
        "defixio": "other small",
        "list": "other small",
        "label": "other small",
        "public legal inscription": "other small",
        "private legal inscription": "other small",
        "elogium": "other small",
        "letter": "other small",
        "seat inscription": "other small",
        "prayer": "other small",
        "assignation inscription": "other small",
        "calendar": "other small",
        "adnuntiatio": "other small",
    }
    cat = t.map(mapping).fillna("unknown")
    order = [
        "epitaph (funerary)", "votive", "identification", "honorific",
        "building/dedicatory", "mile-/leaguestone", "military diploma",
        "boundary", "acclamation", "other small", "unknown",
    ]
    return pd.Categorical(cat, categories=order, ordered=True)


def fine_histogram(lire: pd.DataFrame) -> None:
    """Histogram with 1-year bins; full range; reference lines."""
    fig, ax = plt.subplots(figsize=(12, 6))
    bins = np.arange(0, 301, 1)
    counts, edges = np.histogram(lire["date_range"].clip(upper=300), bins=bins)
    ax.bar(edges[:-1], counts, width=1.0, color="#4C72B0", edgecolor="none")
    for x in SLAB_LINES:
        ax.axvline(x, color="red", linestyle="--", alpha=0.5, linewidth=0.8)
        ax.text(
            x, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 0 else 1,
            f" {x}y",
            color="red", fontsize=8, va="top",
        )
    ax.set_xlabel("Date-range (years; not_after − not_before)")
    ax.set_ylabel("Count of inscriptions")
    ax.set_title(
        "LIRE v3.0 — fine-grained date-range histogram (1-year bins)\n"
        f"n = {len(lire):,} records; red dashes mark editorial-slab anchors"
    )
    ax.set_xlim(0, 300)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "histogram-fine-1y-bins-0-300y.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")


def fine_histogram_log(lire: pd.DataFrame) -> None:
    """Same fine histogram but log y-scale so smaller slabs are visible."""
    fig, ax = plt.subplots(figsize=(12, 6))
    bins = np.arange(0, 301, 1)
    counts, edges = np.histogram(lire["date_range"].clip(upper=300), bins=bins)
    counts = np.where(counts == 0, 0.1, counts)  # avoid log(0)
    ax.bar(edges[:-1], counts, width=1.0, color="#4C72B0", edgecolor="none")
    for x in SLAB_LINES:
        ax.axvline(x, color="red", linestyle="--", alpha=0.5, linewidth=0.8)
    ax.set_xlabel("Date-range (years)")
    ax.set_ylabel("Count of inscriptions (log scale)")
    ax.set_yscale("log")
    ax.set_title(
        "LIRE v3.0 — date-range histogram (1-year bins; log y-scale)\n"
        f"n = {len(lire):,} records; red dashes mark editorial-slab anchors"
    )
    ax.set_xlim(0, 300)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    out = FIG_DIR / "histogram-fine-1y-bins-log-y.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")


def sub_50y_zoom(lire: pd.DataFrame) -> None:
    """Zoom histogram of date_range in [0, 50] with 1-year bins."""
    sub = lire[lire["date_range"] <= 50]
    fig, ax = plt.subplots(figsize=(12, 6))
    bins = np.arange(0, 52, 1)
    counts, edges = np.histogram(sub["date_range"], bins=bins)
    ax.bar(edges[:-1], counts, width=1.0, color="#55A868", edgecolor="none")
    for x in [1, 5, 10, 25, 50]:
        ax.axvline(x, color="red", linestyle="--", alpha=0.6, linewidth=1.0)
        ax.text(
            x, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 0 else 1,
            f" {x}y",
            color="red", fontsize=10, va="top",
        )
    ax.set_xlabel("Date-range (years)")
    ax.set_ylabel("Count of inscriptions")
    ax.set_title(
        "LIRE v3.0 — date-range histogram, sub-50y zoom (1-year bins)\n"
        f"n = {len(sub):,} records with date_range ≤ 50y "
        f"({len(sub)/len(lire)*100:.1f}% of corpus)"
    )
    ax.set_xlim(0, 50)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "histogram-sub-50y-zoom.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")


def threshold_counts(lire: pd.DataFrame) -> None:
    """Threshold count tables: between bins + cumulative under thresholds."""
    n = len(lire)
    # Between-bin counts
    between_rows = []
    for i in range(len(BETWEEN_BINS) - 1):
        lo, hi = BETWEEN_BINS[i], BETWEEN_BINS[i + 1]
        cnt = ((lire["date_range"] >= lo) & (lire["date_range"] < hi)).sum()
        between_rows.append(
            dict(
                bin_lo=lo, bin_hi=hi,
                bin_label=f"[{lo}, {hi})",
                count=int(cnt), pct_of_corpus=round(100 * cnt / n, 2),
            )
        )
    # Tail
    tail_cnt = (lire["date_range"] >= BETWEEN_BINS[-1]).sum()
    between_rows.append(
        dict(
            bin_lo=BETWEEN_BINS[-1], bin_hi=None,
            bin_label=f">= {BETWEEN_BINS[-1]}",
            count=int(tail_cnt), pct_of_corpus=round(100 * tail_cnt / n, 2),
        )
    )
    between_df = pd.DataFrame(between_rows)
    out_a = TBL_DIR / "counts-between-thresholds.csv"
    between_df.to_csv(out_a, index=False)
    print(f"  wrote {out_a}")
    print("\nBetween-threshold counts:")
    print(between_df.to_string(index=False))

    # Cumulative under thresholds
    cum_rows = []
    for thr in CUTOFFS:
        cnt = (lire["date_range"] < thr).sum()
        cum_rows.append(
            dict(
                cutoff=thr,
                count_under=int(cnt),
                pct_under=round(100 * cnt / n, 2),
                count_excluded=int(n - cnt),
                pct_excluded=round(100 * (n - cnt) / n, 2),
            )
        )
    cum_df = pd.DataFrame(cum_rows)
    out_b = TBL_DIR / "counts-cumulative-under.csv"
    cum_df.to_csv(out_b, index=False)
    print(f"\n  wrote {out_b}")
    print("\nCumulative under-threshold counts:")
    print(cum_df.to_string(index=False))

    # Williams ΔT
    dt_rows = []
    for thr in CUTOFFS + [None]:  # None = no cutoff
        if thr is None:
            sub = lire
            label = "no cutoff"
        else:
            sub = lire[lire["date_range"] <= thr]
            label = f"<= {thr}y"
        sigma = (sub["date_range"] / np.sqrt(12)).mean()
        dt_rows.append(
            dict(
                cutoff_label=label,
                n=len(sub),
                mean_sigma_years=round(sigma, 3),
            )
        )
    dt_df = pd.DataFrame(dt_rows)
    out_c = TBL_DIR / "williams-delta-t-by-cutoff.csv"
    dt_df.to_csv(out_c, index=False)
    print(f"\n  wrote {out_c}")
    print("\nWilliams ΔT (mean σ assuming uniform within interval):")
    print(dt_df.to_string(index=False))


def type_breakdown_by_cutoff(lire: pd.DataFrame) -> None:
    """Inscription-type composition at each cutoff."""
    lire = lire.copy()
    lire["type_simple"] = make_simplified_type(lire["type_of_inscription_auto"])

    # Build a wide table: rows = type, cols = cutoffs (with counts + within-cutoff %)
    type_order = list(lire["type_simple"].cat.categories)
    rows = []
    for thr in [1, 5, 10, 25, 50, 100, None]:
        if thr is None:
            sub = lire
            label = "all"
        else:
            sub = lire[lire["date_range"] < thr]
            label = f"<{thr}"
        type_counts = sub["type_simple"].value_counts().reindex(type_order, fill_value=0)
        row = {"cutoff": label, "N_total": int(len(sub))}
        for t in type_order:
            row[f"count_{t}"] = int(type_counts[t])
            row[f"pct_{t}"] = round(100 * type_counts[t] / max(len(sub), 1), 2)
        rows.append(row)
    type_df = pd.DataFrame(rows)
    out_a = TBL_DIR / "type-composition-by-cutoff.csv"
    type_df.to_csv(out_a, index=False)
    print(f"\n  wrote {out_a}")

    # Compact percent-only table for the report
    pct_cols = ["cutoff", "N_total"] + [f"pct_{t}" for t in type_order]
    pct_df = type_df[pct_cols].copy()
    pct_df.columns = ["cutoff", "N_total"] + type_order
    out_b = TBL_DIR / "type-composition-by-cutoff-pct.csv"
    pct_df.to_csv(out_b, index=False)
    print(f"  wrote {out_b}")
    print("\nType composition (% within each cutoff):")
    print(pct_df.to_string(index=False))

    # Stacked bar figure
    fig, ax = plt.subplots(figsize=(14, 7))
    cutoffs_labels = pct_df["cutoff"].tolist()
    bottom = np.zeros(len(cutoffs_labels))
    # Reasonable distinguishable palette
    colours = plt.cm.tab20(np.linspace(0, 1, len(type_order)))
    for i, t in enumerate(type_order):
        vals = pct_df[t].to_numpy()
        ax.bar(cutoffs_labels, vals, bottom=bottom, label=t, color=colours[i])
        bottom += vals
    ax.set_ylabel("% of inscriptions within cutoff")
    ax.set_xlabel("Cutoff (date_range < N years)")
    ax.set_title(
        "LIRE v3.0 — inscription-type composition by date-range cutoff\n"
        "(stacked %; based on type_of_inscription_auto)"
    )
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=9)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.grid(True, axis="y", alpha=0.3)
    # Add N annotations on each bar
    for i, n in enumerate(pct_df["N_total"]):
        ax.text(i, 101, f"n={n:,}", ha="center", fontsize=8, color="#444")
    fig.tight_layout()
    out_c = FIG_DIR / "type-composition-by-cutoff-stacked.png"
    fig.savefig(out_c, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_c}")

    # Companion: median date-range by type
    median_rows = []
    for t in type_order:
        sub = lire[lire["type_simple"] == t]
        median_rows.append(
            dict(
                type=t,
                count=int(len(sub)),
                median_date_range=int(sub["date_range"].median()) if len(sub) else 0,
                mean_date_range=round(sub["date_range"].mean(), 1) if len(sub) else 0,
                pct_with_range_lt_25=round(
                    100 * (sub["date_range"] < 25).sum() / max(len(sub), 1), 2
                ),
            )
        )
    median_df = pd.DataFrame(median_rows)
    out_d = TBL_DIR / "median-date-range-by-type.csv"
    median_df.to_csv(out_d, index=False)
    print(f"\n  wrote {out_d}")
    print("\nMedian date-range by type:")
    print(median_df.to_string(index=False))


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TBL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading LIRE v3.0...")
    lire = load_lire()
    print(f"  loaded {len(lire):,} records")
    print(f"  date_range: mean={lire['date_range'].mean():.2f}, "
          f"median={lire['date_range'].median():.2f}, "
          f"std={lire['date_range'].std():.2f}")

    print("\n=== Histograms ===")
    fine_histogram(lire)
    fine_histogram_log(lire)
    sub_50y_zoom(lire)

    print("\n=== Threshold counts ===")
    threshold_counts(lire)

    print("\n=== Type breakdown ===")
    type_breakdown_by_cutoff(lire)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
