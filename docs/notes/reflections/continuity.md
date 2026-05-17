---
priority: 1
scope: always
title: "Continuity — inscriptions project (living doc)"
audience: "next CC instance picking up the project; Shawn after any break"
status: living; updated at end of each session
started: 2026-04-24
last-updated: 2026-05-17 (post round-3 saturation)
---

# Continuity — inscriptions project

## How to use this file

- **This is the canonical living continuity doc.** It replaces per-session continuity notes.
- At **end of each session**: tick off items completed (`[x]`) with date, add new pending items, prune items that have become irrelevant.
- Session-specific reflections (texture, patterns, surprises) go in `reasoning-log.md` and `working-notes.md`, not here.
- Dated snapshot files (e.g., `continuity-2026-04-23.md`) are historical records — do not update them; use this file instead.

---

## Research state — one-paragraph snapshot (2026-05-17, post-round-3)

The preregistration has reached **conscious saturation** after three rounds of adversarial review and a structured QA pass. Round 1 (dual Claude Opus 4.7, 2026-05-14) produced six consensus blockers; round 2 (ChatGPT 5.5, 2026-05-16) produced ten substantive findings (bucket b) plus mechanical / verification items; round 3 (cross-model: ChatGPT 5.5 fresh-chat + Gemini 3 Pro fresh-context, 2026-05-17) returned only one cross-model-agreed BLOCKING finding and two single-model SHOULD-FIX items, all addressed. Both round-3 verdicts converge on "ready for Martin after these corrections" — corrections applied. **Decisions 12–26 are logged** in `decision-log.md`; **Decision 20 supersedes Decision 17** (the artefact reframing from "midpoint spikes" to "wide-template-slab editorial encoding + real ancient regnal clustering" was driven by three new diagnostics: `runs/2026-05-17-interval-width-diagnostic/`, `runs/2026-05-17-empirical-spa-shape/`, `runs/2026-05-17-date-range-filtered-spas/`). The 2026-05-17 **comprehensive rewrite** of `preregistration-draft.md` (449 lines, +146 / −78 plus round-3 corrections) implements all of Decisions 18–26. The two pre-Phase-2 design artefacts (the template-dictionary scan at `runs/2026-05-XX-template-dictionary/` and the recovery-grid-design at `runs/2026-05-XX-recovery-grid-design/`) are named in the prereg and pinned procedurally; they are committed before any Phase 2 analysis runs. Four decisions (19 mixture observation model, 21 recovery-grid coverage rule + shape library, 23 H3c residual choice + asymmetric Moran's I, 25 numerical PPC thresholds) are explicitly flagged as **primary items for Martin's consultation**. Next deliverable: **Martin's statistician consultation pack** (Task #17). After Martin's input is incorporated, OSF lodgement. The Phase 2 / 3 substantive analysis pipelines remain preregistered-designed but not-yet-implemented — that work tranche begins after OSF lock.

---

## Standing rules — working-relationship register

**Durable.** Read before any substantial block of work. These are decisions, not hints; push back if a situation argues for revisiting a rule, but don't silently deviate.

- **Lab-not-dev-team.** Shawn is PI; main-thread CC is senior analyst / RSE; subagents are specialist consultants. Peer review and Adela are critical friends outside the thread.
- **Critical-friend on statistics is a standing rule** (`~/personal-assistant/data/scratchpad.md`). For every statistical choice — his or yours — run four checks: (a) more appropriate test for the data structure? (b) more powerful / robust alternative? (c) more current best-practice approach? (d) do the method's assumptions actually hold? If yes to any, surface before executing.
- **Context-management band 50–75 %.** Don't pre-empt by truncating; don't skip skill invocations to save tokens. Shawn /reflects-and-exits around 50 %, gets aggressive at 75 %.
- **Pre-launch review** for phase / block / agent launches. Spec before launching. Don't auto-execute without sign-off on novel work.
- **Invoke skills fully.** If a skill is the right tool, use the Skill tool and work the protocol; don't shortcut.
- **Commit before each pipeline stage.** Research-record preservation matters.
- **Push back when warranted.** Explicit standing invitation.
- **Sapphire for compute.** Any bootstrap sweeps, permutation tests, Bayesian sampling, or CPU-intensive work runs on sapphire via SSH. Workdir is `~/Code/inscriptions` (note: NOT `~/inscriptions` — typo caused an agent stall 2026-04-22). uv at `~/.local/bin/uv` (not in non-interactive PATH).
- **Hard-stop rules in agent briefs.** Especially: do NOT silently negotiate parameters down to fit time budgets — halt and report. Two prior incidents (H1 v1 silent bootstrap-from-LIRE; preliminary v2 silent 100/200 reduction) make this a learned-lesson.
- **Agent-session-capture infrastructure operational** (2026-04-24; `/recall agent-infrastructure`). Use agents liberally for research and context management — session trail persistently captured for open-science research-record purposes.

---

## Priority queue — Phase 2 substantive work (post-OSF lock)

Detailed in `planning/backlog-2026-05-03.md` §"What's preregistered, designed, but NOT YET IMPLEMENTED". Headlines:

1. [ ] **H2 mixture-model implementation.** Substantive methodological contribution. ~2-3 days. Preregistered §3 + Decision 7. Outputs `data/processed/city_level_for_h3a.parquet` which unblocks Track 2.
2. [ ] **H3a Bayesian NBR (pymc primary).** Primary quantitative substantive result. ~1-2 days. Awaits H2 output.
3. [ ] **H3a brms shadow execution.** Script ready (`scripts/h3a_brms_shadow.R`); awaits H2 output. ~30 min.
4. [ ] **H3b deviation detection** at H1-reachable cells (Holm-Bonferroni). ~1-2 days.
5. [ ] **H3b Antonine + Crisis-of-Third-Century replication tests.** ~1 day each.
6. [ ] **H3c residuals + Moran's I + provincial-capital t-test.** ~1 day.
7. [ ] **§5 H3a variance partition.** ~6 LOC; rolls in with H3a.
8. [ ] **§5 small-N city trajectory estimation** (Layers A + B + aggregate diagnostic). ~4-7 days incl. Layer B literature ground-truth assembly. Uses baorista (now installed).
9. [ ] **Decision 3 sensitivity comparison: forward-fit vs baorista.** ~1 day.
10. [ ] **§5 other exploratories** (stratified-by-class, scaling-residual, α-as-translator, chronological H3c, letter-count). Cheap each, run alongside H2/H3.

Order: H2 → H3a (with brms shadow + variance partition + sensitivities) → H3b (with replications) → H3c → §5 small-N + Decision 3.

---

## Done — major recent milestones (2026-04-23 → 2026-05-17)

- [x] **Round-3 saturation check — cross-model ChatGPT 5.5 + Gemini 3 Pro** (2026-05-17). Same prompt to both; ChatGPT in a fresh chat for cross-model orthogonality with Gemini's fresh-context. Strong cross-model agreement on one BLOCKING finding (H3c residual analysis was incorrectly described as receiving mixture correction — H3c residuals are computed from H3a's posterior and inherit H3a's date-filtered-count scope). Two single-model SHOULD-FIX items: ChatGPT (multinomial observation model normalisation precision); Gemini ("year-0" terminology — no year 0 in the Julian / Gregorian calendar). All three findings applied. **Both models' verdicts converge: "ready for Martin after these corrections."** See `planning/saturation-check-prompt-2026-05-17.md`, `planning/prereg-saturation-check-GPT55.md`, `planning/prereg-saturation-check-gemini.md` for the full record. Conscious saturation reached; no further adversarial revision cycles needed before Martin's consultation.
- [x] **QA pass on the 2026-05-17 rewrite** (2026-05-17, between rounds 2 and 3). Fresh-context Claude agent against a structured QA brief (stale-framing detection; internal consistency; cross-reference correctness; decision-log consequences fulfilled). 1 BLOCKING + 4 SHOULD-FIX + 2 MINOR findings — all internal-consistency / stale-phrase issues. All applied.
- [x] **2026-05-17 comprehensive rewrite of `preregistration-draft.md`** (+146 / −78; 449 lines pre-QA; ~451 lines post-QA-and-round-3). Implements Decisions 18–26 + bucket (c) mechanical fixes + the QA-pass and round-3 corrections.
- [x] **Decisions 18–26 logged** (2026-05-17), all flagged in the decision-log. **Decision 20 supersedes Decision 17** (template-interval slab convention component replaces the three-tier anchor-year structure). Four are primary statistician questions for Martin: **19** (multinomial primary + Dirichlet-multinomial / rescaled-NegBin supplementary), **21** (procedural recovery-grid + per-cell repeated-replicates coverage rule + design artefact), **23** (Pearson residuals draw-wise for capitals contrast; posterior-mean for Moran's I with field-standard permutation inference + supplementary draw-wise posterior distribution), **25** (numerical PPC failure triggers, specifics in the design artefact). Other Decisions: **18** three-way H3a verdict + probability ladder; **20** template-interval slab convention component; **22** H3a uses date-window-filtered counts (mixture corrects temporal analyses only); **24** freeze LIRE v3.0 for this OSF lodgement; **26** Hanson-population sensitivity + Western-Empire province list operationalisation.
- [x] **Three empirical diagnostics driving the 2026-05-17 artefact reframing** (2026-05-17). `runs/2026-05-17-interval-width-diagnostic/` (the corpus is dominated by exact-century-template intervals; the 22.8× / 41.5× / 18.8× / 39.7× "midpoint spike" ratios were partly a test-statistic artefact). `runs/2026-05-17-empirical-spa-shape/` (the actual SPA shows no anchor-year structure at AD 50/150/250; the largest narrow spikes are at AD 122.5 Hadrian and AD 77.5 Flavian; the 1 BC / AD 1 boundary is the largest single discontinuity at +1,159). `runs/2026-05-17-date-range-filtered-spas/` (regnal spikes amplify under narrow-precision filtering — they are real ancient clustering; the century-boundary plateau-step pattern is the editorial artefact).
- [x] **ChatGPT 5.5 round-2 cross-model adversarial review triaged** (2026-05-17). Sorted into four buckets (`planning/chatgpt-review-triage.md`): 0 superseded; 10 substantive (bucket b, walked through with Shawn one-at-a-time → Decisions 18–26); 9 mechanical / clarity (bucket c); 2 verification (bucket d, both resolved during triage — Phase 1 96-cell arithmetic + Carleton 2018 attribution wording; neither was a confabulation).
- [x] **Adversarial-review-driven revision of the preregistration** (2026-05-14 → 2026-05-16). Dual fresh-context Opus 4.7 reviewers (one statistical-methodology focus, one domain-legibility focus) applied a shared prereg-failure-mode rubric; produced 6 consensus blockers + serious single-agent findings. Triage closed all of bucket (c) (11 items) and produced Decisions 12–17. See `planning/preregistration-changelog.md` "Adversarial-review-driven revision" section for the full timeline.
- [x] **Decisions 12–17 logged** (2026-05-14 → 2026-05-16). 12: rescope primary RQ + promote variance partition to confirmatory via within-between (Mundlak) H3a NBR; 13: bounded exploratory temporal "habit-removed residual trajectory" analysis; 14: Bayesian mixture model + recovery-sim validation; 15: H3b recast as pre-specified exploratory deviation-detection; 16: drop H3c regional-pattern clause (Hanson 2021 confabulation); 17 SUPERSEDED by Decision 20: had specified an empirically-grounded `convention_SPA` shape with three anchor-year tier components, supersession 2026-05-17 reflects the diagnostic reframing.
- [x] **Editorial-convention-hierarchy diagnostic** (2026-05-15). Five-test run on filtered LIRE v3.0. Findings reinterpreted by the 2026-05-17 diagnostics: the int-truncated-midpoint test statistic the diagnostic used conflated wide-slab loading with midpoint anchoring; under the actual per-year aoristic SPA, no anchor-year mass is present at AD 50/150/250. Decision 17 superseded as a result; this run's data is still committed and reproducible.
- [x] **Preregistration rewrite for lodgement** (2026-05-16, commit `eb189df`). 358 lines changed; implemented Decisions 12–17 + bucket (c) + bucket (d). Subsequently rewritten again on 2026-05-17 for Decisions 18–26.
- [x] **Pre-lodgement citation audit** (2026-05-16, commit `c322de6`). Three confabulations caught (Hanson 2021 regional pattern; SR1 design wording; Duncan-Jones 2018 ~85 %); paragraph-number error fixed; wording-drift items refined; Rome verification script committed.
- [x] **ChatGPT 5.5 cross-model adversarial review** (2026-05-17, committed at `planning/cross-model-adversarial-review-preregistration.md`). Engineered via a prereg-failure-mode-rubric-aware prompt (not generic QA). Lengthy; asks for changes; triage queued.

## Done — earlier milestones (2026-04-23 → 2026-05-03)

- [x] **H1 v1 simulation** (2026-04-25). Surfaced FP-inflation problem; informed forward-fit pivot. Now superseded.
- [x] **Forward-fit pivot** (Decisions 8 / 9 / 10, 2026-04-26 to 04-27). New methodology: forward-fit nulls in true-date space + forward-aoristic MC. CPL k=2 dropped per Decision 9; c_20pc_25y retained as hard-test boundary per Decision 10.
- [x] **Forward-fit primitives** (`forward_fit.py`, `forward_fit_cpl.py`). Optimised with numba JIT (~5× speedup over baseline); validated FP control on 30-cell synthetic grid (mean FP 0.034).
- [x] **H1 v2 final simulation** (2026-04-26). 256 cells × 1000 iter × 1000 MC, ~4.7 h on sapphire 24-core. FP control achieved across all 96 zero cells. Headline thresholds locked.
- [x] **Round 1 prereg amendments** (2026-04-25, 5 amendments applied: filter-flag derivation, permutation-envelope wording, shape-bracket, CPL-3 + exploratories, tempun substitution).
- [x] **Round 2 prereg amendments** (2026-04-26 to 04-27, direct-edited): forward-fit + brms stanvar (§3); synthetic-from-null DGP + min_n_unreachable convention (§4); v2 numerical thresholds (§6); TBD 1 + multi-comparison resolved (§8); status field + provenance bumped. Plus Crisis of Third Century, H3a variance partition, §5 small-N city trajectory bundle, FS-4 follow-up.
- [x] **FS-3 trapezoidal aoristic shape** added 2026-04-25.
- [x] **FS-4 provincial prosperity reconstruction** added 2026-04-27.
- [x] **Working-notes Obs 15–30** appended (2026-04-27): forward-fit pivot lessons, engineering wins, agent-routing patterns.
- [x] **baorista + brms + cmdstan install on sapphire** (2026-05-03 to 05-04). All packages working; smoke tests PASS at n=100/500/5000; install script idempotent on fresh R install (user-library bootstrap fix). INSTALL-LOG.md captures all stages + API discoveries + open caveats.
- [x] **Working backlog 2026-05-03** (`planning/backlog-2026-05-03.md`). Captures all preregistered-but-unimplemented work + open caveats.

---

## Priority artefacts (read in this order if context is cold)

1. `planning/preregistration-changelog.md` — full revision history through the 2026-05-16 rewrite, the citation audit corrections, the ChatGPT pass, the 2026-05-17 rewrite, the QA pass, and the round-3 saturation check. **Start here** for the most efficient orientation to current state.
2. `planning/preregistration-draft.md` — current preregistration (post-round-3). Single most important document. ~451 lines.
3. `planning/decision-log.md` — Decisions 1–26. **Most recent and highest-relevance: 18–26 (round-2-driven, 2026-05-17)**, especially the four Martin-flagged: 19 (multinomial likelihood primary + supplementaries), 21 (procedural recovery-grid + per-cell coverage rule + design artefact), 23 (Pearson residuals + asymmetric draw-wise / posterior-mean treatment), 25 (numerical PPC triggers). Also recent: **12 (within-between H3a + variance partition primary)**, **14 (Bayesian mixture + recovery sim)**, **15 (H3b exploratory)**, **16 (drop H3c regional pattern)**. **Decision 17 SUPERSEDED by Decision 20** (artefact reframed from anchor-year spikes to template-interval slab structure).
4. `planning/chatgpt-review-triage.md` — the four-bucket triage of round-2 ChatGPT findings (0a / 10b / 9c / 2d).
5. `planning/cross-model-adversarial-review-preregistration.md` — the round-2 ChatGPT 5.5 review verbatim.
6. `planning/saturation-check-prompt-2026-05-17.md` + `planning/prereg-saturation-check-GPT55.md` + `planning/prereg-saturation-check-gemini.md` — round-3 cross-model saturation check prompt and the two model responses.
7. `runs/2026-05-17-interval-width-diagnostic/outputs/REPORT.md`, `runs/2026-05-17-empirical-spa-shape/outputs/REPORT.md`, `runs/2026-05-17-date-range-filtered-spas/outputs/REPORT.md` — the three diagnostics driving Decision 20 (artefact reframe from "midpoint spikes" to "wide-template-slab editorial encoding + real ancient regnal clustering").
8. `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` — H1 v2 thresholds; the empirical basis for prereg §6 (seed 20260425, commit `00aceb4`).
9. `runs/2026-05-15-editorial-convention-hierarchy/outputs/REPORT.md` — historical diagnostic that originally grounded Decision 17. Reinterpreted by the 2026-05-17 diagnostics (the int-truncated-midpoint test statistic this run used conflated mechanisms); data still committed and reproducible.
10. `runs/2026-05-03-baorista-install/INSTALL-LOG.md` — baorista + brms install record.
11. `planning/backlog-2026-05-03.md` — Phase 2/3 substantive-work backlog (post-OSF-lock work).
12. `docs/notes/reflections/working-notes.md` — running observations.
13. `archive/planning/preregistration-amendments-2026-04-25.md` — historical round-1 amendments record.
14. `planning/prior-art-scout-2026-04-25-aoristic-envelope.md` — literature scan that informed the forward-fit pivot.

---

## Failure modes observed — avoid

- **Path typos in agent briefs.** Sapphire workdir is `~/Code/inscriptions`, not `~/inscriptions`.
- **`pgrep -f` self-match.** Use bracket-escape: `pgrep -f "[.]venv/bin/python3.*verify.py"` or `kill -0 <pid>` on a captured PID.
- **Agent stalling on inline script streaming.** Long Python / R scripts pasted as chat text trigger watchdog timeouts at 600 s. Put script content in the Write tool's `content` parameter, not in chat.
- **Monitor loops tripping on stale files.** File-existence checks fire immediately if stale files from previous runs are present. Prefer mtime comparisons or fresh-run markers.
- **Zotero FTS does not index DOI field.** Idempotency-by-DOI via `zot.items(q=DOI)` fails silently and creates duplicates; use a locally-built DOI index over all group items instead (see `scripts/zotero_batch_add.py::_build_doi_index`).
- **Publisher bot-detection blocks Python default User-Agent.** Use browser-like UA for PDF downloads from Science.org, PNAS, SAGE, NCBI PMC.
- **Agent silent-parameter-reduction is a critical-friend gate failure pattern.** Hard-stop rules in briefs that explicitly forbid renegotiating parameters to fit time budgets.
- **Background agents that arm a Monitor and exit don't re-fire from monitor events.** For "wait for PID death" patterns, use Bash `run_in_background` with `until ! kill -0 PID` instead.
- **baorista API gotchas** (from smoke-test iterations 2026-05-03):
  - `timeRange` must be descending (LARGER first).
  - `(upper - lower + 1) %% resolution == 0` required.
  - Per-event col1 > col2 (numeric ordering; NAMES `StartDate`/`EndDate` are conventional only).
  - Every event must satisfy `lower <= col2 <= col1 <= upper`.
  - `expfit` returns S3 `fittedExp` with `$rhat` / `$ess` directly — no `$samples` slot.
- **Sapphire fresh-R-install user-library bootstrap** (from 2026-05-04 install fix): without creating `R_LIBS_USER` and pushing it onto `.libPaths()`, `install.packages()` falls back to root-owned `/usr/local/lib/R/site-library` and crashes within seconds.

---

## Open caveats (housekeeping; not blocking)

Detailed in `planning/backlog-2026-05-03.md` §"Open caveats / housekeeping". Headlines:

- **Sapphire git state cleanup** — accumulated untracked-but-canonical-on-origin files. Cleanup script in backlog.
- **Smoke-test simplification** — synthetic widths capped at 100 y; production baorista runs on real LIRE need re-validation with full-distribution widths.
- **n=50,000 baorista wall-time at default niter=100,000** — extrapolation 5–25 min; direct benchmark deferred to FS-4 launch.
- **LIST v1.2 swap** — optional; LIRE remains primary.
- **RAC-TRAC 2026 conference details** — TBC.
- **TBD 6 target journal venue** — leaning JAMT; soft commitment.

---

## If context feels cold

1. Read `planning/preregistration-draft.md` start to finish (~10 min).
2. Read `planning/backlog-2026-05-03.md` for what's left to do + caveats (~5 min).
3. Skim Decisions 8 / 9 / 10 in `planning/decision-log.md` for the methodological pivot rationale (~5 min).
4. Skim `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` for current empirical results (~3 min).

That's enough to engage substantively. Deeper context (the scout report, working-notes, amendment trails) reads in another 20-30 min if needed.

---

## Session history — done items (terse)

### 2026-05-17 (round 2 triage → round 3 saturation)

- Round-2 ChatGPT 5.5 cross-model review triaged into four buckets (0a / 10b / 9c / 2d). Bucket (d) verified during triage — neither item was a confabulation. See `planning/chatgpt-review-triage.md`.
- Three empirical diagnostics commissioned and consumed (interval-width, empirical-SPA-shape, date-range-filtered-spas). Reframed the artefact narrative end-to-end: wide-template-slab editorial encoding (the editorial artefact) plus real ancient regnal clustering at AD 77.5 / 122.5 / 212.5 (NOT artefact). 1 BC / AD 1 boundary is the largest single discontinuity in the SPA (+1,159 step).
- Bucket (b) walked through with Shawn one-at-a-time; Decisions 18–26 captured. Decision 20 supersedes Decision 17. Four decisions (19 / 21 / 23 / 25) flagged as primary statistician questions for Martin.
- Comprehensive prereg rewrite (~+146 / −78 over the 2026-05-16 baseline) implementing Decisions 18–26 + bucket (c).
- QA pass by a fresh-context Claude agent — 1 BLOCKING + 4 SHOULD-FIX + 2 MINOR — all applied.
- Round-3 saturation check via ChatGPT 5.5 (fresh chat) + Gemini 3 Pro (fresh context). Strong cross-model agreement on one BLOCKING finding (H3c residual analysis was incorrectly described as mixture-corrected — fixed in 5 prereg locations + 2 decision-log clarifications). Two single-model SHOULD-FIX items: ChatGPT (multinomial normalisation precision); Gemini ("year 0" terminology — no year 0 in Julian / Gregorian calendar). All applied. **Both models converge: ready for Martin.**
- Continuity.md updated; new-session prompt drafted at `planning/next-session-prompt-2026-05-17.md`.

### 2026-05-14 → 2026-05-16 (round 1 + first rewrite)

- Dual Claude adversarial review of the prereg (Opus 4.7, two parallel fresh-context Explore agents); 6 consensus blockers + serious single-agent findings.
- Bucket-(c) triage completed: 11 smaller decisions resolved with Shawn one-at-a-time, captured inline in the prereg.
- Decisions 12–17 logged in `decision-log.md` (Decision 17 later superseded by Decision 20, 2026-05-17).
- Hanson 2021 attribution re-verification surfaced the confabulated regional-pattern claim (two independent agents, page-anchored quotes pp. 147–148). Library scan (8 Hanson items in SDAM-AU + 22 `roman_demography` items + PDF abstracts) confirmed no Hanson-corpus paper carries the claim.
- Editorial-convention-hierarchy five-test diagnostic (`runs/2026-05-15-editorial-convention-hierarchy/`); empirically grounded the (now-superseded) Decision 17.
- Comprehensive prereg rewrite (commit `eb189df`, 2026-05-16; 358 lines changed). Subsequently rewritten again on 2026-05-17 to implement Decisions 18–26.
- Pre-lodgement citation audit (commit `c322de6`); three confabulations caught and corrected; Rome verification script committed; seven missing references found via web-search agent and added to Zotero by Shawn.
- ChatGPT 5.5 cross-model review prompt engineered to elicit orthogonal coverage (not parallel); round-2 review returned 2026-05-17 (commit `6862031`), triaged this session.

### 2026-05-03 / 2026-05-04

- baorista + brms + cmdstan installed on sapphire across all 5 stages (commits `066f25d`, `9d72aae`, `a41f394`, `c97d218`, `bf0d661`). Smoke tests PASS at n=100/500/5000.
- New working backlog `planning/backlog-2026-05-03.md` capturing post-pivot state.
- This continuity.md updated.

### 2026-04-26 / 2026-04-27

- Forward-fit pivot (Decisions 8 / 9 / 10).
- H1 v2 final simulation (256 cells × 1000 iter × 1000 MC, ~4.7 h on sapphire). FP control achieved.
- Round-2 prereg amendments direct-edited.
- Crisis of Third Century, H3a variance partition, §5 small-N city trajectory bundle, FS-4 added.

### 2026-04-25

- H1 v1 simulation (surfaced FP-inflation problem; superseded by v2).
- Round-1 5 prereg amendments applied.
- FS-3 trapezoidal added.
- Prior-art-scout report committed.

### 2026-04-24 (Fri)

Snapshot at this date in `continuity-2026-04-23.md`. Original H1 simulation design phase.

### 2026-04-23 (Thu)

Original methodology design + 2024 archive distillation + Hanson β verification + Zotero ingest. See `continuity-2026-04-23.md`.
