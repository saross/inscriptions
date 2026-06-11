#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_cc_grid.py — orchestrator for the CROSS-CLASSIFIED (D-B) recovery grid.
===========================================================================

Fits the cross-classified time × alignment model (`build_model_cross_classified`)
on grid cells × replicates, in parallel over cells, resumable at cell granularity.
Three p_conv arms (`cross-classified-signoff.md` §2): `tiers3` (shared Amendment-03
3-tier basis), `library` (deterministic 19-row slab library), `free` (own GRW).

NO baseline is fit here — the head-to-head reuses the lead grid's per-cell results
(`outputs/grid/<cell_id>.json`, same `y` draws by construction; signoff §3). Scoring
is a separate step (`aggregate_cc_grid.py`).

Inherits the lead runner's solved infrastructure verbatim (run_joint_grid.py):
spawn + `max_tasks_per_child` worker recycling, build-once + `pm.set_data` per
replicate (no per-fit PyTensor recompile leak), atomic per-cell writes, and
validity-gated resume. Point `TMPDIR` at a root-filesystem directory (NOT the
inode-limited `/tmp` tmpfs).

Usage
-----
    PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN \
    taskset -c 0-11 uv run python code/run_cc_grid.py \
        --pconv-mode library [--pilot] [--n-jobs 12] [--max-tasks-per-child 1] \
        [--n-reps 100] [--cells-limit N] [--cell-stride S]

`--pilot` restricts to the 20-cell decision-gate subset (`grid_lib.PILOT_CELL_IDS`),
defaults `--n-reps` to 20 (the signed-off pilot budget), and writes to a separate
`-pilot` output dir so pilot cells never block the full run's resume.
`--cells-limit` / `--cell-stride` / `--n-reps` are for smoke-testing. The resume
gate requires a cached cell to carry >= the requested replicate count, so a
low-rep smoke into either dir cannot silently poison a later pilot or full run.

Author / Date — Claude Code (Fable 5) on Shawn's brief, 2026-06-11. UK/Aus English.
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
from cell_lib import convergence_pass  # noqa: E402  (the validated gate, unchanged)

PCONV_MODES = ("tiers3", "library", "free")
PILOT_N_REPS = 20   # signed-off pilot budget (signoff §5 step 4)

# θ priors (calibration rule C, κ=40) and the shared 3-tier basis — loaded once
# (module level, so spawn workers re-load them cleanly on import).
_cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())["calibration"]["C"]
THETA_CONV_AB = J.beta_from_mean_concentration(_cal["theta_conv"], G.THETA_PRIOR_KAPPA)
THETA_GEN_AB = J.beta_from_mean_concentration(_cal["theta_gen"], G.THETA_PRIOR_KAPPA)
LATIN_BASIS = np.asarray(
    json.loads(DESIGN_JSON.read_text())["tier_basis_empirical_latin"], dtype=float
)


def grid_dir(mode: str, pilot: bool) -> Path:
    return RUN / "outputs" / f"grid-cc-{mode}{'-pilot' if pilot else ''}"


def status_path(mode: str, pilot: bool) -> Path:
    return RUN / "outputs" / f"grid-cc-STATUS-{mode}{'-pilot' if pilot else ''}.txt"


def basis_for(mode: str) -> np.ndarray | None:
    """The p_conv basis for an arm (None for the free-GRW arm)."""
    if mode == "tiers3":
        return LATIN_BASIS
    if mode == "library":
        return G.slab_library_basis()
    return None


def monitored_vars(mode: str) -> list[str]:
    """Convergence-gate variables — the arm's full sampled-parameter set, matching
    the lead's policy (gate over every sampled block, not just alpha)."""
    base = ["alpha", "sigma_smooth", "z_pgen", "theta_conv", "theta_gen"]
    if mode in ("tiers3", "library"):
        return ["alpha", "tier_weights", "sigma_smooth", "z_pgen",
                "theta_conv", "theta_gen"]
    return base + ["sigma_conv", "z_pconv"]


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


def fit_cc_on_model(model, y_al: np.ndarray, y_non: np.ndarray, k: int,
                    seed: int, var_names: list[str]) -> dict:
    """One cc fit on a PRE-BUILT per-cell model, swapping this replicate's
    (y_aligned, y_nonaligned, k) via pm.set_data → α median/CI + convergence
    (cores=1). Build-once + set_data keeps the PyTensor graph constant so the
    compiled logp is reused (the lead's ~32 MB/fit recompile-leak lesson)."""
    import pymc as pm
    # Self-describing failure if a caller ever passes an inconsistent split (the
    # model would otherwise surface it as an opaque -inf-logp SamplingError).
    if int(np.asarray(y_al).sum()) != int(k):
        raise ValueError(f"set_data invariant: y_al sums to {int(np.asarray(y_al).sum())}, "
                         f"not k={k}")
    with model:
        pm.set_data({"y_al_data": np.asarray(y_al, dtype="int64"),
                     "y_non_data": np.asarray(y_non, dtype="int64"),
                     "k_data": np.asarray(int(k), dtype="int64")})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=G.DRAWS, tune=G.TUNE, chains=G.CHAINS, cores=1,
                              target_accept=G.TACC, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    return _alpha_from_idata(idata, var_names)


def run_cell_cc(cell: dict, n_reps: int, mode: str) -> dict:
    """Fit all replicates of one cell under one arm; aggregate over converged reps."""
    p_conv, p_gen = G.cell_shapes(cell)
    basis = basis_for(mode)
    a_true = cell["alpha_true"]
    var_names = monitored_vars(mode)
    # Build the cc model ONCE for this cell; each replicate's data is swapped via
    # pm.set_data inside fit_cc_on_model. Rep-0 data is only the initial placeholder.
    _y0, y_al0, y_non0, k0 = G.generate_cc(cell, p_conv, p_gen, 0)
    model = J.build_model_cross_classified(y_al0, y_non0, k0, cell["N"], basis,
                                           THETA_CONV_AB, THETA_GEN_AB, pconv_mode=mode)
    reps = []
    t_fit0 = time.time()
    for r in range(n_reps):
        _y, y_al, y_non, k = G.generate_cc(cell, p_conv, p_gen, r)
        data_seed = (G.BASE_SEED + cell["cell_index"]) * 1000 + r
        rec: dict = {"rep": r, "k_frac": round(k / cell["N"], 4)}
        try:
            res = fit_cc_on_model(model, y_al, y_non, k,
                                  data_seed + G.CC_FIT_SEED_OFFSET, var_names)
            res["bias"] = res["alpha_med"] - a_true
            res["cover95"] = bool(res["alpha_lo"] <= a_true <= res["alpha_hi"])
            rec["cc"] = res
        except Exception as exc:  # noqa: BLE001
            rec["cc_error"] = repr(exc)[:200]
        reps.append(rec)
        gc.collect()  # belt-and-braces; the recompile leak is gone via set_data

    ok = [x["cc"] for x in reps if "cc" in x]
    conv = [j for j in ok if j["converged"]]
    base_set = conv if conv else ok
    biases = np.array([j["bias"] for j in base_set]) if base_set else np.array([])

    out = {
        **{kk: cell[kk] for kk in ("cell_index", "cell_id", "recipe", "conv_pct_win",
                                   "alpha_true", "gen_name", "gen_pct_win", "N", "regime")},
        "pconv_mode": mode,
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
        "mean_ci_halfwidth": (float(np.mean([(j["alpha_hi"] - j["alpha_lo"]) / 2
                                             for j in base_set])) if base_set else None),
        "secs_per_fit": round((time.time() - t_fit0) / max(1, n_reps), 2),
        "reps": reps,
    }
    return out


def _worker(args: tuple) -> tuple[int, str, int, int]:
    cell, n_reps, mode, pilot = args
    out = run_cell_cc(cell, n_reps, mode)
    gdir = grid_dir(mode, pilot)
    final = gdir / f"{cell['cell_id']}.json"
    tmp = gdir / f"{cell['cell_id']}.json.tmp"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, final)  # atomic
    return cell["cell_index"], cell["cell_id"], out["n_ok"], out["n_failed"]


def cell_is_done(cell: dict, gdir: Path, n_reps: int) -> bool:
    """Resume gate: done only if the JSON parses, has >= 1 usable replicate, AND
    was run at >= the requested replicate count (so a low-rep smoke result can
    never silently satisfy a pilot or full run — audit finding M1)."""
    p = gdir / f"{cell['cell_id']}.json"
    if not p.exists():
        return False
    try:
        d = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return bool(d.get("n_ok", 0) > 0) and int(d.get("n_reps", 0)) >= n_reps


def write_status(spath: Path, done: int, total: int, t0: float,
                 note: str, extra: str = "") -> None:
    el = time.time() - t0
    rate = done / el if el > 0 else 0.0
    eta = (total - done) / rate if rate > 0 else float("inf")
    spath.write_text(
        f"cc recovery grid — {done}/{total} cells done{note}\n"
        f"elapsed {el/3600:.2f} h · rate {rate*3600:.1f} cells/h · "
        f"ETA {eta/3600:.2f} h\n{extra}\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pconv-mode", required=True, choices=PCONV_MODES)
    ap.add_argument("--pilot", action="store_true",
                    help="20-cell decision-gate subset; separate -pilot output dir")
    ap.add_argument("--n-jobs", type=int, default=12)
    ap.add_argument("--max-tasks-per-child", type=int, default=1,
                    help="recycle each worker after this many cells (spawn context)")
    ap.add_argument("--n-reps", type=int, default=None,
                    help="replicates per cell (default: 20 with --pilot, else "
                         f"{G.N_REPS_DEFAULT}) — audit finding M2")
    ap.add_argument("--cells-limit", type=int, default=None, help="smoke-test: first N cells")
    ap.add_argument("--cell-stride", type=int, default=1, help="smoke-test: every Sth cell")
    args = ap.parse_args()
    if args.n_reps is None:
        args.n_reps = PILOT_N_REPS if args.pilot else G.N_REPS_DEFAULT

    gdir = grid_dir(args.pconv_mode, args.pilot)
    spath = status_path(args.pconv_mode, args.pilot)
    gdir.mkdir(parents=True, exist_ok=True)

    cells = G.enumerate_cells()
    if args.pilot:
        pilot_ids = set(G.PILOT_CELL_IDS)
        cells = [c for c in cells if c["cell_id"] in pilot_ids]
        assert len(cells) == len(G.PILOT_CELL_IDS), "pilot cell_id mismatch vs enumeration"
    if args.cell_stride > 1:
        cells = cells[:: args.cell_stride]
    if args.cells_limit is not None:
        cells = cells[: args.cells_limit]
    sanctioned_reps = PILOT_N_REPS if args.pilot else G.N_REPS_DEFAULT
    is_slice = (args.cell_stride > 1) or (args.cells_limit is not None) \
        or (args.n_reps != sanctioned_reps)
    note = (f"  [arm={args.pconv_mode}{' PILOT' if args.pilot else ''}"
            f"{' SMOKE slice' if is_slice else ''} reps={args.n_reps}]")

    todo = [c for c in cells if not cell_is_done(c, gdir, args.n_reps)]
    total = len(cells)
    done = total - len(todo)
    print(f"cc grid [{args.pconv_mode}]: {total} cells ({len(todo)} to do, {done} cached); "
          f"{args.n_reps} reps; n_jobs {args.n_jobs}{note}", flush=True)
    write_status(spath, done, total, time.time(), note, "starting")
    if not todo:
        print("nothing to do (all cached).")
        return

    t0 = time.time()
    failed_cells: list[str] = []
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, (c, args.n_reps, args.pconv_mode, args.pilot)): c
                for c in todo}
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
                write_status(spath, done, total, t0, note, "ABORTED: BrokenProcessPool")
                raise
            except Exception as exc:  # noqa: BLE001 — one bad cell must not kill the run
                failed_cells.append(cell["cell_id"])
                print(f"WORKER-ERROR {cell['cell_id']}: {repr(exc)[:160]} "
                      f"(continuing; cell will re-run on resume)", flush=True)
            if done % max(1, args.n_jobs) == 0 or done == total:
                write_status(spath, done, total, t0, note,
                             f"last batch ok; worker-errors so far: {len(failed_cells)}")
    write_status(spath, done, total, t0, note,
                 f"COMPLETE — worker-errored cells (need resume): {failed_cells}")
    print(f"cc grid [{args.pconv_mode}] complete. worker-errored cells: {failed_cells}")


if __name__ == "__main__":
    main()
