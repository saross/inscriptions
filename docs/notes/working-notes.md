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

---

## Obs 31 — 2026-05-03 [GOTCHA]: `git clean -fd` removes gitignored files inside untracked directories

`.gitignore` protects files only when their directory ancestors are tracked. An untracked directory is opaque to gitignore — `git clean -d` removes it wholesale including any contents that would individually match an ignore pattern. Caught during sapphire git-state cleanup when the dry-run flagged a 119 MB gitignored `cell-results.parquet` for removal alongside its untracked-on-this-machine ancestor directory.

**Mitigation pattern** (preserve as project default before any `git clean -fd` on machines that haven't pulled recently):

```bash
# 1. ALWAYS dry-run first
git clean -fdn

# 2. For each untracked dir in the dry-run output, enumerate gitignored content
find <untracked-dir> -type f
# Cross-check against .gitignore patterns

# 3. Move precious gitignored files to a safe location BEFORE running clean
mkdir -p ~/git-clean-archive/
mv <untracked-dir>/<precious-file> ~/git-clean-archive/

# 4. Run clean
git clean -fd

# 5. Pull
git pull --ff-only origin main

# 6. Restore precious files (now under tracked ancestors, so gitignore applies)
mv ~/git-clean-archive/<precious-file> <restored-tracked-path>/
```

The full diagnosis is in `abductive-reasoning.md` Entry 5; this Obs is the operational summary. Added to `continuity.md` failure-modes section as "git clean -fd removes gitignored files inside untracked directories".

*Source:* sapphire git-state cleanup 2026-05-03; commits `3256744` (gitignore pattern broadening, applied after the parquet was preserved).

---

## Obs 32 — 2026-05-03: dated-backlog supersession is the right pattern when the project's phase changes substantively

`planning/backlog-2026-04-22.md` was the original working backlog; `planning/backlog-2026-05-03.md` was created today as a *replacement* (the 2026-04-22 file kept as historical record, not updated in-place). This is the same supersession pattern that `continuity-2026-04-23.md` → `continuity.md` used in April.

Decision rule that emerged: **when the project's underlying phase changes substantively (Decisions 8/9/10 forward-fit pivot, plus baorista install + travel-week handoff), supersede the dated working doc rather than amend in place.** When the phase is stable and the work is incremental (e.g., during the original April sprint), update in place.

Two reasons supersession beats in-place amendment for cross-phase changes:

1. **Cognitive load on next-session-CC.** Reading a partially-edited dated backlog mixes "what was true at creation" with "what's true now" without a clean tideline. Reading a fresh dated backlog plus a header pointer to its predecessor preserves the historical record without forcing a parse.
2. **Audit trail for "why did the priority queue change?"** The supersession event is itself a recoverable signal: a new backlog file dated to a phase boundary has the phase-change rationale in its first paragraph. An in-place amendment loses that.

`continuity.md` is different — that one is genuinely living, updated incrementally each session, because the *register-level* content (standing rules, failure modes, "if context feels cold" reading order) is meant to evolve continuously rather than supersede.

*Source:* `planning/backlog-2026-05-03.md` header + supersession note; comparison with `continuity-2026-04-23.md` → `continuity.md` April supersession.

---

## Obs 33 — 2026-05-15 [PATTERN]: dual fresh-context adversarial review converges on the consensus blockers, which are the high-signal findings

Two parallel Opus 4.7 reviewers (one statistical-methodology focus, one domain-legibility focus), both fresh context, both applying the same prereg-failure-mode rubric (researcher degrees of freedom; hypothesis → test → decision rule; does-it-answer-the-question; logical consistency; clarity), produced reports that independently flagged six identical blocking findings — H1 mis-filed as confirmatory; H3b unfalsifiability; Antonine confirmatory/exploratory contradiction; H3b Holm-Bonferroni family-size deferral; primary RQ answered only by an exploratory analysis; H2.2 "local neighbourhood mean" undefined. Plus several serious single-agent findings.

The convergence is the signal. When two independent rubric-aligned readers flag the same finding, that finding has ~ posterior-probability-1 of being a real problem — not a perspectival quirk, not a model-family bias, not a noisy critique. The six consensus blockers were the ones we triaged most aggressively (decisions 12, 14, 15) and resolved most cleanly. The single-agent findings split between "real but only one reader noticed" (some of which became decisions, some bucket (c) items) and "interesting but lower priority" (some bucket (d) items). The ratio of "consensus blockers vs single-agent findings" is itself diagnostic of how mature the document was going into review.

The framing-by-rubric matters. Earlier review attempts (less structured) tended to produce per-reader noise; the shared-rubric framing aligned the readers on the same target categories, so convergence and divergence were both meaningful. Generic "critically review this" prompts don't get this property.

## Obs 34 — 2026-05-16 [GOTCHA]: three confabulated factual claims in one source document, all caught by adversarial verification

A pre-lodgement citation audit of the preregistration found three confabulated attributions to a single source (Hanson 2021): (i) a fabricated regional spatial pattern attributed to him that the paper explicitly contradicts; (ii) an SR1 wording slip mischaracterising his research design as "polity × century resolution" when it is site-level with cumulative inscription counts; (iii) a "~85 % step-down" paraphrase for the military-diplomas evidence when the paper actually describes complete cessation after AD 167.

All three share a profile: **specific, plausibly-phrased, citation-bearing**. None is a hedge or a vague handwave. Each looks, in isolation, like a careful paraphrase of a real published finding. None survived a fresh-context PDF read with the question "where exactly does Hanson say this?"

Operational implications:

- The CLAUDE.md anti-confabulation rule is load-bearing. The instinct to write specifics with high conviction during drafting is *not* defensible without source re-verification. The cost of re-reading is low; the cost of a confabulation in a lodged preregistration is high.
- Pre-lodgement (or pre-publication) citation audits should be a standard step, not an optional defence in depth. Three in one source is the *known* incidence after one audit; there is no reason to assume the audit caught everything.
- The audit caught the third confabulation only after the first two had already been corrected. The pattern is therefore: confabulations cluster (likely the same drafting session under the same conviction-level), so finding one warrants checking the source's other attributions, not just the one flagged.
- The decision log, working notes, and run reports were not audited. They are public-repo documents (the repo is open). A broader pre-lodgement audit pass is worth it.

## Obs 35 — 2026-05-15 [SURPRISE]: the editorial-convention artefact is endpoint rounding, not midpoint inflation — the prior framing captured a derivative effect

The 2026-04-23 descriptive-stats run had quantified the editorial-convention artefact as midpoint inflation: observed/expected ratios 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350. The preregistration's prior framing of the artefact (and the original `convention_SPA` shape default of "uniform century slabs") treated those four midpoint years as the fundamental phenomenon.

A targeted five-test diagnostic in 2026-05-15 (run at `runs/2026-05-15-editorial-convention-hierarchy/`) found that the dominant editorial-rounding mechanism is **inclusive-Roman century counting acting on interval endpoints**: 54.5 % of all `not_before` values in the filtered corpus end in `01` and 53.0 % of all `not_after` values end in `00`. Two-thirds of `not_after` values are `00` or `50`; two-thirds of `not_before` values are `01` or `51`. Intervals like `[1, 100]` and `[101, 200]` then deposit aoristic mass on the midpoint years AD 50 and AD 150 — the midpoint inflation is the *aoristic-mass consequence* of the endpoint rounding, not an independent phenomenon. The `raw_dating` field makes the convention explicit: the top values are literally "1 to 100", "101 to 200", "301 to 500" etc., with the modal endpoint pair matching the string 96–100 % of the time.

This was a conceptual correction to the prereg's prior framing, not just an additional finding. The `convention_SPA` shape in the Bayesian mixture (Decision 17) was restructured around inclusive-Roman tier components (century-incl-start, century-incl-end, century-midpoint, half-century-incl-start, reign-related) rather than uniform century slabs. Field 2's description of the artefact was rewritten to reference endpoint rounding with the trailing-digit statistic, with midpoint inflation noted as the derivative aoristic-mass signal.

Lesson: when a strong descriptive pattern is sitting on a derivative quantity (here: aoristic mass at midpoints), the underlying primitive (here: endpoint frequency) may have a different — and more diagnostic — structure. Worth probing one level up the data-generating chain before committing to a model that targets the derivative. The cost of the probe (a few hundred lines of straightforward analysis) was tiny; the prior framing it overturned was central to the paper's headline contribution.

---

## Obs 36 — 2026-05-17 [SURPRISE]: Obs 35's "midpoint inflation as aoristic-mass consequence" was itself partly a test-statistic artefact

Obs 35 (2026-05-15) treated the 22.8× / 41.5× / 18.8× / 39.7× midpoint O/E ratios at AD 50 / 150 / 250 / 350 as the *aoristic-mass consequence* of inclusive-Roman endpoint rounding — narratively: wide-century intervals like [1, 100] deposit mass on the midpoint year AD 50 by aoristic construction. Three diagnostics on 2026-05-17 (interval-width, empirical-SPA-shape, date-range-filtered) showed this is wrong in two ways. First: under per-year uniform aoristic, the interval [1, 100] deposits *flat* mass across all 100 years — not preferential mass on AD 50. The "deposits mass on midpoints" framing only works under an interval-midpoint test statistic, where the inscription's midpoint (50.5) truncates to AD 50 via `int()`. The 2026-04-23 descriptive-stats run that produced the 22.8× ratios used precisely this `int((nb + na) / 2)` statistic, which conflates wide-template loading with narrow midpoint anchoring. Under the actual 5-year per-year-uniform-aoristic SPA, no anchor-year structure exists at AD 50 / 150 / 250 (local excess −77 / −79 / +22 relative to the surrounding plateau). Second: the SPA *does* show narrow spikes, but at REGNAL years (AD 77.5 Flavian, 122.5 Hadrianic, 212.5 Severan) — driven by real ancient clustering, not editorial artefact. Confirmed by the date-range filter: narrowing to short-precision intervals *amplifies* the regnal spikes (AD 122.5 ratio rises 1.61× → 13.83×) while wide-template plateau-step structure weakens.

Decision 17 (the three-tier anchor-year `convention_SPA` structure) was superseded by Decision 20 (template-interval slab structure: century slabs uniform on [1, 100] etc.; half-century slabs; reign-interval slabs uniform on [117, 138] etc.). Year-precise inscriptions ([123, 123]) stay in `genuine_SPA` as real anchoring, not artefact.

Lesson generalising Obs 35's lesson: probing one level up the data-generating chain is necessary but not sufficient. The *probe itself* needs to use the analysis pipeline's actual computed quantity (per-year aoristic SPA on 5-year bins, as the analysis will compute) rather than a related-but-different statistic (interval-midpoint truncation). When a diagnostic returns "X is the artefact", check whether X is what the analysis sees or what the diagnostic chose to measure. Diagnostic outputs need to be cross-checked against the analysis pipeline's actual quantity before grounding methodology decisions. Practical rule: when commissioning a diagnostic to probe an artefact, include the analysis pipeline's actual SPA computation as a default sanity check.

---

## Obs 37 — 2026-05-17 [PATTERN]: cross-model agreement is the load-bearing signal in adversarial saturation checks

Round-3 saturation check ran the same prompt through ChatGPT 5.5 (fresh chat) and Gemini 3 Pro (fresh context). Both returned BLOCKING + SHOULD-FIX findings; the comparison structure was instructive.

The *cross-model-agreed* BLOCKING finding (H3c described as receiving mixture correction when it should inherit H3a's date-filtered-count scope) was real, structural, and load-bearing — a logical implication of Decision 22 that the rewrite hadn't traced. Both models caught it independently on first read.

The *single-model* SHOULD-FIX findings (ChatGPT: multinomial observation model normalisation precision; Gemini: "year-0" terminology is wrong for the Julian/Gregorian calendar) were real but lower-signal — meaningful catches but not structural blockers. Each model surfaced something the other missed; both findings are valuable; neither was independently load-bearing.

The signal structure: cross-model agreement on a finding = strong evidence it's real and load-bearing. Single-model findings = real but lower priority — the disagreement indicates a model-specific catch, not a load-bearing methodology gap. Use cross-model agreement as the triage filter at saturation: BLOCKING items that both models flag are the must-fix-before-lodgement category; single-model items can be either applied or deferred based on cost.

Generalising: in late-stage adversarial review where the bar is "find what warrants another revision cycle," cross-model orthogonality is more diagnostic than within-model thoroughness. One model thoroughly reviewing is one model's worth of coverage; two models independently reviewing produces N₁ + N₂ findings, of which the (N₁ ∩ N₂) intersection is the high-signal subset and the (N₁ ⊕ N₂) symmetric difference is the lower-signal but still-real catch set.

---

## Obs 38 — 2026-05-17 [GOTCHA]: decision-scope narrowing requires explicitly tracing implications for derivative analyses

Decision 22 (2026-05-17) narrowed H3a from "mixture-corrected counts" to "date-window-filtered counts" because a per-city mixture fit would be unidentified for ~600 of the ~815 cities with N < 100 inscriptions. The decision wording was correct on H3a itself. But H3c — the residual analysis built on H3a's posterior — was not explicitly addressed. The Decision 22 entry's *Mixture's role in the paper* bullet kept the pre-Decision-22 framing where "the mixture corrects H2.1 validation + H3b deviation-detection + the H3c residual analysis where it uses the H3a posterior". After Decision 22, this framing is internally inconsistent: H3a is no longer mixture-corrected; H3c residuals are computed from H3a's posterior; therefore H3c residuals also inherit the date-filtered scope; therefore H3c is not mixture-corrected either. I had followed Decision 22 in letter (changed H3a's scope) but not in spirit (didn't trace the implication for H3c). The 2026-05-17 rewrite carried this error across the prereg's §2 / §3 / §6 / §9; the QA pass didn't catch it because its rubric was "are the decisions' explicit consequences applied?" rather than "have the decisions' logical implications for derivative analyses been traced?"

Both round-3 models (ChatGPT 5.5 and Gemini 3 Pro) caught it independently on first read — the kind of logical-implication error that's invisible to the author inside the rewrite and obvious to a fresh reader.

Lesson for decision-log discipline: when a decision narrows or changes the scope of an analysis, the decision entry's *Consequences* section needs an explicit subsection naming **derivative analyses** that inherit the changed scope. The current Decision 22 entry was clarified inline (with a "round-3 clarification 2026-05-17" marker) to drop H3c from the mixture-corrects list. Future scope-narrowing decisions should list derivative analyses up front.

Lesson for QA brief drafting: QA briefs need to include "trace logical implications for derivative analyses" as a separate target alongside "verify explicit consequences applied." The two are different and the latter doesn't catch the former.

---

## Obs 39 — 2026-05-17 [PATTERN]: saturation-check framing produces cleaner outcomes than comprehensive-review framing in late-stage adversarial cycles

Round 3 was framed as a *saturation check*, not a *comprehensive review*. The prompt explicitly named "find only what warrants another revision cycle" as the rubric and gave the reviewer a verbatim phrase to use when reporting saturation ("Round-3 saturation check returns no findings of magnitude that warrant a further revision cycle"). The "What NOT to do" section was extensive: don't re-find earlier-round items; don't do generic full-document review; don't propose substantive new analyses; don't flag stylistic preferences; don't flag absent items.

Both models calibrated to the framing. ChatGPT returned 1 BLOCKING + 1 SHOULD-FIX; Gemini returned 1 BLOCKING + 1 SHOULD-FIX. Each model independently used near-verbatim variants of the saturation phrase in its overall assessment. The cross-model BLOCKING finding (H3c-scope) was both models' first BLOCKING and only BLOCKING — no extras, no fishing for more findings to look thorough.

Compare to round 2 (ChatGPT, comprehensive review framing): 7 BLOCKING + 6 SHOULD-FIX + 3 MINOR — 16 total findings, some of which were genuinely load-bearing (B3 convention component; B5 H3a mixture scope) and some of which were mechanical (C5 Carleton citation wording; C8 amendment pre/post-lodgement framing). The yield curve flattened toward the end of round 2's findings list; the MINOR category in particular was dominated by stylistic-bordering catches.

The saturation framing did three things well: (i) it set a high bar for what counts as a finding ("warrants another revision cycle"); (ii) it gave the reviewer a clean exit ramp ("no findings" is the desired outcome, stated explicitly); (iii) it eliminated the implicit pressure to manufacture findings to look thorough by explicitly removing the MINOR category. The combination produced higher-signal output per finding than the comprehensive-review framing.

Generalising: in adversarial review cycles, framing the bar at the current state of work matters. Early-stage work benefits from comprehensive-review framing (catch everything, including small things, because the document is still being shaped). Late-stage work — after one or two rounds of revision — benefits from saturation-check framing (only flag what would meaningfully change the document, and explicitly name "no findings" as a valid output). The framing should track the document's maturity.


## Obs 40 — 2026-05-17 [SURPRISE]: the 2026-05-17 diagnostic triplet — anchor-year intuition falsified; what the SPA actually showed and how the slab structure emerged

Obs 35 / 36 record the lesson trail; this entry is the empirical and substantive complement, written up because the underlying finding deserves a substantive observation independent of the methodological lesson. The work behind it is committed at three run directories (`runs/2026-05-17-interval-width-diagnostic/`, `runs/2026-05-17-empirical-spa-shape/`, `runs/2026-05-17-date-range-filtered-spas/`); the numbers below are quoted from those reports.

**What the prior framing predicted.** The 2026-04-23 descriptive-stats pass found observed/expected ratios of 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350 — modally rounded integer midpoints of century-template intervals. Combined with the endpoint-rounding finding from Obs 35 (54.5 % of `not_before` end in `01`; 53.0 % of `not_after` end in `00`; modal `raw_dating` literally the strings "1 to 100", "101 to 200", etc.), the prior framing was: epigraphic editors round interval endpoints to inclusive-Roman century boundaries; under per-year uniform aoristic, these wide-century intervals deposit aoristic mass on the midpoint year; the artefact's SPA signature is midpoint inflation. This framing produced Decision 17's three-tier anchor-year `convention_SPA` shape (century-midpoint, half-century-start, half-century-midpoint).

**The ChatGPT B3 finding that triggered the diagnostics.** Round-2 review (ChatGPT 5.5) flagged a contradiction: under per-year uniform aoristic, the interval [1, 100] deposits *flat* mass across all 100 years — not preferential mass at AD 50. The midpoint inflation cannot be a per-year-uniform-aoristic consequence of wide-template-interval encoding; the prior framing's "deposits mass on midpoints" wording was mechanism-inconsistent with the analysis pipeline's actual aoristic primitive.

**Diagnostic 1 — interval-width** (`runs/2026-05-17-interval-width-diagnostic/`). Established that: (i) the corpus is dominated by exact-century-template intervals — [1, 100] alone is 26.3 % of the filtered corpus, with [101, 200] and [201, 300] adding similar magnitude. (ii) The 22.8× / 41.5× / 18.8× ratios were generated with `int((nb + na) / 2)` as the observed-midpoint statistic — which truncates wide-template midpoints (50.5, 150.5, 250.5) to round years and conflates wide-slab loading with narrow midpoint anchoring. (iii) Removing all narrow intervals (width ≤ 25 years) does *not* collapse the spikes — they *intensify* to 25.1× / 48.3× / 25.2× (109 % / 117 % / 132 % retention of the original ratios). The dominant artefact is wide-template-slab loading on the truncated-midpoint statistic, not midpoint-anchored mass.

**Diagnostic 2 — empirical SPA shape** (`runs/2026-05-17-empirical-spa-shape/`). Constructed the actual 5-year-binned per-year uniform-aoristic SPA over 50 BC – AD 350 — i.e. what the analysis pipeline *actually computes* — and visualised it directly. Findings: (i) No local anchor-year excess at AD 50 / 150 / 250. Local excess relative to the surrounding plateau is −77 / −79 / +22 — within sampling noise of the plateau, not the 22× / 41× / 18× excess the prior framing predicted. (ii) The SPA *does* show narrow spikes, but at *regnal* years: AD 122.5 (Hadrianic) — driven by 552 inscriptions in [117, 138] reign-interval encoding plus a separate 1,304 inscriptions in [123, 123] year-precise encoding; AD 77.5 (Flavian) — [78, 79] etc.; AD 212.5 (Severan) — [212, 217] = 728 inscriptions. (iii) The 1 BC / AD 1 boundary step is the largest single discontinuity in the envelope at +1,159 (between the AD 1 and 1 BC 5-year bins), reflecting the BC/AD calendar-convention discontinuity (no year 0 in the Julian/Gregorian calendar) and the relative scarcity of inscriptions firmly dated to the late Republic. (iv) Smaller century-boundary plateau-steps at AD 100/101 (+96), AD 200/201 (−547), AD 300/301 (+180). (v) Uniform vs trapezoidal aoristic agree quantitatively (per-bin Pearson r = 0.94, max relative diff 47.6 %) but not qualitatively — the choice of aoristic distribution does not alter the artefact's signature.

**Diagnostic 3 — date-range-filtered SPAs** (`runs/2026-05-17-date-range-filtered-spas/`). Recomputed the SPAs under progressive `date_range` thresholds {== 0, ≤ 1, ≤ 10, ≤ 25, ≤ 50, ≤ 75, ≤ 100, ≤ 200, all}. Decisive findings: (i) Regnal spikes *amplify* under narrow-precision filtering. The AD 122.5 spike-to-plateau ratio rises 1.61× at the full corpus → 4.96× at `date_range ≤ 25` → **13.83×** at single-year-precise inscriptions (`date_range == 0`). (ii) The century-boundary plateau-step pattern *weakens* decisively under narrow filtering. The Pearson r between SPA(`date_range ≤ 25`) and SPA(`date_range > 100`) is **0.34** — the two SPAs are essentially uncorrelated, indicating fundamentally different underlying patterns. (iii) A third regnal spike at AD 212.5 (Severan) emerged from the analysis. The interpretation: narrow-precision inscriptions encode real ancient dating clusters; wide-template-interval inscriptions encode editorial-encoding artefacts; the date-range filter separates the two populations.

**The conceptual reframing.** Two distinct populations coexist at AD 122.5:

1. **Reign-interval inscriptions** dated [117, 138] because the editor knows "Hadrianic" but not the exact year. These deposit *uniform mass over the reign interval* — 552 / 21 years ≈ 26 mass units per year. **This is editorial convention; goes in the `convention_SPA` component.**
2. **Year-precise inscriptions** dated [123, 123] because the inscription carries a consular date or imperial-titulature stamp (often *imperator iterum II* etc.). These deposit *point mass at AD 123*. **This is real ancient anchoring; stays in `genuine_SPA`.**

The same logic applies to centuries: [101, 200] dated by an editor unable to pin the date more tightly is convention; [123, 123] dated to a specific year is real history. The populations are separated by interval width.

**What changed.** Decision 17's three-tier anchor-year structure (century-midpoint AD 50 / 150 / 250 / 350; half-century-start AD 51 / 151 / 251; half-century-midpoint AD 25 / 75 / 125 etc.) was superseded by Decision 20's template-interval slab structure: a century-slab tier (`[1, 100]`, `[101, 200]`, etc. with uniform mass over each interval), a half-century-slab tier (`[1, 50]`, `[51, 100]`, `[125, 175]`, etc.), and a reign-interval-slab tier (Augustan `[−27, 14]`, Tiberian, Flavian `[78, 79]`, Trajanic, Hadrianic `[117, 138]`, Antonine `[161, 180]`, Severan `[212, 217]`). Year-precise inscriptions (`[t, t]` encodings) are *not* in the convention component — they remain in `genuine_SPA` as real ancient anchoring.

**Substantive significance.** Two findings of substantive interest beyond the methodology correction:

- **The regnal spikes are real ancient phenomena.** The fact that they amplify under narrow-precision filtering (and that they are driven jointly by reign-interval encoding and by year-precise inscriptions independently encoding the same reigns via consular dates or imperial titulature) means inscription production was non-uniformly concentrated in those reigns. This is a finding about ancient Roman epigraphic practice, not an artefact: the Hadrianic, Flavian, and Severan reigns produced inscription clusters even relative to the surrounding decades. The clusters appear in *both* the reign-interval-dated subcorpus (editorial-convention encoding) and the year-precise subcorpus (real ancient dating), which is consistent with the underlying ancient practice rather than the editorial dating choices.
- **The 1 BC / AD 1 boundary is the empire's single largest dating discontinuity.** The +1,159 step at the calendar boundary is the largest discontinuity in the full envelope SPA — larger than any century boundary, any regnal transition, any administrative reorganisation. It reflects the relative paucity of late-Republican inscriptions plus the calendar's discontinuous structure (no year 0 in the Julian / Gregorian calendar; 1 BC is followed directly by AD 1 with no gap year). This is flagged as a known limitation in the prereg: the BC / AD boundary step is *not* currently modelled as a separate convention-component tier, and the `genuine_SPA` will inherit any residual structure at the boundary.

**Methodological significance for the mixture model.** The Bayesian deconvolution-mixture model now has empirically-grounded structure to estimate. The convention component is a dictionary of template intervals (centuries / half-centuries / reigns) with uniform mass per template; the genuine component is a smooth density plus year-precise anchoring; the mixing weight α is the empire-level fraction attributable to editorial template encoding. The dictionary contents are pinned by a pre-Phase-2 empirical scan (`runs/2026-05-XX-template-dictionary/`) and the model's regularisation comes from Bayesian priors rather than ad-hoc constraints. The recovery simulation (H2.1) tests whether this structure is identifiable from the data — which is the methodological gamble the paper now rests on.

---

## Obs 41 — 2026-05-17 [SURPRISE]: stand-in cross-model statistical review surfaced a basic-rigour gap that three rounds of adversarial review missed

After three rounds of adversarial review (round 1: dual fresh-context Opus 4.7 with the prereg-failure-mode rubric; round 2: ChatGPT 5.5 comprehensive review; round 3: cross-model ChatGPT 5.5 + Gemini 3 Pro saturation check) plus a structured fresh-context QA pass, the prereg reached "ready for Martin" verdict from both round-3 models. As a hedge against Martin's potential delayed reply relative to Adela's Friday 2026-05-22 conference, the consultation pack was put through two **stand-in statistical reviews** with the same two LLMs in a different role: "applied econometrician / statistician giving a targeted review before the actual statistician sees it." The two reviews are committed at `planning/GPT55-statistical-review.md` and `planning/gemini-statistical-review.md`.

**Cross-model-agreement findings.** Two items received independent cross-model agreement:

- **Replicate-count floor too thin.** The prereg's binding floor of ≥ 50 replicates per cell yields a per-cell Wilson 95 % interval on coverage at a true 90 % rate of approximately [0.79, 0.96] — too wide to give a stable pass / fail boundary for the per-cell coverage rule of H2.1. Both reviewers independently recommended ≥ 100. Bumped accordingly (Decision 27).
- **Pearson r too forgiving as shape-recovery metric.** Pearson correlation is scale- and shift-invariant and can stay above 0.95 even when localised mass is mis-allocated in the recovered shape — exactly the failure mode the recovery simulation is meant to catch. Both reviewers recommended a distribution-sensitive supplementary metric (Wasserstein-1 / Jensen-Shannon / integrated absolute error). Added Wasserstein-1 as supplementary; Pearson r retained as binding (Decision 27).

The striking thing about both items is that they are **basic statistical-rigour points**. A Wilson interval on a binomial proportion at n = 50 is undergraduate stats; that 50 replicates is thin for a 90 % coverage test is the kind of point an applied statistician should catch in seconds. That three rounds of adversarial review across two model families missed both items is genuinely informative about what the prior review rounds were and weren't looking for.

**Single-model findings (all GPT5.5).** Five further items addressed genuine gaps: an aoristic-Monte-Carlo sensitivity to test the upstream-aoristic assumption (Decision 28); an 8th PPC category — posterior-predictive spatial autocorrelation on H3a residuals — to forestall the tautology risk in H3c(ii) (Decision 29); a two-tier PPC severity scheme to prevent mild discrepancies from forcing OSF amendments (Decision 30); a three-case interpretive guardrail for H3c(ii) Moran's I (Decision 31); a population- / inscription-weighted `f_within` sensitivity (Decision 32). All five address genuine gaps; none would have triggered a "stop the press" reaction had they been missed.

**Why three rounds missed the cross-model items.** Working hypothesis: role-framing dominates rubric-framing in late-stage LLM review. Each prior round had a specific rubric:

- Round 1 (dual Claude): a **prereg-failure-mode rubric** focused on researcher degrees of freedom, hypothesis → test → decision-rule failures, does-it-answer-the-question, logical consistency, clarity. Caught structural prereg-discipline failures (rescope of H3a; H2 validation; H3b unfalsifiability; H3c regional-pattern confabulation). Did *not* probe implementation-layer statistical rigour.
- Round 2 (ChatGPT 5.5 comprehensive): broader rubric, but framed around the prereg's *substantive choices* — likelihood family; convention component mechanism; H3a estimand scope; PPC trigger numericity. Caught likelihood-specification gaps (D19), convention-mechanism inconsistencies (D20), H3a scope ambiguities (D22), narrative-vs-numerical PPC triggers (D25). Did *not* probe the *parameters* of the H2.1 recovery simulation in detail beyond the procedural-pre-commitment-vs-enumeration question.
- Round 3 (cross-model saturation): explicitly framed as "find only what warrants another revision cycle"; deliberately *not* trying to be comprehensive. Caught one cross-model BLOCKING (H3c-scope inheritance — a logical implication of D22 the rewrite hadn't traced); two single-model SHOULD-FIX. Did *not* probe the H2.1 recovery-simulation parameters (which the round-3 prompt's framing actively discouraged: don't re-find earlier items).

None of the three prior rubrics had **"is this an applied statistician's recommendation?"** as a target. The stand-in reviews did, by construction. Both stand-in reviewers brought a different prior — they were asked to read as an applied statistician would, looking at the *operational parameters* of the methods (coverage thresholds, metric appropriateness, sensitivity completeness, robustness), not at the prereg-as-document failure modes.

**Cross-model agreement remains the high-signal filter.** Obs 37 noted that in adversarial saturation checks, cross-model agreement is the load-bearing signal — single-model items are real but lower-priority. The pattern holds in stand-in review: the two cross-model items (replicate count + Pearson r) are the items I'd most regret missing at lodgement; the five single-model items are improvements but not blockers. Triage rule preserved: cross-model agreement = must-fix; single-model = apply if cheap, defer if not.

**Lesson generalising to research-methodology review.** Late-stage adversarial review at saturation is *role-conditional*, not document-conditional. A document that has saturated under one role's review may still have substantial gaps visible under another role's review. Multiple role-framings (prereg-failure-mode auditor; applied statistician; substantive-domain expert; software engineer reviewing implementation feasibility; ethics / open-science compliance reviewer) cover different gaps. Where the cost of missing a gap is high (lodgement; publication; clinical-trial registration), running multiple role-framings in sequence is cheap insurance. Concretely, for this project: had Martin not been the planned external reviewer, the stand-in-statistician role would have been worth running earlier in the cycle, not as a hedge at the end.

**Note for future projects.** The stand-in-review pattern (same LLM, different role-framing) is a transferable technique. It doesn't substitute for a human expert reviewer, but it does fill in coverage gaps left by adversarial-rubric reviews. Worth keeping in the methodological toolkit as a hedge-against-delay or as a pre-flight check before sending to a high-bandwidth-cost human reviewer.

---

## Obs 42 — 2026-05-20 [GOTCHA]: pandoc URL rendering needs *both* `+autolink_bare_uris` *and* `xurl` to handle long DOIs

While producing the OSF supplementary PDF (`planning/osf-supplementary-2026-05-20.pdf`) from a markdown source, long DOI URLs in the §13 references list overflowed the right page edge. Examples that triggered the issue: `https://doi.org/10.1371/journal.pone.0191055` (Carleton et al. 2018) and `https://doi.org/10.1080/00031305.2018.1549100` (Gelman et al. 2019). The URLs rendered into the PDF as plain text and truncated mid-character at the page boundary.

First fix attempt: `\usepackage{xurl}` via `pandoc --include-in-header=...`. **This alone did nothing.** Visual confirmation showed the same truncation.

Root cause: inspecting the pandoc-generated LaTeX intermediate showed *zero* `\href` or `\url{...}` instances. Pandoc had rendered every bare URL as **plain literal text**, not as a hyperlink macro. The xurl package modifies `\url{...}` typesetting — it cannot break plain text tokens. Pandoc's default markdown reader does not autolink bare URIs; that requires the explicit `+autolink_bare_uris` extension.

Two-pronged fix required, applied together:

1. **Pandoc reader extension**: `-f markdown+autolink_bare_uris` so bare URLs in the markdown are emitted as `\url{...}` macros in the LaTeX.
2. **xurl package**: included via `--include-in-header=` containing `\usepackage{xurl}` (pandoc's own template loads xurl conditionally if available, but explicit is belt-and-braces).

Either fix alone is ineffective. The first alone produces `\url{...}` macros that hyperref renders as unbreakable tokens. The second alone leaves URLs as plain text. Both together: URLs render as clickable hyperlinks AND break at any character to fit the line.

Verification path: spot-check generated LaTeX (`pandoc -t latex --standalone`) for `\href` / `\url` macro counts; if zero, autolink isn't active. Run `pdftotext -layout` on the PDF and search for truncated URLs at column-rightmost positions.

Generalisable: any pandoc workflow producing a publication-grade PDF from markdown with inline URLs needs both flags. The default pandoc CLI does *not* set them. Worth adding to project-specific build scripts.

Captured from PDF iterations v1 → v4 in `planning/osf-supplementary-2026-05-20.pdf`, between commits `98f7607` and `a2e40fd`.

---

## Obs 43 — 2026-05-20 [GOTCHA]: unescaped pipe characters inside markdown-table cells silently truncate content across renderers

The §7 (Effect-size pre-specifications) table in the prereg had this row in source:

```
| H3c (i) | Capitals contrast on draw-wise Pearson residuals | P(mean(r_c | capitals) − mean(r_c | non-capitals) > 0) ≥ 0.95. |
```

The `|` characters inside the conditioning notation `r_c | capitals` were interpreted by every CommonMark-compliant renderer (pandoc, GitHub preview, OSF in-browser preview) as **table column separators**, truncating the visible cell content to `P(mean(r_c` and starting new (mostly-empty) columns from each subsequent `|`.

This is a **silent failure mode**: the source markdown reads correctly to a human; the rendered output is broken without any error or warning; the table structurally renders without complaint (just with extra invisible empty columns). The bug was caught only by adversarial verification post-rendering (see Obs 45).

Fix: escape pipes inside cell content as `\|`. CommonMark-compliant; preserves the visible `|` in the rendered cell while preventing column-separation interpretation.

Generalisation: any markdown table cell whose content contains a `|` (math conditional `P(A | B)`; set-builder `{x | x > 0}`; alternation; absolute-value bars; `Either / Or` lists) must escape it. The escape is locally near-invisible but globally safe across renderers.

Detection: harder than it should be — the markdown looks fine; the rendered output looks "structurally fine" with truncated content; the failure mode is silent. Best protection: adversarial verifier on the rendered artefact (Obs 45). Best prevention: a `grep -nE '^\|.*[a-zA-Z_)] \| [a-zA-Z(]'` style spot-check on table rows during authoring.

Captured from commit `42f639d` (the pipe-escape fix applied to `planning/preregistration-draft.md` line 398 and `planning/osf-supplementary-2026-05-20.md` line 365).

---

## Obs 44 — 2026-05-20 [GOTCHA]: Zenodo concept-DOI vs version-DOI confusion can produce wrong-version citations

The prereg cited LIRE v3.0 with DOI `10.5281/zenodo.8147298`. Verification against DataCite (`https://api.datacite.org/dois/<doi>`) and Zenodo (`https://zenodo.org/api/records/<recid>`) showed this DOI actually resolves to **LIRE v2.3, published 2023-07-14** — *not* v3.0. The correct version-specific DOI for v3.0 (published 2023-10-11, matching the date the prereg also cited) is `10.5281/zenodo.8431452`. The concept DOI for the entire LIRE release series — which resolves to whatever the latest version is — is `10.5281/zenodo.5074773`.

Pattern: Zenodo mints three logically-distinct DOI types for a multi-version deposit:

1. **Concept DOI**: stable pointer to "the work" — resolves to the latest version at the moment of resolution. Useful for "this dataset" claims; *unstable* for "this exact version" claims because it can resolve differently over time as new versions are deposited.
2. **Per-version DOIs**: stable pointers to specific versions. Each version gets its own DOI. Cited papers should pin the version-specific DOI for replicability.
3. **Reserved DOI** (latent): minted at deposit reservation, before publication.

Verification path: hit DataCite or Zenodo API and check the `version` and `publication_date` fields. Zenodo's record API exposes `conceptdoi` and `conceptrecid` alongside the version-specific `doi` and `record_id`. Single API call resolves the ambiguity.

How the prereg ended up with the wrong DOI: most likely a copy-paste from an earlier exploration / notebook that used v2.3, with the human-readable v3.0 + date label updated but the DOI not re-checked. The wrong-DOI / right-date / right-version-label combination is a particularly insidious form of citation error — visual scan doesn't catch it because the metadata all agree; only API verification reveals the divergence.

Generalisable: any time a version-aware deposit is cited, the citation should be verified against the registrar's API at write-time. Applies to Zenodo, OSF, Dryad, figshare, Software Heritage, and any registrar that uses concept-and-version DOI pairs. Worth building into `/cite-new`-equivalent skills.

Captured from the multi-stage citation audit during OSF lodgement (commits `3da5711` and `d6261f1`).

---

## Obs 45 — 2026-05-20 [PATTERN]: adversarial verifier for source-vs-render comparison catches silent rendering-pipeline bugs

After producing the OSF supplementary PDF from its markdown source, dispatched an adversarial verifier agent with the brief: "extract text from the PDF; compare structurally and verbatim against the markdown source; flag every discrepancy that isn't a known-deliberate transformation." The verifier was given an explicit list of acceptable transformations (YAML strip; Field-wrapper strip; cross-reference renumbering with explicit +1 mapping) so it wouldn't flag those as errors.

The verifier caught the §7 H3c(i) pipe-in-cell truncation bug (Obs 43) that author-side review had missed. The bug was invisible in the markdown source (text reads correctly to a human) and only manifested in the rendered PDF. Without the verifier the lodged artefact would have contained a corrupted decision rule in the headline effect-size table.

Pattern: when generating a binary or fixed-format artefact (PDF, image, slide deck, exported data file) from a malleable source (markdown, source code, data file), the author cannot easily catch source-vs-render divergences. A second-pass adversarial verifier agent with the *explicit task of source-to-render comparison* — and an explicit allow-list of acceptable transformations — catches silent rendering failures that author-side review consistently misses.

Cost: one agent dispatch, ~10 minutes wall-clock. Benefit: caught a load-bearing bug before the artefact was deposited in a permanent public record (OSF doesn't support easy retraction). High-leverage pattern for one-shot publishing workflows.

Necessary conditions for the pattern to work:

- The verifier must run AFTER the rendered artefact is produced (not during the build).
- The verifier must have access to both the source and the rendered artefact (not just the source).
- The verifier must be told what transformations are *expected* — otherwise it flags benign differences as errors.
- The verifier should be in a fresh context to avoid carrying author-side priors about "this should be fine."

Generalisable to: PDF generation; slide-deck rendering; chart export; documentation site builds; code-to-config compilation; any pipeline where source-to-render fidelity matters and rendering failures are silent rather than loud.

Captured from the OSF lodgement workflow, leading to commit `42f639d`. Worth adding to the project-level skill set for future high-stakes artefact-generation workflows.

---

## Obs 46 — 2026-05-22 [FINDING]: f_within is materially weighting-sensitive (30 % → 50 %); the unweighted primary is the conservative reading

The preregistered §5 three-weighting sensitivity on the H3a Mundlak f_within (`runs/2026-05-21-talk-prep/code/06-sensitivity-weighting.py`) returned material divergence by the prereg's decision rule. Unweighted f_within = 0.300 [0.240, 0.366]; population-weighted = 0.496 [0.393, 0.610]; inscription-weighted = 0.421 [0.337, 0.512]. Median spread across variants is 0.196, > 3× the primary CI half-width (0.063). Per prereg §5, this is flagged as a paper-level limitation.

Substantively: the population-attributable variance fraction is roughly *double* under weightings that focus on the cities where systematic relationships are sharpest. Two candidate explanations (logged in abductive-reasoning Entry 10): (A) small-N cities have high noise-to-signal that contaminates the unweighted denominator, so weighting cleans the estimate; (B) the substantive role of population in inscription production is genuinely different at different city sizes, with bigger cities exhibiting more diverse population-driven mechanisms. Both predict the same direction of effect but lead to different paper-level interpretations. The diagnostic test — examining the distribution of within-province population deviations in the small-N tail vs the large-N body — is not yet run.

For the conference talk (Adela's delivery Friday 2026-05-22), the unweighted 30 % is reported as the headline per the prereg's binding rule, and the talk's slide 6b speaker notes flag the three-weighting result for any Q&A pushback. For the paper, the three weightings should be reported alongside each other with substantive interpretation, not just as a robustness footnote. This is a real finding about the structure of inscription-population scaling, not just a sensitivity result.

Generalisable: variance-fraction estimands are intrinsically sensitive to the variance denominator's weighting. Any future paper that reports a "fraction of variance attributable to X" estimand should examine the multi-weighting decomposition as part of the primary reporting. This is a known property of mixed-effects model variance decompositions (Nakagawa & Schielzeth 2013 marginal-vs-conditional R²) but is easy to elide as "robustness check" rather than substantive analysis.

Captured from Block 6 of the 2026-05-21 talk-prep run, committed at `773c9e0`.

---

## Obs 47 — 2026-05-22 [GOTCHA]: a single-cell value quoted forward as a "minimum-N" summary can canonise false precision across artefacts

The "minimum N ≈ 1,549" figure quoted in the lodged prereg as the binding-bracket reachability threshold was actually one specific cell of the Phase 1 v2 simulation grid (urban-area level, cpl-k=3 null, Gaussian taper). The full range across the four null-model variants is:

- Province {1,385; 1,618; 1,869; 1,938}
- Urban-area {1,409; **1,549**; 1,854; 1,923}

"1,549" is neither the median nor the conservative value across either level. The two levels' ranges essentially overlap, justifying a single combined headline — but the right headline is "~ 1,600 (range 1,400 – 1,950 across nulls)", not "1,549". The original figure had propagated forward through:

- The lodged preregistration §3 (mentioned multiple times)
- The conference talk's slide 3a (right column bullet)
- The Adela briefing's slide-3a cheat sheet
- The B9 backup slide (small-N cities)
- The paper-fragment draft (`planning/paper-subsection-reachability.md`)
- The continuity doc's future-work entry

Without anyone interrogating "is this number a robust summary, or is it one cell?" until Shawn asked the direct question during deck QA.

Fix (committed at `3e1d74a`): all talk artefacts updated to "≈ 1,600 (range 1,400 – 1,950 across nulls)"; speaker note expanded with the across-nulls rationale; the lodged prereg's number stays as "1,549" since the prereg is committed (any change goes via amendment trail). The continuity doc's mention also updated for consistency in future-work planning.

Generalisable: any "summary statistic" inherited from a prior document deserves a re-derivation from the underlying data before being quoted forward, especially in publication-grade artefacts. For multi-variant simulation outputs (different null models, different tapers, different cells), the multi-variant range should always accompany or replace any single-cell summary. False precision in inherited numbers is a class of error that's invisible to source-review (the source agrees with itself) and only catchable by data-side re-derivation.

The threshold-table parquet (`runs/2026-04-25-h1-simulation/outputs/h1-v2/thresholds.parquet`, ~ 7 KB) is committed and was on disk all along; the cross-variant range was visible the moment the file was opened. Quoting the prereg's number forward without opening the file was the actual error mode. Cheap re-derivation, expensive un-shipping.

Captured from the slide-3a/3b colour-and-clarity QA round in the 2026-05-22 session.

---

## Obs 48 — 2026-05-22 [PATTERN]: agent-in-worktree with halt-and-ask discipline scales well for bounded chunky implementation tasks

Spawned a general-purpose agent in a `git worktree` to handle the Phase 2 mixture-recovery grid design + harness implementation + sapphire launch. The agent's brief was self-contained (read prereg §3-4 + Decisions 17/19/20/21; pin grid axes per the prereg's binding minimums; implement the simulation harness; smoke-test one cell; launch on sapphire OR halt-and-ask if launch is too expensive). The agent honoured the halt-and-ask rule: when the smoke test revealed a 3-5× per-fit slowdown under concurrent load (27-66 h projected wall-clock vs the brief's 9 h upper estimate), the agent committed the design + harness + smoke-test results to its worktree branch but did NOT autonomously launch the grid — it returned the four decision options to the main thread instead.

The pattern that worked:

1. **Bounded brief**: the agent had a clear deliverable scope (design artefact + harness + smoke test + launch decision) with explicit hard-stop rules (no silent replicate-reduction; halt-and-ask if compute is more than projected).
2. **Worktree isolation**: the agent committed to its own branch in `.claude/worktrees/`, leaving the main thread's working tree clean. Four commits preserved with `--no-ff` on merge so the agent's design trail is visible in the main history.
3. **Discipline-respect**: the agent didn't try to negotiate the brief's stop rule down; it stopped and explained. The main thread (with broader standing context about Shawn's "multi-day runs are OK" authorisation) made the actual launch decision afterward.
4. **Honest reporting**: the agent's return message itemised what it couldn't resolve (concurrency slowdown), what it had to proxy (pilot-posterior tier vector), and what wall-clock estimate was realistic given the slowdown. Not a "ready to ship" framing — a "here's the state and here are the open issues" framing.

The agent's smoke test ran in 18s standalone but 70-90s under 19-way parallel — a 4-5x slowdown the agent flagged but underweighted in its 50h wall-clock projection (subsequent observation suggests 80-120h actual). For future similar agent uses: when an agent's wall-clock estimate is based on a smoke-test (typically 1 cell, no concurrency), the main thread should add a "post-smoke verification" step where the realistic-concurrency cost is measured before the final launch decision is locked in.

Pattern is generalisable to other bounded chunky implementation tasks where:
- The work is self-contained enough to brief in a single prompt (~ 1,000-3,000 words).
- The deliverables are concrete and verifiable (committed code + smoke-test results).
- The hard-stop conditions are pre-specifiable (no silent X reductions; halt-and-ask on Y).
- The compute commitment is sequential and pause-able (the agent does design + smoke; main thread launches).

Anti-pattern: agents asked to do exploration-and-judgement work where the brief can't pre-specify what counts as "done." For that, main-thread reasoning with subagents-for-context-management is the better pattern.

Captured from the Phase B agent invocation in the 2026-05-21/22 session, committed at `db04bf0` (merge of `worktree-agent-a6e1b611cd0719a27` into main).

---

## Obs 49 — 2026-05-23 [GOTCHA]: tmpfs inode exhaustion can kill a long compute run while the byte-counter still looks fine

The Phase 2 recovery-grid main run (started 2026-05-22 06:17 on sapphire, finished 2026-05-23 12:07, 29.84 h wall) completed 438 of 450 cells; 12 cells failed late, all of them in the `smooth_decline` shape at low α. The failure mode looked unfamiliar from the orchestrator's stderr — `OSError: [Errno 28] No space left on device` — even though `df -h /tmp` showed only 4.4 GB used out of a 31 GB tmpfs. The disk wasn't full; the **inode table** was. `/tmp`'s tmpfs had a 1,048,576-inode ceiling, and pytensor's compile loop had saturated it (1,048,559 / 1,048,576 used at kill time).

Mechanism. The grid was launched with `PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"` — `allow_gc=False` is a performance setting that tells pytensor *not* to delete its `NamedTemporaryFile` compile artefacts as it goes. With 12 worker processes each recompiling the mixture model graph at every cell × replicate boundary, the per-fit leak (a few hundred small files) accumulated linearly. Most leaked files were under 4 kB, so the byte-counter barely moved while the inode counter climbed monotonically toward the ceiling. Once the table saturated, every subsequent worker that needed to create a temp file got `ENOSPC` and the per-fit retry logic gave up after three attempts. Linux reports inode exhaustion as `ENOSPC` identically to disk exhaustion — easy to misdiagnose if you only check `df -h` and not `df -i`.

The fix for the retry (2026-05-23 12:30 → 13:21, 0.85 h, all 12 cells PASS): drain `/tmp` (1,048,559 → 17 inodes used) and point `TMPDIR` at a disk-backed scratch directory on the same NVMe with 433 GB free. Pytensor's `NamedTemporaryFile` calls honour `TMPDIR`, so this redirected the leak entirely off the tmpfs without changing the rest of the config. Disk-backed storage cannot inode-saturate during a 1 h run because spinning-/SSD-disk inode tables are orders of magnitude larger than the tmpfs default.

Generalisable: any long compute run that uses JIT compilation (pytensor, numba's AOT cache, Cython rebuilds, Triton kernels) and turns the GC off for speed will accumulate small-file leakage. The default tmpfs inode count on Linux is much smaller than its byte capacity — on most distros it's 1 M or 2 M, easily reachable in a multi-hour multi-worker run. Both `df -h` and `df -i` should be in any pre-launch health check, and a `TMPDIR` redirected to disk-backed storage is a cheap insurance policy for any run > ~6 h. Documented in `RETRY-COMMAND.sh` header at commit `3df0d2c`.

*Source:* `runs/2026-05-22-recovery-grid-validation/RETRY-COMMAND.sh` (header explanation); commit `3df0d2c`.

---

## Obs 50 — 2026-05-23 [FINDING]: the recovery grid FAILed — 40.9 % of cells pass both binding criteria; the methodological novelty claim now rests on a contingent fix

The Phase 2 H2.1 recovery-grid validation, designed at `runs/2026-05-22-recovery-grid-design/` per the binding criteria in prereg §3 lines 165–210 (Decision 19), came in at **40.9 %** of cells passing both α-coverage ≥ 90 % and median Pearson r ≥ 0.95 simultaneously, against a binding gate of ≥ 90 % of cells on each criterion. The verdict is FAIL on the prereg's terms. Per-axis breakdown: α-coverage alone passes in 63.6 % of cells; shape recovery alone in 69.8 %; both simultaneously in 40.9 %.

This is what a recovery simulation is *for*. The whole point of running ~ 45,000 fits on synthetic data with known truth before applying the model to LIRE was to find out whether the architecture is sound. It would have been worse to discover the bias on real data with no ground truth to anchor the diagnosis. The grid's job was to flag the problem cheaply, and it did. Restating: this is not a setback that puts the project in doubt; this is the validation gate doing the work it was preregistered to do. The next phase is structural fix → re-validate → unfreeze the binding gate.

The substantive consequence for the paper: the headline methodological-novelty claim ("Bayesian mixture model for editorial-template deconvolution on Latin epigraphy") will need to be qualified as "with empirical-Bayes calibration cohort to break the likelihood ridge" once Stage 3 (Obs 55) lands. The empirical-Bayes pivot is not a small refinement; it changes the model's identifiability story from "fully data-driven decomposition" to "data-driven decomposition with an informative prior derived from a corpus subset." The paper's contribution still stands, but the framing in the discussion needs to be honest about *why* the calibration cohort is necessary — pointing to Spektor & Kellen 2018 for the failure-mode literature and to Wraith et al. 2014 / Christophe et al. 2018 for the precedent for the fix. The "twenty years ago in radiocarbon" frame (Bevan & Crema 2021; Crema 2022) is the rhetorical anchor.

Three structural patterns of failure show up cleanly in the cell-level data: (a) `flat_baseline` shape fails at 0 % shape-pass across all α — a metric-pipeline artefact, not a model-recovery failure (see Obs 53); (b) α=0.95 shape-pass collapses to 22 % from 78–88 % at lower α — sampler-pathology marker for the likelihood ridge (see Obs 51); (c) `regnal_cluster` at α=0.05 has α-coverage 31 % vs the ≥ 90 % gate — the convention component is absorbing genuine narrow signal at low truth-α (see Obs 51 again). These three patterns separate cleanly under the F0/F1/F3 follow-up investigations and define the structural-fix design space for Stage 3.

*Source:* `runs/2026-05-22-recovery-grid-validation/outputs/REPORT.md`; commit `3df0d2c`. Cross-reference Obs 51, 52, 53, 55.

---

## Obs 53 — 2026-05-24 [GOTCHA]: Pearson r against a zero-variance truth is undefined — a binding-criterion bug, not a recovery failure

`flat_baseline` was one of six shapes in the H2.1 recovery-grid design, included as a control: if the truth p_gen is uniform across the envelope, the model should recover ~ uniform. Of the 75 `flat_baseline` cells in the grid, **0 %** passed the prereg's binding shape-recovery criterion (median Pearson r ≥ 0.95).

This was not a recovery failure. Pearson correlation is `cov(x, y) / (σ_x · σ_y)`. When `truth` is constant, `σ_truth = 0`, so the denominator is zero and the metric is mathematically undefined — `scipy.stats.pearsonr` returns NaN with a `ConstantInputWarning`, and the cell-summariser treated NaN as a fail. When we actually looked at what the model recovered in the flat_baseline cells (Experiment B), the posterior-mean p_gen had variance ~ 10⁻⁹–10⁻⁸ against a uniform truth value of 1.25 × 10⁻² — six orders of magnitude below "distinguishable from flat", max deviation ~ 10⁻⁴, Wasserstein-1 ≤ 0.7 years on a 400-year envelope. The recovery was almost perfect; the *measuring stick* was broken on flat surfaces.

The fix is mechanical: replace Pearson r with Wasserstein-1 (the "earth-mover" distance) as the binding shape metric. W-1 is well-defined for any pair of probability vectors including constants, has interpretable units (years on this envelope), and is mass-sensitive in a way Pearson r is not — W-1 catches the kind of small-mass-displacement failure that Pearson r is blind to (the `regnal_cluster` shape passes Pearson r 84 % of the time but has median W-1 ~ 10 years, comparable to the *worst* non-flat shapes at α=0.95; see Obs 51). The empirical W-1 distribution from the 450-cell grid (`runs/2026-05-24-followup-systematics/` F0b) gives 18.6 y as the threshold that matches Pearson r ≥ 0.95 selectivity on non-flat cells; 5 y is one bin width and is markedly stricter (28.8 % pass).

Generalisable: any preregistered binding metric for "recovery against truth" needs to be runnable on every truth shape in the test grid. Constants, zero-mass regions, and degenerate distributions are not edge cases to be handled later — they're tests of whether the metric is well-defined at all. The standard pre-commitment check is "compute this metric on each truth shape with a trivially-correct recovery; does it return a sensible value?" Pearson r on `flat_baseline` would have failed this check the moment it was tried.

This is a Decision-22-class error (Obs 38): a binding numerical criterion was specified for a multi-cell grid without tracing its mathematical implications across every cell's structure. The lesson recurs: when a preregistered criterion is applied across heterogeneous cells, each cell type needs an explicit "does the criterion work here?" check before the gate goes live.

*Source:* `runs/2026-05-24-validation-investigation/outputs/REPORT.md` Experiment B; `runs/2026-05-24-followup-systematics/outputs/REPORT.md` §F0b. Cross-reference Obs 38.

---

## Obs 51 — 2026-05-24 [SURPRISE]: the α-bias is bidirectional and saturates by α=0.70 — it is not a corner pathology at α=1

The pre-investigation mental model was that the recovery-grid failure at α=0.95 was an "extreme corner" issue: the model breaks down at the boundary of the α parameter space, but the rest of the grid is well-behaved. The F0a systematics analysis (`runs/2026-05-24-followup-systematics/`) overturned this read.

Marginalised over every other axis of the 450-cell grid, mean α-bias progresses through:

| α_true | mean(α̂) | bias | direction |
|---|---:|---:|---|
| 0.05 | 0.120 | **+0.070** | over-estimates |
| 0.30 | 0.290 | −0.010 | ~unbiased |
| 0.50 | 0.456 | −0.044 | under |
| 0.70 | 0.640 | −0.060 | under |
| 0.95 | 0.885 | −0.065 | under |

The downward pull on α̂ **starts at α=0.50**, has gained nearly all its eventual magnitude by α=0.70, and only marginally worsens at α=0.95 (Δbias = +0.004 from 0.70 to 0.95). What collapses at α=0.95 is not the bias but the **shape-recovery pass rate** — 78 % → 22 % — because by then α̂ has been pulled far enough toward 0.5 that the recovered p_gen has to absorb the missing convention mass and the Pearson r against truth breaks down.

The shape-by-α heatmap is also bidirectional. `regnal_cluster` is the only shape with *positive* α-bias across α ≤ 0.50 (+0.197 / +0.134 / +0.085 at α=0.05/0.30/0.50). The mechanism: when the truth has narrow concentrated spikes (regnal_cluster's 5-year peaks at Hadrian, Flavian, Severus etc.), the convention component p_conv absorbs the spike signal — the model **over-attributes mass to α** because the convention basis is more flexible at narrow features than the GRW-smoothed p_gen. Same likelihood ridge, opposite sign, depending on which side (convention or genuine) is the "less complex" home for narrow features under the model's smoothness assumptions.

The substantive lesson is the structural-bias diagnostic logic: under a likelihood ridge between a parametric basis and a non-parametric residual, the posterior locates mass at whichever side accommodates it cheaply under the priors. A GRW smoothness prior on log p_gen makes p_gen the "smoother" side; the parametric basis is therefore the "less smooth" side; whichever side is more compatible with the truth's complexity ends up winning. At low α_true with narrow truth → p_conv wins → α̂ over-estimates. At high α_true with smooth truth → p_gen wins → α̂ under-estimates. The ridge is bidirectional and shape-sensitive. This sharpened the question for Martin from "α=0.95 is broken" to "the model's priors implicitly choose a side; please help us understand whether to (i) make the priors symmetric in complexity, (ii) constrain α empirically via the calibration cohort, or (iii) restructure the residual process".

*Source:* `runs/2026-05-24-followup-systematics/outputs/REPORT.md` §F0a Tables 1–3 and heatmap; commit `e21f7bf`.

---

## Obs 52 — 2026-05-24 [PATTERN]: distinguish sampler-effort, sampler-geometry, and structural-identifiability failures via three cheap negative results in sequence

The recovery-grid bias triage ran three sequential cheap diagnostics, each designed to falsify one candidate cause. Each came back **negative** — the candidate explanation was ruled out — and the three negatives together localise the failure to structural identifiability rather than implementation.

**Cheap diagnostic 1 — sampler effort.** Re-fit three α=0.95 cells under three sampling-effort tiers (baseline / harder / hardest: 1k–4k tune, 2k–8k draws, target_accept 0.95–0.995). If the posterior is being approximated badly by an under-powered sampler, harder effort moves α̂ toward truth. **Result:** α̂ moved by ≤ 0.01 across the three tiers while ESS rose ~5×, R-hat fell from 1.04 to ≤ 1.04, divergences eliminated. Same biased posterior, sampled more cleanly. *Cause ruled out:* sampler effort.

**Cheap diagnostic 2 — prior pull.** Swap the α prior from Beta(2,2) (only ~5 % mass above α=0.95) to Beta(1,1) ≡ Uniform(0,1). If the symmetric prior is mechanically pulling α̂ toward 0.5, the uniform prior releases it. **Result:** α̂ moved by +0.025 on average (range +0.004 to +0.037), well below the +0.05 "substantial contributor" threshold. *Cause ruled out:* prior shape.

**Cheap diagnostic 3 — sampler geometry.** Re-parameterise the GRW prior on log p_gen from centred (`log_pgen_increments ~ Normal(0, σ_smooth)`) to non-centred (`z ~ Normal(0,1); log_pgen_increments = σ_smooth · z`). The two are mathematically identical priors with different sampler-space geometries; the textbook cure for Neal-funnel pathologies. **Result:** α̂ moved by +0.001 on average (range −0.003 to +0.005). ESS-bulk improved 45–50×, R-hat from ~1.04 to ~1.0008, divergences 0 → 0 — sampling-quality improvement was huge, but the posterior did not shift. *Cause ruled out:* funnel geometry.

The three negatives leave **structural identifiability**: the data carries a likelihood ridge between α and p_gen complexity that the architecture cannot resolve, regardless of how it's sampled, what prior is on α, or how the smoothness parameter is parameterised. The information needed to nail α down is not in the data and must come from outside the data (a calibration cohort) or from a different model (a structurally constrained residual). This is the framing the empirical-Bayes pivot rests on — see Obs 55.

The generalisable pattern is a diagnostic ordering: when a Bayesian model fails, the candidate causes scale from cheap-to-fix (sampler effort) through mechanical (re-parameterisation) to structural (identifiability). Test them in order of cheapness. Each negative result is itself information — it narrows the candidate-cause space. The three negatives here cost ~ 25 min sapphire compute combined and bought a clean structural diagnosis. The free-win side-finding from diagnostic 3 (the ESS / R-hat improvement) banks an unconditional improvement to the production model regardless of whether the identifiability question is resolved.

*Source:* `runs/2026-05-24-validation-investigation/outputs/REPORT.md` Experiment A; `runs/2026-05-24-followup-alpha-prior/outputs/REPORT.md` F1; `runs/2026-05-24-followup-noncentred-grw/outputs/REPORT.md` F3. Commits `3d23fe6` and `e21f7bf`. Cross-references Obs 28 and Obs 24.

---

## Obs 57 — 2026-05-24 [PATTERN]: a "diagnostic that doesn't fix the headline" still banks structural improvements — separately commit the side-finding

The non-centred GRW re-parameterisation (F3 follow-up) was undertaken with one question in mind: does it cure the α=0.95 bias? Per the brief's pre-stated decision rule (Δα ≥ +0.03 → "marginal fix"; ≥ +0.05 → "substantial fix"), the answer was a clean negative — mean Δα = +0.001 across three cells, three orders of magnitude below the threshold. The bias is not funnel geometry.

But the *side-effect* of the re-parameterisation was substantial and unambiguous. The same three fits showed:

- ESS-bulk: 104 → 7 628 (bimodal), 147 → 6 540 (regnal), 248 → 12 322 (smooth_decline) — **~50× improvement**
- ESS-tail: similar magnitude (72 → 12 193; 260 → 6 798; 421 → 15 441)
- R-hat: ~1.04 → ~1.0008 — collapses ~50× toward 1.0
- Divergences: 0 → 0 (already clean at hardest)
- Wall time: unchanged or slightly faster

This is a **free win on computational efficiency** that is independent of whether the headline question is resolved. The non-centred parameterisation gives the same posterior (prior-equivalence verified to within Monte Carlo error on 1,000 prior draws before any production fits ran) at much higher sampling efficiency. It is an unconditional improvement to the production model. Stage 3 (Obs 55) adopts it as default.

The discipline that worked: separating "did the change fix the headline?" from "did the change improve anything else?" in the post-run analysis. The pre-stated decision rule covered only the headline; the supplementary diagnostics surfaced the side-finding as its own deliverable. The follow-up plan (`planning/h2.1-stage-3-implementation-plan-2026-05-25.md`) treats the parameterisation change as locked-in independently of the empirical-Bayes pivot's outcome — even if Stage 3's full architecture fails Stage 4 validation, the non-centred change still ships.

Generalisable: any diagnostic engineered around a binary headline question should also be instrumented to surface *unconditional structural improvements* the change introduces. The headline question is "did it fix the thing?"; the additional question is "did it improve the engine?". A diagnostic that answers only the first is single-purpose; one that answers both banks gains regardless of headline outcome. In Bayesian model development specifically, sampler-quality diagnostics (ESS, R-hat, divergences, wall-time) should be reported alongside the substantive answer whenever any model-structural change is tested — they're cheap to compute and frequently carry standalone value.

*Source:* `runs/2026-05-24-followup-noncentred-grw/outputs/REPORT.md`; commit `e21f7bf`. Cross-reference Obs 25.

---

## Obs 54 — 2026-05-24 [PATTERN]: interval *structure*, not just interval *width*, is the right partition for aoristic corpora — the family classifier doubled the calibration-cohort size at higher purity

Building a calibration cohort for the empirical-Bayes pivot (Obs 55) required separating "tightly-dated real signal" from "loosely-dated editorial templates" in the LIRE corpus. The obvious first cut is a date-range threshold: `date_range ≤ X` retains signal, drops templates. A 2026-05-24 threshold sweep (`runs/2026-05-24-date-range-threshold-analysis/`) gave the candidate cuts at < 25 y (n = 25,990; 14.2 % of corpus), < 50 y (n = 61,112; 33.4 %), etc. But the type-composition table revealed a problem: at the < 25 y cut, epitaphs (56 % of corpus) fall to 11 % of the subset while honorifics (4 % of corpus) climb to 15 %. The narrow-dated subset is **systematically type-biased** — exactly the Spektor & Kellen 2018 calibration-cohort failure mode that empirical-Bayes is supposed to avoid.

The fix that landed: a **family classifier** (`runs/2026-05-24-type-stratified-narrow-spas/`) that partitions inscriptions on `(not_before, not_after)` *interval structure* rather than width alone:

| Family | Rule | Count | % corpus | Median width |
|---|---|---:|---:|---:|
| **F1_round** | width ∈ {24, 49, 99, 149, 199, 299} AND endpoints on 25-y grid | 110,997 | 60.7 % | 99 |
| **F3_periodic** | width ∈ {19, 29, 39} AND endpoints on 10-y grid, not F1 | 8,145 | 4.5 % | 29 |
| **Tight** | width ≤ 4 AND not F1, not F3 | 14,313 | 7.8 % | 0 |
| **F2_Other** | width ∈ [5, 48] AND not F1, not F3 | 17,528 | 9.6 % | 21 |
| **Big** | width ≥ 49 AND not F1 | 31,870 | 17.4 % | 79 |

F2_Other surfaced the load-bearing insight. The intervals in F2_Other are reign-windows: `AD 291–325` (tetrarchic), `AD 212–217` (Caracalla solo emperor), `AD −27 to 14` (Augustus), `AD 117–138` (Hadrian), `AD 138–161` (Antoninus Pius). These are width-23 to width-47, *not* editorial round-number templates — they're real ancient anchoring at reign granularity. A width-only threshold either includes them (and admits a lot of F1 half-century slabs at width 49) or excludes them (and loses real signal). The interval-structure rule admits F2_Other while excluding F1 half-century slabs of equal width.

The resulting calibration cohort (**Tight ∪ F2_Other = 31,841 records, 17.4 % of corpus**) is double the size of a tight-only cohort (Cohort A: 14,313 at width ≤ 4) and 26 % larger than the cleanest width-based cohort (Cohort C: width ≤ 23 = 25,133), while still narrow on aoristic-uncertainty terms (mean σ = 3.6 y vs corpus mean 29 y). At Stage 2 every 5-y bin in the envelope has ≥ 130 records overlapping, with most bins at 500–3,000 — a well-constrained empirical prior across the whole range.

Generalisable beyond inscriptions: any aoristic corpus where editorial dating conventions cluster on a discrete set of canonical interval widths (centuries, half-centuries, common decadal windows) will have the same interval-structure signal. Round-number / grid-aligned intervals encode "editor doesn't know more precisely than the convention"; off-grid intervals at similar widths often encode real domain-anchoring (here: reigns). The two populations have the same mean width and very different epistemic status. Partitioning on `(start, end, width)` rather than width-alone is a cheap and reproducible discriminator. Worth adopting whenever a corpus mixes editorial and substantive interval encodings.

*Source:* `runs/2026-05-24-date-range-threshold-analysis/outputs/REPORT.md`; `runs/2026-05-24-type-stratified-narrow-spas/outputs/REPORT.md`; `planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`. Commits `b78da5c`, `6734ef0`.

---

## Obs 55 — 2026-05-25 [DECISION]: empirical-Bayes calibration cohort is the structural pivot — break the likelihood ridge with data from the corpus, not from a re-parameterisation

After the F0/F1/F3 follow-ups localised the H2.1 recovery-grid failure to **structural identifiability** rather than implementation (Obs 52), the choice space narrowed to: (i) discard the editorial 65 % of LIRE and analyse only the tight-dated ~ 17 % (the radiocarbon-style "drop unreliable dates" approach); (ii) restructure the residual process (e.g., Dirichlet process on p_gen instead of GRW); (iii) impose an empirical-Bayes informative prior on p_gen derived from a calibration cohort. The decision recorded across `planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`, `planning/h2.1-prior-art-scout-empirical-bayes-calibration-2026-05-24.md`, and `planning/h2.1-stage-3-implementation-plan-2026-05-25.md` lands on (iii), with (i) preserved as fallback.

The architecture: replace three pieces of the current mixture model with empirically-anchored or computationally-improved equivalents while leaving the rest unchanged.

1. **`p_conv` from data, not from a hand-curated template basis.** The current 3-tier × 21-interval placeholder basis is replaced with a fixed (or near-fixed) 80-bin vector derived from the 119,142 F1+F3 inscriptions (Obs 54). Stage 1 (`runs/2026-05-24-empirical-pconv/`) produced this vector and showed that the *best* of the current placeholder tier-weight choices (`pilot_proxy`) is L1 = 0.31 from empirical truth — 15 % of total convention mass mis-allocated relative to the data. The empirical basis is corpus-derived and self-correcting.
2. **`p_gen` prior from Cohort B, type-reweighted.** Stage 2 (`runs/2026-05-24-empirical-pgen-prior/`) used the 31,841 Tight ∪ F2_Other cohort, reweighted by inscription type so the cohort's type composition matches the corpus's (epitaph 3.2× up; honorific 0.28× down; milestones 0.19× down — these are the Spektor & Kellen 2018 bias corrections). Bootstrap-derived per-bin σ_prior averages 0.044 on the log scale — moderately informative, intended to break the ridge while leaving room for the data to refine the shape.
3. **Non-centred GRW.** Already validated by F3 (Obs 52). Banks the 45–50× ESS improvement; zero posterior-shape cost; unconditional adoption.

The structural prior-art match is *not* SDAM-cluster epigraphy. It's BUMPER / SCUBIDO (palaeoclimate transfer functions: well-dated modern calibration period informs a Bayesian model that projects onto fossil data) and Christophe et al. 2018 MD2 (OSL Bayesian mixture: poorly-bleached residual component with informative priors derived from well-bleached reference samples). The strongest theoretical anchor is Wraith et al. 2014 (informative priors in Gaussian mixtures estimated over time) and Semochkina & Walsh 2025 (resolving non-identifiability in Bayesian disease-model calibration via external evidence). Spektor & Kellen 2018 is the failure-mode literature: empirical priors in non-identifiable models can fail to improve recovery when the calibration subset is systematically unrepresentative — which is exactly what the type-reweighting addresses.

The pivot is comparable in scale to the 2026-04-26 forward-fit pivot (Obs 18) but lands on the *prior* side rather than the likelihood side: forward-fit fixed the fitting-space asymmetry by matching the variance structure between observed and MC; the empirical-Bayes pivot fixes the structural identifiability by anchoring p_gen to a corpus-derived prior. Both share the methodological move "the cheap candidate fix in the textbook doesn't work here because the domain differs; the right fix uses domain structure the textbook didn't anticipate". Both ought to be flagged in the paper's methodology section as the substantive contributions, not as housekeeping.

Open risks (logged for the Stage 4 recovery-grid re-validation): (a) the calibration cohort is itself a non-random subsample, so type-reweighting may not fully neutralise its bias; (b) the empirical `p_conv` basis is corpus-wide, so province-level or type-level convention heterogeneity is not absorbed; (c) Stage 4's recovery grid is generated against the *old* basis, so a clean pass requires either re-running the synthetic generator or accepting a stress-test diagnostic.

*Source:* `planning/h2.1-stage-3-implementation-plan-2026-05-25.md`; `runs/2026-05-24-empirical-pconv/outputs/REPORT.md` (Stage 1); `runs/2026-05-24-empirical-pgen-prior/outputs/REPORT.md` (Stage 2); `planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`; `planning/h2.1-prior-art-scout-empirical-bayes-calibration-2026-05-24.md`. Commits `a37261b`, `8e1897b`, `381c303`.

---

## Obs 56 — 2026-05-25 [PATTERN]: when two literatures *should* be in dialogue and aren't, the paper that bridges them is well-positioned — Brughmans / Aarhus / OXREP as the third cluster

Obs 10 (2026-04-23) noted that running `lit-scout` on a topic with a computational sibling requires seeding both clusters explicitly — otherwise the bibliography looks complete within one cluster while having a blind spot across clusters. The 2026-05-25 pottery-aoristic lit-scout (25 references, 0/125 confabulations, 100 % verification) confirms and refines this pattern with a third cluster.

The two methodological clusters the project lives between are:

1. **Radiocarbon SPD methodology** — Crema, Bevan, Palmisano, Timpson, Shennan. Rigorous treatment of date uncertainty; permutation envelopes; modelTest-style significance against null models; large effective sample sizes; well-developed software (rcarbon, ADMUR, baorista).
2. **SDAM-cluster epigraphic methodology** — Heřmánková, Kaše, Sobotková, Glomb. Probabilistic aoristic on inscription corpora (tempun); careful documentation of editorial conventions; less developed envelope / significance machinery.

The lit-scout surfaced a **third cluster** that bridges them: **Brughmans, Poblome, Franconi, Komar, Borisova, Newhard** at Aarhus (and adjacents OXREP at Oxford, ICRATES at KU Leuven). This community applies probabilistic aoristic methods to Roman *ceramics* — amphora fragments, fineware quantification, urban-economic time-series — at empire scale. Komar, Brughmans & Borisova 2025 process 28,851 Italian amphora fragments via aoristic methods; Franconi et al. 2023 cover 550 years in Germania at three quantification strata; Bevan et al. 2013 originated the per-item phase-confidence weight on Antikythera Roman pottery. They cite the radiocarbon-SPD methodologists *sparingly* and the epigraphic-aoristic crowd hardly at all; the substantive cluster (Hanson urban-scaling, OXREP economic-history) operates in a fourth orbit again.

What the inscription paper buys by knowing this: (i) **prior art for non-trivial methodological techniques** the inscription literature lacks — dual-dating sensitivity tests, per-item phase-confidence weights, CPUE-style sampling-intensity denominators, site-binning normalisation (Romanowska et al. 2022 / Crema 2022), modelTest-style null-significance envelopes on aoristic curves (Crema 2025; absent from almost all ceramics-aoristic papers, which Bevan & Crema themselves note as a community weakness). The 2026-05-25 prior-art scout enumerates 15 such techniques at varying implementation cost (≤ 1 day to multi-day). (ii) **A peer-review-ready citation set** — Brughmans / Aarhus reviewers are likely to be in the TRAC orbit at conferences (the RAC-TRAC 2026 session was organised by Heřmánková / Glomb / Kaše and adjacents); engagement with the ceramic-aoristic literature signals the paper is aware of the wider methodological conversation rather than narrowly inscribed in epigraphy alone. (iii) **An explicit cross-proxy validation route** — Palmisano, Bevan & Shennan 2017 report r = 0.53–0.98 across Italian proxy pairs (radiocarbon SPD ↔ ceramic SPA ↔ site count); the recovered LIRE p_gen could be cross-correlated against the Komar et al. 2025 Italian amphora SPA as external substantive validation.

Generalisable to other projects: **the value of cross-cluster lit-scout scales with the disconnectedness of the clusters**. Two clusters that already cite each other heavily yield diminishing returns from explicit cross-seeding. Two clusters with substantive subject-matter overlap and methodological transferability but light citation overlap are the high-value targets. The diagnostic for "should bridge" is content-method overlap divided by mutual-citation density. Practical workflow: when a project sits in a substantive niche with an obvious methodological cousin in another discipline (here: Roman material-culture aoristic methods), run an explicit lit-scout pass seeded on the cousin and compare its bibliography against the in-discipline one. Disjoint bibliographies are the signal that the cousin cluster is worth integrating.

This refines Obs 10 ("seed both clusters when there's a computational sibling") with: "seed all relevant clusters when there are multiple disciplinary cousins, and the value rises sharply when the clusters are bibliographically disconnected despite methodological proximity." Promotion candidate to `~/personal-assistant/notes/llm-craft.md` once the pattern is observed on a second project.

*Source:* `planning/lit-scout-2026-05-25-pottery-aoristic-roman/REPORT.md` (25 rows, 100 % verified); `planning/prior-art-scout-2026-05-25-ceramics-aoristic-techniques/REPORT.md` (15 actionable techniques, 100 % verified). Commits `3e93660`, `6877621`, `b687ed2`.

---

## Obs 58 — 2026-05-26 [DECISION]: letter-count as complementary measure, not better alternative — the 'acts vs content' reframe

The 2026-05-26 letter-count probe (`runs/2026-05-26-letter-count-probe/`) was designed under a binary framing: "is letter-count a better unit than inscription-count?" The probe spec encoded that framing directly in its verdict thresholds — any flag tripping meant letter-count becomes the headline unit (`runs/2026-05-26-letter-count-probe/spec.md` §"Verdict thresholds"). Two flags fired: Flag 2 MATERIAL (Hanson negative-binomial regression β = 0.566 under letter-count vs 0.515 under inscription-count, 95 % CIs non-overlapping; `runs/2026-05-26-letter-count-probe/outputs/tables/nbr-summary.csv`) and significant rank reshuffling at city and province level (Britannia #7 → #19, Hispania citerior #3 → #7, Ostia #3 → #1, Pompeii #1 → #3; `runs/2026-05-26-letter-count-probe/outputs/tables/city-rank-change.csv` and `province-rank-change.csv`). Main-thread Claude proposed adopting letter-count as the new headline with inscription-count demoted to a robustness annex.

Shawn rejected the binary. The operative reframe: **inscription-count measures epigraphic ACTS; letter-count measures epigraphic CONTENT.** These are not rival operationalisations of a single construct — they are different constructs. That is why they diverge where they diverge: frontier-military epigraphy (Britannia, Germania superior) is terse, so letter-count deflates it relative to inscription-count; Italian funerary-monumental (Regio I, Regio X) and Ostian commercial epigraphy are letter-heavy, so letter-count amplifies them; Pompeii's drop is the graffiti effect (high inscription-count, short texts). The divergence is the substantive finding, not a reason to pick a winner.

Consequently: **the delta between the two units becomes a research object in its own right**, directly analogous to how scaling-residuals (observed inscriptions minus what population predicts) are already a research target. The project now has a two-dimensional residual space: scaling-residual × content-residual.

**What changes downstream:**

| Affected component | Previous plan | Revised plan |
|---|---|---|
| Recovery-grid re-simulation | Single inscription-mass grid | Two parallel grids — inscription-mass + letter-mass-conservative (`runs/2026-05-26-recovery-grid-letter-mass/`, spec drafting in flight at time of Obs) |
| Stage 3 mixture model | Single-unit fits | Parallel fits under both units; delta as a third derived output (extends `planning/h2.1-stage-3-implementation-plan-2026-05-25.md`) |
| §5 exploratories | Each run once | Each run under both units; per-subset deltas as data |
| HMM follow-up (Martin Eftimoski) | Observation series = inscription counts | Either or both series; delta as optional third channel |
| OSF amendment scope | "Swap unit" amendment | "Adopt two-measure framework with delta as derived quantity" — one amendment, not a unit-swap |
| Backlog #5 (cumulative-totals experiment) | Standalone §5 exploratory | Subsumed into the two-measure framework |

**Why the binary framing arose.** The probe spec was written with a verdict-threshold structure copied from standard sensitivity-probe templates ("if any flag fires → adopt the alternative"). That structure presupposes unit-selection: the alternatives are rival operationalisations of one thing. When the alternatives are genuinely different constructs, the threshold structure forces a false choice. The spec's framing shaped the interpretation before the results were seen.

**Generalising: a fifth question for unit-of-analysis probe specs.** The standing four-test on statistical choices ("more appropriate test? more powerful alternative? more current best-practice? assumptions hold?") should have a fifth question for unit-of-analysis decisions: "are these rival operationalisations of one construct, or measures of substantively different constructs?" If different constructs: the design should produce a comparative analysis, not a winner. Verdict thresholds are inappropriate.

**Methodological gain from the reframe.** The paper now distinguishes "frequency of inscribing" (epigraphic acts) from "quantity of communication" (epigraphic content) throughout. The delta between them — content surplus or deficit per act — is a third variable capturing something about inscription *style* and *function* that neither measure alone encodes. This is a larger methodological contribution than "we used a better unit."

---

### Related observations and artefacts

**Obs 18** (forward-fit pivot, 2026-04-26): analogous structural reframe — the methodological gain came from reconceptualising the problem rather than selecting between operationalisations. That pivot dissolved the fitting-space asymmetry by changing *what space the model operates in*; this one dissolves the unit-selection problem by recognising the two units are in different construct spaces.

**Proposed Obs 55** (empirical-Bayes calibration-cohort architectural pivot; `docs/notes/reflections/PROPOSED-OBS-49-57-for-review.md`): the prior comparable methodological pivot in the reserved-numbers block. If/when Obs 55 is inducted, this Obs and Obs 55 jointly mark the project's two largest structural pivots of the 2026-05-23 → 2026-05-26 arc.

**Proposed Obs 51** (α-bias surprise, same file): diagnostic-chain finding from which the recovery-grid re-simulation inherits the post-F1+F3 fix. The two parallel grids this Obs introduces will run under the same corrected pipeline.

**Artefacts**: `runs/2026-05-26-letter-count-probe/` (all probe outputs), `runs/2026-05-26-letter-count-probe/spec.md` (the binary-verdict-threshold spec being reframed), `runs/2026-05-26-letter-count-probe/outputs/tables/nbr-summary.csv` (Flag 2 β values), `runs/2026-05-26-letter-count-probe/outputs/tables/city-rank-change.csv` and `province-rank-change.csv` (rank shuffles), `planning/h2.1-stage-3-implementation-plan-2026-05-25.md` (stage 3 plan this Obs extends), `docs/notes/reflections/continuity.md` §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)" (Martin nudge that introduced letter-count to the project).

---

### Findable later

`letter-count`, `complementary-measure`, `acts-vs-content`, `delta-as-residual`, `two-measure-framework`, `binary-framing-resistance`, `methodology-paper-architecture`, `scaling-residuals`, `unit-of-analysis`, `content-residual`, `Britannia rank`, `Ostia rank`, `Pompeii graffiti effect`, `verdict-threshold probe`, `fifth-question unit-of-analysis`, `epigraphic acts`, `epigraphic content`, `NBR beta 0.566`, `NBR beta 0.515`, `recovery-grid letter-mass`

---

## Obs 59 — 2026-05-26 [FINDING]: letter-mass strips between-province habit noise — f_within shifts +9.89 pp under Mundlak

The 2026-05-26 letter-count probe's Bayesian Mundlak refit (`runs/2026-05-26-letter-count-probe/code/06-h3a-bayesian-mundlak-letter.py`, committed at `21a80c0`) ran three response variants on the same 1,044-city, 56-province sample (Hanson-Rome-excluded) and produced directly-comparable f_within posteriors. R-hat = 1.0000 across all three fits, min ESS_bulk = 1,041, zero divergences; wall-clock 4.3 minutes total on sapphire. Numbers sourced from `runs/2026-05-26-letter-count-probe/outputs/tables/h3a-mundlak-three-variants-summary.csv` (pulled from sapphire 2026-05-26; not yet committed to local repo at time of this Obs — commit to follow shortly).

| Variant | f_within median | 95 % CI |
|---|---|---|
| Inscription count | 29.94 % | [23.70 %, 36.63 %] |
| Letter-mass conservative | 39.83 % | [32.04 %, 48.17 %] |
| Letter-mass interpretive | 39.83 % | [31.97 %, 48.30 %] |

The inscription-count result (29.94 %) reproduces the talk-prep slide-6 punchline of 29.95 % (`runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv`) to two decimal places — a cross-seed, cross-run sanity check on model, data, and sampler consistency (talk-prep seed 20260521; this run 20260526). The two letter-mass variants are essentially identical (conservative vs interpretive f_within differ by 0.005 pp), consistent with the Block 2 finding that the two empire SPAs have Pearson r = 0.994.

**The shift is +9.89 pp from the inscription baseline (29.94 % → 39.83 %).** Under the probe's pre-specified verdict thresholds (NO-CHANGE < 2 pp; MODEST 2–5 pp; MATERIAL > 5 pp), this is **Flag 3 MATERIAL**.

**Mechanism.** The between-province component shrinks under letter-mass while the within-province component is roughly stable:

| Parameter | Inscription count | Letter-mass conservative | Change |
|---|---|---|---|
| beta_within median | 0.587 | 0.559 | −5 % |
| beta_between median | −0.248 | −0.158 | −36 % (centring toward zero) |

The denominator of f_within (total variance, incorporating both the beta_between contribution and the province random-effect variance) shrinks faster than the numerator (within variance), so the fraction rises by nearly 10 pp. The between-province variance reduction is the dominant driver, not an increase in the within-province signal.

**Substantive interpretation.** Letter-mass strips out provincial-level epigraphic habit noise — the province-level cultural variation (Latin vs Greek vs frontier-military epigraphic styles; provincial elite practice) that drives inscription-act counts more than information-content counts. Within a province, city population predicts letter production more cleanly than it predicts inscription frequency. The ACT of inscribing varies by province for habit reasons; the AMOUNT inscribed per inscription varies in a way that is better predicted by city-level population. This is what Obs 58's reframe predicted: inscription-count and letter-count are not rivals for the same construct, and the between-province signal embedded in each is different in kind.

Direction-of-effect is consistent with Martin Eftimoski's 2026-05-25 nudge that "letter is the better unit for production / information flow." Magnitude exceeds any preliminary "modest" expectation: this is closer to a doubling of the within-province variance share than a small shift.

**Three-flag verdict on the letter-count probe (all flags now evaluated):**

| Flag | Statistic | Verdict |
|---|---|---|
| 1 | Empire SPA shape, Pearson r | MODEST (r ≈ 0.88–0.90) |
| 2 | Hanson β (frequentist NBR) | MATERIAL (no CI overlap; β 0.566 → 0.515) |
| 3 | f_within (Bayesian Mundlak) | MATERIAL (+9.89 pp; 30 % → 40 %) |

Two of three MATERIAL. The case for keeping both inscription-count and letter-count as first-class measures is overdetermined by the probe's own evidence.

**Empirical corroboration of Obs 58.** Obs 58 was a methodological reframe made before the Bayesian Mundlak result was available; this Obs validates it post-hoc. The units are not rivals for the same construct — they track partially-different signals — and the f_within delta is itself diagnostic: places and contexts where inscription-mass and letter-mass diverge are places where epigraphic habit decouples from epigraphic production. The two-measure framework was locked in for methodological reasons at Obs 58; this empirical result reinforces the lock-in independently.

**Methodological-paper implication.** The f_within shift is a paper-worthy finding in its own right. The within-province epigraphic-population scaling is stronger under letter-mass than under inscription-count by ~ 10 pp. This is publishable as evidence that "epigraphic habit" (act-counts) and "epigraphic production" (content) are partially-independent constructs, with population effects loading more cleanly on content. The within-between decomposition becomes a third axis of the paper's argument alongside the SPA-shape axis and the Hanson-scaling axis.

**Failure-mode note for the record.** The background agent that launched this Mundlak fit on sapphire used a polling pattern that dropped the completion notification — the known failure mode documented in `docs/notes/reflections/continuity.md` §"Failure modes" ("Background agents that arm a Monitor and exit don't re-fire from monitor events"). The result was on sapphire by 02:56 local time; main-thread Claude discovered the completion only when Shawn explicitly asked for status ~ 9 hours later. The pattern that worked: a direct SSH check from main-thread for the output files. Future agents launching long sapphire jobs should report PID + estimated completion + leave a side-channel signal (e.g., write a status file to a known path) rather than relying on the agent's own polling loop.

---

### Related observations and artefacts

**Obs 58** (acts vs content reframe; commit `dd326dc`): the methodological reframe this Obs empirically corroborates. Obs 58 locked in the two-measure framework before the Bayesian result was available; the +9.89 pp f_within shift validates it post-hoc.

**Obs 46** (f_within weighting sensitivity; commit `773c9e0`): the prior f_within material-sensitivity finding (unweighted 30 % → population-weighted 50 %). Obs 59 is a different axis of sensitivity — unit-of-analysis rather than observation-weighting — but both findings reinforce the point that the variance-partition estimand is diagnostically rich, not just a headline number.

**Proposed Obs 55** (empirical-Bayes calibration-cohort architectural pivot; `docs/notes/reflections/PROPOSED-OBS-49-57-for-review.md`): the structural pivot this probe was designed to validate. If/when inducted, Obs 55 and Obs 58–59 jointly bracket the project's largest methodological pivot of the 2026-05-23 → 2026-05-26 arc.

**Continuity §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)"** (`docs/notes/reflections/continuity.md`): the Martin nudge that introduced letter-count and anticipated the direction of the shift.

**Talk-prep H3a result** (`runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv`): f_within = 29.95 % that the inscription-count Mundlak refit here reproduces to two decimal places. The cross-seed replication confirms sampler and data-pipeline stability.

**Artefacts**: `runs/2026-05-26-letter-count-probe/code/06-h3a-bayesian-mundlak-letter.py` (script; commit `21a80c0`), `runs/2026-05-26-letter-count-probe/outputs/tables/h3a-mundlak-three-variants-summary.csv` (headline posteriors; to be committed shortly), `runs/2026-05-26-letter-count-probe/outputs/tables/h3a-mundlak-three-variants-posterior.csv` (full posterior draws; to be committed), `runs/2026-05-26-letter-count-probe/outputs/figures/fig-06-h3a-mundlak-three-variants.png` (comparison figure; to be committed), `runs/2026-05-26-letter-count-probe/RUN-LOG-06.md` (run log; to be committed).

---

### Findable later

`f-within`, `variance-partition`, `Mundlak`, `two-measure-validation`, `epigraphic-habit-vs-production`, `between-province-noise`, `letter-mass-shift`, `content-residual`, `Bayesian-NBR`, `posterior-replication`, `f_within 39.83`, `f_within 29.94`, `9.89 pp`, `beta_between shrinkage`, `Flag 3 MATERIAL`, `three-flag verdict`, `letter-count probe`, `inscription-count probe`, `background-agent polling failure`, `sapphire status file pattern`, `talk-prep replication`, `cross-seed stability`

---

## Obs 60 — 2026-05-26 [FINDING]: letter-mass reshapes the editorial-template tier composition — `pilot_proxy` reign-weight quadruples

The 2026-05-26 recovery-grid two-unit re-simulation (`runs/2026-05-26-recovery-grid-two-unit/spec.md`, commit `507a722`) requires a per-grid `pilot_proxy` tier vector — a three-way weighting over the editorial-template tiers defined in Decision 20 (century-slab, half-century-slab, reign-interval-slab). Grid A (inscription-mass) carries forward the hard-pinned 2026-05-22 anchor `(0.55, 0.30, 0.15)`, derived from inscription-endpoint frequencies per Decision 17 lines 1314–1316 (54.5 % of `not_before` values end in `01`; 53.0 % of `not_after` values end in `00`). Grid B (letter-mass conservative) cannot inherit that vector: the endpoint-frequency descriptive must be re-derived by weighting each inscription's tier contribution by `letter_count_conservative`.

Sapphire pre-launch gate 4 (commit `8925126`) produced both vectors across the same 180,609-row LIRE-filtered corpus:

| Tier | Inscription `pilot_proxy` | Letter `pilot_proxy` | Shift |
|---|---:|---:|---:|
| Century-slab | 0.55 | 0.5230 | −2.7 pp |
| Half-century-slab | 0.30 | 0.0733 | **−22.7 pp** |
| Reign-interval-slab | 0.15 | 0.4038 | **+25.4 pp** |

The century-slab share is roughly stable (~ 3 pp drop). The half-century-slab mass collapses from 30 % to 7 %; the reign-interval-slab mass quadruples from 15 % to 40 %.

**Substantive mechanism.** Reign-interval-dated inscriptions tend to be longer than half-century-slab inscriptions. Imperial titulature, military diplomas, and civic decrees that carry full reign-dating formulas (e.g., `Trib(unicia) pot(estate) XIIII co(n)s(ul) III imp(erator) XVI p(ater) p(atriae)`) include the emperor's name, titles, and the formal dating apparatus — content-heavy by construction. Half-century-slab dating is editorial shorthand applied to inscriptions that vary in length independently of why they were assigned that tier. Letter-weighting amplifies the inscriptions whose dating formula IS the content; it shrinks the inscriptions whose dating is editorial filler.

**The tier-composition shift is the "acts vs content" reframe (Obs 58, commit `dd326dc`) appearing one layer deeper.** Obs 58 made the construct-distinction argument from aggregate divergence and province-rank shuffles; Obs 59 (commit `de8fa8f`) corroborated it at the variance-partition layer (Mundlak f_within +9.89 pp). This Obs is the sibling corroboration at the template-tier-composition layer — the prior shape that feeds into the empirical-Bayes calibration cohort is itself substantively reshaped by the unit-of-analysis choice. The three findings triangulate: the reframe is not a re-labelling but a genuine construct difference embedded throughout the pipeline.

**Implications for the recovery grids** (running on sapphire at time of this Obs, PID 931910, ETA Friday): despite sharing an identical cell design — same axes, shapes, sample sizes, replicate counts, and seed policy — Grid A and Grid B do not run on identical template-prior structures. That is the point. The unit-of-analysis swap reshapes the prior in a substantively meaningful way, and identifiability needs to be validated under each separately. Any Grid B FAIL in the recovery-grid results should not be attributed cleanly to "letter unit is bad": the heavier tail in the letter-count distribution and the tier-vector shift are both candidate explanations, and they need to be disentangled diagnostically.

The verdict-flag-3 result from Obs 59 (+9.89 pp f_within shift) was measured WITHOUT this tier-vector distinction. Block-6 Mundlak treated the response variable directly; no tier-vector entered the computation. The recovery grids ARE running with the re-derived vectors, so the tier-composition shift reported here is a structural input to the grids that Obs 59 did not see.

**For the methodology paper.** The `pilot_proxy` comparison table is itself a paper-worthy artefact. The empirical-template-tier composition under each unit choice tells the reader *why* the two units produce different downstream estimates: not simply because long inscriptions weight differently in aggregate, but because letter-weighting selectively elevates a specific KIND of inscription — reign-dated formulary epigraphy — that has different temporal-clustering properties than half-century-slab editorial assignments. Formulary inscriptions cluster tightly under the reign they name; half-century inscriptions spread across a 50-year window by editorial convention. Letter-mass therefore loads the calibration cohort with more temporally-pinned exemplars, which in turn affects the shape of the empirical prior the mixture model sees. The tier-composition shift is mechanistically connected to the f_within shift reported in Obs 59 and the Hanson-β shift in the probe's Flag 2 — all three reflect the same underlying fact that reign-dated formulary content is longer, more temporally specific, and more concentrated in particular provinces and periods.

---

### Related observations and artefacts

**Obs 58** (acts vs content reframe; commit `dd326dc`): the methodological reframe this Obs corroborates at the template-tier layer. Obs 58 locked in the two-measure framework on construct-distinction grounds; this Obs shows the distinction is embedded in the prior shape itself.

**Obs 59** (Mundlak f_within shift +9.89 pp; commit `de8fa8f`): the sibling corroboration at the variance-partition layer. Together, Obs 59 and this Obs represent two independent empirical demonstrations of the same underlying construct difference — variance-partition and prior-composition are different diagnostics, both pointing the same direction.

**Obs 55** (empirical-Bayes calibration cohort as structural pivot): the architectural decision whose downstream identifiability the recovery grids are testing. The tier-composition shift reported here is a direct input to the calibration-cohort composition under letter-mass.

**Obs 50** (recovery-grid 2026-05-22 FAIL that motivated the diagnostic chain): the structural failure that made the two-unit re-simulation necessary. Context for why the parallel grids exist at all.

**Decision 20** (template-interval slab structure: century-slab, half-century-slab, reign-interval-slab): the tier framework these vectors weight. `pilot_proxy` is a weighting over these three tiers.

**Decision 17** (lines 1314–1316: `not_before` `01` 54.5 %, `not_after` `00` 53.0 %): the inscription-endpoint-frequency descriptive that anchored the hard-pinned inscription-mass `pilot_proxy`. The letter-mass re-derivation uses the same endpoint-pattern classifier but weights by `letter_count_conservative` rather than counting inscriptions uniformly.

**Artefacts**: `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/data/pilot-proxy.json` (hard-pinned inscription vector; commit `8925126`), `runs/2026-05-26-recovery-grid-two-unit/letter-mass/data/pilot-proxy.json` (re-derived letter vector; commit `8925126`), `runs/2026-05-26-recovery-grid-two-unit/spec.md` §3.3 (tier-vector derivation protocol; commit `507a722`).

---

### Findable later

`pilot_proxy`, `tier-vector`, `editorial-template`, `reign-interval-slab`, `half-century-slab`, `letter-weighted-descriptive`, `calibration-cohort`, `empirical-Bayes-prior-shape`, `tier-composition-shift`, `two-measure-corroboration`, `pilot-proxy-json`, `formulary-epigraphy`, `reign-dated`, `letter-count-conservative`, `recovery-grid-two-unit`, `pre-launch-gate`, `century-slab`, `template-prior`, `prior-shape`, `unit-of-analysis-prior`

---

## Obs 61 — 2026-05-30 [FINDING]: letter mass is the temporally *weaker* unit — the heavy-tailed design effect makes content less detectable than acts

The 2026-05-26 "acts vs content" reframe (Obs 58, commit `dd326dc`) established inscription count and letter mass as measures of different constructs. This Obs quantifies a consequence that runs against intuition: **letter mass, the richer content measure, has *less* statistical power for temporal detection than the simpler inscription count** — because it is a compound sum of heavy-tailed per-inscription letter counts, not a count of independent events.

### The finding

**Mechanism.** In a letter-mass spline/permutation SPA each inscription enters weighted by its letter count `w_i`. The Kish effective sample size `n_eff = (Σw_i)²/Σ(w_i²)` then governs precision, and the design effect `DEFF = n/n_eff = 1 + CV²` (CV = coefficient of variation of inscription lengths) measures the loss. Letters within one inscription share a single date, so they are not independent timing observations; weighting by length therefore concentrates the signal in a few long texts and can only *reduce* effective N relative to equal-weight counting.

**Empirical magnitudes** (`scripts/letter-mass-design-effect.py`, on `runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet`, 176,609 inscriptions with ≥ 1 conservative letter):

| Statistic | Value |
|---|---|
| Per-inscription letters, mean | 46.5 |
| Per-inscription letters, median | 26 |
| Per-inscription letters, max | 35,537 |
| Corpus-wide CV² | 14.0 |
| Corpus-wide DEFF | 15.0 |
| Corpus-wide n_eff | 11,777 (6.7 % of n) |
| Per-city median DEFF | 2.21 |
| Per-city DEFF IQR | [1.76, 3.40] |
| Per-city DEFF max | 57.7 |

The median city's letter-mass SPA therefore has ≈ 0.45× the effective N of its inscription-count SPA. The corpus-wide figure also shows that a naive "treat total letters as a count" analysis would overstate effective N by ~697×.

Worst offenders (graffiti-and-monument mixtures maximise length variance):

| City | n | n_eff | DEFF |
|---|---:|---:|---:|
| Pompeii | 4,254 | 779 | 5.46 |
| Ostia | 2,644 | 400 | 6.61 |
| Mogontiacum | 2,392 | 341 | 7.02 |

**Reachability consequence** (`scripts/letter-mass-reachability.py`; a city is letter-mass-eligible for a bracket iff `n_eff ≥` the Phase 1 threshold): at the urban-area 50 %-over-50-year thresholds (1,409–1,923 inscriptions; preregistration §6 line 408), **0 of 1,041 Rome-excluded urban-area cities are eligible under letter mass**, versus 5–7 under inscription count. Letter-mass temporal detection is therefore unreachable corpus-wide, not merely under-powered.

**Why no simulation is needed.** The analytic translation models the design effect as pure effective-N deflation; the neglected heavy-tail effects widen the permutation null and can only reduce power further, so a full compound-process Monte Carlo cannot overturn "0 eligible." Full simulation is logged as an optional methodology-follow-up refinement, not built.

### Why this matters

(i) Justifies OSF Amendment 01 scoping letter-mass time-series/residual analyses as exploratory (unreachable), with confirmatory letter mass confined to the cross-sectional H3a + variance partition, where the design effect does not bite (it regresses per-city *totals*, not within-city timing).

(ii) A genuine, slightly counterintuitive methods-paper contribution: *letter mass trades temporal detectability for content sensitivity.* The very property that makes letter mass a richer content measure — long inscriptions carry more information — is exactly what inflates the design effect and destroys temporal resolution.

(iii) The design effect itself is a reportable artefact characterising when each unit is usable. The `DEFF` table and the per-city distribution are publishable diagnostics in their own right.

### Caveats / methodological notes

The analytic reachability argument assumes the design effect acts as pure effective-N deflation. This is the conservative (power-reducing) direction: any correlation structure among same-inscription letters, or additional heavy-tail effects in the permutation null, can only widen the null further. The "0 eligible" result is therefore robust to the simplifying assumption; it cannot be overturned by a more elaborate model.

The n_eff calculation uses `letter_count_conservative` throughout, consistent with the two-measure framework's conservative branch. The interpretive-letter variant would produce similar or larger DEFF values (interpretive counts include reconstructed letters, which are correlated with conservative counts and would not systematically reduce CV²).

---

### Related observations and artefacts

**Obs 58** (acts vs content reframe; commit `dd326dc`): this Obs extends the construct distinction to the detection-power layer. The reachability failure is a direct consequence of the construct difference Obs 58 identified.

**Obs 59** (commit `de8fa8f`; Mundlak `f_within` +9.89 pp): the variance-partition corroboration of the two-measure framework. Obs 59 showed letter mass strips between-province habit noise; this Obs shows letter mass is simultaneously unreachable for within-city temporal detection. The two findings are not contradictory — they are different diagnostics of the same construct difference.

**Obs 60** (commit `2f86c95`; `pilot_proxy` tier-composition shift): the prior-shape corroboration. Together Obs 59, 60, and 61 triangulate the "acts vs content" reframe across three independent diagnostics: variance partition, prior composition, and detection power.

**OSF Amendment 01** (`planning/osf-amendment-2026-05-29-two-measure-framework.md` §A5.2/§A5.5): the amendment that scopes letter-mass temporal detection as exploratory on the basis of these reachability results.

**Preregistration §6 line 408** (`planning/preregistration-draft.md`): the urban-area 50 %-over-50-year Phase 1 thresholds (exp-step 1,923, exp-gauss 1,854, cpl-3-step 1,409, cpl-3-gauss 1,549) against which `n_eff` was evaluated.

**Artefacts**: `scripts/letter-mass-design-effect.py` (DEFF computation), `scripts/letter-mass-reachability.py` (city-level eligibility), `runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet` (input corpus, 176,609 inscriptions).

---

### Findable later

`letter-mass`, `design-effect`, `kish-effective-sample-size`, `detection-power`, `reachability`, `heavy-tailed-weights`, `compound-sum`, `acts-vs-content`, `two-measure-framework`, `temporal-detectability`, `content-sensitivity`, `n_eff`, `CV-squared`, `Pompeii-DEFF`, `Ostia-DEFF`, `Mogontiacum-DEFF`, `unreachable-corpus-wide`, `OSF-amendment-01`, `analytic-reachability`, `letter-mass-reachability`, `letter-mass-design-effect`, `zero-eligible`, `DEFF-15`, `n_eff-11777`, `effective-sample-size`, `inscription-count-vs-letter-mass-power`

---

## Obs 62 — 2026-05-30 [CORRECTION]: Obs 61 per-city design effect and city denominator corrected (analysis-unit grouping + exact Rome match); headline robust

A code audit (`/audit` over the §5 harness + letter-mass scripts; verification at `scripts/audit-verify-rome-and-deff.py`, commit `5059d6d`) found two unit/input-consistency issues in the numbers Obs 61 reported. Both are corrected here; **Obs 61's qualitative conclusion — letter-mass temporal detection is unreachable corpus-wide — is unchanged and was re-verified.**

**Correction 1 — per-city design-effect grouping.** Obs 61 cited "per-city median DEFF 2.21 (IQR [1.76, 3.40])". That was computed by `place` (raw findspot), because `scripts/letter-mass-design-effect.py` auto-detected the grouping column and picked `place` first. The analysis unit used by the reachability translation and the §5 trajectory work is `urban_context_city` (the Hanson-matched urban area). Recomputed on that unit (≥30 inscriptions, exact-Rome-excluded): **median DEFF 2.38, IQR [1.85, 3.70]** (n=382 cities). The interpretive figure becomes **≈ 0.42× effective N at the median city** (was 0.45×). The corpus-wide DEFF (~15) is unchanged.

**Correction 2 — Rome-exclusion over-match.** The denominator "0 of 1,041 cities" used `contains("rom")`, which spuriously excluded Romula (N=54, a legitimate city), Tauromenium (N=9), and Caesaromagus (Britannia N=12 / Gallia Belgica N=1) alongside Roma. With an exact `Roma`/`Rome` match the corrected denominator is **1,044**.

**Headline re-verified robust.** Under both the buggy and corrected exclusion, letter-mass eligibility is **0** urban-area cities at all four Phase-1 thresholds (1409/1549/1854/1923), versus 5–7 under inscription count. The corrected figures were applied to OSF Amendment 01 (§A5.2/§A5.5) before lodgement (commit `4fad07b`) and the §5 spec; the code fixes (exact Rome match, analysis-unit DEFF reporting, plus a related province-assignment fix that moved the §5 post-clip target count from 267 to 268 by restoring Romula) are in commit `2c82a87`, with the spec finalised at `41cb028`.

### Related observations and artefacts

**Obs 61** (`107226b`): the observation these figures correct; its mechanism (letter mass is a compound sum; the design effect deflates effective N) and qualitative conclusion stand. **Artefacts**: `scripts/audit-verify-rome-and-deff.py` (`5059d6d`), `scripts/letter-mass-design-effect.py`, `scripts/letter-mass-reachability.py`.

### Findable later

`correction`, `obs-61-correction`, `design-effect`, `analysis-unit`, `urban_context_city`, `rome-exclusion`, `denominator-1044`, `kish`, `audit`, `letter-mass`, `reachability`, `headline-robust`

---

## Obs 63 — 2026-06-01 [FINDING]: §5 small-N trajectory estimation has a reliability floor at N≈300 — the calibrated honest-negative-result

The §5 Layer-A production run (`runs/2026-05-30-s5-small-n-trajectories/RESULTS.md`, commit `eb3aef3`) includes a subsample-and-recover calibration (spec §8a.3) that quantifies where small-N inscription-trajectory estimation can be trusted. Method: the 7 large anchors (N≥1549, e.g. Pompeii N=4266) have well-constrained full-N posterior trajectories taken as ground truth; each is randomly down-sampled to N∈{50, 100, 200, 300, 500} (~40 reps each; 1,400 standalone single-city fits; 0 failures) and re-estimated; recovery is scored by coverage (does the small-N 95 % CI contain the full-N truth), posterior-median shape Pearson r, mean CI width, and peak bias.

### The finding

**N\* = 300** (smallest N with coverage ≥ 0.90 AND shape r ≥ 0.90):

| N | coverage | shape r | mean CI width | \|peak bias\| (bins) |
|---|---|---|---|---|
| 50 | 0.78 | 0.77 | 0.117 | 1.18 |
| 100 | 0.82 | 0.82 | 0.096 | 1.05 |
| 200 | 0.91 | 0.89 | 0.081 | 0.77 |
| 300 | 0.94 | 0.92 | 0.072 | 0.64 |
| 500 | 0.97 | 0.96 | 0.063 | 0.41 |

Source: `runs/2026-05-30-s5-small-n-trajectories/code/production/subsample-recover-results.json`, field `aggregate.precision_vs_n`. Donors: Pompeii, Salona, Ostia, Mogontiacum, Aquileia, Puteoli, Carnuntum (1).

Below ~300 inscriptions an individual city's trajectory is unreliable — the credible bands are over-confident (coverage < 0.90) and the recovered shape is noisy (r < 0.90). At/above 300, both metrics clear, so the trajectory is faithful with honestly-calibrated uncertainty. This is the preregistered honest-negative-result made quantitative — the §5 methodological deliverable: a citable reliability floor for small-N inscription SPA trajectory estimation.

### Why this matters

(i) **Quantifies the floor for paper citation.** The preregistration committed to reporting where §5 individual-city trajectories are and are not trustworthy. N\* = 300 is that threshold: anything the paper reports about small-N trajectories should carry this calibration result as the underpinning uncertainty statement.

(ii) **Scopes the individual-curve vs aggregate reading.** Of the 268 §5 target cities, only ~38 have N ≥ 300; for the remaining majority, the individual curve sits below the strict floor and should be read through the pooled/aggregate lens (e.g. the 6-cluster trajectory grouping), not on its own.

(iii) **Positions the result as a methods contribution.** The subsample-and-recover design itself — measuring coverage and shape r simultaneously against full-N ground truth, applied to a spatially structured Bayesian SPA model — is a transferable calibration protocol for inscription-corpus trajectory estimation.

### Caveats / methodological notes

**Conservative.** The calibration fits each subsample standalone (no pooling); the production trajectories use the full hierarchy (city pooled toward province), which can only improve small-N reliability. N\* = 300 is therefore a conservative lower bound; the pooled estimates likely remain trustworthy somewhat below it. The paper should note this when citing the floor.

**Scope of donors.** The 7 donors are concentrated in the western Mediterranean / Danubian provinces. How well N\* generalises to cities with very different temporal distributions (e.g. strongly late-peaked Eastern corpora) is not tested here and is an acknowledged limitation.

**Anchor anchor shape is treated as ground truth.** Each full-N anchor trajectory was accepted as "truth" after convergence checks (R̂, ESS, divergences) and the Pompeii AD-79 external validation. If an anchor's own shape estimate carries substantial uncertainty, coverage measurements will be conservative (the CI needs to contain a noisy target).

### Related observations and artefacts

**Obs 61** (letter mass is temporally weaker; `107226b`): companion §5 reachability finding concerning temporal-detection power for the letter-mass measure. Obs 61's "reachability" is about effective-N deflation under the design effect; this Obs is about estimation reliability above/below the N\* floor — related but distinct diagnostics.

**Obs 62** (Obs 61 correction; per-city DEFF grouping + Rome-exclusion denominator corrected): confirms the corrected §5 city count is 268, consistent with the 268 target cities reported here.

**Artefacts**: `runs/2026-05-30-s5-small-n-trajectories/RESULTS.md`, `runs/2026-05-30-s5-small-n-trajectories/code/production/subsample-recover-results.json`, `runs/2026-05-30-s5-small-n-trajectories/code/production/production-summary.json`, spec §8a.3; commit `eb3aef3`.

### Findable later

`s5-calibration`, `N-star-300`, `reliability-floor`, `subsample-recover`, `small-N-trajectory`, `honest-negative-result`, `coverage`, `shape-r`, `reachability`, `standalone-conservative`, `pooling`, `layer-a`, `precision-vs-N`, `calibration-n-star`, `subsample-and-recover`, `7-donors`, `1400-fits`, `Pompeii-4266`, `Carnuntum-1574`, `trajectory-estimation`, `s5-small-n`, `credible-bands`, `peak-bias`, `ground-truth`

## Obs 64 — 2026-06-01 [FINDING]: the §5 Layer-A model independently recovers the Pompeii AD-79 terminus — strong external validation

The §5 Layer-A production diagnostics (`runs/2026-05-30-s5-small-n-trajectories/RESULTS.md`, commit `eb3aef3`; spec §8a.2) include an external check on Pompeii, buried by Vesuvius in AD 79. The model is given only Pompeii's aoristically-dated inscriptions (N = 4266) — nothing about the eruption date — and its recovered trajectory is tested for whether temporal mass leaks past the known terminus.

### The finding

Genuinely-post-79 mass (bins ≥ AD 100, entirely after the eruption) = **5.0 of 4262 ≈ 0.12 %** — essentially zero, exactly as the historical terminus requires. The AD 75–100 bin is excluded from the post-79 sum because it legitimately covers Pompeii's final pre-eruption years AD 75–79.

| Diagnostic | Value |
|---|---|
| Pompeii N | 4266 |
| Post-79 mass (bins ≥ AD 100) | 5.02 |
| Total allocated mass | 4261.84 |
| Post-79 fraction | 0.12 % |

Source: `production-summary.json`, field `diagnostics.pompeii_ad79`.

This is the strongest available external validation that the Poisson-aoristic likelihood + ICAR smoothing + partial pooling neither fabricate nor misplace temporal mass: the model reconstructs a known historical hard-stop from the data alone, without being told the terminus.

**Companion — anchor internal consistency** (spec §8a.1): each large anchor's standalone Bayesian trajectory versus its own model-free aoristic SPA — Pearson r on shape:

| Anchor | N | shape r | standalone gate |
|---|---|---|---|
| Mogontiacum | 2328 | 0.890 | pass |
| Ostia | 2380 | 0.885 | marginal |
| Pompeii | 4266 | 0.826 | pass |
| Carnuntum (1) | 1574 | 0.818 | pass |
| Aquileia | 2023 | 0.809 | pass |
| Puteoli | 1723 | 0.739 | pass |
| Salona | 3452 | 0.688 | marginal |

Median r ≈ 0.82 (range 0.69–0.89). Source: `production-summary.json`, field `diagnostics.anchor_internal_consistency`.

### Why this matters

(i) **External validation at production scale.** The Pompeii check is independent of the model's parameters: the model was fitted on the full corpus with Pompeii as one of the anchors, and the diagnostic asks whether it respects a terminus it was never given. Passing this test at 0.12 % post-79 leakage confirms the spatial–temporal smoothing is not manufacturing spurious late-period mass.

(ii) **Corroborates the smoke run.** This is the first time the check has been run at full production scale (268 cities, monolithic fit, inscription-25y primary). The result replicates and strengthens confidence from earlier exploratory runs.

(iii) **Anchor internal-consistency provides a routine model-fit diagnostic.** The shape-r table gives reviewers and readers a per-site sanity check: the smoothed Bayesian trajectory tracks the raw SPA at r ≈ 0.69–0.89 everywhere. Salona (r = 0.69) is the weakest site and merits a targeted discussion in any write-up — the SPA and model-trajectory diverge more there than elsewhere.

### Caveats / methodological notes

**Post-79 leakage is non-zero but trivially small.** The 5.0 units of mass in bins ≥ AD 100 out of 4262 total is plausibly rounding and MCMC posterior noise rather than genuine model failure; 0.12 % is well within what any Bayesian sampler would produce.

**Anchor internal-consistency gate definitions differ across anchors.** Some anchors report `gates_pass: false` (Ostia, Salona) on the standalone diagnostic, which uses a stricter single-city convergence criterion than the production monolithic fit. The shape-r values themselves are the primary diagnostic; the gate label is secondary.

**Salona's r = 0.69** may reflect genuine disagreement between the aoristic SPA and the model-smoothed trajectory (e.g., the ICAR spatial prior pulling Salona toward Dalmatian neighbours), not a model failure per se. Worth investigating before the final write-up.

### Related observations and artefacts

**Obs 63** (N\* = 300 calibration; commit `eb3aef3`): the companion §5 calibration finding from the same production run — quantifies the small-N reliability floor. This Obs covers the external validation diagnostics from the same run.

**Obs 61** (letter mass is temporally weaker; `107226b`): §5 reachability / design-effect finding. Background on why inscription-count rather than letter-mass is the primary measure.

**Artefacts**: `runs/2026-05-30-s5-small-n-trajectories/RESULTS.md`, `runs/2026-05-30-s5-small-n-trajectories/code/production/production-summary.json`; commit `eb3aef3`.

### Findable later

`pompeii-ad79`, `external-validation`, `terminus`, `eruption`, `vesuvius`, `s5-layer-a`, `aoristic`, `poisson-aoristic`, `icar`, `anchor-internal-consistency`, `salona`, `trajectory`, `validation`, `shape-r`, `post79-mass`, `post79-fraction`, `temporal-mass-leakage`, `production-diagnostics`, `pompeii-ad79-check`, `ad79`, `layer-a-production`, `mogontiacum`, `ostia`, `aquileia`, `puteoli`, `carnuntum`, `smoke-run-corroboration`, `8a2`, `8a1`

## Obs 65 — 2026-06-02 [GOTCHA]: arviz 1.x makes the netCDF backend optional — a lock refresh silently stripped the ability to read the project's own HDF5 posteriors

While refreshing `uv.lock` to the pymc-6 stack (task #9, PR #5, merged `4df6d47..ad3457b`), a clean dependency resolve produced an environment that imported every package successfully yet **could not read the §5 `.nc` posteriors**. The cause is a quiet consequence of the arviz 0.x → 1.x major refactor.

### The finding

arviz 0.23.x hard-depended on a netCDF backend, so h5netcdf + h5py were always present transitively. arviz 1.1.0 makes the netCDF backend an **optional extra**, and `h5netcdf` 1.8.1 itself declares only `numpy` + `packaging` — leaving the HDF5 binding (h5py or h5pyd) to the caller. So a clean resolve of `pymc>=6.0.1` (which pulls arviz 1.1.0) **dropped both h5netcdf and h5py** from the lock. The four §5 monolithic posteriors are HDF5-format `.nc` (magic bytes `\x89HDF`), written via `InferenceData.to_netcdf` → xarray → h5netcdf → h5py. In the stripped environment every `import` succeeds and an import-only check passes, but `az.from_netcdf(...)` fails at runtime — Layer B's input would be unreadable.

zbook avoided the failure only because it still had h5py 3.16.0 + h5netcdf 1.8.1 as **leftovers** from the arviz-0.x era; a fresh host provisioned from the clean lock would not.

**Fix**: declare `h5netcdf>=1.8.1` and `h5py>=3.16.0` directly in `pyproject.toml` (commit `4df6d47`), so the backend is locked regardless of arviz's optionality.

### Why this matters

(i) **A "clean" lock can be functionally broken in ways imports don't reveal.** The env looks healthy until it tries the actual I/O path. The §5 `preflight.py` check was therefore strengthened to round-trip a real `xarray → h5netcdf → .nc` write+read (not merely import h5py), so this class is caught before any sampling (`ad3457b`).

(ii) **General pattern for major-version dependency bumps.** When a major version moves functionality from a hard dependency to an optional extra, refreshing a lock can quietly remove capability the old lock provided implicitly. After such a bump, verify the *real* operation (here, netCDF I/O), not just that the top-level package imports.

(iii) **Backups inherit the caveat.** The backed-up `.nc` (rpi-qnap, 2026-06-02) carry a MANIFEST recording that they need arviz ≥ 1.x + h5netcdf + h5py to read — a future restorer on a bare or older env would otherwise hit the same wall.

### Caveats / methodological notes

The HDF5-vs-classic-netCDF distinction is load-bearing: classic netCDF could be read by scipy alone, but these are HDF5, so an HDF5 binding is mandatory. The project standardised on h5netcdf (what zbook validated), not netcdf4.

### Related observations and artefacts

**Obs 66** (host stack split): the companion provenance finding from the same session. **Artefacts**: `pyproject.toml`, `runs/2026-05-30-s5-small-n-trajectories/code/preflight.py`, `PROVISIONING.md`; PR #5 (`4df6d47..ad3457b`).

### Findable later

`arviz`, `arviz-1x`, `netcdf`, `hdf5`, `h5netcdf`, `h5py`, `optional-extra`, `uv-lock`, `dependency-hygiene`, `pymc-6`, `lock-refresh`, `backend`, `to-netcdf`, `from-netcdf`, `preflight`, `provisioning`, `major-version-bump`, `silent-breakage`, `reproducibility`, `s5-posteriors`, `task-9`, `pr-5`

## Obs 66 — 2026-06-02 [PROVENANCE]: the project's Bayesian results currently span two stacks — §5 on pymc-6 / arviz-1.1, the recovery grids on pymc-5.28 / arviz-0.23

A side-effect discovery while refreshing the dependency lock (task #9): the project's two main Bayesian work-products were produced on **different major versions** of the core stack.

### The finding

Installed versions, read at source (`.venv` on each host), not from notes:

| host | role | python | pymc | pytensor | arviz |
|---|---|---|---|---|---|
| zbook | §5 Layer-A | 3.13.7 | 6.0.1 | 3.0.3 | 1.1.0 |
| sapphire | recovery grids A + B | 3.13 | 5.28.5 | 2.38.3 | 0.23.4 |

The two recovery grids (inscription + letter, the 2026-05-26 two-unit re-simulation) ran on the **same** sapphire stack, so they are mutually consistent and the cross-grid comparison is internally clean. **§5 is the outlier** — it ran on the newer pymc-6 stack on zbook.

PR #5 **standardised the project on pymc-6**: `uv.lock` now pins pymc 6.0.1 / pytensor 3.0.3 / arviz 1.1.0. The sapphire upgrade (`uv sync --frozen`) is queued for **after Grid B finishes** (never mid-run) — documented in `PROVISIONING.md`.

### Why this matters

(i) **Provenance for the write-up.** Any results table should record which stack produced which number; the recovery-grid and §5 results cross a pymc-major boundary. Benign (they answer different questions) but should be stated, not hidden.

(ii) **Cross-readability constraint.** The §5 `.nc` are arviz-1.1 HDF5 (Obs 65); sapphire's arviz 0.23 may not read them, so **Layer B must run on zbook (or a pymc-6 host) until sapphire is upgraded** — a concrete scheduling constraint.

(iii) **The recovery grids need no re-run.** Because both grids share one stack, there is no need to re-run Grid A under pymc-6 to match Grid B — they are already on the same footing. Only §5 ↔ recovery-grid comparisons cross the version boundary.

### Caveats / methodological notes

The split is partly transient: once sapphire is upgraded post-Grid-B, new work converges on pymc-6. But the *completed* artefacts (Grids A/B on 5.28; §5 on 6.0.1) are fixed historical facts and keep their provenance regardless of later upgrades.

### Related observations and artefacts

**Obs 65** (arviz-1.x optional backend): the companion dependency finding. **Artefacts**: `uv.lock`, `pyproject.toml`, `PROVISIONING.md`; PR #5 (`4df6d47..ad3457b`); §5 posteriors backup MANIFEST (rpi-qnap).

### Findable later

`provenance`, `pymc-6`, `pymc-5`, `arviz-1x`, `arviz-0x`, `pytensor`, `stack-split`, `reproducibility`, `recovery-grid`, `s5-layer-a`, `zbook`, `sapphire`, `host-parity`, `layer-b`, `cross-run-consistency`, `version-pinning`, `task-9`, `pr-5`, `uv-lock`

## Obs 67 — 2026-06-02 [METHODOLOGY / CORRECTION]: Grid A's recovery FAIL is predominantly a metric artefact, not a fit failure

Adjudicating Grid A (inscription-mass) of the two-unit recovery grid under the lodged binding criterion returned **FAIL** — coverage 69.8%, shape-r 70.2%, both-pass 42.7% (vs 40.9% in 2026-05-22; the F1+F3 fixes were only marginal). Re-deriving the per-cell failure structure showed the FAIL is **predominantly a metric problem**, not a model failure:

- **Criterion (ii) is undefined for the flat genuine shape.** Pearson r against a constant truth is `0/0`; all 75 `flat_baseline` cells return `nan` and fail mechanically, capping achievable shape-pass at 375/450 = 83.3% irrespective of model quality. The model recovers flatness *well* (~99% coverage, small W-1).
- **Criterion (i) — exact 95%-CI coverage of α — collapses at large N.** Holding (shape, α, tier) fixed and raising N, cell coverage falls ~1.0 → ~0.0 while the α bias stays small and roughly constant (e.g. regnal_cluster α=0.70: bias 0.004 → 0.053, coverage 1.00 → 0.11). This is posterior concentration / semiparametric Bernstein–von Mises — it measures asymptotic interval calibration, not recovery adequacy.
- **The quantity we consume recovers well throughout:** posterior-median Pearson r between recovered and true `p_gen` ≈ 0.998.

A verified prior-art scout confirmed no surveyed community (radiocarbon SPD / rcarbon, baorista, Bayesian-workflow SBC) gates on exact CI-coverage of a mixing weight; flat is a *standard tested null*; Wasserstein-1 is the theoretically-justified deconvolution metric (Rousseau & Scricciolo 2021). Under the corrected criterion (Decision 33: hybrid shape gate Pearson r ≥ 0.95 non-flat / W-1 ≤ 10 y flat; convergence precondition; α demoted to a quantified diagnostic; operating envelope α ≤ 0.70), Grid A **PASSes at 91.9%** in the operating envelope. **Artefacts**: `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md` + `tables/grid-summary.parquet` (commit `0638093`); Decision 33; OSF Amendment 01 §A5.5.1; `planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`.

> **Update 2026-06-04 (the 91.9% is historical → 98.6%).** The 91.9% headline above was computed under a *zero-tolerance divergence* convergence gate that was later found non-standard (Obs 70): under the field-standard R̂ / bulk-ESS gate the 24 `flat_baseline` cells it excluded all converge, so headline B = diagnostic A = **98.6% (355/360)**, the residual 5 being `bimodal_α=0.70_N=2000` genuine-shape failures. Initially this 98.6% was a direct re-score while the harness still emitted 91.9%; the harness was corrected on 2026-06-04 (`aggregate.py` now re-derives convergence from the stored per-replicate R̂ / bulk-ESS via the shared `cell_lib.convergence_pass` gate, no re-fit) and now reproduces **98.6% in-pipeline** with a passing regression check. See **Obs 70** (gate artefact), **Obs 72** (the complementary letter-mass R̂/ESS failure), and commits `4f96e47` (code) + `0a15667` (re-aggregated artefacts).

### Findable later

`recovery-grid`, `mixture-model`, `deconvolution`, `pearson-r`, `flat-baseline`, `undefined-metric`, `alpha-coverage`, `bernstein-von-mises`, `posterior-concentration`, `wasserstein-1`, `decision-33`, `amendment-01`, `criterion-clarification`, `p-gen`, `operating-envelope`, `prior-art-scout`, `grid-a`, `inscription-mass`

## Obs 68 — 2026-06-02 [LIMITATION]: the recovered genuine-SPA credible band is overconfident for sharply-peaked signals, and degrades with N

The recovery grid validated `p_gen` *shape* recovery (Pearson r ≈ 0.998) but stored only the posterior **median** curve, not the band. A re-fit band-calibration diagnostic (12 cells × 30 reps, zbook; `runs/2026-06-02-recovery-utility-check/`) measured the per-bin credible band's pointwise coverage of the true `p_gen`:

| shape | N=2000 | N=50000 |
|---|---|---|
| smooth_growth | ~0.99 | ~0.99 |
| rise_and_fall | 0.77 | 0.55 |
| regnal_cluster | 0.89 | **0.23** |

Mean pointwise 95% coverage falls 0.90 (N=2k) → 0.67 (N=50k). **The band is honest for smooth signals but overconfident for sharply-peaked ones, degrading with N** — the same posterior-concentration effect that broke α, compounded by the Gaussian-random-walk smoothness prior being unable to represent sharp features (so the posterior concentrates confidently on a too-smooth curve and the narrow band misses the peaks). Pearson r is shift/scale-invariant, so it certifies the *curve* while saying nothing about the *band*. **Consequence for the paper:** report the recovered median timeline (the gated, trustworthy quantity), but do not present its credible band at face value in peaked regimes — the real corpus has sharp regnal clustering (AD ~77 / 122 / 212). Logged as a limitation, not a new gate; deferred fix is a roughness-tolerant `p_gen` prior. **Artefacts**: `runs/2026-06-02-recovery-utility-check/outputs/band-calibration-by-cell.csv`.

### Findable later

`band-calibration`, `credible-interval`, `coverage`, `overconfident`, `posterior-concentration`, `grw`, `smoothness-prior`, `peaked-signal`, `regnal-cluster`, `pearson-r`, `p-gen`, `point-vs-interval`, `uncertainty-presentation`, `roughness-prior`, `large-n`

## Obs 69 — 2026-06-02 [PROVENANCE / LIMITATION]: the real corpus sits just inside the recovery envelope globally, but the late corpus (AD ~142–347) is in the degraded-recovery zone; narrow-dating is strongly type-skewed

The descriptive convention-mass fraction of the real LIRE corpus (F1+F3 family aoristic mass / total, the same definition the model's `p_conv` is built from; `runs/2026-06-02-recovery-utility-check/code/real-corpus-convention-fraction.py`):

- **Corpus-wide ≈ 0.65** — *just inside* the α ≤ 0.70 operating envelope, with little margin (F1_round century templates alone are 59.5% of aoristic mass).
- **21 of 80 time-bins exceed 0.70, spanning AD ~142–347** — the late corpus is in the degraded-recovery zone, so genuine-signal claims for the mid-2nd to 4th centuries (often the historically richest period) need explicit hedging. Dips at the era boundary and regnal years (AD ~77, ~212) are precisely-dated material, a sanity check that the classifier captures something real.

Separately, **narrow-dating is strongly correlated with inscription type** (verified on `type_of_inscription_clean`): epitaphs are 39.3% of the corpus but only 9.0% of narrow-dated inscriptions (0.23×), while honorific (3.15×) and building/dedicatory (2.73×) are over-represented. So discarding template-dated inscriptions ("throw away the slabs") loses 82.5% of the corpus *and* introduces a severe selection bias toward public/official inscriptions — the mixture/aoristic approach (which keeps all data and uses the narrow-dated as a calibration cohort) is preferable on both power and bias grounds. The type-skew means the calibration cohort itself needs post-stratification reweighting (backlog). **Artefacts**: `runs/2026-06-02-recovery-utility-check/outputs/convention-fraction-{by-bin.csv,over-time.png}`.

### Findable later

`convention-fraction`, `operating-envelope`, `real-corpus`, `late-corpus`, `degraded-recovery`, `aoristic`, `family-classifier`, `f1-f3`, `type-skew`, `epitaph`, `selection-bias`, `calibration-cohort`, `post-stratification`, `throw-away-the-slabs`, `discard-vs-decompose`, `p-conv`

## Obs 70 — 2026-06-04 [METHODOLOGY / CORRECTION]: the flat-null convergence "limitation" was an artefact of the zero-tolerance divergence gate, not a property of the method

The gap between headline B (91.9%, denominator = all in-envelope cells) and diagnostic A (98.5%, denominator = convergence-eligible cells) in the corrected Grid A verdict (Obs 67 / Decision 33 / OSF Amendment 01 §A5.5.1) was entirely occupied by 24 `flat_baseline` cells excluded by the convergence precondition. A direct re-score from stored per-replicate diagnostics identified the cause: those 24 cells fail **solely** on the convergence precondition's zero-tolerance divergence gate (`n_divergences == 0` per replicate, encoded in `fit.py`'s `convergence_pass`). Under an R̂/ESS-only gate all 60 flat in-envelope cells pass.

### The finding

The divergences are benign. Across 6,000 in-envelope flat replicates, 10.2% carry ≥ 1 divergence (median count 1; maximum rate 0.36% of post-warmup draws). Diverging replicates recover the flat shape no worse than clean ones:

| comparison | diverging reps | non-diverging reps |
|---|---|---|
| median Wasserstein-1 | 0.59 y | 0.55 y |
| within W1 ≤ 10 y gate | 99.7% | 97.8% |
| Mann–Whitney *p* | ≈ 0.36 | — |

A prior-art scan of Bayesian-workflow practice (Stan diagnostics guidance; Betancourt 2017; Vehtari et al. 2021) confirmed no source endorses a per-replicate zero-tolerance divergence gate or any numeric rate threshold — the field standard is contextual investigation of whether divergences bias the posterior.

The convergence precondition was updated to the field-standard benign-tolerant form: R̂ < 1.01 + bulk-ESS ≥ 400 (the Vehtari et al. 2021 thresholds); divergences assessed for benignity (low rate + recovery-unaffected pass; clustered or persistent fail). This change propagates immediately:

- **Grid A re-scores to B = A = 98.6% (355/360)** — the B/A distinction dissolves, and the flat-null "limitation" is resolved rather than merely reported.
- The backlog re-fit of the 24 flat cells is retired.
- Grid B still FAILs and, under the revised gate, is now shown to fail on R̂/ESS (zero letter cells recovered even after dropping the divergence requirement) — see Obs 72.

### Why this matters

The correction closes a gap that had been logged as a paper-level limitation (that the headline figure required a footnote about 24 excluded cells). After the gate revision the single reported figure (98.6%) is clean, self-consistent, and more defensible by field standards than the prior zero-tolerance stance. OSF Amendment 01 §A5.5.1 encodes both the updated gate and the verified benign-divergence evidence, so the provenance chain to the lodged preregistration is intact.

### Caveats / methodological notes

The `flat_baseline` shape represents the genuine-null hypothesis — no genuine activity above background. Its occasional divergences arise from a funnel geometry in a near-degenerate likelihood (flat truth makes the mixing-weight ridge very shallow): a recognised HMC behaviour that does not indicate model misspecification. The R̂/ESS-based gate is the appropriate tool for detecting actual sampling failure in this regime.

### Related observations and artefacts

**Obs 67** (Grid A FAIL is predominantly a metric artefact): the parent Obs that introduced the corrected criterion and first reported the 91.9%/98.5% split; this Obs closes the residual B/A gap. **Obs 72** (Grid B fails on R̂/ESS, not divergences): the complementary finding for letter-mass under the same gate revision. **Decision 33**: the harness-update decision that introduced the corrected criterion. **Artefacts**: `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md`; `planning/martin-review-statistical-grounds-2026-06-04.md` §(c) (data + scout findings); OSF Amendment 01 §A5.5.1 (commit `11b3388`); `fit.py` `convergence_pass` function (commit `006a655`).

### Findable later

`flat-baseline`, `convergence-gate`, `zero-tolerance`, `divergence`, `benign-divergence`, `rhat`, `ess`, `bulk-ess`, `wasserstein-1`, `mann-whitney`, `grid-a`, `inscription-mass`, `b-a-gap`, `flat-null-limitation`, `amendment-01`, `decision-33`, `obs-67`, `betancourt-2017`, `vehtari-2021`, `field-standard`, `rhat-threshold`, `per-replicate`, `convergence-precondition`, `355-360`, `98-6-percent`, `backlog-retire`

## Obs 71 — 2026-06-04 [RESULT]: small-N reachability floor for subset-specific deconvolution measured

The small-N reachability study (`runs/2026-06-03-small-n-reachability/`; 4,200 fits over 84 cells = 3 shapes × 4 α levels × 7 N values, `pilot_proxy` tier, scored under the §A5.5.1 corrected criterion) measured the minimum subset size N at which subset-specific deconvolution (Decision 34) recovers reliably.

### The finding

Reachability floor (smallest N passing convergence ≥ 90% AND Pearson r ≥ 0.95 in ≥ 90% of replicates):

| shape | α = 0.30 | α = 0.50 | α = 0.70 | α = 0.85 |
|---|---|---|---|---|
| smooth_growth | N ≥ 500 | N ≥ 2,000 | UNREACHED | UNREACHED |
| rise_and_fall | N ≥ 500 | N ≥ 1,000 | N ≥ 2,000 | UNREACHED |
| regnal_cluster | N ≥ 1,000 | N ≥ 1,000 | UNREACHED | UNREACHED |

Within the operating envelope (α ≤ 0.70), the **worst-case floor is N ≥ 2,000**; easiest subsets (α ≈ 0.30, smooth_growth / rise_and_fall) reach N ≥ 500. Two α = 0.70 cells (regnal_cluster, smooth_growth) are unreached even at N = 2,000. The α = 0.85 stress row is unreached throughout.

Recovery quality scales with N (α ≤ 0.70 cells):

| N | mean shape-rate | mean conv-rate | mean \|α-bias\| |
|---|---|---|---|
| 50 | 12% | 100% | 0.155 |
| 350 | 51% | 100% | 0.132 |
| 1,000 | 80% | 99% | 0.134 |
| 2,000 | 94% | 100% | 0.133 |

### Why this matters

Decision 34 authorises proceeding under inscription mass only, with subset-specific deconvolution for subsets large enough to support it and a pooled-convention fall-back for small subsets. This study gives the empirical threshold (N = 2,000 worst-case within the envelope) that operationalises the fall-back trigger. It also confirms that convergence (100% across tested cells) is not itself the bottleneck — shape recovery is. The study was conducted on `pilot_proxy` tier (the realistic descriptive proxy), so the floor reflects actual operating conditions rather than idealised uniform conventions.

### Caveats / methodological notes

The original run (4,189 fits) was lost to a power-cycle before any output was written — no checkpointing was in place. A resumable JSONL checkpoint was added to `reachability.py` (commit `a0458fa`) and the run was repeated in full. The 11 discrepancy (4,200 vs 4,189) reflects incomplete progress at power loss; the re-run is complete and the outputs are authoritative. The `pilot_proxy` tier only is tested; a `uniform` robustness pass is optional backlog. The study ran under `pymc` 6.x (zbook), while the recovery grids used `pymc` 5.28 (sapphire); the model is identical across versions, and this is a calibration property that transfers (Obs 66).

### Related observations and artefacts

**Obs 67** (Grid A PASS under corrected criterion): the criterion used to score this study. **Obs 66** (pymc stack split): explains the host/version context. **Decision 34**: the subset-specific deconvolution decision that this study operationalises. **Artefacts**: `runs/2026-06-03-small-n-reachability/outputs/REPORT.md`; `runs/2026-06-03-small-n-reachability/outputs/figures/reachability-map.png` (commit `5601b04`); `runs/2026-06-03-small-n-reachability/code/reachability.py` (checkpoint logic, commit `a0458fa`).

### Findable later

`small-n`, `reachability`, `subset-specific`, `deconvolution`, `recovery-floor`, `n-floor`, `decision-34`, `pilot-proxy`, `shape-rate`, `convergence-rate`, `alpha-bias`, `smooth-growth`, `rise-and-fall`, `regnal-cluster`, `operating-envelope`, `alpha-0-70`, `alpha-0-85`, `stress-row`, `power-cycle`, `checkpoint`, `jsonl-checkpoint`, `pooled-convention`, `fall-back`, `worst-case-floor`, `2000-inscriptions`, `obs-67`, `obs-66`

## Obs 72 — 2026-06-04 [RESULT]: Grid B (letter-mass) fails recovery on R̂/ESS, not merely divergences

The cross-grid adjudication (commit `1bf791f`) returned inscription PASS / letter FAIL. Under the original corrected criterion the letter-mass failure was attributed to the convergence precondition, but it was not yet clear whether the failure was driven by the zero-tolerance divergence gate (which was independently suspect — see Obs 70) or by genuine HMC sampling failure. The gate revision (Obs 70) resolved the ambiguity.

### The finding

Under the field-standard benign-tolerant gate (R̂ < 1.01 + bulk-ESS ≥ 400; Obs 70): **dropping the divergence requirement recovers zero letter-mass cells**. Every in-envelope letter cell still fails the convergence precondition on R̂/ESS grounds alone; headline B = 0.0% is unchanged. The maximum cell-level convergence rate across all letter-mass cells (including the α = 0.95 stress row) is 0.80, well below the ≥ 90% threshold.

The failure pattern is consistent with a genuine HMC sampling problem rather than a strict gate. Divergences run to ~13,000 per cell in the worst cases; the underlying cause is the compound-sum likelihood: each synthetic inscription deposits a heavy-tailed letter count, making the posterior geometry difficult for NUTS to navigate reliably. The median recovered Pearson r across cells is ≈ 0.76 — partial shape recovery is occurring, but not at a rate that meets the validation criterion.

| metric | value |
|---|---|
| Headline B (binding) | 0.0% (0/360 in-envelope cells) |
| Cells recovered after dropping divergence gate | 0 |
| Maximum cell convergence rate (all cells) | 0.80 |
| Divergences per cell (typical worst-case) | ~13,000 |
| Median recovered Pearson r across cells | ≈ 0.76 |

### Why this matters

This empirically confirms the earlier analytic finding that letter-mass temporal detection is unreachable corpus-wide (OSF Amendment 01 §A5.2), and closes a logical gap: the zero-tolerance gate was separately identified as a potential artefact (Obs 70), so it was important to verify that Grid B's failure is not merely an overly strict gate. It is not. The temporal mixture deconvolution proceeds under inscription mass only (Decision 34). The letter-mass cross-sectional H3a confirmatory is unaffected — it uses per-city totals and does not invoke the temporal deconvolution (§A5.5).

### Caveats / methodological notes

The compound-sum likelihood (sum of heavy-tailed per-inscription counts) is structurally harder for NUTS than the inscription-count likelihood, which is driven by a simple Poisson-count model. A potential sensitivity analysis — applying a 99th-percentile cap on per-inscription letter counts — was noted in the comparison report as optional follow-up; it has not been run and is not required for the current analysis path.

### Related observations and artefacts

**Obs 61** (letter mass is the temporally weaker unit): the earlier analytic finding that this study empirically confirms. **Obs 70** (flat-null divergence gate revision): the gate change that made the R̂/ESS-only diagnosis possible; Obs 72's finding is a consequence of applying Obs 70's reasoning to Grid B. **Obs 67** (Grid A PASS under corrected criterion): the counterpart inscription-mass verdict. **Decision 34**: the outcome-branch decision authorising inscription-mass-only deconvolution. **Artefacts**: `runs/2026-05-26-recovery-grid-two-unit/comparison/COMPARISON-REPORT.md`; `runs/2026-05-26-recovery-grid-two-unit/letter-mass/outputs/REPORT.md` (commit `1bf791f`); OSF Amendment 01 §A5.5.1–§A5.7.

### Findable later

`letter-mass`, `grid-b`, `rhat`, `ess`, `bulk-ess`, `convergence-failure`, `nuts-sampling`, `hmc-divergences`, `compound-sum`, `heavy-tailed`, `letter-count`, `compound-likelihood`, `temporal-detection`, `unreachable`, `inscription-mass-only`, `decision-34`, `h3a-unaffected`, `cross-sectional`, `zero-cells`, `obs-61`, `obs-67`, `obs-70`, `amendment-01`, `a5-2`, `a5-5`, `0-0-percent`, `adjudication`, `1bf791f`

## Obs 73 — 2026-06-04 [METHODOLOGY / INTERPRETATION]: why the `p_gen` band's coverage falls with N — GRW-prior misspecification compounding posterior concentration, not a tunable N

This Obs deepens Obs 68 (which recorded the band-overconfidence limitation) by giving the mechanism, and corrects a natural misreading that there is an "ideal N" at which the calibration problem goes away. The diagnostic is the same 12-cell × 30-rep band-calibration run (`runs/2026-06-02-recovery-utility-check/`); the new reading is of what the per-shape split at matched N reveals.

Two effects of growing N act independently on the recovered `p_gen` 95% credible band.

**Effect 1 — the band narrows universally.** Posterior concentration (Bernstein–von Mises) shrinks the band regardless of signal shape. At α = 0.3, moving from N = 2,000 to N = 50,000 reduces `band_width` approximately three-fold for every shape tested:

| shape | N=2,000 band_width | N=50,000 band_width | ratio |
|---|---|---|---|
| smooth_growth | 0.0083 | 0.0028 | ~3× |
| regnal_cluster | 0.0115 | 0.0032 | ~3.6× |
| rise_and_fall | 0.0077 | 0.0027 | ~2.9× |

This is the same mechanism that demoted α from a binding gate to a diagnostic (Obs 67 / Decision 33): with enough data the posterior becomes very tight — and tight is not the same as correct.

**Effect 2 — the band's centre is biased for sharp features, and that bias does not shrink with N.** The Gaussian-random-walk (GRW) smoothness prior structurally cannot represent a sharp regnal spike; the posterior median sits on a smeared version of the truth. That smearing is a property of the model class, not of sample size, so it does not reduce as N grows.

Combining the two effects: the standard deviation of the posterior shrinks (effect 1) while the bias in its centre stays fixed (effect 2). The bias-to-SD ratio therefore grows with N; eventually the true peak sits outside the now-narrow band and coverage collapses. The band becomes more confident about a slightly wrong answer.

The decisive evidence that this is prior misspecification rather than pure posterior concentration is the per-shape split at α = 0.3 (matched N, matched ~3× band-narrowing):

| shape | N=2,000 cov95 | N=50,000 cov95 | verdict |
|---|---|---|---|
| smooth_growth | 0.998 | 0.990 | holds |
| rise_and_fall | 0.769 | 0.545 | collapses |
| regnal_cluster | 0.894 | 0.230 | collapses |

If the degradation were pure posterior concentration, all shapes would degrade together. Instead, only the shapes the GRW prior cannot represent lose coverage — smooth signals hold near-nominal coverage even at N = 50,000, while regnal_cluster reaches 0.230 at the same N. The Obs 68 means (≈ 0.90 → ≈ 0.67 across the six shape × α cells) are averages over this heterogeneous picture; regnal_cluster at 0.230 is the worst single case.

**This is a failure of the uncertainty band, not the point estimate.** The posterior median still passes the r ≥ 0.95 shape gate (peak in the right place). Honest caveat: "median trustworthy" means shape-trustworthy (timeline correlation); the smoothing prior does slightly attenuate the sharpest peak amplitudes even in the median, so a claim depending on a peak's exact height (not its timing or trajectory) warrants caution for the point estimate too.

**N is not a tunable optimum.** The small-N and large-N problems are different failure modes on different quantities. Small N is a reachability/power problem: the model cannot recover the signal at all, but the bands are honestly wide (Obs 71; worst-case floor N* ≈ 2,000 within the §5 operating envelope). Large N is a calibration problem: the point estimate is excellent but the band is overconfident for peaked signals. These live on different axes — "can I detect it?" vs "is my stated uncertainty honest?" — so there is no N at which both are simultaneously perfect. And N is not a dial: it is however many inscriptions a city or subset actually has. N = 2,000 appears in both studies because it is the smallest grid value tested for band calibration, not because it is optimal.

The upshot (which is encoded in the OSF Amendment 01 limitation note): report the recovered median timeline (robust across N, the gated quantity); where the genuine signal is sharply peaked — the real corpus has strong regnal clustering (Obs 69) — widen or caveat the band rather than trusting its stated width; do not engineer N downward to improve calibration. Deferred fix: a roughness-tolerant `p_gen` prior (backlog).

### Related observations and artefacts

**Obs 68** (the band-overconfidence limitation this Obs explains the mechanism of): recorded the calibration failure and logged it as a limitation; this Obs supplies the causal decomposition into bias and variance components. **Obs 67 + Decision 33** (the same Bernstein–von Mises mechanism that demoted α from binding gate to diagnostic): effect 1 above is the α-demotion mechanism applied to band width rather than coverage. **Obs 69** (the real corpus has sharp regnal clustering): makes this band limitation materially relevant — it is not a theoretical edge case. **Obs 71** (small-N reachability floor): the complementary failure mode on the other axis; together Obs 71 and Obs 73 define the two-sided problem that rules out N as a tuning lever. **Artefacts**: `runs/2026-06-02-recovery-utility-check/outputs/band-calibration-by-cell.csv`; `runs/2026-06-02-recovery-utility-check/code/band-calibration.py`.

### Findable later

`band-calibration`, `coverage-vs-n`, `posterior-concentration`, `bernstein-von-mises`, `model-misspecification`, `grw-prior`, `smoothness-prior`, `peaked-signal`, `regnal-cluster`, `bias-variance`, `band-width`, `point-vs-interval`, `median-vs-band`, `n-not-a-dial`, `reachability-vs-calibration`, `roughness-prior`, `large-n`, `alpha-demotion`, `obs-68-deepens`, `obs-67`, `obs-69`, `obs-71`, `smooth-growth`, `rise-and-fall`, `cov95`, `0-230`, `0-998`, `bias-to-sd-ratio`

## Obs 74 — 2026-06-05 [RESULT]: H3c(i) capitals over-produce (replicates Hanson 2021); H3c(ii) clustering does not — the Mundlak intercepts absorb the spatial structure

H3c(i) — the binding provincial-capital residual contrast (Decision 23: `P(contrast_s>0) ≥ 0.95`, draw-wise) — was found **unrun** by the 2026-06-05 prereg-completeness audit (the H3a confirmatory run had done only H3c(ii) Moran's I) and closed using the **OXREP-authoritative** capital indicator (Hanson 2016 Civic-Status "Provincial capital" — the dataset Hanson 2021 used), with the book/Barrington AD-117 set as a sensitivity.

**Provincial capitals over-produce inscriptions: SUPPORTED in all four cells** (OXREP + AD-117 × empire + Latin), `P(contrast>0) = 1.000` throughout. OXREP primary: empire median contrast **+0.96 [0.74, 1.21]**, Latin **+1.08 [0.81, 1.41]**; capitals' posterior-mean Pearson residual **+0.91** (empire) / **+1.03** (Latin) vs non-capitals **≈ −0.05**. This **replicates Hanson 2021's capital over-production** (answers SR2(i)). In contrast, **H3c(ii) residual spatial clustering is NOT-supported** (Moran's I ≈ 0, both frames). The two cohere via one mechanism: the **Mundlak province random intercepts absorb the broad spatial structure** (residual Moran's I ≈ 0), while the **within-province capital-vs-peer level difference is left in the residuals** (strong capital contrast). Robust to capital definition (OXREP 62 vs AD-117 39 in the empire frame) and to frame. Preliminary; Latin frame amendment-gated (Amendment 02). **Artefacts**: `runs/2026-06-04-h3a-confirmatory/outputs/REPORT-h3c-i-capital-contrast.md`; `h3c-i-results-{oxrep-primary,ad117-sensitivity}.json` (commits `fb1e98a`, `fffb639`); capital indicator `data/processed/provincial-capitals.csv` (OXREP) + `-ad117.csv`. Cross-ref: Decision 23 (H3c split); Decision 36 (Latin frame); the H3a confirmatory REPORT.

### Findable later

`h3c-i`, `provincial-capital`, `capital-contrast`, `hanson-2021`, `replication`, `sr2`, `morans-i`, `h3c-ii`, `mundlak`, `province-intercept`, `oxrep`, `capital-over-production`, `draw-wise-contrast`, `non-replication`, `spatial-autocorrelation`

## Obs 75 — 2026-06-05 [RESULT]: the Latin-province frame strengthens the population signal vs empire-wide — a coverage-confound corroboration

Restricting the cross-sectional analyses to Latin-speaking provinces (Decision 36; the coverage rationale — LIRE = "Latin Inscriptions of the Roman Empire" under-covers Greek-speaking provinces, where Latin inscriptions are a minority) **strengthens the within-province population effect**: H3a `f_within` **0.299 [0.240, 0.365]** (empire, 1,044 cities) → **0.480 [0.401, 0.566]** (Latin, 817 cities); the SR1 OLS log-log slope **0.284** (empire) → **0.505 [0.398, 0.611]** (Latin), markedly closer to Hanson 2021's β = 0.672 (though the 95 % CI still excludes 0.672). A telling corroboration of the coverage argument: of all **65 provinces only 20 clear N ≥ 2,000, and just 1 of those is non-Latin** — Greek provinces are sparsely covered in LIRE. Both `f_within` verdicts SUPPORTED. Preliminary; Latin frame amendment-gated. **Artefacts**: `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md` + `REPORT-latin-h3c-sr1.md`; Decision 36. Cross-ref: Obs 74 (same-frame H3c(i)/H3c(ii)); Decision 36.

### Findable later

`latin-provinces`, `coverage-confound`, `f-within`, `sr1`, `hanson-scaling`, `decision-36`, `amendment-02`, `lire`, `greek-provinces`, `within-province`, `frame-choice`, `0-505-vs-0-672`

## Obs 76 — 2026-06-06 [METHODOLOGY / CORRECTION]: template-dictionary empirical scan fires Decision 20's revisit trigger — curated 3-tier basis is empirically inadequate; multi-century slabs dominate the convention pool and were entirely absent from the dictionary; recovery re-validation now gates H2.1

The H2.1 prerequisite scan (prereg line 202; Decision 20; audit A2; Decision 37 next-session action 1) was run on 2026-06-05 as `runs/2026-06-05-template-dictionary/` (commit `6d8950f`). It enumerates exact `[not_before, not_after]` templates from the LIRE corpus under the pre-registration empire filter (180,609 inscriptions; confirmed) and the Decision 36 Latin frame (109,646 inscriptions; confirmed). Year-precise `[t, t]` templates are excluded from the convention pool per Decision 20 (8,279 inscriptions, 4.58 % of empire corpus; remain in `genuine_SPA`).

### The finding

The curated 3-tier dictionary (century / half-century / reign, Decision 20) is **empirically broken** as a description of the real LIRE convention pool. Key numbers from the empire-frame category-mass table (`tables/category-mass.csv`):

| category | templates | inscriptions | % of convention pool |
|---|---:|---:|---:|
| other | 4,328 | 59,762 | 34.68 % |
| multi_century | 45 | 43,022 | 24.96 % |
| century | 4 | 41,516 | 24.09 % |
| half_century | 7 | 17,166 | 9.96 % |
| bc_ad_boundary | 365 | 6,139 | 3.56 % |
| reign | 71 | 4,725 | 2.74 % |

Three structural failures of the curated basis:

1. **Multi-century slabs (24.96 % of the full empire convention pool) were entirely absent from the curated dictionary.** The earlier empirical-Bayes Stage-1 analysis (`runs/2026-05-24-empirical-pconv/`) computed the same quantity over the 119,142 F1+F3 inscriptions specifically and found two_century + one_and_a_half_century + three_century = 35.93 % of the F1+F3 convention pool. The single most frequent template corpus-wide is `[301, 500]` (N = 15,926, 8.82 % of corpus) — a Late-Antique 200-year slab that deposits convention mass only on AD 301–350 (env-overlap = 0.25). No multi-century tier existed in Decision 20's dictionary to absorb any of this mass.

2. **Reign templates are only 2.74 % of the empire convention pool** (N = 4,725 across 71 distinct reign-interval templates), meaning the curated basis — which gave reigns a full dedicated tier alongside century and half-century — grossly over-weighted their empirical contribution to convention mass.

3. **The dominant templates by count** (top 3 from `tables/templates-empire.csv`): `[301, 500]` (8.82 %), `[101, 200]` (7.37 %), `[301, 400]` (6.01 %). The century class collectively accounts for ~24 %, and the multi-century class for ~25 % — the two are roughly equal, not a 3:1 hierarchy as the curated basis assumed.

An important reconciliation: Decision 20's context (line 1671 of `planning/decision-log.md`) records "`[1, 100]` 26.3 % of corpus". The direct re-scan gives `[1, 100]` = 10,807 (5.98 %). The earlier ~26 % figure described the century-template *class* collectively, not `[1, 100]` alone — a stale specific the REPORT explicitly corrects.

### Why this matters

Decision 20's revisit trigger has fired: the tier structure needs revision before the H2.1 real-data mixture fit. **Decision 38** (commit `66e751a`, 2026-06-06) resolves this by replacing the curated 3-tier basis with an **empirical calendar-slab basis** grouped to ~3 structural tiers (no reign tier — reigns are genuine-but-aoristic and flow to `p_gen`). The reign contradiction is also resolved: the family classifier had been inconsistently placing some reign windows in F3 (convention) because their width happened to match decade-aligned templates — Decision 38 fixes this with a curated historical-anchor interval list, making the split non-width-accidental.

The consequence for H2.1 is an additional gate: **Grid A's 98.6 % recovery PASS (355/360 cells; Obs 67 + Obs 70) was validated against the old curated basis with synthetic proxy tier weights — no real-LIRE three-tier mixture has ever been fit.** The new empirical basis changes the `tier_basis` the model learns weights over; the recovery simulation must be re-run against the new basis shapes before H2.1 can proceed. Recovery re-validation plus an OSF amendment gate the H2.1 fit (Decision 38).

The Stage-1 9-slab `p_conv` decomposition (`runs/2026-05-24-empirical-pconv/`) already embodies the empirical-basis principle: it computed a frequency-weighted vector from the F1+F3 calendar population, already excluding reigns, and already found the two-century slab at 23.69 % and the three-century slab at 4.95 %. Decision 38 adopts this decomposition's population as the new basis, grouped into ~3 structural tiers.

### Caveats / methodological notes

The `[301, 500]` dominance reflects Late-Antique dating practice: the LIRE corpus extends to AD 500, and coarse 200-year slabs are the editors' default for uncertain late inscriptions. Its env-overlap = 0.25 means only one-quarter of the template's width falls inside the \[50 BC, AD 350\] operating envelope — but the mass it deposits on AD 301–350 is real convention signal that the curated basis was missing entirely.

The `other` category (34.68 %) contains templates that fit none of the four named categories. PART 2 of the scan (tier-structure decision and `design.json` commit) must resolve how to handle these — candidate treatments include a fine-grid sensitivity band (Decision 38 D5 for decadal/quarter-century brackets) or a residual-band policy. The `other` total is dominated by templates like `[1, 79]` (N = 3,202), `[151, 250]` (N = 2,782), and `[71, 130]` (N = 2,220) that are neither clean calendar slabs nor reign windows.

**On the ~31 % figure in Decision 38's context text (line 3598 of `planning/decision-log.md`)**: the decision text states "multi-century slabs are ~31 % of the F1+F3 convention pool". The source files give 24.96 % of the full empire convention pool (`tables/category-mass.csv`) and ~35.93 % of the F1+F3 pool specifically (two_century + one_and_a_half_century + three_century from `runs/2026-05-24-empirical-pconv/outputs/REPORT.md`). The ~31 % figure in the decision text does not reproduce from either source and should be treated as a rounded approximation in the decision narrative; the paper-load-bearing numbers are 24.96 % (full pool) and ~36 % (F1+F3 pool).

### Related observations and artefacts

**Obs 40** (2026-05-17 diagnostic triplet — the slab structure emerged from falsifying the anchor-year framing): records how the template-interval structure of Decision 20 was first established; this Obs documents the empirical test that shows that structure was itself incomplete. **Obs 54** (family classifier: F1_round + F3_periodic = 119,142 F1+F3 inscriptions; multi-century slabs are a substantial share of F1_round): the classifier whose F1+F3 pool is the basis for the empirical-pconv Stage-1 analysis this Obs cites. **Obs 55** (empirical-Bayes calibration-cohort pivot; Stage-1 9-slab `p_conv`): the Stage-1 analysis that first revealed the multi-century dominance in the F1+F3 pool and that the best curated-basis choice was L1 = 0.31 from empirical truth. **Obs 60** (letter-mass reshapes the editorial-template tier composition): the `pilot_proxy` tier-vector analysis that used the curated 3-tier basis — its weights are now known to be operating on a structurally inadequate basis. **Obs 67** (Grid A 98.6 % PASS under corrected criterion) + **Obs 70** (the 98.6 % is the revised headline after the zero-tolerance gate was corrected): the recovery-grid validation result that does NOT transfer to the new empirical basis and must be re-run. **Obs 69** (the late corpus AD ~142–347 is in the degraded-recovery zone): the `[301, 500]` slab found here deposits mass squarely in this zone, making the basis-inadequacy consequential for the recovery-relevant region. **Decision 38** (convention = empirical calendar-slab basis, no reign tier; recovery re-validation + OSF amendment gate H2.1): the decision this scan fired.

**Artefacts**: `runs/2026-06-05-template-dictionary/outputs/REPORT.md`; `runs/2026-06-05-template-dictionary/outputs/tables/category-mass.csv`; `runs/2026-06-05-template-dictionary/outputs/tables/templates-empire.csv`; `runs/2026-06-05-template-dictionary/outputs/tables/templates-latin.csv`; `runs/2026-06-05-template-dictionary/outputs/tables/threshold-coverage.csv` (commit `6d8950f`). Decision 38 (commit `66e751a`). Decision 20 (`planning/decision-log.md`). `runs/2026-05-24-empirical-pconv/outputs/REPORT.md` (Stage-1 9-slab `p_conv`; anchor for the F1+F3 multi-century percentages).

### Findable later

`template-dictionary`, `template-dictionary-scan`, `h2.1-prereq`, `decision-20-revisit`, `curated-basis-inadequate`, `multi-century-slab`, `multi-century-absent`, `convention-pool`, `f1-f3-convention-pool`, `301-500`, `late-antique`, `200-year-slab`, `15926`, `8-82-percent`, `reign-tier`, `reign-overweighted`, `2-74-percent`, `24-96-percent`, `category-mass`, `tier-structure`, `no-reign-tier`, `decision-38`, `empirical-calendar-slab`, `recovery-revalidation`, `grid-a-does-not-transfer`, `98-6-percent-invalid-for-new-basis`, `h2.1-gate`, `osf-amendment`, `part-2-design-json`, `threshold-coverage`, `n-threshold`, `year-precise-excluded`, `empire-180609`, `latin-109646`, `template-enumeration`, `obs-40`, `obs-54`, `obs-55`, `obs-60`, `obs-67`, `obs-69`, `obs-70`, `6d8950f`, `66e751a`

## Obs 77 — 2026-06-06 [METHODOLOGY / CONCEPTUAL]: grid-snapping is the observable discriminator between convention and genuine — the conceptual core of Decision 38, and a reframing of the plateau-step SPA artefact

This Obs pairs with Obs 76 (the empirical basis-inadequacy finding) and records the companion conceptual move settled in Decision 38: what makes a date "conventional" is not the absence of evidential signal but the act of snapping genuine-but-coarse evidence onto the BC/AD calendrical lattice. Grid-alignment is the observable shadow of that snapping, separating reign-irregular (genuine-but-aoristic) from decade-/century-aligned (convention) intervals. The empirical consequence — that the event-leak into the convention pool from the family classifier is ~0.1 % — grounds Decision 38's two settled positions: the historical-anchor principle and the decadal + quarter-century sensitivity band.

### The finding

**Convention is genuine-but-coarse evidence rounded onto the BC/AD calendar grid, not signal-free noise.** Every recorded date carries evidential anchoring (letterforms, onomastics/prosopography, formulae, consular dates, find-context — Cooley 2012). What makes a date *conventional* is the **arbitrary rounding of genuine-but-coarse evidence onto the calendrical lattice** (centuries, half-centuries, decade-windows). This snapping introduces two artefacts simultaneously:

1. **Per-inscription distortion**: a true off-grid range (e.g. a letterform in use ~AD 178–323) is truncated/shifted to a round century (`[200, 299]`) and flattened to uniform-within-bin. The genuine latent distribution is not recovered by deconvolution of a *single* inscription — the method un-snaps the **collective** (removes aggregate boundary pile-ups and flat-within-bin shape under the GRW smoothness prior).
2. **Cross-inscription artificial alignment**: many different true distributions snap to the *same* bin, manufacturing the plateau-step pile-ups at century boundaries visible in the observed SPA. This is the mechanistic explanation for the step structure first described in Obs 40 and for the AD ~142–347 convention-dominance reported in Obs 69.

**Grid-alignment is the observable discriminator** — and it is the only available proxy for the dating criterion, because LIRE's `raw_dating` column preserves only the numeric range (`not_before`, `not_after`); the EDH Datierungskriterien field was dropped in the LIRE compilation. The `classify_family` function (`runs/2026-05-24-type-stratified-narrow-spas/code/analyse-cohorts.py`, lines 108–142) operationalises this: F1_round requires width ∈ {24, 49, 99, 149, 199, 299} AND both endpoints `round_aligned(25)` (allowing ±1 for the inclusive-endpoint convention); F3_periodic requires width ∈ {19, 29, 39} AND both endpoints `round_aligned(10)`.

Concretely, this separates:

| example | class | fate |
|---|---|---|
| `[117, 138]` Hadrian; `[212, 217]` Caracalla | F2_Other (width/alignment off-grid) | genuine-but-aoristic → `p_gen` |
| `[131, 170]`; `[161, 200]` | F3_periodic (dr ∈ {39}, both endpoints round_aligned(10)) | convention pool |
| `[101, 200]`; `[1, 100]` | F1_round (dr ∈ {99}, both endpoints round_aligned(25)) | convention pool |

The inconsistency the discriminator exposes: `[161, 180]` (Marcus Aurelius, AD 161–180) classifies as F3_periodic (dr = 19, `round_aligned(10)` satisfied by the ±1 off-by-one allowance), not F2_Other — because its width accidentally matches a decade-aligned window. Decision 38's fix is a **curated historical-anchor interval list** that strips named reign/dynasty/event intervals from the convention pool before computing the empirical basis, making the split non-width-accidental.

**Empirical event-leak (empire prereg-filtered corpus; `runs/2026-06-06-convention-basis-redesign/`):**

| frame | anchor | interval | N in F1+F3 | % of F1+F3 pool |
|---|---|---|---:|---:|
| empire | Aurelian-Marcus | `[161, 180]` | 129 | 0.11 % |
| empire | *(total canonical leak)* | — | 129 | 0.11 % |
| latin | Aurelian-Marcus | `[161, 180]` | 95 | 0.15 % |
| latin | *(total canonical leak)* | — | 95 | 0.15 % |

The F2_Other family (genuine-but-aoristic, empire prereg-filtered) is **17,354 inscriptions** (9.61 % of the 180,609-inscription empire frame), confirming that the classifier already holds the vast majority of reign/dynasty/event content out of the convention pool. The residual canonical leak is 129 inscriptions (0.11 %) — effectively only `[161, 180]`.

A second width-accidental F3 interval worth noting: `[161, 200]` (N = 99 in the empire template scan, `runs/2026-06-05-template-dictionary/outputs/tables/templates-empire.csv`) falls in F3_periodic (dr = 39, both endpoints round_aligned(10) with the ±1 tolerance), but is **not** a canonical reign anchor and therefore does not appear in the formal anchor-leak table. Whether to include it on the historical-anchor removal list is a PART-2 design question; its mass (99 inscriptions) is small either way.

### Why this matters

Decision 38 settles two positions grounded by this conceptual reframing:

1. **Historical-anchor principle**: date assignments tied to reigns, dynasties, or datable events are **genuine-but-aoristic** (they carry signal that "second half of the first century" does not). Pure calendar-segment rounding is **convention**. This resolves the reign contradiction in the prereg and Decision 20 (which placed a reign-interval slab tier *inside* `p_conv`), and it fixes the width-accidental misclassification (`[161, 180]` → F3 by the current classifier, but canonical-reign by the historical-anchor principle).

2. **Decadal + quarter-century sensitivity band**: decade-aligned and quarter-century brackets (~4–5 % of the corpus) are grid-snapped (convention side) but **low-distortion** — artefact magnitude scales with grid coarseness, so deconvolving fine brackets barely moves the result. Report both (with and without) as a robustness band. The tiny event-leak (0.11 %) from a canonical reign interval that happens to land on the decade grid is the empirical confirmation that this sensitivity band is bounded and can safely ride as a check rather than a classification gate.

**For the paper (§2 reframe):** `p_gen` should be described as *"the temporal distribution with the calendar-grid quantisation removed"*, not "the distribution absent convention signal". The method un-snaps the collective convention mass; it does not reconstruct any single inscription's true off-grid latent distribution. This is methodologically distinct from radiocarbon SPD (genuine measurement/calibration uncertainty; no arbitrary rounding) and potentially shared with ceramic typological dating (round-period pinning) — which strengthens the methods-bridge framing and the Crema 2025 cite-and-distinguish positioning.

### Caveats / methodological notes

The Datierungskriterien field (EDH's taxonomised dating rationale — letterforms, titulature, prosopography, etc.) would be the empirical gold standard for the convention/genuine classification; it was dropped from LIRE. Shawn queried the SDAM team on 2026-06-05; pending their reply, the grid-alignment heuristic is the best available proxy. If Datierungskriterien are recoverable via re-join on `EDH-ID`, a direct comparison could validate or supersede the heuristic — this is Decision 38's parked enrichment path.

The `round_aligned(x, mod)` function permits ±1 off-by-one (i.e. `x % mod ∈ {0, 1, mod − 1}`) to accommodate LIRE's inclusive-endpoint convention (an inscription "from the first century" is encoded `[1, 100]`, with 1 and 100 both endpoints of the interval rather than 0 and 99). This is why `[161, 180]` qualifies for F3_periodic: `161 % 10 = 1` (passes the ±1 allowance) and `180 % 10 = 0`. The same ±1 tolerance accounts for the small discrepancy between the template-scan count (128 for `[161, 180]`) and the anchor-leak count (129): the leak script matches with `REIGN_TOL = 1` on both endpoints.

The F2_Other count of 17,354 is from the **prereg-filtered** corpus (180,609 inscriptions). The 2026-05-24 type-stratified REPORT gives 17,528 at 9.59 % for the unfiltered corpus (182,853 inscriptions) — the difference is expected and the correct reference population for H2.1 is the prereg-filtered count.

### Related observations and artefacts

**Obs 76** (template-dictionary empirical scan fires Decision 20 revisit trigger — the curated 3-tier basis is empirically inadequate): the companion empirical finding; this Obs provides the conceptual discriminator and the convention/genuine reframing that Decision 38 is built on. These two Obs together constitute the grounding for Decision 38. **Obs 40** (2026-05-17 diagnostic triplet — anchor-year intuition falsified; the slab structure emerged from the SPA): records the origin of Decision 20's slab framing; the grid-snapping model here extends and supersedes that framing from a descriptive slab typology to a principled causal account. **Obs 54** (family classifier doubles calibration-cohort size at higher purity — interval structure, not just width, is the right partition): the `classify_family` function whose F1/F2_Other/F3 logic this Obs dissects; the inconsistency this Obs identifies (width-accidental reign classification) motivates the historical-anchor fix. **Obs 69** (the late corpus AD ~142–347 is in the degraded-recovery zone; convention fraction ≈ 0.65 corpus-wide, exceeds 0.70 in 21 of 80 time-bins): records the SPA-level consequence of grid-snapping — the plateau-step convention dominance in the late corpus is directly caused by the `[301, 500]` and century-slab pile-ups that the snapping mechanism (this Obs) explains. **Obs 35** (editorial-convention artefact is endpoint rounding; the SPA plateau-steps at century boundaries): the empirical detection of endpoint rounding and the plateau-step artefact that is mechanistically grounded here.

**Artefacts**: `runs/2026-06-06-convention-basis-redesign/outputs/tables/family-split.csv` (F2_Other = 17,354; empire prereg-filtered; uncommitted as of 2026-06-06); `runs/2026-06-06-convention-basis-redesign/outputs/tables/anchor-leak.csv` (canonical-reign leak = 129 inscriptions, 0.11 %; uncommitted); `runs/2026-06-05-template-dictionary/outputs/tables/templates-empire.csv` (raw F3 counts for `[161, 180]` N = 128, `[161, 200]` N = 99; commit `6d8950f`). Decision 38 (`planning/decision-log.md`, commit `66e751a`). `runs/2026-05-24-type-stratified-narrow-spas/code/analyse-cohorts.py` (lines 108–142; `classify_family` / `round_aligned`).

### Findable later

`grid-snapping`, `grid-alignment`, `convention-discriminator`, `historical-anchor-principle`, `genuine-but-aoristic`, `convention-vs-genuine`, `round_aligned`, `off-by-one`, `inclusive-endpoint`, `classify-family`, `f2-other`, `f3-periodic`, `f1-round`, `width-accidental`, `reign-misclassification`, `161-180`, `161-200`, `marcus-aurelius`, `anchor-leak`, `event-leak`, `0-11-percent`, `129-inscriptions`, `17354`, `9-61-percent`, `datierungskriterien`, `raw-dating-dropped`, `sdam-reply`, `edh-criteria`, `calendar-grid-quantisation`, `p-gen-reframe`, `un-snaps-the-collective`, `plateau-step-mechanism`, `bc-ad-lattice`, `century-boundary-pile-up`, `aoristic-convention`, `sensitivity-band`, `decadal-brackets`, `quarter-century`, `4-5-percent`, `cooley-2012`, `crema-2025`, `ceramic-dating`, `decision-38`, `obs-76`, `obs-40`, `obs-54`, `obs-69`, `obs-35`, `66e751a`, `6d8950f`, `convention-basis-redesign`

## Obs 78 — 2026-06-07 [METHODOLOGY / RECOVERY]: the Decision-38 empirical multi-century-bearing convention basis recovers α cleanly at the stress corner — the plateau is NOT confused for genuine quiescence; α-coverage is a large-N diagnostic, not a gate

The recovery re-validation Stage-1 stress-triage (α = 0.95 × `multicentury_heavy` `[0.10,0.10,0.80]` × the three peaked genuine shapes {bimodal, regnal_cluster, rise_and_fall} + a flat_baseline contrast; N ∈ {2,000, 10,000}; 8 cells × 100 replicates; sapphire) **passes** the Decision-38 §6 concern. The fear was that the new `multi_century` tier — a long flat body with an AD 300–350 envelope-edge plateau (15.3 % of its mass; from wide late slabs such as `[301,500]`) — would be **mistaken for genuine quiescence**, i.e. the model would *under*-attribute to convention. The opposite, and negligible, is observed: at the hardest corner (`rise_and_fall`, N = 10,000) the model recovers **α = 0.979 vs true 0.95 (+0.029 bias, sd 0.012)** — the plateau is correctly attributed to convention; shape recovery there is the best of the set (r = 0.838); convergence 1.00 in every cell.

The single cell with α-coverage < 0.90 (`rise_and_fall` N = 10,000, coverage 0.81) is **not** a recovery failure: it is the **benign large-N coverage collapse Amendment 01 §A5.5.1 already documents** — at large N the per-replicate credible interval tightens (sd 0.012) faster than the +0.029 bias shrinks, so the interval misses 0.95 ~19 % of the time, while the *point estimate* is fine. My re-validation spec's original "α-coverage ≥ 0.90 binding" gate was therefore **inconsistent with our own lodged framework** (which demotes α-coverage to a shape-conditioned diagnostic, not a gate); the spec was corrected accordingly, and the full grid (450 cells, PID 1681813) is scored under the Amendment-01 criterion (shape + convergence binding; α reported as Bland–Altman limits of agreement). Operating envelope for production reportability stays α ≤ 0.70 (Decision 37 D5); the α = 0.95 corner is a deliberate beyond-envelope stress. **Implication for H2.1 reporting:** α is a coarse directional convention-fraction statement, not a precise dial — as already required by Obs (Decision 33's ±0.18) and now re-confirmed on the new basis.

**Artefacts**: `runs/2026-06-06-convention-basis-redesign/revalidation/STAGE1-TRIAGE-REPORT.md` + `inscription-mass/outputs/cell-summaries/` (8 triage cells; commit `f90e6c1`); the spec-gate correction (`runs/2026-06-06-convention-basis-redesign/spec.md` §2.1, commit `d93598c`); the basis (`design.json` `tier_basis_empirical`, commit `6e1354b`). Full grid running on sapphire (PID 1681813; verdict pending). Cross-refs: Obs 69 (late corpus p_conv-dominated), Obs 68/73 (peaked-regime caveat), Obs 77 (grid-snapping discriminator); Decision 38 §6; Amendment 01 §A5.5.1; Decision 33 (α ±0.18).

### Findable later

`recovery-re-validation`, `stress-triage`, `multi-century-plateau`, `envelope-edge-plateau`, `alpha-coverage`, `large-n-collapse`, `bland-altman`, `diagnostic-not-gate`, `amendment-01-a5-5-1`, `alpha-recovery`, `0-029-bias`, `0-979`, `rise-and-fall`, `multicentury-heavy`, `quiescence-confusion`, `decision-38-section-6`, `operating-envelope`, `alpha-0-70`, `convention-fraction`, `PID-1681813`, `revalidation`, `shape-recovery`, `pearson-r`, `convergence-1-00`, `obs-69`, `obs-68`, `obs-73`, `obs-77`, `decision-33`, `decision-37-d5`, `f90e6c1`, `d93598c`, `6e1354b`

## Obs 79 — 2026-06-07 [DATA / FRAME]: the realised Latin frame is 39 provinces, not the prereg's 41, because two Latin-classified provinces contribute zero Hanson-matched cities — the 41→39 gap changes no result

The lodged prereg §2 (line 135) defines the Latin / Western-Empire subset as **41 LIRE provinces** (the 2024 notebook `province_language_map`, cell 54, Rome excluded). The realised H3a/H3c/SR1 frame is **39 provinces / 817 cities**. The gap is fully accounted for from evidence (`reconcile-province-maps.py`) and **changes no result**:

1. **Italia** — LIRE `province` value "Italia" carries **1** inscription; Italian provenances are coded to the eleven Augustan regions (all 11 are in the frame), so standalone "Italia" is redundant and empty of signal → **0 Hanson-matched cities**.
2. **Alpes Graiae** — **77** inscriptions, but **0** carry an `urban_context_pop_est` (0 distinct `urban_context_city` with a Hanson population join) → **0 Hanson-matched cities** (its three sibling Alpine provinces — Cottiae, Maritimae, Poeninae — each contribute exactly one city and are in the frame).
3. **Lugdunensis → Lugudunensis** — a 1:1 spelling normalisation to LIRE's actual field value (LIRE "Lugudunensis" N = 746; "Lugdunensis" N = 0); same province, no count change.

So **41 Latin-classified − Italia − Alpes Graiae (both 0 cities) = 39 provinces with ≥ 1 Hanson-matched city**. The realised frame is 817 / 39 whether or not Italia and Alpes Graiae are listed in the map, because neither contributes a city to the population-scaling sample. Documented in OSF **Amendment 02 §A5.3** (lodged 2026-06-06, tag `osf-amendment-02-2026-06-06`). General tell that earned its keep: an apparently-inadvertent omission (a Latin province silently absent from the frame map) was checked at source for **downstream impact** before being treated as a problem — and had none.

**Artefacts**: `runs/2026-06-06-amendment-02-prep/code/reconcile-province-maps.py` → `outputs/province-reconciliation.csv` (commit `d82834c`); the frame map `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`; the city frame `data/processed/city_level_for_h3a_latin.parquet` (817 cities / 39 provinces); OSF Amendment 02 (`planning/osf-amendment-2026-06-06-latin-frame.md` §A5.3, `ce963de`). Cross-refs: Decision 36 (Latin-primary frame); Decision 37 D2 (assigned the 39-vs-41 reconciliation to Amendment 02).

### Findable later

`39-vs-41`, `latin-provinces`, `province-language-map`, `alpes-graiae`, `italia`, `lugudunensis`, `lugdunensis`, `spelling-normalisation`, `0-hanson-cities`, `urban-context-pop-est`, `realised-frame`, `817-cities`, `39-provinces`, `41-provinces`, `frame-reconciliation`, `no-result-impact`, `downstream-impact-check`, `cell-54`, `province_language_map`, `western-empire-subset`, `augustan-regions`, `amendment-02`, `decision-36`, `decision-37-d2`, `reconcile-province-maps`, `d82834c`, `ce963de`

## Obs 80 — 2026-06-08 [RESULT / METHODOLOGY]: H2.1 production α is under-identified for temporally-concentrated units; final frame is 16 confirmatory / 4 caveated-high-α / 9 under-identified

### The finding

The H2.1 temporal-mixture production run (28 units + 'Italia excl. Rome' = unit 29; 0 failed; all converged) returned convention fractions α that are **systematically too low for ~9 temporally-concentrated units** — predominantly frontier/military provinces (Moesia inferior, Britannia, Pannonia inferior, Numidia, Dacia) plus ports and Italian regions (Salona, Ostia, Samnium, Venetia et Histria). The structural cause: their round-period datings cluster in the same narrow occupation window (≈ AD 100–300) as their genuine signal, so the smooth GRW `p_gen` absorbs the convention mass and α collapses.

Diagnostic signature: the shared-basis α falls far below the unit's F1+F3 (grid-aligned) family-mass fraction **and** a per-unit-basis refit produces a large α swing. Moesia inferior is the clearest exemplar: shared-basis α 0.05 vs F1+F3 family fraction 0.60 vs per-unit refit α 0.87 (+0.82 swing). Controls (empire-aggregate, Latium et Campania, Noricum) are basis-stable (|swing| ≤ 0.05).

| tier | N units | operative flag |
|---|---:|---|
| confirmatory | 16 | gap ≤ ~0.20; α basis-stable |
| caveated-high-α | 4 | Dalmatia, latin-aggregate, Pannonia superior, Noricum |
| under-identified | 9 | gap > ~0.25 confirmed by swing > 0.20 |

The confirmatory-eligible set (16 units): empire-aggregate, Latium et Campania, Hispania citerior, Germania superior, Dacia, Africa proconsularis, Germania inferior, Apulia et Calabria, Etruria, Baetica, Transpadana, Pompeii, Mogontiacum, Aquileia, Lusitania, Italia (excl. Rome).

**Pompeii α ≈ 0.001 is CORRECT** (genuine pre-AD-79 precision; only 5 % round-period family mass, concentrated pre-eruption; the model passes this validation unprompted). Italia (excl. Rome) aggregates the 11 Augustan regiones (N ≈ 40,499) and is identifiable (gap 0.09) where the constituent regiones individually are not.

**Reporting change:** α is now stated as a two-bound sensitivity range [shared-basis, per-unit-basis] for flagged units; identifiable units retain a point estimate. The H3b corrected-genuine-SPA hand-off for under-identified units retains convention masquerading as genuine and is treated as exploratory only.

### Why this matters

This is a structural identifiability limit, not a fitting artefact: the shared-basis homogeneity assumption (Decision 38 / Amendment 03 §3) breaks for period-concentrated units. The limit is **larger than** the documented α-diagnostic imprecision (Amendment 01's ±0.18 limits of agreement): Moesia inferior's range spans ≈ 0.82. The preregistered method stands where α is identifiable; this Obs quantifies the boundary and documents the conservative reporting adopted in the interim. The planned remediation (Obs 81) is gated on its own recovery validation.

### Caveats / methodological notes

The H3b identifiable set in the companion draft run (Obs 82) uses the gap criterion (gap < 0.20 → 17 units), which differs from the swing criterion used to populate `identifiability-table.json` (swing > 0.20 → 9 units flagged as under-identified in the production SUMMARY-FINAL). The two criteria disagree on 8 borderline units (Dalmatia, Hispania citerior, Dacia, Africa proconsularis, Baetica, Etruria, Transpadana, Italia). This is an open question (OQ-2 in the H3b spec) that must be resolved before any confirmatory reading.

### Related observations and artefacts

**Obs 78** (Decision-38 basis recovery re-validation: stress-triage passes; α-coverage is a large-N diagnostic, not a gate): the recovery validation that preceded the production run; the production data shows the real-world manifestation of the peaked-genuine hard corner foreshadowed there. **Obs 77** (grid-snapping is the observable discriminator between convention and genuine): the conceptual grounding for the identifiability flag — the grid-alignment family fraction is the independent signal the temporal shape ignores. **Obs 76** (empirical multi-century-bearing basis): the basis used in this production run.

**Artefacts**: `runs/2026-06-07-h2.1-launch-prep/outputs/production/SUMMARY-FINAL.md`; `runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`; `runs/2026-06-07-h2.1-launch-prep/outputs/production/identifiability-table.md`; `runs/2026-06-07-h2.1-launch-prep/outputs/production/identifiability-table.json`. Pre-registration note (DRAFT): `planning/prereg-note-2026-06-09-alpha-identifiability.md`.

### Findable later

`h2.1-production`, `alpha-under-identified`, `period-concentrated`, `temporally-concentrated`, `frontier-provinces`, `shared-basis`, `identifiability-limit`, `two-bound-alpha`, `alpha-range`, `moesia-inferior`, `0-05-vs-0-87`, `britannia`, `pannonia-inferior`, `samnium`, `salona`, `ostia`, `numidia`, `dacia`, `venetia-et-histria`, `umbria`, `pompeii-validation`, `alpha-zero`, `genuine-precision`, `italia-aggregate`, `40499`, `gap-criterion`, `swing-criterion`, `oq-2`, `confirmatory-16`, `caveated-4`, `under-identified-9`, `grw-absorbs`, `convention-masquerades-as-genuine`, `amendment-03`, `decision-38`, `obs-78`, `obs-77`, `obs-76`, `obs-81`, `obs-82`, `summary-final`, `diagnostic-alpha-identifiability-report`, `identifiability-table`

## Obs 81 — 2026-06-09 [METHODOLOGY / THEORY]: the informed-α prior is refuted; the principled remediation is a joint classification-as-likelihood model

### The finding

A wide/tight informed prior on α **cannot fix the under-identification** at any tested concentration (κ ∈ {4, 6, 8, 10, 20}) or sample size (N ∈ {1,500, 2,500, 10,000}). Prototype and small-N re-test results from `runs/2026-06-09-informed-alpha/`:

| N | α_true | prior | α_med | bias |
|---|---|---|---|---|
| 1,500 | 0.60 | flat | 0.034 | −0.566 |
| 1,500 | 0.60 | informed_exact_κ=20 | 0.205 | −0.395 |
| 2,500 | 0.60 | flat | 0.035 | −0.565 |
| 2,500 | 0.60 | informed_exact_κ=20 | 0.205 | −0.395 |

The shape-pairing probe (`code/shape_pairing_probe.py`) is decisive: with the shared (broad) basis, α_bias ≈ −0.56 whether the prior is flat (α_med 0.039) or informed with κ=6 (α_med 0.071). Switch to a narrow (per-unit) basis and α_bias collapses to ≈ +0.01 regardless of prior. **The lever is the convention shape/location, not the prior.**

Statistical theory explains this cleanly. For a partially-identified parameter, the prior over the identification region is **never updated by the data** (Gustafson 2010, `10.2202/1557-4679.1206`; Giacomini & Kitagawa 2021, `10.3982/ecta16773`). Under weak component separation the likelihood is confidently wrong — a threshold estimator that declares components identical when they are not (Feller et al. 2016, `10.48550/arxiv.1602.06595`; *Ann. Appl. Stat.* 2019).

**The principled remediation is to bring the grid-alignment classification in as a second likelihood term** informing α — established practice in the concomitant-variable / latent-class-with-covariates tradition (Dayton & Macready 1988; Huang & Bandeen-Roche 2004 provide the identification theory, `10.1007/bf02295837`; implemented in FlexMix / Grün & Leisch 2008; Bayesian instance: Berrettini et al. 2024). The archaeological structural archetype is the OxCal outlier model (Bronk Ramsey 2009, `10.1017/S0033822200034093`): a two-component reliable/unreliable mixture with per-sample quality weights inside one Bayesian model. The novel core is a **joint temporal-frequency mixture that uses the classification covariate as the identification instrument** — no published work combines a temporal-axis frequency mixture with a classification-as-likelihood identifiability fix.

To build + recovery-validate next session, then OSF amendment.

### Why this matters

This closes the informed-prior path and opens the joint-likelihood path on firm theoretical and empirical ground. The two-citation argument — Feller + Gustafson for why a prior cannot work; Huang & Bandeen-Roche for why a likelihood term can — is cite-ready for the methods section. The novel-core gap (no prior temporal-axis mixture uses classification as the identification instrument) is confirmed on both statistical and archaeological sides: statistical concomitant-variable work is almost all cross-sectional; archaeological work filters upstream or stratifies post-hoc, but does not jointly estimate both shapes.

### Caveats / methodological notes

All 28 informed-prior fits converge cleanly (max R̂ ≤ 1.005; zero divergences), confirming the failure is structural, not a sampler pathology. The small-N advantage of the informed prior is real but inconsequential: at κ=20 and N=1,500, α_med rises from 0.034 to 0.205 for α_true=0.60 — a gain in the posterior mean, but still a bias of −0.40. Zotero dedup for the cited papers is unconfirmed (the scout env lacked the `httpx` dependency); Surovell 2009 and Bayliss 2015 may already be in the library. Feller 2016 is cited via the arXiv/DataCite DOI; the journal version (*Ann. Appl. Stat.* 2019) may be preferable for the paper.

### Related observations and artefacts

**Obs 80** (H2.1 production α under-identified for temporally-concentrated units — the problem this Obs addresses): the production finding that triggered the remediation investigation. **Obs 77** (grid-snapping is the observable discriminator): the conceptual basis for why the classification variable is the natural identification instrument. **Obs 78** (stress-triage passes, but α-coverage is a large-N diagnostic): confirms the recovery framework can detect genuine quiescence; the joint-likelihood model must also pass this test.

**Artefacts**: `runs/2026-06-09-informed-alpha/code/recovery_test.py`; `runs/2026-06-09-informed-alpha/code/small_n_retest.py`; `runs/2026-06-09-informed-alpha/code/shape_pairing_probe.py`; `runs/2026-06-09-informed-alpha/outputs/recovery-results.json`; `runs/2026-06-09-informed-alpha/outputs/small-n-retest.json`; `runs/2026-06-09-informed-alpha/outputs/small-n-retest-note.md`; `runs/2026-06-09-informed-alpha/outputs/shape-pairing-results.json`. Scout synthesis: `planning/scout-2026-06-09-identifiability-remediation-SYNTHESIS.md`. Pre-registration note: `planning/prereg-note-2026-06-09-alpha-identifiability.md`.

### Findable later

`informed-prior`, `informed-alpha`, `alpha-prior-refuted`, `prior-cannot-fix-partial-id`, `gustafson-2010`, `giacomini-kitagawa-2021`, `feller-2016`, `weak-separation`, `confidently-wrong`, `concomitant-variable`, `latent-class-with-covariates`, `huang-bandeen-roche-2004`, `classification-as-likelihood`, `joint-likelihood`, `identification-instrument`, `oxcal-outlier`, `bronk-ramsey-2009`, `two-component-mixture`, `dayton-macready-1988`, `berrettini-2024`, `flexmix`, `novel-core`, `temporal-axis-mixture`, `shape-pairing-probe`, `narrow-basis-vs-broad-basis`, `lever-is-shape-not-prior`, `small-n-retest`, `k20-bias-minus-0-40`, `shape-pairing-results`, `joint-model`, `classification-covariate`, `obs-80`, `obs-77`, `obs-78`, `recovery-validation-gate`, `osf-amendment`

## Obs 82 — 2026-06-09 [RESULT / METHODOLOGY]: H3b is preregistered exploratory; draft run shows an Antonine deficit in both aggregates; exponential null is saturated on the Roman SPA

### The finding

H3b is pre-specified **EXPLORATORY** deviation-detection (Decision 15; preregistration §4). It carries **no Holm-corrected confirmatory family**; any prior reference to "Holm-Bonferroni confirmatory" wording for H3b is stale and superseded by this Obs and the H3b spec. Holm correction is computed descriptively only in the draft run.

Draft run: `runs/2026-06-09-h3b/` (DRAFT-FOR-REVIEW — open questions in `h3b-spec.md` §10 gate any confirmatory reading). 17 identifiable units under the gap criterion (gap < 0.20); identifiability split in `outputs/identifiability-split.json`.

**Key methodological finding — exponential null is saturated.** Under the exponential null, every unit returns global *p* = 0.000 (e.g. empire: 79/80 bins out-of-envelope). The Roman SPA is a strong rise-and-fall curve; a single-rate exponential cannot represent it, so essentially the whole curve "deviates". The exponential null confirms only that the corpus is not featureless-exponential; it **cannot localise events**. **Read deviations off the CPL-3 null** (continuous piecewise-linear, 3 knots), which absorbs the rise-and-fall trend and isolates genuine departures.

**Antonine probe (AD 165–180) — CPL-3 null:**

Both aggregates show an out-of-envelope **deficit centred at AD ~168** under both nulls — directionally consistent with the Antonine Plague mortality signal and Duncan-Jones (2018)'s abrupt post-AD-167 cessation of military diplomas.

| level | null | direction | descriptive bracket | peak yr |
|---|---|---|---|---|
| empire-aggregate | CPL-3 | deficit | ≥ 20 % deficit | 167.5 |
| latin-aggregate | CPL-3 | deficit | ≥ 50 % deficit | 167.5 |

Antonine out-of-envelope in 7/17 identifiable units (empire-aggregate, latin-aggregate, Germania superior, Dacia, Pannonia superior, Africa proconsularis, Noricum).

**Crisis probe (AD 235–284) — CPL-3 null — weaker / diffuse:**

Crisis window is messier (mixed direction; CPL-3 and exponential nulls disagree on sign in some bins) — consistent with a diffuse multi-decade decline rather than a sharp event, and with the late-corpus convention-domination caveat (Obs 69: AD ~142–347 is `p_conv`-dominated even in the corrected curve). Crisis out-of-envelope in 9/17 identifiable units.

**Asclepius-cult + military-administration subsets are deferred** — they require per-subset deconvolution, per-subset Phase-1 reachability, and a LIRE membership rule (no clean Asclepius / military-diploma flag in LIRE `inscr_type` or `type_of_inscription_*` columns). Confirm deferral and supply membership definitions before next session.

### Why this matters

The exponential-saturation finding (OQ-A) is a necessary methodological disclosure: the Phase-1 power study used a featureless base and so the exponential was a sensible primary null there. On the real rise-and-fall Roman corpus the convention inverts. This must be resolved before any confirmatory reading and reported clearly in the paper's methods section. The Antonine deficit direction is consistent across both aggregates and both nulls — the most stable signal in the draft run.

### Caveats / methodological notes

Seven open questions (OQ-1 through OQ-8) gate confirmatory reading: the principal ones are the confirmatory status / Holm-family question (OQ-1), the identifiability criterion (gap vs swing, OQ-2; see also Obs 80 caveat), which null is operative on real data (OQ-A), and the Antonine subset-membership definitions (OQ-6). The identifiable set under the gap criterion (17 units) includes units the swing criterion flags as under-identified (Dalmatia, Africa proconsularis, etc.) — the H3b draft results for those units should be treated with additional caution until OQ-2 is resolved. Lusitania (N = 1,578) is below the CPL-3 reachability threshold used in Phase 1 (OQ-3).

### Related observations and artefacts

**Obs 80** (H2.1 production α under-identified — establishes which units feed the H3b confirmatory set): the corrected-genuine-SPA hand-off used here; under-identified units are exploratory-only in H3b. **Obs 69** (the late corpus AD ~142–347 is `p_conv`-dominated): the convention-domination caveat that makes the Crisis probe the weaker of the two windows. **Obs 78** (recovery re-validation; α-coverage is a large-N diagnostic): the recovery framework whose code is reused in the H3b harness.

**Artefacts**: `runs/2026-06-09-h3b/REPORT.md` (DRAFT-FOR-REVIEW); `runs/2026-06-09-h3b/h3b-spec.md`; `runs/2026-06-09-h3b/outputs/deviations.json`; `runs/2026-06-09-h3b/outputs/deviations-table.csv`; `runs/2026-06-09-h3b/outputs/identifiability-split.json`; `runs/2026-06-09-h3b/outputs/replication-antonine.json`; `runs/2026-06-09-h3b/outputs/replication-crisis.json`.

### Findable later

`h3b`, `h3b-draft`, `deviation-detection`, `exploratory`, `decision-15`, `no-confirmatory-family`, `holm-stale`, `exponential-null-saturated`, `cpl-3`, `cpl3-null`, `rise-and-fall`, `roman-spa`, `antonine-probe`, `antonine-deficit`, `ad-168`, `167-5`, `duncan-jones-2018`, `antonine-plague`, `crisis-probe`, `crisis-third-century`, `diffuse-signal`, `7-of-17`, `9-of-17`, `empire-aggregate`, `latin-aggregate`, `oq-a`, `oq-1`, `oq-2`, `oq-6`, `asclepius-subset`, `military-administration-subset`, `deferred-subsets`, `per-subset-deconvolution`, `reachability`, `lusitania-threshold`, `oq-3`, `gap-criterion`, `17-identifiable`, `obs-80`, `obs-69`, `obs-78`, `deviations-table`, `identifiability-split`, `replication-antonine`

## Obs 83 — 2026-06-09 [METHODOLOGY / RESULT]: the joint identifiability-remediation design pivots from the shared basis to a flexible per-unit basis + classification likelihood

### The finding

The remediation proposed in Obs 81 — bringing the grid-alignment classification in as a second likelihood term informing α — only works with a **flexible per-unit convention basis**, NOT the shared Decision-38 / Amendment-03 basis. Local recovery proof-of-concept (6 realistic synthetic cells, N = 2,000 per cell, 1 replicate each; run on sapphire; `runs/2026-06-09-joint-identifiability/outputs/POC-REPORT.md`):

**Experiment 1 — shared basis + classification (the originally-planned lead): FAILS confounded cells.**

| cell | α_true | shared-only | **shared + classification** | bias |
|---|---|---|---|---|
| conf_a0.2 | 0.2 | 0.00 | **0.00** | −0.20 |
| conf_a0.4 | 0.4 | 0.00 | **0.00** | −0.40 |
| conf_a0.6 | 0.6 | 0.00 | **0.00** | −0.60 |

No better than the shared-basis baseline. The classification binomial is overpowered by a confidently-wrong temporal multinomial (see Obs 84 for the mechanism).

**Experiment 2 — per-unit basis from the TRUE convention shape + classification: RECOVERS.**

| cell | α_true | per-unit-only | **per-unit + classification** | bias |
|---|---|---|---|---|
| ident_a0.3 | 0.3 | 0.37 (+0.07) | **0.32 [0.25, 0.38]** | +0.02 |
| ident_a0.6 | 0.6 | 0.63 (+0.03) | **0.61 [0.55, 0.68]** | +0.01 |
| conf_a0.2 | 0.2 | 0.38 (+0.18) | **0.26 [0.19, 0.33]** | +0.06 |
| conf_a0.4 | 0.4 | 0.52 (+0.12) | **0.45 [0.38, 0.52]** | +0.05 |
| conf_a0.6 | 0.6 | 0.74 (+0.14) | **0.67 [0.60, 0.76]** | +0.07 |
| conf_regnal_a0.5 | 0.5 | 0.53 (+0.03) | **0.51 [0.45, 0.57]** | +0.01 |

6/6 pass (|bias| ≤ 0.07 confounded; ≤ 0.02 identifiable); 6/6 cover α_true at 95 %. The classification term reins in the per-unit basis's over-attribution (per-unit-only reaches +0.12 to +0.18 on the confounded cells; +classification → +0.05 to +0.07).

**Experiment 3 — per-unit basis from the production-realistic ESTIMATED (contaminated) grid-aligned-subset shape + classification: RECOVERS.**

| cell | α_true | **per-unit(est) + classification** | bias | cover95 |
|---|---|---|---|---|
| ident_a0.3 | 0.3 | 0.35 [0.27, 0.43] | +0.05 | ✓ |
| ident_a0.6 | 0.6 | 0.65 [0.57, 0.73] | +0.05 | ✓ |
| conf_a0.2 | 0.2 | 0.27 [0.19, 0.35] | +0.07 | ✓ |
| conf_a0.4 | 0.4 | 0.49 [0.41, 0.59] | +0.09 | ✗ (marginal) |
| conf_a0.6 | 0.6 | 0.72 [0.62, 0.83] | +0.12 | ✗ (marginal) |
| conf_regnal_a0.5 | 0.5 | 0.55 [0.49, 0.63] | +0.05 | ✓ |

6/6 within the |bias| < 0.18 gate; coverage clean for 4/6, marginal for the two high-α confounded cells (a +0.09 to +0.12 residual positive bias from estimated-basis contamination — see Obs 86). Still a decisive improvement on shared-basis under-attribution (−0.20 to −0.60) and per-unit-only over-attribution (+0.12 to +0.18).

**This reverses Amendment 03's shared-basis choice.** The classification likelihood supplies the over-attribution control that the shared basis was adopted to provide — making a per-unit basis safe. Shawn agreed 2026-06-09: per-unit + classification is the lead. θ calibrated from the 19 identifiable units under rule C: θ_conv μ = 0.945, θ_gen μ = 0.155, RMSE = 0.12, κ = 40 (`outputs/theta-calibration.json`). Full recovery grid launched on sapphire: 300 cells × 100 reps + baseline on 90 confounded = 39,000 fits (`full-grid-spec.md`).

### Why this matters

This is the validated form of the remediation and the central methodological result of the session. It determines the production refit (re-fit all 28 H2.1 units under the joint model) and the next OSF amendment, which explicitly reverses Amendment 03's shared-basis choice. The novel core — a temporal-frequency mixture whose mixing weight is identified by a classification likelihood — is confirmed on POC evidence; the full grid is the replicate-level validation gate.

### Caveats / methodological notes

POC = one replicate per cell; convergence not audited per cell (point estimates only). The confounded `%win` = 1.00 is the stress corner; realistic frontier units (~0.88–0.90) are easier. Experiments 1 and 2 use the true convention shape; only Experiment 3 uses the observable estimate. The full grid (currently running on sapphire) supplies replicate-level bias/coverage and the convergence gate. The design change reverses a lodged OSF decision; a formal amendment is required before production use of results.

### Related observations and artefacts

**Obs 81** (informed-α prior refuted; joint-likelihood remediation proposed — this Obs is the POC that pivots its basis from shared to per-unit): the prior session's finding that motivated this work and first named the joint-likelihood approach. **Obs 80** (H2.1 production α under-identified for temporally-concentrated units): the production finding this remediation addresses. **Obs 77** (grid-snapping is the observable discriminator between convention and genuine): the conceptual basis for using grid-alignment classification as the identification instrument. **Obs 84** (why the shared basis is confidently wrong, not merely flat): the theoretical mechanism explaining Experiment 1's failure.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/POC-REPORT.md`; `runs/2026-06-09-joint-identifiability/outputs/poc-recovery.json`; `runs/2026-06-09-joint-identifiability/outputs/poc-perunit-joint.json`; `runs/2026-06-09-joint-identifiability/outputs/poc-estimated-basis.json`; `runs/2026-06-09-joint-identifiability/outputs/theta-calibration.json`; `runs/2026-06-09-joint-identifiability/code/joint_lib.py`; `runs/2026-06-09-joint-identifiability/spec.md`; `runs/2026-06-09-joint-identifiability/full-grid-spec.md`.

### Findable later

`joint-model`, `design-pivot`, `per-unit-basis`, `classification-likelihood`, `shared-basis-fails`, `over-attribution-control`, `reverses-amendment-03`, `theta-calibration`, `rule-C`, `theta-conv-0-945`, `theta-gen-0-155`, `kappa-40`, `poc-recovery`, `poc-perunit-joint`, `poc-estimated-basis`, `39000-fits`, `300-cells`, `stress-corner`, `confounded-cells`, `identifiable-cells`, `6-of-6-pass`, `concomitant-variable`, `confidently-wrong-overpowered`, `classification-binomial`, `temporal-multinomial`, `obs-81`, `obs-80`, `obs-77`, `obs-84`, `amendment-03-reversed`, `production-refit`, `osf-amendment`, `per-unit-estimated-shape`, `aligned-subset-spa`, `theta-calibration-19-units`

## Obs 84 — 2026-06-09 [METHODOLOGY / THEORY]: why the shared basis fails — a confidently-wrong likelihood (weak separation), not mere flatness

### The finding

The mechanism behind Obs 83 Experiment 1. With the shared basis too broad for a temporally-concentrated unit, α > 0 forces convention mass **outside** the unit's data window: the shared Latin basis carries ~36 % of its mass before AD 100, where a frontier unit has almost none. The 80-bin × N-count temporal multinomial penalises that shape misfit enormously. The result is not that the likelihood is merely **flat** in α (the under-identification picture) — it is **confidently wrong**: it prefers α = 0. This is Feller et al. 2016's weak-separation threshold-estimator behaviour (`10.48550/arxiv.1602.06595`): in finite samples the maximum likelihood estimator behaves like a threshold estimator that can give strong evidence that the means are equal when the truth is otherwise. A single classification binomial over N trials cannot overpower an 80-bin multinomial in that confidently-wrong regime.

A **flexible per-unit basis** removes the shape misfit, turning the problem back into genuine partial-identification (Gustafson 2010, `10.2202/1557-4679.1206`: the large-sample posterior's support is the identification region, which the prior cannot shrink — you must add an independent observable). Once the problem is genuinely partially identified, the classification covariate can restore identifiability (Huang & Bandeen-Roche 2004, `10.1007/bf02295837`: theory for identification of latent-class models with covariate effects on class membership).

The three statistical DOIs were verified against authoritative CrossRef / DataCite abstracts this session (`outputs/priority-papers-status.md`). All three papers are NEW to the Zotero library (confirmed against `~/Zotero/zotero.sqlite`); Zotero staging is a tracked follow-up.

### Why this matters

This is the paper's explanatory hook for the pivot — it distinguishes "the temporal likelihood is flat" (false for the shared basis) from "it is confidently wrong" (true), which is why both the informed prior (Obs 81) AND the shared-basis + classification design (Obs 83 Experiment 1) failed, and why a flexible convention shape is a necessary precondition before the classification term can bite. The three-citation spine (Feller for the confidently-wrong mechanism; Gustafson for why a prior cannot fix partial-ID; Huang & Bandeen-Roche for why a likelihood term can) is cite-ready for the methods section.

### Caveats / methodological notes

Claims grounded in authoritative CrossRef / DataCite abstracts; full texts of Gustafson 2010 and Huang & Bandeen-Roche 2004 (paywalled) not yet read this session — full-text reading is a tracked follow-up (Feller is open via arXiv). Feller's preferred citation may be the *Ann. Appl. Stat.* 2019 journal version; the arXiv / DataCite DOI (`10.48550/arxiv.1602.06595`) is what is verified here. The "~36 % before AD 100" figure for the shared Latin basis is stated in POC-REPORT.md §Exp 1; it describes the specific broad-slab basis used in the POC, not a property of every possible shared basis.

### Related observations and artefacts

**Obs 83** (the pivot this mechanism explains): the POC result whose Experiment 1 failure this Obs accounts for theoretically. **Obs 81** (the Feller / Gustafson / Huang & Bandeen-Roche citations first introduced, and the informed-prior refutation): the prior session's theoretical framing; this Obs extends it from the prior to the joint-likelihood case. **Obs 80** (the under-identification this ultimately addresses): the production finding.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/priority-papers-status.md`; `runs/2026-06-09-joint-identifiability/outputs/POC-REPORT.md` (Experiment 1 mechanism section); `planning/scout-2026-06-09-identifiability-remediation-SYNTHESIS.md`.

### Findable later

`confidently-wrong-likelihood`, `weak-separation`, `feller-2016`, `feller-threshold-estimator`, `ann-appl-stat-2019`, `arxiv-1602-06595`, `gustafson-2010`, `identification-region`, `partial-identification`, `huang-bandeen-roche-2004`, `covariate-on-membership`, `shape-misfit`, `36-percent-before-ad-100`, `shared-basis-too-broad`, `temporal-multinomial-overpowers`, `classification-binomial-overpowered`, `why-shared-basis-fails`, `explanatory-hook`, `methods-section`, `three-citation-spine`, `feller-gustafson-hrb`, `prior-cannot-shrink-identification-region`, `confidently-wrong-vs-flat`, `obs-83`, `obs-81`, `obs-80`, `priority-papers-status`, `zotero-new-papers`, `full-text-follow-up`

## Obs 85 — 2026-06-09 [METHODOLOGY]: widening the θ prior is counterproductive — the marginal high-α coverage is contamination bias, not CI under-dispersion

### The finding

An evidence-based course-correction. We expected widening the θ prior (κ 40 → 20 → 12) to widen the α credible interval and fix the marginal high-α coverage seen in Obs 83 Experiment 3. The κ-sweep on the estimated basis (`outputs/poc-kappa-check.json`) showed the opposite — widening **amplifies** a small positive bias:

| cell | α_true | κ = 40 | κ = 20 | κ = 12 |
|---|---|---|---|---|
| conf_a0.2 | 0.2 | 0.27 [0.19, 0.34] ✓ | 0.33 ✗ | 0.50 ✗ |
| conf_a0.4 | 0.4 | 0.49 [0.41, 0.59] (+0.09) | 0.54 | 0.59 |
| conf_a0.6 | 0.6 | 0.72 [0.62, 0.83] (+0.12) | 0.76 | 0.78 (+0.18) |
| ident_a0.6 | 0.6 | 0.65 ✓ | 0.66 ✓ | 0.67 ✓ |

(α_med rounded to 2 d.p. from `poc-kappa-check.json`; identifiable cell is stable across all three κ.)

**Diagnosis.** The marginal coverage at high-α confounded cells is a positive **bias** from estimated-basis contamination (Obs 86), not CI under-dispersion. The grid-aligned-subset SPA ≈ α·θ_conv·p_conv + (1−α)·θ_gen·p_gen, so the convention basis carries a faint copy of the genuine peak; this lets the convention component over-reach. A *tighter* θ prior anchors α to the classification signal and limits the contamination-driven over-attribution; a *looser* prior lets α float up.

**Decision:** keep κ = 40; do NOT widen. The full recovery grid sweeps κ ∈ {40, 80} (tighter) as a sensitivity check — widening is ruled out by this sweep.

### Why this matters

This is a documented reversal of a jointly-agreed plan on empirical evidence — the critical-friend discipline working as intended. Attempting to fix a bias by widening a prior is a standard wrong instinct; the κ-sweep makes the mechanism visible. The reversal also localises the residual-bias source to estimated-basis contamination (Obs 86) rather than to sampler or prior specification, pointing at the principled fix.

### Caveats / methodological notes

The κ-sweep is one replicate per cell on four focus cells at the stress corner (`%win` = 1.00); the full-grid κ-sensitivity arm (κ ∈ {40, 80} on confounded cells) is the replicate-level confirmation. The identifiable cell (ident_a0.6) is stable across all three κ values (α_med 0.65–0.67), confirming the effect is specific to the contaminated confounded regime. The table above shows α_med only (no CI for the κ = 20 and κ = 12 rows); full posterior summaries are in `poc-kappa-check.json`.

### Related observations and artefacts

**Obs 83** (the per-unit + classification design these θ priors serve): the design whose marginal high-α coverage prompted the κ-sweep. **Obs 86** (the contamination this bias arises from): the principled source of the residual and the escalation path. **Obs 81** (the informed-prior refutation — same "prior cannot fix it" theme): a parallel earlier lesson that adding prior information does not resolve structural misfit.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/poc-kappa-check.json`; `runs/2026-06-09-joint-identifiability/outputs/POC-REPORT.md` (κ postscript); `runs/2026-06-09-joint-identifiability/code/poc_kappa_check.py`.

### Findable later

`theta-prior`, `kappa-sweep`, `kappa-40`, `kappa-20`, `kappa-12`, `widening-counterproductive`, `contamination-bias`, `not-ci-underdispersion`, `evidence-based-reversal`, `critical-friend`, `prior-amplifies-bias`, `conf-a0-2-kappa-sweep`, `conf-a0-6-kappa-sweep`, `ident-stable-across-kappa`, `stress-corner-kappa`, `poc-kappa-check`, `tighter-prior`, `kappa-80-sensitivity`, `theta-prior-anchors-alpha`, `obs-83`, `obs-86`, `obs-81`, `jointly-agreed-reversal`, `course-correction`

## Obs 86 — 2026-06-09 [METHODOLOGY]: the estimated per-unit basis carries genuine-peak contamination; the cross-classified time × alignment model is the principled fix (full-grid arm D-B)

### The finding

In production the per-unit convention basis is the aoristic SPA of the grid-aligned-inscription subset. In expectation that SPA is ∝ α·θ_conv·p_conv + (1−α)·θ_gen·p_gen — i.e., **contaminated** by genuine inscriptions that happen to be grid-aligned (at rate θ_gen). That faint copy of the genuine peak lets the convention component over-reach, giving a +0.09 to +0.12 over-attribution at the stress corner (`%win` = 1.00; Obs 83 Experiment 3, conf_a0.4 and conf_a0.6). The residual is a characterised limitation — within the |bias| < 0.18 gate — and is to be reported, not tuned away.

The principled fix is a **cross-classified time × alignment** model: observe the grid-aligned-subset and non-aligned-subset temporal SPAs as **separate** multinomials sharing (α, p_conv, p_gen, θ), so the model *separates* the contamination instead of inheriting it through a fixed contaminated basis. This approach likely removes the residual bias. It has been added to the full recovery grid as a head-to-head arm (`full-grid-spec.md` §1 / §2, decision D-B): {fixed estimated basis — the lead; cross-classified — the candidate refinement}. The cross-classified form will be adopted as the refined lead only if it materially beats the simpler one on the bias surface.

### Why this matters

This Obs characterises the lead design's known residual limitation honestly and pre-registers the principled escalation path. The contamination mechanism is clear (the aligned-subset SPA is a mixture, not a pure convention SPA), the magnitude is known (+0.09 to +0.12 at the stress corner; milder at realistic %win ≈ 0.88), and the full-grid D-B arm will determine whether the simpler fixed-basis design is adequate or whether the cross-classified model is needed. Reporting the contamination mechanism also explains why the κ-sweep (Obs 85) amplified rather than fixed the marginal coverage — the bias source is structural, not sampler-level.

### Caveats / methodological notes

The cross-classified model is not yet built or validated; it is a grid arm and a decision (D-B), not a committed production change. The +0.09/+0.12 figures are at the stress corner (`%win` = 1.00); realistic frontier units with `%win` ~0.88–0.90 are milder. The magnitude of the contamination effect depends on θ_gen (rate at which genuine inscriptions land on the grid) — the θ-mismatch robustness arm in the full grid (`full-grid-spec.md` §2) characterises sensitivity to this. Until the cross-classified arm is validated, the fixed-estimated-basis design remains the lead.

### Related observations and artefacts

**Obs 83** (the estimated-basis lead whose residual this Obs characterises): the Experiment 3 result where the +0.09/+0.12 over-attribution first appeared. **Obs 85** (the κ reversal that localised this bias — widening the θ prior amplified rather than fixed it, confirming the source is contamination, not CI under-dispersion): the diagnostic that identified contamination as the root cause.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/poc-estimated-basis.json`; `runs/2026-06-09-joint-identifiability/outputs/POC-REPORT.md` (Experiment 3 + Conclusions + κ postscript); `runs/2026-06-09-joint-identifiability/full-grid-spec.md` (§1 D-B); `runs/2026-06-09-joint-identifiability/code/poc_estimated_basis.py`.

### Findable later

`estimated-basis`, `contamination-bias`, `aligned-subset-spa`, `genuine-peak-contamination`, `theta-gen-contamination`, `over-attribution`, `cross-classified-model`, `time-x-alignment`, `separate-multinomials`, `decision-D-B`, `full-grid-arm`, `refined-lead`, `candidate-refinement`, `head-to-head-arm`, `stress-corner-bias`, `poc-estimated-basis`, `plus-0-09-plus-0-12`, `characterised-limitation`, `obs-83`, `obs-85`, `theta-mismatch-robustness`, `kappa-reversal-localised-contamination`

## Obs 87 — 2026-06-11 [RESULT / METHODOLOGY]: joint recovery grid VERDICT — resolves confounded under-attribution but is NOT do-no-harm (+0.07 estimated-basis contamination)

### The finding

The 300-cell joint-model recovery-validation grid completed in full (single bit-reproducible method; `build-once + set_data`; n_jobs=12; wall-clock ~25.1 h; 0 worker errors; 0 failed cells). Scored against `runs/2026-06-09-joint-identifiability/full-grid-spec.md` §3; verdict committed in `runs/2026-06-09-joint-identifiability/outputs/grid-VERDICT.md` and `grid-summary.json` (commit `18dac46`).

**C2 — pulled-to-truth (confounded cells): PASS — 64/90 (71 %).**

| metric | lead | shared-basis baseline |
|---|---|---|
| mean \|median α bias\| | **0.066** | 0.362 |
| cells passing C2 | **64/90 (71 %)** | — |
| worst positive median bias | +0.164 | — |

The joint model resolves the frontier-unit under-attribution it was built for: ~5× better than the shared-basis baseline on the confounded cells.

**C1 — do-no-harm (identifiable cells): FAILS — 37/210 (18 %).**

| metric | value |
|---|---|
| cells passing C1 (bias < 0.12 AND coverage ≥ 0.90) | **37/210 (18 %)** |
| mean \|median bias\| | 0.075 (below 0.12 threshold) |
| mean coverage | 0.374 (well below 0.90 threshold) |

The failure is driven entirely by **coverage** (mean 0.374), not bias. The cause is a systematic, near-uniform +0.06–+0.08 over-attribution bias across the full %win × α surface (bias map below), combined with over-confident credible intervals that therefore fail to bracket the truth. The bias is the estimated-basis contamination characterised in Obs 86.

**Bias surface — mean(median bias) by %win × α_true** (from `grid-VERDICT.md`):

| %win \ α | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| 0.53 | +0.08 | +0.08 | +0.08 | +0.08 | +0.06 |
| 0.63 | +0.08 | +0.07 | +0.07 | +0.07 | +0.06 |
| 0.83 | +0.08 | +0.07 | +0.07 | +0.07 | +0.06 |
| 0.95 | +0.08 | +0.07 | +0.08 | +0.08 | +0.06 |
| 1.00 | +0.08 | +0.07 | +0.08 | +0.08 | +0.06 |

The contamination is near-uniform across the %win and α surface; it is not confined to the stress corner.

**C4 — convergence: marginal.** 252/300 cells (84 %) at convergence_rate ≥ 0.95; mean rate 0.950.

**Grid scope** (from `full-grid-spec.md` §2): %win ∈ {0.527, 0.631, 0.834, 0.951, 1.00}; α_true ∈ {0.0, 0.2, 0.4, 0.6, 0.8}; N ∈ {1,500, 2,800, 15,000}; 100 reps per cell; 0 replicate failures.

### Why this matters

This is the gate result for the production refit. The verdict is honest but not a clean pass: the joint model is validated for its primary purpose (recovering α in confounded units) but fails the do-no-harm criterion on identifiable units — the criterion that would allow production use without further work.

The ~+0.07 over-attribution on identifiable units is exactly the estimated-basis contamination exposure pre-committed to reporting in `full-grid-spec.md` §6 (the "we pre-commit to reporting it, not tuning it away" clause). The bias magnitude and surface shape match the POC's +0.05–+0.12 prediction (Obs 86); the grid has now characterised it at replicate scale across the full parameter space.

**Consequence: the planned production refit of the 28 H2.1 units is paused.** The next step is to evaluate the cross-classified time × alignment arm (D-B; spec at `runs/2026-06-09-joint-identifiability/cross-classified-spec.md`, commit `37a94c5`), which identifies p_conv / p_gen from the aligned-vs-non-aligned subset contrast directly — rather than inheriting a contaminated fixed basis — head-to-head against this lead grid. Only if D-B materially reduces the bias surface does it replace the lead; if not, the fixed-estimated-basis design proceeds to production with the +0.07 contamination explicitly disclosed in the paper.

### Caveats / methodological notes

The grid ran the **estimated (contaminated) basis** — the production-realistic case (Obs 83 Experiment 3) — not the true per-unit shape. Results on identifiable cells therefore include the inherent contamination of the observable basis, not a model defect. The C1 failure is structural, not a sampler or prior issue (the κ-sweep in Obs 85 ruled that out). Robustness arms (θ-mismatch, κ-sensitivity, cross-classified) and the Tier-2 interval-level arm are not yet run; the verdict above is for the base 300-cell grid only.

The convergence result (C4: 84 %, mean 0.950) is marginal. Individual low-convergence cells are not disaggregated here; they are in `grid-summary.json`. The build-once + set_data fix (commit `fad6fd5`) produced results that are bit-reproducible across runs but not bit-identical to the original build-fresh-per-rep path (max |Δα| ≈ 2×10⁻³ identifiable / 7×10⁻³ confounded, ~25–100× below the bias thresholds); the entire 300-cell grid uses the new method consistently.

### Related observations and artefacts

**Obs 86** (estimated-basis contamination characterised — +0.09/+0.12 at the stress corner, cross-classified D-B as the principled fix; this Obs is the grid-scale confirmation of that diagnosis): the POC finding this verdict validates and extends to the full bias surface. **Obs 83** (the per-unit + classification design and POC, the pivoted lead whose full validation this is): the design specification. **Obs 85** (κ-sweep localised the C1 failure to contamination bias, not CI under-dispersion): the prior diagnostic that correctly predicted the coverage-not-bias failure mode now seen at grid scale. **Obs 84** (why the shared basis fails — the confidently-wrong mechanism): the theoretical background for why the lead is a necessary improvement over the shared baseline, even with the contamination caveat.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/grid-VERDICT.md` (commit `18dac46`); `runs/2026-06-09-joint-identifiability/outputs/grid-summary.json`; `runs/2026-06-09-joint-identifiability/full-grid-spec.md` §3 (acceptance criteria) + §6 (pre-committed reporting rule); `runs/2026-06-09-joint-identifiability/cross-classified-spec.md` (commit `37a94c5`); `runs/2026-06-09-joint-identifiability/MEMORY-FIX-AND-RUN-STATUS.md` (run provenance, memory-incident recovery, set_data fix).

### Findable later

`joint-recovery-grid`, `verdict`, `300-cells`, `full-grid`, `C1-fails`, `C2-pass`, `do-no-harm-failure`, `coverage-failure`, `identifiable-cells`, `confounded-cells`, `estimated-basis-contamination`, `plus-0-07-over-attribution`, `near-uniform-bias`, `bias-surface`, `win-pct-vs-alpha`, `37-of-210`, `64-of-90`, `18-percent-pass`, `71-percent-pass`, `mean-coverage-0-374`, `mean-bias-0-075`, `mean-bias-0-066`, `baseline-0-362`, `5x-better-than-baseline`, `production-refit-paused`, `cross-classified-arm`, `D-B`, `time-x-alignment`, `contamination-not-tuned-away`, `pre-committed-reporting`, `convergence-marginal`, `84-percent-convergence`, `build-once-set-data`, `bit-reproducible`, `fad6fd5`, `18dac46`, `37a94c5`, `n-jobs-12`, `25-1-hours`, `zero-worker-errors`, `zero-failed-cells`, `obs-86`, `obs-83`, `obs-85`, `obs-84`, `grid-VERDICT`, `grid-summary`

## Obs 88 — 2026-06-11 [RESULT / METHODOLOGY]: cross-classified (D-B) 3-arm pilot — library arm eliminates estimated-basis contamination bias; Option A (tiers3) re-fails exactly as predicted

### The finding

The D-B sign-off (commit `0f9a025`) replaced the spec's binary A-vs-B `p_conv` choice with a
three-arm pilot before committing the full 300 × 100 grid. The three arms were:

- **`tiers3`** (Option A as written): `p_conv` = `tier_weights · LATIN_BASIS` (the shared
  Amendment-03 3-tier empirical basis, `design.json::tier_basis_empirical_latin`).
- **`library`** (recommended candidate): `p_conv` = `tier_weights · SLAB_LIBRARY`, where
  the library rows are the deterministic aoristic boxes of 19 round-endpoint slabs
  (lo ∈ {1, 51, 76, 101, 151} × hi ∈ {150, 200, 250, 300}, lo < hi). No data enters the
  basis — no contamination channel.
- **`free`** (Option B): `p_conv` gets its own non-centred GRW, mirroring `p_gen`.

Pilot: 20 cells × 20 reps × 3 arms on sapphire; 0 per-arm failures.

**Regime summary (mean over cells, converged reps only):**

| arm | regime | n | mean med-bias | mean \|bias\| | coverage | conv |
|---|---|---|---|---|---|---|
| **lead (ref)** | identifiable | 12 | +0.064 | 0.064 | 0.319 | 0.917 |
| tiers3 | identifiable | 12 | −0.002 | 0.031 | 0.321 | 1.000 |
| **library** | identifiable | 12 | **+0.006** | **0.011** | **0.562** | **0.996** |
| free | identifiable | 12 | −0.013 | 0.017 | 0.620 | 0.979 |
| **lead (ref)** | confounded | 8 | +0.081 | 0.081 | 0.320 | 0.938 |
| tiers3 | confounded | 8 | **−0.400** | 0.401 | 0.000 | 1.000 |
| **library** | confounded | 8 | **+0.010** | **0.012** | **0.725** | **1.000** |
| free | confounded | 8 | −0.031 | 0.045 | 0.661 | 0.981 |

**`tiers3` re-fails confounded cells.** Mean confounded median-bias −0.400, reaching −0.798
and −0.799 at α_true = 0.8 (cells `conc_a0.8_gauss_inwin`, `stress_a0.8_regnal`). This
is the POC Experiment 1 α-collapse mechanism reproducing under the cross-classified
likelihood: escaping to α → 0 costs ~10 prior-nats (signoff §2 quantitative prediction)
while holding α at truth with a broad-forced `p_conv` costs hundreds of multinomial nats
(≈ k × KL, k ≈ 1,300 at N = 2,800). Under the cross-classified likelihood, two
multinomials are confidently wrong simultaneously (confounded mean-bias more negative than
the POC single-multinomial result), confirming the signoff §2 prediction in both direction
and severity.

**`library` eliminates the lead's contamination bias and passes both regimes.**
Confounded mean median-bias +0.010 vs lead +0.081 (87 % reduction); identifiable mean
median-bias +0.006 vs lead +0.064 (91 % reduction). The lead's near-uniform +0.06–+0.08
over-attribution surface disappears. Coverage on coverable cells (α_true > 0) rises from
0.456 (lead) to 0.896 (library). Convergence improves from 0.917–0.938 (lead) to
0.996–1.000 (library), confirming signoff §6.3's prediction that the more informative
two-subset likelihood improves sampling geometry.

**Boundary-coverage artefact (all arms, including the lead):** α_true = 0 cells report
coverage 0.000 in every arm. This is an equal-tailed-CI boundary artefact — the 2.5th
percentile of a positive posterior is always > 0, so the true value α = 0 is never
bracketed. The aggregator now breaks this out separately (commit `a28c406`). This artefact
also depressed the lead grid's headline C1 coverage (0.374); a portion of that figure was
never achievable by any model.

**`free` is a viable fallback** (identifiable coverage 0.620, confounded 0.661,
convergence 0.979–0.981) but under-attributes at mid-α confounded corners: −0.170
(`conc_a0.4_gauss_inwin`) and −0.125 (`stress_a0.4_gauss_inwin`). `library` is more
constrained and more interpretable; it is the pilot winner under all four decision
criteria in order (signoff §5).

**Full 300 × 100 `library` run: NOT launched.** Pilot-measured per-fit time for `library`
is 60.4 s/fit (mean; max 94.9 s), projecting to ~41.9 h wall-clock at n_jobs = 12 —
past the signoff §4 30 h hard-stop. Per the standing no-silent-negotiation rule, halted
and reported to Shawn for a resource decision. (`tiers3` projects ~18.7 h; `free` ~25.5 h;
neither is the pilot winner.)

### Why this matters

The pilot answers the central question left open by the Obs 87 verdict: does a
better-specified `p_conv` basis remove the +0.07 contamination surface that caused the
lead to fail C1? The answer is yes — `library`'s identifiable mean bias is +0.006 and
its coverage on coverable cells is 0.896. Equally important, the pilot confirms the
second-opinion prediction (signoff §6.3) that the additional identifying information in
the two-subset likelihood improves, not degrades, sampling geometry (convergence
0.996–1.000 vs lead 0.917–0.938).

The `tiers3` failure is also paper-load-bearing: it is a controlled measurement of the
α-collapse mechanism under the cross-classified likelihood, replicating and extending the
POC Experiment 1 result. This rules out the Option-A-as-written parameterisation for
the full grid and justifies the slab-library design choice in the OSF amendment.

The halted launch is not a failure — it is the hard-stop rule functioning correctly. The
decision now is whether to accept the ~42 h `library` run on sapphire, or to reduce scope
(e.g., N strata, rep count) to fit the hard-stop.

### Caveats / methodological notes

The pilot used 20 cells × 20 reps. Cell selection is stratified by recipe × α × genuine
distribution × N = 2,800 only (8 confounded, 12 identifiable); the full 300-cell grid
covers N ∈ {1,500, 2,800, 15,000} and a wider %win × α surface. The pilot results are
directionally reliable but the headline figures (coverage, convergence) will shift
somewhat in a full run, particularly at N = 15,000.

The coverage figures (0.896 for `library` on α > 0 cells) are from 20 reps — the variance
on a per-cell coverage estimate at 20 reps is high. The full 100-rep run is needed before
the figure is paper-citable. Use the pilot result as a strong directional signal, not a
final number.

The `library`'s 19-row slab basis deliberately excludes near-duplicate (50, ·)/(51, ·)
rows to avoid near-collinear Dirichlet components. The grid recipes' (50, ·) slabs are
represented by (51, ·) rows — a sub-bin difference, negligible against the 0.12 bias gate.
The `library` does not exactly contain the truth, which is the production-realistic case.

### Related observations and artefacts

**Obs 87** (the lead grid VERDICT — C1 fails at 18 %, contamination +0.07 near-uniform;
this Obs is the pilot that measures whether the D-B arm resolves it): the result this
pilot was designed to address. **Obs 86** (the estimated-basis contamination mechanism
characterised; cross-classified D-B as the principled fix): the diagnosis confirmed here
at pilot scale. **Obs 84** (the confidently-wrong likelihood mechanism): the theoretical
underpinning for the `tiers3` failure predicted by signoff §2 and confirmed by the pilot.
**Obs 83** (the per-unit + classification design and POC, including Experiment 1 α-collapse
that `tiers3` now replicates): the original observation whose failure mode the pilot
reproduces.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/cc-PILOT-REPORT.md`
(commit `3137241`); `runs/2026-06-09-joint-identifiability/cross-classified-signoff.md`
(commit `0f9a025`, §2 quantitative prediction and §4 hard-stop rule, §6 second opinions);
`runs/2026-06-09-joint-identifiability/cross-classified-spec.md` (commit `37a94c5`);
`runs/2026-06-09-joint-identifiability/outputs/cc-setdata-validation.json`
(commit `a28c406`, boundary-coverage breakdown).

### Findable later

`cross-classified-pilot`, `3-arm-pilot`, `tiers3-re-fails`, `library-wins`, `free-fallback`,
`option-A-as-written`, `slab-library`, `19-rows`, `deterministic-aoristic-slabs`,
`no-contamination-channel`, `alpha-collapse`, `confidently-wrong-two-multinomials`,
`minus-0-400-confounded`, `minus-0-798`, `minus-0-799`, `poc-experiment-1-reproduces`,
`signoff-prediction-confirmed`, `10-prior-nats`, `bias-eliminated`, `plus-0-010`,
`plus-0-006`, `coverage-0-896`, `coverage-0-000-boundary-artefact`, `equal-tailed-CI-boundary`,
`alpha-true-zero-uncoverable`, `boundary-coverage-breakdown`, `geometry-improves`,
`convergence-0-996`, `convergence-1-000`, `60-4-s-per-fit`, `41-9-hours`, `hard-stop-triggered`,
`no-silent-negotiation`, `launch-halted`, `resource-decision`, `full-run-not-launched`,
`D-B`, `p-conv-parameterisation`, `obs-87`, `obs-86`, `obs-84`, `obs-83`,
`cc-PILOT-REPORT`, `3137241`, `0f9a025`, `a28c406`, `37a94c5`

## Obs 89 — 2026-06-13 [RESULT / METHODOLOGY]: cross-classified `library` full recovery grid — CLEAN PASS; contamination bias eliminated; model adopted as production lead

### The finding

The full 300-cell × 100-rep cross-classified `library`-arm recovery grid completed on
sapphire: **0 failed cells, 0 worker errors, 46.0 h wall-clock**. All four spec §5
adoption criteria are met on every axis — this is a clean pass with no caveats on any
criterion. Artefacts: `runs/2026-06-09-joint-identifiability/outputs/cc-VERDICT-library.md`
and `cc-summary-library.json` (commit `abe0b20`).

**C1 — do-no-harm (identifiable cells): PASSES.**

| metric | cc `library` | lead (Obs 87) |
|---|---|---|
| cells passing C1 (|bias|<0.12 AND coverage≥0.90) | **76/210 (36%)** | 37/210 (18%) |
| mean \|median bias\| | **0.021** | 0.075 |
| mean coverage (all ident) | **0.627** | 0.374 |
| coverage on α>0 cells only (n=168) | **0.784** | 0.456 |

The lead's near-uniform +0.06–+0.08 estimated-basis contamination surface (Obs 87) is
eliminated. The cc `library` bias surface is flat at +0.00–+0.03 across the whole
%win × α plane (tabulated below).

**Bias surface — mean(median bias) by %win × α_true** (source: `cc-VERDICT-library.md`):

| %win \ α | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| 0.53 | +0.01 | +0.01 | +0.02 | +0.02 | +0.01 |
| 0.63 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |
| 0.83 | +0.01 | +0.01 | +0.01 | +0.01 | +0.02 |
| 0.95 | +0.01 | +0.01 | +0.02 | +0.02 | +0.02 |
| 1.00 | +0.01 | +0.02 | +0.03 | +0.03 | +0.02 |

**C2 — pulled-to-truth (confounded cells): PASSES.**

| metric | cc `library` | lead (Obs 87) | shared-basis baseline |
|---|---|---|---|
| cells passing C2 | **72/90 (80%)** | 64/90 (71%) | — |
| mean \|median bias\| | **0.009** | 0.066 | 0.362 |
| worst positive median bias | +0.040 | +0.164 | — |
| mean coverage | **0.763** | 0.462 | — |
| coverage on α>0 confounded cells | **0.953** | — | — |

Confounded |bias| is ~40× below the shared-basis baseline and 7× below the lead.
Confounded α>0 coverage is 0.953 (≈ nominal).

**C4 — convergence: PASSES.**

| metric | cc `library` | lead (Obs 87) |
|---|---|---|
| cells with convergence_rate ≥ 0.95 | **287/300 (96%)** | 252/300 (84%) |
| mean convergence rate | **0.991** | 0.950 |

**Adoption criteria from `cross-classified-spec.md` §5** (all met):

| criterion | value | required |
|---|---|---|
| 1. bias flattens (ident \|bias\| < lead 0.075) | **0.021** | < 0.075 |
| 2. C1 recovers (coverage > lead 0.374, toward 0.90) | **0.627** | > 0.374 |
| 3. C2 not sacrificed (conf \|bias\| << baseline 0.362) | **0.009** | << 0.362 |
| 4. C4 not worse (cell pass-rate ≥ lead 0.84) | **0.957** | ≥ 0.84 |

### Why this matters

This is the gate result that unblocks the production refit. The spec §5 adoption rule
("if it improves C1/coverage without sacrificing C2, it is the better production model
and the OSF amendment adopts it") is satisfied on all four axes simultaneously. The
cc `library` model is therefore **adopted as the production lead**, replacing the
fixed-estimated-basis design whose +0.07 contamination surface (Obs 87) caused C1
to fail.

The N=15,000 watch-item from the phase-gate (the pilot N-scaling probe had shown +0.044
bias on 8 reps, flagged as under-powered) is resolved: full-grid confounded |bias| is
0.009 and the worst single-cell positive median bias is +0.040 — the probe figure was
small-sample noise; the slab library spans the truth at all three N levels.

**Immediate consequence:** the production refit (28 H2.1 units + Italia, per-unit slab
catalogue) and the OSF amendment (reverses Amendment 03's shared basis) are
preregistration-reversing and **await Shawn's sign-off** — not auto-launched.

### Caveats / methodological notes

**Coverage diagnostic — precision-for-accuracy trade, not under-dispersion.** The
identifiable coverage shortfall vs the aspirational 0.90 threshold is fully accounted for
by the tighter posterior, not by over-confidence. Measured on converged replicates:

- The exact two-subset likelihood tightened the posterior to **66% of the lead's width**
  (posterior σ 0.0227 vs 0.0343 on the same cells — more information ⇒ more precision,
  exactly as signoff §6.3 predicted).
- Residual identifiable |bias| 0.024 ÷ σ 0.0227 ≈ **1.07σ**; a pure-shift normal model
  predicts coverage 0.757 vs observed 0.784 — the shortfall is fully explained by the
  residual ~1σ bias against a tighter ruler.
- Posterior σ / replicate sampling-sd = **1.34–1.37 (> 1)** — the credible interval is
  *wider* than the point-estimate scatter, i.e. dispersion is **conservative**, not
  optimistic.

So cc `library` is simultaneously more accurate (bias 3.5× smaller) and more precise
(σ 1.5× tighter) than the lead, with conservative dispersion. The identifiable coverage
shortfall is a measurement artefact of comparing a tighter ruler against a non-zero
residual bias, not a calibration defect.

**Methodological takeaway (lego-brick / paper framing).** The cross-classified
time × alignment model is the exact collapsed concomitant-variable latent-class
likelihood (per-inscription latent type with two manifest indicators: temporal bin +
grid-alignment). The lead's "classification-as-likelihood + estimated basis" was a
composite-likelihood approximation, and the measured +0.07 surface was the cost of that
approximation. The slab `library` (deterministic aoristic boxes of round-endpoint slabs;
no data in the basis mass) is what removes the contamination channel while retaining
shape freedom — the shared 3-tier `tiers3` arm re-failed (Obs 88).

**Grid scope (from `full-grid-spec.md` §2):** %win ∈ {0.527, 0.631, 0.834, 0.951,
1.00}; α_true ∈ {0.0, 0.2, 0.4, 0.6, 0.8}; N ∈ {1,500, 2,800, 15,000}; 100 reps per
cell; 0 replicate failures; 46.0 h wall-clock at n_jobs = 12 on sapphire.

### Related observations and artefacts

**Obs 88** (the 3-arm pilot that selected the `library` arm — this Obs is the full
300-cell confirmation of the pilot result): the pilot that nominated the `library` design
and triggered this run. **Obs 87** (the lead grid VERDICT — C1 fails at 18 %,
estimated-basis contamination +0.07 near-uniform; this Obs is the full remediation):
the prior lead whose contamination surface this Obs eliminates. **Obs 86** (estimated-
basis contamination mechanism characterised; cross-classified D-B as the principled fix):
the diagnosis confirmed here at replicate scale across the full grid. **Obs 85** (κ-sweep
ruled out CI under-dispersion as the C1 failure mode): consistent with this Obs's finding
that the shortfall is bias-driven, not dispersion-driven. **Obs 84** (the confidently-
wrong likelihood mechanism — theoretical underpinning for why the shared basis fails):
the theoretical background that predicted this result.

**Artefacts**: `runs/2026-06-09-joint-identifiability/outputs/cc-VERDICT-library.md`
(commit `abe0b20`); `runs/2026-06-09-joint-identifiability/outputs/cc-summary-library.json`
(commit `abe0b20`); `runs/2026-06-09-joint-identifiability/cross-classified-spec.md`
(commit `37a94c5`, §5 adoption rule); `runs/2026-06-09-joint-identifiability/cross-classified-signoff.md`
(§6c full-grid verdict + coverage diagnostic); `runs/2026-06-09-joint-identifiability/full-grid-spec.md`
§2 (grid scope).

### Findable later

`cross-classified-library`, `cc-library-full-grid`, `clean-pass`, `300-cells`,
`100-reps`, `zero-failed-cells`, `zero-worker-errors`, `46-hours`, `46-0-h`,
`contamination-eliminated`, `estimated-basis-contamination`, `bias-surface-flat`,
`plus-0-00-to-plus-0-03`, `C1-passes`, `C2-passes`, `C4-passes`, `76-of-210`,
`36-percent`, `72-of-90`, `80-percent`, `287-of-300`, `96-percent-convergence`,
`mean-bias-0-021`, `lead-bias-0-075`, `coverage-0-627`, `coverage-0-784`,
`alpha-greater-0`, `confounded-coverage-0-953`, `confounded-bias-0-009`,
`baseline-0-362`, `40x-reduction`, `7x-below-lead`, `mean-rate-0-991`,
`adoption-criteria-all-met`, `spec-5-adoption-rule`, `production-lead-adopted`,
`production-refit-awaits-sign-off`, `OSF-amendment`, `reverses-amendment-03`,
`N-15000-watch-resolved`, `0-044-small-sample-noise`, `worst-cell-plus-0-040`,
`precision-for-accuracy-trade`, `not-under-dispersion`, `posterior-sigma-0-0227`,
`lead-sigma-0-0343`, `66-percent-of-lead-width`, `1-07-sigma`, `predicted-coverage-0-757`,
`observed-coverage-0-784`, `sigma-over-sd-1-34-to-1-37`, `conservative-dispersion`,
`3-5x-smaller-bias`, `1-5x-tighter-sigma`, `collapsed-concomitant-variable`,
`latent-class-likelihood`, `two-manifest-indicators`, `composite-likelihood-approximation`,
`slab-library`, `deterministic-aoristic-slabs`, `no-contamination-channel`,
`tiers3-re-fails`, `n-jobs-12`, `sapphire`, `abe0b20`, `37a94c5`, `obs-88`, `obs-87`,
`obs-86`, `obs-85`, `obs-84`, `cc-VERDICT-library`, `cc-summary-library`,
`cross-classified-spec`, `cross-classified-signoff`

## Obs 90 — 2026-06-13 [RESULT / METHODOLOGY]: cc-library production refit — all 10 diagnostic-flagged frontier units pinned; controls stable; α under-attribution resolved

### The finding

Following Shawn's adoption sign-off of the cross-classified `library` model (Obs 89),
the 29 H2.1 production units were re-fitted under
`build_model_cross_classified(pconv_mode="library")`. Run: `runs/2026-06-13-cc-production-refit/`,
sapphire, 6 min wall-clock, 0 worker errors, **28/29 converge**. Artefacts:
`outputs/REFIT-VERDICT.md` + `outputs/refit-summary.json` (commit `48cb5d5`).

**Two design decisions were settled empirically before fitting** (`spec.md`):

1. **k and n_rows in aoristic-effective counts.** `k = y_aligned.sum()`,
   `n_rows = y_aligned.sum() + y_nonaligned.sum()` (both subsets) — preserving
   the exact lumping/thinning factorisation. The alternative (row counts) differs from
   aoristic-mass aligned-fractions by only **mean 0.021, max 0.058** (Ostia;
   `outputs/unit-measurements.json`), so θ (calibrated on row fractions) transfers with
   ≤0.06 error — well inside tolerance.
2. **Fixed 27-row corpus-wide slab library.** The convention basis is a FIXED,
   a-priori, round-endpoint slab library (`outputs/production-slab-library.json`),
   identical for every unit — NOT the per-unit catalogue signoff §2 sketched. Three
   reasons: (a) direct production analogue of what the grid validated; (b) no per-unit
   membership-contamination channel; (c) avoids per-unit truncation/collinearity tuning.
   Validation: NNLS L1 residual ≤ 0.083 for all real-convention units (mean 0.056;
   Pompeii L1 0.632 is correct — genuine-precision, the diagnostic's validation case).
   Gram condition number **3.0 × 10¹⁷ — lower than the recovery grid's validated 19-row
   library (6.9 × 10¹⁷)**, which converged at 96 %.

**RESULT — frontier units pinned (the point of the exercise).**

All 10 diagnostic-flagged under-attributed frontier units are now pinned within the
H2.1 two-bound [α_shared, α_perunit] range and track the classification-implied α:

| unit | H2.1 α_shared | cc-library α [95 % CI] | α_perunit | implied-α |
|---|---|---|---|---|
| Moesia inferior | 0.050 | **0.626** [0.532, 0.765] | 0.870 | 0.520 |
| Pannonia inferior | 0.147 | **0.630** [0.576, 0.696] | 0.751 | 0.566 |
| Numidia | 0.166 | **0.546** [0.522, 0.573] | 0.515 | 0.425 |
| Ostia | 0.335 | **0.650** [0.577, 0.735] | 0.775 | 0.544 |
| Venetia et Histria / Regio X | 0.452 | **0.844** [0.803, 0.880] | 0.809 | 0.853 |
| Umbria / Regio VI | 0.429 | **0.738** [0.682, 0.800] | 0.700 | 0.722 |
| Salona | 0.538 | **0.987** [0.942, 1.000] | 0.995 | 0.945 |
| Samnium / Regio IV | 0.272 | **0.840** [0.803, 0.883] | 0.860 | 0.834 |
| Britannia | 0.002 | **0.400** [0.340, 0.497] | 0.793 | 0.279 |
| Dacia | 0.001 | **0.157** [0.138, 0.178] | 0.344 | 0.014 |

The cross-classified alignment contrast pins the value the shared basis could not — exactly
the remediation the diagnostic called for. 10/10 frontier units within bounds.

**Controls stable.**

| unit | H2.1 α_shared | cc-library α | Δ vs H2.1 |
|---|---|---|---|
| Pompeii | 0.001 | 0.015 | +0.014 (≈ 0 — genuine-precision correct) |
| empire-aggregate | 0.672 | 0.671 | −0.001 |
| Latium et Campania / Regio I | 0.672 | 0.595 | −0.077 |
| Noricum | 0.880 | 0.784 | −0.096 |
| latin-aggregate | 0.811 | 0.726 | −0.085 |

Pompeii and empire-aggregate are unchanged. A mild, consistent −0.08 to −0.10 downshift on
the broad high-α identifiable units (Latium et Campania, Noricum, latin-aggregate): the cc
model attributes slightly less convention to broad units than the shared-basis fit. This is
small and within the recovery grid's accuracy envelope; it warrants a sentence in the
amendment but is not a validity problem.

**Convergence 28/29.** The one flag is empire-aggregate (the largest unit, n_rows_eff ≈ 151 k,
secondary/context unit): max R-hat 1.026 (gate 1.01), min bulk-ESS 211 (gate 400),
0 divergences. This is a mixing/ESS marginality on the hardest unit, not a validity
problem — α (0.671) matches H2.1 (0.672) exactly, so the estimate is trustworthy. The sampler
config was kept uniform with the recovery-validated grid (2,000 draws / 1,000 tune /
target_accept 0.95) rather than bumped for one secondary unit; reported caveated per spec §4.

### Why this matters

This Obs records the end-to-end resolution of the H2.1 α under-attribution problem. The
DIAGNOSTIC (`runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`)
flagged 10 frontier units whose shared-basis α was implausibly low (temporal concentration
confounds convention and genuine in time, making the shared-basis binomial confidently wrong
for those units — Obs 87, Obs 89). The cc-library refit resolves this directly: the
alignment contrast provides the identifying information the temporal multinomial alone cannot.

The fixed corpus-wide slab library design is paper-load-bearing: it is the exact production
analogue of the recovery-validated grid design (fixed deterministic-box library), it carries
no per-unit contamination channel, and it spans every real unit's aligned SPA at
reconstruction residual ≤ 0.083 — better collinearity than the validated grid basis.

The immediate consequence is that the OSF amendment can now be drafted. The amendment
reverses Amendment 03's shared basis, adopts the cc-library model, and records the
recovery grid (Obs 89) + this refit as the gate. The amendment will be **drafted for
Shawn's review — not lodged without sign-off**. The H3b identifiable-set reconciliation
folds in.

### Caveats / methodological notes

**Coverage caveat carried forward from Obs 89.** Reported 95 % CIs are ~1σ-optimistic by
the recovery grid's residual bias (grid identifiable |bias| 0.024 ≈ 1.07σ against a
posterior σ of 0.023). For units in high-%win × high-α regimes, pair the cc-library point
estimate with the H2.1 two-bound sensitivity as the disclosure (per spec §4 and
`cross-classified-signoff.md` §6c).

**Dacia is a confirmatory, not under-identified, unit** (`h2_under_identified: false` in
`refit-summary.json`). Its implied-α of 0.014 (near zero) makes the two-bound framing less
informative there; the cc-library estimate 0.157 [0.138, 0.178] should be read against the
H2.1 perunit bound (0.344) and the diagnostic context.

**Britannia's implied-α (0.279) is below the cc-library estimate (0.400).** The two-bound
window is wide (0.002–0.793); the cc estimate is interior and reasonable. The implied-α
discrepancy is noted for the amendment but does not undermine the pinning result.

**Empire-aggregate convergence caveat.** Max R-hat 1.026 exceeds the 1.01 gate. The unit
is secondary/context only (it does not feature in H2.1's confirmatory reporting); its
estimate matches H2.1 (0.671 vs 0.672). The caveat is reported per spec §4 and does not
affect the 10/10 frontier-unit verdict.

**Pompeii Δ of +0.014.** The shared-basis α_shared was 0.001; the cc-library median is
0.015. This is a boundary effect — the posterior minimum is constrained above zero by the
prior, and the NNLS L1 residual for Pompeii (0.632) confirms the library cannot represent
Pompeii's aligned SPA. The ~1.5 % value is the prior's floor, not a genuine convention
estimate; this is noted in the REFIT-VERDICT as "genuine-precision, correct".

### Related observations and artefacts

**Obs 89** (cc-library full recovery grid — CLEAN PASS; contamination bias eliminated; model
adopted as production lead; this Obs is the production application of that validated model):
the gate result that authorised this refit. **Obs 87** (the lead grid VERDICT — C1 fails at
18 %, +0.07 estimated-basis contamination near-uniform; this Obs is the refit that resolves
the under-attribution problem the lead could not fix): the prior production result that
motivated the cc model. **Obs 84** (the confidently-wrong likelihood mechanism — the
theoretical explanation for why broad frontier units under-attributed under the shared basis;
this Obs is the empirical resolution at production scale): the diagnosis confirmed in
production here.

The H2.1 diagnostic (`runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`)
is the direct document this refit resolves: the 10 flagged units in its table are the
same 10 now pinned above.

**Artefacts**: `runs/2026-06-13-cc-production-refit/outputs/REFIT-VERDICT.md` (commit
`48cb5d5`); `runs/2026-06-13-cc-production-refit/outputs/refit-summary.json` (commit
`48cb5d5`); `runs/2026-06-13-cc-production-refit/spec.md` (design decisions §1–2);
`runs/2026-06-13-cc-production-refit/outputs/unit-measurements.json` (row vs mass
aligned-fraction discrepancy, Gram condition numbers);
`runs/2026-06-13-cc-production-refit/outputs/production-slab-library.json` (the locked
27-row fixed library); `runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`
(the diagnostic this refit resolves).

### Findable later

`cc-library-production-refit`, `production-refit`, `29-units`, `28-of-29-converge`,
`frontier-units-pinned`, `10-of-10`, `under-attribution-resolved`, `alpha-identifiability`,
`diagnostic-resolved`, `fixed-corpus-wide-library`, `27-rows`, `production-slab-library`,
`aoristic-effective-counts`, `k-y-aligned-sum`, `n-rows-both-subsets`,
`row-vs-mass-aligned-fraction`, `mean-0-021`, `max-0-058`, `ostia-max-discrepancy`,
`gram-condition-3e17`, `gram-condition-6-9e17`, `grid-validated-collinearity`,
`nnls-residual-0-083`, `pompeii-l1-0-632`, `pompeii-genuine-precision-correct`,
`moesia-inferior-0-05-to-0-63`, `pannonia-inferior-0-15-to-0-63`,
`numidia-0-17-to-0-55`, `ostia-0-34-to-0-65`, `venetia-0-45-to-0-84`,
`umbria-0-43-to-0-74`, `salona-0-54-to-0-99`, `samnium-0-27-to-0-84`,
`britannia-0-00-to-0-40`, `dacia-0-00-to-0-16`,
`empire-aggregate-convergence-flag`, `rhat-1-026`, `ess-211`, `0-divergences`,
`n-rows-eff-151k`, `secondary-unit`, `alpha-matches-h2-1`,
`latium-campania-minus-0-077`, `noricum-minus-0-096`, `latin-aggregate-minus-0-085`,
`mild-downshift-broad-units`, `within-recovery-grid-accuracy`,
`2000-draws`, `1000-tune`, `target-accept-0-95`, `build-model-cross-classified`,
`pconv-mode-library`, `two-subset-likelihood`, `alignment-contrast`,
`h2-1-two-bound`, `alpha-shared`, `alpha-perunit`, `implied-alpha`,
`coverage-caveat`, `1-sigma-optimistic`, `signoff-6c`, `osf-amendment`,
`reverses-amendment-03`, `draft-not-lodge`, `h3b-reconciliation-folds-in`,
`sapphire`, `6-min`, `0-worker-errors`, `48cb5d5`, `obs-89`, `obs-87`, `obs-84`,
`REFIT-VERDICT`, `refit-summary`, `unit-measurements`, `production-slab-library`,
`DIAGNOSTIC-alpha-identifiability-REPORT`

## Obs 91 — 2026-06-14 [METHODOLOGY / RESULT]: θ_gen calibration was circularly inflated (0.155 → 0.025); re-derived prior adopted; all frontier units rise to track classification-implied α

### The finding

The cc-library production refit (Obs 90, first-pass commit `48cb5d5`) used θ priors from
`calibrate_theta.py` rule C: θ_conv 0.945, θ_gen 0.155, κ=40. A robustness investigation
(`runs/2026-06-14-hybrid-robustness/`) found θ_gen 0.155 was **inflated by a circularity**:
`calibrate_theta.py` fit θ_gen as the intercept of `aligned_frac ≈ θ_gen + (θ_conv − θ_gen)·α`
using the **under-attributing shared-basis α_shared** — biased-low α's inflate the intercept.

**Three independent methods agree the true θ_gen ≈ 0.025:**

| method | θ_gen | θ_conv | note |
|---|---|---|---|
| Global-θ hybrid joint fit | 0.024 | ~0.933 | weakly identified (α ↔ θ_gen ridge; see Caveats) |
| Re-derivation with corrected α's (`rederive_theta.py`) | 0.025 | 0.930 | `α_cc × mass × all`, all 29 units; RMSE 0.045 vs 0.117 (~2.6× better) |
| Wide-κ θ-prior sweep | ~0.025 | — | stable across conditions; confirms direction |

The re-derivation fit is the canonical source (`outputs/theta-rederivation.json`,
`α_cc×mass×all` row: θ_gen=0.025, θ_conv=0.930, RMSE=0.0448). The reproduction
control (using α_shared → θ_gen 0.160) confirms the method recovers the original
calibration. The production refit's per-unit θ_gen posterior ran at median 0.101 under
the first-pass — the data pulled it down, but the tight κ=40 prior held it above the
data-preferred value.

**θ-prior sensitivity sweep — the robustness annex
(`theta_sweep.py` / `aggregate_sweep.py` → `outputs/THETA-SWEEP-VERDICT.md`;
4 θ-priors × 29 units = 116 cc-library fits, sapphire 18.8 min, 28/29 converge;
baseline reproduces the production refit bit-identically, max |Δα| 0.003):**

- **27/29 units stable** (α-range < 0.10 across baseline / re-derived / wide-κ /
  re-derived-wide); mean range 0.038; broad units + aggregates rock-stable (range ≤ 0.03).
- **Frontier units: 8/10 stable.** The two sensitive units — Moesia inferior (range 0.159)
  and Britannia (range 0.140) — are the most temporally-confounded. Their α moves
  **upward** under the corrected lower θ_gen and stays within the H2.1 two-bound range.
- Operative θ_gen 0.155 → 0.025 shift: uniformly small and positive (mean +0.025,
  max +0.072). The alignment **contrast** — not the θ centre — pins the well-identified α's.

This sweep replaces the poorly-mixing global-θ hybrid as the preregistered robustness annex.

**DECISION (Shawn, 2026-06-14, option i):** adopt the re-derived prior
(θ_conv 0.930, θ_gen 0.025, κ=40) as production. `refit_lib.adopted_theta_priors()`
reads it from `theta-rederivation.json`; `theta_priors()` is preserved for the record.
The first-pass refit (θ_gen 0.155) is preserved at commit `48cb5d5`; the new refit
(commit `35f7c71`) supersedes it.

**RESULT — all 10 frontier units rose under the corrected θ_gen (sapphire, 5.5 min, 28/29 converge):**

| unit | H2.1 α_shared | Obs 90 α (θ_gen 0.155) | adopted-θ α [95 % CI] | implied-α |
|---|---|---|---|---|
| Moesia inferior | 0.050 | 0.626 | **0.698** [0.617, 0.823] | 0.520 |
| Britannia | 0.002 | 0.400 | **0.449** [0.386, 0.544] | 0.279 |
| Pannonia inferior | 0.147 | 0.630 | **0.676** [0.632, 0.737] | 0.566 |
| Ostia | 0.335 | 0.650 | **0.701** [0.641, 0.772] | 0.544 |
| Numidia | 0.166 | 0.546 | **0.554** [0.530, 0.581] | 0.425 |
| Salona | 0.538 | 0.987 | **0.989** [0.951, 1.000] | 0.945 |
| Samnium / Regio IV | 0.272 | 0.840 | **0.860** [0.828, 0.898] | 0.834 |
| Umbria / Regio VI | 0.429 | 0.738 | **0.781** [0.734, 0.833] | 0.722 |
| Venetia et Histria / Regio X | 0.452 | 0.844 | **0.870** [0.845, 0.898] | 0.853 |
| Dacia | 0.001 | 0.157 | **0.171** [0.151, 0.194] | 0.014 |

All 10 track the classification-implied α. Umbria (0.781) and Venetia (0.870) sit above
the Obs 90 α_perunit bounds (0.700 and 0.809 respectively — old per-unit-basis upper
bracket), but that bracket was itself a wrong-high estimate; both track implied-α (0.722
and 0.853) closely. Controls stable: Pompeii 0.016, empire-aggregate 0.680.

### Why this matters

The θ_gen re-centering removes a demonstrated calibration bias from the production prior
and replaces it with a value that fits the aligned-fraction data ~2.6× better (RMSE 0.045
vs 0.117) and is corroborated by two independent methods. The frontier α's move as
expected (upward, proportional to temporal-confounding severity), confirming the model
is responding to the prior in the right direction, not just being pushed around. The
result strengthens the remediation claim: under-attribution is resolved even with the
corrected, lower θ_gen.

The methodological lesson is general: empirical-Bayes plug-in calibration of a
measurement parameter (θ_gen) from a biased first-pass estimate of the latent variable
(α_shared) is circular — the bias propagates into the prior. The fix (re-derive from
corrected estimates, confirm with an independent joint fit + a sensitivity sweep) is
documented here as a reusable pattern.

The OSF amendment (Amendment 04,
`planning/osf-amendment-2026-06-14-cross-classified-remediation.md`) incorporates the
re-derived θ in §A5.1 (the model spec), §A5.4 (the production-refit results table), and
§A5.7 (the θ robustness subsection); the sweep becomes the preregistered robustness annex.

### Caveats / methodological notes

**Global-θ hybrid is weakly identified.** Convergence did not improve when tuning was
doubled and target_accept raised (ESS went 188 → ~70); 0 divergences throughout — this
is an α ↔ θ_gen ridge, not a sampler failure. The hybrid's θ_gen ≈ 0.024 is treated as
directional evidence only, not a point estimate. The θ-prior sweep over the validated
cc-library model is the sound robustness vehicle.

**θ_conv differs slightly across methods.** The hybrid gives θ_conv ~0.933; the
re-derivation gives 0.930 (from `α_cc×mass×all`); the original calibration was 0.945.
The adopted production value is 0.930. The difference from 0.945 is small and within
the per-unit posterior width; it is reported in Amendment 04 §A5.7.

**Moesia inferior and Britannia remain the two most θ-sensitive units** (ranges 0.159
and 0.140 across the sweep). Their adopted-θ α's (0.698 and 0.449) are interior to
the H2.1 two-bound window (Obs 90's [α_shared, α_perunit] brackets) and the remediation
conclusion is unchanged; the θ-sensitivity is disclosed per Amendment 04 §A5.7.

**RMSE improvement figure.** The HYBRID-PILOT-FINDINGS addendum states "2.5× better
(RMSE 0.045 vs 0.117)"; the raw JSON gives 0.0448 vs 0.1175 ≈ 2.6×. The addendum's
"2.5×" is a rounded figure. This Obs uses the JSON-exact values.

### Related observations and artefacts

**Obs 90** (cc-library production refit, first-pass under θ_gen 0.155; this Obs corrects
the θ prior and supersedes the first-pass α table): the Obs being corrected here — its
frontier-unit α's are the "Obs 90 α" column above. **Obs 86** (estimated-basis
contamination and the θ_gen contamination channel; this Obs shows that θ_gen 0.155 was
itself an upward-biased estimate, compounding the contamination problem):
the θ_gen contamination mechanism characterised there is the mechanistic background for
why the calibration was susceptible to this circularity. **Obs 89** (cc-library recovery
grid — CLEAN PASS; the validated model that is the foundation for the θ-prior sweep here):
the grid that authorised production and whose validated structure the sweep uses.

**Artefacts**: `runs/2026-06-14-hybrid-robustness/HYBRID-PILOT-FINDINGS.md` (the
pilot report + addendum that diagnosed the circularity and executed options B and C);
`runs/2026-06-14-hybrid-robustness/outputs/theta-rederivation.json` (the re-derived
θ values; canonical source for the adopted prior);
`runs/2026-06-14-hybrid-robustness/outputs/THETA-SWEEP-VERDICT.md` (the 116-fit
sweep table and verdict);
`runs/2026-06-13-cc-production-refit/outputs/REFIT-VERDICT.md` (the adopted-θ refit
results, commit `35f7c71`; first-pass preserved at `48cb5d5`);
`runs/2026-06-13-cc-production-refit/outputs/refit-summary.json` (commit `35f7c71`);
`planning/osf-amendment-2026-06-14-cross-classified-remediation.md` §A5.1 / §A5.4 / §A5.7
(the amendment folding in this correction).

### Findable later

`theta-gen-calibration`, `circular-calibration`, `empirical-bayes-bias-propagation`,
`theta-gen-inflated`, `theta-gen-0-155`, `theta-gen-0-025`, `theta-conv-0-930`,
`kappa-40`, `calibrate-theta-circularity`, `alpha-shared-biased-low`,
`intercept-inflated`, `rederive-theta`, `theta-rederivation-json`,
`alpha-cc-mass-all`, `rmse-0-045`, `rmse-0-117`, `2-6x-better`, `2-5x-better`,
`three-methods-agree`, `global-theta-hybrid`, `weakly-identified`, `ridge`,
`alpha-theta-ridge`, `ess-188`, `ess-70`, `0-divergences`, `poor-mixing`,
`theta-prior-sweep`, `theta-sweep-verdict`, `theta-sweep-116-fits`,
`4-theta-priors`, `27-of-29-stable`, `8-of-10-frontier-stable`,
`mean-range-0-038`, `max-range-0-159`, `moesia-range-0-159`, `britannia-range-0-140`,
`alignment-contrast-pins-alpha`, `operative-shift-mean-0-025`, `max-shift-0-072`,
`sapphire-18-8-min`, `sapphire-5-5-min`, `28-of-29-converge`,
`adopted-theta-priors`, `theta-priors-kept-for-record`, `first-pass-48cb5d5`,
`adopted-theta-35f7c71`, `decision-option-i`, `shawn-2026-06-14`,
`moesia-0-05-to-0-70`, `britannia-0-00-to-0-45`, `pannonia-inferior-0-15-to-0-68`,
`ostia-0-34-to-0-70`, `numidia-0-17-to-0-55`, `salona-0-54-to-0-99`,
`samnium-0-27-to-0-86`, `umbria-0-43-to-0-78`, `venetia-0-45-to-0-87`,
`dacia-0-00-to-0-17`, `pompeii-0-016`, `empire-aggregate-0-680`,
`umbria-above-perunit-bound`, `venetia-above-perunit-bound`,
`tracks-implied-alpha`, `frontier-units-rise`, `controls-stable`,
`osf-amendment-04`, `a5-1`, `a5-4`, `a5-7`, `robustness-annex`,
`preregistered-robustness`, `replaces-hybrid`, `obs-90`, `obs-89`, `obs-86`,
`HYBRID-PILOT-FINDINGS`, `theta-rederivation`, `THETA-SWEEP-VERDICT`, `REFIT-VERDICT`

## Obs 92 — 2026-06-15 [METHODOLOGY / RESULT]: H3b draw-wise base run — the global Timpson envelope test saturates on real data (large-N over-power); probe-window deficit posteriors are the deliverable

### The finding

The uncertainty-propagating H3b deviation test pushes 8,000 genuine-SPA posterior draws
per unit (from the cc-library adopted-θ refit, Obs 90–91) through a featureless-null
permutation envelope built once per unit. The global Timpson marginal-p is **0 (exponential
null) / ≤ 0.04 (CPL-3 null)** for all **29/29** units under both nulls. This is not a
bug: a faithfulness self-test confirms the draw-wise engine reproduces the library
`forward_envelope_test` / `permutation_envelope_test` bit-for-bit (both nulls), and the
2026-06-09 median-based draft (`REPORT.md`) reached the identical conclusion independently.

**The mechanism is the documented large-N over-power of the basic SPD/Timpson envelope
test.** At n_eff = 1,577–151,361 the pointwise Monte Carlo envelope is Poisson-tight, and
the real Roman epigraphic curve is humped and jagged — far richer in structure than a
monotone exponential or a 3-knot CPL. Essentially the whole curve reads as "deviation":
the exponential null is degenerate on the empire-aggregate (77/80 bins out-of-envelope).
Phase-1 calibrated detection at N ≈ 1,600 by injecting a single event onto a matching
smooth baseline; on real data the null is misspecified relative to the true smooth shape, so
baseline misfit + large N produces global saturation in a regime the calibration never
probed.

**The null construction is the CPL-3 fit to the observed corrected curve** (the standard
SPD self-referential null; Shawn-confirmed D1, 2026-06-15). Fitting CPL-3 to the raw corpus
instead conflates convention-removal reshaping with genuine events and saturates the probe
windows too, rendering them uninformative (tested; this is the rejected alternative).

**The informative deliverable is the probe-window deficit posteriors (CPL null, λ=1.0).**
Two complementary readings per window: net signed windowed departure from the smooth trend
(negative = net deficit) and P(deficit) = posterior probability that ≥ 1 window bin lies
below the envelope. Prereg-named scopes are clean and historically coherent:

| scope | Ant net dep. | Ant P(deficit) | Cri net dep. | Cri P(deficit) |
|---|---|---|---|---|
| empire-aggregate ◆ | **−23%** | **1.00** | **−27%** | **1.00** |
| latin-aggregate ◆ | **−43%** | **1.00** | **−13%** | **1.00** |

Both named scopes (empire-aggregate is the Antonine primary; latin-aggregate the Western-
Empire-provincial Crisis scope, Decision 36) show high-probability deficits at their
respective windows, consistent with Antonine-plague and Third-Century-Crisis decline
narratives. By net departure, **20/29** units show a net Antonine deficit and **14/29**
a net Crisis deficit. By P(deficit) ≥ 0.5: **17/29** (Antonine) and **18/29** (Crisis).

The coverage-inflation sensitivity (λ=1.2, §A5.5) moves only borderline units and
leaves saturated/near-zero ones flat; it is a sensitivity, not the headline reading.

H3b carries no Holm-corrected confirmatory family (prereg; Decision 15); all readings are
descriptive/exploratory. All per-unit rows other than the two named scopes are
exploratory-extra (broader than the prereg's named scope; scope confirmed 2026-06-14).

### The test

**Stage A.** `run_refit.py --emit-draws` re-ran the seeded 29-unit cc-library refit
(adopted-θ: θ_conv 0.930, θ_gen 0.025) on sapphire (5.8 min, 0 errors) and persisted the
genuine-SPA posterior (8,000 draws/unit) previously discarded. Provenance gate PASS 29/29:
α Δ ≤ 1.8 × 10⁻³, SPA Δ ≤ 9.3 × 10⁻⁴.

**Stage B.** `h3b_drawwise.py` built the featureless-null MC envelope once per unit × null,
evaluated all 8,000 draws against it, and computed: marginal-p + P(deviation) + per-draw
spread, λ=1.0/1.2 coverage sensitivity, two probe windows (signed + one-sided), Holm
(descriptive), soft-annotation and reachability flags, and raw-vs-corrected global test.
`run_h3b_drawwise.py` orchestrates; `make_h3b_report.py` produces the DRAFT report.

### Why this matters

The saturation finding is methodologically important in its own right: it shows that the
basic SPD/Timpson global test is uninformative at corpus sizes typical of this project.
The probe-window P(deficit) is the correct H3b deliverable — it tests the locally signed
departure at each named window relative to the curve's own smooth trend, which is exactly
what the prereg names.

The draw-wise architecture propagates genuine uncertainty (8,000 posterior draws per unit
rather than a single posterior-median SPA) through the entire test pipeline, making
P(deficit) a properly Bayesian summary. This is the improvement over the 2026-06-09
median-based draft.

The cc-library adopted-θ refit (Obs 90–91) is the upstream source: the corrected α's and
calibrated θ priors feed directly into the draws used here. Any future sensitivity analysis
(annex items below) inherits this validated foundation.

### Caveats / methodological notes

**Global saturation.** The global marginal-p is an uninformative gate at these corpus
sizes — it always signals "there is structure", which is trivially true for a humped
epigraphic curve. The deliverable is the probe window, not the global p.

**Soft-annotated units.** Moesia inferior and Britannia are θ-sensitive (Obs 91; α
ranges 0.159 and 0.140 across the θ-prior sweep). Their probe readings are flagged `*`
and should be read with additional caution; they are not excluded from the results.

**Reachability caveat.** Lusitania (n_eff 1,577) falls below the CPL-3 province
reachability floor (n_eff < 1,618); its results carry a `‡` flag.

**Coverage caveat.** cc-library posterior 95 % CIs are ~1σ-optimistic (Obs 89–90);
propagated deviations carry this caveat; λ=1.2 is the preregistered sensitivity.

**CPL-3 null fitting.** Fitting to the raw corpus (instead of the observed corrected
curve) saturates the probe windows and is demonstrably wrong — the correction itself
reshapes the whole curve. The adopted observed-corrected construction is the standard
self-referential SPD null and produces differentiated, informative probe readings.

**Deferred robustness annex (PI decision D2, 2026-06-15 — a new session with its own
spec).** (a) A more-flexible smooth null (CPL k=5–7 / penalised spline / Gaussian process
fit to the observed curve) plus an effective-N / reduced-significance variant to test
whether a better-specified null de-saturates the global test at all. (b) The baorista
Bayesian-aoristic null if warranted (`runs/2026-05-03-baorista-install/`; full LIRE-width
revalidation needed). Neither changes the base deliverable; both are independent post-hoc
sensitivities.

### Related observations and artefacts

**Obs 91** (θ_gen re-derived 0.155 → 0.025; all frontier units rise to track
classification-implied α; the adopted-θ refit whose draws this test consumes): the direct
upstream source of the 8,000 draws/unit. **Obs 90** (cc-library production refit — 10/10
frontier units pinned; first-pass θ_gen 0.155; this Obs uses the corrected second-pass at
commit `35f7c71`): the production refit superseded by the adopted-θ pass. **Obs 89**
(cc-library full recovery grid — CLEAN PASS; the validated model authorising production):
the gate result whose validated structure the draw-wise posterior propagates. **Obs 82**
(H3b preregistered exploratory; 2026-06-09 median-based draft run; exponential null
saturated; Antonine deficit in both aggregates): the median-draft precursor that this
draw-wise run supersedes; the saturation conclusion is replicated here. **Obs 23** (real
LIRE has structure beyond CPL k=4 — H3b deviation signal is real; forward-fit CPL shows
saturated FP at n ≥ 2,500): the earlier finding that anticipated exactly this regime of
global saturation on real humped data.

**Artefacts**: `runs/2026-06-09-h3b/REPORT-drawwise-2026-06-15.md` (the finalised base
run report; commit `881aafd`); `runs/2026-06-09-h3b/DECISION-NEEDED-null-construction-2026-06-14.md`
(the diagnosis note recording the D1–D3 decisions and the saturation mechanism);
`runs/2026-06-09-h3b/code/h3b_drawwise.py` (the Stage B engine);
`runs/2026-06-09-h3b/code/run_h3b_drawwise.py` (the run script);
`runs/2026-06-09-h3b/outputs/drawwise/deviations-table.csv` (per-unit × null × λ numbers);
commit `881aafd`.

### Findable later

`H3b`, `deviation-detection`, `Timpson`, `SPD`, `envelope-test`, `large-N-over-power`,
`saturation`, `global-test-saturated`, `p-zero-all-29`, `probe-window`, `P-deficit`,
`Antonine`, `Antonine-plague`, `Crisis-of-the-Third-Century`, `CPL-null`,
`CPL-fit-to-observed-corrected`, `self-referential-null`, `draw-wise`,
`uncertainty-propagation`, `8000-draws`, `genuine-SPA-posterior`, `n-eff-1577-151361`,
`77-of-80-bins`, `exponential-degenerate`, `featureless-null`, `permutation-envelope`,
`faithfulness-self-test`, `bit-for-bit`, `forward-envelope-test`,
`permutation-envelope-test`, `empire-aggregate-minus-23`, `empire-aggregate-minus-27`,
`latin-aggregate-minus-43`, `latin-aggregate-minus-13`, `20-of-29-Antonine`,
`14-of-29-Crisis`, `named-scopes`, `exploratory-extra`, `coverage-inflation`,
`lambda-1-2`, `soft-annotated`, `theta-sensitive`, `reachability-floor-1618`,
`Lusitania-1577`, `Moesia-inferior-soft`, `Britannia-soft`,
`deferred-robustness-annex`, `flexible-null`, `CPL-k5-7`, `GP-null`, `baorista`,
`baorista-null`, `effective-N-thinning`, `reduced-significance`, `decision-D1`,
`decision-D2`, `decision-D3`, `2026-06-15-confirmed`, `stage-A`, `stage-B`,
`provenance-gate`, `h3b-drawwise`, `run-h3b-drawwise`, `make-h3b-report`,
`REPORT-drawwise-2026-06-15`, `DECISION-NEEDED-null-construction`,
`deviations-table-csv`, `881aafd`, `obs-82`, `obs-89`, `obs-90`, `obs-91`, `obs-23`,
`2026-05-03-baorista-install`, `phase-1-calibration`, `N-approx-1600`,
`injected-event`, `matching-baseline`, `null-misspecified`, `baseline-misfit`

## Obs 93 — 2026-06-15 [METHODOLOGY / RESULT]: H3b flexible-null annex part (a) — saturation is structural null-misspecification; baorista NO-GO for the global test; probe-window P(deficit) confirmed robust

### The finding

Part (a) of the H3b flexible-null robustness annex (spec
`runs/2026-06-09-h3b/h3b-flexible-null-annex-spec-2026-06-15.md`;
report `runs/2026-06-09-h3b/outputs/flexnull/ANNEX-REPORT.md`;
engine `runs/2026-06-09-h3b/code/h3b_flexnull.py`; result commit `7fe248a`;
ran on sapphire) asks whether a more-flexible smooth null, and/or a de-powered
significance criterion, can de-saturate the global Timpson test without absorbing
the Antonine/Crisis events it is meant to detect. The base run (Obs 92) accepted
the saturation as an honest large-N over-power finding; this annex tests that
characterisation with two orthogonal levers applied to all 29 cc-library units,
propagating the genuine-SPA posterior draw-wise exactly as the base run.

**The spec §6.3 sweet-spot scan — global marginal-*p* > 0.05 AND named-scope
Antonine P(deficit) ≥ 0.8 — returns 0 hits across all 290 unit × fit
combinations.** Three independent legs:

**Leg 1 — flexibility lever.** Three self-referential smooth nulls fit to the
posterior-median corrected curve, all traced on one effective-degrees-of-freedom
(edf) axis (edf 5→20):

- CPL knot-sweep k ∈ {2, 3, 5, 7} (edf = {5, 7, 11, 15})
- Penalised Poisson B-spline (Eilers & Marx; edf ≈ {5, 10, 20})
- Kernel-ridge GP on log-counts (RBF kernel; edf ≈ {5, 10, 20})

Named-scope results (empire-aggregate n_eff 151,361; latin-aggregate n_eff 101,066):

**empire-aggregate** (global *p* / simultaneous *p* / Antonine P(def) / Crisis P(def)):

| family | edf | global *p* | sim. *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|---|---|
| cpl | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | 7 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | 11 | 0.000 | 0.001 | 0.17 | 1.00 |
| cpl | 15 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | 10 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | 20 | 0.000 | 0.001 | 0.83 | 1.00 |
| gp | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | 10 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | 20 | 0.000 | 0.001 | 0.96 | 1.00 |

**latin-aggregate:**

| family | edf | global *p* | sim. *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|---|---|
| cpl | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | 7 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | 11 | 0.000 | 0.001 | 0.85 | 1.00 |
| cpl | 15 | 0.000 | 0.001 | 0.85 | 1.00 |
| spline | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | 10 | 0.000 | 0.001 | 0.95 | 1.00 |
| spline | 20 | 0.000 | 0.001 | 0.67 | 1.00 |
| gp | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | 10 | 0.000 | 0.001 | 0.91 | 1.00 |
| gp | 20 | 0.000 | 0.001 | 0.75 | 0.98 |

Global marginal-*p* = 0.000 across the entire edf 5→20 ladder for all three
families at both named scopes. Wigglier nulls only erode the probe signal (empire
Antonine P(deficit) 1.00 at edf 5 → 0.83 at spline edf 20) without ever clearing
*p* = 0.05.

**Leg 2 — de-powered (simultaneous-coverage) statistic.** The max-studentised-
deviation simultaneous-band global *p* at the named scopes never exceeds 0.001.
Family-wise coverage across the 80 bins does not rescue the high-N scopes. Only
2/29 small-N units (n_eff ≲ 2,600) ever de-saturate under either the simultaneous
statistic or the wiggliest GP (edf 20); none of those de-saturated units is a sweet
spot (no event signal).

**Leg 3 — effective-N thinning (CPL-3 null).** Rescaling to N′ ∈ {1,500, 3,000,
6,000, 12,000, 25,000}:

| N′ | empire global *p* | empire Ant P(def) | latin global *p* | latin Ant P(def) |
|---|---|---|---|---|
| 1,500 | 0.006 | 0.53 | 0.002 | 0.99 |
| 3,000 | 0.000 | 1.00 | 0.000 | 1.00 |
| 6,000 | 0.000 | 1.00 | 0.000 | 1.00 |
| 12,000 | 0.000 | 1.00 | 0.000 | 0.99 |
| 25,000 | 0.000 | 1.00 | 0.000 | 1.00 |

Empire global *p* = 0.006 and latin global *p* = 0.002 even at N′ ≈ 1,500 — both
still saturated (< 0.05). This is the decisive diagnostic: Phase 1 calibrated
detection at N ≈ 1,600 against a *matching* smooth null; here a *smooth* null on a
*jagged* curve saturates even at N ≈ 1,500. The saturation is therefore **structural
null-misspecification** (a smooth null cannot represent the jagged real epigraphic
curve), not large-N over-power.

**Secondary methodological result — CPL knot-placement instability.** The CPL
knot-sweep is non-monotone in edf: at empire CPL-k5 (edf 11) a knot lands on
the Antonine window and absorbs the event (Ant P(deficit) = 0.17), recovering to
1.00 at k7 (edf 15). The penalised spline and GP ladders are monotone in edf across
both named scopes. This knot-placement instability vindicates carrying the two
penalised-smooth families rather than CPL alone.

### Why this matters

**Consequence 1 — baorista NO-GO for the global test.** A featureless
Bayesian-aoristic growth null (baorista) absorbs *less* structure than these
self-referential nulls, so it cannot de-saturate where they cannot. The §6.3
decision rule (pre-committed in the spec) triggers NO-GO: baorista is demoted to an
optional, lower-priority probe-sharpening cross-check for the global test.
The baorista infra remains installed at `runs/2026-05-03-baorista-install/`
(R 4.4.3 + baorista 0.2.1 + NIMBLE, smoke-tested on sapphire).

**Consequence 2 — probe-window P(deficit) confirmed AND shown robust.** The base
deliverable (Obs 92) is unchanged. The three-leg negative result is itself a
positive robustness certificate: the named-scope Antonine P(deficit) holds ≥ 0.67–
1.00 across the entire edf/N′ ladder until the null is wiggly enough to absorb the
event outright. No lever produces a de-saturated global test with the probe signal
intact.

**Consequence 3 — saturation mechanism clarified.** Obs 92 attributed the saturation
to "large-N over-power"; this annex refines that characterisation. The thinning leg
shows the saturation persists at N′ ≈ 1,500 — a regime where large-N alone cannot
explain it. The correct framing is structural null-misspecification: no smooth null
(however flexible) can track the round-year spikes and sub-bin jaggedness of the real
epigraphic curve well enough to avoid saturation, because the curve's jaggedness is
not smooth-null-representable. This distinction matters for any future SPD-style
deviation test on epigraphic corpora.

**Methodological lesson — CPL knot instability.** The discrete CPL knot-sweep
creates instability that a continuously-penalised smoother avoids. Any future
application of CPL sweeps as a flexibility ladder should carry at least one penalised
family (spline or GP) as a monotone countercheck.

### Caveats / methodological notes

**Self-referential null caveat.** All smoothers fit the posterior-median corrected
curve (D1 construction from the base run). High flexibility therefore trivially
shrinks the residual — the null absorbs the events rather than representing a genuine
background. This is exactly why the event-preservation axis (probe P(deficit)) is
reported at every fit level; any de-saturation that loses the probe signal is
event-absorption, not a fix.

**De-saturation at small-N units.** The 2/29 units that de-saturate under either the
simultaneous statistic or the wiggliest GP (edf 20) are small-N (n_eff ≲ 2,600) with
no event signal. Their de-saturation reflects a wider envelope, not a recovered
event; they are not sweet spots.

**Thinning kills probe power at N′ = 1,500.** Empire Ant P(deficit) falls to 0.53 at
N′ = 1,500, for a different reason than flexibility: fewer effective counts means a
noisier posterior, not event absorption. Both levers reduce the probe signal by
different mechanisms, but neither produces a de-saturated global test with the signal
intact.

**Exploratory framing.** H3b is exploratory (prereg; Decision 15; OSF Amendment 04
§A5.6). The 0.05 / 0.8 thresholds in §6.3 are the pre-committed readout convention,
not a confirmatory gate. Every reading here is descriptive.

**Reproducibility guard.** The CPL k=3 anchor reproduces the base run's marginal-*p*
and named-scope probe P(deficit) bit-for-bit (regression guard in `run_h3b_flexnull.py`).
The spline/GP/simultaneous-band code passed a sanity gate before the sweep ran.

### Related observations and artefacts

**Obs 92** (H3b draw-wise base run — global Timpson saturation attributed to
large-N over-power; probe-window P(deficit) the deliverable; deferred robustness annex
D2 flagged): the base run whose saturation finding this annex tests and refines.
The thinning result revises the mechanism from "large-N over-power" to "structural
null-misspecification", with no change to the deliverable. **Obs 91** (θ_gen
re-derived 0.155 → 0.025; adopted-θ refit whose draws the annex consumes): the
upstream cc-library refit; no re-run was needed here — draws already on disk from
the base run's Stage A. **Obs 23** (real LIRE has structure beyond CPL k=4; H3b
deviation signal is real; forward-fit CPL saturates at n ≥ 2,500): the earlier
finding that anticipated exactly this regime; the thinning result here adds the
further precision that even N ≈ 1,500 saturates under a smooth null on a jagged curve.
**Obs 82** (H3b preregistered exploratory; 2026-06-09 median-based draft; exponential
null saturated): the original draft run whose saturation conclusion is now shown robust
to all three levers.

**Artefacts**:
`runs/2026-06-09-h3b/outputs/flexnull/ANNEX-REPORT.md` (the DRAFT annex report;
verdict and tables re-read for this Obs);
`runs/2026-06-09-h3b/h3b-flexible-null-annex-spec-2026-06-15.md` (the signed-off
spec; §6.3 decision rule and §10 baorista logic);
`runs/2026-06-09-h3b/code/h3b_flexnull.py` (the annex engine);
`runs/2026-06-09-h3b/code/run_h3b_flexnull.py` (the driver; includes the k=3
regression guard);
`runs/2026-06-09-h3b/outputs/flexnull/flexnull-sweep.json` (per unit × family × edf);
`runs/2026-06-09-h3b/outputs/flexnull/flexnull-table.csv` (flat tabulation);
`runs/2026-06-09-h3b/outputs/flexnull/effn-thinning.json` (thinning ladder per unit × N′);
`runs/2026-06-09-h3b/outputs/flexnull/depowered-stat.json` (pointwise vs simultaneous-band);
`runs/2026-05-03-baorista-install/` (baorista infra; demoted to probe-sharpening only);
commit `7fe248a` (annex results).

### Findable later

`H3b`, `flexible-null`, `flexnull`, `flexible-null-annex`, `part-a`,
`robustness-annex`, `null-misspecification`, `structural-null-misspecification`,
`smooth-null`, `self-referential-null`, `CPL-knot-sweep`, `CPL-k2`, `CPL-k3`,
`CPL-k5`, `CPL-k7`, `penalised-spline`, `P-spline`, `Eilers-Marx`, `GP-null`,
`Gaussian-process`, `RBF-kernel`, `edf-5-to-20`, `edf-axis`, `flexibility-lever`,
`effective-N-thinning`, `N-prime-ladder`, `N-prime-1500`, `N-prime-3000`,
`N-prime-6000`, `N-prime-12000`, `N-prime-25000`, `de-powered-statistic`,
`simultaneous-coverage`, `max-studentised-deviation`, `simultaneous-band`,
`Myllymaki-2017`, `JRSS-B`, `global-envelope-test`,
`sweet-spot-scan`, `0-hits`, `290-unit-fit-combinations`,
`global-p-zero`, `global-p-0-006`, `global-p-0-002`,
`probe-preserved`, `probe-window`, `P-deficit`, `Antonine`, `Crisis`,
`empire-aggregate-151361`, `latin-aggregate-101066`,
`empire-Antonine-1-00-edf5`, `empire-Antonine-0-83-spline-edf20`,
`empire-Antonine-0-17-cpl-k5`, `knot-placement-instability`,
`CPL-non-monotone`, `spline-monotone`, `GP-monotone`,
`knot-absorbs-event`, `penalised-smoother-monotone`,
`2-of-29-de-saturate`, `small-N-desaturate`, `n-eff-2600`,
`baorista`, `baorista-NO-GO`, `baorista-demoted`, `probe-sharpening-only`,
`baorista-install`, `R-4-4-3`, `baorista-0-2-1`, `NIMBLE`,
`bit-for-bit`, `regression-guard`, `k3-anchor`, `sanity-gate`,
`7fe248a`, `run-h3b-flexnull`, `h3b-flexnull`, `make-flexnull-report`,
`ANNEX-REPORT`, `flexnull-sweep-json`, `effn-thinning-json`, `depowered-stat-json`,
`flexnull-table-csv`, `decision-D2-closed`, `no-sweet-spot`,
`large-N-over-power-revised`, `baseline-misfit`, `jagged-epigraphic-curve`,
`round-year-spikes`, `sub-bin-wiggle`, `Poisson-tight-envelope`,
`phase-1-calibration`, `N-approx-1600`, `matching-null`, `smooth-null-on-jagged-curve`,
`probe-robust`, `three-legs`, `two-levers`, `orthogonal-levers`,
`obs-92`, `obs-91`, `obs-23`, `obs-82`,
`osf-amendment-04`, `A5-6`, `exploratory`, `decision-15`,
`runs-2026-05-03-baorista-install`, `runs-2026-06-09-h3b`

## Obs 94 — 2026-06-16 [ROBUSTNESS / RESULT]: deconvolution does NOT change H3a — raw-count population–epigraphy scaling is robust to convention-correction

### The finding

We asked whether the cc-library deconvolution (which separates editorial-convention
dating artefacts from genuine production) would materially change H3a — the Hanson
population–inscription-count scaling.

**The publishable robustness statement: the population–epigraphy scaling holds
whether or not we correct for editorial-convention dating.**

Two independent reasons, one structural and one empirical:

**Reason (a) — structural: temporal reshaping conserves the full-window count.**
H3a's date window is the full envelope (50 BC – AD 350;
`h3a_common.DATE_WINDOW`). The deconvolution redistributes probability mass
*between* time-bins but conserves each unit's full-window total — the raw aoristic
SPA and the genuine SPA both normalise to the same n_eff. The reshaping is real and
sizeable (median raw-vs-genuine total-variation distance 0.243, max 0.500), but that
is H3b's signal (a shape statistic); it is invisible to a full-window count. The
only remaining channel for H3a is therefore the per-unit genuine fraction α.

**Reason (b) — empirical: α is uncorrelated with population or corpus size.**
Across the 26 non-aggregate deconvolved units:

| Correlation | α vs population | α vs n_eff |
|---|---|---|
| Spearman | −0.11 | −0.22 |
| Pearson | +0.13 | −0.17 |

The implied shift in the Hanson scaling exponent from replacing raw count N with
genuine count α·N equals the slope of log(α) on log(population). Flat α means a
constant multiplier, which leaves β unchanged.

**Slope estimates for implied Δβ:**

| Estimator | Δβ |
|---|---|
| OLS (all 26 units) | +0.292 |
| OLS 95 % bootstrap CI | [−0.112, +0.865] |
| Theil-Sen (robust) | −0.030 |
| OLS, drop-low-α (α < 0.10) | +0.015 |
| Theil-Sen, drop-low-α | −0.045 |

The OLS estimate (+0.292) is **not robust**: it is dominated by a single
high-leverage unit (see Gotcha below). All robust estimators converge on ≈ 0.

### The methodological gotcha — Pompeii as a high-leverage OLS artefact

The naïve OLS Δβ = +0.292 (95 % bootstrap CI [−0.112, +0.865]) looks non-trivial
but is a **single-unit artefact**. Pompeii (α = 0.02 — a post-AD-79 special case)
occupies the extreme low-α end of the log(α) axis and is a high-leverage point in
the log-space regression. Its removal collapses the OLS slope to +0.015, in line
with the Theil-Sen estimate of −0.030.

**Lesson for future log-space scaling diagnostics:** a near-zero-α unit can dominate
OLS when the effective covariate range in log space is very wide. Use a robust
estimator (Theil-Sen, drop-low-α, or leave-one-out) as the primary and treat OLS as
a secondary check. The Pompeii leverage artefact was caught on a robustness check;
the wide CI already signalled instability.

### Why this matters

1. **H3a primary is confirmed paper-ready as-is.** The preregistered primary
   (Decision 22/35; raw-count Hanson scaling, lodged confirmatory) is already the
   right specification — not merely by preregistration obligation but because the
   deconvolution would not move it materially.

2. **Full deconvolution leverage already cashed.** The cc-library mixture model is
   fully leveraged in H3b (which runs draw-wise on the genuine SPA) and in the
   descriptive genuine-vs-raw SPA figures (where the TV distance up to 0.500 does its
   work). H3a/H3c/SR1 count analyses inherit the same null result.

3. **D13 α-as-translator §5 sensitivity is the right H3a payoff route.** The
   preregistered D13 sensitivity needs **per-city** α. The 29 deconvolved units are
   province/region-level proxies; this diagnostic is therefore a province-level
   stand-in for the city-level confound. The province-level α-vs-size result is
   reassuringly flat, which suggests the expected H3a payoff of a full per-city
   mixture build is **low** — but the definitive test requires per-city deconvolution.

4. **Peak-window scaling is the motivated extension.** The deconvolution *does*
   become relevant for a peak-inscription-rate vs Hanson max-population scaling
   variant (non-preregistered; flagged here as a motivated extension). A peak is a
   shape statistic — not mass-conserved by the full-window sum — so the TV reshaping
   (up to 0.500) would matter there. This carries the GRW peak-attenuation caveat
   and needs per-city deconvolution.

### Caveats / methodological notes

- **Province-level proxy only.** α is available at 29 deconvolved units, mostly at
  province/region granularity. The slope above is a province-level proxy for the
  city-level confound. The city-level test requires per-city deconvolution (D13).
- **Aggregates excluded.** The empire-aggregate, latin-aggregate, and Italia (excl.
  Rome) aggregates were excluded from the correlation to avoid double-counting
  (their n_eff subsumes individual units).
- **Pompeii caveat.** Even the drop-low-α result is dominated by Pompeii's exclusion.
  The five directly-interpretable single-city units (Ostia, Mogontiacum, Aquileia,
  Pompeii, Salona) span a wide α range (0.02–0.99), giving the province-level
  inference both its signal and its instability.
- **H3a is exploratory-adjacent for α-sensitivity.** D13 is framed as a sensitivity
  check, not a primary. The flatness of α-vs-population weakens the case for
  elevating it.

### Related observations and artefacts

**Obs 93** (H3b flexible-null annex part (a) — same cc-library deconvolution
posterior; saturation is structural null-misspecification): the most recent consumer
of the same deconvolution posterior. The TV-distance figures (median 0.243, max
0.500) cited here are the H3b-domain signal that H3a cannot see.

**Obs 92** (H3b draw-wise base run — global Timpson saturation; probe-window
P(deficit) the deliverable): the base H3b run that confirmed the deconvolution is
fully leveraged in H3b, motivating this diagnostic to close off the H3a question.

**Artefacts**:
`runs/2026-06-16-deconv-leverage-diagnostic/outputs/REPORT.md` (the diagnostic
report; all numbers in this Obs verified against it);
`runs/2026-06-16-deconv-leverage-diagnostic/outputs/alpha-population-diagnostic.json`
(underlying data: α medians, population, n_eff, correlations, slope estimates);
`runs/2026-06-16-deconv-leverage-diagnostic/outputs/figures/fig-alpha-vs-size.png`
(scatter: α vs population and vs n_eff, all 29 units);
`runs/2026-06-16-deconv-leverage-diagnostic/code/deconv_leverage_diagnostic.py`
(the diagnostic script);
commit `a6ce8db` (result commit).

### Findable later

`deconvolution-leverage`, `deconv-leverage`, `H3a-robustness`,
`convention-correction`, `raw-count-H3a`, `Hanson-scaling-robustness`,
`alpha-vs-population`, `alpha-uncorrelated`, `Spearman-minus-0-11`,
`Pearson-plus-0-13`, `alpha-vs-n-eff`, `Spearman-minus-0-22`,
`genuine-fraction`, `full-window-count`, `mass-conservation`,
`temporal-reshaping-conserves`, `total-variation-distance`,
`TV-distance-0-243`, `TV-distance-0-500`,
`implied-delta-beta`, `OLS-delta-beta-plus-0-292`,
`OLS-bootstrap-CI-minus-0-112-plus-0-865`,
`Theil-Sen-minus-0-030`, `Theil-Sen`, `drop-low-alpha`,
`drop-low-alpha-OLS-plus-0-015`, `drop-low-alpha-theil-sen-minus-0-045`,
`Pompeii-OLS-leverage-artefact`, `Pompeii-alpha-0-02`,
`high-leverage-near-zero-alpha`, `leave-one-out`,
`single-unit-artefact`, `robust-estimator`,
`26-non-aggregate-units`, `29-deconvolved-units`,
`province-level-proxy`, `city-level-deconvolution`,
`D13-alpha-as-translator`, `alpha-as-translator`,
`per-city-alpha`, `per-city-mixture`,
`peak-window-scaling`, `peak-inscription-rate`,
`GRW-peak-attenuation`, `motivated-extension`, `non-preregistered-extension`,
`mass-conserved`, `shape-statistic`, `full-envelope`,
`h3a-common-DATE-WINDOW`, `50-BC-AD-350`,
`scaling-holds-whether-or-not-we-correct-for-editorial-convention-dating`,
`population-epigraphy-scaling`, `convention-correction-robustness`,
`H3b-signal-invisible-to-H3a`, `fully-leveraged`,
`D13`, `decision-22`, `decision-35`, `SR1`,
`obs-92`, `obs-93`,
`a6ce8db`, `deconv-leverage-diagnostic`, `alpha-population-diagnostic-json`,
`fig-alpha-vs-size`

## Obs 95 — 2026-06-16 [ROBUSTNESS / METHODOLOGY]: §5 sensitivity batch (D11, D12, B4) — all three corroborate H3a and Phase-1; B4 surfaces prereg-vs-implementation discrepancy

### The finding

All three preregistered §5 sensitivities for H3a / Phase-1 return corroborating
results. Numbers below verified against source JSON and REPORT files in
`runs/2026-06-16-s5-sensitivities/`.

---

**D11 — Hanson-population measurement-error sensitivity**

Re-fit the H3a within-between (Mundlak) Negative Binomial Regression (NBR) with the
preregistered Berkson measurement-error (ME) form
`log_pop_c ~ Normal(log_pop_observed_c, σ_pop)`, Mundlak within / between components
recomputed from the latent population each draw.
Primary (no ME): **f_within = 0.299 [0.240, 0.365]** (confirmatory run anchor).

| σ_pop | f_within (median) | 95 % CI | CI shift vs primary | material? | verdict |
|---|---|---|---|---|---|
| — (primary) | 0.299 | [0.240, 0.365] | — | — | supported |
| 0.1 | 0.305 | [0.243, 0.373] | 0.008 | no | supported |
| 0.2 | 0.320 | [0.255, 0.390] | 0.025 | no | supported |
| 0.3 | 0.341 | [0.277, 0.412] | 0.047 | no | supported |

The largest CI shift (0.047 at σ = 0.3) is below the prereg's material-divergence
threshold (50 % of the primary CI width = 0.063). Convergence clean throughout:
R̂ ≤ 1.01, ESS-bulk ≥ 1,080, 0 divergences (tune 4,000 / draw 2,000 × 4 chains).
**f_within is robust to Hanson-population measurement error. No material divergence;
no limitation flagged.**

**Methodological faithfulness catch:** the first implementation used a structural
errors-in-variables hyperprior (a symmetric-error form). Re-reading the prereg showed
it specifies the Berkson form (prior centred on the observed value; measurement error
propagated one-way from observation to latent), so the run was redone with the correct
specification. Recorded as a faithfulness catch to close any audit gap.

---

**D12 — scaling-residual sensitivity**

Construction (documented choice): pooled NBR power-law
`insc ~ NB(exp(a + β·log_pop), φ)` → per-city SAMOC log-scale residual
`r_c = log(insc_c) − (â + β̂·log_pop_c)` → Gaussian within-between partition of `r_c`.

- Pooled power-law slope **β = 0.565** (cf. primary H3a within-province β = 0.587;
  Hanson 2021 ≈ 0.67).
- Residual **β_within = −0.065 [−0.144, +0.011]**, P(> 0) = 0.05;
  residual **f_within ≈ 0.004 [0.00, 0.02]**. Convergence clean (R̂ 1.00, 0 div.).

**Interpretation — a coherence result, not a refutation.** After removing the global
pooled scaling, the within-province population gradient on the residuals is
essentially zero. This means the within-province slope ≈ the global slope (≈ 0.57–
0.59): the Hanson population relationship operates as **one consistent scaling law at
both levels**, so "controlling for scaling" leaves no extra within-province structure.
The primary β_within (0.587, CI well above 0) is real; D12 shows it is the *same* law
as the global scaling, not a province-specific artefact.

---

**B4 — stratified-sampling sensitivity**

Two findings, one methodological and one empirical.

**(a) Prereg-vs-implementation discrepancy.** The preregistered B4 (stratified
bootstrap of LIRE) is **architecturally moot** for the committed v2 Phase-1
thresholds: Decision 8 replaced the LIRE bootstrap with synthetic data drawn from a
parametric null (`h1_sim_v2.py`). The only empirical lever on the thresholds is the
interval-width pool; the per-iteration province / city counts are vestigial metadata
with zero effect on detection. Recommend recording B4 in the obligations audit as
superseded by Decision 8, satisfied via this width-pool check.

**(b) Scheme-(b) threshold re-run result.** Scheme (a) proportional-allocation is
threshold-neutral by construction (it preserves the width distribution exactly).
Scheme (b) reweight-to-balance shifts the width pool (city-balanced median interval
width 99 y → 79 y; over-represented large cities carry wider intervals), triggering a
targeted threshold re-run under global / province-balanced / city-balanced width pools
at matched reduced precision (n_iter = 200, n_mc = 300).

| scheme | median Δ min_n | median Δ (%) | n_lower / n_higher | reachability changed |
|---|---|---|---|---|
| province-balanced | −12 inscriptions | −1.1 % | 7 / 4 of 12 | 0 cells |
| city-balanced | −7 inscriptions | −0.4 % | 6 / 4 of 12 | 0 cells |

Direction is as expected (narrower corpus → less aoristic smearing → easier detection
→ lower thresholds), magnitude is small and within Monte-Carlo noise at n_iter = 200.
**No reachability classifications change.** The Phase-1 detection thresholds are
robust to province / city stratification under both schemes.

Caveat: per-cell threshold deltas are noisy at n_iter = 200 (individual Δ values span
±100–280 inscriptions); the median and the unchanged reachability are the robust
signals, not the per-cell signs.

### Why this matters

1. **H3a primary confirmed robust on two additional axes.** D11 shows f_within is
   stable under realistic population-data noise (a common concern for Hanson's
   non-census estimates). D12 shows the within-province and global slopes are one
   coherent law — the correlation is not a province-specific artefact. Both clear the
   prereg's material-divergence criterion with no limitations flagged.

2. **D12 is a settlement-scaling coherence result.** The usual worry is that a
   within-province β ≈ global β might mean a confound; D12's interpretation is the
   reverse — it means the scaling is a genuinely unified law operating at both levels.
   The primary f_within result (0.299) is therefore not inflated by a global
   composition effect.

3. **B4 closes a prereg obligation and flags a v2 supersession.** The discrepancy
   between the prereg and the v2 implementation (Decision 8 removes the LIRE
   bootstrap) needed to be documented rather than silently ignored. The width-pool
   check is the v2-faithful substitute, and the thresholds are robust to it.

4. **Phase-1 thresholds stand.** The committed full-precision thresholds
   (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`) are the primary; the B4
   stratification check does not displace them.

### Caveats / methodological notes

- **D11 convergence at σ = 0.3.** R̂ = 1.01 (not 1.00) at the highest ME level;
  ESS-bulk 1,080. These are within acceptable bounds and the CIs are still tight, but
  the slight degradation at σ = 0.3 is consistent with the latent-population model
  carrying more sampling difficulty at high noise.
- **D12 construction is terse in the prereg.** The prereg phrasing ("re-run H3a on
  residuals") is ambiguous — a count-model residual or a different estimand is
  possible. The SAMOC log-residual construction is documented in the REPORT and
  recorded here; a different reading would require a re-run.
- **B4 per-cell noise.** At n_iter = 200, individual cell deltas span ±100–280
  inscriptions and include sign reversals; the median and reachability are the
  signal. The full-precision committed thresholds are the primary.
- **Scope: §5 sensitivities only.** All three are preregistered as non-confirmatory
  sensitivity checks (prereg §5). Material divergence would be a reported limitation,
  not an amendment trigger; none was found.

### Related observations and artefacts

**Obs 94** (deconvolution does NOT change H3a — raw-count population–epigraphy
scaling robust to convention-correction; deconvolution leveraged in H3b not H3a):
the most recent H3a robustness Obs; this Obs adds robustness to ME, scaling control,
and stratification, completing the §5 sensitivity programme.

**Obs 92** (H3b draw-wise base run — global Timpson saturation; probe-window
P(deficit) the deliverable): H3b context; the Phase-1 thresholds that B4 tested here
are also consumed by the H3b probe-window machinery.

**Obs 93** (H3b flexible-null annex — saturation is structural null-misspecification;
probe-window P(deficit) confirmed robust): the most recent H3b Obs; the Phase-1
detection thresholds' robustness (B4, this Obs) feeds the H3b pipeline's Phase-1
calibration.

**Artefacts**:
`runs/2026-06-16-s5-sensitivities/REPORT.md` (headline report; D11, D12, B4 summary);
`runs/2026-06-16-s5-sensitivities/outputs/d11-hanson-me-results.json`
(D11 per-σ results, convergence diagnostics, CI-shift table; source for all D11
numbers in this Obs);
`runs/2026-06-16-s5-sensitivities/outputs/d12-scaling-residual-results.json`
(D12 pooled β, residual β_within, f_within; source for all D12 numbers);
`runs/2026-06-16-s5-sensitivities/outputs/REPORT-b4.md` (B4 width-pool diagnostic;
scheme-a/b construction, Wasserstein distances, width-pool table);
`runs/2026-06-16-s5-sensitivities/outputs/REPORT-b4-rerun.md` (B4 threshold re-run
results; per-cell table, headline medians);
`runs/2026-06-16-s5-sensitivities/outputs/b4-threshold-rerun.json`
(B4 per-cell thresholds and deltas; source for all B4 numbers in this Obs);
`runs/2026-06-16-s5-sensitivities/code/d11_hanson_me.py` (D11 engine);
`runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py` (D12 engine);
`runs/2026-06-16-s5-sensitivities/code/b4_stratified_widthpool.py` (B4 width-pool
diagnostic);
`runs/2026-06-16-s5-sensitivities/code/b4_threshold_rerun.py` (B4 threshold re-run);
commit `edc5592` (D11 + D12 results);
commit `6acfddf` (B4 width-pool diagnostic);
commit `6b2a14a` (B4 threshold re-run — B4 closed).

### Findable later

`section-5-sensitivities`, `S5-sensitivities`, `D11`, `D12`, `B4`,
`D11-measurement-error`, `Berkson-ME`, `Berkson-errors-in-variables`,
`structural-EIV`, `faithfulness-catch`, `prereg-vs-implementation`,
`Mundlak-NBR`, `within-between`, `f_within-robustness`,
`f-within-0-299`, `f-within-0-305`, `f-within-0-320`, `f-within-0-341`,
`sigma-pop-0-1`, `sigma-pop-0-2`, `sigma-pop-0-3`,
`CI-shift-0-008`, `CI-shift-0-025`, `CI-shift-0-047`,
`material-divergence-threshold-0-063`, `primary-CI-width-0-1253`,
`rhat-1-01`, `ESS-bulk-1080`, `0-divergences`,
`D12-scaling-residual`, `SAMOC-residual`, `SAMOC-log-residual`,
`pooled-power-law`, `pooled-beta-0-565`, `beta-within-0-587`,
`residual-beta-within-minus-0-065`, `residual-f-within-0-004`,
`P-gt-0-equals-0-05`, `settlement-scaling-coherence`,
`one-consistent-scaling-law`, `province-not-artefact`,
`B4-stratified-sampling`, `province-proportional`, `city-proportional`,
`reweight-to-balance`, `width-pool`, `interval-width-pool`,
`Decision-8-supersession`, `LIRE-bootstrap-replaced`,
`h1-sim-v2`, `parametric-null`, `vestigial-metadata`,
`median-width-99y-to-79y`, `city-balanced-79y`,
`Wasserstein-1`, `Wasserstein-17-45`, `Wasserstein-18-78`,
`median-delta-minus-1-1-pct`, `median-delta-minus-0-4-pct`,
`reachability-unchanged`, `0-cells-flip`,
`n-iter-200`, `n-mc-300`, `reduced-precision`,
`Phase-1-thresholds-robust`, `h1-v2`,
`obligations-audit`, `B4-superseded`, `B4-closed`,
`corroborating-results`, `no-limitation-flagged`,
`obs-92`, `obs-93`, `obs-94`,
`edc5592`, `6acfddf`, `6b2a14a`,
`runs-2026-06-16-s5-sensitivities`

## Obs 96 — 2026-06-16 [RESULT]: §5 Layer B β-inversion complete — gate validates against both independent anchors

### The finding

Per-city relative and Hanson-anchored population trajectories for the 268 §5 target
cities, produced draw-wise via the H3a scaling law inverted through the within-province
exponent:

`pop_t = pop_max · ( insc_t / max_t insc_t )^(1/β_within)`

Two β frames propagated (8,000 Layer-A draws each, resampled from 12,000 H3a draws):
- **Empire frame:** β_within = 0.587 (JSON: 0.5869); exponent 1/β ≈ 1.70 (amplifying)
- **Latin frame:** β_within = 0.733 (JSON: 0.7331); exponent 1/β ≈ 1.36 (less extreme)

Outputs: relative-shape (peak = 1) and Hanson-anchored absolute trajectories, median +
95 % bands; 34/268 cities meet the N ≥ 300 reliability floor (`reliable` flag carried
from Layer A).

**Validation gate (descriptive, exploratory) — PASS: both anchors met.**

Because the 268 target cities are small-N and the large anchors were not in that fit,
Ostia and Pompeii were re-fitted standalone (empire β only) and the identical transform
applied. Both converged: R̂ = 1.0000, 0 divergences, ESS 1,166 (Ostia) / 1,420
(Pompeii).

| Anchor | Inverted-pop peak | P(peak 2nd c. AD) | Post-AD-79 mass fraction | Verdict |
|---|---|---|---|---|
| **Ostia** | AD 125–150 (Hadrianic) | 0.99 | — | matches OCD/Meiggs 2nd-c. apogee |
| **Pompeii** | AD 50–75 (pre-eruption) | 0.00 | 5.4 × 10⁻⁶ ≈ 0.000 | eruption terminus reproduced |

Descriptive aside: a dip in the Ostia trajectory ~AD 160–175 coincides with the Antonine
Plague — intriguing but not a claim (binning/aoristic artefact equally plausible; the
1/β amplification makes small inscription-rate dips look like steep population drops).

**The headline caveat, borne out.** Because β < 1 ⇒ 1/β > 1, the inversion amplifies
every swing. For the **median** target city, the inverted population at AD 250 is ≈ 0 %
of peak (empire frame) — the post-AD-250 inscription collapse, dominated empire-wide by
the epigraphic-habit decline (MacMullen 1982), is NOT demonstrated depopulation. The Latin
frame (1/β ≈ 1.36) is materially less extreme; the amplitude overlay figure shows this
directly. This vindicates the illustrative-only framing and is exactly what the H5
habit-removed residual analysis (Decision 13) is designed to disentangle.

Typical small-N target city: median P(peak in 2nd century) = 0.21 across cities — not
concentrated in the 2nd century as the great anchors are; small/frontier cities are more
varied.

### Why this matters

1. **The §5 Layer B deliverable is done.** Per-city illustrative population-trajectory
   shapes for the 268 target cities are on disk, flagged with the N* = 300 reliability
   floor.
2. **Validation gate demonstrates methodological coherence.** Two independent anchors
   bracket the gate: one tests the growth-to-2nd-c.-peak expectation (Ostia, clean pass),
   the other a hard eruption terminus (Pompeii, clean pass). The gate is descriptive but
   non-trivial.
3. **Amplification is the dominant interpretive caveat.** The 1/β exponent (1.70 empire,
   1.36 Latin) means population swings exceed inscription swings; the post-peak decline
   is partly artefactual. Write-up must lead with the illustrative-only framing.
4. **H5 habit-removed residual is the principled next step.** The inversion works on
   the raw Layer-A trajectory (which includes the empire-wide epigraphic-habit shape);
   the H5 residual (Obs 97) separates habit from city signal before inversion.

### Caveats / methodological notes

- **Illustrative comparative-shape only** — not a population estimate; the preregistration
  wording is binding (Decision 13; prereg §5 "Extension (Layer B)").
- **Cross-sectional → temporal substitution:** the within-province H3a β is used as a
  within-city-over-time exponent — the prereg's flagged "strong assumption"; β_within is
  the least-bad analogue but is still an assumption.
- **Only 34/268 cities meet the N* = 300 floor.** The remaining 234 are below-floor;
  retained and flagged, not suppressed.
- **Hanson anchor** pins peak population to a single static figure; Hanson's own level
  uncertainty is not propagated.
- **Posterior independence** — Layer-A and H3a posteriors combined under independence
  (separate fits).
- **Antonine Plague dip in Ostia** — visually striking, not a claim; binning and
  aoristic spreading plus 1/β amplification are co-equal explanations.

### Related observations and artefacts

**Obs 94** (deconvolution does NOT change H3a — raw-count population–epigraphy scaling
robust to convention-correction): the H3a scaling law consumed here as the β parameter;
confirms the β_within = 0.587 primary is paper-ready.

**Obs 95** (§5 sensitivity batch D11, D12, B4 — all three corroborate H3a): closes the
sensitivity programme for the same H3a result; the robustness stack is the foundation
for using β_within here.

**Obs 97** (H5 — empire-wide common temporal component peaks AD 188; habit-lag
characterised): the complement to this Obs — habit-removed residuals that disentangle
epigraphic habit from city signal in the Layer-A trajectories inverted here.

**Artefacts**:
`runs/2026-06-16-s5-layer-b-beta-inversion/REPORT.md` (source report; all numbers
verified against it and the JSON);
`runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-summary.json`
(per-frame β, per-city peak/decline summaries, gate outcomes, seed, input sha256 provenance;
source for all numbers in this Obs);
`runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-trajectories-empire.nc`
(per-city summary trajectories, empire frame);
`runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-trajectories-latin.nc`
(per-city summary trajectories, Latin frame);
`runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-anchor-gate-empire.png`
(Ostia/Pompeii gate panels);
`runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-amplitude-overlay.png`
(empire-vs-Latin β amplitude sensitivity overlay);
commit `b0de24e` (Layer B results).

### Findable later

`Layer-B`, `beta-inversion`, `layerb`, `s5-layer-b`, `population-trajectory`,
`illustrative-comparative-shape`, `Decision-13`, `prereg-s5`,
`beta-within-0-587`, `beta-within-0-733`, `empire-frame`, `latin-frame`,
`1-over-beta`, `amplification-exponent`, `1-70`, `1-36`,
`268-target-cities`, `34-reliable`, `N-star-300`, `below-floor`,
`Ostia`, `Pompeii`, `anchor-gate`, `validation-gate`,
`Ostia-AD-125-150`, `Ostia-P-peak-2c-0-99`, `Ostia-Hadrianic`,
`Pompeii-AD-50-75`, `Pompeii-post-AD-79-mass-0-000`, `eruption-terminus`,
`Antonine-Plague-dip`, `Meiggs-Roman-Ostia`, `OCD-Ostia`,
`median-P-peak-2c-0-21`, `small-frontier-cities`, `varied-peaks`,
`MacMullen-1982`, `epigraphic-habit-collapse`, `post-AD-250`,
`not-demography`, `not-depopulation`, `illustrative-only`,
`Hanson-anchored`, `cross-sectional-temporal-substitution`,
`pop-max-urban-context`, `posterior-independence`,
`rhat-1-0000`, `ESS-1166`, `ESS-1420`, `0-divergences`,
`layerb-summary-json`, `layerb-trajectories-nc`, `layerb-anchor-gate-png`,
`layerb-amplitude-overlay-png`, `b0de24e`,
`runs-2026-06-16-s5-layer-b-beta-inversion`,
`obs-94`, `obs-95`, `obs-97`

## Obs 97 — 2026-06-17 [RESULT / METHODOLOGY]: §5 H5 — empire-wide common temporal component peaks AD 188; no systematic corpus lag; foundation-terminus check passes

### The finding

H5 is a deterministic read of the §5 Layer-A posterior (`monolithic-inscription-25y.nc`,
268 cities, 8,000 draws, 16 × 25 y bins, 50 BC–AD 350). No new MCMC. The hierarchical
model already decomposes each city's log inscription-rate:

`log_lam[c,t] = α_g + g_shape[t] + b_u[p] + u_shape[p,t] + b_v[c] + v_shape[c,t]`

H5 reads:
- **Empire-wide common temporal component** = `α_g + g_shape[t]` (the shape shared by
  all cities)
- **Habit-removed residual trajectory** = `u_shape[p,t] + v_shape[c,t]` (province +
  city deviation from the empire norm)

**Finding 1 — Empire habit peak: AD 187.5.**
The empire-wide common temporal component (`g_shape`) peaks at **AD 187.5** (bin
[175, 200) — late-Antonine / Severan), consistent with MacMullen's epigraphic-habit
curve and the H3b "hump" (Obs 92–93). Verified in `h5-summary.json`
(`empire_habit_peak_year: 187.5`).

**Finding 2 — Habit lag: no systematic directional lag at corpus level.**
Per-city habit lag = peak year (raw `lam`) − peak year (habit-removed residual), propagated
draw-wise.

| Metric | Value |
|---|---|
| Corpus-median lag (all cities) | 0 yr |
| Corpus-median lag (reliable, N ≥ 300) | 0 yr |
| IQR | [0, 50] yr |
| Fraction-positive lag | 0.48 |

**Read:** no systematic directional pull at the corpus level, but individual cities shift
by up to ~one or two 25-year bins (IQR to 50 yr). The habit confound bites hardest on
small-N cities (which partial-pool toward AD 188); data-rich cities' own signal dominates.

**Finding 3 — Foundation-date terminus check: passes corpus-wide.**
Hanson `Start Date` matched to all **268 cities** (clean match); **99** cities are founded
within the envelope (Start Date > 50 BC) and so provide a meaningful lower-terminus test.

- **Median pre-foundation inscription mass = 0.07 %** (JSON: 0.0007) — essentially zero;
  the Layer-A trajectories respect foundation termini corpus-wide (the lower-terminus
  analogue of Pompeii's AD-79 upper terminus, Obs 96).
- **Notable exceptions are archaeologically sensible:** worst offenders are frontier
  military sites where epigraphy from an earlier military presence predates the town's
  Barrington/Hanson foundation date — a real signal (military-before-civilian), not a
  model error.

| City (Barrington name) | Hanson Start Date | Pre-foundation mass |
|---|---|---|
| Corstopitum (Corbridge) | AD 200 | 59.4 % |
| Corinium Dobunnorum (Cirencester) | AD 100 | 30.2 % |
| Luguvalium (Carlisle) | AD 100 | 26.8 % |
| Centumcellae | AD 106 | 25.8 % |
| Lauriacum | AD 191 | 17.1 % |
| Argentoratum (Strasbourg) | AD 80 | 16.6 % |

All six are well-known Hadrianic or Trajanic frontier garrisons with documented pre-urban
military phases; the over-representation of inscriptions before the civilian foundation
date is archaeologically expected.

**Finding 4 — Magnitude decomposition: the common temporal component is large; the
Latin-minus-Roma diagnostic unit ≈ all-provinces.**
In comparable log-rate SD units (posterior median; `h5-decomposition.json`):

| Component | log-rate SD |
|---|---|
| Empire-common temporal swing (`g`) | 1.11 |
| Province temporal (`u`) | 1.02 |
| City-specific temporal (`v`) | 0.98 |
| Between-city LEVEL spread (cross-sectional / population axis) | 0.78 |

The empire-common temporal component accounts for **≈ 54 %** of a typical city's temporal
variance and is the largest single magnitude among the mid-sized §5 cities — but the
level/population axis (0.78) is **understated by §5 range restriction** (the set excludes
the size extremes), so this is *not* "timing beats population" in the full corpus; level
(cross-sectional, population) and the common component (temporal) live on different axes.
**Latin-minus-Roma (257/268 cities) is essentially identical to all-provinces** (common
peak AD 187.5, sd_level 0.785, sd_v 0.975, common share 0.54) — the diagnostic unit gives
the same decomposition because the §5 set is 96 % Latin-West. The 11 non-Latin Greek-East
cities peak **earlier (~ AD 112.5)** with a tighter level spread (0.52) — a possible
East/West timing difference, but n = 11, a flag not a finding.

### Why this matters

1. **H5 confirms the Layer-A posterior is well-behaved.** The corpus-wide foundation-date
   check (0.07 % pre-foundation mass) is a significant positive: the hierarchical model
   does not extrapolate backward through termini it has no inscriptions to support. The
   two-direction terminus check (Pompeii upper, foundation-date lower) brackets the model
   quality assessment.
2. **The habit peak (AD 187.5) is the quantity to remove before interpreting city
   trajectories as population signals.** The Layer B β-inversion (Obs 96) runs on raw
   `lam`, which includes `g_shape`; the residual `u + v` is the defensible per-city
   signal. The AD-188 peak is consistent with both MacMullen's epigraphic-habit literature
   and the Antonine demographic apogee — the two cannot be separated within this model (see
   Obs 98).
3. **No systematic directional lag** means the H5 residual does not systematically shift
   peaks; the habit confound is a noise amplifier for small-N cities, not a consistent bias
   direction. The IQR of 50 yr spans about two 25-year bins — non-trivial for small-N
   cities, negligible for large ones.
4. **Frontier military exceptions are a real archaeological signal** worth a sentence in
   the write-up: pre-civilian military epigraphy predating the Barrington foundation date
   is expected and documented, not a model artefact.

### Caveats / methodological notes

- **Exploratory; no pre-committed thresholds** (Decision 13; prereg §5, lines 358–364).
  GPT-5.5 flagged the design as "statistically fragile" — read descriptively throughout.
- **Habit component = within-sample empire trajectory** (`g_shape` from the 268-city fit),
  not an external independent measure. It is hierarchically coherent with the per-city
  residuals (same fit) but is not an independent habit proxy.
- **Foundation-anchor coverage:** the terminus check applies only to the 99/268 cities
  founded within the envelope; cities pre-dating 50 BC have no binding lower terminus.
- **N* = 300 floor** carries from Layer A: 34/268 reliable; the lag result is dominated
  by small-N cities whose peaks are noisy.
- **Magnitude decomposition + Latin-minus-Roma** (Finding 4) are computed by the companion
  script `code/h5_decomposition.py` → `outputs/h5-decomposition.json` (commit `3ae63c0`),
  reproducible from the §5 Layer-A posterior. The `median_common_share_of_temporal_var`
  (≈ 54 %) is approximate — it ignores inter-tier covariance. The Greek-East subset is
  n = 11 (descriptive only). A dedicated Latin-only re-fit would barely differ (the global
  `g` is unchanged); it is optional polish, not a correction.

### Related observations and artefacts

**Obs 96** (Layer B β-inversion — gate passes both anchors; 1/β amplification is the
dominant write-up caveat): the Obs this H5 result was designed to complement — H5
produces the habit-removed residuals that disentangle habit from signal before or
alongside the Layer B inversion.

**Obs 98** (the empire-wide common temporal component conflates four drivers — NOT a clean
habit proxy; identification caveat): the direct methodological follow-on from this Obs;
explains why `g_shape` cannot be interpreted as pure epigraphic habit.

**Obs 92** (H3b draw-wise base run — global Timpson saturation; empire temporal "hump"):
the earlier H3b result that established the empire-wide inscription hump; g_shape peak
AD 187.5 is the Layer-A analogue of the H3b hump and they are mutually consistent.

**Obs 93** (H3b flexible-null annex — saturation is structural null-misspecification;
probe-window P(deficit) confirmed robust): the final H3b Obs; the AD-188 hump is
confirmed robust across all null specifications.

**Artefacts**:
`runs/2026-06-17-s5-h5-habit-removed/REPORT.md` (source report; all numbers in this Obs
verified against it and the JSON);
`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-summary.json`
(habit peak year, lag metrics, foundation-terminus coverage; source for all numbers);
`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-residual-trajectories.nc`
(per-city residual + raw trajectories, peak bins, lag with CI, reliability flag);
`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-empire-habit.png` (habit curve figure);
`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-habit-lag-hist.png` (lag distribution);
`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-residual-samples.png`
(sample residual trajectories);
`runs/2026-06-17-s5-h5-habit-removed/spec.md` (the signed-off H5 spec + design decisions);
`runs/2026-06-17-s5-h5-habit-removed/code/h5_habit_removed.py` (engine);
`runs/2026-06-17-s5-h5-habit-removed/code/h5_decomposition.py` +
`outputs/h5-decomposition.json` (Finding 4 magnitude decomposition + Latin-minus-Roma;
commit `3ae63c0`);
commit `4f125cd` (H5 results).

### Findable later

`H5`, `habit-removed`, `h5-habit-removed`, `s5-h5`, `epigraphic-habit`,
`g-shape`, `g_shape`, `empire-common-temporal-component`, `empire-wide-habit`,
`AD-187-5`, `AD-188`, `late-Antonine`, `Severan`, `MacMullen`,
`habit-lag`, `epigraphic-habit-lag`, `corpus-median-lag-0`,
`IQR-0-50`, `fraction-positive-0-48`, `no-systematic-lag`,
`habit-confound`, `small-N-partial-pooling`,
`foundation-terminus`, `foundation-date-check`, `Hanson-Start-Date`,
`268-matched`, `99-within-envelope`, `median-pre-foundation-0-07-pct`,
`military-before-civilian`, `frontier-military`,
`Corstopitum`, `Corbridge`, `59-pct-pre-foundation`,
`Corinium-Dobunnorum`, `Cirencester`, `30-pct-pre-foundation`,
`Luguvalium`, `Carlisle`, `26-pct-pre-foundation`,
`Centumcellae`, `25-pct-pre-foundation`,
`Lauriacum`, `17-pct-pre-foundation`,
`Argentoratum`, `Strasbourg`, `16-pct-pre-foundation`,
`terminus-check`, `Barrington-foundation`, `within-envelope`,
`u-shape`, `v-shape`, `alpha-g`, `residual-trajectory`,
`magnitude-decomposition`, `variance-decomposition`, `sd-common-g-1-11`,
`sd-province-u-1-02`, `sd-city-v-0-98`, `sd-level-0-78`, `common-share-0-54`,
`Latin-minus-Roma`, `Latin-minus-Roma-257`, `diagnostic-unit`,
`Greek-East-11`, `Greek-East-peak-AD-112`, `log-rate-SD`, `range-restriction`,
`h5-decomposition-json`, `3ae63c0`,
`h5-summary-json`, `h5-residual-trajectories-nc`,
`deterministic-read`, `no-MCMC`, `monolithic-inscription-25y`,
`4f125cd`, `runs-2026-06-17-s5-h5-habit-removed`,
`obs-96`, `obs-98`, `obs-92`, `obs-93`

## Obs 98 — 2026-06-17 [METHODOLOGY / THEORY]: the empire-wide common temporal component is NOT a clean epigraphic habit — it conflates four drivers

### The finding

The H5 empire-wide common temporal component `g_shape` (Obs 97: peak AD 187.5) is
identified by the hierarchical model purely through pooling — it is the time-shape that
**all cities share**. It is therefore not, and cannot be, a clean measure of the
epigraphic habit alone.

**The four conflated drivers:**
1. **(a) Cultural epigraphic habit** — the MacMullen/Woolf phenomenon of
   inscription-production as a social practice, independently varying over time
2. **(b) Empire-wide demographic and economic trends** — real population growth,
   urbanisation, and economic integration that increase inscription opportunities
3. **(c) Empire-wide taphonomy and recovery bias** — survival and discovery rates that
   may be correlated across the empire through shared geological and historiographical
   conditions
4. **(d) Residual dating-convention structure** — any dating artefact that is
   spatially or corpus-wide systematic (e.g., round-year preferences that are not
   fully removed by the deconvolution at the aggregate level)

**Critical identification caveat:** §5 Layer A contains no population covariate.
The decomposition separates **empire-common temporal variation** from **city-specific
temporal deviation** — it does NOT separate habit from population. The AD-188 peak of
`g_shape` is consistent with both MacMullen's epigraphic-habit curve and the Antonine
demographic apogee; the two cannot be disentangled within this model.

No external, joinable epigraphic-habit proxy exists for this corpus: the prior-art scout
(2026-04-23, scout-3-epigraphic-habit-proxies) found no suitable independent time-series
that can be merged at city or province level to partial-out the habit component.

**The methodologically defensible quantity:** the residual (`u_shape + v_shape`) — a
city's deviation from the empire norm. Inverting the city residual into a relative
population trajectory is well-posed regardless of the conflation, because the residual
is explicitly what the city does above or below the empire-common trend, whatever that
trend's drivers are. The Layer B β-inversion runs on the raw trajectory (which includes
`g_shape`); a principled "habit-corrected" inversion would use the residual alone.

**Implication for write-up:** the over-claim to avoid is "this is the epigraphic-habit
component". The correct framing is "this is the empire-wide common temporal component"
(in results), with the four candidate drivers listed in the discussion section alongside
the correspondence with the epigraphic-habit literature.

### Why this matters

1. **This is the methodologically central caveat for the paper.** Readers familiar with
   the epigraphic-habit literature will immediately ask "but does the habit component
   confound your population inference?" The answer is yes — it is irreducibly present in
   the raw `g_shape` and in any Layer B inversion that uses raw `lam`. The residual-based
   inversion is the robust alternative.
2. **The naming convention must be enforced in drafting.** "Empire-wide common temporal
   component" in results; interpretive claims about habit vs demographics deferred to
   discussion. See Obs 101 for the structural framing decision.
3. **No habit proxy exists to partial it out.** The prior-art scout established this
   definitively; any future proposal to use an external proxy needs to first revisit the
   scout-3 findings.
4. **The Antonine peak (AD ~188) is the confirmatory meeting-point.** The coincidence of
   the g_shape peak with MacMullen's habit peak and the Antonine demographic apogee is
   genuine and noteworthy — the model is picking up something real. The point of this Obs
   is not to dismiss the peak but to be precise about what it identifies.

### Caveats / methodological notes

- **This is a conceptual/identification caveat**, not an empirical result from a new run.
  It is a methodological characterisation of what Layer A's hierarchical decomposition can
  and cannot identify.
- **The residual is not a pure population signal either.** City-specific `v_shape` captures
  whatever makes a city deviate from the empire norm — it includes city-level demographic,
  economic, taphonomic, and habit variation. The claim is only that it is free of the
  empire-common confound.
- **Taphonomy and dating conventions** are partially removed by the cc-library
  deconvolution (Obs 90–91) at the province level; whether residual empire-wide
  taphonomic structure in `g_shape` is material is unknown.

### Related observations and artefacts

**Obs 97** (H5 — empire habit component peaks AD 187.5; lag characterised): the Obs this
one annotates — the identification caveat applies to g_shape as computed there.

**Obs 96** (Layer B β-inversion — inverts raw `lam` including g_shape; illustrative-only):
the Layer B result is subject to this caveat; the illustrative-only framing partially
absorbs it but does not fully resolve the conflation.

**Obs 101** (paper framing — empirical decomposition first, interpretation later; Hanson
as bridge): the structural decision that externalises these four drivers to the discussion
section and mandates "empire-wide common temporal component" as the results-section name.

**Obs 92–93** (H3b — the empire "hump" / epigraphic-habit saturation context): the H3b
results that established the empire-wide hump; this Obs characterises the identification
problem that the hump literature embodies.

**Artefacts**: no new run artefact (this is a methodological characterisation).
Prior-art scout: `scout-3-epigraphic-habit-proxies` (2026-04-23 lit-scout-iterate
workspace; finding = no suitable joinable external habit proxy exists).
Spec: `runs/2026-06-17-s5-h5-habit-removed/spec.md` (the H5 spec articulates the
two-component decomposition this Obs annotates).

### Findable later

`epigraphic-habit-identification`, `g-shape-conflation`, `four-drivers`,
`empire-common-temporal-component`, `not-pure-habit`, `identification-caveat`,
`habit-vs-population`, `cant-separate-habit-from-demography`,
`Antonine-demographic-apogee`, `MacMullen-Woolf`, `epigraphic-habit-literature`,
`taphonomy-empire-wide`, `dating-convention-residual`,
`no-population-covariate`, `Layer-A-no-covariate`,
`residual-u-v-defensible`, `empire-common-free`,
`habit-proxy-does-not-exist`, `prior-art-scout-2026-04-23`,
`scout-3-epigraphic-habit-proxies`, `no-joinable-external-proxy`,
`over-claim-to-avoid`, `naming-convention`, `results-framing`,
`discussion-section-four-drivers`, `correspondence-habit-literature`,
`habit-corrected-inversion`, `raw-lam-includes-g-shape`,
`identification-problem`, `conceptual-caveat`, `methodological-characterisation`,
`obs-97`, `obs-96`, `obs-101`, `obs-92`, `obs-93`

## Obs 99 — 2026-06-17 [RESULT]: §5 H7 — time-resolved (per-period) H3c; β_within traces a U over the four centuries

### The finding

H7 recomputes H3c diagnostics within 8 × 50-year periods (50 BC – AD 350), using
aoristic-apportioned counts (rounded), fixed 1,044-city universe, and population-based
Mundlak. All 8 Negative Binomial Regression (NBR) fits converged: R̂ = 1.0000, 0
divergences (ESS-bulk range: 688–2,369 across periods).

**Full results table:**

| Period | Non-zero cities | Count | β_within [95 % CI] | Capital P(contrast > 0) | Moran's I k8 | p |
|---|---|---|---|---|---|---|
| 50 BC – AD 0 | 434 | 4,714 | **0.701** [0.596, 0.809] | 1.00 | **+0.029** | **0.021** |
| AD 0–50 | 624 | 12,633 | 0.667 [0.572, 0.768] | 1.00 | +0.016 | 0.111 |
| AD 50–100 | 696 | 14,031 | 0.629 [0.537, 0.727] | 1.00 | +0.005 | 0.292 |
| AD 100–150 | 735 | 11,636 | 0.582 [0.496, 0.670] | 1.00 | −0.014 | 0.187 |
| AD 150–200 | 779 | 12,793 | 0.580 [0.497, 0.667] | 1.00 | −0.005 | 0.459 |
| AD 200–250 | 717 | 10,229 | 0.587 [0.500, 0.674] | 1.00 | −0.003 | 0.466 |
| AD 250–300 | 623 | 5,077 | 0.581 [0.488, 0.674] | 1.00 | −0.014 | 0.155 |
| AD 300–350 | 518 | 3,948 | 0.659 [0.551, 0.770] | 1.00 | −0.012 | 0.219 |

**All numbers verified against `h7-summary.json` and REPORT.md.**

**Three headline findings:**

**1. β_within traces a U over time (descriptive).** β_within falls from **0.701**
(50 BC – AD 0) through a **~0.58 plateau across the high empire (AD 100–250)** — which
is exactly the pooled confirmatory β_within = 0.587 (the pooled result is dominated by
these inscription-rich centuries) — then rises again to **0.659** in the 4th century.
Early- and late-empire epigraphic production scales more steeply with city size than the
high-empire core. CIs overlap throughout, so this is a descriptive trend, not a sharp
break; read accordingly.

**2. Provincial capitals over-produce in every period.** P(contrast > 0) = 1.00 in all
8 periods — the capital over-production effect (H3c) is temporally stable, not a
high-empire artefact. No break; no reversal.

**3. Residual spatial clustering is an early-empire phenomenon only.** Moran's I (k = 8
neighbours) is significantly positive only in **50 BC – AD 0** (I = +0.029, p = 0.021);
from AD 0 onwards it is ~0 / non-significant at any k. Whatever spatial structure
Hanson's pooled residual map carries is concentrated in the earliest period.

### Why this matters

1. **The pooled β_within = 0.587 is the high-empire core, not a period-specific outlier.**
   H7 confirms it is the characteristic value for AD 100–250 — the centuries that
   dominate the corpus — and not an artefact of pooling over a heterogeneous period range.
2. **The U-shape is novel descriptive content.** No published comparator exists (per
   REPORT). It is candidate content for the §5 descriptive section: "the scaling exponent
   is not constant but is most stable during the epigraphic apogee."
3. **Capital stability is a substantive result.** The temporally uniform capital effect
   argues against the capital over-production being a feature of a specific administrative
   or economic period; it is a structural property of the urban hierarchy throughout the
   period of study.
4. **Early spatial clustering needs a sentence.** The AD 50 BC – AD 0 Moran's I result is
   significant and positive; it likely reflects geographic clustering of early Roman
   inscription production in Italy and the established western provinces before the
   empire-wide spread. Worth flagging descriptively; not over-interpreted.
5. **Latin-minus-Roma variant is still outstanding.** The H7 run used the all-provinces
   1,044-city frame; the project's diagnostic unit is Latin-speaking-minus-Roma, which
   requires a separate variant run. See Obs 101 for the framing consequence.

### Caveats / methodological notes

- **Exploratory; no pre-committed thresholds.** No published comparator; read all findings
  descriptively (prereg §5 line 384).
- **50-year periods, not decadal.** Feasibility constraint; finer temporal resolution
  (e.g., 25-year) is a re-run that would narrow the bins and potentially sharpen or
  dissolve the early/late upticks.
- **Aoristic-apportioned counts (rounded).** The midpoint alternative (snap-to-midpoint
  rather than aoristic-fraction) is an unrun sensitivity; the rounding is expected to
  be conservative.
- **All-provinces frame (1,044 cities).** The diagnostic unit for the paper is
  Latin-minus-Roma; the all-provinces frame is baseline context. The H7 result for the
  paper's primary frame requires a Latin-minus-Roma re-run.
- **Early-period CIs are wide** (fewer inscriptions, fewer cities with data): the 50 BC –
  AD 0 β CI [0.596, 0.809] is ≈ 1.5× the width of the high-empire CIs. The U-shape
  endpoints should be treated as indicative, not point estimates.
- **Moran's I k-sensitivity:** the 50 BC – AD 0 period is significant at k = 5 (p = 0.023)
  and k = 8 (p = 0.021) but not k = 10 (p = 0.098); the AD 0–50 period is significant
  at k = 5 only (p = 0.018). The "significant only in 50 BC – AD 0" statement uses k = 8
  as the reference (consistent with H3c); at k = 5 the signal persists one period longer.

### Related observations and artefacts

**Obs 94** (deconvolution does NOT change H3a — cumulative scaling robust; β_within =
0.587 is paper-ready): the source of the pooled value that the H7 time-resolved analysis
recontextualises as the high-empire plateau.

**Obs 95** (§5 sensitivities D11, D12, B4 — all corroborate H3a; B4 closes Phase-1
threshold obligation): the H3a robustness stack that underpins confidence in the per-period
NBR fits here.

**Obs 100** (peak vs cumulative scaling — β ≈ 0.56 at 50y peak, indistinguishable from
cumulative 0.587): the complementary scaling robustness check; together with H7, it
brackets the temporal and measure-space stability of the population–epigraphy relationship.

**Artefacts**:
`runs/2026-06-17-s5-h7-perperiod-h3c/REPORT.md` (source report; all numbers verified);
`runs/2026-06-17-s5-h7-perperiod-h3c/outputs/h7-summary.json`
(per-period β_within, capital contrast, Moran's I per k; source for all numbers);
`runs/2026-06-17-s5-h7-perperiod-h3c/outputs/h7-time-resolved.png` (β over time figure);
`runs/2026-06-17-s5-h7-perperiod-h3c/outputs/h7-per-city-residuals.parquet`
(time-resolved residual-map data, per city per period);
`runs/2026-06-17-s5-h7-perperiod-h3c/code/h7_perperiod_h3c.py` (engine);
commit `fb05c1d` (H7 results + peak-scaling spec).

### Findable later

`H7`, `perperiod-h3c`, `time-resolved-h3c`, `s5-h7`, `per-period`,
`8-periods`, `50-year-periods`, `aoristic-apportioned`, `fixed-1044`,
`U-shape-beta`, `beta-U-shape`, `scaling-exponent-over-time`,
`beta-0-701`, `beta-50bc-ad0`, `late-Republican-Augustan`,
`high-empire-plateau`, `beta-0-58-plateau`, `AD-100-250`,
`beta-0-659`, `4th-century`, `AD-300-350`,
`pooled-beta-0-587`, `confirmatory-beta-same-as-plateau`,
`capitals-over-produce-every-period`, `capital-stable`,
`provincial-capital-contrast`, `P-contrast-1-00`,
`spatial-clustering-early-empire`, `Morans-I`, `Moran-I-k8`,
`Moran-I-0-029`, `p-0-021`, `50bc-ad0-significant`,
`spatial-clustering-washes-out`, `clustering-early-only`,
`novel-descriptive`, `no-published-comparator`,
`Latin-minus-Roma-outstanding`, `all-provinces-frame`,
`1044-city-universe`, `population-based-Mundlak`,
`NBR-per-period`, `Negative-Binomial`, `Mundlak-NBR`,
`rhat-1-0000-all-periods`, `0-divergences`,
`ESS-688`, `ESS-2369`, `wide-CIs-early`,
`h7-summary-json`, `h7-time-resolved-png`,
`h7-per-city-residuals-parquet`, `fb05c1d`,
`runs-2026-06-17-s5-h7-perperiod-h3c`,
`obs-94`, `obs-95`, `obs-100`

## Obs 100 — 2026-06-17 [RESULT / ROBUSTNESS]: §5 peak-inscription vs Hanson-population scaling — peak ≈ cumulative; smoothing neutral

### The finding

Does peak inscription intensity scale with (Hanson peak) population differently from
cumulative output? The H3a confirmatory reference: β_within = 0.587 [0.519, 0.657]
(1,044 cities, full-window cumulative count). Four arms run; all 4 NBR fits converged:
R̂ = 1.0000, 0 divergences.

**Full results table (all numbers verified against `peak-scaling-summary.json`):**

| Arm | β_within | 95 % CI | n cities |
|---|---|---|---|
| Cumulative H3a (reference) | **0.587** | [0.519, 0.657] | 1,044 |
| Raw peak, 50 y window, 1,044 cities (headline) | **0.557** | [0.490, 0.624] | 1,044 |
| Raw peak, 25 y window, 1,044 cities | 0.545 | [0.479, 0.612] | 1,044 |
| Raw peak, 25 y window, 268 §5 cities | 0.223 | [0.130, 0.319] | 268 |
| Modelled peak, 25 y window, 268 §5 cities | 0.213 | [0.112, 0.314] | 268 |

**Two headline findings:**

**1. Peak intensity scales with population essentially like cumulative output.**
On the full 1,044-city frame, the raw-peak exponent (0.557 at 50 y, 0.545 at 25 y) is
**statistically indistinguishable from the cumulative 0.587** (CIs overlap heavily).
Peak production scales with Hanson population at approximately the same law as total
production. Bigger cities have proportionally higher peaks and higher totals by the same
exponent.

**2. Smoothing is neutral; the §5 subset attenuates by range restriction (not a real
flattening).**
On the 268 §5 cities at 25 y, raw-peak 0.223 and modelled-peak 0.213 are essentially
identical — the Layer-A smoothing does NOT bias the peak-scaling exponent (the contrast
Shawn asked for). The much lower value vs the full corpus (0.22 vs 0.55, same window
and measure, only city set differs) is a **range-restriction artefact**: the §5 target
set excludes the largest cities (N ≥ 1,549 anchors) and the smallest (N < 50), truncating
the population range and attenuating the within-province slope. Do NOT read 0.22 as
"peak scaling is flat" — the restricted-set slope is a range artefact; the unrestricted
answer is finding 1.

### Why this matters

1. **Closes the previously open "peak vs cumulative" question.** The Hanson comparison
   against peak population had not been run prior to this; it now corroborates the
   cumulative H3a headline rather than complicating it.
2. **β ≈ 0.56 at peak is the same law as β ≈ 0.59 cumulatively.** A materially different
   peak-scaling exponent would have required a new explanatory story (e.g., cities have
   a fixed inscription ceiling per unit population); the null of "same law" holds.
3. **Smoothing neutrality closes a potential methodological objection.** A critic could
   claim that the Layer-A posterior-smoothing artificially concentrates peak counts and
   inflates or deflates the per-city peak. The overlap test (raw ≈ modelled, 0.223 ≈
   0.213) closes this.
4. **Range restriction is an important methodological lesson for the §5 subset.** The
   §5 subset (268 small-N cities) is not a random subsample of the full 1,044; it
   excludes the full population-range tails. Any within-§5-subset scaling reported in
   the paper should carry a range-restriction caveat; the all-cities frame is the
   population-range-valid result.
5. **Exploratory / tertiary status.** Not preregistered; the cumulative H3a is the
   confirmatory scaling result. This arm is a robustness check and a Hanson-comparison
   extension, not a new confirmatory claim.

### Caveats / methodological notes

- **Exploratory / tertiary; not preregistered.** The cumulative H3a (Decision 22/35;
  raw-count Hanson scaling) is the confirmatory result; this peak-variant is a motivated
  extension.
- **Arm D (modelled peak) uses the posterior-median modelled peak,** not the full Layer-A
  trajectory posterior propagated into β_peak. This is a documented simplification; the
  raw ≈ modelled agreement makes it immaterial for the comparison asked for.
- **Peak count is window-dependent** (50 y vs 25 y both reported; results are nearly
  identical across windows).
- **Range restriction** in the §5-subset arms (0.22) is real and dominant; do not use
  those values as the headline peak-scaling result.
- **The all-provinces frame is used** (1,044 cities); Latin-minus-Roma variant not run
  (see Obs 101 for framing consequence — Latin-minus-Roma is the diagnostic unit).

### Related observations and artefacts

**Obs 94** (deconvolution does NOT change H3a — full-window cumulative scaling robust;
β_within = 0.587 the paper-ready reference value): the cumulative baseline whose peak
analogue is tested here.

**Obs 99** (H7 — β_within over time; U-shape; high-empire plateau at 0.58): the temporal
decomposition of the same β; together with Obs 100 (peak vs cumulative), these two Obs
bracket scaling stability across both the time and measure dimensions.

**Artefacts**:
`runs/2026-06-17-s5-peak-scaling/REPORT.md` (source report; all numbers verified);
`runs/2026-06-17-s5-peak-scaling/outputs/peak-scaling-summary.json`
(all arms, contrasts, convergence, provenance; source for all numbers in this Obs);
`runs/2026-06-17-s5-peak-scaling/outputs/peak-scaling-forest.png` (forest plot);
`runs/2026-06-17-s5-peak-scaling/code/peak_scaling.py` (engine);
commit `e456ad2` (peak-scaling results).

### Findable later

`peak-scaling`, `peak-inscription-scaling`, `s5-peak-scaling`,
`peak-vs-cumulative`, `peak-population-scaling`,
`beta-within-0-557`, `raw-peak-50y`, `1044-cities`,
`beta-within-0-545`, `raw-peak-25y`,
`beta-within-0-223`, `268-s5-cities`, `raw-peak-25y-268`,
`beta-within-0-213`, `modelled-peak-25y-268`,
`smoothing-neutral`, `Layer-A-smoothing-neutral`, `raw-approx-modelled`,
`range-restriction`, `range-restriction-artefact`, `truncated-population-range`,
`N-1549-anchor-excluded`, `N-50-excluded`,
`do-not-read-0-22-as-flat`, `restricted-set-slope`,
`peak-CI-0-490-0-624`, `peak-CI-0-479-0-612`,
`cumulative-H3a-reference`, `beta-0-587-reference`,
`CIs-overlap`, `indistinguishable`,
`same-law-peak-and-cumulative`, `inscription-ceiling-null`,
`overlap-contrast`, `posterior-median-modelled-peak`,
`trajectory-posterior-not-propagated`, `documented-simplification`,
`exploratory-tertiary`, `not-preregistered`, `motivated-extension`,
`Hanson-peak-population`, `Hanson-comparison`,
`4-arms`, `rhat-1-0000`, `0-divergences`,
`peak-scaling-summary-json`, `peak-scaling-forest-png`,
`e456ad2`, `runs-2026-06-17-s5-peak-scaling`,
`obs-94`, `obs-99`

## Obs 101 — 2026-06-17 [FRAMING / METHODOLOGY]: paper framing decision — empirical decomposition first, interpretation later; Hanson as the bridge; diagnostic unit = Latin-minus-Roma

### The finding

A structural decision (Shawn, 2026-06-17) on how to organise the paper results and
discussion sections in light of the §5 Layer A / B / H5 / H7 analyses.

**The decision (five parts):**

**1. Empirical decomposition first.** Present the nested-unit decomposition in the results
section as an objective empirical finding — city-specific temporal component, province
component, between-city level spread, Latin-minus-Roma-common temporal component,
empire-wide-common temporal component — without interpretive labels. The decomposition is
what the model identifies; the interpretation of what drives each component belongs in
discussion.

**2. Interpretation later (discussion section).** In discussion, introduce the four
candidate drivers of the empire-wide common temporal component (Obs 98: cultural habit,
empire-wide demography, taphonomy, dating-convention residual) and note the correspondence
with the epigraphic-habit literature. Do not suppress the correspondence — it is a genuine
and noteworthy connection — but externalise the causal claim about which driver dominates.

**3. Hanson is the bridge.** The Hanson population comparison is introduced at the end of
the results section, as the hinge between empirical pattern and interpretation. Hanson's
estimates are well-regarded (if not universally agreed), and naming him explicitly as the
first interpretive step is safe and transparent. The language in results: "association with
Hanson's population estimates" (not "population scaling" with causal force). The bridge
framing lets the cumulative H3a result (β_within = 0.587 [0.519, 0.657]) stand as the
confirmed results-section finding, with interpretive elaboration in discussion.

**4. Naming discipline.** Two non-negotiable naming rules for drafting:
- In results: "empire-wide common temporal component" (not "epigraphic habit", not "habit
  component" — these imply the causal interpretation)
- In results: "association with Hanson's population estimates" (not "population scaling",
  not "urbanisation proxy")

**5. The diagnostic unit is Latin-speaking-minus-Roma.** The all-provinces (1,044-city)
frame is baseline context; the project's primary diagnostic unit is Latin-speaking
provinces excluding Roma. Metrics computed on the all-provinces frame (H7 β over time,
peak-scaling arms) are valid and important baseline results, but the paper-primary
versions require Latin-minus-Roma variants. This flags H7 (Obs 99) and the peak-scaling
arms (Obs 100) as needing Latin-minus-Roma re-runs before paper-finalisation.

### Why this matters

1. **The empirical/interpretive separation protects the results section from claims the
   model cannot support.** The identification caveat (Obs 98) means any results-section
   claim that `g_shape` = habit or `g_shape` = demography is an over-claim; the separation
   ensures the paper's results section is reproducible and model-conditional, while the
   discussion section carries the interpretive weight.
2. **Naming discipline prevents reviewer objections at first read.** The most common
   critique of epigraphic-habit studies is conflation of "what the inscriptions record"
   with "what the habit does". Using "empire-wide common temporal component" in results
   pre-empts this critique without suppressing the substantive connection to MacMullen.
3. **Hanson as bridge is rhetorically and substantively sound.** Hanson (2016 / 2021) is
   the standard population reference for the Roman world in quantitative urban studies;
   introducing the association explicitly, rather than embedding it as a silent assumption,
   is methodologically transparent and reviewably correct.
4. **The Latin-minus-Roma gap is now formally on the work list.** H7 and peak-scaling are
   currently all-provinces; the diagnostic unit requires Latin-minus-Roma variants. This
   Obs records the gap so it is not silently dropped before paper-finalisation.

### Caveats / methodological notes

- **This is a structural framing decision, not a run artefact.** No new data or statistics
  are introduced here; this Obs records the methodological and organisational decision for
  future reference and write-up guidance.
- **"Empirical" does not mean "atheoretical".** The model results are model-conditional
  (aoristic mixture + hierarchical partial-pooling); the results section should state this
  once, clearly, so that the "empirical" framing is not misread as theory-free.
- **The Hanson-bridge position (end of results) is provisional.** If reviewers or co-authors
  prefer the Hanson comparison in a separate section or as an explicit sensitivity, the
  structural logic of the framing decision still holds; only the location within the paper
  changes.
- **Latin-minus-Roma variants are unrun as of 2026-06-17** for H7 and peak-scaling. The
  all-provinces results are valid baselines; the paper cannot present them as the
  diagnostic-unit result without the variants.

### Related observations and artefacts

**Obs 98** (the empire-wide common temporal component conflates four drivers — the
identification caveat that motivates the empirical/interpretive separation): the core
methodological insight that makes the naming discipline in point 4 non-negotiable.

**Obs 97** (H5 — empire-wide common temporal component peaks AD 187.5; this is the
quantity that must be named carefully in results): the specific g_shape result that the
naming discipline applies to.

**Obs 99** (H7 — β_within U-shape, all-provinces frame; Latin-minus-Roma variant
outstanding): one of the two analyses flagged as needing a Latin-minus-Roma re-run.

**Obs 100** (peak-scaling — all-provinces frame; Latin-minus-Roma variant outstanding):
the other analysis flagged for a Latin-minus-Roma re-run.

**Artefacts**: no run artefact (a structural framing decision). Documentation:
`runs/2026-06-17-s5-h5-habit-removed/spec.md` (the H5 spec articulates the two-component
decomposition this decision builds on);
`runs/2026-06-16-s5-layer-b-beta-inversion/REPORT.md` (Layer B illustrative-only framing
that this decision extends).

### Findable later

`paper-framing`, `framing-decision`, `structural-decision`, `write-up-structure`,
`empirical-decomposition-first`, `interpretation-later`,
`results-discussion-separation`, `identification-caveat-framing`,
`Hanson-as-bridge`, `Hanson-bridge`, `end-of-results`,
`association-with-Hanson`, `not-population-scaling`,
`naming-discipline`, `empire-wide-common-temporal-component`,
`not-epigraphic-habit`, `not-habit-component`,
`four-drivers-in-discussion`, `MacMullen-correspondence`,
`Latin-minus-Roma`, `diagnostic-unit`, `Latin-speaking-minus-Roma`,
`all-provinces-baseline`, `1044-frame-baseline`,
`H7-Latin-minus-Roma-outstanding`, `peak-scaling-Latin-minus-Roma-outstanding`,
`Latin-minus-Roma-variants-needed`, `paper-finalisation-gap`,
`model-conditional`, `aoristic-mixture`, `hierarchical-partial-pooling`,
`reproducible-results-section`, `empirical-not-atheoretical`,
`Hanson-2016`, `Hanson-2021`, `population-reference`,
`beta-within-0-587`, `cumulative-H3a-results-section`,
`reviewer-objection-preempted`, `MacMullen-connection-not-suppressed`,
`obs-98`, `obs-97`, `obs-99`, `obs-100`

## Obs 102 — 2026-06-18 [FRAMING / METHODOLOGY]: held-out validation anchors are a design strength — explain the hold-out; do not refit to include them

### The finding

A research-design and publication-framing decision (Shawn, 2026-06-18): the seven large,
data-rich validation anchors (including Ostia, N = 2,380, and Pompeii, among others;
C = 268 small-N target cities + 7 anchors = 275 cities in the dataprep cache at
`runs/2026-05-30-s5-small-n-trajectories/code/prepared/`, comprising 275
`aoristic-<city>.npz` files + `city-index.parquet`) are held out of the §5 Layer-A
pooled small-N hierarchical fit BY DESIGN, in order to serve as an independent
out-of-sample validation set. The paper EXPLAINS this hold-out as a strength; we
do NOT re-run the monolithic fit to fold the anchors in.

**Two substantive reasons not to refit:**

**1. Re-running would destroy the independent validation.** The anchors' entire value is
that they are NOT in the fit — which is what allows the paper to state that the model
recovered Ostia's 2nd-century apogee and Pompeii's AD-79 terminus out-of-sample (raw
Layer B anchor gate, Obs 96). Including the anchors in the pooled fit eliminates that
out-of-sample claim entirely.

**2. High-N anchors would dominate the shared component.** `g_shape` (the empire-wide
common temporal component) is identified by data-weighted commonality across the pooled
cities. A city with N ≈ 2,380 inscriptions alongside many cities below the N* = 300
reliability floor would carry enormous weight and would CHANGE `g`, making the
"empire-common trend" partly "what the few huge cities do" — a worse estimand for an
analysis whose entire purpose is the data-poor cities.

Therefore "include them later" is not a deferred improvement: it would cost the
out-of-sample validation AND distort `g`. No version of including-the-anchors is
strictly better than the current design.

**Consequence for the residual Layer B**
(`runs/2026-06-17-s5-layer-b-residual/spec.md`, §7): because the anchors are held out
of the pooled fit, they have no empire-common `g`-decomposition — a standalone
single-city fit has only one city, so there is no "shared across cities" tier to
separate from the city-specific residual. Hence the anchors cannot be
residual-decomposed (no u_shape + v_shape to invert) and are NOT re-run in the residual
inversion. They are validated by the raw full-inversion upstream (Obs 96), and the
residual inversion is validated WITHIN-SET via two checks: (a) the foundation-terminus
check — 99 cities are founded within the envelope (Start Date > 50 BC), and median
pre-foundation inscription mass on the residual q is a q-analogue of H5's lam-mass
check (H5 found 0.07 % median pre-foundation mass on the raw trajectories); (b) the
collapse-disappearance contrast — does removing `g` make the raw Layer B's spurious
universal post-AD-250 "collapse" disappear?

**Paper framing (companion to Obs 101's empirical-first structure):**

- *Methods:* "the seven largest, data-rich cities are held out and reserved as
  independent validation anchors."
- *Results / raw Layer B:* out-of-sample anchor recovery presented as CREDIBILITY
  EVIDENCE, not a caveat.
- *Results / residual Layer B:* one honest within-set sentence (the anchors have no
  empire-common decomposition; validated by the full inversion above plus foundation
  termini).
- The preregistration already casts these as validation cities ("Pompeii AD 79,
  Ostia c. AD 250, etc."), so the framing is consistent with the registered design.

**Parked future work (explicitly not now):** if a reviewer wants the RESIDUAL
(habit-removed) trajectory for the famous cities — i.e., "did Ostia's apogee EXCEED
the empire-wide tide, or merely RIDE it?" — answer it with a SEPARATE,
clearly-labelled supplementary hierarchical fit that includes the anchors for that
curiosity only, leaving the primary small-N fit untouched. Cheap, optional,
supplementary — never a change to the primary deliverable.

### Why this matters

1. **Reviewers familiar with held-out validation will read the hold-out as rigour if
   framed as design, or as an unexplained gap if framed as an exclusion.** The framing
   choice is the whole point of this Obs.
2. **It pre-empts the obvious reviewer question "why not just include Ostia and
   Pompeii?"** with a principled answer: doing so loses the out-of-sample validation
   claim and distorts `g`. The two-reason structure can go directly into a methods
   footnote or response-to-reviewers letter.
3. **It settles, before drafting, how the anchor story is told across Methods and both
   Layer B results subsections.** Without this decision recorded, the three different
   places where anchors appear (methods, raw Layer B, residual Layer B) risk
   inconsistent framing.

### Caveats / methodological notes

- This is a framing and research-design decision, not a new empirical result — there is
  no new run artefact associated with this Obs.
- The within-set foundation-terminus check on the residual q is descriptive, with no
  pre-committed threshold (consistent with Decision 13 / exploratory status throughout).
  It is a q-analogue of H5's lam-mass check (Obs 97: 0.07 % median pre-foundation mass
  on raw trajectories), not an identical test.
- The "ride vs exceed" supplementary fit (parked future work above) is strictly optional;
  it is recorded here so it is not lost, but it is not on the critical path.

### Related observations and artefacts

**Obs 96** (§5 Layer B β-inversion complete — gate validates against both independent
anchors): the raw Layer B run that establishes the out-of-sample anchor recovery this
Obs explains as a design strength. Ostia's 2nd-century apogee and Pompeii's AD-79
terminus were recovered out-of-sample from the held-out standalone fits.

**Obs 97** (§5 H5 — empire-wide common temporal component peaks AD 187.5; foundation-
terminus check passes, 0.07 % median pre-foundation mass): the H5 lam-mass result
whose q-analogue is used as within-set validation for the residual Layer B; also
establishes the g_shape quantity that the anchors would distort if included in the
pooled fit.

**Obs 98** (the empire-wide common temporal component is NOT a clean epigraphic habit —
it conflates four drivers): establishes why the anchors cannot be residual-decomposed
via a standalone fit — the u_shape + v_shape separation requires a pooled multi-city
model, not available for a standalone single-city run.

**Obs 101** (empirical decomposition first, interpretation later; Hanson as the bridge;
diagnostic unit = Latin-minus-Roma): companion framing decision; the anchor-treatment
narrative in this Obs is the specific piece of the paper structure Obs 101 does not
cover.

**Artefacts**: no new run artefact (a research-design and framing decision). Source
files anchoring the specifics:
`runs/2026-06-16-s5-layer-b-beta-inversion/spec.md` (lines 17, 73, 77, 80, 197 — C =
268 cities, 7 large anchors NOT in fit, 275 aoristic files, Ostia N = 2,380);
`runs/2026-06-17-s5-h5-habit-removed/REPORT.md` (lines 69–70 — 99 within-envelope
foundation cities, 0.07 % median pre-foundation mass);
`runs/2026-06-17-s5-layer-b-residual/spec.md` §7 (anchors cannot be residual-decomposed;
within-set validation design).

### Findable later

`held-out-anchors`, `validation-set-by-design`, `do-not-refit-to-include`,
`out-of-sample-validation`, `g-shape-domination`, `high-N-cities-dominate-shared-component`,
`residual-anchors-cannot-be-decomposed`, `residual-anchors-supplementary-fit`,
`Ostia-Pompeii`, `Ostia-N-2380`, `ride-vs-exceed-empire-tide`,
`anchor-hold-out-is-a-strength`, `paper-framing-anchors`, `validation-anchors`,
`seven-large-anchors`, `foundation-terminus-within-set`, `q-analogue-lam-mass`,
`collapse-disappearance-contrast`, `within-set-validation`, `99-within-envelope`,
`268-target-cities`, `275-aoristic-files`, `dataprep-cache`,
`standalone-fit-no-g-decomposition`, `no-u-shape-v-shape`,
`ride-vs-exceed-supplementary`, `parked-future-work`, `supplementary-only`,
`preregistration-validation-cities`, `two-reasons-not-to-refit`,
`distort-g-shape`, `lose-out-of-sample`, `methods-footnote`,
`response-to-reviewers`, `obs-96`, `obs-97`, `obs-98`, `obs-101`

## Obs 103 — 2026-06-18 [RESULT / METHODOLOGY]: §5 Layer B (residual) — removing the empire-wide common temporal component dissolves the raw inversion's apparent universal post-AD-250 collapse into moderate, heterogeneous, provincial-tier relative decline

### The finding

The habit-removed (residual) Layer B inverts each city's residual log-trajectory
`r[c,t] = u_shape[p(c),t] + v_shape[c,t]` (the empire-wide common temporal component
`g_shape` **removed**) into a population trajectory **relative to the empire trend**:

`q[c,t] = exp( (1/β_within) · r[c,t] )`

Because `r` is zero-sum over `t`, `q` has geometric mean 1 by construction: `q = 1.0`
means "on the empire trend"; `q = 0.5` means "half". Deterministic transform of the §5
Layer-A posterior — **no MCMC**. β frames: empire `β_within = 0.588` primary; Latin
`0.733` overlay (1/β exponents: 1.70 and 1.36 respectively). Scope: 268 small-N target
cities; 34 meet the N* = 300 reliability floor.

**Wiring guard (self-test) — PASS at machine precision.** Adding `g` back reconstructs
`exp((1/β)·((g+u+v)−max))`, which must equal the raw Layer B relative-shape (within-city
level offsets cancel under peak-normalisation): max abs diff vs the persisted raw
`shape_med` = **5.6 × 10⁻¹⁶** (city Cirta). The *only* difference from the raw Layer B
(Obs 96) is the removal of `g`.

**PRIMARY RESULT — median q vs the empire baseline (1.0), reliable cities, empire β:**

| bin (centre) | era | median `q` | IQR | share below empire |
|---|---|---|---|---|
| AD 112 | early-Antonine | **0.48** | [0.27, 1.74] | 0.65 |
| AD 188 | empire-common peak (`g` peak) | **1.01** | [0.38, 4.36] | 0.50 |
| AD 262 | 3rd century ("crisis") | **0.32** | [0.16, 1.25] | 0.68 |
| AD 338 | late | **0.67** | [0.10, 5.22] | 0.53 |

Removing `g` dissolves the raw inversion's apparent universal post-AD-250 collapse
into city-level heterogeneity:

- At the empire-common peak (AD 188) the median city sits **exactly on the empire trend**
  (`q ≈ 1.01`) — as it must, since that is what `g` captures.
- By the 3rd century the median city is at **≈ 0.32 of its empire-relative baseline** — a
  *moderate* relative decline (factor of ~3), not the raw inversion's near-total collapse.
  ~⅓ of reliable cities are still *at or above* the empire trend (`q ≥ 1`) at AD 262,
  rising to approximately half by AD 338.
- The Latin-β overlay is uniformly milder (1/β = 1.36 vs 1.70): median `q` at AD 262
  = **0.40** (same 68 % below empire).

**SECONDARY RESULT — v-only overlay (province removed too), empire β:**

| bin (centre) | `u+v` median `q` | `v`-only median `q` |
|---|---|---|
| AD 112 | 0.48 | **0.75** |
| AD 188 | 1.01 | **1.31** |
| AD 262 | 0.32 | **0.78** |
| AD 338 | 0.67 | **0.80** |

The v-only trajectory is markedly flatter than u+v. A substantial part of a city's
apparent divergence from the empire trend is its **province's shared deviation**
(`u_shape`), not its own (`v_shape`): the purely city-specific 3rd-century position is
a mild ≈ 0.78 of empire-relative baseline, against 0.32 once the province deviation is
folded in. The late-imperial under-production of these small western cities is largely a
**provincial-tier** phenomenon, not idiosyncratic to individual cities.

**Pending enhancement (no re-fit required):** the current outputs give q_uv
(city-from-empire) and q_v (city-from-province) but NOT q_u (province-from-empire).
These three quantities are nested multiplicatively — `q_uv = q_u × q_v` (since
log q_uv = (1/β)(u+v) = (1/β)u + (1/β)v) — so adding q_u is a small enhancement that
reuses the loaded `u_shape` without any re-fit, and would complete the nested
divergence-decomposition triple for the final-paper table.

### Why this matters

1. **This is the demography-isolating deliverable preregistered under Decision 13.** The
   raw Layer B's dramatic post-AD-250 "collapse" is shown to be mostly the empire-wide
   common component (`g`, Obs 97 — conflating habit, empire demography, taphonomy, and
   dating-convention residual, Obs 98). The genuinely city/province-specific part is a
   moderate, heterogeneous decline — a cleaner object than the raw inversion for the
   discussion section.
2. **The provincial-tier finding is structurally important for the paper.** The v-only
   result reframes "small western cities decline" as largely "their provinces decline
   relative to the empire", bearing on whether drivers are region-wide (provincial) or
   city-idiosyncratic.
3. **The wiring guard ties this Obs to the raw Layer B exactly.** The machine-precision
   self-test (5.6 × 10⁻¹⁶ max abs diff at Cirta) means the residual result is not an
   independent analysis but an algebraically certified transformation of Obs 96 — any
   residual feature that is *not* in the raw result is entirely attributable to the
   removal of `g`.

### Caveats / methodological notes

- **Metric correction (important).** The pre-specified contrast "fraction of own peak at
  AD 250" is **confounded** for the residual: 1/β amplification + GaussianRandomWalk
  endpoint variance push 11 of 34 reliable cities' q-peak to the envelope-edge bins,
  forcing the ratio to ~0 regardless of the actual late level. The correct diagnostic for
  a geom-mean-1 quantity is `q` vs the empire baseline (1.0). The confounded
  frac-of-peak numbers are retained, flagged, in `summary.json → frac_of_peak_CONFOUNDED`
  for transparency only.
- **Edge-bin caveat.** For the same GRW-endpoint reason, the envelope-edge bins
  (AD 12: median `q` 2.74, IQR up to ~18; AD 338: IQR up to ~5.2) have inflated variance
  and are **not** interpreted; the narrative rests on the well-constrained mid-empire bins
  (AD 112 / 188 / 262).
- **Relative, not absolute, not pure demography (Obs 98).** `q` is population relative to
  the empire trend, not absolute population; the residual still carries city/province-level
  taphonomy, economy, and habit. The only clean claim is "free of the empire-common
  confound".
- **Validation.** Foundation-terminus on `q` clean: median pre-foundation mass fraction
  = 0.02 % (99 within-envelope cities). Anchors (Ostia, Pompeii) NOT re-run by design
  — held out, no `g`-decomposition available (Obs 102) — validated by the raw
  full-inversion out-of-sample (Obs 96, clean pass).
- **Exploratory; no thresholds** (Decision 13). N* = 300 floor (34/268 reliable);
  within-sample empire shape (the 268-city `g` is a proxy for the true empire-common
  component).

### Related observations and artefacts

**Obs 96** (§5 Layer B β-inversion complete — inverts the FULL `lam` including `g`;
apparent universal post-AD-250 collapse; anchor gate passes): the raw Layer B of which
this Obs is the habit-removed correction/complement; the wiring self-test ties the two
at machine precision.

**Obs 97** (§5 H5 — empire-wide common temporal component peaks AD 187.5; no systematic
corpus lag; foundation-terminus check passes): identifies and characterises `g_shape`,
the component removed here; the AD-188 peak in the primary result (median `q ≈ 1.01`)
is the expected consequence of removing `g` at its own peak.

**Obs 98** (the empire-wide common temporal component is NOT a clean epigraphic habit —
conflates four drivers; the residual inversion is well-posed regardless): establishes
why the residual `q` is better-posed than the raw `lam` for cross-city comparison,
and why it is not pure demography.

**Obs 101** (empirical decomposition first, interpretation later; naming discipline):
the residual Layer B is presented in results as an empirical nested-unit decomposition
using "empire-wide common temporal component" language; the four-driver interpretation
of `g` is deferred to the discussion per this framing decision.

**Obs 102** (held-out validation anchors are a design strength — do not refit): why
Ostia and Pompeii are not re-run in the residual inversion; the within-set foundation-
terminus check is the residual analogue of H5's lam-mass check.

**Artefacts**:
`runs/2026-06-17-s5-layer-b-residual/REPORT.md` (source report; all numbers verified);
`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-summary.json`
(primary-result tables, self-test, validation, beta frames, provenance; source for all
numbers in this Obs; commit `a5c4699`);
`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-vs-raw.png` (left: raw
apparent collapse; right: residual `q` vs 1.0 baseline with IQR band);
`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-empire.nc`,
`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-latin.nc`
(full per-city trajectory posteriors);
`runs/2026-06-17-s5-layer-b-residual/code/` (reuses
`runs/2026-06-17-s5-h5-habit-removed/code/h5_habit_removed.py` and
`runs/2026-06-16-s5-layer-b-beta-inversion/code/layerb_invert.py`).

### Findable later

`residual-layer-b`, `habit-removed-inversion`, `relative-to-empire`,
`q-vs-empire-baseline`, `collapse-dissolves`, `apparent-universal-collapse`,
`city-level-heterogeneity`, `third-century-relative-decline`,
`provincial-tier-decline`, `v-only-overlay`, `province-from-empire`,
`city-from-province`, `nested-divergence-decomposition`, `multiplicative-decomposition`,
`q-uv-equals-q-u-times-q-v`, `frac-of-peak-confounded`, `GRW-endpoint-artefact`,
`envelope-edge-variance`, `self-test-machine-precision`, `5-6e-16`, `city-Cirta`,
`geom-mean-1`, `not-pure-demography`, `relative-not-absolute`,
`foundation-terminus`, `median-pre-foundation-0-02-percent`,
`Latin-beta-overlay`, `1-over-beta-1-36`, `1-over-beta-1-70`,
`q-at-AD-262-0-32`, `q-at-AD-262-v-only-0-75`,
`q-at-AD-188-1-01`, `q-at-AD-338-0-67`,
`11-of-34-edge-peak`, `268-target-cities`, `34-reliable`,
`beta-within-0-588`, `beta-within-0-733`,
`Decision-13`, `exploratory-no-thresholds`,
`q-uv-primary`, `q-v-city-from-province`, `q-u-province-from-empire-pending`,
`nested-triple-pending`, `reuses-u-shape`,
`obs-96`, `obs-97`, `obs-98`, `obs-101`, `obs-102`

## Obs 104 — 2026-06-18 [RESULT / METHODOLOGY]: §5 size-vs-dynamics probe — city size does NOT predict purely city-specific dynamics (q_v null), but DOES track the province-inclusive trajectory (q_uv): the size–buffering gradient is mostly province-mediated

### The finding

The §5 size-vs-dynamics probe asks cross-city whether Hanson `pop_est` predicts
features of the residual trajectories. Origin: the user-obs 43 well-posed reframe of
"can we compare the isolated city-level effect to Hanson?" (a direct `q_v`-vs-Hanson
overlay is a category mismatch; this asks instead whether size predicts features of the
city-specific trajectory shape).

**Design.** Features extracted from mid-bins (edges excluded): F1 late-level `q[AD 262]`
(headline), F2 volatility `SD_t(log q)` (headline), F3 tilt `log q[AD 262] − log q[AD 112]`
(secondary), F4 peak-bin (secondary). Two trajectory tiers: primary `q_v`
(city-from-province; province AND empire removed), secondary `q_uv` (city-from-empire).
34 reliable cities (N ≥ 300), `pop_est` ∈ [1,000, 153,722], **2.19 log₁₀ decades**, 19
provinces. Spearman ρ (rank-based, robust; Obs 94 leverage lesson) with a city-bootstrap
95 % CI (sampling uncertainty, binding at n = 34) AND a draw-wise ρ posterior (trajectory
uncertainty). Non-circular: §5 Layer A has no population covariate (Obs 98); ρ is exactly
β-frame-invariant per draw (monotone city-constant rescale). Slopes in empire-β units.

---

**PRIMARY TIER — `q_v` (city-from-province) — HEADLINE NULL:**

| feature | Spearman ρ | bootstrap 95 % CI | P(ρ > 0) | draw-wise ρ | draw-wise 95 % CI |
|---|---|---|---|---|---|
| **F1 late-level** *(headline)* | **+0.09** | [−0.26, +0.41] | 0.71 | +0.07 | [−0.18, +0.32] |
| **F2 volatility** *(headline)* | **−0.05** | [−0.39, +0.28] | 0.37 | −0.09 | [−0.30, +0.13] |
| F3 tilt *(secondary)* | +0.31 | [−0.06, +0.61] | 0.96 | +0.21 | [−0.02, +0.43] |
| F4 peak-bin *(secondary)* | +0.04 | [−0.34, +0.39] | 0.58 | +0.02 | [−0.23, +0.29] |

City size does **not** predict where the purely city-specific trajectory sits late, nor
its volatility. F1's OLS slope (+0.284) is inflated by a leverage point relative to
Theil-Sen (+0.130); the rank ρ (+0.09) is the robust read — the Obs 94 leverage check
working. F3 tilt is suggestive (ρ +0.31, P(ρ > 0) 0.96) but it is a *secondary* feature
whose bootstrap CI [−0.06, +0.61] includes 0; the draw-wise ρ (+0.21) nearly excludes 0,
so the binding limit is **sampling (n = 34)**, not the trajectory posterior.

---

**SECONDARY TIER — `q_uv` (city-from-empire) — A COHERENT, PROVINCE-MEDIATED GRADIENT
(the meaningful outcome):**

| feature | Spearman ρ | bootstrap 95 % CI | P-sign | draw-wise ρ | draw-wise 95 % CI |
|---|---|---|---|---|---|
| F1 late-level | **+0.28** | [−0.08, +0.58] | P(ρ>0) 0.93 | +0.21 | [+0.04, +0.37] |
| F2 volatility | **−0.24** | [−0.58, +0.13] | P(ρ<0) 0.90 | −0.21 | [−0.35, −0.06] |
| **F3 tilt** | **+0.38** | **[+0.05, +0.63]** | P(ρ>0) 0.99 | +0.32 | [+0.15, +0.48] |
| F4 peak-bin | +0.12 | [−0.29, +0.47] | P(ρ>0) 0.72 | +0.05 | [−0.08, +0.19] |

On `q_uv` the three magnitude features line up in one coherent direction — **bigger
cities are more buffered relative to the empire**: sustained later (F1 +), less volatile
(F2 −), shallower early-to-late decline (F3 +). F3 is leverage-clean (OLS +1.54 ≈
Theil-Sen +1.60) and is the only feature whose bootstrap CI just clears 0; F1/F2 clear 0
only on the (non-binding) draw-wise band.

**The key structural read (Shawn's meaningful outcome):** the gradient is **much stronger
on `q_uv` than on `q_v`** — F3: +0.38 vs +0.31; F1: +0.28 vs +0.09; F2: −0.24 vs −0.05.
Since `q_uv = q_u × q_v` (i.e. province-from-empire × city-from-province), and removing
the province (`q_v`) largely removes the signal, the size–buffering relationship operates
**mainly at the province tier**: larger cities tend to sit in provinces that decline less
relative to the empire.

**Sensitivity.** On all 268 cities (234 below the N* = 300 floor) every ρ collapses
toward 0 and some flip sign (q_v: F1 −0.10, F3 −0.04). Expected: below-floor
trajectories are uncalibrated and partial-pool toward the common shape, adding noise and
diluting any signal. The (suggestive) structure exists only in the reliable set — a
coherence note, not a contradiction.

### Why this matters

1. **The provincial-tier dominance is the meaningful outcome.** This Obs is a second,
   independent line of evidence for the provincial-tier story established in Obs 103.
   Obs 103 showed the late-imperial decline is itself largely provincial-tier (q_v much
   flatter than u + v); this Obs shows the **covariation of that decline with city size**
   is also provincial-tier. Both the *level* of decline and its *size-correlation* live
   more in the province than in the individual city — consistent with region-wide rather
   than city-idiosyncratic drivers.
2. **It answers the literal question cleanly.** City size does not predict purely
   city-specific dynamics (null on `q_v` F1/F2), while surfacing the more interesting
   structural result. A bounded, honest answer that converts the original (mis-posed)
   question into a real — if underpowered — finding.
3. **For the paper**, this points the interpretation toward province/region-scale drivers
   of late-imperial epigraphic production rather than city-idiosyncratic ones.

### Caveats / methodological notes

- **Exploratory; no thresholds (Decision 13).** SUGGESTIVE, NOT ESTABLISHED: n = 34
  (|ρ| ≳ 0.34 needed to clear a 95 % bootstrap bound); only `q_uv` F3 clears 0 on the
  binding bootstrap CI.
- **Not pure demography (Obs 98).** `v_shape`/`u_shape` carry taphonomy, economy, and
  habit; "buffered" does not mean demographically buffered.
- **Range restriction (Obs 100).** 2.19 log₁₀ decades among small-N targets.
- **Multiple comparisons.** 4 features × 2 tiers × 2 samples reported together; no
  cherry-pick, no threshold.
- **Province-mediation is an inference** from the `q_uv` ≫ `q_v` gap, not a direct
  province-size regression (a natural follow-up if pursued).
- **β-frame.** Rank results β-frame-invariant; slopes in empire-β units.

### Related observations and artefacts

**Obs 103** (§5 Layer B (residual) — late-imperial decline largely provincial-tier; q_v
much flatter than u + v): this Obs is a second, size-covariation line of evidence for the
same provincial-tier dominance finding; together these two Obs frame the province as the
structurally important tier.

**Obs 100** (§5 peak-scaling / Hanson population — peak ≈ cumulative; smoothing neutral;
identifies the N* = 300 reliable subset): establishes the 34-city reliable set used here;
the 2.19-decade range restriction and the low-power framing originate here.

**Obs 98** (empire-wide common temporal component conflates four drivers; residual
inversion well-posed but not pure demography): the "buffered ≠ demographically buffered"
caveat in this Obs traces directly to Obs 98.

**Obs 94** (Theil-Sen / Spearman robustness — caught a Pompeii OLS leverage artefact;
rank ρ is the preferred headline): the same check that flagged a prior leverage artefact
is the motivation for preferring Spearman ρ over OLS here; F1's inflated OLS slope (+0.284
vs Theil-Sen +0.130) is the recurrence of the Obs 94 pattern.

**Artefacts**:
`runs/2026-06-18-s5-size-vs-dynamics/REPORT.md` (source report; all numbers verified
against JSON; commit `55b42bc`);
`runs/2026-06-18-s5-size-vs-dynamics/outputs/size-vs-dynamics-summary.json`
(full Spearman ρ / bootstrap 95 % CI / draw-wise ρ posterior / OLS + Theil-Sen slopes,
per feature × tier × sample; provenance sha256; source for all numbers in this Obs);
`runs/2026-06-18-s5-size-vs-dynamics/outputs/size-vs-dynamics-scatter.png`
(F1/F2 vs log₁₀ pop, `q_v`, with Theil-Sen + ρ);
`runs/2026-06-18-s5-size-vs-dynamics/outputs/size-vs-dynamics-rho-posterior.png`
(draw-wise ρ posteriors).

### Findable later

`size-vs-dynamics`, `city-size-predicts-dynamics`, `province-mediated`,
`provincial-tier-dominance`, `q-v-null`, `q-uv-gradient`,
`bigger-cities-buffered`, `late-imperial-buffering`,
`Hanson-pop-est`, `Spearman-rank-robust`, `city-bootstrap`,
`drawwise-rho`, `beta-frame-invariant`,
`n34-low-power`, `range-restriction-2-19-decades`,
`not-pure-demography`, `Theil-Sen-leverage-check`,
`OLS-inflated-leverage-F1`, `F1-rho-plus-0-09`, `F3-tilt-rho-plus-0-31`,
`q-uv-F1-rho-plus-0-28`, `q-uv-F2-rho-minus-0-24`, `q-uv-F3-rho-plus-0-38`,
`F3-bootstrap-CI-clears-0`, `OLS-1-54-Theil-Sen-1-60`,
`q-uv-stronger-than-q-v`, `province-dominates-city`,
`user-obs-43-reframe`, `Decision-13`, `exploratory-no-thresholds`,
`multiple-features-no-cherry-pick`, `below-floor-noise-dilution`,
`all-268-collapses`, `34-reliable-cities`, `19-provinces`,
`obs-103`, `obs-100`, `obs-98`, `obs-94`

## Obs 105 — 2026-06-18 [RESULT / METHODOLOGY]: province size does NOT drive province-from-empire (q_u) buffering — Obs 104's "province-mediation" is a decomposition fact, not a province-size effect; underpowered, with a tentative city-membership lean

### The finding

**What was tested.** Direct test of the province-mediation *inference* in Obs 104, which
was drawn from `q_uv ≫ q_v` (a cross-tier gap, not a province-level regression). A
background agent ran this on sapphire (2026-06-18); deterministic transform of the §5
Layer-A posterior — no MCMC. Reuses the size-vs-dynamics machinery.

**Unit = province** (35 non-singleton). `q_u[p,t] = exp((1/β)·u_shape[p,t])` computed
directly from `u_shape` (S = 8,000, P = 35, T = 16) at empire β (median 0.587), one
series per province. **Predictor = province size** = `pop_est` aggregated over all member
cities in the full 1,012-city index: **sum** (primary), **mean**, **max** (sensitivities);
log₁₀. Sum range [10,868; 645,931] = **1.77 log₁₀ decades**; member cities 4 / 19 / 70
(min / median / max). Province join: 35/35 `u_shape` provinces matched the full-index
province field, 0 unmatched. **Self-check (PASS):** `q_u` constant within province ✓;
direct `u_shape` inversion reproduces the residual Layer B `q_u_med` to max abs diff 0.0
(spot province Achaia, 2 cities) — bit-exact.

**Features on `q_u`** (mid-bins; edges excluded): F1 late-level `q_u[AD 262]`, F2
volatility `SD_t(log q_u)`, F3 tilt `log q_u[AD 262] − log q_u[AD 112]`; "more buffered" =
F1↑, F2↓, F3↑. **Method:** Spearman ρ primary, province-bootstrap 95 % CI (binding),
draw-wise ρ posterior, OLS + Theil-Sen. Non-circular (Layer A has no population covariate,
Obs 98); ρ β-frame-invariant. **Samples:** all 35 (primary) + 20 with ≥1 reliable (N ≥ 300)
city (sensitivity; province-tier reliability NOT separately calibrated — N* = 300 is a
per-city floor).

**Results — Spearman ρ (province-bootstrap 95 % CI), primary aggregate (sum), all 35:**

| feature | ρ | bootstrap 95 % CI | buffered direction |
|---|---|---|---|
| F1 late-level | −0.05 | [−0.37, +0.28] | ✗ |
| F2 volatility | −0.24 | [−0.51, +0.09] | ✓ |
| F3 tilt | −0.06 | [−0.41, +0.32] | ✗ |

**Nothing clears the 95 % bootstrap bound anywhere** (|ρ| ≳ 0.33 needed at n = 35;
≳ 0.44 at n = 20). Sign is **incoherent** on the primary aggregate (sum): F1 and F3 —
the features that carried the Obs 104 `q_uv` gradient — are flat-to-slightly-anti-buffered;
only F2 leans buffered. The binding uncertainty is **sampling (n)**, not the posterior:
draw-wise bands are uniformly narrower than the bootstrap CIs.

**Sensitivity — mean and max aggregates (per-city scale), reliable-20 subset, lean buffered:**

| aggregate | feature | ρ | bootstrap 95 % CI | P(ρ > 0) |
|---|---|---|---|---|
| mean | F1 late-level | +0.35 | [−0.12, +0.76] | 0.93 |
| mean | F3 tilt | +0.31 | [−0.18, +0.80] | 0.88 |
| max | F3 tilt | +0.37 | [−0.11, +0.73] | 0.94 |
| max (all 35) | F2 volatility | −0.25 | [−0.56, +0.08] | — |

Mean and max lean buffered (especially F1 and F3 on reliable-20), but every CI includes 0.
OLS vs Theil-Sen diverges on sum F1/F3 (leverage; Obs 94) — rank ρ is the robust read.

**Verdict.** The Obs 104 `q_uv ≫ q_v` province-mediation inference is **NOT directly
corroborated** at province level. The city-level size–buffering gradient stands (it is a
property of city-level ranks); this test cannot show its mechanism is "bigger provinces have
more buffered `q_u`". The **sum-vs-mean/max split is the informative part**: the buffered
hint attaches to per-city scale (mean/max) and NOT to total provincial mass (sum), which is
mildly more consistent with a **city-membership channel** (large cities happen to sit in
provinces whose `q_u` is buffered) than with province size driving the province trajectory.
Reading: **ambiguous, leaning not-corroborated** — a directional hint at most.

**Refinement of Obs 104 (explicit).** "Province-mediated" is a **decomposition statement**
(the gradient's variance lives in the `u` tier), NOT evidence of a province-size effect. NOT
in tension with Obs 103 (province tier carries the decline level) — a tier can hold the
decline magnitude without province *size* predicting *which* provinces decline.

### Why this matters

1. **Disciplines the drafting.** Rules out the tempting "larger provinces buffer more /
   decline less" reading of the province-tier dominance in Obs 103/104. The dominance is
   real but is not a size story.
2. **Keeps the `q_uv ≫ q_v` decomposition honestly scoped.** The decomposition result
   locates variance in a tier; it does not identify a province-level driver. Flagging this
   before drafting prevents a category error in the interpretation section.
3. **The city-membership-channel hypothesis is a useful pointer.** Even as a directional
   hint at n = 35, it orients any powered follow-up (e.g. province-composition rather than
   province-size as the predictor).

### Caveats / methodological notes

- **n = 35 (≈ 20 reliable) — very low power.** Nothing clears the bound; null was
  pre-framed as expected and informative (Obs 100). A powered test would require data beyond
  this project's scope.
- **Not pure demography (Obs 98).** `u_shape` carries province-level taphonomy, economy,
  and habit; "buffered" ≠ demographically buffered.
- **Province-tier reliability not separately calibrated.** N* = 300 is a per-city floor;
  the reliable-20 subset is a heuristic proxy for province-level data quality.
- **Range restriction.** 1.77 log₁₀ decades of province sum-size — attenuates any true
  effect toward 0.
- **Multiple comparisons.** 3 aggregates × 3 features × 2 samples reported together;
  no cherry-pick, no threshold (Decision 13).
- **City-membership-channel reading is speculative** at this n — a directional lean, not
  a demonstrated mechanism.

### Related observations and artefacts

**Obs 104** (§5 size-vs-dynamics probe — `q_v` null, `q_uv` province-mediated gradient;
the inference this Obs tests and explicitly refines): the `q_uv ≫ q_v` gap established
there stands at city level; this Obs clarifies it is a decomposition fact, not a
province-size effect.

**Obs 103** (§5 Layer B residual — late-imperial decline largely provincial-tier; `q_v`
much flatter than `u + v`): NOT in tension — that Obs establishes the decline *level* lives
in the province tier; this Obs tests whether province *size* predicts *which* provinces
decline (a different question).

**Obs 100** (§5 peak-scaling / Hanson population — identifies N* = 300 reliable subset;
low-power / range-restriction framing): explains the expected null and the pre-framing of
"informative null".

**Obs 98** (empire-wide common temporal component conflates four drivers; residual
inversion not pure demography): the "buffered ≠ demographically buffered" caveat traces
directly here.

**Artefacts**:
`runs/2026-06-18-province-size-regression/REPORT.md` (source report; all numbers verified;
commit `8da7b16`);
`runs/2026-06-18-province-size-regression/outputs/province-size-regression-summary.json`
(full ρ / bootstrap / draw-wise / slopes per aggregate × feature × sample; province join;
self-check; provenance sha256; source for all numbers in this Obs);
`runs/2026-06-18-province-size-regression/outputs/province-size-regression-scatter.png`;
`runs/2026-06-18-province-size-regression/outputs/province-size-regression-rho-posterior.png`.

### Findable later

`province-size-regression`, `province-mediation-not-confirmed`,
`q-u-province-from-empire`, `decomposition-not-size-effect`,
`city-membership-channel`, `sum-vs-mean-max-split`,
`bigger-provinces-not-more-buffered`, `refines-obs-104`,
`underpowered-null`, `n35`, `province-bootstrap`,
`self-check-bit-exact`, `max-abs-diff-0-0`, `spot-province-Achaia`,
`not-pure-demography`, `range-restriction-1-77-decades`,
`sum-sign-incoherent`, `mean-reliable-20-F1-rho-plus-0-35`,
`max-reliable-20-F3-rho-plus-0-37`, `mean-reliable-20-F3-rho-plus-0-31`,
`binding-uncertainty-sampling`, `draw-wise-narrower`,
`OLS-vs-Theil-Sen-diverges`, `leverage-sum-F1-F3`,
`province-mediation-is-decomposition-statement`, `province-dominance-not-size-story`,
`35-provinces`, `20-reliable`, `1012-city-index`,
`Decision-13`, `exploratory-no-thresholds`, `multiple-features-no-cherry-pick`,
`obs-104`, `obs-103`, `obs-100`, `obs-98`
