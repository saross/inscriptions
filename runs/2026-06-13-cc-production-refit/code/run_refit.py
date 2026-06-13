#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_refit.py — fit the 29 production units under the cc-library model.
======================================================================

Per unit (spec §3): build the cross-classified observables (refit_lib), fit
``build_model_cross_classified(pconv_mode="library")`` with the FIXED slab library
and the rule-C κ=40 θ priors, and extract α median/CI, the corrected genuine SPA
(H3b hand-off), p_conv/tier_weights medians, PPC adequacy, and convergence. Writes
one JSON per unit; aggregation/verdict is a separate step (aggregate_refit.py).

Small job (29 fits, ~30–130 s each ⇒ well under an hour). Inherits the grid's
solved infra: spawn + max_tasks_per_child worker recycling, root-fs TMPDIR, cgroup
MemoryMax cap (set by the launch wrapper). Resumable at unit granularity (a unit
with a parseable JSON carrying convergence info is skipped).

Usage (sapphire) — PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
    uv run python code/run_refit.py [--n-jobs 8] [--only NAME]

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-13. UK/Aus English.
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

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
CELL_LIB_DIR = (  # the recovery-validated gate lives here; insert explicitly
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
    "/revalidation/code")
sys.path.insert(0, str(REFIT / "code"))
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
sys.path.insert(0, CELL_LIB_DIR)
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402
from cell_lib import convergence_pass  # noqa: E402

UNITS_DIR = REFIT / "outputs" / "units"
STATUS_PATH = REFIT / "outputs" / "refit-STATUS.txt"

# Loaded once at module level (re-imported cleanly by spawn workers).
LIBRARY_BASIS, LIBRARY_SLABS = R.load_library_basis()
THETA_CONV_AB, THETA_GEN_AB, THETA_CAL = R.theta_priors()
MONITORED = ["alpha", "tier_weights", "sigma_smooth", "z_pgen", "theta_conv", "theta_gen"]


def fit_one(unit: dict, data: dict) -> dict:
    """Fit one unit's cc-library model and extract the deliverables (spec §3)."""
    import arviz as az
    import pymc as pm

    n_bins = int(data["y_aligned"].size)
    model = J.build_model_cross_classified(
        data["y_aligned"], data["y_nonaligned"], data["k"], data["n_rows"],
        LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB, pconv_mode="library")
    seed = R.REFIT_BASE_SEED + unit["unit_index"]
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                              target_accept=H.TARGET_ACCEPT, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
            ppc = pm.sample_posterior_predictive(idata, progressbar=False, random_seed=seed)

    summ = az.summary(idata, var_names=MONITORED, round_to="none")
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    min_ess_tail = float(summ["ess_tail"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    a = idata.posterior["alpha"].values.reshape(-1)
    alpha_med = float(np.median(a))
    alpha_lo, alpha_hi = (float(x) for x in np.percentile(a, [2.5, 97.5]))

    p_gen = idata.posterior["p_gen"].values.reshape(-1, n_bins)
    p_gen_med = np.median(p_gen, axis=0)
    p_gen_med_norm = p_gen_med / p_gen_med.sum() if p_gen_med.sum() > 0 else p_gen_med
    p_conv_med = np.median(idata.posterior["p_conv"].values.reshape(-1, n_bins), axis=0)
    tw_med = np.median(
        idata.posterior["tier_weights"].values.reshape(-1, LIBRARY_BASIS.shape[0]), axis=0)
    theta_conv_post = float(np.median(idata.posterior["theta_conv"].values))
    theta_gen_post = float(np.median(idata.posterior["theta_gen"].values))

    # PPC adequacy on each subset (mean |obs − ppc-mean| as a fraction of that
    # subset's total), parity with the H2.1 production PPC.
    def mae_frac(obs, name):
        pp = ppc.posterior_predictive[name].values.reshape(-1, n_bins).mean(axis=0)
        tot = max(int(obs.sum()), 1)
        return float(np.abs(obs - pp).mean() / tot)
    ppc_mae_aligned = mae_frac(data["y_aligned"], "y_al_obs")
    ppc_mae_nonaligned = mae_frac(data["y_nonaligned"], "y_non_obs")

    return {
        "name": unit["name"], "kind": unit["kind"], "tier": unit["tier"],
        "frame": unit["frame"], "unit_index": unit["unit_index"],
        "n_rows_raw": data["n_rows_raw"], "n_aligned_raw": data["n_aligned_raw"],
        "k_aligned_eff": data["k"], "n_rows_eff": data["n_rows"],
        "row_aligned_frac": round(data["row_aligned_frac"], 4),
        "mass_aligned_frac": round(data["mass_aligned_frac"], 4),
        "alpha_median": alpha_med, "alpha_ci_lo": alpha_lo, "alpha_ci_hi": alpha_hi,
        "theta_conv_post_med": theta_conv_post, "theta_gen_post_med": theta_gen_post,
        "max_rhat": max_rhat, "min_ess_bulk": min_ess_bulk, "min_ess_tail": min_ess_tail,
        "n_divergences": n_div,
        "convergence_pass": bool(convergence_pass(max_rhat, min_ess_bulk)),
        "ppc_mae_frac_aligned": ppc_mae_aligned,
        "ppc_mae_frac_nonaligned": ppc_mae_nonaligned,
        "corrected_genuine_spa": [float(x) for x in p_gen_med_norm],   # H3b hand-off (sums to 1)
        "p_gen_median_raw": [float(x) for x in p_gen_med],
        "p_conv_median": [float(x) for x in p_conv_med],
        "tier_weights_median": [float(x) for x in tw_med],
    }


def _worker(unit: dict) -> tuple[str, bool, float]:
    df = H.load_filtered_lire()  # aligned_indicator recomputes family internally; no column needed
    latin = H.latin_provinces()
    sub = R.subset_for(df, unit, latin)
    data = R.build_unit_cc_data(sub)
    t0 = time.time()
    out = fit_one(unit, data)
    out["secs"] = round(time.time() - t0, 1)
    tmp = UNITS_DIR / f"{_safe(unit['name'])}.json.tmp"
    final = UNITS_DIR / f"{_safe(unit['name'])}.json"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, final)
    gc.collect()
    return unit["name"], out["convergence_pass"], out["alpha_median"]


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def unit_is_done(unit: dict) -> bool:
    p = UNITS_DIR / f"{_safe(unit['name'])}.json"
    if not p.exists():
        return False
    try:
        d = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return "convergence_pass" in d


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-jobs", type=int, default=8)
    ap.add_argument("--max-tasks-per-child", type=int, default=1)
    ap.add_argument("--only", type=str, default=None, help="fit a single unit by exact name")
    args = ap.parse_args()
    UNITS_DIR.mkdir(parents=True, exist_ok=True)

    units = R.enumerate_refit_units()
    if args.only:
        units = [u for u in units if u["name"] == args.only]
        if not units:
            raise SystemExit(f"no unit named {args.only!r}")
    todo = [u for u in units if not unit_is_done(u)]
    print(f"refit: {len(units)} units ({len(todo)} to do, {len(units)-len(todo)} cached); "
          f"n_jobs {args.n_jobs}; library {LIBRARY_BASIS.shape[0]} rows", flush=True)
    STATUS_PATH.write_text(f"refit — 0/{len(units)} done (starting)\n")
    if not todo:
        print("nothing to do (all cached).")
        return

    t0 = time.time()
    done = len(units) - len(todo)
    failed = []
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, u): u for u in todo}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                name, conv, amed = fut.result()
                done += 1
                print(f"[{done}/{len(units)}] {name}  α={amed:.3f}  "
                      f"conv={'ok' if conv else 'FAIL'}", flush=True)
            except BrokenProcessPool:
                STATUS_PATH.write_text(f"refit — ABORTED BrokenProcessPool at {done}\n")
                print("FATAL: pool broken (OOM?) — resume re-runs unfinished units.", flush=True)
                raise
            except Exception as exc:  # noqa: BLE001
                failed.append(u["name"])
                print(f"WORKER-ERROR {u['name']}: {repr(exc)[:160]}", flush=True)
            STATUS_PATH.write_text(
                f"refit — {done}/{len(units)} done; elapsed {(time.time()-t0)/60:.1f} min; "
                f"worker-errors {len(failed)}\n")
    print(f"refit complete in {(time.time()-t0)/60:.1f} min. worker-errored: {failed}")


if __name__ == "__main__":
    main()
