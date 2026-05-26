---
title: "Letter-count probe — REPORT"
audience: "Shawn (PI); session-handoff readers; future Stage 3 design"
status: final 2026-05-26 (all 6 blocks complete; verdict locked)
date: 2026-05-26
related-artefacts:
  - runs/2026-05-26-letter-count-probe/spec.md   (the binding spec)
  - runs/2026-05-26-letter-count-probe/RUN-LOG-06.md   (sapphire Mundlak log)
  - docs/notes/reflections/working-notes.md Obs 58 (commit dd326dc) — "acts vs content" reframe
  - docs/notes/reflections/working-notes.md Obs 59 (commit de8fa8f) — Mundlak f_within shift
  - docs/notes/reflections/continuity.md §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)"
  - runs/2026-05-26-recovery-grid-two-unit/spec.md   (downstream Stage 3 gate)
---

# Letter-count probe — REPORT

## Headline

Three of three verdict flags evaluated. **Two of three flags MATERIAL**: the unit-of-analysis swap from inscription-count to letter-mass measurably changes the Hanson scaling exponent (β shifts down 0.566 → 0.515 with non-overlapping bootstrap CIs) and the within-province variance partition (f_within shifts up from 29.94 % to 39.83 %, +9.89 pp).

The probe's spec was written with a binary verdict rule ("any flag tripping MATERIAL → letter-count becomes the headline unit"). That rule has been **superseded mid-probe** by Shawn's "acts vs content" reframe (Obs 58, commit `dd326dc`): inscription-count and letter-mass are complementary measures of partially-different constructs, not rival operationalisations of the same construct. **The probe's final verdict is therefore "adopt both as first-class measures; the delta between them is itself a research object."**

The 2026-05-26 recovery-grid two-unit re-simulation (`runs/2026-05-26-recovery-grid-two-unit/spec.md`) is the downstream Stage 3 launch gate that validates identifiability under both units.

## Verdict table — all three flags

| Flag | Statistic | Threshold | Inscription (baseline) | Letter (conservative) | Letter (interpretive) | Verdict |
|------|-----------|-----------|------------------------|----------------------|----------------------|---------|
| **1** | Empire SPA shape — bin-by-bin Pearson r vs inscription-mass | r > 0.95 NO-CHANGE; r < 0.85 MATERIAL | baseline | r = 0.904 | r = 0.883 | **MODEST** |
| **2** | Hanson β — frequentist NBR, 1,000-rep row-resample bootstrap CI | CIs overlap = NO-CHANGE; no overlap = MATERIAL | 0.566 [0.543, 0.574] | 0.515 [0.463, 0.542] | 0.512 [0.468, 0.536] | **MATERIAL** |
| **3** | f_within — Bayesian Mundlak NBR, 95 % credible interval | shift < 2 pp NO-CHANGE; > 5 pp MATERIAL | 29.94 % [23.70, 36.63] | 39.83 % [32.04, 48.17] | 39.83 % [31.97, 48.30] | **MATERIAL** (+9.89 pp) |

The two text-field choices (conservative vs interpretive cleaning) give essentially identical results — empire SPA Pearson r = 0.994 between them (Block 2); Hanson β within 0.003 (Block 4); f_within median identical to 4 decimal places (Block 6). **Conservative is the locked choice for Stage 3** (cleaner default — only counts preserved letters + expanded abbreviations; no scholarly-supply judgement).

## Block-by-block summary

### Block 1 — letter-count computation (`code/01-compute-letter-counts.py`)

Computed `letter_count_conservative` and `letter_count_interpretive` on the 180,609-row filtered LIRE corpus (already filtered to 50 BC – AD 350 envelope per the prereg). Letter = single Latin or Greek alphabetic character (Unicode `[A-Za-zÀ-ÿΑ-Ωα-ω]`); spaces, punctuation, brackets, digits excluded by construction.

| Field | n | %-zero | Median | Q25 | Q75 | Mean | Max | Total mass |
|-------|--:|------:|-------:|----:|----:|-----:|----:|----------:|
| `letter_count_conservative` | 180,609 | 2.21 % | 25 | 10 | 52 | 45.4 | 35,537 | 8,208,304 |
| `letter_count_interpretive` | 180,609 | 2.18 % | 42 | 16 | 82 | 70.8 | 46,926 | 12,780,529 |

Monotonicity check: 375 rows (0.21 %) have interpretive < conservative — well under the 5 % warn threshold; editorial irregularities in LIRE's cleaning pipeline (e.g., `clean_text_conservative` retaining diacritics or vowel-marks the interpretive cleaning strips). Documented; not acted on.

Fat right tail: mean ≫ median (45 vs 25; 71 vs 42). A handful of monumental inscriptions (Res Gestae class — thousands of letters each) dominate the upper tail. Implication: empire SPA averages this out (high N); province / city panels will swing on a few large dedications.

### Block 2 — empire SPA shape comparison (`code/02-empire-spa-letter.py`)

Three SPAs computed under the same 5-year-bin uniform-aoristic deposit; each row contributes weight × overlap fraction to bins it touches; weight = 1 (inscription-mass) or `letter_count_*` (letter-mass).

Pairwise Pearson r (bin-by-bin):

| Pair | Pearson r | Spearman r |
|------|----------:|-----------:|
| inscription × letter_conservative | 0.904 | 0.863 |
| inscription × letter_interpretive | 0.883 | 0.850 |
| letter_conservative × letter_interpretive | 0.994 | 0.989 |

The two letter variants are essentially the same series; the choice of text-field cleaning is methodologically inert for shape purposes.

**Flag 1: MODEST.** The unit-swap measurably reshapes the empire-level temporal distribution (~ 18–22 % of variance is not shared between the two units), but no variant crosses the MATERIAL threshold of r < 0.85.

Absolute-mass total ratios: letter-mass conservative is ~ 48× inscription-mass; interpretive ~ 76×. These match the corpus-mean letters-per-inscription (45.4 conservative; 70.8 interpretive), confirming the aoristic deposit is integrating the per-row weights correctly.

### Block 3 — province + city SPAs + rank shuffles (`code/03-province-city-spas-letter.py`)

Same three weightings applied at province and city granularity. The **rank-shuffle pattern** is a substantive epigraphic-cultural finding in its own right.

**Top 8 provinces** (ranked by inscription count, Rome-excluded; deltas show rank change under letter-mass-conservative):

| Province | Inscr. count | Rank by inscr. | Letter total (cons) | Rank by letter | Δ rank |
|----------|------------:|---------------:|--------------------:|---------------:|------:|
| Latium et Campania / Regio I | 18,496 | 1 | 970,203 | 1 | 0 |
| Dalmatia | 7,088 | 2 | 270,492 | 2 | 0 |
| Hispania citerior | 6,312 | 3 | 188,143 | 7 | **+4** |
| Germania superior | 5,874 | 4 | 162,310 | 10 | **+6** |
| Venetia et Histria / Regio X | 5,872 | 5 | 267,009 | 3 | **−2** |
| Dacia | 4,869 | 6 | 162,725 | 9 | +3 |
| Britannia | 4,646 | 7 | 118,844 | 19 | **+12** |
| Pannonia superior | 4,460 | 8 | 199,595 | 5 | **−3** |

**Top 8 cities** (ranked by inscription count, Rome-excluded, Hanson-matched):

| City | Inscr. count | Rank by inscr. | Letter total (cons) | Rank by letter | Δ rank |
|------|------------:|---------------:|--------------------:|---------------:|------:|
| Pompeii | 4,508 | 1 | 116,946 | 3 | +2 |
| Salona | 3,465 | 2 | 132,089 | 2 | 0 |
| Ostia | 2,644 | 3 | 197,971 | 1 | **−2** |
| Mogontiacum | 2,398 | 4 | 56,840 | 6 | +2 |
| Aquileia | 2,034 | 5 | 82,661 | 5 | 0 |
| Puteoli | 1,780 | 6 | 114,283 | 4 | **−2** |
| Carnuntum (1) | 1,641 | 7 | 51,185 | 8 | +1 |
| Cirta | 1,020 | 8 | 32,039 | 15 | **+7** |

**Pattern.** Frontier-military provinces drop sharply under letter-mass (Britannia, Germania superior, Hispania citerior). Italian / Adriatic provinces with monumental funerary traditions rise (Venetia et Histria, Pannonia superior). Among cities: **Ostia rises to #1** under letter-mass (commercial / harbour administration inscriptions are letter-heavy — mensores lists, collegial dedications, decrees); Pompeii drops to #3 (graffiti effect: huge N of two-word texts); Cirta drops 7 ranks (military / brief epitaph practice).

**Substantive read.** Inscription-count weights frequency of inscribing; letter-mass weights quantity of communication. These are different cultural-archaeological constructs. Military / frontier epigraphy is high-frequency and low-content; Italian-monumental and Ostian-commercial epigraphy is lower-frequency and high-content per act. The rank-shuffle is not noise — it's a real cultural pattern that the inscription-count framing was hiding.

### Block 4 — Hanson NBR (`code/04-hanson-nbr-letter.py`)

Frequentist Negative-Binomial regression of city-level response on `log(Hanson population)`; 1,000-replicate row-resample bootstrap CI on β. 1,044 Hanson cities Rome-excluded; date-window filter matches the prereg H3a specification (Decision 22).

| Variant | β_pop | SE | Bootstrap 95 % CI | α (dispersion) |
|---------|------:|---:|-------------------|---------------:|
| inscription count | 0.566 | 0.043 | [0.543, 0.574] | 2.15 |
| letter-mass conservative | 0.515 | 0.040 | [0.463, 0.542] | 2.04 |
| letter-mass interpretive | 0.512 | 0.040 | [0.468, 0.536] | 2.01 |

**Flag 2: MATERIAL.** Bootstrap CIs do not overlap; β drops ~ 0.05 under letter-mass.

**Comparator context.** Hanson 2021 reports β = 0.672 [0.588, 0.756] (OLS log-log on 554 sites). Carleton et al. 2025 reports β ∈ [0.3, 0.5] across the headline epigraphy spec, with an epigraphy-no-zeros variant at β ~ 0.68. Our inscription-count β = 0.566 overshoots Carleton's headline range; **letter-mass β ≈ 0.51 sits at the upper edge of Carleton's range** — empirically closer to a published cross-empire epigraphic-density-scaling comparator. Direction: letter-mass produces a *less steep* scaling exponent, consistent with the substantive read that information-content scales even more sub-linearly with population than acts do.

**Caveat.** Bootstrap is row-resample (perturbs within-city sampling variability; treats Hanson population estimates as fixed). A city-level bootstrap would give wider CIs (deferred robustness check; carried over from 2026-05-21 talk-prep `03-hanson-nbr-bootstrap.py` documentation).

### Block 5 — frequentist Mundlak variance partition (`code/05-within-province-variance-partition.py`)

Within-between decomposition under the three response variants. Frequentist NBR with `log_pop_within` (city log-pop minus province mean) and `log_pop_prov_mean` as predictors; no province random intercepts.

**This block's f_within is NOT directly comparable to the talk-prep Bayesian Mundlak's ~ 30 % punchline** — the frequentist version's denominator is only the population-attributable variance (no random-effects component). f_within values are ~ 95 % across all three variants; the cross-variant shift is what's interpretable, not the absolute magnitude.

| Variant | β_within | β_between | f_within (frequentist) | shift from baseline |
|---------|---------:|----------:|----------------------:|--------------------:|
| inscription | +0.666 | −0.310 | 95.54 % [93.55, 97.74] | baseline |
| letter (cons) | +0.573 | −0.190 | 97.67 % [96.10, 99.83] | +2.13 pp |
| letter (intr) | +0.577 | −0.199 | 97.50 % [95.68, 99.68] | +1.97 pp |

**Frequentist Flag 3 reading: borderline MODEST.** But the metric was the wrong one for the verdict — Block 6 is the directly-comparable Bayesian re-fit.

### Block 6 — Bayesian Mundlak NBR (sapphire; `code/06-h3a-bayesian-mundlak-letter.py`; `RUN-LOG-06.md`)

Full prereg-spec Bayesian Mundlak NBR with province random intercepts, fit per variant. Three fits ran on sapphire 2026-05-26, total wall-clock 4.3 minutes. All three PASSed the prereg convergence gates: max R-hat = 1.0000; min ESS_bulk = 1,041; zero divergences.

| Variant | f_within median | 95 % CI | P(>0.10) | P(>0.20) | β_within | β_between |
|---------|----------------:|---------|---------:|---------:|---------:|----------:|
| inscription | **29.94 %** | [23.70, 36.63] | 1.00 | 1.00 | +0.587 | −0.248 |
| letter (cons) | **39.83 %** | [32.04, 48.17] | 1.00 | 1.00 | +0.559 | −0.158 |
| letter (intr) | **39.83 %** | [31.97, 48.30] | 1.00 | 1.00 | +0.559 | −0.170 |

**Inscription-count fit reproduces the 2026-05-21 talk-prep slide-6 punchline (29.95 %, seed 20260521) to two decimals on a fresh seed (20260526)** — sanity check on model + data + sampler consistency.

**Flag 3: MATERIAL** under the spec's threshold (> 5 pp shift). The under-letter-mass f_within is +9.89 pp higher than under inscription-mass.

**Mechanism.** β_within is roughly stable across units (0.587 → 0.559, ~ 5 % drop); β_between shrinks substantially toward zero (−0.248 → −0.158, ~ 36 % centring). The total variance denominator shrinks faster than the within-variance numerator, pushing f_within up.

**Substantive interpretation.** Letter-mass partially strips out provincial-level "epigraphic habit" noise — the province-level cultural variation (language, frontier-military style, provincial elite practice) that drives inscription-ACT counts more than information-CONTENT counts. **Within a province, city population predicts letter production more cleanly than it predicts inscription frequency.** The ACT of inscribing varies by province for habit reasons; the AMOUNT inscribed per inscription varies in a way that's better predicted by city-level population.

## Substantive findings (paper-worthy)

1. **"Acts vs content" as a methodological frame.** Inscription-count and letter-mass are complementary measures of partially-different constructs: frequency-of-inscribing vs quantity-of-communication. The paper's methodology section will frame the two-measure decomposition as a structural contribution.

2. **Province / city rank shuffles** (Block 3). The unit-swap reshuffles which provinces and cities are most prominent — Britannia drops 12 ranks, Ostia rises to #1, Cirta drops 7 ranks. This is a substantive epigraphic-cultural pattern: military-frontier epigraphy is high-frequency / low-content, while Italian-monumental and Ostian-commercial epigraphy is lower-frequency / high-content per act. **The rank-shuffle table is a paper-figure candidate.**

3. **Scaling exponent letter-vs-act gap** (Block 4). Letter-mass produces β ≈ 0.51 — sub-linear and closer to Carleton et al. 2025's published epigraphy-density range. Inscription-count's β ≈ 0.57 overshoots Carleton. The direction of the gap is consistent with the "acts vs content" frame: information output scales *more* sub-linearly with population than acts do.

4. **Within-province scaling stronger under letter-mass** (Block 6). f_within rises from 30 % to 40 % (+9.89 pp; nearly a third increase). Substantively: provincial epigraphic-habit variation contaminates inscription-count more than letter-mass; cleanly-predicted-by-population content production stands out more sharply under the letter unit. **Publishable in its own right** as evidence that "epigraphic habit" and "epigraphic production" are partially-independent constructs.

5. **Conservative vs interpretive cleaning is methodologically inert.** Both letter-mass variants produce essentially identical results across all six blocks. **Stage 3 uses conservative letter-mass** as the locked default.

## Implications for Stage 3 (the empirical-Bayes mixture model)

Per the spec at `planning/h2.1-stage-3-implementation-plan-2026-05-25.md`, with the two-measure framework folded in:

1. **Parallel fits under both units.** Stage 3 fits the mixture model twice — once under inscription-mass, once under letter-mass-conservative. The mixture's structural spec (p_conv × α + p_gen × (1−α)) is unit-independent; only the per-row weight in aoristic deposit differs.

2. **Per-bin sigma_prior re-derived from Stage 2 under letter-mass.** The bootstrap-derived sigma_prior (median 0.044 under inscription-mass per Stage 2 work `8e1897b`) needs re-computation under letter-mass weighting before Stage 3 launches the letter-mass fit.

3. **`pilot_proxy` tier vector re-anchored** to letter-mass endpoint frequencies for the letter-mass grid. A short script run during Stage 3 prep produces the letter-mass `pilot-proxy.json`.

4. **Mixing weight α reinterpretation under letter-mass.** Under inscription-count, α is "fraction of inscriptions whose temporal distribution is editorially-template-driven." Under letter-mass, it becomes "fraction of letter mass whose temporal distribution is editorially-template-driven." Substantively similar; technically distinct; report both.

5. **Three Stage 3 outputs**, not one: p_gen + α posteriors under inscription-mass, same under letter-mass, and the **delta** between the two corrected SPAs at each bin (the new derived quantity that operationalises the "acts vs content delta" Obs 58 / 59 frame).

## Limitations and caveats

1. **Bootstrap CI on Block-4 Hanson β** is row-resample only (treats Hanson populations as fixed). A city-level bootstrap would give wider intervals; the gap between inscription-count and letter-mass β estimates is ~ 1.2 model SEs and would likely remain material under a city-level bootstrap, but not certainly.

2. **Block-5 frequentist f_within** is NOT comparable to talk-prep / Block-6 Bayesian f_within because the denominators differ (no province random-effects component). Reported as cross-variant shift only; the spec's flag-3 threshold was re-evaluated under Block 6.

3. **Letter-count distribution is heavy-tailed and uncapped.** A handful of monumental inscriptions (max 35,537 letters under conservative cleaning) dominate their bins. The two-unit recovery grid (`runs/2026-05-26-recovery-grid-two-unit/spec.md`) tests whether this heavy tail affects identifiability; if so, a 99th-percentile-capped sensitivity is available.

4. **OSF amendment status: pending.** The two-measure framework is a post-lodgement methodological change. It needs to be lodged as an OSF amendment before headline confirmatory analyses produce results reported as preregistered. Per memory `2026-05-26-40ce5927fddc`, amendments are batched; this one will go with the post-Martin reframe of D19/D21/D23/D25.

5. **Stage 3 launch is gated** on the two-unit recovery-grid re-simulation passing the binding criterion (≥ 90 % cells pass coverage AND posterior-median Pearson r ≥ 0.95 in ≥ 90 % of cells, per grid). Grid launched 2026-05-26 on sapphire; ~ 60 h wall-clock expected.

## Reproducibility

All scripts callable from project root via `.venv/bin/python runs/2026-05-26-letter-count-probe/code/<script>.py`. Random seeds locked to 20260526 (today's date). Bayesian Mundlak fits used `N_WARMUP = 3000, N_SAMPLE = 2000, N_CHAINS = 4, target_accept = 0.95`. Letter-augmented parquet (`data/lire-filtered-with-letters.parquet`, 60 MB) gitignored; reconstructable deterministically from script 01 + the 2026-05-21 talk-prep filtered LIRE parquet (which is itself reconstructable from `archive/data-2026-04-22/LIRE_v3-0.parquet` via the talk-prep script 01).

## Cross-references

- **Spec**: `runs/2026-05-26-letter-count-probe/spec.md` — the binding spec with verdict thresholds.
- **RUN-LOG**: `runs/2026-05-26-letter-count-probe/RUN-LOG-06.md` — sapphire Bayesian Mundlak fit log.
- **Obs 58** (commit `dd326dc`): "acts vs content" methodological reframe.
- **Obs 59** (commit `de8fa8f`): Mundlak f_within shift; empirical corroboration.
- **Continuity §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)"**: the consultation that introduced letter-count as a nudge.
- **Downstream gate**: `runs/2026-05-26-recovery-grid-two-unit/spec.md` — the two-grid identifiability re-simulation; ~ 60 h sapphire run.
- **Talk-prep reference**: `runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv` — the f_within = 29.95 % punchline reproduced.
- **Comparator**: Carleton et al. 2025 — published cross-empire epigraphic-density-scaling range [0.3, 0.5] that letter-mass β = 0.515 aligns with.

## Definition of done (per spec §10)

- [x] All five script outputs present and inspectable (Block 1–5).
- [x] Block-6 Bayesian Mundlak result added (sapphire run; convergence PASS; results pulled and committed `49957a7`).
- [x] REPORT.md with verdict against all three flags, for both text-field choices.
- [x] Pre-commit critical-friend pass: surfaced caveats around frequentist-vs-Bayesian f_within (Block 5 vs 6); row-resample bootstrap (Block 4); heavy-tail letter-count distribution.
- [x] Single batched commits to git (`f3e5322 → 26ab70e → 507a722 → de8fa8f → 49957a7`); pushed.

Probe closed 2026-05-26.
