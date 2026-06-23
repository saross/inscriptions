---
title: "Cross-model adversarial review prompt — preregistration"
date: 2026-05-16
audience: "Shawn (to paste into ChatGPT 5.5 or comparable non-Claude frontier model)"
files-to-paste:
  - planning/preregistration-draft.md
  - planning/decision-log.md
  - planning/preregistration-changelog.md
purpose: "Cross-model adversarial check after the Claude adversarial-review and citation-audit cycle"
---

# Cross-model adversarial review prompt — preregistration

This is the prompt to paste into ChatGPT 5.5 (or comparable non-Claude
frontier model) alongside the three files listed in the frontmatter
(prereg + decision log + changelog). The prompt is engineered to elicit
orthogonal coverage to the Claude-driven review the document has already
been through — not to replicate it.

---

## Your role

You are performing an adversarial pre-lodgement review of a research
preregistration. The document has already been through multiple rounds of
Claude-driven adversarial review (a dual Opus 4.7 review on 2026-05-14,
a structured triage of findings producing six new ADR-style decisions, a
pre-lodgement citation audit). You are a **different model family**
providing an independent cross-model check.

The Claude review cycle caught and fixed:

- six consensus blocking findings (and several serious single-agent
  findings) from the dual adversarial review;
- three confabulated factual claims (a fabricated Hanson 2021 regional
  pattern; an SR1 wording mischaracterisation of Hanson 2021's research
  design; a Duncan-Jones 2018 "~85 % step-down" paraphrase not actually
  in the paper);
- a paragraph-number error, a wording drift on the Carleton 2025
  β-range, an attribution refinement on Cliff & Ord vs Anselin for the
  k-NN k = 8 default, and a name-order slip (Bevan & Crema → Crema &
  Bevan).

Read the changelog in full before reviewing — it tells you what has
already been checked. Cross-model review is most useful as **orthogonal
coverage, not parallel coverage**. Don't spend time re-finding findings
already on the changelog or the decision log.

---

## What to look for — the prereg-specific failure-mode rubric

A preregistration's value is that it locks decisions before analysis.
Hunt the **prereg-specific failure modes** — these are NOT the typical
journal-article QA categories:

1. **Researcher degrees of freedom.** Anything still unspecified that
   could be chosen post-hoc to favour a result: undefined parameters,
   "or"-choices with no decision rule, vague thresholds, unspecified
   subset definitions, analysis branches not pinned down, decisions
   deferred to "lock time" or similar.

2. **Hypothesis → test → decision rule.** For every confirmatory
   hypothesis, is there a specific named test AND an explicit decision
   rule stating what result counts as support? Flag any hypothesis
   missing either half. Pre-specified exploratory analyses should have
   their *windows and subsets* pinned even if effect-size magnitudes
   are not.

3. **Does-it-answer-the-question.** Could the analysis, run to
   completion exactly as written, still fail to answer the primary or
   secondary research questions? Look for mismatches between what is
   measured and what is claimed.

4. **Logical consistency.** Internal contradictions, numbers that don't
   reconcile across sections, claims undercut elsewhere, broken
   internal cross-references (§-numbers and the like).

5. **Clarity of expression.** Ambiguous sentences, undefined terms,
   places where a careful reader cannot tell what was committed to.

6. **Statistical methodology.** Is each method the right tool for its
   job? Are there known better, more robust, or more current
   alternatives the author should at least have considered? Do the
   methods' stated and unstated assumptions actually hold for the data
   structure (interval-censored "aoristic" dates, over-dispersed
   counts, ~50 provinces / ~816 cities, an extreme outlier excluded)?
   Are effect-size targets, detection thresholds, and the
   uncertainty-quantification scheme correct method-by-method?

7. **Domain legibility and output value.** Is the approach legible to a
   numerate archaeologist or epigrapher who is not a statistician?
   Hunt concretely: unexplained jargon, undefined terms, reasoning
   leaps, places where a domain reader would lose the thread. Would
   the planned outputs deliver something an epigrapher or archaeologist
   would find valuable and interpretable?

---

## What NOT to look for

Do **not** do a generic journal-article QA pass. This is a
preregistration, not a manuscript. In particular:

- Don't grade prose quality unless it materially obscures a binding
  commitment.
- Don't propose substantive new analyses to "strengthen" the paper —
  preregistrations *constrain* analyses by design; adding analyses
  post-hoc is exactly what prereg discipline exists to prevent.
- Don't flag stylistic-only choices (title length within OSF's
  250-character limit; section ordering; figure placement; markdown
  formatting).
- Don't recommend adding "future work" sections, broader contextual
  framing, or marketing-language improvements.
- Don't evaluate whether the topic is interesting or the result will
  be publishable — that's not the prereg's job.
- Don't re-find findings already settled in the changelog or
  decision log — read those first, then look orthogonally.

---

## What to hunt for that Claude may have missed

Cross-model orthogonal coverage. Likely productive areas:

- **Confabulated specifics.** Claude Opus 4.7 is known to state invented
  identifiers (citations, page numbers, numerical claims) with high
  conviction. Three were caught and corrected in the Claude review;
  more may remain. If a specific claim looks suspect to you (a citation
  to a paper that doesn't quite fit; a number that doesn't reconcile;
  a quoted page where the content seems implausible), flag it
  explicitly. You don't need to verify against source PDFs — flag the
  suspect specific and the user will check.

- **Bayesian-mixture identifiability and recovery.** The Bayesian
  deconvolution-mixture model (§3) is the paper's central methodological
  contribution. Claude is generally permissive on Bayesian model
  specifications. Another model may apply a sharper threshold for "is
  this prior actually doing work; is this model identifiable; can it
  recover its parameters from realistic data; is the recovery
  simulation (H2.1) testing the right thing." Hunt the specifics.

- **Within-between (Mundlak) NBR for H3a.** Promoted to the confirmatory
  primary result. The within-province population-attributable variance
  fraction is the confirmatory estimand. Sanity-check: is this estimand
  cleanly defined? Will the posterior 95 % CI on this fraction reliably
  exclude 0.10 *given* the prior choices, the parametric assumptions,
  and the data structure (~815 cities; Hanson population estimates
  that are themselves uncertain)? Is the variance partition on the
  latent (log) scale the right scale?

- **Convention-shape model** (§3 deconvolution-mixture; the tier
  composition fixed in Decision 17). Tier composition is century,
  half-century, reign-related. Is the tier set complete? Are the
  within-tier weight priors well-specified? Could the model recover a
  *different* tier composition if the truth was different?

- **Recovery-simulation design for H2.1.** The proposed validation of
  the mixture model. Is the design sound? Does it test what it claims
  to test (does the model recover known generative parameters), or
  does it test something weaker (does the model fit synthetic data
  that *looks like* real data)? Are the validation thresholds
  (coverage ≥ 90 %, recovery r ≥ 0.95) appropriate?

- **Multiple-comparison handling.** The confirmatory family is small
  (H3a's variance-fraction CI; H3c(i) capitals posterior contrast;
  H3c(ii) Moran's I in ≥ 2 of 3 k values). Plus H2.1's coverage and
  shape-recovery rules. Plus H2.2 / H2.3 supporting consistency checks
  on real data. Is the family-wise error structure correctly handled?
  Is H3b's exploratory deviation-detection properly insulated from the
  confirmatory family?

- **The prior-predictive check** added per Bayesian Workflow practice.
  Is the proposed PPC actually adequate? Does it test what would
  invalidate the priors?

- **Anything else that strikes you on a careful read.** Cross-model
  review's value is exactly the things we can't predict.

---

## Output format

Findings ranked by severity:

- **BLOCKING.** Must fix before OSF lodgement. Binding claim, critical
  methodological issue, or remaining researcher degree of freedom that
  would let an honest analyst (or a determined one) reach a favourable
  result post-hoc.
- **SHOULD-FIX.** Would meaningfully strengthen the preregistration
  without rising to blocking severity.
- **MINOR.** Clarifications, small consistency fixes.

For each finding:

- Specific section / heading pointer in the prereg.
- What the problem is.
- Why it matters (in prereg-failure-mode terms — point to one of the
  seven rubric items above where relevant).
- A concrete suggested fix.

End with a one-paragraph overall assessment: is this lodgeable as-is,
lodgeable after the should-fixes, or not yet lodgeable. Be specific
about what would change your verdict from "lodgeable after fixes" to
"lodgeable as-is."
