---
priority: 4
scope: always
title: "Working Notes"
audience: "researchers and future instances"
---

# Working Notes — inscriptions

Running observations, methodological notes, and analytical findings
that emerge during the project. More structured than session
reflections, less formal than papers or reports. Numbered
sequentially; do not renumber.

Each observation should stand on its own — readable cold, in 3–5
years, without session context. State the fact, cite the source,
note the implication.

---

## Obs 1 — 2026-04-22: LIST and LIRE share an identical 65-attribute schema

LIST (525,870 rows, DOI 10.5281/zenodo.10473706, v1.2 9-Jan-2024) and
LIRE (182,852 rows, DOI 10.5281/zenodo.8147298, v3.0 11-Oct-2023)
share the same 65 attributes. LIRE is a row-filter of LIST: only
records with `is_within_RE == True`, `is_geotemporal == True`, and a
50 BC – AD 350 date-interval intersect. No schema transformation.

**Implication:** a LIRE-to-LIST swap in the analytical pipeline is a
single `read_parquet` change plus application of the three filter
predicates up-front. The conference-paper plan's LIRE-first / LIST-
later strategy is structurally free at swap time.

*Source:* LIST Zenodo record; LIRE Zenodo description; LI_metadata.csv
at `/tmp/LI_metadata.csv`.

---

## Obs 2 — 2026-04-22: `urban_context_pop_est` is pre-joined Hanson 2016 populations at 5-km buffer

Both LIST and LIRE carry `urban_context_pop_est` as a row-level
attribute. The metadata dictionary describes it as *"Estimated
population of a city from Hanson 2016, 2019
http://oxrep.classics.ox.ac.uk/databases/cities/"*. The joining
rule: the ancient toponym of the largest city within a 5-km buffer of
the inscription findspot. `urban_context` gives the class
(large/medium/small/rural); `urban_context_city` gives the toponym.

**Implication:** §5.5 demographic-proxy comparison is a `groupby(
urban_context_city).agg({urban_context_pop_est: 'first', LIST-ID:
'count'})` with a type cast (the column is stored as character).
External join against Hanson's raw data is not required for the
first-pass analysis. Hanson's raw tDAR dataset (record 448563) can
still be useful as ground-truth cross-check.

*Source:* LI_metadata.csv verbatim attribute description; confirmed
by OpenAlex abstract on LIST Zenodo record.

---

## Obs 3 — 2026-04-22: No Python package provides significance envelopes for calendar-date SPAs

The `radiocarbon` PyPI package implements pointwise Monte Carlo
significance envelopes via `SPDTest`, but is hard-coded to radiocarbon
calibration curves (IntCal20/ShCal20) and requires BP dates with
standard deviations — not calendar intervals. `rcarbon` (R, Crema &
Bevan 2021) is the reference implementation with `modelTest()` and
`permTest()` but is R-only and likewise radiocarbon-oriented. ADMUR,
iosacal, p3k14c-py: all radiocarbon-only. `baorista` (Crema 2025):
calendar-compatible but R + NIMBLE, too heavy for the near-term.

**Implication:** the significance-testing layer, the permutation-test
layer, and the power-analysis layer all require implementation in
Python (~200 LOC total). `scipy.stats.permutation_test`,
`numpy.quantile`, and a simulation loop are the primitives.
`rcarbon/tests.R` is the algorithmic reference to port.

*Source:* prior-art-scout pass, 2026-04-22. Full candidate table in
agent output, preserved at
`/tmp/claude-1000/-home-shawn-Code-inscriptions/.../ac5ca3dae06aa2ac3.output`.

---

## Obs 4 — 2026-04-22: `tempun` is SDAM's own Python package; Adela is co-author on the demo notebook

The SDAM team (Kaše, Sobotková, Heřmánková) publishes `tempun` on
PyPI (v0.2.4 Jan 2026, MIT licence). It implements aoristic date
sampling via `model_date(start, stop, size, b)` with `b=0` for
uniform and `b>0` for trapezoidal, plus `get_simulation_variants()`
for replicate generation. Covers criterion (i) of the four
methodological needs; does not cover (ii)–(iv).

Adela Sobotková is a co-author on the `tempun_demo` notebook
(`github.com/sdam-au/tempun_demo`, 2023). Using tempun puts the
project on Adela's conceptual territory and the SDAM team's
toolchain, aligning with the stated preference.

**Implication:** `pip install tempun` is the aoristic-sampling
dependency for the project. Build the significance / permutation /
power layer as a package on top (proposed name: whatever Shawn
prefers; defer to decision-log).

*Source:* prior-art-scout report, 2026-04-22.

---

## Obs 5 — 2026-04-22: Glomb, Kaše & Heřmánková 2022 Asclepius paper is the closest published template

Glomb, Kaše & Heřmánková (2022) "Popularity of the cult of Asclepius
in the times of the Antonine Plague: Temporal modeling of epigraphic
evidence" (*JAS Reports*, DOI 10.1016/j.jasrep.2022.103466) models
temporal distributions of Asclepius-dedication inscriptions against
plague chronology. It applies probabilistic date treatment (aoristic
style) to an epigraphic subset. It does NOT use rcarbon-style
permutation envelopes against a pan-empire null, which is the gap
this paper's approach addresses.

**Implication:** (i) cite as the closest prior art and differentiate
method against it; (ii) the Antonine Plague effect-size anchor for
the Friday power-calculation is well-motivated by existing
literature — Adela will recognise it; (iii) a robust-to-sample-size
detection of the plague signature in the broader LIST corpus would
be a methodologically useful replication-and-extension of this
paper's claim.

*Source:* lit-scout verified bibliography 2026-04-22, row 8.

---

## Obs 6 — 2026-04-22: No rcarbon-style permutation envelope has been applied to Latin inscriptions

Across the verified 25-row bibliography + the prior-art-scout +
targeted searches, no published paper applies Crema/Bevan
permutation-envelope machinery (rcarbon-style `modelTest` or
`permTest`) to Latin inscription date distributions. The SDAM
cluster's temporal modelling uses simpler probabilistic-date
frameworks (e.g., tempun Monte Carlo replicates) without significance
envelopes against a fitted null.

**Implication:** the paper's originality claim is clean and
well-supported. The framing sentence — "the first application of
SPD-permutation-envelope machinery to a large Latin epigraphic
corpus" — can stand in the abstract without hedging.

*Source:* lit-scout verified bibliography 2026-04-22, gap analysis §1.

---

## Obs 7 — 2026-04-22: LIST inherits documented data-quality artefacts from EDH/EDCS

The SDAM team's own methodology paper (Heřmánková, Kaše, Sobotková
2021, *JDH*) documents upstream quality issues that LIST inherits and
that the LIRE filters do NOT fix:

- Century-basis dating produces midpoint spikes at 50, 150, 250 AD
  (§64 of JDH paper).
- Editorial convention produces spikes at reign boundaries (Augustan
  14 BC–AD 27; Antonine AD 97–192; Severan AD 193–235) (§94).
- Province labels in EDH are anchored to mid-2nd-century Roman
  geography and do not respect inscription-date (§48).
- EDCS coordinates have false precision at the 7-decimal level; real
  accuracy is hundreds of metres to kilometres (§60).
- 50% of EDCS coordinates lack documented provenance (§45).

**Implication:** the feasibility study's *data artefacts* section
should enumerate these, state which are mitigated by method choice
(aoristic-uniform treatment damps midpoint spikes somewhat; permutation
envelopes can detect artefact-driven deviations from a realistic
null), and which remain as interpretive caveats (editorial spikes,
province-label anachronism). None of these are reasons to abandon
the project; all are reasons to report transparently.

*Source:* Heřmánková, Kaše, Sobotková 2021, §§41–64, 94, as extracted
by the LIST reconnaissance agent 2026-04-22.

---

## Obs 8 — 2026-04-22: Hanson 2021 letter-count attribution is UNVERIFIED

The 2024 ANU seminar doc attributes a letter-count-as-analysis-
alternative recommendation to Hanson 2021 ("at the suggestion of
Hanson 2021"). The lit-scout proposer and verifier both could not
confirm this from the Hanson 2021 abstract, keywords, or title
(Brepols PDF is paywalled / 403-blocked from both agents). The
Hanson 2021 abstract focuses on *inscription counts* as "information
infrastructure" scaling sub-linearly with settlement populations.

**Implication:** do not cite Hanson 2021 as the source of the
letter-count suggestion in any draft until the primary PDF has been
read and the specific passage located. Alternative possibilities:
the suggestion may be in Hanson/Ortman/Lobo 2017 (functional
diversity indices), or in the broader Bettencourt urban-scaling
literature on signage letter-counts, or in a 2024-moment conflation.

*Source:* lit-scout verified bibliography 2026-04-22, row 1 +
side-question #1 both flagged UNVERIFIED.

---

## Obs 11 — 2026-04-23 [PATTERN]: editorial-convention hierarchy hypothesis — round-number attractors compete with reign boundaries by distance

Across seven editorial-boundary years tested in the 2026-04-23 rerun,
the dip-vs-spike outcome appears to depend on distance to the nearest
round-number attractor (round century / half-century / quarter-century)
rather than on whether the year is a dynastic transition per se:

| Year | Nearest round | Distance | Observed |
|------|---------------|----------|----------|
| AD 97 | AD 100 | 3 y | **DIP** (ratio 0.25) |
| AD 192 | AD 200 | 8 y | DIP |
| AD 193 | AD 200 | 7 y | DIP |
| 14 BC | 15 BC (¼) | 1 y | DIP |
| AD 27 | AD 25 (¼) | 2 y | DIP |
| AD 212 | AD 200 / 225 | 12 / 13 y | **SPIKE** (ratio 1.46) |
| AD 235 | AD 225 / 250 | 10 / 15 y | **SPIKE** (ratio 1.86) |

**Tentative hypothesis.** Editorial anchoring follows a hierarchy —
round century > round half-century > round quarter-century > reign
boundary. When a reign-boundary year is within ~8 years of a strong
round-number attractor, the mass is absorbed by the round number and
the reign-boundary year appears as a dip. When the reign-boundary year
is >10 years from the nearest round number, the reign-boundary
convention wins and the year appears as a spike.

**Why this matters.**

1. **Informs the deconvolution-mixture `convention_SPA` shape.** The
   current mixture-model plan (Decision 7) treats convention as uniform
   century slabs. If the hierarchy hypothesis holds, a weighted
   multi-tier convention (more mass at centuries, less at half-centuries,
   less again at quarter-centuries, residual at reign-boundaries only
   when far from rounds) is a better generative model → sharper
   deconvolution.
2. **Potentially publishable as a methodological finding in its own
   right**: "Quantifying the editorial-convention hierarchy in Latin
   epigraphic databases." Could be a subsection of the main paper or
   headline content for the FS-0 methods-paper split.
3. **Generalisable beyond inscriptions.** Any editor-mediated aoristic
   corpus (historical medical records, court records, cultural-heritage
   objects) potentially exhibits an analogous hierarchy-of-anchors
   behaviour, assuming editors default to round-number dates when
   uncertain. Promotion candidate for
   `~/personal-assistant/notes/llm-craft.md` if the pattern reproduces
   on a second corpus.

**Planned test (Thursday 2026-04-24).** Extend the editorial-spikes
check to seven additional dynastic transitions: AD 68, AD 69, AD 96,
AD 117, AD 138, AD 161, AD 180. Holm-Bonferroni across an expanded
family of 14. Prediction: AD 96 and AD 180 (near round attractors)
should dip; AD 138 and AD 161 (far from rounds) should spike; AD 68,
AD 69, AD 117 (mid-range) are ambiguous.

**Post-LIST-swap extension.** LIST covers late antiquity where LIRE
does not. At that point, add late-antique dynastic transitions
(Diocletian → Tetrarchy → Constantine → Valentinian → Theodosius,
specific years TBD when LIST envelope is in hand) to test whether the
hierarchy hypothesis holds beyond the third century.

*Source:* 2026-04-23 comprehensive profile rerun outputs
(`runs/2026-04-23-descriptive-stats/outputs/artefacts.md`,
`drill-downs/year_97_neighbourhood.md`). Discussion with Shawn
2026-04-23 during wind-down.

---

## Obs 10 — 2026-04-23 [PATTERN]: seed lit-scout across both clusters when a topic has a computational sibling

The verified 25-row bibliography produced by `lit-scout` on 2026-04-22
missed **Aeneas** (DeepMind + University of Nottingham, *Nature* July
2025) — a model trained on ~176,000 Latin inscriptions, directly
adjacent to this project's corpus. A prior-art-scout run on 2026-04-23
surfaced it within minutes.

**Why lit-scout missed it.** The seed list chained through SDAM
epigraphy, Crema/Bevan SPD methodology, and the Hanson urban-demography
cluster. Aeneas lives in a different citation cluster —
NeurIPS / Nature-ML / DH-NLP — that shares vocabulary only thinly with
the epigraphic-methodology cluster we seeded. Backward chaining from
an archaeology-SPD seed doesn't reach Aeneas; forward chaining
doesn't either, because Aeneas's citers are ML and digital humanities
rather than archaeology-methodology.

**The pattern.** When running systematic literature discovery on a
topic that has a **computational sibling** (ML/NLP/AI applied to the
same substantive domain), seed both clusters explicitly — one seed
set from the target-discipline methodology literature, one seed set
from the computational-sibling literature. Chain each independently.
Merge. Otherwise you'll return a bibliography that looks complete
within one cluster and has a blind spot across clusters.

**Implication for this project.** A supplementary `lit-scout` chain
seeded on Aeneas + ML-for-inscriptions + NLP4DH adjacent literature
runs today (2026-04-23) to close the gap before Friday.

**Generalisation candidate for `~/personal-assistant/notes/llm-craft.md`**
if the pattern reproduces on a second project. The convention for this
project: `[PATTERN]` tag in a working-note heading marks a promotion
candidate; promote when the pattern is confirmed outside a single
domain.

*Source:* prior-art-scout report 2026-04-23 (Area 1, Aeneas finding);
lit-scout draft 2026-04-22 (gap analysis, no ML-for-classics rows).

---

## Obs 9 — 2026-04-22: Kaše affiliation update

As of 2024–2025, Vojtěch Kaše's primary affiliation is University of
West Bohemia (Pilsen). He retains an Aarhus University affiliation
through the SDAM / CEDRR projects. Heřmánková and Sobotková remain
at Aarhus.

**Implication:** acknowledgements and correspondence lists should
reflect the West Bohemia / Aarhus dual affiliation for Kaše.

*Source:* lit-scout verified bibliography 2026-04-22, side-question
#2. OpenAlex LIST metadata + Kaše's own profile pages. Verifier
could not independently confirm via metadata endpoint alone; flagged
for user-side confirmation if load-bearing for acknowledgements.
