---
priority: 1
scope: always
title: "Continuity — inscriptions project (living doc)"
audience: "next CC instance picking up the project; Shawn after any break"
status: living; updated at end of each session
started: 2026-04-24
last-updated: 2026-04-24
---

# Continuity — inscriptions project

## How to use this file

- **This is the canonical living continuity doc.** It replaces per-session continuity notes.
- At **end of each session**: tick off items completed (`[x]`) with date, add new pending items, prune items that have become irrelevant.
- Session-specific reflections (texture, patterns, surprises) go in `reasoning-log.md` and `working-notes.md`, not here.
- Dated snapshot files (e.g., `continuity-2026-04-23.md`) are historical records — do not update them; use this file instead.

---

## Research state — one-paragraph snapshot

Preregistration-drafting phase of the RAC-TRAC 2026 (May 2026) / JAMT-or-JAS paper on mixture-corrected summed probability analysis (SPA) of Latin inscriptions against Hanson (2016) urban population. Three-phase design (H1 min-thresholds simulation → H2 mixture-model validation → H3a/b/c population signal) locked in; preregistration draft at `planning/preregistration-draft.md` with 4 of 6 TBDs resolved as of 2026-04-24, 2 deferred by design. Empirical baseline verified: inscription–population scaling is robustly sublinear across four independent tests (Hanson 2021 β ≈ 0.67; HOL 2017 β ≈ 0.69 for functional diversity proxy; Carleton et al. 2025 β ≈ 0.3–0.5 for elite-honorifics; Ross 2024 archived preliminary β ∈ [0.47, 0.68] across OLS + NBR on LIRE v3.0, n = 816).

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
- **Sapphire for compute.** Any bootstrap sweeps, permutation tests, or CPU-intensive work runs on sapphire via SSH. Workdir is `~/Code/inscriptions` (note: NOT `~/inscriptions` — typo caused an agent stall 2026-04-22).
- **Agent-session-capture infrastructure is operational** (2026-04-24; `/recall agent-infrastructure`). Use agents liberally for research and context management — the session trail is persistently captured for open-science research-record purposes.

---

## Priority queue — before OSF preregistration submission

1. [ ] **Run H1 simulation** (~200 LOC Python; `tempun` + `scipy.stats.permutation_test` per Obs 3 / Decision 2).
   - Input: LIRE v3.0 at `archive/data-2026-04-22/LIRE_v3-0.parquet`.
   - Sweeps: city n ∈ {25, 50, 100, 250, 500, 1000, 2500}; province n ∈ {100, 250, 500, 1000, 2500, 5000, 10000, 25000}.
   - 1,000 iterations per cell; Decision 5 effect-size brackets + zero-effect calibration; exponential null primary + CPL secondary; detection-rate curves at 0.70 / 0.80 / 0.90.
   - Outputs → `runs/YYYY-MM-DD-h1-simulation/`.
   - Resolves TBD 1 (numerical thresholds) and enables TBD 5 (Holm-Bonferroni family).

2. [ ] **Write `scripts/h3a_brms_shadow.R`** (~50 LOC R stub).
   - Same model as pymc primary: `count ~ log_pop + (1|province)`, `family = negbinomial()`, `brms::brm()`.
   - Not on OSF critical path, but committing it gives Adela a concrete R-vernacular artefact to audit.

3. [ ] **Coherence re-read of `planning/preregistration-draft.md`** end-to-end.
   - Draft has been edited piece by piece during TBD walkthrough; smooth over internal references and confirm H1 / H2 / H3 flow reads cleanly.
   - Run before Adela sees it.

4. [ ] **Adela review pass.**
   - Shawn shares; timing unscheduled.
   - Any substantive revisions filed as an OSF amendment **before** execution.

5. [ ] **Submit to OSF** (open-ended registration template; mirror map-reader-llm project style).

---

## Priority queue — parallel, before paper-sprint Week 1 (2026-05-03)

- [ ] **`baorista` install on sapphire** (R + NIMBLE + C++). Sunday / Monday (2026-04-27/28). If install non-trivial, Decision 3 fallback demotes baorista from appendix figure to citation-with-rationale.
- [ ] **LIST vs LIRE swap decision.** Week-1 checkpoint. LIRE is primary; LIST extends envelope to AD 600 if ready.
- [ ] **Obs 11 editorial-convention-hierarchy test on 14 boundary years** (originally scheduled Thursday 2026-04-24; may already have run — check `runs/` directory).
- [ ] **Hanson (2021) letter-count attribution** (Obs 8). PDF is now local (Zotero GHPTNHBI / 9Z7EFZVA); verify the specific letter-count passage before any draft cites Hanson 2021 as letter-count source.

---

## 2026-05-03 scope commitment (Decision 7)

- [ ] **Journal venue** — JAMT (methods-heavy) vs JAS (balanced). Resolves TBD 6.
- [ ] **Single paper vs methods/results split** per FS-0 trigger conditions.
   - Trigger (a): methodology content exceeds 3,000–4,000 words.
   - Trigger (b): deconvolution + baorista produce substantively different results.
   - Trigger (c): Aeneas-partition outline suggests a natural companion submission.
- [ ] **May 2026 conference details** confirmed — abstract deadline, format (written vs slides), word count if written.

---

## Standing open items — not blocking, not timed

- [ ] **AD 2230 placeholder values in LIRE `not_after`** — Shawn to report to LIRE / SDAM team (already may have reported; confirm before nagging).
- [ ] **RAC-TRAC 2026 conference details** (abstract deadline, format, word count) TBC; RAC-TRAC-2026 Zotero subcollection (key `U2V6V6YD` in SDAM group 2366083) exists and is ready for citation-bucket use.
- [ ] **Key-scope hygiene** — current Zotero API key has `write: true` on Shawn's user library in addition to SDAM group. Regenerate with tighter scope when convenient. Low severity (personal library + project-scoped key).
- [ ] **Duplicate Zotero items** to merge in UI:
  - Hanson 2021 (GHPTNHBI / 9Z7EFZVA)
  - Hanson-Ortman-Lobo 2017 (PJ829ZHD / G855HU3P)
  - MacMullen 1982 (UGCEBQWY / P6ENVECW)
  - Crema 2016 SPD (ZFKYLSQ8 / Z2UKWW4D / BRL8V3RK)
  - Crema & Bevan 2020 rcarbon (multiple)
  - Carleton 2018 batch-add duplicate (T95BHV43 / GF82TVAB — safe to delete either; both have PDF attached).
- [ ] **Two PDFs missing for already-added Zotero items:**
  - Bevan 2017 PNAS (GM82BQQI) — PMC5724262 bot-blocked from this sandbox; Zotero Connector in a browser will work.
  - Carleton & Groucutt 2020 *Holocene* (4QMRBWB6) — no OA copy per Unpaywall; SAGE-paywalled. Institutional access or library fetch.

---

## Priority artefacts (read in this order if context is cold)

1. `planning/research-intent.md` — paper-level what / why. Primary reference for scope and framing.
2. `planning/preregistration-draft.md` — operationalised research-intent with design choices pre-committed. 4 of 6 TBDs resolved; see §8 for state.
3. `planning/decision-log.md` — 7 ADRs, especially **Decision 7** (paper architecture + scope-commitment path).
4. `runs/2026-04-23-prior-art-scouts/synthesis.md` — consolidated Q1 / Q2 / Q3 findings (effect-size calibration, sublinear-scaling four-way convergence, translator-proxy strategy).
5. `planning/archive-2024-summary.md` — 2024 exploratory notebook distilled; empirical anchors (log-log R² ≈ 0.10 baseline, β ∈ [0.47, 0.68]); failed methods diagnosed (do not preregister without).
6. `planning/future-studies.md` — FS-A through FS-G disaggregation programme.
7. `docs/notes/reflections/working-notes.md` — 12 numbered observations (Obs 7 data-quality artefacts; Obs 11 editorial-convention hierarchy; Obs 12 Turchin scale mismatch).

---

## Failure modes observed — avoid

- **Path typos in agent briefs.** Sapphire workdir is `~/Code/inscriptions`, not `~/inscriptions`.
- **`pgrep -f` self-match.** A regex that matches its own invoking shell command. Use `pgrep -f "[.]venv/bin/python3.*verify.py"` (bracket-escaped first char) or `kill -0 <pid>` on a captured PID.
- **Agent stalling on inline script streaming.** Long Python scripts pasted as chat text can trigger watchdog timeouts at 600 s. Put script content in the `Write` tool's `content` parameter, not in chat.
- **Monitor loops tripping on stale files.** File-existence checks fire immediately if stale files from previous runs are present. Prefer mtime comparisons or fresh-run markers.
- **Zotero FTS does not index DOI field.** Idempotency-by-DOI via `zot.items(q=DOI)` fails silently and creates duplicates; use a locally-built DOI index over all group items instead (see `scripts/zotero_batch_add.py::_build_doi_index`).
- **Publisher bot-detection blocks Python default User-Agent.** Use browser-like UA for PDF downloads from Science.org, PNAS, SAGE, and NCBI PMC. Some fail even then — Zotero Connector in a real browser is the last-resort path.

---

## Session history — done items

### 2026-04-24 (Fri)

**Committed on main:**

- Captured memory: agent-session-capture infrastructure operational (openness / research-record / open-science / context-management / agent-infrastructure, id 2026-04-24-666890d8ab53).
- Verified Hanson 2021 β from local PDF (0.672 mean [0.588, 0.756] / 0.654 median [0.514, 0.774]; OLS log-log 8 bins; n = 554; EDCS; Rome excluded); research-intent + synthesis + archive-2024-summary updated (`d01a702`).
- Corrected Scout 2 misattribution — HOL 2017 β = 0.686 is functional-diversity × population, not inscription-count × population (`d01a702`).
- Demoted information-infrastructure from "complementary" to "alternative" framing per conference-paper editorial call (`3e4a6f4`).
- Captured Turchin 2018 scalar-complexity position as **Obs 12** in working-notes — polity × century vs city × decade scale mismatch (`50360ab`).
- Zotero: env-config + `.gitignore` hardening (`0138972`, `4534584`); SDAM group write-access verified (group 2366083; SPA collection `PZN5ATJK`, 37 pre-existing items).
- Batch-add of 21 items to SDAM SPA via `scripts/zotero_batch_add.py` + PDFs where OA (`e26278e`, `f820afb`); Carleton 2018 double-add flagged (idempotency gap in `zot.items(q=DOI)` diagnosed and fixed; script now uses `_build_doi_index`).
- Follow-up pass: 2 manual no-DOI adds (Beltrán Lloris OHRE chapter, Benefiel & Keesling Brill volume); 2 PDF retries succeeded via Unpaywall (Ortman-Lobo 2024 Sci Adv, Glomb 2022 JASRep) — `0822157`, `6e8355b`.
- `planning/preregistration-draft.md` drafted (monolithic, open-ended OSF format, ~250 lines) — `7ae3e93`.
- TBD walkthrough (all four actionables resolved; commits in parens):
  - TBD 1 — H1 protocol knobs + Glomb reframing (Antonine-anchored dropped; Glomb is a null, not a template). `228a8c6`, `c901aae`.
  - TBD 2 — pymc primary + `scripts/h3a_brms_shadow.R` as shadow for Adela / R-native co-authors. `630fdc4`.
  - TBD 3 — agnostic β prior `Normal(0, 2.5)` + weakly-informative defaults + Gelman et al. 2020 Bayesian-Workflow PPC suite (density overlay + test statistics + Pearson-residual structure). `f18db5b`.
  - TBD 4 — Moran's I via k-NN k = 8 primary + k = 5/10 sensitivity; qualitative Hanson-replication target (his weights construction not specified in the paper, so exact-numerical-match not feasible). `378e708`.
- LIRE subset-filter feasibility confirmed on disk: military diplomas 285 / 442 / 494 rows across `type_of_inscription_clean` / `_auto` / `inscr_type`; Asclepius-cult 358 rows via inscription text regex (vs Glomb et al.'s N = 210, so their filter was stricter).

### 2026-04-23 (Thu) — summary

Snapshot preserved at `continuity-2026-04-23.md`. High-level: comprehensive LIRE v3.0 descriptive-stats rerun; three parallel prior-art scouts commissioned overnight (effect-size calibration; urban-scaling; epigraphic-habit proxies); research-intent doc created; 2024 archive audit commissioned; 14+ commits across planning, runs, docs.
