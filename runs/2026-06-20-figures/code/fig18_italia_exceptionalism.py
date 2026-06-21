#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F18 — Italia exceptionalism (Rome vs Italian municipia vs the provinces).
=========================================================================

The three-way de-fogged comparison (spec §8): the imperial capital (Rome), Italian
*municipal* epigraphy (Italia excl. Rome), and the non-Italian Latin provinces.
Two findings:

* **(a) Convention intensity** — both Rome (α ≈ 0.80) AND Italian municipia
  (α ≈ 0.79) are the most convention-dated epigraphy in the empire, well above the
  non-Italian provinces (α ≈ 0.71). Italian epigraphic culture — capital and towns
  alike — is distinctively editorial/formulaic in its dating. (α = CONVENTION
  fraction.)
* **(b) Genuine chronology** — the de-fogged SPD shapes: does Italian municipal
  epigraphy track Rome or the provinces in *timing*?

Descriptive/exploratory (not preregistered); Italian regions = `refit_lib.
_italian_provinces()` ("/ Regio"). Author: Claude Code (Opus 4.8), 2026-06-21.
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
STEM = "fig18-italia-exceptionalism"

UNITS = [
    ("Roma", T.LATIN, ROMA_DRAWS / "Roma-pgen.npz"),
    ("Italia (excl. Rome)", T.OKABE_ITO["orange"], PROD_DRAWS / "Italia_excl._Rome-pgen.npz"),
    ("non-Italian provinces", T.EMPIRE, ROMA_DRAWS / "provinces-non-Italian-Latin-pgen.npz"),
]


def _alpha():
    out = {}
    for u in json.loads(ROMA_SUM.read_text())["units"]:
        out[u["name"]] = (u["alpha_median"], u["alpha_ci"][0], u["alpha_ci"][1])
    ps = json.loads(PROD_SUM.read_text())
    us = ps["units"] if isinstance(ps, dict) and "units" in ps else ps
    for u in (us if isinstance(us, list) else us.values()):
        if u.get("name") == "Italia (excl. Rome)":
            out[u["name"]] = (u["alpha_median"], u["alpha_ci_lo"], u["alpha_ci_hi"])
    return out


def build():
    x = D.years()
    a = _alpha()
    amap = {"Roma": "Roma", "Italia (excl. Rome)": "Italia (excl. Rome)",
            "non-Italian provinces": "provinces-non-Italian-Latin"}

    fig, (axc, axs) = T.figure_2col(height_ratio=0.42, ncols=2,
                                    gridspec_kw={"width_ratios": [1.0, 1.4]})

    # (a) convention-fraction alpha — all FOUR Italia/Rome units (incl. the pooled
    #     Italia-incl-Rome, for completeness).
    alpha_rows = [
        ("Roma", T.LATIN, "Roma"),
        ("Italia (excl. Rome)", T.OKABE_ITO["orange"], "Italia (excl. Rome)"),
        ("Italia (incl. Rome) *", T.OKABE_ITO["purple"], "Italia-incl-Rome"),
        ("non-Italian provinces", T.EMPIRE, "provinces-non-Italian-Latin"),
    ]
    for i, (label, colour, key) in enumerate(alpha_rows):
        med, lo, hi = a[key]
        axc.plot([lo, hi], [i, i], color=colour, lw=2.2, solid_capstyle="round")
        axc.plot([med], [i], "o", color=colour, ms=6)
        axc.text(hi + 0.012, i, f"{med:.2f}", va="center", fontsize=7)
    axc.axvline(0.70, color=T.NEUTRAL, ls=":", lw=0.9)
    axc.text(0.70, -0.45, "α≤0.70\nenvelope", fontsize=6, color=T.NEUTRAL,
             ha="center", va="bottom")
    axc.set_yticks(range(len(alpha_rows)))
    axc.set_yticklabels([u[0] for u in alpha_rows], fontsize=7.0)
    axc.set_ylim(-0.6, len(alpha_rows) - 0.4)
    axc.set_xlim(0.4, 0.95)
    axc.invert_yaxis()
    axc.set_xlabel("convention fraction α\n(→ more editorial convention)", fontsize=7.2)
    axc.set_title("(a) Italy is the most convention-dated", fontsize=8.4)
    axc.grid(axis="x", alpha=0.4); axc.grid(axis="y", visible=False)

    # (b) genuine SPD shapes
    peaks = []
    for label, colour, npz in UNITS:
        lo, med, hi = D.quantile_band(D.genuine_draws_npz(npz))
        lo, med, hi = (v / D.BIN_SIZE for v in (lo, med, hi))
        T.band(axs, x, lo, hi, color=colour, alpha=0.13)
        axs.plot(x, med, color=colour, lw=1.6, label=label)
        peaks.append(float(hi.max()))
    axs.set_ylim(0, max(peaks) * 1.12)
    T.year_axis(axs, ticks=(0, 100, 200, 300))
    axs.set_ylabel("genuine density (per yr)", fontsize=7.5)
    axs.set_title("(b) De-fogged chronologies", fontsize=8.4)
    axs.legend(loc="upper right", fontsize=6.8)

    fig.suptitle("Italian exceptionalism — Rome and Italian municipia are the "
                 "empire's most convention-dated epigraphy", fontsize=8.8)
    fig.text(0.5, -0.02, "* Italia (incl. Rome) pools Rome + municipia; its α (0.73) "
             "is lower than either component — pooling two differently-shaped genuine "
             "signals makes them more separable from the slab basis (and this fit is "
             "ESS-marginal). Read as secondary.", ha="center", fontsize=5.2,
             color=T.NEUTRAL)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
