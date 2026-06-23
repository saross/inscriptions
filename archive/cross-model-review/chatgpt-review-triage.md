---
priority: 1
scope: in-stream-reference
title: "ChatGPT 5.5 cross-model review — triage"
audience: "Shawn, future CC instances"
status: working — bucket (b) being walked through with Shawn
started: 2026-05-17
inputs:
  - planning/cross-model-adversarial-review-preregistration.md
  - planning/chatgpt-cross-model-review-prompt.md
  - planning/preregistration-draft.md (the target)
  - planning/decision-log.md (esp. Decisions 12, 14, 16, 17)
  - planning/preregistration-changelog.md (review-cycle history)
---

# ChatGPT 5.5 cross-model review — triage

Same four-bucket pattern as the dual Claude review triage. The review
produced **7 BLOCKING, 6 SHOULD-FIX, and 3 MINOR** findings — 16 in
total. None are superseded by existing decisions in a way that lets us
close them as-is — bucket (a) is empty this time, which is consistent
with the cross-model rationale (ChatGPT was briefed to seek orthogonal
coverage).

Two **load-bearing** verifications were performed during triage and are
recorded inline below: the "96 zero-effect calibration cells" count
is correct against the run report but the arithmetic expression that
appears in the prereg is wrong; the Carleton, Campbell & Collard 2018
citation is real and accurate but the attribution wording is loose.

---

## Bucket (a) — superseded by existing decisions

*Empty.* ChatGPT explicitly read the changelog and avoided re-finding
settled items. The review's seven blocking findings all identify
remaining gaps that the Claude-side review and Decisions 12–17 did not
close.

---

## Bucket (b) — substantive, needs Shawn's input

### B1. H3a's confirmatory rule has the wrong logical direction (ChatGPT #1, BLOCKING)

**Issue.** Current wording: "the posterior 95 % credible interval [for
`f_within`] excludes 0.10." A posterior interval `[0.01, 0.08]` excludes
0.10 *from below* and would count as support under the current text,
even though it is evidence *against* the "non-trivial share" claim.

**Background.** Decision 12 records the intent as "population explains a
non-trivial share" (clearly directional). The symmetric "excludes 0.10"
wording is a slip during the comprehensive rewrite that lost the
directional intent.

**Options.**

- **B1.a — Directional posterior probability.** "H3a is supported iff
  `P(f_within > 0.10) ≥ 0.95`." Equivalent to "the posterior 95 % CI
  lies wholly above 0.10."
- **B1.b — Three-way decision rule.** Wholly above 0.10 = supported;
  wholly below 0.10 = explicit evidence against; straddling 0.10 =
  inconclusive. (Adds a named "evidence against" verdict.)

**Recommendation.** B1.a + a one-sentence note that an interval wholly
below 0.10 is reported as evidence against (so the asymmetry is
acknowledged without inventing a separate decision rule). Carry as
Decision 18.

---

### B2. The Bayesian mixture model has no likelihood (ChatGPT #2, BLOCKING)

**Issue.** §3 specifies the deterministic mixture equation
`observed_SPA(t) = α · convention_SPA(t) + (1 − α) · genuine_SPA(t)`
and priors on α, tier weights, and the genuine-component smoothness —
but never states the observation model. The posterior is undefined
without it.

**Plus a related ambiguity ChatGPT flags:** are `convention_SPA` and
`genuine_SPA` normalised densities, count intensities, or posterior
latent curves? And: is aoristic uncertainty propagated into the
likelihood, or only into the SPA upstream?

**Options.**

- **B2.a — Multinomial on binned counts.** `y_t ~ Multinomial(N, p_t)`
  where `p_t = α p_conv,t + (1 − α) p_gen,t` and the two component
  vectors are normalised densities. Standard for compositional shape
  inference; tractable.
- **B2.b — Poisson / negative-binomial intensities per bin.**
  `y_t ~ NegBin(λ_t · w_t, φ)` where `λ_t` is the per-bin intensity and
  `w_t` is the bin width. Handles overdispersion if the mixture is
  noisy.
- **B2.c — Dirichlet-multinomial.** Adds an over-dispersion parameter
  to the multinomial; intermediate cost.

The aoristic-uncertainty question is largely orthogonal: in any of the
above, `y_t` can be defined as either (a) the post-aoristic SPA bin
mass (a fractional count — fits multinomial/Dirichlet-multinomial
naturally if scaled), or (b) integer counts derived by an upstream
step. The recovery simulation makes one of these choices binding for
the validation step.

**Recommendation.** B2.a (multinomial on binned aoristic mass scaled to
integer effective counts via the empirical N) for the binding
specification, with B2.c as a sensitivity if posterior predictive
overdispersion checks fail. **Primary statistician question for
Martin** — the choice has identifiability consequences. Carry as
Decision 19.

---

### B3. Convention component may model the wrong object under Uniform aoristic (ChatGPT #3, BLOCKING)

**Issue.** §2 Description and the plain-English walkthrough say
"intervals such as `[1, 100]` and `[101, 200]` place aoristic mass on
midpoint years by construction." Under pure Uniform aoristic, this is
**not quite right**: a `[1, 100]` interval deposits mass uniformly
across all 100 years, with no midpoint preference. So why does the SPA
show 22.8× / 41.5× / 18.8× / 39.7× O/E spikes specifically at AD
50 / 150 / 250 / 350?

**What's actually going on (my read, needs Shawn's check).** The
empirical spikes are real but their mechanism is not "wide intervals
deposit on midpoints." The most likely mechanism is a *mixture* of
interval widths: a fraction of inscriptions are dated narrowly to
midpoint-adjacent years specifically (e.g. `[45, 55]`, `[50, 50]`),
because editors who can date more precisely than century often choose
round-decade or "mid-2nd-century" anchors. The wide-interval `[1, 100]`
contributions are flat plateaus; the narrow midpoint-anchored
contributions are the actual spikes.

**Implications for the convention component.**

- The current three-tier component (mass at century-start / end /
  midpoint years; plus half-century starts; plus reign-related years)
  **is a reasonable model for the narrow-interval midpoint convention**
  — those *are* mass anchors that look like spikes in the SPA.
- BUT — if the prereg's explanatory text describes the mechanism
  incorrectly, the model's relationship to the data is harder to
  defend. The model removes spikes at anchor years; the wide-interval
  plateaus are a different artefact that the model does *not* address.
- ChatGPT's deeper point: "decide which object is being modelled."
  Either model the convention component as the forward-aoristic
  distribution induced by conventional interval templates (slabs), or
  as anchor-year masses (the current choice), but be honest about
  which.

**Options.**

- **B3.a — Keep anchor-year tiers; fix the explanatory text.** Drop
  the "intervals place mass on midpoints by construction" mechanism
  claim; replace with an accurate description of the narrow-interval-
  midpoint mechanism. The wide-interval plateau artefact is then a
  named limitation, not a target of the deconvolution.
- **B3.b — Augment the convention component with slab/template
  layers.** Add a "century-slab" component (uniform mass on
  `[1, 100]`, `[101, 200]`, etc.) alongside the anchor-year tiers.
  Larger model; recovery simulation would need to test both. Probably
  the more honest model but more work.
- **B3.c — Reframe the deconvolution as removing anchor-year spikes
  only; rename `convention_SPA` accordingly.** Conservative scope
  reduction.

**Recommendation.** B3.a is the lowest-cost honest fix; B3.b is the
methodologically cleanest but adds modelling work. **A statistician
question** — Martin should weigh in on whether the slab layer matters
empirically. Carry as Decision 20.

---

### B4. H2.1 recovery simulation grid is not enumerated; "coverage" criterion is muddled (ChatGPT #4, BLOCKING)

**Issue.** The recovery-simulation grid is described qualitatively
("pre-specified parametric grid spanning empirical α range", "library
of plausible shapes", "tier weights from pilot fit") but no values,
parameter ranges, sample sizes, or replication counts are pinned. This
is a major RDF in the central validation step.

Plus the coverage criterion ("≥ 90 % of grid cells have the true α
inside the posterior 95 % CI") is not really coverage in the
repeated-sampling sense — that requires repeated synthetic datasets
per cell. With one synthetic dataset per cell, it's testing whether the
single realisation happened to include the truth.

**Options.**

- **B4.a — Enumerate the grid in the prereg, with repeated replicates
  per cell.** Add a compact grid table: α values, genuine-shape
  families, tier-weight vectors, sample sizes, interval-width
  distribution, replicates per cell, seed policy. Coverage computed
  over the replicates within each cell.
- **B4.b — Enumerate the grid; report cell-wise pass/fail per single
  synthetic.** Don't call it coverage; call it "single-replicate
  recovery success per cell, ≥ 90 % of cells pass." Cheaper, more
  honest about what's measured, but a weaker validation.
- **B4.c — Defer enumeration to a `runs/2026-05-XX-h2-grid/` artefact
  committed before any confirmatory analysis runs.** The prereg names
  the artefact and freezes the grid via that artefact's commit hash.

**Recommendation.** B4.a (with repeated replicates) is the
methodologically right answer; B4.c is the pragmatic compromise if
enumerating in-prereg makes the document unwieldy. **Statistician
question** — Martin should specify the right replicate count and the
right shape library. Carry as Decision 21.

**Subsidiary issue (ChatGPT flag, same finding):** the "mean Pearson
*r* ≥ 0.95" criterion can hide systematic failure in high-α or
convention-adjacent cells. Report cell-wise *r* not just the mean.
Fold into the same decision.

---

### B5. H3a may not actually use mixture-corrected data (ChatGPT #5, BLOCKING)

**Issue.** The primary RQ says "after controlling for editorial-
convention dating artefacts via a Bayesian deconvolution-mixture
model…" — but the H3a model is
`y_c ~ NegativeBinomial(mu_c, dispersion)` where `y_c` appears to be
the per-city inscription count (date-window-filtered, but not
mixture-corrected). The mixture model corrects the *temporal* SPA; it
is not obvious how it could produce a city-level cross-sectional
corrected count.

**Why this matters.** If the analysis runs as written, it answers
"how do raw date-filtered inscription counts scale with population?",
not "how do mixture-corrected counts scale with population?" That is a
does-it-answer-the-question failure.

**Options.**

- **B5.a — Narrow the claim.** State that H3a uses date-window-filtered
  inscription counts, and the mixture model corrects temporal SPA
  analyses (H2, H3b deviation-detection) but not the cross-sectional
  city-count regression. Lowest-cost honest fix.
- **B5.b — Specify the corrected response.** Define `y_c` as a
  posterior-weighted count derived from the city's `genuine_SPA` (e.g.
  integrate the posterior `genuine_SPA` over the city's analysis
  window, propagate posterior uncertainty into the NBR). Larger model;
  not obviously implementable for low-N cities.
- **B5.c — Hybrid.** Primary H3a uses raw counts (B5.a wording);
  sensitivity H3a uses posterior-weighted counts on the subset of
  cities where the mixture is well-identified (probably the largest 10–
  20 cities). Report both.

**Recommendation.** B5.a for the binding rule; possibly B5.c as
preregistered exploratory. **Statistician question** — Martin should
say whether the posterior-weighted-count approach is viable at all for
the ~815-city regression. Carry as Decision 22.

---

### B6. H3c residuals not operationally defined (ChatGPT #6, BLOCKING)

**Issue.** H3c uses "continuous posterior residuals" — but for a
Bayesian NBR, the choice between raw, Pearson, deviance, or log
residuals is non-trivial. For Moran's I in particular: is it run on
posterior mean residuals (single value per city), posterior median
residuals, one draw, or a posterior distribution of Moran's I values?
Conditional permutation inference on one residual vector is not the
same as propagating posterior uncertainty through Moran's I.

**Options.**

- **B6.a — Pearson residuals on posterior means; permutation
  inference per-k.** Simplest; standard. Loses posterior uncertainty in
  the spatial test.
- **B6.b — Posterior distribution of Moran's I across draws.** For
  each posterior draw, compute Moran's I; report the posterior
  distribution of Moran's I; significance via the fraction of draws
  with `I > 0` and per-draw permutation *p* < 0.05. Cleaner Bayesian
  treatment but more expensive (~1000 permutation tests per posterior
  sample stratum).
- **B6.c — Hybrid.** Capitals contrast: posterior contrast on
  draw-wise log residuals (already preregistered). Moran's I: on
  posterior mean Pearson residuals (B6.a) for the confirmatory rule;
  posterior distribution of Moran's I reported descriptively
  alongside.

**Recommendation.** B6.c — keeps the confirmatory rule tractable and
field-standard while reporting the fuller Bayesian quantity for
honesty. **Statistician question** — Martin should weigh in on whether
posterior-mean Pearson residuals are an acceptable simplification.
Carry as Decision 23.

---

### B7. LIST swap contingency leaves a live data/envelope choice (ChatGPT #7, BLOCKING)

**Issue.** §1 and §7 allow the analytical envelope to extend from AD
350 to AD 600 "if the LIST swap completes during the fortnightly paper
sprint (11–24 May 2026)." "Completes" is not operationally defined;
the consequences are large (dataset, envelope, mixture model, Phase 3
counts, Late Antique additions).

**Easy resolution.** Today is 2026-05-17. The fortnight ends in 7 days.
The swap is not done. The decision is effectively forced.

**Options.**

- **B7.a — Freeze LIRE v3.0 for this OSF lodgement.** LIST v1.2
  becomes a separate post-lodgement amendment or follow-up paper.
- **B7.b — Keep the contingency with hard objective criteria.** Define
  "completes" as: a specified schema check passes, a specified row-
  count reconciliation passes, a date-envelope-validation passes — by
  a hard calendar cutoff before any model output is inspected.
- **B7.c — Pre-commit to LIST and delay lodgement** until the swap is
  ready.

**Recommendation.** B7.a — clean, honest, and matches the project
state. Carry as Decision 24.

---

### B8. Prior- and posterior-predictive failure triggers need numerical thresholds (ChatGPT #8, SHOULD-FIX)

**Issue.** "Most counts in `[0, 10^4]`", "no implausibly large counts",
"divergent", "remaining structure", "beyond Monte Carlo noise" — none
of these are binding criteria. Yet failed checks trigger model
revision.

**Options.**

- **B8.a — Numerical PPC thresholds in the prereg.** E.g. prior
  predictive 99th-percentile count < 10⁴; posterior predictive mean
  within 10 % of observed; PP standard deviation within 20 % of
  observed; residual-vs-fitted slope absolute value < 0.05; etc.
- **B8.b — Numerical thresholds set in a pre-lodgement appendix; the
  prereg names the appendix.** Same effect, less in-prereg text.
- **B8.c — Keep narrative triggers but commit to reporting the
  originally-preregistered model result alongside any revised model.**
  Lighter-touch; addresses the "preserving confirmatory status across
  workflow-driven revision" concern.

**Recommendation.** B8.a is the prereg-disciplined answer; B8.c is the
pragmatic minimum. Carry as Decision 25, with the actual thresholds
specified after Martin's pass (he'll have an opinion).

---

### B9. H3a Hanson-population uncertainty sensitivity (ChatGPT #9, partial, SHOULD-FIX)

**Issue.** Hanson population estimates are treated as exact in the H3a
regression. The estimates are themselves uncertain; treating them as
exact understates the posterior on `β_within` / variance fraction.

**Options.**

- **B9.a — Lognormal measurement-error sensitivity.** Add a sensitivity
  analysis that treats `log_pop_c ~ Normal(log_pop_observed_c, σ_pop)`
  with σ_pop pinned to a plausible value (e.g. 0.2 = ~20 % SE on
  population). Report whether the H3a variance fraction CI changes
  materially.
- **B9.b — Use the existing α-as-translator and scaling-residual
  sensitivity analyses to absorb this concern.** Argue these already
  test robustness to population-mediated confounds. Cheaper; less
  direct.
- **B9.c — Defer to follow-up.** Flag as a known limitation in §9.

**Recommendation.** B9.a as a preregistered exploratory sensitivity
(small additional model; clearly defensible). Fold into the
"additional H3a sensitivities" list — no new decision needed if Shawn
just agrees.

**Other parts of ChatGPT #9 (centring/standardisation, variance
weighting) are bucket (c) — see below.**

---

### B10. Western-Empire province list not enumerated (ChatGPT #10, partial, SHOULD-FIX)

**Issue.** H3b's "Western-Empire provincial subset" is named but not
defined. List the provinces.

**Options.**

- **B10.a — Explicit list in §4.** E.g. the "Latin West" — Italia,
  Gallia (Narbonensis, Lugdunensis, Belgica, Aquitania), Germania
  (Inferior, Superior), Britannia, Hispania (Tarraconensis, Baetica,
  Lusitania), Africa Proconsularis, Numidia, Mauretania (Caesariensis,
  Tingitana), Pannonia, Noricum, Raetia, Dacia, Dalmatia. Or
  whatever the canonical "Western Empire" partition is for this paper.
- **B10.b — Define by language: provinces where Latin is the dominant
  epigraphic language**, with the list derived from LIRE itself.

**Recommendation.** B10.a — explicit list, with Shawn's choice of
canonical partition (he knows this better than ChatGPT or me). Carry as
a triage resolution (not a full decision).

---

## Bucket (c) — mechanical / clarity

Apply directly once bucket (b) decisions are locked.

### C1. H3a predictor centring and standardisation specs (ChatGPT #9, partial)

Add to §3 H3a spec:

- `within_pop_c = log_pop_c − mean(log_pop) within province` (already
  in the spec; explicit grand-centred / not formulation needed for
  `log_pop_province_mean`).
- State whether predictors are standardised before applying the
  `Normal(0, 1)` priors. Without standardisation, `Normal(0, 1)` is
  weakly informative for `β_within` *if* `within_pop_c` is on the
  natural log scale and within-province log-population varies by O(1).
  With standardisation, `Normal(0, 1)` is mildly informative on the
  standardised coefficient.
- State `Var(...)` denominator: unweighted across cities, Rome-
  excluded.

### C2. Subset filter primary picks pinned (ChatGPT #10, partial)

- Military subset: `type_of_inscription_clean == 'military diploma'`
  is primary; `type_of_inscription_auto` is the named sensitivity.
- Asclepius subset: regex `[Aa]esculap|[Aa]sclep` on `inscription`
  free-text is primary if Glomb et al.'s exact filter is not
  recoverable from their published methods by a stated pre-analysis
  date; otherwise their exact filter is primary.

### C3. Confirmatory claim hierarchy paragraph (ChatGPT #11)

Add a paragraph (probably under Field 3 or §6) stating:

- H2.1 is a gate for using the mixture model (failure triggers
  amendment, not just an asterisk on H3).
- H3a is the sole primary confirmatory result.
- H3c(i) and H3c(ii) are separate Hanson-replication confirmatory
  tests, each judged independently.
- No omnibus H3 claim is made.

### C4. Phase 1 cell-count arithmetic corrected (ChatGPT #12)

**Verified.** The "96 zero-effect calibration cells" count is correct
against the run report (empire 6 cells at n=50,000 only; province 48
across 8 n-values × 3 nulls × 2 shapes; urban-area 42 across 7 n-values
× 3 nulls × 2 shapes). The arithmetic expression
"3 levels × 2 nulls × (3 brackets × 2 shapes + 1 zero-effect
calibration) × 1 representative-n cell" evaluates to 42, **not 96**.
Replace with an accurate description (or with a reference to the run
report's grid table).

### C5. Carleton 2018 attribution narrowed (ChatGPT #13)

**Verified.** Carleton, Campbell & Collard 2018 (PLOS ONE 13:e0191055)
is the PEWMA paper on radiocarbon-time-series simulation. The prereg's
attribution — "framework adapts … PEWMA power-simulation framework for
cross-sectional SPA × covariate analysis" — overstates the connection.
PEWMA is a time-series method; the prereg's Phase 1 is cross-sectional
power simulation. Replace with ChatGPT's suggested wording (or a
variant):

> The simulation design is inspired by Carleton, Campbell & Collard's
> use of synthetic archaeological time-series with known effects to
> evaluate method recovery under chronological uncertainty; the
> present SPA permutation-envelope thresholding is project-specific.

### C6. Trapezoidal aoristic parameterisation (ChatGPT #14)

Define the trapezoid: edge weight, plateau width if any, normalisation,
behaviour for very short intervals (e.g. `width < 2 × edge_band`).
Take the parameter values from the existing implementation; if not yet
implemented, take the convention from the literature (e.g. `tempun`'s
"50/50 edge–plateau" or similar).

### C7. H2.1 wording "CI of α̂" → "posterior interval for α" (ChatGPT #15)

Field 3 and §6 H2.1 rows: replace "the posterior α̂ falls within the
95 % credible interval of the true α" / "CI of α̂" with "the posterior
95 % credible interval for α contains the known true α."

### C8. OSF amendment wording pre/post-lodgement (ChatGPT #16)

§7 contingencies: distinguish pre-lodgement (revise + changelog) from
post-lodgement (OSF amendment). Apply to all contingency clauses.

### C9. Centring/standardisation prior implications wording

Same site as C1 — if Shawn picks "standardised predictors", the
`Normal(0, 1)` prior is mildly informative; if not, the prior's
informativeness depends on the natural within-province log-population
scale. Note this in §3.

---

## Bucket (d) — verification required

### D1. Phase 1 zero-effect cell count (ChatGPT #12)

**Resolved during triage.** The count of 96 is correct against the run
report; the arithmetic expression is wrong. Applied as C4 above.

### D2. Carleton 2018 attribution wording (ChatGPT #13)

**Resolved during triage.** Citation is real and accurate; attribution
wording is loose and overreaches. Applied as C5 above.

---

## Plan from here

1. **Walk Shawn through bucket (b)** — items B1–B10 — one at a time;
   capture substantive resolutions as Decisions 18–25 in
   `decision-log.md`. Some items (B2, B3, B4, B5, B6, B8) are
   primary statistician questions; flag them as such in the decision
   entries.
2. **Apply bucket (c)** (and the resolved bucket (b) items) directly
   to `preregistration-draft.md`.
3. **Update `preregistration-changelog.md`** with a "ChatGPT-pass
   adversarial-review-driven revision" entry, mirroring the Claude
   entry.
4. **Build Martin's consultation pack** (Task #17) — curated extract
   of the decision log + the B-bucket questions where Martin's input
   matters most (B2, B3, B4, B5, B6, B8, and revisits of Decisions
   12–17).
5. **Lodge on OSF** after Martin's input is incorporated.

The prereg is closer to lodgeable than it was after the Claude pass,
but ChatGPT's bucket (b) is substantial — there are six genuine model-
specification gaps (B1–B6) and a clean dataset-freeze call (B7) before
this is lodgeable.
