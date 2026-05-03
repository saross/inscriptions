---
priority: 1
scope: always
title: "Continuity — inscriptions project (living doc)"
audience: "next CC instance picking up the project; Shawn after any break"
status: living; updated at end of each session
started: 2026-04-24
last-updated: 2026-05-03
---

# Continuity — inscriptions project

## How to use this file

- **This is the canonical living continuity doc.** It replaces per-session continuity notes.
- At **end of each session**: tick off items completed (`[x]`) with date, add new pending items, prune items that have become irrelevant.
- Session-specific reflections (texture, patterns, surprises) go in `reasoning-log.md` and `working-notes.md`, not here.
- Dated snapshot files (e.g., `continuity-2026-04-23.md`) are historical records — do not update them; use this file instead.

---

## Research state — one-paragraph snapshot (2026-05-03)

Preregistration is at `draft 2026-04-27` after two rounds of amendments — round 1 (2026-04-25) applied 5 amendments; round 2 (2026-04-26 to 2026-04-27) executed the **forward-fit pivot** (Decisions 8 / 9 / 10) plus added Crisis of the Third Century, H3a variance partition, §5 small-N city trajectory estimation (Layers A + B + aggregate diagnostic), and FS-4 follow-up paper. **H1 v2 simulation is COMPLETE** at full preregistered precision (1000 / 1000): FP control achieved (range [0.007, 0.049] across 96 zero cells); binding 50 % / 50 y thresholds in prereg §6. **baorista + brms + cmdstan installed and smoke-validated on sapphire** (commit `bf0d661`, INSTALL-LOG.md). The H2 / H3a / H3b / H3c / §5 substantive analysis pipelines are preregistered, designed, but **not yet implemented** — that's the next major work tranche after Adela's prereg review and OSF lock. Awaiting Adela review.

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

## Done — major recent milestones (2026-04-23 → 2026-05-03)

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

1. `planning/preregistration-draft.md` — current at `draft 2026-04-27`. Single most important document.
2. `planning/decision-log.md` — Decisions 1–10. Especially **8 (forward-fit pivot)**, **9 (precision + compute, drop CPL k=2)**, **10 (c_20pc_25y disposition)**.
3. `planning/backlog-2026-05-03.md` — current working backlog with structured "not yet implemented" + "open caveats" lists.
4. `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` — H1 v2 numerical thresholds (the empirical basis for prereg §6).
5. `runs/2026-05-03-baorista-install/INSTALL-LOG.md` — baorista + brms install record + API discoveries for the main pipeline.
6. `planning/future-studies.md` — FS-1 through FS-4.
7. `docs/notes/reflections/working-notes.md` — Obs 1–30 (Obs 15–30 are the H1 forward-fit pivot lessons).
8. `planning/preregistration-amendments-2026-04-25.md` — round-1 amendments record (round-2 was direct-edit + decision-log).
9. `planning/prior-art-scout-2026-04-25-aoristic-envelope.md` — literature scan that informed the forward-fit pivot; §8 empirical addendum on why scout-recommended Option A failed.

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
