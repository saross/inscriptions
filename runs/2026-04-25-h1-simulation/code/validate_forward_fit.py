#!/usr/bin/env python3
"""
validate_forward_fit.py --- forward-fit pilot, multi-part validation.

This is the gating experiment for the forward-fit methodology. It tests
whether fitting parametric nulls in *true-date* space (treating each
inscription's interval as an integration range) and forward-applying the
empirical aoristic mechanism to MC replicates controls the false-positive
(FP) rate at the nominal alpha = 0.05 across a representative grid.

Three-part design
-----------------
Part A (exp) --- *Synthetic-data* FP and detection for the exponential
null. For each cell ``(b_null, n, bracket)``:
  1. Sample n true dates from f(t; b_null) on [-50, 350].
  2. Sample n widths from the real LIRE width distribution (with replacement).
  3. Random uniform interval positions; construct synthetic [nb, na] rows.
  4. Aoristic-resample once -> synthetic_spa.
  5. Inject the bracket effect (zero magnitude is identity).
  6. Forward-fit the exponential on the synthetic intervals -> b_hat.
  7. Run forward-MC envelope test using b_hat + the row widths -> detected, p.
Cells: 3 b_null x 3 n x 3 bracket = 27 cells.

Part A.cpl --- *Synthetic-data* FP and detection for the CPL k=3 null.
Same grid pattern but with CPL ground truths in place of ``b_null``:
  - cpl_const : near-uniform (boring shape)
  - cpl_peaked: boom-bust (peaked at the envelope mid-point)
  - cpl_asymm : asymmetric (rising-then-falling, off-centre peak)
For each cell: simulate from the ground-truth CPL, fit CPL k=3, run forward
CPL envelope. Cells: 3 truth x 3 n x 3 bracket = 27 cells.

Part B --- *Real-LIRE bootstrap* FP for the exponential null. For each
n in {500, 2500, 10000}, bootstrap from the real filtered LIRE corpus
(zero bracket only). FP is *expected* to be elevated here because real
LIRE has editorial spikes and other non-exponential structure --
diagnostic, not a gate.

Part C --- *Real-LIRE bootstrap* FP for the CPL k=3 null. For each
n in {500, 2500, 10000}, bootstrap from filtered LIRE; fit CPL k=3 on
the bootstrap intervals; run forward CPL envelope. Zero bracket only.
Expectation: lower FP than Part B because CPL absorbs more of LIRE's
structure (e.g. editorial spikes, boom-bust shape) into the fitted null.
If Part C still hits 1.000, that means LIRE's structure exceeds CPL k=3's
flexibility -- itself an informative finding.

Output schema (parquet)
-----------------------

    cell_id, part, method, n, bracket, iter, detected, pval_global,
    n_bins_outside, converged,
    b_null, b_hat,                            # Exp parts (NaN for CPL)
    cpl_truth, cpl_k, cpl_aic, log_likelihood, # CPL parts
    seed_hex, wall_ms

Usage
-----

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/\\
        validate_forward_fit.py \\
        --out runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot \\
        --seed 20260425 --n_iter 100 --n_mc 500 --n_jobs -1 \\
        [--include_cpl]    # adds Part A.cpl and Part C
        [--cpl_only]       # runs only Part A.cpl and Part C (skips A and B)

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
from forward_fit_cpl import (  # noqa: E402
    _cpl_inverse_cdf,
    _normaliser,
    fit_null_cpl_forward,
    forward_envelope_test_cpl,
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

# Part A (exp) grid.
PART_A_B_NULLS: tuple[float, ...] = (-0.005, 0.0, 0.005)
PART_A_NS: tuple[int, ...] = (500, 2_500, 10_000)
PART_A_BRACKETS: dict[str, dict] = {
    "zero":         {"magnitude":  0.0, "duration": 50.0, "shape": "step"},
    "a_50pc_50y":   {"magnitude": -0.5, "duration": 50.0, "shape": "step"},
    "c_20pc_25y":   {"magnitude": -0.2, "duration": 25.0, "shape": "step"},
}

# Part A.cpl ground truths. Each entry has ``interior_xs`` (length k=3)
# and ``heights`` (length 5, will be normalised at simulate time).
PART_A_CPL_TRUTHS: dict[str, dict] = {
    "cpl_const": {
        # Near-uniform (slight wiggle so it's not a perfect line).
        "interior_xs": np.array([50.0, 150.0, 250.0]),
        "heights": np.array([1.0, 1.05, 0.95, 1.05, 1.0]),
    },
    "cpl_peaked": {
        # Boom-bust: rising to a peak in the middle, then declining.
        "interior_xs": np.array([50.0, 150.0, 250.0]),
        "heights": np.array([0.3, 0.8, 1.8, 0.8, 0.3]),
    },
    "cpl_asymm": {
        # Asymmetric: ramp up to a late-mid peak, then sharp decline.
        "interior_xs": np.array([0.0, 150.0, 220.0]),
        "heights": np.array([0.4, 0.6, 1.6, 1.0, 0.3]),
    },
}

# Part B (real LIRE bootstrap, exp null).
PART_B_NS: tuple[int, ...] = (500, 2_500, 10_000)
PART_B_BRACKET = "zero"

# Part C (real LIRE bootstrap, CPL k=3 null).
PART_C_NS: tuple[int, ...] = (500, 2_500, 10_000)
PART_C_BRACKET = "zero"
CPL_K_PRIMARY: int = 3

RANDOM_SEED: int = 20260425


@dataclass(frozen=True)
class CellSpec:
    """Spec for a single (part, generator, n, bracket) cell.

    For Parts A/B (exp): ``b_null`` is the generator (NaN for B);
    ``cpl_truth`` is empty.
    For Parts A.cpl/C (CPL): ``cpl_truth`` names the generator (empty for
    C, which uses real-LIRE bootstrap); ``b_null`` is NaN.
    ``method`` distinguishes "exponential" / "cpl".
    """
    cell_id: str
    part: str             # "A", "A.cpl", "B", "C"
    method: str           # "exponential" | "cpl"
    n: int
    bracket: str
    b_null: float = float("nan")
    cpl_truth: str = ""


def enumerate_cells(
    include_exp: bool = True, include_cpl: bool = True,
) -> list[CellSpec]:
    """Build the cell grid, gated by include flags.

    Returns deterministic ordering by (part, generator, n, bracket).
    """
    cells: list[CellSpec] = []
    if include_exp:
        # Part A: synthetic-data exp.
        for b_null in PART_A_B_NULLS:
            for n in PART_A_NS:
                for bracket in PART_A_BRACKETS:
                    cid = f"A_b{b_null:+.3f}_n{n}_{bracket}"
                    cells.append(CellSpec(
                        cell_id=cid, part="A", method="exponential",
                        n=n, bracket=bracket, b_null=b_null,
                    ))
        # Part B: real LIRE bootstrap exp.
        for n in PART_B_NS:
            cid = f"B_realLIRE_n{n}_{PART_B_BRACKET}"
            cells.append(CellSpec(
                cell_id=cid, part="B", method="exponential",
                n=n, bracket=PART_B_BRACKET,
            ))
    if include_cpl:
        # Part A.cpl: synthetic-data CPL.
        for cpl_name in PART_A_CPL_TRUTHS:
            for n in PART_A_NS:
                for bracket in PART_A_BRACKETS:
                    cid = f"Acpl_{cpl_name}_n{n}_{bracket}"
                    cells.append(CellSpec(
                        cell_id=cid, part="A.cpl", method="cpl",
                        n=n, bracket=bracket, cpl_truth=cpl_name,
                    ))
        # Part C: real LIRE bootstrap CPL.
        for n in PART_C_NS:
            cid = f"C_realLIRE_n{n}_{PART_C_BRACKET}"
            cells.append(CellSpec(
                cell_id=cid, part="C", method="cpl",
                n=n, bracket=PART_C_BRACKET,
            ))
    return cells


# ---------------------------------------------------------------------------
# Simulation helpers
# ---------------------------------------------------------------------------

def _build_truth_dict(name: str) -> dict:
    """Build a CPL-fit-result-style dict for a named ground truth.

    Heights are renormalised so the density integrates to 1 over the envelope.
    """
    spec = PART_A_CPL_TRUTHS[name]
    interior = np.asarray(spec["interior_xs"], dtype=float)
    heights = np.asarray(spec["heights"], dtype=float)
    xs = np.concatenate([[T_MIN], interior, [T_MAX]])
    Z = _normaliser(xs, heights)
    return {
        "knot_positions": interior,
        "knot_heights": heights / Z,
        "log_likelihood": float("nan"),
        "aic": float("nan"),
        "converged": True,
        "n_obs": -1,
        "k": int(len(interior)),
        "n_restarts_attempted": 0,
        "method": "cpl",
    }


def _simulate_exp_intervals(
    b_null: float, n: int, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate ``n`` synthetic intervals from f(t; b_null) (exp truth)."""
    u_t = rng.uniform(size=n)
    t_true = _truncated_exponential_inverse_cdf(u_t, b_null, T_MIN, T_MAX)
    w = rng.choice(widths_pool, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


def _simulate_cpl_intervals(
    truth: dict, n: int, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate ``n`` synthetic intervals from a CPL ground truth."""
    u_t = rng.uniform(size=n)
    t_true = _cpl_inverse_cdf(u_t, truth, T_MIN, T_MAX)
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


# ---------------------------------------------------------------------------
# Per-cell executor
# ---------------------------------------------------------------------------

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

    Branches on (part, method) to choose simulator + fitter + envelope.
    """
    iter_seeds = cell_seed.spawn(n_iter)
    bracket = PART_A_BRACKETS[spec.bracket]

    truth_obj: dict | None = None
    if spec.part == "A.cpl":
        truth_obj = _build_truth_dict(spec.cpl_truth)

    records: list[dict] = []
    for iter_idx, iter_ss in enumerate(iter_seeds):
        t0 = time.perf_counter()
        rng = np.random.default_rng(iter_ss)
        seed_hex = iter_ss.generate_state(4, dtype=np.uint32).tobytes().hex()

        # 1. Build intervals according to part.
        try:
            if spec.part == "A":
                nb_iter, na_iter = _simulate_exp_intervals(
                    spec.b_null, spec.n, widths_pool, rng,
                )
            elif spec.part == "A.cpl":
                nb_iter, na_iter = _simulate_cpl_intervals(
                    truth_obj, spec.n, widths_pool, rng,
                )
            elif spec.part in ("B", "C"):
                nb_iter, na_iter = _bootstrap_real_intervals(
                    nb_pool, na_pool, spec.n, rng,
                )
            else:
                raise ValueError(f"Unknown part: {spec.part}")
        except (ValueError, RuntimeError) as exc:
            logger.warning("simulation failed in %s iter %d: %s",
                           spec.cell_id, iter_idx, exc)
            continue

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

        # 4. Fit + envelope test based on method.
        if spec.method == "exponential":
            try:
                fit = fit_null_exponential_forward(
                    np.column_stack([nb_iter, na_iter]),
                    t_min=T_MIN, t_max=T_MAX,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("exp fit failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            converged = bool(fit["converged"])
            if not converged:
                wall_ms = int((time.perf_counter() - t0) * 1_000)
                records.append(_make_record(
                    spec, iter_idx, detected=False, pval=float("nan"),
                    n_outside=-1, converged=False,
                    b_hat=fit["b"], log_likelihood=fit["log_likelihood"],
                    cpl_aic=float("nan"), seed_hex=seed_hex, wall_ms=wall_ms,
                ))
                continue
            widths_iter = na_iter - nb_iter
            try:
                result = forward_envelope_test(
                    spa_effect, fit["b"], widths_iter, bin_edges,
                    n_mc, rng, n=spec.n, t_min=T_MIN, t_max=T_MAX,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("exp envelope failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            wall_ms = int((time.perf_counter() - t0) * 1_000)
            records.append(_make_record(
                spec, iter_idx,
                detected=bool(result["detected"]),
                pval=float(result["pval_global"]),
                n_outside=int(result["n_bins_outside"]),
                converged=True,
                b_hat=float(fit["b"]),
                log_likelihood=float(fit["log_likelihood"]),
                cpl_aic=float("nan"),
                seed_hex=seed_hex, wall_ms=wall_ms,
            ))
        elif spec.method == "cpl":
            try:
                fit_seed = int(iter_ss.generate_state(1, dtype=np.uint32)[0])
                fit = fit_null_cpl_forward(
                    np.column_stack([nb_iter, na_iter]),
                    k=CPL_K_PRIMARY, t_min=T_MIN, t_max=T_MAX,
                    n_restarts=8, seed=fit_seed,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("CPL fit failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            converged = bool(fit["converged"])
            if not converged:
                wall_ms = int((time.perf_counter() - t0) * 1_000)
                records.append(_make_record(
                    spec, iter_idx, detected=False, pval=float("nan"),
                    n_outside=-1, converged=False,
                    b_hat=float("nan"),
                    log_likelihood=float(fit["log_likelihood"]),
                    cpl_aic=float(fit["aic"]),
                    seed_hex=seed_hex, wall_ms=wall_ms,
                ))
                continue
            widths_iter = na_iter - nb_iter
            try:
                result = forward_envelope_test_cpl(
                    spa_effect, fit, widths_iter, bin_edges,
                    n_mc, rng, n=spec.n, t_min=T_MIN, t_max=T_MAX,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("CPL envelope failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            wall_ms = int((time.perf_counter() - t0) * 1_000)
            records.append(_make_record(
                spec, iter_idx,
                detected=bool(result["detected"]),
                pval=float(result["pval_global"]),
                n_outside=int(result["n_bins_outside"]),
                converged=True,
                b_hat=float("nan"),
                log_likelihood=float(fit["log_likelihood"]),
                cpl_aic=float(fit["aic"]),
                seed_hex=seed_hex, wall_ms=wall_ms,
            ))
        else:
            raise ValueError(f"Unknown method: {spec.method}")
    return records


def _make_record(
    spec: CellSpec, iter_idx: int,
    *, detected: bool, pval: float, n_outside: int, converged: bool,
    b_hat: float, log_likelihood: float, cpl_aic: float,
    seed_hex: str, wall_ms: int,
) -> dict:
    """Build a per-iteration record matching the parquet schema."""
    return {
        "cell_id": spec.cell_id,
        "part": spec.part,
        "method": spec.method,
        "n": spec.n,
        "bracket": spec.bracket,
        "b_null": spec.b_null,
        "cpl_truth": spec.cpl_truth,
        "cpl_k": CPL_K_PRIMARY if spec.method == "cpl" else -1,
        "iter": iter_idx,
        "detected": detected,
        "pval_global": pval,
        "n_bins_outside": n_outside,
        "converged": converged,
        "b_hat": b_hat,
        "log_likelihood": log_likelihood,
        "cpl_aic": cpl_aic,
        "seed_hex": seed_hex,
        "wall_ms": wall_ms,
    }


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
    parser.add_argument("--include_cpl", action="store_true",
                        help="Include Part A.cpl + Part C (CPL extension).")
    parser.add_argument("--cpl_only", action="store_true",
                        help="Run only Part A.cpl + Part C (skip A and B).")
    parser.add_argument("--results_filename", type=str,
                        default="results.parquet",
                        help="Filename for the per-iteration parquet.")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    include_exp = not args.cpl_only
    include_cpl = args.include_cpl or args.cpl_only

    # Load LIRE for widths_pool (Part A) + bootstrap pools (Parts B, C).
    lire_path = Path("archive/data-2026-04-22/LIRE_v3-0.parquet")
    logger.info("Loading LIRE from %s", lire_path)
    df = P.load_filtered_lire(lire_path)
    logger.info("Filtered LIRE: %d rows", len(df))

    nb_pool = df["not_before"].to_numpy(dtype=float)
    na_pool = df["not_after"].to_numpy(dtype=float)
    widths_pool = (na_pool - nb_pool).astype(float)
    widths_pool = widths_pool[widths_pool > 0.0]
    logger.info("Width pool: %d non-degenerate rows; min=%.1f median=%.1f "
                "max=%.1f y", len(widths_pool), float(widths_pool.min()),
                float(np.median(widths_pool)), float(widths_pool.max()))

    bin_edges = P.BIN_EDGES
    bin_centres = P.BIN_CENTRES

    cells = enumerate_cells(include_exp=include_exp, include_cpl=include_cpl)
    n_part_a = sum(1 for c in cells if c.part == "A")
    n_part_acpl = sum(1 for c in cells if c.part == "A.cpl")
    n_part_b = sum(1 for c in cells if c.part == "B")
    n_part_c = sum(1 for c in cells if c.part == "C")
    logger.info(
        "Grid: %d cells (A=%d, A.cpl=%d, B=%d, C=%d) x %d iter x %d MC",
        len(cells), n_part_a, n_part_acpl, n_part_b, n_part_c,
        args.n_iter, args.n_mc,
    )

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

    all_records: list[dict] = []
    for cell_records in results_per_cell:
        all_records.extend(cell_records)

    res_df = pd.DataFrame(all_records)
    out_parquet = args.out / args.results_filename
    res_df.to_parquet(out_parquet, index=False)
    logger.info("Wrote %s (%d rows)", out_parquet, len(res_df))

    # Per-cell sanity summary.
    summary: dict = {}
    grouping = ["part", "method", "n", "bracket", "b_null", "cpl_truth"]
    for keys, sub in res_df.groupby(grouping, dropna=False):
        part, method, n, bracket, b_null, cpl_truth = keys
        if method == "exponential":
            gen_str = (
                f"{b_null:+.4f}" if not pd.isna(b_null) else "real"
            )
        else:
            gen_str = (cpl_truth if cpl_truth and cpl_truth != ""
                       else "real")
        key = f"{part}/{method}/{gen_str}/n{n}/{bracket}"
        sub_ok = sub[sub["converged"]] if "converged" in sub.columns else sub
        if len(sub_ok) == 0:
            summary[key] = {"n_iter": 0, "note": "no converged iterations"}
            continue
        summary[key] = {
            "n_iter": int(len(sub_ok)),
            "detection_rate": float(sub_ok["detected"].mean()),
            "median_pval": float(sub_ok["pval_global"].median()),
            "median_outside": float(sub_ok["n_bins_outside"].median()),
            "median_wall_ms": float(sub_ok["wall_ms"].median()),
        }
        if method == "exponential":
            summary[key]["median_b_hat"] = float(sub_ok["b_hat"].median())
        else:
            summary[key]["median_cpl_aic"] = float(sub_ok["cpl_aic"].median())

    # Choose summary filename to avoid overwriting the existing exp-only
    # summary.json when running CPL-only or the all-up extended run.
    if args.cpl_only:
        summary_filename = "summary-cpl.json"
    elif args.include_cpl:
        summary_filename = "summary-extended.json"
    else:
        summary_filename = "summary.json"
    out_summary = args.out / summary_filename
    with out_summary.open("w") as f:
        json.dump({
            "args": {
                "n_iter": args.n_iter, "n_mc": args.n_mc,
                "seed": args.seed, "n_jobs": args.n_jobs,
                "include_cpl": include_cpl, "cpl_only": args.cpl_only,
            },
            "elapsed_seconds": elapsed,
            "n_cells": len(cells),
            "n_rows": len(res_df),
            "by_cell": summary,
        }, f, indent=2)
    logger.info("Wrote %s", out_summary)


if __name__ == "__main__":
    main()
