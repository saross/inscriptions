#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sim_recovery.py — §5 Layer-A likelihood correctness gate (simulation recovery).
===============================================================================

Validate the single-city Poisson-process aoristic likelihood (``model.py``) by
simulating data from a KNOWN rate curve and checking that the posterior recovers
it. This is the gate: if recovery is poor the likelihood is wrong; if recovery
is good the likelihood is validated.

Simulation design (per the brief):

1. **True curve.** A smooth rise-and-fall bump over the 16 bins (log-rate is a
   Gaussian bump peaking mid-series), scaled so the expected total count is
   ``EXPECTED_N`` (default 150). ``lam_true[t]`` is the true expected count in
   bin ``t``; ``sum_t lam_true == EXPECTED_N``.

2. **Simulate inscriptions.** Draw ``N ~ Poisson(EXPECTED_N)``. For each
   inscription draw a true bin ``t* ~ Categorical(lam_true / sum lam_true)`` and
   a true year uniformly within that bin. Draw an interval WIDTH from the
   empirical target-set width distribution (clipped-interval lengths sampled from
   the real prepared data). Place the interval to CONTAIN the true year (random
   offset), clip to the envelope, and compute its aoristic row. Inscriptions are
   re-drawn if clipping leaves zero aoristic mass (rare; guards log(0)).

3. **Fit and score.** Fit ``model.py``; compute
   (i) Pearson r between posterior-median ``lam`` and ``lam_true``;
   (ii) coverage = fraction of bins whose 95% credible interval contains
        ``lam_true[t]`` (target ~0.95, allowing for aoristic smearing);
   (iii) convergence (max R-hat, min bulk ESS, divergences).

Repeat for ``--n-sims`` datasets and report the distribution of r and coverage.

Run (on zbook, in the venv, with the threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/sim_recovery.py \
        --n-sims 10 --draws 1000 --tune 1000

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model as m  # noqa: E402  (local module)
import dataprep as dp  # noqa: E402

T = dp.N_BINS            # 16
ENV_LO = dp.ENV_LO       # -50
ENV_HI = dp.ENV_HI       # 350
BIN_W = dp.BIN_WIDTH     # 25
EDGES = dp.BIN_EDGES     # length 17


# --------------------------------------------------------------------------- #
# True curve and empirical widths.
# --------------------------------------------------------------------------- #

def true_lambda(expected_n: float = 150.0, peak_bin: float = 7.5,
                spread: float = 3.0, amplitude: float = 1.3) -> np.ndarray:
    """A smooth rise-and-fall true rate curve, scaled to ``expected_n`` total.

    The log-rate is a Gaussian bump centred at ``peak_bin`` with width
    ``spread`` and peak-to-trough log amplitude controlled by ``amplitude``.

    Args:
        expected_n: Target total expected count (sum over bins).
        peak_bin: Bin index (0..T-1, can be fractional) of the bump peak.
        spread: Gaussian width of the bump (in bins).
        amplitude: Log-rate amplitude of the bump.

    Returns:
        ``lam_true`` array of length ``T`` with ``sum == expected_n``.
    """
    t = np.arange(T)
    log_shape = amplitude * np.exp(-0.5 * ((t - peak_bin) / spread) ** 2)
    shape = np.exp(log_shape)
    shape /= shape.sum()
    return shape * expected_n


def empirical_widths(out_dir: Path) -> np.ndarray:
    """Collect clipped-interval widths from the prepared target-set cache.

    Pools the clipped ``(na - nb)`` widths across all cached target +
    large-anchor cities, giving the empirical width distribution used to assign
    realistic intervals to simulated inscriptions.

    Args:
        out_dir: The dataprep cache directory.

    Returns:
        1-D int array of interval widths (years), all > 0.
    """
    idx = pd.read_parquet(out_dir / "city-index.parquet")
    fittable = idx[idx["bucket"].isin(["target", "large_anchor"])]["city"]
    widths = []
    for city in fittable:
        bundle = dp.load_city(out_dir, city)
        widths.append(bundle["na_clip"] - bundle["nb_clip"])
    w = np.concatenate(widths)
    w = w[w > 0]
    return w.astype(int)


# --------------------------------------------------------------------------- #
# Simulation.
# --------------------------------------------------------------------------- #

def simulate_dataset(lam_true: np.ndarray, widths: np.ndarray,
                     rng: np.random.Generator) -> tuple[np.ndarray, int]:
    """Simulate one interval-censored dataset from ``lam_true``.

    Args:
        lam_true: True per-bin expected counts (length ``T``).
        widths: Empirical width pool to sample interval widths from.
        rng: NumPy random generator.

    Returns:
        ``(A, N)``: the aoristic matrix ``(N, T)`` and the realised count ``N``.
    """
    total = lam_true.sum()
    n = int(rng.poisson(total))
    n = max(n, 5)  # guard against a pathological tiny draw
    probs = lam_true / total

    nb_list, na_list = [], []
    for _ in range(n):
        # True bin and a true year uniformly within it.
        t_star = int(rng.choice(T, p=probs))
        lo_edge, hi_edge = EDGES[t_star], EDGES[t_star + 1]
        true_year = rng.uniform(lo_edge, hi_edge)
        # Sample an interval width and place it to contain the true year.
        width = int(rng.choice(widths))
        width = max(width, 1)
        # Random left offset so the interval brackets the true year.
        offset = rng.uniform(0.0, width)
        nb = true_year - offset
        na = nb + width
        # Clip to the envelope.
        nb_c = max(ENV_LO, nb)
        na_c = min(ENV_HI, na)
        if na_c - nb_c <= 0:
            # Degenerate after clipping; fall back to the single true bin.
            nb_c, na_c = lo_edge, hi_edge
        nb_list.append(nb_c)
        na_list.append(na_c)

    A = dp.aoristic_matrix(np.array(nb_list), np.array(na_list))
    # Guard: drop any row that ended up with zero aoristic mass (log(0)).
    mass = A.sum(axis=1)
    A = A[mass > 0]
    return A, A.shape[0]


# --------------------------------------------------------------------------- #
# Scoring.
# --------------------------------------------------------------------------- #

def score_recovery(idata, lam_true: np.ndarray) -> dict:
    """Score one fit against the true curve.

    Args:
        idata: Posterior InferenceData from the fit.
        lam_true: True per-bin expected counts (length ``T``).

    Returns:
        Dict with ``pearson_r``, ``coverage``, plus convergence fields.
    """
    lam_post = idata.posterior["lam"]  # (chain, draw, T)
    lam_med = lam_post.median(("chain", "draw")).values
    lo = lam_post.quantile(0.025, ("chain", "draw")).values
    hi = lam_post.quantile(0.975, ("chain", "draw")).values

    # Pearson r on the shape (median vs true).
    r = float(np.corrcoef(lam_med, lam_true)[0, 1])
    # Coverage: fraction of bins whose 95% CI contains the truth.
    covered = (lam_true >= lo) & (lam_true <= hi)
    coverage = float(covered.mean())

    conv = m.convergence_summary(idata)
    return {
        "pearson_r": r,
        "coverage": coverage,
        "max_rhat": conv["max_rhat"],
        "min_ess_bulk": conv["min_ess_bulk"],
        "n_divergences": conv["n_divergences"],
        "lam_med": lam_med.tolist(),
        "lam_lo": lo.tolist(),
        "lam_hi": hi.tolist(),
    }


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def run(n_sims: int, out_dir: Path, draws: int, tune: int, chains: int,
        target_accept: float, expected_n: float, seed: int,
        results_path: Path | None) -> dict:
    """Run the full sim-recovery loop and return aggregate results."""
    rng = np.random.default_rng(seed)
    lam_true = true_lambda(expected_n=expected_n)
    widths = empirical_widths(out_dir)
    print(f"True curve sum = {lam_true.sum():.1f}; "
          f"empirical width pool n={len(widths)} "
          f"(median {int(np.median(widths))}y, "
          f"p25 {int(np.percentile(widths, 25))}y, "
          f"p75 {int(np.percentile(widths, 75))}y)")
    print(f"lam_true = {np.round(lam_true, 2)}")

    per_sim = []
    for k in range(n_sims):
        A, n = simulate_dataset(lam_true, widths, rng)
        idata = m.fit(A, draws=draws, tune=tune, chains=chains,
                      target_accept=target_accept,
                      random_seed=int(rng.integers(0, 2**31 - 1)),
                      progressbar=False)
        sc = score_recovery(idata, lam_true)
        sc["sim"] = k
        sc["N"] = int(n)
        per_sim.append(sc)
        print(f"  sim {k:>2}: N={n:>3}  r={sc['pearson_r']:.3f}  "
              f"cov={sc['coverage']:.2f}  rhat={sc['max_rhat']:.3f}  "
              f"ess={sc['min_ess_bulk']:.0f}  div={sc['n_divergences']}")

    rs = np.array([s["pearson_r"] for s in per_sim])
    covs = np.array([s["coverage"] for s in per_sim])
    rhats = np.array([s["max_rhat"] for s in per_sim])
    esss = np.array([s["min_ess_bulk"] for s in per_sim])
    divs = np.array([s["n_divergences"] for s in per_sim])

    agg = {
        "n_sims": n_sims,
        "expected_n": expected_n,
        "lam_true": lam_true.tolist(),
        "r_mean": float(rs.mean()), "r_min": float(rs.min()),
        "r_max": float(rs.max()), "r_median": float(np.median(rs)),
        "coverage_mean": float(covs.mean()), "coverage_min": float(covs.min()),
        "coverage_max": float(covs.max()), "coverage_median": float(np.median(covs)),
        "max_rhat_over_sims": float(rhats.max()),
        "min_ess_over_sims": float(esss.min()),
        "total_divergences": int(divs.sum()),
        "sims_passing_gates": int(np.sum(
            (rhats < 1.01) & (esss >= 400) & (divs == 0))),
        "per_sim": per_sim,
    }

    print("\n" + "=" * 64)
    print("SIM-RECOVERY AGGREGATE")
    print("=" * 64)
    print(f"  Pearson r : mean {agg['r_mean']:.3f}  median {agg['r_median']:.3f}  "
          f"min {agg['r_min']:.3f}  max {agg['r_max']:.3f}")
    print(f"  coverage  : mean {agg['coverage_mean']:.3f}  "
          f"median {agg['coverage_median']:.3f}  "
          f"min {agg['coverage_min']:.3f}  max {agg['coverage_max']:.3f}")
    print(f"  convergence: max R-hat {agg['max_rhat_over_sims']:.3f}  "
          f"min ESS {agg['min_ess_over_sims']:.0f}  "
          f"total div {agg['total_divergences']}  "
          f"sims passing gates {agg['sims_passing_gates']}/{n_sims}")
    print("=" * 64)

    if results_path is not None:
        results_path.write_text(json.dumps(agg, indent=2))
        print(f"Results JSON -> {results_path}")
    return agg


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n-sims", type=int, default=10)
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--expected-n", type=float, default=150.0)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--out-dir", type=Path,
                   default=Path(__file__).resolve().parent / "prepared")
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "sim-recovery-results.json")
    args = p.parse_args()
    run(args.n_sims, args.out_dir, args.draws, args.tune, args.chains,
        args.target_accept, args.expected_n, args.seed, args.results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
