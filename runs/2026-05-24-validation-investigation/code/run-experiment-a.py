#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-experiment-a.py
====================

Experiment A — α=0.95 sampler-pathology diagnostic for the H2.1 recovery
grid validation. For three representative α=0.95 cells (one each from
three distinct shapes; all N=10000) we re-fit replicate_000 under three
sampling-effort settings (baseline / harder / hardest) and record full
diagnostics. Posterior JSONs land in
``outputs/diagnostic-fits/<cell_id>/replicate_000_effort=<level>-posterior.json``.

This script is meant to be run via the project's venv on sapphire with
all the TMPDIR / single-threaded-BLAS / PYTENSOR_FLAGS env vars exported
in the calling shell. It honours that environment without re-setting it.

Usage
-----
    source $VENV/bin/activate
    export TMPDIR=...
    export PYTENSOR_FLAGS=...
    # (all the single-threaded-BLAS exports)
    python run-experiment-a.py \\
        --output-root /home/shawn/cc-scratch/.../2026-05-24-validation-investigation \\
        --validation-root /home/shawn/cc-scratch/.../2026-05-22-recovery-grid-validation \\
        --design-json /home/shawn/cc-scratch/.../2026-05-22-recovery-grid-design/design.json

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-24.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import arviz as az  # noqa: E402
import pymc as pm  # noqa: E402
import pytensor.tensor as pt  # noqa: E402
from scipy.stats import pearsonr, wasserstein_distance  # noqa: E402


# ---------------------------------------------------------------------------
# Cells and effort levels (per Shawn's brief).
# ---------------------------------------------------------------------------
CELLS = [
    "shape=bimodal_alpha=0.95_tier=uniform_N=10000",
    "shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000",
    "shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000",
]

EFFORT_LEVELS = {
    "baseline": dict(n_tune=1_000, n_draws=2_000, n_chains=4,
                     target_accept=0.95),
    "harder":   dict(n_tune=2_000, n_draws=4_000, n_chains=4,
                     target_accept=0.99),
    "hardest":  dict(n_tune=4_000, n_draws=8_000, n_chains=4,
                     target_accept=0.995),
}


# ---------------------------------------------------------------------------
# Helpers — model + summariser copied from the original validation code so
# behaviour matches exactly (build_model, summarise_posterior).
# ---------------------------------------------------------------------------
def build_model(y: np.ndarray, tier_basis: np.ndarray) -> pm.Model:
    """Mixture model identical to runs/.../code/02-cell-mixture-fit.py."""
    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    with pm.Model() as model:
        alpha = pm.Beta("alpha", 2.0, 2.0)
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float)
        )
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis)
        )
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
        log_pgen_increments = pm.Normal(
            "log_pgen_increments", mu=0.0, sigma=sigma_smooth,
            shape=n_bins - 1,
        )
        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)]
        )
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)
    return model


def _flat_var(idata: az.InferenceData, name: str) -> np.ndarray:
    arr = idata.posterior[name].values
    if arr.ndim == 2:
        return arr.reshape(-1)
    return arr.reshape(-1, *arr.shape[2:])


def summarise_posterior(
    idata: az.InferenceData,
    truth: dict[str, Any],
    bin_centres: np.ndarray,
) -> dict[str, Any]:
    """Compute diagnostics + recovery scalars. Mirrors original code but
    adds ess_tail and posterior-mean alpha (Shawn asks for posterior-mean
    α, not just median)."""
    summary_df = az.summary(
        idata,
        var_names=[
            "alpha", "tier_weights", "sigma_smooth", "log_pgen_increments",
        ],
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
    pgen_mean = np.mean(pgen_draws, axis=0)
    pgen_median = np.median(pgen_draws, axis=0)
    pgen_lo = np.percentile(pgen_draws, 2.5, axis=0)
    pgen_hi = np.percentile(pgen_draws, 97.5, axis=0)
    truth_pgen = np.asarray(truth["p_gen_true"], dtype=float)
    # Pearson r against truth, computed on posterior-mean p_gen (the
    # brief says "posterior-mean α vs true α, Pearson r vs truth").
    pearson_r_mean, _ = pearsonr(pgen_mean, truth_pgen)
    pearson_r_median, _ = pearsonr(pgen_median, truth_pgen)
    w1_mean = float(wasserstein_distance(
        bin_centres, bin_centres, pgen_mean, truth_pgen))
    w1_median = float(wasserstein_distance(
        bin_centres, bin_centres, pgen_median, truth_pgen))

    return {
        "alpha_true": alpha_true,
        "alpha_median": alpha_med,
        "alpha_mean": alpha_mean,
        "alpha_ci_lo": float(alpha_lo),
        "alpha_ci_hi": float(alpha_hi),
        "alpha_covered_95ci": alpha_covered,
        "pearson_r_pgen_mean": float(pearson_r_mean),
        "pearson_r_pgen_median": float(pearson_r_median),
        "wasserstein_1_pgen_mean": w1_mean,
        "wasserstein_1_pgen_median": w1_median,
        "pgen_mean": pgen_mean.tolist(),
        "pgen_median": pgen_median.tolist(),
        "pgen_ci_lo": pgen_lo.tolist(),
        "pgen_ci_hi": pgen_hi.tolist(),
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "min_ess_tail": min_ess_tail,
        "n_divergences": n_divergences,
    }


# ---------------------------------------------------------------------------
# Main routine
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--validation-root", required=True, type=Path)
    parser.add_argument("--design-json", required=True, type=Path)
    args = parser.parse_args()

    # Re-use 01-synthetic-cell-generator helpers from the validation run.
    code_dir = args.validation_root / "code"
    spec_synth = importlib.util.spec_from_file_location(
        "synth_gen", code_dir / "01-synthetic-cell-generator.py"
    )
    synth_gen = importlib.util.module_from_spec(spec_synth)
    sys.modules["synth_gen"] = synth_gen
    spec_synth.loader.exec_module(synth_gen)

    design = synth_gen.load_design(args.design_json)
    env = synth_gen.make_envelope(design)
    tier_basis = synth_gen.build_tier_basis(design, env)
    bin_centres = env.bin_centres

    run_results: list[dict[str, Any]] = []
    overall_t0 = time.time()
    for cell_id in CELLS:
        # Load synthetic data + truth for replicate_000.
        synth_dir = args.validation_root / "data" / "synthetic-cells" / cell_id
        synth_path = synth_dir / "replicate_000.parquet"
        truth_path = synth_dir / "replicate_000.truth.json"
        df = pd.read_parquet(synth_path)
        with truth_path.open("r", encoding="utf-8") as fh:
            truth = json.load(fh)
        y = df["y"].to_numpy(dtype=np.int64)
        truth["p_gen_true"] = df["p_gen_true"].to_numpy(dtype=float).tolist()
        seed_base = int(truth["seed"]) + 1

        for level, kw in EFFORT_LEVELS.items():
            print(f"[expA] {cell_id}  level={level}  kw={kw}", flush=True)
            t0 = time.time()
            with build_model(y, tier_basis):
                idata = pm.sample(
                    draws=kw["n_draws"],
                    tune=kw["n_tune"],
                    chains=kw["n_chains"],
                    cores=1,  # sequential — matches original grid run
                    random_seed=seed_base,
                    progressbar=False,
                    target_accept=kw["target_accept"],
                    return_inferencedata=True,
                )
            wall_seconds = float(time.time() - t0)
            print(f"[expA]   wall={wall_seconds:.1f}s", flush=True)

            summary = summarise_posterior(idata, truth, bin_centres)
            summary["cell_id"] = cell_id
            summary["replicate"] = 0
            summary["effort_level"] = level
            summary["n_tune"] = kw["n_tune"]
            summary["n_draws"] = kw["n_draws"]
            summary["n_chains"] = kw["n_chains"]
            summary["target_accept"] = kw["target_accept"]
            summary["wall_seconds"] = wall_seconds

            # Persist.
            out_dir = args.output_root / "outputs" / "diagnostic-fits" / cell_id
            out_dir.mkdir(parents=True, exist_ok=True)
            out_json = out_dir / f"replicate_000_effort={level}-posterior.json"
            with out_json.open("w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)

            run_results.append({
                "cell_id": cell_id,
                "effort_level": level,
                "n_tune": kw["n_tune"],
                "n_draws": kw["n_draws"],
                "target_accept": kw["target_accept"],
                "wall_seconds": wall_seconds,
                "n_divergences": summary["n_divergences"],
                "max_rhat": summary["max_rhat"],
                "min_ess_bulk": summary["min_ess_bulk"],
                "min_ess_tail": summary["min_ess_tail"],
                "alpha_true": summary["alpha_true"],
                "alpha_mean": summary["alpha_mean"],
                "alpha_median": summary["alpha_median"],
                "pearson_r_mean": summary["pearson_r_pgen_mean"],
                "wasserstein_1_mean": summary["wasserstein_1_pgen_mean"],
            })

            # Hard-stop guard: brief says "if hardest fit takes >15 min wall,
            # halt and report" — but here we just continue (caller monitors).
            if wall_seconds > 1800:
                print(
                    f"[expA] WARNING: fit exceeded 30 minutes wall — see brief",
                    flush=True,
                )

    overall_wall = time.time() - overall_t0
    print(f"[expA] DONE. total wall = {overall_wall:.1f}s", flush=True)

    # Persist the aggregated results table for the report.
    out_table = args.output_root / "outputs" / "experiment-a-results.json"
    with out_table.open("w", encoding="utf-8") as fh:
        json.dump({"results": run_results, "overall_wall_seconds":
                   overall_wall}, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
