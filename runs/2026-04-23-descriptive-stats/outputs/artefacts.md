# LIRE v3.0 — artefact checks

This file enumerates the data-artefact audit run per the canonical `data-profile-scout` methodology. Expected-signal references are to Heřmánková, Kaše & Sobotková 2021 (JDH 5/1).

Two canonical checks — `is_within_RE-rate` and `is_geotemporal-rate` — are **NOT RUN**: the corresponding boolean columns are absent from the parquet (see `decisions.md` Decision 3). Do not interpret silence as a pass.

## midpoint-inflation

Chi-square test: count at a century-midpoint year (AD 50, 150, 250, 350) vs a ±15-year window (31 year-bins). Expected signal per Heřmánková et al. §64.

| target year | count at year | count in ±15 excl | expected at target (uniform) | chi2 | p-value |
|---:|---:|---:|---:|---:|---:|
| AD 50.0 | 12,108 | 8,451 | 663.194 | 204087.803 | 0.000e+00 |
| AD 150.0 | 20,281 | 4,551 | 801.032 | 489516.01 | 0.000e+00 |
| AD 250.0 | 7,222 | 3,859 | 357.452 | 136221.958 | 0.000e+00 |
| AD 350.0 | 12,689 | 685 | 431.419 | 359873.885 | 0.000e+00 |

## editorial-spikes

For each editorial-boundary year, count at the year vs mean of ±5 neighbours (10 bins), excluding the year itself. Chi-square is computed on `[count_at_year, count_in_neighbours]` vs uniform. Expected signal per Heřmánková et al. §94.

| column | year | count at year | mean of neighbours | count in neighbours | chi2 | p-value |
|---|---:|---:|---:|---:|---:|---:|
| `not_before` | -14 | 20 | 109.5 | 1,095 | 71.841 | 2.333e-17 |
| `not_before` | 27 | 19 | 214.4 | 2,144 | 176.519 | 2.789e-40 |
| `not_before` | 97 | 118 | 2529.8 | 25,298 | 2288.629 | 0.000e+00 |
| `not_before` | 192 | 33 | 129.6 | 1,296 | 70.215 | 5.318e-17 |
| `not_before` | 193 | 465 | 126.8 | 1,268 | 660.007 | 1.489e-145 |
| `not_before` | 212 | 870 | 152.4 | 1,524 | 2151.002 | 0.000e+00 |
| `not_before` | 235 | 121 | 111.1 | 1,111 | 0.796 | 3.724e-01 |
| `not_after` | -14 | 14 | 26.7 | 267 | 5.74 | 1.658e-02 |
| `not_after` | 27 | 17 | 327.5 | 3,275 | 292.862 | 1.183e-65 |
| `not_after` | 97 | 500 | 1638.4 | 16,384 | 767.564 | 6.088e-169 |
| `not_after` | 192 | 221 | 51.9 | 519 | 386.416 | 4.989e-86 |
| `not_after` | 193 | 77 | 77.2 | 772 | 0.0 | 9.827e-01 |
| `not_after` | 212 | 99 | 276.4 | 2,764 | 109.922 | 1.019e-25 |
| `not_after` | 235 | 716 | 486.7 | 4,867 | 94.176 | 2.887e-22 |

## coordinate-precision

- Modal decimal places on `Latitude`: **15** (166,831 rows). Modal on `Longitude`: **15** (103,837 rows).
- Distribution in `tables/artefact_coordinate_precision.csv`.

## outlier-coordinates

- Rows with `|Latitude|>90`: **0**
- Rows with `|Longitude|>180`: **0**
- Any out-of-range: **0** (expected 0).

## duplicate-rows

- Exact-duplicate rows across all columns: **0**
- Rows with duplicate `LIST-ID` value: **0**

## negative-date-range

- Rows where `not_before > not_after`: **0** (expected 0 per release notes).

## date-range-extreme

- Rows with `date_range > 500` years: **264** (0.144% of all rows).

## temporal-outliers

- Rows with `not_before < -50`: **1,949**
- Rows with `not_after > 350`: **32,615**
- Rows outside (50 BC – AD 350) envelope: **34,562** (expected 0).

## geolocated-rate

- Rows with valid (non-null, non-zero) `Latitude` AND `Longitude`: **182,853** of 182,853 = **100.000%** (expected ~100 %).

## is_within_RE-rate — NOT RUN

Column `is_within_RE` is not present in the parquet. Check skipped. See `decisions.md` Decision 3.

## is_geotemporal-rate — NOT RUN

Column `is_geotemporal` is not present in the parquet. Check skipped. See `decisions.md` Decision 3.

## null-profile

- Columns with >50% nulls: **31**.

| column | null rate | n null |
|---|---:|---:|
| `language_EDCS` | 99.974% | 182,806 |
| `inscr_process` | 93.868% | 171,641 |
| `year_of_find` | 85.255% | 155,891 |
| `letter_size` | 85.115% | 155,635 |
| `support_material` | 84.594% | 154,682 |
| `depth_cm` | 83.989% | 153,576 |
| `present_location` | 79.754% | 145,833 |
| `width_cm` | 79.133% | 144,697 |
| `height_cm` | 78.910% | 144,289 |
| `support_objecttype` | 74.805% | 136,783 |
| `type_of_inscription` | 71.823% | 131,331 |
| `keywords_term` | 71.623% | 130,964 |
| `trismegistos_uri` | 68.757% | 125,725 |
| `diplomatic_text` | 66.408% | 121,429 |
| `pleiades_id` | 66.400% | 121,415 |

Full sorted list in `tables/artefact_null_profile.csv` (identical to `tables/null_and_unique_by_column.csv`).

## Unexpected-pattern diagnostic

### View 1 — granularity histogram (date_range categories)

| category | count | % of non-null date_range |
|---|---:|---:|
| eq_0 | 8,279 | 4.528% |
| eq_25 | 172 | 0.094% |
| eq_50 | 631 | 0.345% |
| 99_to_101 (century) | 48,436 | 26.489% |
| 199_to_201 (bicentury) | 28,422 | 15.544% |
| other_round_values (10,20,30,...500) | 3,971 | 2.172% |
| irregular | 92,942 | 50.829% |

- Total non-null `date_range`: **182,853**
- **Flagged anomalies >5 %:**
    - `99_to_101 (century)`: 26.489% (48,436 rows) — worth investigator review.
    - `199_to_201 (bicentury)`: 15.544% (28,422 rows) — worth investigator review.

Round-value detail in `tables/granularity_round_values.csv`.

### View 2 — broad date_range histogram (buckets)

| bucket | count | % of non-null |
|---|---:|---:|
| <=1 | 11,069 | 6.053% |
| 2..25 | 15,093 | 8.254% |
| 26..50 | 35,581 | 19.459% |
| 51..100 | 67,194 | 36.748% |
| 101..200 | 45,159 | 24.697% |
| 201..500 | 8,493 | 4.645% |
| >500 | 264 | 0.144% |

- This view complements the granularity view: bimodality, unexpected peaks, or gaps that the category-based view cannot surface.
