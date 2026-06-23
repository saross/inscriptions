# Outline: Aeneas-partitioned SPA paper (working title)

**Working title.** "Disentangling text signal from editorial convention in Latin inscription chronologies: an Aeneas-based partitioning approach"

**Target venue options (ranked).**
1. *Journal of Digital History* (De Gruyter) — precedent: Heřmánková, Kaše, Sobotková 2021 sits here; natural fit for the corpus + methodology.
2. NLP4DH (ACL workshop) — shorter form; precedent: Gong, Gero, Schiefsky 2025 (Latin-BERT applications).
3. *Digital Scholarship in the Humanities* (Oxford) — precedent: Cullhed 2025 (Llama vs Ithaca).
4. LaTeCH-CLfL (ACL workshop) — lower barrier, faster turnaround.

**Length target.** 5,000–7,000 words (journal) or 4,000–5,000 (workshop).

**Status.** Conceptual outline only. Prerequisites block execution — see §6.

---

## 1. Argument in one sentence

*Aeneas's predictive-distribution variance partitions the LIRE corpus into text-signal-strong and editorially-anchored subsets, enabling a robust check of whether demographic signal in Latin epigraphic summed-probability analyses survives control for editorial-convention contamination.*

## 2. Contributions

1. A novel use of Aeneas that sidesteps the training-data-circularity problem: using predictive *variance* (not mean) avoids the issue that Aeneas learned editorial-default date labels as training targets.
2. An empirical test of whether the corpus-level SPA signal on LIRE (from the main paper) survives the text-signal-strong stratum alone.
3. A generalisable methodology applicable to any ML-attributed chronological corpus where editorial convention may bias labels — extends naturally to Greek epigraphy via Ithaca, and to other attributed corpora with analogous ML tooling.

## 3. Section structure (target ~6,000 words)

**1. Introduction** (~800 words)
   - The editorial-anchor artefact in Latin inscription corpora — what it is, why it matters for quantitative history, reference to main paper.
   - Aeneas and Ithaca (brief) — what they do, their training data, their reported performance.
   - The circularity problem when using Aeneas to re-date corpora Aeneas was trained on.
   - Contribution: variance-based partitioning as a route around circularity.

**2. Background and related work** (~1,000 words)
   - Aoristic analysis in archaeology (Ratcliffe 2002; Crema 2012; Crema & Bevan 2021).
   - SPA applied to Latin epigraphy (main paper; Glomb/Kaše/Heřmánková 2022).
   - Aeneas methodology (Assael et al. 2025) and its Ithaca precursor (Assael et al. 2022).
   - Cullhed (2025) on Llama vs Ithaca — the one existing comparative benchmark.
   - Training-data circularity as a methodological hazard in ML-assisted corpus analysis.

**3. Method** (~1,500 words)
   - Inference on LIRE (or LIST) using the published Aeneas model.
   - Per-inscription predictive distribution over 160 decades.
   - Derivation of the content-signal-strength indicator: predictive entropy, IQR, or variance on the decade distribution (test multiple; preregister primary).
   - Partition: quartiles or fixed-threshold splits of the indicator.
   - Stratified SPAs on each partition.
   - Comparison tests: KS + Cramér-von Mises between partition SPAs; Cliff's delta effect sizes with BCa CIs.
   - Sensitivity analyses: partition threshold, entropy vs IQR vs variance, sampling sub-corpora.
   - Preregistration: the comparison tests + decision rules + sensitivity space, all pre-specified on OSF before inference runs.

**4. Results** (~1,500 words)
   - Aeneas inference execution (n=LIRE, compute cost, validation against held-out labels where available).
   - Partition composition: how rows distribute across text-signal strata; correlation with LIRE's `date_range` (expected: low-variance Aeneas predictions correlate with narrow LIRE ranges).
   - Stratified SPA plots with envelopes.
   - Comparison statistics: do partitions produce different SPAs? Where (which centuries/regions) most?
   - Targeted check: are the century-midpoint artefacts attenuated in the text-signal-strong partition? (predicts: yes, confirming the editorial-convention reading.)

**5. Discussion** (~800 words)
   - What the partition findings imply for the main paper's SPA claims.
   - Generalisation to Greek epigraphy (Ithaca), other ML-attributed corpora.
   - Limitations: Aeneas's own training-data bias at the variance level (is variance genuinely independent of convention? — test empirically).
   - Open question: does the partition approach work for less-scale ML tools (e.g., Latin-BERT of Ceriotti et al. 2025)?

**6. Conclusion** (~400 words)
   - Variance-not-mean reframing as a general methodology pattern for bias-corrected use of ML attribution.
   - Corpus-specific finding: what we learned about LIRE's editorial-convention contamination.

## 4. Figures planned

- Figure 1: schematic of the circularity concern (Aeneas training → Aeneas inference on training-like data).
- Figure 2: example inscriptions at three variance levels (low, medium, high), showing text + Aeneas predictive distribution shape.
- Figure 3: distribution of predictive variance across LIRE.
- Figure 4: stratified SPA comparison (overlay of text-signal-strong vs editorially-anchored).
- Figure 5: artefact attenuation at century midpoints across strata.

## 5. Prerequisites

- Main paper submitted or in press (citable).
- Aeneas model weights downloaded and inference pipeline stood up. Repo: `google-deepmind/predictingthepast`.
- GPU: sapphire's 16 GB VRAM likely sufficient for Aeneas inference at batch size ≥ 1; batch-size testing required. If insufficient, zbook (96 GB VRAM) handles any batch size.
- Preregistration on OSF before running inference.

## 6. Timeline estimate

- Total effort: 3–6 weeks of focused work (not full-time).
- Longest single blocker: standing up the Aeneas inference pipeline reliably at LIRE scale. Literature suggests this is a few days of setup + a few hours of compute.
- Target submission window: 2026-Q3 (post-main-paper).

## 7. Risks

- **Partition fails to separate signal** — if Aeneas predictive variance doesn't correlate with LIRE `date_range` or with text length/informativeness, the method doesn't work. Mitigation: validate on a pilot sub-corpus before committing.
- **Results are null** — partitions produce indistinguishable SPAs. This IS a finding (editorial convention isn't driving the signal) but is a weaker paper. Workshop venue becomes more appropriate than journal.
- **Aeneas's variance is itself contaminated** by editorial convention, because Aeneas may have learned to predict low variance on frequent editorial-label rows. Testable: check whether predictive variance correlates with LIRE's convention-dated vs precision-dated flag. If it does, variance isn't as circularity-free as claimed.
- **Access / cost** — Aeneas model weights and inference code presumed available per GitHub repo; confirm before committing.

## 8. Authorship and acknowledgements

- Primary: Shawn Ross (TBD; depends on collaboration).
- Adela Sobotková as co-author (standing arrangement on the inscription SPA work; she's been in the SDAM team's conceptual territory throughout).
- AI contribution attribution (per `planning/ai-contributions.md`): the variance-based reframing was proposed by Claude during a critical-friend review on 2026-04-23; the research design and execution are Shawn's and collaborators'.

## 9. Related work to revisit before drafting

- Aeneas paper full-text (PDF, not just abstract) — check what performance metrics it reports and whether calibration evaluation (variance → uncertainty) is already done.
- Cullhed 2025 for what comparative evaluation looks like in this space.
- Calibration of neural classifier confidence — methodological literature outside archaeology (Guo et al. 2017 on calibration of modern neural networks). Would be a key citation for the variance-as-uncertainty claim.
