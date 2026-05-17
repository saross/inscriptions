# Round-3 Saturation Check — Preregistration

## BLOCKING

### 1. H3c is still incorrectly described as mixture-corrected in several high-salience scope passages

**Pointer:** Field 2 “Scope of the mixture correction”; plain-English Step 6; §3 “Bayesian NBR for H3a” response-variable paragraph; §9 known limitations.

**Problem:** The current draft correctly states that H3a uses date-window-filtered counts and that the Bayesian mixture is not applied to `y_c`, but it repeatedly adds that mixture correction applies to “the H3c residual analysis” or “H3c-via-residuals”. That is not operationally true: H3c residuals are Pearson residuals from the H3a posterior, and H3a’s posterior is based on date-filtered counts, not mixture-corrected counts.

**Why it matters:** This falls under rubric item 2, especially Decision 22. The current wording creates an internal contradiction: H3c is technically specified as a residual analysis of the date-filtered H3a regression, but the scope prose implies that H3c receives mixture correction. Because H3c is confirmatory, this is more than cosmetic claim drift.

**Concrete suggested fix:** Replace every “H3c-via-residuals” / “H3c residual analysis” occurrence in the mixture-correction scope with wording like:

> The Bayesian mixture corrects the temporal SPA analyses: H2.1 validation and H3b deviation-detection. H3a and H3c are cross-sectional analyses of date-window-filtered counts; H3c inherits H3a’s date-filtered-count scope and does not propagate mixture-posterior uncertainty.

Then keep H3c’s Pearson-residual technical specification unchanged.

---

## SHOULD-FIX

### 2. The multinomial observation model still needs a precise normalisation / effective-count definition

**Pointer:** §3 “Bayesian deconvolution-mixture model”, observation model.

**Problem:** The model says `y_t` is “per-bin observed aoristic mass … rescaled to integer effective counts by multiplying by the effective sample size N and rounding”, then uses `y_t ~ Multinomial(N, p_t)`. This is potentially ambiguous because an SPA constructed as summed per-inscription probability mass normally already sums to N; if such mass is then multiplied by N, the resulting vector would scale incorrectly. The prose elsewhere says the observed SPA is treated as compositional shape data — proportions in each bin — but the binding formula does not explicitly define the raw mass → proportion → integer count transformation.

**Why it matters:** This falls under rubric item 2 / Decision 19. The likelihood family is now chosen, but the observation-vector construction is still just imprecise enough to create an implementation ambiguity in the central Bayesian mixture model.

**Concrete suggested fix:** Add a formal transformation before the multinomial statement, for example:

```text
Let m_t be the raw aoristic SPA mass in bin t, with Σ_t m_t = N_eff.
Define q_t = m_t / Σ_t m_t.
Define y_t = round_to_sum_N(q_t, N_eff), using deterministic largest-remainder rounding so Σ_t y_t = N_eff.
The primary likelihood is y ~ Multinomial(N_eff, p), where
p_t = α p_conv,t + (1 − α) p_gen,t.
```

Alternatively, if you intend to use the fractional SPA mass directly in a custom log-likelihood, say that explicitly and do not describe it as a standard multinomial count vector.

---

## Overall assessment

Round 3 is **close to saturated but not fully saturated**. I did not find a new confabulation suspect in the added numerical narrative, nor a broad failure of Decisions 18–26. The remaining work is narrow: one real internal contradiction about H3c’s mixture-correction scope, and one precision fix in the central multinomial likelihood’s count/proportion construction. Once those two are corrected in the preregistration text, I would move the verdict to: “Round-3 saturation check returns no findings of magnitude that warrant a further revision cycle; ready to lodge subject to the planned statistician consultation.”
