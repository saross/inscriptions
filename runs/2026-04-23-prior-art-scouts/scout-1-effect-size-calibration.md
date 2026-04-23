---
title: "Prior-art scout 1 — effect-size calibration for SPD × covariate variance-explained"
commissioned: 2026-04-23
completed: 2026-04-23
agent: prior-art-scout
scope: Q1 of three-scout overnight run — R² thresholds for H3a variance-explained pre-specification
source: background agent invocation during 2026-04-23 session
verification: agent-returned; DOI / URL verification pending
---

# Scout 1 — Effect-size conventions for R² / variance-explained in SPD × covariate studies

## Executive summary

Partially-solved problem with a significant structural gap. The SPD/SPA × covariate literature is dominated by one of two statistical paradigms: (a) permutation-envelope deviation-detection (inherently non-parametric; no R² analogue), or (b) Bayesian model-selection via Bayes factors, WAIC, DIC, or ABC distance metrics (also no conventional variance-explained statistic). **No field-specific R² conventions or benchmarks exist in this literature** — the question of what counts as small / medium / large R² in SPD × covariate work has not been systematically addressed anywhere.

The closest calibration anchors are:
- **Carleton et al. 2018 (PEWMA simulations)**: r = 0.5 (R² ≈ 0.25) is the practical detection floor for palaeodemographic time-series correlation analysis.
- **Hanson, Ortman & Lobo 2017 (*J. R. Soc. Interface*)**: R² = 0.267 (population vs functional diversity, all cities) and R² = 0.361 (inscription count vs association diversity, excluding Rome) — the only published R² benchmarks in Roman-inscription × population regression using the same Hanson 2016 dataset the project will use.
- **Kolar et al. 2023 (SPD field)**: applies Cohen's brackets (r small ±0.10 / moderate ±0.30 / large ±0.50) directly, without modification. Cohen is the de facto fallback.
- **Palmisano et al. 2021 (Italy & Near East SPD × climate)**: empirical range of Pearson r values from –0.68 to +0.77 in moving-window analyses (R² range 0.005 to 0.59).

**No simulation-based power-analysis templates designed specifically for SPD × covariate correlations exist as packaged tools.** Cohen's generic conventions remain the implicit fallback because no field-specific alternatives have been formally proposed.

## Candidates table (detailed)

| # | Citation | Fit | R² / r reported? | Key value / note |
|---|----------|-----|------------------|------------------|
| 1 | Shennan et al. 2013 (*Nature Comms*) | HIGH framing / LOW R² | **None** | Monte Carlo deviation-detection only; climate dismissal is qualitative |
| 2 | Timpson et al. 2014 (*J. Archaeol. Sci.*) | MEDIUM | **None** for covariates | Monte Carlo envelope; Bevan et al. 2017 reports r = 0.69–0.86 for inter-regional agreement (not climate-SPD) |
| 3 | Timpson et al. 2021 (*J. Archaeol. Sci.*) | LOW for R² | **None** | CPL Bayesian; BIC-based model comparison |
| 4 | Crema & Bevan 2021 (*Radiocarbon*) — rcarbon | HIGH methodology | **None** | Permutation-envelope paradigm; no covariate regression workflow in rcarbon |
| 5 | **Palmisano et al. 2021** (*J. World Prehistory*, Italy) | HIGH | Pearson r range –0.68 to +0.77 | Moving-window 500-year windows; p < 0.05 threshold; R² not computed |
| 6 | Palmisano et al. 2021 (*QSR*, Near East) | HIGH | r = 0.09–0.97 (SPD vs settlement); r = 0.91 / 0.95 (validation) | R² not computed |
| 7 | Bevan et al. 2017 (*PNAS*) | MEDIUM | **None** for climate | Visual alignment + permutation; r = 0.69–0.86 for inter-regional agreement only |
| 8 | **Carleton, Campbell & Collard 2018** (PEWMA power-sim, *PLOS ONE*) | **HIGHEST** | r = 0, 0.25, 0.5, 0.75 tested | Detection reliability: r = 0.25 → 20–30 % detected; r = 0.5 → > 90 % detected; r = 0.75 → robust. **Practical floor: r ≈ 0.5 (R² ≈ 0.25).** |
| 9 | Carleton et al. 2021 (Maya conflict, *PLOS ONE*) | MEDIUM | Bayes Factor = 21.68 ("strong evidence" per Jeffrey's scale) | No R² |
| 10 | Carleton & Groucutt 2021 (*The Holocene*) | HIGH framing | Critique | Argues SPD point-wise regression fundamentally unreliable — but for *radiocarbon* calibration uncertainty; weaker for calendar-date inscription data |
| 11 | **Hanson, Ortman & Lobo 2017** (*JRS Interface*) | HIGHEST direct | R² = 0.267 (all) / 0.361 (excl. Rome) | Direct comparator for project; uses same Hanson 2016 pop dataset |
| 12 | Hanson et al. 2022 (*PLOS ONE*) | MEDIUM | r = 0.52 (diversity); r = 0.11 ("very weak") | Author-stated thresholds "very weak / rather strong / relatively strong" — qualitative only |
| 13 | **Kolar et al. 2023** (*PLOS ONE*) | MEDIUM | Cohen's brackets applied: r small > ±0.10, moderate > ±0.30, large > ±0.50 | **Direct evidence Cohen is used in SPD work** |
| 14 | DiNapoli et al. 2021 Rapa Nui (*Nature Comms*) | MEDIUM | **None** | ABC distance metrics; Bayes Factors; no R² |
| 15 | Gelman, Goodrich, Gabry & Vehtari 2019 (*American Statistician*) | MEDIUM conceptual | Bayesian R² framework | Posterior distribution over R²; **not adopted in SPD/palaeodemography** (adoption gap) |

## Key calibration points

### Carleton et al. 2018 PEWMA simulation (the anchor)

Explicitly tested four true-correlation levels (r = 0, 0.25, 0.5, 0.75) across sample sizes and ¹⁴C uncertainties:

- **r = 0.25** → correctly identified 20–30 % of the time. Authors call this marginal and unreliable.
- **r = 0.50** → correctly identified > 90 % of the time. Practical detection threshold.
- **r = 0.75** → reliable under most conditions.

Translating:
- r = 0.25 → R² = 0.0625 (effectively undetectable)
- r = 0.50 → R² = 0.25 (practical reliability floor)
- r = 0.75 → R² = 0.5625 (robustly detectable)

**Adoption recommendation:** cite Carleton et al. 2018 to motivate R² ≥ 0.25 at urban-area level as "at or above the reliability threshold established in simulation for palaeodemographic time-series methods."

### Hanson, Ortman & Lobo 2017 (direct comparator)

- Population vs functional diversity (all cities): best-fit slope 0.686 (SE 0.078), R² = 0.2670.
- Inscription count vs association diversity (excluding Rome): R² = 0.3607, p < 0.0001.
- Inscription count vs association diversity (including Rome): R² = 0.9426 — should be discounted (Rome has 119,532 inscriptions vs next-largest cities; dominates the regression).

**The project's 2024 baseline R² = 0.101 sits well below Hanson 2017 published benchmarks.** The pre-specified R² ≥ 0.25 at urban-area matches Hanson et al.'s "all cities" published result (0.267). R² ≥ 0.50 at province level is at the upper end of the Palmisano empirical range (0.59).

### Kolar et al. 2023 brackets (Cohen's, unmodified)

Cites in text/tables: "small (> ±0.10), moderate (> ±0.30), large (> ±0.50)" for Pearson r. R² equivalents: small 0.01, moderate 0.09, large 0.25. This is direct evidence that SPD researchers, when forced to be explicit, adopt Cohen's brackets without modification.

### Palmisano et al. 2021 empirical range

- Italian study: moving-window r from –0.68 to +0.77 (R² 0.005 to 0.59 if squared).
- Near East study: SPD vs settlement-size r from 0.09 to 0.97; SPD validation r = 0.91, 0.95.
- Authors describe early-Holocene correlations as "close coupling" without specifying r threshold.

## Simulation-based power analysis

**What exists:**
- **PEWMA simulation (Carleton et al. 2018, CC-BY)** — the only published power-simulation template for palaeodemographic × covariate analysis. Code in PLOS ONE supplementary. Time-series PEWMA, not cross-sectional regression, but the simulation logic is adaptable.
- **rcarbon `modelTest()`** — Monte Carlo vs theoretical growth models, not external covariates.
- **ADMUR, nimbleCarbon** — BIC / WAIC / Bayes factors; no covariate power analysis.
- **Generic R packages (paramtest, pwrss)** — not specialised for SPD contexts.

**What does not exist:** No published, packaged power-analysis simulation for cross-sectional SPD × covariate regression (OLS, Poisson, or negative binomial) at any spatial aggregation level. **Genuine gap.**

**Closest adoptable template:** Carleton et al. 2018 simulation design — fix a true population-covariate correlation, simulate with realistic measurement properties, apply analysis repeatedly, count detection rate. Adapting to the project's log-log OLS or negative binomial framework requires ~200–300 lines of R or Python: specify data-generating process for inscription counts given true population (Poisson / NB); generate synthetic SPA curves at city and province levels; loop over target R² values (0.10, 0.25, 0.50) for 80 % detection power at varying sample sizes.

## Recommendations

### Use directly
1. **Carleton et al. 2018 PEWMA** — cite for the r ≈ 0.5 / R² ≈ 0.25 practical detection floor; motivates urban-area pre-specification.
2. **Hanson, Ortman & Lobo 2017** — cite R² = 0.267 / 0.361 as the direct published comparator; project's 2024 baseline R² = 0.101 and pre-specified R² ≥ 0.25 are calibrated against this.

### Adapt approach
3. **Kolar et al. 2023** — cite as evidence that SPD researchers adopt Cohen's brackets when forced to be explicit; legitimises Cohen as fallback.
4. **Palmisano et al. 2021** — cite Italian / Near East studies for empirical range of field SPD × covariate r values (–0.68 to +0.77; R² 0.005 to 0.59). Province-level R² ≥ 0.50 pre-specification aligns with the upper end.
5. **Gelman et al. 2019 Bayesian R²** — adopt directly via `rstanarm::bayes_R2()` or `brms`. Report posterior median + 89 % / 95 % credible interval instead of point estimate. **Methodological improvement the project can introduce to the SPD literature** (no precedent found).

### Ignore
- Shennan et al. 2013 (no R²)
- Crema & Bevan 2021 / rcarbon (permutation paradigm only)
- DiNapoli 2021 (ABC distance, not R²)
- ADMUR / nimbleCarbon (BIC / WAIC only)

## Carleton & Groucutt 2021 — critique to address

Carleton & Groucutt (2021, *The Holocene*) argues SPD point-wise regression is fundamentally unreliable because the uncertainty structure of SPDs (joint calibration-uncertainty density) cannot be mapped stably onto covariate observations, making regression parameter estimates biased and standard errors invalid.

**Relevance to current project:** The critique applies primarily to calibrated radiocarbon distributions. **Inscription dates do not have calibration uncertainty in the same sense** — they are aoristic ranges, not Bayesian posteriors over calibrated means. The critique is weaker here. The project should acknowledge it, explain why it applies less strongly to calendar-date aoristic data, and cite Carleton & Groucutt (2021) as the methodological warning being addressed.

## Build-vs-adopt verdict

**For R² brackets:** Build the argument, don't adopt a packaged convention. No field-specific brackets exist. Construct the argument:
1. Cohen generic anchor (R² = 0.26 "large").
2. Carleton et al. 2018 PEWMA detection floor (r = 0.5 → R² = 0.25).
3. Palmisano et al. 2021 empirical range (R² 0.005–0.59 in SPD × climate).
4. Hanson et al. 2017 direct comparator (R² = 0.27–0.36 for inscription × population).

**For power analysis:** Build from scratch, using Carleton et al. 2018 as template. ~200–300 lines of R / Python. Could be released as a reproducibility supplement — a minor novelty contribution to the field.

**For Bayesian R²:** Adopt Gelman et al. 2019 directly via rstanarm or brms. First SPD paper to do so = methodological improvement.

## Verification status

**VERIFICATION PENDING.** Carleton 2018 PLOS ONE supplementary code should be retrieved and checked for adaptation. Hanson et al. 2017 R² values from Table 2 should be verified from the paper directly (royalsocietypublishing.org open access). Palmisano et al. 2021 r values accessed via abstract + secondary sources; full verification requires Springer access for the *J. World Prehistory* paper.

## Sources

- Shennan et al. 2013 — [Nature Comms ncomms3486](https://www.nature.com/articles/ncomms3486)
- Timpson et al. 2014 — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0305440314002982)
- Timpson et al. 2021 — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0305440321001436)
- Crema & Bevan 2021 — [author PDF](https://ercrema.github.io/files/Crema%20and%20Bevan%202021.pdf)
- Crema 2022 review — [Springer](https://link.springer.com/article/10.1007/s10816-022-09559-5)
- Palmisano et al. 2021 Italy — [Springer](https://link.springer.com/article/10.1007/s10963-021-09159-3)
- Palmisano et al. 2021 Near East — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0277379120307010)
- Bevan et al. 2017 — [PMC PNAS](https://pmc.ncbi.nlm.nih.gov/articles/PMC5724262/)
- **Carleton et al. 2018 PEWMA** — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5774753/)
- Carleton et al. 2021 Maya — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8323947/)
- Carleton & Groucutt 2021 — [Holocene SAGE](https://journals.sagepub.com/doi/10.1177/0959683620981700)
- DiNapoli et al. 2021 — [PMC Nature Comms](https://pmc.ncbi.nlm.nih.gov/articles/PMC8225912/)
- **Hanson, Ortman & Lobo 2017** — [Royal Society](https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0367)
- Hanson et al. 2022 PLOS ONE — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9202948/)
- Kolar et al. 2023 — [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0291956)
- Gelman et al. 2019 Bayesian R² — [Taylor & Francis](https://www.tandfonline.com/doi/abs/10.1080/00031305.2018.1549100)
- Vehtari Bayesian R² demo — [avehtari.github.io](https://avehtari.github.io/bayes_R2/bayes_R2.html)
- rcarbon CRAN — [package page](https://cran.r-project.org/web/packages/rcarbon/index.html)
- ADMUR CRAN — [package page](https://cran.r-project.org/package=ADMUR)
- nimbleCarbon — [GitHub](https://github.com/ercrema/nimbleCarbon)
- bayes_R2 — [GitHub](https://github.com/jgabry/bayes_R2)
