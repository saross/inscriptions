#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrate.py — §5 Layer-A PRODUCTION orchestrator (BUILD, do NOT auto-run).
=============================================================================

The single launch entrypoint for the §5 Layer-A production run. Given the
prepared caches (25y + 50y, both units' weights), it runs, in order:

1. **The 4 monolithic hierarchical fits** — unit ∈ {inscription, letter} ×
   bin-width ∈ {25y, 50y}, all over the 268 target cities + 45 provinces, with
   the PINNED hyperprior scales (``s_g=0.3, s_u=0.15, s_v=0.15``),
   ``target_accept=0.99``, convergence gates (R-hat < 1.01, bulk ESS >= 400,
   0 divergences; ONE escalation on a miss, gate never relaxed), saving each
   posterior to NetCDF. The inscription fits use ``hier_model``; the letter fits
   use ``letter_model`` with the PPC-selected observation form (``nb``).
   The 4 fits are INDEPENDENT and run concurrently (one process each).

2. **The subsample-recover calibration grid** (``subsample_recover``): 7 donors
   × N ∈ {50,100,200,300,500} × ~40 reps standalone single-city fits,
   embarrassingly parallel across the cores not used by step 1.

3. **Aggregate diagnostics**:
   - precision-vs-N curve + calibration N* (from step 2);
   - trajectory-shape clustering across the 268 target cities (k-means on the
     unit-sum posterior-median trajectories; reports cluster sizes + medoids);
   - 7-anchor INTERNAL CONSISTENCY: each anchor's monolithic posterior trajectory
     vs its own model-free aoristic SPA (Pearson r; smoothing must not distort a
     data-rich city);
   - Pompeii AD-79 EXTERNAL check: genuinely-post-79 mass (bins >= AD 100) should
     be ~0 in the inscription unit.

Parallelism (zbook, 16 physical cores)
--------------------------------------
- Step 1: the 4 monolithic fits are independent; each is launched as its own
  process and samples its 4 chains across 4 cores -> 16 cores for ~4 concurrent
  fits. (25y inscription is the heaviest; 50y and letter are cheaper.)
- Step 2: ``--subsample-parallel`` workers × ``--subsample-cores`` chains.
- Steps 1–2 NEVER sample in the orchestrator's own process — they spawn the fit
  scripts / pool workers. Step 3's anchor internal-consistency and Pompeii AD-79
  checks DO call ``m.fit()`` in-process, but only AFTER the Step 1–2 process
  pools have closed, under the same thread-pinned environment, so they never
  contend with the spawned fits. Nothing samples on import.

SAFETY
------
This module DOES NOT execute anything on import. ``main()`` is gated behind an
explicit ``--confirm-production`` flag for the full run; without it, ``main()``
prints the plan + the per-component run-time estimate and EXITS (a dry run).
The full ``--confirm-production`` path is the PRODUCTION RUN and must be launched
deliberately by Shawn — it is NOT run during the build/benchmark phase.

Launch (PRODUCTION — Shawn runs this deliberately, not during build)::

    source ~/cc-scratch/s5/s5-env.sh
    $PY runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py \
        --confirm-production \
        --out-base runs/2026-05-30-s5-small-n-trajectories/code/production

Dry run (prints plan + estimate, runs nothing)::

    $PY runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp  # noqa: E402

# The 4 monolithic fit configs. bin_width selects the cache; unit selects the
# model + weight; letter uses the PPC-selected observation form.
MONO_CONFIGS = [
    {"unit": "inscription", "bin_width": 25},
    {"unit": "inscription", "bin_width": 50},
    {"unit": "letter", "bin_width": 25},
    {"unit": "letter", "bin_width": 50},
]
LETTER_OBS_FORM = "nb"  # selected by letter_ppc.py (see PRODUCTION-READY.md).

PINNED_SCALES = {"s_g": 0.3, "s_u": 0.15, "s_v": 0.15}

# Subsample-stage worker count. ONE source of truth shared by the production
# run (the ``--subsample-parallel`` argparse default) and the dry-run estimate,
# so the printed estimate models the SAME parallelism the run will actually use.
# (Previously the estimate hard-coded 4 while the run defaulted to 8, over-
# stating the subsample stage ~2x.)
DEFAULT_SUBSAMPLE_PARALLEL = 8


# --------------------------------------------------------------------------- #
# Target-city subset for a given grid.
# --------------------------------------------------------------------------- #

def target_cities(out_dir: Path) -> list[str]:
    """The 268 target cities (``bucket == "target"``) for the monolithic fit."""
    idx = pd.read_parquet(out_dir / "city-index.parquet")
    return idx[idx["bucket"] == "target"]["city"].tolist()


def anchor_cities(out_dir: Path) -> list[str]:
    """The 7 large validation anchors (``bucket == "large_anchor"``)."""
    idx = pd.read_parquet(out_dir / "city-index.parquet")
    return idx[idx["bucket"] == "large_anchor"]["city"].tolist()


# --------------------------------------------------------------------------- #
# One monolithic fit (child process). Returns convergence + saves NetCDF.
# --------------------------------------------------------------------------- #

def _run_monolithic(cfg: dict) -> dict:
    """Child-process worker: assemble + fit one monolithic model, save posterior.

    Inscription unit -> ``hier_model``; letter unit -> ``letter_model`` (nb form).
    Applies the pinned scales + convergence gates with one escalation.
    """
    unit = cfg["unit"]
    bin_width = cfg["bin_width"]
    out_dir = Path(cfg["out_dir"])
    save_path = Path(cfg["save_path"])
    draws, tune, chains, cores = cfg["draws"], cfg["tune"], cfg["chains"], cfg["cores"]
    target_accept = cfg["target_accept"]
    seed = cfg["seed"]
    escalate = cfg["escalate"]
    cities = cfg["cities"]

    t0 = time.perf_counter()
    if unit == "inscription":
        import hier_model as model
        data = model.assemble(out_dir, cities)
        idata = model.fit(data, draws=draws, tune=tune, chains=chains,
                          cores=cores, target_accept=target_accept,
                          random_seed=seed, progressbar=False,
                          **PINNED_SCALES)
    else:  # letter
        import letter_model as model
        data = model.assemble(out_dir, cities)
        idata = model.fit(data, obs_form=LETTER_OBS_FORM, draws=draws, tune=tune,
                          chains=chains, cores=cores, target_accept=target_accept,
                          random_seed=seed, progressbar=False, **PINNED_SCALES)
    conv = model.convergence_summary(idata)
    passed = model.gates_pass(conv)

    if not passed and escalate:
        d2, t2 = draws * 2, tune * 2
        if unit == "inscription":
            idata = model.fit(data, draws=d2, tune=t2, chains=chains, cores=cores,
                              target_accept=target_accept, random_seed=seed + 1,
                              progressbar=False, **PINNED_SCALES)
        else:
            idata = model.fit(data, obs_form=LETTER_OBS_FORM, draws=d2, tune=t2,
                              chains=chains, cores=cores,
                              target_accept=target_accept, random_seed=seed + 1,
                              progressbar=False, **PINNED_SCALES)
        conv = model.convergence_summary(idata)
        passed = model.gates_pass(conv)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    idata.to_netcdf(str(save_path))
    wall = time.perf_counter() - t0
    return {
        "unit": unit, "bin_width": bin_width, "n_cities": len(cities),
        "save_path": str(save_path), "wall_s": wall,
        "convergence": conv, "gates_pass": bool(passed),
    }


# --------------------------------------------------------------------------- #
# Step 1: the 4 monolithic fits, concurrently.
# --------------------------------------------------------------------------- #

def run_monolithic_fits(out_base: Path, draws: int, tune: int, chains: int,
                        cores: int, target_accept: float, seed: int,
                        escalate: bool, max_concurrent: int) -> list[dict]:
    """Launch the 4 monolithic fits concurrently and collect their results."""
    cfgs = []
    for i, c in enumerate(MONO_CONFIGS):
        cache = dp.default_cache_dir(c["bin_width"])
        cities = target_cities(cache)
        tag = f"{c['unit']}-{c['bin_width']}y"
        cfgs.append({
            **c, "out_dir": str(cache), "cities": cities,
            "save_path": str(out_base / f"monolithic-{tag}.nc"),
            "draws": draws, "tune": tune, "chains": chains, "cores": cores,
            "target_accept": target_accept, "seed": seed + i, "escalate": escalate,
        })
    print(f"Step 1: {len(cfgs)} monolithic fits, "
          f"{max_concurrent} concurrent x {cores} chains "
          f"(~{max_concurrent * cores} cores).")
    results = []
    with ProcessPoolExecutor(max_workers=max_concurrent) as ex:
        futs = {ex.submit(_run_monolithic, cfg): cfg for cfg in cfgs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            print(f"  DONE {r['unit']}-{r['bin_width']}y: "
                  f"gates_pass={r['gates_pass']} "
                  f"rhat={r['convergence']['max_rhat']:.4f} "
                  f"ess={r['convergence']['min_ess_bulk']:.0f} "
                  f"div={r['convergence']['n_divergences']} "
                  f"({r['wall_s']:.0f}s) -> {r['save_path']}")
    return results


# --------------------------------------------------------------------------- #
# Step 3 diagnostics.
# --------------------------------------------------------------------------- #

def trajectory_clustering(idata_path: Path, var: str, n_clusters: int = 6,
                          seed: int = 0) -> dict:
    """K-means clustering of the 268 cities' unit-sum posterior-median shapes.

    Args:
        idata_path: NetCDF of a monolithic fit.
        var: posterior trajectory variable (``"lam"`` inscription / ``"Lambda"``
            letter).
        n_clusters: cluster count.
        seed: k-means seed.

    Returns:
        Dict with cluster labels, sizes, and the per-cluster medoid city.
    """
    import arviz as az
    from sklearn.cluster import KMeans

    idata = az.from_netcdf(str(idata_path))
    lam = idata.posterior[var].median(("chain", "draw")).values  # (C, T)
    cities = list(idata.posterior[var].coords["city"].values)
    shapes = lam / lam.sum(axis=1, keepdims=True)
    km = KMeans(n_clusters=n_clusters, random_state=seed, n_init=10).fit(shapes)
    labels = km.labels_
    sizes = {int(k): int((labels == k).sum()) for k in range(n_clusters)}
    medoids = {}
    for k in range(n_clusters):
        members = np.where(labels == k)[0]
        if members.size == 0:
            continue
        d = np.linalg.norm(shapes[members] - km.cluster_centers_[k], axis=1)
        medoids[int(k)] = str(cities[members[int(np.argmin(d))]])
    return {"n_clusters": n_clusters, "sizes": sizes, "medoids": medoids}


def anchor_internal_consistency(out_dir: Path, draws: int, tune: int,
                                chains: int, cores: int, target_accept: float,
                                seed: int) -> dict:
    """§8a.1 internal consistency: each anchor's full-N standalone trajectory
    vs its own model-free aoristic SPA.

    The 7 large anchors are NOT in the monolithic target-set fit (that is the
    268 ``target`` cities); the internal-consistency check is on the anchors'
    OWN data-rich standalone fits (spec §8a.1 — confirm smoothing + the
    likelihood do not distort a data-rich city). Each anchor is fitted standalone
    via ``model.py`` (cheap; these are the same full-N donor truth fits as the
    subsample grid) and its posterior-median trajectory shape is correlated with
    the raw aoristic SPA shape (Pearson r; near 1.0 = no distortion).
    """
    import model as m  # noqa: E402

    out = {}
    for anchor in anchor_cities(out_dir):
        b = dp.load_city(out_dir, anchor)
        A = np.asarray(b["A"], dtype=float)
        idata = m.fit(A, draws=draws, tune=tune, chains=chains, cores=cores,
                      target_accept=target_accept, random_seed=seed,
                      progressbar=False)
        med = idata.posterior["lam"].median(("chain", "draw")).values
        L = A.sum(1) * b["bin_width"]
        P = (A * b["bin_width"]) / L[:, None]
        spa = P.sum(0)                         # model-free SPA (sums to N)
        conv = m.convergence_summary(idata)
        out[anchor] = {
            "N": int(A.shape[0]),
            "shape_r_vs_spa": float(
                np.corrcoef(med / med.sum(), spa / spa.sum())[0, 1]),
            "gates_pass": bool(m.gates_pass(conv)),
        }
    return out


def pompeii_ad79_external(out_dir: Path, draws: int, tune: int, chains: int,
                          cores: int, target_accept: float, seed: int) -> dict:
    """§8a.2 Pompeii AD-79 external check (standalone Pompeii fit).

    Pompeii is a large anchor (buried AD 79), so genuinely-post-79 mass — bins
    starting at/after AD 100, which are entirely after the eruption — should be
    ~0. (The AD 75–100 bin legitimately holds Pompeii's final pre-eruption years
    AD 75–79, so it is excluded from the "post-79" sum; cf. the smoke writeup.)
    Pompeii is not in the monolithic target-set fit, so this uses its own
    standalone fit.
    """
    import model as m  # noqa: E402

    b = dp.load_city(out_dir, "Pompeii")
    A = np.asarray(b["A"], dtype=float)
    idata = m.fit(A, draws=draws, tune=tune, chains=chains, cores=cores,
                  target_accept=target_accept, random_seed=seed,
                  progressbar=False)
    med = idata.posterior["lam"].median(("chain", "draw")).values
    edges, _ = dp.make_grid(int(b["bin_width"]))
    bin_lo = edges[:-1]
    post79 = bin_lo >= 100  # bins starting at/after AD 100 are fully post-79
    return {
        "N": int(A.shape[0]),
        "post79_mass": float(med[post79].sum()),
        "total_mass": float(med.sum()),
        "post79_frac": float(med[post79].sum() / med.sum()),
    }


# --------------------------------------------------------------------------- #
# Run-time estimate (printed by the dry run; populated by BENCHMARK numbers).
# --------------------------------------------------------------------------- #

def runtime_estimate(bench: dict | None) -> dict:
    """Assemble the production run-time estimate from BENCHMARK inputs.

    Args:
        bench: Optional dict of measured timings (``t_single_s``,
            ``t_mono25_insc_s``, ``t_mono25_letter_s``, ``t_mono50_*``). If None,
            placeholders are used and the estimate is flagged provisional.

    Returns:
        A dict with the per-component and total wall-clock estimate (range).
    """
    b = bench or {}
    # Defaults (provisional) if no benchmark provided.
    t_single = b.get("t_single_s", 60.0)
    t_mono25_insc = b.get("t_mono25_insc_s", 3600.0)
    t_mono50_insc = b.get("t_mono50_insc_s", t_mono25_insc * 0.5)
    t_mono25_letter = b.get("t_mono25_letter_s", t_mono25_insc)
    t_mono50_letter = b.get("t_mono50_letter_s", t_mono25_letter * 0.5)
    # 4 fits run concurrently (16 cores / 4 chains = 4 slots): wall = the SLOWEST.
    mono_wall_concurrent = max(t_mono25_insc, t_mono50_insc,
                               t_mono25_letter, t_mono50_letter)
    mono_wall_serial = (t_mono25_insc + t_mono50_insc
                        + t_mono25_letter + t_mono50_letter)
    # Subsample grid: 7 donors x 5 N x 40 reps = 1400 fits, ~16-way parallel.
    # Model the parallelism the PRODUCTION RUN will use (the shared default), NOT
    # the benchmark probe's worker count — the estimate is about the production
    # run, whose ``--subsample-parallel`` defaults to DEFAULT_SUBSAMPLE_PARALLEL.
    n_sub = 7 * 5 * 40
    sub_parallel = DEFAULT_SUBSAMPLE_PARALLEL
    sub_wall = n_sub * t_single / sub_parallel
    return {
        "t_single_s": t_single,
        "t_mono25_insc_s": t_mono25_insc,
        "t_mono50_insc_s": t_mono50_insc,
        "t_mono25_letter_s": t_mono25_letter,
        "t_mono50_letter_s": t_mono50_letter,
        "mono_wall_concurrent_s": mono_wall_concurrent,
        "mono_wall_serial_s": mono_wall_serial,
        "n_subsample_fits": n_sub,
        "subsample_parallel": sub_parallel,
        "subsample_wall_s": sub_wall,
        "total_wall_concurrent_s": mono_wall_concurrent + sub_wall,
        "total_wall_concurrent_h": (mono_wall_concurrent + sub_wall) / 3600.0,
        "provisional": bench is None,
    }


def print_plan(out_base: Path, args, bench: dict | None) -> None:
    """Dry-run plan + run-time estimate (no sampling)."""
    est = runtime_estimate(bench)
    print("=" * 72)
    print("§5 LAYER-A PRODUCTION PLAN  (DRY RUN — nothing sampled)")
    print("=" * 72)
    print("Step 1 — 4 monolithic fits (268 target cities, pinned scales "
          "s_g=0.3 s_u=0.15 s_v=0.15, target_accept=0.99):")
    for c in MONO_CONFIGS:
        print(f"   - {c['unit']:>11}-{c['bin_width']}y  "
              f"(letter form: {LETTER_OBS_FORM})"
              if c["unit"] == "letter" else
              f"   - {c['unit']:>11}-{c['bin_width']}y")
    print("Step 2 — subsample-recover grid: 7 donors x 5 N x ~40 reps "
          "= ~1400 standalone fits.")
    print("Step 3 — diagnostics: precision-vs-N, trajectory clustering, "
          "7-anchor internal consistency, Pompeii AD-79 external.")
    print("-" * 72)
    tag = "PROVISIONAL (no benchmark passed)" if est["provisional"] else "from BENCHMARK"
    print(f"RUN-TIME ESTIMATE ({tag}):")
    print(f"   t_single (one full-config single-city fit) : "
          f"{est['t_single_s'] / 60:.1f} min")
    print(f"   monolithic 25y inscription                  : "
          f"{est['t_mono25_insc_s'] / 60:.1f} min")
    print(f"   monolithic 25y letter                       : "
          f"{est['t_mono25_letter_s'] / 60:.1f} min")
    print(f"   monolithic 50y (each, cheaper)              : "
          f"~{est['t_mono50_insc_s'] / 60:.1f} min")
    print(f"   4 fits concurrent (16 cores) wall           : "
          f"{est['mono_wall_concurrent_s'] / 60:.1f} min "
          f"(serial would be {est['mono_wall_serial_s'] / 60:.1f} min)")
    print(f"   subsample grid ({est['n_subsample_fits']} fits / "
          f"{est['subsample_parallel']}-way)             : "
          f"{est['subsample_wall_s'] / 3600:.1f} h")
    print(f"   TOTAL wall-clock (concurrent)               : "
          f"{est['total_wall_concurrent_h']:.1f} h")
    print("=" * 72)
    print("To LAUNCH the production run, re-run with --confirm-production.")
    print("(This dry run sampled nothing.)")


# --------------------------------------------------------------------------- #
# Production driver (gated).
# --------------------------------------------------------------------------- #

def run_production(out_base: Path, args) -> dict:
    """The full production run (gated behind --confirm-production)."""
    import preflight
    preflight.assert_ready()  # fail fast on a missing dep BEFORE the ~5.7 h run
    out_base.mkdir(parents=True, exist_ok=True)
    summary = {"steps": {}}

    # Step 1: monolithic fits.
    mono = run_monolithic_fits(
        out_base, args.draws, args.tune, args.chains, args.cores,
        args.target_accept, args.seed, escalate=not args.no_escalate,
        max_concurrent=args.mono_concurrent)
    summary["steps"]["monolithic"] = mono

    # Step 2: subsample-recover grid.
    import subsample_recover as sr
    cache25 = dp.default_cache_dir(25)
    donors = anchor_cities(cache25)
    sub = sr.run(
        cache25, donors, list(args.subsample_n_grid), args.subsample_reps,
        args.draws, args.tune, args.chains, args.subsample_cores,
        args.subsample_parallel, args.target_accept, args.seed,
        out_base / "subsample-recover-results.json",
        out_base / "subsample-recover.png")
    summary["steps"]["subsample_recover"] = sub["aggregate"]

    # Step 3: diagnostics on the primary (25y inscription) fit.
    primary = out_base / "monolithic-inscription-25y.nc"
    diag = {}
    if primary.exists():
        diag["clustering"] = trajectory_clustering(primary, "lam")
    # Internal consistency + Pompeii AD-79 are on the anchors' OWN standalone
    # fits (the anchors are not in the monolithic target-set fit).
    diag["anchor_internal_consistency"] = anchor_internal_consistency(
        cache25, args.draws, args.tune, args.chains, args.subsample_cores,
        args.target_accept, args.seed)
    diag["pompeii_ad79"] = pompeii_ad79_external(
        cache25, args.draws, args.tune, args.chains, args.subsample_cores,
        args.target_accept, args.seed)
    summary["steps"]["diagnostics"] = diag

    (out_base / "production-summary.json").write_text(
        json.dumps(summary, indent=2, default=float))
    print(f"\nProduction summary -> {out_base / 'production-summary.json'}")
    return summary


def run_diagnostics_only(out_base: Path, args) -> dict:
    """Re-run Step 3 diagnostics from saved outputs — Steps 1-2 are NOT re-fitted.

    Generalises the one-off ``finish_diagnostics.py`` (which recovered the
    2026-05-31 run after its post-sampling sklearn crash) into a first-class
    ``--resume-diagnostics`` path. Use it whenever the four monolithic ``.nc``
    posteriors + ``subsample-recover-results.json`` already exist in ``out_base``
    but Step 3 (clustering + anchor consistency + Pompeii) needs to be (re)run —
    e.g. after a Step-3 crash, or to recompute a diagnostic without paying the
    ~5.7 h of fitting again.

    The anchor / Pompeii checks DO re-fit those few standalone cities (~15-25
    min; the anchors are not in the monolithic target-set fit), but the 268-city
    monolithic fits and the ~1400-fit subsample grid are loaded from disk, never
    re-sampled. Writes ``production-summary.json`` (overwrites any existing one),
    matching ``run_production``'s structure with a provenance ``note``.
    """
    import preflight
    preflight.assert_ready()  # the anchor/Pompeii re-fits + clustering need deps
    import arviz as az
    import hier_model
    import letter_model

    if not out_base.exists():
        raise SystemExit(f"FATAL: --resume-diagnostics: {out_base} not found")

    # Unit -> module, for convergence_summary / gates_pass on each saved fit.
    mono_modules = {"inscription": hier_model, "letter": letter_model}
    summary = {"steps": {}, "note": (
        "Step 3 (re)run by orchestrate.py --resume-diagnostics; Steps 1-2 "
        "loaded from saved outputs, not re-fitted.")}

    # Step 1, reconstructed: load each .nc and recompute its convergence verdict.
    print("=== Step 1 (reconstructed from saved .nc) ===")
    mono = {}
    for c in MONO_CONFIGS:
        tag = f"{c['unit']}-{c['bin_width']}y"
        p = out_base / f"monolithic-{tag}.nc"
        if not p.exists():
            mono[tag] = {"error": f"missing {p.name}"}
            print(f"  {tag}: MISSING {p.name}")
            continue
        mod = mono_modules[c["unit"]]
        idata = az.from_netcdf(str(p))
        conv = mod.convergence_summary(idata)
        mono[tag] = {"convergence": conv, "gates_pass": bool(mod.gates_pass(conv)),
                     "save_path": str(p)}
        del idata  # bound memory: one 0.6-1.2 GB posterior at a time
        print(f"  {tag}: gates_pass={mono[tag]['gates_pass']} "
              f"rhat={conv['max_rhat']:.4f} ess={conv['min_ess_bulk']:.0f} "
              f"div={conv['n_divergences']}")
    summary["steps"]["monolithic"] = mono

    # Step 2, loaded: the existing subsample-recover aggregate.
    print("=== Step 2 (loaded subsample-recover results) ===")
    sub_path = out_base / "subsample-recover-results.json"
    if not sub_path.exists():
        raise SystemExit(f"FATAL: --resume-diagnostics: {sub_path} not found")
    sub = json.loads(sub_path.read_text())
    summary["steps"]["subsample_recover"] = sub["aggregate"]
    print(f"  calibration N* = {sub['aggregate'].get('calibration_n_star')}, "
          f"n_failures = {sub.get('n_failures')}")

    # Step 3, (re)run: clustering (loads the primary .nc) + the standalone
    # anchor / Pompeii re-fits. Identical calls to run_production's Step 3.
    print("=== Step 3 (clustering + anchor consistency + Pompeii) ===")
    cache25 = dp.default_cache_dir(25)
    diag = {}
    primary = out_base / "monolithic-inscription-25y.nc"
    if primary.exists():
        diag["clustering"] = trajectory_clustering(primary, "lam")
        print(f"  clustering sizes={diag['clustering'].get('sizes')}")
    diag["anchor_internal_consistency"] = anchor_internal_consistency(
        cache25, args.draws, args.tune, args.chains, args.subsample_cores,
        args.target_accept, args.seed)
    diag["pompeii_ad79"] = pompeii_ad79_external(
        cache25, args.draws, args.tune, args.chains, args.subsample_cores,
        args.target_accept, args.seed)
    summary["steps"]["diagnostics"] = diag

    (out_base / "production-summary.json").write_text(
        json.dumps(summary, indent=2, default=float))
    print(f"\nProduction summary -> {out_base / 'production-summary.json'}")
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--confirm-production", action="store_true",
                   help="REQUIRED to actually run. Without it, prints the plan "
                        "+ estimate and exits (dry run).")
    p.add_argument("--out-base", type=Path,
                   default=Path(__file__).resolve().parent / "production")
    p.add_argument("--check-env", action="store_true",
                   help="Run the preflight import + HDF5-backend check and exit "
                        "(no sampling). Use when provisioning a new host.")
    p.add_argument("--resume-diagnostics", action="store_true",
                   help="Skip Steps 1-2; (re)run Step 3 diagnostics from the "
                        "saved .nc + subsample JSON in --out-base. Re-fits only "
                        "the few anchor/Pompeii cities (~15-25 min), never the "
                        "268-city monolithic fits. Generalises "
                        "finish_diagnostics.py.")
    # Monolithic sampler config (production defaults: tune/draws 1000, 4 chains).
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--cores", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--mono-concurrent", type=int, default=4,
                   help="Monolithic fits to run at once (x cores chains).")
    p.add_argument("--no-escalate", action="store_true")
    # Subsample grid config.
    p.add_argument("--subsample-n-grid", nargs="+", type=int,
                   default=[50, 100, 200, 300, 500])
    p.add_argument("--subsample-reps", type=int, default=40)
    p.add_argument("--subsample-cores", type=int, default=2)
    p.add_argument("--subsample-parallel", type=int,
                   default=DEFAULT_SUBSAMPLE_PARALLEL)
    p.add_argument("--seed", type=int, default=2026)
    # Benchmark inputs for the dry-run estimate (seconds).
    p.add_argument(
        "--bench-json", type=Path,
        default=Path(__file__).resolve().parent / "benchmark-results.json",
        help="JSON of measured timings to populate the estimate (defaults to "
             "benchmark-results.json beside this script; falls back to "
             "provisional placeholders if absent).")
    args = p.parse_args()

    if args.check_env:
        import preflight
        return 0 if preflight.report() else 2

    bench = None
    if args.bench_json and args.bench_json.exists():
        # Absence is already guarded by ``.exists()``; guard MALFORMED content
        # too. A corrupt benchmark-results.json must fall back to provisional
        # placeholders (and flag the estimate provisional) rather than crash even
        # the dry run.
        try:
            bench = json.loads(args.bench_json.read_text())
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print(f"WARNING: could not parse {args.bench_json} ({exc}); "
                  "falling back to provisional placeholder estimate.",
                  file=sys.stderr)
            bench = None

    if args.resume_diagnostics:
        run_diagnostics_only(args.out_base, args)
        return 0

    if not args.confirm_production:
        print_plan(args.out_base, args, bench)
        return 0

    run_production(args.out_base, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
