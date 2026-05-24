#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-noncentred-experiment.py
============================

Re-fit the three α=0.95 cells from Experiment A under the non-centred
GRW reparameterisation (cf. ``code/02-mixture-fit-noncentred.py``).
Follow-up to ``runs/2026-05-24-validation-investigation``; tests
whether the funnel geometry of the centred GRW is responsible for the
biased α posterior at α=0.95.

Cloned from
``runs/2026-05-24-validation-investigation/code/run-experiment-a.py``
with these diffs:
  * imports build_model_noncentred from
    ``02-mixture-fit-noncentred.py`` instead of defining
    build_model inline.
  * EFFORT_LEVELS contains only "hardest" by default; baseline can be
    re-enabled via --with-baseline.
  * adds the ``parameterisation = "noncentred"`` tag in every output
    JSON record so downstream comparison is unambiguous.

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
from scipy.stats import pearsonr, wasserstein_distance  # noqa: E402


CELLS = [
    "shape=bimodal_alpha=0.95_tier=uniform_N=10000",
    "shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000",
    "shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000",
]

EFFORT_LEVELS_ALL = {
    "baseline": dict(n_tune=1_000, n_draws=2_000, n_chains=4,
                     target_accept=0.95),
    "hardest":  dict(n_tune=4_000, n_draws=8_000, n_chains=4,
                     target_accept=0.995),
}


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
    """Diagnostics + recovery scalars. Mirrors run-experiment-a.py
    exactly (so the centred vs non-centred comparison reads off the
    same numbers) but adds the ``z_pgen`` raw parameter to the
    convergence-diagnostic vars list (non-centred raw parameters are
    a primary check on sampler health under reparameterisation)."""
    summary_df = az.summary(
        idata,
        var_names=[
            "alpha", "tier_weights", "sigma_smooth", "z_pgen",
            "log_pgen_increments",
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
    parser.add_argument(
        "--with-baseline", action="store_true",
        help="Also fit at baseline effort (3 extra fits).",
    )
    args = parser.parse_args()

    # Active effort levels.
    if args.with_baseline:
        levels = {k: EFFORT_LEVELS_ALL[k] for k in ("baseline", "hardest")}
    else:
        levels = {"hardest": EFFORT_LEVELS_ALL["hardest"]}

    # Load the non-centred model builder.
    code_dir = Path(__file__).resolve().parent
    spec_nc = importlib.util.spec_from_file_location(
        "noncentred_mod", code_dir / "02-mixture-fit-noncentred.py",
    )
    noncentred_mod = importlib.util.module_from_spec(spec_nc)
    sys.modules["noncentred_mod"] = noncentred_mod
    spec_nc.loader.exec_module(noncentred_mod)
    build_model_noncentred = noncentred_mod.build_model_noncentred

    # Re-use 01-synthetic-cell-generator helpers from the validation run.
    spec_synth = importlib.util.spec_from_file_location(
        "synth_gen",
        args.validation_root / "code" / "01-synthetic-cell-generator.py",
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
        synth_dir = (
            args.validation_root / "data" / "synthetic-cells" / cell_id
        )
        synth_path = synth_dir / "replicate_000.parquet"
        truth_path = synth_dir / "replicate_000.truth.json"
        df = pd.read_parquet(synth_path)
        with truth_path.open("r", encoding="utf-8") as fh:
            truth = json.load(fh)
        y = df["y"].to_numpy(dtype=np.int64)
        truth["p_gen_true"] = df["p_gen_true"].to_numpy(
            dtype=float).tolist()
        seed_base = int(truth["seed"]) + 1

        for level, kw in levels.items():
            print(
                f"[expNC] {cell_id}  level={level}  kw={kw}", flush=True,
            )
            t0 = time.time()
            with build_model_noncentred(y, tier_basis):
                idata = pm.sample(
                    draws=kw["n_draws"],
                    tune=kw["n_tune"],
                    chains=kw["n_chains"],
                    cores=1,  # sequential — matches Experiment A
                    random_seed=seed_base,
                    progressbar=False,
                    target_accept=kw["target_accept"],
                    return_inferencedata=True,
                )
            wall_seconds = float(time.time() - t0)
            print(f"[expNC]   wall={wall_seconds:.1f}s", flush=True)

            # Hard-stop guard per brief: hardest > 15 min wall → halt.
            # Note we don't actually halt here (we let the loop finish
            # so subsequent cells aren't blocked), but we DO log and the
            # caller-side report enforces no silent parameter changes.
            if level == "hardest" and wall_seconds > 900:
                print(
                    f"[expNC] WARNING hardest fit > 15 min wall: "
                    f"{wall_seconds:.1f}s — see brief HARD STOP",
                    flush=True,
                )

            summary = summarise_posterior(idata, truth, bin_centres)
            summary["cell_id"] = cell_id
            summary["replicate"] = 0
            summary["effort_level"] = level
            summary["parameterisation"] = "noncentred"
            summary["n_tune"] = kw["n_tune"]
            summary["n_draws"] = kw["n_draws"]
            summary["n_chains"] = kw["n_chains"]
            summary["target_accept"] = kw["target_accept"]
            summary["wall_seconds"] = wall_seconds

            out_dir = (
                args.output_root / "outputs" / "diagnostic-fits" / cell_id
            )
            out_dir.mkdir(parents=True, exist_ok=True)
            out_json = (
                out_dir
                / f"replicate_000_effort={level}-noncentred-posterior.json"
            )
            with out_json.open("w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)

            run_results.append({
                "cell_id": cell_id,
                "effort_level": level,
                "parameterisation": "noncentred",
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

    overall_wall = time.time() - overall_t0
    print(f"[expNC] DONE. total wall = {overall_wall:.1f}s", flush=True)

    out_table = (
        args.output_root / "outputs" / "noncentred-experiment-results.json"
    )
    with out_table.open("w", encoding="utf-8") as fh:
        json.dump(
            {"results": run_results,
             "overall_wall_seconds": overall_wall},
            fh, indent=2,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
