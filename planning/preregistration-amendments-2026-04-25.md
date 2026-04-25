---
priority: 1
scope: in-stream
title: "Preregistration amendments arising from H1 plan review (2026-04-25)"
audience: "Shawn (edit + apply), Adela (co-author review), OSF reviewers"
status: draft; not yet applied to preregistration-draft.md
date: 2026-04-25
---

# Preregistration amendments — 2026-04-25

This document collects proposed amendments to `planning/preregistration-draft.md`
arising from the H1 simulation plan review. **Not yet applied** — Shawn reviews
and edits before these land in the main preregistration draft. Each amendment
lists the affected §, the verbatim current text, the proposed replacement, and
the rationale.

The preregistration has NOT yet been submitted to OSF, so these are pre-submission
edits, not post-submission amendments. After Shawn's edit pass they merge into the
main draft and the "draft 2026-04-24" status updates.

---

## Amendment 1 — Permutation-envelope primitive (prereg §3)

**Affected section:** Preregistration-draft §3 "Analysis pipeline" → "Permutation
envelope" bullet.

**Current text:**

> **Permutation envelope:** rcarbon-style `modelTest()` algorithm (Crema & Bevan
> 2021) ported to Python using `scipy.stats.permutation_test` as the primitive,
> `tempun` for aoristic replicates. Implementation ~200 LOC (Obs 3). Null model:
> exponential or piecewise-linear fitted growth (per Timpson et al. 2014); 1,000
> Monte Carlo replicates; two-sided 95 % envelopes.

**Proposed replacement:**

> **Permutation envelope:** rcarbon-style `modelTest()` algorithm (Crema & Bevan
> 2021) ported to Python as a hand-rolled Monte Carlo envelope loop following
> Timpson et al. (2014) directly. The loop samples MC replicates from the fitted
> parametric null, computes a pointwise 95 % envelope, and evaluates a global
> *p*-value as the proportion of MC replicates with at least as many bins
> falling outside the pointwise envelope as the observed SPA. Aoristic
> resampling is implemented as direct Uniform draws within `[not_before,
> not_after]` per Decision 4 (mathematically equivalent to the Uniform
> aoristic method documented in Kaše, Heřmánková & Sobotková's tempun package,
> which we reimplemented directly due to a numpy-2 incompatibility in tempun
> 0.2.4). Implementation ~200 LOC (Obs 3). Null models: **exponential (primary,
> per Timpson et al. 2014)** and **continuous piecewise-linear with k = 3
> knots (CPL-3; secondary, per Timpson et al. 2021)**; 1,000 Monte Carlo
> replicates; two-sided 95 % envelopes.

**Rationale:**

`scipy.stats.permutation_test` is an exchangeability test primitive for
two-sample comparisons with a user-supplied statistic. The within-SPA envelope
test we need is a single-sample comparison against a parametric null, which
is procedurally different (MC draws from null parameters → pointwise envelope
→ global-p on summary statistic, not label-shuffling between two observed
samples). The original prereg wording invoked `scipy.stats.permutation_test`
as "the primitive" but on inspection this conflates two levels of the test.
The amendment makes the method-description accurate to the operational test
(Timpson et al. 2014 MC envelope, hand-rolled) rather than implying an API
that doesn't fit.

**Methodological impact:** **none**. The change is in wording, not substance.
The algorithm described in the prereg is what we implement; we just describe
it correctly.

---

## Amendment 2 — Effect shape bracket (prereg §4 Phase 1)

**Affected section:** Preregistration-draft §4 "Pre-specified confirmatory
analyses" → "Phase 1 — H1 min-thresholds simulation protocol" → "Effect shape
for injection" paragraph.

**Current text:**

> **Effect shape for injection:** smooth (Gaussian-tapered) dip with FWHM matching
> each Decision 5 bracket's stated duration and magnitude at nadir matching the
> bracket's stated deviation. The Gaussian-taper choice (rather than step-function)
> is deliberately conservative: smooth effects are harder to detect via
> permutation-envelope methods, so thresholds set on smooth effects are upper
> bounds on the sample size needed for sharper effects.

**Proposed replacement:**

> **Effect shape for injection:** both **step-function (sharp)** and
> **Gaussian-tapered (smooth)** injected in parallel; thresholds reported as a
> range per bracket. The step-function is a box-car of bracket magnitude for
> bracket duration, producing the **lower bound** on n for detection ≥ 0.80
> (sharper events are easier to detect). The Gaussian has nadir = bracket
> magnitude and FWHM = bracket duration, producing the **upper bound** on n
> (smooth events with this nominal parametrisation are harder to detect via
> permutation-envelope methods). Reporting both is honest about shape-dependence
> of thresholds — real events span both shapes (e.g., Antonine Plague is sharp
> per Duncan-Jones 2018 military-diploma step-down; demographic decline is
> gradual). Detection rate ≥ 0.80 must be achieved for the **smooth-Gaussian**
> threshold (the binding, conservative bound) for a (level × bracket) cell to
> enter H3 confirmatory testing.

**Rationale:**

The original prereg adopted Gaussian-only to be "deliberately conservative." On
review, this trades interpretability: "50 % sustained over ≥ 50 y" reads most
naturally as "|effect| ≥ 50 % for a continuous 50 y window," which a
Gaussian with nadir = −50 % and FWHM = 50 y only satisfies at a single point.
Reporting thresholds as a range `[n_sharp, n_smooth]` preserves the conservative
interpretation (Gaussian upper bound is binding for eligibility), adds the
more-literal sharp interpretation as a lower bound, and honestly surfaces
shape-dependence for readers.

**Methodological impact:** increased compute (cell count doubles to 256);
decision-eligibility rule clarified (binding threshold is the Gaussian = smooth
upper bound, not the step-function lower bound). H3 subset eligibility is
unchanged in spirit (conservative) and clearer in letter.

---

## Amendment 3 — CPL knot count + exploratory k-sensitivity (prereg §4 + §5)

**Affected sections:**

1. Preregistration-draft §4 Phase 1 → "Null model" paragraph.
2. Preregistration-draft §5 "Exploratory analyses" (new bullets).

**§4 current text:**

> **Null model:** both **exponential (primary, per rcarbon / Timpson et al. 2014)**
> and **continuous piecewise-linear (CPL, secondary, per Timpson et al. 2021)**
> fitted; results compared. Rationale: CPL is more flexible but has more
> parameters; running both lets us check whether null-model choice materially
> affects the min-threshold conclusions.

**§4 proposed replacement:**

> **Null model:** both **exponential (primary, per rcarbon / Timpson et al. 2014)**
> and **continuous piecewise-linear with k = 3 knots (CPL-3, secondary, per
> Timpson et al. 2021)** fitted; results compared. CPL-3 is fixed a priori
> rather than AIC-selected per cell, to give a well-defined secondary threshold
> comparable across subsets and free of per-cell knot-choice edge cases.
> Rationale: CPL is more flexible than exponential but has more parameters;
> running both lets us check whether null-model choice materially affects the
> min-threshold conclusions, and fixed-k keeps the comparison clean.

**§5 new bullets (add to existing list):**

- **CPL knot-sensitivity analysis (exploratory).** For each CPL cell, fits
  k ∈ {2, 3, 4} and records AIC + detection per k. Reports threshold at each
  fixed k and the max−min range as a diagnostic for "does CPL threshold
  depend on knot count?" Non-confirmatory; reported in the paper's supplementary
  material.
- **CPL AIC-select threshold (exploratory).** Per-iteration picks k with
  minimum AIC from {2, 3, 4}; reconstructs threshold under AIC-select
  decision rule (cf. Timpson et al. 2021). Answers "what would AIC-selected
  CPL have given?" without re-simulation. Non-confirmatory.
- **Stratified-sampling sensitivity (exploratory).** Primary H1 thresholds
  use bootstrap (sampling-with-replacement) from filtered LIRE. Post-hoc,
  thresholds are recomputed using stratified-sampling (province-proportional
  or city-proportional draws) from the same persisted per-iteration parquet.
  Reports deltas to bootstrap primary; tests whether empirical province/city
  mix matters for detection power at given n. Non-confirmatory.

**Rationale:**

Fixed k = 3 gives a clean, well-defined secondary null for the comparison
question ("does a more flexible null shift the threshold?"). AIC-select and
k-sensitivity are natural follow-up questions ("does knot choice matter?",
"what would AIC pick?"); recording k ∈ {2, 3, 4} AIC + detection per iteration
enables both without re-simulation. Stratified-sensitivity addresses the
realism question ("bootstrap ignores empirical mix — does that change
thresholds?") without overcommitting the primary preregistration to a less
natural sampling scheme.

**Methodological impact:** confirmatory protocol unchanged (CPL-3 is the
preregistered secondary null). Three exploratory analyses added with explicit
non-confirmatory status, consistent with §5's existing treatment.

---

## Amendment 4 — Tempun dependency → direct reimplementation (prereg §9)

**Affected section:** Preregistration-draft §9 "Software, reproducibility,
and data access" → "Core dependencies (Python)" bullet.

**Current text:**

> **Core dependencies (Python):** `tempun` (SDAM, MIT), `numpy`, `scipy`,
> `pandas`, `pyarrow`, `pymc` (primary Bayesian NBR), `pyzotero`.

**Proposed replacement:**

> **Core dependencies (Python):** `numpy`, `scipy`, `pandas`, `pyarrow`,
> `matplotlib`, `joblib`, `pymc` (primary Bayesian NBR for H3a), `pyzotero`,
> `requests`, `python-dotenv`, `statsmodels`.
>
> **Aoristic resampling implementation note:** the Uniform aoristic method
> (per Decision 4) is implemented directly in `primitives.py::aoristic_resample`
> as ≤ 10 LOC of numpy. We did not use Kaše, Heřmánková & Sobotková's `tempun`
> package (SDAM, MIT; PyPI v0.2.4) because its current release is incompatible
> with numpy ≥ 2.4 (uses the removed `numpy.trapz`). The substitution is
> mathematically equivalent under the Uniform aoristic distribution. Upstream
> issue filed to `sdam-au/tempun` (this repo issue #4); once tempun is
> numpy-2-compatible, we may reintroduce it for H2/H3 pipelines where the
> package offers additional conveniences beyond Uniform aoristic.

**Rationale:**

Reflects the actual dependency manifest post-env-reconcile and discloses the
tempun substitution transparently for reproducibility. Preserves citation of
Kaše et al. Gives the SDAM community visibility on the compatibility gap.

**Methodological impact:** none; the aoristic method is unchanged (Uniform per
Decision 4).

---

## Application workflow

1. Shawn reviews this amendment draft.
2. Shawn applies amendments to `planning/preregistration-draft.md` directly
   (or asks CC to apply them with his edits).
3. `status` field of preregistration-draft updates to reflect the 2026-04-25
   revision.
4. `status` field of this amendment draft updates to "applied" with date.
5. Both files commit together for audit trail.

## Audit trail

- Decision source: `runs/2026-04-25-h1-simulation/decisions.md`.
- Plan source: `runs/2026-04-25-h1-simulation/plan.md`.
- AI contributions: this amendment draft was produced by CC during the
  2026-04-25 plan review session, under Shawn's direction, with four critical-
  friend surfacings and subsequent Shawn sign-off. Attribution logged in
  `planning/ai-contributions.md`.
