#!/usr/bin/env python3
"""
primitives.py --- Reusable primitives for the H1 min-thresholds simulation.

Implements the low-level building blocks consumed by ``h1_sim.py``:

    load_filtered_lire           --- filter + load LIRE v3.0
    aoristic_resample            --- Uniform aoristic resampling (direct numpy)
    fit_null_exponential         --- fit exponential null SPA model
    fit_null_cpl                 --- fit CPL (continuous piecewise linear) null SPA
    sample_null_spa              --- one Monte Carlo replicate under a fitted null
    inject_effect                --- inject step / Gaussian effect on an SPA
    permutation_envelope_test    --- hand-rolled Timpson et al. 2014 envelope test

Design anchors:
  - Decision 7 (decisions.md): `tempun` removed; Uniform aoristic reimplemented
    directly (attribution to Kaše, Heřmánková & Sobotková 2023; Uniform
    aoristic method per Ratcliffe 2002, Crema 2012).
  - Decision 1: hand-rolled Timpson 2014 MC envelope; NOT
    ``scipy.stats.permutation_test`` (which is the wrong API for within-SPA
    deviation detection against a parametric null).
  - Decision 8: schema-compatible return structures suitable for persistence.
  - Decision 3: CPL fit is called separately per k (k=2, 3, 4); this module
    does not pick "best" k --- that is a driver concern.

Seed discipline: every stochastic function takes an explicit
``np.random.Generator`` argument. No implicit global RNG; no
``np.random.seed`` calls.

References:
  - Timpson, A. et al. 2014. "Reconstructing regional population fluctuations
    in the European Neolithic using radiocarbon dates". J. Archaeol. Sci. 52.
  - Ratcliffe, J. H. 2002. "Aoristic signatures and the spatio-temporal
    analysis of high volume crime data". J. Quant. Criminol. 18(1).
  - Crema, E. R. 2012. "Modelling temporal uncertainty in archaeological
    analysis". J. Archaeol. Method Theory 19(3).
  - Kaše, V., Heřmánková, P., Sobotková, A. 2023. LIRE v3.0. Zenodo
    DOI 10.5281/zenodo.8147298. Dataset.

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from scipy import optimize, stats

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants --- envelope and binning
# ---------------------------------------------------------------------------

# 50 BC -- AD 350 inclusive, 5-year bins --> 80 bins.
BIN_EDGES: np.ndarray = np.arange(-50, 350 + 1, 5, dtype=float)
BIN_CENTRES: np.ndarray = 0.5 * (BIN_EDGES[:-1] + BIN_EDGES[1:])
BIN_WIDTH: float = 5.0
N_BINS: int = len(BIN_CENTRES)

# Sanity check at import time: 80 bins.
assert N_BINS == 80, f"Expected 80 bins, got {N_BINS}"


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_filtered_lire(
    path: str | Path,
    min_rows: int = 50_000,
) -> pd.DataFrame:
    """Load LIRE v3.0 and apply the preregistered row filter.

    The preregistration (§3 of ``planning/preregistration-draft.md``) specifies
    filtering to ``is_within_RE == True``, ``is_geotemporal == True`` and
    50 BC -- AD 350 date-interval intersect. The archived LIRE v3.0 parquet
    does not ship these two flag columns (see ``runs/2026-04-23-descriptive-
    stats/decisions.md``), so we derive them conservatively:

        is_geotemporal := ``Latitude`` and ``Longitude`` non-null AND
                          ``not_before`` and ``not_after`` non-null AND
                          ``not_before <= not_after``.
        is_within_RE   := ``province`` non-null and non-empty (provinces are
                          the canonical Roman-Empire geographic grouping in
                          LIRE).

    The date-interval intersect is ``not_before <= 350 AND not_after >= -50``.

    Parameters
    ----------
    path : str | Path
        Path to ``LIRE_v3-0.parquet``.
    min_rows : int, default 50_000
        Assertion floor. The prereg brief notes "if filtered LIRE has < 50,000
        rows, use the actual filtered count and log"; we assert that the
        filtered dataframe is at least this size to catch catastrophic
        loader regressions. Lower if a smaller test fixture is in use.

    Returns
    -------
    pandas.DataFrame
        Columns retained: ``not_before``, ``not_after``, ``province``,
        ``urban_context_city``, ``Latitude``, ``Longitude``. Indexed
        by the integer position in the filtered frame (0 ..).

    Raises
    ------
    AssertionError
        If filtered row count is below ``min_rows`` --- indicates a loader
        regression rather than legitimate data sparseness.
    """
    path = Path(path)
    df = pd.read_parquet(path)

    has_coords = df["Latitude"].notna() & df["Longitude"].notna()
    has_dates = df["not_before"].notna() & df["not_after"].notna()
    valid_order = df["not_before"] <= df["not_after"]
    has_province = df["province"].notna() & (df["province"] != "")

    is_geotemporal = has_coords & has_dates & valid_order
    is_within_re = has_province
    intersects = (df["not_before"] <= 350) & (df["not_after"] >= -50)

    mask = is_geotemporal & is_within_re & intersects
    filtered = df.loc[mask, [
        "not_before", "not_after", "province",
        "urban_context_city", "Latitude", "Longitude",
    ]].reset_index(drop=True).copy()

    n = len(filtered)
    logger.info("Filtered LIRE: %d rows (from %d)", n, len(df))
    assert n >= min_rows, (
        f"Filtered LIRE has {n} rows, below floor {min_rows}. "
        "Likely loader regression; check filter columns."
    )
    return filtered


# ---------------------------------------------------------------------------
# Aoristic resampling (Uniform method)
# ---------------------------------------------------------------------------

def aoristic_resample(
    df: pd.DataFrame,
    n: int,
    bin_edges: np.ndarray,
    rng: np.random.Generator,
    replace: bool = True,
) -> np.ndarray:
    """Build a summed probability analysis (SPA) via Uniform aoristic resampling.

    The Uniform aoristic approach (Ratcliffe 2002; Crema 2012; Kaše et al.
    2023) assigns each inscription a single randomly-drawn year within its
    ``[not_before, not_after]`` interval, then bins the draws. Summed across
    many Monte Carlo iterations this approximates uniform probability mass
    on the interval. For power simulation we use a single realisation per
    SPA build (i.e. *one* uniform draw per inscription), matching Shawn's
    2024 practice.

    This reimplements ``tempun.spa_uniform`` directly to avoid the numpy-2
    incompatibility in ``tempun`` 0.2.4 (Decision 7 of decisions.md).

    Parameters
    ----------
    df : pandas.DataFrame
        Filtered LIRE frame, must contain ``not_before`` and ``not_after``.
    n : int
        Number of rows to draw.
    bin_edges : numpy.ndarray
        Ascending 1-D array of bin edges; returned SPA has length
        ``len(bin_edges) - 1``.
    rng : numpy.random.Generator
        Seeded generator --- no implicit state.
    replace : bool, default True
        Sampling-with-replacement (bootstrap) per Decision 4.

    Returns
    -------
    numpy.ndarray
        SPA vector of integer counts (length ``len(bin_edges) - 1``).
    """
    if n <= 0:
        raise ValueError(f"n must be positive; got {n}")

    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)
    n_rows = len(nb)
    if n_rows == 0:
        raise ValueError("df is empty")

    # Draw row indices (bootstrap).
    idx = rng.integers(0, n_rows, size=n) if replace else rng.choice(
        n_rows, size=n, replace=False,
    )

    lo = nb[idx]
    hi = na[idx]
    # Uniform draw per row. If lo == hi, sample is degenerate (point date) ---
    # numpy's ``uniform`` returns ``lo`` in that case, which is correct.
    years = rng.uniform(lo, hi)

    spa, _ = np.histogram(years, bins=bin_edges)
    return spa.astype(float)


# ---------------------------------------------------------------------------
# Null-model fits
# ---------------------------------------------------------------------------

def fit_null_exponential(spa: np.ndarray, bin_centres: np.ndarray) -> dict:
    """Fit an exponential null model ``log(mean_spa) ~ a + b * t``.

    Fits via ordinary least squares on ``log(spa + 1)`` against ``bin_centres``.
    The +1 offset is the standard zero-count handling for log-linear SPA
    fits and matches Timpson et al. 2014.

    Parameters
    ----------
    spa : numpy.ndarray
        Observed SPA (integer counts).
    bin_centres : numpy.ndarray
        Bin centre-year values.

    Returns
    -------
    dict
        ``{"rate": b, "intercept": a, "residual_rms": rms,
           "fitted": predicted SPA, "model": "exponential"}``.
    """
    if spa.shape != bin_centres.shape:
        raise ValueError("spa and bin_centres must match shape")
    log_y = np.log(spa + 1.0)
    slope, intercept, _, _, _ = stats.linregress(bin_centres, log_y)
    fitted = np.exp(intercept + slope * bin_centres) - 1.0
    # Numerical guard: log-linear back-transform can produce small negatives.
    fitted = np.clip(fitted, 0.0, None)
    residual = spa - fitted
    rms = float(np.sqrt(np.mean(residual ** 2)))
    return {
        "rate": float(slope),
        "intercept": float(intercept),
        "residual_rms": rms,
        "fitted": fitted,
        "model": "exponential",
    }


def _cpl_predict(params: np.ndarray, k: int, t: np.ndarray) -> np.ndarray:
    """Evaluate a continuous-piecewise-linear (CPL) curve on ``t``.

    Parameterisation: ``params`` packs ``k`` interior-knot x-positions in
    the unit interval (transformed via cumulative softmax for monotonicity),
    then ``k + 1`` log-heights at the knots (endpoints + interior). The
    curve is linear between consecutive knots. k=2 means two *interior*
    knots --> three segments.

    Parameters
    ----------
    params : numpy.ndarray
        Flat parameter vector of length ``2 * k + 1``.
    k : int
        Interior-knot count (2, 3 or 4 for our study).
    t : numpy.ndarray
        Evaluation times (bin centres).

    Returns
    -------
    numpy.ndarray
        Predicted SPA (non-negative, same shape as ``t``).
    """
    # Knot x-positions via softmax-normalised cumulative increments.
    raw_x = params[:k]
    # Use softmax over k+1 gaps (k interior knots -> k+1 gaps summing to 1).
    # Construct gaps from raw_x via exp-normalise then cumsum.
    gaps = np.exp(np.concatenate([raw_x, [0.0]]))
    gaps = gaps / gaps.sum()
    cum = np.cumsum(gaps)[:-1]  # length k, interior positions in (0, 1)
    t_lo, t_hi = t.min(), t.max()
    interior = t_lo + cum * (t_hi - t_lo)

    # Log-heights at knots: endpoints + interior --> k + 2 heights?
    # Simpler parameterisation: heights at t_lo, each interior, t_hi.
    # That is k + 2 heights. We packed k + 1 heights --- so use heights at
    # t_lo and each interior, and derive t_hi's height as same as last.
    # Cleaner: repack --- heights at all k + 2 breakpoints.
    log_h = params[k:]  # length k + 1
    xs = np.concatenate([[t_lo], interior, [t_hi]])
    # log_h has k + 1 values; xs has k + 2 knots. Pad by repeating last.
    log_heights = np.concatenate([log_h, [log_h[-1]]])
    # Linear interpolation in log-space, exp back.
    log_pred = np.interp(t, xs, log_heights)
    pred = np.exp(log_pred)
    return pred


def _cpl_neg_log_likelihood(
    params: np.ndarray, k: int, t: np.ndarray, y: np.ndarray,
) -> float:
    """Poisson negative log-likelihood for CPL model."""
    mu = _cpl_predict(params, k, t)
    mu = np.clip(mu, 1e-6, None)
    # Poisson NLL (dropping y! term, constant in params).
    nll = np.sum(mu - y * np.log(mu))
    if not np.isfinite(nll):
        return 1e20
    return float(nll)


def fit_null_cpl(
    spa: np.ndarray,
    bin_centres: np.ndarray,
    k: int,
    n_restarts: int = 4,
    seed: int = 0,
) -> dict:
    """Fit a CPL (continuous piecewise linear) null SPA model with k knots.

    Uses ``scipy.optimize.minimize`` (L-BFGS-B) on the Poisson negative
    log-likelihood. Multiple random restarts guard against local minima.
    AIC uses Poisson log-likelihood and the full free-parameter count
    (``2 * k + 1`` parameters: ``k`` interior-knot positions + ``k + 1``
    log-heights).

    Parameters
    ----------
    spa : numpy.ndarray
        Observed SPA (integer counts).
    bin_centres : numpy.ndarray
        Bin centre-year values.
    k : int
        Interior-knot count (2, 3 or 4).
    n_restarts : int, default 4
        Random restarts to reduce local-minimum risk.
    seed : int, default 0
        Seed for restart draws (deterministic given fixed seed).

    Returns
    -------
    dict
        Keys: ``"knots"`` (x-positions of interior knots, years),
        ``"log_heights"`` (length ``k + 1``), ``"aic"``, ``"residual_rms"``,
        ``"converged"``, ``"fitted"`` (predicted SPA), ``"k"``, ``"model"``.
    """
    if spa.shape != bin_centres.shape:
        raise ValueError("spa and bin_centres must match shape")
    n_params = 2 * k + 1
    local_rng = np.random.default_rng(seed)
    best = None
    best_nll = np.inf
    for _ in range(n_restarts):
        x0 = local_rng.normal(0.0, 0.5, size=n_params)
        # Seed log-heights from log(mean count).
        mean_log = np.log(max(spa.mean(), 1e-3))
        x0[k:] = mean_log + local_rng.normal(0.0, 0.3, size=k + 1)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = optimize.minimize(
                    _cpl_neg_log_likelihood,
                    x0,
                    args=(k, bin_centres, spa),
                    method="L-BFGS-B",
                    options={"maxiter": 500, "gtol": 1e-5},
                )
        except (RuntimeError, ValueError):
            continue
        if result.fun < best_nll and np.isfinite(result.fun):
            best_nll = float(result.fun)
            best = result

    if best is None or not np.isfinite(best_nll):
        # Complete fit failure --- caller handles via fallback logic.
        return {
            "knots": np.array([]),
            "log_heights": np.array([]),
            "aic": float("nan"),
            "residual_rms": float("nan"),
            "converged": False,
            "fitted": np.full_like(spa, fill_value=float("nan"), dtype=float),
            "k": k,
            "model": "cpl",
        }

    fitted = _cpl_predict(best.x, k, bin_centres)
    residual = spa - fitted
    rms = float(np.sqrt(np.mean(residual ** 2)))
    # AIC = 2 * n_params + 2 * NLL (Poisson log-likelihood form; constant y!
    # term cancels in model comparison so we omit it).
    aic = 2.0 * n_params + 2.0 * best_nll

    # Recover interior-knot x-positions for reporting.
    raw_x = best.x[:k]
    gaps = np.exp(np.concatenate([raw_x, [0.0]]))
    gaps = gaps / gaps.sum()
    cum = np.cumsum(gaps)[:-1]
    t_lo, t_hi = bin_centres.min(), bin_centres.max()
    knots = t_lo + cum * (t_hi - t_lo)

    return {
        "knots": knots,
        "log_heights": best.x[k:].copy(),
        "aic": float(aic),
        "residual_rms": rms,
        "converged": bool(best.success),
        "fitted": fitted,
        "k": k,
        "model": "cpl",
        "_raw_params": best.x.copy(),
    }


# ---------------------------------------------------------------------------
# Null SPA sampler (MC replicate)
# ---------------------------------------------------------------------------

def sample_null_spa(
    null_params: dict,
    model: Literal["exponential", "cpl"],
    bin_centres: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Produce one Monte Carlo replicate SPA under a fitted null.

    Poisson noise is added on top of the fitted mean: ``MC_spa[i] ~
    Poisson(max(fitted[i], 0))``. Matches the generative assumption of
    the Timpson et al. 2014 envelope procedure.

    Parameters
    ----------
    null_params : dict
        Fit result from ``fit_null_exponential`` or ``fit_null_cpl``.
    model : {'exponential', 'cpl'}
        Null family.
    bin_centres : numpy.ndarray
        Bin centre-year values.
    rng : numpy.random.Generator
        Seeded generator.

    Returns
    -------
    numpy.ndarray
        MC replicate SPA (non-negative integer counts as float array).
    """
    fitted = null_params["fitted"]
    if fitted.shape != bin_centres.shape:
        raise ValueError("fitted mean must match bin_centres shape")
    mu = np.clip(fitted, 0.0, None)
    # Poisson draw; tolerate NaN fitted (from failed fit) by returning zeros.
    if not np.all(np.isfinite(mu)):
        return np.zeros_like(mu)
    return rng.poisson(mu).astype(float)


# ---------------------------------------------------------------------------
# Effect injection
# ---------------------------------------------------------------------------

def _gaussian_kernel(
    t: np.ndarray, centre: float, fwhm: float,
) -> np.ndarray:
    """Gaussian kernel normalised to peak = 1 at ``t == centre``."""
    sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))  # FWHM -> sigma
    return np.exp(-0.5 * ((t - centre) / sigma) ** 2)


def _step_kernel(
    t: np.ndarray, centre: float, duration: float,
) -> np.ndarray:
    """Box-car kernel (value 1 within window, else 0)."""
    half = 0.5 * duration
    return ((t >= centre - half) & (t < centre + half)).astype(float)


def inject_effect(
    spa: np.ndarray,
    bin_centres: np.ndarray,
    magnitude: float,
    centre_year: float,
    duration: float,
    shape: Literal["step", "gaussian"],
) -> np.ndarray:
    """Inject a multiplicative effect into an SPA.

    Effect form: ``spa_out = spa * (1 + magnitude * kernel(t))`` where
    ``kernel`` is a box-car (``shape='step'``) or normalised Gaussian
    (``shape='gaussian'``) peaking at ``centre_year``.

    Sign convention (decisions.md summary table + Decision 2):
      - ``magnitude < 0`` --> dip (e.g. ``a_50pc_50y`` has magnitude = -0.5).
      - ``magnitude > 0`` --> peak (e.g. ``b_double_25y`` has magnitude = +1.0
        for doubling, i.e. ``2 *`` baseline at peak).
      - ``magnitude = 0`` --> identity transform (zero bracket).

    For Gaussian shape: nadir (or peak) sits at ``centre_year``; FWHM equals
    ``duration`` (decisions.md §3.2 footnote). For step shape: the kernel is
    a box-car of width ``duration`` centred at ``centre_year``.

    Parameters
    ----------
    spa : numpy.ndarray
        Baseline SPA.
    bin_centres : numpy.ndarray
        Bin centre-year values.
    magnitude : float
        Effect magnitude (signed, per bracket convention).
    centre_year : float
        Effect centre year (typically envelope mid-point, AD 150).
    duration : float
        Effect duration (years). For Gaussian, equals FWHM; for step,
        equals box-car width.
    shape : {'step', 'gaussian'}
        Effect shape.

    Returns
    -------
    numpy.ndarray
        Modified SPA (same shape as ``spa``).
    """
    if shape == "step":
        kernel = _step_kernel(bin_centres, centre_year, duration)
    elif shape == "gaussian":
        kernel = _gaussian_kernel(bin_centres, centre_year, duration)
    else:
        raise ValueError(f"Unknown shape: {shape!r}")
    modifier = 1.0 + magnitude * kernel
    # Clamp to non-negative (guards magnitude < -1 on step shape, shouldn't
    # arise for our brackets but defensive).
    modifier = np.clip(modifier, 0.0, None)
    return spa * modifier


# ---------------------------------------------------------------------------
# Permutation-envelope test (Timpson 2014)
# ---------------------------------------------------------------------------

def permutation_envelope_test(
    observed_spa: np.ndarray,
    null_params: dict,
    model: Literal["exponential", "cpl"],
    bin_centres: np.ndarray,
    n_mc: int,
    rng: np.random.Generator,
    alpha: float = 0.05,
    variance_floor: float = 1e-10,
) -> dict:
    """Hand-rolled Timpson et al. 2014 Monte Carlo envelope test.

    Procedure:
      1. Draw ``n_mc`` MC replicate SPAs under the fitted null.
      2. Build pointwise lower / upper envelopes at the (alpha/2, 1 - alpha/2)
         quantiles per bin.
      3. For each MC replicate, count how many of its own bins lie outside
         the pointwise envelope (this calibrates the global statistic).
      4. Count observed bins outside the envelope.
      5. Global *p*-value = proportion of MC replicates whose out-of-envelope
         count is >= observed's.

    Bins whose null MC variance is below ``variance_floor`` are excluded
    from all counts (numerical guard per risk (d) in plan.md §9).

    Parameters
    ----------
    observed_spa : numpy.ndarray
        Observed (possibly effect-injected) SPA.
    null_params : dict
        Fit result passed to ``sample_null_spa``.
    model : {'exponential', 'cpl'}
        Null family.
    bin_centres : numpy.ndarray
        Bin centre-year values.
    n_mc : int
        Number of Monte Carlo null replicates.
    rng : numpy.random.Generator
        Seeded generator.
    alpha : float, default 0.05
        Pointwise envelope level --- envelope is ``(alpha/2, 1 - alpha/2)``.
    variance_floor : float, default 1e-10
        Skip bins whose MC variance is below this floor.

    Returns
    -------
    dict
        Keys:
          - ``detected`` : bool --- ``pval_global < alpha``.
          - ``pval_global`` : float.
          - ``lo_env``, ``hi_env`` : pointwise envelopes.
          - ``n_bins_outside`` : int --- observed bins outside envelope.
          - ``n_bins_skipped`` : int --- zero-variance bins skipped.
    """
    # Draw MC replicates.
    mc_array = np.empty((n_mc, len(bin_centres)), dtype=float)
    for i in range(n_mc):
        mc_array[i] = sample_null_spa(null_params, model, bin_centres, rng)

    # Pointwise envelope.
    lo_env = np.quantile(mc_array, alpha / 2.0, axis=0)
    hi_env = np.quantile(mc_array, 1.0 - alpha / 2.0, axis=0)

    # Variance mask (keep bins with variance >= floor).
    var = mc_array.var(axis=0)
    keep = var >= variance_floor
    n_bins_skipped = int((~keep).sum())

    # Observed: how many kept bins outside pointwise envelope.
    obs_outside_mask = (observed_spa < lo_env) | (observed_spa > hi_env)
    obs_outside = int((obs_outside_mask & keep).sum())

    # Calibrate: for each MC replicate, count its own bins outside envelope.
    mc_outside_mask = (mc_array < lo_env) | (mc_array > hi_env)
    mc_outside = (mc_outside_mask & keep[np.newaxis, :]).sum(axis=1)

    # Global p-value: proportion of MC replicates with >= obs_outside bins
    # outside. Use >= (conservative).
    pval_global = float(np.mean(mc_outside >= obs_outside))

    return {
        "detected": bool(pval_global < alpha),
        "pval_global": pval_global,
        "lo_env": lo_env,
        "hi_env": hi_env,
        "n_bins_outside": obs_outside,
        "n_bins_skipped": n_bins_skipped,
    }


# ---------------------------------------------------------------------------
# Bracket catalogue --- canonical magnitude + duration + sign convention
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BracketSpec:
    """Canonical definition of an effect-size bracket.

    Sign convention per decisions.md: a and c are dips (negative magnitude);
    b is a peak (positive magnitude, +1.0 for 2x baseline at peak); zero is
    the identity transform used for false-positive calibration.
    """
    name: str
    magnitude: float
    duration: float  # years


BRACKETS: dict[str, BracketSpec] = {
    "a_50pc_50y": BracketSpec("a_50pc_50y", magnitude=-0.5, duration=50.0),
    "b_double_25y": BracketSpec("b_double_25y", magnitude=+1.0, duration=25.0),
    "c_20pc_25y": BracketSpec("c_20pc_25y", magnitude=-0.2, duration=25.0),
    "zero": BracketSpec("zero", magnitude=0.0, duration=50.0),
}
