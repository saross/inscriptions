#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-experiment-b.py
=====================

Experiment B — flat_baseline metric-mismatch diagnostic. For five
flat_baseline cells (one per α in {0.05, 0.30, 0.50, 0.70, 0.95}; all
N=10000, tier=uniform) we load the existing replicate_000 posterior and
compute:

  - variance of true p_gen
  - variance of recovered posterior-mean p_gen
  - max |recovered − true|
  - W-1 between true and recovered posterior-mean
  - distribution of per-draw Pearson r vs truth

The posterior JSONs persisted by the validation pipeline contain the
posterior-median p_gen but not the full draws — so we approximate the
per-draw Pearson r distribution using a synthesised plausible-draws
representation derived from the credible-interval extent. To capture the
true per-draw spread we re-load the draws from the saved JSON if
available; if not, we fall back to using the median + 95% CI band as a
deterministic posterior summary and note this in the report.

Inspection note: the validation pipeline persists ``pgen_median`` only —
not ``pgen_ci_lo/hi`` or full draws — so per-draw Pearson r will need to
be reconstructed by re-fitting if required. For Experiment B Shawn's
brief permits reading existing posteriors only; per-draw Pearson r is
therefore computed only over the SUMMARY information available
(posterior-mean), and we flag this in the report under "limitations".

Usage
-----
    source $VENV/bin/activate
    python run-experiment-b.py \\
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
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, wasserstein_distance

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


# ---------------------------------------------------------------------------
# Cells (per Shawn's brief).
# ---------------------------------------------------------------------------
CELLS = [
    ("0.05", "shape=flat_baseline_alpha=0.05_tier=uniform_N=10000"),
    ("0.30", "shape=flat_baseline_alpha=0.30_tier=uniform_N=10000"),
    ("0.50", "shape=flat_baseline_alpha=0.50_tier=uniform_N=10000"),
    ("0.70", "shape=flat_baseline_alpha=0.70_tier=uniform_N=10000"),
    ("0.95", "shape=flat_baseline_alpha=0.95_tier=uniform_N=10000"),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--validation-root", required=True, type=Path)
    parser.add_argument("--design-json", required=True, type=Path)
    args = parser.parse_args()

    # Import the validation synth-gen helpers for the envelope (bin_centres).
    code_dir = args.validation_root / "code"
    spec_synth = importlib.util.spec_from_file_location(
        "synth_gen", code_dir / "01-synthetic-cell-generator.py"
    )
    synth_gen = importlib.util.module_from_spec(spec_synth)
    sys.modules["synth_gen"] = synth_gen
    spec_synth.loader.exec_module(synth_gen)

    design = synth_gen.load_design(args.design_json)
    env = synth_gen.make_envelope(design)
    bin_centres = env.bin_centres

    results = []
    fig, axes = plt.subplots(5, 1, figsize=(10, 14), sharex=True)
    for (alpha_label, cell_id), ax in zip(CELLS, axes):
        # Load truth from the synthetic data parquet (the truth.json
        # doesn't carry p_gen_true — that's in the parquet).
        synth_path = (
            args.validation_root / "data" / "synthetic-cells" / cell_id
            / "replicate_000.parquet"
        )
        df_synth = pd.read_parquet(synth_path)
        truth_pgen = df_synth["p_gen_true"].to_numpy(dtype=float)

        # Load posterior.
        post_path = (
            args.validation_root / "outputs" / "cell-fits" / cell_id
            / "replicate_000-posterior.json"
        )
        with post_path.open("r", encoding="utf-8") as fh:
            posterior = json.load(fh)
        pgen_median = np.asarray(posterior["pgen_median"], dtype=float)

        var_true = float(np.var(truth_pgen))
        var_rec = float(np.var(pgen_median))
        max_abs = float(np.max(np.abs(pgen_median - truth_pgen)))
        w1 = float(wasserstein_distance(
            bin_centres, bin_centres, pgen_median, truth_pgen))
        try:
            pr, _ = pearsonr(pgen_median, truth_pgen)
            pearson_r = float(pr)
        except Exception:
            pearson_r = float("nan")

        # Per-draw Pearson r: not available from the saved summary JSON —
        # the validation pipeline does not persist full draws. We flag
        # this in the report. Here we record the median-based r only.

        results.append({
            "cell_id": cell_id,
            "alpha": alpha_label,
            "var_true_pgen": var_true,
            "var_recovered_mean_pgen": var_rec,
            "max_abs_dev": max_abs,
            "wasserstein_1": w1,
            "pearson_r_median": pearson_r,
            "alpha_true": posterior.get("alpha_true"),
            "alpha_median_posterior": posterior.get("alpha_median"),
            "alpha_covered_95ci": posterior.get("alpha_covered_95ci"),
            "convergence_pass": posterior.get("convergence_pass"),
            "n_divergences": posterior.get("n_divergences"),
            "max_rhat": posterior.get("max_rhat"),
            "min_ess_bulk": posterior.get("min_ess_bulk"),
        })

        # Plot panel: truth, recovered median, no CI (not persisted in
        # the existing summary JSONs).
        ax.plot(bin_centres, truth_pgen, color="black", linewidth=1.5,
                label="true p_gen")
        ax.plot(bin_centres, pgen_median, color="C0", linewidth=1.5,
                label="recovered (posterior-median)")
        ax.set_title(
            f"{cell_id}\n"
            f"var(true)={var_true:.2e}  var(rec)={var_rec:.2e}  "
            f"max|dev|={max_abs:.2e}  W1={w1:.3f}"
        )
        ax.set_ylabel("p_gen")
        ax.legend(loc="upper right", fontsize=8)
        ax.set_ylim(0, max(0.025, float(np.max(pgen_median)) * 1.15))
    axes[-1].set_xlabel("Bin centre (year AD; envelope 50 BC – 350 AD)")
    fig.suptitle(
        "Experiment B — flat_baseline recovery (5 cells, replicate_000)",
        fontsize=12, y=0.998,
    )
    fig.tight_layout()
    fig_path = args.output_root / "outputs" / "figures" / "experiment-b-flat-baseline-recovery.png"
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_path, dpi=150)
    plt.close(fig)

    out_table = args.output_root / "outputs" / "experiment-b-results.json"
    with out_table.open("w", encoding="utf-8") as fh:
        json.dump({"results": results}, fh, indent=2)
    print(f"[expB] wrote {fig_path}")
    print(f"[expB] wrote {out_table}")
    for r in results:
        print(
            f"[expB] α={r['alpha']}  "
            f"var(rec)={r['var_recovered_mean_pgen']:.3e}  "
            f"max|dev|={r['max_abs_dev']:.3e}  W1={r['wasserstein_1']:.3f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
