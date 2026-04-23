# Seed: dataset, environment, and provenance for this run

**Run ID:** `2026-04-23-descriptive-stats`
**Date:** 2026-04-23
**Spec:** `./spec.md`

## Dataset

- **Name:** LIRE — Latin Inscriptions of the Roman Empire, version 3.0.
- **Zenodo DOI:** <https://doi.org/10.5281/zenodo.8147298>.
- **Canonical citation:** Kaše, V., Heřmánková, P., & Sobotková, A. (2023). LIRE (v3.0) [Data set]. Zenodo. <https://doi.org/10.5281/zenodo.8431452>.
- **File:** `/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet`
- **Source record of the file:** inherited from the archived 2024 notebook; identical to the Zenodo v3.0 parquet per archive provenance note 2026-04-22. A reproducible Zenodo-API pull script is on the Thursday backlog but not on today's critical path.
- **Expected dimensions:** 182,852 rows × 65 attributes. Confirm on load.

## Schema

- **File:** `./seed/LI_metadata.csv` — 65-attribute LIST/LIRE metadata dictionary (identical schema between LIST and LIRE; LIRE is a row-filter of LIST).
- **Source:** `/tmp/LI_metadata.csv` retrieved by the LIST reconnaissance agent on 2026-04-22 from <https://zenodo.org/records/10473706/files/LI_metadata.csv?download=1>.

## Environment

- **Python interpreter:** `/home/shawn/personal-assistant/venv/bin/python3`.
- **Expected packages:** pandas, numpy, scipy, pyarrow. No other dependencies.
- **Host:** this is expected to run locally on amd-tower (primary dev machine) or zbook. Compute is trivial for 182 k rows; no sapphire offload required.

## Parameters applied

See `./spec.md` for the full input contract. Summary:

- `subset_levels`: `dataset`, `province`, `urban-area` (via `urban_context_city`).
- `threshold_candidates`: [10, 30, 100, 300] for both province and urban-area.
- `artefact_checks`: `default` plus the editorial-boundary year list from Heřmánková/Kaše/Sobotková 2021 §94.
- `date_columns`: `not_before`, `not_after`.
- `spatial_columns`: `Latitude`, `Longitude`.

## Agent definitions used

- **Proposer:** `~/personal-assistant/agents/data-profile-scout.md`, commit: _recorded at launch time in ./agents.md_.
- **Verifier:** `~/personal-assistant/agents/data-profile-verifier.md`, commit: _recorded at launch time in ./agents.md_.

**Execution-vehicle note:** this run invokes the methodologies via the `general-purpose` agent shell because the named agents are not yet in this session's agent-routing table (they were defined today). The briefs at `./briefs/` inline the full methodology, so the named-agent routing benefit is not load-bearing for this run; it will apply from the next session onward.

## Session context

- Invoked from Claude Code session `91b1783e-e099-49c8-826e-d37026ca716b` on 2026-04-23.
- Main-thread context budget at invocation: ~55 %, soft wind-down target 50 %, hard wind-down 75 %.
- This spec + scaffolding authored during the specification hour of 2026-04-23; execution phase runs async while main-thread turns to other work.
