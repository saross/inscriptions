#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F9 — Where a city's temporal variation comes from.
===================================================

A city's inscription rate through time is built from four nested ingredients: a
shared empire-wide rhythm, a province-specific wobble, a city-specific wobble,
and a steady overall level (how prolific the city is, regardless of timing).

The figure has two parts:

* **Top — the clean three-way partition** of a typical city's *temporal*
  variation into empire-common, province, and city-unique shares (these sum to
  100 %; covariance-attributed, mean over cities/draws). This is the headline:
  empire-common ≈ 38 %, province ≈ 29 %, city-unique ≈ 33 %.
* **Bottom — the magnitudes** of all four components as posterior-median
  log-rate standard deviations (comparable across components), including the
  cross-sectional "level" axis the partition does not cover.

Footnote: the common component's *standalone* share is 54 % (higher than its
38 % partition share because the three temporal tiers are negatively correlated
— they partly offset each other). Obs 101 language: "empire-wide common temporal
component", not "epigraphic habit".

Data: ``h5-decomposition.json`` (component SDs + standalone common share);
``temporal-three-way-split.json`` (the clean partition).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
H5 = ROOT / "runs/2026-06-17-s5-h5-habit-removed/outputs/h5-decomposition.json"
SPLIT = ROOT / "runs/2026-06-20-figures/outputs/temporal-three-way-split.json"
STEM = "fig09-variance-partition"

# Tier colours (shared between the partition bar and the magnitude bars).
C_COMMON, C_PROV, C_CITY, C_LEVEL = (
    T.EMPIRE, T.OKABE_ITO["green"], T.OKABE_ITO["orange"], T.NEUTRAL)


def build():
    d = json.loads(H5.read_text())
    common = d["shared_empire_common"]
    allp = d["all_provinces"]
    latin = d["latin_minus_roma"]
    part = json.loads(SPLIT.read_text())["all_provinces"]["method_c_cov_attributed_mean"]

    fig, (axp, axs) = T.custom(T.WIDTH_1COL, T.WIDTH_1COL * 1.18, nrows=2,
                               gridspec_kw={"height_ratios": [1.0, 4.2]})

    # ---- top: the clean three-way temporal partition (stacked bar) -----------
    shares = [("empire-common", part["common_g"], C_COMMON),
              ("province", part["province_u"], C_PROV),
              ("city-unique", part["city_v_unique"], C_CITY)]
    left = 0.0
    for label, frac, colour in shares:
        axp.barh(0, frac, left=left, height=0.7, color=colour,
                 edgecolor="white", linewidth=0.8)
        axp.text(left + frac / 2, 0, f"{label}\n{frac*100:.0f}%", ha="center",
                 va="center", fontsize=6.6,
                 color="white" if colour != C_CITY else "black", fontweight="bold")
        left += frac
    axp.set_xlim(0, 1)
    axp.set_ylim(-0.5, 0.5)
    axp.axis("off")
    axp.set_title("Temporal variation of a typical city — three-way split "
                  "(sums to 100 %)", fontsize=8.2)

    # ---- bottom: component magnitudes (log-rate SDs) -------------------------
    labels = ["Empire-common\ntemporal", "Province\ntemporal",
              "City-specific\ntemporal", "Between-city\nlevel"]
    vals = [common["sd_common_temporal_g"], common["sd_province_temporal_u"],
            allp["sd_city_temporal_v"], allp["sd_level_lograte"]]
    vals_latin = [common["sd_common_temporal_g"], common["sd_province_temporal_u"],
                  latin["sd_city_temporal_v"], latin["sd_level_lograte"]]
    colours = [C_COMMON, C_PROV, C_CITY, C_LEVEL]
    xpos = np.arange(len(labels))

    axs.bar(xpos, vals, width=0.62, color=colours, zorder=3,
            edgecolor="white", linewidth=0.5)
    axs.scatter(xpos, vals_latin, marker="_", s=200, color=T.OKABE_ITO["black"],
                linewidths=1.3, zorder=5, label="Latin-minus-Roma")
    for x, val in zip(xpos, vals):
        axs.text(x, val + 0.02, f"{val:.2f}", ha="center", va="bottom", fontsize=7.5)
    axs.set_xticks(xpos)
    axs.set_xticklabels(labels, fontsize=7.3)
    axs.set_ylabel("log-rate standard deviation\n(posterior median)")
    axs.set_ylim(0, max(vals) * 1.18)
    axs.grid(axis="y", alpha=0.4)
    axs.set_title("Relative magnitude of the four components", fontsize=8.6)
    axs.legend(loc="upper right", fontsize=7.0)
    axs.text(0.5, -0.30, "Standalone common share is 54 % (higher than its 38 % "
             "partition share:\nthe three temporal tiers are anti-correlated and "
             "partly offset).", transform=axs.transAxes, ha="center", va="top",
             fontsize=6.0, style="italic", color=T.NEUTRAL)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
