#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04-grid-runner.py
=================

Orchestrate the H2.1 recovery-grid simulation. Iterates over the 450
cells pinned in ``design.json``; for each cell, generates 100 replicates,
fits the prereg-binding three-tier multinomial mixture model, and
aggregates per-cell summaries.

Parallelisation strategy
------------------------
The outer joblib loop fans out across cells. By default ``n_jobs = 20``
on sapphire (24 physical cores; 4 reserved as headroom). Each
fit-replicate worker is single-process (``cores = 1`` inside pymc) so
the outer parallelism is the only concurrency layer; this avoids
oversubscription. If a future smoke test shows the per-fit cost is high
enough to make 4-chain in-process parallelism worthwhile, the cap drops
to ``n_jobs = 6`` and pymc's ``cores = 4``.

Resumability
------------
After each cell completes (all 100 replicates fit + per-cell summary
written) the orchestrator updates ``outputs/grid-state.json``. On
restart the runner skips any cell whose per-cell-summary JSON already
exists, so the grid is resumable at cell granularity.

Usage
-----
    python 04-grid-runner.py \\
        --design-json /path/to/design.json \\
        --output-root /path/to/runs/.../recovery-grid-validation \\
        --n-jobs 20 \\
        [--cells-limit N]    (for smoke-test slicing)

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any

from joblib import Parallel, delayed

# Load the sibling 01- and 02- scripts (they are not importable directly
# because of the leading digit).
_THIS_DIR = Path(__file__).resolve().parent

def _load_sibling(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(
        module_name, _THIS_DIR / filename
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


synth_gen = _load_sibling("01-synthetic-cell-generator.py", "synth_gen")
fit_mod = _load_sibling("02-cell-mixture-fit.py", "fit_mod")
agg_mod = _load_sibling("03-cell-aggregator.py", "agg_mod")


def process_cell(
    cell: dict[str, Any],
    design_path: Path,
    output_root: Path,
    n_replicates: int,
    n_draws: int,
    n_tune: int,
    n_chains: int,
    target_accept: float,
    cores: int,
) -> dict[str, Any]:
    """Run scripts 01 + 02 + 03 for one cell. Returns aggregate dict.

    Re-loads the design.json and tier_basis inside the worker so that
    joblib can serialise the work item across process boundaries (numpy
    arrays + a path).
    """
    try:
        design = synth_gen.load_design(design_path)
        env = synth_gen.make_envelope(design)
        tier_basis = synth_gen.build_tier_basis(design, env)

        cell_id = cell["cell_id"]
        # Skip if the cell summary already exists (resumable).
        summary_path = (
            output_root / "outputs" / "cell-summaries"
            / f"{cell_id}-summary.json"
        )
        if summary_path.exists():
            with summary_path.open("r", encoding="utf-8") as fh:
                return json.load(fh)

        t_start = time.time()
        for r in range(n_replicates):
            # 01 — generate (idempotent; re-runs are cheap if files exist).
            synth_path = (
                output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.parquet"
            )
            truth_path = (
                output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.truth.json"
            )
            if not (synth_path.exists() and truth_path.exists()):
                synth_gen.generate_replicate(
                    cell, r, int(design["base_seed"]), env, tier_basis,
                    output_root,
                )

            # 02 — fit (idempotent at the JSON-output level).
            posterior_json = (
                output_root / "outputs" / "cell-fits" / cell_id
                / f"replicate_{r:03d}-posterior.json"
            )
            if not posterior_json.exists():
                fit_mod.fit_replicate(
                    cell_id=cell_id,
                    replicate=r,
                    output_root=output_root,
                    design=design,
                    tier_basis=tier_basis,
                    n_draws=n_draws,
                    n_tune=n_tune,
                    n_chains=n_chains,
                    target_accept=target_accept,
                    cores=cores,
                    progressbar=False,
                )

        # 03 — aggregate.
        aggregate = agg_mod.aggregate_cell(cell_id, output_root, write=True)
        aggregate["wall_seconds_for_cell"] = float(time.time() - t_start)
        return aggregate
    except Exception as exc:  # noqa: BLE001
        tb = traceback.format_exc()
        return {
            "cell_id": cell.get("cell_id", "<unknown>"),
            "error": str(exc),
            "traceback": tb,
        }


def update_state(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the H2.1 recovery-grid simulation."
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--n-jobs", type=int, default=20)
    parser.add_argument(
        "--n-replicates", type=int, default=None,
        help="Override design.json replicates_per_cell (smoke test only).",
    )
    parser.add_argument(
        "--cells-limit", type=int, default=None,
        help="Process only the first N cells (smoke test).",
    )
    parser.add_argument("--n-draws", type=int, default=fit_mod.DEFAULT_N_DRAWS)
    parser.add_argument("--n-tune", type=int, default=fit_mod.DEFAULT_N_TUNE)
    parser.add_argument(
        "--n-chains", type=int, default=fit_mod.DEFAULT_N_CHAINS
    )
    parser.add_argument(
        "--target-accept", type=float, default=fit_mod.DEFAULT_TARGET_ACCEPT
    )
    parser.add_argument(
        "--cores", type=int, default=fit_mod.DEFAULT_CORES,
        help="Cores per pymc fit; total CPU = n_jobs * cores.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    design = synth_gen.load_design(args.design_json)
    n_replicates = (
        args.n_replicates
        if args.n_replicates is not None
        else int(design["replicates_per_cell"])
    )

    cells = synth_gen.enumerate_grid_cells(design)
    if args.cells_limit is not None:
        cells = cells[: args.cells_limit]

    state_path = args.output_root / "outputs" / "grid-state.json"
    state: dict[str, Any] = {
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_cells": len(cells),
        "n_jobs": args.n_jobs,
        "n_replicates_per_cell": n_replicates,
        "design_path": str(args.design_json),
        "completed_cells": [],
        "failed_cells": [],
    }
    update_state(state_path, state)

    print(
        f"[04-grid] launching grid: {len(cells)} cells x "
        f"{n_replicates} replicates; n_jobs={args.n_jobs}; "
        f"cores_per_fit={args.cores}; n_chains={args.n_chains}; "
        f"n_draws={args.n_draws}; n_tune={args.n_tune}; "
        f"target_accept={args.target_accept}"
    )
    t0 = time.time()

    # joblib.Parallel returns results in submission order so we can update
    # state as cells complete.
    parallel = Parallel(
        n_jobs=args.n_jobs,
        backend="loky",
        return_as="generator",
        verbose=10,
    )
    completed = 0
    failed = 0
    delayed_calls = (
        delayed(process_cell)(
            cell,
            args.design_json,
            args.output_root,
            n_replicates,
            args.n_draws,
            args.n_tune,
            args.n_chains,
            args.target_accept,
            args.cores,
        )
        for cell in cells
    )
    for result in parallel(delayed_calls):
        cid = result.get("cell_id", "<unknown>")
        if "error" in result:
            failed += 1
            state["failed_cells"].append(
                {"cell_id": cid, "error": result["error"]}
            )
            print(f"[04-grid] FAILED cell {cid}: {result['error']}")
        else:
            completed += 1
            state["completed_cells"].append(
                {
                    "cell_id": cid,
                    "alpha_coverage": result.get("alpha_coverage"),
                    "median_pearson_r_pgen": result.get(
                        "median_pearson_r_pgen"
                    ),
                    "wall_seconds_for_cell": result.get(
                        "wall_seconds_for_cell"
                    ),
                }
            )
        update_state(state_path, state)
        elapsed = time.time() - t0
        per_cell = elapsed / max(completed + failed, 1)
        remaining = (len(cells) - completed - failed) * per_cell
        print(
            f"[04-grid] progress: {completed + failed}/{len(cells)}  "
            f"elapsed={elapsed:.0f}s  per-cell={per_cell:.0f}s  "
            f"remaining~{remaining:.0f}s"
        )

    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    state["total_wall_seconds"] = float(time.time() - t0)
    update_state(state_path, state)
    print(
        f"[04-grid] grid run complete: {completed} ok, {failed} failed, "
        f"wall={state['total_wall_seconds']:.0f}s"
    )
    return 0 if failed == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
