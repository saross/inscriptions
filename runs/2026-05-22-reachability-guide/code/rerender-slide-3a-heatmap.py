#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rerender-slide-3a-heatmap.py --- Re-render the slide-3a province
heatmap in the same red-yellow-green palette as slide 3b, for visual
consistency across the two main-deck Phase-1 reachability slides.

Background
----------
The original `runs/2026-04-25-h1-simulation/outputs/h1-v2/heatmaps/
province_cpl_gaussian_k3.png` uses the matplotlib viridis-like default
colormap. Slide 3b uses a red→yellow→green colormap that reads
semantically (red = below resolving power; green = reliably
reachable). For undergraduate-history-major audience accessibility,
the two slides should share the same colour grammar.

This script re-renders the same underlying data
(`province_cpl_gaussian_k3.parquet` — 4 brackets × 8 n values) in the
RYG style and saves as `fig-03a-phase1-heatmap-ryg.png`. The original
viridis figure is preserved at its original path (not overwritten).

Inputs
------
runs/2026-04-25-h1-simulation/outputs/h1-v2/heatmaps/province_cpl_gaussian_k3.parquet

Outputs
-------
runs/2026-05-22-reachability-guide/outputs/figures/fig-03a-phase1-heatmap-ryg.png

Then mirrored to:
planning/conference-talk-rac-trac-2026/figures/fig-03-phase1-heatmap.png
(replacing the original viridis figure used by slide 3a in the deck)

Author / Date
-------------
Claude (Opus 4.7), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
SRC_PARQUET = (PROJECT_ROOT / "runs" / "2026-04-25-h1-simulation" /
                "outputs" / "h1-v2" / "heatmaps" /
                "province_cpl_gaussian_k3.parquet")
OUT = RUN_DIR / "outputs" / "figures" / "fig-03a-phase1-heatmap-ryg.png"
TALK_FIG = (PROJECT_ROOT / "planning" / "conference-talk-rac-trac-2026" /
             "figures" / "fig-03-phase1-heatmap.png")

# Match slide 3b's bracket labels exactly for visual grammar.
BRACKET_ORDER = ["c_20pc_25y", "a_50pc_50y", "b_double_25y", "zero"]
BRACKET_LABELS = {
    "c_20pc_25y":   "20 % / 25 y",
    "a_50pc_50y":   "50 % / 50 y\n(binding)",
    "b_double_25y": "100 % / 25 y",
    "zero":         "zero\n(FP control)",
}


def main() -> int:
    df = pd.read_parquet(SRC_PARQUET)
    # df.index = brackets; df.columns = n values (integers)
    n_values = sorted(int(c) for c in df.columns)
    n_cols = len(n_values)
    n_rows = len(BRACKET_ORDER)
    matrix = np.zeros((n_rows, n_cols), dtype=float)
    for i, b in enumerate(BRACKET_ORDER):
        for j, n in enumerate(n_values):
            matrix[i, j] = df.loc[b, n]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    cmap = LinearSegmentedColormap.from_list(
        "ryg", ["#c0392b", "#f1c40f", "#27ae60"], N=256,
    )
    im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0.0, vmax=1.0)

    # Annotate cells
    for i in range(n_rows):
        for j in range(n_cols):
            v = matrix[i, j]
            colour = "white" if v < 0.55 else "black"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=9, color=colour)

    # 80%-detection contour: draw a line between cells where detection
    # crosses the 0.80 boundary, per bracket row.
    # For each row, find the leftmost column where detection >= 0.80
    # and draw a vertical line segment at its left edge.
    for i in range(n_rows):
        for j in range(n_cols):
            if matrix[i, j] >= 0.80:
                ax.plot(
                    [j - 0.5, j - 0.5], [i - 0.5, i + 0.5],
                    color="white", linewidth=2.5,
                )
                ax.plot(
                    [j - 0.5, j - 0.5], [i - 0.5, i + 0.5],
                    color="black", linewidth=1.2,
                )
                break

    ax.set_xticks(range(n_cols))
    ax.set_xticklabels([f"{n:,}" for n in n_values], fontsize=9)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels([BRACKET_LABELS[b] for b in BRACKET_ORDER],
                        fontsize=9)
    ax.set_xlabel("N inscriptions in the analysis unit", fontsize=10)
    ax.set_ylabel("Effect bracket", fontsize=10)
    ax.set_title(
        "Phase 1 reachability — provincial level, cpl-Gaussian null "
        "(detection rate × N × bracket)",
        fontsize=11,
    )

    # Grid between cells
    ax.set_xticks(np.arange(n_cols + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(n_rows + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", length=0)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02, aspect=20)
    cbar.set_label("Detection rate", fontsize=9)
    cbar.ax.axhline(0.80, color="black", linewidth=0.8, linestyle="--")
    cbar.ax.text(
        1.5, 0.80, "0.80 = power\nthreshold",
        transform=cbar.ax.get_yaxis_transform(),
        fontsize=8, va="center",
    )

    # Add a small legend/key explaining the white-edge line
    ax.text(
        0.005, -0.18,
        "White / black line: 80 %-detection contour (left edge = "
        "smallest N at which detection ≥ 0.80 for that bracket)",
        transform=ax.transAxes, fontsize=8, alpha=0.75,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"   -> {OUT}")

    # Mirror to talk figures dir, replacing the viridis original
    shutil.copy2(OUT, TALK_FIG)
    print(f"   mirrored -> {TALK_FIG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
