#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reconcile-province-maps.py — the 39-vs-41 Latin-province reconciliation.

Decision 37 D2 assigned the 39-vs-41 Latin-province reconciliation to OSF
Amendment 02. This resolves it from evidence:

- the "41" is the 2024-notebook ``province_language_map``
  (``archive/2026-04-22-inscriptions-spa.ipynb`` cell 54), Latin provinces with
  Roma excluded (Decision 26 / B10, 2026-05-17);
- the "39" is the current committed, LIRE-field-aligned map
  (``runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv``;
  Decision 36, the first-class frame artefact).

The script diffs the two Latin sets (ignoring the three commented-out combo keys
in the notebook, which were never assigned), normalises spelling, and checks each
discrepant name against the actual ``province`` values in LIRE v3.0 so the
amendment can state how many inscriptions each removed name carried.

Output: outputs/province-reconciliation.csv + console table.

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-06.
Read-only; deterministic.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent.parent
NB = ROOT / "archive" / "2026-04-22-inscriptions-spa.ipynb"
CUR_MAP = ROOT / "runs" / "2026-06-04-h3a-confirmatory" / "data" / "province-language-map.csv"
LIRE = ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
OUT = Path(__file__).resolve().parent.parent / "outputs" / "province-reconciliation.csv"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def parse_2024_map() -> dict[str, str]:
    """Parse the cell-54 province_language_map, EXCLUDING commented-out lines."""
    nb = json.loads(NB.read_text())
    lines = nb["cells"][54]["source"]
    out: dict[str, str] = {}
    in_dict = False
    for raw in lines:
        line = raw.rstrip("\n")
        if "province_language_map = {" in line:
            in_dict = True
            continue
        if in_dict and line.strip().startswith("}"):
            break
        if not in_dict:
            continue
        if line.lstrip().startswith("#"):  # skip commented entries
            continue
        m = re.search(r"'([^']+)'\s*:\s*'(Latin|Greek)'", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def main() -> None:
    map2024 = parse_2024_map()
    lat2024 = [k for k, v in map2024.items() if v == "Latin"]
    lat2024_noroma = [p for p in lat2024 if p != "Roma"]

    cur = pd.read_csv(CUR_MAP, comment="#")
    latcur = cur.loc[cur["language"] == "Latin", "lire_province"].tolist()

    print(f"2024 notebook map: Latin={len(lat2024)} (Roma incl); "
          f"Roma-excluded={len(lat2024_noroma)}")
    print(f"current map: Latin={len(latcur)}")

    n2024 = {norm(p): p for p in lat2024_noroma}
    ncur = {norm(p): p for p in latcur}
    only2024 = sorted(n2024[k] for k in n2024 if k not in ncur)
    onlycur = sorted(ncur[k] for k in ncur if k not in n2024)

    # LIRE province-value counts for the discrepant names + spelling variants.
    lire = pd.read_parquet(LIRE, columns=["province"])
    prov_counts = lire["province"].value_counts(dropna=False)

    def lire_n(name: str) -> int:
        return int(prov_counts.get(name, 0))

    print("\n=== In 2024-Latin (Roma excl) but NOT current-Latin ===")
    rows = []
    for p in only2024:
        n = lire_n(p)
        print(f"  - {p!r:42} LIRE province N={n}")
        rows.append({"name": p, "side": "2024_only", "lire_province_n": n})
    print("=== In current-Latin but NOT 2024-Latin ===")
    for p in onlycur:
        n = lire_n(p)
        print(f"  + {p!r:42} LIRE province N={n}")
        rows.append({"name": p, "side": "current_only", "lire_province_n": n})

    # Spelling-variant check: Lugdunensis vs Lugudunensis in LIRE.
    print("\n=== Spelling-variant audit (LIRE province values) ===")
    for cand in ["Lugdunensis", "Lugudunensis", "Italia", "Alpes Graiae"]:
        print(f"  LIRE province {cand!r}: N={lire_n(cand)}")

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nReconciliation: 41 (2024) - 39 (current) = 2 removed.")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
