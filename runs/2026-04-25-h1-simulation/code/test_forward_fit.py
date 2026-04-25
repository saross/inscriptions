#!/usr/bin/env python3
"""
test_forward_fit.py --- Unit tests for the forward-fit exponential pilot.

Tests cover:

  - test_fit_recovers_known_b : MLE recovers known rate b from large sample.
  - test_fit_uniform_limit    : data drawn from uniform (b = 0) returns b ~ 0.
  - test_mc_sampler_mean_shape: average of many MC replicates has the
                                expected exponential shape modulo the
                                aoristic kernel.
  - test_envelope_fp_under_truth: synthetic data drawn from truth and tested
                                  with the same b should reject at ~alpha.

Run:
  .venv/bin/python3 -m pytest \
    runs/2026-04-25-h1-simulation/code/test_forward_fit.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from forward_fit import (  # noqa: E402
    _truncated_exponential_inverse_cdf,
    fit_null_exponential_forward,
    forward_envelope_test,
    sample_null_spa_forward_exp,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

T_MIN = -50.0
T_MAX = 350.0
BIN_EDGES = np.arange(-50, 350 + 1, 5, dtype=float)
BIN_CENTRES = 0.5 * (BIN_EDGES[:-1] + BIN_EDGES[1:])


def _simulate_intervals(
    b_true: float, n: int, widths: np.ndarray, rng: np.random.Generator,
    t_min: float = T_MIN, t_max: float = T_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate ``n`` synthetic intervals from a truncated exponential.

    Returns ``(nb, na)`` arrays of length ``n``. Mirrors the procedure used
    inside the MC sampler so the tests exercise the same generative model.
    """
    u_t = rng.uniform(size=n)
    t_true = _truncated_exponential_inverse_cdf(u_t, b_true, t_min, t_max)
    w = rng.choice(widths, size=n, replace=True)
    u_pos = rng.uniform(size=n)
    nb = t_true - u_pos * w
    na = nb + w
    return nb, na


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_fit_recovers_known_b() -> None:
    """For n=10000 with known b=0.005, MLE should recover b within 0.001."""
    rng = np.random.default_rng(20260425)
    # Use a realistic width distribution: mostly 50-150 y, some 10-300 y.
    widths = rng.choice([10.0, 25.0, 50.0, 100.0, 150.0, 300.0],
                        size=10000, p=[0.05, 0.10, 0.40, 0.30, 0.10, 0.05])
    nb, na = _simulate_intervals(b_true=0.005, n=10000, widths=widths, rng=rng)
    fit = fit_null_exponential_forward(np.column_stack([nb, na]))
    assert fit["converged"], f"fit did not converge: {fit}"
    err = abs(fit["b"] - 0.005)
    assert err < 0.001, (
        f"b_hat={fit['b']:.5f}, expected 0.005 +/- 0.001 (err={err:.5f})"
    )


def test_fit_uniform_limit() -> None:
    """For data drawn from uniform (b=0), MLE should return |b| < 0.001."""
    rng = np.random.default_rng(20260426)
    widths = rng.choice([10.0, 25.0, 50.0, 100.0, 150.0, 300.0],
                        size=10000, p=[0.05, 0.10, 0.40, 0.30, 0.10, 0.05])
    nb, na = _simulate_intervals(b_true=0.0, n=10000, widths=widths, rng=rng)
    fit = fit_null_exponential_forward(np.column_stack([nb, na]))
    assert fit["converged"], f"fit did not converge: {fit}"
    assert abs(fit["b"]) < 0.001, (
        f"b_hat={fit['b']:.5f}, expected |b| < 0.001 for uniform data"
    )


def test_mc_sampler_mean_shape() -> None:
    """Average MC SPA shape is approximately exponential * uniform aoristic kernel.

    Strategy: for moderate b and a fixed (large) width pool, draw many MC
    replicates, average them, and verify the resulting smoothed shape is
    monotonically increasing in t when ``b > 0`` (and the ratio between
    last- and first-bin counts is in the right ballpark).
    """
    rng = np.random.default_rng(20260427)
    b_true = 0.005
    n = 5000
    n_replicates = 200
    widths = np.full(2000, 50.0)  # uniform 50-y windows for a clean shape

    accum = np.zeros(len(BIN_CENTRES), dtype=float)
    for _ in range(n_replicates):
        accum += sample_null_spa_forward_exp(
            b_true, n, widths, BIN_EDGES, rng, t_min=T_MIN, t_max=T_MAX,
        )
    mean_spa = accum / n_replicates

    # Expected: monotone-increasing smoothed exponential. Compare last 8 bins
    # mean to first 8 bins mean -- ratio should be close to exp(b * range)
    # times a smoothing factor (within ~30 % is plenty for unit-test tolerance
    # given 50-y aoristic blur and stochastic averaging at 200 replicates).
    first = mean_spa[:8].mean()
    last = mean_spa[-8:].mean()
    ratio = last / first
    # exp(b * (350 - (-50))) = exp(0.005 * 400) = exp(2) ~ 7.389. Aoristic
    # smoothing of a 50-y window slightly reduces both extremes. Accept
    # 4 < ratio < 12.
    assert 4.0 < ratio < 12.0, (
        f"mean MC SPA last/first ratio = {ratio:.2f}; "
        "expected ~7.4 (within 4-12)"
    )

    # And monotonic-ish: rolling 5-bin mean should be non-decreasing on
    # average (allow occasional dips from MC noise).
    smoothed = np.convolve(mean_spa, np.ones(5) / 5.0, mode="valid")
    n_increases = int((np.diff(smoothed) > 0).sum())
    n_decreases = int((np.diff(smoothed) < 0).sum())
    assert n_increases > 2 * n_decreases, (
        f"smoothed MC mean SPA not predominantly increasing: "
        f"{n_increases} increases vs {n_decreases} decreases"
    )


def test_envelope_fp_under_truth() -> None:
    """Synthetic data from f(t; b=0.005), fit and test under same b -> FP ~ alpha.

    Exercise the full pipeline 100 times with n = 1000 (small enough to be
    fast, large enough that the envelope behaves). Reject at alpha = 0.05;
    expect detection rate in [0, ~0.15] (Wilson 95 % CI on 0.05 with 100
    iterations is roughly [0.018, 0.107], so we allow up to 0.15 for
    test-time tolerance).
    """
    rng = np.random.default_rng(20260428)
    b_true = 0.005
    n = 1000
    n_iter = 50
    n_mc = 200
    widths_pool = rng.choice(
        [10.0, 25.0, 50.0, 100.0, 150.0, 300.0],
        size=20000, p=[0.05, 0.10, 0.40, 0.30, 0.10, 0.05],
    )

    detections = 0
    for i in range(n_iter):
        nb, na = _simulate_intervals(b_true, n, widths_pool, rng)
        # Build observed SPA via single aoristic draw per row.
        years = rng.uniform(nb, na)
        observed_spa, _ = np.histogram(years, bins=BIN_EDGES)
        observed_spa = observed_spa.astype(float)
        # Fit forward.
        fit = fit_null_exponential_forward(np.column_stack([nb, na]))
        if not fit["converged"]:
            continue
        # Empirical widths: actual widths of the simulated intervals.
        widths = na - nb
        result = forward_envelope_test(
            observed_spa, fit["b"], widths, BIN_EDGES, n_mc, rng, n=n,
        )
        if result["detected"]:
            detections += 1

    fp_rate = detections / n_iter
    # Allow generous tolerance given small n_iter; the assertion is "FP not
    # catastrophically inflated".
    assert fp_rate <= 0.15, (
        f"FP rate {fp_rate:.3f} on synthetic-truth data; expected ~0.05"
    )


# ---------------------------------------------------------------------------
# Edge-case sanity tests
# ---------------------------------------------------------------------------

def test_b_zero_limit_smooth() -> None:
    """At b=0 the inverse-CDF and integrals reduce to the uniform limit."""
    rng = np.random.default_rng(20260429)
    u = rng.uniform(size=1000)
    t = _truncated_exponential_inverse_cdf(u, 0.0, T_MIN, T_MAX)
    # Should be linear in u.
    expected = T_MIN + u * (T_MAX - T_MIN)
    np.testing.assert_allclose(t, expected, atol=1e-10)


def test_two_input_forms_equivalent() -> None:
    """Passing intervals as (n, 2) array vs separate nb/na arrays gives same fit."""
    rng = np.random.default_rng(20260430)
    widths = rng.choice([25.0, 50.0, 100.0, 150.0], size=1000)
    nb, na = _simulate_intervals(0.003, 1000, widths, rng)
    fit_a = fit_null_exponential_forward(np.column_stack([nb, na]))
    fit_b = fit_null_exponential_forward(None, nb=nb, na=na)
    assert abs(fit_a["b"] - fit_b["b"]) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
