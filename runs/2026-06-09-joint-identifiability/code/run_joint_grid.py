#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_joint_grid.py — orchestrator for the joint-model recovery-validation grid.
==============================================================================

Fits the LEAD model (`build_model_joint`, per-unit ESTIMATED basis + κ=40 θ priors) on
every cell × replicate (`grid_lib.enumerate_cells`), in parallel over cells, resumable at
cell granularity. On **confounded** cells it also fits the shared-basis baseline
(`build_model_f1_f3`, temporal only — the under-attributing reference) so the grid itself
demonstrates the lead is *materially better than baseline* (acceptance criterion C2,
`full-grid-spec.md` §3). Per replicate it records the α posterior median + 95 % CI +
convergence; per cell it aggregates bias / coverage / convergence **over the converged
replicates** (non-converged CIs are not trustworthy). Cross-cell scoring is a separate
step (`aggregate_joint_grid.py`).

Robustness (post-audit 2026-06-09): atomic per-cell writes (`os.replace`), validity-gated
resume (a cell is "done" only if its JSON parses AND has ≥ 1 usable replicate), and
crashed-worker isolation (one dead worker does not abort the run).

Memory safety (2026-06-10, after a 60+ GB OOM that aborted the first full run at 10/300
cells): the pool uses the **spawn** start method with `max_tasks_per_child` (default 1) so
each worker is recycled after every cell — its PyMC / PyTensor allocations are returned to
the OS instead of accumulating across cells (the proximate cause of the OOM was long-lived
fork workers never releasing memory). Within a cell, `gc.collect()` runs after every
replicate, and the old `allow_gc=False` PyTensor flag is **no longer used** (it traded
memory for a little speed and fed the leak). Point `TMPDIR` at a root-filesystem directory
(NOT the inode-limited `/tmp` tmpfs) — the PyTensor compile stack leaks small temp files
there and exhausted the tmpfs inode table on a prior multi-day run.

Usage
-----
    PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN \
    taskset -c 0-11 uv run python code/run_joint_grid.py \
        --n-jobs 12 [--max-tasks-per-child 1] [--n-reps 100] \
        [--cells-limit N] [--cell-stride S]

`--cells-limit` / `--cell-stride` / `--n-reps` are for SMOKE-TESTING (a tiny slice
end-to-end). The full run uses the defaults (100 reps, all 300 cells).

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
CELL_LIB_DIR = (
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
    "/revalidation/code"
)
DESIGN_JSON = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign/design.json"
)
sys.path.insert(0, str(RUN / "code"))
sys.path.insert(0, CELL_LIB_DIR)
import joint_lib as J  # noqa: E402
import grid_lib as G  # noqa: E402
from cell_lib import build_model_f1_f3, convergence_pass  # noqa: E402  (validated baseline + gate)

GRID_DIR = RUN / "outputs" / "grid"
STATUS_PATH = RUN / "outputs" / "grid-STATUS.txt"

# θ priors (calibration rule C, κ=40) and the shared Latin baseline basis — loaded once.
_cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())["calibration"]["C"]
THETA_CONV_AB = J.beta_from_mean_concentration(_cal["theta_conv"], G.THETA_PRIOR_KAPPA)
THETA_GEN_AB = J.beta_from_mean_concentration(_cal["theta_gen"], G.THETA_PRIOR_KAPPA)
LATIN_BASIS = np.asarray(
    json.loads(DESIGN_JSON.read_text())["tier_basis_empirical_latin"], dtype=float
)


def _alpha_from_idata(idata, var_names) -> dict:
    import arviz as az
    a = idata.posterior["alpha"].values.reshape(-1)
    summ = az.summary(idata, var_names=var_names, round_to="none")
    max_rhat = float(summ["r_hat"].max())
    min_ess = float(summ["ess_bulk"].min())
    return {
        "alpha_med": float(np.median(a)),
        "alpha_lo": float(np.percentile(a, 2.5)),
        "alpha_hi": float(np.percentile(a, 97.5)),
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess,
        "n_div": int(idata.sample_stats["diverging"].values.sum()),
        "converged": bool(convergence_pass(max_rhat, min_ess)),
    }


def fit_joint_on_model(model, y: np.ndarray, k: int, seed: int) -> dict:
    """One LEAD (joint) fit on a PRE-BUILT per-cell model, swapping this replicate's
    (y, k) via pm.set_data → α median/CI + convergence (cores=1). Building the model once
    per cell and set_data-ing here — rather than rebuilding it every replicate — keeps the
    PyTensor graph constant so the compiled logp is reused instead of recompiled; that is
    what removes the ~32 MB/fit leak (see MEMORY-FIX-AND-RUN-STATUS.md §3/§5). Replicate
    determinism is unchanged: the only per-fit inputs are (y, k) and the explicit seed."""
    import pymc as pm
    with model:
        pm.set_data({"y_data": np.asarray(y, dtype="int64"),
                     "k_data": np.asarray(int(k), dtype="int64")})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=G.DRAWS, tune=G.TUNE, chains=G.CHAINS, cores=1,
                              target_accept=G.TACC, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    return _alpha_from_idata(idata, ["alpha", "tier_weights", "sigma_smooth",
                                     "z_pgen", "theta_conv", "theta_gen"])


def fit_baseline(y: np.ndarray, seed: int) -> dict:
    """Shared-basis temporal-only baseline (the under-attributing reference)."""
    import pymc as pm
    model = build_model_f1_f3(y, LATIN_BASIS)
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=G.DRAWS, tune=G.TUNE, chains=G.CHAINS, cores=1,
                              target_accept=G.TACC, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    return _alpha_from_idata(idata, ["alpha", "tier_weights", "sigma_smooth", "z_pgen"])


def run_cell(cell: dict, n_reps: int) -> dict:
    """Fit all replicates of one cell and aggregate over the converged replicates."""
    p_conv, p_gen = G.cell_shapes(cell)
    basis = G.estimated_basis(p_conv, p_gen, cell["alpha_true"])
    a_true = cell["alpha_true"]
    is_conf = cell["regime"] == "confounded"
    # Build the joint model ONCE for this cell; each replicate's (y, k) is swapped via
    # pm.set_data inside fit_joint_on_model (no per-fit rebuild → no recompile leak). The
    # rep-0 draw is only the initial placeholder data; every replicate then set_data's its
    # own draw, so results are identical to building a fresh model per replicate.
    y0, k0 = G.generate(cell, p_conv, p_gen, 0)
    joint_model = J.build_model_joint(y0, k0, cell["N"], basis, THETA_CONV_AB, THETA_GEN_AB)
    reps = []
    for r in range(n_reps):
        y, k = G.generate(cell, p_conv, p_gen, r)
        data_seed = (G.BASE_SEED + cell["cell_index"]) * 1000 + r
        rec: dict = {"rep": r, "k_frac": round(k / cell["N"], 4)}
        try:
            res = fit_joint_on_model(joint_model, y, k, data_seed + 500_000)
            res["bias"] = res["alpha_med"] - a_true
            res["cover95"] = bool(res["alpha_lo"] <= a_true <= res["alpha_hi"])
            rec["joint"] = res
        except Exception as exc:  # noqa: BLE001
            rec["joint_error"] = repr(exc)[:200]
        if is_conf:
            try:
                b = fit_baseline(y, data_seed + 700_000)
                b["bias"] = b["alpha_med"] - a_true
                rec["baseline"] = b
            except Exception as exc:  # noqa: BLE001
                rec["baseline_error"] = repr(exc)[:200]
        reps.append(rec)
        # Reclaim this replicate's idata (and, on confounded cells, the per-rep baseline
        # model, which is still rebuilt) now rather than letting it accumulate across the
        # loop. The joint model is built once per cell + reused via set_data, so the dominant
        # per-fit recompile leak is gone; this gc.collect() is belt-and-braces for the rest.
        gc.collect()

    # Aggregate the LEAD over CONVERGED replicates (fall back to all-ok if none converged).
    ok = [x["joint"] for x in reps if "joint" in x]
    conv = [j for j in ok if j["converged"]]
    base_set = conv if conv else ok
    biases = np.array([j["bias"] for j in base_set]) if base_set else np.array([])
    base_fits = [x["baseline"] for x in reps if "baseline" in x]
    base_biases = np.array([b["bias"] for b in base_fits]) if base_fits else np.array([])

    out = {
        **{kk: cell[kk] for kk in ("cell_index", "cell_id", "recipe", "conv_pct_win",
                                   "alpha_true", "gen_name", "gen_pct_win", "N", "regime")},
        "n_reps": n_reps,
        "n_ok": len(ok),
        "n_converged": len(conv),
        "n_failed": n_reps - len(ok),
        "agg_over": "converged" if conv else ("ok" if ok else "none"),
        "alpha_med_mean": float(np.mean([j["alpha_med"] for j in base_set])) if base_set else None,
        "bias_mean": float(np.mean(biases)) if base_set else None,
        "bias_median": float(np.median(biases)) if base_set else None,
        "abs_bias_mean": float(np.mean(np.abs(biases))) if base_set else None,
        "coverage_rate": float(np.mean([j["cover95"] for j in base_set])) if base_set else None,
        "convergence_rate": float(len(conv) / len(ok)) if ok else None,
        "mean_n_div": float(np.mean([j["n_div"] for j in ok])) if ok else None,
        # shared-basis baseline (confounded cells only) — the "materially better" reference
        "baseline_n_ok": len(base_fits),
        "baseline_bias_median": float(np.median(base_biases)) if base_fits else None,
        "baseline_abs_bias_median": float(np.median(np.abs(base_biases))) if base_fits else None,
        "reps": reps,
    }
    return out


def _worker(args: tuple) -> tuple[int, str, int, int]:
    cell, n_reps = args
    out = run_cell(cell, n_reps)
    # Atomic write: tmp in the same dir, then os.replace (POSIX-atomic).
    final = GRID_DIR / f"{cell['cell_id']}.json"
    tmp = GRID_DIR / f"{cell['cell_id']}.json.tmp"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, final)
    return cell["cell_index"], cell["cell_id"], out["n_ok"], out["n_failed"]


def cell_is_done(cell: dict) -> bool:
    """Resume gate: a cell counts as done only if its JSON parses AND has >= 1 usable
    replicate (so a truncated or all-failed file is re-run, not silently frozen)."""
    p = GRID_DIR / f"{cell['cell_id']}.json"
    if not p.exists():
        return False
    try:
        d = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return bool(d.get("n_ok", 0) > 0)


def write_status(done: int, total: int, t0: float, slice_note: str, extra: str = "") -> None:
    el = time.time() - t0
    rate = done / el if el > 0 else 0.0
    eta = (total - done) / rate if rate > 0 else float("inf")
    STATUS_PATH.write_text(
        f"joint recovery grid — {done}/{total} cells done{slice_note}\n"
        f"elapsed {el/3600:.2f} h · rate {rate*3600:.1f} cells/h · "
        f"ETA {eta/3600:.2f} h\n{extra}\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-jobs", type=int, default=12)
    ap.add_argument("--max-tasks-per-child", type=int, default=1,
                    help="recycle each worker process after this many cells to bound "
                         "memory (forces the 'spawn' start method; 1 = freshest / safest)")
    ap.add_argument("--n-reps", type=int, default=G.N_REPS_DEFAULT)
    ap.add_argument("--cells-limit", type=int, default=None, help="smoke-test: first N cells")
    ap.add_argument("--cell-stride", type=int, default=1, help="smoke-test: every Sth cell")
    args = ap.parse_args()

    GRID_DIR.mkdir(parents=True, exist_ok=True)
    cells = G.enumerate_cells()
    if args.cell_stride > 1:
        cells = cells[:: args.cell_stride]
    if args.cells_limit is not None:
        cells = cells[: args.cells_limit]
    is_slice = (args.cell_stride > 1) or (args.cells_limit is not None) or (args.n_reps != G.N_REPS_DEFAULT)
    slice_note = (f"  [SMOKE slice: stride={args.cell_stride} limit={args.cells_limit} "
                  f"reps={args.n_reps}]" if is_slice else "")

    todo = [c for c in cells if not cell_is_done(c)]
    total = len(cells)
    done = total - len(todo)
    print(f"grid: {total} cells ({len(todo)} to do, {done} cached); "
          f"{args.n_reps} reps; n_jobs {args.n_jobs}{slice_note}", flush=True)
    write_status(done, total, time.time(), slice_note, "starting")
    if not todo:
        print("nothing to do (all cached).")
        return

    t0 = time.time()
    failed_cells: list[str] = []
    # spawn + max_tasks_per_child: each worker is replaced after `max_tasks_per_child`
    # cells, so PyMC / PyTensor memory is released to the OS instead of accumulating (the
    # 2026-06-09 run OOM'd at 60+ GB with long-lived fork workers). spawn is mandatory here
    # — ProcessPoolExecutor forbids max_tasks_per_child with the default fork context.
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, (c, args.n_reps)): c for c in todo}
        for fut in as_completed(futs):
            cell = futs[fut]
            try:
                ci, cid, n_ok, n_failed = fut.result()
                done += 1
                flag = f" ({n_failed} rep-fails)" if n_failed else ""
                print(f"[{done}/{total}] {cid}  n_ok={n_ok}{flag}", flush=True)
            except BrokenProcessPool:
                print("FATAL: process pool broken (host OOM / killed) — stopping; "
                      "resume re-runs unfinished cells.", flush=True)
                write_status(done, total, t0, slice_note, "ABORTED: BrokenProcessPool")
                raise
            except Exception as exc:  # noqa: BLE001 — one bad cell must not kill the run
                failed_cells.append(cell["cell_id"])
                print(f"WORKER-ERROR {cell['cell_id']}: {repr(exc)[:160]} "
                      f"(continuing; cell will re-run on resume)", flush=True)
            if done % max(1, args.n_jobs) == 0 or done == total:
                write_status(done, total, t0, slice_note,
                             f"last batch ok; worker-errors so far: {len(failed_cells)}")
    write_status(done, total, t0, slice_note,
                 f"COMPLETE — worker-errored cells (need resume): {failed_cells}")
    print(f"grid complete. worker-errored cells (re-run on resume): {failed_cells}")


if __name__ == "__main__":
    main()
