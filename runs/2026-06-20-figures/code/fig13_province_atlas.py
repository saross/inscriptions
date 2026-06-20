#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F13 — Per-province corrected-SPD atlas (§5 hierarchical model).
===============================================================

A small-multiple chronology of the provinces, from the §5 Layer-A hierarchical
trajectory model (the monolithic 25-year inscription fit). Each province's
genuine summed-probability curve is the posterior aggregate of its cities'
smoothed inscription-rate trajectories (Σ_c λ[c,t]), normalised to a density,
with a 95 % credible band. Provinces with at least four §5 cities are shown
(25 provinces, ordered by city count); the model holds out the large anchor
cities, so this is the small-N-city view of each province's chronology.

NOTE: this is the §5 *trajectory* model (smoothed genuine intensity), a DIFFERENT
correction from the cross-classified deconvolution of F1–F4 (which removes
editorial convention). The two are complementary province views.

Data: ``runs/2026-05-30-s5-small-n-trajectories/code/production/
monolithic-inscription-25y.nc`` (gitignored; copied from sapphire) +
``prepared/city-index.parquet`` (city→province).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
NC = ROOT / "runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc"
CITY_INDEX = ROOT / "runs/2026-05-30-s5-small-n-trajectories/code/prepared/city-index.parquet"
STEM = "fig13-province-atlas"
MIN_CITIES = 4
BIN_CENTRES = np.arange(-50, 350, 25) + 12.5  # 25-year grid centres


def _short(name: str) -> str:
    return name.split(" / ")[0]


def build():
    post = az.from_netcdf(str(NC)).posterior
    cities = [str(c) for c in post["lam"].coords["city"].values]
    lam = post["lam"].stack(sample=("chain", "draw")).transpose(
        "sample", "city", "bin").values.astype(float)        # (S, C, T)

    idx = pd.read_parquet(CITY_INDEX).set_index("province")
    city_prov = pd.read_parquet(CITY_INDEX).set_index("city")["province"]
    prov_of = np.array([city_prov[c] for c in cities])

    counts = pd.Series(prov_of).value_counts()
    provinces = [p for p in counts.index if counts[p] >= MIN_CITIES]  # ordered by N

    # Per-province genuine SPD: sum cities' lam, normalise per draw, quantile.
    panels = []
    for p in provinces:
        sel = prov_of == p
        spd = lam[:, sel, :].sum(axis=1)                     # (S, T)
        spd = spd / spd.sum(axis=1, keepdims=True) / 25.0    # per-year density
        lo, med, hi = np.percentile(spd, [2.5, 50, 97.5], axis=0)
        panels.append((p, int(sel.sum()), lo, med, hi))

    ncol = 5
    nrow = int(np.ceil(len(panels) / ncol))
    fig, axes = T.figure_2col(height_ratio=0.95, nrows=nrow, ncols=ncol,
                              sharex=True)
    flat = axes.flatten()

    for ax, (p, n, lo, med, hi) in zip(flat, panels):
        T.band(ax, BIN_CENTRES, lo, hi, color=T.LATIN, alpha=0.22)
        ax.plot(BIN_CENTRES, med, color=T.LATIN, lw=1.2)
        ax.set_ylim(bottom=0)
        ax.set_title(f"{_short(p)} ({n})", fontsize=6.3, pad=2)
        ax.tick_params(labelsize=6)
        ax.set_yticks([])
        T.year_axis(ax, ticks=(0, 200), xlabel="")
    for ax in flat[len(panels):]:
        ax.set_visible(False)

    fig.suptitle("Per-province genuine-SPD atlas (§5 hierarchical model; "
                 "n cities in parentheses)", fontsize=9.0)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
