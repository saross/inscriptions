#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fit.py
======

Per-replicate fitter for the 2026-05-26 two-unit recovery-grid
re-simulation. Loads the synthetic replicate, builds the F1+F3 mixture
model (via ``cell_lib.build_model_f1_f3``), runs NUTS, and writes a
per-replicate posterior-summary JSON + parquet matching the 2026-05-22
schema.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import json
import os
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Suppress noisy banners before importing pymc / arviz.
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN,allow_gc=False")

import arviz as az  # noqa: E402
import pymc as pm  # noqa: E402
from scipy.stats import pearsonr, wasserstein_distance  # noqa: E402

from cell_lib import Envelope, build_model_f1_f3  # noqa: E402


# NUTS settings (locked per spec §3.1).
DEFAULT_N_DRAWS = 2_000
DEFAULT_N_TUNE = 1_000
DEFAULT_N_CHAINS = 4
DEFAULT_TARGET_ACCEPT = 0.95
DEFAULT_CORES = 1

# Convergence gates (prereg §3 line 208).
RHAT_GATE = 1.01
ESS_GATE = 400


def _flat_var(idata: az.InferenceData, name: str) -> np.ndarray:
    """Return the flat (chain*draw, ...) draws array for a posterior var."""
    arr = idata.posterior[name].values
    if arr.ndim == 2:
        return arr.reshape(-1)
    return arr.reshape(-1, *arr.shape[2:])


def summarise_posterior(
    idata: az.InferenceData,
    truth: dict[str, Any],
    bin_centres: np.ndarray,
) -> dict[str, Any]:
    """Compute the per-replicate scalars persisted by the fitter."""
    summary_df = az.summary(
        idata,
        var_names=["alpha", "tier_weights", "sigma_smooth", "z_pgen"],
        round_to="none",
    )
    max_rhat = float(summary_df["r_hat"].max())
    min_ess_bulk = float(summary_df["ess_bulk"].min())
    min_ess_tail = float(summary_df["ess_tail"].min())
    n_divergences = int(idata.sample_stats.diverging.values.sum())

    alpha_samples = _flat_var(idata, "alpha")
    alpha_lo, alpha_hi = np.percentile(alpha_samples, [2.5, 97.5])
    alpha_med = float(np.median(alpha_samples))
    alpha_mean = float(np.mean(alpha_samples))
    alpha_true = float(truth["alpha_true"])
    alpha_covered = bool(alpha_lo <= alpha_true <= alpha_hi)

    pgen_draws = _flat_var(idata, "p_gen")
    pgen_median = np.median(pgen_draws, axis=0)
    truth_pgen = np.asarray(truth["p_gen_true"], dtype=float)
    pearson_r, _ = pearsonr(pgen_median, truth_pgen)
    w1 = float(
        wasserstein_distance(bin_centres, bin_centres, pgen_median, truth_pgen)
    )

    tier_draws = _flat_var(idata, "tier_weights")
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
        "alpha_mean": alpha_mean,
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
        "min_ess_tail": min_ess_tail,
        "n_divergences": n_divergences,
        "convergence_pass": convergence_pass,
    }


def fit_replicate(
    cell_id: str,
    replicate: int,
    output_root: Path,
    env: Envelope,
    tier_basis: np.ndarray,
    n_draws: int = DEFAULT_N_DRAWS,
    n_tune: int = DEFAULT_N_TUNE,
    n_chains: int = DEFAULT_N_CHAINS,
    target_accept: float = DEFAULT_TARGET_ACCEPT,
    cores: int = DEFAULT_CORES,
    progressbar: bool = False,
) -> dict[str, Any]:
    """Fit one replicate and persist the per-replicate posterior summary.

    The model used is ``build_model_f1_f3`` (F1: Beta(1, 1) prior on
    alpha; F3: non-centred GRW). Identical for both grids.
    """
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

    model = build_model_f1_f3(y, tier_basis)
    t0 = time.time()
    # Fit seed: data_seed + 1 (distinct from data-gen seed).
    fit_seed = int(truth["data_seed"]) + 1
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
    summary["unit"] = truth["unit"]
    summary["fit_seconds"] = fit_seconds
    summary["n_draws"] = int(n_draws)
    summary["n_tune"] = int(n_tune)
    summary["n_chains"] = int(n_chains)
    summary["target_accept"] = float(target_accept)
    summary["cores"] = int(cores)

    out_dir = output_root / "outputs" / "cell-fits" / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / f"replicate_{replicate:03d}-posterior.json"
    out_parquet = out_dir / f"replicate_{replicate:03d}-posterior.parquet"
    with out_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    scalar_record = {
        k: v
        for k, v in summary.items()
        if not isinstance(v, (list, dict))
    }
    pd.DataFrame([scalar_record]).to_parquet(out_parquet, index=False)
    return summary
