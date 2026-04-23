# Run spec: LIRE comprehensive descriptive profile + data-artefact audit (revised rerun)

**Date:** 2026-04-23 (revised)
**Block:** data-setup + §5.1–5.2 descriptive statistics + data-artefact audit (comprehensive mode)
**Project:** inscriptions SPA (~/Code/inscriptions/)
**Orchestration:** main-thread CC (amd-tower) → serial proposer/verifier chain via `data-profile-scout` + `data-profile-verifier` (agent definitions at `~/personal-assistant/agents/`; executed via `general-purpose` shell because the named agents are not yet in this session's routing). **Compute runs on sapphire via SSH** per FAIR4RS posture + compute-offload convention.
**Relationship to first run** (commit `f254c4f`): this rerun supersedes the first-run outputs. Motivation: (a) project-local venv instead of personal-assistant venv; (b) comprehensive-mode stats Shawn's notebook uses; (c) best-practice statistical tests replacing chi-square / log-Cohen's-d / BH-FDR with MC permutation (two-stage null) / Cliff's delta / Holm-Bonferroni per post-review self-critique.

## Goal

Produce a clean, reproducible, adversarially-verified descriptive profile of LIRE v3.0 at three subset levels (dataset / province / urban area), with a data-artefact audit against the documented EDH/EDCS inheritance issues, as input to:

- Saturday 2026-04-25 feasibility doc for Adela Sobotková.
- Friday 2026-04-24 minimum-thresholds simulation (this profile tells us typical-n and which subsets qualify).
- Post-Saturday paper-sprint Weeks 1–3 §5.1–5.2 material.

## Inputs

- **Dataset:** `/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet`
  - 65-attribute schema per `seed/LI_metadata.csv` (copied from LIST reconnaissance).
  - Expected 182,852 rows (LIRE v3.0, filtered: is_within_RE=True, is_geotemporal=True, 50 BC – AD 350). Confirm on load.
- **Schema:** `runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv` — full 65-attribute dictionary, inherited from LIST.
- **Date columns:** `["not_before", "not_after"]`.
- **Spatial columns:** `["Latitude", "Longitude"]`.
- **Subset levels (revised thresholds + bivariate):**
  - `dataset` — roll-up, `columns: []`.
  - `province` — `columns: ["province"]`, `threshold_candidates: [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]`.
  - `urban-area` — `columns: ["urban_context_city"]`, same thresholds.
  - `province-x-urban-area` — `columns: ["province", "urban_context_city"]`, same thresholds. Bivariate grouping added this rerun.
- **Per-group detail produced at EVERY threshold** (not only highest), per comprehensive mode.

## Artefact checks

From the catalogue at `~/personal-assistant/agents/data-profile-scout.md`:

- `midpoint-inflation` — chi-square on mid-interval dates vs century midpoints 50, 150, 250, 350 AD.
- `editorial-spikes` — chi-square at: 14 BC, AD 27 (Augustan boundary); AD 97, AD 192 (Antonine); AD 193, AD 212, AD 235 (Severan) — per Heřmánková/Kaše/Sobotková 2021 §94.
- `coordinate-precision` — histogram of decimal places in Latitude/Longitude.
- `null-profile` — per-column null rate.
- `negative-date-range` — should be 0 in LIRE v3.0 (the team fixed these; confirm).
- `date-range-extreme` — rows with date_range > 500 years.
- `geolocated-rate` — expect ~100 % (LIRE is filtered for geolocation).
- `is_within_RE-rate` — expect 100 % (LIRE filter).
- `is_geotemporal-rate` — expect 100 % (LIRE filter).

**Unexpected-pattern diagnostic** is always on: dating-granularity histogram, ordered by frequency. Catches artefacts we didn't enumerate.

## Configurations

- `comprehensive_mode`: `true` (this rerun activates the extended statistics, bootstrap CIs, MC permutation tests, drill-down, and sensitivity sweep).
- `remote_exec`: `{host: sapphire, workdir: ~/Code/inscriptions, venv_python: .venv/bin/python3}` — compute on sapphire via SSH; orchestration on amd-tower.
- `output_dir` (on sapphire): `runs/2026-04-23-descriptive-stats/outputs/` under the repo root.
- `categorical_columns`: `["province", "urban_context_city", "urban_context", "inscr_type", "type_of_inscription_auto", "language_EDCS", "material_clean"]`.
- `text_columns`: `["clean_text_conservative"]` — letter-count using Latin alphabet filter per 2026-04-22 notebook cell 63.
- `numeric_columns`: `["date_range", "Latitude", "Longitude", "letter_count", "urban_context_pop_est"]`.
- `temporal_envelope`: `[-50, 350]`.
- `primary_key`: `LIST-ID`.
- `drill_downs`: year_97_neighbourhood (AD 94–100), antonine_era (AD 96–192).
- `sensitivity_thresholds`: `[0.01, 0.05, 0.10]`.
- `bootstrap_resamples` / `permutation_resamples`: 20 000.
- `n_jobs`: `-1` (exploit all sapphire cores for resample loops).
- `small_n_threshold`: 50 (subsets at/below this get percentile-bootstrap CI alongside BCa).
- `test_family_sizes`: midpoint_inflation=4, editorial_spikes=7, drill_down_year_97=7 → **Westfall-Young stepdown** as primary correction (permutation-based; exploits joint distribution from MC already being run), **Holm-Bonferroni** reported as companion.
- Null model for MC permutation: **aoristic-probability null** (Ratcliffe 2002; Crema 2012).
- `max_runtime_minutes`: 60 for proposer (comprehensive mode + 20k resamples + Westfall-Young companion), 45 for verifier.

## Preregistration status

This run is **exploratory data analysis** — initial descriptive profile of a dataset, not a confirmatory inferential study. Preregistration is not required and would be theatre for this scope. Findings-driven drill-downs (AD 97 neighbourhood, Antonine era) are explicitly exploratory.

Preregistration applies to later stages: (a) Friday minimum-thresholds simulation — OSF preregistration drafted tomorrow before simulation launch; (b) Week-1-to-3 SPA analyses on LIRE/LIST — expanded OSF preregistration before first SPA run. See `planning/decision-log.md` (Decision 7, pending) for scope.

## Expected outputs

Per scout agent's output contract, in `outputs/`:

- `summary.md` — headline findings, ≤1,000 words.
- `profile-dataset.md`, `profile-province.md`, `profile-urban-area.md`.
- `artefacts.md` — per-check results + unexpected-pattern diagnostic.
- `tables/*.csv` — machine-readable versions.
- `decisions.md` — every judgement call.
- `run.log`.

Verifier adds:

- `corrections.md`, `verdict.md`, `verifier.log`.

## Decision-points flagged in advance (stop-and-flag)

- Dataset row count ≠ 182,852 — investigate schema / version before proceeding.
- `is_within_RE`, `is_geotemporal` not 100 % — dataset is not the filtered LIRE we expect.
- `negative-date-range` > 0 — contradicts the LIRE v3.0 cleaning claim.
- Schema disagreement with `seed/LI_metadata.csv`.

## Success criteria

- Proposer completes within 30 min; produces all expected output files; decisions.md has zero stop-flags or documented resolution for each.
- Verifier verdict: PASS or PARTIAL (with divergences under investigator-tolerable threshold).
- Outputs are sufficient to inform Friday's simulation parameters (typical-n distribution, subset-qualification count at each threshold) and to populate §5.1–5.2 of the conference paper.

## Links

- Backlog entry: `planning/backlog-2026-04-22.md` §1 Thursday actionables.
- Decision 1 (LIRE-first): `planning/decision-log.md`.
- Working-notes observations on LIST/LIRE schema and data-quality artefacts: `docs/notes/reflections/working-notes.md` Obs 1–9.
- Agent definitions: `~/personal-assistant/agents/data-profile-scout.md`, `~/personal-assistant/agents/data-profile-verifier.md`.
