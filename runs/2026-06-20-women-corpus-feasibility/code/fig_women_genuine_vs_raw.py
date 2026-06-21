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


SUBSETS = [("women-overall", T.LATIN, "overall"),
           ("women-wives", T.EMPIRE, "wives"),
           ("women-daughters", T.OKABE_ITO["orange"], "daughters")]


def build():
    x = D.years()
    summ = json.loads((OUT / "women-feasibility-summary.json").read_text())
    a = {u["name"]: (u["alpha_median"], u["n_rows_raw"]) for u in summ["units"]}
    trough = json.loads((OUT / "c2c3-trough-read.json").read_text())

    fig, (axa, axb) = T.figure_2col(height_ratio=0.42, ncols=2,
                                    gridspec_kw={"width_ratios": [1.25, 1.0]})

    # ---- (a) overall: genuine vs raw + band + trough window ----
    meta = json.loads((UNITS / "women-overall.json").read_text())
    raw = np.asarray(meta["raw_aoristic_spa"], float)
    raw_dens = raw / raw.sum() / D.BIN_SIZE
    lo, med, hi = D.quantile_band(D.genuine_draws_npz(DRAWS / "women-overall-pgen.npz"))
    lo, med, hi = (v / D.BIN_SIZE for v in (lo, med, hi))
    axa.axvspan(*TROUGH, color=T.OKABE_ITO["purple"], alpha=0.10, zorder=0)
    axa.text(np.mean(TROUGH), 0.03, "C2–C3 trough", transform=axa.get_xaxis_transform(),
             ha="center", va="bottom", fontsize=6.0, color=T.OKABE_ITO["purple"])
    axa.plot(x, raw_dens, color=T.NEUTRAL, ls="--", lw=1.2, alpha=0.9, zorder=3,
             label="raw aoristic")
    T.band(axa, x, lo, hi, color=T.LATIN, alpha=0.22, zorder=4, label="genuine 95 % band")
    axa.plot(x, med, color=T.LATIN, lw=1.7, zorder=5, label="genuine (de-fogged)")
    axa.set_ylim(0, max(float(raw_dens.max()), float(hi.max())) * 1.12)
    axa.set_xlim(x[0] - 5, x[-1] + 5)
    axa.set_ylabel("probability density (per year)", fontsize=7.5)
    T.year_axis(axa)
    axa.set_title("(a) Overall — de-fogged (uncertain)", fontsize=8.4)
    axa.legend(loc="upper left", fontsize=6.6)

    # ---- (b) per-subset genuine medians (indicative; bands omitted for clarity) ----
    for key, colour, label in SUBSETS:
        d = D.genuine_draws_npz(DRAWS / f"{key}-pgen.npz")
        m = np.median(d, axis=0) / D.BIN_SIZE
        axb.plot(x, m, color=colour, lw=1.5,
                 label=f"{label} (α≈{a[key][0]:.2f}, N={a[key][1]})")
    axb.axvspan(*TROUGH, color=T.OKABE_ITO["purple"], alpha=0.10, zorder=0)
    axb.set_ylim(bottom=0)
    axb.set_xlim(x[0] - 5, x[-1] + 5)
    T.year_axis(axb)
    axb.set_title("(b) By role — genuine medians (indicative)", fontsize=8.4)
    axb.legend(loc="upper left", fontsize=6.2)

    # C2–C3 read (indicative): de-fogging shifts mass INTO the trough window.
    o = trough["women-overall"]; dt = trough["women-daughters"]
    axb.text(0.985, 0.97, "C2–C3 trough mass (raw→genuine):\n"
             f"overall {o['raw_trough_frac']:.2f}→{o['genuine_trough_frac_med']:.2f} "
             f"({o['shift']:+.2f}); daughters {dt['raw_trough_frac']:.2f}→"
             f"{dt['genuine_trough_frac_med']:.2f} ({dt['shift']:+.2f})\n"
             "— indicative only: genuine CIs are very wide",
             transform=axb.transAxes, va="top", ha="right", fontsize=5.3,
             bbox=dict(boxstyle="round,pad=0.3", fc="#F4EEF8",
                       ec=T.OKABE_ITO["purple"], lw=0.5))

    fig.suptitle("Women corpus de-fogging — feasibility (INDICATIVE; ~90% convention, "
                 "below floor → not in the reliable regime)", fontsize=8.4)
    fig.text(0.5, -0.01, "Adela Sobotkova collaboration data; operational filters ours "
             "(confirm with her). Feasibility only — no crossover-age trajectory.",
             ha="center", fontsize=5.4, color=T.NEUTRAL)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM, outdir=OUT)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
