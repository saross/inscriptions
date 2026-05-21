#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03-cell-aggregator.py
=====================

Aggregate the per-replicate posterior summaries within one cell of the
H2.1 recovery grid into a single per-cell summary. Computes the
prereg-binding per-cell pass criteria:

- ``alpha_coverage``: fraction of replicates whose alpha 95 % CI
  contains the true alpha. Cell **passes coverage** if >= 0.90
  (prereg §3 line 210, §4 line 333; Decision 21).
- ``median_pearson_r_pgen``: median across replicates of the per-
  replicate Pearson r between posterior-median p_gen and truth.
  Cell **passes shape recovery** if >= 0.95 (prereg §4 line 334).
- ``median_wasserstein_1_pgen``: descriptive supplementary
  (prereg §4 line 334).
- ``convergence_pass_rate``: fraction of replicates meeting both
  R-hat (< 1.01) and ESS_bulk (>= 400) gates with zero divergences.

Output: ``outputs/cell-summaries/<cell_id>-summary.json``.

Usage
-----
    python 03-cell-aggregator.py \\
        --output-root /path/to/runs/.../recovery-grid-validation \\
        --cell-id shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Per-cell pass thresholds (prereg-binding).
ALPHA_COVERAGE_PASS = 0.90
PEARSON_R_PASS = 0.95


def aggregate_cell(
    cell_id: str, output_root: Path, write: bool = True
) -> dict[str, Any]:
    """Aggregate all per-replicate posteriors for one cell.

    Parameters
    ----------
    cell_id : str
    output_root : Path
        Validation-run root.
    write : bool
        If True, persist the aggregate to
        ``outputs/cell-summaries/<cell_id>-summary.json``.

    Returns
    -------
    aggregate : dict
    """
    fits_dir = output_root / "outputs" / "cell-fits" / cell_id
    if not fits_dir.exists():
        raise FileNotFoundError(
            f"No fits directory for cell {cell_id!r}: {fits_dir}"
        )
    parquets = sorted(fits_dir.glob("replicate_*-posterior.parquet"))
    if not parquets:
        raise FileNotFoundError(
            f"No per-replicate parquets found under {fits_dir}"
        )
    records = []
    for p in parquets:
        records.append(pd.read_parquet(p).iloc[0].to_dict())
    df = pd.DataFrame(records)

    n_replicates = int(len(df))
    alpha_coverage = float(df["alpha_covered_95ci"].mean())
    median_pearson = float(df["pearson_r_pgen"].median())
    median_w1 = float(df["wasserstein_1_pgen"].median())
    mean_pearson = float(df["pearson_r_pgen"].mean())
    convergence_pass_rate = float(df["convergence_pass"].mean())
    n_divergences_total = int(df["n_divergences"].sum())
    mean_fit_seconds = float(df["fit_seconds"].mean())

    # Per-tier coverage (descriptive — pulled from JSON sidecars
    # because the parquet keeps only the scalars).
    tier_cov: list[list[bool]] = []
    for p in parquets:
        js = p.with_suffix(".json")
        if js.exists():
            with js.open("r", encoding="utf-8") as fh:
                d = json.load(fh)
                tier_cov.append(d["tier_weights_covered_95ci"])
    if tier_cov:
        tier_cov_arr = np.asarray(tier_cov, dtype=bool)
        per_tier_coverage = tier_cov_arr.mean(axis=0).tolist()
    else:
        per_tier_coverage = []

    # Truth values pulled from the first replicate (constant across
    # replicates within a cell).
    truth_path = (
        output_root / "data" / "synthetic-cells" / cell_id
        / "replicate_000.truth.json"
    )
    with truth_path.open("r", encoding="utf-8") as fh:
        truth = json.load(fh)

    aggregate = {
        "cell_id": cell_id,
        "shape_name": truth["shape_name"],
        "alpha_true": truth["alpha_true"],
        "tier_weights_name": truth["tier_weights_name"],
        "tier_weights_true": truth["tier_weights_true"],
        "n": truth["n"],
        "n_replicates": n_replicates,
        "alpha_coverage": alpha_coverage,
        "alpha_coverage_pass": bool(alpha_coverage >= ALPHA_COVERAGE_PASS),
        "median_pearson_r_pgen": median_pearson,
        "mean_pearson_r_pgen": mean_pearson,
        "pearson_r_pass": bool(median_pearson >= PEARSON_R_PASS),
        "median_wasserstein_1_pgen": median_w1,
        "convergence_pass_rate": convergence_pass_rate,
        "n_divergences_total": n_divergences_total,
        "mean_fit_seconds": mean_fit_seconds,
        "per_tier_coverage": per_tier_coverage,
    }

    if write:
        out_dir = output_root / "outputs" / "cell-summaries"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{cell_id}-summary.json"
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(aggregate, fh, indent=2)
    return aggregate


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate per-replicate posteriors for one cell."
    )
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--cell-id", required=True, type=str)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    agg = aggregate_cell(args.cell_id, args.output_root, write=True)
    print(f"[03-agg] cell {args.cell_id}")
    print(
        f"[03-agg]   alpha_coverage = {agg['alpha_coverage']:.2f} "
        f"({'PASS' if agg['alpha_coverage_pass'] else 'FAIL'})"
    )
    print(
        f"[03-agg]   median Pearson r = {agg['median_pearson_r_pgen']:.4f} "
        f"({'PASS' if agg['pearson_r_pass'] else 'FAIL'})"
    )
    print(
        f"[03-agg]   median W-1 = {agg['median_wasserstein_1_pgen']:.3f}  "
        f"(supplementary)"
    )
    print(
        f"[03-agg]   convergence_pass_rate = "
        f"{agg['convergence_pass_rate']:.2f}; total divergences = "
        f"{agg['n_divergences_total']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
