#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag-refit.py — basis-identifiability test for the unexpected-alpha units.

For each probe unit, refit the SAME observed y under a PER-UNIT convention basis
(the unit's own 3-tier round-period aoristic SPA; empty tiers fall back to the
shared Latin row) and compare alpha to the shared-basis production fit.

If alpha swings sharply (e.g. Moesia inferior 0.05 -> high), alpha is
basis-dependent for that unit: its convention IS present but period-shifted, so
the shared empire-wide basis cannot represent it and the production fit
under-attributes convention (the "corrected SPA" leaks convention as genuine).
A unit whose alpha is stable across bases (e.g. Noricum, the control) is
identifiable — its high alpha is real.
"""
from __future__ import annotations

import json
import numpy as np
import h2_lib as H

PROBE = [  # flagged (large F1+F3-vs-alpha gap) + controls
    "Moesia inferior", "Samnium / Regio IV", "Pannonia inferior", "Numidia",
    "Venetia et Histria / Regio X", "Salona", "Britannia", "Umbria / Regio VI",
    "Ostia", "Dacia",
    # controls (small/negative gap — expect stable alpha):
    "Noricum", "latin-aggregate", "Latium et Campania / Regio I",
]
TIER_DEFS = [[49], [99], [149, 199, 299]]  # sub / century / multi (Decision 38)


def normalise(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return v / s if s > 0 else v


def build_unit_basis(sub, shared: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """Per-unit 3-tier basis from the unit's own round-period (F1/F3-width) mass;
    empty tiers fall back to the shared row so p_conv is never degenerate."""
    rows, counts = [], []
    for i, widths in enumerate(TIER_DEFS):
        m = sub["date_range"].isin(widths).to_numpy()
        counts.append(int(m.sum()))
        if m.sum() == 0:
            rows.append(shared[i])
        else:
            rows.append(normalise(H.aoristic_spa(sub["nb"].to_numpy()[m], sub["na"].to_numpy()[m])))
    return np.vstack(rows), counts


def main() -> int:
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    design = H.load_design()
    units = {u["name"]: u for u in H.enumerate_units()}
    prod = {r["name"]: r for r in json.loads(
        (H.PROJECT_ROOT / "runs/2026-06-07-h2.1-launch-prep/outputs/production/summary.json")
        .read_text(encoding="utf-8"))}
    shared_latin = H.select_basis(design, "latin")

    print(f"{'unit':18s} {'n':>6s} {'a_shared':>9s} {'a_perunit':>10s} {'swing':>7s}  tier_counts conv")
    out = []
    for name in PROBE:
        u = units[name]
        sub = H.subset_corpus(df, u, latin)
        info = H.build_unit_y(sub)
        y = info["y"]
        per_basis, counts = build_unit_basis(sub, shared_latin)
        res = H.fit_unit(np.asarray(y, dtype=np.int64), per_basis,
                         seed=H.BASE_SEED + u["unit_index"] + 7000)
        a_shared = prod[name]["alpha_median"]
        a_unit = res["alpha_median"]
        rec = {"unit": name, "n": info["n_rows"], "alpha_shared": a_shared,
               "alpha_perunit": a_unit, "swing": a_unit - a_shared,
               "perunit_tier_counts": counts, "perunit_conv_pass": res["convergence_pass"]}
        out.append(rec)
        print(f"{name:18s} {info['n_rows']:6d} {a_shared:9.3f} {a_unit:10.3f} "
              f"{a_unit-a_shared:+7.3f}  {counts} conv={res['convergence_pass']}")

    (H.PROJECT_ROOT / "runs/2026-06-07-h2.1-launch-prep/outputs/production"
     / "diag-refit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("\nInterpretation: a large positive swing = convention present but period-shifted")
    print("(shared basis cannot see it -> production alpha under-attributes convention).")
    print("A near-zero swing for the control = alpha is identifiable there.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
