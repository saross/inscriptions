---
title: "Paper draft fragment — reachability guide for the inscription-SPA method"
date: 2026-05-22
audience: "Shawn (for incorporation into the main paper); colleague reviewers concerned about minimum-N thresholds"
purpose: "Pre-empt the 'isn't 1,549 inscriptions too high?' objection by characterising what's reachable across a fuller grid of effect sizes and sample sizes."
status: "draft fragment; intended for §3 (Methods) or §6 (Discussion / Limitations) of the main paper"
---

# What kinds of effects can be detected at what sample sizes?

## The basic point

A frequent — and well-grounded — concern about quantitative inscription studies is that the data are sparse relative to the questions practitioners want to ask. Many cities have only a few hundred dated inscriptions; many subset-of-interest queries (collegia / guild inscriptions; military diplomas; specific religious dedications; epitaphs of named status groups) reduce the working corpus further. Before committing analytic effort, a practitioner reasonably wants to know: *what kinds of temporal patterns can my method credibly detect in a subset of this size, and what kinds will look like noise even when they're real?*

The preregistered Phase 1 simulation (see §3) gives this answer directly. It plants known temporal deviations of pre-specified size, duration, and onset-shape into synthetic corpora across an 11-point sample-size grid (N ∈ {25, 50, 100, 250, 500, 1,000, 2,500, 5,000, 10,000, 25,000, 50,000}) and three analysis levels (empire / province / urban-area), then runs the preregistered permutation-envelope detection method on each cell and measures the detection rate. The binding-bracket headline figure quoted elsewhere in the paper — minimum N ≈ 1,549 for credible 50 %-over-50-y detection at province / urban-area level — is the conservative reading of one cell of this grid. The full grid is more informative.

## Reachability across the grid (Table X)

[INSERT FIGURE: `runs/2026-05-22-reachability-guide/outputs/figures/historian-reachability-heatmap-gaussian.png`]

Reading the table: each cell reports the detection rate (fraction of trials in which the method correctly identified a planted effect) for a given combination of sample size N (rows), effect bracket (columns), and analysis level (panel). Green cells (≥ 0.80) are reliably reachable at the conventional 80 % power threshold. Yellow cells (≈ 0.50 – 0.80) are reachable for some null-model assumptions but not others — partial. Red cells (< 0.50) are effectively unreachable: in such a cell the method will more often miss a real effect than detect it, and any positive result is dominated by sampling noise.

Three patterns are worth flagging:

1. **The minimum-N threshold depends strongly on the effect's shape and duration.** For the binding-bracket effect (50 % amplitude sustained over a 50-year window, Gaussian-tapered), reliable detection requires N ≳ 2,500 at province or urban-area level. For stronger, narrower events (a doubling over 25 years — the kind of fluctuation a major plague or sudden colonial expansion might produce), the threshold is similar (~ 2,500 – 5,000), and the detection rate continues to climb with N. For weaker, narrower events (20 % over 25 years), the method does not reliably detect them at any sample size we tested — the detection rate at N = 25,000 is still below 0.65. These smallest events are below the method's resolving power.

2. **Below ~ 1,000 inscriptions, almost no effect is reliably detectable at the preregistered false-positive rate.** This is not a limitation of our specific method — it is a fundamental statistical-power constraint of inscription-SPA inference. A subset with N ≤ 500 carries enough signal for descriptive shape comparison (Layer A in §5) and for cross-sectional analyses that pool across subsets, but not for confirmatory temporal deviation-detection.

3. **Detection-rate behaviour is non-monotonic at intermediate N for some brackets.** This is not noise: the simulation uses 1,000 Monte Carlo replicates per cell. It reflects the interaction between the planted effect's shape and the null model's flexibility. A piecewise-linear null with three knots can sometimes absorb a planted Gaussian-tapered deviation; this is a worst-case property we report transparently rather than smooth over.

## What this means for practical study design

This grid is designed to be consulted *before* an analysis is launched, not after. Given a substantive question and a subset of N inscriptions, the practitioner can read the table and decide one of three things:

- **Reachable at confirmatory power**: run the preregistered permutation-envelope test with credible interpretation.
- **Partial reachability**: run the test but pre-specify the result will be reported with explicit uncertainty about Type II error.
- **Below threshold**: do not run the confirmatory test; the inscription series can still support descriptive comparative work (per §5 Layer A) or contribute leverage to the cross-sectional regressions (§3, H3a), but it cannot bear the inferential load of a temporal-trajectory claim on its own.

The table also makes explicit what the method **can't** do: smaller subsets (a few hundred inscriptions or fewer), short events (under 25 years), and weak amplitude shifts (under 20 %) are not in scope, regardless of how interesting the historical question is. For those cases, inscriptions remain one evidence stream among several — to be triangulated with archaeology, textual sources, numismatic data, and survey results, rather than read as a stand-alone temporal record.

## Worked example: the collegia / guild inscription subset

To illustrate how this works in practice, consider a substantive question of historical interest: *did Roman collegia (occupational and burial associations) experience a measurable inflection in their epigraphic visibility during the late Antonine and Severan periods, when their juridical status was being clarified by imperial legislation?* The supporting corpus is LIRE inscriptions containing collegium-related terms (`collegium`, `collegia`, *sodalicium*, *corpus*, etc.) — call it `N_collegia`.

At empire-wide scale, the collegia subset is in the low thousands of inscriptions (a precise count would be derived during analysis). Reading the table at the relevant N value:

- For the empire-wide trajectory at N ≈ 2,500 – 5,000, the **50 %-over-50-y bracket is reliably detectable** (detection rate ≥ 0.95 in our simulation grid). A historian could credibly ask "did empire-wide collegia-epigraphy production show a sustained 50 %-amplitude inflection across the AD 175 – 225 window?" — and either find it, or report a credible null.
- At provincial level — say, just the western Latin-Mediterranean collegia subset — N drops by perhaps 50 %, to ~ 1,500. This is at the very lower edge of reachability for the binding bracket; a positive result would warrant caution, a null result would warrant caveat that the sample may be too small.
- At single-city level (e.g., Pompeii collegia or Ostia collegia, both ≤ a few hundred inscriptions), confirmatory deviation-detection is **out of scope**. The series remains valuable for descriptive shape comparison — "Ostia's collegia inscriptions peak in the late 2nd century, consistent with the textual narrative of guild-formalisation under the Antonines" — but not for formal temporal-deviation testing.

The point of this worked example is not the specific collegia result (which would require running the analysis), but the *prior calibration*: the researcher knows, before any data analysis, what claims the inscription series can credibly support. This is a discipline the radiocarbon-SPD literature has only relatively recently adopted (see Carleton & Groucutt 2021 in *The Holocene*; Crema 2022 in *Journal of Archaeological Method and Theory*); inscription-based dates-as-data work is at the same crossroads. We are committing to the discipline.

## What this is *not*

This reachability guide does not exhaustively characterise every possible analysis. It addresses one specific test (the preregistered permutation-envelope deviation-detection) under one set of null models (exponential and piecewise-linear) and three effect-bracket families. Future methodological extensions could broaden the bracket grid (finer effect-size resolution; longer or shorter durations) or implement subset-specific reachability profiles using each subset's own aoristic-width distribution. These are listed in the project's continuity backlog (Tier 2 and Tier 3 extensions); they would not change the qualitative shape of the guide but would refine it.

The guide also does not characterise *Bayesian-aoristic* methods (e.g., Crema 2025's `baorista`), which use categorically different inferential machinery and have their own — possibly more permissive — reachability profiles. A parallel reachability analysis under Bayesian methodology would be a valuable complement.

---

**Note for paper integration**: this fragment is ~ 1,200 words. The natural location is §3 immediately after the Phase 1 description, or as a §6 limitation/discussion subsection. The figure should be a full-page or half-page width inclusion. The collegia worked example can be retained, replaced with a different subset (e.g., military diplomas), or moved to a supplementary table.
