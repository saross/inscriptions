#!/usr/bin/env python3
"""
validate_forward_fit_exp.py --- forward-fit exponential pilot, two-part validation.

This is the gating experiment for the forward-fit methodology. It tests
whether fitting an exponential null in *true-date* space (treating each
inscription's interval as an integration range) and forward-applying the
empirical aoristic mechanism to MC replicates controls the false-positive
(FP) rate at the nominal alpha = 0.05 across a representative grid.

Two-part design
---------------
Part A --- *Synthetic-data* FP and detection. For each cell
``(b_null, n, bracket)``:

  1. Sample n true dates from f(t; b_null) on [-50, 350].
  2. Sample n widths from the real LIRE width distribution (with replacement).
  3. Random uniform interval positions; construct synthetic [nb, na] rows.
  4. Aoristic-resample once -> synthetic_spa.
  5. Inject the bracket effect (zero magnitude is identity).
  6. Forward-fit the exponential on the synthetic intervals -> b_hat.
  7. Run forward-MC envelope test using b_hat + the row widths -> detected, p.

Cells: b_null in {-0.005, 0.0, 0.005} x n in {500, 2500, 10000}
       x bracket in {zero, a_50pc_50y step, c_20pc_25y step}
       = 27 cells.

Expected (gate criteria):
  - zero bracket: FP <= 0.10 (target 0.05).
  - a_50pc_50y:   detection >= 0.80 at sufficient n.
  - c_20pc_25y:   harder; pattern should resemble Option C's results.

Part B --- *Real-LIRE bootstrap* FP. For each n in {500, 2500, 10000},
bootstrap from the real filtered LIRE corpus (zero bracket only, 100
iterations). FP is *expected* to be elevated here because real LIRE has
editorial spikes and other non-exponential structure -- this is the
"real-data deviation detection" sensitivity check, not a methodology
failure indicator.

Output schema (parquet)
-----------------------

    cell_id, part, b_null, n, bracket, iter, detected, pval_global,
    n_bins_outside, b_hat, log_likelihood, seed_hex, wall_ms

Default output: runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/

Usage
-----

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/\\
        validate_forward_fit_exp.py \\
        --out runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot \\
        --seed 20260425 --n_iter 100 --n_mc 500 --n_jobs -1

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

# Ensure local module imports work when run as a script.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import primitives as P  # noqa: E402
from forward_fit import (  # noqa: E402
    _truncated_exponential_inverse_cdf,
    fit_null_exponential_forward,
    forward_envelope_test,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("validate_forward_fit")


# ---------------------------------------------------------------------------
# Grid specification
# ---------------------------------------------------------------------------

T_MIN: float = -50.0
T_MAX: float = 350.0
CENTRE_YEAR: float = 150.0  # mid-envelope; matches Option C validation.

PART_A_B_NULLS: tuple[float, ...] = (-0.005, 0.0, 0.005)
PART_A_NS: tuple[int, ...] = (500, 2_500, 10_000)
PART_A_BRACKETS: dict[str, dict] = {
    "zero":         {"magnitude":  0.0, "duration": 50.0, "shape": "step"},
    "a_50pc_50y":   {"magnitude": -0.5, "duration": 50.0, "shape": "step"},
    "c_20pc_25y":   {"magnitude": -0.2, "duration": 25.0, "shape": "step"},
}

PART_B_NS: tuple[int, ...] = (500, 2_500, 10_000)
PART_B_BRACKET = "zero"  # FP-only sensitivity check

RANDOM_SEED: int = 20260425


@dataclass(frozen=True)
class CellSpec:
    """Spec for a single (part, b_null, n, bracket) cell."""
    cell_id: str
    part: str             # "A" or "B"
    b_null: float         # NaN for Part B (real LIRE)
    n: int
    bracket: str


def enumerate_cells() -> list[CellSpec]:
    """Build the 27 + 3 = 30 cell grid for the forward-fit pilot."""
    cells: list[CellSpec] = []
    # Part A: synthetic-data, full b_null x n x bracket grid.
    for b_null in PART_A_B_NULLS:
        for n in PART_A_NS:
            for bracket in PART_A_BRACKETS:
                cid = f"A_b{b_null:+.3f}_n{n}_{bracket}"
                cells.append(CellSpec(
                    cell_id=cid, part="A",
                    b_null=b_null, n=n, bracket=bracket,
                ))
    # Part B: real-LIRE bootstrap, zero bracket only, 3 n-values.
    for n in PART_B_NS:
        cid = f"B_realLIRE_n{n}_{PART_B_BRACKET}"
        cells.append(CellSpec(
            cell_id=cid, part="B",
            b_null=float("nan"), n=n, bracket=PART_B_BRACKET,
        ))
    return cells


# ---------------------------------------------------------------------------
# Per-cell executor
# ---------------------------------------------------------------------------

def _simulate_intervals(
    b_null: float, n: int, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate ``n`` synthetic intervals from f(t; b_null) over [t_min, t_max].

    Mirrors the forward MC sampler's generative procedure so that under the
    null Part A's data-generating process and the test-time MC replicates
    share variance structure.

    Returns
    -------
    nb, na : numpy.ndarray
        Synthetic interval lower / upper bounds.
    """
    u_t = rng.uniform(size=n)
    t_true = _truncated_exponential_inverse_cdf(u_t, b_null, T_MIN, T_MAX)
    w = rng.choice(widths_pool, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


def _bootstrap_real_intervals(
    nb_pool: np.ndarray, na_pool: np.ndarray, n: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Bootstrap n rows (with replacement) from the real LIRE corpus."""
    idx = rng.integers(0, len(nb_pool), size=n)
    return nb_pool[idx].copy(), na_pool[idx].copy()


def run_cell(
    spec: CellSpec,
    widths_pool: np.ndarray,
    nb_pool: np.ndarray,
    na_pool: np.ndarray,
    bin_edges: np.ndarray,
    bin_centres: np.ndarray,
    n_iter: int,
    n_mc: int,
    cell_seed: np.random.SeedSequence,
) -> list[dict]:
    """Execute one cell: n_iter iterations, return per-iteration records.

    Part A: simulate from b_null, fit, test against forward MC.
    Part B: bootstrap from real LIRE, fit, test against forward MC. Real-data
    structure is expected to elevate FP -- this is the diagnostic question.
    """
    iter_seeds = cell_seed.spawn(n_iter)

    # Bracket parameters (Part A) or just "zero" identity (Part B).
    if spec.part == "A":
        bracket = PART_A_BRACKETS[spec.bracket]
    else:
        bracket = {"magnitude": 0.0, "duration": 50.0, "shape": "step"}

    records: list[dict] = []
    for iter_idx, iter_ss in enumerate(iter_seeds):
        t0 = time.perf_counter()
        rng = np.random.default_rng(iter_ss)
        seed_hex = iter_ss.generate_state(4, dtype=np.uint32).tobytes().hex()

        # 1. Build synthetic or real intervals.
        if spec.part == "A":
            nb_iter, na_iter = _simulate_intervals(
                spec.b_null, spec.n, widths_pool, rng,
            )
        else:
            nb_iter, na_iter = _bootstrap_real_intervals(
                nb_pool, na_pool, spec.n, rng,
            )

        # 2. Aoristic-resample to build observed SPA.
        years = rng.uniform(nb_iter, na_iter)
        spa_observed, _ = np.histogram(years, bins=bin_edges)
        spa_observed = spa_observed.astype(float)

        # 3. Inject bracket effect (zero magnitude = identity).
        spa_effect = P.inject_effect(
            spa_observed, bin_centres,
            magnitude=bracket["magnitude"],
            centre_year=CENTRE_YEAR,
            duration=bracket["duration"],
            shape=bracket["shape"],
        )

        # 4. Forward-fit on this iteration's intervals.
        try:
            fit = fit_null_exponential_forward(
                np.column_stack([nb_iter, na_iter]),
                t_min=T_MIN, t_max=T_MAX,
            )
        except (ValueError, RuntimeError) as e:
            logger.warning("fit failed in %s iter %d: %s",
                           spec.cell_id, iter_idx, e)
            continue
        if not fit["converged"]:
            logger.debug("fit did not converge: %s iter %d",
                         spec.cell_id, iter_idx)
            # Still record but flag.
            wall_ms = int((time.perf_counter() - t0) * 1_000)
            records.append({
                "cell_id": spec.cell_id, "part": spec.part,
                "b_null": spec.b_null, "n": spec.n,
                "bracket": spec.bracket, "iter": iter_idx,
                "detected": False, "pval_global": float("nan"),
                "n_bins_outside": -1,
                "b_hat": fit["b"],
                "log_likelihood": fit["log_likelihood"],
                "converged": False,
                "seed_hex": seed_hex, "wall_ms": wall_ms,
            })
            continue

        # 5. Forward MC envelope test.
        widths_iter = na_iter - nb_iter
        try:
            result = forward_envelope_test(
                spa_effect, fit["b"], widths_iter, bin_edges, n_mc, rng,
                n=spec.n, t_min=T_MIN, t_max=T_MAX,
            )
        except (ValueError, RuntimeError) as e:
            logger.warning("envelope test failed in %s iter %d: %s",
                           spec.cell_id, iter_idx, e)
            continue

        wall_ms = int((time.perf_counter() - t0) * 1_000)
        records.append({
            "cell_id": spec.cell_id,
            "part": spec.part,
            "b_null": spec.b_null,
            "n": spec.n,
            "bracket": spec.bracket,
            "iter": iter_idx,
            "detected": bool(result["detected"]),
            "pval_global": float(result["pval_global"]),
            "n_bins_outside": int(result["n_bins_outside"]),
            "b_hat": float(fit["b"]),
            "log_likelihood": float(fit["log_likelihood"]),
            "converged": True,
            "seed_hex": seed_hex,
            "wall_ms": wall_ms,
        })
    return records


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    """Build grid, dispatch in parallel, write parquet + per-cell summary JSON."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path,
        default=Path("runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot"),
        help="Output directory.",
    )
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n_iter", type=int, default=100,
                        help="Iterations per cell.")
    parser.add_argument("--n_mc", type=int, default=500,
                        help="MC replicates per envelope test.")
    parser.add_argument("--n_jobs", type=int, default=-1,
                        help="joblib n_jobs (-1 = all cores).")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    # Load LIRE -- gives us (i) widths_pool for Part A and (ii) the full
    # corpus for Part B bootstrap.
    lire_path = Path("archive/data-2026-04-22/LIRE_v3-0.parquet")
    logger.info("Loading LIRE from %s", lire_path)
    df = P.load_filtered_lire(lire_path)
    logger.info("Filtered LIRE: %d rows", len(df))

    nb_pool = df["not_before"].to_numpy(dtype=float)
    na_pool = df["not_after"].to_numpy(dtype=float)
    widths_pool = (na_pool - nb_pool).astype(float)
    # Drop any zero-width rows from the empirical width pool (degenerate
    # intervals collapse to point dates, which break the fit).
    widths_pool = widths_pool[widths_pool > 0.0]
    logger.info("Width pool: %d non-degenerate rows; min=%.1f median=%.1f "
                "max=%.1f y", len(widths_pool), float(widths_pool.min()),
                float(np.median(widths_pool)), float(widths_pool.max()))

    bin_edges = P.BIN_EDGES
    bin_centres = P.BIN_CENTRES

    cells = enumerate_cells()
    logger.info("Grid: %d cells (Part A=%d, Part B=%d) x %d iter x %d MC",
                len(cells),
                sum(1 for c in cells if c.part == "A"),
                sum(1 for c in cells if c.part == "B"),
                args.n_iter, args.n_mc)

    master_ss = np.random.SeedSequence(args.seed)
    cell_seeds = master_ss.spawn(len(cells))

    t0 = time.time()
    logger.info("Dispatching %d cells with n_jobs=%d (loky)",
                len(cells), args.n_jobs)
    results_per_cell = Parallel(
        n_jobs=args.n_jobs, backend="loky", verbose=5,
    )(
        delayed(run_cell)(
            spec, widths_pool, nb_pool, na_pool,
            bin_edges, bin_centres,
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

    # Per-cell sanity summary; full SUMMARY.md is generated post-rsync.
    summary: dict = {}
    grouping = ["part", "b_null", "n", "bracket"]
    for keys, sub in res_df.groupby(grouping, dropna=False):
        # b_null may be NaN for Part B; turn into a string key.
        part, b_null, n, bracket = keys
        b_null_str = f"{b_null:+.4f}" if pd.notna(b_null) else "real"
        key = f"{part}/{b_null_str}/n{n}/{bracket}"
        # Restrict to converged runs for rate computation.
        sub_ok = sub[sub["converged"]] if "converged" in sub.columns else sub
        if len(sub_ok) == 0:
            summary[key] = {"n_iter": 0, "note": "no converged iterations"}
            continue
        summary[key] = {
            "n_iter": int(len(sub_ok)),
            "detection_rate": float(sub_ok["detected"].mean()),
            "median_pval": float(sub_ok["pval_global"].median()),
            "median_outside": float(sub_ok["n_bins_outside"].median()),
            "median_b_hat": float(sub_ok["b_hat"].median()),
            "median_wall_ms": float(sub_ok["wall_ms"].median()),
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
