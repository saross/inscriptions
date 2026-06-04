#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reaggregate.py
==============

Aggregation-only driver for the 2026-05-26 two-unit recovery grid: re-roll
every cell's per-replicate posteriors into a fresh per-cell summary JSON,
WITHOUT re-fitting. This re-derives ``convergence_pass_rate`` from the stored
raw diagnostics (``max_rhat`` / ``min_ess_bulk``) under the current canonical
gate (``cell_lib.convergence_pass``), so a convergence-gate change can be
applied to a completed grid by reading the per-replicate posteriors alone.

Motivation
----------
``run-grid.py`` aggregates as a side effect of *fitting*; ``aggregate.py``
exposes the per-cell roll-up but has no top-level driver. When the convergence
gate was refined on 2026-06-04 (field-standard / benign-divergence-tolerant;
Decision 33 / OSF Amendment 01 §A5.5.1) the grid was already complete, so the
correct response is to RE-AGGREGATE, never re-fit. This script is that step,
made first-class and reproducible: run it where the per-replicate posteriors
live (sapphire), then pull the regenerated cell-summaries back and re-run
``finalise-comparison.sh`` (grid-summariser + alpha-bias + cross-grid compare).

Idempotent: re-running overwrites each ``*-summary.json`` from the immutable
per-replicate posteriors. Only the gitignored cell-summaries are written; the
per-replicate posteriors (the raw record) are never touched.

Usage
-----
    python reaggregate.py \\
        --grid-dir /path/to/runs/2026-05-26-recovery-grid-two-unit/inscription-mass

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-04, on Shawn's harness-re-aggregation
brief. UK / Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Local imports — run from the code/ directory (or with it on sys.path) so the
# sibling ``aggregate`` / ``cell_lib`` modules resolve.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregate import aggregate_cell  # noqa: E402


def reaggregate_grid(grid_dir: Path) -> dict[str, float]:
    """Re-aggregate every cell of one grid from its per-replicate posteriors.

    Parameters
    ----------
    grid_dir : Path
        A grid root such as ``.../recovery-grid-two-unit/inscription-mass``.
        Cell-fit directories are read from ``<grid_dir>/outputs/cell-fits/``;
        regenerated summaries are written to
        ``<grid_dir>/outputs/cell-summaries/``.

    Returns
    -------
    dict[str, float]
        Run-level summary: ``n_cells`` aggregated, plus the ``min`` and
        ``mean`` of the re-derived ``convergence_pass_rate`` across cells (a
        quick eyeball that the new gate took effect).

    Raises
    ------
    FileNotFoundError
        If the cell-fits directory is absent or contains no cell directories.
    """
    fits_root = grid_dir / "outputs" / "cell-fits"
    if not fits_root.exists():
        raise FileNotFoundError(f"No cell-fits directory at {fits_root}")
    cell_ids = sorted(p.name for p in fits_root.iterdir() if p.is_dir())
    if not cell_ids:
        raise FileNotFoundError(f"No cell directories under {fits_root}")

    conv_rates: list[float] = []
    for i, cell_id in enumerate(cell_ids, start=1):
        agg = aggregate_cell(cell_id, grid_dir, write=True)
        conv_rates.append(float(agg["convergence_pass_rate"]))
        if i % 50 == 0 or i == len(cell_ids):
            print(f"[reaggregate] {i}/{len(cell_ids)} cells", flush=True)

    return {
        "n_cells": float(len(cell_ids)),
        "min_convergence_pass_rate": float(min(conv_rates)),
        "mean_convergence_pass_rate": float(sum(conv_rates) / len(conv_rates)),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Re-aggregate one grid's cell-summaries from its per-replicate "
            "posteriors under the current convergence gate (no re-fit)."
        )
    )
    parser.add_argument(
        "--grid-dir",
        required=True,
        type=Path,
        help=(
            "Grid root, e.g. "
            ".../recovery-grid-two-unit/inscription-mass (cell-fits are read "
            "from <grid-dir>/outputs/cell-fits/; summaries written to "
            "<grid-dir>/outputs/cell-summaries/)."
        ),
    )
    return parser.parse_args()


def main() -> int:
    """Re-aggregate the grid and report run-level convergence statistics."""
    args = _parse_args()
    grid_dir = args.grid_dir.resolve()
    stats = reaggregate_grid(grid_dir)
    print(
        f"[reaggregate] DONE grid={grid_dir.name}: "
        f"{int(stats['n_cells'])} cells; "
        f"convergence_pass_rate min={stats['min_convergence_pass_rate']:.3f} "
        f"mean={stats['mean_convergence_pass_rate']:.3f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
