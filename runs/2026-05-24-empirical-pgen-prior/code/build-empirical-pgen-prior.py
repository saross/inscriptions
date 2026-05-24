#!/usr/bin/env python3
"""
build-empirical-pgen-prior.py
==============================

Construct the informative prior on the genuine-activity component
(p_gen) of the H2.1 mixture model from Cohort B (Tight ∪ F2_Other,
31,841 records).

Method:

1. Classify LIRE v3.0 with the family classifier (same rules as
   2026-05-24-type-stratified-narrow-spas).
2. Take Cohort B = Tight ∪ F2_Other. This is the calibration cohort —
   inscriptions with tight or reign-window dating, excluding all
   editorial slabs (F1, F3) and very wide non-round intervals (Big).
3. Type-reweight to match corpus type composition (post-stratification).
   This corrects the strong type-bias documented earlier: Cohort B
   is 18 % epitaph vs corpus 56 % epitaph; honorific is over-
   represented; military diplomas are over-represented; etc.
4. Bootstrap CI: resample Cohort B with replacement 1,000 times;
   recompute the reweighted p_gen each time; characterise the
   bin-wise distribution. This gives quantitative uncertainty on
   the prior mean.
5. Derive a sigma_prior heuristic on the LOG scale (matching the
   GRW-on-log-density parameterisation of the current mixture model).
   The prior on log_pgen will then be N(log_pgen_cohort, sigma_prior).

Outputs:

- outputs/figures/pgen-prior-mean-with-ci.png — cohort-derived p_gen
  mean with 90 % bootstrap CI
- outputs/figures/pgen-per-type-contributions.png — which types are
  driving the reweighted prior shape
- outputs/figures/pgen-reweighting-effect.png — unweighted vs
  type-reweighted overlay
- outputs/figures/effective-sample-size-by-year.png — per-bin overlap
  count (where the prior is well-constrained vs thin)
- outputs/figures/sigma-prior-bin-wise.png — bootstrap SD of log_pgen
  per bin (the sigma_prior recommendation)
- outputs/tables/pgen-prior-mean-and-ci.csv — bin centres, mean, 5th/95th
- outputs/tables/sigma-prior-per-bin.csv — bin centres, SD of log_pgen
- outputs/tables/per-type-effective-N-and-weight.csv — sample diagnostic

Inputs:
- archive/data-2026-04-22/LIRE_v3-0.parquet

Author / Date: Claude Opus 4.7 (1M context), 2026-05-24.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DATA_PATH = Path("/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet")
RUN_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = RUN_ROOT / "outputs" / "figures"
TBL_DIR = RUN_ROOT / "outputs" / "tables"

# Envelope and bin size
ENV_START = -50
ENV_END = 350
BIN_SIZE = 5

# Family-classifier constants
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4

# Type taxonomy
TYPE_MAPPING = {
    "epitaph": "epitaph (funerary)",
    "votive inscription": "votive",
    "identification inscription": "identification",
    "owner/artist inscription": "identification",
    "honorific inscription": "honorific",
    "building/dedicatory inscription": "building/dedicatory",
    "mile-/leaguestone": "mile-/leaguestone",
    "military diploma": "military diploma",
    "boundary inscription": "boundary",
    "acclamation": "acclamation",
    "defixio": "other small",
    "list": "other small",
    "label": "other small",
    "public legal inscription": "other small",
    "private legal inscription": "other small",
    "elogium": "other small",
    "letter": "other small",
    "seat inscription": "other small",
    "prayer": "other small",
    "assignation inscription": "other small",
    "calendar": "other small",
    "adnuntiatio": "other small",
}
TYPE_ORDER = [
    "epitaph (funerary)", "votive", "identification", "honorific",
    "building/dedicatory", "mile-/leaguestone", "military diploma",
    "boundary", "acclamation", "other small", "unknown",
]

# Bootstrap settings
N_BOOTSTRAP = 1000
BOOTSTRAP_SEED = 20260524

# Tiny floor to keep log() well-defined
LOG_FLOOR = 1e-6


def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def classify_family(lire: pd.DataFrame) -> pd.Categorical:
    nb = lire["not_before"].to_numpy()
    na = lire["not_after"].to_numpy()
    dr = lire["date_range"].to_numpy()
    f1_mask = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3_mask = (
        np.isin(dr, list(F3_WIDTHS))
        & round_aligned(nb, 10) & round_aligned(na, 10)
        & ~f1_mask
    )
    tight_mask = (dr <= TIGHT_MAX) & ~f1_mask & ~f3_mask
    big_mask = (dr >= 49) & ~f1_mask
    other_mask = ~(f1_mask | f3_mask | tight_mask | big_mask)
    family = np.full(len(lire), "Big", dtype=object)
    family[f1_mask] = "F1_round"
    family[f3_mask] = "F3_periodic"
    family[tight_mask] = "Tight"
    family[other_mask] = "F2_Other"
    family[big_mask] = "Big"
    return pd.Categorical(
        family, categories=["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"],
        ordered=True,
    )


def simplify_type(t: pd.Series) -> pd.Categorical:
    cat = t.map(TYPE_MAPPING).fillna("unknown")
    return pd.Categorical(cat, categories=TYPE_ORDER, ordered=True)


def aoristic_spa(nb: np.ndarray, na: np.ndarray, weights: np.ndarray | None = None) -> np.ndarray:
    """Compute aoristic SPA on the envelope grid; optional per-record weights.

    Each record contributes its weight uniformly over [nb, na] clipped to envelope.
    """
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    spa = np.zeros(n_bins)
    if len(nb) == 0:
        return spa
    nb = nb.astype(float)
    na = na.astype(float)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb
    valid = (width > 0) & (na_c > nb_c)
    nb_c = nb_c[valid]
    na_c = na_c[valid]
    width = width[valid]
    w = weights[valid] if weights is not None else np.ones(len(nb_c))
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        overlap = np.minimum(hi, na_c) - np.maximum(lo, nb_c)
        overlap = np.maximum(overlap, 0)
        spa[i] = (overlap / width * w).sum()
    return spa


def normalise(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return v / s if s > 0 else v


def reweighted_pgen(
    cohort: pd.DataFrame, target_weights: pd.Series,
) -> np.ndarray:
    """Compute type-post-stratified p_gen from a cohort.

    Each record gets weight = target_weights[type] / (count of that type in cohort).
    Result: aoristic SPA reweighted to match target type composition.
    """
    type_counts_in_cohort = cohort["type_simple"].value_counts().reindex(TYPE_ORDER, fill_value=0)
    per_record_w = np.zeros(len(cohort))
    type_arr = cohort["type_simple"].to_numpy()
    for t in TYPE_ORDER:
        n_t = type_counts_in_cohort[t]
        if n_t == 0:
            continue
        w_t = target_weights[t] / n_t
        per_record_w[type_arr == t] = w_t
    spa = aoristic_spa(
        cohort["not_before"].to_numpy(),
        cohort["not_after"].to_numpy(),
        per_record_w,
    )
    return normalise(spa)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TBL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading LIRE v3.0...")
    lire = pd.read_parquet(DATA_PATH)
    lire["date_range"] = (lire["not_after"] - lire["not_before"]).astype(float)
    lire["family"] = classify_family(lire)
    lire["type_simple"] = simplify_type(lire["type_of_inscription_auto"])

    cohort_b = lire[lire["family"].isin(["Tight", "F2_Other"])].copy()
    print(f"  Cohort B = Tight + F2_Other: {len(cohort_b):,} records")

    # Target type composition: corpus
    corpus_total = len(lire)
    target_weights = (lire["type_simple"].value_counts().reindex(TYPE_ORDER, fill_value=0)
                      / corpus_total)
    print(f"\nTarget type composition (full corpus):")
    for t in TYPE_ORDER:
        print(f"  {t:<22} {target_weights[t]*100:>6.2f}%")

    bin_centres = np.arange(ENV_START + BIN_SIZE / 2, ENV_END, BIN_SIZE)
    n_bins = len(bin_centres)

    # ===== Step 1: Reweighted prior mean =====
    print("\nComputing reweighted p_gen prior mean...")
    pgen_mean = reweighted_pgen(cohort_b, target_weights)

    # ===== Step 2: Unweighted comparison =====
    pgen_unweighted = normalise(
        aoristic_spa(cohort_b["not_before"].to_numpy(), cohort_b["not_after"].to_numpy())
    )

    # ===== Step 3: Bootstrap CI =====
    print(f"Bootstrapping {N_BOOTSTRAP} resamples...")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    n = len(cohort_b)
    boot_pgens = np.zeros((N_BOOTSTRAP, n_bins))
    cohort_arr = cohort_b.reset_index(drop=True)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, n, n)
        sub = cohort_arr.iloc[idx]
        boot_pgens[b] = reweighted_pgen(sub, target_weights)
        if (b + 1) % 100 == 0:
            print(f"    {b + 1}/{N_BOOTSTRAP}")

    # Bin-wise CI on linear scale
    p_lo = np.quantile(boot_pgens, 0.05, axis=0)
    p_hi = np.quantile(boot_pgens, 0.95, axis=0)
    p_mean_boot = boot_pgens.mean(axis=0)

    # On log scale (for GRW prior sigma)
    log_floor = LOG_FLOOR
    log_boot = np.log(np.maximum(boot_pgens, log_floor))
    log_mean = log_boot.mean(axis=0)
    log_sd = log_boot.std(axis=0)
    log_p_lo = np.quantile(log_boot, 0.05, axis=0)
    log_p_hi = np.quantile(log_boot, 0.95, axis=0)

    # Write tables
    pd.DataFrame({
        "bin_centre_year": bin_centres,
        "p_gen_mean": pgen_mean,
        "p_gen_mean_bootstrap": p_mean_boot,
        "p_gen_q05": p_lo,
        "p_gen_q95": p_hi,
    }).to_csv(TBL_DIR / "pgen-prior-mean-and-ci.csv", index=False)
    pd.DataFrame({
        "bin_centre_year": bin_centres,
        "log_p_gen_mean": log_mean,
        "log_p_gen_sd": log_sd,
        "log_p_gen_q05": log_p_lo,
        "log_p_gen_q95": log_p_hi,
        "sigma_prior_recommend": log_sd,
    }).to_csv(TBL_DIR / "sigma-prior-per-bin.csv", index=False)

    # Per-type diagnostic
    rows = []
    type_counts = cohort_b["type_simple"].value_counts().reindex(TYPE_ORDER, fill_value=0)
    for t in TYPE_ORDER:
        n_t = type_counts[t]
        rows.append(dict(
            type=t,
            corpus_target_weight=round(target_weights[t], 4),
            cohort_count=int(n_t),
            cohort_pct=round(100 * n_t / len(cohort_b), 2),
            up_or_down_weight_factor=round(
                target_weights[t] / (n_t / len(cohort_b)) if n_t > 0 else float('nan'),
                3,
            ),
        ))
    type_df = pd.DataFrame(rows)
    type_df.to_csv(TBL_DIR / "per-type-effective-N-and-weight.csv", index=False)
    print("\nPer-type reweighting diagnostic:")
    print(type_df.to_string(index=False))

    # ===== Figures =====
    # Figure 1: prior mean with CI band
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.fill_between(bin_centres, p_lo, p_hi, alpha=0.25, color="C2",
                    label="90 % bootstrap CI")
    ax.plot(bin_centres, pgen_mean, color="C2", linewidth=2,
            label="Type-reweighted prior mean")
    ax.plot(bin_centres, pgen_unweighted, color="C0", linewidth=1.2,
            linestyle="--", label="Cohort B unweighted (no reweighting)")
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD)")
    ax.set_ylabel("p_gen density (5-year bins; sums to 1)")
    ax.set_title(
        "Empirical p_gen prior from Cohort B — mean + 90 % bootstrap CI\n"
        f"n_cohort = {len(cohort_b):,}; n_bootstrap = {N_BOOTSTRAP}; "
        "type-reweighted to match full-corpus composition"
    )
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "pgen-prior-mean-with-ci.png", dpi=150)
    plt.close(fig)
    print("  wrote pgen-prior-mean-with-ci.png")

    # Figure 2: per-type contributions to the reweighted prior
    fig, ax = plt.subplots(figsize=(14, 6))
    bottom = np.zeros(n_bins)
    cmap = plt.cm.tab20(np.linspace(0, 1, len(TYPE_ORDER)))
    type_arr = cohort_b["type_simple"].to_numpy()
    for i, t in enumerate(TYPE_ORDER):
        sub = cohort_b[cohort_b["type_simple"] == t]
        if len(sub) == 0:
            continue
        spa_t = normalise(aoristic_spa(
            sub["not_before"].to_numpy(), sub["not_after"].to_numpy()
        ))
        contrib = target_weights[t] * spa_t
        ax.fill_between(bin_centres, bottom, bottom + contrib, color=cmap[i],
                        alpha=0.85, linewidth=0, label=t)
        bottom += contrib
    # Re-normalise stack to match the actual prior mean
    if bottom.sum() > 0:
        scale = 1.0 / bottom.sum()
    else:
        scale = 1.0
    ax.plot(bin_centres, pgen_mean, color="black", linewidth=1.6,
            linestyle="--", label="Aggregate reweighted prior")
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD)")
    ax.set_ylabel("Weighted per-type contribution (unnormalised)")
    ax.set_title(
        "Per-type contributions to the empirical p_gen prior\n"
        "Stacked = type-weighted SPA × corpus target weight. "
        "Dashed = aggregate reweighted prior (after final normalisation)."
    )
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "pgen-per-type-contributions.png", dpi=150)
    plt.close(fig)
    print("  wrote pgen-per-type-contributions.png")

    # Figure 3: reweighting effect
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(bin_centres, pgen_unweighted, color="C0", linewidth=1.8,
            label="Unweighted Cohort B SPA")
    ax.plot(bin_centres, pgen_mean, color="C2", linewidth=2,
            label="Type-reweighted prior")
    ax.fill_between(bin_centres, pgen_unweighted, pgen_mean,
                    alpha=0.2, color="red",
                    label="Difference (reweighting effect)")
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD)")
    ax.set_ylabel("p_gen density")
    ax.set_title(
        "Effect of type-reweighting on the prior shape\n"
        "Reweighting corrects Cohort B's over-representation of honorific/identification/"
        "mile-stone/military-diploma\n"
        "and under-representation of epitaph relative to corpus composition"
    )
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "pgen-reweighting-effect.png", dpi=150)
    plt.close(fig)
    print("  wrote pgen-reweighting-effect.png")

    # Figure 4: effective sample size by year (coverage diagnostic)
    print("Computing effective sample size by year...")
    cohort_nb = cohort_b["not_before"].to_numpy(dtype=float)
    cohort_na = cohort_b["not_after"].to_numpy(dtype=float)
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    # Effective N = number of inscriptions whose interval overlaps the bin
    n_per_bin = np.zeros(n_bins)
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        overlap = np.minimum(hi, cohort_na) - np.maximum(lo, cohort_nb)
        n_per_bin[i] = (overlap > 0).sum()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(bin_centres, n_per_bin, width=BIN_SIZE * 0.9, color="C2", alpha=0.7)
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD)")
    ax.set_ylabel("Cohort B inscriptions overlapping each 5-year bin")
    ax.set_title(
        "Effective sample size by year — Cohort B\n"
        "Per-bin overlap count. Where this is low, the empirical prior is thin "
        "and should have wide bootstrap CI."
    )
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "effective-sample-size-by-year.png", dpi=150)
    plt.close(fig)
    print("  wrote effective-sample-size-by-year.png")

    # Figure 5: sigma_prior per bin (log-scale SD)
    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax1.fill_between(bin_centres, log_p_lo, log_p_hi, alpha=0.25, color="C3",
                     label="90 % bootstrap CI on log p_gen")
    ax1.plot(bin_centres, log_mean, color="C3", linewidth=2, label="log p_gen mean")
    ax1.set_xlim(ENV_START, ENV_END)
    ax1.set_xlabel("Year (AD)")
    ax1.set_ylabel("log p_gen", color="C3")
    ax1.tick_params(axis="y", labelcolor="C3")
    ax1.grid(True, alpha=0.3)
    ax2 = ax1.twinx()
    ax2.plot(bin_centres, log_sd, color="C0", linewidth=1.6,
             linestyle="--", label="bootstrap SD (sigma_prior)")
    ax2.set_ylabel("Bootstrap SD of log p_gen (= sigma_prior recommendation)", color="C0")
    ax2.tick_params(axis="y", labelcolor="C0")
    ax1.set_title(
        "Bin-wise sigma_prior for the GRW-on-log-density formulation\n"
        "Red: mean log p_gen (the prior centre). Blue: bootstrap SD (the prior spread).\n"
        f"Median sigma_prior across non-thin bins ≈ {np.median(log_sd[n_per_bin > 50]):.3f}"
    )
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "sigma-prior-bin-wise.png", dpi=150)
    plt.close(fig)
    print("  wrote sigma-prior-bin-wise.png")

    # Summary print
    print(f"\n=== Summary ===")
    print(f"  Bootstrap median sigma_prior (well-covered bins, n>=50): "
          f"{np.median(log_sd[n_per_bin >= 50]):.4f}")
    print(f"  Bootstrap mean sigma_prior (well-covered bins): "
          f"{np.mean(log_sd[n_per_bin >= 50]):.4f}")
    print(f"  Bootstrap max sigma_prior (well-covered bins): "
          f"{np.max(log_sd[n_per_bin >= 50]):.4f}")
    print(f"  Bins with n<50: {(n_per_bin < 50).sum()} of {n_bins}")
    print(f"  Total cohort N: {len(cohort_b):,}")
    print(f"  Total cohort with envelope overlap: {(cohort_na > ENV_START).sum() & (cohort_nb < ENV_END).sum():,}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
