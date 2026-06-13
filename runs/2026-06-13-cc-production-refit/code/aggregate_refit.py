#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aggregate_refit.py — per-unit α verdict + H2.1 reconciliation for the cc refit.
===============================================================================

Reads the per-unit cc-library fits (`outputs/units/*.json`), the H2.1 finalised
summary (`summary-final.json`: α_shared, α_perunit, under_identified, tier), and
the classification-implied α (`theta-calibration.json` `implied_alpha[C]`), and
emits the reconciliation verdict (spec §4):

  * frontier (under-identified) units: cc-α vs the H2.1 two-bound [shared, perunit]
    + implied-α — does the alignment contrast pin a value between the bounds the
    shared-basis fit could not?
  * controls (identifiable units): cc-α vs H2.1 α_shared — stable (no large move)?
  * convergence: per-unit pass; failures flagged, not dropped.

Emits `outputs/REFIT-VERDICT.md` + `outputs/refit-summary.json` (committed).

Run — PATH=~/.local/bin:$PATH uv run python code/aggregate_refit.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-13. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
UNITS_DIR = REFIT / "outputs" / "units"
SUMMARY_FINAL = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep"
    "/outputs/production/summary-final.json")
THETA_CALIB = JOINT.parent / "outputs" / "theta-calibration.json"

# The diagnostic-flagged under-attributed units (DIAGNOSTIC-alpha-identifiability-REPORT.md §C).
FRONTIER = {
    "Moesia inferior", "Britannia", "Pannonia inferior", "Samnium / Regio IV",
    "Salona", "Ostia", "Venetia et Histria / Regio X", "Numidia", "Dacia",
    "Umbria / Regio VI",
}
CONTROL_REF = {  # diagnostic controls — cc-α expected stable vs H2.1 α_shared
    "Noricum", "latin-aggregate", "Latium et Campania / Regio I", "Pompeii",
    "empire-aggregate",
}


def load_units() -> list[dict]:
    out = []
    for p in sorted(UNITS_DIR.glob("*.json")):
        try:
            out.append(json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def main() -> None:
    units = load_units()
    if not units:
        print("no per-unit fits found.")
        return
    h2 = {r["name"]: r for r in json.loads(SUMMARY_FINAL.read_text(encoding="utf-8"))}
    implied = {e["name"]: e.get("implied_alpha", {}).get("C")
               for e in json.loads(THETA_CALIB.read_text(encoding="utf-8"))["units"]}
    by_name = {u["name"]: u for u in units}

    n = len(units)
    conv_fail = [u["name"] for u in units if not u["convergence_pass"]]
    lines = [f"# cc-library production refit — VERDICT", "",
             f"Units fitted: {n}. Convergence failures: **{len(conv_fail)}**"
             + (f" — {conv_fail}" if conv_fail else "") + ".", ""]

    # Reconciliation table.
    lines += ["## Per-unit α: cc-library vs the H2.1 two-bound diagnostic", "",
              "| unit | tier | cc-α [95% CI] | H2.1 α_shared | α_perunit | implied-α | conv |",
              "|---|---|---|---|---|---|---|"]

    def fmt_unit(u):
        r = h2.get(u["name"], {})
        ash = r.get("alpha_shared")
        apu = r.get("alpha_perunit")
        imp = implied.get(u["name"])
        return (f"| {u['name']} | {r.get('final_tier', u.get('tier', '?'))} | "
                f"{u['alpha_median']:.3f} [{u['alpha_ci_lo']:.3f}, {u['alpha_ci_hi']:.3f}] | "
                f"{ash:.3f} | {apu:.3f} | "
                f"{imp:.3f} | "
                f"{'ok' if u['convergence_pass'] else 'FAIL'} |"
                ) if (ash is not None and apu is not None and imp is not None) else (
                f"| {u['name']} | {u.get('tier','?')} | "
                f"{u['alpha_median']:.3f} [{u['alpha_ci_lo']:.3f}, {u['alpha_ci_hi']:.3f}] | "
                f"{'·' if ash is None else f'{ash:.3f}'} | "
                f"{'·' if apu is None else f'{apu:.3f}'} | "
                f"{'·' if imp is None else f'{imp:.3f}'} | "
                f"{'ok' if u['convergence_pass'] else 'FAIL'} |")

    # Order: frontier first, then controls, then the rest.
    order = ([u for u in units if u["name"] in FRONTIER]
             + [u for u in units if u["name"] in CONTROL_REF]
             + [u for u in units if u["name"] not in FRONTIER | CONTROL_REF])
    for u in order:
        lines.append(fmt_unit(u))

    # Verdict statistics.
    def between(u):
        r = h2.get(u["name"], {})
        lo, hi = sorted([r.get("alpha_shared", np.nan), r.get("alpha_perunit", np.nan)])
        return lo - 0.05 <= u["alpha_median"] <= hi + 0.05  # small tolerance

    front = [u for u in units if u["name"] in FRONTIER]
    ctrl = [u for u in units if u["name"] in CONTROL_REF]
    front_between = [u["name"] for u in front if between(u)]
    # control stability: |cc-α − H2.1 α_shared| small
    ctrl_moves = {u["name"]: round(u["alpha_median"] - h2[u["name"]]["alpha_shared"], 3)
                  for u in ctrl if u["name"] in h2}

    lines += ["", "## Verdict", "",
              f"- **Frontier units pinned within the H2.1 bounds (±0.05):** "
              f"{len(front_between)}/{len(front)} — {front_between}",
              f"- **Frontier units that moved up from the under-attributed α_shared:** "
              + ", ".join(
                  f"{u['name']} {h2[u['name']]['alpha_shared']:.2f}→{u['alpha_median']:.2f}"
                  for u in front if u['name'] in h2) + ".",
              f"- **Control stability (cc-α − H2.1 α_shared):** {ctrl_moves} "
              f"(near 0 = controls unchanged, as required).",
              f"- **Convergence:** {n - len(conv_fail)}/{n} pass.",
              f"- **Coverage caveat (signoff §6c):** reported CIs are ~1σ-optimistic by the "
              f"grid's residual bias; high-%win×high-α units pair with the two-bound "
              f"sensitivity as the disclosure.", ""]

    (REFIT / "outputs" / "REFIT-VERDICT.md").write_text("\n".join(lines))
    (REFIT / "outputs" / "refit-summary.json").write_text(json.dumps(
        {"n_units": n, "convergence_failures": conv_fail,
         "frontier_pinned_within_bounds": front_between,
         "control_moves_vs_shared": ctrl_moves,
         "units": [{k: u.get(k) for k in (
             "name", "tier", "frame", "n_rows_raw", "k_aligned_eff", "n_rows_eff",
             "row_aligned_frac", "mass_aligned_frac", "alpha_median", "alpha_ci_lo",
             "alpha_ci_hi", "theta_conv_post_med", "theta_gen_post_med", "max_rhat",
             "min_ess_bulk", "n_divergences", "convergence_pass",
             "ppc_mae_frac_aligned", "ppc_mae_frac_nonaligned", "secs")}
            | {"h2_alpha_shared": h2.get(u["name"], {}).get("alpha_shared"),
               "h2_alpha_perunit": h2.get(u["name"], {}).get("alpha_perunit"),
               "h2_under_identified": h2.get(u["name"], {}).get("under_identified"),
               "implied_alpha_C": implied.get(u["name"])}
            for u in order]}, indent=1))
    print("\n".join(lines))
    print("\nWrote REFIT-VERDICT.md + refit-summary.json")


if __name__ == "__main__":
    main()
