#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
s5-target-set-profile.py
========================

Profile the §5 small-N city-trajectory target set, to ground the
implementation spec for the Layer-A Bayesian hierarchical trajectory model.

The §5 small-N analysis targets Hanson-matched cities BELOW the Phase-1
confirmatory detection threshold but above the small-N estimation floor
(N >= 50; cf. Crema 2025). This script reports, with Rome excluded:

- how many Hanson-matched cities have a usable inscription count (>= 50),
  split by the confirmatory threshold (1,549, urban-area 50%/50y cpl-3-gauss);
- the N distribution across the target set (percentiles);
- the province structure (how many provinces, cities per province) — this
  determines the partial-pooling hierarchy;
- the temporal span of dated inscriptions.

These numbers decide: monolithic-vs-province-batched model; bin width; the
shape of the city/province pooling hierarchy.

Run (on sapphire, via the grid venv; reads from stdin):
    ssh sapphire '/home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/python' \
        < scripts/s5-target-set-profile.py

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
CITY_COL = "urban_context_city"
POP_COL = "urban_context_pop_est"
PROV_COL = "province"  # also report province_label_clean if present
THRESHOLD = 1549       # urban-area 50%/50y cpl-3-gauss (prereg §6 line 408)
N_FLOOR = 50           # small-N estimation floor (Crema 2025)


def main() -> int:
    if not PARQUET.exists():
        print(f"FATAL: parquet not found at {PARQUET}", file=sys.stderr)
        return 2
    cols = [CITY_COL, POP_COL, PROV_COL, "not_before", "not_after",
            "province_label_clean"]
    df = pd.read_parquet(PARQUET, columns=[c for c in cols if c])
    print(f"Loaded {PARQUET.name}: {len(df)} rows\n")

    # Hanson-matched = has an urban-area city label AND a population estimate.
    matched = df[df[CITY_COL].notna() & df[POP_COL].notna()].copy()
    # Rome-exclusion.
    matched = matched[~matched[CITY_COL].str.lower().str.contains("rom", na=False)]
    print(f"Hanson-matched, Rome-excluded inscriptions: {len(matched)}")

    per_city = (
        matched.groupby(CITY_COL)
        .agg(n=("not_before", "size"),
             pop=(POP_COL, "first"),
             province=(PROV_COL, "first"))
        .reset_index()
    )
    n_cities_total = len(per_city)
    print(f"Hanson-matched, Rome-excluded cities (any N): {n_cities_total}\n")

    # Target-set bucketing.
    below_floor = per_city[per_city["n"] < N_FLOOR]
    target = per_city[(per_city["n"] >= N_FLOOR) & (per_city["n"] < THRESHOLD)]
    above_thr = per_city[per_city["n"] >= THRESHOLD]
    print("=" * 60)
    print("TARGET-SET BUCKETING (inscription count)")
    print("=" * 60)
    print(f"  N <  {N_FLOOR}              : {len(below_floor):>4} cities "
          f"(below estimation floor; excluded)")
    print(f"  {N_FLOOR} <= N < {THRESHOLD}   : {len(target):>4} cities "
          f"(<<< §5 SMALL-N TARGET SET)")
    print(f"  N >= {THRESHOLD}           : {len(above_thr):>4} cities "
          f"(confirmatory-eligible; H3b)")

    if len(target):
        q = np.percentile(target["n"], [10, 25, 50, 75, 90, 99])
        print(f"\n  target-set N distribution:")
        print(f"    min={target['n'].min()}  "
              f"p10={q[0]:.0f} p25={q[1]:.0f} median={q[2]:.0f} "
              f"p75={q[3]:.0f} p90={q[4]:.0f} p99={q[5]:.0f}  "
              f"max={target['n'].max()}")
        print(f"    cities with N in [50,100)  : "
              f"{int(((target['n']>=50)&(target['n']<100)).sum())}")
        print(f"    cities with N in [100,300) : "
              f"{int(((target['n']>=100)&(target['n']<300)).sum())}")
        print(f"    cities with N in [300,1549): "
              f"{int((target['n']>=300).sum())}")

    # Province structure (partial-pooling hierarchy).
    print("\n" + "=" * 60)
    print("PROVINCE STRUCTURE (partial-pooling hierarchy)")
    print("=" * 60)
    for pcol in (PROV_COL, "province_label_clean"):
        if pcol not in per_city.columns and pcol not in matched.columns:
            continue
        src = target if pcol == PROV_COL else None
        if src is None:
            # province_label_clean from matched, joined to target cities
            plc = (matched.groupby(CITY_COL)["province_label_clean"]
                   .first())
            tgt = target.set_index(CITY_COL)
            tgt = tgt.join(plc.rename("plc"))
            grp = tgt.groupby("plc")["n"].count()
            label = "province_label_clean"
        else:
            grp = src.groupby("province")["n"].count()
            label = PROV_COL
        grp = grp.sort_values(ascending=False)
        print(f"\n  by '{label}': {len(grp)} provinces with target cities")
        print(f"    cities/province: median={grp.median():.0f}  "
              f"max={grp.max()} ({grp.idxmax()})  "
              f"singletons={int((grp==1).sum())}")
        print(f"    top 8: " + ", ".join(f"{p}={c}" for p, c in grp.head(8).items()))

    # Temporal span.
    print("\n" + "=" * 60)
    print("TEMPORAL SPAN (dated inscriptions in target set)")
    print("=" * 60)
    tgt_ins = matched[matched[CITY_COL].isin(target[CITY_COL])]
    nb = tgt_ins["not_before"].to_numpy()
    na = tgt_ins["not_after"].to_numpy()
    print(f"  not_before: min={np.nanmin(nb):.0f} max={np.nanmax(nb):.0f}")
    print(f"  not_after : min={np.nanmin(na):.0f} max={np.nanmax(na):.0f}")
    widths = (na - nb)
    wq = np.nanpercentile(widths, [50, 75, 90, 99])
    print(f"  interval width (na-nb): median={wq[0]:.0f} p75={wq[1]:.0f} "
          f"p90={wq[2]:.0f} p99={wq[3]:.0f}  (informs bin width / aoristic)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
