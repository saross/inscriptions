#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_h3b_drawwise.py — Stage-B driver for the draw-wise H3b deviation test.
==========================================================================

Runs the uncertainty-propagating H3b (spec ``h3b-implementation-spec-2026-06-14.md``)
over the 29 cc-library units. For each unit × null (exp primary, cpl-3 secondary):

  1. build the featureless-null MC envelope once (``h3b_drawwise.build_envelope``);
  2. evaluate all ~8,000 genuine-SPA posterior draws against it, at λ=1.0 (primary)
     and λ=1.2 (the §A5.5 coverage-inflation sensitivity pair);
  3. summarise → marginal-*p* (headline) + P(deviation) + per-draw spread, and the
     two probe windows (Antonine, Crisis) with signed/one-sided readings;
  4. additionally evaluate the RAW (uncorrected) SPA against the same envelope
     (the raw-vs-corrected follow-up, launch-spec §8).

Then Holm-adjust the headline marginal-*p* family (descriptive only). Writes
``outputs/drawwise/{deviations.json,deviations-table.csv,replication-antonine.json,
replication-crisis.json,raw-vs-corrected.json}``. Local, permutation-only, no MCMC.

Usage:  uv run python runs/2026-06-09-h3b/code/run_h3b_drawwise.py
Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-06-09-h3b/code"))
import h3b_drawwise as E  # noqa: E402

DRAWS_DIR = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
OUT_DIR = ROOT / "runs/2026-06-09-h3b/outputs/drawwise"
LAMBDAS = [1.0, 1.2]                       # primary + coverage-inflation sensitivity
KIND_SEED_OFFSET = {"exp": 0, "cpl": 100000}   # disjoint per-null seed streams
NULLS = ["exp", "cpl"]
# Prereg-named probe scopes (highlighted; all 29 units are scanned regardless).
NAMED_ANTONINE = {"empire-aggregate"}
NAMED_CRISIS = {"empire-aggregate", "latin-aggregate"}


def _probe_block(dd_counts, env):
    return {"antonine": E.probe_window(dd_counts, env, E.ANTONINE_WINDOW),
            "crisis": E.probe_window(dd_counts, env, E.CRISIS_WINDOW)}


def main() -> None:
    t0 = time.time()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("self-test (engine == library) ...", flush=True)
    E.selftest_faithful()
    print("  passed.\nassembling 29 units ...", flush=True)
    units = E.assemble_units(DRAWS_DIR)
    print(f"  {len(units)} units with draws.", flush=True)

    results = []
    for u in units:
        draws_norm = E.load_draws_normalised(u["name"], DRAWS_DIR)        # (D,80)
        raw_counts = E.raw_aoristic_counts(u["nb"], u["na"], u["n_eff"]).astype(float)
        median_counts = np.median(draws_norm, axis=0) * u["n_eff"]        # CPL fit target
        for kind in NULLS:
            rng = np.random.default_rng(E.MASTER_SEED + KIND_SEED_OFFSET[kind] + u["unit_index"])
            env = E.build_envelope(kind, u, rng, cpl_target=median_counts)
            rec = {
                "name": u["name"], "unit_index": u["unit_index"], "null": kind,
                "frame": u["frame"], "tier": u["tier"], "n_eff": u["n_eff"],
                "alpha_median": u["alpha_median"],
                "alpha_ci": [u["alpha_ci_lo"], u["alpha_ci_hi"]],
                "gap_annotation": u["gap_annotation"],
                "soft_annotated": u["soft_annotated"], "reach_caveat": u["reach_caveat"],
                "n_bins_skipped": env["n_bins_skipped"], "null_fit": env["fit"],
                "seed": int(E.MASTER_SEED + KIND_SEED_OFFSET[kind] + u["unit_index"]),
                "lo_env": [float(x) for x in env["lo"]],
                "hi_env": [float(x) for x in env["hi"]],
                "null_mid": [float(x) for x in env["mid"]],
                "median_corrected_counts": [float(x) for x in median_counts],
            }
            for lam in LAMBDAS:
                dd = E.inflate_draws(draws_norm, lam) * u["n_eff"]
                _, p_d = E.eval_draws(dd, env)
                rec[f"lambda_{lam}"] = {**E.aggregate(p_d), "probes": _probe_block(dd, env)}
            # raw-vs-corrected follow-up: the raw observed SPA against the same null.
            _, p_raw = E.eval_draws(raw_counts[None, :], env)
            rec["raw_signal"] = {"global_p": float(p_raw[0])}
            results.append(rec)
        print(f"  [{u['unit_index']:2d}] {u['name']:<28} n_eff={u['n_eff']:>6} "
              f"marg_p(exp,λ1)={results[-2]['lambda_1.0']['marginal_p']:.3f}", flush=True)

    # Holm across the headline marginal-p family (λ=1.0), per null — descriptive only.
    for kind in NULLS:
        idxs = [i for i, r in enumerate(results) if r["null"] == kind]
        adj = E.holm_adjust([results[i]["lambda_1.0"]["marginal_p"] for i in idxs])
        for i, a in zip(idxs, adj):
            results[i]["holm_marginal_p_lambda1"] = a

    (OUT_DIR / "deviations.json").write_text(json.dumps(results, indent=1))
    _write_table(results)
    _write_replications(results)
    _write_raw_vs_corrected(results)
    print(f"\nwrote outputs → {OUT_DIR}  ({time.time()-t0:.1f}s)")


def _write_table(results) -> None:
    cols = ["name", "null", "n_eff", "alpha_median", "soft_annotated", "reach_caveat",
            "marginal_p", "p_deviation", "p_draw_lo", "p_draw_hi", "holm_marginal_p",
            "marginal_p_infl", "antonine_p_dev", "antonine_p_deficit",
            "crisis_p_dev", "crisis_p_deficit", "raw_global_p"]
    with (OUT_DIR / "deviations-table.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in results:
            a, infl = r["lambda_1.0"], r["lambda_1.2"]
            w.writerow([
                r["name"], r["null"], r["n_eff"], round(r["alpha_median"], 3),
                r["soft_annotated"], r["reach_caveat"],
                round(a["marginal_p"], 4), round(a["p_deviation"], 4),
                round(a["p_draw_lo"], 4), round(a["p_draw_hi"], 4),
                round(r.get("holm_marginal_p_lambda1", float("nan")), 4),
                round(infl["marginal_p"], 4),
                round(a["probes"]["antonine"]["p_window_dev"], 4),
                round(a["probes"]["antonine"].get("p_deficit", float("nan")), 4),
                round(a["probes"]["crisis"]["p_window_dev"], 4),
                round(a["probes"]["crisis"].get("p_deficit", float("nan")), 4),
                round(r["raw_signal"]["global_p"], 4),
            ])


def _write_replications(results) -> None:
    for label, window_key, named in [("antonine", "antonine", NAMED_ANTONINE),
                                     ("crisis", "crisis", NAMED_CRISIS)]:
        block = {"window": list(getattr(E, f"{label.upper()}_WINDOW")),
                 "named_scopes": sorted(named), "units": []}
        for r in results:
            a = r["lambda_1.0"]
            block["units"].append({
                "name": r["name"], "null": r["null"], "n_eff": r["n_eff"],
                "named_scope": r["name"] in named,
                "soft_annotated": r["soft_annotated"], "reach_caveat": r["reach_caveat"],
                "global_marginal_p": round(a["marginal_p"], 4),
                **{k: (round(v, 4) if isinstance(v, float) else v)
                   for k, v in a["probes"][window_key].items() if k != "window"},
            })
        (OUT_DIR / f"replication-{label}.json").write_text(json.dumps(block, indent=1))


def _write_raw_vs_corrected(results) -> None:
    block = []
    for r in results:
        block.append({
            "name": r["name"], "null": r["null"],
            "corrected_marginal_p": round(r["lambda_1.0"]["marginal_p"], 4),
            "raw_global_p": round(r["raw_signal"]["global_p"], 4),
        })
    (OUT_DIR / "raw-vs-corrected.json").write_text(json.dumps(block, indent=1))


if __name__ == "__main__":
    main()
