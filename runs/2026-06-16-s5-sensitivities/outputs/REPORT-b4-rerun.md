# §5 B4 scheme-(b) threshold re-run — DRAFT

> Quantifies whether the balanced width pools (scheme b) move the Phase-1 detection
> thresholds. Reduced precision (n_iter=200, n_mc=300); **the balanced-vs-global
> Δ is the deliverable** — absolute min_n here is not the committed full-precision value.
> 'n/r' = not reachable at the level's max N (Decision 10).

## Headline

- **City-balanced:** median Δmin_n **-7** inscriptions
  (median relative change **-0.4%**); 6 cells
  lower, 4 higher, of 12 comparable;
  reachability changed in 0 cells.
- **Province-balanced:** median Δmin_n **-12**
  (-1.1%); 7 lower / 4 higher.

Interpretation: a narrower balanced corpus (city-balancing cut median width 99y → 79y)
means less aoristic smearing, so detection thresholds fall (easier detection) —
the expected direction. The shift is modest and does not change the substantive reachability picture.

## Per-cell thresholds (min N for ≥80% detection)

| level | bracket | shape | null | global | prov-bal | city-bal | Δprov | Δcity |
|---|---|---|---|---|---|---|---|---|
| province | a_50pc_50y | gaussian | cpl | 1276 | 1436 | 1409 | 161 | 134 |
| province | a_50pc_50y | gaussian | exponential | 1911 | 1915 | 1890 | 4 | -21 |
| province | a_50pc_50y | step | cpl | 992 | 972 | 1105 | -20 | 113 |
| province | a_50pc_50y | step | exponential | 1982 | 1875 | 1968 | -107 | -14 |
| province | b_double_25y | gaussian | cpl | 2111 | 1981 | 1968 | -130 | -143 |
| province | b_double_25y | gaussian | exponential | 2430 | 2500 | 2309 | 70 | -122 |
| province | b_double_25y | step | cpl | n/r | n/r | n/r | n/r | n/r |
| province | b_double_25y | step | exponential | n/r | n/r | n/r | n/r | n/r |
| province | c_20pc_25y | gaussian | cpl | n/r | n/r | n/r | n/r | n/r |
| province | c_20pc_25y | gaussian | exponential | n/r | n/r | n/r | n/r | n/r |
| province | c_20pc_25y | step | cpl | n/r | n/r | n/r | n/r | n/r |
| province | c_20pc_25y | step | exponential | n/r | n/r | n/r | n/r | n/r |
| urban-area | a_50pc_50y | gaussian | cpl | 1604 | 1324 | 1464 | -281 | -141 |
| urban-area | a_50pc_50y | gaussian | exponential | 1988 | 2012 | 1958 | 23 | -30 |
| urban-area | a_50pc_50y | step | cpl | 1136 | 988 | 1136 | -149 | 0 |
| urban-area | a_50pc_50y | step | exponential | 1932 | 1929 | 1934 | -3 | 2 |
| urban-area | b_double_25y | gaussian | cpl | 1929 | 1865 | 2071 | -63 | 143 |
| urban-area | b_double_25y | gaussian | exponential | 25 | 25 | 25 | 0 | 0 |
| urban-area | b_double_25y | step | cpl | n/r | n/r | n/r | n/r | n/r |
| urban-area | b_double_25y | step | exponential | n/r | n/r | n/r | n/r | n/r |
| urban-area | c_20pc_25y | gaussian | cpl | n/r | n/r | n/r | n/r | n/r |
| urban-area | c_20pc_25y | gaussian | exponential | n/r | n/r | n/r | n/r | n/r |
| urban-area | c_20pc_25y | step | cpl | n/r | n/r | n/r | n/r | n/r |
| urban-area | c_20pc_25y | step | exponential | n/r | n/r | n/r | n/r | n/r |

## Bottom line for B4

Scheme (a) is threshold-neutral by construction; scheme (b) moves thresholds
modestly and in the
expected direction (balanced → narrower → lower thresholds).
The committed full-precision thresholds (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`)
remain the primary; this is the preregistered §5 stratification robustness check, with the
v2-supersession caveat recorded in the obligations audit.

## Reproduce
```bash
uv run python runs/2026-06-16-s5-sensitivities/code/b4_threshold_rerun.py
```
