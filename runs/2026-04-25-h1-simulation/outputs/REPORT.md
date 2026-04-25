# H1 Simulation Report

**Run:** 2026-04-25 (commit 982fec9)

**Total iteration records:** 512,000 rows across 256 cells

**Schema (Decision 8 of decisions.md):** exponential cells emit 1 row/iter; CPL cells emit 3 rows/iter (one per k in {2, 3, 4}).

## 1. Headline recommended thresholds (detection >= 0.80)

Primary CPL k = 3. NaN min_n means the largest n in the sweep does not reach the target detection rate; check power curves for that cell.

| Level | Bracket | Null | Shape | min n (interp) | obs min n |
|---|---|---|---|---|---|
| empire | a_50pc_50y | exponential | step | 50000 | 50000 |
| empire | a_50pc_50y | exponential | gaussian | 50000 | 50000 |
| empire | a_50pc_50y | cpl | step | 50000 | 50000 |
| empire | a_50pc_50y | cpl | gaussian | 50000 | 50000 |
| empire | b_double_25y | exponential | step | 50000 | 50000 |
| empire | b_double_25y | exponential | gaussian | 50000 | 50000 |
| empire | b_double_25y | cpl | step | 50000 | 50000 |
| empire | b_double_25y | cpl | gaussian | 50000 | 50000 |
| empire | c_20pc_25y | exponential | step | 50000 | 50000 |
| empire | c_20pc_25y | exponential | gaussian | 50000 | 50000 |
| empire | c_20pc_25y | cpl | step | 50000 | 50000 |
| empire | c_20pc_25y | cpl | gaussian | 50000 | 50000 |
| province | a_50pc_50y | exponential | step | 423 | 500 |
| province | a_50pc_50y | exponential | gaussian | 393 | 500 |
| province | a_50pc_50y | cpl | step | 915 | 1000 |
| province | a_50pc_50y | cpl | gaussian | 882 | 1000 |
| province | b_double_25y | exponential | step | 115 | 250 |
| province | b_double_25y | exponential | gaussian | 100 | 100 |
| province | b_double_25y | cpl | step | 1695 | 2500 |
| province | b_double_25y | cpl | gaussian | 1356 | 2500 |
| province | c_20pc_25y | exponential | step | 343 | 500 |
| province | c_20pc_25y | exponential | gaussian | 321 | 500 |
| province | c_20pc_25y | cpl | step | 3697 | 5000 |
| province | c_20pc_25y | cpl | gaussian | 3299 | 5000 |
| urban-area | a_50pc_50y | exponential | step | 426 | 500 |
| urban-area | a_50pc_50y | exponential | gaussian | 394 | 500 |
| urban-area | a_50pc_50y | cpl | step | 919 | 1000 |
| urban-area | a_50pc_50y | cpl | gaussian | 905 | 1000 |
| urban-area | b_double_25y | exponential | step | 123 | 250 |
| urban-area | b_double_25y | exponential | gaussian | 25 | 25 |
| urban-area | b_double_25y | cpl | step | 1705 | 2500 |
| urban-area | b_double_25y | cpl | gaussian | 1254 | 2500 |
| urban-area | c_20pc_25y | exponential | step | 353 | 500 |
| urban-area | c_20pc_25y | exponential | gaussian | 335 | 500 |
| urban-area | c_20pc_25y | cpl | step | n/a | n/a |
| urban-area | c_20pc_25y | cpl | gaussian | n/a | n/a |

### Range per (level x bracket x null) — [step, gaussian] thresholds

| Level | Bracket | Null | n_sharp (step) | n_smooth (gaussian) |
|---|---|---|---|---|
| empire | a_50pc_50y | exponential | 50000 | 50000 |
| empire | a_50pc_50y | cpl | 50000 | 50000 |
| empire | b_double_25y | exponential | 50000 | 50000 |
| empire | b_double_25y | cpl | 50000 | 50000 |
| empire | c_20pc_25y | exponential | 50000 | 50000 |
| empire | c_20pc_25y | cpl | 50000 | 50000 |
| province | a_50pc_50y | exponential | 423 | 393 |
| province | a_50pc_50y | cpl | 915 | 882 |
| province | b_double_25y | exponential | 115 | 100 |
| province | b_double_25y | cpl | 1695 | 1356 |
| province | c_20pc_25y | exponential | 343 | 321 |
| province | c_20pc_25y | cpl | 3697 | 3299 |
| urban-area | a_50pc_50y | exponential | 426 | 394 |
| urban-area | a_50pc_50y | cpl | 919 | 905 |
| urban-area | b_double_25y | exponential | 123 | 25 |
| urban-area | b_double_25y | cpl | 1705 | 1254 |
| urban-area | c_20pc_25y | exponential | 353 | 335 |
| urban-area | c_20pc_25y | cpl | n/a | n/a |

## 2. Power curves

Per (level x bracket x shape x null x cpl_k), with 0.70 / 0.80 / 0.90 detection-rate gridlines and Wilson 95% CI ribbons.

Files in `power-curves/` (one PNG + one parquet per slice):

- `power-curves/empire_a_50pc_50y_gaussian_cpl_k2.png`
- `power-curves/empire_a_50pc_50y_gaussian_cpl_k3.png`
- `power-curves/empire_a_50pc_50y_gaussian_cpl_k4.png`
- `power-curves/empire_a_50pc_50y_gaussian_exponential.png`
- `power-curves/empire_a_50pc_50y_step_cpl_k2.png`
- `power-curves/empire_a_50pc_50y_step_cpl_k3.png`
- `power-curves/empire_a_50pc_50y_step_cpl_k4.png`
- `power-curves/empire_a_50pc_50y_step_exponential.png`
- `power-curves/empire_b_double_25y_gaussian_cpl_k2.png`
- `power-curves/empire_b_double_25y_gaussian_cpl_k3.png`
- `power-curves/empire_b_double_25y_gaussian_cpl_k4.png`
- `power-curves/empire_b_double_25y_gaussian_exponential.png`
- `power-curves/empire_b_double_25y_step_cpl_k2.png`
- `power-curves/empire_b_double_25y_step_cpl_k3.png`
- `power-curves/empire_b_double_25y_step_cpl_k4.png`
- `power-curves/empire_b_double_25y_step_exponential.png`
- `power-curves/empire_c_20pc_25y_gaussian_cpl_k2.png`
- `power-curves/empire_c_20pc_25y_gaussian_cpl_k3.png`
- `power-curves/empire_c_20pc_25y_gaussian_cpl_k4.png`
- `power-curves/empire_c_20pc_25y_gaussian_exponential.png`
- ... and 76 more

## 3. Effect-size x n heatmaps

Per (level x null x shape x cpl_k), with 0.80 contour highlighted.

Files in `heatmaps/`:

- `heatmaps/empire_cpl_gaussian_k2.png`
- `heatmaps/empire_cpl_gaussian_k3.png`
- `heatmaps/empire_cpl_gaussian_k4.png`
- `heatmaps/empire_cpl_step_k2.png`
- `heatmaps/empire_cpl_step_k3.png`
- `heatmaps/empire_cpl_step_k4.png`
- `heatmaps/empire_exponential_gaussian.png`
- `heatmaps/empire_exponential_step.png`
- `heatmaps/province_cpl_gaussian_k2.png`
- `heatmaps/province_cpl_gaussian_k3.png`
- `heatmaps/province_cpl_gaussian_k4.png`
- `heatmaps/province_cpl_step_k2.png`
- `heatmaps/province_cpl_step_k3.png`
- `heatmaps/province_cpl_step_k4.png`
- `heatmaps/province_exponential_gaussian.png`
- `heatmaps/province_exponential_step.png`
- `heatmaps/urban-area_cpl_gaussian_k2.png`
- `heatmaps/urban-area_cpl_gaussian_k3.png`
- `heatmaps/urban-area_cpl_gaussian_k4.png`
- `heatmaps/urban-area_cpl_step_k2.png`
- `heatmaps/urban-area_cpl_step_k3.png`
- `heatmaps/urban-area_cpl_step_k4.png`
- `heatmaps/urban-area_exponential_gaussian.png`
- `heatmaps/urban-area_exponential_step.png`

## 4. Zero-effect false-positive rates (target ≤ 0.05)

| Level | Null | Shape | cpl_k | n | FP rate |
|---|---|---|---|---|---|
| empire | exponential | step | n/a | 50000 | 1.000 |
| empire | exponential | gaussian | n/a | 50000 | 1.000 |
| empire | cpl | step | 2 | 50000 | 1.000 |
| empire | cpl | step | 3 | 50000 | 1.000 |
| empire | cpl | step | 4 | 50000 | 1.000 |
| empire | cpl | gaussian | 2 | 50000 | 1.000 |
| empire | cpl | gaussian | 3 | 50000 | 1.000 |
| empire | cpl | gaussian | 4 | 50000 | 1.000 |
| province | exponential | step | n/a | 100 | 0.331 |
| province | exponential | step | n/a | 250 | 0.757 |
| province | exponential | step | n/a | 500 | 0.935 |
| province | exponential | step | n/a | 1000 | 1.000 |
| province | exponential | step | n/a | 2500 | 1.000 |
| province | exponential | step | n/a | 5000 | 1.000 |
| province | exponential | step | n/a | 10000 | 1.000 |
| province | exponential | step | n/a | 25000 | 1.000 |
| province | exponential | gaussian | n/a | 100 | 0.367 |
| province | exponential | gaussian | n/a | 250 | 0.778 |
| province | exponential | gaussian | n/a | 500 | 0.948 |
| province | exponential | gaussian | n/a | 1000 | 1.000 |
| province | exponential | gaussian | n/a | 2500 | 1.000 |
| province | exponential | gaussian | n/a | 5000 | 1.000 |
| province | exponential | gaussian | n/a | 10000 | 1.000 |
| province | exponential | gaussian | n/a | 25000 | 1.000 |
| province | cpl | step | 2 | 100 | 0.018 |
| province | cpl | step | 2 | 250 | 0.049 |
| province | cpl | step | 2 | 500 | 0.097 |
| province | cpl | step | 2 | 1000 | 0.347 |
| province | cpl | step | 2 | 2500 | 0.954 |
| province | cpl | step | 2 | 5000 | 1.000 |
| province | cpl | step | 2 | 10000 | 1.000 |
| province | cpl | step | 2 | 25000 | 1.000 |
| province | cpl | step | 3 | 100 | 0.014 |
| province | cpl | step | 3 | 250 | 0.036 |
| province | cpl | step | 3 | 500 | 0.045 |
| province | cpl | step | 3 | 1000 | 0.105 |
| province | cpl | step | 3 | 2500 | 0.470 |
| province | cpl | step | 3 | 5000 | 0.841 |
| province | cpl | step | 3 | 10000 | 0.999 |
| province | cpl | step | 3 | 25000 | 1.000 |
| province | cpl | step | 4 | 100 | 0.007 |
| province | cpl | step | 4 | 250 | 0.021 |
| province | cpl | step | 4 | 500 | 0.041 |
| province | cpl | step | 4 | 1000 | 0.085 |
| province | cpl | step | 4 | 2500 | 0.372 |
| province | cpl | step | 4 | 5000 | 0.777 |
| province | cpl | step | 4 | 10000 | 0.993 |
| province | cpl | step | 4 | 25000 | 1.000 |
| province | cpl | gaussian | 2 | 100 | 0.018 |
| province | cpl | gaussian | 2 | 250 | 0.052 |
| province | cpl | gaussian | 2 | 500 | 0.102 |
| province | cpl | gaussian | 2 | 1000 | 0.346 |
| province | cpl | gaussian | 2 | 2500 | 0.952 |
| province | cpl | gaussian | 2 | 5000 | 1.000 |
| province | cpl | gaussian | 2 | 10000 | 1.000 |
| province | cpl | gaussian | 2 | 25000 | 1.000 |
| province | cpl | gaussian | 3 | 100 | 0.011 |
| province | cpl | gaussian | 3 | 250 | 0.036 |
| province | cpl | gaussian | 3 | 500 | 0.039 |
| province | cpl | gaussian | 3 | 1000 | 0.120 |
| province | cpl | gaussian | 3 | 2500 | 0.452 |
| province | cpl | gaussian | 3 | 5000 | 0.881 |
| province | cpl | gaussian | 3 | 10000 | 1.000 |
| province | cpl | gaussian | 3 | 25000 | 1.000 |
| province | cpl | gaussian | 4 | 100 | 0.019 |
| province | cpl | gaussian | 4 | 250 | 0.023 |
| province | cpl | gaussian | 4 | 500 | 0.025 |
| province | cpl | gaussian | 4 | 1000 | 0.083 |
| province | cpl | gaussian | 4 | 2500 | 0.336 |
| province | cpl | gaussian | 4 | 5000 | 0.804 |
| province | cpl | gaussian | 4 | 10000 | 0.988 |
| province | cpl | gaussian | 4 | 25000 | 1.000 |
| urban-area | exponential | step | n/a | 25 | 0.191 |
| urban-area | exponential | step | n/a | 50 | 0.224 |
| urban-area | exponential | step | n/a | 100 | 0.368 |
| urban-area | exponential | step | n/a | 250 | 0.771 |
| urban-area | exponential | step | n/a | 500 | 0.951 |
| urban-area | exponential | step | n/a | 1000 | 1.000 |
| urban-area | exponential | step | n/a | 2500 | 1.000 |
| urban-area | exponential | gaussian | n/a | 25 | 0.183 |
| urban-area | exponential | gaussian | n/a | 50 | 0.191 |
| urban-area | exponential | gaussian | n/a | 100 | 0.353 |
| urban-area | exponential | gaussian | n/a | 250 | 0.752 |
| urban-area | exponential | gaussian | n/a | 500 | 0.946 |
| urban-area | exponential | gaussian | n/a | 1000 | 1.000 |
| urban-area | exponential | gaussian | n/a | 2500 | 1.000 |
| urban-area | cpl | step | 2 | 25 | 0.011 |
| urban-area | cpl | step | 2 | 50 | 0.015 |
| urban-area | cpl | step | 2 | 100 | 0.016 |
| urban-area | cpl | step | 2 | 250 | 0.054 |
| urban-area | cpl | step | 2 | 500 | 0.082 |
| urban-area | cpl | step | 2 | 1000 | 0.347 |
| urban-area | cpl | step | 2 | 2500 | 0.956 |
| urban-area | cpl | step | 3 | 25 | 0.009 |
| urban-area | cpl | step | 3 | 50 | 0.009 |
| urban-area | cpl | step | 3 | 100 | 0.008 |
| urban-area | cpl | step | 3 | 250 | 0.032 |
| urban-area | cpl | step | 3 | 500 | 0.048 |
| urban-area | cpl | step | 3 | 1000 | 0.093 |
| urban-area | cpl | step | 3 | 2500 | 0.451 |
| urban-area | cpl | step | 4 | 25 | 0.007 |
| urban-area | cpl | step | 4 | 50 | 0.016 |
| urban-area | cpl | step | 4 | 100 | 0.008 |
| urban-area | cpl | step | 4 | 250 | 0.032 |
| urban-area | cpl | step | 4 | 500 | 0.023 |
| urban-area | cpl | step | 4 | 1000 | 0.080 |
| urban-area | cpl | step | 4 | 2500 | 0.362 |
| urban-area | cpl | gaussian | 2 | 25 | 0.016 |
| urban-area | cpl | gaussian | 2 | 50 | 0.014 |
| urban-area | cpl | gaussian | 2 | 100 | 0.012 |
| urban-area | cpl | gaussian | 2 | 250 | 0.068 |
| urban-area | cpl | gaussian | 2 | 500 | 0.105 |
| urban-area | cpl | gaussian | 2 | 1000 | 0.330 |
| urban-area | cpl | gaussian | 2 | 2500 | 0.948 |
| urban-area | cpl | gaussian | 3 | 25 | 0.013 |
| urban-area | cpl | gaussian | 3 | 50 | 0.015 |
| urban-area | cpl | gaussian | 3 | 100 | 0.014 |
| urban-area | cpl | gaussian | 3 | 250 | 0.048 |
| urban-area | cpl | gaussian | 3 | 500 | 0.051 |
| urban-area | cpl | gaussian | 3 | 1000 | 0.109 |
| urban-area | cpl | gaussian | 3 | 2500 | 0.465 |
| urban-area | cpl | gaussian | 4 | 25 | 0.014 |
| urban-area | cpl | gaussian | 4 | 50 | 0.010 |
| urban-area | cpl | gaussian | 4 | 100 | 0.010 |
| urban-area | cpl | gaussian | 4 | 250 | 0.028 |
| urban-area | cpl | gaussian | 4 | 500 | 0.036 |
| urban-area | cpl | gaussian | 4 | 1000 | 0.074 |
| urban-area | cpl | gaussian | 4 | 2500 | 0.368 |

FP rate range across all zero-bracket cells: [0.007, 1.000].

**88 cells exceed 0.05 FP rate** — see table for specifics.

## 5. Exponential vs CPL-3 comparison

| Level | Bracket | Shape | exp n | cpl-3 n | cpl/exp ratio |
|---|---|---|---|---|---|
| empire | a_50pc_50y | step | 50000 | 50000 | 1.00 |
| empire | a_50pc_50y | gaussian | 50000 | 50000 | 1.00 |
| empire | b_double_25y | step | 50000 | 50000 | 1.00 |
| empire | b_double_25y | gaussian | 50000 | 50000 | 1.00 |
| empire | c_20pc_25y | step | 50000 | 50000 | 1.00 |
| empire | c_20pc_25y | gaussian | 50000 | 50000 | 1.00 |
| province | a_50pc_50y | step | 423 | 915 | 2.16 |
| province | a_50pc_50y | gaussian | 393 | 882 | 2.24 |
| province | b_double_25y | step | 115 | 1695 | 14.69 |
| province | b_double_25y | gaussian | 100 | 1356 | 13.56 |
| province | c_20pc_25y | step | 343 | 3697 | 10.78 |
| province | c_20pc_25y | gaussian | 321 | 3299 | 10.27 |
| urban-area | a_50pc_50y | step | 426 | 919 | 2.16 |
| urban-area | a_50pc_50y | gaussian | 394 | 905 | 2.30 |
| urban-area | b_double_25y | step | 123 | 1705 | 13.87 |
| urban-area | b_double_25y | gaussian | 25 | 1254 | 50.17 |

Median ratio (cpl/exp): 2.20; range [1.00, 50.17].

## 6. Exploratory — CPL k-sensitivity (k in {2, 3, 4})

Threshold variation across k values, holding (level, bracket, shape) fixed.

| Level/bracket/shape | k=2 | k=3 | k=4 | spread |
|---|---|---|---|---|
| empire/a_50pc_50y/step | 50000 | 50000 | 50000 | 0 |
| empire/a_50pc_50y/gaussian | 50000 | 50000 | 50000 | 0 |
| empire/b_double_25y/step | 50000 | 50000 | 50000 | 0 |
| empire/b_double_25y/gaussian | 50000 | 50000 | 50000 | 0 |
| empire/c_20pc_25y/step | 50000 | 50000 | 50000 | 0 |
| empire/c_20pc_25y/gaussian | 50000 | 50000 | 50000 | 0 |
| province/a_50pc_50y/step | 1234 | 915 | 941 | 319 |
| province/a_50pc_50y/gaussian | 916 | 882 | 981 | 100 |
| province/b_double_25y/step | 851 | 1695 | 1726 | 876 |
| province/b_double_25y/gaussian | 577 | 1356 | 1447 | 869 |
| province/c_20pc_25y/step | 2092 | 3697 | 3944 | 1852 |
| province/c_20pc_25y/gaussian | 1996 | 3299 | 3912 | 1916 |
| urban-area/a_50pc_50y/step | 1207 | 919 | 945 | 288 |
| urban-area/a_50pc_50y/gaussian | 947 | 905 | 974 | 69 |
| urban-area/b_double_25y/step | 859 | 1705 | 1744 | 885 |
| urban-area/b_double_25y/gaussian | 604 | 1254 | 1387 | 782 |

## 7. Exploratory — AIC-select reconstruction

Per-iteration AIC-best k from `cpl_aic` column. Threshold under the AIC-select rule:

| Level | Bracket | Shape | min n (AIC-select) |
|---|---|---|---|
| empire | a_50pc_50y | gaussian | 50000 |
| empire | a_50pc_50y | step | 50000 |
| empire | b_double_25y | gaussian | 50000 |
| empire | b_double_25y | step | 50000 |
| empire | c_20pc_25y | gaussian | 50000 |
| empire | c_20pc_25y | step | 50000 |
| province | a_50pc_50y | gaussian | 954 |
| province | a_50pc_50y | step | 930 |
| province | b_double_25y | gaussian | 1437 |
| province | b_double_25y | step | 1748 |
| province | c_20pc_25y | gaussian | 3785 |
| province | c_20pc_25y | step | 3966 |
| urban-area | a_50pc_50y | gaussian | 956 |
| urban-area | a_50pc_50y | step | 940 |
| urban-area | b_double_25y | gaussian | 1369 |
| urban-area | b_double_25y | step | 1777 |
| urban-area | c_20pc_25y | gaussian | n/a |
| urban-area | c_20pc_25y | step | n/a |

## 8. Stratified-sampling exploratory

Per Decision 4 (decisions.md) the stratified-by-province / stratified-by-urban-area sensitivity is reconstructable post-hoc from the persisted parquet (using the `province_counts` and `city_counts` dict columns). Not run in this REPORT; deferred to follow-up analysis.

## 9. Execution notes

- Total per-iteration rows: 512,000
- Cells: 256
- Hardware: sapphire (24 cores, 60 GB RAM)
- Total compute: 2063.5 min serial-equivalent; per-iteration mean 242 ms
- CPL fallback fraction <= 20 % in all cells (good).
- CPL fallback fraction range: [0.000, 0.077]; mean 0.013.

## 10. Open questions for Shawn's morning review

1. **Null-model preregistration choice.** The exp-vs-CPL comparison (§5) shows whether thresholds shift materially. If they disagree (cpl/exp ratio > ~1.5), Shawn must pick one for the prereg fix.
2. **Urban-area operability at 50 % / 50 y bracket.** Several urban-area cells likely fail to reach 0.80 detection at any tested n (n_max = 2,500). Suggests urban-area H3 confirmatory scope may be tighter than empire/province.
4. **FP-rate exceeds target in some cells** — check zero-bracket table (§4) for which (level, null, shape) combinations need investigation.
5. **k-sensitivity (§6).** If spread across k in {2, 3, 4} is narrow, k = 3 is robust; if wide, document choice rationale.
