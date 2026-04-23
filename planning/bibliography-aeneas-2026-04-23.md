# Aeneas / computational-sibling bibliography

**Date:** 2026-04-23
**Source:** supplementary `lit-scout` + `lit-scout-verifier` run (proposer-verifier serial chain per `notes/lit-scout-case-study.md`).
**Motivation:** the primary `lit-scout` run of 2026-04-22 chained through SDAM epigraphy + Crema/Bevan SPD methodology + Hanson urban demography and missed the computational-sibling cluster. This pass fills the gap. See `docs/notes/reflections/working-notes.md` Obs 10 for the methodological lesson (`[PATTERN]` tag).
**Verification:** 15/15 rows passed adversarial re-query; 0 corrections to the findings table; Cullhed 2025 year resolved against CrossRef/OpenAlex mismatch (2025 canonical). Working draft and full narrative (landscape, reading tiers, venue analysis, gap analysis, direct answers) preserved at `/tmp/inscriptions-lit-scout-aeneas-draft-2026-04-23.md`.
**BibTeX:** `planning/inscriptions-aeneas.bib` (14 CrossRef-grounded entries; Bamman & Burns 2020 arXiv-only, added manually via Zotero import).

---

## TL;DR

**Aeneas** (Assael et al. 2025, DOI `10.1038/s41586-025-09292-5`) is the Latin counterpart to Ithaca (2022). Trained on ~176,861 inscriptions via EDR + EDH + EDCS; public interface at predictingthepast.com; GitHub at `google-deepmind/predictingthepast`. Two independent competing Latin-epigraphy ML groups also active: Sapienza (Ceriotti et al. 2025, LatinBERT+EDR) and Udine (Locaputo et al. 2024). Cullhed 2025 is the only peer-reviewed comparative benchmark — against Ithaca (not Aeneas); Llama 3.1 wins on restoration, loses on attribution. **No peer-reviewed archaeological critique of Aeneas exists** — publishable gap.

## Load-bearing finding

**Aeneas was trained on EDR + EDH + EDCS.** LIRE is substantially derived from EDCS. **Any evaluation of Aeneas against LIRE / LIST has a training-set overlap (data-leakage) risk.** This affects how we can frame any paper claim involving Aeneas performance. Saturday feasibility doc should flag it explicitly.

## Verified findings table

| # | Fit | Cites | Authors (Year) | Title (short) | DOI | Cluster | Status |
|---|-----|-------|----------------|---------------|-----|---------|--------|
| 1 | HIGH | 7 | Assael et al. (2025) [14 authors] | Contextualizing ancient texts with generative neural networks | 10.1038/s41586-025-09292-5 | Aeneas core | NEW |
| 2 | HIGH | 159 | Assael et al. (2022) [9 authors] | Restoring and attributing ancient texts (Ithaca) | 10.1038/s41586-022-04448-z | Ithaca/Aeneas lineage | [IN ZOTERO] — duplicated (46VK795Q, QLWFV6BA) |
| 3 | HIGH | 0 | Ceriotti, Gerardi, Malatesta, Orlandi (2025) | Language Modeling for Epigraphs: BERT for EDR's Latin | 10.1109/ieee-ch65308.2025.11279443 | Latin-epigraphy BERT | NEW |
| 4 | HIGH | 3 | Locaputo et al. (2024) | AI for the Restoration of Ancient Inscriptions: A Computational Linguistics Perspective | 10.1007/978-3-031-57675-1_7 | Latin-epigraphy BERT | NEW |
| 5 | HIGH | 51 | Sommerschield et al. (2023) [10 authors] | Machine Learning for Ancient Languages: A Survey | 10.1162/coli_a_00481 | ML-for-ancient survey | NEW |
| 6 | HIGH | 0 | Cullhed (2025) | Instruction-tuning LLMs to restore ancient Greek papyri and inscriptions | 10.1093/llc/fqaf131 | Ithaca/Aeneas comparative | NEW |
| 7 | HIGH | 42 | Assael, Sommerschield, Prag (2019) | Pythia — deep learning on Greek epigraphy | 10.18653/v1/d19-1668 | Pythia/Ithaca/Aeneas lineage | NEW |
| 8 | MEDIUM | 1 | Tupman (2025) | AI for Latin inscriptions — *Nature* News & Views | 10.1038/d41586-025-02132-6 | Aeneas commentary | NEW |
| 9 | MEDIUM | 0 | Krause (2025) | Reconstructing Latin inscriptions with Aeneas — *Folia Linguistica* review | 10.1515/flin-2025-2027 | Aeneas commentary | NEW |
| 10 | HIGH | 0 | Gong, Gero, Schiefsky (2025) | Augmented Close Reading for Classical Latin using BERT | 10.18653/v1/2025.nlp4dh-1.35 | Latin-BERT applications | NEW |
| 11 | MEDIUM | 4 | Aioanei et al. (2024) | Deep Aramaic — synthetic data for ML in epigraphy | 10.1371/journal.pone.0299297 | ML-epigraphy methodology | NEW |
| 12 | MEDIUM | 1 | Pavlopoulos et al. (2024) | Error Correction in Recognised Byzantine Greek | 10.18653/v1/2024.ml4al-1.1 | ML4AL shared task | NEW |
| 13 | MEDIUM | 10 | Lazar et al. (2021) | Filling Gaps in Ancient Akkadian Texts (MLM) | 10.18653/v1/2021.emnlp-main.384 | MLM for ancient-text restoration | NEW |
| 14 | LOW | 3 | Chapinal-Heras, Díaz-Sánchez (2024) | AI applications in human sciences research | 10.1016/j.daach.2024.e00323 | AI-humanities survey | NEW |
| 15 | LOW | 1 | Qi, Wen (2025) | LLMs in Archaeological Science: A Review | 10.3390/electronics14224507 | LLM-archaeology survey | NEW |

**arXiv-only (manual Zotero entry):** Bamman & Burns (2020), *Latin BERT: A Contextual Language Model for Classical Philology*, arXiv:2009.10053, OpenAlex W3088026279. Foundational Latin-BERT; referenced by Gong (row 10) and Ceriotti (row 3).

## Reading tiers

- **Tier A (in depth):** Aeneas (1), Ithaca (2), Ceriotti (3), Locaputo (4), Cullhed (6).
- **Tier B (selective):** ML4AL Survey (5), Pythia (7), Gong (10), Tupman (8).
- **Tier C (skim/passing):** Krause (9), Aioanei (11), Pavlopoulos (12), Lazar (13), Chapinal-Heras (14), Qi (15).

## Gaps that inform the paper

1. **No critical epigrapher response to Aeneas** beyond Tupman's *Nature* N&V — publishable niche.
2. **No published Aeneas vs Ceriotti LatinBERT+EDR comparison** on a shared test set.
3. **No ML/NLP paper uses LIRE or LIST specifically** — both a gap and a possible contribution.
4. **No published critique of Ithaca / Aeneas dating methodology** — ground truth is epigrapher-assigned intervals; epistemic circularity unexamined.

## Venues (computational-sibling ranked)

- *Nature* — flagship; Ithaca, Aeneas.
- *Digital Scholarship in the Humanities* (Oxford) — Cullhed 2025. Right fit for epigrapher-authored critique.
- *Computational Humanities Research* — ML4AL and Lazar-track audience.
- *Computational Linguistics* (MIT) — methodological contributions.
- NLP4DH / LaTeCH-CLfL / ML4AL / ALP (ACL workshops) — DH / ancient-language ML.
- IEEE CH — Ceriotti 2025.

**Recommendation if our paper turns out to need a computational-sibling venue**: *Digital Scholarship in the Humanities* for a critical audit; NLP4DH / LaTeCH for a positive ML contribution. Primary venues (JAMT, JAS) per `planning/bibliography-2026-04-22.md` unchanged.

## Zotero actions (additions to Issue #1 scope)

- Import the 14 NEW DOIs from `inscriptions-aeneas.bib` into the `SDAM-AU > SPA > 2026 conference paper` subcollection.
- Manually add Bamman & Burns 2020 (arXiv:2009.10053, OpenAlex W3088026279).
- Merge existing duplicate Ithaca entries (keys `46VK795Q`, `QLWFV6BA`) — adds to the Meyer-1990 merge task already in the cull list.
