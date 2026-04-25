#!/usr/bin/env python3
"""
h1_sim.py --- Driver for the H1 min-thresholds simulation.

Enumerates the 256-cell experimental grid (Decision 2 of decisions.md),
dispatches cells to a ``joblib.Parallel`` worker pool with strict
``SeedSequence`` discipline, and writes ``cell-results.parquet`` to
the per-run outputs directory.

Grid (Decision summary table):
  - Subset levels: empire / province / urban-area
  - Brackets: a_50pc_50y / b_double_25y / c_20pc_25y / zero
  - Shapes: step / gaussian
  - Null models: exponential (primary), cpl (secondary)
  - n-sweep:
      empire: {50000}
      province: {100, 250, 500, 1000, 2500, 5000, 10000, 25000}
      urban-area: {25, 50, 100, 250, 500, 1000, 2500}
  - Iterations per cell: 1,000
  - MC replicates per test: 1,000
  - CPL k values: {2, 3, 4} (three rows per iteration for CPL cells)

Per-iteration persistence schema (Decision 8 of decisions.md):

    cell_id, level, bracket, shape, n, null_model, cpl_k, cpl_aic, iter,
    detected, pval_global, n_bins_outside, null_residual_rms,
    province_counts (dict), city_counts (dict), seed_hex, wall_ms

Seed discipline (plan.md §8): master ``np.random.SeedSequence(20260425)``
spawns per-cell sequences, which in turn spawn per-iteration sequences.
No global ``np.random.seed()`` calls.

Modes:
  --mode=simulate (default): run the full grid.
  --mode=report              : rebuild plots and thresholds from existing parquet.

Usage (from repo root):

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/h1_sim.py \\
        --out runs/2026-04-25-h1-simulation/outputs \\
        --n-jobs -1 2>&1 | tee runs/2026-04-25-h1-simulation/outputs/run.log

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import argparse
import collections
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

# Ensure this module is importable when run as a script and also when imported.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (  # noqa: E402
    BIN_CENTRES,
    BIN_EDGES,
    BRACKETS,
    N_BINS,
    aoristic_resample,
    fit_null_cpl,
    fit_null_exponential,
    inject_effect,
    load_filtered_lire,
    permutation_envelope_test,
)

logger = logging.getLogger("h1_sim")

# ---------------------------------------------------------------------------
# Run-wide constants
# ---------------------------------------------------------------------------

RANDOM_SEED = 20260425  # Decision summary table
CENTRE_YEAR = 150.0     # midpoint of 50 BC -- AD 350 envelope
N_ITERATIONS_DEFAULT = 1_000
N_MC_DEFAULT = 1_000
CPL_K_VALUES = (2, 3, 4)

LEVEL_N_SWEEPS: dict[str, tuple[int, ...]] = {
    "empire": (50_000,),
    "province": (100, 250, 500, 1_000, 2_500, 5_000, 10_000, 25_000),
    "urban-area": (25, 50, 100, 250, 500, 1_000, 2_500),
}

BRACKET_NAMES = ("a_50pc_50y", "b_double_25y", "c_20pc_25y", "zero")
SHAPE_NAMES = ("step", "gaussian")
NULL_MODELS = ("exponential", "cpl")


# ---------------------------------------------------------------------------
# Cell specification
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CellSpec:
    """Canonical specification for a single experimental cell.

    A cell combines one (level, bracket, shape, n, null_model) tuple.
    For CPL cells, all ``k`` in ``CPL_K_VALUES`` are fit per iteration;
    one parquet row is emitted per (iteration, k) combination, so CPL cells
    produce 3 rows per iteration and exponential cells produce 1 row.
    """
    cell_id: str
    level: str
    bracket: str
    shape: str
    n: int
    null_model: str
    n_iterations: int = N_ITERATIONS_DEFAULT
    n_mc: int = N_MC_DEFAULT


def enumerate_cells() -> list[CellSpec]:
    """Build the full 256-cell grid.

    Returns
    -------
    list[CellSpec]
        Deterministic ordering by (level, bracket, shape, n, null_model).
    """
    cells: list[CellSpec] = []
    for level, ns in LEVEL_N_SWEEPS.items():
        for bracket in BRACKET_NAMES:
            for shape in SHAPE_NAMES:
                for n in ns:
                    for null_model in NULL_MODELS:
                        cid = f"{level}_{bracket}_{shape}_n{n}_{null_model}"
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
# Cell executor
# ---------------------------------------------------------------------------

def _record_from_iteration(
    *,
    spec: CellSpec,
    iter_idx: int,
    detected: bool,
    pval_global: float,
    n_bins_outside: int,
    null_residual_rms: float,
    province_counts: dict,
    city_counts: dict,
    seed_hex: str,
    wall_ms: int,
    cpl_k: int | float,
    cpl_aic: float,
) -> dict:
    """Build one Decision-8-schema dict for parquet append."""
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
        "null_residual_rms": null_residual_rms,
        "province_counts": province_counts,
        "city_counts": city_counts,
        "seed_hex": seed_hex,
        "wall_ms": wall_ms,
    }


def run_cell(
    spec: CellSpec,
    source_df: pd.DataFrame,
    cell_seed: np.random.SeedSequence,
) -> list[dict]:
    """Execute all iterations for one cell.

    Parameters
    ----------
    spec : CellSpec
        Cell specification.
    source_df : pandas.DataFrame
        Filtered LIRE frame. Broadcast read-only across workers by joblib.
    cell_seed : numpy.random.SeedSequence
        Per-cell SeedSequence; spawns iteration-level sequences.

    Returns
    -------
    list[dict]
        One dict per (iteration, [k]) combination, Decision-8 schema.
    """
    records: list[dict] = []
    bracket_spec = BRACKETS[spec.bracket]

    # Effective n --- empire level may cap at df size.
    effective_n = min(spec.n, len(source_df)) if spec.level == "empire" else spec.n
    if effective_n != spec.n:
        logger.info(
            "%s: capped n from %d to %d (df size)",
            spec.cell_id, spec.n, effective_n,
        )

    iter_seeds = cell_seed.spawn(spec.n_iterations)

    for iter_idx, iter_ss in enumerate(iter_seeds):
        t0 = time.perf_counter()
        rng = np.random.default_rng(iter_ss)
        # Derive a per-iteration seed_hex from the SeedSequence's *full* state
        # (entropy + spawn_key path). ``iter_ss.entropy`` alone is identical
        # across spawned children, so we use ``generate_state`` to obtain a
        # 128-bit deterministic fingerprint that varies per iter_idx.
        seed_hex = iter_ss.generate_state(4, dtype=np.uint32).tobytes().hex()

        # 1. Draw bootstrap sample and build observed SPA.
        nb = source_df["not_before"].to_numpy(dtype=float)
        na = source_df["not_after"].to_numpy(dtype=float)
        idx = rng.integers(0, len(source_df), size=effective_n)
        lo_years = nb[idx]
        hi_years = na[idx]
        drawn_years = rng.uniform(lo_years, hi_years)
        spa_observed, _ = np.histogram(drawn_years, bins=BIN_EDGES)
        spa_observed = spa_observed.astype(float)

        # Record province / city counts for stratified-sensitivity replay.
        provs = source_df["province"].to_numpy()[idx]
        cities = source_df["urban_context_city"].to_numpy()[idx]
        province_counts = dict(collections.Counter(provs.tolist()))
        # Drop None / empty keys for compactness.
        province_counts = {
            str(k): int(v) for k, v in province_counts.items()
            if k is not None and str(k) != ""
        }
        city_counts = {
            str(k): int(v) for k, v in collections.Counter(cities.tolist()).items()
            if k is not None and str(k) != "" and str(k) != "nan"
        }

        # 2. Inject effect on the observed SPA (this is the "effect-present"
        # realisation the envelope test will flag against the null).
        spa_effect = inject_effect(
            spa_observed,
            BIN_CENTRES,
            magnitude=bracket_spec.magnitude,
            centre_year=CENTRE_YEAR,
            duration=bracket_spec.duration,
            shape=spec.shape,
        )

        # 3. Fit null model(s).
        if spec.null_model == "exponential":
            null_fit = fit_null_exponential(spa_observed, BIN_CENTRES)
            result = permutation_envelope_test(
                observed_spa=spa_effect,
                null_params=null_fit,
                model="exponential",
                bin_centres=BIN_CENTRES,
                n_mc=spec.n_mc,
                rng=rng,
                alpha=0.05,
            )
            wall_ms = int((time.perf_counter() - t0) * 1_000)
            records.append(_record_from_iteration(
                spec=spec,
                iter_idx=iter_idx,
                detected=result["detected"],
                pval_global=result["pval_global"],
                n_bins_outside=result["n_bins_outside"],
                null_residual_rms=null_fit["residual_rms"],
                province_counts=province_counts,
                city_counts=city_counts,
                seed_hex=seed_hex,
                wall_ms=wall_ms,
                cpl_k=float("nan"),
                cpl_aic=float("nan"),
            ))
        elif spec.null_model == "cpl":
            # Fit k = 2, 3, 4 separately. On fit failure, fall back to
            # exponential null for that k (logged in cpl_k metadata).
            for k in CPL_K_VALUES:
                null_fit = fit_null_cpl(
                    spa_observed, BIN_CENTRES, k=k,
                    seed=int(iter_ss.generate_state(1, dtype=np.uint32)[0]),
                )
                if not null_fit["converged"]:
                    logger.debug(
                        "%s iter %d k=%d: CPL fit failed, fallback to exp",
                        spec.cell_id, iter_idx, k,
                    )
                    null_fit = fit_null_exponential(spa_observed, BIN_CENTRES)
                    fallback_aic = float("nan")
                else:
                    fallback_aic = null_fit["aic"]
                result = permutation_envelope_test(
                    observed_spa=spa_effect,
                    null_params=null_fit,
                    model=null_fit["model"],
                    bin_centres=BIN_CENTRES,
                    n_mc=spec.n_mc,
                    rng=rng,
                    alpha=0.05,
                )
                wall_ms = int((time.perf_counter() - t0) * 1_000)
                records.append(_record_from_iteration(
                    spec=spec,
                    iter_idx=iter_idx,
                    detected=result["detected"],
                    pval_global=result["pval_global"],
                    n_bins_outside=result["n_bins_outside"],
                    null_residual_rms=null_fit["residual_rms"],
                    province_counts=province_counts,
                    city_counts=city_counts,
                    seed_hex=seed_hex,
                    wall_ms=wall_ms,
                    cpl_k=k,
                    cpl_aic=fallback_aic,
                ))
        else:
            raise ValueError(f"Unknown null_model: {spec.null_model}")

    return records


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--data",
        default="archive/data-2026-04-22/LIRE_v3-0.parquet",
        help="Path to LIRE parquet (relative to repo root or absolute).",
    )
    parser.add_argument(
        "--out",
        default="runs/2026-04-25-h1-simulation/outputs",
        help="Output directory.",
    )
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument(
        "--n-iterations",
        type=int,
        default=N_ITERATIONS_DEFAULT,
        help="Iterations per cell (override for smoke tests).",
    )
    parser.add_argument(
        "--n-mc",
        type=int,
        default=N_MC_DEFAULT,
        help="MC replicates per test (override for smoke tests).",
    )
    parser.add_argument(
        "--mode",
        choices=("simulate", "report"),
        default="simulate",
    )
    parser.add_argument(
        "--cells",
        type=int,
        default=None,
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

    if args.mode == "report":
        if not parquet_path.exists():
            logger.error("No cell-results.parquet found at %s", parquet_path)
            return 2
        logger.info("Report mode: rebuilding plots from %s", parquet_path)
        # Defer to plots / power_curves modules.
        from plots import build_all_plots  # local import to keep deps minimal
        from power_curves import build_power_curves, extract_thresholds
        df = pd.read_parquet(parquet_path)
        curves = build_power_curves(df)
        curves.to_parquet(out_dir / "power-curves.parquet")
        thresholds = extract_thresholds(curves)
        thresholds.to_parquet(out_dir / "thresholds.parquet")
        build_all_plots(df, curves, out_dir)
        logger.info("Report rebuild complete: %s", out_dir)
        return 0

    # --- Simulate mode --------------------------------------------------
    source_df = load_filtered_lire(args.data)
    logger.info(
        "Loaded filtered LIRE: %d rows, %d columns",
        len(source_df), len(source_df.columns),
    )

    cells = enumerate_cells()
    if args.cells:
        cells = cells[: args.cells]
        logger.warning("Debug: limiting to first %d cells", len(cells))
    logger.info("Executing %d cells; iterations=%d mc=%d n_jobs=%d",
                len(cells), args.n_iterations, args.n_mc, args.n_jobs)

    # Override iteration / MC counts into cells if user set non-default.
    if args.n_iterations != N_ITERATIONS_DEFAULT or args.n_mc != N_MC_DEFAULT:
        cells = [
            CellSpec(
                cell_id=c.cell_id,
                level=c.level,
                bracket=c.bracket,
                shape=c.shape,
                n=c.n,
                null_model=c.null_model,
                n_iterations=args.n_iterations,
                n_mc=args.n_mc,
            )
            for c in cells
        ]

    # Master SeedSequence --> spawn one per cell.
    master_ss = np.random.SeedSequence(args.seed)
    cell_seeds = master_ss.spawn(len(cells))

    t_start = time.perf_counter()
    with Parallel(n_jobs=args.n_jobs, backend="loky", verbose=5) as pool:
        results = pool(
            delayed(run_cell)(spec, source_df, cell_seed)
            for spec, cell_seed in zip(cells, cell_seeds)
        )
    wall_total = time.perf_counter() - t_start
    logger.info("Completed %d cells in %.1f s", len(cells), wall_total)

    # Flatten + write.
    flat = [rec for cell_recs in results for rec in cell_recs]
    df_out = pd.DataFrame(flat)
    logger.info("Writing %d rows --> %s", len(df_out), parquet_path)
    df_out.to_parquet(parquet_path, index=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
