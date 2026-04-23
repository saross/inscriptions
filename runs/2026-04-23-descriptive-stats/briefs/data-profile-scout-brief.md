# Invocation brief: data-profile-scout → LIRE v3.0 descriptive profile (2026-04-23)

You are acting as **data-profile-scout** per the canonical methodology at `~/personal-assistant/agents/data-profile-scout.md`. The named agent is not yet in this session's routing table (it was defined today); you're running as `general-purpose` agent following that methodology. The full methodology is inlined below so you need not read the canonical definition unless you need clarification on an edge case.

## Your role

You produce a rigorous, reproducible descriptive profile of the LIRE v3.0 Latin inscription corpus, with a data-artefact audit against documented EDH/EDCS inheritance issues. Your output will be adversarially re-checked by `data-profile-verifier` against the same dataset in a fresh context — make your numerical claims explicit so the verifier's job is re-computation, not guessing.

## Methodology (inlined from canonical definition)

### Output contract

Write to `output_dir` as files (never per-row dumps to stdout):

- `summary.md` — ≤1,000 words. Headline findings, per-subset highlights, artefact summary, cross-references to the other files.
- `profile-dataset.md` — dataset-level stats.
- `profile-province.md` — per-province stats.
- `profile-urban-area.md` — per-urban-area stats.
- `artefacts.md` — detailed results per artefact check + unexpected-pattern diagnostic (two views: granularity histogram + broad date-range histogram).
- `tables/*.csv` — machine-readable versions of every table referenced in the markdown.
- `claims.jsonl` — **machine-readable enumeration of every numerical claim made in the markdown reports.** One JSON object per line: `{claim_id, category, description, value, units, source_method, source_file}`. Categories: `count`, `rate`, `percentage`, `mean`, `median`, `chisq`, `pvalue`, `ranking`, `threshold_qualifying`. Primary input for the verifier — every claim you want the verifier to re-check must appear here. Aim for at least 50 claims from this run (exhaustive, not selective).
- `decisions.md` — every judgement call. Fact / default / alternatives / rationale / investigator-review flag. Append to the existing file at `../decisions.md` (pre-created stub).
- `run.log` — short tool-use trace.

Response to caller (≤500 words): 3–5 bullet findings, paths to files, any investigator-flagged decisions, any artefact-check failures, approximate runtime.

### Core steps

1. **Validate environment.** Confirm `venv_python` resolves and `import pandas, numpy, scipy, pyarrow` all succeed. Fail fast if not.
2. **Load dataset, confirm dimensions.** Record actual rows × columns. Compare to expected 182,852 × 65. Stop-and-flag if dimensions differ.
3. **Schema validation.** Compare columns against `seed/LI_metadata.csv`. Stop-and-flag on disagreement.
4. **Dataset-level profile.** Row count; per-column null rate; per-column unique-value count; distribution of `date_range = not_after - not_before`; count of rows with valid (non-null, non-zero) Latitude AND Longitude.
5. **Subset profiles.** For `province`, `urban-area` (via `urban_context_city`):
   - Count per group; rank-ordered top-20 groups by count.
   - At thresholds [10, 30, 100, 300]: how many groups qualify.
   - For groups passing threshold 100: per-group stats (count, date-range min/max/mean, null rates on key columns: `Latitude`, `Longitude`, `not_before`, `not_after`, `urban_context_pop_est` if applicable).
6. **Artefact checks** (see catalogue below).
7. **Unexpected-pattern diagnostic** (two views):
   - **Granularity histogram** ordered by frequency: how many rows have `date_range = 0`, `= 25`, `= 50`, `= 99-101` (century-rounded), `= 199-201`, other round numbers, irregular values. Flag any anomaly >5 % as worth investigator review.
   - **Date-range distribution**: broad histogram of `date_range` values bucketed (1, 25, 50, 100, 200, 500+). Surfaces bimodality, unexpected peaks, or gaps the granularity categories miss.
8. **Summarise** in `summary.md` with cross-references.

### Artefact checks (run all)

- `midpoint-inflation` — chi-square on mid-interval dates `(not_before + not_after) / 2` binned by century-midpoint years (50, 150, 250, 350 AD) vs the surrounding years (within ±15 years). Expected positive signal per Heřmánková/Kaše/Sobotková 2021 §64.
- `editorial-spikes` — chi-square at editorial-boundary years: 14 BC, AD 27, AD 97, AD 192, AD 193, AD 212, AD 235. For each, compare count at year X vs mean of counts at X±5 excluding X. Expected positive signal per the same paper §94.
- `coordinate-precision` — histogram of decimal places in Latitude and Longitude columns; flag the distribution.
- `outlier-coordinates` — rows where `|Latitude| > 90` or `|Longitude| > 180`. Expected 0.
- `null-profile` — per-column null rate, sorted descending. Flag columns with >50 % nulls.
- `duplicate-rows` — count of exact-duplicate rows across all columns; count of rows with duplicate `LIST-ID` (primary key).
- `negative-date-range` — count rows with `not_before > not_after`. Expected 0 in LIRE v3.0 (per team's release notes); deviation stop-and-flags.
- `date-range-extreme` — rows with `date_range > 500` years.
- `temporal-outliers` — rows where `not_before < -50` or `not_after > 350` (outside LIRE's stated 50 BC – AD 350 envelope). Expected 0.
- `geolocated-rate` — rows with valid `Latitude` AND `Longitude` / total. Expected ~100 % for LIRE.
- `is_within_RE-rate` — expected 100 % for LIRE.
- `is_geotemporal-rate` — expected 100 % for LIRE.

### Decision-point discipline

**Stop-and-flag** (write entry to `../decisions.md`, halt):

- Dataset row count ≠ 182,852 without documented explanation.
- Schema disagreement with `seed/LI_metadata.csv`.
- `is_within_RE` or `is_geotemporal` not 100 %.
- `negative-date-range` count > 0.
- Environment validation fails.

**Flag-and-continue** (write entry, proceed):

- Subset threshold boundary unusual (< 3 or > 100 groups qualifying at threshold 100).
- Unexpected-pattern anomaly > 5 %.
- Artefact check errors out (proceed to next check).

### Failure modes to actively avoid

- Unbounded iteration / per-row dumps.
- Silent judgement (every judgement → decisions entry).
- Context overrun (outputs are files; response is short summary).
- Hardcoded domain vocabulary.
- Package installation.
- Environment fallback (use `venv_python` or fail).

## Inputs for this run

- `dataset_path`: `/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet`
- `schema`: `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv`
- `subset_levels`:
  ```json
  [
    {"name": "dataset", "columns": []},
    {"name": "province", "columns": ["province"], "threshold_candidates": [10, 30, 100, 300]},
    {"name": "urban-area", "columns": ["urban_context_city"], "threshold_candidates": [10, 30, 100, 300]}
  ]
  ```
- `artefact_checks`: full default catalogue above.
- `date_columns`: `["not_before", "not_after"]`.
- `spatial_columns`: `["Latitude", "Longitude"]`.
- `output_dir`: `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/`
- `decisions_file`: `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/decisions.md` (append, do not overwrite).
- `venv_python`: `/home/shawn/personal-assistant/venv/bin/python3`.
- `max_runtime_minutes`: 30.

## Context

This run feeds Friday's minimum-thresholds simulation (the profile tells us which subsets qualify at each threshold and typical-n distribution) and Saturday's feasibility doc for Adela Sobotková. Quality matters more than breadth: a clean profile of three subset levels is more useful than a noisy profile of ten. Accuracy of numerical claims is the single most important property of your output — the verifier will catch arithmetic errors, but not conceptual confusions.

The 2024 ANU seminar (see `planning/cc-briefing-2026-04-22.md` §5) ran an equivalent profile on an earlier LIRE version. If your figures diverge substantially (by >10 % on headline counts) from round numbers that feel plausible for the seminar-era profile, flag it — there may be a schema or filter change between versions.

Return your structured summary as your final message; write everything else to files.
