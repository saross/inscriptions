---
title: "OSF Preregistration — Bayesian mixture-corrected SPAs of Latin inscriptions vs Hanson urban population"
format: OSF open-ended registration (four fields)
status: draft for lodgement (2026-05-16)
---

# Preregistration — Bayesian mixture-corrected SPAs of Latin inscriptions vs Hanson urban population

**Format note:** this document is organised to map onto the four fields of an OSF *open-ended registration* (Title; Description; Research Questions / Hypotheses; Additional Information). Fields 1–3 are short; Field 4 carries the detail.

---

## Field 1: Title

**Mixture-corrected SPAs of Latin inscriptions against Hanson urban population estimates: a preregistered three-phase analysis.**

---

## Field 2: Description

We preregister a three-phase analysis of the spatial distribution of Latin inscriptions in the Roman Empire (50 BC – AD 350), using summed probability analysis (SPA) with a novel Bayesian deconvolution-mixture correction for editorial-convention dating artefacts.

The editorial-convention artefact, quantified empirically in the project's descriptive profiling of LIRE v3.0, takes the form of pronounced endpoint rounding under inclusive-Roman century counting: **54.5 % of all `not_before` values in the filtered corpus end in `01`; 53.0 % of all `not_after` values end in `00`**. The widely-observed inflation in aoristic mass at century-midpoint years (AD 50 / 150 / 250 / 350, with observed/expected ratios of 22.8× / 41.5× / 18.8× / 39.7× respectively, all Westfall-Young adjusted *p* < 0.001 on 20,000 permutations) is a *derivative* effect of this endpoint rounding — intervals such as `[1, 100]` and `[101, 200]` place aoristic mass on midpoint years by construction.

**Phase 1** establishes methodological readiness via simulation-based minimum-sample-size thresholds for permutation-envelope deviation-detection. Phase 1 is complete and its results are reported in this preregistration as fixed groundwork that gates Phase 2 and Phase 3 testing.

**Phase 2** validates the Bayesian mixture model by a recovery simulation — synthetic observed SPAs are constructed from a *known* genuine SPA, a *known* mixing weight α, and a *known* convention component; the model is judged to validate if it recovers the known α and the known genuine-SPA shape within a preregistered tolerance. Real-data consistency and robustness checks complement the recovery simulation but do not stand in for validation.

**Phase 3** quantifies the population dimension's footprint on inscription variation via a Bayesian negative-binomial regression of inscription counts on Hanson (2016) urban-population estimates, specified with within-between (Mundlak) centring to give a clean *within-province* population effect; permutation-envelope deviation-detection at pre-specified historical windows; and a Hanson-replication residual analysis (provincial-capital contrast plus spatial-autocorrelation clustering).

The paper's primary contribution is methodological; the illustrative substantive finding is a within-province population-attributable variance fraction at urban-area scale. The substantive interpretive question — what inscription production proxies (urban-information-infrastructure, socio-political complexity, or some combination) — is deliberately scoped out of this preregistration. Confirmatory results test the reproducibility of patterns in the corrected signal, not the validity of any specific proxy model.

---

## Field 3: Research Questions and Hypotheses

### Primary research question

After controlling for editorial-convention dating artefacts via a Bayesian deconvolution-mixture model, what fraction of the **within-province** spatial variation in Latin inscription production during the Roman Empire is accounted for by urban population dynamics?

### Secondary research questions (descriptive context — not confirmatory hypotheses)

(SR1) Does mixture-corrected SPA at urban-area and province scales reproduce, on artefact-corrected data, the sublinear inscription-vs-population scaling pattern reported by Hanson (2021, mean exponent β = 0.672, 95 % CI [0.588, 0.756] in site-level cumulative inscription counts across 554 sites with Rome excluded) and for elite-honorific subsets by Carleton et al. (2025, β ≈ 0.3–0.5 across the monument and headline-epigraphy analyses, with an epigraphy-no-zeros variant at β ≈ 0.68)?

(SR2) Do urban-area residuals from the mixture-corrected regression reproduce two further findings of Hanson (2021): (i) that provincial capitals over-produce inscriptions relative to the scaling expectation (Hanson 2021, p. 148: mean residual 0.43 for provincial capitals vs ~0.06 for *coloniae* / *municipia*); and (ii) that residuals are spatially clustered (Hanson 2021, Table 7.4: Moran's I = 0.046, z = 4.571, *p* < 0.0001 for residuals; I = −0.006, *p* = 0.282 for raw counts)?

### Completed methodological groundwork (Phase 1)

Phase 1 was a simulation-based determination of minimum-sample-size thresholds for permutation-envelope deviation-detection across the H3 analysis levels (empire, province, urban-area). It is not a confirmatory hypothesis with a live decision rule; the simulation is complete, the thresholds it produced are reported in §6, and they gate which (level × subset) combinations are eligible for Phase 3 confirmatory testing. Full pipeline (code, fixed random seed 20260425, parametric grid, results) is committed to the public project repository for end-to-end reproducibility.

### Confirmatory hypotheses (Phase 2 and Phase 3)

**H2 — Bayesian mixture-model validation via recovery simulation.**

H2.1 (recovery simulation, confirmatory): synthetic observed SPAs are constructed from a known genuine SPA + known α + known convention component, across a pre-specified parametric grid spanning the empirical range of α observed during pilot fitting. The Bayesian mixture is judged validated if the recovered posterior α̂ falls within the 95 % credible interval of the true α in ≥ 90 % of grid cells *and* the recovered genuine-SPA shape correlates (Pearson r) with the true genuine shape at ≥ 0.95 on average across grid cells. Either failure triggers an OSF amendment and model revision before any Phase 3 analysis.

**H3 — Population signal.**

H3a (primary confirmatory quantitative result; within-province population-attributable variance fraction): a Bayesian within-between (Mundlak) negative-binomial regression of inscription counts on Hanson (2016) urban population, splitting `log(population)` into a province-mean component and a city-level within-province deviation, yields a *within-province population-attributable variance fraction* whose posterior 95 % credible interval excludes 0.10. The estimand is `Var(β_within · (log_pop − log_pop_province_mean)) / Var(log E[insc])` on the latent (log) scale; reporting includes the full posterior distribution as the estimate.

H3c (Hanson 2021 residual replication; two-part confirmatory):

- H3c(i) — provincial-capital residuals: on the H3a posterior, the contrast `mean_residual(provincial_capitals) − mean_residual(non-capitals)` exceeds 0 with posterior probability ≥ 0.95. Computed as a posterior contrast over draws (not a frequentist *t*-test on posterior summaries).
- H3c(ii) — spatial clustering: Moran's I on H3a residuals is > 0 at *p* < 0.05 in at least two of the sensitivity series {k = 5, k = 8, k = 10} k-NN spatial weights. No regional-pattern map-match clause (see §3 and the change log).

### Pre-specified exploratory analyses (not confirmatory)

**H3b — pre-specified exploratory deviation-detection.** Mixture-corrected SPAs are scanned at pre-specified historical windows on pre-specified subsets, against the project's permutation-envelope machinery. Specifically:

- **Antonine probe (AD 165–180):** tested at empire level, at an Asclepius-cult subset (replicating Glomb, Kaše & Heřmánková 2022 on artefact-corrected data at larger N), and at a military-administration subset (replicating Duncan-Jones 2018-style severe-effect prediction), conditional on per-subset Phase 1 reachability.
- **Crisis-of-the-Third-Century probe (AD 235–284 inclusive, 50 years under inclusive-Roman counting):** tested at empire level and at a Western-Empire provincial subset, conditional on Phase 1 reachability.

No effect-size magnitudes are pre-committed for either probe — the empirical priors conflict (Glomb et al. 2022 found a null at small N; Duncan-Jones 2018, Fig. 4 / Table 7.1, found an abrupt cessation of military diplomas after AD 167, effectively a complete halt in that subcorpus until a single resumption in AD 177; the Crisis is a diffuse multi-decade decline). Results are reported against the project's standard effect-size brackets (50 % over ≥ 50 y; doubling over ≥ 25 y; 20 % over ≥ 25 y) descriptively, with multiplicity reported alongside, but no Holm-corrected confirmatory family is formed.

**Phase 2 real-data consistency and robustness checks** (supporting, not validation):

H2.2: the mixture-corrected `genuine_SPA` shows reduced editorial-convention spikes — at the four century-midpoint bins (AD 50, 150, 250, 350), the corrected value at each midpoint falls within 1.5× of the mean of the corrected `genuine_SPA` over the ±25-year neighbourhood (5 bins on each side), excluding the midpoint bin itself. Reported alongside: (i) a shoulder-excluded variant additionally excluding the bins at ±5 y; and (ii) the same ratio at ±15 y and ±35 y neighbourhood widths as a width-sensitivity check.

H2.3: `genuine_SPA` converges across date-range threshold filtering — Pearson r ≥ 0.9 between any two SPAs constructed from subsets filtered by `date_range` ≤ 25, 50, 100, 200, 300 years.

H2.4: stratified-by-convention-class SPA (hard classification: convention-anchored vs precise) recovers a SPA shape agreeing with the Bayesian mixture's `genuine_SPA` within sampling error. Reported transparently as an internal-consistency check, *not* an independent validation (the two methods share the same convention-vs-precise row classification).

---

## Field 4: Additional Information

### 1. Dataset and corpus

**Primary:** LIRE v3.0 (Kaše, Heřmánková & Sobotková, Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 rows; 63 attributes in the released parquet. Two filter flags used below — `is_within_RE` and `is_geotemporal` — are **derived** at filter time rather than being native columns of the released parquet: `is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT NULL AND not_before ≤ not_after` (the row has a usable geographic and temporal locus); `is_within_RE := province IS NOT NULL` (the row is geo-located within a Roman province). Filtering with these derived flags plus a 50 BC – AD 350 date-interval intersect (overlap, not containment) yields **180,609 rows** (≈ 98.8 % of the pre-filter total). Pre-joined Hanson (2016) urban-population estimates are available as the `urban_context_pop_est` attribute at row level (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

**Possible extension:** LIST v1.2 (same team, Zenodo DOI 10.5281/zenodo.10473706, 9 January 2024). 525,870 rows; the same released schema as LIRE. Extends the temporal envelope to 50 BC – AD 600 (sparser Late Antique coverage). If the LIST swap is ready during the fortnightly paper sprint (11–24 May 2026), analyses extend accordingly; otherwise the LIRE envelope remains primary.

**Rome excluded** from all scaling regressions as an extreme outlier, following Hanson (2021, Table 7.3 caption) — methodologically consistent with prior published work. Rome alone contributes **65,435 inscriptions** to the filtered corpus: 36.2 % of the 180,609-row total, or 46.5 % of the 140,575 inscriptions assigned to a Hanson-catalogued city. The Rome-excluded corpus is therefore **115,174 inscriptions**. Excluding Rome removes a single data point that would otherwise dominate the scaling fit; the exclusion is reported transparently and is not tested as a sensitivity (see §9).

### 2. Subset levels and sample-size sweep

Subsets analysed at three levels, each with a minimum-inscription-count threshold fixed by the completed Phase 1 simulation (see §6):

- **Empire-wide:** all inscriptions meeting filters; primary level for temporal analyses (Rome excluded). Phase 1 swept empire-level n at 1,000 / 2,500 / 5,000 / 10,000 / 25,000 / 50,000 inscriptions.
- **Province:** ~50 provinces in LIRE. Threshold candidate values tested by simulation: 100, 250, 500, 1,000, 2,500, 5,000, 10,000, 25,000 inscriptions.
- **Urban area:** ~816 cities with Hanson population estimates. Threshold candidate values tested by simulation: 25, 50, 100, 250, 500, 1,000, 2,500 inscriptions.

The cross-city H3a Bayesian NBR uses *all* ~815 cities with Hanson population estimates after Rome-exclusion — the Phase 1 thresholds gate per-subset *time-series* analyses (H3b deviation-detection; the §5 small-N trajectory work), not the cross-sectional regression.

Date-range filtering thresholds examined for H2.3 robustness: `date_range` ≤ 25, 50, 100, 200, 300 years (matching the 2024 exploratory-notebook sweeps).

### Analysis pipeline — a plain-English walkthrough

*This subsection explains the analysis in plain terms, for readers — including numerate archaeologists and epigraphers who are not statisticians — who want the intuition before the technical detail. It is explanatory only: §3 below is the binding technical specification, and where the two appear to differ, §3 governs.*

**The problem.** Every Latin inscription in the corpus carries a *date range* — an earliest and a latest plausible year — rather than an exact date. We want to know two things: how inscription production varied across cities, and how far that variation is driven by city population. Two obstacles stand in the way. First, the dates are uncertain. Second, the dates are *systematically distorted* by editorial convention: epigraphic editors, faced with a vaguely datable inscription, round its date range to inclusive-Roman century boundaries — "2nd century AD" gets encoded as the interval AD 101–200, "1st century AD" as AD 1–100, and so on. This rounding is visible directly in the data: over half of all interval starts (`not_before` values) end in `01`, and over half of all interval ends (`not_after` values) end in `00`. The widely-noted "spikes" at AD 50 / 150 / 250 / 350 are a *consequence* of this — intervals like AD 1–100 place aoristic weight on AD 50 by construction.

**Step 1 — from date ranges to a production curve (aoristic sampling and the SPA).** "Aoristic" — a term borrowed from criminology and archaeology meaning *"of indeterminate time"* — handles date uncertainty by spreading each inscription's "weight" uniformly across its possible date range, instead of pretending it has a single true date. Summing that spread weight across every inscription year by year produces a *summed probability analysis* (SPA), a curve estimating how much inscription production happened in each period. We compute the SPA on 5-year bins (so each point of the curve represents a 5-year window) — fine enough to see decadal structure, coarse enough to be stable. The SPA is the basic object every later step works on.

**Step 2 — removing the editorial artefact (the Bayesian mixture model).** The SPA we observe is a *blend* of two components: a "convention" component, produced entirely by editorial rounding to century and half-century boundaries; and a "genuine" component, reflecting the ancient pattern of inscription production. The mixture model formalises this as `observed = α × convention + (1 − α) × genuine`, where α is the share attributable to convention. We fit the model in a Bayesian framework — meaning we specify prior distributions on α, on the shape of the convention component, and on the shape of the genuine component, then update those priors against the observed SPA to obtain *posterior* distributions for all three. The posterior on the genuine component is the corrected curve; the posterior on α tells us how much of the observed SPA was convention. This deconvolution is the paper's central methodological contribution.

The convention component itself has explicit structure: a *century* layer (mass at the inclusive-Roman boundaries — AD 1, 101, 201, 301 for starts; AD 100, 200, 300 for ends; AD 50, 150, 250, 350 as the midpoints intervals like 1–100 land on), a *half-century* layer (mass at AD 51, 151, 251), and a small *reign-related* layer (mass at the small set of dynastic-transition years that the descriptive profiling identified as additional rounding anchors). The Bayesian priors regularise the inverse problem — without them, deconvolution is ill-posed; with them, the data adjudicates the relative weight of each layer.

**Step 3 — validating the mixture model (recovery simulation).** Before trusting the corrected curve, we need to know the model can actually recover known answers. We build a *recovery simulation*: we construct synthetic observed SPAs by combining a known genuine SPA, a known α, and a known convention component, then run the Bayesian mixture on those synthetics and check it recovers the known α and the known genuine shape. The model is judged validated if it does so within a preregistered tolerance across a parametric grid. If it fails, we amend the preregistration and revise the model before doing any of the substantive analyses. This recovery simulation is the actual validation of the mixture; the existing real-data consistency and robustness checks (does the corrected curve look right? is it stable across data subsets?) are supporting evidence, not validation in their own right.

**Step 4 — telling signal from noise (the permutation envelope).** Even a corrected curve wiggles. To decide whether a given wiggle is a real historical event or just noise, we build a "what noise alone looks like" band: we simulate many artificial datasets under a deliberately featureless model (smooth growth or decline, no special events), measure how much *those* curves wiggle, and check whether the real curve pokes outside the resulting band. Poking outside it indicates a deviation unlikely to be chance. The featureless models we use are *exponential growth* (a single parameter — the growth or decay rate) and *piecewise-linear with three knots* ("CPL-3" — three connected line segments, with the knot positions allowed to fit; flexible enough to capture rise-and-fall but rigid enough to be a clear null). The technical subtlety: the featureless model is fitted to the *date ranges themselves* (treating each row's `[not_before, not_after]` as the observation and integrating the model's density over the range), and the date-range uncertainty is then re-applied when generating simulated datasets. A more naive approach fitted the model on the already-uncertainty-spread observed SPA and then re-applied that uncertainty when simulating — double-counting the uncertainty, narrowing the noise band, and producing false alarms. The forward-fit approach corrects this and gives proper false-positive control.

**Step 5 — establishing what the method can detect (Phase 1, complete).** None of the above is worth running on a corpus too small for the method to see anything. So before the substantive work, we simulated: at each analysis level (whole empire, individual province, individual city), and for events of several sizes, how many inscriptions does a level need before the method reliably detects the event? Phase 1 is complete; the resulting thresholds (§6) fix which subsets are eligible for confirmatory deviation-detection.

**Step 6 — the population question (H3a, Bayesian negative-binomial regression).** With a corrected signal in hand, we ask how far city population explains inscription production. The regression is *negative-binomial* because inscription counts are far more variable than a simple count model would predict (they are *over-dispersed*), and *Bayesian* because that yields a full distribution of plausible values for every quantity of interest — which is where the analysis's uncertainty intervals come from. The regression splits each city's `log(population)` into two parts: a *province-mean* component (the average log-population of cities in the city's province) and a *within-province* component (how much the city's log-population deviates from its province's mean). Each gets its own coefficient. The split lets us identify a clean *within-province* population effect — "holding province constant, do bigger cities produce proportionally more inscriptions" — that is unconfounded with province-level differences in epigraphic culture, administrative structure, and survival-bias. The between-province effect is also reported but with an explicit caveat: it is not separately identifiable from "province-level everything else." This Mundlak ("within-between") specification is the standard solution in multilevel modelling when a city-level predictor varies between groups (cities cluster by province; provinces have systematically different city-size distributions).

The headline quantity is the **within-province population-attributable variance fraction** — the proportion of the variance in `log E[inscriptions per city]` accounted for by the within-province component of `log(population)`. We pre-commit to the *estimand*, not to a specific numerical value: the confirmatory rule is that the posterior 95 % credible interval excludes 0.10 (a non-trivial share).

**Step 7 — which cities break the pattern, and where (H3c, residuals and spatial clustering).** Finally, we look at the cities the regression gets *wrong* — those producing markedly more or fewer inscriptions than their population predicts (the residuals) — and ask two questions about them. First, do *provincial capitals* over-produce relative to other Roman city-statuses (replicating Hanson 2021's finding that capital residuals are markedly positive)? Computed as a posterior contrast: on each posterior draw of the residuals, we take the difference (mean over capitals) − (mean over non-capitals), and ask whether that difference exceeds 0 with posterior probability ≥ 0.95. Second, are the residuals *spatially clustered*? Computed as Moran's I — the standard test for spatial autocorrelation — on the residual surface, using nearest-neighbour spatial weights with sensitivity at k = 5, 8, and 10. Hanson 2021 reported Moran's I = 0.046, *p* < 0.0001 for residuals (and Moran's I ≈ 0, *p* = 0.282 for raw counts, confirming the clustering is in the residuals, not in the base inscription count distribution). The confirmatory rule is Moran's I > 0 at *p* < 0.05 in at least two of the three k values.

**How the phases connect.** Phase 1 (completed groundwork) determines which (level × subset) combinations are eligible for Phase 3 deviation-detection. Phase 2 (Bayesian mixture validation) provides the corrected signal used in Phase 3. Phase 3 (H3a within-between regression + H3c residual analysis) answers the primary research question and the Hanson-replication secondary questions. The pre-specified exploratory H3b deviation-detection at the Antonine and Crisis-of-the-Third-Century windows runs alongside Phase 3 but is not gated by confirmatory testing — its windows and subsets are pre-specified but its effect-size magnitudes are not.

### 3. Analysis pipeline

- **Aoristic sampling:** the Uniform aoristic method — each inscription's probability mass spread uniformly over `[not_before, not_after]` — is the primary treatment. A trapezoidal distribution (mid-interval more probable than the interval edges) is run as a sensitivity analysis on **every (level × subset) combination eligible for H3 confirmatory testing** (i.e. every subset that clears the Phase 1 reachability threshold for the binding bracket), plus the full-empire SPA. Convergence between uniform and trapezoidal is assessed by Pearson *r* between the two SPAs per subset; the sensitivity is deemed material in any subset where *r* < 0.95, in which case the trapezoidal SPA is reported alongside the uniform primary. The Uniform method is implemented directly in the project code (≤ 10 lines of numpy) rather than via the SDAM `tempun` package, whose current release (0.2.4) is incompatible with numpy ≥ 2.4; the direct implementation is mathematically equivalent to `tempun`'s Uniform aoristic method.

- **Binning:** 5-year bins across the analysis envelope (matching the 2024 exploratory notebook; reviewer-familiar).

- **SPA construction:** sum of per-inscription probability mass across bins; optional weighting by `clean_text_conservative` letter count for the secondary letter-count analyses (see §5).

- **Permutation envelope:** an rcarbon-style `modelTest()` significance test (Crema & Bevan 2021), implemented in Python as a hand-rolled Monte Carlo envelope loop following Timpson et al. (2014). The loop samples Monte Carlo replicates from a fitted parametric null, computes a pointwise 95 % envelope, and evaluates a global *p*-value as the proportion of replicates with at least as many bins falling outside the pointwise envelope as the observed SPA. Two design choices are central:

  **The null is fitted in true-date space, not in aoristic-smeared SPA space.** The maximum-likelihood fit treats each row's `[not_before, not_after]` interval as the observation and integrates the parametric density `f(t; θ)` over the interval: `L_i(θ) = ∫_{nb_i}^{na_i} f(t; θ) dt / Z(θ)`. For the exponential null this has a closed form; for the CPL null it is per-segment trapezoidal integration. Fitting in true-date space means the date-range uncertainty is *not* absorbed into the fitted null.

  **Monte Carlo replicates are forward-aoristic-smeared.** Synthetic true dates are drawn from the fitted density `f(t; θ̂)`, paired with empirical `[not_before, not_after]` widths drawn from the bootstrap sample, positioned uniformly within the resulting interval, and aoristic-resampled once by a uniform draw within the interval. This produces Monte Carlo SPAs whose variance structure matches the observed SPA pipeline (bootstrap row → aoristic-resample → bin) under the null model. An alternative that fits the null on the already-smeared observed SPA and then re-applies aoristic widths was tested and rejected: it double-counts the date-range uncertainty (the fitted null is already smeared, because it was fit on smeared data), inflating the Monte Carlo envelope width and the false-positive rate. The forward-fit-in-true-date-space approach corrects this and recovers proper false-positive control — false-positive rates fall within `[0.007, 0.049]` across all 96 zero-effect calibration cells of the completed Phase 1 simulation (Cells > 0.05: 0 of 96).

  Null models: **exponential** (primary, per Timpson et al. 2014) and **continuous piecewise-linear with k = 3 knots** (CPL-3, secondary, per Timpson et al. 2021); 1,000 Monte Carlo replicates; two-sided 95 % envelopes. CPL with k = 3 is the *sole* confirmatory CPL null; CPL with k = 2 knots was tested in validation and excluded (systematic false-positive bias at high n on a 3-knot ground truth — structurally underfit), and CPL with k = 4 knots is retained as an exploratory upper bound for knot-count sensitivity only (k = 3 is AIC-best in 73 % of CPL iterations in the completed Phase 1 simulation; AIC-selected results are reported in supplementary material and do not substitute for the fixed-k = 3 confirmatory result).

- **Bayesian deconvolution-mixture model:** the observed SPA is modelled as

  `observed_SPA(t) = α · convention_SPA(t) + (1 − α) · genuine_SPA(t)`

  with the components specified as follows.

  **Convention component.** A weighted sum over three pre-specified tiers, with tier weights estimated jointly with α:

  - **Century tier:** mass at the inclusive-Roman century-start years (AD 1, 101, 201, 301), the inclusive-Roman century-end years (AD 100, 200, 300; AD 0 included as a boundary anchor for pre-AD-1 intervals), and the century-midpoint years (AD 50, 150, 250, 350) on which intervals like `[1, 100]` and `[101, 200]` deposit mass.
  - **Half-century tier:** mass at AD 51, 151, 251 (inclusive-Roman half-century starts).
  - **Reign-related tier:** mass at a curated set of dynastic-transition years where the project's diagnostic identified Holm-significant endpoint clustering: 27 BC, AD 14, 41, 69, 79 (Vesuvius / Titus), 117, 138, 161, 217, 222, 235, 251, and 270.

  Within each tier, each anchor year is given the same weight; the tier-level weights are estimated. Sub-century tiers (quarter-century, decade, lustrum) are *not* given a model component — the diagnostic showed these are at or below baseline.

  **Genuine component.** A smooth non-negative density over the analysis envelope, with a smoothness prior (Gaussian random walk; bandwidth weakly-informative). No assumption about the shape — the genuine component is what remains after the convention is removed.

  **Priors.** α ~ Beta(2, 2) (centred at 0.5, weakly-informative); tier weights ~ Dirichlet (uniform); genuine-component smoothness ~ HalfNormal(σ) with σ ~ HalfNormal(1).

  **Fit.** Posterior sampling via pymc (Hamiltonian Monte Carlo / NUTS). Convergence diagnostics: Gelman-Rubin R̂ < 1.01 on all parameters; effective sample size ≥ 400 per chain on α and tier weights; no divergences. Failure of any diagnostic triggers an OSF amendment.

  **Validation.** Recovery simulation per H2.1 (see §4). The supporting consistency / robustness checks (H2.2 / H2.3 / H2.4) run on real data.

- **Bayesian NBR for H3a (within-between specification):**

  ```text
  y_c ~ NegativeBinomial(mu_c, dispersion)
  log(mu_c) = α_0 + α_province[c]
              + β_within  · (log_pop_c - log_pop_province_mean[c])
              + β_between · log_pop_province_mean[c]

  Priors (preregistered, weakly-informative):
    α_0          ~ Normal(0, 5)         # intercept on log-count scale
    β_within     ~ Normal(0, 1)         # weakly-informative; prior-predictive checked
    β_between    ~ Normal(0, 1)         # weakly-informative
    α_province   ~ Normal(0, σ_prov)    # random intercepts
    σ_prov       ~ HalfNormal(1)        # provincial heterogeneity
    1/dispersion ~ HalfNormal(1)        # overdispersion
  ```

  The within-between (Mundlak / hybrid) specification gives a clean *within-province* population effect by construction: the within-province deviation `(log_pop_c − log_pop_province_mean[c])` is orthogonal to province membership, so its variance component is unambiguous and unentangled with `α_province`. The between-province effect `β_between · log_pop_province_mean[c]` is also reported but explicitly flagged as not independently identifiable from province-level "everything else" (see §9).

  **Sample.** All cities with Hanson population estimates, Rome excluded (~ 815 cities). The Phase 1 ≈ 1,549-inscription urban-area threshold gates per-city *temporal* analyses (H3b deviation-detection; the §5 trajectory work), not this cross-city regression.

  **Confirmatory estimand and decision rule (H3a).** The within-province population-attributable variance fraction on the latent (log) scale:

  `f_within = Var(β_within · (log_pop_c − log_pop_province_mean[c])) / Var(log E[inscriptions_c])`

  computed per posterior draw and reported as a posterior distribution. The hypothesis is supported if the posterior 95 % credible interval excludes 0.10. (The numerator is the within-province population contribution; the denominator is the total variance in the linear predictor on the log scale, computed on the same posterior draw to avoid scale ambiguity.) Reporting also includes Bayesian R² (Gelman, Goodrich, Gabry & Vehtari 2019; full-model latent-scale; cross-checked against `brms::bayes_R2`), the OLS log-log coefficient as a direct comparator to Hanson, Ortman & Lobo 2017, and the between-province component reported descriptively.

  **Prior predictive checks** (preregistered, per the Gelman et al. 2020 "Bayesian Workflow" arXiv:2011.01808): before fitting, simulate observed inscription counts from the prior alone (no data) and check that the simulated counts span a plausible range for ~ 815 Roman cities (most counts in [0, 10^4]; no implausibly large counts). If the prior generates physically absurd counts, the priors are revised before fitting; the revision is recorded in the change log.

  **Posterior predictive checks** (preregistered):

  1. **Density overlay** (`arviz.plot_ppc`): posterior-predictive inscription-count distribution overlaid against the observed count distribution.
  2. **Test statistics** — observed vs posterior-predictive: proportion of zeros (NBR sanity check — triggers zero-inflation consideration if divergent), mean, standard deviation, 95th percentile, mean-variance ratio (dispersion adequacy).
  3. **Residual structure** — standardised Pearson residuals vs fitted values and vs key predictors (within-province `log_pop` deviation, province); looks for remaining structure indicating model mis-specification.

  Any failed check triggers an OSF amendment and model revision before moving to H3c.

  **Primary implementation in `pymc`** (Python). **Secondary `brms`-via-R cross-validation shadow** (~ 50 lines, committed as `scripts/h3a_brms_shadow.R`): refits the same within-between model in R + Stan, providing (i) cross-language validation that pymc and brms agree on the posterior within Monte Carlo noise and (ii) legibility for R-native co-authors who read brms syntax more fluently than pymc code. The brms shadow's negative-binomial dispersion-prior parameterisation requires a small Jacobian adjustment to match pymc's preregistered `1/dispersion ~ HalfNormal(1)` prior; details (the `stanvar()` block and the Jacobian derivation) are committed in the script's docstring and supplementary material rather than reproduced here. If pymc and brms disagree on the posterior beyond Monte Carlo noise, the cause is investigated; if the disagreement materially affects H3a's confirmatory result, an OSF amendment is filed before lodging final results.

- **Residual analysis (H3c).** Per-city posterior residuals are extracted from the H3a fit. The *continuous* posterior residual is the quantity used in both H3c confirmatory tests (the capitals contrast and Moran's I). For descriptive purposes in the paper, cities are labelled "over-producing" / "under-producing" / "typical" when the observed count falls outside / inside the ±95 % posterior credible interval from predicted — this labelling is narrative only and does not gate any confirmatory decision rule.

- **Spatial clustering (H3c).** Moran's I with row-standardised spatial weights via *k*-nearest-neighbours (`libpysal.weights.KNN.from_dataframe`). **Primary k = 8** — Cliff & Ord 1981 on Moran's I in general; the k = 8 default for point data follows the k-NN convention codified by Anselin 1995 and subsequent spatial-econometrics literature; robust to the Empire's uneven site density. **Sensitivity at k = 5 and k = 10** reported alongside. Hanson (2021, Table 7.4) reported Moran's I = 0.046 on residuals (z = 4.571, *p* < 0.0001) and Moran's I = −0.006 on raw counts (z = −1.076, *p* = 0.282), using ArcGIS's default Spatial Autocorrelation tool (Hanson 2021, p. 145; weights construction unspecified — exact-numerical-match is not feasible). The confirmatory rule is **Moran's I > 0 at *p* < 0.05 in at least two of {k = 5, k = 8, k = 10}**. No "qualitative pattern matches Hanson's map" clause: a prior re-verification of Hanson 2021 (recorded in the change log) confirmed that Hanson does *not* identify a regional pattern in the residuals — on the contrary, he explicitly states "there does not seem to be any obvious pattern" (p. 147) and that sites from different regions are "evenly scattered" (p. 148). The Moran's I clustering finding is the only spatial-structural claim Hanson makes, and is the only one we replicate.

### Uncertainty quantification

Every quantity this preregistration commits to is reported with an interval. Because the analyses span frequentist simulation, frequentist model fitting, and Bayesian inference, the interval *type* differs by analysis — there is no single confidence-interval recipe that fits all of them.

| Analysis | Quantity | Interval method |
|---|---|---|
| Phase 1 (completed) | Detection rate per cell | Wilson score 95 % interval on the proportion of simulation iterations with *p* < 0.05 (n_iter = 1,000). |
| Permutation envelope (H3b) | The envelope itself | 2.5th / 97.5th percentiles of the Monte Carlo replicate distribution, per bin (pointwise 95 % envelope); significance via the Timpson et al. (2014) global *p*-value. The envelope *is* the uncertainty representation — no separate interval is computed. |
| H2.1 (recovery) | α̂, recovered genuine-SPA shape | Posterior 95 % credible interval on α̂ per grid cell (Bayesian mixture); Pearson r between recovered and known genuine shape, reported as a posterior distribution. |
| H2.2 | Midpoint vs neighbourhood ratio | Direct point estimate from the corrected `genuine_SPA`; primary and sensitivity windows reported alongside. |
| H2.3 | Pairwise Pearson *r* across threshold-filtered SPAs | Nonparametric bootstrap percentile interval (rows resampled with replacement). |
| H3a | β_within, β_between, variance partition, Bayesian R² | Posterior 95 % credible intervals, computed directly from the fitted posterior. Bootstrap is *not* used: the posterior distribution already represents the full uncertainty, and resampling a Bayesian fit would double-count it. |
| H3c (i) | Capitals contrast | Posterior 95 % credible interval on the contrast; decision rule reported as P(contrast > 0). |
| H3c (ii) | Moran's I | Conditional permutation inference (999 permutations of residuals over fixed spatial weights) — the field-standard significance procedure for Moran's I — reported for each of k = 5, 8, 10. |

Where an interval excludes (or includes) a preregistered threshold, that is the basis on which the corresponding hypothesis is judged supported or not.

### 4. Pre-specified confirmatory and exploratory analyses

**Phase 1 — completed groundwork.**

Phase 1 has executed; the protocol-as-run is described here for the research record. For each combination of (subset level ∈ {empire, province, urban-area}; effect-size bracket ∈ {the three brackets — 50 %/≥ 50 y, doubling/≥ 25 y, 20 %/≥ 25 y — plus a zero-effect calibration check}; sample size n ∈ logarithmic sweep):

1. **Generate synthetic intervals from a specified ground-truth null.** For exponential ground truth, draw `n` true dates `t_i ~ Exp(b_null)` truncated to the analysis envelope `[-50, 350]`; for CPL ground truth, draw from the fitted CPL density. Pair each `t_i` with a width `w_i` drawn from the empirical width distribution of filtered LIRE; sample `u_i ~ Uniform(0, 1)`; construct `[nb_i, na_i] = [t_i - u_i · w_i, t_i + (1 - u_i) · w_i]`. This is the synthetic interval list for the iteration.
2. **Aoristic-resample** by drawing `y_i ~ Uniform(nb_i, na_i)` for each row; bin via `np.histogram` on 5-year edges. This is the synthetic SPA.
3. **Inject the effect** at the target magnitude and duration, with shape ∈ {step, Gaussian} per the effect-shape pre-specification (see below).
4. **Forward-fit the null** to the synthetic intervals via maximum-likelihood interval-integral (closed-form for exponential; per-segment trapezoidal for CPL k = 3 and k = 4); the fit recovers an estimate of `b_null` (or the CPL parameters), not the smeared SPA shape.
5. **Generate `n_mc = 1000` MC replicates** under the fitted null using the same forward-aoristic procedure, and compute the Timpson et al. (2014) global-*p* envelope test against the (effect-injected) synthetic SPA. Record detection at *p* < 0.05.
6. Repeat steps 1–5 a total of `n_iter = 1000` times per cell. Detection rate per cell = fraction with `p < 0.05`. The Wilson 95 % interval on a 0.80 detection rate at `n_iter = 1000` is approximately `[0.775, 0.823]` — adequate for threshold-setting.

Cell count: 3 levels × 2 nulls × (3 brackets × 2 shapes + 1 zero-effect calibration) × 1 representative-n cell per (level × null × shape × bracket) combination = **96 zero-effect calibration cells** plus the substantive-effect cells; full grid in the run report.

**Detection threshold and the unreachable convention.** The cell-eligibility criterion is **detection rate ≥ 0.80** at the cell's *n*. Cells where the maximum *n* in the level's sweep gives detection < 0.80 are tagged `min_n_unreachable` rather than imputing a fictitious extrapolated threshold. The 20 %-over-25-years bracket is preregistered as a hard-test boundary anchoring the bottom of the power curve, and is **not** in the (exploratory) H3b family: it proved near-universally unreachable.

**Null model:** both **exponential** (primary, per Timpson et al. 2014) and **continuous piecewise-linear with k = 3 knots** (CPL-3, secondary, per Timpson et al. 2021) are fitted; results compared. CPL-3 is fixed a priori rather than AIC-selected per cell, to give a well-defined secondary threshold comparable across subsets.

**Effect shape for injection:** both **step-function** and **Gaussian-tapered** injected in parallel; thresholds reported as a range per bracket. The Gaussian's parametrisation is FWHM = bracket duration (a convention; binding thresholds inherit this choice). Detection rate ≥ 0.80 must be achieved for the smooth-Gaussian threshold (the binding, conservative bound) for a (level × bracket) cell to enter H3 confirmatory testing.

The framework adapts Carleton, Campbell & Collard (2018, *PLOS ONE* 13:e0191055; code CC-BY)'s PEWMA power-simulation framework for cross-sectional SPA × covariate analysis.

**Phase 2 — Bayesian mixture validation.**

*Confirmatory recovery simulation (H2.1).* Construct synthetic observed SPAs by combining: a *known genuine SPA* drawn from a pre-specified library of plausible shapes (smooth growth; smooth decline; rise-and-fall; multi-modal); a *known α* drawn from a pre-specified grid spanning the empirical pilot range; and a *known convention component* with tier weights drawn from the empirical posterior of a pilot fit. For each (genuine shape × α × tier weighting) cell, run the Bayesian mixture and record (a) whether the recovered posterior α̂'s 95 % CI covers the true α; (b) the Pearson r between the recovered posterior-median genuine SPA and the true genuine SPA. The model is validated if (a) ≥ 90 % of grid cells have correct coverage *and* (b) the average Pearson r across grid cells is ≥ 0.95. Either failure triggers an OSF amendment and model revision.

*Supporting consistency and robustness checks (H2.2 / H2.3 / H2.4)* on real LIRE data. Reported alongside the recovery-simulation results, but not as validation in their own right.

**Phase 3 — H3 substantive analyses.**

- **H3a:** Bayesian within-between negative-binomial regression as specified in §3 above. Confirmatory decision rule on the within-province population-attributable variance fraction stated in Field 3. OLS log-log reported alongside as descriptive comparator to Hanson, Ortman & Lobo 2017.
- **H3c:** (i) posterior contrast on continuous residuals (capitals vs non-capitals) — confirmatory rule P(contrast > 0) ≥ 0.95; (ii) Moran's I on continuous residuals at k = 5, 8, 10 — confirmatory rule Moran's I > 0 at *p* < 0.05 in ≥ 2 of 3 k values. Note H3c(i)'s posterior contrast on Bayesian quantities is preferred to a frequentist *t*-test on posterior summaries; the two inferential frameworks should not be mixed within a single test.
- **H3b (pre-specified exploratory; see also §5):** permutation-envelope deviation-detection at the Antonine probe (AD 165–180) and the Crisis-of-the-Third-Century probe (AD 235–284 inclusive, 50 years). Windows and subsets are pre-specified (see Field 3); effect-size magnitudes are not. Results reported descriptively against the project's standard brackets, with multiplicity noted; no Holm-corrected confirmatory family.

### 5. Exploratory analyses (pre-specified but non-confirmatory)

- **H3b deviation-detection at the Antonine probe** (AD 165–180) — pre-specified scope as in Field 3.
- **H3b deviation-detection at the Crisis-of-the-Third-Century probe** (AD 235–284 inclusive, 50 years) — pre-specified scope as in Field 3.
- **CPL knot-sensitivity analysis (Phase 1 supplementary).** For each CPL cell in the Phase 1 simulation, fits k ∈ {2, 3, 4} and records AIC + detection per k. Reports threshold at each fixed k and the max−min range as a diagnostic. Non-confirmatory; supplementary material.
- **CPL AIC-select threshold (Phase 1 supplementary).** Per-iteration picks k with minimum AIC from {2, 3, 4}; reconstructs threshold under AIC-select decision rule (cf. Timpson et al. 2021). Reports what AIC-select would have given; does *not* substitute for the fixed-k = 3 confirmatory result.
- **Stratified-sampling sensitivity (Phase 1 supplementary).** Phase 1 thresholds use bootstrap (sampling-with-replacement) from filtered LIRE; thresholds are recomputed using stratified-sampling (province-proportional or city-proportional draws). Reports deltas to bootstrap primary.
- **Temporal "habit-removed residual trajectory" analysis.** SPA's chief advantage over Hanson's point-estimate population data is that it produces a *time series* per city. The naive comparison (does a city's SPA peak match its independently-known demographic peak?) is confounded by the empire-wide epigraphic habit's own temporal shape. To control for the habit: decompose each city's SPA trajectory into an *empire-wide habit component* plus a *city-specific residual trajectory*, and validate the residual against independent temporal evidence. Anchor types, in priority order:
  - **Foundation dates** — applied corpus-wide; well-attested in standard references; a colony founded in AD X should show ~ zero SPA mass before AD X.
  - **Independent peak-population dates** — assembled for a bounded case-study set only; compared as posterior-CI calibration (does the independent date fall within the posterior peak-time credible interval).
  - **Multi-point independent trajectories** — for the few well-studied cities where they exist; full-shape comparison (overlapping the small-N "Layer B validation gate" item below).
  - **Ordinal flourishing-era rankings** — where absolute dates are unavailable; rank-correlation of SPA-peak order against independent ordinal knowledge.

  A *systematic* offset between city-specific inscription peaks and independent demographic peaks is reported as a quantitative estimate of the *epigraphic-habit lag* — a methodological finding, not a failure. The analysis is exploratory throughout: no pre-committed thresholds; the independent-anchor evidence is too sparse and uncertain to bind. Scope is explicitly bounded: foundation dates corpus-wide, plus a deliberately time-boxed case-study set for richer anchors; comprehensive independent-date assembly is deferred to a follow-up paper.

- **City-level temporal trajectory estimation for small-N cities.** The Phase 1 confirmatory eligibility threshold (≈ 1,549 inscriptions for 50 %-over-50-years detection at urban-area level; see §6) restricts H3b urban-area deviation-detection to a handful of the largest cities. The remaining ~ 800 Hanson-matched cities have inscription counts below the confirmatory threshold but are not analytically inert — Bayesian aoristic estimation with explicit uncertainty propagation can produce trajectory-shape estimates from corpora as small as N ≈ 50 (cf. Crema 2025 baorista; Crema & Bevan 2021).

  **Core (Layer A) — temporal trajectory shape estimation.** For each Hanson-matched city, compute a posterior distribution over time-binned inscription density via a Bayesian hierarchical model (ICAR prior for temporal smoothing; partial-pooling toward province-level mean trajectory; aoristic uncertainty propagated per inscription). Report per-city posterior trajectory shape with 95 % credible intervals. Estimation, not hypothesis testing.

  **Extension (Layer B) — tentative inversion to time-varying population.** Under the assumption that the cross-sectional β-scaling estimated from H3a holds within-city over time, invert each city's trajectory to an illustrative time-varying population estimate: `pop_t ≈ pop_max × (insc_t / insc_max)^(1/β_within)`. Strong assumption flagged: within-city β stability over time is only approximately true. Reported as illustrative comparative-shape outputs only — *not* as quantitative population claims.

  **Aggregate diagnostic.** Posterior precision vs N (median CI width binned by N); trajectory-shape clustering; Layer B validation gate at independently-dated cities (Pompeii AD 79, Ostia c. AD 250, etc.). A negative result is itself a methodological contribution.

  **Province-scale extension.** Same methodology at province scale (~ 50 provinces) as a parallel methodological output, with substantive provincial-prosperity reconstruction deferred to a planned follow-up paper.

- **Stratified-by-convention-class SPA** as a real-data internal-consistency check on the Bayesian mixture (overlapping H2.4; reported separately for transparency).

- **`baorista` Bayesian aoristic comparison** (Crema 2025) on representative provincial subsets. baorista — with NIMBLE, brms, and cmdstanr — is installed and smoke-validated on the project's compute server (see §8); the comparison runs as an appendix figure with accompanying discussion, providing a Bayesian-aoristic cross-check on the frequentist permutation-envelope results.

- **Scaling-residual sensitivity analysis for H3a:** compute per-city residuals from a fitted power-law `inscriptions ∝ population^β`; re-run H3a on residuals. Tests whether the Hanson-population correlation survives scaling-controlled analysis.

- **α-as-translator sensitivity analysis for H3a:** include per-city posterior mixture α as an additional covariate in the NBR; test whether the within-province β estimate shifts meaningfully. Informs whether the Hanson correlation is confounded by epigraphic-habit intensity.

- **Chronological resolution of H3c urban-area residuals:** extend Hanson's (2021) time-pooled residual analysis by computing residuals per decadal period. Exploratory because no published comparator exists.

- **Information-infrastructure versus complexity-markers theoretical framing.** The paper presents both readings of what inscription production proxies — Hanson's (2021) "information infrastructure" and the alternative reading of inscriptions as markers of socio-political complexity — and discusses the evidence bearing on each, rather than adjudicating between them. Feedback from presenting the work at RAC-TRAC 2026 is treated as critique to inform further exploration of both readings, not as the deciding word on which is correct. This theoretical-framing exploration is exploratory by intent; no preregistered hypothesis turns on which framing is correct.

- **Letter-count alternative analysis.** Per subset, repeat the H3 analyses using summed conservative letter counts (the `clean_text_conservative` field — Latin A–Z characters only, Greek excluded) in place of inscription counts. The rationale is a deliberate methodological disagreement with Hanson (2021). Hanson identifies the total volume of lettering as a methodologically desirable measure but rejects it as impractical, because so many inscriptions are fragmentary that their original lengths cannot be estimated (Hanson 2021, p. 142). We — with the LIRE team — take the opposite view: a flat inscription count implicitly treats a long monumental text and a three-word funerary fragment as equivalent units, when they plainly are not, and letter count, for all its preservation problems, at least registers something of the quantity of information an inscription carried. Letter count is treated as the lesser of two evils, not a problem-free measure, and reported as a cross-check on the inscription-count results rather than a replacement for them. The `clean_text_conservative` variant is used in preference to the interpretive variants because the interpretive text incorporates modern editorial restorations and expansions — exactly the kind of editor-dependent variation the deconvolution-mixture model exists to remove — whereas the conservative text counts only what survives; `clean_text_interpretive_word` is available as a sensitivity check. The analysis carries forward an exploratory observation from the project's 2024 seminar work, where a Negative Binomial model on letter counts produced a strikingly high pseudo-R²; that result was flagged at the time as "too good to be true" and a suspected artefact of the count model's dispersion structure, and is revisited here with the corrected pipeline.

### 6. Effect-size pre-specifications (summary)

| Hypothesis | Quantity | Preregistered target |
|---|---|---|
| **Confirmatory** | | |
| H2.1 (recovery simulation) | Coverage on true α | ≥ 90 % of grid cells have the true α inside the posterior 95 % CI of α̂. |
| H2.1 (recovery simulation) | Mean genuine-shape recovery | Mean Pearson r ≥ 0.95 between recovered and true genuine SPA across grid cells. |
| H3a primary | Within-province population-attributable variance fraction | Posterior 95 % CI of `Var(β_within · within_pop) / Var(log E[insc])` excludes 0.10. |
| H3c (i) | Capitals contrast | P(mean_residual(capitals) − mean_residual(non-capitals) > 0) ≥ 0.95. |
| H3c (ii) | Moran's I on residuals | > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} k-NN weights. |
| **Supporting consistency (real data, Phase 2)** | | |
| H2.2 | Corrected midpoint vs neighbourhood | Corrected `genuine_SPA` at each century midpoint within 1.5× of mean over ±25-year neighbourhood (excluding midpoint bin); sensitivity at ±5y shoulder-exclusion, ±15y and ±35y widths reported alongside. |
| H2.3 | Pairwise Pearson r across threshold variants | r ≥ 0.9 between any two threshold-filtered `genuine_SPA` variants. |
| H2.4 | Stratified-by-convention-class SPA vs deconvolved | Agreement within sampling error (continuous discrepancy reported; no binary threshold). |
| **Completed groundwork (Phase 1, fixed; not confirmatory)** | | |
| Phase 1 power floor | Detection rate | ≥ 0.80 at *p* < 0.05 per bracket; zero-effect false-positive rate ≤ 0.05 (achieved across all 96 zero-effect calibration cells, range `[0.007, 0.049]`). |
| Phase 1 thresholds (50 % over ≥ 50 y) | min n at detection ≥ 0.80 | **province** exp-step 1938, exp-gauss 1869, cpl-3-step 1385, cpl-3-gauss 1618; **urban-area** exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549; **empire** reachable at n = 50,000. |
| Phase 1 thresholds (doubling over ≥ 25 y) | min n at detection ≥ 0.80 | Gaussian shape: empire reachable at n = 50,000; province exp 2118, cpl-3 1934; urban-area exp 2160, cpl-3 1905. Step shape unreachable across all levels. |
| Phase 1 thresholds (20 % over 25 y; hard-test boundary) | min n at detection ≥ 0.80 | Empire / cpl-3 / Gaussian reachable at n = 50,000 (single marginally-reachable cell); all other combinations unreachable. Bracket retained as honest-uncertainty anchor; not in the H3b family. |
| **Pre-specified exploratory** | | |
| H3b Antonine probe | Deviation at AD 165–180 | Permutation-envelope departure at empire, Asclepius-cult, and military subsets; reported descriptively against project brackets; no pre-committed magnitude. |
| H3b Crisis-of-the-Third-Century probe | Deviation at AD 235–284 (50 y inclusive) | Permutation-envelope departure at empire and Western-Empire-provincial subsets, conditional on Phase 1 reachability; reported descriptively against project brackets; no pre-committed magnitude. |

### 7. Planned deviations and contingencies

- **Levels at which Phase 1 did not establish a finite detection threshold** within the swept sample-size range are dropped from confirmatory testing at that level (and from H3b exploratory testing on the relevant subsets) and may optionally be retained in the paper as exploratory. Phase 1 is complete; §6 gives the resulting thresholds and the levels they make eligible.
- **If the recovery-simulation validation fails** (either coverage or shape-recovery), an OSF amendment is filed and the Bayesian mixture is revised before any Phase 3 analysis runs. Likely revisions: re-parameterisation of the convention tier weights; smoothness prior on the genuine component; alternative tier composition.
- **If the pymc / brms shadow posteriors disagree beyond Monte Carlo noise** on H3a's confirmatory quantities, the cause is investigated; a material disagreement triggers an OSF amendment before final results are lodged.
- **If posterior or prior predictive checks fail** for H3a, the model is revised (priors, link function, or model structure) and the revision is recorded in the change log; an OSF amendment is filed.
- **If the LIST swap completes during the fortnightly paper sprint (11–24 May 2026),** the analytical envelope extends to AD 600 and Late Antique subsets are added; otherwise the LIRE envelope remains primary.
- **If substantive methodology changes are required after lodgement** — whether prompted by co-author input, the planned statistician consultation, the planned cross-model adversarial review, or anything else — an amendment to this preregistration is filed on OSF before implementation.

### 8. Software, reproducibility, and data access

- **Language:** Python 3.13 for the primary pipeline; R 4.4.3 for the `brms` shadow validation of the H3a model and for the baorista comparison.
- **Environment:** `uv`-managed Python virtual environment with a pinned `requirements.txt`; the R packages are installed on the project's compute server.
- **Core dependencies (Python):** `numpy`, `scipy`, `pandas`, `pyarrow`, `matplotlib`, `joblib`, `statsmodels`, `libpysal` (spatial weights for Moran's I), `pymc` (Bayesian mixture and H3a NBR), `pyzotero`, `requests`, `python-dotenv`. `cmdstanpy` is also installed as a fallback sampler backend but is not on the H3a NBR's critical path (pymc uses its native NUTS implementation).
- **Aoristic resampling implementation note:** the Uniform aoristic method is implemented directly in `primitives.py::aoristic_resample` as ≤ 10 lines of numpy. The SDAM `tempun` package (MIT; PyPI 0.2.4) was not used, because its current release is incompatible with numpy ≥ 2.4 (it calls the removed `numpy.trapz`); the direct implementation is mathematically equivalent under the Uniform aoristic distribution. An upstream issue has been filed to `sdam-au/tempun`; if `tempun` becomes numpy-2-compatible, it may be reintroduced for the H2 / H3 pipelines.
- **R dependencies (shadow validation and baorista comparison; not on the critical path for the primary Python results):** R 4.4.3, `cmdstanr` 0.9.0, `nimble` 1.4.2, `baorista` 0.2.1, and `brms` 2.23.0, with `posterior`, `bayesplot`, `loo`, and `arrow`. All installed and smoke-validated on the project compute server.
- **Data:** LIRE v3.0 (Zenodo DOI 10.5281/zenodo.8147298; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) as a ground-truth cross-check for `urban_context_pop_est`.
- **Subset-filter feasibility (confirmed on LIRE v3.0).** Military-administration subset: `type_of_inscription_clean == 'military diploma'` yields 285 rows (66.4 % null in that field; the ML-classified `type_of_inscription_auto` yields 442 rows at 13.8 % null and is a valid alternative). Asclepius-cult subset: regex `[Aa]esculap|[Aa]sclep` on the `inscription` free-text field yields 358 rows — substantially above Glomb, Kaše & Heřmánková's (2022) N = 210, suggesting their filter was stricter. The preregistered Glomb-replication test will either adopt their exact filter (if recoverable from their published methods) or use the broader keyword match and report both N values.
- **Code:** the project repository is public at `github.com/saross/inscriptions`. Phase 1 simulation code, the canonical random seed (20260425), and all simulation outputs (FP-calibration results, threshold tables, power curves, heatmaps) are committed to the public repository, providing end-to-end reproducibility from raw data to thresholds.
- **Run artefacts:** each analysis stage is captured in a per-stage `runs/<date>-<description>/` directory recording its specification, agent briefs, random seed, code, outputs, and decisions.
- **Pre-lodgement state of substantive analyses.** As of lodgement, no confirmatory analysis preregistered here has been executed on LIRE v3.0. Prior exploratory regressions of inscription and letter counts against Hanson (2016) urban population estimates (frequentist OLS, NBR-GLM, robust, and related models with bootstrap intervals) were carried out on LIRE v3.0 in the project's exploratory notebooks; those results are documented in the project repository and inform the prior expectations cited here, but are not themselves confirmatory tests of these preregistered hypotheses.
- **Research record:** agent-session-capture infrastructure is operational; individual AI-agent prompts and outputs are preserved per open-science requirements.

### 9. Known limitations (preregistered)

- **Editorial-convention artefact identification.** The Bayesian mixture addresses endpoint rounding at inclusive-Roman century boundaries, century-midpoint mass, half-century rounding, and the small set of dynastic-transition years where the descriptive profiling identified Holm-significant endpoint clustering. Other documented LIST / LIRE artefacts — province-label anachronism (Heřmánková, Kaše & Sobotková 2021, §29; EDH anchors province labels to mid-2nd-century Roman geography), EDCS coordinate imprecision (§60), 50 % missing coordinate provenance (§45) — remain as interpretive caveats. The preregistration commits to transparent reporting of these, not to methodological correction.
- **Single-dimension complexity (Turchin et al. 2018).** The multi-factor complexity decomposition in the paper's theoretical frame operates at city / province × decadal scale; Turchin's "single latent dimension" operates at polity × century scale. Different scales; the paper acknowledges this but does not attempt empirical disaggregation of the non-population dimensions.
- **Identifiability of complexity dimensions.** With inscription count as the sole observable and Hanson population as the sole external covariate, dimensions 2–6 of the complexity decomposition (economic prosperity, social differentiation, cultural translator, ideology, residual) remain theoretically present but empirically entangled in the residual variance and in the between-province component of the H3a regression. The paper acknowledges this as a scope limitation; disaggregation is left to future work.
- **Between-province population effect not separately identifiable.** The H3a within-between specification cleanly identifies the *within-province* population effect (orthogonal to province membership), but the *between-province* component is entangled with `α_province` — i.e. with province-level "everything else." The between-province population gradient is reported but explicitly flagged as not separable from province-level cultural, administrative, and survival-bias variation.
- **Rome exclusion.** Rome is excluded from scaling regressions as an extreme outlier. Consistent with Hanson (2021) methodology; reported transparently; not tested as a sensitivity.
- **Chronological envelope.** 50 BC – AD 350 (LIRE); extensible to AD 600 conditional on LIST swap. Late Antique and post-AD-600 phenomena out of scope for this paper.

### 10. Hypothesis-level structure summary

```text
Phase 1 (completed groundwork)        Phase 2 (Bayesian mixture)       Phase 3 (population analyses)
-----------------------------         ----------------------------     -------------------------
detection thresholds fixed in §6  →   H2.1 recovery-sim validation  →  H3a within-between NBR
(not a confirmatory hypothesis)       (confirmatory)                   variance partition (confirmatory)
                                      H2.2 / H2.3 / H2.4 supporting    H3c capitals + Moran's I (confirmatory)
                                      consistency checks (real data)   H3b exploratory deviation-detection
                                                                       at Antonine and Crisis probes
```

### 11. Provenance

- **Preregistration drafted** by Claude Code (Anthropic, Opus 4.7) under Shawn Ross's direction.
- **Authors and contributions (CRediT taxonomy):**
  - Shawn Ross (Macquarie University) — Conceptualization, Methodology, Investigation, Writing – original draft, Writing – review & editing, Supervision, Project administration.
  - Adela Sobotková (Aarhus University) — Methodology, Validation, Writing – review & editing.
- **AI contributions:** theoretical-frame refinements (identifiability scope, the scaling-residual sensitivity flag, the cultural-translator confound strategy), articulation of the deconvolution-mixture model, the temporal "habit-removed residual trajectory" framing, and this preregistration draft. All substantive AI intellectual contributions are logged in the project repository.
- **Funding:** no funding was received for this work.
- **Competing interests:** the authors declare no competing interests.
- **Ethics:** this work reanalyses publicly available, published datasets and did not require ethics review.
