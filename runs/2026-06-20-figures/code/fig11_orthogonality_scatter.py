#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F11 — Two over-production channels are independent.
===================================================

Two distinct ways an inscription corpus can be "more than expected":

* **scaling residual** (x) — more *inscriptions* than the city's population
  predicts ("prolific for size", the H3a over-production channel);
* **content residual** (y) — more *letters per inscription* than its count
  predicts ("verbose per act", the A01 content channel).

They are statistically orthogonal (Spearman ρ ≈ 0; Obs 108): a city's tendency to
over-produce inscriptions tells you nothing about whether its inscriptions are
wordier. Points are coloured by quadrant; axes centred on the medians.

Data: ``runs/2026-06-20-a01-content-residual/outputs/content-residual-per-city.csv``
(817 Latin cities).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
CSV = ROOT / "runs/2026-06-20-a01-content-residual/outputs/content-residual-per-city.csv"
STEM = "fig11-orthogonality-scatter"


def build():
    df = pd.read_csv(CSV).dropna(subset=["scaling_residual", "content_residual"])
    x = df["scaling_residual"].to_numpy()
    y = df["content_residual"].to_numpy()
    # Centre on medians for a clean cross-haired scatter (rank stats unaffected).
    xc = x - np.median(x)
    yc = y - np.median(y)
    rho, p = spearmanr(x, y)

    fig, ax = T.figure_1col(height_ratio=0.92)

    T.zero_line(ax, "h")
    T.zero_line(ax, "v")
    ax.scatter(xc, yc, s=9, color=T.LATIN, alpha=0.40, linewidths=0, zorder=3)

    # A least-squares line to show the (near-zero) tilt.
    b, a = np.polyfit(xc, yc, 1)
    xs = np.linspace(xc.min(), xc.max(), 50)
    ax.plot(xs, a + b * xs, color=T.OKABE_ITO["black"], lw=1.0, ls="--",
            zorder=4)

    ax.text(0.03, 0.97, f"Spearman ρ = {rho:+.3f}  (p = {p:.2f})\n"
            "→ channels independent", transform=ax.transAxes, va="top",
            fontsize=7.5, bbox=dict(boxstyle="round,pad=0.3", fc="white",
                                    ec=T.NEUTRAL, lw=0.5, alpha=0.9))

    ax.set_xlabel("scaling residual  (inscriptions vs population:\n"
                  "“prolific for size” →)")
    ax.set_ylabel("content residual  (letters vs count:\n“verbose per act” →)")
    ax.set_title("Over-production channels are orthogonal", fontsize=9.0)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
