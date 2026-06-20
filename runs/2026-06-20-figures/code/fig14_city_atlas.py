#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F14 — Per-city corrected-SPD atlas (§5 hierarchical model).
===========================================================

A broad small-multiple chronology of individual cities — the 34 "reliable"
cities (those with at least ~300 inscriptions, the threshold at which the §5
trajectory model is dependable), far more than the five anchor cities of F4.
Each city's genuine summed-probability curve is its posterior inscription-rate
trajectory (λ[c,t]) from the §5 Layer-A hierarchical model, normalised to a
density, with a 95 % credible band. Cities are ordered by inscription count.

Like F13 (the province atlas), this uses the §5 trajectory model (which pools
and smooths across cities), a DIFFERENT correction from the cross-classified
deconvolution of F1–F4. The large anchor cities (Ostia, Pompeii, …) are held out
of this model and so do not appear here.

Data: ``monolithic-inscription-25y.nc`` (λ per city; gitignored, copied from
sapphire); ``layerb-residual-trajectories-empire.nc`` (per-city N + reliable
flag).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import arviz as az
import numpy as np
import xarray as xr

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
NC = ROOT / "runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc"
LAYERB = ROOT / "runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-empire.nc"
STEM = "fig14-city-atlas"
BIN_CENTRES = np.arange(-50, 350, 25) + 12.5  # 25-year grid centres
NCOL = 6


def _short(name: str) -> str:
    """Compact city label: drop the disambiguating parenthetical."""
    return name.split(" (")[0]


def build():
    post = az.from_netcdf(str(NC)).posterior
    cities = [str(c) for c in post["lam"].coords["city"].values]
    lam = post["lam"].stack(sample=("chain", "draw")).transpose(
        "sample", "city", "bin").values.astype(float)        # (S, C, T)

    # Per-city N + reliability (N >= 300) from the Layer-B file, mapped by name.
    lb = xr.open_dataset(LAYERB)
    lb_city = [str(c) for c in lb.coords["city"].values]
    N = dict(zip(lb_city, lb["N"].values))
    reliable = dict(zip(lb_city, lb["reliable"].values.astype(bool)))

    sel = [c for c in cities if reliable.get(c, False)]
    sel.sort(key=lambda c: -N[c])                            # by inscription count
    cidx = {c: i for i, c in enumerate(cities)}

    nrow = int(np.ceil(len(sel) / NCOL))
    fig, axes = T.figure_2col(height_ratio=1.12, nrows=nrow, ncols=NCOL,
                              sharex=True)
    flat = axes.flatten()

    for ax, city in zip(flat, sel):
        spd = lam[:, cidx[city], :]                          # (S, T)
        spd = spd / spd.sum(axis=1, keepdims=True) / 25.0    # per-year density
        lo, med, hi = np.percentile(spd, [2.5, 50, 97.5], axis=0)
        T.band(ax, BIN_CENTRES, lo, hi, color=T.LATIN, alpha=0.22)
        ax.plot(BIN_CENTRES, med, color=T.LATIN, lw=1.1)
        ax.set_ylim(bottom=0)
        ax.set_title(f"{_short(city)} ({int(N[city])})", fontsize=6.0, pad=2)
        ax.set_yticks([])
        ax.tick_params(labelsize=5.5)
        T.year_axis(ax, ticks=(0, 200), xlabel="")
    for ax in flat[len(sel):]:
        ax.set_visible(False)

    fig.suptitle("Per-city genuine-SPD atlas (§5 hierarchical model; "
                 "34 reliable cities, N in parentheses)", fontsize=9.0)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
