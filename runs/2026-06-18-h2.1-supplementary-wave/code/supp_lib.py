#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
supp_lib.py — the two NEW supplementary-wave model builders (SPEC §3).
======================================================================

The H2.1 supplementary wave (``runs/2026-06-18-h2.1-supplementary-wave/SPEC.md``)
re-maps the lodged Dirichlet-multinomial (C5) and rescaled negative-binomial (C6)
supplementaries onto the **adopted cross-classified likelihood** (Amendment 04,
``joint_lib.build_model_cross_classified``). Both supplementaries keep the
cross-classified structural block VERBATIM — they only swap the two subset
*observation* terms — so the overdispersion enters the aligned / non-aligned
count vectors while α stays identified by the alignment contrast (SPEC §2.1,
Fork-1 resolution).

To guarantee the structural prior is byte-identical to the primary (SPEC §3:
"importing the shared block from joint_lib to guarantee the structural prior is
byte-identical — no copy-paste drift"), both builders call the single shared
helper ``joint_lib.cc_structural_block`` — the same helper the adopted primary
``build_model_cross_classified`` now calls. The only difference between the three
models is the likelihood:

  * primary : ``Multinomial(k, p_aligned)`` + ``Multinomial(n-k, p_nonalign)``
  * C5 (DM) : ``DirichletMultinomial(k, κ·p_aligned)`` + …(n-k, κ·p_nonalign)
  * C6 (NB) : ``NegativeBinomial(mu=k·p_aligned, α=φ)`` per bin + …(n-k, …)

In all three the per-inscription alignment split stays a clean Binomial
classification term (SPEC §3.1/§3.2): the prereg's overdispersion is bin-level /
compositional, which is exactly the two subset count-vectors, not the alignment
Bernoulli.

What this module provides
-------------------------
* ``build_model_cc_dirichlet_multinomial(...)`` — C5 (SPEC §3.1).
* ``build_model_cc_negbin(...)`` — C6 (SPEC §3.2).

Both expose ``k_data`` / ``y_al_data`` / ``y_non_data`` as mutable ``pm.Data``
(build-once + ``pm.set_data`` per realisation; required for the C10 aoristic-MC
and for the set_data-parity smoke gate, SPEC §3.4 gate 3).

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------- #
# Import the SHARED cross-classified structural block from joint_lib (the      #
# adopted primary). Absolute path: the repo lives at the same location on      #
# amd-tower and sapphire (standing rule).                                       #
# --------------------------------------------------------------------------- #
JOINT = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code"
)
if str(JOINT) not in sys.path:
    sys.path.insert(0, str(JOINT))
import joint_lib as J  # noqa: E402


def _validate_cc_counts(y_aligned: np.ndarray, y_nonaligned: np.ndarray,
                        k_cc: int, n_rows: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Shared count-consistency validation (parity with the primary builder).

    Casts the two subset count vectors to int64, checks they share a shape, and
    enforces the lumping/thinning bookkeeping ``k_cc == y_aligned.sum()`` and
    ``n_rows == y_aligned.sum() + y_nonaligned.sum()`` (so the cross-classified
    factorisation holds exactly).

    Returns
    -------
    (y_aligned_int64, y_nonaligned_int64, n_bins)
    """
    y_aligned = np.asarray(y_aligned, dtype="int64")
    y_nonaligned = np.asarray(y_nonaligned, dtype="int64")
    if y_aligned.shape != y_nonaligned.shape:
        raise ValueError(f"y_aligned shape {y_aligned.shape} != "
                         f"y_nonaligned shape {y_nonaligned.shape}")
    if int(y_aligned.sum()) != int(k_cc):
        raise ValueError(f"y_aligned sums to {int(y_aligned.sum())}, not k_cc={k_cc}")
    if int(y_aligned.sum() + y_nonaligned.sum()) != int(n_rows):
        raise ValueError("aligned + non-aligned counts do not sum to n_rows")
    return y_aligned, y_nonaligned, int(y_aligned.size)


# --------------------------------------------------------------------------- #
# C5 — Dirichlet-multinomial cross-classified model (SPEC §3.1).               #
# --------------------------------------------------------------------------- #
def build_model_cc_dirichlet_multinomial(
        y_aligned: np.ndarray, y_nonaligned: np.ndarray,
        k_cc: int, n_rows: int,
        tier_basis: np.ndarray | None,
        theta_conv_ab: tuple[float, float],
        theta_gen_ab: tuple[float, float],
        s_kappa: float = 1e3,
        kappa_fixed: float | None = None,
        pconv_mode: str = "library"):
    """C5: cross-classified Dirichlet-multinomial supplementary (SPEC §3.1).

    Replaces each subset's ``Multinomial`` with a ``DirichletMultinomial`` that
    shares ONE concentration ``κ`` (the single-κ lodged form, prereg l.192):
    larger κ ⇒ tighter to the multinomial; ``κ → ∞`` recovers the primary
    exactly. The Binomial classification term is RETAINED (the alignment split is
    a clean per-inscription Bernoulli; the prereg overdispersion is bin-level).

    ::

        kappa      ~ HalfNormal(σ = s_kappa)        # tuned on the pilot (SPEC §3.3)
        k_obs      ~ Binomial(n_rows, w_a)          observed = k_data
        y_al_obs   ~ DirichletMultinomial(k,     κ·p_aligned)   observed = y_al_data
        y_non_obs  ~ DirichletMultinomial(n-k,   κ·p_nonalign)  observed = y_non_data

    Parameters
    ----------
    y_aligned, y_nonaligned : (N_BINS,) int arrays
        Per-bin aligned / non-aligned subset counts.
    k_cc : int
        Total aligned count; must equal ``y_aligned.sum()``.
    n_rows : int
        Total inscriptions; must equal ``y_aligned.sum() + y_nonaligned.sum()``.
    tier_basis : (n_tiers, N_BINS) float array, or None
        Convention basis (None only for ``pconv_mode='free'``).
    theta_conv_ab, theta_gen_ab : (a, b)
        Beta shape parameters for the θ priors.
    s_kappa : float
        σ of the ``HalfNormal`` prior on κ (SPEC §3.3; default 1e3, re-tuned at
        pilot). Ignored when ``kappa_fixed`` is set.
    kappa_fixed : float or None
        If given, κ is PINNED to this constant (NOT sampled) — used by the
        smoke-test reduction gate (SPEC §3.4 gate 1) at κ ≈ 1e6 to certify the DM
        reduces to the primary. ``None`` (default) ⇒ κ is a free ``HalfNormal``.
    pconv_mode : str
        ``"library"`` (production) | ``"tiers3"`` | ``"free"``.

    Returns
    -------
    model : pymc.Model
        ``k_data`` / ``y_al_data`` / ``y_non_data`` are mutable ``pm.Data``
        (build-once + ``pm.set_data``; SPEC §3.4 gate 3).
    """
    import pymc as pm
    import pytensor.tensor as pt

    y_aligned, y_nonaligned, n_bins = _validate_cc_counts(
        y_aligned, y_nonaligned, k_cc, n_rows)

    with pm.Model() as model:
        # ---- SHARED structural block (byte-identical to the primary) ----
        blk = J.cc_structural_block(n_bins, tier_basis, theta_conv_ab,
                                    theta_gen_ab, pconv_mode=pconv_mode)
        w_a = blk["w_a"]
        p_aligned = blk["p_aligned"]
        p_nonalign = blk["p_nonalign"]

        # ---- the ONLY new structural node: the shared concentration κ ----
        if kappa_fixed is not None:
            # Smoke-gate reduction mode: pin κ to a large constant so the DM
            # concentrates to the multinomial. NOT a free parameter, so the
            # posterior has the SAME free dimensions as the primary.
            kappa = pt.constant(float(kappa_fixed))
        else:
            # → multinomial as κ → ∞; weakly informative across κ∈~[10, 1e4]
            # at s_kappa ≈ 1e3 (tuned on the pilot prior-predictive, SPEC §3.3).
            kappa = pm.HalfNormal("kappa", sigma=float(s_kappa))

        # ---- observed data: mutable for build-once + set_data ----
        # NB pm.Data downcasts int64 → int32 internally (pytensor intX); this is the
        # same downcast ceiling joint_lib.build_model_cross_classified flags — SAFE at
        # N ≤ ~15,000 (our largest unit is well under), UNSAFE only at N ≳ 2×10⁹ where
        # int32 overflows. Re-check before reusing this builder at that scale.
        k_data = pm.Data("k_data", np.asarray(int(k_cc), dtype="int64"))
        y_al_data = pm.Data("y_al_data", y_aligned)
        y_non_data = pm.Data("y_non_data", y_nonaligned)

        # ---- likelihood: Binomial classification + two DirichletMultinomials ----
        # The DM concentration vector ``a = κ·p`` MUST be strictly > 0 in every bin:
        # the DirichletMultinomial (like the NegBin below) HARD-ERRORS on a true zero
        # in ``a`` (a degenerate Dirichlet), UNLIKE the primary's Multinomial, which
        # tolerates ``p = 0`` at a zero-count bin. We rely on p_aligned / p_nonalign
        # being strictly positive — the structural block builds them as a normalised
        # vector of STRICTLY POSITIVE numerators (num_al / sum(num_al), with every
        # mixture term a product of positive probabilities), so every bin keeps a
        # small positive mass and ``a = κ·p > 0`` holds without a clip. (No clip is
        # added: clipping would alter the likelihood.)
        pm.Binomial("k_obs", n=int(n_rows), p=w_a, observed=k_data)
        pm.DirichletMultinomial("y_al_obs", n=k_data, a=kappa * p_aligned,
                                observed=y_al_data)
        pm.DirichletMultinomial("y_non_obs", n=int(n_rows) - k_data,
                                a=kappa * p_nonalign, observed=y_non_data)

    return model


# --------------------------------------------------------------------------- #
# C6 — rescaled negative-binomial cross-classified model (SPEC §3.2).          #
# --------------------------------------------------------------------------- #
def build_model_cc_negbin(
        y_aligned: np.ndarray, y_nonaligned: np.ndarray,
        k_cc: int, n_rows: int,
        tier_basis: np.ndarray | None,
        theta_conv_ab: tuple[float, float],
        theta_gen_ab: tuple[float, float],
        inv_phi_fixed: float | None = None,
        pconv_mode: str = "library"):
    """C6: cross-classified rescaled negative-binomial supplementary (SPEC §3.2).

    Per-bin independent ``NegativeBinomial`` on each subset's EXPECTED counts
    (``mu = subset_total · p_subset``), sharing one dispersion ``φ`` with
    ``1/φ ~ HalfNormal(1)`` (prereg l.192). Using the subset total as the rate
    base ``N`` avoids the absolute-scale degeneracy the prereg warns of. The
    Binomial classification term is RETAINED.

    ::

        inv_phi    ~ HalfNormal(1)                      # 1/φ, prereg l.192
        phi         = 1 / inv_phi
        k_obs      ~ Binomial(n_rows, w_a)              observed = k_data
        y_al_obs   ~ NegativeBinomial(mu=k·p_aligned,    α=φ)  observed = y_al_data
        y_non_obs  ~ NegativeBinomial(mu=(n-k)·p_nonalign, α=φ) observed = y_non_data

    NB this does NOT reduce bit-identically to the multinomial (different family
    by construction; the prereg frames it as a "cross-check", not a nested model).
    The sanity target is α close to the primary at large φ (low overdispersion) —
    the smoke-test large-φ gate (SPEC §3.4 gate 2) pins ``inv_phi`` tiny.

    Parameters
    ----------
    y_aligned, y_nonaligned : (N_BINS,) int arrays
        Per-bin aligned / non-aligned subset counts.
    k_cc : int
        Total aligned count; must equal ``y_aligned.sum()``.
    n_rows : int
        Total inscriptions; must equal ``y_aligned.sum() + y_nonaligned.sum()``.
    tier_basis : (n_tiers, N_BINS) float array, or None
        Convention basis (None only for ``pconv_mode='free'``).
    theta_conv_ab, theta_gen_ab : (a, b)
        Beta shape parameters for the θ priors.
    inv_phi_fixed : float or None
        If given, ``1/φ`` is PINNED to this small constant (φ → ∞, low
        overdispersion) — used by the smoke-test large-φ sanity gate (SPEC §3.4
        gate 2). ``None`` (default) ⇒ ``inv_phi`` is a free ``HalfNormal(1)``.
    pconv_mode : str
        ``"library"`` (production) | ``"tiers3"`` | ``"free"``.

    Returns
    -------
    model : pymc.Model
        ``k_data`` / ``y_al_data`` / ``y_non_data`` are mutable ``pm.Data``
        (build-once + ``pm.set_data``; SPEC §3.4 gate 3).
    """
    import pymc as pm
    import pytensor.tensor as pt

    y_aligned, y_nonaligned, n_bins = _validate_cc_counts(
        y_aligned, y_nonaligned, k_cc, n_rows)

    with pm.Model() as model:
        # ---- SHARED structural block (byte-identical to the primary) ----
        blk = J.cc_structural_block(n_bins, tier_basis, theta_conv_ab,
                                    theta_gen_ab, pconv_mode=pconv_mode)
        w_a = blk["w_a"]
        p_aligned = blk["p_aligned"]
        p_nonalign = blk["p_nonalign"]

        # ---- the ONLY new structural node: the shared dispersion φ ----
        if inv_phi_fixed is not None:
            # Smoke-gate large-φ mode: pin 1/φ tiny ⇒ φ huge ⇒ NegBin → Poisson
            # → multinomial-conditional. NOT a free parameter.
            inv_phi = pt.constant(float(inv_phi_fixed))
        else:
            inv_phi = pm.HalfNormal("inv_phi", sigma=1.0)  # 1/φ ~ HalfNormal(1)
        phi = pm.Deterministic("phi", 1.0 / inv_phi)

        # ---- observed data: mutable for build-once + set_data ----
        # NB pm.Data downcasts int64 → int32 internally (pytensor intX); the SAME
        # downcast ceiling joint_lib.build_model_cross_classified flags — SAFE at
        # N ≤ ~15,000 (our largest unit is well under), UNSAFE only at N ≳ 2×10⁹
        # where int32 overflows. Re-check before reusing this builder at that scale.
        k_data = pm.Data("k_data", np.asarray(int(k_cc), dtype="int64"))
        y_al_data = pm.Data("y_al_data", y_aligned)
        y_non_data = pm.Data("y_non_data", y_nonaligned)

        # ---- likelihood: Binomial classification + per-bin NegativeBinomials ----
        # mu = subset_total · p_subset (the lodged λ = N·p, with N = subset total).
        # As with the DM above, the per-bin rate ``mu = N·p`` MUST be strictly > 0:
        # the NegativeBinomial HARD-ERRORS on ``mu = 0`` (a degenerate rate), UNLIKE
        # the primary's Multinomial, which tolerates ``p = 0`` at a zero-count bin. We
        # rely on p_aligned / p_nonalign being strictly positive (the structural block
        # normalises strictly-positive numerators), so every bin keeps positive rate
        # mass without a clip. (No clip is added: clipping would alter the likelihood.)
        pm.Binomial("k_obs", n=int(n_rows), p=w_a, observed=k_data)
        pm.NegativeBinomial("y_al_obs", mu=k_data * p_aligned, alpha=phi,
                            observed=y_al_data)
        pm.NegativeBinomial("y_non_obs", mu=(int(n_rows) - k_data) * p_nonalign,
                            alpha=phi, observed=y_non_data)

    return model
