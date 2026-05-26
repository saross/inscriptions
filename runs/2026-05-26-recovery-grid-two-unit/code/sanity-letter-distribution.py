#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sanity-letter-distribution.py
=============================

Pre-launch sanity gate 3 (spec §7): re-confirm the empirical
letter-count distribution matches the descriptive recorded by the
2026-05-26 letter-count probe (median ~ 25, mean ~ 45, max ~ 35K).
Failure indicates the parquet on this host differs from the probe's
parquet — most likely a stale rsync.

Tolerances: median +/- 2 letters, mean +/- 5 letters, max +/- 200
letters (the probe's max is 35,537 — tight but allows for small
sampling-driven drift if the parquet is regenerated).

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# Expected descriptives (from 2026-05-26 letter-count probe).
EXPECTED = {
    "n_rows": 180_609,
    "median": 25.0,
    "mean": 45.4,
    "max": 35_537,
    "pct_zero": 2.215,
}
TOLERANCES = {
    "median": 2.0,
    "mean": 5.0,
    "max": 200,
    "pct_zero": 0.5,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Letter-count distribution sanity check."
    )
    parser.add_argument("--letter-parquet", required=True, type=Path)
    parser.add_argument(
        "--run-root", required=True, type=Path,
        help="Parent two-unit run dir (output written under comparison/).",
    )
    args = parser.parse_args()

    df = pd.read_parquet(
        args.letter_parquet, columns=["letter_count_conservative"]
    )
    n_rows = int(df.shape[0])
    arr = df["letter_count_conservative"].to_numpy()
    median = float(np.median(arr))
    mean = float(np.mean(arr))
    mx = int(np.max(arr))
    pct_zero = float((arr == 0).mean() * 100)

    diag = {
        "letter_parquet": str(args.letter_parquet),
        "actual": {
            "n_rows": n_rows,
            "median": median,
            "mean": mean,
            "max": mx,
            "pct_zero": pct_zero,
        },
        "expected": EXPECTED,
        "tolerances": TOLERANCES,
    }

    fails = []
    if n_rows != EXPECTED["n_rows"]:
        fails.append(f"n_rows={n_rows} expected={EXPECTED['n_rows']}")
    if abs(median - EXPECTED["median"]) > TOLERANCES["median"]:
        fails.append(f"median={median} expected~{EXPECTED['median']}")
    if abs(mean - EXPECTED["mean"]) > TOLERANCES["mean"]:
        fails.append(f"mean={mean:.2f} expected~{EXPECTED['mean']}")
    if abs(mx - EXPECTED["max"]) > TOLERANCES["max"]:
        fails.append(f"max={mx} expected~{EXPECTED['max']}")
    if abs(pct_zero - EXPECTED["pct_zero"]) > TOLERANCES["pct_zero"]:
        fails.append(f"pct_zero={pct_zero:.3f} expected~{EXPECTED['pct_zero']}")

    diag["pass"] = bool(not fails)
    diag["fails"] = fails

    out_path = (
        args.run_root / "comparison" / "sanity-letter-distribution.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(diag, fh, indent=2)

    print(
        f"[sanity-letter-dist] n_rows={n_rows:,}  median={median:.1f}  "
        f"mean={mean:.2f}  max={mx:,}  pct_zero={pct_zero:.3f}%"
    )
    print(
        f"[sanity-letter-dist] verdict="
        f"{'PASS' if diag['pass'] else 'FAIL: ' + ', '.join(fails)}"
    )
    print(f"[sanity-letter-dist] wrote {out_path}")
    return 0 if diag["pass"] else 4


if __name__ == "__main__":
    sys.exit(main())
