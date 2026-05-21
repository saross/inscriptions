#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04-mixture-recovery-synthetic.py --- Block 4 (A+ stretch) of the
RAC-TRAC 2026 talk-prep run.

Purpose
-------
Synthetic recovery demonstration of the preregistered Bayesian mixture model
(`preregistration-draft.md` §4). Goal: show on one synthetic cell that, given
a known generative process

  p_t = alpha * p_conv,t + (1 - alpha) * p_gen,t
  y   ~ Multinomial(N_eff, p)

with a known editorial-template convention structure (century-slab tier) and
a known smooth genuine shape (Gaussian peaking at AD 150), the model
recovers:

  (i)  the mixture weight alpha (true = 0.5), with a posterior 95% credible
       interval that should contain the truth;
  (ii) the genuine-shape vector p_gen, with Pearson r >= 0.95 between
       posterior median and truth (the preregistered shape-recovery bar).

This is NOT the full preregistered model. Simplifications for the talk demo:
  - One tier only (century slabs); the preregistered model has three tiers
    (century, half-century, reign-interval). The principle is the same.
  - p_gen is parametric (single Gaussian). The preregistered model uses a
    smoothness-prior on p_gen (sigma ~ HalfNormal(1)) for flexibility.
    The Gaussian gives the cleanest visual demonstration.
  - Single synthetic cell. The preregistered validation grid runs 100
    replicates per (alpha, shape, tier-weights, N) cell.

All three simplifications are stated in the slide speaker notes.

Inputs
------
None (synthetic).

Outputs
-------
runs/2026-05-21-talk-prep/outputs/figures/fig-05-mixture-recovery.png
runs/2026-05-21-talk-prep/outputs/tables/mixture-recovery-diagnostics.csv
runs/2026-05-21-talk-prep/outputs/tables/mixture-recovery-posterior-summary.csv

Mirrored to planning/conference-talk-rac-trac-2026/figures/.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-21, on Shawn's brief.
"""

from __future__ import annotations

import shutil
import sys
import warnings
from pathlib import Path

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
from scipy.stats import pearsonr

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"
TALK_FIG_DIR = PROJECT_ROOT / "planning" / "conference-talk-rac-trac-2026" / "figures"

for d in (FIG_DIR, TBL_DIR, TALK_FIG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Analysis envelope and bins (same as the empirical SPAs).
ENVELOPE_MIN = -50
ENVELOPE_MAX = 350
BIN_WIDTH = 5
BIN_EDGES = np.arange(ENVELOPE_MIN, ENVELOPE_MAX + 1, BIN_WIDTH, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0
N_BINS = len(BIN_CENTRES)

# Synthetic ground truth.
TRUE_ALPHA = 0.5
TRUE_MU = 150.0          # Gaussian peak year (AD 150)
TRUE_SIGMA = 40.0        # Gaussian scale (years)
N_TOTAL = 5_000          # synthetic sample size
TRUE_TIER_WEIGHTS = np.array([0.25, 0.25, 0.25, 0.25])  # four century slabs

# Century-slab boundaries (AD): [0,100), [100,200), [200,300), [300,400)
# (overlap envelope clips at 350 but the slab can extend beyond; the basis
# vectors below normalise within their envelope-intersect span).
CENTURY_SLABS = [(0, 100), (100, 200), (200, 300), (300, 400)]

# NUTS settings (per prereg-style; honest for a synthetic-cell demo).
N_WARMUP = 1_000
N_SAMPLE = 2_000
N_CHAINS = 4
RANDOM_SEED = 20_260_521

# Figure styling.
FIG_SIZE_WIDE = (12.0, 7.5)
DPI = 200


# ---------------------------------------------------------------------------
# Generative model: build the truth in numpy, then fit in pymc.
# ---------------------------------------------------------------------------
def build_century_slab_basis() -> np.ndarray:
    """4 x N_BINS basis where row k is the bin-membership weight for slab k.

    Each slab deposits uniform mass over its overlap with [ENVELOPE_MIN,
    ENVELOPE_MAX]; row k sums to 1.0.

    Returns
    -------
    basis : (4, N_BINS) float array.
    """
    basis = np.zeros((len(CENTURY_SLABS), N_BINS), dtype=float)
    for k, (lo, hi) in enumerate(CENTURY_SLABS):
        # Overlap of each bin with [lo, hi].
        bin_lo = BIN_EDGES[:-1]
        bin_hi = BIN_EDGES[1:]
        overlap = np.maximum(0.0, np.minimum(bin_hi, hi) - np.maximum(bin_lo, lo))
        # Each year in the slab deposits uniform mass; normalise to sum 1.
        slab_width = float(hi - lo)
        basis[k] = overlap / slab_width
        # If the slab extends past the envelope, mass is < 1 here --- so
        # renormalise to sum to 1 within the envelope so each slab is a
        # proper probability distribution over the bin grid.
        s = basis[k].sum()
        if s > 0:
            basis[k] = basis[k] / s
    return basis


def gaussian_pgen(mu: float, sigma: float) -> np.ndarray:
    """Normalised Gaussian shape over the bin centres."""
    u = (BIN_CENTRES - mu) / sigma
    g = np.exp(-0.5 * u * u)
    return g / g.sum()


def generate_synthetic() -> tuple[np.ndarray, dict]:
    """Construct the synthetic observation y and return (y, truth-dict)."""
    rng = np.random.default_rng(RANDOM_SEED)
    basis = build_century_slab_basis()
    p_conv = TRUE_TIER_WEIGHTS @ basis        # (N_BINS,)
    p_conv = p_conv / p_conv.sum()
    p_gen = gaussian_pgen(TRUE_MU, TRUE_SIGMA)
    p_true = TRUE_ALPHA * p_conv + (1.0 - TRUE_ALPHA) * p_gen
    p_true = p_true / p_true.sum()

    y = rng.multinomial(N_TOTAL, p_true).astype(int)

    truth = {
        "basis": basis,
        "p_conv": p_conv,
        "p_gen": p_gen,
        "p_true": p_true,
        "alpha": TRUE_ALPHA,
        "mu": TRUE_MU,
        "sigma": TRUE_SIGMA,
        "tier_weights": TRUE_TIER_WEIGHTS.copy(),
        "n_total": N_TOTAL,
    }
    return y, truth


# ---------------------------------------------------------------------------
# pymc model
# ---------------------------------------------------------------------------
def fit_mixture(y: np.ndarray, basis: np.ndarray) -> az.InferenceData:
    """Fit the multinomial mixture using NUTS.

    Latent parameters
    -----------------
    alpha           : Beta(2, 2)              (mixture weight)
    tier_weights    : Dirichlet([1, 1, 1, 1]) (4-century-slab weights)
    mu_gen          : Normal(150, 100)        (Gaussian peak)
    sigma_gen       : HalfNormal(50)          (Gaussian scale)

    Observation likelihood
    ----------------------
    y ~ Multinomial(N_total, alpha * p_conv + (1 - alpha) * p_gen)
    where p_conv = tier_weights @ basis
          p_gen  = softmax(-0.5 * ((t - mu_gen) / sigma_gen)^2)

    Returns
    -------
    arviz.InferenceData
    """
    n_total_obs = int(y.sum())
    bin_centres_np = BIN_CENTRES.astype(float)

    with pm.Model() as model:
        alpha = pm.Beta("alpha", 2.0, 2.0)
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(basis.shape[0]),
        )
        mu_gen = pm.Normal("mu_gen", mu=150.0, sigma=100.0)
        sigma_gen = pm.HalfNormal("sigma_gen", sigma=50.0)

        p_conv = pm.math.dot(tier_weights, basis)
        z = (bin_centres_np - mu_gen) / sigma_gen
        log_gen = -0.5 * z * z
        # Stable softmax:
        max_lg = pm.math.max(log_gen)
        unnorm = pm.math.exp(log_gen - max_lg)
        p_gen = unnorm / pm.math.sum(unnorm)
        pm.Deterministic("p_gen", p_gen)
        pm.Deterministic("p_conv", p_conv)

        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        # Multinomial requires p to sum to 1; we ensure by construction
        # (p_conv and p_gen each sum to 1; convex combination does too).

        pm.Multinomial("y_obs", n=n_total_obs, p=p_mix, observed=y)

        print(f"[block-4] sampling NUTS: warmup={N_WARMUP}, draws={N_SAMPLE}, "
              f"chains={N_CHAINS} ...")
        idata = pm.sample(
            draws=N_SAMPLE,
            tune=N_WARMUP,
            chains=N_CHAINS,
            random_seed=RANDOM_SEED,
            progressbar=False,
            target_accept=0.95,
            return_inferencedata=True,
        )
    return idata


# ---------------------------------------------------------------------------
# Diagnostics + figure
# ---------------------------------------------------------------------------
def summarise_posterior(idata: az.InferenceData, truth: dict) -> dict:
    """Compute scalar diagnostics + recovery metrics."""
    post = idata.posterior
    summary = az.summary(idata, var_names=["alpha", "mu_gen", "sigma_gen",
                                            "tier_weights"])
    # alpha recovery
    alpha_samples = post["alpha"].values.flatten()
    alpha_lo, alpha_hi = np.percentile(alpha_samples, [2.5, 97.5])
    alpha_med = float(np.median(alpha_samples))
    alpha_covered = bool(alpha_lo <= truth["alpha"] <= alpha_hi)
    # p_gen recovery: posterior median across draws, then Pearson r vs truth
    pgen_draws = post["p_gen"].values.reshape(-1, N_BINS)
    pgen_median = np.median(pgen_draws, axis=0)
    r, _ = pearsonr(pgen_median, truth["p_gen"])
    # Convergence diagnostics
    max_rhat = float(summary["r_hat"].max())
    min_ess_bulk = float(summary["ess_bulk"].min())

    return {
        "alpha_true": truth["alpha"],
        "alpha_median": alpha_med,
        "alpha_ci_lo": float(alpha_lo),
        "alpha_ci_hi": float(alpha_hi),
        "alpha_covered_95ci": alpha_covered,
        "pearson_r_pgen": float(r),
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "pgen_median": pgen_median,
        "pgen_draws": pgen_draws,
    }


def render_recovery(y: np.ndarray, truth: dict, summ: dict) -> Path:
    """Two-panel figure: (a) alpha posterior; (b) p_gen recovery overlay."""
    fig = plt.figure(figsize=FIG_SIZE_WIDE)
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1])

    # (a) alpha posterior histogram + true value.
    ax_alpha = fig.add_subplot(gs[:, 0])
    alpha_samples = summ["pgen_draws"]  # dummy --- use rebuilt below
    # We need alpha samples directly; pull from summ
    # (we stored them implicitly; recompute from idata path? Simpler:
    # we'll use median/CI from summ, and reconstruct samples from saved arviz)
    # For the figure, use alpha summary stats plus the CI band.
    # Draw a stylised posterior approximation:
    ax_alpha.axvline(
        truth["alpha"], color="black", linestyle="--", linewidth=1.5,
        label=f"true alpha = {truth['alpha']:.2f}",
    )
    ax_alpha.axvspan(
        summ["alpha_ci_lo"], summ["alpha_ci_hi"], color="C0", alpha=0.25,
        label=(f"95% CI [{summ['alpha_ci_lo']:.3f}, "
               f"{summ['alpha_ci_hi']:.3f}]"),
    )
    ax_alpha.axvline(
        summ["alpha_median"], color="C0", linewidth=1.5,
        label=f"posterior median = {summ['alpha_median']:.3f}",
    )
    ax_alpha.set_xlim(0, 1)
    ax_alpha.set_xlabel(r"$\alpha$ (mixture weight)")
    ax_alpha.set_ylabel("")
    ax_alpha.set_yticks([])
    ax_alpha.set_title("Posterior on alpha", fontsize=11)
    cov_str = "OK" if summ["alpha_covered_95ci"] else "MISS"
    ax_alpha.text(
        0.5, 0.92, f"95% CI covers truth? {cov_str}",
        transform=ax_alpha.transAxes, ha="center", fontsize=10,
        bbox={"facecolor": "lightyellow", "edgecolor": "grey", "alpha": 0.7},
    )
    ax_alpha.legend(loc="upper right", fontsize=8)

    # (b-top) Observed SPA + true components
    ax_obs = fig.add_subplot(gs[0, 1])
    ax_obs.bar(BIN_CENTRES, y, width=BIN_WIDTH * 0.9, color="lightgrey",
               edgecolor="grey", linewidth=0.5,
               label=f"synthetic y (N = {int(y.sum()):,})")
    # Overlay true components on the count scale (multiply by N_total).
    n = int(y.sum())
    ax_obs.plot(
        BIN_CENTRES, n * truth["alpha"] * truth["p_conv"],
        color="C3", linewidth=1.5,
        label=f"truth: alpha * p_conv  (alpha = {truth['alpha']:.2f})",
    )
    ax_obs.plot(
        BIN_CENTRES, n * (1 - truth["alpha"]) * truth["p_gen"],
        color="C2", linewidth=1.5,
        label=f"truth: (1-alpha) * p_gen",
    )
    ax_obs.plot(
        BIN_CENTRES, n * truth["p_true"], color="black", linewidth=1.2,
        linestyle=":", label="truth: mixture",
    )
    ax_obs.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
    ax_obs.set_ylabel("count")
    ax_obs.set_title(
        "Synthetic observed data + true generative components",
        fontsize=11,
    )
    ax_obs.legend(loc="upper right", fontsize=8)

    # (b-bottom) Recovered p_gen vs truth
    ax_rec = fig.add_subplot(gs[1, 1], sharex=ax_obs)
    # Credible band from posterior draws.
    pgen_lo = np.percentile(summ["pgen_draws"], 2.5, axis=0)
    pgen_hi = np.percentile(summ["pgen_draws"], 97.5, axis=0)
    ax_rec.fill_between(
        BIN_CENTRES, pgen_lo, pgen_hi, color="C2", alpha=0.25,
        label="recovered p_gen 95% credible band",
    )
    ax_rec.plot(
        BIN_CENTRES, summ["pgen_median"], color="C2", linewidth=1.6,
        label=f"recovered p_gen posterior median",
    )
    ax_rec.plot(
        BIN_CENTRES, truth["p_gen"], color="black", linestyle="--",
        linewidth=1.4, label=f"true p_gen (Gaussian; mu = {truth['mu']:.0f}, "
                              f"sigma = {truth['sigma']:.0f})",
    )
    ax_rec.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
    ax_rec.set_xlabel("year")
    ax_rec.set_ylabel("p_gen mass per 5-y bin")
    ax_rec.set_title(
        f"Recovered genuine shape  (Pearson r vs truth = "
        f"{summ['pearson_r_pgen']:.3f})", fontsize=11,
    )
    ax_rec.legend(loc="upper right", fontsize=8)

    diag_str = (
        f"NUTS diagnostics: max R-hat = {summ['max_rhat']:.4f}; "
        f"min ESS_bulk = {summ['min_ess_bulk']:.0f}; "
        f"prereg gates: R-hat < 1.01, ESS >= 400."
    )
    fig.suptitle(
        "Synthetic mixture recovery (one cell)",
        fontsize=12, y=0.995,
    )
    fig.text(
        0.50, 0.01, diag_str, ha="center", fontsize=8, alpha=0.7,
    )

    out = FIG_DIR / "fig-05-mixture-recovery.png"
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-4]   -> {out}")
    return out


def mirror_to_talk_dir(paths: list[Path]) -> None:
    for p in paths:
        dest = TALK_FIG_DIR / p.name
        shutil.copy2(p, dest)
        print(f"[block-4]   mirrored -> {dest}")


def main() -> int:
    print("[block-4] generating synthetic data ...")
    y, truth = generate_synthetic()
    print(f"[block-4] N_total = {y.sum():,};  max bin = {y.max()};  "
          f"min bin = {y.min()};  zero-bins = {(y == 0).sum()}")

    print("[block-4] fitting Bayesian mixture (multinomial primary) ...")
    idata = fit_mixture(y, truth["basis"])
    print("[block-4] sampling complete")

    summ = summarise_posterior(idata, truth)
    print(f"\n[block-4] ALPHA RECOVERY")
    print(f"    true alpha        = {truth['alpha']:.3f}")
    print(f"    posterior median  = {summ['alpha_median']:.3f}")
    print(f"    95% CI            = [{summ['alpha_ci_lo']:.3f}, "
          f"{summ['alpha_ci_hi']:.3f}]")
    print(f"    covers truth?     = {summ['alpha_covered_95ci']}")
    print(f"\n[block-4] SHAPE RECOVERY")
    print(f"    Pearson r (median p_gen vs truth) = {summ['pearson_r_pgen']:.3f}")
    print(f"    (prereg bar: >= 0.95)")
    print(f"\n[block-4] CONVERGENCE")
    print(f"    max R-hat       = {summ['max_rhat']:.4f}   (gate: < 1.01)")
    print(f"    min ESS_bulk    = {summ['min_ess_bulk']:.0f}   (gate: >= 400)")

    # Persist diagnostics.
    pd.DataFrame([{
        "alpha_true": truth["alpha"],
        "alpha_median": summ["alpha_median"],
        "alpha_ci_lo": summ["alpha_ci_lo"],
        "alpha_ci_hi": summ["alpha_ci_hi"],
        "alpha_covered_95ci": summ["alpha_covered_95ci"],
        "pearson_r_pgen": summ["pearson_r_pgen"],
        "max_rhat": summ["max_rhat"],
        "min_ess_bulk": summ["min_ess_bulk"],
        "n_total": int(y.sum()),
        "n_warmup": N_WARMUP,
        "n_sample": N_SAMPLE,
        "n_chains": N_CHAINS,
    }]).to_csv(TBL_DIR / "mixture-recovery-diagnostics.csv", index=False)

    az.summary(idata, var_names=["alpha", "mu_gen", "sigma_gen", "tier_weights"]
               ).to_csv(TBL_DIR / "mixture-recovery-posterior-summary.csv")

    fig_paths = [render_recovery(y, truth, summ)]
    mirror_to_talk_dir(fig_paths)
    return 0


if __name__ == "__main__":
    sys.exit(main())
