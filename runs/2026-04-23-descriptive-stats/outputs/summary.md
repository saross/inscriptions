# LIRE v3.0 — descriptive profile summary

_Generated 2026-04-23 11:59:51 by data-profile-scout methodology (general-purpose agent; schema disagreements & fixed-environment decisions recorded in `decisions.md`)._

## Headline findings

1. **Corpus scale**: 182,853 rows × 63 columns. Parquet has 63 columns, seed schema documents 66 — three schema-listed columns (`is_geotemporal`, `is_within_RE`, `material_EDCS`) are absent from the parquet. Brief expected 182,852 rows; we observed 182,853. See `decisions.md` Decisions 2-3.
2. **Geolocation**: 182,853/182,853 rows (100.000%) have valid (non-null, non-zero) `Latitude` AND `Longitude`. Expected ~100 % for LIRE; this is the observed rate under the stated criteria.
3. **Date-range granularity is overwhelmingly century-scale**: 48,436 rows (26.49% of non-null date ranges) fall in the 99-101 year century bucket; 8,279 (4.53%) have `date_range == 0`; 28,422 (15.54%) fall in the 199-201 bicentury bucket. See `artefacts.md` §*Unexpected-pattern*.
4. **Subset thresholds**: at n>=100, **52** province groups and **170** urban-area (`urban_context_city`) groups qualify. At n>=300, **43** and **46** qualify respectively. Full detail in `profile-province.md`, `profile-urban-area.md`.
5. **Artefact audit summary**: `negative-date-range` = 0 (expected 0, PASS); `outlier-coordinates` (out-of-range lat/lon) = 0 (expected 0, PASS); `temporal-outliers` (outside 50 BC – AD 350) = 34,562; `duplicate-rows` exact = 0, duplicate `LIST-ID` = 0; `date-range-extreme` (>500 y) = 264; columns with >50% nulls = 31. Two canonical checks (`is_within_RE-rate`, `is_geotemporal-rate`) were **not run** because the columns are absent from the parquet.

## Per-subset highlights

- **Province**: largest groups are `Roma` (65,457), `Latium et Campania / Regio I` (18,512), `Dalmatia` (7,088).
- **Urban area**: largest groups are `Roma` (65,452), `Pompeii` (4,511), `Salona` (3,472).

## Output files

- `profile-dataset.md` — dataset-level profile.
- `profile-province.md` — per-province profile.
- `profile-urban-area.md` — per-urban-area profile.
- `artefacts.md` — all artefact checks + unexpected-pattern diagnostic.
- `claims.jsonl` — machine-readable enumeration of numerical claims.
- `tables/` — CSV versions of every table referenced in the markdown.
- `decisions.md` (at `../decisions.md`) — judgement calls during this run.
- `run.log` — tool-use trace.