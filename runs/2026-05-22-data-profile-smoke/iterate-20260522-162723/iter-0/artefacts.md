# Artefact checks — LIRE v3.0

## midpoint-inflation

- Rows whose midpoint = century-midpoint year: **53,949**
- Rows whose midpoint = adjacent-to-century-midpoint year (±1): **508** (sum across both adjacents)
- Expected at century-midpoints if uniform: **254.0**
- Observed/expected ratio: **212.40×**
- Chi² (1 d.o.f.): **11350996.16**, p = **0**
- Interpretation: ratios substantially above 1.0 indicate the century-basis editorial dating artefact (SDAM).

## editorial-spikes

| Year | nb obs | nb adj mean | nb ratio | na obs | na adj mean | na ratio |
|-----:|------:|-----------:|--------:|------:|-----------:|--------:|
| -14 | 20 | 243.5 | 0.08 | 14 | 20.5 | 0.68 |
| 27 | 19 | 75.0 | 0.25 | 17 | 12.0 | 1.42 |
| 96 | 113 | 67.0 | 1.69 | 559 | 261.0 | 2.14 |
| 97 | 118 | 299.5 | 0.39 | 500 | 321.0 | 1.56 |
| 192 | 33 | 304.5 | 0.11 | 221 | 62.0 | 3.56 |
| 193 | 465 | 54.0 | 8.61 | 77 | 139.0 | 0.55 |
| 235 | 121 | 79.5 | 1.52 | 716 | 52.5 | 13.64 |

Aggregate chi² (not_before, sum over editorial years): **48.76**, p = **2.89e-12**.


## coordinate-precision

| Decimal places | Count |
|---------------:|------:|
| 0 | 80 |
| 1 | 372 |
| 2 | 1,671 |
| 3 | 7,936 |
| 4 | 94,163 |
| >4 | 261,484 |

>4 decimal places dominate at 71.5% of non-null coordinate values; this is the false-precision indicator.

## outlier-coordinates

- |Latitude| > 90: **0**
- |Longitude| > 180: **0**


## null-profile

- Columns with null_rate > 50%: **31**
- Full per-column null table: `tables/column-stats.csv`

- High-null columns: `tables/artefact-high-null-columns.csv`


## duplicate-rows

- Exact-duplicates across all columns: **0**
- Duplicates on primary key `LIST-ID`: **0**


## negative-date-range

- Rows where `not_before > not_after`: **0**


## date-range-extreme

- Rows where `date_range > 500`: **264**


## temporal-outliers

- Conservative envelope used (none supplied): [-700, 700]
- `not_before` outside envelope: **0**
- `not_after` outside envelope: **4**
- Observed range `not_before`: [-430, 350]
- Observed range `not_after`: [-50, 2230]


## geolocated-rate

- Rows with valid coordinates: **182,853** of 182,853 = **100.0%**


## is_within_RE-rate / is_geotemporal-rate

Could not run: columns `is_within_RE` and `is_geotemporal` are absent from the LIRE v3.0 schema. See `decisions.md`.


## Unexpected-pattern diagnostic

### Granularity histogram

| Bucket | Count | Share of dated |
|:-------|------:|--------------:|
| exact-0 | 8,279 | 4.5% |
| exact-25 | 172 | 0.1% |
| exact-50 | 631 | 0.3% |
| exact-100 | 662 | 0.4% |
| exact-200 | 170 | 0.1% |
| exact-500 | 0 | 0.0% |
| other-multiples-of-10 | 4,422 | 2.4% |
| other | 168,517 | 92.2% |

### Date-range distribution (broad)

| Bin (years) | Count | Share |
|:------------|------:|------:|
| 0 | 8,279 | 4.5% |
| 1-25 | 17,883 | 9.8% |
| 26-50 | 35,581 | 19.5% |
| 51-100 | 67,194 | 36.7% |
| 101-200 | 45,159 | 24.7% |
| 201-500 | 8,493 | 4.6% |
| >500 | 264 | 0.1% |
