#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F12 — Reachability map (the instrument's operating envelope).
=============================================================

How well the deconvolution recovers the genuine shape as a function of corpus
size N and the true convention fraction α — the method's "spec sheet". Each cell
is shaded by the recovery rate (fraction of replicates meeting the coverage +
shape-correlation criteria, averaged over test shapes); a tick (✓) marks cells
that pass the formal reachability gate. Recovery improves with N and degrades as
α rises: the reliable operating envelope is roughly N ≳ 500 (easy subsets) to
N ≈ 2 000 (hard), with α ≲ 0.70.

Data: ``runs/2026-06-03-small-n-reachability/outputs/reachability-by-cell.csv``
(N × α grid over several synthetic test shapes).

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
CSV = ROOT / "runs/2026-06-03-small-n-reachability/outputs/reachability-by-cell.csv"
STEM = "fig12-reachability-map"


def build():
    df = pd.read_csv(CSV)
    # Aggregate over test shapes per (alpha, N): mean recovery rate + pass frac.
    grp = df.groupby(["alpha_true", "n"]).agg(
        shape_rate=("shape_rate", "mean"),
        pass_frac=("cell_pass", "mean")).reset_index()
    rate = grp.pivot(index="alpha_true", columns="n", values="shape_rate")
    passf = grp.pivot(index="alpha_true", columns="n", values="pass_frac")
    rate = rate.sort_index(ascending=False)        # high α at top
    passf = passf.reindex(rate.index)

    alphas = list(rate.index)
    ns = list(rate.columns)

    fig, ax = T.figure_1col(height_ratio=0.78)
    im = ax.imshow(rate.values, aspect="auto", cmap=T.SEQ_CMAP_CVD,
                   vmin=0, vmax=1, origin="upper")

    # Mark gate-passing cells with font-safe markers: filled = all test shapes
    # pass (reliable), open = some pass (marginal).
    rel_x, rel_y, marg_x, marg_y = [], [], [], []
    for i in range(len(alphas)):
        for j in range(len(ns)):
            pf = passf.values[i, j]
            if pf >= 0.999:
                rel_x.append(j); rel_y.append(i)
            elif pf > 0:
                marg_x.append(j); marg_y.append(i)
    ax.scatter(rel_x, rel_y, s=55, marker="o", facecolor="white",
               edgecolor="black", linewidths=0.8, zorder=5, label="reliable")
    ax.scatter(marg_x, marg_y, s=45, marker="o", facecolor="none",
               edgecolor="white", linewidths=1.3, zorder=5, label="marginal")

    ax.set_xticks(range(len(ns)))
    ax.set_xticklabels([f"{n:,}" for n in ns], fontsize=7.5)
    ax.set_yticks(range(len(alphas)))
    ax.set_yticklabels([f"{a:.2f}" for a in alphas], fontsize=7.5)
    ax.set_xlabel("corpus size N")
    ax.set_ylabel("true convention fraction α")
    ax.set_title("Reachability: shape recovery over N × α", fontsize=9.0)
    ax.legend(loc="upper left", fontsize=6.8, framealpha=0.9,
              facecolor="white")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("shape-recovery rate", fontsize=7.5)
    cbar.ax.tick_params(labelsize=7)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
