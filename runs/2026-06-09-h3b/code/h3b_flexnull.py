#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h3b_flexnull.py — flexible-null robustness annex engine (part a).
=================================================================

Implements part (a) of the H3b flexible-null robustness annex
(``h3b-flexible-null-annex-spec-2026-06-15.md``; D2's deferred work). The base
draw-wise run accepted the global Timpson-test saturation and made the
probe-window P(deficit) the deliverable. This annex asks whether a more-flexible
smooth null and/or a de-powered significance criterion de-saturate the GLOBAL
test — and, crucially, whether de-saturation only comes by absorbing the
Antonine/Crisis events the test is meant to detect.

Design (Shawn-confirmed 2026-06-15):

* **Flexibility lever** (broad-shape misfit, M1): three smooth-null families fit
  to the posterior-median corrected count SPA (self-referential null, base D1),
  all on one **effective-degrees-of-freedom (edf)** axis —
    - ``cpl``    : CPL knot-sweep k ∈ {2,3,5,7}, edf = 2k+1 (reuses
                   ``primitives.fit_null_cpl`` unchanged; k=3 is the base-run anchor);
    - ``spline`` : Poisson penalised B-spline (Eilers–Marx), edf-targeted via a
                   second-difference penalty;
    - ``gp``     : Gaussian-process (kernel-ridge on log-counts), edf-targeted via
                   the RBF length-scale.
* **Effective-N / reduced-significance lever** (large-N jaggedness, M2):
    - effective-N thinning ladder on the fixed CPL-3 null;
    - a de-powered **simultaneous-coverage** global statistic (max studentised
      deviation; a sup-type global envelope in the spirit of Myllymäki et al. 2017).

Every smooth null produces a *fitted mean*; that mean is fed through the SAME
Poisson Monte-Carlo envelope as the base run (``primitives.sample_null_spa``), so
the three families are directly comparable and the k=3 CPL point reproduces the
base run bit-for-bit (enforced by the driver's regression guard). All
draw-evaluation, probe-window, aggregation, and coverage-inflation helpers are
reused unchanged from ``h3b_drawwise``.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-15.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.interpolate import BSpline

import h3b_drawwise as E  # noqa: E402  (sets up sys.path for primitives etc.)

P = E.P  # the H1 primitives module (fit_null_cpl, sample_null_spa, ...)

# Reused constants (single source of truth = the base engine).
BIN_CENTRES: np.ndarray = E.BIN_CENTRES
N_BINS: int = E.N_BINS
ALPHA: float = E.ALPHA
VARIANCE_FLOOR: float = E.VARIANCE_FLOOR
N_MC: int = E.N_MC
MASTER_SEED: int = E.MASTER_SEED

# Disjoint per-family seed offsets. ``cpl`` reuses the base run's offset (100000)
# so that the k=3 envelope MC stream is bit-identical to the base run.
SEED_OFFSET = {"cpl": 100_000, "spline": 200_000, "gp": 300_000, "thin": 400_000}

# Flexibility ladders.
CPL_KS = [2, 3, 5, 7]              # edf = 2k+1 → {5, 7, 11, 15}
SMOOTH_TARGET_EDF = [5.0, 10.0, 20.0]   # spline + gp traced on a matched edf ladder

# Effective-N thinning ladder (capped per unit at its actual n_eff).
THIN_NPRIME = [1500, 3000, 6000, 12000, 25000]


# ===========================================================================
# Poisson MC envelope from an arbitrary fitted mean (the single mechanism)
# ===========================================================================
def build_envelope_from_mean(fitted: np.ndarray, n_eff: int,
                             rng: np.random.Generator, n_mc: int = N_MC,
                             return_mc: bool = False) -> dict[str, Any]:
    """Build the pointwise Timpson envelope from a fitted mean SPA.

    Reproduces the cpl branch of ``h3b_drawwise.build_envelope`` exactly — it
    reuses ``primitives.sample_null_spa`` for each replicate, so given the same
    ``fitted`` and ``rng`` the envelope is bit-identical to the base run. Returns
    the per-bin lo/hi/mid, the kept-bin mask, the per-replicate out-of-envelope
    counts (``mc_out``), the per-bin sd, and (optionally) the raw MC matrix for
    the simultaneous-band statistic.
    """
    fitted = np.asarray(fitted, dtype=float)
    params_like = {"fitted": fitted}
    mc = np.empty((n_mc, N_BINS), dtype=float)
    for i in range(n_mc):
        mc[i] = P.sample_null_spa(params_like, "cpl", BIN_CENTRES, rng)
    lo = np.quantile(mc, ALPHA / 2.0, axis=0)
    hi = np.quantile(mc, 1.0 - ALPHA / 2.0, axis=0)
    keep = mc.var(axis=0) >= VARIANCE_FLOOR
    mid = np.median(mc, axis=0)
    mc_out = (((mc < lo) | (mc > hi)) & keep[None, :]).sum(axis=1)
    env: dict[str, Any] = {
        "lo": lo, "hi": hi, "keep": keep, "mid": mid, "mc_out": mc_out,
        "sd": mc.std(axis=0), "n_eff": int(n_eff),
        "n_bins_skipped": int((~keep).sum()),
    }
    if return_mc:
        env["mc"] = mc
    return env


# ===========================================================================
# Smooth-null families (each returns a fitted mean + its effective df)
# ===========================================================================
def fit_mean_cpl(m: np.ndarray, k: int, n_restarts: int | None = None,
                 seed: int = 0) -> dict[str, Any]:
    """CPL-k fit to the corrected count SPA ``m`` (reuses ``fit_null_cpl``).

    k=3 with ``n_restarts=4, seed=0`` reproduces the base run's CPL null exactly;
    k≥5 uses more restarts (15 free params at k=7 needs them).
    """
    if n_restarts is None:
        n_restarts = 4 if k <= 3 else 12
    params = P.fit_null_cpl(np.asarray(m, dtype=float), BIN_CENTRES, k=k,
                            n_restarts=n_restarts, seed=seed)
    return {
        "fitted": np.asarray(params["fitted"], dtype=float),
        "edf": float(2 * k + 1), "family": "cpl", "k": int(k),
        "aic": float(params.get("aic", float("nan"))),
        "rms": float(params.get("residual_rms", float("nan"))),
        "converged": bool(params.get("converged", False)),
    }


def _bspline_basis(x: np.ndarray, n_interior: int, degree: int = 3) -> np.ndarray:
    """Cubic B-spline design matrix with boundary knots placed just outside the
    data range (so every centre has full support). Shape ``(len(x), n_basis)``,
    ``n_basis = n_interior + degree + 1``."""
    x = np.asarray(x, dtype=float)
    lo, hi = float(x.min()), float(x.max())
    span = hi - lo
    interior = np.linspace(lo, hi, n_interior + 2)[1:-1]
    t = np.concatenate([np.full(degree + 1, lo - 1e-6 * span),
                        interior,
                        np.full(degree + 1, hi + 1e-6 * span)])
    return BSpline.design_matrix(x, t, degree).toarray()


def _diff_penalty(n_basis: int, order: int = 2) -> np.ndarray:
    """Second-order difference penalty matrix ``Dᵀ D`` (Eilers–Marx P-spline)."""
    d = np.eye(n_basis)
    for _ in range(order):
        d = np.diff(d, axis=0)
    return d.T @ d


def _fit_poisson_pspline(y: np.ndarray, basis: np.ndarray, pen: np.ndarray,
                         lam: float, n_iter: int = 100, tol: float = 1e-8
                         ) -> tuple[np.ndarray, float]:
    """Penalised Poisson IRLS (log link). Returns (fitted mean, effective df).

    edf = trace[(BᵀWB + λP)⁻¹ BᵀWB] at the converged weights.
    """
    n_basis = basis.shape[1]
    beta = np.full(n_basis, np.log(max(float(np.mean(y)), 1e-3)))
    ridge = 1e-6 * np.eye(n_basis)
    for _ in range(n_iter):
        eta = np.clip(basis @ beta, -30.0, 30.0)
        mu = np.exp(eta)
        w = np.clip(mu, 1e-6, None)              # floored Poisson IRLS weights
        z = eta + (y - mu) / w                   # working response (same W)
        btw = basis.T * w                        # Bᵀ W
        lhs = btw @ basis + lam * pen + ridge
        rhs = btw @ z
        # lstsq (not solve): degenerate units (e.g. Pompeii post-AD-79, a near-all-
        # zero curve) collapse the weighted normal matrix; lstsq stays finite. For
        # well-conditioned units (all-positive counts) this equals solve.
        beta_new = np.linalg.lstsq(lhs, rhs, rcond=None)[0]
        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            break
        beta = beta_new
    mu = np.exp(np.clip(basis @ beta, -30.0, 30.0))
    w = np.clip(mu, 1e-6, None)
    btwb = (basis.T * w) @ basis
    hat = np.linalg.lstsq(btwb + lam * pen + ridge, btwb, rcond=None)[0]
    return mu, float(np.trace(hat))


def fit_mean_spline(m: np.ndarray, target_edf: float, n_interior: int = 18
                    ) -> dict[str, Any]:
    """Poisson P-spline fit to ``m``, smoothing parameter bisected to ``target_edf``.

    edf decreases monotonically in λ, so we bisect log10(λ) on the edf residual.
    Reports the *actual* attained edf (the flexibility axis), not the target.
    """
    y = np.asarray(m, dtype=float)
    basis = _bspline_basis(BIN_CENTRES, n_interior)
    pen = _diff_penalty(basis.shape[1], order=2)
    lo_l, hi_l = -8.0, 10.0          # log10(λ) search bracket
    edf = float("nan")
    mu = np.full_like(y, float(np.mean(y)))
    for _ in range(45):
        mid = 0.5 * (lo_l + hi_l)
        mu, edf = _fit_poisson_pspline(y, basis, pen, 10.0 ** mid)
        if edf > target_edf:         # too flexible → more penalty
            lo_l = mid
        else:
            hi_l = mid
    return {"fitted": mu, "edf": float(edf), "family": "spline",
            "target_edf": float(target_edf), "log10_lambda": float(0.5 * (lo_l + hi_l)),
            "n_basis": int(basis.shape[1]), "converged": bool(np.isfinite(edf))}


def _rbf(x: np.ndarray, ell: float) -> np.ndarray:
    d = (x[:, None] - x[None, :]) / ell
    return np.exp(-0.5 * d * d)


def fit_mean_gp(m: np.ndarray, target_edf: float, noise_frac: float = 0.05
                ) -> dict[str, Any]:
    """Gaussian-process (kernel-ridge on log-counts) fit to ``m``, RBF length-scale
    bisected to ``target_edf``.

    Smoother matrix S = K (K + σ²I)⁻¹ on the centred log-counts; edf = trace(S),
    which decreases monotonically in the length-scale ℓ. σ² is a fixed fraction of
    the log-count variance. Mean = exp(centred GP fit), clipped to a sane range.
    """
    x = np.asarray(BIN_CENTRES, dtype=float)
    y = np.log(np.asarray(m, dtype=float) + 0.5)
    ybar = float(np.mean(y))
    yc = y - ybar
    sigma2 = max(noise_frac * float(np.var(yc)), 1e-8)
    eye = np.eye(len(x))

    def edf_smoother(ell: float) -> tuple[float, np.ndarray]:
        k = _rbf(x, ell)
        smoother = k @ np.linalg.solve(k + sigma2 * eye, eye)
        return float(np.trace(smoother)), smoother

    lo_l, hi_l = np.log10(3.0), np.log10(3000.0)   # log10(ℓ) bracket
    edf = float("nan")
    smoother = eye
    for _ in range(45):
        mid = 0.5 * (lo_l + hi_l)
        edf, smoother = edf_smoother(10.0 ** mid)
        if edf > target_edf:          # too wiggly → larger length-scale
            lo_l = mid
        else:
            hi_l = mid
    ell = 10.0 ** (0.5 * (lo_l + hi_l))
    edf, smoother = edf_smoother(ell)
    fitted_log = np.clip(ybar + smoother @ yc,
                         np.log(0.5), np.log(max(float(np.sum(m)), 1.0)))
    return {"fitted": np.exp(fitted_log), "edf": float(edf), "family": "gp",
            "target_edf": float(target_edf), "length_scale": float(ell),
            "converged": bool(np.isfinite(edf))}


# ===========================================================================
# De-powered (simultaneous-coverage) global statistic — max studentised dev
# ===========================================================================
def simultaneous_eval(draws_counts: np.ndarray, env: dict) -> dict[str, float]:
    """Draw-wise simultaneous-band (sup-type) global *p*.

    For each MC replicate and each posterior draw, compute the max over kept bins
    of the studentised absolute deviation from the null centre,
    ``d = max_i |x_i − mid_i| / sd_i``. The per-draw global *p* is the add-one
    fraction of MC replicates with ``d_mc ≥ d_obs``; the marginal is the mean over
    draws. Controls the family-wise (simultaneous) out-of-envelope rate across the
    80 bins, de-powering the pointwise 'any-bin-out' statistic. Requires
    ``env['mc']`` (build the envelope with ``return_mc=True``).
    """
    mc = env["mc"]
    keep = env["keep"]
    sd = env["sd"]
    mid = env["mid"]
    mask = keep & (sd > 0)
    if not mask.any():
        return {"marginal_p_sim": float("nan"), "p_sim_deviation": float("nan")}
    sdm = sd[mask]
    midm = mid[mask]
    d_mc = np.max(np.abs(mc[:, mask] - midm) / sdm, axis=1)          # (M,)
    d_obs = np.max(np.abs(draws_counts[:, mask] - midm) / sdm, axis=1)  # (D,)
    n_mc = d_mc.size
    order = np.sort(d_mc)
    ge = n_mc - np.searchsorted(order, d_obs, side="left")           # #{d_mc ≥ d_obs}
    p_d = (1.0 + ge) / (1.0 + n_mc)
    return {"marginal_p_sim": float(np.mean(p_d)),
            "p_sim_deviation": float(np.mean(p_d < ALPHA))}
