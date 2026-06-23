---
title: "Talking points and feedback framing — RAC-TRAC 2026 talk"
date: 2026-05-20 (overnight)
audience: "Adela (presenter) + Shawn (advisor on talk content)"
purpose: "Anticipate audience objections, frame the talk's claims at the right level of certainty, prepare feedback prompts."
---

# Talking points and feedback framing

## Why this matters (the audience-frame strategy)

RAC-TRAC audiences are **Roman archaeologists, classicists, ancient historians, theoretical archaeologists, and epigraphers**. Their *prior* on this kind of work is that **inscription counts reflect cultural enthusiasm for inscribing** — Ramsay MacMullen's "epigraphic habit" framing (1982), reinforced by Hanson (2021) and others. That prior is well-earned: the field has decades of evidence that epigraphic production is culturally patterned (Greek vs Latin habits; military vs civilian sub-corpora; religious phases; commemorative practices) in ways that don't reduce neatly to demography.

**Our talk does not refute this prior.** Our talk argues for a more nuanced position:

> *Inscription counts reflect cultural epigraphic practice* and *some* underlying demographic structure. Once we account for editorial distortion in the dating evidence and isolate the within-province population effect, a measurable population signal remains. We aren't claiming inscriptions are demographic data; we're claiming they're partially demographic — enough to be worth modelling carefully.

This is the *empirical wedge* we want to drive into the field's prior, and it's important to land it with the right tone:

- **Not** "we've solved this" — the audience will resist
- **Not** "habit is wrong" — straw-manning the prior
- **Yes** "habit is real and we account for it; population is also a contributor; here's how we separate them; this is preregistered"

## Anticipated objections and prepared responses

### Objection 1: "But inscription counts mostly reflect the epigraphic habit, not population"

**Response framing**: "Agreed — that's why we use a within-province specification. The Mundlak / within-between decomposition separates the *between-province* variation (which is heavily confounded with cultural-administrative differences in epigraphic practice — the habit) from the *within-province* variation (which is much harder to attribute purely to habit — within a province, why would Pompeii inscribe more than Capua just because of cultural preference?). The preregistered confirmatory test attaches only to the within-province component. The between-province component is reported but flagged as confounded — exactly the point the habit critique makes."

**Backup point**: Hanson 2021 himself reports residual structure — provincial capitals over-produce inscriptions relative to scaling expectation, even controlling for population. That residual structure is *interesting*; it has to come from somewhere, and "habit alone" doesn't predict that specific structural pattern.

### Objection 2: "Population estimates from Hanson 2016 are very uncertain"

**Response framing**: "Yes — and we preregistered a measurement-error sensitivity on exactly this. The H3a primary uses Hanson's point estimates; the preregistered sensitivity refits with `log_pop_c ~ Normal(log_pop_observed_c, σ_pop)` for σ_pop ∈ {0.1, 0.2, 0.3}. If the within-province variance fraction shifts by more than 50 % of its CI width under any σ_pop, that's flagged as a limitation. This is in §5 of the preregistration."

**Backup point**: Hanson's populations are *max theoretical* (urban footprint × density), not realised peaks. We have a tertiary analysis logged in continuity to test max-pop against peak-window inscription counts (5-year and 25-year windows) as a future check on whether the scaling relationship holds when both predictor and response are "peak" measures.

### Objection 3: "Why do you exclude Rome?"

**Response framing**: "Rome contributes 65,435 inscriptions to the filtered corpus — 36 % of the total, or 47 % of the Hanson-catalogued city subset. As a single data point it dominates the scaling regression. We follow Hanson 2021's own exclusion practice (Table 7.3 caption). The exclusion is reported transparently and is NOT tested as a sensitivity in this preregistration — that's a known limitation flagged in §9. Anyone who wants to include Rome can — but they should be aware they're fitting one extreme point."

### Objection 4: "Frequentist NBR isn't your preregistered method, why show it?"

**Response framing**: "This is preliminary, post-lodgement work for this talk specifically. The preregistered analysis is Bayesian within-between NBR with Mundlak centring, plus brms shadow validation. Both attach to the same target estimand — the within-province population-attributable variance fraction — but use different inferential machinery. The frequentist NBR comparison to Hanson 2021's β = 0.672 lets us anchor our methodology against published comparators while the full Bayesian implementation is in progress."

### Objection 5: "How do you handle the editorial-template problem?"

**Response framing**: "The wide-template editorial encoding is real and measurable — slide 2 shows that 54.5 % of `not_before` values end in `01` and 53 % of `not_after` values end in `00`, which is the editorial signature of century-template intervals. We've designed a Bayesian deconvolution-mixture model that decomposes the observed SPA into a convention component (built from the empirically-attested template intervals) and a genuine signal. The model and its validation grid are preregistered. This talk shows the schematic / synthetic recovery demonstration; the full validation runs post-talk."

**Backup point**: H3a (the population scaling) operates on date-window-filtered *counts*, not on the mixture-corrected SPA. The mixture corrects the *temporal* analyses (H2 and H3b deviation-detection). For the cross-sectional H3a regression, the date-window filter is the artefact protection.

### Objection 6: "What about specific subgroups (military / religious / honorific)?"

**Response framing**: "The preregistration includes subset-specific work as both confirmatory (H3b Antonine probe uses an Asclepius-cult subset; H3b Crisis probe uses a Western-Empire provincial subset; H3a operates on Hanson-matched urban cities) and exploratory (stratified-by-class SPA analysis listed in §5). We'd love to hear what subgroups you'd specifically nominate as either natural negative controls (where habit-only should clearly dominate) or natural positive controls (where population should clearly dominate)."

### Objection 7: "Have you accounted for survival bias / publication bias?"

**Response framing**: "Partly — the LIRE corpus aggregates EDH + EDCS coverage, which means we inherit their editorial decisions and known coverage gaps. Hanson 2021's between-province component is flagged in our prereg as 'not separately identifiable from province-level cultural, administrative, and survival-bias variation' — we explicitly DO NOT claim the between-province effect as a clean population signal. Within-province is more defensible because it controls for province-level survival differences (assuming roughly equal survival bias within a province). This is a real limitation we're transparent about."

## Specific feedback prompts (close of talk)

These are the four prompts on slide 7. Adela can adapt these on the day; specifically:

1. **"Does the editorial-template decomposition match your experience with the source dating conventions?"**
   - Domain-expert validation of the convention component
   - We're operating on regularities in the data; want to know if practitioners recognise the same regularities from their own work

2. **"Are there subgroups (inscription type / monument / region / period) where the habit-only critique is clearly dominant — i.e. natural negative controls?"**
   - Asks the audience to nominate test cases where our scaling argument *should* fail
   - If they can't nominate clear negatives, the habit-only critique is at risk of being unfalsifiable

3. **"What independent demographic anchors would you use to validate the 'habit-removed residual' temporal analysis?"**
   - The §5 exploratory work needs independent peak-population dates
   - Audience may know specific published demographic reconstructions we should consult

4. **"Where does provincial-capital over-production come from, in your interpretation? Status display? Administrative density? Both?"**
   - Hanson 2021's residual finding that the H3c(i) confirmatory test replicates
   - We want field interpretation, not just statistical replication

## Tone and pacing notes for Adela

- **Pacing**: 12 min / 7 slides ≈ 100 s per slide. Slides 2, 5, 6 will need slightly more (~ 110–120 s each); slides 1, 3, 4, 7 can run closer to 90 s. Speaker notes embed the budget.
- **Pre-emptive concession**: open slide 1 by *naming* the habit-only critique, not avoiding it. This earns audience trust.
- **Hedge language**: every quantitative result is *preliminary*; every confirmatory test is *forthcoming*; the deck is for *feedback*. This protects against any audience member who treats the talk as final results.
- **Open-science framing**: name the OSF preregistration (with DOI if available) once, on slide 7. Don't over-claim — preregistration is a discipline, not a guarantee of truth.
- **Q&A reserve**: B1–B6 backup slides ready. If a question goes substantive, jump to a backup; if a question goes meta-methodological (e.g., "why preregister?"), have a 30-second answer ready.

## What "good" feedback would look like

After the talk, the kind of input we'd value most:

- Nominations of **specific subcorpora** as negative or positive controls for the scaling argument
- **Independent demographic data** sources we haven't considered (textual evidence, archaeological-survey-derived population estimates, etc.)
- **Critique of the convention-component construction** — does the template-slab dictionary include the right intervals? Are there template conventions we missed?
- **Concerns about the Hanson population estimates** — known issues with specific cities? Known biases by province or type?
- **Methodological pointers** — are there published statistical approaches to similar dating-distortion problems in archaeology / ancient history that we should be citing?

Less valuable but still worth listening for:

- The standard "habit is everything" objection — useful to hear, but doesn't advance the discussion unless framed against the within-between decomposition

What we should explicitly NOT defend hard against in the Q&A:

- **Specific points of statistical method**: we're not statisticians; defer to the preregistration and Martin's consultation pack as the methodological core
- **The "what does this prove?" question**: nothing in the talk is a proof. It's a methodological demonstration plus a preliminary scaling result. Lean on that explicitly.
