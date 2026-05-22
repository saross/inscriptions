#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-historian-table.py --- Historian-facing reachability table for the
RAC-TRAC paper supplement and conference deck.

Purpose
-------
Re-present the Phase 1 v2 power-curve outputs in a form a historian or
classicist can read at a glance: "given N inscriptions in your unit /
subset, what kinds of temporal deviations can the preregistered method
credibly detect?"

The Phase 1 v2 simulation already explored an 11-point n-grid
({25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000}) across
three effect brackets, two tapers, and three null-model classes. The
binding-bracket headline number (n >= 1,549 at 80% detection at
province / urban-area level) is the conservative slice; the full grid
covers more substantive history.

This script collapses the grid down two axes:

  - Across shape (gaussian / step taper): report the gaussian-taper
    detection rate as the headline (smoother events are the typical
    historical case; the step taper is the sharp-onset stress test).
    Both are saved.
  - Across null_model + cpl_k (exponential / cpl-k=3 / cpl-k=4):
    report the MIN across the three variants as the headline
    (conservative reading: "the method detects this in the
    worst-case null specification"); the per-null breakdown is also
    saved.

Outputs are oriented for the historian's lookup question:

  "I have N inscriptions in my subset.
   For each preregistered effect bracket,
   what's the detection rate?"

Inputs
------
runs/2026-04-25-h1-simulation/outputs/h1-v2/power-curves.parquet
runs/2026-04-25-h1-simulation/outputs/h1-v2/thresholds.parquet

Outputs
-------
runs/2026-05-22-reachability-guide/outputs/tables/historian-reachability-table.csv
runs/2026-05-22-reachability-guide/outputs/figures/historian-reachability-heatmap.png

Author / Date
-------------
Claude (Opus 4.7), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
SRC = PROJECT_ROOT / "runs" / "2026-04-25-h1-simulation" / "outputs" / "h1-v2"
TBL = RUN_DIR / "outputs" / "tables"
FIG = RUN_DIR / "outputs" / "figures"
TBL.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

# Order brackets by the rough "size of event" — smaller (harder) first.
BRACKET_ORDER = ["c_20pc_25y", "a_50pc_50y", "b_double_25y"]
BRACKET_LABELS = {
    "c_20pc_25y":   "20 %-over-25 y\n(narrow, weak)",
    "a_50pc_50y":   "50 %-over-50 y\n(binding bracket)",
    "b_double_25y": "100 %-over-25 y\n(sharp, strong)",
}
LEVEL_LABELS = {
    "empire":     "Empire-level",
    "province":   "Provincial-level",
    "urban-area": "Urban-area-level",
}
# n-grid is 11 points; we display all in the historian-facing view.
N_GRID = [25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000]


def build_table(pc: pd.DataFrame, taper: str = "gaussian") -> pd.DataFrame:
    """Build the worst-case-null detection rate table.

    For each (level, bracket, n) — restricting to the specified taper —
    take the MINIMUM detection rate across the three null-model variants
    (exponential, cpl-k=3, cpl-k=4). The min is the conservative reading.

    Returns a wide DataFrame indexed by (level, n) with bracket columns.
    """
    sub = pc[pc["shape"] == taper].copy()
    # Worst-case across nulls: min detection rate
    agg = (
        sub.groupby(["level", "bracket", "n"])["detection_rate"]
           .min()
           .reset_index()
    )
    wide = agg.pivot(index=["level", "n"], columns="bracket", values="detection_rate")
    wide = wide.reindex(columns=BRACKET_ORDER)
    return wide.reset_index()


def render_heatmap(wide: pd.DataFrame, taper: str, out_path: Path) -> None:
    """Render a 3-panel heatmap: empire / province / urban-area.

    Rows = n (sample size; log-spaced labels); columns = effect bracket;
    colour = detection rate. Annotated cells. Red-yellow-green colormap
    with detection-rate thresholds (0.7, 0.8) marked.
    """
    fig, axes = plt.subplots(
        1, 3, figsize=(13, 5), sharey=True,
        gridspec_kw={"wspace": 0.10},
    )

    # Red → yellow → green colour scheme
    cmap = LinearSegmentedColormap.from_list(
        "ryg", ["#c0392b", "#f1c40f", "#27ae60"], N=256,
    )

    for ax, level in zip(axes, ["empire", "province", "urban-area"]):
        sub = wide[wide["level"] == level].copy()
        sub = sub.sort_values("n")
        sub = sub[sub["n"].isin(N_GRID)]

        # Matrix: rows = n (ascending), cols = brackets
        matrix = sub[BRACKET_ORDER].to_numpy()
        n_values = sub["n"].tolist()

        im = ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=0.0, vmax=1.0)

        # Annotate cells with detection-rate values
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                v = matrix[i, j]
                if np.isnan(v):
                    txt = "—"
                    colour = "grey"
                else:
                    txt = f"{v:.2f}"
                    colour = "white" if v < 0.55 else "black"
                ax.text(j, i, txt, ha="center", va="center",
                        fontsize=8.5, color=colour)

        ax.set_xticks(range(len(BRACKET_ORDER)))
        ax.set_xticklabels([BRACKET_LABELS[b] for b in BRACKET_ORDER],
                            fontsize=9)
        ax.set_yticks(range(len(n_values)))
        ax.set_yticklabels([f"{n:,}" for n in n_values], fontsize=9)
        ax.set_title(LEVEL_LABELS[level], fontsize=11)

        if ax is axes[0]:
            ax.set_ylabel("N inscriptions in the analysis unit / subset",
                          fontsize=10)

    fig.suptitle(
        "Reachability — detection rate at varying sample size N "
        f"(Gaussian-tapered events; worst-case across null models)"
        if taper == "gaussian" else
        "Reachability — detection rate at varying sample size N "
        f"(step-onset events; worst-case across null models)",
        fontsize=12, y=1.02,
    )

    # Colorbar
    cbar = fig.colorbar(im, ax=axes, shrink=0.7, pad=0.02)
    cbar.set_label("Detection rate (fraction of trials where the "
                    "method correctly flags the planted effect)",
                    fontsize=9)
    cbar.ax.axhline(0.80, color="black", linewidth=0.8, linestyle="--")
    cbar.ax.text(
        1.4, 0.80, "0.80 = standard\npower threshold",
        transform=cbar.ax.get_yaxis_transform(),
        fontsize=8, va="center",
    )

    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"   -> {out_path}")


def main() -> int:
    pc = pd.read_parquet(SRC / "power-curves.parquet")
    print(f"loaded {len(pc):,} power-curve rows from "
          f"{SRC / 'power-curves.parquet'}")

    for taper in ("gaussian", "step"):
        print(f"\n--- taper = {taper} ---")
        wide = build_table(pc, taper=taper)

        # Persist CSV
        csv_path = TBL / f"historian-reachability-table-{taper}.csv"
        wide.to_csv(csv_path, index=False, float_format="%.3f")
        print(f"   -> {csv_path}")

        # Print headline view
        print("\nWorst-case detection rate (min across 3 null models):")
        for level in ("empire", "province", "urban-area"):
            sub = wide[wide["level"] == level].copy()
            sub = sub.sort_values("n")
            print(f"\n  {LEVEL_LABELS[level]}:")
            print("  ", " | ".join(
                ["N".rjust(7)] + [b.ljust(14) for b in BRACKET_ORDER]
            ))
            for _, row in sub.iterrows():
                line = [f"{int(row['n']):>7,}"]
                for b in BRACKET_ORDER:
                    v = row[b]
                    s = f"{v:.3f}" if not pd.isna(v) else "  -  "
                    line.append(s.ljust(14))
                print("   ", " | ".join(line))

        # Render the figure
        png_path = FIG / f"historian-reachability-heatmap-{taper}.png"
        render_heatmap(wide, taper, png_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
