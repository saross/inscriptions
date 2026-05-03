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
