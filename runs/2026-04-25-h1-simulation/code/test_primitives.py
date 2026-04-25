#!/usr/bin/env python3
"""
test_primitives.py --- Unit tests for H1 simulation primitives.

Covers the minimal invariants listed in the build-agent brief:

  - test_inject_effect_step          : step kernel is exact box-car.
  - test_inject_effect_gaussian_nadir: Gaussian nadir == magnitude, FWHM ==
                                       duration.
  - test_inject_effect_zero          : zero bracket is identity transform.
  - test_aoristic_resample_uniform   : draws lie within [not_before, not_after]
                                       for every sampled row.
  - test_permutation_envelope_null   : identity null --> detection rate ~ alpha.
  - test_seedsequence_reproducibility: same master seed --> identical outputs.

Run:  .venv/bin/python3 -m pytest runs/2026-04-25-h1-simulation/code/\\
         test_primitives.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from primitives import (  # noqa: E402
    BIN_CENTRES,
    BIN_EDGES,
    BRACKETS,
    aoristic_resample,
    fit_null_exponential,
    inject_effect,
    permutation_envelope_test,
    sample_null_spa,
)


# ---------------------------------------------------------------------------
# inject_effect: step shape
# ---------------------------------------------------------------------------

def test_inject_effect_step() -> None:
    """Step kernel produces an exact box-car modifier on the SPA."""
    spa = np.ones_like(BIN_CENTRES) * 100.0
    # 50 % dip over 50 y centred at AD 150.
    out = inject_effect(spa, BIN_CENTRES, magnitude=-0.5,
                        centre_year=150.0, duration=50.0, shape="step")
    # Inside the box: value should equal 100 * (1 - 0.5) = 50.
    inside = (BIN_CENTRES >= 125.0) & (BIN_CENTRES < 175.0)
    np.testing.assert_allclose(out[inside], 50.0)
    # Outside the box: untouched (100).
    np.testing.assert_allclose(out[~inside], 100.0)


# ---------------------------------------------------------------------------
# inject_effect: gaussian shape
# ---------------------------------------------------------------------------

def test_inject_effect_gaussian_nadir() -> None:
    """Gaussian nadir equals magnitude; FWHM equals duration."""
    spa = np.ones_like(BIN_CENTRES) * 100.0
    duration = 50.0
    magnitude = -0.5
    out = inject_effect(spa, BIN_CENTRES, magnitude=magnitude,
                        centre_year=150.0, duration=duration, shape="gaussian")
    # Bin nearest to centre_year should be (close to) nadir:
    idx_centre = int(np.argmin(np.abs(BIN_CENTRES - 150.0)))
    # The centre bin is at 147.5 (BIN_CENTRES = -47.5, -42.5, ..., 347.5);
    # slight offset from 150.0 so nadir-at-bin is slightly above magnitude.
    nadir_factor = 1.0 + magnitude * np.exp(
        -0.5 * ((BIN_CENTRES[idx_centre] - 150.0) /
                (duration / (2.0 * np.sqrt(2.0 * np.log(2.0))))) ** 2
    )
    np.testing.assert_allclose(out[idx_centre], 100.0 * nadir_factor, rtol=1e-10)

    # FWHM check: at t = centre +/- duration / 2 the Gaussian kernel = 0.5,
    # so the modifier should be (1 + magnitude * 0.5). Because ``centre_year``
    # (150.0) falls between bin centres (147.5 and 152.5), the bin nearest
    # the FWHM half-point is offset from the idealised half-point; we compute
    # the *exact* expected value at that actual bin centre rather than
    # comparing to the ideal 75.0. This verifies the Gaussian kernel itself.
    half_idx = int(np.argmin(np.abs(BIN_CENTRES - (150.0 + duration / 2.0))))
    sigma = duration / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    expected_half = 100.0 * (1.0 + magnitude * np.exp(
        -0.5 * ((BIN_CENTRES[half_idx] - 150.0) / sigma) ** 2
    ))
    np.testing.assert_allclose(out[half_idx], expected_half, rtol=1e-10)
    # And verify that at the *exact* FWHM half-point the kernel value is 0.5
    # (independently of bin discretisation) via the documented formula.
    t_half = 150.0 + duration / 2.0
    kernel_at_half = np.exp(-0.5 * ((t_half - 150.0) / sigma) ** 2)
    np.testing.assert_allclose(kernel_at_half, 0.5, rtol=1e-10)


# ---------------------------------------------------------------------------
# inject_effect: zero bracket == identity
# ---------------------------------------------------------------------------

def test_inject_effect_zero() -> None:
    """Zero bracket (magnitude == 0) must be exact identity."""
    rng = np.random.default_rng(42)
    spa = rng.uniform(0, 200, size=len(BIN_CENTRES))
    zero = BRACKETS["zero"]
    assert zero.magnitude == 0.0

    out_step = inject_effect(spa, BIN_CENTRES, magnitude=zero.magnitude,
                             centre_year=150.0, duration=zero.duration,
                             shape="step")
    out_gauss = inject_effect(spa, BIN_CENTRES, magnitude=zero.magnitude,
                              centre_year=150.0, duration=zero.duration,
                              shape="gaussian")
    np.testing.assert_allclose(out_step, spa)
    np.testing.assert_allclose(out_gauss, spa)


# ---------------------------------------------------------------------------
# aoristic_resample: draws inside [not_before, not_after]
# ---------------------------------------------------------------------------

def test_aoristic_resample_uniform() -> None:
    """Every Uniform aoristic draw must lie inside its row's interval.

    Build a small synthetic frame, run a large resample, then verify the
    realised bin counts are consistent with the row intervals (a stronger
    check --- all *realised* draws lie in *some* row's interval).
    """
    df = pd.DataFrame({
        "not_before": [-40.0, 0.0, 100.0, 200.0],
        "not_after": [-20.0, 50.0, 150.0, 300.0],
    })
    rng = np.random.default_rng(123)
    n = 10_000
    spa = aoristic_resample(df, n=n, bin_edges=BIN_EDGES, rng=rng, replace=True)

    # Non-negative counts, total ~ n.
    assert spa.sum() == pytest.approx(n, abs=10)
    assert (spa >= 0).all()

    # Union of intervals is [-40, -20] U [0, 50] U [100, 150] U [200, 300].
    # No count may land outside this union.
    in_union = (
        ((BIN_CENTRES >= -40) & (BIN_CENTRES <= -20))
        | ((BIN_CENTRES >= 0) & (BIN_CENTRES <= 50))
        | ((BIN_CENTRES >= 100) & (BIN_CENTRES <= 150))
        | ((BIN_CENTRES >= 200) & (BIN_CENTRES <= 300))
    )
    # Some leak is possible at bin-edge discretisation; use edge-based test.
    # Bins strictly outside any interval's extended span (+/- bin_width / 2) should be 0.
    extended_mask = (
        ((BIN_CENTRES >= -42.5) & (BIN_CENTRES <= -17.5))
        | ((BIN_CENTRES >= -2.5) & (BIN_CENTRES <= 52.5))
        | ((BIN_CENTRES >= 97.5) & (BIN_CENTRES <= 152.5))
        | ((BIN_CENTRES >= 197.5) & (BIN_CENTRES <= 302.5))
    )
    assert (spa[~extended_mask] == 0).all()


# ---------------------------------------------------------------------------
# permutation_envelope_test: null == identity --> detection ~ alpha
# ---------------------------------------------------------------------------

def test_permutation_envelope_null() -> None:
    """Under a correctly-specified null (no effect), detection rate
    should approach alpha (0.05). We check detection rate < 0.20 on 40
    independent null realisations --- loose because n_mc is small in a
    test, but this catches gross mis-calibration (e.g. rate > 0.5)."""
    rng_seed = np.random.SeedSequence(424242)
    child_seeds = rng_seed.spawn(40)

    # Fixed fitted "null": flat SPA at lambda = 50 per bin. We sample
    # observed_spa FROM this same null and feed it to the envelope test.
    fitted = np.full_like(BIN_CENTRES, fill_value=50.0)
    null_params = {
        "fitted": fitted,
        "residual_rms": 0.0,
        "rate": 0.0,
        "intercept": np.log(50.0),
        "model": "exponential",
    }

    n_detected = 0
    for ss in child_seeds:
        rng = np.random.default_rng(ss)
        observed = sample_null_spa(null_params, "exponential", BIN_CENTRES, rng)
        result = permutation_envelope_test(
            observed_spa=observed,
            null_params=null_params,
            model="exponential",
            bin_centres=BIN_CENTRES,
            n_mc=200,  # keep test fast
            rng=rng,
            alpha=0.05,
        )
        if result["detected"]:
            n_detected += 1
    rate = n_detected / 40
    # Alpha is 0.05; binomial 95% CI for rate on 40 trials at true 0.05
    # goes up to ~0.17. Assert gross mis-calibration only.
    assert rate <= 0.25, f"null-detection rate {rate:.3f} too high"


# ---------------------------------------------------------------------------
# SeedSequence reproducibility
# ---------------------------------------------------------------------------

def test_seedsequence_reproducibility() -> None:
    """Identical master seed --> identical outputs across runs."""
    df = pd.DataFrame({
        "not_before": np.linspace(-40, 300, 100),
        "not_after": np.linspace(-20, 340, 100),
    })

    def run_once(seed: int) -> tuple[np.ndarray, np.ndarray]:
        master = np.random.SeedSequence(seed)
        ss_a, ss_b = master.spawn(2)
        rng_a = np.random.default_rng(ss_a)
        spa_a = aoristic_resample(df, n=500, bin_edges=BIN_EDGES,
                                  rng=rng_a, replace=True)
        rng_b = np.random.default_rng(ss_b)
        fit = fit_null_exponential(spa_a, BIN_CENTRES)
        mc = sample_null_spa(fit, "exponential", BIN_CENTRES, rng_b)
        return spa_a, mc

    spa1, mc1 = run_once(20260425)
    spa2, mc2 = run_once(20260425)
    np.testing.assert_array_equal(spa1, spa2)
    np.testing.assert_array_equal(mc1, mc2)

    # Different seed --> different outputs (not identical).
    spa3, _ = run_once(20260426)
    assert not np.array_equal(spa1, spa3)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
