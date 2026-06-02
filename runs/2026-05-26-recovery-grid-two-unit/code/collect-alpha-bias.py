#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect-alpha-bias.py
=====================

Compact recovered-alpha-bias collector for one grid of the 2026-05-26
two-unit recovery simulation.

The per-cell summary JSONs (from ``aggregate.py``) keep the alpha COVERAGE
fraction but not the recovered-alpha point estimates, so the
``fig-alpha-bias-by-tier.png`` figure in ``compare-grids.py`` cannot be
built from them alone. This script walks the per-replicate posterior
parquets (which DO carry ``alpha_median`` / ``alpha_true``) and rolls them
into a small per-cell ``alpha-bias.parquet`` table that the comparison
harness consumes.

It reads only the three columns it needs and is strictly read-only over
the grid's finished outputs — safe to run against Grid A while Grid B is
still fitting (it touches a different subtree and no live processes).

Output
------
``<grid-dir>/outputs/tables/alpha-bias.parquet`` with one row per cell:

    cell_id, shape_name, alpha_true, tier_weights_name, n, n_reps,
    median_recovered_alpha, alpha_bias_mean, alpha_bias_median

where ``alpha_bias_* = recovered_alpha_median - alpha_true`` aggregated
over the cell's replicates (signed; positive = recovered alpha too high).

Usage
-----
    python collect-alpha-bias.py \\
        --grid-dir /path/to/runs/.../recovery-grid-two-unit/inscription-mass

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

# Parse the canonical cell_id, e.g.
# "shape=regnal_cluster_alpha=0.70_tier=uniform_N=2000".
_CELL_RE = re.compile(
    r"^shape=(?P<shape>.+?)_alpha=(?P<alpha>[\d.]+)_"
    r"tier=(?P<tier>.+?)_N=(?P<n>\d+)$"
)


def parse_cell_id(cell_id: str) -> dict:
    """Decompose a cell_id into its four design axes (raises on mismatch)."""
    m = _CELL_RE.match(cell_id)
    if not m:
        raise ValueError(f"Unparseable cell_id: {cell_id!r}")
    return {
        "shape_name": m.group("shape"),
        "alpha_true": float(m.group("alpha")),
        "tier_weights_name": m.group("tier"),
        "n": int(m.group("n")),
    }


def collect(grid_dir: Path) -> pd.DataFrame:
    """Aggregate recovered-alpha bias per cell from per-replicate parquets."""
    fits_root = grid_dir / "outputs" / "cell-fits"
    if not fits_root.exists():
        raise FileNotFoundError(f"No cell-fits directory at {fits_root}")

    rows = []
    cell_dirs = sorted(d for d in fits_root.iterdir() if d.is_dir())
    for cell_dir in cell_dirs:
        parquets = sorted(cell_dir.glob("replicate_*-posterior.parquet"))
        if not parquets:
            continue
        recovered = []
        truth = None
        for p in parquets:
            # Column-selective read keeps this cheap across ~100 files/cell.
            d = pd.read_parquet(p, columns=["alpha_true", "alpha_median"])
            recovered.append(float(d["alpha_median"].iloc[0]))
            truth = float(d["alpha_true"].iloc[0])
        rec = pd.Series(recovered, dtype=float)
        axes = parse_cell_id(cell_dir.name)
        # Prefer the parquet's alpha_true; fall back to the parsed axis.
        alpha_true = truth if truth is not None else axes["alpha_true"]
        bias = rec - alpha_true
        rows.append(
            {
                "cell_id": cell_dir.name,
                "shape_name": axes["shape_name"],
                "alpha_true": alpha_true,
                "tier_weights_name": axes["tier_weights_name"],
                "n": axes["n"],
                "n_reps": int(len(rec)),
                "median_recovered_alpha": float(rec.median()),
                "alpha_bias_mean": float(bias.mean()),
                "alpha_bias_median": float(bias.median()),
            }
        )
    if not rows:
        raise FileNotFoundError(
            f"No per-replicate parquets found under {fits_root}"
        )
    return pd.DataFrame(rows)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Collect per-cell recovered-alpha bias for one grid."
    )
    p.add_argument("--grid-dir", required=True, type=Path)
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    grid_dir = args.grid_dir.resolve()
    df = collect(grid_dir)

    tables_dir = grid_dir / "outputs" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    out_path = tables_dir / "alpha-bias.parquet"
    df.to_parquet(out_path, index=False)

    print(f"[alpha-bias] cells: {len(df)}")
    print(
        f"[alpha-bias] mean |bias| across cells: "
        f"{df['alpha_bias_mean'].abs().mean():.4f}"
    )
    print(
        f"[alpha-bias] worst over-estimate: "
        f"{df['alpha_bias_mean'].max():+.4f}; "
        f"worst under-estimate: {df['alpha_bias_mean'].min():+.4f}"
    )
    print(f"[alpha-bias] wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
