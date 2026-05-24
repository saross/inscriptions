#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-mixture-fit-noncentred.py
============================

Non-centred reparameterisation of the H2.1 multinomial mixture model.
This is a follow-up to the Experiment-A diagnostic
(``runs/2026-05-24-validation-investigation``) that found the α=0.95
posterior converges to biased α ≈ 0.74-0.86 even at the hardest NUTS
setting. The hypothesis tested here: the centred Gaussian random walk
on ``log_pgen_increments`` has funnel geometry around the
hierarchical scale ``sigma_smooth`` that even the hardest-effort
sampler cannot fully traverse, leaving the chain in a biased mode.

Diff vs the production ``02-cell-mixture-fit.py`` (centred):
------------------------------------------------------------
ONLY the construction of ``log_pgen_increments`` changes. Everything
else — Beta(2,2) on alpha, Dirichlet on tier_weights, HalfNormal(1) on
sigma_smooth, the cumsum-then-softmax chain, the Multinomial
observation — is byte-for-byte identical.

Centred (original lines 168-174 of 02-cell-mixture-fit.py):
    sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
    log_pgen_increments = pm.Normal(
        "log_pgen_increments",
        mu=0.0,
        sigma=sigma_smooth,
        shape=n_bins - 1,
    )

Non-centred (this file):
    sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
    z_pgen = pm.Normal("z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1)
    log_pgen_increments = pm.Deterministic(
        "log_pgen_increments", sigma_smooth * z_pgen,
    )

Mathematical equivalence: if z ~ Normal(0, 1) and σ is independent of
z, then σ·z ~ Normal(0, σ). The induced prior on
``log_pgen_increments``, and hence on ``log_pgen_raw`` (via cumsum) and
``p_gen`` (via softmax), is identical to the centred construction.
The change affects only the sampler's parameter-space geometry: the
sampler now explores (z, σ) which is approximately spherical and
free of the σ–increments funnel.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-24, follow-up to Experiment A.
"""

from __future__ import annotations

import warnings

import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import pymc as pm  # noqa: E402
import pytensor.tensor as pt  # noqa: E402


def build_model_noncentred(
    y: np.ndarray,
    tier_basis: np.ndarray,
) -> pm.Model:
    """Non-centred variant of the H2.1 mixture model.

    Parameters
    ----------
    y : (N_BINS,) int array
        Observed multinomial counts per 5-year bin.
    tier_basis : (3, N_BINS) float array
        Tier basis matrix; each row sums to 1.

    Returns
    -------
    model : pymc.Model
    """
    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        # Mixture weight (prereg §3 line 206) — IDENTICAL to centred.
        alpha = pm.Beta("alpha", 2.0, 2.0)
        # Tier weights (Dirichlet uniform) — IDENTICAL to centred.
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float),
        )
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis),
        )
        # GRW bandwidth — IDENTICAL to centred.
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)

        # *** Non-centred reparameterisation begins ***
        # Sample standard-normal raw increments, then scale by
        # sigma_smooth deterministically. This breaks the funnel
        # between sigma_smooth and the increment scale.
        z_pgen = pm.Normal(
            "z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1,
        )
        log_pgen_increments = pm.Deterministic(
            "log_pgen_increments", sigma_smooth * z_pgen,
        )
        # *** Non-centred reparameterisation ends ***

        # Cumsum and softmax — IDENTICAL to centred.
        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)],
        )
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))

        # Mixture and observation — IDENTICAL to centred.
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)

    return model


def build_model_centred(
    y: np.ndarray,
    tier_basis: np.ndarray,
) -> pm.Model:
    """Centred reference variant (copy of production
    ``02-cell-mixture-fit.py::build_model``) for the prior-equivalence
    sanity check ONLY. Not used for production fits."""
    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"
    with pm.Model() as model:
        alpha = pm.Beta("alpha", 2.0, 2.0)
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float),
        )
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis),
        )
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
        log_pgen_increments = pm.Normal(
            "log_pgen_increments",
            mu=0.0,
            sigma=sigma_smooth,
            shape=n_bins - 1,
        )
        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)],
        )
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)
    return model
