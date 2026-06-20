#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F16 — Capital comparison (Rome vs provincial capitals vs aggregates).
=====================================================================

The de-fogged "capital comparison" (spec runs/2026-06-21-rome-capital-comparison/
spec.md), two tracks sharing the one universal library basis:

* **(a) Empire frame** — genuine SPD of Rome vs the empire-62 provincial-capitals
  composite vs the empire aggregate.
* **(b) Latin frame** — genuine SPD of the Latin-41 capitals vs the Latin
  aggregate (Rome-free; clean Latin-primary comparison).
* **(c) Convention intensity** — each unit's **convention fraction α** (median +
  95 % CI). NB α IS THE CONVENTION FRACTION (1 − α = genuine); higher α = more
  editorial-convention dating. The 0.70 reliable-envelope line is marked.

Headline: **Rome is the most convention-dated unit (α ≈ 0.80)** — far above the
provincial capitals (α ≈ 0.56), which are themselves *less* convention-dated than
the general provinces/aggregates. The imperial capital's apparent chronology is
the most editorial of all.

Data: genuine-SPD draws (this run's + the production refit's posterior-draws);
α from the unit summaries. Descriptive/exploratory; Rome excluded from all
regressions (Decision 36).

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figdata as D
import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
ROMA_DRAWS = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs/posterior-draws"
PROD_DRAWS = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
ROMA_SUM = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs/roma-italia-summary.json"
PROD_SUM = ROOT / "runs/2026-06-13-cc-production-refit/outputs/refit-summary.json"
STEM = "fig16-capital-comparison"


def _alpha_lookup():
    """unit name -> (alpha_median, ci_lo, ci_hi) [convention fraction]."""
    out = {}
    rs = json.loads(ROMA_SUM.read_text())
    for u in rs["units"]:
        out[u["name"]] = (u["alpha_median"], u["alpha_ci"][0], u["alpha_ci"][1])
    ps = json.loads(PROD_SUM.read_text())
    units = ps["units"] if isinstance(ps, dict) and "units" in ps else ps
    for u in (units if isinstance(units, list) else units.values()):
        if u.get("name") in ("empire-aggregate", "latin-aggregate"):
            out[u["name"]] = (u["alpha_median"], u["alpha_ci_lo"], u["alpha_ci_hi"])
    return out


def _draws(unit, prod=False):
    return D.genuine_draws_npz((PROD_DRAWS if prod else ROMA_DRAWS)
                               / f"{D.safe_name(unit)}-pgen.npz")


def _plot_spd(ax, x, draws, colour, label):
    lo, med, hi = D.quantile_band(draws)
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))
    T.band(ax, x, lo, hi, color=colour, alpha=0.14)
    ax.plot(x, med, color=colour, lw=1.6, label=label)
    return float(hi.max())


def build():
    x = D.years()
    a = _alpha_lookup()

    fig, axes = T.figure_2col(height_ratio=0.40, ncols=3,
                              gridspec_kw={"width_ratios": [1.25, 1.0, 1.05]})
    axa, axb, axc = axes

    # (a) empire frame
    peaks = [
        _plot_spd(axa, x, _draws("empire-aggregate", prod=True), T.EMPIRE,
                  "empire aggregate"),
        _plot_spd(axa, x, _draws("capitals-empire-62"), T.OKABE_ITO["green"],
                  "prov. capitals (62)"),
        _plot_spd(axa, x, _draws("Roma"), T.LATIN, "Roma"),
    ]
    axa.set_ylim(0, max(peaks) * 1.12)
    T.year_axis(axa, ticks=(0, 100, 200, 300))
    axa.set_ylabel("genuine density (per yr)", fontsize=7.5)
    axa.set_title("(a) Empire frame", fontsize=8.5)
    axa.legend(loc="upper right", fontsize=6.6)

    # (b) latin frame
    peaks_b = [
        _plot_spd(axb, x, _draws("latin-aggregate", prod=True), T.EMPIRE,
                  "Latin aggregate"),
        _plot_spd(axb, x, _draws("capitals-latin-41"), T.OKABE_ITO["green"],
                  "Latin capitals (41)"),
    ]
    axb.set_ylim(0, max(peaks_b) * 1.12)
    T.year_axis(axb, ticks=(0, 100, 200, 300))
    axb.set_title("(b) Latin frame (Rome-free)", fontsize=8.5)
    axb.legend(loc="upper right", fontsize=6.6)

    # (c) convention-fraction alpha strip
    rows = [
        ("Roma", "Roma", T.LATIN),
        ("prov. capitals (emp-62)", "capitals-empire-62", T.OKABE_ITO["green"]),
        ("Latin capitals (41)", "capitals-latin-41", T.OKABE_ITO["green"]),
        ("empire aggregate", "empire-aggregate", T.EMPIRE),
        ("Latin aggregate", "latin-aggregate", T.EMPIRE),
    ]
    for i, (label, key, colour) in enumerate(rows):
        med, lo, hi = a[key]
        axc.plot([lo, hi], [i, i], color=colour, lw=2.0, solid_capstyle="round")
        axc.plot([med], [i], "o", color=colour, ms=5)
        axc.text(hi + 0.01, i, f"{med:.2f}", va="center", fontsize=6.5)
    axc.axvline(0.70, color=T.NEUTRAL, ls=":", lw=0.9)
    axc.text(0.70, len(rows) - 0.4, " reliable\n envelope\n α≤0.70", fontsize=5.8,
             color=T.NEUTRAL, va="top", ha="left")
    axc.set_yticks(range(len(rows)))
    axc.set_yticklabels([r[0] for r in rows], fontsize=6.8)
    axc.set_ylim(-0.6, len(rows) - 0.4)
    axc.set_xlim(0.0, 1.0)
    axc.invert_yaxis()
    axc.set_xlabel("convention fraction α\n(→ more editorial convention)", fontsize=7.0)
    axc.set_title("(c) Convention intensity", fontsize=8.5)
    axc.grid(axis="x", alpha=0.4)
    axc.grid(axis="y", visible=False)

    fig.suptitle("Capital comparison — Rome is the most convention-dated unit "
                 "(α = convention fraction)", fontsize=9.2)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
