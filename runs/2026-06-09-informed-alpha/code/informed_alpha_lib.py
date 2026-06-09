#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
informed_alpha_lib.py — PROTOTYPE informed-α prior variant of the H2.1 mixture.
================================================================================

EXPLORATORY PROTOTYPE (2026-06-09). NOT a production change. Built for review
with Shawn; every design choice is flagged in the REPORT, not finalised here.

Why this exists
---------------
The H2.1 temporal-mixture (``build_model_f1_f3`` in
``runs/2026-06-06-convention-basis-redesign/revalidation/code/cell_lib.py``)
fits the editorial-convention fraction ``α`` with a *flat* ``Beta(1, 1)`` prior
against a *fixed shared* convention basis (one broad empire/Latin basis shared
across all units). For temporally-CONCENTRATED units — mostly frontier provinces
whose round-period dating clusters in their occupation window (AD ~100–300, where
their genuine signal also lives) — convention and genuine are confounded in time.
The smooth genuine component (GRW ``p_gen``) absorbs the period-concentrated
convention mass and ``α`` COLLAPSES far below the true convention fraction
(diagnostic: ``runs/2026-06-07-h2.1-launch-prep/outputs/production/
DIAGNOSTIC-alpha-identifiability-REPORT.md``). A per-unit basis OVER-attributes
instead. The split is under-identified from the temporal SHAPE alone.

The fix idea (Shawn's lead)
---------------------------
Inject the INDEPENDENT signal the temporal shape ignores: the unit's
grid-alignment / family-mass fraction (F1+F3 round-period mass fraction — an
observable proxy for convention computed from interval WIDTHS + round ENDPOINTS,
not from where the mass sits in time). Replace the flat ``α ~ Beta(1, 1)`` with
an INFORMED prior CENTRED on that family fraction, but kept WIDE so the data can
still move it. This should pull under-attributing units toward their true ``α``
without the per-unit basis's over-attribution.

What this module provides
-------------------------
``build_model_informed_alpha(y, tier_basis, alpha_a, alpha_b)`` — a byte-for-byte
copy of ``build_model_f1_f3`` with the SINGLE change being the ``α`` prior:

    α ~ Beta(alpha_a, alpha_b)        # informed; was Beta(1, 1)

plus ``beta_from_mean_concentration(mean, concentration)`` — the helper that maps
a target prior MEAN (the family fraction) + a CONCENTRATION (kept small/WIDE) to
the ``(a, b)`` Beta shape parameters. Everything else (Dirichlet tier_weights,
non-centred GRW ``p_gen``, the cumsum/softmax chain, the multinomial likelihood)
is identical to ``build_model_f1_f3`` so that the ONLY thing being tested is the
prior.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's exploratory brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------- #
# Prior parameterisation: mean + concentration → Beta(a, b).                    #
# --------------------------------------------------------------------------- #
def beta_from_mean_concentration(
    mean: float, concentration: float
) -> tuple[float, float]:
    """Map a target prior MEAN and a CONCENTRATION to Beta ``(a, b)`` parameters.

    The Beta distribution is parameterised here by its mean ``μ = a / (a + b)``
    and its concentration ``κ = a + b`` (sometimes called the "sample size" or
    "precision" of the Beta), giving::

        a = μ · κ
        b = (1 − μ) · κ

    A SMALL ``κ`` makes the prior WIDE (more mass spread toward both 0 and 1);
    a LARGE ``κ`` makes it a tight spike around ``μ``. For this prototype we want
    the prior to be informative about LOCATION (centred on the family fraction)
    but WEAK about CONFIDENCE (so the data can still move ``α``), hence a small
    ``κ`` (the prototype default sweep uses κ ∈ {4, 6, 8}; see the recovery
    script). For reference, ``κ = 2`` with ``μ = 0.5`` recovers the flat
    ``Beta(1, 1)`` status-quo prior exactly.

    Guard rails
    -----------
    The mean is clipped to ``[ε, 1 − ε]`` (ε = 1e-3) so that a family fraction of
    exactly 0 or 1 (which can occur for degenerate units) does not produce a
    zero-valued Beta parameter, which PyMC rejects. The concentration must be
    strictly positive.

    Parameters
    ----------
    mean : float
        Target prior mean for ``α`` — for this prototype the unit's
        grid-alignment family fraction (F1+F3 round-period mass fraction).
    concentration : float
        Beta concentration ``κ = a + b``. Smaller ⇒ wider prior. Must be > 0.

    Returns
    -------
    (a, b) : tuple[float, float]
        Beta shape parameters, both strictly positive.

    Examples
    --------
    >>> a, b = beta_from_mean_concentration(0.6, 6.0)
    >>> round(a, 3), round(b, 3)
    (3.6, 2.4)
    >>> beta_from_mean_concentration(0.5, 2.0)  # recovers flat Beta(1, 1)
    (1.0, 1.0)
    """
    if concentration <= 0:
        raise ValueError(f"concentration must be > 0, got {concentration!r}")
    eps = 1e-3
    mu = float(np.clip(mean, eps, 1.0 - eps))
    a = mu * concentration
    b = (1.0 - mu) * concentration
    return float(a), float(b)


# --------------------------------------------------------------------------- #
# Model builder — identical to build_model_f1_f3 EXCEPT the α prior.            #
# --------------------------------------------------------------------------- #
def build_model_informed_alpha(
    y: np.ndarray,
    tier_basis: np.ndarray,
    alpha_a: float,
    alpha_b: float,
):
    """Three-tier multinomial mixture with an INFORMED ``Beta(alpha_a, alpha_b)``
    prior on ``α`` (the editorial-convention fraction).

    This is a copy of ``build_model_f1_f3``
    (``runs/2026-06-06-convention-basis-redesign/revalidation/code/cell_lib.py``)
    with the SINGLE change::

        alpha = pm.Beta("alpha", alpha_a, alpha_b)   # was pm.Beta("alpha", 1, 1)

    Use ``beta_from_mean_concentration(family_fraction, κ)`` to obtain
    ``(alpha_a, alpha_b)`` from a target mean (the unit's family fraction) and a
    WIDE concentration. Everything else — the Dirichlet ``tier_weights``, the
    deterministic ``p_conv = tier_weights · tier_basis``, the ``HalfNormal``
    GRW bandwidth, the F3 non-centred ``z_pgen`` reparameterisation, the
    cumsum/softmax chain producing ``p_gen``, the mixture
    ``p_mix = α·p_conv + (1−α)·p_gen``, and the ``Multinomial`` likelihood — is
    byte-identical to ``build_model_f1_f3`` so the ONLY thing under test is the
    prior on ``α``.

    Parameters
    ----------
    y : (N_BINS,) int array
        Observed multinomial counts per 5-year bin.
    tier_basis : (3, N_BINS) float array
        The (shared) convention basis; each row sums to 1.
    alpha_a, alpha_b : float
        Beta shape parameters for the informed ``α`` prior. Both must be > 0.

    Returns
    -------
    model : pymc.Model
    """
    # Local import so the module can be imported (for the helper / docs) without
    # PyMC loaded — mirrors the cell_lib convention.
    import pymc as pm
    import pytensor.tensor as pt

    if alpha_a <= 0 or alpha_b <= 0:
        raise ValueError(
            f"alpha_a, alpha_b must both be > 0, got ({alpha_a}, {alpha_b})"
        )

    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        # THE ONLY CHANGE vs build_model_f1_f3: informed Beta prior on α.
        alpha = pm.Beta("alpha", alpha_a, alpha_b)

        # --- everything below is byte-identical to build_model_f1_f3 ---
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float)
        )
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis)
        )

        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)

        z_pgen = pm.Normal(
            "z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1
        )
        log_pgen_increments = pm.Deterministic(
            "log_pgen_increments", sigma_smooth * z_pgen
        )

        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)]
        )
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))

        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)

    return model
