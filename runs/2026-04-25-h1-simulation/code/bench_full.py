#!/usr/bin/env python3
"""
bench_full.py --- End-to-end ``_neg_log_likelihood`` benchmark.

Times the complete objective (interval integrals + log + sum + log normaliser)
that L-BFGS-B calls thousands of times during a fit. Used to verify that
optimising the inner kernel translates to a wall-time win in the full
fit, not just in synthetic micro-benchmarks.

Run:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/bench_full.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import numba

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from forward_fit_cpl import (  # noqa: E402
    _interval_integrals,
    _neg_log_likelihood as _nll_baseline,
    _normaliser,
    _unpack_params,
)


@numba.njit(cache=True, fastmath=True)
def _nll_numba_kernel(
    raw_x: np.ndarray, log_h: np.ndarray,
    nb: np.ndarray, na: np.ndarray,
    t_min: float, t_max: float,
) -> float:
    """Numba JIT for the full objective.

    Internally:
      1. Decode position params (cumulative softmax).
      2. Build xs, heights.
      3. Compute Z (normaliser).
      4. Compute per-row integrals.
      5. Sum log per_row - n * log Z.
    """
    k = raw_x.shape[0]
    # Cumulative softmax (k+1 gaps, sum to 1).
    # gaps_raw = exp([raw_x..., 0]).
    max_arg = 0.0
    for i in range(k):
        if raw_x[i] > max_arg:
            max_arg = raw_x[i]
    # Stable softmax with the implicit zero appended.
    s = np.exp(-max_arg)  # contribution from the appended 0
    for i in range(k):
        s += np.exp(raw_x[i] - max_arg)
    # Build cumulative interior positions.
    interior = np.empty(k, dtype=np.float64)
    cum = 0.0
    for i in range(k):
        gap = np.exp(raw_x[i] - max_arg) / s
        cum += gap
        interior[i] = t_min + cum * (t_max - t_min)

    # Build xs array of length k+2.
    n_seg = k + 1
    xs = np.empty(n_seg + 1, dtype=np.float64)
    xs[0] = t_min
    for i in range(k):
        xs[i + 1] = interior[i]
    xs[n_seg] = t_max

    # Heights = exp(log_h), length k+2.
    heights = np.empty(n_seg + 1, dtype=np.float64)
    for i in range(n_seg + 1):
        heights[i] = np.exp(log_h[i])

    # Normaliser Z.
    Z = 0.0
    for s_idx in range(n_seg):
        seg_w = xs[s_idx + 1] - xs[s_idx]
        Z += 0.5 * (heights[s_idx] + heights[s_idx + 1]) * seg_w
    if not np.isfinite(Z) or Z <= 0.0:
        return 1e20

    # Per-row integrals + log + sum.
    n_rows = nb.shape[0]
    log_floor = 1e-300
    sum_log = 0.0
    for i in range(n_rows):
        nb_i = nb[i]
        na_i = na[i]
        s_int = 0.0
        for s_idx in range(n_seg):
            xa = xs[s_idx]
            xb = xs[s_idx + 1]
            seg_w = xb - xa
            if seg_w <= 0.0:
                continue
            lo = nb_i if nb_i > xa else xa
            hi = na_i if na_i < xb else xb
            ov = hi - lo
            if ov > 0.0:
                ha = heights[s_idx]
                hb = heights[s_idx + 1]
                slope = (hb - ha) / seg_w
                mid = 0.5 * (lo + hi) - xa
                s_int += (ha + slope * mid) * ov
        if s_int < log_floor:
            s_int = log_floor
        sum_log += np.log(s_int)

    nll = -(sum_log - float(n_rows) * np.log(Z))
    if not np.isfinite(nll):
        return 1e20
    return nll


def _nll_numba(params: np.ndarray, k: int, nb: np.ndarray, na: np.ndarray,
               t_min: float, t_max: float) -> float:
    """Public wrapper with the same signature as the baseline."""
    raw_x = params[:k]
    log_h = params[k:]
    return _nll_numba_kernel(raw_x, log_h, nb, na, t_min, t_max)


def main() -> int:
    rng = np.random.default_rng(20260425)
    n = 2500
    midpts = rng.uniform(-50, 350, size=n)
    widths = rng.choice([10.0, 25.0, 50.0, 100.0, 150.0, 300.0], size=n)
    nb = midpts - 0.5 * widths
    na = midpts + 0.5 * widths
    t_min = -50.0
    t_max = 350.0
    n_runs = 1000

    for k in (3, 4):
        n_params = 2 * k + 2
        params = rng.normal(0.0, 0.3, size=n_params)
        params[k:] = np.log(rng.uniform(0.001, 0.005, size=k + 2))

        # Warm-up.
        for _ in range(5):
            _nll_baseline(params, k, nb, na, t_min, t_max)
            _nll_numba(params, k, nb, na, t_min, t_max)

        # Correctness.
        a = _nll_baseline(params, k, nb, na, t_min, t_max)
        b = _nll_numba(params, k, nb, na, t_min, t_max)
        rel = abs(a - b) / max(abs(a), 1.0)
        print(
            f"# k={k}: baseline NLL = {a:.6f}; numba NLL = {b:.6f}; "
            f"rel diff = {rel:.2e}"
        )

        # Time.
        t0 = time.perf_counter_ns()
        for _ in range(n_runs):
            _nll_baseline(params, k, nb, na, t_min, t_max)
        t_baseline = (time.perf_counter_ns() - t0) / n_runs / 1e3  # us
        t0 = time.perf_counter_ns()
        for _ in range(n_runs):
            _nll_numba(params, k, nb, na, t_min, t_max)
        t_numba = (time.perf_counter_ns() - t0) / n_runs / 1e3
        print(
            f"k={k}: baseline {t_baseline:7.1f} us | "
            f"numba {t_numba:6.1f} us | speedup {t_baseline / t_numba:.2f}x"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
