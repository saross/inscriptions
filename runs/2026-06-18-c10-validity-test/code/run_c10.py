#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_c10.py — driver for the C10 aoristic-MC validity test (1a + 1b + 1c).
=========================================================================

Wires the three SPEC §3 tests and writes
``outputs/VALIDITY-REPORT.md`` + ``outputs/results.json`` per the §3b
pre-registered decision rule.

    1a — slab-concentration diagnostic on the REAL empire aligned subset
         (deterministic, NO MCMC): the three §3a metrics on the aoristic-mass SPA
         vs N point-date-sampled SPAs.
    1b — ground-truth recovery (synthetic, decisive, MCMC): sweep planted
         α ∈ {0.3, 0.5, 0.68, 0.8}, ≥3 generator seeds; fit the mass-deconvolution
         arm (``build_model_cross_classified(pconv_mode="library")``) and the
         point-date aoristic-MC arm (N_MC = 10); recover α both ways vs planted.
    1c — mass-preserving vs point-collapse contrast on the REAL empire data
         (MCMC): aoristic-MC two ways and compare recovered α.

BUILD-ONLY / RUN GATE
---------------------
This driver performs MCMC. It is NOT run as part of the build/audit — it runs
**only after audit sign-off** (the synthetic generator's faithfulness to SPEC §2 is
the key audit target). The post-audit run command is in the module docstring of
``c10_lib`` and the BUILD-NOTES; see ``main()``'s ``--stage`` switch.

All generators, count builders, and diagnostics live in ``c10_lib`` (imported here);
the MCMC model is the lodged ``joint_lib.build_model_cross_classified`` (imported,
never modified). The point-date arm reuses the C10 method
(``c10_lib.point_date_cc_counts``, the same scheme as the lodged
``run_supp.aoristic_mc_realisation``).

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np

RUN_DIR = Path("/home/shawn/Code/inscriptions/runs/2026-06-18-c10-validity-test")
CODE_DIR = RUN_DIR / "code"
OUT_DIR = RUN_DIR / "outputs"
for _d in (str(CODE_DIR),):
    if _d not in sys.path:
        sys.path.insert(0, _d)

import c10_lib as C  # noqa: E402

# h2_lib / joint_lib / refit_lib are wired by c10_lib's sys.path inserts.
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402

# --------------------------------------------------------------------------- #
# Test configuration (SPEC §3b / §5; all pinned for the audit).                 #
# --------------------------------------------------------------------------- #
PLANTED_ALPHAS = (0.3, 0.5, 0.68, 0.8)   # SPEC §3b sweep
N_SEEDS = 3                              # SPEC §3b: >= 3 generator seeds per alpha
N_SYNTH = 3000                           # synthetic inscriptions per (alpha, seed)
N_MC = 10                                # SPEC §5: PIN N_MC = 10 for the recovery test
N_DIAG_SPA = 10                          # 1a: number of point-date-sampled SPAs
BASE_SEED = 20260618                     # this run's base seed (distinct per arm)
GENUINE_PGEN = "empire"                  # SPEC §3b: empire posterior p_gen (else "gauss")
GENUINE_HALF_WIDTH = C.GENUINE_HALF_WIDTH_DEFAULT  # 2.5 y (one-bin tight bracket)

# §3b recovery tolerance (the recovery-grid tolerance, "≈ <= 0.1").
RECOVERY_TOL = 0.1
# §3b reading-(b) "low floor near ~0.10" the pilot showed (for the flat-in-true-α test).
PILOT_FLOOR = 0.10

# 1c mass-preserving jitter: ±1 bin (±BIN_SIZE years) on each recorded bound.
JITTER_BINS = 1


# =========================================================================== #
# Shared MCMC helpers (the lodged production sampler config; NO new model).      #
# =========================================================================== #
def _sample_alpha(model, seed: int) -> np.ndarray:
    """Sample one cross-classified model with the production config; return α draws.

    Uses the lodged ``h2_lib`` sampler defaults (draws / tune / chains / target-accept),
    cores = 1, so the synthetic fits sit on the identical footing as production.
    """
    import pymc as pm

    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                target_accept=H.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True)
    return idata.posterior["alpha"].values.reshape(-1)


def _alpha_stats(draws: np.ndarray) -> dict[str, float]:
    """Median + 95 % CI of pooled α draws."""
    lo, hi = (float(x) for x in np.percentile(draws, [2.5, 97.5]))
    return {"alpha_median": float(np.median(draws)),
            "alpha_ci_lo": lo, "alpha_ci_hi": hi, "ci_width": hi - lo}


def _fit_mass_arm(ya: np.ndarray, yn: np.ndarray, k: int, n_rows: int,
                  basis: np.ndarray, tc_ab, tg_ab, seed: int) -> np.ndarray:
    """Fit the mass-deconvolution arm on one synthetic frame; return α draws.

    Builds the lodged ``build_model_cross_classified(pconv_mode="library")`` on the
    aoristic-mass counts and samples once. This is the arm already validated to
    recover α (the recovery-grid machinery; SPEC §3b "reuse … for the mass-arm").
    """
    model = J.build_model_cross_classified(
        ya, yn, k, n_rows, basis, tc_ab, tg_ab, pconv_mode="library")
    return _sample_alpha(model, seed)


def _fit_pointdate_arm(df, basis: np.ndarray, tc_ab, tg_ab,
                       base_seed: int, n_mc: int) -> dict[str, Any]:
    """Fit the point-date aoristic-MC arm on one synthetic frame; return pooled α.

    Build-once-then-``set_data`` over ``n_mc`` point-date realisations (the lodged C10
    method), pooling α draws across realisations — exactly the
    ``run_supp.run_pilot`` aoristic-MC loop, on synthetic data. The alignment subset
    totals ``k_cc`` / ``n_rows`` are the point-date raw counts (held constant; each
    inscription deposits one count into one bin of its fixed subset).
    """
    import pymc as pm

    pooled = []
    per_real = []
    model = None
    # First realisation fixes the held-constant totals the model is built on.
    for r in range(n_mc):
        rng_r = np.random.default_rng(base_seed + r)
        ya_r, yn_r, k_cc, n_rows = C.point_date_cc_counts(df, rng_r)
        # M2 GUARD before every set_data swap.
        assert int(ya_r.sum()) == k_cc, f"point-date realisation {r}: k mismatch"
        assert int(ya_r.sum() + yn_r.sum()) == n_rows, (
            f"point-date realisation {r}: n_rows mismatch")
        if model is None:
            model = J.build_model_cross_classified(
                ya_r, yn_r, k_cc, n_rows, basis, tc_ab, tg_ab, pconv_mode="library")
        else:
            with model:
                pm.set_data({"k_data": np.asarray(k_cc, dtype="int64"),
                             "y_al_data": ya_r, "y_non_data": yn_r})
        a_r = _sample_alpha(model, base_seed + r)
        pooled.append(a_r)
        per_real.append({"realisation": r, "alpha_median": float(np.median(a_r))})
    pooled_arr = np.concatenate(pooled)
    out = _alpha_stats(pooled_arr)
    out["per_realisation_alpha_median"] = [pr["alpha_median"] for pr in per_real]
    out["n_mc"] = n_mc
    return out


# =========================================================================== #
# 1a — slab-concentration diagnostic (real empire aligned subset; NO MCMC).      #
# =========================================================================== #
def run_1a(basis: np.ndarray, slabs, seed: int) -> dict[str, Any]:
    """The three §3a metrics on the REAL empire aligned subset, deterministic.

    Loads the real empire data (``refit_lib`` / ``h2_lib``), takes the empire-aggregate
    subset, applies the real rule-C ``aligned_indicator``, builds the aoristic-mass
    aligned SPA and ``N_DIAG_SPA`` point-date-sampled aligned SPAs, and computes
    metrics (i) L1-to-nearest-slab-row, (ii) round-boundary mass fraction (+ ratio to
    uniform), (iii) best-fit non-negative slab-mixture weight — for BOTH schemes.

    Expected under reading (b): aoristic-mass is slab-like (low L1, high round-boundary
    ratio, high slab-mixture weight); point-date SPAs are markedly flatter.
    """
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    units = {u["name"]: u for u in R.enumerate_refit_units()}
    sub = R.subset_for(df, units["empire-aggregate"], latin)
    amask = J.aligned_indicator(sub, rule=R.ALIGN_RULE).astype(bool)

    # Aoristic-mass aligned SPA (deterministic).
    mass_spa = C.aoristic_mass_spa(sub, mask=amask)
    mass_metrics = {
        "l1_to_nearest_slab": C.l1_to_nearest_slab_row(mass_spa, basis),
        "round_boundary": C.round_boundary_mass_fraction(mass_spa),
        "slab_mixture": C.best_fit_slab_mixture_weight(mass_spa, basis),
    }

    # N point-date-sampled aligned SPAs (stochastic; summarise across draws).
    pt_l1, pt_ratio, pt_wt = [], [], []
    for s in range(N_DIAG_SPA):
        rng = np.random.default_rng(seed + s)
        pt_spa = C.point_date_spa(sub, rng, mask=amask)
        pt_l1.append(C.l1_to_nearest_slab_row(pt_spa, basis)["l1_min"])
        pt_ratio.append(C.round_boundary_mass_fraction(pt_spa)["ratio"])
        pt_wt.append(C.best_fit_slab_mixture_weight(pt_spa, basis)["total_weight"])

    def _summ(vals):
        a = np.asarray(vals, dtype=float)
        return {"mean": float(a.mean()), "min": float(a.min()), "max": float(a.max())}

    return {
        "unit": "empire-aggregate",
        "n_rows": int(len(sub)),
        "n_aligned": int(amask.sum()),
        "n_point_date_spa": N_DIAG_SPA,
        "aoristic_mass": mass_metrics,
        "point_date": {
            "l1_to_nearest_slab": _summ(pt_l1),
            "round_boundary_ratio": _summ(pt_ratio),
            "slab_mixture_total_weight": _summ(pt_wt),
        },
    }


# =========================================================================== #
# 1b — ground-truth recovery (synthetic, decisive; MCMC).                        #
# =========================================================================== #
def run_1b(basis: np.ndarray, slabs, tc_ab, tg_ab) -> dict[str, Any]:
    """Recovery sweep: planted α × seeds × two arms (mass + point-date).

    For each planted α in PLANTED_ALPHAS and each of N_SEEDS generator seeds, generate
    a synthetic per-inscription frame (SPEC §2), then recover α two ways:
    mass-deconvolution and point-date aoristic-MC. Records recovered α (median + 95 %
    CI) for both arms vs the planted α, plus the realised (observed) α in the frame.
    """
    p_gen, pgen_label = C.resolve_pgen(GENUINE_PGEN)
    cells = []
    for ai, alpha in enumerate(PLANTED_ALPHAS):
        for si in range(N_SEEDS):
            gen_seed = BASE_SEED + 1000 * ai + si           # generator seed
            mass_fit_seed = BASE_SEED + 100_000 + 1000 * ai + si
            pt_base_seed = BASE_SEED + 300_000 + 10_000 * ai + 1000 * si

            df = C.generate_inscriptions(
                alpha, N_SYNTH, gen_seed, slabs, p_gen,
                genuine_half_width=GENUINE_HALF_WIDTH)
            realised_alpha = float((df["type"] == "convention").mean())

            mass = C.mass_cc_counts(df)
            t0 = time.time()
            mass_draws = _fit_mass_arm(
                mass["y_aligned"], mass["y_nonaligned"], mass["k"], mass["n_rows"],
                basis, tc_ab, tg_ab, mass_fit_seed)
            mass_secs = time.time() - t0
            mass_stats = _alpha_stats(mass_draws)

            t0 = time.time()
            pt_stats = _fit_pointdate_arm(df, basis, tc_ab, tg_ab, pt_base_seed, N_MC)
            pt_secs = time.time() - t0

            cells.append({
                "planted_alpha": float(alpha),
                "seed_index": si,
                "gen_seed": gen_seed,
                "realised_alpha": realised_alpha,
                "n_aligned_raw": mass["n_aligned_raw"],
                "row_aligned_frac": mass["row_aligned_frac"],
                "mass_aligned_frac": mass["mass_aligned_frac"],
                "mass_arm": {**mass_stats, "delta": mass_stats["alpha_median"] - alpha,
                             "secs": round(mass_secs, 1)},
                "point_date_arm": {**pt_stats,
                                   "delta": pt_stats["alpha_median"] - alpha,
                                   "secs": round(pt_secs, 1)},
            })
    return {"pgen": pgen_label, "n_synth": N_SYNTH, "n_mc": N_MC,
            "n_seeds": N_SEEDS, "planted_alphas": list(PLANTED_ALPHAS),
            "cells": cells}


# =========================================================================== #
# 1c — mass-preserving vs point-collapse contrast (real empire; MCMC).           #
# =========================================================================== #
def _jitter_bounds(nb: np.ndarray, na: np.ndarray, rng: np.random.Generator,
                   jitter_bins: int = JITTER_BINS) -> tuple[np.ndarray, np.ndarray]:
    """Perturb recorded interval bounds by ±``jitter_bins`` bins (mass-preserving 1c).

    Each bound gets an independent uniform integer shift in
    ``{−jitter_bins, …, +jitter_bins} × BIN_SIZE`` years; bounds are re-ordered so
    ``na >= nb`` and a minimum 1-year width is enforced so the aoristic SPA stays
    well-defined (an interval that collapses to a point would deposit zero mass in
    ``aoristic_spa``, which requires width > 0). The mass is then KEPT spread over the
    perturbed interval (the aoristic-mass build), so the slab structure survives while
    date-bracket uncertainty is injected — the SPEC §3c corrected-sensitivity prototype.
    """
    span = jitter_bins * H.BIN_SIZE
    shift_nb = rng.integers(-jitter_bins, jitter_bins + 1, size=len(nb)) * H.BIN_SIZE
    shift_na = rng.integers(-jitter_bins, jitter_bins + 1, size=len(na)) * H.BIN_SIZE
    nb2 = nb + shift_nb
    na2 = na + shift_na
    swap = na2 < nb2
    nb2[swap], na2[swap] = na2[swap], nb2[swap]
    # Enforce a minimum width so aoristic_spa (width > 0) keeps every inscription.
    degenerate = na2 <= nb2
    na2[degenerate] = nb2[degenerate] + H.BIN_SIZE
    return nb2.astype(float), na2.astype(float)


def _mass_preserving_realisation(sub, amask: np.ndarray,
                                 rng: np.random.Generator
                                 ) -> tuple[np.ndarray, np.ndarray, int, int]:
    """One mass-preserving realisation of cross-classified aoristic-mass counts.

    Jitters the recorded bounds (±1 bin), then builds aoristic-MASS largest-remainder
    counts within each FIXED alignment subset (alignment is on the ORIGINAL recorded
    interval, held constant — the SPEC §3c design). Returns ``(y_aligned,
    y_nonaligned, k, n_rows)`` in aoristic-effective counts with the lumping/thinning
    invariants asserted.
    """
    nb = sub["nb"].to_numpy().astype(float)
    na = sub["na"].to_numpy().astype(float)
    nb2, na2 = _jitter_bounds(nb, na, rng)
    ya = H.largest_remainder(H.aoristic_spa(nb2[amask], na2[amask]))
    yn = H.largest_remainder(H.aoristic_spa(nb2[~amask], na2[~amask]))
    ya = np.asarray(ya, dtype="int64")
    yn = np.asarray(yn, dtype="int64")
    k = int(ya.sum())
    n_rows = int(k + int(yn.sum()))
    assert int(ya.sum()) == k, "mass-preserving: k mismatch"
    assert int(ya.sum() + yn.sum()) == n_rows, "mass-preserving: n_rows mismatch"
    return ya, yn, k, n_rows


def run_1c(basis: np.ndarray, tc_ab, tg_ab) -> dict[str, Any]:
    """Aoristic-MC two ways on the REAL empire: point-collapse vs mass-preserving.

    Both schemes run N_MC realisations on the empire-aggregate aligned/non-aligned
    subsets (alignment FIXED on the original recorded intervals) and pool α draws.

    * Point-collapse — the current C10: ``t_i ~ Uniform(interval)`` → one bin each
      (``c10_lib.point_date_cc_counts``).
    * Mass-preserving — jitter the recorded bounds ±1 bin but KEEP the mass spread
      over the (perturbed) interval (``_mass_preserving_realisation``).

    Expected under reading (b): α collapses under point-collapse only; the
    mass-preserving variant stays near the deconvolution α (~0.68).
    """
    import pymc as pm

    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    units = {u["name"]: u for u in R.enumerate_refit_units()}
    sub = R.subset_for(df, units["empire-aggregate"], latin)
    amask = J.aligned_indicator(sub, rule=R.ALIGN_RULE).astype(bool)

    results: dict[str, Any] = {"unit": "empire-aggregate", "n_mc": N_MC,
                               "n_rows_raw": int(len(sub)),
                               "n_aligned_raw": int(amask.sum())}

    # ---- (A) point-collapse (the current C10) ----
    pooled = []
    model = None
    base = BASE_SEED + 500_000
    for r in range(N_MC):
        rng_r = np.random.default_rng(base + r)
        ya_r, yn_r, k_cc, n_rows = C.point_date_cc_counts(sub, rng_r, amask=amask)
        assert int(ya_r.sum()) == k_cc and int(ya_r.sum() + yn_r.sum()) == n_rows
        if model is None:
            model = J.build_model_cross_classified(
                ya_r, yn_r, k_cc, n_rows, basis, tc_ab, tg_ab, pconv_mode="library")
        else:
            with model:
                pm.set_data({"k_data": np.asarray(k_cc, dtype="int64"),
                             "y_al_data": ya_r, "y_non_data": yn_r})
        pooled.append(_sample_alpha(model, base + r))
    results["point_collapse"] = _alpha_stats(np.concatenate(pooled))

    # ---- (B) mass-preserving perturbation ----
    # NOTE: aoristic-effective totals (k, n_rows) vary slightly per realisation with
    # the largest-remainder rounding of the jittered SPA, so the model is REBUILT each
    # realisation (cannot set_data across changing totals). N_MC small (10) so cheap.
    pooled_mp = []
    base = BASE_SEED + 700_000
    for r in range(N_MC):
        rng_r = np.random.default_rng(base + r)
        ya_r, yn_r, k_cc, n_rows = _mass_preserving_realisation(sub, amask, rng_r)
        model_mp = J.build_model_cross_classified(
            ya_r, yn_r, k_cc, n_rows, basis, tc_ab, tg_ab, pconv_mode="library")
        pooled_mp.append(_sample_alpha(model_mp, base + r))
    results["mass_preserving"] = _alpha_stats(np.concatenate(pooled_mp))
    results["jitter_bins"] = JITTER_BINS
    return results


# =========================================================================== #
# Verdict (SPEC §3b pre-registered decision rule).                              #
# =========================================================================== #
def decide(res_1b: dict[str, Any]) -> dict[str, Any]:
    """Apply the SPEC §3b decision rule to the 1b recovery sweep.

    (b) CONFIRMED if: the mass arm recovers planted α across the sweep (|Δα| within
        RECOVERY_TOL) AND the point-date arm collapses to a low floor LARGELY
        INDEPENDENT of planted α (flat in true α, near the pilot floor ~0.10).
    (a) SUPPORTED if: the point-date arm also TRACKS planted α (recovers within
        RECOVERY_TOL across the sweep).

    "Flat in true α" is operationalised as: the spread of the per-planted-α mean
    point-date α across the sweep is small (< RECOVERY_TOL) AND the slope of
    point-date α vs planted α is shallow (< 0.5) — i.e. point-date α barely moves as
    planted α spans 0.3 → 0.8.
    """
    cells = res_1b["cells"]
    planted = np.array([c["planted_alpha"] for c in cells], dtype=float)
    mass_med = np.array([c["mass_arm"]["alpha_median"] for c in cells], dtype=float)
    pt_med = np.array([c["point_date_arm"]["alpha_median"] for c in cells], dtype=float)

    mass_abs_dev = np.abs(mass_med - planted)
    pt_abs_dev = np.abs(pt_med - planted)
    mass_recovers = bool(np.all(mass_abs_dev <= RECOVERY_TOL))
    pt_tracks = bool(np.all(pt_abs_dev <= RECOVERY_TOL))

    # Per-planted-α mean point-date α, and the flatness diagnostics.
    uniq = np.array(sorted(set(planted)))
    pt_means = np.array([pt_med[planted == a].mean() for a in uniq])
    pt_spread = float(pt_means.max() - pt_means.min())
    # OLS slope of point-date α vs planted α.
    slope = float(np.polyfit(planted, pt_med, 1)[0]) if len(set(planted)) > 1 else float("nan")
    pt_flat = bool(pt_spread < RECOVERY_TOL and abs(slope) < 0.5)
    near_floor = bool(np.median(pt_med) <= PILOT_FLOOR + RECOVERY_TOL)

    if mass_recovers and pt_flat:
        verdict = "(b) CONFIRMED — point-date sampling destroys the convention signal"
    elif pt_tracks:
        verdict = "(a) SUPPORTED — point-date aoristic-MC tracks planted alpha; C10 stands"
    else:
        verdict = ("INDETERMINATE — neither rule cleanly met; inspect the sweep "
                   "(mass_recovers=%s, pt_flat=%s, pt_tracks=%s)"
                   % (mass_recovers, pt_flat, pt_tracks))

    return {
        "verdict": verdict,
        "mass_recovers_within_tol": mass_recovers,
        "mass_max_abs_dev": float(mass_abs_dev.max()),
        "point_date_tracks_within_tol": pt_tracks,
        "point_date_max_abs_dev": float(pt_abs_dev.max()),
        "point_date_flat_in_true_alpha": pt_flat,
        "point_date_mean_per_planted_alpha": {float(a): float(m)
                                              for a, m in zip(uniq, pt_means)},
        "point_date_spread": pt_spread,
        "point_date_slope_vs_planted": slope,
        "point_date_near_pilot_floor": near_floor,
        "recovery_tol": RECOVERY_TOL,
        "pilot_floor": PILOT_FLOOR,
    }


# =========================================================================== #
# Report writers.                                                               #
# =========================================================================== #
def _write_report_md(path: Path, results: dict[str, Any]) -> None:
    """Write the human-readable VALIDITY-REPORT.md (the a-vs-b verdict)."""
    L = ["# C10 aoristic-MC validity test — VALIDITY REPORT", ""]
    L.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    if "verdict" in results:
        L.append("## Verdict (SPEC §3b decision rule)")
        L.append("")
        v = results["verdict"]
        L.append(f"**{v['verdict']}**")
        L.append("")
        L.append(f"- mass arm recovers planted α within tol ({v['recovery_tol']}): "
                 f"**{v['mass_recovers_within_tol']}** "
                 f"(max |Δα| = {v['mass_max_abs_dev']:.3f})")
        L.append(f"- point-date arm tracks planted α within tol: "
                 f"**{v['point_date_tracks_within_tol']}** "
                 f"(max |Δα| = {v['point_date_max_abs_dev']:.3f})")
        L.append(f"- point-date arm flat in true α: "
                 f"**{v['point_date_flat_in_true_alpha']}** "
                 f"(spread {v['point_date_spread']:.3f}, "
                 f"slope {v['point_date_slope_vs_planted']:.3f})")
        L.append(f"- point-date α near pilot floor (~{v['pilot_floor']}): "
                 f"**{v['point_date_near_pilot_floor']}**")
        L.append("")

    if "test_1b" in results:
        L.append("## 1b — ground-truth recovery (synthetic)")
        L.append("")
        L.append(f"p_gen = {results['test_1b']['pgen']}; N_synth = "
                 f"{results['test_1b']['n_synth']}; N_MC = {results['test_1b']['n_mc']}; "
                 f"seeds = {results['test_1b']['n_seeds']}.")
        L.append("")
        L.append("| planted α | seed | realised α | mass α (med [CI]) | point-date α (med [CI]) |")
        L.append("|---|---|---|---|---|")
        for c in results["test_1b"]["cells"]:
            m, p = c["mass_arm"], c["point_date_arm"]
            L.append(f"| {c['planted_alpha']:.2f} | {c['seed_index']} | "
                     f"{c['realised_alpha']:.3f} | "
                     f"{m['alpha_median']:.3f} [{m['alpha_ci_lo']:.3f}, {m['alpha_ci_hi']:.3f}] | "
                     f"{p['alpha_median']:.3f} [{p['alpha_ci_lo']:.3f}, {p['alpha_ci_hi']:.3f}] |")
        L.append("")

    if "test_1a" in results:
        a = results["test_1a"]
        L.append("## 1a — slab-concentration diagnostic (real empire aligned subset)")
        L.append("")
        L.append(f"Unit {a['unit']}; n_rows {a['n_rows']}, n_aligned {a['n_aligned']}; "
                 f"{a['n_point_date_spa']} point-date SPAs.")
        L.append("")
        am = a["aoristic_mass"]
        pt = a["point_date"]
        L.append("| metric | aoristic-mass | point-date (mean) |")
        L.append("|---|---|---|")
        L.append(f"| L1 to nearest slab row | {am['l1_to_nearest_slab']['l1_min']:.3f} | "
                 f"{pt['l1_to_nearest_slab']['mean']:.3f} |")
        L.append(f"| round-boundary mass ratio (vs uniform) | "
                 f"{am['round_boundary']['ratio']:.3f} | "
                 f"{pt['round_boundary_ratio']['mean']:.3f} |")
        L.append(f"| best-fit slab-mixture weight | {am['slab_mixture']['total_weight']:.3f} | "
                 f"{pt['slab_mixture_total_weight']['mean']:.3f} |")
        L.append("")

    if "test_1c" in results:
        c = results["test_1c"]
        L.append("## 1c — mass-preserving vs point-collapse (real empire)")
        L.append("")
        L.append(f"Unit {c['unit']}; N_MC {c['n_mc']}; jitter ±{c['jitter_bins']} bin(s).")
        L.append("")
        L.append("| scheme | α median | 95 % CI |")
        L.append("|---|---|---|")
        L.append(f"| point-collapse (current C10) | {c['point_collapse']['alpha_median']:.3f} | "
                 f"[{c['point_collapse']['alpha_ci_lo']:.3f}, "
                 f"{c['point_collapse']['alpha_ci_hi']:.3f}] |")
        L.append(f"| mass-preserving (±1 bin) | {c['mass_preserving']['alpha_median']:.3f} | "
                 f"[{c['mass_preserving']['alpha_ci_lo']:.3f}, "
                 f"{c['mass_preserving']['alpha_ci_hi']:.3f}] |")
        L.append("")

    path.write_text("\n".join(L), encoding="utf-8")


# =========================================================================== #
# Driver.                                                                       #
# =========================================================================== #
def main() -> None:
    """Run the selected stages and write results.json + VALIDITY-REPORT.md.

    POST-AUDIT RUN COMMAND (sapphire/zbook; do NOT run during build):
        cd /home/shawn/Code/inscriptions
        .venv/bin/python runs/2026-06-18-c10-validity-test/code/run_c10.py --stage all
    """
    ap = argparse.ArgumentParser(description="C10 aoristic-MC validity test driver.")
    ap.add_argument("--stage", choices=["1a", "1b", "1c", "all"], default="all",
                    help="which test(s) to run (default: all)")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR,
                    help=f"output directory (default {OUT_DIR})")
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    basis, slabs = R.load_library_basis()
    tc_ab, tg_ab, _theta_fit = R.adopted_theta_priors()

    results: dict[str, Any] = {
        "spec": "runs/2026-06-18-c10-validity-test/SPEC.md",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "planted_alphas": list(PLANTED_ALPHAS), "n_seeds": N_SEEDS,
            "n_synth": N_SYNTH, "n_mc": N_MC, "base_seed": BASE_SEED,
            "genuine_pgen": GENUINE_PGEN, "genuine_half_width": GENUINE_HALF_WIDTH,
            "align_rule": R.ALIGN_RULE, "recovery_tol": RECOVERY_TOL,
            "theta_conv_ab": list(tc_ab), "theta_gen_ab": list(tg_ab),
        },
    }

    if args.stage in ("1a", "all"):
        results["test_1a"] = run_1a(basis, slabs, BASE_SEED + 900_000)
    if args.stage in ("1b", "all"):
        results["test_1b"] = run_1b(basis, slabs, tc_ab, tg_ab)
        results["verdict"] = decide(results["test_1b"])
    if args.stage in ("1c", "all"):
        results["test_1c"] = run_1c(basis, tc_ab, tg_ab)

    (args.out_dir / "results.json").write_text(
        json.dumps(results, indent=2, default=float), encoding="utf-8")
    _write_report_md(args.out_dir / "VALIDITY-REPORT.md", results)
    print(f"Wrote {args.out_dir / 'results.json'} and "
          f"{args.out_dir / 'VALIDITY-REPORT.md'}")


if __name__ == "__main__":
    main()
