#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rederive_theta.py — (B) re-derive θ from the corrected cc-library α's.
======================================================================

The pilot found the hybrid robustly wants θ_gen ≈ 0.02 vs the calibrated 0.155.
Hypothesis (HYBRID-PILOT-FINDINGS.md finding 2): `calibrate_theta.py` fit θ_gen as
the intercept of `aligned_frac ≈ θ_gen + (θ_conv − θ_gen)·α` using the
**under-attributing shared-basis α_shared**; biased-low α's inflate the intercept.

This script re-runs that exact constrained least-squares fit but swapping α_shared for
the **cross-classified α** (`refit-summary.json`), for two aligned-fraction
definitions:
  * **row** — the row aligned-fraction `calibrate_theta` used (to reproduce 0.155);
  * **mass** — the aoristic-effective k/N the cc binomial actually sees (the operative
    quantity for the cc model's θ).

Reports θ (θ_gen, θ_conv, RMSE) under {α_shared, α_cc} × {row, mass}, over both the
original identifiable subset and all 29 units. Local; no PyMC.

Run — PATH=~/.local/bin:$PATH uv run python code/rederive_theta.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
HYB = Path("/home/shawn/Code/inscriptions/runs/2026-06-14-hybrid-robustness")
REFIT_SUMMARY = REFIT / "outputs" / "refit-summary.json"
THETA_CALIB = JOINT / "outputs" / "theta-calibration.json"


def fit_theta(alpha: np.ndarray, aligned_frac: np.ndarray) -> tuple[float, float, float]:
    """Constrained grid least-squares for (θ_gen, θ_conv), 0 ≤ θ_gen < θ_conv ≤ 1.
    VERBATIM grid from calibrate_theta.fit_theta (θ_gen ∈ [0, 0.30], θ_conv ∈
    [0.55, 1.0])."""
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
    units = json.loads(REFIT_SUMMARY.read_text())["units"]
    calib_units = {u["name"]: u for u in json.loads(THETA_CALIB.read_text())["units"]}

    # Assemble per-unit (α_shared, α_cc, row_frac, mass_frac, under_identified).
    rows = []
    for u in units:
        name = u["name"]
        cu = calib_units.get(name, {})
        mass_frac = (u["k_aligned_eff"] / u["n_rows_eff"]) if u.get("n_rows_eff") else None
        rows.append({
            "name": name,
            "alpha_shared": u.get("h2_alpha_shared"),
            "alpha_cc": u.get("alpha_median"),
            "row_frac": u.get("row_aligned_frac"),
            "mass_frac": round(mass_frac, 4) if mass_frac is not None else None,
            # original calibration used under_identified==False as the identifiable set
            "under_identified": (cu.get("under_identified")
                                 if "under_identified" in cu else u.get("h2_under_identified")),
        })

    def do_fit(alpha_key: str, frac_key: str, subset: str) -> dict:
        sel = [r for r in rows
               if r[alpha_key] is not None and r[frac_key] is not None
               and (subset == "all" or r["under_identified"] is False)]
        a = np.array([r[alpha_key] for r in sel], dtype=float)
        f = np.array([r[frac_key] for r in sel], dtype=float)
        tg, tc, rmse = fit_theta(a, f)
        return {"theta_gen": round(tg, 4), "theta_conv": round(tc, 4),
                "rmse": round(rmse, 4), "n": len(sel)}

    out = {"generated": "2026-06-14", "calibrated_reference": {"theta_gen": 0.155,
           "theta_conv": 0.945, "note": "calibrate_theta.py rule C, row-frac vs α_shared, identifiable"},
           "fits": {}}
    print(f"{'condition':42s} {'n':>3s} {'θ_gen':>7s} {'θ_conv':>7s} {'RMSE':>6s}")
    for alpha_key, alabel in (("alpha_shared", "α_shared"), ("alpha_cc", "α_cc")):
        for frac_key, flabel in (("row_frac", "row"), ("mass_frac", "mass")):
            for subset in ("identifiable", "all"):
                key = f"{alabel}×{flabel}×{subset}"
                fit = do_fit(alpha_key, frac_key, subset)
                out["fits"][key] = fit
                print(f"{key:42s} {fit['n']:3d} {fit['theta_gen']:7.3f} "
                      f"{fit['theta_conv']:7.3f} {fit['rmse']:6.3f}")

    (HYB / "outputs" / "theta-rederivation.json").write_text(json.dumps(out, indent=1))
    print(f"\nWrote {HYB / 'outputs' / 'theta-rederivation.json'}")
    print("\nKey contrast — the operative cc quantity (mass-frac):")
    print(f"  calibrated (α_shared, row, identifiable): θ_gen 0.155  [the production prior centre]")
    base = out["fits"]["α_shared×row×identifiable"]
    rederiv = out["fits"]["α_cc×mass×all"]
    print(f"  reproduce  (α_shared, row, identifiable): θ_gen {base['theta_gen']:.3f}")
    print(f"  RE-DERIVED (α_cc,     mass, all 29):      θ_gen {rederiv['theta_gen']:.3f}, "
          f"θ_conv {rederiv['theta_conv']:.3f}")


if __name__ == "__main__":
    main()
