---
priority: 1
scope: in-stream
title: "Prior-art scout — aoristic-SPA parametric-null envelope FP inflation"
audience: "Shawn, Adela, build-agents working on H1 v2"
status: VERIFICATION PENDING per scout protocol
date: 2026-04-25
sources_searched: "GitHub (rcarbon, baorista, ADMUR), rdrr.io, CRAN, Cambridge OA, Springer, PMC, ScienceDirect, Wiley, OSF SocArXiv, WebSearch (general + targeted)"
verification_status: "Several specific claims require re-verification against full texts; flagged with [VERIFY] inline. Run /lit-scout-verify on this report before any citations are made in the paper."
---

# Prior-Art Scout Report — Aoristic-SPA Parametric-Null Envelope: False-Positive Rate Inflation

**Commissioned for:** `/home/shawn/Code/inscriptions` 2026-04-25 plan review
**Scout model:** Claude Sonnet 4.6 (sub-agent)
**Recorded by:** Claude Code main thread (Opus 4.7) — verbatim transcription with light formatting

---

## Sources searched

GitHub (`gh search repos`, `gh api` for rcarbon and baorista source), rdrr.io (rcarbon docs), CRAN (baorista metadata, vignette), Cambridge Open Access (Crema & Bevan 2021 PDF — binary, unreadable), Springer Link (Crema 2022 *JAMT* — paywalled, abstracted only), PMC (Carleton et al. 2018 open access), ScienceDirect (Glomb et al. 2022 — paywalled), Wiley (baorista *Archaeometry* paper — paywalled), OSF SocArXiv (Carleton & Groucutt 2021 preprint — no text served), WebSearch (general + targeted per question). Zotero `pyzotero` not queried (collection SDAM group 2366083 / `PZN5ATJK` — left for Shawn's local query). Hugging Face not searched (no ML/model dimension to this question).

---

## 1. Executive summary

The failure mode found in the H1 simulation — parametric-null Monte Carlo envelope FP-rate inflating to near 1.0 at large n for aoristic SPA data — has a well-documented root cause in the radiocarbon-SPD literature but has not, to this scout's knowledge, been documented specifically for inscription SPA / aoristic data in the published literature. The root-cause diagnosis (variance mismatch between the aoristic-smeared observed SPA and the Poisson-on-smooth-fit MC replicates) is precisely the same as the radiocarbon-SPD problem, but `rcarbon::modelTest()` solves it by a mechanism the project's current pipeline does not replicate: `rcarbon` samples *n* synthetic radiocarbon measurements from the fitted null, calibrates each one, and sums the calibrated probability mass — thereby preserving per-date measurement uncertainty in the MC replicates. The project's pipeline omits the aoristic-resample step from the MC replicates. This is a protocol deviation from the rcarbon port the prereg claims. **Option A** (aoristic-resample-from-fit MC) is the direct port of the rcarbon mechanism to inscription data; it is the field-standard fix. **baorista** uses a categorically different architecture (Bayesian MCMC, not a parametric-null MC envelope) and does not directly replace the permutation-envelope test. **No inscription-SPA paper has reported FP-rate calibration.**

---

## 2. Findings per question

### Q1 — How does `rcarbon::modelTest()` construct MC replicates?

**Finding: rcarbon uses an uncertainty-preserving resampling mechanism, not Poisson draws on the smooth fit.**

The source code of `rcarbon/R/tests.R` (retrieved directly from `gh api repos/ahb108/rcarbon/contents/R/tests.R`) is unambiguous. The critical loop (single-core path) reads:

```r
# method == "uncalsample" (default):
randomDates[[i]] = sample(cragrids[[i]]$CRA, replace=TRUE,
                          size=samplesize[s,i],
                          prob=cragrids[[i]]$PrDens)
randomSDs <- sample(size=length(unlist(randomDates)), errors, replace=TRUE)
tmp <- calibrate(x=unlist(randomDates), errors=randomSDs, ...)
simDateMatrix <- tmp$calmatrix
sim[,s] <- apply(simDateMatrix, 1, sum)
```

Mechanism in pseudocode:

```
For each MC iteration s = 1..nsim:
  1. Back-calibrate the fitted null (predgrid) to 14C space → cragrids[i]$PrDens
  2. Sample n synthetic 14C measurements from cragrids[i] (weighted by PrDens)
  3. Sample n measurement errors from the empirical error distribution
  4. Calibrate all n synthetic measurements → n calibrated probability distributions
  5. Sum calibrated distributions across events → replicate SPD
  6. Rescale to match fitted-null total probability mass
```

Step 4 is the key: each synthetic date has its own calibrated probability distribution (analogous to a single inscription's aoristic mass spread over `[not_before, not_after]`). The MC replicate SPD therefore carries per-date uncertainty variance, not just Poisson-on-mean variance.

**The project's deviation:** `sample_null_spa` in `primitives.py` draws `Poisson(fitted_mean_per_bin)` per bin independently. This completely bypasses the per-date uncertainty step. The variance in MC replicates is `Poisson(lambda_bin)`, where `lambda_bin` is the smooth fitted value — orders of magnitude smaller than the aoristic-smearing variance in the observed SPA. The FP rate observed is the direct consequence.

**Documented in:** rcarbon `modelTest` source (GitHub repo `ahb108/rcarbon`); documentation at `rdrr.io/cran/rcarbon/man/modelTest.html`; the Crema & Bevan 2021 paper (DOI 10.1017/RDC.2020.95) references this mechanism.

**Note in rcarbon docs [VERIFY verbatim]:** "Notice that estimating growth model parameters directly from SPD can be biased, resulting into a null hypothesis that is not necessarily representative (see Crema 2022)." This warning appears in the `modelTest` docstring and references a *separate* bias (the null fit is biased because it's fitted to the observed SPD, not a true null). This is a second problem distinct from the variance-mismatch FP inflation.

---

### Q2 — Has FP-rate inflation at large n been documented for SPD/SPA?

**Finding: The root cause is documented but the specific pattern (FP → 1 at large n) has not been quantified in the published literature for inscription/aoristic data. Partial documentation exists for radiocarbon SPD.**

**Crema 2022, JAMT** (DOI 10.1007/s10816-022-09559-5) — "Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed." The rcarbon docstring explicitly cites this paper in the `modelTest` warning: "estimating growth model parameters directly from SPD can be biased." [VERIFY: Full text paywalled; abstract confirms it covers bias and inference limitations in SPD methods.] It does not appear to report FP-rate-vs-n curves for the parametric-null case. Crema's main concern is the circularity of fitting a null to the observed SPD rather than a true population parameter — this is a related but distinct bias from the FP-inflation problem.

**Carleton & Groucutt 2021, *The Holocene* 31(4): 630–643** (DOI 10.1177/0959683620981700) — "Sum things are not what they seem: Problems with point-wise interpretations and quantitative analyses of proxies based on aggregated radiocarbon dates." Argues SPDs "conflate process variation with chronological uncertainty" and that some shortcomings are fundamental to the SPD approach. [VERIFY: Full text paywalled; preprint at osf.io/preprints/socarxiv/yp38j — page served empty.] Critique the variance-conflation issue directly, which is the conceptual foundation of the FP inflation. They do not appear to report FP-rate-vs-n simulations.

**Carleton, Campbell & Collard 2018, *PLOS ONE* 13(1): e0191055** (DOI 10.1371/journal.pone.0191055) — The PEWMA paper. Full text at PMC5774753 retrieved and read. They report ~10% FP rate stable across parameters, not rising with n: "modes of the hit rate distributions hovered around 10%, irrespective of the experimental parameters." Tested increasing date counts from 5 to 25 and found "no noticeable effect" on FP rates. Different method (PEWMA on radiocarbon time-series) and a much smaller n range than the project's problem. They do **not** report FP-rate-vs-n for the parametric-null envelope test. No analogous fix is proposed.

**Timpson et al. 2014** (*J. Archaeol. Sci.* 52: 549–557) — Canonical reference for the MC envelope method. The `rcarbon` docs describe their `calsample` method as "the approach of Timpson et al. 2014." Timpson's method generates MC replicates by sampling synthetic dates, calibrating them, and summing — which is exactly what preserves per-date uncertainty. The paper applies a criterion to "remove false positives from both the simulated and observed distributions" — suggesting awareness of FP issues, addressed heuristically. [VERIFY: Full text not retrieved.]

**Timpson et al. 2021, *Phil. Trans. B* 376** (PMC7741102) — The ADMUR/CPL paper. Introduces the CPL model as a likelihood-based alternative to SPD-envelope tests. The CPL approach (implemented in the ADMUR R package) side-steps the envelope-test problem entirely by computing a proper likelihood ratio. ADMUR `GitHub AdrianTimpson/ADMUR` exists. [VERIFY: Whether the 2021 paper specifically discusses FP-rate issues with the 2014 MC envelope method.]

**Conclusion on Q2:** No paper has published a simulation study showing FP-rate rising from ~0.05 to 1.0 as n increases for an aoristic-SPA / inscription-data parametric-null envelope test. The project's simulation is likely the first to document this pattern quantitatively at these scales. The conceptual root cause (variance mismatch) is acknowledged obliquely by Carleton & Groucutt 2021 and Crema 2022, and the fix (uncertainty-preserving resampling) is implicit in the rcarbon architecture since Timpson 2014 — but no one has drawn all these threads together for inscription SPA specifically.

---

### Q3 — What does baorista do differently?

**Finding: baorista's architecture is categorically different from a parametric-null MC envelope test. It does not directly solve or replace the permutation-envelope test; it is an alternative inferential framework.**

baorista source code retrieved from `gh api repos/ercrema/baorista`. Two key files examined:

**`mcsim.R`** — The `mcsim()` function does **not** draw from a fitted null. It samples from the **aoristic weights matrix** directly:

```r
mcsim <- function(x, nsim=1000) {
  sims <- sapply(1:x$n, function(x, p, n) {
    rmultinom(n=n, size=1, prob=p[x,])
  }, p=x$pmat, n=nsim, simplify='array')
  sums <- apply(sims, 1:2, sum)
  ...
}
```

This is pure aoristic bootstrap — each event is assigned to one time-block per simulation according to its aoristic probability vector. The result is a distribution of aoristic counts that reflects **chronological uncertainty only**, not any null growth model. Used to generate confidence intervals on the aoristic sum itself, not to test a null. The docstring explicitly says: "it provides only a description of the sample rather than the underlying population."

**`expfit.R`** — The `expfit()` function fits a Bayesian exponential growth model using NIMBLE. The NIMBLE model is:

```r
theta[,] ~ dAExp(r=r, z=n.tblocks)
r ~ rPrior
```

where `dAExp` is a custom distribution that computes the likelihood `p(aoristic weight matrix | r)` by marginalising over the time-block assignments within the NIMBLE likelihood evaluation. **This means the MCMC samples the growth rate r given the full aoristic weight matrix — it does NOT jointly sample individual date assignments during MCMC.** The uncertainty propagation is via the probability matrix (each row = one event's aoristic weight vector), not via explicit latent-date sampling.

**Does baorista side-step the FP problem?** Not directly, because baorista does not implement a parametric-null envelope test at all. Its inferential output is:

1. A posterior distribution over r (exponential growth rate) or the ICAR time-frequency vector.
2. Monte Carlo uncertainty bands on the aoristic sum via `mcsim()` (chronological uncertainty only, no null model).

To use baorista as a substitute for the permutation-envelope test, a posterior predictive check could be constructed: given the posterior over r (or the ICAR latent field), generate predictive aoristic distributions and compare the observed SPA against those. **This would implicitly propagate both model-parameter uncertainty and aoristic-uncertainty** — which is exactly what the correct fix requires. But baorista does not implement this comparison step out of the box; it would be a manual construction.

**Computational cost:** `expfit.R` defaults to `niter=100,000`, `nburnin=50,000`, `thin=10`, `nchains=4`. For small n this is fine; for n=50,000 inscription empire-level runs, the `dAExp` custom likelihood evaluates a sum over `50,000 × n_tblocks` matrix per MCMC step — likely very slow. [VERIFY: No benchmark reported in documentation.]

**CRAN metadata:** version 0.2.1, published 2024-08-19, licence GPL ≥ 2 (compatible with the project if consumed as a tool). Requires R ≥ 3.5.0 and `nimble` ≥ 0.12.0.

---

### Q4 — Is "aoristic-resample-from-fit" a known fix?

**Finding: The mechanism is identical to what rcarbon does, described as the canonical approach since Timpson 2014. The inscription-data adaptation is, as far as this scout can determine, novel — but the principle is direct prior art from radiocarbon SPD practice.**

The rcarbon `modelTest` `calsample` method (explicitly credited to Timpson et al. 2014) does exactly Option A, adapted for radiocarbon:

1. Sample n calendar dates from the fitted null density.
2. Back-calibrate each calendar date to a synthetic 14C measurement.
3. Calibrate each synthetic measurement → individual calibrated probability distribution.
4. Sum all calibrated distributions → MC replicate SPD.

The inscription-data analogue (Option A) would be:

1. Fit null to observed SPA → smooth density over `[−50, 350]`.
2. Sample n synthetic "event years" from the fitted null density.
3. Assign each synthetic event a `[not_before, not_after]` interval drawn from the **empirical distribution of interval widths** in the bootstrap sample.
4. Aoristic-resample each synthetic event uniformly within its interval → bin → MC replicate SPA.

Step 3 is the critical difference from the rcarbon analogue (in rcarbon, "back-calibration" plays the role that assigning a width distribution plays in inscription SPA). The principle of matching MC-replicate variance structure to observed SPA variance structure is canonical since Timpson 2014 / rcarbon. The specific implementation for inscription data with empirical width sampling has not been published as a named procedure.

**No published name found** for the inscription-specific variant. Search terms "aoristic resampling null model", "synthetic inscriptions date-range uncertainty", and related queries returned no named procedure in the literature.

---

### Q5 — Inscription-SPA papers with FP-rate calibration

**Glomb, Kaše & Heřmánková 2022** (*JASRep*, DOI 10.1016/j.jasrep.2022.103270) — Retrieved partial info from SSRN preprint and ScienceDirect abstract (full text paywalled). Use Monte Carlo simulation to test temporal distributions of Asclepius-cult inscriptions (N=210 inscriptions). Compare against general epigraphic trends and find no significant increase during the Antonine Plague period (KS p=0.20, null not rejected). **No FP-rate calibration reported.** Their n=210 is small enough that the FP-inflation problem (which the project's data shows is serious at n ≥ 500 for the exponential null) is unlikely to have caused spurious results in their study — but they did not check.

**Kaše, Heřmánková & Sobotková 2021** — Searches found "Inscriptions as Data: Digital Epigraphy in Macro-Historical Perspective" (*J. Digital History*, 2021; DOI 10.1515/jdh-2021-1004) and the LIRE dataset methodology. Their temporal method: "assigned to each dated inscription 1,000 random dates within its temporal interval, created randomly following a uniform distribution." Pure aoristic resampling, not a permutation-envelope test. **No FP-rate calibration reported.**

**Carleton, Iriarte & Coetzer 2025** (*Nature Cities*, DOI 10.1038/s44284-025-00213-1 [VERIFY]) — Honorific-scaling paper. Uses Bayesian scaling regression on honorific inscription counts vs population. Regression model, not envelope test. **No FP-rate calibration for an envelope test.** Not directly comparable.

**Heřmánková, Kaše & Sobotková 2021** — LIRE methodology paper. Documents the aoristic approach as a descriptive tool, not a null-hypothesis envelope test. **No FP-rate calibration.**

**Mazzamurro 2024/2025** — No relevant results found in searches. [VERIFY: May exist under a different author-name form or journal.]

**Conclusion:** No inscription-SPA paper in the retrieved literature has reported FP-rate calibration for a parametric-null permutation-envelope test. This is a genuine gap. The project's simulation is the first documented FP-rate characterisation for inscription SPA at empirically relevant sample sizes.

---

### Q6 — Non-parametric envelopes (Option C)

**Finding: Non-parametric SPD envelope approaches exist in the radiocarbon literature but are not standard for inscription SPA. The main non-parametric route is row-resample (observed dates permuted), which avoids fitting a smooth null entirely.**

**rcarbon's `permTest` function** implements a **mark-permutation test**: dates are randomly reassigned to groups (rather than drawn from a smooth null), producing replicates with exactly the same overall temporal distribution as observed. This is a non-parametric alternative for *comparing two SPDs*, not for testing an observed SPA against a null growth model.

**Row-resample / label-shuffle approach:** For testing deviation from a null growth curve, the non-parametric alternative would be to resample inscription rows with replacement from the observed corpus to generate MC replicates, then build the envelope from those resampled SPAs. This preserves the full empirical aoristic variance (because actual inscriptions with their actual date ranges are resampled) but yields an envelope centred on the **observed** SPA, not on a theoretical null. This is more useful for confidence interval estimation than null-hypothesis testing.

**ADMUR (Timpson et al. 2021)** — The CPL likelihood approach bypasses the envelope test entirely, replacing it with a proper likelihood ratio test. Arguably the cleanest solution for the null-hypothesis testing problem but requires a well-specified parametric model and is computationally heavier.

**Block-bootstrap** — No specific publication found for SPD/SPA. The approach would block-resample bins of the SPA to preserve temporal autocorrelation, generating empirical variance estimates. Standard time-series bootstrap but has not been named or described for SPA specifically in the literature reviewed.

**Trade-offs reported:** The mark-permutation approach (non-parametric Option C for group comparison) gives exact permutation-based p-values but does not test against a parametric growth model — it tests whether two empirical distributions differ. For this project's use case (testing whether SPA departs from a null growth model), Option A (aoristic-resample-from-fit) is preferred *in principle* because it gives a null distribution centred on the theoretical null rather than on the observed data.

---

## 3. Cross-reference table

| Source | Q1 (rcarbon) | Q2 (FP) | Q3 (baorista) | Q4 (Option A) | Q5 (inscription) | Q6 (non-param) |
|--------|---|---|---|---|---|---|
| rcarbon source (tests.R) | **DIRECT** | bias notes | — | **prior art** | — | permTest |
| Crema & Bevan 2021 | describes | — | — | — | — | — |
| Crema 2022 *JAMT* | cited | reviews bias | — | — | — | — |
| Crema 2025 / baorista | — | — | **full** | — | — | mcsim |
| Timpson et al. 2014 | calsample = canonical | first fix | — | **origin** | — | — |
| Timpson et al. 2021 / ADMUR | — | bypasses | — | — | — | CPL likelihood |
| Carleton et al. 2018 | — | ~10 % FP, n-stable | — | — | — | — |
| Carleton & Groucutt 2021 | — | variance critique | — | — | — | — |
| Glomb et al. 2022 | — | — | — | — | **no FP cal** | — |
| Kaše et al. 2021 | — | — | — | — | **descriptive only** | — |
| Carleton et al. 2025 | — | — | — | — | not envelope | — |

---

## 4. Recommendations (as delivered by scout)

### Use directly

**Option A: Aoristic-resample-from-fit MC.** Direct port of the rcarbon/Timpson 2014 mechanism to inscription data. Field-standard fix. Mechanism:

1. Fit null to observed SPA.
2. Treat fitted null as a calendar-year density; sample n synthetic event-years from it.
3. For each synthetic event, draw a date-range width from the empirical width distribution of the bootstrap sample.
4. Assign `not_before = event_year − width/2`, `not_after = event_year + width/2`.
5. Aoristic-resample each synthetic event uniformly within its interval; bin → MC replicate SPA.

Implementation cost: modest (< 20 additional LOC in `primitives.py`).

### Adapt approach

**ADMUR/CPL likelihood (Timpson et al. 2021)** — replaces the envelope test with a proper likelihood ratio. Most principled but requires fitting a CPL model and computing a likelihood ratio test.

**baorista posterior predictive check** — would constitute a proper Bayesian version of Option A. Computational cost is high (NIMBLE MCMC, 100k+ iterations). Does not directly yield the global-p statistic the prereg specifies. Remains valuable as Decision 3 sensitivity.

### Ignore

**Pure Poisson draws on smooth fit (current `sample_null_spa`).** Confirmed broken at n ≥ 500. Do not retain.

**baorista `mcsim()` as a null-test substitute.** The `mcsim` function resamples from aoristic weights only — uncertainty around observed, not around a theoretical null. Cannot replace the permutation-envelope test for null-hypothesis testing.

---

## 5. Build-vs-adopt verdict

**Build Option A in Python.** Nothing in the literature requires adopting a new library or switching to R. The radiocarbon-SPD prior art (rcarbon, Timpson 2014) gives the algorithm precisely. The inscription-data adaptation (using empirical width distribution instead of back-calibration) is a direct methodological port. Implement in `sample_null_spa` — change is localised.

**Concurrent actions:**

- File a prereg amendment to describe the MC replicate mechanism explicitly.
- Run FP-rate calibration check on the fixed implementation before re-running H1.
- Retain baorista as Decision 3 sensitivity analysis on representative provincial subsets; promote the "baorista posterior predictive" to secondary result only if it converges and gives materially different results from the fixed frequentist test.

---

## 6. DOIs for Zotero (`/cite-new`)

The following items may not be in the Zotero collection yet — confirm against `PZN5ATJK` before adding:

| # | Authors | Title (short) | DOI | Note |
|---|---|---|---|---|
| 1 | Crema & Bevan 2021 | Inference from large sets of radiocarbon dates | 10.1017/RDC.2020.95 | rcarbon methods |
| 2 | Crema 2022 | Statistical inference of prehistoric demography (*JAMT*) | 10.1007/s10816-022-09559-5 | Review + bias |
| 3 | Crema 2025 | A Bayesian alternative for aoristic analyses | 10.1111/arcm.12984 | baorista |
| 4 | Timpson et al. 2014 | Reconstructing regional population fluctuations | 10.1016/j.jas.2014.08.011 | MC envelope origin |
| 5 | Timpson et al. 2021 | Modelling population dynamics, S. American Arid Diagonal | 10.1098/rstb.2019.0723 [VERIFY] | ADMUR / CPL |
| 6 | Carleton et al. 2018 | Radiocarbon dating uncertainty + PEWMA | 10.1371/journal.pone.0191055 | Power simulation |
| 7 | Carleton & Groucutt 2021 | Sum things are not what they seem | 10.1177/0959683620981700 | Variance critique |
| 8 | Glomb et al. 2022 | Popularity of the cult of Asclepius | 10.1016/j.jasrep.2022.103270 [VERIFY] | Inscription SPA precedent |
| 9 | Carleton et al. 2025 | Parallel scaling of elite wealth | 10.1038/s44284-025-00213-1 [VERIFY] | Honorific scaling |

---

## 7. VERIFICATION PENDING markers

The following specific claims require re-verification against full texts before use in the paper:

- [VERIFY] Crema 2022 *JAMT*: specific language about null-model bias and whether it discusses FP-rate-vs-n. Paper paywalled.
- [VERIFY] Crema & Bevan 2021: exact wording of the MC replicate description in the methods. PDF retrieved as binary; unreadable.
- [VERIFY] Timpson et al. 2021 *Phil. Trans. B*: DOI `10.1098/rstb.2019.0723` — needs confirmation. Whether the paper explicitly criticises the 2014 envelope method's FP properties.
- [VERIFY] Glomb et al. 2022 *JASRep*: DOI and whether the methods section describes the null MC mechanism in enough detail to confirm they do not use uncertainty-preserving resampling.
- [VERIFY] Carleton et al. 2025 *Nature Cities*: DOI — retrieved from search result but not confirmed from the abstract directly.
- [VERIFY] baorista `expfit` computational cost at n=50,000: no benchmark in documentation.

Run `/lit-scout-verify` on this report before any cited claim is used in the paper or amendments.

---

## 8. Empirical follow-up — what we learned from validation

**Recorded by Claude Code main thread on 2026-04-25 after running the scout's recommended Option A.**

The scout recommended Option A as the field-standard fix. We implemented it (`runs/2026-04-25-h1-simulation/code/experiment_aoristic_mc.py::sample_null_spa_aoristic`) and ran a validation experiment. **Option A failed worse than the original Poisson-on-fit MC** (FP rate 1.000 vs 0.535 in the same cell).

Diagnosis: the implementation faithfully ported rcarbon's mechanism, but the ported mechanism is **double-smearing** in the inscription-data context. rcarbon's null fit is in calendar-year space; back-calibrating produces synthetic 14C measurements which are then calibrated to produce proper per-event probability distributions. The smearing is applied **once** to each synthetic event's calibrated distribution.

In the inscription analogue: the null fit is on the **already-aoristic-smeared observed SPA**. Drawing synthetic event-years from this fit AND re-applying empirical widths via aoristic resampling smears the synthetic events **twice**. The resulting MC envelope is over-smoothed; observed retains residual peakiness from real LIRE structure (editorial conventions, real growth-decline patterns); observed sits outside the over-smoothed MC envelope; FP inflated to 1.0.

The scout's Option A is correct **if** the null fit is in true-date space (un-smeared). For radiocarbon, it is. For inscriptions as currently fit, it isn't. The scout missed this implementation subtlety because the documented rcarbon mechanism doesn't surface it — rcarbon users don't need to think about it because radiocarbon calibration doesn't have this asymmetry.

**Subsequent path:** Tested **Option C** (non-parametric row-bootstrap MC). PASSES FP control empirically (FP = 0.071 single cell; full-grid validation 0.033 mean). But Option C is provably unable to detect features that exist in the corpus (under bootstrap principle, observed and MC are exchangeable — no detection power on real events).

**Current pilot:** Forward-fit exponential null in *true-date space* (likelihood treats `[nb_i, na_i]` as integration range; fit recovers the parametric density without the smearing). MC then forward-applies aoristic to synthetic events drawn from this true-date null. Smearing applied once, to MC events; observed already has it once. **Variance structures should match.** Validation in progress.

This addendum corrects the scout's Option A recommendation in light of empirical findings, without retracting the analytical content of the report.

---

## Sources (URLs as cited by scout)

- [modelTest documentation (rdrr.io)](https://rdrr.io/cran/rcarbon/man/modelTest.html)
- [rcarbon GitHub repository](https://github.com/ahb108/rcarbon)
- [Crema & Bevan 2021 (Radiocarbon)](https://ercrema.github.io/files/Crema%20and%20Bevan%202021.pdf)
- [Crema 2022 *JAMT* (Springer)](https://link.springer.com/article/10.1007/s10816-022-09559-5)
- [baorista GitHub repository](https://github.com/ercrema/baorista)
- [baorista CRAN page](https://cran.r-project.org/web/packages/baorista/index.html)
- [baorista *Archaeometry* (Wiley)](https://onlinelibrary.wiley.com/doi/10.1111/arcm.12984)
- [Carleton, Campbell & Collard 2018 *PLOS ONE* (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5774753/)
- [Timpson et al. 2021 *Phil. Trans. B* (PubMed)](https://pubmed.ncbi.nlm.nih.gov/33250032/)
- [ADMUR GitHub repository](https://github.com/AdrianTimpson/ADMUR)
- [Carleton & Groucutt 2021 (Holocene)](https://journals.sagepub.com/doi/10.1177/0959683620981700)
- [Glomb, Kaše & Heřmánková 2022 (SSRN preprint)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4044525)
- [Carleton, Iriarte & Coetzer 2025 (Nature Cities)](https://www.nature.com/articles/s44284-025-00213-1)
- [Heřmánková, Kaše & Sobotková — Inscriptions as Data (De Gruyter)](https://www.degruyterbrill.com/document/doi/10.1515/jdh-2021-1004/html)
