---
title: "Adela briefing — RAC-TRAC 2026 talk delivery"
date: 2026-05-21
audience: "Adela Sobotková (delivering the paper Friday 22 May 2026 14:20 Aarhus time, room Preben Hornung)"
author: "Shawn Ross (paper author, in absentia) via overnight talk-prep run"
purpose: "Practical delivery brief: deck contents, headline numbers, anticipated Q&A, backup-slide map, honest-disclosure boundary."
length: "~ 15 min read on the day; print-ready as a single document."
---

# Adela briefing — RAC-TRAC 2026 talk delivery

Thanks Adela. This briefing covers what's in the deck, what's preliminary,
how to handle the most likely Q&A, and what to elide if you run short on
time. Pair with `talking-points-feedback.md` (sibling file) for the longer
prepared-objection notes — this document is the quick-reference.

## 1 · Deck format and files

| Artefact | Path | Purpose |
|---|---|---|
| Primary deck | `planning/conference-talk-rac-trac-2026/slide-outline.html` | Self-contained revealjs HTML (~ 6 MB, all figures embedded as data URIs). Open in any modern browser; press **`s`** to enter speaker view. |
| Paper-document backup | `planning/conference-talk-rac-trac-2026/slide-outline.pdf` | 11-page LaTeX paper-document fallback if the HTML setup fails. Not a slide-format PDF — use the HTML if at all possible. |
| Quarto source | `planning/conference-talk-rac-trac-2026/slide-outline.qmd` | Re-render if last-minute edits are needed: `quarto render slide-outline.qmd --to revealjs` |
| Figures | `planning/conference-talk-rac-trac-2026/figures/` | All five talk figures + the run-mirror in `runs/2026-05-21-talk-prep/outputs/figures/` |

**Recommended setup on the day**: bring the HTML on a USB stick AND email it to
yourself. Test it in the lectern browser before the session starts. If for any
reason the HTML doesn't load, the PDF is a paper-document reading copy.

## 2 · Slide-by-slide cheat sheet

Target: ~ 12 min over 8 slides (added one to the original 7 for the Bayesian
Mundlak result). Average ~ 90 s per slide.

### Slide 1 — Dates-as-data tradition + the puzzle (~ 90 s)
- Open by *naming* the habit-only critique (MacMullen 1982; Hanson 2021). Don't avoid it.
- Frame the talk as a methodological contribution that takes that critique seriously.
- Mention LIRE v3.0: **180,609** inscriptions, 50 BC – AD 350, Latin epigraphy.
- Tone: open, inviting feedback. Not "we've solved this."

### Slide 2 — Editorial distortion has a measurable signature (~ 110 s)
- The empirical SPA shape decomposes cleanly: wide-template plateaus + narrow regnal spikes + BC/AD step.
- Specifics: **54.5 %** of `not_before` end in `01`; **53.0 %** of `not_after` end in `00`. Largest single step in the SPA is **+1,159 at 1 BC / AD 1**.
- Spike-to-plateau ratio at AD 122.5 jumps from 1.61× to **13.83×** when filtered to narrow-precision inscriptions — i.e. the spike is REAL ancient clustering, the plateau is editorial encoding.
- This earns the audience's attention for the methodological argument that follows.

### Slide 3 — Phase 1 reachability (~ 100 s)
- Phase 1 is **complete methodology**, locked at OSF lodgement.
- Take-home: we did the simulation work first to determine where the data has enough power. Cells that don't clear the minimum-N threshold are flagged "unreachable" rather than reported with inflated false-positives.
- Specifics: empire reachable at n = 50,000; provinces and urban areas at n ≈ **1,549** for the binding bracket; **96 H1-reachable cells** total.
- If asked about FP control: ≤ 5 % across all 96 zero-effect cells (range [0.007, 0.049]).
- If asked about the math: forward-fit null in true-date space → synthetic-from-null DGP with empirical aoristic widths → 1,000 iterations × 1,000 MC replicates.

### Slide 4 — Multi-scale SPA shapes (~ 100 s)
- Two figures: top-8 provinces (left) + top-8 cities (right), each scaled to unit peak height.
- The point is empirical, not statistical: at every scale, structure beyond uniform.
- **Validity check**: Pompeii cuts off cleanly at AD 79 (Vesuvius). This is a smoking-gun that the pipeline is doing the right thing.
- Be explicit: these are RAW, not mixture-corrected. The mixture is what we discuss next.

### Slide 5 — Bayesian mixture decomposition (~ 110 s)
- This is the METHODOLOGICAL CORE.
- Model: `y_t ~ Multinomial(N, α · p_conv + (1 − α) · p_gen)`. Convention component built from empirically-attested template intervals (century slabs, half-century slabs, reign-interval slabs). Year-precise inscriptions stay in `p_gen` as real ancient anchors.
- The recovery figure shows: on a SYNTHETIC dataset with known α = 0.50 and known smooth Gaussian shape, the model recovered **α median = 0.477, 95% CI [0.414, 0.541]** (covers truth) and **Pearson r = 1.000** against the true shape. All preregistered validation gates pass (R̂ = 1.0000; ESS ≥ 2,567; Pearson ≥ 0.95 threshold cleared).
- **Honest disclosure**: one synthetic cell, parametric simplification (one tier + Gaussian); the prereg's full validation runs 100 replicates per cell across a multi-axis grid. Full validation runs post-talk.

### Slide 6a — Frequentist scaling comparator (~ 100 s)
- This is the comparator to Hanson 2021 (β = 0.672 [0.588, 0.756]) and Carleton et al. 2025 (β ≈ 0.3 – 0.5; no-zeros ≈ 0.68).
- Our **frequentist NBR β = 0.566, bootstrap 95 % CI [0.543, 0.574]** on **1,044** Hanson-matched cities ex-Rome.
- **OLS log-log β = 0.284 (R² = 0.04)** — dampened by the low-count tail; NBR is the better spec for over-dispersed count data.
- Lead the audience to slide 6b: this is just the comparator; the BINDING analysis is the Bayesian Mundlak on the next slide.

### Slide 6b — How much of the variation is population vs everything else? (~ 130 s — the SUBSTANTIVE PUNCHLINE)
- The within-between (Mundlak) decomposition is the methodological key.
- Each city's `log(pop)` splits into a province-mean component + a within-province deviation. β_within is the coefficient on the deviation — the WITHIN-PROVINCE population effect, orthogonal to province membership.
- **Headline numbers**:
  - **β_within = 0.587** (close to Carleton's "no-zeros" 0.68)
  - **β_between ≈ −0.26 with wide CI** (not separately identifiable from province-level everything else; explicitly flagged)
  - **f_within = 0.299, 95 % CI [0.240, 0.366]** — verdict **SUPPORTED** (prereg's three-way rule: 95 % CI wholly above 0.10)
  - **P(f_within > 0.20) ≈ 1.000**
  - R̂ = 1.0000; ESS_bulk ≥ 861; 0 divergences
- **The framing line**: "~ 30 % of city-to-city systematic variation in inscription production is attributable to within-province population. Habit, convention, survival, and provincial-administrative effects together account for the other ~ 70 %." That's the complexity-decomposition Shawn's abstract promises.

### Slide 7 — Where this is heading + feedback prompts (~ 80 s)
- One slide; close out. Acknowledge OSF lodgement (`osf.io/uycs6`, currently embargoed); point to the public repo at the lodgement tag.
- Six feedback prompts on the right. Pick **2–3 to highlight aloud**; the rest are there for the audience to read at their own pace.
- Recommended priority for what to say out loud:
  1. Prompt 1 (editorial-template decomposition — for Heřmánková / Kaše / Glomb specifically)
  2. Prompt 2 (the 70% non-population variance — which sub-mechanisms?)
  3. Prompt 6 if Sommerschield is still in the room — open the cross-collaboration question

## 3 · Anticipated Q&A — quick responses

(For the longer versions, see `talking-points-feedback.md`. These are the
3-sentence headline responses.)

### Q1 — "Counts mostly reflect the epigraphic habit, not population"
- "Agreed in part — that's why the within-between specification separates them. The Mundlak decomposition isolates the within-province population effect, orthogonal to province-level habit / culture / survival differences. The binding test attaches only to f_within, which here is 0.30 with the 95 % CI wholly above the 0.10 threshold. The between-province component IS reported but flagged as confounded with everything-else."

### Q2 — "Hanson 2016 populations are uncertain"
- "Yes. The prereg includes a measurement-error sensitivity at σ_pop ∈ {0.1, 0.2, 0.3}; if f_within shifts by more than 50 % of its CI width under any σ_pop, that's flagged. Not run yet — that's preregistered post-talk Phase 3 work."

### Q3 — "Why exclude Rome?"
- "Rome contributes 65,435 of 180,609 inscriptions (36 %); as a single outlier it dominates the scaling fit. Hanson 2021 excludes Rome for the same reason (Table 7.3 caption). Reported transparently."

### Q4 — "Why frequentist and Bayesian on the same deck?"
- "Slide 6a is the direct comparator to the published literature (Hanson 2021, Carleton 2025), which is frequentist. Slide 6b is the preregistered within-province decomposition — that's the genuinely new substantive analysis. They answer related but distinct questions; β_within = 0.587 sits inside the bootstrap CI of empire-wide β = [0.543, 0.574], so they're qualitatively consistent."

### Q5 — "How do you handle wide-template editorial encoding?"
- "Two-pronged. For the cross-sectional H3a regression on slide 6b, the protection is the 50 BC – AD 350 date-window filter itself (cross-sectional artefact protection). For the temporal SPA analyses (H2.1 validation, H3b deviation-detection), the protection is the Bayesian mixture model shown on slide 5. The mixture is NOT applied to the cross-sectional counts because per-city mixture is unidentified for ~ 600 of the ~ 1,000 cities below N = 100."

### Q6 — "Which subgroups would dominate / fail the population scaling?"
- "Open question — this is one of our explicit feedback prompts (slide 7, prompt 3). The prereg pre-specifies subset analyses; we'd love nominations of natural negative controls (where habit-only should clearly dominate) or natural positives."

### Q7 — "What about survival bias?"
- "Real and acknowledged. The between-province component is explicitly flagged as not separately identifiable from province-level survival-bias variation. Within-province is more defensible because it controls for province-level survival differences. Reported as a limitation in the prereg §9."

### Q8 — "Where can I see the prereg / repo?"
- "The OSF preregistration is at **`osf.io/uycs6`** — the URL is publicly visible but the deposit contents are **currently embargoed pending a journal-submission decision** on whether to submit to a venue requiring double-blind review. The embargo will lift once we decide on a venue. The repo is public at **`github.com/saross/inscriptions/tree/osf-lodgement-2026-05-20`** — that's the snapshot at the moment of lodgement."

### Q9 — "The 1,044 cities — the prereg says ~ 815?"
- *Unlikely to come up unless someone has pre-read the prereg.* If it does:
- "Good catch. The prereg's '~ 815' figure was inherited from our 2024 exploratory notebook, which applied an additional Latin-speaking-province filter via a manually-curated province-language mapping that isn't a column in the LIRE parquet. The prereg's text spec — 'all cities with Hanson population estimates, Rome excluded' — yields 1,044 directly from the parquet. We're following the text spec, not the inherited number. This is logged as a methodological footnote in `runs/2026-05-21-talk-prep/code/01-filter-and-prep.py` and will be addressed in the prereg amendment trail."

## 4 · Backup-slide map (Q&A reserve)

If a question goes substantive, jump to the relevant backup slide. Press
**`o`** in revealjs for the slide overview, or use the slide number.
The deck now carries a **12-slide deep-dive** behind the main 8 main slides.

| If asked about… | Jump to | Says… |
|---|---|---|
| Why exclude Rome | **B1** | 36 % of corpus, dominates as outlier, Hanson 2021 also excludes |
| Why the 50 BC – AD 350 envelope | **B2** | Constrains the data-attribution artefact; aligned with Hanson 2016 |
| Hanson population uncertainty | **B3** | Preregistered Bayesian measurement-error sensitivity (σ_pop ∈ {0.1, 0.2, 0.3}) |
| Why NBR not OLS log-log | **B4** | Over-dispersed counts; OLS dragged toward zero by low-count tail |
| Why no per-city mixture | **B5** | Unidentified for ~ 600 cities with N < 100; date-window filter is the cross-sectional artefact protection |
| Year-precise inscriptions in the mixture | **B6** | Not in convention component; stay in p_gen as real ancient anchors |
| Survival / publication bias | **B7** | Within-province is robust to province-level survival; between-province explicitly flagged |
| 1,044 vs prereg's "~815" sample-size note | **B8** | Stale Latin-province subset; we use the text-spec-faithful denominator; logged for amendment |
| Can small-N cities tell us anything? | **B9** | Yes for shape claims + H3a leverage; no for temporal deviation-detection |
| Hanson 2021's specific residual findings | **B10** | Provincial-capital over-production; Moran's I = 0.046 on residuals; prereg H3c replicates both |
| Future statistical directions (HMM) | **B11** | Martin's state-space proposal; post-lodgement OSF amendment if pursued |
| Why both frequentist and Bayesian | **B12** | Slide 6a is the published-literature comparator; slide 6b is the new substantive contribution |

## 5 · Tone and what to *not* over-claim

Read every quantitative slide aloud with the framing **"preliminary,
post-lodgement; the preregistered analysis is forthcoming"** — this is
non-negotiable for preregistration compliance and protects against any
audience member who treats the talk as a final result.

**What is in scope to claim** with confidence:
- Editorial-template distortion is real, measurable, and separable (slide 2)
- Phase 1 reachability is locked methodology (slide 3)
- The mixture model can recover known answers on synthetic data (slide 5)
- Population accounts for ~ 30 % of city-level systematic variation (slide 6b) — *preliminary*

**What to be careful about claiming**:
- "Habit is wrong" — never. Habit is real; we account for it; both matter.
- "We've settled the population vs habit debate" — never.
- "The full preregistered analysis confirms…" — say "the preliminary
  Bayesian Mundlak fit *supports* the within-province population effect;
  full preregistered Phase 2/3 work runs post-talk."
- The mixture model's specific tier weights or genuine-SPA shape on real
  data — the talk shows synthetic recovery only; real-data fits are
  Phase 2.

**What's defensible to defer**:
- "How robust is f_within = 0.30 to specification choices?" — prereg
  includes three-weighting sensitivity, measurement-error sensitivity,
  brms shadow validation. All post-talk.
- "Per-city α estimates" — unidentified for low-N cities; out of scope.
- "Statistical method details" — defer to the prereg and Martin's
  consultation pack; you don't have to be the statistician in the room.

## 6 · If you're asked a question you don't know

Three escape patterns, in priority order:

1. **"That's exactly the kind of feedback we're looking for — would you mind dropping me a line / catching me afterwards?"** This is the prepared response for any audience member who raises something substantive that needs more thought.
2. **"Shawn would have a better answer — let me get back to you via email / drop me your card."** Reasonable for any technical question outside the talking points.
3. **"I'll take that one to the discussion."** Buy time during Q&A; come back to the room afterwards.

## 7 · Logistics

- **Slot**: Friday 22 May 14:20 in room **Preben Hornung**. Session is TRAC7 ("Beyond names and numbers"); organisers Heřmánková / Glomb / Kaše (Masaryk SDAM — the LIRE creators).
- **Adjacent talks**: Sommerschield (Aeneas, neural-net for Latin inscriptions) precedes you at 14:00 — natural overlap; Bennett (global epitaphs) follows at 15:00.
- **Your own talk** at 12:20 on marriage ages is separate; this brief is only for the 14:20 slot.
- **Time budget**: 12 min presentation; 5 – 7 min for Q&A inside the 20-min slot. Pace yourself; the speaker-notes in the .qmd embed per-slide time budgets.
- **The OSF embargo handling**: if pressed, "the prereg is currently embargoed pending a journal-submission decision; the embargo will lift when we choose a venue." That's the line. No need to elaborate.

## 8 · After the talk

- **Capture audience feedback**: any nominations of subcorpora as negative or positive controls; any independent demographic-data pointers; any methodological pointers we should be citing. A 5-minute voice memo / scribbled notes is invaluable.
- **Email Shawn ASAP** with anything substantive. He'll fold into the post-talk reflection.
- **The reflection file** lives at `docs/notes/reflections/` — Shawn will post-process; you don't need to write into it directly.

---

Break a leg. The room is the right room for this material — the LIRE
creators are in the audience and the session abstract explicitly welcomes
statistical methods for selection-bias mitigation. The deck is built to
land the empirical wedge "population is a *partial* contributor and we
can measure how much" — not to refute the habit-only prior, but to
nuance it with a preregistered methodology.
