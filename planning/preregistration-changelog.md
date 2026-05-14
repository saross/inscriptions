---
priority: 2
scope: in-stream-reference
title: "Preregistration — Change Log and Editorial Commentary"
audience: "Shawn, Adela, future CC instances; OSF reviewers if useful as provenance"
status: living; maintained until OSF lodgement, then superseded by an errata document
started: 2026-05-14
---

# Preregistration — Change Log and Editorial Commentary

## Purpose

This document is the revision history and editorial commentary for
`planning/preregistration-draft.md`. The preregistration itself is kept as a
clean representation of its current final state — it carries no amendment trail,
no cross-references to numbered decisions or planning documents, and no
working-document furniture. All of that provenance lives here instead.

**Scope boundary.** This log is maintained **up to OSF lodgement**. After
lodgement, the preregistration is a fixed public record, and any subsequent
change is tracked in a separate **errata document** (post-registration
amendments are governed by OSF's own amendment mechanism and the contingency
rules in the preregistration's "Planned deviations and contingencies" section).

**Relationship to the decision log.** Methodology and scope *decisions* — the
"why did you do X?" auditable answers — live in `planning/decision-log.md` as
ADR-style entries. This change log records *what changed in the preregistration
document and when*; where a change implements a decision, the entry names the
decision-log entry. The two are complementary: the decision log is the
reasoning, this is the document history.

---

## Pre-history — draft evolution before the lodgement pass (2026-04-24 → 2026-04-27)

Reconstructed from git history of `planning/preregistration-draft.md`. Commit
hashes are the re-verifiable anchors.

### Initial draft (2026-04-24)

- `7ae3e93` — OSF preregistration draft created (open-ended four-field format,
  monolithic single document).
- `228a8c6` — resolved the H1 simulation protocol parameters.
- `c901aae` — applied the Glomb, Kaše & Heřmánková (2022) reframing of the
  Antonine test as exploratory replication; confirmed LIRE subset-filter
  feasibility (military-administration and Asclepius-cult subsets).
- `630fdc4` — fixed the H3a Bayesian NBR software choice: `pymc` primary,
  `brms`-via-R shadow.
- `f18db5b` — fixed the H3a priors and the posterior-predictive-check suite.
- `378e708` — fixed the Moran's I spatial-weights construction (k-NN, k = 8
  primary, k = 5 / k = 10 sensitivity).

### Round-1 amendments (2026-04-25)

- `efc6e07` — applied five amendments arising from the H1 simulation plan
  review: permutation-envelope primitive wording, effect-shape pre-specification,
  shape-bracket handling, CPL-3 plus exploratories, and `tempun` substitution.
  The amendment proposals were drafted and recorded in
  `preregistration-amendments-2026-04-25.md` (commits `1427d88`, `80b3f4a`,
  `efc6e07`); that document is now archived (see "Archived documents" below).

### Round-2 forward-fit pivot (2026-04-26 → 2026-04-27)

The H1 v1 simulation surfaced catastrophic false-positive-rate inflation in the
parametric-null Monte Carlo envelope. The methodological response was the
forward-fit pivot, recorded as decision-log Decisions 8, 9, and 10.

- `426a2f6` — §3 rewritten for forward-fit nulls in true-date space; added the
  `brms` stanvar shape-prior detail.
- `3e59aa6` — §4 Phase 1 rewritten for the synthetic-data-from-specified-null
  data-generating process, forward-fit, and the `min_n_unreachable` convention.
- `8de6d7e` — §6 effect-size table updated with the H1 v2 numerical thresholds;
  the 20%/25y bracket recorded as a hard-test boundary.
- `c3026bd` — §8 open-design-decisions list updated: H1 thresholds resolved,
  multiple-comparison family resolved.
- `989c084` — status field and §12 provenance updated for the round-2 pivot.
- `b68b4a2` — round-2 cross-references tightened; H3b family-size arithmetic
  reconciled.
- `df6593b` — added the Crisis-of-the-Third-Century exploratory H3b test and the
  H3a variance-partition exploratory analysis.
- `7aebcec` — added the §5 small-N city-level temporal-trajectory estimation
  (Layers A and B plus the aggregate diagnostic).
- `dd17afb` — added the §5 province-scale parallel methodological output and the
  FS-4 follow-up paper.

---

## Editorial pass for lodgement (2026-05-14)

A single editorial pass to bring the draft to a clean, lodgement-ready final
state. Adela Sobotková delegated preregistration review to Shawn; this pass
incorporates that review. Changes, each with its rationale:

1. **§4.1 — Rome statistics added.** Stated Rome's inscription count (65,435),
   its share of the filtered corpus (36.2%, or 46.5% of inscriptions assigned to
   a Hanson city), and the Rome-excluded total (115,174). Rationale: the
   Rome-exclusion was asserted without quantifying what is excluded; the figures
   make the scope of the exclusion transparent. Counts computed directly from
   `archive/data-2026-04-22/LIRE_v3-0.parquet` under the §4.1 filter, which
   reproduces the stated 180,609-row total exactly.

2. **H1.1 and the baorista material updated to current state.** H1.1 reworded to
   reflect that the simulation is complete and the thresholds are determined and
   tabled in §6 (previously "to be determined"). The baorista exploratory
   analysis and its contingency updated from "if compilable on sapphire" to
   reflect that baorista, brms, NIMBLE, and cmdstanr are installed and
   smoke-validated on sapphire. Rationale: the draft promised work as
   conditional that has since been done.

3. **Plain-English methods walkthrough added before §3.** A new explanatory
   subsection narrating the analysis pipeline in plain terms, placed before the
   technical §3, with a header noting that §3 is the binding specification.
   Rationale: archaeology-journal reviewers routinely require statistical
   approaches to be explained in plain English; a separate walkthrough provides
   the explanation while keeping the binding technical text precise and
   unambiguous.

4. **Uncertainty-quantification subsection added.** A new subsection presenting,
   per analysis, how confidence or credible intervals are computed: Wilson score
   intervals for H1 detection rates; Monte Carlo percentile bands plus the
   global p-value for permutation envelopes; nonparametric row bootstrap for the
   mixture-model α and the H2.3 Pearson r; posterior credible intervals for the
   H3a Bayesian NBR quantities and the H3c residuals; conditional permutation
   inference for Moran's I. Rationale: the draft did not present uncertainty
   characterisation systematically; for the Bayesian components, posterior
   credible intervals replace bootstrap intervals.

5. **Information-infrastructure vs complexity-markers framing cleaned up.**
   Both theoretical framings presented as worth exploring and discussing, with
   conference feedback treated as critique to inform further exploration rather
   than as the deciding word.

6. **Letter-count analysis reframed.** Preregistered as summed
   `clean_text_conservative` letter counts (Latin A–Z filter, Greek excluded),
   with `clean_text_interpretive_word` available as a sensitivity check.
   Hanson (2021, p. 142) cited correctly as a foil: he identifies inscription
   length as methodologically desirable but rejects it on fragmentation grounds;
   the project takes the opposite view. The analysis itself is attributed to the
   2024 seminar exploratory work, its actual documented origin. Rationale: the
   prior attribution of the letter-count *recommendation* to Hanson 2021 was an
   error (verified against the primary PDF — Hanson explicitly counts
   inscriptions and does not attempt length estimation). The conservative text
   variant is the more defensible choice for this paper because the interpretive
   variants embed modern editorial restoration practice, which is precisely the
   editor-dependent variation the mixture model exists to deconvolve.

7. **Resolved items, round-2 amendments, and the open-design-decisions list
   folded into the main text.** The §8 "Open design decisions" list, the
   "Additional items resolved" block, and the §12 "Round-2 amendments applied"
   block removed; their substance folded into the relevant main-text sections.
   The multiple-comparison single-null choice retained as a pre-specified
   analysis-time rule within the confirmatory-analysis section. Rationale: this
   is the first lodged preregistration, so the document should read as a single
   clean final state, not as a draft with an amendment trail.

8. **Decision, planning-document, run-directory, commit-hash, and observation
   cross-references stripped.** All "Decision N", `planning/...`, `runs/...`,
   commit-hash, and "Obs N" references removed from the preregistration body;
   their substance inlined so the document is self-contained. The provenance
   linkage lives in `decision-log.md` and in this change log. Rationale: a
   lodged preregistration should be a clean, self-contained representation of
   its final state.

9. **"Earlier / first preregistration" framing removed.** This is the first
   lodged preregistration; references implying prior preregistrations or
   revisions removed. Internal draft-revision history is recorded here, not in
   the preregistration body.

10. **Sprint references updated.** "Paper-sprint Week 1" references updated to
    the fortnightly sprint of 11–24 May 2026.

11. **§12 roles converted to CRediT taxonomy.** Author contributions expressed
    using the Contributor Roles Taxonomy (CRediT) rather than position titles
    such as "PI". Rationale: CRediT is more substantive and position-title
    conventions vary by country.

12. **§12 funding and competing interests stated.** Recorded as no funding and
    no competing interests.

13. **Repository named.** The public repository `github.com/saross/inscriptions`
    named in §9.

14. **Target-conference and target-journal-venue specifics removed.** The
    preregistration no longer names a target conference or journal. The
    submission-venue decision (JAMT) is recorded in `decision-log.md` as a
    committed decision; naming a venue in the preregistration is unnecessary and
    premature.

15. **Software list updated.** §9 updated to reflect the packages now installed
    and smoke-validated on sapphire: `pymc`, `cmdstanpy`, `baorista`, `brms`,
    `nimble`, `cmdstanr`, and supporting R packages, with versions.

16. **Deviations and contingencies updated.** §7 refreshed for current state:
    H1 simulation complete, baorista installed (its contingency no longer live),
    Adela's review delegated to Shawn.

17. **Working-document furniture removed.** The "Review pointers for Shawn"
    section removed; the frontmatter simplified to a minimal clean header; the
    format note trimmed to drop the TBD-marker reference.

---

## Archived documents

- `preregistration-amendments-2026-04-25.md` — the round-1 amendment proposals
  drafted from the H1 simulation plan review. All five amendments were applied
  to the draft in commit `efc6e07` (2026-04-25). Archived to
  `archive/planning/` during the 2026-05-14 lodgement pass; its content is
  superseded by the "Round-1 amendments" entry in the pre-history above.
