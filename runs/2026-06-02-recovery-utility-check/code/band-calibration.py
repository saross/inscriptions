#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
band-calibration.py
===================

Diagnostic: does the recovered genuine-SPA (``p_gen``) **credible band** have
honest coverage? The 2026-05-26 recovery grid validated p_gen *shape* recovery
(Pearson r) and stored only the posterior *median* curve, not the per-bin band.
This re-fits a representative subset of operating-envelope cells, extracts the
per-bin p_gen posterior, and measures **pointwise band coverage**: the fraction
of time-bins where the 95% credible interval contains the true p_gen, averaged
over bins and replicates.

The headline question this answers: is the genuine-timeline error band
trustworthy, and — critically — does its coverage **degrade at large N** the way
the mixing-weight α coverage did (the posterior-concentration effect that broke
the lodged criterion), or does it hold?

Re-uses the grid's exact cell-construction, synthetic-data generation, and model
(`cell_lib`, `synth`) so the diagnostic speaks to the real grid. Fits run under
whatever pymc is installed on the host; the model is identical to the grid's, so
band calibration (a property of the model + NUTS) transfers. Stack note: the
grid was fit under pymc 5.28 on sapphire; this diagnostic is intended for zbook
(pymc 6.x) — flagged in the output.

Usage
-----
    python band-calibration.py --design-json <design.json> \\
        --grid-code <recovery-grid-two-unit/code> \\
        --output-dir <outputs/> [--n-reps 30] [--n-jobs 8] [--smoke]

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

# Single-thread BLAS so the outer process pool does not oversubscribe cores.
for _v in (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_v, "1")
os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN,allow_gc=False")
warnings.filterwarnings("ignore")

# --------------------------------------------------------------------------- #
# Representative subset — operating envelope, spanning the axes that matter    #
# for band calibration: shape difficulty x mixing weight x sample size.       #
# --------------------------------------------------------------------------- #
SUBSET_SHAPES = ["smooth_growth", "rise_and_fall", "regnal_cluster"]  # easy→hard
SUBSET_ALPHAS = [0.30, 0.70]      # moderate and high-but-in-envelope convention
SUBSET_NS = [2000, 50000]         # small vs large N — the key contrast
SUBSET_TIER = "uniform"

# NUTS settings — identical to the grid (spec §3.1).
N_DRAWS, N_TUNE, N_CHAINS, TARGET_ACCEPT = 2_000, 1_000, 4, 0.95
CRED = (2.5, 97.5)  # 95% central credible interval


def _select_cells(cells: list[dict]) -> list[dict]:
    """Filter the full 450-cell enumeration down to the diagnostic subset."""
    chosen = []
    for c in cells:
        cid = c["cell_id"]
        ok_shape = any(f"shape={s}_" in cid for s in SUBSET_SHAPES)
        ok_tier = f"tier={SUBSET_TIER}_" in cid
        ok_alpha = any(abs(c["alpha"] - a) < 1e-9 for a in SUBSET_ALPHAS)
        ok_n = int(c["n"]) in SUBSET_NS
        if ok_shape and ok_tier and ok_alpha and ok_n:
            chosen.append(c)
    return chosen


def _worker(task: dict) -> dict:
    """Generate one replicate, fit it, and return p_gen band-coverage stats.

    Runs in a child process: rebuilds the envelope/tier-basis/cell locally
    (so only plain picklable args cross the boundary), generates the exact
    grid replicate (deterministic seeds), fits the F1+F3 model with cores=1,
    and measures pointwise 95% (and 50%) coverage of the true p_gen.
    """
    sys.path.insert(0, task["grid_code"])
    import pymc as pm  # noqa: E402
    from cell_lib import (  # noqa: E402
        build_model_f1_f3, build_tier_basis, enumerate_grid_cells,
        load_design, make_envelope,
    )
    from synth import generate_replicate  # noqa: E402

    design = load_design(Path(task["design_json"]))
    env = make_envelope(design)
    tier_basis = build_tier_basis(design, env)
    cells = enumerate_grid_cells(design)
    cell = next(c for c in cells if c["cell_id"] == task["cell_id"])

    scratch = Path(task["scratch_root"])
    synth_path = generate_replicate(
        cell, task["replicate"], task["base_seed"], env, tier_basis,
        scratch, unit="inscription",
    )
    df = pd.read_parquet(synth_path)
    y = df["y"].to_numpy(dtype=np.int64)
    p_gen_true = df["p_gen_true"].to_numpy(dtype=float)

    fit_seed = task["base_seed"] + cell["cell_index"] + task["replicate"] + 1
    model = build_model_f1_f3(y, tier_basis)
    with model:
        idata = pm.sample(
            draws=N_DRAWS, tune=N_TUNE, chains=N_CHAINS, cores=1,
            target_accept=TARGET_ACCEPT, random_seed=fit_seed,
            progressbar=False,
        )

    pgen = idata.posterior["p_gen"].values  # (chain, draw, n_bins)
    pgen = pgen.reshape(-1, pgen.shape[-1])  # (samples, n_bins)
    lo95, hi95 = np.percentile(pgen, CRED, axis=0)
    lo50, hi50 = np.percentile(pgen, [25.0, 75.0], axis=0)
    covered95 = (p_gen_true >= lo95) & (p_gen_true <= hi95)
    covered50 = (p_gen_true >= lo50) & (p_gen_true <= hi50)
    import arviz as az  # noqa: E402
    max_rhat = float(az.rhat(idata, var_names=["alpha"])["alpha"].values)

    return {
        "cell_id": task["cell_id"],
        "shape_name": task["shape_name"],
        "alpha_true": task["alpha"],
        "n": task["n"],
        "replicate": task["replicate"],
        "pointwise_cov95": float(covered95.mean()),
        "pointwise_cov50": float(covered50.mean()),
        "mean_band_width95": float(np.mean(hi95 - lo95)),
        "alpha_rhat": max_rhat,
    }


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="p_gen band-calibration diagnostic.")
    p.add_argument("--design-json", required=True, type=Path)
    p.add_argument("--grid-code", required=True, type=Path,
                   help="recovery-grid-two-unit/code dir (cell_lib, synth).")
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--n-reps", type=int, default=30)
    p.add_argument("--n-jobs", type=int, default=8)
    p.add_argument("--base-seed", type=int, default=20260526)
    p.add_argument("--smoke", action="store_true",
                   help="1 cell x 2 reps, sequential.")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    grid_code = str(args.grid_code.resolve())
    sys.path.insert(0, grid_code)
    from cell_lib import enumerate_grid_cells, load_design  # noqa: E402

    design = load_design(args.design_json)
    cells = _select_cells(enumerate_grid_cells(design))
    if not cells:
        print("[band-cal] ERROR: subset matched no cells.", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    scratch_root = args.output_dir / "scratch"
    scratch_root.mkdir(parents=True, exist_ok=True)

    if args.smoke:
        cells = [c for c in cells if "rise_and_fall" in c["cell_id"]
                 and "N=2000" in c["cell_id"] and abs(c["alpha"] - 0.30) < 1e-9]
        n_reps, n_jobs = 2, 1
    else:
        n_reps, n_jobs = args.n_reps, args.n_jobs

    tasks = [
        {
            "design_json": str(args.design_json.resolve()),
            "grid_code": grid_code,
            "scratch_root": str(scratch_root),
            "base_seed": args.base_seed,
            "cell_id": c["cell_id"],
            "shape_name": c["cell_id"].split("_alpha")[0].replace("shape=", ""),
            "alpha": float(c["alpha"]),
            "n": int(c["n"]),
            "replicate": r,
        }
        for c in cells for r in range(n_reps)
    ]
    print(f"[band-cal] {len(cells)} cells x {n_reps} reps = {len(tasks)} fits "
          f"(n_jobs={n_jobs})")

    records = []
    if n_jobs == 1:
        for t in tasks:
            records.append(_worker(t))
            print(f"[band-cal] done {t['cell_id']} rep {t['replicate']} "
                  f"cov95={records[-1]['pointwise_cov95']:.3f}")
    else:
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            futs = {ex.submit(_worker, t): t for t in tasks}
            for i, fut in enumerate(as_completed(futs), 1):
                records.append(fut.result())
                if i % 20 == 0 or i == len(tasks):
                    print(f"[band-cal] {i}/{len(tasks)} fits complete")

    df = pd.DataFrame(records)
    out_parquet = args.output_dir / "band-calibration-replicates.parquet"
    df.to_parquet(out_parquet, index=False)

    # Per-cell aggregation.
    agg = (
        df.groupby(["shape_name", "alpha_true", "n"])
        .agg(cov95=("pointwise_cov95", "mean"),
             cov50=("pointwise_cov50", "mean"),
             band_width=("mean_band_width95", "mean"),
             n_reps=("replicate", "count"))
        .reset_index()
        .sort_values(["shape_name", "alpha_true", "n"])
    )
    agg_path = args.output_dir / "band-calibration-by-cell.csv"
    agg.to_csv(agg_path, index=False)

    print("\n=== Pointwise p_gen band coverage (target 0.95) ===")
    print(agg.to_string(index=False))
    print("\n=== Does coverage degrade at large N? (mean cov95 by N) ===")
    print(df.groupby("n")["pointwise_cov95"].mean().to_string())
    print(f"\n[band-cal] wrote {out_parquet}")
    print(f"[band-cal] wrote {agg_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
