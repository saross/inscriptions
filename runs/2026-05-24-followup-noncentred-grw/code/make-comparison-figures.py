#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make-comparison-figures.py
==========================

Produce three side-by-side figures (one per α=0.95 cell) showing
recovered p_gen under non-centred GRW vs centred GRW at the hardest
effort, plus the truth. Reads:

  * non-centred posteriors from
    ``outputs/diagnostic-fits/<cell_id>/replicate_000_effort=hardest-noncentred-posterior.json``
  * centred posteriors from the prior Experiment A run at
    ``../2026-05-24-validation-investigation/outputs/diagnostic-fits/<cell_id>/replicate_000_effort=hardest-posterior.json``
  * truth from
    ``../2026-05-22-recovery-grid-validation/data/synthetic-cells/<cell_id>/replicate_000.truth.json``
    and the parquet sibling (for p_gen_true).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


ROOT = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-24-followup-noncentred-grw"
)
EXPA_ROOT = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-24-validation-investigation"
)
VALIDATION_ROOT = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-22-recovery-grid-validation"
)
DESIGN_JSON = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-22-recovery-grid-design/design.json"
)
CELLS = [
    "shape=bimodal_alpha=0.95_tier=uniform_N=10000",
    "shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000",
    "shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000",
]

# Load envelope (bin centres) via synth_gen.
spec_synth = importlib.util.spec_from_file_location(
    "synth_gen", VALIDATION_ROOT / "code" / "01-synthetic-cell-generator.py",
)
synth_gen = importlib.util.module_from_spec(spec_synth)
sys.modules["synth_gen"] = synth_gen
spec_synth.loader.exec_module(synth_gen)
design = synth_gen.load_design(DESIGN_JSON)
env = synth_gen.make_envelope(design)
bin_centres = env.bin_centres


for cell_id in CELLS:
    # Non-centred (this run).
    nc_path = (
        ROOT / "outputs" / "diagnostic-fits" / cell_id
        / "replicate_000_effort=hardest-noncentred-posterior.json"
    )
    with nc_path.open("r", encoding="utf-8") as fh:
        nc = json.load(fh)
    pgen_nc_mean = np.asarray(nc["pgen_mean"])
    pgen_nc_lo = np.asarray(nc["pgen_ci_lo"])
    pgen_nc_hi = np.asarray(nc["pgen_ci_hi"])

    # Centred (Experiment A hardest).
    c_path = (
        EXPA_ROOT / "outputs" / "diagnostic-fits" / cell_id
        / "replicate_000_effort=hardest-posterior.json"
    )
    with c_path.open("r", encoding="utf-8") as fh:
        c = json.load(fh)
    pgen_c_mean = np.asarray(c["pgen_mean"])
    pgen_c_lo = np.asarray(c["pgen_ci_lo"])
    pgen_c_hi = np.asarray(c["pgen_ci_hi"])

    # Truth.
    synth_dir = VALIDATION_ROOT / "data" / "synthetic-cells" / cell_id
    df = pd.read_parquet(synth_dir / "replicate_000.parquet")
    truth_pgen = df["p_gen_true"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    ax.plot(
        bin_centres, truth_pgen, "k-", lw=2.0, label="truth p_gen",
    )
    ax.plot(
        bin_centres, pgen_c_mean, color="tab:red", lw=1.2,
        label=(
            f"centred GRW posterior mean "
            f"(α̂={c['alpha_mean']:.3f}, r={c['pearson_r_pgen_mean']:.3f})"
        ),
    )
    ax.fill_between(
        bin_centres, pgen_c_lo, pgen_c_hi,
        color="tab:red", alpha=0.12,
        label="centred 95% CI",
    )
    ax.plot(
        bin_centres, pgen_nc_mean, color="tab:blue", lw=1.2,
        label=(
            f"non-centred GRW posterior mean "
            f"(α̂={nc['alpha_mean']:.3f}, r={nc['pearson_r_pgen_mean']:.3f})"
        ),
    )
    ax.fill_between(
        bin_centres, pgen_nc_lo, pgen_nc_hi,
        color="tab:blue", alpha=0.12,
        label="non-centred 95% CI",
    )
    short = cell_id.split("_")[0].replace("shape=", "")
    ax.set_title(
        f"p_gen recovery: centred vs non-centred GRW (hardest effort)\n"
        f"cell = {short}  |  truth α=0.95  |  N=10 000",
        fontsize=10,
    )
    ax.set_xlabel("year (AD)")
    ax.set_ylabel("p_gen")
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    out_path = (
        ROOT / "outputs" / "figures"
        / f"compare-noncentred-vs-centred-{short}.png"
    )
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out_path}", flush=True)

print("[fig] DONE.", flush=True)
