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
