#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate_theta.py — calibrate θ_conv, θ_gen from the identifiable production units.
====================================================================================

The joint model's classification term ``k ~ Binomial(N, α·θ_conv + (1−α)·θ_gen)``
needs ``θ_conv`` (≈ P[grid-aligned | convention-class]) and ``θ_gen`` (≈ P[grid-
aligned | genuine-class]) pinned — a single per-unit binomial cannot identify all
three jointly (spec §4.1). We calibrate the prior CENTRES empirically from the units
whose temporal ``α`` is RELIABLE (``under_identified == False`` in the production
``summary-final.json``), by least-squares fit of::

    aligned_frac(unit) ≈ θ_gen + (θ_conv − θ_gen) · α_shared(unit)

over the identifiable units, for each grid-alignment rule {A, C, D} (spec §3). The
classification-implied ``α`` = ``(aligned_frac − θ_gen)/(θ_conv − θ_gen)`` is reported
per unit alongside the production ``[α_shared, α_perunit]`` bracket, so its position is
explicit.

Output
------
``outputs/theta-calibration.json`` — per-rule (θ_conv, θ_gen, RMSE) + per-unit
aligned fractions and implied α. This is the reproducible source of the spec §4.1
numbers; the POC and any production refit read θ from here.

Run
---
    PATH=/home/shawn/.local/bin:$PATH uv run python code/calibrate_theta.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
SUMMARY_FINAL = (
    Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep")
    / "outputs" / "production" / "summary-final.json"
)
sys.path.insert(0, str(H2))
sys.path.insert(0, str(RUN / "code"))

import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402

RULES = ("A", "C", "D")


def fit_theta(alpha: np.ndarray, aligned_frac: np.ndarray) -> tuple[float, float, float]:
    """Constrained grid least-squares for (θ_gen, θ_conv) with 0 ≤ θ_gen < θ_conv ≤ 1.

    Returns (θ_gen, θ_conv, RMSE). The grid (θ_gen ∈ [0, 0.30], θ_conv ∈ [0.55, 1.0])
    keeps the solution interpretable (genuine rarely aligned; convention usually
    aligned) and matches the spec §4.1 search.
    """
    best = None
    for tg in np.linspace(0.0, 0.30, 61):
        for tc in np.linspace(0.55, 1.0, 91):
            pred = tg + (tc - tg) * alpha
            sse = float(((pred - aligned_frac) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, float(tg), float(tc))
    sse, tg, tc = best
    return tg, tc, float(np.sqrt(sse / len(alpha)))


def main() -> None:
    summary = json.loads(SUMMARY_FINAL.read_text(encoding="utf-8"))
    by_name = {r["name"]: r for r in summary}

    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    units = H.enumerate_units()

    # Per-unit aligned fractions under each rule (row-weighted).
    per_unit: dict[str, dict] = {}
    idx_full = df.index
    for u in units:
        sub = H.subset_corpus(df, u, latin)
        loc = idx_full.get_indexer(sub.index)
        rec = by_name.get(u["name"], {})
        entry = {
            "name": u["name"],
            "kind": u["kind"],
            "n_rows": int(len(sub)),
            "under_identified": rec.get("under_identified"),
            "alpha_shared": rec.get("alpha_shared"),
            "alpha_perunit": rec.get("alpha_perunit"),
            "aligned_frac": {},
        }
        for rule in RULES:
            ind = J.aligned_indicator(df, rule=rule)
            entry["aligned_frac"][rule] = float(ind[loc].mean()) if len(loc) else float("nan")
        per_unit[u["name"]] = entry

    # Calibrate θ per rule on the identifiable units.
    calib: dict[str, dict] = {}
    ident = [e for e in per_unit.values()
             if e["under_identified"] is False and e["alpha_shared"] is not None]
    for rule in RULES:
        a = np.array([e["alpha_shared"] for e in ident], dtype=float)
        k = np.array([e["aligned_frac"][rule] for e in ident], dtype=float)
        tg, tc, rmse = fit_theta(a, k)
        calib[rule] = {
            "theta_gen": round(tg, 4),
            "theta_conv": round(tc, 4),
            "rmse": round(rmse, 4),
            "n_calib": len(ident),
        }
        # implied alpha per unit under this rule
        for e in per_unit.values():
            kf = e["aligned_frac"][rule]
            impl = (kf - tg) / (tc - tg) if (tc - tg) > 0 else float("nan")
            e.setdefault("implied_alpha", {})[rule] = float(np.clip(impl, 0.0, 1.0))

    out = {
        "generated": "2026-06-09",
        "source_summary": str(SUMMARY_FINAL),
        "lead_rule": "C",
        "calibration": calib,
        "n_identifiable_calib": len(ident),
        "units": list(per_unit.values()),
    }
    out_path = RUN / "outputs" / "theta-calibration.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Console summary.
    print("θ calibration (identifiable units, n =", len(ident), "):")
    for rule in RULES:
        c = calib[rule]
        print(f"  rule {rule}: θ_gen={c['theta_gen']:.3f}  θ_conv={c['theta_conv']:.3f}  "
              f"RMSE={c['rmse']:.3f}")
    print(f"\nWrote {out_path}")
    print("\nUnder-identified units — classification-implied α (rule C) vs bracket:")
    print(f"  {'unit':30s} {'a_sh':>5s} {'a_pu':>5s} {'alnC':>5s} {'implC':>5s}")
    for e in per_unit.values():
        if e["under_identified"] is True:
            print(f"  {e['name'][:30]:30s} {e['alpha_shared']:5.2f} {e['alpha_perunit']:5.2f} "
                  f"{e['aligned_frac']['C']:5.2f} {e['implied_alpha']['C']:5.2f}")


if __name__ == "__main__":
    main()
