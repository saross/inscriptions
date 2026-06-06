#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""01-verify-convention-population.py — Decision 38 step-0 verification (read-only).

Purpose
-------
Re-verify, on the *preregistration-filtered* corpus (the population the H2.1
production model actually sees), the figures the Decision 38 convention-basis
redesign is built on:

1. The prereg filter reproduces 180,609 rows (empire frame).
2. The family classification (Tight / F2_Other / F1_round / F3_periodic / Big)
   split, so we know the size of the F1+F3 *calendar* convention pool that the
   new empirical slab-type basis is constructed from.
3. The 9 calendar slab-type frequencies *within* the prereg-filtered F1+F3 pool
   (the 2026-05-24 ``slab-type-weights.csv`` was built on UNFILTERED LIRE — this
   recomputes on the filtered corpus so the basis weights match the model's
   population).
4. The reign / dynasty / event LEAK into F1+F3 — the inscriptions whose
   ``[not_before, not_after]`` coincides with a historical-anchor interval and
   therefore (per Decision 38) belong in ``genuine`` but are currently swept into
   the convention pool by the width-accidental family classifier
   (e.g. ``[161, 180]`` Marcus → F3). Quantifies the mass the curated
   historical-anchor removal list must strip.

This script COMMITS NOTHING to the model and writes only diagnostic tables. It
is the empirical grounding for the PART-2 design proposal (historical-anchor
list + grouped ~3-tier empirical calendar-slab basis).

Lineage / consistency
---------------------
- Filter: identical to ``runs/2026-06-05-template-dictionary/code/scan_templates.py``
  (``load_filtered_lire``) → 180,609.
- ``classify_family`` / slab widths: identical to
  ``runs/2026-05-24-empirical-pconv/code/build-empirical-pconv.py`` and the
  2026-05-24 cohort analysis (F1_WIDTHS, F3_WIDTHS, round_aligned).
- Canonical historical-anchor intervals: the ``CANONICAL_REIGNS`` dictionary
  from ``scan_templates.py`` (descriptive labelling list), used here to measure
  the leak. The committed historical-anchor removal list is a separate PART-2
  artefact; this only measures how much mass it must address.

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet            (read-only; raw LIRE v3.0)
runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv  (Latin frame)

Outputs (runs/2026-06-06-convention-basis-redesign/outputs/tables/)
-------
family-split.csv          — per-family counts, both frames
slab-frequencies.csv      — 9 slab-type counts/weights within filtered F1+F3
anchor-leak.csv           — F1/F3 inscriptions on canonical anchor intervals

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-06.
UK/Australian English; Oxford comma. Read-only; deterministic (pure counting).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = (
    PROJECT_ROOT / "runs" / "2026-06-04-h3a-confirmatory" / "data"
    / "province-language-map.csv"
)
TBL_DIR = RUN_DIR / "outputs" / "tables"
TBL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Prereg envelope + expected filtered count (scan_templates.py).
# ---------------------------------------------------------------------------
ENVELOPE_MIN = -50
ENVELOPE_MAX = 350
EXPECTED_N = 180_609

# ---------------------------------------------------------------------------
# Family classifier constants (build-empirical-pconv.py). date_range is the
# EXCLUSIVE width (not_after - not_before); [1, 100] -> 99.
# ---------------------------------------------------------------------------
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4

SLAB_TYPES = {
    24: "quarter_century",
    49: "half_century",
    99: "century",
    149: "one_and_a_half_century",
    199: "two_century",
    299: "three_century",
    19: "twenty_year_window",
    29: "thirty_year_window",
    39: "forty_year_window",
}

# Canonical historical-anchor intervals (reigns/dynasties), from scan_templates.py
# CANONICAL_REIGNS. Endpoints are conventional accession/death years; matched
# here within +/- REIGN_TOL on both endpoints to measure the leak.
REIGN_TOL = 1
CANONICAL_REIGNS: dict[str, tuple[int, int]] = {
    "Augustan": (-27, 14),
    "Tiberian": (14, 37),
    "Caligulan": (37, 41),
    "Claudian": (41, 54),
    "Neronian": (54, 68),
    "Vespasianic": (69, 79),
    "Flavian": (69, 96),
    "Domitianic": (81, 96),
    "Nervan-Trajanic": (96, 117),
    "Trajanic": (98, 117),
    "Hadrianic": (117, 138),
    "Antonine-Pius": (138, 161),
    "Aurelian-Marcus": (161, 180),
    "Antonine-broad": (138, 192),
    "Commodan": (180, 192),
    "Severan-dynasty": (193, 235),
    "Septimius-Severus": (193, 211),
    "Caracallan": (212, 217),
    "Soldier-emperors": (235, 284),
    "Tetrarchic": (284, 305),
    "Constantinian": (306, 337),
}


def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    """True where x mod `mod` is in {0, 1, mod-1} (the family-classifier rule)."""
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def load_filtered_lire() -> pd.DataFrame:
    """Load LIRE v3.0 and apply the prereg filter (must yield EXPECTED_N rows)."""
    df = pd.read_parquet(DATA_PATH)
    is_geotemporal = (
        df["Latitude"].notna()
        & df["Longitude"].notna()
        & df["not_before"].notna()
        & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    in_envelope = (df["not_after"] >= ENVELOPE_MIN) & (df["not_before"] <= ENVELOPE_MAX)
    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["nb"] = sub["not_before"].astype(int)
    sub["na"] = sub["not_after"].astype(int)
    sub["date_range"] = (sub["na"] - sub["nb"]).astype(int)  # EXCLUSIVE width
    if len(sub) != EXPECTED_N:
        raise ValueError(
            f"Filtered corpus is {len(sub):,} rows; expected {EXPECTED_N:,}."
        )
    return sub


def classify_family(df: pd.DataFrame) -> pd.Categorical:
    """Family classification, identical to build-empirical-pconv.py."""
    nb = df["nb"].to_numpy()
    na = df["na"].to_numpy()
    dr = df["date_range"].to_numpy()

    f1_mask = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3_mask = (
        np.isin(dr, list(F3_WIDTHS))
        & round_aligned(nb, 10)
        & round_aligned(na, 10)
        & ~f1_mask
    )
    tight_mask = (dr <= TIGHT_MAX) & ~f1_mask & ~f3_mask
    big_mask = (dr >= 49) & ~f1_mask
    other_mask = ~(f1_mask | f3_mask | tight_mask | big_mask)

    family = np.full(len(df), "Big", dtype=object)
    family[f1_mask] = "F1_round"
    family[f3_mask] = "F3_periodic"
    family[tight_mask] = "Tight"
    family[other_mask] = "F2_Other"
    family[big_mask] = "Big"
    return pd.Categorical(
        family,
        categories=["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"],
        ordered=True,
    )


def latin_province_set() -> set[str]:
    """Latin-speaking province names (Decision 36 frame)."""
    lang_map = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    return set(lang_map.loc[lang_map["language"] == "Latin", "lire_province"])


def family_split(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """Per-family counts + percentages for one frame."""
    vc = df["family"].value_counts().reindex(
        ["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"]
    )
    out = vc.reset_index()
    out.columns = ["family", "n"]
    out["frame"] = label
    out["pct_of_frame"] = (100 * out["n"] / len(df)).round(2)
    return out[["frame", "family", "n", "pct_of_frame"]]


def slab_frequencies(conv: pd.DataFrame, label: str) -> pd.DataFrame:
    """9 slab-type counts/weights within the F1+F3 convention pool."""
    pool_n = len(conv)
    rows = []
    for width, name in SLAB_TYPES.items():
        n = int((conv["date_range"] == width).sum())
        rows.append(
            {
                "frame": label,
                "slab_name": name,
                "width_excl": int(width),
                "family": "F1" if width in F1_WIDTHS else "F3",
                "count": n,
                "weight": round(n / pool_n, 4) if pool_n else 0.0,
                "pct_of_pool": round(100 * n / pool_n, 2) if pool_n else 0.0,
            }
        )
    df = pd.DataFrame(rows).sort_values("count", ascending=False).reset_index(drop=True)
    # Any F1+F3 inscriptions whose width is not one of the 9 canonical slabs?
    accounted = df["count"].sum()
    df_extra = pd.DataFrame(
        [{"frame": label, "slab_name": "__unaccounted__", "width_excl": -1,
          "family": "?", "count": int(pool_n - accounted),
          "weight": round((pool_n - accounted) / pool_n, 4) if pool_n else 0.0,
          "pct_of_pool": round(100 * (pool_n - accounted) / pool_n, 2) if pool_n else 0.0}]
    )
    return pd.concat([df, df_extra], ignore_index=True)


def anchor_leak(conv: pd.DataFrame, label: str) -> pd.DataFrame:
    """F1/F3 inscriptions whose [nb, na] matches a canonical anchor interval.

    For each canonical reign/dynasty interval, count F1+F3 inscriptions whose
    endpoints both fall within +/- REIGN_TOL. These are the width-accidental
    leaks Decision 38's historical-anchor removal list must strip from convention.
    """
    nb = conv["nb"].to_numpy()
    na = conv["na"].to_numpy()
    rows = []
    matched_any = np.zeros(len(conv), dtype=bool)
    for name, (rlo, rhi) in CANONICAL_REIGNS.items():
        m = (np.abs(nb - rlo) <= REIGN_TOL) & (np.abs(na - rhi) <= REIGN_TOL)
        cnt = int(m.sum())
        matched_any |= m
        if cnt:
            rows.append(
                {"frame": label, "anchor": name, "lo": rlo, "hi": rhi,
                 "n_in_F1F3": cnt}
            )
    df = pd.DataFrame(rows).sort_values("n_in_F1F3", ascending=False) if rows else pd.DataFrame(
        columns=["frame", "anchor", "lo", "hi", "n_in_F1F3"]
    )
    total_leak = int(matched_any.sum())
    pool_n = len(conv)
    summary = pd.DataFrame(
        [{"frame": label, "anchor": "__TOTAL_LEAK__", "lo": -1, "hi": -1,
          "n_in_F1F3": total_leak,
          "pct_of_pool": round(100 * total_leak / pool_n, 4) if pool_n else 0.0}]
    )
    if not df.empty:
        df["pct_of_pool"] = (100 * df["n_in_F1F3"] / pool_n).round(4)
    return pd.concat([df, summary], ignore_index=True)


def main() -> None:
    print(f"Loading {DATA_PATH} ...")
    df = load_filtered_lire()
    df["family"] = classify_family(df)
    print(f"  empire-filtered rows: {len(df):,} (expected {EXPECTED_N:,})  OK")

    latin = latin_province_set()
    df_lat = df.loc[df["province"].isin(latin)].copy()
    print(f"  Latin-frame rows: {len(df_lat):,}")

    # --- Family split ---
    fs = pd.concat(
        [family_split(df, "empire"), family_split(df_lat, "latin")],
        ignore_index=True,
    )
    fs.to_csv(TBL_DIR / "family-split.csv", index=False)
    print("\n=== Family split ===")
    print(fs.to_string(index=False))

    # --- Convention pools (F1+F3) ---
    conv_emp = df[df["family"].isin(["F1_round", "F3_periodic"])].copy()
    conv_lat = df_lat[df_lat["family"].isin(["F1_round", "F3_periodic"])].copy()
    print(f"\nF1+F3 convention pool: empire={len(conv_emp):,}  latin={len(conv_lat):,}")

    # --- Slab frequencies ---
    sf = pd.concat(
        [slab_frequencies(conv_emp, "empire"), slab_frequencies(conv_lat, "latin")],
        ignore_index=True,
    )
    sf.to_csv(TBL_DIR / "slab-frequencies.csv", index=False)
    print("\n=== Slab-type frequencies within filtered F1+F3 (empire) ===")
    print(sf[sf["frame"] == "empire"].to_string(index=False))

    # --- Anchor leak ---
    al = pd.concat(
        [anchor_leak(conv_emp, "empire"), anchor_leak(conv_lat, "latin")],
        ignore_index=True,
    )
    al.to_csv(TBL_DIR / "anchor-leak.csv", index=False)
    print("\n=== Reign/event leak into F1+F3 (empire) ===")
    print(al[al["frame"] == "empire"].to_string(index=False))

    print("\nWrote: family-split.csv, slab-frequencies.csv, anchor-leak.csv")
    print("Done (read-only; nothing committed to the model).")


if __name__ == "__main__":
    main()
