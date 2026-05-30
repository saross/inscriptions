#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit-verify-rome-and-deff.py
=============================

Verify two audit findings before correcting any published number (Obs 61 /
OSF Amendment 01):

1. Rome-exclusion over-match: `contains("rom")` vs exact Roma/Rome — which
   cities differ, and the corrected city-count denominators.
2. Per-city design effect grouped by the ANALYSIS UNIT (`urban_context_city`)
   vs the raw findspot (`place`) that the design-effect script auto-picked.

Read-only; reproduces the disputed figures from the source parquet.

Run (on sapphire, grid venv, stdin)::
    ssh sapphire '/home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/python' \
        < scripts/audit-verify-rome-and-deff.py

Author / Date: Claude (Opus 4.8, 1M context), 2026-05-30.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

PARQUET = (
    "/home/shawn/Code/inscriptions/runs/2026-05-26-letter-count-probe/"
    "data/lire-filtered-with-letters.parquet"
)
W = "letter_count_conservative"
THRESHOLDS = {"cpl-3-step": 1409, "cpl-3-gauss": 1549,
              "exp-gauss": 1854, "exp-step": 1923}


def deff_median(df, col, min_n=30):
    """Median/IQR per-city Kish design effect for cities with >= min_n insc."""
    sub = df[df[col].notna() & (df[W] > 0)]
    deffs = []
    for _, g in sub.groupby(col):
        w = g[W].to_numpy(float)
        if w.size >= min_n:
            s1, s2 = w.sum(), (w * w).sum()
            deffs.append(w.size * s2 / (s1 * s1))
    d = np.array(deffs)
    return len(d), np.median(d), np.percentile(d, 25), np.percentile(d, 75), d.max()


def main():
    df = pd.read_parquet(PARQUET)
    print(f"rows: {len(df)}")

    for col in ("urban_context_city", "place"):
        names = df[col].dropna().unique()
        loose = sorted(n for n in names if "rom" in str(n).lower())
        exact = sorted(n for n in names if str(n).lower() in ("roma", "rome"))
        spurious = sorted(set(loose) - set(exact))
        print(f"\n=== Rome match on '{col}' ===")
        print(f"  loose contains('rom') matches {len(loose)}: {loose}")
        print(f"  exact Roma/Rome matches {len(exact)}: {exact}")
        print(f"  SPURIOUSLY excluded by loose: {spurious}")
        # N for each spurious city.
        for s in spurious:
            n = int((df[col] == s).sum())
            print(f"    {s}: N={n}")

    # --- Corrected denominators (reachability groups by urban_context_city) ---
    print("\n=== eligibility denominator (urban_context_city) ===")
    for excl, label in (("loose", "contains('rom')"), ("exact", "Roma/Rome only")):
        names = df["urban_context_city"].dropna().unique()
        if excl == "loose":
            drop = {n for n in names if "rom" in str(n).lower()}
        else:
            drop = {n for n in names if str(n).lower() in ("roma", "rome")}
        sub = df[df["urban_context_city"].notna()
                 & ~df["urban_context_city"].isin(drop)
                 & (df[W] > 0)]
        per = sub.groupby("urban_context_city").agg(
            n=(W, "size"),
            n_eff=(W, lambda x: x.sum()**2 / (x.values**2).sum()),
        )
        n_cities = len(per)
        elig_insc = {lab: int((per["n"] >= t).sum()) for lab, t in THRESHOLDS.items()}
        elig_lett = {lab: int((per["n_eff"] >= t).sum()) for lab, t in THRESHOLDS.items()}
        print(f"  [{label}] cities={n_cities}")
        print(f"    eligible (inscription n>=thr): {elig_insc}")
        print(f"    eligible (letter   n_eff>=thr): {elig_lett}")

    # --- Per-city DEFF: analysis unit vs findspot ---
    print("\n=== per-city DEFF (>=30 insc, exact-Rome-excluded) ===")
    for col in ("urban_context_city", "place"):
        names = df[col].dropna().unique()
        drop = {n for n in names if str(n).lower() in ("roma", "rome")}
        sub = df[df[col].notna() & ~df[col].isin(drop)]
        nc, med, q25, q75, mx = deff_median(sub, col)
        print(f"  by '{col}': n_cities={nc}  median={med:.2f}  "
              f"IQR=[{q25:.2f},{q75:.2f}]  max={mx:.2f}")

    # --- Target-set count (urban_context_city, Hanson-matched, pre-clip) ---
    print("\n=== target set (urban_context_city, Hanson-matched, pre-clip) ===")
    for excl, label in (("loose", "contains('rom')"), ("exact", "Roma/Rome only")):
        m = df[df["urban_context_city"].notna() & df["urban_context_pop_est"].notna()]
        names = m["urban_context_city"].unique()
        if excl == "loose":
            drop = {n for n in names if "rom" in str(n).lower()}
        else:
            drop = {n for n in names if str(n).lower() in ("roma", "rome")}
        m = m[~m["urban_context_city"].isin(drop)]
        per = m.groupby("urban_context_city").size()
        tgt = int(((per >= 50) & (per < 1549)).sum())
        anchors = int((per >= 1549).sum())
        print(f"  [{label}] target(50<=N<1549)={tgt}  anchors(N>=1549)={anchors}")


if __name__ == "__main__":
    main()
