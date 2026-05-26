#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-grid.py
===========

Top-level orchestrator for **one** grid of the 2026-05-26 two-unit
recovery-grid re-simulation. Selects between Grid A (inscription-mass)
and Grid B (letter-mass conservative) via ``--unit``. Iterates the 450
cells (= 5 alpha x 6 shapes x 5 tier x 3 N) and within each cell runs
``--n-replicates`` (default 100) replicates end-to-end (synthesise -> fit
-> aggregate). Resumable at cell granularity: cells whose
per-cell-summary JSON already exists are skipped.

Operates in two modes:

- ``--mode orchestrator`` (default): the parent process. Loads the
  design.json, enumerates 450 cells, maintains a pool of up to
  ``--n-jobs`` cell-worker subprocesses, persists ``grid-state.json``
  after each cell completes.
- ``--mode cell-worker``: child process for one cell.

Spec lineage
------------
- §3.1 — F1+F3 baked in via ``cell_lib.build_model_f1_f3``.
- §3.3 — pilot_proxy override: inscription uses the design.json default
  (0.55, 0.30, 0.15); letter loads the re-derived vector from
  ``letter-mass/data/pilot-proxy.json`` written by
  ``derive-pilot-proxy.py``.
- §3.5 — per-grid base seeds (20260526 / 20260527).
- §6 — sapphire concurrency: ``--n-jobs 12`` under
  ``taskset -c 0-11``, ``cores 1`` per fit.

Usage
-----
    python run-grid.py \\
        --unit inscription \\
        --design-json /path/to/2026-05-22-recovery-grid-design/design.json \\
        --run-root /path/to/runs/2026-05-26-recovery-grid-two-unit \\
        --letter-parquet /path/to/lire-filtered-with-letters.parquet \\
        --n-jobs 12 \\
        [--n-replicates 100] \\
        [--cells-limit N]    (smoke-test slicing)

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any

# Cap BLAS / OpenMP threads to 1 — propagated to child subprocesses via
# os.environ inheritance. Without this, pymc/numpy/pytensor auto-detect
# all 24 cores and 12 cell-workers oversubscribe sapphire.
_BLAS_THREAD_VARS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "NUMBA_NUM_THREADS",
)
for _v in _BLAS_THREAD_VARS:
    os.environ.setdefault(_v, "1")

os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN,allow_gc=False")

_THIS_DIR = Path(__file__).resolve().parent
_THIS_SCRIPT = Path(__file__).resolve()
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

# Per-grid base seeds (spec §3.5).
BASE_SEED_INSCRIPTION = 20_260_526
BASE_SEED_LETTER = 20_260_527

# Inscription-mass pilot_proxy is the 2026-05-22 value (spec §3.3).
PILOT_PROXY_INSCRIPTION = (0.55, 0.30, 0.15)


def grid_subdir(unit: str) -> str:
    """Return the per-grid subdir name."""
    return "inscription-mass" if unit == "inscription" else "letter-mass"


def base_seed_for(unit: str) -> int:
    return BASE_SEED_INSCRIPTION if unit == "inscription" else BASE_SEED_LETTER


def pilot_proxy_for(unit: str, output_root: Path) -> tuple[float, float, float]:
    """Resolve the pilot_proxy tier vector for the requested grid.

    - inscription: hard-pinned to (0.55, 0.30, 0.15). The value is
      written to ``output_root / data / pilot-proxy.json`` at launch for
      record-preservation symmetry with the letter grid.
    - letter: loaded from
      ``output_root / data / pilot-proxy.json`` (re-derived by the
      pre-launch ``derive-pilot-proxy.py`` script; spec §3.3).
    """
    if unit == "inscription":
        w = PILOT_PROXY_INSCRIPTION
        out_json = output_root / "data" / "pilot-proxy.json"
        out_json.parent.mkdir(parents=True, exist_ok=True)
        if not out_json.exists():
            with out_json.open("w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "unit": "inscription",
                        "weights": list(w),
                        "tier_order": ["century", "half_century", "reign"],
                        "anchor": (
                            "2026-05-22 design.json pilot_proxy; "
                            "endpoint-frequency descriptive "
                            "(Decision 17 lines 1314-1316)."
                        ),
                    },
                    fh,
                    indent=2,
                )
        return w
    # letter
    js = output_root / "data" / "pilot-proxy.json"
    if not js.exists():
        raise FileNotFoundError(
            f"Missing letter-mass pilot-proxy.json at {js}. "
            "Run derive-pilot-proxy.py before launching Grid B."
        )
    with js.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    w = tuple(float(x) for x in d["weights"])
    if len(w) != 3:
        raise ValueError(
            f"pilot-proxy.json weights must have length 3; got {w!r}"
        )
    return w  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Cell-worker mode: process one cell end-to-end.
# ---------------------------------------------------------------------------
def cell_worker_main(args: argparse.Namespace) -> int:
    """Generate all replicates for one cell, fit each, aggregate."""
    try:
        from cell_lib import (
            build_tier_basis,
            enumerate_grid_cells,
            load_design,
            load_letter_count_distribution,
            make_envelope,
        )
        from synth import generate_replicate
        from fit import fit_replicate
        from aggregate import aggregate_cell

        design = load_design(args.design_json)
        env = make_envelope(design)
        tier_basis = build_tier_basis(design, env)

        output_root = args.run_root / grid_subdir(args.unit)

        # Resolve pilot_proxy for this grid before enumerating cells.
        pp = pilot_proxy_for(args.unit, output_root)
        all_cells = enumerate_grid_cells(design, pilot_proxy_weights=pp)
        if args.cell_index < 0 or args.cell_index >= len(all_cells):
            print(
                f"[cell-worker] cell_index {args.cell_index} out of range",
                file=sys.stderr,
            )
            return 2
        cell = all_cells[args.cell_index]
        cell_id = cell["cell_id"]

        summary_path = (
            output_root / "outputs" / "cell-summaries"
            / f"{cell_id}-summary.json"
        )
        if summary_path.exists() and not args.force:
            print(f"[cell-worker] cell {cell_id} already complete; skipping.")
            return 0

        # Load letter distribution if needed.
        letter_dist = None
        if args.unit == "letter":
            letter_dist = load_letter_count_distribution(args.letter_parquet)

        base_seed = base_seed_for(args.unit)

        t_start = time.time()
        for r in range(args.n_replicates):
            synth_path = (
                output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.parquet"
            )
            truth_path = (
                output_root / "data" / "synthetic-cells" / cell_id
                / f"replicate_{r:03d}.truth.json"
            )
            if not (synth_path.exists() and truth_path.exists()):
                generate_replicate(
                    cell, r, base_seed, env, tier_basis,
                    output_root, args.unit, letter_dist=letter_dist,
                )
            posterior_json = (
                output_root / "outputs" / "cell-fits" / cell_id
                / f"replicate_{r:03d}-posterior.json"
            )
            if not posterior_json.exists():
                fit_replicate(
                    cell_id=cell_id,
                    replicate=r,
                    output_root=output_root,
                    env=env,
                    tier_basis=tier_basis,
                    n_draws=args.n_draws,
                    n_tune=args.n_tune,
                    n_chains=args.n_chains,
                    target_accept=args.target_accept,
                    cores=args.cores,
                    progressbar=False,
                )
        aggregate = aggregate_cell(cell_id, output_root, write=True)
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
# Orchestrator mode.
# ---------------------------------------------------------------------------
def update_state(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(state_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    tmp.replace(state_path)


def orchestrator_main(args: argparse.Namespace) -> int:
    from cell_lib import enumerate_grid_cells, load_design

    output_root = args.run_root / grid_subdir(args.unit)

    design = load_design(args.design_json)
    n_replicates = (
        args.n_replicates
        if args.n_replicates is not None
        else int(design["replicates_per_cell"])
    )

    # Resolve pilot_proxy (so the enumeration the orchestrator sees
    # matches what the workers will compute).
    pp = pilot_proxy_for(args.unit, output_root)
    cells = enumerate_grid_cells(design, pilot_proxy_weights=pp)
    if args.cells_limit is not None:
        cells = cells[: args.cells_limit]
    if args.cell_indices:
        idx_set = set(int(s) for s in args.cell_indices.split(","))
        cells = [c for c in cells if c["cell_index"] in idx_set]

    state_path = output_root / "outputs" / "grid-state.json"
    state: dict[str, Any] = {
        "unit": args.unit,
        "base_seed": base_seed_for(args.unit),
        "pilot_proxy": list(pp),
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
        f"[orch] unit={args.unit} launching grid: {len(cells)} cells x "
        f"{n_replicates} replicates; n_jobs={args.n_jobs}; "
        f"cores_per_fit={args.cores}; n_chains={args.n_chains}; "
        f"n_draws={args.n_draws}; n_tune={args.n_tune}; "
        f"target_accept={args.target_accept}",
        flush=True,
    )
    t0 = time.time()

    inflight: dict[subprocess.Popen[bytes], dict[str, Any]] = {}
    queue = list(cells)
    completed = 0
    failed = 0

    def launch_one(cell: dict[str, Any]) -> subprocess.Popen[bytes]:
        cmd = [
            sys.executable,
            str(_THIS_SCRIPT),
            "--mode", "cell-worker",
            "--unit", args.unit,
            "--design-json", str(args.design_json),
            "--run-root", str(args.run_root),
            "--cell-index", str(cell["cell_index"]),
            "--n-replicates", str(n_replicates),
            "--n-draws", str(args.n_draws),
            "--n-tune", str(args.n_tune),
            "--n-chains", str(args.n_chains),
            "--target-accept", str(args.target_accept),
            "--cores", str(args.cores),
        ]
        if args.letter_parquet is not None:
            cmd += ["--letter-parquet", str(args.letter_parquet)]
        log_dir = output_root / "outputs" / "cell-logs"
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
        inflight[proc] = {
            "cell": cell, "log_fh": log_fh, "log_path": log_path,
        }
        return proc

    while queue or inflight:
        while queue and len(inflight) < args.n_jobs:
            launch_one(queue.pop(0))

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
                output_root / "outputs" / "cell-summaries"
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
                    f"see {meta['log_path']}",
                    flush=True,
                )
            update_state(state_path, state)
            elapsed = time.time() - t0
            total_done = completed + failed
            per_cell = elapsed / max(total_done, 1)
            remaining_cells = (len(cells) - total_done)
            remaining_s = (
                (remaining_cells * per_cell) / max(args.n_jobs, 1)
                if remaining_cells > 0
                else 0
            )
            print(
                f"[orch] {args.unit} progress: {total_done}/{len(cells)}  "
                f"completed={completed}  failed={failed}  "
                f"elapsed={elapsed:.0f}s  per-cell={per_cell:.0f}s  "
                f"remaining~{remaining_s:.0f}s "
                f"({remaining_s / 3600:.2f}h)",
                flush=True,
            )

    state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    state["total_wall_seconds"] = float(time.time() - t0)
    update_state(state_path, state)
    print(
        f"[orch] {args.unit} grid run complete: "
        f"{completed} ok, {failed} failed, "
        f"wall={state['total_wall_seconds']:.0f}s "
        f"({state['total_wall_seconds'] / 3600:.2f}h)",
        flush=True,
    )
    return 0 if failed == 0 else 3


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Two-unit recovery-grid orchestrator + worker."
    )
    parser.add_argument(
        "--mode", choices=("orchestrator", "cell-worker"),
        default="orchestrator",
    )
    parser.add_argument(
        "--unit", required=True, choices=("inscription", "letter"),
        help=(
            "Selects Grid A (inscription-mass) or Grid B "
            "(letter-mass conservative)."
        ),
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument(
        "--run-root", required=True, type=Path,
        help="Parent runs/2026-05-26-recovery-grid-two-unit/ directory.",
    )
    parser.add_argument(
        "--letter-parquet", type=Path, default=None,
        help=(
            "Path to lire-filtered-with-letters.parquet "
            "(required for --unit letter)."
        ),
    )
    parser.add_argument("--n-jobs", type=int, default=12)
    parser.add_argument(
        "--n-replicates", type=int, default=None,
        help="Override design.json replicates_per_cell.",
    )
    parser.add_argument(
        "--cells-limit", type=int, default=None,
        help="Process only the first N cells (smoke test).",
    )
    parser.add_argument(
        "--cell-indices", type=str, default=None,
        help="Comma-separated cell_index list (smoke-test cell selector).",
    )
    parser.add_argument("--n-draws", type=int, default=2000)
    parser.add_argument("--n-tune", type=int, default=1000)
    parser.add_argument("--n-chains", type=int, default=4)
    parser.add_argument("--target-accept", type=float, default=0.95)
    parser.add_argument("--cores", type=int, default=1)
    parser.add_argument(
        "--cell-index", type=int, default=-1,
        help="(cell-worker mode) which cell to process.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="(cell-worker mode) re-run even if summary already exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.unit == "letter" and args.letter_parquet is None:
        print(
            "ERROR: --letter-parquet is required when --unit letter.",
            file=sys.stderr,
        )
        return 2
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
