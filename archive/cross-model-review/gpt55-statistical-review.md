# Targeted Statistical Review of the Preregistration

**Project:** Bayesian mixture-corrected SPAs of Latin inscriptions against Hanson urban population estimates  
**Purpose:** Targeted review of the statistical approaches before statistician consultation and Friday conference presentation  
**Status:** Prepared from the review response in this chat  

---

## Bottom line

My judgement is that the preregistration is **good enough to present on Friday as a statistically disciplined preregistration in final consultation**, but I would **not lodge it unchanged on OSF before a statistician has looked at the four primary items in the consultation pack**: the mixture likelihood, the recovery-simulation validation rule, the residual/spatial-inference design, and the PPC thresholds. Those are already correctly identified in the pack as the open statistical judgement calls. The document is not, in my view, in “another adversarial rewrite needed” territory.

The strongest parts are the **Mundlak negative-binomial specification**, the decision to make H3a the sole primary confirmatory quantitative result, the separation of H3b into exploratory temporal deviation-detection, and the explicit claim hierarchy. The weakest parts are the **multinomial likelihood over rounded aoristic mass**, the **limited per-cell replication in the recovery simulation**, and the **mixed Bayesian/frequentist treatment of Moran’s I**.

---

## Triage verdict

| Area | Verdict | What I would do before Friday |
|---|---:|---|
| H3a Mundlak NBR | **Strong / defensible** | Present confidently, but call `f_within` a latent-scale systematic-variation estimand. |
| H2 mixture model | **Promising but most exposed** | Present as a Bayesian deconvolution model with planned recovery validation, not as already statistically settled. |
| H2.1 recovery simulation | **Good structure; tolerances need statistician input** | Say the grid and pass/fail rule are preregistered but under external statistical review. |
| H3c residuals / Moran’s I | **Defensible but caveat-heavy** | Present as a Hanson-replication analysis; avoid overstating spatial-inference certainty. |
| PPC thresholds | **Right idea; numbers not ready** | Do not defend the straw thresholds in talk; say numerical PPC triggers will be pinned before fitting. |
| Multiplicity policy | **Mostly defensible** | Avoid any omnibus “all hypotheses supported” language. |
| Habit-removed trajectories | **Exploratory only** | Relegate to future/exploratory methods, not a main claim. |

---

## 1. Mixture observation model: main statistical vulnerability

The preregistration now defines the Bayesian deconvolution model as a compositional mixture, converting raw aoristic mass `m_t` into a normalised empirical shape `q_t`, then into integer counts `y_t` by deterministic largest-remainder rounding before fitting:

```text
y ~ Multinomial(N_eff, p)
p_t = α p_conv,t + (1 − α) p_gen,t
```

It also specifies Dirichlet-multinomial and rescaled negative-binomial supplementary fits.

That is a coherent modelling choice, but it is not innocuous. The key issue is that **aoristic mass is not the same thing as observed categorical bin counts**. A broad interval-dated inscription contributes fractional mass across many bins; the multinomial likelihood then treats the rounded bin vector as if it arose from `N_eff` categorical draws. That risks overstating temporal information, especially where wide template intervals dominate.

I would not say the multinomial is “wrong”. It is a reasonable pragmatic primary model if the goal is to estimate a **compositional artefact-versus-genuine shape**. But I would want the preregistration and presentation to avoid implying that this is a generative model of individual inscription dates. It is better described as:

> a compositional likelihood for the binned aoristic empirical curve, validated by recovery simulation and checked against overdispersed alternatives.

The consultation pack already asks exactly the right questions: whether multinomial-on-binned-aoristic-mass is appropriate, whether deterministic rounding biases inference, whether aoristic uncertainty should be propagated through the likelihood, and whether the components are identifiable when `p_conv` and `p_gen` become too similar.

**Recommendation:** keep the multinomial primary, but add one binding sensitivity if feasible: either a Dirichlet/logistic-normal likelihood directly on `q_t`, or a Monte Carlo sensitivity that re-runs the mixture on multiple latent-date/aoristic realisations. The latter need not be the primary model, but it would directly answer the statistician’s likely concern: “how much does α move when the interval uncertainty is not collapsed into one deterministic SPA?”

---

## 2. Convention component: much improved, but identifiability remains the central threat

The shift from “midpoint spikes” to wide-template slab encoding is a major improvement. The preregistration now specifies century, half-century, and reign-interval slab tiers, with each template depositing uniform mass across its interval, and year-precise inscriptions left in the genuine component.

The remaining statistical issue is **not** whether the convention component is archaeologically plausible; it is whether the model can distinguish:

1. a genuine smooth ancient rise/fall pattern;
2. broad editorial slabs;
3. genuine regnal clustering;
4. smoothing-prior artefacts.

The recovery simulation is therefore doing essential work. In the talk, I would say the deconvolution is “regularised and recovery-validated”, not merely “Bayesian”. The Bayesian framing alone does not solve identifiability; the recovery grid is what must demonstrate that the prior, convention dictionary, and genuine-shape prior can recover known mixtures.

---

## 3. Recovery simulation: right architecture, but 50 replicates is thin

The recovery simulation is one of the best parts of the design. It constructs synthetic observed SPAs from known genuine shapes, known α values, and known convention components, then validates recovery across a pre-specified grid. The pass rule requires ≥90% of cells to pass, with a cell passing if ≥90% of its replicates have 95% credible intervals containing the true α, plus Pearson `r ≥ 0.95` for recovered shape in ≥90% of cells.

My concern is the **precision of the per-cell pass/fail decision**. With only 50 replicates, a true 90% coverage cell has a fairly wide binomial uncertainty interval. A cell observed at 45/50 is treated as passing; 44/50 fails. That is a brittle boundary. If the number of cells is large, this brittleness will propagate into the ≥90% cell-pass rule.

**Recommendation:** for the final preregistration, I would prefer ≥100 replicates per cell, and ideally ≥200 for the smaller final grid. If compute cost is high, use a two-stage design:

1. run 50 replicates across the full grid to identify failure regions;
2. rerun boundary/high-risk cells at 200 replicates.

I would also not rely on Pearson `r` alone for shape recovery. Pearson correlation can be high even when localised mass is misplaced, especially with smooth curves. Add at least one local-mass-sensitive metric: integrated absolute error, Wasserstein-1, or maximum absolute bin deviation after smoothing. Pearson `r` can remain the headline continuity metric.

---

## 4. H3a Mundlak NBR: statistically the cleanest confirmatory component

This is the most defensible confirmatory analysis. The model uses a negative-binomial response for city inscription counts, splits log-population into within-province deviation and province mean, and estimates a within-province population-attributable variance fraction on the latent log scale.

The reason this is strong is that it fixes the earlier covariance problem. The consultation pack explicitly explains that the previous variance decomposition silently dropped covariance between population and province effects, while the Mundlak split makes the within-province component orthogonal to province membership by construction.

The latent-scale `f_within` is defensible because the question is about systematic variation in `log E[count]`, not raw count variance mixed with overdispersion. The preregistration also states that both numerator and denominator are computed on the same posterior draw, which avoids a common variance-decomposition ambiguity.

My caveats:

1. **The 0.10 threshold is substantively reasonable but arbitrary.** That is acceptable in a preregistration, provided the prior-predictive check confirms the rule is not vacuous.

2. **Unweighted variance across cities should be defended explicitly.** It answers “what share of city-to-city systematic variation?” not “what share of inscription-weighted variation?” That is fine, but a reviewer may ask. A population-weighted or inscription-weighted sensitivity would be useful but not necessary for the confirmatory result.

3. **Using date-window-filtered counts rather than mixture-corrected counts is a real scope limitation, but not a flaw.** The pack states clearly that the mixture corrects temporal SPA analyses, not per-city counts, and that a per-city mixture would be unidentified for ~600 of ~815 cities. This should be said plainly in the presentation.

---

## 5. PPC thresholds: right commitment, but do not defend the straw numbers yet

The preregistration has the right principle: PPC failure triggers are numerical, not narrative, and thresholds are pinned in a pre-Phase-2 design artefact before pilot-fit inspection. The current categories include prior-predictive count caps, posterior-predictive mean/std/tail/zeros, residual-vs-fitted slope, and province-level residual dispersion.

The consultation pack’s Q4 rightly admits that the straw thresholds are not yet trusted. I agree. For a heavy-tailed city-count model, “mean within 5%” may be less informative than:

- top-k share of inscriptions;
- maximum or 99th percentile city count;
- distribution of log-counts;
- posterior-predictive distribution of province-level totals;
- posterior-predictive Moran’s I or semivariogram of residuals.

I would add **one H3c-specific PPC**: compute spatial autocorrelation on posterior-predictive residual surfaces under the fitted H3a model. This does not replace the confirmatory Moran’s I test, but it tells you whether the model routinely generates residual spatial structure of the observed magnitude.

The failure response is good: if a trigger trips, revise transparently, report the preregistered model alongside the revised model, and file an OSF amendment. I would only soften “any trigger initiates model revision” into “any critical trigger” or define severity levels. Otherwise a mild tail discrepancy could force a formal revision even when the main model is adequate.

---

## 6. H3c residuals and Moran’s I: defensible, but easy to overstate

The Pearson residual definition is operationally clear and appropriate for a negative-binomial model. The preregistration computes residuals draw-wise using the full city-level posterior mean, including the province random intercept.

Including the province random intercept is not double-counting. It means residuals are deviations from the **full fitted city expectation**, not merely from the fixed population effect. That is defensible. But it also means the residual surface is not directly equivalent to Hanson’s simpler residual surface. It may remove province-level structure that Hanson’s residuals retained. I would frame H3c as “replicating the qualitative Hanson residual findings under a stricter multilevel model”, not as an exact numerical replication.

The asymmetric treatment is the most debatable part: the capitals contrast is draw-wise Bayesian, while Moran’s I is computed on posterior-mean residuals with conditional permutation inference, with posterior draws of Moran’s I reported supplementarily.

That is defensible because Moran’s I has a field-standard permutation procedure. But the interpretation needs a guardrail:

- If posterior-mean Moran’s I is permutation-significant and the posterior distribution of `I_s` is mostly positive, this is strong support.
- If posterior-mean Moran’s I is significant but the 95% posterior interval for `I_s` crosses zero widely, the result should be described as **permutation-significant on the posterior-mean residual surface, but sensitive to posterior uncertainty**.
- If the posterior distribution of `I_s` is centred near zero, I would not call H3c(ii) substantively supported even if the posterior-mean permutation test passes.

The current preregistration reports the posterior distribution of `I_s` but does not make it part of the decision rule. That is acceptable for lodgement, but the paper’s prose must not hide the posterior-uncertainty caveat.

---

## 7. Multiplicity: no correction is defensible if the prose is disciplined

The confirmatory claim hierarchy is quite clean. H2.1 is a gate, H3a is the sole primary quantitative confirmatory result, H3c(i) and H3c(ii) are separate Hanson-replication tests, and H3b is explicitly exploratory.

I would not require Holm correction across H2.1, H3a, H3c(i), and H3c(ii), because these are not four interchangeable tests of one omnibus null. The consultation pack’s own rationale is basically right.

The condition is that the paper must not later say “the confirmatory family was supported” or “H3c was supported” unless it is very explicit about each component. The current text already avoids an omnibus H3c claim, which is the key protection.

A conservative statistician might still ask for an H3c-only adjustment because H3c has two replication tests. I would resist that unless you want a single “H3c replication” claim. If the claims remain separate — capital over-production and residual spatial clustering — no correction is acceptable.

---

## 8. Habit-removed residual trajectories: useful but keep it exploratory

The habit-removed residual trajectory design is intellectually attractive, but statistically fragile. The pack correctly notes that raw city-SPA peaks are confounded by the empire-wide epigraphic-habit curve, and proposes decomposing each city into an empire-wide habit component plus city residual trajectory, then validating against foundation dates and bounded independent anchors.

My concern is that subtracting an empire-wide habit from sparse city SPAs can create artefacts: negative residual mass, scale-dependence through the choice of `w_c`, and selection bias in the richer case-study cities. A hierarchical GP or multilevel temporal model would be more principled, but that is probably too much for this paper.

For Friday: mention this only as an exploratory extension. Do not let it distract from H2/H3a/H3c.

---

## Suggested wording for Friday

I would use something like this in the presentation:

> The preregistration is statistically specified but still under external statistical review. The confirmatory population model is a Bayesian within-between negative-binomial regression estimating a latent-scale within-province population-attributable variance fraction. The main methodological risk lies in the Bayesian SPA deconvolution model: we treat the binned aoristic curve as compositional data under a multinomial primary likelihood, validate it by recovery simulation, and report overdispersed supplementary fits. The statistician consultation is focused precisely on that likelihood, the recovery-grid tolerances, residual spatial inference, and numerical PPC thresholds.

That wording is honest and defensible. It signals maturity without pretending that the statistician’s review is a formality.
