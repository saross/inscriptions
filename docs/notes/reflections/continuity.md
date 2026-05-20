---
priority: 1
scope: always
title: "Continuity — inscriptions project (living doc)"
audience: "next CC instance picking up the project; Shawn after any break"
status: living; updated at end of each session
started: 2026-04-24
last-updated: 2026-05-17 (post stand-in statistical review; D27–32 incorporated; lodgement-ready)
---

# Continuity — inscriptions project

## How to use this file

- **This is the canonical living continuity doc.** It replaces per-session continuity notes.
- At **end of each session**: tick off items completed (`[x]`) with date, add new pending items, prune items that have become irrelevant.
- Session-specific reflections (texture, patterns, surprises) go in `reasoning-log.md` and `working-notes.md`, not here.
- Dated snapshot files (e.g., `continuity-2026-04-23.md`) are historical records — do not update them; use this file instead.

---

## Research state — one-paragraph snapshot (2026-05-20, post-lodgement; conference-talk prep in flight)

The **OSF preregistration is lodged** (commit `a2e40fd`; git tag `osf-lodgement-2026-05-20`; OSF DOI pending Shawn's confirmation post-submit). The lodged document and supplementary upload PDF reflect three rounds of adversarial review, a stand-in cross-model statistical review (Decisions 27–32), and four rounds of pre-lodgement quality fixes (pipe-in-table-cell escape; ASCII-flowchart sizing; URL-overflow via `pandoc -f markdown+autolink_bare_uris` + `xurl`). Martin's HMM-pivot proposal (his post-statistician-pack response) is logged as a post-lodgement extension on which Decisions 33+ will be drafted once he replies to our seven follow-up questions (sent 2026-05-19); the prior-art scout (`planning/prior-art-scout-2026-05-19-hmm-aoristic.md`) confirms the combination is genuinely novel and identifies baorista as the natural emission-layer foundation. **Decisions 1–32 are logged**; key decisions for orientation: 12 (Mundlak NBR + variance partition); 14 (Bayesian mixture + recovery sim); 18 (three-way H3a verdict); 19, 21, 23, 25 (the four Martin-flagged primary items); 20 (template-interval slab structure, supersedes 17); 22 (date-window-filtered counts for H3a / H3c); 27–32 (stand-in-review-driven refinements). Two pre-Phase-2 design artefacts (template-dictionary + recovery-grid-design) are deferred post-talk. **Current focus**: preliminary results for Shawn's RAC-TRAC 2026 TRAC7 talk on Friday 2026-05-22 14:20 — overnight planning done; implementation begins next session. Phase 2 / 3 substantive analyses (the full preregistered pipeline) remain designed but not-yet-implemented; that work tranche begins after the conference.

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

## Conference talk — RAC-TRAC 2026 (in flight, 2026-05-20 overnight → 2026-05-22 14:20 talk)

**The OSF preregistration was lodged 2026-05-20 (DOI pending Shawn's confirmation).** Immediately following lodgement, the project pivoted to producing preliminary results for **Shawn's TRAC7 talk at RAC-TRAC 2026 in Aarhus, Friday 22 May 2026 14:20, room Preben Hornung**. (See `planning/conference-talk-rac-trac-2026/conference-context.md` for full conference briefing.)

**Open question to confirm Friday morning:** Shawn originally described the talk as "Adela giving a 12-minute talk." Conference programme shows Shawn delivering the SPA / LIRE paper at 14:20 and Adela delivering her own marriage-ages paper at 12:20 in the same session. Who is presenting which content needs confirmation — for safety, content has been prepared on the assumption that the SPA / LIRE / Hanson-scaling material is delivered (whether by Shawn solo or by Adela on Shawn's behalf).

Scope: **Lean A+ (lean A + synthetic mixture-recovery demo + stretch Bayesian H3a)**, fallback to lean A.

Overnight artefacts produced (2026-05-20):

- [x] `planning/conference-talk-rac-trac-2026/conference-context.md` — full briefing (programme, audience, format)
- [x] `planning/conference-talk-rac-trac-2026/asset-inventory.md` — what figures / code / data exist that can be reused
- [x] `planning/conference-talk-rac-trac-2026/slide-outline.qmd` — 7-slide Quarto revealjs skeleton with speaker notes
- [x] `planning/conference-talk-rac-trac-2026/analysis-roadmap.md` — 36-hour hour-by-hour plan with decision gates
- [x] `planning/conference-talk-rac-trac-2026/talking-points-feedback.md` — anticipated objections, audience framing, feedback prompts
- [x] `planning/next-session-prompt-2026-05-21.md` — handoff for the morning session

Implementation plan summary (full detail in `analysis-roadmap.md`):

1. [ ] **Hours 0–4** Filter LIRE corpus (50 BC – AD 350; 180,609 rows); sanity-check counts against prereg figures
2. [ ] **Hours 4–10** Empire / province / city SPA figures (re-use 2024 notebook cells 134–161)
3. [ ] **Hours 10–18** Frequentist NBR-GLM Hanson scaling: β + bootstrap 95 % CI; comparison to Hanson 2021 β = 0.672
4. [ ] **Hours 18–26 (A+ stretch)** Synthetic mixture-recovery demo: one cell with known α + known genuine shape; pymc multinomial mixture; recovered posteriors
5. [ ] **Hours 26–30 (further stretch)** Bayesian within-between H3a fit (preregistered model) — drop entirely if mixture demo over-runs
6. [ ] **Hours 26–32** Assemble Quarto deck; speaker notes; render to HTML + PDF
7. [ ] **Hours 32–36** Speaker briefing for whoever is presenting; final reproducibility check; commit + push

**Key audience facts** (from conference scout):
- TRAC7 session organisers are Petra Heřmánková, Tomáš Glomb, Vojtěch Kaše — **the LIRE / SDAM creators**. Glomb wrote the Asclepius-cult paper we cite (2022). Be careful with corpus claims; be ready for substantive technical feedback.
- Adjacent talks: Sommerschield (Aeneas neural-net; 14:00, directly precedes); Bennett (global Roman epitaph patterns; 15:00).
- Slot is 20 min (Q&A batched at end of block); target 12 min talk leaves buffer.
- Session theme explicitly welcomes statistical-bias-mitigation + Bayesian work — the room is the right room.

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

## Tertiary / future-work analyses (not preregistered)

Logged for later consideration. Not part of the 2026-05-19 OSF lodgement; would be filed as post-lodgement OSF amendments or as follow-up paper material if pursued.

1. [ ] **Max-Hanson-pop vs peak-inscription-window scaling test.** Hanson's urban-area population estimates appear to be *max theoretical* populations (max settlement footprint × estimated population density per Chapter 4 methodology, Hanson 2016 pp. 49–80), not realised peak populations at a single moment — i.e., an envelope / carrying-capacity measure rather than a temporal snapshot. The preregistered H3a uses cumulative date-window-filtered inscription counts vs Hanson max-pop, which dimensionally pairs envelope-against-envelope. A complementary test would substitute the response with the **highest 25-year or 5-year inscription count** per city (sliding-window max), keeping Hanson max-pop as predictor. This pairs theoretical-max against realised-peak rather than envelope-against-envelope, and would reveal whether the scaling relationship holds when the response is a "peak-rate" measure rather than a "total-production" measure. Implementation notes: (a) only applicable to cities with sufficient N to make a peak-window meaningful — likely the Phase 1 urban-area threshold (~1,549 inscriptions) or a lower exploratory threshold; (b) for fairness, both 25-year and 5-year windows should be tested as a sensitivity; (c) Hanson 2016 catalogue (PDF at `~/Zotero/storage/FGM4PVSX/`) does not include per-city peak dates, so no comparable max-pop-date axis is available — the test is one-sided (variation in the response only). Diagnostic-confirmatory framing: report whether the β scaling exponent under peak-window response differs materially from the preregistered cumulative-count β. **Not preregistered now**; logged here so it isn't lost.

---

## Done — major recent milestones (2026-04-23 → 2026-05-17)

- [x] **Decisions 27–32 incorporated into prereg + decision log + changelog + pack** (2026-05-17 later). Six new decisions arising from the stand-in cross-model statistical reviews: D27 (recovery-sim refinements — replicate count ≥ 100; Wasserstein-1 supplementary shape metric); D28 (aoristic-MC supplementary fit); D29 (8th PPC category — posterior-predictive spatial autocorrelation on H3a residuals); D30 (two-tier PPC severity scheme); D31 (three-case interpretive guardrail for H3c(ii) Moran's I); D32 (population- / inscription-weighted `f_within` sensitivity). All threaded into prereg as clean methodological statements without provenance markers (provenance in decision log + changelog). Pack reframed inline-marker state from "proposed pending sign-off" to "incorporated; reversal via OSF amendment if Martin recommends." Five focused commits committed and pushed.
- [x] **Stand-in cross-model statistical review** (2026-05-17 later). ChatGPT 5.5 + Gemini 3 Pro reviews of the consultation pack, taking an "applied econometrician / statistician" role. Two cross-model-agreement items (replicate count thin; Pearson r too forgiving) plus five single-model items (all GPT5.5). Committed at `planning/GPT55-statistical-review.md` and `planning/gemini-statistical-review.md`. Drove Decisions 27–32 above.
- [x] **Martin statistician consultation pack** (2026-05-17). `planning/martin-consultation-pack-2026-05-17.md`, 863 lines, structured as exec-summary + 8-question list + deep-dive appendices, tuned for an applied-econometrician audience (Mundlak / identifiability / RDF / FDR-Holm vocabulary). Eight questions: 4 primary (D19 / D21 / D23 / D25) + 4 secondary (D12, D13, multiple-comparison policy, design-artefact contents). Goes to Martin 2026-05-17.
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
6a. `planning/martin-consultation-pack-2026-05-17.md` — the structured consultation pack sent to Martin. 863 lines; exec-summary + 8-question list + deep-dive appendices.
6b. `planning/GPT55-statistical-review.md` + `planning/gemini-statistical-review.md` — the two stand-in cross-model statistical reviews of the consultation pack (in an applied-statistician role; hedge against Martin's potential delay). Drove Decisions 27–32.
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

### 2026-05-17 (later — Martin pack + stand-in statistical review + D27–32)

- Drafted Martin consultation pack (`planning/martin-consultation-pack-2026-05-17.md`, 863 lines, exec-summary + 8-question list + appendices, applied-econometrician framing).
- Pre-pack-send hedge: ran stand-in cross-model statistical reviews with ChatGPT 5.5 + Gemini 3 Pro in an "applied econometrician / statistician" role. Both committed at `planning/GPT55-statistical-review.md` and `planning/gemini-statistical-review.md`.
- Two cross-model-agreement items emerged: replicate-count floor too thin (≥ 50 → ≥ 100); Pearson r too forgiving as shape-recovery metric (add Wasserstein-1 supplementary). Five single-model items (all GPT5.5): aoristic-MC sensitivity; 8th PPC category (posterior-predictive spatial autocorrelation on H3a residuals); population- / inscription-weighted `f_within` sensitivity; three-case interpretive guardrail for H3c(ii) Moran's I; two-tier PPC severity scheme.
- All seven items captured as **Decisions 27–32** in the decision log, each tagged "provisional pending Martin's eventual review; subject to OSF amendment."
- Prereg surgery to incorporate D27–32 across §3, §4, §5, §6, §7, and Field 3 — clean methodological statements without provenance markers.
- Changelog updated with a new "2026-05-17 (later) — Stand-in cross-model statistical review; Decisions 27–32" section.
- Pack `[stand-in update]` markers reframed from "Proposed pending sign-off" to "Incorporated; reversal via OSF amendment if your review recommends it."
- Five focused commits + push (482cc87, feae7c5, 88de0e5, 4bc67bd, 28fd3f7).
- Continuity.md + working-notes Obs 40/41 + next-session prompt drafted.

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
