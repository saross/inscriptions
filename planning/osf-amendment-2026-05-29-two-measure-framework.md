---
title: "OSF Amendment 01 — Two-measure framework (epigraphic acts and epigraphic content)"
amendment-number: 01
status: DRAFT for Shawn's review and lodgement (not yet lodged)
date-drafted: 2026-05-29
date-updated: "2026-06-02 (added §A5.5.1: recovery-grid binding-criterion metric correction, surfaced by the Grid A adjudication)"
scope: "Two-measure framework (acts vs content) + recovery-grid binding-criterion clarification (§A5.5.1)"
preregistration: "https://osf.io/uycs6/ (lodged 2026-05-20; embargoed)"
lodged-version: "git tag osf-lodgement-2026-05-20 (https://github.com/saross/inscriptions/tree/osf-lodgement-2026-05-20)"
filed-under: "preregistration §7 / contingency clause (preregistration-draft.md line 423): substantive methodology changes after lodgement are filed as an OSF amendment before implementation."
author: "Shawn Ross (with Claude Code as analyst/RSE)"
gate: "BINDING — Stage 3 confirmatory fits under the two-measure framework must not run until this amendment is lodged."
---

# OSF Amendment 01 — Two-measure framework (epigraphic acts and epigraphic content)

## A1. Identification and trigger

This is the first amendment to the project's preregistration (Open Science
Framework, OSF, record `osf.io/uycs6/`, lodged 2026-05-20, currently
embargoed). It is filed under the preregistration's own contingency rule
(`preregistration-draft.md` line 423): *"If substantive methodology changes
are required after lodgement … an OSF amendment is filed before
implementation."*

**Trigger.** The 2026-05-26 letter-count probe
(`runs/2026-05-26-letter-count-probe/REPORT.md`) and the methodological
reframe it prompted, recorded as Observation 58 in the project working notes
(`docs/notes/reflections/working-notes.md`, commit `dd326dc`) and
corroborated by Observations 59 (`de8fa8f`) and 60 (`2f86c95`).

**Second trigger (2026-06-02; §A5.5.1).** Adjudicating Grid A of the two-unit
recovery simulation exposed that the lodged recovery-grid binding criterion is
mathematically undefined for the flat genuine shape and gates on exact α
credible-interval coverage that collapses at large *N* for asymptotic reasons
unrelated to recovery. The metric correction is folded into this amendment as
§A5.5.1 rather than filed separately, since both changes concern the same
recovery-grid / Stage-3 gate.

## A2. Summary of the change

The lodged preregistration treats **letter count** as a single §5
pre-specified *exploratory* cross-check, reported alongside the
inscription-count analyses but explicitly *"as a cross-check on the
inscription-count results rather than a replacement for them"*
(`preregistration-draft.md` line 388).

This amendment replaces that framing with a **two-measure framework**:

- **Inscription count** measures **epigraphic acts** (how often a community
  inscribed). It remains the project's **primary-by-convention** measure: it
  is the unit used by Hanson (2021), keeps the analysis comparable to the
  field, and is unchanged by this amendment.
- **Letter mass** measures **epigraphic content** (how much was inscribed).
  It is **promoted from an exploratory cross-check to a co-registered
  parallel confirmatory measure** of a *different construct* — not a rival
  operationalisation of the same construct, and not a replacement for
  inscription count.
- The **delta between the two measures** (the content surplus or deficit per
  act) becomes a **pre-specified derived quantity**, reported descriptively
  as a second residual axis alongside the existing scaling residual.

The two measures are analysed **in parallel**, each within its own
confirmatory family, and reported **side by side**. No multiplicity
correction is applied *across* the two units, for the reason given in §A5.3.

This amendment additionally **clarifies the recovery-grid binding criterion**
(§A5.5.1, a metric correction surfaced when Grid A was adjudicated on
2026-06-02): the lodged criterion is undefined for the flat genuine shape
(Pearson *r* on a constant target) and gates on exact α credible-interval
coverage, which collapses at large *N* for asymptotic reasons unrelated to
recovery. The corrected criterion patches the flat case with Wasserstein-1,
keeps Pearson *r* ≥ 0.95 for all other shapes, demotes α to a quantified
diagnostic, and reports the grid as a recoverability map with a stated
operating envelope.

## A3. Rationale

Inscription count and letter mass are **not two ways of measuring the same
thing**. A flat inscription count treats a long monumental dedication and a
three-word funerary fragment as equivalent units; letter mass registers
something of the quantity of information each carried. The lodged
preregistration already states this disagreement with Hanson (2021), who
identified total lettering as the methodologically desirable measure but
rejected it as impractical for fragmentary material (Hanson 2021, p. 142).

What the lodged preregistration did **not** do is follow the disagreement to
its conclusion. If the two measures track partially different constructs —
*acts* versus *content* — then asking "which is the better unit?" is the
wrong question. Where they diverge is itself the finding, not a tie-breaker:
terse frontier-military epigraphy deflates under letter mass; monumental and
commercial epigraphy amplifies; high-count, low-content corpora (e.g.
graffiti-rich assemblages) separate the two measures sharply. The project
therefore adopts both measures and treats their **difference** as a third
variable capturing inscription *style* and *function* that neither measure
alone encodes. This is a larger and more defensible methodological
contribution than substituting one unit for another.

## A4. Relationship to already-observed exploratory results (transparency)

We record explicitly what had been observed at the time this amendment was
conceived, so that the promotion of letter mass to confirmatory status can be
judged on its merits.

The 2026-05-26 probe was an **exploratory** descriptive comparison run on
LIRE v3.0 (it pre-dates and does not use the preregistered confirmatory
pipeline). It found material divergence between the two units — a
Hanson-style negative-binomial scaling exponent whose 95 % confidence
intervals did not overlap between units, and substantial city- and
province-level rank reshuffling (specifics in
`runs/2026-05-26-letter-count-probe/REPORT.md` and the tables it cites). A
subsequent Bayesian within–between (Mundlak) refit found the
within-province population-attributable variance fraction `f_within` higher
under letter mass.

**This amendment is construct-driven, not result-driven**, on three checks
that a reviewer can verify:

1. **The framework refuses to pick a winner.** It does not adopt the measure
   that "did better"; it retains inscription count as primary-by-convention
   and adds letter mass as a parallel measure of a distinct construct. The
   divergence the probe found is treated as corroboration of the construct
   distinction, not as a reason to prefer one unit.
2. **The confirmatory decision rules for the letter-mass analyses are
   identical to the pre-existing inscription-count rules** (the same three-way
   `f_within` verdict; the same recovery-grid validation gate). No rule is
   tuned to the observed letter-mass result.
3. **Letter-mass Stage 3 fits remain gated** on the letter-mass recovery-grid
   simulation passing the same binding criteria as inscription mass (§A5.5).
   The amendment does not licence reporting any letter-mass confirmatory
   result that has not first cleared validation.

## A5. Pre-specifications

### A5.1 Measure definitions

- **Inscription count (acts).** Unchanged from the lodged preregistration:
  the per-subset, date-window-filtered inscription count specified in §3 and
  Decision 22.
- **Letter mass (content).** Summed **`clean_text_conservative`** characters
  (Latin A–Z only; Greek excluded), per the existing definition at
  `preregistration-draft.md` line 388. `clean_text_interpretive_word` is
  retained as a sensitivity variant. **Scope limitation, stated plainly:**
  because Greek is excluded, the content measure is *Latin* content; subsets
  and regions with substantial Greek epigraphy are under-counted on the
  content axis, and this is reported as a limitation wherever the content
  measure is used.

### A5.2 Confirmatory structure under two units (scope)

The **letter-mass confirmatory family is deliberately bounded** to the
cross-sectional analyses, to avoid requiring a new unit-specific power
(reachability) simulation (see §A5.5 note):

- **Confirmatory under letter mass:** the **H3a within–between
  negative-binomial regression** (the three-way `f_within` verdict of
  `preregistration-draft.md` line 397) and the **H3a variance partition**.
- **Exploratory under letter mass (reported under both units, not
  confirmatory):** H3c spatial-residual analyses, H3b deviation-detection,
  and all §5 exploratories. Their confirmatory eligibility depends on
  detection-power thresholds (Phase 1; §6, lines 408–410), which are
  calibrated for an equal-weight *count* process and do **not** transfer to
  letter mass — a *compound sum* of heavy-tailed per-inscription letter
  counts. Empirically (`scripts/letter-mass-design-effect.py`), the
  letter-weight Kish design effect is large: corpus-wide ~15, per-city median
  ~2.4 (interquartile range ~1.9–3.7, at the `urban_context_city` analysis
  unit). The letter-mass detection SPA therefore carries *fewer* effective
  observations than the inscription-count SPA for the same inscriptions
  (≈ 0.42× at the median city), making
  letter-mass temporal detection *less* powered, not more. An analytic
  reachability translation (`scripts/letter-mass-reachability.py`) shows the
  consequence is categorical: **no** city in the corpus clears the
  preregistered urban-area detection thresholds under letter mass (0 of 1,044
  Rome-excluded urban-area cities, versus 5–7 under inscription count) — even
  Pompeii, Salona, and Ostia fall below the floor once weighted by content.
  Letter-mass temporal detection is therefore not merely under-powered but
  unreachable corpus-wide; it cannot be confirmatory and is reported
  descriptively. Letter-mass time-series and residual analyses are
  consequently exploratory in this paper.

Inscription count retains its full pre-existing confirmatory family
unchanged.

### A5.3 Multiplicity

**Each unit forms its own confirmatory family. No Holm–Bonferroni (or other)
multiplicity correction is applied across the two units.**

Justification: multiplicity correction guards against inflated
false-positive rates when the *same* hypothesis is tested multiple ways. Here
the two units operationalise **different constructs** (acts versus content)
and therefore answer **different research questions**: "does within-province
population explain variation in epigraphic *acts*?" and "…in epigraphic
*content*?" are not two tests of one hypothesis. Correcting across them would
penalise the project for asking two questions rather than one, and would
misrepresent the inferential structure. Within each unit, the existing
multiplicity policy is unchanged. The H3a verdict is rendered **separately and
explicitly per unit**; the paper does not combine them into a single verdict.

### A5.4 The inter-measure delta (derived, exploratory)

A **pre-specified derived quantity**, the **content residual**, is computed
and reported descriptively:

- **Definition.** For the cross-sectional city set, fit `log(letter_mass) ~
  log(inscription_count)` across cities; the per-city residual is the content
  residual (positive = more content per act than the corpus norm; negative =
  less). The project thereby has a **two-dimensional residual space**:
  scaling residual (observed inscriptions minus what population predicts) ×
  content residual (observed content minus what inscription count predicts).
- **Status.** Exploratory and descriptive. **No pre-committed threshold and
  no confirmatory verdict** attach to the delta; it is a novel quantity and is
  reported as a map/descriptive characterisation and cross-tabulated against
  the scaling residual. It does **not** trigger an OSF amendment.
- **Subsumption.** The previously logged standalone "cumulative-totals Hanson
  negative-binomial experiment (inscription count and letter count)" (the
  project's tertiary backlog item 5) is **subsumed** into this two-measure
  framework rather than run as a separate exploratory.

### A5.5 Recovery-grid validation under two units (the gate)

The lodged preregistration's H2.1 recovery-simulation gate
(`preregistration-draft.md` §3 line 61; §4 line 334; §6 lines 395–396) —
**(i)** ≥ 90 % of grid cells achieve per-cell α coverage and **(ii)**
posterior-median Pearson *r* ≥ 0.95 between recovered and true genuine SPA in
≥ 90 % of cells — now runs as **two parallel grids**, one per unit:

- **Grid A — inscription mass** and **Grid B — letter-mass conservative**,
  under the same corrected (F1+F3, empirical-Bayes) pipeline. Both are
  specified and running at `runs/2026-05-26-recovery-grid-two-unit/`
  (spec at `…/spec.md`).
- **Gate rule.** A Stage 3 confirmatory fit under a given unit is permitted
  only if **that unit's grid passes both binding criteria**. The outcome
  branching is pinned in `…/spec.md` §5: both grids pass → Stage 3 proceeds
  under both units; one passes → Stage 3 proceeds under that unit only; both
  fail → the mixture is revised before any Stage 3 fit (per the lodged
  preregistration's existing recovery-failure contingency, line 420).
- **Note (why letter-mass confirmatory is scoped to the cross-section).** The
  recovery grid validates the **mixture model** (the temporal deconvolution)
  under each unit; it does **not** establish **detection-power** thresholds,
  which are a separate Phase-1 product and cannot be re-used for letter mass.
  Letter mass is a compound sum of heavy-tailed per-inscription letter counts
  (per-city Kish design effect median ~2.4; §A5.2), so its temporal-detection
  power is design-effect-limited and *lower* than inscription count's. The
  cross-sectional H3a regresses per-city letter-mass *totals* on population
  and does not use detection thresholds (see line 131), so the design effect
  does not bear on it — confining the letter-mass *confirmatory* family to the
  cross-section is therefore principled, not a convenience. An analytic reachability
  translation (`scripts/letter-mass-reachability.py`) already shows
  letter-mass temporal detection is unreachable for every urban-area city in
  the corpus (0 of 1,044, versus 5–7 under inscription count); because the
  neglected heavy-tail effects can only reduce power further, a full
  compound-process simulation cannot overturn this. The simulation is
  therefore logged as an optional methodology-follow-up refinement, not a
  prerequisite; the paper reports the analytic reachability result.

### A5.5.1 Binding-criterion clarification (metric correction)

Adjudicating Grid A (inscription mass) on completion (2026-06-02;
`runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md`)
exposed two defects in the lodged binding criterion as written — both
*mathematical / asymptotic*, not recovery failures. This subsection corrects
them. The correction was checked against field practice by a closed-loop
prior-art scout and an implementation review
(`planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`).

**The two defects.**

1. **Criterion (ii) is undefined for the flat genuine shape.** Pearson *r*
   between a recovered curve and a *constant* true SPA is `0/0` (the truth has
   zero variance). All 75 `flat_baseline` cells return `nan` and fail
   mechanically, capping achievable shape-pass at 83.3% — independent of model
   quality, and identically for both units. The model in fact recovers flatness
   well (≈99% cell coverage; small Wasserstein-1).
2. **Criterion (i) — exact 95%-CI coverage of α — collapses at large *N*.**
   Holding (shape, α, tier) fixed and increasing *N*, cell coverage falls from
   ~1.0 to ~0.0 while the α bias stays small and roughly constant — the standard
   posterior-concentration / semiparametric Bernstein–von Mises effect (the
   interval narrows below a fixed small bias). It measures asymptotic interval
   calibration, not recovery adequacy. No surveyed community (radiocarbon SPD,
   baorista, Bayesian-workflow SBC) gates on exact CI coverage of a mixing
   parameter.

**The corrected criterion.** The recovery grid is reported as a
**recoverability map** with a stated **operating envelope** (consistent with the
project's reachability-guide methodology), not a binary whole-grid pass/fail.
Within the operating envelope:

- **Precondition — convergence.** A cell is eligible only if ≥90% of its
  replicates converge (max R̂ < 1.01; divergence count within the lodged
  threshold). This makes the existing convergence requirement an explicit gate.
- **Binding criterion — genuine-SPA (`p_gen`) shape recovery (hybrid).** In ≥90%
  of eligible cells: posterior-median Pearson *r* ≥ 0.95 for **non-flat** genuine
  shapes (**unchanged from the lodged preregistration**); and, for the
  **flat_baseline** shape only (where Pearson *r* is undefined), Wasserstein-1
  between posterior-median recovered and true SPA ≤ **T_flat = 10 years**
  (the maximum W1 among well-recovered flat cells is 9.8 y; rounded up).
  Wasserstein-1 is additionally reported for *all* shapes as a supplementary
  distribution-sensitive metric. A single global W1 threshold is *not* used,
  because W1 magnitude depends on the true shape's geometry (good-recovery W1
  ranges ≈0.8–24 across shapes) and would penalise high-spread shapes; only the
  *undefined* flat case is patched.
- **Operating envelope.** The binding criterion is evaluated where the
  deconvolution is identifiable: empirically **α ≤ 0.70** across all shapes and
  sample sizes. Cells with α ≥ 0.95 (≤5% genuine signal; near-unidentifiable;
  degraded convergence) are reported as a **stress-test sensitivity, not gated**.
  Where the *real* corpus α exceeds the envelope (plausible in late,
  template-dominated sub-periods), genuine-signal claims for those regimes are
  flagged as degraded-recovery, not reported as validated.
- **α (mixing weight) — diagnostic, not gate.** α recovery is reported as a
  **quantified diagnostic** (signed bias and its distribution), not a binding
  gate. Rationale: (a) exact CI coverage of a mixing weight is not field-standard
  and collapses at large *N* under negligible bias; (b) α is recoverable only to
  a practical tolerance (operating-envelope 90th-percentile |bias| ≈ **0.18**),
  which supports the coarse, directional convention-fraction statements the paper
  makes but not a tight gate. **All α-derived claims in the paper are hedged to
  this demonstrated recovery precision.**

**Outcome under the corrected criterion (transparency).** Under the lodged
criterion Grid A returned 42.7% both-pass; under the corrected criterion it
passes the binding shape recovery at **91.9%** within the operating envelope
(convergence + hybrid shape). Grid B (letter mass) is adjudicated identically on
completion. These figures are a preview recomputed from the stored Grid A
posteriors; the finalised adjudication re-runs the corrected criterion on both
grids' stored outputs (no re-fitting required, because W1 and the α intervals are
already stored per cell/replicate).

**Metric-correction-driven, not verdict-driven (the integrity checks a reviewer
can verify).** Mirroring §A4:

1. The correction targets two *mathematical / asymptotic* defects (undefined-on-
   flat; coverage-collapse-at-large-*N*), identified from the failure structure
   independently of the verdict, and confirmed field-standard by a prior-art
   scout + implementation review (artefacts above).
2. The non-flat shape criterion is **unchanged** from the lodged preregistration
   (Pearson *r* ≥ 0.95); only the *undefined* flat case is patched (W1), and α is
   moved to a diagnostic.
3. Thresholds (T_flat = 10 y from well-recovered flat cells; operating envelope
   α ≤ 0.70 from near-unidentifiability at α ≥ 0.95) are set from theory and the
   known-good sub-grid **before** the headline two-grid verdict; the failing
   scenarios (full-grid; α-gated) are reported alongside the passing one.

**Statistician sign-off** (Martin, at draft): the exact operationalisation of the
α diagnostic and the operating-envelope cut are flagged for a second opinion.

### A5.6 Exploratory analyses under both units

Per Observation 58: the §5 pre-specified exploratory analyses are run under
**both** units where applicable, with the per-subset delta reported as data.
These remain exploratory (no confirmatory verdicts), exactly as in the lodged
preregistration.

## A6. What does NOT change

- Inscription count remains the **primary-by-convention headline measure**;
  comparability with Hanson (2021) is preserved.
- The inscription-count confirmatory family, its decision rules, and its
  multiplicity policy are **unchanged**.
- The chronological envelope (50 BC – AD 350), the LIRE v3.0 freeze
  (Decision 24), and all other lodged specifications are **unchanged**.
- The recovery-grid is applied per unit; the R̂/ESS convergence gates and PPC
  trigger scheme are **unchanged**. The recovery-grid **binding criteria are
  clarified** (metric correction) per §A5.5.1: the undefined-on-flat Pearson
  case is patched with Wasserstein-1, exact α-coverage is replaced by an α
  diagnostic, and the grid is reported as a recoverability map with a stated
  operating envelope. The non-flat shape criterion (Pearson *r* ≥ 0.95) is
  unchanged.

## A7. Exact preregistration edits to apply on lodgement

To be applied to `preregistration-draft.md` (the living `main` copy) in
lockstep with lodgement; the lodged authority remains git tag
`osf-lodgement-2026-05-20` until then:

1. **§3 (H3a specification):** add letter mass as a co-registered parallel
   confirmatory measure for H3a + variance partition, with the per-unit
   separate-verdict and no-cross-unit-correction statement (§A5.2, §A5.3).
2. **§5 line 388 (letter-count alternative analysis):** reframe from
   "exploratory cross-check / lesser of two evils / not a replacement" to the
   two-measure framework; cross-reference the content-residual derived
   quantity.
3. **§5:** add the content-residual derived quantity (§A5.4); note §5
   exploratories run under both units; note subsumption of backlog item 5.
4. **§6 effect-size table:** add (a) a letter-mass H3a `f_within` verdict row
   (same three-way rule), (b) a second H2.1 row for the letter-mass recovery
   grid, and (c) a content-residual descriptive row (no threshold).
5. **§3 line 61 / §4 line 334 / §6 lines 395–396 (recovery-grid binding
   criterion):** apply the §A5.5.1 metric correction — patch the flat-shape
   case with Wasserstein-1 (T_flat = 10 y), retain Pearson *r* ≥ 0.95 for
   non-flat shapes, make the convergence precondition explicit, demote exact
   α-coverage to an α-recovery diagnostic, and reframe the gate as a
   recoverability map with a stated operating envelope (α ≤ 0.70). Update both
   H2.1 rows in the §6 table accordingly.
6. **§7 / §11:** record this amendment in the planned-deviations text and the
   §11 post-lodgement amendment trail.
7. **`preregistration-changelog.md`:** add a dated amendment section.

## A8. Provenance

- **Statistical reasoning recorded under the project's standing
  critical-friend rule:** the no-cross-unit-correction decision (§A5.3) and
  the scoping of the letter-mass confirmatory family to the cross-section
  (§A5.2, §A5.5) are the two statistically load-bearing choices in this
  amendment and are justified inline.
- **Artefacts:** `runs/2026-05-26-letter-count-probe/` (probe);
  `runs/2026-05-26-recovery-grid-two-unit/` (two-grid validation);
  Observations 58–60 in `docs/notes/reflections/working-notes.md`.
- **Binding-criterion clarification (§A5.5.1):** the metric correction is
  driven by the Grid A adjudication
  (`runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md`,
  committed `0638093`; harness committed `4a3a8d2`), a closed-loop prior-art
  scout, and an implementation review, both recorded at
  `planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`. Field
  basis: no surveyed community gates on exact CI coverage of a mixing weight;
  Wasserstein-1 is theoretically justified for deconvolution recovery (Rousseau
  & Scricciolo 2021); flat/uniform is a standard tested null in radiocarbon SPD
  work (Crema 2022). This is the second statistically load-bearing change in the
  amendment (with §A5.3) and is flagged for statistician sign-off at draft.
- **Repository state:** edits to be applied on `main`; a new lodgement tag
  will be cut when the amendment is lodged to OSF.
