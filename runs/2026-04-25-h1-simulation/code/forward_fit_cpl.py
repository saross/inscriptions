#!/usr/bin/env python3
"""
forward_fit_cpl.py --- Forward-fit CPL null in *true-date* space + MC sampler.

This is the continuous-piecewise-linear (CPL) extension of ``forward_fit.py``.
The exponential pilot (commit d3e0a74) PASSED its FP / detection gate on
synthetic data drawn from a smooth exponential null but produced FP = 1.000
on bootstrapped real LIRE because LIRE has substantial structure beyond a
smooth exponential (editorial spikes, boom-bust shape). The CPL extension
fits a piecewise-linear true-date density that absorbs this structure; the
forward-MC envelope is then expected to control FP on real LIRE bootstrap
too.

Public API
----------
- ``fit_null_cpl_forward(intervals, k, t_min, t_max, n_restarts, seed)``
  Maximum-likelihood fit of a piecewise-linear true-date density with ``k``
  interior knots, via L-BFGS-B with multiple random restarts. Returns the
  best-likelihood result.

- ``sample_null_spa_forward_cpl(cpl_params, n, widths, bin_edges, rng,
  t_min, t_max)``
  Generate one MC replicate SPA: draw n true-date samples from the fitted
  CPL via inverse-CDF (analytic, segment-wise quadratic), sample widths,
  forward-apply the aoristic mechanism, bin.

- ``forward_envelope_test_cpl(observed_spa, cpl_params, widths, bin_edges,
  n_mc, rng, alpha, variance_floor)``
  Run the Timpson-style envelope test using the forward CPL MC sampler.
  Mirrors ``forward_fit.forward_envelope_test``'s return contract.

Parametrisation
---------------
Density ``f(t; theta)`` is piecewise-linear on ``[t_min, t_max]`` with
``k`` interior knots. Breakpoints: ``[t_min, x_1, ..., x_k, t_max]``
(``k + 2`` breakpoints). Heights at all breakpoints: ``[h_0, h_1, ...,
h_{k+1}]`` (``k + 2`` heights). The density is forced non-negative via
``h_j = exp(eta_j)`` for free parameters ``eta_j`` then renormalised to
integrate to 1 over ``[t_min, t_max]``.

Free parameters in the optimisation:
  - ``k`` interior knot positions in normalised ``[0, 1]`` (transformed
    via cumulative softmax to ensure strict ordering ``0 < x_1 < ... <
    x_k < 1``).
  - ``k + 2`` log-heights at all breakpoints.

Total: ``2k + 2`` raw parameters. AIC uses ``n_params = 2k + 1``
(identifiable count after the normalisation constraint). This matches
``primitives.fit_null_cpl``'s convention so that AIC values are
comparable across the v1 (smeared-space) and v2 (true-date forward-fit)
implementations.

Likelihood
----------
For one row's interval ``[nb_i, na_i]`` clipped to the envelope:

    L_i(theta) = (1 / Z(theta)) * integral_{nb_i}^{na_i} f(t; theta) dt

The integral over an interval is the sum of per-segment trapezoidal areas
clipped to the segment overlap with ``[nb_i, na_i]``. The normaliser
``Z(theta) = sum_segments (h_a + h_b) / 2 * (t_b - t_a)``.

Optimisation
------------
L-BFGS-B with box bounds on positions (raw cumsoftmax inputs) and
log-heights. Multiple random restarts (default 8) to mitigate local
minima; we take the best-likelihood result. Logged convergence flag is
the success of the best-restart run.

Numerical notes
---------------
The trapezoidal integrals are exact in floating point (no quadrature
error). Edge case: ``h_j -> 0`` is allowed via ``exp(eta_j)`` --
``eta_j -> -infty`` is fine; the box bound on ``eta`` (default
``[-25, 25]``) keeps the density ratio across the envelope to roughly
``exp(50) ~ 5e21`` in the worst case, well wider than any realistic
empirical shape.

Edge cases:
  - Knot positions degenerating to envelope edges or to each other:
    cumulative-softmax with bounded raw inputs prevents this in the
    interior of the parameter space.
  - Numerical underflow when a segment is very narrow with very small
    heights: the per-row integral is computed in linear (not log) space
    and then ``log(...)``'d, so a clipped-to-zero integral would yield
    ``-inf`` log-likelihood and a large NLL. We add a per-row floor of
    ``1e-300`` to prevent ``log(0)``; this is below float64 underflow
    so it never affects converged regions.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
References:
  - Timpson, A., Barberena, R., Thomas, M. G., Mendez, C. & Manning, K.
    2021. "Directly modelling population dynamics in the South American
    Arid Diagonal using 14C dates." Phil. Trans. R. Soc. B 376: 20190723.
  - Crema, E. R. & Bevan, A. 2021. "Inference from large sets of
    radiocarbon dates: Software and methods." Radiocarbon 63(1).
"""

from __future__ import annotations

import logging
from typing import Sequence

import numpy as np
from scipy import optimize

# Optional numba JIT acceleration. The objective + inner-row kernel is the
# L-BFGS-B hot path; numba gives a ~5x speedup over the numpy-only code.
# If numba is unavailable, ``fit_null_cpl_forward`` falls back to the
# Python objective transparently. Numba is added as an explicit project
# dependency to keep the fast path the default.
try:
    import numba  # type: ignore
    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only on numba-less envs
    numba = None  # type: ignore
    _NUMBA_AVAILABLE = False

logger = logging.getLogger(__name__)

# Lower / upper bounds on log-heights (eta). exp(-25) ~ 1.4e-11 ; exp(25)
# ~ 7.2e10. The optimisation never benefits from going outside this range
# given any realistic data; bounding stops L-BFGS-B from exploring divergent
# regions when the objective is locally flat.
_ETA_LO: float = -25.0
_ETA_HI: float = 25.0

# Bound on the raw "position" inputs (transformed via cumulative softmax).
# A bound of +/- 6 keeps softmax weights within ~e^12 ~ 1.6e5 ratio between
# the most- and least-likely gap; sufficient for the optimiser to express
# any reasonable knot configuration.
_POS_LO: float = -6.0
_POS_HI: float = 6.0

# Tiny floor used to avoid ``log(0)`` on degenerate per-row integrals.
_LOG_FLOOR: float = 1e-300


# ---------------------------------------------------------------------------
# Parameter packing / unpacking
# ---------------------------------------------------------------------------

def _unpack_params(
    params: np.ndarray, k: int, t_min: float, t_max: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Decode ``params`` into (breakpoint_xs, breakpoint_heights).

    ``params`` layout: first ``k`` entries are raw position inputs, next
    ``k + 2`` entries are log-heights at all breakpoints.

    Position decoding (cumulative-softmax on ``k + 1`` gaps):

        gaps = softmax([raw_x_1, ..., raw_x_k, 0])
        cumulative gaps yield positions ``cum[0] ... cum[k-1]`` in (0, 1).

    The interior x-positions are then mapped to absolute years via
    ``t_lo + cum * (t_hi - t_lo)``.

    Parameters
    ----------
    params : numpy.ndarray
        Flat parameter vector of length ``2 * k + 2``.
    k : int
        Interior-knot count.
    t_min, t_max : float
        Envelope bounds.

    Returns
    -------
    xs : numpy.ndarray
        Sorted breakpoint positions (length ``k + 2``):
        ``[t_min, x_1, ..., x_k, t_max]``.
    heights : numpy.ndarray
        Heights at each breakpoint (length ``k + 2``), all positive.
    """
    raw_x = params[:k]
    log_h = params[k:]

    # Cumulative-softmax to get k interior positions in (0, 1).
    gaps_raw = np.exp(np.concatenate([raw_x, [0.0]]))
    gaps = gaps_raw / gaps_raw.sum()  # k + 1 entries summing to 1
    cum = np.cumsum(gaps)[:-1]        # k interior positions in (0, 1)
    interior = t_min + cum * (t_max - t_min)
    xs = np.concatenate([[t_min], interior, [t_max]])

    heights = np.exp(log_h)
    return xs, heights


def _normaliser(xs: np.ndarray, heights: np.ndarray) -> float:
    """Compute ``Z = integral_{t_min}^{t_max} f(t) dt`` for a CPL density.

    Sum of trapezoidal areas across ``k + 1`` segments. Always positive
    given strictly-positive ``heights``.
    """
    widths = np.diff(xs)
    avg_h = 0.5 * (heights[:-1] + heights[1:])
    return float(np.sum(widths * avg_h))


# ---------------------------------------------------------------------------
# Per-row interval integral
# ---------------------------------------------------------------------------

def _interval_integrals(
    nb: np.ndarray, na: np.ndarray,
    xs: np.ndarray, heights: np.ndarray,
) -> np.ndarray:
    """Compute the integral ``int_{nb_i}^{na_i} f(t) dt`` per row.

    Vectorised over rows; loops over ``k + 1`` segments. For each segment
    ``[xa, xb]`` with heights ``[ha, hb]``, the per-row contribution is
    the trapezoidal area on ``[max(nb_i, xa), min(na_i, xb)]`` if this
    overlap is positive, else zero.

    Parameters
    ----------
    nb, na : numpy.ndarray
        Per-row interval bounds; ``na > nb``.
    xs : numpy.ndarray
        Breakpoint positions (length ``k + 2``).
    heights : numpy.ndarray
        Breakpoint heights (length ``k + 2``).

    Returns
    -------
    numpy.ndarray
        Per-row integral (positive). Pre-normalisation -- caller divides
        by ``Z`` to get a probability density value.

    Notes
    -----
    Optimised vs the original v1 implementation in two ways:

      1. Drop the per-segment ``np.any(valid)`` short-circuit. Profiling
         showed the boolean reduce dominated wall-time over the savings.
      2. Compute the trapezoidal mean-height directly as
         ``ha + slope * (0.5 * (lo + hi) - xa)`` rather than averaging
         two interpolated heights -- saves one temporary allocation per
         segment.
      3. Accumulate via ``+=`` into a pre-allocated output rather than
         building per-segment ``seg_int`` and rebinding.

    The vectorised numpy form is the Python fallback when numba is
    unavailable; the production fit uses ``_nll_numba_kernel`` directly.
    """
    n_seg = len(xs) - 1
    integrals = np.zeros(nb.shape, dtype=float)
    for s in range(n_seg):
        xa = xs[s]
        xb = xs[s + 1]
        ha = heights[s]
        hb = heights[s + 1]
        seg_w = xb - xa
        # Avoid division by a degenerate-zero segment width (shouldn't
        # occur with the cumulative-softmax positions, but defensive).
        if seg_w <= 0:
            continue
        slope = (hb - ha) / seg_w
        # Overlap of [nb_i, na_i] with [xa, xb], clamped to non-negative.
        lo = np.maximum(nb, xa)
        hi = np.minimum(na, xb)
        overlap = hi - lo
        np.maximum(overlap, 0.0, out=overlap)
        # Trapezoidal area = mean_height * overlap.
        # mean_height = (h_at_lo + h_at_hi) / 2
        #             = ha + slope * (0.5 * (lo + hi) - xa)
        mean_h = ha + slope * (0.5 * (lo + hi) - xa)
        integrals += mean_h * overlap
    return integrals


# ---------------------------------------------------------------------------
# Numba JIT inner kernel for the negative log likelihood
# ---------------------------------------------------------------------------
#
# The L-BFGS-B optimiser calls ``_neg_log_likelihood`` thousands of times
# per fit (across 8 restarts x ~50 BFGS iters x ~9 evaluations for the
# finite-difference Jacobian). Profiling at n_obs = 2500, k = 3 showed
# 58 % of fit wall-time in ``_interval_integrals`` (per-segment numpy
# ops) and another ~10 % in the surrounding cumulative-softmax decode +
# np.log + np.sum. JIT-compiling the entire NLL into a single tight loop
# avoids the per-call ufunc overhead that dominates at this scale and
# delivers a ~5x speedup.
#
# Branching on ``_NUMBA_AVAILABLE`` keeps the module importable in
# numba-less environments (the Python objective is then used).

if _NUMBA_AVAILABLE:

    @numba.njit(cache=True, fastmath=True)
    def _nll_numba_kernel(
        raw_x: np.ndarray, log_h: np.ndarray,
        nb: np.ndarray, na: np.ndarray,
        t_min: float, t_max: float,
    ) -> float:
        """Numba JIT: complete CPL negative log-likelihood.

        Inputs:
          - ``raw_x`` (length k): raw positions, decoded via cumulative
            softmax with an implicit zero appended.
          - ``log_h`` (length k+2): log-heights at all breakpoints.
          - ``nb, na``: per-row interval bounds.
          - ``t_min, t_max``: envelope.

        Returns the NLL as a float (or 1e20 on numerical failure).
        Mirror of the pure-Python ``_neg_log_likelihood`` modulo the
        param packing convention.
        """
        k = raw_x.shape[0]
        # Stable softmax over raw_x with an implicit zero appended.
        max_arg = 0.0  # the appended-zero entry
        for i in range(k):
            if raw_x[i] > max_arg:
                max_arg = raw_x[i]
        s = np.exp(-max_arg)  # contribution from the appended 0
        for i in range(k):
            s += np.exp(raw_x[i] - max_arg)

        # Build xs, heights as length-(k+2) arrays.
        n_seg = k + 1
        xs = np.empty(n_seg + 1, dtype=np.float64)
        xs[0] = t_min
        cum = 0.0
        for i in range(k):
            gap = np.exp(raw_x[i] - max_arg) / s
            cum += gap
            xs[i + 1] = t_min + cum * (t_max - t_min)
        xs[n_seg] = t_max

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

        # Per-row integral + log + sum, fused into one outer-segment loop.
        n_rows = nb.shape[0]
        log_floor = 1e-300
        # Per-row accumulator.
        per_row = np.zeros(n_rows, dtype=np.float64)
        for s_idx in range(n_seg):
            xa = xs[s_idx]
            xb = xs[s_idx + 1]
            seg_w = xb - xa
            if seg_w <= 0.0:
                continue
            ha = heights[s_idx]
            hb = heights[s_idx + 1]
            slope = (hb - ha) / seg_w
            for i in range(n_rows):
                lo = nb[i] if nb[i] > xa else xa
                hi = na[i] if na[i] < xb else xb
                ov = hi - lo
                if ov > 0.0:
                    mid = 0.5 * (lo + hi) - xa
                    per_row[i] += (ha + slope * mid) * ov

        sum_log = 0.0
        for i in range(n_rows):
            v = per_row[i]
            if v < log_floor:
                v = log_floor
            sum_log += np.log(v)

        nll = -(sum_log - float(n_rows) * np.log(Z))
        if not np.isfinite(nll):
            return 1e20
        return nll

else:  # pragma: no cover - fallback path

    def _nll_numba_kernel(  # type: ignore[no-redef]
        raw_x: np.ndarray, log_h: np.ndarray,
        nb: np.ndarray, na: np.ndarray,
        t_min: float, t_max: float,
    ) -> float:
        """Pure-Python fallback when numba is unavailable.

        Reconstructs the same maths via the existing helpers; matches
        the numba kernel's float return contract.
        """
        params = np.concatenate([raw_x, log_h])
        k = raw_x.shape[0]
        return _neg_log_likelihood(params, k, nb, na, t_min, t_max)


def _neg_log_likelihood(
    params: np.ndarray, k: int, nb: np.ndarray, na: np.ndarray,
    t_min: float, t_max: float,
) -> float:
    """Negative interval log-likelihood for the CPL null at ``params``.

    ``logL(theta) = sum_i log( int_{nb_i}^{na_i} f(t; theta) dt )
                   - n * log( Z(theta) )``

    Pure-Python reference; production code path uses
    :func:`_nll_numba_kernel` via :func:`_neg_log_likelihood_fast`.
    Retained here for unit tests + as a numba-less fallback.
    """
    xs, heights = _unpack_params(params, k, t_min, t_max)
    Z = _normaliser(xs, heights)
    if not np.isfinite(Z) or Z <= 0:
        return 1e20
    per_row = _interval_integrals(nb, na, xs, heights)
    # Floor degenerate zeros to avoid log(0). Using ``np.maximum`` so the
    # gradient information is preserved everywhere except a measure-zero
    # set.
    per_row = np.maximum(per_row, _LOG_FLOOR)
    log_per_row = np.log(per_row)
    nll = -(np.sum(log_per_row) - len(nb) * np.log(Z))
    if not np.isfinite(nll):
        return 1e20
    return float(nll)


def _neg_log_likelihood_fast(
    params: np.ndarray, k: int, nb: np.ndarray, na: np.ndarray,
    t_min: float, t_max: float,
) -> float:
    """Optimised NLL: dispatches to the numba kernel when available.

    Drop-in replacement for :func:`_neg_log_likelihood`; the only
    difference is that the inner row / segment loop runs in numba-JIT
    machine code rather than as a sequence of numpy ufunc calls.
    """
    raw_x = params[:k]
    log_h = params[k:]
    return float(_nll_numba_kernel(raw_x, log_h, nb, na, t_min, t_max))


# ---------------------------------------------------------------------------
# Public API: fit
# ---------------------------------------------------------------------------

def fit_null_cpl_forward(
    intervals: np.ndarray | Sequence | None,
    k: int,
    t_min: float = -50.0,
    t_max: float = 350.0,
    n_restarts: int = 8,
    seed: int = 20260425,
    nb: np.ndarray | None = None,
    na: np.ndarray | None = None,
) -> dict:
    """Forward-fit a CPL null in *true-date* space.

    Treats each inscription's interval ``[nb_i, na_i]`` as an integration
    range in the likelihood. Maximises the interval log-likelihood for a
    piecewise-linear density with ``k`` interior knots over the analysis
    envelope.

    Parameters
    ----------
    intervals : numpy.ndarray | sequence | None
        ``(n, 2)`` array of ``[nb, na]`` rows, OR ``None`` (then ``nb`` and
        ``na`` must be supplied as 1-D arrays).
    k : int
        Interior-knot count. Must satisfy ``k >= 1``; recommended ``k in
        {2, 3, 4}`` for archaeological SPA work.
    t_min, t_max : float
        Analysis envelope; intervals are clipped to this.
    n_restarts : int, default 8
        Number of random restarts for L-BFGS-B. The best (lowest NLL) result
        is kept.
    seed : int, default 20260425
        Seed for restart initial-condition draws.
    nb, na : numpy.ndarray | None
        Alternative input form: 1-D arrays of interval lower / upper bounds.

    Returns
    -------
    dict
        Keys: ``"knot_positions"`` (length ``k`` interior-knot years),
        ``"knot_heights"`` (length ``k + 2`` heights at all breakpoints
        including endpoints, *normalised* so the density integrates to 1
        on the envelope), ``"log_likelihood"`` (float, the maximum found
        across restarts), ``"aic"`` (``-2 * log_L + 2 * (2k + 1)``),
        ``"converged"`` (bool, success flag of the best restart),
        ``"n_obs"`` (int, rows used after envelope clipping),
        ``"k"`` (int), ``"n_restarts_attempted"`` (int),
        ``"method"`` (``"cpl"``).

    Raises
    ------
    ValueError
        If ``k < 1`` or no intervals overlap the envelope.
    """
    if k < 1:
        raise ValueError(f"k must be >= 1; got {k}")

    # Resolve input form.
    if nb is not None or na is not None:
        if nb is None or na is None:
            raise ValueError("if nb is given, na must also be given")
        nb_arr = np.asarray(nb, dtype=float)
        na_arr = np.asarray(na, dtype=float)
    else:
        intervals = np.asarray(intervals, dtype=float)
        if intervals.ndim != 2 or intervals.shape[1] != 2:
            raise ValueError(
                f"intervals must be shape (n, 2); got {intervals.shape}",
            )
        nb_arr = intervals[:, 0].copy()
        na_arr = intervals[:, 1].copy()
    if nb_arr.shape != na_arr.shape:
        raise ValueError("nb and na must match shape")

    # Clip to envelope; drop rows entirely outside.
    nb_clip = np.maximum(nb_arr, t_min)
    na_clip = np.minimum(na_arr, t_max)
    valid = na_clip > nb_clip
    nb_use = nb_clip[valid]
    na_use = na_clip[valid]
    n_obs = int(valid.sum())
    if n_obs == 0:
        raise ValueError("no intervals overlap the envelope; cannot fit")

    n_params = 2 * k + 2
    bounds = (
        [(_POS_LO, _POS_HI)] * k
        + [(_ETA_LO, _ETA_HI)] * (k + 2)
    )

    local_rng = np.random.default_rng(seed)
    best = None
    best_nll = np.inf
    n_attempted = 0
    log_h_centre = float(np.log(1.0 / (t_max - t_min)))

    # Build a midpoint-empirical-density seed for log-heights: estimate
    # density at evenly-spaced breakpoint locations via a coarse histogram
    # over the per-row interval midpoints. Rough but informative; reduces
    # optimisation distance from the initial guess.
    midpoints = 0.5 * (nb_use + na_use)
    coarse_edges = np.linspace(t_min, t_max, k + 3)
    coarse_counts, _ = np.histogram(midpoints, bins=coarse_edges)
    # Normalise to densities.
    seg_w = float(coarse_edges[1] - coarse_edges[0])
    coarse_dens = coarse_counts / max(int(coarse_counts.sum()), 1) / seg_w
    # Smooth log-heights at the breakpoints (k + 2 of them: edges of bins
    # plus interior). We have k + 2 coarse-bin midpoints; their log-density
    # gives a reasonable height seed.
    coarse_centres = 0.5 * (coarse_edges[:-1] + coarse_edges[1:])
    log_h_seed = np.log(np.maximum(coarse_dens, 1e-9))
    # Interpolate to evenly-spaced breakpoints in [t_min, t_max].
    breakpoint_xs = np.linspace(t_min, t_max, k + 2)
    log_h_init = np.interp(breakpoint_xs, coarse_centres, log_h_seed)
    # Centre to improve numerical conditioning (approximate density ~ 1/range).
    log_h_init = log_h_init - log_h_init.mean() + log_h_centre

    for restart_i in range(n_restarts):
        n_attempted += 1
        # Mix of initialisation strategies for diversity:
        #   restart 0: even-spaced positions + empirical-histogram heights
        #   restart 1: even-spaced positions + uniform heights
        #   restart >=2: random positions + jittered empirical heights
        x0 = np.empty(n_params)
        if restart_i == 0:
            x0[:k] = 0.0  # cumulative-softmax of zeros -> evenly spaced
            x0[k:] = log_h_init
        elif restart_i == 1:
            x0[:k] = 0.0
            x0[k:] = log_h_centre + local_rng.normal(0.0, 0.3, size=k + 2)
        else:
            x0[:k] = local_rng.normal(0.0, 1.0, size=k)
            x0[k:] = log_h_init + local_rng.normal(0.0, 0.5, size=k + 2)
        # Clip to bounds.
        for i in range(n_params):
            lo_i, hi_i = bounds[i]
            x0[i] = float(np.clip(x0[i], lo_i + 1e-6, hi_i - 1e-6))

        try:
            result = optimize.minimize(
                _neg_log_likelihood_fast,
                x0,
                args=(k, nb_use, na_use, t_min, t_max),
                method="L-BFGS-B",
                bounds=bounds,
                options={"maxiter": 1000, "gtol": 1e-6, "ftol": 1e-9},
            )
        except (RuntimeError, ValueError) as exc:
            logger.debug("CPL fit restart %d raised: %s", restart_i, exc)
            continue

        if not np.isfinite(result.fun):
            continue
        if result.fun < best_nll:
            best_nll = float(result.fun)
            best = result

    if best is None or not np.isfinite(best_nll):
        # Total fit failure -- return a flagged result so callers can
        # branch (e.g. fall back to a uniform null).
        return {
            "knot_positions": np.array([]),
            "knot_heights": np.array([]),
            "log_likelihood": float("nan"),
            "aic": float("nan"),
            "converged": False,
            "n_obs": n_obs,
            "k": k,
            "n_restarts_attempted": n_attempted,
            "method": "cpl",
        }

    # Decode best params and renormalise heights so the density integrates
    # to 1 over the envelope (so that downstream samplers and MC use a
    # proper density).
    xs, heights = _unpack_params(best.x, k, t_min, t_max)
    Z = _normaliser(xs, heights)
    heights = heights / Z

    log_likelihood = float(-best.fun)
    n_id_params = 2 * k + 1  # identifiable parameters under normalisation
    aic = float(-2.0 * log_likelihood + 2.0 * n_id_params)

    return {
        "knot_positions": xs[1:-1].copy(),  # interior knots only (length k)
        "knot_heights": heights.copy(),     # all breakpoints (length k + 2)
        "log_likelihood": log_likelihood,
        "aic": aic,
        "converged": bool(best.success),
        "n_obs": n_obs,
        "k": k,
        "n_restarts_attempted": n_attempted,
        "method": "cpl",
    }


# ---------------------------------------------------------------------------
# Inverse-CDF sampling from a fitted CPL density
# ---------------------------------------------------------------------------

def _all_breakpoints(cpl_params: dict, t_min: float, t_max: float) -> np.ndarray:
    """Reconstruct the full (k+2) breakpoint position array from a fit dict."""
    interior = cpl_params["knot_positions"]
    return np.concatenate([[t_min], interior, [t_max]])


def _cpl_inverse_cdf(
    u: np.ndarray, cpl_params: dict,
    t_min: float, t_max: float,
) -> np.ndarray:
    """Sample from the fitted CPL density via piecewise-quadratic inverse-CDF.

    Procedure:
      1. Compute per-segment areas ``A_s = (h_a + h_b)/2 * (x_b - x_a)``.
       These sum to 1 (post-normalisation in the fit).
      2. Cumulative areas ``F_s = sum_{r <= s} A_r`` give the segment
         boundaries on the CDF axis.
      3. For each ``u``, locate its segment via ``searchsorted``; within
         the segment, solve the quadratic
             u_local = (h_a * dt + 0.5 * slope * dt^2) / A_s
         for ``dt = t - x_a``, where ``slope = (h_b - h_a) / (x_b - x_a)``.
         Closed form via the standard quadratic root selection (positive
         branch).

    Parameters
    ----------
    u : numpy.ndarray
        Uniform samples in ``[0, 1]``.
    cpl_params : dict
        Fit result from :func:`fit_null_cpl_forward` (heights normalised).
    t_min, t_max : float
        Envelope bounds.

    Returns
    -------
    numpy.ndarray
        True-date samples, in ``[t_min, t_max]``.
    """
    xs = _all_breakpoints(cpl_params, t_min, t_max)
    heights = np.asarray(cpl_params["knot_heights"], dtype=float)
    if len(heights) != len(xs):
        raise ValueError(
            f"heights ({len(heights)}) and xs ({len(xs)}) length mismatch",
        )

    # Per-segment areas (normalised heights => sum to 1.0).
    seg_widths = np.diff(xs)
    seg_areas = 0.5 * (heights[:-1] + heights[1:]) * seg_widths
    cum_areas = np.cumsum(seg_areas)
    # Numerical guard: cum_areas[-1] should be ~1.0; clamp u so we never
    # land beyond the last segment due to floating-point drift.
    cum_areas[-1] = max(cum_areas[-1], 1.0 + 1e-9)

    # Locate each u's segment (right-open intervals).
    # ``searchsorted`` with side='right' on cum_areas returns the index s
    # such that cum_areas[s-1] < u <= cum_areas[s].
    seg_idx = np.searchsorted(cum_areas, u, side="right")
    seg_idx = np.clip(seg_idx, 0, len(seg_areas) - 1)

    # Per-sample local CDF offset within its segment.
    cum_prev = np.where(seg_idx > 0, cum_areas[np.maximum(seg_idx - 1, 0)], 0.0)
    u_local = u - cum_prev  # in [0, A_s] for that sample

    # Per-sample segment endpoints + heights.
    xa = xs[seg_idx]
    xb = xs[seg_idx + 1]
    ha = heights[seg_idx]
    hb = heights[seg_idx + 1]
    seg_w = xb - xa

    # Solve quadratic: u_local = ha * dt + 0.5 * slope * dt^2
    # where slope = (hb - ha) / seg_w.
    slope = np.where(seg_w > 0, (hb - ha) / np.where(seg_w > 0, seg_w, 1.0), 0.0)

    # Two cases:
    #   slope == 0 (flat segment): u_local = ha * dt -> dt = u_local / ha.
    #   slope != 0: 0.5 * slope * dt^2 + ha * dt - u_local = 0.
    #               dt = (-ha +/- sqrt(ha^2 + 2 * slope * u_local)) / slope.
    #               Choose the positive root in [0, seg_w].
    is_flat = np.abs(slope) < 1e-15
    dt = np.empty_like(u_local)
    # Flat case.
    safe_ha = np.where(is_flat & (ha > 0), ha, 1.0)
    dt_flat = np.where(ha > 0, u_local / safe_ha, 0.0)
    # Non-flat case.
    discriminant = ha * ha + 2.0 * slope * u_local
    discriminant = np.maximum(discriminant, 0.0)
    sqrt_disc = np.sqrt(discriminant)
    # Positive root: (-ha + sqrt_disc) / slope. Algebraic identity:
    # ((-ha + sqrt_disc) / slope) for slope > 0 with ha >= 0 gives
    # dt >= 0. For slope < 0 with ha >= 0, the root is also non-negative
    # because sqrt_disc <= ha there. Either way, this branch is the
    # physically-meaningful root.
    safe_slope = np.where(is_flat, 1.0, slope)
    dt_quad = (-ha + sqrt_disc) / safe_slope
    dt = np.where(is_flat, dt_flat, dt_quad)
    # Numerical clip into [0, seg_w].
    dt = np.clip(dt, 0.0, seg_w)

    t = xa + dt
    return np.clip(t, t_min, t_max)


# ---------------------------------------------------------------------------
# Public API: forward MC sampler
# ---------------------------------------------------------------------------

def sample_null_spa_forward_cpl(
    cpl_params: dict,
    n: int,
    widths: np.ndarray,
    bin_edges: np.ndarray,
    rng: np.random.Generator,
    t_min: float = -50.0,
    t_max: float = 350.0,
) -> np.ndarray:
    """Generate one MC replicate SPA from a fitted CPL true-date null.

    Procedure (mirrors ``forward_fit.sample_null_spa_forward_exp``):
      1. Sample ``n`` true dates from the CPL density via piecewise-
         quadratic inverse CDF.
      2. Sample ``n`` widths from the empirical width distribution
         (with replacement).
      3. Sample ``n`` interval positions ``u_i ~ Uniform(0, 1)``;
         construct ``nb_i = t_i - u_i * w_i``, ``na_i = nb_i + w_i``.
      4. Aoristic-resample: draw ``y_i ~ Uniform(nb_i, na_i)``, single
         draw per row.
      5. Bin via ``np.histogram``.

    Variance structure: each MC replicate carries one layer of aoristic
    smearing (step 4), matching the observed SPA pipeline.

    Parameters
    ----------
    cpl_params : dict
        Fit result from :func:`fit_null_cpl_forward`. Must have
        ``knot_positions`` and ``knot_heights`` keys (heights normalised
        to integrate to 1 on the envelope).
    n : int
        Sample size for this replicate.
    widths : numpy.ndarray
        Empirical interval-width distribution.
    bin_edges : numpy.ndarray
        Bin edges; output SPA has length ``len(bin_edges) - 1``.
    rng : numpy.random.Generator
        Seeded generator.
    t_min, t_max : float
        Analysis envelope.

    Returns
    -------
    numpy.ndarray
        MC replicate SPA (float).
    """
    if n <= 0:
        raise ValueError(f"n must be positive; got {n}")
    if widths.size == 0:
        raise ValueError("widths is empty")
    if not cpl_params.get("converged", False):
        raise ValueError("cpl_params must come from a converged fit")

    # 1. Sample n true dates from the CPL density.
    u_t = rng.uniform(size=n)
    t_true = _cpl_inverse_cdf(u_t, cpl_params, t_min, t_max)

    # 2. Widths from empirical distribution (with replacement).
    w = rng.choice(widths, size=n, replace=True)

    # 3. Interval position: u_pos ~ Uniform(0, 1); nb = t - u_pos * w.
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w

    # 4. Aoristic-resample: single uniform draw per row.
    y = rng.uniform(nb, na)

    # 5. Bin.
    spa, _ = np.histogram(y, bins=bin_edges)
    return spa.astype(float)


# ---------------------------------------------------------------------------
# Public API: envelope test
# ---------------------------------------------------------------------------

def forward_envelope_test_cpl(
    observed_spa: np.ndarray,
    cpl_params: dict,
    widths: np.ndarray,
    bin_edges: np.ndarray,
    n_mc: int,
    rng: np.random.Generator,
    n: int | None = None,
    alpha: float = 0.05,
    variance_floor: float = 1e-10,
    t_min: float = -50.0,
    t_max: float = 350.0,
) -> dict:
    """Timpson 2014 envelope test using the forward CPL MC sampler.

    Mirrors ``forward_fit.forward_envelope_test``'s return contract;
    differs only in that the MC replicates are drawn from a fitted CPL
    null (via :func:`sample_null_spa_forward_cpl`) instead of an
    exponential null.

    Parameters
    ----------
    observed_spa : numpy.ndarray
        Observed (possibly effect-injected) SPA.
    cpl_params : dict
        Fit result from :func:`fit_null_cpl_forward`.
    widths : numpy.ndarray
        Empirical interval-width distribution.
    bin_edges : numpy.ndarray
        Bin edges; ``len(bin_edges) - 1`` must equal ``len(observed_spa)``.
    n_mc : int
        Number of MC replicates.
    rng : numpy.random.Generator
        Seeded generator.
    n : int | None
        Sample size for each MC replicate. If ``None``, defaults to
        ``observed_spa.sum()`` (rounded). Pass the cell n explicitly to
        avoid drift from non-integer sums.
    alpha : float
        Pointwise envelope level.
    variance_floor : float
        Bins with MC variance below this are excluded from out-of-envelope
        counts (numerical guard).
    t_min, t_max : float
        Analysis envelope.

    Returns
    -------
    dict
        Same shape as :func:`forward_fit.forward_envelope_test`:
        ``detected``, ``pval_global``, ``lo_env``, ``hi_env``,
        ``n_bins_outside``, ``n_bins_skipped``.
    """
    n_bins = len(bin_edges) - 1
    if observed_spa.shape != (n_bins,):
        raise ValueError(
            f"observed_spa shape {observed_spa.shape} mismatches "
            f"bin_edges -> {n_bins} bins",
        )
    if n is None:
        n = int(round(float(observed_spa.sum())))
        if n <= 0:
            raise ValueError("inferred n from observed_spa.sum() is non-positive")

    mc_array = np.empty((n_mc, n_bins), dtype=float)
    for i in range(n_mc):
        mc_array[i] = sample_null_spa_forward_cpl(
            cpl_params, n, widths, bin_edges, rng, t_min=t_min, t_max=t_max,
        )

    lo_env = np.quantile(mc_array, alpha / 2.0, axis=0)
    hi_env = np.quantile(mc_array, 1.0 - alpha / 2.0, axis=0)

    var = mc_array.var(axis=0)
    keep = var >= variance_floor
    n_bins_skipped = int((~keep).sum())

    obs_outside_mask = (observed_spa < lo_env) | (observed_spa > hi_env)
    obs_outside = int((obs_outside_mask & keep).sum())

    mc_outside_mask = (mc_array < lo_env) | (mc_array > hi_env)
    mc_outside = (mc_outside_mask & keep[np.newaxis, :]).sum(axis=1)

    pval_global = float(np.mean(mc_outside >= obs_outside))
    return {
        "detected": bool(pval_global < alpha),
        "pval_global": pval_global,
        "lo_env": lo_env,
        "hi_env": hi_env,
        "n_bins_outside": obs_outside,
        "n_bins_skipped": n_bins_skipped,
    }
