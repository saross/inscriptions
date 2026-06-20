#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F7 — Population–epigraphy scaling: within vs between province.
==============================================================

The headline scaling result (H3a), shown as the Mundlak within/between split on
the Latin diagnostic frame (817 cities, Roma excluded):

* **(a) Within province** — an added-variable plot: each city's
  within-province population deviation (x) against its within-province
  inscription-count deviation (y = log count minus its province mean). The
  relationship is steep and supported; the fitted NBR slope is
  β_within = 0.73 [0.65, 0.82]. Provincial capitals (highlighted) sit above the
  cloud (their over-production, F6).
* **(b) Between province** — one point per province: province mean population
  (x) vs province mean log count (y). The fitted slope β_between = 0.04
  [−0.48, 0.57] crosses zero — between-province scaling is flat and uncertain.

So the population–epigraphy association is a *within*-province phenomenon. Framed
as "association with population", model-conditional (Obs 101); not a causal law.

Data: ``city_level_for_h3a_latin.parquet`` (Mundlak columns) + the Latin betas
from ``h3a-results.json`` (sensitivity_B_latin); capital list from the H3c-i JSON.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
FRAME = ROOT / "data/processed/city_level_for_h3a_latin.parquet"
H3A = ROOT / "runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json"
CAPS = ROOT / "runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results-oxrep-primary.json"
STEM = "fig07-pop-epigraphy-within-between"


def build():
    df = pd.read_parquet(FRAME).copy()
    betas = json.loads(H3A.read_text())["sensitivity_B_latin"]["betas"]
    b_w = betas["beta_within"]
    b_b = betas["beta_between"]
    caps = set(json.loads(CAPS.read_text())["latin"]["capital_cities"])

    df["log_count"] = np.log(df["inscription_count"].clip(lower=1))
    df["is_capital"] = df["city"].isin(caps)
    # Within-province count deviation (added-variable plot y-axis).
    df["log_count_within"] = df["log_count"] - df.groupby("province")["log_count"].transform("mean")

    fig, (axw, axb) = T.custom(T.WIDTH_1COL, T.WIDTH_1COL * 1.5, nrows=2)

    # --- panel (a): within-province added-variable plot -----------------------
    noncap = df[~df["is_capital"]]
    cap = df[df["is_capital"]]
    axw.scatter(noncap["log_pop_within"], noncap["log_count_within"], s=7,
                color=T.NEUTRAL, alpha=0.40, linewidths=0, zorder=2,
                label="city")
    axw.scatter(cap["log_pop_within"], cap["log_count_within"], s=16,
                color=T.LATIN, alpha=0.9, marker="^", linewidths=0, zorder=4,
                label="provincial capital")
    xs = np.linspace(df["log_pop_within"].min(), df["log_pop_within"].max(), 50)
    axw.plot(xs, b_w["median"] * xs, color=T.LATIN, lw=1.8, zorder=5)
    # Slope-uncertainty fan through the origin.
    T.band(axw, xs, b_w["ci_lo"] * xs, b_w["ci_hi"] * xs, color=T.LATIN,
           alpha=0.15, zorder=1)
    axw.text(0.04, 0.92, f"β$_{{within}}$ = {b_w['median']:.2f} "
             f"[{b_w['ci_lo']:.2f}, {b_w['ci_hi']:.2f}]",
             transform=axw.transAxes, fontsize=7.5, va="top")
    axw.set_xlabel("within-province population deviation (log)")
    axw.set_ylabel("within-province count\ndeviation (log)")
    axw.set_title("(a) Within province — steep, supported", fontsize=9.0)
    axw.legend(loc="lower right", fontsize=7.0)

    # --- panel (b): between-province (one point per province) -----------------
    prov = df.groupby("province").agg(
        log_pop_prov_mean=("log_pop_prov_mean", "first"),
        mean_log_count=("log_count", "mean"),
        n_cities=("city", "size")).reset_index()
    axb.scatter(prov["log_pop_prov_mean"], prov["mean_log_count"],
                s=12 + prov["n_cities"] * 0.4, color=T.EMPIRE, alpha=0.7,
                linewidths=0, zorder=3)
    xb = np.linspace(prov["log_pop_prov_mean"].min(),
                     prov["log_pop_prov_mean"].max(), 50)
    centre_x = prov["log_pop_prov_mean"].mean()
    centre_y = prov["mean_log_count"].mean()
    axb.plot(xb, centre_y + b_b["median"] * (xb - centre_x), color=T.EMPIRE,
             lw=1.8, zorder=4)
    T.band(axb, xb, centre_y + b_b["ci_lo"] * (xb - centre_x),
           centre_y + b_b["ci_hi"] * (xb - centre_x), color=T.EMPIRE,
           alpha=0.15, zorder=1)
    axb.text(0.04, 0.92, f"β$_{{between}}$ = {b_b['median']:.2f} "
             f"[{b_b['ci_lo']:.2f}, {b_b['ci_hi']:.2f}]  (crosses 0)",
             transform=axb.transAxes, fontsize=7.5, va="top")
    axb.set_xlabel("province mean population (log)")
    axb.set_ylabel("province mean\ncount (log)")
    axb.set_title("(b) Between province — flat, uncertain", fontsize=9.0)

    fig.suptitle("Population–epigraphy scaling is within-province\n"
                 "(Latin frame, Roma excluded)", fontsize=9.5)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
