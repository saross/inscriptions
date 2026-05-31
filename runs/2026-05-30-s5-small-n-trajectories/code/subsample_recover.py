#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
subsample_recover.py — §5 Layer-A subsample-and-recover calibration grid.
=========================================================================

The calibration test of spec §8a.3: how small can a city's inscription count get
before the trajectory method's credible intervals become too wide to be
informative? We answer it by subsampling the 7 large anchors (which have enough
data that their full-N standalone posterior-median trajectory is a trustworthy
*truth*), refitting at a ladder of reduced N, and scoring recovery of that truth.

Design (spec §8a.3)
-------------------
- **Donors:** the 7 large anchors (``bucket == "large_anchor"``: Pompeii, Salona,
  Ostia, Mogontiacum, Aquileia, Puteoli, Carnuntum (1)). They span trajectory
  shapes (Pompeii early/terminated, Ostia later peak, frontier vs Italian).
- **Truth:** each donor's full-N standalone (``model.py``, no pooling) posterior
  -median ``lam`` trajectory, normalised to a SHAPE (so coverage/correlation are
  about trajectory shape, not level, which subsampling rescales by N/N_full).
- **Grid:** ``N ∈ {50, 100, 200, 300, 500}`` × ``reps`` random subsamples per
  (donor, N) cell (default 40; spec says 30–50). A subsample draws ``N`` rows
  without replacement from the donor's inscriptions.
- **Tiers:**
    - **PRIMARY = standalone** (no pooling): isolates likelihood + aoristic +
      RW-smoothing at small N; conservative (pooling can only help). This is the
      grid that runs in full.
    - **SECONDARY = in-hierarchy** (optional, ``--secondary-cells``): refit a
      handful of (donor, N) cells inside the full hierarchy to confirm pooling
      improves coverage. Off by default (it needs the all-city cache + is far
      heavier); a small number of cells is enough to make the point.
- **Metrics per fit** (scored against the donor's full-N shape truth):
    - trajectory 95% CI coverage of the truth (fraction of bins whose CI
      contains the truth shape; target ~0.95);
    - posterior-median shape Pearson r vs truth;
    - mean 95% CI width (→ the precision-vs-N curve);
    - peak bias: signed error in the argmax-bin location (recovered peak − truth
      peak), in bins.
- **Deliverable:** the precision-vs-N curve + a calibration N* below which
  coverage/width make trajectories uninformative (aggregated in ``aggregate``).

Parallelism
-----------
The grid is embarrassingly parallel. ``--n-parallel`` worker processes each run
one single-city fit at a time with ``--cores`` chains; pick ``n_parallel ×
cores ≈ 16`` to saturate zbook (default 8 workers × 2 chains = 16, but the
production default uses 4 chains — see ``--cores``). Each worker re-imports a
thread-pinned ``model.py``; the parent never samples.

This module is the DRIVER. Running it at full grid size IS production-scale
compute (~1,400 fits) — do NOT do that here; benchmark with a tiny
``--donors``/``--reps``/``--n-grid`` subset (the orchestrator wires the full
grid behind an explicit launch).

Run (BENCHMARK example — one donor, 2 reps, 2 N values)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/subsample_recover.py \
        --donors Ostia --reps 2 --n-grid 100 200 --n-parallel 4 --cores 2

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp  # noqa: E402

DEFAULT_N_GRID = (50, 100, 200, 300, 500)


# --------------------------------------------------------------------------- #
# Shape + scoring helpers.
# --------------------------------------------------------------------------- #

def to_shape(lam: np.ndarray) -> np.ndarray:
    """Normalise a per-bin rate trajectory to a unit-sum SHAPE.

    Subsampling rescales the level (fewer inscriptions -> lower rate), so
    recovery is scored on the trajectory SHAPE. Dividing by the sum removes the
    level and leaves the temporal profile.
    """
    lam = np.asarray(lam, dtype=float)
    s = lam.sum()
    return lam / s if s > 0 else lam


def score_against_truth(lam_draws_med: np.ndarray, lam_lo: np.ndarray,
                        lam_hi: np.ndarray, truth_shape: np.ndarray) -> dict:
    """Score one fit's trajectory against the donor's full-N shape truth.

    The posterior median + 95% CI are converted to shapes by dividing each by
    the MEDIAN trajectory's sum (a single positive scalar), so the CI stays a
    valid interval on the same shape scale as the truth.

    Args:
        lam_draws_med: Posterior-median ``lam`` (length T).
        lam_lo, lam_hi: 2.5 / 97.5 percentile ``lam`` (length T).
        truth_shape: Donor full-N median trajectory as a unit-sum shape.

    Returns:
        Dict with ``coverage``, ``shape_r``, ``mean_ci_width``, ``peak_bias``.
    """
    denom = lam_draws_med.sum()
    denom = denom if denom > 0 else 1.0
    med_s = lam_draws_med / denom
    lo_s = lam_lo / denom
    hi_s = lam_hi / denom

    covered = (truth_shape >= lo_s) & (truth_shape <= hi_s)
    coverage = float(covered.mean())
    # Pearson r on the shape (median vs truth).
    shape_r = float(np.corrcoef(med_s, truth_shape)[0, 1])
    mean_ci_width = float(np.mean(hi_s - lo_s))
    peak_bias = int(np.argmax(med_s) - np.argmax(truth_shape))
    return {
        "coverage": coverage,
        "shape_r": shape_r,
        "mean_ci_width": mean_ci_width,
        "peak_bias": peak_bias,
    }


# --------------------------------------------------------------------------- #
# Worker: one standalone fit on a subsample (runs in a child process).
# --------------------------------------------------------------------------- #

def _fit_subsample(args: dict) -> dict:
    """Child-process worker: subsample a donor, fit standalone, score.

    Imports ``model`` inside the child so each worker has its own pymc/pytensor
    state. Thread pinning is inherited from the parent's environment.

    FAULT TOLERANCE: the whole body is wrapped so a SINGLE failed fit (sampler
    error, NaN, etc.) returns a marker dict (``ok=False`` with the traceback)
    rather than raising — a propagating exception through ``fut.result()`` would
    otherwise abort the entire ~1,400-fit grid and lose every completed fit. The
    driver counts, logs, and excludes failures, then still writes the partial
    results.
    """
    import traceback

    donor = args["donor"]
    n = args["n"]
    rep = args["rep"]
    try:
        import model as m  # noqa: E402  (local single-city model)

        A_full = args["A_full"]          # (N_full, T) donor aoristic matrix
        truth_shape = np.asarray(args["truth_shape"])
        draws, tune, chains, cores = (
            args["draws"], args["tune"], args["chains"], args["cores"])
        target_accept = args["target_accept"]
        seed = args["seed"]

        rng = np.random.default_rng(seed)
        N_full = A_full.shape[0]
        k = min(n, N_full)
        idx = rng.choice(N_full, size=k, replace=False)
        A = A_full[idx]
        # Guard zero-mass rows (should not occur; dataprep drops them).
        A = A[A.sum(axis=1) > 0]

        t0 = time.perf_counter()
        idata = m.fit(A, draws=draws, tune=tune, chains=chains, cores=cores,
                      target_accept=target_accept,
                      random_seed=int(rng.integers(0, 2**31 - 1)),
                      progressbar=False)
        wall = time.perf_counter() - t0

        lam = idata.posterior["lam"]
        med = lam.median(("chain", "draw")).values
        lo = lam.quantile(0.025, ("chain", "draw")).values
        hi = lam.quantile(0.975, ("chain", "draw")).values
        conv = m.convergence_summary(idata)
        sc = score_against_truth(med, lo, hi, truth_shape)

        return {
            "ok": True,
            "donor": donor, "n": n, "rep": rep, "N_realised": int(A.shape[0]),
            "wall_s": wall, **sc,
            "max_rhat": conv["max_rhat"], "min_ess_bulk": conv["min_ess_bulk"],
            "n_divergences": conv["n_divergences"],
            "gates_pass": bool(m.gates_pass(conv)),
        }
    except Exception as exc:  # noqa: BLE001 — one bad fit must not abort the grid
        return {
            "ok": False,
            "donor": donor, "n": n, "rep": rep,
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }


# --------------------------------------------------------------------------- #
# Truth: donor full-N standalone fit (run once per donor, in-process).
# --------------------------------------------------------------------------- #

def donor_truth(out_dir: Path, donor: str, draws: int, tune: int, chains: int,
                cores: int, target_accept: float, seed: int) -> tuple[np.ndarray, np.ndarray, dict]:
    """Fit a donor at full N standalone; return (A_full, truth_shape, conv).

    The donor's full-N posterior-median trajectory (as a unit-sum shape) is the
    recovery truth for every subsample of that donor.
    """
    import model as m  # noqa: E402

    bundle = dp.load_city(out_dir, donor)
    A_full = np.asarray(bundle["A"], dtype=np.float64)
    idata = m.fit(A_full, draws=draws, tune=tune, chains=chains, cores=cores,
                  target_accept=target_accept, random_seed=seed,
                  progressbar=False)
    med = idata.posterior["lam"].median(("chain", "draw")).values
    conv = m.convergence_summary(idata)
    return A_full, to_shape(med), conv


# --------------------------------------------------------------------------- #
# Aggregation.
# --------------------------------------------------------------------------- #

def aggregate(per_fit: list[dict]) -> dict:
    """Aggregate per-fit scores into the (donor, N) precision-vs-N grid.

    Returns per-cell means (coverage, shape r, CI width, |peak bias|) and a
    headline precision-vs-N curve pooled over donors, plus a coarse calibration
    N* = the smallest N at which pooled coverage >= 0.90 AND mean shape r >= 0.9
    (informative-recovery threshold; reported, not hard-coded into any claim).

    Transparency: ``np.corrcoef`` returns NaN for a constant-shape rep (zero
    variance), and pandas ``mean`` silently skips those NaNs, shrinking the
    effective rep count behind a ``shape_r`` mean. We therefore COUNT the NaN
    ``shape_r`` reps per cell (``shape_r_nan``) and overall (``shape_r_nan_total``)
    so the dropped reps are visible rather than silent.
    """
    df = pd.DataFrame(per_fit)
    shape_r_nan_total = int(df["shape_r"].isna().sum())
    cells = (
        df.groupby(["donor", "n"])
        .agg(coverage=("coverage", "mean"),
             shape_r=("shape_r", "mean"),
             shape_r_nan=("shape_r", lambda s: int(s.isna().sum())),
             mean_ci_width=("mean_ci_width", "mean"),
             abs_peak_bias=("peak_bias", lambda s: float(np.mean(np.abs(s)))),
             reps=("rep", "count"),
             frac_gates_pass=("gates_pass", "mean"))
        .reset_index()
    )
    curve = (
        df.groupby("n")
        .agg(coverage=("coverage", "mean"),
             shape_r=("shape_r", "mean"),
             mean_ci_width=("mean_ci_width", "mean"),
             abs_peak_bias=("peak_bias", lambda s: float(np.mean(np.abs(s)))))
        .reset_index()
        .sort_values("n")
    )
    n_star = None
    for _, row in curve.iterrows():
        if row["coverage"] >= 0.90 and row["shape_r"] >= 0.90:
            n_star = int(row["n"])
            break
    return {
        "cells": cells.to_dict(orient="records"),
        "precision_vs_n": curve.to_dict(orient="records"),
        "calibration_n_star": n_star,
        "n_fits": int(len(df)),
        "shape_r_nan_total": shape_r_nan_total,
    }


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def run(out_dir: Path, donors: list[str], n_grid: list[int], reps: int,
        draws: int, tune: int, chains: int, cores: int, n_parallel: int,
        target_accept: float, seed: int, results_path: Path | None,
        png_path: Path | None) -> dict:
    """Run the (donor × N × rep) standalone subsample-recover grid."""
    idx = pd.read_parquet(out_dir / "city-index.parquet")
    anchors = idx[idx["bucket"] == "large_anchor"]["city"].tolist()
    for d in donors:
        if d not in set(idx["city"]):
            raise ValueError(f"donor {d!r} not in the cache.")
    print(f"Donors: {donors}  (cache anchors: {anchors})")
    print(f"N grid: {n_grid}  reps/cell: {reps}  "
          f"=> {len(donors) * len(n_grid) * reps} subsample fits "
          f"+ {len(donors)} full-N truth fits")
    print(f"Parallelism: {n_parallel} workers x {cores} chains "
          f"(~{n_parallel * cores} cores); sampler draws={draws} tune={tune}")

    # 1. Donor truths (sequential; each uses `cores` chains).
    truths, A_fulls, truth_conv = {}, {}, {}
    for d in donors:
        A_full, ts, conv = donor_truth(
            out_dir, d, draws, tune, chains, cores, target_accept, seed)
        truths[d], A_fulls[d], truth_conv[d] = ts, A_full, conv
        print(f"  truth[{d}] N_full={A_full.shape[0]} "
              f"peak_bin={int(np.argmax(ts))} "
              f"conv rhat={conv['max_rhat']:.3f} ess={conv['min_ess_bulk']:.0f} "
              f"div={conv['n_divergences']}")

    # 2. Build the subsample task list.
    tasks = []
    rng = np.random.default_rng(seed + 1)
    for d in donors:
        for n in n_grid:
            for rep in range(reps):
                tasks.append({
                    "donor": d, "n": int(n), "rep": rep,
                    "A_full": A_fulls[d], "truth_shape": truths[d],
                    "draws": draws, "tune": tune, "chains": chains,
                    "cores": cores, "target_accept": target_accept,
                    "seed": int(rng.integers(0, 2**31 - 1)),
                })

    # 3. Run the grid in a process pool. A single failed (donor, N, rep) fit is
    #    recorded as a failure and EXCLUDED from the aggregate — it must not lose
    #    every completed fit. Both the worker (catching its own exception) and
    #    this loop (catching a worker that fails to even return) are guarded.
    per_fit: list[dict] = []
    failures: list[dict] = []
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=n_parallel) as ex:
        futs = {ex.submit(_fit_subsample, t): t for t in tasks}
        done = 0
        for fut in as_completed(futs):
            task = futs[fut]
            try:
                r = fut.result()
            except Exception as exc:  # noqa: BLE001 — worker died before returning
                r = {
                    "ok": False, "donor": task["donor"], "n": task["n"],
                    "rep": task["rep"], "error": f"{type(exc).__name__}: {exc}",
                }
            done += 1
            if not r.get("ok", True):
                failures.append(r)
                print(f"  [{done}/{len(tasks)}] FAILED {r['donor']:>14} "
                      f"N={r['n']:>3} rep={r['rep']:>2}: "
                      f"{r.get('error', 'unknown error')}")
                continue
            per_fit.append(r)
            print(f"  [{done}/{len(tasks)}] {r['donor']:>14} N={r['n']:>3} "
                  f"rep={r['rep']:>2}: cov={r['coverage']:.2f} r={r['shape_r']:.3f} "
                  f"width={r['mean_ci_width']:.4f} peakbias={r['peak_bias']:+d} "
                  f"rhat={r['max_rhat']:.3f} div={r['n_divergences']} "
                  f"({r['wall_s']:.0f}s)")
    grid_wall = time.perf_counter() - t0
    if failures:
        print(f"\n  WARNING: {len(failures)}/{len(tasks)} fits FAILED and were "
              "excluded from the aggregate:")
        for f in failures:
            print(f"    - {f['donor']} N={f['n']} rep={f['rep']}: "
                  f"{f.get('error', 'unknown error')}")

    agg = aggregate(per_fit) if per_fit else {
        "cells": [], "precision_vs_n": [], "calibration_n_star": None,
        "n_fits": 0, "note": "all fits failed; no aggregate computed",
    }
    print("\n" + "=" * 70)
    print("PRECISION-vs-N (pooled over donors)")
    print("=" * 70)
    for row in agg["precision_vs_n"]:
        print(f"  N={int(row['n']):>3}: coverage {row['coverage']:.3f}  "
              f"shape r {row['shape_r']:.3f}  "
              f"mean CI width {row['mean_ci_width']:.4f}  "
              f"|peak bias| {row['abs_peak_bias']:.2f} bins")
    print(f"\n  calibration N* (coverage>=0.90 & shape r>=0.90): "
          f"{agg['calibration_n_star']}")
    n_nan = agg.get("shape_r_nan_total", 0)
    if n_nan:
        print(f"  NOTE: {n_nan}/{len(per_fit)} reps had a constant-shape (NaN) "
              "shape_r and were skipped from the shape_r means.")
    print(f"  grid wall: {grid_wall:.0f}s for {len(tasks)} fits "
          f"({grid_wall / max(len(tasks), 1):.1f}s/fit amortised across "
          f"{n_parallel} workers)")

    out = {
        "donors": donors, "n_grid": list(n_grid), "reps": reps,
        "sampler": {"draws": draws, "tune": tune, "chains": chains,
                    "cores": cores, "target_accept": target_accept},
        "n_parallel": n_parallel, "grid_wall_s": grid_wall,
        "truth_convergence": {d: truth_conv[d] for d in donors},
        "aggregate": agg, "per_fit": per_fit,
        "n_tasks": len(tasks), "n_failures": len(failures),
        "failures": [
            {"donor": f["donor"], "n": f["n"], "rep": f["rep"],
             "error": f.get("error", "unknown error")}
            for f in failures
        ],
    }
    if results_path is not None:
        results_path.write_text(json.dumps(out, indent=2, default=float))
        print(f"Results JSON -> {results_path}")
    if png_path is not None:
        save_png(agg, png_path)
    return out


def save_png(agg: dict, png_path: Path) -> None:
    """Plot the precision-vs-N curve (coverage, CI width, shape r vs N)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    curve = pd.DataFrame(agg["precision_vs_n"]).sort_values("n")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    axes[0].plot(curve["n"], curve["coverage"], "-o")
    axes[0].axhline(0.95, color="grey", ls=":")
    axes[0].set_title("95% CI coverage of truth"); axes[0].set_xlabel("N")
    axes[0].set_ylabel("coverage"); axes[0].set_ylim(0, 1.05)
    axes[1].plot(curve["n"], curve["mean_ci_width"], "-o", color="C1")
    axes[1].set_title("mean 95% CI width (shape scale)"); axes[1].set_xlabel("N")
    axes[2].plot(curve["n"], curve["shape_r"], "-o", color="C2")
    axes[2].axhline(0.90, color="grey", ls=":")
    axes[2].set_title("posterior-median shape r"); axes[2].set_xlabel("N")
    axes[2].set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    print(f"PNG -> {png_path}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--donors", nargs="+", default=None,
                   help="Donor city names (default: all 7 large anchors).")
    p.add_argument("--n-grid", nargs="+", type=int, default=list(DEFAULT_N_GRID))
    p.add_argument("--reps", type=int, default=40)
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--cores", type=int, default=4,
                   help="Chains run concurrently per fit (cores per worker).")
    p.add_argument("--n-parallel", type=int, default=4,
                   help="Concurrent worker processes (n_parallel x cores ~ 16).")
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--out-dir", type=Path, default=dp.default_cache_dir(25))
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "subsample-recover-results.json")
    p.add_argument("--png", type=Path,
                   default=Path(__file__).resolve().parent / "subsample-recover.png")
    args = p.parse_args()

    idx = pd.read_parquet(args.out_dir / "city-index.parquet")
    donors = args.donors or idx[idx["bucket"] == "large_anchor"]["city"].tolist()
    run(args.out_dir, donors, args.n_grid, args.reps, args.draws, args.tune,
        args.chains, args.cores, args.n_parallel, args.target_accept,
        args.seed, args.results, args.png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
