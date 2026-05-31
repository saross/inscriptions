#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_bin_nesting.py — confirm the 50y grid nests the 25y grid.
================================================================

The 50-year robustness grid must be an exact COARSENING of the 25-year primary
grid: every 50y bin is the union of two adjacent 25y bins, and the 50y edges are
a subset of the 25y edges. If that holds, the bin-width robustness check is a
clean re-aggregation rather than an independent re-gridding (spec §3).

Two checks:

1. **Edge nesting.** ``make_grid(50)`` edges ⊆ ``make_grid(25)`` edges, and each
   50y bin ``[E_2k, E_2k+2)`` (25y indexing) maps to one 50y bin.
2. **Aoristic re-aggregation.** For each cached city, the 50y aoristic matrix
   equals the 25y matrix with adjacent column PAIRS summed and HALVED. Because
   ``a25[:, 2k] + a25[:, 2k+1]`` is the fraction-of-(two 25y bins) covered (each
   weighted to its own 25y width), the equivalent 50y fraction-of-bin weight is
   ``(a25[:, 2k]*25 + a25[:, 2k+1]*25) / 50 = (a25[:, 2k] + a25[:, 2k+1]) / 2``.
   We verify ``max |a50 - (a25_pairs)/2| < 1e-12`` over all rows of every city.

Run (on zbook, in the venv)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/verify_bin_nesting.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp  # noqa: E402


def main() -> int:
    """Run both nesting checks across the cached 25y and 50y target sets."""
    e25, n25 = dp.make_grid(25)
    e50, n50 = dp.make_grid(50)

    # --- Check 1: edge nesting -------------------------------------------- #
    e50_in_e25 = np.all(np.isin(e50, e25))
    print(f"25y grid: {n25} bins, edges {e25.astype(int).tolist()}")
    print(f"50y grid: {n50} bins, edges {e50.astype(int).tolist()}")
    print(f"  50y edges ⊆ 25y edges : {bool(e50_in_e25)}")
    assert e50_in_e25, "50y edges are NOT a subset of 25y edges — grids do not nest."
    assert n25 == 2 * n50, f"expected n25 == 2*n50; got {n25} vs {n50}"

    # --- Check 2: aoristic re-aggregation over every cached city ---------- #
    dir25 = dp.default_cache_dir(25)
    dir50 = dp.default_cache_dir(50)
    idx = pd.read_parquet(dir25 / "city-index.parquet")
    fittable = idx[idx["bucket"].isin(["target", "large_anchor"])]["city"].tolist()

    worst = 0.0
    worst_city = None
    n_checked = 0
    for city in fittable:
        b25 = dp.load_city(dir25, city)
        b50 = dp.load_city(dir50, city)
        a25 = np.asarray(b25["A"], dtype=float)        # (N, 16)
        a50 = np.asarray(b50["A"], dtype=float)        # (N, 8)
        # Sum adjacent 25y column pairs, halve to convert to 50y fraction-of-bin.
        a25_reagg = (a25[:, 0::2] + a25[:, 1::2]) / 2.0   # (N, 8)
        err = float(np.max(np.abs(a50 - a25_reagg)))
        if err > worst:
            worst, worst_city = err, city
        n_checked += 1

    print(f"\nRe-aggregation check over {n_checked} cached cities:")
    print(f"  max |a50 - (a25 adjacent-pair mean)| = {worst:.2e}  "
          f"(worst city: {worst_city})")
    ok = worst < 1e-12
    print(f"  NESTING {'CONFIRMED' if ok else 'FAILED'} "
          f"(50y bin == union of two adjacent 25y bins).")
    return 0 if (e50_in_e25 and ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
