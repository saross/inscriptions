#!/usr/bin/env python3
"""
forward_fit.py --- Forward-fit exponential null in *true-date* space + MC sampler.

Implements the pilot specified in
`planning/prior-art-scout-2026-04-25-aoristic-envelope.md` §8 (empirical
addendum). The motivation: Option A (aoristic-resample-from-fit MC, fitted
in already-aoristic-smeared space) double-smears MC replicates and blows up
the false-positive rate. Forward-fit instead estimates the true-date
exponential parameter `b` by treating each inscription's interval
``[nb_i, na_i]`` as an *integration range* in the likelihood, then forward-
applies the empirical aoristic mechanism to MC replicates so that observed
and replicate SPAs share a single layer of aoristic smearing.

Public API
----------
- ``fit_null_exponential_forward(intervals, t_min, t_max)``
  Closed-form interval-likelihood maximum-likelihood fit of the exponential
  rate ``b`` over the analysis envelope ``[t_min, t_max]``.

- ``sample_null_spa_forward_exp(b, n, widths, bin_edges, rng, t_min, t_max)``
  Generate one MC replicate SPA: draw n true-date samples from the truncated
  exponential, sample widths from the empirical distribution, place each
  interval uniformly around its true date, aoristic-resample, bin.

- ``forward_envelope_test(observed_spa, b_hat, widths, bin_edges, n_mc,
  rng, alpha, variance_floor)``
  Run the Timpson-style envelope test using the forward MC sampler.

Numerical-stability notes
-------------------------
For exponential ``f(t; b) = exp(b * t) / Z(b)`` over ``[t_min, t_max]``:

    Z(b) = (exp(b * t_max) - exp(b * t_min)) / b   (b != 0)
    Z(0) = t_max - t_min

    log L_i(b) = log( exp(b * na_i) - exp(b * nb_i) )
               - log( exp(b * t_max) - exp(b * t_min) )

For non-tiny ``|b|`` the raw exponentials overflow (e.g. ``b * t_max ~ 17`` is
fine, but the optimiser will probe the whole bracket). We factor out the
maximum of the two exponents per term:

    log( exp(a) - exp(b) ) = max(a, b) + log( 1 - exp( min(a, b) - max(a, b) ) )
                           = max(a, b) + log1p( -exp( min - max ) )

This is stable for ``a > b``; we always have ``na_i > nb_i`` and
``t_max > t_min``, and we constrain ``b * (a - b) > 0`` separately.

For ``|b| -> 0`` the closed-form has a removable singularity. We switch to a
Taylor expansion in ``b`` when ``|b| * (t_max - t_min) < 1e-6``:

    Z(b) ~ (t_max - t_min) * (1 + b * (t_max + t_min) / 2 + O(b^2))

and likewise for the per-interval integral.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import logging
from typing import Sequence

import numpy as np
from scipy import optimize

logger = logging.getLogger(__name__)

# A small bound below which we treat ``b`` as effectively zero for the
# closed-form interval-integral (uniform-limit). Chosen so that
# ``|b| * (t_max - t_min) ~ |b| * 400`` stays below 4e-4 -- well within
# float64 precision for the log1p expansions.
_B_SMALL: float = 1e-6


# ---------------------------------------------------------------------------
# Likelihood helpers
# ---------------------------------------------------------------------------

def _log_diff_exp(a: np.ndarray | float, b: np.ndarray | float) -> np.ndarray:
    """Numerically stable ``log(exp(a) - exp(b))`` with ``a >= b``.

    Implementation factor-out: ``log(exp(a) - exp(b)) = a + log1p(-exp(b - a))``.
    Caller must ensure ``a >= b`` everywhere; this routine does not check.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    # ``b - a <= 0`` always; ``exp(b - a) in (0, 1]`` so log1p arg in (-1, 0].
    return a + np.log1p(-np.exp(b - a))


def _interval_integral_exp(
    nb: np.ndarray, na: np.ndarray, b: float,
) -> np.ndarray:
    """Compute ``log( int_{nb}^{na} exp(b * t) dt )`` per interval, stable.

    For ``b != 0``:
        ``int = (exp(b * na) - exp(b * nb)) / b``
        ``log int = log( exp(b * na) - exp(b * nb) ) - log|b|``
        Sign handling: ``b > 0 -> exp(b * na) > exp(b * nb)`` since ``na > nb``;
        ``b < 0 -> exp(b * na) < exp(b * nb)``. We always take the larger of
        the two as ``a`` in ``_log_diff_exp``. The integral itself is positive
        (assuming ``na > nb``); ``int = (e^(b*na) - e^(b*nb)) / b``. If b > 0,
        numerator is positive. If b < 0, numerator is negative AND b is
        negative, so the ratio is positive.

        Practically: ``log int = log|exp(b * na) - exp(b * nb)| - log|b|``.

    For ``|b| < _B_SMALL`` we Taylor-expand:
        ``int = (na - nb) * (1 + b * (na + nb) / 2 + ...)``
        ``log int = log(na - nb) + b * (na + nb) / 2 + O(b^2)``.

    Parameters
    ----------
    nb, na : numpy.ndarray
        Per-row interval bounds; must satisfy ``na >= nb``.
    b : float
        Exponential rate.

    Returns
    -------
    numpy.ndarray
        ``log(integral)`` per row.
    """
    width = na - nb
    if abs(b) < _B_SMALL:
        # Taylor expansion: log((na-nb) * (1 + b*(na+nb)/2 + ...))
        # The log1p of the first-order correction is enough at this scale.
        return np.log(width) + np.log1p(b * (na + nb) / 2.0)
    # General case.
    arg_a = b * na
    arg_b = b * nb
    if b > 0:
        # exp(b*na) > exp(b*nb): max is arg_a.
        log_diff = _log_diff_exp(arg_a, arg_b)
    else:
        # b < 0: exp(b*nb) > exp(b*na); max is arg_b. Numerator is negative
        # but we want |numerator|, so swap.
        log_diff = _log_diff_exp(arg_b, arg_a)
    return log_diff - np.log(abs(b))


def _envelope_log_norm(t_min: float, t_max: float, b: float) -> float:
    """Compute ``log( int_{t_min}^{t_max} exp(b * t) dt )``, stable.

    Same trick as :func:`_interval_integral_exp` but on the analysis envelope.
    """
    width = t_max - t_min
    if abs(b) < _B_SMALL:
        return float(np.log(width) + np.log1p(b * (t_max + t_min) / 2.0))
    arg_max_t = b * t_max
    arg_min_t = b * t_min
    if b > 0:
        log_diff = _log_diff_exp(arg_max_t, arg_min_t)
    else:
        log_diff = _log_diff_exp(arg_min_t, arg_max_t)
    return float(log_diff - np.log(abs(b)))


def _neg_log_likelihood(
    b: float, nb: np.ndarray, na: np.ndarray,
    t_min: float, t_max: float,
) -> float:
    """Negative interval log-likelihood for the exponential null at rate ``b``.

    ``logL(b) = sum_i [ log integral_{nb_i}^{na_i} exp(b*t) dt ]
              - n * log integral_{t_min}^{t_max} exp(b*t) dt``

    Parameters
    ----------
    b : float
        Rate (years^-1).
    nb, na : numpy.ndarray
        Per-row interval bounds (clipped to envelope by caller).
    t_min, t_max : float
        Envelope bounds.

    Returns
    -------
    float
        Negative log-likelihood (to be minimised).
    """
    log_per_row = _interval_integral_exp(nb, na, b)
    log_norm = _envelope_log_norm(t_min, t_max, b)
    nll = -(np.sum(log_per_row) - len(nb) * log_norm)
    if not np.isfinite(nll):
        return 1e20
    return float(nll)


# ---------------------------------------------------------------------------
# Public API: fit
# ---------------------------------------------------------------------------

def fit_null_exponential_forward(
    intervals: np.ndarray | Sequence,
    t_min: float = -50.0,
    t_max: float = 350.0,
    nb: np.ndarray | None = None,
    na: np.ndarray | None = None,
    b_bracket: tuple[float, float] = (-0.05, 0.05),
) -> dict:
    """Forward-fit an exponential null in *true-date* space.

    Treats each inscription's interval ``[nb_i, na_i]`` as an integration range
    in the likelihood. The fit recovers the rate ``b`` of the underlying true-
    date density without first smearing it through the aoristic mechanism.

    Parameters
    ----------
    intervals : numpy.ndarray | sequence
        Either an ``(n, 2)`` array of ``[nb, na]`` rows OR ``None`` (then both
        ``nb`` and ``na`` must be supplied as 1-D arrays).
    t_min, t_max : float
        Analysis envelope. Intervals are clipped to ``[t_min, t_max]`` before
        fitting; rows that lie entirely outside the envelope are dropped.
    nb, na : numpy.ndarray | None
        Alternative input form: 1-D arrays of interval lower / upper bounds.
    b_bracket : tuple[float, float]
        Optimisation bracket for ``minimize_scalar`` brent. Default
        ``(-0.05, 0.05)``: over the AD 0--350 envelope this maps to growth
        rates of ``exp(±0.05 * 400) ~ exp(±20)`` density ratio across the
        envelope -- comfortably wider than any plausible empirical rate.

    Returns
    -------
    dict
        ``{"b": float, "log_likelihood": float, "converged": bool,
           "n_obs": int, "method": "exponential"}``.
    """
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
    valid = na_clip > nb_clip  # strictly positive width post-clip
    nb_use = nb_clip[valid]
    na_use = na_clip[valid]
    n_obs = int(valid.sum())
    if n_obs == 0:
        raise ValueError("no intervals overlap the envelope; cannot fit")

    # Brent optimisation.
    result = optimize.minimize_scalar(
        _neg_log_likelihood,
        args=(nb_use, na_use, t_min, t_max),
        method="bounded",
        bounds=b_bracket,
        options={"xatol": 1e-7},
    )
    b_hat = float(result.x)
    log_likelihood = float(-result.fun)
    converged = bool(result.success)
    return {
        "b": b_hat,
        "log_likelihood": log_likelihood,
        "converged": converged,
        "n_obs": n_obs,
        "method": "exponential",
    }


# ---------------------------------------------------------------------------
# Public API: forward MC sampler
# ---------------------------------------------------------------------------

def _truncated_exponential_inverse_cdf(
    u: np.ndarray, b: float, t_min: float, t_max: float,
) -> np.ndarray:
    """Sample from truncated exponential on ``[t_min, t_max]`` via inverse CDF.

    For ``b != 0``:
        ``F(t) = (exp(b * t) - exp(b * t_min)) / (exp(b * t_max) - exp(b * t_min))``
        ``F^{-1}(u) = log( exp(b * t_min) + u * (exp(b * t_max) - exp(b * t_min)) ) / b``

    Numerically stable form using log-sum-exp:
        Let ``A = b * t_min``, ``B = b * t_max``. We need
        ``log( exp(A) + u * (exp(B) - exp(A)) )`` for ``u in [0, 1]``.
        Equivalent: ``log( (1 - u) * exp(A) + u * exp(B) )``.
        Use logaddexp on ``log(1 - u) + A`` and ``log(u) + B``, with care at
        the endpoints (``u = 0`` or ``u = 1``).

    For ``|b| < _B_SMALL``: uniform on ``[t_min, t_max]``.
    """
    if abs(b) < _B_SMALL:
        return t_min + u * (t_max - t_min)
    A = b * t_min
    B = b * t_max
    # Guard endpoints.
    eps = np.finfo(float).tiny
    u_safe = np.clip(u, eps, 1.0 - eps)
    log_term_a = np.log1p(-u_safe) + A  # log((1-u) * exp(A))
    log_term_b = np.log(u_safe) + B     # log(u * exp(B))
    log_sum = np.logaddexp(log_term_a, log_term_b)
    t = log_sum / b
    # Numerical guard: clip to envelope.
    return np.clip(t, t_min, t_max)


def sample_null_spa_forward_exp(
    b: float,
    n: int,
    widths: np.ndarray,
    bin_edges: np.ndarray,
    rng: np.random.Generator,
    t_min: float = -50.0,
    t_max: float = 350.0,
) -> np.ndarray:
    """Generate one MC replicate SPA by forward-applying aoristic to a fitted null.

    Procedure:
      1. Sample ``n`` true dates ``t_i`` from truncated exponential on
         ``[t_min, t_max]`` with rate ``b`` (inverse-CDF).
      2. Sample ``n`` widths ``w_i`` from the empirical width distribution
         (with replacement).
      3. Sample ``n`` interval positions ``u_i ~ Uniform(0, 1)`` placing the
         interval ``[t_i - u_i * w_i, t_i - u_i * w_i + w_i]`` -- i.e. the
         interval *contains* ``t_i`` at proportion ``u_i`` from its left edge.
      4. Aoristic-resample: draw ``y_i ~ Uniform(nb_i, na_i)`` (one draw per
         row, matching observed pipeline).
      5. Bin via ``np.histogram``.

    Variance structure: each MC replicate carries one layer of aoristic
    smearing (step 4), matching the observed SPA pipeline.

    Parameters
    ----------
    b : float
        Fitted true-date exponential rate.
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

    # 1. True dates from truncated exponential.
    u_t = rng.uniform(size=n)
    t_true = _truncated_exponential_inverse_cdf(u_t, b, t_min, t_max)

    # 2. Widths from empirical distribution (with replacement).
    w = rng.choice(widths, size=n, replace=True)

    # 3. Interval position: u_i ~ Uniform(0, 1); nb = t - u * w.
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w

    # 4. Aoristic-resample: one uniform draw per row.
    y = rng.uniform(nb, na)

    # 5. Bin.
    spa, _ = np.histogram(y, bins=bin_edges)
    return spa.astype(float)


# ---------------------------------------------------------------------------
# Public API: envelope test
# ---------------------------------------------------------------------------

def forward_envelope_test(
    observed_spa: np.ndarray,
    b_hat: float,
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
    """Timpson 2014 envelope test using the forward-fit exponential MC.

    Parameters
    ----------
    observed_spa : numpy.ndarray
        Observed (possibly effect-injected) SPA.
    b_hat : float
        Fitted exponential rate from
        :func:`fit_null_exponential_forward`.
    widths : numpy.ndarray
        Empirical interval-width distribution to feed the forward MC.
    bin_edges : numpy.ndarray
        Bin edges; ``len(bin_edges) - 1`` must equal ``len(observed_spa)``.
    n_mc : int
        Number of MC replicates.
    rng : numpy.random.Generator
        Seeded generator.
    n : int | None
        Sample size for each MC replicate. If ``None``, defaults to
        ``observed_spa.sum()`` (rounded). Caller should pass the cell n
        explicitly to avoid drift from non-integer sums.
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
        Same shape as :func:`primitives.permutation_envelope_test`:
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
        mc_array[i] = sample_null_spa_forward_exp(
            b_hat, n, widths, bin_edges, rng, t_min=t_min, t_max=t_max,
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
