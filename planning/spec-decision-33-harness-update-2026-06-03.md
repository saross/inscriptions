---
title: "Spec — recovery-grid harness update to the Decision-33 / §A5.5.1 corrected criterion"
author: "Claude (Opus 4.8, 1M context), on Shawn's brief"
date: 2026-06-03
status: APPROVED 2026-06-03 by Shawn — §6 denominator = (A) eligible-in-envelope; implement once Grid B finishes (Martin draft-stage nod still pending, non-blocking for adjudication)
scope: "grid-summariser.py + compare-grids.py — adjudication-criterion change only; no re-fit"
supersedes-criterion-in: "runs/2026-05-26-recovery-grid-two-unit/code/{grid-summariser.py, compare-grids.py}"
---

# Spec: grid-harness update to the corrected binding criterion (§A5.5.1)

## 1. Objective

Update the two recovery-grid adjudication scripts to compute the **§A5.5.1
corrected criterion** (Decision 33) **alongside** the lodged criterion they
currently compute, so the headline Grid A / Grid B verdict and the cross-grid
comparison are adjudicated on the corrected metric while still reporting the
lodged-criterion reference for transparency.

**No re-fitting.** Every quantity the corrected criterion needs is already
stored per cell (§4); the change is pure post-processing over the existing
`cell-summaries/*-summary.json`.

## 2. What the criterion changes (lodged → corrected)

Source of truth: `planning/osf-amendment-2026-05-29-two-measure-framework.md`
§A5.5.1; `planning/decision-log.md` Decision 33.

| Element | Lodged (current harness) | Corrected (§A5.5.1) |
|---|---|---|
| Convergence | implicit (reported) | **explicit precondition**: cell eligible iff `convergence_pass_rate ≥ 0.90` |
| Shape gate | `median_pearson_r_pgen ≥ 0.95` for **all** shapes (flat → `nan` → auto-fail) | **hybrid**: non-flat → `median_pearson_r_pgen ≥ 0.95` (**unchanged**); `flat_baseline` only → `median_wasserstein_1_pgen ≤ T_flat = 10 y` |
| α (mixing weight) | binding gate: `alpha_coverage ≥ 0.90` | **demoted to diagnostic** — report signed bias + 90th-pct \|bias\| (≈0.18); **not gated** |
| Scope | whole grid, binary pass/fail | **operating envelope** `α ≤ 0.70`; cells `α ≥ 0.95` reported as **stress sensitivity, not gated** |
| Grid verdict | `frac_cov ≥ 0.90 AND frac_r ≥ 0.90` | `frac(shape-pass among eligible in-envelope cells) ≥ 0.90` |

Pre-committed thresholds (do not tune to the verdict): `T_flat = 10.0 y` (max W1
among well-recovered flat cells = 9.8, rounded up); `α-envelope = 0.70`;
`convergence_frac = 0.90`; `shape Pearson floor = 0.95` (unchanged).

## 3. New constants

```python
T_FLAT_YEARS        = 10.0          # flat-shape W1 gate (§A5.5.1)
ALPHA_ENVELOPE      = 0.70          # operating-envelope ceiling
CONVERGENCE_FRAC    = 0.90          # explicit convergence precondition
SHAPE_PEARSON_PASS  = 0.95          # unchanged (non-flat)
GLOBAL_FRAC_PASS    = 0.90          # unchanged (grid-level fraction)
FLAT_SHAPE          = "flat_baseline"
ALPHA_STRESS        = 0.95          # reported separately, never gated
```

## 4. Stored fields the corrected criterion reads (verified present)

From a Grid A `*-summary.json` (re-read 2026-06-03):

- `shape_name` — one of {bimodal, flat_baseline, regnal_cluster, rise_and_fall,
  smooth_decline, smooth_growth}; flat case = `flat_baseline`.
- `median_pearson_r_pgen` — non-flat shape gate (≈`nan` for flat).
- `median_wasserstein_1_pgen` — flat shape gate (defined for flat).
- `convergence_pass_rate` — explicit convergence precondition.
- `alpha_true` — envelope partition (observed set {0.05, 0.30, 0.50, 0.70, 0.95};
  read from data, do **not** hardcode).
- α-bias for the diagnostic is already collected in
  `<grid>/outputs/tables/alpha-bias.parquet` (`collect-alpha-bias.py`).

→ **No re-fit, no posterior reload.** Confirmed.

## 5. Per-cell derived columns (both scripts)

```python
is_flat              = shape_name == FLAT_SHAPE
convergence_eligible = convergence_pass_rate >= CONVERGENCE_FRAC
shape_pass_corrected = where(is_flat,
                             median_wasserstein_1_pgen <= T_FLAT_YEARS,
                             median_pearson_r_pgen     >= SHAPE_PEARSON_PASS)
cell_pass_corrected  = convergence_eligible & shape_pass_corrected
in_envelope          = alpha_true <= ALPHA_ENVELOPE
```

Retain the existing `alpha_coverage_pass`, `pearson_r_pass`, `both_pass`
(lodged) columns unchanged, so both criteria sit in `grid-summary.parquet`.

## 6. Grid-level verdict (corrected) — DECISION POINT for sign-off

§A5.5.1: *"In ≥90% of eligible cells: [shape pass] … evaluated where α ≤ 0.70."*
Two defensible denominators; they differ only if convergence failures cluster
in-envelope:

- **(A) eligible-in-envelope denominator** *(recommended):*
  `validated = mean(shape_pass_corrected | in_envelope & convergence_eligible) ≥ 0.90`,
  and report the convergence-exclusion count separately.
- **(B) all-in-envelope denominator:**
  `validated = mean(cell_pass_corrected | in_envelope) ≥ 0.90`
  (non-converged cells count as failures).

**Built-in correctness check:** whichever denominator is chosen, re-running the
updated `grid-summariser.py` over Grid A's stored summaries **must reproduce the
§A5.5.1 preview of 91.9% within-envelope shape-pass**. If it does not, the
denominator/partition is wrong. (This is the cheapest possible regression test
and should be asserted in the script's stdout.) → *Shawn to confirm A vs B; I'll
wire the 91.9% reproduction as a hard assertion either way.*

## 7. `grid-summariser.py` changes

1. Add the §3 constants.
2. Add §5 derived columns in `load_all_summaries` (or a new `add_corrected_flags`).
3. `compute_verdict` → return **both** verdicts: `lodged` (existing fields,
   renamed for clarity) and `corrected` (envelope shape-pass per §6), plus the
   full-grid corrected pass (incl. α≥0.95 stress) and the convergence-exclusion
   count.
4. `make_report` → §1 Headline shows **both** verdicts side by side
   (lodged 42.7% ref / corrected 91.9% envelope for Grid A), a new
   "operating-envelope vs stress (α≥0.95)" split, and an α-diagnostic block
   (signed bias, 90th-pct |bias| from `alpha-bias.parquet`). Keep the existing
   per-axis tables; add a `shape_pass_corrected` column.
5. `write_grid_summary_parquet` → persist the new derived columns too.

## 8. `compare-grids.py` changes

1. Mirror the §3 constants + §5 derived columns (it re-derives `both_pass` at
   `load`; add `cell_pass_corrected`).
2. `grid_verdict(...)` → add a `corrected=True/False` mode (envelope-restricted,
   hybrid shape gate) beside the existing `exclude_flat` diagnostic.
3. Four-way cross-unit classification (`both`, A-only, B-only, neither) → compute
   on `cell_pass_corrected` **within the operating envelope**, alongside the
   existing lodged-criterion classification. Stress cells (α≥0.95) tabulated
   separately, never in the headline four-way.
4. `COMPARISON-REPORT.md` → headline on corrected; lodged + flat-excluded kept as
   reference/diagnostic sections.

## 9. Validation before adjudication

1. `grid-summariser.py` on Grid A stored summaries → assert corrected
   within-envelope shape-pass == 91.9% (±rounding) — the §A5.5.1 preview.
2. A-vs-A smoke of `compare-grids.py` (as in the lodged harness) on the corrected
   path → four-way must be 100% `both` (a grid vs itself).
3. Only then run on Grid B once `GRID-B-END rc=0`.

## 10. Gates (do NOT implement/run until cleared)

- **Shawn sign-off on this spec** (esp. §6 denominator A vs B).
- **Martin draft-stage nod** on the α-diagnostic operationalisation + envelope
  cut (§A5.5.1 explicitly flags this for his second opinion). Per the 2026-05-26
  recalibration this is a *draft-stage* check, not a blocker for adjudication —
  but the criterion stays **provisional** until he confirms.
- **Grid B finished** (`GRID-B-END rc=0`) before the cross-grid step.
- **HARD GATE (downstream):** OSF Amendment 01 must be lodged before any Stage-3
  *confirmatory* work. The harness update + adjudication themselves are within
  the pre-lodgement window (Decision 33 status); the Stage-3 launch is what the
  lodgement gates.

## 11. Effort / risk

~Half a day. Pure post-processing; reversible (old columns retained; both
verdicts reported). Main risk is the §6 denominator choice — de-risked by the
91.9% reproduction assertion. No compute, no API, no re-fit.
