#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_supp_production.py — supplementary-wave PRODUCTION orchestrator (SPEC §§4, 6, 7).
=====================================================================================

The production driver for the H2.1 supplementary wave
(``runs/2026-06-18-h2.1-supplementary-wave/SPEC.md``), across all 29 production units
(``refit_lib.enumerate_refit_units()``). It discharges the lodged items the pilot
(``run_supp.py --pilot``, signed off in ``outputs/PILOT-REPORT.md``) cleared for
production:

  * **C5 / C6** — model comparison. Per unit, fit the Dirichlet-multinomial
    (``supp_lib.build_model_cc_dirichlet_multinomial``) and the rescaled
    negative-binomial (``supp_lib.build_model_cc_negbin``) on the adopted
    cross-classified likelihood, re-using the lodged PRIMARY α (from
    ``runs/2026-06-13-cc-production-refit/``; NOT re-run) for the side-by-side.
    Reports (i) the α median + 95 % CI SIDE-BY-SIDE across primary / DM / NB (does
    the family move α?); (ii) the multinomial posterior-predictive dispersion check
    on the primary (is overdispersion warranted? — the prereg's stated DM/NB trigger,
    l.192); and (iii) each family's OWN within-family WAIC (descriptive, NOT
    cross-compared). Cross-family PSIS-LOO is NOT computed — it is methodologically
    inapplicable across the joint-multinomial primary/DM and the per-bin NegBin
    (audit fix C1; see BUILD-NOTES.md). → ``outputs/model-comparison.md`` + per-unit
    JSON.
  * **C11** — trapezoidal-aoristic sensitivity. Re-derive the trapezoidal SPA per
    unit + full empire (reusing the lodged 2026-05-17 apportionment), report (a) the
    input-level Pearson r vs the matched-convention uniform SPA, and (b) refit under
    the trapezoidal input and the output-level r on the deconvolved ``p_gen``. Material
    if either r < 0.95 → reported alongside. → ``outputs/trapezoidal.md``.
  * **H2.2 (C13)** — read-off, NO new MCMC. Per unit, the template-boundary step
    magnitude |Δ| in the corrected (posterior ``p_gen``, reused from the lodged
    posterior-draws) vs the uncorrected (raw SPA); % reduction; fraction of units
    meeting ≥ 50 %. → ``outputs/h2.2-boundary-steps.md``.
  * **H2.3 (C14)** — threshold convergence. Per unit, refit on the corpus filtered to
    ``date_range ≤ T`` for T ∈ {25, 50, 100, 200, 300}; pairwise Pearson r on the
    deconvolved ``p_gen`` across thresholds with an inscription-bootstrap CI; rule
    r ≥ 0.9; units below the reachability floor at tight T are CAVEATED, not failed.
    → ``outputs/h2.3-threshold-convergence.md``.
  * **H2.4 (C15)** — stratified-by-convention-class SPA. Per unit, the genuine-classed
    and convention-classed strata SPAs vs the model's deconvolved ``p_gen``, within an
    inscription-bootstrap sampling-error band (internal-consistency framing). →
    ``outputs/h2.4-stratified.md``.
  * **C16** — α descriptive read-off from the lodged refit summary. → folds into
    ``outputs/REPORT.md``.

**C10 (aoristic-MC) is NOT built here** — it is held pending a separate validity test
(``runs/2026-06-18-c10-validity-test/``), excluded from this driver's scope per the
build brief.

BUILD-ONLY at the time of writing: this driver is AUDITED before it is ever run
(standing rule). Running it performs MCMC and must happen on sapphire after sign-off.

Reuse (imported, never modified)
--------------------------------
* ``supp_lib`` — the two audited DM / NB builders (the only novel models).
* ``joint_lib`` — ``build_model_cross_classified`` (the primary, for the H2.3 and C11
  refits), ``aligned_indicator(rule="C")``.
* ``refit_lib`` — ``enumerate_refit_units``, ``build_unit_cc_data``,
  ``load_library_basis``, ``adopted_theta_priors``, ``ALIGN_RULE``, ``subset_for``.
* ``h2_lib`` — corpus loader, aoristic SPA, ``classify_family``, ``latin_provinces``,
  binning grid, and the sampling config (N_DRAWS / N_TUNE / N_CHAINS, cores = 1).
* ``cell_lib.convergence_pass`` — the SPEC §7 convergence verdict.
* ``supp_production_lib`` — the pure read-off helpers (C11 / H2.2 / H2.3-prep / H2.4 /
  C16 / bootstrap), importable without a PyMC stack.
* The lodged posterior ``p_gen`` draws (``runs/2026-06-13-cc-production-refit/outputs/
  posterior-draws/<safe-name>-pgen.npz``) — the corrected SPA for H2.2 / H2.4 and the
  uniform-input baseline for the C11 output-level r — reused, NOT re-fit.

The DM κ PRIOR is ``HalfNormal(σ = S_KAPPA = 5000)`` (audit fix C2; was 1e3). The pilot
DM fit returned κ ≈ 5,800 (data-dominated posterior); σ = 5000 places the weakly-informative
prior bulk around that without the downward pull the earlier σ = 1000 caused. κ itself is
sampled (free), not fixed — only its prior σ is pinned here. The value is FLAGGED FOR FINAL
HUMAN CONFIRM before the run — see BUILD-NOTES.md (C2).

Sampling config + infra
------------------------
Inherits the primary sampling config (``h2_lib`` N_DRAWS / N_TUNE / N_CHAINS, cores = 1)
and the cc-grid sapphire infra (``ProcessPoolExecutor`` spawn workers,
``max_tasks_per_child`` recycling, root-fs ``TMPDIR``, cgroup ``MemoryMax`` set by the
launch wrapper). Host / paths are PARAMETERISED (``--root``). Idata ``.nc`` are NOT
written (only per-unit JSON + the per-draw ``p_gen`` for the H2.3 refits, which are
gitignored ``.npz``). Resumable at unit granularity.

Usage (sapphire) — BUILD-ONLY until audited; do NOT run before sign-off::

    PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
        PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
        uv run python code/run_supp_production.py --n-jobs 10

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

# --------------------------------------------------------------------------- #
# Path wiring. Parameterised root (``--root``); default the standing checkout   #
# (identical on amd-tower and sapphire). The supplementary read-off helpers do  #
# the sibling-run sys.path insertion, so we reuse theirs to avoid drift.        #
# --------------------------------------------------------------------------- #
DEFAULT_ROOT = Path("/home/shawn/Code/inscriptions")
RUN_REL = Path("runs") / "2026-06-18-h2.1-supplementary-wave"

# Module-level handles populated by ``_wire`` (so spawn workers re-import cleanly).
H = J = R = S = SP = None
convergence_pass = None
LIBRARY_BASIS = THETA_CONV_AB = THETA_GEN_AB = None

# --------------------------------------------------------------------------- #
# Production constants (SPEC §3.3 / §4 / §5 / §6 / §7).                          #
# --------------------------------------------------------------------------- #
S_KAPPA = 5000                      # DM concentration prior σ (audit fix C2; was 1e3).
#                                     Pilot fit κ ≈ 5,800; σ = 5000 places the prior bulk
#                                     around it without the downward pull σ = 1000 caused.
#                                     FLAGGED FOR FINAL HUMAN CONFIRM before the run.
PROD_BASE_SEED = 20260618           # production seed; per-unit seed = base + unit_index
H2_3_SEED_OFFSET = 200_000          # disjoint seed block for the H2.3 threshold refits
BOOT_SEED_OFFSET = 400_000          # disjoint seed block for the bootstrap CIs
N_BOOT = 1000                       # bootstrap replicates (H2.3 r CI; H2.4 band)
REACHABILITY_FLOOR = 2000           # SPEC §6 worst-case N floor (caveat, not exclude)


def _wire(root: Path) -> None:
    """Import the shared modules + load the FIXED library / θ once (spawn-safe).

    Called at module import in each worker (via ``_worker``) and in ``main``. The
    library basis + adopted θ priors are the production identicals the primary,
    DM and NB all share (SPEC §3); loaded once and held at module level.
    """
    global H, J, R, S, SP, convergence_pass
    global LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB
    supp_code = root / RUN_REL / "code"
    if str(supp_code) not in sys.path:
        sys.path.insert(0, str(supp_code))
    import supp_production_lib as _SP
    _SP.wire_paths(root)                       # inserts h2/joint/refit/cell/spa-shape
    import h2_lib as _H
    import joint_lib as _J
    import refit_lib as _R
    import supp_lib as _S
    from cell_lib import convergence_pass as _cp
    H, J, R, S, SP = _H, _J, _R, _S, _SP
    convergence_pass = _cp
    LIBRARY_BASIS, _slabs = R.load_library_basis()
    THETA_CONV_AB, THETA_GEN_AB, _fit = R.adopted_theta_priors()


def _safe(name: str) -> str:
    """Filesystem-safe unit name — VERBATIM from ``run_refit._safe`` so the lodged
    posterior-draws ``.npz`` filenames map identically (the H2.2 / H2.4 reuse)."""
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


# =========================================================================== #
# Sampling + extraction helpers (production config; SPEC §4 / §7).             #
# =========================================================================== #
def _sample(model, seed: int, with_loglik: bool):
    """Sample one model with the production config (cores = 1); return InferenceData.

    ``with_loglik`` requests the pointwise log-likelihood group at sample time
    (``idata_kwargs={"log_likelihood": True}``) — used for each family's OWN
    WITHIN-family WAIC/LOO (descriptive context only; C1.iii). It is NOT used for any
    cross-family comparison: cross-family PSIS-LOO across these models is inapplicable
    (the primary/DM emit a joint multinomial log-lik, 3 points/unit; the NegBin emits
    per-bin, 161 points) — see ``fit_model_comparison`` and BUILD-NOTES.md (C1).
    """
    import pymc as pm
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                target_accept=H.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True,
                idata_kwargs={"log_likelihood": with_loglik})
    return idata


def _convergence(idata) -> dict[str, Any]:
    """Convergence verdict on the SPEC §7 gate set (α + tier_weights only).

    R̂ and bulk-ESS are computed on α + tier_weights (the spec's stated gate, §7);
    gating on the wider monitored set (z_pgen GRW increments) is stricter than the
    spec and noisy. Divergences are reported (benign-divergence treatment,
    Amendment 01), not zero-tolerance. For these NON-confirmatory items a failure is
    a per-unit limitation, surfaced — never silently dropped (SPEC §7).
    """
    import arviz as az
    gate = az.summary(idata, var_names=["alpha", "tier_weights"], round_to="none")
    max_rhat = float(gate["r_hat"].max())
    min_ess = float(gate["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())
    return {"max_rhat": max_rhat, "min_ess_bulk": min_ess, "n_divergences": n_div,
            "convergence_pass": bool(convergence_pass(max_rhat, min_ess)),
            "gate_vars": ["alpha", "tier_weights"]}


def _alpha_summary(idata) -> dict[str, float]:
    """α median + 95 % CI from one fit."""
    a = idata.posterior["alpha"].values.reshape(-1)
    lo, hi = (float(x) for x in np.percentile(a, [2.5, 97.5]))
    return {"alpha_median": float(np.median(a)), "alpha_ci_lo": lo,
            "alpha_ci_hi": hi, "ci_width": hi - lo}


def _pgen_median_norm(idata, n_bins: int) -> np.ndarray:
    """Posterior-median genuine SPA ``p_gen`` (length n_bins), normalised to sum 1."""
    pg = idata.posterior["p_gen"].values.reshape(-1, n_bins)
    med = np.median(pg, axis=0)
    return SP.normalise(med)


def _within_family_waic(idata) -> dict[str, Any]:
    """Each observed node's OWN WAIC — WITHIN-FAMILY descriptive context only (C1.iii).

    *** This is NOT a cross-family model-comparison number. ***  Cross-family PSIS-LOO
    across the supplementary families is INAPPLICABLE: the primary and the DM emit a
    JOINT-multinomial pointwise log-likelihood (the two subset multinomials score one
    log-lik point each → 3 points/unit incl. the Binomial), while the per-bin NegBin
    emits 1 + N_BINS + N_BINS ≈ 161 points/unit. ``az.compare`` cannot rank models
    whose pointwise log-likelihoods live on differently-shaped observation spaces —
    forcing a shared ``obs`` axis (as an earlier draft did) compares incommensurable
    quantities and is methodologically invalid. See BUILD-NOTES.md (C1).

    Instead, for DESCRIPTIVE context we report each family's OWN per-node WAIC,
    computed independently on that node (no pooling across families, no ranking):
    ``elpd_waic`` + ``p_waic`` for each of ``k_obs`` / ``y_al_obs`` / ``y_non_obs``.
    These are only ever interpreted within a single family (e.g. "the DM's y_al_obs
    elpd"), never across families. The model-comparison VERDICT is carried by the α
    side-by-side (does the family move α?) and the multinomial PPC dispersion ratio
    (is overdispersion warranted?), NOT by any cross-family information criterion.

    Returns ``{node: {elpd_waic, p_waic, n_obs} | {error: …}}`` for the three nodes;
    a node that cannot form a WAIC (e.g. a 1-point joint log-lik) is reported with its
    error string rather than silently dropped. Best-effort — never raises.
    """
    import arviz as az
    out: dict[str, Any] = {
        "note": ("WITHIN-FAMILY descriptive WAIC per observed node; NOT a cross-family "
                 "comparison (inapplicable across joint-multinomial vs per-bin NegBin "
                 "observation structures — see BUILD-NOTES.md C1).")}
    if not hasattr(idata, "log_likelihood"):
        out["error"] = "no log_likelihood group (model fit without with_loglik)"
        return out
    ll_vars = set(idata.log_likelihood.data_vars)
    for node in ("k_obs", "y_al_obs", "y_non_obs"):
        if node not in ll_vars:
            out[node] = {"error": "node absent from log_likelihood group"}
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")    # benign p_waic / scale notices
                w = az.waic(idata, var_name=node, scale="log")
            # n_obs = pointwise log-lik element count per draw = total / (chain·draw);
            # 1 for a joint-multinomial node, N_BINS for a per-bin NegBin node.
            da = idata.log_likelihood[node]
            per_draw = int(da.size // (da.sizes["chain"] * da.sizes["draw"]))
            out[node] = {
                "elpd_waic": float(getattr(w, "elpd_waic", float("nan"))),
                "p_waic": float(getattr(w, "p_waic", float("nan"))),
                "n_obs": per_draw}
        except Exception as exc:  # noqa: BLE001
            out[node] = {"error": repr(exc)[:160]}
    return out


# =========================================================================== #
# C5 / C6 — per-unit model comparison (DM + NB fits; primary reused).          #
# =========================================================================== #
def fit_model_comparison(unit: dict, data: dict) -> dict[str, Any]:
    """Fit DM + NB for one unit and assemble the C5 / C6 model-comparison record.

    Model-comparison deliverable (audit fix C1 — cross-family PSIS-LOO REMOVED as
    methodologically invalid). The prereg asks for the supplementaries "reported
    alongside for model-comparison cross-checks"; this is discharged by:

      (i)   the α median + 95 % CI SIDE-BY-SIDE across primary / DM / NB — the
            substantive question, "does the overdispersed family move the α verdict?"
            (primary α is the lodged value; DM / NB α from their fits here);
      (ii)  the multinomial POSTERIOR-PREDICTIVE DISPERSION check on the primary — the
            prereg's stated trigger (l.192) for preferring DM/NB: a bin-level dispersion
            ratio ≈ 1 says the multinomial is adequate (overdispersion NOT warranted),
            > 1 says it is; the adjudicator of whether DM/NB are even needed;
      (iii) each family's OWN per-node WAIC, reported WITHIN-FAMILY ONLY (descriptive
            context, NOT cross-compared) via ``_within_family_waic``.

    Cross-family PSIS-LOO is INAPPLICABLE here: the primary/DM emit a joint-multinomial
    pointwise log-lik (3 points/unit) and the NegBin emits per-bin (≈161 points/unit);
    ``az.compare`` cannot rank models on differently-shaped observation spaces. See
    BUILD-NOTES.md (C1). The model-comparison VERDICT is therefore (i) + (ii), NOT any
    information criterion.

    The PRIMARY α + CI come from the lodged refit summary (NOT re-run; SPEC §4 reuse).
    The primary is RE-FIT here ONLY for the posterior-predictive dispersion check (ii)
    and its own within-family WAIC (iii) — neither of which the lodged refit persisted.
    The re-fit uses the SAME per-unit seed as the refit (``REFIT_BASE_SEED +
    unit_index``) so it reproduces the lodged posterior to MCMC noise; its α is taken
    from the summary, so any tiny re-fit drift does not touch the reported α.

    Returns the per-unit JSON record: α side-by-side (primary from summary, DM, NB),
    the κ / φ posteriors, the dispersion ratios, per-family within-family WAIC, the
    α-movement verdict, and the per-fit convergence + timing.
    """
    ya, yn = data["y_aligned"], data["y_nonaligned"]
    k, n_rows = data["k"], data["n_rows"]
    n_bins = int(ya.size)
    rec: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "tier": unit["tier"],
        "unit_index": unit["unit_index"], "n_rows_eff": n_rows, "k_eff": k,
        "n_rows_raw": data["n_rows_raw"],
        "below_reachability_floor": bool(n_rows < REACHABILITY_FLOOR),
    }

    # --- lodged PRIMARY α (read-off; not re-run) for the side-by-side ---
    summ = {u["name"]: u for u in SP.load_refit_summary().get("units", [])}
    prim = summ.get(unit["name"], {})
    rec["primary_lodged"] = {
        "alpha_median": prim.get("alpha_median"),
        "alpha_ci_lo": prim.get("alpha_ci_lo"),
        "alpha_ci_hi": prim.get("alpha_ci_hi"),
        "convergence_pass": prim.get("convergence_pass"),
        "source": "runs/2026-06-13-cc-production-refit/outputs/refit-summary.json"}

    # --- primary RE-FIT (PPC dispersion + within-family WAIC only; α from lodged) ---
    t0 = time.time()
    primary = J.build_model_cross_classified(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        pconv_mode="library")
    seed_p = R.REFIT_BASE_SEED + unit["unit_index"]
    idata_p = _sample(primary, seed_p, with_loglik=True)
    rec["primary_refit"] = {
        **_alpha_summary(idata_p), "secs": round(time.time() - t0, 1),
        "convergence": _convergence(idata_p),
        "dispersion": _dispersion_check(idata_p, ya, yn),
        "within_family_waic": _within_family_waic(idata_p),
        "note": ("re-fit for the PPC dispersion check + within-family WAIC only; "
                 "reported α is primary_lodged")}

    # --- DM fit (free κ at the brief-pinned S_KAPPA) ---
    t0 = time.time()
    dm = S.build_model_cc_dirichlet_multinomial(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        s_kappa=S_KAPPA, pconv_mode="library")
    idata_dm = _sample(dm, PROD_BASE_SEED + unit["unit_index"], with_loglik=True)
    kappa = idata_dm.posterior["kappa"].values.reshape(-1)
    rec["dm"] = {
        **_alpha_summary(idata_dm), "secs": round(time.time() - t0, 1),
        "convergence": _convergence(idata_dm),
        "within_family_waic": _within_family_waic(idata_dm),
        "kappa_median": float(np.median(kappa)),
        "kappa_ci_lo": float(np.percentile(kappa, 2.5)),
        "kappa_ci_hi": float(np.percentile(kappa, 97.5)),
        "s_kappa_prior_sigma": S_KAPPA}

    # --- NB fit (free φ) ---
    t0 = time.time()
    nb = S.build_model_cc_negbin(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        pconv_mode="library")
    idata_nb = _sample(nb, PROD_BASE_SEED + unit["unit_index"], with_loglik=True)
    phi = idata_nb.posterior["phi"].values.reshape(-1)
    rec["nb"] = {
        **_alpha_summary(idata_nb), "secs": round(time.time() - t0, 1),
        "convergence": _convergence(idata_nb),
        "within_family_waic": _within_family_waic(idata_nb),
        "phi_median": float(np.median(phi)),
        "phi_ci_lo": float(np.percentile(phi, 2.5)),
        "phi_ci_hi": float(np.percentile(phi, 97.5))}

    # --- model-comparison VERDICT (C1): NOT a cross-family information criterion. ---
    # (i) does the overdispersed family MOVE the lodged primary α?  (ii) is
    # overdispersion even WARRANTED (primary multinomial PPC dispersion ratio vs 1)?
    # A small |Δα| + a dispersion ratio ≈ 1 ⇒ the multinomial is adequate and the α
    # attribution is family-robust (the supplementaries cross-check, don't overturn).
    am_p = rec["primary_lodged"].get("alpha_median")
    disp = rec["primary_refit"]["dispersion"]
    disp_finite = [v for v in (disp.get("dispersion_ratio_aligned"),
                               disp.get("dispersion_ratio_nonaligned"))
                   if isinstance(v, (int, float)) and np.isfinite(v)]
    disp_max = max(disp_finite) if disp_finite else None
    rec["alpha_verdict"] = {
        "delta_alpha_dm_vs_primary": (abs(rec["dm"]["alpha_median"] - am_p)
                                      if am_p is not None else None),
        "delta_alpha_nb_vs_primary": (abs(rec["nb"]["alpha_median"] - am_p)
                                      if am_p is not None else None),
        "primary_dispersion_ratio_max": disp_max,
        "overdispersion_warranted": (bool(disp_max > 1.0)
                                     if disp_max is not None else None),
        "interpretation": ("model-comparison VERDICT (C1; NOT cross-family LOO): the "
                           "supplementary families CROSS-CHECK the primary α — a small "
                           "|Δα| says the α attribution is family-robust; the primary "
                           "multinomial PPC dispersion ratio (≈1 vs >1) adjudicates "
                           "whether the DM/NB overdispersed families are warranted at "
                           "all. Each family's WAIC is within-family-only descriptive "
                           "context, never cross-compared.")}
    return rec


def _dispersion_check(idata, obs_aligned: np.ndarray,
                      obs_nonaligned: np.ndarray) -> dict[str, Any]:
    """Bin-level over-dispersion of the primary vs the multinomial expectation.

    The prereg's stated DM trigger (l.192) is bin-level over-dispersion of the
    multinomial primary. Per subset, the mean squared Pearson residual

        D = mean_b[ (obs_b − E[y_b])² / Var_mult[y_b] ],  Var_mult = n·p_b·(1 − p_b)

    averaged over the posterior — ≈ 1 under an adequate multinomial, > 1 under
    over-dispersion (the DM-preferring regime). Reported, not gated. (Identical
    formula to the pilot's ``multinomial_dispersion_check``; kept self-contained
    so the production driver does not depend on the pilot module.)
    """
    def _ratio(p_name: str, obs: np.ndarray) -> float:
        n_bins = obs.size
        p = idata.posterior[p_name].values.reshape(-1, n_bins)
        n_total = int(obs.sum())
        e = n_total * p
        var = n_total * p * (1.0 - p)
        var = np.where(var > 0, var, np.nan)
        resid2 = (obs[None, :] - e) ** 2 / var
        return float(np.nanmean(np.nanmean(resid2, axis=0)))

    return {
        "dispersion_ratio_aligned": _ratio("p_aligned", obs_aligned),
        "dispersion_ratio_nonaligned": _ratio("p_nonalign", obs_nonaligned),
        "n_aligned": int(obs_aligned.sum()), "n_nonaligned": int(obs_nonaligned.sum()),
        "interpretation": "≈1 multinomial-adequate; >1 over-dispersed (DM-preferring)"}


# =========================================================================== #
# C11 — trapezoidal-aoristic sensitivity (input-level r + refit output r).      #
# =========================================================================== #
def trapezoidal_unit(unit: dict, sub, posterior_draws_dir: Path) -> dict[str, Any]:
    """C11 for one unit: input-level r + trapezoidal-input refit output-level r.

    (a) INPUT-level: the trapezoidal SPA vs the matched-convention uniform SPA
        (both built with the lodged 2026-05-17 apportionment on the h2_lib grid;
        see ``supp_production_lib.trapezoidal_spa_on_h2_grid``) → Pearson r.
    (b) OUTPUT-level: refit the PRIMARY cross-classified model on a TRAPEZOIDAL-input
        observation (the two subset SPAs apportioned trapezoidally, largest-remainder
        rounded), extract the deconvolved ``p_gen``, and correlate it against the
        LODGED uniform-input ``p_gen`` (reused from the posterior-draws ``.npz`` — the
        primary is NOT re-fit on the uniform input). Material if either r < 0.95.

    The trapezoidal subset SPAs are built per alignment subset (rule C) so the
    cross-classified contrast is preserved; ``k`` and ``n_rows`` are the trapezoidal
    largest-remainder totals (the model's Binomial / Multinomial ``n`` must match its
    own observation, exactly as the uniform refit does).

    Convention (audit fix M2): the output-level refit uses
    ``SP.trapezoidal_spa_h2_convention`` — the lodged trapezoidal SHAPE on the EXACT
    ``h2_lib.aoristic_spa`` width/clip/drop convention the lodged uniform-input
    ``p_gen`` was fit under (interval ``[nb, na]``, width ``na − nb``, clipped to the
    envelope, rows with width ≤ 0 dropped). This makes the trapezoidal arm
    convention-matched to the uniform arm it is correlated against, so the output-level
    r isolates the trapezoidal-SHAPE effect rather than confounding it with a
    width/clip-convention change. (The INPUT-level r above is a separate, already-
    convention-matched trapezoid-vs-uniform comparison under the 2026-05-17 convention
    — left untouched.)
    """
    import empirical_spa_shape as T   # the lodged 2026-05-17 apportionment (on sys.path)

    nb_all = sub["nb"].to_numpy()
    na_all = sub["na"].to_numpy()

    # (a) input-level r on the full unit (matched convention).
    spa_uni = SP.uniform_spa_2026_05_17(nb_all, na_all, H, T)
    spa_trap = SP.trapezoidal_spa_on_h2_grid(nb_all, na_all, H, T)
    input_r = SP.pearson_r(spa_uni, spa_trap)

    rec: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "unit_index": unit["unit_index"],
        "input_level": {
            "pearson_r": input_r, "threshold": SP.C11_R_THRESHOLD,
            "material": bool(np.isfinite(input_r) and input_r < SP.C11_R_THRESHOLD)},
    }

    # (b) trapezoidal-input refit → output-level r vs the lodged uniform p_gen.
    # M2: the OUTPUT-level trapezoidal arm uses the h2_lib width/clip convention
    # (trapezoidal_spa_h2_convention) — the SAME convention the lodged uniform-input
    # p_gen (the comparison arm) was fit under — so the output-level r isolates the
    # trapezoidal-shape effect, not a width/clip-convention artefact.
    amask = J.aligned_indicator(sub, rule=R.ALIGN_RULE)
    al, non = sub.loc[amask], sub.loc[~amask]
    ya = H.largest_remainder(SP.trapezoidal_spa_h2_convention(
        al["nb"].to_numpy(), al["na"].to_numpy(), H, T))
    yn = H.largest_remainder(SP.trapezoidal_spa_h2_convention(
        non["nb"].to_numpy(), non["na"].to_numpy(), H, T))
    k = int(ya.sum())
    n_rows = int(k + int(yn.sum()))
    n_bins = int(ya.size)

    t0 = time.time()
    model = J.build_model_cross_classified(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        pconv_mode="library")
    idata = _sample(model, PROD_BASE_SEED + unit["unit_index"], with_loglik=False)
    pgen_trap = _pgen_median_norm(idata, n_bins)

    pgen_uni = _load_lodged_pgen_median(unit["name"], posterior_draws_dir, n_bins)
    out_r = SP.pearson_r(pgen_trap, pgen_uni) if pgen_uni is not None else float("nan")
    rec["output_level"] = {
        "pearson_r": out_r, "threshold": SP.C11_R_THRESHOLD,
        "material": bool(np.isfinite(out_r) and out_r < SP.C11_R_THRESHOLD),
        "uniform_pgen_source": ("lodged posterior-draws .npz (reused, not re-fit)"
                                if pgen_uni is not None else "MISSING — caveat"),
        "convergence": _convergence(idata), "secs": round(time.time() - t0, 1),
        "k_eff_trap": k, "n_rows_eff_trap": n_rows}
    rec["report_alongside"] = bool(rec["input_level"]["material"]
                                   or rec["output_level"]["material"])
    return rec


def _load_lodged_pgen_median(name: str, posterior_draws_dir: Path,
                             n_bins: int) -> np.ndarray | None:
    """Median uniform-input ``p_gen`` from the lodged posterior-draws ``.npz`` (reuse).

    Returns the per-draw-median, sum-1-normalised genuine SPA the lodged primary refit
    persisted (``p_gen`` group, shape (n_draws, n_bins)). ``None`` if the ``.npz`` is
    absent (caveated downstream — the H2.2 / C11 output-level leg needs it).
    """
    if posterior_draws_dir is None:
        return None
    p = posterior_draws_dir / f"{_safe(name)}-pgen.npz"
    if not p.exists():
        return None
    z = np.load(p, allow_pickle=True)
    pg = np.asarray(z["p_gen"], dtype=float).reshape(-1, n_bins)
    return SP.normalise(np.median(pg, axis=0))


# =========================================================================== #
# H2.2 (C13) — corrected-vs-uncorrected boundary-step read-off (NO MCMC).      #
# =========================================================================== #
def boundary_steps_unit(unit: dict, sub, posterior_draws_dir: Path) -> dict[str, Any]:
    """H2.2 for one unit: corrected (lodged p_gen) vs uncorrected (raw SPA) steps.

    Read-off only (SPEC §4): the uncorrected SPA is the unit's raw uniform aoristic
    SPA (``h2_lib.aoristic_spa``); the corrected SPA is the lodged posterior-median
    ``p_gen`` (reused from the posterior-draws ``.npz`` — the primary is NOT re-fit).
    Reports per-boundary step magnitudes, % reduction, and whether the unit meets the
    ≥ 50 % reduction target.
    """
    nb = sub["nb"].to_numpy()
    na = sub["na"].to_numpy()
    uncorrected = H.aoristic_spa(nb, na)
    corrected = _load_lodged_pgen_median(unit["name"], posterior_draws_dir, H.N_BINS)
    rec: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "unit_index": unit["unit_index"],
        "n_rows_raw": int(len(sub))}
    if corrected is None:
        rec["error"] = "lodged p_gen .npz missing; cannot read off corrected steps"
        return rec
    rec.update(SP.boundary_step_reduction(corrected, uncorrected, H))
    return rec


# =========================================================================== #
# H2.3 (C14) — threshold convergence (refits on date_range ≤ T).               #
# =========================================================================== #
def threshold_convergence_unit(unit: dict, sub) -> dict[str, Any]:
    """H2.3 for one unit: refit at each date_range ≤ T, pairwise p_gen r + boot CI.

    For each T ∈ {25, 50, 100, 200, 300}: filter the unit's rows to date_range ≤ T,
    rebuild the cross-classified observation (rule-C subsets, largest-remainder),
    refit the PRIMARY, and extract the deconvolved ``p_gen``. Then compute the
    pairwise Pearson r between every threshold pair's ``p_gen`` (rule r ≥ 0.9) and an
    inscription-bootstrap CI on the r between adjacent thresholds. Units that drop
    below the reachability floor at a tight T are CAVEATED (the row is kept, flagged),
    NOT failed (SPEC §6).
    """
    rng = np.random.default_rng(PROD_BASE_SEED + BOOT_SEED_OFFSET + unit["unit_index"])
    rec: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "unit_index": unit["unit_index"],
        "thresholds": list(SP.H2_3_THRESHOLDS), "per_threshold": {}}

    pgen_by_T: dict[int, np.ndarray] = {}
    rows_by_T: dict[int, Any] = {}
    for T in SP.H2_3_THRESHOLDS:
        sub_T = SP.filter_by_date_range(sub, T)
        rows_by_T[T] = sub_T
        n_raw = int(len(sub_T))
        tinfo: dict[str, Any] = {"n_rows_raw": n_raw,
                                 "below_reachability_floor": bool(n_raw < REACHABILITY_FLOOR)}
        if n_raw == 0:
            tinfo["error"] = "empty after filter"
            rec["per_threshold"][str(T)] = tinfo
            continue
        amask = J.aligned_indicator(sub_T, rule=R.ALIGN_RULE)
        al, non = sub_T.loc[amask], sub_T.loc[~amask]
        ya = H.largest_remainder(H.aoristic_spa(al["nb"].to_numpy(), al["na"].to_numpy()))
        yn = H.largest_remainder(H.aoristic_spa(non["nb"].to_numpy(), non["na"].to_numpy()))
        k = int(ya.sum())
        n_rows = int(k + int(yn.sum()))
        if k <= 0 or (n_rows - k) <= 0:
            tinfo["error"] = "one alignment subset empty after filter (no cc contrast)"
            rec["per_threshold"][str(T)] = tinfo
            continue
        n_bins = int(ya.size)
        t0 = time.time()
        model = J.build_model_cross_classified(
            ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
            pconv_mode="library")
        seed = PROD_BASE_SEED + H2_3_SEED_OFFSET + unit["unit_index"] * 10 + _t_idx(T)
        idata = _sample(model, seed, with_loglik=False)
        pgen_by_T[T] = _pgen_median_norm(idata, n_bins)
        tinfo.update({**_alpha_summary(idata), "k_eff": k, "n_rows_eff": n_rows,
                      "convergence": _convergence(idata), "secs": round(time.time() - t0, 1)})
        rec["per_threshold"][str(T)] = tinfo

    # Pairwise p_gen Pearson r across thresholds (rule r ≥ 0.9).
    ts = sorted(pgen_by_T)
    pairwise: list[dict[str, Any]] = []
    for i in range(len(ts)):
        for jx in range(i + 1, len(ts)):
            ti, tj = ts[i], ts[jx]
            r = SP.pearson_r(pgen_by_T[ti], pgen_by_T[tj])
            pairwise.append({"T_a": ti, "T_b": tj, "pearson_r": r,
                             "meets_rule": bool(np.isfinite(r) and r >= SP.H2_3_R_THRESHOLD)})
    rec["pairwise_r"] = pairwise
    rec["rule_r"] = SP.H2_3_R_THRESHOLD
    finite = [p["pearson_r"] for p in pairwise if np.isfinite(p["pearson_r"])]
    rec["min_pairwise_r"] = float(min(finite)) if finite else float("nan")
    rec["all_pairs_meet_rule"] = bool(pairwise) and all(
        p["meets_rule"] for p in pairwise if np.isfinite(p["pearson_r"]))

    # Bootstrap CI on the r between ADJACENT thresholds (the tightest pair test).
    boot: list[dict[str, Any]] = []
    for i in range(len(ts) - 1):
        ta, tb = ts[i], ts[i + 1]
        sub_a, sub_b = rows_by_T[ta], rows_by_T[tb]

        def _builder(keys, _sa=sub_a, _sb=sub_b):
            # Resample the WIDER threshold's rows (sub_b ⊇ sub_a as date filters
            # nest); the tighter SPA is the date_range ≤ ta subset of the SAME
            # resample, so both SPAs share the bootstrap draw (a paired resample).
            res = _sb.iloc[keys]
            res_a = res.loc[res["date_range"] <= ta]
            spa_a = SP.normalise(H.aoristic_spa(res_a["nb"].to_numpy(), res_a["na"].to_numpy()))
            spa_b = SP.normalise(H.aoristic_spa(res["nb"].to_numpy(), res["na"].to_numpy()))
            return spa_a, spa_b

        ci = SP.bootstrap_pearson_ci(
            np.arange(len(sub_b)), _builder, N_BOOT, rng)
        boot.append({"T_a": ta, "T_b": tb, **ci})
    rec["bootstrap_adjacent_r"] = boot
    rec["caveated_below_floor"] = bool(any(
        v.get("below_reachability_floor") for v in rec["per_threshold"].values()))
    return rec


def _t_idx(T: int) -> int:
    """Index of T within the threshold tuple (for a collision-free per-fit seed)."""
    return SP.H2_3_THRESHOLDS.index(T)


# =========================================================================== #
# H2.4 (C15) — stratified-by-class SPA vs the deconvolved p_gen (NO MCMC).      #
# =========================================================================== #
def stratified_unit(unit: dict, sub, posterior_draws_dir: Path) -> dict[str, Any]:
    """H2.4 for one unit: genuine- and convention-classed strata vs lodged p_gen.

    Read-off (SPEC §4): build the genuine-classed (Tight) and convention-classed
    (F1_round + F3_periodic) strata SPAs with inscription-bootstrap sampling-error
    bands, and compare the model's deconvolved ``p_gen`` (lodged posterior median,
    reused) against each via (i) the fraction of bins where ``p_gen`` falls inside
    the stratum band, and (ii) the point Pearson r. Internal-consistency framing —
    the genuine-classed stratum should TRACK the deconvolved genuine SPA; the
    convention-classed stratum is the contrast.

    CAVEAT (audit fix M1 — reported, computation UNCHANGED): the stratum SPAs are
    built with ``h2_lib.aoristic_spa``, which drops rows with ``width = na − nb ≤ 0``
    — i.e. the YEAR-PRECISE rows (``na == nb``, a zero-width interval). This is
    CONSISTENT with how the primary ``p_gen`` was fit (the same drop, so the
    comparison is valid and apples-to-apples), but it means the genuine-classed
    stratum UNDER-REPRESENTS exactly the date-honest year-precise inscriptions this
    H2.4 internal-consistency check is most about. We report the count of dropped
    year-precise rows per stratum (``n_year_precise_dropped``) so the
    under-representation is visible; we do NOT change the computation (changing it
    would break the consistency with the lodged primary). See BUILD-NOTES.md (M1).
    """
    rng = np.random.default_rng(
        PROD_BASE_SEED + BOOT_SEED_OFFSET + 1 + unit["unit_index"])
    pgen = _load_lodged_pgen_median(unit["name"], posterior_draws_dir, H.N_BINS)
    rec: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "unit_index": unit["unit_index"],
        "n_rows_raw": int(len(sub)),
        "m1_caveat": ("genuine/convention strata SPAs drop year-precise (na==nb, "
                      "width≤0) rows via h2_lib.aoristic_spa — consistent with the "
                      "lodged primary p_gen fit, but under-represents the date-honest "
                      "year-precise inscriptions; see n_year_precise_dropped per "
                      "stratum and BUILD-NOTES.md M1.")}
    if pgen is None:
        rec["error"] = "lodged p_gen .npz missing; cannot compare strata to p_gen"
        return rec
    # M1: count the year-precise (na==nb) rows in each stratum that h2_lib.aoristic_spa
    # silently drops (width≤0), so the under-representation is reported per stratum.
    # (Read-off only — the stratum SPA / band computation below is UNCHANGED.)
    fam_all = H.classify_family(sub)
    nb_all = sub["nb"].to_numpy()
    na_all = sub["na"].to_numpy()
    year_precise = (na_all - nb_all) <= 0
    for label, fams in (("genuine_classed", SP.GENUINE_FAMILIES),
                        ("convention_classed", SP.CONVENTION_FAMILIES)):
        band = SP.stratified_bootstrap_band(sub, H, fams, N_BOOT, rng)
        spa = np.asarray(band["spa"], dtype=float)
        frac_in = SP.fraction_in_band(pgen, np.asarray(band["band_lo"], dtype=float),
                                      np.asarray(band["band_hi"], dtype=float))
        in_stratum = np.isin(fam_all, list(fams))
        n_dropped = int((in_stratum & year_precise).sum())
        rec[label] = {
            "families": list(fams), "n_rows": band["n_rows"],
            "n_year_precise_dropped": n_dropped,         # M1 caveat (width≤0 → dropped)
            "pearson_r_vs_pgen": SP.pearson_r(spa, pgen),
            "frac_pgen_in_band": frac_in, "n_boot": band["n_boot"],
            "spa": band["spa"], "band_lo": band["band_lo"], "band_hi": band["band_hi"]}
    return rec


# =========================================================================== #
# JSON helper.                                                                  #
# =========================================================================== #
def _jsonable(x: Any) -> Any:
    """Coerce numpy / pandas scalars to plain Python for ``json.dumps``."""
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    try:
        return float(x)
    except (TypeError, ValueError):
        return str(x)


# =========================================================================== #
# Per-unit worker (MCMC items: C5/C6 + C11 + H2.3; resumable).                 #
# =========================================================================== #
def _worker(unit: dict, root_str: str, draws_dir_str: str | None) -> tuple[str, bool]:
    """One unit's MCMC-bearing supplementary items, written to a per-unit JSON.

    Runs C5 / C6 (model comparison), C11 (trapezoidal refit), and H2.3 (threshold
    refits) — the items that fit. The read-off items that need only the lodged
    posterior (H2.2, H2.4) are ALSO assembled here (so a unit's JSON is
    self-contained), since they are cheap and need the same loaded corpus. The
    aoristic-MC (C10) is NOT run — it is held (out of scope for this driver).

    Resumable: a unit whose JSON already carries ``model_comparison`` is skipped by
    ``_unit_done``.
    """
    root = Path(root_str)
    _wire(root)
    draws_dir = Path(draws_dir_str) if draws_dir_str else None
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    sub = R.subset_for(df, unit, latin)
    data = R.build_unit_cc_data(sub)

    t0 = time.time()
    out: dict[str, Any] = {
        "name": unit["name"], "frame": unit["frame"], "tier": unit["tier"],
        "unit_index": unit["unit_index"],
        "model_comparison": fit_model_comparison(unit, data),   # C5 / C6
        "trapezoidal": trapezoidal_unit(unit, sub, draws_dir),  # C11
        "threshold_convergence": threshold_convergence_unit(unit, sub),  # H2.3
        "boundary_steps": boundary_steps_unit(unit, sub, draws_dir),     # H2.2 (read-off)
        "stratified": stratified_unit(unit, sub, draws_dir),             # H2.4 (read-off)
    }
    out["total_secs"] = round(time.time() - t0, 1)

    units_dir = root / RUN_REL / "outputs" / "units"
    units_dir.mkdir(parents=True, exist_ok=True)
    tmp = units_dir / f"{_safe(unit['name'])}.json.tmp"
    final = units_dir / f"{_safe(unit['name'])}.json"
    tmp.write_text(json.dumps(out, indent=1, default=_jsonable))
    os.replace(tmp, final)
    gc.collect()
    conv = out["model_comparison"].get("dm", {}).get("convergence", {}).get(
        "convergence_pass", False)
    return unit["name"], bool(conv)


def _unit_done(unit: dict, root: Path) -> bool:
    """A unit is done iff its JSON exists and carries a ``model_comparison`` block."""
    p = root / RUN_REL / "outputs" / "units" / f"{_safe(unit['name'])}.json"
    if not p.exists():
        return False
    try:
        d = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return "model_comparison" in d


# =========================================================================== #
# Deliverable writers (the §11 Markdown outputs + per-item aggregation).        #
# =========================================================================== #
def _load_units(root: Path) -> list[dict[str, Any]]:
    """Load every per-unit JSON (in enumeration order)."""
    units = R.enumerate_refit_units()
    out: list[dict[str, Any]] = []
    for u in units:
        p = root / RUN_REL / "outputs" / "units" / f"{_safe(u['name'])}.json"
        if p.exists():
            out.append(json.loads(p.read_text()))
    return out


def write_deliverables(root: Path) -> None:
    """Assemble every per-item Markdown deliverable + REPORT.md from the unit JSONs."""
    out_dir = root / RUN_REL / "outputs"
    recs = _load_units(root)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    _write_model_comparison(out_dir / "model-comparison.md", recs, stamp)
    _write_trapezoidal(out_dir / "trapezoidal.md", recs, stamp)
    _write_h22(out_dir / "h2.2-boundary-steps.md", recs, stamp)
    _write_h23(out_dir / "h2.3-threshold-convergence.md", recs, stamp)
    _write_h24(out_dir / "h2.4-stratified.md", recs, stamp)
    _write_report(out_dir / "REPORT.md", recs, root, stamp)


def _hdr(title: str, stamp: str, spec_ref: str) -> list[str]:
    """Standard deliverable header lines."""
    return [f"# {title}", "",
            f"- Generated (UTC): {stamp}",
            f"- Spec: {RUN_REL}/SPEC.md {spec_ref}",
            f"- Scope: 28 + Italia-excl-Rome = 29 production units; C10 EXCLUDED (held).",
            f"- Sampling: {H.N_CHAINS} chains × ({H.N_TUNE} tune + {H.N_DRAWS} draws), "
            f"cores=1, target_accept={H.TARGET_ACCEPT}.", ""]


def _write_model_comparison(path: Path, recs: list[dict], stamp: str) -> None:
    """C5 / C6 deliverable — α side-by-side + multinomial PPC dispersion (C1).

    Cross-family PSIS-LOO is NOT reported: it is methodologically inapplicable across
    the joint-multinomial primary/DM and the per-bin NegBin (differently-shaped
    observation spaces; see BUILD-NOTES.md C1). The deliverable is the comparison the
    prereg actually asks for — α side-by-side (does the family move α?) + the primary
    multinomial PPC dispersion ratio (is overdispersion warranted?).
    """
    lines = _hdr("C5 / C6 — model comparison (Dirichlet-multinomial + negative-binomial)",
                 stamp, "§4 (C5/C6)")
    lines += ["**Method note (C1):** cross-family PSIS-LOO is NOT reported — it is "
              "inapplicable across the joint-multinomial (primary, DM; 3 log-lik "
              "points/unit) and per-bin negative-binomial (≈161 points/unit) "
              "observation structures. The model-comparison verdict is the α "
              "side-by-side (does the family move α?) plus the primary multinomial "
              "posterior-predictive dispersion ratio (is overdispersion warranted?). "
              "Each family's own WAIC is in the per-unit JSON, within-family-only.", "",
              "## α side-by-side (median, 95 % CI) — does the family move α?", "",
              "| unit | primary (lodged) | DM | NB | |Δα| DM | |Δα| NB |",
              "|------|------------------|----|----|--------|--------|"]
    for r in recs:
        mc = r.get("model_comparison", {})
        if not mc:
            continue
        p = mc.get("primary_lodged", {})
        dm, nb = mc.get("dm", {}), mc.get("nb", {})
        v = mc.get("alpha_verdict", {})
        prim_ci = _fmt_ci(p.get("alpha_median"), p.get("alpha_ci_lo"), p.get("alpha_ci_hi"))
        lines.append(
            f"| {r['name']} | {prim_ci} "
            f"| {_fmt_ci(dm.get('alpha_median'), dm.get('alpha_ci_lo'), dm.get('alpha_ci_hi'))} "
            f"| {_fmt_ci(nb.get('alpha_median'), nb.get('alpha_ci_lo'), nb.get('alpha_ci_hi'))} "
            f"| {_fmt(v.get('delta_alpha_dm_vs_primary'))} "
            f"| {_fmt(v.get('delta_alpha_nb_vs_primary'))} |")
    lines += ["", "## DM κ / NB φ posteriors + multinomial PPC dispersion "
              "(overdispersion warranted?)", "",
              "| unit | κ median [95% CI] | φ median | disp. aligned | disp. non-al | "
              "overdisp.? |",
              "|------|-------------------|----------|---------------|--------------|"
              "------------|"]
    for r in recs:
        mc = r.get("model_comparison", {})
        if not mc:
            continue
        dm, nb = mc.get("dm", {}), mc.get("nb", {})
        d = mc.get("primary_refit", {}).get("dispersion", {})
        v = mc.get("alpha_verdict", {})
        ow = v.get("overdispersion_warranted")
        ow_str = "YES" if ow else ("no" if ow is not None else "—")
        lines.append(
            f"| {r['name']} | {_fmt(dm.get('kappa_median'))} "
            f"[{_fmt(dm.get('kappa_ci_lo'))}, {_fmt(dm.get('kappa_ci_hi'))}] "
            f"| {_fmt(nb.get('phi_median'))} | {_fmt(d.get('dispersion_ratio_aligned'))} "
            f"| {_fmt(d.get('dispersion_ratio_nonaligned'))} | {ow_str} |")
    lines += ["", f"- DM κ prior: HalfNormal(σ = S_KAPPA = {S_KAPPA:g}) — pilot κ ≈ 5,800; "
              "σ = 5000 centres the weakly-informative prior near it (audit fix C2; "
              "see BUILD-NOTES.md).",
              "- Dispersion ratio ≈ 1 ⇒ the multinomial primary is adequate "
              "(overdispersion NOT warranted); > 1 ⇒ DM/NB preferred. This is the "
              "prereg's stated DM/NB trigger (l.192) and the model-comparison "
              "adjudicator — NOT a cross-family information criterion (C1).",
              "- Per-family within-family WAIC (descriptive, NOT cross-compared) is in "
              "the per-unit JSON (outputs/units/, `*.model_comparison.{primary_refit,"
              "dm,nb}.within_family_waic`).", ""]
    path.write_text("\n".join(lines) + "\n")


def _write_trapezoidal(path: Path, recs: list[dict], stamp: str) -> None:
    """C11 deliverable — input-level + output-level trapezoidal r."""
    lines = _hdr("C11 — trapezoidal-aoristic sensitivity", stamp, "§4 (C11)")
    lines += ["Material if either r < 0.95 (input-level uniform-vs-trapezoid SPA, OR "
              "output-level deconvolved-p_gen r); reported alongside if so. Empire is "
              "pre-triggered at the input level (r = 0.94, 2026-05-17).", "",
              "| unit | input r | output r | report-alongside? |",
              "|------|---------|----------|-------------------|"]
    n_material = 0
    for r in recs:
        t = r.get("trapezoidal", {})
        if not t:
            continue
        ir = t.get("input_level", {}).get("pearson_r")
        orr = t.get("output_level", {}).get("pearson_r")
        ra = t.get("report_alongside")
        if ra:
            n_material += 1
        lines.append(f"| {r['name']} | {_fmt(ir, 4)} | {_fmt(orr, 4)} | "
                     f"{'YES' if ra else 'no'} |")
    lines += ["", f"- Units flagged report-alongside: {n_material} / {len(recs)}.",
              "- Trapezoidal apportionment reused from "
              "runs/2026-05-17-empirical-spa-shape/code/empirical_spa_shape.py "
              "(imported; original untouched).",
              "- **Convention (M2):** the INPUT-level r matches trapezoid vs uniform "
              "under the 2026-05-17 inclusive-Roman convention "
              "(`trapezoidal_spa_on_h2_grid` vs `uniform_spa_2026_05_17`), isolating "
              "the mass SHAPE. The OUTPUT-level r matches the trapezoidal refit to the "
              "lodged uniform-input `p_gen` under the `h2_lib.aoristic_spa` width/clip "
              "convention (`trapezoidal_spa_h2_convention`), so it too isolates the "
              "shape effect rather than a width/clip artefact. See BUILD-NOTES.md (M2).",
              ""]
    path.write_text("\n".join(lines) + "\n")


def _write_h22(path: Path, recs: list[dict], stamp: str) -> None:
    """H2.2 deliverable — boundary-step % reduction; fraction meeting ≥ 50 %."""
    lines = _hdr("H2.2 (C13) — corrected-SPA boundary-step reduction", stamp, "§4 (H2.2)")
    lines += ["Step |Δ| at BC/AD 0, AD 100, 200, 300: corrected (posterior p_gen, "
              "lodged) vs uncorrected (raw SPA), normalised. Target: ≥ 50 % mean "
              "reduction per unit.", "",
              "| unit | mean % reduction | meets ≥50%? | per-boundary % (0/100/200/300) |",
              "|------|------------------|-------------|-------------------------------|"]
    n_meet = n_have = 0
    for r in recs:
        b = r.get("boundary_steps", {})
        if not b or "error" in b:
            lines.append(f"| {r['name']} | — | — | {b.get('error', 'n/a')} |")
            continue
        n_have += 1
        if b.get("meets_50pct"):
            n_meet += 1
        pb = b.get("per_boundary", {})
        per = " / ".join(_fmt_pct(pb.get(str(y), {}).get("pct_reduction"))
                         for y in (0, 100, 200, 300))
        lines.append(f"| {r['name']} | {_fmt_pct(b.get('mean_pct_reduction'))} | "
                     f"{'YES' if b.get('meets_50pct') else 'no'} | {per} |")
    frac = (n_meet / n_have) if n_have else float("nan")
    lines += ["", f"- Fraction of units meeting ≥ 50 % reduction: {n_meet}/{n_have} "
              f"({frac:.0%})." if n_have else "- No units with a corrected SPA available.",
              ""]
    path.write_text("\n".join(lines) + "\n")


def _write_h23(path: Path, recs: list[dict], stamp: str) -> None:
    """H2.3 deliverable — pairwise threshold r + bootstrap CI; reachability caveats."""
    lines = _hdr("H2.3 (C14) — threshold convergence (date_range ≤ T)", stamp, "§4 (H2.3)")
    lines += ["Pairwise Pearson r on the deconvolved p_gen across T ∈ "
              "{25, 50, 100, 200, 300}; rule r ≥ 0.9. Units below the reachability "
              "floor (N < 2,000) at tight T are CAVEATED, not failed.", "",
              "| unit | min pairwise r | all pairs ≥0.9? | caveated (floor)? |",
              "|------|----------------|-----------------|-------------------|"]
    n_pass = n_have = 0
    for r in recs:
        h = r.get("threshold_convergence", {})
        if not h:
            continue
        n_have += 1
        if h.get("all_pairs_meet_rule"):
            n_pass += 1
        lines.append(f"| {r['name']} | {_fmt(h.get('min_pairwise_r'), 3)} | "
                     f"{'YES' if h.get('all_pairs_meet_rule') else 'no'} | "
                     f"{'YES' if h.get('caveated_below_floor') else 'no'} |")
    lines += ["", f"- Units meeting r ≥ 0.9 on all threshold pairs: {n_pass}/{n_have}.",
              "- Per-threshold α / convergence and adjacent-threshold bootstrap r CIs "
              "are in the per-unit JSON (outputs/units/).", ""]
    path.write_text("\n".join(lines) + "\n")


def _write_h24(path: Path, recs: list[dict], stamp: str) -> None:
    """H2.4 deliverable — stratified-class SPA vs p_gen agreement."""
    lines = _hdr("H2.4 (C15) — stratified-by-class SPA vs deconvolved p_gen", stamp,
                 "§4 (H2.4)")
    lines += ["Internal-consistency check (NOT independent validation): the genuine-"
              "classed (Tight) and convention-classed (F1_round + F3_periodic) strata "
              "SPAs vs the model p_gen, within an inscription-bootstrap band.", "",
              "**CAVEAT (M1):** the stratum SPAs are built with `h2_lib.aoristic_spa`, "
              "which drops year-precise rows (`na == nb`, width ≤ 0). This is CONSISTENT "
              "with how the lodged primary `p_gen` was fit (so the comparison is valid), "
              "but it UNDER-REPRESENTS exactly the date-honest year-precise inscriptions "
              "this check is about — the `genuine drop` column counts the dropped rows "
              "per genuine stratum. See BUILD-NOTES.md (M1).", "",
              "| unit | genuine r | genuine frac-in-band | genuine drop | conv r | "
              "conv frac-in-band |",
              "|------|-----------|----------------------|--------------|--------|"
              "-------------------|"]
    for r in recs:
        s = r.get("stratified", {})
        if not s or "error" in s:
            lines.append(f"| {r['name']} | — | — | — | — | {s.get('error', 'n/a')} |")
            continue
        g, c = s.get("genuine_classed", {}), s.get("convention_classed", {})
        lines.append(f"| {r['name']} | {_fmt(g.get('pearson_r_vs_pgen'), 3)} | "
                     f"{_fmt_pct(g.get('frac_pgen_in_band'))} | "
                     f"{g.get('n_year_precise_dropped', '—')} | "
                     f"{_fmt(c.get('pearson_r_vs_pgen'), 3)} | "
                     f"{_fmt_pct(c.get('frac_pgen_in_band'))} |")
    lines += ["", "- The genuine-classed stratum should TRACK the deconvolved genuine "
              "SPA (high r, high frac-in-band); the convention-classed stratum is the "
              "contrast. Full per-bin bands are in the per-unit JSON.",
              "- `genuine drop` = year-precise (na==nb) rows dropped from the genuine "
              "stratum by the width≤0 rule (M1); a large count means the stratum SPA "
              "materially under-samples the date-honest tail.", ""]
    path.write_text("\n".join(lines) + "\n")


def _write_report(path: Path, recs: list[dict], root: Path, stamp: str) -> None:
    """REPORT.md — integrating verdict + the C16 α read-off + the design pins (§5)."""
    lines = _hdr("H2.1 supplementary wave — production REPORT", stamp, "§§4, 6, 7, 11")
    lines += ["## C16 — α descriptive read-off (from the lodged refit summary)", "",
              "| unit | frame | N_eff | α median | 95 % CI | conv | below floor? |",
              "|------|-------|-------|----------|---------|------|--------------|"]
    for row in SP.c16_alpha_table(root):
        below = (row.get("n_rows_eff") or 10 ** 9) < REACHABILITY_FLOOR
        lines.append(
            f"| {row['name']} | {row.get('frame')} | {row.get('n_rows_eff')} | "
            f"{_fmt(row.get('alpha_median'), 4)} | "
            f"[{_fmt(row.get('alpha_ci_lo'), 4)}, {_fmt(row.get('alpha_ci_hi'), 4)}] | "
            f"{'ok' if row.get('convergence_pass') else 'FAIL'} | "
            f"{'YES' if below else 'no'} |")
    lines += ["", "## Design-artefact pins (SPEC §5; re-stated, not re-derived)", "",
              "- N_MC = 30, divergence-flag = 1.5× — pertain to C10 (aoristic-MC), "
              "which is HELD and NOT run by this driver.",
              "- W1 (Wasserstein-1, shape) flagging threshold inherited from the "
              "recovery grid (runs/2026-05-26-recovery-grid-two-unit/): Pearson r ≥ 0.95 "
              "(non-flat) / W1 ≤ 10 y (flat_baseline). Re-stated per SPEC §5; not "
              "re-derived.", "",
              "## Per-item deliverables", "",
              "- C5 / C6: `model-comparison.md`  - C11: `trapezoidal.md`",
              "- H2.2: `h2.2-boundary-steps.md`  - H2.3: `h2.3-threshold-convergence.md`",
              "- H2.4: `h2.4-stratified.md`  - C16: this file.", "",
              "## Convergence surfacing (SPEC §7)", ""]
    # Surface every per-fit convergence failure (non-confirmatory: report, don't drop).
    fails: list[str] = []
    for r in recs:
        mc = r.get("model_comparison", {})
        for fam in ("primary_refit", "dm", "nb"):
            cv = mc.get(fam, {}).get("convergence", {})
            if cv and not cv.get("convergence_pass", True):
                fails.append(f"{r['name']} / {fam} (R̂={_fmt(cv.get('max_rhat'),4)}, "
                             f"ESS={_fmt(cv.get('min_ess_bulk'),0)})")
    if fails:
        lines.append("Per-fit convergence failures (reported as per-unit limitations, "
                     "NOT blockers; empire-aggregate is the known under-converger):")
        lines.append("")
        for f in fails:
            lines.append(f"- {f}")
    else:
        lines.append("No per-fit convergence failures recorded in the loaded unit JSONs.")
    lines.append("")
    path.write_text("\n".join(lines) + "\n")


# --- tiny Markdown formatters ---
def _fmt(x: Any, nd: int = 1) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    try:
        return f"{float(x):.{nd}f}"
    except (TypeError, ValueError):
        return str(x)


def _fmt_pct(x: Any) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{float(x) * 100:.0f}%"


def _fmt_ci(med: Any, lo: Any, hi: Any) -> str:
    if med is None:
        return "—"
    return f"{_fmt(med, 4)} [{_fmt(lo, 4)}, {_fmt(hi, 4)}]"


# =========================================================================== #
# Main.                                                                         #
# =========================================================================== #
def main() -> None:
    ap = argparse.ArgumentParser(
        description="H2.1 supplementary-wave PRODUCTION orchestrator (C10 excluded).")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT,
                    help="repo root (parameterised; default the standing checkout path).")
    ap.add_argument("--n-jobs", type=int, default=8,
                    help="parallel worker processes (SPEC §8: n_jobs 8–12).")
    ap.add_argument("--max-tasks-per-child", type=int, default=1,
                    help="worker recycling (cc-grid pattern; default 1).")
    ap.add_argument("--only", type=str, default=None,
                    help="run a single unit by exact name (debug / resume).")
    ap.add_argument("--write-only", action="store_true",
                    help="skip fitting; only (re)assemble the Markdown deliverables "
                         "from the existing per-unit JSONs.")
    args = ap.parse_args()

    _wire(args.root)
    out_dir = args.root / RUN_REL / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    draws_dir = (args.root / "runs" / "2026-06-13-cc-production-refit" / "outputs"
                 / "posterior-draws")
    draws_dir_str = str(draws_dir) if draws_dir.exists() else None
    if draws_dir_str is None:
        print("WARNING: lodged posterior-draws dir not found — H2.2 / H2.4 / C11 "
              "output-level legs will be caveated (need the uniform-input p_gen).",
              flush=True)

    if args.write_only:
        write_deliverables(args.root)
        print(f"deliverables (re)written → {out_dir}")
        return

    units = R.enumerate_refit_units()
    if args.only:
        units = [u for u in units if u["name"] == args.only]
        if not units:
            raise SystemExit(f"no unit named {args.only!r}")
    todo = [u for u in units if not _unit_done(u, args.root)]
    print(f"supplementary production: {len(units)} units "
          f"({len(todo)} to do, {len(units) - len(todo)} cached); n_jobs {args.n_jobs}; "
          f"C10 EXCLUDED (held). draws-dir={'present' if draws_dir_str else 'MISSING'}",
          flush=True)
    if not todo:
        print("nothing to fit (all cached); assembling deliverables.")
        write_deliverables(args.root)
        return

    t0 = time.time()
    done = len(units) - len(todo)
    failed: list[str] = []
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, u, str(args.root), draws_dir_str): u for u in todo}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                name, conv = fut.result()
                done += 1
                print(f"[{done}/{len(units)}] {name}  DM-conv="
                      f"{'ok' if conv else 'FAIL'}", flush=True)
            except BrokenProcessPool:
                print("FATAL: pool broken (OOM?) — resume re-runs unfinished units.",
                      flush=True)
                raise
            except Exception as exc:  # noqa: BLE001
                failed.append(u["name"])
                print(f"WORKER-ERROR {u['name']}: {repr(exc)[:200]}", flush=True)
    print(f"fits complete in {(time.time() - t0) / 60:.1f} min. "
          f"worker-errored: {failed}", flush=True)
    write_deliverables(args.root)
    print(f"deliverables written → {out_dir}")


if __name__ == "__main__":
    main()
