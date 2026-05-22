# LIRE v3.0 — descriptive profile (summary)

Dataset: `LIRE_v3-0.parquet`. Rows: **182,853**. Columns: **63**. Primary key: `LIST-ID` (182,853 unique, 0 null).

## Headline findings

- **Dating coverage:** 182,853 of 182,853 rows (100.0%) have both `not_before` and `not_after`. Observed envelope: `not_before` ∈ [-430, 350]; `not_after` ∈ [-50, 2230].

- **Geolocation:** 182,853 of 182,853 rows (100.0%) have valid coordinates (both `Latitude` and `Longitude` non-null and in range).

- **Midpoint-inflation artefact:** ratio of observed century-midpoint counts to mean of adjacent years = **212.40×** (chi²=11350996.2, p=0). Strong overrepresentation at editorial century-midpoints is the SDAM-documented dating artefact.

- **Duplicate rows:** 0 exact duplicates across all columns; 0 duplicates on primary key `LIST-ID`.

- **High-null columns (>50% null):** 31 of 63.


## Per-subset highlights

- **province:** 66 distinct groups; threshold qualifying counts (100→53, 1000→30, 10000→2); largest group `Roma` with 65,457 rows.

- **urban-area:** 1,046 distinct groups; threshold qualifying counts (10→610, 100→171, 1000→10); largest group `Roma` with 65,452 rows.


## Artefact summary

- **Midpoint-inflation:** observed = 53,949; expected from adjacent years = 254.0; ratio = 212.40× (p=0).

- **Editorial spikes (aggregate not_before chi²):** 48.8, p=2.89e-12.

- **Coordinate precision:** 71.5% of non-null coordinate values have >4 decimal places (false-precision indicator).

- **Outlier coordinates:** lat |·|>90 = 0; lon |·|>180 = 0.

- **Negative date_range (not_before > not_after):** 0.

- **date_range > 500 years:** 264.

- **Temporal envelope outliers (against conservative [-700, 700]):** not_before=0, not_after=4.

- **`is_within_RE` / `is_geotemporal`:** could not run — columns absent from LIRE v3.0 schema.


## Cross-references

- `profile-province.md`, `profile-urban-area.md`

- `artefacts.md`

- `claims.jsonl` — machine-readable claim ledger backing every number in these reports.

- `tables/*.csv` — backing data for every table.

- `decisions.md` — judgement-call audit trail.
