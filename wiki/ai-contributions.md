# AI contributions to this project

**Purpose.** Running log of substantive contributions to the project's research programme made by AI collaborators. Maintained per Shawn's research practice of recording AI-driven intellectual contributions transparently, aligned with his RDA AI-disclosure working-group commitments.

**Scope.** Substantive means: methodology proposals, analytical framings, literature-discovery reframings, interpretive moves, research-design suggestions — things that would be attributed as intellectual contribution in a footnote or acknowledgement if made by a human collaborator. Routine execution (running agents, writing boilerplate code, file bookkeeping) is out of scope for this log.

**Conventions.**
- Entries dated.
- Attribution format: `Claude (model Opus 4.7) via Claude Code session <id>`.
- Brief context: what was being discussed when the contribution arose.
- The contribution itself, neutrally described.
- Downstream impact: how the contribution shaped what followed.

---

## 2026-04-23 — Aeneas-partition reframing

**Context.** Discussion of how to correct for editorial-convention artefacts detected in the descriptive profile of LIRE v3.0 (century-midpoint and round-year clusters in the `mid` distribution). Shawn asked: "can Aeneas (re)date inscriptions?" as a potential correction route.

**Claude's contribution.** Claude reframed the question. Shawn's framing assumed Aeneas's predicted dates (mean of the predictive distribution) would be the useful output. Claude observed that using Aeneas's mean to re-date is partly circular — Aeneas was trained on EDH + EDCS + EDR using their editorial-default date labels as training targets, so its predictions will reproduce the convention, not correct for it.

The reframing: use Aeneas's predictive **variance / distribution shape** (not mean) as a content-signal-strength indicator per inscription. High predictive variance ⇒ text is date-uninformative, label carries the signal ⇒ likely editorially-anchored. Low predictive variance ⇒ text has strong independent date signal ⇒ content-verified. Partition the corpus by this indicator and run stratified SPAs.

**Why this matters.** The partition depends on predictive variance, not predictive mean — variance reflects how diffusely the text content pins the date, a latent quantity independent of editorial label frequency. This sidesteps the training-data-circularity that afflicts re-dating uses of Aeneas.

**Downstream impact.** Identified as the basis for a potential follow-up paper (`planning/paper-outlines/aeneas-partition.md`). Noted in `planning/future-studies.md` as FS-1. No paper in our Aeneas-cluster bibliography does this reframing, so the contribution appears to be genuinely novel.

---

## 2026-04-23 — Explicit deconvolution mixture model for editorial-convention artefact

**Context.** Same discussion. Shawn asked what statistical corrections or modelling could de-couple inscription counts from editorial-anchor years.

**Claude's contribution.** Proposed a mixture-model framing:

```
observed_SPA(y) = α · convention_SPA(y) + (1 − α) · genuine_SPA(y)
```

with α estimated from the dataset (e.g., via the midpoint-inflation ratio or a row-level convention-vs-precision classification) and `genuine_SPA` recovered by deconvolution. Claude presented this as one of four ranked mitigation options alongside (i) thresholded SPAs (Shawn's established 2024 practice), (ii) stratified SPAs by convention-vs-precision, and (iii) Bayesian aoristic (via baorista, already on the project roadmap as Decision 3).

**Claude's recommendation.** Given the options, (iv) is the most novel and publishable methodology contribution. Recommended including it as headline methodology in the main SPA paper rather than a separate publication, because it strengthens the main paper without scope-creep.

**Downstream impact.** Recorded in `planning/future-studies.md` as FS-2. After a critical-friend push-back on an earlier four-co-equal-methods plan, **elevated to the primary correction method in the main SPA paper** (per Decision 7 in `planning/decision-log.md`). Not co-equal; it's the headline. Stratification (the nearest-equivalent approach) demoted to appendix as cross-check. Thresholded SPAs (Shawn's 2024 practice) retained as in-body robustness. baorista Bayesian run on a subset and reported as comparative methodology in appendix. FS-0 captures the contingent methods/results split of the main paper with an end-of-Week-1-of-sprint (2026-05-03) commitment deadline — default single combined paper.

---

## Convention

Future entries follow the same structure: Context / Claude's contribution / Why it matters / Downstream impact.

For the main paper and any follow-ups, the acknowledgements section should reference this log (and individual entries where specific contributions were load-bearing for specific claims). The log is committed to the repo and citable alongside the paper's other artefacts at Zenodo deposit time.
