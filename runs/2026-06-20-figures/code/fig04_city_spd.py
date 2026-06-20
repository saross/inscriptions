#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F4 — City-level SPD, corrected vs uncorrected, with uncertainty.
================================================================

The five independently-anchored cities used to validate the deconvolution:
Pompeii (buried AD 79), Ostia (2nd-century apogee), Salona, Aquileia, and
Mogontiacum. Each shows the raw aoristic SPD against the deconvolved genuine SPD
+ 95 % band. Pompeii is the external check — genuine mass after the AD 79
eruption (dotted line) should collapse to ~0, which it does.

(Small-N city *trajectories* are the §5 hierarchical model — see the F13 atlas;
F4 is the data-rich anchor cities fitted standalone in the deconvolution refit.)

Data: ``figdata`` raw aoristic + per-city genuine draws (cc production refit).
Encoding: Latin frame -> vermillion genuine + band; raw = grey dashed.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import figdata as D
import figtheme as T

STEM = "fig04-city-spd"

CITIES = ["Pompeii", "Ostia", "Salona", "Aquileia", "Mogontiacum"]
POMPEII_ERUPTION = 79  # AD; the external validation terminus.


def _draw(ax, name: str) -> None:
    """One city panel: raw (grey dashed) vs genuine (vermillion) + band."""
    x = D.years()
    n_rows = D.unit_n_rows(name)

    raw_dens = D.normalise(D.raw_aoristic_mass(name)) / D.BIN_SIZE
    lo, med, hi = D.quantile_band(D.genuine_draws(name))
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))

    ax.plot(x, raw_dens, color=T.NEUTRAL, linestyle="--", linewidth=1.0,
            alpha=0.9, zorder=3)
    T.band(ax, x, lo, hi, color=T.LATIN, alpha=0.22, zorder=4)
    ax.plot(x, med, color=T.LATIN, linewidth=1.5, zorder=5)

    # Pompeii: mark the AD 79 eruption (the external validation terminus).
    if name == "Pompeii":
        ax.axvline(POMPEII_ERUPTION, color=T.OKABE_ITO["black"], lw=0.8,
                   ls=":", zorder=6)
        ax.annotate("AD 79", xy=(POMPEII_ERUPTION, ax.get_ylim()[1]),
                    xytext=(POMPEII_ERUPTION + 8, 0.92), textcoords=("data",
                    "axes fraction"), fontsize=6.5, va="top")

    ax.set_ylim(0, float(hi.max()) * 1.18)
    ax.set_title(f"{name}  (N = {n_rows:,})", fontsize=8.0)
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.tick_params(labelsize=7)


def build():
    """Assemble the F4 2×3 small-multiple (5 cities + a hidden 6th cell)."""
    fig, axes = T.figure_2col(height_ratio=0.62, nrows=2, ncols=3, sharex=True)
    flat = axes.flatten()
    for ax, name in zip(flat, CITIES):
        _draw(ax, name)
    flat[5].set_visible(False)  # only five anchor cities
    # Salona (top-right) sits above the hidden cell, so restore its x-labels.
    flat[2].tick_params(labelbottom=True)
    flat[2].set_xlabel("Year")

    for ax in axes[:, 0]:
        ax.set_ylabel("density (per yr)", fontsize=7.5)
    for ax in flat[:3]:
        ax.set_xlabel("")

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color=T.NEUTRAL, ls="--", lw=1.0, label="raw aoristic"),
        Line2D([0], [0], color=T.LATIN, lw=1.5, label="genuine (+ 95 % band)"),
    ]
    fig.legend(handles=handles, loc="lower right", ncol=1, fontsize=7.5,
               bbox_to_anchor=(0.92, 0.12))
    fig.suptitle("Anchor-city deconvolution (Pompeii = AD 79 external check)",
                 fontsize=9.5)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
