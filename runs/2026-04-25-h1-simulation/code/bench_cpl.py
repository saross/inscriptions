#!/usr/bin/env python3
"""
bench_cpl.py --- Benchmark the CPL forward-fit on a representative sample.

Measures the median wall-time per ``fit_null_cpl_forward`` call for
k in {3, 4} on a synthetic dataset of n=2500 intervals drawn from the
LIRE width distribution and a CPL k=3 ground truth (the v2 simulation
DGP). Used as the optimisation baseline + as a regression check after
each round of optimisation in Stage 1.

Run:

    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/bench_cpl.py \
        --n_obs 2500 --n_warm 1 --n_runs 5
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from forward_fit import _truncated_exponential_inverse_cdf  # noqa: E402
from forward_fit_cpl import (  # noqa: E402
    _cpl_inverse_cdf,
    _normaliser,
    fit_null_cpl_forward,
)
import primitives as P  # noqa: E402


T_MIN = -50.0
T_MAX = 350.0


def _build_truth_dict() -> dict:
    """Build the LIRE-AIC-best CPL k=3 truth used by the v2 driver."""
    interior = np.array([25.42975781, 213.26566364, 280.14316364])
    heights = np.array([3.86324508e-05, 2.79243263e-03,
                        3.10599537e-03, 1.25029924e-04, 6.49470852e-03])
    xs = np.concatenate([[T_MIN], interior, [T_MAX]])
    Z = _normaliser(xs, heights)
    return {
        "knot_positions": interior,
        "knot_heights": heights / Z,
        "log_likelihood": float("nan"),
        "aic": float("nan"),
        "converged": True,
        "n_obs": -1,
        "k": 3,
        "n_restarts_attempted": 0,
        "method": "cpl",
    }


def _simulate_intervals(
    truth: dict, n: int, widths_pool: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate ``n`` synthetic intervals from a CPL truth + width pool."""
    u_t = rng.uniform(size=n)
    t_true = _cpl_inverse_cdf(u_t, truth, T_MIN, T_MAX)
    w = rng.choice(widths_pool, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        default="archive/data-2026-04-22/LIRE_v3-0.parquet",
        help="LIRE parquet path (used only for the empirical width pool).",
    )
    parser.add_argument("--n_obs", type=int, default=2500)
    parser.add_argument("--n_warm", type=int, default=1,
                        help="Warm-up fits per k (excluded from timing).")
    parser.add_argument("--n_runs", type=int, default=5,
                        help="Timed fits per k.")
    parser.add_argument("--n_restarts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--k_values", type=str, default="3,4",
                        help="Comma-separated CPL k values to benchmark.")
    args = parser.parse_args()

    # Load LIRE width pool.
    df = P.load_filtered_lire(args.data)
    nb_pool = df["not_before"].to_numpy(dtype=float)
    na_pool = df["not_after"].to_numpy(dtype=float)
    widths_pool = (na_pool - nb_pool).astype(float)
    widths_pool = widths_pool[widths_pool > 0.0]

    truth = _build_truth_dict()
    rng = np.random.default_rng(args.seed)

    k_values = [int(x) for x in args.k_values.split(",")]
    print(
        f"# bench_cpl.py: n_obs={args.n_obs} n_runs={args.n_runs} "
        f"n_warm={args.n_warm} n_restarts={args.n_restarts}"
    )
    print(f"# Width pool n={len(widths_pool)}, median={np.median(widths_pool):.1f}")

    for k in k_values:
        # Pre-build datasets so the fit routine sees identical data each iter
        # (avoid letting RNG variability dominate timing variance).
        datasets = []
        for _ in range(args.n_warm + args.n_runs):
            nb, na = _simulate_intervals(truth, args.n_obs, widths_pool, rng)
            datasets.append((nb, na))

        # Warm-up.
        for i in range(args.n_warm):
            nb, na = datasets[i]
            fit_null_cpl_forward(
                np.column_stack([nb, na]), k=k,
                t_min=T_MIN, t_max=T_MAX,
                n_restarts=args.n_restarts, seed=args.seed + i,
            )

        # Timed runs.
        times: list[float] = []
        for i in range(args.n_runs):
            nb, na = datasets[args.n_warm + i]
            t0 = time.perf_counter()
            fit = fit_null_cpl_forward(
                np.column_stack([nb, na]), k=k,
                t_min=T_MIN, t_max=T_MAX,
                n_restarts=args.n_restarts, seed=args.seed + 100 + i,
            )
            elapsed = time.perf_counter() - t0
            times.append(elapsed)

        times_arr = np.asarray(times)
        print(
            f"k={k}: median {np.median(times_arr) * 1e3:.1f} ms; "
            f"mean {np.mean(times_arr) * 1e3:.1f} ms; "
            f"min {np.min(times_arr) * 1e3:.1f} ms; "
            f"max {np.max(times_arr) * 1e3:.1f} ms; "
            f"converged: {bool(fit['converged'])}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
