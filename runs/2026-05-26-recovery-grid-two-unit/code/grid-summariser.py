#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grid-summariser.py
==================

Per-grid summariser for the 2026-05-26 two-unit recovery-grid
re-simulation. Reads every per-cell summary JSON for ONE grid
(``inscription-mass`` or ``letter-mass``) and emits that grid's
binding-criterion verdict.

This generalises the single-grid ``runs/2026-05-22-recovery-grid-
validation/code/05-grid-summariser.py`` to the two-unit directory layout
(spec.md §4) and additionally persists a machine-readable
``grid-summary.parquet`` table (the cross-grid comparison harness,
``compare-grids.py``, consumes it). The cell-summary JSON schema is
identical between the two runs, so the binding logic is unchanged.

Binding criteria (prereg §4 lines 333-334; spec.md §5):

- ``frac_cells_pass_alpha_coverage``: fraction of cells where
  ``alpha_coverage >= 0.90``. Validation requires this fraction >= 0.90.
- ``frac_cells_pass_shape_recovery``: fraction of cells where the
  posterior-median Pearson r (``median_pearson_r_pgen``) >= 0.95.
  Validation requires this fraction >= 0.90.

The grid is VALIDATED (PASS) only if BOTH fractions are >= 0.90.

Outputs (written under ``<grid-dir>/outputs/``):

- ``tables/grid-summary.parquet`` -- one row per cell; all summary
  fields plus a derived ``both_pass`` flag.
- ``REPORT.md`` -- headline verdict, per-axis pass rates, failed-cell
  table, diagnostics, and the Wasserstein-1 supplementary.

Usage
-----
    python grid-summariser.py \\
        --grid-dir /path/to/runs/2026-05-26-recovery-grid-two-unit/inscription-mass

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------- #
# Binding thresholds (prereg-binding; identical to the 2026-05-22 run).        #
# --------------------------------------------------------------------------- #
ALPHA_COVERAGE_PASS = 0.90  # per-cell coverage floor
SHAPE_PEARSON_PASS = 0.95   # per-cell median-Pearson-r floor
GLOBAL_FRAC_PASS = 0.90     # fraction-of-cells floor for both criteria


def load_all_summaries(grid_dir: Path) -> pd.DataFrame:
    """Load every per-cell summary JSON for one grid into a DataFrame.

    Parameters
    ----------
    grid_dir : Path
        A grid root such as ``.../recovery-grid-two-unit/inscription-mass``.
        Cell summaries are expected at ``<grid_dir>/outputs/cell-summaries/
        *-summary.json``.

    Returns
    -------
    pandas.DataFrame
        One row per cell, columns matching the cell-summary JSON schema.

    Raises
    ------
    FileNotFoundError
        If the cell-summaries directory is absent or contains no summaries.
    """
    summaries_dir = grid_dir / "outputs" / "cell-summaries"
    if not summaries_dir.exists():
        raise FileNotFoundError(
            f"No cell-summaries directory at {summaries_dir}"
        )
    records = []
    for path in sorted(summaries_dir.glob("*-summary.json")):
        with path.open("r", encoding="utf-8") as handle:
            records.append(json.load(handle))
    if not records:
        raise FileNotFoundError(
            f"No per-cell summaries found under {summaries_dir}"
        )
    return pd.DataFrame(records)


def compute_verdict(df: pd.DataFrame) -> dict[str, object]:
    """Compute the grid-level binding verdict from per-cell flags.

    Returns a dict carrying the three fractions, the per-criterion
    pass booleans, the combined ``validated`` verdict, and the cell count.
    """
    n_cells = int(len(df))
    cov_pass = df["alpha_coverage_pass"].astype(bool)
    r_pass = df["pearson_r_pass"].astype(bool)
    both_pass = cov_pass & r_pass

    frac_cov = float(cov_pass.mean())
    frac_r = float(r_pass.mean())
    frac_both = float(both_pass.mean())

    return {
        "n_cells": n_cells,
        "frac_cov": frac_cov,
        "frac_r": frac_r,
        "frac_both": frac_both,
        "cov_criterion_pass": bool(frac_cov >= GLOBAL_FRAC_PASS),
        "r_criterion_pass": bool(frac_r >= GLOBAL_FRAC_PASS),
        "validated": bool(
            frac_cov >= GLOBAL_FRAC_PASS and frac_r >= GLOBAL_FRAC_PASS
        ),
    }


def write_grid_summary_parquet(df: pd.DataFrame, grid_dir: Path) -> Path:
    """Persist the per-cell table (plus a ``both_pass`` flag) to parquet.

    This is the machine-readable artefact the cross-grid comparison harness
    joins on ``cell_id``. Returns the written path.
    """
    out = df.copy()
    out["both_pass"] = (
        out["alpha_coverage_pass"].astype(bool)
        & out["pearson_r_pass"].astype(bool)
    )
    tables_dir = grid_dir / "outputs" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    out_path = tables_dir / "grid-summary.parquet"
    out.to_parquet(out_path, index=False)
    return out_path


def make_report(df: pd.DataFrame) -> str:
    """Render the per-grid REPORT.md content as a single Markdown string."""
    verdict = compute_verdict(df)
    n_cells = verdict["n_cells"]
    cov_pass = df["alpha_coverage_pass"].astype(bool)
    r_pass = df["pearson_r_pass"].astype(bool)
    both_pass = cov_pass & r_pass

    # The unit label is constant within a grid; read it from the first row.
    unit = str(df["unit"].iloc[0]) if "unit" in df.columns else "unknown"

    lines: list[str] = []
    lines.append(f"# Recovery Grid — {unit}-mass — Per-Grid Report")
    lines.append("")
    lines.append(
        "Bayesian deconvolution-mixture model validation via the two-unit "
        "recovery simulation."
    )
    lines.append(
        "See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the "
        "binding decision rule, and the 2026-05-22 predecessor run for the "
        "shared cell design."
    )
    lines.append("")
    lines.append("## 1. Headline result")
    lines.append("")
    lines.append(
        f"**Unit of analysis:** {unit}-mass "
        f"(each synthetic inscription deposits "
        f"{'unit count' if unit == 'inscription' else 'letter mass'})."
    )
    lines.append("")
    lines.append(
        f"**Validation verdict:** "
        f"{'PASS' if verdict['validated'] else 'FAIL'} "
        f"(binding criteria require >= {GLOBAL_FRAC_PASS:.0%} of cells to "
        f"pass coverage AND shape recovery)"
    )
    lines.append("")
    lines.append("| Criterion | Threshold | Result | Pass? |")
    lines.append("|---|---|---|---|")
    lines.append(
        f"| alpha-coverage >= {ALPHA_COVERAGE_PASS:.0%} per cell "
        f"| >= {GLOBAL_FRAC_PASS:.0%} of cells "
        f"| {verdict['frac_cov']:.1%} ({int(cov_pass.sum())}/{n_cells}) "
        f"| {'PASS' if verdict['cov_criterion_pass'] else 'FAIL'} |"
    )
    lines.append(
        f"| median Pearson r >= {SHAPE_PEARSON_PASS:.2f} per cell "
        f"| >= {GLOBAL_FRAC_PASS:.0%} of cells "
        f"| {verdict['frac_r']:.1%} ({int(r_pass.sum())}/{n_cells}) "
        f"| {'PASS' if verdict['r_criterion_pass'] else 'FAIL'} |"
    )
    lines.append(
        f"| Both criteria simultaneously | (informational) "
        f"| {verdict['frac_both']:.1%} ({int(both_pass.sum())}/{n_cells}) "
        f"| — |"
    )
    lines.append("")

    # ----- Per-axis pass rates ------------------------------------------- #
    lines.append("## 2. Per-axis pass rates")
    lines.append("")
    for axis, col in [
        ("alpha", "alpha_true"),
        ("shape", "shape_name"),
        ("tier_weights", "tier_weights_name"),
        ("N", "n"),
    ]:
        lines.append(f"### 2.{axis}")
        lines.append("")
        lines.append(
            f"| {axis} | n_cells | alpha-cov pass | shape pass | both |"
        )
        lines.append("|---|---|---|---|---|")
        for key, grp in df.groupby(col):
            n_k = len(grp)
            cov_k = grp["alpha_coverage_pass"].astype(bool).mean()
            r_k = grp["pearson_r_pass"].astype(bool).mean()
            both_k = (
                grp["alpha_coverage_pass"].astype(bool)
                & grp["pearson_r_pass"].astype(bool)
            ).mean()
            lines.append(
                f"| {key} | {n_k} | {cov_k:.0%} | {r_k:.0%} | {both_k:.0%} |"
            )
        lines.append("")

    # ----- Failed cells -------------------------------------------------- #
    failed = df[~both_pass].sort_values(
        ["alpha_coverage", "median_pearson_r_pgen"]
    )
    lines.append("## 3. Failed cells (either criterion)")
    lines.append("")
    if failed.empty:
        lines.append("None — every cell passed both criteria.")
    else:
        lines.append(
            "| cell_id | alpha_cov | median Pearson r | median W-1 "
            "| convergence_pass | divergences |"
        )
        lines.append("|---|---|---|---|---|---|")
        for _, row in failed.iterrows():
            lines.append(
                f"| `{row['cell_id']}` "
                f"| {row['alpha_coverage']:.2f} "
                f"| {row['median_pearson_r_pgen']:.4f} "
                f"| {row['median_wasserstein_1_pgen']:.2f} "
                f"| {row['convergence_pass_rate']:.2f} "
                f"| {int(row['n_divergences_total'])} |"
            )
    lines.append("")

    # ----- Diagnostics --------------------------------------------------- #
    lines.append("## 4. Diagnostics")
    lines.append("")
    lines.append(
        f"- Mean fit-seconds per replicate: "
        f"{float(df['mean_fit_seconds'].mean()):.2f}"
    )
    lines.append(
        f"- Min cell-level convergence pass rate: "
        f"{float(df['convergence_pass_rate'].min()):.2%}"
    )
    lines.append(
        f"- Cells with any divergences: "
        f"{int((df['n_divergences_total'] > 0).sum())}/{n_cells}"
    )
    lines.append("")

    # ----- Wasserstein-1 supplementary ----------------------------------- #
    lines.append("## 5. Wasserstein-1 supplementary")
    lines.append("")
    lines.append(
        "Wasserstein-1 is reported per cell as a distribution-sensitive "
        "shape metric (prereg §4 line 334). Its flagging threshold remains "
        "deferred (spec.md §5; needs empirical posteriors to anchor) and is "
        "NOT part of the binding rule."
    )
    lines.append("")
    lines.append(
        f"- Median across cells: "
        f"{float(df['median_wasserstein_1_pgen'].median()):.2f}"
    )
    lines.append(
        f"- 90th percentile across cells: "
        f"{float(df['median_wasserstein_1_pgen'].quantile(0.9)):.2f}"
    )
    lines.append("")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Summarise one grid of the two-unit recovery simulation into "
            "REPORT.md + grid-summary.parquet."
        )
    )
    parser.add_argument(
        "--grid-dir",
        required=True,
        type=Path,
        help=(
            "Grid root, e.g. "
            ".../recovery-grid-two-unit/inscription-mass (cell-summaries "
            "are read from <grid-dir>/outputs/cell-summaries/)."
        ),
    )
    return parser.parse_args()


def main() -> int:
    """Load summaries, compute the verdict, write parquet + REPORT.md."""
    args = _parse_args()
    grid_dir = args.grid_dir.resolve()

    df = load_all_summaries(grid_dir)
    verdict = compute_verdict(df)

    parquet_path = write_grid_summary_parquet(df, grid_dir)
    report = make_report(df)
    report_path = grid_dir / "outputs" / "REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    unit = str(df["unit"].iloc[0]) if "unit" in df.columns else "unknown"
    print(f"[grid-summariser] unit={unit}-mass  n_cells={verdict['n_cells']}")
    print(
        f"[grid-summariser] coverage pass-rate "
        f"{verdict['frac_cov']:.1%} (need >= {GLOBAL_FRAC_PASS:.0%}) -> "
        f"{'PASS' if verdict['cov_criterion_pass'] else 'FAIL'}"
    )
    print(
        f"[grid-summariser] shape-r pass-rate  "
        f"{verdict['frac_r']:.1%} (need >= {GLOBAL_FRAC_PASS:.0%}) -> "
        f"{'PASS' if verdict['r_criterion_pass'] else 'FAIL'}"
    )
    print(
        f"[grid-summariser] VERDICT: "
        f"{'PASS' if verdict['validated'] else 'FAIL'}"
    )
    print(f"[grid-summariser] wrote {parquet_path}")
    print(f"[grid-summariser] wrote {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
