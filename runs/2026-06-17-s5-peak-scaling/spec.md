# §5 Peak-inscription vs Hanson-population scaling (SPEC)

- **Status:** spec + run (Shawn directed both arms + overlap contrast,
  2026-06-17). Exploratory / tertiary (not preregistered; the cumulative H3a is
  the confirmatory scaling result).
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-17.
- **Run dir:** `runs/2026-06-17-s5-peak-scaling/`.

---

## 1. Question

H3a's confirmatory scaling uses **cumulative** inscription counts:
`β_within^cumulative = 0.587 [0.519, 0.657]`. This run asks the distinct question
**does *peak* inscription intensity scale with (Hanson, peak) population, and is
the exponent different?** — i.e. do larger cities have proportionally higher
*peaks*, or merely higher *totals*?

Method: per-city peak inscription measure → the same H3a non-centred Mundlak NBR
→ `β_within^peak`, contrasted with 0.587.

## 2. Two arms + overlap contrast (Shawn's direction)

- **Arm A — raw aoristic peak, all 1044 cities (headline).** Per-city peak count
  = max over **50-year** periods of the aoristic-apportioned, rounded count
  (reusing the H7 builder). Full H3a 1044-city frame + the parquet's
  population-based Mundlak. Directly comparable to `β^cumulative` (same cities,
  same NBR). Also fit a **25-year** peak (window sensitivity).
- **Arm B — modelled trajectory peak, 268 §5 cities.** Per-city peak count =
  `round(max_t median(lam))` from the Layer-A posterior (25y native). NBR with
  Mundlak recomputed over the 268-city subset.
- **Overlap contrast (268 §5 cities, 25y):** raw-25y-peak vs modelled-25y-peak,
  same cities + Mundlak → isolates the effect of the Layer-A smoothing on the
  peak-scaling exponent.

## 3. Reported

`β_within` for: cumulative (0.587, reference), raw-peak-50y-1044 (headline),
raw-peak-25y-1044, raw-peak-25y-268, modelled-peak-25y-268. A forest plot of all
five. Interpretation: peak-scaling vs cumulative-scaling; smoothing effect on the
overlap set.

## 4. Design notes / caveats

- **Arm B does not propagate the Layer-A trajectory posterior** into
  `β^peak,modelled` (uses the posterior-median peak); a documented simplification
  for an exploratory contrast. (Full propagation = NBR per draw, deferred.)
- Mundlak recomputed over each city set (project convention: centring is
  sample-relative). 1044 arms use the parquet's full-set centring.
- Peak count depends on window width (25y vs 50y) — both reported.
- Sampler: tune 3000 / draws 2000 / 4 chains / target_accept 0.95 (exploratory);
  gates reported, warn-not-halt.
- Tertiary / not preregistered; descriptive contrast, not a confirmatory test.

## 5. Inputs

- `data/processed/city_level_for_h3a.parquet` (1044-city frame + Mundlak).
- Raw LIRE via `h3a_common.load_filtered_lire` (per-period aoristic counts).
- Layer-A posterior `monolithic-inscription-25y.nc` (modelled peak; on sapphire).
- `runs/2026-05-30-.../code/prepared/city-index.parquet` (268-city pop/province).

## 6. Compute

Sapphire; 4 NBR fits (MCMC) — background, a few minutes.
