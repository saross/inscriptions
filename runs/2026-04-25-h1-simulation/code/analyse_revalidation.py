#!/usr/bin/env python3
"""
analyse_revalidation.py --- Compare optimised-fit FP rates vs Stage 3 PASS.

Reads the post-optimisation re-validation parquet and emits a summary
that can be checked against ``forward-fit-pilot/SUMMARY-CPL.md``. The
gate criterion: Part A.cpl synthetic-data zero-bracket FP rate must
fall within the Stage 3 PASS envelope (mean 0.034, max 0.070, all
cells <= 0.10) within Monte Carlo noise (n_iter = 100, Wilson 95 % CI
on 0.05 extends to ~0.107).

Run on sapphire:
    .venv/bin/python3 runs/2026-04-25-h1-simulation/code/analyse_revalidation.py \
        --in runs/2026-04-25-h1-simulation/outputs/optimisation/revalidation
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--in", dest="in_dir", required=True, type=Path,
        help="Revalidation output directory.",
    )
    args = parser.parse_args()

    df = pd.read_parquet(args.in_dir / "results.parquet")
    print(f"Total rows: {len(df)}")
    print()

    # Part A.cpl synthetic, zero bracket -- the gate criterion
    sub = df[(df["part"] == "A.cpl") & (df["bracket"] == "zero")]
    agg = sub.groupby(["cpl_truth", "n"])["detected"].mean().reset_index()
    agg.columns = ["cpl_truth", "n", "FP_rate"]
    print("=== Part A.cpl synthetic, zero bracket (FP gate) ===")
    print(agg.to_string(index=False))
    print()
    print(f"FP range: [{agg['FP_rate'].min():.3f}, "
          f"{agg['FP_rate'].max():.3f}]; mean {agg['FP_rate'].mean():.3f}")
    print(f"Cells > 0.05: {(agg['FP_rate'] > 0.05).sum()} / {len(agg)}")
    print(f"Cells > 0.10: {(agg['FP_rate'] > 0.10).sum()} / {len(agg)}")
    print()

    # Part A.cpl detection on binding bracket
    print("=== Part A.cpl detection on a_50pc_50y at n>=2500 (gate) ===")
    det = df[(df["part"] == "A.cpl") & (df["bracket"] == "a_50pc_50y")
             & (df["n"] >= 2500)]
    agg2 = det.groupby(["cpl_truth", "n"])["detected"].mean().reset_index()
    agg2.columns = ["cpl_truth", "n", "detection_rate"]
    print(agg2.to_string(index=False))
    print(f"\nMin detection at n>=2500: {agg2['detection_rate'].min():.3f}")
    print()

    # Part A exp synthetic
    print("=== Part A exp synthetic, zero bracket (exp FP) ===")
    expsub = df[(df["part"] == "A") & (df["bracket"] == "zero")]
    agg_exp = expsub.groupby(["b_null", "n"])["detected"].mean().reset_index()
    agg_exp.columns = ["b_null", "n", "FP_rate"]
    print(agg_exp.to_string(index=False))
    print(f"\nFP range: [{agg_exp['FP_rate'].min():.3f}, "
          f"{agg_exp['FP_rate'].max():.3f}]; "
          f"mean {agg_exp['FP_rate'].mean():.3f}")
    print()

    # Part C real-LIRE diagnostic
    print("=== Part C real-LIRE bootstrap CPL FP (diagnostic) ===")
    subc = df[df["part"] == "C"]
    if len(subc) > 0:
        aggc = subc.groupby(["n"])["detected"].mean().reset_index()
        aggc.columns = ["n", "FP_rate"]
        print(aggc.to_string(index=False))
    print()

    # Wall-time
    summary_path = args.in_dir / "summary-extended.json"
    if summary_path.exists():
        with summary_path.open() as f:
            summary = json.load(f)
        print(f"Wall-time: {summary['elapsed_seconds']:.1f}s "
              f"= {summary['elapsed_seconds'] / 60:.1f}m")

    # Gate check
    print("\n=== Gate check ===")
    cpl_zero_max = float(agg["FP_rate"].max())
    cpl_zero_mean = float(agg["FP_rate"].mean())
    pass_fp_envelope = cpl_zero_mean <= 0.054 and cpl_zero_max <= 0.10
    pass_detection = float(agg2["detection_rate"].min()) >= 0.95
    print(f"CPL FP mean {cpl_zero_mean:.3f} "
          f"(target <= 0.054 = 0.034 + 0.02): "
          f"{'PASS' if cpl_zero_mean <= 0.054 else 'FAIL'}")
    print(f"CPL FP max  {cpl_zero_max:.3f} (target <= 0.10): "
          f"{'PASS' if cpl_zero_max <= 0.10 else 'FAIL'}")
    print(f"Min binding-bracket detection at n>=2500 "
          f"{float(agg2['detection_rate'].min()):.3f} "
          f"(target >= 0.95): "
          f"{'PASS' if pass_detection else 'FAIL'}")
    print(f"\nOverall verdict: "
          f"{'PASS' if pass_fp_envelope and pass_detection else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
