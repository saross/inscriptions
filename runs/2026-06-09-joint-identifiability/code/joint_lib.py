#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
joint_lib.py — JOINT identifiability-remediation mixture (temporal + classification).
=====================================================================================

The H2.1 temporal-mixture (``build_model_f1_f3`` in
``runs/2026-06-06-convention-basis-redesign/revalidation/code/cell_lib.py``) splits a
unit's summed-probability analysis (SPA) into an editorial-convention component
(fraction ``α``, shape ``p_conv`` = a Dirichlet reweighting of the shared 3-tier
calendar-slab basis) and a smooth genuine component (the GRW ``p_gen``). For
**temporally-concentrated** units convention and genuine are confounded in time, the
GRW absorbs the convention mass, and ``α`` collapses — the split is partially
identified (diagnostic ``runs/2026-06-07-h2.1-launch-prep/outputs/production/
DIAGNOSTIC-alpha-identifiability-REPORT.md``). An informed ``α`` *prior* could not fix
it (``runs/2026-06-09-informed-alpha/``): a prior over a partially-identified region is
never updated by the data (Gustafson 2010), and the GRW makes the likelihood
*confidently* wrong (Feller et al. 2016).

The remediation (spec ``runs/2026-06-09-joint-identifiability/spec.md``) injects the
independent signal the temporal shape ignores — each inscription's **grid-alignment**
(interval width + round endpoints) — as a SECOND LIKELIHOOD TERM that shares ``α``:

    π_align = α·θ_conv + (1 − α)·θ_gen
    k_aligned ~ Binomial(N_rows, π_align)

This is the concomitant-variable / latent-class-with-covariate remedy (Dayton &
Macready 1988 → Huang & Bandeen-Roche 2004), whose archaeological archetype is the
OxCal two-component outlier mixture (Bronk Ramsey 2009). ``θ_conv`` (≈ P[aligned |
convention]) and ``θ_gen`` (≈ P[aligned | genuine]) are calibrated from the
identifiable units (``calibrate_theta.py``) and supplied as informative priors so that
``k`` informs ``α`` (a single binomial cannot identify all three jointly).

What this module provides
-------------------------
* ``aligned_indicator(df, rule="C")`` — the per-inscription convention-typed indicator.
* ``beta_from_mean_concentration(mean, kappa)`` — (a, b) for a θ prior (μ, κ).
* ``build_model_joint(y, k_aligned, n_rows, tier_basis, theta_conv_ab, theta_gen_ab)``
  — the joint model: temporal block byte-identical to ``build_model_f1_f3``, plus the
  classification binomial.
* ``slab_mixture_spa(slabs, env)`` — aoristic SPA of a realistic round-endpoint slab
  mixture (the realistic convention shape; NOT a narrow Gaussian).
* ``gaussian_pgen`` / ``regnal_cluster_pgen`` / ``uniform_pgen`` — genuine-shape helpers.

Design principle — the temporal block is a VERBATIM copy of ``build_model_f1_f3`` (as
``informed_alpha_lib`` did), so the ONLY new thing under test is the classification term.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# Envelope constants (mirror h2_lib / cell_lib; the basis is built on these).   #
# --------------------------------------------------------------------------- #
ENV_START = -50
ENV_END = 350
BIN_SIZE = 5
N_BINS = (ENV_END - ENV_START) // BIN_SIZE  # 80
BIN_EDGES = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

# Family-classifier constants — VERBATIM from h2_lib / 02-build-empirical-basis.py.
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4


# --------------------------------------------------------------------------- #
# Grid-alignment (convention-typed) indicator.                                  #
# --------------------------------------------------------------------------- #
def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    """VERBATIM from h2_lib.round_aligned: x mod ``mod`` in {0, 1, mod-1}."""
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def classify_family(nb: np.ndarray, na: np.ndarray, dr: np.ndarray) -> np.ndarray:
    """VERBATIM family classifier (h2_lib.classify_family), taking arrays.

    Returns one of {F1_round, F3_periodic, Tight, F2_Other, Big} per inscription.
    """
    f1 = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3 = np.isin(dr, list(F3_WIDTHS)) & round_aligned(nb, 10) & round_aligned(na, 10) & ~f1
    fam = np.full(len(nb), "Big", dtype=object)
    tight = (dr <= TIGHT_MAX) & ~f1 & ~f3
    big = (dr >= 49) & ~f1
    other = ~(f1 | f3 | tight | big)
    fam[f1] = "F1_round"
    fam[f3] = "F3_periodic"
    fam[tight] = "Tight"
    fam[other] = "F2_Other"
    fam[big] = "Big"
    return fam


def aligned_indicator(df: pd.DataFrame, rule: str = "C") -> np.ndarray:
    """Per-inscription convention-typed (grid-aligned) indicator (spec §3).

    Expects columns ``nb``, ``na``, ``date_range`` (as built by
    ``h2_lib.load_filtered_lire``).

    Rules
    -----
    ``"C"`` (lead) : ``family ∈ {F1_round, F3_periodic}`` OR a ``Big`` slab whose
        BOTH endpoints are on the 25-year grid (``round_aligned(nb,25) ∧
        round_aligned(na,25)``). The "round-endpoint grid-alignment score that ALSO
        credits wide Big slabs, not just F1+F3."
    ``"A"`` : ``family ∈ {F1_round, F3_periodic}`` only (robustness comparison).
    ``"D"`` : pure geometry — both endpoints on the 25-year grid AND width ≥ 25
        (robustness comparison; no family taxonomy).

    Returns
    -------
    (N,) bool array — True where the inscription is convention-typed.
    """
    nb = df["nb"].to_numpy()
    na = df["na"].to_numpy()
    dr = df["date_range"].to_numpy()
    if rule == "A":
        fam = classify_family(nb, na, dr)
        return np.isin(fam, ["F1_round", "F3_periodic"])
    if rule == "C":
        fam = classify_family(nb, na, dr)
        f1f3 = np.isin(fam, ["F1_round", "F3_periodic"])
        big_round = (fam == "Big") & round_aligned(nb, 25) & round_aligned(na, 25)
        return f1f3 | big_round
    if rule == "D":
        return round_aligned(nb, 25) & round_aligned(na, 25) & (dr >= 25)
    raise ValueError(f"unknown aligned-indicator rule {rule!r}")


# --------------------------------------------------------------------------- #
# Beta(μ, κ) reparameterisation for the θ priors (cf. informed_alpha_lib).      #
# --------------------------------------------------------------------------- #
def beta_from_mean_concentration(mean: float, kappa: float) -> tuple[float, float]:
    """Map a target mean μ and concentration κ = a + b to Beta ``(a, b)``.

    ``a = μ·κ``, ``b = (1 − μ)·κ``. Larger κ ⇒ tighter prior. Mean clipped to
    ``[1e-3, 1 − 1e-3]`` so degenerate fractions do not produce a zero parameter.
    """
    if kappa <= 0:
        raise ValueError(f"kappa must be > 0, got {kappa!r}")
    eps = 1e-3
    mu = float(np.clip(mean, eps, 1.0 - eps))
    return float(mu * kappa), float((1.0 - mu) * kappa)


# --------------------------------------------------------------------------- #
# Realistic convention shape: aoristic SPA of a round-endpoint slab mixture.     #
# --------------------------------------------------------------------------- #
def _aoristic_spa(nb: np.ndarray, na: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    """Weighted aoristic SPA on the envelope (each interval deposits ``weight``
    uniformly across [nb, na], normalised by ORIGINAL width, clipped to envelope).

    Mirrors ``h2_lib.aoristic_spa`` but allows per-interval weights (for slab
    mixtures). Returns a length-``N_BINS`` vector (NOT normalised to 1)."""
    spa = np.zeros(N_BINS)
    nb = np.asarray(nb, dtype=float)
    na = np.asarray(na, dtype=float)
    if nb.size == 0:
        return spa
    if weights is None:
        weights = np.ones_like(nb)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb
    valid = (width > 0) & (na_c > nb_c)
    nb_c, na_c, width, w = nb_c[valid], na_c[valid], width[valid], weights[valid]
    for i in range(N_BINS):
        lo, hi = BIN_EDGES[i], BIN_EDGES[i + 1]
        overlap = np.maximum(np.minimum(hi, na_c) - np.maximum(lo, nb_c), 0.0)
        spa[i] = (w * overlap / width).sum()
    return spa


def slab_mixture_spa(slabs: list[tuple[int, int]],
                     weights: list[float] | None = None) -> np.ndarray:
    """Normalised aoristic SPA of a mixture of round-endpoint convention slabs.

    Each slab ``(lo, hi)`` is a wide editorial bracket (e.g. ``(101, 300)`` — "the
    occupation period"). The result is the realistic broad-slab convention shape the
    spec calls for (NOT a narrow Gaussian). Sums to 1.
    """
    if not slabs:
        raise ValueError("slabs must be non-empty")
    nb = np.array([s[0] for s in slabs], dtype=float)
    na = np.array([s[1] for s in slabs], dtype=float)
    w = np.ones(len(slabs)) if weights is None else np.asarray(weights, dtype=float)
    spa = _aoristic_spa(nb, na, w)
    s = spa.sum()
    if s <= 0:
        raise ValueError(f"slab mixture {slabs} produced zero-sum SPA")
    return spa / s


# --------------------------------------------------------------------------- #
# Genuine-shape helpers (sum-to-1 p_gen vectors).                               #
# --------------------------------------------------------------------------- #
def gaussian_pgen(mu: float, sigma: float) -> np.ndarray:
    """Single-peak genuine shape (normalised Gaussian over bin centres)."""
    z = (BIN_CENTRES - mu) / sigma
    v = np.exp(-0.5 * z * z)
    return v / v.sum()


def regnal_cluster_pgen(mus: list[float], sigma: float = 12.0,
                        weights: list[float] | None = None,
                        baseline: float = 0.15) -> np.ndarray:
    """Peaked genuine shape: a cluster of reign-scale spikes on a low baseline.

    The recovery grid's hard corner — sharp genuine peaks the GRW can confuse with
    period-concentrated convention. ``baseline`` is the uniform floor weight.
    """
    w = np.ones(len(mus)) if weights is None else np.asarray(weights, dtype=float)
    v = np.zeros(N_BINS)
    for mu, wi in zip(mus, w):
        g = np.exp(-0.5 * ((BIN_CENTRES - mu) / sigma) ** 2)
        v = v + wi * g / g.sum()
    v = v / v.sum()
    v = (1.0 - baseline) * v + baseline * (np.ones(N_BINS) / N_BINS)
    return v / v.sum()


def uniform_pgen() -> np.ndarray:
    """Flat genuine control."""
    return np.ones(N_BINS) / N_BINS


# --------------------------------------------------------------------------- #
# Largest-remainder rounding (VERBATIM from h2_lib) for integer y from mass.     #
# --------------------------------------------------------------------------- #
def largest_remainder(mass: np.ndarray) -> np.ndarray:
    """Hare rounding of a per-bin mass vector to integers summing to round(sum)."""
    total = int(round(float(mass.sum())))
    floors = np.floor(mass).astype(np.int64)
    if total <= 0:
        return np.zeros_like(floors)
    deficit = total - int(floors.sum())
    remainder = mass - np.floor(mass)
    if deficit > 0:
        idx = np.argsort(-remainder, kind="stable")[:deficit]
        floors[idx] += 1
    elif deficit < 0:
        idx = np.argsort(remainder, kind="stable")[: (-deficit)]
        floors[idx] -= 1
    return floors


# --------------------------------------------------------------------------- #
# The JOINT model.                                                              #
# --------------------------------------------------------------------------- #
def build_model_joint(y: np.ndarray, k_aligned: int, n_rows: int,
                      tier_basis: np.ndarray,
                      theta_conv_ab: tuple[float, float],
                      theta_gen_ab: tuple[float, float]):
    """Joint temporal-mixture + grid-alignment-classification model (spec §4).

    The temporal block (alpha prior, Dirichlet tier_weights, ``p_conv``, the
    non-centred GRW ``p_gen``, the mixture, and the Multinomial likelihood) is
    BYTE-IDENTICAL to ``build_model_f1_f3``
    (``runs/2026-06-06-convention-basis-redesign/revalidation/code/cell_lib.py``).
    The ONLY addition is the classification binomial sharing ``alpha``::

        theta_conv ~ Beta(*theta_conv_ab)            # P(aligned | convention), prior ~1
        theta_gen  ~ Beta(*theta_gen_ab)             # P(aligned | genuine),    prior ~0
        pi_align    = alpha*theta_conv + (1-alpha)*theta_gen
        k_obs      ~ Binomial(n_rows, pi_align)      observed = k_aligned

    Parameters
    ----------
    y : (N_BINS,) int array
        Observed multinomial counts per 5-year bin (largest-remainder of the SPA).
    k_aligned : int
        Number of convention-typed (grid-aligned) inscriptions in the unit.
    n_rows : int
        Total inscriptions in the unit (the binomial denominator).
    tier_basis : (n_tiers, N_BINS) float array
        Shared convention basis; each row sums to 1.
    theta_conv_ab, theta_gen_ab : (a, b)
        Beta shape parameters for the θ priors (from ``beta_from_mean_concentration``).

    Returns
    -------
    model : pymc.Model
        ``y`` and ``k_aligned`` are wrapped in mutable ``pm.Data`` ("y_data", "k_data"),
        so a caller may build the model once per cell and swap each replicate's data via
        ``pm.set_data({"y_data": ..., "k_data": ...})`` without rebuilding the graph — this
        is what stops the per-fit PyTensor recompile/leak. A single build+sample is unchanged.
    """
    import pymc as pm
    import pytensor.tensor as pt

    if not (0 <= k_aligned <= n_rows):
        raise ValueError(f"k_aligned {k_aligned} not in [0, n_rows={n_rows}]")
    a_conv, b_conv = theta_conv_ab
    a_gen, b_gen = theta_gen_ab
    if min(a_conv, b_conv, a_gen, b_gen) <= 0:
        raise ValueError("theta Beta parameters must all be > 0")

    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        # ---- temporal block: BYTE-IDENTICAL to build_model_f1_f3 ----
        alpha = pm.Beta("alpha", 1.0, 1.0)
        tier_weights = pm.Dirichlet("tier_weights", a=np.ones(n_tiers, dtype=float))
        p_conv = pm.Deterministic("p_conv", pt.dot(tier_weights, tier_basis))
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
        z_pgen = pm.Normal("z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1)
        log_pgen_increments = pm.Deterministic("log_pgen_increments", sigma_smooth * z_pgen)
        log_pgen_raw = pt.concatenate([pt.zeros((1,)), pt.cumsum(log_pgen_increments)])
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        # Observed counts as a MUTABLE container so a caller can build the model ONCE per
        # cell and swap y across replicates with pm.set_data — this keeps the graph constant
        # so PyTensor reuses the cached compiled logp instead of recompiling (and retaining
        # ~32 MB) every fit. For a single build+sample it is identical to `observed=y`.
        y_data = pm.Data("y_data", np.asarray(y, dtype="int64"))
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y_data)

        # ---- NEW: classification binomial sharing alpha ----
        theta_conv = pm.Beta("theta_conv", a_conv, b_conv)
        theta_gen = pm.Beta("theta_gen", a_gen, b_gen)
        pi_align = pm.Deterministic(
            "pi_align", alpha * theta_conv + (1.0 - alpha) * theta_gen
        )
        # k_aligned likewise mutable (swapped per replicate alongside y_data).
        k_data = pm.Data("k_data", np.asarray(int(k_aligned), dtype="int64"))
        pm.Binomial("k_obs", n=int(n_rows), p=pi_align, observed=k_data)

    return model


# --------------------------------------------------------------------------- #
# The CROSS-CLASSIFIED time × alignment model (D-B).                            #
# --------------------------------------------------------------------------- #
def build_model_cross_classified(y_aligned: np.ndarray, y_nonaligned: np.ndarray,
                                 k_cc: int, n_rows: int,
                                 tier_basis: np.ndarray | None,
                                 theta_conv_ab: tuple[float, float],
                                 theta_gen_ab: tuple[float, float],
                                 pconv_mode: str = "library"):
    """Cross-classified time × alignment model (``cross-classified-spec.md`` §1).

    The EXACT likelihood of the per-inscription generative process (type ~
    Bernoulli(α); bin ~ p_type; aligned ~ Bernoulli(θ_type)), by the standard
    lumping/thinning factorisation (signoff §1)::

        w_a        = α·θ_conv + (1−α)·θ_gen                       # P(aligned)
        p_aligned   = (α·θ_conv·p_conv     + (1−α)·θ_gen·p_gen)     / w_a
        p_nonalign  = (α·(1−θ_conv)·p_conv + (1−α)·(1−θ_gen)·p_gen) / (1−w_a)
        k_cc       ~ Binomial(n_rows, w_a)
        y_aligned  ~ Multinomial(k_cc,          p_aligned)
        y_nonalign ~ Multinomial(n_rows − k_cc, p_nonalign)

    No estimated (contaminated) basis enters: ``p_conv`` and ``p_gen`` are
    identified by the CONTRAST between the two alignment subsets. The α prior,
    GRW ``p_gen`` block, and θ priors are verbatim from ``build_model_joint``.

    Parameters
    ----------
    y_aligned, y_nonaligned : (N_BINS,) int arrays
        Per-bin counts of the aligned / non-aligned subsets (``grid_lib.generate_cc``).
    k_cc : int
        Total aligned count; must equal ``y_aligned.sum()``.
    n_rows : int
        Total inscriptions; must equal ``y_aligned.sum() + y_nonaligned.sum()``.
    tier_basis : (n_tiers, N_BINS) float array, or None
        Convention basis for ``pconv_mode`` ``"tiers3"`` (the shared Amendment-03
        3-tier basis) or ``"library"`` (the deterministic slab library); must be
        None for ``"free"``.
    theta_conv_ab, theta_gen_ab : (a, b)
        Beta shape parameters for the θ priors.
    pconv_mode : str
        ``"tiers3"`` | ``"library"`` — ``p_conv = tier_weights · tier_basis``
        (Dirichlet weights); ``"free"`` — ``p_conv`` gets its own non-centred GRW
        mirroring ``p_gen`` (signoff §2 arms).

    Returns
    -------
    model : pymc.Model
        ``y_aligned``, ``y_nonaligned``, and ``k_cc`` are mutable ``pm.Data``
        ("y_al_data", "y_non_data", "k_data") — build once per cell, swap each
        replicate via ``pm.set_data`` (the lead's set_data lesson; spec §4).
    """
    import pymc as pm
    import pytensor.tensor as pt

    if pconv_mode not in ("tiers3", "library", "free"):
        raise ValueError(f"unknown pconv_mode {pconv_mode!r}")
    if pconv_mode == "free":
        if tier_basis is not None:
            raise ValueError("tier_basis must be None for pconv_mode='free'")
    elif tier_basis is None:
        raise ValueError(f"tier_basis is required for pconv_mode={pconv_mode!r}")
    a_conv, b_conv = theta_conv_ab
    a_gen, b_gen = theta_gen_ab
    if min(a_conv, b_conv, a_gen, b_gen) <= 0:
        raise ValueError("theta Beta parameters must all be > 0")
    y_aligned = np.asarray(y_aligned, dtype="int64")
    y_nonaligned = np.asarray(y_nonaligned, dtype="int64")
    if int(y_aligned.sum()) != int(k_cc):
        raise ValueError(f"y_aligned sums to {int(y_aligned.sum())}, not k_cc={k_cc}")
    if int(y_aligned.sum() + y_nonaligned.sum()) != int(n_rows):
        raise ValueError("aligned + non-aligned counts do not sum to n_rows")
    n_bins = int(y_aligned.size)
    if tier_basis is not None:
        assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        alpha = pm.Beta("alpha", 1.0, 1.0)

        # ---- p_conv: per-arm parameterisation (signoff §2) ----
        if pconv_mode in ("tiers3", "library"):
            n_tiers = int(tier_basis.shape[0])
            tier_weights = pm.Dirichlet("tier_weights", a=np.ones(n_tiers, dtype=float))
            p_conv = pm.Deterministic("p_conv", pt.dot(tier_weights, tier_basis))
        else:
            # Free non-centred GRW, mirroring the p_gen block with its own scale.
            sigma_conv = pm.HalfNormal("sigma_conv", sigma=1.0)
            z_pconv = pm.Normal("z_pconv", mu=0.0, sigma=1.0, shape=n_bins - 1)
            log_pconv_increments = pm.Deterministic(
                "log_pconv_increments", sigma_conv * z_pconv
            )
            log_pconv_raw = pt.concatenate([pt.zeros((1,)), pt.cumsum(log_pconv_increments)])
            log_pconv_centered = log_pconv_raw - pt.max(log_pconv_raw)
            unnorm_conv = pt.exp(log_pconv_centered)
            p_conv = pm.Deterministic("p_conv", unnorm_conv / pt.sum(unnorm_conv))

        # ---- p_gen block: VERBATIM from build_model_joint ----
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
        z_pgen = pm.Normal("z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1)
        log_pgen_increments = pm.Deterministic("log_pgen_increments", sigma_smooth * z_pgen)
        log_pgen_raw = pt.concatenate([pt.zeros((1,)), pt.cumsum(log_pgen_increments)])
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))

        # ---- θ priors: verbatim from build_model_joint ----
        theta_conv = pm.Beta("theta_conv", a_conv, b_conv)
        theta_gen = pm.Beta("theta_gen", a_gen, b_gen)

        # ---- alignment-conditional mixtures (each a proper simplex: the     ----
        # ---- numerators sum exactly to w_a and 1−w_a respectively).          ----
        w_a = pm.Deterministic("pi_align", alpha * theta_conv + (1.0 - alpha) * theta_gen)
        num_al = alpha * theta_conv * p_conv + (1.0 - alpha) * theta_gen * p_gen
        num_non = (alpha * (1.0 - theta_conv) * p_conv
                   + (1.0 - alpha) * (1.0 - theta_gen) * p_gen)
        p_aligned = pm.Deterministic("p_aligned", num_al / w_a)
        p_nonalign = pm.Deterministic("p_nonalign", num_non / (1.0 - w_a))

        # ---- observed data: all three mutable for build-once + set_data ----
        k_data = pm.Data("k_data", np.asarray(int(k_cc), dtype="int64"))
        y_al_data = pm.Data("y_al_data", y_aligned)
        y_non_data = pm.Data("y_non_data", y_nonaligned)
        pm.Binomial("k_obs", n=int(n_rows), p=w_a, observed=k_data)
        pm.Multinomial("y_al_obs", n=k_data, p=p_aligned, observed=y_al_data)
        pm.Multinomial("y_non_obs", n=int(n_rows) - k_data, p=p_nonalign,
                       observed=y_non_data)

    return model
