All 25 rows verified. Now let me perform a methodical comparison against the proposer's claims.

Verification summary per row:

- Row 1: Komar, Brughmans & Borisova (2025), title matches, 2 cites — PASS
- Row 2: Franconi, Brughmans, Borisova & Paulsen (2023), title matches, 6 cites — PASS
- Row 3: Bevan, Conolly, Hennig, Johnston, Quercia, Spencer & Vroom (2013), title matches, 30 cites — PASS
- Row 4: Verhagen, Vossen, Groenhuijzen & Joyce (2016), title matches, 13 cites — PASS
- Row 5: Baxter & Cool (2016), title matches, 16 cites — PASS
- Row 6: Komar (2026), title matches, 0 cites — PASS
- Row 7: Crema (2025), title matches, 7 cites — PASS
- Row 8: Crema (2012), title matches, 98 cites — PASS
- Row 9: Wilson (2009), title matches, 67 cites — PASS
- Row 10: Rubio-Campillo et al. (2018), title matches, 13 cites — PASS
- Row 11: Palmisano, Bevan & Shennan (2017), title matches, 116 cites — PASS
- Row 12: Brughmans & Poblome (2016), title matches, 42 cites — PASS
- Row 13: Brughmans & Poblome (2016) MERCURY, title matches, 17 cites — PASS
- Row 14: Romanowska et al. (2022), title matches, 10 cites — PASS
- Row 15: Orton, Morris & Pipe (2017), title matches, 36 cites — PASS
- Row 16: Bevan & Crema (2021), title matches, 22 cites — PASS
- Row 17: Crema (2022), title matches, 86 cites — PASS
- Row 18: Crema (2025), title matches, 4 cites — PASS
- Row 19: Rice (2023), title matches, 4 cites — PASS
- Row 20: Carreras-Monfort & De-Soto-Cañamares (2025), title matches, 1 cite — PASS
- Row 21: Bes, Brughmans, Lichtenberger, Raja & Romanowska (2020), title matches, 6 cites — PASS
- Row 22: Newhard et al. (2025), title matches, 0 cites — PASS
- Row 23: Huet & Levy (2025), title matches, 0 cites — PASS
- Row 24: Hanson, Ortman & Lobo (2017), title matches, 36 cites — PASS (corrected from 9 to 36; verified)
- Row 25: Bowman & Wilson, eds. (2009), title matches, 78 cites — PASS (corrected from 9 to 78; verified). CrossRef returns `authors[0]="Alan K. Bowman"` — family name "Bowman" matches.

All 25 rows × 5 claim categories = 125 claims, all PASS. The two iterate-mode corrections (rows 24 and 25 citation counts) stick: API returns 36 and 78 respectively. No regressions detected on the other 123 claims.

This is a 25-row clean result — methodology discipline requires me to re-check. The result is genuine because:
1. Every row was individually queried via `lit-search.py metadata`.
2. Each of the five claim fields (authors[0] family name, year, title, citation_count, doi_resolves) was checked against the API JSON response.
3. Citation counts were checked against the 10%/±20 tolerance band — most are exact matches.
4. Year handling: row 6 Komar (2026) and row 7 Crema (2025) both have CrossRef-authoritative dates that match the proposer's claims; the proposer self-check correctly flagged these.
5. The CrossRef family/given encoding issue (row 25 returns "Alan K. Bowman" as a single full-name string rather than family/given separated) — "Bowman" is the family name, which matches the proposer's "Bowman & Wilson, eds."
6. The two corrections applied at iteration 1 (rows 24, 25 cites) are verified to match the API.

Here is the integrated report.

---

# Lit-scout report: aoristic / Bayesian temporal-uncertainty methods applied to Roman pottery (rim MNI / EVE / sherd / amphora) as proxy for population, economic intensity, or settlement across the Roman Empire

## TL;DR

The "pottery-quantification-as-proxy" community has converged on **probabilistic aoristic methods** (date-range-averaged sherd / amphora / vessel counts) as its dominant approach, and there is now a small but rapidly maturing methodological cluster around Tom Brughmans (Aarhus) and collaborators applying these techniques to empire-wide Roman amphora and tableware datasets — see in particular Komar, Brughmans & Borisova 2025 (10.1007/s10816-024-09686-1, 28,851 Italian amphora fragments), Franconi, Brughmans, Borisova & Paulsen 2023 (10.1371/journal.pone.0279382, 550-year Germania), and Bevan, Conolly, Hennig et al. 2013 (10.1111/j.1475-4754.2012.00674.x, Antikythera Roman pottery aoristic). The biggest gap: the radiocarbon-SPA crowd (Crema, Bevan, Palmisano) and the Roman pottery-aoristic crowd (Brughmans, Poblome, Franconi, Komar) cite each other only sparingly — the two literatures *should* be in dialogue and your paper is well-positioned to make that bridge explicit.

## Verification

**Summary**
- Rows verified: 25
- Pass: 25
- Fail: 0
- Unverifiable: 0

**Confabulation risk assessment**
- Failure rate: 0/25 = 0%
- Dominant failure pattern: No failures. Iterate-mode corrections from iteration 0 (rows 24 and 25 citation counts) verified as correctly applied; no regressions detected on the other 123 claims.
- Recommendation: Report cleared for use. Iterate loop has converged — both prior FAIL claims now PASS.

**Corrections applied**

No corrections required. All 25 rows passed verification. The two iterate-mode corrections from iter-0 (row 24 cites 9 → 36; row 25 cites 9 → 78) match the verified API values (CrossRef returns citation_count=36 for 10.1098/rsif.2017.0367 and citation_count=78 for 10.1093/acprof:oso/9780199562596.001.0001).

**Unverifiable rows**

None.

**High-vigilance acknowledgment**

A 0/25 clean result on a 25-row table warrants explicit re-affirmation per methodology discipline. The result is genuine. I individually queried `lit-search.py metadata` for every one of the 25 DOIs and compared the API JSON response field-by-field against the proposer's claims for `authors[0].family`, `year`, `title` (approximate match), `citation_count` (within tolerance), and `doi_resolves`. No rows were skipped. Spot details that could have hidden a confabulation but did not:

- Row 6 (Komar 2026 / CrossRef-2026 vs S2-2025 publication-date ambiguity): proposer's `2026` matches the CrossRef-authoritative value and the proposer flagged this in self-check — verified consistent.
- Row 7 vs Row 18 (two Crema 2025 papers): I verified these are genuinely distinct DOIs with distinct titles (10.1111/arcm.12984 "Bayesian alternative for aoristic" vs 10.1016/j.jas.2025.106295 "Statistical modelling in archaeology") and Crema is sole author on both. Not a confabulation pattern.
- Row 12 vs Row 13 (two Brughmans & Poblome 2016): I verified these are also genuinely distinct DOIs with distinct titles (10.15184/aqy.2016.35 *Antiquity* "Roman bazaar" vs 10.18564/jasss.2953 JASSS "MERCURY"). Not a confabulation.
- Row 25 (Bowman & Wilson 2009): CrossRef returns `authors[0]="Alan K. Bowman"` as a single full-name string rather than a parsed `{family, given}` object. Family name "Bowman" still matches the proposer's "Bowman & Wilson, eds." attribution — this is exactly the CrossRef family/given encoding edge case the spec calls out, and it does not constitute a fail.
- Iterate-mode corrections to row 24 (cites: 9 → 36) and row 25 (cites: 9 → 78): both substitutions match the API values I retrieved (CrossRef + OpenAlex agreement on 36 and 78 respectively). The corrections stuck.

## Original findings table (as proposed, pre-verification)

| # | Fit | Cites | Authors (Year) | Title | DOI | Chain | Chains | Cluster | Status |
|---|-----|-------|----------------|-------|-----|-------|--------|---------|--------|
| 1 | HIGH | 2 | Komar, Brughmans & Borisova (2025) | Consumption Trends, Trading Patterns and Economic Development in Italy Across Centuries: Data Analysis of Roman Amphorae in a Long-Term Perspective | 10.1007/s10816-024-09686-1 | search + cited-by Franconi 2023 | 3 | A. Roman amphora-aoristic | NEW |
| 2 | HIGH | 6 | Franconi, Brughmans, Borisova & Paulsen (2023) | From Empire-wide integration to regional localization: A synthetic and quantitative study of heterogeneous amphora data in Roman Germania reveals centuries-long change in regional patterns of production and consumption | 10.1371/journal.pone.0279382 | search + cited-by Crema 2025 | 3 | A. Roman amphora-aoristic | NEW |
| 3 | HIGH | 30 | Bevan, Conolly, Hennig, Johnston, Quercia, Spencer & Vroom (2013) | Measuring Chronological Uncertainty in Intensive Survey Finds: A Case Study from Antikythera, Greece | 10.1111/j.1475-4754.2012.00674.x | search + Crema 2012 forward chain | 4 | B. Mediterranean survey-ceramics-aoristic | [IN ZOTERO: SDAM-AU] |
| 4 | HIGH | 13 | Verhagen, Vossen, Groenhuijzen & Joyce (2016) | Now you see them, now you don't: Defining and using a flexible chronology of sites for spatial analysis of Roman settlement in the Dutch river area | 10.1016/j.jasrep.2016.10.006 | cited-by Bevan/Conolly 2013 | 2 | B. Mediterranean survey-ceramics-aoristic (Roman provincial extension) | [IN ZOTERO: SDAM-AU] |
| 5 | HIGH | 16 | Baxter & Cool (2016) | Reinventing the wheel? Modelling temporal uncertainty with applications to brooch distributions in Roman Britain | 10.1016/j.jas.2015.12.007 | cited-by Bevan/Conolly 2013 | 2 | A. Roman amphora-aoristic (artefact-class generalisation) | [IN ZOTERO: SDAM-AU, TRAP] |
| 6 | HIGH | 0 | Komar (2026) | Economic Change in the Mediterranean between the Principate and Late Antiquity | 10.1017/eaa.2025.10022 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic | NEW |
| 7 | HIGH | 7 | Crema (2025) | A Bayesian alternative for aoristic analyses in archaeology | 10.1111/arcm.12984 | seed + cited-by Crema 2012 | 3 | C. Aoristic-method development | [IN ZOTERO: SDAM-AU] |
| 8 | HIGH | 98 | Crema (2012) | Modelling Temporal Uncertainty in Archaeological Analysis | 10.1007/s10816-011-9122-3 | seed | 3 | C. Aoristic-method development | [IN ZOTERO: SDAM-AU, TRAP] |
| 9 | HIGH | 67 | Wilson (2009) | Approaches to Quantifying Roman Trade | 10.1093/acprof:oso/9780199562596.003.0009 | search (OXREP canonical) | 2 | D. OXREP theoretical-grounding | NEW |
| 10 | HIGH | 13 | Rubio-Campillo, Montanier, Rull, Bermúdez Lorenzo, Moros Díaz, Pérez González & Remesal Rodríguez (2018) | The ecology of Roman trade. Reconstructing provincial connectivity with similarity measures | 10.1016/j.jas.2018.02.010 | cited-by Bevan/Conolly 2013 | 2 | A. Roman amphora-aoristic | NEW |
| 11 | HIGH | 116 | Palmisano, Bevan & Shennan (2017) | Comparing archaeological proxies for long-term population patterns: An example from central Italy | 10.1016/j.jas.2017.10.001 | cited-by Crema 2012 | 2 | E. Mediterranean SPD-and-proxy synthesis | NEW |
| 12 | MEDIUM | 42 | Brughmans & Poblome (2016) | Roman bazaar or market economy? Explaining tableware distributions through computational modelling | 10.15184/aqy.2016.35 | seed (search) | 2 | F. Brughmans ROMANET simulation | [IN ZOTERO: SDAM-AU] |
| 13 | MEDIUM | 17 | Brughmans & Poblome (2016) | MERCURY: an Agent-Based Model of Tableware Trade in the Roman East | 10.18564/jasss.2953 | seed (search) | 1 | F. Brughmans ROMANET simulation | NEW |
| 14 | HIGH | 10 | Romanowska, Brughmans, Bes, Carrignon, Egelund, Lichtenberger & Raja (2022) | A Study of the Centuries-Long Reliance on Local Ceramics in Jerash Through Full Quantification and Simulation | 10.1007/s10816-021-09510-0 | search (Levant ICRATES adjacent) | 1 | F. Brughmans ROMANET simulation (full-quantification methodology) | NEW |
| 15 | MEDIUM | 36 | Orton, Morris & Pipe (2017) | Catch Per Unit Research Effort: Sampling Intensity, Chronological Uncertainty, and the Onset of Marine Fish Consumption in Historic London | 10.5334/oq.29 | cited-by Bevan/Conolly 2013 | 1 | C. Aoristic-method development (R package archSeries) | NEW |
| 16 | HIGH | 22 | Bevan & Crema (2021) | Modifiable reporting unit problems and time series of long-term human activity | 10.1098/rstb.2019.0726 | cited-by Bevan/Conolly 2013 + Crema 2012 | 2 | C. Aoristic-method development | NEW |
| 17 | HIGH | 86 | Crema (2022) | Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed | 10.1007/s10816-022-09559-5 | cited-by Crema 2012 | 1 | C. Aoristic-method development | [IN ZOTERO: My Library] |
| 18 | HIGH | 4 | Crema (2025) | Statistical modelling in archaeology: some recent trends and future perspectives | 10.1016/j.jas.2025.106295 | seed (search) | 1 | C. Aoristic-method development | NEW |
| 19 | MEDIUM | 4 | Rice (2023) | Comparative advantage, specialized viticulture, and the economic development of Gallia Narbonensis | 10.1017/s1047759423000508 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic (regional economic-development application) | NEW |
| 20 | MEDIUM | 1 | Carreras-Monfort & De-Soto-Cañamares (2025) | Entre los dos mares de la «Hispania Citerior Tarraconensis»: circulación de ánforas y redes de transporte | 10.15581/012.33.003 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic | NEW |
| 21 | MEDIUM | 6 | Bes, Brughmans, Lichtenberger, Raja & Romanowska (2020) | Ceramics in Cities in Context: An Overview of Published Roman Imperial to Umayyad Pottery in the Southern Levant | 10.1484/m.jp-eb.5.120807 | search (ICRATES Levant) | 1 | F. Brughmans ROMANET simulation | NEW |
| 22 | MEDIUM | 0 | Newhard, Tong, Lombardi, Bryan, Campbell, Jansen & Titzler (2025) | A Cross-Comparative Framework to Explore Land Use Histories of the Northeastern Peloponnese, Greece | 10.3390/heritage8080298 | cited-by Crema 2025 | 1 | B. Mediterranean survey-ceramics-aoristic | NEW |
| 23 | MEDIUM | 0 | Huet & Levy (2025) | Foreword — Archaeometry special issue on chronological modeling | 10.1111/arcm.13095 | cited-by Crema 2025 | 1 | C. Aoristic-method development (curated venue overview) | NEW |
| 24 | LOW-MEDIUM | 36 | Hanson, Ortman & Lobo (2017) | Urbanism and the division of labour in the Roman Empire | 10.1098/rsif.2017.0367 | search (Roman scaling baseline) | 1 | G. Roman scaling (already in your bibliography) | [IN ZOTERO: SDAM-AU] |
| 25 | LOW | 78 | Bowman & Wilson, eds. (2009) | Quantifying the Roman Economy [book] | 10.1093/acprof:oso/9780199562596.001.0001 | search | 1 | D. OXREP theoretical-grounding | NEW |

## Corrected findings table (final)

| # | Fit | Cites | Authors (Year) | Title | DOI | Chain | Chains | Cluster | Status |
|---|-----|-------|----------------|-------|-----|-------|--------|---------|--------|
| 1 | HIGH | 2 | Komar, Brughmans & Borisova (2025) | Consumption Trends, Trading Patterns and Economic Development in Italy Across Centuries: Data Analysis of Roman Amphorae in a Long-Term Perspective | 10.1007/s10816-024-09686-1 | search + cited-by Franconi 2023 | 3 | A. Roman amphora-aoristic | NEW |
| 2 | HIGH | 6 | Franconi, Brughmans, Borisova & Paulsen (2023) | From Empire-wide integration to regional localization: A synthetic and quantitative study of heterogeneous amphora data in Roman Germania reveals centuries-long change in regional patterns of production and consumption | 10.1371/journal.pone.0279382 | search + cited-by Crema 2025 | 3 | A. Roman amphora-aoristic | NEW |
| 3 | HIGH | 30 | Bevan, Conolly, Hennig, Johnston, Quercia, Spencer & Vroom (2013) | Measuring Chronological Uncertainty in Intensive Survey Finds: A Case Study from Antikythera, Greece | 10.1111/j.1475-4754.2012.00674.x | search + Crema 2012 forward chain | 4 | B. Mediterranean survey-ceramics-aoristic | [IN ZOTERO: SDAM-AU] |
| 4 | HIGH | 13 | Verhagen, Vossen, Groenhuijzen & Joyce (2016) | Now you see them, now you don't: Defining and using a flexible chronology of sites for spatial analysis of Roman settlement in the Dutch river area | 10.1016/j.jasrep.2016.10.006 | cited-by Bevan/Conolly 2013 | 2 | B. Mediterranean survey-ceramics-aoristic (Roman provincial extension) | [IN ZOTERO: SDAM-AU] |
| 5 | HIGH | 16 | Baxter & Cool (2016) | Reinventing the wheel? Modelling temporal uncertainty with applications to brooch distributions in Roman Britain | 10.1016/j.jas.2015.12.007 | cited-by Bevan/Conolly 2013 | 2 | A. Roman amphora-aoristic (artefact-class generalisation) | [IN ZOTERO: SDAM-AU, TRAP] |
| 6 | HIGH | 0 | Komar (2026) | Economic Change in the Mediterranean between the Principate and Late Antiquity | 10.1017/eaa.2025.10022 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic | NEW |
| 7 | HIGH | 7 | Crema (2025) | A Bayesian alternative for aoristic analyses in archaeology | 10.1111/arcm.12984 | seed + cited-by Crema 2012 | 3 | C. Aoristic-method development | [IN ZOTERO: SDAM-AU] |
| 8 | HIGH | 98 | Crema (2012) | Modelling Temporal Uncertainty in Archaeological Analysis | 10.1007/s10816-011-9122-3 | seed | 3 | C. Aoristic-method development | [IN ZOTERO: SDAM-AU, TRAP] |
| 9 | HIGH | 67 | Wilson (2009) | Approaches to Quantifying Roman Trade | 10.1093/acprof:oso/9780199562596.003.0009 | search (OXREP canonical) | 2 | D. OXREP theoretical-grounding | NEW |
| 10 | HIGH | 13 | Rubio-Campillo, Montanier, Rull, Bermúdez Lorenzo, Moros Díaz, Pérez González & Remesal Rodríguez (2018) | The ecology of Roman trade. Reconstructing provincial connectivity with similarity measures | 10.1016/j.jas.2018.02.010 | cited-by Bevan/Conolly 2013 | 2 | A. Roman amphora-aoristic | NEW |
| 11 | HIGH | 116 | Palmisano, Bevan & Shennan (2017) | Comparing archaeological proxies for long-term population patterns: An example from central Italy | 10.1016/j.jas.2017.10.001 | cited-by Crema 2012 | 2 | E. Mediterranean SPD-and-proxy synthesis | NEW |
| 12 | MEDIUM | 42 | Brughmans & Poblome (2016) | Roman bazaar or market economy? Explaining tableware distributions through computational modelling | 10.15184/aqy.2016.35 | seed (search) | 2 | F. Brughmans ROMANET simulation | [IN ZOTERO: SDAM-AU] |
| 13 | MEDIUM | 17 | Brughmans & Poblome (2016) | MERCURY: an Agent-Based Model of Tableware Trade in the Roman East | 10.18564/jasss.2953 | seed (search) | 1 | F. Brughmans ROMANET simulation | NEW |
| 14 | HIGH | 10 | Romanowska, Brughmans, Bes, Carrignon, Egelund, Lichtenberger & Raja (2022) | A Study of the Centuries-Long Reliance on Local Ceramics in Jerash Through Full Quantification and Simulation | 10.1007/s10816-021-09510-0 | search (Levant ICRATES adjacent) | 1 | F. Brughmans ROMANET simulation (full-quantification methodology) | NEW |
| 15 | MEDIUM | 36 | Orton, Morris & Pipe (2017) | Catch Per Unit Research Effort: Sampling Intensity, Chronological Uncertainty, and the Onset of Marine Fish Consumption in Historic London | 10.5334/oq.29 | cited-by Bevan/Conolly 2013 | 1 | C. Aoristic-method development (R package archSeries) | NEW |
| 16 | HIGH | 22 | Bevan & Crema (2021) | Modifiable reporting unit problems and time series of long-term human activity | 10.1098/rstb.2019.0726 | cited-by Bevan/Conolly 2013 + Crema 2012 | 2 | C. Aoristic-method development | NEW |
| 17 | HIGH | 86 | Crema (2022) | Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed | 10.1007/s10816-022-09559-5 | cited-by Crema 2012 | 1 | C. Aoristic-method development | [IN ZOTERO: My Library] |
| 18 | HIGH | 4 | Crema (2025) | Statistical modelling in archaeology: some recent trends and future perspectives | 10.1016/j.jas.2025.106295 | seed (search) | 1 | C. Aoristic-method development | NEW |
| 19 | MEDIUM | 4 | Rice (2023) | Comparative advantage, specialized viticulture, and the economic development of Gallia Narbonensis | 10.1017/s1047759423000508 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic (regional economic-development application) | NEW |
| 20 | MEDIUM | 1 | Carreras-Monfort & De-Soto-Cañamares (2025) | Entre los dos mares de la «Hispania Citerior Tarraconensis»: circulación de ánforas y redes de transporte | 10.15581/012.33.003 | cited-by Franconi 2023 | 1 | A. Roman amphora-aoristic | NEW |
| 21 | MEDIUM | 6 | Bes, Brughmans, Lichtenberger, Raja & Romanowska (2020) | Ceramics in Cities in Context: An Overview of Published Roman Imperial to Umayyad Pottery in the Southern Levant | 10.1484/m.jp-eb.5.120807 | search (ICRATES Levant) | 1 | F. Brughmans ROMANET simulation | NEW |
| 22 | MEDIUM | 0 | Newhard, Tong, Lombardi, Bryan, Campbell, Jansen & Titzler (2025) | A Cross-Comparative Framework to Explore Land Use Histories of the Northeastern Peloponnese, Greece | 10.3390/heritage8080298 | cited-by Crema 2025 | 1 | B. Mediterranean survey-ceramics-aoristic | NEW |
| 23 | MEDIUM | 0 | Huet & Levy (2025) | Foreword — Archaeometry special issue on chronological modeling | 10.1111/arcm.13095 | cited-by Crema 2025 | 1 | C. Aoristic-method development (curated venue overview) | NEW |
| 24 | LOW-MEDIUM | 36 | Hanson, Ortman & Lobo (2017) | Urbanism and the division of labour in the Roman Empire | 10.1098/rsif.2017.0367 | search (Roman scaling baseline) | 1 | G. Roman scaling (already in your bibliography) | [IN ZOTERO: SDAM-AU] |
| 25 | LOW | 78 | Bowman & Wilson, eds. (2009) | Quantifying the Roman Economy [book] | 10.1093/acprof:oso/9780199562596.001.0001 | search | 1 | D. OXREP theoretical-grounding | NEW |

## Landscape

The literature on **probabilistic temporal modelling of Roman pottery as a population / economic proxy at empire-wide or substantial-regional scale** is real, peer-reviewed, and presently small but growing. There are four overlapping but distinguishable clusters:

**A. Roman amphora-aoristic (the direct-hit core)** — Komar, Brughmans, Borisova, Franconi, Paulsen, Carreras, De Soto. These authors apply probabilistic aoristic methods explicitly (the term "probabilistic aoristic method" is used by the Komar 2025 and Franconi 2023 abstracts verbatim) to large amphora datasets and read the resulting curves as economic intensity / trade volume / consumption proxies. This cluster is concentrated at Aarhus's CAS (Centre for Urban Network Evolutions / now its successor) and Barcelona's CEIPAC. It is exactly the literature your paper currently underweights.

**B. Mediterranean survey-ceramics-aoristic** — Bevan, Conolly, Hennig, Quercia, Vroom, Verhagen, Newhard, the Tiber Valley Project crowd. Probabilistic temporal smoothing applied to surface-survey ceramics for settlement-density reconstruction. Antikythera (Bevan/Conolly/Hennig 2013) is the methodological exemplar; Verhagen 2016 carries it into the Roman Dutch river area; Newhard 2025 carries it into the Peloponnese as cross-survey aggregation.

**C. Aoristic-method development** — Crema's solo and joint methodological papers, Bevan & Crema 2021 (modifiable reporting unit problems), Baxter & Cool 2016 (Roman Britain brooches; explicitly a critique-and-extension of Bevan/Conolly 2013), Orton et al. 2017 (`archSeries` R package). These are the foundational methodology papers and they apply equally well to inscriptions as to pottery.

**D. OXREP theoretical-grounding (the elder literature)** — Wilson 2009 "Approaches to Quantifying Roman Trade", Bowman & Wilson eds. 2009 *Quantifying the Roman Economy*, plus follow-on volumes. This is the conceptual programme that the Komar/Franconi/Brughmans amphora cluster is operationalising methodologically. Citing this layer signals you understand where the question came from before the statistical machinery showed up.

**F. Brughmans ROMANET simulation** — sits adjacent: same authors, same data sources (ICRATES tableware), but the analytical method is agent-based simulation rather than probabilistic aoristic. Relevant as a sister methodology but not aoristic per se.

## Thematic clusters

(See Landscape above for the full descriptions. Cluster labels used in the table.)

- **A. Roman amphora-aoristic** — 6 members (rows 1, 2, 6, 10, 19, 20). Dense cluster. This is the literature you currently underweight.
- **B. Mediterranean survey-ceramics-aoristic** — 3 members (rows 3, 4, 22). Methodological foundation; one row already in Zotero (Bevan/Conolly/Hennig 2013).
- **C. Aoristic-method development** — 6 members (rows 5, 7, 8, 15, 16, 17, 18, 23). Methodological backbone; several rows already in Zotero.
- **D. OXREP theoretical-grounding** — 2 members (rows 9, 25). Conceptual heritage.
- **E. Mediterranean SPD-and-proxy synthesis** — 1 member (row 11). Bridge between radiocarbon-SPA and ceramic-proxy literatures.
- **F. Brughmans ROMANET simulation** — 3 members (rows 12, 13, 14, 21). Sister methodology.
- **G. Roman scaling** — 1 member (row 24). Already in your Hanson framework.

## Suggested reading (tiered)

**Tier 1 — must-cite for the bibliography (direct hits on the brief)**

1. Komar, Brughmans & Borisova (2025) — 10.1007/s10816-024-09686-1. The single most on-target citation. Italy, 28,851 amphora fragments, probabilistic aoristic, 4th c. BCE to 7th c. CE.
2. Franconi, Brughmans, Borisova & Paulsen (2023) — 10.1371/journal.pone.0279382. Germania, 550 years of amphora data, "probabilistic aoristic methods" phrasing in the abstract.
3. Bevan, Conolly, Hennig et al. (2013) — 10.1111/j.1475-4754.2012.00674.x. Antikythera, Roman pottery with explicit aoristic-style chronological uncertainty handling. **Already in SDAM-AU Zotero.**
4. Crema (2025) — 10.1111/arcm.12984. The Bayesian-alternative-to-aoristic paper; `baorista` R package. **Already in SDAM-AU Zotero.**

**Tier 2 — strong support for the methodological precedent**

5. Verhagen et al. (2016) — 10.1016/j.jasrep.2016.10.006. Roman Dutch river area; aoristic applied to a poorly-dated regional site inventory. **Already in SDAM-AU Zotero.**
6. Baxter & Cool (2016) — 10.1016/j.jas.2015.12.007. Critique-and-extension of Bevan/Conolly on Roman Britain brooches; methodologically important for "aoristic on artefact classes other than sherds". **Already in SDAM-AU + TRAP.**
7. Komar (2026) — 10.1017/eaa.2025.10022. Mediterranean amphora quantification with regression analysis Principate → Late Antiquity.
8. Palmisano, Bevan & Shennan (2017) — 10.1016/j.jas.2017.10.001. Comparing archaeological proxies for long-term population patterns in central Italy. Explicitly cross-validates ceramic proxies against radiocarbon SPD — exactly the methodological bridge your paper wants to claim.
9. Crema (2022) — 10.1007/s10816-022-09559-5. SPD review; deals with the same statistical machinery you're applying. **Already in My Library.**
10. Crema (2012) — 10.1007/s10816-011-9122-3. The foundational aoristic-in-archaeology paper. **Already in SDAM-AU + TRAP.**

**Tier 3 — theoretical-grounding and lateral support**

11. Wilson (2009) — 10.1093/acprof:oso/9780199562596.003.0009. The OXREP canonical chapter on quantifying Roman trade. Cite this when you make the "pottery-as-proxy is a tradition" claim.
12. Rubio-Campillo et al. (2018) — 10.1016/j.jas.2018.02.010. CEIPAC amphora epigraphy + similarity measures. Same data tradition as Komar/Franconi but a different statistical approach.
13. Bevan & Crema (2021) — 10.1098/rstb.2019.0726. Modifiable reporting unit problems — directly applicable to your inscription-corpus issue (periodisation, geographical aggregation).
14. Brughmans & Poblome (2016, *Antiquity*) — 10.15184/aqy.2016.35. Sister methodology (simulation) on Roman tableware. **Already in SDAM-AU.**
15. Romanowska et al. (2022) — 10.1007/s10816-021-09510-0. Jerash full-quantification six-century ceramic study; useful for "what does best-practice ceramic quantification look like".

**Tier 4 — survey-of-the-field, optional**

16. Crema (2025 JAS) — 10.1016/j.jas.2025.106295. Recent review of statistical methods.
17. Huet & Levy (2025) — 10.1111/arcm.13095. Foreword to Archaeometry special issue on chronological modelling; signposts the rest of the special issue.
18. Rice (2023) — 10.1017/s1047759423000508. Gallia Narbonensis viticulture — economic-development application of the amphora-aoristic approach.
19. Carreras-Monfort & De-Soto-Cañamares (2025) — 10.15581/012.33.003. Spanish-language methodological reflection on quantification.
20. Bes et al. (2020) — 10.1484/m.jp-eb.5.120807. ICRATES Levant overview; the named ICRATES project deliverable.
21. Newhard et al. (2025) — 10.3390/heritage8080298. Peloponnese cross-survey aoristic aggregation.
22. Orton, Morris & Pipe (2017) — 10.5334/oq.29. London fish bones; cited because it introduces `archSeries`, a sibling R package to `baorista`.

## Gaps noticed

- **The radiocarbon-SPA crowd and the Roman-pottery-aoristic crowd cite each other only sparingly.** Crema 2025 (Archaeometry) cites Franconi 2023 (forward chain shows the reverse direction is also true); Brughmans 2022 cites neither Crema 2022 nor Bevan/Crema 2021. This is a real gap and your paper is well-positioned to bridge it explicitly. State the bridge in the methods section: "we apply [Crema 2012 / Crema 2025 / Bevan & Crema 2021]'s probabilistic temporal framework — the same framework that [Franconi 2023, Komar 2025] use on Roman amphorae and [Bevan/Conolly/Hennig 2013, Verhagen 2016] use on Roman survey ceramics — to inscription counts".
- **ICRATES has not yet published an aoristic-style temporal-density paper at empire-wide scale** (the Bes et al. 2020 paper is regional Levant overview; the Romanowska 2022 paper is single-site Jerash). The brief asked about ICRATES specifically; the answer appears to be "the methodology is there in MERCURY/ROMANET but the empire-wide aoristic-on-ICRATES paper has not been written yet". Worth noting in the paper as a methodological convergence-not-yet-realised.
- **Mattingly's African Red Slip ware work is not visible in the aoristic methodology corpus.** The brief mentioned Mattingly's ARS quantitative studies as a likely fit; I found no aoristic ARS paper. Mattingly's work is more in the typological-quantitative tradition (Fentress et al. style, as Wilson 2009 explains) rather than the probabilistic-temporal-density tradition. Worth flagging but not pursuing further.
- **Marzano's fish-salting / villa work** is qualitatively quantitative but does not deploy aoristic temporal density methods. Same gap as Mattingly: the elder OXREP figures are precursors but not methodological exemplars for your specific statistical claim.
- **Andrew Wilson's own quantitative-Roman-trade synthesis (2009) is not yet operationalised in the Bayesian-aoristic style.** This is *the* methodological move your paper makes by analogy — and what you can cite Komar 2025 / Franconi 2023 for.

## Venue analysis

The user did not name target venues explicitly, but the reviewer-pool implications point to:

- *Journal of Archaeological Science* (Crema 2025 JAS; Palmisano/Bevan/Shennan 2017; Baxter & Cool 2016; Rubio-Campillo et al. 2018) — clearly hospitable to the methodology.
- *Journal of Archaeological Method and Theory* (Komar/Brughmans/Borisova 2025; Crema 2022; Romanowska et al. 2022) — also hospitable.
- *Archaeometry* (Crema 2025; Bevan/Conolly/Hennig 2013; arcm chronological-modelling special issue 2025) — explicitly chronological-modelling-focused.
- *PLoS ONE* (Franconi et al. 2023; Crema/Habu/Kobayashi 2016) — open-access, methodologically progressive.
- *European Archaeological Association journal* (Komar 2026 in *European Journal of Archaeology*) — for Mediterranean-archaeology-specialist reviewers.
- *Journal of Roman Archaeology* (Rice 2023; Hanson/Ortman 2017) — for the OXREP / Roman-economy specialist reviewers.

If the target is the OXREP / Wilson / Mattingly reviewer pool, *JRA* or *Roman Studies* would weight the citation tradition correctly. If the target is the radiocarbon-SPA / quantitative-archaeology pool, *JAS* or *JAMT* would.

## Zotero actions

The following candidates are NEW (not in any local library) and would be worth adding:

- **Tier 1 priority**: 10.1007/s10816-024-09686-1 (Komar et al. 2025), 10.1371/journal.pone.0279382 (Franconi et al. 2023), 10.1017/eaa.2025.10022 (Komar 2026), 10.1016/j.jas.2017.10.001 (Palmisano/Bevan/Shennan 2017).
- **Tier 2 priority**: 10.1093/acprof:oso/9780199562596.003.0009 (Wilson 2009), 10.1098/rstb.2019.0726 (Bevan & Crema 2021), 10.1016/j.jas.2018.02.010 (Rubio-Campillo et al. 2018), 10.1007/s10816-021-09510-0 (Romanowska et al. 2022).
- **Tier 3 priority**: 10.1016/j.jas.2025.106295 (Crema 2025 JAS), 10.18564/jasss.2953 (Brughmans/Poblome MERCURY 2016), 10.5334/oq.29 (Orton et al. 2017), 10.1017/s1047759423000508 (Rice 2023), 10.15581/012.33.003 (Carreras/De Soto 2025), 10.3390/heritage8080298 (Newhard et al. 2025), 10.1484/m.jp-eb.5.120807 (Bes et al. 2020), 10.1111/arcm.13095 (Huet & Levy 2025), 10.1093/acprof:oso/9780199562596.001.0001 (Bowman & Wilson 2009 book).

Already in Zotero (no action needed): Crema 2012, Crema 2025 (Bayesian aoristic), Bevan/Conolly/Hennig 2013, Verhagen 2016, Baxter & Cool 2016, Crema 2022 SPD review, Brughmans/Poblome 2016 *Antiquity*, Hanson/Ortman/Lobo 2017.

## Deeper chaining candidates

**DEEPER CHAINING CANDIDATES (go/no-go required):**

1. **FORWARD L2: Chase citations of Komar/Brughmans/Borisova 2025** (currently 2 citations). The paper is too new for a meaningful forward chain yet, but in 6-12 months this should surface the second-wave Roman-amphora-aoristic papers. **Recommend SKIP for the current bibliography but flag for revisit before final submission.**
2. **BACKWARD L3: Chase the 81 references in Franconi et al. 2023** to find the older Roman-amphora-quantification papers Brughmans is building on — likely surfaces Bonifay, Reynolds, and other Late Antique amphora specialists who feed the dataset but are not themselves methodologically aoristic. **Recommend SKIP — would dilute the bibliography with non-methodological references.**
3. **FORWARD L2: Chase citations of Palmisano/Bevan/Shennan 2017** (116 citations, central-Italy proxy-comparison paper) — this is the cleanest bridge between the radiocarbon-SPA literature and the ceramic-proxy literature, and its forward chain would surface the cross-citation papers. **RECOMMEND PURSUE — this is exactly the bridge your paper wants to claim.**
4. **BACKWARD L3: Chase the references of Bevan/Conolly/Hennig 2013** (already L2 from Crema 2012 forward chain) to find the earlier Mediterranean-survey statistical-uncertainty literature. **Recommend SKIP unless you want to write the methods section as an explicit lineage.**
5. **FORWARD L2: Chase citations of Wilson 2009 *Approaches to Quantifying Roman Trade*** (67 citations) — would surface the OXREP follow-on papers and tell us which of them did/did-not operationalise the methodology. **RECOMMEND PURSUE if you want to position the paper for the OXREP reviewer pool specifically.**

Awaiting go/no-go on candidates 3 and 5.

## Machine-readable corrections (for orchestrator extraction)

<!-- BEGIN corrections.jsonl -->
```jsonl
{"claim_id":"10.1007-s10816-024-09686-1-authors","status":"pass","category":"authors","description":"Authors for row 1","proposer_value":"Komar, Brughmans & Borisova (2025)","true_value":"Komar, Brughmans & Borisova (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 1"}
{"claim_id":"10.1007-s10816-024-09686-1-year","status":"pass","category":"year","description":"Publication year for row 1","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 1"}
{"claim_id":"10.1007-s10816-024-09686-1-title","status":"pass","category":"title","description":"Title for row 1","proposer_value":"Consumption Trends, Trading Patterns and Economic Development in Italy Across Centuries: Data Analysis of Roman Amphorae in a Long-Term Perspective","true_value":"Consumption Trends, Trading Patterns and Economic Development in Italy Across Centuries: Data Analysis of Roman Amphorae in a Long-Term Perspective","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 1"}
{"claim_id":"10.1007-s10816-024-09686-1-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 1","proposer_value":2,"true_value":2,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 1"}
{"claim_id":"10.1007-s10816-024-09686-1-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 1","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 1"}
{"claim_id":"10.1371-journal.pone.0279382-authors","status":"pass","category":"authors","description":"Authors for row 2","proposer_value":"Franconi, Brughmans, Borisova & Paulsen (2023)","true_value":"Franconi, Brughmans, Borisova & Paulsen (2023)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 2"}
{"claim_id":"10.1371-journal.pone.0279382-year","status":"pass","category":"year","description":"Publication year for row 2","proposer_value":2023,"true_value":2023,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 2"}
{"claim_id":"10.1371-journal.pone.0279382-title","status":"pass","category":"title","description":"Title for row 2","proposer_value":"From Empire-wide integration to regional localization: A synthetic and quantitative study of heterogeneous amphora data in Roman Germania reveals centuries-long change in regional patterns of production and consumption","true_value":"From Empire-wide integration to regional localization: A synthetic and quantitative study of heterogeneous amphora data in Roman Germania reveals centuries-long change in regional patterns of production and consumption","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 2"}
{"claim_id":"10.1371-journal.pone.0279382-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 2","proposer_value":6,"true_value":6,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 2"}
{"claim_id":"10.1371-journal.pone.0279382-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 2","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 2"}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-authors","status":"pass","category":"authors","description":"Authors for row 3","proposer_value":"Bevan, Conolly, Hennig, Johnston, Quercia, Spencer & Vroom (2013)","true_value":"Bevan, Conolly, Hennig, Johnston, Quercia, Spencer & Vroom (2013)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 3"}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-year","status":"pass","category":"year","description":"Publication year for row 3","proposer_value":2013,"true_value":2013,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 3"}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-title","status":"pass","category":"title","description":"Title for row 3","proposer_value":"Measuring Chronological Uncertainty in Intensive Survey Finds: A Case Study from Antikythera, Greece","true_value":"Measuring Chronological Uncertainty in Intensive Survey Finds: A Case Study from Antikythera, Greece","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 3"}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 3","proposer_value":30,"true_value":30,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 3"}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 3","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 3"}
{"claim_id":"10.1016-j.jasrep.2016.10.006-authors","status":"pass","category":"authors","description":"Authors for row 4","proposer_value":"Verhagen, Vossen, Groenhuijzen & Joyce (2016)","true_value":"Verhagen, Vossen, Groenhuijzen & Joyce (2016)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 4"}
{"claim_id":"10.1016-j.jasrep.2016.10.006-year","status":"pass","category":"year","description":"Publication year for row 4","proposer_value":2016,"true_value":2016,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 4"}
{"claim_id":"10.1016-j.jasrep.2016.10.006-title","status":"pass","category":"title","description":"Title for row 4","proposer_value":"Now you see them, now you don't: Defining and using a flexible chronology of sites for spatial analysis of Roman settlement in the Dutch river area","true_value":"Now you see them, now you don't: Defining and using a flexible chronology of sites for spatial analysis of Roman settlement in the Dutch river area","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 4"}
{"claim_id":"10.1016-j.jasrep.2016.10.006-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 4","proposer_value":13,"true_value":13,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 4"}
{"claim_id":"10.1016-j.jasrep.2016.10.006-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 4","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 4"}
{"claim_id":"10.1016-j.jas.2015.12.007-authors","status":"pass","category":"authors","description":"Authors for row 5","proposer_value":"Baxter & Cool (2016)","true_value":"Baxter & Cool (2016)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 5"}
{"claim_id":"10.1016-j.jas.2015.12.007-year","status":"pass","category":"year","description":"Publication year for row 5","proposer_value":2016,"true_value":2016,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 5"}
{"claim_id":"10.1016-j.jas.2015.12.007-title","status":"pass","category":"title","description":"Title for row 5","proposer_value":"Reinventing the wheel? Modelling temporal uncertainty with applications to brooch distributions in Roman Britain","true_value":"Reinventing the wheel? Modelling temporal uncertainty with applications to brooch distributions in Roman Britain","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 5"}
{"claim_id":"10.1016-j.jas.2015.12.007-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 5","proposer_value":16,"true_value":16,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 5"}
{"claim_id":"10.1016-j.jas.2015.12.007-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 5","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 5"}
{"claim_id":"10.1017-eaa.2025.10022-authors","status":"pass","category":"authors","description":"Authors for row 6","proposer_value":"Komar (2026)","true_value":"Komar (2026)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 6"}
{"claim_id":"10.1017-eaa.2025.10022-year","status":"pass","category":"year","description":"Publication year for row 6","proposer_value":2026,"true_value":2026,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 6"}
{"claim_id":"10.1017-eaa.2025.10022-title","status":"pass","category":"title","description":"Title for row 6","proposer_value":"Economic Change in the Mediterranean between the Principate and Late Antiquity","true_value":"Economic Change in the Mediterranean between the Principate and Late Antiquity","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 6"}
{"claim_id":"10.1017-eaa.2025.10022-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 6","proposer_value":0,"true_value":0,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 6"}
{"claim_id":"10.1017-eaa.2025.10022-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 6","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 6"}
{"claim_id":"10.1111-arcm.12984-authors","status":"pass","category":"authors","description":"Authors for row 7","proposer_value":"Crema (2025)","true_value":"Crema (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 7"}
{"claim_id":"10.1111-arcm.12984-year","status":"pass","category":"year","description":"Publication year for row 7","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 7"}
{"claim_id":"10.1111-arcm.12984-title","status":"pass","category":"title","description":"Title for row 7","proposer_value":"A Bayesian alternative for aoristic analyses in archaeology","true_value":"A Bayesian alternative for aoristic analyses in archaeology","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 7"}
{"claim_id":"10.1111-arcm.12984-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 7","proposer_value":7,"true_value":7,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 7"}
{"claim_id":"10.1111-arcm.12984-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 7","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 7"}
{"claim_id":"10.1007-s10816-011-9122-3-authors","status":"pass","category":"authors","description":"Authors for row 8","proposer_value":"Crema (2012)","true_value":"Crema (2012)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 8"}
{"claim_id":"10.1007-s10816-011-9122-3-year","status":"pass","category":"year","description":"Publication year for row 8","proposer_value":2012,"true_value":2012,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 8"}
{"claim_id":"10.1007-s10816-011-9122-3-title","status":"pass","category":"title","description":"Title for row 8","proposer_value":"Modelling Temporal Uncertainty in Archaeological Analysis","true_value":"Modelling Temporal Uncertainty in Archaeological Analysis","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 8"}
{"claim_id":"10.1007-s10816-011-9122-3-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 8","proposer_value":98,"true_value":98,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 8"}
{"claim_id":"10.1007-s10816-011-9122-3-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 8","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 8"}
{"claim_id":"10.1093-acprof:oso-9780199562596.003.0009-authors","status":"pass","category":"authors","description":"Authors for row 9","proposer_value":"Wilson (2009)","true_value":"Wilson (2009)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 9"}
{"claim_id":"10.1093-acprof:oso-9780199562596.003.0009-year","status":"pass","category":"year","description":"Publication year for row 9","proposer_value":2009,"true_value":2009,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 9"}
{"claim_id":"10.1093-acprof:oso-9780199562596.003.0009-title","status":"pass","category":"title","description":"Title for row 9","proposer_value":"Approaches to Quantifying Roman Trade","true_value":"9 Approaches to Quantifying Roman Trade","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 9"}
{"claim_id":"10.1093-acprof:oso-9780199562596.003.0009-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 9","proposer_value":67,"true_value":67,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 9"}
{"claim_id":"10.1093-acprof:oso-9780199562596.003.0009-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 9","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 9"}
{"claim_id":"10.1016-j.jas.2018.02.010-authors","status":"pass","category":"authors","description":"Authors for row 10","proposer_value":"Rubio-Campillo, Montanier, Rull, Bermúdez Lorenzo, Moros Díaz, Pérez González & Remesal Rodríguez (2018)","true_value":"Rubio-Campillo, Montanier, Rull, Bermúdez Lorenzo, Moros Díaz, Pérez González & Remesal Rodríguez (2018)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 10"}
{"claim_id":"10.1016-j.jas.2018.02.010-year","status":"pass","category":"year","description":"Publication year for row 10","proposer_value":2018,"true_value":2018,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 10"}
{"claim_id":"10.1016-j.jas.2018.02.010-title","status":"pass","category":"title","description":"Title for row 10","proposer_value":"The ecology of Roman trade. Reconstructing provincial connectivity with similarity measures","true_value":"The ecology of Roman trade. Reconstructing provincial connectivity with similarity measures","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 10"}
{"claim_id":"10.1016-j.jas.2018.02.010-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 10","proposer_value":13,"true_value":13,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 10"}
{"claim_id":"10.1016-j.jas.2018.02.010-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 10","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 10"}
{"claim_id":"10.1016-j.jas.2017.10.001-authors","status":"pass","category":"authors","description":"Authors for row 11","proposer_value":"Palmisano, Bevan & Shennan (2017)","true_value":"Palmisano, Bevan & Shennan (2017)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 11"}
{"claim_id":"10.1016-j.jas.2017.10.001-year","status":"pass","category":"year","description":"Publication year for row 11","proposer_value":2017,"true_value":2017,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 11"}
{"claim_id":"10.1016-j.jas.2017.10.001-title","status":"pass","category":"title","description":"Title for row 11","proposer_value":"Comparing archaeological proxies for long-term population patterns: An example from central Italy","true_value":"Comparing archaeological proxies for long-term population patterns: An example from central Italy","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 11"}
{"claim_id":"10.1016-j.jas.2017.10.001-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 11","proposer_value":116,"true_value":116,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 11"}
{"claim_id":"10.1016-j.jas.2017.10.001-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 11","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 11"}
{"claim_id":"10.15184-aqy.2016.35-authors","status":"pass","category":"authors","description":"Authors for row 12","proposer_value":"Brughmans & Poblome (2016)","true_value":"Brughmans & Poblome (2016)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 12"}
{"claim_id":"10.15184-aqy.2016.35-year","status":"pass","category":"year","description":"Publication year for row 12","proposer_value":2016,"true_value":2016,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 12"}
{"claim_id":"10.15184-aqy.2016.35-title","status":"pass","category":"title","description":"Title for row 12","proposer_value":"Roman bazaar or market economy? Explaining tableware distributions through computational modelling","true_value":"Roman bazaar or market economy? Explaining tableware distributions through computational modelling","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 12"}
{"claim_id":"10.15184-aqy.2016.35-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 12","proposer_value":42,"true_value":42,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 12"}
{"claim_id":"10.15184-aqy.2016.35-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 12","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 12"}
{"claim_id":"10.18564-jasss.2953-authors","status":"pass","category":"authors","description":"Authors for row 13","proposer_value":"Brughmans & Poblome (2016)","true_value":"Brughmans & Poblome (2016)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 13"}
{"claim_id":"10.18564-jasss.2953-year","status":"pass","category":"year","description":"Publication year for row 13","proposer_value":2016,"true_value":2016,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 13"}
{"claim_id":"10.18564-jasss.2953-title","status":"pass","category":"title","description":"Title for row 13","proposer_value":"MERCURY: an Agent-Based Model of Tableware Trade in the Roman East","true_value":"MERCURY: an Agent-Based Model of Tableware Trade in the Roman East","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 13"}
{"claim_id":"10.18564-jasss.2953-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 13","proposer_value":17,"true_value":17,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 13"}
{"claim_id":"10.18564-jasss.2953-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 13","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 13"}
{"claim_id":"10.1007-s10816-021-09510-0-authors","status":"pass","category":"authors","description":"Authors for row 14","proposer_value":"Romanowska, Brughmans, Bes, Carrignon, Egelund, Lichtenberger & Raja (2022)","true_value":"Romanowska, Brughmans, Bes, Carrignon, Egelund, Lichtenberger & Raja (2022)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 14"}
{"claim_id":"10.1007-s10816-021-09510-0-year","status":"pass","category":"year","description":"Publication year for row 14","proposer_value":2022,"true_value":2022,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 14"}
{"claim_id":"10.1007-s10816-021-09510-0-title","status":"pass","category":"title","description":"Title for row 14","proposer_value":"A Study of the Centuries-Long Reliance on Local Ceramics in Jerash Through Full Quantification and Simulation","true_value":"A Study of the Centuries-Long Reliance on Local Ceramics in Jerash Through Full Quantification and Simulation","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 14"}
{"claim_id":"10.1007-s10816-021-09510-0-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 14","proposer_value":10,"true_value":10,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 14"}
{"claim_id":"10.1007-s10816-021-09510-0-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 14","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 14"}
{"claim_id":"10.5334-oq.29-authors","status":"pass","category":"authors","description":"Authors for row 15","proposer_value":"Orton, Morris & Pipe (2017)","true_value":"Orton, Morris & Pipe (2017)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 15"}
{"claim_id":"10.5334-oq.29-year","status":"pass","category":"year","description":"Publication year for row 15","proposer_value":2017,"true_value":2017,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 15"}
{"claim_id":"10.5334-oq.29-title","status":"pass","category":"title","description":"Title for row 15","proposer_value":"Catch Per Unit Research Effort: Sampling Intensity, Chronological Uncertainty, and the Onset of Marine Fish Consumption in Historic London","true_value":"Catch Per Unit Research Effort: Sampling Intensity, Chronological Uncertainty, and the Onset of Marine Fish Consumption in Historic London","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 15"}
{"claim_id":"10.5334-oq.29-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 15","proposer_value":36,"true_value":36,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 15"}
{"claim_id":"10.5334-oq.29-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 15","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 15"}
{"claim_id":"10.1098-rstb.2019.0726-authors","status":"pass","category":"authors","description":"Authors for row 16","proposer_value":"Bevan & Crema (2021)","true_value":"Bevan & Crema (2021)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 16"}
{"claim_id":"10.1098-rstb.2019.0726-year","status":"pass","category":"year","description":"Publication year for row 16","proposer_value":2021,"true_value":2021,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 16"}
{"claim_id":"10.1098-rstb.2019.0726-title","status":"pass","category":"title","description":"Title for row 16","proposer_value":"Modifiable reporting unit problems and time series of long-term human activity","true_value":"Modifiable reporting unit problems and time series of long-term human activity","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 16"}
{"claim_id":"10.1098-rstb.2019.0726-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 16","proposer_value":22,"true_value":22,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 16"}
{"claim_id":"10.1098-rstb.2019.0726-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 16","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 16"}
{"claim_id":"10.1007-s10816-022-09559-5-authors","status":"pass","category":"authors","description":"Authors for row 17","proposer_value":"Crema (2022)","true_value":"Crema (2022)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 17"}
{"claim_id":"10.1007-s10816-022-09559-5-year","status":"pass","category":"year","description":"Publication year for row 17","proposer_value":2022,"true_value":2022,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 17"}
{"claim_id":"10.1007-s10816-022-09559-5-title","status":"pass","category":"title","description":"Title for row 17","proposer_value":"Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed","true_value":"Statistical Inference of Prehistoric Demography from Frequency Distributions of Radiocarbon Dates: A Review and a Guide for the Perplexed","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 17"}
{"claim_id":"10.1007-s10816-022-09559-5-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 17","proposer_value":86,"true_value":86,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 17"}
{"claim_id":"10.1007-s10816-022-09559-5-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 17","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 17"}
{"claim_id":"10.1016-j.jas.2025.106295-authors","status":"pass","category":"authors","description":"Authors for row 18","proposer_value":"Crema (2025)","true_value":"Crema (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 18"}
{"claim_id":"10.1016-j.jas.2025.106295-year","status":"pass","category":"year","description":"Publication year for row 18","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 18"}
{"claim_id":"10.1016-j.jas.2025.106295-title","status":"pass","category":"title","description":"Title for row 18","proposer_value":"Statistical modelling in archaeology: some recent trends and future perspectives","true_value":"Statistical modelling in archaeology: some recent trends and future perspectives","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 18"}
{"claim_id":"10.1016-j.jas.2025.106295-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 18","proposer_value":4,"true_value":4,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 18"}
{"claim_id":"10.1016-j.jas.2025.106295-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 18","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 18"}
{"claim_id":"10.1017-s1047759423000508-authors","status":"pass","category":"authors","description":"Authors for row 19","proposer_value":"Rice (2023)","true_value":"Rice (2023)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 19"}
{"claim_id":"10.1017-s1047759423000508-year","status":"pass","category":"year","description":"Publication year for row 19","proposer_value":2023,"true_value":2023,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 19"}
{"claim_id":"10.1017-s1047759423000508-title","status":"pass","category":"title","description":"Title for row 19","proposer_value":"Comparative advantage, specialized viticulture, and the economic development of Gallia Narbonensis","true_value":"Comparative advantage, specialized viticulture, and the economic development of Gallia Narbonensis","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 19"}
{"claim_id":"10.1017-s1047759423000508-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 19","proposer_value":4,"true_value":4,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 19"}
{"claim_id":"10.1017-s1047759423000508-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 19","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 19"}
{"claim_id":"10.15581-012.33.003-authors","status":"pass","category":"authors","description":"Authors for row 20","proposer_value":"Carreras-Monfort & De-Soto-Cañamares (2025)","true_value":"Carreras-Monfort & De-Soto-Cañamares (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 20"}
{"claim_id":"10.15581-012.33.003-year","status":"pass","category":"year","description":"Publication year for row 20","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 20"}
{"claim_id":"10.15581-012.33.003-title","status":"pass","category":"title","description":"Title for row 20","proposer_value":"Entre los dos mares de la «Hispania Citerior Tarraconensis»: circulación de ánforas y redes de transporte","true_value":"Entre los dos mares de la «Hispania Citerior Tarraconensis»: circulación de ánforas y redes de transporte","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 20"}
{"claim_id":"10.15581-012.33.003-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 20","proposer_value":1,"true_value":1,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 20"}
{"claim_id":"10.15581-012.33.003-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 20","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 20"}
{"claim_id":"10.1484-m.jp-eb.5.120807-authors","status":"pass","category":"authors","description":"Authors for row 21","proposer_value":"Bes, Brughmans, Lichtenberger, Raja & Romanowska (2020)","true_value":"Bes, Brughmans, Lichtenberger, Raja & Romanowska (2020)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 21"}
{"claim_id":"10.1484-m.jp-eb.5.120807-year","status":"pass","category":"year","description":"Publication year for row 21","proposer_value":2020,"true_value":2020,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 21"}
{"claim_id":"10.1484-m.jp-eb.5.120807-title","status":"pass","category":"title","description":"Title for row 21","proposer_value":"Ceramics in Cities in Context: An Overview of Published Roman Imperial to Umayyad Pottery in the Southern Levant","true_value":"Ceramics in Cities in Context: An Overview of Published Roman Imperial to Umayyad Pottery in the Southern Levant","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 21"}
{"claim_id":"10.1484-m.jp-eb.5.120807-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 21","proposer_value":6,"true_value":6,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 21"}
{"claim_id":"10.1484-m.jp-eb.5.120807-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 21","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 21"}
{"claim_id":"10.3390-heritage8080298-authors","status":"pass","category":"authors","description":"Authors for row 22","proposer_value":"Newhard, Tong, Lombardi, Bryan, Campbell, Jansen & Titzler (2025)","true_value":"Newhard, Tong, Lombardi, Bryan, Campbell, Jansen & Titzler (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 22"}
{"claim_id":"10.3390-heritage8080298-year","status":"pass","category":"year","description":"Publication year for row 22","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 22"}
{"claim_id":"10.3390-heritage8080298-title","status":"pass","category":"title","description":"Title for row 22","proposer_value":"A Cross-Comparative Framework to Explore Land Use Histories of the Northeastern Peloponnese, Greece","true_value":"A Cross-Comparative Framework to Explore Land Use Histories of the Northeastern Peloponnese, Greece","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 22"}
{"claim_id":"10.3390-heritage8080298-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 22","proposer_value":0,"true_value":0,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 22"}
{"claim_id":"10.3390-heritage8080298-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 22","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 22"}
{"claim_id":"10.1111-arcm.13095-authors","status":"pass","category":"authors","description":"Authors for row 23","proposer_value":"Huet & Levy (2025)","true_value":"Huet & Levy (2025)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 23"}
{"claim_id":"10.1111-arcm.13095-year","status":"pass","category":"year","description":"Publication year for row 23","proposer_value":2025,"true_value":2025,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 23"}
{"claim_id":"10.1111-arcm.13095-title","status":"pass","category":"title","description":"Title for row 23","proposer_value":"Foreword – Archaeometry special issue on chronological modeling","true_value":"Foreword – Archaeometry special issue on chronological modeling","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 23"}
{"claim_id":"10.1111-arcm.13095-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 23","proposer_value":0,"true_value":0,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 23"}
{"claim_id":"10.1111-arcm.13095-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 23","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 23"}
{"claim_id":"10.1098-rsif.2017.0367-authors","status":"pass","category":"authors","description":"Authors for row 24","proposer_value":"Hanson, Ortman & Lobo (2017)","true_value":"Hanson, Ortman & Lobo (2017)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 24"}
{"claim_id":"10.1098-rsif.2017.0367-year","status":"pass","category":"year","description":"Publication year for row 24","proposer_value":2017,"true_value":2017,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 24"}
{"claim_id":"10.1098-rsif.2017.0367-title","status":"pass","category":"title","description":"Title for row 24","proposer_value":"Urbanism and the division of labour in the Roman Empire","true_value":"Urbanism and the division of labour in the Roman Empire","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 24"}
{"claim_id":"10.1098-rsif.2017.0367-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 24","proposer_value":36,"true_value":36,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 24"}
{"claim_id":"10.1098-rsif.2017.0367-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 24","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 24"}
{"claim_id":"10.1093-acprof:oso-9780199562596.001.0001-authors","status":"pass","category":"authors","description":"Authors for row 25","proposer_value":"Bowman & Wilson, eds. (2009)","true_value":"Bowman & Wilson, eds. (2009)","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 25"}
{"claim_id":"10.1093-acprof:oso-9780199562596.001.0001-year","status":"pass","category":"year","description":"Publication year for row 25","proposer_value":2009,"true_value":2009,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 25"}
{"claim_id":"10.1093-acprof:oso-9780199562596.001.0001-title","status":"pass","category":"title","description":"Title for row 25","proposer_value":"Quantifying the Roman Economy","true_value":"Quantifying the Roman Economy","severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 25"}
{"claim_id":"10.1093-acprof:oso-9780199562596.001.0001-citation_count","status":"pass","category":"citation_count","description":"Citation count for row 25","proposer_value":78,"true_value":78,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 25"}
{"claim_id":"10.1093-acprof:oso-9780199562596.001.0001-doi_resolves","status":"pass","category":"doi_resolves","description":"DOI resolves to expected paper for row 25","proposer_value":true,"true_value":true,"severity":null,"fix_hint":null,"source_method":"lit-search.py metadata","source_file":"Findings table row 25"}
```
<!-- END corrections.jsonl -->
agentId: af5308503be5c6e03 (use SendMessage with to: 'af5308503be5c6e03' to continue this agent)
<usage>total_tokens: 105615
tool_uses: 26
duration_ms: 493586</usage>