#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark.py — §5 Layer-A production run-time BENCHMARK (reduced-cost timing).
==============================================================================

Estimate the production run-time WITHOUT running production. Three measurements,
each with REDUCED cost (short warmups / single fits), then a principled
extrapolation to the full ``tune 1000 / draws 1000`` configuration:

t_single
    One FULL-config (tune 1000 / draws 1000 / 4 chains / target_accept 0.99)
    single-city ``model.py`` fit on a representative target city (N~150;
    Lugdunum). This is the per-fit cost that drives the ~1,400-fit
    subsample-recover grid, so it is measured at full config (it is cheap).

t_mono (inscription 25y, letter 25y, and 50y note)
    Build the FULL 268-city monolithic model and run a REDUCED fit
    (``--mono-tune`` / ``--mono-draws``, e.g. 100/100). Separate the fixed model
    BUILD+COMPILE overhead from the per-iteration sampling cost so the
    extrapolation to 1000/1000 is:

        t_mono(tune, draws) ≈ build_compile_s
                             + (tune + draws) * per_iter_s

    where ``per_iter_s`` is estimated from the reduced run's sampling wall
    divided by its (tune + draws). Chains run in PARALLEL across cores, so the
    wall is the per-chain iteration cost, not summed over chains. The 50y model
    has half the bins (8 vs 16) and so fewer latent rates -> cheaper; we run a
    reduced 50y fit too and report the measured ratio rather than assuming 0.5x.

Extrapolation caveats (reported, not hidden):
    - NUTS tree depth can GROW with draws as the sampler explores; a short warmup
      may under- or over-estimate steady-state leapfrog cost. We mitigate by
      timing the SAMPLING phase (post-warmup) separately where possible and using
      it for ``per_iter_s``, and we flag the assumption.
    - target_accept=0.99 yields deeper trees (more leapfrog steps/iteration) than
      0.95; the reduced run uses the SAME target_accept=0.99, so per-iter cost is
      representative.

Output: ``benchmark-results.json`` (consumed by ``orchestrate.py --bench-json``)
and a console summary with the assembled production estimate + range.

Run (on zbook, threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/benchmark.py \
        --mono-tune 100 --mono-draws 100

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp          # noqa: E402
import model as sm             # noqa: E402
import hier_model as hm        # noqa: E402
import letter_model as lm      # noqa: E402


def time_single(out_dir: Path, city: str, draws: int, tune: int, chains: int,
                cores: int, target_accept: float, seed: int) -> dict:
    """Time one FULL-config single-city fit on a representative city."""
    bundle = dp.load_city(out_dir, city)
    A = np.asarray(bundle["A"], dtype=np.float64)
    t0 = time.perf_counter()
    idata = sm.fit(A, draws=draws, tune=tune, chains=chains, cores=cores,
                   target_accept=target_accept, random_seed=seed,
                   progressbar=False)
    wall = time.perf_counter() - t0
    conv = sm.convergence_summary(idata)
    return {
        "city": city, "N": int(A.shape[0]), "wall_s": wall,
        "draws": draws, "tune": tune, "chains": chains, "cores": cores,
        "max_rhat": conv["max_rhat"], "min_ess_bulk": conv["min_ess_bulk"],
        "n_divergences": conv["n_divergences"],
    }


def time_monolithic_with_compile_probe(unit: str, bin_width: int,
                                       mono_tune: int, mono_draws: int,
                                       chains: int, cores: int,
                                       target_accept: float, seed: int) -> dict:
    """Build the full 268-city monolithic model; isolate compile cost with a
    1+1 probe fit, time a reduced fit, and extrapolate to 1000/1000.

    Run a tiny ``tune=1, draws=1`` fit first to absorb the JIT/compile cost,
    then the reduced fit; the per-iteration cost is taken from the DIFFERENCE so
    the fixed compile overhead is removed from the extrapolation slope. This
    yields:  t(tune,draws) ≈ compile_s + (tune+draws)*per_iter_s.
    """
    import pymc as pm
    import pandas as pd

    cache = dp.default_cache_dir(bin_width)
    idx = pd.read_parquet(cache / "city-index.parquet")
    cities = idx[idx["bucket"] == "target"]["city"].tolist()

    t_assemble0 = time.perf_counter()
    if unit == "inscription":
        data = hm.assemble(cache, cities)
        model = hm.build_model(data, s_g=0.3, s_u=0.15, s_v=0.15)
        conv_fn = hm.convergence_summary
        n_insc = int(data.A_all.shape[0])
    else:
        data = lm.assemble(cache, cities)
        model = lm.build_model(data, obs_form="nb", s_g=0.3, s_u=0.15, s_v=0.15)
        conv_fn = lm.convergence_summary
        n_insc = None
    assemble_build_s = time.perf_counter() - t_assemble0

    # Probe fit: tune=1, draws=1 -> dominated by compile + fixed startup.
    n_probe = 2  # tune 1 + draws 1
    t_probe0 = time.perf_counter()
    with model:
        pm.sample(draws=1, tune=1, chains=chains, cores=cores,
                  target_accept=target_accept, random_seed=seed,
                  progressbar=False, compute_convergence_checks=False)
    probe_wall = time.perf_counter() - t_probe0

    # Reduced fit (compile is cached now, so its wall is ~compile_resid + iters).
    t_fit0 = time.perf_counter()
    with model:
        idata = pm.sample(draws=mono_draws, tune=mono_tune, chains=chains,
                         cores=cores, target_accept=target_accept,
                         random_seed=seed + 1, progressbar=False,
                         compute_convergence_checks=True)
    reduced_wall = time.perf_counter() - t_fit0
    conv = conv_fn(idata)

    # The probe and reduced are SEPARATE pm.sample calls, each re-spawning chain
    # workers (process start cost ~constant C). Model the two walls as:
    #   probe_wall   = C + n_probe   * per_iter
    #   reduced_wall = C + n_reduced * per_iter
    # Solve for per_iter (slope) and C (intercept) from the two points.
    n_reduced = mono_tune + mono_draws
    per_iter_s = (reduced_wall - probe_wall) / (n_reduced - n_probe)
    per_iter_s = max(per_iter_s, 1e-6)
    fixed_overhead_s = reduced_wall - n_reduced * per_iter_s

    def extrapolate(tune: int, draws: int) -> float:
        return fixed_overhead_s + (tune + draws) * per_iter_s

    return {
        "unit": unit, "bin_width": bin_width, "n_cities": len(cities),
        "n_total_inscriptions": n_insc,
        "assemble_build_s": assemble_build_s,
        "probe_wall_s": probe_wall, "reduced_tune": mono_tune,
        "reduced_draws": mono_draws, "reduced_fit_wall_s": reduced_wall,
        "per_iter_s": per_iter_s, "fixed_overhead_s": fixed_overhead_s,
        "extrapolated_1000_1000_s": extrapolate(1000, 1000),
        "max_rhat": conv["max_rhat"], "min_ess_bulk": conv["min_ess_bulk"],
        "n_divergences": conv["n_divergences"],
    }


def assemble_estimate(t_single: dict, monos: list[dict], subsample_parallel: int,
                      n_donors: int = 7, n_grid: int = 5, reps: int = 40) -> dict:
    """Assemble the production wall-clock estimate (per-component + range)."""
    by_key = {f"{m['unit']}-{m['bin_width']}y": m for m in monos}
    mono_walls = {k: m["extrapolated_1000_1000_s"] for k, m in by_key.items()}
    # 4 fits run concurrently across 16 cores (4 chains each): wall = slowest.
    mono_wall_concurrent = max(mono_walls.values())
    mono_wall_serial = sum(mono_walls.values())

    n_sub = n_donors * n_grid * reps
    t_single_s = t_single["wall_s"]
    # Subsample fits are standalone single-city; the grid spans N=50..500. The
    # benchmarked t_single is at N~150; small-N fits are a touch cheaper, large
    # ones a touch dearer, so t_single is a reasonable per-fit average. Range
    # uses ±30% to bracket the N-dependence + scheduler overhead.
    sub_wall_mid = n_sub * t_single_s / subsample_parallel
    sub_wall_lo = sub_wall_mid * 0.7
    sub_wall_hi = sub_wall_mid * 1.3

    total_mid = mono_wall_concurrent + sub_wall_mid
    total_lo = mono_wall_concurrent + sub_wall_lo
    total_hi = mono_wall_serial + sub_wall_hi  # pessimistic: monos serial too
    return {
        "mono_walls_s": mono_walls,
        "mono_wall_concurrent_s": mono_wall_concurrent,
        "mono_wall_serial_s": mono_wall_serial,
        "t_single_s": t_single_s,
        "n_subsample_fits": n_sub,
        "subsample_parallel": subsample_parallel,
        "subsample_wall_mid_s": sub_wall_mid,
        "subsample_wall_lo_s": sub_wall_lo,
        "subsample_wall_hi_s": sub_wall_hi,
        "total_wall_mid_h": total_mid / 3600,
        "total_wall_lo_h": total_lo / 3600,
        "total_wall_hi_h": total_hi / 3600,
    }


def run(out_dir25: Path, single_city: str, mono_tune: int, mono_draws: int,
        chains: int, cores: int, target_accept: float, seed: int,
        subsample_parallel: int, units: list[str], bin_widths: list[int],
        results_path: Path) -> dict:
    """Run all benchmark measurements and assemble the estimate."""
    print("=" * 72)
    print("BENCHMARK 1 — t_single (full-config single-city fit)")
    print("=" * 72)
    t_single = time_single(out_dir25, single_city, draws=1000, tune=1000,
                           chains=chains, cores=cores,
                           target_accept=target_accept, seed=seed)
    print(f"  {t_single['city']} (N={t_single['N']}): "
          f"{t_single['wall_s']:.1f}s wall  "
          f"(rhat {t_single['max_rhat']:.3f} ess {t_single['min_ess_bulk']:.0f} "
          f"div {t_single['n_divergences']})")

    print("\n" + "=" * 72)
    print(f"BENCHMARK 2 — t_mono (reduced tune={mono_tune}/draws={mono_draws}, "
          f"compile-probe extrapolation to 1000/1000)")
    print("=" * 72)
    monos = []
    for unit in units:
        for bw in bin_widths:
            print(f"\n  -> monolithic {unit}-{bw}y ...")
            m = time_monolithic_with_compile_probe(
                unit, bw, mono_tune, mono_draws, chains, cores,
                target_accept, seed)
            monos.append(m)
            print(f"     probe {m['probe_wall_s']:.0f}s, reduced "
                  f"({mono_tune}+{mono_draws}) {m['reduced_fit_wall_s']:.0f}s, "
                  f"per-iter {m['per_iter_s']:.3f}s, fixed "
                  f"{m['fixed_overhead_s']:.0f}s")
            print(f"     EXTRAPOLATED 1000/1000 = "
                  f"{m['extrapolated_1000_1000_s']:.0f}s "
                  f"({m['extrapolated_1000_1000_s'] / 60:.1f} min)  "
                  f"[reduced-run rhat {m['max_rhat']:.3f} "
                  f"ess {m['min_ess_bulk']:.0f} div {m['n_divergences']}]")

    est = assemble_estimate(t_single, monos, subsample_parallel)
    print("\n" + "=" * 72)
    print("ASSEMBLED PRODUCTION ESTIMATE")
    print("=" * 72)
    for k, v in est["mono_walls_s"].items():
        print(f"  monolithic {k:>16}: {v / 60:.1f} min")
    print(f"  4 monolithic fits concurrent (16 cores) : "
          f"{est['mono_wall_concurrent_s'] / 60:.1f} min "
          f"(serial {est['mono_wall_serial_s'] / 60:.1f} min)")
    print(f"  t_single (subsample fit, N~150)         : "
          f"{est['t_single_s']:.0f}s")
    print(f"  subsample grid ({est['n_subsample_fits']} fits, "
          f"{est['subsample_parallel']}-way parallel): "
          f"{est['subsample_wall_mid_s'] / 3600:.1f} h "
          f"(range {est['subsample_wall_lo_s'] / 3600:.1f}–"
          f"{est['subsample_wall_hi_s'] / 3600:.1f} h)")
    print(f"  TOTAL wall-clock: {est['total_wall_mid_h']:.1f} h  "
          f"(range {est['total_wall_lo_h']:.1f}–{est['total_wall_hi_h']:.1f} h)")
    print("=" * 72)

    out = {
        "t_single": t_single,
        "monolithic": monos,
        "estimate": est,
        # Fields consumed by orchestrate.py --bench-json:
        "t_single_s": t_single["wall_s"],
        "t_mono25_insc_s": next(
            (m["extrapolated_1000_1000_s"] for m in monos
             if m["unit"] == "inscription" and m["bin_width"] == 25), None),
        "t_mono50_insc_s": next(
            (m["extrapolated_1000_1000_s"] for m in monos
             if m["unit"] == "inscription" and m["bin_width"] == 50), None),
        "t_mono25_letter_s": next(
            (m["extrapolated_1000_1000_s"] for m in monos
             if m["unit"] == "letter" and m["bin_width"] == 25), None),
        "t_mono50_letter_s": next(
            (m["extrapolated_1000_1000_s"] for m in monos
             if m["unit"] == "letter" and m["bin_width"] == 50), None),
        "subsample_parallel": subsample_parallel,
    }
    results_path.write_text(json.dumps(out, indent=2, default=float))
    print(f"Results JSON -> {results_path}")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--single-city", default="Lugdunum")
    p.add_argument("--mono-tune", type=int, default=100)
    p.add_argument("--mono-draws", type=int, default=100)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--cores", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--subsample-parallel", type=int, default=4,
                   help="Concurrent subsample workers assumed for the estimate.")
    p.add_argument("--units", nargs="+", default=["inscription", "letter"])
    p.add_argument("--bin-widths", nargs="+", type=int, default=[25, 50])
    p.add_argument("--out-dir", type=Path, default=dp.default_cache_dir(25))
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "benchmark-results.json")
    args = p.parse_args()
    run(args.out_dir, args.single_city, args.mono_tune, args.mono_draws,
        args.chains, args.cores, args.target_accept, args.seed,
        args.subsample_parallel, args.units, args.bin_widths, args.results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
