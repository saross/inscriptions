#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-cell-mixture-fit.py
======================

Fit the preregistered Bayesian mixture model to one synthetic replicate
from the H2.1 recovery grid. This implements the prereg's binding spec
(prereg §3 lines 165-210):

    y_t ~ Multinomial(N, p_t)
    p_t = alpha * p_conv,t + (1 - alpha) * p_gen,t
    p_conv = tier_weights @ tier_basis   (3 tiers; Decision 20)
    p_gen  = softmax(log_p_gen_raw)
    log_p_gen_raw ~ GaussianRandomWalk(sigma_smooth)
    sigma_smooth ~ HalfNormal(1)
    alpha ~ Beta(2, 2)
    tier_weights ~ Dirichlet([1, 1, 1])

The Gaussian random-walk smoothness prior on log p_gen replaces the
talk-demo's parametric Gaussian — this is the Phase-2-rigorous spec
(prereg §3 line 204).

This script supports both single-replicate fitting (CLI invocation for
the smoke test) and a programmatic API used by the orchestrator.

Usage (CLI for smoke test)
--------------------------
    python 02-cell-mixture-fit.py \\
        --design-json /path/to/design.json \\
        --output-root /path/to/runs/.../recovery-grid-validation \\
        --cell-id shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000 \\
        --replicate 0 \\
        [--n-draws 2000] [--n-tune 1000] [--n-chains 4] \\
        [--target-accept 0.95] [--cores 1]

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Suppress the very noisy pymc / pytensor compilation banners and arviz
# FutureWarnings; these clutter the per-fit logs in a 450-cell grid.
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN")

import arviz as az  # noqa: E402
import pymc as pm  # noqa: E402
import pytensor.tensor as pt  # noqa: E402
from scipy.stats import pearsonr, wasserstein_distance  # noqa: E402

# Reuse helpers from the generator script. The two scripts live in the
# same directory; we add it to sys.path so the imports work either when
# called as a module or executed directly.
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))
# The leading "01-" in the filename prevents normal `import` — load via
# importlib instead so we can reuse the design parsing helpers.
import importlib.util  # noqa: E402

_SPEC = importlib.util.spec_from_file_location(
    "synth_gen", _THIS_DIR / "01-synthetic-cell-generator.py"
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Could not load 01-synthetic-cell-generator.py")
synth_gen = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(synth_gen)


# ---------------------------------------------------------------------------
# Default NUTS settings (overridable via CLI).
# ---------------------------------------------------------------------------
DEFAULT_N_DRAWS = 2_000
DEFAULT_N_TUNE = 1_000
DEFAULT_N_CHAINS = 4
DEFAULT_TARGET_ACCEPT = 0.95
DEFAULT_CORES = 1  # within-fit; orchestrator parallelises across cells.

# Convergence gates (prereg §3 line 208).
RHAT_GATE = 1.01
ESS_GATE = 400


# ---------------------------------------------------------------------------
# Model construction
# ---------------------------------------------------------------------------
def build_model(
    y: np.ndarray,
    tier_basis: np.ndarray,
) -> pm.Model:
    """Construct the prereg-binding three-tier multinomial mixture.

    Parameters
    ----------
    y : (N_BINS,) int array
        Observed multinomial counts per 5-year bin.
    tier_basis : (3, N_BINS) float array
        Tier basis matrix; each row sums to 1.

    Returns
    -------
    model : pymc.Model
    """
    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        # Mixture weight (prereg §3 line 206).
        alpha = pm.Beta("alpha", 2.0, 2.0)
        # Tier weights (Dirichlet uniform; prereg §3 line 206).
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float)
        )
        # Convention component: tier_weights @ tier_basis.
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis)
        )
        # Genuine component: softmax of a Gaussian random walk on log
        # densities. The smoothness prior is the prereg's Gaussian random
        # walk with HalfNormal(1) bandwidth (§3 line 204, 206).
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
        # GaussianRandomWalk over N_BINS log-density values.
        # Anchor the first bin's log-density at 0 (a fixed reference,
        # absorbed by the softmax) and let the increments be normal with
        # scale sigma_smooth. Implemented via cumulative-sum of normal
        # increments to stay compatible with the pymc 6 API in the
        # sapphire venv.
        log_pgen_increments = pm.Normal(
            "log_pgen_increments",
            mu=0.0,
            sigma=sigma_smooth,
            shape=n_bins - 1,
        )
        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)]
        )
        # Softmax to a probability vector summing to 1.
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))

        # Mixture and observation.
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)

    return model


# ---------------------------------------------------------------------------
# Posterior summarisation
# ---------------------------------------------------------------------------
def _flat_var(idata: az.InferenceData, name: str) -> np.ndarray:
    """Return the flat (chain*draw, ...) draws array for a posterior var."""
    arr = idata.posterior[name].values
    if arr.ndim == 2:
        # (chain, draw)
        return arr.reshape(-1)
    # (chain, draw, *)
    return arr.reshape(-1, *arr.shape[2:])


def summarise_posterior(
    idata: az.InferenceData,
    truth: dict[str, Any],
    bin_centres: np.ndarray,
) -> dict[str, Any]:
    """Compute the per-replicate scalars persisted by this script.

    Parameters
    ----------
    idata : arviz.InferenceData
        Output of ``pm.sample``.
    truth : dict
        Loaded from the replicate's ``*.truth.json`` sidecar.
    bin_centres : (N_BINS,) float array
        Used as the support for Wasserstein-1.
    """
    # Convergence diagnostics over the parameters we care about.
    summary_df = az.summary(
        idata,
        var_names=[
            "alpha", "tier_weights", "sigma_smooth", "log_pgen_increments",
        ],
        round_to="none",
    )
    max_rhat = float(summary_df["r_hat"].max())
    min_ess_bulk = float(summary_df["ess_bulk"].min())
    n_divergences = int(idata.sample_stats.diverging.values.sum())

    # Alpha recovery.
    alpha_samples = _flat_var(idata, "alpha")
    alpha_lo, alpha_hi = np.percentile(alpha_samples, [2.5, 97.5])
    alpha_med = float(np.median(alpha_samples))
    alpha_true = float(truth["alpha_true"])
    alpha_covered = bool(alpha_lo <= alpha_true <= alpha_hi)

    # p_gen recovery.
    pgen_draws = _flat_var(idata, "p_gen")  # (chain*draw, N_BINS)
    pgen_median = np.median(pgen_draws, axis=0)
    truth_pgen = np.asarray(truth["p_gen_true"], dtype=float)
    pearson_r, _ = pearsonr(pgen_median, truth_pgen)
    w1 = float(
        wasserstein_distance(bin_centres, bin_centres, pgen_median, truth_pgen)
    )

    # Tier weights recovery (descriptive).
    tier_draws = _flat_var(idata, "tier_weights")  # (chain*draw, 3)
    tier_lo = np.percentile(tier_draws, 2.5, axis=0)
    tier_hi = np.percentile(tier_draws, 97.5, axis=0)
    tier_med = np.median(tier_draws, axis=0)
    truth_tier = np.asarray(truth["tier_weights_true"], dtype=float)
    tier_covered = [
        bool(tier_lo[k] <= truth_tier[k] <= tier_hi[k])
        for k in range(len(truth_tier))
    ]

    convergence_pass = bool(
        max_rhat < RHAT_GATE
        and min_ess_bulk >= ESS_GATE
        and n_divergences == 0
    )

    return {
        "alpha_true": alpha_true,
        "alpha_median": alpha_med,
        "alpha_ci_lo": float(alpha_lo),
        "alpha_ci_hi": float(alpha_hi),
        "alpha_covered_95ci": alpha_covered,
        "pearson_r_pgen": float(pearson_r),
        "wasserstein_1_pgen": float(w1),
        "pgen_median": pgen_median.tolist(),
        "tier_weights_true": truth_tier.tolist(),
        "tier_weights_median": tier_med.tolist(),
        "tier_weights_ci_lo": tier_lo.tolist(),
        "tier_weights_ci_hi": tier_hi.tolist(),
        "tier_weights_covered_95ci": tier_covered,
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_divergences,
        "convergence_pass": convergence_pass,
    }


# ---------------------------------------------------------------------------
# Public API: fit one replicate end-to-end
# ---------------------------------------------------------------------------
def fit_replicate(
    cell_id: str,
    replicate: int,
    output_root: Path,
    design: dict[str, Any],
    tier_basis: np.ndarray,
    n_draws: int = DEFAULT_N_DRAWS,
    n_tune: int = DEFAULT_N_TUNE,
    n_chains: int = DEFAULT_N_CHAINS,
    target_accept: float = DEFAULT_TARGET_ACCEPT,
    cores: int = DEFAULT_CORES,
    progressbar: bool = False,
) -> dict[str, Any]:
    """Fit one replicate and persist the per-replicate posterior summary.

    Parameters
    ----------
    cell_id : str
        Cell id matching the directory under data/synthetic-cells/.
    replicate : int
        Replicate index 0-99.
    output_root : Path
        Validation-run root.
    design : dict
        Loaded design.json.
    tier_basis : (3, N_BINS) float array
    n_draws, n_tune, n_chains, target_accept, cores
        NUTS settings.

    Returns
    -------
    summary : dict, same content written to disk as
        ``outputs/cell-fits/<cell_id>/replicate_<r>-posterior.json`` plus
        a parquet sibling.
    """
    env = synth_gen.make_envelope(design)

    # Locate the replicate's data + truth.
    synth_path = (
        output_root / "data" / "synthetic-cells" / cell_id
        / f"replicate_{replicate:03d}.parquet"
    )
    truth_path = (
        output_root / "data" / "synthetic-cells" / cell_id
        / f"replicate_{replicate:03d}.truth.json"
    )
    if not synth_path.exists() or not truth_path.exists():
        raise FileNotFoundError(
            f"Missing synthetic data or truth sidecar for "
            f"cell {cell_id!r} replicate {replicate}."
        )
    df = pd.read_parquet(synth_path)
    with truth_path.open("r", encoding="utf-8") as fh:
        truth = json.load(fh)
    y = df["y"].to_numpy(dtype=np.int64)
    truth["p_gen_true"] = df["p_gen_true"].to_numpy(dtype=float).tolist()

    # Build + fit model.
    model = build_model(y, tier_basis)
    t0 = time.time()
    fit_seed = int(truth["seed"]) + 1  # distinct from data-gen seed
    with model:
        idata = pm.sample(
            draws=n_draws,
            tune=n_tune,
            chains=n_chains,
            cores=cores,
            random_seed=fit_seed,
            progressbar=progressbar,
            target_accept=target_accept,
            return_inferencedata=True,
        )
    fit_seconds = float(time.time() - t0)

    summary = summarise_posterior(idata, truth, env.bin_centres)
    summary["cell_id"] = cell_id
    summary["replicate"] = int(replicate)
    summary["fit_seconds"] = fit_seconds
    summary["n_draws"] = int(n_draws)
    summary["n_tune"] = int(n_tune)
    summary["n_chains"] = int(n_chains)
    summary["target_accept"] = float(target_accept)
    summary["cores"] = int(cores)

    # Persist.
    out_dir = output_root / "outputs" / "cell-fits" / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / f"replicate_{replicate:03d}-posterior.json"
    out_parquet = out_dir / f"replicate_{replicate:03d}-posterior.parquet"
    with out_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    # Parquet sibling captures the scalar fields for quick aggregation.
    scalar_record = {
        k: v
        for k, v in summary.items()
        if not isinstance(v, (list, dict))
    }
    pd.DataFrame([scalar_record]).to_parquet(out_parquet, index=False)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fit the H2.1 mixture model to one synthetic replicate."
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--cell-id", required=True, type=str)
    parser.add_argument("--replicate", required=True, type=int)
    parser.add_argument("--n-draws", type=int, default=DEFAULT_N_DRAWS)
    parser.add_argument("--n-tune", type=int, default=DEFAULT_N_TUNE)
    parser.add_argument("--n-chains", type=int, default=DEFAULT_N_CHAINS)
    parser.add_argument(
        "--target-accept", type=float, default=DEFAULT_TARGET_ACCEPT
    )
    parser.add_argument("--cores", type=int, default=DEFAULT_CORES)
    parser.add_argument("--progressbar", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    design = synth_gen.load_design(args.design_json)
    env = synth_gen.make_envelope(design)
    tier_basis = synth_gen.build_tier_basis(design, env)

    summary = fit_replicate(
        cell_id=args.cell_id,
        replicate=args.replicate,
        output_root=args.output_root,
        design=design,
        tier_basis=tier_basis,
        n_draws=args.n_draws,
        n_tune=args.n_tune,
        n_chains=args.n_chains,
        target_accept=args.target_accept,
        cores=args.cores,
        progressbar=args.progressbar,
    )
    print(f"[02-fit] cell {args.cell_id}  replicate {args.replicate}")
    print(
        f"[02-fit]   alpha: true={summary['alpha_true']:.3f}  "
        f"median={summary['alpha_median']:.3f}  "
        f"CI=[{summary['alpha_ci_lo']:.3f}, {summary['alpha_ci_hi']:.3f}]  "
        f"covered={summary['alpha_covered_95ci']}"
    )
    print(
        f"[02-fit]   p_gen Pearson r vs truth = "
        f"{summary['pearson_r_pgen']:.4f}  W1 = "
        f"{summary['wasserstein_1_pgen']:.3f}"
    )
    print(
        f"[02-fit]   max R-hat = {summary['max_rhat']:.4f}  "
        f"min ESS_bulk = {summary['min_ess_bulk']:.0f}  "
        f"divergences = {summary['n_divergences']}  "
        f"convergence_pass = {summary['convergence_pass']}"
    )
    print(f"[02-fit]   fit_seconds = {summary['fit_seconds']:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
