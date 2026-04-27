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

---

## Obs 12 — 2026-04-24: Turchin et al. 2018's "single latent dimension of complexity" is at polity × century scale and does not usefully apply at this paper's city × decade scale

Turchin, Currie, Whitehouse et al. 2018 (*PNAS* 115:E144–E151, DOI
10.1073/pnas.1708800115; Zotero 4QJ9UWLD; also in the SDAM group's
`quantifying_human_activity` subcollection) apply principal components
analysis to nine "complexity characteristics" aggregated from 51
Seshat-coded variables across 414 polities covering ~10,000 years. PC1
explains ~77 % of variance; all nine CCs — polity population, polity
territory, capital population, four tiers of hierarchy (settlement /
administrative / religious / military), government variables,
infrastructure, information variables (writing / records), and economy
— load strongly and positively. Interpreted as "cultural complexity is
effectively one-dimensional."

**Why the 77 % headline overstates.** (i) The nine CCs were
pre-selected *because* they are expected to covary — PCA inevitably
concentrates variance on PC1 for such inputs. (ii) Seshat imputes
missing values using rules that smooth across variables, propagating
correlation between CCs. (iii) Several CCs are ordinal or categorical;
PCA assumes continuous metric data. (iv) Seshat oversamples
well-documented polities, which are typically complex and literate —
the "complexity" axis partly reflects "how much was written down about
this society." Follow-up work in the same research programme has been
more cautious about the strongest version of the claim.

**Why it does not give what the paper needs.** Seshat codes the Roman
Empire as roughly five polity-stages (Republic → Early Principate →
High Principate → Crisis → Dominate) at ~century resolution. No
province-level and no decadal variation. For a mixture-corrected SPA
that operates at city/province scale and decadal resolution, Seshat's
PC1 is too coarse in both spatial and temporal dimensions. Building a
Roman-Empire complexity PC1 at useful granularity from independent
time-resolved proxies (coin mint output, shipwreck frequency, building
dedications, army strength, monumental construction) would be a
substantial independent project, not a citation.

**Relationship to this paper's five-dimensional decomposition.**
Different scales of analysis. Turchin's claim is at polity × century;
this paper analyses city/province × decade. The paper's binding
identifiability constraint is already internal — five decomposition
dimensions, one observable (inscription count), one external covariate
(Hanson population) — and is stated explicitly in
`planning/research-intent.md`. Turchin 2018 is a theoretical
positioning in the comparative-historical literature, not an empirical
rebuttal of the city-scale decomposition. Whether the non-population
dimensions collapse onto a single latent factor at city scale is
empirically testable with external covariates for each dimension
(FS-A–D), but out of scope for the current paper.

**Treatment in the paper.** Three sentences in the discussion: cite
Turchin 2018 as the strongest "complexity is effectively scalar"
position in the comparative-historical literature; note that the
finding operates at polity × century scale while this paper analyses
city/province × decadal variation; flag that scale-collapse at the
city level is testable but deferred. Not a research-design constraint.

*Source:* discussion with Shawn 2026-04-24 after inspection of the
SDAM group's `quantifying_human_activity` subcollection
(key `AF78R8XB`, 12 items). The subcollection is Shawn's earlier
scan for complexity-proxy literature; most items are theoretical /
methodological rather than direct per-dimension proxies for FS-A–G.

---

## Obs 13 — 2026-04-24: Four-way convergence on sublinear β — robust methodological triangulation

The inscription-to-urban-population scaling exponent is **robustly sublinear
across four independent tests** using different datasets, regression
families, and research groups. None finds super-linear β; all fall within
a tight window [0.3, 0.7].

| Source | Dataset | Method | β | 95 % CI |
|---|---|---|---|---|
| Hanson 2021 *JUA* Table 7.3 | EDCS, 554 sites empire-wide, Rome excl. | OLS log-log, 8 pop-bins | **0.672** (mean) | [0.588, 0.756] |
| Hanson 2021 *JUA* Table 7.3 | as above | OLS log-log, 8 pop-bins | 0.654 (median) | [0.514, 0.774] |
| Hanson, Ortman & Lobo 2017 *JRS Interface* | same | OLS log-log | 0.686 (functional diversity vs pop — inscriptions as sampling frame) | SE = 0.078 |
| Carleton et al. 2025 *Nature Cities* | elite-honorific inscription proxies | Bayesian scaling | 0.3–0.5 | credible intervals |
| Ross 2024 (archived unpublished notebook) | LIRE v3.0, 816 cities with Hanson estimates | OLS log-log | 0.473 | [0.376, 0.569] |
| Ross 2024 | as above | NBR with log link, 1000-bootstrap | 0.683 | [0.532, 0.849] |

**Implication.** The sublinear pattern is robust enough that the paper
should treat it as an established empirical fact rather than a finding
to be re-established. The *explanation* of sublinearity (complexity-
markers with saturation at scale, vs Hanson's information-infrastructure
framing) remains open and is the theoretical-frame decision deferred
to RAC-TRAC 2026 audience response. The four-way convergence across
OLS, Negative Binomial, and Bayesian regression families also moots
the methodological worry that any one regression family's artefacts
drive the sublinear finding — the conclusion survives re-estimation
under different distributional assumptions.

**Critical-friend caveat.** One leg of the four-way convergence (HOL
2017 β = 0.686) is measured on **functional diversity** as the output
variable, not inscription count directly. Inscriptions are the sampling
frame for the diversity index. The finding is still sublinear and
relevant, but it is not strictly a fifth independent estimate of
"inscription count ∝ population^β" — it is a β for a related quantity
that inherits sample structure from inscriptions. The four-way framing
is supported; a hypothetical "five-way" framing would be over-counting.

*Source:* Explore-agent direct PDF verification of Hanson 2021
(`scripts/zotero.py::get_pdf_path('GHPTNHBI')` → Table 7.3 and Figures
7.4, 7.5, 7.6); Scout 2 scout-2-urban-scaling-inscriptions.md;
Ross 2024 archived notebook summarised at `planning/archive-2024-summary.md`.
Committed as theoretical-frame paragraph in
`planning/research-intent.md` (commits `d01a702`, `3e4a6f4`) and
`runs/2026-04-23-prior-art-scouts/synthesis.md`.

---

## Obs 14 — 2026-04-24 [GOTCHA]: Zotero FTS (`q=` parameter) does not index the DOI field

Discovered empirically during the 2026-04-24 batch-add of 23 papers to
the SDAM SPA collection via pyzotero (`scripts/zotero_batch_add.py`,
agent `a050742b9dd16db93`).

**Symptom.** An explicit DOI-based idempotency check (`zot.items(q=doi,
qmode='everything', limit=25)`) returned zero hits for DOIs known to be
present in the group library. The batch-add consequently created a
duplicate for Carleton, Campbell & Collard 2018 PLOS ONE — one item
(`T95BHV43`) from the single-paper test run, another (`GF82TVAB`) from
the full-batch run of the same DOI.

**Cause.** Zotero's full-text search indexes title, creator names, note
body, tag names, and attachment filenames — but **not the structured
DOI field**. A DOI string as `q=` therefore returns zero hits unless
that DOI literal appears in one of the indexed text fields. This is
the Zotero REST API's behaviour; pyzotero forwards it verbatim.

**Fix pattern.** Build a local DOI index once per operation by paging
through all items in the target library:

```python
def _build_doi_index(zot) -> dict[str, dict]:
    index = {}
    start = 0
    while True:
        batch = zot.items(start=start, limit=100)
        if not batch:
            break
        for item in batch:
            doi = item.get('data', {}).get('DOI', '').strip().lower()
            if doi:
                index[doi] = item
        start += 100
    return index
```

Then check candidate DOIs against the in-memory index before creating.
Committed in `scripts/zotero_batch_add.py` at commit `e26278e` and
extended at `6e8355b`.

**Implication for future work.** Any API-based idempotency check must
verify the API's query semantics on a known-positive case before being
trusted at scale. "Search by canonical identifier" is not a universal
pattern — different archival APIs (Zotero, Mendeley, EndNote, etc.)
index different field sets, and identifier fields are not necessarily
included. Before committing to a search-based idempotency pattern,
test it: insert (or find) a known item, query for it, verify the
result contains it.

**Why it wasn't caught in pre-launch review.** The agent brief
specified "idempotency via DOI search before create" but did not
commit to a *specific implementation pattern* for the search. The
agent picked `zot.items(q=doi)` as the obvious choice; the pre-launch
review didn't push back because the pattern name sounded correct. For
future agent briefs that rely on a safety check, specify the exact
mechanism, not just the check's goal.

*Source:* agent `a050742b9dd16db93` batch-add run 2026-04-24; root-
cause diagnosis in the agent's final report; fix committed at
`e26278e` and extended at `6e8355b`. Documented in `continuity.md`
under "Failure modes observed" and here for future reference.

---

## Obs 15 — 2026-04-26: FP-inflation diagnosis — variance-structure mismatch between observed and MC

The H1 v1 simulation's catastrophic false-positive rate (FP = 1.000 at
empire-scale n; ≥ 0.95 at province n ≥ 500) traces to a variance-structure
mismatch between the observed Sum-Probability Aggregate (SPA) and the
parametric-null Monte Carlo (MC) replicates. The observed SPA carries
aoristic-smearing variance — roughly `n × p_eb (1 − p_eb)` summed over
events, where `p_eb` is the per-bin aoristic mass — typically 5–10× larger
than `Poisson(fitted_mean)` for inscription widths around 50 y. The MC
sampler drew `Poisson(fitted_mean)` per bin independently, giving
catastrophically tight envelopes. The mismatch worsens with n: as the
observed SPA's smearing variance accumulates linearly in n, the
Poisson-on-mean MC variance accumulates only in proportion to the bin
mean, so the gap widens. Diagnostic signature: zero-effect cells with FP
elevation that scales with n, not with effect size. Fix requires matching
variance structures by forward-applying smearing in MC.

*Source:* `runs/2026-04-25-h1-simulation/outputs/REPORT.md` §4 broken-FP
table; root-cause diagnosis in `planning/decision-log.md` Decision 8
Context.

---

## Obs 16 — 2026-04-26 [PATTERN]: a "field-standard fix" can fail under domain port if the fitting space differs

The 2026-04-25 prior-art scout recommended `rcarbon::modelTest`'s
`calsample` mechanism as the canonical fix for parametric-null envelope
FP-inflation — a method standard in radiocarbon Sum-Probability
Distribution (SPD) work since Timpson et al. 2014. We implemented it
faithfully (`experiment_aoristic_mc.py::sample_null_spa_aoristic`) and FP
got *worse*: 1.000 vs 0.535 in the same cell.

Root cause: in radiocarbon, the null is fit in calendar-year space
(unsmeared); `calsample` samples calendar dates from the fit and
back-calibrates each — smearing applied **once**. For inscriptions, the
v1 null was fit on the **already-aoristic-smeared observed SPA**;
sampling synthetic event-years from this fit and re-applying empirical
widths via aoristic resampling smears each MC event **twice**. Observed
retains residual peakiness; the over-smoothed MC envelope misses it; FP
inflates to 1.000.

The pattern: when porting methodology across domains, audit the *fitting
space*, not just the algorithm. The literature does not surface this
asymmetry because radiocarbon does not have a smeared-vs-unsmeared
distinction — calibration is the only smearing step, applied once at
read-time. Promotion candidate to `~/personal-assistant/notes/llm-craft.md`
once the pattern is observed on a second cross-domain port.

*Source:* `planning/prior-art-scout-2026-04-25-aoristic-envelope.md` §8
empirical addendum; `planning/decision-log.md` Decision 8 root-cause 2.

---

## Obs 17 — 2026-04-26 [PATTERN]: a bootstrap-of-self envelope cannot detect features that exist in the corpus

The Option C non-parametric MC (row-bootstrap from filtered LIRE) PASSED
the FP-control gate empirically — mean FP = 0.033 across an 80-cell
sapphire validation grid; max 0.080; no cell > 0.10. Detection power
against injected effects on synthetic-from-corpus data was preserved.
But the test is fundamentally unable to detect features that *exist* in
the source corpus: under the bootstrap principle, observed and MC are
exchangeable when both are drawn from the same source, so a real
Antonine Plague dip or genuine growth-decline shape is, by construction,
swept into the reference distribution. Power against injected effects
≠ power against real events.

Critical-friend gate: when validating a methodology, check that the
test's null hypothesis matches the substantive question. Option C's
H0 is "is observed extreme relative to other re-bootstraps of itself?",
not "is observed extreme relative to a parametric growth model?" — fine
for H1 power calibration on synthetic data, fatal for H3b's real-data
deviation question.

*Source:* `runs/2026-04-25-h1-simulation/outputs/option-c-validation/SUMMARY.md`;
`planning/decision-log.md` Decision 8 Options Considered (Option C
rejection rationale).

---

## Obs 18 — 2026-04-26: forward-fit in true-date space resolves the variance and fitting-space problems simultaneously

The forward-fit methodology fits the parametric density `f(t; θ)` by
maximum likelihood treating each row's `[nb_i, na_i]` as the integration
range, integrating the density over the interval — no smearing absorbed
into the fit. Closed-form interval integral for exponential
(`(exp(b·na) − exp(b·nb)) / b` with `_log_diff_exp` numerical
stabilisation); per-segment trapezoidal integration for continuous
piecewise-linear (CPL). Monte Carlo: sample synthetic events from the
fitted true-date density, draw widths from the empirical width
distribution, apply uniform-position aoristic resampling **once**. Both
observed and MC now carry single-smear variance; the null is in
true-date space, so the fitting-space asymmetry is dissolved.

Pilot validation (`forward-fit-pilot/SUMMARY.md` and `SUMMARY-CPL.md`):
Part A synthetic FP mean 0.040 across 9 zero cells (0/9 > 0.10);
detection at n = 2500, 50%/50y bracket saturates at 0.99–1.00. Part B
real-LIRE FP elevated as expected (1.000 at n ≥ 2500) because real LIRE
has structure beyond a smooth exponential — this is the *signal* H3b
will detect, not a methodology failure.

*Source:* `runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/SUMMARY.md`,
`SUMMARY-CPL.md`; `planning/decision-log.md` Decision 8.

---

## Obs 19 — 2026-04-26: power simulation must draw "observed" from the null, not from the empirical corpus

The original H1 v1 implementation simulated "observed" by row-bootstrap
from real LIRE, then tested for departure from a fitted null. But under
the real H0 (no effect injected), "observed" should come from the null
data-generating process, not from the empirical distribution. The v1
loop was testing detection-of-injected-effect on data that already
contained real LIRE features (editorial spikes, Severan-era surges,
plague-period dips), so any iteration's "FP" was a mix of real-data
deviation and pure noise.

The H1 v2 corrected loop: synthetic data drawn from a specified
ground-truth null → aoristic-resampled → observed_spa → forward-fit
null → forward MC. Per Carleton, Campbell & Collard 2018's
PEWMA-framework convention, this is the only loop structure that yields
properly calibrated FP rates and unconfounded power estimates.

The v1 framing matched the prereg's English description ("simulate a
synthetic SPA under the null") but not the prereg's intent. Lesson:
prereg prose specifying "synthetic data under the null" should be
operationalised as a specific data-generating-process diagram in the
simulation code, not left to the implementer's discretion.

*Source:* `planning/decision-log.md` Decision 8 "coupled change"
paragraph; `runs/2026-04-25-h1-simulation/outputs/REPORT.md` (v1) vs
`outputs/h1-v2/REPORT-v2-final.md` (v2) comparison.

---

## Obs 20 — 2026-04-27: CPL k = 3 beats exponential on power for inscription SPA; k = 2 is structurally underfit on a 3-knot truth

In the H1 v2 final results, CPL k = 3 thresholds are 12–29 % lower than
exponential at the binding 50 % / 50 y bracket (median cpl/exp ratio 0.88;
range [0.71, 1.00]). FP control is comparable on synthetic-from-CPL data
(both methods FP < 0.05 across the zero-bracket grid). Mechanism: a more
flexible null absorbs more of LIRE's empirical shape into the null fit,
leaving cleaner residual signal for the deviation test. Reporting both
nulls characterises the shape-dependence directly — a reviewer-facing
benefit.

CPL k = 2 was dropped from the primary grid per Decision 9. Validation
evidence: k = 2 fits show systematic FP = 1.000 bias at high n on
simulations from a 3-knot ground truth (LIRE's AIC-best CPL). k = 2
is structurally underfit because two pieces cannot represent a 3-knot
shape; the misspecification cascades through the fitted MC.

AIC-select on the H1 v2 CPL iterations converges on k = 3 (73 % of
iterations) with k = 4 (27 %); the AIC-select threshold tracks the
k = 3-fixed threshold within ~50 n at H1-relevant cells, confirming that
k = 3 is the right primary and k = 4 is a useful exploratory upper
bound that does not change conclusions.

*Source:* `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`
§§4–5; `planning/decision-log.md` Decision 9 (k = 2 drop rationale).

---

## Obs 21 — 2026-04-27: step shape is harder to detect than Gaussian shape for narrow-duration peaks (counterintuitive)

Across the H1 v2 grid, narrow-duration step events are systematically
harder to detect than Gaussian events of the same magnitude × duration.
The `b_double_25y` step bracket (box-car: +5 events per 5 y bin × 5 bins,
total +25 events) is unreachable at empire and province scales across
all (null × k) combinations; the Gaussian variant (concentrated mass at
peak) is reachable at province / urban-area n ≈ 1900–2200.

Counterintuitive on first inspection: the step distributes the same
total mass over more bins, so total events are equal. But the SPA
permutation-envelope test's signal-to-noise ratio scales with **per-bin
peak height**, not with total mass — a Gaussian concentrates its mass
at the central bin, producing a sharper peak that exceeds the envelope
at fewer bins-with-larger-deviations; the step spreads its mass and
produces smaller per-bin deviations that the envelope can absorb.

Methodology caveat worth flagging in the paper: power statements about
"detect a doubling event over 25 y" are shape-dependent. Box-car events
(plague years where production halts then resumes) are statistically
harder to detect than peaked events (commemorative spikes around a
specific year) of equal total magnitude.

*Source:* `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`
§§1–2 unreachable-cell flags.

---

## Obs 22 — 2026-04-27: `c_20pc_25y` is operationally dead at urban-area scale across all (null × shape × k) combinations

The H1 v2 final results show `c_20pc_25y / urban-area` detection caps at
0.075–0.113 across all (null × shape × k) combinations even at n = 2500
(the level's max n). The 20 % / 25 y bracket reaches 0.80 detection only
in a single marginal cell (empire / cpl-3 / gaussian at n = 50 000). At
the noise floor of permutation-envelope methods on aoristic SPA at any
feasible inscription-corpus size — a property of the test, not a
methodology defect.

Decision 10 retains `c_20pc_25y` as a *preregistered hard-test boundary*
in H1 (anchors the bottom of the power curve; reviewer-facing answer to
"could you have detected smaller effects?") but removes it from the H3b
*confirmatory eligibility list*. The two roles are separable: a bracket
can be preregistered as a hard test without being preregistered as
confirmatory-eligible. H3b's confirmatory family (Holm–Bonferroni
corrected) reduces to `a_50pc_50y` and `b_double_25y` at H1-reachable
cells.

*Source:* `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`
§2 unreachable-cell summary; `planning/decision-log.md` Decision 10.

---

## Obs 23 — 2026-04-27: real LIRE has structure beyond CPL k = 4 — the H3b deviation signal is real

Forward-fit CPL on real-LIRE bootstraps (Part C diagnostic) shows
saturated FP at n ≥ 2500: 0.990 at n = 2500, 1.000 at n = 10 000, even
under k = 4. Meaning: LIRE has features beyond what 4-knot piecewise
linear can absorb — round-century editorial spikes, common-formula
artefacts, plague-period dips, and so on. This is precisely the
"deviation against a smooth null" signal that H3b is designed to
detect; it confirms that the deviation tests will have plenty to detect,
which de-risks the H3b empirical chapter.

Mechanism interpretation: CPL k ≤ 4 fits LIRE's overall growth-decline
shape (FP at n = 500 drops from 0.730 under exp to 0.170 under k = 3 —
the smooth shape is being absorbed correctly), but cannot represent the
sharper editorial-convention spikes. Going to k > 4 was deferred per
the working CPL methodology (computational cost; risk of overfitting on
the editorial spikes themselves).

*Source:* `runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/SUMMARY-CPL.md`
§3 Part C; `runs/2026-04-25-h1-simulation/outputs/optimisation/SPEEDUP.md`
revalidation table.

---

## Obs 24 — 2026-04-26 [PATTERN]: two-stage gating with hard-stop rules works for risky engineering investments

The forward-fit methodology was committed via two-stage gating:
exponential pilot first (~2–3 h focused effort with closed-form 1-D
likelihood); CPL extension only after pilot PASS. Pilot hard-stop rule:
"FP > 0.20 mean across Part A zero cells → FAIL; FP ≤ 0.10 across all
Part A zero cells AND detection ≥ 0.80 at n = 2500 for 50 %/50 y →
PASS." Observed FP mean 0.040; detection 0.99–1.00; PASS. Then proceed
to CPL (~2–3 days work; closed-form interval integrals + L-BFGS-B with
random restarts). Same hard-stop rule applied to the CPL pilot; PASS.

Pattern: cheap test before expensive commitment; clear PASS/FAIL
criteria stated *before* running; no "marginal-pass-as-pass"
negotiation when results come in. Useful for any engineering investment
> 1 day of focused work, especially when an earlier candidate fix has
already failed empirically (Option A; cf. Obs 16).

Promotion candidate to `~/personal-assistant/notes/llm-craft.md` once
the pattern recurs on a second project.

*Source:* `runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/SUMMARY.md`
§7 hard-stop check; `SUMMARY-CPL.md` §7 hard-stop check.

---

## Obs 25 — 2026-04-26: numba JIT plus a numpy refactor unlocks ~5× speedup on tight numerical kernels

Before committing to a full preregistered 1000 / 1000 H1 v2 rerun
(naive ~94 h on sapphire), the forward-fit CPL implementation was
profile-driven-optimised to 4.78× (k = 3) / 5.44× (k = 4) speedup —
median per-fit wall-time from 759 ms / 1512 ms to 159 ms / 278 ms.
Wall-time for the full preregistered run dropped from ~94 h to ~4.7 h.

Two changes carried the win:

1. **Vectorisation, low-temporary form** — pre-allocate `integrals`
   once; accumulate via `+=`; combine `mean_h` computation into a
   single expression. Drops 5 temp-array allocations per segment per
   evaluation.
2. **Numba `@njit` on the full negative log-likelihood kernel** —
   collapses ufunc-dispatch overhead. Inner-kernel µs/call: baseline
   95.1 → numpy-minimal 50.0 → numba 6.3 (k = 3); full-NLL: baseline
   132.3 → numba 28.8 (4.6×).

Lesson: don't accept "current code speed × parameters = days" without
profiling first. The optimisation budget was ~4–8 h; the saved compute
was ~89 h. Hard-stop "stop at numba" prevented Cython / C scope creep.
Analytical L-BFGS-B gradients (3–5× further speedup) are logged as
future-work if H1 v3 needs them.

*Source:* `runs/2026-04-25-h1-simulation/outputs/optimisation/SPEEDUP.md`
headline-result table and "what was changed" section.

---

## Obs 26 — 2026-04-26: group-by-interval optimisation is data-generating-process-dependent

Profiling identified group-by-`(nb, na)` as a candidate optimisation
for forward-fit CPL: compute the interval integral once per unique
dating band, then multiply by row count. **Useless for synthetic-from-null
H1 v2** — all 2500 intervals in a typical iteration have unique
`(nb, na)` pairs by construction (continuous distributions for
`t_true`, widths, and position). **Valuable for real-data bootstrap
H3a / H3b** — real LIRE bootstraps show ~5.6× clustering on
`(nb, na)` pairs (448 unique pairs out of 2500 in benchmark sampling).

Pattern: the value of a group-by optimisation is determined by the
DGP's discrete vs continuous structure, not by the method implementation.
Worth re-checking at each pipeline stage that uses the same primitive
under different DGPs. Future-work hook for the H3a / H3b real-LIRE
bootstrap analyses; `bench_quick.py` already counts unique pairs
ready for the revisit.

*Source:* `runs/2026-04-25-h1-simulation/outputs/optimisation/SPEEDUP.md`
"what was NOT changed (and why)" §(a).

---

## Obs 27 — 2026-04-26 [PATTERN]: background-agent + Bash-poll-PID handoff for long-running compute

When an agent's expected context budget is shorter than a planned
compute run's wall-time, the long-run-handoff pattern works: agent
kicks off `nohup` job on sapphire; captures PID; emits a
`run-in-progress.md` doc with monitoring commands (PID, expected
duration, output path, success criteria); exits its own context cleanly.
Main thread (or a fresh agent) polls the PID with Bash `run_in_background`,
gets a notification when the process exits, and processes the next
stage.

Used during the 2026-04-26 H1 v2 production run (~4.7 h sapphire wall);
allowed the work to span context-window boundaries without losing
progress. The pattern is general: any compute task whose wall-time
exceeds a single agent's reliable context envelope should plan the
handoff explicitly rather than hoping a single session lasts.

Promotion candidate to `~/personal-assistant/notes/llm-craft.md` once
the pattern recurs on a different project class.

*Source:* H1 v2 production-run handoff pattern, 2026-04-26.

---

## Obs 28 — 2026-04-26 [GOTCHA]: agent silent-parameter-reduction is a critical-friend gate failure pattern

Two instances observed in this sprint:

1. **H1 v1 silent DGP swap.** The v1 simulation silently row-bootstrapped
   from real LIRE instead of running the preregistered synthetic-from-null
   DGP. The agent's brief specified "simulate a synthetic SPA under the
   null"; the implementation operationalised this as bootstrap-from-LIRE
   without flagging the choice. Consequence: tested injected-effect
   detection on data already containing real-LIRE features.
2. **H1 v2 preliminary parameter cut.** The first v2 build silently
   reduced `n_iter` 1000 → 100 and `n_mc` 1000 → 200 to fit a 60 min
   wall-time cap; framed as "adequate precision". Wilson 95 % CI on a
   0.80 detection rate at n_iter = 100 is [0.715, 0.866] (width 0.151) —
   too wide for confident threshold-setting at the 0.80 boundary.

Fix pattern: agent briefs for prereg-bound work must include explicit
**HALT, do not negotiate parameters** rules with examples of what NOT
to do (no silent `n_iter` reduction; no silent DGP substitution; no
"adequate precision" framing without a CI-width calculation). The
pre-launch review must specifically check parameter values against the
prereg, not just the algorithmic structure.

*Source:* `planning/decision-log.md` Decision 8 (v1 DGP), Decision 9
Context (v2 parameter cut); session reflection 2026-04-26.

---

## Obs 29 — 2026-04-26 [PATTERN]: structured decision-log entries with context, options, decision, consequences, and revisit triggers prevent silent drift

Decisions 8, 9, and 10 — the methodological pivot, the precision-and-compute
envelope, and the c_20pc_25y disposition — were captured in the
existing ADR-style decision-log template. The structure forced
articulation of: what changed to make this a decision now (Context);
what alternatives were considered and rejected (Options); the chosen
option with one-paragraph justification (Decision); easier / harder /
committed-to / accepted (Consequences); reopen conditions (Revisit
triggers). The result is reviewer-defensible without ambiguity, and
preserves enough context that a future-Shawn re-reading the log in 18
months can reconstruct the reasoning.

The discipline is worth maintaining for any methodology choice or scope
boundary that would be defensible in writing but not obvious from the
code alone. Skip for "standard practice with no live alternative"; use
for any pivot, scope-narrowing, or compute / cost commitment.

*Source:* `planning/decision-log.md` Decisions 8, 9, 10 as worked
examples; template at the head of the file.

---

## Obs 30 — 2026-04-26: direct prereg edit + decision-log capture beats staging-amendment doc once the round has been reviewed

Two rounds of prereg amendment so far. Round 1 (2026-04-25 amendments
to §3 / §4 / §6 / §8 numerical thresholds) used a **staging document**
that batched several proposed amendments for review before any prereg
prose was touched. Round 2 (2026-04-26 forward-fit pivot) went
**direct-edit** to the prereg + Decisions 8 / 9 / 10 in the log + a
note in the prereg appendix linking to the decision log.

Both work; the trade-off is review locus.

- **Staging document** is useful for batch review of multiple
  proposals where the prereg edits are entangled and reviewing them
  together avoids reviewer thrash. Adds one round-trip.
- **Direct edit + decision-log capture** is cleaner for a single
  coherent pivot whose rationale fits in one decision-log entry.
  Removes the round-trip; the decision log is the durable record.

Preserved as pre-submission flexibility: with the prereg not yet
locked, both patterns are available. Once the prereg is OSF-locked, all
amendments will go through OSF's amendment workflow, and the
staging-document pattern likely becomes the default again.

*Source:* `planning/decision-log.md` Decisions 8 / 9 / 10 commit
sequence; comparison with the 2026-04-25 staging-document pattern in
the prereg history.
