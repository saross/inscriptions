#!/usr/bin/env python3
"""
probe2.py --- Refined wall-time probe.

Runs CPL province cells with two n_mc values to disentangle the
fixed-cost-per-iteration (CPL fit, which is independent of n_mc) from
the MC-loop cost (linear in n_mc). This lets us extrapolate to the
production n_mc=1000 with confidence.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from h1_sim import CellSpec, run_cell  # noqa: E402
from primitives import load_filtered_lire  # noqa: E402


def time_cell(spec, df, label):
    ss = np.random.SeedSequence(20260425).spawn(1)[0]
    t0 = time.perf_counter()
    recs = run_cell(spec, df, ss)
    elapsed = time.perf_counter() - t0
    per_iter = elapsed / spec.n_iterations
    print(f"  {label}: total={elapsed:.2f}s, per_iter={per_iter*1000:.1f}ms, "
          f"{len(recs)} records", flush=True)
    return per_iter


def main():
    print("Loading filtered LIRE...", flush=True)
    df = load_filtered_lire("archive/data-2026-04-22/LIRE_v3-0.parquet")

    # CPL province n=2500: vary n_mc to disentangle.
    n_iter = 30
    print("\n--- CPL n=2500 ---", flush=True)
    t_mc100 = time_cell(
        CellSpec("p_cpl_mc100", "province", "c_20pc_25y", "gaussian",
                 2_500, "cpl", n_iter, 100),
        df, "n_mc=100")
    t_mc500 = time_cell(
        CellSpec("p_cpl_mc500", "province", "c_20pc_25y", "gaussian",
                 2_500, "cpl", n_iter, 500),
        df, "n_mc=500")

    # Linear extrapolation: t(mc) = a + b*mc.
    # t_mc100 = a + b*100; t_mc500 = a + b*500.
    # b = (t_mc500 - t_mc100) / 400; a = t_mc100 - 100*b.
    b = (t_mc500 - t_mc100) / 400.0
    a = t_mc100 - 100.0 * b
    print(f"\nFixed cost per iter (CPL fit): {a*1000:.1f}ms", flush=True)
    print(f"MC cost per replicate: {b*1000:.3f}ms", flush=True)
    t_mc1000_cpl = a + 1000.0 * b
    print(f"Extrapolated CPL n=2500 @ mc=1000: {t_mc1000_cpl*1000:.1f}ms/iter",
          flush=True)
    print(f"  CPL cell @ 1000 iters: {t_mc1000_cpl*1000:.1f}s", flush=True)

    # Now exp province n=2500.
    print("\n--- Exp n=2500 ---", flush=True)
    t_exp_mc100 = time_cell(
        CellSpec("p_exp_mc100", "province", "c_20pc_25y", "gaussian",
                 2_500, "exponential", n_iter, 100),
        df, "n_mc=100")
    t_exp_mc500 = time_cell(
        CellSpec("p_exp_mc500", "province", "c_20pc_25y", "gaussian",
                 2_500, "exponential", n_iter, 500),
        df, "n_mc=500")
    b_exp = (t_exp_mc500 - t_exp_mc100) / 400.0
    a_exp = t_exp_mc100 - 100.0 * b_exp
    t_mc1000_exp = a_exp + 1000.0 * b_exp
    print(f"\nFixed cost (exp fit): {a_exp*1000:.1f}ms", flush=True)
    print(f"MC cost: {b_exp*1000:.3f}ms", flush=True)
    print(f"Extrapolated Exp n=2500 @ mc=1000: {t_mc1000_exp*1000:.1f}ms/iter",
          flush=True)
    print(f"  Exp cell @ 1000 iters: {t_mc1000_exp*1000:.1f}s", flush=True)

    # Empire n=50000 exp (one cell).
    print("\n--- Exp empire n=50000 ---", flush=True)
    t_emp_mc100 = time_cell(
        CellSpec("p_emp_mc100", "empire", "c_20pc_25y", "gaussian",
                 50_000, "exponential", n_iter, 100),
        df, "n_mc=100")
    t_emp_mc500 = time_cell(
        CellSpec("p_emp_mc500", "empire", "c_20pc_25y", "gaussian",
                 50_000, "exponential", n_iter, 500),
        df, "n_mc=500")
    b_emp = (t_emp_mc500 - t_emp_mc100) / 400.0
    a_emp = t_emp_mc100 - 100.0 * b_emp
    t_mc1000_emp = a_emp + 1000.0 * b_emp
    print(f"\nExp empire @ mc=1000: {t_mc1000_emp*1000:.1f}ms/iter, "
          f"{t_mc1000_emp*1000:.1f}s/cell", flush=True)

    # Full grid total: 16 empire (8 exp + 8 cpl), 64 prov (32 + 32),
    # 56 urban (28 + 28). Conservatively use province numbers for prov+urban
    # (urban is smaller-n and likely cheaper).
    n_emp_exp = 8
    n_emp_cpl = 8
    n_prov_exp = 32
    n_prov_cpl = 32
    n_urb_exp = 28
    n_urb_cpl = 28

    serial_emp_exp = n_emp_exp * t_mc1000_emp * 1000  # 1000 iters
    # Empire CPL likely ~3-5x exp cost (3 k values × CPL fit). Pessimistic 5x.
    serial_emp_cpl = n_emp_cpl * t_mc1000_emp * 5.0 * 1000
    serial_prov_exp = n_prov_exp * t_mc1000_exp * 1000
    serial_prov_cpl = n_prov_cpl * t_mc1000_cpl * 1000
    serial_urb_exp = n_urb_exp * t_mc1000_exp * 1000
    serial_urb_cpl = n_urb_cpl * t_mc1000_cpl * 1000
    serial_total = (serial_emp_exp + serial_emp_cpl + serial_prov_exp +
                    serial_prov_cpl + serial_urb_exp + serial_urb_cpl)
    print(f"\nSerial estimate: {serial_total/60:.1f} min", flush=True)
    print(f"  emp_exp: {serial_emp_exp/60:.1f} min", flush=True)
    print(f"  emp_cpl: {serial_emp_cpl/60:.1f} min", flush=True)
    print(f"  prov_exp: {serial_prov_exp/60:.1f} min", flush=True)
    print(f"  prov_cpl: {serial_prov_cpl/60:.1f} min", flush=True)
    print(f"  urb_exp: {serial_urb_exp/60:.1f} min", flush=True)
    print(f"  urb_cpl: {serial_urb_cpl/60:.1f} min", flush=True)

    n_cores = 24
    overhead = 1.3
    parallel = (serial_total / n_cores) * overhead
    print(f"\nParallel ({n_cores} cores, {overhead}x): {parallel/60:.1f} min",
          flush=True)
    print(f"Worst case (3x): {3*parallel/60:.1f} min", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
