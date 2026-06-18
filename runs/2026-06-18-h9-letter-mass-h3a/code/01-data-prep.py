#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-data-prep.py --- Step 1 of the H9 letter-mass H3a confirmatory run.

Regenerate the city-level LETTER-MASS frame from raw LIRE v3.0, for BOTH the
H9 frames:

  - PRIMARY  = Latin-speaking provinces (Decision 36 / OSF Amendment 02).
  - SECONDARY/context = empire-wide (within the original lodged prereg text).

Per-city LETTER MASS (the H9 response) is the SUM, over a city's
date-window-filtered, Hanson-matched, Rome-excluded inscriptions, of the
per-inscription Latin-A--Z `letter_count_conservative` (primary content
measure; Amendment 01 §A5.1). The interpretive variant is built alongside as a
sensitivity. HARD-STOPs if the filtered row counts diverge from the prereg
targets, or if the Latin city count is far from the expected ~817.

This script is the H9 analogue of
`runs/2026-06-04-h3a-confirmatory/code/01-data-prep.py`; it changes only the
response variable (letter mass vs inscription count) and the primary/secondary
frame ordering (Latin primary vs empire primary).

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet  (raw, read-only)
runs/2026-06-18-h9-letter-mass-h3a/data/province-language-map.csv  (Latin frame)

Outputs
-------
runs/2026-06-18-h9-letter-mass-h3a/data/processed/city_level_for_h9_latin.parquet
runs/2026-06-18-h9-letter-mass-h3a/data/processed/city_level_for_h9_empire.parquet
runs/2026-06-18-h9-letter-mass-h3a/outputs/sample-counts.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-18, H9 build brief
(BUILD-AND-COMMIT-ONLY; no fit run).
"""

from __future__ import annotations

import json
import sys

import h9_common as H

# The per-inscription letter-count column summed into the per-city response.
# PRIMARY content measure: conservative (Amendment 01 §A5.1).
PRIMARY_LETTER_COL = "letter_count_conservative"
# Sensitivity content measure: interpretive (built and persisted alongside).
SENSITIVITY_LETTER_COL = "letter_count_interpretive"


def _letter_summary(frame, response="letter_mass") -> dict:
    """Compact descriptive summary of a per-city letter-mass response."""
    s = frame[response]
    return {
        "min": int(s.min()),
        "median": float(s.median()),
        "mean": float(s.mean()),
        "max": int(s.max()),
        "total": int(s.sum()),
        "n_zero": int((s == 0).sum()),
    }


def main() -> int:
    print(f"[01-data-prep] loading raw LIRE from {H.RAW_LIRE}")
    filtered = H.load_filtered_lire()
    print(f"[01-data-prep] filtered corpus: {len(filtered):,} rows "
          "(+ Latin-A--Z letter counts attached)")

    passed, observed, msgs = H.check_row_counts(filtered)
    print("[01-data-prep] row-level sanity-check vs prereg targets:")
    for m in msgs:
        print(m)
    if not passed:
        print("[01-data-prep] HARD-STOP: filtered row count diverges from "
              "180,609 / prereg targets by > 1%. Halting per spec.")
        return 1

    # Total corpus-wide letter mass under each measure (provenance / sanity).
    total_letters_cons = int(filtered[PRIMARY_LETTER_COL].sum())
    total_letters_intr = int(filtered[SENSITIVITY_LETTER_COL].sum())
    print(f"[01-data-prep] corpus letters (conservative, Latin A-Z): "
          f"{total_letters_cons:,}")
    print(f"[01-data-prep] corpus letters (interpretive, Latin A-Z): "
          f"{total_letters_intr:,}")

    H.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    counts: dict = {
        "filtered_rows": int(len(filtered)),
        "row_targets_observed": observed,
        "corpus_letters_conservative_latin_az": total_letters_cons,
        "corpus_letters_interpretive_latin_az": total_letters_intr,
        "primary_letter_col": PRIMARY_LETTER_COL,
        "frames": {},
    }

    # =====================================================================
    # PRIMARY frame: Latin-speaking provinces (Decision 36 / Amendment 02).
    # Both letter-mass measures are built; the conservative one is the
    # confirmatory response, the interpretive one is the sensitivity.
    # =====================================================================
    latin_cons = H.build_latin_frame(filtered, PRIMARY_LETTER_COL)
    n_latin = len(latin_cons)
    n_latin_prov = int(latin_cons["province"].nunique())
    print(f"[01-data-prep] PRIMARY (Latin, conservative): {n_latin:,} cities, "
          f"{n_latin_prov} Latin provinces")
    if not (750 <= n_latin <= 870):
        print(f"[01-data-prep] HARD-STOP: Latin city count {n_latin} far from "
              "expected ~817 (Decision 36 / Amendment 02). Mapping may be "
              "wrong. Halting.")
        return 1

    # Attach the interpretive letter mass as an extra column on the same Latin
    # cities (so a sensitivity fit can read one parquet). Build the interpretive
    # Latin frame and map its letter_mass onto the conservative frame by city.
    latin_intr = H.build_latin_frame(filtered, SENSITIVITY_LETTER_COL)
    intr_by_city = latin_intr.set_index("city")["letter_mass"]
    latin_cons["letter_mass_interpretive"] = (
        latin_cons["city"].map(intr_by_city).astype("int64")
    )
    latin_cons.to_parquet(H.LATIN_PARQUET, index=False)
    print(f"[01-data-prep]   -> {H.LATIN_PARQUET}")
    counts["frames"]["latin_primary"] = {
        "n_cities": n_latin,
        "n_provinces": n_latin_prov,
        "letter_mass_conservative_summary": _letter_summary(latin_cons),
        "letter_mass_interpretive_summary":
            _letter_summary(latin_cons, "letter_mass_interpretive"),
    }

    # =====================================================================
    # SECONDARY / context frame: empire-wide (within lodged prereg text).
    # =====================================================================
    empire_cons, empire_provs = H.build_empire_frame(filtered, PRIMARY_LETTER_COL)
    n_empire = len(empire_cons)
    n_empire_prov = len(empire_provs)
    print(f"[01-data-prep] SECONDARY (empire, conservative): {n_empire:,} "
          f"cities, {n_empire_prov} provinces")
    if not (1_000 <= n_empire <= 1_100):
        print(f"[01-data-prep] HARD-STOP: empire city count {n_empire} far from "
              "expected ~1,044. Halting.")
        return 1

    empire_intr, _ = H.build_empire_frame(filtered, SENSITIVITY_LETTER_COL)
    intr_by_city_e = empire_intr.set_index("city")["letter_mass"]
    empire_cons["letter_mass_interpretive"] = (
        empire_cons["city"].map(intr_by_city_e).astype("int64")
    )
    empire_cons.to_parquet(H.EMPIRE_PARQUET, index=False)
    print(f"[01-data-prep]   -> {H.EMPIRE_PARQUET}")
    counts["frames"]["empire_secondary"] = {
        "n_cities": n_empire,
        "n_provinces": n_empire_prov,
        "letter_mass_conservative_summary": _letter_summary(empire_cons),
        "letter_mass_interpretive_summary":
            _letter_summary(empire_cons, "letter_mass_interpretive"),
    }

    # --- counts sidecar ---------------------------------------------------
    out_json = H.RUN_DIR / "outputs" / "sample-counts.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(counts, indent=2))
    print(f"[01-data-prep]   -> {out_json}")
    print("[01-data-prep] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
