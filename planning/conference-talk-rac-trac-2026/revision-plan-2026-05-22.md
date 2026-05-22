---
title: "Per-slide revision plan — applying Adela's feedback to the RAC-TRAC deck"
date: 2026-05-22
audience: "Shawn (for approval) + Claude (next step's working brief)"
purpose: "Translate Adela's feedback + Shawn's narrative reframing into concrete per-slide changes. Approve, modify, or push back before any qmd edits."
status: "DRAFT — for Shawn's review"
---

# Headline direction

From Shawn's reply to Adela (the operative constraint for this revision):

> *"essentially no discussion of statistical method in the main slides other than saying what was done, focus entirely on reason why we're doing this, what the implications of the results are, and what the contribution is."*

**Main 9 slides become narrative-only.** Mechanics (alpha posterior, Mundlak, NBR, f_within, R-hat, ESS) move to G-series and B-series. Substantive numbers (30 %, ~1,600, 54.5 % / 53 %) stay — only the presentation changes.

# Proposed new arc for the main 9 slides

The substantive shape stays the same. The voice changes everywhere.

| New | Old | Working title | One-line job |
|---|---|---|---|
| 1 | 1 | The question we're trying to answer | Set up the population-vs-habit debate; promise a partition |
| 2 | 2 | Roman dates are by convention, not by year | Show the slab/spike signature; concrete example of "2nd century" |
| 3 | 3a + 3b | What we can — and can't — see in this data | Sensitivity framing: 50 %/50 y, ~ 1,600 needed; smaller / faster = unreachable |
| 4 | 4 | Production shapes at empire, province, and city scale | One-or-two interpretive annotations on the figures |
| 5 | 5 | A way to remove the convention layer | Before/after framing; alpha posterior moves to G |
| 6 | 6a + 6b | What we found | Headline: ~ 30 % within-province population, ~ 70 % everything else |
| 7 | 7 | What it means | Implications for habit critique, epigraphy, Adela's-kind-of-work |
| 8 | (new) | What we'd love feedback on | The four questions from old slide 7 |
| 9 | (new) | Where this is going | Preregistration; forthcoming work; contact |

That's 9 main slides — same total — but with implications + feedback split out from the current crowded slide 7.

Alternative: **stay at 7 main slides** and fold "what we'd love feedback on" + "where this is going" into the single closing slide as currently. Open question for Shawn.

# Per-slide revision detail

## Slide 1 (was 1) — The question

**Adela's hit**: "What is the contribution here, what problem are we solving... what implications it has on epigraphic studies beyond 'better understanding of our data'."

**What to change**:

- Drop the "40 years of dates as data" lead — it's inside-baseball for radiocarbon-savvy archaeologists; not the right entry point.
- Lead with **the substantive question**: *Can inscription counts tell us about Roman populations — or are they just cultural artefacts?*
- Three-bullet body:
  - **The habit-only critique** (MacMullen 1982; reinforced by Hanson 2021): inscription counts reflect epigraphic culture, not demography.
  - **The other view** (Petra at our 2025 conversation): if even ~ 10 % of variation in counts is population-driven, that's a significant contribution.
  - **Our goal**: a preregistered partition — how much is population, how much is everything else? If there's a real signal, we open inscription-SPA as a partial population proxy, parallel to radiocarbon-SPA in prehistoric demography.
- Image: keep the raw empire-wide SPA (works as "here's the data we're trying to read"); OR swap to a stylised slab/spike diagram if a clearer visual exists. Going with the current SPA image is fine.

**What to drop**: "180,609 inscriptions" detail (move to a footer or slide 2); the "editorial distortion" phrasing.

## Slide 2 (was 2) — Roman dates are by convention

**Adela's hit**: "you lost me here — what do you mean by editorial distortion (fuzzy chrono categories, selection of samples, ??) Context needed."

**What to change**:

- **Rename**: from "Editorial distortion has a measurable signature" to **"Roman dates are dated by convention, not by year"** (or similar). The word "convention" is what Shawn used in his reply; Adela's confusion was that "editorial distortion" reads as a vague catch-all.
- **Open with a concrete example**, not a chart:
  > *When a Roman epigrapher writes "2nd century AD", they don't mean the inscription is equally likely to be from any year between AD 100 and 199. They mean "the 2nd-century template" — a convention for expressing roughly-known dates.*
- Then introduce the empirical signature:
  - 54.5 % of `not_before` end in `01`; 53.0 % of `not_after` end in `00` — the slab signature of century templates
  - Large step at AD 1 (+1,159 inscriptions); narrow spikes at AD 77.5 / 122.5 / 212.5 — *those* are real ancient clustering (consular- or reign-dated)
- **Drop** the technical width-histogram figure (move to G or B). One figure on this slide, not two.
- Keep the regnal-spike framing because it's the proof that slabs ≠ all the structure — there's real signal under the convention layer.

## Slide 3 (merged from 3a + 3b) — Sensitivity: what we can and can't detect

**Adela's hit**: "so the meaning of the slide is that for analysis of a subset one needs to have at least 1549 inscriptions? And for empire-wide analysis at least 50,000? I don't quite understand the y axis 'bracket' labels, are these 25 and 50-year bins? What are the 20-50pc? What are 96 reachable analysis cells?"

This is the slide that took the worst hit in clarity. The 96-cell heatmap is unsalvageable for a 12-min talk audience.

**What to change**:

- **Reframe the question** from "reachability" to **sensitivity**: *What scale of historical change can we detect with the data we have?*
- **Drop the heatmap from the main slide.** It moves to G3 (the existing power-simulation explainer) and/or a new B slide for the audience members who want the detail.
- Replace with a **simple three-line table** or annotated narrative:

  | Question scale | Minimum sample | Example |
  |---|---|---|
  | Crisis-of-the-3rd-century-scale change (50 % over 50 years) | ~ 1,600 inscriptions | Top 8 provinces (each > 4,500); ~ 30 large Hanson-matched cities |
  | Sharper, smaller events (20 % over 25 years) | Not reachable at any sample we tested | — |
  | Shape comparison only (no formal change-detection) | Any N | Most cities; many small provinces |

- **Connect to Adela's wife/daughter work explicitly** (Adela's standing question; also relevant to the audience): *200 inscriptions per 50-year bin = descriptive shape claims supported; quantitative change-detection requires aggregation across bins or subsets.*

**What's gained**: a slide a historian can read in 20 seconds and a presenter can talk to in 60 seconds.

**What's lost**: the visual sophistication of the heatmap. Restored in G3 / B-series.

## Slide 4 (was 4) — Production shapes

**Adela's hit**: "What does it tell us except that each place is a tad different, peaks meaning good signal/economy vs troughs meaning ...?"

**What to change**:

- **Add interpretive annotations to the figures.** Pick 1–2 features that match recognisable historical events:
  - Top-provinces panel: arrow / label on the **Antonine peak in Asia / Achaea** (or whichever province shows it cleanly); arrow / label on a **3rd-century crisis trough** in a Western province.
  - Top-cities panel: arrow / label on **Pompeii's pre-AD 79 cut-off** as a survival-bias illustration; arrow / label on one other interpretable feature.
- **Lead with the interpretive question, not the data display**: *Production shapes vary by province and by city. Some features match historical periods we'd expect to see; others don't. Worth modelling — not just noise.*
- **Add a "for the audience" hook**: *"Which shapes look most interesting? Where do they match — or contradict — your own corpus knowledge?"* (feeds slide 7 / 8 question prompt)

**What's gained**: a slide that interprets, not just displays.

**Note on figure work**: arrows / annotations would need to be added in the figure source (matplotlib / Inkscape). If figure-edit time is short, we can do this purely in the caption — annotate in prose: "*the Antonine peak around AD 150 is visible in Asia and Achaea; the 3rd-century trough is visible in most Western provinces.*"

## Slide 5 (was 5) — A way to remove the convention layer

**Adela's hit**: "I am lost! perhaps the most unclear slide: mysterious templates intervals again; what is alpha and the posterior on alpha. This slides needs a narrative."

This is the most-confusing slide and needs the largest rewrite.

**What to change**:

- **Title change**: from "Bayesian mixture decomposition" to **"Removing the convention layer"** (or "From observed SPA to ancient signal").
- **Drop entirely from the main slide**: α (alpha), the posterior CI [0.414, 0.541], Pearson r = 1.000, "synthetic cell N = 5,000, true α = 0.50". All of this goes to G4 (existing).
- **New plain-language framing**:
  > *The observed SPA has two layers: the convention layer (those century slabs and reign templates) and a real-ancient layer underneath. We borrow a Bayesian aoristic technique developed by Crema and colleagues for interval-dated ceramics (Crema 2024) to estimate the two layers separately. The output is a SPA with the convention slabs flattened out — a cleaner picture of ancient production over time.*
- **Replace the synthetic-cell validation figure** with a **before/after schematic**: raw SPA (with slabs visible) on the left → modelled "ancient signal" SPA on the right.
- One line on validation: *"The model recovers known signals under simulation; full validation grid in progress."*

**What's gained**: a slide a non-statistical audience can follow.

**What's lost**: the recovery-demo evidence. Restored in G4 + the new B-slide on mixture validation.

**Figure question**: do we have a before/after picture? If not, we may need to create one — even a rough mock-up of an SPA with the slabs visible vs the same with slabs subtracted would do. Or use the existing fig-05 with the caption rewritten to avoid α / posterior language and treat it as a schematic.

## Slide 6 (merged from 6a + 6b) — What we found

**Adela's hit (6a)**: "On what grounds should we expect a function of 1 or more here given preservation biases, pressure for space, etc. What can we relate this ratio to? Why is Hanson's number higher — is he including Rome? What does it actually mean on the ground?"

**Adela's hit (6b)**: "Where does the 30:70% ratio come from? I do not see it in the graphs at all. What is the benefit of Bayesian Mundlak?"

**Decision needed from Shawn** (before I edit): keep 6a as a separate slide, or **fold the comparator framing into slide 6's text and lead with the 30 % headline**?

**Recommended (per Shawn's "no statistical method in main slides" rule)**: merge into a **single result slide**. The frequentist NBR coefficient β = 0.566 becomes a one-line comparator footnote ("*broadly consistent with Hanson 2021's β = 0.672 and Carleton 2025's ~ 0.68; both exclude Rome*"). The within-between decomposition becomes the main visual.

**What to change**:

- **Lead with the headline**, big text:
  > **~ 30 % of city-to-city variation in inscription counts is explained by within-province population. ~ 70 % is everything else.**
  > *95 % credible interval on the 30 % figure: [24 %, 37 %].*
- **New figure**: a visual that shows the 30 % directly — Adela's specific complaint. Options:
  - A **stacked bar**: total variation = 30 % within-province population + 70 % everything else.
  - A **within-province scatterplot**: for one or two example provinces, plot city population vs city inscription count, with the within-province trend line — showing that the relationship *holds within a province*, before any of the across-province confounds enter.
  - The existing `fig-06b-h3a-mundlak.png` — can we re-caption it so the 30 % is legible? If yes, that's the lowest-cost option.
- **One-line explanation** of what "within-province" means: *"We compare cities to other cities in the same province, not across the empire. That strips out province-level differences in habit, administration, and survival — leaving the population effect."*
- **Address Adela's "is Hanson including Rome?" question** directly: *"Hanson 2021 also excludes Rome. The difference between our β = 0.566 and his 0.672 comes from corpus choice and dating filter, not Rome."* — moves to B1 or G6.
- **Address MAUP / ecological fallacy** in one line: *"This is a single-scale (city-within-province) analysis. The full multi-scale (city–conventus–province) cross-check is in the post-talk Tier 2 work."* Flag honestly, don't bury.

## Slide 7 (was 7, now Implications) — What it means

**Adela's hit (large)**: "What is the contribution here... what implications it has on epigraphic studies beyond 'better understanding of our data'." (Also from Shawn's reply: the implications-focused reframe is the talk's main pivot.)

**What to change**:

- **Restructure entirely from "what's next + open questions" to "what this means".** Three blocks:

  1. **For the habit-only critique** — *Inscription counts carry a measurable demographic signal: about a third of city-to-city variation is within-province population. The strong "habit-only" position is partially refuted; habit is still the dominant share, but not the whole story.*
  2. **For epigraphic studies more broadly** — *Count-based and SPA-based analysis of inscriptions becomes a legitimate tool, with population as a partial control. Tier studies by sample size: change-detection above ~ 1,600 inscriptions; descriptive shape claims at any size; cross-sectional regressions can use everyone.*
  3. **For specific subfields and small-N studies** — *Adela's wife/daughter work (~ 200 inscriptions per 50 y bin) sits in the descriptive-shape regime: confidently interpretable for shape; below the change-detection floor. Other small-corpus projects can read off their position on the same sensitivity ladder.*

- **One line on what comes next** (formerly the bulk of this slide; now compressed):
  - Mixture-validation grid in progress; antonine + crisis probes; provincial-capital residuals; statistician review.

## Slide 8 (new — split from old 7) — Feedback we'd love

The four feedback questions, in plain English, with the framing "*we're presenting this for input from the room*". This is currently buried as the right half of old slide 7; pulling it out gives it the airtime Shawn's response signals it deserves.

- *Does the convention-based dating decomposition match your experience with the source-dating practice in EDH / EDCS / LIRE?*
- *Which sub-mechanisms drive the ~ 70 % non-population variance — monumental practice, status display, religious cycles, administrative density?*
- *What natural negative-control subgroups should we expect habit alone to dominate?*
- *What independent demographic anchors would you use to validate the corrected SPA?*

## Slide 9 (new — split from old 7) — Open science

- **Preregistration**: osf.io/uycs6 (embargoed; lodged 2026-05-20)
- **Repository**: github.com/saross/inscriptions/tree/osf-lodgement-2026-05-20
- **Contact**: Shawn Ross · shawn@fieldnote.au
- One-liner: *this talk is for feedback; the confirmatory tests are pinned in the preregistration and run post-talk.*

# B-series and G-series changes

## New / revised G slides

- **G2.5 (new) — What is "convention-based dating"?** — formal explainer for what we call out on revised slide 2.
- **G4 (existing) — fine.** Bayesian mixture decomposition.
- **G7 / G8 (existing) — fine.** Mundlak + f_within. Where the technical language now lives.
- **G3 (existing) — fine.** Power simulation explainer. Houses what we removed from slide 3.

## New / revised B slides

- **B6 (new or repurposed) — MAUP / ecological-fallacy concern.** Addresses Adela's specific critique. *Within-province analysis partially addresses this; full multi-scale cross-check (city → conventus → province) is in Tier 2 post-talk.*
- **B-prev (graffiti / non-monumental).** Adela hinted at it: "*are graffiti included, e.g.*". One slide on what LIRE includes / excludes.
- **B-prev (mixture before/after schematic).** The visual we promised on slide 5 — full-size in B for the curious.
- **Existing B1–B12** — minor updates only (mostly cross-references to new slide numbers).

# What stays — substantive findings to preserve verbatim

Even after the reframe:

- 30 % within-province population-attributable variance; 95 % CI [24 %, 37 %]
- ~ 1,600 minimum inscriptions (range 1,400 – 1,950 across nulls) for 50 %/50 y detection
- 54.5 % of `not_before` = `01`; 53.0 % of `not_after` = `00`; +1,159 at AD 1
- AD 77.5, 122.5, 212.5 regnal/consular template spikes
- β_within ≈ 0.587 (Mundlak); β = 0.566 (empire NBR comparator)
- 1,044 Hanson-matched cities (Rome excluded); 56 provinces
- Top 8 provinces > 4,500 inscriptions each
- Phase A sensitivities: measurement-error ROBUST under σ_pop ∈ {0.1, 0.2, 0.3}; three-weighting MATERIAL DIVERGENCE (binding per § 5)

# Open decisions for Shawn (please respond before I edit the qmd)

1. **Slide count**: 9 main slides (new structure with split implications / feedback / open-science), or stay at 7 (keep them folded into old slide 7)?
2. **Slide 5 visual**: build a before/after schematic figure, or re-caption the existing synthetic-cell figure to drop the alpha-posterior language?
3. **Slide 6 visual**: re-caption the existing `fig-06b-h3a-mundlak.png`, or build a new stacked-variance bar showing 30 % / 70 % explicitly? (Re-caption is fast; new figure is ~ 30 min.)
4. **Slide 4 annotations**: add arrows/labels to the figure (figure-edit time), or do the annotation purely in caption text?
5. **Drop slide 6a (frequentist NBR) entirely from main, keep only the 30 % within-province headline?** Or merge β = 0.566 as a one-line footnote on the new merged slide 6?
6. **Adela's MAUP / ecological-fallacy point** — address briefly on slide 6, or only in the B-series? Recommended: one line on slide 6 (acknowledges the concern without going methodological).
