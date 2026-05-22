---
priority: 5
scope: always
title: "Session Log"
audience: "researchers and future instances"
---

# Session Log — inscriptions

Factual record of what was done, decided, and produced each session.
Summarises; does not reflect — that's `session-reflection.md`.

Close each entry with a brief **Contextual assumptions** note where
non-obvious: decisions made under time pressure, tool/API constraints
that shaped approach, external dependencies that influenced choices.
Skip when context is self-evident.

*Entries appended by `/reflect`.*

---

## 2026-04-22 → 2026-04-23 — Entry 1

Continuous session, single session ID. Spanning ~14 hours across two calendar days.

**Done**

- Set up project scaffolding: `docs/notes/reflections/`, `planning/decision-log.md`, `planning/future-studies.md`, `planning/ai-contributions.md`, `planning/paper-outlines/`, `planning/memos/`.
- Verified bibliography (25 rows) + BibTeX for primary lit-scout chain (SDAM/Crema/Hanson cluster). Commit range through `2af64e4`.
- Supplementary lit-scout on Aeneas / ML-for-inscriptions (15 rows). Commit `2abdc83`.
- Installed `uv` on amd-tower; `uv init` + project venv with pandas, numpy, scipy, pyarrow, statsmodels, joblib. `pyproject.toml` + `uv.lock` committed (`6639fd5`).
- SSH-set up sapphire: uv installed, inscriptions repo cloned, `uv sync` reproduced the locked environment.
- Restored personal-assistant venv to pre-session state (uninstalled the 6 packages the first run added).
- Ran `data-profile-scout` (proposer) in comprehensive mode on sapphire: 5.64 min runtime, 1,305 claims, commit `32760ea`. Aoristic null, Westfall-Young stepdown with Holm-Bonferroni companion, BCa bootstrap (percentile fallback for n < 50), 20k resamples, joblib parallelism, assumption-check discipline in decisions.md.
- Ran `data-profile-verifier` on sapphire: PARTIAL verdict, 1303/1330 pass, 27 major corrections (none critical). Commit `8e64a21`. Method-as-implemented checks all pass.
- Committed planning state-of-play: Decision 7 (paper architecture), future-studies (FS-0/1/2), ai-contributions, Aeneas-partition outline, backlog update. Commit `3d61929`.
- Captured Obs 11 in working-notes: editorial-convention hierarchy hypothesis + Thursday test plan + post-LIST extension. Commit `78b2c0c`.
- Continuity message written. Commit `a72446c`.
- Reflection documents updated (this commit pending).

**Decided**

- Decision 7: main SPA paper deconvolution architecture — explicit deconvolution mixture as primary correction; thresholded SPAs as in-body robustness; stratified SPAs (convention vs precision) in appendix; baorista Bayesian (Crema 2025) run properly on a subset, reported in appendix as comparative methodology. Scope-commitment deadline end of Week 1 of paper sprint (Sunday 2026-05-03).
- OSF (not Zenodo, not AsPredicted) for preregistration deposits. Confirmatory/exploratory split adopted per Shawn's map-reader-llm precedent. Current rerun framed as exploratory; preregistration reserved for Friday's min-thresholds simulation and for Week-1-to-3 SPA analyses.
- Statistical-methodology review produced four refinements to the first-run plan (all applied before rerun): aoristic-probability null (Ratcliffe/Crema) replacing two-stage uniform; Westfall-Young permutation-based stepdown replacing Holm-Bonferroni as primary correction; required assumption-check discipline in `decisions.md`; stochastic-claim fields (`random_seed`, `resamples`, `method_parameters`, `code_location`) added to `claims.jsonl` schema.
- Thresholds for subset-qualification: `[10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]` applied to province, urban-area, and bivariate province × urban-area levels. Matches archival working set.
- Project venv tooling: `uv` + `pyproject.toml` + `uv.lock` (FAIR4RS-aligned lockfile reproducibility).

**Produced**

- `runs/2026-04-23-descriptive-stats/` complete research record: spec, seed, agents.md, briefs, RO-Crate metadata, code (profile.py + verify.py), outputs (15 markdown files + 60 CSV tables + claims.jsonl with 1,305 claims + corrections.md + verdict.md + decisions.md with 14 entries), run.log and verifier.log.
- Two new verified bibliographies (primary + Aeneas-cluster) totalling 40 rows + BibTeX.
- Six new planning documents: decision-log, future-studies, ai-contributions, backlog, paper-outline for Aeneas-partition, memo on `/reflect` multi-invocation safety.
- Five reflection documents including this one and the continuity message.
- One new `[PATTERN]` working-notes observation (Obs 11, editorial-convention hierarchy) plus one captured earlier in the session (Obs 10, computational-sibling seeding).

**Contextual assumptions**

- `uv` chosen over `pip + requirements.txt` on FAIR4RS + modern-Python-convergence grounds; Shawn may not have encountered `uv` before today but accepted the recommendation.
- Sapphire workdir path `~/Code/inscriptions` (not `~/inscriptions`) — a path-typo in the first agent brief caused a stall; paths corrected throughout before re-run.
- Comprehensive-mode profile ran on sapphire not amd-tower per the "CRITICAL — run all compute-intensive analysis on sapphire" rule from scratchpad; 5.64 min runtime means local execution would have been viable, but the rule was observed regardless.
- First-run outputs in `runs/2026-04-23-descriptive-stats/outputs/` were overwritten by the rerun; first-run state preserved only in git history at commit `f254c4f`.
- Two first-run output artefacts (`profile_lire_v30.py`, stale `corrections.md`/`verdict.md`/`verifier.log`) were overwritten or superseded; no explicit cleanup commit separating the two runs.

---

## 2026-04-23 → 2026-04-24 — Entry 2

Continuous session straddling the day change (Sydney local); same session ID. Shawn went AFK for ~6 hours mid-session; autonomous agent-coordinated work completed before his return. 22 commits on `main`.

**Done**

- Memory captured: agent-session-capture infrastructure operational — `category:openness`, id `2026-04-24-666890d8ab53`, tags: `agent-infrastructure` (new), `research-record`, `open-science`, `context-management`.
- Hanson 2021 β verified from local PDF (Zotero `GHPTNHBI` / `9Z7EFZVA` duplicates). Authoritative values from Table 7.3, p. 146: **β = 0.672 mean** (95 % CI [0.588, 0.756]) / **β = 0.654 median** ([0.514, 0.774]); OLS log-log on 8 equally-sized population bins; n = 554 Empire cities with ≥ 1 inscription out of 593 total; EDCS corpus; Rome excluded as extreme outlier; R² = 0.976 (mean) / 0.950 (median). Verbatim "infrastructure for information" framing at pp. 139–140, 147. Provincial-capital mean residual = 0.43 vs ~ 0.06 for *coloniae*/*municipia* (p. 148). Moran's I for residuals = 0.046, z = 4.571, *p* < 0.0001 (Table 7.4); inscriptions raw-counts Moran's I = −0.006 (random). ArcGIS Spatial Autocorrelation tool used (p. 145); weights construction not specified in paper. Commit `d01a702`.
- Corrected Scout 2 misattribution: β ≈ 0.643 via Brewminate reconstruction was for HOL 2017, but HOL 2017 measures functional diversity vs population (β = 0.686, SE 0.078), not inscription count directly. Commit `d01a702`.
- Information-infrastructure framing demoted from "complementary" to "alternative" per editorial decision for RAC-TRAC 2026 conference paper — complexity-markers primary, information-infrastructure as brief alternative, audience response informs final journal version. Commit `3e4a6f4`.
- Obs 12 captured in `working-notes.md`: Turchin et al. 2018 "single latent dimension" of cultural complexity operates at polity × century scale (PCA on 9 complexity characteristics from 414 Seshat polities, PC1 ≈ 77 % variance); not a direct rebuttal of this paper's multi-factor decomposition which operates at city/province × decadal scale. Three-sentence discussion-section treatment agreed. Commit `50360ab`.
- Zotero infrastructure: `.env` template + `.gitignore` hardening (commits `0138972`, `4534584`); SDAM group write-access verified via `pyzotero.zotero.Zotero('2366083', 'group', API_KEY).key_info()`. Target collection: `PZN5ATJK` (SPA, 37 pre-existing items).
- Batch-add of 23 curated papers to SDAM SPA collection via `scripts/zotero_batch_add.py`: 21 new items created + 1 duplicate (Carleton 2018, both `T95BHV43` and `GF82TVAB`, awaiting manual merge) + 2 skipped as no-DOI. 7 PDFs attached via magic-byte-verified download; 3 PDFs failed to Cloudflare bot-detection (Ortman-Lobo 2024, Bevan 2017, Carleton-Groucutt 2020). Commits `e26278e` (script), `f820afb` (log).
- Follow-up pass (`scripts/zotero_followup.py`): added 2 no-DOI items manually (Beltrán Lloris 2015 OHRE chapter `5P6SIHDP`; Benefiel & Keesling 2024 Brill volume `FATTZZ4X`); retried 4 PDFs via Unpaywall with browser User-Agent; 2 additional PDFs attached (Ortman-Lobo 2024 `K9NHZPDT`, Glomb 2022 `PMVKIVN8`); 2 genuinely unavailable (Bevan 2017 PMC bot-blocked; Carleton-Groucutt 2020 no OA copy per Unpaywall). Commits `0822157`, `6e8355b`.
- `planning/preregistration-draft.md` drafted: monolithic open-ended OSF format covering H1 (min-thresholds simulation) + H2 (mixture-model validation) + H3a/b/c (population signal). ~250 lines; four fields (Title, Description, RQs / Hypotheses, Additional Information); 6 TBD markers. Commit `7ae3e93`.
- **TBD walkthrough** — all four 2026-04-24-actionable TBDs resolved; TBD 5 and TBD 6 deferred by design:
  - **TBD 1** (H1 simulation protocol knobs): urban-area sweep {25, 50, 100, 250, 500, 1000, 2500}; province sweep extended to include 25,000; 1,000 iterations per cell; exponential null primary + continuous piecewise-linear secondary; detection-rate curves at 0.70 / 0.80 / 0.90; Antonine-anchored target **dropped** per Glomb re-read (see below); effect-shape smooth Gaussian-tapered dip matching each Decision 5 bracket. Commits `228a8c6`, `c901aae`.
  - **TBD 2** (Bayesian NBR software): **pymc primary** + `scripts/h3a_brms_shadow.R` secondary cross-validation shadow (~50-line R stub) for R-native co-author legibility. Carleton et al. 2025's provincial random effects consumed as data (not code) per the Q3 translator-triangulation strategy. Commit `630fdc4`.
  - **TBD 3** (priors + PPCs): β ~ Normal(0, 2.5) agnostic; α_0 ~ Normal(0, 5); σ_prov ~ HalfNormal(1); 1/alpha ~ HalfNormal(1). PPC suite per Gelman, Vehtari, Simpson, Betancourt et al. 2020 Bayesian Workflow: density overlay + test statistics (zero-count, mean, SD, 95th percentile, mean-variance ratio) + Pearson-residual structure. Commit `f18db5b`.
  - **TBD 4** (Moran's I spatial weights): k-NN k = 8 primary via `libpysal.weights.KNN`, row-standardised; k = 5 and k = 10 sensitivity; Hanson 2021's weights construction unspecified in paper, so qualitative replication target only (≥ 2 of 3 k values significant + map-pattern match). Commit `378e708`.
- Glomb, Kaše & Heřmánková (2022) PDF re-read via Explore agent (`a7d8aa16d878e56a1`). **Finding**: the paper is a null for Asclepius-cult inscriptions around the Antonine Plague (N = 210, KS = 0.11, *p* = 0.20), not the detected-signal template the Scout 3 framing implied. Required dropping the Antonine-anchored H1 target and reframing the Antonine H3b test as exploratory replication-of-Glomb. Preregistration reframed at commit `c901aae`. Captured as abductive-reasoning Entry 3.
- LIRE subset-filter feasibility confirmed on disk (`archive/data-2026-04-22/LIRE_v3-0.parquet`, 182,853 × 63 columns): military diplomas 285 / 442 / 494 rows via `type_of_inscription_clean` / `_auto` / `inscr_type` respectively; Asclepius-cult 358 rows via inscription text regex `[Aa]esculap|[Aa]sclep` (vs Glomb et al.'s stricter N = 210). Noted in preregistration §9 at commit `c901aae`.
- Canonical living continuity doc created: `docs/notes/reflections/continuity.md`. Replaces dated per-session continuity notes with a single cross-session tracker structured around priority queues (pre-prereg submission; pre-paper-sprint-Week-1; standing open items) plus session history. `continuity-2026-04-23.md` preserved as historical snapshot. Commit `e19348d`.
- Reflection documents updated (this commit pending).

**Decided**

- Preregistration scope: **monolithic, OSF open-ended format**, mirroring map-reader-llm precedent. Covers H1 + H2 + H3.
- Glomb (2022) role in preregistration: **motivating prior, not effect-size template**. H1's Antonine-anchored privileged target dropped; H3b's Antonine-specific test reframed as preregistered exploratory replication of Glomb + Duncan-Jones.
- Information-infrastructure framing: **alternative interpretation** for the conference paper, not co-equal with complexity-markers. Audience response informs whether it survives into the journal version.
- Bayesian NBR implementation: **pymc primary + brms shadow** (`scripts/h3a_brms_shadow.R` to be written as ~50-line stub, not on the OSF critical path).
- β prior: **agnostic Normal(0, 2.5)** (not literature-informed), explicitly to avoid the appearance of loading the dice toward the ~0.5 sublinear literature value.
- Spatial weights for Moran's I: **k-NN k = 8 primary, k = 5 / 10 sensitivity**, qualitative Hanson-replication target (not numerical match — his weights construction unspecified in paper).
- Continuity doc discipline: **single living `continuity.md` per project**, updated at each session's `/reflect`; dated snapshots are historical only, not maintained.
- Anti-confabulation rule explicitly added to global CLAUDE.md mid-session: re-verify specific numbers / paths / identifiers from source before citing, treat prior context as pointer-not-authority.

**Produced**

- 22 commits on `main` (enumerated above).
- 23 new items in SDAM Zotero group library SPA collection: 21 via batch-add + 2 via follow-up manual add. 9 PDFs attached automatically (batch-add) + 2 via follow-up Unpaywall retry = 11 PDFs. 1 duplicate awaiting manual merge. 2 items (Bevan 2017, Carleton-Groucutt 2020) have metadata but no PDF pending manual retrieval via Zotero Connector in a browser.
- 2 new Python scripts: `scripts/zotero_batch_add.py` (with `_build_doi_index` idempotency fix) and `scripts/zotero_followup.py` (with Europe PMC fallback and corrected pyzotero attachment-return parsing).
- 1 new canonical reflection doc (`continuity.md`, 154 lines) + 1 historical-snapshot preservation (`continuity-2026-04-23.md` untouched).
- 1 memory record (`2026-04-24-666890d8ab53`, category `openness`).
- Updated reflection docs: Obs 12 (Turchin), Obs 13 (four-way sublinear convergence), Obs 14 (Zotero FTS gotcha) in `working-notes.md`; abductive-reasoning Entries 3 and 4; reasoning-log Entry 3; session-reflection Entry 2; this session-log Entry 2.

**Contextual assumptions**

- Session started when system clock reported 2026-04-23; transitioned to 2026-04-24 mid-session. Calendar-day references in early commit messages may appear inconsistent with commit timestamps; this is expected.
- Shawn went AFK for a ~6-hour stretch mid-session, returned with decisions already needed; the autonomous-agent-coordination block (Explore paper-find agent + general-purpose Zotero batch-add agent, both in background) was authorised implicitly by the earlier "use agents more liberally, the research record is captured" framing rather than by per-agent approval. This is consistent with the agent-session-capture memory captured at the start of the AFK block.
- `scripts/h3a_brms_shadow.R` committed to be written but **does not yet exist**. The brms-shadow decision was made before the script. Creation of the shadow is on the pre-submission priority queue.
- The preregistration draft has not been end-to-end coherence-reviewed after the piecewise TBD edits. Coherence pass is on the pre-submission priority queue before Adela review.
- Anti-confabulation rule landed in global CLAUDE.md mid-session; reflection-doc entries honour it by re-checking commit hashes via `git log` and PDF values via direct `Read` rather than citing from memory alone.

---

## 2026-05-03 → 2026-05-04 — Entry 3

Operational session (install + cleanup + handoff for travel) bridging two calendar days. Same instance throughout; no compaction. ~10 commits on `main`. Three machines (amd-tower / sapphire / zbook) brought into three-way sync at HEAD `3256744`.

**Done**

- baorista install plan generated by background Plan agent: `planning/baorista-install-plan.md` (commit `507c0c8`, 464 lines). Stage 0 reconnaissance recorded sapphire's pre-install state (Ubuntu 25.04, 24 cores, 60 GiB RAM, g++ 14.2.0, R/cmdstan/NIMBLE/baorista/brms/cmdstanr all absent).
- baorista install executed across all 5 stages: PyMC + cmdstanpy + cmdstan compiled (Stage 0), R 4.4.3 + gfortran + 4 dev headers via Shawn's manual sudo (Stage 1), cmdstanr 0.9.0 + nimble 1.4.2 + baorista 0.2.1 + brms 2.23.0 + arrow 24.0.0 + posterior 1.7.0 + bayesplot 1.15.0 + loo 2.9.0 (Stage 2), Track 2 brms shadow parse-check (Stage 3), three smoke-test tiers passing at n=100 / 500 / 5,000 (Stage 4). Final commit `c97d218`. Reproducibility re-pass added user-library bootstrap fix (commit `bf0d661`).
- Three-machine sync: zbook pulled from 94 commits behind to current HEAD; `uv sync` created the project venv on zbook with pymc 5.28.5 + cmdstanpy 1.3.0 + scientific stack. amd-tower already current. sapphire current.
- Sapphire git-state cleanup: removed 23 MB stale archive, ~5 MB duplicate-of-origin output dirs, byte-identical `pyproject.toml`/`uv.lock` mods. Preserved 119 MB `cell-results.parquet` + 21 MB `install.log` via temporary archive-and-restore. Sapphire now at clean working tree, HEAD `3256744`.
- `.gitignore` pattern broadened: `runs/**/cell-results.parquet` (was `runs/**/outputs/cell-results.parquet`) to match H1 v2's `outputs/h1-v2/cell-results.parquet` nesting. Commit `3256744`.
- `planning/backlog-2026-05-03.md` created (commit `8f25d0f`). Supersedes `backlog-2026-04-22.md` as the working backlog. Three sections: NOT YET IMPLEMENTED (preregistered Phase 2 / Phase 3 work), open caveats, standing rules + failure modes (duplicated from continuity for self-contained use).
- `docs/notes/reflections/continuity.md` updated: research-state snapshot bumped to 2026-05-03; priority queue restructured to Phase 2 substantive work (post-OSF lock); Done section extended through 2026-05-04 baorista install. baorista API gotchas + sapphire fresh-R user-library bootstrap added to failure modes.
- Smoke-test API discovery sequence captured in `runs/2026-05-03-baorista-install/INSTALL-LOG.md` §"baorista API discoveries (preserved for the project's main pipeline)". Five gotchas documented: timeRange descending; `(upper - lower + 1) %% resolution == 0` required; per-event col1 > col2 by numeric value (not column name); event must satisfy `lower <= col2 <= col1 <= upper`; `expfit` returns S3 `fittedExp` with `$rhat` / `$ess` directly, no `$samples` slot.
- Reflection docs updated this session-end: session-reflection Entry 3, abductive-reasoning Entry 5 (gitclean-on-untracked-dir gotcha), working-notes Obs 31 + Obs 32, this session-log Entry 3.

**Decided**

- baorista install proceeds before OSF lock (Shawn 2026-05-03): pure infrastructure, no methodological coupling, install outcome is preregistered-compatible either way (Decision 3 fallback in place). Net upside: working baorista when prereg locks.
- Smoke-test ceiling at n=5,000 (n=50,000 deferred to FS-4 timing study): linear extrapolation suggests <60 s at niter=4000 / 5–25 min at default niter=100,000, retiring the `[VERIFY]`-flagged "could take days" worry.
- PyMC pre-installed defensively on sapphire (Shawn directive): Decision 3 fallback path is "free" if NIMBLE compile failed. NIMBLE compiled cleanly first try; fallback didn't fire, but the pre-install retains value for FS-4 follow-up Python-native ICAR work.
- Sapphire git state cleanup approach: `git clean -fd` after preserving gitignored artefacts to a sapphire-local archive directory. Discard byte-identical `pyproject.toml` / `uv.lock` local mods. Commit-and-push gitignore pattern broadening separately.
- `planning/backlog-2026-04-22.md` kept as historical record, not updated in place. New `planning/backlog-2026-05-03.md` is the live working backlog. Same supersession pattern as `continuity-2026-04-23.md` → `continuity.md` in April.

**Produced**

- ~10 commits on `main`: `507c0c8` (install plan), `066f25d` (PyMC + cmdstanpy deps), `9d72aae` (PARTIAL state pre-Stage-1), `a41f394` (smoke-test BP-conversion fix), `c97d218` (PASS final), `bf0d661` (user-library bootstrap fix), `8f25d0f` (backlog-2026-05-03 + continuity update), `3256744` (gitignore pattern broadening).
- New planning doc: `planning/baorista-install-plan.md` (464 lines).
- New install record: `runs/2026-05-03-baorista-install/INSTALL-LOG.md` (covers all 5 stages, API discoveries, 3 iterations of smoke-test debugging).
- New working backlog: `planning/backlog-2026-05-03.md` (206 lines).
- Updated continuity: `docs/notes/reflections/continuity.md` (now the canonical living tracker through 2026-05-04).
- Updated reflection docs: this session-log Entry 3 + session-reflection Entry 3 + abductive-reasoning Entry 5 + working-notes Obs 31 + Obs 32.
- Sapphire-local archive at `~/h1-v2-raw-archive/` (created and removed after restoring artefacts).
- Three-machine sync: amd-tower / sapphire / zbook all at HEAD `3256744`, all working trees clean.

**Contextual assumptions**

- Session started 2026-05-03 afternoon (local) with the explicit motivation that Shawn had a week of travel coming up; the operational goal was a clean three-machine state that supports prereg-only work from any machine without further setup. The cumulative result (zbook fully synced + working baorista on sapphire + clean working trees + new backlog + updated continuity) is calibrated to that goal, not to a maximally-substantive Phase 2 / Phase 3 push.
- Stage 1 of the baorista install required interactive sudo on sapphire (apt install). The agent halted cleanly and Shawn ran the sudo apt commands himself (~3 minutes); the resume agent then took it from there. This is the documented `Do NOT bypass sudo` constraint working as intended.
- baorista's smoke test went through three iterations to converge: (i) calendar dates direct → API rejected timeRange ordering, (ii) BP conversion + clamp + zero-width nudge → API rejected at-boundary edge cases, (iii) widths capped at 100y + centres inset by half-width → PASS. Iterations 1 and 2 surfaced real API gotchas; iteration 3 was a smoke-test simplification (cap widths) that's documented as a re-validation requirement before any production baorista run on real LIRE data.
- The previous-agent monitor-and-exit pattern (documented at working-notes Obs 27) recurred twice this session — the resume agent set up monitors and exited prematurely once during Stage 2, and the smoke-execution agent did the same during Stage 4. The pattern was caught both times by main-thread Bash background polling on PID death; no work was lost. But it's evidence that the failure-mode list documented in continuity.md isn't yet fully reaching the agent briefs I generate: the briefs this session still nudged toward Monitor for "wait for PID death" patterns rather than `until ! kill -0 PID`.
- The `git clean -fd` near-miss (almost deleted 119 MB gitignored cell-results.parquet inside an untracked dir) was caught by reading the dry-run output carefully and recognising that the about-to-be-removed directory contained the precious gitignored file. The fix was to move the gitignored artefacts to a sapphire-local archive before running clean. Recorded as abductive-reasoning Entry 5 + working-notes Obs 31 + a continuity.md failure-modes line. The lesson is procedural: dry-run is non-optional, and dry-run alone isn't sufficient — must enumerate the contents of any untracked directories the dry-run flags.
- `cell-results.parquet` location was the immediate driver of the gitignore pattern broadening: the H1 v2 layout placed the parquet at `runs/.../outputs/h1-v2/cell-results.parquet` (extra `h1-v2/` dir vs the v1 layout that the original gitignore pattern matched). Pattern updated from `runs/**/outputs/cell-results.parquet` to `runs/**/cell-results.parquet`. Same change applied to `run.pid`. The fix is now in origin and pulled to all three machines.

---

## Entry 4 — 2026-05-14 → 2026-05-17: adversarial-review-driven preregistration revision and pre-lodgement audit

Multi-day session spanning four calendar days under a single Opus 4.7 (1M-context) instance. Continuous; no compaction. Working from the post-editorial-pass preregistration baseline (commit `eced14c`, 2026-05-14) through to the post-ChatGPT-review committed state (commit `6862031`, 2026-05-17).

**Done**

- **Dual fresh-context adversarial review of the preregistration** (2026-05-14). Two parallel Opus 4.7 Explore agents — one with statistical-methodology focus, one with domain legibility / output-value focus. Both applied a shared seven-point prereg-failure-mode rubric. Both concluded "not yet lodgeable, all fixable." Surfaced 6 consensus blocking findings plus several serious single-agent findings.
- **Triage of findings into four buckets** (2026-05-15). (a) Superseded by Decisions 12–17; (b) statistician questions for Martin's consultation; (c) eleven smaller calls needing Shawn's input; (d) ~ 20 mechanical / clarity fixes.
- **Bucket (c) worked through one-at-a-time with Shawn** (2026-05-15). All eleven items resolved: H2.2 neighbourhood definition (±25 y excluding midpoint + bracketing variants); H3c qualitative-map clause dropped (Decision 16, after Hanson re-verification — see below); editorial-convention-hierarchy specification grounded empirically (Decision 17, after diagnostic run); trapezoidal aoristic sensitivity scoped (full H3-eligible set + full-empire); Crisis window arithmetic corrected (AD 235–284 inclusive = 50 y); H3c residual classification clarified as descriptive; proxy-framing scoping sentence; pre-lodgement state attestation; shorter title; H3a sample size clarification; FP-calibration reproducibility anchor.
- **Decisions 12–17 logged** in `planning/decision-log.md`.
- **Hanson 2021 attribution re-verification** (2026-05-15). Bucket-(c) item 2 triggered a fresh-context PDF read; agent found the regional spatial pattern attributed to Hanson 2021 is not in the paper. A second consolidated re-verification (also fresh context) confirmed and surfaced a second mischaracterisation (SR1's "polity × century resolution" wording). A subsequent SDAM-AU library scan (8 Hanson items + 22 `roman_demography` items; PDF abstracts read for items lacking Zotero `abstractNote`) confirmed no Hanson-corpus paper supports the regional claim.
- **Editorial-convention-hierarchy five-test diagnostic** run (2026-05-15, `runs/2026-05-15-editorial-convention-hierarchy/`). Reframed the artefact mechanism as endpoint rounding under inclusive-Roman counting; midpoint inflation is derivative.
- **Comprehensive preregistration rewrite** (commit `eb189df`, 2026-05-16). 358 lines changed (223 insertions, 135 deletions). Implements Decisions 12–17, all bucket (c) resolutions, and the bucket (d) mechanical fixes. Primary RQ rescoped to within-province spatial; H3a respec'd as within-between (Mundlak) NBR; H2 restructured around recovery simulation; H3b recast as pre-specified exploratory; H3c-spatial reduced to Moran's I clustering only; H1 demoted from confirmatory hypothesis to completed groundwork; convention-shape model specified per Decision 17; temporal exploratory analysis added (Decision 13); plain-English walkthrough rewritten.
- **Preregistration changelog** updated (same commit). New sections: "Adversarial-review-driven revision (2026-05-14 → 2026-05-16)" and "Upcoming pre-lodgement steps."
- **Pre-lodgement citation audit** (commit `c322de6`, 2026-05-16). Fresh-context Explore agent verified every author-year citation and load-bearing factual claim against its source with page-anchored evidence. Three confabulations caught and corrected: (i) Hanson 2021 regional pattern (already addressed via Decision 16); (ii) SR1 "polity × century" wording; (iii) Duncan-Jones 2018 "~ 85 % step-down" (actual paper text: complete cessation after AD 167 per Fig. 4 / Table 7.1). Plus one paragraph-number error (Heřmánková §48 → §29), a wording-drift on Carleton 2025 β-range, a Cliff & Ord 1981 / Anselin 1995 attribution split, and a name-order slip (Bevan & Crema → Crema & Bevan). All applied to the prereg.
- **Rome-count reproducibility script** (commit `c322de6`). `runs/2026-05-16-rome-count-verification/`: small Python script that reproduces, from the LIRE v3.0 parquet under the preregistration's §1 filter, the cited Rome figures (65,435 / 36.230 % / 140,575 / 46.548 % / 115,174) — anchors the Rome-count claim for citation-audit reproducibility.
- **DOI / reference lookup** for seven missing Zotero entries (Timpson 2021 *Phil. Trans. R. Soc. B*; Gelman 2020 Bayesian Workflow arXiv:2011.01808; Mundlak 1978 *Econometrica*; Bell & Jones 2015 *PSRM*; Cliff & Ord 1981 Pion; Crema 2025 *Archaeometry*; Anselin 1995 *Geographical Analysis*). Returned via web-search agent; Shawn added all to Zotero with full-text where available.
- **Crema 2025 baorista citation tighten** (commit `e8d92a4`, 2026-05-16). §5 small-N citation cleaned from "Crema 2025 baorista" to "Crema 2025" (resolves cleanly to the *Archaeometry* methods paper; the `baorista` package is named separately where the implementation matters).
- **ChatGPT 5.5 cross-model review prompt** (commit `fc26497`, 2026-05-16). `planning/chatgpt-cross-model-review-prompt.md` — engineered to elicit orthogonal coverage (not parallel coverage) via prereg-specific failure-mode rubric, explicit anti-generic-QA framing, and named cross-model attention areas.
- **ChatGPT 5.5 review received and committed** (commit `6862031`, 2026-05-17). `planning/cross-model-adversarial-review-preregistration.md`. Lengthy; asks for changes; triage deferred to next session at 76 % context.
- **Continuity-doc and reflection-doc updates** (this entry, 2026-05-17): `docs/notes/reflections/continuity.md` updated to 2026-05-17 with new session-history entry, new "done milestones" entries, and refreshed priority-artefacts list. New entries appended to `session-reflection.md` (Entry 4), `abductive-reasoning.md` (Entry 6), `working-notes.md` (Obs 33, 34, 35).

**Decided**

- Promote variance partition to confirmatory; respec H3a as within-between NBR (Decision 12).
- Bounded exploratory temporal analysis via habit-removed residual trajectory (Decision 13).
- Bayesian mixture with recovery-simulation validation, replacing the prior maximum-likelihood deconvolution (Decision 14).
- H3b recast as pre-specified exploratory deviation-detection — no Holm family, no pre-committed effect-size magnitudes; resolves three consensus blockers at once (Decision 15).
- H3c-spatial decision rule reduced to Moran's I clustering only; regional-pattern clause dropped after the Hanson re-verification (Decision 16).
- `convention_SPA` shape specified with three empirically-grounded tier components (century, half-century, reign-related) per the 2026-05-15 diagnostic (Decision 17).
- Eleven bucket-(c) resolutions inline in the prereg.
- Five citation-audit corrections applied (one paragraph-number, one wording drift, one attribution split, one name-order, one confabulation paraphrase).
- ChatGPT review queued for next session (chosen deferral at 76 % context).

**Produced**

- 8 commits on `main`: `41a4821` (Decisions 12–16), `93711b2` (editorial-convention diagnostic spec + script), `cfe3dc3` (diagnostic outputs + Decision 17), `eb189df` (prereg rewrite + changelog), `c322de6` (citation-audit corrections + Rome verification), `e8d92a4` (Crema citation tighten), `fc26497` (ChatGPT review prompt), `6862031` (ChatGPT review committed).
- New decision-log entries 12–17 in `planning/decision-log.md`.
- New changelog sections (adversarial-review-driven revision + upcoming pre-lodgement steps) in `planning/preregistration-changelog.md`.
- New run directories: `runs/2026-05-15-editorial-convention-hierarchy/` (spec, scripts, outputs, REPORT.md); `runs/2026-05-16-rome-count-verification/` (script + outputs).
- New planning artefacts: `planning/chatgpt-cross-model-review-prompt.md`; `planning/cross-model-adversarial-review-preregistration.md`.
- Comprehensive prereg rewrite at `planning/preregistration-draft.md` (358 lines changed).

**Contextual assumptions**

- Adela delegated the prereg review to Shawn (noted at the start of bucket-(c) work). The dual Claude review + ChatGPT pass + planned Martin consultation is the substitute for what would otherwise have been a co-author review pass.
- The dual review was dispatched fresh-context on Opus deliberately to avoid the satisficing trap that "Claude reviewing Claude's prior work" risks. The two agents had different briefs (statistical vs. legibility) but shared rubric; convergence on the consensus blockers vindicated the dual-agent design.
- The ChatGPT 5.5 cross-model review prompt was engineered with explicit anti-generic-QA framing because of a worry that ChatGPT (or any frontier model not briefed) would default to journal-article-style critique rather than prereg-specific failure-mode hunting. The prompt's "What NOT to look for" section is doing real work.
- The decision to *defer* ChatGPT-review triage to the next session at 76 % context follows the standing rule "Context-management band 50–75 %... aggressive at 75 %." Triage requires iterative read + edit + verify cycles which would degrade past 85 %.
- Three confabulations in one source document (Hanson 2021) — all caught by the pre-lodgement audit — is the headline operational finding. It vindicates the anti-confabulation rule in CLAUDE.md as load-bearing infrastructure rather than ceremonial caution. It also raises the open question of whether other project documents (decision log, working notes, run reports) carry similar confabulations; the audit was scoped only to the prereg. A broader audit before lodgement is queued but not scheduled.
- All H1 v2 simulation outputs + the editorial-convention-hierarchy diagnostic are committed, pushed, and reproducible from the canonical random seeds (20260425 for H1 v2). The Rome-count is also anchored via the new verification script. Pre-lodgement reproducibility is in good shape.

---

## Entry 5 — 2026-05-17: round-2 ChatGPT triage, three diagnostics reshape the artefact, comprehensive rewrite, QA, round-3 cross-model saturation

Direct continuation of Entry 4 — same instance (no compaction) picking up the deferred ChatGPT 5.5 round-2 triage. Single sustained session of ~12 hours; ended at conscious-saturation state.

**Done**

- **ChatGPT 5.5 round-2 review triaged** into four buckets (`planning/chatgpt-review-triage.md`): 0 (a) superseded; 10 (b) substantive; 9 (c) mechanical / clarity; 2 (d) verification (both verified during triage — neither was a confabulation).
- **Three empirical diagnostics commissioned** in sequence to settle ChatGPT B3 (convention component vs Uniform aoristic). (i) `runs/2026-05-17-interval-width-diagnostic/` — found [1, 100] is 26.3% of the corpus; the 22.8× / 41.5× / 18.8× ratios were partly an artefact of the int-truncated-midpoint test statistic the 2026-05-15 diagnostic used. (ii) `runs/2026-05-17-empirical-spa-shape/` — the actual SPA shows no anchor-year structure at AD 50 / 150 / 250 (local excess −77 / −79 / +22); the dominant narrow spikes are at regnal years AD 122.5 (Hadrian; ratio 1.61×) and AD 77.5 (Flavian); the largest single discontinuity is the +1,159 step at the 1 BC / AD 1 boundary. (iii) `runs/2026-05-17-date-range-filtered-spas/` — regnal spikes *amplify* under narrow-precision filtering (AD 122.5 ratio rises 1.61× → 13.83×) while the century-boundary plateau-step pattern weakens decisively (Pearson r between SPA(≤25) and SPA(>100) = 0.34); a third regnal spike at AD 212.5 (Severan, [212, 217] = 728 inscriptions) emerged.
- **Bucket (b) walked through with Shawn one-at-a-time**, capturing **Decisions 18–26**. Decision 20 supersedes Decision 17 (template-interval slab convention component replaces the three-tier anchor-year structure).
- **Comprehensive prereg rewrite** implementing Decisions 18–26 + bucket (c) mechanical fixes. +146 / −78 over the 2026-05-16 baseline.
- **QA pass** by a fresh-context Claude agent against a structured QA brief. Caught 1 BLOCKING (Step 2 walkthrough omitted the multinomial likelihood) + 4 SHOULD-FIX (broken cross-references, line-31 ambiguity, SR1 conflated mixture-corrected SPA with cross-sectional scaling, §9 mis-located year-precise inscriptions) + 2 MINOR. All applied.
- **Round-3 saturation check** via ChatGPT 5.5 (fresh chat) and Gemini 3 Pro (fresh context) on the same prompt. Both models returned 1 BLOCKING (cross-model agreement: H3c described as receiving mixture correction when it should inherit H3a's date-filtered scope) + 1 SHOULD-FIX each (ChatGPT: multinomial normalisation precision; Gemini: "year-0" terminology wrong for Julian / Gregorian calendar). Both verdicts converged on "ready for Martin after these corrections." All three findings applied to prereg + decision log + changelog.
- **Continuity.md + new-session prompt drafted**. `docs/notes/reflections/continuity.md` updated for post-round-3 state; `planning/next-session-prompt-2026-05-17.md` drafted for the fresh-context CC who will take Martin's pack (Task #6 → Task #17 in the wider tracker). Flagged the non-standard continuity.md path explicitly in the new-session prompt.

**Decided**

- **Decision 18**: H3a three-way directional verdict (supported / evidence against / inconclusive) + posterior-probability ladder reporting.
- **Decision 19**: Bayesian mixture observation model — multinomial primary; Dirichlet-multinomial + rescaled NegBin supplementary. Primary item for Martin's consultation.
- **Decision 20**: Convention component is a template-interval slab structure (century-slab + half-century-slab + reign-interval-slab tiers; dictionary pinned by pre-Phase-2 empirical scan; year-precise inscriptions in `genuine_SPA`). **Supersedes Decision 17.**
- **Decision 21**: H2.1 recovery-simulation grid procedurally pre-committed (axes + per-cell ≥ 50 replicates + cell-wise reporting + design-artefact reference); specific values pinned in `runs/2026-05-XX-recovery-grid-design/` pre-Phase-2 artefact. Primary item for Martin's consultation.
- **Decision 22**: H3a uses date-window-filtered counts (not mixture-corrected); mixture corrects temporal analyses only. Primary RQ rewording.
- **Decision 23**: H3c Pearson residuals; capitals contrast on draw-wise residuals; Moran's I on posterior-mean residuals with field-standard conditional permutation inference; posterior distribution of Moran's I across draws reported supplementarily. Primary item for Martin's consultation.
- **Decision 24**: Freeze LIRE v3.0 for this OSF lodgement. LIST v1.2 reserved for post-lodgement amendment or follow-up.
- **Decision 25**: PPC failure triggers are numerical, not narrative. Specifics pinned in the same pre-Phase-2 design artefact as the recovery grid (one artefact, two specification tables). Primary item for Martin's consultation.
- **Decision 26**: Hanson-population measurement-error sensitivity (σ_pop ∈ {0.1, 0.2, 0.3}) added to §5; Western-Empire-provincial subset operationalised via the project's `province_language` classification (Latin, excluding Roma; 41 LIRE provinces).
- **Round-3 H3c clarification** (inline correction in Decision 22's entry; not a new decision): H3c is *not* in the mixture-correction scope. It inherits H3a's date-filtered-count scope. Marked "round-3 clarification 2026-05-17."

**Produced**

- 0 commits — Shawn typically reviews and commits himself at end of session. All changes are in the working tree.
- Three diagnostic run directories with full reports + figures + tables: `runs/2026-05-17-interval-width-diagnostic/`, `runs/2026-05-17-empirical-spa-shape/`, `runs/2026-05-17-date-range-filtered-spas/`.
- New planning documents: `planning/chatgpt-review-triage.md` (4-bucket triage doc); `planning/saturation-check-prompt-2026-05-17.md` (round-3 prompt); `planning/prereg-saturation-check-GPT55.md` + `planning/prereg-saturation-check-gemini.md` (round-3 model responses); `planning/next-session-prompt-2026-05-17.md` (handoff prompt).
- Updates to: `planning/preregistration-draft.md` (+149 / −79 net, ~451 lines); `planning/decision-log.md` (Decisions 18–26 added + round-3 inline clarifications + Decision 17 supersession note); `planning/preregistration-changelog.md` (full round-2-triage + diagnostics + rewrite + QA + round-3 saturation arc added); `docs/notes/reflections/continuity.md` (post-round-3 snapshot + done milestones + priority artefacts updated); reflection docs (this entry + session-reflection Entry 5 + abductive-reasoning Entry 7 + working-notes Obs 36–39).

**Contextual assumptions**

- The session started with Shawn's continuity prompt explicitly framing the work as "pick up the preregistration cycle" from the deferred ChatGPT-review triage. The prior session's deferral at 76% context (Entry 4's end-state) was the design that made this single sustained session productive — round 2's findings had time to be triaged carefully rather than rushed.
- The diagnostic cascade (three diagnostics in sequence) was reactive, not pre-planned. Each diagnostic was commissioned in response to the previous one's surprises. The decision-log records the conclusions cleanly but the *process* was sequential surprise rather than three-step study. This is captured in session-reflection Entry 5 and abductive-reasoning Entry 7 for posterity.
- The bucket-(b) walkthrough mode (one item at a time with options + recommendation + Shawn's call captured as Decision 18+) is the same pattern that produced Decisions 12–17 in the prior session. Same pattern, different round; nine decisions in one extended session.
- Round-3 saturation check was framed deliberately as "find only what warrants another revision cycle" rather than as comprehensive adversarial review. The saturation-check framing is a deliberate methodological choice — the document has matured enough that comprehensive review would manufacture findings to look thorough. Both round-3 models calibrated to this framing. See Obs 39 for the pattern.
- The ChatGPT 5.5 round-3 chat was a *new* chat, not a continuation of the round-2 chat. The reasoning (anchoring on prior framing vs fresh document evidence; pairing fresh-context with Gemini's fresh-context for clean cross-model comparison) was a small but consequential design decision made mid-session.
- The two pre-Phase-2 design artefacts (`runs/2026-05-XX-template-dictionary/` for Decision 20's slab dictionary; `runs/2026-05-XX-recovery-grid-design/` for Decisions 21 + 25's recovery-grid values + numerical PPC thresholds) are named in the prereg but do not yet exist on disk. They are committed-before-Phase-2 commitments; the prereg binds to their commit hashes prospectively.
- Conscious-saturation state was the felt session-end goal Shawn named at round 3 start ("I'd feel better if we got to the point where we consciously say 'ok, I've seen the feedback, and none of it is worth actioning, the prereg is good'"). The round-3 cross-model convergent verdict ("ready for Martin after these corrections") delivered on that goal.


---

## Entry 6 — 2026-05-17 (later): Martin consultation pack, stand-in cross-model statistical reviews, Decisions 27–32, prereg incorporates, lodgement-ready

Direct continuation of Entry 5 — same instance (no compaction), picking up immediately after Entry 5's conscious-saturation handoff. About twelve hours of total work today across the two entries.

**Done**

- **Drafted Martin's statistician consultation pack** at `planning/martin-consultation-pack-2026-05-17.md` (863 lines). Structure: executive summary (with substantive-question lead paragraph at Shawn's request) + 8-question list (4 primary tracking the Martin-flagged decisions D19 / D21 / D23 / D25, plus secondary on D12 Mundlak + D13 trajectory + Field-3 multiplicity + design-artefact contents) + deep-dive appendices (orientation, primary-question, secondary-question, supporting reference material). Tuned for applied-econometrician audience (Mundlak / RDF / FDR-Holm / RoPE vocabulary used directly; Roman-epigraphy context kept brief).
- **Ran two stand-in cross-model statistical reviews** as a hedge against Martin's potential delay before Adela's Friday 2026-05-22 conference presentation. ChatGPT 5.5 and Gemini 3 Pro, both in an "applied econometrician / statistician giving a targeted review before the actual statistician sees it" role. Committed at `planning/GPT55-statistical-review.md` and `planning/gemini-statistical-review.md`.
- **Identified two cross-model-agreement items** (replicate-count floor too thin at ≥ 50; Pearson r too forgiving as binding shape-recovery metric) and **five single-model items** (all GPT5.5: aoristic-MC sensitivity; H3c-specific posterior-predictive spatial-autocorrelation PPC; two-tier PPC severity scheme; three-case interpretive guardrail for H3c(ii) Moran's I; population- / inscription-weighted `f_within` sensitivity).
- **Captured all seven items as Decisions 27–32** in `planning/decision-log.md` (541 lines added). Each decision tagged "provisional pending Martin's eventual review; subject to revision via OSF amendment." Six separate decisions for honesty (matches the project's one-decision-per-substantive-change pattern; merging was an option but rejected).
- **Edited the preregistration draft** (`planning/preregistration-draft.md`) to incorporate D27–32 across §3 (mixture model + H3a PPC + H3c residuals/Moran's I), §4 (Phase 2 recovery sim), §5 (exploratory three-weighting sensitivity), §6 (effect-size table), §7 (contingencies), and Field 3 H3c(ii) wording. Decision: no provenance markers in the prereg itself — clean methodological statements of *what* will be done; provenance lives in decision log and changelog.
- **Updated the changelog** (`planning/preregistration-changelog.md`) with a new "2026-05-17 (later) — Stand-in cross-model statistical review; Decisions 27–32" section recording the cross-model-vs-single-model split, the per-decision rationale, the methodological note on LLM-stand-in substitution, and the rewritten "Upcoming pre-lodgement steps" section (lodgement target Tuesday 2026-05-19; pre-Tuesday Martin reply folded in; otherwise lodge as-is and treat subsequent Martin feedback as OSF amendments).
- **Reframed the consultation pack's `[stand-in update]` markers** from "Proposed pending Martin's sign-off" to "Incorporated [stand-in update — Decision NN]; reversal via OSF amendment if your review recommends it." Top acknowledgement paragraph and Q-summary table footnote rewritten to match.
- **Five focused commits**: `482cc87` (stand-in review files); `feae7c5` (Decisions 27–32); `88de0e5` (prereg surgical edits); `4bc67bd` (changelog); `28fd3f7` (pack reframing). Pushed to origin/main.
- **Wrap-up artefacts**: continuity.md updated for the post-D27–32 lodgement-ready state (snapshot rewritten; new "Pre-lodgement staging work" section; Done milestones extended); working-notes Obs 40 (the 2026-05-17 diagnostic triplet's substantive findings — anchor-year intuition falsified, slab structure emerged, regnal spikes are real ancient clustering, +1,159 BC/AD boundary step) and Obs 41 (the stand-in-cross-model-review pattern as transferable methodological technique); next-session prompt at `planning/next-session-prompt-2026-05-18.md` with the lodgement-staging queue. One additional commit (`939d331`) + push for the wrap-up.
- **Earlier in the session, before the stand-in-review pivot**: drafted the consultation pack including substantive-question lead paragraph; identified the two stand-in reviews' findings; recommended bumping the cross-model-agreement items as straws and incorporating the single-model items as proposed pending Martin; pivoted to "incorporate everything as Decisions 27–32" when Shawn decided to push forward with Tuesday lodgement regardless of Martin's reply timing.

**Decided**

- **Send pack to Martin 2026-05-17 (today)**; lodge on OSF Tuesday 2026-05-19 whether or not Martin replies; any subsequent Martin feedback handled as post-lodgement OSF amendments per §7. Adela's Friday 2026-05-22 conference is the hard deadline.
- **Six separate decisions (27–32) rather than fewer combined decisions** — preserves the project's one-substantive-change-per-decision pattern; matches the existing 18–26 cadence.
- **No provenance markers in the prereg itself** — provenance lives in decision log and changelog; prereg is a clean statement of methodology. Pack carries provenance via `[stand-in update]` markers.
- **Cross-model-agreement items bumped as straws (D27); single-model items incorporated as preregistered methodology (D28–32)** — all subject to OSF amendment if Martin recommends revision. The single-model items are real catches addressing genuine gaps; deferring them indefinitely would be over-cautious.
- **Wrap up this session ad-hoc rather than try `/handoff`** (which landed after this session launched) — `/handoff` available in the next session; the manual wrap-up uses what's already in context.

**Produced**

- 6 commits, 6 file changes by content: `planning/decision-log.md`, `planning/preregistration-draft.md`, `planning/preregistration-changelog.md`, `planning/martin-consultation-pack-2026-05-17.md` (new), `planning/GPT55-statistical-review.md` + `planning/gemini-statistical-review.md` (new), `planning/next-session-prompt-2026-05-18.md` (new), `docs/notes/reflections/continuity.md`, `docs/notes/reflections/working-notes.md`.
- 6 new decisions (27–32) totalling ~ 541 lines in the decision log.
- 1 new section in the changelog (~ 153 lines).
- Prereg surgical edits totalling +36 / −12 lines (net).
- Pack additions and reframing totalling +58 / −14 lines (net).
- Working-notes Obs 40 (~ 80 lines) and Obs 41 (~ 60 lines).
- Continuity.md updates (+171 / −3 lines).
- Next-session prompt (~ 100 lines).

**Contextual assumptions.** The Friday 2026-05-22 conference presentation by Adela imposed the hard deadline that drove the "lodge Tuesday regardless of Martin's reply" decision. Without that deadline, the natural workflow would have been: send pack → wait for Martin → incorporate → lodge. With the deadline, the workflow became: send pack and run stand-in review in parallel → incorporate stand-in findings as Decisions 27–32 → lodge Tuesday with the stand-in-derived methodology → treat Martin's eventual reply as post-lodgement amendment work. The trade-off (visible-on-OSF amendment trail vs missed conference feedback opportunity) was discussed explicitly with Shawn; the lodgement-with-amendments choice was the conscious one. The stand-in-review-as-hedge-against-delay is a specific methodological substitution that wouldn't be the default in normal circumstances.

The session ended cleanly with no outstanding edits; all artefacts committed and pushed. The handoff to the next session is well-documented (continuity.md + next-session prompt + working-notes Obs 40/41); the next session can begin staging work (template-dictionary scan; recovery-grid-design draft; date-stamp prereg refs; OSF lodgement) immediately after a brief read of the continuity doc.

---

## Entry 7 — 2026-05-20 → 2026-05-21: OSF lodgement (with four-iteration PDF) and overnight conference-talk planning

Two calendar days of operational work that closed the OSF lodgement and opened the RAC-TRAC 2026 conference-talk implementation phase.

**OSF lodgement workflow (2026-05-20).**

- **Pre-lodgement final fixes** to `planning/preregistration-draft.md`: radiocarbon-SPA lineage framing rewritten (Rick 1987 → Williams 2012 → Timpson et al. 2014 → Crema & Bevan 2021) per Shawn's added Field-2 paragraph; 5-year-bin rationale rewritten with empirical justification (the Antonine probe's 15-year window forces bin ≤ 5 y); typo fixes in the goals paragraph; LIRE v3.0 DOI corrected (was `8147298` = v2.3; now `8431452` = v3.0); duplicate DOI bug at §8 Data line caught and fixed by the second pre-lodgement pass; pipe-in-table-cell escape applied to §7 H3c(i) row in both `preregistration-draft.md` and the OSF supplementary `osf-supplementary-2026-05-20.md`.
- **OSF supplementary file** built as `planning/osf-supplementary-2026-05-20.md` (498 lines): YAML frontmatter / format note / Field 1 / Field 2 stripped (those go into OSF form fields directly); Field-wrapper labels dropped; Field 3 renumbered to §1; Field 4 subsections § 1–12 renumbered to §2–13; 42 internal `§N` cross-references systematically incremented by +1; paper-internal `§29 / §45 / §60` references (in the Heřmánková 2021 citation) correctly preserved. A new "Preregistration — supplementary detail" title block and one-paragraph lede prepended for self-containment.
- **§12 References list** compiled: 21 entries; APA-7-ish author-date format with sentence case in titles and DOI URLs; alphabetical by first-author surname with same-author entries chronological; Mundlak 1978 included as eponym-source for the within-between specification.
- **Bibliography verification**: 18 of 20 catalogued citations confirmed present in Shawn's Zotero (item IDs in the bibliography commit message); 3 added via `/cite-new` (Rick 1987; LIRE v3.0 dataset; LIST v1.2 dataset). The LIRE Zenodo DOI mismatch (v2.3 at `8147298` vs v3.0 at `8431452`) caught at this stage via DataCite API verification.
- **PDF iteration v1 → v4** via pandoc 3.6.3 + xelatex. v1 (1 in margins, default mono; URL truncation present but not flagged yet). v2 (pipe-in-cell fix; 0.8 in margins; monofont Scale=0.78 to fit the ASCII flowchart and the H3a NBR formula). v3 (`xurl` package added — ineffective alone because pandoc rendered bare URLs as plain text). v4 (`-f markdown+autolink_bare_uris` + `xurl` together — finally produced clean wrapping). Each iteration committed and the OSF lodgement tag re-pointed.
- **Adversarial verifier** dispatched after PDF v2 against the supplementary file. Verdict: PARTIAL → PASS after the pipe-in-cell fix. Verifier caught the truncation bug that author-side review had missed; without the verifier the lodged artefact would have contained a corrupted decision rule in §7.
- **Lodgement tag chain**: `acf7263` (initial v2) → `dca8d99` (pipe-fix v2) → `9d12ce9` (v3 with xurl-only) → final at `dca8d99...→ a2e40fd` post v4 (autolink + xurl). Each move via `git tag -d` + `git push --delete` + `git tag -a` + `git push origin`, with annotation updated each time.
- **OSF deposit completed** by Shawn 2026-05-20 evening at `https://osf.io/uycs6/`. Embargoed pending decision on submission to a journal requiring double-blind review.

**Overnight conference-talk planning (2026-05-20 evening into 2026-05-21).**

- **Conference scout** dispatched in background (RAC-TRAC 2026 Aarhus details, audience profile, programme parsing). Returned mid-foreground-work with the critical finding that Shawn — not Adela — has the SPA paper at 14:20 Friday, with Adela's own marriage-ages paper at 12:20 the same session. Flagged in handoff for morning resolution.
- **Asset inventory** (`planning/conference-talk-rac-trac-2026/asset-inventory.md`): catalogued the 2024 exploratory notebook's pipeline (empire/province/city SPAs; frequentist NBR-with-bootstrap; Hanson-pop join already done) and the three 2026-05-17 diagnostic runs as the figure substrate for the talk. Main work for next session: apply the prereg date-window filter + re-render at slide aspect.
- **Slide outline** (`planning/conference-talk-rac-trac-2026/slide-outline.qmd`): 7-slide Quarto revealjs skeleton with speaker notes embedded as HTML comments; placeholders for figures; footer + slides #5/#7 reference the OSF URL.
- **Analysis roadmap** (`analysis-roadmap.md`): 36-hour hour-by-hour plan with two explicit decision gates (hour 18 for A+ go/no-go; hour 26 for Bayesian H3a stretch). Per Shawn's "A+ if possible with fallback to lean A" framing.
- **Talking points** (`talking-points-feedback.md`): 7 anticipated audience objections with prepared responses (epigraphic-habit-only critique; Hanson-pop uncertainty; Rome exclusion; frequentist-vs-Bayesian justification; editorial-template handling; subgroup nominations; survival-bias). 5 feedback prompts for the closing slide.
- **Conference context** (`conference-context.md`): full briefing from the scout — RAC/TRAC identity, dates, venue, TRAC7 session details with running order, audience profile (Roman archaeologists, classicists, digital humanists; LIRE creators are session organisers), format expectations, past editions, practical info.
- **Continuity update**: research-state snapshot rewritten for post-lodgement state; new "Conference talk — RAC-TRAC 2026" in-flight section replacing the (completed) pre-lodgement staging work.
- **Next-session handoff prompt** (`planning/next-session-prompt-2026-05-21.md`): briefs the new CC instance with the resolved-questions section at the top, decision-gate framing, risk register, audience reality (LIRE creators in the room), and out-of-scope clarifications.

**Morning resolution (2026-05-21).**

- **Speaker confirmed**: Adela reads Shawn's paper at the 14:20 slot. Shawn can't travel; remote presentation not supported. Adela's own 12:20 marriage-ages paper is separate work.
- **OSF URL confirmed**: `https://osf.io/uycs6/`, embargoed. Folded into prereg §11 Provenance (post-lodgement amendment trail); slide deck footer + slides #5/#7; README.md (previously single-line; now a proper project landing page).
- **`/handoff` invoked**: continuity session-log entry appended; working-notes Obs 42–45 added (pandoc URL handling; markdown pipe escape; Zenodo concept-DOI confusion; adversarial-verifier pattern); five wiki candidates flagged in personal-assistant `notes/_inbox.md`; new file `docs/notes/user-observations.md` seeded with four observations Shawn accepted.

**Artefacts touched (this session).**

- 14 commits across the inscriptions repo (`3da5711` to `848edfa`) covering bibliography compilation, four PDF iterations with tag-moves, OSF supplementary file creation + clean-up, continuity updates, conference-talk planning bundle, morning resolution, and `/handoff` close.
- 1 commit in personal-assistant `notes/` repo (`8098985`) — `_inbox.md` additions for weekly-review curation.
- New planning directory `planning/conference-talk-rac-trac-2026/` (5 files: conference-context, asset-inventory, slide-outline.qmd, analysis-roadmap, talking-points-feedback).
- New `planning/next-session-prompt-2026-05-21.md`.
- New `planning/osf-supplementary-2026-05-20.md` + `.pdf` (the lodged supplementary artefact).
- New `planning/prior-art-scout-2026-05-19-hmm-aoristic.md` (already from 2026-05-19 but committed during today's work).
- New `docs/notes/user-observations.md` (4 entries seeded at /handoff).
- Updated `README.md` from single-line to full project landing page.
- Updated `planning/preregistration-draft.md` (§11 Provenance OSF-URL amendment trail; multiple pre-lodgement fixes; §12 References added; §8 Data DOI corrected).
- Updated `docs/notes/reflections/continuity.md` (research-state snapshot post-lodgement; in-flight section updated; session-log entry appended).
- Updated `docs/notes/reflections/working-notes.md` (Obs 42–45 appended).
- Lodgement tag `osf-lodgement-2026-05-20` created and re-pointed four times, settling at commit `a2e40fd` post v4 PDF.

**Contextual assumptions.** The Friday 2026-05-22 conference deadline is now a *hard* deadline — Adela needs the slide deck and speaker notes by Friday morning Aarhus time. The 36-hour analysis roadmap is built around her arrival; the decision gates exist because the implementation work is genuinely time-bounded. The OSF embargo on the prereg is a "in case we go double-blind" hedge, not a settled decision; the URL is publicly visible (unblockable) but the deposit contents are gated. The lodgement tag NOT including the OSF-URL amendment (the amendment lives in post-tag commits) is the deliberate convention — anyone needing the "as lodged" version clones at the tag, not at main. The next-session implementation work has been deliberately kept out of this session because the cleaner handoff is starting fresh with the roadmap in hand rather than mid-debugging-cycle.

---

## 2026-05-21 → 2026-05-22 — Session log: RAC-TRAC talk-prep arc, end to end

Continuous single-session run from the Entry-7 handoff (post-OSF-lodgement, conference-talk-implementation pivot) through to a clean session-close for Adela's Friday-afternoon delivery at TRAC7 Aarhus.

**Repository state at session open**: HEAD = `b0f1ddd` (`docs(reflect): /reflect entries — Entry 7 across reflection docs`). Clean tree.

**Repository state at session close**: HEAD = `51f3c9f` (`docs(continuity): session handoff — talk-day queue + next-session prompt`). Clean tree. On origin/main.

**Block-by-block summary of work landed**:

- **Block 1** (`runs/2026-05-21-talk-prep/code/01-filter-and-prep.py`): apply prereg-canonical filter to LIRE v3.0; 180,609 rows; four row-level counts hit exact (180,609 / 65,435 Rome / 115,174 ex-Rome / 140,575 Hanson-city-assigned). One flagged finding deferred: the prereg's "~ 815" Hanson-cities figure was inherited from a stale Latin-province subset; text-spec-faithful count is 1,044. Shawn approved (a) — broader 1,044-city sample.
- **Block 2** (`02-empire-province-city-spas.py`): empire/province/city raw SPAs at 16:9; later re-rendered as 2x4 small-multiples per Shawn's feedback. Validity check: Pompeii cuts off cleanly at AD 79.
- **Block 3** (`03-hanson-nbr-bootstrap.py`): frequentist NBR + 1,000-replicate row-resample bootstrap. β = 0.566, 95 % CI [0.543, 0.574]; OLS log-log β = 0.284, R² = 0.04. Later re-rendered with (const, slope) bootstrap pairs for a fitted-line CI band.
- **Block 4** (`04-mixture-recovery-synthetic.py`): synthetic mixture-recovery demo. α posterior covers truth (0.477 / 95 % CI [0.414, 0.541]; truth 0.50); Pearson r = 1.000 vs true p_gen; all prereg validation gates pass. Ran on sapphire (2 s; native C-compile).
- **Block 4b** (`05-h3a-bayesian-mundlak.py`): Bayesian within-between Mundlak NBR per prereg §4. β_within = 0.587; β_between ≈ −0.26 (CI straddles 0); **f_within = 0.299, 95 % CI [0.240, 0.366]; verdict supported**. Re-fit with tune=3,000 (initial tune=1,000 hit R-hat = 1.0100 exactly at gate). Ran on sapphire (78 s).
- **Block 5** (slide assembly): populated `slide-outline.qmd` with all five new figures + numerical results. Added a new slide 6b for the Mundlak result. Wired in slide-2 figures from `runs/2026-05-17-*/` and slide-3 figure from `runs/2026-04-25-h1-simulation/`. Rendered three formats: Quarto revealjs HTML; LaTeX paper-document PDF; slide-format PDF via Decktape + Brave (installed at `~/tools/decktape/` for this session, reusable for HUMN8031). Fixed title-slide "Invalid Date" bug + empty-slide-from-orphan-comment bug.
- **Block 6** (`adela-briefing.md`): wrote the slide-by-slide cheat-sheet + 9 anticipated-question Q&A responses + backup-slide map + tone framing + logistics. ~ 4,000 words.

**Phase A sensitivities (Block 6 + 7, ran overnight on sapphire)**:
- `06-sensitivity-weighting.py`: three-weighting f_within. Material divergence flagged per prereg §5: unweighted 0.300; population-weighted 0.496; inscription-weighted 0.421. Median spread 0.196 > primary half-width 0.063. Substantive finding logged in working-notes Obs 46 + abductive-reasoning Entry 10.
- `07-sensitivity-measurement-error.py`: Hanson-population measurement-error at σ_pop ∈ {0.1, 0.2, 0.3}. ROBUST under all three σ_pop levels; max shift from primary 0.045, well inside the 0.063 threshold. Strengthens the B3 backup-slide claim.

**Phase B mixture-recovery grid validation (running on sapphire)**:
- Spawned a background `general-purpose` agent in a worktree to handle the design + harness + smoke-test + launch. Worktree at `.claude/worktrees/agent-a6e1b611cd0719a27`.
- Agent committed 4 logical units: design artefact (`runs/2026-05-22-recovery-grid-design/`), simulation harness (`runs/2026-05-22-recovery-grid-validation/code/`), smoke-test results + dynamic-module-loading fix, subprocess-pool orchestrator + halt-for-direction.
- Grid axes (honouring prereg/Decision 21 binding minimums): 5 α × 6 shapes × 5 tier-weight vectors × 3 N values × 100 replicates = 450 cells × 100 reps = 45,000 fits.
- Smoke test passed: one cell × one replicate gave α covering truth, Pearson r = 0.9929 (above prereg-binding 0.95), R̂ = 1.0063, 0 divergences.
- Agent halted at launch decision because parallel-load wall-clock projection (27-66 h) exceeded the brief's 9.4 h spec estimate. Main thread launched after Shawn's "save ~ 20 % of cores; multi-day OK" direction.
- Worktree merged into main via `--no-ff` (commit `db04bf0`); worktree branch deleted after merge.
- Grid running on sapphire at `~/cc-scratch/inscriptions-recovery-grid/` with `--n-jobs 19`. 9 of 450 cells complete at session-close (~ 10 h elapsed). Realistic wall-clock estimate now 80-120 h based on observed per-fit timing under parallel load.

**Tier-1 historian-facing reachability guide**:
- `runs/2026-05-22-reachability-guide/code/build-historian-table.py` — derives a worst-case-across-nulls detection-rate table from the existing Phase 1 v2 `power-curves.parquet`. No new compute required.
- `runs/2026-05-22-reachability-guide/code/rerender-slide-3a-heatmap.py` — re-renders the slide 3a Phase-1 heatmap in red-yellow-green palette matching slide 3b's colour grammar.
- Three-panel heatmap (empire / province / urban-area) with detection rate annotated per cell; greyed cells mark "not in this level's simulation grid".
- Paper draft fragment at `planning/paper-subsection-reachability.md` (~ 1,200 words) with collegia worked example.
- Tier 2/3/4 follow-ups logged in continuity (finer bracket grid; per-subset reachability; baorista parallel analysis).
- Slide 3b in main deck (was B13; promoted on Shawn's request).

**Deck iteration arc** (high-level, no commit-by-commit fidelity):

- Initial: 7-slide skeleton from the overnight planning.
- Pass 1: added slide 6b for Mundlak result (8 main slides).
- Pass 2: applied `smaller: true` globally + per-slide trims to fight overflow under revealjs's 720p canvas.
- Pass 3: ruthless visible-text minimisation per Shawn's pedagogical feedback ("audiences can't both read and listen").
- Pass 4: renamed slide 6 → 6a; replaced jargony "binding analysis" with question-form title; added 12 backup slides (B1-B12) for anticipated-question reserve.
- Pass 5: added 9 G-series methods-glossary slides for plain-English methods explainers.
- Pass 6: added B13 (reachability heatmap); promoted to slide 3b in the next pass; renamed slide 3 → 3a.
- Pass 7: fixed slide 3a chart bug (sharey=True misaligned empire-level data); recoloured to RYG to match 3b; tightened bracket labels to prevent overlap.
- Pass 8: corrected "1,549 min N" → "~ 1,600 (range 1,400 – 1,950 across nulls)" per the four-cell range; expanded speaker notes with empire-only-at-50k rationale + 1,600 vs 1,549 rationale.

Final deck: 33 slides (title + 9 main + deep-dive intro + 12 B + glossary intro + 9 G).

**Continuity updates**:
- Four open caveats from Phase B work logged: concurrency slowdown unresolved; `pilot_proxy` tier vector is a proxy not a real posterior draw; W-1 + PPC numerical thresholds deferred; smoke-test R-hat close to gate.
- Tier 2/3/4 reachability extensions logged as future work.
- New "Talk-day handoff queue" section above the existing Phase 2 substantive work queue, with three immediate priorities for next session.

**Tooling additions** (out-of-repo, local machine):
- `~/tools/decktape/` — local Decktape install via npm (109 deps, no Chromium pull). Points at Brave via `PUPPETEER_EXECUTABLE_PATH=/usr/bin/brave-browser`. Reusable across projects.

**Sapphire workspace**:
- `~/cc-scratch/inscriptions-talk-prep/` — Phase A sensitivities + Blocks 1-5 sapphire mirror; venv with pymc 6.0.1.
- `~/cc-scratch/inscriptions-recovery-grid/` — Phase 2 grid validation; running.

**Memory captures**:
- Saved feedback memory: route compute to sapphire (not local); background tasks > 3 min. (Existing scratchpad rule from 2026-03-24 was the primary; the JSONL memory entry is the secondary capture.)

**Contextual assumptions.** This session ran continuously across a calendar-day boundary without compaction or instance change — all entries reflect direct first-person experience. The talk delivery is Friday 2026-05-22 14:20 Aarhus time, ~ 7-8 hours after session close (Australia time). Adela has feedback in Shawn's email (not in the project files at session close); next session inherits the incorporation task. The Phase 2 grid is running independent of any further session activity; sapphire is on a stable network and the nohup process survives session disconnection. Standing rules respected throughout: all serious compute on sapphire; local-machine work limited to text edits + visual QA + light pandas; no silent parameter reductions on preregistered analyses; binary deliverables visually confirmed with Shawn before commit (validated repeatedly this session — Shawn caught the 1,549-false-precision issue and the slide-3a chart bug that I had visual-scanned without noticing).
