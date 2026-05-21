#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-empire-province-city-spas.py --- Block 2 of the RAC-TRAC 2026 talk-prep run.

Purpose
-------
Produce the empire / province / city SPA figures for slide #4 of the
conference talk. All three use the prereg-canonical 5-year-bin uniform
aoristic deposit (per-year uniform mass; partial-overlap inscriptions
contribute their overlap fraction; unit-mass normalisation).

Three figures:

  (1) fig-04a-empire-spa.png       --- empire-wide SPA on 180,609 rows.
  (2) fig-04b-province-spa.png     --- top-N provinces (Rome-excluded);
                                       each scaled to unit height,
                                       overlaid for shape comparison.
  (3) fig-04c-city-spa.png         --- top-8 Hanson-cities by inscription
                                       count (Rome-excluded); small
                                       multiples, each scaled to unit
                                       height.

City-grain note (per Block 1 finding)
-------------------------------------
Per Shawn's 2026-05-21 decision, we follow the prereg TEXT spec ("all cities
with Hanson population estimates, Rome excluded" --- 1,044 cities) rather
than the 2024-notebook's narrower Latin-province subset (~815). The "Latin
provinces" framing in the roadmap becomes simply "top-N provinces by
Rome-excluded inscription count" --- inheritance of the underlying
methodological posture, just without the manually-curated language dictionary.

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet  (from Block 1)

Outputs
-------
runs/2026-05-21-talk-prep/outputs/figures/fig-04a-empire-spa.png
runs/2026-05-21-talk-prep/outputs/figures/fig-04b-province-spa.png
runs/2026-05-21-talk-prep/outputs/figures/fig-04c-city-spa.png
runs/2026-05-21-talk-prep/outputs/tables/province-spa-rank.csv
runs/2026-05-21-talk-prep/outputs/tables/city-spa-rank.csv

Mirrored to planning/conference-talk-rac-trac-2026/figures/ at the end so the
Quarto deck can reference figures by a stable path.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-21, on Shawn's brief.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

# Prereg analysis envelope and binning (per preregistration-draft.md §4).
ENVELOPE_MIN = -50
ENVELOPE_MAX = 350
BIN_WIDTH = 5

BIN_EDGES = np.arange(ENVELOPE_MIN, ENVELOPE_MAX + 1, BIN_WIDTH, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

# Talk figure aspect: 16:9 at sensible DPI for revealjs embedding.
FIG_SIZE_WIDE = (12.0, 6.75)     # 16:9 at 12"
FIG_SIZE_GRID = (12.0, 7.5)      # slight extra height for small-multiples
DPI = 200

# How many provinces / cities to show on the comparison figures.
N_PROVINCES = 8                  # top 8 by Rome-excluded inscription count
N_CITIES = 8                     # top 8 Hanson-cities ex-Rome (roadmap: 6-10)

# Random seed --- recorded for ritual, though uniform-aoristic deposit is
# deterministic (no resampling).
RANDOM_SEED = 20_260_521


# ---------------------------------------------------------------------------
# Canonical uniform-aoristic SPA. Ported verbatim from
# runs/2026-05-17-date-range-filtered-spas/code/date_range_filtered_spas.py
# (lines 199-234), which is the project's tested implementation.
# ---------------------------------------------------------------------------
def uniform_aoristic_spa(
    not_before: np.ndarray,
    not_after: np.ndarray,
    width: np.ndarray,
    bin_edges: np.ndarray = BIN_EDGES,
) -> np.ndarray:
    """Build a summed-probability array (SPA) under uniform aoristic mass.

    Each inscription contributes ``overlap(bin, [not_before, not_after + 1)) /
    width`` to every bin it touches. An inscription whose entire interval lies
    inside the envelope deposits exactly 1.0 unit of mass; partial-overlap
    inscriptions contribute their overlap fraction.

    Parameters
    ----------
    not_before, not_after : np.ndarray
        Integer interval endpoints (inclusive).
    width : np.ndarray
        Integer array. width = not_after - not_before + 1 (inclusive-Roman).
    bin_edges : np.ndarray, default BIN_EDGES
        Float array of length N_BINS + 1; half-open bins.

    Returns
    -------
    np.ndarray
        SPA vector (float), length len(bin_edges) - 1.
    """
    interval_lo = not_before.astype(float)
    interval_hi = not_after.astype(float) + 1.0
    density = 1.0 / width.astype(float)

    spa = np.zeros(len(bin_edges) - 1, dtype=float)
    for i in range(len(bin_edges) - 1):
        b_lo = bin_edges[i]
        b_hi = bin_edges[i + 1]
        overlap = np.maximum(
            0.0, np.minimum(interval_hi, b_hi) - np.maximum(interval_lo, b_lo)
        )
        spa[i] = (overlap * density).sum()
    return spa


def spa_of(df: pd.DataFrame) -> np.ndarray:
    """Convenience wrapper: compute SPA for a sub-DataFrame."""
    return uniform_aoristic_spa(
        df["not_before"].to_numpy(),
        df["not_after"].to_numpy(),
        df["width"].to_numpy(),
    )


# ---------------------------------------------------------------------------
# Rome-identification --- mirrors Block 1.
# ---------------------------------------------------------------------------
def rome_mask(df: pd.DataFrame) -> pd.Series:
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


# ---------------------------------------------------------------------------
# Figure-builder helpers --- each writes one PNG and returns the figure
# so callers can also save high-DPI copies into the talk figures dir.
# ---------------------------------------------------------------------------
def style_axes(ax: plt.Axes, ylabel: str = "summed probability mass / 5 y") -> None:
    """Common axis decoration for SPA figures.

    Adds centred year axis from 50 BC to AD 350, with reign-era guides at
    the BC/AD step and at canonical century boundaries.
    """
    ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
    ax.set_xlabel("year")
    ax.set_ylabel(ylabel)
    ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.8)
    for x in (100, 200, 300):
        ax.axvline(x, color="grey", linestyle=":", alpha=0.25, linewidth=0.6)


def bootstrap_spa(df: pd.DataFrame, n_reps: int = 1000) -> np.ndarray:
    """1,000-replicate row-resample bootstrap of the uniform-aoristic SPA.

    Returns
    -------
    (n_reps, N_BINS) array of SPA replicates.
    """
    print(f"[block-2] bootstrapping empire SPA: {n_reps} replicates "
          f"on {len(df):,} rows")
    rng = np.random.default_rng(RANDOM_SEED)
    nb = df["not_before"].to_numpy()
    na = df["not_after"].to_numpy()
    w = df["width"].to_numpy()
    n_rows = len(df)
    reps = np.zeros((n_reps, len(BIN_CENTRES)), dtype=float)
    for b in range(n_reps):
        idx = rng.integers(0, n_rows, size=n_rows)
        reps[b] = uniform_aoristic_spa(nb[idx], na[idx], w[idx])
        if (b + 1) % 100 == 0:
            print(f"    .. {b + 1}/{n_reps}")
    return reps


def render_empire(df: pd.DataFrame, n_bootstrap: int = 1000) -> Path:
    """Render the empire-wide SPA + 95% row-resample bootstrap CI band."""
    print(f"[block-2] empire SPA on {len(df):,} rows")
    spa = spa_of(df)
    boot = bootstrap_spa(df, n_reps=n_bootstrap)
    ci_lo = np.percentile(boot, 2.5, axis=0)
    ci_hi = np.percentile(boot, 97.5, axis=0)

    fig, ax = plt.subplots(figsize=FIG_SIZE_WIDE)
    ax.fill_between(BIN_CENTRES, ci_lo, ci_hi, alpha=0.25, color="C0",
                    label="95 % row-resample bootstrap CI (1,000 reps)")
    ax.plot(BIN_CENTRES, spa, color="C0", linewidth=1.6,
            label="empire SPA (point estimate)")
    style_axes(ax)
    ax.set_title(
        f"Raw uncorrected empire SPA, LIRE v3.0 ({len(df):,} inscriptions; "
        f"5-year bins; uniform aoristic mass)",
        fontsize=12,
    )
    ax.legend(loc="upper right", fontsize=9)
    out = FIG_DIR / "fig-04a-empire-spa.png"
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-2]   -> {out}")
    # Persist the bootstrap replicates table.
    pd.DataFrame(
        np.column_stack([BIN_CENTRES, spa, ci_lo, ci_hi]),
        columns=["bin_centre", "spa_point", "ci_lo_2p5", "ci_hi_97p5"],
    ).to_csv(TBL_DIR / "empire-spa-bootstrap.csv", index=False)
    return out


def render_province(df: pd.DataFrame) -> Path:
    """Render top-N province SPAs (Rome-excluded) as 2x4 small-multiples,
    unit-peak-normalised, shared Y axis."""
    rome = rome_mask(df)
    ex_rome = df.loc[~rome].copy()
    counts = ex_rome.groupby("province").size().sort_values(ascending=False)
    top_provinces = counts.head(N_PROVINCES).index.tolist()
    counts.to_csv(TBL_DIR / "province-spa-rank.csv",
                  header=["inscription_count_ex_rome"])
    print(f"[block-2] province SPA: top {N_PROVINCES} provinces "
          f"(out of {len(counts)}) by Rome-excluded inscription count")
    for p in top_provinces:
        print(f"    {p:30} N = {int(counts[p]):>6,}")

    n_cols = 4
    n_rows = (N_PROVINCES + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=FIG_SIZE_GRID, sharex=True, sharey=True,
    )
    axes = np.asarray(axes).reshape(-1)
    cmap = plt.get_cmap("viridis")
    for i, prov in enumerate(top_provinces):
        ax = axes[i]
        sub = ex_rome.loc[ex_rome["province"] == prov]
        spa = spa_of(sub)
        if spa.max() > 0:
            spa = spa / spa.max()
        colour = cmap(i / max(1, N_PROVINCES - 1))
        ax.fill_between(BIN_CENTRES, spa, alpha=0.25, color=colour)
        ax.plot(BIN_CENTRES, spa, color=colour, linewidth=1.2)
        ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
        ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.7)
        for x in (100, 200, 300):
            ax.axvline(x, color="grey", linestyle=":", alpha=0.2, linewidth=0.5)
        ax.set_title(f"{prov}  (N = {int(counts[prov]):,})", fontsize=10)
        ax.set_ylim(0, 1.05)
    for j in range(len(top_provinces), len(axes)):
        axes[j].set_visible(False)
    for ax in axes[-n_cols:]:
        ax.set_xlabel("year")
    for ax in axes[::n_cols]:
        ax.set_ylabel("SPA (norm.)")
    fig.suptitle(
        f"Raw uncorrected per-province SPAs: top {N_PROVINCES} by "
        f"inscription count, Rome excluded; unit-peak-normalised",
        fontsize=12, y=0.995,
    )
    out = FIG_DIR / "fig-04b-province-spa.png"
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-2]   -> {out}")
    return out


def render_city(df: pd.DataFrame) -> Path:
    """Render top-N Hanson-city SPAs (Rome-excluded), as small multiples."""
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    sample = df.loc[~rome & has_hanson].copy()
    counts = sample.groupby("urban_context_city").size().sort_values(ascending=False)
    top_cities = counts.head(N_CITIES).index.tolist()
    counts.head(50).to_csv(TBL_DIR / "city-spa-rank.csv",
                           header=["inscription_count_filtered"])
    print(f"[block-2] city SPA: top {N_CITIES} Hanson-cities ex-Rome "
          f"(out of {len(counts)}) by inscription count")
    for c in top_cities:
        print(f"    {c:30} N = {int(counts[c]):>6,}")

    n_cols = 4
    n_rows = (N_CITIES + n_cols - 1) // n_cols
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=FIG_SIZE_GRID, sharex=True, sharey=True,
    )
    axes = np.asarray(axes).reshape(-1)
    cmap = plt.get_cmap("viridis")
    for i, city in enumerate(top_cities):
        ax = axes[i]
        sub = sample.loc[sample["urban_context_city"] == city]
        spa = spa_of(sub)
        if spa.max() > 0:
            spa = spa / spa.max()
        colour = cmap(i / max(1, N_CITIES - 1))
        ax.fill_between(BIN_CENTRES, spa, alpha=0.25, color=colour)
        ax.plot(BIN_CENTRES, spa, color=colour, linewidth=1.2)
        ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
        ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.7)
        for x in (100, 200, 300):
            ax.axvline(x, color="grey", linestyle=":", alpha=0.2, linewidth=0.5)
        ax.set_title(f"{city}  (N = {int(counts[city]):,})", fontsize=10)
        ax.set_ylim(0, 1.05)
    for j in range(len(top_cities), len(axes)):
        axes[j].set_visible(False)
    # Shared axis labels.
    for ax in axes[-n_cols:]:
        ax.set_xlabel("year")
    for ax in axes[::n_cols]:
        ax.set_ylabel("SPA (norm.)")
    fig.suptitle(
        f"Raw uncorrected per-city SPAs: top {N_CITIES} Hanson-matched "
        f"cities ex-Rome by inscription count; unit-peak-normalised",
        fontsize=12, y=0.995,
    )
    out = FIG_DIR / "fig-04c-city-spa.png"
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-2]   -> {out}")
    return out


def mirror_to_talk_dir(paths: list[Path]) -> None:
    """Copy figures to the talk figures dir for Quarto stable-pathing."""
    for p in paths:
        dest = TALK_FIG_DIR / p.name
        shutil.copy2(p, dest)
        print(f"[block-2]   mirrored -> {dest}")


def main() -> int:
    if not DATA_PATH.exists():
        print(
            f"[block-2] HALT: filtered parquet missing at {DATA_PATH}. "
            "Run 01-filter-and-prep.py first."
        )
        return 1
    df = pd.read_parquet(DATA_PATH)
    print(f"[block-2] loaded {len(df):,} rows from {DATA_PATH.name}")
    np.random.seed(RANDOM_SEED)

    paths = [
        render_empire(df),
        render_province(df),
        render_city(df),
    ]
    mirror_to_talk_dir(paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
