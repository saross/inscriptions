# Cross-grid comparison — two-unit recovery simulation

Head-to-head of **inscription-mass** (Grid A) and **letter-mass** (Grid B) recovery grids. See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the binding decision rule and outcome-branching.

## 0. HARD GATE — OSF Amendment 01 not yet lodged

The Stage-3 launch path named in this report is a **recommendation only**. Per the project standing rule (memory `2026-05-26-40ce5927fddc`), **no Stage-3 confirmatory work may begin until OSF Amendment 01 is lodged** — even a both-PASS verdict does not authorise launch. Confirm lodgement with Shawn before any confirmatory-claim-producing run.

## 1. Binding verdict — corrected criterion (Decision 33 / §A5.5.1)

The **binding** cross-grid verdict uses the corrected criterion: a convergence precondition (≥ 90% of replicates) + a hybrid shape gate (median Pearson r ≥ 0.95 for non-flat shapes; Wasserstein-1 ≤ 10 y for flat_baseline), α demoted to a diagnostic, within the operating envelope (α ≤ 0.70). Headline **B** = clean-pass (convergence AND shape) over all in-envelope cells (binding); **A** = shape-pass among convergence-eligible cells. The lodged criterion is retained as a reference in §1R.

| Grid | headline B (binding) | diagnostic A | conv-excluded | Verdict |
|---|---|---|---|---|
| inscription-mass | **98.6%** (355/360) | 98.6% | 0 | PASS |
| letter-mass | **0.0%** (0/360) | n/a (no convergent cells) | 360 | FAIL |

**Outcome branch (binding): PASS / FAIL.** letter-mass calibration cohort lacks identifiability. Investigate the heavy-tail letter-count distribution (try a 99th-pct cap as sensitivity) and the cohort size. Stage 3 launches under inscription-mass only; letter-mass reported as a limitation.

### 1a. Four-way cell classification (corrected, operating envelope)

| classification | n cells |
|---|---|
| both-pass | 0 |
| inscription-only | 355 |
| letter-only | 0 |
| both-fail | 5 |
| stress(out-of-env) | 90 |

> **letter-mass convergence note.** **No** in-envelope cell reaches the 90% convergence precondition (max convergence_pass_rate < 0.90) under the field-standard R̂ / bulk-ESS gate; the heavy-tailed letter-count likelihood produces genuine sampling-convergence failures (poor mixing / low bulk-ESS), not merely benign divergences. Letter-mass fails on convergence before shape recovery is even assessable, so diagnostic A is undefined. This is consistent with inscription count being the primary unit of analysis (Obs 61).

## 1R. Per-grid verdicts — LODGED criterion (reference only)

**Binding rule (prereg §4 / spec §5):** a unit is validated only if ≥ 90% of cells pass coverage AND ≥ 90% pass median-Pearson-r ≥ 0.95.

| Grid | coverage pass-rate | shape-r pass-rate | both | Verdict |
|---|---|---|---|---|
| inscription-mass (as-written) | 69.8% (314/450) | 70.2% (316/450) | 42.7% (192/450) | FAIL |
| letter-mass (as-written) | 6.7% (30/450) | 13.3% (60/450) | 4.4% (20/450) | FAIL |

**Outcome branch (as-written): FAIL / FAIL.** Both unit choices fail the prereg-binding criteria. Stage 3 cannot launch under the current methodology as-written. Trigger a second diagnostic chain (analogous to 2026-05-24) on the two-grid failure pattern: likely a structural model revision, prior re-derivation, or a methodological pivot beyond the calibration-cohort empirical-Bayes design.

Before concluding the methodology is unsound, read the flat-excluded diagnostic verdict in §1b: part of the as-written FAIL is the known undefined-Pearson-r artefact on flat_baseline.

### 1b. Flat-baseline-excluded DIAGNOSTIC view (not the binding rule)

`flat_baseline` returns an undefined Pearson r (constant truth → zero variance; documented in `runs/2026-05-24-followup-systematics/`), so its 75 cells fail criterion (b) mechanically and cap as-written shape-pass at 83.3%. Excluding them isolates the genuine model-quality comparison. **This is diagnostic only; changing the binding metric is an OSF-amendment decision.**

| Grid | coverage pass-rate | shape-r pass-rate | both | Verdict |
|---|---|---|---|---|
| inscription-mass (flat-excluded) | 64.0% (240/375) | 84.3% (316/375) | 51.2% (192/375) | FAIL |
| letter-mass (flat-excluded) | 7.7% (29/375) | 16.0% (60/375) | 5.3% (20/375) | FAIL |

**Outcome branch (flat-excluded): FAIL / FAIL.** Both unit choices fail the prereg-binding criteria. Stage 3 cannot launch under the current methodology as-written. Trigger a second diagnostic chain (analogous to 2026-05-24) on the two-grid failure pattern: likely a structural model revision, prior re-derivation, or a methodological pivot beyond the calibration-cohort empirical-Bayes design.

## 2. Four-way cell classification

| classification | n cells |
|---|---|
| both-pass | 12 |
| inscription-only | 180 |
| letter-only | 8 |
| both-fail | 250 |

Filter views available in `cell-pass-comparison.parquet`: `both-pass` (good), `inscription-only` (letter-mass identifiability problem), `letter-only` (inscription-mass identifiability problem), `both-fail` (still need a structural rethink).

## 3. Failure localisation (per spec §5)

### 3.inscription-mass — per-shape both-pass-rate

| shape | n | cov pass | shape pass | both |
|---|---|---|---|---|
| flat_baseline | 75 | 99% | 0% | 0% |
| smooth_growth | 75 | 100% | 88% | 88% |
| smooth_decline | 75 | 97% | 88% | 85% |
| rise_and_fall | 75 | 53% | 87% | 40% |
| bimodal | 75 | 37% | 73% | 25% |
| regnal_cluster | 75 | 32% | 85% | 17% |

- Cells with α-coverage = 0.00 (CI never covers true α): **36** (by shape: {'regnal_cluster': 24, 'bimodal': 12}; by N: {50000: 25, 10000: 10, 2000: 1}). These recover shape well but α with biased precision — the α/shape-complexity likelihood ridge.

### 3.letter-mass — per-shape both-pass-rate

| shape | n | cov pass | shape pass | both |
|---|---|---|---|---|
| flat_baseline | 75 | 1% | 0% | 0% |
| smooth_growth | 75 | 9% | 7% | 5% |
| smooth_decline | 75 | 15% | 7% | 7% |
| rise_and_fall | 75 | 1% | 25% | 1% |
| bimodal | 75 | 3% | 8% | 3% |
| regnal_cluster | 75 | 11% | 33% | 11% |

- Cells with α-coverage = 0.00 (CI never covers true α): **236** (by shape: {'rise_and_fall': 55, 'bimodal': 53, 'regnal_cluster': 42, 'smooth_decline': 31, 'smooth_growth': 31, 'flat_baseline': 24}; by N: {2000: 104, 10000: 79, 50000: 53}). These recover shape well but α with biased precision — the α/shape-complexity likelihood ridge.

## 4. Figures

- `figures/fig-pass-rate-heatmap.png` — side-by-side (α × shape) both-pass-rate heatmaps, shared 0–1 colour scale (paper-figure candidate).
- `figures/fig-alpha-bias-by-tier.png` — recovered-α bias by tier and unit (paper-figure candidate).

## 5. Wasserstein-1 supplementary

W-1 is a distribution-sensitive shape metric reported per cell (prereg §4 line 334); its flagging threshold remains deferred and is NOT part of the binding rule.

- inscription-mass: median 7.90; 90th pct 19.39
- letter-mass: median 12.19; 90th pct 39.96

## 6. Methodology note for OSF Amendment 01

Binding criterion (b) (median Pearson r ≥ 0.95) is **undefined** for the `flat_baseline` shape (constant truth, zero variance), so it is unsatisfiable for that shape regardless of model quality, and caps as-written shape-pass at 83.3% for BOTH units. The amendment should either (i) exclude undefined-r cells from criterion (b), or (ii) substitute the Wasserstein-1 metric for the flat case. This is flagged for Shawn + statistician sign-off; this harness applies the criterion as currently written.
