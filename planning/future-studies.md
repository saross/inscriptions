# Future studies — methodology directions not pursued in the current paper

**Purpose.** Ideas identified during the current project that could warrant separate papers or follow-up work. Kept alive per the externalise-or-lose-them rule. Each entry has: origin (when/where raised), contributor attribution (who proposed), current status, trigger for revisit.

## FS-3 — Aoristic-shape sensitivity for Roman epigraphic SPA

**Origin.** 2026-04-25, during methodological-pivot discussion on H1 envelope-test FP control. Shawn raised: "Crema's other work suggests ceramic dates follow trapezoidal distributions rather than uniform — should we test other shapes too?"

**Proposed by.** Shawn (research question); Claude (initial framing of how it integrates with our pipeline).

**Idea.** Aoristic methodology assumes a date-density shape over each row's `[not_before, not_after]` interval. The current paper uses **Uniform** aoristic per Decision 4 (with **trapezoidal** preregistered as a narrow Decision 4 sensitivity for selected subsets). Crema 2012 (*J. Archaeol. Method Theory* 19(3)) argues the appropriate shape depends on the artefact-class production curve: ceramics typically follow a trapezoidal curve (gradual ramp-up, plateau, ramp-down of production); coinage follows different shapes (issue-event spikes); inscriptions of different types may have different curves still. Crema 2025 (*Archaeometry*; baorista) handles arbitrary shapes within a Bayesian framework.

**For Roman epigraphy specifically.** No published study has systematically estimated the right shape for Latin epigraphic SPA. Reasonable hypotheses: military diplomas (sharp, one-off issuance dates) ⇒ near-uniform across narrow ranges; funerary / dedicatory inscriptions (palaeographic / formulaic dating) ⇒ possibly peaked or skewed; certain chronologically-constrained types (e.g., honorific inscriptions to specific emperors) ⇒ may peak at the relevant reign with ramps either side.

**Why it matters for our work.** Aoristic shape is upstream of every SPA result. If the true shape is trapezoidal but we use uniform, our SPAs are systematically distorted (peaks broadened, edges over-smoothed). Substantive conclusions on temporal patterns depend on this assumption being approximately right. Independent of the FP-control issue we're resolving in H1 v2 (forward-fit / non-parametric envelope methods).

**Standalone-paper potential.** Yes. Methodological + empirical. Outline:
1. Prior-art-scout sub-task: confirm the absence of published systematic shape-estimation for Latin epigraphic SPA.
2. Theoretical: derive the SPA expectation under different per-row shapes (uniform, trapezoidal, peaked-at-centre, edge-skewed).
3. Empirical: estimate per-inscription-type shape priors from external evidence (LIRE's `type_of_inscription_clean` × external archaeological / palaeographic dating studies).
4. Application: re-run the current paper's main analyses under (i) uniform [primary], (ii) per-type-empirical shape, (iii) trapezoidal [Crema-default]. Quantify how thresholds, mixture-corrected SPAs, and population-scaling β change under each.
5. Could integrate with FS-1 (Aeneas-partition): high-content-signal inscriptions may require different shape priors than editorially-anchored ones.

Target venues: *Journal of Archaeological Method and Theory* (where Crema 2012 lives), *Archaeometry*, *Journal of Computer Applications in Archaeology*. Length: 6–8k words.

**Prerequisites.**
- Main SPA paper submitted or in press (so the aoristic-shape question can be motivated by reference to a working pipeline).
- Or: integrated as a more substantial Decision 4 sensitivity in the current paper if scope permits (low priority — main paper already has H2 mixture as the substantive methodological contribution).

**Revisit trigger.** After main paper submitted; could be 2026 Q4 / 2027 Q1. Or earlier if reviewers of the main paper specifically push on the uniform-aoristic assumption.

**Risk that would change recommendation.** External-evidence shape priors prove unrecoverable for Latin inscriptions (no reliable per-type chronological independent data), reducing the empirical contribution to a thought-experiment.

**Cross-link.** Current paper's narrow trapezoidal sensitivity (prereg §3, Decision 4) is the seed for this future work; FS-3 expands the systematic comparison.

---

## FS-1 — Aeneas predictive-distribution-variance as corpus-partitioning tool

**Origin.** 2026-04-23, during discussion of how to correct for editorial-convention artefacts in SPA on LIRE.

**Proposed by.** Claude (reframing of Shawn's question "can Aeneas re-date inscriptions?"). Shawn asked the question; Claude proposed the specific reframing that treats Aeneas's predictive *variance* (not mean) as the signal of interest, thereby sidestepping the training-data circularity that would afflict a re-dating use.

**Idea.** Aeneas (Assael et al. 2025, *Nature*) outputs a probability distribution across 160 decades for each Latin inscription. Rather than using the mean as a re-date (which is circular — Aeneas was trained on EDH+EDCS+EDR with their editorial-default labels), use the *shape* (variance, entropy, IQR) of the predictive distribution as a content-signal-strength indicator. High-variance predictions ⇒ inscription text is date-uninformative and the LIRE label is carrying most of the date information (likely editorial default). Low-variance predictions ⇒ text has strong independent date signal.

Partition the corpus by predictive-variance quantile. Run stratified SPAs on each partition. If partitions produce similar SPAs, editorial convention is not driving the signal; if they differ substantially, the corpus-level SPA has editorial contamination specifically in the high-variance stratum.

**Why this sidesteps circularity.** The partition depends on predictive variance, not predictive mean. Aeneas learning "AD 150 is a common label" from training doesn't bias its *variance* estimate — variance reflects how diffusely the text content pins the date, which is a different latent quantity from how often editors chose a given label.

**Standalone-paper potential.** Yes — this is genuinely novel (no paper in the computational-sibling bibliography does it). Target venues: NLP4DH or LaTeCH (ACL workshops), *Journal of Digital History*, *Digital Scholarship in the Humanities*. Length: 5–7k words. Outline at `planning/paper-outlines/aeneas-partition.md`.

**Prerequisites.**
- Aeneas model weights available (via `google-deepmind/predictingthepast`).
- Inference feasible at LIRE scale (~182k rows) on available GPU hardware — sapphire's 16 GB VRAM likely sufficient, but batch-size testing required.
- Main SPA paper submitted or in press (so we can cite it as the motivating corpus-level analysis).

**Revisit trigger.** After main paper submitted; before Paper A/B+ cycle begins. Could be a natural Paper B for 2026 Q3.

**Risk that would change recommendation.** Aeneas inference proves infeasible at scale, or test-of-principle run (on a sample) shows predictive variance doesn't separate content-strong from editorially-anchored inscriptions (i.e., Aeneas's variance doesn't behave as hypothesised).

---

## FS-0 — Conditional: split main paper into methods paper (JAMT) + results paper

**Origin.** 2026-04-23, during scoping discussion on how heavily to develop the deconvolution-mixture methodology in the main paper.

**Idea.** The current plan is to cover four complementary deconvolution approaches in the main SPA paper: (1) thresholded SPAs (Shawn's 2024 practice); (2) stratified SPAs by convention-vs-precision classification; (3) baorista Bayesian sensitivity (Crema 2025); (4) explicit deconvolution mixture model. Light-to-medium treatment in the body of the paper, detailed development in appendices / supplemental materials.

**Contingency.** If, in the course of writing, the methodological contributions turn out to be substantial enough to warrant independent publication, split into:

- **Methods paper** — target JAMT. Title direction: "Porting radiocarbon summed-probability analysis to epigraphic corpora: methodological adaptations and editorial-convention deconvolution." Covers the four deconvolution approaches + simulation validation + application notes.
- **Results paper** — target JAS or *Journal of Urban Archaeology*. Title direction: "The epigraphic habit quantified: summed probability analysis of Latin inscriptions across the Roman Empire." Applies the methodology and interprets substantive findings.

**Not a too-thin-salami-slicing risk** because:
- The methods paper is generalisable — applies to any editor-mediated aoristic corpus, not only inscriptions. Generates its own citation surface (radiocarbon SPD community + digital humanities).
- The results paper stands alone as a substantive archaeological-historical contribution even without the methods details (which get cited rather than restated).

**Revisit trigger.** **End of Week 1 of paper sprint (Sunday 2026-05-03)** per Decision 7 — no later. If methodology content exceeds 3,000–4,000 words of novel material during drafting, OR if deconvolution + baorista produce substantively different results (making the methodology story richer), OR if the Aeneas-partition outline suggests a natural companion submission, split becomes viable.

**Default if unresolved.** Single combined paper. The point of the Week-1 commitment is to prevent scope drift; "we're still deciding" is not an acceptable state past that date.

**Preliminary signals to watch for** (per Decision 7):
- Deconvolution-mixture pilot run on a province — if clean results at first attempt, methodology stays compact; if substantial tuning needed, expands toward split threshold.
- baorista install cost — if non-trivial (C++ / NIMBLE pain on sapphire), comparison may need to downgrade to citation-with-rationale.
- Literature prior art — how did Timpson/Crema structure their Neolithic SPD work (methods-first, results-first, combined)? Field convention informs our default.

---

## FS-2 — Explicit editorial-convention deconvolution mixture model

**Origin.** 2026-04-23, critical-friend review of correction options for the century-midpoint / round-year editorial artefacts detected in the LIRE descriptive profile.

**Proposed by.** Claude, during the critical-friend review of statistical-correction options for the mid-midpoint-inflation artefact.

**Idea.** Model the observed aoristic SPA as a mixture:

```
observed_SPA(y) = α · convention_SPA(y) + (1 − α) · genuine_SPA(y)
```

where `convention_SPA` is a parameterised shape representing the editorial-default SPA (e.g., uniform-over-century slabs at each century where century-default rows concentrate), and `genuine_SPA` is the demographic/cultural signal we want to isolate.

Estimate α from the dataset via the midpoint-inflation ratio, or via a mixture-model likelihood fit on the row-level convention-vs-precision classification. Once α is estimated, invert to recover `genuine_SPA`.

**Current-paper status (revised 2026-04-23 after critical-friend push-back).** **Elevated to primary correction in the main SPA paper** per Decision 7. Not one-of-four-co-equal; it's THE headline correction, with three supporting approaches:

- **In body**: thresholded SPAs as robustness (Shawn's 2024 practice).
- **In appendix**: stratified SPAs by convention/precision classification (cross-checks the mixture's deconvolved SPA).
- **In appendix**: baorista Bayesian (Crema 2025) run on a representative subset — comparative methodology not a throwaway citation.

Rationale for the architecture change: stratified and mixture answer largely the same question with different mechanics; running both as co-equal primary methods invites redundancy. Mixture is more novel, produces a clean counterfactual, has a better narrative. Stratified becomes validation not presentation.

**Simulation validation**: main-paper treatment includes a synthetic-data test that the mixture recovers a known α. Heavier methodology validation reserved for a methods-paper split per FS-0 if that path triggers.

**Revisit trigger.** Decision reassessed at end-of-Week-1 of paper sprint (Sunday 2026-05-03) per Decision 7: is methodology content substantial enough to split? Default remains single combined paper.

---

## Convention for this file

- Entries numbered FS-N.
- Each entry includes origin (when/where), contributor attribution, current status, revisit trigger, and a clean framing of the idea.
- When an entry is "graduated" (i.e., promoted to main-paper scope, started as separate paper, or explicitly abandoned), note the graduation with date and outcome; do not delete the entry.
- When contributor attribution names Claude: the factual source of the idea matters for Shawn's research-record practice (see `planning/ai-contributions.md`).
