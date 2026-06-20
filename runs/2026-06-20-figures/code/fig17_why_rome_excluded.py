#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F17 — "Why Rome is excluded" (illustrative leverage demo).
==========================================================

A pooled scaling scatter (log inscription count vs log population, all cities)
with **Rome plotted as the extreme high-leverage outlier**, and the fitted
log-log scaling line shown **with vs without Rome** — making Hanson 2021's
Fig. 7.4 exclusion point visually concrete. Rome (pop ≈ 923,000; count ≈ 65,000)
sits ~2.3× the next-largest population and ~14× the next-largest inscription
count; including it visibly drags the fitted line.

This is the methods-section exhibit for *why* the Rome exclusion (Decision 36;
Hanson's only statistical outlier) is justified. **Framing (spec §3.3):** the
pooled / between-city scaling, NOT the within-province Mundlak — Rome is alone in
its own province, so it carries no within-province contrast; the distortion is the
high-leverage outlier in the pooled fit. Illustrative; not a confirmatory fit.

Data: `data/processed/city_level_for_h3a.parquet` (1,044 Rome-excluded cities:
`urban_context_pop_est`, `inscription_count`) + Rome appended from the filtered
LIRE corpus (`urban_context_pop_est` for Roma; count = filtered rows with
`urban_context_city == "Roma"`).

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
FRAME = ROOT / "data/processed/city_level_for_h3a.parquet"
STEM = "fig17-why-rome-excluded"

sys.path.insert(0, str(ROOT / "runs/2026-06-07-h2.1-launch-prep/code"))
import h2_lib as H  # noqa: E402


def _rome_point():
    """Rome's (population, count) from the filtered corpus — the outlier point."""
    df = H.load_filtered_lire()
    roma = df.loc[df["urban_context_city"] == "Roma"]
    pop = float(roma["urban_context_pop_est"].dropna().mode().iloc[0])  # 923,313
    count = int(len(roma))
    return pop, count


def build():
    fr = pd.read_parquet(FRAME)
    x = np.log(fr["urban_context_pop_est"].to_numpy())
    y = np.log(fr["inscription_count"].clip(lower=1).to_numpy())
    rpop, rcount = _rome_point()
    rx, ry = np.log(rpop), np.log(rcount)

    # OLS log-log fits: without Rome (the frame) vs with Rome appended.
    b_wo, a_wo = np.polyfit(x, y, 1)
    xw = np.append(x, rx); yw = np.append(y, ry)
    b_w, a_w = np.polyfit(xw, yw, 1)

    fig, ax = T.figure_1col(height_ratio=0.92)

    ax.scatter(x, y, s=7, color=T.NEUTRAL, alpha=0.40, linewidths=0, zorder=2,
               label="city (Rome excluded)")
    ax.scatter([rx], [ry], s=70, color=T.LATIN, marker="*", linewidths=0,
               zorder=5, label="Rome")

    xs = np.linspace(min(x.min(), rx), max(x.max(), rx), 50)
    ax.plot(xs, a_wo + b_wo * xs, color=T.EMPIRE, lw=1.7, zorder=4,
            label=f"fit without Rome (β={b_wo:.2f})")
    ax.plot(xs, a_w + b_w * xs, color=T.OKABE_ITO["orange"], lw=1.5,
            ls="--", zorder=4, label=f"fit WITH Rome (β={b_w:.2f})")

    ax.annotate("Rome — the only\nHanson outlier", xy=(rx, ry),
                xytext=(rx - 3.4, ry - 0.3), fontsize=7.0, ha="left", va="top",
                color=T.LATIN,
                arrowprops=dict(arrowstyle="->", lw=0.7, color=T.LATIN))

    ax.set_xlabel("log population (Hanson estimate)")
    ax.set_ylabel("log inscription count")
    ax.set_title("Why Rome is excluded from the scaling regressions",
                 fontsize=8.8)
    ax.legend(loc="lower right", fontsize=6.6)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
