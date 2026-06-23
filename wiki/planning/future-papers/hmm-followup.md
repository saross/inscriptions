---
title: "HMM follow-up paper — stub"
status: placeholder; substantive work deferred until the current epigraphic-SPA paper is closer to draft
audience: "Martin Eftimoski (collaborator); Shawn (PI); future-CC continuing"
date-created: 2026-05-26
related-artefacts:
  - wiki/continuity.md §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)"
  - runs/2026-05-26-letter-count-probe/REPORT.md
  - archive/specs/h2.1-stage-3-implementation-plan-2026-05-25.md
---

# Hidden-Markov-model follow-up paper — stub

This directory is a one-page scaffold for a second-paper follow-on to the current epigraphic-SPA / Hanson-scaling paper. **No substantive work is in scope here yet.** The trigger for moving from stub to active work is "current paper is close to draft" — likely 2026-Q3 if the present timeline holds.

## What Martin proposed (2026-05-25 consultation)

Martin Eftimoski's interest in the inscriptions project consolidated around a hidden-Markov-model formulation. His framing, paraphrased from the consultation:

> *Hidden Markov model: I've observed x inscriptions in this century. I am not observing the true human population. We know the general structural shape of population (rising versus falling). When did the structural break from rising to falling occur? Similar for provinces or cities. What is the most likely population sequence to produce the set of inscriptions we observe? Assumption about the population structural shape. You can build a distribution that you think is appropriate at each level.*

The latent variable is **human population trajectory** at empire / province / city levels. The observation is the **epigraphic record**. The model's job is to reconstruct the population trajectory most consistent with the observed inscription / letter record, under structural-break priors (rising → falling) that match cross-empire demographic history.

## Two-measure observation channel (post-2026-05-26 reframe)

The current paper's two-measure framework (Obs 58, commit `dd326dc`; REPORT at `runs/2026-05-26-letter-count-probe/REPORT.md`) gives the HMM paper a richer observation space:

- **Channel 1**: inscription-count time series (acts).
- **Channel 2**: letter-mass time series (content).
- **Channel 3**: the delta between channels 1 and 2 at each time bin — the "content-residual" that operationalises the acts-vs-content delta.

The HMM can take channel 1 alone, channel 2 alone, or both jointly. The richest formulation jointly models the two channels with shared latent population but distinct emission distributions:

- Population → inscription count via the act-side emission (sub-linear scaling with β_acts ≈ 0.57 per the 2026-05-26 probe).
- Population → letter mass via the content-side emission (sub-linear scaling with β_content ≈ 0.51 per the 2026-05-26 probe).
- The gap (β_acts − β_content) is the content-residual signal.

## Pre-conditions before substantive HMM work begins

The HMM paper is gated on the current paper reaching a stable draft. Specifically:

1. Stage 3 (empirical-Bayes mixture model) complete under both units per `runs/2026-05-26-recovery-grid-two-unit/spec.md` outcome branching.
2. Phase 2 / 3 substantive analyses (H2 / H3a / H3b / H3c / §5) complete.
3. Current paper's first full draft circulated to co-authors for review.

Until those conditions hold, the HMM track stays in this stub.

## Light scaffolding to do *now* (so the track is ready when triggered)

- [x] **2026-05-26**: this stub created.
- [ ] **Pre-trigger**: invite Martin to the GitHub repo at `https://github.com/saross/inscriptions` so he can read the codebase asynchronously. Martin is a Claude Code power user; he'll run his own analyses when ready.
- [ ] **Pre-trigger**: a short prior-art scan on HMM / state-space / latent-population models applied to historical demographic data. Likely candidates from the 2026-05-19 HMM-aoristic prior-art scout at `archive/scouts/prior-art-scout-2026-05-19-hmm-aoristic.md` — that scout confirmed `baorista` (Crema 2025) as the natural emission-layer foundation, and identified that the inscription / latent-population combination is genuinely novel.
- [ ] **Pre-trigger**: a single-page methodological sketch that Martin can read in 5 minutes — emission distribution candidates (Negative Binomial for inscription counts; Negative Binomial again for letter mass with higher α dispersion; jointly with shared latent), state-space prior structures (rising-then-falling with structural-break detection), and what a result would look like.

## Authority and amendment

This stub is methodological development and pre-paper exploration. **No OSF amendment needed for any work happening in this directory** (memory `2026-05-26-40ce5927fddc`); the current paper's prereg covers only the SPA + scaling work, not the follow-on HMM track. A separate prereg for the HMM paper will be lodged when that track moves from stub to active.

## Cross-references

- `wiki/continuity.md` §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)" — the consultation that triggered this stub.
- `archive/scouts/prior-art-scout-2026-05-19-hmm-aoristic.md` — earlier HMM prior-art scout (predates Martin's letter-count nudge).
- `runs/2026-05-26-letter-count-probe/REPORT.md` — the probe whose results define the two-measure observation channel.
- Memory `2026-05-26-214ce5ca1491` — Martin Eftimoski profile (statistician collaborator; comp-sci PhD; econometric training; weaker in Bayesian statistics).

---

*This stub is intentionally minimal. The cost of premature design here exceeds the benefit; the substantive work waits for the trigger condition.*
