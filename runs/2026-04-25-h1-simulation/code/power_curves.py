#!/usr/bin/env python3
"""
power_curves.py --- Detection-rate curve builder and threshold extractor.

Consumes the per-iteration parquet produced by ``h1_sim.py`` (schema per
decisions.md §8) and produces:

    build_power_curves(cell_summary) -> pandas.DataFrame
        One row per (level, bracket, shape, null_model, cpl_k, n) with
        detection rate, binomial standard error, and Wilson 95 % CI.

    extract_thresholds(power_curves, targets=(0.70, 0.80, 0.90))
        One row per (level, bracket, shape, null_model, cpl_k, target)
        reporting the minimum n at which detection rate >= target (with
        linear interpolation across n-grid points for non-empire levels).

Primary reporting column (decisions.md §3): ``cpl_k == 3`` for CPL cells.
Exploratory analyses (k-sensitivity, AIC-select) use all k in {2, 3, 4}.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)

GROUP_KEYS = ["level", "bracket", "shape", "null_model", "cpl_k", "n"]


def _wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    z = stats.norm.ppf(1.0 - alpha / 2.0)
    p = k / n
    denom = 1.0 + z ** 2 / n
    centre = (p + z ** 2 / (2.0 * n)) / denom
    half = z * np.sqrt(p * (1.0 - p) / n + z ** 2 / (4.0 * n ** 2)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def build_power_curves(cell_results: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-iteration results into per-cell detection rates.

    Parameters
    ----------
    cell_results : pandas.DataFrame
        Per-iteration parquet (Decision 8 schema).

    Returns
    -------
    pandas.DataFrame
        Columns: level, bracket, shape, null_model, cpl_k, n, n_iter,
        n_detected, detection_rate, ci_lo, ci_hi, wall_ms_mean.
    """
    # NaN cpl_k (exponential cells) needs a placeholder for grouping.
    df = cell_results.copy()
    df["cpl_k"] = df["cpl_k"].fillna(-1)  # -1 sentinel for "not applicable"

    grouped = df.groupby(GROUP_KEYS, sort=True, dropna=False)

    rows: list[dict] = []
    for (level, bracket, shape, null_model, cpl_k, n), sub in grouped:
        n_iter = len(sub)
        n_det = int(sub["detected"].sum())
        rate = n_det / n_iter if n_iter else float("nan")
        ci_lo, ci_hi = _wilson_ci(n_det, n_iter)
        rows.append({
            "level": level,
            "bracket": bracket,
            "shape": shape,
            "null_model": null_model,
            "cpl_k": cpl_k,
            "n": n,
            "n_iter": n_iter,
            "n_detected": n_det,
            "detection_rate": rate,
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
            "wall_ms_mean": float(sub["wall_ms"].mean()),
        })
    return pd.DataFrame(rows)


def _interpolate_threshold(
    ns: np.ndarray, rates: np.ndarray, target: float,
) -> float:
    """Linearly interpolate the minimum n at which rate >= target.

    Parameters
    ----------
    ns : numpy.ndarray
        Monotone-ascending n values.
    rates : numpy.ndarray
        Detection rates aligned with ``ns``.
    target : float
        Target detection rate (e.g. 0.80).

    Returns
    -------
    float
        Interpolated n. Returns ``NaN`` if no cell reaches the target;
        returns ``ns[0]`` if the smallest-n cell already meets target.
    """
    if len(ns) == 0:
        return float("nan")
    order = np.argsort(ns)
    ns_sorted = np.asarray(ns)[order]
    rates_sorted = np.asarray(rates)[order]

    # If even the largest n doesn't reach target --> threshold not reachable.
    if np.all(rates_sorted < target):
        return float("nan")
    # If smallest n already meets target --> return it.
    if rates_sorted[0] >= target:
        return float(ns_sorted[0])

    # Find first index where rate >= target.
    i = int(np.argmax(rates_sorted >= target))
    # Linear interp between (ns[i-1], rates[i-1]) and (ns[i], rates[i]).
    n0, n1 = ns_sorted[i - 1], ns_sorted[i]
    r0, r1 = rates_sorted[i - 1], rates_sorted[i]
    if r1 == r0:
        return float(n1)
    return float(n0 + (target - r0) * (n1 - n0) / (r1 - r0))


def extract_thresholds(
    power_curves: pd.DataFrame,
    targets: tuple[float, ...] = (0.70, 0.80, 0.90),
) -> pd.DataFrame:
    """Extract minimum-n thresholds per (level, bracket, shape, null_model, cpl_k).

    Parameters
    ----------
    power_curves : pandas.DataFrame
        Output of ``build_power_curves``.
    targets : tuple of float, default (0.70, 0.80, 0.90)
        Target detection rates.

    Returns
    -------
    pandas.DataFrame
        One row per (level, bracket, shape, null_model, cpl_k, target)
        with interpolated ``min_n`` and nearest observed ``obs_min_n``.
    """
    out: list[dict] = []
    group_cols = ["level", "bracket", "shape", "null_model", "cpl_k"]
    for keys, sub in power_curves.groupby(group_cols, sort=True, dropna=False):
        ns = sub["n"].to_numpy()
        rates = sub["detection_rate"].to_numpy()
        level, bracket, shape, null_model, cpl_k = keys
        for target in targets:
            interp = _interpolate_threshold(ns, rates, target)
            # Nearest observed n meeting target.
            meets = sub.loc[sub["detection_rate"] >= target, "n"]
            obs_min = int(meets.min()) if not meets.empty else -1
            out.append({
                "level": level,
                "bracket": bracket,
                "shape": shape,
                "null_model": null_model,
                "cpl_k": cpl_k,
                "target": target,
                "min_n": interp,
                "obs_min_n": obs_min,
            })
    return pd.DataFrame(out)
