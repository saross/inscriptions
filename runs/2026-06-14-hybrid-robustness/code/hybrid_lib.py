#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hybrid_lib.py — the hybrid (global-θ) cross-classified model over all units.
============================================================================

Assembles the U production units into ONE PyMC fit (spec.md), identical to U
independent cross-classified `library` fits EXCEPT that θ_conv, θ_gen are single
GLOBAL scalars (estimated, wider prior) instead of per-unit Beta(κ=40) priors. α is
NOT pooled (units not exchangeable). The per-unit likelihood is the exact
cross-classified two-subset form; the convention basis is the FIXED corpus-wide slab
library (same as the production refit).

Batched over units: every per-unit quantity carries a leading U axis, so the model is
one set of vectorised RVs rather than a Python loop of U sub-models (faster sampling,
identical model).

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
sys.path.insert(0, str(REFIT / "code"))
import refit_lib as R  # noqa: E402  (per-unit cc data prep + fixed library + h2_lib paths)
import h2_lib as H  # noqa: E402


def assemble_unit_data() -> dict:
    """Build the stacked (U, …) observed arrays for the 29 production units.

    Returns y_aligned (U, K), y_nonaligned (U, K), k (U,), N (U,), plus the unit
    names/order. Reuses the production refit's per-unit cc data prep verbatim so the
    hybrid sees exactly the same data the lead refit did.
    """
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    units = R.enumerate_refit_units()
    y_al, y_non, k, N, names = [], [], [], [], []
    for u in units:
        d = R.build_unit_cc_data(R.subset_for(df, u, latin))
        y_al.append(d["y_aligned"])
        y_non.append(d["y_nonaligned"])
        k.append(d["k"])
        N.append(d["n_rows"])
        names.append(u["name"])
    return {
        "y_aligned": np.vstack(y_al).astype("int64"),
        "y_nonaligned": np.vstack(y_non).astype("int64"),
        "k": np.asarray(k, dtype="int64"),
        "N": np.asarray(N, dtype="int64"),
        "names": names,
    }


def build_model_hybrid(data: dict, library_basis: np.ndarray,
                       theta_conv_mu_kappa: tuple[float, float] = (0.85, 4.0),
                       theta_gen_mu_kappa: tuple[float, float] = (0.15, 4.0)):
    """The hybrid model (spec.md §"The model"). θ global + wider; α/shape per-unit.

    Parameters
    ----------
    data : dict
        From ``assemble_unit_data`` — y_aligned/y_nonaligned (U, K), k/N (U,).
    library_basis : (n_lib, K) float array
        The fixed corpus-wide slab library (rows sum to 1).
    theta_conv_mu_kappa, theta_gen_mu_kappa : (μ, κ)
        WIDE global θ priors (κ=4 default; the hybrid learns θ — spec §2).
    """
    import pymc as pm
    import pytensor.tensor as pt

    y_al = data["y_aligned"]
    y_non = data["y_nonaligned"]
    k_obs = data["k"]
    N = data["N"]
    U, K = y_al.shape
    n_lib = int(library_basis.shape[0])
    # Per-unit invariants (the cc factorisation, batched).
    assert (y_al.sum(axis=1) == k_obs).all(), "k != y_aligned row sums"
    assert (y_al.sum(axis=1) + y_non.sum(axis=1) == N).all(), "subset sums != N"

    ac, kc = theta_conv_mu_kappa
    ag, kg = theta_gen_mu_kappa

    with pm.Model(coords={"unit": data["names"], "bin": np.arange(K)}) as model:
        # GLOBAL measurement parameters (estimated, wide).
        theta_conv = pm.Beta("theta_conv", ac * kc, (1.0 - ac) * kc)
        theta_gen = pm.Beta("theta_gen", ag * kg, (1.0 - ag) * kg)

        # Per-unit α (NOT pooled) and convention weights (fixed library).
        alpha = pm.Beta("alpha", 1.0, 1.0, dims="unit")
        tier_weights = pm.Dirichlet("tier_weights", a=np.ones(n_lib), dims=("unit", "lib"),
                                    shape=(U, n_lib))
        p_conv = pt.dot(tier_weights, library_basis)          # (U, K)

        # Per-unit non-centred GRW p_gen (batched).
        sigma = pm.HalfNormal("sigma", 1.0, dims="unit")
        z = pm.Normal("z", 0.0, 1.0, shape=(U, K - 1))
        log_incr = sigma[:, None] * z                          # (U, K-1)
        log_raw = pt.concatenate([pt.zeros((U, 1)), pt.cumsum(log_incr, axis=1)], axis=1)
        log_centred = log_raw - pt.max(log_raw, axis=1, keepdims=True)
        unnorm = pt.exp(log_centred)
        p_gen = unnorm / pt.sum(unnorm, axis=1, keepdims=True)  # (U, K)

        # Alignment-conditional mixtures (cancellation-free simplex normalisation).
        a = alpha[:, None]
        w_a = pm.Deterministic("w_a", alpha * theta_conv + (1.0 - alpha) * theta_gen,
                               dims="unit")
        num_al = a * theta_conv * p_conv + (1.0 - a) * theta_gen * p_gen
        num_non = a * (1.0 - theta_conv) * p_conv + (1.0 - a) * (1.0 - theta_gen) * p_gen
        p_aligned = num_al / pt.sum(num_al, axis=1, keepdims=True)
        p_nonalign = num_non / pt.sum(num_non, axis=1, keepdims=True)

        # Observed (constants — one fit, no set_data).
        pm.Binomial("k_obs", n=N, p=w_a, observed=k_obs, dims="unit")
        pm.Multinomial("y_al_obs", n=k_obs, p=p_aligned, observed=y_al, dims=("unit", "bin"))
        pm.Multinomial("y_non_obs", n=(N - k_obs), p=p_nonalign, observed=y_non,
                       dims=("unit", "bin"))

    return model
