#!/usr/bin/env python3
"""
build-empirical-pconv.py
========================

Construct the empirical editorial-convention component (p_conv) of the
H2.1 mixture model from the F1 (round-number) + F3 (periodic-window)
families identified by the 2026-05-24 family classifier.

The current H2.1 model uses a hand-curated 3-tier × 21-interval basis
specified in `runs/2026-05-22-recovery-grid-design/design.json`. That
design's own `template_intervals_note` flags these intervals as
"a working dictionary scoped to the recovery simulation … the
production mixture fit on real data will use the empirical-scan
dictionary instead." This script generates that empirical-scan
dictionary directly from F1+F3 inscriptions.

Approach:

1. Classify every LIRE v3.0 inscription as F1, F3, Tight, F2_Other, or
   Big (same classifier as 2026-05-24-type-stratified-narrow-spas).
2. For each F1/F3 inscription, spread mass 1.0 uniformly across its
   [not_before, not_after] interval into 5-year bins on the envelope
   50 BC – AD 400.
3. Sum across all F1+F3 inscriptions and normalise → empirical p_conv.
4. Decompose p_conv by slab-type (24-y quarter-century, 49-y
   half-century, 99-y century, 149-y, 199-y, 299-y; 19-y, 29-y, 39-y
   periodic windows) so we can see what each slab-type contributes
   to the editorial convention shape.
5. Compare against the current generic tier-template basis under each
   of the 5 design.json `tier_weight_grid` choices.

Outputs:

- `outputs/figures/empirical-pconv-vs-current-basis.png` — overlay of
  empirical p_conv against the 5 current tier-weight-grid cases
- `outputs/figures/pconv-decomposition-by-slab.png` — per-slab-type
  basis rows + their stacked contribution to p_conv
- `outputs/figures/pconv-difference-heatmap.png` — empirical minus
  current basis under each weight choice
- `outputs/tables/slab-type-weights.csv` — empirical weight per slab type
- `outputs/tables/empirical-pconv-vector.csv` — the actual p_conv array

Inputs: archive/data-2026-04-22/LIRE_v3-0.parquet
       runs/2026-05-22-recovery-grid-design/design.json (for comparison)

Author / Date: Claude Opus 4.7 (1M context), 2026-05-24.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


DATA_PATH = Path("/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet")
DESIGN_PATH = Path(
    "/home/shawn/Code/inscriptions/runs/2026-05-22-recovery-grid-design/design.json"
)
RUN_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = RUN_ROOT / "outputs" / "figures"
TBL_DIR = RUN_ROOT / "outputs" / "tables"

# Envelope and bin size: match the prereg (50 BC – AD 350).
ENV_START = -50
ENV_END = 350
BIN_SIZE = 5

# Family classifier constants (same as cohort analysis)
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4

# Slab-type taxonomy by width
SLAB_TYPES = {
    24: "quarter_century",       # F1
    49: "half_century",          # F1
    99: "century",               # F1
    149: "one_and_a_half_century",  # F1
    199: "two_century",          # F1
    299: "three_century",        # F1
    19: "twenty_year_window",    # F3
    29: "thirty_year_window",    # F3
    39: "forty_year_window",     # F3
}


def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def classify_family(lire: pd.DataFrame) -> pd.Series:
    nb = lire["not_before"].to_numpy()
    na = lire["not_after"].to_numpy()
    dr = lire["date_range"].to_numpy()

    f1_mask = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3_mask = (
        np.isin(dr, list(F3_WIDTHS))
        & round_aligned(nb, 10)
        & round_aligned(na, 10)
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
        categories=["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"],
        ordered=True,
    )


def aoristic_spa(df: pd.DataFrame) -> np.ndarray:
    """Compute aoristic SPA on the envelope grid at BIN_SIZE resolution.
    Each inscription contributes mass 1.0 uniformly across [nb, na].
    Returns vector of length n_bins."""
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    spa = np.zeros(n_bins)
    if len(df) == 0:
        return spa

    nb = df["not_before"].to_numpy(dtype=float)
    na = df["not_after"].to_numpy(dtype=float)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb  # use ORIGINAL width as denominator
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


def normalise(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return v / s if s > 0 else v


def build_tier_basis_from_design(design: dict) -> dict:
    """Recreate the current 3-tier basis from design.json, plus the 5
    tier-weight combinations. Returns dict with 'tier_basis' (3 × N_bins
    array) and 'tier_weights' (dict name → (3,) array)."""
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    bin_edges = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
    tier_order = design["tier_order"]
    intervals_by_tier = design["template_intervals_by_tier"]

    basis = np.zeros((len(tier_order), n_bins))
    for k, tier_name in enumerate(tier_order):
        intervals = intervals_by_tier[tier_name]
        tier_sum = np.zeros(n_bins)
        for iv in intervals:
            lo_iv, hi_iv = float(iv["lo"]), float(iv["hi"])
            width = hi_iv - lo_iv
            if width <= 0:
                continue
            per_bin = np.zeros(n_bins)
            for i in range(n_bins):
                lo, hi = bin_edges[i], bin_edges[i + 1]
                overlap = max(0, min(hi, hi_iv) - max(lo, lo_iv))
                per_bin[i] = overlap / width
            s = per_bin.sum()
            if s > 0:
                tier_sum += per_bin / s
        s = tier_sum.sum()
        if s > 0:
            basis[k] = tier_sum / s

    tier_weights = {
        tw["name"]: np.asarray(tw["weights"])
        for tw in design["tier_weight_grid"]
    }
    return {"tier_basis": basis, "tier_weights": tier_weights,
            "tier_order": tier_order}


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TBL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading LIRE v3.0...")
    lire = pd.read_parquet(DATA_PATH)
    lire["date_range"] = (lire["not_after"] - lire["not_before"]).astype(float)
    lire["family"] = classify_family(lire)

    # F1+F3 subset for empirical p_conv
    convention = lire[lire["family"].isin(["F1_round", "F3_periodic"])].copy()
    print(f"  classified: F1={('F1_round'==lire['family']).sum():,}  "
          f"F3={('F3_periodic'==lire['family']).sum():,}  "
          f"convention total={len(convention):,}")

    bin_centres = np.arange(ENV_START + BIN_SIZE / 2, ENV_END, BIN_SIZE)
    n_bins = len(bin_centres)
    print(f"  envelope: 50 BC – AD 350 in {BIN_SIZE}-year bins; n_bins={n_bins}")

    # ===== Step 1: Aggregate empirical p_conv =====
    print("\nComputing empirical p_conv...")
    pconv_emp = aoristic_spa(convention)
    pconv_emp_norm = normalise(pconv_emp)
    out = TBL_DIR / "empirical-pconv-vector.csv"
    pd.DataFrame({"bin_centre_year": bin_centres,
                  "p_conv_empirical": pconv_emp_norm}).to_csv(out, index=False)
    print(f"  wrote {out}")

    # ===== Step 2: Per-slab-type decomposition =====
    print("\nDecomposing by slab type...")
    slab_rows = []
    slab_bases = {}
    total_mass = len(convention)
    for width, slab_name in SLAB_TYPES.items():
        sub = convention[convention["date_range"] == width]
        n = len(sub)
        if n == 0:
            continue
        spa = aoristic_spa(sub)
        slab_bases[slab_name] = normalise(spa)
        slab_rows.append(dict(
            slab_name=slab_name, width=int(width),
            count=int(n),
            weight=round(n / total_mass, 4),
            pct=round(100 * n / total_mass, 2),
            family="F1" if width in F1_WIDTHS else "F3",
        ))
    slab_df = pd.DataFrame(slab_rows).sort_values(
        "count", ascending=False).reset_index(drop=True)
    out = TBL_DIR / "slab-type-weights.csv"
    slab_df.to_csv(out, index=False)
    print("\nSlab-type weights (within F1+F3):")
    print(slab_df.to_string(index=False))
    print(f"  wrote {out}")

    # ===== Step 3: Reconstruct empirical p_conv as weighted sum of slab bases =====
    pconv_reconstructed = np.zeros(n_bins)
    for _, row in slab_df.iterrows():
        pconv_reconstructed += row["weight"] * slab_bases[row["slab_name"]]
    pconv_reconstructed = normalise(pconv_reconstructed)

    diff = np.abs(pconv_emp_norm - pconv_reconstructed).sum()
    print(f"\nReconstruction check: |aggregate - sum of weighted slabs|_L1 = {diff:.4f}")
    # Should be very small (only differs if there are F1+F3 inscriptions at
    # non-standard widths not in SLAB_TYPES).

    # ===== Step 4: Current tier-template basis for comparison =====
    print("\nBuilding current tier-template basis from design.json...")
    with open(DESIGN_PATH) as f:
        design = json.load(f)
    cur = build_tier_basis_from_design(design)
    cur_pconvs = {}
    for tw_name, w in cur["tier_weights"].items():
        cur_pconvs[tw_name] = w @ cur["tier_basis"]  # 3, dot (3, N) -> N

    # ===== Plot 1: Empirical p_conv vs current basis under each weight choice =====
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(bin_centres, pconv_emp_norm, color="black", linewidth=2.5,
            label="Empirical p_conv (F1+F3 derived)")
    cmap = plt.cm.tab10
    for i, (name, vec) in enumerate(cur_pconvs.items()):
        ax.plot(bin_centres, vec, color=cmap(i), linewidth=1.2, alpha=0.85,
                label=f"current tier-template — {name}")
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD; 50 BC – AD 350 envelope)")
    ax.set_ylabel("p_conv density (5-year bins; sums to 1)")
    ax.set_title(
        "Empirical p_conv from F1+F3 vs current placeholder tier-template basis\n"
        "Current basis is theory-derived (design.json); empirical is data-derived "
        f"from {len(convention):,} F1+F3 inscriptions"
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "empirical-pconv-vs-current-basis.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\n  wrote {out}")

    # ===== Plot 2: Per-slab-type decomposition + stacked contribution =====
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    # Top: individual slab-type basis rows (normalised per-row)
    ax_top = axes[0]
    cmap = plt.cm.viridis(np.linspace(0, 1, len(slab_df)))
    for (i, row), c in zip(slab_df.iterrows(), cmap):
        b = slab_bases[row["slab_name"]]
        ax_top.plot(bin_centres, b, color=c, linewidth=1.3,
                    label=f"{row['slab_name']} (width={row['width']}, n={row['count']:,}, w={row['weight']:.3f})")
    ax_top.set_ylabel("Per-slab-type basis (sums to 1 per row)")
    ax_top.set_title("Slab-type basis rows — each row is the SPA for inscriptions of that exact width")
    ax_top.legend(loc="upper right", fontsize=8, ncol=2)
    ax_top.grid(True, alpha=0.3)

    # Bottom: stacked weighted contribution to p_conv
    ax_bot = axes[1]
    stack_bottom = np.zeros(n_bins)
    for (i, row), c in zip(slab_df.iterrows(), cmap):
        b = slab_bases[row["slab_name"]] * row["weight"]
        ax_bot.fill_between(bin_centres, stack_bottom, stack_bottom + b,
                            color=c, alpha=0.85, linewidth=0,
                            label=f"{row['slab_name']}")
        stack_bottom += b
    # Overlay total empirical p_conv
    ax_bot.plot(bin_centres, pconv_emp_norm, color="red", linewidth=1.5,
                linestyle="--", label="aggregate empirical p_conv")
    ax_bot.set_xlim(ENV_START, ENV_END)
    ax_bot.set_xlabel("Year (AD)")
    ax_bot.set_ylabel("Weighted contribution to p_conv")
    ax_bot.set_title("Stacked contributions to empirical p_conv (sum = aggregate p_conv)")
    ax_bot.legend(loc="upper right", fontsize=8, ncol=2)
    ax_bot.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "pconv-decomposition-by-slab.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")

    # ===== Plot 3: Difference heatmap — empirical minus each current weight choice =====
    fig, ax = plt.subplots(figsize=(14, 5))
    diff_grid = np.array(
        [pconv_emp_norm - cur_pconvs[name] for name in cur_pconvs]
    )
    vmax = np.abs(diff_grid).max()
    im = ax.imshow(
        diff_grid, aspect="auto",
        extent=[ENV_START, ENV_END, -0.5, len(cur_pconvs) - 0.5],
        cmap="RdBu_r", vmin=-vmax, vmax=vmax, origin="lower",
    )
    ax.set_yticks(range(len(cur_pconvs)))
    ax.set_yticklabels(list(cur_pconvs.keys()))
    ax.set_xlabel("Year (AD)")
    ax.set_title(
        "Empirical p_conv MINUS each current tier-weight-grid choice\n"
        "Red = empirical higher than current; Blue = current higher than empirical"
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Density difference (5y bin)")
    fig.tight_layout()
    out = FIG_DIR / "pconv-difference-heatmap.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")

    # ===== Diagnostic: which current case is "closest" to empirical? =====
    print("\nL1 distance between empirical and each current case:")
    print(f"  {'case':<25}  L1 distance  max abs diff")
    distances = []
    for name, vec in cur_pconvs.items():
        l1 = np.abs(pconv_emp_norm - vec).sum()
        maxabs = np.abs(pconv_emp_norm - vec).max()
        print(f"  {name:<25}  {l1:>10.4f}  {maxabs:>11.5f}")
        distances.append(dict(case=name, l1=round(l1, 4),
                              max_abs_diff=round(float(maxabs), 5)))
    pd.DataFrame(distances).to_csv(
        TBL_DIR / "distance-empirical-vs-current.csv", index=False
    )

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
