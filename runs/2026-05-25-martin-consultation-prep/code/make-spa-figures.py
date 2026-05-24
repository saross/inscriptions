#!/usr/bin/env python3
"""
make-spa-figures.py
====================

Generate the two SPA figures for the 2026-05-25 Martin consultation:

1. **Slab-highlighting SPA** — full-corpus aoristic SPA stacked by
   family classification. Shows the fraction of each year's apparent
   activity that comes from editorial templates (F1+F3) vs genuine
   signal (Tight+F2_Other) vs wide non-round (Big).

2. **Slab-excluding SPA** — clean Cohort B (Tight+F2_Other) SPA
   with the type-reweighted prior mean overlaid. The actual genuine-
   activity pattern as best we can recover it before mixture-model
   inference.

These supplement the existing figures:
- fig-02a-empirical-spa.png (uncorrected SPA, full corpus)
- fig-06-nbr-bootstrap.png (Hanson scaling)

Author / Date: Claude Opus 4.7, 2026-05-25.
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
PGEN_TABLE = Path(
    "/home/shawn/Code/inscriptions/runs/2026-05-24-empirical-pgen-prior/"
    "outputs/tables/pgen-prior-mean-and-ci.csv"
)
RUN_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = RUN_ROOT / "outputs" / "figures"

ENV_START = -50
ENV_END = 350
BIN_SIZE = 5

F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4


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
        family,
        categories=["Tight", "F2_Other", "Big", "F3_periodic", "F1_round"],
        ordered=True,
    )


def aoristic_spa(nb: np.ndarray, na: np.ndarray) -> np.ndarray:
    """Aoristic SPA: each inscription spreads mass 1.0 uniformly over [nb, na]."""
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    spa = np.zeros(n_bins)
    if len(nb) == 0:
        return spa
    nb_c = np.maximum(nb.astype(float), ENV_START)
    na_c = np.minimum(na.astype(float), ENV_END)
    width = na.astype(float) - nb.astype(float)
    valid = (width > 0) & (na_c > nb_c)
    nb_c = nb_c[valid]
    na_c = na_c[valid]
    width = width[valid]
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        overlap = np.minimum(hi, na_c) - np.maximum(lo, nb_c)
        overlap = np.maximum(overlap, 0)
        spa[i] = (overlap / width).sum()
    return spa


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading LIRE v3.0...")
    lire = pd.read_parquet(DATA_PATH)
    lire["date_range"] = (lire["not_after"] - lire["not_before"]).astype(float)
    lire["family"] = classify_family(lire)

    bin_centres = np.arange(ENV_START + BIN_SIZE / 2, ENV_END, BIN_SIZE)
    print(f"  envelope: 50 BC – AD 350 in {BIN_SIZE}-y bins (n_bins={len(bin_centres)})")

    # Compute per-family SPA
    fam_spas = {}
    print("\nComputing per-family SPAs...")
    for fam in ["Tight", "F2_Other", "Big", "F3_periodic", "F1_round"]:
        sub = lire[lire["family"] == fam]
        fam_spas[fam] = aoristic_spa(
            sub["not_before"].to_numpy(), sub["not_after"].to_numpy()
        )
        print(f"  {fam:<12} n={len(sub):>7,}  total mass={fam_spas[fam].sum():>10,.1f}")
    total_spa = sum(fam_spas.values())
    print(f"  TOTAL        n={len(lire):>7,}  total mass={total_spa.sum():>10,.1f}")

    # ===== FIGURE 1: Slab-highlighting SPA (stacked by family) =====
    print("\nDrawing slab-highlighting SPA...")
    fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                             gridspec_kw={"height_ratios": [3, 2]})

    # Top: stacked absolute counts
    ax = axes[0]
    colours = {
        "Tight": "#2ECC71",       # vivid green — hard signal
        "F2_Other": "#27AE60",    # darker green — reign-window signal
        "Big": "#95A5A6",         # grey — wide non-round
        "F3_periodic": "#F39C12", # orange — periodic editorial
        "F1_round": "#E74C3C",    # red — round-number editorial
    }
    labels = {
        "Tight": "Tight (≤4 y) — hard signal",
        "F2_Other": "F2_Other (5-48 y, reign-window) — signal",
        "Big": "Big (≥49 y, non-round) — wide; ambiguous",
        "F3_periodic": "F3_periodic (19/29/39 y) — editorial template",
        "F1_round": "F1_round (24/49/99/149/199/299 y) — editorial template",
    }
    bottom = np.zeros(len(bin_centres))
    for fam in ["Tight", "F2_Other", "Big", "F3_periodic", "F1_round"]:
        ax.fill_between(bin_centres, bottom, bottom + fam_spas[fam],
                        color=colours[fam], alpha=0.85, linewidth=0,
                        label=labels[fam])
        bottom += fam_spas[fam]
    ax.plot(bin_centres, total_spa, color="black", linewidth=1.4,
            label="Total corpus SPA")
    ax.set_ylabel("Aoristic mass per 5-y bin")
    ax.set_title(
        "Slab-highlighting SPA — LIRE v3.0, n = 182,853\n"
        "Stacked by family classification. Red+orange = editorial templates (65 % of corpus); "
        "greens = signal (17 %); grey = wide non-round (17 %)."
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)

    # Bottom: per-year fractional composition
    ax2 = axes[1]
    fractions_bottom = np.zeros(len(bin_centres))
    for fam in ["Tight", "F2_Other", "Big", "F3_periodic", "F1_round"]:
        frac = fam_spas[fam] / np.where(total_spa > 0, total_spa, 1.0)
        ax2.fill_between(bin_centres, fractions_bottom, fractions_bottom + frac,
                         color=colours[fam], alpha=0.85, linewidth=0)
        fractions_bottom += frac
    ax2.set_xlim(ENV_START, ENV_END)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel("Year (AD; negative = BC)")
    ax2.set_ylabel("Per-year fraction by family")
    ax2.set_title(
        "Per-year compositional fractions — same colour mapping.\n"
        "Where red+orange dominate, the apparent SPA is mostly editorial template; "
        "where greens dominate, the SPA is mostly signal."
    )
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    out = FIG_DIR / "spa-slab-highlighting.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")

    # Compute summary stats
    f1f3_total = fam_spas["F1_round"] + fam_spas["F3_periodic"]
    signal_total = fam_spas["Tight"] + fam_spas["F2_Other"]
    big_total = fam_spas["Big"]
    print("\n=== Per-region editorial fraction ===")
    regions = [
        (-50, 0, "50 BC – AD 1"),
        (0, 100, "AD 1 – AD 100"),
        (100, 200, "AD 100 – AD 200"),
        (200, 300, "AD 200 – AD 300"),
        (300, 350, "AD 300 – AD 350"),
    ]
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    for r_lo, r_hi, label in regions:
        mask = (bin_centres >= r_lo) & (bin_centres < r_hi)
        f1f3 = f1f3_total[mask].sum()
        sig = signal_total[mask].sum()
        big = big_total[mask].sum()
        tot = total_spa[mask].sum()
        print(f"  {label:<20}  total={tot:>9,.1f}  "
              f"editorial={100*f1f3/tot:>5.1f}%  "
              f"signal={100*sig/tot:>5.1f}%  "
              f"big={100*big/tot:>5.1f}%")

    # ===== FIGURE 2: Slab-excluding SPA (Cohort B with reweighted-prior overlay) =====
    print("\nDrawing slab-excluding SPA...")

    cohort_b = lire[lire["family"].isin(["Tight", "F2_Other"])]
    cb_spa = aoristic_spa(
        cohort_b["not_before"].to_numpy(), cohort_b["not_after"].to_numpy()
    )
    # Load type-reweighted prior from Stage 2
    pgen_df = pd.read_csv(PGEN_TABLE)

    fig, ax = plt.subplots(figsize=(14, 6))
    # Unweighted Cohort B SPA (rescaled to match total mass for overlay)
    # Plot both on absolute density (sum-to-1 normalised) and as count-mass
    cb_spa_norm = cb_spa / cb_spa.sum()
    ax.fill_between(bin_centres, 0, cb_spa_norm, alpha=0.3, color="#27AE60",
                    label=f"Cohort B unweighted (n={len(cohort_b):,} signal records)")
    ax.plot(bin_centres, cb_spa_norm, color="#27AE60", linewidth=1.5)
    # Reweighted prior overlay
    pgen_mean = pgen_df["p_gen_mean"].to_numpy()
    pgen_q05 = pgen_df["p_gen_q05"].to_numpy()
    pgen_q95 = pgen_df["p_gen_q95"].to_numpy()
    ax.fill_between(bin_centres, pgen_q05, pgen_q95, alpha=0.25, color="#2C3E50",
                    label="Type-reweighted (empirical-Bayes prior) 90 % CI")
    ax.plot(bin_centres, pgen_mean, color="#2C3E50", linewidth=2.2,
            label="Type-reweighted mean (the empirical-Bayes prior on p_gen)")

    # Optionally mark notable events for context
    for year, name in [
        (-27, "Augustus"), (14, "Tib."), (79, "Vesuvius"),
        (117, "Hadrian"), (192, "Comm. d."), (235, "Sev. Alex. d."),
        (293, "Tetrarchy"),
    ]:
        ax.axvline(year, color="grey", linestyle=":", alpha=0.4, linewidth=0.8)
        ax.text(year, ax.get_ylim()[1] * 0.92, f" {name}", color="grey",
                fontsize=7, rotation=90, va="top")

    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD; negative = BC)")
    ax.set_ylabel("p_gen density (5-y bins; sums to 1)")
    ax.set_title(
        "Slab-excluding SPA — Cohort B only (Tight + F2_Other)\n"
        f"n = {len(cohort_b):,} signal records (17.4 % of corpus, family-filtered to exclude editorial templates).\n"
        "Type-reweighted version (dark) is what the empirical-Bayes prior on p_gen would consume."
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "spa-slab-excluding.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
