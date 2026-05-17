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

---

## Entry 3 — 2026-04-24: Glomb, Kaše & Heřmánková (2022) is a null, not a template

### Surprising fact

I had scheduled a PDF re-read of Glomb, Kaše & Heřmánková (2022) "Popularity of the cult of Asclepius in the times of the Antonine Plague" to extract the empirical Antonine-Plague signature profile — magnitude, FWHM, onset character — for use as the fourth effect-size anchor (Antonine-anchored) in the preregistered H1 simulation. The expected artefact was a shape: "50 % dip, FWHM ≈ 25 y, smooth onset" or similar.

The re-read agent returned the opposite. The paper reports **no detected signal** for Asclepius-cult inscriptions around the Antonine Plague. Two-sample Kolmogorov-Smirnov test: KS = 0.11, *p* = 0.20 on N = 210 Asclepius-cult inscriptions vs a composition-matched random-LIRE control. The authors explicitly note that KS power is inversely proportional to sample size, so "no detected signal at N = 210" is either a true null or an N-limited null — either way, there is no empirical profile to anchor on from this paper.

The only empirical Antonine effect-templates the paper cites (Duncan-Jones 2018 on military diplomas; Romanowska et al. 2021 on Palmyra portraits) are both drawn from material cultures too narrow to generalise to the broad inscription-production distribution our analysis is built around.

### Probe

Verified by: (a) the Explore agent's systematic extraction of Figure 1 and Table summary values from the PDF, showing no distinguishable dip; (b) direct quotation from p. 6: *"there is no statistically significant rise in the number of inscriptions simulated for the cult of Asclepius either in the time of the Antonine Plague (ca 165–180 CE) or in the short time horizon after"*; (c) the 25-year time-block analysis (Figure 4) that shows the 151–175 CE block indistinguishable from adjacent blocks.

Cross-checked against my prior expectation: Glomb is cited in the project's prior-art scout (Scout 3) as "closest published template" for the Antonine signature. That framing — "template" — is what I'd internalised. It's wrong in the important direction: Glomb is methodologically adjacent (aoristic dating + Monte Carlo comparison against baseline) but substantively a null. My mental shortcut conflated "near in method" with "near in finding".

### Belief revision

Old belief: *Glomb, Kaše & Heřmánková (2022) provides an empirical Antonine-plague inscription-rate profile that can serve as the effect-size template for a preregistered power analysis. The "Antonine-anchored" effect-size target is distinct from and more concrete than the generic Decision 5 brackets.*

Revised belief: *Glomb et al. (2022) is a null result at N = 210. No empirical Antonine-plague signature in inscription data has been detected at publishable confidence. The correct preregistration strategy is (a) drop "Antonine-anchored" as a privileged H1 effect-size target — use only Decision 5's three generic brackets + a zero-effect calibration check; (b) demote the Antonine-specific H3b test from "confirmatory primary" to "preregistered exploratory replication of Glomb et al. 2022 and Duncan-Jones 2018 at larger N and on mixture-corrected data"; (c) re-cast Glomb as motivating prior — "at what sample size would a Glomb-type test become informative?" — rather than effect-size template.*

The revised belief is strictly stronger. It removes an unwarranted privilege, sharpens the preregistration's claims to what the evidence supports, and uses the Glomb null as a feature (motivation for the power analysis) rather than a bug (template that doesn't exist).

### What would change this belief

- A new paper detecting an Antonine signature in general Latin inscription data at publishable confidence. Would allow re-anchoring on a real template.
- Discovery that Glomb's N = 210 is the power floor, and our mixture-corrected full-corpus analysis detects a signal post-correction at larger N. Would mean the effect is real but was masked by noise and editorial-convention artefacts at Glomb's resolution — in which case Antonine-specific H3b becomes a confirmatory (not exploratory) test in follow-up work.
- Verification that the Duncan-Jones military-diplomas or Romanowska Palmyra-portraits profile generalises to broader inscription categories. Would restore a usable empirical template, probably at Romanowska's 30–50 % magnitude over ~15 y rather than Duncan-Jones's extreme military-administrative collapse.

### How I noticed

I didn't. The Explore agent's output contradicted the framing I'd given it. I had written the brief as "extract the Glomb et al. Antonine-Plague signature profile" — assuming there was one — and the agent correctly reported that no such profile exists in the paper. Credit to the agent's brief-following discipline (it didn't fabricate a profile just because the brief asked for one) and to the brief's "quote verbatim; if a number is absent from the paper, say 'not reported' rather than inferring" instruction.

This is a second data point for the pattern Entry 1 flagged around Guard A (per-field metadata re-query at drafting time) being the load-bearing reliability mechanism: I had *inferred* Glomb had a detected signal from a secondary summary (Scout 3's "closest published template" framing), not from the paper itself. Primary-source verification caught it.

### Implications

Applied immediately to the preregistration:

1. §4 Phase 1 H1 simulation: effect-size targets reduced to Decision 5 a/b/c + zero-effect calibration check; smooth Gaussian-tapered dip shapes matching each bracket's magnitude and FWHM.
2. §3 H3b hypothesis: Antonine-specific test reframed as exploratory replication, no committed effect-size expectation, reported against Decision 5 brackets.
3. §4 Phase 3 H3b: Antonine test at AD 165–180 runs on empire level, Asclepius subset (Glomb replication), military-administration subset (Duncan-Jones replication), conditional on per-subset n thresholds being met.
4. §9 adds the subset-filter-feasibility confirmation: LIRE text regex on `[Aa]esculap|[Aa]sclep` yields 358 rows (vs Glomb's N = 210; their filter was stricter — we either match exactly or report both).

### Source

Explore-agent PDF extraction 2026-04-24 (`a7d8aa16d878e56a1`). Commit `c901aae` applied the reframing to `planning/preregistration-draft.md`. Original Scout 3 report at `runs/2026-04-23-prior-art-scouts/scout-3-epigraphic-habit-proxies.md`.

---

## Entry 4 — 2026-04-24: pyzotero `q=DOI` semantic trap creates silent duplicates

### Surprising fact

`scripts/zotero_batch_add.py` created a duplicate of Carleton, Campbell & Collard 2018 PLOS ONE in the SDAM Zotero group library despite an explicit idempotency-by-DOI check. Both item keys (`T95BHV43` from the test run; `GF82TVAB` from the full batch run) have the PDF correctly attached and are correctly linked to the SPA collection. The agent correctly logged the second run as `created` rather than `already_complete`, and the duplicate was only noticed in post-run verification.

The cause, diagnosed by the agent after the run: **Zotero's `q=` FTS parameter does not index the DOI field.** `zot.items(q='10.1371/journal.pone.0191055', qmode='everything', limit=25)` returns zero hits even when that DOI is present on an item. Zotero's FTS indexes title, creator names, notes, tags, and attachment filenames, but not DOI. The idempotency check was therefore structurally blind.

### Probe

Agent's post-run diagnostic: ran a `zot.items(q='<doi>')` call against a DOI known to be present (the duplicate existed, so both item keys carried that DOI) and observed zero hits. Confirmed against a title-word query against the same item, which returned both items as expected.

This wasn't a bug in pyzotero — the library forwards `q=` to Zotero's REST API verbatim, and the API-side FTS is what's limited. The documentation at pyzotero.readthedocs.io lists `qmode` values but doesn't enumerate which fields FTS covers for each mode; the Zotero Web API documentation at [www.zotero.org/support/dev/web_api/v3/basics](https://www.zotero.org/support/dev/web_api/v3/basics) is where the field list lives, and even there it's not prominently surfaced.

### Belief revision

Old belief: *For idempotent writes via a search-before-create pattern, any reasonable "search by canonical identifier" query will work. DOI is a canonical identifier; `q=<doi>` should return matching items.*

Revised belief: *Search APIs differ in which fields they index. Before trusting a search-based idempotency check at scale, verify the query semantics on a known-positive case. For Zotero specifically, idempotency must use either (a) a locally-built index over all group items' `data.DOI` fields, or (b) the API's filter-based search if supported, not `q=` FTS.*

The revised belief was implemented immediately in the batch-add script: after the empirical failure, the agent added a `_build_doi_index()` function that pages through all items in the group once, extracts DOIs into a normalised dict, and checks new additions against that index. This pattern is now the project's default for any Zotero idempotency check.

### What would change this belief

A future Zotero API version that indexes DOI in FTS. Would let the simpler `q=<doi>` pattern work. Unlikely near-term; the Zotero API v3 has been stable for years.

A different archival-bibliography tool (e.g., Mendeley, EndNote Web, BibTeX-plus-git) with different query semantics. Same pattern would apply — verify before trusting.

### How I noticed

I didn't in advance. The agent caught it empirically after the duplicate was created, diagnosed the cause, fixed the script, and flagged the duplicate for manual UI-level merge in its final report. The catch was entirely post-hoc. The pre-launch review of the agent's brief specified "idempotency via DOI search before create" without specifying *which* search mechanism — I'd assumed `q=DOI` would work because DOI is a first-class field in Zotero. That assumption was untested.

### Implications

1. Immediate: one duplicate in the SDAM library awaiting manual merge (Shawn flagged this as his to handle).
2. Script-level fix already in place (`_build_doi_index` in `scripts/zotero_batch_add.py` commit `e26278e`, extended/reviewed in `6e8355b`). Safe to re-run.
3. Added to the project's failure-mode list in `continuity.md` under "Zotero FTS does not index DOI field" — documented as a gotcha for future instances.
4. Generalisable principle for pre-launch agent-brief review: when specifying a safety check, commit to a specific implementation pattern, not just the check's goal. "Search by DOI before create" allows many implementations, not all of which work; "DOI-index-lookup before create" is unambiguous.

### Source

Agent `a050742b9dd16db93` batch-add run 2026-04-24. Commits `e26278e` (initial script), `f820afb` (run log), `0822157` (follow-up script), `6e8355b` (follow-up fix with Europe PMC fallback and attachment-return parsing).

---

## Entry 5 — 2026-05-03: `git clean -fd` removes gitignored files inside untracked directories

### Surprising fact

During the sapphire git-state cleanup, `git clean -fdn` (dry-run) flagged the *entire* `runs/2026-04-25-h1-simulation/outputs/h1-v2/` directory for removal — including the gitignored `cell-results.parquet` (119 MB, ~5 h of sapphire compute to regenerate) sitting inside it. This contradicted my prior expectation that `.gitignore` patterns universally protect matching paths, regardless of where in the tree they live. The dry-run output was unambiguous: "Would remove `runs/2026-04-25-h1-simulation/outputs/h1-v2/`" — directory removal is recursive, and gitignore-pattern matching apparently does not interpose.

`git check-ignore -v runs/2026-04-25-h1-simulation/outputs/h1-v2/cell-results.parquet` returned empty — i.e. git did *not* consider this file ignored. The file matched the gitignore pattern `runs/**/cell-results.parquet` syntactically, but the path's directory ancestor (`runs/.../h1-v2/`) was itself untracked, and git's ignore-evaluation short-circuits in that case: it doesn't look inside untracked directories at all.

### Probe

Caught before running `git clean -fd` for real. The dry-run output was the only signal — I'd nearly run `git clean -fd` directly without dry-running first, and was about to delete ~140 MB of irreplaceable-on-this-timescale research artefacts.

Verified the diagnosis post-hoc by reading `man gitignore` more carefully:

> If a parent directory of pattern is itself excluded, the file is not re-included. It is not possible to re-include a file if a parent directory of that file is excluded.

This is for the *exclusion* direction (patterns can't override an excluded ancestor). The mirror behaviour for `git clean` is described in `man git-clean`:

> git-clean removes untracked files from the working tree.

— and the relevant subtlety isn't called out: untracked *directories* are removed wholesale by `-d`, and gitignore patterns *do not protect contents of untracked directories*. The `man` page says `-x` removes ignored files too; without `-x`, it skips files at the top level that are ignored, but still removes untracked directories regardless of what they contain.

### Belief revision

Old belief: *Files matching a `.gitignore` pattern are protected from `git clean` regardless of where they live in the tree. The pattern is the protection.*

Revised belief: *`.gitignore` protects files only when their directory ancestors are tracked. An untracked directory is opaque to gitignore; `git clean -d` removes it wholesale, including any contents that would individually match an ignore pattern.* The protection is **not** the pattern — it's the *combination* of the pattern *and* a tracked-ancestor path. Gitignore is a within-tree mechanism, not an absolute path-based filter.

### What would change this belief

A future git version that extends gitignore's semantics to look inside untracked directories during `clean`. Possible but unlikely; the current behaviour has been stable for many years and reflects a deliberate design choice (untracked directories are treated as a single opaque unit by clean, both for performance and conceptual simplicity).

A configuration option (e.g., a new flag like `git clean --respect-ignore-in-untracked-dirs`) that opts into the protection. Not currently available; if it appeared, the safety pattern below would be obsolete.

### How I noticed

The dry-run output ("Would remove `runs/.../h1-v2/`") combined with my knowledge that `cell-results.parquet` lived inside that path. The path-membership recognition was the trigger; the dry-run *result* alone wouldn't have flagged it (`git clean -fdn` doesn't enumerate the contents of dirs it plans to remove). I had nearly skipped the dry-run.

### Implications

1. **Immediate**: moved both gitignored artefacts (`cell-results.parquet` 119 MB, `install.log` 21 MB) to a sapphire-local archive directory before running clean, then restored after pull. Working tree clean; both artefacts preserved.

2. **Generalisable safety pattern**: before any `git clean -fd` (or `-fdx`) run on a working tree with untracked directories that *might* contain gitignored content:

   - Dry-run first (`git clean -fdn`) — **not optional**, even when you think you know what's there.
   - For each untracked directory in the dry-run output, list its contents and identify any gitignored files (`find <untracked-dir> -type f` plus knowledge of the project's `.gitignore` patterns).
   - Move those files to a safe location *before* running the clean. Restore after.

3. **Project failure-mode list**: added to `continuity.md` failure-modes section as "git clean -fd removes gitignored files inside untracked directories — preserve them deliberately first".

4. **Reasoning-pattern link to Entry 4** (pyzotero `q=DOI` trap): both entries record the same family of surprise — *I assumed a tool's documented behaviour applied universally; actually it applies only conditionally, and the conditions weren't surfaced in the docs I'd read*. Entry 4 was on a search-API's index-coverage; Entry 5 is on git's directory-traversal semantics. Different tools, identical reasoning failure. The pattern is: **before trusting a documented protection at scale, verify the precondition.** For Zotero FTS, the precondition was "DOI is indexed" (it isn't). For gitignore-during-clean, the precondition is "directory ancestor is tracked" (often isn't on machines that haven't pulled recently). The principle of **pre-launch verification of tool semantics on a known-positive case** that I derived from Entry 4 applies here verbatim — and I didn't apply it. The documented-but-leaky channel from "lessons learned" to "applied next time" is itself worth flagging (see this session's session-reflection.md Entry 3 texture note).

### Source

Sapphire git-state cleanup, 2026-05-03. Commits `3256744` (gitignore pattern broadening, applied after the parquet was preserved and the cleanup completed). Diagnosis from `git check-ignore -v` output + `man gitignore` re-read.

---

## Entry 6 — 2026-05-15: Hanson 2021's regional residual pattern is not in the paper

**Surprising fact.** During bucket-(c) item 2 of the dual-review triage, working through the H3c "qualitative pattern matches Hanson's map" clause, I asked an Explore agent to verify against the PDF. The clause attributed to Hanson 2021 a specific regional pattern: "over-production concentrated in Italy and along the Rhine/Danube frontier; under-production scattered in Britannia, Gaul peripheries, and other western edges of the Empire." The clause had been in the prereg since the original 2026-04-24 draft. The verification agent returned, with page-anchored verbatim quotes, that Hanson explicitly states "there does not seem to be any obvious pattern" (p. 147) and that sites from different regions are "evenly scattered" (p. 148). The attribution was a confabulation.

**Probe.** Three-stage check before changing anything substantive. (a) Second consolidated re-verification of every Hanson 2021 attribution in the prereg by a fresh-context agent — confirmed the regional-pattern absence with the same quotes and surfaced a second mischaracterisation (SR1's "polity × century resolution" wording — Hanson works at site level, not polity × century). All six other Hanson 2021 attributions verified exactly (β = 0.672 mean, Moran's I = 0.046 / z = 4.571 / p < 0.0001, etc.). (b) SDAM-AU library scan over all 8 Hanson items + 22 items in the `roman_demography` collection, with PDF abstracts read where Zotero metadata was empty, to look for any Hanson-corpus paper that *does* make a regional inscription-residual claim. None found. The relevant adjacent material (Hanson 2016 monograph's per-province urban analyses; Wilson 2012's North African temporal contrast; Hanson & Ortman 2020's civic-status residual patterning) addresses related but different objects. (c) The subsequent pre-lodgement citation audit caught a *third* confabulation (Duncan-Jones 2018 "~85 % step-down" — Duncan-Jones actually says complete cessation after AD 167 per Fig. 4 / Table 7.1). Three confabulations in one source, one document, surfaced by sequential adversarial reads.

**Belief revision.** Three layers, in increasing scope.
(i) **On the specific claim:** the H3c "qualitative map match" clause was dropped (Decision 16); H3c-spatial reduces to Moran's I clustering only — which is the verified Hanson finding.
(ii) **On the writing process:** my prior assumption was that the prereg's specific citations to Hanson 2021 reflected a careful reading. The reality is that the original drafting was produced under high conviction at session-level distances that didn't include verification against the source. The three confabulations all share a structural pattern — specific, paraphrased, plausible — exactly the failure mode CLAUDE.md's anti-confabulation rule names. The rule is not ceremonial; it is load-bearing project infrastructure, and the pre-lodgement audit was the right step.
(iii) **On project documents more broadly:** the citation audit was scoped to the preregistration. The decision log, working notes, changelog, and runs/-directory reports were not audited. They may contain similar confabulations. Whether that matters depends on which documents are public-facing — the decision log is in a public repo and will be read by Martin; some run reports cite specifics that have been picked up and re-cited elsewhere. Worth a broader audit before lodgement, or at minimum a flagged caveat that only the prereg has been audited.

**Method-level lesson.** The dual-review-into-triage-into-audit pipeline worked as designed. The dual review didn't *directly* catch the regional pattern — it flagged the clause as "unoperationalised researcher degree of freedom." The decision-making around how to operationalise it (the bucket-(c) item 2 deliberation: should we drop it or define a regional contrast?) forced the question "where exactly does Hanson say this?" — which forced the verification. Without the operationalisation deliberation, the clause would have stayed in the lodged prereg as a vague Hanson-attributed criterion, and the confabulation would have been caught (if at all) by a reviewer at journal submission. The lesson generalises: when a confirmatory clause is vague enough to defer, that vagueness is sometimes hiding a confabulation. Operationalising-or-dropping is the diagnostic.

---

## Entry 7 — 2026-05-17: the editorial-convention diagnostic's test statistic was wrong, and Decision 17 had to be superseded

**Surprising fact.** ChatGPT's round-2 review finding B3 ("convention component appears inconsistent with the stated Uniform aoristic SPA") was a paper-thin technical observation that turned out to dismantle the prior session's headline conceptual finding. The observation: under pure Uniform aoristic, an interval like [1, 100] deposits flat mass uniformly across all 100 years, not preferentially on AD 50. So the preregistration's claim that "intervals like [1, 100] and [101, 200] place aoristic mass on midpoint years by construction" is wrong as stated. But the SPA *did* show pronounced O/E ratios of 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 / 250 / 350 — these were the empirical basis for Decision 17's three-tier anchor-year `convention_SPA` structure. If the mechanism story was wrong, what was producing the ratios?

**Probe.** Three sequential diagnostics, each commissioned in response to the previous one's findings.

(a) **Interval-width diagnostic** (`runs/2026-05-17-interval-width-diagnostic/`). Decomposed the corpus by interval width and stratified the "spike contribution" at AD 50 / 150 / 250 / 350 by the width of the contributing inscriptions. Two findings: (i) the corpus is dominated by exact century templates ([1, 100] alone is 26.3% of the corpus); (ii) the 22.8× / 41.5× / 18.8× ratios were generated by the prior diagnostic's test statistic `int((nb + na) / 2)`, which makes wide-century-template midpoints (50.5, 150.5, 250.5) truncate to round years — conflating wide-slab loading with narrow midpoint-anchored intervals. Removing all narrow intervals (width ≤ 25) does NOT collapse the spikes — it *increases* the O/E to 25.1× / 48.3× / 25.2× (109% / 117% / 132% retained). The artefact is in the wide-template inscriptions, not in narrow midpoint-anchored intervals.

(b) **Empirical-SPA-shape diagnostic** (`runs/2026-05-17-empirical-spa-shape/`). Constructed the actual 5-year per-year-uniform-aoristic SPA over 50 BC – AD 350 and looked at it directly. Findings: no local excess at AD 50 / 150 / 250 (local excess relative to surrounding plateau: −77 / −79 / +22 — i.e. essentially zero, well within sample noise); the dominant narrow features are at *regnal* dates (AD 122.5 with spike-to-plateau ratio 1.61× driven by Hadrian's reign [117, 138] = 552 inscriptions plus [123, 123] = 1,304 inscriptions; AD 77.5 with ratio 1.51× driven by Flavian consular templates); the largest single discontinuity in the SPA is the +1,159 step at the 1 BC / AD 1 boundary. Decision 17's anchor-year three-tier structure (mass at year ≡ 0, 1, 50 mod 100; year ≡ 51 mod 100; reign-related curated 13-year list) was targeting features the actual SPA does not show.

(c) **Date-range-filtered SPA diagnostic** (`runs/2026-05-17-date-range-filtered-spas/`). Recomputed the SPAs under progressive `date_range` thresholds {0, ≤1, ≤10, ≤25, ≤50, ≤75, ≤100, ≤200, all}. Decisive findings: the regnal spikes *amplify* under narrow-precision filtering — AD 122.5 spike-to-plateau ratio rises from 1.61× → 4.96× → 13.83× as the threshold tightens from full → ≤25 → ==0. If the spikes were editorial artefact, narrow-precision filtering would dilute them; instead they concentrate. The century-boundary plateau-step pattern, in contrast, weakens decisively under narrow filtering (Pearson r between SPA(≤25) and SPA(>100) is only 0.34). The regnal spikes are *real ancient clustering*; the century-template plateaus are *editorial-encoding artefact*. A third regnal spike at AD 212.5 (Severan, [212, 217] = 728 inscriptions) emerged from this diagnostic.

**Belief revision.** Three layers, in increasing scope.

(i) **On the specific tier structure:** Decision 17 (three-tier anchor-year convention component: century / half-century-arithmetic / reign-related curated 13-year list) is superseded by Decision 20 (template-interval slab convention component: century slabs uniform on [1, 100] etc.; half-century slabs; reign-interval slabs uniform on dictionary-built reign intervals like [117, 138]). Year-precise inscriptions ([123, 123] etc.) stay in `genuine_SPA` as real ancient anchoring, not as artefact. This is a structural reframing of the central methodological contribution, not a parameter tweak.

(ii) **On diagnostic methodology:** when a diagnostic's "observed" statistic is something other than the analysis pipeline's actual computed quantity, the diagnostic can be internally consistent and externally misleading. The 2026-05-15 editorial-convention-hierarchy diagnostic used `int((nb + na) / 2)` to identify "anchor-year mass at AD 50 / 150 / 250" — a defensible test for the question "do interval midpoints cluster on round years?" but *not* the same question as "does the per-year aoristic SPA show anchor-year mass at those years?" The diagnostic's findings were correct *for the test statistic it used* but the prereg's framing inherited them as if they were findings about the SPA. Diagnostic outputs need to be cross-checked against the analysis pipeline's actual computed quantity before they ground methodology decisions. The general lesson: when commissioning a diagnostic, name the actual SPA bin computation as a default-included sanity check.

(iii) **On the project's anti-confabulation discipline.** Decision 17's anchor-year framing was not a *confabulation* in the citation-audit sense — it was internally derived from the project's own diagnostic, not falsely attributed to an external source. But it *was* a wrong-with-confidence claim about the data that survived multiple rewrites of the preregistration. The structural pattern is similar to a confabulation: high-conviction wording about specifics, internally consistent but empirically wrong, propagated through descendant documents until challenged by a different probe. The anti-confabulation rule in CLAUDE.md ("Before citing a specific number, filename, path, identifier, commit hash, config value, or quoted text in a claim to Shawn, re-read the source file") was designed for external citations but the *spirit* — re-verify specifics at the source rather than trust prior summaries — applies just as much to internally-derived empirical claims about the dataset. Decision 17's framing should have been pressure-tested against the actual SPA shape before it became Decision-log canonical.

**Method-level lesson.** The cascade of three diagnostics produced the right final picture, but the *first* diagnostic should have been the empirical-SPA-shape one — the most direct, most literal question "what does the SPA actually look like?" — rather than the interval-width decomposition which was responsive to ChatGPT's specific framing. The interval-width diagnostic was useful (it identified the test-statistic conflation as the source of the 22.8× ratios) but the empirical-SPA diagnostic was the diagnostic that *grounded* the reframing. When future diagnostic cascades start, consider sequencing the most-direct-question diagnostic first, then the responsive-to-the-specific-question diagnostics in service of explaining what the first one revealed. This isn't a hard rule — sometimes the most direct question is dependent on the responsive diagnostic to even be well-posed — but the default of "most-direct first" would have shortened today's cascade from three diagnostics to two.

**Second-order surprise.** Three rounds of adversarial review, a structured QA pass, and the comprehensive 2026-05-17 rewrite did not catch a related belief-revision-overflow error: the H3c residual analysis was repeatedly described as receiving mixture correction, but H3c residuals are computed from H3a's posterior, and H3a uses date-filtered counts (Decision 22), so H3c inherits H3a's date-filtered scope — the mixture isn't correcting anything in the H3c chain. I had narrowed H3a in Decision 22 ("the mixture corrects temporal analyses, not the cross-sectional H3a") but kept the "H3c-via-residuals" phrase in the *Mixture's role in the paper* bullet of Decision 22 itself, inheriting the pre-Decision-22 framing where H3a was assumed mixture-corrected. The 2026-05-17 rewrite carried that wording forward across the prereg's §2 / §3 / §6 / §9. Both ChatGPT 5.5 and Gemini 3 Pro caught this independently in round 3, as their cross-model-agreement BLOCKING finding. The structural cause: when a decision narrows scope (Decision 22 took H3a out of mixture correction), the decision's *consequences for derivative analyses* must be explicitly traced — H3c is derivative of H3a; if H3a is no longer mixture-corrected, H3c is also no longer mixture-corrected. The QA brief asked "are the decisions' consequences applied?" but didn't ask "have the decisions' logical implications for derivative analyses been traced?" The latter is a different and stricter question. Future QA briefs need both.


---

## Entry 8 — 2026-05-17: late-stage adversarial review at saturation does not imply coverage; role-framing matters

**Surprising fact.** A consultation pack was drafted for an external statistician (Martin, applied econometrician). Before sending the pack, two stand-in cross-model statistical reviews were run as a hedge against Martin's potential delay: ChatGPT 5.5 and Gemini 3 Pro, both in an "applied econometrician / statistician giving a targeted review before the actual statistician sees it" role. Both reviewers independently flagged two items: (i) the prereg-binding floor of ≥ 50 replicates per cell for the H2.1 recovery-simulation coverage rule is thin — a Wilson 95 % interval at n = 50 for a true 90 % coverage rate is [0.79, 0.96], so the per-cell pass / fail boundary is brittle and propagates noise into the global ≥ 90 % cells-pass rule; (ii) Pearson r ≥ 0.95 between recovered and true genuine SPA is too forgiving as the binding shape-recovery metric — Pearson r is scale- and shift-invariant and can remain above 0.95 even when localised mass is mis-allocated, which is precisely the failure mode the recovery simulation exists to catch. Both are basic statistical-rigour points. **Both should have been caught by any of the three prior rounds of adversarial review across two model families (dual Claude Opus 4.7, ChatGPT 5.5, cross-model ChatGPT + Gemini 3 Pro).** None of them was.

**Probe.** Compare the rubrics across the four review rounds.

- **Round 1 (dual Claude, prereg-failure-mode rubric):** researcher degrees of freedom; hypothesis → test → decision-rule failures; does-it-answer-the-question; logical / internal consistency; clarity. The rubric is structured around the *prereg-as-document* failure modes catalogued in the open-science prereg-discipline literature (Nosek, Simmons, Wagenmakers). It caught: H1 mis-filed as confirmatory (D11/12); H3b unfalsifiability and the Holm-Bonferroni family-size deferral (D15); the primary RQ answered only by an exploratory analysis (D12); H3c regional-pattern confabulation (D16); H2.2 "local neighbourhood mean" underspecified.
- **Round 2 (ChatGPT 5.5, comprehensive substantive review):** likelihood family; convention component mechanism; H3a scope; PPC trigger numericity. The rubric is broader but framed around the prereg's *substantive choices* — the model-and-data side. It caught: likelihood-specification gaps (D19); convention-mechanism inconsistencies driving D20; H3a-scope ambiguities (D22); narrative-vs-numerical PPC triggers (D25).
- **Round 3 (cross-model saturation, "find only what warrants revision"):** an explicit anti-comprehensive framing. It caught one cross-model BLOCKING (H3c-scope inheritance from D22 — a *logical implication* of D22 the rewrite hadn't traced) plus one single-model SHOULD-FIX from each model.
- **Stand-in reviews (applied-statistician role):** read the *operational parameters* of the methods — coverage thresholds, metric appropriateness, sensitivity completeness, robustness, identifiability of the estimands. Found the n = 50 replicate-floor brittleness and the Pearson-r blind-spot, plus five single-model items (aoristic-MC sensitivity; PP spatial autocorrelation PPC; severity tiers; three-case Moran's I guardrail; weighted `f_within` sensitivity).

None of the first three rubrics had "is this an applied statistician's recommendation?" as a target by construction. The first rubric was a document-discipline rubric (does this look like a competent preregistration?); the second was a substantive-choice rubric (does this likelihood / mechanism / scope work?); the third was a saturation rubric (is there anything new worth flagging?). All three were legitimate; none was operationally-focused on the statistics. The stand-in-statistician reviews were operationally-focused by construction.

**Belief revision.** Three layers, in increasing scope.

(i) **On the specific items.** The replicate-count floor and Pearson r supplementary are real gaps, not minor refinements — at n = 50 the Wilson interval is wide enough that the per-cell pass / fail rule is genuinely brittle, and Pearson r can stay high while the recovered shape is materially wrong in localised ways. D27 (bump floor to ≥ 100; add Wasserstein-1 supplementary) closes both gaps. This is a normal corrigible-by-amendment situation; both items are now in the prereg.

(ii) **On the prior model of adversarial review.** The implicit prior model was something like "more rounds of adversarial review → more coverage → eventually saturation = found everything material." Each round was framed as catching what the previous round missed; round 3's saturation rubric was the explicit terminal "no more revision cycles needed" gate. The cross-model agreement on the saturation-check verdict ("ready for Martin") was treated as the load-bearing signal that coverage had been reached. **The stand-in reviews falsified that model.** Coverage is not document-conditional — it is *role-conditional*. The three prior rounds saturated under their respective rubrics, but the rubrics' coverage was structurally incomplete in the operational-statistics dimension. A document can saturate against multiple rubrics simultaneously while remaining underexamined in a dimension none of the rubrics target.

(iii) **On adversarial-review methodology more generally.** The corollary: for late-stage adversarial review at a saturation gate, *running multiple role-framings is a coverage strategy, not a redundancy*. Each role-framing has a different prior about what makes review-worthy gaps. Prereg-failure-mode rubric (open-science discipline lens); substantive-choice rubric (methodology lens); applied-statistician rubric (operational-rigour lens); subject-matter-expert rubric (domain-knowledge lens, which Martin will provide); software-engineer-reviewing-implementation rubric (code-feasibility lens, which the next-session pymc-scaffold work will probe). These rubrics don't substitute for each other — they cover *different* surfaces of the same document. Saturation under one rubric is genuinely useful (it tells you the prereg is well-specified by that rubric's lights); it just isn't coverage in the document-conditional sense.

**Method-level lesson.** The stand-in-cross-model-review pattern is now part of the methodological toolkit. For future high-stakes documents (preregistrations, conference papers, grant proposals, anything pre-publication or pre-lodgement): run at least two role-framings before signoff, and prefer cross-model agreement on findings as the high-signal triage filter (per Obs 37 in working-notes). The marginal cost of one additional role-framing is low (LLM cycle); the upside is real (cross-model agreement on basic-rigour items is a meaningful catch). The pattern doesn't substitute for a human expert reviewer — Martin still gets the pack — but it fills coverage gaps left by adversarial-rubric review and reduces the bandwidth cost on the human reviewer who would otherwise need to identify those gaps.

**Second-order observation.** This entry was easy to write because both stand-in reviewers happened to agree on the same two items — cross-model agreement made the "this is a real catch, not a noise" judgement straightforward. If only one stand-in reviewer had flagged the replicate-count issue, I would have triaged it down as a single-model catch and possibly deferred it as not-load-bearing. The cross-model orthogonality at saturation produced both the catch and the confidence in the catch. The lesson generalises: cross-model framing is doing two jobs at once — improving coverage *and* providing the credibility signal for the items found.
