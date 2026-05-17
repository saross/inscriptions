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

## Adversarial-review-driven revision (2026-05-14 → 2026-05-16)

A multi-day cycle of structured adversarial review, targeted re-verification
of factual claims, empirical diagnostics, and a comprehensive rewrite. This
phase moved the preregistration from "draft for lodgement (2026-05-14)" — the
editorial-pass state — to the current draft (2026-05-16), incorporating six
new decisions (Decisions 12–17, recorded in `decision-log.md`), eleven
smaller calls (bucket (c) of the triage), and around twenty mechanical or
clarity fixes (bucket (d)).

### Dual adversarial review (2026-05-14)

Two fresh-context Explore agents reviewed the post-editorial-pass
preregistration in parallel: one with a statistical-methodology focus, the
other with a domain legibility / output-value focus. Both ran on Opus;
neither had access to the other's findings; both applied a shared
preregistration-failure-mode rubric (researcher degrees of freedom;
hypothesis → test → decision rule; does-the-analysis-answer-the-question;
logical consistency; clarity). Both concluded *not yet lodgeable, all
fixable*.

The two reviews converged on six consensus blocking findings:

1. H1 mis-filed as a confirmatory hypothesis (it is a completed methods
   step with no live decision rule).
2. H3b's decision rule near-unfalsifiable ("at least one bracket at one or
   more of 12 cells"); the subset × window family was never enumerated.
3. The Antonine test labelled confirmatory in §6 ("≥ 50 % dip") but
   exploratory in Field 3 / §4 — a direct internal contradiction.
4. H3b's Holm-Bonferroni family-size choice (12 vs 6 cells) deferred to
   "lock time" — a researcher degree of freedom.
5. The primary research question answered only by an exploratory analysis
   (the variance partition was filed under §5 exploratory).
6. H2.2's "local neighbourhood mean" undefined — controls the H2.2 pass /
   fail.

Plus serious single-agent findings: the variance partition is statistically
mis-specified (ignores fixed–random covariance); H3c's capitals test runs
a frequentist *t*-test on Bayesian posterior quantities and ignores spatial
autocorrelation; H2.1 is a non-hypothesis (α > 0 is already known from the
measured spikes); Moran's I decision rule inconsistent across three
sections; H2 has no ground-truth validation (the "Phase 2 validates the
mixture model" overclaim).

### Triage and bucket-(c) resolutions (2026-05-15)

Findings were sorted into four buckets: (a) superseded by Decisions 12–17;
(b) statistician questions for the planned consultation; (c) smaller
calls needing Shawn's input; (d) mechanical / clarity fixes. Bucket (c)
— the smaller calls — was worked through one at a time:

1. **H2.2 "local neighbourhood mean" defined.** ±25-year window (5 bins
   each side), excluding the midpoint bin, computed on the corrected
   `genuine_SPA` values (not O/E ratios). Bracketing variants reported
   alongside as a diagnostic (shoulder-excluded; ±15 y and ±35 y widths).
2. **H3c-spatial qualitative-map clause dropped (Decision 16).** The
   clause attributed a regional residual pattern to Hanson 2021 that
   re-verification confirmed is not in the paper (see below). H3c-spatial
   reduces to Moran's I clustering only.
3. **Editorial-convention-hierarchy specification empirically grounded
   (Decision 17).** A five-test diagnostic run (committed at
   `runs/2026-05-15-editorial-convention-hierarchy/`) established the
   hierarchy's structure.
4. **Trapezoidal aoristic sensitivity scoped.** Run on every H3-eligible
   (level × subset) combination plus the full-empire SPA; convergence
   criterion Pearson *r* ≥ 0.95.
5. **Crisis-of-the-Third-Century window arithmetic corrected.** AD 235–284
   inclusive is 50 years under inclusive-Roman counting (the dominant
   convention in LIRE's date encoding), not 49 years subtractively. Window
   reconciles with the ≥ 50-year bracket.
6. **H3c residual classification clarified as descriptive.** The ±95 %
   CI labelling is narrative only; the confirmatory H3c tests use
   continuous posterior residuals (sidesteps the multiple-comparison
   concern raised in the review).
7. **Proxy-framing scoping sentence added.** Field 2 (Description) and §5
   theoretical-framing item now explicitly state that the substantive
   interpretive question — what inscriptions proxy — is out-of-prereg
   scope.
8. **Pre-lodgement state attestation added** (§8). As of lodgement, no
   confirmatory analysis preregistered here has been executed on LIRE
   v3.0. Prior exploratory frequentist regressions on v3.0 are documented
   in the project repository and inform prior expectations but are not
   confirmatory tests.
9. **Title shortened.** The longer subtitle form dropped in favour of the
   shorter form: "Mixture-corrected SPAs of Latin inscriptions against
   Hanson urban population estimates: a preregistered three-phase
   analysis."
10. **H3a sample size clarified.** The Bayesian NBR uses all ~ 815
    Hanson-matched cities (Rome-excluded); the Phase 1 ≈ 1,549-inscription
    urban-area threshold gates per-city *time-series* analyses, not the
    cross-city regression.
11. **FP-calibration anchor.** The Phase 1 false-positive range
    `[0.007, 0.049]` across 96 zero-effect cells is anchored generically
    via a reproducibility statement in §8 of the preregistration (Phase 1
    code, seed 20260425, and outputs are committed to the public
    repository) rather than via a specific `runs/...` cross-reference in
    the prereg body. The specific audit-trail anchor: simulation outputs
    at `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`,
    pipeline code in `runs/2026-04-25-h1-simulation/code/`, commit
    `00aceb4` ("feat(runs/h1): H1 v2 FINAL — full preregistered precision
    (1000/1000)"), random seed `20260425`.

### Hanson 2021 attribution re-verification (2026-05-15)

While working through bucket (c) item 2, the H3c qualitative-map clause
("over-production concentrated in Italy and along the Rhine / Danube
frontier; under-production scattered in Britannia, Gaul peripheries, and
other western edges of the Empire") attributed to Hanson 2021 was put to
a fresh-context Explore agent for verification against the PDF. The
agent's finding — that Hanson 2021 does *not* claim this regional pattern,
and on the contrary explicitly states "there does not seem to be any
obvious pattern" (p. 147) and that sites from different regions are
"evenly scattered" (p. 148) — was confirmed by a second consolidated
re-verification (also fresh context).

All other Hanson 2021 attributions in the prereg verified exactly:
β = 0.672 mean exponent (Table 7.3, p. 146); Moran's I = 0.046 with
z = 4.571 and *p* < 0.0001 on residuals; Moran's I = −0.006 with
*p* = 0.282 on raw counts (Table 7.4, p. 148); provincial-capital mean
residual 0.43 vs ~ 0.06 for *coloniae* / *municipia* (p. 148); Rome
excluded as extreme outlier (Table 7.3 caption, p. 146); ArcGIS Moran's I
tool (p. 145); letter-count rationale (p. 142).

A second mischaracterisation was caught by the same re-verification: SR1's
"polity × century resolution" phrasing for Hanson 2021 — Hanson works at
*site* level with cumulative inscription counts, not polity × century.
SR1 rewritten.

A subsequent library scan (all 8 Hanson items in the SDAM-AU group
library plus the 22-item `roman_demography` collection; PDF abstracts
read where Zotero metadata was empty) confirmed no Hanson-corpus paper
makes an explicit inscription-residual regional claim. Decision 16
commits to dropping the clause from the confirmatory rule.

The discovery of two confabulated Hanson 2021 attributions in one paper
triggered a scheduled pre-lodgement citation audit of the full
preregistration (Task #21 in the project task tracker).

### Editorial-convention-hierarchy diagnostic (2026-05-15)

A five-test diagnostic was run to resolve bucket (c) item 3 (the
undefined "editorial-convention-hierarchy test"). The run is committed
at `runs/2026-05-15-editorial-convention-hierarchy/`; full report at
`outputs/REPORT.md`. Five tests across the filtered LIRE v3.0 corpus
(180,609 rows): top-N endpoint frequencies; hierarchical O/E by tier;
trailing-two-digit histogram; reign-boundary specific test; convention-
text labelled subset.

The diagnostic surfaced a *conceptual correction* to the preregistration's
prior artefact framing. The dominant editorial convention is
**inclusive-Roman century counting** — 54.5 % of all `not_before` values
end in `01`, and 53.0 % of all `not_after` values end in `00`. The
previously-reported century-midpoint inflation at AD 50 / 150 / 250 / 350
is a *derivative* effect of this endpoint rounding (intervals like
`[1, 100]` and `[101, 200]` deposit aoristic mass on midpoint years). The
Bayesian-mixture `convention_SPA` shape is now structured to reflect the
endpoint-rounding mechanism with three tier components (century,
half-century, reign-related), recorded as Decision 17.

Tier ranking (combined endpoints, geometric-mean O/E at σ = 20-year
baseline): century-incl-start 20.28; century-incl-end 18.34;
century-midpoint 10.16; half-century-incl-start 2.44; reign-related 0.75
overall (with 13 of 39 reign-boundary years Holm-significant);
sub-century tiers (quarter-century, decade, lustrum) all below baseline.

### Comprehensive rewrite (2026-05-16)

A single comprehensive rewrite of `preregistration-draft.md` implementing
Decisions 12–17, all bucket (c) resolutions, and the bucket (d)
mechanical and clarity fixes. Headline changes:

- **Primary research question rescoped** (Decision 12): spatial only,
  within-province, focused on the population-attributable variance
  fraction.
- **H3a respecified** (Decision 12): Bayesian within-between (Mundlak)
  negative-binomial regression. Confirmatory estimand is the
  within-province population-attributable variance fraction; falsifiable
  rule is "posterior 95 % CI excludes 0.10."
- **H2 restructured** (Decision 14): Bayesian mixture model, validated by
  a pre-specified recovery simulation (the new H2.1 confirmatory
  hypothesis). H2.2 / H2.3 / H2.4 honestly relabelled as supporting
  consistency / robustness checks on real data, not validation in their
  own right.
- **H3b recast as pre-specified exploratory** (Decision 15): Antonine
  and Crisis windows are the two pre-specified probes; no pre-committed
  effect-size magnitudes; no Holm-corrected confirmatory family.
- **H3c-spatial reduced to Moran's I clustering only** (Decision 16):
  the regional-pattern clause is dropped (its Hanson 2021 attribution did
  not survive re-verification).
- **H3c provincial-capital test switched to a posterior contrast on
  continuous residuals** (resolves Agent A's B8 finding that a
  frequentist *t*-test on Bayesian posterior quantities is incoherent).
- **H1 demoted from confirmatory hypothesis to completed groundwork.**
  Phase 1 thresholds reported in §6 but no longer presented as a
  confirmatory hypothesis (it is a completed methods step with no live
  decision rule).
- **Convention-shape model specified empirically** (Decision 17):
  century / half-century / reign-related tiers, drawn from the
  2026-05-15 diagnostic.
- **Temporal exploratory analysis added** (Decision 13): habit-removed
  residual trajectory analysis, with foundation dates as the primary
  anchor type and a bounded case-study set for richer independent
  anchors.
- **Plain-English walkthrough rewritten** to introduce all load-bearing
  terms ("aoristic", "deconvolution", "forward-fit", "random intercepts",
  "CPL knots", "bins") on first use and to align step-by-step with the
  technical §3. Re-described the artefact at endpoint level (not just
  midpoint inflation) to match Decision 17.
- **§6 effect-size table restructured** to distinguish confirmatory,
  supporting-consistency, completed-groundwork, and pre-specified-
  exploratory rows. Removed the contradictory "H3b primary | Antonine
  | ≥ 50 % dip" row.
- **Prior predictive checks added** to the Bayesian workflow (alongside
  the pre-existing posterior predictive checks).
- **Weakly-informative priors** on β_within and β_between
  (`Normal(0, 1)`), replacing the previous wide `Normal(0, 2.5)`.
- **Multiple mechanical fixes** per bucket (d): cmdstanpy dependency
  clarified as fallback (not on H3a critical path); brms shadow Jacobian
  block moved out of the binding spec text; "Westfall-Young *p* ≈ 0"
  given resolution (*p* < 0.001 on 20,000 permutations); cell-count
  derivation made explicit; SR1 / SR2 stated as descriptive context;
  §10 structure diagram updated; Hanson city count harmonised throughout;
  Moran's I decision rule reconciled across Field 3, §3, and §6;
  pymc / brms disagreement contingency added to §7.

Diff stat: 223 insertions, 135 deletions (358 lines changed; 87-line net
growth). Substantive rather than purely additive — most changes are
structural rewrites rather than appends.

---

## ChatGPT 5.5 cross-model-review-driven revision (2026-05-17)

A second adversarial-review cycle, driven this time by ChatGPT 5.5
(GPT-5.5; OpenAI). The cross-model rationale, prompt, and elicited
review are committed at `planning/chatgpt-cross-model-review-prompt.md`
and `planning/cross-model-adversarial-review-preregistration.md`. The
review produced 7 BLOCKING, 6 SHOULD-FIX, and 3 MINOR findings — 16 in
total — orthogonal to the Claude-pass findings (the prompt was
engineered to seek orthogonal coverage; the changelog and decision-log
were included as inputs precisely to deter re-finding settled items).

### Triage (2026-05-17)

Findings sorted into four buckets (`planning/chatgpt-review-triage.md`):

- **(a) Superseded:** empty — ChatGPT explicitly avoided re-finding
  Decisions 12–17 by reading the changelog.
- **(b) Substantive — needs Shawn input (10 items):** B1 H3a
  directional rule; B2 mixture likelihood; B3 convention component
  vs Uniform aoristic; B4 recovery-simulation grid + coverage rule;
  B5 H3a uses raw vs corrected counts; B6 H3c residual definition;
  B7 LIST swap contingency; B8 PPC numerical triggers; B9 Hanson-
  population uncertainty sensitivity; B10 Western-Empire province
  list. All ten resolved with Shawn this session as Decisions 18–26.
- **(c) Mechanical / clarity (9 items):** C1 H3a predictor centring;
  C2 subset filter primary picks; C3 confirmatory claim hierarchy;
  C4 Phase 1 cell-count arithmetic; C5 Carleton 2018 attribution
  narrowed; C6 trapezoidal aoristic parameterisation; C7 H2.1 wording
  fix (folded into Decision 21); C8 OSF amendment pre/post-lodgement
  wording; C9 centring/standardisation implications. Applied directly
  in the 2026-05-17 rewrite.
- **(d) Verification (2 items, both resolved during triage):** D1
  Phase 1 96-cell arithmetic verified against the run report (count
  correct; arithmetic expression wrong, applied via C4); D2 Carleton
  2018 attribution verified (paper real and accurate; attribution
  wording overreaches, applied via C5). Neither was a confabulation.

### Three empirical diagnostics driving Decision 20 (2026-05-17)

ChatGPT finding B3 (convention component vs Uniform aoristic)
identified that the prereg's "intervals like `[1, 100]` place
aoristic mass on midpoint years" claim is wrong under uniform
aoristic — a wide-template interval deposits flat plateau mass, not
preferential midpoint mass. The empirical signature of the artefact
in the SPA was an open question; three diagnostic runs were
commissioned to resolve it.

1. **Interval-width diagnostic**
   (`runs/2026-05-17-interval-width-diagnostic/`). Established that
   the dominant artefact mechanism is wide-century-slab loading
   ([1, 100] is 26 % of the corpus; [101, 200] and [201, 300] adding
   roughly the same magnitude again), and that the headline 22.8 ×
   / 41.5 × / 18.8 × ratios were generated by the `int((nb + na) / 2)`
   test statistic — which makes wide-template midpoints (50.5, 150.5,
   250.5) truncate to round years, conflating wide-slab loading with
   midpoint-anchored mass.

2. **Empirical-SPA-shape diagnostic**
   (`runs/2026-05-17-empirical-spa-shape/`). Constructed the actual
   5-year per-year-uniform-aoristic SPA over 50 BC – AD 350 directly.
   Found: no anchor-year structure at AD 50 / 150 / 250 (local
   excess −77 / −79 / +22 relative to the local plateau); the
   largest narrow spikes are at AD 122.5 (Hadrian) and AD 77.5
   (Flavian); the 1 BC / AD 1 boundary is the largest single
   discontinuity (+1,159).

3. **Date-range-filtered SPA diagnostic**
   (`runs/2026-05-17-date-range-filtered-spas/`). Recomputed the SPAs
   under progressive `date_range` thresholds {0, ≤ 1, ≤ 10, ≤ 25, ≤ 50,
   ≤ 75, ≤ 100, ≤ 200, all}. Findings: regnal spikes *amplify* under
   narrow-precision filtering (AD 122.5 spike-to-plateau ratio rises
   from 1.61 × → 4.96 × → 13.83 × as we tighten from full → ≤ 25 →
   = 0); the century-boundary plateau-step pattern weakens decisively
   (Pearson r between SPA( ≤ 25) and SPA( > 100) = 0.34); a third
   regnal spike at AD 212.5 (Severan, [212, 217] = 728 inscriptions)
   was discovered. **The regnal spikes are real ancient clustering;
   the plateau-step pattern is editorial-encoding artefact.**

The diagnostic chain reframed the artefact from "century-midpoint
inflation" (the framing under Decision 17) to "wide-template-slab
editorial encoding plus real ancient regnal clustering." Decision 17's
three-tier anchor-year convention-component structure was *superseded*
by Decision 20's template-interval slab structure.

### Decisions 18–26 captured (2026-05-17)

- **Decision 18 — H3a directional confirmatory rule.** Three-way
  verdict (supported / evidence against / inconclusive) with
  posterior-probability ladder reporting. Resolves B1.
- **Decision 19 — Bayesian mixture observation model.** Multinomial
  primary; Dirichlet-multinomial and rescaled NegBin supplementary
  for model-comparison reporting. Resolves B2. Primary item for
  Martin's consultation.
- **Decision 20 — Convention component is a template-interval slab
  structure (supersedes Decision 17).** Century-slab + half-century-
  slab + reign-interval-slab tiers. Dictionary pinned by a pre-Phase-2
  empirical scan. Resolves B3. Primary item for Martin's consultation.
- **Decision 21 — H2.1 recovery-simulation grid procedurally
  preregistered + pre-Phase-2 design artefact.** Coverage rule
  corrected to per-cell repeated-replicates. Cell-wise reporting
  required. Resolves B4 and folds in C7's wording fix. Primary item
  for Martin's consultation.
- **Decision 22 — H3a uses date-window-filtered counts.** Primary RQ
  rewording: artefact protection for H3a is the date-window filter;
  mixture corrects temporal analyses only. Resolves B5.
- **Decision 23 — H3c residuals are Pearson residuals.** Draw-wise
  capitals contrast; posterior-mean residuals for Moran's I
  confirmatory rule with field-standard permutation inference;
  posterior distribution of Moran's I across draws reported as
  supplementary. Resolves B6. Primary item for Martin's consultation.
- **Decision 24 — Freeze LIRE v3.0 for this OSF lodgement.** LIST is
  a post-lodgement amendment or follow-up candidate. Resolves B7.
- **Decision 25 — PPC failure triggers are numerical, not narrative.**
  Specifics pinned in the same pre-Phase-2 design artefact as the
  recovery-grid spec (one artefact, two specification tables).
  Resolves B8. Primary item for Martin's consultation.
- **Decision 26 — Smaller-substantive adjustments.** Hanson-population
  measurement-error sensitivity (σ_pop ∈ {0.1, 0.2, 0.3}) added as
  preregistered exploratory; Western-Empire-provincial subset
  operationalised via the project's existing province_language
  classification. Resolves B9 and B10.

Four of the nine new decisions (19, 21, 23, 25) are flagged as
primary items for the planned Martin consultation.

### Comprehensive rewrite of `preregistration-draft.md` (2026-05-17)

A single comprehensive rewrite implementing Decisions 18–26 plus the
bucket-(c) mechanical fixes. Headline changes:

- **§2 Description rewritten** to drop the misleading "midpoint
  spike" framing (the 22.8 × / 41.5 × / 18.8 × / 39.7 × O/E ratios
  were partly a test-statistic artefact; not the artefact's primary
  signature in the actual SPA). New framing: wide-template editorial
  encoding (54.5 % `not_before` end-in-01 / 53.0 % `not_after` end-
  in-00; [1, 100] is 26 % of corpus) plus real ancient regnal
  clustering. The three 2026-05-17 diagnostic runs are cross-
  referenced as the empirical basis.
- **Field 3 H3a decision rule rewritten** to three-way verdict
  (Decision 18); H3c residual operationalisation pinned (Decision
  23); confirmatory claim hierarchy paragraph added (C3); Western-
  Empire subset operationalised (Decision 26).
- **Primary RQ rewritten** to drop the "after controlling via
  Bayesian mixture model" framing for H3a (Decision 22) — now reads
  "after applying a 50 BC – AD 350 date-window filter."
- **§3 Bayesian mixture spec rewritten** with explicit multinomial
  observation model (Decision 19), template-interval slab convention
  structure (Decision 20), supplementary Dirichlet-multinomial and
  rescaled-NegBin fits, design-artefact-pinned recovery-grid axes
  (Decision 21), numerical PPC thresholds (Decision 25).
- **§3 NBR rewritten** to state response is date-filtered counts
  (Decision 22); three-way decision rule (Decision 18); predictor-
  scaling specs (C9); Pearson residual definition for H3c (Decision
  23).
- **§4 Phase 1 96-cell arithmetic corrected** (was: "3 × 2 ×
  (3 × 2 + 1) × 1 = 42 ≠ 96"; corrected to the actual grid
  decomposition: empire 6 + province 48 + urban-area 42 = 96). C4.
- **§4 Carleton 2018 citation narrowed** (C5). The "PEWMA power-
  simulation framework for cross-sectional SPA × covariate analysis"
  attribution overreached; reworded to honest "inspired by their
  synthetic-time-series-with-known-effects design."
- **§4 Phase 2 rewritten** for procedural recovery-grid + design-
  artefact reference (Decision 21).
- **§1 LIST extension paragraph removed** (Decision 24); §7 LIST
  swap contingency clause removed; pre/post-lodgement amendment
  wording added (C8).
- **§5 Hanson-population measurement-error sensitivity added**
  (Decision 26).
- **§6 effect-size table** updated for the three-way H3a verdict,
  Pearson-residual H3c rules, H2.1 coverage-rule wording fix, and
  H2.2 boundary-step framing.
- **§9 three new limitations** added: BC / AD boundary step at
  1 BC / AD 1; H3a-uses-date-filtered-counts scope-limit; Western-
  Empire frontier-province classifications (Moesia / Sicilia).
- **§10 hypothesis-structure diagram** updated to reflect Decision
  22's date-filtered-counts scope.
- **Trapezoidal aoristic parameterisation** pinned in §3 (C6):
  `edge_band = min(width / 4, 10 years)`; plateau density
  `1 / (width − edge_band)`; linear edge ramp; integrates to 1.

Diff stat: 146 insertions, 78 deletions (224 lines changed; 68-line
net growth, taking the draft from 381 to 449 lines). Most changes
are structural rewrites of §2 / §3 / §4 / §6 / §9 rather than appends.

### Hanson 2021 attributions and other citations unchanged

The ChatGPT pass surfaced no new confabulated factual claims — only
the Carleton 2018 attribution-wording overreach (C5). The Claude-
pass-corrected Hanson 2021 attributions (mean exponent β = 0.672;
Moran's I = 0.046; provincial-capital mean residual 0.43; ArcGIS
spatial-autocorrelation tool; letter-count rationale on p. 142; no
regional-pattern map-match) were all verified by the previous
citation audit and remain intact.

---

## Round-3 saturation check — cross-model (ChatGPT 5.5 + Gemini 3 Pro) (2026-05-17)

A third adversarial pass, framed as a saturation check rather than
a comprehensive review. Two models in parallel: ChatGPT 5.5 (same
model as round 2, but a fresh chat) and Gemini 3 Pro (a new model
for cross-model orthogonality). Prompt and elicited reviews committed
at `planning/saturation-check-prompt-2026-05-17.md`,
`planning/prereg-saturation-check-GPT55.md`, and
`planning/prereg-saturation-check-gemini.md`.

### Findings (cross-model comparison)

- **Strong cross-model agreement (BLOCKING; both models):** the
  preregistration repeatedly described "the H3c residual analysis"
  as part of the mixture-correction scope — but H3c residuals are
  computed from H3a's posterior, and H3a uses date-window-filtered
  counts (Decision 22), so H3c inherits the date-filtered-count
  scope and is *not* mixture-corrected. This was a logical gap
  Decision 22 opened that the 2026-05-17 rewrite carried forward
  out of inheritance from the pre-Decision-22 framing.
- **ChatGPT-only (SHOULD-FIX):** the multinomial observation model's
  count / proportion / integer-vector transformation was
  underspecified; the "rescale by multiplying by N and rounding"
  phrasing was ambiguous because the raw aoristic-mass SPA already
  sums to N by construction.
- **Gemini-only (SHOULD-FIX):** the "year-0" terminology at the
  BC → AD boundary was historiographically wrong (1 BC is followed
  directly by AD 1; no year 0 in the Julian / Gregorian calendar),
  signalling a basic chronological error to historian readers
  precisely where the paper diagnoses chronological artefacts.

Cross-model interpretation: agreement on a finding is strong
signal it's real. Single-model findings are model-specific catches
that are still real (both are caught and applied) but lower the
signal that they're load-bearing methodology gaps.

### Verdict from both models

- **ChatGPT 5.5:** "Round 3 is close to saturated but not fully
  saturated. ... Once those two are corrected in the preregistration
  text, I would move the verdict to: 'no findings of magnitude that
  warrant a further revision cycle; ready to lodge subject to the
  planned statistician consultation.'"
- **Gemini 3 Pro:** "Real work remaining (but very minor). ... Fix
  that single contradiction, adjust the 'year 0' phrasing for the
  historian audience, and this document will be fully saturated and
  ready to lodge."

### Corrections applied (2026-05-17)

- **H3c-scope correction** in five locations across the prereg
  (§2 "Scope of the mixture correction" paragraph; plain-English
  Step 6; §3 "Bayesian NBR for H3a" response variable paragraph;
  §9 known limitations on date-filtered-counts; the "How the
  phases connect" walkthrough paragraph is unchanged because it
  references H3c's residual analysis structurally, not its
  mixture-correction scope), plus two corresponding edits to
  Decision 22 in `decision-log.md` (the mixture's-role-in-the-paper
  bullet and the §3 scope-of-application consequence) flagged as
  "round-3 clarification 2026-05-17."
- **Multinomial observation-model normalisation** rewritten in §3
  to define the m_t → q_t → y_t transformation explicitly:
  raw aoristic mass m_t (sums to N_eff by construction); empirical
  shape q_t = m_t / Σm_t; integer count vector y_t via deterministic
  largest-remainder rounding with Σy_t = N_eff. The multinomial
  likelihood y ~ Multinomial(N_eff, p) attaches to this integer
  vector explicitly.
- **Year-0 terminology** corrected across the prereg, decision log,
  and changelog: replaced with "1 BC / AD 1 boundary" or "BC / AD
  boundary" as appropriate. The §9 limitation gains an explanatory
  parenthetical noting that 1 BC is followed directly by AD 1 in
  the Julian / Gregorian calendar.

### Saturation verdict

Both models converge: after these corrections, the preregistration
has saturated. No further adversarial revision cycles are necessary
before the planned statistician consultation. The document is ready
for Martin's pack and, after Martin's input, OSF lodgement.

---

## Upcoming pre-lodgement steps

The preregistration is ready for the planned statistician
consultation. Outstanding work before lodgement:

1. **Statistician consultation pack for Martin** (Task #17). Curated
   extract of the decision log focused on the four Martin-flagged
   decisions (19 mixture observation model; 21 recovery-grid
   coverage rule and shape library; 23 H3c residual choice and
   asymmetric draw-wise / posterior-mean split for Moran's I; 25
   numerical PPC thresholds); the original Decisions 12–17 also
   included where Martin should weigh in (within-between
   specification, prior choices, multiple-comparison policy).
2. **Apply Martin's input** to the preregistration; document.
3. **Lodge on OSF.** After Martin's input is incorporated and any
   remaining issues from the consultation are resolved. The pre-
   Phase-2 design artefact (recovery-grid values + numerical PPC
   thresholds) is committed in parallel with lodgement.

---

## Archived documents

- `preregistration-amendments-2026-04-25.md` — the round-1 amendment proposals
  drafted from the H1 simulation plan review. All five amendments were applied
  to the draft in commit `efc6e07` (2026-04-25). Archived to
  `archive/planning/` during the 2026-05-14 lodgement pass; its content is
  superseded by the "Round-1 amendments" entry in the pre-history above.
