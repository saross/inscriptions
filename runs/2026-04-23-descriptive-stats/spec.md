# Run spec: LIRE descriptive profile + data-artefact audit

**Date:** 2026-04-23
**Block:** data-setup + §5.1–5.2 descriptive statistics + data-artefact audit
**Project:** inscriptions SPA (~/Code/inscriptions/)
**Orchestration:** main-thread CC → serial proposer/verifier chain via `data-profile-scout` + `data-profile-verifier` (agent definitions at `~/personal-assistant/agents/`; today executed via `general-purpose` shell because the named agents are not yet in this session's routing).

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
- **Subset levels:**
  - `dataset` — roll-up, `columns: []`.
  - `province` — `columns: ["province"]`, `threshold_candidates: [10, 30, 100, 300]`.
  - `urban-area` — `columns: ["urban_context_city"], threshold_candidates: [10, 30, 100, 300]`.

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

- `venv_python`: `/home/shawn/personal-assistant/venv/bin/python3` (confirmed to have pandas + numpy + scipy + pyarrow via existing lit-search.py usage).
- `output_dir`: `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/`
- `max_runtime_minutes`: 30 for proposer, 20 for verifier.

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
