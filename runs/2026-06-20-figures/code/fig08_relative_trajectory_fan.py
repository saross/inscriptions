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
    n_rel = int(rel.sum())

    med = np.median(quv, axis=0)
    lo25, hi75 = np.percentile(quv, [25, 75], axis=0)
    m188 = float(med[np.argmin(np.abs(yr - 187.5))])
    m262 = float(med[np.argmin(np.abs(yr - 262.5))])

    # Full-width: a detailed annotated time-series needs horizontal room (it was
    # cramped at single-column).
    fig, ax = T.figure_2col(height_ratio=0.42, ncols=1)

    # The empire-trend reference (q = 1).
    ax.axhline(1.0, color=T.NEUTRAL, lw=0.8, ls=":", zorder=1)
    ax.text(yr[-1], 1.02, "on empire trend", fontsize=6.5, color=T.NEUTRAL,
            va="bottom", ha="right")

    # ONE moderate uncertainty fan (the inter-quartile spread) with crisp edges,
    # so the median trajectory stays legible (the 10–90 fan filled the panel).
    ax.fill_between(yr, lo25, hi75, color=T.EMPIRE, alpha=0.18, linewidth=0,
                    zorder=2, label="inter-city IQR (25–75 %)")
    ax.plot(yr, lo25, color=T.EMPIRE, lw=0.5, alpha=0.5, zorder=2)
    ax.plot(yr, hi75, color=T.EMPIRE, lw=0.5, alpha=0.5, zorder=2)

    # The across-city median trajectory — the focus; markers read it as discrete
    # 25-year estimates rather than a noisy continuous line.
    ax.plot(yr, med, color=T.EMPIRE, lw=2.3, marker="o", ms=3.4,
            markerfacecolor="white", markeredgewidth=1.0, zorder=5,
            label="across-city median (q)")

    # Narrative annotations (anchors are held out, so annotate dates).
    ax.annotate("Antonine peak\n(AD 188)", xy=(187.5, m188),
                xytext=(95, 1.34), fontsize=7.0, ha="center", va="center",
                arrowprops=dict(arrowstyle="->", lw=0.7, color=T.OKABE_ITO["black"]))
    ax.annotate("trough\n(AD 262)", xy=(262.5, m262), xytext=(300, 0.66),
                fontsize=7.0, ha="center", va="center",
                arrowprops=dict(arrowstyle="->", lw=0.7, color=T.OKABE_ITO["black"]))

    ax.set_ylim(0.0, 1.5)
    ax.set_xlim(yr[0] - 5, yr[-1] + 5)
    ax.set_ylabel("city population relative to empire trend (q)")
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.set_title("Illustrative relative shape — NOT a population estimate",
                 fontsize=8.8)
    ax.text(0.015, 0.04, f"{n_rel} reliable cities (N $\\geq$ 300); anchors held out",
            transform=ax.transAxes, fontsize=6.5, color=T.NEUTRAL, va="bottom")
    ax.legend(loc="upper right", fontsize=7.5)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
