#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F1 — Deconvolution before/after (hero / explainer).
===================================================

The figure that sells the method (summary §1): the empire's *raw* aoristic
summed-probability curve — lumpy, with editorial-convention round-date slabs
spiking it — is deconvolved into a *genuine* smooth temporal distribution with a
95 % credible band.

Panels: one. Empire frame only (the all-provinces context unit).

Data
----
* Raw aoristic SPD + its convention (F1_round + F3_periodic) component,
  recomputed from the prereg-filtered LIRE corpus (``figdata``).
* Genuine SPD posterior draws (cross-classified production refit
  ``empire-aggregate-pgen.npz``: 8 000 draws × 80 bins).

Both curves are shown as per-year densities (area = 1) so the *shape* change is
directly comparable; the convention component is drawn on the raw curve's scale
so its height is its true contribution to the raw lumpiness.

Encoding: genuine = solid, saturated empire blue + translucent 95 % band; raw =
muted grey dashed; convention component = orange fill (the contamination the
method removes).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import figdata as D
import figtheme as T

UNIT = "empire-aggregate"
STEM = "fig01-deconvolution-before-after"


def build():
    """Assemble the F1 figure object."""
    x = D.years()

    # --- raw aoristic SPD + convention component (mass -> per-year density) ---
    raw_mass = D.raw_aoristic_mass(UNIT)
    conv_mass = D.convention_mass(UNIT)
    raw_total = float(raw_mass.sum())
    raw_dens = raw_mass / raw_total / D.BIN_SIZE        # area under raw = 1
    conv_dens = conv_mass / raw_total / D.BIN_SIZE      # convention's share of raw

    # --- genuine SPD draws -> 95 % band (already sum-1 -> per-year density) ---
    lo, med, hi = D.quantile_band(D.genuine_draws(UNIT))
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))

    fig, ax = T.figure_1col(height_ratio=0.74)

    # Convention contamination: orange fill on the raw scale.
    ax.fill_between(x, 0, conv_dens, color=T.OKABE_ITO["orange"], alpha=0.45,
                    linewidth=0, zorder=2,
                    label="editorial-convention component")
    # Raw aoristic curve: muted, dashed.
    ax.plot(x, raw_dens, color=T.NEUTRAL, linestyle="--", linewidth=1.2,
            alpha=0.9, zorder=3, label="raw aoristic (uncorrected)")

    # Genuine deconvolved SPD: empire blue, solid, with 95 % band.
    T.band(ax, x, lo, hi, color=T.EMPIRE, alpha=0.22, zorder=4,
           label="genuine 95 % credible band")
    ax.plot(x, med, color=T.EMPIRE, linewidth=1.8, zorder=5,
            label="genuine (deconvolved)")

    # Headroom above the tallest peak so the legend never collides with a curve.
    ax.set_ylim(0, float(hi.max()) * 1.30)
    ax.set_ylabel("probability density (per year)")
    T.year_axis(ax)
    ax.set_title("Deconvolving editorial convention from the empire SPD")
    ax.legend(loc="upper right", fontsize=7.2)

    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
