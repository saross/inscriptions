# LIRE v3.0 — dataset-level profile

_Generated 2026-04-23 11:59:45 by `data-profile-scout` methodology._

## Dimensions

- Rows: **182,853**
- Columns in parquet: **63**
- Attributes documented in seed schema `LI_metadata.csv`: **66**
- Schema disagreement: three columns in schema are not present in parquet (`is_geotemporal`, `is_within_RE`, `material_EDCS`). All 63 parquet columns are in the schema. See `decisions.md` Decision 3.

## Date-range summary

- Rows with both `not_before` and `not_after` non-null: **182,853** (100.000%)
- Rows with null `not_before`: **0**; with null `not_after`: **0**
- `date_range` = `not_after - not_before`:
    - mean: **101.287** years
    - median: **99.000** years
    - min: **0** years; max: **2059** years
    - (broad distribution + granularity diagnostic in `artefacts.md` §§ *Unexpected-pattern diagnostic*)

## Spatial summary

- Rows with valid (non-null, non-zero) `Latitude` AND `Longitude`: **182,853** (100.000%)
- Rows with non-null `Latitude` AND non-null `Longitude` (including zeros): **182,853**
- Because LIRE is a geotemporal subset of the combined corpus, the valid-coordinate rate is expected to be ~100 %. Any shortfall from 100 % is discussed in `artefacts.md` under `geolocated-rate`.

## Per-column null / uniqueness

Full table in `tables/null_and_unique_by_column.csv`. Top-10 most-null columns:

| column | null rate | n null | n unique |
|---|---:|---:|---:|
| `language_EDCS` | 99.974% | 182,806 | 6 |
| `inscr_process` | 93.868% | 171,641 | 7 |
| `year_of_find` | 85.255% | 155,891 | 899 |
| `letter_size` | 85.115% | 155,635 | 3,596 |
| `support_material` | 84.594% | 154,682 | 59 |
| `depth_cm` | 83.989% | 153,576 | 177 |
| `present_location` | 79.754% | 145,833 | 4,762 |
| `width_cm` | 79.133% | 144,697 | 353 |
| `height_cm` | 78.910% | 144,289 | 345 |
| `support_objecttype` | 74.805% | 136,783 | 39 |

- Columns with >50% nulls: **31** (see `artefacts.md` §`null-profile`).
