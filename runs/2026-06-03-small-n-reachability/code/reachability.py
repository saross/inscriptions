#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reachability.py
===============

Small-N deconvolution-reachability study (spec: ``../spec.md``; Decision 34).
Measures the minimum subset size N at which **subset-specific** Bayesian
deconvolution (the model learns its own convention mix; no corpus p_conv
imposed) reliably recovers the genuine SPA, under the Decision-33 criterion.

For each cell (shape × α × N × tier) it fits ``--n-reps`` synthetic replicates
with ``cell_lib.build_model_f1_f3`` (the validated grid model) and records, per
replicate: posterior-median Pearson r vs true p_gen (binding shape metric),
convergence (max R̂, divergences), α bias (diagnostic), pointwise 95 % p_gen band
coverage (diagnostic), and Wasserstein-1 (supplementary). A cell **passes** if
≥ 90 % of replicates converge AND ≥ 90 % reach Pearson r ≥ 0.95. The reachability
floor per (shape, α) is the smallest passing N.

**Resumable.** Every completed fit is checkpointed to an append-only JSONL log
(``reachability-records.jsonl``) the instant it returns, so an interrupted run
resumes from where it stopped rather than restarting; re-launch with the same
``--output-dir`` to continue, or delete the log for a clean run.

The grid's design.json only carries N ∈ {2000, 10000, 50000}, so cells at the new
small N values are constructed directly from the design's shape specs + the
pilot_proxy tier vector, with fresh cell indices and a distinct base seed
(20260603) to keep stochastic streams disjoint from the production grid.

Re-uses the grid code (``cell_lib``, ``synth``); intended for zbook (pymc 6.x).

Usage
-----
    python reachability.py --design-json <design.json> \\
        --grid-code <recovery-grid-two-unit/code> --output-dir <outputs/> \\
        [--n-reps 50] [--n-jobs 16] [--smoke]

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-03, on Shawn's brief.
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

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN,allow_gc=False")
warnings.filterwarnings("ignore")

# --- Design axes (spec §3) -------------------------------------------------- #
SHAPES = ["smooth_growth", "rise_and_fall", "regnal_cluster"]
ALPHAS = [0.30, 0.50, 0.70, 0.85]
NS = [50, 100, 200, 350, 500, 1000, 2000]
TIER_NAME = "pilot_proxy"
PILOT_PROXY = (0.55, 0.30, 0.15)   # inscription pilot_proxy (spec §3.3)
BASE_SEED = 20260603

# NUTS settings — identical to the grid (spec §3.1).
N_DRAWS, N_TUNE, N_CHAINS, TARGET_ACCEPT = 2_000, 1_000, 4, 0.95
RHAT_GATE = 1.01
PEARSON_PASS = 0.95
CELL_PASS_FRAC = 0.90

# Default worker count leaves headroom for SSH + system responsiveness
# (2026-06-03: n_jobs=16 saturated zbook to the point SSH could not handshake;
# Shawn's guidance — keep a few cores free). Capped at 14.
DEFAULT_JOBS = min(14, max(1, (os.cpu_count() or 8) - 4))


def _build_cells(grid_code: str, design_json: str) -> list[dict]:
    """Construct cells at the study's (shape × α × N) from the design specs.

    Pulls the shape spec dicts and the pilot_proxy tier vector from the grid's
    own enumeration (so synth/build_pgen receive exactly what they expect), then
    stamps fresh N, α, cell_index, cell_id.
    """
    sys.path.insert(0, grid_code)
    from cell_lib import enumerate_grid_cells, load_design  # noqa: E402

    design = load_design(Path(design_json))
    template = enumerate_grid_cells(design, pilot_proxy_weights=PILOT_PROXY)
    # Shape spec per shape name (from any template cell of that shape).
    shape_spec = {}
    tier_weights = None
    for c in template:
        nm = c["cell_id"].split("_alpha")[0].replace("shape=", "")
        if nm in SHAPES and nm not in shape_spec:
            shape_spec[nm] = c["shape"]
        if tier_weights is None and f"tier={TIER_NAME}_" in c["cell_id"]:
            tier_weights = np.asarray(c["tier_weights"], dtype=float)
    missing = [s for s in SHAPES if s not in shape_spec]
    if missing:
        raise RuntimeError(f"shape specs not found for: {missing}")

    cells, idx = [], 0
    for shape in SHAPES:
        for alpha in ALPHAS:
            for n in NS:
                cells.append({
                    "cell_index": idx,
                    "cell_id": f"shape={shape}_alpha={alpha}_tier={TIER_NAME}_N={n}",
                    "shape": shape_spec[shape],
                    "alpha": float(alpha),
                    "tier_weights": tier_weights,
                    "tier_weights_name": TIER_NAME,
                    "n": int(n),
                    "shape_name": shape,
                })
                idx += 1
    return cells


def _worker(task: dict) -> dict:
    """Fit one replicate; return the full metric set for the reachability map."""
    sys.path.insert(0, task["grid_code"])
    import arviz as az  # noqa: E402
    import pymc as pm  # noqa: E402
    from scipy.stats import pearsonr, wasserstein_distance  # noqa: E402
    from cell_lib import (  # noqa: E402
        build_model_f1_f3, build_tier_basis, load_design, make_envelope,
    )
    from synth import generate_replicate  # noqa: E402

    design = load_design(Path(task["design_json"]))
    env = make_envelope(design)
    tier_basis = build_tier_basis(design, env)
    cell = {k: task[k] for k in
            ("cell_index", "cell_id", "shape", "alpha", "tier_weights",
             "tier_weights_name", "n")}
    cell["tier_weights"] = np.asarray(cell["tier_weights"], dtype=float)

    synth_path = generate_replicate(
        cell, task["replicate"], BASE_SEED, env, tier_basis,
        Path(task["scratch_root"]), unit="inscription",
    )
    df = pd.read_parquet(synth_path)
    y = df["y"].to_numpy(dtype=np.int64)
    p_gen_true = df["p_gen_true"].to_numpy(dtype=float)

    fit_seed = BASE_SEED + cell["cell_index"] + task["replicate"] + 1
    model = build_model_f1_f3(y, tier_basis)
    with model:
        idata = pm.sample(draws=N_DRAWS, tune=N_TUNE, chains=N_CHAINS, cores=1,
                          target_accept=TARGET_ACCEPT, random_seed=fit_seed,
                          progressbar=False)

    summ = az.summary(idata, var_names=["alpha", "tier_weights", "sigma_smooth",
                                        "z_pgen"], round_to="none")
    max_rhat = float(summ["r_hat"].max())
    n_div = int(idata.sample_stats.diverging.values.sum())
    a = idata.posterior["alpha"].values.reshape(-1)
    alpha_bias = float(np.median(a) - cell["alpha"])
    pgen = idata.posterior["p_gen"].values.reshape(-1, p_gen_true.size)
    pgen_med = np.median(pgen, axis=0)
    pearson_r = float(pearsonr(pgen_med, p_gen_true)[0])
    w1 = float(wasserstein_distance(env.bin_centres, env.bin_centres,
                                    pgen_med, p_gen_true))
    lo, hi = np.percentile(pgen, [2.5, 97.5], axis=0)
    band_cov95 = float(((p_gen_true >= lo) & (p_gen_true <= hi)).mean())

    return {
        "cell_id": cell["cell_id"], "shape_name": task["shape_name"],
        "alpha_true": cell["alpha"], "n": cell["n"], "replicate": task["replicate"],
        "pearson_r": pearson_r, "abs_alpha_bias": abs(alpha_bias),
        "max_rhat": max_rhat, "n_divergences": n_div, "band_cov95": band_cov95,
        "w1": w1,
        "converged": bool(max_rhat < RHAT_GATE and n_div == 0),
        "shape_pass": bool(pearson_r >= PEARSON_PASS),
    }


def _load_records(path: Path) -> list[dict]:
    """Read all completed-fit metric dicts from a checkpoint JSONL log.

    Tolerates a truncated final line (an append interrupted mid-write): parsing
    stops at the first undecodable line, so the single fit it represents is
    simply re-run on resume. Returns an empty list if the log does not exist.
    """
    records: list[dict] = []
    if not path.exists():
        return records
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                break
    return records


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Small-N deconvolution reachability.")
    p.add_argument("--design-json", required=True, type=Path)
    p.add_argument("--grid-code", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--n-reps", type=int, default=50)
    p.add_argument("--n-jobs", type=int, default=DEFAULT_JOBS,
                   help="parallel fits; default leaves headroom for ssh/system.")
    p.add_argument("--smoke", action="store_true")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    grid_code = str(args.grid_code.resolve())
    cells = _build_cells(grid_code, str(args.design_json.resolve()))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    scratch = args.output_dir / "scratch"
    scratch.mkdir(parents=True, exist_ok=True)

    if args.smoke:
        cells = [c for c in cells if c["shape_name"] == "rise_and_fall"
                 and abs(c["alpha"] - 0.50) < 1e-9 and c["n"] in (100, 2000)]
        n_reps, n_jobs = 2, 2
    else:
        n_reps, n_jobs = args.n_reps, args.n_jobs

    tasks = [
        {**{k: c[k] for k in ("cell_index", "cell_id", "shape", "alpha",
                              "tier_weights", "tier_weights_name", "n",
                              "shape_name")},
         "design_json": str(args.design_json.resolve()), "grid_code": grid_code,
         "scratch_root": str(scratch), "replicate": r}
        for c in cells for r in range(n_reps)
    ]
    # --- Resumable checkpoint log (one JSON line per completed fit) ---------- #
    # Each fit's metrics are appended to an append-only log the instant the fit
    # returns (write + flush + fsync), so an interrupted run — machine hang,
    # reboot, OOM — loses at most the fits still in flight, not the whole run.
    # Re-launching with the same --output-dir reads the log, skips fits already
    # recorded, and resumes; delete the .jsonl to force a clean re-run. Smoke
    # uses a separate log so its 2-cell subset never shadows a real run's
    # identical cell_ids. (2026-06-03 incident: a 4189/4200 in-memory run was
    # lost to a power-cycle — this log is the fix.)
    ckpt = args.output_dir / ("reachability-records.smoke.jsonl" if args.smoke
                              else "reachability-records.jsonl")
    done = {(r["cell_id"], r["replicate"]) for r in _load_records(ckpt)}
    pending = [t for t in tasks if (t["cell_id"], t["replicate"]) not in done]
    print(f"[reach] {len(cells)} cells x {n_reps} reps = {len(tasks)} fits "
          f"(n_jobs={n_jobs})")
    if done:
        print(f"[reach] resuming from {ckpt.name}: {len(done)} fits already "
              f"done, {len(pending)} remaining")

    with ckpt.open("a", encoding="utf-8") as log:
        def _checkpoint(rec: dict) -> None:
            """Append one fit's metrics and force them to stable storage."""
            log.write(json.dumps(rec) + "\n")
            log.flush()
            os.fsync(log.fileno())

        if n_jobs == 1:
            for i, t in enumerate(pending, 1):
                _checkpoint(_worker(t))
                if i % 50 == 0 or i == len(pending):
                    print(f"[reach] {i}/{len(pending)} new fits complete")
        else:
            with ProcessPoolExecutor(max_workers=n_jobs) as ex:
                futs = [ex.submit(_worker, t) for t in pending]
                for i, f in enumerate(as_completed(futs), 1):
                    _checkpoint(f.result())
                    if i % 50 == 0 or i == len(pending):
                        print(f"[reach] {i}/{len(pending)} new fits complete")

    # Aggregate from the full checkpoint log (resumed + newly completed fits).
    df = pd.DataFrame(_load_records(ckpt))
    df.to_parquet(args.output_dir / "reachability-replicates.parquet", index=False)

    agg = (df.groupby(["shape_name", "alpha_true", "n"]).agg(
        conv_rate=("converged", "mean"), shape_rate=("shape_pass", "mean"),
        mean_abs_alpha_bias=("abs_alpha_bias", "mean"),
        band_cov95=("band_cov95", "mean"), n_reps=("replicate", "count"),
    ).reset_index())
    agg["cell_pass"] = (agg.conv_rate >= CELL_PASS_FRAC) & (agg.shape_rate >= CELL_PASS_FRAC)
    agg = agg.sort_values(["shape_name", "alpha_true", "n"])
    agg.to_csv(args.output_dir / "reachability-by-cell.csv", index=False)

    print("\n=== Reachability floor (smallest passing N per shape × α) ===")
    for (sh, al), g in agg.groupby(["shape_name", "alpha_true"]):
        passing = g[g.cell_pass]["n"]
        floor = int(passing.min()) if len(passing) else None
        print(f"  {sh:15s} α={al:.2f}: floor = "
              f"{'N≥'+str(floor) if floor else 'UNREACHED in tested range'}")
    print(f"\n[reach] wrote {args.output_dir/'reachability-by-cell.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
