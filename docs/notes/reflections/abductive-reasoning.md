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
