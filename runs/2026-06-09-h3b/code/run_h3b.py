#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_h3b.py — DRAFT H3b deviation-detection driver.

Orchestrates the H3b pre-specified exploratory deviation-detection (see
``h3b-spec.md``):

  1. assemble per-unit corrected SPAs + raw intervals (reused H2.1 harness);
  2. per unit × null (exponential primary, CPL-3 secondary) run the forward-fit
     featureless-null envelope test (reused Phase-1 machinery);
  3. read the two pre-specified probe windows (Antonine, Crisis);
  4. Holm-adjust across the family (descriptive multiplicity diagnostic);
  5. run the two named replication probes (empire + Western-Empire-provincial =
     latin-aggregate for the Crisis; empire / unit-level for the Antonine, with
     the cult/military subsets flagged NOT-YET-BUILT);
  6. run the raw-vs-corrected follow-up;
  7. write ``outputs/deviations.json``, ``deviations-table.csv``,
     ``replication-antonine.json``, ``replication-crisis.json``.

Everything is DRAFT-FOR-REVIEW. Deterministic; master seed 20260609.

Usage
-----
    uv run python runs/2026-06-09-h3b/code/run_h3b.py [--n-mc N] [--quick]

Author: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

import h3b_lib as H

OUT_DIR = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-h3b/outputs")
NULLS = ("exponential", "cpl3")


def run_all(n_mc: int) -> dict:
    """Run the full DRAFT H3b pass and return a results bundle."""
    units = H.assemble_unit_data()
    print(f"Assembled {len(units)} units "
          f"({sum(u.identifiable for u in units)} identifiable).")

    # ---- Primary: per unit × null envelope test on the CORRECTED SPA. -------
    results: list[H.DeviationResult] = []
    for unit in units:
        rng = np.random.default_rng(H.MASTER_SEED + unit.unit_index)
        for null in NULLS:
            res = H.run_unit_null(unit, null, rng, n_mc=n_mc, signal="corrected")
            res.probes["antonine"] = H.summarise_probe(res, H.ANTONINE_WINDOW, "antonine")
            res.probes["crisis"] = H.summarise_probe(res, H.CRISIS_WINDOW, "crisis")
            results.append(res)
        print(f"  {unit.name:35s} "
              f"exp p={results[-2].pval_global:.3f} "
              f"cpl3 p={results[-1].pval_global:.3f} "
              f"{'[IDENT]' if unit.identifiable else '[flagged]'}")

    # ---- Holm across the CONFIRMATORY-ELIGIBLE family (identifiable units, ---
    # both nulls). Reported descriptively (spec §2 / OQ-1). A separate Holm is
    # computed across the flagged (exploratory) family for completeness.
    _apply_holm(results, restrict_identifiable=True, group="identifiable")
    _apply_holm(results, restrict_identifiable=False, group="flagged")

    # ---- Raw-vs-corrected follow-up (launch-spec §8) on identifiable units. --
    raw_compare = []
    for unit in (u for u in units if u.identifiable):
        rng = np.random.default_rng(H.MASTER_SEED + 100_000 + unit.unit_index)
        raw_res = H.run_unit_null(unit, "exponential", rng, n_mc=n_mc, signal="raw")
        raw_res.probes["antonine"] = H.summarise_probe(raw_res, H.ANTONINE_WINDOW, "antonine")
        raw_res.probes["crisis"] = H.summarise_probe(raw_res, H.CRISIS_WINDOW, "crisis")
        # Find the matching corrected exp result.
        corr = next(r for r in results if r.name == unit.name and r.null == "exponential")
        raw_compare.append({
            "name": unit.name,
            "corrected_exp_pval": corr.pval_global,
            "raw_exp_pval": raw_res.pval_global,
            "corrected_antonine_out": corr.probes["antonine"]["any_out_of_envelope"],
            "raw_antonine_out": raw_res.probes["antonine"]["any_out_of_envelope"],
            "corrected_crisis_out": corr.probes["crisis"]["any_out_of_envelope"],
            "raw_crisis_out": raw_res.probes["crisis"]["any_out_of_envelope"],
        })

    # ---- The two named replication probes. ----------------------------------
    antonine_rep = _antonine_replication(results)
    crisis_rep = _crisis_replication(results)

    return {
        "units": units,
        "results": results,
        "raw_compare": raw_compare,
        "antonine": antonine_rep,
        "crisis": crisis_rep,
        "n_mc": n_mc,
    }


def _apply_holm(
    results: list[H.DeviationResult],
    restrict_identifiable: bool,
    group: str,
) -> None:
    """Holm-adjust within a group (identifiable or flagged) and store on results."""
    members = [r for r in results
               if r.identifiable == restrict_identifiable]
    pvals = [r.pval_global for r in members]
    adj = H.holm_adjust(pvals)
    for r, a in zip(members, adj):
        r.pval_holm = a
        # tag the group for the table
        r.probes["_holm_group"] = group


def _antonine_replication(results: list[H.DeviationResult]) -> dict:
    """Antonine probe (AD 165–180) — empire/unit-level on existing corrected SPAs.

    The prereg names empire + Asclepius-cult + military-administration subsets.
    The cult/military subsets are NOT YET BUILT (need per-subset deconvolution +
    Phase-1 reachability + a LIRE membership rule — spec OQ-6); flagged here.
    """
    empire = next((r for r in results
                   if r.name == "empire-aggregate" and r.null == "exponential"), None)
    latin = next((r for r in results
                  if r.name == "latin-aggregate" and r.null == "exponential"), None)
    return {
        "window": list(H.ANTONINE_WINDOW),
        "empire_aggregate": (empire.probes["antonine"] | {"global_pval": empire.pval_global}
                             if empire else None),
        "latin_aggregate": (latin.probes["antonine"] | {"global_pval": latin.pval_global}
                            if latin else None),
        "asclepius_cult_subset": "NOT BUILT — needs per-subset deconvolution + "
                                 "Phase-1 reachability + LIRE membership rule (OQ-6)",
        "military_administration_subset": "NOT BUILT — same dependency (OQ-6)",
        "note": "Glomb et al. 2022 null at small N vs Duncan-Jones 2018 abrupt "
                "post-AD-167 cessation; no magnitude pre-committed (prereg line 101).",
    }


def _crisis_replication(results: list[H.DeviationResult]) -> dict:
    """Crisis probe (AD 235–284) — empire + Western-Empire-provincial subset.

    The Western-Empire-provincial subset (``province_language == 'Latin' AND
    province != 'Roma'``) IS the latin-aggregate unit (Rome excluded by
    construction). So both named subsets are directly runnable.
    """
    empire = next((r for r in results
                   if r.name == "empire-aggregate" and r.null == "exponential"), None)
    latin = next((r for r in results
                  if r.name == "latin-aggregate" and r.null == "exponential"), None)
    return {
        "window": list(H.CRISIS_WINDOW),
        "empire_aggregate": (empire.probes["crisis"] | {"global_pval": empire.pval_global}
                             if empire else None),
        "western_empire_provincial_latin_aggregate":
            (latin.probes["crisis"] | {"global_pval": latin.pval_global}
             if latin else None),
        "note": "Western-Empire-provincial subset = latin-aggregate "
                "(province_language=='Latin' AND province!='Roma'; Rome excluded "
                "by construction). Diffuse multi-decade decline; no magnitude "
                "pre-committed.",
    }


def _result_row(r: H.DeviationResult) -> dict:
    """Flatten one result for the CSV table."""
    return {
        "unit": r.name,
        "null": r.null,
        "n_eff": r.n_eff,
        "identifiable": r.identifiable,
        "holm_group": r.probes.get("_holm_group", ""),
        "pval_global": round(r.pval_global, 4),
        "pval_holm": (round(r.pval_holm, 4) if r.pval_holm is not None else ""),
        "detected_raw": r.detected,
        "n_bins_outside": r.n_bins_outside,
        "antonine_out": r.probes["antonine"]["any_out_of_envelope"],
        "antonine_dir": r.probes["antonine"]["direction"],
        "antonine_bracket": r.probes["antonine"]["descriptive_bracket"],
        "crisis_out": r.probes["crisis"]["any_out_of_envelope"],
        "crisis_dir": r.probes["crisis"]["direction"],
        "crisis_bracket": r.probes["crisis"]["descriptive_bracket"],
    }


def write_outputs(bundle: dict) -> None:
    """Write all JSON / CSV deliverables."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Full per-result JSON (drop the bulky envelope arrays into a compact form).
    dev = []
    for r in bundle["results"]:
        d = asdict(r)
        # Keep envelopes + observed but they are 80-long; retain for plotting.
        dev.append(d)
    (OUT_DIR / "deviations.json").write_text(
        json.dumps({"n_mc": bundle["n_mc"], "master_seed": H.MASTER_SEED,
                    "results": dev}, indent=2),
        encoding="utf-8",
    )

    # Flat table.
    rows = [_result_row(r) for r in bundle["results"]]
    with (OUT_DIR / "deviations-table.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    (OUT_DIR / "replication-antonine.json").write_text(
        json.dumps(bundle["antonine"], indent=2), encoding="utf-8")
    (OUT_DIR / "replication-crisis.json").write_text(
        json.dumps(bundle["crisis"], indent=2), encoding="utf-8")
    (OUT_DIR / "raw-vs-corrected.json").write_text(
        json.dumps(bundle["raw_compare"], indent=2), encoding="utf-8")

    print(f"Wrote outputs to {OUT_DIR}")


def main() -> None:
    """CLI entry point."""
    ap = argparse.ArgumentParser(description="DRAFT H3b deviation-detection.")
    ap.add_argument("--n-mc", type=int, default=H.N_MC,
                    help=f"MC replicate count (default {H.N_MC}).")
    ap.add_argument("--quick", action="store_true",
                    help="Quick smoke run with n_mc=100.")
    args = ap.parse_args()
    n_mc = 100 if args.quick else args.n_mc

    bundle = run_all(n_mc=n_mc)
    write_outputs(bundle)


if __name__ == "__main__":
    main()
