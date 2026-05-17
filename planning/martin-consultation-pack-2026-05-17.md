---
title: "Statistician consultation pack — Latin-inscriptions preregistration"
date: 2026-05-17
audience: "Martin (applied econometrician; the project's invited external statistician reviewer)"
prepared-by: "Shawn Ross (PI) with Claude Code (Anthropic, Opus 4.7)"
status: "draft for Martin; pre-OSF lodgement"
target-document: "planning/preregistration-draft.md (~451 lines, dated 2026-05-17)"
estimated-reading-time: "Executive summary + question list: ~25 min. Each appendix: 10–20 min, consult as needed."
---

# Consultation pack — preregistered Latin-inscription analysis

## How to read this pack

Three layers, in order of decreasing concision:

1. **Executive summary** (this section + the next) — what the project is, what's stable, where I want your eyes.
2. **Consultation questions** — seven questions, each with the immediate background, the current decision, and an explicit ask. Primary four (most consequential); secondary three (still warranting your review).
3. **Appendices** — deep dives, one per question, plus an orientation appendix (corpus, terminology) and a supporting-material appendix (effect-size table, uncertainty-quantification table, known limitations).

The preregistration itself is `planning/preregistration-draft.md` in the project repository (~451 lines); the decision log is `planning/decision-log.md`. Anything in this pack is a précis of those documents; where the précis and the source documents disagree, the source documents govern.

How you engage is up to you: marginal notes on a printout, an email reply keyed by question number, a call, a written memo — whichever fits your time. Even partial input on one or two of the primary questions is genuinely useful; this pack errs on the side of completeness because OSF lodgement is the next step after your input is incorporated, so getting it wrong has more consequence than getting it long.

---

## Executive summary

**The project.** A preregistered three-phase analysis of Latin inscriptions from the Roman Empire (50 BC – AD 350), using the LIRE v3.0 corpus (~ 181 k inscriptions, ~ 815 cities with matched Hanson 2016 population estimates). Two methodological objects: (a) a **Bayesian deconvolution-mixture model** that separates a corpus-level temporal SPA ("summed probability analysis" — a kernel-density-style empirical curve over time) into an editorial-encoding-artefact component and a genuine ancient-pattern component; (b) a **Bayesian within-between (Mundlak) negative-binomial regression** of city-level inscription counts on log-population, identifying a clean within-province population effect. The headline confirmatory result is the within-province population-attributable variance fraction `f_within`; secondary confirmatory tests replicate Hanson (2021)'s residual findings (provincial capitals over-produce; residuals are spatially clustered).

**What's stable.** Phase 1 (a Monte Carlo power simulation establishing minimum sample sizes for permutation-envelope deviation-detection at three subset levels) is complete, with false-positive control verified across 96 zero-effect calibration cells. The corpus filtering, the within-between NBR specification, the decision-rule structure (three-way verdicts), the directional H3a rule (`f_within` against a 0.10 threshold), the corpus choice (LIRE v3.0 frozen for this lodgement), and the artefact diagnosis (a 2026-05-17 triplet of diagnostics established that the dominant editorial artefact is wide-template-slab encoding, *not* anchor-year inflation, and that narrow regnal spikes at AD 77.5 / 122.5 / 212.5 are real ancient clustering — not artefact) are all settled.

**What's open — where I'd like your input.** Seven question-clusters, listed below at one-line resolution, with detail in the question section and full technical context in the appendices:

| # | Question (one-line)                                                                                                                                                                                                | Decision ref | Priority |
|---|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|----------|
| 1 | Is multinomial-on-binned-aoristic-mass the right primary observation model for the mixture, with Dirichlet-multinomial and rescaled NegBin as supplementary fits? Is aoristic uncertainty being absorbed correctly? | D19          | Primary  |
| 2 | Is the recovery-simulation grid + the per-cell-coverage validation rule (≥ 90 % of cells, each cell passing iff ≥ 90 % of ≥ 50 replicates produce 95 % CIs containing the true α, plus Pearson r ≥ 0.95 on shape) defensible?                                                  | D21          | Primary  |
| 3 | For H3c: are Pearson residuals on the Mundlak NBR right, is the asymmetric draw-wise (capitals contrast) / posterior-mean-with-frequentist-permutation (Moran's I) treatment defensible, and should we worry about ignoring posterior uncertainty in the spatial test? | D23          | Primary  |
| 4 | Are the numerical-PPC trigger categories (and what they imply about model revision) the right set for an NBR with random intercepts? Anything missing — autocorrelation-in-residuals, posterior-predictive spatial diagnostics, etc.? | D25          | Primary  |
| 5 | Within-between (Mundlak) NBR with `f_within` defined as `Var(β_within · within-deviation) / Var(log E[count])` on the latent scale — is that the right estimand, and is the latent-scale choice defensible vs response-scale? Is the 0.10 substantive threshold sensible *a priori*? | D12          | Secondary |
| 6 | "Habit-removed residual trajectory" analysis (decompose city SPA into an empire-wide habit + city residual; validate residual against foundation dates and bounded independent anchors) — sensible exploratory design, or fundamentally confounded? | D13          | Secondary |
| 7 | Confirmatory claim hierarchy: H2.1, H3a, H3c(i), H3c(ii) judged independently — no omnibus family, no Holm correction. Defensible, or do we need a multiplicity adjustment somewhere? | Field 3      | Secondary |
| 8 | Pre-Phase-2 design artefacts (`runs/2026-05-XX-recovery-grid-design/` and `runs/2026-05-XX-template-dictionary/`) are not yet built — recovery-grid values, numerical PPC thresholds, and the template-dictionary scan all crystallise into those artefacts before any Phase 2 analysis runs. Would you like to review the artefacts before they're committed, suggest specific pinned values now, or propose additional content categories? | D19 / D20 / D21 / D25 | Secondary |

**Format note for primary questions 1, 2, 3, and 4.** These four decisions are flagged in the decision log as *primary statistician questions*; the corresponding decision-log entries (Decisions 19, 21, 23, 25 in `planning/decision-log.md`) record the explicit motivation for flagging each. The appendices reproduce the substance but the decision log is the canonical record.

**Background on this project's review process.** This preregistration has been through three rounds of cross-model adversarial review (round 1: dual fresh-context Claude Opus 4.7 reviewers; round 2: ChatGPT 5.5; round 3: cross-model ChatGPT 5.5 + Gemini 3 Pro) plus a structured fresh-context QA pass; both round-3 verdicts converge on "ready for the statistician." So the gaps you're being asked to inspect are gaps that survived four cycles of model-graded review, not first-draft issues. The questions below are deliberately the ones where LLM review cannot substitute for a statistician's judgement.

---

## Background — read once

*Skip if you already have context from the broader engagement.*

**The corpus.** LIRE v3.0 (Kaše, Heřmánková & Sobotková 2023; Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 inscriptions; 63 attributes. We apply a geographic filter (province assigned), a temporal filter (date interval overlaps 50 BC – AD 350), and exclude Rome from regression analyses (an extreme outlier — 65 k inscriptions alone, ~ 36 % of the filtered corpus). The Rome-excluded analytical corpus is **115,174 inscriptions** across **~ 815 cities** with matched Hanson 2016 population estimates.

**The dating problem and the SPA.** Most inscriptions carry only an interval `[not_before, not_after]` rather than an exact date. The "summed probability analysis" (SPA) — borrowed from radiocarbon archaeology and palaeodemography — spreads each inscription's unit mass uniformly across its date range, then sums across all inscriptions to get a curve `m_t` representing the empirical density of inscription production over time at 5-year resolution. This is the basic input to all temporal analyses.

**The editorial-artefact problem.** Latin epigraphic editors faced with a vaguely-datable inscription round to template intervals — Roman centuries `[1, 100]`, half-centuries `[125, 175]`, reign intervals `[117, 138]` (Hadrianic), and so on. Endpoint statistics: **54.5 % of `not_before` end in `01`; 53.0 % of `not_after` end in `00`** — the signature of century-template rounding. Under uniform-aoristic this template encoding deposits flat plateaus of mass over century blocks rather than excesses on midpoint years. (The earlier draft of this prereg framed the artefact as "midpoint spikes" — that framing was falsified by three diagnostic runs on 2026-05-17; the present draft replaces it.) The dominant artefact is the wide-template slab structure, with the BC / AD calendar-boundary step (+1,159 between the AD 1 and 1 BC bins of the empirical SPA — the largest single discontinuity in the envelope) as a secondary feature.

**The three phases.**

| Phase | Status | Object | Method |
|-------|--------|--------|--------|
| 1 | complete | Minimum-sample-size thresholds for permutation-envelope deviation-detection | Monte Carlo simulation (256 cells × 1000 iterations × 1000 MC; FP control verified at all 96 zero-effect cells) |
| 2 | designed, not yet executed | Bayesian deconvolution-mixture model + recovery-simulation validation | Bayesian mixture in pymc; recovery simulation over a pre-Phase-2 design-artefact-pinned grid |
| 3 | designed, not yet executed | Within-between NBR (H3a, confirmatory); Pearson residual analysis (H3c, confirmatory); permutation-envelope deviation-detection (H3b, exploratory) | Bayesian NBR in pymc + brms shadow validation; conditional-permutation Moran's I; permutation-envelope on mixture-corrected SPAs |

**Phase 1 thresholds (relevant for sample-size reasoning later).** The Phase 1 simulation establishes that — for the most-detectable bracket ("50 % effect sustained over ≥ 50 years," Gaussian shape) — *empire*-level deviation-detection requires N ≈ 50 k, *province*-level requires N ≈ 1.4–1.9 k, and *urban-area*-level requires N ≈ 1.4–1.9 k inscriptions, with the harder brackets (doubling-over-25-years; 20 %-over-25-years) reachable only at empire / province level for the easiest combination. These are deviation-detection thresholds for the permutation-envelope, not for the H3a cross-sectional regression — the latter uses all ~ 815 Hanson-matched cities.

**Terminology cheat-sheet.**

- *SPA* = summed probability analysis (empirical density of inscription production over time).
- *Aoristic* = the method of spreading each interval-dated inscription's mass uniformly over its `[not_before, not_after]` range; from criminology / archaeology.
- *Within-between specification* (Mundlak 1978; Bell & Jones 2015) = split a level-1 predictor into the level-2 group mean and the within-group deviation, with separate coefficients.
- *Permutation envelope* (rcarbon::modelTest, Crema & Bevan 2021; Timpson et al. 2014) = a pointwise + global Monte Carlo significance test for an SPA against a parametric null.
- *Forward-fit* = the null parametric model is fitted to the date *intervals*, not to the already-smeared aoristic SPA, then sampled forward through the aoristic procedure to generate Monte Carlo replicates. Avoids double-counting the date-range uncertainty.

---

## Primary consultation questions

Four primary questions, in approximate order of methodological consequence. Each has: (a) one-paragraph immediate background; (b) the specific decision the prereg currently commits to; (c) the explicit ask.

### Q1 — Mixture observation model: multinomial primary, Dirichlet-multinomial + rescaled NegBin supplementary

**Background.** The Bayesian deconvolution-mixture model decomposes the observed empirical SPA `m_t` (a 5-year-binned aoristic density) into a *convention* component (uniform mass over template intervals — centuries, half-centuries, reigns) and a *genuine* component (smooth ancient-history density), with mixing weight `α ∈ [0, 1]`. Both components are normalised to compositional shapes (`Σ_t p_t = 1`); the observed SPA is converted to integer bin counts `y_t` by largest-remainder rounding to total N. The primary observation model is **multinomial**: `y ~ Multinomial(N, p_t)` with `p_t = α · p_conv,t + (1 − α) · p_gen,t`. Two supplementary fits are reported alongside (for model-checking, not as confirmatory comparators): **Dirichlet-multinomial** (adds a concentration κ for bin-level overdispersion) and **rescaled NegBin** (`y_t ~ NegBin(N · p_t, φ)` — the rescaling avoids the absolute-scale degeneracy that would arise without it).

Aoristic uncertainty enters *upstream* in the SPA construction (one aoristic-mass SPA per fit), not via per-inscription latent-date sampling propagated into the likelihood. We considered propagating aoristic uncertainty into the likelihood but did not commit to it for the primary or supplementary analyses.

**Decision (Decision 19).** Multinomial primary; Dirichlet-multinomial and rescaled NegBin as supplementary (the latter reported descriptively, not as a confirmatory comparator). Components normalised to sum to 1. Aoristic uncertainty handled upstream.

**Ask.**

- **(a)** Is the multinomial the right primary likelihood for this problem class, or would you reach for something else (e.g. a hierarchical / nested multinomial, a Poisson with offset, or a fully compositional Dirichlet-process mixture)?
- **(b)** Is the largest-remainder integer-rounding step a clean way to bridge the continuous aoristic density to the discrete count likelihood, or does it introduce its own bias? The aoristic SPA is a sum of fractional contributions; we round once, deterministically, to keep N fixed. Alternative: skip rounding and use a Dirichlet observation model directly on `q_t = m_t / Σ m_t`.
- **(c)** Is the decision to treat aoristic uncertainty as upstream (one SPA → one fit) defensible at corpus level, or do you anticipate that the posterior on α would shift materially under per-inscription-latent-date propagation? If material, is it worth doing for the primary or only as a sensitivity?
- **(d)** Identifiability: with both components compositional (each summing to 1) and α weighting their convex combination, are there pathologies you'd flag — e.g. cases where `p_conv,t` and `p_gen,t` are too similar in shape to admit a unique decomposition?

**Where to go for more detail.** Appendix B.1 (mixture model deep dive: full likelihood spec, priors, identifiability mechanics, the slab structure of the convention component).

---

### Q2 — H2.1 recovery-simulation grid and the per-cell-coverage validation rule

**Background.** The mixture model is validated by a recovery simulation: build synthetic observed SPAs from a *known* genuine SPA + a *known* α + a *known* convention component built from the slab structure of D20, run the mixture, and check it recovers the truth. The grid axes are pre-committed in the prereg (α grid of ≥ 5 values spanning the empirical pilot range; genuine-shape library of ≥ 6 shapes including smooth growth / decline / rise-and-fall / multi-modal / regnal-cluster / flat-baseline; tier-weight vectors of ≥ 5 covering pilot-drawn and corner cases; representative N values from Phase 1's reachability map; ≥ 50 replicates per cell; cell-deterministic seeds). Specific numerical values are pinned in a pre-Phase-2 design artefact (`runs/2026-05-XX-recovery-grid-design/`) committed before any recovery simulation runs.

The **validation rule** has two parts: (i) ≥ 90 % of cells achieve **per-cell coverage**, where a cell passes iff ≥ 90 % of its replicates produce a posterior 95 % CI on α containing the true α (a proper repeated-sampling coverage statement, not a one-shot per-cell check); (ii) posterior-median Pearson r between recovered and true genuine SPA ≥ 0.95 in ≥ 90 % of cells. Cell-wise results are reported in addition to global pass-rate.

**Decision (Decision 21).** Procedural pre-commitment to grid axes + per-cell-coverage rule, specific values pinned in the design artefact. The 90 % / 90 % thresholds, the ≥ 50 replicates minimum, the ≥ 0.95 shape-recovery threshold, and the shape-library completeness are all flagged as Martin-consultation items in the decision-log entry.

**Ask.**

- **(a)** Is ≥ 90 % of cells, with cell-passes requiring ≥ 90 % of replicates' 95 % CIs containing the truth, the right structure for the coverage rule? An alternative would be a single global coverage rate (pool replicates across cells) — but that hides cell-level structural failure modes (e.g. coverage collapsing only in high-α / convention-adjacent cells). Cell-wise reporting is binding either way.
- **(b)** ≥ 50 replicates per cell — defensible, or do you want more (e.g. ≥ 200 for tighter Wilson intervals on per-cell coverage)? Cost is roughly linear in replicates × cells; expect O(50–100) cells.
- **(c)** Is **Pearson r ≥ 0.95** the right shape-recovery metric? Alternatives: KS distance between posterior-median and true shape; integrated absolute error; Wasserstein-1. Pearson r is intuitive and cheap; we use it for compatibility with the Phase 1 simulation; we suspect it under-penalises localised mass-redistribution failures.
- **(d)** Shape library completeness — is six (growth, decline, rise-and-fall, multi-modal, regnal-cluster, flat-baseline) enough, and are there shapes you'd add as torture tests (e.g. a regime-switching shape that breaks the smoothness prior)?
- **(e)** Should the supplementary fits (Dirichlet-multinomial; rescaled NegBin) also be validated by the same recovery simulation, with separate cell-wise pass tables, or only the multinomial primary?

**Where to go for more detail.** Appendix B.2 (recovery grid deep dive: the design artefact's scope, the convention-component slab structure that's mirrored in the synthetic SPAs, why the 90 % / 90 % thresholds, the relationship to the Phase 1 simulation).

---

### Q3 — H3c residuals: Pearson choice, draw-wise / posterior-mean asymmetric treatment

**Background.** H3c replicates two findings of Hanson (2021): (i) provincial capitals over-produce inscriptions relative to non-capital city-statuses (a *capitals contrast*); (ii) residuals are spatially clustered (Moran's I positive). Both run on residuals from the H3a within-between NBR. The current spec is **Pearson residuals**:

```
For posterior draw s and city c:
  r_c,s = (y_c − μ_c,s) / sqrt(μ_c,s + μ_c,s² / φ_s)
```

where `μ_c,s` is the full city-level posterior mean (including the province random intercept `α_province[c]`) and `φ_s` the posterior draw of the overdispersion parameter.

**Asymmetric inferential treatment:**

- **H3c(i) capitals contrast** is **draw-wise**: per posterior draw, compute `contrast_s = mean(r_c,s | capitals) − mean(r_c,s | non-capitals)`; the rule is `P(contrast > 0) ≥ 0.95` (posterior probability over draws).
- **H3c(ii) Moran's I** is computed on **posterior-mean residuals** `r_c = (1/S) Σ_s r_c,s` (one residual per city, averaged across draws), with conditional permutation inference (999 permutations of `r_c` over fixed spatial weights) per `k ∈ {5, 8, 10}`. The rule is Moran's I > 0 at *p* < 0.05 in ≥ 2 of 3 k. **Supplementary (binding):** the posterior distribution of Moran's I across draws (per k) is reported as 2.5 / 50 / 97.5 percentiles of I_s for transparency.

**Rationale for asymmetry.** The capitals contrast naturally lives in posterior space ("does the contrast exceed 0 with high posterior probability?") — draw-wise computation answers this directly. Moran's I, by contrast, has a field-standard frequentist permutation procedure (Anselin's conditional permutation; Cliff & Ord 1981); running it on posterior-mean residuals keeps the inferential gold standard while reporting the posterior distribution of I_s supplementarily. We rejected a fully draw-wise Moran's I (`P(I > 0) ≥ 0.95 in ≥ 2 of 3 k`) because it would substitute a posterior-probability rule for a field-standard permutation rule that has known operating characteristics.

**Decision (Decision 23).** Pearson residuals throughout; draw-wise capitals contrast; posterior-mean residuals for Moran's I with field-standard conditional permutation inference. Posterior distribution of I across draws reported supplementarily.

**Ask.**

- **(a)** Is **Pearson** the right residual for an NBR with random intercepts? Alternatives we considered: deviance residuals (better-behaved at extreme μ, but no closed-form posterior-draw computation), log residuals `log(y_c + 0.5) − log(μ_c)` (Hanson 2021's implicit scale), posterior-predictive residuals (uncertainty already baked in). Are we right to prefer Pearson, and does the "include the random intercept in μ" choice raise any concerns about double-counting?
- **(b)** Is the **asymmetric draw-wise / posterior-mean treatment defensible** to a spatial econometrician, or does the inconsistency look like ad-hocery? The alternatives are: fully draw-wise Moran's I (loses the field-standard); fully posterior-mean (loses the natural draw-wise contrast for capitals); or a single inferential framework throughout (which would require choosing).
- **(c)** Is the **supplementary "posterior distribution of I_s per k"** an adequate way to surface the posterior uncertainty that the confirmatory rule hides? If the supplementary's 2.5–97.5 percentile range crosses zero while the posterior-mean Moran's I is significantly positive, what's the right interpretive language?
- **(d)** **k-NN weight choice.** Primary k = 8 (Anselin convention for point data); sensitivity at k = 5 and k = 10. Decision-rule wording: ≥ 2 of 3 k. Is the k-NN sensitivity set the right operationalisation of "robust spatial structure," or would you prefer a Gaussian-decay or distance-band weight as a complementary check? (The Empire's uneven site density argues against fixed distance-bands.)

**Where to go for more detail.** Appendix B.3 (residual definition deep dive; Hanson 2021's published numbers; the BC / AD-boundary residual concern).

---

### Q4 — Numerical posterior-predictive-check thresholds

**Background.** The prereg requires numerical PPC failure triggers, not narrative ones — the same procedural-prereg-plus-design-artefact pattern as the recovery grid (Decision 25 / 21 share the artefact). Trigger categories (each gets a specific numerical threshold pinned in the artefact before any pilot fit):

| Category | Numerical bound (pinned in design artefact) |
|----------|---------------------------------------------|
| Prior-predictive 99th-percentile per-city count | Cap value (sanity bound on prior tail) |
| Posterior-predictive *mean* | Within X % of observed |
| Posterior-predictive *std* | Within Y % of observed |
| Posterior-predictive 95th-percentile tail count | Within specified bounds of observed |
| Posterior-predictive proportion-of-zeros | Within specified bounds of observed (NBR zero-inflation sanity) |
| Residual-vs-fitted slope (standardised Pearson residuals over μ̂) | Absolute slope < threshold |
| Province-level residual dispersion | Ratio of within-province residual variance to grand residual variance, within bounds |

**Failure response.** Any tripped trigger initiates model revision (priors, link, or structure). The **originally-preregistered model is reported alongside** the revised model in the paper — confirmatory status preserved for the original; the revised model reported as a transparent post-hoc revision. An OSF amendment is filed before final results are lodged.

**Decision (Decision 25).** Numerical, not narrative; specific thresholds pinned in the pre-Phase-2 design artefact (shared with the recovery-grid spec). Listed as a primary item for your consultation because the specific X / Y / tail / slope / dispersion bounds need expert input.

**Ask.**

- **(a)** Is the **category set complete**? Notable possible additions: posterior-predictive *spatial-autocorrelation* check on H3a residuals (predict, then test for spatial structure in `y_pred` to verify Hc isn't a tautology); autocorrelation in standardised residuals if ordered by population or province; posterior-predictive *log-likelihood replicate distribution* (Bayesian-p style global fit check).
- **(b)** What are **defensible numerical thresholds** for an NBR of inscription counts at city level (counts ranging from low single digits to ~ 65 k for Rome — though Rome is excluded)? **These are the values we are most uncertain about and most want your input on.** Our current straw values are X = 5 %, Y = 10 %, tail-percentile bounds = ± 20 % of observed, residual-vs-fitted slope < 0.05, dispersion ratio bounds 0.5–2.0 — **flagged here as provisional placeholders, not commitments**. They are the back-of-envelope numbers we landed on without external statistician input; we expect them to be wrong by factors we cannot estimate. Even rough suggestions ("X should be more like 10–15 %", "the slope threshold is too lax", "drop category 7 and replace with autocorrelation-in-residuals") are exactly the input we are looking for. The design artefact is where the final values will be pinned; your input is the gating piece of that pinning.
- **(c)** Is the **failure response defensible**? "Report original alongside revised, mark revised as post-hoc, file an OSF amendment" — is that the right confirmatory-status preservation rule, or would you prefer a stronger commitment (refuse to revise; report only the original) or a weaker one (treat revision as routine Bayesian workflow without amendment)?
- **(d)** Is there a **PPC-trigger category that should be H3c-specific** — e.g. a check on the *posterior-mean residual surface* before Moran's I is run, to ensure the residuals aren't already smooth enough to bias the spatial test?

**Where to go for more detail.** Appendix B.4 (PPC deep dive: full prior-predictive design; relationship between PPC failure and the H2.1 recovery validation).

---

## Secondary consultation questions

Four secondary questions — still warranting your review, but not flagged as Martin-primary in the decision log. Same structure: background, decision, ask. Q8 is meta (input on the pre-Phase-2 design artefacts) and can be answered briefly at whatever level of engagement suits you.

### Q5 — H3a estimand: within-between (Mundlak) NBR, latent-scale variance fraction, 0.10 substantive threshold

**Background.** The primary RQ asks what fraction of within-province spatial variation in inscription production is accounted for by urban population. H3a operationalises this via a Bayesian within-between (Mundlak / Bell-Jones-style) negative-binomial regression:

```
y_c ~ NegBin(μ_c, φ)
log(μ_c) = α_0 + α_province[c]
          + β_within  · (log_pop_c − log_pop_province_mean[c])
          + β_between · log_pop_province_mean[c]

α_0          ~ Normal(0, 5)
β_within     ~ Normal(0, 1)
β_between    ~ Normal(0, 1)
α_province   ~ Normal(0, σ_prov)
σ_prov       ~ HalfNormal(1)
1/φ          ~ HalfNormal(1)
```

Sample is all ~ 815 Hanson-matched cities (Rome excluded). The **confirmatory estimand** is the within-province population-attributable variance fraction:

```
f_within = Var(β_within · (log_pop_c − log_pop_province_mean[c])) / Var(log E[insc_c])
```

computed **per posterior draw** on the **latent (log) scale**, reported as a posterior distribution. Both Var(…) terms are computed unweighted across cities on the same posterior draw to avoid scale ambiguity.

**Decision rule (three-way; Decision 18):**

- **Supported:** posterior 95 % CI for `f_within` wholly above **0.10**.
- **Evidence against:** wholly below 0.10.
- **Inconclusive:** straddles 0.10.

Supplementary reporting (binding alongside the verdict): the full posterior of `f_within`, plus P(f_within > 0.05), P(f_within > 0.10), P(f_within > 0.20) as a posterior-probability ladder.

**Why the within-between specification.** An earlier draft tried to decompose `Var(log E[insc])` as `Var(β · log_pop) + Var(α_province) + residual` — but `log_pop` and `α_province` are correlated (provinces differ systematically in their city-size distributions), so the cross-covariance term was being silently dropped and the three "proportions" did not sum to one. The Mundlak split makes `(log_pop_c − log_pop_province_mean[c])` orthogonal to province membership by construction, so its variance component is unambiguous; the between-province component is reported but explicitly flagged as not separately identifiable from province-level "everything else."

**Why mixture *not* applied to H3a's `y_c`.** The Bayesian mixture corrects the **temporal** SPA analyses (H2.1, H3b) — it produces a posterior over a temporal shape, not over a per-city corrected count. A per-city mixture fit was rejected because it would be unidentified for ~ 600 of the ~ 815 cities (N < 100). The cross-sectional artefact protection for H3a (and H3c, which inherits via the H3a posterior) is the **50 BC – AD 350 date-window filter**; the mixture's empire-level α posterior is reported as descriptive context but doesn't propagate into H3a's CI. This is a genuine scope limit, flagged as a Known Limitation in the prereg.

**Decision (Decision 12, with the directional refinement of Decision 18 and the date-filtered-count scope of Decision 22).** Mundlak NBR; `f_within` on the latent log scale as the primary estimand; three-way decision rule against 0.10.

**Ask.**

- **(a)** **Estimand scale.** Latent (log) scale vs response scale — is the latent-scale choice defensible, or would response-scale (`Var(E[insc_c]) / Var(insc_c)`) be preferred? Latent-scale gives a cleaner interpretation in terms of the *linear-predictor* variance components; response-scale matches the original count-distribution variance, but mixes overdispersion in non-trivial ways. We chose latent-scale on the argument that the question is about the *systematic* component of count variation, not its mean-variance scaling; we want to know we're not wrong.
- **(b)** **Threshold value.** 0.10 — defensible as a substantive "non-trivial share" bound, or is there a better-grounded choice? Prior-predictive-distribution-of-`f_within` is a candidate diagnostic: if the prior predictive places > 50 % mass above 0.10, the rule is near-vacuous *a priori*. We're committed to running the prior-predictive check before fitting; the threshold is revisable if it turns out to be a priori implausible.
- **(c)** **Mundlak vs alternative specifications.** Bell & Jones 2015 recommend Mundlak / hybrid for within-between separation; you might prefer (i) commonality / hierarchical-partitioning analysis (Nimon & Reio 2011) for variance decomposition; (ii) Lewbel-style heteroskedasticity-based identification; (iii) ICC-only reporting without a fraction estimand. Anything you'd push us toward?
- **(d)** **Sample / structure.** ~ 815 cities clustered in ~ 50 provinces; province-mean log-pop ranges substantially. Is the random-intercept-only structure (no random slopes for `β_within`) the right pull? Random slopes would let `β_within` vary across provinces; we omitted them because the within-province sample sizes are very uneven (some provinces have < 10 cities).

**Where to go for more detail.** Appendix C.1 (H3a deep dive: prior choices and Jacobian for the brms shadow; pymc / brms cross-validation; the within-between literature trail; the Hanson 2021 OLS log-log scaling comparator).

---

### Q6 — Habit-removed residual trajectory analysis (exploratory)

**Background.** The SPA's chief advantage over Hanson's single-maximum-population estimate per city is that it produces a *time series per city*. The naive "is the city's SPA peak near the city's independently-known demographic peak?" comparison is confounded by the *empire-wide epigraphic-habit shape* — the MacMullen / Meyer "rise and fall of the epigraphic habit." A raw peak-to-peak comparison largely measures the habit, not the city.

**Design.** Decompose each city's SPA trajectory into:

- An **empire-wide habit component** (estimated from the corpus-level SPA, possibly via the same mixture machinery that gives the corpus-level `genuine_SPA`).
- A **city-specific residual trajectory** (after habit removal).

Then validate the residual against independent temporal anchors, in priority order:

- **Foundation dates** — corpus-wide; sharp prediction (~ zero residual SPA mass before the foundation year).
- **Independent peak-population dates** — assembled for a bounded case-study set; compared as posterior-CI calibration (does the independent date fall in the posterior peak-time CI?).
- **Multi-point independent trajectories** — for the few well-studied cities; full-shape comparison.
- **Ordinal flourishing-era rankings** — rank-correlation of peak order against independent ordinal knowledge.

A *systematic* offset between city-specific inscription peaks and demographic peaks is reported as a quantitative estimate of the **epigraphic-habit lag** — methodological finding, not a failure.

**Decision (Decision 13).** Bounded exploratory analysis throughout; no pre-committed thresholds; foundation dates corpus-wide; richer independent dates time-boxed.

**Ask.**

- **(a)** **Decomposition method.** Empire-wide habit estimated as the corpus-level `genuine_SPA` from the mixture, with city residual `= city_SPA − w_c · empire_habit` for some normalisation `w_c` — is that the right operationalisation, or would you go for something like a multi-level Gaussian-process decomposition with a global mean function and city deviations?
- **(b)** **Identifiability under sparse anchors.** Foundation dates are sharp; peak-population dates are sparser and uncertain. Is "compare residual peak-time posterior CI to independent anchor" a clean falsifiable design, or is the anchor uncertainty too large to bind in practice?
- **(c)** **The epigraphic-habit-lag estimand.** If we observe a systematic +30 year offset between inscription peak and demographic peak across the case-study set, we want to report it as an empirical lag estimate. Is that econometrically sound, or are we falling into a selection-bias trap (cities with rich enough independent dates are atypical)?

**Where to go for more detail.** Appendix C.2 (habit-removed trajectory deep dive: relationship to the existing Layer A / Layer B small-N city trajectory work in §5; the bounded literature task; expected anchor-set size).

---

### Q7 — Confirmatory claim hierarchy + multiple-comparison policy

**Background.** The preregistration treats its confirmatory claims as a small, *independent* set rather than as an omnibus family:

| Hypothesis | Status | Decision rule |
|------------|--------|---------------|
| H2.1 | Gate for the mixture model | Per-cell coverage ≥ 90 %, ≥ 90 % cells pass; Pearson r ≥ 0.95 on shape in ≥ 90 % cells. Failure → OSF amendment + revision before Phase 3. |
| H3a | Sole primary quantitative confirmatory result | Three-way verdict on `f_within` against 0.10. |
| H3c(i) | Hanson-replication: capitals over-produce | P(contrast > 0) ≥ 0.95 (posterior probability over draws of the Pearson-residual capitals-vs-non-capitals contrast). |
| H3c(ii) | Hanson-replication: residual spatial clustering | Moran's I > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} (conditional permutation inference on posterior-mean Pearson residuals). |

**Explicit policy:**

- Each hypothesis is judged independently. No omnibus "H3c was supported" claim — the paper reports the verdict on each part.
- H3b (the pre-specified deviation-detection at the Antonine and Crisis-of-the-Third-Century probes) is **not** in the confirmatory family — its windows and subsets are pre-specified but no effect-size magnitudes are pre-committed and no Holm-corrected confirmatory family is formed.
- If H3a returns "evidence against," H3c is still reported as Hanson-replication, descriptively.

**Why no multiple-comparison correction.** Four reasons advanced in the prereg's confirmatory-claim-hierarchy paragraph: (i) each hypothesis answers a different substantive question — they're not redundant tests of the same effect; (ii) H2.1 is a gating condition, not a co-equal claim; (iii) the H3c(i) and H3c(ii) replications are independent published findings from Hanson 2021, judged separately; (iv) the project's prior-art is replication-oriented (Hanson 2021 doesn't apply multiple-comparison correction across his own findings either).

**Decision (Field 3, "Confirmatory claim hierarchy").** Independent judgement; no Holm or Bonferroni correction.

**Ask.**

- **(a)** Is "no correction, judged independently" defensible to a sympathetic statistician, or would you require *some* multiplicity adjustment somewhere — e.g. an FDR within the H3c family (two tests) or a stricter posterior-probability threshold on H3c(i) given H3c(ii)?
- **(b)** Is the **"H3a evidence-against → H3c reported descriptively"** rule the right downstream consequence, or should H3c be removed from the published confirmatory family entirely if H3a is against?
- **(c)** Is the **directional three-way verdict on H3a** itself (Decision 18) a defensible alternative to a more standard Bayes-factor-with-RoPE approach? We considered RoPE-ing around 0.10 ± δ but committed to the directional CI rule for legibility.

**Where to go for more detail.** Appendix C.3 (confirmatory-hierarchy deep dive: the H3b exploratory framing; the relationship between H2.1 gating and the other confirmatory claims; the prior-art on multiple-comparison in this corner of archaeological methods).

---

### Q8 — Pre-Phase-2 design artefacts: input on the pinned values before they're committed

**Background.** Several of the prereg's procedural commitments deliberately defer specific numerical values to pre-Phase-2 design artefacts — committed and time-stamped before any Phase 2 analysis runs, but written after the prereg is lodged at OSF. The design pattern (Decisions 19, 20, 21, 25) was to pre-commit *axes and rules* in the prereg body and pin *specific values* in named `runs/...` directories whose commit hashes are referenced by the prereg. Two artefacts are involved:

- `runs/2026-05-XX-recovery-grid-design/` — pins (a) the recovery-grid specific values (α values, shape-library parameter choices, tier-weight vectors, sample sizes, replicate counts, base seed) per Decision 21, and (b) the numerical PPC thresholds per Decision 25. One artefact, two spec tables.
- `runs/2026-05-XX-template-dictionary/` — pins the slab-structure dictionary contents (which century / half-century / reign-interval templates pass the N ≥ threshold inclusion rule, and what the threshold is) per Decision 20.

These artefacts are **not yet built**. They will be written, committed, and time-stamped between OSF lodgement and any Phase 2 analysis run. Your input — at whatever level of engagement you want to offer — is the gating piece of their content.

**Decision (procedural pattern, Decisions 19 / 20 / 21 / 25).** Axes and rules in the prereg; specific values in the artefacts; artefacts committed before Phase 2 begins; the prereg's mention of the artefacts' `runs/...` paths is the cross-reference.

**Ask.**

- **(a)** **Would you like to review the artefacts before they're committed?** If yes, we'd send the draft artefact files (plain markdown / YAML, ~ a few hundred lines each) for your eyes before time-stamping and committing. This is the highest-engagement option and the one most likely to produce defensible numbers.
- **(b)** **Would you like to suggest specific pinned values now**, in writing, that we then propagate into the artefacts? Areas where we are most uncertain and most want your input:
  - **Recovery-grid α values.** We pre-commit "≥ 5 values spanning the empirical pilot range with corner cases included." Without a pilot fit in hand, our straw is `{0.05, 0.20, 0.40, 0.60, 0.80}` — broad coverage with two corner cases. Defensible? Wrong?
  - **Recovery-grid shape-library parameters.** The six shape categories are pre-committed (smooth growth, smooth decline, rise-and-fall, multi-modal, regnal-cluster, flat-baseline); the specific parameterisations of each (e.g. what growth rate, what peak time, what multi-modal frequency) are open.
  - **Recovery-grid tier-weight vectors.** Five vectors pre-committed (uniform, century-heavy, reign-heavy, half-century-heavy, pilot-posterior-drawn). Specific weights within each open.
  - **Recovery-grid replicate count.** Pre-committed ≥ 50 per cell. Default 50 is our straw; doubling to 100 or 200 is cheap if you'd prefer.
  - **Numerical PPC thresholds.** The seven categories of Appendix B.4 with the straw values flagged in Q4(b) — the values we are most uncertain about and most want your input on.
  - **Template-dictionary inclusion threshold.** "N ≥ a stated threshold" for an exact-match template-interval to enter the slab dictionary. We have no straw — frankly, we want your input on what makes statistical sense as a minimum count.
- **(c)** **Are there content categories we have not anticipated** that should also live in the artefacts? Examples that have come up in earlier rounds of review but were not adopted: posterior-predictive spatial-autocorrelation diagnostic for H3a residuals; cross-validation log-likelihood threshold for the mixture fit; pilot-fit calibration check (does the pilot α posterior fall in a plausible prior range *a priori*).
- **(d)** **Engagement format.** Email exchange / annotated draft artefacts / a single call / a structured questionnaire — what fits your bandwidth?

**Where to go for more detail.** Appendix B.2 (recovery-grid spec), Appendix B.4 (PPC thresholds), and §B.1.2 (template-dictionary structure) collectively describe what would land in the artefacts. Decisions 19, 20, 21, and 25 in `planning/decision-log.md` give the procedural-pattern reasoning.

---

## End of question list — appendices follow

The appendices are deep dives, intended to be consulted when a primary or secondary question above raises a follow-up. They reproduce material from the preregistration draft and decision log; where the appendix and the source documents disagree, the source documents govern. Each appendix is independently readable.

- **Appendix A — Project orientation:** corpus details, the artefact diagnosis, the phase / hypothesis map, the analysis-pipeline plain-English walkthrough.
- **Appendix B — Primary-question deep dives:** B.1 (mixture model), B.2 (recovery simulation), B.3 (residuals), B.4 (PPC thresholds).
- **Appendix C — Secondary-question deep dives:** C.1 (H3a within-between NBR), C.2 (habit-removed trajectory), C.3 (confirmatory hierarchy and multiplicity).
- **Appendix D — Supporting reference material:** effect-size table; uncertainty-quantification table; known limitations; provenance.

---

# Appendix A — Project orientation

## A.1 Corpus details

**LIRE v3.0** (Kaše, Heřmánková & Sobotková 2023; Zenodo DOI 10.5281/zenodo.8147298, 11 October 2023). 182,853 inscriptions; 63 attributes in the released parquet. Two filter flags used below are *derived* at filter time:

- `is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT NULL AND not_before ≤ not_after`
- `is_within_RE := province IS NOT NULL`

Filtering with these flags plus a 50 BC – AD 350 date-interval intersect yields **180,609 rows** (≈ 98.8 % of the pre-filter total). Pre-joined Hanson (2016) urban-population estimates are available as `urban_context_pop_est` (joining rule: ancient toponym of the largest city within a 5-km buffer of the inscription findspot).

**Rome excluded** from all scaling regressions as an extreme outlier (Hanson 2021, Table 7.3 caption). Rome alone contributes **65,435 inscriptions** to the filtered corpus (36.2 % of the 180,609-row total, 46.5 % of the 140,575 inscriptions assigned to a Hanson-catalogued city). The Rome-excluded analytical corpus is **115,174 inscriptions**.

**LIST v1.2** (Kaše, Heřmánková & Sobotková 2024; Zenodo DOI 10.5281/zenodo.10473706) is a candidate post-lodgement amendment / follow-up paper dataset; it extends the envelope to 50 BC – AD 600. Not part of this preregistration (Decision 24).

## A.2 The editorial-artefact diagnosis

The earlier draft of this preregistration framed the artefact as "century-midpoint inflation" (peaks at AD 50, 150, 250) and proposed a three-tier anchor-year convention component. Three diagnostic runs on 2026-05-17 — committed at `runs/2026-05-17-interval-width-diagnostic/`, `runs/2026-05-17-empirical-spa-shape/`, and `runs/2026-05-17-date-range-filtered-spas/` — established that:

1. **The headline "midpoint spike" ratios (22.8× / 41.5× / 18.8× O/E at AD 50 / 150 / 250)** were generated by an `int((not_before + not_after) / 2)` test statistic that truncates century-template midpoints (50.5, 150.5, 250.5) to whole years, conflating wide-template-slab loading with midpoint-anchored mass.
2. **The actual per-year-uniform-aoristic SPA over 50 BC – AD 350** shows no anchor-year excess at AD 50 / 150 / 250 (local excess −77 / −79 / +22 relative to the local plateau). The largest narrow spikes are at AD 122.5 (Hadrian) and AD 77.5 (Flavian). The largest single discontinuity is at the 1 BC / AD 1 boundary (+1,159).
3. **Regnal spikes amplify under narrow-precision filtering** (AD 122.5 ratio: 1.61× at full corpus → 4.96× at `date_range ≤ 25` → 13.83× at single-year-precise inscriptions). The plateau-step pattern *weakens* decisively under narrow filtering (Pearson r between SPA(`date_range ≤ 25`) and SPA(`date_range > 100`) = 0.34). Conclusion: regnal spikes are *real ancient clustering*; the plateau-step pattern is *editorial-encoding artefact*.

These three diagnostics drove Decision 20 (the convention component is a template-interval slab structure — centuries, half-centuries, reigns — not anchor-year tiers).

## A.3 Phase / hypothesis map

```text
Phase 1 (completed groundwork)         Phase 2 (Bayesian mixture)        Phase 3 (population analyses)
-----------------------------          ----------------------------      -------------------------
detection thresholds fixed in §6   →   H2.1 recovery-sim validation   →  H3a within-between NBR
(not a confirmatory hypothesis)        (confirmatory; multinomial        on date-window-filtered
                                        likelihood; per-cell coverage    counts (confirmatory;
                                        rule)                            three-way verdict on
                                       H2.2 / H2.3 / H2.4 supporting     f_within against 0.10)
                                       consistency checks (real data)   H3c capitals contrast +
                                                                          Moran's I on Pearson
                                                                          residuals (confirmatory)
                                                                         H3b exploratory
                                                                          deviation-detection
                                                                          at Antonine and Crisis
                                                                          probes
```

## A.4 Plain-English walkthrough (reproduced from prereg)

The full plain-English walkthrough is in `planning/preregistration-draft.md`, lines 133–159. It explains the analysis in plain terms for numerate archaeologists / epigraphers and is the most accessible single description of the pipeline. Reproduced here only as a pointer.

---

# Appendix B — Primary-question deep dives

## B.1 Mixture model deep dive (supports Q1)

### B.1.1 Full likelihood specification

Let `m_t` be the raw per-bin aoristic-mass SPA on a 5-year grid for a subset of `N_eff` inscriptions. Under per-year uniform aoristic, each inscription contributes total mass 1 distributed across the bins its date range covers, so `Σ_t m_t = N_eff` (modulo truncation at the analysis envelope). Define `q_t = m_t / Σ_t m_t` (empirical SPA shape, summing to 1). Convert to integer counts by **largest-remainder rounding**:

```
y_t = lr_round(N_eff · q_t)
   such that Σ_t y_t = N_eff exactly
   (integer parts assigned; residual N_eff − Σ_t ⌊N_eff · q_t⌋ units
    distributed to bins with largest fractional remainders;
    ties broken by bin index)
```

Let `p_conv,t` and `p_gen,t` be non-negative vectors summing to 1 (normalised densities over the analysis envelope). Then:

```
p_t = α · p_conv,t + (1 − α) · p_gen,t
y ~ Multinomial(N_eff, p_t)        # primary likelihood
```

**Supplementary fits (reported alongside, not confirmatory comparators):**

- **Dirichlet-multinomial:** `y_t ~ DirichletMultinomial(N_eff, κ · p_t)` with concentration `κ ~ HalfNormal(prior tuned on pilot fit)`. Reduces to multinomial as `κ → ∞`. Handles bin-level overdispersion.
- **Rescaled NegBin:** `y_t ~ NegativeBinomial(λ_t = N_eff · p_t, φ)` with `1/φ ~ HalfNormal(1)`. The `λ = N_eff · p_t` parameterisation avoids the absolute-scale degeneracy that would arise if `λ_conv,t` and `λ_gen,t` were free.

### B.1.2 Convention component — template-interval slab structure

A dictionary of template intervals, grouped into tiers:

- **Century-slab tier:** uniform mass over `[1, 100]`, `[101, 200]`, `[201, 300]`, `[301, 400]`, and BC equivalents (`[−99, 0]`, `[−199, −100]`).
- **Half-century-slab tier:** uniform mass over empirically-supported half-century templates from the pre-Phase-2 dictionary-build scan (candidates: `[1, 50]`, `[51, 100]`, `[125, 175]`, etc.).
- **Reign-interval-slab tier:** uniform mass over reign-interval templates (Augustan `[−27, 14]`, Tiberian, Flavian `[78, 79]`, Trajanic, Hadrianic `[117, 138]`, Antonine `[161, 180]`, Severan `[212, 217]`).

Within each tier, each template's mass is normalised to its template width. Tier-level weights are estimated jointly with α. Year-precise inscriptions (`[t, t]` encodings) are *not* in the convention component — they remain in `genuine_SPA` as real ancient anchoring.

**Dictionary-build procedure (pre-Phase-2, not preregistration substance):** scan the filtered corpus for exact-match interval templates; include any template with N ≥ a stated threshold (threshold pinned in the implementation scan's run report at `runs/2026-05-XX-template-dictionary/`). The committed empirical scan replaces a curated 13-year list from the superseded Decision 17. The procedural commitment is the prereg-binding part; the actual dictionary contents are implementation artefacts.

### B.1.3 Genuine component

A smooth non-negative density over the analysis envelope, with a **Gaussian random-walk smoothness prior** and a weakly-informative bandwidth.

### B.1.4 Priors

- `α ~ Beta(2, 2)` (centred at 0.5, weakly-informative).
- Tier weights `~ Dirichlet(uniform)`.
- Genuine-component smoothness `σ ~ HalfNormal(1)`.

### B.1.5 Fit and convergence

Posterior sampling via **pymc** (Hamiltonian Monte Carlo / NUTS) for the multinomial primary; the Dirichlet-multinomial and rescaled NegBin supplementaries also fit in pymc.

**Convergence diagnostics:** Gelman-Rubin `R̂ < 1.01` on all parameters; effective sample size ≥ 400 per chain on α and tier weights; no divergences. Failure of any diagnostic triggers an OSF amendment.

### B.1.6 Identifiability and aoristic-uncertainty propagation

**Identifiability concerns we anticipate:**

- If the genuine component's smoothness prior is too permissive, it can absorb century-slab structure that should be attributed to the convention component (and conversely).
- The Beta(2, 2) prior on α is symmetric around 0.5; we don't know the empirical α range yet (the pilot fit informs that).
- Pathological case: a genuine SPA that happens to be a smooth interpolation of the slab structure is unidentifiable from convention alone.

**Why aoristic uncertainty is upstream not per-inscription.** We considered per-inscription latent-date sampling propagated into the likelihood (each inscription with date range `[nb_i, na_i]` would have a latent `t_i ~ Uniform(nb_i, na_i)` in the model). We rejected this for the primary because (i) it dramatically expands the parameter space (N_eff ~ 10^5 latent dates); (ii) we expect the aoristic-uncertainty effect on α to be small at corpus scale (the mixture is a *shape* model on binned mass, and the per-year uniform aoristic deterministically maps interval data to bin mass — re-sampling within each interval would average to the same expectation). **This is one of the questions where we explicitly want your judgement** — see Q1(c).

### B.1.7 Cross-references

- Decision 19 (likelihood family): `planning/decision-log.md` lines 1517–1645.
- Decision 20 (slab structure): `planning/decision-log.md` lines 1647–1825.
- Prereg §3 "Bayesian deconvolution-mixture model": `planning/preregistration-draft.md` lines 177–205.

---

## B.2 Recovery-simulation deep dive (supports Q2)

### B.2.1 The grid axes (prereg-binding)

| Axis | Pre-committed scope | Specific values pinned in `runs/2026-05-XX-recovery-grid-design/` |
|------|---------------------|-------------------------------------------------------------------|
| α | ≥ 5 values spanning the empirical pilot range; corner cases (near 0, near 1) included | Pilot-informed |
| Genuine-shape library | ≥ 6 shapes: {smooth growth, smooth decline, rise-and-fall, multi-modal, regnal-cluster (mirroring AD 77.5 / 122.5 / 212.5 empirical pattern), flat-baseline} | Concrete parameter choices in artefact |
| Tier-weight vectors | ≥ 5 vectors: {uniform across tiers, century-heavy, reign-heavy, half-century-heavy, pilot-posterior-drawn} | Concrete vectors |
| Sample sizes | Representative N values from empire, province, urban-area levels | Pinned from Phase 1's reachability map |
| Replicates per cell | ≥ 50 | Specific count (default 50) |
| Seed policy | Cell-deterministic (seed = base_seed + cell_index) | Specific base_seed |

### B.2.2 The validation rule

**A cell passes coverage** iff ≥ 90 % of its replicates produce a posterior 95 % CI on α that contains the true α (proper repeated-sampling coverage at the cell level — this is the part the previous draft got wrong; the previous draft ran one synthetic per cell and asked whether that one CI contained the truth, which doesn't establish coverage).

**The mixture is validated** iff:

1. ≥ 90 % of cells pass coverage, AND
2. The posterior-median Pearson r between recovered and known genuine SPA is ≥ 0.95 in ≥ 90 % of cells.

**Cell-wise reporting required** (not just global mean): the report identifies any cells that fail and characterises the failure mode.

### B.2.3 Failure response

Either failure (coverage or shape) triggers an **OSF amendment** and model revision before any Phase 3 analysis runs. Likely revisions: re-parameterisation of the convention tier weights; smoothness prior on the genuine component; alternative tier composition; alternative observation-model family (D19's Dirichlet-multinomial or rescaled NegBin promoted to primary).

### B.2.4 Why the H2.1 wording was corrected

The original H2.1 wording read "the posterior α̂ falls within the 95 % CI of the true α" — backward (the true α is fixed; the posterior is the distribution; the CI is on α̂). The corrected wording is "the posterior 95 % credible interval for α contains the known true α." This is the rule.

### B.2.5 The design artefact's dual role

`runs/2026-05-XX-recovery-grid-design/` pins both:

1. The recovery-grid specific values (this appendix).
2. The numerical PPC thresholds (Appendix B.4).

One artefact, two spec tables. Committed before any Phase 2 analysis runs; the prereg names this artefact and binds the grid + PPCs to its commit hash.

### B.2.6 Cross-references

- Decision 21: `planning/decision-log.md` lines 1828–1965.
- Prereg §4 "Phase 2 — Bayesian mixture validation": `planning/preregistration-draft.md` lines 301–316.

---

## B.3 H3c residuals deep dive (supports Q3)

### B.3.1 The residual definition (binding)

```
For posterior draw s and city c:
  r_c,s = (y_c − μ_c,s) / sqrt(μ_c,s + μ_c,s² / φ_s)
```

where `μ_c,s` is the full posterior mean for city c on draw s, **including the province random intercept α_province[c]** (so the residual is relative to the Mundlak NBR's full city-level mean, not just the population-only fixed effect), and `φ_s` is the posterior overdispersion-parameter draw.

Why include the random intercept? Two arguments. (a) Mathematically, μ_c,s should reflect the full conditional mean of the model — that's the residual's denominator-by-construction. (b) Practically, excluding the random intercept would push provincial-level structure into the residuals, which would then be picked up by Moran's I as "spatial structure" when it's really "provincial-block structure." Including the random intercept means H3c(ii) tests for *residual* spatial structure beyond the province blocks.

### B.3.2 H3c(i) — capitals contrast (binding)

```
For posterior draw s:
  contrast_s = mean(r_c,s | c ∈ provincial_capitals)
             − mean(r_c,s | c ∉ provincial_capitals)
Decision rule:
  P(contrast > 0) ≥ 0.95
  (posterior probability over draws)
```

### B.3.3 H3c(ii) — Moran's I (binding)

```
r_c = posterior mean residual
    = (1/S) · Σ_s r_c,s
For each k ∈ {5, 8, 10}:
  Compute Moran's I on r_c with k-NN row-
    standardised spatial weights
  Conditional permutation inference (999
    permutations of r_c over fixed weights)
Decision rule:
  Moran's I > 0 at p < 0.05 in ≥ 2 of {k = 5, 8, 10}
```

### B.3.4 Supplementary reporting (binding)

Posterior distribution of Moran's I across draws (per k): for each posterior draw s, compute `I_s` on `r_·,s` with the same k-NN weights. Report as 2.5 / 50 / 97.5 percentiles of I_s per k. Makes posterior uncertainty visible without replacing the field-standard permutation rule.

### B.3.5 Why the asymmetric inferential treatment

The capitals contrast naturally lives in posterior space — "does the contrast exceed 0 with high posterior probability?" — and draw-wise computation directly answers it. Moran's I has a field-standard frequentist permutation procedure (Cliff & Ord 1981; Anselin's conditional permutation); using posterior-mean residuals preserves the field-standard inference for the confirmatory rule while reporting the posterior distribution of I supplementarily.

The two tests answer different questions (a categorical contrast vs a spatial-structure test); using the natural inferential framework for each is more defensible than forcing both into the same scheme. **But this is one of the points we'd most like your judgement on** — see Q3(b).

### B.3.6 Hanson 2021's published numbers (for replication)

- Capitals contrast: mean residual 0.43 for provincial capitals vs ~ 0.06 for *coloniae* / *municipia* (Hanson 2021, p. 148).
- Moran's I: I = 0.046, z = 4.571, *p* < 0.0001 for residuals; I = −0.006, z = −1.076, *p* = 0.282 for raw counts (Hanson 2021, Table 7.4). ArcGIS default Spatial Autocorrelation tool used; weights construction unspecified. Exact-numerical-match is not feasible; we test the *direction and rejection-of-null*, not the specific I value.

### B.3.7 Cross-references

- Decision 23: `planning/decision-log.md` lines 2108–2261.
- Prereg "Residual analysis (H3c)" and "Spatial clustering (H3c)": `planning/preregistration-draft.md` lines 257–259.

---

## B.4 PPC thresholds deep dive (supports Q4)

### B.4.1 Trigger categories (prereg-binding)

**Straw values flagged as provisional placeholders.** The numerical values below are back-of-envelope guesses, not commitments — input on every row is welcome (see Q4(b) and Q8 for the explicit ask).

| # | Category | Numerical bound type | Provisional straw value (input invited) |
|---|----------|----------------------|-----------------------------------------|
| 1 | Prior-predictive 99th-percentile per-city count | Cap (sanity bound on prior tail) | TBD — no straw yet |
| 2 | Posterior-predictive *mean* | Within X % of observed | Straw: X = 5 % |
| 3 | Posterior-predictive *std* | Within Y % of observed | Straw: Y = 10 % |
| 4 | Posterior-predictive 95th-percentile tail count | Within bounds of observed | Straw: ± 20 % |
| 5 | Posterior-predictive proportion-of-zeros | Within bounds of observed | TBD — no straw yet |
| 6 | Residual-vs-fitted slope (std. Pearson over μ̂) | Absolute slope < threshold | Straw: 0.05 |
| 7 | Province-level residual dispersion | Within-province vs grand variance ratio bounds | Straw: 0.5–2.0 |

### B.4.2 Failure response

Any tripped trigger initiates model revision (revising priors, link function, or model structure). The **originally-preregistered model result is reported alongside** the revised model's result in the paper — confirmatory status preserved for the original; revised model reported as transparent post-hoc revision. An OSF amendment is filed before final results are lodged.

**No PPC trigger is used to test a hypothesis** — these are diagnostic checks on model fit, not confirmatory tests.

### B.4.3 Relationship to H2.1

The same `runs/2026-05-XX-recovery-grid-design/` design artefact pins both the recovery-grid spec (Appendix B.2) and the PPC numerical thresholds (this appendix). One artefact, two spec tables. The artefact is committed before any Phase 2 analysis runs.

### B.4.4 Cross-references

- Decision 25: `planning/decision-log.md` lines 2345–2434.
- Prereg "Prior predictive checks" and "Posterior predictive checks" sections under H3a in §3: `planning/preregistration-draft.md` lines 245–253.
- Prereg §7 contingencies: `planning/preregistration-draft.md` lines 387–396.

---

# Appendix C — Secondary-question deep dives

## C.1 H3a within-between NBR deep dive (supports Q5)

### C.1.1 The full model

```
y_c ~ NegativeBinomial(μ_c, dispersion)
log(μ_c) = α_0 + α_province[c]
          + β_within  · (log_pop_c − log_pop_province_mean[c])
          + β_between · log_pop_province_mean[c]

Priors (preregistered, weakly-informative):
  α_0          ~ Normal(0, 5)        # intercept on log-count scale
  β_within     ~ Normal(0, 1)        # weakly-informative; prior-predictive checked
  β_between    ~ Normal(0, 1)        # weakly-informative
  α_province   ~ Normal(0, σ_prov)   # random intercepts
  σ_prov       ~ HalfNormal(1)       # provincial heterogeneity
  1/dispersion ~ HalfNormal(1)       # overdispersion
```

### C.1.2 Response variable scope

`y_c` is the per-city inscription count under the 50 BC – AD 350 date-window filter — **not** mixture-corrected. Mixture-correction applies to *temporal* analyses (H2.1 validation, H3b deviation-detection). The mixture's empire-level posterior α is reported as descriptive context, but neither H3a's confirmatory rule nor H3c's residuals are gated on it. This is a real scope limit, flagged as a Known Limitation; it traces to the unidentifiability of per-city mixture fits for ~ 600 of ~ 815 cities with N < 100. See Decision 22 for the explicit reasoning and the rejected alternatives (the "specify a corrected response" and the "hybrid: corrected on ~ 200 high-N cities" paths).

### C.1.3 Predictor scaling

`log_pop_c` is on the natural log scale. The within-province deviation `(log_pop_c − log_pop_province_mean[c])` and the province-mean `log_pop_province_mean[c]` enter the linear predictor *unstandardised*. Under this scaling, `Normal(0, 1)` on `β_within` and `β_between` is weakly-informative: it places ~ 68 % prior mass on |β| < 1, corresponding to multiplicative effects up to ~ 2.7× per unit-log-population deviation. Sensitivity to standardisation reported as an exploratory check.

### C.1.4 The estimand

```
f_within = Var(β_within · (log_pop_c − log_pop_province_mean[c])) / Var(log E[inscriptions_c])
         (computed per posterior draw, on the latent log scale,
          unweighted across cities Rome-excluded)
```

The numerator is the within-province population contribution; the denominator is the total variance in the linear predictor on the log scale, computed on the same posterior draw to avoid scale ambiguity.

### C.1.5 The three-way decision rule

- **Supported:** posterior 95 % CI for `f_within` wholly above 0.10.
- **Evidence against:** wholly below 0.10.
- **Inconclusive:** straddles 0.10.

Supplementary reporting (binding alongside the verdict): P(f_within > 0.05), P(f_within > 0.10), P(f_within > 0.20).

### C.1.6 The brms / pymc shadow

Primary implementation in `pymc` (Python). Secondary `brms`-via-R cross-validation shadow (~ 50 lines, committed as `scripts/h3a_brms_shadow.R`): refits the same within-between model in R + Stan, providing (i) cross-language validation that pymc and brms agree on the posterior within Monte Carlo noise and (ii) legibility for R-native co-authors. The brms shadow's negative-binomial dispersion-prior parameterisation requires a small Jacobian adjustment to match pymc's preregistered `1/dispersion ~ HalfNormal(1)` prior; details (the `stanvar()` block and the Jacobian derivation) are in the script's docstring and supplementary material.

### C.1.7 Hanson 2021's OLS log-log comparator

The H3a Bayesian NBR coefficient is supplemented by an OLS log-log regression for direct comparability to Hanson, Ortman & Lobo 2017 and Hanson 2021's β = 0.672 site-level exponent. Comparator, not confirmatory.

### C.1.8 Cross-references

- Decision 12 (Mundlak + variance-fraction estimand): `planning/decision-log.md` lines 710–828.
- Decision 18 (three-way decision rule): `planning/decision-log.md` lines 1420–1515.
- Decision 22 (date-filtered scope, not mixture-corrected): `planning/decision-log.md` lines 1968–2106.
- Prereg "Bayesian NBR for H3a": `planning/preregistration-draft.md` lines 206–255.

---

## C.2 Habit-removed residual trajectory deep dive (supports Q6)

### C.2.1 The decomposition

For each city c:

```
SPA_c(t) = w_c · habit(t) + residual_c(t)
```

where `habit(t)` is an empire-wide habit-curve estimate (from the corpus-level `genuine_SPA` produced by the mixture, or — as a simpler alternative — directly from the corpus-level raw SPA with appropriate normalisation), and `w_c` is a city-specific scale.

### C.2.2 Anchor types (in priority order)

| Anchor | Coverage | Prediction sharpness |
|--------|----------|----------------------|
| Foundation dates | Corpus-wide; well-attested in standard references | Very sharp: ~ zero residual SPA mass before the year of foundation |
| Independent peak-population dates | Bounded case-study set | Posterior-CI calibration (does the independent date fall in the posterior peak-time CI?) |
| Multi-point independent trajectories | A few well-studied cities (Pompeii, Ostia, etc.) | Full-shape comparison; overlaps the small-N Layer A / Layer B work in prereg §5 |
| Ordinal flourishing-era rankings | Where absolute dates are unavailable | Rank-correlation of SPA-peak order against independent ordinal knowledge |

### C.2.3 The epigraphic-habit-lag estimand

If we observe a systematic offset between city-specific inscription peaks and independent demographic peaks across the case-study set, we report it as a quantitative estimate of the **epigraphic-habit lag** — a methodological finding (the habit responds with a lag to the underlying demography), not a failure of the analysis. The lag is reported as a posterior mean offset across the case-study cities, with explicit caveats about case-study selection bias.

### C.2.4 Why "exploratory throughout"

Independent-anchor evidence is too sparse and uncertain to bind: foundation dates are corpus-wide and sharp but only constrain the *left edge* of a residual trajectory; peak-population dates are at most a handful, with their own uncertainty; multi-point independent trajectories exist for very few cities. No pre-committed thresholds; results reported descriptively.

### C.2.5 Cross-references

- Decision 13: `planning/decision-log.md` lines 829–928.
- Prereg §5 "Temporal habit-removed residual trajectory analysis": `planning/preregistration-draft.md` lines 332–338.

---

## C.3 Confirmatory-hierarchy deep dive (supports Q7)

### C.3.1 The full confirmatory family

| # | Hypothesis | What it tests | Decision rule | Status |
|---|------------|---------------|---------------|--------|
| 1 | H2.1 | Recovery validation of the mixture | ≥ 90 % cells achieve per-cell coverage (≥ 90 % replicates' 95 % CIs containing α); Pearson r ≥ 0.95 on shape in ≥ 90 % cells | Gate for the mixture; failure → revision + amendment before Phase 3 |
| 2 | H3a | Within-province population-attributable variance fraction | Three-way verdict on `f_within` against 0.10 | Sole primary quantitative confirmatory result |
| 3 | H3c(i) | Provincial capitals over-produce relative to non-capitals | `P(contrast > 0) ≥ 0.95` (posterior probability over draws) | Hanson-replication |
| 4 | H3c(ii) | Spatial clustering of residuals | Moran's I > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10} | Hanson-replication |

### C.3.2 Outside the confirmatory family

- **H3b** (pre-specified exploratory deviation-detection at the Antonine and Crisis windows): windows and subsets pre-specified, but no effect-size magnitudes pre-committed; no Holm-corrected confirmatory family formed. Results reported descriptively against project effect-size brackets.
- **H2.2 / H2.3 / H2.4** (real-data internal-consistency checks): not validation in their own right; reported alongside the recovery simulation.

### C.3.3 No multiple-comparison correction — the four arguments

1. Each hypothesis answers a different substantive question; they are not redundant tests of the same effect.
2. H2.1 is a gating condition, not a co-equal claim — it's the validation of the mixture, run before any Phase 3 analysis.
3. The H3c(i) and H3c(ii) replications are independent published findings from Hanson 2021, judged separately rather than as an omnibus replication.
4. The project's prior-art is replication-oriented (Hanson 2021 does not apply multiple-comparison correction across his own findings either).

### C.3.4 The "H3a evidence against" downstream rule

If H3a returns "evidence against the non-trivial-share claim," H3c is still reported as Hanson-replication (it tests a separate question — capitals and clustering — regardless of whether population explains a non-trivial variance share). The paper's headline becomes "H3a evidence against the non-trivial-share claim; H3c results reported descriptively as Hanson-replication."

### C.3.5 Cross-references

- Decision 18 (directional / three-way H3a verdict): `planning/decision-log.md` lines 1420–1515.
- Prereg Field 3 "Confirmatory claim hierarchy": `planning/preregistration-draft.md` lines 80–88.

---

# Appendix D — Supporting reference material

## D.1 Effect-size pre-specifications

The full table from the preregistration (`planning/preregistration-draft.md` lines 366–386):

| Hypothesis | Quantity | Preregistered target |
|---|---|---|
| **Confirmatory** | | |
| H2.1 (recovery simulation) | Per-cell α coverage | ≥ 90 % of grid cells achieve per-cell coverage; a cell passes iff ≥ 90 % of replicates produce a posterior 95 % CI containing the true α. Cell-wise results reported. |
| H2.1 (recovery simulation) | Genuine-shape recovery | Posterior-median Pearson r ≥ 0.95 between recovered and true genuine SPA in ≥ 90 % of cells. |
| H3a primary | Within-province population-attributable variance fraction `f_within` | Three-way verdict: supported (posterior 95 % CI wholly above 0.10), evidence against (wholly below), inconclusive (straddles). Supplementary: P(f_within > 0.05), P(> 0.10), P(> 0.20). |
| H3c(i) | Capitals contrast on draw-wise Pearson residuals | P(mean(r_c | capitals) − mean(r_c | non-capitals) > 0) ≥ 0.95. |
| H3c(ii) | Moran's I on posterior-mean Pearson residuals | I > 0 at *p* < 0.05 in ≥ 2 of {k = 5, 8, 10}. Supplementary: posterior distribution of I per k. |
| **Supporting consistency (real data, Phase 2)** | | |
| H2.2 | Boundary-step reduction in corrected SPA | Per template boundary year (0, 100, 200, 300), corrected step magnitude reduced by ≥ 50 % relative to uncorrected SPA. |
| H2.3 | Pairwise Pearson r across threshold variants | r ≥ 0.9 between any two threshold-filtered `genuine_SPA` variants. |
| H2.4 | Stratified-by-convention-class SPA vs deconvolved | Agreement within sampling error (continuous discrepancy reported). |
| **Completed groundwork (Phase 1, fixed; not confirmatory)** | | |
| Phase 1 power floor | Detection rate | ≥ 0.80 at *p* < 0.05 per bracket; zero-effect FP rate ≤ 0.05 (achieved across 96 zero-effect cells, range [0.007, 0.049]). |
| Phase 1 thresholds (50 % over ≥ 50 y) | min n at detection ≥ 0.80 | **province** exp-step 1938, exp-gauss 1869, cpl-3-step 1385, cpl-3-gauss 1618; **urban-area** exp-step 1923, exp-gauss 1854, cpl-3-step 1409, cpl-3-gauss 1549; **empire** reachable at n = 50,000. |
| Phase 1 thresholds (doubling over ≥ 25 y) | min n at detection ≥ 0.80 | Gaussian shape: empire reachable at n = 50,000; province exp 2118, cpl-3 1934; urban-area exp 2160, cpl-3 1905. Step shape unreachable across all levels. |
| Phase 1 thresholds (20 % over 25 y; hard-test boundary) | min n at detection ≥ 0.80 | Empire / cpl-3 / Gaussian reachable at n = 50,000 (single marginally-reachable cell); all other combinations unreachable. Bracket retained as honest-uncertainty anchor; not in the H3b family. |
| **Pre-specified exploratory** | | |
| H3b Antonine probe | Deviation at AD 165–180 | Permutation-envelope departure at empire, Asclepius-cult, military subsets; descriptive against project brackets; no pre-committed magnitude. |
| H3b Crisis-of-the-Third-Century probe | Deviation at AD 235–284 | Permutation-envelope departure at empire and Western-Empire-provincial subsets; descriptive against project brackets; no pre-committed magnitude. |

## D.2 Uncertainty-quantification table

From the preregistration (`planning/preregistration-draft.md` lines 265–275):

| Analysis | Quantity | Interval method |
|---|---|---|
| Phase 1 (completed) | Detection rate per cell | Wilson score 95 % interval on the proportion of simulation iterations with *p* < 0.05 (n_iter = 1,000). |
| Permutation envelope (H3b) | The envelope itself | 2.5 / 97.5 percentiles of MC replicate distribution per bin (pointwise 95 % envelope); significance via Timpson et al. (2014) global *p*. The envelope *is* the uncertainty representation — no separate interval is computed. |
| H2.1 (recovery) | α, recovered genuine-SPA shape | Posterior 95 % CI on α per grid cell (Bayesian mixture); Pearson r between recovered and known genuine shape as a posterior distribution. Coverage computed per cell across replicates. |
| H2.2 | Boundary-step reduction | Direct point estimate from the corrected `genuine_SPA`; reported per template boundary year. |
| H2.3 | Pairwise Pearson r across threshold-filtered SPAs | Nonparametric bootstrap percentile interval (rows resampled with replacement). |
| H3a | β_within, β_between, variance fraction, Bayesian R² | Posterior 95 % CIs, computed directly from the fitted posterior. Bootstrap is *not* used — the posterior already represents the full uncertainty. |
| H3c(i) | Capitals contrast | Posterior 95 % CI on the draw-wise contrast; decision rule reported as P(contrast > 0). |
| H3c(ii) | Moran's I | Conditional permutation inference (999 permutations of posterior-mean Pearson residuals over fixed spatial weights) — the field-standard significance procedure for Moran's I — reported for each of k = 5, 8, 10. Supplementary: posterior distribution of I across draws per k. |

## D.3 Known limitations (selected; preregistered)

From the preregistration (`planning/preregistration-draft.md` lines 412–423):

- **Editorial-template artefact identification.** The Bayesian mixture addresses wide-template editorial encoding (century, half-century, reign-interval templates). Year-precise inscriptions are not modelled as artefact — they remain in `genuine_SPA` as real ancient anchoring. Other documented LIST / LIRE artefacts (province-label anachronism; EDCS coordinate imprecision; 50 % missing coordinate provenance) remain as interpretive caveats.
- **BC / AD boundary step.** The empirical SPA shows a +1,159 step at the 1 BC / AD 1 boundary — the largest single discontinuity in the analysis envelope, attributable to the BC / AD calendar-convention boundary (1 BC followed directly by AD 1; no year 0 in the Julian / Gregorian calendar) and the comparative rarity of inscriptions firmly dated to the late Republic. *Not* currently modelled as a separate convention-component tier; the `genuine_SPA` will inherit any residual structure at this boundary. Flagged as a known limitation.
- **H3a and H3c use date-window-filtered counts, not mixture-corrected counts.** The Bayesian mixture corrects temporal SPA analyses (H2.1, H3b); it is *not* applied to the cross-sectional H3a regression. H3c's Pearson residuals are derived from H3a's posterior and inherit H3a's date-filtered-count scope. A per-city mixture fit was not pursued because it would be unidentified for ~ 600 of ~ 815 cities (N < 100). Cross-sectional artefact protection for H3a and H3c is the 50 BC – AD 350 date-window filter. Neither H3a's variance-fraction posterior nor H3c's residual analyses propagate mixture-posterior uncertainty into their credible intervals — a genuine scope limit.
- **Western-Empire provincial subset frontier classifications.** Three provinces in the Latin-classification set sit on the linguistic frontier (Moesia Inferior; Moesia Superior; Sicilia). Classification choice (all three included as "Latin") is the project's existing operational rule; reported transparently; not tested as a sensitivity (post-hoc Moesia / Sicilia exclusion reserved for follow-up).
- **Between-province population effect not separately identifiable.** Mundlak specification cleanly identifies the within-province effect; between-province component entangled with `α_province` — province-level "everything else." Reported but explicitly flagged.
- **Rome exclusion.** Rome is excluded from scaling regressions as an extreme outlier. Consistent with Hanson (2021) methodology; reported transparently; not tested as a sensitivity.
- **Hanson population uncertainty.** Hanson (2016) population estimates carry their own uncertainty, treated as exact in the H3a primary regression. A measurement-error sensitivity is preregistered in §5 (σ_pop ∈ {0.1, 0.2, 0.3}) to quantify the impact on `f_within`.
- **Chronological envelope.** 50 BC – AD 350 (LIRE v3.0). Late Antique and post-AD-350 phenomena out of scope; envelope extension to AD 600 via LIST v1.2 is a candidate for either a post-lodgement OSF amendment or a follow-up paper.

## D.4 Provenance and key references

**Project leads.** Shawn Ross (Macquarie University). Adela Sobotková (Aarhus University) — collaborator on the LIRE / LIST corpora and the broader research programme.

**Key references for this pack.**

- Mundlak, Y. (1978). On the pooling of time series and cross section data. *Econometrica* 46(1), 69–85.
- Bell, A. & Jones, K. (2015). Explaining fixed effects: random effects modeling of time-series cross-sectional and panel data. *Political Science Research and Methods* 3(1), 133–153.
- Hanson, J. W. (2016). *An Urban Geography of the Roman World, 100 BC – AD 300*. Archaeopress. (Population data; OXREP Roman Cities Dataset.)
- Hanson, J. W. (2021). The Distribution of Inscriptions in the Roman Empire. In Brughmans & Wilson (eds.), *Simulating Roman Economies* 138–168. (β = 0.672 scaling; capitals over-production; Moran's I = 0.046.)
- Carleton, W. C. et al. (2025). Sociopolitical Complexity in the Roman Empire. *Cliodynamics* (β ≈ 0.3–0.5 scaling for elite-honorific subsets.)
- Hanson, J. W., Ortman, S. G. & Lobo, J. (2017). Urbanism and the division of labour in the Roman Empire. *Journal of the Royal Society Interface* 14(136), 20170367.
- Crema, E. R. (2025). baorista: Bayesian aoristic estimation in R. (CRAN package; smoke-validated on the project compute server.)
- Crema, E. R. & Bevan, A. (2021). Inference from large sets of radiocarbon dates: software and methods. *Radiocarbon* 63(1), 23–39.
- Timpson, A. et al. (2014). Reconstructing regional population fluctuations in the European Neolithic using summed radiocarbon dates: a new case-study using an improved method. *Journal of Archaeological Science* 52, 549–557.
- Timpson, A., Barberena, R., Thomas, M. G., Méndez, C. & Manning, K. (2021). Directly modelling population dynamics in the South American Arid Diagonal using 14C dates. *Philosophical Transactions of the Royal Society B* 376, 20190723. (CPL methodology.)
- Anselin, L. (1995). Local indicators of spatial association — LISA. *Geographical Analysis* 27(2), 93–115. (Conditional-permutation Moran's I; k-NN weights convention.)
- Cliff, A. D. & Ord, J. K. (1981). *Spatial Processes: Models and Applications*. Pion. (Moran's I.)
- Gelman, A., Goodrich, B., Gabry, J. & Vehtari, A. (2019). R-squared for Bayesian regression models. *The American Statistician* 73(3), 307–309. (Bayesian R² used as comparator.)

**AI contributions to this preregistration.** Theoretical-frame refinements (identifiability scope, the scaling-residual sensitivity flag, the cultural-translator confound strategy), articulation of the deconvolution-mixture model, the template-interval slab convention-component structure, the temporal habit-removed residual trajectory framing, and this preregistration draft were carried out by Claude Code (Anthropic, Opus 4.7) under Shawn Ross's direction. All substantive AI intellectual contributions are logged in the project repository.

---

*End of consultation pack.*
