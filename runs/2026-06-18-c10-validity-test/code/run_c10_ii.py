#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_c10_ii.py — driver for the C10 follow-up "(ii)" realism-graded recovery test.
=================================================================================

Resolves the puzzle the first validity test (``run_c10.py``) left open: the
point-date aoristic-MC RECOVERED the planted α on the idealised §2 synthetic
(verdict (a)), yet on the REAL empire it collapsed (point-collapse α = 0.100 vs
mass-preserving α = 0.615 in 1c). So the idealised generator is missing the
real-data feature that drives the collapse. (ii) GRADES the realism of the
generator and asks, per variant: *does the point-date arm now DIVERGE from the mass
arm (and/or collapse toward the ~0.1 floor), reproducing the 1c gap?*

For each variant in {R0 baseline, R1, R2, R3, R1+R2} (``c10_ii_lib.VARIANTS``):
plant α ∈ {0.3, 0.5, 0.68, 0.8}, ≥ 2 generator seeds, generate a synthetic frame,
then recover α two ways from the SAME frame:

* **mass arm** — ``build_model_cross_classified(pconv_mode="library")`` on the
  aoristic-mass counts (``c10_lib.mass_cc_counts``); the arm already validated to
  recover α.
* **point-date arm** — the lodged C10 build-once-then-``set_data`` loop over
  ``N_MC = 10`` point-date realisations (``c10_lib.point_date_cc_counts``), pooling
  α draws.

Both arm-fitters and the α summary are REUSED from ``run_c10`` (imported, not
reimplemented). The generator is the new ``c10_ii_lib.generate_inscriptions_variant``
(R0 delegates verbatim to ``c10_lib.generate_inscriptions``).

OUTCOME OF INTEREST + DECISION RULE
-----------------------------------
Per variant we record the recovered α (median + 95 % CI) for both arms vs planted,
and the arm DIVERGENCE Δ = |mass α − point-date α|. The verdict names which
idealisation(s) reproduce the 1c collapse:

* a variant **REPRODUCES the collapse** if, across its sweep, the mass arm still
  recovers planted α (max |mass − planted| ≤ ``RECOVERY_TOL``) while the point-date
  arm DIVERGES from the mass arm (mean Δ ≥ ``DIVERGENCE_TOL``) AND/OR collapses
  toward the pilot floor (median point-date α ≤ ``PILOT_FLOOR + RECOVERY_TOL``).
* R0 is the negative control (must NOT reproduce — it is the (a)-verdict baseline).
* R3 is the confirmatory null (predicted NOT to reproduce — true-date shape is
  irrelevant to either arm).

BUILD-ONLY / RUN GATE
---------------------
This driver performs MCMC. It is NOT run during the build/audit — it runs ONLY
after audit sign-off (standing rule). The post-audit run command is in ``main()``'s
docstring and in ``C10-FOLLOWUP-NOTES.md``.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-19. UK/Australian English; Oxford comma.
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
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import c10_ii_lib as C2  # noqa: E402  (the new realism-graded generator)
import c10_lib as C  # noqa: E402  (count builders; wires h2_lib / joint_lib / refit_lib)
import run_c10 as RC  # noqa: E402  (REUSE the validated arm-fitters; no side effects at import)

import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402

# --------------------------------------------------------------------------- #
# Test configuration (mirrors run_c10's pinned config; all fixed for the audit). #
# --------------------------------------------------------------------------- #
PLANTED_ALPHAS = (0.3, 0.5, 0.68, 0.8)        # same sweep as the first wave
N_SEEDS = 2                                    # SPEC (ii): >= 2 generator seeds
N_SYNTH = 3000                                 # synthetic inscriptions per (variant, alpha, seed)
N_MC = 10                                      # production-pinned N_MC for the recovery test
BASE_SEED = 20260619                           # this wave's base seed (distinct from run_c10's)
GENUINE_PGEN = "empire"                        # empire posterior p_gen (matches the first wave)
GENUINE_HALF_WIDTH = C.GENUINE_HALF_WIDTH_DEFAULT  # 2.5 y (R0 tight bracket)
DEFAULT_VARIANTS = list(C2.VARIANTS)           # R0, R1, R2, R3, R1+R2

# Decision thresholds.
RECOVERY_TOL = 0.1     # mass arm "recovers planted α" if max |mass − planted| <= this
DIVERGENCE_TOL = 0.15  # arms "diverge" if mean |mass − point-date| >= this (the 1c gap ≈ 0.52)
PILOT_FLOOR = 0.10     # the ~0.10 point-collapse floor the pilot + 1c showed


# =========================================================================== #
# Per-cell fit: generate one frame, recover α on both arms.                      #
# =========================================================================== #
def _fit_cell(variant: str, alpha: float, si: int, ai: int,
              slabs, basis: np.ndarray, tc_ab, tg_ab,
              p_gen: np.ndarray, width_dist, theta_conv: float, theta_gen: float,
              ) -> dict[str, Any]:
    """Generate one synthetic frame for ``(variant, alpha, seed)`` and fit both arms.

    Seeds are derived collision-free from BASE_SEED, the variant index, the planted-α
    index, and the seed index, so every cell is deterministic and independent.
    """
    vi = C2.VARIANTS.index(variant)
    gen_seed = BASE_SEED + 1_000_000 * vi + 1000 * ai + si
    mass_fit_seed = BASE_SEED + 100_000 + 1_000_000 * vi + 1000 * ai + si
    pt_base_seed = BASE_SEED + 300_000 + 1_000_000 * vi + 10_000 * ai + 1000 * si

    df = C2.generate_inscriptions_variant(
        variant, alpha, N_SYNTH, gen_seed, slabs, p_gen,
        width_dist=width_dist, theta_conv=theta_conv, theta_gen=theta_gen,
        genuine_half_width=GENUINE_HALF_WIDTH)
    realised_alpha = float((df["type"] == "convention").mean())
    theta_real = C2.realised_theta(df)

    # ---- mass arm (the validated recovery arm; REUSED from run_c10) ----
    mass = C.mass_cc_counts(df)
    t0 = time.time()
    mass_draws = RC._fit_mass_arm(
        mass["y_aligned"], mass["y_nonaligned"], mass["k"], mass["n_rows"],
        basis, tc_ab, tg_ab, mass_fit_seed)
    mass_secs = time.time() - t0
    mass_stats = RC._alpha_stats(mass_draws)

    # ---- point-date arm (the lodged C10 set_data loop; REUSED from run_c10) ----
    t0 = time.time()
    pt_stats = RC._fit_pointdate_arm(df, basis, tc_ab, tg_ab, pt_base_seed, N_MC)
    pt_secs = time.time() - t0

    divergence = abs(mass_stats["alpha_median"] - pt_stats["alpha_median"])
    return {
        "variant": variant,
        "planted_alpha": float(alpha),
        "seed_index": si,
        "gen_seed": gen_seed,
        "realised_alpha": realised_alpha,
        "theta_conv_realised": theta_real["theta_conv_realised"],
        "theta_gen_realised": theta_real["theta_gen_realised"],
        "n_aligned_raw": mass["n_aligned_raw"],
        "row_aligned_frac": mass["row_aligned_frac"],
        "mass_aligned_frac": mass["mass_aligned_frac"],
        "mass_arm": {**mass_stats, "delta_vs_planted": mass_stats["alpha_median"] - alpha,
                     "secs": round(mass_secs, 1)},
        "point_date_arm": {**pt_stats,
                           "delta_vs_planted": pt_stats["alpha_median"] - alpha,
                           "secs": round(pt_secs, 1)},
        "arm_divergence": divergence,
    }


# =========================================================================== #
# Per-variant verdict.                                                          #
# =========================================================================== #
def decide_variant(cells: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply the (ii) decision rule to one variant's sweep of cells.

    A variant REPRODUCES the 1c collapse if the mass arm still recovers planted α
    (max |mass − planted| <= RECOVERY_TOL) AND the point-date arm DIVERGES from the
    mass arm (mean |mass − point-date| >= DIVERGENCE_TOL) and/or collapses toward the
    pilot floor (median point-date α <= PILOT_FLOOR + RECOVERY_TOL).
    """
    planted = np.array([c["planted_alpha"] for c in cells], dtype=float)
    mass_med = np.array([c["mass_arm"]["alpha_median"] for c in cells], dtype=float)
    pt_med = np.array([c["point_date_arm"]["alpha_median"] for c in cells], dtype=float)
    diverg = np.array([c["arm_divergence"] for c in cells], dtype=float)

    mass_recovers = bool(np.all(np.abs(mass_med - planted) <= RECOVERY_TOL))
    mean_divergence = float(diverg.mean())
    arms_diverge = bool(mean_divergence >= DIVERGENCE_TOL)
    pt_near_floor = bool(np.median(pt_med) <= PILOT_FLOOR + RECOVERY_TOL)
    reproduces = bool(mass_recovers and (arms_diverge or pt_near_floor))

    return {
        "mass_recovers_within_tol": mass_recovers,
        "mass_max_abs_dev": float(np.abs(mass_med - planted).max()),
        "mean_arm_divergence": mean_divergence,
        "max_arm_divergence": float(diverg.max()),
        "arms_diverge": arms_diverge,
        "point_date_median_alpha": float(np.median(pt_med)),
        "point_date_near_pilot_floor": pt_near_floor,
        "reproduces_collapse": reproduces,
    }


def overall_verdict(per_variant: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Name which idealisation(s) reproduce the 1c collapse (the (ii) deliverable).

    R0 is the negative control (expected NOT to reproduce); R3 the confirmatory null
    (expected NOT to reproduce). The reproducing variant(s) name the missing
    real-data feature: R1 → realistic interval widths; R2 → θ contamination; R1+R2 →
    the joint effect.
    """
    reproducers = [v for v, d in per_variant.items() if d["reproduces_collapse"]]
    r0 = per_variant.get("R0", {})
    r3 = per_variant.get("R3", {})
    control_clean = (not r0.get("reproduces_collapse", True)) and \
                    (not r3.get("reproduces_collapse", True))

    if not reproducers:
        verdict = ("NO VARIANT reproduces the 1c collapse — the missing feature is "
                   "not interval widths, θ contamination, or true-date shape; "
                   "inspect the sweep / widen the realism grid.")
    else:
        verdict = ("REPRODUCED by: " + ", ".join(sorted(reproducers)) +
                   " — these idealisation(s) drive the point-date collapse seen on "
                   "real empire (1c).")
        if not control_clean:
            verdict += (" CAUTION: a control (R0) and/or the null (R3) ALSO "
                        "reproduced — the contrast is not clean; inspect.")
    return {
        "verdict": verdict,
        "reproducing_variants": sorted(reproducers),
        "control_clean": bool(control_clean),
        "recovery_tol": RECOVERY_TOL,
        "divergence_tol": DIVERGENCE_TOL,
        "pilot_floor": PILOT_FLOOR,
    }


# =========================================================================== #
# Report writer.                                                                #
# =========================================================================== #
def _write_report_md(path: Path, results: dict[str, Any]) -> None:
    """Write the human-readable FOLLOWUP-REPORT.md (per-variant tables + verdict)."""
    L = ["# C10 follow-up (ii) — realism-graded recovery report", ""]
    L.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    L.append("")
    cfg = results["config"]
    L.append(f"Variants: {', '.join(cfg['variants'])}. "
             f"Planted α: {cfg['planted_alphas']}; seeds: {cfg['n_seeds']}; "
             f"N_synth = {cfg['n_synth']}; N_MC = {cfg['n_mc']}; p_gen = {cfg['genuine_pgen']}.")
    L.append("")
    L.append("Real empire 1c reference (first wave): point-collapse α = 0.100, "
             "mass-preserving α = 0.615.")
    L.append("")

    if "verdict" in results:
        v = results["verdict"]
        L.append("## Verdict — which idealisation reproduces the collapse")
        L.append("")
        L.append(f"**{v['verdict']}**")
        L.append("")
        L.append(f"- reproducing variant(s): **{v['reproducing_variants']}**")
        L.append(f"- control clean (R0 + R3 do NOT reproduce): "
                 f"**{v['control_clean']}**")
        L.append(f"- thresholds: recovery_tol = {v['recovery_tol']}, "
                 f"divergence_tol = {v['divergence_tol']}, pilot_floor = {v['pilot_floor']}")
        L.append("")

    if "per_variant_verdict" in results:
        L.append("## Per-variant verdict summary")
        L.append("")
        L.append("| variant | mass recovers | mean arm divergence | point-date median α | "
                 "near floor | reproduces collapse |")
        L.append("|---|---|---|---|---|---|")
        for vname in results["config"]["variants"]:
            d = results["per_variant_verdict"][vname]
            L.append(f"| {vname} | {d['mass_recovers_within_tol']} | "
                     f"{d['mean_arm_divergence']:.3f} | {d['point_date_median_alpha']:.3f} | "
                     f"{d['point_date_near_pilot_floor']} | "
                     f"**{d['reproduces_collapse']}** |")
        L.append("")

    L.append("## Per-variant recovery tables")
    L.append("")
    for vname in results["config"]["variants"]:
        cells = [c for c in results["cells"] if c["variant"] == vname]
        if not cells:
            continue
        L.append(f"### {vname}")
        L.append("")
        L.append("| planted α | seed | realised α | θ_conv | θ_gen | "
                 "mass α (med [CI]) | point-date α (med [CI]) | divergence |")
        L.append("|---|---|---|---|---|---|---|---|")
        for c in cells:
            m, p = c["mass_arm"], c["point_date_arm"]
            L.append(f"| {c['planted_alpha']:.2f} | {c['seed_index']} | "
                     f"{c['realised_alpha']:.3f} | "
                     f"{c['theta_conv_realised']:.3f} | {c['theta_gen_realised']:.3f} | "
                     f"{m['alpha_median']:.3f} [{m['alpha_ci_lo']:.3f}, {m['alpha_ci_hi']:.3f}] | "
                     f"{p['alpha_median']:.3f} [{p['alpha_ci_lo']:.3f}, {p['alpha_ci_hi']:.3f}] | "
                     f"{c['arm_divergence']:.3f} |")
        L.append("")

    path.write_text("\n".join(L), encoding="utf-8")


# =========================================================================== #
# Driver.                                                                       #
# =========================================================================== #
def main() -> None:
    """Run the realism-graded recovery sweep and write results + report.

    POST-AUDIT RUN COMMAND (sapphire/zbook; do NOT run during build):
        cd /home/shawn/Code/inscriptions
        .venv/bin/python runs/2026-06-18-c10-validity-test/code/run_c10_ii.py \\
            --variants R0 R1 R2 R3 R1+R2
    """
    ap = argparse.ArgumentParser(
        description="C10 follow-up (ii) realism-graded recovery test driver.")
    ap.add_argument("--variants", nargs="+", default=DEFAULT_VARIANTS,
                    choices=list(C2.VARIANTS),
                    help=f"which variant(s) to run (default: {DEFAULT_VARIANTS})")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR,
                    help=f"output directory (default {OUT_DIR})")
    ap.add_argument("--out-prefix", type=str, default="followup-ii",
                    help="filename stem for results.json / report.md (default 'followup-ii')")
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Lodged production artefacts (read-only): basis, slabs, θ priors.
    basis, slabs = R.load_library_basis()
    tc_ab, tg_ab, theta_fit = R.adopted_theta_priors()
    # The production θ MEANS (for R2's contamination mix) — read from the artefact.
    theta_conv = float(theta_fit["theta_conv"])   # ≈ 0.930
    theta_gen = float(theta_fit["theta_gen"])      # ≈ 0.025
    p_gen, pgen_label = C.resolve_pgen(GENUINE_PGEN)

    # Real empire width distribution (for R1) — pure data profiling, NO MCMC.
    width_dist = C2.real_empire_width_dist("empire-aggregate")

    results: dict[str, Any] = {
        "spec": "runs/2026-06-18-c10-validity-test/SPEC.md (follow-up ii)",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "variants": list(args.variants),
            "planted_alphas": list(PLANTED_ALPHAS), "n_seeds": N_SEEDS,
            "n_synth": N_SYNTH, "n_mc": N_MC, "base_seed": BASE_SEED,
            "genuine_pgen": pgen_label, "genuine_half_width": GENUINE_HALF_WIDTH,
            "align_rule": R.ALIGN_RULE,
            "theta_conv_mean": theta_conv, "theta_gen_mean": theta_gen,
            "theta_conv_ab": list(tc_ab), "theta_gen_ab": list(tg_ab),
            "recovery_tol": RECOVERY_TOL, "divergence_tol": DIVERGENCE_TOL,
            "pilot_floor": PILOT_FLOOR,
            "width_dist_provenance": {
                "n_aligned": width_dist.n_aligned,
                "n_nonaligned": width_dist.n_nonaligned},
        },
        "cells": [],
        "per_variant_verdict": {},
    }

    for variant in args.variants:
        for ai, alpha in enumerate(PLANTED_ALPHAS):
            for si in range(N_SEEDS):
                cell = _fit_cell(
                    variant, alpha, si, ai, slabs, basis, tc_ab, tg_ab,
                    p_gen, width_dist, theta_conv, theta_gen)
                results["cells"].append(cell)
        v_cells = [c for c in results["cells"] if c["variant"] == variant]
        results["per_variant_verdict"][variant] = decide_variant(v_cells)

    results["verdict"] = overall_verdict(results["per_variant_verdict"])

    (args.out_dir / f"{args.out_prefix}-results.json").write_text(
        json.dumps(results, indent=2, default=float), encoding="utf-8")
    _write_report_md(args.out_dir / f"{args.out_prefix}-report.md", results)
    print(f"Wrote {args.out_dir / (args.out_prefix + '-results.json')} and "
          f"{args.out_dir / (args.out_prefix + '-report.md')}")


if __name__ == "__main__":
    main()
