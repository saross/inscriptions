# Lit-scout VERIFICATION RECORD — point-date MC vs mass-apportionment bias under classification contamination

Date: 2026-06-19
Query: is the "point-date Monte Carlo collapses a mixture-component share under classification
contamination, while mass-apportionment recovers it" effect a named/documented phenomenon?
(inscriptions / LIRE deconvolution paper; C10 (ii) follow-up.)

## Verifier verdict

- Rows verified: **21 / 21 PASS** — 0 fail, 0 unverifiable, **0 corrections required**.
- Method: each DOI individually re-queried via `lit-search.py metadata` (CrossRef primary,
  OpenAlex secondary; Semantic Scholar intermittently HTTP-429 but every row resolved from
  CrossRef). Compared `authors[0]` family name, year, title, citation_count field-by-field.
- High-vigilance re-check (clean 21-row table → re-check, not relax): independently re-ran the
  three rows most prone to silent failure — particle name "van Lieshout" (row 15), diacritic/
  hyphen "Collins‐Elliott" (row 16), highest count Vermunt 1976 (row 8) — all reconfirmed. Row
  10 second-author CrossRef oddity ("Richard Hahn, P.") does not affect the verdict (authors[0]
  = "Xia, Michelle"). The proposer's Guard-A year corrections (Carleton 2021, van Lieshout
  2023, Collins-Elliott 2019, Bevan-Antikythera 2013, Blomberg & Todorov 2025) all held.
- **Report cleared for use.** `⚠ VERIFICATION PENDING` marker removed.

## Headline answer

Yes — the general case is documented well enough to cite, under TWO names in TWO fields, and
the conjunction (our cross-classified time×alignment deconvolution with a noisy class
indicator) is NOVEL:

- **Mechanism — "three-step / classify-analyze plug-in bias"** (latent-class/mixture
  statistics): plugging a point-estimated, MISCLASSIFIED latent assignment into a downstream
  model systematically attenuates the estimate, with the bias governed by classification error.
  Keystone: Bolck, Croon & Hagenaars 2004 (10.1093/pan/mph001, 1083 cites); quantified: Bakk et
  al. 2013 (10.1177/0081175012470644); framed: Bray, Lanza & Tan 2015 (10.1080/10705511.2014.935265).
  This is exactly our θ_conv/θ_gen story from C10 (ii).
- **Archaeological setting — aoristic pointwise-vs-mass critique**: Carleton & Groucutt 2021
  (10.1177/0959683620981700); Roberts et al. 2012 chronological apportioning (10.1016/j.jas.2011.12.022);
  Crema 2012/2025 (10.1007/s10816-011-9122-3, 10.1111/arcm.12984); van Lieshout & Markwitz 2023
  state-estimation (10.1111/sjos.12619).
- **Why mass-apportionment recovers α**: integrate-out / conditional-expectation correction —
  proper-vs-improper imputation (Nielsen 2003, 10.1111/j.1751-5823.2003.tb00214.x) and the
  regression-dilution analogue (Hutcheon et al. 2010, 10.1136/bmj.c2289; Stefanski & Carroll 1985,
  10.1214/aos/1176349741).

Mapping onto our work: point-date sampling = the hard "classify-analyze" plug-in; θ-contamination
= the classification error that drives the bias; mass-based deconvolution = the integrate-out fix.

## Artefacts

- Full cleared report (verbatim proposer draft; verifier made 0 changes):
  `/tmp/lit-scout-drafts/draft-20260619-aoristic-mc-bias.md`
- BibTeX (21 verified entries, CrossRef): `/tmp/lit-scout-bibtex-20260619-aoristic-mc.bib`
- 13 NEW papers to stage to Zotero (8 already held; see "Zotero actions" in the draft).
