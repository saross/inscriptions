#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
supp_production_lib.py — pure-analysis read-off helpers for the supplementary wave.
===================================================================================

The H2.1 supplementary-wave production driver
(``runs/2026-06-18-h2.1-supplementary-wave/SPEC.md``) splits into two kinds of work:

  * **MCMC-heavy items** — C5 / C6 model-comparison (Dirichlet-multinomial +
    negative-binomial fits per unit) and H2.3 threshold refits — which live in the
    orchestrator ``run_supp_production.py`` because they import ``pymc`` and fit; and
  * **pure read-off / numerical items** — C11 (trapezoidal apportionment), H2.2
    (corrected-vs-uncorrected boundary-step magnitudes), H2.4 (stratified-by-family
    SPA), C16 (α descriptive read-off), plus the shared bootstrap and Pearson
    helpers — which need NO MCMC and so live HERE, importable and unit-testable
    without a PyMC / ArviZ stack.

Every function reuses the lodged corpus + SPA machinery by IMPORTING it (never
re-implementing): ``h2_lib`` for the corpus loader, the uniform aoristic SPA,
``classify_family`` and the binning grid; ``refit_lib`` for unit enumeration and
per-unit cross-classified data; ``joint_lib`` for the rule-C alignment indicator;
and the lodged trapezoidal apportionment from
``runs/2026-05-17-empirical-spa-shape/code/empirical_spa_shape.py`` (reused, the
original untouched — SPEC C11 reuse note).

This module DOES NOT fit anything, DOES NOT call ``pm.sample``, and DOES NOT touch
SSH. It is safe to import and exercise during the build/audit phase.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

# --------------------------------------------------------------------------- #
# Path wiring. Parameterised root via ``wire_paths``; the default is the        #
# standing checkout (identical on amd-tower and sapphire). The trapezoidal      #
# apportionment lives in the 2026-05-17 empirical-SPA-shape run — imported, not #
# copied (the original is never edited; SPEC C11 reuse note honoured by reuse). #
# --------------------------------------------------------------------------- #
DEFAULT_ROOT = Path("/home/shawn/Code/inscriptions")


def wire_paths(root: Path = DEFAULT_ROOT) -> None:
    """Insert the sibling-run code dirs on ``sys.path`` (idempotent).

    Inserts (in import-priority order) the supplementary-wave code dir, the
    cc-production-refit code dir (``refit_lib``), the H2.1 launch-prep code dir
    (``h2_lib``), the joint-identifiability code dir (``joint_lib``), the
    convention-basis revalidation code dir (``cell_lib``), and the empirical-SPA-
    shape code dir (the lodged trapezoidal apportionment).
    """
    supp = root / "runs" / "2026-06-18-h2.1-supplementary-wave" / "code"
    refit = root / "runs" / "2026-06-13-cc-production-refit" / "code"
    h2 = root / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
    joint = root / "runs" / "2026-06-09-joint-identifiability" / "code"
    cell_lib = (root / "runs" / "2026-06-06-convention-basis-redesign"
                / "revalidation" / "code")
    spa_shape = root / "runs" / "2026-05-17-empirical-spa-shape" / "code"
    for p in (str(supp), str(refit), str(h2), str(joint), str(cell_lib),
              str(spa_shape)):
        if p not in sys.path:
            sys.path.insert(0, p)


# --------------------------------------------------------------------------- #
# Template-boundary bins (H2.2 / SPEC §4): the BC/AD 0, AD 100, 200, 300        #
# century-template boundaries the prereg names (Field 3 l.105). On the          #
# h2_lib grid (ENV_START=-50, BIN_SIZE=5, N_BINS=80) the right-open bin         #
# containing a boundary year Y is index (Y - ENV_START)//BIN_SIZE.              #
# --------------------------------------------------------------------------- #
TEMPLATE_BOUNDARY_YEARS = (0, 100, 200, 300)

# H2.3 date_range filter thresholds (SPEC §4 / C14; prereg Field 3 l.107).
H2_3_THRESHOLDS = (25, 50, 100, 200, 300)

# H2.4 strata (SPEC §4 / C15). ``classify_family`` labels: F1_round, F3_periodic,
# Tight, F2_Other, Big. The genuine-classed strata are the date-honest families
# (Tight + the year-precise rows inside it); the convention-classed strata are the
# template families F1_round + F3_periodic (the round / periodic-width templates).
GENUINE_FAMILIES = ("Tight",)
CONVENTION_FAMILIES = ("F1_round", "F3_periodic")

# Material-divergence rule (SPEC §4): C11 and H2.3 share the r-thresholds.
C11_R_THRESHOLD = 0.95      # trapezoidal "report-alongside" trigger (input + output)
H2_3_R_THRESHOLD = 0.90     # H2.3 threshold-convergence rule


# =========================================================================== #
# Generic numerical helpers (no MCMC, no I/O).                                  #
# =========================================================================== #
def pearson_r(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation of two equal-length vectors, NaN-safe at zero variance.

    Returns ``float('nan')`` if either input has zero variance (a flat vector has
    no linear correlation to report), rather than raising or emitting a warning.
    """
    a = np.asarray(a, dtype=float).reshape(-1)
    b = np.asarray(b, dtype=float).reshape(-1)
    if a.size != b.size:
        raise ValueError(f"length mismatch: {a.size} vs {b.size}")
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def normalise(v: np.ndarray) -> np.ndarray:
    """Normalise a non-negative vector to sum 1 (returns the input if it sums ≤ 0)."""
    v = np.asarray(v, dtype=float)
    s = v.sum()
    return v / s if s > 0 else v


def bootstrap_pearson_ci(
        unit_keys: np.ndarray,
        spa_builder,
        n_boot: int,
        rng: np.random.Generator,
        ci: tuple[float, float] = (2.5, 97.5)) -> dict[str, float]:
    """City/inscription bootstrap CI on a Pearson r between two SPAs (SPEC §4).

    Resamples the underlying rows WITH replacement (a non-parametric inscription
    bootstrap; ``unit_keys`` is the row-index array of the unit's rows), rebuilds
    BOTH SPAs being correlated from the resampled rows via ``spa_builder``, and
    reports the Pearson-r distribution's median + percentile CI. Used for the H2.3
    pairwise-threshold r CIs (SPEC §4: "bootstrap CI").

    Parameters
    ----------
    unit_keys : (N,) int array
        Positional row indices of the unit's rows (resampled with replacement).
    spa_builder : callable(resampled_keys) -> (spa_a, spa_b)
        Returns the two SPAs to be correlated, built from the resampled rows.
    n_boot : int
        Bootstrap replicate count.
    rng : numpy.random.Generator
        Seeded generator.
    ci : (lo_pct, hi_pct)
        Percentile bounds (default the 95 % interval).

    Returns
    -------
    dict with ``r_median``, ``r_ci_lo``, ``r_ci_hi``, ``n_boot``, ``n_valid``
    (replicates with a finite r — a degenerate resample with a flat SPA is dropped).
    """
    unit_keys = np.asarray(unit_keys)
    n = unit_keys.size
    rs: list[float] = []
    for _ in range(n_boot):
        take = rng.integers(0, n, size=n)
        spa_a, spa_b = spa_builder(unit_keys[take])
        r = pearson_r(spa_a, spa_b)
        if np.isfinite(r):
            rs.append(r)
    if not rs:
        return {"r_median": float("nan"), "r_ci_lo": float("nan"),
                "r_ci_hi": float("nan"), "n_boot": n_boot, "n_valid": 0}
    arr = np.asarray(rs)
    lo, hi = (float(x) for x in np.percentile(arr, list(ci)))
    return {"r_median": float(np.median(arr)), "r_ci_lo": lo, "r_ci_hi": hi,
            "n_boot": n_boot, "n_valid": int(arr.size)}


# =========================================================================== #
# C11 — trapezoidal-aoristic apportionment (SPEC §4).                           #
# =========================================================================== #
def trapezoidal_spa_on_h2_grid(nb: np.ndarray, na: np.ndarray, H, T) -> np.ndarray:
    """Trapezoidal-aoristic SPA on the h2_lib grid, reusing the lodged apportionment.

    Calls the lodged ``trapezoidal_aoristic_spa`` from the 2026-05-17 empirical-SPA-
    shape run (imported as ``T``; the original file is never edited — SPEC C11 reuse
    note) on the h2_lib binning grid, so the trapezoidal and uniform SPAs are on
    BYTE-IDENTICAL bin edges and are directly Pearson-comparable.

    Convention reconciliation (flagged for audit): the two lodged SPA builders use
    DIFFERENT continuous-year conventions —

      * ``h2_lib.aoristic_spa`` treats the interval as ``[nb, na]`` with denominator
        ``width = na − nb`` (NOT the inclusive +1), clipped to ``[ENV_START, ENV_END]``;
      * the 2026-05-17 ``uniform_aoristic_spa`` / ``trapezoidal_aoristic_spa`` treat
        the interval as the half-open ``[nb, na+1)`` with denominator ``width =
        na − nb + 1`` (inclusive-Roman), and do NOT clip to the envelope.

    For C11 we need the trapezoidal-vs-uniform contrast on a CONSISTENT footing, so
    we build BOTH legs with the 2026-05-17 module (its ``uniform_aoristic_spa`` and
    ``trapezoidal_aoristic_spa``) on the h2_lib grid — see ``uniform_spa_2026_05_17``.
    Mixing the h2_lib uniform with the 2026-05-17 trapezoid would confound the
    aoristic-shape change (the C11 question) with a width-denominator change (an
    unrelated convention artefact). The input-level r is therefore an apples-to-apples
    trapezoid-vs-uniform comparison under one width convention.

    Parameters
    ----------
    nb, na : int arrays
        Interval endpoints (h2_lib ``nb`` / ``na`` columns).
    H : module
        ``h2_lib`` (for ``BIN_EDGES``).
    T : module
        The lodged ``empirical_spa_shape`` module (for ``trapezoidal_aoristic_spa``).

    Returns
    -------
    spa : (N_BINS,) float array on the h2_lib grid.
    """
    nb = np.asarray(nb)
    na = np.asarray(na)
    width = (na - nb + 1).astype(float)   # inclusive-Roman width (2026-05-17 convention)
    return T.trapezoidal_aoristic_spa(nb, na, width, bin_edges=H.BIN_EDGES)


def uniform_spa_2026_05_17(nb: np.ndarray, na: np.ndarray, H, T) -> np.ndarray:
    """Uniform-aoristic SPA on the h2_lib grid using the 2026-05-17 convention.

    The matched-convention uniform leg for the C11 input-level r (see the note in
    ``trapezoidal_spa_on_h2_grid``): same inclusive-Roman ``[nb, na+1)`` width and
    same (un-clipped) apportionment as the trapezoidal leg, so the only difference
    between the two SPAs is the trapezoidal vs uniform mass SHAPE — which is exactly
    the C11 sensitivity.
    """
    nb = np.asarray(nb)
    na = np.asarray(na)
    width = (na - nb + 1).astype(float)
    return T.uniform_aoristic_spa(nb, na, width, bin_edges=H.BIN_EDGES)


# =========================================================================== #
# H2.2 — corrected-vs-uncorrected template-boundary step magnitudes (SPEC §4).  #
# =========================================================================== #
def boundary_bin_index(year: int, H) -> int:
    """Index of the right-open h2_lib bin whose ``[lo, hi)`` contains ``year``.

    The boundary STEP at ``year`` is measured as ``|spa[idx] − spa[idx − 1]|`` —
    the jump from the bin just left of the boundary into the boundary bin (the
    plateau-edge transition the prereg's H2.2 reduction targets). Raises if the
    boundary bin or its left neighbour falls outside the grid.
    """
    idx = int((year - H.ENV_START) // H.BIN_SIZE)
    if idx <= 0 or idx >= H.N_BINS:
        raise ValueError(f"boundary year {year} maps to edge bin {idx} (no left "
                         f"neighbour on the grid); cannot measure a step")
    return idx


def boundary_steps(spa: np.ndarray, H,
                   boundary_years=TEMPLATE_BOUNDARY_YEARS) -> dict[int, float]:
    """Absolute bin-to-bin step magnitude ``|Δ|`` at each template boundary.

    For each boundary year, returns ``|spa[idx] − spa[idx − 1]|`` where ``idx`` is
    the boundary bin (``boundary_bin_index``). The SPA should be passed NORMALISED
    (sum 1) so corrected (posterior ``p_gen``) and uncorrected (raw SPA) steps are
    on the same scale — H2.2 compares their RATIO, so a common normalisation is the
    correct footing (the prereg's "step magnitude reduced ≥ 50 %", Field 3 l.105).
    """
    spa = np.asarray(spa, dtype=float)
    return {int(y): float(abs(spa[boundary_bin_index(y, H)]
                              - spa[boundary_bin_index(y, H) - 1]))
            for y in boundary_years}


def boundary_step_reduction(corrected_spa: np.ndarray, uncorrected_spa: np.ndarray,
                            H, boundary_years=TEMPLATE_BOUNDARY_YEARS) -> dict[str, Any]:
    """Per-boundary % reduction in step magnitude, corrected vs uncorrected (H2.2).

    Both SPAs are normalised to sum 1 before the step read-off (a common footing).
    The % reduction at a boundary is ``(uncorr − corr) / uncorr`` (a positive value
    means the deconvolution FLATTENED the template step, as H2.2 predicts). The
    prereg target is ``≥ 50 %``; the unit "meets" H2.2 if its MEAN reduction across
    the four boundaries is ≥ 50 % (reported per-boundary too, so a single-boundary
    failure is visible).

    Returns
    -------
    dict with per-boundary ``corrected`` / ``uncorrected`` / ``pct_reduction``
    steps, the ``mean_pct_reduction``, and the boolean ``meets_50pct``.
    """
    corr = normalise(corrected_spa)
    uncorr = normalise(uncorrected_spa)
    steps_corr = boundary_steps(corr, H, boundary_years)
    steps_uncorr = boundary_steps(uncorr, H, boundary_years)
    per_boundary: dict[str, Any] = {}
    reductions: list[float] = []
    for y in boundary_years:
        u = steps_uncorr[int(y)]
        c = steps_corr[int(y)]
        # % reduction: positive ⇒ corrected step is smaller (flattened). Guard the
        # u == 0 corner (no template step to flatten) → NaN, excluded from the mean.
        red = (u - c) / u if u > 0 else float("nan")
        per_boundary[str(int(y))] = {
            "uncorrected_step": u, "corrected_step": c, "pct_reduction": red}
        if np.isfinite(red):
            reductions.append(red)
    mean_red = float(np.mean(reductions)) if reductions else float("nan")
    return {
        "per_boundary": per_boundary,
        "mean_pct_reduction": mean_red,
        "meets_50pct": bool(np.isfinite(mean_red) and mean_red >= 0.50),
        "boundary_years": list(boundary_years),
    }


# =========================================================================== #
# H2.4 — stratified-by-convention-class SPA (SPEC §4).                          #
# =========================================================================== #
def stratified_family_spa(df_unit, H, families) -> tuple[np.ndarray, int]:
    """Normalised uniform-aoristic SPA of one family stratum within a unit.

    Builds the h2_lib uniform aoristic SPA of the rows whose ``family`` label is in
    ``families`` (the genuine-classed or convention-classed strata, SPEC §4 / C15),
    normalised to sum 1 (a shape, for the Pearson / band comparison against the
    model's deconvolved ``p_gen``). Returns ``(spa, n_rows_in_stratum)``.
    """
    fam = H.classify_family(df_unit)
    mask = np.isin(fam, list(families))
    sub = df_unit.loc[mask]
    spa = H.aoristic_spa(sub["nb"].to_numpy(), sub["na"].to_numpy())
    return normalise(spa), int(mask.sum())


def stratified_bootstrap_band(
        df_unit, H, families, n_boot: int, rng: np.random.Generator,
        ci: tuple[float, float] = (2.5, 97.5)) -> dict[str, Any]:
    """Per-bin bootstrap sampling-error band on a family-stratum SPA (H2.4).

    H2.4 asks whether the stratified-by-class SPA agrees with the model's
    deconvolved ``p_gen`` "within sampling error" (SPEC §4 / C15 — internal
    consistency, NOT independent validation). We bound the stratified SPA's
    sampling error by an inscription bootstrap: resample the stratum's rows with
    replacement, rebuild the normalised SPA, and report the per-bin percentile band.
    The caller checks the fraction of bins where the model ``p_gen`` falls inside
    the band (the agreement metric) plus the point Pearson r.

    Returns
    -------
    dict with the point ``spa`` (length N_BINS), the per-bin ``band_lo`` / ``band_hi``
    (length N_BINS), ``n_rows`` (stratum size), and ``n_boot``.
    """
    fam = H.classify_family(df_unit)
    mask = np.isin(fam, list(families))
    sub = df_unit.loc[mask]
    nb = sub["nb"].to_numpy()
    na = sub["na"].to_numpy()
    point = normalise(H.aoristic_spa(nb, na))
    n = nb.size
    if n == 0:
        nanrow = np.full(H.N_BINS, float("nan"))
        return {"spa": point.tolist(), "band_lo": nanrow.tolist(),
                "band_hi": nanrow.tolist(), "n_rows": 0, "n_boot": n_boot}
    boots = np.empty((n_boot, H.N_BINS), dtype=float)
    for b in range(n_boot):
        take = rng.integers(0, n, size=n)
        boots[b] = normalise(H.aoristic_spa(nb[take], na[take]))
    lo = np.percentile(boots, ci[0], axis=0)
    hi = np.percentile(boots, ci[1], axis=0)
    return {"spa": point.tolist(), "band_lo": lo.tolist(), "band_hi": hi.tolist(),
            "n_rows": int(n), "n_boot": n_boot}


def fraction_in_band(values: np.ndarray, band_lo: np.ndarray,
                     band_hi: np.ndarray) -> float:
    """Fraction of bins where ``values`` (e.g. model p_gen) lies within the band.

    NaN band bins (empty stratum) are excluded from both numerator and denominator,
    so the metric is over the bins where a band could be formed.
    """
    values = np.asarray(values, dtype=float)
    lo = np.asarray(band_lo, dtype=float)
    hi = np.asarray(band_hi, dtype=float)
    valid = np.isfinite(lo) & np.isfinite(hi)
    if not valid.any():
        return float("nan")
    inside = (values[valid] >= lo[valid]) & (values[valid] <= hi[valid])
    return float(np.mean(inside))


# =========================================================================== #
# C16 — α descriptive read-off from the lodged refit summary (SPEC §4).         #
# =========================================================================== #
def load_refit_summary(root: Path = DEFAULT_ROOT) -> dict[str, Any]:
    """Load the lodged cc-production-refit summary (the primary α's; SPEC reuse).

    Read-only; the primary fits are reused, never re-run (SPEC §4 / reuse note).
    """
    p = (root / "runs" / "2026-06-13-cc-production-refit" / "outputs"
         / "refit-summary.json")
    return json.loads(p.read_text(encoding="utf-8"))


def c16_alpha_table(root: Path = DEFAULT_ROOT) -> list[dict[str, Any]]:
    """Per-unit α (median + 95 % CI) read-off for C16 (descriptive context).

    Pulls ``alpha_median`` / ``alpha_ci_lo`` / ``alpha_ci_hi`` from the refit summary
    per unit, plus frame / tier / convergence and the effective N (so the reachability
    floor caveat, SPEC §6, can be applied downstream). Empire and Latin aggregates are
    flagged via their ``frame``. Pure read-off — no fit.
    """
    summ = load_refit_summary(root)
    rows: list[dict[str, Any]] = []
    for u in summ["units"]:
        rows.append({
            "name": u["name"], "frame": u.get("frame"), "tier": u.get("tier"),
            "n_rows_eff": u.get("n_rows_eff"), "n_rows_raw": u.get("n_rows_raw"),
            "alpha_median": u.get("alpha_median"),
            "alpha_ci_lo": u.get("alpha_ci_lo"), "alpha_ci_hi": u.get("alpha_ci_hi"),
            "convergence_pass": u.get("convergence_pass"),
        })
    return rows


# =========================================================================== #
# H2.3 — date_range threshold filtering (data-prep; the refits live in the      #
# orchestrator because they fit, SPEC §4 / C14).                                #
# =========================================================================== #
def filter_by_date_range(df_unit, threshold: int):
    """Subset a unit's rows to ``date_range ≤ threshold`` (H2.3 / C14).

    ``date_range`` (= ``na − nb``) is added by ``h2_lib.load_filtered_lire``. The
    filtered subset is the corpus the model is refit on at that threshold; tighter
    thresholds keep only the date-honest (narrow-interval) rows.
    """
    return df_unit.loc[df_unit["date_range"] <= int(threshold)]
