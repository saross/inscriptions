#!/usr/bin/env python3
"""
plots.py --- Matplotlib (Agg-backend) figure generation for H1 simulation.

Two figure families:

  1. Power curves per (level x bracket x null_model x shape x cpl_k):
     detection rate vs n with 0.70 / 0.80 / 0.90 target gridlines and
     Wilson 95 % CI ribbons.

  2. Heatmaps per (level x null_model x shape): detection-rate matrix
     over (bracket, n) with the 0.80 contour highlighted.

Each figure ships alongside a parquet of the plotted data to support
reuse in REPORT.md without rerunning the simulation.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, must be set before pyplot import

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

logger = logging.getLogger(__name__)

TARGETS = (0.70, 0.80, 0.90)
BRACKET_ORDER = ("c_20pc_25y", "a_50pc_50y", "b_double_25y", "zero")


def _plot_power_curve(
    sub: pd.DataFrame,
    title: str,
    png_path: Path,
    parquet_path: Path,
) -> None:
    """Plot detection rate vs n for a single (level, bracket, shape,
    null_model, cpl_k) slice."""
    sub = sub.sort_values("n").reset_index(drop=True)
    sub.to_parquet(parquet_path, index=False)

    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(sub["n"], sub["detection_rate"], marker="o",
            color="tab:blue", label="detection rate")
    ax.fill_between(sub["n"], sub["ci_lo"], sub["ci_hi"],
                    alpha=0.2, color="tab:blue", label="Wilson 95 % CI")
    for t in TARGETS:
        ax.axhline(t, linestyle="--", linewidth=0.8, color="gray", alpha=0.6)
        ax.text(sub["n"].max(), t, f" {t:.2f}", va="center",
                ha="left", fontsize=8, color="gray")
    ax.set_xscale("log")
    ax.set_xlabel("n (sample size)")
    ax.set_ylabel("detection rate")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title(title, fontsize=10)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)


def _plot_heatmap(
    sub: pd.DataFrame,
    title: str,
    png_path: Path,
    parquet_path: Path,
) -> None:
    """Heatmap: bracket x n detection-rate with 0.80 contour."""
    pivot = sub.pivot_table(
        index="bracket", columns="n",
        values="detection_rate", aggfunc="mean",
    )
    # Enforce deterministic row order.
    ordered_brackets = [b for b in BRACKET_ORDER if b in pivot.index]
    pivot = pivot.loc[ordered_brackets]
    pivot.to_parquet(parquet_path)

    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    data = pivot.to_numpy(dtype=float)
    im = ax.imshow(
        data, aspect="auto", origin="lower",
        cmap="viridis", vmin=0.0, vmax=1.0,
    )
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=8)
    ax.set_xlabel("n")
    ax.set_ylabel("bracket")
    ax.set_title(title, fontsize=10)
    fig.colorbar(im, ax=ax, label="detection rate")

    # 0.80 contour. Matplotlib requires at least a (2, 2) array; skip
    # when the grid is degenerate (e.g. empire with one n, or a single
    # bracket in a narrowed dataset).
    if data.shape[0] >= 2 and data.shape[1] >= 2:
        try:
            ax.contour(
                np.arange(data.shape[1]),
                np.arange(data.shape[0]),
                data,
                levels=[0.80],
                colors="white", linewidths=1.2,
            )
        except ValueError:
            logger.debug("Contour skipped for %s (insufficient variation)", title)

    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)


def build_all_plots(
    cell_results: pd.DataFrame,
    power_curves: pd.DataFrame,
    out_dir: Path,
) -> None:
    """Drive both plot families; write PNGs and per-plot parquet to ``out_dir``.

    Parameters
    ----------
    cell_results : pandas.DataFrame
        Raw per-iteration parquet (unused today but passed through for
        future plotters that might need e.g. iteration-level residual
        distributions).
    power_curves : pandas.DataFrame
        Output of ``power_curves.build_power_curves``.
    out_dir : pathlib.Path
        Output root; subdirs ``power-curves/`` and ``heatmaps/`` are created.
    """
    curve_dir = out_dir / "power-curves"
    heat_dir = out_dir / "heatmaps"
    curve_dir.mkdir(parents=True, exist_ok=True)
    heat_dir.mkdir(parents=True, exist_ok=True)

    # ---- Power curves --------------------------------------------------
    curve_keys = ["level", "bracket", "shape", "null_model", "cpl_k"]
    for keys, sub in power_curves.groupby(curve_keys, sort=True, dropna=False):
        level, bracket, shape, null_model, cpl_k = keys
        k_tag = "" if cpl_k == -1 else f"_k{int(cpl_k)}"
        slug = f"{level}_{bracket}_{shape}_{null_model}{k_tag}"
        png = curve_dir / f"{slug}.png"
        pq = curve_dir / f"{slug}.parquet"
        title = (
            f"{level} / {bracket} / {shape} / {null_model}"
            + (f" (k={int(cpl_k)})" if cpl_k != -1 else "")
        )
        _plot_power_curve(sub, title, png, pq)
    logger.info("Power curves written to %s", curve_dir)

    # ---- Heatmaps ------------------------------------------------------
    heat_keys = ["level", "null_model", "shape", "cpl_k"]
    for keys, sub in power_curves.groupby(heat_keys, sort=True, dropna=False):
        level, null_model, shape, cpl_k = keys
        k_tag = "" if cpl_k == -1 else f"_k{int(cpl_k)}"
        slug = f"{level}_{null_model}_{shape}{k_tag}"
        png = heat_dir / f"{slug}.png"
        pq = heat_dir / f"{slug}.parquet"
        title = (
            f"{level} / {null_model} / {shape}"
            + (f" (k={int(cpl_k)})" if cpl_k != -1 else "")
        )
        _plot_heatmap(sub, title, png, pq)
    logger.info("Heatmaps written to %s", heat_dir)
