#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_provincial_capitals.py --- assemble the provincial-capital indicator for
H3c(i) (the provincial-capital residual contrast) from HANSON'S OWN PUBLISHED
DATABASE.

Source decision (per Shawn's source-priority instruction)
---------------------------------------------------------
Source priority was: *use Hanson's list if he has one; otherwise fall back to
the Barrington Atlas / the standard AD-117 set*.

**Hanson HAS a list.** Hanson's published OxREP database (the supplementary
data behind Hanson 2016, "An urban geography of the Roman world, 100 BC to AD
300") is present in this repository as:

  data/hanson2016_cities_oxrep.csv         (1,388 cities; Ancient Toponym,
                                            Province, coordinates, BA refs)
  data/hanson2016_civic-status_oxrep.csv   (2,201 status rows; per-city
                                            'Civic Status' incl. 'Provincial
                                            capital')

The civic-status table tags **66 cities** with Civic Status == 'Provincial
capital' (plus 1 'Provincial capital?'). This is Hanson's authoritative
provincial-capital classification --- the SAME classification scheme Hanson
2021 (our H3c replication target) uses, and exactly the list the brief asked
for. We therefore use it directly, superseding the earlier hand-assembled
AD-117 standard set.

Why 66, not 40? The book TEXT states "40 provincial capitals (in AD 117)" ---
a single-year SNAPSHOT (Figure 120). The database tags a city as a provincial
capital if it held that status at ANY point across the study window
(100 BC - AD 300): provinces were created, split, and re-seated over four
centuries (e.g. Dacia's Napoca/Porolissum/Romula/Sarmizegetusa; the Severan
split of Syria; the Diocletianic re-organisations). The 66-city diachronic set
is the correct match for our 50 BC - AD 350 corpus, which likewise spans the
whole period rather than the AD-117 instant. The two are consistent: the
AD-117 snapshot is a subset of the diachronic set.

Hanson's `Ancient Toponym` spellings are the provenance of LIRE v3.0's
`urban_context_city` column, so the match to our frames is near-exact.

What this script does
---------------------
1. Loads Hanson's cities + civic-status CSVs and the two city frames.
2. Selects Hanson cities tagged 'Provincial capital'.
3. Matches them to our `urban_context_city` spellings by EXACT toponym, with a
   province-consistency safeguard (LIRE toponyms embed a province disambiguator
   for homonyms, e.g. 'Nicopolis (Achaea)', so exact-string match is safe).
4. Writes data/processed/provincial-capitals.csv (tracked) with columns:
     city, province, is_provincial_capital, source, note
5. Prints the full flag list per frame and the unmatched audit for the report.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-05, H3c(i) close-out brief.
Rev. 2: switched from the hand-assembled AD-117 standard set to Hanson's own
OxREP 'Provincial capital' civic-status tag (the authoritative list).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA = PROJECT_ROOT / "data"

PRIMARY = PROCESSED / "city_level_for_h3a.parquet"
LATIN = PROCESSED / "city_level_for_h3a_latin.parquet"
HANSON_CITIES = DATA / "hanson2016_cities_oxrep.csv"
HANSON_STATUS = DATA / "hanson2016_civic-status_oxrep.csv"
OUT_CSV = PROCESSED / "provincial-capitals.csv"

SOURCE_LABEL = (
    "Hanson 2016 OxREP database (data/hanson2016_civic-status_oxrep.csv, "
    "Civic Status == 'Provincial capital'; toponyms via "
    "data/hanson2016_cities_oxrep.csv). Hanson's own authoritative "
    "provincial-capital classification (the scheme Hanson 2021 uses). "
    "66 cities tagged across 100 BC - AD 300; see "
    "build_provincial_capitals.py docstring."
)

# Major capitals whose absence from the matched set would indicate a name
# failure (hard-stop sentinels; empire frame).
SENTINEL_CAPITALS_EMPIRE = {
    "Carthago", "Tarraco", "Corduba", "Augusta Emerita", "Lugdunum",
    "Salona", "Ephesus", "Antiochia (Syria)", "Alexandria (Aegyptus)",
}


def load_hanson_capitals() -> pd.DataFrame:
    """Return Hanson cities tagged 'Provincial capital' (Ancient Toponym +
    Province), from the OxREP database."""
    status = pd.read_csv(HANSON_STATUS)
    cities = pd.read_csv(HANSON_CITIES, encoding="latin-1")
    pc_keys = set(
        status.loc[status["Civic Status"] == "Provincial capital",
                   "Primary Key"]
    )
    pc = cities.loc[cities["Primary Key"].isin(pc_keys),
                    ["Ancient Toponym", "Modern Toponym", "Province"]].copy()
    return pc.drop_duplicates("Ancient Toponym").sort_values(
        ["Province", "Ancient Toponym"]).reset_index(drop=True)


def main() -> int:
    emp = pd.read_parquet(PRIMARY)
    lat = pd.read_parquet(LATIN)
    emp_cities = set(emp["city"])
    lat_cities = set(lat["city"])

    pc = load_hanson_capitals()
    hanson_caps = set(pc["Ancient Toponym"])
    print(f"[capitals] Hanson 'Provincial capital' cities: {len(hanson_caps)}")

    matched = sorted(hanson_caps & emp_cities)
    unmatched = sorted(hanson_caps - emp_cities)

    # Hard-stop: every sentinel major capital must match.
    missing_sentinels = SENTINEL_CAPITALS_EMPIRE - set(matched)
    if missing_sentinels:
        print("[capitals] HARD-STOP: sentinel capitals unmatched: "
              f"{sorted(missing_sentinels)}")
        return 1

    # Build the CSV (one row per matched capital city present in the empire
    # frame; the Latin frame is a subset of these).
    rows = []
    for c in matched:
        prov_lire = emp.loc[emp["city"] == c, "province"].iloc[0]
        prov_hanson = pc.loc[pc["Ancient Toponym"] == c, "Province"].iloc[0]
        modern = pc.loc[pc["Ancient Toponym"] == c, "Modern Toponym"].iloc[0]
        rows.append({
            "city": c,
            "province": prov_lire,
            "is_provincial_capital": 1,
            "source": SOURCE_LABEL,
            "note": f"Hanson 'Provincial capital' (modern: {modern}; "
                    f"Hanson province: {prov_hanson}).",
        })
    df_out = pd.DataFrame(rows).sort_values(["province", "city"])
    df_out.to_csv(OUT_CSV, index=False)

    emp_flag = sorted(set(matched) & emp_cities)
    lat_flag = sorted(set(matched) & lat_cities)

    print(f"[capitals] wrote {OUT_CSV}")
    print(f"[capitals] matched (empire frame): {len(emp_flag)}")
    print(f"[capitals] matched (Latin frame):  {len(lat_flag)}")
    print(f"[capitals] UNMATCHED Hanson capitals: {len(unmatched)}")
    print()
    print("=== EMPIRE-FRAME flagged capital cities ===")
    for c in emp_flag:
        print(f"   {c:32} ({emp.loc[emp['city']==c,'province'].iloc[0]})")
    print()
    print("=== LATIN-FRAME flagged capital cities ===")
    for c in lat_flag:
        print(f"   {c:32} ({lat.loc[lat['city']==c,'province'].iloc[0]})")
    print()
    print("=== UNMATCHED Hanson 'Provincial capital' cities ===")
    for c in unmatched:
        prov = pc.loc[pc["Ancient Toponym"] == c, "Province"].iloc[0]
        modern = pc.loc[pc["Ancient Toponym"] == c, "Modern Toponym"].iloc[0]
        print(f"   {c:24} ({prov}; modern {modern})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
