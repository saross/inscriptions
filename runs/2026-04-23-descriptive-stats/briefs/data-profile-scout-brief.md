# Invocation brief: data-profile-scout → LIRE v3.0 comprehensive descriptive profile (2026-04-23, revised)

You are acting as **data-profile-scout** per the canonical methodology at `~/personal-assistant/agents/data-profile-scout.md`. The named agent is not yet in this session's routing; you're running as `general-purpose` agent following that methodology. The canonical definition is authoritative; this brief provides the run-specific inputs and the handful of inscription-specific pieces that don't belong in a domain-agnostic agent definition.

## Your role

Produce a rigorous, reproducible **comprehensive-mode** descriptive profile of the LIRE v3.0 Latin inscription corpus plus an adversarial-verifier-friendly claims enumeration. Output informs Friday's minimum-thresholds simulation and Saturday's feasibility doc for Adela Sobotková. Compute runs on sapphire via SSH; orchestration stays on amd-tower.

## Inputs

### Core data
- `dataset_path`: `/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet` (relative to repo root: `archive/data-2026-04-22/LIRE_v3-0.parquet`).
- `schema`: `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv` (relative: `runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv`).
- `primary_key`: `LIST-ID`.
- `date_columns`: `["not_before", "not_after"]`.
- `spatial_columns`: `["Latitude", "Longitude"]`.
- `temporal_envelope`: `[-50, 350]` (LIRE's stated envelope, 50 BC – AD 350). Note LIRE uses overlap-filter semantics; any row whose interval intersects this envelope is in the corpus.

### Subset levels (with revised thresholds)

```json
[
  {"name": "dataset", "columns": []},
  {"name": "province", "columns": ["province"],
   "threshold_candidates": [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]},
  {"name": "urban-area", "columns": ["urban_context_city"],
   "threshold_candidates": [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]},
  {"name": "province-x-urban-area", "columns": ["province", "urban_context_city"],
   "threshold_candidates": [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]}
]
```

Per-group detail (count, date-range stats, null rates, bootstrap CIs on mean / median date-range) is produced at **every threshold**, not only the highest.

### Comprehensive mode

`comprehensive_mode: true`

Supporting parameters:

- `categorical_columns`: `["province", "urban_context_city", "urban_context", "inscr_type", "type_of_inscription_auto", "language_EDCS", "material_clean"]`.
- `text_columns`: `["clean_text_conservative"]` — letter-count using the Latin alphabet filter from the 2026-04-22 notebook cell 63 (lowercase + uppercase Latin A–Z, whitespace-separated; Greek characters filtered out — preserves `letter_count` definition consistent with prior work).
- `numeric_columns`: `["date_range", "Latitude", "Longitude", "letter_count", "urban_context_pop_est"]` (letter_count is derived in step 2; urban_context_pop_est needs a type cast from string to float with null-sentinel handling).
- `drill_downs`:
  - `{target_name: "year_97_neighbourhood", year_range: [94, 100], description: "Neighbourhood of the AD 97 editorial-dip anomaly found in the first run"}`
  - `{target_name: "antonine_era", year_range: [96, 192], description: "Full Antonine era to contextualise the AD 97 dip"}`
- `sensitivity_thresholds`: `[0.01, 0.05, 0.10]` (applied to the unexpected-pattern flag threshold).
- `test_family_sizes`: `{"midpoint_inflation": 4, "editorial_spikes": 7, "drill_down_year_97": 7}` — each ≤ 15; Westfall-Young stepdown applies as primary correction with Holm-Bonferroni as companion sanity-check.
- `bootstrap_resamples`: `20000`.
- `permutation_resamples`: `20000`.
- `n_jobs`: `-1` (all cores on sapphire).
- `small_n_threshold`: `50` (subsets at or below n=50 get both BCa and percentile-bootstrap CIs reported; flag when they disagree by > 10 % relative width).
- `null_cooccurrence_threshold`: `0.50`.

### Artefact checks

Run the full catalogue from the canonical agent definition:

- `midpoint-inflation` — MC permutation (**aoristic-probability null** per canonical methodology: for each row, aoristic weight at year Y = 1/date_range within interval; expected count at year Y = Σ aoristic weights; observed count at year Y = rows where mid_r = Y; null resampling redraws each row's mid uniformly within its interval) at century midpoints AD 50, 150, 250, 350. Observed / expected ratio + BCa CI + Westfall-Young-corrected p-value + Holm-Bonferroni companion.
- `editorial-spikes` — same aoristic-null framework at years 14 BC, AD 27, AD 97, AD 192, AD 193, AD 212, AD 235; observed count at year Y = rows with `not_before_r = Y` OR `not_after_r = Y` (report both endpoint variants). Report direction (spike vs dip) alongside magnitude. **Historical note for this run: in the first run AD 97 came out as a DIP not a spike, against prior expectation — the drill-down below investigates.**
- `coordinate-precision`, `outlier-coordinates`, `null-profile`, `duplicate-rows`, `negative-date-range`, `date-range-extreme`, `temporal-outliers`, `geolocated-rate`, `is_within_RE-rate`, `is_geotemporal-rate` — as specified in the canonical definition.

**Historical context for `negative-date-range`:** previous LIRE versions had transposed `not_before`/`not_after` dates that produced negative ranges. Shawn reported these to the LIRE maintainers; LIRE v3.0 release notes claim zero negatives. Verify and state the result explicitly in `summary.md` with the historical note. If non-zero, stop-and-flag.

**Historical context for `temporal-outliers`:** first-run result was 34,562 rows with endpoints outside [50 BC, 350 AD]; LIRE uses overlap-filter semantics. AD 2230 placeholder values are a known upstream bug Shawn reported to the LIRE team; AD 700 may be plausible data within LIRE's extended envelope. Re-verify the counts; include a breakdown of the most extreme endpoint values (top-10 `not_after` above 350).

### Output contract

Write to `runs/2026-04-23-descriptive-stats/outputs/` on sapphire (which is `~/inscriptions/runs/2026-04-23-descriptive-stats/outputs/`).

Per the canonical output contract plus the comprehensive-mode extensions:

- `summary.md` — headline findings, ≤1,200 words (comprehensive mode bumps the cap). Historical-context paragraphs on negative-date-range and temporal-outliers per above.
- `profile-dataset.md`, `profile-province.md`, `profile-urban-area.md`, `profile-province-x-urban-area.md`.
- `artefacts.md`, `comprehensive.md`, `distribution-shape.md`, `temporal-coverage.md`, `categorical-distributions.md`, `concentration.md`, `text-statistics.md`, `correlations.md`, `null-cooccurrence.md`.
- `drill-downs/year_97_neighbourhood.md`, `drill-downs/antonine_era.md`.
- `sensitivity-sweep.md`.
- `tables/*.csv` for every referenced table.
- `claims.jsonl` — aim for ≥150 claims this run (comprehensive mode expands the claim surface substantially).
- `decisions.md` — append to the existing run-level file at `runs/2026-04-23-descriptive-stats/decisions.md`.
- `run.log`.

### Remote execution

`remote_exec`:

```
host: sapphire
workdir: ~/inscriptions          (Shawn's home on sapphire — the cloned repo root)
venv_python: .venv/bin/python3   (relative to workdir; created via `uv sync`)
```

Python runs on sapphire via the SSH wrapper per the canonical Remote execution section. Your analysis script is written to `runs/2026-04-23-descriptive-stats/code/profile.py`, committed + pushed from amd-tower, pulled on sapphire, executed, outputs committed + pushed from sapphire, pulled back on amd-tower.

### Stop-and-flag conditions specific to this run

- Dataset row count ≠ 182,853 — investigate before proceeding (first-run established this count; brief's earlier "182,852" was a mis-transcription from reconnaissance).
- Schema disagreement on any column in `primary_key`, `date_columns`, `spatial_columns`, `subset_levels.columns`, or the comprehensive-mode column lists — halt.
- `negative-date-range` > 0 — contradicts LIRE v3.0 release claim; halt.
- `sapphire` unreachable or `uv sync` fails — halt; the brief expects sapphire execution.

### Flag-and-continue (write entry, proceed)

- Schema has extra columns not used by this run — log and continue.
- Artefact check errors out — mark NOT RUN in `artefacts.md`, continue.
- Subset-threshold qualification counts unusual (< 3 or > 100 qualifying at a threshold) — expected at the high end of our threshold set; log but proceed.

## Context

First run of this block (2026-04-23, committed at `a5b31af..f254c4f`) used the personal-assistant venv and a minimal threshold set; verifier passed 223/223 claims. This revised run is motivated by: (a) correct FAIR4RS posture via project-local venv; (b) comprehensive-mode stats Shawn uses when starting on a new dataset; (c) best-practice statistical tests replacing chi-square + log-Cohen's-d + BH-FDR with MC permutation (two-stage null) + Cliff's delta / Vargha-Delaney + Holm-Bonferroni per the self-critique of the first-run proposal. Expected runtime on sapphire: 15–30 minutes (bootstrap CIs and MC permutation tests are the dominant cost).

Return your structured summary (≤500 words) as the final message; everything else to files.
