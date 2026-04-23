# LIRE v3.0 descriptive profile (2026-04-23 rerun, comprehensive)

## Headline findings

1. The LIRE v3.0 parquet at `archive/data-2026-04-22/LIRE_v3-0.parquet` contains 182,853 rows × 65 columns and is consistent with the first run's 182,853 count.
2. `negative-date-range` = **0** — this matches the LIRE v3.0 release-note claim of zero negative ranges; previous LIRE versions had transposed endpoints that Shawn reported to the maintainers.
3. Midpoint-inflation at century boundaries (AD 50/150/250/350) shows observed/expected ratios of 22.83, 41.50, 18.82, 39.70 under the aoristic-probability null; Westfall-Young adjusted p-values: 0, 0, 0, 0.
4. Editorial-spikes at year AD 97: the two endpoint variants confirm the first-run finding that year 97 is a dip, not a spike, under the aoristic null. Direction and adjusted p-values in `artefacts.md`.
5. Subset-level qualification: at threshold n ≥ 25, `province` has 59 qualifying groups covering 100.0% of the corpus. Full sweep in `tables/subset-summary.csv`.

## Historical context — negative-date-range

Previous LIRE versions had transposed `not_before`/`not_after` dates that produced negative ranges. Shawn reported these to the LIRE maintainers; LIRE v3.0 release notes claim zero negatives. This run verifies: **0 negative-range rows observed.** If non-zero, this would halt the run.

## Historical context — temporal-outliers

LIRE uses an overlap-filter semantics for the stated 50 BC – AD 350 envelope (a row is included if its `[not_before, not_after]` interval intersects the envelope at any point), not a strict containment filter. The re-verified counts under a containment interpretation are: 
- 1,949 rows with `not_before` < -50 (top-10 most extreme `not_before`: [-430.0, -400.0, -370.0, -300.0, -300.0, -300.0, -300.0, -300.0, -300.0, -300.0]).
- 32,615 rows with `not_after` > 350 (top-10 most extreme `not_after`: [2230.0, 2009.0, 800.0, 730.0, 700.0, 700.0, 700.0, 700.0, 700.0, 700.0]).
- 34,562 rows with at least one endpoint outside the envelope.
- 182,853 rows with intervals overlapping the envelope.

The AD 2230 placeholder values are a known upstream bug reported to the LIRE team; AD 700 values may be plausible under LIRE's extended envelope (verify with upstream maintainers).

## Schema check

- Schema rows: 66; parquet columns: 65.
- Schema-only (absent from parquet): ['is_geotemporal', 'is_within_RE', 'material_EDCS'].
- Parquet-only (absent from schema): none.
- The two artefact checks dependent on schema-only columns (`is_within_RE-rate`, `is_geotemporal-rate`) are marked NOT RUN in `artefacts.md`. A derived geolocated × has-date rate is reported in artefacts.md at 1.000.

## Methodology notes

- **Aoristic-probability null** (Ratcliffe 2002; Crema 2012) is used for all MC permutation tests on temporal artefact checks. For each row, aoristic weight at year Y is 1/date_range within `[not_before, not_after]` and zero outside; expected count at Y is the sum of weights; null resampling draws each row's midpoint uniformly within its own interval.
- **Westfall-Young stepdown** is the primary multiple-comparison correction (uses the joint null distribution); **Holm-Bonferroni** is reported as a companion sanity-check.
- **Cliff's delta** + **Vargha-Delaney A** are the primary effect-size measures for distribution comparisons (Cliff's delta on date_range for Roma vs Provincia incerta = 0.070; Vargha-Delaney A = 0.535).
- **BCa bootstrap**, 20,000 resamples, is used for interval estimation; percentile-bootstrap CIs are reported alongside for subsets with n < 50.
- `joblib.Parallel(n_jobs=-1)` runs the resample loops.

## Deferred categories

All comprehensive-mode categories listed in the brief were executed: distribution-shape, temporal-coverage, categorical-distributions, concentration, text-statistics, correlations, null-cooccurrence, drill-downs, sensitivity-sweep. None were skipped.

## Run metadata

- Random seed: `20260423`
- Bootstrap resamples: `20000` (capped at 2,000 for ratio CIs in MC tests to manage wall-clock)
- Permutation resamples: `20000`
- n_jobs: `-1` (effective cores set by joblib default)
