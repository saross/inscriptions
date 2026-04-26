#!/usr/bin/env python3
"""
experiment_aoristic_mc.py --- single-cell test harness for the (A) fix.

Tests the hypothesis that high zero-effect false-positive (FP) rates in
the H1 simulation are caused by an uncertainty-structure mismatch between
observed SPAs (which carry aoristic-resample variance) and MC replicate
SPAs (which carry only Poisson-on-fit variance).

Hypothesised fix (Option A): generate MC replicates by *aoristic-
resampling* synthetic inscriptions whose true centres are drawn from the
fitted null-as-probability-mass-function and whose interval widths are
drawn from the empirical width distribution of the bootstrap sample.
This way both observed and MC replicate SPAs carry the same aoristic-
smearing variance under H0.

This script:
  - Picks one cell where the original FP rate was high (default:
    province / cpl-3 / n=2500, where original FP=0.470).
  - Runs N iterations using both the OLD sampler (Poisson-on-fit) and
    the NEW sampler (aoristic-from-fit).
  - Reports FP rate and detection rate (under one non-zero bracket) for
    each.
  - Saves results to runs/2026-04-25-h1-simulation/outputs/experiment-A/.

The script is a one-off experiment, NOT a unit test; once the fix is
validated, the new sampler is folded into primitives.py and committed.

Usage:
  python3 experiment_aoristic_mc.py [--n_iter 200] [--n_mc 1000]
                                     [--n 2500] [--level province]

Author: Claude Code (Opus 4.7) under Shawn Ross's direction, 2026-04-25.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd

import primitives as P

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# New aoristic-from-fit MC sampler (the proposed Option A fix)
# ---------------------------------------------------------------------------

def sample_null_spa_aoristic(
    null_params: dict,
    n: int,
    widths: np.ndarray,
    bin_edges: np.ndarray,
    bin_centres: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate one MC replicate SPA by aoristic-resampling under the null.

    Procedure:
      1. Treat the fitted null SPA as a probability mass function over
         bin_centres (normalised to sum to 1).
      2. Draw ``n`` synthetic interval-centre years from this pmf, with
         within-bin uniform jitter to break lattice effects.
      3. Draw ``n`` interval widths from the empirical width distribution
         (with replacement).
      4. Construct synthetic ``[not_before, not_after]`` per row.
      5. Aoristic-draw a uniform date within each row's interval.
      6. Bin into ``bin_edges`` --> MC replicate SPA.

    This produces MC replicates whose uncertainty structure matches the
    observed SPA pipeline (bootstrap from LIRE --> aoristic-resample -->
    bin), under the null hypothesis that the fit captures the true shape.

    Parameters
    ----------
    null_params : dict
        From ``fit_null_exponential`` or ``fit_null_cpl``; uses the
        ``"fitted"`` key as the pmf shape.
    n : int
        Number of synthetic inscriptions per replicate (matches observed
        cell n).
    widths : numpy.ndarray
        Empirical interval widths from the bootstrap sample
        (``not_after - not_before``, length n).
    bin_edges : numpy.ndarray
        Bin edges (length len(bin_centres) + 1).
    bin_centres : numpy.ndarray
        Bin centre-year values.
    rng : numpy.random.Generator
        Seeded generator.

    Returns
    -------
    numpy.ndarray
        MC replicate SPA.
    """
    fitted = null_params["fitted"]
    if fitted.shape != bin_centres.shape:
        raise ValueError("fitted must match bin_centres shape")
    pdf = np.clip(fitted, 0.0, None)
    total = pdf.sum()
    if not np.isfinite(total) or total <= 0:
        return np.zeros(len(bin_centres), dtype=float)
    pdf = pdf / total

    bin_width = float(bin_edges[1] - bin_edges[0])

    # 1-2. Draw synthetic centres from pmf, with within-bin uniform jitter.
    chosen_bin_idx = rng.choice(len(bin_centres), size=n, p=pdf)
    centres = bin_centres[chosen_bin_idx] + rng.uniform(
        -bin_width / 2.0, bin_width / 2.0, size=n,
    )

    # 3. Draw widths from empirical distribution (with replacement).
    w = rng.choice(widths, size=n, replace=True)

    # 4. Construct synthetic [not_before, not_after].
    half = w / 2.0
    nb_synth = centres - half
    na_synth = centres + half

    # 5. Aoristic-draw within each interval.
    years = rng.uniform(nb_synth, na_synth)

    # 6. Bin.
    spa, _ = np.histogram(years, bins=bin_edges)
    return spa.astype(float)


def sample_mc_nonparametric(
    df: pd.DataFrame,
    n: int,
    bin_edges: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate one MC replicate SPA by row-bootstrap + aoristic resample.

    Option C in the scout taxonomy: non-parametric envelope. Bootstrap n
    rows from the filtered LIRE frame with replacement; for each row draw
    a uniform date within its [not_before, not_after]; bin. This yields
    MC replicates with EXACTLY the same variance structure as observed
    (same operation, fresh randomness).

    Tests: is observed extreme relative to other re-bootstraps of itself?
    Does NOT test against a parametric null growth model.
    """
    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)
    idx = rng.integers(0, len(df), size=n)
    years = rng.uniform(nb[idx], na[idx])
    spa, _ = np.histogram(years, bins=bin_edges)
    return spa.astype(float)


def envelope_test_with_sampler(
    observed_spa: np.ndarray,
    null_params: dict | None,
    bin_centres: np.ndarray,
    bin_edges: np.ndarray,
    n_mc: int,
    rng: np.random.Generator,
    *,
    sampler: str,
    n: int | None = None,
    widths: np.ndarray | None = None,
    df: pd.DataFrame | None = None,
    alpha: float = 0.05,
    variance_floor: float = 1e-10,
) -> dict:
    """Run Timpson 2014 envelope test with a swappable MC sampler.

    sampler='old':           Poisson-on-fit (current primitives.sample_null_spa).
    sampler='aoristic':      aoristic-from-fit. Requires n + widths.
    sampler='nonparametric': row-bootstrap + aoristic from df. Requires n + df.
    """
    mc_array = np.empty((n_mc, len(bin_centres)), dtype=float)
    if sampler == "old":
        for i in range(n_mc):
            mc_array[i] = P.sample_null_spa(
                null_params, "cpl", bin_centres, rng,
            )
    elif sampler == "aoristic":
        if n is None or widths is None:
            raise ValueError("aoristic sampler requires n and widths")
        for i in range(n_mc):
            mc_array[i] = sample_null_spa_aoristic(
                null_params, n, widths, bin_edges, bin_centres, rng,
            )
    elif sampler == "nonparametric":
        if n is None or df is None:
            raise ValueError("nonparametric sampler requires n and df")
        for i in range(n_mc):
            mc_array[i] = sample_mc_nonparametric(df, n, bin_edges, rng)
    else:
        raise ValueError(f"unknown sampler: {sampler!r}")

    lo_env = np.quantile(mc_array, alpha / 2.0, axis=0)
    hi_env = np.quantile(mc_array, 1.0 - alpha / 2.0, axis=0)

    var = mc_array.var(axis=0)
    keep = var >= variance_floor

    obs_outside_mask = (observed_spa < lo_env) | (observed_spa > hi_env)
    obs_outside = int((obs_outside_mask & keep).sum())

    mc_outside_mask = (mc_array < lo_env) | (mc_array > hi_env)
    mc_outside = (mc_outside_mask & keep[np.newaxis, :]).sum(axis=1)

    pval_global = float(np.mean(mc_outside >= obs_outside))
    return {
        "detected": bool(pval_global < alpha),
        "pval_global": pval_global,
        "n_bins_outside": obs_outside,
    }


# ---------------------------------------------------------------------------
# Experiment driver
# ---------------------------------------------------------------------------

def run_one_iter(
    df: pd.DataFrame,
    n: int,
    bracket_magnitude: float,
    bracket_duration: float,
    bracket_shape: str,
    cpl_k: int,
    bin_edges: np.ndarray,
    bin_centres: np.ndarray,
    n_mc: int,
    rng: np.random.Generator,
) -> dict:
    """One iteration: bootstrap, aoristic-resample, fit CPL, inject, test (both samplers)."""
    # Bootstrap n rows.
    idx = rng.integers(0, len(df), size=n)
    nb = df["not_before"].to_numpy(dtype=float)[idx]
    na = df["not_after"].to_numpy(dtype=float)[idx]
    widths = na - nb

    # Aoristic-resample to build observed SPA.
    years = rng.uniform(nb, na)
    observed_spa, _ = np.histogram(years, bins=bin_edges)
    observed_spa = observed_spa.astype(float)

    # Fit CPL-k.
    fit = P.fit_null_cpl(observed_spa, bin_centres, k=cpl_k)
    if not fit.get("converged", False):
        return {"converged": False}

    # Inject effect (zero magnitude = identity).
    spa_modified = P.inject_effect(
        observed_spa, bin_centres,
        magnitude=bracket_magnitude,
        centre_year=150.0,  # mid-envelope
        duration=bracket_duration,
        shape=bracket_shape,
    )

    # Test all three samplers.
    res_old = envelope_test_with_sampler(
        spa_modified, fit, bin_centres, bin_edges, n_mc, rng,
        sampler="old",
    )
    res_aor = envelope_test_with_sampler(
        spa_modified, fit, bin_centres, bin_edges, n_mc, rng,
        sampler="aoristic", n=n, widths=widths,
    )
    res_np = envelope_test_with_sampler(
        spa_modified, None, bin_centres, bin_edges, n_mc, rng,
        sampler="nonparametric", n=n, df=df,
    )
    return {
        "converged": True,
        "detected_old": res_old["detected"],
        "pval_old": res_old["pval_global"],
        "n_outside_old": res_old["n_bins_outside"],
        "detected_aor": res_aor["detected"],
        "pval_aor": res_aor["pval_global"],
        "n_outside_aor": res_aor["n_bins_outside"],
        "detected_np": res_np["detected"],
        "pval_np": res_np["pval_global"],
        "n_outside_np": res_np["n_bins_outside"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n_iter", type=int, default=200,
                        help="Iterations per (cell, bracket).")
    parser.add_argument("--n_mc", type=int, default=1000,
                        help="MC replicates per envelope test.")
    parser.add_argument("--n", type=int, default=2500,
                        help="Bootstrap sample size (matches H1 cell n).")
    parser.add_argument("--cpl_k", type=int, default=3,
                        help="CPL knot count (matches H1 primary).")
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--out", type=Path,
                        default=Path("runs/2026-04-25-h1-simulation/outputs/experiment-A"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    # Load LIRE.
    lire_path = Path("archive/data-2026-04-22/LIRE_v3-0.parquet")
    logger.info("Loading LIRE from %s", lire_path)
    df = P.load_filtered_lire(lire_path)
    logger.info("Filtered LIRE: %d rows", len(df))

    bin_edges = P.BIN_EDGES
    bin_centres = P.BIN_CENTRES

    # Brackets to test: zero (FP target ≤0.05) + a_50pc_50y (detection sanity).
    brackets = {
        "zero":         {"magnitude":  0.0, "duration": 50.0, "shape": "step"},
        "a_50pc_50y":   {"magnitude": -0.5, "duration": 50.0, "shape": "step"},
    }

    ss = np.random.SeedSequence(args.seed)
    children = ss.spawn(args.n_iter * len(brackets))

    results = []
    t0 = time.time()
    for b_idx, (b_name, b_params) in enumerate(brackets.items()):
        logger.info("Bracket %s — running %d iterations", b_name, args.n_iter)
        for i in range(args.n_iter):
            seed_idx = b_idx * args.n_iter + i
            rng = np.random.Generator(np.random.PCG64(children[seed_idx]))
            r = run_one_iter(
                df, args.n,
                b_params["magnitude"], b_params["duration"], b_params["shape"],
                args.cpl_k, bin_edges, bin_centres, args.n_mc, rng,
            )
            r["bracket"] = b_name
            r["iter"] = i
            results.append(r)
            if (i + 1) % 50 == 0:
                logger.info("  bracket=%s iter=%d/%d", b_name, i + 1, args.n_iter)
    elapsed = time.time() - t0
    logger.info("Total elapsed: %.1f s", elapsed)

    res_df = pd.DataFrame(results)
    out_parquet = args.out / "results.parquet"
    res_df.to_parquet(out_parquet, index=False)
    logger.info("Wrote %s", out_parquet)

    # Summary.
    converged = res_df[res_df["converged"]]
    summary = {}
    for b_name in brackets:
        sub = converged[converged["bracket"] == b_name]
        if len(sub) == 0:
            continue
        summary[b_name] = {
            "n_converged": int(len(sub)),
            "rate_old":  float(sub["detected_old"].mean()),
            "rate_aor":  float(sub["detected_aor"].mean()),
            "rate_np":   float(sub["detected_np"].mean()),
            "median_pval_old": float(sub["pval_old"].median()),
            "median_pval_aor": float(sub["pval_aor"].median()),
            "median_pval_np":  float(sub["pval_np"].median()),
            "median_outside_old": float(sub["n_outside_old"].median()),
            "median_outside_aor": float(sub["n_outside_aor"].median()),
            "median_outside_np":  float(sub["n_outside_np"].median()),
        }

    out_summary = args.out / "summary.json"
    with out_summary.open("w") as f:
        json.dump({
            "args": {
                "n_iter": args.n_iter, "n_mc": args.n_mc,
                "n": args.n, "cpl_k": args.cpl_k, "seed": args.seed,
            },
            "elapsed_seconds": elapsed,
            "by_bracket": summary,
            "interpretation": (
                "rate_old should match the broken FP rate in REPORT.md "
                "(province cpl-3 step n=2500 zero: ~0.45). rate_new should "
                "drop to ~0.05 if Option A fixes the variance-mismatch. "
                "For a_50pc_50y, rate_new should remain HIGH (≥0.80) — "
                "verifying detection power is preserved."
            ),
        }, f, indent=2)
    logger.info("Wrote %s", out_summary)

    # Print summary to stdout.
    print()
    print("=" * 70)
    print("EXPERIMENT (A) — aoristic-from-fit MC vs Poisson-on-fit MC")
    print(f"Cell: province / cpl-{args.cpl_k} / step / n={args.n}")
    print(f"Iterations: {args.n_iter} per bracket; MC: {args.n_mc} per test")
    print("=" * 70)
    for b_name, s in summary.items():
        print(f"\nBracket: {b_name}")
        print(f"  Converged: {s['n_converged']}/{args.n_iter}")
        print(f"  rate_old  (Poisson-on-fit):    {s['rate_old']:.3f}")
        print(f"  rate_aor  (aoristic-from-fit): {s['rate_aor']:.3f}")
        print(f"  rate_np   (row-bootstrap):     {s['rate_np']:.3f}")
        print(f"  median p (old / aor / np): {s['median_pval_old']:.3f}"
              f" / {s['median_pval_aor']:.3f} / {s['median_pval_np']:.3f}")
        print(f"  median bins outside (old / aor / np): {s['median_outside_old']:.1f}"
              f" / {s['median_outside_aor']:.1f} / {s['median_outside_np']:.1f}")
    print()
    print("Pass criteria for each sampler:")
    print("  zero bracket:        rate ≤ 0.10 (target ≤ 0.05)")
    print("  a_50pc_50y bracket:  rate ≥ 0.70 (detection power preserved)")
    print()


if __name__ == "__main__":
    main()
