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

The corpus-wide DEFF is computed on inscriptions with letter > 0 (zero-letter
acts carry no letter mass). The per-city DEFF is reported for BOTH groupings,
explicitly labelled: ``urban_context_city`` (the analysis unit — PRIMARY, the
figure the paper cites) and ``place`` (raw findspot — SECONDARY). Rome is
excluded by an EXACT ``roma``/``rome`` test, never a loose substring.

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

# Candidate substrings for auto-detecting the conservative letter-count column.
# Ordered by preference.
LETTER_COL_HINTS = (
    "conservative",
    "letters_conservative",
    "letter_count_conservative",
    "n_letters_conservative",
)

# Per-city grouping is computed for BOTH of these, explicitly labelled, rather
# than silently auto-picking one (audit finding A1):
#   - ``urban_context_city`` is the ANALYSIS UNIT (Hanson urban-area city) — the
#     PRIMARY per-city DEFF the paper cites.
#   - ``place`` is the raw findspot — a SECONDARY view only.
GROUP_COLS = ("urban_context_city", "place")

# Rome-exclusion: EXACT match only ("roma"/"rome"). A loose contains("rom")
# over-matches Romula, Tauromenium, and Caesaromagus (see
# audit-verify-rome-and-deff.py), so we never use a substring test here.
ROME_TOKENS = ("roma", "rome")


def is_rome(name: object) -> bool:
    """EXACT Rome match: ``str(name).strip().lower() in ("roma", "rome")``."""
    return str(name).strip().lower() in ROME_TOKENS


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
    # The corpus DEFF is computed on inscriptions with letter > 0 (``w_pos``):
    # an inscription with 0 conservative letters carries no letter mass, so it
    # contributes nothing to the letter-weighted SPA whose design effect we are
    # measuring. (It still counts as one epigraphic act in the inscription-count
    # process; that process is the n=1 baseline, not the thing under test here.)
    # We report the zero-letter count separately for transparency.
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

    # Per-city design effect, reported for BOTH groupings explicitly (audit
    # finding A1): the time-series detection runs per subset/city, so the
    # corpus-wide number can mislead, and the choice of grouping column matters.
    print("\n" + "=" * 64)
    print("PER-CITY DESIGN EFFECT (analysis-unit view)")
    print("=" * 64)
    for group_col, role in (
        ("urban_context_city", "PRIMARY — analysis unit; the figure the paper cites"),
        ("place", "SECONDARY — raw findspot"),
    ):
        if group_col not in df.columns:
            print(f"\n(column '{group_col}' absent; skipping)")
            continue
        _per_city_deff(df, group_col, letter_col, role)
    return 0


def _per_city_deff(df: pd.DataFrame, group_col: str, letter_col: str,
                   role: str) -> None:
    """Report the per-city Kish DEFF summary for one grouping column.

    Rome (exact ``roma``/``rome`` only) is excluded, and only cities with at
    least 30 inscriptions (letter > 0) are summarised.
    """
    sub = df[[group_col, letter_col]].copy()
    sub = sub[sub[group_col].notna()]
    sub = sub[~sub[group_col].map(is_rome)]
    sub = sub[np.isfinite(sub[letter_col]) & (sub[letter_col] > 0)]
    deffs: list[float] = []
    for _, grp in sub.groupby(group_col):
        wv = grp[letter_col].to_numpy(dtype=float)
        if wv.size >= 30:  # only cities with enough inscriptions to matter
            s1 = wv.sum()
            s2 = (wv * wv).sum()
            deffs.append((wv.size * s2) / (s1 * s1))
    print(f"\ngrouping by '{group_col}'  ({role})")
    if not deffs:
        print("  no city had >= 30 inscriptions; skipping.")
        return
    deff_arr = np.array(deffs)
    n_cities = len(deff_arr)
    med_deff = float(np.median(deff_arr))
    print(f"  cities with >= 30 inscriptions (Rome-excluded): {n_cities}")
    print(f"  per-city DEFF (= 1 + CV^2 of letter counts within city):")
    print(f"    median  = {med_deff:.2f}")
    print(f"    25-75%  = [{np.percentile(deff_arr, 25):.2f}, "
          f"{np.percentile(deff_arr, 75):.2f}]")
    print(f"    10-90%  = [{np.percentile(deff_arr, 10):.2f}, "
          f"{np.percentile(deff_arr, 90):.2f}]")
    print(f"    max     = {deff_arr.max():.2f}")
    # Effective-N shrinkage at the median city.
    print(
        f"  interpretation: at the median city, the letter-mass SPA has "
        f"~1/{med_deff:.2f} = {1.0 / med_deff:.2f}x the effective N of the "
        f"inscription-count SPA for the SAME inscriptions."
    )


if __name__ == "__main__":
    sys.exit(main())
