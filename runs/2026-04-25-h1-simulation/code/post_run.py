#!/usr/bin/env python3
"""
post_run.py --- Generate REPORT.md from simulation outputs.

Reads cell-results.parquet, power-curves.parquet, thresholds.parquet
(written by --mode=report), computes CPL fallback fractions, FP rates,
and writes a Markdown report.

Usage:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/post_run.py \\
        --out runs/2026-04-25-h1-simulation/outputs
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out = Path(args.out)
    cell = pd.read_parquet(out / "cell-results.parquet")
    curves = pd.read_parquet(out / "power-curves.parquet")
    thresh = pd.read_parquet(out / "thresholds.parquet")

    # ---- Compute CPL fallback fraction per cell ----------------------------
    cpl = cell[cell["null_model"] == "cpl"].copy()
    fallback = (
        cpl.groupby(["cell_id", "level", "bracket", "shape", "n", "cpl_k"])
        .agg(n_iter=("iter", "count"),
             n_fallback=("cpl_aic", lambda s: int(s.isna().sum())))
        .reset_index()
    )
    fallback["fallback_frac"] = fallback["n_fallback"] / fallback["n_iter"]
    flagged = fallback[fallback["fallback_frac"] > 0.20].copy()

    # ---- FP rate (zero bracket) -------------------------------------------
    fp = curves[curves["bracket"] == "zero"].copy()

    # ---- Headline thresholds (detection >= 0.80 only, primary cpl_k=3) -----
    headline = thresh[
        (thresh["target"] == 0.80)
        & ((thresh["cpl_k"] == 3.0) | (thresh["cpl_k"] == -1.0))
    ].copy()

    # Sort
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

    # ---- Build REPORT.md ---------------------------------------------------
    lines: list[str] = []
    lines.append("# H1 Simulation Report")
    lines.append("")
    lines.append("**Run:** 2026-04-25 (commit 982fec9)")
    lines.append("")
    lines.append("**Total iteration records:** "
                 f"{len(cell):,} rows across {cell['cell_id'].nunique()} cells")
    lines.append("")
    lines.append(
        "**Schema (Decision 8 of decisions.md):** "
        "exponential cells emit 1 row/iter; CPL cells emit 3 rows/iter (one per k in {2, 3, 4})."
    )
    lines.append("")

    # 1. Headline thresholds.
    lines.append("## 1. Headline recommended thresholds (detection >= 0.80)")
    lines.append("")
    lines.append("Primary CPL k = 3. NaN min_n means the largest n in the sweep does not reach the target detection rate; check power curves for that cell.")
    lines.append("")
    lines.append("| Level | Bracket | Null | Shape | min n (interp) | obs min n |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in headline.iterrows():
        if r["bracket"] == "zero":
            continue  # zero bracket goes in FP table
        min_n_str = (
            f"{int(round(r['min_n']))}" if not np.isnan(r["min_n"]) else "n/a"
        )
        obs_str = (
            f"{int(r['obs_min_n'])}" if r["obs_min_n"] != -1 else "n/a"
        )
        lines.append(
            f"| {r['level']} | {r['bracket']} | {r['null_model']} | "
            f"{r['shape']} | {min_n_str} | {obs_str} |"
        )
    lines.append("")

    # Range summary [n_sharp, n_smooth] per (level x bracket x null).
    lines.append("### Range per (level x bracket x null) — [step, gaussian] thresholds")
    lines.append("")
    lines.append("| Level | Bracket | Null | n_sharp (step) | n_smooth (gaussian) |")
    lines.append("|---|---|---|---|---|")
    for level in ("empire", "province", "urban-area"):
        for bracket in ("a_50pc_50y", "b_double_25y", "c_20pc_25y"):
            for null_model in ("exponential", "cpl"):
                step_row = headline[
                    (headline["level"] == level)
                    & (headline["bracket"] == bracket)
                    & (headline["null_model"] == null_model)
                    & (headline["shape"] == "step")
                ]
                gauss_row = headline[
                    (headline["level"] == level)
                    & (headline["bracket"] == bracket)
                    & (headline["null_model"] == null_model)
                    & (headline["shape"] == "gaussian")
                ]
                step_n = (
                    f"{int(round(step_row.iloc[0]['min_n']))}"
                    if (len(step_row) > 0
                        and not np.isnan(step_row.iloc[0]["min_n"]))
                    else "n/a"
                )
                gauss_n = (
                    f"{int(round(gauss_row.iloc[0]['min_n']))}"
                    if (len(gauss_row) > 0
                        and not np.isnan(gauss_row.iloc[0]["min_n"]))
                    else "n/a"
                )
                lines.append(
                    f"| {level} | {bracket} | {null_model} | "
                    f"{step_n} | {gauss_n} |"
                )
    lines.append("")

    # 2. Power curves.
    lines.append("## 2. Power curves")
    lines.append("")
    lines.append("Per (level x bracket x shape x null x cpl_k), with 0.70 / 0.80 / 0.90 detection-rate gridlines and Wilson 95% CI ribbons.")
    lines.append("")
    lines.append("Files in `power-curves/` (one PNG + one parquet per slice):")
    lines.append("")
    pc_dir = out / "power-curves"
    if pc_dir.exists():
        pngs = sorted(pc_dir.glob("*.png"))
        for p in pngs[:20]:
            lines.append(f"- `power-curves/{p.name}`")
        if len(pngs) > 20:
            lines.append(f"- ... and {len(pngs) - 20} more")
    lines.append("")

    # 3. Heatmaps.
    lines.append("## 3. Effect-size x n heatmaps")
    lines.append("")
    lines.append("Per (level x null x shape x cpl_k), with 0.80 contour highlighted.")
    lines.append("")
    lines.append("Files in `heatmaps/`:")
    lines.append("")
    hm_dir = out / "heatmaps"
    if hm_dir.exists():
        for p in sorted(hm_dir.glob("*.png")):
            lines.append(f"- `heatmaps/{p.name}`")
    lines.append("")

    # 4. Zero-effect FP rate.
    lines.append("## 4. Zero-effect false-positive rates (target ≤ 0.05)")
    lines.append("")
    lines.append("| Level | Null | Shape | cpl_k | n | FP rate |")
    lines.append("|---|---|---|---|---|---|")
    fp_sorted = fp.copy()
    fp_sorted["_lvl"] = fp_sorted["level"].map(level_order)
    fp_sorted["_null"] = fp_sorted["null_model"].map(null_order)
    fp_sorted["_shp"] = fp_sorted["shape"].map(shape_order)
    fp_sorted = fp_sorted.sort_values(["_lvl", "_null", "_shp", "cpl_k", "n"])
    for _, r in fp_sorted.iterrows():
        cpl_k_str = "n/a" if r["cpl_k"] == -1 else f"{int(r['cpl_k'])}"
        lines.append(
            f"| {r['level']} | {r['null_model']} | {r['shape']} | "
            f"{cpl_k_str} | {int(r['n'])} | {r['detection_rate']:.3f} |"
        )
    lines.append("")
    fp_max = fp["detection_rate"].max()
    fp_min = fp["detection_rate"].min()
    lines.append(
        f"FP rate range across all zero-bracket cells: "
        f"[{fp_min:.3f}, {fp_max:.3f}]."
    )
    lines.append("")
    fp_violators = fp[fp["detection_rate"] > 0.05]
    if len(fp_violators) > 0:
        lines.append(f"**{len(fp_violators)} cells exceed 0.05 FP rate** — see table for specifics.")
    else:
        lines.append("All cells within FP target.")
    lines.append("")

    # 5. Exp vs CPL comparison.
    lines.append("## 5. Exponential vs CPL-3 comparison")
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
                    "exp_n": e, "cpl_n": c, "ratio": c / e if e > 0 else np.nan,
                })
    if delta_rows:
        lines.append("| Level | Bracket | Shape | exp n | cpl-3 n | cpl/exp ratio |")
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
                f"Median ratio (cpl/exp): {np.median(ratios):.2f}; "
                f"range [{min(ratios):.2f}, {max(ratios):.2f}]."
            )
    else:
        lines.append("Insufficient data: at least one cell has unreachable threshold.")
    lines.append("")

    # 6. Exploratory: CPL k-sensitivity.
    lines.append("## 6. Exploratory — CPL k-sensitivity (k in {2, 3, 4})")
    lines.append("")
    lines.append("Threshold variation across k values, holding (level, bracket, shape) fixed.")
    lines.append("")
    k_thresh = thresh[
        (thresh["target"] == 0.80) & (thresh["null_model"] == "cpl")
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
                if all(k in k_vals for k in (2, 3, 4)) and \
                   not any(np.isnan(k_vals[k]) for k in (2, 3, 4)):
                    spread = max(k_vals.values()) - min(k_vals.values())
                    k_summary.append({
                        "key": f"{level}/{bracket}/{shape}",
                        "k2": int(round(k_vals[2])),
                        "k3": int(round(k_vals[3])),
                        "k4": int(round(k_vals[4])),
                        "spread": int(round(spread)),
                    })
    if k_summary:
        lines.append("| Level/bracket/shape | k=2 | k=3 | k=4 | spread |")
        lines.append("|---|---|---|---|---|")
        for r in k_summary[:20]:
            lines.append(
                f"| {r['key']} | {r['k2']} | {r['k3']} | {r['k4']} | "
                f"{r['spread']} |"
            )
        if len(k_summary) > 20:
            lines.append(f"| ... ({len(k_summary) - 20} more cells) |  |  |  |  |")
    lines.append("")

    # 7. AIC-select reconstruction.
    lines.append("## 7. Exploratory — AIC-select reconstruction")
    lines.append("")
    lines.append("Per-iteration AIC-best k from `cpl_aic` column. Threshold under the AIC-select rule:")
    lines.append("")
    cpl_only = cell[(cell["null_model"] == "cpl")
                    & cell["cpl_aic"].notna()].copy()
    if len(cpl_only) > 0:
        cpl_only["aic_rank"] = cpl_only.groupby(
            ["cell_id", "iter"]
        )["cpl_aic"].rank(method="first")
        aic_select = cpl_only[cpl_only["aic_rank"] == 1].copy()
        aic_curves = (
            aic_select.groupby(
                ["level", "bracket", "shape", "n"]
            )
            .agg(detection_rate=("detected", "mean"),
                 n_iter=("detected", "count"))
            .reset_index()
        )
        # Quick threshold extraction.
        from power_curves import _interpolate_threshold
        aic_thresh_rows: list[dict] = []
        for keys, sub in aic_curves.groupby(
            ["level", "bracket", "shape"]
        ):
            level, bracket, shape = keys
            ns = sub["n"].to_numpy()
            rates = sub["detection_rate"].to_numpy()
            if len(ns) >= 2:
                interp = _interpolate_threshold(ns, rates, 0.80)
            else:
                interp = (
                    float(ns[0]) if len(ns) == 1 and rates[0] >= 0.80
                    else np.nan
                )
            aic_thresh_rows.append({
                "level": level, "bracket": bracket, "shape": shape,
                "min_n": interp,
            })
        if aic_thresh_rows:
            lines.append("| Level | Bracket | Shape | min n (AIC-select) |")
            lines.append("|---|---|---|---|")
            for r in aic_thresh_rows:
                if r["bracket"] == "zero":
                    continue
                n_str = (
                    f"{int(round(r['min_n']))}"
                    if not np.isnan(r["min_n"])
                    else "n/a"
                )
                lines.append(
                    f"| {r['level']} | {r['bracket']} | {r['shape']} | "
                    f"{n_str} |"
                )
    else:
        lines.append("No CPL fits with AIC available — likely all fits used fallback.")
    lines.append("")

    # 8. Stratified sampling.
    lines.append("## 8. Stratified-sampling exploratory")
    lines.append("")
    lines.append(
        "Per Decision 4 (decisions.md) the stratified-by-province / "
        "stratified-by-urban-area sensitivity is reconstructable post-hoc "
        "from the persisted parquet (using the `province_counts` and "
        "`city_counts` dict columns). Not run in this REPORT; deferred "
        "to follow-up analysis."
    )
    lines.append("")

    # 9. Execution notes.
    lines.append("## 9. Execution notes")
    lines.append("")
    lines.append(f"- Total per-iteration rows: {len(cell):,}")
    lines.append(f"- Cells: {cell['cell_id'].nunique()}")
    lines.append("- Hardware: sapphire (24 cores, 60 GB RAM)")
    if "wall_ms" in cell.columns:
        wall_total = cell["wall_ms"].sum() / 1000.0
        wall_mean = cell["wall_ms"].mean()
        lines.append(
            f"- Total compute: {wall_total/60:.1f} min serial-equivalent; "
            f"per-iteration mean {wall_mean:.0f} ms"
        )
    if len(flagged) > 0:
        lines.append(
            f"- **CPL fallback flag:** {len(flagged)} cells with > 20 % "
            f"fallback (CPL fit failure → exponential)."
        )
        for _, r in flagged.head(10).iterrows():
            lines.append(
                f"  - {r['cell_id']} k={int(r['cpl_k'])}: "
                f"{r['fallback_frac']:.1%}"
            )
        if len(flagged) > 10:
            lines.append(f"  - ... and {len(flagged) - 10} more")
    else:
        lines.append("- CPL fallback fraction <= 20 % in all cells (good).")
    fb_max = fallback["fallback_frac"].max() if len(fallback) > 0 else 0.0
    fb_mean = fallback["fallback_frac"].mean() if len(fallback) > 0 else 0.0
    lines.append(
        f"- CPL fallback fraction range: "
        f"[0.000, {fb_max:.3f}]; mean {fb_mean:.3f}."
    )
    lines.append("")

    # 10. Open questions.
    lines.append("## 10. Open questions for Shawn's morning review")
    lines.append("")
    lines.append("1. **Null-model preregistration choice.** The exp-vs-CPL comparison (§5) shows whether thresholds shift materially. If they disagree (cpl/exp ratio > ~1.5), Shawn must pick one for the prereg fix.")
    lines.append("2. **Urban-area operability at 50 % / 50 y bracket.** Several urban-area cells likely fail to reach 0.80 detection at any tested n (n_max = 2,500). Suggests urban-area H3 confirmatory scope may be tighter than empire/province.")
    if len(flagged) > 0:
        lines.append(
            f"3. **CPL fallback flagged in {len(flagged)} cells** (> 20 % "
            "fallback). Worth inspecting: if all in low-n urban cells, "
            "expected; if in high-n province cells, points to fit "
            "instability."
        )
    if fp_max > 0.05:
        lines.append(
            "4. **FP-rate exceeds target in some cells** — check "
            "zero-bracket table (§4) for which (level, null, shape) "
            "combinations need investigation."
        )
    lines.append(
        "5. **k-sensitivity (§6).** If spread across k in {2, 3, 4} is "
        "narrow, k = 3 is robust; if wide, document choice rationale."
    )
    lines.append("")

    out_md = out / "REPORT.md"
    out_md.write_text("\n".join(lines))
    print(f"Wrote REPORT.md ({len(lines)} lines, "
          f"{out_md.stat().st_size} bytes) to {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
