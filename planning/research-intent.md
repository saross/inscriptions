---
priority: 1
scope: in-stream
title: "Research Intent — Paper A: Latin Inscription SPA with Mixture Correction"
audience: "Adela (co-author), methodological reviewers, future CC instances, Shawn after any break"
status: draft 2026-04-23 — precedes OSF preregistration
---

# Research Intent — Latin inscription SPA paper

## Purpose in one sentence

This paper asks what fraction of the temporal and spatial variation in Latin inscription production during the Roman Empire (50 BC – AD 350) is accounted for by urban population dynamics, using summed probability analysis (SPA) with a novel deconvolution-mixture correction for editorial-convention artefacts.

## Theoretical frame — inscriptions as a proxy for social complexity

In the processual-archaeology tradition, Latin inscription production is a signature of Roman social complexity — a multi-factor construct. We decompose complexity as:

1. **Population** — more people → more inscriptions.
2. **Economic prosperity** — wealthier populations → more inscriptions per capita.
3. **Social differentiation / status hierarchies** — more differentiation → more status-claiming inscriptions per capita.
4. **Cultural translator — the "epigraphic habit"** — the cultural preference for making inscriptions. **Necessary but not sufficient**: gates whether dimensions 1–3 translate into inscription production.
5. **Ideological** — religious devotion, political discourse.
6. **Residual / unmodelled.**

These dimensions drive inscription counts multiplicatively. With inscription counts as the sole observable and minimal external covariates, the dimensions are **empirically unidentifiable from each other.** This is the load-bearing scope constraint for this paper: we address dimension 1 directly (via Hanson 2016 `urban_context_pop_est` pre-joined to LIRE v3.0) and leave the remaining dimensions as theoretically present but empirically entangled.

Prior quantitative engagement with individual dimensions has been sparse. MacMullen (1982) and Meyer (1990) established the rise-and-fall pattern of the epigraphic habit qualitatively. Hanson (2016) operationalised urban population for the Roman Empire. Glomb, Kaše and Heřmánková (2022) applied probabilistic dating with a cultural-transmission model to Asclepius-cult inscriptions. No published work has applied radiocarbon-SPD best-practice methodology (Crema & Bevan 2021; Crema 2022) to quantitatively disaggregate any one complexity dimension at the empire scale.

## Primary hypotheses (narrow, testable)

**H1 — Methodological readiness (sample-size thresholds).** LIRE v3.0 contains sufficient inscription density at province and urban-area levels to support permutation-envelope SPA signal detection at effect sizes relevant to Roman-era demographic events (Antonine Plague, 3rd-century dislocation). Minimum sample thresholds per subset level to be determined by simulation and preregistered.

**H2 — Editorial-convention correction (mixture-model validation).** A mixture model with explicit editorial-convention spike function recovers artefact mass consistent with baseline profiling (observed/expected ratios 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350; Westfall-Young adjusted *p* ≈ 0; see `runs/2026-04-23-descriptive-stats/`). Mixture-corrected SPAs converge under threshold robustness (`date_range` ≤ 25 / 50 / 100 / 200 / 300 years) and agree with stratified-by-convention-class SPAs (appendix cross-check).

**H3 — Population signal.** Mixture-corrected SPA values at urban-area and province level correlate with Hanson (2016) urban population estimates at spatial/temporal resolutions to be preregistered. Three related quantitative results appear in the paper:

- **H3a — variance-explained.** R² (or analogue) with bootstrap confidence intervals at urban-area and province scales. Primary quantitative substantive result.
- **H3b — deviation-detection.** Where the mixture-corrected SPA departs from a fitted null; effect-size targets per Decision 5 (50 % over ≥ 50 y; doubling over ≥ 25 y; 20 % over ≥ 25 y; Antonine-anchored). Complements H3a by answering a different question.
- **H3c — urban-area residuals.** Cities that systematically over- or under-produce inscriptions relative to Hanson-predicted counts, mapped and tabulated. Outliers are interpretable as entry-points for the other complexity dimensions (economy, differentiation, translator, ideology) in follow-up work. Extends Hanson (2021) §7.5–7.6 residual analysis to mixture-corrected data.

## What this paper claims

- **Primary contribution: methodological.** First application of SPD-permutation-envelope machinery, adapted for calendar-date aoristic data, with novel deconvolution-mixture correction for editorial-convention artefacts, to a large Latin inscription corpus.
- **Illustrative substantive findings:**
  - **Population-variance decomposition** — a quantitative estimate of the population dimension's footprint on inscription temporal-spatial variation, with uncertainty bounds. Per consultations with field epigraphers, this is publishable as a standalone contribution.
  - **Urban-area residual analysis** — cities that systematically over- or under-produce inscriptions relative to Hanson-predicted counts, mapped and tabulated; outliers are interpretable as entry-points for the other complexity dimensions in follow-up work. Extends Hanson (2021) §7.5–7.6.
- **Everything else is exploratory / discussion-section.**

## What this paper does not claim

- **Does not disaggregate the five-plus complexity dimensions.** Empirical identifiability requires external covariates currently in-hand for dimension 1 only.
- **Does not resolve the epigraphic-habit-as-translator problem.** The mixture correction addresses one specific artefact (editorial-convention spikes at century midpoints and other conventional dates); the time- and space-varying cultural translator remains unmodelled.
- **Does not establish causal relationships.** Correlation with uncertainty bounds is the endpoint.
- **Does not cover the full Roman chronological range.** LIRE v3.0's envelope (50 BC – AD 350) is the scope; LIST-provided Late-Antique material is deferred.

## Why this matters

- **For epigraphy.** Quantifying the population–inscription relationship with uncertainty bounds is a standalone contribution. The qualitative claim has held for 40+ years without quantification.
- **For archaeological methodology.** Demonstrates that SPD-permutation-envelope machinery transfers from radiocarbon to calendar-date aoristic data, opening inscriptions as a population-variance proxy for periods and regions where radiocarbon evidence is sparse — notably Roman-era urban contexts.
- **For Roman history.** Quantitative engagement with long-running debates (3rd-century decline, Antonine Plague demographic impact, the rise and fall of the epigraphic habit) — not resolving them, but providing tools and first-order results against which to calibrate.

## Scope commitment

Single combined paper targeting JAMT (methods-heavy) or JAS (balanced), per Decision 7 default. The narrow testable claim (population-variance decomposition) is compact enough that the methodology content can travel with the result without triggering the 3,000–4,000-word methods threshold that would force a methods/results split (FS-0). Reconfirm at Week-1 checkpoint (Sunday 2026-05-03).

## Future-work trajectory — disaggregating the complexity stack

This paper addresses dimension 1 (population). The programme continues by disaggregating additional dimensions one at a time, adopting existing operationalisations rather than building proxies from scratch:

- **FS-A: Economic differentiation via job-title frequency.** Count the diversity of economic / occupational titles (collegia, craft specialisations, merchants, officials) per inscription or per urban area as a proxy for economic differentiation. Existing operationalisations in the epigraphic and socio-economic literature to be surveyed. Plausibly applicable to the same corpus without new fieldwork.
- **FS-B: Social differentiation via prosopographic rank structure.** Senatorial, equestrian, decurion, freedman, slave distributions over time and space — existing prosopographic resources (PIR, EDR) provide the operationalisation.
- **FS-C: Ideology via inscription-category distribution.** Votive / funerary / imperial / public distributions as a proxy for the ideological mix. LIRE category fields to be surveyed.
- **FS-D: Cultural translator via mixture α.** The `α` parameter from the deconvolution mixture is itself interpretable as a proxy for epigraphic-habit intensity — regions and periods with α → 1 rely heavily on conventional dating, which is itself a signal about inscription production practices. Novel; would require its own methodological paper.
- **FS-E: Aeneas-partition follow-up** (see `planning/future-studies.md` FS-1). Uses Aeneas text-signal variance to partition LIRE and cross-check whether main-paper signal survives the editorially-anchored subset.
- **FS-F: Full-range multi-factor model.** Three-to-five-year horizon: joint modelling of all dimensions with identifiability achieved via external covariates for each. The current paper is stepping-stone one.
- **FS-G: Production-cost differential via ceramic vs stone inscriptions.** The cost of producing a stone inscription is substantially higher than a ceramic one; the ratio of ceramic to stone inscription production across time and space is a proxy for **economic accessibility of the epigraphic habit** — how far down the socio-economic ladder the cultural translator reaches. Speaks to dimensions 2 (economic prosperity / accessibility) and 4 (cultural translator range) simultaneously. Shawn's 2024 intuition: "what can we learn from the difference in production costs?" (archived notebook to-do; resurrected 2026-04-23).

## Relationship to Decision 7

Decision 7 fixes the methodology architecture: deconvolution-mixture (primary) + thresholded SPAs (body robustness) + stratified-by-convention-class SPAs (appendix cross-check) + baorista Bayesian comparison (appendix). This research-intent document specifies **what question the methodology is answering** and **what claims the paper makes about the world**. Decision 7 is the *how*; this document is the *what* and *why*.

## Open questions for co-authors and resolution before preregistration

1. **Conference venue and deadline** — still TBC per `planning/backlog-2026-04-22.md` §7. Determines final scope and abstract submission timing.
2. **Effect-size targets adequacy** — Decision 5 specifies three deviation-detection brackets plus Antonine-anchored; these were framed for H1 (methodological readiness) and H3b (deviation detection). Confirm they are also appropriate anchors for the variance-explained framing in H3a, or whether a separate power-analysis specification is needed.
3. **Scaling-law confound** — If inscription production scales super-linearly with urban population (per the urban-scaling literature, Ortman and colleagues in other archaeological contexts), the H3 variance-explained result needs to be computed on the scaling residuals rather than raw counts. Preregistration to specify which target quantity (raw correlation vs scaling-controlled correlation) is primary. This is a live critical-friend flag raised at intent-drafting time, not yet resolved.
4. **Cultural-translator confound on the Hanson correlation** — bigger cities may produce inscriptions at disproportionate rates not because of population alone but because of scale-dependent cultural translation. If so, the H3 correlation partly tracks the translator, not population itself. Preregistration to acknowledge this confound and specify whether any sensitivity analysis addresses it.

## Provenance

Drafted 2026-04-23 at Shawn's request, as precondition for the OSF preregistration of the `min-thresholds → mixture validation → population correlation` programme. Multi-factor theoretical frame articulated by Shawn; identifiability-scope reasoning, future-work decomposition, and scaling-law confound flag contributed by main-thread Claude in critical-friend register. Subject to Shawn's edits before commit. See `planning/ai-contributions.md` for the standing log of substantive AI intellectual contributions.
