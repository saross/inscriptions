# §5 B4 — stratified-sampling sensitivity (v2-faithful) — DRAFT

> **⚠ FORWARD POINTER — the "MATERIAL — re-run warranted" verdict below WAS
> resolved.** The §"Verdict — MATERIAL" call (that the balanced width pool could
> shift the thresholds, so a targeted re-run was warranted) was acted on: the
> re-run is in the sibling `REPORT-b4-rerun.md`, whose "Bottom line for B4" finds
> scheme (b) moves the thresholds **modestly and in the expected direction**
> (balanced → narrower → lower; median Δ −7 inscriptions / −0.4 %), with **no
> reachability classification changed** and the committed full-precision v2
> thresholds (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`) remaining the
> primary. So the B4 sensitivity is **robust**, not material to the committed
> thresholds — read the "MATERIAL" verdict below as "flagged, then re-run and
> found non-material" (Obs 95). Do not cite the MATERIAL call as a standing
> threshold risk.

> **Key finding first:** the preregistered B4 (stratified *bootstrap* of LIRE) is
> **architecturally moot for the committed v2 Phase-1 thresholds** — Decision 8 replaced
> the LIRE bootstrap with synthetic data from a parametric null (`h1_sim_v2.py`). The only
> empirical lever on the thresholds is the **interval-width pool**; the per-iteration
> province/city counts are vestigial metadata with no effect on detection. This is a
> prereg-obligation-vs-implementation discrepancy worth recording in the obligations audit.

## What B4 means for v2, and the result

- **Scheme (a) proportional-allocation** preserves the width distribution exactly →
  **threshold-neutral by construction** (it removes resample variance, which the
  synthetic v2 design has none of). No computation needed.
- **Scheme (b) reweight-to-balance** (equalise province / city contributions; down-weights
  the over-represented Rome/Ostia and heavily-sampled provinces) changes the width mix —
  but only matters if interval widths differ across strata. The cheap check:

| width pool | mean (y) | p10 | p25 | p50 | p75 | p90 |
|---|---|---|---|---|---|---|
| global (v2 committed) | 105.67 | 24.0 | 49.0 | 99.0 | 149.0 | 199.0 |
| province-balanced (b) | 97.49 | 3.0 | 25.0 | 99.0 | 147.0 | 199.0 |
| city-balanced (b) | 87.95 | 3.0 | 27.0 | 79.0 | 99.0 | 199.0 |

Wasserstein-1 distance from the global pool: province-balanced **17.45 y**,
city-balanced **18.78 y** (tolerance = 10% of the global
median width = 9.9 y). Median-width shift:
province +0.0%, city -20.2%.

## Verdict — MATERIAL — a targeted threshold re-run under the balanced width pool is warranted

The balanced width distribution diverges materially from the global pool, so the thresholds could shift. A targeted re-run of the threshold-setting cells (province + urban-area N-sweeps, binding brackets) under the balanced width pool is warranted — flagged, not run here.

## Resolution for the obligations audit (item B4)

Record B4 as **superseded by Decision 8** (no LIRE bootstrap in the committed v2 design),
with this width-pool composition check as the v2-faithful substitute. Result: a width-pool re-run is the next step.

## Reproduce
```bash
uv run python runs/2026-06-16-s5-sensitivities/code/b4_stratified_widthpool.py
```
