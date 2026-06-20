#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F3 — Province-level SPD, corrected vs uncorrected, with uncertainty.
====================================================================

A small-multiple of six informative Latin provinces spanning the empire — the
Italian core, Iberia, Africa, the Balkans, and two frontier provinces (one of
them a caveated low-N case, shown honestly) — each with its raw aoristic SPD
(uncorrected) against the deconvolved genuine SPD and 95 % band. Shows the
correction is province-general, not an aggregate artefact, and that the
frontier/low-N units carry visibly wider uncertainty.

(The FULL per-province chronology is the F13 atlas; F3 is the curated, legible
before/after subset.)

Data: ``figdata`` raw aoristic + per-province genuine draws (cc production
refit). Per-panel densities (area = 1) so each province's shape reads clearly
regardless of corpus size; panel titles carry the province row count N.

Encoding: Latin frame -> vermillion genuine + band; raw = grey dashed.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import figdata as D
import figtheme as T

STEM = "fig03-province-spd"

# Curated subset (all have genuine draws; core -> frontier; last is caveated).
PROVINCES = [
    "Latium et Campania / Regio I",   # Italian core (highest N)
    "Hispania citerior",              # Iberia
    "Africa proconsularis",           # Africa
    "Dalmatia",                       # Balkans / Adriatic
    "Germania superior",              # Rhine frontier
    "Britannia",                      # NW frontier (caveated, low N)
]
CAVEATED = {"Britannia"}


def _short(name: str) -> str:
    """Drop the Italian regio suffix for a compact panel title."""
    return name.split(" / ")[0]


def _draw(ax, name: str) -> None:
    """One province panel: raw (grey dashed) vs genuine (vermillion) + band."""
    x = D.years()
    n_rows = D.unit_n_rows(name)

    raw_dens = D.normalise(D.raw_aoristic_mass(name)) / D.BIN_SIZE
    lo, med, hi = D.quantile_band(D.genuine_draws(name))
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))

    ax.plot(x, raw_dens, color=T.NEUTRAL, linestyle="--", linewidth=1.0,
            alpha=0.9, zorder=3)
    T.band(ax, x, lo, hi, color=T.LATIN, alpha=0.22, zorder=4)
    ax.plot(x, med, color=T.LATIN, linewidth=1.5, zorder=5)

    ax.set_ylim(0, float(hi.max()) * 1.18)
    title = _short(name) + (" *" if name in CAVEATED else "")
    ax.set_title(f"{title}  (N = {n_rows:,})", fontsize=8.0)
    # Sparser ticks so labels don't collide on the narrow small-multiple panels.
    T.year_axis(ax, ticks=(0, 100, 200, 300))
    ax.tick_params(labelsize=7)


def build():
    """Assemble the F3 2×3 small-multiple."""
    fig, axes = T.figure_2col(height_ratio=0.62, nrows=2, ncols=3, sharex=True)
    flat = axes.flatten()
    for ax, name in zip(flat, PROVINCES):
        _draw(ax, name)
    # Shared y-label on the left column; x-label on the bottom row only.
    for ax in axes[:, 0]:
        ax.set_ylabel("density (per yr)", fontsize=7.5)
    for ax in flat[:3]:
        ax.set_xlabel("")

    # Figure-level legend (raw vs genuine) + the caveat note.
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color=T.NEUTRAL, ls="--", lw=1.0, label="raw aoristic"),
        Line2D([0], [0], color=T.LATIN, lw=1.5, label="genuine (+ 95 % band)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=7.5,
               bbox_to_anchor=(0.5, -0.03))
    fig.suptitle("Province-level deconvolution (* = caveated, low N)",
                 fontsize=9.5)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
