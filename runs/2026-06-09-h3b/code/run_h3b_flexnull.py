#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_h3b_flexnull.py — Stage-B driver for the flexible-null robustness annex (a).
================================================================================

Runs part (a) of ``h3b-flexible-null-annex-spec-2026-06-15.md`` over the 29
cc-library units. For each unit:

  1. **Flexibility lever** — fit three smooth-null families to the posterior-median
     corrected count SPA and trace each on the effective-df (edf) axis:
       cpl k∈{2,3,5,7}; spline edf≈{5,10,20}; gp edf≈{5,10,20}.
     For each fit: build the Poisson MC envelope once; evaluate all ~8,000
     genuine-SPA posterior draws (λ=1.0 primary, λ=1.2 coverage sensitivity);
     record the pointwise global marginal-*p* + P(deviation) + per-draw spread,
     the de-powered **simultaneous-band** global *p*, and the two probe windows
     (Antonine, Crisis) with signed/one-sided readings.
  2. **Effective-N lever** — on the fixed CPL-3 null, thin to N′∈{1.5k…25k} (capped
     at n_eff) and record the global marginal-*p* + probe P(deficit) at each N′.

A **regression guard** asserts the k=3 CPL point reproduces the base run
(``outputs/drawwise/deviations.json``) bit-for-bit before the sweep runs; a light
sanity check validates the new spline/GP/simultaneous code. Writes
``outputs/flexnull/{flexnull-sweep.json,flexnull-table.csv,effn-thinning.json,
depowered-stat.json}``. Local/sapphire, permutation-only, no MCMC, no API.

Usage:  uv run python runs/2026-06-09-h3b/code/run_h3b_flexnull.py
Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-15.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

# Degenerate probe windows (empty / all-NaN kept bins on thinned or post-cutoff
# units) legitimately return NaN departures; silence the benign numpy warnings.
warnings.filterwarnings("ignore", message="Mean of empty slice")
warnings.filterwarnings("ignore", message="All-NaN slice encountered")

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-06-09-h3b/code"))
import h3b_drawwise as E   # noqa: E402
import h3b_flexnull as F   # noqa: E402

DRAWS_DIR = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
BASE_DEV = ROOT / "runs/2026-06-09-h3b/outputs/drawwise/deviations.json"
OUT_DIR = ROOT / "runs/2026-06-09-h3b/outputs/flexnull"
LAMBDAS = [1.0, 1.2]
NAMED = {"empire-aggregate", "latin-aggregate"}


def _probe_block(dd_counts, env):
    return {"antonine": E.probe_window(dd_counts, env, E.ANTONINE_WINDOW),
            "crisis": E.probe_window(dd_counts, env, E.CRISIS_WINDOW)}


# ---------------------------------------------------------------------------
# Pre-run guards
# ---------------------------------------------------------------------------
def regression_guard(units: list[dict]) -> None:
    """Assert the k=3 CPL point reproduces the base draw-wise run bit-for-bit."""
    base = {(r["name"], r["null"]): r for r in json.loads(BASE_DEV.read_text())}
    checked = 0
    for u in units:
        if u["name"] not in NAMED:
            continue
        draws_norm = E.load_draws_normalised(u["name"], DRAWS_DIR)
        n_eff = u["n_eff"]
        median_counts = np.median(draws_norm, axis=0) * n_eff
        idx = u["unit_index"]
        seed = F.MASTER_SEED + F.SEED_OFFSET["cpl"] + idx

        env_base = E.build_envelope("cpl", u, np.random.default_rng(seed),
                                    cpl_target=median_counts)
        fit3 = F.fit_mean_cpl(median_counts, 3)
        env_mine = F.build_envelope_from_mean(fit3["fitted"], n_eff,
                                              np.random.default_rng(seed))
        for key in ("lo", "hi", "mid"):
            assert np.allclose(env_base[key], env_mine[key], atol=0, rtol=0), \
                f"{u['name']}: envelope {key} mismatch vs base build_envelope"
        assert np.array_equal(env_base["mc_out"], env_mine["mc_out"]), \
            f"{u['name']}: mc_out mismatch vs base"

        dd1 = draws_norm * n_eff
        _, p_base = E.eval_draws(dd1, env_base)
        _, p_mine = E.eval_draws(dd1, env_mine)
        assert np.array_equal(p_base, p_mine), f"{u['name']}: per-draw p mismatch"
        marg = float(np.mean(p_mine))
        committed = base[(u["name"], "cpl")]["lambda_1.0"]["marginal_p"]
        assert abs(marg - committed) < 1e-9, \
            f"{u['name']}: marginal_p {marg} vs committed {committed}"
        checked += 1
    assert checked == 2, f"regression guard expected 2 named units, checked {checked}"
    print(f"  regression guard PASS ({checked} named units reproduce base bit-for-bit).")


def sanity_smooth(units: list[dict]) -> None:
    """Light validity check on the new spline/GP/simultaneous code (no garbage)."""
    u = next(x for x in units if x["name"] == "empire-aggregate")
    draws_norm = E.load_draws_normalised(u["name"], DRAWS_DIR)
    m = np.median(draws_norm, axis=0) * u["n_eff"]
    for fam, fn in (("spline", F.fit_mean_spline), ("gp", F.fit_mean_gp)):
        for tgt in F.SMOOTH_TARGET_EDF:
            fit = fn(m, tgt)
            assert np.all(np.isfinite(fit["fitted"])) and np.all(fit["fitted"] >= 0), \
                f"{fam} edf~{tgt}: non-finite/negative fitted mean"
            assert 2.0 <= fit["edf"] <= F.N_BINS, f"{fam}: edf {fit['edf']} out of range"
    env = F.build_envelope_from_mean(m, u["n_eff"], np.random.default_rng(1),
                                     return_mc=True)
    sim = F.simultaneous_eval(draws_norm * u["n_eff"], env)
    assert 0.0 <= sim["marginal_p_sim"] <= 1.0, "simultaneous p out of [0,1]"
    print("  smooth-null + simultaneous sanity PASS.")


# ---------------------------------------------------------------------------
# Per-unit sweep
# ---------------------------------------------------------------------------
def fit_specs():
    """(family, level-label, fit-callable) tuples defining the edf ladder."""
    specs = [("cpl", f"k{k}", (lambda m, k=k: F.fit_mean_cpl(m, k))) for k in F.CPL_KS]
    for tgt in F.SMOOTH_TARGET_EDF:
        specs.append(("spline", f"edf{int(tgt)}", (lambda m, t=tgt: F.fit_mean_spline(m, t))))
    for tgt in F.SMOOTH_TARGET_EDF:
        specs.append(("gp", f"edf{int(tgt)}", (lambda m, t=tgt: F.fit_mean_gp(m, t))))
    return specs


def run_unit(u: dict) -> tuple[list[dict], list[dict]]:
    draws_norm = E.load_draws_normalised(u["name"], DRAWS_DIR)
    n_eff = u["n_eff"]
    idx = u["unit_index"]
    median_counts = np.median(draws_norm, axis=0) * n_eff
    dd = {lam: E.inflate_draws(draws_norm, lam) * n_eff for lam in LAMBDAS}

    sweep_rows: list[dict] = []
    for family, level, fit_fn in fit_specs():
        fit = fit_fn(median_counts)
        seed = F.MASTER_SEED + F.SEED_OFFSET[family] + idx
        env = F.build_envelope_from_mean(fit["fitted"], n_eff,
                                         np.random.default_rng(seed), return_mc=True)
        agg = {lam: E.aggregate(E.eval_draws(dd[lam], env)[1]) for lam in LAMBDAS}
        sim = F.simultaneous_eval(dd[1.0], env)
        probes = _probe_block(dd[1.0], env)
        sweep_rows.append({
            "name": u["name"], "unit_index": idx, "n_eff": n_eff,
            "named_scope": u["name"] in NAMED,
            "soft_annotated": u["soft_annotated"], "reach_caveat": u["reach_caveat"],
            "family": family, "level": level, "edf": round(float(fit["edf"]), 3),
            "fit_converged": bool(fit.get("converged", True)),
            "fit_detail": {k: fit[k] for k in fit
                           if k in ("k", "target_edf", "aic", "rms",
                                    "log10_lambda", "length_scale", "n_basis")},
            "seed": int(seed),
            "marginal_p": round(agg[1.0]["marginal_p"], 6),
            "p_deviation": round(agg[1.0]["p_deviation"], 6),
            "p_draw_lo": round(agg[1.0]["p_draw_lo"], 6),
            "p_draw_hi": round(agg[1.0]["p_draw_hi"], 6),
            "marginal_p_lambda1.2": round(agg[1.2]["marginal_p"], 6),
            "marginal_p_sim": round(sim["marginal_p_sim"], 6),
            "p_sim_deviation": round(sim["p_sim_deviation"], 6),
            "antonine_p_deficit": round(probes["antonine"].get("p_deficit", float("nan")), 6),
            "antonine_p_dev": round(probes["antonine"]["p_window_dev"], 6),
            "antonine_rel_dep_med": round(
                probes["antonine"].get("windowed_rel_departure_med", float("nan")), 6),
            "crisis_p_deficit": round(probes["crisis"].get("p_deficit", float("nan")), 6),
            "crisis_p_dev": round(probes["crisis"]["p_window_dev"], 6),
            "crisis_rel_dep_med": round(
                probes["crisis"].get("windowed_rel_departure_med", float("nan")), 6),
        })

    # Effective-N thinning on the fixed CPL-3 null.
    fit3 = F.fit_mean_cpl(median_counts, 3)
    thin_rows: list[dict] = []
    for nprime in F.THIN_NPRIME:
        if nprime > n_eff:
            continue
        scale = nprime / n_eff
        env_t = F.build_envelope_from_mean(fit3["fitted"] * scale, nprime,
                                           np.random.default_rng(
                                               F.MASTER_SEED + F.SEED_OFFSET["thin"] + idx))
        dd_t = draws_norm * nprime
        agg_t = E.aggregate(E.eval_draws(dd_t, env_t)[1])
        probes_t = _probe_block(dd_t, env_t)
        thin_rows.append({
            "name": u["name"], "unit_index": idx, "n_eff": n_eff,
            "named_scope": u["name"] in NAMED, "n_prime": int(nprime),
            "marginal_p": round(agg_t["marginal_p"], 6),
            "antonine_p_deficit": round(
                probes_t["antonine"].get("p_deficit", float("nan")), 6),
            "crisis_p_deficit": round(
                probes_t["crisis"].get("p_deficit", float("nan")), 6),
        })
    return sweep_rows, thin_rows


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
def write_outputs(sweep: list[dict], thin: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "flexnull-sweep.json").write_text(json.dumps(sweep, indent=1))
    (OUT_DIR / "effn-thinning.json").write_text(json.dumps(thin, indent=1))
    # De-powered comparison: pointwise vs simultaneous marginal-p per sweep point.
    depow = [{"name": r["name"], "family": r["family"], "level": r["level"],
              "edf": r["edf"], "marginal_p_pointwise": r["marginal_p"],
              "marginal_p_simultaneous": r["marginal_p_sim"]} for r in sweep]
    (OUT_DIR / "depowered-stat.json").write_text(json.dumps(depow, indent=1))
    cols = ["name", "n_eff", "named_scope", "soft_annotated", "reach_caveat",
            "family", "level", "edf", "fit_converged",
            "marginal_p", "marginal_p_sim", "marginal_p_lambda1.2",
            "antonine_p_deficit", "crisis_p_deficit",
            "antonine_rel_dep_med", "crisis_rel_dep_med"]
    with (OUT_DIR / "flexnull-table.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in sweep:
            w.writerow([r[c] for c in cols])


def main() -> None:
    t0 = time.time()
    print("assembling 29 units ...", flush=True)
    units = E.assemble_units(DRAWS_DIR)
    print(f"  {len(units)} units with draws.\nrunning pre-run guards ...", flush=True)
    regression_guard(units)
    sanity_smooth(units)
    print("sweeping flexibility + effective-N levers ...", flush=True)

    sweep: list[dict] = []
    thin: list[dict] = []
    for u in units:
        s_rows, t_rows = run_unit(u)
        sweep.extend(s_rows)
        thin.extend(t_rows)
        cpl3 = next(r for r in s_rows if r["family"] == "cpl" and r["level"] == "k3")
        gp20 = next(r for r in s_rows if r["family"] == "gp" and r["level"] == "edf20")
        print(f"  [{u['unit_index']:2d}] {u['name']:<26} n_eff={u['n_eff']:>6} "
              f"cpl3 p={cpl3['marginal_p']:.3f}/sim={cpl3['marginal_p_sim']:.3f} "
              f"gp20 p={gp20['marginal_p']:.3f} AntPdef={gp20['antonine_p_deficit']:.2f}",
              flush=True)

    write_outputs(sweep, thin)
    print(f"\nwrote outputs → {OUT_DIR}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
