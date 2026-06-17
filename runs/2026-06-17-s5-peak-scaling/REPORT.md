# §5 Peak-inscription vs Hanson-population scaling — RESULTS

- **Status:** COMPLETE (exploratory / tertiary; not preregistered).
- **Run:** sapphire, 2026-06-17; 4 NBR fits, all converged (R̂ = 1.0000, 0 div).
  `code/peak_scaling.py`; log `run.log`. Figure `outputs/peak-scaling-forest.png`.

---

## 1. Question

Does *peak* inscription intensity scale with (Hanson, peak) population, and is the
exponent different from the **cumulative** H3a scaling `β_within = 0.587 [0.519,
0.657]`?

## 2. Results

| Arm | β_within [95% CI] | n cities |
|---|---|---|
| cumulative (H3a, reference) | **0.587** [0.519, 0.657] | 1044 |
| **raw peak, 50y, all 1044** (headline) | **0.557** [0.490, 0.624] | 1044 |
| raw peak, 25y, all 1044 | 0.545 [0.479, 0.612] | 1044 |
| raw peak, 25y, 268 §5 cities | 0.223 [0.130, 0.319] | 268 |
| modelled peak, 25y, 268 §5 cities | 0.213 [0.112, 0.314] | 268 |

## 3. Two findings

1. **Peak intensity scales with population essentially like cumulative output.**
   On the full 1044-city frame, the peak-scaling exponent (0.557 at 50y, 0.545 at
   25y) is **statistically indistinguishable from the cumulative 0.587** (CIs
   overlap heavily) — marginally flatter, not significantly. *Answer to the
   original question:* yes, peak production scales with Hanson population, at ≈ the
   same exponent as total production. Bigger cities have proportionally higher
   peaks **and** higher totals, by the same law.

2. **The overlap contrast: smoothing does not bias the exponent; the §5 subset
   attenuates it (range restriction).** On the 268 §5 cities, raw-peak (0.223)
   and modelled-peak (0.213) β's are **the same** — the Layer-A smoothing leaves
   the peak-scaling exponent unchanged (the contrast Shawn asked for). The much
   lower value vs the full corpus (0.22 vs 0.55, *same* window and measure, only
   the city set differs) is a **range-restriction artefact**: the §5 target set
   excludes the largest cities (N ≥ 1549 anchors) and the smallest (N < 50), so
   its truncated population range attenuates the within-province slope. **Do not
   read 0.22 as "peak scaling is flat"** — it is the restricted-set slope; the
   unrestricted answer is finding 1.

## 4. Caveats

- Exploratory / tertiary; not preregistered (the cumulative H3a is the
  confirmatory scaling result).
- Arm B uses the posterior-**median** modelled peak; the Layer-A trajectory
  posterior is not propagated into `β^peak,modelled` (documented simplification;
  the raw≈modelled agreement makes this immaterial here).
- Peak count is window-dependent (50y vs 25y both reported; nearly identical).
- §5-subset arms attenuated by range restriction (finding 2).

## 5. Outputs

`outputs/peak-scaling-summary.json` (all arms + contrasts + provenance),
`outputs/peak-scaling-forest.png`.

## 6. Bottom line

Peak inscription intensity scales with Hanson population at β ≈ 0.56 — the same
law as cumulative output (0.587). The Layer-A smoothing does not change the
exponent; the apparent flattening on the §5 subset is range restriction, not a
real effect. The cumulative H3a result stands as the scaling headline; the peak
variant corroborates rather than complicates it.
