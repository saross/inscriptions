#!/usr/bin/env python3
"""
validate_option_c.py --- multi-cell validation of the non-parametric
row-bootstrap Monte Carlo (MC) envelope (Option C in the scout taxonomy).

Background
----------
The H1 simulation (commit 9b34ad8, 2026-04-25) discovered catastrophic
false-positive (FP) inflation in the original parametric Poisson-on-fit
MC envelope: zero-effect FP rates ranged from ~0.01 up to 1.00, with
many province / urban-area cells well above the nominal alpha = 0.05.
A pilot experiment (experiment_aoristic_mc.py) confirmed:

  - Old (Poisson-on-fit) and Aoristic-from-fit (Option A) samplers fail
    to control FP at the worst broken cell.
  - **Option C (non-parametric row-bootstrap from filtered LIRE) gave
    FP ~ 0.07 at province / cpl-3 / step / n=2500** --- close to the
    0.05 target.

This script extends the validation across a representative grid of
80 cells (3 levels x 2 shapes x 4 brackets x reduced n-sweep), running
200 iterations each with 500 MC replicates per envelope test, on
sapphire's 24-core CPU pool.

Method (Option C)
-----------------
For each iteration:

  1. Bootstrap n rows from filtered LIRE.
  2. Aoristic-resample those rows uniformly within their
     [not_before, not_after] intervals -> observed Summed Probability
     Array (SPA).
  3. Optionally inject an effect (zero-effect = identity; non-zero
     brackets test detection power).
  4. Build n_mc replicate SPAs by re-bootstrapping n rows from full
     filtered LIRE + fresh aoristic-resample (NO parametric null fit).
  5. Compute pointwise alpha/2 and 1 - alpha/2 envelope quantiles.
  6. Count observed bins outside envelope; reference distribution is
     the per-replicate count of bins outside envelope. Reject if
     pval_global = mean(mc_outside >= obs_outside) < alpha.

The MC replicates here have the same operational variance structure
as the observed SPA (same bootstrap + aoristic operation, fresh
randomness), so under the null the observed should NOT be extreme
relative to the reference distribution. Under a real injected effect
the observed should fall outside the envelope (preserving detection
power).

Schema
------

    cell_id, level, shape, n, bracket, iter,
    detected, pval_global, n_bins_outside, seed_hex, wall_ms

(Note: no null_model / cpl_k / cpl_aic columns --- Option C is
parametric-null-free.)

Usage
-----

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/validate_option_c.py \\
        --out runs/2026-04-25-h1-simulation/outputs/option-c-validation \\
        --seed 20260425 --n_iter 200 --n_mc 500 --n_jobs -1

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

# Ensure primitives.py is importable when run as a script.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import primitives as P  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("validate_option_c")


# ---------------------------------------------------------------------------
# Grid specification
# ---------------------------------------------------------------------------

LEVEL_N_SWEEPS: dict[str, tuple[int, ...]] = {
    "empire": (50_000,),
    "province": (100, 500, 2_500, 10_000, 25_000),
    "urban-area": (25, 100, 500, 2_500),
}

SHAPE_NAMES = ("step", "gaussian")

# Bracket specs match primitives.BRACKETS.
BRACKET_SPECS: dict[str, dict] = {
    "zero":          {"magnitude":  0.0, "duration": 50.0},
    "a_50pc_50y":    {"magnitude": -0.5, "duration": 50.0},
    "b_double_25y":  {"magnitude": +1.0, "duration": 25.0},
    "c_20pc_25y":    {"magnitude": -0.2, "duration": 25.0},
}

CENTRE_YEAR = 150.0  # mid-envelope (50 BC -- AD 350)
RANDOM_SEED = 20260425


@dataclass(frozen=True)
class CellSpec:
    """One (level, shape, n, bracket) cell."""
    cell_id: str
    level: str
    shape: str
    n: int
    bracket: str


def enumerate_cells() -> list[CellSpec]:
    """Build the 80-cell validation grid.

    Returns
    -------
    list[CellSpec]
        Deterministic ordering by (level, shape, n, bracket).
        Cell count: (1 + 5 + 4) levels-by-n x 2 shapes x 4 brackets = 80.
    """
    cells: list[CellSpec] = []
    for level, ns in LEVEL_N_SWEEPS.items():
        for shape in SHAPE_NAMES:
            for n in ns:
                for bracket in BRACKET_SPECS:
                    cid = f"{level}_{shape}_n{n}_{bracket}"
                    cells.append(CellSpec(
                        cell_id=cid,
                        level=level,
                        shape=shape,
                        n=n,
                        bracket=bracket,
                    ))
    return cells


# ---------------------------------------------------------------------------
# Option C MC sampler + envelope test
# (Mirrors experiment_aoristic_mc.sample_mc_nonparametric --- copied here
# so this driver is self-contained and does not depend on the pilot's
# untracked module.)
# ---------------------------------------------------------------------------

def sample_mc_nonparametric(
    nb: np.ndarray,
    na: np.ndarray,
    n: int,
    bin_edges: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """One MC replicate SPA via row-bootstrap + aoristic resample.

    Parameters
    ----------
    nb : numpy.ndarray
        not_before column of filtered LIRE (length N_total).
    na : numpy.ndarray
        not_after column of filtered LIRE (length N_total).
    n : int
        Bootstrap sample size (matches observed-cell n).
    bin_edges : numpy.ndarray
        Histogram bin edges.
    rng : numpy.random.Generator
        Seeded generator.

    Returns
    -------
    numpy.ndarray
        MC replicate SPA (length len(bin_edges) - 1).
    """
    idx = rng.integers(0, len(nb), size=n)
    years = rng.uniform(nb[idx], na[idx])
    spa, _ = np.histogram(years, bins=bin_edges)
    return spa.astype(float)


def envelope_test_nonparametric(
    observed_spa: np.ndarray,
    nb: np.ndarray,
    na: np.ndarray,
    n: int,
    bin_edges: np.ndarray,
    n_mc: int,
    rng: np.random.Generator,
    *,
    alpha: float = 0.05,
    variance_floor: float = 1e-10,
) -> dict:
    """Timpson 2014 envelope test using non-parametric MC sampler.

    The reference distribution for ``pval_global`` is the per-replicate
    count of bins outside the pointwise envelope, computed across the
    same MC array (each replicate is "left out" implicitly because the
    envelope is symmetric and the count statistic is robust).

    Parameters
    ----------
    observed_spa : numpy.ndarray
        Bootstrap-then-aoristic observed SPA (possibly with effect injected).
    nb, na : numpy.ndarray
        Filtered LIRE date bounds.
    n : int
        Bootstrap sample size for MC replicates (matches observed cell n).
    bin_edges : numpy.ndarray
        Histogram bin edges.
    n_mc : int
        Number of MC replicates.
    rng : numpy.random.Generator
        Seeded generator.
    alpha : float, default 0.05
        Two-tailed alpha for the envelope.
    variance_floor : float, default 1e-10
        Bins with MC variance below this are excluded (empty/edge bins).

    Returns
    -------
    dict
        ``{"detected": bool, "pval_global": float, "n_bins_outside": int}``
    """
    n_bins = len(bin_edges) - 1
    mc_array = np.empty((n_mc, n_bins), dtype=float)
    for i in range(n_mc):
        mc_array[i] = sample_mc_nonparametric(nb, na, n, bin_edges, rng)

    lo_env = np.quantile(mc_array, alpha / 2.0, axis=0)
    hi_env = np.quantile(mc_array, 1.0 - alpha / 2.0, axis=0)

    var = mc_array.var(axis=0)
    keep = var >= variance_floor

    obs_outside_mask = (observed_spa < lo_env) | (observed_spa > hi_env)
    obs_outside = int((obs_outside_mask & keep).sum())

    mc_outside_mask = (mc_array < lo_env) | (mc_array > hi_env)
    mc_outside = (mc_outside_mask & keep[np.newaxis, :]).sum(axis=1)

    pval_global = float(np.mean(mc_outside >= obs_outside))
    return {
        "detected": bool(pval_global < alpha),
        "pval_global": pval_global,
        "n_bins_outside": obs_outside,
    }


# ---------------------------------------------------------------------------
# Cell executor (one cell -> list of per-iteration records)
# ---------------------------------------------------------------------------

def run_cell(
    spec: CellSpec,
    nb: np.ndarray,
    na: np.ndarray,
    bin_edges: np.ndarray,
    bin_centres: np.ndarray,
    n_iter: int,
    n_mc: int,
    cell_seed: np.random.SeedSequence,
) -> list[dict]:
    """Execute one cell: n_iter iterations, each running an Option C envelope test.

    Parameters
    ----------
    spec : CellSpec
    nb, na : numpy.ndarray
        Filtered LIRE not_before / not_after arrays.
    bin_edges, bin_centres : numpy.ndarray
        SPA bin edges + centres.
    n_iter : int
        Iterations per cell.
    n_mc : int
        MC replicates per envelope test.
    cell_seed : numpy.random.SeedSequence
        Per-cell SeedSequence; spawns iteration-level sequences.

    Returns
    -------
    list[dict]
        One row per iteration, validation schema.
    """
    bracket = BRACKET_SPECS[spec.bracket]
    iter_seeds = cell_seed.spawn(n_iter)

    # Cap empire-level n at LIRE size (full filtered frame ~ 50 000).
    effective_n = min(spec.n, len(nb)) if spec.level == "empire" else spec.n

    records: list[dict] = []
    for iter_idx, iter_ss in enumerate(iter_seeds):
        t0 = time.perf_counter()
        rng = np.random.default_rng(iter_ss)
        seed_hex = iter_ss.generate_state(4, dtype=np.uint32).tobytes().hex()

        # 1. Bootstrap + aoristic -> observed SPA.
        idx = rng.integers(0, len(nb), size=effective_n)
        years = rng.uniform(nb[idx], na[idx])
        spa_observed, _ = np.histogram(years, bins=bin_edges)
        spa_observed = spa_observed.astype(float)

        # 2. Inject effect (zero magnitude is identity).
        spa_effect = P.inject_effect(
            spa_observed,
            bin_centres,
            magnitude=bracket["magnitude"],
            centre_year=CENTRE_YEAR,
            duration=bracket["duration"],
            shape=spec.shape,
        )

        # 3. Run Option C envelope test against fresh non-parametric MC.
        result = envelope_test_nonparametric(
            spa_effect, nb, na, effective_n,
            bin_edges, n_mc, rng,
            alpha=0.05,
        )

        wall_ms = int((time.perf_counter() - t0) * 1_000)
        records.append({
            "cell_id": spec.cell_id,
            "level": spec.level,
            "shape": spec.shape,
            "n": spec.n,
            "bracket": spec.bracket,
            "iter": iter_idx,
            "detected": bool(result["detected"]),
            "pval_global": float(result["pval_global"]),
            "n_bins_outside": int(result["n_bins_outside"]),
            "seed_hex": seed_hex,
            "wall_ms": wall_ms,
        })
    return records


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def main() -> None:
    """Build grid, parallel-dispatch cells, write parquet + summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path,
        default=Path("runs/2026-04-25-h1-simulation/outputs/option-c-validation"),
        help="Output directory.",
    )
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n_iter", type=int, default=200,
                        help="Iterations per cell.")
    parser.add_argument("--n_mc", type=int, default=500,
                        help="MC replicates per envelope test.")
    parser.add_argument("--n_jobs", type=int, default=-1,
                        help="joblib n_jobs (-1 = all cores).")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    # Load LIRE.
    lire_path = Path("archive/data-2026-04-22/LIRE_v3-0.parquet")
    logger.info("Loading LIRE from %s", lire_path)
    df = P.load_filtered_lire(lire_path)
    logger.info("Filtered LIRE: %d rows", len(df))

    # Pre-extract NumPy arrays for cheap broadcast across joblib workers.
    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)

    bin_edges = P.BIN_EDGES
    bin_centres = P.BIN_CENTRES

    # Enumerate grid + spawn per-cell SeedSequences.
    cells = enumerate_cells()
    logger.info("Grid: %d cells x %d iter x %d MC = %d envelope tests",
                len(cells), args.n_iter, args.n_mc,
                len(cells) * args.n_iter)
    logger.info("Expected parquet rows: %d", len(cells) * args.n_iter)

    master_ss = np.random.SeedSequence(args.seed)
    cell_seeds = master_ss.spawn(len(cells))

    t0 = time.time()
    logger.info("Dispatching %d cells with n_jobs=%d (loky)",
                len(cells), args.n_jobs)
    results_per_cell = Parallel(n_jobs=args.n_jobs, backend="loky", verbose=5)(
        delayed(run_cell)(
            spec, nb, na, bin_edges, bin_centres,
            args.n_iter, args.n_mc, cell_seed,
        )
        for spec, cell_seed in zip(cells, cell_seeds)
    )
    elapsed = time.time() - t0
    logger.info("All cells complete in %.1f s (%.1f min)",
                elapsed, elapsed / 60.0)

    # Flatten + persist.
    all_records: list[dict] = []
    for cell_records in results_per_cell:
        all_records.extend(cell_records)

    res_df = pd.DataFrame(all_records)
    out_parquet = args.out / "results.parquet"
    res_df.to_parquet(out_parquet, index=False)
    logger.info("Wrote %s (%d rows)", out_parquet, len(res_df))

    # Quick sanity summary; full SUMMARY.md is generated post-rsync locally.
    summary: dict = {}
    for (level, shape, n, bracket), sub in res_df.groupby(
        ["level", "shape", "n", "bracket"]
    ):
        key = f"{level}/{shape}/n{n}/{bracket}"
        summary[key] = {
            "n_iter": int(len(sub)),
            "detection_rate": float(sub["detected"].mean()),
            "median_pval": float(sub["pval_global"].median()),
            "median_outside": float(sub["n_bins_outside"].median()),
            "median_wall_ms": float(sub["wall_ms"].median()),
        }
    out_summary = args.out / "summary.json"
    with out_summary.open("w") as f:
        json.dump({
            "args": {
                "n_iter": args.n_iter, "n_mc": args.n_mc,
                "seed": args.seed, "n_jobs": args.n_jobs,
            },
            "elapsed_seconds": elapsed,
            "n_cells": len(cells),
            "n_rows": len(res_df),
            "by_cell": summary,
        }, f, indent=2)
    logger.info("Wrote %s", out_summary)


if __name__ == "__main__":
    main()
