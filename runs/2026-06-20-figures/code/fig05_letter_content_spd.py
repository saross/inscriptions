#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F5 — Letter-count (content) SPD analogue.
=========================================

The content measure: instead of counting inscriptions, count *letters* (a proxy
for epigraphic output / information flow, Martin's "crucial" nudge). The empire
summed-probability curve for letter mass tracks the inscription-count curve
closely — the content measure corroborates the count measure temporally — with
modest divergences (periods of wordier vs terser inscriptions).

Two letter measures are shown: conservative (only securely-counted letters) and
interpretive (including reconstructed text); both bracket the inscription shape.

NOTE ON UNCERTAINTY: these are *raw* aoristic SPDs (deterministic), so no
credible band is drawn — the inferential content result (within-province
letter-mass scaling, H9) is the F-scaling story, not an SPD band. F5 makes the
descriptive point that content and count share a temporal profile.

Data: ``runs/2026-05-26-letter-count-probe/outputs/tables/empire-spa-three-ways.csv``
(inscription / letter-conservative / letter-interpretive empire SPAs, 80×5y grid).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
CSV = ROOT / "runs/2026-05-26-letter-count-probe/outputs/tables/empire-spa-three-ways.csv"
STEM = "fig05-letter-content-spd"


def _density(col: pd.Series) -> pd.Series:
    """Normalise an SPA column to a per-year density (area = 1)."""
    return col / col.sum() / 5.0  # 5-year bins


def build():
    df = pd.read_csv(CSV)
    x = df["bin_centre"].to_numpy()

    fig, ax = T.figure_1col(height_ratio=0.72)

    ax.plot(x, _density(df["spa_inscription"]), color=T.NEUTRAL, lw=1.6,
            zorder=4, label="inscription count")
    ax.plot(x, _density(df["spa_letter_conservative"]), color=T.LATIN, lw=1.6,
            zorder=5, label="letter mass (conservative)")
    ax.plot(x, _density(df["spa_letter_interpretive"]), color=T.LATIN, lw=1.2,
            ls=(0, (4, 2)), alpha=0.8, zorder=3,
            label="letter mass (interpretive)")

    peak = max(_density(df["spa_inscription"]).max(),
               _density(df["spa_letter_conservative"]).max())
    ax.set_ylim(0, float(peak) * 1.22)
    ax.set_ylabel("probability density (per year)")
    T.year_axis(ax)
    ax.set_title("Content (letter-count) SPD tracks the inscription SPD\n"
                 "(empire, raw aoristic)", fontsize=8.8)
    ax.legend(loc="upper right", fontsize=7.0)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
