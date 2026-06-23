This is an exceptionally mature, meticulously reasoned preregistration. The pivots you made during the adversarial review—specifically the shift to **forward-fitting** the null in true-date space (Decision 8), adopting the **Mundlak within-between specification** (Decision 12), and shifting the convention component from midpoint spikes to **wide-template slabs** (Decision 20)—have structurally sound-proofed this analysis against the most common critiques in computational archaeology.

Given your conference presentation on Friday and the tight timeline, I have put on my "applied statistician/econometrician" hat to give you a targeted, stand-in review addressing the exact questions you flagged in the **Martin Consultation Pack**. 

You can confidently present this framework on Friday. Here are my targeted statistical verdicts to help you push ahead.

---

### 1. The Mixture Observation Model (Q1)
* **The Ask:** Is Multinomial the right primary observation model, and is handling aoristic uncertainty upstream defensible?
* **Verdict:** **Yes, proceed as planned.** 
* **Reasoning:** Modeling the integer-rounded mass as a Multinomial distribution perfectly matches the compositional nature of your inquiry (what *proportion* of mass belongs to the convention vs. genuine signal). 
* **Aoristic Upstream:** Resolving aoristic uncertainty upstream (one SPA $\rightarrow$ one fit) is entirely defensible for a corpus of 115k inscriptions. Re-sampling latent dates per MCMC step would be computationally disastrous and mathematically redundant: by the Law of Large Numbers, the per-inscription uniform assignment washes out variance at the 5-year bin level.
* **Warning for Friday:** Be prepared for overdispersion. The Multinomial model assumes variance is strictly tied to the mean ($np(1-p)$). Archaeological data is notoriously "clumpy." Your decision to report the **Dirichlet-Multinomial** as a supplementary fit is the perfect safety net. If your Multinomial PPCs fail, you have a pre-registered off-ramp.

### 2. Recovery Simulation Grid & Coverage (Q2)
* **The Ask:** Is the 90% cell coverage rule with 50 replicates, and Pearson $r \ge 0.95$ for shape recovery, defensible?
* **Verdict:** **Statistically sound, but tweak the shape metric if possible.**
* **Reasoning:** A 90% coverage threshold is a standard, robust heuristic for Monte Carlo validation. However, with only 50 replicates per cell, your confidence interval for the coverage rate is wide (a true 90% rate has a 95% Wilson interval of roughly [0.79, 0.96]). If compute allows, bumping to **100 replicates** provides a much stabler pass/fail metric.
* **Shape Metric (Pearson r):** Pearson $r$ is scale and shift invariant. Because your vectors are compositional (sum to 1), scale invariance is fine. However, $r$ can sometimes be overly forgiving to localized mass redistribution. **Recommendation:** Keep $r$ for now so you don't derail your sprint, but for the paper, consider supplementing it with **Jensen-Shannon Divergence** or **Wasserstein Distance** (Earth Mover's Distance), which are the gold standards for comparing probability distributions.

### 3. H3c Residuals and Moran's I (Q3)
* **The Ask:** Are Pearson residuals on the Mundlak NBR right? Is the asymmetric treatment (draw-wise for capitals, posterior-mean for Moran's I) defensible?
* **Verdict:** **Highly defensible and elegantly pragmatic.**
* **Reasoning:** Including the province random intercept ($\alpha_{province}$) in your residual calculation is exactly the right move. If you excluded it, Moran's I would just flag the between-province variance as "spatial clustering." By including it, H3c properly tests for *sub-provincial* spatial structure.
* **Asymmetric inference:** Bayesian spatial econometrics is notoriously difficult. Forcing Moran's I into a fully Bayesian draw-wise framework breaks the standard conditional permutation inference spatial statisticians expect. Your compromise—using the posterior mean for the frequentist gold-standard test, while supplying the posterior distribution of $I$ as supplementary transparency—is the best of both worlds. 

### 4. Numerical PPC Thresholds (Q4)
* **The Ask:** What are defensible numerical thresholds for the NBR PPCs?
* **Verdict / Recommendations:** Negative Binomial models with random intercepts can generate massive tails. Here are defensible "straw" bounds you can confidently pin in your design artifact:
    *   **PP Mean:** $\pm 5\%$ of observed.
    *   **PP Std Dev:** $\pm 10\%$ to $15\%$ of observed (variance is harder to pin down than mean).
    *   **95th Percentile (Tail):** $\pm 20\%$ of observed. (NBR tails are highly volatile).
    *   **Proportion of Zeros:** $\pm 5$ percentage points of observed.
    *   **Residual vs. Fitted slope:** $< 0.05$ (standardized).

### 5. H3a Estimand: Mundlak Variance Fraction (Q5)
* **The Ask:** Latent (log) scale variance fraction, and the 0.10 threshold.
* **Verdict:** **Latent scale is correct. The 0.10 threshold is substantive.**
* **Reasoning:** You *must* compute this on the latent (log) scale. On the response (count) scale, the variance of a Negative Binomial is $\mu + \mu^2/\phi$. This means the variance depends on the mean, entangling the population effect with the baseline count of the city. The latent linear predictor cleanly separates the additive variance components.
* **0.10 Threshold:** In the noisy realm of archaeological survey data, claiming that *10% of the variance* is purely attributable to local population dynamics (after controlling for province-level effects) is a bold, substantive claim. It is not a vacuous prior.

### 6. Habit-Removed Trajectory (Q6)
* **The Ask:** Is the exploratory $SPA_c = w_c \cdot habit + residual_c$ decomposition confounded?
* **Verdict:** **Safe as exploratory.**
* **Reasoning:** By removing the empire-wide habit, you cleanly isolate local momentum. The primary statistical risk is how you define the scale weight $w_c$. (e.g., is it just the ratio of city inscriptions to empire inscriptions?). Because this is strictly bound to exploratory case studies and foundation dates, the risk to your confirmatory pipeline is zero.

### 7. Confirmatory Claim Hierarchy & Multiplicity (Q7)
* **The Ask:** Is "no correction, judged independently" defensible?
* **Verdict:** **Yes. Do not apply a Holm/Bonferroni correction.**
* **Reasoning:** Multiple comparison corrections (like Bonferroni or FDR) are required when testing the *same hypothesis* across multiple subsets (fishing for significance), or testing multiple variants of an outcome. You are testing fundamentally orthogonal theoretical questions:
    *   H2.1: Does the model work? (Validation)
    *   H3a: Do counts scale with population? (Scaling)
    *   H3c(i): Do capitals over-produce? (Administrative status)
    *   H3c(ii): Do residuals cluster in space? (Geography)
    *   Because the answers to these questions are independent, an omnibus correction is statistically inappropriate. 

---

### Advice for the Friday Conference Presentation

1. **Own the Date-Window Pivot:** If asked why you don't mixture-correct the city-level regressions (H3a), explicitly state the identifiability problem: *“600 of our 815 cities have N < 100. A per-city Bayesian deconvolution collapses to the prior at that sample size. We protect the cross-sectional data by using a strict 50 BC – AD 350 date-window filter.”* This shows immense methodological maturity.
2. **Lean into the Artefact Diagnosis:** Your discovery that the "century-midpoint spike" was actually a test-statistic artifact, and that wide-interval slabs are the true culprit (Decision 20), is a fantastic narrative beat for a presentation. It shows rigorous data-vetting.
3. **Mundlak Specification:** Emphasize the "Within-Between" split. Archaeologists will immediately intuitively grasp that "cities in different provinces have different epigraphic habits." Showing that you mathematically separated the *local* population effect from the *provincial* baseline will win over skeptics.

You are in fantastic shape to present this. Good luck on Friday!