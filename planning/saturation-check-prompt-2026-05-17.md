---
title: "Round-3 saturation-check prompt — preregistration"
date: 2026-05-17
audience: "Shawn (to paste into ChatGPT 5.5 and Gemini 3 Pro)"
files-to-paste:
  - planning/preregistration-draft.md
  - planning/decision-log.md
  - planning/preregistration-changelog.md
  - planning/cross-model-adversarial-review-preregistration.md
purpose: "Third adversarial pass — saturation check before OSF lodgement. Cross-model run on ChatGPT 5.5 (same model as round 2) AND Gemini 3 Pro (new model). Compare findings."
---

# Round-3 saturation-check prompt — preregistration

Paste this prompt into ChatGPT 5.5 and into Gemini 3 Pro alongside
the four files in the frontmatter. Same prompt to both models. The
purpose is *cross-model orthogonal coverage* AND *a saturation
check*: this is round 3 on a document that's been through two
prior adversarial cycles plus a QA pass; the question is whether
any further finding is significant enough to warrant another
revision cycle, or whether the document has saturated.

---

## Your role

You are performing the **third adversarial pass** on a research
preregistration. The document has already been through:

- **Round 1 (2026-05-14):** dual-agent Claude Opus 4.7 adversarial
  review on the editorial-pass-state draft. Six consensus blocking
  findings plus several serious single-agent findings. All addressed
  via Decisions 12–17 and the 2026-05-16 comprehensive rewrite.
- **Round 2 (2026-05-16):** cross-model adversarial pass by ChatGPT
  5.5. 7 BLOCKING + 6 SHOULD-FIX + 3 MINOR — 16 findings total. All
  addressed via Decisions 18–26 (one of which, Decision 20,
  supersedes Decision 17), the 2026-05-17 comprehensive rewrite,
  and three new empirical diagnostics that reframed the artefact
  narrative.
- **QA pass (2026-05-17):** structured QA on the rewrite by a
  separate Claude agent (fresh context). Caught 1 blocking + 4
  should-fix + 2 minor — all internal-consistency and stale-phrase
  issues. All applied.

The full provenance is in `preregistration-changelog.md`. Read it
first — it tells you what has already been caught and fixed.

You are round 3. Cross-model orthogonal coverage (you're either
ChatGPT 5.5, who saw the document last cycle but has not seen the
rewrite; or Gemini 3 Pro, who has not seen the document at all).

## What to look for — a saturation-check rubric

A *saturation check* is different from a comprehensive review. The
question is not "find me everything," it is **"is there any
remaining finding significant enough to warrant another revision
cycle?"** If there is nothing, say so explicitly — that is the
desired outcome.

Hunt these four specific failure modes:

1. **Confabulation suspects in the NEW content.** The 2026-05-17
   rewrite added specific factual claims that were not in the
   document at round 2:

   - Three regnal-cluster years (AD 77.5 Flavian; AD 122.5
     Hadrianic; AD 212.5 Severan; with reign-interval inscription
     counts and spike-to-plateau ratios).
   - The +1,159 step at the BC → AD year-0 boundary.
   - "26.3 % of corpus" for the [1, 100] template.
   - The 54.5 % / 53.0 % endpoint-rounding statistics (carried over
     from earlier but now load-bearing for the new narrative).
   - The three diagnostic run paths
     (`runs/2026-05-17-interval-width-diagnostic/`,
     `runs/2026-05-17-empirical-spa-shape/`,
     `runs/2026-05-17-date-range-filtered-spas/`) — these are
     supposed to be real local-filesystem artefacts.

   If any specific numerical claim, citation, or named identifier
   looks suspect to you, flag it. You do not need to verify against
   sources — flag the suspect specific and Shawn will check.

2. **Logical gaps the new decisions opened.** Decisions 18–26 made
   nine new methodology commitments. Walk each decision against the
   prereg's current state and check whether the decision opened a
   downstream problem the rewrite didn't solve. Particular targets:

   - **Decision 22** (H3a uses date-filtered counts, not mixture-
     corrected counts). Does this create a problem for H3c's residual
     analysis, which runs on H3a's posterior? Does it create an
     inconsistency between the H2 mixture-validates-temporal-analyses
     framing and the H3a population claim?
   - **Decision 20** (template-interval slab convention component).
     Is the slab structure compatible with the H2.1 recovery-
     simulation grid (which must build synthetics from this
     structure)? Is the "year-precise inscriptions stay in
     genuine_SPA" rule operationalised consistently?
   - **Decision 21** (procedural recovery grid + pre-Phase-2 design
     artefact). Is the design artefact's prereg-binding role clear?
     Could the artefact be written in a way that retroactively
     loosens the prereg's commitments?
   - **Decision 19** (multinomial likelihood primary; Dirichlet-
     multinomial and rescaled NegBin supplementary). Are the
     supplementary models truly "not confirmatory comparators" as
     stated, or could they end up shadow-driving the H2.1 verdict?

3. **Stale-anchoring drift in the new explanatory text.** §2
   Description was rewritten end-to-end; the plain-English
   walkthrough Steps 2/3/6/7 were rewritten; §9 known limitations
   was extended. Does the new explanatory text accurately describe
   the new methodology? Could a careful reader misinterpret what
   was committed to? Particularly: does §2's "wide-template-slab
   editorial encoding plus real ancient regnal clustering" framing
   hold up against the technical §3 spec? Does the walkthrough
   Step 2's "multinomial likelihood ... compositional shape data"
   addition (a QA-pass fix) integrate cleanly with the rest of
   Step 2?

4. **Anything else that strikes you on a careful read** that
   warrants another revision cycle. Use your judgement on
   "significant enough" — the bar is a real methodology gap or a
   real factual error, not a wording preference.

## What NOT to do

- **Do not re-find items already addressed.** The changelog
  enumerates what each prior round caught and how it was fixed. If
  your finding looks like a re-statement of an earlier round's
  finding, drop it.
- **Do not do a generic full-document review.** This is a
  saturation check. The rubric is the four targets above. Treat
  anything else as out of scope unless it rises to "this warrants
  another revision cycle."
- **Do not propose substantive new analyses to add.** The
  preregistration's scope is fixed; adding analyses now is exactly
  what prereg discipline prevents.
- **Do not flag stylistic preferences, prose-quality issues, or
  minor formatting.** The QA pass already swept for these.
- **Do not flag absent items.** If something isn't preregistered,
  it isn't preregistered — that's a scope choice, not a finding.
- **Do not evaluate whether the work is interesting or
  publishable.** Out of scope.

## Output format

If you find **nothing significant enough to warrant another
revision cycle**, say so explicitly. State:

> "Round-3 saturation check returns no findings of magnitude that
> warrant a further revision cycle. The preregistration is ready
> to lodge subject to the planned statistician consultation."

This is the desired outcome.

If you find anything, structure findings by severity:

- **BLOCKING:** must fix before OSF lodgement. Binding claim,
  internal contradiction, real methodology gap the rewrite opened,
  factual error in the new content.
- **SHOULD-FIX:** would meaningfully strengthen the preregistration
  without rising to blocking severity. Bar: would I personally
  delay lodgement for this? If yes, SHOULD-FIX. If no, drop it.
- (No MINOR category. The QA pass already swept for minor issues.
  If a finding doesn't reach SHOULD-FIX, drop it.)

For each finding:

- Specific section / heading pointer in the prereg.
- What the problem is, in one or two sentences.
- Why it matters and which of the four rubric items it falls under.
- A concrete suggested fix.

End with a one-paragraph overall assessment: is this round-3
saturated, or is there real work remaining? Be specific about what
would change your verdict from "real work remaining" to "saturated."

## Cross-model note for Shawn

The same prompt is being run against ChatGPT 5.5 and Gemini 3 Pro
in parallel. Cross-model agreement (both find the same gap)
indicates a real issue. Cross-model disagreement (one finds, the
other does not) indicates the finding warrants extra scrutiny but
may be a model-specific artefact. Both reviews are saved for
provenance.
