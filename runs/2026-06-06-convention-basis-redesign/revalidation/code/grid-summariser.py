#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grid-summariser.py
==================

Per-grid summariser for the 2026-05-26 two-unit recovery-grid
re-simulation. Reads every per-cell summary JSON for ONE grid
(``inscription-mass`` or ``letter-mass``) and emits that grid's
binding-criterion verdict.

This generalises the single-grid ``runs/2026-05-22-recovery-grid-
validation/code/05-grid-summariser.py`` to the two-unit directory layout
(spec.md §4) and additionally persists a machine-readable
``grid-summary.parquet`` table (the cross-grid comparison harness,
``compare-grids.py``, consumes it). The cell-summary JSON schema is
identical between the two runs, so the binding logic is unchanged.

Binding criteria (prereg §4 lines 333-334; spec.md §5):

- ``frac_cells_pass_alpha_coverage``: fraction of cells where
  ``alpha_coverage >= 0.90``. Validation requires this fraction >= 0.90.
- ``frac_cells_pass_shape_recovery``: fraction of cells where the
  posterior-median Pearson r (``median_pearson_r_pgen``) >= 0.95.
  Validation requires this fraction >= 0.90.

The grid is VALIDATED under the LODGED criterion only if BOTH fractions are
>= 0.90. As of 2026-06-03 the lodged criterion is retained as a *reference*; the
BINDING verdict is the corrected criterion (Decision 33 / OSF Amendment 01
§A5.5.1), computed alongside it: a convergence precondition + a hybrid shape gate
(Pearson r >= 0.95 non-flat; Wasserstein-1 <= 10 y for flat_baseline, where
Pearson r is undefined), alpha demoted to a diagnostic, evaluated within the
operating envelope (alpha <= 0.70). It is reported as headline B (clean-pass over
all in-envelope cells) plus diagnostic A (shape-pass among convergence-eligible).
Both verdicts appear in REPORT.md and grid-summary.parquet. No re-fit (W1 +
convergence are stored).

Outputs (written under ``<grid-dir>/outputs/``):

- ``tables/grid-summary.parquet`` -- one row per cell; all summary
  fields plus a derived ``both_pass`` flag.
- ``REPORT.md`` -- headline verdict, per-axis pass rates, failed-cell
  table, diagnostics, and the Wasserstein-1 supplementary.

Usage
-----
    python grid-summariser.py \\
        --grid-dir /path/to/runs/2026-05-26-recovery-grid-two-unit/inscription-mass

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------- #
# Binding thresholds (prereg-binding; identical to the 2026-05-22 run).        #
# --------------------------------------------------------------------------- #
ALPHA_COVERAGE_PASS = 0.90  # per-cell coverage floor
SHAPE_PEARSON_PASS = 0.95   # per-cell median-Pearson-r floor
GLOBAL_FRAC_PASS = 0.90     # fraction-of-cells floor for both criteria

# --------------------------------------------------------------------------- #
# Corrected binding criterion (Decision 33 / OSF Amendment 01 §A5.5.1).         #
# Computed ALONGSIDE the lodged criterion above; NO re-fit — Wasserstein-1 and  #
# convergence are already stored per cell.                                      #
# --------------------------------------------------------------------------- #
FLAT_SHAPE = "flat_baseline"  # the only shape with undefined Pearson r
T_FLAT_YEARS = 10.0           # W1 gate for the flat shape (max well-recovered W1 9.8 y, rounded up)
ALPHA_ENVELOPE = 0.70         # operating-envelope ceiling (criterion evaluated here)
ALPHA_STRESS = 0.95           # near-unidentifiable stress row (reported, never gated)
CONVERGENCE_FRAC = 0.90       # explicit convergence precondition (>=90% replicates converge)

# Grid A reference figures for the built-in regression check (Decision 33 /
# §A5.5.1). Headline B = clean-pass (convergence AND shape) over all in-envelope
# cells; diagnostic A = shape-pass among convergence-eligible in-envelope cells.
#
# Under the field-standard convergence gate (R-hat / bulk-ESS only; cell_lib.
# convergence_pass, refined 2026-06-04) the A/B gap CLOSES: the 24 flat_baseline
# cells that the earlier zero-tolerance divergence gate had excluded all pass
# R-hat / bulk-ESS, so headline B = diagnostic A = 98.6% (355/360 in-envelope
# cells; the 5 non-passers are bimodal_alpha=0.70_N=2000 cells failing on genuine
# shape, not convergence). The pre-2026-06-04 figures were B = 91.9% / A = 98.5%.
# Re-derived in-pipeline by reaggregate.py (no re-fit).
#
# DESIGN-SPECIFIC GUARD. These figures belong to the *2026-05-22 / 2026-05-26
# validated design*. They are a regression guard for a re-run of THAT design, not
# a target for a different convention basis. The 2026-06-06 Decision-38
# re-validation deliberately rebuilds the tier basis, so its headline is a fresh
# MEASUREMENT, not a Grid-A regression target ("Grid A 98.6% does not transfer").
# Hence the hard-assert below is OPT-IN via --assert-grid-a-regression; by default
# the Grid-A delta is surfaced as informational context and never aborts scoring.
GRID_A_HEADLINE_B = 0.986
GRID_A_DIAGNOSTIC_A = 0.986
REGRESSION_TOL = 0.003


def load_all_summaries(grid_dir: Path) -> pd.DataFrame:
    """Load every per-cell summary JSON for one grid into a DataFrame.

    Parameters
    ----------
    grid_dir : Path
        A grid root such as ``.../recovery-grid-two-unit/inscription-mass``.
        Cell summaries are expected at ``<grid_dir>/outputs/cell-summaries/
        *-summary.json``.

    Returns
    -------
    pandas.DataFrame
        One row per cell, columns matching the cell-summary JSON schema.

    Raises
    ------
    FileNotFoundError
        If the cell-summaries directory is absent or contains no summaries.
    """
    summaries_dir = grid_dir / "outputs" / "cell-summaries"
    if not summaries_dir.exists():
        raise FileNotFoundError(
            f"No cell-summaries directory at {summaries_dir}"
        )
    records = []
    for path in sorted(summaries_dir.glob("*-summary.json")):
        with path.open("r", encoding="utf-8") as handle:
            records.append(json.load(handle))
    if not records:
        raise FileNotFoundError(
            f"No per-cell summaries found under {summaries_dir}"
        )
    return pd.DataFrame(records)


def compute_verdict(df: pd.DataFrame) -> dict[str, object]:
    """Compute the grid-level binding verdict from per-cell flags.

    Returns a dict carrying the three fractions, the per-criterion
    pass booleans, the combined ``validated`` verdict, and the cell count.
    """
    n_cells = int(len(df))
    cov_pass = df["alpha_coverage_pass"].astype(bool)
    r_pass = df["pearson_r_pass"].astype(bool)
    both_pass = cov_pass & r_pass

    frac_cov = float(cov_pass.mean())
    frac_r = float(r_pass.mean())
    frac_both = float(both_pass.mean())

    return {
        "n_cells": n_cells,
        "frac_cov": frac_cov,
        "frac_r": frac_r,
        "frac_both": frac_both,
        "cov_criterion_pass": bool(frac_cov >= GLOBAL_FRAC_PASS),
        "r_criterion_pass": bool(frac_r >= GLOBAL_FRAC_PASS),
        "validated": bool(
            frac_cov >= GLOBAL_FRAC_PASS and frac_r >= GLOBAL_FRAC_PASS
        ),
    }


def add_corrected_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add the §A5.5.1 corrected-criterion per-cell flags (no re-fit).

    Adds five columns derived purely from stored fields:

    - ``is_flat`` -- the ``flat_baseline`` shape (Pearson r undefined there).
    - ``convergence_eligible`` -- ``convergence_pass_rate >= CONVERGENCE_FRAC``
      (the explicit convergence precondition).
    - ``shape_pass_corrected`` -- hybrid shape gate: median Pearson r >= 0.95
      for non-flat shapes; median Wasserstein-1 <= ``T_FLAT_YEARS`` for the flat
      shape (where Pearson r is undefined).
    - ``cell_pass_corrected`` -- ``convergence_eligible AND shape_pass_corrected``.
    - ``in_envelope`` -- ``alpha_true <= ALPHA_ENVELOPE`` (operating envelope).
    """
    out = df.copy()
    is_flat = out["shape_name"] == FLAT_SHAPE
    out["is_flat"] = is_flat
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


def compute_corrected_verdict(df: pd.DataFrame) -> dict[str, object]:
    """Compute the §A5.5.1 corrected verdict (headline B; diagnostic A).

    Requires the columns added by :func:`add_corrected_flags`. The binding
    criterion is evaluated within the operating envelope (``alpha_true <=
    ALPHA_ENVELOPE``):

    - **Headline B** -- clean-pass (convergence AND hybrid shape) over ALL
      in-envelope cells; the binding figure: ``B >= GLOBAL_FRAC_PASS`` validates.
    - **Diagnostic A** -- hybrid shape-pass among convergence-eligible
      in-envelope cells (recovery quality where the fit is trustworthy).

    The A/B gap is exactly the convergence-excluded in-envelope cells. Under the
    field-standard gate (cell_lib.convergence_pass; R-hat / bulk-ESS only) Grid A
    has NO such cells -- A and B coincide at 98.6% -- because the 24
    ``flat_baseline`` cells the earlier zero-tolerance divergence gate excluded
    all pass R-hat / bulk-ESS (Decision 33 / §A5.5.1; the benign-divergence
    refinement of 2026-06-04). Any residual gap under this gate would be genuine
    R-hat / bulk-ESS non-convergence, reported by shape below.
    """
    env = df[df["in_envelope"]]
    n_env = int(len(env))
    elig = env["convergence_eligible"].astype(bool)
    n_elig = int(elig.sum())
    clean = env["cell_pass_corrected"].astype(bool)
    shape = env["shape_pass_corrected"].astype(bool)

    headline_b = float(clean.mean()) if n_env else float("nan")
    diagnostic_a = float(shape[elig].mean()) if n_elig else float("nan")
    stress = df[df["alpha_true"] >= ALPHA_STRESS]

    return {
        "n_envelope": n_env,
        "n_eligible": n_elig,
        "n_excluded_nonconv": int((~elig).sum()),
        "n_clean_pass": int(clean.sum()),
        "n_shape_pass_eligible": int(shape[elig].sum()),
        "headline_b": headline_b,
        "diagnostic_a": diagnostic_a,
        "validated": bool(headline_b >= GLOBAL_FRAC_PASS),
        "excluded_by_shape": {
            str(k): int(v)
            for k, v in env[~elig]["shape_name"].value_counts().items()
        },
        "n_stress": int(len(stress)),
        "stress_shape_pass": (
            float(stress["shape_pass_corrected"].astype(bool).mean())
            if len(stress) else float("nan")
        ),
    }


def write_grid_summary_parquet(df: pd.DataFrame, grid_dir: Path) -> Path:
    """Persist the per-cell table (plus a ``both_pass`` flag) to parquet.

    This is the machine-readable artefact the cross-grid comparison harness
    joins on ``cell_id``. Returns the written path.
    """
    out = df.copy()
    out["both_pass"] = (
        out["alpha_coverage_pass"].astype(bool)
        & out["pearson_r_pass"].astype(bool)
    )
    tables_dir = grid_dir / "outputs" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    out_path = tables_dir / "grid-summary.parquet"
    out.to_parquet(out_path, index=False)
    return out_path


def make_report(df: pd.DataFrame) -> str:
    """Render the per-grid REPORT.md content as a single Markdown string."""
    verdict = compute_verdict(df)
    n_cells = verdict["n_cells"]
    cov_pass = df["alpha_coverage_pass"].astype(bool)
    r_pass = df["pearson_r_pass"].astype(bool)
    both_pass = cov_pass & r_pass

    # The unit label is constant within a grid; read it from the first row.
    unit = str(df["unit"].iloc[0]) if "unit" in df.columns else "unknown"

    lines: list[str] = []
    lines.append(f"# Recovery Grid — {unit}-mass — Per-Grid Report")
    lines.append("")
    lines.append(
        "Bayesian deconvolution-mixture model validation via the two-unit "
        "recovery simulation."
    )
    lines.append(
        "See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the "
        "binding decision rule, and the 2026-05-22 predecessor run for the "
        "shared cell design."
    )
    lines.append("")
    lines.append("## 1. Headline result")
    lines.append("")
    lines.append(
        f"**Unit of analysis:** {unit}-mass "
        f"(each synthetic inscription deposits "
        f"{'unit count' if unit == 'inscription' else 'letter mass'})."
    )
    lines.append("")
    lines.append(
        f"**Validation verdict:** "
        f"{'PASS' if verdict['validated'] else 'FAIL'} "
        f"(binding criteria require >= {GLOBAL_FRAC_PASS:.0%} of cells to "
        f"pass coverage AND shape recovery)"
    )
    lines.append("")
    lines.append("| Criterion | Threshold | Result | Pass? |")
    lines.append("|---|---|---|---|")
    lines.append(
        f"| alpha-coverage >= {ALPHA_COVERAGE_PASS:.0%} per cell "
        f"| >= {GLOBAL_FRAC_PASS:.0%} of cells "
        f"| {verdict['frac_cov']:.1%} ({int(cov_pass.sum())}/{n_cells}) "
        f"| {'PASS' if verdict['cov_criterion_pass'] else 'FAIL'} |"
    )
    lines.append(
        f"| median Pearson r >= {SHAPE_PEARSON_PASS:.2f} per cell "
        f"| >= {GLOBAL_FRAC_PASS:.0%} of cells "
        f"| {verdict['frac_r']:.1%} ({int(r_pass.sum())}/{n_cells}) "
        f"| {'PASS' if verdict['r_criterion_pass'] else 'FAIL'} |"
    )
    lines.append(
        f"| Both criteria simultaneously | (informational) "
        f"| {verdict['frac_both']:.1%} ({int(both_pass.sum())}/{n_cells}) "
        f"| — |"
    )
    lines.append("")
    lines.append(
        "> The verdict above is the **lodged** criterion, retained as a "
        "reference. The **binding** verdict is the corrected criterion in §1b."
    )
    lines.append("")

    # ----- Corrected binding criterion (Decision 33 / §A5.5.1) ----------- #
    cv = compute_corrected_verdict(df)
    lines.append("## 1b. Corrected binding criterion (Decision 33 / §A5.5.1) — BINDING")
    lines.append("")
    lines.append(
        "Convergence precondition "
        f"(≥ {CONVERGENCE_FRAC:.0%} of replicates converge) + hybrid shape gate "
        f"(median Pearson r ≥ {SHAPE_PEARSON_PASS:.2f} for non-flat shapes; "
        f"Wasserstein-1 ≤ {T_FLAT_YEARS:.0f} y for `flat_baseline`, where Pearson r "
        f"is undefined), α demoted to a diagnostic, evaluated within the operating "
        f"envelope (α ≤ {ALPHA_ENVELOPE:.2f}). Cells with α ≥ {ALPHA_STRESS:.2f} are a "
        "reported stress sensitivity, not gated. W1 + convergence are stored, so "
        "this is computed without re-fitting."
    )
    lines.append("")
    lines.append(
        f"**Verdict: {'PASS' if cv['validated'] else 'FAIL'}** — headline "
        f"**{cv['headline_b']:.1%}** of in-envelope cells are clean passes "
        f"(convergence AND shape), against a ≥ {GLOBAL_FRAC_PASS:.0%} bar."
    )
    lines.append("")
    lines.append("| Figure | Definition | Value |")
    lines.append("|---|---|---|")
    lines.append(
        f"| **Headline (B)** | clean-pass (convergence AND shape) ÷ all "
        f"in-envelope | **{cv['headline_b']:.1%}** "
        f"({cv['n_clean_pass']}/{cv['n_envelope']}) |"
    )
    lines.append(
        f"| Diagnostic (A) | shape-pass ÷ convergence-eligible in-envelope "
        f"| {cv['diagnostic_a']:.1%} "
        f"({cv['n_shape_pass_eligible']}/{cv['n_eligible']}) |"
    )
    lines.append(
        f"| Convergence-excluded | non-converged in-envelope cells "
        f"| {cv['n_excluded_nonconv']} (by shape: {cv['excluded_by_shape']}) |"
    )
    lines.append(
        f"| Stress (α ≥ {ALPHA_STRESS:.2f}) | shape-pass among stress cells "
        f"(not gated) | {cv['stress_shape_pass']:.1%} ({cv['n_stress']} cells) |"
    )
    lines.append("")
    if cv["n_excluded_nonconv"]:
        lines.append(
            f"> **Convergence-excluded cells.** {cv['n_excluded_nonconv']} "
            "in-envelope cell(s) fall below the convergence precondition "
            f"(< {CONVERGENCE_FRAC:.0%} of replicates pass R̂ / bulk-ESS) and so are "
            f"excluded from the headline (B {cv['headline_b']:.1%}) but not from the "
            f"diagnostic (A {cv['diagnostic_a']:.1%}); by shape: "
            f"{cv['excluded_by_shape']}. Under the field-standard gate (R̂ / bulk-ESS "
            "only; divergences are recorded but not auto-failing — "
            "`cell_lib.convergence_pass`, Decision 33 / §A5.5.1) these are genuine "
            "sampling-convergence failures, not the benign flat-null divergences the "
            "earlier zero-tolerance gate tripped on."
        )
        lines.append("")

    # ----- Per-axis pass rates ------------------------------------------- #
    lines.append("## 2. Per-axis pass rates")
    lines.append("")
    for axis, col in [
        ("alpha", "alpha_true"),
        ("shape", "shape_name"),
        ("tier_weights", "tier_weights_name"),
        ("N", "n"),
    ]:
        lines.append(f"### 2.{axis}")
        lines.append("")
        lines.append(
            f"| {axis} | n_cells | alpha-cov pass | shape pass | both |"
        )
        lines.append("|---|---|---|---|---|")
        for key, grp in df.groupby(col):
            n_k = len(grp)
            cov_k = grp["alpha_coverage_pass"].astype(bool).mean()
            r_k = grp["pearson_r_pass"].astype(bool).mean()
            both_k = (
                grp["alpha_coverage_pass"].astype(bool)
                & grp["pearson_r_pass"].astype(bool)
            ).mean()
            lines.append(
                f"| {key} | {n_k} | {cov_k:.0%} | {r_k:.0%} | {both_k:.0%} |"
            )
        lines.append("")

    # ----- Failed cells -------------------------------------------------- #
    failed = df[~both_pass].sort_values(
        ["alpha_coverage", "median_pearson_r_pgen"]
    )
    lines.append("## 3. Failed cells (either criterion)")
    lines.append("")
    if failed.empty:
        lines.append("None — every cell passed both criteria.")
    else:
        lines.append(
            "| cell_id | alpha_cov | median Pearson r | median W-1 "
            "| convergence_pass | divergences |"
        )
        lines.append("|---|---|---|---|---|---|")
        for _, row in failed.iterrows():
            lines.append(
                f"| `{row['cell_id']}` "
                f"| {row['alpha_coverage']:.2f} "
                f"| {row['median_pearson_r_pgen']:.4f} "
                f"| {row['median_wasserstein_1_pgen']:.2f} "
                f"| {row['convergence_pass_rate']:.2f} "
                f"| {int(row['n_divergences_total'])} |"
            )
    lines.append("")

    # ----- Diagnostics --------------------------------------------------- #
    lines.append("## 4. Diagnostics")
    lines.append("")
    lines.append(
        f"- Mean fit-seconds per replicate: "
        f"{float(df['mean_fit_seconds'].mean()):.2f}"
    )
    lines.append(
        f"- Min cell-level convergence pass rate: "
        f"{float(df['convergence_pass_rate'].min()):.2%}"
    )
    lines.append(
        f"- Cells with any divergences: "
        f"{int((df['n_divergences_total'] > 0).sum())}/{n_cells}"
    )
    lines.append("")

    # ----- Wasserstein-1 supplementary ----------------------------------- #
    lines.append("## 5. Wasserstein-1 supplementary")
    lines.append("")
    lines.append(
        "Wasserstein-1 is reported per cell as a distribution-sensitive "
        "shape metric (prereg §4 line 334). Its flagging threshold remains "
        "deferred (spec.md §5; needs empirical posteriors to anchor) and is "
        "NOT part of the binding rule."
    )
    lines.append("")
    lines.append(
        f"- Median across cells: "
        f"{float(df['median_wasserstein_1_pgen'].median()):.2f}"
    )
    lines.append(
        f"- 90th percentile across cells: "
        f"{float(df['median_wasserstein_1_pgen'].quantile(0.9)):.2f}"
    )
    lines.append("")
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Summarise one grid of the two-unit recovery simulation into "
            "REPORT.md + grid-summary.parquet."
        )
    )
    parser.add_argument(
        "--grid-dir",
        required=True,
        type=Path,
        help=(
            "Grid root, e.g. "
            ".../recovery-grid-two-unit/inscription-mass (cell-summaries "
            "are read from <grid-dir>/outputs/cell-summaries/)."
        ),
    )
    parser.add_argument(
        "--assert-grid-a-regression",
        action="store_true",
        help=(
            "Hard-assert the inscription headline B / diagnostic A reproduce the "
            "validated 2026-05-22/26 Grid-A figures (exit 1 on mismatch). Use ONLY "
            "when re-running that exact design. For a new convention basis (e.g. the "
            "2026-06-06 Decision-38 re-validation) leave this OFF: the headline is a "
            "fresh measurement, not a regression target."
        ),
    )
    return parser.parse_args()


def main() -> int:
    """Load summaries, compute the verdict, write parquet + REPORT.md."""
    args = _parse_args()
    grid_dir = args.grid_dir.resolve()

    df = add_corrected_flags(load_all_summaries(grid_dir))
    verdict = compute_verdict(df)          # lodged criterion (reference)
    cv = compute_corrected_verdict(df)     # corrected §A5.5.1 criterion (binding)

    parquet_path = write_grid_summary_parquet(df, grid_dir)
    report = make_report(df)
    report_path = grid_dir / "outputs" / "REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    unit = str(df["unit"].iloc[0]) if "unit" in df.columns else "unknown"
    print(f"[grid-summariser] unit={unit}-mass  n_cells={verdict['n_cells']}")
    print(
        f"[grid-summariser] LODGED (reference): coverage {verdict['frac_cov']:.1%}, "
        f"shape-r {verdict['frac_r']:.1%} -> "
        f"{'PASS' if verdict['validated'] else 'FAIL'}"
    )
    print(
        f"[grid-summariser] CORRECTED (§A5.5.1, BINDING): headline B "
        f"{cv['headline_b']:.1%}, diagnostic A {cv['diagnostic_a']:.1%}, "
        f"excluded {cv['n_excluded_nonconv']} {cv['excluded_by_shape']} -> "
        f"{'PASS' if cv['validated'] else 'FAIL'}"
    )

    # Built-in regression check — DESIGN-SPECIFIC, OPT-IN. The GRID_A_* references
    # are the 2026-06-03 adjudication figures for the *validated 2026-05-22/26
    # design* (Decision 33 / §A5.5.1); they guard a re-run of THAT design against a
    # silent partition/criterion regression. A *different* convention basis (the
    # 2026-06-06 Decision-38 re-validation) has no such reference — its headline is
    # a fresh measurement ("Grid A 98.6% does not transfer"). So: hard-assert (exit
    # 1 on mismatch) only when the caller opts in via --assert-grid-a-regression;
    # otherwise surface the Grid-A delta as informational context and never abort.
    if unit == "inscription":
        for label, got, ref in [
            ("headline B", cv["headline_b"], GRID_A_HEADLINE_B),
            ("diagnostic A", cv["diagnostic_a"], GRID_A_DIAGNOSTIC_A),
        ]:
            delta = got - ref
            ok = abs(delta) <= REGRESSION_TOL
            if args.assert_grid_a_regression:
                print(
                    f"[grid-summariser] regression {label}: {got:.1%} vs Grid-A ref "
                    f"{ref:.1%} -> {'OK' if ok else 'MISMATCH'}"
                )
                if not ok:
                    print(
                        f"[grid-summariser] ERROR: corrected-criterion regression "
                        f"FAILED for {label} (got {got:.4f}, ref {ref:.4f}, "
                        f"tol {REGRESSION_TOL}). Criterion/partition changed.",
                        file=sys.stderr,
                    )
                    return 1
            else:
                print(
                    f"[grid-summariser] basis-shift {label}: {got:.1%} "
                    f"(Grid-A {ref:.1%}; Δ {delta:+.1%}) -- informational; this "
                    f"design's headline is a measurement, not a Grid-A regression "
                    f"target. Pass --assert-grid-a-regression only when re-running "
                    f"the validated Grid-A design."
                )

    print(f"[grid-summariser] wrote {parquet_path}")
    print(f"[grid-summariser] wrote {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
