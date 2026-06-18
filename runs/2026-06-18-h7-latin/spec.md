# §5 H7-Latin — per-period (time-resolved) H3c, Latin frame (SPEC)

- **Status:** spec + run (Shawn pre-authorised this background follow-up,
  2026-06-17/18). Exploratory (prereg §5 line 384; no thresholds, Decision 13).
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-18.
- **Run dir:** `runs/2026-06-18-h7-latin/`.
- **Parent (all-provinces) run:** `runs/2026-06-17-s5-h7-perperiod-h3c/` (Obs 99).

---

## 1. What this is — a frame swap, not new methodology

This is the **Latin-frame variant** of the signed-off all-provinces §5 H7
(time-resolved per-period H3c). Every modelling choice is inherited **verbatim**
by importing the all-provinces module `h7_perperiod_h3c.py` and calling its
functions unchanged: the 8 × 50-year period grid, the aoristic apportionment, the
H3a non-centred Mundlak negative-binomial regression (NBR), the H3c diagnostics
(provincial-capital residual contrast `P(contrast > 0)`; Moran's I spatial
clustering, k ∈ {5, 8, 10}), the priors, the sampler (tune 3000 / draws 2000 /
4 chains / target_accept 0.95, seed 20260617), and the convergence gates
(R̂ < 1.01, bulk-ESS ≥ 400, 0 divergences; warn-not-halt per period).

**The ONLY change is the city / province universe.** All-provinces used the
1044-city / 56-province primary frame; this variant uses the
**Latin-speaking-provinces-minus-Roma** diagnostic unit.

## 2. The Latin frame — matches the H3a confirmatory precedent EXACTLY

Universe = `data/processed/city_level_for_h3a_latin.parquet`, the canonical
Sensitivity-B Latin frame emitted by
`runs/2026-06-04-h3a-confirmatory/code/h3a_common.build_latin_frame`:

- **817 cities / 39 Latin provinces** (the language assignment is externalised in
  `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`).
- **Roma excluded.** Roma is dropped at the primary-frame stage (the `rome_mask`
  predicate `urban_context_city == 'roma'`), so the Latin frame is already
  "Latin-minus-Roma" — exactly the diagnostic unit (Obs 41, Obs 101).
- **Mundlak within / between predictors recomputed over the Latin-only set**
  (correct sample-relative centring; within-deviations sum to 0 per province),
  with `province_idx` re-indexed 0..38.

Per-period aoristic counts are computed over the full Hanson corpus (inherited
`aoristic_period_counts`) and **mapped onto the Latin city set**; cities not in
the Latin frame are dropped by the join — the same mechanism the all-provinces
driver uses for its 1044 universe. Coordinates and the capital set are likewise
restricted to the Latin frame.

### Count verification (anti-confabulation gate)

Verified 2026-06-18 against the H3a precedent
`runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json`
(`latin_n_cities: 817`, `latin_n_provinces: 39`):

| Quantity | Latin frame | H3a precedent | Match |
|---|---|---|---|
| cities | 817 | 817 | ✓ |
| provinces | 39 | 39 | ✓ |
| Roma present | no | excluded | ✓ |
| capitals in frame | 41 (of 62 total) | — | (sufficient for contrast) |
| cumulative count (Σ inscription_count) | 72,006 | — | — |

The driver **hard-stops** if the frame is not 817/39 or if Roma is present.

## 3. Cumulative comparator

The relevant cumulative scaling exponent for this NBR-based analysis is the
**Latin NBR β_within = 0.733 [0.648, 0.820]**, re-verified 2026-06-18 from
`runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc` (NOT the OLS log-log
slope 0.505 in `sr1-latin-results.json`, which is a different, simpler estimator).

## 4. Deliverables

`outputs/`: `h7-latin-summary.json` (per-period counts, convergence, β_within,
capital contrast, Moran's I per k; frame provenance + comparator),
`h7-latin-per-city-residuals.parquet`, `h7-latin-time-resolved.png`, and the
per-period NBR posteriors `h7-latin-idata-*.nc` (regenerable; large).

## 5. Compare to all-provinces (Obs 99)

All-provinces headline: β_within U-shape (0.70 → ~0.58 high-empire plateau →
0.66 4th c.); capitals over-produce every period (P = 1.00); residual clustering
significant only in the earliest period. The Latin variant asks: does the U-shape
persist on Latin? capital over-production? early-only clustering? — all read
descriptively, no thresholds.

## 6. Caveats (inherited)

Exploratory, no published comparator, no thresholds. 50-year periods (not literal
decadal — feasibility). Aoristic-rounded counts (midpoint an unrun sensitivity).
Sparse early/late periods may pool province intercepts; convergence reported per
period.

## 7. Compute

Sapphire; 8 NBR fits (MCMC) sequentially — tens of minutes.
