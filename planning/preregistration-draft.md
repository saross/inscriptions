---
priority: 1
scope: in-stream
title: "OSF Preregistration (open-ended) — Draft"
audience: "Shawn (review + edit), Adela (co-author review), OSF reviewers"
status: draft 2026-04-24; awaiting Shawn's edit pass before Adela review
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

**Primary:** LIRE v3.0 (Kaše, Heřmánková & Sobotková, Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 rows; 65 attributes. Filtered to `is_within_RE == True`, `is_geotemporal == True`, and a 50 BC – AD 350 date-interval intersect. Pre-joined Hanson (2016) urban-population estimates available as the `urban_context_pop_est` attribute at row level (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

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
- **Permutation envelope:** rcarbon-style `modelTest()` algorithm (Crema & Bevan 2021) ported to Python using `scipy.stats.permutation_test` as the primitive, `tempun` for aoristic replicates. Implementation ~200 LOC (Obs 3). Null model: exponential or piecewise-linear fitted growth (per Timpson et al. 2014); 1,000 Monte Carlo replicates; two-sided 95 % envelopes.
- **Deconvolution-mixture model:** `observed_SPA = α · convention_SPA + (1 − α) · genuine_SPA`. α estimated by maximum-likelihood or mixture-model fit on the convention-vs-precision row classification; `genuine_SPA` recovered by linear deconvolution with non-negativity constraints. `convention_SPA` shape: uniform century slabs per Decision 7 default, OR hierarchical (century > half-century > quarter-century > reign-boundary) if the Obs 11 editorial-convention-hierarchy test (Thursday 2026-04-24) confirms. Defaults to uniform if hierarchy test is inconclusive at 14-boundary sample.
- **Bayesian NBR for H3a:** `log(E[inscriptions_city]) = α_0 + α_province + β · log(population_city) + ε`, fitted with weakly informative priors, negative-binomial family, log link, provincial random intercepts. **Primary implementation in `pymc`** (Python; stays in the project venv). **Secondary `brms`-via-R cross-validation shadow** (~50 lines, committed as `scripts/h3a_brms_shadow.R`): refits the same model in R+Stan via brms' formula syntax (`count ~ log_pop + (1|province)`, `family = negbinomial()`), providing (i) cross-language validation that pymc and brms agree on the posterior within MC noise and (ii) legibility for R-native co-authors (Adela Sobotková and others) who read brms syntax more fluently than pymc code. Outputs (posterior draws, summary tables, figures) exchanged as CSV / parquet / PNG — language-neutral. Bayesian R² reported per Gelman, Goodrich, Gabry & Vehtari (2019) via `pymc`-native computation and cross-checked against `brms::bayes_R2()`. Full posterior distributions retained for downstream residual analysis.
- **Residual analysis (H3c):** per-city residuals extracted from H3a posterior; classified as over-producing, under-producing, or typical (±95 % credible interval from predicted).
- **Spatial clustering:** Moran's I with row-standardised spatial weights (*k*-nearest-neighbours with *k* = 5, or distance-based within 500 km — TBD; pick to match Hanson 2021's approach after PDF re-read).

### 4. Pre-specified confirmatory analyses

**Phase 1 — H1 min-thresholds simulation protocol (to run first).**

For each combination of (subset level ∈ {empire, province, urban-area}; effect-size target ∈ {Decision 5 a/b/c + zero-effect calibration check}; sample size n ∈ logarithmic sweep):

1. Simulate a synthetic SPA under the null (fitted model of the corresponding real-world subset).
2. Inject an effect of the target magnitude and duration.
3. Apply the permutation-envelope test.
4. Record detection / non-detection.
5. Repeat 1,000 times per cell.

Detection rate per cell = fraction detecting at *p* < 0.05. **Preregistered threshold per level = smallest n at which detection rate ≥ 0.80** for each of the Decision 5 a/b/c targets; the most conservative (50 % / ≥ 50 y) is the binding threshold for downstream H2 and H3 subset-eligibility decisions. Detection-rate curves at 0.70 / 0.80 / 0.90 reported for transparency. Zero-effect cell must return false-positive rate ≤ 0.05 as a calibration check.

**Null model:** both **exponential (primary, per rcarbon / Timpson et al. 2014)** and **continuous piecewise-linear (CPL, secondary, per Timpson et al. 2021)** fitted; results compared. Rationale: CPL is more flexible but has more parameters; running both lets us check whether null-model choice materially affects the min-threshold conclusions.

**Effect shape for injection:** smooth (Gaussian-tapered) dip with FWHM matching each Decision 5 bracket's stated duration and magnitude at nadir matching the bracket's stated deviation. The Gaussian-taper choice (rather than step-function) is deliberately conservative: smooth effects are harder to detect via permutation-envelope methods, so thresholds set on smooth effects are upper bounds on the sample size needed for sharper effects.

Adapts the Carleton, Campbell & Collard (2018, *PLOS ONE* 13:e0191055; code CC-BY) PEWMA power-simulation framework for cross-sectional SPA × covariate analysis.

**Phase 2 — H2 mixture-model validation (after H1 thresholds fixed).**

Run the mixture-model fit on empire-level LIRE. Report α̂ and 95 % CI; report corrected century-midpoint observed/expected ratios; report pairwise Pearson *r* across threshold-filtered `genuine_SPA` variants; report stratified-by-convention-class SPA alongside deconvolved `genuine_SPA`. H2.1–H2.4 criteria as listed in Field 3.

**Phase 3 — H3 substantive analyses.**

- H3a: Bayesian NBR as specified in §3 above. Report β, posterior R² (median + 95 % CI), comparison with OLS log-log (reported alongside as direct comparator to Hanson, Ortman & Lobo 2017).
- H3b: Permutation-envelope SPAs at every preregistered subset × effect-size combination. Holm-Bonferroni correction across the full family. **Antonine-specific test is preregistered as exploratory replication of Glomb, Kaše & Heřmánková (2022) and Duncan-Jones (2018)**: at AD 165–180, test for deviation in mixture-corrected SPA at empire level, at Asclepius-cult subset (replicates Glomb et al.'s design at larger N and on corrected data), and at military-administration subset (replicates Duncan-Jones-style severe-effect prediction), conditional on per-subset sample-size thresholds being met. Results reported against Decision 5 brackets; no specific effect size preregistered for the Antonine test itself. Subset-filtering feasibility depends on LIRE type / category / deity fields — confirmed as part of this preregistration (see §9 Software & data).
- H3c: Residual classification + Moran's I + provincial-capital *t*-test as listed in H3.

### 5. Exploratory analyses (explicitly flagged as non-confirmatory)

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
| H1 power floor | Detection rate | ≥ 0.80 at p < 0.05 per Decision 5 bracket; zero-effect false-positive rate ≤ 0.05 |
| H2.1 | α̂ | Posterior CI excludes 0; point estimate > 0.1 |
| H2.2 | Corrected century-midpoint O/E | Within 1.5× of local neighbourhood mean |
| H2.3 | Pairwise Pearson *r* across threshold variants | ≥ 0.9 |
| H3a urban-area | Bayesian R² | ≥ 0.25 (anchored on Hanson, Ortman & Lobo 2017 R² = 0.267) |
| H3a province | Bayesian R² | ≥ 0.50 (Palmisano et al. 2021 upper empirical range) |
| H3b primary | Antonine signature | ≥ 50 % dip sustained ≥ 50 y at AD 165–180 |
| H3b secondary | Other targets | Decision 5 a/b/c effect-sizes, Holm-Bonferroni corrected |
| H3c provincial-capital | Mean residual difference | One-sided *t*-test *p* < 0.05 |
| H3c spatial clustering | Moran's I | > 0, *p* < 0.05 |

### 7. Planned deviations and contingencies

- **If H1 reveals insufficient data density at a given subset level,** H2 and H3 analyses at that level are dropped from confirmatory testing and (optionally) retained in the paper as exploratory.
- **If Obs 11 editorial-convention-hierarchy test confirms** (Thursday 2026-04-24), `convention_SPA` shape in the mixture shifts from uniform century slabs to weighted hierarchical. If inconclusive, default uniform is retained per Decision 7.
- **If `baorista` compilation fails on sapphire,** the Bayesian-aoristic comparison demotes from appendix figure to citation-with-rationale (per Decision 3 fallback).
- **If LIST swap completes before paper-sprint Week 1,** analytical envelope extends to AD 600 and Late Antique subsets are added; otherwise LIRE envelope remains.
- **If Adela requests substantive methodology changes during co-author review,** an amendment to this preregistration is filed on OSF before implementation.

### 8. Open design decisions (TBD markers — resolve before submission)

- Final preregistered sample-size thresholds from the H1 simulation.
- ~~Bayesian-NBR software choice~~ **Resolved 2026-04-24:** primary `pymc`; secondary `brms`-via-R shadow (~50-line script) for the H3a model only, as cross-validation + R-team legibility. Carleton et al. 2025's provincial posterior effects consumed as data, not code.
- Exact priors on α_0, α_province, β, dispersion — weakly informative, specifics after Adela consults.
- Spatial-weights construction for Moran's I: *k*-NN (*k* = 5) vs distance-based (500 km cut-off) — match Hanson (2021) when local PDF is read in detail.
- Multiple-comparison family for H3b: exact Holm-Bonferroni family after H1 fixes the subset × effect-size grid.
- Decision-log reference for the target venue (JAMT methods-heavy vs JAS balanced) — committed at end of Week 1 paper sprint (2026-05-03) per Decision 7.

### 9. Software, reproducibility, and data access

- **Language:** Python 3.13 (primary); R if `brms` is preferred for Bayesian NBR.
- **Environment:** `uv`-managed venv at `~/Code/inscriptions/.venv/`; `requirements.txt` pinned.
- **Core dependencies (Python):** `tempun` (SDAM, MIT), `numpy`, `scipy`, `pandas`, `pyarrow`, `pymc` (primary Bayesian NBR), `pyzotero`.
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

---

## Review pointers for Shawn

- **Tone and depth:** aimed at OSF open-ended registration standards — discursive where helpful, concise where possible. Compare to your map-reader-llm prereg and push back if this is over- or under-specified for the format you want.
- **Preregistered claims vs exploratory:** §4 (confirmatory) and §5 (exploratory) are the core boundary. Moving items between them materially changes what the preregistration binds you to.
- **TBD markers:** 6 explicit items in §8 need your input before OSF submission.
- **Effect-size anchors:** §6 summary table collects all preregistered thresholds. If any feel too ambitious or too lax, that's the place to push.
- **Limitations:** §10 is written to be honest-sooner-rather-than-later; reviewers will read it.
- **Adela review step:** not scheduled in this draft; recommend it before OSF submission. Diff this draft against her expectations; file any amendments on OSF after initial registration if substantive changes arise.
- **Next mechanical steps after your edit pass:** (i) run H1 simulation, (ii) fix the TBD thresholds, (iii) Adela review, (iv) submit on OSF, (v) execute H2 + H3.
