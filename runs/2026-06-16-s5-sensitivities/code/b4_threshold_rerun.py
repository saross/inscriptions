#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
b4_threshold_rerun.py — §5 B4 scheme-(b): do balanced width pools move the thresholds?
======================================================================================

The width-pool diagnostic (`b4_stratified_widthpool.py`) showed the v2-faithful B4 lever
is the interval-width pool, and that reweighting to a province/city-BALANCED corpus shifts
it materially (city-balanced median width 99y → 79y). This script quantifies the
downstream effect: it re-runs the threshold-setting Phase-1 cells under three width pools
— **global** (the committed pool), **province-balanced**, **city-balanced** — all at the
SAME reduced precision, so the precision cancels in the balanced-vs-global **delta** (the
deliverable; absolute thresholds here are not the committed full-precision ones).

Reuse-only: `h1_sim_v2.run_cell` (passed a custom `widths_pool`), `power_curves`. Cells:
levels {province, urban-area} × brackets {a_50pc_50y, b_double_25y, c_20pc_25y} × 2 shapes
× 2 nulls × the level N-sweeps. Primary reporting null per cell: CPL k=3 / exponential.

Outputs (`runs/2026-06-16-s5-sensitivities/outputs/`):
  b4-threshold-rerun.json, b4-thresholds-table.csv, REPORT-b4-rerun.md.
Sapphire (CPU). Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-16.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-04-25-h1-simulation/code"))
import primitives as P        # noqa: E402
import h1_sim_v2 as H1        # noqa: E402
import power_curves as PC     # noqa: E402

DATA = "archive/data-2026-04-22/LIRE_v3-0.parquet"
OUT_DIR = ROOT / "runs/2026-06-16-s5-sensitivities/outputs"
N_ITER, N_MC, N_JOBS, SEED = 200, 300, 12, 20_260_616
TARGET = 0.80
LEVELS = {"province", "urban-area"}
BRACKETS = {"a_50pc_50y", "b_double_25y", "c_20pc_25y"}
KEY = ["level", "bracket", "shape", "null_model"]


def balanced_weights(strata: np.ndarray) -> np.ndarray:
    s = pd.Series(strata.astype(str))
    counts = s.map(s.value_counts())
    valid = (s.values != "nan") & (s.values != "") & (s.values != "None")
    w = np.where(valid, 1.0 / counts.to_numpy(), 0.0)
    return w / w.sum()


def build_pools(widths, prov, city, seed) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    pw, cw = balanced_weights(prov), balanced_weights(city)
    n = len(widths)
    return {
        "global": widths,
        "province_balanced": rng.choice(widths, size=n, replace=True, p=pw),
        "city_balanced": rng.choice(widths, size=n, replace=True, p=cw),
    }


def threshold_cells() -> list[H1.CellSpec]:
    return [H1.CellSpec(cell_id=c.cell_id, level=c.level, bracket=c.bracket,
                        shape=c.shape, n=c.n, null_model=c.null_model,
                        n_iterations=N_ITER, n_mc=N_MC)
            for c in H1.enumerate_cells()
            if c.level in LEVELS and c.bracket in BRACKETS]


def run_pool(name, widths_pool, cells, master_seed) -> pd.DataFrame:
    """Run all threshold cells under one width pool; return primary-null thresholds."""
    dummy_prov = np.array(["NA"] * 10)          # vestigial metadata pools (unused)
    dummy_city = np.array(["NA"] * 10)
    cell_seeds = np.random.SeedSequence(master_seed).spawn(len(cells))
    t0 = time.time()
    with Parallel(n_jobs=N_JOBS, backend="loky", verbose=0) as pool:
        results = pool(
            delayed(H1.run_cell)(spec, widths_pool, dummy_prov, dummy_city,
                                 P.BIN_EDGES, P.BIN_CENTRES, cs)
            for spec, cs in zip(cells, cell_seeds))
    flat = [r for rc in results for r in rc]
    curves = PC.build_power_curves(pd.DataFrame(flat))
    thr = PC.extract_thresholds(curves, targets=(TARGET,))
    primary = thr[((thr.null_model == "cpl") & (thr.cpl_k == 3))
                  | ((thr.null_model == "exponential") & (thr.cpl_k == -1))].copy()
    primary["pool"] = name
    print(f"  [{name}] {len(cells)} cells in {time.time()-t0:.0f}s; "
          f"{primary['min_n'].notna().sum()}/{len(primary)} reachable", flush=True)
    return primary[KEY + ["pool", "min_n", "obs_min_n"]]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = P.load_filtered_lire(DATA)
    widths = (df["not_before"].to_numpy(float) * -1 + df["not_after"].to_numpy(float))
    keep = widths > 0
    widths = widths[keep]
    pools = build_pools(widths, df["province"].to_numpy()[keep],
                        df["urban_context_city"].to_numpy()[keep], SEED)
    cells = threshold_cells()
    print(f"loaded {len(widths)} widths; {len(cells)} threshold cells × {len(pools)} pools; "
          f"n_iter={N_ITER} n_mc={N_MC}", flush=True)

    tables = []
    for name, pool in pools.items():
        tab = run_pool(name, pool, cells, SEED)
        tab.to_json(OUT_DIR / f"b4-thr-{name}.json", orient="records", indent=1)  # partial
        tables.append(tab)

    wide = tables[0][KEY].drop_duplicates()
    for name in pools:
        sub = pd.concat(tables)
        sub = sub[sub["pool"] == name][KEY + ["min_n"]].rename(columns={"min_n": name})
        wide = wide.merge(sub, on=KEY, how="left")
    for bal in ("province_balanced", "city_balanced"):
        wide[f"delta_{bal}"] = wide[bal] - wide["global"]      # <0 = lower threshold

    wide.to_csv(OUT_DIR / "b4-thresholds-table.csv", index=False)
    summary = _summarise(wide)
    (OUT_DIR / "b4-threshold-rerun.json").write_text(
        json.dumps({"sampling": {"n_iter": N_ITER, "n_mc": N_MC, "target": TARGET,
                                 "seed": SEED, "note": "balanced-vs-global delta is the "
                                 "deliverable; absolute min_n at reduced precision"},
                    "summary": summary,
                    "rows": wide.replace({np.nan: None}).to_dict("records")}, indent=1))
    _write_report(wide, summary)
    print("\nSUMMARY:", json.dumps(summary, indent=1))
    print(f"wrote → {OUT_DIR}")


def _summarise(wide: pd.DataFrame) -> dict:
    out = {}
    for bal in ("province_balanced", "city_balanced"):
        d = wide[f"delta_{bal}"].to_numpy(dtype=float)
        both = wide[["global", bal]].notna().all(axis=1)
        rel = ((wide.loc[both, bal] - wide.loc[both, "global"]) / wide.loc[both, "global"])
        out[bal] = {
            "n_cells_comparable": int(both.sum()),
            "median_delta_min_n": float(np.nanmedian(d)),
            "median_rel_change_pct": float(np.nanmedian(rel) * 100) if both.any() else float("nan"),
            "n_lower": int((d < 0).sum()), "n_higher": int((d > 0).sum()),
            "reachability_changed": int(
                (wide["global"].isna() ^ wide[bal].isna()).sum()),
        }
    return out


def _write_report(wide: pd.DataFrame, s: dict) -> None:
    def fmt(v):
        return "n/r" if pd.isna(v) else f"{v:.0f}"
    lines = ["| level | bracket | shape | null | global | prov-bal | city-bal | Δprov | Δcity |",
             "|---|---|---|---|---|---|---|---|---|"]
    for _, r in wide.sort_values(KEY).iterrows():
        lines.append(f"| {r['level']} | {r['bracket']} | {r['shape']} | {r['null_model']} | "
                     f"{fmt(r['global'])} | {fmt(r['province_balanced'])} | {fmt(r['city_balanced'])} | "
                     f"{fmt(r['delta_province_balanced'])} | {fmt(r['delta_city_balanced'])} |")
    cb, pb = s["city_balanced"], s["province_balanced"]
    md = f"""# §5 B4 scheme-(b) threshold re-run — DRAFT

> Quantifies whether the balanced width pools (scheme b) move the Phase-1 detection
> thresholds. Reduced precision (n_iter={N_ITER}, n_mc={N_MC}); **the balanced-vs-global
> Δ is the deliverable** — absolute min_n here is not the committed full-precision value.
> 'n/r' = not reachable at the level's max N (Decision 10).

## Headline

- **City-balanced:** median Δmin_n **{cb['median_delta_min_n']:+.0f}** inscriptions
  (median relative change **{cb['median_rel_change_pct']:+.1f}%**); {cb['n_lower']} cells
  lower, {cb['n_higher']} higher, of {cb['n_cells_comparable']} comparable;
  reachability changed in {cb['reachability_changed']} cells.
- **Province-balanced:** median Δmin_n **{pb['median_delta_min_n']:+.0f}**
  ({pb['median_rel_change_pct']:+.1f}%); {pb['n_lower']} lower / {pb['n_higher']} higher.

Interpretation: a narrower balanced corpus (city-balancing cut median width 99y → 79y)
means less aoristic smearing, so detection thresholds {'fall (easier detection)' if cb['median_delta_min_n'] < 0 else 'rise'} —
the expected direction. {'The shift is modest and does not change the substantive reachability picture.' if abs(cb['median_rel_change_pct']) < 25 and cb['reachability_changed'] <= 2 else 'The shift is large enough to change the reachability picture in some cells — see the table.'}

## Per-cell thresholds (min N for ≥{TARGET:.0%} detection)

{chr(10).join(lines)}

## Bottom line for B4

Scheme (a) is threshold-neutral by construction; scheme (b) moves thresholds
{'modestly' if abs(cb['median_rel_change_pct']) < 25 else 'materially'} and in the
expected direction (balanced → narrower → {'lower' if cb['median_delta_min_n'] < 0 else 'higher'} thresholds).
The committed full-precision thresholds (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`)
remain the primary; this is the preregistered §5 stratification robustness check, with the
v2-supersession caveat recorded in the obligations audit.

## Reproduce
```bash
uv run python runs/2026-06-16-s5-sensitivities/code/b4_threshold_rerun.py
```
"""
    (OUT_DIR / "REPORT-b4-rerun.md").write_text(md)


if __name__ == "__main__":
    main()
