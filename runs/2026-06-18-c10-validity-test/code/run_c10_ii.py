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
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path
from typing import Any

import numpy as np

RUN_DIR = Path("/home/shawn/Code/inscriptions/runs/2026-06-18-c10-validity-test")
CODE_DIR = RUN_DIR / "code"
OUT_DIR = RUN_DIR / "outputs"

# --------------------------------------------------------------------------- #
# Module-level handles populated by ``_wire`` so spawn workers re-import        #
# cleanly. The FIXED, NON-MCMC artefacts (library basis + slabs, adopted θ      #
# priors + means, the empire p_gen, the real-empire width distribution) are     #
# loaded ONCE PER WORKER by ``_wire`` and held here, so they are NOT pickled     #
# per task — only the four small cell-identity scalars (variant, α, seed-index, #
# α-index) cross the process boundary for each cell. This mirrors the proven    #
# supplementary-wave driver's ``_wire`` init                                    #
# (runs/2026-06-18-h2.1-supplementary-wave/code/run_supp_production.py).        #
# --------------------------------------------------------------------------- #
C2 = C = RC = H = J = R = None
_BASIS = _SLABS = _TC_AB = _TG_AB = None
_THETA_CONV = _THETA_GEN = _P_GEN = _PGEN_LABEL = _WIDTH_DIST = None


def _wire() -> None:
    """Import the shared modules + load the FIXED library / θ / p_gen / widths once.

    Called at the top of every worker task (idempotent: skips the load if already
    wired) and once in ``main``. Because the C10 modules live in ``CODE_DIR`` and
    ``c10_lib`` itself inserts the lodged ``h2_lib`` / ``joint_lib`` / ``refit_lib``
    directories onto ``sys.path``, a spawn worker only needs ``CODE_DIR`` on the path
    before importing them. The artefacts loaded here are ALL deterministic, NON-MCMC
    reads (the production library basis + slabs, the adopted θ priors + means, the
    empire posterior ``p_gen``, and the real-empire recorded-width distribution); they
    are the production identicals every cell shares, so they are loaded ONCE per worker
    (not re-loaded per task) and held at module level rather than pickled per task.
    """
    global C2, C, RC, H, J, R
    global _BASIS, _SLABS, _TC_AB, _TG_AB
    global _THETA_CONV, _THETA_GEN, _P_GEN, _PGEN_LABEL, _WIDTH_DIST
    if str(CODE_DIR) not in sys.path:
        sys.path.insert(0, str(CODE_DIR))
    import c10_ii_lib as _C2  # the new realism-graded generator
    import c10_lib as _C      # count builders; wires h2_lib / joint_lib / refit_lib
    import run_c10 as _RC      # REUSE the validated arm-fitters; no import side effects
    import h2_lib as _H
    import joint_lib as _J
    import refit_lib as _R
    C2, C, RC, H, J, R = _C2, _C, _RC, _H, _J, _R
    if _BASIS is not None:
        return  # already loaded once in this (worker) process — do not re-load
    # Lodged production artefacts (read-only): basis, slabs, θ priors + means.
    _BASIS, _SLABS = R.load_library_basis()
    _TC_AB, _TG_AB, theta_fit = R.adopted_theta_priors()
    _THETA_CONV = float(theta_fit["theta_conv"])   # ≈ 0.930
    _THETA_GEN = float(theta_fit["theta_gen"])     # ≈ 0.025
    _P_GEN, _PGEN_LABEL = C.resolve_pgen(GENUINE_PGEN)
    # Real empire width distribution (for R1) — pure data profiling, NO MCMC.
    _WIDTH_DIST = C2.real_empire_width_dist("empire-aggregate")

# --------------------------------------------------------------------------- #
# Module-level constants needed at argument-parse time (the variant tuple and    #
# the R0 tight half-width). These come from two cheap, side-effect-free imports  #
# of the in-tree libraries — pure Python constants, NO MCMC, NO artefact load.   #
# The full library / θ / p_gen / width artefacts are loaded lazily by ``_wire``  #
# (in the parent and, spawn-safely, in each worker), NOT here.                    #
# --------------------------------------------------------------------------- #
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
import c10_ii_lib as _C2_CONST  # noqa: E402  (the new realism-graded generator)
import c10_lib as _C_CONST  # noqa: E402  (also wires h2_lib / joint_lib / refit_lib)

# --------------------------------------------------------------------------- #
# Test configuration (mirrors run_c10's pinned config; all fixed for the audit). #
# --------------------------------------------------------------------------- #
PLANTED_ALPHAS = (0.3, 0.5, 0.68, 0.8)        # same sweep as the first wave
N_SEEDS = 2                                    # SPEC (ii): >= 2 generator seeds
N_SYNTH = 3000                                 # synthetic inscriptions per (variant, alpha, seed)
N_MC = 10                                      # production-pinned N_MC for the recovery test
BASE_SEED = 20260619                           # this wave's base seed (distinct from run_c10's)
GENUINE_PGEN = "empire"                        # empire posterior p_gen (matches the first wave)
GENUINE_HALF_WIDTH = _C_CONST.GENUINE_HALF_WIDTH_DEFAULT  # 2.5 y (R0 tight bracket)
DEFAULT_VARIANTS = list(_C2_CONST.VARIANTS)    # R0, R1, R2, R3, R1+R2
N_JOBS_DEFAULT = 10                            # cc-grid/SPEC convention (parallelise ACROSS cells)
MAX_TASKS_PER_CHILD_DEFAULT = 4               # recycle workers to bound PyMC/PyTensor memory growth

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
# Spawn-safe per-cell worker (parallelises ACROSS independent cells).           #
# =========================================================================== #
def _worker(variant: str, alpha: float, si: int, ai: int) -> dict[str, Any]:
    """Fit ONE cell ``(variant, α, seed)`` in a worker process (spawn-safe).

    Each cell is fully independent: it derives its own seeds collision-free from
    ``BASE_SEED`` + the (variant, α-index, seed-index) — IDENTICALLY to the sequential
    version, inside ``_fit_cell`` — generates its own synthetic frame, fits both arms,
    and returns a self-contained result dict. The worker therefore reproduces the
    sequential per-cell result bit-for-bit, independent of which order cells complete.

    Only the four small cell-identity scalars are pickled across the process boundary;
    the FIXED, shared library / θ / p_gen / width artefacts are (re-)loaded ONCE per
    worker by ``_wire`` (re-imported under spawn, not passed as a pickled closure) and
    read from module level. Each fit still runs cores = 1 (n_jobs parallelises ACROSS
    cells, cores = 1 WITHIN each — no negotiate-down of the per-fit sampler config).
    """
    _wire()  # spawn-safe: re-import the modules + load the FIXED artefacts once/worker
    return _fit_cell(
        variant, alpha, si, ai, _SLABS, _BASIS, _TC_AB, _TG_AB,
        _P_GEN, _WIDTH_DIST, _THETA_CONV, _THETA_GEN)


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

    Dispatch is PARALLELISED across cells (one cell = one ``(variant, α, seed)``) with
    a spawn-safe ``ProcessPoolExecutor`` (``--n-jobs`` worker processes, recycled every
    ``--max-tasks-per-child`` tasks); each cell still runs cores = 1 WITHIN its fit.
    Because every cell derives its own seeds from (variant, α-index, seed-index) inside
    ``_fit_cell`` — exactly as the sequential version did — and the per-variant
    aggregation is order-insensitive, the results are IDENTICAL to the sequential run
    regardless of completion order. Collected cells are placed back into the exact
    sequential enumeration order before aggregation, so the output JSON/MD is
    byte-for-byte the same as the sequential version (only dispatch changed).

    POST-AUDIT RUN COMMAND (sapphire/zbook; do NOT run during build):
        cd /home/shawn/Code/inscriptions
        TMPDIR=$HOME/tmp_grid_scratch \\
            .venv/bin/python runs/2026-06-18-c10-validity-test/code/run_c10_ii.py \\
            --variants R0 R1 R2 R3 R1+R2 --n-jobs 10
    """
    ap = argparse.ArgumentParser(
        description="C10 follow-up (ii) realism-graded recovery test driver.")
    ap.add_argument("--variants", nargs="+", default=DEFAULT_VARIANTS,
                    choices=list(_C2_CONST.VARIANTS),
                    help=f"which variant(s) to run (default: {DEFAULT_VARIANTS})")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR,
                    help=f"output directory (default {OUT_DIR})")
    ap.add_argument("--out-prefix", type=str, default="followup-ii",
                    help="filename stem for results.json / report.md (default 'followup-ii')")
    ap.add_argument("--n-jobs", type=int, default=N_JOBS_DEFAULT,
                    help=f"parallel worker processes ACROSS cells (cores=1 within each "
                         f"fit; cc-grid/SPEC convention, default {N_JOBS_DEFAULT}).")
    ap.add_argument("--max-tasks-per-child", type=int, default=MAX_TASKS_PER_CHILD_DEFAULT,
                    help=f"recycle a worker after this many cells, to bound PyMC / "
                         f"PyTensor memory growth (default {MAX_TASKS_PER_CHILD_DEFAULT}).")
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # Load the FIXED artefacts ONCE in the parent (basis, slabs, θ priors + means,
    # p_gen, real-empire widths) via the same spawn-safe ``_wire`` the workers use;
    # the parent reads the config-block values straight off the module-level handles.
    _wire()

    # Build the FLAT list of all cells (variant × α × seed) up front, IN THE SEQUENTIAL
    # ENUMERATION ORDER. Each carries its position so the collected results can be
    # placed back into that order regardless of completion order (order-independence).
    cell_specs: list[tuple[int, str, float, int, int]] = []
    for variant in args.variants:
        for ai, alpha in enumerate(PLANTED_ALPHAS):
            for si in range(N_SEEDS):
                cell_specs.append((len(cell_specs), variant, float(alpha), si, ai))

    results: dict[str, Any] = {
        "spec": "runs/2026-06-18-c10-validity-test/SPEC.md (follow-up ii)",
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "variants": list(args.variants),
            "planted_alphas": list(PLANTED_ALPHAS), "n_seeds": N_SEEDS,
            "n_synth": N_SYNTH, "n_mc": N_MC, "base_seed": BASE_SEED,
            "genuine_pgen": _PGEN_LABEL, "genuine_half_width": GENUINE_HALF_WIDTH,
            "align_rule": R.ALIGN_RULE,
            "theta_conv_mean": _THETA_CONV, "theta_gen_mean": _THETA_GEN,
            "theta_conv_ab": list(_TC_AB), "theta_gen_ab": list(_TG_AB),
            "recovery_tol": RECOVERY_TOL, "divergence_tol": DIVERGENCE_TOL,
            "pilot_floor": PILOT_FLOOR,
            "width_dist_provenance": {
                "n_aligned": _WIDTH_DIST.n_aligned,
                "n_nonaligned": _WIDTH_DIST.n_nonaligned},
        },
        "cells": [],
        "per_variant_verdict": {},
    }

    # Submit every cell to the spawn-safe pool; collect via as_completed (arrival
    # order), but slot each result back at its ORIGINAL index so the assembled
    # ``cells`` list is in the identical sequential order.
    by_index: list[dict[str, Any] | None] = [None] * len(cell_specs)
    t0 = time.time()
    n_done = 0
    print(f"C10 follow-up (ii): {len(cell_specs)} cells "
          f"({len(args.variants)} variants × {len(PLANTED_ALPHAS)} α × {N_SEEDS} seeds); "
          f"n_jobs {args.n_jobs}, max_tasks_per_child {args.max_tasks_per_child}.",
          flush=True)
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, variant, alpha, si, ai): idx
                for idx, variant, alpha, si, ai in cell_specs}
        for fut in as_completed(futs):
            idx = futs[fut]
            try:
                by_index[idx] = fut.result()
                n_done += 1
                cell = by_index[idx]
                print(f"[{n_done}/{len(cell_specs)}] {cell['variant']} "
                      f"α={cell['planted_alpha']:.2f} seed={cell['seed_index']} "
                      f"(mass {cell['mass_arm']['alpha_median']:.3f} / "
                      f"point-date {cell['point_date_arm']['alpha_median']:.3f})",
                      flush=True)
            except BrokenProcessPool:
                print("FATAL: worker pool broken (OOM?) — nothing was written; "
                      "re-run with a smaller --n-jobs.", flush=True)
                raise
    if any(c is None for c in by_index):  # defensive: a worker errored without breaking
        missing = [cell_specs[i][1:] for i, c in enumerate(by_index) if c is None]
        raise SystemExit(f"FATAL: {len(missing)} cell(s) returned no result: {missing}")

    results["cells"] = list(by_index)  # already in sequential enumeration order
    for variant in args.variants:
        v_cells = [c for c in results["cells"] if c["variant"] == variant]
        results["per_variant_verdict"][variant] = decide_variant(v_cells)

    results["verdict"] = overall_verdict(results["per_variant_verdict"])

    (args.out_dir / f"{args.out_prefix}-results.json").write_text(
        json.dumps(results, indent=2, default=float), encoding="utf-8")
    _write_report_md(args.out_dir / f"{args.out_prefix}-report.md", results)
    print(f"Wrote {args.out_dir / (args.out_prefix + '-results.json')} and "
          f"{args.out_dir / (args.out_prefix + '-report.md')} "
          f"in {(time.time() - t0) / 60:.1f} min.")


if __name__ == "__main__":
    main()
