#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""finalise-results.py — apply the identifiability flag + two-bound alpha to the
H2.1 production results, and add the 'Italia (excl. Rome)' aggregate unit.

Operationalises recommendations 1 (flag), 2 (two-bound alpha) and 4-Italia from
DIAGNOSTIC-alpha-identifiability-REPORT.md. Reads the per-unit production fits
(summary.json) and the two-bound identifiability table (identifiability-table.json),
fits Italia (shared Latin basis) for a complete record, and writes:

  - units/unit-29.json            (Italia full production record)
  - SUMMARY-FINAL.md              (flag + two-bound alpha + final tier per unit)
  - identifiable-units.json       (the confirmatory-eligible set for H3b)

Flag (family-fraction anchor): a unit UNDER-attributes convention when its shared
alpha sits far below its grid-alignment family fraction, gap = f1f3_frac - alpha.
  gap > 0.25  -> under-identified (correction unreliable)
  0.20 < gap <= 0.25 -> borderline
Tiers: review-nonconverged / under-identified / caveated-high-alpha (alpha>0.70,
identifiable) / confirmatory (converged, in-envelope, identifiable).
H3b confirmatory set = converged AND alpha<=0.70 AND identifiable (gap<=0.25).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import h2_lib as H

PROD = H.PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "outputs" / "production"
GAP_UNDER = 0.25
GAP_BORDER = 0.20


def main() -> int:
    summ = json.loads((PROD / "summary.json").read_text(encoding="utf-8"))
    idtab = {r["name"]: r for r in json.loads(
        (PROD / "identifiability-table.json").read_text(encoding="utf-8"))}

    # --- Fit Italia (excl. Rome) under the shared Latin basis for a full record ---
    df = H.load_filtered_lire(); df["family"] = H.classify_family(df)
    italian = sorted(p for p in df["province"].unique() if "Regio" in str(p))
    info = H.build_unit_y(df.loc[df["province"].isin(italian)])
    design = H.load_design()
    res = H.fit_unit(np.asarray(info["y"], dtype=np.int64),
                     H.select_basis(design, "latin"), seed=H.BASE_SEED + 100)
    italia = {"name": "Italia (excl. Rome)", "kind": "aggregate", "frame": "latin",
              "unit_index": 29, "n_eff": info["n_eff"], "n_rows": info["n_rows"],
              "f1f3_family_mass_fraction": info["f1f3_family_mass_fraction"],
              "prep_tier": "aggregate-added", **res}
    (PROD / "units" / "unit-29.json").write_text(json.dumps(italia, indent=2), encoding="utf-8")
    summ = [r for r in summ if r["name"] != "Italia (excl. Rome)"] + [italia]

    rows = []
    for r in summ:
        a = r["alpha_median"]; frac = r["f1f3_family_mass_fraction"]; gap = frac - a
        a_perunit = idtab.get(r["name"], {}).get("alpha_perunit")
        under = gap > GAP_UNDER
        border = GAP_BORDER < gap <= GAP_UNDER
        if not r["convergence_pass"]:
            tier = "review-nonconverged"
        elif under:
            tier = "under-identified"
        elif a > H.ALPHA_ENVELOPE:
            tier = "caveated-high-alpha"
        else:
            tier = "confirmatory"
        rows.append({
            "unit_index": r["unit_index"], "name": r["name"], "n_eff": r["n_eff"],
            "f1f3_frac": round(frac, 3), "alpha_shared": round(a, 3),
            "alpha_perunit": (round(a_perunit, 3) if a_perunit is not None else None),
            "gap_family_minus_alpha": round(gap, 3),
            "under_identified": bool(under), "borderline": bool(border),
            "in_envelope": bool(a <= H.ALPHA_ENVELOPE),
            "convergence_pass": bool(r["convergence_pass"]),
            "final_tier": tier,
            "confirmatory_eligible": bool(r["convergence_pass"] and a <= H.ALPHA_ENVELOPE and not under),
        })

    rows.sort(key=lambda x: x["unit_index"])
    (PROD / "identifiable-units.json").write_text(json.dumps(
        [r["name"] for r in rows if r["confirmatory_eligible"]], indent=2), encoding="utf-8")

    from collections import Counter
    tiers = Counter(r["final_tier"] for r in rows)
    elig = [r["name"] for r in rows if r["confirmatory_eligible"]]
    lines = ["# H2.1 production — FINAL SUMMARY (identifiability flag + two-bound alpha)", "",
             f"Units: {len(rows)} (incl. Italia). Final tiers: {dict(tiers)}.",
             f"Confirmatory-eligible (H3b set): {len(elig)} — {', '.join(elig)}.", "",
             "Flag = shared alpha far below grid-alignment family fraction "
             "(gap = f1f3_frac - alpha; >0.25 under-identified). alpha reported as a "
             "two-bound range [shared basis, per-unit basis] for transparency.", "",
             "| unit | n_eff | F1+F3 | alpha [shared, per-unit] | gap | flag | tier |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        pu = r["alpha_perunit"]
        rng = f"[{r['alpha_shared']}, {pu}]" if pu is not None else f"{r['alpha_shared']}"
        fl = "UNDER-ID" if r["under_identified"] else ("borderline" if r["borderline"] else "ok")
        lines.append(f"| {r['name']} | {r['n_eff']} | {r['f1f3_frac']} | {rng} "
                     f"| {r['gap_family_minus_alpha']:+.2f} | {fl} | {r['final_tier']} |")
    (PROD / "SUMMARY-FINAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (PROD / "summary-final.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    print(f"[finalise] Italia n_eff={info['n_eff']} alpha={res['alpha_median']:.3f} "
          f"conv={res['convergence_pass']}")
    print(f"[finalise] tiers={dict(tiers)}")
    print(f"[finalise] confirmatory-eligible (H3b): {len(elig)} units")
    print(f"[finalise] wrote SUMMARY-FINAL.md, summary-final.json, identifiable-units.json, units/unit-29.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
