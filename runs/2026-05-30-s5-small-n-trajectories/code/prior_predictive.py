#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prior_predictive.py — §5 Layer-A hyperprior pinning via prior-predictive check.
===============================================================================

Pin the HalfNormal scales on (sigma_g, sigma_u, sigma_v) by sampling trajectory
ensembles FROM THE PRIOR ALONE (no data, no likelihood, no fitting — so the
priors are set without peeking at any result). For each candidate scale tuple we
draw the hyperparameters and the non-centred RW1 innovations, form the implied
log-rate trajectories exactly as ``hier_model.py`` does, and summarise whether
the ensemble looks like *plausible epigraphic histories*:

- Trajectories should rise/fall over centuries, NOT jump wildly bin-to-bin.
- A sensible global band allows up to ~1-1.5 log-units (~3-4.5x) of SMOOTH
  multi-bin variation but penalises jagged +/- large swings between adjacent
  25-year bins.
- Province / city deviations should be MODEST relative to the global trajectory
  (so we want sigma_u, sigma_v < sigma_g).

Two ensembles are summarised per scale:

1. **Global shape** ``g_shape`` (zero-sum cumsum walk * sigma_g). Diagnostics:
   - ``adj_jump``     : max |g[t] - g[t-1]| over t (adjacent-bin log-jump).
   - ``ptr``          : peak-to-trough ratio exp(max g - min g) (multiplicative
                        spread of the global trajectory across the 4 centuries).

2. **Province / city deviation** ``u_shape`` / ``v_shape`` (same form, scale
   sigma_u / sigma_v). Diagnostic:
   - ``dev_range``    : exp(max - min) of the deviation (multiplicative spread a
                        province/city can sit away from its parent).

The grid is small (spec suggestion: sigma_g in {0.3,0.5,0.7},
sigma_u, sigma_v in {0.2,0.3,0.5}). We pick scales whose ensemble has:
  - global adj-jump mostly < ~0.5 log-units (smooth, not jagged),
  - global peak-to-trough median around ~2-4x (real epigraphic centuries do rise
    and fall by a few-fold), 95th pct not exploding past ~6-8x,
  - province/city deviation spread modest (median multiplicative range < ~2x).

We SAVE a prior-predictive overlay PNG (sampled global trajectories + a
deviation panel) for Shawn's sanity check and RECOMMEND specific scales.

Run (on zbook, in the venv, with threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/prior_predictive.py \
        --n-draws 4000

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np

T = 16  # bins, must match dataprep.N_BINS / hier_model.T_BINS


# --------------------------------------------------------------------------- #
# Prior sampling of one tier (the exact non-centred zero-sum RW1 form).
# --------------------------------------------------------------------------- #

def sample_tier_shapes(scale_sd: float, n_draws: int,
                       rng: np.random.Generator) -> np.ndarray:
    """Draw ``n_draws`` zero-sum RW1 *shape* trajectories for one tier.

    Reproduces ``hier_model.py``'s tier construction exactly:
      sigma  ~ HalfNormal(scale_sd)
      z      ~ Normal(0, 1, T)
      walk   = cumsum(z) * sigma
      shape  = walk - mean(walk)          # zero-sum over time

    Args:
        scale_sd: HalfNormal scale on the RW1 innovation SD (the knob).
        n_draws: Number of prior trajectories to draw.
        rng: NumPy random generator.

    Returns:
        ``(n_draws, T)`` array of zero-sum log-rate shape trajectories.
    """
    # HalfNormal(scale_sd) == |Normal(0, scale_sd)|.
    sigma = np.abs(rng.normal(0.0, scale_sd, size=(n_draws, 1)))
    z = rng.normal(0.0, 1.0, size=(n_draws, T))
    walk = np.cumsum(z, axis=1) * sigma
    return walk - walk.mean(axis=1, keepdims=True)


def summarise_shapes(shapes: np.ndarray) -> dict:
    """Ensemble diagnostics for a set of zero-sum shape trajectories.

    Args:
        shapes: ``(n_draws, T)`` zero-sum log-rate trajectories.

    Returns:
        Dict of distributional summaries of adjacent-bin log-jump and
        peak-to-trough ratio.
    """
    adj = np.abs(np.diff(shapes, axis=1))             # (n, T-1)
    max_adj = adj.max(axis=1)                          # worst jump per draw
    span = shapes.max(axis=1) - shapes.min(axis=1)     # log peak-to-trough
    ptr = np.exp(span)                                 # multiplicative spread

    def pct(a, q):
        return float(np.percentile(a, q))

    return {
        "adj_jump_median": float(np.median(max_adj)),
        "adj_jump_p90": pct(max_adj, 90),
        "adj_jump_p99": pct(max_adj, 99),
        "ptr_median": float(np.median(ptr)),
        "ptr_p90": pct(ptr, 90),
        "ptr_p99": pct(ptr, 99),
        "span_log_median": float(np.median(span)),
        "span_log_p75": pct(span, 75),
        "span_log_p90": pct(span, 90),
        # Fraction of draws inside the brief's "smooth, <= 1.5 log-unit" band.
        "frac_span_lt_1p5lu": float(np.mean(span < 1.5)),
        "frac_adj_lt_0p5lu": float(np.mean(max_adj < 0.5)),
    }


# --------------------------------------------------------------------------- #
# Grid search over candidate scales.
# --------------------------------------------------------------------------- #

def run_grid(s_g_grid, s_u_grid, s_v_grid, n_draws, seed):
    """Summarise the prior ensemble for every scale on the grid.

    Global scales are scored on their own; deviation scales (u, v) share the
    same single-tier diagnostic (both are zero-sum RW1 shapes), so we score the
    UNION of u and v candidate scales once and reuse.

    Returns:
        ``(global_rows, dev_rows)``: lists of per-scale diagnostic dicts.
    """
    rng = np.random.default_rng(seed)

    global_rows = []
    for s_g in s_g_grid:
        shapes = sample_tier_shapes(s_g, n_draws, rng)
        row = {"scale": s_g, "tier": "global"}
        row.update(summarise_shapes(shapes))
        global_rows.append(row)

    dev_rows = []
    for s in sorted(set(list(s_u_grid) + list(s_v_grid))):
        shapes = sample_tier_shapes(s, n_draws, rng)
        row = {"scale": s, "tier": "deviation"}
        row.update(summarise_shapes(shapes))
        dev_rows.append(row)

    return global_rows, dev_rows


def recommend(global_rows, dev_rows):
    """Pick scales by the plausibility criteria; return the recommendation dict.

    The criteria translate the brief's plausibility band ("up to ~1-1.5
    log-units of SMOOTH multi-bin variation; penalise jagged adjacent swings;
    deviations modest relative to the global trajectory") into concrete cuts on
    the prior ensemble.

    Global criterion: the TYPICAL trajectory should rise/fall by ~1 log-unit
    (median peak-to-trough log-span ~0.8-1.2, i.e. ~2.5-3.5x) and stay smooth
    (median max adjacent-bin jump < 0.5 log-units), with the bulk (>= ~65% of
    draws) inside the 1.5-log-unit band. Among scales meeting smoothness, pick
    the LARGEST whose median log-span is still <= ~1.0 — that admits genuine
    multi-bin variation without the median trajectory exceeding the 1.5-log-unit
    ceiling. (The cumsum-RW1 has a heavy ENDPOINT tail by construction, so we
    judge on the median/p75 of the span, not the extreme ptr p99.)

    Deviation criterion: genuinely MODEST and strictly sub-global — median
    multiplicative spread < ~1.7x, p90 < ~4x, and scale < the chosen global
    scale, so province/city deviations sit well inside the global trajectory's
    envelope (the property that lets shrinkage tighten small-N cities).
    """
    # Global: smooth (adj-jump median < 0.5), bulk inside 1.5 log-units, and
    # median span <= ~1.0 log-unit; among those, take the largest scale.
    g_ok = [r for r in global_rows
            if r["adj_jump_median"] < 0.5
            and r["span_log_median"] <= 1.0
            and r["frac_span_lt_1p5lu"] >= 0.65]
    g_pick = max(g_ok, key=lambda r: r["scale"]) if g_ok else \
        min(global_rows, key=lambda r: abs(r["span_log_median"] - 0.9))

    # Deviation: modest spread, strictly smaller than global.
    d_ok = [r for r in dev_rows
            if r["ptr_median"] < 1.7 and r["ptr_p90"] < 4.0
            and r["scale"] < g_pick["scale"]]
    d_pick = max(d_ok, key=lambda r: r["scale"]) if d_ok else \
        min(dev_rows, key=lambda r: r["ptr_median"])

    return {
        "s_g": g_pick["scale"],
        "s_u": d_pick["scale"],
        "s_v": d_pick["scale"],
        "global_pick_diag": g_pick,
        "dev_pick_diag": d_pick,
    }


# --------------------------------------------------------------------------- #
# Overlay PNG.
# --------------------------------------------------------------------------- #

def save_png(rec, n_show, seed, png_path):
    """Save a prior-predictive overlay PNG for the recommended scales.

    Left panel: ``n_show`` sampled GLOBAL trajectories (exp scale, normalised to
    a notional mean per-city total) at the recommended ``s_g``. Right panel:
    sampled province/city DEVIATION multipliers at the recommended ``s_u``.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(seed + 7)
    edges = np.arange(-50, 350 + 25, 25, dtype=float)
    centres = (edges[:-1] + edges[1:]) / 2

    g = sample_tier_shapes(rec["s_g"], n_show, rng)        # (n_show, T) log
    u = sample_tier_shapes(rec["s_u"], n_show, rng)        # deviation log

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))

    # Global: show as multiplicative trajectory (exp of zero-sum shape).
    for i in range(n_show):
        axes[0].plot(centres, np.exp(g[i]), color="C0", alpha=0.18, lw=0.8)
    axes[0].plot(centres, np.exp(np.median(g, axis=0)), color="k", lw=2,
                 label="prior median")
    axes[0].axhline(1.0, color="grey", ls=":", lw=1)
    axes[0].set_title(f"Prior GLOBAL trajectories  (s_g={rec['s_g']})\n"
                      f"exp(zero-sum shape): multiplier vs trajectory mean")
    axes[0].set_xlabel("year (AD; negative = BC)")
    axes[0].set_ylabel("rate multiplier (x mean)")
    axes[0].legend(fontsize=8)

    # Deviation: exp of u-shape = multiplicative province/city offset.
    for i in range(n_show):
        axes[1].plot(centres, np.exp(u[i]), color="C1", alpha=0.18, lw=0.8)
    axes[1].axhline(1.0, color="grey", ls=":", lw=1)
    axes[1].set_title(f"Prior province/city DEVIATIONS  (s_u=s_v={rec['s_u']})\n"
                      f"exp(zero-sum shape): multiplier vs parent")
    axes[1].set_xlabel("year (AD; negative = BC)")
    axes[1].set_ylabel("deviation multiplier (x parent)")

    fig.tight_layout()
    fig.savefig(png_path, dpi=130)
    print(f"\nPrior-predictive overlay PNG -> {png_path}")


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n-draws", type=int, default=4000,
                   help="Prior trajectories per scale (diagnostics).")
    p.add_argument("--n-show", type=int, default=60,
                   help="Trajectories drawn for the overlay PNG.")
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--s-g-grid", type=float, nargs="+", default=[0.3, 0.5, 0.7])
    p.add_argument("--s-u-grid", type=float, nargs="+", default=[0.15, 0.2, 0.3, 0.5])
    p.add_argument("--s-v-grid", type=float, nargs="+", default=[0.15, 0.2, 0.3, 0.5])
    p.add_argument("--png", type=Path,
                   default=Path(__file__).resolve().parent / "prior-predictive-overlay.png")
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "prior-predictive-results.json")
    args = p.parse_args()

    global_rows, dev_rows = run_grid(
        args.s_g_grid, args.s_u_grid, args.s_v_grid, args.n_draws, args.seed)

    print("=" * 78)
    print("PRIOR-PREDICTIVE GRID — GLOBAL shape (sigma_g ~ HalfNormal(s_g))")
    print("=" * 78)
    print(f"  {'s_g':>5} {'adj med':>8} {'adj p90':>8} "
          f"{'span med':>9} {'span p75':>9} {'span p90':>9} "
          f"{'ptr med':>8} {'<1.5lu':>7} {'<.5adj':>7}")
    for r in global_rows:
        print(f"  {r['scale']:>5} {r['adj_jump_median']:>8.3f} "
              f"{r['adj_jump_p90']:>8.2f} "
              f"{r['span_log_median']:>9.2f} {r['span_log_p75']:>9.2f} "
              f"{r['span_log_p90']:>9.2f} {r['ptr_median']:>8.2f} "
              f"{r['frac_span_lt_1p5lu']:>7.2f} {r['frac_adj_lt_0p5lu']:>7.2f}")

    print("\n" + "=" * 78)
    print("PRIOR-PREDICTIVE GRID — DEVIATION shape (sigma_u/v ~ HalfNormal(s))")
    print("=" * 78)
    print(f"  {'s':>5} {'adj_jump med':>12} {'p90':>6} "
          f"{'ptr med':>8} {'ptr p90':>8} {'ptr p99':>8}")
    for r in dev_rows:
        print(f"  {r['scale']:>5} {r['adj_jump_median']:>12.3f} "
              f"{r['adj_jump_p90']:>6.2f} "
              f"{r['ptr_median']:>8.2f} {r['ptr_p90']:>8.2f} {r['ptr_p99']:>8.2f}")

    rec = recommend(global_rows, dev_rows)
    print("\n" + "=" * 78)
    print("RECOMMENDATION")
    print("=" * 78)
    print(f"  s_g = {rec['s_g']}   s_u = {rec['s_u']}   s_v = {rec['s_v']}")
    print(f"  global pick : adj_jump med {rec['global_pick_diag']['adj_jump_median']:.3f}, "
          f"ptr med {rec['global_pick_diag']['ptr_median']:.2f}, "
          f"ptr p90 {rec['global_pick_diag']['ptr_p90']:.2f}")
    print(f"  dev pick    : ptr med {rec['dev_pick_diag']['ptr_median']:.2f}, "
          f"ptr p90 {rec['dev_pick_diag']['ptr_p90']:.2f}")
    print("=" * 78)

    save_png(rec, args.n_show, args.seed, args.png)

    out = {
        "n_draws": args.n_draws,
        "global_rows": global_rows,
        "dev_rows": dev_rows,
        "recommendation": {k: rec[k] for k in ("s_g", "s_u", "s_v")},
        "recommendation_diag": {
            "global_pick": rec["global_pick_diag"],
            "dev_pick": rec["dev_pick_diag"],
        },
    }
    args.results.write_text(json.dumps(out, indent=2))
    print(f"Results JSON -> {args.results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
