#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-prior-equivalence.py
==========================

Sanity check: sample 1 000 prior draws from BOTH the centred and the
non-centred GRW constructions in the H2.1 mixture model and compare
the empirical mean, variance, and a selection of quantiles of
``log_pgen_increments``. If the two parameterisations are
mathematically equivalent (which they must be by construction), the
empirical statistics should agree within Monte Carlo error
(~ 1/sqrt(1000) ≈ 3% in standard deviations of a Normal).

Per the brief: if equivalence cannot be established, HALT and report;
do not proceed to production fits.

This script also uses the real ``y`` and ``tier_basis`` from the
bimodal α=0.95 cell so the dimensions match the production model,
but the observed-data factor cancels out of the prior so this is just
for shape compatibility.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import pymc as pm  # noqa: E402

# Load the non-centred + centred model builders.
_CODE_DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "noncentred_mod", _CODE_DIR / "02-mixture-fit-noncentred.py",
)
noncentred_mod = importlib.util.module_from_spec(spec)
sys.modules["noncentred_mod"] = noncentred_mod
spec.loader.exec_module(noncentred_mod)

# Load the synth-gen helpers from the validation run.
VALIDATION_ROOT = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-22-recovery-grid-validation"
)
DESIGN_JSON = Path(
    "/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/"
    "2026-05-22-recovery-grid-design/design.json"
)
spec_synth = importlib.util.spec_from_file_location(
    "synth_gen", VALIDATION_ROOT / "code" / "01-synthetic-cell-generator.py",
)
synth_gen = importlib.util.module_from_spec(spec_synth)
sys.modules["synth_gen"] = synth_gen
spec_synth.loader.exec_module(synth_gen)

design = synth_gen.load_design(DESIGN_JSON)
env = synth_gen.make_envelope(design)
tier_basis = synth_gen.build_tier_basis(design, env)

# Use the bimodal α=0.95 cell's replicate_000 data — only needed for
# matching dimensions; prior draws ignore the likelihood.
cell_id = "shape=bimodal_alpha=0.95_tier=uniform_N=10000"
synth_path = (
    VALIDATION_ROOT / "data" / "synthetic-cells" / cell_id
    / "replicate_000.parquet"
)
df = pd.read_parquet(synth_path)
y = df["y"].to_numpy(dtype=np.int64)


def prior_log_pgen_increments(builder, n_draws=1_000, seed=20260524):
    """Draw `n_draws` prior samples; return (n_draws, n_bins-1) of
    log_pgen_increments and (n_draws,) of sigma_smooth."""
    model = builder(y, tier_basis)
    with model:
        idata = pm.sample_prior_predictive(
            draws=n_draws, random_seed=seed,
        )
    inc = idata.prior["log_pgen_increments"].values  # (chain, draw, n_bins-1)
    sig = idata.prior["sigma_smooth"].values         # (chain, draw)
    inc = inc.reshape(-1, inc.shape[-1])
    sig = sig.reshape(-1)
    return inc, sig


print("[equiv] sampling centred prior...", flush=True)
inc_c, sig_c = prior_log_pgen_increments(noncentred_mod.build_model_centred)
print("[equiv] sampling non-centred prior...", flush=True)
inc_n, sig_n = prior_log_pgen_increments(noncentred_mod.build_model_noncentred)

print(f"[equiv] centred  inc shape = {inc_c.shape}", flush=True)
print(f"[equiv] noncentr inc shape = {inc_n.shape}", flush=True)

# The increments depend on a random sigma_smooth, so unconditionally
# their marginal variance is E[sigma_smooth^2]. The mean must be 0 by
# symmetry. Compare per-bin statistics across all increments pooled.
out = {}

# Pool ALL increment entries together (n_draws * (n_bins-1) scalars).
flat_c = inc_c.reshape(-1)
flat_n = inc_n.reshape(-1)
out["n_samples_per_construction"] = int(flat_c.size)
out["centred_mean"] = float(np.mean(flat_c))
out["noncentred_mean"] = float(np.mean(flat_n))
out["centred_std"] = float(np.std(flat_c))
out["noncentred_std"] = float(np.std(flat_n))
out["centred_var"] = float(np.var(flat_c))
out["noncentred_var"] = float(np.var(flat_n))

# Quantiles of the pooled increments.
qs = [0.01, 0.025, 0.05, 0.25, 0.5, 0.75, 0.95, 0.975, 0.99]
out["centred_quantiles"] = {
    f"q{q}": float(np.quantile(flat_c, q)) for q in qs
}
out["noncentred_quantiles"] = {
    f"q{q}": float(np.quantile(flat_n, q)) for q in qs
}
# Per-bin std (each of the 79 increments has the same marginal dist,
# but check that the empirical per-bin std is similar between
# constructions).
out["centred_per_bin_std_mean"] = float(np.mean(np.std(inc_c, axis=0)))
out["noncentred_per_bin_std_mean"] = float(np.mean(np.std(inc_n, axis=0)))

# sigma_smooth marginal — should be HalfNormal(1) in both.
out["centred_sigma_mean"] = float(np.mean(sig_c))
out["noncentred_sigma_mean"] = float(np.mean(sig_n))
out["centred_sigma_std"] = float(np.std(sig_c))
out["noncentred_sigma_std"] = float(np.std(sig_n))

# Verdict: ratios should be ~1.0; differences should be small relative
# to MC error. For a HalfNormal(1) scale, E[sigma^2] = 1, so
# Var(increment) marginal ≈ 1, and we should see std ≈ 1 in both.
ratio_var = out["noncentred_var"] / out["centred_var"]
ratio_std = out["noncentred_std"] / out["centred_std"]
out["ratio_var_noncentred_to_centred"] = float(ratio_var)
out["ratio_std_noncentred_to_centred"] = float(ratio_std)

# Print a verdict.
print(json.dumps(out, indent=2), flush=True)

ok_mean = abs(out["centred_mean"]) < 0.1 and abs(out["noncentred_mean"]) < 0.1
ok_var = 0.85 < ratio_var < 1.15  # 15% tolerance on MC variance of variance
ok_sigma = (
    abs(out["centred_sigma_mean"] - out["noncentred_sigma_mean"]) < 0.05
)
out["equivalence_verdict"] = {
    "ok_mean_near_zero": bool(ok_mean),
    "ok_variance_ratio_within_15pct": bool(ok_var),
    "ok_sigma_marginal_matches": bool(ok_sigma),
    "overall_pass": bool(ok_mean and ok_var and ok_sigma),
}
print(json.dumps(out["equivalence_verdict"], indent=2), flush=True)

out_path = (
    _CODE_DIR.parent / "outputs" / "prior-equivalence-check.json"
)
out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open("w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2)
print(f"[equiv] wrote {out_path}", flush=True)

sys.exit(0 if out["equivalence_verdict"]["overall_pass"] else 1)
