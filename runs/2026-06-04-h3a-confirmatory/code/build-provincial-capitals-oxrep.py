#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-provincial-capitals-oxrep.py
==================================

Build the **authoritative** provincial-capital indicator for H3c(i) from the
Hanson 2016 OXREP Cities Database (the same dataset Hanson 2021 — our H3c
replication target — used). This SUPERSEDES the book/Barrington AD-117 fallback
(``build_provincial_capitals.py`` → ``provincial-capitals-ad117.csv``), which is
retained as a sensitivity.

Method
------
1. From the OXREP **Civic Status** table, take every Primary Key whose civic
   status is ``Provincial capital`` (or the single ``Provincial capital?``) —
   67 cities (66 + 1 queried). This is "ever a provincial capital" across the
   dataset's 100 BC – AD 300 horizon (the book's "40 in AD 117", Fig. 120, is a
   single-year snapshot; that AD-117 set is the sensitivity).
2. Join to the OXREP **Cities** table for the Ancient Toponym + Province.
3. Match to our city frames by **exact full Ancient-Toponym string** — our city
   names (and OXREP's) embed the province disambiguator (e.g. ``Nicopolis
   (Achaea)``), so an exact-string match is collision-safe (it cannot flag a
   non-capital that merely shares a bare toponym with a capital in another
   province — the safeguard flagged by the H3c(i) agent). A first-4-char
   province cross-check is logged for transparency (apparent mismatches are
   benign dataset spelling differences, e.g. OXREP ``Silicia`` vs our
   ``Sicilia``, ``Gallia Lugdunensis`` vs ``Lugudunensis``).

Output
------
``data/processed/provincial-capitals.csv`` — one row per OXREP provincial
capital present in our empire frame (the superset of the Latin frame), columns:
``city, oxrep_primary_key, oxrep_province, our_province, is_provincial_capital,
source``. The H3c(i) contrast script reads the ``city`` column as the capital
set and aligns it to each frame.

Encoding note: the OXREP CSVs are Latin-1.

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-05, on Shawn's brief (OXREP is the
authoritative source; book/Barrington is the fallback).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "data"
PROCESSED = DATA / "processed"
CITIES_CSV = DATA / "hanson2016_cities_oxrep.csv"
CIVIC_CSV = DATA / "hanson2016_civic-status_oxrep.csv"
EMPIRE_PARQUET = PROCESSED / "city_level_for_h3a.parquet"          # superset frame
OUT_CSV = PROCESSED / "provincial-capitals.csv"

PROVCAP_STATUSES = {"Provincial capital", "Provincial capital?"}


def main() -> int:
    cities = pd.read_csv(CITIES_CSV, encoding="latin-1")
    civic = pd.read_csv(CIVIC_CSV, encoding="latin-1")

    keys = set(civic.loc[civic["Civic Status"].isin(PROVCAP_STATUSES), "Primary Key"])
    ox_caps = cities[cities["Primary Key"].isin(keys)][
        ["Primary Key", "Ancient Toponym", "Province"]
    ].copy()
    print(f"[build-oxrep] OXREP provincial-capital cities (incl '?'): {len(ox_caps)}")

    emp = pd.read_parquet(EMPIRE_PARQUET)[["city", "province"]]
    our_cities = set(emp["city"].astype(str))

    # Exact full-toponym match (collision-safe; disambiguators embedded).
    ox_caps["in_frame"] = ox_caps["Ancient Toponym"].astype(str).isin(our_cities)
    matched = ox_caps[ox_caps["in_frame"]].copy()
    absent = ox_caps[~ox_caps["in_frame"]]
    print(f"[build-oxrep] matched to empire frame (exact toponym): "
          f"{len(matched)}/{len(ox_caps)}")
    print(f"[build-oxrep] OXREP capitals absent from our frame "
          f"({len(absent)}): {sorted(absent['Ancient Toponym'])}")

    # Attach our province (for the transparency cross-check) and write.
    out = matched.merge(emp, left_on="Ancient Toponym", right_on="city", how="left")
    out = out.rename(columns={
        "Primary Key": "oxrep_primary_key",
        "Province": "oxrep_province",
        "province": "our_province",
    })
    out["is_provincial_capital"] = 1
    out["source"] = (
        "Hanson 2016 OXREP Cities Database, Civic Status = 'Provincial capital' "
        "(incl. one 'Provincial capital?'); the dataset Hanson 2021 used. "
        "Matched to our cities by exact Ancient-Toponym string (collision-safe). "
        "Downloaded 2026-06-05 from oxrep.web.ox.ac.uk/cities-database."
    )
    out = out[["city", "oxrep_primary_key", "oxrep_province", "our_province",
               "is_provincial_capital", "source"]].sort_values("city")
    out.to_csv(OUT_CSV, index=False)
    print(f"[build-oxrep] wrote {len(out)} capital rows -> {OUT_CSV}")

    # Benign province-spelling cross-check (transparency only).
    mism = out[out["our_province"].astype(str).str[:4].str.lower()
               != out["oxrep_province"].astype(str).str[:4].str.lower()]
    print(f"[build-oxrep] province-name spelling differences (benign): {len(mism)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
