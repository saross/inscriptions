#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_supp.py — supplementary-wave orchestrator (PILOT mode; SPEC §9).
====================================================================

The H2.1 supplementary wave (``runs/2026-06-18-h2.1-supplementary-wave/SPEC.md``)
re-maps the lodged Dirichlet-multinomial (C5) and rescaled negative-binomial (C6)
supplementaries onto the adopted cross-classified likelihood, and runs the
preregistered sensitivities/consistency checks alongside the primary. This module
implements the **prereg-mandated pilot gate** (SPEC §9) — the cheap, supervised
step that MUST be signed off before the full 29-unit production run is authorised.

THIS IS BUILD-ONLY at the time of writing: the pilot is AUDITED before it is ever
run. ``--pilot`` is the only implemented mode; the full production sweep is a
follow-on that gates on the pilot report.

What the pilot does (SPEC §9.2–§9.4), when later run on sapphire
---------------------------------------------------------------
1. **DM + NB model-comparison fits** on empire-aggregate AND Latium et Campania /
   Regio I (a mid-size diagnostic unit). Records per-fit wall time, convergence
   (the SPEC §7 α + tier_weights gate), and the κ posterior. Computes the
   multinomial **posterior-predictive dispersion** check on the PRIMARY fit (the
   prereg's stated trigger for preferring the DM, l.192): bin-level observed
   variance vs the multinomial expectation.
2. **κ-tuning** — a prior-predictive check on empire at candidate ``S_KAPPA`` so the
   ``HalfNormal(σ = S_KAPPA)`` prior places mass across κ ∈ ~[10, 1e4] (weakly
   informative, data-dominated; does NOT force overdispersion). Chooses ``S_KAPPA``;
   records the value + rationale.
3. **Aoristic-MC PILOT SUBSAMPLE** — empire ONLY, ``N_MC = 10`` (explicitly a PILOT
   subsample, NOT the production ``N_MC = 30``). Per realisation: sample
   ``t_i ~ Uniform(nb_i, na_i)`` per inscription (year-precise ``[t, t]`` fixed),
   bin to the 5-year grid WITHIN each FIXED alignment subset — ``k_cc`` and
   ``n_rows`` are HELD CONSTANT (alignment depends on the recorded interval +
   ``ALIGN_RULE = "C"``, NOT the sampled date). Fits the PRIMARY (not DM/NB — the
   prereg aoristic-MC is the multinomial primary only) via ``set_data`` each
   realisation; pools α across realisations. Reports the cross-realisation 95 % α
   band and per-realisation wall time, and PROJECTS the full ``N_MC = 30`` × 29-unit
   aoristic-MC cost and the whole-wave cost vs SPEC §8 (~20 core-hr / ~3–5 h wall).
   Flags if the projection exceeds ~8 h wall (the SPEC §8 halt-and-report ceiling).
4. Writes ``outputs/PILOT-REPORT.md``.

The M2 sum-invariant guard
--------------------------
Before EVERY ``pm.set_data`` swap in the aoristic-MC, this driver ASSERTS
``y_aligned.sum() == k_cc`` AND ``y_aligned.sum() + y_nonaligned.sum() == n_rows``
(the audit's M2 guard). The DM/Multinomial silently returns ``-inf`` if a swap
breaks ``sum(obs) == n``, so a broken realisation would otherwise corrupt the pooled
α without erroring — the assert turns a silent corruption into a loud failure.

Sampling config + infra
------------------------
Reuses the production sampling config (``h2_lib`` N_DRAWS / N_TUNE / N_CHAINS,
``cores = 1``) and the cc-grid sapphire infra patterns (spawn workers, root-fs
``TMPDIR``, cgroup ``MemoryMax`` set by the launch wrapper). Host / paths are
PARAMETERISED (``--root``); nothing is hardcoded to a single run.

Usage (sapphire) — BUILD-ONLY until audited; do NOT run before sign-off::

    PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
        PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
        uv run python code/run_supp.py --pilot

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------- #
# Path wiring. Parameterised root (``--root``) so the driver is not pinned to a #
# single checkout; the repo lives at the same location on amd-tower and         #
# sapphire (standing rule), so the default is correct on both.                  #
# --------------------------------------------------------------------------- #
DEFAULT_ROOT = Path("/home/shawn/Code/inscriptions")


def _wire_paths(root: Path) -> None:
    """Insert the sibling-run code dirs on ``sys.path`` (idempotent)."""
    h2 = root / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
    joint = root / "runs" / "2026-06-09-joint-identifiability" / "code"
    refit = root / "runs" / "2026-06-13-cc-production-refit" / "code"
    supp = root / "runs" / "2026-06-18-h2.1-supplementary-wave" / "code"
    cell_lib = (root / "runs" / "2026-06-06-convention-basis-redesign"
                / "revalidation" / "code")
    for p in (str(supp), str(refit), str(h2), str(joint), str(cell_lib)):
        if p not in sys.path:
            sys.path.insert(0, p)


# --------------------------------------------------------------------------- #
# Pilot constants (SPEC §9). PILOT values — explicitly NOT production.          #
# --------------------------------------------------------------------------- #
PILOT_UNITS = ["empire-aggregate", "Latium et Campania / Regio I"]
AOMC_UNIT = "empire-aggregate"          # aoristic-MC pilot subsample: empire ONLY
N_MC_PILOT = 10                         # PILOT subsample (NOT production N_MC = 30)
N_MC_PRODUCTION = 30                    # SPEC §5 design-artefact pin (for projection)
N_UNITS_PRODUCTION = 29                 # SPEC §6 scope (for projection)
WALL_CEILING_HOURS = 8.0                # SPEC §8 halt-and-report ceiling

# κ-tuning prior-predictive (SPEC §3.3). Candidate σ for HalfNormal(σ) on κ, chosen
# so the prior places mass across κ ∈ ~[10, 1e4] (weakly informative, data-dominated).
S_KAPPA_CANDIDATES = [1e2, 3e2, 1e3, 3e3, 1e4]
S_KAPPA_DEFAULT = 1e3                   # SPEC §3.3 default starting point
KAPPA_PRIOR_SPAN = (10.0, 1e4)          # target prior coverage on κ
PRIOR_PRED_DRAWS = 20000                # prior-predictive sample size (cheap, no fit)

PILOT_SEED = 20260618                   # fixed pilot seed


# =========================================================================== #
# Aoristic-MC data realisation (SPEC §9.3 / C10).                              #
# =========================================================================== #
def aoristic_mc_realisation(df_unit, amask: np.ndarray, rng: np.random.Generator,
                            H, k_cc: int, n_rows: int) -> tuple[np.ndarray, np.ndarray]:
    """One aoristic-MC realisation: point-date counts within FIXED subsets.

    Samples ``t_i ~ Uniform(nb_i, na_i)`` per inscription (year-precise ``[t, t]``
    fixed), clips to the binning envelope, and bins to the 5-year grid WITHIN each
    alignment subset. Alignment membership (``amask``) is FIXED across realisations
    (it depends on the recorded interval + ``ALIGN_RULE``, NOT the sampled date), so
    ``k_cc`` (aligned inscription count) and ``n_rows`` (total) are held CONSTANT —
    each inscription always deposits exactly one count into exactly one bin of its
    own subset.

    Parameters
    ----------
    df_unit : pandas.DataFrame
        The unit's filtered rows (columns ``nb`` / ``na`` from ``load_filtered_lire``).
    amask : (N,) bool array
        The FIXED per-inscription aligned indicator (``joint_lib.aligned_indicator``).
    rng : numpy.random.Generator
        Seeded generator (per-realisation seed handled by the caller).
    H : module
        ``h2_lib`` (for the envelope constants + bin edges).
    k_cc, n_rows : int
        The held-constant aligned total and grand total (asserted against below).

    Returns
    -------
    (y_aligned, y_nonaligned) : int64 arrays of length ``H.N_BINS``
        Per-bin point-date counts of the aligned / non-aligned subsets, with
        ``y_aligned.sum() == k_cc`` and ``y_aligned.sum() + y_nonaligned.sum() ==
        n_rows`` (the M2 invariant, re-asserted by the caller before set_data).
    """
    nb = df_unit["nb"].to_numpy().astype(float)
    na = df_unit["na"].to_numpy().astype(float)
    # Sample a point date per inscription. np.random.Generator.uniform draws on the
    # half-open [lo, hi); a degenerate interval (nb == na, year-precise) returns lo
    # exactly, which is the fixed [t, t] case the spec calls out.
    t = np.where(na > nb, rng.uniform(nb, na), nb)
    # Clip into the binning envelope so every inscription lands in a bin (keeps the
    # per-subset totals constant — the SPA convention clips to the envelope too).
    t = np.clip(t, H.ENV_START, H.ENV_END - 1e-9)
    # Bin to the 5-year grid (right-open bins; the final clip keeps t < ENV_END).
    bin_idx = np.floor((t - H.ENV_START) / H.BIN_SIZE).astype(int)
    bin_idx = np.clip(bin_idx, 0, H.N_BINS - 1)

    y_aligned = np.bincount(bin_idx[amask], minlength=H.N_BINS).astype("int64")
    y_nonaligned = np.bincount(bin_idx[~amask], minlength=H.N_BINS).astype("int64")
    return y_aligned, y_nonaligned


# =========================================================================== #
# Posterior-predictive dispersion check (SPEC §4 / §9.2).                       #
# =========================================================================== #
def multinomial_dispersion_check(idata, obs_aligned: np.ndarray,
                                 obs_nonaligned: np.ndarray) -> dict:
    """Bin-level over-dispersion of the PRIMARY fit vs the multinomial expectation.

    The prereg's stated trigger for preferring the DM (l.192) is bin-level
    over-dispersion of the multinomial primary. For each subset we compare the
    observed per-bin count to its posterior-predictive multinomial variance:
    ``Var_mult[y_b] = n · p_b · (1 − p_b)``, averaged over the posterior. The
    dispersion ratio is the mean squared Pearson residual

        D = mean_b[ (obs_b − E[y_b])² / Var_mult[y_b] ]

    which is ≈ 1 under an adequate multinomial and > 1 under over-dispersion (the
    DM-preferring regime). Reported per subset; NOT a gate (it informs the κ tuning
    and the model-comparison narrative).

    Parameters
    ----------
    idata : arviz.InferenceData
        The primary fit's posterior (must carry ``p_aligned`` / ``p_nonalign``).
    obs_aligned, obs_nonaligned : int arrays
        The observed per-bin subset counts.

    Returns
    -------
    dict with ``dispersion_ratio_aligned`` / ``dispersion_ratio_nonaligned`` and
    the subset totals used as the multinomial ``n``.
    """
    def _ratio(p_name: str, obs: np.ndarray) -> float:
        n_bins = obs.size
        p = idata.posterior[p_name].values.reshape(-1, n_bins)   # (draws, bins)
        n_total = int(obs.sum())
        e = n_total * p                                          # E[y_b] per draw
        var = n_total * p * (1.0 - p)                            # multinomial Var
        var = np.where(var > 0, var, np.nan)                     # guard zero-mass bins
        # Mean over draws of the squared Pearson residual, then over bins.
        resid2 = (obs[None, :] - e) ** 2 / var
        per_bin = np.nanmean(resid2, axis=0)
        return float(np.nanmean(per_bin))

    return {
        "dispersion_ratio_aligned": _ratio("p_aligned", obs_aligned),
        "dispersion_ratio_nonaligned": _ratio("p_nonalign", obs_nonaligned),
        "n_aligned": int(obs_aligned.sum()),
        "n_nonaligned": int(obs_nonaligned.sum()),
        "interpretation": "≈1 multinomial-adequate; >1 over-dispersed (DM-preferring)",
    }


# =========================================================================== #
# Sampling + convergence helpers (production config; SPEC §4 / §7).            #
# =========================================================================== #
def _sample(model, seed: int, H):
    """Sample one model with the production config (cores = 1); return InferenceData."""
    import pymc as pm
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                target_accept=H.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True)
    return idata


def _convergence(idata, convergence_pass) -> dict:
    """Convergence verdict on the SPEC §7 gate set (α + tier_weights ONLY).

    Gating on the wider monitored set (e.g. z_pgen) is stricter than the spec and
    noisy; the spec's stated gate is α + tier_weights (SPEC §7). Wider diagnostics
    are reported for the record but not gated on.
    """
    import arviz as az
    gate = az.summary(idata, var_names=["alpha", "tier_weights"], round_to="none")
    max_rhat = float(gate["r_hat"].max())
    min_ess = float(gate["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())
    return {"max_rhat": max_rhat, "min_ess_bulk": min_ess, "n_divergences": n_div,
            "convergence_pass": bool(convergence_pass(max_rhat, min_ess)),
            "gate_vars": ["alpha", "tier_weights"]}


def _alpha_summary(idata) -> dict:
    """α median + 95 % CI from one fit."""
    a = idata.posterior["alpha"].values.reshape(-1)
    lo, hi = (float(x) for x in np.percentile(a, [2.5, 97.5]))
    return {"alpha_median": float(np.median(a)), "alpha_ci_lo": lo,
            "alpha_ci_hi": hi, "ci_width": hi - lo}


# =========================================================================== #
# κ-tuning prior-predictive (SPEC §3.3 / §9.2).                                #
# =========================================================================== #
def kappa_prior_predictive(s_kappa: float, rng: np.random.Generator) -> dict:
    """Prior-predictive coverage of κ ~ HalfNormal(σ = s_kappa) over κ ∈ ~[10, 1e4].

    Draws κ from the half-normal prior and reports the fraction landing inside the
    target weakly-informative span ``KAPPA_PRIOR_SPAN`` plus the prior quantiles.
    A good ``S_KAPPA`` places substantial mass across the span without forcing
    overdispersion (κ too small) or pinning the multinomial limit (κ uniformly huge).
    NO fit — analytic prior draws only (cheap).
    """
    # HalfNormal(σ) = |Normal(0, σ)|.
    draws = np.abs(rng.normal(0.0, s_kappa, size=PRIOR_PRED_DRAWS))
    lo, hi = KAPPA_PRIOR_SPAN
    frac_in_span = float(np.mean((draws >= lo) & (draws <= hi)))
    q = np.percentile(draws, [5, 25, 50, 75, 95]).tolist()
    return {
        "s_kappa": s_kappa,
        "frac_in_target_span": frac_in_span,
        "target_span": list(KAPPA_PRIOR_SPAN),
        "kappa_quantiles_5_25_50_75_95": [float(x) for x in q],
    }


# =========================================================================== #
# Pilot driver (SPEC §9).                                                       #
# =========================================================================== #
def run_pilot(root: Path, out_dir: Path, n_mc: int = N_MC_PILOT) -> dict:
    """Execute the SPEC §9 pilot and return the full result dict.

    BUILD-ONLY note: this is the function the audited driver will run on sapphire
    after sign-off. It performs MCMC fits — do NOT call it as part of the build/audit.
    """
    import refit_lib as R
    import joint_lib as J
    import supp_lib as S
    import h2_lib as H
    from cell_lib import convergence_pass

    library_basis, _ = R.load_library_basis()
    theta_conv_ab, theta_gen_ab, _ = R.adopted_theta_priors()
    units = {u["name"]: u for u in R.enumerate_refit_units()}
    df = H.load_filtered_lire()
    latin = H.latin_provinces()

    report: dict = {
        "spec": "runs/2026-06-18-h2.1-supplementary-wave/SPEC.md §9",
        "mode": "PILOT",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "seed": PILOT_SEED,
        "sampling_config": {"draws": H.N_DRAWS, "tune": H.N_TUNE,
                            "chains": H.N_CHAINS, "cores": 1,
                            "target_accept": H.TARGET_ACCEPT},
        "n_mc_pilot": n_mc, "n_mc_production": N_MC_PRODUCTION,
        "model_comparison": {}, "kappa_tuning": {}, "aoristic_mc": {},
    }

    # ----------------------------------------------------------------------- #
    # (1) DM + NB model-comparison fits on the two pilot units + primary PPC    #
    #     dispersion (SPEC §9.2).                                                #
    # ----------------------------------------------------------------------- #
    for uname in PILOT_UNITS:
        unit = units[uname]
        sub = R.subset_for(df, unit, latin)
        data = R.build_unit_cc_data(sub)
        ya, yn = data["y_aligned"], data["y_nonaligned"]
        k, n_rows = data["k"], data["n_rows"]
        seed = PILOT_SEED + unit["unit_index"]
        unit_rec: dict = {"n_rows_eff": n_rows, "k_eff": k,
                          "n_rows_raw": data["n_rows_raw"]}

        # Primary (re-fit here for the PPC dispersion check; production re-uses the
        # refit's idata, but the pilot needs the posterior-predictive in hand).
        t0 = time.time()
        primary = J.build_model_cross_classified(
            ya, yn, k, n_rows, library_basis, theta_conv_ab, theta_gen_ab,
            pconv_mode="library")
        idata_primary = _sample(primary, seed, H)
        unit_rec["primary"] = {
            **_alpha_summary(idata_primary), "secs": round(time.time() - t0, 1),
            "convergence": _convergence(idata_primary, convergence_pass)}
        unit_rec["primary"]["dispersion"] = multinomial_dispersion_check(
            idata_primary, ya, yn)

        # DM fit (free κ at the default S_KAPPA; κ posterior recorded).
        t0 = time.time()
        dm = S.build_model_cc_dirichlet_multinomial(
            ya, yn, k, n_rows, library_basis, theta_conv_ab, theta_gen_ab,
            s_kappa=S_KAPPA_DEFAULT, pconv_mode="library")
        idata_dm = _sample(dm, seed, H)
        kappa = idata_dm.posterior["kappa"].values.reshape(-1)
        unit_rec["dm"] = {
            **_alpha_summary(idata_dm), "secs": round(time.time() - t0, 1),
            "convergence": _convergence(idata_dm, convergence_pass),
            "kappa_median": float(np.median(kappa)),
            "kappa_ci_lo": float(np.percentile(kappa, 2.5)),
            "kappa_ci_hi": float(np.percentile(kappa, 97.5))}

        # NB fit (free φ; dispersion posterior recorded).
        t0 = time.time()
        nb = S.build_model_cc_negbin(
            ya, yn, k, n_rows, library_basis, theta_conv_ab, theta_gen_ab,
            pconv_mode="library")
        idata_nb = _sample(nb, seed, H)
        phi = idata_nb.posterior["phi"].values.reshape(-1)
        unit_rec["nb"] = {
            **_alpha_summary(idata_nb), "secs": round(time.time() - t0, 1),
            "convergence": _convergence(idata_nb, convergence_pass),
            "phi_median": float(np.median(phi))}

        report["model_comparison"][uname] = unit_rec

    # ----------------------------------------------------------------------- #
    # (2) κ-tuning prior-predictive on empire (SPEC §3.3 / §9.2).               #
    # ----------------------------------------------------------------------- #
    rng = np.random.default_rng(PILOT_SEED)
    sweeps = [kappa_prior_predictive(s, rng) for s in S_KAPPA_CANDIDATES]
    # Choose the candidate maximising weakly-informative coverage of κ ∈ ~[10, 1e4].
    chosen = max(sweeps, key=lambda r: r["frac_in_target_span"])
    report["kappa_tuning"] = {
        "candidates": sweeps,
        "chosen_s_kappa": chosen["s_kappa"],
        "rationale": (
            "S_KAPPA chosen to maximise prior mass across κ ∈ ~[10, 1e4] "
            "(weakly informative, data-dominated; does not force overdispersion). "
            "Cross-checked against the empire DM κ posterior above — if the κ "
            "posterior sits well inside the prior bulk, the prior is data-dominated "
            "as required (SPEC §3.3). Re-confirm on the figure before sign-off."),
        "empire_dm_kappa_posterior": report["model_comparison"]
        .get("empire-aggregate", {}).get("dm", {}),
    }

    # ----------------------------------------------------------------------- #
    # (3) Aoristic-MC PILOT SUBSAMPLE on empire ONLY, N_MC = 10 (SPEC §9.3).     #
    #     PRIMARY only (the prereg aoristic-MC is the multinomial primary).      #
    # ----------------------------------------------------------------------- #
    import pymc as pm

    unit = units[AOMC_UNIT]
    sub = R.subset_for(df, unit, latin)
    amask = J.aligned_indicator(sub, rule=R.ALIGN_RULE)   # FIXED across realisations
    # Held-constant subset totals = the aoristic-MC's OWN point-date raw counts:
    # k_cc = aligned inscription count, n_rows = total inscriptions (each inscription
    # deposits exactly one count into one bin of its fixed subset). The model is built
    # ONCE on realisation 0 and re-used via set_data, so its pm.Data k_cc / n_rows
    # must match THESE totals (NOT refit_lib's aoristic-effective k / n_rows).
    k_cc = int(amask.sum())
    n_rows = int(len(sub))
    base_seed = PILOT_SEED + 10_000          # disjoint from the per-unit fit seeds

    aomc_alpha_pooled = []                    # pooled α draws across realisations
    per_real = []                             # per-realisation records
    model = None
    for r in range(n_mc):
        rng_r = np.random.default_rng(base_seed + r)
        ya_r, yn_r = aoristic_mc_realisation(sub, amask, rng_r, H, k_cc, n_rows)

        # M2 GUARD (audit): the DM/Multinomial silently returns -inf if a set_data
        # swap breaks sum(obs)==n, so assert the invariant BEFORE every swap.
        assert int(ya_r.sum()) == k_cc, (
            f"realisation {r}: y_aligned.sum()={int(ya_r.sum())} != k_cc={k_cc}")
        assert int(ya_r.sum() + yn_r.sum()) == n_rows, (
            f"realisation {r}: aligned+non-aligned={int(ya_r.sum() + yn_r.sum())} "
            f"!= n_rows={n_rows}")

        t0 = time.time()
        if model is None:
            # Build ONCE on realisation 0 (its data are already the held-constant
            # totals), then swap subsequent realisations in via set_data.
            model = J.build_model_cross_classified(
                ya_r, yn_r, k_cc, n_rows, library_basis, theta_conv_ab, theta_gen_ab,
                pconv_mode="library")
        else:
            with model:
                pm.set_data({"k_data": np.asarray(k_cc, dtype="int64"),
                            "y_al_data": ya_r, "y_non_data": yn_r})
        idata_r = _sample(model, base_seed + r, H)
        secs = time.time() - t0
        a_r = idata_r.posterior["alpha"].values.reshape(-1)
        aomc_alpha_pooled.append(a_r)
        per_real.append({
            "realisation": r, "secs": round(secs, 1),
            "alpha_median": float(np.median(a_r)),
            "convergence": _convergence(idata_r, convergence_pass)})

    pooled = np.concatenate(aomc_alpha_pooled)
    band_lo, band_hi = (float(x) for x in np.percentile(pooled, [2.5, 97.5]))
    cross_real_width = band_hi - band_lo
    # Primary single-SPA 95 % CI width (from the empire model-comparison primary fit)
    # for the SPEC §5 divergence-flag (cross-realisation range vs 1.5× primary width).
    primary_ci_width = (report["model_comparison"]
                        .get(AOMC_UNIT, {}).get("primary", {}).get("ci_width"))
    divergence_flag = (primary_ci_width is not None
                       and cross_real_width > 1.5 * primary_ci_width)

    mean_secs = float(np.mean([pr["secs"] for pr in per_real]))
    # Whole-wave cost projection (SPEC §8). Aoristic-MC dominates (~80 %): project it
    # from the measured per-realisation time, then gross up to the full wave.
    aomc_core_s_full = mean_secs * N_MC_PRODUCTION * N_UNITS_PRODUCTION
    aomc_core_hr_full = aomc_core_s_full / 3600.0
    whole_wave_core_hr = aomc_core_hr_full / 0.80   # aoristic-MC ≈ 80 % (SPEC §8)
    # Wall projection at the SPEC §8 parallelism (n_jobs 8–12; use 10 as midpoint).
    n_jobs = 10
    whole_wave_wall_hr = whole_wave_core_hr / n_jobs
    exceeds_ceiling = whole_wave_wall_hr > WALL_CEILING_HOURS

    report["aoristic_mc"] = {
        "unit": AOMC_UNIT, "n_mc_pilot": n_mc, "k_cc": k_cc, "n_rows": n_rows,
        "per_realisation": per_real,
        "mean_secs_per_realisation": round(mean_secs, 1),
        "cross_realisation_alpha_band_95": [band_lo, band_hi],
        "cross_realisation_width": cross_real_width,
        "primary_single_spa_ci_width": primary_ci_width,
        "divergence_flag": bool(divergence_flag),
        "divergence_rule": "cross-realisation 95% α-range > 1.5× primary 95% CI width",
        "projection": {
            "note": "PILOT N_MC=10 → projected to production N_MC=30 × 29 units",
            "aomc_core_hours_full": round(aomc_core_hr_full, 2),
            "whole_wave_core_hours": round(whole_wave_core_hr, 2),
            "n_jobs_assumed": n_jobs,
            "whole_wave_wall_hours": round(whole_wave_wall_hr, 2),
            "spec_budget_core_hours": 20, "spec_budget_wall_hours": "3–5",
            "wall_ceiling_hours": WALL_CEILING_HOURS,
            "exceeds_ceiling": bool(exceeds_ceiling),
            "halt_and_report": bool(exceeds_ceiling)},
    }

    # ----------------------------------------------------------------------- #
    # (4) Write outputs (JSON + PILOT-REPORT.md) — SPEC §9.4.                    #
    # ----------------------------------------------------------------------- #
    (out_dir / "pilot-results.json").write_text(json.dumps(report, indent=2))
    _write_pilot_report_md(out_dir / "PILOT-REPORT.md", report)
    return report


def _write_pilot_report_md(path: Path, report: dict) -> None:
    """Render the pilot report Markdown (SPEC §9.4 deliverable)."""
    aomc = report["aoristic_mc"]
    proj = aomc["projection"]
    kt = report["kappa_tuning"]
    lines: list[str] = []
    lines.append("# H2.1 supplementary wave — PILOT report")
    lines.append("")
    lines.append(f"- Generated (UTC): {report['generated_utc']}")
    lines.append(f"- Spec: {report['spec']}")
    lines.append(f"- Seed: {report['seed']}")
    sc = report["sampling_config"]
    lines.append(f"- Sampling: {sc['chains']} chains × ({sc['tune']} tune + "
                 f"{sc['draws']} draws), cores={sc['cores']}, "
                 f"target_accept={sc['target_accept']}")
    lines.append("")
    lines.append("## 1. DM + NB model comparison (two pilot units)")
    lines.append("")
    lines.append("| unit | family | α median | α 95% CI | conv | secs | κ / φ |")
    lines.append("|------|--------|----------|----------|------|------|-------|")
    for uname, rec in report["model_comparison"].items():
        for fam in ("primary", "dm", "nb"):
            f = rec.get(fam, {})
            if not f:
                continue
            extra = ""
            if fam == "dm":
                extra = f"κ={f.get('kappa_median', float('nan')):.1f}"
            elif fam == "nb":
                extra = f"φ={f.get('phi_median', float('nan')):.1f}"
            conv = "ok" if f.get("convergence", {}).get("convergence_pass") else "FAIL"
            lines.append(
                f"| {uname} | {fam} | {f.get('alpha_median', float('nan')):.4f} | "
                f"[{f.get('alpha_ci_lo', float('nan')):.4f}, "
                f"{f.get('alpha_ci_hi', float('nan')):.4f}] | {conv} | "
                f"{f.get('secs', float('nan'))} | {extra} |")
    lines.append("")
    lines.append("### Primary multinomial PPC dispersion (DM trigger, SPEC §4)")
    lines.append("")
    for uname, rec in report["model_comparison"].items():
        d = rec.get("primary", {}).get("dispersion", {})
        if d:
            lines.append(
                f"- **{uname}**: dispersion ratio aligned="
                f"{d['dispersion_ratio_aligned']:.3f}, non-aligned="
                f"{d['dispersion_ratio_nonaligned']:.3f} "
                f"({d['interpretation']}).")
    lines.append("")
    lines.append("## 2. κ-tuning (prior-predictive)")
    lines.append("")
    lines.append(f"- **Chosen S_KAPPA = {kt['chosen_s_kappa']:g}**")
    lines.append(f"- Rationale: {kt['rationale']}")
    lines.append("")
    lines.append("| S_KAPPA | frac in [10, 1e4] | κ quantiles (5/25/50/75/95) |")
    lines.append("|---------|-------------------|------------------------------|")
    for c in kt["candidates"]:
        q = c["kappa_quantiles_5_25_50_75_95"]
        qstr = " / ".join(f"{x:.0f}" for x in q)
        lines.append(f"| {c['s_kappa']:g} | {c['frac_in_target_span']:.3f} | {qstr} |")
    lines.append("")
    lines.append("## 3. Aoristic-MC PILOT SUBSAMPLE (empire only)")
    lines.append("")
    lines.append(f"- **PILOT N_MC = {aomc['n_mc_pilot']}** (NOT production "
                 f"N_MC = {report['n_mc_production']}).")
    lines.append(f"- Unit: {aomc['unit']}; k_cc={aomc['k_cc']}, n_rows={aomc['n_rows']}.")
    band = aomc["cross_realisation_alpha_band_95"]
    lines.append(f"- Cross-realisation 95% α band: [{band[0]:.4f}, {band[1]:.4f}] "
                 f"(width {aomc['cross_realisation_width']:.4f}).")
    lines.append(f"- Primary single-SPA 95% CI width: "
                 f"{aomc['primary_single_spa_ci_width']}.")
    lines.append(f"- **Divergence flag: {aomc['divergence_flag']}** "
                 f"({aomc['divergence_rule']}).")
    lines.append(f"- Mean wall per realisation: "
                 f"{aomc['mean_secs_per_realisation']} s.")
    lines.append("")
    lines.append("### Whole-wave cost projection (SPEC §8)")
    lines.append("")
    lines.append(f"- Aoristic-MC (N_MC={report['n_mc_production']} × "
                 f"{N_UNITS_PRODUCTION} units): "
                 f"~{proj['aomc_core_hours_full']} core-hr.")
    lines.append(f"- Whole wave (aoristic-MC ≈ 80%): "
                 f"~{proj['whole_wave_core_hours']} core-hr.")
    lines.append(f"- Projected wall at n_jobs={proj['n_jobs_assumed']}: "
                 f"~{proj['whole_wave_wall_hours']} h "
                 f"(SPEC §8 budget: {proj['spec_budget_core_hours']} core-hr / "
                 f"{proj['spec_budget_wall_hours']} h wall).")
    if proj["exceeds_ceiling"]:
        lines.append("")
        lines.append(f"> **HALT AND REPORT (SPEC §8):** projected wall "
                     f"~{proj['whole_wave_wall_hours']} h exceeds the "
                     f"~{proj['wall_ceiling_hours']} h ceiling. Do NOT silently "
                     f"reduce N_MC / draws / chains / unit count — Shawn decides "
                     f"(accept the longer run, stage it, or trim scope).")
    lines.append("")
    lines.append("## Sign-off checklist (SPEC §9)")
    lines.append("")
    lines.append("- [ ] Smoke gates pass (`smoke_supp.py`).")
    lines.append("- [ ] κ choice (above) — prior data-dominated, κ posterior inside bulk.")
    lines.append("- [ ] Measured cost vs the SPEC §8 budget (above).")
    lines.append("- [ ] No convergence surprises across the pilot fits.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Supplementary-wave orchestrator (pilot).")
    ap.add_argument("--pilot", action="store_true",
                    help="run the SPEC §9 pilot gate (the only implemented mode).")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                    help="repo root (parameterised; default the standing checkout path).")
    ap.add_argument("--n-mc", type=int, default=N_MC_PILOT,
                    help=f"aoristic-MC pilot realisations (default {N_MC_PILOT}; "
                         f"the PILOT subsample, NOT production {N_MC_PRODUCTION}).")
    args = ap.parse_args()

    _wire_paths(args.root)
    out_dir = (args.root / "runs" / "2026-06-18-h2.1-supplementary-wave" / "outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.pilot:
        ap.error("only --pilot is implemented; the full production sweep gates on "
                 "the signed-off pilot report (SPEC §9).")

    report = run_pilot(args.root, out_dir, n_mc=args.n_mc)
    aomc = report["aoristic_mc"]["projection"]
    print(f"\nPILOT complete — report → {out_dir / 'PILOT-REPORT.md'}")
    print(f"  chosen S_KAPPA = {report['kappa_tuning']['chosen_s_kappa']:g}")
    print(f"  projected whole-wave wall ~{aomc['whole_wave_wall_hours']} h "
          f"(ceiling {aomc['wall_ceiling_hours']} h); "
          f"halt-and-report={aomc['halt_and_report']}")


if __name__ == "__main__":
    main()
