---
priority: 1
scope: in-stream
title: "OSF Preregistration (open-ended) — Draft"
audience: "Shawn (review + edit), Adela (co-author review), OSF reviewers"
status: draft 2026-04-27 (round-2 forward-fit pivot per Decisions 8–10 applied 2026-04-26; round-2 follow-ups 2026-04-27: §4 Crisis-of-Third-Century exploratory H3b cell + §5 H3a variance-partition exploratory + §6 Crisis row; round-1 5 amendments retained); awaiting Adela review
format: OSF open-ended registration (four fields)
---

# Preregistration draft — Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population

**Format note:** this document is organised to map onto the four fields of an OSF *open-ended registration* (Title; Description; Research Questions / Hypotheses; Additional Information). Fields 1–3 are short; Field 4 carries the detail. `TBD` markers throughout flag decisions awaiting Shawn's input; each is also listed explicitly under §"Open design decisions" below.

---

## Field 1: Title

**Mixture-corrected summed probability analysis of Latin inscriptions against Hanson (2016) urban population: methodological readiness, editorial-convention deconvolution, and population-variance decomposition at city and province scales.**

(Alternative shorter form for the title field if 250-character limit is an issue: *"Mixture-corrected SPAs of Latin inscriptions against Hanson urban population estimates: a preregistered three-phase analysis."*)

---

## Field 2: Description

We preregister a three-phase analysis of the temporal and spatial distribution of Latin inscriptions in the Roman Empire (50 BC – AD 350), using summed probability analysis (SPA) with a novel deconvolution-mixture correction for editorial-convention artefacts. Phase 1 establishes methodological readiness via simulation-based minimum-sample-size thresholds. Phase 2 validates the mixture model against empirically-measured editorial-convention signatures (observed / expected inscription-count ratios of 22.8×, 41.5×, 18.8×, and 39.7× at AD 50 / 150 / 250 / 350 respectively, all Westfall-Young adjusted *p* ≈ 0 in baseline profiling). Phase 3 quantifies the population dimension's footprint on inscription variation via Bayesian negative-binomial regression against Hanson (2016) urban-population estimates, with complementary permutation-envelope deviation-detection and urban-area residual analysis extending Hanson (2021). The paper's primary contribution is methodological; the illustrative substantive finding is a population-variance decomposition at urban and provincial scales.

---

## Field 3: Research Questions and Hypotheses

### Primary research question

What fraction of the temporal and spatial variation in Latin inscription production during the Roman Empire is accounted for by urban population dynamics, after controlling for editorial-convention dating artefacts via a deconvolution-mixture model?

### Secondary research questions

(SR1) Does mixture-corrected SPA at urban and province scales reproduce, at artefact-corrected and decadal resolution, the sublinear inscription-vs-population scaling pattern reported at polity × century resolution by Hanson (2021, β = 0.67 mean) and for elite-honorific subsets by Carleton et al. (2025, β ≈ 0.3–0.5)?

(SR2) Do urban-area residuals from the mixture-corrected regression reproduce Hanson (2021)'s finding that provincial capitals over-produce inscriptions relative to the scaling expectation and that residuals are spatially clustered (Hanson 2021, mean residual 0.43 for provincial capitals vs ~0.06 for *coloniae* / *municipia*; Moran's I = 0.046, *p* < 0.0001)?

### Hypotheses (confirmatory, pre-specified)

**H1 — Methodological readiness (sample-size thresholds).**
H1.1: At empire, province, and urban-area levels, minimum inscription-count thresholds exist at which permutation-envelope SPA reliably detects effects of the magnitude of the Antonine Plague signature reported by Glomb, Kaše & Heřmánková (2022). These thresholds are to be determined by simulation and preregistered *post hoc* of the simulation but *ante hoc* of the substantive analyses H2 and H3.

**H2 — Editorial-convention correction (mixture-model validation).**
H2.1: A deconvolution-mixture model `observed_SPA = α · convention_SPA + (1 − α) · genuine_SPA` fit to LIRE v3.0 recovers α significantly greater than 0 at empire level (i.e., non-trivial editorial-convention mass exists).
H2.2: The mixture-corrected `genuine_SPA` shows century-midpoint observed/expected ratios consistent with a convention-free baseline (target: ratios drop from 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350 to within 1.5× of local neighbourhood means).
H2.3: `genuine_SPA` converges across threshold robustness: Pearson *r* ≥ 0.9 between any two SPAs constructed from subsets filtered by `date_range` ≤ 25, 50, 100, 200, 300 years.
H2.4 (appendix cross-check): stratified-by-convention-class SPA (hard classification: convention-anchored vs precise) recovers a SPA shape agreeing with the mixture-deconvolved `genuine_SPA` within sampling error.

**H3 — Population signal.**
H3a (variance-explained, primary quantitative result): mixture-corrected SPA values at urban-area and province levels correlate with Hanson (2016) urban population estimates, with Bayesian R² ≥ 0.25 at urban-area level and Bayesian R² ≥ 0.50 at province level.
H3b (deviation-detection): mixture-corrected SPAs show permutation-envelope departures matching at least one Decision 5 effect-size target — 50 % sustained deviation over ≥ 50 y, doubling over ≥ 25 y, or 20 % over ≥ 25 y — at one or more preregistered (subset × temporal-window) combinations, Holm-Bonferroni corrected across the family. An **Antonine-specific test at AD 165–180** is preregistered as exploratory replication of Glomb, Kaše & Heřmánková (2022; N = 210 Asclepius-cult inscriptions, KS *p* = 0.20, null) and Duncan-Jones (2018; military diplomas, step-down at AD 167, ~85 % magnitude) — reported against Decision 5 brackets but not pre-committed to a specific effect-size expectation, because the empirical prior is a null at smaller N and an extreme reduction in a material-specific subcorpus.
H3c (urban-area residuals): residuals from the H3a Bayesian NBR reproduce Hanson (2021) patterns: (i) provincial capitals have higher mean residual than non-capitals (one-sided *t*-test on posterior residuals, *p* < 0.05); (ii) residuals are spatially clustered (Moran's I > 0 at *p* < 0.05).

---

## Field 4: Additional Information

### 1. Dataset and corpus

**Primary:** LIRE v3.0 (Kaše, Heřmánková & Sobotková, Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 rows; 63 attributes in the released parquet (the prereg's earlier 65-attribute count conflated derived flags with native columns). The `is_within_RE` and `is_geotemporal` flags referenced in earlier prereg revisions are **derived** at filter time, not native to the released parquet: `is_geotemporal := Lat IS NOT NULL AND Lon IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT NULL AND not_before ≤ not_after` (i.e., a row has a usable geographic and temporal locus); `is_within_RE := province IS NOT NULL` (i.e., a row is geo-located within a Roman province). Filtering with these derived flags plus a 50 BC – AD 350 date-interval intersect yields **180,609 rows** (≈ 98.8 % of the pre-filter total). Derivation rules are consistent with the 2026-04-23 descriptive-stats run (see `runs/2026-04-23-descriptive-stats/decisions.md`). Pre-joined Hanson (2016) urban-population estimates available as the `urban_context_pop_est` attribute at row level (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

**Possible extension:** LIST v1.2 (same team, Zenodo DOI 10.5281/zenodo.10473706, 9 January 2024). 525,870 rows; identical 65-attribute schema. Extends temporal envelope to 50 BC – AD 600 (sparser Late Antique coverage). If LIST swap is ready before paper-sprint Week 1 (by 2026-05-03), analyses extend accordingly; otherwise LIRE envelope remains primary.

**Rome excluded** from all scaling regressions as an extreme outlier, following Hanson (2021, Table 7.3 caption) — methodologically consistent with prior published work.

### 2. Subset levels and sample-size sweep

Subsets analysed at three levels, each with a preregistered minimum-inscription-count threshold (to be fixed after H1 simulation):

- **Empire-wide:** all inscriptions meeting filters; primary level for temporal analyses.
- **Province:** ~50 provinces in LIRE. Threshold candidate values tested by simulation: 100, 250, 500, 1000, 2500, 5000, 10000, 25000 inscriptions.
- **Urban area:** ~816 cities with Hanson population estimates. Threshold candidate values tested by simulation: 25, 50, 100, 250, 500, 1000, 2500 inscriptions.

Date-range filtering thresholds examined for H2 robustness: `date_range` ≤ 25, 50, 100, 200, 300 years (matching 2024 exploratory-notebook sweeps).

### 3. Analysis pipeline

- **Aoristic sampling:** `tempun` (SDAM, MIT licence; Kaše et al., PyPI v0.2.4). Uniform distribution over `[not_before, not_after]` per Decision 4 (primary); trapezoidal (Decision 4 sensitivity) for selected subsets.
- **Binning:** 5-year bins across the envelope (matching the 2024 notebook; reviewer-familiar).
- **SPA construction:** sum of per-inscription probability mass across bins; optional weighting by `letter_count` for the secondary letter-count analyses (see §5 Exploratory).
- **Permutation envelope:** rcarbon-style `modelTest()` algorithm (Crema & Bevan 2021) ported to Python as a hand-rolled Monte Carlo envelope loop following Timpson et al. (2014) directly. **Null fitted in true-date space, not in aoristic-smeared SPA space** (per Decision 8, 2026-04-26): the maximum-likelihood fit treats each row's `[not_before, not_after]` interval as the observation and integrates the parametric density `f(t; θ)` over the interval, `L_i(θ) = ∫_{nb_i}^{na_i} f(t; θ) dt / Z(θ)`. For exponential, this has a closed form; for CPL, per-segment trapezoidal integration. **MC replicates are forward-aoristic-smeared**: synthetic true dates are drawn from the fitted density `f(t; θ̂)`, paired with empirical `[not_before, not_after]` widths drawn from the bootstrap sample, positioned uniformly within the resulting interval, and aoristic-resampled once via uniform draw within the interval. This produces MC SPAs whose variance structure matches the observed SPA pipeline (bootstrap row → aoristic-resample → bin) under the null model. The original prereg's "scipy.stats.permutation_test as the primitive" wording was a domain-port artefact: scipy's primitive is for two-sample exchangeability, not within-SPA envelope tests; the hand-rolled MC envelope is the correct mechanism. The "rcarbon-port without forward-fit" approach (sampling from the smeared-space null fit and re-applying aoristic widths) was attempted in pilot and rejected: it double-smears (the null is already aoristic-smeared because it was fit on smeared data), inflating MC envelope width inappropriately. The forward-fit-in-true-date-space approach corrects this and recovers proper FP control (`runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` §3 confirms FP rates within `[0.007, 0.049]` across all 96 zero-bracket cells). Aoristic resampling is implemented as direct Uniform draws within `[not_before, not_after]` per Decision 4 (mathematically equivalent to the Uniform aoristic method documented in Kaše, Heřmánková & Sobotková's `tempun` package, which we reimplemented directly due to a numpy-2 incompatibility in tempun 0.2.4). Implementation ~600 LOC across `forward_fit.py` + `forward_fit_cpl.py` + `h1_sim_v2.py`. Null models: **exponential (primary, per Timpson et al. 2014)** and **continuous piecewise-linear with k = 3 knots (CPL-3, secondary, per Timpson et al. 2021)**; 1,000 Monte Carlo replicates; two-sided 95 % envelopes. CPL k = 2 was excluded from the primary grid per Decision 9 (validation evidence shows systematic FP = 1.0 bias at high n on a 3-knot truth — structurally underfit). CPL k = 4 is retained as an exploratory upper bound for k-sensitivity per Decision 9 (AIC-best k = 3 in 73 % of CPL iterations on H1 v2 final).
- **Deconvolution-mixture model:** `observed_SPA = α · convention_SPA + (1 − α) · genuine_SPA`. α estimated by maximum-likelihood or mixture-model fit on the convention-vs-precision row classification; `genuine_SPA` recovered by linear deconvolution with non-negativity constraints. `convention_SPA` shape: uniform century slabs per Decision 7 default, OR hierarchical (century > half-century > quarter-century > reign-boundary) if the Obs 11 editorial-convention-hierarchy test (Thursday 2026-04-24) confirms. Defaults to uniform if hierarchy test is inconclusive at 14-boundary sample.
- **Bayesian NBR for H3a:** `log(E[inscriptions_city]) = α_0 + α_province + β · log(population_city) + ε`, with:

  ```text
  y_c ~ NegativeBinomial(mu_c, alpha)
  log(mu_c) = α_0 + α_province[c] + β · log(pop_c)

  Priors (preregistered):
    α_0        ~ Normal(0, 5)         # intercept on log-count scale
    β          ~ Normal(0, 2.5)       # agnostic; wide enough that likelihood dominates
    α_province ~ Normal(0, σ_prov)    # random intercepts
    σ_prov     ~ HalfNormal(1)        # provincial heterogeneity
    1/alpha    ~ HalfNormal(1)        # overdispersion
  ```

  β prior chosen **agnostic** (not centred on the ~0.5 literature value) to avoid any appearance of the preregistration loading the dice toward the sublinear result; with n = 816 cities with Hanson estimates, the likelihood dominates a Normal(0, 2.5) prior comfortably.

  **Primary implementation in `pymc`** (Python; stays in the project venv). **Secondary `brms`-via-R cross-validation shadow** (~50 lines, committed as `scripts/h3a_brms_shadow.R`): refits the same model in R+Stan via brms' formula syntax (`count ~ log_pop + (1|province)`, `family = negbinomial()`), providing (i) cross-language validation that pymc and brms agree on the posterior within MC noise and (ii) legibility for R-native co-authors (Adela Sobotková and others) who read brms syntax more fluently than pymc code. Outputs (posterior draws, summary tables, figures) exchanged as CSV / parquet / PNG — language-neutral. Bayesian R² reported per Gelman, Goodrich, Gabry & Vehtari (2019) via `pymc`-native computation and cross-checked against `brms::bayes_R2()`. Full posterior distributions retained for downstream residual analysis.

  **Brms shadow shape-prior implementation (technical detail).** brms parameterises the negative binomial with `shape = α` (the dispersion parameter directly), not `1/α`. The pymc primary preregisters `inv_alpha = 1/α ~ HalfNormal(1)`. Direct translation `prior(normal(0, 1), class = "shape")` would place the prior on `α` rather than `1/α` — the reverse regularisation direction (toward overdispersed rather than toward Poisson). To match the preregistered prior exactly, the brms shadow uses a `stanvar()` block that places `HalfNormal(1)` on `1/shape` with the appropriate Jacobian:

  ```r
  inv_shape_prior <- stanvar(
    scode = "target += normal_lpdf(1.0 / shape | 0, 1) - 2 * log(shape);",
    block = "model"
  )
  ```

  Jacobian derivation: if `y = 1/x`, then `|dy/dx| = 1/x²`, so the implied prior on `x` in log-density form is `log p_y(1/x) - 2 log(x)`. Stan samples on `shape` (= `x`); the `target` increment realises this transformation. Posterior agreement between pymc and brms is then expected on all quantities including the raw dispersion parameter, not only on μ-scale quantities.

  **Posterior predictive checks (preregistered; routine per Gelman, Vehtari, Simpson, Betancourt et al. 2020 "Bayesian Workflow", arXiv:2011.01808):**

  1. **Density overlay** (`arviz.plot_ppc`): posterior-predictive inscription-count distribution overlaid against the observed count distribution.
  2. **Test statistics** — observed vs posterior-predictive: proportion of zeros (NBR sanity check — triggers zero-inflation consideration if divergent), mean, standard deviation, 95th percentile, mean-variance ratio (dispersion adequacy).
  3. **Residual structure** — standardised Pearson residuals vs fitted values and vs key predictors (`log_pop`, province); looks for remaining structure indicating model mis-specification.

  Any failed check triggers an OSF amendment and model revision before moving to H3b / H3c.
- **Residual analysis (H3c):** per-city residuals extracted from H3a posterior; classified as over-producing, under-producing, or typical (±95 % credible interval from predicted).
- **Spatial clustering (H3c):** Moran's I with row-standardised spatial weights via *k*-nearest-neighbours (`libpysal.weights.KNN.from_dataframe`). **Primary k = 8** (standard practice for point data per Cliff & Ord 1981; robust to the Empire's uneven site density). **Sensitivity at k = 5 and k = 10** reported alongside. Hanson (2021) used ArcGIS's default Spatial Autocorrelation (Global Moran's I) tool (p. 145); the paper does not specify his weights construction, so exact-numerical-match is not feasible. His Moran's I = 0.046 (z = 4.571, *p* < 0.0001 for residuals; I = −0.006, *p* = 0.282 for raw counts, confirming random) is the **qualitative replication target**: we declare H3c spatial-clustering successful if **Moran's I > 0 at *p* < 0.05 in at least two of {k = 5, k = 8, k = 10}** and the qualitative pattern matches Hanson's map (over-production concentrated in Italy and along the Rhine / Danube frontier; under-production scattered in Britannia, Gaul peripheries, and other western edges of the Empire).

### 4. Pre-specified confirmatory analyses

**Phase 1 — H1 min-thresholds simulation protocol (to run first).**

For each combination of (subset level ∈ {empire, province, urban-area}; effect-size target ∈ {Decision 5 a/b/c + zero-effect calibration check}; sample size n ∈ logarithmic sweep):

1. **Generate synthetic intervals from a specified ground-truth null** (Decision 8). For exponential ground truth, draw `n` true dates `t_i ~ Exp(b_null)` truncated to the analysis envelope `[-50, 350]`; for CPL ground truth, draw from the fitted CPL density. Pair each `t_i` with a width `w_i` drawn from the empirical width distribution of filtered LIRE; sample `u_i ~ Uniform(0, 1)`; construct `[nb_i, na_i] = [t_i - u_i · w_i, t_i + (1 - u_i) · w_i]`. This is the synthetic interval list for the iteration.
2. **Aoristic-resample** by drawing `y_i ~ Uniform(nb_i, na_i)` for each row; bin via `np.histogram` on 5-year edges. This is the synthetic SPA.
3. **Inject the effect** at the target magnitude and duration with shape ∈ {step, Gaussian} per the effect-shape pre-specification above (round-1 Amendment 2 in `planning/preregistration-amendments-2026-04-25.md`).
4. **Forward-fit the null** to the synthetic intervals via maximum-likelihood interval-integral (closed-form for exp; per-segment trapezoidal for CPL k = 3 and k = 4); the fit recovers an estimate of `b_null` (or the CPL parameters), not the smeared SPA shape.
5. **Generate `n_mc = 1000` MC replicates** under the fitted null using the same forward-aoristic procedure (synthetic true dates from `f(t; θ̂)`, empirical widths, aoristic-resample), and compute the Timpson 2014 global-p envelope test against the (effect-injected) synthetic SPA. Record detection at *p* < 0.05.
6. Repeat steps 1–5 a total of `n_iter = 1000` times per cell (the preregistered precision; Decision 9). Detection rate per cell = fraction with `p < 0.05`. Wilson 95 % CI on a 0.80 detection rate at `n_iter = 1000` is approximately `[0.775, 0.823]` — adequate for threshold-setting at the 0.80 boundary.

The H1 v1 implementation (2026-04-25, since superseded) deviated from the preregistered protocol by (i) bootstrapping observed_spa from real LIRE rather than simulating from a specified null, and (ii) using `Poisson(fitted_mean)` per bin for MC rather than the forward-aoristic mechanism specified above. Both deviations are documented in `runs/2026-04-25-h1-simulation/outputs/REPORT.md` and Decision 8; the H1 v2 implementation in `runs/2026-04-25-h1-simulation/code/h1_sim_v2.py` honours the preregistered protocol as restated here.

**Detection threshold and the unreachable convention.** The preregistered cell-eligibility criterion is **detection rate ≥ 0.80** at the cell's *n*. Cells where the maximum *n* in the level's sweep gives detection < 0.80 are tagged `min_n_unreachable: True` rather than imputing a fictitious extrapolated threshold. Such cells are out-of-scope for H3 confirmatory testing per the prereg's existing eligibility framework. The `c_20pc_25y` bracket is preregistered as a hard-test boundary anchoring the bottom of the power curve (Decision 10) and is **not in the H3b confirmatory family** — its near-universal unreachability across (level × null × shape × k) cells in H1 v2 final (`runs/.../REPORT-v2-final.md` §2 lists 24 unreachable c_20pc_25y combinations) does not gate confirmatory testing.

**Null model:** both **exponential (primary, per rcarbon / Timpson et al. 2014)** and **continuous piecewise-linear with k = 3 knots (CPL-3, secondary, per Timpson et al. 2021)** fitted; results compared. CPL-3 is fixed a priori rather than AIC-selected per cell, to give a well-defined secondary threshold comparable across subsets and free of per-cell knot-choice edge cases. Rationale: CPL is more flexible than exponential but has more parameters; running both lets us check whether null-model choice materially affects the min-threshold conclusions, and fixed-k keeps the comparison clean.

**Effect shape for injection:** both **step-function (sharp)** and **Gaussian-tapered (smooth)** injected in parallel; thresholds reported as a range per bracket. The step-function is a box-car of bracket magnitude for bracket duration, producing the **lower bound** on n for detection ≥ 0.80 (sharper events are easier to detect). The Gaussian has nadir = bracket magnitude and FWHM = bracket duration, producing the **upper bound** on n (smooth events with this nominal parametrisation are harder to detect via permutation-envelope methods). Reporting both is honest about shape-dependence of thresholds — real events span both shapes (e.g., Antonine Plague is sharp per Duncan-Jones 2018 military-diploma step-down; demographic decline is gradual). Detection rate ≥ 0.80 must be achieved for the **smooth-Gaussian** threshold (the binding, conservative bound) for a (level × bracket) cell to enter H3 confirmatory testing.

Adapts the Carleton, Campbell & Collard (2018, *PLOS ONE* 13:e0191055; code CC-BY) PEWMA power-simulation framework for cross-sectional SPA × covariate analysis.

**Phase 2 — H2 mixture-model validation (after H1 thresholds fixed).**

Run the mixture-model fit on empire-level LIRE. Report α̂ and 95 % CI; report corrected century-midpoint observed/expected ratios; report pairwise Pearson *r* across threshold-filtered `genuine_SPA` variants; report stratified-by-convention-class SPA alongside deconvolved `genuine_SPA`. H2.1–H2.4 criteria as listed in Field 3.

**Phase 3 — H3 substantive analyses.**

- H3a: Bayesian NBR as specified in §3 above. Report β, posterior R² (median + 95 % CI), comparison with OLS log-log (reported alongside as direct comparator to Hanson, Ortman & Lobo 2017).
- H3b: Permutation-envelope SPAs at every preregistered subset × effect-size combination. Holm-Bonferroni correction across the full family. **Antonine-specific test is preregistered as exploratory replication of Glomb, Kaše & Heřmánková (2022) and Duncan-Jones (2018)**: at AD 165–180, test for deviation in mixture-corrected SPA at empire level, at Asclepius-cult subset (replicates Glomb et al.'s design at larger N and on corrected data), and at military-administration subset (replicates Duncan-Jones-style severe-effect prediction), conditional on per-subset sample-size thresholds being met. Results reported against Decision 5 brackets; no specific effect size preregistered for the Antonine test itself. Subset-filtering feasibility depends on LIRE type / category / deity fields — confirmed as part of this preregistration (see §9 Software & data).

  **Crisis-of-the-Third-Century test (exploratory, added 2026-04-27).** A second exploratory replication targeting the **mid-3rd-century inscription decline at AD 235–284** (Duncan-Jones 1996; MacMullen 1982; Mrozek 1973). Unlike the Antonine signature (sharp, ~ 15-year window, single causal event), the Third-Century Crisis is a diffuse, multifaceted ~ 50-year decline driven by overlapping factors (Plague of Cyprian AD 249–262, military instability, monetary collapse, provincial fragmentation). The test window is AD 235–284 (49 years, marginally aligned with the 50 % / ≥ 50 y Decision 5 bracket); reported against Decision 5 brackets but **not pre-committed to a specific effect-size expectation** given the diffuse causal structure. Tested at empire level and at a Western-Empire provincial subset (where the Crisis impact was qualitatively sharpest per the cited literature), conditional on per-subset H1 reachability. Adds a half-century-scale event to complement the Antonine sharp-event replication, broadening the paper's substantive grounding without adding confirmatory family members.
- H3c: Residual classification + Moran's I + provincial-capital *t*-test as listed in H3.

### 5. Exploratory analyses (explicitly flagged as non-confirmatory)

- **CPL knot-sensitivity analysis (exploratory, H1).** For each CPL cell in the H1 simulation, fits k ∈ {2, 3, 4} and records AIC + detection per k. Reports threshold at each fixed k and the max−min range as a diagnostic for "does CPL threshold depend on knot count?" Non-confirmatory; reported in the paper's supplementary material.
- **CPL AIC-select threshold (exploratory, H1).** Per-iteration picks k with minimum AIC from {2, 3, 4}; reconstructs threshold under AIC-select decision rule (cf. Timpson et al. 2021). Answers "what would AIC-selected CPL have given?" without re-simulation. Non-confirmatory.
- **Stratified-sampling sensitivity (exploratory, H1).** Primary H1 thresholds use bootstrap (sampling-with-replacement) from filtered LIRE. Post-hoc, thresholds are recomputed using stratified-sampling (province-proportional or city-proportional draws) from the same persisted per-iteration parquet. Reports deltas to bootstrap primary; tests whether empirical province / city mix matters for detection power at given n. Non-confirmatory.
- **Variance partition for H3a (exploratory, added 2026-04-27).** From the fitted Bayesian NBR posterior, decompose total variance in `log(E[inscriptions_city])` into three components: (i) `Var(β · log_pop_city)` — the population-scaling contribution; (ii) `Var(α_province)` — province-level "everything else" (economic, infrastructural, cultural variation absorbed into the random intercepts); (iii) negative-binomial residual variance — city-level "everything else" (local cultural conditions, micro-economy, patronage, prestige factors). Report each as a proportion of total variance with 95 % credible intervals (per Gelman, Hill & Yajima 2014 hierarchical variance partitioning). **No pre-committed numerical target** — the partition is hypothesis-generating, intended to characterise population's footprint relative to higher-order factors that this analysis cannot separately identify (per §10 limitations on identifiability of complexity dimensions). Sanity-check: total variance explained by the fixed + random effects should be consistent with the H3a Bayesian R² confirmatory targets within posterior uncertainty. Pre-specified interpretation framework: if `Var(β · log_pop) / Var(total) < 0.50`, this is consistent with substantial role for higher-order factors absorbed into province REs and residual; if ≥ 0.50, population is the dominant identified driver. The 0.50 threshold is for narrative framing only, not a confirmatory criterion.
- **Stratified-by-convention-class SPA** as alternative to the mixture (appendix cross-check on H2; already in the H2.4 structure but reported separately for transparency).
- **`baorista` Bayesian aoristic comparison** (Crema 2025) on representative provincial subsets if compilable on sapphire (R + NIMBLE + C++); demoted to citation-with-rationale if install fails (per Decision 3 fallback).
- **Scaling-residual sensitivity analysis for H3a:** compute per-city residuals from a fitted power-law `inscriptions ∝ population^β`; re-run H3a on residuals. Tests whether the Hanson-population correlation survives scaling-controlled analysis.
- **α-as-translator sensitivity analysis for H3a:** include per-city mixture α as an additional covariate in the NBR; test whether β_pop estimate shifts meaningfully. Informs whether the Hanson correlation is confounded by epigraphic-habit intensity (variable across regions).
- **Chronological resolution of H3c urban-area residuals:** extend Hanson's (2021) time-pooled residual analysis by computing residuals per decadal period. Exploratory because no published comparator exists.
- **Information-infrastructure vs complexity-markers theoretical framing:** both presented in the paper; audience response at RAC-TRAC 2026 informs which carries into the journal version.
- **Letter-count alternative analysis:** per subset, repeat H3 using summed letter counts instead of inscription counts. Inherits the 2024 notebook's observation that letter count and inscription count are nearly equivalent population predictors but with letter count showing higher-variance Negative Binomial pseudo-R² (suspected artefact of dispersion structure; Shawn flagged "too good to be true" in the archived notes).

### 6. Effect-size pre-specifications (summary)

| Hypothesis | Quantity | Preregistered target |
|---|---|---|
| H1 power floor | Detection rate | ≥ 0.80 at *p* < 0.05 per Decision 5 bracket; zero-effect false-positive rate ≤ 0.05 (achieved across all 96 v2-final zero cells, range `[0.007, 0.049]`). |
| H1 binding thresholds (50 % / ≥ 50 y, primary) | min n at detection ≥ 0.80 | **province** exp-step 1938, exp-gauss 1869, cpl-3-step 1385, cpl-3-gauss 1618; **urban-area** exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549; **empire** reachable at n = 50 000 (calibration). H1 v2 final 2026-04-26. |
| H1 b_double_25y thresholds | min n at detection ≥ 0.80 | Gaussian shape: empire reachable at n = 50 000; province exp 2118, cpl-3 1934; urban-area exp 2160, cpl-3 1905. **Step shape unreachable across all levels** (mass spread evenly across 5 bins; SNR per bin marginal). |
| H1 c_20pc_25y thresholds (hard-test boundary, Decision 10) | min n at detection ≥ 0.80 | Empire/cpl-3/gaussian reachable at n = 50 000 (single marginal-reachable cell); **all other (level × null × shape × k) combinations unreachable**. Bracket retained in H1 as honest-uncertainty anchor; **not in H3b confirmatory family**. |
| H2.1 | α̂ | Posterior CI excludes 0; point estimate > 0.1 |
| H2.2 | Corrected century-midpoint O/E | Within 1.5× of local neighbourhood mean |
| H2.3 | Pairwise Pearson *r* across threshold variants | ≥ 0.9 |
| H3a urban-area | Bayesian R² | ≥ 0.25 (anchored on Hanson, Ortman & Lobo 2017 R² = 0.267) |
| H3a province | Bayesian R² | ≥ 0.50 (Palmisano et al. 2021 upper empirical range) |
| H3b primary | Antonine signature | ≥ 50 % dip sustained ≥ 50 y at AD 165–180 |
| H3b secondary | Other targets | Decision 5 a/b effect-sizes (c retired per Decision 10), Holm-Bonferroni corrected over remaining-eligible (level × bracket × shape) cells per H1 v2 reachability map. |
| H3b exploratory | Crisis of Third Century | AD 235–284 window (49 y); reported against Decision 5 brackets; magnitude **not** pre-committed (diffuse causal structure). Empire + Western-Empire-provincial subset, conditional on H1 reachability. Replication targets: Duncan-Jones 1996, MacMullen 1982, Mrozek 1973. |
| H3c provincial-capital | Mean residual difference | One-sided *t*-test *p* < 0.05 |
| H3c spatial clustering | Moran's I | > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} k-NN weights; qualitative pattern matches Hanson (2021) map |

### 7. Planned deviations and contingencies

- **If H1 reveals insufficient data density at a given subset level,** H2 and H3 analyses at that level are dropped from confirmatory testing and (optionally) retained in the paper as exploratory.
- **If Obs 11 editorial-convention-hierarchy test confirms** (Thursday 2026-04-24), `convention_SPA` shape in the mixture shifts from uniform century slabs to weighted hierarchical. If inconclusive, default uniform is retained per Decision 7.
- **If `baorista` compilation fails on sapphire,** the Bayesian-aoristic comparison demotes from appendix figure to citation-with-rationale (per Decision 3 fallback).
- **If LIST swap completes before paper-sprint Week 1,** analytical envelope extends to AD 600 and Late Antique subsets are added; otherwise LIRE envelope remains.
- **If Adela requests substantive methodology changes during co-author review,** an amendment to this preregistration is filed on OSF before implementation.

### 8. Open design decisions (TBD markers — resolve before submission)

- ~~Final preregistered sample-size thresholds from the H1 simulation~~ **Resolved 2026-04-26 (H1 v2 final):** binding 50%/50y thresholds tabled in §6; b_double_25y/step unreachable at all levels; c_20pc_25y operationally restricted (Decision 10). FP-rate target ≤ 0.05 achieved across all 96 v2-final zero-bracket cells (range [0.007, 0.049]). Full threshold map at `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` and `thresholds.parquet`.
- ~~Bayesian-NBR software choice~~ **Resolved 2026-04-24:** primary `pymc`; secondary `brms`-via-R shadow (~50-line script) for the H3a model only, as cross-validation + R-team legibility. Carleton et al. 2025's provincial posterior effects consumed as data, not code.
- ~~Exact priors on α_0, α_province, β, dispersion~~ **Resolved 2026-04-24:** `α_0 ~ Normal(0, 5)`; `β ~ Normal(0, 2.5)` (agnostic); `σ_prov ~ HalfNormal(1)`; `1/alpha ~ HalfNormal(1)`. PPC suite: density overlay + test statistics (zero-count, mean, SD, 95th, M/V ratio) + Pearson-residual structure. Adela amendment path preserved: any substantive revision of priors or PPCs triggers an OSF amendment before execution.
- ~~Spatial-weights construction for Moran's I~~ **Resolved 2026-04-24:** k-NN k = 8 primary (row-standardised, `libpysal.weights.KNN`), k = 5 and k = 10 as sensitivity; three-way pattern (≥ 2 of 3 significant + qualitative Hanson-map match) is the H3c spatial-clustering success criterion. Hanson 2021 weights construction is unspecified in his paper (ArcGIS default), so exact-numerical-match is not feasible and not attempted.
- ~~Multiple-comparison family for H3b: exact Holm-Bonferroni family after H1 fixes the subset × effect-size grid.~~ **Resolved 2026-04-26:** Holm-Bonferroni correction applied across the H1-reachable (level × null × bracket × shape) cells. Family excludes `c_20pc_25y` (Decision 10) and step-shape `b_double_25y` at all levels (unreachable). Reachable confirmatory cells: 2 levels (province, urban-area) × 2 nulls (exp, cpl-3) × 3 reachable bracket-shape combinations (`a_50pc_50y / step`, `a_50pc_50y / gaussian`, `b_double_25y / gaussian`) = **12 cells**. If exp and cpl-3 are reported as primary-plus-sensitivity rather than independent confirmatory tests, the corrected family collapses to 6 cells (one null per cell). The single null × multiple-comparison commitment is locked when the H3 results parquet is built; preregistered options are: (a) treat exp and cpl-3 as separate confirmatory hypotheses (Holm across 12); (b) treat cpl-3 primary, exp as sensitivity (Holm across 6).
- Decision-log reference for the target venue (JAMT methods-heavy vs JAS balanced) — committed at end of Week 1 paper sprint (2026-05-03) per Decision 7.

**Additional items resolved 2026-04-26 (forward-fit pivot, Decisions 8–10):**

- **MC mechanism**: forward-fit in true-date space (per row interval-likelihood maximisation) + forward-aoristic MC (synthetic true dates → empirical widths → aoristic-resample-once). Documented in §3 and Decision 8. Supersedes Poisson-on-fit MC of v1.
- **CPL k**: k = 3 primary; k = 4 exploratory upper bound; k = 2 excluded from primary grid (validation evidence: k = 2 systematically underfit at high n on a 3-knot truth, per Decision 9).
- **H1 simulation framework**: synthetic-data-from-specified-null DGP (per §4 Phase 1 above). Supersedes the v1 bootstrap-from-LIRE deviation.
- **`c_20pc_25y` disposition**: preregistered hard-test boundary in H1; retired from H3b confirmatory family (Decision 10).

### 9. Software, reproducibility, and data access

- **Language:** Python 3.13 (primary); R if `brms` is preferred for Bayesian NBR.
- **Environment:** `uv`-managed venv at `~/Code/inscriptions/.venv/`; `requirements.txt` pinned.
- **Core dependencies (Python):** `numpy`, `scipy`, `pandas`, `pyarrow`, `matplotlib`, `joblib`, `pymc` (primary Bayesian NBR for H3a), `pyzotero`, `requests`, `python-dotenv`, `statsmodels`.
- **Aoristic resampling implementation note:** the Uniform aoristic method (per Decision 4) is implemented directly in `primitives.py::aoristic_resample` as ≤ 10 LOC of numpy. We did not use Kaše, Heřmánková & Sobotková's `tempun` package (SDAM, MIT; PyPI v0.2.4) because its current release is incompatible with numpy ≥ 2.4 (uses the removed `numpy.trapz`). The substitution is mathematically equivalent under the Uniform aoristic distribution. Upstream issue filed to `sdam-au/tempun` (this repo issue #4); once tempun is numpy-2-compatible, we may reintroduce it for H2 / H3 pipelines where the package offers additional conveniences beyond Uniform aoristic.
- **Secondary dependencies (R; shadow validation only):** `R ≥ 4.3`, `rstan`, `brms` — installed on sapphire for the H3a cross-check run; not on the critical path for reproducing the paper's primary results.
- **Data:** LIRE v3.0 (Zenodo DOI 10.5281/zenodo.8147298; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) as ground-truth cross-check for `urban_context_pop_est`.
- **Subset-filter feasibility (confirmed 2026-04-24 on LIRE v3.0).** Military-administration subset: `type_of_inscription_clean == 'military diploma'` yields 285 rows (66.4 % null in that field; the ML-classified `type_of_inscription_auto` yields 442 rows at 13.8 % null and is a valid alternative). Asclepius-cult subset: regex `[Aa]esculap|[Aa]sclep` on the `inscription` free-text field yields 358 rows — substantially above Glomb, Kaše & Heřmánková's (2022) N = 210, suggesting their filter was stricter. The preregistered Glomb-replication test will either adopt their exact filter (if recoverable from their Methods) or use the broader keyword match and report both N values.
- **Code:** repository at `github.com/TBD` (Shawn to create public mirror before submission).
- **Run artefacts:** per-stage `runs/<YYYY-MM-DD>-<description>/` directories, capturing spec, briefs, seed, code, outputs, decisions (project convention established 2026-04-23).
- **Research record:** agent-session-capture infrastructure operational (2026-04-24; captured in project memory). Individual AI-agent prompts and outputs preserved per open-science requirements.

### 10. Known limitations (preregistered)

- **Editorial-convention artefact identification.** The mixture model addresses century-midpoint spikes directly. Other documented LIST/LIRE artefacts — reign-boundary clustering, province-label anachronism (Heřmánková, Kaše & Sobotková 2021, §48; EDH anchors province labels to mid-2nd-century Roman geography), EDCS coordinate imprecision (§60; 7-decimal false precision on hundreds-of-metres real accuracy), 50 % missing coordinate provenance (§45) — remain as interpretive caveats. The preregistration commits to transparent reporting of these, not to methodological correction.
- **Single-dimension complexity (Turchin et al. 2018).** The multi-factor complexity decomposition in the paper's theoretical frame operates at city / province × decadal scale; Turchin's "single latent dimension" operates at polity × century scale. Different scales; the paper acknowledges but does not attempt empirical disaggregation of the non-population dimensions. See `docs/notes/reflections/working-notes.md` Obs 12.
- **Rome-exclusion.** Rome is excluded from scaling regressions as an extreme outlier. Consistent with Hanson (2021) methodology; reported transparently; not tested as a sensitivity.
- **Identifiability of complexity dimensions.** With inscription count as the sole observable and Hanson population as the sole external covariate, dimensions 2–6 of the complexity decomposition (economic prosperity, social differentiation, cultural translator, ideology, residual) remain theoretically present but empirically entangled. The paper acknowledges this as scope limitation; disaggregation is future work (FS-A through FS-G in `planning/research-intent.md`).
- **Chronological envelope.** 50 BC – AD 350 (LIRE); extensible to AD 600 conditional on LIST swap. Late Antique and post-AD-600 phenomena out of scope for this paper.

### 11. Hypothesis-level structure summary

```text
Phase 1 (simulation) → Phase 2 (LIRE) → Phase 3 (LIRE)
     H1                  H2.1 – H2.4        H3a variance-explained (primary)
 min-thresholds       mixture validation   H3b deviation-detection
                                            H3c urban residuals
```

### 12. Provenance

- **Preregistration drafted:** 2026-04-24 by Claude Code (Anthropic, Opus 4.7) under Shawn Ross's direction.
- **Authors and roles:** Shawn Ross (PI, Macquarie University) — research question, theoretical framing, substantive interpretation, scope decisions. Adela Sobotková (Aarhus SDAM) — co-author, methodology review, epigraphic-domain expertise, SDAM corpus familiarity.
- **AI contributions:** theoretical-frame refinements (identifiability scope, scaling-residual sensitivity flag, translator-confound strategy), deconvolution-mixture model articulation (attributed in `planning/ai-contributions.md`), this preregistration draft. All substantive intellectual contributions logged.
- **Reference documents:**
  - `planning/research-intent.md` — paper-level intent; this preregistration operationalises it.
  - `planning/decision-log.md` — 7 architecture decision records (ADRs).
  - `planning/archive-2024-summary.md` — 2024 exploratory work; source of sample-size and threshold starting points.
  - `runs/2026-04-23-prior-art-scouts/synthesis.md` — effect-size calibration, scaling-law resolution, translator-proxy strategy.
  - `docs/notes/reflections/working-notes.md` — numbered observations including Obs 7 (data-quality artefacts), Obs 11 (editorial-convention hierarchy hypothesis), Obs 12 (Turchin 2018 scale mismatch).
- **Funding, ethics, competing interests:** to be completed by Shawn before OSF submission.
- **Target conference:** RAC-TRAC 2026 (Roman Archaeology Conference / Theoretical Roman Archaeology Conference), May 2026 — venue confirmed; abstract deadline TBD. Zotero subcollection `RAC-TRAC-2026` (key `U2V6V6YD`, SDAM group 2366083) tracks citations as drafting progresses.
- **Target journal venue:** JAMT (methods-heavy) or JAS (balanced), final scope commitment at Week-1 sprint checkpoint 2026-05-03 per Decision 7.
- **Round-2 amendments applied 2026-04-26.** Forward-fit nulls in true-date space (Decision 8); CPL k = 2 dropped from primary grid (Decision 9); `c_20pc_25y` retained as preregistered hard-test boundary, retired from H3b confirmatory family (Decision 10). H1 v2 final results (`runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`, commit `00aceb4`) provide the resolved numerical thresholds and FP-rate validation. Decision-log entries 8–10 carry the rationale; `planning/prior-art-scout-2026-04-25-aoristic-envelope.md` (with §8 empirical addendum) carries the literature scan and the why-Option-A-failed analysis.

---

## Review pointers for Shawn

- **Tone and depth:** aimed at OSF open-ended registration standards — discursive where helpful, concise where possible. Compare to your map-reader-llm prereg and push back if this is over- or under-specified for the format you want.
- **Preregistered claims vs exploratory:** §4 (confirmatory) and §5 (exploratory) are the core boundary. Moving items between them materially changes what the preregistration binds you to.
- **TBD markers:** 6 explicit items in §8 need your input before OSF submission.
- **Effect-size anchors:** §6 summary table collects all preregistered thresholds. If any feel too ambitious or too lax, that's the place to push.
- **Limitations:** §10 is written to be honest-sooner-rather-than-later; reviewers will read it.
- **Adela review step:** not scheduled in this draft; recommend it before OSF submission. Diff this draft against her expectations; file any amendments on OSF after initial registration if substantive changes arise.
- **Next mechanical steps after your edit pass:** (i) run H1 simulation, (ii) fix the TBD thresholds, (iii) Adela review, (iv) submit on OSF, (v) execute H2 + H3.
