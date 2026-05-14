---
title: "OSF Preregistration — Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population"
format: OSF open-ended registration (four fields)
status: draft for lodgement (2026-05-14)
---

# Preregistration — Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population

**Format note:** this document is organised to map onto the four fields of an OSF *open-ended registration* (Title; Description; Research Questions / Hypotheses; Additional Information). Fields 1–3 are short; Field 4 carries the detail.

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
H1.1: At empire, province, and urban-area levels, minimum inscription-count thresholds exist at which permutation-envelope SPA reliably detects effects of the magnitude of the Antonine Plague signature reported by Glomb, Kaše & Heřmánková (2022). These thresholds were determined by the Phase 1 simulation, which is complete; the resulting thresholds are fixed in §6. Phase 1 was executed and its thresholds locked before any Phase 2 (H2) or Phase 3 (H3) analysis — that is, *post hoc* of the simulation but *ante hoc* of the substantive analyses.

**H2 — Editorial-convention correction (mixture-model validation).**
H2.1: A deconvolution-mixture model `observed_SPA = α · convention_SPA + (1 − α) · genuine_SPA` fit to LIRE v3.0 recovers α significantly greater than 0 at empire level (i.e., non-trivial editorial-convention mass exists).
H2.2: The mixture-corrected `genuine_SPA` shows century-midpoint observed/expected ratios consistent with a convention-free baseline (target: ratios drop from 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350 to within 1.5× of local neighbourhood means).
H2.3: `genuine_SPA` converges across threshold robustness: Pearson *r* ≥ 0.9 between any two SPAs constructed from subsets filtered by `date_range` ≤ 25, 50, 100, 200, 300 years.
H2.4 (appendix cross-check): stratified-by-convention-class SPA (hard classification: convention-anchored vs precise) recovers a SPA shape agreeing with the mixture-deconvolved `genuine_SPA` within sampling error.

**H3 — Population signal.**
H3a (variance-explained, primary quantitative result): mixture-corrected SPA values at urban-area and province levels correlate with Hanson (2016) urban population estimates, with Bayesian R² ≥ 0.25 at urban-area level and Bayesian R² ≥ 0.50 at province level.
H3b (deviation-detection): mixture-corrected SPAs show permutation-envelope departures matching at least one preregistered effect-size bracket — 50 % sustained deviation over ≥ 50 y, doubling over ≥ 25 y, or 20 % over ≥ 25 y — at one or more preregistered (subset × temporal-window) combinations, Holm-Bonferroni corrected across the family. An **Antonine-specific test at AD 165–180** is preregistered as exploratory replication of Glomb, Kaše & Heřmánková (2022; N = 210 Asclepius-cult inscriptions, KS *p* = 0.20, null) and Duncan-Jones (2018; military diplomas, step-down at AD 167, ~85 % magnitude) — reported against the preregistered effect-size brackets but not pre-committed to a specific effect-size expectation, because the empirical prior is a null at smaller N and an extreme reduction in a material-specific subcorpus.
H3c (urban-area residuals): residuals from the H3a Bayesian NBR reproduce Hanson (2021) patterns: (i) provincial capitals have higher mean residual than non-capitals (one-sided *t*-test on posterior residuals, *p* < 0.05); (ii) residuals are spatially clustered (Moran's I > 0 at *p* < 0.05).

---

## Field 4: Additional Information

### 1. Dataset and corpus

**Primary:** LIRE v3.0 (Kaše, Heřmánková & Sobotková, Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 rows; 63 attributes in the released parquet. Two filter flags used below — `is_within_RE` and `is_geotemporal` — are **derived** at filter time rather than being native columns of the released parquet: `is_geotemporal := Lat IS NOT NULL AND Lon IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT NULL AND not_before ≤ not_after` (the row has a usable geographic and temporal locus); `is_within_RE := province IS NOT NULL` (the row is geo-located within a Roman province). Filtering with these derived flags plus a 50 BC – AD 350 date-interval intersect (overlap, not containment) yields **180,609 rows** (≈ 98.8 % of the pre-filter total). Pre-joined Hanson (2016) urban-population estimates are available as the `urban_context_pop_est` attribute at row level (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

**Possible extension:** LIST v1.2 (same team, Zenodo DOI 10.5281/zenodo.10473706, 9 January 2024). 525,870 rows; the same released schema as LIRE. Extends the temporal envelope to 50 BC – AD 600 (sparser Late Antique coverage). If the LIST swap is ready during the fortnightly paper sprint (11–24 May 2026), analyses extend accordingly; otherwise the LIRE envelope remains primary.

**Rome excluded** from all scaling regressions as an extreme outlier, following Hanson (2021, Table 7.3 caption) — methodologically consistent with prior published work. Rome alone contributes **65,435 inscriptions** to the filtered corpus: 36.2 % of the 180,609-row total, or 46.5 % of the 140,575 inscriptions assigned to a Hanson-catalogued city. The Rome-excluded corpus is therefore **115,174 inscriptions**. Excluding Rome removes a single data point that would otherwise dominate the scaling fit; the exclusion is reported transparently and is not tested as a sensitivity (see §9).

### 2. Subset levels and sample-size sweep

Subsets analysed at three levels, each with a preregistered minimum-inscription-count threshold (fixed by the completed Phase 1 simulation; see §6):

- **Empire-wide:** all inscriptions meeting filters; primary level for temporal analyses (Rome excluded).
- **Province:** ~50 provinces in LIRE. Threshold candidate values tested by simulation: 100, 250, 500, 1000, 2500, 5000, 10000, 25000 inscriptions.
- **Urban area:** ~816 cities with Hanson population estimates. Threshold candidate values tested by simulation: 25, 50, 100, 250, 500, 1000, 2500 inscriptions.

Date-range filtering thresholds examined for H2 robustness: `date_range` ≤ 25, 50, 100, 200, 300 years (matching the 2024 exploratory-notebook sweeps).

### Analysis pipeline — a plain-English walkthrough

*This subsection explains the analysis in plain terms, for readers — including non-statistician archaeologists — who want the intuition before the technical detail. It is explanatory only: §3 below is the binding technical specification, and where the two appear to differ, §3 governs.*

**The problem.** Every Latin inscription in the corpus carries a *date range* — an earliest and a latest plausible year — rather than an exact date. We want to know two things: how inscription production rose and fell over time, and how far that pattern is driven by the size of the cities producing the inscriptions. Two obstacles stand in the way. First, the dates are uncertain. Second, the dates are *systematically distorted*: epigraphic editors, faced with a vaguely datable inscription, tend to record it at a round century-midpoint (AD 50, 150, 250, or 350), which creates artificial spikes that are an artefact of editorial habit rather than a feature of the ancient world.

**Step 1 — from date ranges to a production curve (aoristic sampling and the SPA).** "Aoristic" analysis handles date uncertainty by spreading each inscription's "weight" across its possible date range instead of pretending it has a single true date. Summing that spread weight across every inscription, year by year, produces a *summed probability analysis* (SPA) — a curve estimating how much inscription production happened in each period. This curve is the basic object that every later step works on.

**Step 2 — removing the editorial artefact (the deconvolution-mixture model).** The SPA we observe is a blend: part of it is genuine ancient signal, part of it is the century-midpoint editorial artefact. The mixture model formalises this as `observed = α × convention pattern + (1 − α) × genuine pattern`. It estimates `α` — the share of the curve attributable to editorial convention — from the data, then recovers the genuine pattern by subtracting the convention component out. This deconvolution is the paper's central methodological contribution.

**Step 3 — telling signal from noise (the permutation envelope).** Even a corrected curve wiggles. To decide whether a given wiggle is a real historical event or just noise, we build a "what noise alone looks like" band: we simulate many artificial datasets under a deliberately featureless model (smooth growth or decline, no special events), measure how much *those* curves wiggle, and check whether the real curve pokes outside the resulting band. Poking outside it indicates a deviation unlikely to be chance. One technical subtlety matters here — the "forward-fit" approach: the featureless model is fitted to the *true underlying dates*, and the date-range uncertainty is then re-applied to the simulated datasets, so the artificial curves carry the same uncertainty structure as the real one. A more naive approach applied that uncertainty smearing twice over, which made the noise band artificially narrow and produced false alarms; the forward-fit approach corrects this.

**Step 4 — establishing what the method can detect (H1, Phase 1, now complete).** None of the above is worth running on a corpus too small for the method to see anything. So before the substantive work, we simulated: at each analysis level (whole empire, individual province, individual city), and for events of several sizes, how large does the corpus need to be before the method reliably detects the event? Those simulations are complete; they fix the minimum inscription counts (§6) below which an analysis level is not eligible for confirmatory testing.

**Step 5 — the population question (H3a, Bayesian negative-binomial regression).** With a corrected signal in hand, we ask how far city population explains inscription production. The regression is *negative-binomial* because inscription counts are far more variable than a simple count model would predict (they are over-dispersed), and *Bayesian* because that yields a full distribution of plausible values for every quantity of interest — which is also where the analysis's uncertainty intervals come from (see "Uncertainty quantification" below). Province-level "random intercepts" absorb the systematic differences between provinces, so that the population effect is estimated cleanly.

**Step 6 — which cities break the pattern, and where (H3c, residuals and spatial clustering).** Finally, we look at the cities the regression gets *wrong* — those producing markedly more or fewer inscriptions than their population predicts (the residuals) — and ask whether the over- and under-producers cluster geographically (a spatial-autocorrelation statistic, Moran's I). This reproduces and extends Hanson's (2021) finding that provincial capitals over-produce inscriptions and that the pattern is spatially structured.

**How the phases connect.** The three phases gate one another: Phase 1 (H1) establishes that the method *can* detect events at a given corpus size; Phase 2 (H2) *cleans* the signal of the editorial artefact; Phase 3 (H3) asks what the cleaned signal says about population. Each phase must succeed on its own terms before the next is interpretable.

### 3. Analysis pipeline

- **Aoristic sampling:** the Uniform aoristic method — each inscription's probability mass spread uniformly over `[not_before, not_after]` — is the primary treatment; a trapezoidal distribution (mid-interval more probable than the interval edges) is run as a sensitivity analysis on selected subsets (the full-empire SPA and a small number of representative province and city SPAs). The Uniform method is implemented directly in the project code (≤ 10 lines of numpy) rather than via the SDAM `tempun` package, whose current release (0.2.4) is incompatible with numpy ≥ 2.4; the direct implementation is mathematically equivalent to `tempun`'s Uniform aoristic method.
- **Binning:** 5-year bins across the analysis envelope (matching the 2024 exploratory notebook; reviewer-familiar).
- **SPA construction:** sum of per-inscription probability mass across bins; optional weighting by conservative letter count for the secondary letter-count analyses (see §5 Exploratory).
- **Permutation envelope:** an rcarbon-style `modelTest()` significance test (Crema & Bevan 2021), implemented in Python as a hand-rolled Monte Carlo envelope loop following Timpson et al. (2014). The loop samples Monte Carlo replicates from a fitted parametric null, computes a pointwise 95 % envelope, and evaluates a global *p*-value as the proportion of replicates with at least as many bins falling outside the pointwise envelope as the observed SPA. Two design choices are central:

  **The null is fitted in true-date space, not in aoristic-smeared SPA space.** The maximum-likelihood fit treats each row's `[not_before, not_after]` interval as the observation and integrates the parametric density `f(t; θ)` over the interval: `L_i(θ) = ∫_{nb_i}^{na_i} f(t; θ) dt / Z(θ)`. For the exponential null this has a closed form; for the CPL null it is per-segment trapezoidal integration. Fitting in true-date space means the date-range uncertainty is *not* absorbed into the fitted null.

  **Monte Carlo replicates are forward-aoristic-smeared.** Synthetic true dates are drawn from the fitted density `f(t; θ̂)`, paired with empirical `[not_before, not_after]` widths drawn from the bootstrap sample, positioned uniformly within the resulting interval, and aoristic-resampled once by a uniform draw within the interval. This produces Monte Carlo SPAs whose variance structure matches the observed SPA pipeline (bootstrap row → aoristic-resample → bin) under the null model. An alternative that fits the null on the already-smeared observed SPA and then re-applies aoristic widths was tested and rejected: it smears the uncertainty twice over (the fitted null is already smeared, because it was fit on smeared data), which inflates the Monte Carlo envelope width and the false-positive rate. The forward-fit-in-true-date-space approach corrects this and recovers proper false-positive control — false-positive rates fall within `[0.007, 0.049]` across all 96 zero-effect calibration cells of the completed Phase 1 simulation.

  Null models: **exponential** (primary, per Timpson et al. 2014) and **continuous piecewise-linear with k = 3 knots** (CPL-3, secondary, per Timpson et al. 2021); 1,000 Monte Carlo replicates; two-sided 95 % envelopes. CPL with k = 2 knots was tested in validation and excluded from the primary grid: it shows a systematic false-positive bias (rates approaching 1.0) at high n on a 3-knot ground truth, because k = 2 is too inflexible to represent the empirical shape of the corpus — it is structurally underfit. CPL with k = 4 knots is retained as an exploratory upper bound for knot-count sensitivity (k = 3 is AIC-best in 73 % of CPL iterations in the completed Phase 1 simulation).
- **Deconvolution-mixture model:** `observed_SPA = α · convention_SPA + (1 − α) · genuine_SPA`. `α` is estimated by maximum-likelihood (or mixture-model) fit on the convention-versus-precision row classification; `genuine_SPA` is recovered by linear deconvolution with non-negativity constraints. The `convention_SPA` shape is uniform century slabs by default; it shifts to a weighted hierarchical shape (century > half-century > quarter-century > reign-boundary) only if the editorial-convention-hierarchy test confirms that hierarchy on a 14-boundary sample. If that test is inconclusive, the uniform default is retained (see §7).
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

### Uncertainty quantification

Every quantity this preregistration commits to is reported with an interval. Because the analyses span frequentist simulation, frequentist model fitting, and Bayesian inference, the interval *type* differs by analysis — there is no single confidence-interval recipe that fits all of them. In particular, the nonparametric bootstrap intervals used in the 2024 exploratory work do not transfer to the Bayesian components, where the posterior distribution is itself the uncertainty representation. The mapping is preregistered as follows:

| Analysis | Quantity | Interval method |
|---|---|---|
| H1 (Phase 1) | Detection rate per cell | Wilson score 95 % interval on the proportion of simulation iterations with *p* < 0.05 (n_iter = 1,000). |
| Permutation envelope (H1, H3b) | The envelope itself | The 2.5th / 97.5th percentiles of the Monte Carlo replicate distribution, per bin (pointwise 95 % envelope); significance via the Timpson et al. (2014) global *p*-value. The envelope *is* the uncertainty representation — no separate interval is computed. |
| H2 | Mixture weight α̂ | Nonparametric bootstrap: inscription rows resampled with replacement, the mixture refit on each resample, 95 % percentile interval over α̂. This is the one component where a classic nonparametric bootstrap is the natural method. |
| H2.3 | Pairwise Pearson *r* across threshold-filtered SPAs | Nonparametric bootstrap percentile interval (rows resampled with replacement). |
| H3a | β, Bayesian R², variance-partition components | Posterior 95 % credible intervals, computed directly from the fitted posterior. Bootstrap is *not* used: the posterior distribution already represents the full uncertainty, and resampling a Bayesian fit would double-count it. |
| H3c | Per-city residuals | Posterior 95 % credible intervals, propagated from the H3a posterior. |
| H3c | Moran's I | Conditional permutation inference (999 permutations of residuals over fixed spatial weights) — the field-standard significance procedure for Moran's I — reported for each of k = 5, 8, 10. |

Where an interval excludes (or includes) a preregistered threshold, that is the basis on which the corresponding hypothesis is judged supported or not.

### 4. Pre-specified confirmatory analyses

**Phase 1 — H1 min-thresholds simulation protocol (completed; protocol as executed).**

For each combination of (subset level ∈ {empire, province, urban-area}; effect-size bracket ∈ {the three preregistered brackets — 50 %/≥50 y, doubling/≥25 y, 20 %/≥25 y — plus a zero-effect calibration check}; sample size n ∈ logarithmic sweep):

1. **Generate synthetic intervals from a specified ground-truth null.** For exponential ground truth, draw `n` true dates `t_i ~ Exp(b_null)` truncated to the analysis envelope `[-50, 350]`; for CPL ground truth, draw from the fitted CPL density. Pair each `t_i` with a width `w_i` drawn from the empirical width distribution of filtered LIRE; sample `u_i ~ Uniform(0, 1)`; construct `[nb_i, na_i] = [t_i - u_i · w_i, t_i + (1 - u_i) · w_i]`. This is the synthetic interval list for the iteration.
2. **Aoristic-resample** by drawing `y_i ~ Uniform(nb_i, na_i)` for each row; bin via `np.histogram` on 5-year edges. This is the synthetic SPA.
3. **Inject the effect** at the target magnitude and duration, with shape ∈ {step, Gaussian} per the effect-shape pre-specification (see "Effect shape for injection" below).
4. **Forward-fit the null** to the synthetic intervals via maximum-likelihood interval-integral (closed-form for exponential; per-segment trapezoidal for CPL k = 3 and k = 4); the fit recovers an estimate of `b_null` (or the CPL parameters), not the smeared SPA shape.
5. **Generate `n_mc = 1000` MC replicates** under the fitted null using the same forward-aoristic procedure (synthetic true dates from `f(t; θ̂)`, empirical widths, aoristic-resample), and compute the Timpson et al. (2014) global-*p* envelope test against the (effect-injected) synthetic SPA. Record detection at *p* < 0.05.
6. Repeat steps 1–5 a total of `n_iter = 1000` times per cell (the preregistered precision). Detection rate per cell = fraction with `p < 0.05`. The Wilson 95 % interval on a 0.80 detection rate at `n_iter = 1000` is approximately `[0.775, 0.823]` — adequate for threshold-setting at the 0.80 boundary.

**Detection threshold and the unreachable convention.** The preregistered cell-eligibility criterion is **detection rate ≥ 0.80** at the cell's *n*. Cells where the maximum *n* in the level's sweep gives detection < 0.80 are tagged `min_n_unreachable` rather than imputing a fictitious extrapolated threshold; such cells are out of scope for H3 confirmatory testing. The 20 %-over-25-years bracket is preregistered as a hard-test boundary anchoring the bottom of the power curve, and is **not in the H3b confirmatory family**: it proved near-universally unreachable across analysis levels, null models, effect shapes, and CPL knot counts in the completed Phase 1 simulation, but retaining it as a hard-test boundary keeps the power curve honestly anchored at its lower limit.

**Null model:** both **exponential (primary, per rcarbon / Timpson et al. 2014)** and **continuous piecewise-linear with k = 3 knots (CPL-3, secondary, per Timpson et al. 2021)** fitted; results compared. CPL-3 is fixed a priori rather than AIC-selected per cell, to give a well-defined secondary threshold comparable across subsets and free of per-cell knot-choice edge cases. Rationale: CPL is more flexible than exponential but has more parameters; running both lets us check whether null-model choice materially affects the min-threshold conclusions, and fixed-k keeps the comparison clean.

**Effect shape for injection:** both **step-function (sharp)** and **Gaussian-tapered (smooth)** injected in parallel; thresholds reported as a range per bracket. The step-function is a box-car of bracket magnitude for bracket duration, producing the **lower bound** on n for detection ≥ 0.80 (sharper events are easier to detect). The Gaussian has nadir = bracket magnitude and FWHM = bracket duration, producing the **upper bound** on n (smooth events with this nominal parametrisation are harder to detect via permutation-envelope methods). Reporting both is honest about shape-dependence of thresholds — real events span both shapes (e.g., Antonine Plague is sharp per Duncan-Jones 2018 military-diploma step-down; demographic decline is gradual). Detection rate ≥ 0.80 must be achieved for the **smooth-Gaussian** threshold (the binding, conservative bound) for a (level × bracket) cell to enter H3 confirmatory testing.

Adapts the Carleton, Campbell & Collard (2018, *PLOS ONE* 13:e0191055; code CC-BY) PEWMA power-simulation framework for cross-sectional SPA × covariate analysis.

**Phase 2 — H2 mixture-model validation.**

Run the mixture-model fit on empire-level LIRE. Report α̂ and 95 % CI; report corrected century-midpoint observed/expected ratios; report pairwise Pearson *r* across threshold-filtered `genuine_SPA` variants; report stratified-by-convention-class SPA alongside deconvolved `genuine_SPA`. H2.1–H2.4 criteria as listed in Field 3.

**Phase 3 — H3 substantive analyses.**

- H3a: Bayesian NBR as specified in §3 above. Report β, posterior R² (median + 95 % CI), comparison with OLS log-log (reported alongside as direct comparator to Hanson, Ortman & Lobo 2017).
- H3b: Permutation-envelope SPAs at every preregistered subset × effect-size combination. **Multiple-comparison correction.** The Holm-Bonferroni family comprises the Phase 1-reachable (level × null × bracket × shape) cells, excluding the 20 %-over-25-years bracket and the step-shape doubling-over-25-years bracket (both unreachable at all levels). This yields the reachable confirmatory cells: 2 levels (province, urban-area) × 2 null models (exponential, CPL-3) × 3 reachable bracket-shape combinations (50 %/≥50 y step, 50 %/≥50 y Gaussian, doubling/≥25 y Gaussian) = 12 cells. One pre-specified choice is locked when the H3 results are first assembled, before any H3b *p*-value is inspected: either (a) exponential and CPL-3 are treated as separate confirmatory hypotheses and Holm-Bonferroni is applied across all 12 cells, or (b) CPL-3 is treated as primary and exponential as sensitivity and Holm-Bonferroni is applied across 6 cells (one null per cell). The choice is recorded at lock time and not revisited. **Antonine-specific test is preregistered as exploratory replication of Glomb, Kaše & Heřmánková (2022) and Duncan-Jones (2018)**: at AD 165–180, test for deviation in mixture-corrected SPA at empire level, at Asclepius-cult subset (replicates Glomb et al.'s design at larger N and on corrected data), and at military-administration subset (replicates Duncan-Jones-style severe-effect prediction), conditional on per-subset sample-size thresholds being met. Results reported against the preregistered effect-size brackets; no specific effect size preregistered for the Antonine test itself. Subset-filtering feasibility depends on LIRE type / category / deity fields — confirmed as part of this preregistration (see §8).

  **Crisis-of-the-Third-Century test (exploratory).** A second exploratory replication targeting the **mid-3rd-century inscription decline at AD 235–284** (Duncan-Jones 1996; MacMullen 1982; Mrozek 1973). Unlike the Antonine signature (sharp, ~ 15-year window, single causal event), the Third-Century Crisis is a diffuse, multifaceted ~ 50-year decline driven by overlapping factors (Plague of Cyprian AD 249–262, military instability, monetary collapse, provincial fragmentation). The test window is AD 235–284 (49 years, marginally aligned with the 50 %-over-≥50-years bracket); reported against the preregistered effect-size brackets but **not pre-committed to a specific effect-size expectation** given the diffuse causal structure. Tested at empire level and at a Western-Empire provincial subset (where the Crisis impact was qualitatively sharpest per the cited literature), conditional on per-subset H1 reachability. Adds a half-century-scale event to complement the Antonine sharp-event replication, broadening the paper's substantive grounding without adding confirmatory family members.
- H3c: Residual classification + Moran's I + provincial-capital *t*-test as listed in H3.

### 5. Exploratory analyses (explicitly flagged as non-confirmatory)

- **CPL knot-sensitivity analysis (exploratory, H1).** For each CPL cell in the H1 simulation, fits k ∈ {2, 3, 4} and records AIC + detection per k. Reports threshold at each fixed k and the max−min range as a diagnostic for "does CPL threshold depend on knot count?" Non-confirmatory; reported in the paper's supplementary material.
- **CPL AIC-select threshold (exploratory, H1).** Per-iteration picks k with minimum AIC from {2, 3, 4}; reconstructs threshold under AIC-select decision rule (cf. Timpson et al. 2021). Answers "what would AIC-selected CPL have given?" without re-simulation. Non-confirmatory.
- **Stratified-sampling sensitivity (exploratory, H1).** Primary H1 thresholds use bootstrap (sampling-with-replacement) from filtered LIRE. Post-hoc, thresholds are recomputed using stratified-sampling (province-proportional or city-proportional draws) from the same persisted per-iteration parquet. Reports deltas to bootstrap primary; tests whether empirical province / city mix matters for detection power at given n. Non-confirmatory.
- **City-level temporal trajectory estimation for small-N cities (exploratory).** The confirmatory eligibility threshold (≈ 1,549 inscriptions for 50 %-over-50-years detection at urban-area level; see §6) restricts H3a / H3b urban-area confirmatory testing to a handful of the largest cities. The remaining ~800 Hanson-matched cities have inscription counts below the confirmatory threshold but are not analytically inert — Bayesian aoristic estimation with explicit uncertainty propagation can produce trajectory-shape estimates from corpora as small as N ≈ 50 (cf. Crema 2025 baorista; Bevan & Crema 2021 hierarchical diachronic-process modelling). This exploratory analysis pursues two layered questions plus an aggregate-level methodological diagnostic.

  **Core (Layer A) — temporal trajectory shape estimation.** For each Hanson-matched city, compute a posterior distribution over time-binned inscription density via a Bayesian hierarchical model: city-level temporal trajectory with an ICAR (intrinsic conditional autoregressive) prior for temporal smoothing, partial-pooling toward the province-level mean trajectory, aoristic uncertainty propagated per inscription. Report per-city posterior trajectory shape with 95 % credible intervals. **This is estimation, not hypothesis testing**: a city's trajectory is characterised by its CI band, not "significantly different from null". Implementation likely shares the baorista pipeline (see the baorista comparison item below) — practical economy.

  **Extension (Layer B) — tentative inversion to time-varying population.** Under the assumption that the cross-sectional β-scaling estimated from H3a (sublinear, β ∈ [0.3, 0.7]) holds within-city over time, invert each city's trajectory to an illustrative time-varying population estimate: `pop_t ≈ pop_max × (insc_t / insc_max)^(1/β)`. **Strong assumption flagged**: within-city β stability over time is only approximately true; known to be violated where epigraphic habit varies systematically (the Third-Century Crisis is the most likely systematic violation). Estimates are reported as illustrative *comparative-shape* outputs only — **not as quantitative population claims** at specific time points — with explicit caveat to that effect in any output that consumes them.

  **Aggregate diagnostic (~800 cities) — where do these methods work, where do they fail?** With several hundred cities in the small-N category, the analysis can move past per-city estimation to a methodological diagnostic. Pre-specified diagnostic outputs:

  - **Posterior precision vs N.** Median CI width of trajectory estimates binned by N. Identifies the practical N-floor below which estimates are too diffuse to be interpretively useful.
  - **Trajectory shape clustering.** Cluster the per-city trajectories (e.g., k-medoids on dynamic-time-warping distance) and report cluster sizes + exemplars. If clusters align with independent groupings (province, chronological epoch, dominant inscription type), the methodology is informative; if clusters appear random, it isn't.
  - **Layer B validation gate.** Where independent (non-inscription-based) population estimates exist for specific periods at specific cities (archaeological reconstructions: Pompeii AD 79, Ostia c. AD 250, etc.), compare β-inverted estimates against the independent estimates within their respective CIs. Validation gate: if Layer B trajectories overlap independent estimates' CIs in the cities where comparison is possible, the inversion is illustrative-grade defensible; if they don't, Layer B is reported as failed and the methodology constraint is itself the contribution.

  **Honest-negative-result framing.** This analysis is preregistered with the explicit possibility that small-N Bayesian aoristic estimation does not produce useful per-city estimates, or that β-inversion fails the validation gate. A negative result — "the methodology does not extend usefully to N < ~Z" — is itself a methodological contribution; constraints on aoristic SPA inference at small N are an open question in the field and documenting them empirically is valuable. The diagnostic outputs are pre-specified so that reporting the constraint is a clean exercise regardless of which way the data falls.

  **Province-scale extension (parallel methodological output).** The same methodology is applied at province scale (~50 provinces) as a parallel output: Bayesian aoristic temporal trajectory estimation per province (Layer A), tentative β-inversion to province-level temporal "inscription-derived complexity proxy" (Layer B, with all the within-province β-stability caveats noted above), and the precision-vs-N diagnostic adapted for the smaller provincial N. Province-scale results are reported as **methodological outputs only** — substantive claims about provincial prosperity dynamics are deferred to a planned follow-up paper on provincial prosperity reconstruction from inscription trajectories, where the substantial task of assembling provincial-prosperity ground truth from the archaeological / numismatic / historical literature can be undertaken with the dedicated treatment it warrants. The current paper's province-scale analysis demonstrates that the methodology runs at this aggregation level and characterises its small-N behaviour at the province count of ~50; it does not claim provincial prosperity reconstruction.

- **Variance partition for H3a (exploratory).** From the fitted Bayesian NBR posterior, decompose total variance in `log(E[inscriptions_city])` into three components: (i) `Var(β · log_pop_city)` — the population-scaling contribution; (ii) `Var(α_province)` — province-level "everything else" (economic, infrastructural, cultural variation absorbed into the random intercepts); (iii) negative-binomial residual variance — city-level "everything else" (local cultural conditions, micro-economy, patronage, prestige factors). Report each as a proportion of total variance with 95 % credible intervals (per Gelman, Hill & Yajima 2014 hierarchical variance partitioning). **No pre-committed numerical target** — the partition is hypothesis-generating, intended to characterise population's footprint relative to higher-order factors that this analysis cannot separately identify (per §9 limitations on identifiability of complexity dimensions). Sanity-check: total variance explained by the fixed + random effects should be consistent with the H3a Bayesian R² confirmatory targets within posterior uncertainty. Pre-specified interpretation framework: if `Var(β · log_pop) / Var(total) < 0.50`, this is consistent with substantial role for higher-order factors absorbed into province REs and residual; if ≥ 0.50, population is the dominant identified driver. The 0.50 threshold is for narrative framing only, not a confirmatory criterion.
- **Stratified-by-convention-class SPA** as alternative to the mixture (appendix cross-check on H2; already in the H2.4 structure but reported separately for transparency).
- **`baorista` Bayesian aoristic comparison** (Crema 2025) on representative provincial subsets. baorista — with NIMBLE, brms, and cmdstanr — is installed and smoke-validated on the project's compute server (see §8); the comparison runs as an appendix figure with accompanying discussion, providing a Bayesian-aoristic cross-check on the frequentist permutation-envelope results.
- **Scaling-residual sensitivity analysis for H3a:** compute per-city residuals from a fitted power-law `inscriptions ∝ population^β`; re-run H3a on residuals. Tests whether the Hanson-population correlation survives scaling-controlled analysis.
- **α-as-translator sensitivity analysis for H3a:** include per-city mixture α as an additional covariate in the NBR; test whether β_pop estimate shifts meaningfully. Informs whether the Hanson correlation is confounded by epigraphic-habit intensity (variable across regions).
- **Chronological resolution of H3c urban-area residuals:** extend Hanson's (2021) time-pooled residual analysis by computing residuals per decadal period. Exploratory because no published comparator exists.
- **Information-infrastructure versus complexity-markers theoretical framing.** The paper presents both readings of what inscription production proxies — Hanson's (2021) "information infrastructure" and the alternative reading of inscriptions as markers of socio-political complexity — and discusses the evidence bearing on each, rather than adjudicating between them. Feedback from presenting the work at RAC-TRAC 2026 is treated as critique to inform further exploration of both readings, not as the deciding word on which is correct.
- **Letter-count alternative analysis.** Per subset, repeat the H3 analyses using summed conservative letter counts (the `clean_text_conservative` field — Latin A–Z characters only, Greek excluded) in place of inscription counts. The rationale is a deliberate methodological disagreement with Hanson (2021). Hanson identifies the total volume of lettering as a methodologically desirable measure but rejects it as impractical, because so many inscriptions are fragmentary that their original lengths cannot be estimated (Hanson 2021, p. 142). We — with the LIRE team — take the opposite view: a flat inscription count implicitly treats a long monumental text and a three-word funerary fragment as equivalent units, when they plainly are not, and letter count, for all its preservation problems, at least registers something of the quantity of information an inscription carried. Letter count is treated as the lesser of two evils, not a problem-free measure, and reported as a cross-check on the inscription-count results rather than a replacement for them. The `clean_text_conservative` variant is used in preference to the interpretive variants because the interpretive text incorporates modern editorial restorations and expansions — exactly the kind of editor-dependent variation the deconvolution-mixture model exists to remove — whereas the conservative text counts only what survives; `clean_text_interpretive_word` is available as a sensitivity check. The analysis carries forward an exploratory observation from the project's 2024 seminar work, where a Negative Binomial model on letter counts produced a strikingly high pseudo-R²; that result was flagged at the time as "too good to be true" and a suspected artefact of the count model's dispersion structure, and is revisited here with the corrected pipeline.

### 6. Effect-size pre-specifications (summary)

| Hypothesis | Quantity | Preregistered target |
|---|---|---|
| H1 power floor | Detection rate | ≥ 0.80 at *p* < 0.05 per preregistered effect-size bracket; zero-effect false-positive rate ≤ 0.05 (achieved across all 96 zero-effect calibration cells, range `[0.007, 0.049]`). |
| H1 binding thresholds (50 % over ≥ 50 y, primary) | min n at detection ≥ 0.80 | **province** exp-step 1938, exp-gauss 1869, cpl-3-step 1385, cpl-3-gauss 1618; **urban-area** exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549; **empire** reachable at n = 50 000 (calibration). |
| H1 thresholds (doubling over ≥ 25 y) | min n at detection ≥ 0.80 | Gaussian shape: empire reachable at n = 50 000; province exp 2118, cpl-3 1934; urban-area exp 2160, cpl-3 1905. **Step shape unreachable across all levels** (mass spread evenly across 5 bins; signal-to-noise per bin marginal). |
| H1 thresholds (20 % over 25 y; hard-test boundary) | min n at detection ≥ 0.80 | Empire / cpl-3 / Gaussian reachable at n = 50 000 (single marginally-reachable cell); **all other combinations of level, null, shape, and CPL knot count unreachable**. Bracket retained in H1 as an honest-uncertainty anchor; **not in the H3b confirmatory family**. |
| H2.1 | α̂ | Posterior CI excludes 0; point estimate > 0.1 |
| H2.2 | Corrected century-midpoint O/E | Within 1.5× of local neighbourhood mean |
| H2.3 | Pairwise Pearson *r* across threshold variants | ≥ 0.9 |
| H3a urban-area | Bayesian R² | ≥ 0.25 (anchored on Hanson, Ortman & Lobo 2017 R² = 0.267) |
| H3a province | Bayesian R² | ≥ 0.50 (Palmisano et al. 2021 upper empirical range) |
| H3b primary | Antonine signature | ≥ 50 % dip sustained ≥ 50 y at AD 165–180 |
| H3b secondary | Other targets | The 50 %-over-≥50-years and doubling-over-≥25-years brackets (the 20 %-over-25-years bracket is retired from the confirmatory family — see §4); Holm-Bonferroni corrected over the remaining-eligible (level × bracket × shape) cells per the Phase 1 reachability map. |
| H3b exploratory | Crisis of Third Century | AD 235–284 window (49 y); reported against the preregistered effect-size brackets; magnitude **not** pre-committed (diffuse causal structure). Empire + Western-Empire-provincial subset, conditional on H1 reachability. Replication targets: Duncan-Jones 1996, MacMullen 1982, Mrozek 1973. |
| H3c provincial-capital | Mean residual difference | One-sided *t*-test *p* < 0.05 |
| H3c spatial clustering | Moran's I | > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} k-NN weights; qualitative pattern matches Hanson (2021) map |

### 7. Planned deviations and contingencies

- **Levels at which Phase 1 did not establish a finite detection threshold** within the swept sample-size range are dropped from confirmatory testing at that level, and may optionally be retained in the paper as exploratory. Phase 1 is complete; §6 gives the resulting thresholds and the levels they make eligible.
- **If the editorial-convention-hierarchy test confirms** the hierarchy on its 14-boundary sample, the `convention_SPA` shape in the deconvolution-mixture model shifts from uniform century slabs to a weighted hierarchical shape (century > half-century > quarter-century > reign-boundary). If the test is inconclusive, the uniform default is retained.
- **If the LIST swap completes during the fortnightly paper sprint (11–24 May 2026),** the analytical envelope extends to AD 600 and Late Antique subsets are added; otherwise the LIRE envelope remains primary.
- **If substantive methodology changes are required after lodgement** — whether prompted by co-author input or by anything else — an amendment to this preregistration is filed on OSF before implementation.

### 8. Software, reproducibility, and data access

- **Language:** Python 3.13 for the primary pipeline; R 4.4.3 for the `brms` shadow validation of the H3a model and for the baorista comparison.
- **Environment:** `uv`-managed Python virtual environment with a pinned `requirements.txt`; the R packages are installed on the project's compute server.
- **Core dependencies (Python):** `numpy`, `scipy`, `pandas`, `pyarrow`, `matplotlib`, `joblib`, `statsmodels`, `libpysal` (spatial weights for Moran's I), `pymc` and `cmdstanpy` (Bayesian NBR for H3a), `pyzotero`, `requests`, `python-dotenv`.
- **Aoristic resampling implementation note:** the Uniform aoristic method is implemented directly in `primitives.py::aoristic_resample` as ≤ 10 lines of numpy. The SDAM `tempun` package (MIT; PyPI 0.2.4) was not used, because its current release is incompatible with numpy ≥ 2.4 (it calls the removed `numpy.trapz`); the direct implementation is mathematically equivalent under the Uniform aoristic distribution. An upstream issue has been filed to `sdam-au/tempun`; if `tempun` becomes numpy-2-compatible, it may be reintroduced for the H2 / H3 pipelines, where it offers conveniences beyond Uniform aoristic resampling.
- **R dependencies (shadow validation and baorista comparison; not on the critical path for the primary Python results):** R 4.4.3, `cmdstanr` 0.9.0, `nimble` 1.4.2, `baorista` 0.2.1, and `brms` 2.23.0, with `posterior`, `bayesplot`, `loo`, and `arrow`. All installed and smoke-validated on the project compute server.
- **Data:** LIRE v3.0 (Zenodo DOI 10.5281/zenodo.8147298; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) as a ground-truth cross-check for `urban_context_pop_est`.
- **Subset-filter feasibility (confirmed on LIRE v3.0).** Military-administration subset: `type_of_inscription_clean == 'military diploma'` yields 285 rows (66.4 % null in that field; the ML-classified `type_of_inscription_auto` yields 442 rows at 13.8 % null and is a valid alternative). Asclepius-cult subset: regex `[Aa]esculap|[Aa]sclep` on the `inscription` free-text field yields 358 rows — substantially above Glomb, Kaše & Heřmánková's (2022) N = 210, suggesting their filter was stricter. The preregistered Glomb-replication test will either adopt their exact filter (if recoverable from their published methods) or use the broader keyword match and report both N values.
- **Code:** the project repository is public at `github.com/saross/inscriptions`.
- **Run artefacts:** each analysis stage is captured in a per-stage `runs/<date>-<description>/` directory recording its specification, agent briefs, random seed, code, outputs, and decisions.
- **Research record:** agent-session-capture infrastructure is operational; individual AI-agent prompts and outputs are preserved per open-science requirements.

### 9. Known limitations (preregistered)

- **Editorial-convention artefact identification.** The mixture model addresses century-midpoint spikes directly. Other documented LIST/LIRE artefacts — reign-boundary clustering, province-label anachronism (Heřmánková, Kaše & Sobotková 2021, §48; EDH anchors province labels to mid-2nd-century Roman geography), EDCS coordinate imprecision (§60; 7-decimal false precision on hundreds-of-metres real accuracy), 50 % missing coordinate provenance (§45) — remain as interpretive caveats. The preregistration commits to transparent reporting of these, not to methodological correction.
- **Single-dimension complexity (Turchin et al. 2018).** The multi-factor complexity decomposition in the paper's theoretical frame operates at city / province × decadal scale; Turchin's "single latent dimension" operates at polity × century scale. Different scales; the paper acknowledges this but does not attempt empirical disaggregation of the non-population dimensions.
- **Rome-exclusion.** Rome is excluded from scaling regressions as an extreme outlier. Consistent with Hanson (2021) methodology; reported transparently; not tested as a sensitivity.
- **Identifiability of complexity dimensions.** With inscription count as the sole observable and Hanson population as the sole external covariate, dimensions 2–6 of the complexity decomposition (economic prosperity, social differentiation, cultural translator, ideology, residual) remain theoretically present but empirically entangled. The paper acknowledges this as a scope limitation; disaggregation is left to future work.
- **Chronological envelope.** 50 BC – AD 350 (LIRE); extensible to AD 600 conditional on LIST swap. Late Antique and post-AD-600 phenomena out of scope for this paper.

### 10. Hypothesis-level structure summary

```text
Phase 1 (simulation) → Phase 2 (LIRE) → Phase 3 (LIRE)
     H1                  H2.1 – H2.4        H3a variance-explained (primary)
 min-thresholds       mixture validation   H3b deviation-detection
                                            H3c urban residuals
```

### 11. Provenance

- **Preregistration drafted** by Claude Code (Anthropic, Opus 4.7) under Shawn Ross's direction.
- **Authors and contributions (CRediT taxonomy):**
  - Shawn Ross (Macquarie University) — Conceptualization, Methodology, Investigation, Writing – original draft, Writing – review & editing, Supervision, Project administration.
  - Adela Sobotková (Aarhus University) — Methodology, Validation, Writing – review & editing.
- **AI contributions:** theoretical-frame refinements (identifiability scope, the scaling-residual sensitivity flag, and the cultural-translator confound strategy), articulation of the deconvolution-mixture model, and this preregistration draft. All substantive AI intellectual contributions are logged in the project repository.
- **Funding:** no funding was received for this work.
- **Competing interests:** the authors declare no competing interests.
- **Ethics:** this work reanalyses publicly available, published datasets and did not require ethics review.
