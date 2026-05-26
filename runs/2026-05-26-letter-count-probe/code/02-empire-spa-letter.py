#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-empire-spa-letter.py --- Block 2 of the 2026-05-26 letter-count probe.

Purpose
-------
Compute the empire-wide SPA three ways and compare:

  (1) inscription-mass    : each row contributes 1.0 unit of aoristic mass
                            (matches the 2026-05-21 talk-prep convention).
  (2) letter-mass (conservative)   : each row contributes
                                     `letter_count_conservative` units of mass.
  (3) letter-mass (interpretive)   : each row contributes
                                     `letter_count_interpretive` units of mass.

In all three cases the mass is distributed uniformly across the row's date
interval `[not_before, not_after]` in 5-year bins on the prereg envelope
[50 BC, AD 350].

Outputs
-------
1. `fig-02-empire-spa-overlay-normalised.png`  --- each SPA divided by its
   own max for direct shape comparison.
2. `fig-02-empire-spa-overlay-absolute.png`  --- absolute mass on a shared
   log-y axis to surface the scale ratios (letter-mass total / inscription
   total ~= mean letters per inscription).
3. `outputs/tables/empire-spa-three-ways.csv`  --- bin-centre, three SPA
   values per row.
4. `outputs/tables/empire-spa-pearson-r.csv`  --- pairwise Pearson r between
   the three SPAs (bin-by-bin), plus Spearman as a robust supplement.

Verdict flag (spec §"Verdict thresholds")
-----------------------------------------
First of three flags evaluated. Bin-by-bin Pearson r between inscription-mass
and each letter-mass variant is the headline statistic. Thresholds:

    r > 0.95  --> "no meaningful change" for that text-field choice.
    r < 0.85  --> "material change"; if either text-field hits this band,
                  letter-count must become the headline unit (spec §"Action
                  rules", flag 1).
    0.85 <= r <= 0.95 --> "modest shift; document and proceed".

Inputs
------
runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet

Reproducibility
---------------
RANDOM_SEED = 20260526 (no bootstrap in this block; deterministic SPA).

Date
----
2026-05-26
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
INPUT_PATH = RUN_DIR / "data" / "lire-filtered-with-letters.parquet"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"

for d in (FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Prereg-canonical envelope and bin width.
ENVELOPE_MIN = -50
ENVELOPE_MAX = 350
BIN_WIDTH = 5
BIN_EDGES = np.arange(ENVELOPE_MIN, ENVELOPE_MAX + 1, BIN_WIDTH, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

FIG_SIZE_WIDE = (12.0, 6.75)
DPI = 200

RANDOM_SEED = 20260526


# ---------------------------------------------------------------------------
# Weighted uniform-aoristic SPA primitive.
#
# Generalises the 2026-05-21 unit-mass primitive to per-row weights. Each
# row's `weight` is distributed uniformly across its [not_before,
# not_after + 1) interval; bins receive the row's weight scaled by the
# overlap fraction of their bin with the interval.
# ---------------------------------------------------------------------------
def weighted_aoristic_spa(
    not_before: np.ndarray,
    not_after: np.ndarray,
    width: np.ndarray,
    weight: np.ndarray,
    bin_edges: np.ndarray = BIN_EDGES,
) -> np.ndarray:
    """Build a weighted SPA under uniform aoristic mass.

    Parameters
    ----------
    not_before, not_after : np.ndarray
        Integer interval endpoints (inclusive).
    width : np.ndarray
        Integer array, not_after - not_before + 1.
    weight : np.ndarray
        Per-row mass to deposit (1.0 == inscription-mass; letter count ==
        letter-mass).
    bin_edges : np.ndarray
        Float array of length N_BINS + 1; half-open bins.

    Returns
    -------
    np.ndarray
        SPA vector (float), length len(bin_edges) - 1.
    """
    interval_lo = not_before.astype(float)
    interval_hi = not_after.astype(float) + 1.0
    density = weight.astype(float) / width.astype(float)

    spa = np.zeros(len(bin_edges) - 1, dtype=float)
    for i in range(len(bin_edges) - 1):
        b_lo = bin_edges[i]
        b_hi = bin_edges[i + 1]
        overlap = np.maximum(
            0.0, np.minimum(interval_hi, b_hi) - np.maximum(interval_lo, b_lo)
        )
        spa[i] = (overlap * density).sum()
    return spa


def main():
    if not INPUT_PATH.exists():
        sys.exit(f"FATAL: input parquet not found at {INPUT_PATH}; run 01 first.")

    df = pd.read_parquet(INPUT_PATH)
    n_rows = len(df)
    print(f"Loaded {n_rows:,} rows.")

    # `width` is not in the filtered parquet under that name; compute it
    # consistently with the 2026-05-21 talk-prep convention.
    width = (df["not_after"].to_numpy().astype(int)
             - df["not_before"].to_numpy().astype(int) + 1)
    if (width <= 0).any():
        sys.exit("FATAL: non-positive width(s); LIRE filter expected to "
                 "guarantee not_before <= not_after.")

    nb = df["not_before"].to_numpy()
    na = df["not_after"].to_numpy()

    print("Computing three empire SPAs...")
    spa_inscription = weighted_aoristic_spa(nb, na, width, np.ones(n_rows))
    spa_letter_cons = weighted_aoristic_spa(
        nb, na, width, df["letter_count_conservative"].to_numpy()
    )
    spa_letter_intr = weighted_aoristic_spa(
        nb, na, width, df["letter_count_interpretive"].to_numpy()
    )

    print(f"  inscription-mass:           total = {spa_inscription.sum():>14,.0f}")
    print(f"  letter-mass (conservative): total = {spa_letter_cons.sum():>14,.0f}")
    print(f"  letter-mass (interpretive): total = {spa_letter_intr.sum():>14,.0f}")

    # -----------------------------------------------------------------------
    # Pearson + Spearman pairwise.
    # -----------------------------------------------------------------------
    def corrs(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
        # Bin-by-bin pairing (a[i] vs b[i]).
        from scipy.stats import pearsonr, spearmanr
        return float(pearsonr(a, b).statistic), float(spearmanr(a, b).statistic)

    pairs = [
        ("inscription", "letter_conservative", spa_inscription, spa_letter_cons),
        ("inscription", "letter_interpretive", spa_inscription, spa_letter_intr),
        ("letter_conservative", "letter_interpretive", spa_letter_cons, spa_letter_intr),
    ]
    rows = []
    for a_name, b_name, a, b in pairs:
        r_p, r_s = corrs(a, b)
        rows.append({"a": a_name, "b": b_name, "pearson_r": r_p, "spearman_r": r_s})
    corr_tbl = pd.DataFrame(rows)
    corr_tbl.to_csv(TBL_DIR / "empire-spa-pearson-r.csv", index=False, float_format="%.4f")
    print("\nBin-by-bin correlations (empire-level):")
    print(corr_tbl.to_string(index=False))

    # Verdict-flag annotation.
    def annotate_flag(r: float) -> str:
        if r > 0.95:
            return "FLAG-1 NO-CHANGE (r > 0.95)"
        if r < 0.85:
            return "FLAG-1 MATERIAL (r < 0.85)"
        return "FLAG-1 MODEST (0.85 <= r <= 0.95)"

    print(
        "\nFLAG 1 (SPA shape, empire-level):\n"
        f"  inscription vs letter_conservative : "
        f"{annotate_flag(corr_tbl.loc[0, 'pearson_r'])}\n"
        f"  inscription vs letter_interpretive : "
        f"{annotate_flag(corr_tbl.loc[1, 'pearson_r'])}"
    )

    # -----------------------------------------------------------------------
    # Persist the three SPAs.
    # -----------------------------------------------------------------------
    spa_tbl = pd.DataFrame({
        "bin_centre": BIN_CENTRES,
        "spa_inscription": spa_inscription,
        "spa_letter_conservative": spa_letter_cons,
        "spa_letter_interpretive": spa_letter_intr,
    })
    spa_tbl.to_csv(TBL_DIR / "empire-spa-three-ways.csv", index=False, float_format="%.4f")

    # -----------------------------------------------------------------------
    # Figure 1: shape comparison --- each SPA normalised to its own max.
    # -----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_WIDE)
    ax.plot(
        BIN_CENTRES, spa_inscription / spa_inscription.max(),
        color="#264653", linewidth=1.8,
        label="inscription-mass (each row = 1 unit)",
    )
    ax.plot(
        BIN_CENTRES, spa_letter_cons / spa_letter_cons.max(),
        color="#e76f51", linewidth=1.4,
        label="letter-mass (conservative cleaning)",
    )
    ax.plot(
        BIN_CENTRES, spa_letter_intr / spa_letter_intr.max(),
        color="#2a9d8f", linewidth=1.4, linestyle="--",
        label="letter-mass (interpretive cleaning)",
    )
    ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
    ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.8)
    for x in (100, 200, 300):
        ax.axvline(x, color="grey", linestyle=":", alpha=0.25, linewidth=0.6)
    ax.set_xlabel("year")
    ax.set_ylabel("SPA, normalised to own max")
    ax.set_title(
        f"Empire SPA shape comparison: inscription-mass vs letter-mass "
        f"(N = {n_rows:,}; 5 y bins; uniform aoristic deposit)",
        fontsize=11,
    )
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "fig-02-empire-spa-overlay-normalised.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"\n  shape overlay -> {out.relative_to(PROJECT_ROOT)}")

    # -----------------------------------------------------------------------
    # Figure 2: absolute-mass comparison (log y) to surface scale ratios.
    # -----------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=FIG_SIZE_WIDE)
    ax.plot(
        BIN_CENTRES, spa_inscription,
        color="#264653", linewidth=1.8,
        label=f"inscription-mass (total = {spa_inscription.sum():,.0f})",
    )
    ax.plot(
        BIN_CENTRES, spa_letter_cons,
        color="#e76f51", linewidth=1.4,
        label=f"letter-mass conservative (total = {spa_letter_cons.sum():,.0f})",
    )
    ax.plot(
        BIN_CENTRES, spa_letter_intr,
        color="#2a9d8f", linewidth=1.4, linestyle="--",
        label=f"letter-mass interpretive (total = {spa_letter_intr.sum():,.0f})",
    )
    ax.set_yscale("log")
    ax.set_xlim(ENVELOPE_MIN, ENVELOPE_MAX)
    ax.axvline(0, color="grey", linestyle="--", alpha=0.4, linewidth=0.8)
    for x in (100, 200, 300):
        ax.axvline(x, color="grey", linestyle=":", alpha=0.25, linewidth=0.6)
    ax.set_xlabel("year")
    ax.set_ylabel("mass per 5 y bin (log)")
    ax.set_title(
        "Empire SPA absolute mass (log y): inscription- vs letter-weighting",
        fontsize=11,
    )
    ax.legend(loc="lower center", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "fig-02-empire-spa-overlay-absolute.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"  absolute overlay -> {out.relative_to(PROJECT_ROOT)}")

    print("Done.")


if __name__ == "__main__":
    main()
