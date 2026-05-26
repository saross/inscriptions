---
priority: 1
scope: always
title: "Continuity — inscriptions project (living doc)"
audience: "next CC instance picking up the project; Shawn after any break"
status: living; updated at end of each session
started: 2026-04-24
last-updated: 2026-05-26 (letter-count probe complete; recovery-grid two-unit running on sapphire; "acts vs content" reframe locked)
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

## Martin Eftimoski consultation outcome — recalibration (2026-05-26)

The 2026-05-25 consultation with **Martin Eftimoski** (the project's statistician collaborator — comp-sci PhD candidate at UNSW, applied-econometrics undergrad-MA, co-author on the 2017-ish Kazanlak burial-mounds ordered-logit paper; weaker on Bayesian register) produced a different signal than the project had been planning around. Recalibration in summary:

- **Martin's role reframed: time-poor passion-project collaborator, not primary methodologist.** He's running his own business and pursuing a PhD; the inscriptions project is goodwill plus shared interest. Working assumption from here on: **one sanity-check read at draft-paper stage**; he will NOT engage in detail with the 8 consultation-pack questions (`planning/martin-consultation-pack-2026-05-17.md`), the 7 Stage-3 design decisions (`planning/stage-3-implementation-plan.md` commit `381c303`), or the four "Martin-flagged primary" decisions D19 / D21 / D23 / D25.
- **Editorial-convention correction (SPA, mixture model, empirical-Bayes pivot): we proceed on our own.** Martin's one-line gloss — *"Model the process based off the more granular inscriptions, then construct a confidence band around the 'slab' inscriptions given what has been observed. Use the more frequent / granular information to characterise the 'slabs'"* — is essentially the empirical-Bayes calibration-cohort architecture we have already designed (Obs 55 candidate; commit `8e1897b` Stage 2; commit `381c303` Stage 3 spec), expressed in frequentist register. He confirmed the approach is plausible without engaging design-deep. **Stage 3 (empirical-Bayes) remains the right pivot; proceed.**
- **Sample-size minima — "the data we have is the data we have."** Martin's framing: use what we have even with high uncertainty; let critics try to do better. **The §5 small-N city trajectories work is unblocked** (was hedged on Martin's guidance about minimum-N thresholds).
- **Population–inscription scaling coefficient: we develop it; Martin reviews at draft.** He's content with the current approach.
- **Letter-count nudge — promoted to active probe.** Martin thinks switching from inscription count to letter count is "crucial" — letter is a better unit of epigraphic production and information flow. Previously logged as a §5 exploratory; **promoted to in-flight probe beginning the 2026-05-26 session.**
- **HMM follow-up paper — parallel track.** Martin's real interest is a follow-up Hidden-Markov-Model paper: given inscription counts (or letter counts), what's the most likely latent population trajectory? Structural-break priors (rising → falling), at empire / province / city levels. This is **a second-paper track, not part of the current paper**. He's a Claude Code power user; he'll be invited to the GitHub repo and run his own analyses. **Action**: create a one-page stub at `planning/hmm-paper-stub/` to preserve the design idea; substantive HMM work deferred until the current paper is closer to draft.
- **Prereg framing of "Martin-flagged primary" decisions.** D19 / D21 / D23 / D25 — and the 7 Stage-3 design decisions — are now **project-decided with collaborator sanity-check at draft stage**, not awaiting-Martin-confirmation. Prereg framing to be amended in the next OSF amendment batch (not this session; flagged as backlog under Open caveats below).
- **Ceramics-aoristic action items** in the section below (10 items) **all remain relevant** — they are tools the project uses to do the work itself; Martin's non-engagement doesn't change their value. See cross-reference below.

---

## Conference talk — RAC-TRAC 2026 (in flight, 2026-05-20 overnight → 2026-05-22 14:20 talk)

**The OSF preregistration was lodged 2026-05-20 (DOI pending Shawn's confirmation).** Immediately following lodgement, the project pivoted to producing preliminary results for **Shawn's TRAC7 talk at RAC-TRAC 2026 in Aarhus, Friday 22 May 2026 14:20, room Preben Hornung**. (See `planning/conference-talk-rac-trac-2026/conference-context.md` for full conference briefing.)

**Speaker confirmed (2026-05-21)**: **Adela reads the paper on Shawn's behalf** at the 14:20 Friday TRAC7 slot. Shawn cannot travel to Denmark; RAC-TRAC does not support remote presentations. Adela also has her own separate paper at 12:20 in the same session (Roman marriage ages); the 14:20 slot delivers Shawn's SPA / LIRE / Hanson-scaling content.

**OSF preregistration confirmed (2026-05-21)**: `https://osf.io/uycs6/`, lodged 2026-05-20; **currently embargoed** pending the project's decision on whether to submit to a journal requiring double-blind review. The URL is publicly visible (unblockable); the deposit contents are gated. Embargo will lift once a venue is chosen. URL folded into: prereg §11 Provenance (post-lodgement amendment trail); slide deck footer + slides #5 and #7; project README.md.

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

## Post-Martin / methodology-refinement action items (added 2026-05-25; confirmed-relevant 2026-05-26 post-consultation)

**These are tools the project owns and applies itself — not asks of Martin.** All 10 items remain relevant under the 2026-05-26 recalibration (see top-of-doc section); Martin's non-engagement with design-detail does not change their value.

Concrete techniques to adopt from the ceramics-aoristic-dating community, surfaced by the closed-loop prior-art scout at `planning/prior-art-scout-2026-05-25-ceramics-aoristic-techniques/REPORT.md` (15 candidate techniques, verifier-PASS after one iteration). Companion lit-scout bibliography at `planning/lit-scout-2026-05-25-pottery-aoristic-roman/` (25 references; Brughmans / Aarhus cluster as the bridge community).

### Use directly — low cost, high leverage

1. [ ] **Dual-dating sensitivity test** — run the mixture model under (a) intervals-as-recorded and (b) tightened-to-Tight+F2_Other intervals; overlay. Quantifies bracket-sensitivity directly. *<1 day diagnostic, no model restructure. Source: Franconi et al. 2023 / Komar et al. 2025.*
2. [ ] **Interval-length duration reweighting** (`w_i = 1/Δτ_i`) on the input SPA before model fitting. Removes structural over-representation of century-slab inscriptions relative to Tight datings. *<1 day preprocessing. Source: Bevan & Crema 2021 — the MRUP paper.*
3. [ ] **Null-model permutation envelope for p_gen** — simulate 1,000 curves from a flat / exponential / logistic-growth null; overlay 2.5th-97.5th percentile band on the recovered posterior. Standard in radiocarbon SPD literature; conspicuously absent in ceramics-aoristic papers. *1-3 days. Source: Crema 2025 / `rcarbon::modelTest()`.*
4. [ ] **Site-binning normalisation** — group inscriptions by `provenance_site`, compute per-site SPA, normalise each to unity, sum. Addresses Rome / Ostia over-representation. *1-3 days. Source: Crema 2022 / Romanowska et al. 2022 / `rcarbon`.*
5. [ ] **Stacked sensitivity-bands as primary visualisation convention** — adopt the ceramics-community figure idiom (line for posterior median + shaded bands for methodological sensitivity) for the main results figures. *<1 day plotting change.*
6. [ ] **Corpus-source stratification supplementary** — run the pipeline separately on CIL / AE / EDH-derived subsets; present three p_gen curves side-by-side as a robustness annex. Pre-empts the corpus-heterogeneity reviewer objection. *<1 day. Source: Franconi et al. 2023 §Data.*

### Adapt — feasible but requires design decision

7. [ ] **Per-item phase-confidence weight** derived from family classifier (Tight → w=1.0, F1 century slab → w=0.7, F3 periodic → w=0.8, etc.). Sharpens the calibration-cohort signal. *1-3 days. Source: Bevan, Conolly et al. 2013 (Antikythera).*
8. [ ] **CPUE-style sampling-intensity denominator** using LIRE provenanced-sites-active-per-bin as the denominator. Addresses differential epigraphic-fieldwork intensity. *1-3 days; the denominator may itself be confounded — report transparently. Source: Orton, Morris & Pipe 2017.*
9. [ ] **Proxy cross-correlation as external validation** — normalise the recovered p_gen to [0, 1] and correlate against the Palmisano et al. 2017 central-Italy ceramic SPA + Komar et al. 2025 Italian amphora SPA + OXREP proxy estimates. *1-3 days; comparison-data acquisition is the main cost. Source: Palmisano, Bevan & Shennan 2017.*
10. [ ] **Gaussian popularity curves for p_conv template internals** — non-uniform within-slab distributions parameterised by Stage 2 calibration-cohort empirical modes. *1-3 days. Source: Roberts et al. 2012 / `kairos::apportion()`.*

### Methodology-paper framing implication

The prior-art scout concluded that the LIRE mixture-model's explicit `p_conv` / `p_gen` decomposition is **genuinely novel** — the ceramics community handles editorial-convention heterogeneity through sensitivity stratification (Franconi et al. 2023 et al.) rather than through structural decomposition. The paper can frame this verbatim: *"where ceramicists treat convention heterogeneity as a sensitivity parameter (Franconi et al. 2023), we treat it as a structural model component that is simultaneously estimated."* This positions the methodology paper (if split off from the substantive paper) as bridging the inscription and ceramic literatures.

Software stack confirmed (all licences compatible): `kairos` (tesselle, GPL-3.0), `rcarbon` (ahb108), `archSeries` (davidcorton), `datplot` (lsteinmann, GPL-3.0), `CeramicApportioning` (mpeeples2008), plus `baorista` already in toolkit.

---

## Working-notes register — current state

Working-notes.md is at **Obs 60** (2026-05-26). The 9 proposed Obs 49–57 from the 2026-05-25 gap-analysis agent were landed via batch intake on 2026-05-26 (commit range `43d814d..65edb2e`); the `PROPOSED-OBS-49-57-for-review.md` staging file was deleted as part of the same intake. Obs 58 (commit `dd326dc`) captures the "acts vs content" reframe; Obs 59 (`de8fa8f`) corroborates it at the Mundlak f_within layer (+9.89 pp shift); Obs 60 (`2f86c95`) corroborates at the editorial-template-tier layer (pilot_proxy reign-weight quadruples under letter-mass). Obs 56 was flagged at intake as a promotion candidate to `~/personal-assistant/notes/llm-craft.md` (the bridge-the-clusters lit-scout heuristic).

---

## Talk-day handoff queue (2026-05-22 session close)

Pre-/post-talk work for the next session. **Read `planning/next-session-prompt-2026-05-22.md` first.**

1. [x] 2026-05-22 **Adela's feedback on the deck incorporated.** Substantial narrative reframe: less technical detail, more historical implications. Main path went from 9 main / 12 backup / 9 glossary to **9 main + 13 backup + 9 glossary**, with slide-6 merging old 6a/6b into "What we found" (the ~ 30 % within-province punchline) and demoting frequentist NBR to B12; slide-7a promoting Adela's wife/daughter corpus as a worked example. Feedback at `planning/conference-talk-rac-trac-2026/adela-feedback.md`; QA agent report at `qa-report-2026-05-22.md`.

2. [x] 2026-05-22 **Continuous speaker script composed.** `planning/conference-talk-rac-trac-2026/inscription-spa-script.md` and `.pdf` — ~ 1,900 spoken words across 10 slides (~ 12.7 min at 150 wpm). Plus a separate `inscription-spa-notes.{md,pdf}` standalone bullet-form notes extracted from the `::: notes` divs, for live glance reference.

3. [x] 2026-05-22 **Phase 2 grid restarted under optimised SMT-aware config.** Background-agent investigation diagnosed SMT saturation (19 workers on 12 physical cores) as the 3-4× slowdown cause; killed + restarted with `n_jobs=12` + `taskset -c 0-11` + `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`. Empirical post-restart per-fit times match prediction (N=2,000 ≈ 18 s; N=10,000 ≈ 30 s); wall-clock projection went from ~ 100 h to ~ 31.6 h. Grid running unattended. When done, run `runs/2026-05-22-recovery-grid-validation/code/05-grid-summariser.py` for per-cell pass-rate table + binding-criterion verdict. See `CONCURRENCY-INVESTIGATION.md` + `RESTART-LOG.md`.

---

## Priority queue — Phase 2 substantive work (post-OSF lock)

Detailed in `planning/backlog-2026-05-03.md` §"What's preregistered, designed, but NOT YET IMPLEMENTED". Headlines:

0. [x] **Letter-count probe — complete 2026-05-26.** Six blocks executed; REPORT at `runs/2026-05-26-letter-count-probe/REPORT.md` (commit `348ea25`). Three flags evaluated: Flag 1 SPA-shape MODEST (r ≈ 0.88-0.90); **Flag 2 Hanson β MATERIAL** (no CI overlap; β 0.566 → 0.515); **Flag 3 f_within MATERIAL** (Bayesian Mundlak, +9.89 pp; 30 % → 40 %). The probe's spec wrote a binary verdict rule that was superseded mid-session by Shawn's **"acts vs content" reframe** (Obs 58 commit `dd326dc`): inscription-count and letter-mass are complementary measures of partially-different constructs; their delta is itself a research object. Stage 3 will fit under both units in parallel. The recovery-grid two-unit re-simulation (`runs/2026-05-26-recovery-grid-two-unit/spec.md`) is now the Stage 3 launch gate; production running on sapphire PID 931910 since 2026-05-26 05:53 UTC; ETA ~76 h sequential; STATUS file at `~/Code/inscriptions/runs/2026-05-26-recovery-grid-two-unit/STATUS.txt` on sapphire.
1. [ ] **H2 mixture-model implementation.** Substantive methodological contribution. ~2-3 days. Preregistered §3 + Decision 7. Outputs `data/processed/city_level_for_h3a.parquet` which unblocks Track 2.
2. [ ] **H3a Bayesian NBR (pymc primary).** Primary quantitative substantive result. ~1-2 days. Depends on H2 output.
3. [ ] **H3a brms shadow execution.** Script ready (`scripts/h3a_brms_shadow.R`); depends on H2 output. ~30 min.
4. [ ] **H3b deviation detection** at H1-reachable cells (Holm-Bonferroni). ~1-2 days.
5. [ ] **H3b Antonine + Crisis-of-Third-Century replication tests.** ~1 day each.
6. [ ] **H3c residuals + Moran's I + provincial-capital t-test.** ~1 day.
7. [ ] **§5 H3a variance partition.** ~6 LOC; rolls in with H3a.
8. [ ] **§5 small-N city trajectory estimation** (Layers A + B + aggregate diagnostic). ~4-7 days incl. Layer B literature ground-truth assembly. Uses baorista (now installed). **Unblocked 2026-05-26** by Martin's "data we have is the data we have" framing — no longer hedged on minimum-N guidance.
9. [ ] **Decision 3 sensitivity comparison: forward-fit vs baorista.** ~1 day.
10. [ ] **§5 other exploratories** (stratified-by-class, scaling-residual, α-as-translator, chronological H3c). Cheap each, run alongside H2/H3. *(letter-count promoted to item 0 above.)*

Order: letter-count probe (in flight) → H2 → H3a (with brms shadow + variance partition + sensitivities) → H3b (with replications) → H3c → §5 small-N + Decision 3.

---

## Tertiary / future-work analyses (not preregistered)

Logged for later consideration. Not part of the 2026-05-19 OSF lodgement; would be filed as post-lodgement OSF amendments or as follow-up paper material if pursued.

1. [ ] **Max-Hanson-pop vs peak-inscription-window scaling test.** Hanson's urban-area population estimates appear to be *max theoretical* populations (max settlement footprint × estimated population density per Chapter 4 methodology, Hanson 2016 pp. 49–80), not realised peak populations at a single moment — i.e., an envelope / carrying-capacity measure rather than a temporal snapshot. The preregistered H3a uses cumulative date-window-filtered inscription counts vs Hanson max-pop, which dimensionally pairs envelope-against-envelope. A complementary test would substitute the response with the **highest 25-year or 5-year inscription count** per city (sliding-window max), keeping Hanson max-pop as predictor. This pairs theoretical-max against realised-peak rather than envelope-against-envelope, and would reveal whether the scaling relationship holds when the response is a "peak-rate" measure rather than a "total-production" measure. Implementation notes: (a) only applicable to cities with sufficient N to make a peak-window meaningful — likely the Phase 1 urban-area threshold (~1,600 inscriptions) or a lower exploratory threshold; (b) for fairness, both 25-year and 5-year windows should be tested as a sensitivity; (c) Hanson 2016 catalogue (PDF at `~/Zotero/storage/FGM4PVSX/`) does not include per-city peak dates, so no comparable max-pop-date axis is available — the test is one-sided (variation in the response only). Diagnostic-confirmatory framing: report whether the β scaling exponent under peak-window response differs materially from the preregistered cumulative-count β. **Not preregistered now**; logged here so it isn't lost.

2. [ ] **Reachability-guide extension — cheap (~ 1 day sapphire compute).** Tier 2 of the historian-facing reachability work begun 2026-05-22. The current Phase 1 v2 grid covers three effect-size brackets (20% / 50% / 100%) × two durations (25y / 50y). Fill in 10% / 30% / 70% amplitudes and 15y / 75y / 100y durations to give historians a richer effect-detection envelope. Reuses the existing Phase 1 simulation harness with new bracket-generator calls; no architectural change. Output: refined version of `runs/2026-05-22-reachability-guide/outputs/figures/historian-reachability-heatmap-*.png` plus updated paper subsection at `planning/paper-subsection-reachability.md`.

3. [ ] **Reachability-guide extension — substantive (multi-day sapphire compute).** Tier 3 of the historian-facing reachability work. Produce **per-subset reachability tables** for the project's preregistered subsets (collegia, military diplomas, religious dedications, imperial-titulature, stratified by inscription type, etc.). Each subset has its own aoristic-width distribution and temporal envelope; the reachability profile is therefore subset-specific, not derivable from the empire-level Phase 1 grid by simple N-scaling. Implementation: per-subset Phase 1 runs with the subset's own width distribution as input. Multi-day compute. Output artefact is the methodological-toolkit contribution that makes the paper a reference for future inscription-SPA work — every subsequent researcher with a subset of N inscriptions can consult it before launching an analysis. The collegia subset is the worked example in the current paper-fragment draft.

4. [ ] **Bayesian-method reachability comparison.** A parallel reachability analysis under `baorista` (Crema 2025) Bayesian-aoristic methodology. Bayesian methods have different — possibly more permissive — reachability profiles than the frequentist permutation-envelope test. Complementary to Tier 3; ~ 1 day compute once baorista runs are stable on sapphire (see Decision 3).

5. [ ] **Cumulative-totals Hanson NBR experiment (inscription count and letter count).** Low-priority follow-up to the 2026-05-26 letter-count probe. The probe matches the prereg's date-window-filtered count specification (Decision 22) for comparability with H3a. A separate experiment should aggregate cumulative totals across the full analysis envelope (50 BC – AD 350) — both inscription counts and letter counts — and re-fit the Hanson NBR, to test whether the date-window filter materially changes the scaling exponent versus the simpler envelope-cumulative specification. Cheap (~ <1 day); reuses the same pipeline with the date-window filter removed. Logged here so it isn't lost; no time-pressure.

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
- **Prereg framing of D19 / D21 / D23 / D25 needs amendment** — currently flagged as "Martin-flagged primary" (awaiting-statistician) in `planning/preregistration-draft.md` and `planning/decision-log.md`. Per the 2026-05-26 recalibration (Martin's role reframed to single sanity-check at draft stage), these are project-decided with collaborator sanity-check at draft. Same applies to the 7 Stage-3 design decisions in `planning/stage-3-implementation-plan.md`. Reframe in the next OSF amendment batch.

### Open caveats from the 2026-05-21/22 Phase A + Phase B work

Raised during the talk-prep sensitivities and the Phase 2 recovery-grid launch; not blocking the talk but flagged for follow-up:

- [x] 2026-05-22 **Concurrency slowdown on sapphire — resolved.** Root cause was SMT saturation: 19 workers on a 12-physical-core Ryzen 9 7900 (24 SMT) meant 14 of 19 workers shared SMT siblings, costing ~ 3.2× per-fit time invisible to per-worker CPU% accounting. Cure: `n_jobs=12` + `taskset -c 0-11` pinning to physical cores + `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`. Empirical: 18 s/fit at N=2,000 (was 62 s); 30 s/fit at N=10,000 (was 90 s). Grid wall-clock ~ 100 h → ~ 31.6 h. Full diagnosis in `runs/2026-05-22-recovery-grid-validation/CONCURRENCY-INVESTIGATION.md`; restart log + verification in `RESTART-LOG.md`. **For any future Bayesian / pymc grid on Ryzen-class hardware**: pin to physical cores, set `n_jobs = physical_core_count`, not SMT count. Captured as memory `2026-05-22-018eedaeab88`.
- **`pilot_proxy` tier vector is a proxy, not a real posterior draw.** The (0.55, 0.30, 0.15) "pilot_proxy" entry in the Phase 2 grid's tier-weight library is anchored to Decision 17's endpoint-frequency descriptives (54.5 % `not_before` `01`, 53.0 % `not_after` `00`), not to an actual posterior draw from a pilot fit. Replace with a real posterior draw once a pilot mixture fit becomes available. Flagged transparently in `runs/2026-05-22-recovery-grid-design/spec.md §2.3`.
- **W-1 (Wasserstein-1) flagging threshold and PPC numerical thresholds deferred.** Both need empirical posteriors to anchor; cannot be pinned a priori. The recovery-grid simulation reports W-1 as a supplementary shape metric but does NOT gate on it yet. PPC numerical thresholds will be set after the first real-data Phase 2 fit. Flagged in `runs/2026-05-22-recovery-grid-design/spec.md §6`.
- **Smoke-test R-hat is close to the binding gate.** Smoke-test cell (`shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000` rep 0) had max R-hat 1.0063 vs the prereg-binding gate of < 1.01 (so it passed). The Gaussian-random-walk smoothness prior on `log p_gen` is the slowest-mixing parameter. If cell-wide R-hat pass rate in the full grid dips below the convergence-gate target, the response is **more draws / more tune iterations — not relaxing the gate**. Flagged in `runs/2026-05-22-recovery-grid-validation/SMOKE-TEST.md` §"Convergence".

---

## If context feels cold

1. Read `planning/preregistration-draft.md` start to finish (~10 min).
2. Read `planning/backlog-2026-05-03.md` for what's left to do + caveats (~5 min).
3. Skim Decisions 8 / 9 / 10 in `planning/decision-log.md` for the methodological pivot rationale (~5 min).
4. Skim `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` for current empirical results (~3 min).

That's enough to engage substantively. Deeper context (the scout report, working-notes, amendment trails) reads in another 20-30 min if needed.

---

## Session history — done items (terse)

### 2026-05-26 (letter-count probe complete + recovery-grid launched + "acts vs content" reframe locked)

The session that operationalised the post-Martin recalibration. Opened with a name correction: the 2026-05-25 consultee was **Martin Eftimoski (NOT Drechsler)**; three planning files + the continuity 2026-05-25 session-history block fixed in `f3e5322`, memory `2026-05-26-214ce5ca1491` captures the corrected profile. Then the **letter-count probe** ran six blocks: blocks 1–5 on amd-tower (descriptive + empire-SPA + province/city SPAs with rank shuffles + Hanson NBR + frequentist Mundlak); block 6 the directly-comparable Bayesian Mundlak NBR on sapphire (`21a80c0`, `49957a7`; 4.3 min wall-clock; all three variants PASSed convergence gates). Verdict: Flag 2 (Hanson β) and Flag 3 (f_within +9.89 pp; 30 % → 40 %) both MATERIAL; Flag 1 (SPA shape) MODEST. **Shawn rejected the spec's binary verdict rule mid-probe**: inscription-count and letter-mass are complementary measures of partially-different constructs ("acts vs content"); their delta is a research object in its own right. This was the session's defining methodological move, captured at Obs 58 (`dd326dc`), corroborated empirically by Obs 59 (`de8fa8f`, Mundlak +9.89 pp) and Obs 60 (`2f86c95`, pilot_proxy reign-weight quadruples under letter-weighting — corroboration at the editorial-template-tier layer). The probe REPORT closed task #6 at `348ea25`. The **recovery-grid two-unit re-simulation** spec was drafted (`507a722`) per the new framework — two grids head-to-head (inscription-mass + letter-mass-conservative); harness built and smoke-tested on sapphire (`16c8c88`, `8925126`, `65756ac`); production launched 05:53 UTC at PID 931910 with ETA ~76 h sequential (Friday AEST). Working-notes batch intake landed the 9 pending proposed Obs 49–57 (`43d814d..65edb2e`) plus cleanup of the staging file. HMM follow-up paper stub created at `planning/hmm-paper-stub/` (`dad1fcd`). Two memories captured beyond the name fix: `2026-05-26-40ce5927fddc` (amendment-gate rule — flag before launching work whose published claims require a not-yet-lodged OSF amendment). ~22 commits this session; all pushed.

### 2026-05-25 (Martin consultation prep)

Day of the Martin Eftimoski consultation. Pre-meeting work: composed `runs/2026-05-25-martin-consultation-prep/BRIEFING.md` (main briefing, 7 sections) and `BRIEFING-supplementary-issues.md` (covers the 8 unanswered 2026-05-17 pack questions + 3 new findings + H3b/H3c/§5/strategic decisions). Produced 4 key figures: uncorrected SPA, slab-highlighting SPA (new; stacked-by-family), slab-excluding SPA (new; reweighted-prior overlay), Hanson NBR scaling. Discovered along the way: AD 300-350 is 80 % editorial templates by aoristic mass — the late corpus is even more template-dominated than the AD 1-300 body. Then two scouts: `/lit-scout-iterate` for pottery-aoristic Roman bibliography (25 references, Brughmans / Aarhus / OXREP / ICRATES cluster; verifier-PASS after one iteration; 15 staged to Zotero, 8 already in libraries, 2 OXREP chapters required hand-curation from OpenAlex + Semantic Scholar because CrossRef returned 404 on `acprof:oso` DOIs); then `/prior-art-scout-iterate` for ceramics-aoristic actionable techniques (15 candidates; verifier-PASS after one iteration on a single DOI-confabulation correction; identified 6 directly-adoptable + 4 to-adapt; methodological-novelty claim sharpened to "structural mixture decomposition is novel; ceramicists use sensitivity stratification"). All action items folded into the post-Martin section above. Commits: `55e050c` (consultation briefing + figures), `dbae06f` (supplementary briefing), `3e93660` (lit-scout), `b687ed2` (OXREP bib hand-curation), `6877621` (prior-art scout).

### 2026-05-24 (alpha-bias diagnostic + family classifier + empirical-Bayes Stages 1+2)

The most methodologically rich day of the project. Started with the recovery-grid FAIL verdict (40.9 % of cells pass both binding criteria — committed `3df0d2c` after the 12-cell retry resolved the /tmp inode catastrophe). Diagnostic investigation Experiments A + B (`3d23fe6`) traced the failure to a structural likelihood ridge between α and shape complexity that biases α toward the middle of its range. Three follow-up investigations ruled out two cheap fixes and banked a free win: F0 (systematics across all 450 cells: bias begins at α=0.30 not α=0.95 as initially thought; regnal_cluster shows bidirectional bias); F1 (sharper α prior Beta(1,1) → Δα +0.025; not prior-pull); F3 (non-centred GRW reparameterisation → Δα +0.001 but ESS gain of 45-50× — adopt unconditionally) (`e21f7bf`). Date-range threshold analysis revealed slab structure: 99/49/24/199 are the dominant editorial-template widths; F1+F3 round-number-and-periodic families together account for 65 % of corpus; produced family classifier on `(not_before, not_after)` interval structure (`6734ef0`). Type-bias finding (epitaph is 56 % of corpus but only 18 % of narrow-dated subset) prompted post-stratification reweighting design. Discard-vs-recover rationale documented (`ce140d1`) — explicit decision-tree branching on recovery-grid verdict. Empirical-Bayes Stage 1 (`a37261b`): F1+F3 inscriptions yield empirical p_conv; replaces the placeholder template-dictionary from prereg §3 line 202. Stage 2 (`8e1897b`): Cohort B (Tight ∪ F2_Other, 31,841 records) gives well-constrained empirical p_gen prior with bootstrap-derived per-bin sigma_prior (median 0.044). Stage 3 implementation plan drafted by agent (`381c303`) — 12 sections, 5,700 words, 7 design decisions flagged for Martin. Martin consultation pack (`e57dc6b`) + four planning explainers in plain-language register (`b78da5c`). Memory captured: "default to non-specialist register for stats explanations to Shawn" (saved 2026-05-24-e6ec8f9174f1).

### 2026-05-23 (grid retry + concurrency-investigation handoff)

Picked up the 2026-05-22 grid restart on sapphire (PID 659564, projected ~ 31.6 h wall). At 08:09 UTC: 363/450 done + 12 in-flight + **12 failed**. Root cause of failures: tmpfs `/tmp` on sapphire hit its 1,048,576-inode ceiling during the alpha=0.30 smooth_decline cells; pytensor's `NamedTemporaryFile` outputs accumulated faster than they were cleaned. All 12 failures returned `OSError: [Errno 28] No space left on device`. Grid completed cleanly at 12:07 UTC (29.84 h wall — beating the 31.6 h projection by 5 %). Retry plan: clean `/tmp` (1,048,559 → 17 inodes used; 5.7 s); redirect TMPDIR to a disk-backed location (`~/cc-scratch/inscriptions-recovery-grid/pytensor-tmp/`); relaunch — 51 min wall, 450/450 complete, 0 failed (`3df0d2c`). Summariser run revealed the FAIL verdict (40.9 % pass-both), kicking off the 2026-05-24 diagnostic chain. The TMPDIR-redirect pattern saved us during the retry: 23,264 pytensor temp files accumulated harmlessly on disk vs the 1M tmpfs limit. Worth Obs (queued in working-notes review).

### 2026-05-22 (talk-day session — deck rewrite + grid restart)

Final deck-prep session ahead of Adela's 14:20 Friday delivery at TRAC7 Aarhus. Substantive narrative reframe responding to Adela's per-slide feedback (less stats detail; more historical implications; undergrad-history-major level). Main path went to **9 main (1, 2, 3a, 3b, 4, 5, 6, 7, 7a, 8, 9) + 13 backup B + 9 G** with slide-6 merging the old 6a (NBR comparator) and 6b (Mundlak) into a single "What we found" punchline (the 30 % within-province partition), demoting frequentist NBR to B12; slide-7a promoting Adela's wife/daughter corpus as a worked example. New `fig-06-variance-partition.png` (clean 30/70 stacked bar with six-factor categorisation: habit · economic · social · political · cultural · survival) replaces a four-panel posterior summary as the slide-6 hero. Five other figures had baked-in matplotlib titles cropped (`*.original.png` backups preserved). Speaker notes converted to `::: notes` divs (so reveal.js speaker view picks them up) then rewritten as glance-friendly bullets. Four delivery artefacts produced: `inscription-spa-slides.{pdf,html}`, `inscription-spa-script.{md,pdf}` (~ 1,900 spoken words, ~ 12.7 min), `inscription-spa-notes.{md,pdf}` (standalone bullet reference). Parallel track: the Phase-2 mixture-recovery grid on sapphire was killed and restarted under an optimised SMT-aware config after a background investigation diagnosed SMT saturation as the slowdown cause. Empirical post-restart timings match prediction; wall-clock projection went from ~ 100 h to ~ 31.6 h. Three background agents used (investigation, restart, speaker-notes QA); all returned clean. Final renamed-deck artefact set is `inscription-spa-*` (replacing the legacy `slide-outline.*`).

- Commits: `854d196` (feedback + planning) · `47ff7ce` (deck rewrite + figures) · `80f3805` (re-render) · `4a54cc3` (script + notes) · `8626726` (archive stale paper-format PDF) · `cb32234` (grid investigation + restart log) · `f4318cc` (data-profile smoke)
- Reports: `runs/2026-05-22-recovery-grid-validation/CONCURRENCY-INVESTIGATION.md` · `RESTART-LOG.md` · `planning/conference-talk-rac-trac-2026/qa-report-2026-05-22.md`
- Memories captured (5): `2026-05-22-018eedaeab88` (SMT saturation gotcha), `…-96af8f645552` (matplotlib title bake-in gotcha), `…-48f6cf79bd4f` (time-pressure feedback), `…-81c83b4699bb` (hardware-name scrubbing feedback), `…-bbda749c90b1` (minimalism principle feedback)
- User observation: Obs 5 (visual-scan verification is the only real review for visual deliverables — three new data points in one session)
- Concurrency-slowdown caveat from 2026-05-21/22 — **resolved**

### 2026-05-20 / 2026-05-21 (OSF lodgement + conference-talk planning)

- **OSF lodgement.** Preregistration lodged at `https://osf.io/uycs6/` (embargoed pending double-blind submission decision); supplementary upload PDF deposited. Repository tagged at lodgement state: `osf-lodgement-2026-05-20` → commit `a2e40fd`. Tag moved four times across the day as PDF rendering bugs surfaced and were fixed.
- **Pre-lodgement fixes** to `planning/preregistration-draft.md` and the OSF supplementary upload (`planning/osf-supplementary-2026-05-20.md`, `.pdf`): radiocarbon-SPA framing (Rick 1987 → Williams 2012 → Timpson et al. 2014 → Crema & Bevan 2021); empirically-grounded 5-year-bin rationale (Antonine probe FWHM constraint); LIRE v3.0 DOI corrected from v2.3's `8147298` to v3.0's `8431452` (Obs 44); duplicate DOI bug in §8 Data line found and fixed; pipe-in-table-cell bug fixed across both files (Obs 43); §12 References list built (21 entries; APA-7-ish; Mundlak 1978 included as eponym-source).
- **OSF supplementary** built as a separate clean upload artefact (498 lines): YAML / Field-1 / Field-2 stripped; Field 3 → §1; Field-4 subsections § 1–12 → §2–13; 42 internal cross-references renumbered (+1); paper-internal Heřmánková §29/§45/§60 references correctly preserved.
- **PDF generation v1 → v4** via pandoc 3.6.3 + xelatex: v1 (1in margins, default mono); v2 (pipe-cell fix + 0.8in margins + mono Scale=0.78 to fit ASCII flowchart + H3a NBR formula); v3 (`xurl` package — ineffective alone); v4 (`xurl` + pandoc `-f markdown+autolink_bare_uris` — both required, see Obs 42). 32 pages letter-size, all URLs wrap, all tables intact.
- **Adversarial verifier** dispatched after PDF v2 produced — caught the pipe-in-cell H3c(i) truncation bug that author-side review had missed (Obs 45). Verifier verdict: PARTIAL → PASS after fix.
- **Tertiary analysis logged** in continuity: max-Hanson-pop vs peak-inscription-window scaling test. Hanson's populations are max-theoretical (footprint × density), not realised peak; envelope-vs-envelope rather than max-vs-max. Logged as a post-lodgement future-work amendment candidate.
- **Conference talk planning** (overnight, externalised). New directory `planning/conference-talk-rac-trac-2026/`:
  - `conference-context.md` (briefing from scout): RAC/TRAC 2026 Aarhus, Thu 21 – Sat 23 May 2026; **session TRAC7 "Beyond names and numbers: Quantitative epigraphy and the discovery of historical patterns"** organised by Heřmánková, Glomb, Kaše (the SDAM / LIRE creators); **Shawn's paper slot Friday 22 May 14:20 room Preben Hornung**; 20-min standard slot; adjacent talks Sommerschield (Aeneas; 14:00) and Bennett (15:00).
  - `asset-inventory.md`: 2024 exploratory notebook (`archive/2026-04-22-inscriptions-spa.ipynb`) is the goldmine — empire / province / city SPAs + frequentist Hanson NBR-with-bootstrap already implemented; main work for next session is applying the prereg date-window filter and re-rendering at slide aspect.
  - `slide-outline.qmd`: 7-slide Quarto revealjs skeleton + speaker notes (HTML comments).
  - `analysis-roadmap.md`: 36-hour hour-by-hour plan with decision gates at hour 18 (A+ go/no-go) and hour 26 (Bayesian H3a stretch go/no-go).
  - `talking-points-feedback.md`: 7 anticipated objections + prepared responses + 5 feedback prompts (one specifically inviting Sommerschield engagement).
- **Speaker question resolved 2026-05-21**: **Adela is reading the paper on Shawn's behalf** at the 14:20 Friday slot. Shawn cannot travel; remote presentation not supported. Adela also has her own separate paper at 12:20 (Roman marriage ages).
- **OSF URL folded** across artefacts: prereg §11 Provenance (post-lodgement amendment trail); slide deck footer + slides 5 / 7; project `README.md` (previously empty; now a proper landing page).
- **Commits + push** across the two days: pre-lodgement (`feae7c5` → `a2e40fd`, ~10 focused commits); overnight planning `83574a8`; resolved-question `003393c`; working-notes Obs 42–45 + this entry pending.

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
