#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""smoke-data.py — cheap data-layer sanity check for the H2.1 harness (no fitting).

Verifies: corpus loads (180,609), design + basis load, the 28 units enumerate,
and a few units build sane y / N_eff / family-mass fractions. Catches data/path
bugs before any pymc fit. Read-only.
"""
from __future__ import annotations

import numpy as np
import h2_lib as H


def main() -> int:
    print("[smoke-data] loading filtered corpus ...")
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    print(f"  corpus rows: {len(df):,}  | Latin provinces: {len(latin)}")

    design = H.load_design()
    print(f"  design.json OK; empire basis {np.asarray(design['tier_basis_empirical']).shape}")

    units = H.enumerate_units()
    print(f"  enumerated units: {len(units)} (expect 28)")
    print(f"  tiers: {dict((t, sum(1 for u in units if u['tier']==t)) for t in set(u['tier'] for u in units))}")

    # Build y for a representative few: both aggregates, the biggest province,
    # a city, and a grey-band province.
    probe = ["empire-aggregate", "latin-aggregate", "Latium et Campania",
             "Pompeii", "Lusitania"]
    print("\n  unit                      frame   n_rows   n_eff   F1+F3-mass-frac  basis")
    for name in probe:
        u = next(x for x in units if x["name"] == name)
        sub = H.subset_corpus(df, u, latin)
        info = H.build_unit_y(sub)
        basis = H.select_basis(design, u["frame"])
        print(f"  {name:24s}  {u['frame']:6s}  {info['n_rows']:6d}  {info['n_eff']:6d}"
              f"     {info['f1f3_family_mass_fraction']:.3f}        {basis.shape}")
        assert info["y"].sum() == info["n_eff"]
        assert len(info["y"]) == H.N_BINS

    print("\n[smoke-data] PASS — data layer sane.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
