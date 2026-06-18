#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smoke_supp.py — the three §3.4 smoke gates for the supplementary builders.
==========================================================================

MUST pass before any pilot / production fit (SPEC §3.4 / §9.1). Run on sapphire
(small unit, fast). The three gates:

1. **DM → multinomial reduction.** Fit ``build_model_cc_dirichlet_multinomial``
   with κ PINNED large (1e6) on a small unit; assert the posterior on α AND θ AND
   ``p_gen`` matches the primary ``build_model_cross_classified`` to MCMC noise
   (|Δα| ≤ 2e-3 — the same gate as the H3b provenance check; θ within 5e-3;
   ``p_gen`` agreement). Certifies the DM builder is "primary plus overdispersion,
   nothing else" (SPEC §3.4 gate 1: α + θ + p_gen, not α alone).
2. **NegBin large-φ α-sanity.** Fit ``build_model_cc_negbin`` with ``inv_phi``
   pinned tiny (φ → ∞); assert α within ~0.01 of the primary. The rescaled NegBin
   is a NON-NESTED cross-check (SPEC §3.2), NOT a multinomial reduction — it has no
   term conditioning the per-bin counts to the subset total — so this is evidence
   the overdispersed family does not move the α verdict, not a nested-reduction
   proof. Not bit-identical (different family by construction).
3. **set_data logp-parity (NO sampling).** A ``pm.set_data`` swap must rewire the
   data into a likelihood graph IDENTICAL to a fresh build. Tested by evaluating
   the compiled logp of two model graphs — one built fresh on the unit's real data,
   one built on different but internally-valid placeholder data then ``set_data``-d
   to the same real data — at ONE shared fixed parameter point. logp is
   deterministic, so |logp_A − logp_B| < 1e-8 is decisive and IMMUNE to the
   NUTS/threaded-BLAS sampling nondeterminism that the project documents (so this
   does NOT re-use the old sampled-draw ``np.array_equal`` bit-identity test, which
   would spuriously fail — see ``validate_cc_setdata.py`` and
   ``verify_emit_provenance.py``). The gate runs on ALL THREE builders (primary,
   DM, NegBin), so it now exercises the supplementary likelihoods too.

The smallest production unit (by effective N) is auto-selected so the gates are
fast. Same sampler config as production (4 × (1000 tune + 2000 draws), cores=1).

Usage (sapphire):
  PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN \
    uv run python code/smoke_supp.py

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------- #
# Path wiring (absolute; repo at the same location on amd-tower and sapphire). #
# --------------------------------------------------------------------------- #
ROOT = Path("/home/shawn/Code/inscriptions")
H2 = ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
JOINT = ROOT / "runs" / "2026-06-09-joint-identifiability" / "code"
REFIT = ROOT / "runs" / "2026-06-13-cc-production-refit" / "code"
SUPP = ROOT / "runs" / "2026-06-18-h2.1-supplementary-wave" / "code"
CELL_LIB_DIR = (ROOT / "runs" / "2026-06-06-convention-basis-redesign"
                / "revalidation" / "code")
for p in (str(SUPP), str(REFIT), str(H2), str(JOINT), str(CELL_LIB_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402
import supp_lib as S  # noqa: E402
from cell_lib import convergence_pass  # noqa: E402

# Smoke-gate tolerances (SPEC §3.4).
TOL_DM_REDUCTION = 2e-3     # |Δα| DM(κ=1e6) vs primary (gate 1, α)
TOL_THETA = 5e-3            # |Δθ_conv|, |Δθ_gen| DM(κ=1e6) vs primary (gate 1, θ)
TOL_PGEN_BIN = 0.02         # max per-bin |Δp_gen| (gate 1, p_gen — OR the r-test below)
TOL_PGEN_ONE_MINUS_R = 0.01  # 1 − Pearson r(p_gen) acceptable if the bin test misses
TOL_NEGBIN = 1e-2           # |Δα| NegBin(φ→∞) vs primary (gate 2)
TOL_LOGP_PARITY = 1e-8      # |logp_A − logp_B| for the set_data logp-parity gate (gate 3)
KAPPA_LARGE = 1e6           # pinned κ for the reduction gate
INV_PHI_TINY = 1e-6         # pinned 1/φ for the large-φ gate

SMOKE_SEED = 20260618       # fixed smoke seed (shared across the fitting gates)

# Loaded once: the FIXED slab library + adopted θ priors (production identicals).
LIBRARY_BASIS, _ = R.load_library_basis()
THETA_CONV_AB, THETA_GEN_AB, _ = R.adopted_theta_priors()
# Reported diagnostics across all the monitored structural parameters …
MONITORED = ["alpha", "tier_weights", "sigma_smooth", "z_pgen",
             "theta_conv", "theta_gen"]
# … but the CONVERGENCE GATE itself is the spec's stated set only: α + tier_weights
# (SPEC §7). Gating on z_pgen too (the GRW increments) is stricter than spec and
# noisy — a benign GRW-tail ESS dip must not be mislabelled as a builder defect.
CONV_GATE_VARS = ["alpha", "tier_weights"]


def _sample(model, seed: int):
    """Sample one model with the production config; return the InferenceData."""
    import pymc as pm
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                target_accept=H.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True)
    return idata


def _alpha_draws(idata) -> np.ndarray:
    """Flattened α posterior draws (chains × draws,)."""
    return idata.posterior["alpha"].values.reshape(-1)


def _theta_medians(idata) -> tuple[float, float]:
    """Posterior medians of (θ_conv, θ_gen) for the gate-1 θ-parity check."""
    return (float(np.median(idata.posterior["theta_conv"].values)),
            float(np.median(idata.posterior["theta_gen"].values)))


def _pgen_median(idata) -> np.ndarray:
    """Posterior-median genuine SPA ``p_gen`` (length N_BINS), normalised to 1.

    Used by the gate-1 ``p_gen`` agreement check (SPEC §3.4 gate 1 requires α AND
    θ AND p_gen to match the primary under the DM reduction, not α alone).
    """
    pg = idata.posterior["p_gen"].values
    n_bins = pg.shape[-1]
    med = np.median(pg.reshape(-1, n_bins), axis=0)
    s = med.sum()
    return med / s if s > 0 else med


def _conv(idata) -> dict:
    """Convergence summary, gating on the SPEC §7 set (α + tier_weights).

    Reports the broader monitored diagnostics (``MONITORED``) for the record, but
    the pass/fail verdict is computed on ``CONV_GATE_VARS`` ONLY — the spec's stated
    gate. The wider R̂ / ESS (including z_pgen) are reported as ``*_monitored`` so a
    GRW-tail dip is visible without failing the gate. Compute this ONCE per fit and
    cache the dict (it was previously evaluated twice per fit).
    """
    import arviz as az
    summ_all = az.summary(idata, var_names=MONITORED, round_to="none")
    summ_gate = az.summary(idata, var_names=CONV_GATE_VARS, round_to="none")
    max_rhat = float(summ_gate["r_hat"].max())          # gate set only
    min_ess = float(summ_gate["ess_bulk"].min())        # gate set only
    n_div = int(idata.sample_stats["diverging"].values.sum())
    return {
        "max_rhat": max_rhat, "min_ess_bulk": min_ess, "n_divergences": n_div,
        # The wider monitored diagnostics, for the record (NOT gated on).
        "max_rhat_monitored": float(summ_all["r_hat"].max()),
        "min_ess_bulk_monitored": float(summ_all["ess_bulk"].min()),
        "convergence_pass": bool(convergence_pass(max_rhat, min_ess)),
        "gate_vars": CONV_GATE_VARS,
    }


def _grade_gate(within_tol: bool, conv_passes: bool) -> tuple[str, bool]:
    """Grade a comparison gate, with convergence gating the verdict (SPEC §7).

    A convergence dip must NOT be mislabelled as a builder defect: if EITHER fit in
    a comparison failed the (α + tier_weights) convergence gate, the gate result is
    ``INCONCLUSIVE — non-converged`` (the Δ is still reported), rather than a hard
    reduction-failure. Only a converged-but-out-of-tolerance comparison is a true
    FAIL.

    Parameters
    ----------
    within_tol : bool
        Whether the measured Δ is within the gate tolerance.
    conv_passes : bool
        Whether BOTH fits in the comparison passed the convergence gate.

    Returns
    -------
    (status, gate_ok) : (str, bool)
        ``status`` ∈ {"PASS", "FAIL", "INCONCLUSIVE — non-converged"};
        ``gate_ok`` is True only for a converged PASS (the run-level gate AND).
    """
    if not conv_passes:
        return "INCONCLUSIVE — non-converged", False
    return ("PASS", True) if within_tol else ("FAIL", False)


def _valid_placeholder(ya: np.ndarray, yn: np.ndarray, k: int,
                       n_rows: int) -> tuple[np.ndarray, np.ndarray]:
    """An internally-valid placeholder split of the SAME shape / k / n_rows.

    The gate-3 logp-parity test needs ``model_B`` built on data that is DIFFERENT
    from the unit's real data but still satisfies the cross-classified invariants
    (``y_aligned.sum() == k`` and ``y_aligned.sum() + y_nonaligned.sum() == n_rows``)
    so the builders' own ``_validate_cc_counts`` passes and the DM/Multinomial
    ``sum(obs) == n`` invariant holds at build time. We keep the per-subset totals
    (and hence ``k`` / ``n_rows``) fixed and only RESHUFFLE the within-subset bin
    assignment (a circular roll), guaranteeing a genuinely different count vector
    while preserving every invariant. ``set_data`` then swaps it back to the real
    data, and logp-parity certifies the swap is exact.

    Returns
    -------
    (y_aligned_placeholder, y_nonaligned_placeholder) : int64 arrays
    """
    ya_ph = np.roll(np.asarray(ya, dtype="int64"), 1)
    yn_ph = np.roll(np.asarray(yn, dtype="int64"), 1)
    # A circular roll is a permutation, so the subset sums are preserved exactly.
    assert int(ya_ph.sum()) == int(k), "placeholder roll changed k"
    assert int(ya_ph.sum() + yn_ph.sum()) == int(n_rows), "placeholder roll changed n_rows"
    # Guard against the degenerate case where a roll is a no-op (all mass in the
    # bin a roll maps to itself — impossible for a length>1 vector with >1 nonzero
    # bin, but keep the assertion honest): require it to actually differ.
    if np.array_equal(ya_ph, np.asarray(ya, dtype="int64")) and \
            np.array_equal(yn_ph, np.asarray(yn, dtype="int64")):
        raise RuntimeError("placeholder identical to real data; cannot test set_data")
    return ya_ph, yn_ph


def _logp_parity(build, ya: np.ndarray, yn: np.ndarray,
                 ya_ph: np.ndarray, yn_ph: np.ndarray,
                 k: int, n_rows: int) -> tuple[float, float, float]:
    """logp-parity for one builder: fresh(real) vs placeholder + set_data(real).

    NO sampling. Builds ``model_A`` on the REAL data and ``model_B`` on the
    placeholder data, swaps ``model_B``'s ``k_data`` / ``y_al_data`` / ``y_non_data``
    TOGETHER to the real data via ``pm.set_data`` (so the sum==n invariant holds),
    compiles each model's logp, and evaluates BOTH at the SAME single fixed
    parameter point (``model_A.initial_point()``). Returns ``(logp_A, logp_B, |Δ|)``.

    Parameters
    ----------
    build : callable(y_aligned, y_nonaligned) -> pymc.Model
        Builds the model on the given subset count vectors (k / n_rows are closed
        over by the caller; the builders bake them into the ``n=`` of the
        Binomial / Multinomial).
    ya, yn : int arrays
        The unit's REAL aligned / non-aligned subset counts.
    ya_ph, yn_ph : int arrays
        The internally-valid placeholder counts (same shape / k / n_rows).
    k, n_rows : int
        The (held-constant) aligned total and grand total.

    Returns
    -------
    (logp_A, logp_B, abs_delta) : (float, float, float)
    """
    import pymc as pm

    # model_A: fresh build on the REAL data.
    model_a = build(ya, yn)
    point = model_a.initial_point()        # the SHARED fixed evaluation point
    logp_a = float(model_a.compile_logp()(point))

    # model_B: build on the PLACEHOLDER data, then set_data → the real data.
    model_b = build(ya_ph, yn_ph)
    with model_b:
        # Swap k_data, y_al_data AND y_non_data together so the DM / Multinomial
        # sum(obs)==n invariant holds after the swap (audit M2 guard).
        pm.set_data({
            "k_data": np.asarray(int(k), dtype="int64"),
            "y_al_data": np.asarray(ya, dtype="int64"),
            "y_non_data": np.asarray(yn, dtype="int64"),
        })
    logp_b = float(model_b.compile_logp()(point))   # SAME fixed point

    return logp_a, logp_b, abs(logp_a - logp_b)


def _pick_smallest_unit() -> tuple[dict, dict]:
    """Build CC data for every unit; return the (unit, data) with the smallest
    effective N (the fastest unit for the smoke gates)."""
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    best = None
    for unit in R.enumerate_refit_units():
        sub = R.subset_for(df, unit, latin)
        if len(sub) == 0:
            continue
        data = R.build_unit_cc_data(sub)
        # Need both subsets non-empty for the cross-classified contrast.
        if data["k"] <= 0 or (data["n_rows"] - data["k"]) <= 0:
            continue
        if best is None or data["n_rows"] < best[1]["n_rows"]:
            best = (unit, data)
    if best is None:
        raise RuntimeError("no eligible smoke unit found")
    return best


def main() -> None:
    out_dir = ROOT / "runs" / "2026-06-18-h2.1-supplementary-wave" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    results: dict = {"seed": SMOKE_SEED, "gates": {}}

    unit, data = _pick_smallest_unit()
    ya, yn, k, n_rows = data["y_aligned"], data["y_nonaligned"], data["k"], data["n_rows"]
    print(f"smoke unit: {unit['name']!r}  N_eff={n_rows}  k={k}  "
          f"(n_rows_raw={data['n_rows_raw']})", flush=True)
    results["unit"] = {"name": unit["name"], "n_rows_eff": n_rows, "k_eff": k,
                       "n_rows_raw": data["n_rows_raw"]}

    # ---- PRIMARY reference fit (shared by gates 1 and 2) ----
    t0 = time.time()
    primary = J.build_model_cross_classified(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        pconv_mode="library")
    idata_primary = _sample(primary, SMOKE_SEED)
    med_primary = float(np.median(_alpha_draws(idata_primary)))
    theta_conv_p, theta_gen_p = _theta_medians(idata_primary)
    pgen_p = _pgen_median(idata_primary)
    conv_primary = _conv(idata_primary)   # compute ONCE, cache, reuse (audit fix 4)
    t_primary = time.time() - t0
    print(f"  primary    α_med={med_primary:.5f}  ({t_primary:.1f}s)  "
          f"{conv_primary}", flush=True)
    results["primary"] = {
        "alpha_median": med_primary, "theta_conv_med": theta_conv_p,
        "theta_gen_med": theta_gen_p, "secs": round(t_primary, 1),
        "convergence": conv_primary}

    # ---- GATE 1: DM → multinomial reduction at κ = 1e6 (α AND θ AND p_gen) ----
    # SPEC §3.4 gate 1 requires α, θ AND p_gen to match the primary under the DM
    # reduction — not α alone. Under κ → ∞ the DirichletMultinomial concentrates to
    # the Multinomial, so the DM builder must recover the primary posterior across
    # the whole structural vector, certifying it is "primary plus overdispersion,
    # nothing else".
    t0 = time.time()
    dm = S.build_model_cc_dirichlet_multinomial(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        kappa_fixed=KAPPA_LARGE, pconv_mode="library")
    idata_dm = _sample(dm, SMOKE_SEED)
    med_dm = float(np.median(_alpha_draws(idata_dm)))
    theta_conv_dm, theta_gen_dm = _theta_medians(idata_dm)
    pgen_dm = _pgen_median(idata_dm)
    conv_dm = _conv(idata_dm)
    t_dm = time.time() - t0

    d_alpha_dm = abs(med_dm - med_primary)
    d_theta_conv = abs(theta_conv_dm - theta_conv_p)
    d_theta_gen = abs(theta_gen_dm - theta_gen_p)
    # p_gen agreement: max per-bin |Δ| OR (1 − Pearson r) — either within tolerance
    # accepts (the bin test is the primary criterion; r catches shape agreement when
    # a single bin is fractionally over the abs-diff bar but the curves co-vary).
    pgen_max_abs = float(np.max(np.abs(pgen_dm - pgen_p)))
    pgen_r = float(np.corrcoef(pgen_dm, pgen_p)[0, 1])
    pgen_one_minus_r = 1.0 - pgen_r
    pgen_ok = (pgen_max_abs < TOL_PGEN_BIN) or (pgen_one_minus_r < TOL_PGEN_ONE_MINUS_R)

    within_tol_dm = (d_alpha_dm <= TOL_DM_REDUCTION
                     and d_theta_conv <= TOL_THETA
                     and d_theta_gen <= TOL_THETA
                     and pgen_ok)
    conv_ok_dm = conv_primary["convergence_pass"] and conv_dm["convergence_pass"]
    status_dm, gate1_pass = _grade_gate(within_tol_dm, conv_ok_dm)
    print(f"  GATE 1 DM(κ=1e6)  α_med={med_dm:.5f}  |Δα|={d_alpha_dm:.2e}  "
          f"|Δθc|={d_theta_conv:.2e}  |Δθg|={d_theta_gen:.2e}  "
          f"pgen_max|Δ|={pgen_max_abs:.3e}  1−r={pgen_one_minus_r:.2e}  "
          f"{status_dm}  ({t_dm:.1f}s)", flush=True)
    results["gates"]["dm_reduction"] = {
        "alpha_median": med_dm, "delta_alpha": d_alpha_dm, "tol_alpha": TOL_DM_REDUCTION,
        "theta_conv_med": theta_conv_dm, "theta_gen_med": theta_gen_dm,
        "delta_theta_conv": d_theta_conv, "delta_theta_gen": d_theta_gen,
        "tol_theta": TOL_THETA,
        "pgen_max_abs_diff": pgen_max_abs, "pgen_one_minus_pearson_r": pgen_one_minus_r,
        "tol_pgen_bin": TOL_PGEN_BIN, "tol_pgen_one_minus_r": TOL_PGEN_ONE_MINUS_R,
        "pgen_agreement": pgen_ok,
        "within_tol": within_tol_dm, "status": status_dm, "pass": gate1_pass,
        "secs": round(t_dm, 1), "convergence": conv_dm}

    # ---- GATE 2: NegBin large-φ α-sanity (1/φ pinned tiny; NON-NESTED cross-check) ----
    # The rescaled NegBin is a NON-NESTED cross-check (SPEC §3.2), NOT a multinomial
    # reduction: it has no term conditioning the per-bin counts to the subset total,
    # so under φ → ∞ it does NOT recover the multinomial bit-identically. The sanity
    # target is simply that α lands within ~0.01 of the primary — evidence the
    # overdispersed family does not move the α verdict.
    t0 = time.time()
    nb = S.build_model_cc_negbin(
        ya, yn, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
        inv_phi_fixed=INV_PHI_TINY, pconv_mode="library")
    idata_nb = _sample(nb, SMOKE_SEED)
    med_nb = float(np.median(_alpha_draws(idata_nb)))
    conv_nb = _conv(idata_nb)
    t_nb = time.time() - t0
    d_alpha_nb = abs(med_nb - med_primary)
    within_tol_nb = d_alpha_nb <= TOL_NEGBIN
    conv_ok_nb = conv_primary["convergence_pass"] and conv_nb["convergence_pass"]
    status_nb, gate2_pass = _grade_gate(within_tol_nb, conv_ok_nb)
    print(f"  GATE 2 NegBin(φ→∞)  α_med={med_nb:.5f}  |Δα|={d_alpha_nb:.2e}  "
          f"(tol {TOL_NEGBIN:.0e})  {status_nb}  ({t_nb:.1f}s)", flush=True)
    results["gates"]["negbin_largephi"] = {
        "alpha_median": med_nb, "delta_alpha": d_alpha_nb,
        "tol": TOL_NEGBIN, "within_tol": within_tol_nb, "status": status_nb,
        "pass": gate2_pass, "secs": round(t_nb, 1), "convergence": conv_nb,
        "note": ("non-nested cross-check, not a multinomial reduction (SPEC §3.2): "
                 "evidence the overdispersed family does not move the α verdict")}

    # ---- GATE 3: set_data logp-parity at a fixed point (NO sampling) ----
    # Old gate 3 asserted np.array_equal bit-identity on SAMPLED α draws across two
    # model graphs under FAST_RUN + threaded BLAS — which the project documents as
    # NON-reproducible (validate_cc_setdata.py: "graph-construction differences shift
    # NUTS trajectories"; verify_emit_provenance.py: "not bit-reproducible … float
    # reductions reorder"), so it would spuriously FAIL and sys.exit(1) the whole run.
    #
    # Replaced with a deterministic logp-parity test that does NO sampling. For each
    # builder we compile the model logp and evaluate it at ONE shared fixed parameter
    # point (model_A.initial_point()) on two graphs:
    #   model_A — built directly on the unit's REAL (ya, yn, k, n_rows);
    #   model_B — built on DIFFERENT but internally-valid placeholder data of the same
    #             shape (same k / n_rows so the build-time Binomial/Multinomial `n=`
    #             ints match; a within-subset bin reshuffle), then pm.set_data to swap
    #             k_data + y_al_data + y_non_data TOGETHER to the real data (so the
    #             DM/Multinomial sum(obs)==n invariant holds after the swap).
    # logp is deterministic, so |logp_A − logp_B| < 1e-8 is decisive and immune to the
    # sampler nondeterminism. This certifies set_data rewires the data into an IDENTICAL
    # likelihood graph, and (unlike the old gate, which touched only the primary) now
    # exercises all three builders — including the DM and NegBin likelihoods.
    ya_ph, yn_ph = _valid_placeholder(ya, yn, k, n_rows)

    builders = {
        "primary": (
            lambda y_a, y_n: J.build_model_cross_classified(
                y_a, y_n, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
                pconv_mode="library")),
        "dirichlet_multinomial": (
            lambda y_a, y_n: S.build_model_cc_dirichlet_multinomial(
                y_a, y_n, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
                kappa_fixed=KAPPA_LARGE, pconv_mode="library")),
        "negbin": (
            lambda y_a, y_n: S.build_model_cc_negbin(
                y_a, y_n, k, n_rows, LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB,
                inv_phi_fixed=INV_PHI_TINY, pconv_mode="library")),
    }

    parity_results: dict = {}
    gate3_pass = True
    for bname, build in builders.items():
        logp_a, logp_b, dlp = _logp_parity(build, ya, yn, ya_ph, yn_ph, k, n_rows)
        ok = bool(dlp < TOL_LOGP_PARITY)
        gate3_pass = gate3_pass and ok
        parity_results[bname] = {
            "logp_A_real_fresh": logp_a, "logp_B_placeholder_then_setdata": logp_b,
            "abs_delta_logp": dlp, "tol": TOL_LOGP_PARITY, "pass": ok}
        print(f"  GATE 3 logp-parity [{bname:21s}]  logp_A={logp_a:.6f}  "
              f"logp_B={logp_b:.6f}  |Δ|={dlp:.3e}  (tol {TOL_LOGP_PARITY:.0e})  "
              f"{'PASS' if ok else 'FAIL'}", flush=True)
    results["gates"]["set_data_logp_parity"] = {
        "method": ("fresh-build(real) vs build(placeholder)+set_data(real); compiled "
                   "logp at a single fixed point (model_A.initial_point()); NO sampling"),
        "builders": parity_results, "pass": gate3_pass}

    all_pass = gate1_pass and gate2_pass and gate3_pass
    results["all_pass"] = all_pass
    (out_dir / "smoke-results.json").write_text(json.dumps(results, indent=2))
    print(f"\nSMOKE {'ALL PASS' if all_pass else 'FAILED'} — "
          f"results → {out_dir / 'smoke-results.json'}", flush=True)
    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
