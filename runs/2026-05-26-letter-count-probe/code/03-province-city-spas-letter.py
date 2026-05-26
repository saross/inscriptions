#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03-province-city-spas-letter.py --- Block 3 of the 2026-05-26 letter-count probe.

Purpose
-------
Per-province and per-city SPAs under the three weightings (inscription-mass,
letter-mass conservative, letter-mass interpretive). Two outputs feed back
into the verdict:

1. Small-multiples figures (top-N by inscription count, Rome-excluded) ---
   each panel shows three SPA traces overlaid; if the temporal shape
   diverges noticeably under letter-mass for any province/city, surfaces it
   visually.

2. Rank-change tables --- if the top-N by inscription-count selection
   reorders when we re-rank by letter-mass total, that reorder is itself
   the headline finding (signals that a few-but-long inscriptions can
   eclipse many-but-short).

Selection convention (per spec Decision 3): present BOTH same-rank-as-2026-05-21
AND letter-rank, with explicit rank-change tables. Top 8 provinces (Rome-
excluded by province field) and top 8 Hanson-cities ex-Rome.

Inputs
------
runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet

Outputs
-------
outputs/figures/fig-03a-province-spa-grid.png  --- 8-panel small multiples;
    each panel has three overlaid traces.
outputs/figures/fig-03b-city-spa-grid.png  --- ditto for top 8 cities.
outputs/tables/province-rank-change.csv  --- columns: province,
    inscription_count, letter_total_conservative, letter_total_interpretive,
    rank_by_inscription, rank_by_letter_cons, rank_by_letter_intr,
    delta_rank_cons, delta_rank_intr.
outputs/tables/city-rank-change.csv  --- ditto for cities.

Reproducibility
---------------
RANDOM_SEED = 20260526 (deterministic; recorded for ritual).

Date
----
2026-05-26
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
INPUT_PATH = RUN_DIR / "data" / "lire-filtered-with-letters.parquet"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"

for d in (FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)

ENVELOPE_MIN = -50
ENVELOPE_MAX = 350
BIN_WIDTH = 5
BIN_EDGES = np.arange(ENVELOPE_MIN, ENVELOPE_MAX + 1, BIN_WIDTH, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

N_TOP = 8
FIG_SIZE_GRID = (14.0, 8.0)
DPI = 200
RANDOM_SEED = 20260526


def weighted_aoristic_spa(nb, na, w, wt, bin_edges=BIN_EDGES):
    """See 02-empire-spa-letter.py for full docstring."""
    interval_lo = nb.astype(float)
    interval_hi = na.astype(float) + 1.0
    density = wt.astype(float) / w.astype(float)
    spa = np.zeros(len(bin_edges) - 1, dtype=float)
    for i in range(len(bin_edges) - 1):
        b_lo = bin_edges[i]
        b_hi = bin_edges[i + 1]
        overlap = np.maximum(
            0.0, np.minimum(interval_hi, b_hi) - np.maximum(interval_lo, b_lo)
        )
        spa[i] = (overlap * density).sum()
    return spa


def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def _spa_three_ways(sub_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute the three SPAs for a sub-DataFrame."""
    nb = sub_df["not_before"].to_numpy()
    na = sub_df["not_after"].to_numpy()
    w = (na - nb + 1).astype(int)
    n = len(sub_df)
    spa_i = weighted_aoristic_spa(nb, na, w, np.ones(n))
    spa_c = weighted_aoristic_spa(nb, na, w, sub_df["letter_count_conservative"].to_numpy())
    spa_p = weighted_aoristic_spa(nb, na, w, sub_df["letter_count_interpretive"].to_numpy())
    return spa_i, spa_c, spa_p


def _norm(x: np.ndarray) -> np.ndarray:
    """Peak-normalise for shape comparison, guarding against all-zero SPAs."""
    m = x.max()
    return x / m if m > 0 else x


def render_grid(
    sub_label: str,
    group_col: str,
    df: pd.DataFrame,
    top_labels: list[str],
    counts_lookup: pd.DataFrame,
    out_fig: Path,
) -> None:
    """Render the 4x2 small-multiples grid; one panel per label."""
    n_cols = 4
    n_rows = (N_TOP + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=FIG_SIZE_GRID,
                             sharex=True, sharey=True)
    axes = np.asarray(axes).reshape(-1)

    for i, name in enumerate(top_labels):
        ax = axes[i]
        sub = df.loc[df[group_col] == name]
        spa_i, spa_c, spa_p = _spa_three_ways(sub)

        ax.plot(BIN_CENTRES, _norm(spa_i), color="#264653", linewidth=1.4,
                label="inscr-mass" if i == 0 else None)
        ax.plot(BIN_CENTRES, _norm(spa_c), color="#e76f51", linewidth=1.0,
                label="letter-cons" if i == 0 else None)
        ax.plot(BIN_CENTRES, _norm(spa_p), color="#2a9d8f", linewidth=1.0,
                linestyle="--", label="letter-intr" if i == 0 else None)
        ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
        ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.7)
        for x in (100, 200, 300):
            ax.axvline(x, color="grey", linestyle=":", alpha=0.2, linewidth=0.5)

        n_inscr = int(counts_lookup.loc[name, "inscription_count"])
        n_letters_c = int(counts_lookup.loc[name, "letter_total_conservative"])
        ax.set_title(
            f"{name}\nN = {n_inscr:,} inscr · {n_letters_c:,} letters",
            fontsize=9,
        )
        ax.set_ylim(0, 1.05)

    for j in range(len(top_labels), len(axes)):
        axes[j].set_visible(False)
    for ax in axes[-n_cols:]:
        ax.set_xlabel("year")
    for ax in axes[::n_cols]:
        ax.set_ylabel("SPA (norm.)")
    # Single legend at the top.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, 0.99))
    fig.suptitle(
        f"{sub_label} SPA comparison (top {N_TOP} by inscription count, "
        f"Rome-excluded): three weightings, peak-normalised per panel",
        fontsize=11, y=0.94,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(out_fig, dpi=DPI)
    plt.close(fig)
    print(f"  -> {out_fig.relative_to(PROJECT_ROOT)}")


def build_rank_table(
    df: pd.DataFrame,
    group_col: str,
    out_csv: Path,
) -> pd.DataFrame:
    """Aggregate per-group totals + rank by each weighting; emit CSV."""
    agg = df.groupby(group_col).agg(
        inscription_count=(group_col, "size"),
        letter_total_conservative=("letter_count_conservative", "sum"),
        letter_total_interpretive=("letter_count_interpretive", "sum"),
    )
    agg["rank_by_inscription"] = agg["inscription_count"].rank(ascending=False, method="min").astype(int)
    agg["rank_by_letter_cons"] = agg["letter_total_conservative"].rank(ascending=False, method="min").astype(int)
    agg["rank_by_letter_intr"] = agg["letter_total_interpretive"].rank(ascending=False, method="min").astype(int)
    agg["delta_rank_cons"] = agg["rank_by_letter_cons"] - agg["rank_by_inscription"]
    agg["delta_rank_intr"] = agg["rank_by_letter_intr"] - agg["rank_by_inscription"]
    agg = agg.sort_values("rank_by_inscription")
    agg.to_csv(out_csv)
    return agg


def main():
    if not INPUT_PATH.exists():
        sys.exit(f"FATAL: input parquet not found at {INPUT_PATH}; run 01 first.")

    df = pd.read_parquet(INPUT_PATH)
    n_rows = len(df)
    print(f"Loaded {n_rows:,} rows.")

    rome = rome_mask(df)
    ex_rome = df.loc[~rome].copy()
    has_hanson = ex_rome["urban_context_pop_est"].notna()
    cities_sample = ex_rome.loc[has_hanson].copy()
    print(f"  Rome-excluded:                       {len(ex_rome):,}")
    print(f"  Rome-excluded + Hanson-city-matched: {len(cities_sample):,}")

    # ----------------------------------- province
    prov_tbl = build_rank_table(
        ex_rome, "province",
        TBL_DIR / "province-rank-change.csv",
    )
    top_provinces = prov_tbl.head(N_TOP).index.tolist()
    print("\nTop provinces by inscription count:")
    print(prov_tbl.head(N_TOP)[
        ["inscription_count", "letter_total_conservative",
         "letter_total_interpretive", "rank_by_letter_cons",
         "rank_by_letter_intr", "delta_rank_cons", "delta_rank_intr"]
    ].to_string())

    render_grid(
        "Province",
        "province",
        ex_rome,
        top_provinces,
        prov_tbl,
        FIG_DIR / "fig-03a-province-spa-grid.png",
    )

    # ----------------------------------- city
    city_tbl = build_rank_table(
        cities_sample, "urban_context_city",
        TBL_DIR / "city-rank-change.csv",
    )
    top_cities = city_tbl.head(N_TOP).index.tolist()
    print("\nTop cities by inscription count:")
    print(city_tbl.head(N_TOP)[
        ["inscription_count", "letter_total_conservative",
         "letter_total_interpretive", "rank_by_letter_cons",
         "rank_by_letter_intr", "delta_rank_cons", "delta_rank_intr"]
    ].to_string())

    render_grid(
        "City",
        "urban_context_city",
        cities_sample,
        top_cities,
        city_tbl,
        FIG_DIR / "fig-03b-city-spa-grid.png",
    )

    print("\nDone.")


if __name__ == "__main__":
    main()
