# LIRE v3.0 — per-province profile

_Group column: `province`._

## Basic counts

- Rows with valid (non-null, non-empty) `province` label: **180,609** of 182,853 (98.773%)
- Null `province` rows: **2,244**; empty-string rows: **0**
- Distinct non-empty groups: **65**

## Top-20 groups by row count

| rank | group | count | % of valid |
|---:|---|---:|---:|
| 1 | `Roma` | 65,457 | 36.242% |
| 2 | `Latium et Campania / Regio I` | 18,512 | 10.250% |
| 3 | `Dalmatia` | 7,088 | 3.924% |
| 4 | `Hispania citerior` | 6,312 | 3.495% |
| 5 | `Germania superior` | 5,874 | 3.252% |
| 6 | `Venetia et Histria / Regio X` | 5,872 | 3.251% |
| 7 | `Dacia` | 4,870 | 2.696% |
| 8 | `Britannia` | 4,647 | 2.573% |
| 9 | `Pannonia superior` | 4,460 | 2.469% |
| 10 | `Samnium / Regio IV` | 4,187 | 2.318% |
| 11 | `Africa proconsularis` | 3,518 | 1.948% |
| 12 | `Germania inferior` | 3,390 | 1.877% |
| 13 | `Apulia et Calabria / Regio II` | 3,132 | 1.734% |
| 14 | `Pannonia inferior` | 3,132 | 1.734% |
| 15 | `Numidia` | 3,014 | 1.669% |
| 16 | `Etruria / Regio VII` | 2,801 | 1.551% |
| 17 | `Umbria / Regio VI` | 2,763 | 1.530% |
| 18 | `Noricum` | 2,761 | 1.529% |
| 19 | `Baetica` | 2,593 | 1.436% |
| 20 | `Transpadana / Regio XI` | 2,434 | 1.348% |

Full ranking: `tables/top20_province.csv`.

## Threshold qualification

| min rows per group | groups qualifying |
|---:|---:|
| 10 | 60 |
| 30 | 58 |
| 100 | 52 |
| 300 | 43 |

See `tables/threshold_qualifying_province.csv`.

## Per-group detail at threshold 100

- Number of groups at threshold 100: **52**
- Mean per-group count: **3465.6**; median: **1182**
- Mean Latitude null-rate: **0.0000%**; mean `not_before` null-rate: **0.0000%**

Full detail in `tables/detail_threshold100_province.csv` (sorted by count descending).
