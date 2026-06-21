#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Women §6 figure — de-fogging vs tempun vs raw (different artefacts).
===================================================================

The Option-2 §6 comparison (option-2-case-study-outline.md): the women corpus's
temporal distribution three ways — raw aoristic (uncorrected), **tempun**
(Monte-Carlo aoristic dating-uncertainty, mean + 90 % band), and the cc-library
**genuine** de-fogged SPD (+ 95 % band).

**The point:** tempun's mean tracks the raw shape (both peak ~AD 188) — tempun
models *dating uncertainty* but is **blind to editorial convention**; it would
report the AD-188 peak as if genuine. The de-fogging is what diagnoses that the
peak is ~90 % round-slab artefact (here the genuine band is wide because almost
nothing genuine remains to pin down). tempun and de-fogging correct **different**
artefacts — complementary, not redundant.

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-06-20-figures/code"))
import figdata as D       # noqa: E402
import figtheme as T      # noqa: E402

OUT = ROOT / "runs/2026-06-20-women-corpus-feasibility/outputs"
STEM = "fig-women-tempun-comparison"
TEMPUN_COLOUR = T.OKABE_ITO["green"]


def build():
    x = D.years()
    # raw aoristic (overall) → per-year density
    raw = np.asarray(json.loads((OUT / "units/women-overall.json").read_text())
                     ["raw_aoristic_spa"], float)
    raw_dens = raw / raw.sum() / D.BIN_SIZE
    # genuine de-fogged (overall) → per-year density + band
    lo, med, hi = D.quantile_band(D.genuine_draws_npz(OUT / "posterior-draws/women-overall-pgen.npz"))
    lo, med, hi = (v / D.BIN_SIZE for v in (lo, med, hi))
    # tempun (overall): already per-year density on 25-y blocks
    tp = json.loads((OUT / "tempun-women.json").read_text())["subsets"]["overall"]
    tx = np.asarray(tp["block_mid_years"]); tmean = np.asarray(tp["density_mean"])
    tlo = np.asarray(tp["density_lo90"]); thi = np.asarray(tp["density_hi90"])

    fig, ax = T.figure_2col(height_ratio=0.44, ncols=1)

    ax.plot(x, raw_dens, color=T.NEUTRAL, ls="--", lw=1.2, alpha=0.9, zorder=3,
            label="raw aoristic (uncorrected)")
    ax.fill_between(tx, tlo, thi, color=TEMPUN_COLOUR, alpha=0.16, zorder=2)
    ax.plot(tx, tmean, color=TEMPUN_COLOUR, lw=1.7, marker="o", ms=3, zorder=4,
            label="tempun (aoristic MC: mean + 90 % band)")
    T.band(ax, x, lo, hi, color=T.LATIN, alpha=0.20, zorder=2)
    ax.plot(x, med, color=T.LATIN, lw=1.7, zorder=5,
            label="genuine de-fogged (+ 95 % band)")

    ax.set_ylim(bottom=0)
    ax.set_xlim(x[0] - 5, x[-1] + 5)
    ax.set_ylabel("probability density (per year)")
    T.year_axis(ax)
    ax.set_title("Women corpus: tempun (dating uncertainty) vs de-fogging "
                 "(convention) — different artefacts", fontsize=8.4)
    ax.legend(loc="upper left", fontsize=6.8)
    ax.text(0.985, 0.96, "tempun tracks the RAW shape (peaks ~AD 188): it models\n"
            "dating uncertainty but is blind to editorial convention.\n"
            "De-fogging diagnoses the ~90 % convention (wide genuine band\n"
            "= little genuine signal to recover). Complementary, not redundant.",
            transform=ax.transAxes, va="top", ha="right", fontsize=5.8,
            bbox=dict(boxstyle="round,pad=0.35", fc="#EEF5EE", ec=TEMPUN_COLOUR, lw=0.6))
    ax.text(0.985, 0.02, "Adela Sobotkova collaboration data; feasibility/case-study "
            "only — no crossover trajectory.", transform=ax.transAxes,
            va="bottom", ha="right", fontsize=5.2, color=T.NEUTRAL)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM, outdir=OUT)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
