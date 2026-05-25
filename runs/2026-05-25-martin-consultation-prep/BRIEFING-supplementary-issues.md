---
title: "Martin consultation 2026-05-25 — supplementary issues briefing"
audience: "Shawn (PI), going into the consultation"
register: "Plain-language; companion to BRIEFING.md; covers items beyond the alpha-bias / calibration-cohort work"
date: 2026-05-25
status: pre-meeting brief (supplementary)
related-artefacts:
  - runs/2026-05-25-martin-consultation-prep/BRIEFING.md (main briefing)
  - planning/martin-consultation-pack-2026-05-17.md (the previous consultation pack, sent eight days ago, unanswered)
  - planning/decision-log.md (Decisions 1–32)
  - planning/preregistration-draft.md
  - planning/backlog-2026-05-03.md
---

# Supplementary issues briefing

The main `BRIEFING.md` covers the alpha-bias diagnosis and the
empirical-Bayes calibration-cohort fix. This document covers everything
*else* that's on Martin's desk or should be — particularly the
**eight-question pack sent to him on 2026-05-17 and still unanswered**.
Read this second; the main briefing first.

---

## 1. The eight questions from 2026-05-17 — STILL OUTSTANDING

The previous Martin pack at `planning/martin-consultation-pack-
2026-05-17.md` (863 lines, structured for an applied-econometrician
audience) was sent 2026-05-17. To our knowledge Martin has not yet
responded. The pack covers methodological choices that were
**incorporated into the preregistration as "pending Martin's review;
OSF amendment if revision recommended"** — meaning all eight are
provisionally locked but Martin's input could reverse any of them.

If he hasn't pre-read the pack, surface it explicitly at the top of
the meeting. Even if he has, ask him to confirm or push back on each.

### Q1 — Mixture observation model (Decision 19)

We adopted **multinomial as primary**, with Dirichlet-multinomial
and rescaled negative-binomial as supplementary. The choice matters
because the multinomial has no over-dispersion parameter; if the
true counts are over-dispersed, the multinomial likelihood will
under-state CI widths. We want Martin's view on whether the
supplementary safety net is sufficient or whether the over-dispersed
form should be primary.

### Q2 — Recovery-simulation per-cell coverage rule (Decision 21)

The recovery grid uses a 100-replicate-per-cell rule with α-coverage ≥
90 % per cell. We want Martin to confirm 100 is sufficient (Decision
27 bumped this from 50 after cross-model stand-in review). **This is
now empirically pressure-tested by our F1 / F3 / F0 follow-ups**;
the grid ran 100 replicates × 450 cells and we have detailed
diagnostics.

### Q3 — H3c residuals: Pearson choice + asymmetric treatment (Decision 23)

We use **Pearson residuals**, with the capitals contrast computed
draw-wise and the Moran's I clustering computed on posterior-mean
residuals (using field-standard permutation inference). The asymmetric
treatment is deliberate — capitals contrast is two-group and a draw-
wise distribution is informative; Moran's I needs the posterior-mean
single-statistic plus permutation. We want Martin's sign-off on the
asymmetry.

### Q4 — Numerical PPC thresholds (Decision 25)

The preregistered PPC suite has eight categories (Gelman et al. 2020
+ Decision 29's posterior-predictive spatial autocorrelation). The
numerical pass/fail thresholds are **deferred to a pre-Phase-2 design
artefact** — not yet committed. Martin's input on what the thresholds
should be is direct value, particularly for the two-tier severity
scheme (Decision 30).

### Q5 — H3a Mundlak NBR estimand (Decision 12)

`f_within = Var(β_within · log_pop_within) / Var(latent linear predictor)`.
The 0.10 substantive threshold for "population matters within
provinces" was set provisionally. Stand-in cross-model review
endorsed both the spec and the 0.10 threshold; we want Martin's
confirmation.

### Q6 — Habit-removed residual trajectory (Decision 13)

This is the *exploratory* analysis where we look at the
inscription-rate-minus-Hanson-population residual trajectory over
time. The intent is to surface temporally-coherent residual patterns
without binding the analysis to specific thresholds. Martin's input
on whether this exploratory framing is defensible.

### Q7 — Confirmatory hierarchy + multiple-comparison policy

We do **not** apply Holm correction across the H1 / H2 / H3a / H3b /
H3c confirmatory family. Reasoning: each hypothesis tests a different
empirical question; they're not exchangeable; Holm is conservative
when applied to a small set of pre-specified non-exchangeable
hypotheses. Stand-in review endorsed this. Want Martin's
confirmation explicitly — this is the kind of multiple-comparison
question reviewers will probe.

### Q8 — Pre-Phase-2 design artefact inputs

Items still uncommitted that we want Martin's view on:

- **Recovery-grid alpha values** — currently {0.05, 0.30, 0.50, 0.70,
  0.95}. We've now learned (from F0a) that the bias begins at α = 0.30
  and saturates by α = 0.70 — should the grid be refined to add
  α = 0.10 / 0.20 / 0.40 for finer resolution of the bias onset?
- **Numerical PPC thresholds** (overlaps Q4).
- **Wasserstein-1 flagging threshold** — Stage 2 of our recent work
  suggested **W-1 ≤ 18.6 years** matches the current Pearson r ≥ 0.95
  selectivity. Locking this number is on the table.
- **Aoristic-Monte-Carlo N_MC** and divergence-flag threshold for
  Decision 28's supplementary mixture fit.
- **Per-category 2 × / 1.5 × severity cutoffs** (Decision 30 PPC
  scheme).
- **Posterior-predictive Moran's I bounds** for the H3a residuals
  spatial autocorrelation check.
- **Template-dictionary inclusion threshold** — historically a
  placeholder. Now superseded by our empirical p_conv work (Stage 1)
  — worth flagging that the template dictionary is now empirical-data-
  derived rather than threshold-based.

---

## 2. New findings since 2026-05-17 that affect prereg-binding decisions

Three items where our recent work changes the empirical basis for
preregistered decisions:

### 2.1 The F0a regnal_cluster bidirectional bias finding

The systematic analysis of all 450 cells revealed that the
`regnal_cluster` shape shows a **bidirectional α-bias** — positive
at α = 0.05, negative at α = 0.70 — *opposite-direction biases at
different α values for the same shape*. None of the other five shapes
flip sign.

**Why it matters for the prereg**: H3c (residual clustering) and §5
chronological-resolution analyses examine reign-specific patterns.
If the model's residual structure is biased differently depending on
where the genuine activity sits relative to a reign-window, the
residual clustering claims become harder to defend. **This is
worth flagging to Martin as an unexpected finding that may require
its own prereg amendment**.

### 2.2 W-1 threshold proposal (F0b)

F0b computed the empirical W-1 distribution across the 450 cells.
**W-1 ≤ 18.6 years reproduces the current Pearson r ≥ 0.95
selectivity** on non-flat cells. A principled alternative: **W-1 ≤ 5
years** (one 5-y bin width), which is markedly stricter (28.8 %
non-flat pass rate).

**Decision needed**: which threshold for the OSF amendment that
replaces Pearson r (which is NaN-on-flat-baseline) with W-1 as the
binding shape metric.

### 2.3 Empirical p_conv displaces the placeholder template dictionary

Decision 20 specified a "template-interval slab structure" for the
convention component. The actual template-interval dictionary was a
placeholder (Decision 21's pre-Phase-2 design artefact). Stage 1 of
our recent work **replaces the placeholder with empirically-derived
slab weights** from F1 + F3 inscriptions. This is a strict
improvement, but should be incorporated as an OSF amendment when
the embargo lifts.

---

## 3. H3b — the secondary substantive analyses (medium priority)

Three preregistered analyses that have not yet been touched. Each
needs an H2 mixture-model output before it can run, so they're
downstream of the alpha-bias fix.

### 3.1 H3b deviation detection (Holm-Bonferroni at H1-reachable cells)

Forward-fit envelope test at the cells where H1 confirmed reachability
(`c_20pc_25y` excluded per Decision 10). Six-cell or twelve-cell
configurations — option preregistered, locked when H2's results
parquet is built. Estimated 1-2 days implementation once H2 lands.

### 3.2 H3b Antonine-specific replication test (AD 165-180)

Empire-wide + Asclepius-cult subset (Glomb et al. 2022) + military-
administration subset (Duncan-Jones 2018). Per-subset eligibility
gated on H1 reachability. **Preregistered exploratory replication
of two specific prior-literature claims.**

### 3.3 H3b Crisis-of-Third-Century replication (AD 235-284)

Empire + Western-Empire-provincial subset. Half-century-scale event;
diffuse causal structure; magnitude not pre-committed.

**For Martin**: any view on whether the Holm-Bonferroni framing is
correct here? The Antonine and Crisis tests are exploratory
replications, not part of the confirmatory family — confirming this
framing avoids family-expansion concerns.

---

## 4. §5 small-N city trajectory work — Layer B literature assembly

Preregistered §5 includes a small-N city trajectory estimation using
baorista (Crema 2025). The approach has three layers:

- **Layer A** — aoristic-Bayesian per-city posteriors.
- **Layer B** — independent literature ground-truth assembly (we
  curate published date-anchored events: city foundations, known
  building campaigns, dated colonial settlements). Layer B is the
  *hard* one — comprehensive assembly is deferred to a follow-up
  paper; the current paper uses a deliberately time-boxed case-study
  set for richer anchors.
- **Aggregate diagnostic** — comparison between Layer A and Layer B.

**For Martin**: any view on whether the Layer B time-boxing is
defensible? The risk is that the case-study set is cherry-picked
toward cities with rich anchor evidence, which biases the diagnostic.

This is also the place where baorista (the Bayesian aoristic
methodology of Crema 2025) explicitly enters. Decision 3 specifies
a sensitivity comparison between forward-fit and baorista on
representative provincial subsets — also on the H3b post-output
queue.

---

## 5. Publication / strategic decisions

Three items where Martin's input would be useful but they're not
methodological-statistical:

### 5.1 Target journal venue (TBD 6, Decision 7 deferred)

Leaning JAMT (*Journal of Archaeological Method and Theory*) — methods-
focused, longer word limits, substantive grounding via H2/H3a +
replication tests. Alternative: JAS (*Journal of Archaeological
Science*). Martin's view on which is the right venue.

### 5.2 Methodology paper vs substantive paper split

Currently bundled as a single paper. The empirical-Bayes calibration
cohort work + the family classifier is potentially a separable
methodology contribution. **The split decision affects how the
H2/H3 substantive results are framed and what reviewer pool sees the
paper.**

### 5.3 OSF embargo lifting

Currently embargoed pending double-blind submission decision.
Embargo lift timing affects when we can publicly cite the prereg URL
and when the methodology paper (if separable) can move forward.

### 5.4 Acknowledgement / co-authorship on methodology paper

If the empirical-Bayes calibration cohort approach (or the family
classifier) becomes a separable methodology paper, ask whether Martin
would like authorship recognition. He's been substantively involved
in the diagnostic-statistical thinking even if his formal review of
the eight 2026-05-17 questions is pending.

---

## 6. Reproducibility / open-science commitments

Lower priority for today, but worth knowing:

- **Phase 2 Dockerfile + Zenodo archival** — mandated at paper
  submission. Snapshots `pyproject.toml` + `uv.lock` + R session +
  cmdstan + baorista + repo into a reproducible image. *Not blocking
  today's conversation.*
- **LIRE v3.0 frozen** (Decision 24). LIST v1.2 swap is deferred to
  post-lodgement amendment or follow-up paper.

---

## 7. Suggested triage for today's 90 minutes

If Martin has not pre-read the 2026-05-17 pack, the consultation
realistically cannot cover everything. Suggested triage:

**Highest priority (must cover today):**

1. Decisions A and B from the main briefing — recover-vs-discard and
   empirical-Bayes soundness. Everything else hinges on these.
2. **The eight 2026-05-17 questions in headline form**, with offer to
   discuss whichever Martin wants to dig into. At minimum: Q1
   (mixture observation model), Q3 (H3c residuals), Q4 (PPC
   thresholds), Q7 (multiple-comparison policy).
3. The seven Stage 3 implementation decisions (from the main
   briefing).
4. **The F0a regnal_cluster bidirectional bias finding** — this is a
   new diagnostic finding that may require its own prereg amendment.

**If time permits:**

5. The W-1 threshold (18.6 y vs 5 y) — quick decision.
6. The §5 small-N work — Layer B time-boxing defensibility.
7. The methodology-paper-split question.

**Defer to written follow-up if necessary:**

8. H3b Holm-Bonferroni framing.
9. Journal venue.
10. Authorship recognition.

---

## 8. One-line items to drop in the meeting if they fit

- "We've banked a 45-50× ESS improvement via non-centred GRW — that's
  decoupled from the alpha-bias question; we're adopting it
  unconditionally."
- "The empirical p_conv we now use is *not* the placeholder template
  dictionary the prereg specified — it's the data-derived
  replacement. Should be folded into an OSF amendment."
- "Recovery grid showed 80 % of the AD 300-350 period is editorial
  templates — the late corpus is even more template-dominated than
  the body. Worth flagging when we report late-period H3 results."
- "F0a found a bidirectional bias in regnal_cluster that none of
  the other shapes show. Possibly worth its own prereg amendment."

End of supplementary briefing.
