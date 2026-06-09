#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aggregate_joint_grid.py — grid verdict + bias map for the joint recovery grid.
==============================================================================

Reads every `outputs/grid/<cell_id>.json` written by `run_joint_grid.py` and scores the
acceptance criteria (`full-grid-spec.md` §3): do-no-harm on identifiable cells (C1),
pulled-to-truth on confounded cells (C2 — incl. *materially better than the shared-basis
baseline*), coverage, convergence (C4). Emits `outputs/grid-VERDICT.md` and
`outputs/grid-summary.json` (per-cell table + the bias surface over %win × α_true).

Robustness (post-audit 2026-06-09): fully-failed cells (`n_ok == 0`) are **reported**, not
silently dropped; the "worst positive bias" statistic is guarded; C2 scores all three
spec conjuncts (the baseline data is recorded per confounded cell by the runner). Cell
aggregates are over the **converged** replicates (the runner's `agg_over` field).

Run — PATH=~/.local/bin:$PATH uv run python code/aggregate_joint_grid.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
GRID_DIR = RUN / "outputs" / "grid"

BETTER_MARGIN = 0.05   # "materially better than baseline" margin (|lead| + margin < |baseline|)


def main() -> None:
    all_cells = [json.loads(p.read_text()) for p in sorted(GRID_DIR.glob("*.json"))]
    if not all_cells:
        print("no completed cells yet.")
        return
    # Separate scorable cells from fully-failed ones (reported, not dropped).
    scored = [c for c in all_cells if c.get("n_ok", 0) > 0 and c.get("bias_median") is not None]
    failed = [c for c in all_cells if c.get("n_ok", 0) == 0]

    ident = [c for c in scored if c["regime"] == "identifiable"]
    conf = [c for c in scored if c["regime"] == "confounded"]

    lines = ["# Joint recovery grid — VERDICT", "",
             f"Cells with usable data: {len(scored)} "
             f"({len(ident)} identifiable, {len(conf)} confounded). "
             f"Fully-failed cells (n_ok=0): **{len(failed)}**"
             + (f" — {[c['cell_id'] for c in failed]}" if failed else "") + ".",
             ""]

    # C1 — do-no-harm (identifiable): |median bias| < 0.12 AND coverage >= 0.90.
    if ident:
        b = np.abs([c["bias_median"] for c in ident])
        cov = np.array([c["coverage_rate"] for c in ident])
        c1 = int(np.sum((b < 0.12) & (cov >= 0.90)))
        lines += ["## C1 — do-no-harm (identifiable)",
                  f"- passing (|median bias|<0.12 AND coverage>=0.90): **{c1}/{len(ident)}** "
                  f"({100*c1/len(ident):.0f}%)",
                  f"- mean |median bias| {b.mean():.3f}; mean coverage {cov.mean():.3f}", ""]

    # C2 — pulled-to-truth (confounded): |median bias|<0.18 AND median bias<=+0.12
    #      AND materially better than the shared-basis baseline.
    if conf:
        bm = np.array([c["bias_median"] for c in conf])
        cov = np.array([c["coverage_rate"] for c in conf])
        base = np.array([c.get("baseline_abs_bias_median") if c.get("baseline_abs_bias_median")
                         is not None else np.nan for c in conf])
        lead_abs = np.abs(bm)
        better = (lead_abs + BETTER_MARGIN) < base          # NaN → False (baseline missing)
        has_base = ~np.isnan(base)
        passing = (lead_abs < 0.18) & (bm <= 0.12) & better
        c2 = int(np.sum(passing))
        lines += ["## C2 — pulled-to-truth (confounded)",
                  f"- passing (|median bias|<0.18 AND bias<=+0.12 AND >baseline by {BETTER_MARGIN}): "
                  f"**{c2}/{len(conf)}** ({100*c2/len(conf):.0f}%)",
                  f"- mean median bias {bm.mean():+.3f}; mean coverage {cov.mean():.3f}",
                  f"- worst positive median bias {max(float(bm.max()), 0.0):+.3f}",
                  f"- cells with baseline recorded: {int(has_base.sum())}/{len(conf)}; "
                  f"mean lead |bias| {lead_abs.mean():.3f} vs mean baseline |bias| "
                  f"{np.nanmean(base):.3f}", ""]

    # C4 — convergence (per-cell convergence_rate >= 0.95).
    conv = np.array([c["convergence_rate"] for c in scored if c.get("convergence_rate") is not None])
    if conv.size:
        lines += ["## C4 — convergence",
                  f"- cells with convergence_rate>=0.95: **{int(np.sum(conv>=0.95))}/{conv.size}** "
                  f"({100*np.mean(conv>=0.95):.0f}%); mean rate {conv.mean():.3f}", ""]

    # Bias surface over %win × α_true (mean median-bias of the LEAD).
    lines += ["## Bias surface — mean(median bias) by %win × α_true", ""]
    wins = sorted({c["conv_pct_win"] for c in scored})
    alphas = sorted({c["alpha_true"] for c in scored})
    lines += ["| %win \\ α | " + " | ".join(f"{a:.1f}" for a in alphas) + " |",
              "|" + "---|" * (len(alphas) + 1)]
    for w in wins:
        row = [f"| {w:.2f} "]
        for a in alphas:
            sub = [c for c in scored if c["conv_pct_win"] == w and c["alpha_true"] == a]
            row.append(f"| {np.mean([c['bias_median'] for c in sub]):+.2f} " if sub else "| · ")
        lines.append("".join(row) + "|")
    lines += [""]

    # Overall.
    rep_fails = sum(c.get("n_failed", 0) for c in all_cells)
    lines += ["## Overall",
              f"- replicate failures across grid: {rep_fails} "
              f"(in {len([c for c in all_cells if c.get('n_failed',0)])} cells)",
              f"- fully-failed cells: {len(failed)}",
              f"- grid scope: %win {wins}, α {alphas}, "
              f"N {sorted({c['N'] for c in scored})}", ""]

    (RUN / "outputs" / "grid-VERDICT.md").write_text("\n".join(lines))
    (RUN / "outputs" / "grid-summary.json").write_text(json.dumps(
        {"n_cells_total": len(all_cells), "n_scored": len(scored), "n_failed": len(failed),
         "cells": [{k: c.get(k) for k in ("cell_id", "regime", "conv_pct_win", "alpha_true",
                                          "gen_name", "N", "bias_median", "coverage_rate",
                                          "convergence_rate", "baseline_bias_median",
                                          "n_ok", "n_converged", "n_failed")}
                   for c in all_cells]}, indent=1))
    print("\n".join(lines))
    print("\nWrote grid-VERDICT.md + grid-summary.json")


if __name__ == "__main__":
    main()
