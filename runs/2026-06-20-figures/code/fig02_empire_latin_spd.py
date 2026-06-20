#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 — Empire + Latin SPD, corrected vs uncorrected, with uncertainty.
====================================================================

Two panels side by side: (a) the empire (all provinces, incl. Roma) and (b) the
Latin diagnostic frame (Latin-speaking provinces, Roma excluded). Each panel
overlays the raw aoristic SPD (uncorrected) against the deconvolved genuine SPD
with its 95 % credible band — the before/after of F1, shown for both frames so
the reader sees the correction is not an empire-only artefact.

Data: ``figdata`` raw aoristic + ``empire-aggregate`` / ``latin-aggregate``
genuine draws (cross-classified production refit). Densities (area = 1) on a
shared y-axis so the two frames are directly comparable.

Encoding: frame colour fixed (empire = blue, Latin = vermillion); genuine =
solid + 95 % band, raw = muted grey dashed.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import figdata as D
import figtheme as T

STEM = "fig02-empire-latin-spd"

PANELS = [
    ("empire-aggregate", T.EMPIRE, "(a) Empire (all provinces)"),
    ("latin-aggregate", T.LATIN, "(b) Latin provinces (Roma excluded)"),
]


def _draw_frame(ax, unit: str, colour: str, title: str) -> float:
    """One panel: raw (grey dashed) vs genuine (frame colour) + 95 % band.

    Returns the panel's peak density (for setting a common, untruncated y-limit).
    """
    x = D.years()

    raw_dens = D.normalise(D.raw_aoristic_mass(unit)) / D.BIN_SIZE
    lo, med, hi = D.quantile_band(D.genuine_draws(unit))
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))

    ax.plot(x, raw_dens, color=T.NEUTRAL, linestyle="--", linewidth=1.1,
            alpha=0.9, zorder=3, label="raw aoristic")
    T.band(ax, x, lo, hi, color=colour, alpha=0.22, zorder=4,
           label="genuine 95 % band")
    ax.plot(x, med, color=colour, linewidth=1.7, zorder=5, label="genuine")

    T.year_axis(ax)
    ax.set_title(title, fontsize=9.0)
    ax.legend(loc="upper right", fontsize=7.0)
    return max(float(raw_dens.max()), float(hi.max()))


def build():
    """Assemble the F2 two-panel figure."""
    fig, axes = T.figure_2col(height_ratio=0.42, ncols=2, sharey=True)
    peaks = [_draw_frame(ax, unit, colour, title)
             for ax, (unit, colour, title) in zip(axes, PANELS)]
    # One shared, untruncated y-limit with headroom (sharey -> set once).
    axes[0].set_ylim(0, max(peaks) * 1.15)
    axes[0].set_ylabel("probability density (per year)")
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
