#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pilot.py — the hybrid pilot: one joint fit over the 29 units + concordance preview.
=======================================================================================

Fits the global-θ hybrid (hybrid_lib) once on the real 29 production units and checks
(spec.md §Pilot): sampler health, the global θ posterior vs the calibrated (0.945,
0.155), and a concordance preview — do the cross-classified per-unit α medians
(`refit-summary.json`) fall inside the hybrid's per-unit α 95% CIs, mean discrepancy
< 0.05? Emits HYBRID-PILOT-REPORT.md + hybrid-pilot.json.

Usage (sapphire) — PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
    uv run python code/run_pilot.py [--draws 1500] [--tune 1500] [--target-accept 0.95]

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

HYB = Path("/home/shawn/Code/inscriptions/runs/2026-06-14-hybrid-robustness")
REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
sys.path.insert(0, str(HYB / "code"))
sys.path.insert(0, str(REFIT / "code"))
import hybrid_lib as Hy  # noqa: E402
import refit_lib as R  # noqa: E402

REFIT_SUMMARY = REFIT / "outputs" / "refit-summary.json"
THETA_CALIB_CONV, THETA_CALIB_GEN = 0.945, 0.155


def main() -> None:
    import arviz as az
    import pymc as pm

    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=1500)
    ap.add_argument("--tune", type=int, default=1500)
    ap.add_argument("--target-accept", type=float, default=0.95)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--cores", type=int, default=4)
    args = ap.parse_args()

    (HYB / "outputs").mkdir(parents=True, exist_ok=True)
    data = Hy.assemble_unit_data()
    basis, _ = R.load_library_basis()
    model = Hy.build_model_hybrid(data, basis)
    U = len(data["names"])
    print(f"hybrid pilot: {U} units, library {basis.shape[0]} rows; "
          f"draws {args.draws} tune {args.tune} chains {args.chains} cores {args.cores}",
          flush=True)

    t0 = time.time()
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=args.draws, tune=args.tune, chains=args.chains,
                              cores=args.cores, target_accept=args.target_accept,
                              random_seed=20260614, progressbar=False,
                              return_inferencedata=True)
    secs = time.time() - t0

    # Sampler health over the sampled blocks.
    summ = az.summary(idata, var_names=["alpha", "tier_weights", "sigma", "z",
                                        "theta_conv", "theta_gen"], round_to="none")
    max_rhat = float(summ["r_hat"].max())
    min_ess = float(summ["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    # Global θ posterior.
    tc = idata.posterior["theta_conv"].values.reshape(-1)
    tg = idata.posterior["theta_gen"].values.reshape(-1)
    theta = {
        "theta_conv": {"median": float(np.median(tc)),
                       "ci": [float(np.percentile(tc, 2.5)), float(np.percentile(tc, 97.5))],
                       "calibrated": THETA_CALIB_CONV},
        "theta_gen": {"median": float(np.median(tg)),
                      "ci": [float(np.percentile(tg, 2.5)), float(np.percentile(tg, 97.5))],
                      "calibrated": THETA_CALIB_GEN},
    }

    # Per-unit hybrid α + concordance vs the cross-classified refit α.
    a_post = idata.posterior["alpha"].values.reshape(-1, U)
    refit = {r["name"]: r for r in json.loads(REFIT_SUMMARY.read_text())["units"]}
    rows, discrepancies, inside = [], [], 0
    for i, name in enumerate(data["names"]):
        ai = a_post[:, i]
        hy_med = float(np.median(ai))
        hy_lo, hy_hi = float(np.percentile(ai, 2.5)), float(np.percentile(ai, 97.5))
        cc = refit.get(name, {})
        cc_med = cc.get("alpha_median")
        in_ci = (cc_med is not None) and (hy_lo <= cc_med <= hy_hi)
        inside += int(in_ci)
        if cc_med is not None:
            discrepancies.append(hy_med - cc_med)
        rows.append({"name": name, "hybrid_alpha_med": hy_med,
                     "hybrid_ci": [hy_lo, hy_hi], "cc_alpha_med": cc_med,
                     "cc_in_hybrid_ci": bool(in_ci),
                     "discrepancy": (hy_med - cc_med) if cc_med is not None else None})

    disc = np.array(discrepancies)
    concordance = {
        "n_units": U,
        "cc_median_inside_hybrid_ci": inside,
        "frac_inside": round(inside / U, 3),
        "mean_discrepancy": float(disc.mean()),
        "max_abs_discrepancy": float(np.abs(disc).max()),
    }
    healthy = (max_rhat < 1.01) and (min_ess >= 400)
    theta_sane = (theta["theta_conv"]["ci"][0] <= THETA_CALIB_CONV <= theta["theta_conv"]["ci"][1]
                  or abs(theta["theta_conv"]["median"] - THETA_CALIB_CONV) < 0.1)

    out = {"secs": round(secs, 1), "max_rhat": max_rhat, "min_ess_bulk": min_ess,
           "n_divergences": n_div, "sampler_healthy": healthy,
           "theta": theta, "theta_sane": bool(theta_sane),
           "concordance": concordance, "units": rows}
    (HYB / "outputs" / "hybrid-pilot.json").write_text(json.dumps(out, indent=1))

    lines = [
        "# Hybrid robustness — PILOT report (global-θ cross-classified, one joint fit)", "",
        f"Joint fit over {U} units in {secs/60:.1f} min. "
        f"Sampler: max R̂ {max_rhat:.4f}, min bulk-ESS {min_ess:.0f}, "
        f"{n_div} divergences → **{'HEALTHY' if healthy else 'MARGINAL/FAIL'}**.", "",
        "## Global θ (estimated, wide prior) vs the lead's calibrated values",
        f"- θ_conv {theta['theta_conv']['median']:.3f} "
        f"[{theta['theta_conv']['ci'][0]:.3f}, {theta['theta_conv']['ci'][1]:.3f}] "
        f"(calibrated {THETA_CALIB_CONV})",
        f"- θ_gen {theta['theta_gen']['median']:.3f} "
        f"[{theta['theta_gen']['ci'][0]:.3f}, {theta['theta_gen']['ci'][1]:.3f}] "
        f"(calibrated {THETA_CALIB_GEN})",
        f"- θ sane vs calibration: **{theta_sane}**", "",
        "## Concordance preview (cross-classified α vs hybrid α)",
        f"- cc median inside hybrid 95% CI: **{inside}/{U}** ({concordance['frac_inside']:.0%})",
        f"- mean discrepancy (hybrid − cc): **{concordance['mean_discrepancy']:+.3f}** "
        f"(concordant if |mean| < 0.05)",
        f"- max |discrepancy|: {concordance['max_abs_discrepancy']:.3f}", "",
        "## Per-unit (sorted by |discrepancy|)",
        "| unit | cc α | hybrid α [95% CI] | in CI | Δ |",
        "|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda x: -abs(x["discrepancy"] or 0)):
        cc = f"{r['cc_alpha_med']:.3f}" if r["cc_alpha_med"] is not None else "·"
        d = f"{r['discrepancy']:+.3f}" if r["discrepancy"] is not None else "·"
        lines.append(f"| {r['name']} | {cc} | {r['hybrid_alpha_med']:.3f} "
                     f"[{r['hybrid_ci'][0]:.3f}, {r['hybrid_ci'][1]:.3f}] | "
                     f"{'yes' if r['cc_in_hybrid_ci'] else 'NO'} | {d} |")
    gate = healthy and theta_sane and concordance["frac_inside"] >= 0.5
    lines += ["", f"## Gate to advance to hierarchical validation: "
              f"**{'PASS' if gate else 'REVIEW'}** "
              f"(sampler healthy AND θ sane AND no gross concordance breakdown)", ""]
    (HYB / "outputs" / "HYBRID-PILOT-REPORT.md").write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\nWrote HYBRID-PILOT-REPORT.md + hybrid-pilot.json")


if __name__ == "__main__":
    main()
