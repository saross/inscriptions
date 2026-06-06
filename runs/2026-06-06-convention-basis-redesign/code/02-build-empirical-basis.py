#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""02-build-empirical-basis.py — Decision 38 step 2: empirical 3-tier convention basis.

Purpose
-------
Build the production convention basis (``p_conv`` template) for the H2.1
temporal-mixture model from the *empirical* prereg-filtered F1+F3 calendar
population, under the Decision 38 redesign and Shawn's Option-2 choice
(2026-06-06):

  * 3 LEARNED tiers, 5 CORE calendar slabs only:
      - sub_century   : half-century (exclusive width 49)
      - century       : century       (width 99)
      - multi_century : 1.5- + 2- + 3-century (widths 149, 199, 299), pooled
  * Each tier basis row is the frequency-weighted aoristic SPA of the actual
    inscriptions in that tier's slab-widths (NOT a theoretical uniform over
    canonical templates) — Decision 38 sec 3 ("frequency-weighted from the
    F1+F3 calendar population").
  * The FINE brackets (quarter-century w24; 20/30/40-y windows w19/29/39) are
    EXCLUDED from the primary p_conv (Option 2) -> they fall to genuine in the
    primary fit. Their anchor-stripped pooled SPA is built separately as the
    add-them-back SENSITIVITY-band component.
  * Reign/dynasty/event leaks are stripped from the convention pool via the
    curated historical-anchor list (Decision 38 step 1). For the 5 core slabs
    this removes nothing (anchor-clean by construction); for the fine-bracket
    sensitivity component it removes the [161,180] leak (129 inscriptions).
  * NO reign tier (Decision 38 supersedes Decision 20's reign tier).

The basis SHAPE is built once per frame (empire primary/context; Latin primary
per Decision 36) and is a FIXED, unit-independent convention template shared
across every H2.1 unit — a per-unit basis would absorb that unit's genuine
temporal signal into p_conv and defeat the deconvolution. The learned Dirichlet
tier weights + alpha + GRW p_gen carry all per-unit variation.

Outputs
-------
design.json                          — the frozen basis artefact (this run dir)
outputs/figures/basis-rows.png       — the 3 core tier rows + fine-bracket row
outputs/tables/tier-weights-empirical.csv
outputs/REPORT.md                    — PART-2 design report

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet
runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv
runs/2026-06-06-convention-basis-redesign/historical-anchor-intervals.json
runs/2026-05-22-recovery-grid-design/design.json  (shape_library / alpha_grid / n_grid reuse)

Status
------
PROPOSAL pending Shawn sign-off + recovery re-validation + OSF amendment. The
basis is NOT wired into a production fit by this script; it freezes the artefact
the re-validation generates synthetics from and the production fit will consume.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-06.
UK/Australian English; Oxford comma. Deterministic (pure counting + SPA).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = (
    PROJECT_ROOT / "runs" / "2026-06-04-h3a-confirmatory" / "data"
    / "province-language-map.csv"
)
ANCHOR_JSON = RUN_DIR / "historical-anchor-intervals.json"
OLD_DESIGN = PROJECT_ROOT / "runs" / "2026-05-22-recovery-grid-design" / "design.json"
DESIGN_OUT = RUN_DIR / "design.json"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"
REPORT_OUT = RUN_DIR / "outputs" / "REPORT.md"
FIG_DIR.mkdir(parents=True, exist_ok=True)
TBL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Envelope (prereg; matches cell_lib.Envelope and build-empirical-pconv).
# ---------------------------------------------------------------------------
ENV_START = -50
ENV_END = 350
BIN_SIZE = 5
N_BINS = (ENV_END - ENV_START) // BIN_SIZE  # 80
EXPECTED_N = 180_609

# Family-classifier constants (build-empirical-pconv.py). EXCLUSIVE width.
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4

# Tier definitions under Decision 38 / Option 2 (exclusive widths).
TIER_DEFS = {
    "sub_century": [49],            # half-century
    "century": [99],               # century
    "multi_century": [149, 199, 299],  # 1.5 / 2 / 3 century, pooled
}
TIER_ORDER = ["sub_century", "century", "multi_century"]
FINE_BRACKET_WIDTHS = [24, 19, 29, 39]  # quarter-century + 20/30/40-y windows


def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def load_filtered_lire() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    is_geotemporal = (
        df["Latitude"].notna() & df["Longitude"].notna()
        & df["not_before"].notna() & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    in_envelope = (df["not_after"] >= ENV_START) & (df["not_before"] <= ENV_END)
    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["nb"] = sub["not_before"].astype(int)
    sub["na"] = sub["not_after"].astype(int)
    sub["date_range"] = (sub["na"] - sub["nb"]).astype(int)
    if len(sub) != EXPECTED_N:
        raise ValueError(f"Filtered corpus {len(sub):,} != expected {EXPECTED_N:,}.")
    return sub


def classify_family(df: pd.DataFrame) -> np.ndarray:
    nb = df["nb"].to_numpy()
    na = df["na"].to_numpy()
    dr = df["date_range"].to_numpy()
    f1 = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3 = np.isin(dr, list(F3_WIDTHS)) & round_aligned(nb, 10) & round_aligned(na, 10) & ~f1
    fam = np.full(len(df), "Big", dtype=object)
    tight = (dr <= TIGHT_MAX) & ~f1 & ~f3
    big = (dr >= 49) & ~f1
    other = ~(f1 | f3 | tight | big)
    fam[f1] = "F1_round"
    fam[f3] = "F3_periodic"
    fam[tight] = "Tight"
    fam[other] = "F2_Other"
    fam[big] = "Big"
    return fam


def latin_provinces() -> set[str]:
    m = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    return set(m.loc[m["language"] == "Latin", "lire_province"])


def load_anchor_intervals() -> list[tuple[int, int]]:
    spec = json.loads(ANCHOR_JSON.read_text(encoding="utf-8"))
    return [(iv["lo"], iv["hi"]) for iv in spec["intervals"]], int(
        spec["match_rule"]["endpoint_tolerance_years"]
    )


def anchor_mask(df: pd.DataFrame, anchors, tol: int) -> np.ndarray:
    """True where [nb, na] matches any anchor within +/- tol on both endpoints."""
    nb = df["nb"].to_numpy()
    na = df["na"].to_numpy()
    m = np.zeros(len(df), dtype=bool)
    for lo, hi in anchors:
        m |= (np.abs(nb - lo) <= tol) & (np.abs(na - hi) <= tol)
    return m


# Envelope grid (edges + centres) shared by aoristic SPA.
BIN_EDGES = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0


def aoristic_spa(nb: np.ndarray, na: np.ndarray) -> np.ndarray:
    """Aoristic SPA on the envelope; each inscription deposits mass 1.0 uniformly
    across [nb, na] using ORIGINAL width as denominator, clipped to the envelope
    (identical convention to build-empirical-pconv.aoristic_spa)."""
    spa = np.zeros(N_BINS)
    if len(nb) == 0:
        return spa
    nb = nb.astype(float)
    na = na.astype(float)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb
    valid = (width > 0) & (na_c > nb_c)
    nb_c, na_c, width = nb_c[valid], na_c[valid], width[valid]
    for i in range(N_BINS):
        lo, hi = BIN_EDGES[i], BIN_EDGES[i + 1]
        overlap = np.maximum(np.minimum(hi, na_c) - np.maximum(lo, nb_c), 0.0)
        spa[i] = (overlap / width).sum()
    return spa


def normalise(v: np.ndarray) -> np.ndarray:
    s = v.sum()
    return v / s if s > 0 else v


def build_frame_basis(conv: pd.DataFrame) -> dict:
    """Build the 3 core tier rows + fine-bracket row for one frame.

    `conv` is the F1+F3 pool with anchor leaks ALREADY stripped.
    Returns dict with tier_basis (3 x N_BINS), tier counts, empirical tier
    weights, and the anchor-stripped fine-bracket row + count.
    """
    rows = []
    counts = {}
    for tier in TIER_ORDER:
        widths = TIER_DEFS[tier]
        sub = conv[conv["date_range"].isin(widths)]
        counts[tier] = int(len(sub))
        rows.append(normalise(aoristic_spa(sub["nb"].to_numpy(), sub["na"].to_numpy())))
    basis = np.vstack(rows)  # (3, N_BINS), each row sums to 1
    core_total = sum(counts.values())
    tier_weights_emp = np.array([counts[t] / core_total for t in TIER_ORDER])

    fine = conv[conv["date_range"].isin(FINE_BRACKET_WIDTHS)]
    fine_row = normalise(aoristic_spa(fine["nb"].to_numpy(), fine["na"].to_numpy()))
    return {
        "tier_basis": basis,
        "tier_counts": counts,
        "core_total": core_total,
        "tier_weights_empirical": tier_weights_emp,
        "fine_bracket_row": fine_row,
        "fine_bracket_count": int(len(fine)),
    }


def main() -> None:
    print(f"Loading {DATA_PATH} ...")
    df = load_filtered_lire()
    df["family"] = classify_family(df)
    print(f"  empire-filtered rows: {len(df):,}  OK")

    anchors, tol = load_anchor_intervals()
    print(f"  loaded {len(anchors)} historical-anchor intervals (tol +/-{tol})")

    latin = latin_provinces()
    df_lat = df.loc[df["province"].isin(latin)].copy()

    frames = {}
    for label, frame_df in [("empire", df), ("latin", df_lat)]:
        conv = frame_df[np.isin(frame_df["family"], ["F1_round", "F3_periodic"])].copy()
        leak = anchor_mask(conv, anchors, tol)
        n_leak = int(leak.sum())
        conv_clean = conv.loc[~leak].copy()
        print(
            f"  [{label}] F1+F3 pool={len(conv):,}  anchor-leak stripped={n_leak}"
            f"  -> clean pool={len(conv_clean):,}"
        )
        fb = build_frame_basis(conv_clean)
        fb["pool_n"] = len(conv_clean)
        fb["anchor_leak_stripped"] = n_leak
        frames[label] = fb

    # --- Tier-weight grid (order: sub_century, century, multi_century) ---
    emp_emp = frames["empire"]["tier_weights_empirical"]
    tier_weight_grid = [
        {"name": "uniform", "weights": [1 / 3, 1 / 3, 1 / 3]},
        {"name": "subcentury_heavy", "weights": [0.70, 0.20, 0.10]},
        {"name": "century_heavy", "weights": [0.20, 0.70, 0.10]},
        {"name": "multicentury_heavy", "weights": [0.10, 0.10, 0.80]},
        {"name": "empirical", "weights": [round(float(w), 6) for w in emp_emp]},
    ]

    # --- Reuse shape_library / alpha_grid / n_grid from the validated grid ---
    old = json.loads(OLD_DESIGN.read_text(encoding="utf-8"))

    design = {
        "schema_version": "2.0",
        "design_artefact_id": "2026-06-06-convention-basis-redesign",
        "supersedes": "2026-05-22-recovery-grid-design (tier structure only)",
        "binds": {
            "decisions": [35, 36, 37, 38],
            "option": "Decision 38 Option 2 (3 tiers, fine brackets excluded from primary)",
        },
        "envelope": {
            "envelope_min_year": ENV_START, "envelope_max_year": ENV_END,
            "bin_width_years": BIN_SIZE, "n_bins": N_BINS,
        },
        "tier_order": TIER_ORDER,
        "tier_definitions_exclusive_width": TIER_DEFS,
        "fine_bracket_widths_excluded_from_primary": FINE_BRACKET_WIDTHS,
        "basis_construction": (
            "Empirical: each tier row is the frequency-weighted aoristic SPA of "
            "all anchor-stripped F1+F3 inscriptions whose exclusive width is in "
            "that tier's slab-widths. Fixed, unit-independent, shared across all "
            "H2.1 units. Built per frame."
        ),
        "tier_basis_empirical": frames["empire"]["tier_basis"].tolist(),
        "tier_basis_empirical_latin": frames["latin"]["tier_basis"].tolist(),
        "fine_bracket_row_empire": frames["empire"]["fine_bracket_row"].tolist(),
        "fine_bracket_row_latin": frames["latin"]["fine_bracket_row"].tolist(),
        "provenance_counts": {
            label: {
                "pool_n_anchor_clean": frames[label]["pool_n"],
                "anchor_leak_stripped": frames[label]["anchor_leak_stripped"],
                "tier_counts": frames[label]["tier_counts"],
                "core_total": frames[label]["core_total"],
                "tier_weights_empirical": [
                    round(float(w), 6) for w in frames[label]["tier_weights_empirical"]
                ],
                "fine_bracket_count": frames[label]["fine_bracket_count"],
            }
            for label in ("empire", "latin")
        },
        # --- recovery-validation axes (reused from the validated grid) ---
        "base_seed": 20260606,
        "replicates_per_cell": old["replicates_per_cell"],
        "seed_policy": old["seed_policy"],
        "alpha_grid": old["alpha_grid"],
        "shape_library": old["shape_library"],
        "tier_weight_grid": tier_weight_grid,
        "n_grid": old["n_grid"],
        "decision_rule": old["decision_rule"],
        "anchor_list_ref": "historical-anchor-intervals.json",
        "status": "PROPOSAL pending sign-off + recovery re-validation + OSF amendment",
        "built": "2026-06-06",
    }
    DESIGN_OUT.write_text(json.dumps(design, indent=2), encoding="utf-8")
    print(f"\nWrote {DESIGN_OUT}")

    # --- tier-weights table ---
    tw_rows = []
    for label in ("empire", "latin"):
        f = frames[label]
        for i, tier in enumerate(TIER_ORDER):
            tw_rows.append({
                "frame": label, "tier": tier,
                "n_inscriptions": f["tier_counts"][tier],
                "empirical_weight": round(float(f["tier_weights_empirical"][i]), 4),
            })
    pd.DataFrame(tw_rows).to_csv(TBL_DIR / "tier-weights-empirical.csv", index=False)

    # --- figure: the 3 core rows + fine-bracket row (empire) + old basis ---
    fig, ax = plt.subplots(figsize=(13, 6))
    colours = {"sub_century": "tab:blue", "century": "tab:green",
               "multi_century": "tab:red"}
    for i, tier in enumerate(TIER_ORDER):
        ax.plot(BIN_CENTRES, frames["empire"]["tier_basis"][i],
                color=colours[tier], lw=2,
                label=f"{tier} (n={frames['empire']['tier_counts'][tier]:,})")
    ax.plot(BIN_CENTRES, frames["empire"]["fine_bracket_row"],
            color="grey", lw=1.3, ls="--",
            label=f"fine brackets (excluded; n={frames['empire']['fine_bracket_count']:,})")
    ax.set_xlim(ENV_START, ENV_END)
    ax.set_xlabel("Year (AD; 50 BC – AD 350 envelope)")
    ax.set_ylabel("Basis density (5-y bins; each row sums to 1)")
    ax.set_title(
        "Decision 38 / Option 2 empirical convention basis (empire frame)\n"
        "3 core learned tiers; fine brackets excluded from primary (dashed)"
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "basis-rows.png", dpi=150)
    plt.close(fig)
    print(f"Wrote {FIG_DIR / 'basis-rows.png'}")

    # --- console summary of the multi-century plateau (Decision 38 sec 6 risk) ---
    mc = frames["empire"]["tier_basis"][TIER_ORDER.index("multi_century")]
    print("\nMulti-century row (empire) diagnostics — the recovery-hard plateau:")
    print(f"  max/min density ratio: {mc.max() / mc[mc > 0].min():.2f}")
    print(f"  mass in last 10 bins (AD 300-350): {mc[-10:].sum():.4f}")
    print(f"  mass in first 10 bins (50 BC-AD 0): {mc[:10].sum():.4f}")
    print(f"  flat-core (bins 20-60, AD 50-250) mean density: {mc[20:60].mean():.5f}")

    print("\nEmpirical tier weights (empire):",
          [round(float(w), 4) for w in emp_emp])
    print("Done. PROPOSAL artefact written; nothing launched.")


if __name__ == "__main__":
    main()
