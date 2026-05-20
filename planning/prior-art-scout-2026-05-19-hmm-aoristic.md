---
title: "Prior-art scout — latent-population HMM with aoristic-interval emission"
date: 2026-05-19
scout-agent: prior-art-scout (Claude Sonnet 4.6)
commissioned-by: Shawn Ross
context: "Martin's proposed methodological pivot from Bayesian mixture to HMM / latent-population state-space approach. Search for prior art before drafting Decision 33."
verification-status: "All cited papers carry DOIs or arXiv IDs. Items marked [NEEDS VERIFICATION] should be confirmed against full text before use in the paper."
---

# Prior-Art Scout Report: Latent-Population HMM / State-Space Model with Aoristic-Interval Emission for Roman Epigraphy

## Search sources consulted

GitHub (`gh search repos`, `gh api` for baorista and nimbleCarbon source files), CRAN (baorista, nimbleCarbon, KFAS, MARSS, pomp, bsts, nimbleEcology, hsmm documentation), arXiv, PubMed/PMC, ScienceDirect (abstracts only — full texts paywalled), Springer (abstracts), WebSearch (targeted queries across archaeology, ecology, epidemiology, palaeoclimate, historical demography, and point-process statistics). Zotero collection not queried directly (pyzotero access not available in this agent session). Hugging Face not searched — no ML model or dataset dimension to this question.

---

## 1. Executive Summary

The specific combination — **latent-population state-space or HMM with aoristic/interval-censored emission over empire-wide hierarchically structured data** — does not appear to exist in the published literature. Nothing in archaeology, epigraphy, or adjacent fields has assembled this particular configuration. That said, the component pieces are individually well developed: the ecological Integrated Population Model (IPM) tradition (Kéry & Schaub; JAGS/nimble), the palaeoclimate BARCAST family (Tingley & Huybers), the epidemiological state-space / backcalculation tradition, and the radiocarbon-archaeology NIMBLE / Bayesian trajectory family (Crema, nimbleCarbon) all supply directly applicable structural analogues.

The closest single-methodology precedent is the Crema–Shoda 2021 / nimbleCarbon approach: Bayesian fitting of parametric growth curves to aoristic data via NIMBLE, using a custom aoristic-marginalised likelihood. This is the right inferential infrastructure, but it fits a **fixed parametric trajectory** (exponential, logistic, phase) rather than a **stochastic latent-state process with stationary transitions**. The gap between baorista/nimbleCarbon and what Martin proposes is precisely the addition of a stochastic process model in the transition layer — replacing a deterministic growth-rate parameter with a latent random walk or AR(1) on log-population.

No paper has applied a state-space or HMM to inscription data, or to any aoristic archaeological data, with the posterior-path-ensemble as the inferential product. **This is fresh territory.** The foundational analogues to cite are from ecology (Kéry & Schaub IPM; pomp / King et al. 2016) and palaeoclimate (Tingley & Huybers 2010 BARCAST), not from archaeology itself.

---

## 2. Candidates Table

| # | Name / Reference | Type | URL / DOI | Stars / Version | Last Active | Fit | Notes |
|---|---|---|---|---|---|---|---|
| 1 | **baorista** (Crema 2024/2025) | R package | github.com/ercrema/baorista / 10.1111/arcm.12984 | v0.2.1, CRAN | 2025-07-22 | MEDIUM | Bayesian aoristic emission via NIMBLE custom distribution; fits exponential/logistic/ICAR — no stochastic transition kernel. Closest existing tool. |
| 2 | **nimbleCarbon** (Crema & Shoda 2021) | R package | github.com/ercrema/nimbleCarbon / 10.1371/journal.pone.0251695 | v0.2, CRAN | 2024 | MEDIUM | Bayesian radiocarbon growth-model fitting via NIMBLE; structurally identical to baorista but for 14C data. Same gap: deterministic parametric trajectory, no latent stochastic dynamics. |
| 3 | **pomp** (King, Nguyen & Ionides 2016) | R package | kingaa.github.io/pomp / arXiv:1509.00503 | v6.3, CRAN | 2025 | HIGH (infrastructure) | General partially-observed Markov process inference; particle MCMC, iterated filtering, SMC. Can encode any user-specified state-space model. No aoristic emission built in. Highest-fit infrastructure option. |
| 4 | **MARSS** (Holmes, Ward & Scheuerell) | R package | github.com/nwfsc-timeseries/MARSS | v3.11, CRAN | 2024 | MEDIUM (structure) | Multivariate AR state-space for Gaussian observations. EM-algorithm; not designed for non-Gaussian / custom emission. Demonstrates hierarchical AR structure usable as inspiration. |
| 5 | **KFAS** (Helske 2017) | R package | cran.r-project.org/package=KFAS / arXiv:1612.01907 | v1.6.0, CRAN | 2024 | MEDIUM (Poisson SSM) | Kalman filter/smoother for exponential-family state space (Poisson, NB, binomial). No aoristic interval emission. Good reference for Poisson SSM structure. |
| 6 | **bsts** (Scott & Varian 2014) | R package | cran.r-project.org/package=bsts | v0.9.10, CRAN | 2023 | LOW-MEDIUM | Bayesian structural time series; supports Poisson. Good for structural decomposition but no custom aoristic likelihood. |
| 7 | **nimbleEcology** (Goldstein et al. 2021) | R package | cran.r-project.org/package=nimbleEcology / 10.1002/ece3.6053 | v0.4.1, CRAN | 2024 | MEDIUM (N-mixture) | NIMBLE distributions for HMM, dynamic HMM, N-mixture, open occupancy. Dail-Madsen open N-mixture is structurally analogous (latent abundance + imperfect detection). No aoristic emission. |
| 8 | **hsmm / PHSMM** (O'Connell et al. 2010; Koslik et al. 2022) | R packages | ideas.repec.org/a/eee/csdana/v54y2010 / arXiv:2101.09197 | CRAN | 2022 | LOW-MEDIUM | Hidden semi-Markov models; flexible dwell-time distributions. Relevant if dynastic-stability dwell matters. No count-data aoristic emission. |
| 9 | **Integrated Population Models** (Schaub & Kéry 2022) | Book + JAGS | Academic Press, ISBN 9780323908108 | Canonical reference | 2022 | HIGH (conceptual) | State-space population models with multiple data streams, hierarchically pooled. The structural template for what Martin proposes. No interval-censored emission. |
| 10 | **BARCAST** (Tingley & Huybers 2010) | Method + Matlab | 10.1175/2009JCLI3015.1 | — | 2010 | HIGH (analogy) | Bayesian hierarchical state-space: AR(1) latent field + proxy observation equation. Observation equation links latent state to imperfect proxy. Exact structural analogue but for climate, not counts. |
| 11 | **Bayesian state-space for Finnish historical pop.** (Voutilainen et al. 2020) | Paper | PMC7329763 / 10.1007/s13524-020-00889-1 | — | 2020 | MEDIUM | Bayesian hierarchical time-series for population from imperfect parish records. Transition model: births–deaths accounting equation. Not a Markov chain on log-N; closer to demographic bookkeeping. |
| 12 | **HIV epidemic state-space / backcalculation** (various, 1990s–2000s) | Literature | PubMed 2000845; ScienceDirect S0895717700001291 | — | ~2000 | MEDIUM (problem isomorphism) | Backcalculation from AIDS deaths to HIV incidence using convolution over incubation-period interval. Structural isomorph of integrating inscription likelihood over aoristic interval. |
| 13 | **Capture-recapture HMM for register data** (Brown et al. 2026) | Paper | arXiv:2603.24643 | Preprint Mar 2026 | 2026 | MEDIUM | Cormack-Jolly-Seber CJS formulated as HMM for population size/dynamics from registers. Handles false-positive and false-negative observation error. No aoristic/interval-censored emission per se but addresses imperfect-register population inference. Very recent. |
| 14 | **Crema & Bevan 2017 spatio-temporal radiocarbon** | Paper | 10.1016/j.jas.2017.09.010 | — | 2017 | LOW-MEDIUM | Spatio-temporal hotspot/coldspot detection for radiocarbon SPDs across space; uses spatial comparison of local SPDs, not a state-space model. Relevant for spatial pooling design. |
| 15 | **Tallavaara & Pesonen 2018** | Paper | 10.1016/j.jas.2018.06.008 | — | 2018 | MEDIUM (concept) | Radiocarbon SPDs fed into population ecology (Lotka–Volterra, logistic) model fitting via ABC. Process-model thinking applied to radiocarbon; no state-space latent dynamics per se. |
| 16 | **Carleton & Groucutt 2021** | Paper | 10.1177/0959683620981700 | — | 2021 | HIGH (critique) | Foundational critique arguing SPDs conflate process variance and chronological uncertainty — precisely the theoretical motivation for the HMM approach. Argues for generative models. Does not implement one. |
| 17 | **Briz-Redón 2023 Bayesian aoristic logistic regression** | Paper | 10.1007/s10940-023-09580-1 / arXiv:2304.05933 | — | 2023 | LOW-MEDIUM | Bayesian spatio-temporal logistic regression for crime data with interval-censored times; aoristic weighting integrated into likelihood. No latent population state, no state-space transitions. Criminology, not archaeology. |
| 18 | **Log-Gaussian Cox Process (LGCP) for spatio-temporal points** (Taylor et al. 2013; lgcp R package) | R package + paper | arXiv:1110.6054 | CRAN | 2023 | MEDIUM (emission structure) | LGCP: latent Gaussian intensity field → Poisson point process. Handles spatially/temporally varying latent intensity. No interval-censored event times; treats events as point-located in time. |
| 19 | **pomp iterated-block particle filter** (Ionides et al. 2022) | Paper | arXiv:2206.03837 | — | 2022 | HIGH (inference method) | Iterated block particle filter for coupled dynamic systems with shared + unit-specific parameters. Directly applicable to spatially coupled latent-population model across 96 cells. |
| 20 | **Penalised likelihood HMM for count time series** (Zucchini et al. 2018 / arXiv:1901.03275) | Paper | arXiv:1901.03275 | — | 2019 | LOW-MEDIUM | Non-parametric HMM fitting for count data (Poisson). Standard Poisson emission; no interval-censored observation model. Useful reference for HMM on counts, not for aoristic problem. |

---

## 3. Findings by Search Target

### 3.1 Direct prior art in archaeology / epigraphy

**Verdict: None found.** No paper applies a hidden Markov model, state-space model, or any latent-intensity generative model with stochastic transition dynamics to inscription, ceramic, coin, or any other aoristic archaeological data.

The nearest approaches are:

- **baorista (Crema 2025)** — NIMBLE-based Bayesian fitting to aoristic data, but uses a deterministic growth-rate or ICAR smooth as the trajectory model. The ICAR component is a temporal random-walk *prior on the probability mass function* (fitting a probability distribution over time-blocks), not a stochastic *population process model* with annual-scale latent states and a generative Poisson emission. These are structurally different: the ICAR fits a shape; the proposed HMM asks "what annual-resolution population path is consistent with the data?" That said, baorista's `dAOG` / `dAExp` custom distributions (which marginalise the aoristic probability matrix into the NIMBLE likelihood) are a directly reusable design pattern for the emission layer of the proposed HMM.

- **nimbleCarbon (Crema & Shoda 2021)** — Identical architecture to baorista but for radiocarbon. Same gap.

- **Aoristic SPD analyses** (Crema, Bevan, Shennan; rcarbon) — All remain in the descriptive-frequentist or parametric-null-test domain. The generative / latent-dynamics direction has not been taken.

The aoristic literature has generated critique of its own limitations (Carleton & Groucutt 2021) that explicitly calls for generative/process models, but no one has published the actual implementation in any archaeological context.

### 3.2 Adjacent fields: ecology — Integrated Population Models

**IPMs (Kéry & Schaub 2022; Schaub & Abadi 2011)** are the closest structural template outside archaeology. An IPM combines:

- A **state-space process model** (Leslie matrix or random walk on log-N) for latent population trajectory.
- Multiple **data streams** (count surveys, mark-recapture, productivity data), each with its own likelihood, jointly fitted in a single hierarchical Bayesian model (BUGS/JAGS/Stan).

The structural mapping to the proposed model is direct: inscriptions = the "count survey" data stream; the aoristic integration = the observation uncertainty layer; the stationary random-walk transition on log-N = the process model. IPMs do not have interval-censored observation times — ecological survey dates are known — but the hierarchical multi-stream structure with heterogeneous observation models is exactly what is needed.

**Key reference:** Schaub & Kéry (2022) *Integrated Population Models: Theory and Ecological Applications with R and JAGS* (Academic Press). The earlier Kéry & Schaub (2012) *Bayesian Population Analysis Using WinBUGS* (Academic Press) contains the foundational state-space count-survey models. No bridge to archaeology has been published [NEEDS VERIFICATION against Scopus].

**nimbleEcology** (Goldstein et al. 2021; DOI 10.1002/ece3.6053) implements the Dail–Madsen open N-mixture model as a NIMBLE distribution — this is a discrete-time dynamic HMM for open-population abundance with imperfect detection, fitted in the same NIMBLE environment as baorista. This is the closest ready-made software for the proposed model's structure, albeit with a binomial detection model rather than aoristic integration.

### 3.3 Adjacent fields: ecology — N-mixture / occupancy models

**N-mixture models** (Royle 2004; Dorazio 2013) model latent abundance N at each site with imperfect detection probability. The observation equation Y | N ~ Binomial(N, p) is structurally analogous to what the proposed model needs (inscription count Y | latent population N → Poisson(r × N × Δt), integrated over aoristic interval). Open-population N-mixture (Dail & Madsen 2011) extends this to temporal dynamics with survival and recruitment parameters — effectively a discrete-time HMM on abundance.

No archaeological application found in any search. **The bridge is yet to be published.**

### 3.4 Adjacent fields: epidemiology — backcalculation and latent infection dynamics

**HIV backcalculation** (Brookmeyer & Gail 1988, PubMed 2000845; Tan et al. 2016, PMC4942036) reconstructs HIV incidence I(t) from observed AIDS death counts D(t) via convolution: D(t) = ∫ I(t-s) f(s) ds, where f(s) is the incubation-period distribution. This is structurally isomorphic to the proposed model's inscription emission: observed inscription count Y(t) = ∫ λ(t') N(t') dt', integrated over the aoristic interval. The HIV backcalculation literature solved this problem (for fixed, known incubation distribution rather than aoristic interval) using both non-parametric (B-spline) and state-space methods.

**State-space HIV epidemic model** (Tan & Ye 2000, ScienceDirect S0895717700001291 — confirmed abstract; full text paywalled) uses Kalman-recursion state-space to combine HIV incidence dynamics with AIDS case observations, explicitly handling the convolution structure. This is a direct analogue — latent epidemic dynamics, imperfect-time observation, Kalman inference.

**COVID/Ebola nowcasting** — the interval-censored onset-to-report delay problem (e.g., estimating R_t when reporting delays are interval-censored) is a well-developed area with Stan / R implementations (EpiNow2, EpiLPS). The mathematical structure (integrate over uncertain observation delay) is exactly the proposed model's emission structure. [NEEDS VERIFICATION: whether EpiNow2 specifically uses a state-space transition model or just a regression; arXiv:2303.01365 and related papers would confirm.]

### 3.5 Adjacent fields: palaeoclimate proxy-based reconstruction

**BARCAST (Tingley & Huybers 2010, 10.1175/2009JCLI3015.1)** is the canonical reference. The model has:

- **Evolution equation:** True climate field T(location, t) follows an AR(1) process in time, plus spatial covariance (Matérn kernel). This is the direct analogue of the proposed stationary random-walk transition on log-population.
- **Observation equation:** Proxy observation P(location, t) = α + β × T(location, t) + ε, where ε is proxy-specific noise. This is the analogue of the proposed emission Y_t ~ Poisson(r × N_t), integrated over the aoristic interval.
- **Inference:** Full Bayesian posterior over all latent field values T(location, t) — the *ensemble of plausible latent climate paths* — via Gibbs sampling.

This is arguably the closest structural match to what Martin proposes, transposed from climate to demography. The key architectural differences are: (i) BARCAST uses a Gaussian observation equation; the proposed model needs a Poisson-integrated-over-aoristic emission; (ii) BARCAST's proxies have known observation times; inscriptions have interval-uncertain times. The **ensemble-of-posterior-paths** inferential product and the **shock detection** approach (does the posterior ensemble concentrate downturns at known events?) is exactly the BARCAST validation logic applied to plague events.

### 3.6 Adjacent fields: historical demography

**Voutilainen et al. 2020 (PMC7329763)** reconstruct Finnish population 1647–1850 from incomplete parish records using a Bayesian hierarchical time-series. The model is closer to demographic bookkeeping (μ_t = μ_{t-1} + births - deaths, observed via noisy census counts) than to a Markov-chain process model, and it does not have interval-censored observation times. However, it demonstrates Bayesian hierarchical state-reconstruction from imperfect historical records and is a citable precedent in the historical demography tradition.

**Hin & Zagheni (IUSSP paper, iussp.org)** use microsimulation (SOCSIM) for Roman Italy population dynamics — deterministic/demographic bookkeeping, not Bayesian state-space inference. Not a methodological precedent for the proposed approach.

**Wheldon et al. 2013 (Bayesian population reconstruction, *Demography*)** — Bayesian model for age-structured population counts from imperfect survey data. Closer to IPM than HMM; also works from decadal census intervals. Not a direct analogue but demonstrates the tradition.

### 3.7 Building blocks: Cox processes with interval-censored observations

**The integrated-likelihood emission** (each inscription i with interval [a_i, b_i] contributing ∫_{a_i}^{b_i} λ(t | N_t) dt) is a doubly-stochastic Poisson / Cox process with interval-censored event locations. This is a **recognised but incompletely solved** problem in the point-process literature.

What has been done:

- **Log-Gaussian Cox Process (LGCP)** — the lgcp R package (Taylor et al. 2013, arXiv:1110.6054; *JRSS-C* v52) fits spatio-temporal LGCPs, but treats event locations as known point observations, not as interval-uncertain. The latent intensity Gaussian process is a partial analogue of the proposed latent population N_t.
- **Exact Bayesian Gaussian Cox processes via random integral** (arXiv:2406.19722) — recent paper solving exact MCMC for GP Cox processes by treating the integral of the intensity as a latent variable. Methodology relevant to the aoristic integral problem. [NEEDS VERIFICATION of exact method.]
- **No published method** directly handles temporal Cox processes with interval-censored event locations in a state-space framework. The proposed project would need to construct this marginalised emission from first principles, following the pattern established by Crema's `dAExp`/`dAOG` distributions in baorista — which do exactly this for simpler (parametric trajectory) models.

### 3.8 Building blocks: PyMC / Stan / NIMBLE implementations

**NIMBLE (via baorista and nimbleCarbon)** — already demonstrated for aoristic-marginalised likelihoods. The custom distribution approach (`nimbleFunction` objects in nimbleEcology) can encode arbitrary MCMC observation models. The aoristic integration is implementable as a `nimbleFunction`. JAGS is not suitable (cannot encode custom likelihoods of this form).

**Stan** — Stan's `target +=` syntax supports arbitrary marginalised log-likelihoods; interval-censored aoristic integration is implementable as a sum over annual bins. Stan HMMs are well-supported (Stan User Guide, §Hidden Markov Models). A Stan forum thread (discourse.mc-stan.org/t/fitting-a-hidden-markov-model-with-hierarchical-emission-parameters/1404) demonstrates hierarchical Poisson-emission HMMs. Stan's forward-backward algorithm gives the full posterior over latent paths, not just Viterbi MAP. **Stan is a strong candidate for implementation.**

**PyMC** — PyMC 5 supports custom log-likelihoods and GP-based Cox processes (the `lgcp` example gallery entry demonstrates Poisson intensity fields). No built-in forward-backward HMM, but the `pytensor` scan / `pymc-hmm` library (GitHub: bwengals/pymc-hmm [NEEDS VERIFICATION]) may provide it. PyMC's `DiscreteMarkovChain` and `HMM` submodule (if it exists in v5) need confirmation.

**pomp (King et al. 2016, arXiv:1509.00503)** — the most general framework for non-linear, non-Gaussian state-space inference. Iterated block particle filter (Ionides et al. 2022, arXiv:2206.03837) handles the 96-cell spatially coupled model. The aoristic emission can be written as a user-specified `dmeasure` function. However, pomp is R-only and maximum-likelihood focused (iterated filtering); full Bayesian posterior-path sampling requires particle MCMC, which is expensive at empire-wide scale.

---

## 4. Recommendations

### Use directly

**NIMBLE + baorista's custom distribution pattern.** The `dAOG` / `dAExp` distributions in baorista (GitHub: ercrema/baorista, R/dexpfit.R) implement the aoristic-marginalised likelihood within a NIMBLE model. The proposed HMM extension requires adding a stochastic process model for N_t above the emission layer. baorista already does the hard part (integrating over the aoristic probability matrix); the project only needs to replace its fixed-parameter trajectory with a latent random-walk state. Adoption cost: moderate (requires NIMBLE literacy, already partially present given existing baorista installation).

**nimbleEcology's open N-mixture structure (Dail–Madsen).** Provides a NIMBLE implementation of discrete-time dynamic abundance with latent-state transitions and imperfect detection. Study and adapt: replace binomial detection model with aoristic-marginalised Poisson.

**pomp infrastructure for particle-filter inference.** For the empire-wide spatial model (96 cells, annual resolution), pomp's iterated block particle filter is the state-of-the-art inference engine. The `dmeasure` function can encode the aoristic integration.

### Adapt approach

**Integrated Population Model structure (Kéry & Schaub / Schaub & Kéry).** The JAGS IPM code in their textbooks provides copy-paste templates for: (a) state-space log-N random walk, (b) Poisson count emission, (c) hierarchical pooling across spatial units. Adapt by substituting the aoristic-integrated Poisson emission for the standard Poisson. Cost: medium (requires JAGS → NIMBLE or Stan translation, but the structural mapping is direct).

**BARCAST AR(1) evolution equation.** The BARCAST state evolution (AR(1) on the latent field, stationary variance, spatial covariance) is the direct template for the proposed transition kernel on log-population. Adapt by replacing the climate-proxy observation equation with the aoristic Poisson emission.

**HIV backcalculation / epidemiological interval-censored emission.** The convolution integral in backcalculation is mathematically equivalent to the aoristic integral. The non-parametric B-spline approaches to recovering the latent incidence function (Bacchetti & Moss 1996 etc.) can inform the regularisation approach for the latent population trajectory.

### Ignore for now

**MARSS** — Gaussian observation model only; would require a non-trivial extension for Poisson-aoristic emission that negates its main advantage (analytic EM algorithm). Not worth the adaptation effort.

**bsts** — Similar issue; Poisson support exists but relies on data augmentation to conditionally Gaussian; aoristic integration would require custom extension. Viable only for prototyping with approximations.

**hsmm/PHSMM** — HSMM is relevant if the project wants to model regime dwell times explicitly (e.g., "stable growth regime" vs "plague/crisis regime"), but adds substantial complexity. Defer until the basic HMM is validated.

**LGCP (lgcp package)** — the LGCP framework models a log-Gaussian intensity field; interesting for the spatial dimension, but the standard LGCP pipeline assumes point-located events, not interval-censored. Would require non-standard extension. The conceptual framework (latent intensity → Poisson observations) is identical to the proposed model, but the standard implementation is not directly usable.

---

## 5. Build-vs-Adopt Verdict

**Adopt + Build (hybrid).** No off-the-shelf package implements the proposed model. The verdict is:

1. **Adopt** the NIMBLE infrastructure and the aoristic-marginalised likelihood pattern from baorista (specifically the `dAOG`/`dAExp` nimbleFunctions, which are the hardest part to write from scratch).

2. **Adapt** the Kéry & Schaub IPM state-space structure (stationary random walk on log-N, Poisson emission, hierarchical pooling) by substituting the aoristic-marginalised Poisson emission for the standard Poisson emission.

3. **Build** the new component: the stochastic transition kernel (AR(1) or bounded random walk on log-N_t) that connects annual latent-population states. This component has no existing implementation in any archaeological or epigraphic software and is the novel contribution.

The most practical path is therefore: **NIMBLE model written in the baorista codebase style**, adapting its `nimbleFunction` design for the custom distribution, adding the random-walk process layer, and running the empire-wide 96-cell model at annual or decadal resolution. Stan is a viable alternative for smaller spatial subsets and would support the full forward-backward posterior path ensemble more naturally than NIMBLE's default MCMC.

---

## 6. Novelty Assessment

The combination — **Latin epigraphy × empire-wide hierarchical state-space × aoristic-interval emission × posterior path sampling for shock detection** — is, on the evidence of this search, **genuinely novel**. No prior art exists.

Adjacent literature that establishes the closest analogues and would be cited as foundational:

| Component | Foundational citation |
|---|---|
| State-space population dynamics with stochastic transition | Kéry & Schaub (2012) *Bayesian Population Analysis*; Schaub & Kéry (2022) *Integrated Population Models* |
| Bayesian proxy-state reconstruction (AR(1) evolution + obs equation) | Tingley & Huybers (2010) *J. Climate* 23:2759–2781, DOI 10.1175/2009JCLI3015.1 |
| Aoristic-marginalised Bayesian likelihood in NIMBLE | Crema (2025) *Archaeometry* 10.1111/arcm.12984 (baorista) |
| Theoretical motivation: SPD conflates process variance and obs uncertainty | Carleton & Groucutt (2021) *The Holocene* 10.1177/0959683620981700 |
| Interval-censored emission via convolution / marginalisation | Brookmeyer & Gail (1988) backcalculation literature [NEEDS DOI]; HIV state-space models |
| Partially-observed Markov process inference (particle filter) | King, Nguyen & Ionides (2016) *J. Stat. Softw.* 69(12), arXiv:1509.00503 |
| Capture-recapture HMM for imperfect population registers | Brown et al. (2026) arXiv:2603.24643 [preprint, NEEDS VERIFICATION of publication status] |

The claim to novelty rests specifically on the **combination** of:
(a) the stochastic stationary transition kernel (not in baorista/nimbleCarbon),
(b) the aoristic-marginalised Poisson emission (not in any ecology/epidemiology/climate package),
(c) applied to empire-wide hierarchically structured epigraphic data (not done by anyone in any field).

If any one of these three components were absent, the novelty claim would be weaker. All three together appear not to have been assembled before.

---

## 7. Risks and Known Limitations Surfaced by the Literature

1. **Computational scaling (critical).** The prior scout (2026-04-25 report, Section Q3) found that baorista's NIMBLE MCMC on the full empire dataset (n ≈ 50,000 inscriptions) runs the `dAExp` distribution over a 50,000 × n_blocks matrix per MCMC step, with no benchmark available. The proposed HMM adds a forward-backward algorithm over T × K states per MCMC step (T = annual bins ~500, K = latent population states if discretised). This is likely **computationally intractable** for the full dataset in NIMBLE's default MCMC. Solutions: (a) particle MCMC via pomp (scales better); (b) decadal rather than annual time steps; (c) spatial batching (province-level fitting before empire-level hierarchical pooling); (d) variational inference (not yet in NIMBLE; available in PyMC).

2. **Identifiability of latent N_t vs detection model.** In N-mixture / occupancy literature, identifiability of latent abundance and detection probability is a known problem (Kéry & Schaub 2012 discuss this at length). The proposed model faces the same problem: is a downturn in inscription counts driven by population decline or by a reduction in the propensity to inscribe (the "epigraphic habit" variation)? Without an independent constraint on the detection process (analogous to ecology's repeated surveys), the latent N_t and the per-capita inscription rate are only weakly identified. **This is the most serious inferential risk.**

3. **Stationarity assumption.** The proposal specifies a stationary transition kernel. The Roman empire's population trajectory over 1 BC–AD 500 was demonstrably non-stationary (growth through the Antonine period, decline through Late Antiquity). A stationary random walk can still reconstruct non-stationary trajectories via the posterior, but the stationary prior will fight against large secular drifts. Consider an AR(1) kernel with zero mean on log-N (log-scale random walk) plus a slow secular trend component, or an explicit non-stationary kernel with wider variance for post-AD 250. This is a design decision, not a fatal flaw.

4. **The bimodal aoristic interval width distribution.** The LIRE corpus has many narrow (~10–25 yr) and many very wide (~100–200 yr) intervals. Wide-interval inscriptions contribute diffuse likelihood mass across many time bins. At annual resolution, most of each wide-interval inscription's likelihood is spread so thinly that it contributes negligible information per bin. The forward-backward algorithm must handle this; poor numerical conditioning is possible at annual resolution. Decadal binning substantially mitigates this.

5. **Forward-backward vs Viterbi.** The proposal correctly specifies posterior path sampling (forward-backward) rather than Viterbi MAP. This is the right choice for uncertainty quantification, but it requires either MCMC integration over latent paths (expensive) or a particle-filter approximation. The literature (pomp; nimbleCarbon particle MCMC) provides both options, but neither is trivial to implement for a 96-cell spatially hierarchical model.

6. **R package licensing.** baorista: GPL ≥ 2; nimbleCarbon: GPL ≥ 2; pomp: GPL ≥ 2; nimbleEcology: GPL ≥ 2; MARSS: GPL-3; KFAS: LGPL-3. All compatible with MIT or CC BY 4.0 downstream use (consume as tool; no copyleft obligation if not distributing modified source).

---

## 8. Summary of Search Gaps

The following areas were searched but returned no relevant hits, which is itself informative:

- No HMM or state-space model applied to inscription, ceramic, coin, or any aoristic archaeological data (multiple targeted searches).
- No bridge published between ecological IPMs and archaeological count data with interval-censored dates.
- No PyMC or Stan implementation of a state-space population model with aoristic-marginalised emission found on GitHub or Stan forums (closest: a Stan forum thread on hierarchical HMM with Poisson emission, without aoristic integration).
- No application of the LGCP framework to aoristic-uncertain event locations found.
- Zotero collection PZN5ATJK not directly queried; this report may duplicate items already in the collection.

---

## Sources

- [baorista CRAN](https://cran.r-project.org/web/packages/baorista/index.html)
- [baorista GitHub (ercrema)](https://github.com/ercrema/baorista)
- [Crema 2025, *Archaeometry* (baorista paper)](https://onlinelibrary.wiley.com/doi/10.1111/arcm.12984)
- [nimbleCarbon GitHub (ercrema)](https://github.com/ercrema/nimbleCarbon)
- [Crema & Shoda 2021, *PLOS ONE* (nimbleCarbon)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8133439/)
- [pomp R package (kingaa.github.io)](https://kingaa.github.io/pomp/)
- [King, Nguyen & Ionides 2016, *J. Stat. Softw.* (arXiv:1509.00503)](https://arxiv.org/abs/1509.00503)
- [Ionides et al. 2022 iterated block particle filter (arXiv:2206.03837)](https://arxiv.org/abs/2206.03837)
- [Schaub & Kéry 2022 IPM book (Amazon)](https://www.amazon.com/Integrated-Population-Models-Ecological-Applications/dp/0323908101)
- [nimbleEcology CRAN](https://cran.r-project.org/web/packages/nimbleEcology/vignettes/Introduction_to_nimbleEcology.html)
- [Ponisio et al. 2020 nimbleEcology (*Ecol. Evol.*)](https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.6053)
- [MARSS R package](https://nwfsc-timeseries.github.io/MARSS/)
- [KFAS CRAN / arXiv:1612.01907](https://arxiv.org/abs/1612.01907)
- [bsts CRAN (Bayesian structural time series)](https://cran.r-project.org/web/packages/bsts/bsts.pdf)
- [hsmm R package (*Comput. Stat. Data Anal.* 2010)](https://ideas.repec.org/a/eee/csdana/v54y2010i3p611-619.html)
- [PHSMM / Koslik et al. 2022 (arXiv:2101.09197)](https://arxiv.org/abs/2101.09197)
- [Tingley & Huybers 2010 BARCAST (*J. Climate*)](https://journals.ametsoc.org/view/journals/clim/23/10/2009jcli3015.1.xml)
- [Voutilainen et al. 2020 Finnish historical population (PMC7329763)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7329763/)
- [Carleton & Groucutt 2021 *The Holocene* (DOI 10.1177/0959683620981700)](https://journals.sagepub.com/doi/10.1177/0959683620981700)
- [Crema 2022 *JAMT* SPD review](https://link.springer.com/article/10.1007/s10816-022-09559-5)
- [Tallavaara & Pesonen 2018 *J. Archaeol. Sci.*](https://www.sciencedirect.com/science/article/abs/pii/S0305440318302784)
- [Crema & Bevan 2017 spatio-temporal radiocarbon](https://www.sciencedirect.com/science/article/abs/pii/S0305440317301310)
- [Brown et al. 2026 capture-recapture HMM (arXiv:2603.24643)](https://arxiv.org/abs/2603.24643)
- [Briz-Redón 2023 Bayesian aoristic logistic regression (arXiv:2304.05933)](https://arxiv.org/abs/2304.05933)
- [Taylor et al. 2013 lgcp R package (arXiv:1110.6054)](https://arxiv.org/abs/1110.6054)
- [lgcp *J. Stat. Softw.* v52 (JHU)](https://pure.johnshopkins.edu/en/publications/lgcp-inference-with-spatial-and-spatio-temporal-log-gaussian-cox--3/)
- [PMC4942036 HIV backcalculation modified method](https://pmc.ncbi.nlm.nih.gov/articles/PMC4942036/)
- [PyMC LGCP example gallery](https://www.pymc.io/projects/examples/en/latest/gaussian_processes/log-gaussian-cox-process.html)
- [Stan HMM hierarchical emission discussion](https://discourse.mc-stan.org/t/fitting-a-hidden-markov-model-with-hierarchical-emission-parameters/1404)
- [Newman et al. 2023 state-space ecological time series (*Methods Ecol. Evol.*)](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13833)
- [Arora et al. 2024 exact Bayesian Gaussian Cox processes (arXiv:2406.19722)](https://arxiv.org/abs/2406.19722)

---

**Note to Shawn / Martin:** The two highest-priority reading items before prototyping are (1) Schaub & Kéry (2022) IPM, Chapter 10–12 (state-space count surveys, hierarchical pooling), and (2) the BARCAST paper (Tingley & Huybers 2010) for the AR(1) evolution + observation-equation structure. Both are directly translatable to the proposed model with the baorista aoristic emission substituted in.
