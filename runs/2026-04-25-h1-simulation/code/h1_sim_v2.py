#!/usr/bin/env python3
"""
h1_sim_v2.py --- v2 driver for the H1 min-thresholds simulation.

Replaces ``h1_sim.py`` v1 per the forward-fit pilot's findings
(commits ``0974fa3``, ``7292807``, ``d3e0a74``, and ``9b37e1b``)
and the precision / scope decisions of 2026-04-26.

References to the project decision log (``planning/decision-log.md``):

  - **Decision 8 (2026-04-26):** Forward-fit nulls in true-date space
    (supersedes Decision 2's Poisson-on-fit MC). v1 fitted nulls in
    already-aoristic-smeared SPA space, which double-smeared the MC
    replicates and inflated FP to 1.000 at high n. v2 uses
    ``forward_fit.fit_null_exponential_forward`` and
    ``forward_fit_cpl.fit_null_cpl_forward`` -- both fit the parametric
    null directly on the per-row interval likelihood, then forward-apply
    the empirical aoristic mechanism to MC replicates. The H1
    simulation framework also moves from "bootstrap n rows from real
    LIRE" to "synthetic data drawn from a specified ground-truth null"
    so the simulation answers the proper power-calibration question.
  - **Decision 9 (2026-04-26):** Drop CPL k=2 from the primary cell
    grid (k=3 primary, k=4 exploratory upper bound; k=2 is documented
    as structurally underfit on the LIRE 3-knot AIC-best truth and
    excluded from primary). Also: optimise the forward-fit CPL
    objective via numba JIT (~5x speedup); rerun at the full
    preregistered precision n_iter = 1000, n_mc = 1000 with no
    wall-time cap.
  - **Decision 10 (2026-04-26):** Keep the ``c_20pc_25y`` bracket as
    a preregistered hard-test boundary in H1 but remove it from the
    H3b confirmatory eligibility list. Cells where detection < 0.80 at
    the level's maximum n are tagged ``min_n_unreachable: True`` in
    the post-run report rather than imputing extrapolated thresholds.

For exponential cells: synthetic data come from the truncated exponential
``f(t; b_null=0.005)`` -- a moderate growth shape that matches the
median ``b_hat`` observed in the forward-fit pilot's Part B real-LIRE
runs. For CPL cells: synthetic data come from the AIC-best CPL k=3 fit
on real LIRE (a realistic shape capturing growth-and-decline without
editorial spikes; computed once at module-load time and inlined as
``LIRE_CPL_TRUTH`` below).

Schema (parquet)
----------------
Per-iteration row, identical-where-possible to v1's Decision 8 schema
with one addition (``b_null_or_cpl_truth``) and one new field
(``min_n_unreachable``, populated post-run by the report builder):

    cell_id, level, bracket, shape, n, null_model, cpl_k, cpl_aic, iter,
    detected, pval_global, n_bins_outside, null_log_likelihood,
    b_hat, b_null_or_cpl_truth, province_counts, city_counts,
    seed_hex, wall_ms

Notable schema changes vs v1:
  - ``null_residual_rms`` (v1, smeared-space residual) replaced by
    ``null_log_likelihood`` (true-date interval log-likelihood).
  - ``b_hat`` added (NaN for CPL cells).
  - ``b_null_or_cpl_truth`` records the synthetic-data ground truth used
    per iteration (``"b={b}"`` for exp, ``"cpl_lire_aicbest"`` for CPL).
  - For CPL cells, k in {3, 4} are fit per iteration (k=2 dropped per
    Decision 9): 2 rows per CPL iteration. k=3 is the primary
    threshold-setting null; k=4 is reported as the k-sensitivity
    upper bound.

Unreachable-cell handling (per Decision 10): keep ``c_20pc_25y`` in
the v2 grid as a hard test. Cells that do not reach detection >= 0.80
at the maximum n in their level's sweep get ``min_n_unreachable: True``
in the post-run report, *not* an extrapolated threshold. The driver
itself only writes the per-iteration parquet; the unreachability tag is
computed in the report stage (``post_run_v2.py``) from the persisted
parquet.

Usage (from repo root):

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/h1_sim_v2.py \\
        --out runs/2026-04-25-h1-simulation/outputs/h1-v2 \\
        --seed 20260425 --n_iter 1000 --n_mc 1000 --n_jobs -1

No wall-time cap is enforced. The run completes when joblib reports
all cells done. Estimated sapphire wall-time at full precision after
the Decision 9 optimisation: ~4-7 hours.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25
(initial); updated 2026-04-26 for Decisions 8, 9, 10.
"""

from __future__ import annotations

import argparse
import collections
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

logger = logging.getLogger("h1_sim_v2")

# ---------------------------------------------------------------------------
# Run-wide constants
# ---------------------------------------------------------------------------

RANDOM_SEED = 20260425
T_MIN = -50.0
T_MAX = 350.0
CENTRE_YEAR = 150.0
N_ITERATIONS_DEFAULT = 1_000
N_MC_DEFAULT = 1_000
CPL_K_VALUES = (3, 4)  # k=2 dropped per Decision 9 (structurally underfit)

LEVEL_N_SWEEPS: dict[str, tuple[int, ...]] = {
    "empire":     (50_000,),
    "province":   (100, 250, 500, 1_000, 2_500, 5_000, 10_000, 25_000),
    "urban-area": (25, 50, 100, 250, 500, 1_000, 2_500),
}
BRACKET_NAMES = ("a_50pc_50y", "b_double_25y", "c_20pc_25y", "zero")
SHAPE_NAMES = ("step", "gaussian")
NULL_MODELS = ("exponential", "cpl")

# Synthetic ground truths.
B_NULL_TRUTH: float = 0.005  # exp ground-truth rate for power simulation
# AIC-best CPL k=3 fit on real LIRE (180,609 intervals), computed under
# n_restarts=12, seed=20260425. Pre-computed once and inlined here so
# every cell uses the same ground truth (no bootstrap).
LIRE_CPL_TRUTH: dict = {
    "knot_positions": np.array([25.42975781, 213.26566364, 280.14316364]),
    "knot_heights":   np.array([3.86324508e-05, 2.79243263e-03,
                                3.10599537e-03, 1.25029924e-04,
                                6.49470852e-03]),
    "log_likelihood": -310288.28,
    "aic": 620590.57,
    "converged": True,
    "n_obs": 180_609,
    "k": 3,
    "n_restarts_attempted": 12,
    "method": "cpl",
}


# ---------------------------------------------------------------------------
# Cell specification
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CellSpec:
    """Canonical specification for a single experimental cell."""
    cell_id: str
    level: str
    bracket: str
    shape: str
    n: int
    null_model: str
    n_iterations: int = N_ITERATIONS_DEFAULT
    n_mc: int = N_MC_DEFAULT


def enumerate_cells() -> list[CellSpec]:
    """Build the full v2 cell grid (matches v1's 256 cells)."""
    cells: list[CellSpec] = []
    for level, ns in LEVEL_N_SWEEPS.items():
        for bracket in BRACKET_NAMES:
            for shape in SHAPE_NAMES:
                for n in ns:
                    for null_model in NULL_MODELS:
                        cid = (
                            f"{level}_{bracket}_{shape}_n{n}_{null_model}"
                        )
                        cells.append(CellSpec(
                            cell_id=cid,
                            level=level,
                            bracket=bracket,
                            shape=shape,
                            n=n,
                            null_model=null_model,
                        ))
    return cells


# ---------------------------------------------------------------------------
# Synthetic-data simulation helpers
# ---------------------------------------------------------------------------

def _simulate_intervals_exp(
    n: int, b_null: float, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate n synthetic intervals from the exp ground truth."""
    u_t = rng.uniform(size=n)
    t_true = _truncated_exponential_inverse_cdf(u_t, b_null, T_MIN, T_MAX)
    w = rng.choice(widths_pool, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


def _simulate_intervals_cpl(
    n: int, truth: dict, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate n synthetic intervals from the CPL ground truth."""
    u_t = rng.uniform(size=n)
    t_true = _cpl_inverse_cdf(u_t, truth, T_MIN, T_MAX)
    w = rng.choice(widths_pool, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


# ---------------------------------------------------------------------------
# Cell executor
# ---------------------------------------------------------------------------

def _record(
    *, spec: CellSpec, iter_idx: int,
    detected: bool, pval_global: float, n_bins_outside: int,
    null_log_likelihood: float, b_hat: float,
    b_null_or_cpl_truth: str,
    province_counts: dict, city_counts: dict,
    seed_hex: str, wall_ms: int,
    cpl_k: int | float, cpl_aic: float,
    converged: bool,
) -> dict:
    """Build one v2 schema dict for parquet append."""
    return {
        "cell_id": spec.cell_id,
        "level": spec.level,
        "bracket": spec.bracket,
        "shape": spec.shape,
        "n": spec.n,
        "null_model": spec.null_model,
        "cpl_k": cpl_k,
        "cpl_aic": cpl_aic,
        "iter": iter_idx,
        "detected": detected,
        "pval_global": pval_global,
        "n_bins_outside": n_bins_outside,
        "null_log_likelihood": null_log_likelihood,
        "b_hat": b_hat,
        "b_null_or_cpl_truth": b_null_or_cpl_truth,
        "province_counts": province_counts,
        "city_counts": city_counts,
        "seed_hex": seed_hex,
        "wall_ms": wall_ms,
        "converged": converged,
    }


def run_cell(
    spec: CellSpec,
    widths_pool: np.ndarray,
    province_pool: np.ndarray,
    city_pool: np.ndarray,
    bin_edges: np.ndarray,
    bin_centres: np.ndarray,
    cell_seed: np.random.SeedSequence,
) -> list[dict]:
    """Execute all iterations for one cell.

    Per-iteration procedure (synthetic-data-from-null):
      1. Simulate n intervals from the ground-truth null (exp b_null=0.005
         or CPL LIRE-AIC-best).
      2. Aoristic-resample once -> ``spa_observed``.
      3. Inject the bracket effect on top -> ``spa_effect``.
      4. Forward-fit the parametric null on the synthetic intervals.
      5. Run forward-MC envelope test -> detected, pval, n_bins_outside.
      6. Record per-iteration row(s); CPL emits one row per k in {2, 3, 4}.

    Province / city "counts" are bootstrap-style draws from real LIRE
    province / city pools so v1's stratified-sampling exploratory analysis
    remains reconstructable from the v2 parquet, even though v2 never
    actually bootstraps from real LIRE.
    """
    records: list[dict] = []
    bracket_spec = P.BRACKETS[spec.bracket]

    iter_seeds = cell_seed.spawn(spec.n_iterations)

    for iter_idx, iter_ss in enumerate(iter_seeds):
        t0 = time.perf_counter()
        rng = np.random.default_rng(iter_ss)
        seed_hex = iter_ss.generate_state(4, dtype=np.uint32).tobytes().hex()

        # 1. Simulate intervals from the ground truth.
        if spec.null_model == "exponential":
            nb_iter, na_iter = _simulate_intervals_exp(
                spec.n, B_NULL_TRUTH, widths_pool, rng,
            )
            truth_label = f"b={B_NULL_TRUTH:+.4f}"
        else:  # cpl
            nb_iter, na_iter = _simulate_intervals_cpl(
                spec.n, LIRE_CPL_TRUTH, widths_pool, rng,
            )
            truth_label = "cpl_lire_aicbest"

        # 2. Aoristic-resample.
        years = rng.uniform(nb_iter, na_iter)
        spa_observed, _ = np.histogram(years, bins=bin_edges)
        spa_observed = spa_observed.astype(float)

        # 3. Inject effect.
        spa_effect = P.inject_effect(
            spa_observed, bin_centres,
            magnitude=bracket_spec.magnitude,
            centre_year=CENTRE_YEAR,
            duration=bracket_spec.duration,
            shape=spec.shape,
        )

        # Bootstrap province / city counts for stratified-sensitivity replay
        # (preserves the v1 schema's province_counts / city_counts so any
        # post-hoc stratified analysis can be run on v2 outputs too).
        pc_idx = rng.integers(0, len(province_pool), size=spec.n)
        province_draw = province_pool[pc_idx]
        city_draw = city_pool[pc_idx]
        province_counts = {
            str(k): int(v) for k, v in
            collections.Counter(province_draw.tolist()).items()
            if k is not None and str(k) != ""
        }
        city_counts = {
            str(k): int(v) for k, v in
            collections.Counter(city_draw.tolist()).items()
            if k is not None and str(k) != "" and str(k) != "nan"
        }

        # 4. + 5. Fit null and run envelope test, branching on null model.
        widths_iter = na_iter - nb_iter
        if spec.null_model == "exponential":
            try:
                fit = fit_null_exponential_forward(
                    np.column_stack([nb_iter, na_iter]),
                    t_min=T_MIN, t_max=T_MAX,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("exp fit failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            try:
                result = forward_envelope_test(
                    spa_effect, fit["b"], widths_iter, bin_edges,
                    spec.n_mc, rng, n=spec.n, t_min=T_MIN, t_max=T_MAX,
                )
            except (ValueError, RuntimeError) as exc:
                logger.warning("exp envelope failed in %s iter %d: %s",
                               spec.cell_id, iter_idx, exc)
                continue
            wall_ms = int((time.perf_counter() - t0) * 1_000)
            records.append(_record(
                spec=spec, iter_idx=iter_idx,
                detected=bool(result["detected"]),
                pval_global=float(result["pval_global"]),
                n_bins_outside=int(result["n_bins_outside"]),
                null_log_likelihood=float(fit["log_likelihood"]),
                b_hat=float(fit["b"]),
                b_null_or_cpl_truth=truth_label,
                province_counts=province_counts,
                city_counts=city_counts,
                seed_hex=seed_hex,
                wall_ms=wall_ms,
                cpl_k=float("nan"),
                cpl_aic=float("nan"),
                converged=bool(fit["converged"]),
            ))
        elif spec.null_model == "cpl":
            # Fit k=2, 3, 4 per iteration (v1 convention).
            fit_seed = int(iter_ss.generate_state(1, dtype=np.uint32)[0])
            for k in CPL_K_VALUES:
                try:
                    fit = fit_null_cpl_forward(
                        np.column_stack([nb_iter, na_iter]),
                        k=k, t_min=T_MIN, t_max=T_MAX,
                        n_restarts=8, seed=fit_seed + k,
                    )
                except (ValueError, RuntimeError) as exc:
                    logger.warning("CPL k=%d fit failed in %s iter %d: %s",
                                   k, spec.cell_id, iter_idx, exc)
                    continue
                if not fit["converged"]:
                    wall_ms = int((time.perf_counter() - t0) * 1_000)
                    records.append(_record(
                        spec=spec, iter_idx=iter_idx,
                        detected=False, pval_global=float("nan"),
                        n_bins_outside=-1,
                        null_log_likelihood=float(fit["log_likelihood"]),
                        b_hat=float("nan"),
                        b_null_or_cpl_truth=truth_label,
                        province_counts=province_counts,
                        city_counts=city_counts,
                        seed_hex=seed_hex, wall_ms=wall_ms,
                        cpl_k=k, cpl_aic=float(fit["aic"]),
                        converged=False,
                    ))
                    continue
                try:
                    result = forward_envelope_test_cpl(
                        spa_effect, fit, widths_iter, bin_edges,
                        spec.n_mc, rng, n=spec.n, t_min=T_MIN, t_max=T_MAX,
                    )
                except (ValueError, RuntimeError) as exc:
                    logger.warning("CPL envelope failed k=%d in %s iter %d: %s",
                                   k, spec.cell_id, iter_idx, exc)
                    continue
                wall_ms = int((time.perf_counter() - t0) * 1_000)
                records.append(_record(
                    spec=spec, iter_idx=iter_idx,
                    detected=bool(result["detected"]),
                    pval_global=float(result["pval_global"]),
                    n_bins_outside=int(result["n_bins_outside"]),
                    null_log_likelihood=float(fit["log_likelihood"]),
                    b_hat=float("nan"),
                    b_null_or_cpl_truth=truth_label,
                    province_counts=province_counts,
                    city_counts=city_counts,
                    seed_hex=seed_hex, wall_ms=wall_ms,
                    cpl_k=k, cpl_aic=float(fit["aic"]),
                    converged=True,
                ))
        else:
            raise ValueError(f"Unknown null_model: {spec.null_model}")

    return records


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--data",
        default="archive/data-2026-04-22/LIRE_v3-0.parquet",
        help="Path to LIRE parquet (relative to repo root or absolute). "
        "Used only to derive the empirical width pool for synthetic "
        "interval generation; intervals themselves are *not* bootstrapped.",
    )
    parser.add_argument(
        "--out",
        default="runs/2026-04-25-h1-simulation/outputs/h1-v2",
        help="Output directory.",
    )
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n_jobs", type=int, default=-1)
    parser.add_argument(
        "--n_iter", type=int, default=N_ITERATIONS_DEFAULT,
        help="Iterations per cell (override for smoke tests).",
    )
    parser.add_argument(
        "--n_mc", type=int, default=N_MC_DEFAULT,
        help="MC replicates per envelope test (override for smoke tests).",
    )
    parser.add_argument(
        "--cells", type=int, default=None,
        help="Limit to first N cells (debugging only).",
    )
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=args.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = out_dir / "cell-results.parquet"

    # Load LIRE for widths_pool + province_pool + city_pool.
    source_df = P.load_filtered_lire(args.data)
    nb = source_df["not_before"].to_numpy(dtype=float)
    na = source_df["not_after"].to_numpy(dtype=float)
    widths_pool = (na - nb).astype(float)
    widths_pool = widths_pool[widths_pool > 0.0]
    province_pool = source_df["province"].to_numpy()
    city_pool = source_df["urban_context_city"].to_numpy()
    logger.info(
        "Loaded LIRE: %d rows; width pool %d non-degenerate; "
        "median width %.1f y",
        len(source_df), len(widths_pool), float(np.median(widths_pool)),
    )

    cells = enumerate_cells()
    if args.cells:
        cells = cells[: args.cells]
        logger.warning("Debug: limiting to first %d cells", len(cells))

    # Override iteration / MC counts into cells if user set non-default.
    if args.n_iter != N_ITERATIONS_DEFAULT or args.n_mc != N_MC_DEFAULT:
        cells = [
            CellSpec(
                cell_id=c.cell_id, level=c.level, bracket=c.bracket,
                shape=c.shape, n=c.n, null_model=c.null_model,
                n_iterations=args.n_iter, n_mc=args.n_mc,
            )
            for c in cells
        ]

    logger.info(
        "Executing %d cells; iterations=%d mc=%d n_jobs=%d",
        len(cells), args.n_iter, args.n_mc, args.n_jobs,
    )

    master_ss = np.random.SeedSequence(args.seed)
    cell_seeds = master_ss.spawn(len(cells))

    t_start = time.perf_counter()
    with Parallel(n_jobs=args.n_jobs, backend="loky", verbose=5) as pool:
        results = pool(
            delayed(run_cell)(
                spec, widths_pool, province_pool, city_pool,
                P.BIN_EDGES, P.BIN_CENTRES, cell_seed,
            )
            for spec, cell_seed in zip(cells, cell_seeds)
        )
    wall_total = time.perf_counter() - t_start
    logger.info("Completed %d cells in %.1f s (%.1f min)",
                len(cells), wall_total, wall_total / 60.0)

    flat = [rec for cell_recs in results for rec in cell_recs]
    df_out = pd.DataFrame(flat)
    logger.info("Writing %d rows --> %s", len(df_out), parquet_path)
    df_out.to_parquet(parquet_path, index=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
