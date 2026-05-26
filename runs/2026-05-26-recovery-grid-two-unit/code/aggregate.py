#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aggregate.py
============

Per-cell aggregator for the 2026-05-26 two-unit recovery-grid
re-simulation. Roll all per-replicate posterior parquets within one cell
into a per-cell summary JSON containing the prereg-binding pass / fail
flags. Schema matches the 2026-05-22 aggregator.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Per-cell pass thresholds (prereg-binding; unchanged from 2026-05-22).
ALPHA_COVERAGE_PASS = 0.90
PEARSON_R_PASS = 0.95


def aggregate_cell(
    cell_id: str, output_root: Path, write: bool = True
) -> dict[str, Any]:
    """Aggregate all per-replicate posteriors for one cell."""
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

    # Per-tier coverage descriptive — pulled from per-replicate JSON.
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

    # Truth values from replicate 000 sidecar.
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
        "unit": truth["unit"],
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
