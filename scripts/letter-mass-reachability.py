#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
letter-mass-reachability.py
===========================

Analytic (leading-order) letter-mass detection-reachability translation.

A city is eligible for confirmatory temporal deviation-detection at a given
bracket iff its inscription count clears the Phase-1 detection-power threshold
for that bracket. Under letter mass, detection power is (to leading order) a
function of the *effective* sample size of the letter-weighted SPA, not the
raw inscription count — so the eligibility rule becomes:

    eligible(letter mass)  <=>  n_eff = (sum w)^2 / sum(w^2)  >=  threshold

where w_i is the conservative letter count of inscription i. This script counts
how many cities clear each Phase-1 urban-area 50 %-over-50-years threshold
under inscription count (n) versus under letter mass (n_eff), and lists the
cities in the neighbourhood of the boundary.

Caveat (leading order). This treats the heavy-tailed letter weights purely as
an effective-N deflation (Kish). A full compound-process power simulation would
additionally capture how the tail reshapes the permutation null's distribution.
This analytic translation is the methods-paper baseline; the simulation is a
logged follow-up.

Thresholds (preregistration-draft.md §6 line 408; urban-area, 50 % over >= 50 y,
detection >= 0.80):
    exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549.

Run (on sapphire, via the grid venv; reads from stdin):
    ssh sapphire '/home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/python' \
        < scripts/letter-mass-reachability.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

PARQUET = Path(
    "/home/shawn/Code/inscriptions/runs/2026-05-26-letter-count-probe/"
    "data/lire-filtered-with-letters.parquet"
)
LETTER_COL = "letter_count_conservative"

# Phase-1 urban-area 50 %-over->=50-y thresholds (min n at detection >= 0.80).
THRESHOLDS = {
    "cpl-3-step": 1409,
    "cpl-3-gauss": 1549,
    "exp-gauss": 1854,
    "exp-step": 1923,
}

# Grouping columns to try (Hanson urban-area unit, then raw findspot).
GROUP_COLS = ("urban_context_city", "place")

# Rome-exclusion: the preregistration excludes Rome from city/urban analyses.
# EXACT match only ("roma"/"rome") — a loose contains("rom") over-matches
# Romula, Tauromenium, Caesaromagus (see audit-verify-rome-and-deff.py).
ROME_TOKENS = ("roma", "rome")


def per_city_table(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Per-city inscription count n and letter-mass effective N n_eff."""
    sub = df[[group_col, LETTER_COL]].copy()
    sub = sub[sub[group_col].notna()]
    sub = sub[np.isfinite(sub[LETTER_COL]) & (sub[LETTER_COL] > 0)]
    rows = []
    for city, grp in sub.groupby(group_col):
        w = grp[LETTER_COL].to_numpy(dtype=float)
        n = int(w.size)
        s1 = float(w.sum())
        s2 = float((w * w).sum())
        n_eff = (s1 * s1) / s2
        rows.append(
            {"city": str(city), "n": n, "n_eff": n_eff, "deff": n / n_eff}
        )
    return pd.DataFrame(rows).sort_values("n", ascending=False)


def is_rome(name: str) -> bool:
    """EXACT Rome match (the city actually called Rome), not a substring test.

    Uses ``str(name).strip().lower() in ("roma", "rome")``. An earlier loose
    ``contains("rom")`` test wrongly dropped legitimate target cities — Romula
    (N=54), Tauromenium, and the two Caesaromagus entries — verified in
    ``scripts/audit-verify-rome-and-deff.py``.
    """
    return str(name).strip().lower() in ROME_TOKENS


def main() -> int:
    if not PARQUET.exists():
        print(f"FATAL: parquet not found at {PARQUET}", file=sys.stderr)
        return 2
    df = pd.read_parquet(PARQUET, columns=list(GROUP_COLS) + [LETTER_COL])
    print(f"Loaded {PARQUET.name}: {len(df)} rows\n")

    for group_col in GROUP_COLS:
        if group_col not in df.columns:
            print(f"(column '{group_col}' absent; skipping)\n")
            continue
        tbl = per_city_table(df, group_col)
        # Rome-excluded view (the analysis convention).
        tbl_norome = tbl[~tbl["city"].map(is_rome)]

        print("=" * 70)
        print(f"GROUPING BY '{group_col}'  ({len(tbl)} cities; "
              f"{len(tbl_norome)} after Rome-exclusion)")
        print("=" * 70)

        print(f"{'threshold':<14} {'n>=thr (inscr)':>16} "
              f"{'n_eff>=thr (letter)':>20}")
        for label, thr in THRESHOLDS.items():
            n_insc = int((tbl_norome["n"] >= thr).sum())
            n_lett = int((tbl_norome["n_eff"] >= thr).sum())
            print(f"{label+' '+str(thr):<14} {n_insc:>16} {n_lett:>20}")

        # List the boundary neighbourhood: cities with n_eff >= 1000 OR
        # n >= the lowest threshold, so both sides of the line are visible.
        lo = min(THRESHOLDS.values())
        nbhd = tbl_norome[
            (tbl_norome["n_eff"] >= 1000) | (tbl_norome["n"] >= lo)
        ].copy()
        nbhd = nbhd.sort_values("n", ascending=False)
        print(f"\nboundary neighbourhood (Rome-excluded; "
              f"n_eff>=1000 or n>={lo}):")
        print(f"  {'city':<32} {'n':>7} {'n_eff':>9} {'DEFF':>6}  "
              f"{'letter-elig?':>12}")
        for _, r in nbhd.iterrows():
            elig = "YES" if r["n_eff"] >= lo else "no"
            print(f"  {r['city'][:32]:<32} {int(r['n']):>7} "
                  f"{r['n_eff']:>9.0f} {r['deff']:>6.2f}  {elig:>12}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
