#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot-followup-alpha-prior.py
============================

Render the three comparison figures for the
``2026-05-24-followup-alpha-prior`` follow-up to Experiment A. One PNG
per cell. Each figure has three rows (baseline / harder / hardest).
Each row shows:

- the true p_gen (black line)
- the recovered posterior-mean p_gen under the **uniform** α prior
  (this run; blue line with 95% credible band)
- the recovered posterior-mean p_gen under the **default Beta(2,2)** α
  prior (Experiment A; orange line, no band — for visual comparison
  only)

The figure title and per-row label include the posterior-mean α for
both priors and the truth value (0.95 in every row), so a reader can
see at a glance whether the uniform prior moved α toward truth.

Usage
-----
    source $VENV/bin/activate
    python plot-followup-alpha-prior.py \\
        --output-root /home/shawn/cc-scratch/.../2026-05-24-followup-alpha-prior \\
        --validation-root /home/shawn/cc-scratch/.../2026-05-22-recovery-grid-validation \\
        --expA-root /home/shawn/cc-scratch/.../2026-05-24-validation-investigation \\
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


CELLS = [
    "shape=bimodal_alpha=0.95_tier=uniform_N=10000",
    "shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000",
    "shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000",
]

EFFORT_ORDER = ["baseline", "harder", "hardest"]


def _load_posterior(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--validation-root", required=True, type=Path)
    parser.add_argument("--expA-root", required=True, type=Path)
    parser.add_argument("--design-json", required=True, type=Path)
    args = parser.parse_args()

    # Bin centres from the design helpers.
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

    fig_dir = args.output_root / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    for cell_id in CELLS:
        # Truth.
        synth_dir = args.validation_root / "data" / "synthetic-cells" / cell_id
        df = pd.read_parquet(synth_dir / "replicate_000.parquet")
        truth_pgen = df["p_gen_true"].to_numpy(dtype=float)

        fig, axes = plt.subplots(
            3, 1, figsize=(9, 9), sharex=True, sharey=True
        )
        for ax, level in zip(axes, EFFORT_ORDER):
            uni_path = (
                args.output_root / "outputs" / "diagnostic-fits" / cell_id
                / f"replicate_000_effort={level}-posterior.json"
            )
            def_path = (
                args.expA_root / "outputs" / "diagnostic-fits" / cell_id
                / f"replicate_000_effort={level}-posterior.json"
            )
            uni = _load_posterior(uni_path)
            default = _load_posterior(def_path)

            uni_mean = np.asarray(uni["pgen_mean"], dtype=float)
            uni_lo = np.asarray(uni["pgen_ci_lo"], dtype=float)
            uni_hi = np.asarray(uni["pgen_ci_hi"], dtype=float)
            def_mean = np.asarray(default["pgen_mean"], dtype=float)

            ax.plot(bin_centres, truth_pgen, color="black", lw=1.6,
                    label="truth (p_gen_true)")
            ax.fill_between(bin_centres, uni_lo, uni_hi,
                            color="tab:blue", alpha=0.18,
                            label="uniform-α 95% CI")
            ax.plot(bin_centres, uni_mean, color="tab:blue", lw=1.4,
                    label=f"uniform α ~ Beta(1,1)  α̂={uni['alpha_mean']:.3f}")
            ax.plot(bin_centres, def_mean, color="tab:orange", lw=1.2,
                    linestyle="--",
                    label=f"default α ~ Beta(2,2)  α̂={default['alpha_mean']:.3f}")
            ax.set_title(
                f"{level}  (n_tune={uni['n_tune']}, n_draws={uni['n_draws']}, "
                f"target_accept={uni['target_accept']}, "
                f"div={uni['n_divergences']}, R-hat={uni['max_rhat']:.3f})",
                fontsize=10,
            )
            ax.set_ylabel("p_gen")
            ax.legend(fontsize=8, loc="upper right")
            ax.grid(True, alpha=0.3)

        axes[-1].set_xlabel("year (bin centre)")
        # Cell title gives the truth and a quick Δα across rows.
        rows_delta = []
        for level in EFFORT_ORDER:
            uni = _load_posterior(
                args.output_root / "outputs" / "diagnostic-fits" / cell_id
                / f"replicate_000_effort={level}-posterior.json"
            )
            default = _load_posterior(
                args.expA_root / "outputs" / "diagnostic-fits" / cell_id
                / f"replicate_000_effort={level}-posterior.json"
            )
            rows_delta.append(uni["alpha_mean"] - default["alpha_mean"])
        fig.suptitle(
            f"{cell_id}\n"
            f"truth α=0.95  |  Δα(uniform − default) at "
            f"baseline/harder/hardest = "
            f"{rows_delta[0]:+.3f} / {rows_delta[1]:+.3f} / "
            f"{rows_delta[2]:+.3f}",
            fontsize=11,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        # Trim cell id for filename: strip "shape=" / "alpha=" markers.
        slug = (
            cell_id
            .replace("shape=", "")
            .replace("alpha=", "a")
            .replace("tier=", "")
            .replace("N=", "N")
        )
        out_png = fig_dir / f"followup-alpha-prior-{slug}.png"
        fig.savefig(out_png, dpi=150)
        plt.close(fig)
        print(f"[plot] wrote {out_png}", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
