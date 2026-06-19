# Results-documentation consistency audit — inscriptions / LIRE deconvolution paper

- **Date:** 2026-06-20
- **Auditor:** Claude (Opus 4.8, 1M context), read-only audit on Shawn's brief.
- **Scope:** all 58 run directories under `runs/` (enumerated with `ls runs/`),
  plus a check of `planning/` for de-facto write-ups.
- **Mode:** READ-ONLY. No analysis, code, data, or compute was modified, run, or
  committed. The only file created is this report.
- **Status of this document:** working note, not committed; for the team's pre-write-up
  uplift planning.

This audit derives the documentation rubric from the project's **own** best practice
(it does not impose an external standard), nominates the single best-documented run as
the exemplar, records each other run's delta against it, and produces a prioritised
"results documentation uplift" task-list.

---

## (a) The rubric — derived from the project's own best practice

Surveying the run directories, the project's mature runs (mid-June 2026 cohort)
converge on a consistent eight-component documentation pattern. A fully-documented
run has:

1. **`spec.md`** (variously `spec.md` / `*-spec.md` / `SPEC.md` / `launch-spec.md` /
   `plan.md` / `design.json`) — a *pre-launch* spec carrying: a **Status line**, an
   explicit **sign-off** (`EXECUTED` / "signed off" / "proceed-to-run granted" /
   "audit-before-run"), an **inputs-verified** table (source path + what was checked),
   the **method**, the **deliverables**, a **self-check / guards** section, **caveats**
   to carry into the write-up, **compute** notes (host, API spend), and **verdict-logic**
   (what each outcome would mean, pre-committed).
2. **`REPORT.md`** (or `*-VERDICT.md` / `RESULTS.md` / `FINDINGS.md` /
   `VALIDITY-REPORT.md`) — a results write-up carrying: a **Status banner** (e.g.
   "COMPLETE"), a **Verdict**, **results stated as generated-from-data** (numbers
   re-derivable from the persisted outputs), **caveats**, an **Outputs list**, and
   **Obs-register cross-references** ("Obs N").
3. **`code/`** with **header docstrings / blocks** (purpose, args, cross-refs to
   sibling diagnostics and Obs) — per the project's `CLAUDE.md` conventions.
4. **`outputs/`** with **provenance** — seeds and, for deterministic-read runs,
   **input `sha256`**. (MCMC runs in this project record seed but not input sha256;
   that is the project's own observed convention and is not penalised below.)
5. A **"Reproduce" / run-command** — the exact command. The exemplar carries this in
   the Status/Run line rather than a literal `## Reproduce` heading, so a co-located
   command in the spec or the code docstring counts.
6. A **`run.log`** capturing the actual run (sampler trace, convergence, timings).
7. A **link to the Obs register** — the run's result is recorded as an `Obs N` entry in
   `docs/notes/working-notes.md` (107 numbered observations as of this audit, each
   citing the source run dir + persisted artefacts).
8. **Supersede / stale banners** where a result was later overturned or rebuilt
   (the project uses `⚠ SUPERSEDED` / `RESOLVED` / "superseded by Decision N").

**Two project-specific conventions confirmed against the exemplar itself**, so they are
*not* treated as defects across the board: (i) there is no literal `## Reproduce`
heading — the command lives in the Status line; (ii) input `sha256` is present only in
deterministic-read runs, not MCMC runs (which record seed only).

---

## (b) The exemplar — `runs/2026-06-18-province-size-regression/`

This run hits **all eight** components and is the cleanest instance of the project's own
template:

- **spec.md** (215 lines) — `Status: EXECUTED 2026-06-18`, an explicit sign-off
  ("design signed off in the brief — proceed-to-run granted"), an **inputs re-verified
  this session** table (each input with source path + what was checked + a verified
  province-join count), method, deliverables, a numbered **self-check** (two guards with
  exact tolerances), seven load-bearing **caveats**, a **compute** section (sapphire, no
  API spend), and a **§9 verdict logic** pre-committing what each outcome means.
- **REPORT.md** (106 lines) — `Status: COMPLETE`, a stated **Verdict** ("NOT directly
  corroborated; underpowered"), a **PASS self-check** quoted from the run ("max abs diff
  0.0 — bit-exact"), every number **generated-from-data**, six caveats, an **Outputs**
  list, and **Obs cross-refs** (Obs 104, 103, 100, 98).
- **code/province_size_regression.py** — a full header docstring (purpose, unit
  definition, features, statistic, β-frame-invariance argument, Obs cross-refs).
- **outputs/** — `province-size-regression-summary.json` carries seed **and input
  `sha256`** (verified present).
- **run.log** — captures the join, both self-check guards, samples, and per-feature ρ
  with bootstrap CIs.
- **Obs link** — the result is lodged as **Obs 105** (`docs/notes/working-notes.md:5204`),
  "all numbers verified", with re-verifiable artefact paths.

The sibling `runs/2026-06-18-s5-size-vs-dynamics/` (its parent; spec `Status: EXECUTED`,
seed + sha256, Obs 104) and the whole `runs/2026-06-17-s5-*` family are near-identical in
quality. The province-size-regression run is nominated because it is the single most
self-contained, end-to-end instance (spec sign-off flipped to EXECUTED, self-check PASS
quoted in the report, sha256 present, matching Obs).

---

## (c) Per-run audit table — delta vs the exemplar

Component key: ✓ present · ◐ partial · ✗ missing. Components: 1 spec · 2 REPORT ·
3 code-headers · 4 provenance(seed/sha256) · 5 reproduce-cmd · 6 run.log · 7 Obs-link ·
8 supersede-banner. "Obs" column = mentions of the dir name in `working-notes.md`.

| Run dir | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Obs | Genuine? | Sev | Key delta / note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-04-23-descriptive-stats | ✓ | ◐ | ✓ | ◐ | ◐ | ✓ | ✓ | – | 1 | yes | **LOW** — results split summary.md+verdict.md (no single REPORT); `outputs/summary.md` says 65 cols vs run.log/decisions 63 (internal contradiction); no sha256 |
| 2026-04-23-prior-art-scouts | – | – | – | – | – | – | ◐ | – | 1 | **transient** | **N/A** — lit-scout notes; "verification pending" never resolved (content caveat, not doc defect) |
| 2026-04-24-zotero-batch-add | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | – | 0 | **transient** | **N/A** — Zotero ingestion logs only |
| 2026-04-25-h1-simulation | ✓ | ◐ | ✓ | ◐ | ✗ | ◐ | ✓ | ◐ | 14 | yes (foundational) | **MEDIUM** — top-level `outputs/REPORT.md` is the **v1** (FP=1.000) result with **no supersede banner** though Obs 19 records it superseded by `h1-v2/REPORT-v2-final.md`; v2-final lacks Status/Verdict/sha256/Obs back-ref |
| 2026-04-25-h3a-brms-shadow | ◐ | ✗ | – | ✗ | – | ✗ | ✗ | 0 | deferred build | **LOW** — README correctly self-flags "built, not yet executed" (input not yet produced); outputs/ only `.gitkeep`. Re-confirm whether now runnable or abandoned |
| 2026-05-03-baorista-install | – | ◐ | ✓ | – | – | ✓ | ✓ | – | 5 | **transient** | **N/A** — install + smoke log; well-documented as an install |
| 2026-05-15-editorial-convention-hierarchy | ◐ | ✓ | ✓ | ◐ | ◐ | ✓ | ✓ | – | 1 | yes | **MEDIUM** — strong report + Obs 35 link; spec lacks sign-off/self-check/verdict-logic; no sha256; cmd only in docstring |
| 2026-05-16-rome-count-verification | ✗ | ◐ | ✓ | ✗ | ◐ | ✗ | ✗ | 0 | semi-utility | **LOW** — verifies prereg counts; `verification.md` flat list, no status/verdict banner; cmd in docstring; 0 Obs (verifies prereg, not a finding) |
| 2026-05-17-date-range-filtered-spas | ✗ | ✓ | ✓ | ◐ | ✗ | ✗ | ✓ | – | 2 | yes | **MEDIUM** — REPORT has Verdict; no spec/sha256/run.log/reproduce; Obs 35–37 cite it (register→run only) |
| 2026-05-17-empirical-spa-shape | ✗ | ✓ | ✓ | ◐ | ✗ | ✗ | ✓ | – | 2 | yes | **MEDIUM** — as above; "Modelling implication" conclusion in lieu of Status banner; no run.log |
| 2026-05-17-interval-width-diagnostic | ✗ | ✓ | ✓ | ◐ | ✗ | ✗ | ✓ | – | 2 | yes | **MEDIUM** — as above; no spec/run.log/sha256 |
| 2026-05-21-talk-prep | ◐ | ◐ | ✓ | ◐ | ✗ | ✗ | ✓ | – | 3 | mostly prep | **LOW–MED** — spec status "in flight (Block 1 in progress)" **contradicts** plan.md (Blocks 1–6 done); promised `outputs/REPORT.md` never produced; key numbers Obs-captured elsewhere |
| 2026-05-22-data-profile-smoke | ✗ | ✗ | – | ◐ | – | ✓ | ✗ | – | 0 | **transient** | **N/A** — explicit tooling smoke test (`comprehensive_mode:false`) |
| 2026-05-22-reachability-guide | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | 0 | **transient** | **N/A** — re-renders existing h1-simulation outputs for slides; no new result |
| 2026-05-22-recovery-grid-design | ✓ | ✗ | – | – | – | – | ◐ | ✗ | 1 | design artefact | **LOW–MED** — binding design pin (legit no REPORT); but its validation **FAILed** then was reworked (empirical-Bayes) and the design carries **no forward outcome banner** |
| 2026-05-22-recovery-grid-validation | ◐* | ✓ | ✓ | ◐ | ◐ | ✓ | ◐ | ✗ | 2 | yes (load-bearing) | **HIGH** — `outputs/REPORT.md:8` **"Validation verdict: FAIL"** (line 12: 63.6% / 286 cells) with **no supersede banner**; that verdict was **overturned** (Obs 67: PASS 91.9%→98.6% under corrected criterion). Cold reader takes a now-wrong conclusion. *spec lives in sibling design dir |
| 2026-05-24-date-range-threshold-analysis | ✗ | ◐ | ✓ | ◐ | ✗ | ✗ | ◐ | – | 2 | yes | **MEDIUM** — REPORT has tables but no Status/Verdict/Obs back-ref; no spec/reproduce/run.log |
| 2026-05-24-empirical-pconv | ✗ | ◐ | ✓ | ◐ | ✗ | ✗ | ◐ | – | 6 | yes | **MEDIUM** — anchor for multi-century percentages; no Status/Verdict; working-notes:2136 separately flags Decision 38's "~31%" narrative figure does not reproduce here (24.96%/35.93%) — downstream-narrative issue to reconcile |
| 2026-05-24-empirical-pgen-prior | ✗ | ◐ | ✓ | ◐ | ✗ | ✗ | ◐ | – | 2 | yes | **MEDIUM** — "Headline" in lieu of Verdict/Status; no spec/reproduce/run.log |
| 2026-05-24-followup-alpha-prior | ✗ | ✓ | ✓ | ◐ | ✓ | ✓ | ◐ | – | 1 | yes | **MEDIUM** — most complete of the 05-24 four (only one with both a Reproduce section and a real `outputs/run.log`); reproduce cmd points at sapphire scratch path, not repo path; no spec |
| 2026-05-24-followup-noncentred-grw | ✗ | ✓ | ✓ | ◐ | ✓ | ✗ | ◐ | – | 2 | yes | **MEDIUM** — REPORT + reproduce; no run.log; no spec; sapphire-scratch reproduce path |
| 2026-05-24-followup-systematics | ✗ | ✓ | ✓ | ◐ | ✗ | ✗ | ✓ | – | 4 | yes | **MEDIUM** — best-cited of the four (Obs 38/51); strong REPORT; no spec/reproduce/run.log |
| 2026-05-24-type-stratified-narrow-spas | ✗ | ◐ | ✓ | ✗ | ✗ | ✗ | ✓ | – | 4 | yes (reusable classifier) | **MEDIUM** — polished 262-line REPORT but no Status/Verdict banner; no seed/sha256/reproduce/run.log; strong external linkage (Obs 54, 77) |
| 2026-05-24-validation-investigation | ✗ | ◐ | ✓ | ◐ | ✓ | ◐ | ✓ | – | 2 | yes | **MEDIUM** — 366-line REPORT + reproduce + real `outputs/experiment-a.log`; no status banner/spec; partial log (A only). Backs Obs 52/53 |
| 2026-05-25-martin-consultation-prep | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | 0 | **transient** | **N/A** — pre-meeting briefs; underlying findings live in type-stratified dir / Obs 54 |
| 2026-05-26-letter-count-probe | ✓ | ✓ | ✓ | ◐ | ◐ | ◐ | ✓ | ✓ | 6 | yes | **LOW** — best-documented older run (locked verdict thresholds; genuine supersede banner; Obs 58/59 bidirectional). Defects: **broken Obs path** REPORT.md:9–10 cites `docs/notes/reflections/working-notes.md` (does not exist; canonical is `docs/notes/working-notes.md`); RUN-LOG covers Block 6 only |
| 2026-05-26-recovery-grid-two-unit | ✓ | ✓ | ✓ | ◐ | ✓ | ◐ | ✓ | ✓ | 5 | yes (central recovery result) | **LOW** — full spec + 3 REPORTs + correct supersede banner (`comparison/RUNBOOK.md:68`); no sha256; run.log sapphire-only/uncommitted |
| 2026-05-30-s5-small-n-trajectories | ✓ | ✓ | ✓ | ◐ | ◐ | ✗ | ✓ | ◐ | 7 | yes (foundational) | **MEDIUM** — feeds many later runs; **no run.log anywhere**; no output sha256; outputs nested under `code/production/` not `outputs/`; **`PRODUCTION-READY.md:5–6` says "has NOT been launched … Awaiting Shawn's go"** while `RESULTS.md` says COMPLETE/launched 2026-05-31 — contradiction, no reconciling banner; SMOKE-*.md superseded scaffolding unbannered |
| 2026-06-02-recovery-utility-check | ✗ | ✗ | ✓ | ◐ | ◐ | ◐ | ◐ | – | 6 | yes | **MEDIUM** — worst-documented *genuine* run: **no spec, no REPORT, zero in-dir markdown**; all findings externalised to Obs 67/68/69/73 (which carry artefact paths); `outputs/band-cal.log` is real. Not HIGH only because the Obs register fully carries it with re-verifiable anchors |
| 2026-06-03-small-n-reachability | ✓ | ✓ | ✓ | ◐ | ◐ | ◐ | ◐ | – | 2 | yes | **MEDIUM** — spec status "awaiting sign-off"; 46-line REPORT with verdict; `outputs/reach.log` real; no sha256/reproduce; in-dir docs cite no Obs back. Backs Obs 71 |
| 2026-06-04-envelope-finer-alpha | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0 | yes (load-bearing) | **HIGH** — contains **only** `outputs/reachability-by-cell.csv` + `reachability-records.jsonl`: no code, spec, report, seed, or Obs. Yet cited in a **lodged OSF amendment** (`planning/osf-amendment-2026-05-29-two-measure-framework.md:395`) and `continuity.md:434` ("confirmed α ≤ 0.70"). Not reproducible from its own dir; generating script absent |
| 2026-06-04-h3a-confirmatory | ◐ | ✓ | ✓ | ◐ | ◐ | ✗ | ✓ | ◐ | 3 | yes (load-bearing β source) | **MEDIUM** — `idata-primary.nc` reused as β source downstream; but `outputs/REPORT.md:3` **still "Status: PRELIMINARY — pending Shawn's sign-off"** though signed off (Decision 37) and OSF Amendment 02 lodged — the 2026-06-06 label-flip pass updated the sibling JSONs/companion reports to CONFIRMATORY but **missed REPORT.md**; spec offsite; no run.log |
| 2026-06-05-template-dictionary | ◐ | ✓ | ✓ | ◐ | ✗ | ✗ | ✓ | ✓ | 4 | yes | **MEDIUM** — REPORT + Obs 76; spec partial; no reproduce/run.log/sha256 |
| 2026-06-06-amendment-02-prep | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ◐ | – | 1 | mostly transient | **LOW** — amendment prose + label-flip script; one genuine Obs-79-cited micro-analysis (`reconcile-province-maps.py`) |
| 2026-06-06-convention-basis-redesign | ✓ | ✓ | ✓ | ◐ | ✓ | ◐ | ✓ | ✓ | 3 | yes | **LOW** — full triage→full-grid→verdict-gate narrative in-tree; Obs 76/78; no sha256 |
| 2026-06-07-amendment-03-prep | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | – | 0 | **transient** | **N/A** — pandoc prose-assembly emitting OSF amendment text |
| 2026-06-07-h2.1-launch-prep | ✓ | ✓ | ✓ | ◐ | ◐ | ◐ | ✓ | ◐ | 4 | yes (production) | **MEDIUM** — actually the *executed* H2.1 production run (launch-spec §10: "PRIMARY RUN COMPLETE: 28/28"); folder name misleads; **no forward banner** to `cc-production-refit` which refit & superseded its production α's — a reader of `SUMMARY-FINAL.md` won't know it's stale |
| 2026-06-09-h3b | ✓ | ✓ | ✓ | ◐ | ✓ | ✗ | ✓ | ✓ | 19 | yes | **MEDIUM** — best supersede-banner discipline in the project (clean 3-stage chain, every stale artefact `⚠ SUPERSEDED`/`RESOLVED`); Obs 82/92/93; only gap is no committed run.log |
| 2026-06-09-informed-alpha | ✗ | ◐ | ✓ | ◐ | ✗ | ✗ | ✓ | ◐ | 2 | yes | **MEDIUM** — no spec; report partial; Obs 81; no reproduce/run.log |
| 2026-06-09-joint-identifiability | ✓ | ◐ | ✓ | ◐ | ◐ | ◐ | ✓ | ◐ | 18 | yes | **MEDIUM** — 5 specs, no consolidated REPORT; **stale spec Status lines** (`full-grid-spec.md:3` "PROPOSED — needs sign-off", `cross-classified-spec.md:3` "PROPOSED" though signed off, run, and adopted as production lead per `cross-classified-signoff.md:307`/Obs 89); `MEMORY-FIX-AND-RUN-STATUS.md` + `priority-papers-status.md` are un-archived scratch left in run root |
| 2026-06-13-cc-production-refit | ✓ | ✓ | ✓ | ◐ | ✓ | ◐ | ✓ | ✓ | 8 | yes (feeds H3b) | **LOW** — most-traced (8 Obs w/ commit hashes); the only **draw-integrity** PROVENANCE-MANIFEST (verifies draw reproduction, not input sha256); inline supersession disclosure |
| 2026-06-14-amendment-04-prep | ✗ | ✗ | ◐ | ✗ | ✗ | ✗ | ✗ | – | 0 | **transient** | **N/A** — OSF amendment prose-assembly |
| 2026-06-14-hybrid-robustness | ✓ | ✓ | ✓ | ◐ | ✓ | ◐ | ✓ | ✓ | 4 | yes | **LOW** — exemplary disambiguating README; Obs 91; folder undersells itself; no sha256 |
| 2026-06-16-deconv-leverage-diagnostic | ✗ | ✓ | ✓ | ◐ | ✓ | ✗ | ✓ | ◐ | 4 | yes | **LOW** — REPORT + reproduce + Obs 94/95; no spec; no run.log |
| 2026-06-16-s5-layer-b-beta-inversion | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | 10 | yes | **LOW** — strongest near-exemplar (seed + **sha256** `21e985…`, bonus INPUTS.md); only flaw: `spec.md:3` Status frozen "DRAFT — awaiting … sign-off. Do not execute" with §11 boxes unticked though REPORT COMPLETE. Obs 102 |
| 2026-06-16-s5-sensitivities | ✗ | ◐ | ✓ | ◐ | ✗ | ✗ | ✓ | ◐ | 12 | yes | **MEDIUM** — most divergent of the s5 family: no spec, no top-level run.log (per-script logs), 3 DRAFT-banner reports, `d12-…-results.json` no provenance; `outputs/REPORT-b4.md` "MATERIAL" verdict later reversed to "robust" with no forward stale-banner. Obs 95 |
| 2026-06-17-s5-h5-habit-removed | ✓ | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ | – | 14 | yes | **LOW** — spec + COMPLETE report (cites Obs 98); deterministic provenance block but no seed/sha256. Obs 97/98 |
| 2026-06-17-s5-h7-perperiod-h3c | ✓ | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ | – | 6 | yes | **LOW** — best run.log of its group; seed present, no sha256 (MCMC). Obs 99 (register→dir only) |
| 2026-06-17-s5-layer-b-residual | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | 8 | yes | **LOW** — meets/exceeds exemplar (12-section spec, seed + sha256, self-check guards); only delta: spec Status still "DRAFT — Do not execute" though §12 sign-off ticked. Obs 103 |
| 2026-06-17-s5-peak-scaling | ◐ | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ | – | 5 | yes | **MEDIUM** — lighter 6-section spec (no sign-off/self-check/verdict-logic); seed no sha256; no in-doc Obs cite (lodged as Obs 100); stray duplicate `outputs/run.log` |
| 2026-06-18-c10-validity-test | ◐ | ◐ | ✓ | ◐ | ◐ | ✓ | ✗ | ✗ | 0 | yes | **HIGH** — `BUILD-NOTES.md:3` + `C10-FOLLOWUP-NOTES.md:3` **"BUILT, NOT RUN"** while `outputs/VALIDITY-REPORT.md` (verdict "(a) SUPPORTED"), `followup-ii-report.md`, `run-c10-full.log`, `results.json` (seed 20260618) all show **two full result-bearing waves ran**; verdict reports buried in `outputs/` (no root REPORT/Status banner); **0 Obs** |
| 2026-06-18-h2.1-supplementary-wave | ◐ | ◐ | ✓ | ◐ | ✗ | ✗ | ✗ | ✗ | 0 | yes (production) | **HIGH** — `SPEC.md:6` **"DRAFT — pre-launch sign-off pending"** + `BUILD-NOTES` "Nothing has been run" while `outputs/REPORT.md` is the **canonical all-29-unit production read-off** (generated 2026-06-18T13:30) with α medians + CIs; REPORT has **no Status banner / no Verdict heading**; **no top-level run.log**; **0 Obs** |
| 2026-06-18-h7-latin | ✓ | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ | – | 5 | yes | **LOW** — clean frame-swap; count-verification table + hard-stop guard substitute for sha256; REPORT COMPLETE cites Obs 99/101; honest provenance note (agent blocked from writing REPORT) |
| 2026-06-18-h9-letter-mass-h3a | ✗ | ✗ | ✓ | ◐ | ✗ | ✓ | ✗ | ✗ | 0 | yes (confirmatory-adjacent) | **HIGH** — `BUILD-NOTES.md:3` **"CODE BUILT, NOT RUN"** while `run.log:1` shows a real run (2026-06-18T08:35:24Z) and `outputs/h9-results.json` (seed 20260618) exist; **no spec, no REPORT**; verdict ("f_within supported") exists **only in commit subject `ec99343`**; **0 Obs**. Weakest doc-to-result gap in the project |
| 2026-06-18-peak-scaling-latin | ✓ | ✓ | ✓ | ◐ | ✗ | ✓ | ✓ | – | 4 | yes | **LOW** — same clean pattern as h7-latin; REPORT COMPLETE cites parent Obs 100; no sha256 |
| 2026-06-18-province-size-regression | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | 4 | yes | **EXEMPLAR** — all 8 components; Obs 105 |
| 2026-06-18-s5-size-vs-dynamics | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ◐ | 4 | yes | **LOW** — exemplar's parent/twin (spec `Status: EXECUTED`, seed + sha256, Obs 104); soft spot: its "province-mediation" inference partly walked back by Obs 105 with no forward-pointer banner here |
| 2026-06-19-d13-alpha-as-translator | ◐ | ✓ | ✓ | ◐ | ◐ | ✗ | ✓ | – | 6 | yes | **MEDIUM** — REPORT exists but mis-located at `outputs/D13-REPORT.md` (hidden from root listing); also lodged Obs 107; `spec.md:3` Status still "DRAFT … Do NOT launch compute until signed off" though run completed; **no run.log** for a 163-per-city-fit MCMC run |

**Counts (genuine runs only; transients excluded):** HIGH = 5 · MEDIUM = 19 · LOW = 14.
**Transient / N-A (no uplift needed):** 8 (prior-art-scouts, zotero-batch-add,
baorista-install, data-profile-smoke, reachability-guide, martin-consultation-prep,
amendment-03-prep, amendment-04-prep). amendment-02-prep is mostly transient but LOW.
h3a-brms-shadow is a correctly self-flagged deferred build (LOW).

---

## (d) Prioritised "results documentation uplift" task-list

Highest-severity first. Each task is concrete and actionable. (No edits were made; this
is the to-do list.)

### Tier 1 — HIGH: result exists but the directory's own docs deny it, or it is not reproducible / not reported anywhere

These five are the gate to writing from `runs/` safely. A co-author reading the dir's own
status banner would draw the wrong conclusion.

1. **`runs/2026-06-18-h9-letter-mass-h3a/`** — the worst gap. (a) Flip `BUILD-NOTES.md:3`
   "CODE BUILT, NOT RUN" → an EXECUTED status with the run timestamp from `run.log:1`;
   (b) add a `REPORT.md` (or `*-VERDICT.md`) stating the verdict that currently lives
   **only** in commit `ec99343` ("f_within supported (all frames)"), with the α medians
   from `outputs/h9-results.json`; (c) lodge an `Obs N` entry in `working-notes.md`
   (the existing "letter-mass" Obs 59/61 are the *earlier* 2026-05-26 work, not this run);
   (d) add/locate a `spec.md`.
2. **`runs/2026-06-18-c10-validity-test/`** — (a) flip `BUILD-NOTES.md:3` and
   `C10-FOLLOWUP-NOTES.md:3` "BUILT, NOT RUN" to a completed status; (b) promote a root
   `REPORT.md` with a Status banner pointing to the two existing in-`outputs/` verdict
   reports (`VALIDITY-REPORT.md` "(a) SUPPORTED — C10 stands"; `followup-ii-report.md`);
   (c) lodge the C10-validity verdict as an `Obs N` (currently 0 Obs).
3. **`runs/2026-06-18-h2.1-supplementary-wave/`** — (a) flip `SPEC.md:6` "DRAFT —
   pre-launch sign-off pending" and the BUILD-NOTES "Nothing has been run" to EXECUTED;
   (b) add a Status banner + Verdict heading to the existing canonical all-29-unit
   `outputs/REPORT.md`; (c) add a top-level `run.log` (or note where the production run
   log lives); (d) lodge an `Obs N` for the supplementary wave (currently 0 Obs).
4. **`runs/2026-06-04-envelope-finer-alpha/`** — a result feeding a **lodged OSF
   amendment** with no code/spec/report/seed/Obs. (a) Recover and commit the generating
   script (the marathon log `continuity.md:434` says it ran on sapphire, n_jobs=14,
   ~25 min — find it in scratch or the `reachability.py` lineage); (b) add a short spec +
   REPORT stating the "α ≤ 0.70 gradual decline" verdict the amendment relies on;
   (c) lodge an `Obs N`. If the script is genuinely unrecoverable, add a banner saying so
   and pointing to the parent `reachability.py` commit, so the amendment's basis is at
   least traceable.
5. **`runs/2026-05-22-recovery-grid-validation/`** — `outputs/REPORT.md:8`
   "Validation verdict: FAIL" (line 12: 63.6% / 286 cells) is **overturned** by Obs 67
   (PASS 91.9%→98.6% under the corrected, field-standard criterion). Add a top-of-file
   **supersede banner**: "⚠ SUPERSEDED — this FAIL used a zero-tolerance divergence gate;
   re-scored to PASS under the corrected criterion, see Obs 67 / Decision 33." This is
   the single most dangerous stale result for a write-up.

### Tier 2 — MEDIUM: stale status banners that contradict reality, and missing-spec / missing-Obs-link on genuine results

6. **Flip the stale "DRAFT / not-launched / PRELIMINARY" spec & report banners on
   completed runs** (a one-line edit each; group as one hygiene pass):
   - `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md:3` "PRELIMINARY — pending
     sign-off" → CONFIRMATORY (the 2026-06-06 label-flip pass missed this one file; its
     own sibling JSONs already say CONFIRMATORY). **Load-bearing — this is the β source.**
   - `runs/2026-05-30-s5-small-n-trajectories/PRODUCTION-READY.md:5–6` "has NOT been
     launched … Awaiting Shawn's go" → reconcile with `RESULTS.md` (COMPLETE, launched
     2026-05-31). **Foundational — many later runs depend on its outputs.**
   - `runs/2026-06-09-joint-identifiability/full-grid-spec.md:3` and
     `cross-classified-spec.md:3` "PROPOSED — needs sign-off" → signed-off/EXECUTED
     (cross-classified was adopted as the production lead, `cross-classified-signoff.md:307`).
   - `runs/2026-06-16-s5-layer-b-beta-inversion/spec.md:3`,
     `runs/2026-06-17-s5-layer-b-residual/spec.md` (§12 ticked),
     `runs/2026-06-19-d13-alpha-as-translator/spec.md:3` — all "DRAFT — Do not execute"
     though run & reported. Flip to EXECUTED (the exemplar/size-vs-dynamics pattern).
   - `runs/2026-05-21-talk-prep/spec.md` "in flight (Block 1 in progress)" → complete;
     and either produce the promised `outputs/REPORT.md` or drop the promise.
7. **`runs/2026-06-02-recovery-utility-check/`** — worst-documented genuine run (no spec,
   no REPORT, zero in-dir markdown). Add a short REPORT pointing to Obs 67/68/69/73 (which
   already carry the artefact paths), and a one-line spec/Status. (Not Tier 1 because the
   Obs register fully carries the findings with re-verifiable anchors.)
8. **`runs/2026-06-19-d13-alpha-as-translator/`** — the REPORT exists but is mis-located
   at `outputs/D13-REPORT.md` (hidden from a root listing). Add a root `REPORT.md` (or a
   pointer), and a `run.log` for the 163-per-city-fit MCMC.
9. **Add forward supersede / "now stale, see X" banners** where a later run overturned or
   rebuilt an earlier one (navigation hazards for the write-up):
   - `runs/2026-06-07-h2.1-launch-prep/` → forward-banner to `2026-06-13-cc-production-refit`
     (which refit & superseded its production α's).
   - `runs/2026-05-22-recovery-grid-design/` → forward-banner to the validation FAIL +
     the empirical-Bayes rework.
   - `runs/2026-04-25-h1-simulation/outputs/REPORT.md` (v1, FP=1.000) → supersede banner
     pointing to `h1-v2/REPORT-v2-final.md` (Obs 19).
   - `runs/2026-06-16-s5-sensitivities/outputs/REPORT-b4.md` ("MATERIAL" verdict reversed
     to "robust") and `runs/2026-06-18-s5-size-vs-dynamics/` (inference walked back by
     Obs 105) → forward banners.
10. **Add `spec.md` + an in-report `Obs N` back-reference to the 2026-05-17 SPA diagnostic
    chain and the 2026-05-24 cohort** (date-range-filtered-spas, empirical-spa-shape,
    interval-width-diagnostic; date-range-threshold-analysis, empirical-pconv,
    empirical-pgen-prior, followup-*, type-stratified, validation-investigation,
    s5-sensitivities, s5-peak-scaling, deconv-leverage, informed-alpha). These are
    genuine, Obs-linked results whose **traceability is one-directional** (the Obs
    register cites them, but they never cite the Obs back). A one-line "→ Obs N" in each
    REPORT closes the loop cheaply. Promote the `followup-alpha-prior` REPORT (the only
    05-24 run with both a reproduce section and a real run.log) as the template to copy.

### Tier 3 — LOW: cosmetic / consistency

11. **Fix the broken Obs path** in `runs/2026-05-26-letter-count-probe/REPORT.md:9–10` —
    it cites `docs/notes/reflections/working-notes.md`, which does not exist; the
    canonical file is `docs/notes/working-notes.md`. (Grep the repo for the same wrong
    path elsewhere.)
12. **Reconcile the column-count contradiction** in
    `runs/2026-04-23-descriptive-stats/outputs/summary.md` (65 cols) vs run.log/decisions
    (63 parquet cols).
13. **Reconcile the "~31%" narrative figure** (Decision 38) against
    `runs/2026-05-24-empirical-pconv/` (REPORT gives 24.96% full pool / 35.93% F1+F3;
    flagged at `working-notes.md:2136`) before it lands in the paper.
14. **Repoint sapphire-scratch reproduce paths** in the 05-24 followup REPORTs
    (`/home/shawn/cc-scratch/...`) to repo-relative paths.
15. **Archive the scratch files** left in `runs/2026-06-09-joint-identifiability/` root
    (`MEMORY-FIX-AND-RUN-STATUS.md` — load-bearing as grid provenance, keep but mark;
    `priority-papers-status.md` → `planning/`).
16. **Adopt input `sha256` for deterministic-read runs** that lack it, and a one-line
    `## Reproduce` block, to bring the LOW near-exemplars (h7-latin, peak-scaling-latin,
    h5-habit-removed, h7-perperiod, convention-basis-redesign, hybrid-robustness,
    recovery-grid-two-unit) fully to exemplar standard. Lowest priority — none blocks a
    write-up.

---

## Verdict

**Uplift is needed before writing from `runs/` as-is — but the minimum set is small,
bounded, and mostly mechanical.** The recent (mid-June) cohort is genuinely
solid-and-consistent and could be written from today; the problems are concentrated.

- **The blocking minimum is Tier 1 (5 dirs) + task 6 (flip the stale banners).** Four of
  the five HIGH dirs are the *most recent* results (c10, h2.1-supp-wave, h9 from 18 June;
  envelope-finer-alpha feeding a lodged amendment) where the run completed but the
  directory's own status banner still says "NOT RUN" / "DRAFT" and **no Obs entry exists**
  — so these results are currently invisible to anyone navigating by the canonical Obs
  register or trusting the in-dir banners. The fifth (recovery-grid-validation) presents a
  **FAIL verdict that was overturned**, with no banner. Writing from the repo without
  fixing these risks either omitting real results or citing a discredited one.
- **Tier 2 is strongly advisable but not strictly blocking** — the genuine results there
  are reproducible and *are* lodged in the Obs register; the gaps are missing specs, stale
  "DRAFT" banners, one mis-located REPORT, and one-directional Obs links.
- **Tier 3 is cosmetic** and can follow the write-up.

The good news for the team: the project already has an excellent, repeatable template (the
province-size-regression / s5 cohort) and a rich, well-anchored Obs register (107 entries).
The uplift is bringing the five HIGH dirs and the stale-banner set up to that template, not
inventing one.
