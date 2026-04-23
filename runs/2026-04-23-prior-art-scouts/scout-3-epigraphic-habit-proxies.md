---
title: "Prior-art scout 3 — quantitative epigraphic-habit translator proxies"
commissioned: 2026-04-23
completed: 2026-04-23
agent: prior-art-scout
scope: Q3 of three-scout overnight run — cultural-translator covariate candidates for H3 sensitivity analysis
source: background agent invocation during 2026-04-23 session
verification: agent-returned; DOI / URL verification pending
---

# Scout 3 — Quantitative proxies for epigraphic-habit variation

## Executive summary

The MacMullen–Meyer–Woolf framework remains overwhelmingly qualitative; this has not fundamentally changed. What has emerged since c. 2015 is a cluster of urban-scaling and computational-epigraphy studies that encounter the epigraphic-habit problem and deal with it — but nearly always by exclusion or containment (restricting analysis to the Latin West; treating east vs west as a binary indicator variable; acknowledging the problem and proceeding) rather than by constructing an explicit numerical proxy. The one partial exception is Hanson (2021), who demonstrates a **sublinear** power-law relationship between inscription counts and estimated city populations, which implicitly characterises the habit as a scaling coefficient. Carleton et al. (2025) advance this via full Bayesian scaling regression with provincial-level random effects, providing the most methodologically rigorous treatment to date, though neither paper produces a standalone proxy that can be detached from its model and joined to an external dataset like LIRE. For the use-case (a cultural-translator covariate in a sensitivity analysis), **the literature offers approaches to adapt rather than ready-made measures to adopt.**

## Candidates

| # | Citation | Type | Activity | Fit | Notes |
|---|----------|------|----------|-----|-------|
| 1 | Hanson, J. W. (2021) "Cities, information, and the epigraphic habit." *J. Urban Archaeology* 4: 137–52 | Journal article | 2021 | **HIGH** | Closest existing operationalisation; establishes **sublinear** scaling of inscription counts vs population; argues inscriptions are "information infrastructure." Paywall; supplementary data unknown. |
| 2 | Carleton, W. C. *et al.* (2025) "Parallel scaling of elite wealth in ancient Roman and modern cities." *Nature Cities*. DOI 10.1038/s44284-025-00213-1 | Journal + open code | 2025 (repo updated Jan 2026) | **HIGH** | Uses honorific-dedication inscriptions + monuments as proxies for elite wealth. Bayesian scaling regression explicitly accounts for "potential regional differences among Roman provinces." Province-level random effects included. Code at [wccarleton/urbanscale](https://github.com/wccarleton/urbanscale), CC BY 4.0. |
| 3 | Hanson, J. W., Ortman, S. G., & Lobo, J. (2017) "Urbanism and the division of labour in the Roman Empire." *J. Royal Society Interface* 14: 20170367 | Journal article | 2017 | MEDIUM-HIGH | Uses inscription counts per city alongside guild / association counts; handles habit variation by limiting analysis to western provinces. Habit treated as binary (east/west) rather than continuous covariate. |
| 4 | Kaše, V., Heřmánková, P., & Sobotková, A. (2022) "Division of labor, specialization and diversity in the ancient Roman cities." *PLOS ONE* 17(6): e0269869 | Open-access article + data | 2022 | MEDIUM | Operationalises occupational diversity using **frequency-per-1,000-words normalisation** and bootstrap **1,000-inscription standardised samples**. Restricts to western Empire to control for habit variation. Technique is usable. Code: [sdam-au/social_diversity](https://github.com/sdam-au/social_diversity). |
| 5 | Glomb, T., Kaše, V., & Heřmánková, P. (2022) "Popularity of the cult of Asclepius in the times of the Antonine Plague." *JAS: Reports* 43: 103466 | Open-access article | 2022 | MEDIUM | **Closest existing procedural analogue for temporal habit control.** Monte Carlo simulation of inscription-date uncertainty compared against general epigraphic trend as baseline. Category-specific trend assessed for deviation. Observed/expected ratio per time-bin is an implicit temporal-habit-intensity proxy. Not extracted as reusable variable. |
| 6 | Meyer, E. A. (1990) *JRS* 80: 74–96 | Journal article | 1990 | LOW (as proxy source) | Foundational but qualitative in causal argument. Confirms ~75 % of provincial inscriptions are epitaphs. No formula, no per-capita rates. East/west differential as qualitative factor. |
| 7 | Beltrán Lloris, F. (2015) "The Epigraphic Habit in the Roman World." In Bruun & Edmondson (eds.), *Oxford Handbook of Roman Epigraphy*, 131–48 | Book chapter | 2015 | LOW (as proxy) / **HIGH (as methodological warning)** | Provides raw counts by region (Table 8.2: 458,178 inscriptions from 21,300+ sites) and city-level (Table 8.3). **Critically dismantles MacMullen's Severan-peak graphs as reflecting Lassère's dating conventions rather than real production** — directly validates 2026 mixture-correction framing. Identifies 72 % instrumentum domesticum inflation problem in Britannia. Does not propose replacement formula. |
| 8 | Woolf, G. (1996) "Monumental Writing and the Expansion of Roman Society in the Early Empire." *JRS* 86: 22–39 | Journal article | 1996 | LOW (as proxy source) | Seminal qualitative; bar charts of inscription count by 25-year periods for Gallia Narbonensis and the Three Gauls. No normalisation. |
| 9 | Fernández-Corral, M. (2023/2024) "Roman Voting Tribes, Citizenship, and Epigraphic Habit" in Benefiel & Keesling (eds.) | Book chapter | 2023 | LOW-MEDIUM | Proposes voting-tribe (tribus) mentions as implicit proxy for honorific-habit intensity. ~484 inscriptions with tribal indications concentrated in coastal conventus Tarraconensis. Hispania Citerior only; generalisation uncertain. |
| 10 | Benefiel, R. & Keesling, C. M. (eds.) (2024) *Inscriptions and the Epigraphic Habit* (Brill) | Edited volume | 2024 | LOW | Largely qualitative. BMCR reviewer notes Porucznik's chapter on the Black Sea is the "sole contribution offering a statistical examination." Bodel's introduction explicitly rejects quantification. |
| 11 | Heřmánková, P., Kaše, V., & Sobotková, A. (2021) "Inscriptions as data." *J. Digital History* 1(1) | Open-access article | 2021 | MEDIUM (as dataset gateway) | Methodological paper describing how to treat inscription corpora as data. Defines the LIST dataset (525,870 inscriptions, 65 attributes). |
| 12 | Galsterer (1990); Alföldy (1991) | Essays | 1990–91 | LOW | No evidence of numerical proxy development. |

## Recommendations

### Use directly (with adaptation)

**Carleton et al. (2025) + wccarleton/urbanscale repository.** Most actionable single resource. Bayesian regression in R and Python modelling inscription / monument counts against city population with province-level random effects. The random effects are the closest thing in the literature to an explicit epigraphic-habit covariate vector: extracting the posterior province-level intercepts would yield an independent habit-intensity index joinable to LIRE via Hanson's city-population dataset. CC BY 4.0; Jupyter notebooks and R/Python scripts.

### Adapt the approach

**Glomb, Kaše, & Heřmánková (2022) temporal procedure.** For each time-bin, compute expected frequency of a target inscription category under a null model (random draw from full corpus matched to the same temporal distribution as the general database trend), then test whether observed frequency deviates. The ratio observed/expected per time-bin is an implicit temporal habit-intensity measure. Directly adaptable to LIRE: the "general trend" baseline (all-corpus temporal distribution) computed from EDCS or LIST and each city expressed as a deviation score → candidate α-translator sensitivity variable.

**Hanson (2021) scaling relationship.** Establishes that inscription counts scale **sublinearly** with population — a formal precedent for the correlation H3 will report. The scaling exponent is the empirical basis for claiming population is a genuine driver, not merely an artefact of habit. Full paper paywalled; should be obtained via Macquarie institutional access to verify the exponent and regional residuals.

### Ignore for proxy purposes

MacMullen (1982), Meyer (1990), Woolf (1996/1998), Beltrán Lloris (2015), Alföldy (1991). All are essential intellectual context but none produce a formula, normalised rate, or joinable covariate. **Beltrán Lloris remains essential as methodological citation** for the editorial-convention critique of MacMullen's Severan-peak graphs (directly supports the 2026 mixture-correction approach).

## Build-vs-adopt verdict

**Combine, then construct a novel proxy.**

There is no ready-made, standalone, continuously-valued, province- or city-level epigraphic-habit intensity index that can simply be downloaded and joined to LIRE. **That does not exist.** The absence itself justifies the sensitivity-analysis framing and is reportable as a literature gap.

What exists and can be combined:

1. **Hanson (2021) sublinear scaling** → residuals from a population-scaling regression fitted on the OXREP Roman Cities dataset ([TDAR 448563](https://core.tdar.org/dataset/448563)) measure how much a given city over- or under-produces inscriptions relative to its size — an operationalisation of local epigraphic-habit intensity *net* of population.
2. **Carleton et al. (2025) provincial random effects** → province-level continuous adjustment factor, estimated jointly with population uncertainty. More defensible than naive raw-count ratios.
3. **Glomb et al. (2022) Monte Carlo temporal baseline** → time-bin-level habit proxy (observed / expected ratio for category composition). Handles temporal variation.

Combined: spatial (Carleton provincial effects) + city-level (Hanson residuals) + temporal (Glomb observed/expected ratios) = a multi-dimensional habit proxy. Documenting this construction, and documenting the absence of an established index as a gap in the literature, is a genuine contribution.

## Search coverage and gaps

**Sources searched:** GitHub, Web (Google Scholar proxy), Semantic Scholar, Cambridge Core, Oxford Academic, PLOS ONE / PMC, Brill, BMCR, Sehepunkte, Academia.edu, ResearchGate, Zenodo, TDAR, Nature, arXiv, Hugging Face, PyPI, npm, GitLab.

**Absences that are informative:**

- No results for Gong / Schiefsky computational epigraphy in habit-quantification scope.
- No results for Galsterer 1990 or Alföldy 1991 numerical operationalisation.
- No PyPI or npm packages for epigraphic-habit modelling.
- No Hugging Face models or spaces on epigraphic habit.
- Problem has not been packaged as a reusable software component anywhere.

**Paywalled, not fully inspected:**

- Hanson (2021) *J. Urban Archaeology* (Brepols paywall; abstract + ORA record accessed; full methodology, figures, and exponent values not confirmed).
- Carleton et al. (2025) *Nature Cities* (redirected 303; methodology obtained only via press coverage + Semantic Scholar abstract).

## Implications for the current paper

**Critical empirical finding to verify against Scout 2 (urban-scaling):** Hanson (2021) reports **sublinear** scaling of inscriptions with population. If confirmed, this inverts the framing assumed in Scout 2's brief (which defaulted to the Ortman super-linear pattern). Consequences for H3:

- Sublinear β < 1 means per-capita inscription rates **decrease** with city size — the opposite of what the Ortman framework predicts for production outputs.
- Hanson's "inscriptions as information infrastructure" framing aligns with sublinear scaling (information infrastructure saturates) and may re-open the information-theoretic framing the draft research-intent deprioritised.
- The variance-explained and residual-analysis operationalisations in H3a / H3c should be fitted against a sublinear model, not an OLS assumption.

**Operationalisation technique ready to adopt:** Kaše, Heřmánková & Sobotková (2022) **frequency-per-1,000-words normalisation + bootstrap 1,000-inscription standardised samples**. Transferable to LIRE analyses.

**Paper's literature-gap framing strengthened:** the absence of a numerical epigraphic-habit proxy is a real gap. The paper can cite this scout's finding (in paraphrase: "no published work operationalises epigraphic-habit variation as a continuous covariate at the empire scale") as motivation for the α-parameter-as-translator interpretation (FS-D) and for the mixture-model framing.

## Verification status

**VERIFICATION PENDING.** All DOIs, URLs, and citation counts are agent-returned and should be verified before any of these sources are cited in print. The Hanson (2021) sublinear finding in particular is load-bearing for the scaling-law question (Q2) and should be directly verified from the paper PDF before the preregistration commits to a sublinear model assumption.

## Sources

- Hanson 2021 — [Brepols](https://www.brepolsonline.net/doi/10.1484/J.JUA.5.126597) / [ORA Oxford](https://ora.ox.ac.uk/objects/uuid:90f08acb-16c3-4b80-90f8-f2a2b87e703a)
- Carleton et al. 2025 — [Nature Cities](https://www.nature.com/articles/s44284-025-00213-1) / [GitHub wccarleton/urbanscale](https://github.com/wccarleton/urbanscale)
- Hanson, Ortman & Lobo 2017 — [Royal Society](https://royalsocietypublishing.org/doi/abs/10.1098/rsif.2017.0367)
- Kaše, Heřmánková & Sobotková 2022 — [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0269869) / [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9202948/)
- Glomb, Kaše & Heřmánková 2022 — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2352409X22001298)
- Heřmánková, Kaše & Sobotková 2021 — [J. Digital History](https://www.degruyterbrill.com/document/doi/10.1515/jdh-2021-1004/html)
- Meyer 1990 — [Cambridge Core](https://www.cambridge.org/core/journals/journal-of-roman-studies/article/abs/explaining-the-epigraphic-habit-in-the-roman-empire-the-evidence-of-epitaphs1/A89F0F7C8CFB45A7A1D62D1561E0D2B8)
- Beltrán Lloris 2015 — [Academia.edu preprint](https://www.academia.edu/9670039/)
- Woolf 1996 — [ResearchGate](https://www.researchgate.net/publication/259415171_Monumental_Writing_and_the_Expansion_of_Roman_Society_in_the_Early_Empire)
- Fernández-Corral 2023 — [Brill](https://brill.com/display/book/9789004683129/BP000014.xml)
- Benefiel & Keesling 2024 — [Brill](https://brill.com/display/title/69091) / [BMCR review](https://bmcr.brynmawr.edu/2025/2025.02.39/)
- LIST dataset — [Zenodo](https://zenodo.org/records/10473706)
- Hanson OXREP dataset — [TDAR 448563](https://core.tdar.org/dataset/448563/population-area-and-infrastructural-measures-for-roman-cities-of-the-imperial-period)
- Bodel 2023 — [Academia.edu](https://www.academia.edu/115118360/Epigraphic_culture_and_the_epigraphic_mode_2023)
