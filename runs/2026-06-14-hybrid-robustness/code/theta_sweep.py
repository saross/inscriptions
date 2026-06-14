#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
theta_sweep.py — (C) θ-prior-sensitivity sweep on the validated cc-library model.
=================================================================================

The robustness annex (replacing the poorly-mixing global-θ hybrid; see
HYBRID-PILOT-FINDINGS.md). Re-fit each of the 29 production units under several θ-prior
conditions and ask: **are the per-unit α's stable to the θ assumption?** The conditions
bracket the two θ centres the project now has evidence for — the production calibration
(θ_gen 0.155) and the re-derived value from the corrected α's (θ_gen ≈ 0.025; (B),
`theta-rederivation.json`) — at two concentrations (κ 40 tight, κ 12 loose).

This is well-identified (one cc-library fit per unit — the validated model — not the
joint hybrid), so its intervals are trustworthy. Reuses the production refit's data prep
(`refit_lib`), model (`joint_lib.build_model_cross_classified`, `library`), and fixed
library verbatim; only the θ prior varies.

Usage (sapphire) — PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
    uv run python code/theta_sweep.py [--n-jobs 8]

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
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

HYB = Path("/home/shawn/Code/inscriptions/runs/2026-06-14-hybrid-robustness")
REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
CELL_LIB_DIR = ("/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
                "/revalidation/code")
for p in (HYB / "code", REFIT / "code", H2, JOINT, CELL_LIB_DIR):
    sys.path.insert(0, str(p))
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402
from cell_lib import convergence_pass  # noqa: E402

SWEEP_ROOT = HYB / "outputs"
LIBRARY_BASIS, _ = R.load_library_basis()
MONITORED = ["alpha", "tier_weights", "sigma_smooth", "z_pgen", "theta_conv", "theta_gen"]

# θ-prior conditions (θ_conv_mu, θ_gen_mu, κ). 'baseline' reproduces the production
# refit (a consistency check); the rest bracket the re-derived θ centre + width.
CONDITIONS = {
    "baseline":       (0.945, 0.155, 40.0),   # production calibration (rule C, κ=40)
    "rederived":      (0.930, 0.025, 40.0),   # (B) corrected centre, same concentration
    "wide":           (0.945, 0.155, 12.0),   # original centre, loose — let data move θ
    "rederived_wide": (0.930, 0.025, 12.0),   # corrected centre, loose
}
# Deterministic per-condition seed offsets (NOT hash(), which is run-randomised).
# baseline = 0 so it reproduces the production refit bit-identically (consistency check);
# the others get distinct offsets.
COND_SEED_OFFSET = {c: (0 if c == "baseline" else i * 100_000)
                    for i, c in enumerate(CONDITIONS)}


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def fit_unit_cond(unit: dict, data: dict, cond: str) -> dict:
    """Fit one unit under one θ-prior condition; extract α med/CI + convergence + θ_gen."""
    import arviz as az
    import pymc as pm
    tcmu, tgmu, kappa = CONDITIONS[cond]
    tc_ab = J.beta_from_mean_concentration(tcmu, kappa)
    tg_ab = J.beta_from_mean_concentration(tgmu, kappa)
    n_bins = int(data["y_aligned"].size)
    model = J.build_model_cross_classified(
        data["y_aligned"], data["y_nonaligned"], data["k"], data["n_rows"],
        LIBRARY_BASIS, tc_ab, tg_ab, pconv_mode="library")
    seed = R.REFIT_BASE_SEED + unit["unit_index"] + COND_SEED_OFFSET[cond]
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                              target_accept=H.TARGET_ACCEPT, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    summ = az.summary(idata, var_names=MONITORED, round_to="none")
    a = idata.posterior["alpha"].values.reshape(-1)
    return {
        "name": unit["name"], "condition": cond,
        "theta_prior": {"conv_mu": tcmu, "gen_mu": tgmu, "kappa": kappa},
        "alpha_median": float(np.median(a)),
        "alpha_ci_lo": float(np.percentile(a, 2.5)),
        "alpha_ci_hi": float(np.percentile(a, 97.5)),
        "theta_gen_post_med": float(np.median(idata.posterior["theta_gen"].values)),
        "max_rhat": float(summ["r_hat"].max()),
        "min_ess_bulk": float(summ["ess_bulk"].min()),
        "convergence_pass": bool(convergence_pass(float(summ["r_hat"].max()),
                                                  float(summ["ess_bulk"].min()))),
    }


def _worker(task: tuple) -> tuple[str, str, float, bool]:
    unit, cond = task
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    data = R.build_unit_cc_data(R.subset_for(df, unit, latin))
    t0 = time.time()
    out = fit_unit_cond(unit, data, cond)
    out["secs"] = round(time.time() - t0, 1)
    d = SWEEP_ROOT / f"sweep-{cond}"
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / f"{_safe(unit['name'])}.json.tmp"
    final = d / f"{_safe(unit['name'])}.json"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, final)
    gc.collect()
    return unit["name"], cond, out["alpha_median"], out["convergence_pass"]


def task_done(unit: dict, cond: str) -> bool:
    p = SWEEP_ROOT / f"sweep-{cond}" / f"{_safe(unit['name'])}.json"
    if not p.exists():
        return False
    try:
        return "convergence_pass" in json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-jobs", type=int, default=8)
    ap.add_argument("--max-tasks-per-child", type=int, default=1)
    args = ap.parse_args()

    units = R.enumerate_refit_units()
    tasks = [(u, c) for c in CONDITIONS for u in units if not task_done(u, c)]
    total = len(CONDITIONS) * len(units)
    done = total - len(tasks)
    print(f"θ-sweep: {len(CONDITIONS)} conditions × {len(units)} units = {total} fits "
          f"({len(tasks)} to do, {done} cached); n_jobs {args.n_jobs}", flush=True)
    if not tasks:
        print("nothing to do (all cached).")
        return

    t0 = time.time()
    failed = []
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, t): t for t in tasks}
        for fut in as_completed(futs):
            u, c = futs[fut]
            try:
                name, cond, amed, conv = fut.result()
                done += 1
                print(f"[{done}/{total}] {cond}/{name}  α={amed:.3f} "
                      f"{'ok' if conv else 'FAIL'}", flush=True)
            except BrokenProcessPool:
                print("FATAL: pool broken — resume re-runs unfinished tasks.", flush=True)
                raise
            except Exception as exc:  # noqa: BLE001
                failed.append((u["name"], c))
                print(f"WORKER-ERROR {c}/{u['name']}: {repr(exc)[:140]}", flush=True)
    print(f"θ-sweep complete in {(time.time()-t0)/60:.1f} min. worker-errored: {failed}")


if __name__ == "__main__":
    main()
