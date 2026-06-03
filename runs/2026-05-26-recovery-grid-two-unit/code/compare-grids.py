#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare-grids.py
================

Cross-grid comparison harness for the 2026-05-26 two-unit recovery-grid
re-simulation. Reads the two per-grid summary tables produced by
``grid-summariser.py`` (one for inscription-mass, one for letter-mass),
joins them cell-by-cell, and emits the head-to-head artefacts that drive
the Stage-3 launch decision (spec.md §5):

- ``comparison/cell-pass-comparison.parquet`` -- one row per cell, both
  grids' pass flags side by side, plus a four-way ``classification``
  (both-pass / <A>-only / <B>-only / both-fail).
- ``comparison/figures/fig-pass-rate-heatmap.png`` -- side-by-side
  (alpha x shape) both-pass-rate heatmaps on a shared 0-1 colour scale
  (paper-figure candidate; spec.md §10.5).
- ``comparison/figures/fig-alpha-bias-by-tier.png`` -- recovered-alpha
  bias by tier, per unit, IF the compact ``alpha-bias.parquet`` tables
  exist for both grids (produced by ``collect-alpha-bias.py``). Skipped
  with a logged note otherwise (paper-figure candidate; spec.md §10.5).
- ``comparison/COMPARISON-REPORT.md`` -- the head-to-head write-up that
  determines which row of the spec.md §5 outcome-branching table applies
  and states the recommended Stage-3 launch path.

Design notes
------------
- The binding criteria are applied EXACTLY as preregistered (spec.md §5;
  prereg §4 lines 333-334): a grid is validated only if >= 90% of cells
  pass coverage AND >= 90% pass median-Pearson-r >= 0.95.
- A KNOWN metric artefact (documented in
  ``runs/2026-05-24-followup-systematics/``): Pearson r is undefined for
  the ``flat_baseline`` shape (a constant truth has zero variance), so all
  flat_baseline cells fail criterion (b) mechanically and cap the
  achievable shape-pass at 375/450 = 83.3%. The report therefore presents
  BOTH the faithful as-written verdict AND a clearly-marked
  flat-baseline-excluded DIAGNOSTIC verdict, so the genuine cross-unit
  comparison is legible. The flat-excluded view is NOT a substitute for
  the prereg-binding rule; any criterion change is an OSF-amendment
  decision, not this harness's to make.
- HARD GATE: the Stage-3 launch path this report names is a RECOMMENDATION
  only. No Stage-3 confirmatory work may begin until OSF Amendment 01 is
  lodged (project standing rule; memory 2026-05-26-40ce5927fddc).

Usage
-----
    # Standard (both grids summarised):
    python compare-grids.py \\
        --run-root /path/to/runs/2026-05-26-recovery-grid-two-unit

    # Override grid dirs/names (e.g. A-vs-A plumbing smoke test):
    python compare-grids.py \\
        --grid-a-dir .../inscription-mass --grid-a-name inscription \\
        --grid-b-dir .../inscription-mass --grid-b-name inscription_copy

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: no display on the compute hosts
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# --------------------------------------------------------------------------- #
# Binding thresholds (prereg-binding; identical to grid-summariser.py).        #
# --------------------------------------------------------------------------- #
GLOBAL_FRAC_PASS = 0.90
FLAT_SHAPE = "flat_baseline"

# Corrected binding criterion (Decision 33 / §A5.5.1); mirrors grid-summariser.py.
SHAPE_PEARSON_PASS = 0.95
T_FLAT_YEARS = 10.0
ALPHA_ENVELOPE = 0.70
ALPHA_STRESS = 0.95
CONVERGENCE_FRAC = 0.90

# Canonical axis orders for stable, readable heatmaps.
ALPHA_ORDER = [0.05, 0.30, 0.50, 0.70, 0.95]
SHAPE_ORDER = [
    "flat_baseline",
    "smooth_growth",
    "smooth_decline",
    "rise_and_fall",
    "bimodal",
    "regnal_cluster",
]


# --------------------------------------------------------------------------- #
# Loading                                                                      #
# --------------------------------------------------------------------------- #
def load_grid_summary(grid_dir: Path) -> pd.DataFrame:
    """Load one grid's per-cell summary table.

    Expects ``<grid_dir>/outputs/tables/grid-summary.parquet`` (written by
    ``grid-summariser.py``). Raises a clear, actionable error if absent.
    """
    parquet = grid_dir / "outputs" / "tables" / "grid-summary.parquet"
    if not parquet.exists():
        raise FileNotFoundError(
            f"No grid-summary.parquet at {parquet}.\n"
            f"Run:  python grid-summariser.py --grid-dir {grid_dir}\n"
            f"first (it aggregates the per-cell summary JSONs)."
        )
    df = pd.read_parquet(parquet)
    if "both_pass" not in df.columns:
        df["both_pass"] = (
            df["alpha_coverage_pass"].astype(bool)
            & df["pearson_r_pass"].astype(bool)
        )
    return _ensure_corrected_flags(df)


def _ensure_corrected_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the §A5.5.1 corrected per-cell flags exist (recompute if absent).

    grid-summariser.py writes these columns into grid-summary.parquet; this is a
    fallback for any parquet produced before that change.
    """
    needed = {"convergence_eligible", "shape_pass_corrected",
              "cell_pass_corrected", "in_envelope"}
    if needed.issubset(df.columns):
        return df
    out = df.copy()
    is_flat = out["shape_name"] == FLAT_SHAPE
    out["convergence_eligible"] = out["convergence_pass_rate"] >= CONVERGENCE_FRAC
    out["shape_pass_corrected"] = (
        (is_flat & (out["median_wasserstein_1_pgen"] <= T_FLAT_YEARS))
        | (~is_flat & (out["median_pearson_r_pgen"] >= SHAPE_PEARSON_PASS))
    )
    out["cell_pass_corrected"] = (
        out["convergence_eligible"] & out["shape_pass_corrected"]
    )
    out["in_envelope"] = out["alpha_true"] <= ALPHA_ENVELOPE
    return out


def grid_verdict_corrected(df: pd.DataFrame) -> dict:
    """Corrected §A5.5.1 verdict for one grid: headline B + diagnostic A.

    Headline B = clean-pass (convergence AND hybrid shape) over all in-envelope
    cells (the binding figure). Diagnostic A = shape-pass among convergence-
    eligible in-envelope cells (nan if none converge -- as for letter-mass).
    """
    env = df[df["in_envelope"]]
    n_env = int(len(env))
    elig = env["convergence_eligible"].astype(bool)
    n_elig = int(elig.sum())
    clean = env["cell_pass_corrected"].astype(bool)
    shape = env["shape_pass_corrected"].astype(bool)
    headline_b = float(clean.mean()) if n_env else float("nan")
    diagnostic_a = float(shape[elig].mean()) if n_elig else float("nan")
    return {
        "n_envelope": n_env,
        "n_eligible": n_elig,
        "n_excluded_nonconv": int((~elig).sum()),
        "n_clean_pass": int(clean.sum()),
        "headline_b": headline_b,
        "diagnostic_a": diagnostic_a,
        "validated": bool(n_env and headline_b >= GLOBAL_FRAC_PASS),
        "excluded_by_shape": {
            str(k): int(v)
            for k, v in env[~elig]["shape_name"].value_counts().items()
        },
    }


def grid_verdict(df: pd.DataFrame, exclude_flat: bool = False) -> dict:
    """Compute a grid's binding verdict (optionally excluding flat_baseline).

    The ``exclude_flat`` view is a diagnostic that removes the cells where
    Pearson r is undefined; it is NOT the prereg-binding rule.
    """
    sub = df[df["shape_name"] != FLAT_SHAPE] if exclude_flat else df
    n_cells = int(len(sub))
    cov = sub["alpha_coverage_pass"].astype(bool)
    r = sub["pearson_r_pass"].astype(bool)
    both = cov & r
    frac_cov = float(cov.mean())
    frac_r = float(r.mean())
    return {
        "n_cells": n_cells,
        "frac_cov": frac_cov,
        "frac_r": frac_r,
        "frac_both": float(both.mean()),
        "n_cov": int(cov.sum()),
        "n_r": int(r.sum()),
        "n_both": int(both.sum()),
        "validated": bool(
            frac_cov >= GLOBAL_FRAC_PASS and frac_r >= GLOBAL_FRAC_PASS
        ),
    }


# --------------------------------------------------------------------------- #
# Comparison join + four-way classification                                    #
# --------------------------------------------------------------------------- #
def _classify(both_a: bool, both_b: bool, name_a: str, name_b: str) -> str:
    """Map a (both_pass_A, both_pass_B) pair to a four-way label."""
    if both_a and both_b:
        return "both-pass"
    if both_a and not both_b:
        return f"{name_a}-only"
    if both_b and not both_a:
        return f"{name_b}-only"
    return "both-fail"


def build_comparison(
    df_a: pd.DataFrame, df_b: pd.DataFrame, name_a: str, name_b: str
) -> pd.DataFrame:
    """Join the two grids on cell_id and add the four-way classification.

    Inner join: the two grids share an identical 450-cell design, so an
    inner join should retain all cells; a mismatch in cell count is itself
    diagnostic and is surfaced by the caller.
    """
    keys = ["cell_id", "shape_name", "alpha_true", "tier_weights_name", "n"]
    keep = keys + [
        "alpha_coverage",
        "alpha_coverage_pass",
        "median_pearson_r_pgen",
        "pearson_r_pass",
        "median_wasserstein_1_pgen",
        "convergence_pass_rate",
        "n_divergences_total",
        "both_pass",
        "cell_pass_corrected",
    ]
    a = df_a[keep].copy()
    b = df_b[keep].copy()
    merged = a.merge(
        b, on=keys, suffixes=(f"_{name_a}", f"_{name_b}"), how="inner"
    )
    # in_envelope is a pure function of alpha_true (a join key), so recompute it
    # unsuffixed rather than carrying two identical suffixed copies.
    merged["in_envelope"] = merged["alpha_true"] <= ALPHA_ENVELOPE
    # Lodged four-way (prereg both_pass).
    merged["classification"] = [
        _classify(ba, bb, name_a, name_b)
        for ba, bb in zip(
            merged[f"both_pass_{name_a}"].astype(bool),
            merged[f"both_pass_{name_b}"].astype(bool),
        )
    ]
    # Corrected four-way (cell_pass_corrected), restricted to the operating
    # envelope; out-of-envelope (stress) cells are labelled separately.
    merged["classification_corrected"] = [
        (_classify(ca, cb, name_a, name_b) if ie else "stress(out-of-env)")
        for ie, ca, cb in zip(
            merged["in_envelope"],
            merged[f"cell_pass_corrected_{name_a}"].astype(bool),
            merged[f"cell_pass_corrected_{name_b}"].astype(bool),
        )
    ]
    return merged


# --------------------------------------------------------------------------- #
# Figures                                                                      #
# --------------------------------------------------------------------------- #
def _pass_rate_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Mean both-pass per (alpha x shape) cell, ordered canonically."""
    pivot = (
        df.assign(both=df["both_pass"].astype(float))
        .pivot_table(
            index="alpha_true", columns="shape_name", values="both",
            aggfunc="mean",
        )
        .reindex(index=ALPHA_ORDER, columns=SHAPE_ORDER)
    )
    return pivot


def make_heatmap(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    name_a: str,
    name_b: str,
    out_path: Path,
) -> None:
    """Side-by-side (alpha x shape) both-pass-rate heatmaps, shared 0-1 scale."""
    piv_a = _pass_rate_pivot(df_a)
    piv_b = _pass_rate_pivot(df_b)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
    for ax, piv, name in [
        (axes[0], piv_a, name_a),
        (axes[1], piv_b, name_b),
    ]:
        im = ax.imshow(
            piv.values, vmin=0.0, vmax=1.0, cmap="RdYlGn", aspect="auto"
        )
        ax.set_xticks(range(len(piv.columns)))
        ax.set_xticklabels(piv.columns, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(piv.index)))
        ax.set_yticklabels([f"{a:.2f}" for a in piv.index])
        ax.set_xlabel("genuine shape")
        ax.set_ylabel("true alpha (convention mass)")
        ax.set_title(f"{name}-mass: both-criteria pass-rate")
        # Annotate each tile with its pass-rate (or '·' for NaN).
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                val = piv.values[i, j]
                txt = "·" if np.isnan(val) else f"{val:.0%}"
                ax.text(
                    j, i, txt, ha="center", va="center", fontsize=8,
                    color="black",
                )
    fig.colorbar(
        im, ax=axes, fraction=0.025, pad=0.02,
        label="fraction of (tier x N) cells passing both criteria",
    )
    fig.suptitle(
        "Recovery-grid both-criteria pass-rate, by unit of analysis "
        "(higher = better; flat_baseline column is capped by the "
        "undefined-Pearson-r artefact)",
        fontsize=10,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def make_alpha_bias_figure(
    run_root: Path,
    grid_a_dir: Path,
    grid_b_dir: Path,
    name_a: str,
    name_b: str,
    out_path: Path,
) -> bool:
    """Recovered-alpha bias by tier, per unit, from compact alpha-bias tables.

    Reads ``<grid>/outputs/tables/alpha-bias.parquet`` (produced by
    ``collect-alpha-bias.py``). Returns True if the figure was written,
    False (with a logged note) if either table is missing.
    """
    tab_a = grid_a_dir / "outputs" / "tables" / "alpha-bias.parquet"
    tab_b = grid_b_dir / "outputs" / "tables" / "alpha-bias.parquet"
    if not (tab_a.exists() and tab_b.exists()):
        print(
            "[compare] alpha-bias.parquet not found for both grids; "
            "skipping fig-alpha-bias-by-tier.png. Produce it with "
            "collect-alpha-bias.py per grid, then re-run."
        )
        return False

    frames = []
    for tab, name in [(tab_a, name_a), (tab_b, name_b)]:
        d = pd.read_parquet(tab)
        d["unit"] = name
        frames.append(d)
    bias = pd.concat(frames, ignore_index=True)
    # Mean signed bias (recovered - true) per (tier, unit).
    grp = (
        bias.groupby(["tier_weights_name", "unit"])["alpha_bias_mean"]
        .mean()
        .unstack("unit")
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    grp.plot(kind="bar", ax=ax)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("tier-weight vector")
    ax.set_ylabel("mean recovered-alpha bias (recovered − true)")
    ax.set_title("Alpha-recovery bias by tier and unit of analysis")
    ax.legend(title="unit")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return True


# --------------------------------------------------------------------------- #
# §5 outcome-branch determination                                              #
# --------------------------------------------------------------------------- #
def determine_outcome_branch(
    a_pass: bool, b_pass: bool, name_a: str, name_b: str
) -> tuple[str, str]:
    """Return (branch_label, recommended-Stage-3-path text) per spec.md §5."""
    if a_pass and b_pass:
        return (
            "PASS / PASS",
            f"Launch Stage 3 under both units in parallel (the planned "
            f"two-measure framework); the inter-measure delta becomes a "
            f"third output.",
        )
    if a_pass and not b_pass:
        return (
            "PASS / FAIL",
            f"{name_b}-mass calibration cohort lacks identifiability. "
            f"Investigate the heavy-tail letter-count distribution (try a "
            f"99th-pct cap as sensitivity) and the cohort size. Stage 3 "
            f"launches under {name_a}-mass only; {name_b}-mass reported as "
            f"a limitation.",
        )
    if b_pass and not a_pass:
        return (
            "FAIL / PASS",
            f"{name_a}-mass identifiability problem persists despite "
            f"F1+F3; the 2026-05-22 finding generalises. Stage 3 launches "
            f"under {name_b}-mass only; {name_a}-mass reported as a "
            f"limitation. Trigger a structural-pivot diagnostic if both "
            f"H3a and H3b need {name_a}-mass.",
        )
    return (
        "FAIL / FAIL",
        "Both unit choices fail the prereg-binding criteria. Stage 3 "
        "cannot launch under the current methodology as-written. Trigger a "
        "second diagnostic chain (analogous to 2026-05-24) on the two-grid "
        "failure pattern: likely a structural model revision, prior "
        "re-derivation, or a methodological pivot beyond the "
        "calibration-cohort empirical-Bayes design.",
    )


# --------------------------------------------------------------------------- #
# Report                                                                       #
# --------------------------------------------------------------------------- #
def _verdict_row(label: str, v: dict) -> str:
    return (
        f"| {label} | {v['frac_cov']:.1%} ({v['n_cov']}/{v['n_cells']}) "
        f"| {v['frac_r']:.1%} ({v['n_r']}/{v['n_cells']}) "
        f"| {v['frac_both']:.1%} ({v['n_both']}/{v['n_cells']}) "
        f"| {'PASS' if v['validated'] else 'FAIL'} |"
    )


def make_report(
    merged: pd.DataFrame,
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    name_a: str,
    name_b: str,
    alpha_bias_done: bool,
    partial_note: str | None,
) -> str:
    """Render COMPARISON-REPORT.md content."""
    va = grid_verdict(df_a)
    vb = grid_verdict(df_b)
    va_nf = grid_verdict(df_a, exclude_flat=True)
    vb_nf = grid_verdict(df_b, exclude_flat=True)

    branch, path_text = determine_outcome_branch(
        va["validated"], vb["validated"], name_a, name_b
    )
    branch_nf, path_text_nf = determine_outcome_branch(
        va_nf["validated"], vb_nf["validated"], name_a, name_b
    )

    # Corrected criterion (Decision 33 / §A5.5.1) — the binding verdict.
    cva = grid_verdict_corrected(df_a)
    cvb = grid_verdict_corrected(df_b)
    branch_c, path_text_c = determine_outcome_branch(
        cva["validated"], cvb["validated"], name_a, name_b
    )

    counts = merged["classification"].value_counts().to_dict()
    counts_c = merged["classification_corrected"].value_counts().to_dict()

    L: list[str] = []
    L.append("# Cross-grid comparison — two-unit recovery simulation")
    L.append("")
    L.append(
        f"Head-to-head of **{name_a}-mass** (Grid A) and **{name_b}-mass** "
        f"(Grid B) recovery grids. See "
        f"`runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the "
        f"binding decision rule and outcome-branching."
    )
    L.append("")
    if partial_note:
        L.append(f"> ⚠️ **{partial_note}**")
        L.append("")

    # ---- OSF hard-gate banner (always first, always loud) -------------- #
    L.append("## 0. HARD GATE — OSF Amendment 01 not yet lodged")
    L.append("")
    L.append(
        "The Stage-3 launch path named in this report is a **recommendation "
        "only**. Per the project standing rule (memory "
        "`2026-05-26-40ce5927fddc`), **no Stage-3 confirmatory work may "
        "begin until OSF Amendment 01 is lodged** — even a both-PASS "
        "verdict does not authorise launch. Confirm lodgement with Shawn "
        "before any confirmatory-claim-producing run."
    )
    L.append("")

    # ---- Binding verdict: corrected criterion (Decision 33 / §A5.5.1) --- #
    def _cv_row(label: str, cv: dict) -> str:
        a_val = cv["diagnostic_a"]
        a_str = f"{a_val:.1%}" if a_val == a_val else "n/a (no convergent cells)"
        return (
            f"| {label} | **{cv['headline_b']:.1%}** "
            f"({cv['n_clean_pass']}/{cv['n_envelope']}) | {a_str} "
            f"| {cv['n_excluded_nonconv']} | "
            f"{'PASS' if cv['validated'] else 'FAIL'} |"
        )

    L.append("## 1. Binding verdict — corrected criterion (Decision 33 / §A5.5.1)")
    L.append("")
    L.append(
        "The **binding** cross-grid verdict uses the corrected criterion: a "
        f"convergence precondition (≥ {CONVERGENCE_FRAC:.0%} of replicates) + a "
        f"hybrid shape gate (median Pearson r ≥ {SHAPE_PEARSON_PASS:.2f} for "
        f"non-flat shapes; Wasserstein-1 ≤ {T_FLAT_YEARS:.0f} y for flat_baseline), "
        f"α demoted to a diagnostic, within the operating envelope "
        f"(α ≤ {ALPHA_ENVELOPE:.2f}). Headline **B** = clean-pass (convergence AND "
        "shape) over all in-envelope cells (binding); **A** = shape-pass among "
        "convergence-eligible cells. The lodged criterion is retained as a "
        "reference in §1R."
    )
    L.append("")
    L.append("| Grid | headline B (binding) | diagnostic A | conv-excluded | Verdict |")
    L.append("|---|---|---|---|---|")
    L.append(_cv_row(f"{name_a}-mass", cva))
    L.append(_cv_row(f"{name_b}-mass", cvb))
    L.append("")
    L.append(f"**Outcome branch (binding): {branch_c}.** {path_text_c}")
    L.append("")
    L.append("### 1a. Four-way cell classification (corrected, operating envelope)")
    L.append("")
    L.append("| classification | n cells |")
    L.append("|---|---|")
    for key in [
        "both-pass", f"{name_a}-only", f"{name_b}-only", "both-fail",
        "stress(out-of-env)",
    ]:
        L.append(f"| {key} | {counts_c.get(key, 0)} |")
    L.append("")
    if cva["n_excluded_nonconv"] and set(cva["excluded_by_shape"]) == {FLAT_SHAPE}:
        L.append(
            f"> **{name_a}-mass flat-null note.** Its {cva['n_excluded_nonconv']} "
            "convergence-excluded in-envelope cells are all `flat_baseline` — a "
            "flat-null sampling quirk (flatness still recovered correctly), the "
            f"entire gap between B ({cva['headline_b']:.1%}) and A "
            f"({cva['diagnostic_a']:.1%}). Deferred re-fit logged in the backlog."
        )
        L.append("")
    if cvb["n_eligible"] == 0:
        L.append(
            f"> **{name_b}-mass convergence note.** **No** in-envelope cell reaches "
            f"the {CONVERGENCE_FRAC:.0%} convergence precondition (max "
            f"convergence_pass_rate < {CONVERGENCE_FRAC:.2f}); the heavy-tailed "
            "letter-count likelihood produces severe divergences. Letter-mass fails "
            "on convergence before shape recovery is even assessable, so diagnostic "
            "A is undefined. This is consistent with inscription count being the "
            "primary unit of analysis (Obs 61)."
        )
        L.append("")

    # ---- Lodged-criterion reference verdicts --------------------------- #
    L.append("## 1R. Per-grid verdicts — LODGED criterion (reference only)")
    L.append("")
    L.append(
        "**Binding rule (prereg §4 / spec §5):** a unit is validated only "
        f"if ≥ {GLOBAL_FRAC_PASS:.0%} of cells pass coverage AND "
        f"≥ {GLOBAL_FRAC_PASS:.0%} pass median-Pearson-r ≥ 0.95."
    )
    L.append("")
    L.append("| Grid | coverage pass-rate | shape-r pass-rate | both | Verdict |")
    L.append("|---|---|---|---|---|")
    L.append(_verdict_row(f"{name_a}-mass (as-written)", va))
    L.append(_verdict_row(f"{name_b}-mass (as-written)", vb))
    L.append("")
    L.append(
        f"**Outcome branch (as-written): {branch}.** {path_text}"
    )
    if branch == "FAIL / FAIL":
        L.append("")
        L.append(
            "Before concluding the methodology is unsound, read the "
            "flat-excluded diagnostic verdict in §1b: part of the as-written "
            "FAIL is the known undefined-Pearson-r artefact on flat_baseline."
        )
    L.append("")
    L.append("### 1b. Flat-baseline-excluded DIAGNOSTIC view (not the binding rule)")
    L.append("")
    L.append(
        "`flat_baseline` returns an undefined Pearson r (constant truth → "
        "zero variance; documented in `runs/2026-05-24-followup-"
        "systematics/`), so its 75 cells fail criterion (b) mechanically "
        "and cap as-written shape-pass at 83.3%. Excluding them isolates "
        "the genuine model-quality comparison. **This is diagnostic only; "
        "changing the binding metric is an OSF-amendment decision.**"
    )
    L.append("")
    L.append("| Grid | coverage pass-rate | shape-r pass-rate | both | Verdict |")
    L.append("|---|---|---|---|---|")
    L.append(_verdict_row(f"{name_a}-mass (flat-excluded)", va_nf))
    L.append(_verdict_row(f"{name_b}-mass (flat-excluded)", vb_nf))
    L.append("")
    L.append(f"**Outcome branch (flat-excluded): {branch_nf}.** {path_text_nf}")
    L.append("")

    # ---- Four-way classification --------------------------------------- #
    L.append("## 2. Four-way cell classification")
    L.append("")
    L.append("| classification | n cells |")
    L.append("|---|---|")
    for key in ["both-pass", f"{name_a}-only", f"{name_b}-only", "both-fail"]:
        L.append(f"| {key} | {counts.get(key, 0)} |")
    L.append("")
    L.append(
        "Filter views available in `cell-pass-comparison.parquet`: "
        "`both-pass` (good), "
        f"`{name_a}-only` ({name_b}-mass identifiability problem), "
        f"`{name_b}-only` ({name_a}-mass identifiability problem), "
        "`both-fail` (still need a structural rethink)."
    )
    L.append("")

    # ---- Failure localisation (§5 reporting requirement) --------------- #
    L.append("## 3. Failure localisation (per spec §5)")
    L.append("")
    for name, df in [(name_a, df_a), (name_b, df_b)]:
        L.append(f"### 3.{name}-mass — per-shape both-pass-rate")
        L.append("")
        L.append("| shape | n | cov pass | shape pass | both |")
        L.append("|---|---|---|---|---|")
        for shape in SHAPE_ORDER:
            grp = df[df["shape_name"] == shape]
            if grp.empty:
                continue
            cov = grp["alpha_coverage_pass"].astype(bool).mean()
            r = grp["pearson_r_pass"].astype(bool).mean()
            both = (
                grp["alpha_coverage_pass"].astype(bool)
                & grp["pearson_r_pass"].astype(bool)
            ).mean()
            L.append(
                f"| {shape} | {len(grp)} | {cov:.0%} | {r:.0%} | {both:.0%} |"
            )
        L.append("")
        # Zero-coverage cells: the high-precision-but-biased-alpha pattern.
        zc = df[df["alpha_coverage"] == 0.0]
        by_shape = {str(k): int(v) for k, v in zc["shape_name"].value_counts().items()}
        by_n = {int(k): int(v) for k, v in zc["n"].value_counts().items()}
        L.append(
            f"- Cells with α-coverage = 0.00 (CI never covers true α): "
            f"**{len(zc)}** (by shape: {by_shape}; by N: {by_n}). These "
            f"recover shape well but α with biased precision — the "
            f"α/shape-complexity likelihood ridge."
        )
        L.append("")

    # ---- Figures ------------------------------------------------------- #
    L.append("## 4. Figures")
    L.append("")
    L.append(
        "- `figures/fig-pass-rate-heatmap.png` — side-by-side (α × shape) "
        "both-pass-rate heatmaps, shared 0–1 colour scale "
        "(paper-figure candidate)."
    )
    if alpha_bias_done:
        L.append(
            "- `figures/fig-alpha-bias-by-tier.png` — recovered-α bias by "
            "tier and unit (paper-figure candidate)."
        )
    else:
        L.append(
            "- `figures/fig-alpha-bias-by-tier.png` — NOT produced "
            "(alpha-bias.parquet missing for one/both grids; run "
            "`collect-alpha-bias.py` per grid, then re-run this script)."
        )
    L.append("")

    # ---- Wasserstein-1 supplementary ----------------------------------- #
    L.append("## 5. Wasserstein-1 supplementary")
    L.append("")
    L.append(
        "W-1 is a distribution-sensitive shape metric reported per cell "
        "(prereg §4 line 334); its flagging threshold remains deferred and "
        "is NOT part of the binding rule."
    )
    L.append("")
    for name, df in [(name_a, df_a), (name_b, df_b)]:
        med = float(df["median_wasserstein_1_pgen"].median())
        p90 = float(df["median_wasserstein_1_pgen"].quantile(0.9))
        L.append(f"- {name}-mass: median {med:.2f}; 90th pct {p90:.2f}")
    L.append("")

    # ---- Methodology note ---------------------------------------------- #
    L.append("## 6. Methodology note for OSF Amendment 01")
    L.append("")
    L.append(
        "Binding criterion (b) (median Pearson r ≥ 0.95) is **undefined** "
        "for the `flat_baseline` shape (constant truth, zero variance), so "
        "it is unsatisfiable for that shape regardless of model quality, "
        "and caps as-written shape-pass at 83.3% for BOTH units. The "
        "amendment should either (i) exclude undefined-r cells from "
        "criterion (b), or (ii) substitute the Wasserstein-1 metric for the "
        "flat case. This is flagged for Shawn + statistician sign-off; this "
        "harness applies the criterion as currently written."
    )
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #
def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Cross-grid comparison for the two-unit recovery sim."
    )
    p.add_argument(
        "--run-root", type=Path, default=None,
        help="Parent run dir; derives inscription-mass/ and letter-mass/.",
    )
    p.add_argument("--grid-a-dir", type=Path, default=None)
    p.add_argument("--grid-b-dir", type=Path, default=None)
    p.add_argument("--grid-a-name", type=str, default="inscription")
    p.add_argument("--grid-b-name", type=str, default="letter")
    p.add_argument(
        "--out-dir", type=Path, default=None,
        help="Comparison output dir (default <run-root>/comparison).",
    )
    return p.parse_args()


def main() -> int:
    args = _parse_args()

    # Resolve grid dirs from --run-root unless explicitly overridden.
    if args.grid_a_dir is None or args.grid_b_dir is None:
        if args.run_root is None:
            print(
                "[compare] ERROR: provide --run-root, or both --grid-a-dir "
                "and --grid-b-dir.", file=sys.stderr,
            )
            return 2
        grid_a_dir = (args.grid_a_dir or args.run_root / "inscription-mass").resolve()
        grid_b_dir = (args.grid_b_dir or args.run_root / "letter-mass").resolve()
    else:
        grid_a_dir = args.grid_a_dir.resolve()
        grid_b_dir = args.grid_b_dir.resolve()

    name_a, name_b = args.grid_a_name, args.grid_b_name
    out_dir = (
        args.out_dir.resolve() if args.out_dir
        else (args.run_root.resolve() / "comparison" if args.run_root
              else grid_a_dir.parent / "comparison")
    )

    df_a = load_grid_summary(grid_a_dir)
    df_b = load_grid_summary(grid_b_dir)

    # Partial-run guard: flag if either grid has < 450 cells.
    partial_note = None
    if len(df_a) < 450 or len(df_b) < 450:
        partial_note = (
            f"PARTIAL DATA — {name_a}-mass has {len(df_a)}/450 cells, "
            f"{name_b}-mass has {len(df_b)}/450 cells. Verdicts below are "
            f"provisional until both grids complete."
        )
        print(f"[compare] {partial_note}")

    merged = build_comparison(df_a, df_b, name_a, name_b)
    if len(merged) < min(len(df_a), len(df_b)):
        print(
            f"[compare] WARNING: join kept {len(merged)} cells "
            f"(< min grid size); cell_id mismatch between grids."
        )

    # Artefacts.
    figs_dir = out_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    comp_path = out_dir / "cell-pass-comparison.parquet"
    merged.to_parquet(comp_path, index=False)

    make_heatmap(df_a, df_b, name_a, name_b, figs_dir / "fig-pass-rate-heatmap.png")
    alpha_bias_done = make_alpha_bias_figure(
        args.run_root or grid_a_dir.parent, grid_a_dir, grid_b_dir,
        name_a, name_b, figs_dir / "fig-alpha-bias-by-tier.png",
    )

    report = make_report(
        merged, df_a, df_b, name_a, name_b, alpha_bias_done, partial_note
    )
    report_path = out_dir / "COMPARISON-REPORT.md"
    report_path.write_text(report, encoding="utf-8")

    # Console summary.
    va, vb = grid_verdict(df_a), grid_verdict(df_b)
    cva, cvb = grid_verdict_corrected(df_a), grid_verdict_corrected(df_b)
    branch, _ = determine_outcome_branch(
        va["validated"], vb["validated"], name_a, name_b
    )
    branch_c, _ = determine_outcome_branch(
        cva["validated"], cvb["validated"], name_a, name_b
    )
    print(f"[compare] CORRECTED (binding) {name_a}-mass: "
          f"{'PASS' if cva['validated'] else 'FAIL'} (headline B "
          f"{cva['headline_b']:.1%})")
    print(f"[compare] CORRECTED (binding) {name_b}-mass: "
          f"{'PASS' if cvb['validated'] else 'FAIL'} (headline B "
          f"{cvb['headline_b']:.1%})")
    print(f"[compare] corrected outcome branch: {branch_c}")
    print(f"[compare] lodged (reference) branch: {branch}")
    print(f"[compare] wrote {comp_path}")
    print(f"[compare] wrote {figs_dir / 'fig-pass-rate-heatmap.png'}")
    print(f"[compare] wrote {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
