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


---

## 2026-05-22 — Talk-day session (Adela's feedback incorporated; Phase 2 grid restarted)

**Scope.** Final deck-prep ahead of Adela's 14:20 Friday delivery at TRAC7 Aarhus. Incorporated her per-slide feedback into the deck; produced standalone speaker artefacts; killed and restarted the Phase 2 mixture-recovery grid under an optimised concurrency configuration after a background investigation diagnosed the slowdown cause.

**Deck content changes.**

- Main path went from 9 main / 12 backup / 9 glossary to **9 main + 13 backup + 9 glossary**, plus new slide 7a (worked example).
- Slide 6 merged old 6a (frequentist NBR comparator) and 6b (Bayesian Mundlak) into a single "What we found" punchline slide. Frequentist NBR demoted to B12.
- Slide 7a added (between general implications and feedback questions) promoting Adela's wife/daughter corpus as a worked example.
- Slide 5 reworked to drop the alpha-posterior framing in main visible content; "Output" line added in right column.
- Slide 2 went through three iterations on minimalism (caption + punchline + spike interpretation).
- Slides 3a / 3b: technical jargon stripped from captions (`a_50pc_50y`, `CPL-Gaussian` gone); bullets tightened.
- Slide 4: captions now name Pompeii AD 79 cut-off + Dacia AD 106-271 window as verified interpretive anchors.
- Slides 7, 8, 9 split from the previous combined slide 7: implications / feedback questions / open science as three separate slides.
- B1, B3, B7, B13 elaborated for standalone-readability (Shawn's request that backup slides be consult-as-artefact rather than terse).
- B1, B3, B13 subsequently split into a/b pairs to fix overflow on PDF render (no `.scrollable`; clean two-slide approach).
- New backup R-slide B13a/b: Multi-scale (MAUP) cross-check — direct response to Adela's specific critique.
- Local hardware references (`zbook`, `sapphire`) scrubbed from speaker notes and B-slide bodies.
- All stale `slide 6a` / `slide 6b` cross-references updated to `slide 6` post-merge.

**Figures.**

- `fig-06-variance-partition.png` (new): clean horizontal stacked bar showing the 30 % within-province / 70 % "habit · economic · social · political · cultural · survival" partition with 95 % CI annotation. Built in matplotlib (~ 30 lines); replaces the four-panel posterior summary as the slide-6 hero.
- Five figures with baked-in matplotlib titles cropped via PIL: `fig-02a` (was "A1. Empirical SPA — uniform aoristic mass…"); `fig-03` (was "Phase 1 reachability — provincial level…"); `fig-04b` ("Raw uncorrected per-province SPAs:…"); `fig-04c` ("Raw uncorrected per-city SPAs:…"); `fig-05` ("Synthetic mixture recovery (one cell)"). Originals preserved as `*.original.png` siblings for round-trip recovery.
- `fig-04b` and `fig-04c` got short title bars added back via PIL composite ("Uncorrected per-province SPAs" / "Uncorrected per-city SPAs") at Shawn's request — short chart titles on the figure, separate caption underneath.
- `fig-05` had the left "Posterior on alpha" panel cropped off (~ 1/3 of figure width); the right two panels (synthetic data decomposition + recovered ancient signal vs truth) are what now displays. Caption rewritten to describe both panels.

**Speaker artefacts.**

- HTML-comment speaker notes converted to `::: notes` divs so reveal.js speaker view (press `s`) picks them up (27 blocks).
- All 27 notes rewritten as glance-friendly bullet lists (target ≤ 10-15 bullets per main slide; ≤ 6 per backup).
- `inscription-spa-script.md/.pdf`: continuous-prose speaker script for rehearsal, ~ 1,900 spoken words across 10 slides (~ 12.7 min at 150 wpm). Hybrid format: slide-number headings as soft breaks; slide-advance cues in `[brackets]`.
- `inscription-spa-notes.md/.pdf`: standalone bullet-form notes extracted from the `::: notes` divs, keyed to each slide. Printable / second-screen reference for live delivery.

**File renames.** All deck-related artefacts renamed from `slide-outline.*` to `inscription-spa-*` for semantic clarity. Stale prior-session paper-format PDF moved to `archive/planning/conference-talk-rac-trac-2026/slide-outline-paper-format-2026-05-22-1244.pdf`.

**Grid restart.**

- Background investigation agent diagnosed: SMT saturation (19 workers on 12 physical cores = 14 of 19 workers SMT-paired; 21% silicon-level wall-clock lost to contention, invisible to per-worker CPU%).
- Recommended config: `n_jobs=12`, `taskset -c 0-11` pin to physical cores, `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`.
- Second background agent applied the restart. Verification: 12 workers spawned, all pinned to logical CPUs 0-11 (mask `fff`).
- Empirical post-restart timings: N=2,000 ≈ 18 s/fit (predicted 20-25); N=10,000 ≈ 30 s/fit (predicted 29-36). Wall-clock projection ~ 31.6 h (was ~ 100 h).
- Grid running unattended at session close. Pre-restart snapshot of `grid-state.json` preserved on sapphire.

**Background agents this session (3 total, all clean returns).**

1. Concurrency investigation (`a9041eeae8e2603bd`): 1.2k tokens, 48 tool uses, 13 min wall. Read SMOKE-TEST.md, ran live diagnostics on sapphire (with explicit "do not touch the live grid" constraint), produced `CONCURRENCY-INVESTIGATION.md`.
2. Grid restart (`a900b09abfd3554a1`): pre-restart snapshot saved → SIGINT to PID 633268 → all 18 workers gone within 30 s → relaunch under new config → verify mask + worker count → monitor first 5 cells → write `RESTART-LOG.md`. The earlier attempt (`af4524a13e1677586`) failed with API 529 before any tool calls; relaunch succeeded.
3. Speaker notes consistency QA (`a50ed4e0681bf19b7`): walked through all main slides, identified divergences between visible content and speaker notes (notably slide 5's α-posterior references after the panel was cropped; slide 7's wife/daughter narration after the example moved to 7a), edited only speaker notes, produced `qa-report-2026-05-22.md`.

**Commits.** Seven on `main`, all pushed:

1. `854d196` — captured Adela's feedback + revision plan + QA report + TRAC PDF reference
2. `47ff7ce` — deck source rewrite (qmd content + figure crops + new variance-partition figure + originals)
3. `80f3805` — rendered deck artefacts (HTML + PDF; stale slide-outline.* removed)
4. `4a54cc3` — speaker script + standalone notes (MD + PDF for both)
5. `8626726` — archive stale LaTeX paper-format slide-outline PDF
6. `cb32234` — grid concurrency investigation + restart log
7. `f4318cc` — data-profile-iterate smoke-test outputs

Plus a handoff commit `6f94bc8` (continuity + user-observations Obs 5).

**Memory captures (5 via /remember).**

- `2026-05-22-018eedaeab88` [gotcha] — SMT saturation cure (n_jobs=physical_cores + taskset pinning)
- `2026-05-22-96af8f645552` [gotcha] — matplotlib `set_title` bakes invisibly into PNGs
- `2026-05-22-48f6cf79bd4f` [feedback] — time-pressure cue → immediate explicit re-scope, not silent continuation
- `2026-05-22-81c83b4699bb` [feedback] — hardware-name scrubbing for public artefacts
- `2026-05-22-bbda749c90b1` [feedback] — minimalism = state the pedagogical principle, not just "shorter"

**User-observations addition (1).** Obs 5 — visual-scan verification is the only real review for visual deliverables. Three new data points this session (figure title bake-in; caption row-direction error; slide overflow) reinforce Obs 1.

**Wiki candidates flagged (2 in `~/personal-assistant/notes/_inbox.md`).**

- Bounded background-agent briefs with halt-and-ask discipline scaling across a session (this session = three concurrent agents, all clean).
- Three-artefact set for delegated talks (slides + bullet notes + continuous script — three cognitive moments).

**Contextual assumptions.** This session ran continuously without compaction. The talk delivery is Friday 2026-05-22 14:20 Aarhus time; Adela delivers; Shawn cannot travel. The deck PDF was sent to Adela at session close; grid runs unattended on sapphire; sapphire is on stable network and nohup process survives session disconnection. Standing rule respected throughout: all serious compute on sapphire (the grid + the investigation agent's diagnostics ran there); local-machine work limited to text edits + visual QA + light pandas / PIL / Python. Three "visual-scan verification" catches by Shawn this session continue to validate the user-observations Obs 1 + 5 pattern; my "looks fine to me" reads on rendered visual artefacts are systematically less reliable than his.

---

## 2026-05-23 → 2026-05-25 — Session log: the recovery-grid FAIL → diagnostic chain → empirical-Bayes pivot → Martin-consultation prep arc

A three-day continuous methodological arc closing the recovery-grid validation phase and opening the Stage-3 implementation phase.

### Day 1 — 2026-05-23 (grid retry + diagnosis prologue)

**What happened.** The Phase 2 recovery-grid that had been running since 2026-05-22 06:17 sapphire-local finished at 2026-05-23 12:07 — 29.84 h wall-clock vs the 31.6 h projection (~5% under). 438/450 cells completed; 12 cells failed late. Root cause of failures: `/tmp` on sapphire is tmpfs (31 GB / 1,048,576-inode ceiling); pytensor's `NamedTemporaryFile` outputs accumulated under `allow_gc=False` past the inode limit. Linux reports inode exhaustion as `ENOSPC` identically to disk exhaustion; `df -h` showed plenty of byte-space free.

**The retry.** Drain `/tmp` (1,048,559 → 17 inodes used; 5.7 s); redirect `TMPDIR` to disk-backed scratch (433 GB free on NVMe). Relaunch via `RETRY-COMMAND.sh` keeping all other config identical. Retry took 0.85 h wall; all 12 cells PASS; the failed cells had partial replicates on disk and resumed cleanly. 23,264 pytensor temp files accumulated harmlessly on the disk-backed `TMPDIR` over the retry duration — would have re-blown the tmpfs ceiling without the redirect.

**Summariser run.** `runs/2026-05-22-recovery-grid-validation/code/05-grid-summariser.py` produced REPORT.md with the binding-criterion verdict: **40.9 % of cells passing both criteria, vs the ≥ 90 % gate. FAIL.** Per-axis breakdown: α-coverage alone 63.6 %; shape-Pearson-r alone 69.8 %.

**Commits.** `3df0d2c` (close recovery grid + 12-cell retry, with RETRY-COMMAND.sh documenting the /tmp inode root cause).

### Day 2 — 2026-05-24 (four follow-up investigations + cohort design + Stages 1+2)

**Experiments A + B** (`runs/2026-05-24-validation-investigation/`, commit `3d23fe6`). Three α=0.95 cells × three sampler-effort tiers; result: posterior unchanged across effort tiers, ruling out sampler-effort as the dominant cause. Experiment B examined the flat_baseline shape's 0% pass rate; established that the model recovers near-perfectly but Pearson r is undefined on zero-variance truth — a metric-pipeline bug, not a recovery failure. (Candidate Obs 53.)

**F0 + F1 + F3** (`runs/2026-05-24-followup-systematics/`, `…followup-alpha-prior/`, `…followup-noncentred-grw/`, commit `e21f7bf`). F0 systematics analysis revealed the α-bias is bidirectional and saturates by α=0.70 — not a corner pathology at α=1 (candidate Obs 51). F1 swapped α prior to Uniform(0,1) → Δα = +0.025, below the +0.05 threshold; prior pull ruled out. F3 reparameterised GRW from centred to non-centred → Δα = +0.001 but ESS-bulk improved 45-50× and R-hat collapsed from ~1.04 to ~1.0008. Funnel geometry ruled out; non-centred adopted unconditionally as free win (candidate Obs 57). Three sequential clean-negatives localise the failure to structural identifiability (candidate Obs 52).

**Date-range threshold analysis** (`runs/2026-05-24-date-range-threshold-analysis/`, commit `b78da5c`). Histograms of LIRE v3.0 `(not_after − not_before)` revealing the slab structure: 99-y peak (47k records), 49-y peak (20k), 199-y peak (28k), 24-y small peak (857). Per-bin counts at 25 % grid alignment. Type-composition table showed the narrow-dated subset is severely type-biased: epitaphs 56 % of corpus, 11 % of <25-y subset.

**Family classifier + type-stratified narrow SPAs** (`runs/2026-05-24-type-stratified-narrow-spas/`, commit `6734ef0`). The load-bearing methodological abstraction of the session. Partition LIRE on `(not_before, not_after)` interval structure: F1_round (round-number slabs, 60.7 %), F3_periodic (decade-grid 30-y windows, 4.5 %), Tight (≤4 y, 7.8 %), F2_Other (5-48 y reign-windows, 9.6 %), Big (≥49 y non-round, 17.4 %). Cohort B = Tight ∪ F2_Other = 31,841 records (17.4 % of corpus) is the empirical-Bayes calibration cohort. F2_Other surfaced reign-window content (Antoninus Pius `AD 138–161`, tetrarchic `AD 291–325`, Hadrian `AD 117–138`, etc.) that width-only filtering would have missed. (Candidate Obs 54.)

**Discard-vs-recover rationale** (`planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`, commit `ce140d1`). Prompted by Shawn's "playing devil's advocate" framing (candidate user-observation Obs 6). Documented as a decision-tree branching on whether the empirical-Bayes pivot's Stage 4 validation succeeds.

**Stages 1 + 2 of the empirical-Bayes calibration cohort.**

- Stage 1 (`runs/2026-05-24-empirical-pconv/`, commit `a37261b`): empirical p_conv from F1+F3 inscriptions. 80-bin vector. L1 distance from the placeholder tier-template basis (pilot_proxy choice) = 0.31; ~15 % of total convention mass mis-allocated in the placeholder.
- Stage 2 (`runs/2026-05-24-empirical-pgen-prior/`, commit `8e1897b`): empirical p_gen prior from Cohort B with type-reweighting (epitaph 3.2× up; honorific 0.28× down; milestone 0.19× down; military diploma 0.18× down). Bootstrap-derived per-bin σ_prior averages 0.044 on log scale.

**Stage 3 implementation plan** (`planning/h2.1-stage-3-implementation-plan-2026-05-25.md`, commit `381c303`). Drafted by an agent; 12 sections, 5,700 words, 7 design decisions flagged for Martin.

**Five planning explainer docs** (commit `b78da5c`): `h2.1-mixture-model-problem-explained-2026-05-24.md`, `h2.1-follow-up-candidates-2026-05-24.md`, `h2.1-prior-art-scout-empirical-bayes-calibration-2026-05-24.md`, plus the discard-vs-recover rationale and the Stage-3 plan. Pitched in the non-specialist register Shawn approved and captured as memory `2026-05-24-e6ec8f9174f1`.

**Martin consultation pack** (`planning/martin-consultation-2026-05-25-followup.md`, commit `e57dc6b`). Six framed questions for the consultation; supersedes the four questions in the Experiment A/B diagnostic report. Compiled alongside the Stage-3 implementation plan and the planning explainers.

### Day 3 — 2026-05-25 (Martin consultation prep + two scouts + working-notes review)

**Martin consultation briefings** (`runs/2026-05-25-martin-consultation-prep/`, commits `55e050c` + `dbae06f`). Main briefing (7-section pre-meeting brief) + supplementary briefing (covers the 8 unanswered 2026-05-17 pack questions, 3 new findings, H3b/H3c/§5 backlog, strategic decisions). Four key figures: uncorrected SPA, slab-highlighting SPA (new, stacked-by-family), slab-excluding SPA (new, reweighted-prior overlay), Hanson NBR scaling. Per-region editorial-fraction analysis revealed AD 300-350 is 80 % editorial templates (template-dominated late corpus).

**Lit-scout — pottery-aoristic Roman bibliography** (`planning/lit-scout-2026-05-25-pottery-aoristic-roman/`, commit `3e93660`). Closed-loop iteration via `/lit-scout-iterate`: iter-0 returned 25 references with 26/27 PASS + 1 FAIL (two citation_count confabulations on rows 24-25, value-reuse pattern). Iter-1 applied corrections; all 27 PASS. 15 new items imported to Zotero staging; 8 already in libraries (SDAM-AU + roman_demography); 2 OXREP chapters required hand-curation from OpenAlex + Semantic Scholar because CrossRef returns 404 on OUP `acprof:oso` DOIs (commit `b687ed2`). Headline finding: the Brughmans / Aarhus cluster (Komar/Brughmans/Borisova 2025, Franconi et al. 2023, Bevan et al. 2013) is the bridging community between radiocarbon-SPD methodologists and epigraphy-aoristic.

**Prior-art-scout — ceramics-aoristic actionable techniques** (`planning/prior-art-scout-2026-05-25-ceramics-aoristic-techniques/`, commit `6877621`). Closed-loop iteration via `/prior-art-scout-iterate`: iter-0 returned 15 candidate techniques with 1 FAIL on a DOI confabulation (Bellanger & Husi 2012, off by six digits — `.12.039` resolved to a paleoindian dental microwear paper; correct DOI `.06.031`). Iter-1 applied correction; all 27 claims PASS. Identified 6 directly-adoptable + 4 to-adapt + 5 to-ignore techniques. Sharpened the methodological-novelty claim: the LIRE p_conv/p_gen decomposition is genuinely novel; ceramicists use sensitivity stratification not structural decomposition.

**Continuity update + post-Martin action items** (commit `88f7c93`). Added a "Post-Martin / methodology-refinement action items" section to continuity.md with the 6 directly-adoptable + 4 to-adapt techniques from the prior-art scout. Added session-history entries for 2026-05-23, 2026-05-24, 2026-05-25. Added a "Working-notes review — in flight" section flagging the gap-analysis agent.

**Working-notes gap-analysis agent** (commit `11ca91e`). Background agent reviewed recent runs/commits and proposed 9 Obs entries (49-57) covering the 2026-05-23 → 2026-05-25 gap. Inventoried 12 candidate topics, proposed 9 (skipped 3 for overlap-with-existing-Obs or planning-artefact-status). Proposals at `docs/notes/reflections/PROPOSED-OBS-49-57-for-review.md` for Shawn's selective commit.

**`/handoff` session-close** (commit `6fda233`). Updated continuity.md (working-notes-review section now references the proposal file); appended 4 new user-observations (Obs 6-9) — devil's-advocate prompting (Obs 6); verify-before-contradicting-agent (Obs 7); explicit scope-out clauses (Obs 8); in-session `/remember` is immediately load-bearing (Obs 9). Committed Shawn's raw Martin consultation notes at `planning/martin.md`. Five wiki candidates flagged to `~/personal-assistant/data/notes/_inbox.md` (separate `pa-data` submodule, commit `63c75ec`).

### Artefacts touched

**New runs.** `runs/2026-05-24-validation-investigation/`, `…followup-systematics/`, `…followup-alpha-prior/`, `…followup-noncentred-grw/`, `…date-range-threshold-analysis/`, `…type-stratified-narrow-spas/`, `…empirical-pconv/`, `…empirical-pgen-prior/`, `runs/2026-05-25-martin-consultation-prep/`.

**New planning docs.** `planning/h2.1-mixture-model-problem-explained-2026-05-24.md`, `h2.1-follow-up-candidates-2026-05-24.md`, `h2.1-discard-vs-recover-rationale-2026-05-24.md`, `h2.1-prior-art-scout-empirical-bayes-calibration-2026-05-24.md`, `h2.1-stage-3-implementation-plan-2026-05-25.md`, `martin-consultation-2026-05-25-followup.md`, `lit-scout-2026-05-25-pottery-aoristic-roman/`, `prior-art-scout-2026-05-25-ceramics-aoristic-techniques/`, `martin.md`.

**Updated docs.** `docs/notes/reflections/continuity.md`, `docs/notes/user-observations.md` (Obs 6-9), and at session-close `docs/notes/reflections/{session-reflection,reasoning-log,abductive-reasoning,session-log}.md`.

**Proposals pending review.** `docs/notes/reflections/PROPOSED-OBS-49-57-for-review.md` (9 candidate Obs entries from the gap-analysis agent).

### Commits in arc

`3df0d2c` (grid retry close) → `3d23fe6` (Experiments A+B) → `e21f7bf` (F0+F1+F3) → `e57dc6b` (Martin pack) → `b78da5c` (planning explainers + threshold analysis) → `6734ef0` (family classifier + cohort comparison) → `ce140d1` (discard-vs-recover rationale) → `a37261b` (Stage 1 empirical p_conv) → `8e1897b` (Stage 2 empirical p_gen prior) → `381c303` (Stage 3 plan) → `55e050c` (Martin briefing + figures) → `dbae06f` (supplementary briefing) → `3e93660` (lit-scout) → `b687ed2` (OXREP bib hand-curation) → `6877621` (prior-art scout) → `88f7c93` (continuity update with action items + session history) → `11ca91e` (proposed Obs 49-57) → `6fda233` (handoff bundle).

### User-observations addition (4)

- **Obs 6** (2026-05-25): explicit "devil's advocate" framing produces more rigorous analysis than open prompts. Anchor: discard-vs-recover rationale at commit `ce140d1`.
- **Obs 7** (2026-05-25): when I doubt an agent's output, verify against source before contradicting. Anchor: Stage 3 implementation-plan filename mis-flag at commit `381c303`.
- **Obs 8** (2026-05-25): explicit scope-out clauses make scope-honesty easier near session-end. Anchor: working-notes gap-analysis ask.
- **Obs 9** (2026-05-25): in-session `/remember` captures are immediately load-bearing, not just future-facing. Anchor: register-preference memory `2026-05-24-e6ec8f9174f1`.

### Wiki candidates flagged (5 in `~/personal-assistant/data/notes/_inbox.md`)

- Three cheap diagnostic negatives in sequence localise a Bayesian-model failure to its mechanism.
- Bridge-the-clusters lit-scout: disconnection-as-signal heuristic (refines an earlier observation; observed twice now).
- Empirical-Bayes calibration cohort as a methodology pattern for breaking structural unidentifiability.
- tmpfs inode exhaustion as silent killer for long Bayesian compute runs.
- Non-specialist register / explainer-pattern preference (already memory-captured; promotion candidate to `notes/working-with-claude.md`).

### Contextual assumptions

The recovery-grid FAIL is being framed as the validation gate doing its job, not as a setback. The empirical-Bayes pivot is the project's second structural redesign driven by validation-gate output (after the 2026-04-26 forward-fit pivot). Martin's consultation on 2026-05-25 produced notes at `planning/martin.md` — short, unstructured, capturing his HMM-framing direction and a "use granular to characterise slabs" idea that aligns with our empirical-Bayes approach. Whether he addressed the eight 2026-05-17 pack questions is not yet clear from his notes; the post-Martin action items in continuity.md may need re-prioritising once his input is processed. All sapphire compute completed cleanly; all 18 commits this arc are on `origin/main`; working tree clean at handoff. The session ran continuously without compaction.

---

## 2026-05-26 — Letter-count probe complete; recovery-grid two-unit launched; "acts vs content" reframe locked

Single-day session, continuous (no compaction). Opened with the post-Martin recalibration in train (3 planning files + continuity 2026-05-25 history block to fix from "Drechsler" to "Eftimoski"). Closed with the letter-count probe complete, six commits of substantive work landed plus ~16 of supporting infrastructure, the recovery-grid two-unit re-simulation running on sapphire, and the working-notes register caught up (Obs 49-60 all landed).

### Headlines

- **Letter-count probe complete.** Six blocks executed: 01 letter-count computation; 02 empire SPA shape comparison; 03 province/city rank shuffles; 04 Hanson NBR; 05 frequentist Mundlak; 06 Bayesian Mundlak on sapphire. REPORT at `runs/2026-05-26-letter-count-probe/REPORT.md` (commit `348ea25`). Three flags evaluated: Flag 1 (SPA shape) MODEST; **Flag 2 (Hanson β) MATERIAL** (no CI overlap; β 0.566 → 0.515); **Flag 3 (f_within) MATERIAL** (+9.89 pp; 29.94 % → 39.83 %).
- **"Acts vs content" reframe locked** (Obs 58, commit `dd326dc`). I coined the construct-distinction in Block 3's substantive writeup; Shawn extended it to "complementary measures with delta as research object, analogous to scaling-residuals." Reshapes Stage 3 (parallel fits under both units), the recovery-grid re-simulation (two grids head-to-head), and the methodology paper's argument structure.
- **Mundlak corroboration** (Obs 59, commit `de8fa8f`). Bayesian fits on sapphire matched talk-prep slide-6 punchline at 29.94 % for inscription-count (sanity-check); +9.89 pp shift to 39.83 % under letter-mass. Mechanism: β_between centres toward zero (−0.248 → −0.158); denominator shrinks faster than numerator.
- **`pilot_proxy` template-tier corroboration** (Obs 60, commit `2f86c95`). Letter-mass re-derivation shifts the tier vector from (0.55, 0.30, 0.15) to (0.5230, 0.0733, 0.4038) — reign-interval mass quadruples; half-century mass collapses; century mass roughly stable. Letter-weighting elevates reign-dated formulary epigraphy (imperial titulature, military diplomas, full dating apparatus).
- **Recovery-grid two-unit re-simulation running** (`runs/2026-05-26-recovery-grid-two-unit/`; spec commit `507a722`). Two grids head-to-head — inscription-mass + letter-mass conservative, both with F1 + F3 structural fixes baked in. Production launched on sapphire PID 931910 at 2026-05-26 05:53 UTC; ETA ~ 76 h sequential; STATUS.txt at the spec'd path is the polling side-channel.
- **Working-notes batch intake.** 9 proposed Obs 49-57 landed in recommended order (commit range `43d814d..65edb2e`); `PROPOSED-OBS-49-57-for-review.md` staging file deleted; working-notes is now at Obs 60.
- **HMM follow-up paper stub** created at `planning/hmm-paper-stub/` (commit `dad1fcd`). One-page placeholder; substantive work deferred until current paper closer to draft.
- **Name correction** (commit `f3e5322`). Three planning files + continuity 2026-05-25 history block: "Martin Drechsler" → "Martin Eftimoski." Memory `2026-05-26-214ce5ca1491` captures the corrected profile.

### New / updated runs

- `runs/2026-05-26-letter-count-probe/` (six code scripts; outputs; REPORT)
- `runs/2026-05-26-recovery-grid-two-unit/` (spec; harness in `code/`; pre-launch gate artefacts; pilot_proxy artefacts per grid)

### New planning docs

- `planning/hmm-paper-stub/README.md`

### Updated docs

- `docs/notes/reflections/continuity.md` (Martin-recalibration section + priority queue + working-notes section + 2026-05-26 session-history entry)
- `docs/notes/reflections/working-notes.md` (Obs 49-60 landed)
- `docs/notes/user-observations.md` (Obs 10-12 added; see below)
- `docs/notes/reflections/{session-reflection, abductive-reasoning, session-log}.md` (at session close)
- Three `planning/h2.1-*.md` files: name correction
- `.gitignore`: added `lire-filtered-with-letters.parquet` exclusion; recovery-grid-two-unit per-replicate exclusions

### Commits in arc

`dd326dc` (Obs 58) → `21a80c0` (block-6 script setup) → `f3e5322` (name correction + continuity recalibration) → `26ab70e` (letter-probe blocks 1-5) → `507a722` (recovery-grid spec) → `de8fa8f` (Obs 59) → `49957a7` (Mundlak result outputs) → `348ea25` (REPORT.md closes probe) → `16c8c88` (recovery-grid harness) → `8925126` (pre-launch gate artefacts) → `65756ac` (wrapper smoke-summary fix) → `dad1fcd` (HMM stub) → `43d814d..65edb2e` (Obs 49-57 batch intake + cleanup; 10 commits) → `2f86c95` (Obs 60) → `25f655d` (continuity handoff). ~ 22 commits; all pushed to `origin/main`.

### User-observations addition (3)

- **Obs 10** (2026-05-26): Substantive intellectual contributions need accurate attribution; under-claiming erases what I bring to co-research. Anchor: the "acts vs content" coinage in Block 3 writeup + Shawn's credit-correction at session-close. Memory `2026-05-26-652990d9d646`.
- **Obs 11** (2026-05-26): Pause and surface methodologically-different metrics before committing; "lab-not-dev-team" working as designed. Anchor: Block-5 frequentist Mundlak f_within ≈ 95 % vs Block-6 Bayesian ≈ 30 % (different denominators).
- **Obs 12** (2026-05-26): Substantial spec docs can evolve mid-session as findings accumulate; don't lock too early. Anchor: recovery-grid two-unit spec evolved through three design expansions across the session.

### Wiki candidates flagged (3 in `~/personal-assistant/notes/_inbox.md`)

- Binary verdict thresholds force false choices when alternatives are different constructs rather than rival operationalisations — candidate for `llm-craft.md` or new `notes/sensitivity-probe-design.md`.
- Long sapphire-job orchestration pattern (agent launches under nohup, captures remote PID, writes STATUS.txt side-channel, exits with PID + STATUS reported; main thread polls via direct SSH) — candidate for new `notes/agent-orchestration.md`.
- Agent anti-confabulation catches brief errors when a brief carries specific factual claims; cascading anti-confabulation discipline from briefing to execution — candidate to extend `llm-craft.md`.

### Memories captured this session (3)

- `2026-05-26-214ce5ca1491` (contact): Martin Eftimoski profile + correction from "Drechsler."
- `2026-05-26-40ce5927fddc` (feedback): amendment-gate rule — flag before launching work whose published claims need a not-yet-lodged OSF amendment.
- `2026-05-26-652990d9d646` (feedback): take credit honestly for substantive contributions; default to claiming; Shawn corrects over-claiming; the error-mode is under-claiming.

### Contextual assumptions

The session opened with the Bayesian Mundlak's actual wall-clock (4.3 min) substantially below my pre-launch estimate (45 min) — the harness is well-tuned and my estimates were conservative. The recovery-grid two-unit launch authorisation was gated explicitly on Mundlak completion (per spec §10 Decision 4); that trigger fired at 02:56 UTC; harness-prep agent dispatched 4-5 h later (after Shawn's session re-engagement) with the spec's launch authorisation already locked. The Mundlak agent's dropped completion notification (documented failure mode) was handled by direct SSH check when Shawn asked for status — no friction. All session work happened on amd-tower; sapphire is doing the production compute under nohup. The harness-prep agent flagged the wall-clock estimate from spec §6 (~ 60 h) as too optimistic and reported ~ 76 h based on smoke-test timings; the deviation was surfaced rather than relaxed. Working tree clean at handoff; one outstanding state: sapphire's working tree diverges from `origin/HEAD` in the smoke-cell artefact deletions (intentional, per the harness's resumability skip logic; sapphire never pushes). All ~ 22 commits this session are on `origin/main`.

---

## 2026-05-29 → 2026-06-01 — §5 Layer-A concept-to-production, OSF Amendment 01, two /audit cycles

**Done / produced.**

- Grid-B status corrected (parallelism-double-counting ETA bug; true ~3 June). zbook upgraded to sapphire parity (pymc 6.0.1 / pytensor 3.0.3 / arviz 1.1.0) and made the §5 compute host.
- **OSF Amendment 01** drafted (`planning/osf-amendment-2026-05-29-two-measure-framework.md`): parallel-co-registered two-measure framework; Martin/statistician references scrubbed; figures corrected pre-lodgement per audit (`b5b39dc` → `4fad07b`).
- **Letter-mass design effect** quantified (`scripts/letter-mass-design-effect.py`, `letter-mass-reachability.py`, `audit-verify-rome-and-deff.py`): per-city DEFF ≈ 2.4; 0 of 1,044 urban-area cities reachable. Obs 61 (`107226b`), corrected by Obs 62 (`805c991`).
- **§5 Layer-A built**: spec + open items resolved (`85c76a1`/`e687ecd`/`41cb028`); single-city + hierarchical smoke validated (`27b3576`/`a265074`); production infra + tracked launch wrapper (`a0ccf79`/`f5927b8`); two audit remediations (`2c82a87`/`687b96e`).
- **Production run** on zbook (~5.7 h); crashed at Step 3 on an undeclared `scikit-learn`; fixed (`62f3266`) via `finish_diagnostics.py` (re-ran Step 3 only, from the saved posteriors).
- **§5 results** (`eb3aef3`, `RESULTS.md`): primary inscription-25y PASSED (R̂ 1.0000, ESS 2571); 3 marginal fits at R̂ 1.0100 accepted-with-caveat; calibration **N\*=300**; Pompeii AD-79 post-79 mass 0.12 %; 6-cluster trajectory grouping. Obs 63 (`0dc72ad`) + Obs 64 (`dfd873e`).
- **Handoff**: continuity updated (`628f801`); user-obs 13–15 (`8225c21`); craft candidates flagged to `~/personal-assistant/notes/_inbox.md`.

**Open at session close.** OSF Amendment 01 lodgement (Shawn's action — Stage-3 gate); Grid B → cross-grid comparison + Stage-3 decision (~3 June); §5 Layer B (needs H3a `β_within`); dependency-hygiene follow-up (task #9); ceramics-aoristic diagnostics (task #6).

### Contextual assumptions

§5 Layer A is *exploratory* (not Stage-3 confirmatory), so it needed no amendment gate to run — that is why it could proceed while the amendment sits un-lodged. The four `.nc` posteriors (3.6 GB) are a **single copy on zbook** (Layer B's input); single-copy risk explicitly accepted by Shawn until Layer B runs. The run used `target_accept=0.99` (the non-centred RW funnel needs it); the three marginal R̂=1.0100 fits escalated once and still landed on the strict `<1.01` boundary — accepted for exploratory work. The production crash was an *undeclared* dependency (`scikit-learn` absent from `pyproject.toml`) on a venv built ad-hoc rather than via `uv sync` — drift, not a code bug. Grid B left entirely untouched on sapphire throughout (Shawn's instruction). ~25 commits, all on `origin/main`.

## 2026-06-02 — §5 posterior backup + dependency-hygiene (pymc-6 standardisation), PR #5

**Done / produced.**

- **§5 posteriors backed up** zbook → `rpi-server:/mnt/qnap/shawn/Backups/inscriptions-research-data/2026-05-30-s5-small-n-trajectories-posteriors/` (3.69 GB, 4 `.nc`); sha256-verified identical on both ends; `MANIFEST.md` + `MANIFEST-sha256.txt` written. Single-copy risk closed (an accepted risk at last session's close).
- **Task #9 dependency hygiene** (PR #5, rebase-merged to `main` `4df6d47..ad3457b`): `uv.lock` refreshed to the validated pymc-6 stack (pymc 6.0.1 / pytensor 3.0.3 [pinned via `[tool.uv] constraint-dependencies`] / arviz 1.1.0 / scikit-learn 1.8.0); `h5netcdf` + `h5py` added as direct deps (the arviz-1.x optional-backend fix); `preflight.py` added (import check + real `xarray→h5netcdf` round-trip) and wired into `run-production.sh` + a `--check-env` flag; `--resume-diagnostics` flag added to `orchestrate.py` (generalises `finish_diagnostics.py`, archived to `archive/superseded-code/2026-05-30-s5-small-n-trajectories/`); `PROVISIONING.md` added.
- **Validation**: fresh `uv sync --frozen` env read a real §5 posterior (zero version drift vs zbook's freeze); three-agent `/audit` — no Critical findings, 8 robustness/accuracy fixes applied; end-to-end `--resume-diagnostics` on zbook (symlink copy, production untouched) reproduced the committed summary **bit-for-bit** (anchor r `|diff|=0`, Pompeii 0.001179, N\*=300).
- **Observations**: Obs 65 (arviz-1.x optional netCDF backend), Obs 66 (pymc-6 §5 vs pymc-5.28 recovery-grid stack split); user-obs 17 (decompose a default's reasoning rather than default to momentum). zbook + amd-tower both synced to `main @ ad3457b`, pymc-6.
- **Handoff**: continuity updated; inbox flag (arviz-1.x trap) committed in the `data` repo; memory captured (direct-on-`main` norm for solo repos).

**Open at session close.** OSF Amendment 01 lodgement (Shawn, today/tomorrow — Stage-3 gate); sapphire pymc-6 upgrade (`uv sync --frozen`, after Grid B finishes, never mid-run); cross-grid comparison harness + Stage-3 decision (~3 June, fresh session). Grid B ~81 % (366/450), 0 failures, ETA ~3 June. Deferred: Grid A output backup (lower priority — reproducible simulation); whether sapphire's arviz-0.23 can read the §5 arviz-1.1 `.nc` (untested — flagged).

### Contextual assumptions

Branched + PR'd the migration, which Shawn corrected as over-ceremony for solo research repos (direct-on-`main` is the norm; memory captured) — the PR was rebase-merged to keep history linear, branch deleted. The pytensor 3.0.3 pin is deliberate (reproducibility over the one-patch-newer 3.0.4 a clean resolve picks). The e2e ran against a symlink copy with the committed summary checksummed first, so production results were provably untouched; test outputs deleted after confirmation. amd-tower can read posteriors but cannot *fit* (no Python 3.13 dev headers, so pytensor cannot compile) — relevant only if it is ever used as a compute host. Grid B left untouched on sapphire throughout. ~7 commits across the session, all on `origin/main` (plus 1 in the `data` repo for the inbox flag).

## 2026-06-02 → 2026-06-03 — Grid A adjudicated (FAIL) → criterion clarification, utility review, subset reframe, small-N reachability

**Done / produced.**

- **Grid A (inscription-mass) adjudicated — FAIL.** Built generalised per-grid summariser (`grid-summariser.py`) + cross-grid comparison harness (`compare-grids.py`) + `collect-alpha-bias.py` + `finalise-comparison.sh` + `comparison/RUNBOOK.md`; smoke-tested A-vs-A. Verdict: coverage 69.8%, shape-r 70.2%, both-pass 42.7% (vs 40.9% in 2026-05-22 — F1+F3 only marginal). Failure decomposed: (i) Pearson r undefined for flat_baseline (75 cells, caps shape-pass at 83.3%); (ii) exact α-coverage collapses at large N at near-constant tiny bias (BvM artefact). `p_gen` shape recovers (r≈0.998) throughout. REPORT + `grid-summary.parquet` + `alpha-bias.parquet` committed.
- **Prior-art scout + `/review-implementation`** on recovery-validation metrics. Scout (verified, 15/17 PASS, 2 bibliographic fixes): no surveyed community gates on exact CI-coverage of a mixing weight; flat is a standard tested null; W1 theoretically justified (Rousseau & Scricciolo 2021); record at `planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`. Review found SBC doesn't fit a fixed-true-value grid; z-score shares the large-N fragility; a global W1 threshold is shape-unfair (→ hybrid patch).
- **Decision 33 + OSF Amendment 01 §A5.5.1** (criterion clarification): hybrid shape gate (Pearson r ≥ 0.95 non-flat unchanged; W1 ≤ T_flat=10y flat); convergence precondition explicit; **α demoted from binding gate to quantified diagnostic** (90th-pct |bias| ≈ 0.18); operating-envelope / recoverability reframe (α ≤ 0.70). Grid A preview under corrected criterion: **91.9% PASS** in the operating envelope.
- **Utility review** (`planning/recovery-grid-utility-review-2026-06-02.md`): four confirmations (principled / literature / good-practice / uncertainty-presentation) + two diagnostics. **(a) band calibration** (re-fit 12 cells×30 reps, zbook): p_gen band honest for smooth signals (~0.99) but overconfident for peaked ones, degrading with N (regnal_cluster 0.23 at N=50k) — report median, not band, in peaked regimes. **(b) real-corpus convention fraction**: corpus-wide ≈0.65 (just inside envelope) but >0.70 across AD ~142–347 (late corpus in degraded zone). `runs/2026-06-02-recovery-utility-check/`.
- **Decision 34** (subset mechanism): subset analyses use **subset-specific** deconvolution; the empire-wide `p_conv` is NOT imposed on subsets. Settles the under-specified H3b mechanism; amendment-relevant. **Significance/applications note** (`planning/paper-significance-and-applications-2026-06-03.md`): the paper-facing "why" (core re-application case = subset temporal de-fogging; empire-scale apps; three-part "why bother" answer).
- **Small-N reachability study** (`runs/2026-06-03-small-n-reachability/`): spec + driver (`reachability.py`, learns convention per-subset) + report-generator, smoke-tested; full run (84 cells × 50 reps) launched on zbook to measure the minimum-N floor. **Blocked**: zbook overloaded (`n_jobs=16` → swap-thrash → dropped off network at 99.5% complete); floor result pending zbook recovery next session.
- **Housekeeping**: 449 untracked Grid A cell-summary JSONs gitignored (content preserved in `grid-summary.parquet`); diagnostic logs/scratch gitignored; `reachability.py` default `n_jobs` → `min(14, cpu_count−4)`. Memory captured (`2026-06-03-08277f53bdc5`, the n_jobs gotcha).

**Open at session close.** Reachability floor (pull from zbook → `make-reachability-report.py` → figure+REPORT → wire into significance doc + Decision 34) — *first next-session item*. Grid B finishing on sapphire (441/450 at close) → cross-grid comparison + harness update to the Decision-33 criterion (RUNBOOK). OSF Amendment 01 lodgement (Shawn; now carries §A5.5.1 + Decision 34). Martin draft-stage sign-off (α-diagnostic + envelope cut). Deferred fit-side to-dos (informed α prior; roughness-tolerant p_gen prior) logged in backlog.

### Contextual assumptions

The session spanned 2026-06-02 (resume, after the dependency-hygiene session) into 2026-06-03. The 91.9%-PASS preview used a bias-tolerance proxy for the α-calibration gate (conservative; the tolerance-coverage variant converges with it at large N) and the hybrid shape gate, computed from stored posteriors — no re-fit. Band-calibration + reachability fits ran on zbook under pymc 6.0.1 vs the grid's pymc-5.28 (model identical; calibration transfers — flagged). The amendment is drafted, not lodged — Stage-3 work stays gated. The reachability run is a `nohup` process: the zbook network drop did not kill it; results write to disk at completion and are safe once zbook is reachable. ~10 commits, all on `origin/main`.

## 2026-06-03 → 2026-06-04 — reachability floor → Stage-3 adjudication → field-standard criterion → lodge-ready amendment

**Reachability floor (the handoff's first action).** zbook had rebooted; the original small-N run was unrecoverable (no checkpointing — 4,189 in-memory fits lost). Added a resumable JSONL checkpoint to `reachability.py` (`a0458fa`), smoke-verified, re-ran on zbook (n_jobs=14, 4,200 fits, ~25 min). **Floor measured:** within α ≤ 0.70, worst-case **N ≈ 2,000**; as low as ~500 for easy (low-α, simple-shape) subsets; α = 0.70 partly unreached, α = 0.85 unreached. Wired into the significance note + Decision 34 (`5601b04`).

**Stage-3 cross-grid adjudication.** Grid B (letter-mass) finished on sapphire (`GRID-B-END rc=0`, 0 failures). Updated the harness (`grid-summariser.py`, `compare-grids.py`) to the Decision-33 / §A5.5.1 corrected criterion alongside the lodged one (`4aa837b`, `1bf791f`). **Verdict: inscription PASS / letter FAIL → Stage 3 under inscription-mass only.** Grid B fails on convergence (no cell ≥ 0.90; R̂/ESS, not just divergences).

**Field-standard criterion refinement (the session's pivot).** The corrected-criterion A-vs-B gap (91.9 % vs 98.5 %) traced to a zero-tolerance divergence gate. A literature scout (Stan/Betancourt) + direct re-score established the flat-null divergences are benign (Mann–Whitney p ≈ 0.36; all 24 cells pass R̂/ESS). Changed the gate to field-standard benign-tolerant (`fit.py`); **Grid A re-scores to B = A = 98.6 %**, flat-null limitation dissolved, backlog re-fit retired. α-diagnostic reframed to Bland–Altman limits of agreement, shape-conditioned. A finer-α run (sapphire) confirmed α ≤ 0.70 as the operating-envelope cut (gradual, shape-dependent decline above it).

**Amendment (OSF Amendment 01).** Fully encoded the 2026-06-04 findings into §A5.5.1 + §A5.7; added a plain-language summary; reframed A7 as a fresh section-keyed upload (not in-place edits); stripped internal-tooling / statistician / mother–daughter references for external readers (`efbcd9c`, `270faea`). **Lodge-ready** (Shawn lodging it).

**Grounding + bibliography.** Wrote the statistical-grounds memo for the four flagged decisions (data + SME framing + recommendations). Verified 12 sources (CrossRef/arXiv; corrected Modrák → 2025, Crema → 2020-online); staged to My Library > staging > `2026-06-04-bayesian-workflow-conventions-divergences-recovery` (12/12; script `524ea32`).

**Infrastructure.** Both compute hosts (sapphire 72-behind, zbook 27-behind) caught up to `main` via verified `git reset --hard` preserving gitignored outputs. Corrected a stale 5-replicate Grid B exemplar to the real 100-replicate value.

### Contextual assumptions
- The amendment's 98.6 % is verified by direct re-score from stored per-replicate R̂/ESS (no re-fit). The committed harness still emits 91.9 % (old cell-summaries); making `grid-summariser`/`compare-grids` reproduce 98.6 % in-pipeline (re-aggregate cell-summaries under the new `fit.py` gate) is the deferred next step. Decision 33 / Obs 67 still cite 91.9 % as historical and want a 2026-06-04 annotation.
- zbook's live memory split (32 GB VRAM / 94 GB RAM) contradicts the network-resources doc; possibly altered by the power-cycle — flagged for Shawn's BIOS check.
- sapphire is now on pymc 6.0.1 (talk-prep venv); the grids ran on 5.28 — committed-artefact provenance unchanged.

## 2026-06-05 → 2026-06-06 — H2.1 prerequisite scan → genuine/conventional settled (Decision 38) → lit-scout grounding → tooling hardening + hygiene

Resumed inscriptions at the H2.1 prep gate. The session settled the genuine-vs-conventional question and hardened/cleaned the literature-and-Zotero tooling.

**Template-dictionary scan (the H2.1 prerequisite).** Built + ran `runs/2026-06-05-template-dictionary/` (`6d8950f`): empire (180,609) + Latin (109,646, reproduced exactly) exact-template enumeration. Found the curated 3-tier convention basis empirically inadequate — multi-century slabs ~31% of the convention pool and absent; reign ~2.7%; `[301,500]` the single most frequent template (8.8%). Reconciled the family classifier (F1/F2_Other/F3/Tight/Big), the Stage-1 9-slab empirical p_conv, and a lodged-prereg reign contradiction via fan-out explore agents.

**Decision 38 (`66e751a`).** Historical-anchor principle (reigns/dynasties/events → genuine-but-aoristic; calendar-segment rounding → convention); grid-quantisation reframing of "convention"; convention basis = empirical calendar slab-types grouped to ~3 tiers, **no reign tier**; decadal + quarter-century as a sensitivity band; **recovery re-validation now precedes H2.1** (the 98.6% does not transfer); cite-and-distinguish novelty positioning; OSF amendment required (separable from Amendment 02). Supersedes Decision 20's tier typing; refines Decision 37.

**Lit-scout (verified) + two deeper chains.** `/lit-scout` proposer+verifier (19 rows, clean) + a Crema-2025 forward chain + an EDH-heiDOK backward chain (both verified). Novelty survives the pre-emption check; nearest competitor = Tobalina-Pulido & Martín-Rodilla 2026 (`10.5334/jcaa.220`, fuzzy-logic uncertainty *quantification*, not deconvolution). Warrant = Crema 2025; dating-method authority = Cooley 2012 + Hartmann 2025. EDH Datierungskriterien = cite-the-data (`zenodo.3575154` + Grieshaber + EpiDoc Guidelines; the EpiDoc `@evidence` list maps ~1:1 onto the EDH criteria).

**Zotero staging.** 9 epigraphic-dating references staged to `My Library > staging > 2026-06-06-epigraphic-dating-methodology` (`5c6cddd`, `e94b240`, `c2a6ea9`).

**Tooling hardening (personal-assistant).** `lit-search.py` 429 retry/backoff + per-host pacing (`fbe743c`, pushed to main). Importer `lit-scout-zotero-import.py` 429 resilience + explicit DataCite source (chain CrossRef→DataCite→OpenAlex, DataCite authoritative for datasets): implemented on a worktree-isolated branch (`2140b21`, 83 assertions), reviewed, merged to personal-assistant main (`6d25850`).

**Tooling hygiene (inscriptions).** Archived the five bespoke Zotero staging one-offs to `archive/superseded-code/zotero-staging/`; created `inscriptions/CLAUDE.md` externalising the canonical shared tooling + the correct pattern + its known gaps; fixed the README's stale mention (`ca974d3`).

### Contextual assumptions
- Two parallel sessions were live: Shawn's warm-context review of the scan (which caught two errors in my fresh-session proposal — threshold-routing contamination and spot-check-vs-re-validation) and another branch (`fix/litscout-zotero-arxiv-doi`) Shawn merged mid-session. personal-assistant was under concurrent auto-sync (main advanced during agent runs); every agent commit was re-verified at source and scoped with explicit pathspecs.
- Semantic Scholar rate-limited (HTTP 429) repeatedly across the session — the motivation for the retry/pacing work.
- H2.1 remains gated: still pending are the curated historical-anchor interval list, the empirical calendar-slab basis rebuild, the recovery re-validation (α=0.95 × multi-century stress-triage first), and the OSF amendment. Parked: the EDH dating-criteria enrichment (awaiting SDAM reply) and OSF Amendment 02 (Latin frame).

## 2026-06-06 → 2026-06-07 — Decision-38 gate executed → re-validation triage PASS + full grid launched → OSF Amendment 02 LODGED → H2.1 launch-prep drafted

Resumed inscriptions at the H2.1 prep gate and executed the Decision-38 redesign end to end, lodged Amendment 02, and staged the H2.1 launch.

**Decision-38 basis built (Option 2).** Shawn chose 3 learned tiers from the 5 core calendar slabs (sub-century [half-50] / century / multi-century [150+200+300]); the 4 fine brackets excluded from primary `p_conv` → add-them-back sensitivity band. Built the curated historical-anchor list (`historical-anchor-intervals.json`) and the empirical, frequency-weighted, per-frame basis (`design.json`, empire + Latin); reign leak = 129 (`[161,180]`, 0.11%) stripped; empirical tier weights [0.184, 0.431, 0.385]. `runs/2026-06-06-convention-basis-redesign/` (`6e1354b`).

**Recovery re-validation.** Wrote the spec (stress-triage first; `75e9088`). Stage-1 triage (8 cells, sapphire) PASS: convergence 1.00; α recovered to +0.029 at the worst corner — the multi-century plateau is attributed to convention, not confused for genuine quiescence (Decision-38 §6 fear resolved). The one sub-0.90 α-coverage cell was the benign large-N collapse Amendment 01 §A5.5.1 already documents; corrected the spec gate to the Amendment-01 criterion (α = diagnostic; shape + convergence binding) (`f90e6c1`, `d93598c`; `STAGE1-TRIAGE-REPORT.md`). Shawn signed off → full grid (450 cells, fresh harness copy, PID 1681813) launched; ~144/450 at close, 0 failed.

**OSF Amendment 02 (Latin frame) LODGED 2026-06-06** (tag `osf-amendment-02-2026-06-06`). Prepared the 4-artefact package mirroring A01 (`c4c40dc`; word-wrap fix for OSF pasting `472f146`; LODGED status `ce963de`). Resolved the 39-vs-41 province reconciliation from evidence (`runs/2026-06-06-amendment-02-prep/`, `d82834c`): Italia (N=1) + Alpes Graiae (N=77) classify Latin but contribute 0 Hanson-matched cities → realised frame 817/39, no result impact; Lugdunensis→Lugudunensis spelling. Decision 36 gate cleared; 14 PRELIMINARY labels flipped to confirmatory across 6 Latin result artefacts (`ebbf332`). Generalised the PDF builder to read its title from frontmatter (`86dead0`).

**Git tidy.** Extended `.gitignore` to the revalidation run dir per the 2026-05-26 heuristic (bulk ignored; grid-state + REPORT + 8 triage summaries tracked); repo 0 untracked (`c32f0a7`).

**H2.1 launch-prep** (`runs/2026-06-07-h2.1-launch-prep/`). Verified + pinned the unit set: 26 primary fits (empire 180,609 + Latin 109,646 + 19 provinces + 5 cities at N≥2,000; grey-band Moesia inferior + Lusitania), matching Decision 37 D1 exactly (`1e11414`). Drafted the H2.1 launch spec (`9f00f26`) and the Amendment 03 convention-model skeleton (`edf4cd9`), both with grid-dependent sections placeheld. Updated continuity (`a8369d5`).

### Contextual assumptions
- The full grid runs on sapphire independently of the session; its verdict (the H2.1 gate) was still pending at close. ETA ~12 h total — much faster than the spec's conservative ~1–1.5 day figure (fast N=2k/10k cells + 12-way parallelism + 8 pre-done triage cells).
- ssh-launched background jobs timed out the ssh client twice but `nohup` detached the runs; verified single-orchestrator at source before trusting each launch.
- Sapphire's working tree holds the actively-written grid outputs untracked, blocking pulls; left unreconciled on purpose (don't disturb a running grid) — resolve once it exits (SHA-verify-then-remove-then-pull, as done earlier this session).
- The spec's α-coverage gate was corrected mid-session to the lodged Amendment 01 §A5.5.1 criterion after the triage exposed the inconsistency.
- Amendment 03's `justification.txt`/`summary-addendum`/PDF are deliberately not yet generated — they derive from the finalised §A5.5, which awaits the grid verdict.

## 2026-06-08 → 2026-06-09 — full-grid PASS → Amendment 03 LODGED → H2.1 production run done + finalised → α-identifiability found, diagnosed, literature-grounded → joint-model scoped

A marathon execution-and-discovery session. Commits `b206626..418f822`, all pushed.

**Full grid PASS.** The 450-cell re-validation finished 438/450 with 12 `smooth_decline` cells failing on a transient tmpfs ENOSPC (PyTensor numba temp files filled the 31 GB RAM-backed `/tmp`); re-ran the 12 with `TMPDIR` on the 264 GB root disk → 450/0 (deterministic seeds). Verdict **B = 96.4 %** under the Amendment-01 §A5.5.1 criterion (`FULL-GRID-REPORT.md`); the summariser's Grid-A regression assert scoped opt-in (`5494347`); α-recovery LoA [−0.12, +0.13], within Decision 33's ±0.18 (`compute-alpha-loa.py`).

**grid-state retention rule** (Shawn, once-and-for-all): live `grid-state.json` gitignored; tracked record = `grid-state-final.json` run-close snapshot; 4 runs migrated (`b206626`).

**Amendment 03 (convention-model)** §A5.5 filled + 4-artefact package built (`build-justification.py` + the PDF builder) + **LODGED by Shawn**.

**H2.1 PRODUCTION RUN** (`runs/2026-06-07-h2.1-launch-prep/`): built the harness (`code/{h2_lib,fit-unit,run-h2}.py`) reusing the recovery-validated `build_model_f1_f3` + `aoristic_spa`; smoke-tested; ran 28 units (+ **Italia excl. Rome** = unit-29, N 40,499), 0 failed, all converged, wall 98 s (`8c8151f`, `4c30c20`). Finalised with the identifiability flag + two-bound α (`finalise-results.py`, `8a31edf`): **16 confirmatory-eligible, 4 caveated-high-α, 9 under-identified** (`SUMMARY-FINAL.md`).

**α-identifiability diagnostic** (`DIAGNOSTIC-alpha-identifiability-REPORT.md`, `identifiability-table.*`): for temporally-concentrated frontier units convention & genuine are confounded in time → α under-attributes (Moesia inf shared 0.05 vs per-unit-basis 0.87 vs 60 % grid-aligned); flag = shared α far below the grid-alignment family fraction. **informed-α prototype + small-N re-test** (`runs/2026-06-09-informed-alpha/`): a prior cannot fix a confidently-wrong likelihood at any width/N — REFUTED; the lever is the convention shape/location. **H3b DRAFT** (`runs/2026-06-09-h3b/`): exploratory per Decision 15 (not confirmatory); Antonine deficit ~AD 168; CPL-3 null. **prereg note** drafted (`planning/prereg-note-2026-06-09-alpha-identifiability.md`). **Two scouts** (`planning/scout-2026-06-09-...-SYNTHESIS.md`): the joint-likelihood remediation (classification as a 2nd likelihood term) is established practice (concomitant-variable mixtures; OxCal outlier model); novel core = joint temporal-frequency mixture with classification as the identification instrument.

### Contextual assumptions
- Heavy reliance on parallel background agents (H3b, informed-α prototype, small-N re-test, 2 scouts) per Shawn's standing "use agents / manage context" instruction; each agent's claims (esp. DOIs and the H3b-exploratory prereg reading) were independently re-verified at source before being trusted or relayed.
- All agent work was committed by the main loop (agents instructed not to run git) to avoid index races on the shared working tree.
- The two scouts could not query the Zotero library (a missing `httpx` dep in their env), so the "all candidates NEW" dedup is **unconfirmed** — verify before staging.
- Sapphire git was left **behind origin with untracked diagnostic outputs** throughout (agents read existing committed inputs + ran scp'd code from `~/h2-smoke` scratch); reconcile (SHA-verify-remove-pull) before the next sapphire compute run.
- The H3b draft and the joint-model design are explicitly FOR REVIEW / next-session — not finalised; H3b's identifiable-unit set (agent gap<0.20 → 17) differs slightly from the finalise set (gap≤0.25 → 16) pending reconciliation.

## 2026-06-09 — joint identifiability-remediation BUILT + POC'd → design PIVOTED → audited → full recovery grid LAUNCHED

Remote-control session. New run dir `runs/2026-06-09-joint-identifiability/`. Commits `44c7aa1..ef10c58` (+ this reflect), all pushed.

**Sapphire git reconciled** at the top (was 15 behind; SHA-verify-remove-pull on 6 identical H2.1 outputs → ff-pull; later a second reconcile for the committed POC outputs). Now 0/0 at the grid-harness commit.

**Built the joint model** (`code/joint_lib.py`): `build_model_joint` = temporal block byte-identical to `build_model_f1_f3` + a classification binomial `k ~ Binomial(N, α·θ_conv + (1−α)·θ_gen)` sharing α. Grid-alignment indicator (rule C = F1∨F3 ∨ round-endpoint Big). **θ calibrated** from the 19 production-identifiable units (`calibrate_theta.py` → `theta-calibration.json`): rule C θ_conv 0.945, θ_gen 0.155, RMSE 0.12; classification-implied α lands inside the [shared, per-unit] bracket for every under-identified unit.

**Local recovery POC on sapphire** (`POC-REPORT.md`; amd-tower lacks `python3-dev` for the PyTensor C backend): **Exp 1** shared basis + classification FAILS confounded cells (α≈0); **Exp 2** per-unit basis (true shape) + classification recovers (|bias| ≤ 0.07); **Exp 3** per-unit basis (estimated/contaminated shape) + classification recovers (|bias| ≤ 0.12). **Design PIVOTED** to per-unit basis + classification (reverses Amendment 03's shared basis). **κ-sweep** (`poc-kappa-check.json`): widening the θ prior amplifies the residual bias → keep κ=40. Findings grounded in the statistical trio (Feller/Gustafson/Huang & Bandeen-Roche), verified from authoritative abstracts (`priority-papers-status.md`).

**Decisions (Shawn):** per-unit + classification is the LEAD; **hybrid (Option 3)** spec'd as the *preregistered robustness check* (`hybrid-robustness-spec.md`, global θ estimated, α independent — no pooling); κ=40; the prereg is to be amended (sweeping all changes since the last lodged amendment) before Option 3; the hybrid gets one pilot fit to measure compute before its full validation.

**Pre-launch `/audit`** (Shawn's gate; 4 parallel subagents): cleared `joint_lib`/`grid_lib`; fixed `run_joint_grid` (atomic `os.replace` writes, validity-gated resume, crashed-worker isolation, converged-subset aggregates, divergence surfacing, shared-basis baseline on confounded cells) + `aggregate_joint_grid` (3-conjunct C2, failed-cell reporting). Smoke-tested (stride-43 7-cell slice, 4 ident + 3 confounded): 0 failures, atomic writes confirmed, aggregator correct (lead |bias| 0.072 vs baseline 0.202 on confounded).

**Full grid LAUNCHED** on sapphire (PID 1899820): 300 cells × 100 reps + baseline on 90 confounded ≈ 39,000 fits; ETA ~16–18 h; resumable; STATUS `outputs/grid-STATUS.txt`, log `outputs/full-grid.log`, per-cell JSON `outputs/grid/` (all gitignored — only `grid-VERDICT.md` + `grid-summary.json` get committed). Obs 83–86 logged (`ef10c58`). Continuity + prereg-note banner + `.gitignore` committed.

### Contextual assumptions
- The full grid runs on sapphire independently of the session; the verdict (the joint-model gate) is pending at close (~16–18 h out). `aggregate_joint_grid.py` produces the verdict when cells complete.
- The ~16–18 h ETA corrects the "~1 h" first quoted to Shawn (the original full-grid-spec under-counted: 100 reps × 300 cells × lead + 90-confounded baseline; the N=15000 fits run ~30 s each).
- Live grid outputs are deliberately gitignored (regenerable; grid-state retention rule); the next session commits only the verdict + summary snapshots after the run.
- 762 stale untracked files from the superseded 2026-05-26 two-unit grid remain on sapphire (regenerable; not deleted — flagged for optional cleanup, harmless to the resumable reconcile pattern).
- Full-text reading of the 3 NEW statistical papers + canonical Zotero staging (a minimal lit-scout-iterate workspace → the shared importer, NOT a bespoke script) are tracked follow-ups; the dedup itself is done.

## Session 2026-06-10 → 2026-06-11 — sapphire incident recovery → proper memory fix → clean grid restart → verdict

**Incident.** The launched grid (PID 1899820) OOM'd and self-aborted at **10/300 cells** (`BrokenProcessPool`); throughput had collapsed to 2 cells/h under swap thrash. Diagnosed **two** independent root causes: (1) RAM OOM from long-lived fork pool workers never releasing PyTensor memory + `allow_gc=False`; (2) `/tmp` tmpfs at **100 % inodes** (~1.05 M leaked `tempfile` files, June 4–7) → `mkdtemp() ENOSPC` → intermittent SSH `255`. Cleared `/tmp` (100 %→1 %; detached `find -delete`), cleared ~18 confirmed-orphan `map-reader-llm` workers (Shawn confirmed; that project runs on zbook now).

**Memory fix #1 (bounding), committed `e4298e5`, `/audit`-clean.** `run_joint_grid.py`: spawn start method + `max_tasks_per_child=1` (recycle worker per cell → memory returned to OS), per-rep `gc.collect()`, dropped `allow_gc=False`, `TMPDIR` to root fs. Measured pilot + a definitive worst-cell measurement (conc_a0.2_gauss_inwin_N15000, 100 reps) → **per-worker peak 6.7 GB**, climbing linearly (~32 MB/fit). Sized **n_jobs=6**; launched under a `systemd --user --scope -p MemoryMax=50G -p MemorySwapMax=0` cgroup cap; ran ~109/300 overnight, healthy.

**Memory fix #2 (proper, with Shawn), committed `fad6fd5`, `/audit`-clean.** Refactored `build_model_joint` to wrap y/k in mutable `pm.Data`; `run_cell` builds the joint model once per cell and swaps replicate data via `fit_joint_on_model` + `pm.set_data`. Eliminates the per-fit PyTensor recompile/leak at source. Scope: joint model only (`build_model_f1_f3` left untouched — imported by H2.1 + 5 runs). Gate 1 (`validate_setdata.py`/`determinism_test.py`, committed `6fe80d9`): new code **bit-reproducible** (new-vs-new = 0.000) but **not bit-identical** to old (~2×10⁻³ method-specific NUTS-path delta; conv flags match). Gate 2: worst-cell RSS now ~2 GB at 100 reps (joint flat; residual is the still-rebuilt baseline) → **n_jobs=12 safe**.

**Decision (Shawn): RESTART** rather than mix methods. Deleted the 116 old-method cells; relaunched all 300 fresh with the new code at **n_jobs=12**, cgroup-capped, monitored.

**Result — full 300-cell grid (committed `18dac46`).** 25.1 h, 0 worker-errors, 0 failed cells, bit-reproducible. Scored vs `full-grid-spec.md §3`: **C2 PASS** 64/90 (lead |bias| 0.066 vs baseline 0.362, ~5×); **C1 FAILS** 37/210 — coverage 0.374 (bias fine at 0.075), from a near-uniform **+0.06…+0.08** contamination bias across the whole surface; **C4 marginal** (84 %, mean 0.950). Not a clean pass: the documented estimated-basis contamination is real and degrades coverage.

**Next-session set-up.** Shawn chose to **evaluate the cross-classified time × alignment arm (D-B)** before any production refit; spec drafted + committed (`cross-classified-spec.md`, `37a94c5`). Incident writeup committed (`MEMORY-FIX-AND-RUN-STATUS.md`, `29945f9`/`284c4b6`).

### Contextual assumptions
- The verdict is **not** the clean pass the original plan assumed; the "production-refit 28 units → OSF amendment" path is **paused** pending the D-B arm's outcome. The amendment still REVERSES Amendment 03's shared basis and the prereg-note "Planned remediation" § is still stale-flagged.
- Sapphire memory/`/tmp` infrastructure is now solved and reusable: spawn+`max_tasks_per_child`, root-fs `TMPDIR`, `systemd-run --user` cgroup cap (export `XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS` when detached). The next grid arm inherits all of it.
- The standing `/tmp` `tempfile` leak in the PyMC/R workflow is unfixed at source (only cleared) — a follow-up; the named `/tmp` files (`h3a_*.py`, `gs_perm.sh`, `k3_scoring.sh`, `run_sweep.sh`) point at the offending sweep/scoring/shadow scripts.
- Sapphire git carries untracked copies of `validate_setdata.py`/`determinism_test.py`/`grid-VERDICT.md`/`grid-summary.json` (now committed from local) — the next sapphire reconcile must clear those untracked files before `git pull` (sha-verify-then-remove, per the established pattern).
- Next session is run by a different model (Fable 5); the carry-forward includes an orientation + explicit second-opinion items.

## Session 2026-06-11 → 2026-06-14 — cross-classified D-B → adoption → production refit → θ robustness → OSF Amendment 04 LODGED

**D-B cross-classified arm.** Signed off `cross-classified-spec.md` with three corrections (the generator invariant was unsatisfiable as written → conditional-split construction; the compute estimate was ~15× low; §2 p_conv decided by a 3-arm pilot, not A-vs-B). Built the generator + `build_model_cross_classified` (modes tiers3/library/free) + runner + aggregator; 4-agent `/audit` (no criticals). **3-arm pilot** (20 cells × 20 reps): `library` wins decisively (confounded bias +0.010 vs tiers3 −0.400 vs free −0.031); `tiers3` reproduced the predicted POC-Exp-1 collapse. **Full 300×100 `library` grid** (sapphire, ~46 h, 0 failures): CLEAN PASS — C1 |bias| 0.021 (the +0.07 contamination surface eliminated), C2 72/90 with |bias| 0.009 vs baseline 0.362, C4 96%; coverage 0.374→0.627 (a precision-for-accuracy trade — the posterior tightened to 66% of the lead's width — not under-dispersion). **Adopted** as production lead (Shawn sign-off).

**Production refit** (`runs/2026-06-13-cc-production-refit/`). Two design decisions settled empirically: aoristic-effective counts for k/n_rows (θ transfers; row-vs-mass aligned-frac ≤ 0.06); a FIXED 27-row corpus-wide slab library (not a per-unit catalogue — no contamination channel; spans every unit's aligned shape, NNLS L1 ≤ 0.083 except Pompeii). Refit of 29 units: all 10 frontier units pinned (Moesia inferior 0.05→0.70, etc.), controls stable, 28/29 converge. The α-identifiability diagnostic is resolved.

**θ robustness (B+C).** Hybrid pilot weakly identified (α↔θ_gen ridge) but surfaced θ_gen ≈ 0.024. (B) Re-derivation from corrected α's → θ_gen 0.025 (2.5× better fit; the calibration's 0.155 was circularly biased by the shared-basis α's). (C) θ-prior sweep (4 priors × 29 units): 27/29 stable. **Shawn adopted the re-derived θ** (decision i); refit re-run under θ_conv 0.930 / θ_gen 0.025 (frontier α's rose slightly).

**OSF Amendment 04 — drafted, verified, LODGED 2026-06-14** (`planning/osf-amendment-2026-06-14-cross-classified-remediation.md`; tag `osf-amendment-04-2026-06-14` → commit `61c954c`). Reverses Amendment 03's shared basis; adopts cc-library; A1–A8 mirror A03; 5 DOIs verified. §A5.6 rewritten after pulling the H3b spec + Decision 15: H3b is exploratory (not confirmatory); lodges the *principle* (replace the identifiability restriction with uncertainty propagation), not a unit set, separating lodged-now from the downstream H3b implementation. Adversarial verification agent caught 2 critical stale-value bugs (a false "tag absent" records note; empire-aggregate R̂/ESS left at the first-pass 1.026/211 vs adopted-θ 1.008/315) — both fixed. Package (justification.txt + summary-addendum + PDF) built via `runs/2026-06-14-amendment-04-prep/code/build-justification.py`. Created the missing `osf-amendment-03-2026-06-08` tag (→ `90897d6`) along the way; all four amendment tags now resolve on the remote.

**Repo hygiene.** Reclaimed ~2.9 GB (regenerable 2026-05-26 synthetic cells; the results were committed) + 533 MB revalidation cells; gitignored + removed prior-run transients; tracked `diag-refit.json` (the basis-swing diagnostic record); removed a low-value grid-state pre-rerun snapshot. Both machines clean and synced.

### Contextual assumptions
- The remediation is **complete and lodged**; the "production-refit → amendment" path three prior sessions deferred is closed. The production α's now live under the adopted θ (θ_gen 0.025); the first-pass (θ_gen 0.155) is preserved at commit `48cb5d5`.
- **Next-session priorities, in order (Shawn):** (1) the `/tmp` hygiene task on sapphire — fix the offending scripts' tempfile handling, default `TMPDIR` to root-fs, add an age-based janitor (show the diff before applying; it touches other runs' scripts); (2) the H3b implementation — the H2.1 hand-off must emit the genuine-SPA *posterior* (currently the median only) and the H3b envelope test must run draw-wise (decision #1), which also resolves the H3b draft's open questions (OQ-2 criterion, OQ-8 per-unit scope). Recorded as next-session priorities deliberately rather than a cron, because both need Shawn in the loop.
- The H3b spec (`runs/2026-06-09-h3b/h3b-spec.md`) remains a DRAFT with 8 open questions; the amendment does not pre-empt them.

## Session 2026-06-14 → 2026-06-15 — /tmp hygiene (216 GB reclaim + 3-layer fix) → H3b draw-wise base run (D1–D3)

**[1] `/tmp` hygiene** (`PROVISIONING.md` "Temp/scratch hygiene"; commit `71961df`). Diagnosis corrected: the continuity's four named "offending scripts" were stale — three don't exist, the fourth already redirects `TMPDIR`, and `gs_perm.sh`/`k3_scoring.sh` were loose non-git working files left in `/tmp`. Real leak = unbounded `~/.pytensor/numba` (201 GB) + per-run pytensor scratch (`~/cc-scratch/…two-unit` 13 GB / 2.97 M files), with no machine-default `TMPDIR` and no janitor. Reclaimed **216 GB** (root-fs 71%→42%); verified-regenerable only (caches + grid intermediates whose REPORTs are committed); left the Qwen3-VL model + `bootstrap-cis` (other projects) untouched. 3-layer fix: L1 machine-default `TMPDIR=~/cc-scratch/tmp` prepended above `~/.bashrc`'s non-interactive guard (verified for `ssh sapphire 'cmd'`; backup `~/.bashrc.bak-2026-06-14`); L2 historical run-scripts deliberately not retrofitted (L1 catches them); L3 `scripts/sapphire-cc-scratch-hygiene.conf` systemd-tmpfiles drop-in (14-day age-evict; reuses the active daily clean timer; Shawn installed → `/etc/tmpfiles.d/`). `/tmp` self-cleans via the OS `q /tmp 10d` policy (confirmed working).

**[2] H3b Stage A — re-emit the posterior** (commits `f0d049d`/`fd85a3d`/`8999fc8`). The refit kept only medians, so `run_refit.py --emit-draws` was added to persist the full per-draw `p_gen` posterior (8,000 draws/unit → `runs/2026-06-13-cc-production-refit/outputs/posterior-draws/`, gitignored, ~64 MB). Re-ran the seeded 29-unit refit on sapphire (5.8 min, 0 errors). Fixed an `np.savez` `.npz`-auto-append bug (file-handle write). **Provenance gate PASS 29/29** (`verify_emit_provenance.py`): the re-run reproduces the committed adopted-θ fits to MCMC noise (α Δ ≤ 1.8e-3, SPA Δ ≤ 9.3e-4, draws↔median 4.6e-9). Gate tolerances set to MCMC-noise level after establishing PyMC NUTS is not bit-reproducible under FAST_RUN/threaded BLAS.

**[2] H3b Stage B — draw-wise engine + run** (commits `b707e7f`/`881aafd`). `h3b_drawwise.py`: builds the featureless-null MC envelope once per unit × null and evaluates all 8,000 draws against it; a self-test asserts the inlined envelope matches the library `forward/permutation_envelope_test` bit-for-bit. `run_h3b_drawwise.py` drives 29 units × 2 nulls × λ∈{1.0,1.2}. **D1–D3 resolved (Shawn 2026-06-15):** D1 — CPL fits the *observed corrected* curve (standard SPD; a correction to OQ-5-as-confirmed, "fit to raw", which saturated the probes too); D2 — accept the global saturation (large-N over-power; global p≈0 for all 29 under both nulls — reproduces the 2026-06-09 draft), report probe-window P(deficit) as the deliverable, defer the large-N + baorista annex; D3 — keep exp as a labelled saturated cross-check.

**Result** (`REPORT-drawwise-2026-06-15.md`, generated from `deviations.json`; 3 figures). Probe deficits reported as net windowed departure % + P(deficit). Named scopes clean and historically coherent: empire-aggregate Antonine −23% / Crisis −27% (both P(def)=1.0), latin-aggregate −43% / −13% (both P(def)=1.0). By net departure, 20/29 net Antonine deficit, 14/29 net Crisis. Soft-annotated (Moesia inferior, Britannia) + reachability (Lusitania n_eff 1,577 < 1,618) flagged not excluded; λ=1.2 coverage-inflation moves only borderline units. Old `REPORT.md` banner-superseded; spec marked EXECUTED; DECISION note marked resolved.

**Housekeeping.** `units-prev-provenance` snapshot removed from sapphire; `.bashrc.bak-2026-06-14` kept (safety); session methodology learning written to the JSONL memory store; continuity updated (2026-06-15 SESSION CLOSE prepended). Both machines clean + synced (`e6ab700`).

### Contextual assumptions
- The H3b **base run is the committed deliverable**; the global test is reported honestly as a saturated gate and the probe-window deficit posteriors are the result. Nothing here is confirmatory (H3b is exploratory; no Holm family).
- **baorista infra already exists** (`runs/2026-05-03-baorista-install/`, 2026-05-03: R 4.4.3 + baorista 0.2.1 + NIMBLE on sapphire, smoke-tested, empire-scale feasible) — so the deferred annex's baorista item is ~2–4 days, not greenfield; the smoke test capped widths at 100 y (not realistic 300 y), so production needs full-LIRE-width re-validation.
- **Next: the flexible-null robustness annex** (D2's deferred work), recommended for a NEW session with its own spec + pre-launch sign-off: (a) cheap first — a more-flexible smooth null (CPL k=5–7 / spline / GP fit to the observed curve) + an effective-N/reduced-significance variant (~1 day, local, reuses all machinery) to test whether a better-specified null de-saturates the global test at all; (b) then baorista if warranted. Also still pending: §5 substantive work.

## Session 2026-06-15 → 2026-06-16 — flexible-null annex (D2 closed) → deconvolution-leverage + peak diagnostics → §5 sensitivity batch (D11/D12/B4)

**[1] H3b flexible-null robustness annex — D2's deferred work, part (a)** (spec `438fd43`; engine+driver `4593367`; spline-IRLS fix `db11f7e`; report/figures `5d2edfb`; results `7fe248a`). Spec signed off (Shawn), executed on sapphire. Two orthogonal levers on the 29 cc-units, propagating the genuine-SPA posterior draw-wise: a **flexibility lever** (CPL k∈{2,3,5,7} + Poisson P-spline + kernel-ridge GP, all fit to the posterior-median corrected curve, on one effective-df axis) and an **effective-N lever** (thinning ladder + a de-powered simultaneous-coverage / max-studentised-deviation global statistic). k=3 CPL reproduces the base run bit-for-bit (regression guard). **Verdict: NO-GO on baorista-for-the-global-test** — the sweet-spot scan (global p>0.05 AND named-scope Antonine P(deficit)≥0.8) returns **0 hits across all 290 unit×fit combinations**. The saturation is robust to null flexibility (edf 5→20), to the de-powered statistic, AND to effective-N thinning to N′≈1,500 (empire global p still 0.006) → **structural null-misspecification, not large-N over-power**. Probe-window P(deficit) confirmed/shown robust as THE deliverable. Wrinkle: the CPL knot-sweep is non-monotone (empire k5 absorbs the Antonine window, k7 recovers); the penalised spline/GP ladders are monotone → vindicates carrying all three families. → **Obs 93** (`4c27a98`).

**[2] Deconvolution-leverage diagnostic — does the deconvolution help H3a?** (α-vs-pop `6e3d541`; Pompeii-artefact robustness fix `d72ad06`; results `a6ce8db`). Shawn's question. **No** for the cumulative Hanson scaling: H3a's date window is the full envelope, so reshaping conserves the count (mass conservation); the only channel, α, is uncorrelated with population (Spearman −0.11) and corpus size (−0.22). Implied β-shift from genuine count α·N robustly ≈0 (Theil-Sen −0.03; drop-Pompeii OLS +0.015) — naïve OLS +0.29 was one high-leverage unit (Pompeii, α=0.016) in log space, caught on a robustness check. Publishable line: "the population–epigraphy scaling holds whether or not we correct for editorial-convention dating." → **Obs 94** (`9152d4a`).

**[3] Peak-shift diagnostic — Shawn's follow-up** (script `d136c2f`; results `6bf7638`). A peak/max-window statistic is shape-sensitive (not mass-conserved), so the deconvolution IS in scope there. The genuine 25-y peak is **~+60% taller** than raw (25/26 units rise), shifted ~10–18 y (empire peak AD 188→208) — convention-removal dominates GRW attenuation. **But** the lift is uniform across size (log(peak ratio) vs population: Spearman −0.00, Theil-Sen −0.005) → moves the peak-scaling *intercept*, not β. Both cumulative and peak exponents robust; the peak height/timing change is real descriptive value. Province-level proxy; city-level test needs the per-city mixture.

**[4] §5 sensitivity batch (D11, D12, B4)** (D11 EIV first-pass `42c9891`; D11 Berkson fix + D12 `7d2ea3e`; D11/D12 results `edc5592`; B4 width-pool `3f6abb9`/`6acfddf`; B4 threshold re-run `29c48b5`/`6b2a14a`). Primary 1,044-city Hanson frame; sapphire MCMC.
- **D11 (Hanson-pop measurement error):** corrected to the prereg's **Berkson** form `log_pop_c ~ Normal(log_pop_observed_c, σ_pop)` after the first pass used a structural EIV hyperprior. f_within robust: 0.299 → 0.305/0.320/0.341 for σ 0.1/0.2/0.3, all supported, max CI shift 0.047 < 0.063 threshold → no material divergence. Clean convergence (R̂ ≤ 1.01, ESS ≥ 1,080, 0 div).
- **D12 (scaling-residual):** pooled NBR power-law β=0.565 → SAMOC log-residual → Gaussian within-between partition. Residual β_within −0.065 [−0.144,0.011] ≈ 0, residual f_within ≈ 0.004 — **coherence** result (within-province scaling = global scaling law; primary β_within 0.587 stands). Shawn approved the construction.
- **B4 (stratified-sampling):** reading `h1_sim_v2.py` showed **Decision 8 replaced the LIRE bootstrap with synthetic-data-from-null** → B4-as-written is moot (width pool is the only lever; province/city counts vestigial). v2-faithful: scheme (a) proportional-allocation threshold-neutral by construction; scheme (b) reweight-to-balance shifts the width pool (city-balanced median 99y→79y). Threshold re-run under global / province-balanced / city-balanced pools at matched reduced precision (n_iter=200, n_mc=300): **thresholds robust** — median Δ −1.1% / −0.4%, within MC noise, 0 reachability changes. → **Obs 95** (`07acb34`).

**Housekeeping** (`e5e8f76`). Obligations audit updated: D11/D12/B4 flipped UNACCOUNTED → RESOLVED 2026-06-16 (mark, not delete). Layer B (β-inversion) staged in continuity for a fresh session — now unblocked (H3a β_within: empire 0.587, Latin ~0.733), with inputs, compute host, the four design decisions, and the pending Ostia validation gate. Both machines clean + synced.

### Contextual assumptions
- The flexnull annex and the diagnostics are **exploratory robustness**; none changes a confirmatory result or the base H3b deliverable. The §5 sensitivities are preregistered exploratory (material divergence = reported limitation, never an amendment trigger).
- The deconvolution-leverage and peak diagnostics are **province-level proxies** (only the 29 province/region-level units are deconvolved). The definitive city-level tests (D13 α-as-translator; the peak-window scaling test) need a per-city mixture, deliberately not built given the flat proxy results.
- **B4 is superseded-by-Decision-8:** the prereg's stratified-bootstrap B4 doesn't apply to the v2 synthetic-data thresholds; the width-pool check is the v2-faithful substitute (recorded in the audit).
- All compute on **sapphire** (Shawn's instruction — not amd-tower); reduced-precision MCMC for the §5 sensitivities + B4 re-run, baselines at matched precision so deltas are clean.

## Session 2026-06-16 → 2026-06-17 — §5 substantive arc: Layer B (β-inversion) → H5 (common temporal component) → H7 (time-resolved H3c) → peak-scaling; + paper-framing decision

A long multi-phase session (resumed across a crash) that took four staged §5 pieces from spec to committed result, then turned in the back half to a paper-framing decision driven by Shawn's questions.

**[1] Layer B — β-inversion to time-varying population** (spec+sign-off `efa4e71`; inputs staged on sapphire `a6424b3`; script post-`/audit` `2fe14d7`; results `b0de24e`). Per-city population trajectories via `pop_t ∝ insc_t^(1/β_within)`, draw-wise (empire β 0.587 primary, Latin 0.733 overlay), relative + Hanson-anchored. Four design decisions signed off; Ostia expectation grounded by a light lit search (OCD/Meiggs/Boin). Deterministic transform of the §5 Layer-A posterior + standalone anchor re-fits (the only MCMC). `/audit` clean (2 medium fixes). **Validation gate PASSES both anchors**: Ostia apogee AD 125–150 (P(peak 2nd c.)=0.99), Pompeii peak AD 50–75, post-AD-79 mass 0.000. 1/β>1 amplification → median target-city inverted pop at AD 250 ≈0% of peak (epigraphic-habit decline, not demography) → illustrative-only. → **Obs 96**.

**[2] H5 — habit-removed residual / empire-wide common temporal component** (results `4f125cd`; decomposition script+json `5badf5f`/`3ae63c0`; Obs completion + report reframe `c9aff73`). Deterministic read of the §5 Layer-A posterior (no MCMC). Common temporal component (`g_shape`) peaks AD 187.5; habit-lag corpus-median ≈0, IQR ±50y; foundation-terminus check clean (0.07% median pre-foundation mass, 99 within-envelope), worst offenders frontier-military sites. Magnitude decomposition (log-rate SD): common g 1.11, province u 1.02, city v 0.98, between-city level 0.78; common ≈54% of per-city temporal variance. Latin-minus-Roma (257/268) ≈ identical; Greek-East-11 peak earlier (~AD112). → **Obs 97 + 98**.

**[3] H7 — time-resolved (per-period) H3c** (results `fb05c1d`). 8×50y periods; aoristic-apportioned counts, fixed 1044-city universe + population-based Mundlak; H3a NBR + H3c diagnostics replicated from the audited confirmatory code; all 8 fits converged. β_within U-shape over time (0.70 → ~0.58 high-empire plateau → 0.66); capitals over-produce in every period (P(contrast>0)=1.00); residual spatial clustering significant only in 50BC–AD0 (Moran k8 +0.029, p=0.021). → **Obs 99**.

**[4] Peak-scaling — peak-inscription vs Hanson-population** (results `e456ad2`). Both arms Shawn directed. Raw aoristic peak (50y, 1044): β_within 0.557 [0.49,0.62] — indistinguishable from cumulative 0.587 (peak scales like total). Overlap (268 §5, 25y): raw 0.223 ≈ modelled 0.213 — Layer-A smoothing neutral; the §5-subset drop is range restriction. Answers the open "Hanson vs peak population" question; corroborates the cumulative H3a headline. → **Obs 100**.

**[5] /observe + paper-framing decision** (Obs 96–101 `93e1ade`; Obs 97 completion + H5 reframe `c9aff73`). Recorded six Observations. **Framing decision (Shawn):** present the empirical nested-unit decomposition first (results), interpretive labels (population, habit) later (discussion), with Hanson as the explicit first interpretive step (the bridge); name the quantity "empire-wide common temporal component" not "habit"; results are model-conditional; **diagnostic unit = Latin-speaking-minus-Roma**. → **Obs 101**.

### Contextual assumptions
- All four analyses are **exploratory** (Layer B/H5 Decision 13; H7 prereg §5; peak-scaling tertiary/not-preregistered). None changes a confirmatory result.
- H7 and peak-scaling ran on the **all-provinces 1044 frame**; Latin-minus-Roma variants (the diagnostic unit) are staged for next session. The §5 decomposition is frame-insensitive (96% Latin-West).
- The **identification caveat (Obs 98)** governs interpretation: `g_shape` conflates habit/demography/taphonomy/convention; the decomposition separates empire-common from city-specific, not habit from population.
- Next priority (Shawn): the **habit-removed (residual) Layer B** — invert the city residual into a population trajectory *relative to the empire trend* (well-posed regardless of the conflation).
- All compute on **sapphire**; inputs (Layer-A `.nc`, H3a β `.nc`, dataprep cache) staged + sha256-verified there this session.

## Session 2026-06-17 → 2026-06-18 — residual Layer B (+ q_u nested triple) → size-vs-dynamics probe → province-size regression → obligations-audit refresh + amendment-status correction → Latin variants (H7 + peak-scaling)

A long consolidation session: cleared the staged residual Layer B priority and the chain of follow-up questions it generated, refreshed the prereg-obligations register (correcting a stale amendment-status belief), and cleared the Latin diagnostic-unit variants. Two background agents (province-size, Latin variants); five Observations (102–106) + one user-observation (43). All compute on sapphire; all artefacts verified at source before commit.

**[1] Residual Layer B — habit-removed β-inversion** (`runs/2026-06-17-s5-layer-b-residual/`). Spec + design sign-off `1484e2e`/`5a7a3ba`; `/audit`-clean script. Inverts only the city residual `u+v` (empire-common `g` removed): `q = exp((1/β)·(u+v))`, geom-mean 1 by construction. **Mid-run metric correction** (`063504c`): the pre-specified "frac-of-own-peak" contrast was confounded (1/β amplification + GRW endpoint variance, 11/34 cities peak at envelope edges) and falsely mimicked the raw collapse; replaced with `q`-vs-empire-baseline. Result (`a5c4699`): the apparent universal post-AD-250 collapse **dissolves** — median reliable `q` on the empire trend at the AD-188 peak (1.01), ~0.32 at AD 262, heterogeneous; self-test bit-exact (adding `g` back reproduces raw Layer B `shape_med`, 5.6e-16). **q_u nested triple added** (`63e90ce`/`bc824c8`) on Shawn's request: province-from-empire (q_u), city-from-province (q_v), city-from-empire (q_uv = q_u·q_v per draw, guarded). The late decline is largely **provincial-tier** (AD262: city-from-empire 0.32, province-from-empire 0.56, city-from-province 0.78). → **Obs 102** (held-out anchors are a design strength, `3f5fcd2`), **Obs 103** (`d49bf21`; v-only rounding fix `bc0358d`).

**[2] size-vs-dynamics probe** (`runs/2026-06-18-s5-size-vs-dynamics/`, spec `7f94943`/`35ba098`/`923ceb4`, results `55b42bc`). The well-posed reframe (user-obs 43) of Shawn's "compare the isolated city effect to Hanson?" — a category mismatch (level-free shape vs static level), redirected to: does city size (`pop_est`) predict features of `q_v`? **Null on the headline** (q_v late-level ρ +0.09, volatility −0.05); `q_uv` (city-from-empire) shows a coherent "bigger = more buffered" gradient (F3 tilt ρ +0.38, bootstrap CI [+0.05,+0.63]); since it weakens once the province is removed, the gradient is *inferred* province-mediated. Spearman (robust, Obs-94 lesson) + city-bootstrap + draw-wise ρ; non-circular (Layer A has no pop covariate). n=34, underpowered, null pre-framed informative. → **Obs 104** (`cfb951c`).

**[3] province-size regression** (background agent; `runs/2026-06-18-province-size-regression/`, results `8da7b16`). Direct test of [2]'s province-mediation inference: regress province `q_u` features on province size (`pop_est` summed over the full index). Province join 35/35 clean; self-check bit-exact (0.0). **Not corroborated** — province *size* does not drive `q_u` buffering (sum aggregate null/sign-incoherent; mean/max lean buffered but CIs include 0; n≈20–35). Refines Obs 104: "province-mediated" is a *decomposition* fact (variance in the `u` tier), **not** a province-size effect; not in tension with the provincial-tier decline level. → **Obs 105** (`95fea55`). User-obs 43 (`181ef3c`): the naive-question→reframe is the statistician dynamic Shawn values (Martin Eftimoski / 2017 Kazanlak déjà vu).

**[4] Obligations-audit refresh + amendment-status correction** (`81ffd16`). The 2026-06-05 audit was partly stale (predates the H3c(i) closure, the §5 arc, A03/A04). Wrote `planning/prereg-obligations-audit-2026-06-18.md`; banner-superseded the old one. **Key correction (verified at git tags + summary-addenda): all four amendments 01–04 are LODGED** — A02 (Latin-primary) since 2026-06-06, *not pending* as the old audit (and my own verbal overview) said → the Latin frame is the lodged primary, not amendment-gated. The **H2.1 supplementary wave** (Dirichlet-MM/NegBin/aoristic-MC/trapezoidal/H2.2–2.4/empire-α) confirmed **staged-not-run** (production SUMMARY) → the largest remaining confirmatory debt. Two stale amendment DRAFT headers flipped to LODGED (`8ee9bc7`).

**[5] Latin variants — H7-Latin + peak-scaling-Latin** (background agent; `runs/2026-06-18-h7-latin/`, `runs/2026-06-18-peak-scaling-latin/`, results `2b159f1`). Diagnostic-unit (lodged primary frame, A02) versions of H7 and peak-scaling. Frame verified = H3a precedent (817 cities / 39 provinces, Roma excluded). All fits converged (R̂ 1.0000, 0 div). **H7-Latin:** β_within U-shape **persists, shifted up** (0.89 → ~0.69 high-empire plateau → 0.80; plateau ~0.69 ≈ Latin cumulative 0.733); capitals over-produce every period (P=1.00 ×8); clustering early-empire-only (2 earliest periods). **peak-scaling-Latin:** raw peak β 0.700 (50y)/0.693 (25y) ≈ Latin cumulative 0.733. Confirms the all-provinces findings on the diagnostic unit → U-shape is not a Greek-East artefact. → **Obs 106** (`e7bb733`).

### Contextual assumptions
- All five analyses are **exploratory** (Decision 13 / prereg §5); none changes a confirmatory result. The Latin variants are frame-swaps of already-signed-off analyses.
- **Background-agent discipline:** both agents did everything *except* git (the main session owns all commits, to avoid concurrent-push races); their numbers were re-verified against `summary.json` before commit.
- The 8 H7-Latin per-period idata `.nc` (~456 MB) are regenerable and gitignored (kept on sapphire).
- **Amendment status is now definitively all-lodged** (01–04); supersedes any earlier "A02 pending" in older docs/continuity session-history blocks (those are historical, not updated).
- Next genuine work (per the 2026-06-18 audit): the **H2.1 supplementary wave** (largest confirmatory debt; needs new DM/NegBin builders + a supervised launch spec); then D13 α-as-translator (downstream of a real per-city mixture), H6 baorista cross-check, H4 province-scale Layer B, H9 confirmatory letter-mass H3a; then the write-up (empirical-first, Obs 101). No amendment lodgement outstanding.

## Session 2026-06-18 → 2026-06-19 — H2.1 supplementary wave (all-29) → H9 confirmatory letter-mass H3a → C10 aoristic-MC validity test → C10 (ii) realism-graded recovery → aoristic-MC-bias lit-scout

A marathon orchestration session (Shawn travelling, working from zbook): spec'd and ran the largest remaining confirmatory debt (the H2.1 supplementary wave), ran the pending confirmatory H9, and resolved the C10 aoristic-MC question end to end — validity test, realism-graded follow-up, verified literature scout. ~20 background/foreground agents across amd-tower/sapphire/zbook, every code artefact gated build→audit→run. All results verified at source before commit.

**[1] H2.1 supplementary wave — all 29 units** (`runs/2026-06-18-h2.1-supplementary-wave/`; spec `1dee8bf`; driver + 3 audit rounds → `5685e39`; results `1a4a9b1`, 54.5 min on zbook). Fork-1 (Shawn): the lodged single-multinomial DM/NegBin/aoristic-MC supplementaries re-map onto the Amendment-04 cross-classified likelihood. **C5/C6:** DM/NegBin do not move α (max |Δα| 0.016); multinomial adequate (overdispersion warranted in only 4/29). Cross-family PSIS-LOO dropped as inapplicable (→ α side-by-side + dispersion adjudicator). **C11:** input-level r (the prereg Decision-4 measure; output-level r dropped as convention-confounded); 2/29 flag report-alongside (empire 0.9402, Aquileia 0.9269). **H2.2:** 15/29 (52%) meet ≥50% boundary-step reduction. **H2.3:** 8/29 meet r≥0.9 (rest below the N<2000 floor, caveated). **H2.4 + C16** assembled. κ=5000 (pilot-tuned). Only empire-aggregate/NB under-converges (R̂ 1.013, known), reported as a limitation.

**[2] H9 — confirmatory letter-mass H3a** (`runs/2026-06-18-h9-letter-mass-h3a/`, `ec99343`; zbook, ~9 min). Mirror of the inscription-count H3a with letter-mass (content measure, Amendment 01) as response. **f_within SUPPORTED on every frame:** Latin (primary) 0.448 [0.364,0.535], empire 0.356; pop-weighted 0.626, letter-weighted 0.607; P(>0.05/0.10/0.20)=1.0. Max R̂ 1.000, 0 div. PPC 8 pass / 2 minor (the expected count-pinned tail caveat). **Both measures — acts + content — corroborate** within-province population scaling.

**[3] C10 aoristic-MC validity test** (`runs/2026-06-18-c10-validity-test/`, `6ce6e3f`; verdict `116fe3b`). 1a slab-concentration + 1b ground-truth recovery + 1c mass-preserving-vs-point-collapse. **Pre-registered verdict: (a)** — on synthetic ground-truth, point-date *recovers* the planted α (refuting my reading-(b) lean). But 1c (real empire) confirmed the collapse is real (point-collapse 0.10 vs mass-preserving 0.62) — a 1b/1c mismatch the idealised synthetic didn't reproduce.

**[4] C10 (ii) realism-graded recovery** (`d475348`; parallelised `5544c15`, n_jobs=10, ~65 min). R0 control / R1 widths / R2 θ-contamination / R3 latent-null / R1+R2. **Verdict: θ-contamination (R2, R1+R2) drives the collapse, NOT width** (R1 didn't cleanly reproduce; biased the mass arm). Mechanism: under realistic alignment misclassification, point-date = a hard plug-in of a misclassified assignment that collapses the mixture share while mass-apportionment (integrate-out) recovers it. **The deconvolution α stands; the point-date 0.10 is a method artefact.**

**[5] Lit-scout — aoristic-MC bias under misclassification** (`planning/lit-scout-2026-06-19-aoristic-mc-misclassification-bias/`, `423832a`; verified 21/21 DOIs, 0 corrections). The phenomenon is documented under two names: the **"three-step / classify-analyze plug-in bias"** (Bolck-Croon-Hagenaars 2004; Bakk 2013 — bias governed by classification error; = our θ story) and the **aoristic pointwise-vs-mass critique** (Carleton & Groucutt 2021; Roberts 2012). The *conjunction* (this bias in a cross-classified aoristic deconvolution) is novel. **13 new papers staged to Zotero** (staging subcollection, deduped across SDAM-AU/TRAP/My Library; 8 already held).

### Contextual assumptions
- **Mode:** orchestration — spec → delegate build → audit → run → collect, ~20 agents, three machines, while Shawn travelled. The standing **audit-before-run** rule gated every artefact and caught multiple silent-failure bugs (the supp-wave driver's optional add-ons took 3 audit rounds; the prereg-required core was clean throughout).
- **C10 status:** essentially resolved — the deconvolution α is trustworthy; the point-date aoristic-MC is artefactual under realistic θ and should be reported as a method limitation, not a genuine α-sensitivity. The lit-scout's "deeper chaining" candidates (forward-chain Bakk 2013 / Xia 2020) are optional, not run.
- **Parallelisation oversight + fix:** the C10 scripts ran sequentially (unlike the cc-grid/supp-wave norm); fixed via the supp-wave ProcessPoolExecutor pattern. A reusable sapphire-parallel-run module is **slated** (Shawn's standardisation point), not built.
- **Debugging note:** ~15 min lost to misdiagnosing a `pkill -f` self-match as SSH rate-limiting; fixed with the `[r]` pattern (also explains an earlier non-firing Monitor).
- **Machines:** amd-tower / sapphire / zbook synced (zbook prepared for the train); gitignored idata `.nc` regenerable, kept on the compute hosts.

## Session 2026-06-19 → 2026-06-20 — D13 close → H4/H6/B′ resolved → documentation accuracy-certified (Workflow) → collaborator key-findings summary → figures spec

**Done:**
- **D13 α-as-translator DISCHARGED** (the last preregistered obligation): Option A, standalone per-city α (163 Latin cities N≥100, 162/163 converge) as an H3a NBR covariate; clean β_within null (+0.431→+0.422, 0.14 SD), robust under M=50 multiple imputation (FMI 0.5%). City-level confirmation of Obs 94. → Obs 107.
- **H4 closed** by adopting q_u (province-from-empire; standalone province inversion → follow-up). **H6 baorista deferred** to follow-up. **B′ city-α map parked** (post-travel/follow-up).
- **Two read-only assurance sweeps:** prereg-obligations-coverage (`planning/prereg-obligations-coverage-sweep-2026-06-20.md`, 54/63 covered) + results-documentation-uplift (`planning/results-documentation-uplift-2026-06-20.md`).
- **A01 §A5.4 content-residual DISCHARGED** (Obs 108; content/scaling channels orthogonal, ρ +0.004) → prereg unconditionally complete. **Tier-1/2/3 documentation cleanup** (Obs 109–111 for H9/C10/supp-wave; banners, cross-links, broken path, 65→63 typo).
- **|Δα| pinned** to 0.0156 (latin-agg DM) across REPORT/model-comparison/Obs 111. **~31% Option 1** (cite ~36%/24.96%, footnote lodged rounding, lodged text unedited; `a4416e4`).
- **Documentation-accuracy audit WORKFLOW** (first in-anger Workflow use): 7 clusters, 677 specifics, 97.5% matched, 17 corrections **applied + re-verified at source** (`af4d527`..`1079098`, `63f910c`), 1 false alarm overturned; cross-document consistency confirmed. Certificate `planning/doc-accuracy-audit-2026-06-20.md`. → **documentation accuracy-certified, write-up-ready.**
- **Collaborator key-findings summary** v1 → v2 → refinements (`reports/key-findings-summary-2026-06-20.md`, `4061a0b`→`a84511d`): non-specialist explanations, per-section results, ≈54/24/22 temporal split, population bottom line (within-province ~48%; between-province weak), verbosity-is-idiosyncratic descriptive add.
- **Figures spec** (`runs/2026-06-20-figures/spec.md`): 13 figures, code-based (matplotlib), 12/13 from local data, atlas needs §5 `.nc` regen; Claude Design ruled out for data figures.
- **women.csv thread started:** read Adela Sobotkova's TRAC "Graveyard→Time-Series" talk; set the worked-example boundary (method vignette here, substantive crossover-age history → EJA companion); feasibility spec (`runs/2026-06-20-women-corpus-feasibility/spec.md`).
- **Sync:** all machines (amd-tower/sapphire/zbook) + origin to HEAD; diagnosed + explained a VS Code stale-buffer (not a git fault).

---

## Session 2026-06-20 → 2026-06-21 — figures build (F1–F19 + women) → α-inversion correction → Roma/Italia → women Option-1/2 (probe + tempun)

**Done:**
- **Figure set built (code-based matplotlib):** shared `figtheme.py`/`figdata.py`; **F1–F14** (SPD before/after, province/city small-multiples + atlases, capital over-production, within/between scaling, β-over-time, orthogonality, reachability, variance partition) + **F15–F19** (Rome de-fogged, capital comparison, why-Rome-excluded, Italia exceptionalism, Italia temporal) + the women figures. JAMT/Springer specs: sans-serif (Nimbus Sans), 84/174 mm, vector PDF + 600-dpi PNG, Okabe–Ito frames, **BC/AD axis** (Shawn's standing preference). No §5 `.nc` regen needed — the 2026-05-31 monolithic posterior was intact on sapphire/zbook (md5-verified, copied down). Figure captions (non-specialist) + figindex.
- **Exact three-way temporal split** (`compute_temporal_split.py`): tiers are anti-correlated; clean covariance-attributed partition **empire-common 38% / province 29% / city-unique 33%** (sums to 100), 54% standalone footnoted. Supersedes the indicative 54/24/22.
- **α-DIRECTION CORRECTION (Obs 116):** the key-findings summary had α inverted ("genuine fraction"). **α is the CONVENTION fraction** (model `p_mix = α·p_conv + (1−α)·p_gen`; confirmed by pi_align + **Pompeii α=0.016**). Empire α=0.68 = ⅔ convention / ⅓ genuine (Latin 0.74 = ¾). Corrected summary body + callout + banner (`1fffc72`); one residual spec line (`f4a93b2`); captions were already correct. **Shawn confirmed the framing** (expected ~⅔ convention from the ~100y median date range).
- **Roma + Italia (Obs 114):** 5 new cc-library fits (reusing production `fit_one`; one universal basis). **Rome α=0.80** (most convention-dated unit); provincial capitals 0.56 (less than provinces, 0.71); **Italian exceptionalism** — Rome + Italian municipia (0.80/0.79) the empire's most convention-dated; **Severan crossover** (F19: Italy peaks ~AD80, provinces AD212). `REPORT.md`, summary §4b. *(Italia-incl-Rome ESS-marginal, 397<400 — flagged.)*
- **Women Option-1 feasibility (Obs 115):** 3 fits; ~90% convention (α 0.90/0.84), below/at floor → **not in the reliable de-fogging regime**. `MEMO.md`, figure, indicative C2–C3 read.
- **Women Option-2 (case-study) — spec + outline + the decisive analyses:** the three-option ladder recorded (reconstructed middle rung, Shawn-confirmed); `option-2-case-study-spec.md` + `option-2-case-study-outline.md` (spine = diagnostic + hypothesis-generator). **Better-dated probe (Obs 117): NO reachable subset** — width is the wrong axis (convention structural at round widths; ≤50y band α=0.97); genuine core N≈6–315 below floor. **`tempun` installed + run** (`tempun==0.2.6`; §6 figure: tempun overlays the raw shape, blind to convention). Summary §4c (with charts); MEMO charts embedded.
- **Crash diagnosis** (`planning/archive-search-crash-diagnosis-2026-06-21.md`): a `zcat|tr|grep` over the gzipped session archive crashed the machine (newline-collapse + near-quadratic regex × concurrency, no limits). Safe pattern (`rg -z`, sequential, capped) for the infra "search-the-archives" skill.
- **Obs 114–117**; reflections (this set); **all machines + origin synced @ `d2452fa`** (then this reflection commit); BC/AD preference saved to memory.

**Contextual assumptions:** much of this ran as a long **autonomous block while Shawn was AFK** ("run all of it"), so the discipline mattered — spec-before-run, audit-before-launch, commit-per-stage, layered independent checks (code-review + obs-writer each caught a different error). The α-inversion is the session's headline; the figure set + the two analysis threads (Roma/Italia, women) are otherwise complete and documented. Two items remain Shawn's: the α *headline framing* (resolved — he's fine with "⅔ convention") and Option-2 *drafting* (parked until the paper-wide outline next session).

**Contextual assumptions:** Shawn travelling within days (no unattended multi-day sapphire runs started); the documentation is now treated as the *foundation the write-up is built on*, which is why the accuracy bar was raised to value-level verification; first session to use the Workflow tool in anger. **MILESTONE: the entire analytical programme + its documentation are complete; next session = figures.**
