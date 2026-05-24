#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot-experiment-a.py
======================

Build the three Experiment A diagnostic figures: per cell, a 3-row stack
of recovered posterior-mean p_gen against truth (one row per effort
level: baseline, harder, hardest).

Usage
-----
    source $VENV/bin/activate
    python plot-experiment-a.py \\
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


CELLS = [
    "shape=bimodal_alpha=0.95_tier=uniform_N=10000",
    "shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000",
    "shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000",
]
LEVELS = ["baseline", "harder", "hardest"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--validation-root", required=True, type=Path)
    parser.add_argument("--design-json", required=True, type=Path)
    args = parser.parse_args()

    code_dir = args.validation_root / "code"
    spec = importlib.util.spec_from_file_location(
        "synth_gen", code_dir / "01-synthetic-cell-generator.py"
    )
    synth_gen = importlib.util.module_from_spec(spec)
    sys.modules["synth_gen"] = synth_gen
    spec.loader.exec_module(synth_gen)
    design = synth_gen.load_design(args.design_json)
    env = synth_gen.make_envelope(design)
    bin_centres = env.bin_centres

    for cell_id in CELLS:
        # Truth.
        synth_df = pd.read_parquet(
            args.validation_root / "data" / "synthetic-cells" / cell_id
            / "replicate_000.parquet"
        )
        truth_pgen = synth_df["p_gen_true"].to_numpy(dtype=float)

        fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True, sharey=True)
        for level, ax in zip(LEVELS, axes):
            post_path = (
                args.output_root / "outputs" / "diagnostic-fits" / cell_id
                / f"replicate_000_effort={level}-posterior.json"
            )
            with post_path.open("r", encoding="utf-8") as fh:
                d = json.load(fh)
            pgen_mean = np.asarray(d["pgen_mean"], dtype=float)
            pgen_lo = np.asarray(d["pgen_ci_lo"], dtype=float)
            pgen_hi = np.asarray(d["pgen_ci_hi"], dtype=float)

            ax.fill_between(
                bin_centres, pgen_lo, pgen_hi, alpha=0.25,
                color="C0", label="recovered 95% CI",
            )
            ax.plot(bin_centres, pgen_mean, color="C0", linewidth=1.6,
                    label="recovered (posterior-mean)")
            ax.plot(bin_centres, truth_pgen, color="black", linewidth=1.5,
                    label="true p_gen")
            ax.set_title(
                f"{level}: tune={d['n_tune']} draws={d['n_draws']} "
                f"ta={d['target_accept']} | "
                f"div={d['n_divergences']}  R-hat={d['max_rhat']:.3f}  "
                f"min ESS_bulk={d['min_ess_bulk']:.0f}  "
                f"wall={d['wall_seconds']:.0f}s\n"
                f"α_true={d['alpha_true']:.2f}  "
                f"α_mean={d['alpha_mean']:.3f}  "
                f"r(mean,truth)={d['pearson_r_pgen_mean']:.3f}  "
                f"W1={d['wasserstein_1_pgen_mean']:.2f}",
                fontsize=9,
            )
            ax.set_ylabel("p_gen")
            ax.legend(loc="upper right", fontsize=8)
        axes[-1].set_xlabel("Bin centre (year AD; envelope 50 BC – 350 AD)")
        fig.suptitle(
            f"Experiment A — {cell_id}\nposterior-mean p_gen vs truth at "
            "three sampling-effort levels",
            fontsize=11,
        )
        fig.tight_layout()
        # Filename-safe cell label
        safe_label = (
            cell_id.replace("shape=", "")
            .replace("_tier=", "_")
            .replace("_alpha=", "_a")
            .replace("_N=", "_N")
        )
        fig_path = (
            args.output_root / "outputs" / "figures"
            / f"experiment-a-{safe_label}.png"
        )
        fig.savefig(fig_path, dpi=150)
        plt.close(fig)
        print(f"[expA-plot] wrote {fig_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
