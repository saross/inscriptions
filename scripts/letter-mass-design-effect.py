#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
letter-mass-design-effect.py
============================

Quantify the Kish design effect of using letter mass (a compound sum of
per-inscription letter counts) in place of inscription count (an equal-weight
count of epigraphic acts) as the unit for spline / permutation-envelope
detection analyses.

Motivation
----------
Letter mass is NOT a count of independent events: each inscription contributes
a *weight* equal to its letter count, and those weights are heavy-tailed
(monumental / formulary texts carry orders of magnitude more letters than
funerary fragments). The Phase-1 detection-power machinery assumes an
equal-weight count process; this script measures, empirically, how far letter
mass departs from that assumption.

Statistics reported (Kish, 1965)
--------------------------------
Let w_i be the conservative letter count of inscription i, n the number of
inscriptions, S1 = sum(w), S2 = sum(w**2).

- n_eff(letter) = S1**2 / S2          effective sample size of the
                                      letter-weighted SPA.
- DEFF          = n / n_eff = 1 + CV**2 (CV = coefficient of variation of w).
- n_eff(letter) / n = 1 / DEFF        letter-mass effective N relative to the
                                      inscription-count effective N (= n).
                                      <1 means letter mass has FEWER effective
                                      observations than inscription count.
- naive_overstatement = S2 / S1 = mean(w) * DEFF
                                      factor by which a naive "treat total
                                      letters as a count" run would overstate
                                      effective N (hence overstate power).

Run (on sapphire, via the grid venv; reads from stdin):
    ssh sapphire '/home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/python' \
        < scripts/letter-mass-design-effect.py

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

# Candidate substrings for auto-detecting the conservative letter-count column
# and a city/site grouping column. Ordered by preference.
LETTER_COL_HINTS = (
    "conservative",
    "letters_conservative",
    "letter_count_conservative",
    "n_letters_conservative",
)
CITY_COL_HINTS = ("place", "provenance", "findspot", "site", "city", "urban")


def _pick_column(cols: list[str], hints: tuple[str, ...]) -> list[str]:
    """Return columns whose lowercased name contains any hint, hint-order."""
    out: list[str] = []
    lower = {c: c.lower() for c in cols}
    for h in hints:
        for c in cols:
            if h in lower[c] and c not in out:
                out.append(c)
    return out


def design_effect(w: np.ndarray) -> dict[str, float]:
    """Compute Kish design-effect statistics for a weight vector w >= 0."""
    w = np.asarray(w, dtype=float)
    w = w[np.isfinite(w)]
    n = int(w.size)
    s1 = float(w.sum())
    s2 = float((w * w).sum())
    mean = s1 / n
    n_eff = (s1 * s1) / s2
    deff = n / n_eff
    cv2 = deff - 1.0
    return {
        "n": n,
        "mean_w": mean,
        "median_w": float(np.median(w)),
        "max_w": float(w.max()),
        "total_letters_S1": s1,
        "cv2": cv2,
        "deff": deff,
        "n_eff_letter": n_eff,
        "n_eff_over_n": n_eff / n,
        "naive_overstatement": s2 / s1,
    }


def main() -> int:
    if not PARQUET.exists():
        print(f"FATAL: parquet not found at {PARQUET}", file=sys.stderr)
        return 2
    df = pd.read_parquet(PARQUET)
    print(f"Loaded {PARQUET.name}: shape={df.shape}")
    print("Columns:")
    for c in df.columns:
        print(f"  - {c}  ({df[c].dtype})")

    # Detect the conservative letter-count column (numeric).
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    letter_candidates = [
        c for c in _pick_column(list(df.columns), LETTER_COL_HINTS)
        if c in numeric_cols
    ]
    print(f"\nNumeric letter-count candidates: {letter_candidates}")
    if not letter_candidates:
        print(
            "No numeric column matched the letter hints; "
            "inspect the column list above and re-run with an explicit column.",
            file=sys.stderr,
        )
        return 3
    letter_col = letter_candidates[0]
    print(f"Using letter-count column: '{letter_col}'")

    w = df[letter_col].to_numpy(dtype=float)
    # Keep only positive letter counts (an inscription with 0 conservative
    # letters carries no content mass; it still counts as one epigraphic act).
    w_pos = w[np.isfinite(w) & (w > 0)]
    n_total = int(np.isfinite(w).sum())
    n_zero = int((np.isfinite(w) & (w <= 0)).sum())

    print("\n" + "=" * 64)
    print("CORPUS-WIDE DESIGN EFFECT (letter mass vs inscription count)")
    print("=" * 64)
    print(f"inscriptions with finite letter count : {n_total}")
    print(f"  of which zero conservative letters  : {n_zero}")
    stats = design_effect(w_pos)
    print(f"\nletter weights w_i (conservative letters per inscription):")
    print(f"  mean(w)            = {stats['mean_w']:.1f}")
    print(f"  median(w)          = {stats['median_w']:.1f}")
    print(f"  max(w)             = {stats['max_w']:.0f}")
    print(f"  total letters S1   = {stats['total_letters_S1']:.3e}")
    print(f"  CV^2               = {stats['cv2']:.2f}")
    print(f"\nKish design effect:")
    print(f"  DEFF = 1 + CV^2    = {stats['deff']:.2f}")
    print(f"  n (inscriptions)   = {stats['n']}")
    print(f"  n_eff (letter SPA) = {stats['n_eff_letter']:.1f}")
    print(
        f"  n_eff/n            = {stats['n_eff_over_n']:.4f}  "
        f"(<1 => letter mass has FEWER effective obs than inscription count)"
    )
    print(
        f"  naive overstatement= {stats['naive_overstatement']:.1f}x  "
        f"(factor by which 'total letters as a count' overstates effective N)"
    )

    # Per-city design effect at the analysis unit (time-series detection runs
    # per subset/city, so the corpus-wide number can mislead).
    city_candidates = _pick_column(list(df.columns), CITY_COL_HINTS)
    print("\n" + "=" * 64)
    print("PER-CITY DESIGN EFFECT (analysis-unit view)")
    print("=" * 64)
    print(f"city/site column candidates: {city_candidates}")
    if not city_candidates:
        print("No city/site column detected; skipping per-city view.")
        return 0
    city_col = city_candidates[0]
    print(f"Using grouping column: '{city_col}'")

    sub = df[[city_col, letter_col]].copy()
    sub = sub[np.isfinite(sub[letter_col]) & (sub[letter_col] > 0)]
    deffs = []
    for _, grp in sub.groupby(city_col):
        wv = grp[letter_col].to_numpy(dtype=float)
        if wv.size >= 30:  # only cities with enough inscriptions to matter
            s1 = wv.sum()
            s2 = (wv * wv).sum()
            deffs.append((wv.size, (wv.size * s2) / (s1 * s1)))
    if not deffs:
        print("No city had >= 30 inscriptions; skipping per-city summary.")
        return 0
    n_cities = len(deffs)
    deff_arr = np.array([d for _, d in deffs])
    size_arr = np.array([s for s, _ in deffs])
    print(f"\ncities with >= 30 inscriptions: {n_cities}")
    print(f"per-city DEFF (= 1 + CV^2 of letter counts within city):")
    print(f"  median  = {np.median(deff_arr):.2f}")
    print(f"  25-75%  = [{np.percentile(deff_arr, 25):.2f}, "
          f"{np.percentile(deff_arr, 75):.2f}]")
    print(f"  10-90%  = [{np.percentile(deff_arr, 10):.2f}, "
          f"{np.percentile(deff_arr, 90):.2f}]")
    print(f"  max     = {deff_arr.max():.2f}")
    # Effective-N shrinkage at the median city.
    med_deff = float(np.median(deff_arr))
    print(
        f"\ninterpretation: at the median city, the letter-mass SPA has "
        f"~1/{med_deff:.2f} = {1.0/med_deff:.2f}x the effective N of the "
        f"inscription-count SPA for the SAME inscriptions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
