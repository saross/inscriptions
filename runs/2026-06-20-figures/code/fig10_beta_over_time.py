#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F10 — Within-province scaling exponent over time (the U-shape).
===============================================================

The within-province population–epigraphy scaling exponent β_within, fitted
independently in each of the eight 50-year periods (H7), for both frames. It
traces a shallow U: steeper early (~0.70), a high-empire plateau near 0.58
(≈ the pooled cumulative value), and a steepening again in the 4th century. The
exponent is well below 1 throughout — sublinear scaling in every period.

Data: ``h7-summary.json`` (empire) + ``h7-latin-summary.json`` (Latin), each
period's β_within median + 95 % CI.

Encoding: empire = blue, Latin = vermillion; median line + 95 % ribbon; the
high-empire plateau annotated.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
H7E = ROOT / "runs/2026-06-17-s5-h7-perperiod-h3c/outputs/h7-summary.json"
H7L = ROOT / "runs/2026-06-18-h7-latin/outputs/h7-latin-summary.json"
STEM = "fig10-beta-over-time"


def _series(path):
    """(midpoints, median, lo, hi) of β_within across periods from an h7 JSON."""
    d = json.loads(path.read_text())
    labels = d["period_labels"]
    mids, med, lo, hi = [], [], [], []
    for lab in labels:
        a, b = (float(v) for v in lab.split(".."))
        mids.append((a + b) / 2.0)
        pp = d["per_period"][lab]
        med.append(pp["beta_within_median"])
        lo.append(pp["beta_within_ci"][0])
        hi.append(pp["beta_within_ci"][1])
    return (np.array(mids), np.array(med), np.array(lo), np.array(hi))


def build():
    fig, ax = T.figure_1col(height_ratio=0.74)

    for path, colour, label in [(H7E, T.EMPIRE, "empire"),
                                (H7L, T.LATIN, "Latin")]:
        mids, med, lo, hi = _series(path)
        T.band(ax, mids, lo, hi, color=colour, alpha=0.18)
        ax.plot(mids, med, "-o", color=colour, ms=4, lw=1.5, label=label)

    # The pooled cumulative empire value (β_within ≈ 0.587) as a reference.
    ax.axhline(0.587, color=T.NEUTRAL, ls=":", lw=0.9, zorder=1)
    ax.text(330, 0.587, "pooled\n0.587", fontsize=6.3, color=T.NEUTRAL,
            va="center", ha="left")
    # Sublinear reference (β = 1).
    ax.axhline(1.0, color=T.NEUTRAL, ls=(0, (2, 3)), lw=0.7, alpha=0.6, zorder=1)
    ax.text(-45, 1.0, "linear (β = 1)", fontsize=6.3, color=T.NEUTRAL,
            va="bottom", ha="left")

    ax.annotate("high-empire plateau ≈ 0.58", xy=(150, 0.585),
                xytext=(40, 0.30), fontsize=6.8,
                arrowprops=dict(arrowstyle="->", lw=0.6, color=T.OKABE_ITO["black"]))

    ax.set_ylim(0.1, 1.12)
    ax.set_xlim(-55, 360)
    ax.set_ylabel("within-province scaling exponent β$_{within}$")
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.set_title("Sublinear scaling in every period (U-shaped over time)",
                 fontsize=8.8)
    ax.legend(loc="upper right", fontsize=7.5)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
