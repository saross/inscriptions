#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make-reachability-report.py
===========================

Post-process the small-N reachability run (``reachability.py``) into the
paper-facing artefacts: a reachability-map figure (per-shape α × N heatmaps of
shape-recovery rate, with the pass/fail boundary marked) and a REPORT.md that
states the floor per (shape, α), the headline floor, and the α-bias / band-
coverage trends with N.

Kept separate from the fitting driver so it can be re-run cheaply against the
stored ``reachability-by-cell.csv`` (the driver writes that + the per-replicate
parquet at completion). Reads the CSV; writes figure + REPORT; no fitting.

Usage
-----
    python make-reachability-report.py --output-dir <outputs/>

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-03, on Shawn's brief.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ENVELOPE_ALPHA = 0.70  # operating-envelope ceiling (Decision 33)


def _pivot(df: pd.DataFrame, shape: str, value: str) -> pd.DataFrame:
    """α (rows, ascending) × N (cols, ascending) pivot for one shape."""
    sub = df[df.shape_name == shape]
    return sub.pivot_table(index="alpha_true", columns="n", values=value).sort_index()


def make_figure(df: pd.DataFrame, out_path: Path) -> None:
    """Per-shape α × N heatmaps of shape-recovery rate; ✓ marks passing cells."""
    shapes = list(df.shape_name.unique())
    fig, axes = plt.subplots(1, len(shapes), figsize=(6 * len(shapes), 4.5),
                             squeeze=False)
    for ax, shape in zip(axes[0], shapes):
        rate = _pivot(df, shape, "shape_rate")
        passes = _pivot(df, shape, "cell_pass")
        im = ax.imshow(rate.values, vmin=0, vmax=1, cmap="RdYlGn", aspect="auto",
                       origin="lower")
        ax.set_xticks(range(len(rate.columns)))
        ax.set_xticklabels(rate.columns, rotation=45, ha="right")
        ax.set_yticks(range(len(rate.index)))
        ax.set_yticklabels([f"{a:.2f}" for a in rate.index])
        ax.set_xlabel("N (subset size)")
        ax.set_ylabel("α (convention fraction)")
        ax.set_title(f"{shape}")
        for i in range(rate.shape[0]):
            for j in range(rate.shape[1]):
                v = rate.values[i, j]
                p = bool(passes.values[i, j]) if not np.isnan(passes.values[i, j]) else False
                txt = ("✓ " if p else "") + ("·" if np.isnan(v) else f"{v:.0%}")
                ax.text(j, i, txt, ha="center", va="center", fontsize=8,
                        color="black")
    fig.colorbar(im, ax=axes[0].tolist(), fraction=0.02, pad=0.02,
                 label="shape-recovery rate (Pearson r ≥ 0.95)")
    fig.suptitle("Subset-specific deconvolution reachability — shape recovery by "
                 "subset size N and convention fraction α (✓ = cell passes the "
                 "Decision-33 criterion)", fontsize=10)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_report(df: pd.DataFrame) -> str:
    """Render REPORT.md: floor table, headline, and N-trends."""
    L: list[str] = []
    L.append("# Small-N deconvolution-reachability — REPORT")
    L.append("")
    L.append("Minimum subset size N at which **subset-specific** Bayesian "
             "deconvolution recovers the genuine SPA under the Decision-33 "
             "criterion (convergence ≥ 90 % AND Pearson r ≥ 0.95 in ≥ 90 % of "
             "replicates). See `spec.md` and Decision 34.")
    L.append("")

    # Floor table.
    L.append("## 1. Reachability floor (smallest passing N)")
    L.append("")
    L.append("| shape | α | floor (min passing N) |")
    L.append("|---|---|---|")
    floors = {}
    for (sh, al), g in df.groupby(["shape_name", "alpha_true"]):
        passing = sorted(int(n) for n in g[g.cell_pass]["n"])
        floor = passing[0] if passing else None
        floors[(sh, al)] = floor
        L.append(f"| {sh} | {al:.2f} | "
                 f"{('N ≥ ' + str(floor)) if floor else 'UNREACHED in tested range'} |")
    L.append("")

    # Headline within the operating envelope (α ≤ 0.70).
    env_floors = [f for (sh, al), f in floors.items()
                  if al <= ENVELOPE_ALPHA and f is not None]
    unreached_env = [(sh, al) for (sh, al), f in floors.items()
                     if al <= ENVELOPE_ALPHA and f is None]
    L.append("## 2. Headline")
    L.append("")
    if env_floors:
        worst = max(env_floors)
        L.append(f"- Within the operating envelope (α ≤ {ENVELOPE_ALPHA:.2f}), "
                 f"subset-specific de-fogging is reliable for **N ≥ {worst}** "
                 f"across the tested shapes (the worst-case floor).")
    if unreached_env:
        L.append(f"- Unreached even at the largest tested N within the envelope: "
                 f"{unreached_env} — these need a larger N or the pooled-"
                 f"convention fall-back.")
    L.append(f"- The high-α stress row (α = 0.85, late-corpus regime) is reported "
             f"separately; its floors are expected higher / unreached.")
    L.append("")

    # Trends with N.
    L.append("## 3. Diagnostics by N (α ≤ 0.70 cells)")
    L.append("")
    env = df[df.alpha_true <= ENVELOPE_ALPHA]
    by_n = env.groupby("n").agg(shape_rate=("shape_rate", "mean"),
                                conv_rate=("conv_rate", "mean"),
                                band_cov95=("band_cov95", "mean"),
                                mean_abs_alpha_bias=("mean_abs_alpha_bias", "mean"))
    L.append("| N | mean shape-rate | mean conv-rate | mean band cov95 | mean |α-bias| |")
    L.append("|---|---|---|---|---|")
    for n, r in by_n.iterrows():
        L.append(f"| {int(n)} | {r.shape_rate:.0%} | {r.conv_rate:.0%} "
                 f"| {r.band_cov95:.2f} | {r.mean_abs_alpha_bias:.3f} |")
    L.append("")
    L.append("Band coverage (target 0.95) and α-bias are diagnostics, not gates; "
             "they show how recovery quality scales with N.")
    L.append("")

    L.append("## 4. Caveats")
    L.append("")
    L.append("- Convention pattern = `pilot_proxy` (the realistic descriptive "
             "proxy); a `uniform` robustness pass is optional.")
    L.append("- Fits run under zbook's pymc 6.x; the grid used pymc 5.28 (model "
             "identical — a calibration property, transfers).")
    L.append("- Below the floor: pooled-convention borrow / §5 hierarchical model "
             "/ descriptive reporting (Decision 34; out of scope here).")
    L.append("")
    return "\n".join(L)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Reachability figure + REPORT.")
    p.add_argument("--output-dir", required=True, type=Path)
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    csv = args.output_dir / "reachability-by-cell.csv"
    if not csv.exists():
        raise FileNotFoundError(f"No {csv}; run reachability.py first.")
    df = pd.read_csv(csv)
    # Guard: cell_pass may load as bool or str depending on writer.
    if df["cell_pass"].dtype == object:
        df["cell_pass"] = df["cell_pass"].astype(str).str.lower().eq("true")

    make_figure(df, args.output_dir / "figures" / "reachability-map.png")
    report = make_report(df)
    (args.output_dir / "REPORT.md").write_text(report, encoding="utf-8")
    print(f"[report] wrote {args.output_dir/'figures'/'reachability-map.png'}")
    print(f"[report] wrote {args.output_dir/'REPORT.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
