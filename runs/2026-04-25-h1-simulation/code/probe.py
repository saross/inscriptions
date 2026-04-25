#!/usr/bin/env python3
"""
probe.py --- Wall-time probe for the H1 simulation.

Runs a small, representative subset of cells with reduced iteration counts
to estimate per-iteration wall time across the four "shapes" of compute
work (exponential null vs CPL null × small n vs large n). Multiplies up
to produce a full-sweep wall-time estimate.

Output: prints the estimate to stdout. Does NOT write parquet.

Usage (from sapphire ~/Code/inscriptions):

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/probe.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from h1_sim import CellSpec, run_cell  # noqa: E402
from primitives import load_filtered_lire  # noqa: E402


def time_one_cell(spec: CellSpec, source_df, master_seed: int = 20260425) -> float:
    """Run one cell and return wall-time in seconds."""
    ss = np.random.SeedSequence(master_seed).spawn(1)[0]
    t0 = time.perf_counter()
    recs = run_cell(spec, source_df, ss)
    elapsed = time.perf_counter() - t0
    print(f"  {spec.cell_id}: {elapsed:.2f}s, {len(recs)} records", flush=True)
    return elapsed


def main() -> int:
    print("Loading filtered LIRE...", flush=True)
    df = load_filtered_lire("archive/data-2026-04-22/LIRE_v3-0.parquet")
    print(f"  {len(df)} rows loaded", flush=True)

    # Reduced iters/mc: 50 iters × 100 mc instead of 1000 × 1000.
    # Scaling factor for full grid: (1000/50) * (1000/100) = 200x per iteration cost.
    # But MC is the inner loop dominating cost; iter scales linearly. So
    # full_cost ~= probe_cost * (1000/50) * (1000/100) = 200x per cell.
    n_iter = 50
    n_mc = 100
    scale_factor = (1000 / n_iter) * (1000 / n_mc)

    probes = [
        # Exponential null cells.
        CellSpec("probe_emp_exp", "empire", "c_20pc_25y", "gaussian",
                 50_000, "exponential", n_iter, n_mc),
        CellSpec("probe_prov_exp_2500", "province", "c_20pc_25y", "gaussian",
                 2_500, "exponential", n_iter, n_mc),
        CellSpec("probe_urb_exp_500", "urban-area", "c_20pc_25y", "gaussian",
                 500, "exponential", n_iter, n_mc),
        # CPL cells (3x more MC work because k = 2, 3, 4).
        CellSpec("probe_prov_cpl_2500", "province", "c_20pc_25y", "gaussian",
                 2_500, "cpl", n_iter, n_mc),
        CellSpec("probe_urb_cpl_500", "urban-area", "c_20pc_25y", "gaussian",
                 500, "cpl", n_iter, n_mc),
    ]

    print(f"\nRunning {len(probes)} probe cells (iter={n_iter}, mc={n_mc})...",
          flush=True)
    times: dict[str, float] = {}
    for spec in probes:
        times[spec.cell_id] = time_one_cell(spec, df)

    # Estimate full sweep: 256 cells = 128 exp + 128 cpl.
    # Take avg per-cell from each null model; weight by mean n if needed.
    # Conservative: assume all cells like the slowest probe of each null type.
    exp_max = max(times["probe_emp_exp"], times["probe_prov_exp_2500"],
                  times["probe_urb_exp_500"])
    cpl_max = max(times["probe_prov_cpl_2500"], times["probe_urb_cpl_500"])
    exp_mean = np.mean([times["probe_emp_exp"],
                        times["probe_prov_exp_2500"],
                        times["probe_urb_exp_500"]])
    cpl_mean = np.mean([times["probe_prov_cpl_2500"],
                        times["probe_urb_cpl_500"]])

    print(f"\nProbe times: exp_max={exp_max:.1f}s, cpl_max={cpl_max:.1f}s",
          flush=True)
    print(f"Probe times: exp_mean={exp_mean:.1f}s, cpl_mean={cpl_mean:.1f}s",
          flush=True)

    # Scale up to 1000 iters × 1000 mc.
    # 128 exp cells + 128 cpl cells.
    full_exp_serial = 128 * exp_mean * scale_factor
    full_cpl_serial = 128 * cpl_mean * scale_factor
    full_serial = full_exp_serial + full_cpl_serial

    n_cores = 24
    overhead = 1.3  # joblib/load-imbalance fudge.
    parallel_estimate = (full_serial / n_cores) * overhead

    print(f"\nFull-grid scale-up (iter * mc factor = {scale_factor:.0f}x):")
    print(f"  Serial estimate: {full_serial / 60:.1f} min "
          f"(exp={full_exp_serial/60:.1f}, cpl={full_cpl_serial/60:.1f})")
    print(f"  Parallel ({n_cores} cores, {overhead}x overhead): "
          f"{parallel_estimate / 60:.1f} min")
    print(f"  Worst case (5x): {5 * parallel_estimate / 60:.1f} min")
    return 0


if __name__ == "__main__":
    sys.exit(main())
