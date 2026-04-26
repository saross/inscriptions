#!/usr/bin/env python3
"""
post_run_v2.py --- v2 REPORT.md generator for h1_sim_v2 outputs.

Wraps the v1 post_run pipeline (power_curves, plots, thresholds) and
adds:

  - ``min_n_unreachable`` flag per (level, bracket, shape, null_model,
    cpl_k) cell that does not reach detection >= 0.80 at the maximum n
    in its level's sweep. Per Shawn's 2026-04-26 morning decision: keep
    c_20pc_25y in the v2 grid as a hard test, REPORT.md flags
    unreachable cells rather than imputing extrapolated thresholds.
  - "v2" tag in REPORT.md headers; comparison column to v1 thresholds
    where available.

Usage:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/post_run_v2.py \\
        --in runs/2026-04-25-h1-simulation/outputs/h1-v2 \\
        --out runs/2026-04-25-h1-simulation/outputs/h1-v2

The ``--in`` and ``--out`` are typically the same directory.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from plots import build_all_plots  # noqa: E402
from power_curves import (  # noqa: E402
    build_power_curves,
    extract_thresholds,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("post_run_v2")

# Maximum n per level (matches LEVEL_N_SWEEPS in h1_sim_v2.py).
LEVEL_MAX_N = {
    "empire": 50_000,
    "province": 25_000,
    "urban-area": 2_500,
}

DETECTION_TARGET = 0.80


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="in_dir", required=True,
                        type=Path, help="Input directory containing "
                        "cell-results.parquet.")
    parser.add_argument("--out", required=True, type=Path,
                        help="Output directory for REPORT-v2.md, plots, "
                        "and supplementary parquets.")
    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    parquet = in_dir / "cell-results.parquet"
    if not parquet.exists():
        logger.error("No cell-results.parquet at %s", parquet)
        return 2
    logger.info("Loading %s", parquet)
    cell = pd.read_parquet(parquet)
    logger.info("Loaded %d rows; %d unique cells",
                len(cell), cell["cell_id"].nunique())

    # ---- Power curves + thresholds (v1 pipeline, schema-compatible) -------
    logger.info("Building power curves...")
    curves = build_power_curves(cell)
    curves.to_parquet(out_dir / "power-curves.parquet")
    logger.info("Wrote %d power-curve rows", len(curves))

    logger.info("Extracting thresholds...")
    thresh = extract_thresholds(curves)
    thresh.to_parquet(out_dir / "thresholds.parquet")
    logger.info("Wrote %d threshold rows", len(thresh))

    # ---- min_n_unreachable flag --------------------------------------------
    # Per (level, bracket, shape, null_model, cpl_k), check whether the
    # power curve at level's max_n meets DETECTION_TARGET.
    flagged_rows: list[dict] = []
    group_cols = ["level", "bracket", "shape", "null_model", "cpl_k"]
    for keys, sub in curves.groupby(group_cols, sort=True, dropna=False):
        level, bracket, shape, null_model, cpl_k = keys
        if bracket == "zero":
            continue  # zero bracket is FP, not detection
        max_n = LEVEL_MAX_N.get(level, sub["n"].max())
        # Find the row at max_n.
        row_at_max = sub[sub["n"] == max_n]
        if len(row_at_max) == 0:
            continue
        rate_at_max = float(row_at_max.iloc[0]["detection_rate"])
        unreachable = rate_at_max < DETECTION_TARGET
        flagged_rows.append({
            "level": level,
            "bracket": bracket,
            "shape": shape,
            "null_model": null_model,
            "cpl_k": cpl_k,
            "max_n": max_n,
            "rate_at_max_n": rate_at_max,
            "min_n_unreachable": unreachable,
        })
    flag_df = pd.DataFrame(flagged_rows)
    flag_df.to_parquet(out_dir / "unreachable-flags.parquet")
    n_unreachable = int(flag_df["min_n_unreachable"].sum())
    logger.info("min_n_unreachable: %d / %d (level x bracket x shape x null x k) "
                "cells fail to reach detection >= %.2f at level's max n",
                n_unreachable, len(flag_df), DETECTION_TARGET)

    # ---- Plots --------------------------------------------------------------
    logger.info("Building plots...")
    build_all_plots(cell, curves, out_dir)
    logger.info("Plots written.")

    # ---- REPORT-v2.md -------------------------------------------------------
    lines: list[str] = []
    lines.append("# H1 v2 Simulation Report")
    lines.append("")
    lines.append("**Driver:** ``h1_sim_v2.py`` (forward-fit nulls in "
                 "true-date space; synthetic-from-null DGP)")
    lines.append("")
    lines.append("**Total iteration records:** "
                 f"{len(cell):,} rows across {cell['cell_id'].nunique()} cells")
    lines.append("")

    # 1. Headline thresholds.
    lines.append("## 1. Headline thresholds (detection >= 0.80, primary CPL k=3)")
    lines.append("")
    headline = thresh[
        (thresh["target"] == DETECTION_TARGET)
        & ((thresh["cpl_k"] == 3.0) | (thresh["cpl_k"] == -1.0))
    ].copy()

    bracket_order = {"a_50pc_50y": 0, "b_double_25y": 1,
                     "c_20pc_25y": 2, "zero": 3}
    level_order = {"empire": 0, "province": 1, "urban-area": 2}
    null_order = {"exponential": 0, "cpl": 1}
    shape_order = {"step": 0, "gaussian": 1}
    headline["_lvl"] = headline["level"].map(level_order)
    headline["_brk"] = headline["bracket"].map(bracket_order)
    headline["_shp"] = headline["shape"].map(shape_order)
    headline["_null"] = headline["null_model"].map(null_order)
    headline = headline.sort_values(
        ["_lvl", "_brk", "_null", "_shp"]
    ).drop(columns=["_lvl", "_brk", "_shp", "_null"])

    lines.append("| Level | Bracket | Null | Shape | min n (interp) | "
                 "obs min n | unreachable |")
    lines.append("|---|---|---|---|---|---|---|")
    for _, r in headline.iterrows():
        if r["bracket"] == "zero":
            continue
        # Look up unreachable flag.
        match = flag_df[
            (flag_df["level"] == r["level"])
            & (flag_df["bracket"] == r["bracket"])
            & (flag_df["shape"] == r["shape"])
            & (flag_df["null_model"] == r["null_model"])
            & (flag_df["cpl_k"] == r["cpl_k"])
        ]
        unreachable = (
            "**YES**" if len(match) > 0 and bool(match.iloc[0]["min_n_unreachable"])
            else "no"
        )
        min_n_str = (
            f"{int(round(r['min_n']))}" if not np.isnan(r["min_n"]) else "n/a"
        )
        obs_str = (
            f"{int(r['obs_min_n'])}" if r["obs_min_n"] != -1 else "n/a"
        )
        lines.append(
            f"| {r['level']} | {r['bracket']} | {r['null_model']} | "
            f"{r['shape']} | {min_n_str} | {obs_str} | {unreachable} |"
        )
    lines.append("")

    # 2. Unreachable cells summary.
    lines.append("## 2. Unreachable-cell flag summary")
    lines.append("")
    lines.append(
        "Per Shawn's 2026-04-26 morning decision: cells where detection "
        f"rate < {DETECTION_TARGET:.2f} at the level's maximum n are tagged "
        "``min_n_unreachable: True`` rather than extrapolated to a fictitious "
        "threshold. Tagged cells appear below."
    )
    lines.append("")
    if n_unreachable > 0:
        unreachable_df = flag_df[flag_df["min_n_unreachable"]].copy()
        unreachable_df["_lvl"] = unreachable_df["level"].map(level_order)
        unreachable_df["_brk"] = unreachable_df["bracket"].map(bracket_order)
        unreachable_df["_shp"] = unreachable_df["shape"].map(shape_order)
        unreachable_df["_null"] = unreachable_df["null_model"].map(null_order)
        unreachable_df = unreachable_df.sort_values(
            ["_lvl", "_brk", "_null", "_shp", "cpl_k"]
        )
        lines.append(
            "| Level | Bracket | Null | k | Shape | rate at max n | max n |"
        )
        lines.append("|---|---|---|---|---|---|---|")
        for _, r in unreachable_df.iterrows():
            k_str = "n/a" if r["cpl_k"] == -1 else f"k={int(r['cpl_k'])}"
            lines.append(
                f"| {r['level']} | {r['bracket']} | {r['null_model']} | "
                f"{k_str} | {r['shape']} | {r['rate_at_max_n']:.3f} | "
                f"{int(r['max_n'])} |"
            )
        lines.append("")
        lines.append(
            f"**{n_unreachable}** of {len(flag_df)} (level x bracket x shape x "
            f"null x k) detection cells are unreachable at the level's max n."
        )
    else:
        lines.append("All detection cells reach detection >= "
                     f"{DETECTION_TARGET:.2f} at their level's max n.")
    lines.append("")

    # 3. Zero-bracket FP rates.
    lines.append("## 3. Zero-bracket FP rates (target <= 0.05)")
    lines.append("")
    fp = curves[curves["bracket"] == "zero"].copy()
    fp["_lvl"] = fp["level"].map(level_order)
    fp["_null"] = fp["null_model"].map(null_order)
    fp["_shp"] = fp["shape"].map(shape_order)
    fp = fp.sort_values(["_lvl", "_null", "_shp", "cpl_k", "n"])
    lines.append("| Level | Null | Shape | cpl_k | n | FP rate |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in fp.iterrows():
        cpl_k_str = "n/a" if r["cpl_k"] == -1 else f"{int(r['cpl_k'])}"
        lines.append(
            f"| {r['level']} | {r['null_model']} | {r['shape']} | "
            f"{cpl_k_str} | {int(r['n'])} | {r['detection_rate']:.3f} |"
        )
    lines.append("")
    fp_max = fp["detection_rate"].max() if len(fp) > 0 else 0.0
    fp_min = fp["detection_rate"].min() if len(fp) > 0 else 0.0
    lines.append(
        f"FP rate range: [{fp_min:.3f}, {fp_max:.3f}]. "
        f"Cells > 0.05: {int((fp['detection_rate'] > 0.05).sum())} / {len(fp)}."
    )
    lines.append("")

    # 4. Exp vs CPL k=3 comparison.
    lines.append("## 4. Exponential vs CPL-3 threshold comparison")
    lines.append("")
    delta_rows: list[dict] = []
    for level in ("empire", "province", "urban-area"):
        for bracket in ("a_50pc_50y", "b_double_25y", "c_20pc_25y"):
            for shape in ("step", "gaussian"):
                exp_row = headline[
                    (headline["level"] == level)
                    & (headline["bracket"] == bracket)
                    & (headline["shape"] == shape)
                    & (headline["null_model"] == "exponential")
                ]
                cpl_row = headline[
                    (headline["level"] == level)
                    & (headline["bracket"] == bracket)
                    & (headline["shape"] == shape)
                    & (headline["null_model"] == "cpl")
                ]
                if len(exp_row) == 0 or len(cpl_row) == 0:
                    continue
                e = exp_row.iloc[0]["min_n"]
                c = cpl_row.iloc[0]["min_n"]
                if np.isnan(e) or np.isnan(c):
                    continue
                delta_rows.append({
                    "level": level, "bracket": bracket, "shape": shape,
                    "exp_n": e, "cpl_n": c,
                    "ratio": c / e if e > 0 else np.nan,
                })
    if delta_rows:
        lines.append("| Level | Bracket | Shape | exp n | cpl-3 n | "
                     "cpl/exp ratio |")
        lines.append("|---|---|---|---|---|---|")
        for r in delta_rows:
            lines.append(
                f"| {r['level']} | {r['bracket']} | {r['shape']} | "
                f"{int(round(r['exp_n']))} | {int(round(r['cpl_n']))} | "
                f"{r['ratio']:.2f} |"
            )
        ratios = [r["ratio"] for r in delta_rows if not np.isnan(r["ratio"])]
        if ratios:
            lines.append("")
            lines.append(
                f"Median cpl/exp ratio: {np.median(ratios):.2f}; "
                f"range [{min(ratios):.2f}, {max(ratios):.2f}]."
            )
    else:
        lines.append("No comparable cells (all unreachable in at least one null).")
    lines.append("")

    # 5. CPL k-sensitivity.
    # Per Decision 9, the primary cell grid drops k=2 (structurally
    # underfit on the LIRE 3-knot AIC-best truth). The k-sensitivity
    # narrows to k in {3, 4}: k=3 is the primary threshold-setting null;
    # k=4 is the exploratory upper bound.
    lines.append("## 5. CPL k-sensitivity (k in {3, 4} per Decision 9)")
    lines.append("")
    k_thresh = thresh[
        (thresh["target"] == DETECTION_TARGET)
        & (thresh["null_model"] == "cpl")
    ]
    k_summary: list[dict] = []
    for level in ("empire", "province", "urban-area"):
        for bracket in ("a_50pc_50y", "b_double_25y", "c_20pc_25y"):
            for shape in ("step", "gaussian"):
                sub = k_thresh[
                    (k_thresh["level"] == level)
                    & (k_thresh["bracket"] == bracket)
                    & (k_thresh["shape"] == shape)
                ]
                k_vals: dict[int, float] = {}
                for _, r in sub.iterrows():
                    k_vals[int(r["cpl_k"])] = r["min_n"]
                # Both k=3 and k=4 must be present and non-NaN to summarise.
                if all(k in k_vals for k in (3, 4)) and \
                   not any(np.isnan(k_vals[k]) for k in (3, 4)):
                    spread = max(k_vals[k] for k in (3, 4)) \
                        - min(k_vals[k] for k in (3, 4))
                    k_summary.append({
                        "key": f"{level}/{bracket}/{shape}",
                        "k3": int(round(k_vals[3])),
                        "k4": int(round(k_vals[4])),
                        "spread": int(round(spread)),
                    })
    if k_summary:
        lines.append("| Level/bracket/shape | k=3 | k=4 | spread |")
        lines.append("|---|---|---|---|")
        for r in k_summary[:30]:
            lines.append(
                f"| {r['key']} | {r['k3']} | {r['k4']} | {r['spread']} |"
            )
        if len(k_summary) > 30:
            lines.append(f"| ... ({len(k_summary) - 30} more cells) |  |  |  |")
    else:
        lines.append(
            "No reachable cells with both k=3 and k=4 thresholds; "
            "k-sensitivity table not constructible."
        )
    lines.append("")

    # AIC-best k distribution (computed from per-iteration cell parquet,
    # not from the threshold table).
    aic_best_lines: list[str] = []
    if "cpl_aic" in cell.columns and "cpl_k" in cell.columns:
        cpl_iter = cell[cell["null_model"] == "cpl"].copy()
        # For each (cell_id, iter), find which k has the lowest cpl_aic.
        if len(cpl_iter) > 0:
            cpl_iter["cpl_k"] = cpl_iter["cpl_k"].astype(int)
            best_per_iter = (
                cpl_iter.sort_values("cpl_aic")
                .groupby(["cell_id", "iter"])
                .first()
                .reset_index()
            )
            best_dist = (
                best_per_iter["cpl_k"].value_counts(normalize=True)
                .sort_index()
            )
            aic_best_lines.append("**AIC-best k distribution** "
                                  "(across all CPL iterations):")
            aic_best_lines.append("")
            aic_best_lines.append("| k | proportion |")
            aic_best_lines.append("|---|---|")
            for k_val, prop in best_dist.items():
                aic_best_lines.append(f"| {int(k_val)} | {prop:.3f} |")
    if aic_best_lines:
        lines.extend(aic_best_lines)
        lines.append("")

    # 6. Wall-time and convergence.
    lines.append("## 6. Execution diagnostics")
    lines.append("")
    if "wall_ms" in cell.columns:
        wall_total = cell["wall_ms"].sum() / 1000.0
        wall_med = cell["wall_ms"].median()
        wall_p95 = cell["wall_ms"].quantile(0.95)
        lines.append(
            f"- Total compute (serial-equivalent): "
            f"{wall_total / 60:.1f} min."
        )
        lines.append(
            f"- Per-iteration wall_ms: median {wall_med:.0f}, p95 {wall_p95:.0f}."
        )
    if "converged" in cell.columns:
        conv = cell["converged"].mean()
        lines.append(f"- Convergence rate: {conv:.3f} "
                     f"({int(cell['converged'].sum())} / {len(cell)}).")
    lines.append("")

    out_md = out_dir / "REPORT-v2.md"
    out_md.write_text("\n".join(lines))
    logger.info("Wrote %s (%d lines)", out_md, len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
