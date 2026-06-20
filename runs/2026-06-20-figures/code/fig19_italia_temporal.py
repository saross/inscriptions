#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F19 — Italia temporal read (Italian municipia vs the provinces over time).
==========================================================================

The de-fogged genuine-SPD trajectories of Italian municipal epigraphy (Italia
excl. Rome) and the non-Italian Latin provinces, with the Severan watershed (the
Antonine Constitution, AD 212) marked. Reads descriptively *when* the two
chronologies diverge or converge — is Italian distinctiveness concentrated
*before* the Severan period?

Method note (spec §8): this uses the FULL-WINDOW de-fogged trajectories, NOT
per-50-year-period deconvolution fits — within a single 50 y period the 50–300 y
convention slabs are not separable from genuine (identifiability needs the full
envelope), so per-period α would be unsound. The full-window genuine trajectories
carry the temporal divergence descriptively. Exploratory; not preregistered.

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import figdata as D
import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
ROMA_DRAWS = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs/posterior-draws"
PROD_DRAWS = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
STEM = "fig19-italia-temporal"
ANTONINE_CONSTITUTION = 212  # AD; the Severan-era watershed marker.


def build():
    x = D.years()
    ital = D.genuine_draws_npz(PROD_DRAWS / "Italia_excl._Rome-pgen.npz")
    prov = D.genuine_draws_npz(ROMA_DRAWS / "provinces-non-Italian-Latin-pgen.npz")

    fig, ax = T.figure_2col(height_ratio=0.42, ncols=1)

    # Severan-watershed shading (AD 193–235, Severan dynasty) + AD 212 line.
    ax.axvspan(193, 235, color=T.NEUTRAL, alpha=0.08, zorder=0)
    ax.axvline(ANTONINE_CONSTITUTION, color=T.OKABE_ITO["black"], lw=0.8, ls=":",
               zorder=1)
    ax.annotate("Antonine\nConstitution\n(AD 212)", xy=(ANTONINE_CONSTITUTION, 1),
                xytext=(ANTONINE_CONSTITUTION + 6, 0.95), textcoords=("data", "axes fraction"),
                fontsize=6.3, va="top", ha="left")

    for draws, colour, label in [
            (ital, T.OKABE_ITO["orange"], "Italia (excl. Rome) — municipia"),
            (prov, T.EMPIRE, "non-Italian Latin provinces")]:
        lo, med, hi = D.quantile_band(draws)
        lo, med, hi = (v / D.BIN_SIZE for v in (lo, med, hi))
        T.band(ax, x, lo, hi, color=colour, alpha=0.16)
        ax.plot(x, med, color=colour, lw=1.8, label=label)

    ax.set_ylim(bottom=0)
    ax.set_ylabel("genuine density (per year)")
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.set_title("Italian municipal vs provincial chronology, de-fogged "
                 "(Severan watershed marked)", fontsize=8.6)
    ax.legend(loc="upper right", fontsize=7.2)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
