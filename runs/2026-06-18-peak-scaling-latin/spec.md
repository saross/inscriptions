# §5 peak-vs-cumulative scaling — Latin frame (SPEC)

- **Status:** spec + run (Shawn pre-authorised this background follow-up,
  2026-06-17/18). Exploratory / tertiary (not preregistered; the cumulative H3a
  Latin is the confirmatory scaling result). No thresholds (Decision 13).
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-18.
- **Run dir:** `runs/2026-06-18-peak-scaling-latin/`.
- **Parent (all-provinces) run:** `runs/2026-06-17-s5-peak-scaling/` (Obs 100).

---

## 1. What this is — a frame swap, not new methodology

Latin-frame variant of the signed-off all-provinces §5 peak-scaling run. The
per-city peak-count construction (aoristic max over fixed-width bins), the H3a
non-centred Mundlak negative-binomial regression (NBR), the priors, the sampler
(tune 3000 / draws 2000 / 4 chains / target_accept 0.95, seed 20260617), and the
convergence gates (R̂ < 1.01, ESS ≥ 400, 0 div; warn-not-halt) are inherited
**verbatim** by importing the all-provinces module `peak_scaling.py`. The ONLY
change is restricting the city / province universe to the **Latin-minus-Roma**
diagnostic unit (Obs 41, Obs 101; Amendment 02).

## 2. Scope of the frame swap

The all-provinces run had three arms:

- **Arm A — raw aoristic peak, full 1044-city frame (the headline).** 50-year peak
  + 25-year window sensitivity.
- **Arm B + overlap — 268 "§5" cities** from the Layer-A trajectory
  `city-index.parquet` (modelled-peak vs raw-peak; a range-restriction probe).

**Only Arm A is a frame swap of the Latin universe.** The 268-city §5 arms are an
orthogonal subset — the Layer-A modelled-trajectory target set; in the
all-provinces run their low β (≈ 0.22) was diagnosed as **range restriction**, not
a real flattening (Obs 100). That subset is defined by the trajectory-modelling
pipeline, not by language, so it is **not** part of the Latin-frame definition.
This variant therefore runs **Arm A restricted to the Latin frame** (50y headline
+ 25y sensitivity) against the Latin cumulative β. The §5-subset arms are
intentionally out of scope.

## 3. The Latin frame — matches the H3a precedent EXACTLY

Universe = `data/processed/city_level_for_h3a_latin.parquet`
(`h3a_common.build_latin_frame`, Sensitivity B):

- **817 cities / 39 Latin provinces**, **Roma excluded**, **Mundlak recomputed
  over the Latin set** (`province_idx` re-indexed 0..38). Language assignment is
  externalised in `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`.

Peak counts are computed over the full corpus (inherited `aoristic_peak_counts`)
and mapped onto the Latin frame; non-Latin cities are dropped by the join.

### Count verification (anti-confabulation gate)

Verified 2026-06-18 against
`runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json` (817 / 39):

| Quantity | Latin frame | H3a precedent | Match |
|---|---|---|---|
| cities | 817 | 817 | ✓ |
| provinces | 39 | 39 | ✓ |
| Roma present | no | excluded | ✓ |

The driver **hard-stops** if the frame is not 817/39 or Roma is present.

## 4. Cumulative comparator

**Latin NBR β_within = 0.733 [0.648, 0.820]**, re-verified 2026-06-18 from
`runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc` (NOT the OLS log-log
slope 0.505 in `sr1-latin-results.json`).

## 5. Reported

`β_within` for: cumulative-Latin (0.733, reference), raw-peak-50y-Latin
(headline), raw-peak-25y-Latin (window sensitivity); a forest plot of the three.
Interpretation: is peak scaling ≈ cumulative on the Latin frame, as it was on
all-provinces (raw peak 0.557 ≈ cumulative 0.587; Obs 100)?

## 6. Caveats (inherited)

Exploratory / tertiary; not preregistered. Peak count is window-dependent (50y vs
25y both reported). Sampler exploratory; gates reported, warn-not-halt.

## 7. Compute

Sapphire; 2 NBR fits (MCMC) — a few minutes.
