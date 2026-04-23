# Artefact checks

## Midpoint-inflation (aoristic-probability null, Westfall-Young + Holm)

| year | observed | expected_aoristic | ratio | 95% CI | raw_p | WY-p | Holm-p |
|---|---|---|---|---|---|---|---|
| 50 | 12091 | 529.6 | 22.832 | [22.363, 23.285] | 5e-05 | 0 | 0.0002 |
| 150 | 19861 | 478.6 | 41.495 | [40.489, 42.478] | 5e-05 | 0 | 0.0002 |
| 250 | 7206 | 382.9 | 18.819 | [17.992, 19.614] | 5e-05 | 0 | 0.0002 |
| 350 | 12685 | 319.5 | 39.700 | [38.518, 40.863] | 5e-05 | 0 | 0.0002 |

## Editorial-spikes

| year | endpoint | direction | observed | expected | ratio | 95% CI | raw_p | WY-p | Holm-p |
|---|---|---|---|---|---|---|---|---|---|
| -14 | not_before | dip | 20 | 156.9 | 0.127 | [0.077, 0.182] | 5e-05 | 0.0001 | 0.00035 |
| 27 | not_before | dip | 19 | 491.2 | 0.039 | [0.023, 0.058] | 5e-05 | 0.0001 | 0.00035 |
| 97 | not_before | dip | 118 | 469.9 | 0.251 | [0.209, 0.292] | 5e-05 | 0.0001 | 0.00035 |
| 192 | not_before | dip | 33 | 525.8 | 0.063 | [0.041, 0.085] | 5e-05 | 0.0001 | 0.00035 |
| 193 | not_before | dip | 465 | 559.2 | 0.832 | [0.767, 0.900] | 5e-05 | 0.0001 | 0.00035 |
| 212 | not_before | spike | 870 | 595.4 | 1.461 | [1.384, 1.535] | 5e-05 | 0.0001 | 0.00035 |
| 235 | not_before | dip | 121 | 385.9 | 0.314 | [0.265, 0.361] | 5e-05 | 0.0001 | 0.00035 |
| -14 | not_after | dip | 14 | 156.9 | 0.089 | [0.046, 0.134] | 5e-05 | 0.6488 | 0.00035 |
| 27 | not_after | dip | 17 | 491.2 | 0.035 | [0.019, 0.052] | 5e-05 | 0.6488 | 0.00035 |
| 97 | not_after | spike | 500 | 469.9 | 1.064 | [0.977, 1.149] | 0.1386 | 0.6488 | 0.1386 |
| 192 | not_after | dip | 221 | 525.8 | 0.420 | [0.369, 0.472] | 5e-05 | 0.6488 | 0.00035 |
| 193 | not_after | dip | 77 | 559.2 | 0.138 | [0.110, 0.166] | 5e-05 | 0.6488 | 0.00035 |
| 212 | not_after | dip | 99 | 595.4 | 0.166 | [0.136, 0.196] | 5e-05 | 0.6488 | 0.00035 |
| 235 | not_after | spike | 716 | 385.9 | 1.855 | [1.733, 1.985] | 5e-05 | 0.6488 | 0.00035 |

## Coordinate-precision
- Latitude mean decimal places: 6.03; median: 7.0
- Longitude mean decimal places: 6.14; median: 7.0

## Outlier coordinates
- Lat out of range: 0
- Lon out of range: 0
- Outside Mediterranean bbox ([20,60]°N × [-15,50]°E): 0 (0.000)

## Null profile (top 10)

| column | null_rate |
|---|---|
| language_EDCS | 1.000 |
| inscr_process | 0.939 |
| year_of_find | 0.853 |
| letter_size | 0.851 |
| support_material | 0.846 |
| depth_cm | 0.840 |
| present_location | 0.798 |
| width_cm | 0.791 |
| height_cm | 0.789 |
| support_objecttype | 0.748 |

## Duplicate rows
- Duplicated on `LIST-ID`: 0
- Duplicated on full row: 0

## Negative date range
- Count: **0** (LIRE v3.0 release claims zero; verified)

## Date range extreme
- min / median / mean / max: 1 / 100 / 102.3 / 2060 yr
- 95th pct / 99th pct: 200 / 300
- Exactly 0 / 1 / 2 / 3 / 100 / 101 / 201 yr: 0 / 8279 / 2790 / 1434 / 47761 / 662 / 170

## Temporal outliers
- `not_before` < -50: 1,949
- `not_after` > 350: 32,615
- Either endpoint outside envelope: 34,562
- Interval overlaps envelope: 182,853
- Top-10 most extreme `not_after`: [2230.0, 2009.0, 800.0, 730.0, 700.0, 700.0, 700.0, 700.0, 700.0, 700.0]
- Top-10 most extreme `not_before`: [-430.0, -400.0, -370.0, -300.0, -300.0, -300.0, -300.0, -300.0, -300.0, -300.0]

## Geolocated / is_geotemporal
- Geolocated rate (Latitude ∧ Longitude not null): 1.000
- Derived geotemporal rate (coords ∧ at-least-one-date): 1.000
- **is_within_RE-rate: NOT RUN** --- column `is_within_RE` absent from parquet (see decisions.md)
- **is_geotemporal-rate: NOT RUN** --- column `is_geotemporal` absent from parquet (see decisions.md)
