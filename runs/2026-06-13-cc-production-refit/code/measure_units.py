#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
measure_units.py — empirical inputs for the cc-library production-refit spec.
=============================================================================

Before wiring the recovery-validated cross-classified `library` model to real
units, two design decisions need data (not assumption):

1. **k / n_rows definition.** The cc factorisation forces ``k = y_aligned.sum()``
   (aoristic-effective counts), but θ was calibrated on *row* aligned-fractions
   (`calibrate_theta.py`). This script measures, per unit, the row aligned-fraction
   vs the aoristic-mass aligned-fraction, so we can quantify the θ-transfer
   approximation under the aoristic-consistent choice (envelope clipping hits wide
   aligned intervals hardest, so the two can diverge).

2. **Per-unit slab catalogue.** Signoff §2's production analogue is "the
   deterministic aoristic boxes of the distinct grid-aligned interval types
   observed in the unit". This script measures, per unit, how many distinct
   grid-aligned (nb, na) interval types exist, how much aligned mass the top-K
   cover, and the width distribution — so the catalogue rule does not explode into
   near-collinear Dirichlet rows.

Read-only; pandas/numpy only (no PyMC), so it runs anywhere the corpus is present.

Run — PATH=~/.local/bin:$PATH uv run python code/measure_units.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-13. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402

ALIGN_RULE = "C"   # lead rule (matches θ calibration + the grid)


def aligned_mass_fraction(sub, aligned_mask_sub) -> tuple[float, float, float, float]:
    """(total_mass, aligned_mass, nonaligned_mass, mass_aligned_frac) for a unit."""
    nb = sub["nb"].to_numpy()
    na = sub["na"].to_numpy()
    total = float(H.aoristic_spa(nb, na).sum())
    al = float(H.aoristic_spa(nb[aligned_mask_sub], na[aligned_mask_sub]).sum())
    non = float(H.aoristic_spa(nb[~aligned_mask_sub], na[~aligned_mask_sub]).sum())
    return total, al, non, (al / total if total > 0 else float("nan"))


def catalogue_stats(sub, aligned_mask_sub) -> dict:
    """Distinct grid-aligned (nb, na) interval-type stats for the unit's aligned
    subset: count, cumulative aligned-row coverage by the top-K most frequent
    types, and the aligned-width distribution."""
    al = sub.loc[aligned_mask_sub]
    if len(al) == 0:
        return {"n_aligned_rows": 0, "n_distinct_types": 0}
    types = Counter(zip(al["nb"].to_numpy().tolist(), al["na"].to_numpy().tolist()))
    n_distinct = len(types)
    ordered = types.most_common()
    n_al = len(al)
    cum = {}
    run = 0
    for k_top in (5, 10, 15, 20, 30):
        run = sum(c for _, c in ordered[:k_top])
        cum[f"top{k_top}_rowcov"] = round(run / n_al, 3)
    widths = (al["na"] - al["nb"]).to_numpy()
    return {
        "n_aligned_rows": int(n_al),
        "n_distinct_types": int(n_distinct),
        "top_types": [{"nb": int(nb), "na": int(na), "n": int(c)}
                      for (nb, na), c in ordered[:12]],
        "cum_rowcov": cum,
        "width_pctiles": {p: int(np.percentile(widths, p)) for p in (10, 50, 90, 99)},
        "frac_width_ge_49": round(float((widths >= 49).mean()), 3),  # "Big/F1 wide slab" share
    }


def main() -> None:
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    units = H.enumerate_units()
    aligned_full = J.aligned_indicator(df, rule=ALIGN_RULE)  # bool over full df
    idx_full = df.index

    out = []
    for u in units:
        sub = H.subset_corpus(df, u, latin)
        loc = idx_full.get_indexer(sub.index)
        amask = aligned_full[loc]
        n_rows = int(len(sub))
        n_aligned_rows = int(amask.sum())
        row_frac = float(n_aligned_rows / n_rows) if n_rows else float("nan")
        total, al_m, non_m, mass_frac = aligned_mass_fraction(sub, amask)
        rec = {
            "name": u["name"], "kind": u["kind"], "tier": u["tier"], "frame": u["frame"],
            "n_rows": n_rows,
            "n_aligned_rows": n_aligned_rows,
            "row_aligned_frac": round(row_frac, 4),
            "mass_total": round(total, 1),
            "mass_aligned": round(al_m, 1),
            "mass_nonaligned": round(non_m, 1),
            "mass_aligned_frac": round(mass_frac, 4),
            "row_minus_mass_frac": round(row_frac - mass_frac, 4),
            **catalogue_stats(sub, amask),
        }
        out.append(rec)

    (REFIT / "outputs" / "unit-measurements.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")

    # Console summary — the two decisions.
    print(f"Units: {len(out)}\n")
    print("=== k/n_rows: row aligned-frac vs aoristic-mass aligned-frac ===")
    print(f"{'unit':34s} {'nrow':>6s} {'rowAF':>6s} {'massAF':>6s} {'Δ':>6s}")
    deltas = []
    for r in out:
        deltas.append(abs(r["row_minus_mass_frac"]))
        print(f"{r['name'][:34]:34s} {r['n_rows']:6d} {r['row_aligned_frac']:6.3f} "
              f"{r['mass_aligned_frac']:6.3f} {r['row_minus_mass_frac']:+6.3f}")
    print(f"\nmean |row−mass aligned-frac| = {np.mean(deltas):.4f}; "
          f"max = {np.max(deltas):.4f}")

    print("\n=== catalogue: distinct grid-aligned interval types per unit ===")
    print(f"{'unit':34s} {'nAlg':>6s} {'nTypes':>7s} {'top10':>6s} {'top20':>6s} {'w50':>5s} {'w≥49':>5s}")
    for r in out:
        if r.get("n_distinct_types", 0) == 0:
            print(f"{r['name'][:34]:34s} {0:6d}    (no aligned rows)")
            continue
        c = r["cum_rowcov"]
        w50 = r["width_pctiles"].get(50, r["width_pctiles"].get("50"))
        print(f"{r['name'][:34]:34s} {r['n_aligned_rows']:6d} {r['n_distinct_types']:7d} "
              f"{c['top10_rowcov']:6.2f} {c['top20_rowcov']:6.2f} "
              f"{w50:5d} {r['frac_width_ge_49']:5.2f}")
    nt = [r["n_distinct_types"] for r in out if r.get("n_distinct_types")]
    print(f"\ndistinct-types: min {min(nt)}, median {int(np.median(nt))}, max {max(nt)}")
    print(f"\nWrote {REFIT / 'outputs' / 'unit-measurements.json'}")


if __name__ == "__main__":
    main()
