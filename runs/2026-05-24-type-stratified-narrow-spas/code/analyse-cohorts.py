#!/usr/bin/env python3
"""
analyse-cohorts.py
==================

Per-type narrow-dated SPAs for three calibration-cohort definitions,
plus year-by-year waterfall heatmaps, plus type-reweighted aggregate
p_gen. Implements the Family classifier (F1 round-number slabs, F3
periodic windows, F2 reign-windows, Tight, Big) and uses it to define
methodologically defensible empirical-Bayes calibration cohorts.

Three cohort definitions:

- Cohort A — Tight: date_range ≤ 4. Gold standard control.
- Cohort B — Family-filtered: Tight ∪ "Other" (5-48y, not F1, not F3).
  Includes reign-window content; excludes editorial slabs.
- Cohort C — Width-23: date_range ≤ 23. Conservative width-only baseline.

Family classifier (rules):

- F1 (round-number slab): date_range ∈ {24, 49, 99, 149, 199, 299}
  AND both endpoints multiples of 25 (allowing ±1 for inclusive-endpoint
  convention).
- F3 (periodic 30-y windows): date_range ∈ {19, 29, 39} AND both
  endpoints multiples of 10 (allowing ±1), AND not in F1.
- Tight: date_range ≤ 4.
- Big: date_range ≥ 49 AND not F1.
- F2 / Other: the residual — date_range ∈ [5, 48] and not in F1 or F3.
  Empirically dominated by reign-window templates.

Outputs:

- outputs/figures/family-classification-summary.png
- outputs/figures/per-type-spas-by-cohort.png (9 types × 3 cohorts grid)
- outputs/figures/reweighted-pgen-by-cohort.png (overlay)
- outputs/figures/waterfall-aggregate.png (cutoff × year heatmap, agg)
- outputs/figures/waterfall-per-type.png (cutoff × year heatmap, per type)
- outputs/tables/family-classification-counts.csv
- outputs/tables/cohort-summary.csv
- outputs/tables/cohort-type-composition.csv
- outputs/tables/reweighting-weights.csv

Inputs: archive/data-2026-04-22/LIRE_v3-0.parquet
Author / Date: Claude Opus 4.7, 2026-05-24.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


DATA_PATH = Path("/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet")
RUN_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = RUN_ROOT / "outputs" / "figures"
TBL_DIR = RUN_ROOT / "outputs" / "tables"

# Time envelope for SPAs (we use 50 BC – AD 400 to give a bit of buffer
# beyond the prereg 50 BC – AD 350 window).
ENV_START = -50
ENV_END = 400
BIN_SIZE = 5  # years per SPA bin

# Family classification constants
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4  # ≤ this is "tight"

# Type-simplification mapping (same as the prior threshold analysis)
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


def round_aligned(x, mod):
    """Return mask of values aligned to a `mod`-year grid, allowing the
    inclusive-endpoint off-by-one convention."""
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def classify_family(lire: pd.DataFrame) -> pd.Series:
    """Return a Categorical with one of: F1, F3, Tight, F2_Other, Big."""
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
    family[big_mask] = "Big"  # Already default but explicit
    return pd.Categorical(
        family,
        categories=["Tight", "F2_Other", "F1_round", "F3_periodic", "Big"],
        ordered=True,
    )


def simplify_type(t: pd.Series) -> pd.Categorical:
    cat = t.map(TYPE_MAPPING).fillna("unknown")
    return pd.Categorical(cat, categories=TYPE_ORDER, ordered=True)


def compute_spa(
    df: pd.DataFrame, env_start: int = ENV_START,
    env_end: int = ENV_END, bin_size: int = BIN_SIZE,
) -> np.ndarray:
    """Compute summed probability of activity (uniform aoristic spread).

    For each inscription, spread probability mass 1.0 uniformly over
    [not_before, not_after]. Sum across inscriptions. Returns the SPA
    vector with bins of size bin_size from env_start to env_end."""
    n_bins = (env_end - env_start) // bin_size
    bin_centres = np.arange(env_start + bin_size / 2,
                            env_end, bin_size, dtype=float)
    spa = np.zeros(n_bins)

    nb = df["not_before"].to_numpy()
    na = df["not_after"].to_numpy()
    # Clip to envelope
    nb = np.maximum(nb, env_start)
    na = np.minimum(na, env_end)
    # Width after clipping
    width = na - nb
    valid = width > 0
    nb = nb[valid]
    na = na[valid]
    width = width[valid]

    # For each bin, sum (overlap with [nb, na]) / width
    bin_edges = np.arange(env_start, env_end + bin_size, bin_size, dtype=float)
    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        overlap = np.minimum(hi, na) - np.maximum(lo, nb)
        overlap = np.maximum(overlap, 0)
        spa[i] = (overlap / width).sum()
    return bin_centres, spa


def make_cohorts(lire: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build three cohort dataframes."""
    cohort_a = lire[lire["family"] == "Tight"].copy()  # ≤4y
    cohort_b = lire[lire["family"].isin(["Tight", "F2_Other"])].copy()  # Family-filtered
    cohort_c = lire[lire["date_range"] <= 23].copy()  # Width-based ≤23
    return {"A_Tight": cohort_a, "B_FamFilt": cohort_b, "C_Width23": cohort_c}


def family_summary(lire: pd.DataFrame) -> None:
    """Tabulate + plot the family classification."""
    n = len(lire)
    rows = []
    for fam in lire["family"].cat.categories:
        sub = lire[lire["family"] == fam]
        rows.append(dict(
            family=fam,
            count=int(len(sub)),
            pct=round(100 * len(sub) / n, 2),
            median_date_range=int(sub["date_range"].median()) if len(sub) else 0,
            mean_date_range=round(sub["date_range"].mean(), 1) if len(sub) else 0,
        ))
    df = pd.DataFrame(rows)
    out = TBL_DIR / "family-classification-counts.csv"
    df.to_csv(out, index=False)
    print(f"\n=== Family classification ===")
    print(df.to_string(index=False))
    print(f"  wrote {out}")

    # Figure
    fig, ax = plt.subplots(figsize=(10, 5))
    colours = {
        "Tight": "#2ECC71",       # green
        "F2_Other": "#3498DB",    # blue
        "F1_round": "#E74C3C",    # red (BAD)
        "F3_periodic": "#F39C12", # orange (BAD)
        "Big": "#95A5A6",         # grey
    }
    bars = ax.bar(
        df["family"], df["count"],
        color=[colours[f] for f in df["family"]],
    )
    for bar, pct in zip(bars, df["pct"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{pct:.1f}%", ha="center", va="bottom", fontsize=10,
        )
    ax.set_ylabel("Count of inscriptions")
    ax.set_title(
        "LIRE v3.0 — Family classification\n"
        "Tight + F2_Other = candidate calibration cohort (legitimate dates + reign-windows)\n"
        "F1_round + F3_periodic = editorial artefacts to exclude; Big = too wide for cohort"
    )
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "family-classification-summary.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")


def cohort_summary(cohorts: dict[str, pd.DataFrame]) -> None:
    """Cohort sizes + type composition + Williams ΔT."""
    rows = []
    for name, df in cohorts.items():
        sigma = (df["date_range"] / np.sqrt(12)).mean()
        rows.append(dict(
            cohort=name,
            n_records=int(len(df)),
            pct_of_corpus=round(100 * len(df) / 182853, 2),
            mean_date_range=round(df["date_range"].mean(), 2),
            median_date_range=int(df["date_range"].median()),
            mean_sigma_years=round(sigma, 2),
        ))
    df = pd.DataFrame(rows)
    out = TBL_DIR / "cohort-summary.csv"
    df.to_csv(out, index=False)
    print(f"\n=== Cohort summary ===")
    print(df.to_string(index=False))
    print(f"  wrote {out}")


def type_composition(cohorts: dict[str, pd.DataFrame], full_corpus: pd.DataFrame) -> None:
    """Type composition for each cohort."""
    rows = []
    full_n = len(full_corpus)
    full_counts = full_corpus["type_simple"].value_counts().reindex(TYPE_ORDER, fill_value=0)
    full_pct = (full_counts / full_n * 100).round(2)
    rows.append({"cohort": "full_corpus", "N": full_n,
                 **{t: full_pct[t] for t in TYPE_ORDER}})
    for name, df in cohorts.items():
        counts = df["type_simple"].value_counts().reindex(TYPE_ORDER, fill_value=0)
        pct = (counts / len(df) * 100).round(2)
        rows.append({"cohort": name, "N": len(df),
                     **{t: pct[t] for t in TYPE_ORDER}})
    out_df = pd.DataFrame(rows)
    out = TBL_DIR / "cohort-type-composition.csv"
    out_df.to_csv(out, index=False)
    print(f"\n=== Cohort type composition (% within cohort) ===")
    print(out_df.to_string(index=False))
    print(f"  wrote {out}")


def per_type_spas(
    cohorts: dict[str, pd.DataFrame], full_corpus: pd.DataFrame,
) -> tuple[dict[str, dict[str, np.ndarray]], np.ndarray]:
    """Compute per-type SPA for each cohort. Returns nested dict
    {cohort_name: {type: spa_vector}} plus the bin_centres vector."""
    bin_centres = None
    results = {}
    for cohort_name, df in cohorts.items():
        results[cohort_name] = {}
        for t in TYPE_ORDER:
            sub = df[df["type_simple"] == t]
            if len(sub) == 0:
                bc, spa = compute_spa(df.head(0))  # zeros
            else:
                bc, spa = compute_spa(sub)
            if bin_centres is None:
                bin_centres = bc
            results[cohort_name][t] = spa
    return results, bin_centres


def plot_per_type_spas(
    spas: dict[str, dict[str, np.ndarray]],
    bin_centres: np.ndarray,
    cohorts: dict[str, pd.DataFrame],
) -> None:
    """Grid figure: TYPE_ORDER rows × cohort columns."""
    # Drop types with zero records across all cohorts to declutter
    active_types = [
        t for t in TYPE_ORDER
        if any(spas[c][t].sum() > 0 for c in spas)
    ]
    n_types = len(active_types)
    n_cohorts = len(spas)
    fig, axes = plt.subplots(
        n_types, n_cohorts, figsize=(3.5 * n_cohorts, 1.8 * n_types),
        sharex=True, squeeze=False,
    )
    cohort_labels = list(spas.keys())
    for i, t in enumerate(active_types):
        for j, c in enumerate(cohort_labels):
            ax = axes[i][j]
            spa = spas[c][t]
            n_records = (cohorts[c]["type_simple"] == t).sum()
            # Normalise so SPAs are comparable
            total = spa.sum()
            spa_norm = spa / total if total > 0 else spa
            ax.fill_between(bin_centres, spa_norm, alpha=0.4, color="C0")
            ax.plot(bin_centres, spa_norm, color="C0", linewidth=0.8)
            ax.set_xlim(ENV_START, ENV_END)
            ax.tick_params(labelsize=7)
            if i == 0:
                ax.set_title(c, fontsize=10)
            if j == 0:
                ax.set_ylabel(t, fontsize=8, rotation=0, ha="right", va="center")
            ax.text(
                0.97, 0.92, f"n={n_records:,}",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=7, color="#444",
            )
            ax.grid(True, alpha=0.2)
    fig.suptitle(
        "Per-type SPA by cohort — LIRE v3.0\n"
        "Each row = inscription type; each column = candidate calibration cohort.\n"
        "Normalised within panel; n in top-right",
        fontsize=11,
    )
    fig.text(0.5, 0.01, "Year (AD)", ha="center")
    fig.tight_layout(rect=[0, 0.02, 1, 0.97])
    out = FIG_DIR / "per-type-spas-by-cohort.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\n  wrote {out}")


def reweighted_pgen(
    spas: dict[str, dict[str, np.ndarray]],
    bin_centres: np.ndarray,
    full_corpus: pd.DataFrame,
) -> None:
    """For each cohort, compute reweighted aggregate p_gen by post-
    stratification on type composition. Save weights table; plot
    overlay."""
    # Corpus type composition (target weights)
    corpus_type_counts = full_corpus["type_simple"].value_counts()
    corpus_total = len(full_corpus)
    target_weights = (corpus_type_counts / corpus_total).reindex(TYPE_ORDER, fill_value=0)

    # For each cohort: compute reweighted p_gen
    weight_rows = []
    fig, ax = plt.subplots(figsize=(12, 6))
    colours = {"A_Tight": "C0", "B_FamFilt": "C2", "C_Width23": "C3"}

    for cohort_name, type_spas in spas.items():
        # Type counts in cohort
        # Sum of SPA per type gives total records of that type that fall
        # in envelope; for weighting we need fraction of cohort that is
        # each type — use direct counts from the cohort frame would be
        # cleaner but for the reweighting we just need the per-type SPA.
        # Reweighting formula: pgen_reweighted = sum_type [w_target_type * spa_type / spa_type.sum()]
        pgen_re = np.zeros_like(bin_centres)
        for t in TYPE_ORDER:
            spa_t = type_spas[t]
            if spa_t.sum() == 0:
                continue
            spa_t_norm = spa_t / spa_t.sum()  # density per type
            w = target_weights[t]             # corpus target fraction
            pgen_re += w * spa_t_norm
            weight_rows.append(dict(
                cohort=cohort_name, type=t,
                target_weight=round(w, 4),
                in_cohort_total=int(spa_t.sum()),
                contributes_to_pgen=spa_t.sum() > 0,
            ))
        # Renormalise (numerical safety)
        if pgen_re.sum() > 0:
            pgen_re = pgen_re / pgen_re.sum()
        ax.plot(
            bin_centres, pgen_re,
            label=f"Cohort {cohort_name}",
            color=colours.get(cohort_name, "k"), linewidth=1.6,
        )

    # For reference, the unweighted aggregate of cohort B
    ag_b_unw = sum(spas["B_FamFilt"].values())
    if ag_b_unw.sum() > 0:
        ag_b_unw = ag_b_unw / ag_b_unw.sum()
        ax.plot(
            bin_centres, ag_b_unw,
            label="Cohort B unweighted (for reference)",
            color="C2", linestyle="--", linewidth=1.0, alpha=0.7,
        )

    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD)")
    ax.set_ylabel("Reweighted p_gen (density)")
    ax.set_title(
        "Type-reweighted aggregate p_gen by cohort — LIRE v3.0\n"
        "Reweighting matches each cohort's type composition to the full corpus.\n"
        "This is what the empirical-Bayes prior on p_gen would actually be."
    )
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = FIG_DIR / "reweighted-pgen-by-cohort.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")

    # Weights table
    weights_df = pd.DataFrame(weight_rows)
    out_t = TBL_DIR / "reweighting-weights.csv"
    weights_df.to_csv(out_t, index=False)
    print(f"  wrote {out_t}")


def waterfall(lire: pd.DataFrame) -> None:
    """Year-by-year cutoff sweep: x = year, y = cutoff (1..50), colour = SPA density.
    Aggregate version + per-type version."""
    # Aggregate
    cutoffs = np.arange(1, 51)
    n_bins = (ENV_END - ENV_START) // BIN_SIZE
    grid = np.zeros((len(cutoffs), n_bins))
    bin_centres = np.arange(ENV_START + BIN_SIZE / 2, ENV_END, BIN_SIZE)
    for i, c in enumerate(cutoffs):
        sub = lire[lire["date_range"] <= c]
        if len(sub) == 0:
            continue
        bc, spa = compute_spa(sub)
        # Normalise so each row sums to 1 — shows shape, not amplitude
        grid[i, :] = spa / spa.sum() if spa.sum() > 0 else spa

    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(
        grid, aspect="auto", origin="lower",
        extent=[ENV_START, ENV_END, cutoffs.min() - 0.5, cutoffs.max() + 0.5],
        cmap="viridis",
    )
    # Mark editorial-slab anchors as horizontal lines
    for slab in [19, 24, 29, 39, 49]:
        if slab <= 50:
            ax.axhline(slab - 0.5, color="red", linestyle="--",
                       alpha=0.5, linewidth=0.8)
            ax.text(ENV_END + 5, slab, f"{slab}y", color="red", fontsize=8,
                    va="center")
    ax.set_xlabel("Year (AD; envelope 50 BC – AD 400)")
    ax.set_ylabel("Cutoff (date_range ≤ N years)")
    ax.set_title(
        "Waterfall: aggregate SPA shape vs cutoff — LIRE v3.0\n"
        "Each row is the within-row-normalised SPA for inscriptions with date_range ≤ row-value.\n"
        "Red dashes mark editorial-artefact-width thresholds (19, 24, 29, 39, 49)"
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Within-row normalised SPA density")
    fig.tight_layout()
    out = FIG_DIR / "waterfall-aggregate.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"\n  wrote {out}")

    # Per-type waterfall — grid of 4 most-populated types
    pop_types = ["epitaph (funerary)", "honorific", "identification",
                 "votive", "building/dedicatory", "military diploma"]
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharex=True, sharey=True)
    for ax, t in zip(axes.flatten(), pop_types):
        grid_t = np.zeros((len(cutoffs), n_bins))
        for i, c in enumerate(cutoffs):
            sub = lire[(lire["date_range"] <= c) & (lire["type_simple"] == t)]
            if len(sub) < 5:
                continue
            bc, spa = compute_spa(sub)
            grid_t[i, :] = spa / spa.sum() if spa.sum() > 0 else spa
        im = ax.imshow(
            grid_t, aspect="auto", origin="lower",
            extent=[ENV_START, ENV_END, cutoffs.min() - 0.5, cutoffs.max() + 0.5],
            cmap="viridis",
        )
        for slab in [19, 24, 29, 39, 49]:
            ax.axhline(slab - 0.5, color="red", linestyle="--",
                       alpha=0.4, linewidth=0.6)
        ax.set_title(t, fontsize=10)
    fig.text(0.5, 0.02, "Year (AD)", ha="center")
    fig.text(0.02, 0.5, "Cutoff (date_range ≤ N years)", va="center",
             rotation=90)
    fig.suptitle(
        "Waterfall: per-type SPA shape vs cutoff — LIRE v3.0\n"
        "Red dashes mark editorial-artefact-width thresholds",
        fontsize=12,
    )
    fig.tight_layout(rect=[0.03, 0.03, 1, 0.97])
    out = FIG_DIR / "waterfall-per-type.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  wrote {out}")


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TBL_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading LIRE v3.0...")
    lire = pd.read_parquet(DATA_PATH)
    lire["date_range"] = lire["not_after"] - lire["not_before"]
    lire["family"] = classify_family(lire)
    lire["type_simple"] = simplify_type(lire["type_of_inscription_auto"])
    print(f"  loaded {len(lire):,} records")

    family_summary(lire)
    cohorts = make_cohorts(lire)
    cohort_summary(cohorts)
    type_composition(cohorts, lire)

    print("\nComputing per-type SPAs...")
    spas, bin_centres = per_type_spas(cohorts, lire)
    plot_per_type_spas(spas, bin_centres, cohorts)
    reweighted_pgen(spas, bin_centres, lire)

    print("\nComputing waterfall...")
    waterfall(lire)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
