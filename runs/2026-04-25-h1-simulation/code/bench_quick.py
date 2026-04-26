#!/usr/bin/env python3
"""
bench_quick.py --- Direct timing of ``_interval_integrals`` vs candidates.

Bypasses scipy.optimize entirely; just times the per-evaluation kernel
that dominates the L-BFGS-B inner loop. Used for fast iteration on
optimisation candidates.

Run:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/bench_quick.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from forward_fit_cpl import _interval_integrals as _int_baseline  # noqa: E402
import numba  # noqa: E402


@numba.njit(cache=True, fastmath=True)
def _int_numba(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Numba JIT inner kernel: row-major double loop, no temp allocations."""
    n_rows = nb.shape[0]
    n_seg = xs.shape[0] - 1
    integrals = np.zeros(n_rows, dtype=np.float64)
    for s in range(n_seg):
        xa = xs[s]
        xb = xs[s + 1]
        seg_w = xb - xa
        if seg_w <= 0.0:
            continue
        ha = heights[s]
        hb = heights[s + 1]
        slope = (hb - ha) / seg_w
        for i in range(n_rows):
            lo = nb[i] if nb[i] > xa else xa
            hi = na[i] if na[i] < xb else xb
            ov = hi - lo
            if ov > 0.0:
                mid = 0.5 * (lo + hi) - xa
                integrals[i] += (ha + slope * mid) * ov
    return integrals


@numba.njit(cache=True, fastmath=True, parallel=False)
def _int_numba_seg_first(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Same but row-outer / segment-inner (better cache behaviour for small k)."""
    n_rows = nb.shape[0]
    n_seg = xs.shape[0] - 1
    integrals = np.zeros(n_rows, dtype=np.float64)
    for i in range(n_rows):
        nb_i = nb[i]
        na_i = na[i]
        s_int = 0.0
        for s in range(n_seg):
            xa = xs[s]
            xb = xs[s + 1]
            seg_w = xb - xa
            if seg_w <= 0.0:
                continue
            lo = nb_i if nb_i > xa else xa
            hi = na_i if na_i < xb else xb
            ov = hi - lo
            if ov > 0.0:
                ha = heights[s]
                hb = heights[s + 1]
                slope = (hb - ha) / seg_w
                mid = 0.5 * (lo + hi) - xa
                s_int += (ha + slope * mid) * ov
        integrals[i] = s_int
    return integrals


def _int_vec_2d(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Vectorised 2D version: full (rows × segments) numpy broadcast.

    Same maths as :func:`_interval_integrals` but eliminates the per-segment
    Python loop and the per-segment ``np.any`` short-circuit (which was the
    measured ufunc-reduce hot spot).
    """
    # xs shape (k+2,); heights shape (k+2,).
    n_seg = xs.shape[0] - 1
    xa = xs[:n_seg]            # (S,)
    xb = xs[1:]                # (S,)
    ha = heights[:n_seg]       # (S,)
    hb = heights[1:]           # (S,)
    seg_w = xb - xa            # (S,)
    # Avoid div-by-zero on degenerate segments.
    safe_w = np.where(seg_w > 0, seg_w, 1.0)
    slope = (hb - ha) / safe_w  # (S,)

    # Broadcast: rows on axis 0, segments on axis 1.
    nb_b = nb[:, None]          # (R, 1)
    na_b = na[:, None]          # (R, 1)
    lo = np.maximum(nb_b, xa)   # (R, S)
    hi = np.minimum(na_b, xb)   # (R, S)
    overlap = hi - lo           # (R, S)
    valid = overlap > 0         # (R, S) bool

    h_at_lo = ha + slope * (lo - xa)
    h_at_hi = ha + slope * (hi - xa)
    seg_int = np.where(valid, 0.5 * (h_at_lo + h_at_hi) * overlap, 0.0)
    # Sum along segments for each row.
    return seg_int.sum(axis=1)


def _int_vec_clip(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Same 2D form but uses ``np.clip(overlap, 0, +inf)`` instead of where.

    Replaces the ``valid`` boolean mask with a clip-to-zero. For invalid
    overlaps (lo >= hi), seg_int = 0.5 * (h_at_lo + h_at_hi) * 0 = 0, so
    we just clamp negative overlaps to 0 and skip the boolean mask.
    """
    n_seg = xs.shape[0] - 1
    xa = xs[:n_seg]
    xb = xs[1:]
    ha = heights[:n_seg]
    hb = heights[1:]
    seg_w = xb - xa
    safe_w = np.where(seg_w > 0, seg_w, 1.0)
    slope = (hb - ha) / safe_w

    nb_b = nb[:, None]
    na_b = na[:, None]
    lo = np.maximum(nb_b, xa)
    hi = np.minimum(na_b, xb)
    overlap = np.maximum(hi - lo, 0.0)  # zero out invalid overlaps

    h_at_lo = ha + slope * (lo - xa)
    h_at_hi = ha + slope * (hi - xa)
    seg_int = 0.5 * (h_at_lo + h_at_hi) * overlap
    return seg_int.sum(axis=1)


def _int_loop_no_check(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Like baseline but drop the ``np.any`` early-exit + ``zeros_like``.

    Allocate output once, accumulate per segment via ``+=``. No mask check.
    """
    n_seg = xs.shape[0] - 1
    integrals = np.zeros(nb.shape, dtype=float)
    for s in range(n_seg):
        xa = xs[s]; xb = xs[s + 1]
        ha = heights[s]; hb = heights[s + 1]
        seg_w = xb - xa
        if seg_w <= 0:
            continue
        slope = (hb - ha) / seg_w
        lo = np.maximum(nb, xa)
        hi = np.minimum(na, xb)
        overlap = np.maximum(hi - lo, 0.0)
        h_at_lo = ha + slope * (lo - xa)
        h_at_hi = ha + slope * (hi - xa)
        integrals += 0.5 * (h_at_lo + h_at_hi) * overlap
    return integrals


def _int_loop_minimal(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Loop variant using fewest temporaries.

    Inline maths to reduce array allocations:

      h_at_lo = ha + slope * (lo - xa) = ha + slope * (max(nb, xa) - xa)
                = ha + slope * max(nb - xa, 0)
      h_at_hi = ha + slope * (hi - xa)

    Combine: trapezoid area = 0.5 * (h_at_lo + h_at_hi) * (hi - lo).
    Use one big accumulator and one temp.
    """
    n_seg = xs.shape[0] - 1
    integrals = np.zeros(nb.shape, dtype=float)
    for s in range(n_seg):
        xa = xs[s]; xb = xs[s + 1]
        ha = heights[s]; hb = heights[s + 1]
        seg_w = xb - xa
        if seg_w <= 0:
            continue
        slope = (hb - ha) / seg_w

        # lo and hi as scalars per row, but cheap because numpy ufuncs.
        lo = np.maximum(nb, xa)
        hi = np.minimum(na, xb)
        overlap = hi - lo
        np.maximum(overlap, 0.0, out=overlap)
        # Mean height at trapezoid: (h_at_lo + h_at_hi) / 2
        # = ha + slope * ((lo - xa) + (hi - xa)) / 2
        # = ha + slope * (lo + hi - 2*xa) / 2.
        mean_h = ha + slope * (0.5 * (lo + hi) - xa)
        integrals += mean_h * overlap
    return integrals


def _int_blas_form(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Express segment-sum as a sum-axis-1 of (R, S) view computed lazily.

    Uses the trick that for trapezoidal integration we can decompose:
      contribution = 0.5 * (h_at_lo + h_at_hi) * (hi - lo)
                   = 0.5 * (2*ha + slope * (lo + hi - 2*xa)) * (hi - lo)
                   = ha * (hi - lo) + 0.5 * slope * ((lo + hi) - 2*xa) * (hi - lo)

    Compute (R, S) overlap matrix once, derive everything else.
    """
    n_seg = xs.shape[0] - 1
    xa = xs[:n_seg]
    xb = xs[1:]
    ha = heights[:n_seg]
    hb = heights[1:]
    seg_w = xb - xa
    safe_w = np.where(seg_w > 0, seg_w, 1.0)
    slope = (hb - ha) / safe_w

    nb_b = nb[:, None]
    na_b = na[:, None]
    lo = np.maximum(nb_b, xa)
    hi = np.minimum(na_b, xb)
    overlap = hi - lo
    np.maximum(overlap, 0.0, out=overlap)
    mean_h = ha + slope * (0.5 * (lo + hi) - xa)
    return (mean_h * overlap).sum(axis=1)


def _setup_inputs(rng_seed: int = 42, n: int = 2500, k: int = 3):
    """Generate a representative (nb, na, xs, heights) tuple for benchmarking."""
    rng = np.random.default_rng(rng_seed)
    # Synthetic intervals: random midpoints + widths drawn from a heavy
    # distribution so most rows span at least one knot.
    midpts = rng.uniform(-50, 350, size=n)
    widths = rng.choice([10.0, 25.0, 50.0, 100.0, 150.0, 300.0], size=n)
    nb = midpts - 0.5 * widths
    na = midpts + 0.5 * widths
    # Random CPL params in the typical regime.
    xs = np.linspace(-50, 350, k + 2)
    heights = rng.uniform(0.001, 0.005, size=k + 2)
    return nb, na, xs, heights


def main() -> int:
    n_runs = 1000
    candidates = [
        ("baseline",         _int_baseline),
        ("vec_2d",           _int_vec_2d),
        ("vec_clip",         _int_vec_clip),
        ("loop_no_chk",      _int_loop_no_check),
        ("loop_minimal",     _int_loop_minimal),
        ("blas_form",        _int_blas_form),
        ("numba",            _int_numba),
        ("numba_seg_first",  _int_numba_seg_first),
    ]
    for k in (3, 4):
        nb, na, xs, heights = _setup_inputs(n=2500, k=k)
        ref = _int_baseline(nb, na, xs, heights)
        # Warm-up + correctness.
        print(f"\n# === k={k} ===")
        for name, fn in candidates:
            for _ in range(5):
                fn(nb, na, xs, heights)
            got = fn(nb, na, xs, heights)
            err = float(np.max(np.abs(ref - got)))
            t0 = time.perf_counter_ns()
            for _ in range(n_runs):
                fn(nb, na, xs, heights)
            t_us = (time.perf_counter_ns() - t0) / n_runs / 1e3
            print(f"  {name:14s}: {t_us:7.1f} us | err {err:.2e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
