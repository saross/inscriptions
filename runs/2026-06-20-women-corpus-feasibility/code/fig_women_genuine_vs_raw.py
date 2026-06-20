#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Women feasibility figure — genuine vs raw SPD + the reachability verdict.
========================================================================

The deliverable figure for the "From Graveyard to Time Series" feasibility study
(spec runs/2026-06-20-women-corpus-feasibility/spec.md, Stage 1): the datable
conjugal women corpus's raw aoristic SPD vs its de-fogged genuine SPD with 95 %
band, with the C2–C3 crossover-trough window (~AD 150–275) marked.

**The honest verdict, shown on the figure:** the corpus is ~90 % editorial
convention (convention fraction α ≈ 0.90 overall / 0.84 daughters) and below/at
the reachability floor (overall N=1,291 and wives N=838 marginal; daughters N=453
below the 500 floor). With α far above the 0.70 reliable envelope, the corpus is
NOT in the reliable de-fogging regime — a valid, important feasibility outcome:
the time-resolution of the crossover claim cannot be rescued by de-fogging here.

Collaboration data (Adela Sobotkova, Aarhus) — for the co-author conversation, NOT
for publication without her involvement. Operational filters ours (flag for her
confirmation). Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21.
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
UNITS = OUT / "units"
DRAWS = OUT / "posterior-draws"
STEM = "fig-women-genuine-vs-raw"
TROUGH = (150, 275)  # C2–C3 crossover-trough window of interest (descriptive)


def build():
    x = D.years()
    meta = json.loads((UNITS / "women-overall.json").read_text())
    raw = np.asarray(meta["raw_aoristic_spa"], float)
    raw_dens = raw / raw.sum() / D.BIN_SIZE
    lo, med, hi = D.quantile_band(D.genuine_draws_npz(DRAWS / "women-overall-pgen.npz"))
    lo, med, hi = (v / D.BIN_SIZE for v in (lo, med, hi))

    summ = json.loads((OUT / "women-feasibility-summary.json").read_text())
    a = {u["name"]: (u["alpha_median"], u["n_rows_raw"]) for u in summ["units"]}

    fig, ax = T.figure_2col(height_ratio=0.42, ncols=1)

    # C2–C3 trough window of interest.
    ax.axvspan(*TROUGH, color=T.OKABE_ITO["purple"], alpha=0.10, zorder=0)
    ax.text(np.mean(TROUGH), 0.04, "C2–C3 trough window", transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=6.2, color=T.OKABE_ITO["purple"])

    ax.plot(x, raw_dens, color=T.NEUTRAL, ls="--", lw=1.2, alpha=0.9, zorder=3,
            label="raw aoristic (uncorrected)")
    T.band(ax, x, lo, hi, color=T.LATIN, alpha=0.22, zorder=4, label="genuine 95 % band")
    ax.plot(x, med, color=T.LATIN, lw=1.7, zorder=5, label="genuine (de-fogged)")

    ax.set_ylim(0, max(float(raw_dens.max()), float(hi.max())) * 1.18)
    ax.set_xlim(x[0] - 5, x[-1] + 5)
    ax.set_ylabel("probability density (per year)")
    T.year_axis(ax)
    ax.set_title("Women corpus de-fogging — feasibility (datable conjugal corpus)",
                 fontsize=8.8)
    ax.legend(loc="upper left", fontsize=7.0)

    verdict = (
        f"FEASIBILITY VERDICT — not in the reliable de-fogging regime:\n"
        f"• convention fraction α ≈ {a['women-overall'][0]:.2f} overall / "
        f"{a['women-daughters'][0]:.2f} daughters  (~90% editorial convention)\n"
        f"• N: overall {a['women-overall'][1]}, wives {a['women-wives'][1]} (marginal); "
        f"daughters {a['women-daughters'][1]} (below the 500 floor)\n"
        f"• α ≫ 0.70 reliable envelope → de-fogging cannot rescue the time-resolution here")
    ax.text(0.985, 0.96, verdict, transform=ax.transAxes, va="top", ha="right",
            fontsize=6.0, bbox=dict(boxstyle="round,pad=0.35", fc="#FBEEF3",
                                    ec=T.LATIN, lw=0.7))
    ax.text(0.985, 0.02, "Adela Sobotkova collaboration data; operational filters "
            "ours (confirm with her). Feasibility only — no crossover trajectory.",
            transform=ax.transAxes, va="bottom", ha="right", fontsize=5.4,
            color=T.NEUTRAL)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM, outdir=OUT)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
