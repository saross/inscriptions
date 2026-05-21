#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05-grid-summariser.py
=====================

Read all per-cell summaries from
``outputs/cell-summaries/<cell_id>-summary.json`` and emit the global
H2.1 validation REPORT.md. Computes the prereg-binding pass rates:

- ``frac_cells_pass_alpha_coverage``: fraction of cells where
  alpha_coverage >= 0.90. Validation requires >= 0.90.
- ``frac_cells_pass_shape_recovery``: fraction of cells where
  median Pearson r >= 0.95. Validation requires >= 0.90.

Also emits a per-cell pass/fail table and characterises failure modes
where cells fail (which alpha / shape / tier-weight / N combinations).

Usage
-----
    python 05-grid-summariser.py \\
        --output-root /path/to/runs/.../recovery-grid-validation

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

# Global validation thresholds (prereg-binding).
ALPHA_COVERAGE_PASS = 0.90  # per cell
SHAPE_PEARSON_PASS = 0.95   # per cell
GLOBAL_FRAC_PASS = 0.90     # of cells


def load_all_summaries(output_root: Path) -> pd.DataFrame:
    summaries_dir = output_root / "outputs" / "cell-summaries"
    if not summaries_dir.exists():
        raise FileNotFoundError(
            f"No cell-summaries directory at {summaries_dir}"
        )
    records = []
    for p in sorted(summaries_dir.glob("*-summary.json")):
        with p.open("r", encoding="utf-8") as fh:
            records.append(json.load(fh))
    if not records:
        raise FileNotFoundError("No per-cell summaries found.")
    return pd.DataFrame(records)


def make_report(df: pd.DataFrame) -> str:
    n_cells = int(len(df))
    cov_pass = df["alpha_coverage_pass"].astype(bool)
    r_pass = df["pearson_r_pass"].astype(bool)
    both_pass = cov_pass & r_pass

    frac_cov = float(cov_pass.mean())
    frac_r = float(r_pass.mean())
    frac_both = float(both_pass.mean())

    validated = bool(
        frac_cov >= GLOBAL_FRAC_PASS and frac_r >= GLOBAL_FRAC_PASS
    )

    lines: list[str] = []
    lines.append("# H2.1 Recovery Grid — Final Report")
    lines.append("")
    lines.append(
        "Bayesian deconvolution-mixture model validation via the H2.1 "
        "recovery simulation."
    )
    lines.append(
        "See `runs/2026-05-22-recovery-grid-design/spec.md` for the binding"
        " grid axes and decision rule."
    )
    lines.append("")
    lines.append("## 1. Headline result")
    lines.append("")
    lines.append(
        f"**Validation verdict:** "
        f"{'PASS' if validated else 'FAIL'} (binding criteria require "
        f">= {GLOBAL_FRAC_PASS:.0%} of cells to pass coverage AND "
        f"shape recovery)"
    )
    lines.append("")
    lines.append("| Criterion | Threshold | Result | Pass? |")
    lines.append("|---|---|---|---|")
    lines.append(
        f"| alpha-coverage >= {ALPHA_COVERAGE_PASS:.0%} per cell | "
        f">= {GLOBAL_FRAC_PASS:.0%} of cells | "
        f"{frac_cov:.1%} ({int(cov_pass.sum())}/{n_cells} cells) | "
        f"{'PASS' if frac_cov >= GLOBAL_FRAC_PASS else 'FAIL'} |"
    )
    lines.append(
        f"| median Pearson r >= {SHAPE_PEARSON_PASS:.2f} per cell | "
        f">= {GLOBAL_FRAC_PASS:.0%} of cells | "
        f"{frac_r:.1%} ({int(r_pass.sum())}/{n_cells} cells) | "
        f"{'PASS' if frac_r >= GLOBAL_FRAC_PASS else 'FAIL'} |"
    )
    lines.append(
        f"| Both criteria simultaneously | (informational) | "
        f"{frac_both:.1%} ({int(both_pass.sum())}/{n_cells}) | — |"
    )
    lines.append("")

    # Per-axis pass rates.
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

    # Failed cells table.
    failed = df[~(cov_pass & r_pass)].sort_values(
        ["alpha_coverage", "median_pearson_r_pgen"]
    )
    lines.append("## 3. Failed cells (either criterion)")
    lines.append("")
    if failed.empty:
        lines.append("None — every cell passed both criteria.")
    else:
        lines.append(
            "| cell_id | alpha_cov | median Pearson r | median W-1 |"
            " convergence_pass | divergences |"
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

    # Wall-clock + convergence diagnostics.
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
    lines.append("## 5. Wasserstein-1 supplementary")
    lines.append("")
    lines.append(
        "Wasserstein-1 is reported per cell as a distribution-sensitive "
        "shape metric (prereg §4 line 334). The flagging threshold is "
        "deferred to a follow-up artefact (see design spec §6)."
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
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarise the H2.1 recovery grid into REPORT.md."
    )
    parser.add_argument("--output-root", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    df = load_all_summaries(args.output_root)
    report = make_report(df)
    out_path = args.output_root / "outputs" / "REPORT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"[05-summary] wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
