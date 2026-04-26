#!/usr/bin/env python3
"""
profile_cpl.py --- cProfile a single ``fit_null_cpl_forward`` call.

Captures function-level profile data so we can see where the L-BFGS-B
runs spend their time. Used as a one-shot diagnostic; not part of the
production code path.

Run:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/profile_cpl.py \
        --n_obs 2500 --k 3
"""
from __future__ import annotations

import argparse
import cProfile
import io
import pstats
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from bench_cpl import _build_truth_dict, _simulate_intervals  # noqa: E402
from forward_fit_cpl import fit_null_cpl_forward  # noqa: E402
import primitives as P  # noqa: E402


T_MIN = -50.0
T_MAX = 350.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n_obs", type=int, default=2500)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--n_restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument(
        "--data",
        default="archive/data-2026-04-22/LIRE_v3-0.parquet",
    )
    args = parser.parse_args()

    df = P.load_filtered_lire(args.data)
    nb_pool = df["not_before"].to_numpy(dtype=float)
    na_pool = df["not_after"].to_numpy(dtype=float)
    widths_pool = (na_pool - nb_pool).astype(float)
    widths_pool = widths_pool[widths_pool > 0.0]

    truth = _build_truth_dict()
    rng = np.random.default_rng(args.seed)
    nb, na = _simulate_intervals(truth, args.n_obs, widths_pool, rng)

    profiler = cProfile.Profile()
    profiler.enable()
    fit = fit_null_cpl_forward(
        np.column_stack([nb, na]), k=args.k,
        t_min=T_MIN, t_max=T_MAX,
        n_restarts=args.n_restarts, seed=args.seed,
    )
    profiler.disable()

    print(f"# k={args.k} n_obs={args.n_obs} converged={fit['converged']}")
    print(f"# log_lik={fit['log_likelihood']:.3f}")
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats("cumulative")
    stats.print_stats(40)
    print(s.getvalue())

    s2 = io.StringIO()
    stats2 = pstats.Stats(profiler, stream=s2).sort_stats("tottime")
    stats2.print_stats(40)
    print("\n# === sorted by tottime ===")
    print(s2.getvalue())

    return 0


if __name__ == "__main__":
    sys.exit(main())
