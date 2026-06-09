# Full recovery-validation grid — spec (for Shawn sign-off)

**Status:** PROPOSED — needs Shawn sign-off before the sapphire grid (novel work +
reverses a lodged design decision + substantial compute). **Date:** 2026-06-09.
**Author:** Claude Code (Opus 4.8). Supersedes the lead design in `spec.md` §4 per the
POC (`outputs/POC-REPORT.md`). UK/Aus English.

## 1. The validated design (pivoted)

The joint model is **flexible per-unit convention basis + grid-alignment classification
binomial**, NOT the shared-basis + classification design `spec.md` led with (POC
Experiment 1 showed that fails — the confidently-wrong temporal term overpowers the
classification when the convention shape is constrained-wrong).

```
α            ~ Beta(1, 1)
tier_weights ~ Dirichlet(ones(n_tiers))
p_conv        = tier_weights · UNIT_BASIS         # per-unit: aoristic SPA of the unit's
                                                  #   grid-aligned-subset, as a (k×N_BINS)
                                                  #   basis (k bracket rows for shape freedom)
p_gen         = softmax(cumsum(σ·z))              # non-centred GRW (unchanged)
y_obs        ~ Multinomial(N_eff, α·p_conv + (1−α)·p_gen)
θ_conv, θ_gen ~ Beta(μ, κ)                        # calibrated (rule C: 0.945 / 0.155, κ=40)
k_aligned    ~ Binomial(N_rows, α·θ_conv + (1−α)·θ_gen)
```

`build_model_joint` already implements this (the basis argument is per-unit, not shared).
The only production-pipeline change vs H2.1 is: (a) build each unit's convention basis
from its grid-aligned-subset SPA; (b) pass `k_aligned`, `n_rows`. Everything else
(sampler, convergence gate, extraction) is unchanged.

**θ-prior κ = 40 confirmed (NOT widened).** Shawn and I initially agreed to widen the θ
prior to κ≈12; the empirical κ-sweep (`outputs/POC-REPORT.md` postscript) showed widening
*amplifies* a small positive bias rather than fixing the marginal high-α coverage — the
residual is estimated-basis *contamination* bias, not CI under-dispersion. **Keep κ = 40**;
the grid sweeps κ ∈ {40, 80} (tighter) as a sensitivity, not wider.

**Estimated-basis contamination — principled fix to evaluate (D-B).** The per-unit basis
from the aligned-subset SPA carries a faint copy of the genuine peak (`∝ α·θ_conv·p_conv +
(1−α)·θ_gen·p_gen`), giving a +0.09/+0.12 over-attribution at the stress corner. A fully
**cross-classified time × alignment** model — aligned-subset and non-aligned-subset
temporal SPAs as *separate* multinomials sharing (α, p_conv, p_gen, θ) — separates the
contamination instead of inheriting it, and likely removes the residual bias. The grid
evaluates {fixed estimated basis (lead), cross-classified} so we adopt the cross-classified
form as the lead only if it materially beats the simpler one on the bias surface.

**Decision needed (D-A): the per-unit-basis shape parameterisation** — single row
(SPA of aligned subset) vs the 3-row ±shift bracket the POC used (a little shape freedom).
Recommend the bracket; the grid tests both.

## 2. Grid axes (well-specified, Tier 1)

| axis | levels | n |
|---|---|---|
| regime / convention `%win` | identifiable (0.55, 0.63), confounded (0.85, 0.95, 1.00) | 5 |
| α_true | 0.0, 0.2, 0.4, 0.6, 0.8 | 5 |
| genuine shape | gaussian-early, gaussian-inwin, regnal-cluster, broad/uniform | 4 |
| N | 1500, 2800, 15000 | 3 |
| replicates | per cell | 20 |

Base grid = 5 × 5 × 4 × 3 = **300 cells × 20 = 6,000 fits** (matches the recovery-grid
scale). Convention basis fed to the fit is the **estimated (contaminated) aligned-subset
shape** (POC Experiment 3) — the production-realistic case — with the *true*-shape fit as
a reference arm on a 1-in-5 subsample.

**Robustness arms (smaller, layered):**
- **θ-mismatch** (spec §7d): generate with θ_gen_true ∈ {0.15, 0.25}, θ_conv_true ∈
  {0.95, 0.90}; fit with the calibrated priors. ~600 fits.
- **κ-sensitivity:** θ-prior κ ∈ {40, 80} on the confounded cells (tighter only — the
  κ-sweep ruled out widening). ~400 fits.
- **Cross-classified time × alignment variant (D-B):** the contamination-separating model
  (§1), evaluated head-to-head with the fixed-estimated-basis lead on the confounded +
  identifiable cells. ~600 fits.
- **Tier 2 interval-level** (spec §5): draw per-inscription intervals from a slab
  dictionary + genuine generator, classify with the real `aligned_i` rule, aoristic-SPA →
  (y, k). The cleanest test that the estimated shape + the binomial assumption are not
  load-bearing. Reduced axes (~100 cells × 10). 

Total ≈ **8,000–9,000 fits**. At ~4 s/fit on sapphire with `n_jobs=12` core-capped
parallelism, wall-clock ≈ **45–60 min** of compute (plus generation + aggregation).

## 3. Acceptance criteria (the verdict)

Per cell, aggregate over replicates:

1. **Do-no-harm (identifiable):** |median α bias| < 0.12 AND ≥ 0.90 coverage. (Primary.)
2. **Pulled-to-truth (confounded):** |median α bias| < 0.18, no systematic bias > +0.12,
   AND materially better than the shared-basis baseline (which the grid also runs). (Primary.)
3. **Coverage:** 95 % CI covers α_true at ≥ 0.90 across cells (diagnostic; the POC flagged
   marginal coverage at high-α confounded cells — quantify it).
4. **Convergence:** per-cell `convergence_pass` (max R̂ < 1.01, min bulk-ESS ≥ 400) ≥ 95 %.
5. **PPC** not degraded vs the temporal-only fit.
6. **Bias map:** report the residual-bias surface over (`%win`, α_true, N) so production
   units can be read against it (which units sit in a high-bias corner).

## 4. Production refit + reporting (after a clean grid)

- Re-fit the 28 H2.1 units (+ Italia) under the joint model; per-unit basis from each
  unit's grid-aligned-subset SPA; report the joint α with CI.
- The two-bound [shared, per-unit] sensitivity range stays as the *fallback* disclosure
  for any unit the grid flags as high-residual-bias.
- Reconcile the H3b identifiable set against the joint-α identifiability (the gap<0.20→17
  vs gap≤0.25→16 reconciliation folds in here).

## 5. OSF amendment plan

Fold into one amendment (supersedes `planning/prereg-note-2026-06-09-alpha-
identifiability.md`, whose "Planned remediation" section is now **wrong** — it still
describes the refuted informed-α *prior*):

1. Disclose the α-identifiability limit of the Amendment-03 **shared** basis for
   temporally-concentrated units (the diagnostic).
2. Adopt the joint model (flexible per-unit basis + classification likelihood) as the
   remediation; cite Feller 2016 + Gustafson 2010 (problem) and Huang & Bandeen-Roche
   2004 + Bronk Ramsey 2009 (the fix), per the scout synthesis.
3. Record the recovery-validation grid as the gate (criteria §3).
4. Note this **reverses** Amendment 03's shared-basis choice — the classification term is
   what makes the per-unit basis safe (it supplies the over-attribution control the shared
   basis was adopted to provide).

## 6. Critical-friend note (standing rule)

The pivoted design is *more* faithful to the concomitant-variable mixture than the
shared-basis version (a flexible mixture whose weight is identified by a covariate). The
remaining methodological exposure is the **residual positive bias** under the estimated
shape (POC +0.05 to +0.12) — the grid must characterise it, and we pre-commit to reporting
it (not tuning it away). The empirical κ-sweep already corrected one mistaken instinct
(widening the θ prior *amplifies* this bias). The **hybrid-over-units** model (global θ
estimated, α independent) is spec'd as a preregistered robustness check —
`hybrid-robustness-spec.md` — not as the lead.

## 7. Decisions — agreed + outstanding

**Agreed (Shawn, 2026-06-09):**
- Design pivot to per-unit basis + classification — approved *in principle*.
- Lead = Option 2 (per-unit + classification); **hybrid (Option 3) spec'd as a
  preregistered robustness check** (`hybrid-robustness-spec.md`).
- θ-prior κ = 40 (NOT widened — the κ-sweep reversed the widen-prior plan; §1).

**Outstanding for sign-off:**
- **(Q-launch)** Approve launching the **full grid** (≈ 8–9k fits, ~1 h sapphire compute)
  as specified — this is the compute + Amendment-03-reversal commitment.
- **(D-A)** per-unit basis = single-row vs 3-row-bracket (recommend bracket; grid tests both).
- **(D-B)** the **estimated-basis contamination** residual (+0.09/+0.12 at the stress
  corner): accept-and-report, or build + validate the **cross-classified time × alignment**
  model (§1) as the refined lead? (Grid evaluates both; the question is which we adopt as
  primary if both pass.)
- Papers: dedup done; full-text read + canonical Zotero staging tracked as follow-ups
  (`outputs/priority-papers-status.md`).
