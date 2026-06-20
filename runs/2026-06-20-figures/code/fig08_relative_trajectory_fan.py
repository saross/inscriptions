#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F8 — Relative-trajectory fan (the reframed population question).
================================================================

The §5 residual Layer-B trajectories: each reliable city's inferred population
*relative to the empire-wide trend* (q_uv — the city-from-empire residual,
habit-removed), over time. The across-city median traces a rise to ~1.0 at the
Antonine peak (AD 188), a trough to ~0.32 around the Cyprianic period (AD 262),
and a partial late recovery — but cities are HETEROGENEOUS, not collapsing in
unison. A thin overlay shows the city-specific tier alone (q_v), whose AD 262
level (~0.78) is shallower: the late decline is largely provincial-tier (Obs 103).

**This is an illustrative relative SHAPE, not a population estimate** (Obs 96 /
103): the 1/β inversion amplifies, the anchors (Ostia, Pompeii) are held out of
this fit, and no absolute level is claimed. q = 1 means a city tracks the empire
trend.

Data: ``layerb-residual-trajectories-empire.nc`` (q_uv / q_v medians per city,
reliable subset, 25-year grid).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import xarray as xr

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
NC = ROOT / "runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-empire.nc"
STEM = "fig08-relative-trajectory-fan"


def build():
    ds = xr.open_dataset(NC)
    yr = ds.coords["bin_centre_year"].values
    rel = ds["reliable"].values.astype(bool)
    quv = ds["q_uv_med"].values[rel]          # (n_reliable, bin)
    qv = ds["q_v_med"].values[rel]
    n_rel = int(rel.sum())

    med = np.median(quv, axis=0)
    lo10, hi90 = np.percentile(quv, [10, 90], axis=0)
    lo25, hi75 = np.percentile(quv, [25, 75], axis=0)
    med_v = np.median(qv, axis=0)

    fig, ax = T.figure_1col(height_ratio=0.82)

    # Inter-city spread fans (10–90 and 25–75) — the heterogeneity, without the
    # cluttered per-city spaghetti.
    T.band(ax, yr, lo10, hi90, color=T.EMPIRE, alpha=0.14, zorder=2,
           label="inter-city 10–90 %")
    T.band(ax, yr, lo25, hi75, color=T.EMPIRE, alpha=0.22, zorder=3,
           label="inter-city 25–75 %")
    # Across-city median trajectory.
    ax.plot(yr, med, color=T.EMPIRE, lw=2.0, zorder=5,
            label="across-city median (city-from-empire)")
    # City-specific tier only (shallower late decline).
    ax.plot(yr, med_v, color=T.OKABE_ITO["purple"], lw=1.3, ls=(0, (4, 2)),
            zorder=4, label="city-specific tier only (q$_v$)")
    # Reference: on the empire trend.
    ax.axhline(1.0, color=T.NEUTRAL, lw=0.8, ls=":", zorder=1)
    ax.text(yr[-1], 1.0, "on empire trend ", fontsize=6.5, color=T.NEUTRAL,
            va="bottom", ha="right")

    # Narrative annotations (the anchors are held out, so annotate dates).
    ax.annotate("Antonine peak (AD 188)",
                xy=(187.5, med[np.argmin(np.abs(yr - 187.5))]),
                xytext=(-30, 1.40), fontsize=6.8, ha="left",
                arrowprops=dict(arrowstyle="->", lw=0.6, color=T.OKABE_ITO["black"]))
    ax.annotate("trough (AD 262)", xy=(262.5, med[np.argmin(np.abs(yr - 262.5))]),
                xytext=(300, 0.10), fontsize=6.8, ha="center", va="top",
                arrowprops=dict(arrowstyle="->", lw=0.6, color=T.OKABE_ITO["black"]))

    ax.set_ylim(0.0, 1.55)
    ax.set_xlim(yr[0] - 5, yr[-1] + 5)
    ax.set_ylabel("city population relative to empire trend (q)")
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.set_title("Illustrative relative shape — NOT a population estimate",
                 fontsize=8.8)
    ax.text(0.015, 0.97, f"reliable cities only (N $\\geq$ 300): {n_rel} of 268; "
            "anchors held out", transform=ax.transAxes, fontsize=6.0,
            color=T.NEUTRAL, va="top")
    # Legend below the axes (keeps the busy plot area clear).
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2,
              fontsize=6.5, columnspacing=1.2)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
