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

---

## Entry 9 — 2026-05-20: pandoc-PDF URL overflow has two independent root causes; xurl-alone is necessary but not sufficient

**Surprising fact.** During the fourth pre-lodgement fix cycle on the OSF supplementary PDF, long DOI URLs in the §13 references list overflowed the right page edge — examples included `https://doi.org/10.1371/journal.pone.0191055` (Carleton et al. 2018) and `https://doi.org/10.1080/00031305.2018.1549100` (Gelman et al. 2019), both truncated mid-character at the page boundary. The standard advice for this class of problem — and the advice I had committed v3 of the PDF on — is to add the `xurl` LaTeX package, which redefines `\url` to allow line breaks at any character. I added xurl via `--include-in-header=...`, confirmed it loaded (visible in the LaTeX intermediate at line 95), regenerated, surfaced the PDF to Shawn as "fixed." Shawn opened it and the URLs were still overflowing.

**Probe.** Inspect the pandoc-generated LaTeX intermediate `/tmp/osf.tex`. Search for `\href` occurrences: **zero**. Search for `\url` occurrences: **zero**. The URLs are present as literal text. Pandoc's default markdown reader does not autolink bare URIs — that requires the explicit reader extension `+autolink_bare_uris`. Without it, pandoc renders bare URLs in the markdown source as **plain text**, not as hyperlink macros. xurl modifies the typesetting of `\url{...}` — it cannot break plain text tokens.

Hypothesis: the PDF pipeline has two independent stages where URLs can fail to break: (a) the markdown → LaTeX stage, where pandoc must produce `\url{...}` or `\href{...}` for URL handling to engage downstream; (b) the LaTeX → PDF stage, where `\url`'s default typesetting forbids mid-token breaks unless a package like xurl loosens it. Solo xurl addresses (b); solo `+autolink_bare_uris` addresses (a); the pre-v3 state addressed *neither*; v3 addressed *only (b)*; the fix requires *both*.

Test: regenerate with `-f markdown+autolink_bare_uris` plus the existing `--include-in-header` containing `\usepackage{xurl}`. Re-inspect LaTeX intermediate: `\url{...}` macros present for every bare URL in the source. Regenerate PDF. Visual scan of the references page: all URLs now wrap cleanly.

**Belief revision.** Three layers.

(i) **On the specific issue.** Pandoc's default behaviour is to *not* autolink bare URIs — they pass through as literal text. The `+autolink_bare_uris` extension is required to turn them into `\url{...}` macros. This is a documented behaviour but easy to overlook because most pandoc tutorials assume markdown sources have URLs in angle brackets `<...>` (CommonMark autolinks) or in reference-style hyperlinks `[text](url)`, both of which pandoc DOES autolink by default. Bare URIs in the prose body are the case `+autolink_bare_uris` exists for.

(ii) **On the standard advice for this class of problem.** "Add xurl" is the StackOverflow / pandoc-forums standard advice for URL overflow in pandoc-PDF outputs. The advice is half-right: xurl is necessary if URLs overflow because they're typeset as unbreakable tokens. But it's incomplete advice if pandoc isn't producing those tokens in the first place. The standard advice assumes pandoc *is* producing `\url{...}` — which it does by default for angle-bracket-wrapped and reference-style URLs, but not for bare URIs. The asymmetry is invisible in the rendered output (you see URL overflow either way) and only becomes visible at the LaTeX-intermediate stage.

(iii) **On debugging PDF-generation pipelines more generally.** When a layout fix doesn't appear in the output, the temptation is to assume the fix needs to be larger / stronger / wrapped in additional packages. The actual lesson is more boring: **check the intermediate stage before assuming the source-side fix worked.** Pandoc → LaTeX → PDF has three independent stages; each can introduce silent failures; the intermediate is cheap to inspect (`pandoc -t latex --standalone -o /tmp/check.tex`) and contains the actual evidence about which stage the failure lives in. The 15 minutes spent on this diagnostic loop after v3 was committed were 15 minutes that would have been zero minutes if I'd inspected the LaTeX intermediate before v3's "ready" claim.

**Method-level lesson.** For pandoc-to-PDF pipelines producing publication-grade documents: spot-check the intermediate after every non-trivial source-side change. If a layout fix doesn't show up in the rendered output, the failure is almost certainly upstream of the LaTeX-to-PDF stage that the fix targeted. The cost of one `pandoc -t latex --standalone` invocation is seconds; the cost of committing a wrong "fixed" claim and discovering the failure later (in front of the user, or worse, in a permanent deposit) is much higher.

Working-notes Obs 42 carries the operational guidance for the specific issue. The wider abductive lesson is the one this entry captures: **silent multi-stage pipelines need stage-by-stage verification**, not end-to-end "did the output change?" verification. The latter can't distinguish between "fix applied to wrong stage" and "fix wasn't enough." The former can.

**Second-order observation.** This entry was easy to write because both stand-in reviewers happened to agree on the same two items — cross-model agreement made the "this is a real catch, not a noise" judgement straightforward. If only one stand-in reviewer had flagged the replicate-count issue, I would have triaged it down as a single-model catch and possibly deferred it as not-load-bearing. The cross-model orthogonality at saturation produced both the catch and the confidence in the catch. The lesson generalises: cross-model framing is doing two jobs at once — improving coverage *and* providing the credibility signal for the items found.

---

## Entry 10 — 2026-05-22: f_within is materially weighting-sensitive; the unweighted 30 % is the conservative reading, not the full story

**Surprising fact.** The preregistered §5 three-weighting sensitivity (Block 6 of the 2026-05-22 talk-prep work) returned material divergence in a direction I did not anticipate. The three variants:

| Weighting              | f_within median | 95 % CI         |
|------------------------|-----------------|-----------------|
| Unweighted (binding)   | 0.300           | [0.240, 0.366]  |
| Population-weighted    | **0.496**       | [0.393, 0.610]  |
| Inscription-weighted   | **0.421**       | [0.337, 0.512]  |

Median spread across variants is 0.196, more than three times the primary CI half-width (0.063). Per the prereg's §5 decision rule, this triggers a "flag as limitation in the paper" outcome. But that "limitation" framing understates what the data is actually saying. The population-weighted variant — where each city contributes to the variance numerator + denominator in proportion to its population — gives f_within ≈ 0.50, roughly *double* the unweighted estimate.

I had braced for this sensitivity to come back robust (a "yes, the answer doesn't change much under different weighting choices" check). It did not. The three weightings disagree by a factor of 1.65×.

**Probe.** What does it *mean* that f_within is bigger when cities are weighted by their size? Two candidate explanations.

Candidate A: the sample's noise-vs-signal ratio varies systematically with city size, and weighted variances reduce the influence of noisy observations. Specifically: small cities have small inscription counts (the minimum is N = 1 in the LIRE-Hanson join). Small counts have high *relative* uncertainty — the NegBin variance at low mu is large compared to mu — so the *systematic* contribution of population to log expected count is masked by the *random* contribution of sampling noise. Weighting by population (or by inscription count) reduces the influence of these high-noise observations. The weighted f_within is therefore a "cleaner" measure of the population-attributable variance, with less noise contamination.

Candidate B: population's *substantive* role in inscription production is genuinely different at different city sizes. Bigger cities might have more diverse mechanisms by which population produces inscriptions (more workshops; more occupational specialisation; more elite patrons commissioning monumental epigraphy); smaller cities might have a thinner palette of inscription-producing mechanisms, dominated by individual elite/military presence rather than by population-driven mechanisms. Under this reading, the weighted variants aren't "cleaner" — they're answering a different question: "within the cities where systematic population-driven inscription production is operating, how much does population explain?" vs the unweighted "across all cities, how much does population explain?".

Both candidates predict the same direction of effect (weighted variants give bigger f_within); they differ in interpretation. Candidate A is a "this is the right number to quote" story; Candidate B is a "the choice of weighting is itself substantive" story.

Test: examine the *distribution of within-province population deviations* in the small-N tail vs the large-N body. If candidate A is right, the small-N tail should look noisier (more dispersed deviations relative to systematic population variation); if candidate B is right, the small-N tail might look qualitatively different (e.g., truncated, sparse, with discontinuous patches reflecting individual cities rather than continuous population gradients).

Test not yet run — this is a session-close abductive note, not a completed investigation. Logged for future session.

**Belief revision.** Three layers.

(i) **On the specific number.** I had been quoting "30 % of city-to-city variation attributable to within-province population" as the talk's headline. That number is correct as the prereg-binding answer. But the prereg's reason for choosing unweighted variance as the primary is methodological (it's the simplest, least-confounded denominator definition), not substantive. The substantive headline-finding is more nuanced: *at least* 30 % is population-attributable, and *up to* roughly 50 % under weightings that focus on the cities where systematic relationships are sharpest. The talk should report 30 % as the conservative reading; the paper should walk through all three weightings and let the reader see the range.

(ii) **On the prereg's §5 sensitivities more generally.** I had been thinking of the §5 sensitivities as a list of "checks the prereg includes for due diligence". They are also (often) *substantive analyses that answer related but distinct questions*. The three-weighting result here is a case where the "sensitivity" is at least as informative about the underlying phenomenon as the "primary". Going forward, every §5 sensitivity should be approached as a potentially-substantive analysis, not just a robustness check, and the paper should give them analytical space rather than relegating them to a limitations subsection.

(iii) **On variance-partition estimands more generally.** The "fraction of variation attributable to X" question is intuitively unambiguous but technically depends on which variance you're computing — which is sensitive to how observations are weighted. This is a known property of variance decompositions in mixed-effects models (the difference between "marginal R²" and "conditional R²" in Nakagawa & Schielzeth 2013 is a special case), but I had not internalised it as something that could matter *substantively* for this specific result. Going forward, any variance-fraction estimand I quote will get the multi-weighting decomposition examined as part of the primary reporting, not as a sensitivity.

**Method-level lesson.** When a sensitivity analysis is preregistered to "report alongside" the primary, *report alongside* should be taken literally — give it analytical space in the primary write-up, not just a footnote in the limitations. The three-weighting sensitivity is the right test for whether a variance-fraction estimand is robust to its denominator choice. When it isn't robust, that's information, not a problem to be hand-waved. The prereg's §5 framing — "exploratory sensitivities answering related but distinct substantive questions" — is precisely right; it took the empirical result to land that framing as more than a paragraph.

**Second-order observation.** This was a surprise I would not have detected without running the sensitivity. The talk's slide 6b reports the 30 % unweighted figure as the headline, and that's correct under the prereg's binding rule — but a reader of the slide alone would not know that population's contribution roughly doubles under reasonable alternative weightings. The B12 backup slide ("Why both frequentist and Bayesian?") doesn't carry this nuance either. If a curious audience member asks "how robust is the 30 % to weighting choices?", the honest answer is "not very — the population-weighted variant is ~ 50 %, and the prereg flags this as a limitation". I should have folded this into the deck more explicitly; it's the kind of substantive nuance the talk's pedagogical-clarity rewrite tended to elide. Worth raising in the Adela-feedback-incorporation pass next session.


---

## Entry 11 — 2026-05-22: the SMT-saturation diagnosis is a one-layer-down lesson about benchmarking compute-bound workloads

**Surprising fact.** A pymc/pytensor Bayesian mixture-recovery grid running on sapphire (Ryzen 9 7900, 12 physical / 24 SMT cores) was 3-4× slower than the standalone single-fit benchmark. The prior session's smoke-test had benchmarked three concurrency configurations:

| Config | Per-fit wall | Throughput |
|---|---|---|
| Standalone (1 fit) | ~14-18 s | — |
| Bash-parallel 20 procs | 17-32 s (avg 26 s) | 0.59 fits/s |
| joblib loky n_jobs=20 | 50-115 s | 0.25 fits/s |
| Subprocess-pool n_jobs=20 (chosen) | ~50 s | 0.19 fits/s |

The smoke-test author concluded that subprocess startup overhead explained the gap between bash-parallel (0.59 fits/s) and subprocess-pool (0.19 fits/s). On that reasoning, the chosen orchestrator was intrinsically ~ 3× slower than the optimum and there was no fix short of rewriting the orchestrator.

I had been ready to accept that conclusion. The fix turned out to be entirely different and operated on a different layer of the system.

**Probe.** A background investigation agent re-examined the live grid (PIDs of all 19 workers, `/proc/PID/cpu_allowed_list` reads, `vmstat` snapshots, `ps` with `-o cpu_allowed`, py-spy-style stack samples). Three observations layered into the diagnosis:

1. **SMT pairing**: in steady-state ps snapshots, **7 of 12 physical cores hosted 2 workers via SMT siblings**; 5 hosted 1 worker. 14 of 19 workers (74%) were in SMT-contended pairs. The kernel scheduler had distributed workers across the 24 logical CPUs roughly evenly — but "evenly across 24 logical CPUs" maps to "unevenly across 12 physical cores".

2. **Per-worker CPU% looks fine**: each worker really IS at ~ 100% of its allocated logical-CPU slice. The contention is *between* SMT-paired workers at the silicon level, not at the OS-scheduler level. Per-process `%CPU` accounting can't see this — it reports the worker's own utilisation of its allocated thread, not the contention with its SMT sibling for shared per-core resources (L2 cache, FPU dispatch, branch predictor, memory controller queues).

3. **`vmstat` shows the missing time**: under the grid's load, `vmstat` reports `us=79 id=21`. The 21% idle is wall-clock that's invisible to per-worker accounting but real — it's the silicon waiting on resource contention between SMT pairs. That 21% is roughly the slowdown factor relative to non-paired workload.

The fix predicted from this diagnosis: cap `n_jobs` at the physical-core count and pin to logical CPUs 0-11 (the first SMT thread of each physical core), avoiding SMT siblings entirely.

**Hypothesis tested + confirmed.** Predicted post-restart per-fit times under `n_jobs=12 + taskset -c 0-11`:

| Cell N | Predicted | Measured (post-restart) |
|---|---|---|
| N = 2,000 | 20-25 s | **~ 18 s** (slightly better) |
| N = 10,000 | 29-36 s | **~ 30 s** (within range) |
| N = 50,000 | 45-72 s | **~ 50 s** (low end of range) |

Predicted total wall-clock: 25-35 h. Measured trajectory: **31.6 h**. The restart agent ran the predict-then-measure protocol and confirmed both the per-fit timings AND the aggregate wall-clock match the SMT-pinning model within the predicted ranges.

**Belief revision.** Three layers, in increasing scope.

(i) **On the specific bottleneck.** I had been ready to attribute the slowdown to orchestrator-level overhead (subprocess startup, pytensor compile-cache locks, joblib coordination). All of those were ruled out: subprocess startup amortises to negligible because each cell runs 100 fits per python invocation; compile-cache locks would show as `D` state in `ps`, not `R` (workers were 100% in `R`); joblib coordination cost was already eliminated by using a plain subprocess pool, not joblib. The actual bottleneck was at the silicon layer — SMT-sibling contention — invisible to all of the higher-layer diagnostic tools the smoke-test had used. Lesson: when the obvious software-level mechanisms have been ruled out but the gap persists, look one layer down (silicon scheduling, NUMA, memory bandwidth) before declaring the workload intrinsically slow.

(ii) **On the smoke-test pattern more generally.** The smoke-test had benchmarked three configurations and chosen the best of the three. What it had NOT done was benchmark across `n_jobs` *values* within a configuration. The 0.59 fits/s "bash-parallel 20 procs" result was a transient — short-lived shells in the smoke-test didn't all coexist for the full window. Under steady-state contention (which the live grid actually runs in), every concurrency config gives 50-100 s/fit because they're all SMT-saturated above n_jobs=12. The smoke-test missed this because it was comparing orchestrators, not n_jobs values. Going forward, any concurrency benchmark needs to sweep `n_jobs` from `physical_core_count − k` to `physical_core_count + k` to see the knee-of-the-curve, not just pick the best orchestrator.

(iii) **On benchmarking compute-bound workloads more broadly.** The smoke-test had ALSO assumed that per-fit time would be independent of N (cell sample size); empirically N=2,000 cells take 62 s pre-restart and N=10,000 cells take 90 s pre-restart (44 % increase, not constant). That assumption was a second source of wall-clock under-projection: the smoke-test extrapolated from N=2,000 timings, missing the N-scaling cost. For future grid-scale Bayesian workloads on memory-bandwidth-sensitive hardware, the benchmark sweep needs both axes: `n_jobs × N`, not just `n_jobs` at one fixed N. The Ryzen's shared L3 cache (32 MB across two CCDs) is the latent variable explaining the N-scaling cost; larger N means more posterior-draw memory pressure means more cache-miss latency.

**Method-level lesson.** *Predict-then-measure is the discipline that distinguishes a defensible diagnosis from a confident guess.* The background investigation agent did three things that made this entry possible: (i) it stated a quantitative prediction (n_jobs=12 → ~ 25-35 h wall-clock; per-fit ~ 17-25 s at N=2,000) before the restart; (ii) it pre-specified an early-halt threshold (> 35 s/fit after 5 cells = halt and report); (iii) it measured the actual post-restart timings and compared to the prediction. The prediction held. If it had failed, the post-restart agent would have halted the grid and surfaced the failure — not autonomously expanded scope to debug. This protocol is more robust than "diagnose and fix" because it makes the diagnosis falsifiable. Going forward, any compute-infrastructure diagnosis I do should produce a numeric prediction before the fix is applied; the fix is only "validated" if the prediction holds within stated bounds.

**Second-order observation.** This is the second time in two sessions that a quantitative-prediction-with-bounded-test approach has produced a clean result (the first was the OSF lodgement adversarial-verifier dispatch from 2026-05-20, which made fix-quality falsifiable in the same way). The pattern works because it forces the diagnostic step to commit to a specific mechanism, not just a vague "this should be faster". A mechanism that predicts the wrong number is more useful than a mechanism that predicts no number, because the wrong-number case is informative — it tells you *which* layer of the model was wrong. The SMT-pinning prediction could have come back at "predicted 25-35 h, observed 80 h" — that would have told us SMT pairing was not the only bottleneck and there was a second layer to investigate (NUMA, memory bandwidth, something else). It came back within range, which means SMT pairing WAS the dominant bottleneck. Either outcome would have been informative; an unfalsifiable diagnosis would not.

The pattern generalises: research-side claims should similarly carry quantitative predictions where possible. The 30% within-province population partition is more credible because the prereg committed to a "supported / borderline / refuted" decision rule with specific thresholds; the f_within sensitivity result is more credible because the prereg committed to a "if shifts by > 50% of CI width, flag as limitation" rule. Each predicted-then-measured number is a falsifiable step. The grid-restart's success today is a small-scale instance of the same discipline.

---

## Entry 12 — 2026-05-24: the α=0.95 bias was framed as a corner pathology; F0a revealed it as a likelihood ridge across the whole α axis

**The surprising fact.** The H2.1 recovery-grid FAIL verdict on 2026-05-23 had identified three failure modes: `flat_baseline` 0% shape-pass (turned out to be a metric bug — see Entry 13); α=0.95 shape-pass collapsing from 78-88% at lower α to 22%; `regnal_cluster` at α=0.05 with α-coverage 31%. The natural mental model after Experiment A (which fit three α=0.95 cells under three sampler-effort tiers and saw the posterior fail to shift) was that α=0.95 is the boundary of a parameter-space region the model can't handle — a corner pathology, the model becoming unidentifiable as α → 1 in the usual mixture-near-boundary way. The fix candidates that follow from "corner pathology" are: tighter α prior, stronger constraints near 1, or simply scoping out the α ≥ 0.95 regime.

**The probe.** F0a (`runs/2026-05-24-followup-systematics/`) ran a different diagnostic: rather than re-fitting cells, walk through the existing 450 cells' summaries and compute mean α-bias by α_true marginalised over shape, tier_weights, N. No new compute beyond reading the summary JSONs. This is the cheapest possible probe — it asks "what does the bias look like across the whole grid, not just at α=0.95?" and answers from already-existing data.

**The result.** Mean bias by α_true: +0.070 at α=0.05 (over-estimation), −0.010 at α=0.30 (near-unbiased), −0.044 at α=0.50, −0.060 at α=0.70, −0.065 at α=0.95. The downward pull starts at α=0.50, has gained nearly all its eventual magnitude by α=0.70, and only marginally worsens at α=0.95 (Δ = +0.004 from 0.70 to 0.95). What collapses at α=0.95 is not the bias *magnitude* but the shape-recovery *pass rate* — by α=0.95, α̂ has been pulled far enough toward 0.5 that the recovered p_gen has to absorb the missing convention mass, and the Pearson r against truth breaks down. The bias is *bidirectional*: positive at low α, near-zero in the middle, negative at high α.

The per-shape breakdown sharpened the picture further. `regnal_cluster` is the only shape with *positive* α-bias at α ≤ 0.50 (+0.197 / +0.134 / +0.085 at α=0.05/0.30/0.50). The bias direction depends on which side of the mixture (convention or genuine) is "less complex" relative to the truth. Under the GRW smoothness prior on log p_gen, p_gen is the smoother side; the convention basis is therefore the less-smooth side; whichever side is more compatible with the truth's complexity wins, and α̂ moves toward whichever side has more mass to absorb. At low α_true with narrow truth → p_conv absorbs spikes → α̂ over-estimates. At high α_true with smooth truth → p_gen absorbs the smoothness → α̂ under-estimates.

**The belief revision.** The "corner pathology at α=1" frame is replaced by "likelihood ridge between α and shape complexity across the whole α range, with shape-conditional directionality". The downstream consequences are substantial:

- Fix candidates from the corner-pathology frame (tighter prior near α=1, parameter-space transform that compresses the boundary) are largely irrelevant. The bias is not concentrated at the boundary.
- The fix needs to address the ridge itself — either by constraining one side of the mixture (the empirical-Bayes calibration cohort approach, Entry 14's pivot), or by restructuring the prior so neither side has the "less smooth" / "less complex" advantage (the rigid-prior or ordered-mixture options Martin's review may surface).
- The bidirectional pattern matters substantively for the paper: regnal-clustered truth (which is exactly the kind of pattern the H3b Antonine and Crisis-of-Third-Century replications would test for) is the shape where the model *over*-attributes signal to convention, biasing the recovered p_gen toward smoother shapes than truth.

**Method-level lesson.** *When a failure mode shows up at one extreme of the parameter grid, run the cheapest possible marginalised diagnostic before locking in the "extreme is broken" frame.* The systematics diagnostic (read existing summaries, compute mean by axis) cost no new compute and revealed that the bias is structural, not local. The corner-pathology frame would have led to fix candidates that the data don't support. The structural-identifiability frame leads to the calibration-cohort pivot. The difference between the two frames is one diagnostic running over 450 already-computed cells.

The generalisation is broader than this project: any time a Bayesian model fails at one corner of a multi-dimensional grid, the first probe should ask "is this a boundary effect or a marginal pattern showing through more clearly at the boundary?" The answer changes the fix-space substantially. For the H2.1 case, the answer was "marginal pattern" and the fix is structural. For other models the answer might be "true boundary effect"; you only know by looking at the whole grid.

---

## Entry 13 — 2026-05-24: three textbook fixes for the H2.1 bias all came back negative — the bias is structural identifiability, not implementation

**The surprising fact (cumulative across three probes).** After Entry 12 reframed the bias from "corner pathology" to "likelihood ridge", the next question was *what kind of ridge* — i.e., which of the model's implementation choices is the load-bearing source. Three textbook candidate fixes had natural diagnostic tests:

1. Sampler is approximating the posterior badly under-power (cheap fix: more compute).
2. The α prior (Beta(2, 2), symmetric around 0.5) is pulling α̂ toward the middle (cheap fix: loosen to Uniform).
3. The centred Gaussian-random-walk parameterisation on `log_pgen_increments` has Neal-funnel geometry that traps the sampler in a biased region (textbook cure: non-centred reparameterisation).

I expected at least one of these to be the primary cause, with the other two contributing some smaller amount. The mental model was "find the dominant cause, fix it, see if α̂ shifts enough; the rest is noise". This is the standard textbook diagnosis-then-fix flow for Bayesian model failures.

**The probes.** Three sequential diagnostics, each designed to falsify one candidate cause and committed pre-probe to a quantitative threshold:

- **Experiment A** (`runs/2026-05-24-validation-investigation/`): re-fit three α=0.95 cells under three sampler-effort tiers (1k–4k tune, 2k–8k draws, target_accept 0.95–0.995). Decision rule: if α̂ moves > +0.03 between tiers, the sampler is the dominant cause.
- **F1** (`runs/2026-05-24-followup-alpha-prior/`): swap α prior from Beta(2, 2) to Beta(1, 1) ≡ Uniform(0, 1). Decision rule: if α̂ moves > +0.05 from baseline, prior pull is a "substantial contributor".
- **F3** (`runs/2026-05-24-followup-noncentred-grw/`): non-centred GRW reparameterisation. Mathematically identical prior, different sampler geometry. Decision rule: if α̂ moves > +0.08, geometry is the load-bearing cause.

**The results.**

- Experiment A: α̂ moved by ≤ 0.01 across the three tiers. ESS rose ~5×, R-hat fell from 1.04 to ≤ 1.04, divergences eliminated. *Same biased posterior, sampled more cleanly.* Cause ruled out: sampler effort.
- F1: α̂ moved by +0.025 on average (range +0.004 to +0.037). *Below the +0.05 threshold.* Cause ruled out: prior shape.
- F3: α̂ moved by +0.001 on average (range −0.003 to +0.005). *Three orders of magnitude below the +0.08 threshold.* Sampler-quality diagnostics improved massively: ESS-bulk 45-50× higher, R-hat collapses from ~1.04 to ~1.0008. *Posterior unchanged; engine substantially better.* Cause ruled out: funnel geometry. Side-finding: an unconditional sampling-efficiency improvement worth banking regardless of the headline question.

Three clean negatives.

**The belief revision.** The bias is *structural identifiability*: the data carries a likelihood ridge between α and p_gen complexity that the architecture cannot resolve, regardless of how it's sampled, what prior is on α, or how the smoothness parameter is parameterised. The information needed to nail α down is *not in the data* under the current model architecture and must come from outside the data (an informative prior derived from a corpus subset) or from a different model (a structurally constrained residual process that breaks the ridge by construction).

This is a stronger negative result than "the textbook fix didn't help much"; it's "three orthogonal textbook fixes each failed by orders of magnitude on their respective diagnostic threshold". The diagnostic chain produced a *positive* finding about structural identifiability through a sequence of well-designed *negative* findings about implementation.

**Method-level lessons.**

*(i) Diagnostic ordering matters.* Sampler effort → prior shape → sampler geometry → structural is the right order because it scales from cheap-to-fix to expensive-to-fix. Each diagnostic costs more time and tooling than the previous; each negative narrows the candidate-cause space. The wrong order — "what if it's structural?" first — risks committing to an expensive restructure when the cause is a simple sampler-effort issue. The right order — "what if it's just under-sampled?" first — burns the cheap diagnostics first and validates them as ruled-out before reaching for the expensive ones.

*(ii) Pre-committed thresholds make negatives informative.* Each F-experiment specified its decision rule *before* the data came back. F1's +0.05 "substantial contributor" threshold meant the +0.025 result was a clean rule-out, not an ambiguous "kind of moved a bit" finding. F3's +0.08 "substantial fix" threshold meant the +0.001 result was unambiguous. Without the pre-committed thresholds, the temptation is to look at +0.025 and say "well, that's *some* prior pull, let's keep it on the suspect list" — which is exactly the kind of motivated-reasoning that turns negative results into noise. With the thresholds, the rule-out is binary and the candidate-cause stack shrinks cleanly.

*(iii) Side-findings can have unconditional value.* F3's primary purpose was "does non-centred GRW fix the bias?". Answer: no. But its secondary effect — 45-50× ESS improvement, R-hat collapsing toward 1.0, divergences gone — is independently valuable. The non-centred parameterisation is adopted unconditionally for the production Stage 3 model regardless of whether the empirical-Bayes pivot's Stage 4 validation succeeds. The discipline that surfaced this: report sampler-quality diagnostics alongside the headline question whenever any model-structural change is tested. They're cheap to compute and frequently carry standalone value (candidate Obs 57). The fact that this was a *predicted* side-effect of non-centred reparameterisation in the Stan / PyMC user community helped — I expected the ESS gain; I just wasn't sure how large it would be.

**Second-order observation.** The forward-fit pivot (Entry 2, 2026-04-26) and the empirical-Bayes pivot (Entry 14, this session) share the methodological move "three sequential diagnostic negatives → structural redesign". For forward-fit, the negatives were the FP-inflation results from the H1 v1 simulation; for empirical-Bayes, the negatives are F1 + F3 (and the marginal F0a finding from Entry 12 that re-frames the problem space). Both pivots came from running diagnostics honestly, pre-committing to decision thresholds, and treating clean negatives as informative rather than as failures. The methodology-paper section on validation gates should make this explicit: the gates aren't quality control, they're the engine that drives structural redesign. Candidate Obs 52 captures the diagnostic-ordering recipe.

---

## 2026-05-26 — Entry 15: the Mundlak f_within +9.89 pp shift; "modest" prior, "material" posterior; spec-binary encoded an unfounded assumption

The 2026-05-26 letter-count probe produced the cleanest belief-revision sequence in the project's recent history, with two intertwined surprising facts: (i) the within-province variance partition shifted +9.89 pp under letter-mass, well beyond Shawn's expected "modest"; (ii) the probe's own verdict-threshold structure had encoded an assumption — that the two units were rival operationalisations of one construct — that the data actively falsified. Both belief revisions matter; the second is the larger one because it reshapes how I should design sensitivity-probe specs going forward.

**The surprising facts (in temporal order).**

*Block 3 (Province / city rank shuffles).* Letter-mass reshuffled the top-N rankings substantially: Britannia dropped 12 ranks (#7 → #19); Ostia rose from #3 to #1; Hispania citerior dropped from #3 to #7; Germania superior dropped #4 to #10; Pompeii dropped #1 to #3; Cirta dropped #8 to #15. I had drafted the probe spec assuming the swap might be invisible at the empire level (Flag 1 SPA shape, Pearson r ≈ 0.88 — modest). What the rank-shuffle pattern showed was not noise but cultural-archaeological structure: frontier-military epigraphy is terse (Britannia, Germania superior, Cirta drop); Italian funerary monumentalism is letter-heavy (Latium et Campania holds #1, Venetia et Histria rises); Ostian commercial epigraphy is letter-heavy by genre (Ostia rises to #1). Writing this up coined the construct-distinction: *"inscription-count weights frequency of inscribing; letter-mass weights quantity of communication."*

*Block 4 (Hanson β).* Bootstrap CIs did not overlap: inscription-count β = 0.566 [0.543, 0.574]; letter-mass conservative β = 0.515 [0.463, 0.542]. Flag 2 MATERIAL. I had not formed a prior beyond "the swap will probably show *something*"; the magnitude of the gap (~ 1.2 model SEs apart, with non-overlapping bootstrap CIs) was sharper than expected.

*Block 6 (Bayesian Mundlak on sapphire).* Three variants ran cleanly in 4.3 min total wall-clock (much faster than the 45 min I had estimated; the harness is well-tuned). Inscription-count f_within = 29.94 % reproduced the talk-prep slide-6 punchline of 29.95 % to two decimals — a clean sanity-check on model + data + sampler consistency across seeds. Letter-mass f_within = 39.83 % — **+9.89 pp shift, MATERIAL** on the spec's threshold. Shawn's stated prior was "modest" based on two-year-old preliminary work; my own prior was anchored to his. The +10 pp shift was approximately a third increase in the within-province share, well outside either of our expected ranges.

**The probes.**

For the Mundlak shift, the post-hoc probe was the mechanism decomposition: β_within is roughly stable (0.587 → 0.559, ~ 5 % drop); β_between centres substantially toward zero (−0.248 → −0.158, ~ 36 % centring). The total-variance denominator (which includes the province random-effect variance) shrinks faster than the within-variance numerator, pushing f_within up. The substantive read: letter-mass partially strips out provincial-level "epigraphic habit" noise — the province-level cultural variation (Latin vs Greek vs frontier-military epigraphic styles; provincial elite practice) that drives ACT-counts more than CONTENT-counts. Within a province, city population predicts letter production more cleanly than it predicts inscription frequency.

For the spec-binary-encoding observation, the probe was Shawn's reframe itself: he read the Block 3 substantive writeup, named what was happening (*"explore both and consider the deltas between them, analogous to how we are looking at residuals in inscription-population relationships"*), and the binary-verdict structure dissolved. The probe was a single sentence — but the falsification was retroactive: it revealed that my spec's "any flag tripping → letter-count becomes the headline unit" rule had encoded an unfounded assumption that the units were rival operationalisations of one construct. The data showed they are partially-different constructs; the appropriate verdict structure should have allowed "adopt both as first-class measures" as an outcome.

**The belief revisions.**

*(i) Letter-mass and inscription-count are tracking partially-different signals at the variance-decomposition level, not just the SPA-shape level.* The Mundlak shift adds a third layer of empirical corroboration on top of the Block-2 SPA-shape Pearson r and the Block-4 Hanson-β gap. The `pilot_proxy` re-derivation (Obs 60; reign-interval-slab mass quadruples under letter-weighting) adds a fourth. The two-measure framework is overdetermined empirically — the units genuinely track different things, and the delta is informative across multiple analytical layers.

*(ii) Sensitivity-probe specs with binary verdict thresholds structurally encode an assumption — that the alternatives are rival operationalisations of one construct — that the data may falsify. When the data shows the alternatives are different constructs, the binary forces a false choice and erases the methodological contribution.* This is a method-level lesson rather than a project-specific finding. The four critical-friend stats checks (appropriate test? more powerful alternative? more current best-practice? assumptions hold?) should have a fifth question for unit-of-analysis decisions: *"Are these rival operationalisations of one construct, or different constructs?"* If the answer might be "different constructs", the verdict structure should allow "adopt both with delta as derived quantity" as an outcome. Captured in user-observation Obs 10 and the `_inbox` candidate for `notes/llm-craft.md`.

**Method-level lessons.**

*Substantive engagement breaks structural assumptions in the spec.* I coined the "acts vs content" construct-distinction during Block 3's substantive writeup, not during spec auditing. The spec's binary structure was invisible to me until Shawn surfaced the alternative. Engaging substantively with the data (reading rank shuffles as cultural-archaeological pattern, not as "which unit wins") is what surfaced the construct-distinction. The pattern: spec-auditing alone may not reveal structurally-encoded assumptions; substantive engagement with results-in-progress is what makes those assumptions visible.

*Direct credit-discipline matters for the research record.* When I drafted a user-observation crediting Shawn for the whole reframe, I erased my own coinage. Shawn corrected me directly: *"it was you who noticed."* The correction is now durable feedback (memory `2026-05-26-652990d9d646`). The research-record integrity issue is non-trivial: if Obs 58's "acts vs content" framing is later cited in the methodology paper, accurate attribution matters for how the contribution is understood. Default to claiming substantive contributions; over-claiming gets corrected; under-claiming systematically obscures co-research capability.

**Second-order observation.** The forward-fit pivot (Entry 2, 2026-04-26), the empirical-Bayes pivot (Entry 14, 2026-05-24), and this two-measure reframe (Entry 15, 2026-05-26) are now three project-internal pivots driven by validation-gate output. The first two were driven by simulation FAIL results that forced structural redesign. This one is different in kind: it was driven not by a FAIL but by a substantive-engagement observation that broke the spec's structural premise. The pattern generalises: validation gates can drive pivots through PASS-with-substantive-finding as well as through FAIL. The methodology paper should treat the gates as a *general* engine for structural redesign — both negative-result-driven and substantive-finding-driven — not just a quality-control mechanism.

---

## Entry 16 — 2026-05-29 → 2026-06-01: a unit that "looks like more data" carries less — a compound-sum design effect reverses the expected direction; and a 5-hours-late crash exposes a verification-layer mismatch

**Surprising fact (1).** Letter mass vastly exceeds inscription count (≈ 8.2 M letters vs ≈ 180 k inscriptions), so the intuitive expectation — held by me at the outset, and implicit in the project's treatment of letter mass as the richer measure (the "acts vs content" reframe, Entry 15) — is that letter mass is the *stronger* unit for detecting temporal change: more data, more power.

**Probe.** Shawn declined a convenience-scoped "letter-mass time-series is out of scope" and asked whether the reason was *principled* or just expedient. That forced a quantification: the Kish design effect of letter mass as the analysis unit (`scripts/letter-mass-design-effect.py`, `letter-mass-reachability.py`).

**Belief revision.** The expected direction reversed. Letter mass is not a count of independent events; it is a *compound sum* of per-inscription letter counts, and those counts are heavy-tailed (median 26, max 35,537). The variance of such a sum is dominated by its largest terms, so the Kish effective sample size `n_eff = (Σw)²/Σw²` collapses: per-city design effect ≈ 2.4, `n_eff` ≈ 0.42× the inscription-count effective N, and at the urban-area Phase-1 detection thresholds **0 of 1,044 cities are reachable under letter mass versus 5–7 under inscription count**. The richer content measure is the *temporally weaker* one. This scoped OSF Amendment 01: letter-mass confirmatory is confined to the cross-sectional H3a (which regresses per-city totals and so does not feel the design effect); the time-series stays exploratory.

**Method-level lesson (1).** When a candidate unit "looks like more data" because its raw total dwarfs the alternative (letters ≫ inscriptions), check whether it is a *count of independent events* or a *weighted / compound sum*. A compound sum of heavy-tailed weights can carry *less* effective information than the plain count it derives from — the design effect can swamp the apparent data-volume gain. The diagnostic is one cheap Kish computation and can reverse a scoping decision. This extends the standing critical-friend checks and Entry 15's "different constructs?" question with a further one for any unit-of-analysis choice: *"count or compound sum, and what is the effective N?"*

**Surprising fact (2) — a second-order, verification-layer revision.** The §5 production run crashed 5.7 hours in on `ModuleNotFoundError: No module named 'sklearn'`, *after* passing two adversarial `/audit` cycles, a benchmark, and a dry-run.

**Probe / revision.** The audits verified code *correctness* (logic, the Poisson-aoristic likelihood, the production-launch gate) exhaustively and found real issues; but the failure lived at the *environment* layer — an undeclared dependency on a venv built ad-hoc rather than from the lockfile — and the offending import was lazy, executed only at the final diagnostic step. None of four verification steps was the right check for that layer. Belief revision: verification rigour does not transfer across layers; "the code is audited" says nothing about "the machine has what the code needs," and an unattended multi-hour run needs a pre-flight that exercises every import path (or a fail-fast import check) precisely because lazy imports defer the failure to the most expensive possible moment.

**Second-order observation.** Both revisions share a shape: a quantity that *looks* sufficient at one layer — raw data volume; code correctness — is insufficient at the layer that actually governs the outcome — effective sample size; environment completeness. The recurring failure mode is *layer-confusion*: trusting a measure or a check drawn from the wrong layer. The cheap guard in both cases is the same move — identify the layer that actually governs and measure / check *there* (the Kish effective N for the unit decision; import-resolution for the run decision). A candidate generalisation for the cross-project investigation: when confidence is high but derived from one layer, ask explicitly which layer the next failure would come from, and whether anything has checked *that* one.

## Entry 17 — 2026-06-02: a "clean" lockfile refresh yields an environment that imports everything yet cannot read the project's own data — and the fix reproduces the very gap it was built to close

**Context / continuity.** This entry is, unusually, a direct test of the prior one. Entry 16 (2026-06-01) proposed a candidate generalisation for the cross-project investigation: *when confidence is high but derived from one layer, ask explicitly which layer the next failure would come from, and whether anything has checked that one* — coined after a 5.7 h run crashed on an environment-layer fault that four code-layer checks had missed. Task #9 this session was that remedy. The remedy bit.

**Surprising fact.** Refreshing `uv.lock` to the pymc-6 stack produced an environment in which all 15 runtime packages imported successfully — and `arviz.from_netcdf()` on a §5 posterior would fail. A clean, fully-resolved, internally-consistent lock left the project unable to read its own primary artefacts.

**Probe.** Checked the `.nc` magic bytes (`\x89HDF` — HDF5, not classic netCDF, so an HDF5 binding is mandatory); diffed the regenerated lock against both the prior lock and zbook's validated freeze. The arviz 0.x→1.x refactor had moved the netCDF backend from a hard dependency to an optional extra, so a clean resolve dropped h5netcdf and h5py — present until then only as arviz-0.x transitive leftovers. Declaring h5netcdf re-exposed the gap one level down: h5netcdf 1.8.1 declares only numpy+packaging, leaving the HDF5 binding to the caller, so h5py had to be declared too.

**Belief revision.** "A lockfile that resolves cleanly reproduces the environment that ran" is false across a major-version boundary: a major bump can relocate capability into optional extras, so a clean re-lock silently *removes* function the old lock supplied implicitly. The check that certifies an environment must therefore exercise the real operation — an actual `xarray→h5netcdf→.nc` round-trip — not a proxy for it.

**Method-level lesson — the recursion.** The pre-flight import check built as Entry 16's remedy *would have passed* on the broken environment: every import resolved; only the I/O failed. That is Entry 16's exact failure shape — a measure from one layer ("does it import?") treated as sufficient for an outcome governed by another ("does the real operation succeed?") — reproduced *inside the fix for that failure shape*. The `/audit` pass caught it: its top finding was precisely that the preflight tested h5py-imports rather than the netCDF write path, and the corrected check now round-trips the real write. So the generalisation did not merely survive a test; it predicted the weak spot in its own remedy.

**Second-order observation (for the cross-project investigation).** Entry 16's generalisation needs a corollary: *apply the layer-confusion check recursively to the remedy itself.* A check built in response to a layer-confusion failure is liable to the same error — testing a convenient proxy (imports resolve) for the governing operation (data round-trips). The discriminating question is not "did I add a check at the right layer?" but "does my check *do the thing*, or a stand-in that can pass while the thing fails?" The cheap guard is the same move applied once more — make the verification perform the real operation — which is also why the end-to-end bit-for-bit reproduction, not the unit-level reasoning, was the validation that actually settled it.

## Entry 18 — 2026-06-02 → 2026-06-03: a high shape-correlation certifies the recovered *curve* but is silent about its *uncertainty band* — the same layer-confusion, now living inside the validation metric

**Context / continuity.** A third instalment of the running cross-project thread (Entries 16, 17): a measure taken at one layer treated as sufficient for a property governed by another. This time the layer-confusion was not in a packaging check or an environment check — it was in the *validation metric itself*, and I nearly shipped its conclusion before testing the property it left unmeasured.

**Surprising fact.** The recovery grid validated the genuine-SPA reconstruction with posterior-median Pearson r ≈ 0.998 — excellent *shape* recovery — and I wrote "trust the timeline shape." But a re-fit band-calibration probe found the recovered *credible band* badly miscalibrated for sharply-peaked signals: pointwise 95% coverage falls from ~0.90 at N=2,000 to **0.23 at N=50,000** for the regnal-cluster shape. A near-perfect shape-correlation coexisted with a credible band that contained the truth less than a quarter of the time.

**Probe.** Re-fit a representative subset (the grid stored only the posterior median, not the band), extracted the per-bin posterior, and measured pointwise coverage by N. The pattern: smooth shapes calibrate (~0.99); peaked shapes degrade, worsening with N. Mechanism — Pearson r is shift- and scale-invariant, so it scores the *correlation* of the recovered curve with truth while saying nothing about whether the posterior's *spread* is honest; and the Gaussian-random-walk smoothness prior cannot represent sharp features, so at large N the posterior concentrates confidently on a slightly-too-smooth curve and the narrow band misses the true peaks.

**Belief revision.** "The model recovers the signal well" (high r) does **not** imply "the model's uncertainty about the signal is honest" (calibrated band). These are *different layers of the same object* — point estimate vs. interval — and a metric that certifies one is mute on the other. The downstream consequence is concrete: report the recovered median timeline, but do not present its credible band at face value in peaked regimes; the band understates uncertainty and the peaks are attenuated. The gate validates what we *use* (the de-fogged trajectory); it does not, on its own, license the error bars.

**Method-level lesson — the same move, a third domain.** Entries 16–17 were *imports-resolve* (proxy) vs *I/O-succeeds* (property), and *code-audited* vs *environment-checked*. Entry 18 is *shape-correlates* (proxy for "the reconstruction is trustworthy") vs *band-is-calibrated* (the property a reader will actually lean on). The discriminating question generalises cleanly across all three: **does the measure exercise the property the conclusion rests on, or a correlate that can pass while that property fails?** And the cure is identical each time — when in doubt, *measure the real property directly*. The one new wrinkle worth flagging for the investigation: here the proxy-gap was something I had *flagged in writing* ("honest-point-B: we validated the shape, not the band") and then almost left as a caveat. Flagging the gap is not closing it; running the measurement is. The reflex to upgrade from "I should note this is unvalidated" to "I will now validate it" is the cheap, decisive move — and it overturned a claim I had already put in front of the human.

## Entry 19 — 2026-06-03 → 2026-06-04: a "limitation" of the method was an artefact of a pass/fail threshold we wrote ourselves — the layer-confusion theme, applied to a criterion

**Surprising fact.** Adjudicating the recovery grid under the corrected criterion, Grid A produced a persistent gap: 91.9 % of in-envelope cells passed if non-converged cells counted as failures, 98.5 % among convergent cells only. The entire gap was 24 cells — and *all 24 were the flat-null shape*. A "limitation" (the flat null doesn't converge) that I documented at length and built a reporting decision (headline-B vs diagnostic-A) around.

**The probe.** Three converging checks, prompted by Shawn asking for *principled grounds* rather than a reported choice. (1) **Decomposition** — under an R̂/ESS-only convergence test (dropping the per-replicate `n_divergences == 0` requirement), *all 60* flat in-envelope cells pass; the 24 failures were caused *solely* by the divergence gate, not by R̂ or ESS. (2) **Benignity test** — across 6,000 flat replicates, the ~10 % carrying a divergence recover the flat shape *no worse* than the clean ones (median W1 0.59 vs 0.55; Mann–Whitney p ≈ 0.36): scattered false positives, not biasing pathologies. (3) **Literature** — a sweep of Stan/Betancourt practice found *no* source endorses a zero-tolerance per-replicate divergence gate or any numeric rate threshold; the field standard is contextual investigation, and "a few divergences + good R̂/ESS = often good enough."

**Belief revision.** The flat-null "limitation" was not a property of the method. It was an artefact of a pass/fail threshold *we had chosen* — a zero-tolerance divergence gate stricter than field practice. Relaxing it to the field-standard rule (R̂/ESS + a benign-divergence check) collapsed the 91.9 %/98.5 % distinction into a single 98.6 %, dissolved the limitation, and retired a backlog re-fit. The elaborate adjudication of *how to report* the gap had been aimed one layer too high; the gap itself lived in the criterion.

**Why it belongs here, and what generalises.** This is the project's recurring layer-confusion theme (Entries 16–18) applied to a new layer: not a *check* aimed at the wrong layer (17), nor a *metric* silent about the layer that matters (18), but a *criterion* — a self-imposed threshold — mistaken for a finding. The diagnostic signature is identical across all four: an apparent property of the world that is actually a property of *our own instrument*, visible only when you doubt the instrument rather than the world. The transferable rule: **when a limitation is driven by a threshold you set, the threshold is the first hypothesis to test, not the conclusion to report around.** The near-miss — I had written that the gate was "stricter than field practice" while still treating it as a fixed constraint — is the same shape as Entry 18 (noticing the band, certifying the curve): the right observation, filed under the wrong action.

**Counterfactual that didn't happen.** Had Shawn accepted headline-B as the answer (it was defensible, and I'd recommended it), the amendment would have shipped a real "limitation" and a queued re-fit for a non-problem. The forcing function was his asking for *grounds* rather than a *choice* — which converted a reporting decision into an empirical question, and the empirical answer dissolved the decision.

## Entry 20 — 2026-06-04 → 2026-06-05: a track asserted "nearly done" was missing a binding confirmatory test — the believed-state, not the world, was the error

**Surprising fact.** After the H3a confirmatory blind run and the Latin H3c/SR1 rerun, I asserted the cross-sectional track was "nearly done." A systematic preregistration-obligations completeness audit (a fresh agent extracting every committed obligation and assigning a status) returned a verdict I did not expect: **H3c(i), the provincial-capital residual contrast — a *binding confirmatory* test (Decision 23) — had never been run**, and a *prerequisite* for the next phase (the H2.1 template-dictionary scan, Decision 20) did not exist. Both were UNACCOUNTED: pre-specified, no artefact, in no plan.

**Probe.** Verified directly against the prereg rather than trusting the audit: §3 line 81 + §4 line 345 bind H3c(i) on `P(contrast>0) ≥ 0.95`; grep confirmed "capital" appeared nowhere in either done REPORT. The gap was real. Closed it with the authoritative source (Hanson's own OXREP civic-status flag) → SUPPORTED in all four cells.

**Belief revision.** "Cross-sectional track ≈ complete" → "a binding confirmatory test and a phase prerequisite were missing." The correction did not come from re-examining the *world* (the data, the model) — those were fine — but from re-examining my *claim about the project's state*.

**What generalises — a distinct failure mode from Entries 16–19.** Those entries were *layer-confusion*: an apparent property of the world that was actually a property of our instrument (a check at the wrong layer, a metric silent about the layer that matters, a self-imposed threshold mistaken for a finding). This one is different: a **completeness claim made from memory and momentum rather than from the committed record.** The discipline I reliably apply to a *cited specific* — re-read it at source before asserting it — I failed to apply to a claim about *what is done*. The transferable rule: **"this phase is done" is a hypothesis to be checked against the obligation set, not an observation.** The obligations audit is to project-state what re-reading-the-source is to a number; both convert a confident assertion into a verified one, and both belong at reflex level — ideally as a phase *gate*, run before the "done" is spoken, not after a human prompts for it.

**Counterfactual that didn't happen.** Had we moved to H2.1 without the audit, we would have (a) carried an *incomplete* cross-sectional track — a missing binding confirmatory test, surfacing only at write-up or review — and (b) hit the absent template-dictionary prerequisite mid-launch. The forcing function was Shawn asking for the audit; the lesson is that I should have wanted it myself before declaring near-completion.

## Entry 21 — 2026-06-05 → 2026-06-06: a recovery-validated model component was empirically mis-specified, and a tool I "needed to write" already existed — both believed-state-vs-world errors, both corrected by going to source

**Context / continuity.** Entry 20 (2026-06-04→05) framed its lesson as *the believed-state, not the world, was the error* — a track asserted "nearly done" was missing a binding test. This session produced two more instances of the same shape, which now looks less like coincidence and more like the dominant failure mode of a long, momentum-carrying project.

**Surprising fact (1).** The template-dictionary scan — a prerequisite I expected to be a formality — showed the convention basis the project had been carrying (curated century/half-century/reign tiers, *recovery-validated at 98.6%*) was empirically wrong: multi-century slabs are ~31% of the convention pool and were entirely absent from the dictionary; reign templates, which had their own tier, are ~2.7%. A component everyone believed adequate, with a passing validation to point to, did not match the corpus.

**Probe.** Re-read the F1/F2_Other/F3/Tight family classifier, the Stage-1 empirical p_conv (9 width-based slab types), and the lodged prereg — at source, via fan-out explore agents instructed to quote and flag contradictions, not synthesise. This surfaced that (i) two convention bases coexisted; (ii) the lodged prereg put reigns *in* convention while the later family classifier held them *out* — an unreconciled contradiction; (iii) the 98.6% had validated the *old basis shapes*, so it does not transfer.

**Belief revision.** Two layers. Narrowly: the basis must be empirically re-derived and recovery re-validated before H2.1 (Decision 38). Deeply — the part worth keeping — *convention is not the absence of signal*. It is genuine-but-coarse evidence quantised onto the BC/AD calendar grid; the artefact is the rounding (per-item distortion + cross-item boundary pile-ups), and the discriminator is grid-snapping, an *observable* proxy for the dating-criterion LIRE discarded. The reframing dissolved a contradiction the project had carried since Decision 20.

**Surprising fact (2), same shape.** I dispatched a staging agent on the belief that a bespoke script was "the method," anchored on a project-local precedent — and only on Shawn's prompt discovered the canonical shared importer already existed and was more capable. The believed map ("I must write this") diverged from the territory ("it's already built"). Corrected the same way as (1): go to source (read the canonical tool), then externalise the finding so the next instance can't repeat it (a new project `CLAUDE.md`).

**Generalisation (candidate).** A passing validation certifies the thing it tested, not the thing you believe it tested (Entry 18's lesson), now recurring at the level of a whole model component — the 98.6% certified synthetic-basis recovery, not real-basis adequacy. And the corrective for a believed-state-vs-world error is almost always the same and almost always cheap: stop reasoning from the summary and read the source. The prerequisite scan worked precisely because it forced that read *before* the mis-specification could propagate into every H2.1 result — a gate earns its cost by failing early.

## Entry 22 — 2026-06-06 → 2026-06-07: the believed-state-vs-world error, authored by me and ratified by the PI, caught only when the data tripped it — the corrective needs to move upstream of the result

**Context / continuity.** Entries 20 and 21 named this project's dominant failure mode: *the believed-state, not the world, is the error*, corrected by going to source. Entry 21 logged two instances and called the corrective "almost always cheap." This session produced a third instance with a worse provenance and a clean counter-example, which together sharpen the generalisation.

**Surprising fact.** The recovery re-validation triage reported a gate failure. But the failing quantity — exact credible-interval coverage of the mixing weight α at large N — was one our *own lodged Amendment 01 §A5.5.1* had already established is unreliable (it collapses at large N under negligible bias) and had explicitly demoted from a gate to a diagnostic. I had written the re-validation spec's "α-coverage binding" gate three days *after* lodging the amendment that says α-coverage must not be a gate, and Shawn had signed it off.

**Probe.** Read the failing cell's actual α posterior at source: recovered 0.979 vs true 0.95 (bias +0.029, sd 0.012), shape r 0.838. Then re-read Amendment 01 §A5.5.1. The "failure" was the documented benign collapse; the model recovers α and shape; the basis is sound.

**Belief revision.** Narrowly: correct the spec — α-coverage is a diagnostic, shape and convergence are binding (the lodged criterion). Deeply: Entry 21's framing was too kind to this failure mode. It said the corrective ("read the source") is cheap *and* implied it is reliably applied. This instance shows it is reliably applied *too late* — after a result trips the flawed belief — because the belief had passed two checkpoints (my authoring, the PI's sign-off) without anyone reading the source it contradicted. The believed-state error is not just a thing that happens to summaries under context pressure; it survives *human review* when the reviewer also reasons from the believed state.

**The counter-example, same session.** The Alpes Graiae reconciliation is the corrective applied *upstream*: a possible error (a Latin province missing from the frame map) was checked at source for downstream impact (0 population-matched cities → no result change) *before* being escalated. Cost: one query. The difference between the gate and the omission is purely *when* the source-read happened — after the result vs before the alarm. That timing is the entire lever.

**Generalisation (revised).** The corrective for a believed-state-vs-world error is to read the source — but its *value* is set by where in the pipeline you read. Read it when a result trips your belief and you have merely caught a near-miss after building on the belief; read it when you write the belief (a spec, an acceptance gate, a flag) and you prevent the error entirely. Concretely for this project: every new acceptance criterion must be cross-checked against the lodged record *at spec-write time*, because a sign-off does not constitute that check — the PI and I share the believed state, so we fail the same way together. The cheap corrective is only cheap if it runs *before*, not after.

## Entry 23 — 2026-06-08 → 2026-06-09: a clean result that contradicted domain knowledge — a *sibling* of the believed-state error, caught not by reading the source but by confronting the world

**Context / continuity.** Entries 20–22 named this project's dominant failure mode — *the believed state, not the world, is the error* — corrected by *reading the source*, with its value set by *when* you read (Entry 22: at spec-write time, not when a result trips the belief). This session produced a failure with a different structure, and naming the difference is the point.

**Surprising fact.** The H2.1 production run was technically flawless (28/28 converged, 0 divergences, 0 failures) yet returned convention fractions that, for several provinces, contradicted what is known about them: Moesia inferior α = 0.05 despite ~60 % of its mass being round-period / grid-aligned; Dacia and Britannia α ≈ 0. The implausibility was not *internal* (no inconsistency with the lodged record) — it was *external*: the numbers did not match the corpus a domain expert knows. And it was the human, not any pipeline diagnostic, who asked the question.

**Probe.** Three escalating steps. (i) Descriptive family-composition per unit — confirmed the flagged units *are* heavily round-dated, so a low α is under-attribution, not genuine precision (Pompeii α ≈ 0 *is* genuine precision — a clean control that the same probe validated). (ii) A per-unit-basis refit — α swung 0.05 → 0.87 for Moesia and held for the controls, proving α is *basis-dependent* (under-identified) for these units, not merely imprecise. (iii) An informed-α prototype — a prior could *not* fix it, at any width or N. The lit-scout then supplied the why: a prior over a partially-identified region is never revised by the data (Gustafson 2010; Giacomini & Kitagawa 2021), and weak component separation makes the likelihood *confidently wrong* (Feller 2016).

**Belief revision.** Narrowly: the convention/genuine split is fundamentally under-identified for temporally-concentrated units, and the fix is auxiliary classification as a *likelihood* term, not a prior (established practice — concomitant-variable mixtures; the OxCal outlier model). Deeply — the new generalisation: the project has a *second* failure mode, sibling to the believed-state error. The believed-state error is an *internal* inconsistency (the spec contradicts the lodged record), caught by *reading the source*. This is an *external* implausibility (a clean result contradicts the world), caught only by *confronting the result with domain knowledge*. The second is more dangerous because every internal check passes — convergence, PPC, the run status all certified a result that was substantively wrong; no amount of source-reading would have caught it. The corrective is a *different reflex*: route every substantive result past domain plausibility before building on it, and where possible build that check into the pipeline (the identifiability flag and two-bound α now do).

**Note on the empirical–theory convergence.** The empirical probe (a prior cannot move the confounded α) and the formal literature (a prior over a non-identified region is unrevised by data) agreed exactly. When an independent empirical result and an independent theoretical result point to the same conclusion, the conclusion is about as well-supported as this project gets — and it is worth noticing the empirical route ran *first*, which is the cheaper insurance when you do not yet know the relevant theory exists. The prototype-before-build discipline both killed a wrong fix and earned the confidence to pursue the right one.

## Entry 24 — 2026-06-09: the remediation worked, but not the way it was designed — the recovery test invalidated the design that motivated it

**Context / continuity.** Entry 23 ended on an explicit open question: would the joint model *recover* the confounded units or only *bound* them, once recovery-validated on *realistic* (broad-slab, not narrow-Gaussian) synthetic convention? The plan carried into this session — written into the continuity doc and broadly endorsed — was specific: classification as a second likelihood term, with the **shared** convention basis (Decision 38 / Amendment 03), leading; the per-unit basis having been rejected for over-attribution.

**Surprising fact.** On realistic synthetic cells, the planned design **failed**: shared basis + classification returned α ≈ 0 on every confounded cell (bias −0.20 to −0.60) — no better than the shared-basis baseline it was meant to beat. The classification term, the thing the whole remediation rested on, *did not bite*. Meanwhile the **rejected** per-unit basis + the same classification term recovered α cleanly (|bias| ≤ 0.07 on the true shape, ≤ 0.12 on the realistic estimated shape). The design we were confident in was wrong, and the design we had ruled out was right.

**Probe.** Three nested recovery experiments (POC-REPORT Exp 1/2/3) isolated it: (1) shared basis + classification — fails; (2) per-unit basis + classification, true shape — recovers; (3) per-unit basis + classification, contaminated/estimated shape — recovers with a small residual bias. The mechanism: with the shared basis too broad, α > 0 forces convention mass outside the unit's data window, so the 80-bin temporal multinomial is not flat in α but *confidently wrong* (Feller weak-separation), and it overpowers the single classification binomial. Free the convention *shape* (per-unit basis) and the temporal likelihood becomes genuinely flat/partial-ID — and *then* the classification covariate identifies α (Huang & Bandeen-Roche). A second, smaller probe — the κ-sweep — disconfirmed the jointly-agreed plan to widen the θ prior: widening *amplified* the residual bias rather than curing the coverage, because the residual is contamination bias, not interval under-dispersion.

**Belief revision.** Narrowly: the lever is the convention **shape and the classification count jointly**, not the count alone with a fixed shape; the per-unit basis is safe *because* the classification term supplies the over-attribution control the shared basis was adopted to provide; κ stays at 40. Deeply — a generalisation about the role of a recovery validation itself: I had implicitly treated the POC as a *confirmation* step ("validate the planned model before scaling"). It functioned instead as a *falsification* step — its real value was overturning the design, not blessing it. A recovery validation earns its cost precisely when it can, and does, invalidate the design that motivated it; if it can only ratify, it is theatre. This pairs with Entries 18/22 (a validation certifies what it tests, not what you believe it tests) but inverts the polarity — there the validation falsely *passed* the believed model; here it correctly *failed* it. The shared lesson across all of them: the apparatus must be allowed to contradict the plan, and the plan's confidence (continuity doc, PI sign-off, a day-old emphatic handoff) is not evidence.

**Note on where the surprise did *not* propagate.** The cost of being wrong was one POC (≈ six fits), not a 39,000-fit grid built on the wrong model — because the POC ran before the grid, exactly as the prototype-before-build discipline intends. The same discipline that killed the informed-α prior in Entry 23 killed the shared-basis design here. Its value is not that the first design is usually right (it was not, twice running) but that the falsification is cheap when it comes first.

## Entry 25 — 2026-06-10/11: two predictions falsified by cheap experiments — a misattributed symptom and a "bit-identical" claim that was never achievable

**Context / continuity.** This session opened to assess Entry 24's grid verdict but found the run dead; it became an infrastructure marathon. Two of its turns are textbook surprise→probe→revision, and both resolved by a *targeted experiment* rather than reasoning — which is the pattern worth logging.

**Surprising fact #1 — a symptom that didn't fit its assumed cause.** The grid had clearly OOM'd, so when sapphire's SSH failed intermittently (`255`, "no banner"), the natural attribution was "the box is still thrashing from the OOM." But the OOM was over (the grid was dead, 57 GB free), yet SSH kept failing. *Probe:* ping (alive) → multi-port TCP sweep (both sshd and open-webui accept connections but can't answer → userspace-wide, not service-specific) → verbose SSH (`mkdtemp() failed: No space left on device`) → `df -h` (14 % blocks — *not* full) → `df -i` (**100 % inodes**). *Belief revision:* there were **two independent resource exhaustions**, not one — RAM (the OOM) and `/tmp` tmpfs inodes (~1.05 M leaked `tempfile` files from days-old work). The general point: "no banner + free disk" has a specific cause (inode exhaustion) distinct from the louder one (thrash), and a single big failure is a good place for a second, quieter failure to hide. The instinct to attribute a residual symptom to the dominant cause is exactly the trap; the `df -i` check is one keystroke and settles it.

**Surprising fact #2 — a validation I expected to pass, didn't, and the failure was informative.** I refactored the leaky model to `pm.set_data` and asserted the validation gate would be *bit-identical* (same priors, same seeds, data entering differently). It wasn't — old-vs-new α differed ~2×10⁻³. The satisficing response ("tiny, fine") was available and tempting. *Probe:* instead of judging the magnitude, I ran the *new* code twice with identical seeds → **max |Δ| = 0.000**. *Belief revision:* the new code is bit-*reproducible*; therefore the 2×10⁻³ old-vs-new gap is **method-specific**, not a noise floor — the shared-variable graph genuinely differs from the constant-baked graph, so the same seed walks a different but equally valid NUTS trajectory through the *same* posterior. "Bit-identical to the old code" was never an achievable bar (the graphs differ by construction), and recognising that reframed the decision from "is 2×10⁻³ acceptable?" (a judgement) to "keep mixed-method or restart for one consistent method?" (a clean choice, surfaced to the PI with the numbers; he chose restart). The reusable inference move: when a reproducibility claim fails by a small amount, the diagnostic is *new-vs-new*, which partitions the gap into "the method changed something" vs "the computation is just noisy" — two different decisions hang on which it is.

**Where this connects to the running thread.** The session's terminal result extends the Entry 18/19/22/24 lineage one more turn. The 300-cell grid ran *flawlessly* — 0 failures, bit-reproducible — and its honest output is that the model **fails C1 (do-no-harm) on coverage** (0.374), because it carries the +0.07 estimated-basis contamination the spec predicted. Across the lineage: a validation can pass the believed-but-wrong model (18/22); a clean run can hide a wrong answer (19); a recovery test can falsify the design that motivated it (24); and here, a clean run *correctly reports* its own model's characterised flaw. The constant is that "it ran cleanly" is information about the apparatus, never about the truth of the answer — and the apparatus must be built so the answer can still come back "not good enough." It did.

## Entry 26 — 2026-06-14: a robustness check that failed as a vehicle but succeeded as a diagnostic — the calibrated θ was circularly biased

**Context / continuity.** The cross-classified `library` model had passed its recovery grid and refit the 29 production units; the remaining step before lodging the amendment was the preregistered robustness check — a global-θ hybrid that estimates the alignment rates θ jointly (with a wide prior) rather than plugging in the calibrated values, then asks whether the per-unit α's survive.

**Surprising fact.** Two things at once. (1) The hybrid was *weakly identified* on the real data — convergence got *worse* with more compute (tune doubled, target-accept raised), invariant to prior width, zero divergences: the signature of a ridge, not a sampling deficit. So it failed as a robustness *vehicle*. (2) Yet it robustly preferred θ_gen ≈ 0.024, a long way from the calibrated 0.155 — and the per-unit α's it implied were *concordant* with the production fit on the frontier units. A model too poorly identified to trust for its intervals was nonetheless telling me, stably, that one of the production fit's fixed inputs was wrong.

**Probe.** Two cheap, independent checks. (i) Re-derive the θ calibration's regression using the *corrected* cc-library α's in place of the under-attributing shared-basis α's it had originally used → θ_gen 0.025, and a 2.5× better fit to the aligned-fraction data (RMSE 0.045 vs 0.117). (ii) A θ-prior sensitivity sweep over the 29 units at four priors → the per-unit α's are stable for 27/29; only the two most temporally-confounded units move, and within bounds. Three independent routes — hybrid joint fit, re-derivation, sweep — agreed on θ_gen ≈ 0.02–0.025.

**Belief revision.** Narrowly: the production θ prior was mis-centred and should be re-derived (Shawn adopted it; the refit re-ran, the frontier α's rose slightly, more in line with the classification-implied values). Deeply — a generalisation about empirical-Bayes plug-in calibration: *a parameter calibrated from a first-pass estimate that the model will later correct is circularly biased, and the bias propagates silently into production.* `calibrate_theta` had fit θ_gen against the very α's the cross-classified model exists to fix; the under-attribution in those α's inflated θ_gen, which then subtly shaped the corrected fit. Nothing internal flagged it — the calibration converged, the fit converged. It took a *robustness check designed to vary that exact assumption* to expose it, and the check exposed it even though the check's own model was too weak to lodge. The reusable inference: a robustness check earns its cost when it can contradict the thing it varies — and a check can be *too poorly identified to trust for its primary output yet still diagnostic for its secondary one*. Failing as a vehicle and succeeding as a diagnostic are not mutually exclusive; the discipline is to read what it surfaced before discarding it for failing.

**Where this sits in the lineage.** Entries 24/25 logged the apparatus correctly *failing* a believed model (the shared-basis design; the bit-identical claim). This is the same polarity once more — a check returning "the assumption you plugged in is wrong" — but the twist is that the check itself was broken, and the signal survived its brokenness. The constant across the lineage holds: the apparatus must be allowed to contradict the plan, and this time it did so from inside a model I had already decided not to trust.

## Entry 27 — 2026-06-14 → 2026-06-15: a self-test-verified pipeline returned a degenerate result — the surprise that wasn't a bug, told apart from one by the test built to tell them apart

**Context / continuity.** Implementing the H3b deviation test along the line Entry 22 had set up: emit the genuine-SPA posterior from the cc-library refit and propagate it draw-wise through the featureless-null envelope. Stage A verified (provenance gate: re-run reproduces the lodged fits to MCMC noise); the Stage-B engine carried a self-test asserting its inlined envelope matched the reused library test *bit-for-bit*; the headline statistic (marginal-p) had been deliberately chosen with Shawn over the alternative.

**Surprising fact.** The global test returned p = 0 for **all 29 units under both nulls** — total saturation, the carefully-chosen marginal-p uniformly uninformative. And a second surprise nested inside the first: my OQ-5-confirmed construction (fit the CPL null to the *raw* corpus) saturated the *probe windows* too, where I had expected differentiation. A pipeline I had verified at every internal joint produced a result that, taken at face value, says nothing.

**Probe.** Four cheap, convergent checks. (i) *Is it the code?* The self-test had already passed — engine == library to machine precision — so the saturation is not an implementation artefact. (ii) *Has this been seen?* The abandoned 2026-06-09 median-based draft (`h3b_lib.py` + its `REPORT.md`, which I'd only just discovered) reached the *identical* p = 0 conclusion independently. (iii) *What's the structure?* empire shows 77/80 bins out-of-envelope; the pointwise envelope width scales as ~1/√N, so at n_eff of 10³–10⁵ any smooth-null misfit exceeds it. (iv) *Why do the probes saturate under my CPL but not the draft's?* The draft fits CPL to the *observed corrected* curve (the null tracks the curve's own trend → only local departures show); I fit it to the *raw* corpus (so the entire convention-removal reshaping reads as deviation). Switching to fit-to-observed de-saturated the probe windows into a differentiated P(deficit).

**Belief revision.** Narrowly: the basic Timpson/SPD global envelope test is *over-powered to degeneracy* on these corpora — the informative readout is the probe-window deficit posteriors, not the global p; and the CPL featureless null must be fit to the observed corrected curve, not the raw. Deeply, two generalisations. First — *"the pipeline is correct" and "the result is meaningful" are independent claims, and a bit-for-bit self-test is precisely the instrument that lets you separate them*: without it I'd have spent the night hunting a bug that wasn't there; with it, "the result looks broken" resolved in one read to "the method is degenerate here," a finding rather than a defect. Second — *a preregistered test validated against a matching-baseline simulation can be degenerate on real data where the null is misspecified*: Phase-1 calibrated detection at N≈1,600 by injecting a single event onto the *generating* smooth shape; on real data the null can't reproduce the true smooth shape at all, so baseline misfit + large N saturates the test in a regime the calibration never probed. The reachability table measured the wrong thing for the real-data case, and nothing internal flagged the gap.

**Where this sits in the lineage.** Entries 24–26 had the apparatus contradict a *model* (the shared basis) or a *parameter* (the calibrated θ). Entry 27 is the apparatus contradicting the *test itself* — the instrument, not what it measures — and the new move is that the disambiguator (the self-test) was built *before* it was needed, so the contradiction arrived pre-sorted into "method, not code." The recurring constant deepens: not only must the apparatus be allowed to contradict the plan, the apparatus that lets a degenerate *result* be read as a finding rather than mistaken for a *failure* is one you have to construct in advance, while you still believe the result will be clean.

## Entry 28 — 2026-06-15 → 2026-06-16: the deconvolution that doesn't change the scaling but does change the peak — and a "material" headline that dissolved under one robustness check

**Context / continuity.** Same cc-library deconvolution posterior as Entry 27 (the H3b saturation), turned on a different question Shawn posed: does the deconvolution we built actually *help* the Hanson population–inscription analyses, which currently use raw counts? The prior — his and mine — was that a model which visibly reshapes the temporal curve ought to change a downstream analysis that consumes it.

**Surprising fact (two).** First: it doesn't move the *cumulative* scaling at all. H3a's date window is the full envelope, so the reshaping conserves each unit's count (mass conservation), and the only remaining channel — the genuine fraction α — is flat across population (Spearman −0.11). Second, against a specific prior: when Shawn asked the sharp follow-up — does it change a *peak* statistic? — I expected the deconvolution's GRW smoothness prior to *attenuate* the peak (lower it). Instead the genuine peak is **+60% higher** and ~20 years later than the raw aoristic peak. The reshaping is large and real; it just doesn't touch the scaling.

**Probe.** Cheap, diagnostic-first, every time. (i) *Does α correlate with population?* Compute it on the 29 units — no; and the naïve OLS slope that said "yes, +0.29" was one high-leverage unit (Pompeii, α≈0.016) in log space — Theil-Sen and leave-one-out collapse it to ≈0. (ii) *Does the peak move, and does the move scale with size?* Propagate the genuine-SPA draws → peak rises +60% in 25/26 units, but log(peak ratio) vs population is flat (Spearman −0.00). (iii) *Why up, not down?* The raw aoristic peak is *suppressed* by convention-smearing (wide round-number intervals spread mass thinly); removing it concentrates the genuine signal, and that suppression-removal dominates the GRW attenuation I'd worried about.

**Belief revision.** Narrowly: the Hanson scaling — cumulative *and* peak-window — is robust to the deconvolution ("the population–epigraphy scaling holds whether or not we correct for editorial-convention dating"). Deeply: *a reshaping changes a downstream statistic only if two independent conditions both hold — the statistic is shape-sensitive (not mass-conserved over the analysis window), AND the reshaping's magnitude correlates with the predictor.* The peak satisfies the first and fails the second, which is exactly why the deconvolution changes the *description* of production (peak height and timing) but not the *scaling law*. The prior "a model that reshapes the curve must change analyses that use it" was missing both qualifiers; and the GRW-attenuation expectation had the wrong sign because I'd modelled one of two competing effects without asking which dominates.

**Where this sits in the lineage.** Entry 27 was the apparatus contradicting the *test*; Entry 28 is the apparatus contradicting a *prediction about what a tool we built would do* — and the corrective was the same diagnostic-first reflex three times in one session (α-vs-pop, peak-vs-size, and a fourth flavour: reading `h1_sim_v2.py` and finding B4's bootstrap had been removed by Decision 8, making the obligation moot before any run). The session's constant: when you think a lever will move the answer, measure whether it does before building the thing that assumes it does. Each time, the lever moved less than expected — and once (the peak) it moved a lot, but on an axis that didn't matter for the law.

## Entry 29 — 2026-06-16 → 2026-06-17: the quantity I'd named "the epigraphic habit" is not the habit — a label revised by the human's question, not a diagnostic

**Context / continuity.** §5 H5, the "habit-removed residual trajectory". The §5 Layer-A hierarchical model factors each city's log-rate into a global shape `g_shape`, province `u_shape`, and city `v_shape`. I had specced and reported H5 by *naming* `g_shape` "the empire-wide epigraphic habit" (the prereg's own term) and the residual `u+v` as "habit-removed" — and the run had produced a clean result (g peaks AD 188, matching MacMullen and the H3b hump; foundation-terminus check passes). The result felt finished.

**Surprising fact.** Not an apparatus contradiction this time — a *question*. Shawn asked: "how are we extracting *habit* from the data, as distinct from population or other contributing factors?" The surprise was realising I could not cleanly answer it. The model has *no population covariate*; `g_shape` is simply the time-shape all cities share, identified by pooling. So calling it "habit" was an interpretive label I'd attached to a statistical common-component, and the decomposition does not separate habit from population at all — it separates *empire-common* from *city-specific*.

**Probe.** Conceptual, then quantitative. (i) *What does the model actually identify?* The common component is whatever moves empire-wide in synchrony; that necessarily conflates the cultural habit, empire-wide demography/economy, taphonomy, and residual dating-convention — four drivers, not one. (ii) *Is there an external habit proxy to disentangle them?* No — the 2026-04-23 prior-art scout established none exists. (iii) *How big is the common component vs the "population" axis?* I'd reported magnitudes from transient output; persisting the computation (`h5_decomposition.py`) anchored them: common temporal swing SD 1.11, ≈54 % of a city's temporal variance, larger than the between-city level spread 0.78 — but the level/population axis is a *different plane* (cross-sectional, not temporal) and is range-restricted in the §5 set, so "bigger than" is not "more important than". (iv) *Does the diagnostic unit change it?* Restricting to Latin-minus-Roma (257/268) leaves the decomposition ~identical — the concern that I'd used the wrong frame was, for §5, nearly moot.

**Belief revision.** Narrowly: rename throughout — `g_shape` is the **empire-wide common temporal component**, not "the habit"; the residual is the defensible per-city quantity; the four candidate causes are externalised into the discussion, where the correspondence with the epigraphic-habit literature is *noted, not asserted*. This drove a paper-framing decision (empirical decomposition first; interpretation, incl. habit and population, later; Hanson as the explicit first interpretive step). Deeply: *a label is a hypothesis about identification, and it should be tested against "what does this quantity actually separate from what?" before it ships* — I had let the prereg's domain term ("habit") stand as if it were an identified construct, when the estimator only delivers a common-vs-idiosyncratic split. The honest move is to name the quantity by *what the model does* (a shared time-shape) and reserve the causal name for the discussion.

**Where this sits in the lineage.** Entries 27–28 had the *apparatus* contradict a test or a prediction; Entry 29 is the *human's question* contradicting my *label* — the reframe came from a domain question, not a diagnostic, and the corrective was conceptual (what does the quantity mean) rather than computational (does the lever move). It also closes a loop with the session's other thread: the obs-writer's refusal to record the magnitude numbers until they were persisted (write-side anti-confab) is the same discipline applied to a *number* that this entry applies to a *name* — don't ship a specific (a value, or a causal label) you cannot anchor in, respectively, a file or an identification argument.

## Entry 30 — 2026-06-17 → 2026-06-18: a follow-up built to confirm a claim disconfirmed its mechanism — and a summary statistic that mimicked the very phenomenon it measured

**Context / continuity.** The habit-removed residual Layer B (Entry 29's reframe, now executed) and its descendants. Two beliefs were in play. (a) The residual inversion — invert the city residual `u+v` after removing the empire-common `g` — would *dissolve* the raw Layer B's apparent universal post-AD-250 collapse, because the empire-wide decline lives in `g`. (b) Having found (Obs 104) that the size–buffering gradient was stronger in `q_uv` (city-from-empire) than `q_v` (city-from-province), I inferred and reported, with some enthusiasm, that the buffering is "province-mediated".

**Surprising fact (two).** First: the residual Layer B's pre-specified contrast — `q` at AD 250 as a fraction of the city's own peak — came back ≈ 0, *reproducing* the collapse it was meant to dissolve. The instrument said the opposite of the mechanism I understood. Second: a direct test built to *confirm* (b) — regress province `q_u` features on province size — did not corroborate it. Province *size* does not predict province buffering; the primary aggregate (total provincial mass) is null and sign-incoherent on exactly the features that carried the Obs 104 gradient.

**Probe.** First fact: don't trust the number, plot the object. `q` vs the empire baseline (1.0) — not vs its own peak — was 0.32 at AD 262, not 0. The peak-normalisation was confounded: `1/β>1` amplification plus the GRW's high-variance endpoints push a third of cities' "peak" to the envelope edges, so the ratio is ~0 regardless of the late level. The collapse *does* dissolve; the metric was the wrong yardstick for an amplified zero-sum trajectory. Second fact: read the *split*. The buffered hint attaches to mean/max province size (per-city scale) and not to sum (total mass), and — the load-bearing distinction — a *decomposition fact* (the gradient's variance lives in the `u` tier) is not a *mechanism* (province size driving the trajectory). The regression separates them; only the weaker reading survives, and even that is underpowered (n≈20–35, nothing clears the bound).

**Belief revision.** Narrowly: (a) the demography-isolating result holds, measured correctly — the median city sits at ~0.32 of its empire-relative baseline by the 3rd c., a moderate heterogeneous decline, not annihilation; report `q`-vs-baseline, demote frac-of-peak to a flagged footnote. (b) "Province-mediated" is downgraded to a *decomposition* statement and explicitly *not* a province-size effect (Obs 105 refines Obs 104). Deeply, two: first — *a pre-specified summary statistic can mimic the phenomenon it is meant to detect; when the statistic fights a mechanism you understand, suspect the statistic and inspect the raw object* (the same instrument-not-phenomenon move as Entry 27's degenerate test, but here the instrument was a metric I chose, not a test I inherited). Second — *the discipline that matters is building the test that can disconfirm your own just-made claim, and pre-framing its null as informative so the disconfirmation lands as a refinement, not a defeat.* I could have rested on the `q_uv ≫ q_v` inference; choosing to test it directly is what kept Obs 104 from over-claiming a mechanism the data don't support.

**Where this sits in the lineage.** Entry 27 (apparatus contradicts the *test*), 28 (contradicts a *prediction about a tool*), 29 (the human's *question* contradicts a *label*). Entry 30 is the apparatus — a follow-up *I chose to build* — contradicting my *own just-made interpretation*, and a metric contradicting the mechanism it measured. The new move is agency over the disconfirmer: Entries 27–29 had the contradiction arrive (from a self-test built earlier, a sharp question, a reframe); here I manufactured the instrument that could prove me wrong and pre-committed to reading its null as a result. The session's constant across all four: the apparatus must be allowed — and here, *built* — to contradict the analyst, and the highest-value outputs (Obs 105's refinement; the corrected residual diagnostic) came from letting it.

## Entry 31 — 2026-06-18 → 2026-06-19: a pre-registered verdict that refuted my hypothesis, a follow-up that refuted my next one, and an empirical artefact the literature had already named

**Context / continuity.** The H2.1 supplementary pilot found that the preregistered aoristic-MC (C10), re-mapped onto the Amendment-04 cross-classified model, collapses the convention share α from the deconvolution's ~0.68 to ~0.10 on the real empire data, while mass-apportionment holds. I framed the choice as reading (b) — "point-date sampling destroys the slab-concentration the cross-classified α detects" — and led Shawn toward it with some confidence; the pre-registered validity battery (1a diagnostic, 1b ground-truth recovery, 1c contrast) would adjudicate.

**Surprising fact (two, in sequence).** First: the pre-registered 1b returned **(a)** — on synthetic ground-truth, the point-date arm *recovers* a planted α just as well as the mass arm (slope ~1.05). My (b) was refuted by the very test built to check it. Yet 1c showed the real-empire collapse is genuine (point-collapse 0.10 vs mass-preserving 0.62). The instrument said "point-date is fine" on synthetic and "point-date collapses" on real — a 1b/1c contradiction the clean (a) verdict papered over. Second: I then bet the difference was the interval-*width* distribution (the synthetic used idealised widths). The realism-graded follow-up (ii) showed it is **θ-contamination** (R2: realistic imperfect alignment separation, θ_conv 0.93/θ_gen 0.025) — *not* width (R1 didn't cleanly reproduce it; it biased the mass arm too). Wrong at both forks.

**Probe.** For the first: don't bank the binary, name the tension — why does the same method recover on synthetic but collapse on real? Hypothesis: the synthetic was too idealised (perfect θ separation), so build a test that grades realism on the *recorded-interval* dimensions (point-date samples the recorded interval, never the latent true date — so the latent-shape variant R3 must be a null, and it was). For the second: instrument all the dimensions (width R1, θ R2, latent R3, joint R1+R2) rather than only width, and read which one makes point-date diverge from mass while mass still recovers the planted α. Only R2 (and R1+R2) did, cleanly; R1 broke both arms; R0/R3 stayed clean.

**Belief revision.** The empire point-date collapse is **real but a method artefact, not a property of the data**: under realistic alignment misclassification, point-date sampling (a hard plug-in of a misclassified latent assignment) collapses the mixture share, while mass-apportionment (integrate-out) recovers the truth. So the **deconvolution α ≈ 0.68 stands**; the point-date 0.10 is the artefact, and reading (b)'s spirit is rescued with a precise mechanism (θ-contamination), having been refuted in its literal form. Then the held lit-scout supplied the name: this is the **"three-step / classify-analyze plug-in bias"** (Bolck-Croon-Hagenaars 2004, 1083 cites; Bakk 2013 ties it specifically to classification error) — point-date = the hard plug-in, θ = the classification error, mass = the integrate-out correction — joined to the aoristic "pointwise-vs-mass" critique (Carleton & Groucutt 2021; Roberts 2012). We had rediscovered a textbook result from the data; the conjunction (this bias in a cross-classified aoristic deconvolution) is novel.

**Where this sits in the lineage.** Entries 27–30 were each the apparatus contradicting the analyst — a self-test, a prediction, the human's question, a self-built follow-up. Entry 31 is the apparatus contradicting me *twice in one arc* (the pre-registered verdict refuted my hypothesis; the realism test refuted my next one) with a third agency on top: the *literature* naming the mechanism I'd reconstructed empirically. The new move is the convergence of three independent confirmations — an empirical collapse, a planted-α recovery isolating its cause, and a 1083-cite keystone — on one answer I'd twice guessed wrong. The session's constant: build the disconfirmer and let it win; and when a clean pre-registered verdict sits oddly beside a real observation, the tension *is* the finding.
