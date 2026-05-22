# Speaker notes — *Dates-as-Data for Inscriptions*

*Companion to `inscription-spa-slides.pdf` / `.html` · RAC-TRAC 2026, TRAC7, Aarhus*

Brief bullet reminders per slide. For the full continuous prose, see `inscription-spa-script.md`.

---

## 1 · Are inscriptions a demographic proxy?

**Slide 1** (≈ 90 s)

- SPA tradition: Rick 1987 · Timpson 2014 · Crema & Bevan 2021
- LIRE v3.0: 180,609 inscriptions, Western Empire, 50 BC – AD 350 (Kaše 2023)
- Objection: MacMullen 1982 / Hanson 2021 — *epigraphic habit*, not demography
- Wedge (Petra Heřmánková): even ~ 10 % demographic = significant
- *Take-away*: not refuting habit — testing how much signal survives
- Tone: exploratory, feedback-seeking

---

## 2 · Problem: Serious editorial distortion of inscription dates

**Slide 2** (≈ 110 s)

- **Concrete example**: "2nd c AD" ≠ uniform 100–199, it's *the template*
- Other examples: "mid-Flavian" · "reign of Hadrian" · "second quarter of the 3rd c"
- **Hazard**: uniform-aoristic on conventional dates → flat plateaus + sharp steps
- **Evidence**: 54.5 % `not_before` end `01` · 53 % `not_after` end `00` · +1,159 at BC/AD step
- **Spikes (proactive — someone will ask)**: AD 77.5 / 122.5 / 212.5 are a mix of convention + tighter dating
- **Hadrianic 122.5**: ~ 70 % year-precise (consular AD 123) + ~ 30 % reign-template [117, 138]
- **Close**: convention is separable → slide 3a (reach) · slide 5 (model)

*If pressed on specifics*:
- AD 77.5 = Flavian consular pairs [78, 79] etc — real practice, "Flavian" is editorial label
- AD 212.5 = Severan reign-interval, closest to pure convention
- High-precision filter (≤ 25 y): ~ 20,286 inscriptions; NB Hadrian's 21-y reign fits inside → filter is not a clean separator; mixture model on slide 5 is the proper tool

---

## 3a · Minimum corpus required to detect deviations determined by simulation

**Slide 3a** (≈ 100 s)

- **Power simulation** done *before* substantive analysis — pre-analysis discipline
- Synthetic corpora with planted signal → run detection method → measure rate
- 96 cells × 1,000 replicates each
- **Empire** (n = 50,000): reachable — that's the only n tested at empire
- **Province / city**: ≥ ~ 1,600 inscriptions for crisis-scale (50 % / 50 y)
- False-positive ≤ 5 % across all 96 nulls (range [0.007, 0.049])

*If pressed*:
- "1,600" is rounded; measured floors range 1,385–1,938 across four null specs
- Heatmap colours: greener = reliably detectable; redder = below floor

---

## 3b · Deviation detection across sample and effect sizes

**Slide 3b** (≈ 90 s)

- **Practical reads** for a historian's subset:
  - **N < 1,000** → cross-sectional or descriptive only
  - **N ≈ 2,500** → 50 % / 50 y events reliably (≥ 0.97 detection)
  - **20 % / 25 y** → undetectable at any tested N (method-broad, not us-specific)
- Empire-wide subsets (e.g. collegia ≈ 3,000) → reachable at empire, partial at province
- "Pre-analysis discipline" — what claims YOUR subset supports

*If pressed*:
- Tier 2 follow-up: finer brackets · Tier 3: per-subset reachability with subset's own aoristic widths
- Method = preregistered permutation-envelope test; Bayesian aoristic (Crema 2025) may differ

---

## 4 · What the data look like at multiple scales

**Slide 4** (≈ 110 s)

- Top 8 provinces + top 8 Hanson-cities, peak-normalised, **raw** (no mixture correction)
- **Pompeii**: cuts off at AD 79 (Vesuvius) — literal preservation artefact
- **Dacia**: narrow AD 100–270 ≈ Roman occupation (Trajan → Aurelian)
- Latium-Campania early spike includes the Pompeii contribution
- Other features: Pannonia super late peak · Britannia mid-2nd c · Cirta tight peak AD 200
- *Mix of demography, habit, and preservation — distinguishing them is the rest of the talk*
- Q&A invitation: which shapes does the room recognise?

---

## 5 · Removing the convention layer

**Slide 5** (≈ 110 s)

- **Model**: observed SPA = convention slabs + ancient signal (mixture)
- Convention component constrained by **template dictionary**: centuries, half-centuries, reigns (Augustan, Flavian, Hadrianic, Antonine, Severan)
- Year-precise inscriptions → stay in ancient signal (real anchors)
- Constraint makes the mixture **identifiable** — can't trade mass arbitrarily
- **Provenance**: Crema 2024 (baorista, interval-dated ceramics) — direct transfer
- 2024 pilot: discarded wide dates → lost > 50 % of corpus (median range > 100 y); mixture keeps them
- **Figure**: synthetic data, top panel = mixed observation (red+green overlay on grey), bottom panel = recovered ancient signal vs planted truth
- **Output (right column)**: cleaner SPA → input to all downstream temporal analyses
- *Don't say*: "α / posterior / Pearson r / NUTS" — that panel was cropped; refer to G-series if asked

---

## 6 · What we found

**Slide 6 — THE PUNCHLINE** (≈ 130 s · *let it breathe*)

- **Method**: compare cities **WITHIN same province** → strips out province-level confounds (habit, economic, social, political, cultural, survival)
- "Within-between" decomposition borrowed from **Mundlak (1970s econometrics)**
- **Result**: ~ 30 % of city-to-city variation = within-province population
- Sample: 1,044 Hanson-matched cities **ex-Rome**
- 95 % CI [24 %, 37 %] — well above preregistered 10 % "supported" threshold
- "First preregistered quantitative partition of habit-vs-population on a major inscription corpus"
- **MAUP caveat**: single-scale here; multi-scale check (cities-within-macro-regions etc.) post-talk

**DON'T say aloud**: "Bayesian Mundlak NBR" · "β_within" · "f_within" · "posterior" · "0.587"

**Anticipated questions**:
- *Why no mixture correction here?* → cross-sectional uses date-window filter, not mixture; per-city mixture unidentified for ~ 600 small cities
- *Vs Hanson 2021?* → β ≈ 0.566 (CI [0.543, 0.574]) vs Hanson 0.672 / Carleton ~ 0.68 — same family; both exclude Rome; difference is corpus / filter (backup B12)
- *Subgroups?* → prereg § 5, post-talk

---

## 7 · What it means

**Slide 7** (≈ 100 s)

**Three implications**:

1. **Habit-only critique** — partially refuted; not the whole story (~ 30 % demographic vs ~ 70 % habit-territory)
2. **Inscription-SPA toolkit** opens for epigraphic studies, with sample-size tiering (back to slides 3a / 3b)
3. **Small-N corpora** not shut out — descriptive + cross-sectional remain at any N

Transition to 7a: "Let me show you what that looks like concretely…"

---

## 7a · Worked example: marriage-age inscriptions

**Slide 7a** (≈ 70 s · *can compress to 45 s if her own talk already gave the data structure*)

- **Corpus**: Adela's wife / daughter — ~ 1,700 records (894 wives + 813 daughters); C2 + C3 dominate (~ 75 %)
- **Classic framing**: Shaw & Saller — wife-overtakes-daughter age as marriage-age proxy
- **Question**: did the crossover age *shift* (Antonine plague, 3rd-c. crisis)?
- **Static crossover**: comfortably supported · Adela has reproduced Shaw under stricter filters
- **Continuous trajectory** (per-50-y bin, ~ 200–300 records): below the 1,600 floor
- **Workaround**: categorical comparison across pooled periods; urban vs rural slicing
- **General point**: any small-corpus project maps onto the same ladder

---

## 8 · Questions for this room

**Slide 8** (≈ 60 s)

- **Pause 5–10 s after each question** — invite thinking, don't fill time
- Order: Q1 first if LIRE / SDAM colleagues present · Q3 first otherwise (most provocative)
- Q1 = LIRE / SDAM team · Q2 = methodology · Q3 = falsification · Q4 = anchors

---

## 9 · Open science

**Slide 9** (≈ 30 s · close)

- OSF prereg lodged 2026-05-20, embargoed
- Repo public at lodgement tag — clone & audit
- Feedback-seeking; confirmatory tests run post-talk
- *"Thank you. I'd value your feedback."*
- Press `o` for overview if Q&A needs backup slides

---

## B1a · Why exclude Rome — the numbers

SPEAKER NOTE B1a: short version if asked — "Rome has 65,435
inscriptions, the next largest has 4,508. As a single point it
dominates the regression; Hanson and Carleton both exclude it for
the same reason."

---

## B1b · Why exclude Rome — what we report

SPEAKER NOTE B1b: only the most stats-savvy questioner will ask
about including Rome. If they do, point them at this slide. The
"could in principle" line is the right tone — we're not avoiding
the question, we're flagging that the answer would carry a known
caveat.

---

## B2 · Why the 50 BC – AD 350 envelope?

SPEAKER NOTE B2: the envelope is a date-attribution artefact protection.
Going earlier or later requires modelling different epigraphic regimes
(Republican Latin vs Late Antique Christian). An envelope extension to
AD 600 via LIST v1.2 is a candidate for a follow-up paper.

---

## B3a · Hanson population uncertainty — the data

SPEAKER NOTE B3a: the audience's natural objection is "Hanson's
numbers are noisy, so any analysis taking them at face value is
suspect". That objection is valid. B3b describes how we test
robustness to that noise.

---

## B3b · Hanson population uncertainty — what we do about it

SPEAKER NOTE B3b: short version — "Hanson populations are
max-theoretical, not realised peaks. The preregistered sensitivity
runs a Bayesian measurement-error model with σ_pop up to 0.3;
the pre-binding sensitivity shows robust under all three levels.
Formal version of the test runs post-talk."

---

## B4 · Why NBR? Why not OLS log-log?

SPEAKER NOTE B4: this is methodologically important and worth landing
clearly with a stats-curious audience. The specification matters
because OLS log-log assumes Gaussian noise on log-counts at a constant
scale, but low-count cities have much higher relative noise. NBR
handles that. The published comparators (Hanson 2021, Carleton 2025)
use OLS log-log — our preliminary fit at NBR sits in the same family,
which validates the methodology while pointing to a spec improvement.

---

## B5 · Why not fit the mixture model per-city?

SPEAKER NOTE B5: identifiability matters. Even with a perfect model,
you can't extract a 5-parameter mixture decomposition from 30
inscriptions. The empire-level fit (with N = 180,609) has plenty of
data; per-city fits don't. The 50 BC – AD 350 date-window filter does
the artefact-protection job for the cross-sectional analyses; the
mixture handles only the temporal analyses (H2.1 validation, H3b
deviation-detection).

---

## B6 · How does the mixture treat year-precise inscriptions?

SPEAKER NOTE B6: this matters because year-precise inscriptions are the
strongest signal of genuine ancient production. AD 122.5 is partly
driven by the exact-year template [123, 123] (1,304 inscriptions
explicitly dated by consular AD 123). Folding those into the convention
component would mean treating real ancient anchoring as artefact —
methodologically wrong.

---

## B7 · Survival and publication bias

SPEAKER NOTE B7: short version — "Province-level survival
differences are absorbed into the between-province coefficient and
don't bias the within-province 30 %. Pompeii is the obvious
within-province survival outlier; its cut-off is empirically
visible so we can handle it. Smaller within-province differences
should average across 1,044 cities."

---

## B8 · The sample-size footnote: 1,044 vs the prereg's "~815"

SPEAKER NOTE B8: only mention this if asked. It's a transparency
footnote — we found a discrepancy between the prereg's quoted N and
what the text-spec produces from the data. We're going with the
text-spec. Will be addressed in the amendment trail.

---

## B9 · Can small-N cities (100–250 inscriptions) tell us anything?

SPEAKER NOTE B9: this is the historian's natural question. The answer
is nuanced: small-N cities are not "noise" but they're also not
quantitative time-series. They carry shape information that's useful
when triangulated with archaeological / textual / numismatic evidence;
they're too sparse to bear formal inferential load on their own. The
prereg's §5 Layer A (descriptive shape comparison) and Layer B
(tentative inversion to population trajectory under assumption) are
the framings to use. Best practice: use the inscription series to
corroborate inferences from other evidence streams, not to carry them.

---

## B10 · Hanson's residual findings (Hanson 2021 replication)

SPEAKER NOTE B10: Hanson's residual structure is itself a substantive
historical finding — it says provincial capitals are not just bigger,
they're a *different kind* of city for epigraphic purposes. Our
preregistered H3c is the two-part replication test on the LIRE corpus.

---

## B11 · Martin's state-space / HMM alternative

SPEAKER NOTE B11: this is the "future methodological directions" line
of questioning. Martin's proposal would make the population a latent
time-series rather than a static value joined from Hanson 2016; the
inscription series becomes an emission of the latent population
process. State-space / HMM machinery is well-developed in ecology and
climate science but hasn't been applied to epigraphic corpora.
Genuinely novel and exciting; on the post-talk agenda.

---

## B12 · Why both frequentist and Bayesian under the hood?

SPEAKER NOTE B12: this is the "why two analyses?" question. They
serve different purposes: comparator validation against the
published literature (frequentist NBR), and the new substantive
contribution (Bayesian Mundlak). They land in the same ballpark,
which validates the methodology; the Mundlak within-between split
is the genuine new information.

NB: in the revised deck, the frequentist NBR comparator no longer
has its own main-deck slide — it lives here. The main result slide
(slide 6) leads with the 30 % within-province partition.

---

## B13a · Multi-scale (MAUP) — the concern

SPEAKER NOTE B13a: Adela's specific critique on the lodged draft.
This slide names the concern; B13b describes the post-talk fix.

---

## B13b · Multi-scale (MAUP) — the planned check

SPEAKER NOTE B13b: honest answer if pressed in Q&A — "Yes, we
know; multi-scale is on the post-talk to-do list. We expect the
30 % to be robust but that's testable rather than asserted."

---
