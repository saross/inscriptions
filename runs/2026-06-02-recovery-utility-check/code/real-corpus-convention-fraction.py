#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
real-corpus-convention-fraction.py
==================================

Diagnostic (b): where does the REAL corpus sit relative to the recovery
model's operating envelope (α ≤ 0.70)?

The recovery grid established that the genuine signal is reliably recoverable
only while the editorial-convention mass fraction (α) is ≤ ~0.70. This script
computes the **descriptive** convention-mass fraction of the real LIRE corpus —
both globally and over time — using the project's own family classifier
(F1 round-number + F3 periodic templates = "convention"; everything else =
genuine/other), and overlays the 0.70 envelope line.

This is a descriptive computation on the raw interval structure
(`not_before`/`not_after`), independent of the Bayesian fit, so it is a robust
characterisation of p_conv (per the 2026-06-02 discussion) as well as the
answer to "which periods fall in the degraded-recovery zone?".

`classify_family`, `aoristic_spa`, `round_aligned` and the family constants are
copied verbatim from
`runs/2026-05-24-empirical-pconv/code/build-empirical-pconv.py` so the
"convention" definition is identical to the one the model's p_conv is built
from.

Usage
-----
    python real-corpus-convention-fraction.py \\
        --lire <lire-filtered-with-letters.parquet> --output-dir <outputs/>

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# --- Envelope + family constants (verbatim from build-empirical-pconv.py) --- #
ENV_START, ENV_END, BIN_SIZE = -50, 350, 5
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4
CONVENTION_FAMILIES = {"F1_round", "F3_periodic"}  # the p_conv source
ENVELOPE_ALPHA = 0.70  # operating-envelope ceiling from the recovery grid


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
        & round_aligned(nb, 10) & round_aligned(na, 10) & ~f1_mask
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
        categories=["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"],
        ordered=True,
    )


def aoristic_spa(df: pd.DataFrame) -> np.ndarray:
    """Aoristic SPA on the envelope grid; mass 1.0 spread uniformly over
    [nb, na] (original width as denominator)."""
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    spa = np.zeros(n_bins)
    if len(df) == 0:
        return spa
    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb
    valid = (width > 0) & (na_c > nb_c)
    nb_c, na_c, width = nb_c[valid], na_c[valid], width[valid]
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        overlap = np.maximum(np.minimum(hi, na_c) - np.maximum(lo, nb_c), 0)
        spa[i] = (overlap / width).sum()
    return spa


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Real-corpus convention fraction.")
    p.add_argument("--lire", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(args.lire, columns=["not_before", "not_after"])
    df = df.dropna(subset=["not_before", "not_after"]).copy()
    df["not_before"] = df["not_before"].astype(int)
    df["not_after"] = df["not_after"].astype(int)
    df["date_range"] = df["not_after"] - df["not_before"]
    df["family"] = classify_family(df)

    total_spa = aoristic_spa(df)
    conv_spa = aoristic_spa(df[df["family"].isin(CONVENTION_FAMILIES)])
    # Upper-bound sensitivity: also count "Big" (broad, non-template) as convention.
    convbig_spa = aoristic_spa(
        df[df["family"].isin(CONVENTION_FAMILIES | {"Big"})]
    )

    edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    centres = (edges[:-1] + edges[1:]) / 2.0
    with np.errstate(divide="ignore", invalid="ignore"):
        alpha_t = np.where(total_spa > 0, conv_spa / total_spa, np.nan)
        alpha_t_big = np.where(total_spa > 0, convbig_spa / total_spa, np.nan)

    global_alpha = float(conv_spa.sum() / total_spa.sum())
    global_alpha_big = float(convbig_spa.sum() / total_spa.sum())

    # Family mass shares (corpus-wide, aoristic).
    fam_share = {
        fam: float(aoristic_spa(df[df["family"] == fam]).sum() / total_spa.sum())
        for fam in ["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"]
    }

    # Periods exceeding the envelope.
    over = centres[(alpha_t > ENVELOPE_ALPHA)]
    over_big = centres[(alpha_t_big > ENVELOPE_ALPHA)]

    # --- Table ---
    tbl = pd.DataFrame({
        "bin_start_year": edges[:-1].astype(int),
        "bin_centre": centres,
        "total_mass": total_spa,
        "convention_mass_F1F3": conv_spa,
        "alpha_t_F1F3": alpha_t,
        "alpha_t_incl_Big": alpha_t_big,
    })
    tbl_path = args.output_dir / "convention-fraction-by-bin.csv"
    tbl.to_csv(tbl_path, index=False)

    # --- Figure ---
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(centres, alpha_t, color="firebrick", lw=2,
            label="convention fraction α(t)  (F1+F3 templates)")
    ax.plot(centres, alpha_t_big, color="darkorange", lw=1.2, ls="--",
            label="α(t) incl. 'Big' broad intervals (upper bound)")
    ax.axhline(ENVELOPE_ALPHA, color="black", ls=":", lw=1.5,
               label=f"recovery operating envelope (α = {ENVELOPE_ALPHA})")
    ax.axhline(global_alpha, color="firebrick", ls="-.", lw=0.9, alpha=0.6,
               label=f"corpus-wide α = {global_alpha:.2f}")
    ax.set_xlabel("year (negative = BC)")
    ax.set_ylabel("editorial-convention mass fraction")
    ax.set_ylim(0, 1)
    ax.set_title("Real-corpus convention fraction over time vs the recovery "
                 "operating envelope")
    ax.legend(fontsize=8, loc="upper left")
    fig_path = args.output_dir / "convention-fraction-over-time.png"
    fig.savefig(fig_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    # --- Report to stdout ---
    print(f"[real-alpha] corpus rows used: {len(df)}")
    print(f"[real-alpha] corpus-wide convention fraction (F1+F3): "
          f"{global_alpha:.3f}  -> {'IN envelope' if global_alpha<=ENVELOPE_ALPHA else 'OUTSIDE envelope'}")
    print(f"[real-alpha] corpus-wide incl. Big (upper bound): {global_alpha_big:.3f}")
    print("[real-alpha] family aoristic-mass shares:")
    for fam, s in fam_share.items():
        print(f"             {fam:14s} {s:.3f}")
    print(f"[real-alpha] bins with α(t) > {ENVELOPE_ALPHA} (F1+F3): "
          f"{len(over)}/{len(centres)}")
    if len(over):
        print(f"             year range: {int(over.min())}..{int(over.max())}")
    print(f"[real-alpha] bins with α(t) > {ENVELOPE_ALPHA} incl. Big: "
          f"{len(over_big)}/{len(centres)} "
          f"({int(over_big.min())}..{int(over_big.max())})" if len(over_big) else "")
    print(f"[real-alpha] wrote {tbl_path}")
    print(f"[real-alpha] wrote {fig_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
