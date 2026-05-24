#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-experiment-followup-alpha-prior.py
======================================

Follow-up to Experiment A — α=0.95 prior-pull vs structural
unidentifiability diagnostic for the H2.1 recovery grid validation.

We re-fit the same 3 α=0.95 cells × 3 effort levels (baseline / harder
/ hardest) that Experiment A used, changing **one and only one thing**:
the prior on the mixture weight α. The production model and Experiment
A both use ``alpha ~ Beta(2, 2)``. This script uses
``alpha ~ Beta(1, 1)`` — mathematically equivalent to a Uniform(0, 1)
prior, which is the loosest prior that respects α ∈ (0, 1) as a
probability mass and is therefore the cleanest "remove the prior pull"
manipulation.

Hypothesis under test (from Shawn's brief, anchored on
2026-05-24-validation-investigation REPORT.md):

- If Δα ≡ α_posterior_mean(Beta(1,1)) − α_posterior_mean(Beta(2,2)) is
  large (≥ +0.10) and pushes the posterior toward truth (α_true = 0.95),
  then Experiment A's bias was substantially driven by **prior pull**
  (Beta(2,2) is symmetric and puts only ~5% mass above α=0.95). The fix
  may then be as cheap as re-specifying the prior.
- If Δα is small (< +0.05) the posterior is sitting where it sits
  regardless of the prior, confirming Experiment A's verdict of
  **structural model misspecification / partial unidentifiability**.

Critical-friend statistical confirmation
----------------------------------------
- Beta(1, 1) has PDF
      f(x; 1, 1) = Γ(2)/(Γ(1)·Γ(1)) · x^0 · (1−x)^0 = 1  for x ∈ (0, 1)
  i.e., it is exactly the Uniform(0, 1) distribution. The Beta family
  is the natural conjugate parameterisation for a probability on (0, 1)
  and so we keep it for code-symmetry with the production model — only
  the (a, b) shape parameters change from (2, 2) to (1, 1).
- Every other component of the model is **unchanged** vs the production
  ``02-cell-mixture-fit.py`` and Experiment A's ``run-experiment-a.py``:
  - ``sigma_smooth ~ HalfNormal(1)``
  - ``log_pgen_increments ~ Normal(0, sigma_smooth)`` with shape
    ``(n_bins − 1,)``, anchored at log p(bin 0) = 0
  - ``tier_weights ~ Dirichlet([1, 1, 1])`` (uniform on the 3-simplex)
  - ``tier_basis`` matrix loaded from the design.json (3 tiers × 80
    5-year bins, AD 1–400)
  - ``Multinomial(N, α·p_conv + (1−α)·p_gen)`` likelihood
- We do NOT change the sampler (default pymc NUTS, no numpyro), the
  seed strategy (truth["seed"]+1, matching Experiment A), or any other
  knob. This is a pure prior-swap.

Usage
-----
    source /home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/activate
    export TMPDIR=/home/shawn/cc-scratch/inscriptions-recovery-grid/pytensor-tmp
    export PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"
    export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
    export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1
    taskset -c 0-5 python run-experiment-followup-alpha-prior.py \\
        --output-root /home/shawn/cc-scratch/.../2026-05-24-followup-alpha-prior \\
        --validation-root /home/shawn/cc-scratch/.../2026-05-22-recovery-grid-validation \\
        --design-json /home/shawn/cc-scratch/.../2026-05-22-recovery-grid-design/design.json

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-24, on Shawn's brief.
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
# Cells and effort levels — IDENTICAL to Experiment A so results are paired.
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

# Hard-stop sanity bound on per-fit wall (Shawn's brief: hardest must
# finish within 15 min; we set the script-level guard at 20 min to leave
# slack for the harder/baseline fits and only halt on truly pathological
# stalls).
HARDSTOP_SECONDS = 1200.0


# ---------------------------------------------------------------------------
# Model — IDENTICAL to Experiment A except alpha ~ Beta(1, 1).
# ---------------------------------------------------------------------------
def build_model_uniform_alpha(
    y: np.ndarray,
    tier_basis: np.ndarray,
) -> pm.Model:
    """Mixture model with Uniform(0,1) prior on α.

    Differs from production ``02-cell-mixture-fit.py`` and Experiment A
    in EXACTLY ONE LINE: ``alpha ~ Beta(1, 1)`` instead of
    ``alpha ~ Beta(2, 2)``. All other priors, the likelihood, and the
    parameterisation are bit-identical (modulo NumPy/PyTensor float
    determinism).
    """
    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    with pm.Model() as model:
        # ★ THE ONLY CHANGE vs Experiment A ★
        # Production / Experiment A: pm.Beta("alpha", 2.0, 2.0)
        # Here (Uniform-on-α diagnostic):
        alpha = pm.Beta("alpha", 1.0, 1.0)
        # ★ END CHANGE ★
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
    """Compute diagnostics + recovery scalars. Mirrors Experiment A
    exactly so the two posteriors can be diffed field-for-field."""
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
    pearson_r_mean, _ = pearsonr(pgen_mean, truth_pgen)
    pearson_r_median, _ = pearsonr(pgen_median, truth_pgen)
    w1_mean = float(wasserstein_distance(
        bin_centres, bin_centres, pgen_mean, truth_pgen))
    w1_median = float(wasserstein_distance(
        bin_centres, bin_centres, pgen_median, truth_pgen))

    return {
        "alpha_prior": "Beta(1, 1) [Uniform(0, 1)]",
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
    halted = False

    for cell_id in CELLS:
        if halted:
            break
        synth_dir = args.validation_root / "data" / "synthetic-cells" / cell_id
        synth_path = synth_dir / "replicate_000.parquet"
        truth_path = synth_dir / "replicate_000.truth.json"
        df = pd.read_parquet(synth_path)
        with truth_path.open("r", encoding="utf-8") as fh:
            truth = json.load(fh)
        y = df["y"].to_numpy(dtype=np.int64)
        truth["p_gen_true"] = df["p_gen_true"].to_numpy(dtype=float).tolist()
        # Match Experiment A's seed convention precisely.
        seed_base = int(truth["seed"]) + 1

        for level, kw in EFFORT_LEVELS.items():
            print(
                f"[followup] {cell_id}  level={level}  kw={kw}",
                flush=True,
            )
            t0 = time.time()
            with build_model_uniform_alpha(y, tier_basis):
                idata = pm.sample(
                    draws=kw["n_draws"],
                    tune=kw["n_tune"],
                    chains=kw["n_chains"],
                    cores=1,  # sequential within fit — matches Experiment A
                    random_seed=seed_base,
                    progressbar=False,
                    target_accept=kw["target_accept"],
                    return_inferencedata=True,
                )
            wall_seconds = float(time.time() - t0)
            print(f"[followup]   wall={wall_seconds:.1f}s", flush=True)

            summary = summarise_posterior(idata, truth, bin_centres)
            summary["cell_id"] = cell_id
            summary["replicate"] = 0
            summary["effort_level"] = level
            summary["n_tune"] = kw["n_tune"]
            summary["n_draws"] = kw["n_draws"]
            summary["n_chains"] = kw["n_chains"]
            summary["target_accept"] = kw["target_accept"]
            summary["wall_seconds"] = wall_seconds

            out_dir = args.output_root / "outputs" / "diagnostic-fits" / cell_id
            out_dir.mkdir(parents=True, exist_ok=True)
            out_json = out_dir / f"replicate_000_effort={level}-posterior.json"
            with out_json.open("w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)
            print(f"[followup]   wrote {out_json}", flush=True)

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
                "alpha_ci_lo": summary["alpha_ci_lo"],
                "alpha_ci_hi": summary["alpha_ci_hi"],
                "pearson_r_mean": summary["pearson_r_pgen_mean"],
                "wasserstein_1_mean": summary["wasserstein_1_pgen_mean"],
            })

            # Hard-stop guard (Shawn's brief).
            if wall_seconds > HARDSTOP_SECONDS:
                print(
                    f"[followup] HARD-STOP: fit exceeded "
                    f"{HARDSTOP_SECONDS:.0f}s — halting and reporting.",
                    flush=True,
                )
                halted = True
                break

    overall_wall = time.time() - overall_t0
    print(f"[followup] DONE. total wall = {overall_wall:.1f}s", flush=True)

    out_table = args.output_root / "outputs" / "followup-results.json"
    out_table.parent.mkdir(parents=True, exist_ok=True)
    with out_table.open("w", encoding="utf-8") as fh:
        json.dump({
            "results": run_results,
            "overall_wall_seconds": overall_wall,
            "halted_early": halted,
            "alpha_prior": "Beta(1, 1) [Uniform(0, 1)]",
        }, fh, indent=2)
    return 0 if not halted else 4


if __name__ == "__main__":
    sys.exit(main())
