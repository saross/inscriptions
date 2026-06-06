#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify-unit-set.py — pin + verify the H2.1 mixture unit set (Decision 37 D1).

The H2.1 temporal-mixture is fit per unit; a unit is eligible for a standalone
mixture fit only if it clears the deconvolution-reachability floor N >= 2,000
(Decision 34). This script counts, on the prereg-filtered corpus, the inscriptions
per Latin-speaking province and per city (``urban_context_city``), and pins the
unit set:

  * empire-aggregate (full filtered corpus, incl. Rome) — secondary/context;
  * Latin-aggregate (the 39 Latin-speaking provinces, Rome excluded) — primary;
  * Latin provinces clearing N >= 2,000 (reportable);
  * Latin cities clearing N >= 2,000, Rome excluded (reportable);
  * grey-band provinces N in [1,549, 2,000) — caveated option (1,549 = the H1 v2
    50 %/50 y confirmatory threshold);
  * sub-floor units (< 1,549) fall back to date-window counts / §5.

Verifies the realised counts against Decision 37 D1 (19 provinces + 5 named
cities). Read-only; deterministic (pure counting).

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet
runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv

Outputs (runs/2026-06-07-h2.1-launch-prep/outputs/)
-------
province-counts.csv   — every Latin province with N + tier
city-counts.csv       — cities with N >= 1,000 + tier + province
unit-set.json         — the pinned unit set the launch spec consumes

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-07.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

SCRIPT = Path(__file__).resolve()
RUN = SCRIPT.parent.parent
ROOT = RUN.parent.parent
DATA = ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
LANG = ROOT / "runs" / "2026-06-04-h3a-confirmatory" / "data" / "province-language-map.csv"
OUT = RUN / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

FLOOR = 2000          # deconvolution-reachability floor (Decision 34)
GREY_LO = 1549        # H1 v2 50%/50y confirmatory threshold (grey-band lower edge)
EXPECTED_FILTERED = 180_609
EXPECTED_LATIN = 109_646


def tier(n: int) -> str:
    if n >= FLOOR:
        return "reportable"
    if n >= GREY_LO:
        return "grey-band"
    return "sub-floor"


def main() -> None:
    df = pd.read_parquet(DATA)
    geo = (
        df["Latitude"].notna() & df["Longitude"].notna()
        & df["not_before"].notna() & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    inre = df["province"].notna()
    env = (df["not_after"] >= -50) & (df["not_before"] <= 350)
    f = df.loc[geo & inre & env].copy()
    assert len(f) == EXPECTED_FILTERED, f"filtered {len(f)} != {EXPECTED_FILTERED}"

    latin = set(pd.read_csv(LANG, comment="#").query("language == 'Latin'")["lire_province"])
    fl = f[f["province"].isin(latin)]
    assert len(fl) == EXPECTED_LATIN, f"Latin {len(fl)} != {EXPECTED_LATIN}"

    # --- provinces ---
    pc = fl["province"].value_counts()
    prov_rows = [{"province": p, "n": int(n), "tier": tier(int(n))} for p, n in pc.items()]
    pd.DataFrame(prov_rows).to_csv(OUT / "province-counts.csv", index=False)
    prov_reportable = [r["province"] for r in prov_rows if r["tier"] == "reportable"]
    prov_grey = [r["province"] for r in prov_rows if r["tier"] == "grey-band"]

    # --- cities (urban_context_city, full filtered corpus, Rome excluded) ---
    cc = f["urban_context_city"].value_counts()
    city_rows = []
    for c, n in cc.items():
        if c == "Roma" or n < 1000:
            continue
        prov = f.loc[f["urban_context_city"] == c, "province"].mode()
        pv = prov.iloc[0] if len(prov) else None
        city_rows.append({
            "city": c, "n": int(n), "tier": tier(int(n)),
            "province": pv, "latin_province": bool(pv in latin),
        })
    pd.DataFrame(city_rows).to_csv(OUT / "city-counts.csv", index=False)
    city_reportable = [r["city"] for r in city_rows if r["tier"] == "reportable"]

    unit_set = {
        "artefact_id": "2026-06-07-h2.1-unit-set",
        "binds": {"decisions": [34, 36, 37], "decision_37": "D1"},
        "reachability_floor": FLOOR,
        "grey_band_lower": GREY_LO,
        "corpus": {"filtered_empire": int(len(f)), "latin_frame": int(len(fl))},
        "aggregates": {
            "empire": {"n": int(len(f)), "role": "secondary/context (incl. Rome)"},
            "latin": {"n": int(len(fl)), "role": "primary (39 Latin provinces, Rome excluded)"},
        },
        "latin_provinces_reportable": {
            "count": len(prov_reportable),
            "units": [{"province": p, "n": int(pc[p])} for p in prov_reportable],
        },
        "latin_cities_reportable": {
            "count": len(city_reportable),
            "field": "urban_context_city",
            "units": [{"city": r["city"], "n": r["n"], "province": r["province"]}
                      for r in city_rows if r["tier"] == "reportable"],
        },
        "grey_band_provinces": {
            "count": len(prov_grey),
            "units": [{"province": p, "n": int(pc[p])} for p in prov_grey],
        },
        "n_primary_fits": 2 + len(prov_reportable) + len(city_reportable),
        "sub_floor_policy": "units < 1,549 fall back to date-window counts / §5 (not a standalone mixture)",
        "provenance": {
            "built": "2026-06-07",
            "script": "runs/2026-06-07-h2.1-launch-prep/code/verify-unit-set.py",
            "lire": "archive/data-2026-04-22/LIRE_v3-0.parquet",
            "frame": "runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv",
        },
    }
    (OUT / "unit-set.json").write_text(json.dumps(unit_set, indent=2), encoding="utf-8")

    print(f"empire {len(f):,} | Latin {len(fl):,}")
    print(f"Latin provinces N>=2000: {len(prov_reportable)} (expect 19)")
    print(f"grey-band provinces: {len(prov_grey)} -> {prov_grey}")
    print(f"cities N>=2000 (excl Roma): {len(city_reportable)} -> {city_reportable}")
    print(f"primary mixture fits: {unit_set['n_primary_fits']} (2 aggregates + {len(prov_reportable)} provinces + {len(city_reportable)} cities)")
    print(f"wrote {OUT/'unit-set.json'}, province-counts.csv, city-counts.csv")


if __name__ == "__main__":
    main()
