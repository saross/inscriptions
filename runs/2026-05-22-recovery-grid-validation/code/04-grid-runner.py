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
This script operates in two modes:

- ``--mode orchestrator`` (default): the parent process. Loads the
  design.json, enumerates the 450 cells, and maintains a pool of up to
  ``--n-jobs`` concurrent subprocesses, each launched in
  ``--mode cell-worker`` to process one cell. Persists
  ``grid-state.json`` after each cell completes.
- ``--mode cell-worker``: child process. Generates all replicates for
  one cell, fits each, aggregates the per-cell summary. The
  subprocess-based parallelism (rather than joblib/loky) was adopted
  after benchmark testing showed loky-based concurrency inflated
  per-fit wall by 3-5x (likely shared pytensor compile-state across
  worker processes), whereas independent subprocess launches preserved
  near-isolated per-fit timings.

Resumability
------------
After each cell completes (all replicates fit + per-cell summary
written) the orchestrator updates ``outputs/grid-state.json``. On
restart, the orchestrator skips any cell whose per-cell-summary JSON
already exists. The grid is resumable at cell granularity.

Single-threaded BLAS
--------------------
Each cell-worker inherits ``OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=
MKL_NUM_THREADS=1`` from the parent's environment, preventing
oversubscription on a 24-core box when n_jobs is high.

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
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

# Cap BLAS / OpenMP threads to 1 in the parent process AND propagate to
# subprocesses via inheritance. Without this, pymc / numpy / pytensor
# auto-detect all 24 cores and 20 parallel cell-workers oversubscribe
# the box, blowing per-fit wall from ~14 s to ~100 s.
_BLAS_THREAD_VARS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
for _v in _BLAS_THREAD_VARS:
    os.environ.setdefault(_v, "1")

_THIS_DIR = Path(__file__).resolve().parent
_THIS_SCRIPT = Path(__file__).resolve()


def _load_sibling(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(
        module_name, _THIS_DIR / filename
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {filename}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Cell-worker mode: process one cell end-to-end.
# ---------------------------------------------------------------------------
def cell_worker_main(args: argparse.Namespace) -> int:
    """Single-cell worker. Generates all replicates, fits each, aggregates.

    Returns 0 on success; non-zero on failure. Writes the per-cell
    summary to ``outputs/cell-summaries/<cell_id>-summary.json`` as a
    side effect — the orchestrator looks for this file to determine
    success.
    """
    try:
        synth_gen = _load_sibling(
            "01-synthetic-cell-generator.py", "synth_gen"
        )
        fit_mod = _load_sibling("02-cell-mixture-fit.py", "fit_mod")
        agg_mod = _load_sibling("03-cell-aggregator.py", "agg_mod")

        design = synth_gen.load_design(args.design_json)
        env = synth_gen.make_envelope(design)
        tier_basis = synth_gen.build_tier_basis(design, env)

        all_cells = synth_gen.enumerate_grid_cells(design)
        if args.cell_index < 0 or args.cell_index >= len(all_cells):
            print(
                f"[cell-worker] cell_index {args.cell_index} out of range",
                file=sys.stderr,
            )
            return 2
        cell = all_cells[args.cell_index]
        cell_id = cell["cell_id"]

        # Resumability check.
        summary_path = (
            args.output_root / "outputs" / "cell-summaries"
            / f"{cell_id}-summary.json"
        )
        if summary_path.exists() and not args.force:
            print(f"[cell-worker] cell {cell_id} already complete; skipping.")
            return 0

        t_start = time.time()
        for r in range(args.n_replicates):
            synth_path = (
                args.output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.parquet"
            )
            truth_path = (
                args.output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.truth.json"
            )
            if not (synth_path.exists() and truth_path.exists()):
                synth_gen.generate_replicate(
                    cell, r, int(design["base_seed"]), env, tier_basis,
                    args.output_root,
                )
            posterior_json = (
                args.output_root / "outputs" / "cell-fits" / cell_id
                / f"replicate_{r:03d}-posterior.json"
            )
            if not posterior_json.exists():
                fit_mod.fit_replicate(
                    cell_id=cell_id,
                    replicate=r,
                    output_root=args.output_root,
                    design=design,
                    tier_basis=tier_basis,
                    n_draws=args.n_draws,
                    n_tune=args.n_tune,
                    n_chains=args.n_chains,
                    target_accept=args.target_accept,
                    cores=args.cores,
                    progressbar=False,
                )
        aggregate = agg_mod.aggregate_cell(
            cell_id, args.output_root, write=True
        )
        wall = time.time() - t_start
        aggregate["wall_seconds_for_cell"] = float(wall)
        print(
            f"[cell-worker] cell {cell_id} OK: "
            f"alpha_cov={aggregate['alpha_coverage']:.2f}  "
            f"median_r={aggregate['median_pearson_r_pgen']:.3f}  "
            f"wall={wall:.0f}s"
        )
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[cell-worker] ERROR cell_index={args.cell_index}: {exc}",
              file=sys.stderr)
        traceback.print_exc()
        return 3


# ---------------------------------------------------------------------------
# Orchestrator mode: pool of subprocess cell-workers.
# ---------------------------------------------------------------------------
def update_state(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(state_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    tmp.replace(state_path)


def orchestrator_main(args: argparse.Namespace) -> int:
    synth_gen = _load_sibling("01-synthetic-cell-generator.py", "synth_gen")
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
        f"[orch] launching grid: {len(cells)} cells x "
        f"{n_replicates} replicates; n_jobs={args.n_jobs}; "
        f"cores_per_fit={args.cores}; n_chains={args.n_chains}; "
        f"n_draws={args.n_draws}; n_tune={args.n_tune}; "
        f"target_accept={args.target_accept}"
    )
    t0 = time.time()

    # Subprocess pool: a dict from popen-handle to cell metadata.
    inflight: dict[subprocess.Popen[bytes], dict[str, Any]] = {}
    queue = list(cells)
    completed = 0
    failed = 0

    def launch_one(cell: dict[str, Any]) -> subprocess.Popen[bytes]:
        # Each worker is a subprocess invocation of this same script
        # in --mode cell-worker.
        cmd = [
            sys.executable,
            str(_THIS_SCRIPT),
            "--mode", "cell-worker",
            "--design-json", str(args.design_json),
            "--output-root", str(args.output_root),
            "--cell-index", str(cell["cell_index"]),
            "--n-replicates", str(n_replicates),
            "--n-draws", str(args.n_draws),
            "--n-tune", str(args.n_tune),
            "--n-chains", str(args.n_chains),
            "--target-accept", str(args.target_accept),
            "--cores", str(args.cores),
        ]
        log_dir = args.output_root / "outputs" / "cell-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"{cell['cell_id']}.log"
        log_fh = log_path.open("w", encoding="utf-8")
        proc = subprocess.Popen(
            cmd,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
            cwd=os.getcwd(),
        )
        inflight[proc] = {"cell": cell, "log_fh": log_fh, "log_path": log_path}
        return proc

    while queue or inflight:
        # Top up to n_jobs in-flight workers.
        while queue and len(inflight) < args.n_jobs:
            launch_one(queue.pop(0))

        # Poll for completion. Use a short wait to keep the loop tight
        # without busy-spinning.
        done = []
        for proc in list(inflight.keys()):
            rc = proc.poll()
            if rc is not None:
                done.append((proc, rc))
        if not done:
            time.sleep(2)
            continue

        for proc, rc in done:
            meta = inflight.pop(proc)
            meta["log_fh"].close()
            cell = meta["cell"]
            cid = cell["cell_id"]
            summary_path = (
                args.output_root / "outputs" / "cell-summaries"
                / f"{cid}-summary.json"
            )
            if rc == 0 and summary_path.exists():
                completed += 1
                with summary_path.open("r", encoding="utf-8") as fh:
                    summary = json.load(fh)
                state["completed_cells"].append(
                    {
                        "cell_id": cid,
                        "alpha_coverage": summary.get("alpha_coverage"),
                        "median_pearson_r_pgen": summary.get(
                            "median_pearson_r_pgen"
                        ),
                        "mean_fit_seconds": summary.get("mean_fit_seconds"),
                    }
                )
            else:
                failed += 1
                state["failed_cells"].append(
                    {
                        "cell_id": cid,
                        "returncode": rc,
                        "log_path": str(meta["log_path"]),
                    }
                )
                print(
                    f"[orch] FAILED cell {cid}: rc={rc}; "
                    f"see {meta['log_path']}"
                )
            update_state(state_path, state)
            elapsed = time.time() - t0
            total_done = completed + failed
            per_cell = elapsed / max(total_done, 1)
            remaining_cells = (len(cells) - total_done)
            # Account for the n_jobs concurrency in the remaining estimate.
            remaining_s = (remaining_cells * per_cell) / max(
                args.n_jobs, 1
            ) if remaining_cells > 0 else 0
            print(
                f"[orch] progress: {total_done}/{len(cells)}  "
                f"completed={completed}  failed={failed}  "
                f"elapsed={elapsed:.0f}s  per-cell={per_cell:.0f}s  "
                f"remaining~{remaining_s:.0f}s "
                f"({remaining_s / 3600:.2f}h)"
            )

    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    state["total_wall_seconds"] = float(time.time() - t0)
    update_state(state_path, state)
    print(
        f"[orch] grid run complete: {completed} ok, {failed} failed, "
        f"wall={state['total_wall_seconds']:.0f}s "
        f"({state['total_wall_seconds'] / 3600:.2f}h)"
    )
    return 0 if failed == 0 else 3


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="H2.1 recovery-grid orchestrator + worker."
    )
    parser.add_argument(
        "--mode", choices=("orchestrator", "cell-worker"),
        default="orchestrator",
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--n-jobs", type=int, default=20)
    parser.add_argument(
        "--n-replicates", type=int, default=None,
        help="Override design.json replicates_per_cell.",
    )
    parser.add_argument(
        "--cells-limit", type=int, default=None,
        help="Process only the first N cells (smoke test).",
    )
    parser.add_argument("--n-draws", type=int, default=2000)
    parser.add_argument("--n-tune", type=int, default=1000)
    parser.add_argument("--n-chains", type=int, default=4)
    parser.add_argument("--target-accept", type=float, default=0.95)
    parser.add_argument("--cores", type=int, default=1)
    # Cell-worker-only.
    parser.add_argument(
        "--cell-index", type=int, default=-1,
        help="(cell-worker mode) which cell to process (0-based index "
        "into the deterministic grid enumeration).",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="(cell-worker mode) re-run even if the per-cell summary "
        "already exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.mode == "cell-worker":
        if args.cell_index < 0:
            print(
                "ERROR: --cell-index is required in cell-worker mode.",
                file=sys.stderr,
            )
            return 2
        if args.n_replicates is None:
            print(
                "ERROR: --n-replicates is required in cell-worker mode.",
                file=sys.stderr,
            )
            return 2
        return cell_worker_main(args)
    return orchestrator_main(args)


if __name__ == "__main__":
    sys.exit(main())
