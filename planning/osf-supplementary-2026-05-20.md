# Preregistration — supplementary detail

**Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population estimates: a preregistered three-phase analysis.**

*Supplementary document accompanying the OSF preregistration. Title and overall description are entered into the corresponding OSF form fields; this file contains the full research-questions, methodology, sensitivity, limitations, provenance, and references content.*

---

## 1. Research questions and hypotheses

### Primary research question

After applying a 50 BC – AD 350 date-window filter to constrain the date-attribution artefact, what fraction of the **within-province** spatial variation in Latin inscription production during the Roman Empire is accounted for by urban population dynamics?

### Secondary research questions (descriptive context — not confirmatory hypotheses)

(SR1) Does the present analysis, operating on date-window-filtered cross-sectional counts for the scaling comparison, reproduce the sublinear inscription-vs-population scaling pattern reported by Hanson (2021, mean exponent β = 0.672, 95 % CI [0.588, 0.756] in site-level cumulative inscription counts across 554 sites with Rome excluded) and for elite-honorific subsets by Carleton et al. (2025, β ≈ 0.3–0.5 across the monument and headline-epigraphy analyses, with an epigraphy-no-zeros variant at β ≈ 0.68)? The OLS log-log coefficient reported alongside the H3a Bayesian within-between NBR (see §4) is the direct comparator.

(SR2) Do urban-area residuals from the date-filtered regression reproduce two further findings of Hanson (2021): (i) that provincial capitals over-produce inscriptions relative to the scaling expectation (Hanson 2021, p. 148: mean residual 0.43 for provincial capitals vs ~0.06 for *coloniae* / *municipia*); and (ii) that residuals are spatially clustered (Hanson 2021, Table 7.4: Moran's I = 0.046, z = 4.571, *p* < 0.0001 for residuals; I = −0.006, *p* = 0.282 for raw counts)?

### Completed methodological groundwork (Phase 1)

Phase 1 was a simulation-based determination of minimum-sample-size thresholds for permutation-envelope deviation-detection across the H3 analysis levels (empire, province, urban-area). It is not a confirmatory hypothesis with a live decision rule; the simulation is complete, the thresholds it produced are reported in §7, and they gate which (level × subset) combinations are eligible for Phase 3 confirmatory testing. Full pipeline (code, fixed random seed 20260425, parametric grid, results) is committed to the public project repository for end-to-end reproducibility.

### Confirmatory hypotheses (Phase 2 and Phase 3)

**H2 — Bayesian mixture-model validation via recovery simulation.**

H2.1 (recovery simulation, confirmatory): synthetic observed SPAs are constructed from a known genuine SPA + known α + known convention component, across a pre-specified parametric grid whose axes are committed in this preregistration and whose specific values are pinned in a pre-Phase-2 design artefact (committed before any recovery simulation runs). The Bayesian mixture is judged validated if **(i) ≥ 90 % of grid cells achieve per-cell coverage** — defined as ≥ 90 % of the cell's replicates producing a posterior 95 % credible interval for α that contains the known true α — **and (ii) the posterior-median Pearson r between recovered and known genuine-SPA shape is ≥ 0.95 in ≥ 90 % of cells.** Either failure triggers an OSF amendment and model revision before any Phase 3 analysis. Cell-wise results are reported in addition to global pass-rate.

**H3 — Population signal.**

H3a (primary confirmatory quantitative result; within-province population-attributable variance fraction): a Bayesian within-between (Mundlak) negative-binomial regression of **date-window-filtered** inscription counts on Hanson (2016) urban population, splitting `log(population)` into a province-mean component and a city-level within-province deviation, yields a *within-province population-attributable variance fraction* `f_within`. The estimand is `Var(β_within · (log_pop − log_pop_province_mean)) / Var(log E[insc])` on the latent (log) scale, computed per posterior draw and reported as a posterior distribution. The confirmatory decision rule is three-way:

- **Supported:** posterior 95 % credible interval for `f_within` lies wholly above 0.10.
- **Evidence against:** posterior 95 % credible interval lies wholly below 0.10.
- **Inconclusive:** posterior 95 % credible interval straddles 0.10.

Supplementary reporting (binding alongside the verdict): the full posterior of `f_within`, plus P(f_within > 0.05), P(f_within > 0.10), and P(f_within > 0.20) as a posterior-probability ladder.

H3c (Hanson 2021 residual replication; two-part confirmatory). Residuals are **Pearson residuals** from the H3a posterior; for posterior draw *s* and city *c*:

```text
r_c,s = (y_c − μ_c,s) / sqrt(μ_c,s + μ_c,s² / φ_s)
```

where μ_c,s is the full city-level posterior mean on draw *s* (including the province random intercept) and φ_s is the posterior overdispersion parameter draw.

- H3c(i) — provincial-capital residuals: per posterior draw *s*, compute `contrast_s = mean(r_c,s | c ∈ provincial_capitals) − mean(r_c,s | c ∉ provincial_capitals)`; the rule is `P(contrast > 0) ≥ 0.95` (posterior probability over draws).
- H3c(ii) — spatial clustering: Moran's I is computed on the posterior-mean Pearson residual vector `r_c = (1/S) Σ_s r_c,s` with k-NN row-standardised spatial weights at k ∈ {5, 8, 10}; conditional permutation inference (999 permutations) per k. The rule is **Moran's I > 0 at *p* < 0.05 in at least two of the sensitivity series {k = 5, k = 8, k = 10}**. Supplementary: the posterior distribution of Moran's I across draws (per k), reported as 2.5 / 50 / 97.5 percentiles. A **three-case interpretive guardrail** governs the paper's reporting language: a result that passes the rule is described as **clean replication** if the posterior distribution of `I_s` at primary k = 8 shows ≥ 95 % of draws above 0, **permutation-significant but posterior-sensitive** if the 95 % posterior interval of `I_s` crosses zero, and **not substantively supported** if the posterior is centred near zero (< 50 % of draws above 0) — see §4 for the full spec. No regional-pattern map-match clause.

### Confirmatory claim hierarchy

The confirmatory claims this preregistration commits to are judged independently, not as an omnibus family:

- **H2.1** is a gate for using the mixture model. H2.1 failure triggers model revision and an OSF amendment before any Phase 3 analysis runs; the original mixture specification and the revised specification are both reported.
- **H3a** is the sole primary confirmatory quantitative result. Its three-way verdict (supported / evidence against / inconclusive) is the paper's headline finding.
- **H3c(i)** (capitals over-produce) and **H3c(ii)** (residuals spatially cluster) are each separate Hanson-replication confirmatory tests, judged independently. No omnibus "H3c was supported" claim is made; the paper reports the verdict on each part.
- **H3b** (pre-specified exploratory deviation-detection at the Antonine and Crisis probes) is *not* in the confirmatory family — its windows and subsets are pre-specified, but no effect-size magnitudes are pre-committed and no Holm-corrected confirmatory family is formed.
- If H3a returns "evidence against," H3c is still reported as Hanson-replication; the paper's headline becomes "H3a evidence against the non-trivial-share claim; H3c results reported descriptively."

### Pre-specified exploratory analyses (not confirmatory)

**H3b — pre-specified exploratory deviation-detection.** Mixture-corrected SPAs are scanned at pre-specified historical windows on pre-specified subsets, against the project's permutation-envelope machinery. Specifically:

- **Antonine probe (AD 165–180):** tested at empire level, at an Asclepius-cult subset (replicating Glomb, Kaše & Heřmánková 2022 on artefact-corrected data at larger N), and at a military-administration subset (replicating Duncan-Jones 2018-style severe-effect prediction), conditional on per-subset Phase 1 reachability.
- **Crisis-of-the-Third-Century probe (AD 235–284 inclusive, 50 years under inclusive-Roman counting):** tested at empire level and at a Western-Empire provincial subset (operationally defined in §3 as `province_language == 'Latin' AND province != 'Roma'`), conditional on Phase 1 reachability.

No effect-size magnitudes are pre-committed for either probe — the empirical priors conflict (Glomb et al. 2022 found a null at small N; Duncan-Jones 2018, Fig. 4 / Table 7.1, found an abrupt cessation of military diplomas after AD 167, effectively a complete halt in that subcorpus until a single resumption in AD 177; the Crisis is a diffuse multi-decade decline). Results are reported against the project's standard effect-size brackets (50 % over ≥ 50 y; doubling over ≥ 25 y; 20 % over ≥ 25 y) descriptively, with multiplicity reported alongside, but no Holm-corrected confirmatory family is formed.

**Phase 2 real-data consistency and robustness checks** (supporting, not validation):

H2.2: the mixture-corrected `genuine_SPA` shows reduced editorial-template artefact — the corrected curve's plateau-step structure at the 1 BC / AD 1, AD 100 / 101, AD 200 / 201, and AD 300 / 301 century boundaries (visible in the uncorrected SPA at step magnitudes +1,159 / +96 / −547 / +180 respectively) is markedly reduced in the corrected curve. Reported quantitatively as the relative magnitude of each boundary step in corrected vs uncorrected SPA.

H2.3: `genuine_SPA` converges across date-range threshold filtering — Pearson r ≥ 0.9 between any two SPAs constructed from subsets filtered by `date_range` ≤ 25, 50, 100, 200, 300 years.

H2.4: stratified-by-convention-class SPA (hard classification: convention-anchored vs precise) recovers a SPA shape agreeing with the Bayesian mixture's `genuine_SPA` within sampling error. Reported transparently as an internal-consistency check, *not* an independent validation (the two methods share the same convention-vs-precise row classification).

---


## 2. Dataset and corpus

**Primary (and sole) dataset for this preregistration:** LIRE v3.0 (Kaše, Heřmánková & Sobotková, Zenodo DOI 10.5281/zenodo.8431452, 11 October 2023). 182,853 rows; 63 attributes in the released parquet. Two filter flags used below — `is_within_RE` and `is_geotemporal` — are **derived** at filter time rather than being native columns of the released parquet: `is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT NULL AND not_before ≤ not_after` (the row has a usable geographic and temporal locus); `is_within_RE := province IS NOT NULL` (the row is geo-located within a Roman province). Filtering with these derived flags plus a 50 BC – AD 350 date-interval intersect (overlap, not containment) yields **180,609 rows** (≈ 98.8 % of the pre-filter total). Pre-joined Hanson (2016) urban-population estimates are available as the `urban_context_pop_est` attribute at row level (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

No envelope extension to AD 600 is permitted under this preregistration. The LIST v1.2 corpus (same team, Zenodo DOI 10.5281/zenodo.10473706, 9 January 2024) extends the temporal envelope to 50 BC – AD 600 (sparser Late Antique coverage) and is a candidate dataset for either a post-lodgement OSF amendment or a follow-up paper; not part of this preregistration.

**Rome excluded** from all scaling regressions as an extreme outlier, following Hanson (2021, Table 7.3 caption) — methodologically consistent with prior published work. Rome alone contributes **65,435 inscriptions** to the filtered corpus: 36.2 % of the 180,609-row total, or 46.5 % of the 140,575 inscriptions assigned to a Hanson-catalogued city. The Rome-excluded corpus is therefore **115,174 inscriptions**. Excluding Rome removes a single data point that would otherwise dominate the scaling fit; the exclusion is reported transparently and is not tested as a sensitivity (see §10).

## 3. Subset levels and sample-size sweep

Subsets analysed at three levels, each with a minimum-inscription-count threshold fixed by the completed Phase 1 simulation (see §7):

- **Empire-wide:** all inscriptions meeting filters; primary level for temporal analyses (Rome excluded). Phase 1 swept empire-level n at 1,000 / 2,500 / 5,000 / 10,000 / 25,000 / 50,000 inscriptions.
- **Province:** ~50 provinces in LIRE. Threshold candidate values tested by simulation: 100, 250, 500, 1,000, 2,500, 5,000, 10,000, 25,000 inscriptions.
- **Urban area:** ~816 cities with Hanson population estimates. Threshold candidate values tested by simulation: 25, 50, 100, 250, 500, 1,000, 2,500 inscriptions.

The cross-city H3a Bayesian NBR uses *all* ~815 cities with Hanson population estimates after Rome-exclusion — the Phase 1 thresholds gate per-subset *time-series* analyses (H3b deviation-detection; the §6 small-N trajectory work), not the cross-sectional regression.

Date-range filtering thresholds examined for H2.3 robustness: `date_range` ≤ 25, 50, 100, 200, 300 years (matching the 2024 exploratory-notebook sweeps).

**Western-Empire ('Latin speaking') provincial subset (used by H3b's Crisis probe):** all LIRE v3.0 provinces where the project's `province_language` classification equals `'Latin'`, *excluding* the province `'Roma'`. The classification is taken from the project's prior exploratory work (`archive/2026-04-22-inscriptions-spa.ipynb` cell 54) and covers 41 LIRE provinces (after Rome-exclusion), including the Italian core ("Italia" plus the eleven Augustan regions), the Latin West (Gauls, Germanies, Britannia, Hispaniae, African provinces), and the Danube-and-frontier provinces (Noricum, Raetia, Pannoniae, Dalmatia, Dacia, Moesiae). The full list is committed to the public project repository (see §9); the three frontier-province classifications (Moesia Inferior, Moesia Superior, Sicilia) are flagged in §10 as bilingual-frontier judgement calls.

### Analysis pipeline — a plain-English walkthrough

*This subsection explains the analysis in plain terms. It is explanatory only: §4 below is the binding technical specification, and where the two appear to differ, §4 governs.*

**The problem.** Every Latin inscription in the corpus carries a *date range* — an earliest and a latest plausible year — rather than an exact date. We want to know two things: how inscription production varied across cities, and how far that variation is driven by city population. Two obstacles stand in the way. First, the dates are uncertain. Second, the dates are *systematically distorted* by editorial template encoding: epigraphic editors, faced with an inscription they can date only to a broad period, round its date range to a small set of standard *template intervals* — inclusive-Roman centuries ([1, 100], [101, 200], etc.), half-centuries ([125, 175] for "mid-3rd century"), and reign intervals ([117, 138] for "Hadrianic"). This template encoding is visible directly in the data: over half of all interval starts end in `01` and over half of all interval ends end in `00`. The corpus is dominated by these template intervals (the [1, 100] template alone accounts for 26 % of the corpus).

**Step 1 — from date ranges to a production curve (aoristic sampling and the SPA).** "Aoristic" — a term borrowed from criminology and archaeology meaning *"of indeterminate time"* — handles date uncertainty by spreading each inscription's "weight" uniformly across its possible date range, instead of pretending it has a single true date. Summing that spread weight across every inscription year by year produces a *summed probability analysis* (SPA), a curve estimating how much inscription production happened in each period. We compute the SPA on 5-year bins (so each point of the curve represents a 5-year window) — fine enough to see decadal structure, coarse enough to be stable. The SPA is the basic object every later step works on.

**Step 2 — removing the editorial-template artefact (the Bayesian mixture model).** The SPA we observe is a *blend* of two components: a "convention" component, produced by editorial template encoding (wide intervals deposit flat plateaus of mass; a [1, 100] inscription contributes equally to every year from AD 1 to AD 100); and a "genuine" component, reflecting the ancient pattern of inscription production. The mixture model formalises this as `observed = α × convention + (1 − α) × genuine`, where α is the share attributable to template encoding. We fit the model in a Bayesian framework — meaning we specify prior distributions on α, on the shape of the convention component, and on the shape of the genuine component, then update those priors against the observed SPA to obtain *posterior* distributions for all three. The posterior on the genuine component is the corrected curve; the posterior on α tells us how much of the observed SPA was template encoding. This deconvolution is the paper's central methodological contribution.

The convention component has explicit structure: a small dictionary of *template intervals* — centuries ([1, 100], [101, 200], etc.), half-centuries ([1, 50], [51, 100], etc., where empirically supported), and reign intervals (Augustan [27 BC, AD 14], Flavian [78, 79], Hadrianic [117, 138], Antonine [161, 180], Severan [212, 217], etc.). Each template deposits *uniform mass over its interval*. The Bayesian model estimates the weight of each template-type tier (century slab, half-century slab, reign-interval slab) and a single α. Year-precise inscriptions ([123, 123] — typically inscriptions that carry a consular date or imperial-titulature stamp) are not part of the convention component; they remain in `genuine_SPA` as real ancient anchoring. The Bayesian priors regularise the inverse problem — without them, deconvolution is ill-posed; with them, the data adjudicates each tier's weight.

Mechanically, the model treats the observed SPA as compositional shape data — the proportion of mass in each 5-year bin — and the binding observation model is multinomial. Two supplementary fits are reported alongside as model-comparison cross-checks: a Dirichlet-multinomial fit (which adds an overdispersion parameter, useful if bin counts have more variability than the multinomial allows for) and a rescaled negative-binomial fit (an alternative overdispersion treatment). The supplementary fits are not confirmatory comparators; the validation rule (Step 3) and all H3 substantive analyses attach to the multinomial primary.

**Step 3 — validating the mixture model (recovery simulation).** Before trusting the corrected curve, we need to know the model can actually recover known answers. We build a *recovery simulation*: we construct synthetic observed SPAs by combining a known genuine SPA, a known α, and a known convention component built from the template-interval slab structure described above, then run the Bayesian mixture on those synthetics and check it recovers the known α and the known genuine shape. The simulation runs many synthetic replicates per grid cell, so the validation criterion is proper *coverage* in the repeated-sampling sense: each grid cell must produce a posterior 95 % credible interval that contains the true α in ≥ 90 % of its replicates, AND the posterior-median Pearson r against the true genuine shape must be ≥ 0.95 in ≥ 90 % of cells. The grid axes (α range, shape library, tier-weight vectors, sample sizes) are pre-committed in this preregistration; specific values are pinned in a pre-Phase-2 design artefact at `runs/2026-05-XX-recovery-grid-design/` (committed before any recovery simulation runs). If the model fails the recovery test, we amend the preregistration and revise the model before doing any of the substantive analyses. The existing real-data consistency and robustness checks (does the corrected curve look right? is it stable across data subsets?) are supporting evidence, not validation in their own right.

**Step 4 — telling signal from noise (the permutation envelope).** Even a corrected curve wiggles. To decide whether a given wiggle is a real historical event or just noise, we build a "what noise alone looks like" band: we simulate many artificial datasets under a deliberately featureless model (smooth growth or decline, no special events), measure how much *those* curves wiggle, and check whether the real curve pokes outside the resulting band. Poking outside it indicates a deviation unlikely to be chance. The featureless models we use are *exponential growth* (a single parameter — the growth or decay rate) and *piecewise-linear with three knots* ("CPL-3" — three connected line segments, with the knot positions allowed to fit; flexible enough to capture rise-and-fall but rigid enough to be a clear null). The technical subtlety: the featureless model is fitted to the *date ranges themselves* (treating each row's `[not_before, not_after]` as the observation and integrating the model's density over the range), and the date-range uncertainty is then re-applied when generating simulated datasets. A more naive approach fitted the model on the already-uncertainty-spread observed SPA and then re-applied that uncertainty when simulating — double-counting the uncertainty, narrowing the noise band, and producing false alarms. The forward-fit approach corrects this and gives proper false-positive control.

**Step 5 — establishing what the method can detect (Phase 1, complete).** None of the above is worth running on a corpus too small for the method to see anything. So before the substantive work, we simulated: at each analysis level (whole empire, individual province, individual city), and for events of several sizes, how many inscriptions does a level need before the method reliably detects the event? Phase 1 is complete; the resulting thresholds (§7) fix which subsets are eligible for confirmatory deviation-detection.

**Step 6 — the population question (H3a, Bayesian negative-binomial regression).** With the date-window-filtered corpus in hand, we ask how far city population explains inscription production. Important scope: the H3a regression uses *date-window-filtered* inscription counts as its response — the Bayesian mixture's correction is applied to the temporal SPA analyses (H2.1 validation and H3b deviation-detection), not to the cross-sectional city counts. H3c (Step 7) inherits this scope, since H3c residuals are computed from H3a's posterior. A per-city mixture fit would be unidentified for the ~600 cities below N = 100 inscriptions. The regression is *negative-binomial* because inscription counts are far more variable than a simple count model would predict (they are *over-dispersed*), and *Bayesian* because that yields a full distribution of plausible values for every quantity of interest — which is where the analysis's uncertainty intervals come from. The regression splits each city's `log(population)` into two parts: a *province-mean* component (the average log-population of cities in the city's province) and a *within-province* component (how much the city's log-population deviates from its province's mean). Each gets its own coefficient. The split lets us identify a clean *within-province* population effect — "holding province constant, do bigger cities produce proportionally more inscriptions" — that is unconfounded with province-level differences in epigraphic culture, administrative structure, and survival-bias. The between-province effect is also reported but with an explicit caveat: it is not separately identifiable from "province-level everything else." This Mundlak ("within-between") specification is the standard solution in multilevel modelling when a city-level predictor varies between groups (cities cluster by province; provinces have systematically different city-size distributions).

The headline quantity is the **within-province population-attributable variance fraction** `f_within` — the proportion of the variance in `log E[inscriptions per city]` accounted for by the within-province component of `log(population)`. We pre-commit to the *estimand*, not to a specific numerical value: the confirmatory rule is three-way (the posterior 95 % CI lies wholly above 0.10 → supported; wholly below → evidence against; straddling → inconclusive). The paper additionally reports the posterior-probability ladder P(f_within > 0.05), P(f_within > 0.10), P(f_within > 0.20) regardless of the verdict.

**Step 7 — which cities break the pattern, and where (H3c, residuals and spatial clustering).** Finally, we look at the cities the regression gets *wrong* — those producing markedly more or fewer inscriptions than their population predicts (the residuals) — and ask two questions about them. The residual we use is the standardised *Pearson residual* (the field-standard NBR residual; it normalises for the mean-variance relationship), computed draw-wise on the posterior. First, do *provincial capitals* over-produce relative to other Roman city-statuses (replicating Hanson 2021's finding that capital residuals are markedly positive)? Computed as a posterior contrast: on each posterior draw of the Pearson residuals, we take the difference (mean over capitals) − (mean over non-capitals), and ask whether that difference exceeds 0 with posterior probability ≥ 0.95. Second, are the residuals *spatially clustered*? Computed as Moran's I — the standard test for spatial autocorrelation — on the *posterior-mean* Pearson residual surface (one residual per city, averaged across posterior draws), using nearest-neighbour spatial weights with sensitivity at k = 5, 8, and 10. We use posterior-mean residuals here, rather than draw-wise, so that the test retains the field-standard conditional permutation inference; the posterior distribution of Moran's I across draws is reported supplementarily for transparency. Hanson 2021 reported Moran's I = 0.046, *p* < 0.0001 for residuals (and Moran's I ≈ 0, *p* = 0.282 for raw counts, confirming the clustering is in the residuals, not in the base inscription count distribution). The confirmatory rule is Moran's I > 0 at *p* < 0.05 in at least two of the three k values.

**How the phases connect.** Phase 1 (completed groundwork) determines which (level × subset) combinations are eligible for Phase 3 deviation-detection. Phase 2 (Bayesian mixture validation) produces the corrected temporal signal used in Phase 3's temporal analyses (H3b deviation-detection). Phase 3 (H3a within-between regression + H3c residual analysis) answers the primary research question and the Hanson-replication secondary questions. The pre-specified exploratory H3b deviation-detection at the Antonine and Crisis-of-the-Third-Century windows runs alongside Phase 3 but is not gated by confirmatory testing — its windows and subsets are pre-specified but its effect-size magnitudes are not.

## 4. Analysis pipeline

- **Aoristic sampling:** the Uniform aoristic method — each inscription's probability mass spread uniformly over `[not_before, not_after]` — is the primary treatment. A trapezoidal distribution is run as a sensitivity analysis on **every (level × subset) combination eligible for H3 confirmatory testing** (i.e. every subset that clears the Phase 1 reachability threshold for the binding bracket), plus the full-empire SPA. The trapezoidal parameterisation: `edge_band = min(width / 4, 10 years)`; within the central plateau of width `width − 2·edge_band` the per-year mass is constant at density `1 / (width − edge_band)`; over each edge ramp (length `edge_band`) the per-year mass ramps linearly from 0 at the absolute interval edge to plateau density at distance `edge_band` from the edge. The trapezoid integrates to 1 exactly; for very short intervals (`width < 8`) the trapezoid degenerates to a triangular shape. Convergence between uniform and trapezoidal SPAs is assessed by Pearson *r* per subset; the sensitivity is deemed material in any subset where *r* < 0.95, in which case the trapezoidal SPA is reported alongside the uniform primary. The Uniform method is implemented directly in the project code (≤ 10 lines of numpy) rather than via the SDAM `tempun` package, whose current release (0.2.4) is incompatible with numpy ≥ 2.4; the direct implementation is mathematically equivalent to `tempun`'s Uniform aoristic method.

- **Binning:** 5-year bins across the analysis envelope. 5-year bins across the 50 BC – AD 350 envelope (80 bins). The 5-year resolution is set by the smallest preregistered event window — the Antonine probe (AD 165–180, 15 years) — for which bin width ≤ event-width / 3 is required for reliable Gaussian-tapered shape recovery. 5-year bins also cleanly resolve the editorial-template plateau-step boundaries documented in §3 (steps at AD 1, 101, 201, 301) without aliasing.

- **SPA construction:** sum of per-inscription probability mass across bins; optional weighting by `clean_text_conservative` letter count for the secondary letter-count analyses (see §6).

- **Permutation envelope:** an rcarbon-style `modelTest()` significance test (Crema & Bevan 2021), implemented in Python as a hand-rolled Monte Carlo envelope loop following Timpson et al. (2014). The loop samples Monte Carlo replicates from a fitted parametric null, computes a pointwise 95 % envelope, and evaluates a global *p*-value as the proportion of replicates with at least as many bins falling outside the pointwise envelope as the observed SPA. Two design choices are central:

  **The null is fitted in true-date space, not in aoristic-smeared SPA space.** The maximum-likelihood fit treats each row's `[not_before, not_after]` interval as the observation and integrates the parametric density `f(t; θ)` over the interval: `L_i(θ) = ∫_{nb_i}^{na_i} f(t; θ) dt / Z(θ)`. For the exponential null this has a closed form; for the CPL null it is per-segment trapezoidal integration. Fitting in true-date space means the date-range uncertainty is *not* absorbed into the fitted null.

  **Monte Carlo replicates are forward-aoristic-smeared.** Synthetic true dates are drawn from the fitted density `f(t; θ̂)`, paired with empirical `[not_before, not_after]` widths drawn from the bootstrap sample, positioned uniformly within the resulting interval, and aoristic-resampled once by a uniform draw within the interval. This produces Monte Carlo SPAs whose variance structure matches the observed SPA pipeline (bootstrap row → aoristic-resample → bin) under the null model. An alternative that fits the null on the already-smeared observed SPA and then re-applies aoristic widths was tested and rejected: it double-counts the date-range uncertainty (the fitted null is already smeared, because it was fit on smeared data), inflating the Monte Carlo envelope width and the false-positive rate. The forward-fit-in-true-date-space approach corrects this and recovers proper false-positive control — false-positive rates fall within `[0.007, 0.049]` across all 96 zero-effect calibration cells of the completed Phase 1 simulation (Cells > 0.05: 0 of 96).

  Null models: **exponential** (primary, per Timpson et al. 2014) and **continuous piecewise-linear with k = 3 knots** (CPL-3, secondary, per Timpson et al. 2021); 1,000 Monte Carlo replicates; two-sided 95 % envelopes. CPL with k = 3 is the *sole* confirmatory CPL null; CPL with k = 2 knots was tested in validation and excluded (systematic false-positive bias at high n on a 3-knot ground truth — structurally underfit), and CPL with k = 4 knots is retained as an exploratory upper bound for knot-count sensitivity only (k = 3 is AIC-best in 73 % of CPL iterations in the completed Phase 1 simulation; AIC-selected results are reported in supplementary material and do not substitute for the fixed-k = 3 confirmatory result).

- **Bayesian deconvolution-mixture model:** the observed SPA is modelled as a compositional mixture of a convention component (built from template-interval slabs) and a genuine component, with an explicit multinomial observation model.

  **Observation model (binding).** Let `m_t` be the raw per-bin aoristic-mass SPA on a 5-year grid for a given subset of N_eff inscriptions. Under per-year uniform aoristic each inscription contributes total mass 1 distributed across the bins its date range covers, so by construction `Σ_t m_t = N_eff` (modulo truncation at the analysis envelope). Define `q_t = m_t / Σ_t m_t` (the empirical SPA shape, summing to 1). Convert to integer counts by largest-remainder rounding: `y_t = lr_round(N_eff · q_t)` with the rounding scheme chosen deterministically so that `Σ_t y_t = N_eff` exactly (integer parts assigned, residual `N_eff − Σ_t ⌊N_eff · q_t⌋` units distributed to bins with largest fractional remainders, ties broken by bin index).

  Let `p_conv,t` and `p_gen,t` be non-negative vectors summing to 1 (normalised densities over the analysis envelope). Then

  ```text
  p_t = α · p_conv,t + (1 − α) · p_gen,t
  y ~ Multinomial(N_eff, p)
  ```

  is the binding primary likelihood. The compositional-shape interpretation is explicit: the model treats the SPA as a discrete count distribution over 5-year bins, with the integer-count vector `y` derived deterministically from the empirical aoristic mass before fitting. Two **supplementary fits** are reported alongside for model-comparison: (a) **Dirichlet-multinomial** — `y_t ~ DirichletMultinomial(N, κ · p_t)` with concentration `κ ~ HalfNormal(prior tuned on pilot fit)`, reducing to multinomial as `κ → ∞`; this handles bin-level overdispersion if the multinomial posterior-predictive dispersion check fails. (b) **Rescaled negative-binomial** — `y_t ~ NegativeBinomial(λ_t = N · p_t, φ)` with `1/φ ~ HalfNormal(1)`; the `λ = N · p_t` parameterisation avoids the scale-degeneracy that would arise if `λ_conv,t` and `λ_gen,t` were free on absolute scale. The supplementary fits are not confirmatory comparators; the H2.1 recovery validation and H3 substantive analyses all attach to the multinomial primary.

  **Aoristic-uncertainty sensitivity (supplementary).** The primary multinomial fit absorbs aoristic uncertainty upstream — each subset's empirical SPA `m_t` is computed deterministically from per-inscription uniform-aoristic mass, and a single SPA enters one mixture fit. The expectation is that per-inscription uniform aoristic averages out at the 5-year bin level for N_eff ~ 10^5 inscriptions (a Law-of-Large-Numbers argument); where wide template intervals dominate the corpus, this expectation's premises are weaker, so the assumption is tested by a supplementary analysis. **Procedure:** **N_MC independently-sampled aoristic SPA realisations** are constructed (N_MC ∈ [20, 50], pinned in the pre-Phase-2 design artefact). Each realisation samples one per-inscription latent date `t_i ~ Uniform(nb_i, na_i)`, bins those latent dates into the 5-year grid (yielding a different empirical SPA per realisation), and runs the **primary multinomial mixture fit** on the resulting SPA. The cross-realisation posterior of α — the union of all per-realisation posteriors on α, equally weighted across realisations — is reported alongside the primary single-SPA posterior. **Divergence flag (preregistered):** if the cross-realisation 95 % range on α exceeds 1.5× the primary single-SPA posterior 95 % CI width, this is reported as a material limitation of the upstream-aoristic choice in the paper. The aoristic-MC supplementary does not trigger an OSF amendment by itself; it is a preregistered sensitivity, not a confirmatory test. The supplementary is run only on the multinomial primary — the Dirichlet-multinomial and rescaled NegBin supplementaries above are not separately aoristic-MC'd.

  **Convention component (template-interval slab structure).** A dictionary of template intervals, grouped into tiers by template type:

  - **Century-slab tier:** uniform mass over `[1, 100]`, `[101, 200]`, `[201, 300]`, `[301, 400]`, and BC equivalents (`[−99, 0]`, `[−199, −100]`).
  - **Half-century-slab tier:** uniform mass over the empirically-supported half-century templates from the pre-Phase-2 dictionary-build scan (candidates include `[1, 50]`, `[51, 100]`, `[125, 175]`, etc.).
  - **Reign-interval-slab tier:** uniform mass over reign-interval templates from the same scan (candidates include Augustan `[−27, 14]`, Tiberian, Flavian `[78, 79]`, Trajanic, Hadrianic `[117, 138]`, Antonine `[161, 180]`, Severan `[212, 217]`).

  The dictionary contents are pinned by a pre-Phase-2 empirical scan committed to a named `runs/2026-05-XX-template-dictionary/` directory before the Bayesian mixture fits; the scan enumerates exact-match interval templates in the LIRE v3.0 corpus and includes any template with N ≥ a stated threshold. Within each tier, each template's mass is normalised to its template width; the tier-level weights are estimated jointly with α. Year-precise inscriptions (`[t, t]` encodings) are *not* in the convention component — they remain in `genuine_SPA` as real ancient anchoring.

  **Genuine component.** A smooth non-negative density over the analysis envelope, with a Gaussian random-walk smoothness prior and a weakly-informative bandwidth.

  **Priors.** `α ~ Beta(2, 2)` (centred at 0.5, weakly-informative); tier weights `~ Dirichlet(uniform)`; genuine-component smoothness `σ ~ HalfNormal(1)`.

  **Fit.** Posterior sampling via pymc (Hamiltonian Monte Carlo / NUTS) for the multinomial primary. The Dirichlet-multinomial and rescaled NegBin supplementaries are also fit in pymc. Convergence diagnostics: Gelman-Rubin R̂ < 1.01 on all parameters; effective sample size ≥ 400 per chain on α and tier weights; no divergences. Failure of any diagnostic triggers an OSF amendment.

  **Validation.** Recovery simulation per H2.1 (see §5): ≥ 100 replicates per cell; per-cell coverage rule on α (≥ 90 % of replicates' 95 % CIs containing the true α; ≥ 90 % of cells must pass); binding shape-recovery rule is Pearson r ≥ 0.95 between recovered posterior-median and true genuine SPA in ≥ 90 % of cells, with **Wasserstein-1 (Earth Mover's distance) reported as a supplementary distribution-sensitive shape metric** per cell against a design-artefact-pinned flagging threshold. The supporting consistency / robustness checks (H2.2 / H2.3 / H2.4) run on real data.

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

  **Response variable.** `y_c` is the per-city inscription count under the 50 BC – AD 350 date-window filter. The Bayesian mixture is *not* applied to `y_c`; mixture correction applies to the temporal SPA analyses (H2.1 validation and H3b deviation-detection). The H3c residual analysis (see below) is computed from this regression's posterior and inherits its date-filtered-count scope — it is *not* a mixture-corrected analysis. The mixture's empire-level posterior α is reported as descriptive context.

  **Predictor scaling.** `log_pop_c` is on the natural log scale; the within-province deviation `(log_pop_c − log_pop_province_mean[c])` and the province-mean `log_pop_province_mean[c]` enter the linear predictor unstandardised. Under this scaling, `Normal(0, 1)` on `β_within` and `β_between` is weakly-informative: it places ~ 68 % prior mass on |β| < 1, corresponding to multiplicative effects up to ~ 2.7× per unit-log-population deviation. Sensitivity to standardisation is reported as an exploratory check.

  The within-between (Mundlak / hybrid) specification gives a clean *within-province* population effect by construction: the within-province deviation `(log_pop_c − log_pop_province_mean[c])` is orthogonal to province membership, so its variance component is unambiguous and unentangled with `α_province`. The between-province effect `β_between · log_pop_province_mean[c]` is also reported but explicitly flagged as not independently identifiable from province-level "everything else" (see §10).

  **Sample.** All cities with Hanson population estimates, Rome excluded (~ 815 cities). The Phase 1 ≈ 1,549-inscription urban-area threshold gates per-city *temporal* analyses (H3b deviation-detection; the §6 trajectory work), not this cross-city regression.

  **Confirmatory estimand and decision rule (H3a).** The within-province population-attributable variance fraction on the latent (log) scale:

  `f_within = Var(β_within · (log_pop_c − log_pop_province_mean[c])) / Var(log E[inscriptions_c])`

  computed per posterior draw and reported as a posterior distribution. **Variance is computed unweighted across cities (Rome-excluded) for the binding primary `f_within`**; this is the version on which the three-way verdict below is computed. Two **supplementary weighted variants** — population-weighted (city weight `w_c = population_c`) and inscription-weighted (city weight `w_c = y_c`) — are computed as §6 pre-specified exploratory sensitivities and reported alongside the primary as full posterior distributions; they answer related but different substantive questions (what share of population-weighted, respectively inscription-weighted, log-count variance does within-province population explain?). The hypothesis verdict is three-way:

  - **Supported:** posterior 95 % credible interval for `f_within` lies wholly above 0.10.
  - **Evidence against:** posterior 95 % credible interval lies wholly below 0.10.
  - **Inconclusive:** posterior 95 % credible interval straddles 0.10.

  Supplementary reporting (binding alongside the verdict): P(f_within > 0.05), P(f_within > 0.10), P(f_within > 0.20) as a posterior-probability ladder.

  (The numerator is the within-province population contribution; the denominator is the total variance in the linear predictor on the log scale, computed on the same posterior draw to avoid scale ambiguity.) Reporting also includes Bayesian R² (Gelman, Goodrich, Gabry & Vehtari 2019; full-model latent-scale; cross-checked against `brms::bayes_R2`), the OLS log-log coefficient as a direct comparator to Hanson, Ortman & Lobo 2017, and the between-province component reported descriptively.

  **Prior predictive checks (numerical, per Decision 25 / §8).** Before fitting, simulate observed inscription counts from the prior alone (no data) and check that the simulated counts satisfy numerical thresholds pinned in the pre-Phase-2 design artefact (categories: prior 99th-percentile per-city count cap; tail-count bounds). The specific numerical thresholds are committed to the design artefact before any pilot fit is inspected.

  **Posterior predictive checks (numerical):**

  1. **Density overlay** (`arviz.plot_ppc`): posterior-predictive inscription-count distribution overlaid against the observed count distribution.
  2. **Test statistics** — observed vs posterior-predictive: proportion of zeros (NBR sanity check); mean (within X % of observed; X pinned in design artefact); standard deviation (within Y % of observed); 95th percentile (within tail-count bounds); mean-variance ratio (dispersion adequacy).
  3. **Residual structure** — standardised Pearson residuals vs fitted values and vs key predictors (within-province `log_pop` deviation, province); residual-vs-fitted slope below pinned threshold; province-level residual dispersion within pinned bounds.
  4. **Posterior-predictive spatial autocorrelation on H3a residuals** — for each posterior draw, compute `y_pred,c` per city; compute Pearson residuals of `y_pred,c` against `μ_c,s`; compute Moran's I on the resulting posterior-predictive residual surface with the same k-NN spatial weights as H3c(ii) (primary k = 8). Repeat across draws to obtain the posterior-predictive distribution of Moran's I. Trigger: observed Moran's I (from the H3c(ii) posterior-mean residual computation) lies outside the design-artefact-pinned range of the posterior-predictive I distribution (default: outside the 5th–95th percentile, with severity tiers per the response rule below). A tripped trigger here means the model is unable to generate the observed degree of residual spatial structure under its own posterior, and is reported with a tautology caveat in the H3c(ii) interpretation.

  **Failure response (two-tier severity).** A trigger's severity is judged against its design-artefact-pinned bound:

  - **Critical trigger:** PPC value lies outside the bound by > 2× the bound's magnitude (or, for trigger categories with directional bounds — e.g. residual-vs-fitted slope — the sign is unexpected). Response: model revision (priors, link, or structure); the originally-preregistered model result is reported alongside the revised model; an OSF amendment is filed before final results are lodged.
  - **Minor trigger:** PPC value lies outside the bound by ≤ 1.5× the bound's magnitude (tripped, but marginally). Response: reported as a caveat in the paper; no model revision required; no OSF amendment.

  The 1.5× / 2× cutoffs are straw values pinned per-category in the design artefact (they may differ across categories — e.g. proportion-of-zeros may warrant a tighter cutoff than tail-count). No PPC trigger is used to test a hypothesis; these are diagnostic checks on model fit, not confirmatory tests.

  **Primary implementation in `pymc`** (Python). **Secondary `brms`-via-R cross-validation shadow** (~ 50 lines, committed as `scripts/h3a_brms_shadow.R`): refits the same within-between model in R + Stan, providing (i) cross-language validation that pymc and brms agree on the posterior within Monte Carlo noise and (ii) legibility for R-native co-authors who read brms syntax more fluently than pymc code. The brms shadow's negative-binomial dispersion-prior parameterisation requires a small Jacobian adjustment to match pymc's preregistered `1/dispersion ~ HalfNormal(1)` prior; details (the `stanvar()` block and the Jacobian derivation) are committed in the script's docstring and supplementary material rather than reproduced here. If pymc and brms disagree on the posterior beyond Monte Carlo noise, the cause is investigated; if the disagreement materially affects H3a's confirmatory result, an OSF amendment is filed before lodging final results.

- **Residual analysis (H3c).** Per-city *Pearson residuals* are extracted from the H3a posterior. For posterior draw *s* and city *c*: `r_c,s = (y_c − μ_c,s) / sqrt(μ_c,s + μ_c,s² / φ_s)`, where μ_c,s is the full posterior mean for city c on draw s (including the province random intercept α_province[c]) and φ_s is the posterior overdispersion parameter draw. For descriptive purposes in the paper, cities are labelled "over-producing" / "under-producing" / "typical" when the observed count falls outside / inside the ±95 % posterior credible interval from predicted — this labelling is narrative only and does not gate any confirmatory decision rule.

- **Spatial clustering (H3c).** Moran's I with row-standardised spatial weights via *k*-nearest-neighbours (`libpysal.weights.KNN.from_dataframe`). **Primary k = 8** — Cliff & Ord 1981 on Moran's I in general; the k = 8 default for point data follows the k-NN convention codified by Anselin 1995 and subsequent spatial-econometrics literature; robust to the Empire's uneven site density. **Sensitivity at k = 5 and k = 10** reported alongside. The Moran's I confirmatory test runs on the **posterior-mean Pearson residual vector** `r_c = (1/S) Σ_s r_c,s` — one residual per city, averaged across posterior draws — with conditional permutation inference (999 permutations of `r_c` over fixed spatial weights) per k. This keeps the field-standard frequentist permutation procedure for spatial autocorrelation while making the posterior uncertainty visible via the supplementary reporting. Hanson (2021, Table 7.4) reported Moran's I = 0.046 on residuals (z = 4.571, *p* < 0.0001) and Moran's I = −0.006 on raw counts (z = −1.076, *p* = 0.282), using ArcGIS's default Spatial Autocorrelation tool (Hanson 2021, p. 145; weights construction unspecified — exact-numerical-match is not feasible). The confirmatory rule is **Moran's I > 0 at *p* < 0.05 in at least two of {k = 5, k = 8, k = 10}**. **Supplementary (binding):** the posterior distribution of Moran's I across draws (per k) — for each posterior draw s, compute I_s on `r_·,s`; report the 2.5 / 50 / 97.5 percentiles of I_s per k.

  **Three-case interpretive guardrail.** The decision rule above is unchanged; the guardrail governs the paper's reporting language for the case in which the rule passes:

  - **Case 1 — clean replication.** Rule passes AND the posterior distribution of `I_s` at primary k = 8 shows ≥ 95 % of draws above 0. Reported as: "the spatial-clustering finding replicates Hanson 2021 robustly, with posterior support."
  - **Case 2 — permutation-significant but posterior-sensitive.** Rule passes BUT the 95 % posterior interval of `I_s` at primary k = 8 crosses zero. Reported as: "the spatial-clustering finding is permutation-significant on the posterior-mean residual surface but sensitive to posterior uncertainty — not described as a clean replication of Hanson 2021."
  - **Case 3 — confirmatory rule passes without substantive support.** Rule passes AND the posterior distribution of `I_s` at primary k = 8 is centred near zero (< 50 % of draws above 0). Reported as: "the confirmatory rule passes but does not survive posterior-uncertainty diagnostics — H3c(ii) is **not** claimed as substantively supported." The result is reported with this explicit non-support framing rather than as a Hanson-replication finding.

  The case-classification thresholds (≥ 95 % of draws for Case 1; < 50 % for Case 3) are committed in this preregistration. The H3c(ii) reporting is additionally conditioned on the 8th PPC category above (posterior-predictive spatial autocorrelation on H3a residuals): a tripped 8th-PPC trigger imposes the further tautology caveat that the model is structurally underspecified for the spatial pattern observed.

  No "qualitative pattern matches Hanson's map" clause: a prior re-verification of Hanson 2021 (recorded in the change log) confirmed that Hanson does *not* identify a regional pattern in the residuals — on the contrary, he explicitly states "there does not seem to be any obvious pattern" (p. 147) and that sites from different regions are "evenly scattered" (p. 148). The Moran's I clustering finding is the only spatial-structural claim Hanson makes, and is the only one we replicate.

### Uncertainty quantification

Every quantity this preregistration commits to is reported with an interval. Because the analyses span frequentist simulation, frequentist model fitting, and Bayesian inference, the interval *type* differs by analysis — there is no single confidence-interval recipe that fits all of them.

| Analysis | Quantity | Interval method |
|---|---|---|
| Phase 1 (completed) | Detection rate per cell | Wilson score 95 % interval on the proportion of simulation iterations with *p* < 0.05 (n_iter = 1,000). |
| Permutation envelope (H3b) | The envelope itself | 2.5th / 97.5th percentiles of the Monte Carlo replicate distribution, per bin (pointwise 95 % envelope); significance via the Timpson et al. (2014) global *p*-value. The envelope *is* the uncertainty representation — no separate interval is computed. |
| H2.1 (recovery) | α, recovered genuine-SPA shape | Posterior 95 % credible interval on α per grid cell (Bayesian mixture); Pearson r between recovered and known genuine shape, reported as a posterior distribution. Coverage computed per cell across replicates (≥ 90 % of replicates' posterior 95 % CIs contain the true α). |
| H2.2 | Boundary-step reduction | Direct point estimate from the corrected `genuine_SPA`; reported per template boundary year. |
| H2.3 | Pairwise Pearson *r* across threshold-filtered SPAs | Nonparametric bootstrap percentile interval (rows resampled with replacement). |
| H3a | β_within, β_between, variance fraction, Bayesian R² | Posterior 95 % credible intervals, computed directly from the fitted posterior. Bootstrap is *not* used: the posterior distribution already represents the full uncertainty, and resampling a Bayesian fit would double-count it. |
| H3c (i) | Capitals contrast | Posterior 95 % credible interval on the draw-wise contrast; decision rule reported as P(contrast > 0). |
| H3c (ii) | Moran's I | Conditional permutation inference (999 permutations of posterior-mean Pearson residuals over fixed spatial weights) — the field-standard significance procedure for Moran's I — reported for each of k = 5, 8, 10. Supplementary: posterior distribution of I across draws (per k). |

Where an interval excludes (or includes) a preregistered threshold, that is the basis on which the corresponding hypothesis is judged supported, evidence-against, or inconclusive.

## 5. Pre-specified confirmatory and exploratory analyses

**Phase 1 — completed groundwork.**

Phase 1 has executed; the protocol-as-run is described here for the research record. For each combination of (subset level ∈ {empire, province, urban-area}; effect-size bracket ∈ {the three brackets — 50 %/≥ 50 y, doubling/≥ 25 y, 20 %/≥ 25 y — plus a zero-effect calibration check}; sample size n ∈ logarithmic sweep):

1. **Generate synthetic intervals from a specified ground-truth null.** For exponential ground truth, draw `n` true dates `t_i ~ Exp(b_null)` truncated to the analysis envelope `[-50, 350]`; for CPL ground truth, draw from the fitted CPL density. Pair each `t_i` with a width `w_i` drawn from the empirical width distribution of filtered LIRE; sample `u_i ~ Uniform(0, 1)`; construct `[nb_i, na_i] = [t_i - u_i · w_i, t_i + (1 - u_i) · w_i]`. This is the synthetic interval list for the iteration.
2. **Aoristic-resample** by drawing `y_i ~ Uniform(nb_i, na_i)` for each row; bin via `np.histogram` on 5-year edges. This is the synthetic SPA.
3. **Inject the effect** at the target magnitude and duration, with shape ∈ {step, Gaussian} per the effect-shape pre-specification (see below).
4. **Forward-fit the null** to the synthetic intervals via maximum-likelihood interval-integral (closed-form for exponential; per-segment trapezoidal for CPL k = 3 and k = 4); the fit recovers an estimate of `b_null` (or the CPL parameters), not the smeared SPA shape.
5. **Generate `n_mc = 1000` MC replicates** under the fitted null using the same forward-aoristic procedure, and compute the Timpson et al. (2014) global-*p* envelope test against the (effect-injected) synthetic SPA. Record detection at *p* < 0.05.
6. Repeat steps 1–5 a total of `n_iter = 1000` times per cell. Detection rate per cell = fraction with `p < 0.05`. The Wilson 95 % interval on a 0.80 detection rate at `n_iter = 1000` is approximately `[0.775, 0.823]` — adequate for threshold-setting.

**Zero-effect calibration cell count.** The grid contains 96 zero-effect calibration cells, decomposed by level: empire (6 cells; 1 representative n × 3 null variants {exp, cpl-k3, cpl-k4} × 2 shapes {step, gauss}); province (48 cells; 8 sample-size points × 3 null variants × 2 shapes); urban-area (42 cells; 7 sample-size points × 3 null variants × 2 shapes). Total 6 + 48 + 42 = 96. Full grid table in the run report at `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`.

**Detection threshold and the unreachable convention.** The cell-eligibility criterion is **detection rate ≥ 0.80** at the cell's *n*. Cells where the maximum *n* in the level's sweep gives detection < 0.80 are tagged `min_n_unreachable` rather than imputing a fictitious extrapolated threshold. The 20 %-over-25-years bracket is preregistered as a hard-test boundary anchoring the bottom of the power curve, and is **not** in the (exploratory) H3b family: it proved near-universally unreachable.

**Null model:** both **exponential** (primary, per Timpson et al. 2014) and **continuous piecewise-linear with k = 3 knots** (CPL-3, secondary, per Timpson et al. 2021) are fitted; results compared. CPL-3 is fixed a priori rather than AIC-selected per cell, to give a well-defined secondary threshold comparable across subsets.

**Effect shape for injection:** both **step-function** and **Gaussian-tapered** injected in parallel; thresholds reported as a range per bracket. The Gaussian's parametrisation is FWHM = bracket duration (a convention; binding thresholds inherit this choice). Detection rate ≥ 0.80 must be achieved for the smooth-Gaussian threshold (the binding, conservative bound) for a (level × bracket) cell to enter H3 confirmatory testing.

The simulation design is inspired by Carleton, Campbell & Collard's (2018, *PLOS ONE* 13:e0191055; code CC-BY) use of synthetic archaeological time-series with known effects to evaluate method recovery under chronological uncertainty; the present SPA permutation-envelope cross-sectional thresholding is project-specific.

**Phase 2 — Bayesian mixture validation.**

*Confirmatory recovery simulation (H2.1).* Construct synthetic observed SPAs by combining: a *known genuine SPA* drawn from a pre-specified shape library; a *known α* drawn from a pre-specified grid spanning the empirical pilot range; and a *known convention component* built from the template-interval slab structure with tier weights drawn from a pre-specified set of vectors. The specific values along each axis are pinned in a pre-Phase-2 design artefact at `runs/2026-05-XX-recovery-grid-design/` (committed before any recovery simulation runs; a separate artefact from the `runs/2026-05-XX-template-dictionary/` empirical-scan artefact referenced in §4, which pins the dictionary contents of the slab structure itself). The grid axes (prereg-binding):

- **α grid:** at least 5 values spanning the empirical pilot range, with corner cases (α near 0, α near 1) included.
- **Genuine-shape library:** at least 6 shapes covering {smooth growth, smooth decline, rise-and-fall, multi-modal, regnal-cluster (mirroring the empirical regnal-spike pattern), flat-baseline}.
- **Tier-weight vectors:** at least 5 vectors covering {uniform across tiers, century-heavy, reign-heavy, half-century-heavy, pilot-posterior-drawn}.
- **Sample sizes:** representative N values from empire, province, and urban-area levels (specific N's pinned from Phase 1's reachability map).
- **Replicates per cell:** ≥ 100. (Design-artefact default is 100; the artefact may pin a higher value at boundary cells, e.g. a two-stage variant running 50 across the full grid to identify failure regions and 200 at boundary cells.)
- **Seed policy:** cell-deterministic (seed = base_seed + cell_index).

For each (genuine shape × α × tier-weighting × N) cell, generate the cell's replicate datasets and run the Bayesian mixture (multinomial primary; Dirichlet-multinomial and rescaled-NegBin supplementaries reported alongside). For each replicate record: (a) whether the recovered posterior 95 % CI for α contains the true α; (b) the Pearson r between the recovered posterior-median genuine SPA and the true genuine SPA; (c) the **Wasserstein-1 (Earth Mover's distance)** between the recovered posterior-median and true genuine SPA. **A cell passes coverage** if ≥ 90 % of its replicates produce a posterior 95 % CI on α that contains the true α. **The mixture is validated** if (i) ≥ 90 % of cells pass coverage *and* (ii) the posterior-median Pearson r is ≥ 0.95 in ≥ 90 % of cells. Cell-wise results are reported in addition to the global pass-rate (a global mean obscures systematic failure in high-α or convention-adjacent cells). **Wasserstein-1 is reported as a supplementary distribution-sensitive shape metric** per cell, with a design-artefact-pinned flagging threshold; the Wasserstein-1 result is descriptive — it is not part of the binding validation rule, but it is reported alongside the Pearson r outcome for every cell to make localised mass-redistribution failures visible. Either binding failure mode (coverage or Pearson-r shape) triggers an OSF amendment and model revision.

An **aoristic-Monte-Carlo supplementary** is run on the **primary multinomial fit on real LIRE data** (not within the recovery simulation): N_MC independently-sampled aoristic SPA realisations (N_MC ∈ [20, 50], pinned in the design artefact) feed the mixture; the cross-realisation posterior of α is reported alongside the primary single-SPA posterior. A divergence flag is preregistered (cross-realisation 95 % range exceeds 1.5× the primary posterior's 95 % CI width → reported as a material limitation). The aoristic-MC supplementary is a sensitivity analysis on the upstream-aoristic assumption, not a confirmatory test — see §4 ("Aoristic-uncertainty sensitivity").

The same `runs/2026-05-XX-recovery-grid-design/` design artefact also pins the **numerical PPC thresholds** referenced in §4 and §8 (categories: prior 99th-percentile count cap; PP mean / std / tail-count / proportion-of-zeros bounds; residual-vs-fitted slope threshold; province-level residual dispersion bound; posterior-predictive Moran's I distribution bound), the **Wasserstein-1 flagging threshold** for H2.1 supplementary shape recovery, the **aoristic-MC N_MC value and divergence-flag threshold**, and the **two-tier severity cutoffs** (critical / minor) per PPC category. One artefact, several specification tables.

*Supporting consistency and robustness checks (H2.2 / H2.3 / H2.4)* on real LIRE data. Reported alongside the recovery-simulation results, but not as validation in their own right.

**Phase 3 — H3 substantive analyses.**

- **H3a:** Bayesian within-between negative-binomial regression on date-window-filtered counts as specified in §4 above. Three-way decision rule on the within-province population-attributable variance fraction stated in Field 3. OLS log-log reported alongside as descriptive comparator to Hanson, Ortman & Lobo 2017.
- **H3c:** (i) posterior contrast on draw-wise Pearson residuals (capitals vs non-capitals) — confirmatory rule P(contrast > 0) ≥ 0.95; (ii) Moran's I on posterior-mean Pearson residuals at k = 5, 8, 10 with conditional permutation inference — confirmatory rule Moran's I > 0 at *p* < 0.05 in ≥ 2 of 3 k values; supplementary posterior distribution of I per k reported. Note H3c(i)'s posterior contrast on Bayesian quantities is preferred to a frequentist *t*-test on posterior summaries; the asymmetric draw-wise / posterior-mean split between H3c(i) and H3c(ii) is intentional (the capitals contrast question naturally lives in posterior space; the Moran's I question retains the field-standard permutation procedure).
- **H3b (pre-specified exploratory; see also §6):** permutation-envelope deviation-detection at the Antonine probe (AD 165–180) and the Crisis-of-the-Third-Century probe (AD 235–284 inclusive, 50 years). Windows and subsets are pre-specified (see Field 3 and §3); effect-size magnitudes are not. Results reported descriptively against the project's standard brackets, with multiplicity noted; no Holm-corrected confirmatory family.

## 6. Exploratory analyses (pre-specified but non-confirmatory)

- **H3b deviation-detection at the Antonine probe** (AD 165–180) — pre-specified scope as in Field 3.
- **H3b deviation-detection at the Crisis-of-the-Third-Century probe** (AD 235–284 inclusive, 50 years) — pre-specified scope as in Field 3.
- **Hanson-population measurement-error sensitivity for H3a.** Re-run the H3a within-between NBR with a lognormal measurement-error model on the Hanson population predictor: `log_pop_c ~ Normal(log_pop_observed_c, σ_pop)` for σ_pop ∈ {0.1, 0.2, 0.3} (low / moderate / high measurement uncertainty). Report the posterior on `f_within` under each σ_pop. Material divergence from the primary H3a result (posterior 95 % CI on `f_within` shifts by more than 50 % of its primary-result width under any σ_pop) is flagged as a limitation in the paper; does *not* trigger an OSF amendment (this is a preregistered exploratory sensitivity, not a confirmatory test).

- **Three-weighting sensitivity for `f_within`.** The binding primary `f_within` (§4) is computed unweighted across cities — answering "what share of city-to-city *systematic variation* does within-province population explain?" The same primary RQ admits two related but distinct readings under different variance-denominator weightings: a **population-weighted** variant (city weight `w_c = population_c`, normalised so weights sum to N_cities) answers "what share of *population-weighted* log-count variance does within-province population explain?", and an **inscription-weighted** variant (`w_c = y_c`) answers "what share of *inscription-weighted* log-count variance?". Both numerator and denominator variances are computed with the same weights in each variant; both are computed per posterior draw and reported as full posterior distributions alongside the unweighted primary. **Material divergence:** if the spread across the three weighted variants exceeds half the primary unweighted posterior 95 % CI width, this is flagged as a limitation in the paper (the substantive reading of the primary depends on which variation is being partitioned). Does *not* trigger an OSF amendment — preregistered exploratory sensitivity, not a confirmatory test. Reporting is read alongside §7 H3a row's confirmatory verdict, not as a co-equal verdict.
- **CPL knot-sensitivity analysis (Phase 1 supplementary).** For each CPL cell in the Phase 1 simulation, fits k ∈ {2, 3, 4} and records AIC + detection per k. Reports threshold at each fixed k and the max−min range as a diagnostic. Non-confirmatory; supplementary material.
- **CPL AIC-select threshold (Phase 1 supplementary).** Per-iteration picks k with minimum AIC from {2, 3, 4}; reconstructs threshold under AIC-select decision rule (cf. Timpson et al. 2021). Reports what AIC-select would have given; does *not* substitute for the fixed-k = 3 confirmatory result.
- **Stratified-sampling sensitivity (Phase 1 supplementary).** Phase 1 thresholds use bootstrap (sampling-with-replacement) from filtered LIRE; thresholds are recomputed using stratified-sampling (province-proportional or city-proportional draws). Reports deltas to bootstrap primary.
- **Temporal "habit-removed residual trajectory" analysis.** SPA's chief advantage over Hanson's point-estimate population data is that it produces a *time series* per city. The naive comparison (does a city's SPA peak match its independently-known demographic peak?) is confounded by the empire-wide epigraphic habit's own temporal shape. To control for the habit: decompose each city's SPA trajectory into an *empire-wide habit component* plus a *city-specific residual trajectory*, and validate the residual against independent temporal evidence. Anchor types, in priority order:
  - **Foundation dates** — applied corpus-wide; well-attested in standard references; a colony founded in AD X should show ~ zero SPA mass before AD X.
  - **Independent peak-population dates** — assembled for a bounded case-study set only; compared as posterior-CI calibration (does the independent date fall within the posterior peak-time credible interval).
  - **Multi-point independent trajectories** — for the few well-studied cities where they exist; full-shape comparison (overlapping the small-N "Layer B validation gate" item below).
  - **Ordinal flourishing-era rankings** — where absolute dates are unavailable; rank-correlation of SPA-peak order against independent ordinal knowledge.

  A *systematic* offset between city-specific inscription peaks and independent demographic peaks is reported as a quantitative estimate of the *epigraphic-habit lag* — a methodological finding, not a failure. The analysis is exploratory throughout: no pre-committed thresholds; the independent-anchor evidence is too sparse and uncertain to bind. Scope is explicitly bounded: foundation dates corpus-wide, plus a deliberately time-boxed case-study set for richer anchors; comprehensive independent-date assembly is deferred to a follow-up paper.

- **City-level temporal trajectory estimation for small-N cities.** The Phase 1 confirmatory eligibility threshold (≈ 1,549 inscriptions for 50 %-over-50-years detection at urban-area level; see §7) restricts H3b urban-area deviation-detection to a handful of the largest cities. The remaining ~ 800 Hanson-matched cities have inscription counts below the confirmatory threshold but are not analytically inert — Bayesian aoristic estimation with explicit uncertainty propagation can produce trajectory-shape estimates from corpora as small as N ≈ 50 (cf. Crema 2025; Crema & Bevan 2021).

  **Core (Layer A) — temporal trajectory shape estimation.** For each Hanson-matched city, compute a posterior distribution over time-binned inscription density via a Bayesian hierarchical model (ICAR prior for temporal smoothing; partial-pooling toward province-level mean trajectory; aoristic uncertainty propagated per inscription). Report per-city posterior trajectory shape with 95 % credible intervals. Estimation, not hypothesis testing.

  **Extension (Layer B) — tentative inversion to time-varying population.** Under the assumption that the cross-sectional β-scaling estimated from H3a holds within-city over time, invert each city's trajectory to an illustrative time-varying population estimate: `pop_t ≈ pop_max × (insc_t / insc_max)^(1/β_within)`. Strong assumption flagged: within-city β stability over time is only approximately true. Reported as illustrative comparative-shape outputs only — *not* as quantitative population claims.

  **Aggregate diagnostic.** Posterior precision vs N (median CI width binned by N); trajectory-shape clustering; Layer B validation gate at independently-dated cities (Pompeii AD 79, Ostia c. AD 250, etc.). A negative result is itself a methodological contribution.

  **Province-scale extension.** Same methodology at province scale (~ 50 provinces) as a parallel methodological output, with substantive provincial-prosperity reconstruction deferred to a planned follow-up paper.

- **Stratified-by-convention-class SPA** as a real-data internal-consistency check on the Bayesian mixture (overlapping H2.4; reported separately for transparency).

- **`baorista` Bayesian aoristic comparison** (Crema 2025) on representative provincial subsets. baorista — with NIMBLE, brms, and cmdstanr — is installed and smoke-validated on the project's compute server (see §9); the comparison runs as an appendix figure with accompanying discussion, providing a Bayesian-aoristic cross-check on the frequentist permutation-envelope results.

- **Scaling-residual sensitivity analysis for H3a:** compute per-city residuals from a fitted power-law `inscriptions ∝ population^β`; re-run H3a on residuals. Tests whether the Hanson-population correlation survives scaling-controlled analysis.

- **α-as-translator sensitivity analysis for H3a:** include per-city posterior mixture α as an additional covariate in the NBR; test whether the within-province β estimate shifts meaningfully. Informs whether the Hanson correlation is confounded by epigraphic-habit intensity. (Caveat: per-city α is unidentified for low-N cities; this sensitivity is restricted to cities with N ≥ 100, ~ 200 cities.)

- **Chronological resolution of H3c urban-area residuals:** extend Hanson's (2021) time-pooled residual analysis by computing residuals per decadal period. Exploratory because no published comparator exists.

- **Information-infrastructure versus complexity-markers theoretical framing.** The paper presents both readings of what inscription production proxies — Hanson's (2021) "information infrastructure" and the alternative reading of inscriptions as markers of socio-political complexity — and discusses the evidence bearing on each, rather than adjudicating between them. Feedback from presenting the work at RAC-TRAC 2026 is treated as critique to inform further exploration of both readings, not as the deciding word on which is correct. This theoretical-framing exploration is exploratory by intent; no preregistered hypothesis turns on which framing is correct.

- **Letter-count alternative analysis.** Per subset, repeat the H3 analyses using summed conservative letter counts (the `clean_text_conservative` field — Latin A–Z characters only, Greek excluded) in place of inscription counts. The rationale is a deliberate methodological disagreement with Hanson (2021). Hanson identifies the total volume of lettering as a methodologically desirable measure but rejects it as impractical, because so many inscriptions are fragmentary that their original lengths cannot be estimated (Hanson 2021, p. 142). We — with the LIRE team — take the opposite view: a flat inscription count implicitly treats a long monumental text and a three-word funerary fragment as equivalent units, when they plainly are not, and letter count, for all its preservation problems, at least registers something of the quantity of information an inscription carried. Letter count is treated as the lesser of two evils, not a problem-free measure, and reported as a cross-check on the inscription-count results rather than a replacement for them. The `clean_text_conservative` variant is used in preference to the interpretive variants because the interpretive text incorporates modern editorial restorations and expansions — exactly the kind of editor-dependent variation the deconvolution-mixture model exists to remove — whereas the conservative text counts only what survives; `clean_text_interpretive_word` is available as a sensitivity check. The analysis carries forward an exploratory observation from the project's 2024 seminar work, where a Negative Binomial model on letter counts produced a strikingly high pseudo-R²; that result was flagged at the time as "too good to be true" and a suspected artefact of the count model's dispersion structure, and is revisited here with the corrected pipeline.

## 7. Effect-size pre-specifications (summary)

| Hypothesis | Quantity | Preregistered target |
|---|---|---|
| **Confirmatory** | | |
| H2.1 (recovery simulation) | Per-cell α coverage | ≥ 90 % of grid cells achieve per-cell coverage, where a cell *passes* iff ≥ 90 % of its replicates produce a posterior 95 % CI containing the true α. Cell-wise results reported. |
| H2.1 (recovery simulation) | Genuine-shape recovery | Posterior-median Pearson r ≥ 0.95 between recovered and true genuine SPA in ≥ 90 % of grid cells (binding rule). **Supplementary**: Wasserstein-1 (Earth Mover's distance) between posterior-median and true genuine SPA reported per cell against a design-artefact-pinned flagging threshold; descriptive only, not part of the binding rule. |
| H3a primary | Within-province population-attributable variance fraction `f_within` | **Three-way verdict.** Supported: posterior 95 % CI wholly above 0.10. Evidence against: wholly below 0.10. Inconclusive: straddles 0.10. Supplementary reporting: P(f_within > 0.05), P(f_within > 0.10), P(f_within > 0.20). The verdict is computed on the **unweighted** primary `f_within`; **population-weighted** and **inscription-weighted** `f_within` variants are reported as §6 exploratory sensitivities alongside, not as co-equal confirmatories. |
| H3c (i) | Capitals contrast on draw-wise Pearson residuals | P(mean(r_c | capitals) − mean(r_c | non-capitals) > 0) ≥ 0.95. |
| H3c (ii) | Moran's I on posterior-mean Pearson residuals | I > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} k-NN weights (conditional permutation inference). Supplementary: posterior distribution of I per k. **Three-case interpretive guardrail** governs the paper's reporting language when the rule passes (clean replication ≥ 95 % of `I_s` draws > 0 at k = 8; permutation-significant but posterior-sensitive if 95 % posterior interval crosses zero; not substantively supported if posterior centred near zero, < 50 % draws > 0) — see §4. |
| **Mixture supplementary sensitivities (real data, Phase 2)** | | |
| H2 aoristic-MC sensitivity | Cross-realisation posterior of α across N_MC ∈ [20, 50] independently-sampled aoristic SPA realisations (design-artefact-pinned N_MC) | Reported alongside the primary single-SPA posterior on α. **Divergence flag:** if the cross-realisation 95 % range on α exceeds 1.5× the primary posterior's 95 % CI width, flagged as a material limitation in the paper. Preregistered exploratory sensitivity; no OSF amendment trigger. |
| **Supporting consistency (real data, Phase 2)** | | |
| H2.2 | Boundary-step reduction in corrected SPA | Per template boundary year (0, 100, 200, 300), corrected step magnitude reduced by ≥ 50 % relative to uncorrected SPA. |
| H2.3 | Pairwise Pearson r across threshold variants | r ≥ 0.9 between any two threshold-filtered `genuine_SPA` variants. |
| H2.4 | Stratified-by-convention-class SPA vs deconvolved | Agreement within sampling error (continuous discrepancy reported; no binary threshold). |
| **Completed groundwork (Phase 1, fixed; not confirmatory)** | | |
| Phase 1 power floor | Detection rate | ≥ 0.80 at *p* < 0.05 per bracket; zero-effect false-positive rate ≤ 0.05 (achieved across all 96 zero-effect calibration cells, range `[0.007, 0.049]`). |
| Phase 1 thresholds (50 % over ≥ 50 y) | min n at detection ≥ 0.80 | **province** exp-step 1938, exp-gauss 1869, cpl-3-step 1385, cpl-3-gauss 1618; **urban-area** exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549; **empire** reachable at n = 50,000. |
| Phase 1 thresholds (doubling over ≥ 25 y) | min n at detection ≥ 0.80 | Gaussian shape: empire reachable at n = 50,000; province exp 2118, cpl-3 1934; urban-area exp 2160, cpl-3 1905. Step shape unreachable across all levels. |
| Phase 1 thresholds (20 % over 25 y; hard-test boundary) | min n at detection ≥ 0.80 | Empire / cpl-3 / Gaussian reachable at n = 50,000 (single marginally-reachable cell); all other combinations unreachable. Bracket retained as honest-uncertainty anchor; not in the H3b family. |
| **Pre-specified exploratory** | | |
| H3b Antonine probe | Deviation at AD 165–180 | Permutation-envelope departure at empire, Asclepius-cult, and military subsets; reported descriptively against project brackets; no pre-committed magnitude. |
| H3b Crisis-of-the-Third-Century probe | Deviation at AD 235–284 (50 y inclusive) | Permutation-envelope departure at empire and Western-Empire-provincial (`province_language == 'Latin' AND province != 'Roma'`) subsets, conditional on Phase 1 reachability; reported descriptively against project brackets; no pre-committed magnitude. |

## 8. Planned deviations and contingencies

Before lodgement, this preregistration may be revised; any revision is recorded in the change log (`planning/preregistration-changelog.md`). After OSF lodgement, the preregistration is a fixed public record and any subsequent change is filed as an OSF amendment before implementation.

- **Levels at which Phase 1 did not establish a finite detection threshold** within the swept sample-size range are dropped from confirmatory testing at that level (and from H3b exploratory testing on the relevant subsets) and may optionally be retained in the paper as exploratory. Phase 1 is complete; §7 gives the resulting thresholds and the levels they make eligible.
- **If the recovery-simulation validation fails** (either coverage or shape-recovery), an OSF amendment is filed and the Bayesian mixture is revised before any Phase 3 analysis runs. Likely revisions: re-parameterisation of the convention tier weights; smoothness prior on the genuine component; alternative tier composition; alternative observation-model family (Decision 19's supplementaries become candidate primaries).
- **If the pymc / brms shadow posteriors disagree beyond Monte Carlo noise** on H3a's confirmatory quantities, the cause is investigated; a material disagreement (affecting the H3a verdict) triggers an OSF amendment before final results are lodged.
- **If any numerical PPC threshold is tripped** for H3a (the design-artefact-pinned thresholds; see §4 and §5), the response is **two-tier severity-conditional**: a *critical* trigger (PPC value > 2× the design-artefact-pinned bound, or sign-flipped where applicable) initiates model revision (priors, link function, or model structure); the originally-preregistered model result is reported alongside the revised model's result; an OSF amendment is filed before final results are lodged. A *minor* trigger (PPC value within > 1× but ≤ 1.5× the bound — tripped, but marginally) is reported as a caveat in the paper without forcing model revision and without an OSF amendment. The 2× / 1.5× cutoffs and the per-category response wording are pinned in the design artefact.
- **If substantive methodology changes are required after lodgement** — whether prompted by co-author input, the planned statistician consultation, or anything else — an OSF amendment is filed before implementation.

## 9. Software, reproducibility, and data access

- **Language:** Python 3.13 for the primary pipeline; R 4.4.3 for the `brms` shadow validation of the H3a model and for the baorista comparison.
- **Environment:** `uv`-managed Python virtual environment with a pinned `requirements.txt`; the R packages are installed on the project's compute server.
- **Core dependencies (Python):** `numpy`, `scipy`, `pandas`, `pyarrow`, `matplotlib`, `joblib`, `statsmodels`, `libpysal` (spatial weights for Moran's I), `pymc` (Bayesian mixture and H3a NBR), `pyzotero`, `requests`, `python-dotenv`. `cmdstanpy` is also installed as a fallback sampler backend but is not on the H3a NBR's critical path (pymc uses its native NUTS implementation).
- **Aoristic resampling implementation note:** the Uniform aoristic method is implemented directly in `primitives.py::aoristic_resample` as ≤ 10 lines of numpy. The SDAM `tempun` package (MIT; PyPI 0.2.4) was not used, because its current release is incompatible with numpy ≥ 2.4 (it calls the removed `numpy.trapz`); the direct implementation is mathematically equivalent under the Uniform aoristic distribution. An upstream issue has been filed to `sdam-au/tempun`; if `tempun` becomes numpy-2-compatible, it may be reintroduced for the H2 / H3 pipelines.
- **R dependencies (shadow validation and baorista comparison; not on the critical path for the primary Python results):** R 4.4.3, `cmdstanr` 0.9.0, `nimble` 1.4.2, `baorista` 0.2.1, and `brms` 2.23.0, with `posterior`, `bayesplot`, `loo`, and `arrow`. All installed and smoke-validated on the project compute server.
- **Data:** LIRE v3.0 (Zenodo DOI 10.5281/zenodo.8431452, v3.0, 11 October 2023; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) as a ground-truth cross-check for `urban_context_pop_est`.
- **Subset-filter feasibility (confirmed on LIRE v3.0).** Military-administration subset: `type_of_inscription_clean == 'military diploma'` yields 285 rows (66.4 % null in that field; primary filter for the military subset); the ML-classified `type_of_inscription_auto` yields 442 rows at 13.8 % null and is a named sensitivity. Asclepius-cult subset: if Glomb, Kaše & Heřmánková's (2022) exact filter is recoverable from their published methods by the pre-Phase-2 design-artefact commit date, it is primary; otherwise the regex `[Aa]esculap|[Aa]sclep` on the `inscription` free-text field is primary (yields 358 rows). Both N values are reported.
- **Western-Empire-provincial subset:** operationally defined as `province_language == 'Latin' AND province != 'Roma'`, using the project's province-language classification (committed in the public repository). 41 LIRE v3.0 provinces qualify under the Rome-exclusion rule.
- **Code:** the project repository is public at `github.com/saross/inscriptions`. Phase 1 simulation code, the canonical random seed (20260425), and all simulation outputs (FP-calibration results, threshold tables, power curves, heatmaps) are committed to the public repository, providing end-to-end reproducibility from raw data to thresholds. The pre-Phase-2 design artefact pinning the H2.1 recovery-grid values and the numerical PPC thresholds is committed before any Phase 2 analysis runs.
- **Repository state at lodgement:** the code, simulation outputs, decision log, changelog, diagnostic runs, and all other repository artefacts referenced in this preregistration correspond to the state of the public repository at git tag `osf-lodgement-2026-05-20` (https://github.com/saross/inscriptions/tree/osf-lodgement-2026-05-20). Readers verifying or replicating any claim in this preregistration should clone or browse the repository at that tag rather than at `main`.
- **Run artefacts:** each analysis stage is captured in a per-stage `runs/<date>-<description>/` directory recording its specification, agent briefs, random seed, code, outputs, and decisions.
- **Pre-lodgement state of substantive analyses.** As of lodgement, no confirmatory analysis preregistered here has been executed on LIRE v3.0. Prior exploratory regressions of inscription and letter counts against Hanson (2016) urban population estimates (frequentist OLS, NBR-GLM, robust, and related models with bootstrap intervals) were carried out on LIRE v3.0 in the project's exploratory notebooks; those results are documented in the project repository and inform the prior expectations cited here, but are not themselves confirmatory tests of these preregistered hypotheses.
- **Research record:** agent-session-capture infrastructure is operational; individual AI-agent prompts and outputs are preserved per open-science requirements.

## 10. Known limitations (preregistered)

- **Editorial-template artefact identification.** The Bayesian mixture addresses wide-template editorial encoding (century, half-century, and reign-interval templates). Year-precise inscriptions are *not* modelled as artefact — they remain in `genuine_SPA` as real ancient anchoring. Other documented LIST / LIRE artefacts — province-label anachronism (Heřmánková, Kaše & Sobotková 2021, §29; EDH anchors province labels to mid-2nd-century Roman geography), EDCS coordinate imprecision (§60), 50 % missing coordinate provenance (§45) — remain as interpretive caveats. The preregistration commits to transparent reporting of these, not to methodological correction.
- **BC / AD boundary step.** The empirical SPA shows a +1,159 step at the 1 BC / AD 1 boundary — the largest single discontinuity in the analysis envelope, attributable to the BC / AD calendar-convention boundary (1 BC is followed directly by AD 1; no year 0 in the Julian / Gregorian calendar) and the comparative rarity of inscriptions firmly dated to the late Republic. This boundary effect is *not* currently modelled as a separate convention-component tier; the `genuine_SPA` will inherit any residual structure at the BC / AD boundary. Flagged as a known limitation.
- **H3a and H3c use date-window-filtered counts, not mixture-corrected counts.** The Bayesian mixture corrects the temporal SPA analyses (H2.1 validation; H3b deviation-detection); it is *not* applied to the cross-sectional H3a regression. H3c's Pearson residuals are derived from H3a's posterior and therefore inherit H3a's date-filtered-count scope — H3c is also not a mixture-corrected analysis. A per-city mixture fit was not pursued because it would be unidentified for the ~ 600 cities below N = 100 inscriptions; cross-sectional artefact protection for both H3a and H3c is the 50 BC – AD 350 date-window filter. Neither H3a's variance-fraction posterior nor H3c's residual analyses propagate mixture-posterior uncertainty into their credible intervals — a genuine scope limit.
- **Western-Empire-provincial subset frontier classifications.** Three provinces in the Latin-classification set sit on the linguistic frontier: Moesia Inferior (Latin-administered, Greek-influenced via the Black Sea coast); Moesia Superior (Latin-administered); Sicilia (Latin-administered with significant Greek-speaking population). The classification choice (all three included as "Latin") is the project's existing operational rule; it is reported transparently and is *not* tested as a sensitivity in this preregistration (a post-hoc Moesia / Sicilia exclusion is reserved for follow-up).
- **Single-dimension complexity (Turchin et al. 2018).** The multi-factor complexity decomposition in the paper's theoretical frame operates at city / province × decadal scale; Turchin's "single latent dimension" operates at polity × century scale. Different scales; the paper acknowledges this but does not attempt empirical disaggregation of the non-population dimensions.
- **Identifiability of complexity dimensions.** With inscription count as the sole observable and Hanson population as the sole external covariate, dimensions 2–6 of the complexity decomposition (economic prosperity, social differentiation, cultural translator, ideology, residual) remain theoretically present but empirically entangled in the residual variance and in the between-province component of the H3a regression. The paper acknowledges this as a scope limitation; disaggregation is left to future work.
- **Between-province population effect not separately identifiable.** The H3a within-between specification cleanly identifies the *within-province* population effect (orthogonal to province membership), but the *between-province* component is entangled with `α_province` — i.e. with province-level "everything else." The between-province population gradient is reported but explicitly flagged as not separable from province-level cultural, administrative, and survival-bias variation.
- **Rome exclusion.** Rome is excluded from scaling regressions as an extreme outlier. Consistent with Hanson (2021) methodology; reported transparently; not tested as a sensitivity.
- **Hanson population uncertainty.** Hanson (2016) population estimates carry their own uncertainty, treated as exact in the H3a primary regression. A measurement-error sensitivity is preregistered in §6 (σ_pop ∈ {0.1, 0.2, 0.3}) to quantify the impact on `f_within`.
- **Mismatch between Hanson's population (maxima) and inscription counts (cumulative).** Hanson's population estimates are peak-imperial-era maxima; H3a's cumulative-count response is dimensionally a comparison of integrated inscription output against peak population, not max-against-max. We retain the cumulative-count response for direct replicability with Hanson 2021 and Carleton et al. 2025; a max-to-max analysis would require defining a peak-window operationalisation that cannot be applied to small-N cities and would diverge from the replication target.
- **Chronological envelope.** 50 BC – AD 350 (LIRE v3.0). Late Antique and post-AD-350 phenomena out of scope for this paper; an envelope extension to AD 600 via LIST v1.2 is a candidate for either a post-lodgement OSF amendment or a follow-up paper (see §2 and §8).

## 11. Hypothesis-level structure summary

```text
Phase 1 (completed groundwork)        Phase 2 (Bayesian mixture)       Phase 3 (population analyses)
-----------------------------         ----------------------------     -------------------------
detection thresholds fixed in §7  →   H2.1 recovery-sim validation  →  H3a within-between NBR
(not a confirmatory hypothesis)       (confirmatory; multinomial       on date-window-filtered
                                       likelihood; coverage rule)       counts (confirmatory;
                                      H2.2 / H2.3 / H2.4 supporting     three-way verdict on
                                      consistency checks (real data)    f_within)
                                                                       H3c capitals contrast +
                                                                        Moran's I on Pearson
                                                                        residuals (confirmatory)
                                                                       H3b exploratory
                                                                        deviation-detection
                                                                        at Antonine and Crisis
                                                                        probes
```

## 12. Provenance

- **Preregistration drafted** by Claude Code (Anthropic, Opus 4.7) under Shawn Ross's direction and with full human review.
- **Authors and contributions (CRediT taxonomy):**
  - Shawn Ross (Macquarie University) — Conceptualization, Methodology, Investigation, Writing – original draft, Writing – review & editing, Supervision, Project administration.
  - Adela Sobotková (Aarhus University) — Methodology, Validation, Writing – review & editing.
- **AI contributions:** theoretical-frame refinements (identifiability scope, the scaling-residual sensitivity flag, the cultural-translator confound strategy), articulation of the deconvolution-mixture model, the template-interval slab convention-component structure, the temporal "habit-removed residual trajectory" framing, and this preregistration draft. All substantive AI intellectual contributions are logged in the project repository.
- **Funding:** no funding was received for this work.
- **Competing interests:** the authors declare no competing interests.
- **Ethics:** this work reanalyses publicly available, published datasets and did not require ethics review.

---

## 13. References

Anselin, L. (1995). Local indicators of spatial association—LISA. *Geographical Analysis*, 27(2), 93–115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x

Carleton, W. C., Campbell, D., & Collard, M. (2018). Radiocarbon dating uncertainty and the reliability of the PEWMA method of time-series analysis for research on long-term human–environment interaction. *PLOS ONE*, 13(1), e0191055. https://doi.org/10.1371/journal.pone.0191055

Carleton, W. C., Elton, H., Miranda, W., Work, I., Safarik, D., Winkelmann, R., Laubichler, M., Renn, J., & Roberts, P. (2025). Parallel scaling of elite wealth in ancient Roman and modern cities with implications for understanding urban inequality. *Nature Cities*, 2(4), 344–355. https://doi.org/10.1038/s44284-025-00213-1

Cliff, A. D., & Ord, J. K. (1981). *Spatial processes: Models and applications*. Pion.

Crema, E. R., & Bevan, A. (2021). Inference from large sets of radiocarbon dates: Software and methods. *Radiocarbon*, 63(1), 23–39. https://doi.org/10.1017/RDC.2020.95

Crema, E. R. (2025). A Bayesian alternative for aoristic analyses in archaeology. *Archaeometry*, 67(S1), 7–30. https://doi.org/10.1111/arcm.12984

Duncan-Jones, R. (2018). Antonine Plague revisited. *Arctos — Acta Philologica Fennica*, 52, 41–72. https://doi.org/10.71390/arctos.84955

Gelman, A., Goodrich, B., Gabry, J., & Vehtari, A. (2019). R-squared for Bayesian regression models. *The American Statistician*, 73(3), 307–309. https://doi.org/10.1080/00031305.2018.1549100

Glomb, T., Kaše, V., & Heřmánková, P. (2022). Popularity of the cult of Asclepius in the times of the Antonine Plague: Temporal modeling of epigraphic evidence. *Journal of Archaeological Science: Reports*, 43, 103466. https://doi.org/10.1016/j.jasrep.2022.103466

Hanson, J. W. (2016). *An urban geography of the Roman world, 100 BC to AD 300*. Archaeopress.

Hanson, J. W., Ortman, S. G., & Lobo, J. (2017). Urbanism and the division of labour in the Roman Empire. *Journal of the Royal Society Interface*, 14(136), 20170367. https://doi.org/10.1098/rsif.2017.0367

Hanson, J. W. (2021). Cities, information, and the epigraphic habit: Re-evaluating the links between the numbers of inscriptions and the sizes of sites. *Journal of Urban Archaeology*, 4, 137–152. https://doi.org/10.1484/J.JUA.5.126597

Heřmánková, P., Kaše, V., & Sobotková, A. (2021). Inscriptions as data: Digital epigraphy in macro-historical perspective. *Journal of Digital History*, 1(1). https://doi.org/10.1515/JDH.2021.1004.R1

Kaše, V., Heřmánková, P., & Sobotková, A. (2023). *LIRE: Latin Inscriptions of the Roman Empire* (Version v3.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.8431452

Kaše, V., Heřmánková, P., & Sobotková, A. (2024). *LIST* (Version v1.2) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.10473706

Mundlak, Y. (1978). On the pooling of time series and cross section data. *Econometrica*, 46(1), 69–85. https://doi.org/10.2307/1913646

Rick, J. W. (1987). Dates as data: An examination of the Peruvian preceramic radiocarbon record. *American Antiquity*, 52(1), 55–73. https://doi.org/10.2307/281060

Timpson, A., Colledge, S., Crema, E., Edinborough, K., Kerig, T., Manning, K., Thomas, M. G., & Shennan, S. (2014). Reconstructing regional population fluctuations in the European Neolithic using radiocarbon dates: A new case-study using an improved method. *Journal of Archaeological Science*, 52, 549–557. https://doi.org/10.1016/j.jas.2014.08.011

Timpson, A., Barberena, R., Thomas, M. G., Méndez, C., & Manning, K. (2021). Directly modelling population dynamics in the South American Arid Diagonal using ¹⁴C dates. *Philosophical Transactions of the Royal Society B*, 376(1816), 20190723. https://doi.org/10.1098/rstb.2019.0723

Turchin, P., Currie, T. E., Whitehouse, H., François, P., Feeney, K., Mullins, D., Hoyer, D., Collins, C., et al. (2018). Quantitative historical analysis uncovers a single dimension of complexity that structures global variation in human social organization. *Proceedings of the National Academy of Sciences*, 115(2), E144–E151. https://doi.org/10.1073/pnas.1708800115

Williams, A. N. (2012). The use of summed radiocarbon probability distributions in archaeology: A review of methods. *Journal of Archaeological Science*, 39(3), 578–589. https://doi.org/10.1016/j.jas.2011.07.014
