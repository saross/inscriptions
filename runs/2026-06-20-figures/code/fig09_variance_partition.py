#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F9 — Magnitude of the nested log-rate components.
=================================================

The empirical decomposition of a city's log inscription-rate into four nested
components, shown as their posterior-median log-rate standard deviations (the
units are comparable across components, h5-decomposition.json):

* **Empire-common temporal (g)** — the shared temporal swing (peaks AD 188);
  the largest component.
* **Province temporal (u)** and **City temporal (v)** — the residual temporal
  deviations at the province and city tiers.
* **Between-city level** — the cross-sectional (population) axis: how much cities
  differ in overall level, independent of shape.

The common component alone accounts for ≈ 54 % of a typical city's *temporal*
variance (Var_t(g) / Var_t(g+u+v)); the three temporal tiers do not partition
cleanly (they are negatively correlated — see temporal-three-way-split.json).
Language framing (Obs 101): "empire-wide common temporal component", not
"epigraphic habit". Latin-minus-Roma values are materially identical (annotated).

Data: ``runs/2026-06-17-s5-h5-habit-removed/outputs/h5-decomposition.json``.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
H5 = ROOT / "runs/2026-06-17-s5-h5-habit-removed/outputs/h5-decomposition.json"
STEM = "fig09-variance-partition"


def build():
    d = json.loads(H5.read_text())
    common = d["shared_empire_common"]
    allp = d["all_provinces"]
    latin = d["latin_minus_roma"]

    # Four components (posterior-median log-rate SDs), all-provinces frame.
    labels = ["Empire-common\ntemporal (g)", "Province\ntemporal (u)",
              "City\ntemporal (v)", "Between-city\nlevel"]
    vals = [common["sd_common_temporal_g"], common["sd_province_temporal_u"],
            allp["sd_city_temporal_v"], allp["sd_level_lograte"]]
    # Latin-minus-Roma counterparts (g, u shared; v, level differ slightly).
    vals_latin = [common["sd_common_temporal_g"], common["sd_province_temporal_u"],
                  latin["sd_city_temporal_v"], latin["sd_level_lograte"]]
    colours = [T.EMPIRE, T.OKABE_ITO["green"], T.OKABE_ITO["orange"], T.NEUTRAL]
    common_share = allp["median_common_share_of_temporal_var"]

    fig, ax = T.figure_1col(height_ratio=0.80)
    xpos = np.arange(len(labels))

    bars = ax.bar(xpos, vals, width=0.62, color=colours, zorder=3,
                  edgecolor="white", linewidth=0.5)
    # Latin-minus-Roma markers (≈identical) as small ticks.
    ax.scatter(xpos, vals_latin, marker="_", s=220, color=T.OKABE_ITO["black"],
               linewidths=1.3, zorder=5, label="Latin-minus-Roma")

    for x, val in zip(xpos, vals):
        ax.text(x, val + 0.02, f"{val:.2f}", ha="center", va="bottom",
                fontsize=7.5)

    ax.set_xticks(xpos)
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_ylabel("log-rate standard deviation\n(posterior median)")
    ax.set_ylim(0, max(vals) * 1.18)
    ax.grid(axis="y", alpha=0.4)
    ax.legend(loc="upper right", fontsize=7.0)

    # Title + the common-temporal share as a subtitle (above the plot, no
    # overlap with the tall left-hand bars).
    ax.set_title("Relative magnitude of the nested log-rate components",
                 fontsize=9.0, pad=18)
    ax.text(0.5, 1.025, f"common (g) $\\approx$ {common_share*100:.0f}% of a "
            "typical city's temporal variance", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=7.3, style="italic",
            color=T.EMPIRE)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
