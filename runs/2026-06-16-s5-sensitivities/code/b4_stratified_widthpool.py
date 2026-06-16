#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
b4_stratified_widthpool.py — §5 B4 stratified-sampling sensitivity, v2-faithful.
================================================================================

The preregistered B4 ("recompute Phase-1 bootstrap thresholds under stratified —
province/city-proportional — draws; report deltas to bootstrap primary") was written
against the v1 design that bootstrapped inscriptions from real LIRE. **Decision 8
replaced that bootstrap with synthetic data drawn from a parametric ground-truth
null** (`h1_sim_v2.py`); the only empirical input to the v2 thresholds is the
**interval-width pool** (`widths_pool`, used by `_simulate_intervals_{exp,cpl}`). The
per-iteration `province_counts`/`city_counts` are vestigial metadata and do not affect
detection. So:

  - Scheme (a) proportional-allocation stratified sampling PRESERVES the width
    distribution → threshold-neutral by construction (it only removes resample
    variance, which the synthetic v2 design does not carry).
  - Scheme (b) reweight-to-balance (equalise province / city contributions) CHANGES
    the width mix → can move thresholds, but ONLY if interval widths differ across
    provinces / cities.

This script runs the cheap, decisive check (diagnostic-first): does the
province/city-BALANCED width distribution differ from the global pool that the
committed v2 thresholds used? If the divergence is small, the thresholds are robust
to stratification without any grid re-run; if large, a targeted re-run of the
threshold cells under the balanced width pool is warranted (flagged, not run here).

Outputs (`runs/2026-06-16-s5-sensitivities/outputs/`):
  b4-widthpool-diagnostic.json, REPORT-b4.md.
Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-16.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-04-25-h1-simulation/code"))
import primitives as P   # noqa: E402  (the exact loader the v2 sim used)

DATA = "archive/data-2026-04-22/LIRE_v3-0.parquet"
OUT_DIR = ROOT / "runs/2026-06-16-s5-sensitivities/outputs"
QUANTILES = [10, 25, 50, 75, 90]


def balanced_weights(strata: np.ndarray) -> np.ndarray:
    """Scheme (b): equal total weight per stratum, spread within. Over-represented
    strata (Rome/Ostia; heavily-sampled provinces) are down-weighted."""
    s = pd.Series(strata.astype(str))
    counts = s.map(s.value_counts())
    valid = (s.values != "nan") & (s.values != "") & (s.values != "None")
    w = np.where(valid, 1.0 / counts.to_numpy(), 0.0)
    return w / w.sum()


def wq(values: np.ndarray, weights: np.ndarray, qs) -> list[float]:
    """Weighted quantiles."""
    order = np.argsort(values)
    v, w = values[order], weights[order]
    cw = np.cumsum(w) - 0.5 * w
    cw /= w.sum()
    return [float(np.interp(q / 100.0, cw, v)) for q in qs]


def describe(values, weights, label):
    mean = float(np.average(values, weights=weights))
    quants = wq(values, weights, QUANTILES)
    return {"label": label, "mean_width": round(mean, 2),
            "quantiles": {str(q): round(x, 1) for q, x in zip(QUANTILES, quants)}}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = P.load_filtered_lire(DATA)
    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)
    widths = (na - nb).astype(float)
    keep = widths > 0.0
    widths = widths[keep]
    prov = df["province"].to_numpy()[keep]
    city = df["urban_context_city"].to_numpy()[keep]
    n = len(widths)
    glob_w = np.full(n, 1.0 / n)

    prov_w = balanced_weights(prov)
    city_w = balanced_weights(city)

    pools = {
        "global": describe(widths, glob_w, "global (v2 committed pool)"),
        "province_balanced_b": describe(widths, prov_w, "province-balanced (scheme b)"),
        "city_balanced_b": describe(widths, city_w, "city-balanced (scheme b)"),
    }
    # Distributional divergence (Wasserstein-1, years) of each balanced pool vs global.
    w1_prov = float(wasserstein_distance(widths, widths, glob_w, prov_w))
    w1_city = float(wasserstein_distance(widths, widths, glob_w, city_w))
    med_glob = pools["global"]["quantiles"]["50"]
    out = {
        "n_inscriptions": int(n),
        "n_provinces": int(pd.Series(prov.astype(str)).nunique()),
        "n_cities": int(pd.Series(city.astype(str)).replace({"nan": np.nan}).nunique()),
        "pools": pools,
        "wasserstein1_vs_global": {"province_balanced": round(w1_prov, 2),
                                   "city_balanced": round(w1_city, 2)},
        "median_width_shift_pct": {
            "province_balanced": round(100 * (pools["province_balanced_b"]["quantiles"]["50"] - med_glob) / med_glob, 1),
            "city_balanced": round(100 * (pools["city_balanced_b"]["quantiles"]["50"] - med_glob) / med_glob, 1)},
        "scheme_a_note": "proportional-allocation preserves the width distribution exactly "
                         "→ threshold-neutral by construction in the synthetic v2 design",
    }
    # Verdict: 'small' if both balanced pools' W1 < 10% of the global median width.
    tol = 0.10 * med_glob
    out["robust_no_rerun"] = bool(w1_prov < tol and w1_city < tol)
    out["wasserstein_tolerance_10pct_median"] = round(tol, 2)

    (OUT_DIR / "b4-widthpool-diagnostic.json").write_text(json.dumps(out, indent=1))
    _write_report(out)
    print(json.dumps(out, indent=1))
    print(f"\nwrote → {OUT_DIR}")


def _write_report(o: dict) -> None:
    p = o["pools"]
    verdict = ("ROBUST — no grid re-run needed" if o["robust_no_rerun"]
               else "MATERIAL — a targeted threshold re-run under the balanced width pool is warranted")
    md = f"""# §5 B4 — stratified-sampling sensitivity (v2-faithful) — DRAFT

> **Key finding first:** the preregistered B4 (stratified *bootstrap* of LIRE) is
> **architecturally moot for the committed v2 Phase-1 thresholds** — Decision 8 replaced
> the LIRE bootstrap with synthetic data from a parametric null (`h1_sim_v2.py`). The only
> empirical lever on the thresholds is the **interval-width pool**; the per-iteration
> province/city counts are vestigial metadata with no effect on detection. This is a
> prereg-obligation-vs-implementation discrepancy worth recording in the obligations audit.

## What B4 means for v2, and the result

- **Scheme (a) proportional-allocation** preserves the width distribution exactly →
  **threshold-neutral by construction** (it removes resample variance, which the
  synthetic v2 design has none of). No computation needed.
- **Scheme (b) reweight-to-balance** (equalise province / city contributions; down-weights
  the over-represented Rome/Ostia and heavily-sampled provinces) changes the width mix —
  but only matters if interval widths differ across strata. The cheap check:

| width pool | mean (y) | p10 | p25 | p50 | p75 | p90 |
|---|---|---|---|---|---|---|
| global (v2 committed) | {p['global']['mean_width']} | {p['global']['quantiles']['10']} | {p['global']['quantiles']['25']} | {p['global']['quantiles']['50']} | {p['global']['quantiles']['75']} | {p['global']['quantiles']['90']} |
| province-balanced (b) | {p['province_balanced_b']['mean_width']} | {p['province_balanced_b']['quantiles']['10']} | {p['province_balanced_b']['quantiles']['25']} | {p['province_balanced_b']['quantiles']['50']} | {p['province_balanced_b']['quantiles']['75']} | {p['province_balanced_b']['quantiles']['90']} |
| city-balanced (b) | {p['city_balanced_b']['mean_width']} | {p['city_balanced_b']['quantiles']['10']} | {p['city_balanced_b']['quantiles']['25']} | {p['city_balanced_b']['quantiles']['50']} | {p['city_balanced_b']['quantiles']['75']} | {p['city_balanced_b']['quantiles']['90']} |

Wasserstein-1 distance from the global pool: province-balanced **{o['wasserstein1_vs_global']['province_balanced']} y**,
city-balanced **{o['wasserstein1_vs_global']['city_balanced']} y** (tolerance = 10% of the global
median width = {o['wasserstein_tolerance_10pct_median']} y). Median-width shift:
province {o['median_width_shift_pct']['province_balanced']:+}%, city {o['median_width_shift_pct']['city_balanced']:+}%.

## Verdict — {verdict}

{'The balanced width distributions are close to the global pool, so the synthetic-data interval generation — and hence the detection thresholds — would be essentially unchanged under either stratification scheme. **B4 is satisfied: the Phase-1 thresholds are robust to province/city stratification.** No grid re-run is warranted.' if o['robust_no_rerun'] else 'The balanced width distribution diverges materially from the global pool, so the thresholds could shift. A targeted re-run of the threshold-setting cells (province + urban-area N-sweeps, binding brackets) under the balanced width pool is warranted — flagged, not run here.'}

## Resolution for the obligations audit (item B4)

Record B4 as **superseded by Decision 8** (no LIRE bootstrap in the committed v2 design),
with this width-pool composition check as the v2-faithful substitute. {'Result: robust.' if o['robust_no_rerun'] else 'Result: a width-pool re-run is the next step.'}

## Reproduce
```bash
uv run python runs/2026-06-16-s5-sensitivities/code/b4_stratified_widthpool.py
```
"""
    (OUT_DIR / "REPORT-b4.md").write_text(md)


if __name__ == "__main__":
    main()
