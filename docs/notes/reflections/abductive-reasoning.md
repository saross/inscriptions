---
priority: 3
scope: conditional
title: "Abductive Reasoning Investigation"
audience: "researchers and future instances"
conditions: "Update when the session produced a surprising finding,
  a belief revision, or a hypothesis that was tested and either
  confirmed or disconfirmed."
---

# Abductive Reasoning — inscriptions

Surprising-fact → probe → belief-revision sequences from sessions on
this project. Part of a cross-project research investigation into AI
reasoning patterns.

Only updated when a session produced a genuinely surprising finding
or a non-trivial revision of prior beliefs. The conditional trigger
keeps entries sharp — if I find myself writing a forced entry to
satisfy the template, the session didn't warrant one.

Entries numbered sequentially and dated.

---

## Entry 1 — 2026-04-22: zero-correction verifier on a 25-row bibliography

### Surprising fact

The `lit-scout-verifier` returned **0 corrections on 25 rows**. Every
Authors, Year, Title, and Cites field matched the re-queried
CrossRef/OpenAlex response. The verifier itself explicitly flagged
the result as surprising, given the documented base rates in the
project's own lit-scout case study:

- v1 (April 2026): 75% author-attribution failure rate on a 4-row
  spot-check of a 37-row table. The failure that motivated the
  proposer-verifier architecture.
- v3 (April 2026): 4% verifier-caught error rate on a 25-row
  Bayesian-archaeological-dating query (one Row 16 CrossRef family-
  name parsing error).

My prior going into today's verifier run, calibrated off those two
data points, was roughly 10–20% corrections expected. Zero was
genuinely unexpected.

### Probe

The verifier's own re-check was extensive: it specifically
scrutinised (a) 8-author rows for order fidelity (rows 11, 12, 18);
(b) Czech diacritic encoding for the SDAM cluster (rows 6, 7, 8, 23,
25); (c) non-CrossRef registries (Zenodo row 23 and arXiv row 25,
both of which returned CrossRef 404 as expected and were confirmed
via OpenAlex fallback); (d) composite/book/data DOIs (rows 2, 17, 23,
25). All passed. The verifier's confidence that the clean result is
genuine, not an artefact of permissive checking, is well-grounded.

Separately, I can cross-check against a partial signal: the proposer
explicitly applied Guard A (per-field metadata re-query) on rows 3,
5, 7, 9 and reported them clean. The verifier's re-check of those
four matched. If Guard A generalised silently to the remaining 21
rows — which it should, because Guard A is a procedure applied to
every candidate row before drafting, not a rule applied only to
spot-checked rows — then zero-correction is what a well-executed
proposer-plus-Guard-A pass should produce.

### Belief revision

The 75% → 4% → 0% arc is not a decaying base rate of lit-scout
reliability. It's a **function of which guards were actually running**
at each stage:

- v1: prompt-level "never fabricate" discipline only. Per the case
  study: this constraint failed for narrative-column authors because
  the retrieval happened for DOIs and titles, but the authors were
  synthesised from training-data memory at drafting time without a
  dedicated retrieval step. 75% failure rate.
- v3: Guard A (mandatory `metadata DOI` call, output used verbatim)
  fully in place at Phase 6 of the proposer. One missed row (out of
  25) because CrossRef returned an ambiguous family/given encoding
  for Philippe Lanos & Anne Philippe that the proposer parsed as
  "Philippe & Philippe." 4% failure rate.
- v4 (today): Guard A as in v3, plus a fresh-context verifier in the
  adversarial role (serial dispatch from the main thread). No
  CrossRef ambiguity of the Lanos-Philippe kind in this row set. 0%
  failure rate.

The prior belief being revised: *"lit-scout has an inherent
confabulation rate on narrative columns that a verifier pass will
typically catch at some non-zero rate."* The revised belief:
*"lit-scout with Guard A applied at the proposer stage produces
near-zero narrative-column confabulation. The verifier catches the
residual failures driven by upstream metadata-encoding ambiguities
(like the Lanos-Philippe family/given parse) that Guard A is blind
to, because Guard A trusts the API response verbatim and CrossRef
sometimes encodes names in a way the string template parses wrong."*

### Implications for practice

1. **Guard A is load-bearing.** The proposer-verifier architecture
   gets most of its reliability from Guard A's in-stream retrieval
   discipline, not from the adversarial verifier. The verifier is
   defence-in-depth catching upstream-encoding failures, not the
   primary safety net.
2. **Verifier catch-rate scales with metadata-encoding ambiguity in
   the query set.** Sets where the seed DOIs go through well-behaved
   publishers (JAS, PNAS, Nature, PLOS) will see near-zero catches.
   Sets that chain through historical / legacy / non-Roman-alphabet
   metadata will see more. Ancient history / classics queries
   (today's set) touched JSTOR rows at 1990s dates but no non-Latin
   alphabets — low ambiguity.
3. **The "don't trust clean results" reflex is still right, but the
   *reason* is different.** Not "verifier might have missed
   something"; more "the underlying metadata might have an encoding
   artefact Guard A is structurally blind to." Spot-check remains
   useful for catching that residual class, but on a much narrower
   suspicion surface than the 2026-04-17 v1 results suggested.

### What would change this belief

- A session where Guard A is in place but a spot-check finds a
  non-encoding authorship error. Would mean Guard A can fail even
  when retrieval succeeds — suggesting a drifted-proposer failure
  mode I haven't seen. Watch for this on the next long-chain run.
- A verifier that fires on a well-encoded set and still flags ≥1
  correction. Would suggest the zero-correction result today was
  lucky, not structural. Unlikely given the extensiveness of today's
  re-check, but not impossible.

### Source

Today's lit-scout + lit-scout-verifier run for the inscriptions SPA
bibliography. Draft: `/tmp/inscriptions-lit-scout-draft-2026-04-22.md`.
Verified report: `planning/bibliography-2026-04-22.md`. Case-study
comparison: `~/personal-assistant/notes/lit-scout-case-study.md`.

---

## Entry 2 — 2026-04-23: editorial-convention hierarchy — one-factor explanation revised to distance-dependent hierarchy

### Surprising fact

The comprehensive profile rerun found what appeared to be a clean one-factor explanation for the AD 97 editorial-spikes dip: the Antonine-era editorial convention anchors on AD 100 (round century) rather than on the reign boundary (AD 96/98); round-century beats reign-boundary. I was ready to commit to this reading and move on.

Then Shawn asked: "You've compared the Flavian/Antonine boundary (96/98) to the round century (100), but you've also flagged 235 (end of Severans) as a major peak. Should we check the other dynastic transitions?"

The question exposed that AD 235 is a **spike, not a dip** — contradicting the one-factor "round century beats reign boundary" rule. Both findings are real in the data; the one-factor rule can't account for both.

### Probe

Sorting the seven tested editorial-boundary years by distance to the nearest round-number attractor (round century, half-century, quarter-century):

| Year | Nearest round | Distance | Result |
|------|---------------|----------|--------|
| AD 97 | AD 100 | 3 y | DIP (ratio 0.25) |
| AD 192 | AD 200 | 8 y | DIP |
| AD 193 | AD 200 | 7 y | DIP |
| 14 BC | 15 BC (¼) | 1 y | DIP |
| AD 27 | AD 25 (¼) | 2 y | DIP |
| AD 212 | AD 200 / 225 | 12 / 13 y | SPIKE (ratio 1.46) |
| AD 235 | AD 225 / 250 | 10 / 15 y | SPIKE (ratio 1.86) |

The data pattern is cleaner than the one-factor rule: distance-to-nearest-round-attractor (≤ 8 years = dip, > 10 years = spike) matches all seven observations, whereas "round century beats reign boundary" fails on AD 212 and AD 235.

### Belief revision

Old belief: *Editorial convention in Latin epigraphic corpora is a two-option choice — editors default to the round century when close to one, otherwise use the reign-boundary year.*

Revised belief: *Editorial anchoring is a distance-dependent hierarchy. The convention prefers round-number attractors in order: round century > round half-century > round quarter-century > reign boundary. The closest attractor wins, and reign-boundary years appear as spikes only when no round-number attractor is close (> 10 years distant).*

The revised belief is strictly stronger — it has prediction content. For seven additional dynastic transitions scheduled for Thursday's test:

- **Near a round attractor (predict DIP)**: AD 96 (4 y from AD 100), AD 180 (5 y from AD 175).
- **Far from a round attractor (predict SPIKE)**: AD 138 (12 y from AD 150 and 13 y from AD 125), AD 161 (11 y from AD 150 and 14 y from AD 175).
- **Mid-range (ambiguous)**: AD 68, AD 69, AD 117.

### Implications

1. Informs the shape of `convention_SPA` in the main paper's deconvolution-mixture model (Decision 7). Was modelling it as uniform century slabs; a hierarchical weighted attractor profile (more mass at centuries, less at half-centuries, less again at quarter-centuries, residual on reign-boundaries only when far from rounds) is a better generative model → sharper deconvolution.
2. Potentially publishable as a standalone methodological subsection or as headline content for the FS-0 methods-paper split.
3. Generalisable beyond inscriptions — any editor-mediated aoristic corpus could exhibit analogous hierarchy-of-anchors behaviour. Promotion candidate for `~/personal-assistant/notes/llm-craft.md` if reproduces on a second corpus.

### What would change this belief

- Thursday's test on the seven new transitions produces results contrary to the distance-dependent prediction (e.g., AD 138 dips rather than spikes; AD 96 spikes rather than dips). Would suggest the hierarchy is not the right frame, or is dataset-specific, or is moderated by other factors (reign length? frequency of inscriptions to that reign? regional variation?).
- Replication on LIST's late-antique extension fails to reproduce the pattern for Diocletian / Constantinian / Theodosian transitions.

### How I noticed

Shawn's question. I was ready to commit to the one-factor reading. The prompt to "check the other dynastic transitions" wasn't a challenge to my interpretation — it was a request for more cases — but framing the pattern-across-cases test revealed the incompleteness of the one-factor rule. Worth capturing as a lesson for future similar situations: when I've reached a clean interpretation, stress-test it against the broadest available evidence, not just the cases that motivated it.

### Source

Session discussion 2026-04-23 with Shawn after the comprehensive profile rerun returned. Editorial-spikes test results at `runs/2026-04-23-descriptive-stats/outputs/artefacts.md`; drill-down at `drill-downs/year_97_neighbourhood.md`. Hypothesis + test plan captured as Obs 11 in `working-notes.md`; Thursday test and post-LIST extension in `planning/backlog-2026-04-22.md`.
