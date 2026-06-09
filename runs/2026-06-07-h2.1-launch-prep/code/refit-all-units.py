#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refit-all-units.py — operationalise the identifiability flag + two-bound alpha.

For EVERY production unit (28) plus the new 'Italia (excl. Rome)' aggregate (the
11 Augustan regiones), fit alpha under BOTH the shared per-frame basis and a
per-unit basis, and emit the two-bound alpha sensitivity range + the
identifiability flag (basis-swing > SWING_FLAG => under-identified). The shared
fit for the 28 reuses the production summary; Italia is fit fresh both ways.

Output: outputs/production/identifiability-table.{json,md}.
"""
from __future__ import annotations

import json
import numpy as np
import h2_lib as H

TIER_DEFS = [[49], [99], [149, 199, 299]]
SWING_FLAG = 0.20  # |per-unit alpha - shared alpha| above this => under-identified


def normalise(v):
    s = v.sum()
    return v / s if s > 0 else v


def per_unit_basis(sub, shared):
    rows = []
    for i, widths in enumerate(TIER_DEFS):
        m = sub["date_range"].isin(widths).to_numpy()
        rows.append(shared[i] if m.sum() == 0
                    else normalise(H.aoristic_spa(sub["nb"].to_numpy()[m], sub["na"].to_numpy()[m])))
    return np.vstack(rows)


def main() -> int:
    df = H.load_filtered_lire(); df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    design = H.load_design()
    units = H.enumerate_units()

    # Append Italia (excl. Rome) = all provinces whose name carries '/ Regio'.
    italian = sorted(p for p in df["province"].unique() if "Regio" in str(p))
    italia = {"name": "Italia (excl. Rome)", "kind": "aggregate", "frame": "latin",
              "tier": "aggregate-added", "unit_index": 100,
              "filter": ("province_in", italian)}
    units = units + [italia]

    prod = {r["name"]: r["alpha_median"] for r in json.loads(
        (H.PROJECT_ROOT / "runs/2026-06-07-h2.1-launch-prep/outputs/production/summary.json")
        .read_text(encoding="utf-8"))}

    rows = []
    for u in units:
        if u["filter"][0] == "province_in":
            sub = df.loc[df["province"].isin(u["filter"][1])]
        else:
            sub = H.subset_corpus(df, u, latin)
        info = H.build_unit_y(sub)
        y = np.asarray(info["y"], dtype=np.int64)
        shared_basis = H.select_basis(design, u["frame"])
        # shared alpha: reuse production where available, else fit
        if u["name"] in prod:
            a_shared = prod[u["name"]]
        else:
            a_shared = H.fit_unit(y, shared_basis, seed=H.BASE_SEED + u["unit_index"])["alpha_median"]
        a_unit = H.fit_unit(y, per_unit_basis(sub, shared_basis),
                            seed=H.BASE_SEED + u["unit_index"] + 7000)["alpha_median"]
        swing = a_unit - a_shared
        rows.append({
            "name": u["name"], "kind": u["kind"], "n_eff": info["n_eff"],
            "f1f3_frac": round(info["f1f3_family_mass_fraction"], 3),
            "alpha_shared": round(a_shared, 3), "alpha_perunit": round(a_unit, 3),
            "swing": round(swing, 3),
            "identifiable": bool(abs(swing) <= SWING_FLAG),
        })
        print(f"  {u['name']:30s} a=[{a_shared:.3f},{a_unit:.3f}] swing={swing:+.3f} "
              f"{'OK' if abs(swing)<=SWING_FLAG else 'UNDER-IDENTIFIED'}")

    rows.sort(key=lambda r: -r["swing"])
    out = H.PROJECT_ROOT / "runs/2026-06-07-h2.1-launch-prep/outputs/production"
    (out / "identifiability-table.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    n_flag = sum(1 for r in rows if not r["identifiable"])
    lines = ["# Identifiability table — two-bound alpha (shared vs per-unit basis)", "",
             f"Flagged under-identified (|swing| > {SWING_FLAG}): {n_flag}/{len(rows)}.", "",
             "| unit | n_eff | F1+F3 | alpha range [shared, per-unit] | swing | identifiable |",
             "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['name']} | {r['n_eff']} | {r['f1f3_frac']} | "
                     f"[{r['alpha_shared']}, {r['alpha_perunit']}] | {r['swing']:+.3f} | "
                     f"{'yes' if r['identifiable'] else '**NO**'} |")
    (out / "identifiability-table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[refit-all] {n_flag}/{len(rows)} under-identified; wrote identifiability-table.md/json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
