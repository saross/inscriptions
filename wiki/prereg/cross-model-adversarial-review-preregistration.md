# Cross-model adversarial review — preregistration

## BLOCKING findings

### 1. H3a’s confirmatory decision rule has the wrong logical direction

**Pointer:** Field 3, H3a; §3 “Confirmatory estimand and decision rule”; §6 effect-size table.

**Problem:** The rule is that H3a is supported if the posterior 95% credible interval for the within-province population-attributable variance fraction “excludes 0.10”. That is not equivalent to “population explains a non-trivial share”. A posterior interval of `[0.01, 0.08]` would exclude 0.10 and would therefore count as support under the current wording, despite being evidence *against* the intended claim.

**Why it matters:** This is a direct hypothesis → decision-rule failure. It could invert the interpretation of the primary result.

**Suggested fix:** Replace every “excludes 0.10” formulation with a directional rule, for example:

> H3a is supported iff the posterior 95% credible interval for `f_within` lies wholly above 0.10, equivalently `P(f_within > 0.10) ≥ 0.95`.

Also state explicitly that an interval wholly below 0.10 is evidence against the H3a claim, not support.

---

### 2. The Bayesian mixture model is not yet a complete statistical model

**Pointer:** §3 “Bayesian deconvolution-mixture model”; H2.1; §6 H2.1 rows.

**Problem:** The model specifies the deterministic mixture equation and priors, but not the likelihood / observation model. It is unclear whether the observed SPA vector is treated as counts, proportions, fractional aoristic mass, multinomial outcomes, Poisson / negative-binomial bin counts, Dirichlet-multinomial proportions, Gaussian errors around a smoothed curve, or something else. It is also unclear whether `convention_SPA` and `genuine_SPA` are normalised densities, count intensities, or posterior latent curves.

**Why it matters:** This is the central methodological contribution. Without the likelihood and normalisation conventions, the Bayesian model is not reproducible and its identifiability cannot be assessed. The priors alone do not define the posterior.

**Suggested fix:** Add a short formal observation model. For example, choose and state something like:

```text
Let y_t be the observed 5-year binned SPA mass/count in bin t.
Let p_convention,t and p_genuine,t be non-negative vectors summing to 1.
p_t = α p_convention,t + (1 − α) p_genuine,t.
y ~ Multinomial(N, p)
```

or, if overdispersion/fractional mass makes multinomial inappropriate, specify the alternative explicitly. The fix should state: target variable, bin units, normalisation, likelihood, overdispersion treatment, and whether uncertainty from aoristic allocation enters the likelihood or is handled upstream.

---

### 3. The convention component appears inconsistent with the stated Uniform aoristic SPA

**Pointer:** Description; plain-English Step 2; §3 “Convention component”; Decision 17 implementation in the draft.

**Problem:** The preregistration says the editorial convention is endpoint rounding to intervals such as `[1, 100]`, then models the convention component as mass at century starts, century ends, and century midpoints. But under the stated Uniform aoristic treatment, an interval `[1, 100]` contributes probability mass across the whole interval, not a point mass at AD 50. The current wording repeatedly says such intervals “deposit mass” on midpoint years. They do include the midpoint, but not preferentially.

**Why it matters:** This is not merely wording. If the model removes point-mass spikes at anchors while the actual aoristic artefact is a slab/plateau induced by wide conventional intervals, the deconvolution may correct the wrong object. It also raises a confabulated-specifics concern: the “midpoint spike” may be a property of interval-midpoint summaries rather than of the Uniform aoristic SPA.

**Suggested fix:** Decide which object is being modelled.

If the target is the **SPA**, define `convention_SPA` as the forward-aoristic distribution induced by conventional interval templates: century intervals, half-century intervals, reign-anchored intervals, etc. That means slabs over intervals, not point anchors.

If the target is the **endpoint/midpoint distribution**, rename the model accordingly and explain how its posterior is propagated into the SPA. Do not call midpoint mass an aoristic consequence unless the code really constructs SPAs from midpoints.

---

### 4. H2.1’s recovery simulation is still under-specified and its “coverage” criterion is statistically muddled

**Pointer:** Field 3 H2.1; §4 “Phase 2 — Bayesian mixture validation”; §6 H2.1 rows.

**Problem:** H2.1 refers to a “pre-specified parametric grid”, a “pre-specified library of plausible shapes”, an α grid “spanning the empirical pilot range”, and tier weights drawn from the empirical posterior of a pilot fit. The actual grid is not enumerated: no α values, genuine-shape parameters, tier-weight combinations, sample sizes, number of synthetic replicates per cell, width distributions, noise model, or random seed policy are fixed in the preregistration.

There is a second issue: “≥ 90% of grid cells have the true α inside the posterior 95% CI” is not really coverage unless each grid cell has repeated synthetic datasets. Coverage is a repeated-sampling property. One posterior interval per grid cell mostly tests whether a single synthetic realisation happened to include the truth.

**Why it matters:** This is a major researcher-degree-of-freedom problem in the central validation step. The recovery simulation could be made easy or hard by later choices. It also risks validating only the model’s ability to recover data generated from itself.

**Suggested fix:** Add a compact H2.1 grid table:

- α values, e.g. `{0.1, 0.25, 0.5, 0.75, 0.9}` or empirically justified alternatives;
- genuine-shape families and their exact parameters;
- tier-weight vectors, including posterior-like, flat, and corner/stress cases;
- sample sizes / total SPA mass;
- interval-width distribution source;
- number of synthetic datasets per grid cell;
- random seed policy;
- pass/fail rule computed over repeated replicates, not bare grid cells.

Also report cell-wise failures, not only the mean Pearson r. A mean `r ≥ 0.95` can hide systematic failure in high-α or convention-adjacent cells.

---

### 5. H3a claims to be “mixture-corrected”, but the NBR appears to use raw cross-sectional counts

**Pointer:** Primary research question; Field 3 H3a; plain-English Step 6; §3 “Bayesian NBR for H3a”.

**Problem:** The primary question says “After controlling for editorial-convention dating artefacts via a Bayesian deconvolution-mixture model…”. But the H3a model is specified as:

```text
y_c ~ NegativeBinomial(mu_c, dispersion)
```

where `y_c` appears to be the inscription count per Hanson city. The preregistration does not define `y_c` as a mixture-corrected count, nor explain how a temporal deconvolution model produces city-level corrected cross-sectional counts for ~815 cities, many with low N.

**Why it matters:** The analysis could run exactly as written and answer “how do raw date-filtered inscription counts scale with Hanson population?”, not “how do mixture-corrected inscription-production estimates scale with population?” That is a does-it-answer-the-question problem.

**Suggested fix:** Either:

1. **Narrow the claim:** state that H3a uses date-window-filtered inscription counts, not mixture-corrected counts, and that the Bayesian mixture corrects temporal SPA analyses but not the cross-sectional city-count regression; or
2. **Specify the corrected response:** define exactly how `y_c` is derived from the posterior `genuine_SPA` for each city/province and how uncertainty in that correction enters the NBR.

The first option is probably cleaner unless you truly have a stable city-level mixture correction.

---

### 6. H3c residuals are not operationally defined

**Pointer:** §3 “Residual analysis (H3c)”; §3 “Spatial clustering (H3c)”; §4 H3c; §6 H3c rows.

**Problem:** H3c uses “continuous posterior residuals”, but does not define the residual. For a negative-binomial Bayesian model, plausible residuals include raw residuals, log residuals, Pearson residuals, deviance residuals, posterior predictive residuals, residuals with or without the province random intercept, and residuals computed on posterior means versus draw-wise quantities.

For Moran’s I, it is also unclear whether the test uses posterior mean residuals, posterior median residuals, one residual draw, or a posterior distribution of Moran’s I values. Conditional permutation inference on a posterior residual vector is not the same thing as propagating posterior uncertainty through Moran’s I.

**Why it matters:** H3c(i) and H3c(ii) can change under different residual definitions. This is a direct researcher-degree-of-freedom issue in a confirmatory test.

**Suggested fix:** Add a formal residual definition, for example:

```text
For posterior draw s and city c:
r_c,s = log(y_c + 0.5) − log(mu_c,s)
```

or whichever residual is intended. Then state:

- whether `mu_c,s` includes province random effects;
- whether capitals contrast is draw-wise over `r_c,s`;
- whether Moran’s I uses posterior mean residuals, posterior median residuals, or a draw-wise posterior distribution;
- how the permutation p-value is combined with posterior uncertainty.

---

### 7. The LIST swap contingency leaves a live data/envelope choice

**Pointer:** Dataset section; Planned deviations and contingencies; Known limitations.

**Problem:** The preregistration allows the analytical envelope to extend from AD 350 to AD 600 “if the LIST swap completes during the fortnightly paper sprint (11–24 May 2026)”. “Completes” is not operationally defined, and the consequences are large: dataset, temporal envelope, subset composition, mixture model, Phase 3 counts, and Late Antique additions may all change.

**Why it matters:** This is a live dataset-selection degree of freedom. Even if no confirmatory analysis has been run, the criterion is too soft for a preregistration.

**Suggested fix:** Freeze LIRE v3.0 for this OSF lodgement and make LIST v1.2 a separate amendment or exploratory extension. If you retain the contingency, define objective readiness criteria that are independent of results: exact schema checks, join checks, row-count reconciliation, date-envelope validation, and a hard calendar cutoff before any substantive model output is inspected.

---

## SHOULD-FIX findings

### 8. Prior and posterior predictive failure triggers are too vague

**Pointer:** §3 “Prior predictive checks”; §3 “Posterior predictive checks”; §7 contingencies.

**Problem:** Phrases such as “most counts in [0, 10^4]”, “no implausibly large counts”, “divergent”, “remaining structure”, and “beyond Monte Carlo noise” are not binding criteria. Yet failed checks trigger model revision.

**Why it matters:** Model revision after seeing prior or posterior diagnostics is reasonable Bayesian workflow, but preregistration needs to constrain when that happens and how confirmatory status is preserved.

**Suggested fix:** Add numerical triggers, for example: prior predictive 99th percentile below a stated upper count; fewer than X% of draws with counts above Rome-excluded plausible maxima; posterior predictive tail-count checks outside specified posterior predictive intervals; residual-vs-fitted slope threshold; province-level residual dispersion threshold. Also state that the originally preregistered model result will be reported even if an amended model is fitted.

---

### 9. H3a predictor centring, variance weighting, and Hanson-population uncertainty need tightening

**Pointer:** §3 H3a model and estimand.

**Problem:** The within-between specification is conceptually right, but several details remain unstated:

- Is `log_pop_province_mean` grand-centred?
- Are predictors standardised before applying `Normal(0, 1)` priors?
- Is `Var(...)` computed unweighted across cities, population-weighted, inscription-weighted, or province-balanced?
- Are Hanson population estimates treated as exact?

**Why it matters:** These choices affect priors, MCMC geometry, the variance-fraction estimand, and the width of the posterior interval. Treating Hanson estimates as exact will understate uncertainty if the estimates are noisy.

**Suggested fix:** Define:

```text
within_pop_c = log_pop_c − mean(log_pop_c within province)
between_pop_c = mean(log_pop_c within province) − grand_mean(log_pop)
```

Then state whether these are standardised for modelling and whether the reported variance fraction is computed over unweighted Rome-excluded Hanson cities. Add a limitation or sensitivity for Hanson population uncertainty, even if only a simple lognormal measurement-error sensitivity.

---

### 10. H3b exploratory subsets are not fully pinned

**Pointer:** Field 3 H3b; §4 H3b; §8 subset-filter feasibility.

**Problem:** The Antonine and Crisis windows are pinned, but some subsets are not. The Asclepius subset may use Glomb et al.’s exact filter “if recoverable” or a broader keyword match. The military subset has both `type_of_inscription_clean == 'military diploma'` and an ML-classified alternative described as valid. “Western-Empire provincial subset” is not enumerated.

**Why it matters:** Even exploratory preregistered analyses should pin windows and subsets. Otherwise the exploratory output can still drift towards favourable or more interpretable results.

**Suggested fix:** Define primary and sensitivity filters now. For example:

- military primary: `type_of_inscription_clean == 'military diploma'`; auto-classified field sensitivity only;
- Asclepius primary: exact Glomb filter if published in sufficient detail by a specified pre-analysis date, otherwise the preregistered regex becomes primary;
- Western Empire: explicit province list.

---

### 11. Multiple-comparison / claim hierarchy should be stated explicitly

**Pointer:** Field 3 confirmatory hypotheses; §4 Phase 3; §6 table.

**Problem:** H3a, H3c(i), and H3c(ii) are all confirmatory, but the preregistration does not state whether they are independent claims, a hierarchy, or an omnibus H3 family. H3c is described as “two-part confirmatory”, but it is not explicit whether H3c is supported only if both parts pass.

**Why it matters:** This affects how the paper can phrase “the confirmatory hypotheses were supported”. It is not necessarily a statistical flaw, but it is a claim-discipline issue.

**Suggested fix:** Add a short “confirmatory claim hierarchy” paragraph:

- H2.1 is a gate for using the mixture model.
- H3a is the sole primary confirmatory result.
- H3c(i) and H3c(ii) are separate Hanson-replication confirmatory tests.
- No omnibus H3 claim is made unless all specified components pass; or define the alternative explicitly.

---

### 12. Phase 1 cell-count arithmetic still looks inconsistent

**Pointer:** §4 Phase 1 cell count; §6 Phase 1 power floor.

**Problem:** The text says:

> 3 levels × 2 nulls × (3 brackets × 2 shapes + 1 zero-effect calibration) × 1 representative-n cell ... = 96 zero-effect calibration cells

That expression does not yield 96 zero-effect calibration cells. It seems to conflate substantive-effect cells, zero-effect cells, and representative-n calibration cells.

**Why it matters:** This is completed groundwork, so it may not create a live degree of freedom, but it weakens trust in the simulation audit trail.

**Suggested fix:** Replace the arithmetic with the exact grid definition from the run report. If the 96-cell figure is correct, show the factors that multiply to 96. If not, correct the count everywhere.

---

### 13. The Carleton et al. 2018 citation wording is probably too broad

**Pointer:** §4 Phase 1: “framework adapts Carleton, Campbell & Collard (2018…)’s PEWMA power-simulation framework for cross-sectional SPA × covariate analysis.”

**Problem:** A quick spot-check confirms that Carleton, Campbell & Collard 2018 is the PLOS ONE PEWMA paper, but the paper frames itself as a simulation study of radiocarbon dating uncertainty and PEWMA time-series regression, not as a general “cross-sectional SPA × covariate” power-simulation framework. The prereg wording may be defensible as adaptation, but it is loose enough to invite a citation-audit correction. ([journals.plos.org](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0191055))

**Why it matters:** This is a confabulated-specifics risk, not a methodological blocker.

**Suggested fix:** Reword to something narrower:

> The simulation design is inspired by Carleton, Campbell & Collard’s use of synthetic archaeological time-series with known relationships to evaluate method recovery under chronological uncertainty, but the present SPA permutation-envelope thresholding is project-specific.

---

## MINOR findings

### 14. The trapezoidal aoristic sensitivity is underdefined

**Pointer:** §3 “Aoristic sampling”.

**Problem:** “Trapezoidal distribution” is described conceptually but not parameterised. Different trapezoids could produce different sensitivity results.

**Suggested fix:** Define the exact trapezoid: edge weight, plateau width if any, normalisation, and behaviour for very short intervals.

---

### 15. H2.1 wording says “CI of α̂” rather than posterior interval for α

**Pointer:** Field 3 H2.1; §6 H2.1.

**Problem:** “The posterior α̂ falls within the 95% credible interval of the true α” / “CI of α̂” is slightly backwards. The true α is fixed in the simulation; the posterior interval is for α.

**Suggested fix:** Use:

> the posterior 95% credible interval for α contains the known true α.

---

### 16. “OSF amendment before final results are lodged” should distinguish pre- and post-lodgement

**Pointer:** §7 contingencies.

**Problem:** Some contingencies refer to filing an OSF amendment before results are lodged. If this document is not yet lodged, changes are revisions; after lodgement, they are amendments.

**Suggested fix:** Use wording such as:

> before lodgement, the preregistration is revised and the changelog updated; after lodgement, an OSF amendment is filed before implementing the change.

---

## Overall assessment

Not yet lodgeable. The document is much stronger than the state described in the changelog, but there are still several preregistration-level blockers: the H3a support rule is logically wrong, the Bayesian mixture lacks a complete likelihood/target specification, the convention component may be modelling the wrong object under Uniform aoristic SPA, H2.1’s recovery simulation is not fully pinned, H3a may not actually use mixture-corrected data, H3c residuals are undefined, and the LIST contingency leaves a live dataset/envelope choice. I would move this to “lodgeable after fixes” once those blockers are resolved. I would move it to “lodgeable as-is” only after the fixes are made in the prereg text itself, not merely recorded as intentions in the decision log.
