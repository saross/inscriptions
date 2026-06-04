#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-data-prep.py --- Step 1 of the H3a confirmatory run.

Regenerate the canonical city-level frame from raw LIRE v3.0 and emit the
primary parquet plus the three sensitivity frames. HARD-STOPs if the filtered
row counts diverge from the prereg targets.

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet  (raw, read-only)
runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv  (Sensitivity B)

Outputs
-------
data/processed/city_level_for_h3a.parquet              (PRIMARY, 1,044 cities)
data/processed/city_level_for_h3a_with_zeros.parquet   (Sensitivity A)
data/processed/city_level_for_h3a_latin.parquet        (Sensitivity B, ~815)
runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-04, blind-run brief.
"""

from __future__ import annotations

import json
import sys

import h3a_common as H


def main() -> int:
    print(f"[01-data-prep] loading raw LIRE from {H.RAW_LIRE}")
    filtered = H.load_filtered_lire()
    print(f"[01-data-prep] filtered corpus: {len(filtered):,} rows")

    passed, observed, msgs = H.check_row_counts(filtered)
    print("[01-data-prep] row-level sanity-check vs prereg targets:")
    for m in msgs:
        print(m)
    if not passed:
        print("[01-data-prep] HARD-STOP: filtered row count diverges from "
              "180,609 / prereg targets by > 1%. Halting per spec.")
        return 1

    # --- PRIMARY frame ----------------------------------------------------
    primary, provinces = H.build_primary_frame(filtered)
    n_primary = len(primary)
    n_prov = len(provinces)
    print(f"[01-data-prep] PRIMARY: {n_primary:,} cities, {n_prov} provinces")
    if not (1_000 <= n_primary <= 1_100):
        print(f"[01-data-prep] HARD-STOP: primary city count {n_primary} far "
              "from expected ~1,044. Halting.")
        return 1
    H.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    primary.to_parquet(H.PRIMARY_PARQUET, index=False)
    print(f"[01-data-prep]   -> {H.PRIMARY_PARQUET}")

    # --- Sensitivity A: with-zeros ----------------------------------------
    with_zeros = H.build_with_zeros_frame(filtered)
    n_with_zeros = len(with_zeros)
    n_zero_cities = int((with_zeros["inscription_count"] == 0).sum())
    print(f"[01-data-prep] WITH-ZEROS: {n_with_zeros:,} cities "
          f"({n_zero_cities} structural zeros added)")
    with_zeros.to_parquet(H.WITHZEROS_PARQUET, index=False)
    print(f"[01-data-prep]   -> {H.WITHZEROS_PARQUET}")

    # --- Sensitivity B: Latin-only ----------------------------------------
    latin = H.build_latin_frame(filtered)
    n_latin = len(latin)
    print(f"[01-data-prep] LATIN-ONLY: {n_latin:,} cities "
          f"({latin['province'].nunique()} Latin provinces)")
    if not (750 <= n_latin <= 870):
        print(f"[01-data-prep] HARD-STOP: Latin city count {n_latin} far from "
              "expected ~815. Mapping may be wrong. Halting.")
        return 1
    latin.to_parquet(H.LATIN_PARQUET, index=False)
    print(f"[01-data-prep]   -> {H.LATIN_PARQUET}")

    # --- counts sidecar ---------------------------------------------------
    counts = {
        "filtered_rows": int(len(filtered)),
        "row_targets_observed": observed,
        "primary_n_cities": n_primary,
        "primary_n_provinces": n_prov,
        "with_zeros_n_cities": n_with_zeros,
        "with_zeros_n_structural_zeros": n_zero_cities,
        "latin_n_cities": n_latin,
        "latin_n_provinces": int(latin["province"].nunique()),
        "primary_count_summary": {
            "min": int(primary["inscription_count"].min()),
            "median": float(primary["inscription_count"].median()),
            "mean": float(primary["inscription_count"].mean()),
            "max": int(primary["inscription_count"].max()),
        },
    }
    out_json = H.RUN_DIR / "outputs" / "sample-counts.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(counts, indent=2))
    print(f"[01-data-prep]   -> {out_json}")
    print("[01-data-prep] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
