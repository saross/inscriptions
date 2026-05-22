# Decisions log — LIRE v3.0 descriptive profile (first run)

Every judgement call encountered during the profiling run. Each entry records: fact observed, default applied, alternatives considered, rationale, and whether the call warrants investigator review.

## Schema validation (non-breaking)

**Fact:** All invocation-referenced columns present. Dataset has 63 columns; the invocation references only the subset above plus the primary key. Columns `is_within_RE` and `is_geotemporal` named in the default artefact-check catalogue are absent.

**Default applied:** Flag-and-continue per decision-point discipline. Report the corresponding checks as `could not run` with reason `column absent`.

**Investigator review:** Not required; these columns are not part of the LIRE v3.0 schema.

## Temporal envelope absent from invocation

**Fact:** The `temporal-outliers` check requires a stated temporal envelope (e.g., [-50, 350] for LIRE) to be meaningful. None was provided.

**Default applied:** Report observed min/max of `not_before` and `not_after` and flag rows outside an empirically-conservative envelope of [-700, 700] (anything outside that window for a Latin epigraphic corpus is almost certainly a data-entry artefact).

**Investigator review:** Recommended — the project should specify the canonical envelope so future runs are not threshold-arbitrary.

## Subset threshold boundary unusual (province)

**Fact:** 2 groups qualify at the highest threshold (10000) for subset level province.

**Default applied:** Flag-and-continue.

**Investigator review:** Recommended — threshold may be mis-set if downstream analysis needs a particular cohort size.

## Unexpected-pattern diagnostic — no >5% anomalies

**Fact:** No granularity bucket exceeded the 5% flag threshold (after standard buckets). Default applied: continue with full report. Investigator review not required.
