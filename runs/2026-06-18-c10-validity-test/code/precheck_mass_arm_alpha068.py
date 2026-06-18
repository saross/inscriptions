#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
precheck_mass_arm_alpha068.py — single-cell mass-arm pre-check for the C10 test.
================================================================================

ONE cheap pre-check (audit verdict iii): run the **mass arm ONLY**, at the single
planted α = 0.68, one generator seed — the hardest-but-decisive point (the static
θ-tension bias is +0.044 there and the test's (b)-verdict boundary is near). The
question it settles: does the synthetic θ degeneracy compromise the test's
mass-arm baseline?

This is **"running the audited code"**, NOT new analysis logic. It reproduces
*exactly one cell* of ``run_c10.run_1b`` (planted α = 0.68, seed-index 0) by
calling the existing AUDITED ``c10_lib`` functions and the lodged
``joint_lib.build_model_cross_classified`` with the production sampling config —
the same generate → mass-counts → fit → compare chain ``run_1b`` runs, with the
identical per-(α, seed) seed scheme. Nothing in ``c10_lib`` or ``run_c10`` is
modified. The only thing this adds over the audited ``run_c10._fit_mass_arm`` is
**retaining the InferenceData** so the gate can report R̂ / ESS / divergences;
the sampler call is byte-for-byte the production config in ``run_c10._sample_alpha``.

Seed derivation (verbatim from ``run_c10.run_1b``):
    PLANTED_ALPHAS = (0.3, 0.5, 0.68, 0.8) → α = 0.68 is index ai = 2; seed si = 0
    gen_seed      = BASE_SEED + 1000*ai + si        = 20260618 + 2000 = 20262618
    mass_fit_seed = BASE_SEED + 100_000 + 1000*ai + si = 20360618 + 2000 = 20362618

Run (zbook; minutes):
    cd /home/shawn/Code/inscriptions
    .venv/bin/python runs/2026-06-18-c10-validity-test/code/precheck_mass_arm_alpha068.py

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

RUN_DIR = Path("/home/shawn/Code/inscriptions/runs/2026-06-18-c10-validity-test")
CODE_DIR = RUN_DIR / "code"
OUT_DIR = RUN_DIR / "outputs"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import c10_lib as C  # noqa: E402  (wires h2_lib / joint_lib / refit_lib)
import run_c10 as RC  # noqa: E402  (the audited driver — config + helpers)

# h2_lib / joint_lib / refit_lib are on sys.path via c10_lib's inserts.
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402

import arviz as az  # noqa: E402
import pymc as pm  # noqa: E402


def main() -> None:
    """Reproduce the single α = 0.68, seed-0 mass-arm cell of run_1b; report the gate."""
    # ---- the exact run_1b cell coordinates for planted α = 0.68, seed-index 0 ----
    alpha = 0.68
    ai = RC.PLANTED_ALPHAS.index(alpha)        # 2
    si = 0
    gen_seed = RC.BASE_SEED + 1000 * ai + si
    mass_fit_seed = RC.BASE_SEED + 100_000 + 1000 * ai + si

    # ---- the production basis / θ priors (lodged artefacts; same as run_c10.main) ---
    basis, slabs = R.load_library_basis()
    tc_ab, tg_ab, _theta_fit = R.adopted_theta_priors()
    p_gen, pgen_label = C.resolve_pgen(RC.GENUINE_PGEN)

    print(f"[precheck] planted α = {alpha} (ai={ai}, si={si}); "
          f"gen_seed={gen_seed}, mass_fit_seed={mass_fit_seed}")
    print(f"[precheck] p_gen = {pgen_label}; N_synth = {RC.N_SYNTH}; "
          f"half_width = {RC.GENUINE_HALF_WIDTH}")
    print(f"[precheck] sampler: draws={H.N_DRAWS} tune={H.N_TUNE} "
          f"chains={H.N_CHAINS} target_accept={H.TARGET_ACCEPT} cores=1")

    # ---- STEP 1: generate synthetic inscriptions (AUDITED c10_lib) ----
    df = C.generate_inscriptions(
        alpha, RC.N_SYNTH, gen_seed, slabs, p_gen,
        genuine_half_width=RC.GENUINE_HALF_WIDTH)
    realised_alpha = float((df["type"] == "convention").mean())

    # ---- STEP 2: build the aoristic-MASS count representation (AUDITED c10_lib) ----
    mass = C.mass_cc_counts(df)
    print(f"[precheck] realised α = {realised_alpha:.4f}; "
          f"k = {mass['k']}, n_rows = {mass['n_rows']}; "
          f"row_aligned_frac = {mass['row_aligned_frac']:.4f}, "
          f"mass_aligned_frac = {mass['mass_aligned_frac']:.4f}")

    # ---- STEP 3: fit the mass arm (lodged build_model_cross_classified) ----
    # Mirrors run_c10._fit_mass_arm + _sample_alpha EXACTLY (production config);
    # we retain the idata only to report convergence diagnostics.
    model = J.build_model_cross_classified(
        mass["y_aligned"], mass["y_nonaligned"], mass["k"], mass["n_rows"],
        basis, tc_ab, tg_ab, pconv_mode="library")
    t0 = time.time()
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                target_accept=H.TARGET_ACCEPT, random_seed=mass_fit_seed,
                progressbar=False, return_inferencedata=True)
    secs = time.time() - t0

    # ---- STEP 4: recovered α median + 95 % CI, |Δα|, convergence ----
    draws = idata.posterior["alpha"].values.reshape(-1)
    stats = RC._alpha_stats(draws)            # AUDITED summary (median + 95 % CI)
    delta = stats["alpha_median"] - alpha
    abs_delta = abs(delta)

    summ = az.summary(idata, var_names=["alpha"])
    rhat = float(summ["r_hat"].iloc[0])
    ess_bulk = float(summ["ess_bulk"].iloc[0])
    ess_tail = float(summ["ess_tail"].iloc[0])
    n_div = int(idata.sample_stats["diverging"].values.sum())

    # ---- the pre-registered gate (the brief's thresholds) ----
    if abs_delta <= 0.05:
        gate = ("BASELINE CLEAN: idealised θ is fine; proceed to the full battery.")
    elif abs_delta >= 0.08:
        gate = ("BASELINE DRIFTS: the generator needs realistic-θ contamination "
                "before the test is valid.")
    else:
        contains = stats["alpha_ci_lo"] <= alpha <= stats["alpha_ci_hi"]
        gate = (f"BORDERLINE: |Δα| = {abs_delta:.4f} in (0.05, 0.08); "
                f"95% CI {'COMFORTABLY CONTAINS' if contains else 'does NOT contain'} "
                f"0.68 → lean {'clean' if contains else 'drift'}.")

    result = {
        "precheck": "c10 mass-arm single-cell (planted alpha=0.68, seed-index 0)",
        "spec": "runs/2026-06-18-c10-validity-test/SPEC.md",
        "audited_code_commit": "6ce6e3f (c10_lib.py + run_c10.py)",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "planted_alpha": alpha,
        "gen_seed": gen_seed,
        "mass_fit_seed": mass_fit_seed,
        "realised_alpha": realised_alpha,
        "n_synth": RC.N_SYNTH,
        "genuine_pgen": pgen_label,
        "genuine_half_width": RC.GENUINE_HALF_WIDTH,
        "k": mass["k"], "n_rows": mass["n_rows"],
        "row_aligned_frac": mass["row_aligned_frac"],
        "mass_aligned_frac": mass["mass_aligned_frac"],
        "sampler": {"draws": H.N_DRAWS, "tune": H.N_TUNE, "chains": H.N_CHAINS,
                    "target_accept": H.TARGET_ACCEPT, "cores": 1},
        "recovered_alpha_median": stats["alpha_median"],
        "recovered_alpha_ci_lo": stats["alpha_ci_lo"],
        "recovered_alpha_ci_hi": stats["alpha_ci_hi"],
        "ci_width": stats["ci_width"],
        "delta": delta,
        "abs_delta": abs_delta,
        "r_hat": rhat,
        "ess_bulk": ess_bulk,
        "ess_tail": ess_tail,
        "n_divergences": n_div,
        "wall_secs": round(secs, 1),
        "gate": gate,
    }

    out_path = OUT_DIR / "precheck-mass-arm-alpha068.json"
    out_path.write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")

    # Save idata for provenance (gitignored .nc). arviz>=1.x exposes this as the
    # InferenceData method ``idata.to_netcdf`` (the module-level ``az.to_netcdf``
    # was removed); wrapped so a save hiccup never loses the already-written JSON.
    nc_path = OUT_DIR / "precheck-mass-arm-alpha068.nc"
    try:
        idata.to_netcdf(str(nc_path))
    except Exception as exc:  # noqa: BLE001 — provenance-only; gate already saved
        print(f"[precheck] WARNING: could not write idata .nc ({exc}); "
              f"gate results already in {out_path}")

    print("\n========== C10 MASS-ARM PRE-CHECK (planted α = 0.68) ==========")
    print(f"recovered α median = {stats['alpha_median']:.4f}  "
          f"95% CI [{stats['alpha_ci_lo']:.4f}, {stats['alpha_ci_hi']:.4f}]  "
          f"(width {stats['ci_width']:.4f})")
    print(f"|Δα| = |{stats['alpha_median']:.4f} - 0.68| = {abs_delta:.4f}  "
          f"(signed Δ = {delta:+.4f})")
    print(f"convergence: R-hat = {rhat:.4f}, ESS bulk = {ess_bulk:.0f}, "
          f"ESS tail = {ess_tail:.0f}, divergences = {n_div}")
    print(f"wall time: {secs:.1f} s")
    print(f"\nGATE: {gate}")
    print(f"\nWrote {out_path}")
    print(f"Wrote {nc_path} (gitignored)")


if __name__ == "__main__":
    main()
