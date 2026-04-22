# Inscriptions SPA — verified bibliography

**Date:** 2026-04-22
**Source:** `lit-scout` proposer + `lit-scout-verifier` (serial proposer-verifier pattern per `notes/lit-scout-case-study.md`).
**Verification:** 25 / 25 rows passed adversarial re-query against CrossRef + OpenAlex metadata. 0 corrections applied. Verifier specifically re-checked author orderings on 8-author rows (#11, #12), Czech diacritics on SDAM rows (#6, #7, #8, #23, #25), and non-CrossRef registries (Zenodo #23, arXiv #25) — all pass.
**BibTeX file:** `planning/inscriptions-spa.bib` (generated from this DOI set via CrossRef content negotiation).

---

## TL;DR

A robust SDAM/Aarhus–West Bohemia cluster exists around Kaše / Heřmánková / Sobotková — four directly relevant papers plus the LIST Zenodo dataset — and Crema's 2025 *baorista* paper (10.1111/arcm.12984) is the methodologically crucial recent development: it develops Bayesian alternatives to aoristic analysis for exactly the kind of phase-dated, non-radiocarbon data inscriptions represent.

**Top-3 must-reads**: Crema & Bevan (2021) 10.1017/rdc.2020.95 for the rcarbon toolchain; Crema (2025) 10.1111/arcm.12984 for the method most directly applicable to epigraphic chronology; Heřmánková, Kaše & Sobotková (2021) 10.1515/jdh-2021-1004 for the benchmark precedent in digital epigraphy at macro-scale.

**Biggest gap**: no paper yet applies Crema/Bevan permutation-envelope machinery to epigraphic datasets. A LIST × rcarbon-style SPA is genuinely novel — the paper's originality claim is clean.

---

## Findings table (verified)

| # | Fit | Cites | Authors (Year) | Title | DOI | Chain | Cluster | Status |
|---|-----|-------|----------------|-------|-----|-------|---------|--------|
| 1 | HIGH | 6 | Hanson, J. W. (2021) | Cities, Information, and the Epigraphic Habit: Re-evaluating the Links between the Numbers of Inscriptions and the Sizes of Sites | 10.1484/j.jua.5.126597 | seed | Roman epigraphic habit, quantitative | NEW |
| 2 | HIGH | 77 | Hanson, J. W. (2016) | An Urban Geography of the Roman World, 100 BC to AD 300 | 10.2307/j.ctv17db2z4 | seed | Roman urban demography | NEW |
| 3 | HIGH | 405 | Williams, Alan N. (2012) | The use of summed radiocarbon probability distributions in archaeology: a review of methods | 10.1016/j.jas.2011.07.014 | seed | SPD methodology review | NEW |
| 4 | HIGH | 244 | Crema, Enrico R.; Bevan, Andrew (2021) | Inference from Large Sets of Radiocarbon Dates: Software and Methods | 10.1017/rdc.2020.95 | seed | rcarbon/SPD permutation machinery | NEW |
| 5 | HIGH | 84 | Crema, E. R. (2022) | Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed | 10.1007/s10816-022-09559-5 | seed | SPD methodology review | NEW |
| 6 | HIGH | 9 | Heřmánková, Petra; Kaše, Vojtěch; Sobotková, Adéla (2021) | Inscriptions as data: digital epigraphy in macro-historical perspective | 10.1515/jdh-2021-1004 | seed | SDAM epigraphic methodology | NEW |
| 7 | HIGH | 9 | Kaše, Vojtěch; Heřmánková, Petra; Sobotková, Adéla (2022) | Division of labor, specialization and diversity in the ancient Roman cities: A quantitative approach to Latin epigraphy | 10.1371/journal.pone.0269869 | refs-of #6 | SDAM epigraphic methodology | NEW |
| 8 | HIGH | 1 | Glomb, Tomáš; Kaše, Vojtěch; Heřmánková, Petra (2022) | Popularity of the cult of Asclepius in the times of the Antonine Plague: Temporal modeling of epigraphic evidence | 10.1016/j.jasrep.2022.103466 | seed | SDAM temporal modelling of inscriptions | NEW |
| 9 | HIGH | 7 | Crema, Enrico R. (2025) | A Bayesian alternative for aoristic analyses in archaeology | 10.1111/arcm.12984 | cited-by #5 | Aoristic/Bayesian methodology | NEW |
| 10 | HIGH | 98 | Crema, Enrico R. (2012) | Modelling Temporal Uncertainty in Archaeological Analysis | 10.1007/s10816-011-9122-3 | refs-of #9 | Aoristic/Bayesian methodology | NEW |
| 11 | HIGH | 562 | Shennan et al. (2013) | Regional population collapse followed initial agriculture booms in mid-Holocene Europe | 10.1038/ncomms3486 | refs-of #4 | SPD permutation applications | NEW |
| 12 | HIGH | 302 | Timpson et al. (2014) | Reconstructing regional population fluctuations in the European Neolithic using radiocarbon dates: a new case-study using an improved method | 10.1016/j.jas.2014.08.011 | refs-of #4 | SPD permutation machinery | NEW |
| 13 | MEDIUM | 59 | Hanson, J. W.; Ortman, S. G. (2017) | A systematic method for estimating the populations of Greek and Roman settlements | 10.1017/s1047759400074134 | cited-by #1 | Roman urban demography | NEW |
| 14 | MEDIUM | 36 | Hanson, J. W.; Ortman, S. G.; Lobo, J. (2017) | Urbanism and the division of labour in the Roman Empire | 10.1098/rsif.2017.0367 | cited-by #1 | Roman urban scaling / inscriptions as proxy | NEW |
| 15 | HIGH | 116 | Palmisano, A.; Bevan, A.; Shennan, S. (2017) | Comparing archaeological proxies for long-term population patterns: An example from central Italy | 10.1016/j.jas.2017.10.001 | refs-of #4 | Multi-proxy demography (incl. Italy) | NEW |
| 16 | MEDIUM | 34 | Palmisano et al. (2021) | Long-Term Demographic Trends in Prehistoric Italy: Climate Impacts and Regionalised Socio-Ecological Trajectories | 10.1007/s10963-021-09159-3 | refs-of #5 | SPD applications, Italy | NEW |
| 17 | MEDIUM | 18 | Palmisano, A.; Bevan, A.; Shennan, S. (2018) | Regional Demographic Trends and Settlement Patterns in Central Italy: Archaeological Sites and Radiocarbon Dates | 10.5334/joad.43 | refs-of #15 | Open archaeological data | NEW |
| 18 | MEDIUM | 211 | Bevan et al. (2017) | Holocene fluctuations in human population demonstrate repeated links to food production and climate | 10.1073/pnas.1709190114 | refs-of #4 | SPD applications | NEW |
| 19 | HIGH | 163 | Ratcliffe, Jerry H. (2002) | Aoristic Signatures and the Spatio-Temporal Analysis of High Volume Crime Patterns | 10.1023/a:1013240828824 | refs-of #10 | Aoristic method origin | NEW |
| 20 | MEDIUM | 92 | MacMullen, Ramsay (1982) | The Epigraphic Habit in the Roman Empire | 10.2307/294470 | refs-of #6 | Epigraphic habit foundations | NEW |
| 21 | MEDIUM | 49 | Woolf, Greg (1996) | Monumental Writing and the Expansion of Roman Society in the Early Empire | 10.2307/300421 | refs-of #6 | Epigraphic habit foundations | NEW |
| 22 | MEDIUM | 47 | Meyer, Elizabeth A. (1990) | Explaining the Epigraphic Habit in the Roman Empire: The Evidence of Epitaphs | 10.2307/300281 | refs-of #6 | Epigraphic habit foundations | **[IN ZOTERO] — duplicated (SIUN4WXI, WNBSMYDZ); merge candidate** |
| 23 | HIGH | 1 | Kaše, V.; Heřmánková, P.; Sobotková, A. (2024) | LIST (Latin Inscriptions in Space and Time) dataset | 10.5281/zenodo.10473706 | dataset-for #6 | Epigraphic dataset | NEW |
| 24 | MEDIUM | 0 | Heřmánková et al. (2025) | From Fragmented Data to Linked History: Developing the FAIR Epigraphic Vocabularies | 10.5334/johd.428 | cited-by #6 | FAIR epigraphy | NEW |
| 25 | MEDIUM | 0 | Mazzamurro, M.; Hermankova, P.; Coscia, M.; Brughmans, T. (2025) | The Economic Complexity of the Roman Empire | 10.48550/arxiv.2508.19892 | cited-by #7 | SDAM-adjacent applications of LIST | NEW — OpenAlex-only (arXiv preprint) |

*Full author lists for multi-author rows preserved in the verified draft at `/tmp/inscriptions-lit-scout-draft-2026-04-22.md`.*

---

## Reading tiers

**Tier 1 — must-read before drafting the methods section (8)**: rows 4, 5, 9, 6, 7, 8, 10, 1.
*Rationale: rcarbon/SPD grammar (4, 5); Bayesian-aoristic pivot for inscription-style data (9); Aarhus group prior art on LIST-type data (6, 7, 8); aoristic primer (10); Hanson hypothesis under test (1).*

**Tier 2 — SPD/demography background (5)**: rows 3, 11, 12, 15, 18.

**Tier 3 — Roman urban demography framing (3)**: rows 2, 13, 14.

**Tier 4 — epigraphic habit framing (3–4)**: rows 20, 21, 22; optionally 16.

**Tier 5 — data and context (2)**: rows 23 (LIST dataset — cite every time the corpus is mentioned), 17 (open-data template for derivative dataset deposit).

**Tier 6 — adjacent (3)**: rows 24, 25, 19.

---

## Gaps in the literature

1. **No published paper applies rcarbon permutation envelopes to Latin inscription date distributions.** The Glomb/Kaše/Heřmánková 2022 Asclepius paper does temporal modelling of epigraphic evidence but with a simpler probabilistic-date framework; it does not use Crema/Bevan permutation tests against a null pan-empire envelope. **This is the originality of what this paper proposes.**
2. **No paper benchmarks aoristic SPA vs Crema's 2025 Bayesian alternative on inscription data.** Crema 2025 calls for exactly this application; none exists yet for epigraphy. Second-paper opportunity.
3. **Very few non-SDAM authors engage methodologically with LIST.** All SDAM applications come from the same author cluster; external validation would strengthen the dataset's standing and this paper's citation edge.
4. **The 1982 → 2021 gap in quantitative epigraphic habit work.** Between MacMullen 1982 and the Hanson/SDAM quantitative revival after ~2017, there are few purely-quantitative interventions. This paper enters a thin literature, not a crowded one.
5. **Hanson's population-estimate dataset has no Zenodo/Figshare deposit.** tDAR record 448563 is the documented source; LIST already embeds Hanson 2016 classifications via `urban_context_*` attributes (confirmed by OpenAlex abstract on row 23).

---

## Venue analysis

- **Journal of Archaeological Method and Theory (JAMT)** — primary target for the methods paper. Crema 2012 and Crema 2022 both landed here.
- **Journal of Archaeological Science (JAS)** — companion applied paper. Williams 2012, Timpson 2014, Palmisano 2017.
- **Radiocarbon (Cambridge)** — home of the rcarbon methodology papers; possible if methodological focus dominates.
- **Archaeometry (Wiley)** — Crema 2025 baorista landed here.
- **Journal of Open Archaeology Data (JOAD)** — derivative dataset deposit.

**Recommendation**: JAMT (methods paper) / JAS (applied companion) / JOAD (data).

---

## Flagged / unverifiable claims

- **Hanson 2021 letter-count claim.** The 2024 ANU seminar doc attributes the letter-count recommendation to Hanson 2021. The paper abstract, keywords, and title do not support this (focus is inscription-counts as information infrastructure). The Brepols PDF is 403-walled from both proposer and verifier. **Action required**: PDF check before citing. Possibilities: (a) body text does discuss letter-counts, (b) 2024 attribution is conflated (e.g., with Hanson/Ortman/Lobo 2017 or the Bettencourt scaling literature).
- **Kaše affiliation.** Proposer states University of West Bohemia primary (from OpenAlex profile data); verifier cannot confirm from metadata endpoint alone but did not find contradicting evidence. Action required if affiliation is load-bearing for acknowledgements.
- **Row 25 (Mazzamurro 2025).** arXiv preprint, CrossRef 404, OpenAlex-only. Author list verified against OpenAlex. Action required only if the citation becomes load-bearing.
- **tDAR Hanson dataset.** Record ID 448563 exists but landing page 403-blocked from both agents. Action required if we need machine-readable Hanson population data beyond what LIST already embeds.

---

## Zotero actions

1. **Merge duplicate Meyer 1990 entries** (keys `SIUN4WXI`, `WNBSMYDZ`). Run as part of the planned cull pass.
2. **Add 24 NEW entries** (all rows except #22) via the BibTeX file at `planning/inscriptions-spa.bib`. File-import into Zotero.
3. **Subcollection path**: `SDAM-AU > SPA > 2026 conference paper` (per proposed Zotero structure in the backlog).
4. **Parallel**: run `/gaps` on the existing `SDAM-AU > SPA` collection to surface anything this bibliography missed.

---

## Deeper chaining — deferred

Not run; awaiting go/no-go. Backlogged for post-Saturday.

1. **Forward L2 of Kaše et al. 2022 PLOS ONE (#7)** — to find any non-SDAM uses of LIST. *Recommended: approve.*
2. **Forward L2 of Crema & Bevan 2021 rcarbon (#4)** — to find non-Neolithic applications. *Conditional.*
3. **Backward L3 of Crema 2025 baorista (#9)** — defer.
