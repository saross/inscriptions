# LIRE v3.0 — per-urban-area profile

_Group column: `urban_context_city`._

## Basic counts

- Rows with valid (non-null, non-empty) `urban_context_city` label: **141,909** of 182,853 (77.608%)
- Null `urban_context_city` rows: **40,944**; empty-string rows: **0**
- Distinct non-empty groups: **1,045**

## Top-20 groups by row count

| rank | group | count | % of valid |
|---:|---|---:|---:|
| 1 | `Roma` | 65,452 | 46.123% |
| 2 | `Pompeii` | 4,511 | 3.179% |
| 3 | `Salona` | 3,472 | 2.447% |
| 4 | `Mogontiacum` | 2,971 | 2.094% |
| 5 | `Ostia` | 2,647 | 1.865% |
| 6 | `Aquileia` | 2,034 | 1.433% |
| 7 | `Puteoli` | 1,780 | 1.254% |
| 8 | `Carnuntum (1)` | 1,648 | 1.161% |
| 9 | `Cirta` | 1,020 | 0.719% |
| 10 | `Porolissum` | 967 | 0.681% |
| 11 | `Capua` | 929 | 0.655% |
| 12 | `Apulum (2)` | 855 | 0.602% |
| 13 | `Sarmizegetusa` | 700 | 0.493% |
| 14 | `Mediolanum (Italia (XI Transpadana))` | 639 | 0.450% |
| 15 | `Aventicum` | 609 | 0.429% |
| 16 | `Segobriga` | 595 | 0.419% |
| 17 | `Misenum` | 593 | 0.418% |
| 18 | `Colonia Augusta Treverorum` | 587 | 0.414% |
| 19 | `Augusta Emerita` | 557 | 0.393% |
| 20 | `Herculaneum` | 528 | 0.372% |

Full ranking: `tables/top20_urban-area.csv`.

## Threshold qualification

| min rows per group | groups qualifying |
|---:|---:|
| 10 | 609 |
| 30 | 384 |
| 100 | 170 |
| 300 | 46 |

See `tables/threshold_qualifying_urban-area.csv`.

## Per-group detail at threshold 100

- Number of groups at threshold 100: **170**
- Mean per-group count: **730.2**; median: **196**
- Mean Latitude null-rate: **0.0000%**; mean `not_before` null-rate: **0.0000%**

Full detail in `tables/detail_threshold100_urban-area.csv` (sorted by count descending).
