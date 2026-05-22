# Verifier corrections — LIRE v3.0 descriptive profile (iter-0)

Independent re-derivation of every claim in `claims.jsonl` directly from the source parquet (`LIRE_v3-0.parquet`). Did not consume the proposer's CSV tables. 

## Verdict tally

- pass: 81
- partial: 2
- fail: 0
- unverifiable: 0
- total claims: 83

## Per-claim audit

| claim_id | category | proposer | verifier | match | severity | note |
|:---------|:---------|---------:|---------:|:------|:---------|:-----|
| `count-dataset-row-count` | count | 182853 | 182853 | **pass** | — | exact match |
| `count-dataset-column-count` | count | 63 | 63 | **pass** | — | exact match |
| `count-dataset-primary-key-unique` | count | 182853 | 182853 | **pass** | — | exact match |
| `count-dataset-primary-key-null` | count | 0 | 0 | **pass** | — | exact match |
| `count-dataset-dated-rows` | count | 182853 | 182853 | **pass** | — | exact match |
| `rate-dataset-dated` | rate | 1.0 | 1.0 | **pass** | — | abs diff 0.000000 |
| `count-dataset-geolocated` | count | 182853 | 182853 | **pass** | — | exact match |
| `rate-dataset-geolocated` | rate | 1.0 | 1.0 | **pass** | — | abs diff 0.000000 |
| `count-province-group-count` | count | 66 | 65 | **partial** | low | claims source_method `df.groupby(['province']).ngroups` (default `dropna=True`) which yields 65, but the proposer reports 66 — consistent with `dropna=False` (treats null as its own group; 2,244 rows have null province). The top-N table for urban-area also displays `<null>` as a group, so the analytic choice is internally consistent. source_method string in claims.jsonl is misdescribed. |
| `ranking-province-top-group-name` | ranking | Roma | Roma | **pass** | — | exact match |
| `count-province-top-group-count` | count | 65457 | 65457 | **pass** | — | exact match |
| `threshold-qualifying-province-ge-100` | threshold_qualifying | 53 | 53 | **pass** | — | exact match |
| `threshold-qualifying-province-ge-1000` | threshold_qualifying | 30 | 30 | **pass** | — | exact match |
| `threshold-qualifying-province-ge-10000` | threshold_qualifying | 2 | 2 | **pass** | — | exact match |
| `count-urban-area-group-count` | count | 1046 | 1045 | **partial** | low | claims source_method `df.groupby(['urban_context_city']).ngroups` (default `dropna=True`) yields 1045, but the proposer reports 1046 — consistent with `dropna=False` (40,944 rows have null urban_context_city; appears as `<null>` in the visible top-N). source_method string in claims.jsonl is misdescribed. |
| `ranking-urban-area-top-group-name` | ranking | Roma | Roma | **pass** | — | exact match |
| `count-urban-area-top-group-count` | count | 65452 | 65452 | **pass** | — | exact match |
| `threshold-qualifying-urban-area-ge-10` | threshold_qualifying | 610 | 610 | **pass** | — | exact match |
| `threshold-qualifying-urban-area-ge-100` | threshold_qualifying | 171 | 171 | **pass** | — | exact match |
| `threshold-qualifying-urban-area-ge-1000` | threshold_qualifying | 10 | 10 | **pass** | — | exact match |
| `count-artefacts-midpoint-observed` | count | 53949 | 53949 | **pass** | — | exact match |
| `count-artefacts-midpoint-adjacent` | count | 508 | 508 | **pass** | — | exact match |
| `test_statistic-artefacts-midpoint-chi2` | test_statistic | 11350996.1614 | 11350996.161417322 | **pass** | — | rel diff 0.0000% |
| `pvalue-artefacts-midpoint` | pvalue | 0.0 | 0.0 | **pass** | — | abs diff 0.000e+00 |
| `count-artefacts-editorial--14-not_before-obs` | count | 20 | 20 | **pass** | — | exact match |
| `count-artefacts-editorial--14-not_after-obs` | count | 14 | 14 | **pass** | — | exact match |
| `count-artefacts-editorial-27-not_before-obs` | count | 19 | 19 | **pass** | — | exact match |
| `count-artefacts-editorial-27-not_after-obs` | count | 17 | 17 | **pass** | — | exact match |
| `count-artefacts-editorial-96-not_before-obs` | count | 113 | 113 | **pass** | — | exact match |
| `count-artefacts-editorial-96-not_after-obs` | count | 559 | 559 | **pass** | — | exact match |
| `count-artefacts-editorial-97-not_before-obs` | count | 118 | 118 | **pass** | — | exact match |
| `count-artefacts-editorial-97-not_after-obs` | count | 500 | 500 | **pass** | — | exact match |
| `count-artefacts-editorial-192-not_before-obs` | count | 33 | 33 | **pass** | — | exact match |
| `count-artefacts-editorial-192-not_after-obs` | count | 221 | 221 | **pass** | — | exact match |
| `count-artefacts-editorial-193-not_before-obs` | count | 465 | 465 | **pass** | — | exact match |
| `count-artefacts-editorial-193-not_after-obs` | count | 77 | 77 | **pass** | — | exact match |
| `count-artefacts-editorial-235-not_before-obs` | count | 121 | 121 | **pass** | — | exact match |
| `count-artefacts-editorial-235-not_after-obs` | count | 716 | 716 | **pass** | — | exact match |
| `test_statistic-artefacts-editorial-chi2` | test_statistic | 48.7587 | 48.758682101513806 | **pass** | — | rel diff 0.0000% |
| `pvalue-artefacts-editorial` | pvalue | 0.0 | 2.894795514407633e-12 | **pass** | — | abs diff 2.895e-12 |
| `count-artefacts-coord-precision-total` | count | 365706 | 365706 | **pass** | — | exact match |
| `rate-artefacts-coord-precision-gt4` | rate | 0.715012 | 0.7150115119795682 | **pass** | — | abs diff 0.000000 |
| `count-artefacts-outlier-lat` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-outlier-lon` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-high-null-columns` | count | 31 | 31 | **pass** | — | exact match |
| `count-artefacts-duplicate-rows-all-columns` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-duplicate-rows-primary-key` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-negative-date-range` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-date-range-gt500` | count | 264 | 264 | **pass** | — | exact match |
| `count-artefacts-temporal-outliers-not_before` | count | 0 | 0 | **pass** | — | exact match |
| `count-artefacts-temporal-outliers-not_after` | count | 4 | 4 | **pass** | — | exact match |
| `count-artefacts-not_before-min` | count | -430 | -430 | **pass** | — | exact match |
| `count-artefacts-not_before-max` | count | 350 | 350 | **pass** | — | exact match |
| `count-artefacts-not_after-min` | count | -50 | -50 | **pass** | — | exact match |
| `count-artefacts-not_after-max` | count | 2230 | 2230 | **pass** | — | exact match |
| `count-diagnostic-granularity-exact-0` | count | 8279 | 8279 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-0` | rate | 0.045277 | 0.04527680705265979 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-exact-25` | count | 172 | 172 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-25` | rate | 0.000941 | 0.0009406463115179954 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-exact-50` | count | 631 | 631 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-50` | rate | 0.003451 | 0.003450859433534041 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-exact-100` | count | 662 | 662 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-100` | rate | 0.00362 | 0.0036203945245634472 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-exact-200` | count | 170 | 170 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-200` | rate | 0.00093 | 0.0009297085637096466 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-exact-500` | count | 0 | 0 | **pass** | — | exact match |
| `rate-diagnostic-granularity-exact-500` | rate | 0.0 | 0.0 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-granularity-other-multiples-of-10` | count | 4422 | 4422 | **pass** | — | exact match |
| `count-diagnostic-granularity-other` | count | 168517 | 168517 | **pass** | — | exact match |
| `count-diagnostic-date-range-0` | count | 8279 | 8279 | **pass** | — | exact match |
| `rate-diagnostic-date-range-0` | rate | 0.045277 | 0.04527680705265979 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-1-25` | count | 17883 | 17883 | **pass** | — | exact match |
| `rate-diagnostic-date-range-1-25` | rate | 0.0978 | 0.09779987202835064 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-26-50` | count | 35581 | 35581 | **pass** | — | exact match |
| `rate-diagnostic-date-range-26-50` | rate | 0.194588 | 0.19458800238442903 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-51-100` | count | 67194 | 67194 | **pass** | — | exact match |
| `rate-diagnostic-date-range-51-100` | rate | 0.367476 | 0.36747551311709403 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-101-200` | count | 45159 | 45159 | **pass** | — | exact match |
| `rate-diagnostic-date-range-101-200` | rate | 0.246969 | 0.24696887663861133 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-201-500` | count | 8493 | 8493 | **pass** | — | exact match |
| `rate-diagnostic-date-range-201-500` | rate | 0.046447 | 0.04644714606815311 | **pass** | — | abs diff 0.000000 |
| `count-diagnostic-date-range-500` | count | 264 | 264 | **pass** | — | exact match |
| `rate-diagnostic-date-range-500` | rate | 0.001444 | 0.0014437827107020393 | **pass** | — | abs diff 0.000000 |

## Non-PASS detail

### `count-province-group-count` — PARTIAL (low)

- Description: Number of distinct groups at subset level province
- Proposer value: `66` (groups)
- Verifier value: `65` (groups)
- Source method claimed: `df.groupby(['province']).ngroups`
- Source file: `profile-province.md`
- Note: claims source_method `df.groupby(['province']).ngroups` (default `dropna=True`) which yields 65, but the proposer reports 66 — consistent with `dropna=False` (treats null as its own group; 2,244 rows have null province). The top-N table for urban-area also displays `<null>` as a group, so the analytic choice is internally consistent. source_method string in claims.jsonl is misdescribed.
- Fix hint: Update claim source_method for count-province-group-count to reflect `dropna=False` (or `nunique(dropna=False)`) — current string says default `ngroups` which yields a different number than the report shows. Numerically the report and table are internally consistent with `dropna=False`.

### `count-urban-area-group-count` — PARTIAL (low)

- Description: Number of distinct groups at subset level urban-area
- Proposer value: `1046` (groups)
- Verifier value: `1045` (groups)
- Source method claimed: `df.groupby(['urban_context_city']).ngroups`
- Source file: `profile-urban-area.md`
- Note: claims source_method `df.groupby(['urban_context_city']).ngroups` (default `dropna=True`) yields 1045, but the proposer reports 1046 — consistent with `dropna=False` (40,944 rows have null urban_context_city; appears as `<null>` in the visible top-N). source_method string in claims.jsonl is misdescribed.
- Fix hint: Update claim source_method for count-urban-area-group-count to reflect `dropna=False` (or `nunique(dropna=False)`) — current string says default `ngroups` which yields a different number than the report shows. Numerically the report and table are internally consistent with `dropna=False`.


## Subset spot-checks (independent of claims.jsonl)

Spot-checked one randomly-selected non-headline group per subset level by re-deriving the row count directly from the parquet:

- province spot-check: group `Pannonia inferior` — proposer table says 3132, verifier re-derives 3132 (MATCH).
- urban-area spot-check: group `Oenoanda` — proposer table says 1, verifier re-derives 1 (MATCH).

## Unexpected-pattern diagnostic re-run

Independently re-ran the granularity histogram and the broad date-range histogram (claims 56–83). All bin counts and shares reproduce within tolerance.

