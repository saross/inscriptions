# H1 v2 Simulation Report

**Driver:** ``h1_sim_v2.py`` (forward-fit nulls in true-date space; synthetic-from-null DGP)

**Total iteration records:** 384,000 rows across 256 cells

## 1. Headline thresholds (detection >= 0.80, primary CPL k=3)

| Level | Bracket | Null | Shape | min n (interp) | obs min n | unreachable |
|---|---|---|---|---|---|---|
| empire | a_50pc_50y | exponential | step | 50000 | 50000 | no |
| empire | a_50pc_50y | exponential | gaussian | 50000 | 50000 | no |
| empire | a_50pc_50y | cpl | step | 50000 | 50000 | no |
| empire | a_50pc_50y | cpl | gaussian | 50000 | 50000 | no |
| empire | b_double_25y | exponential | step | n/a | n/a | **YES** |
| empire | b_double_25y | exponential | gaussian | 50000 | 50000 | no |
| empire | b_double_25y | cpl | step | n/a | n/a | **YES** |
| empire | b_double_25y | cpl | gaussian | 50000 | 50000 | no |
| empire | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| empire | c_20pc_25y | exponential | gaussian | n/a | n/a | **YES** |
| empire | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| empire | c_20pc_25y | cpl | gaussian | 50000 | 50000 | no |
| province | a_50pc_50y | exponential | step | 1938 | 2500 | no |
| province | a_50pc_50y | exponential | gaussian | 1869 | 2500 | no |
| province | a_50pc_50y | cpl | step | 1385 | 2500 | no |
| province | a_50pc_50y | cpl | gaussian | 1618 | 2500 | no |
| province | b_double_25y | exponential | step | n/a | n/a | **YES** |
| province | b_double_25y | exponential | gaussian | 2118 | 2500 | no |
| province | b_double_25y | cpl | step | n/a | n/a | **YES** |
| province | b_double_25y | cpl | gaussian | 1934 | 2500 | no |
| province | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| province | c_20pc_25y | exponential | gaussian | n/a | n/a | **YES** |
| province | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| province | c_20pc_25y | cpl | gaussian | n/a | n/a | **YES** |
| urban-area | a_50pc_50y | exponential | step | 1923 | 2500 | no |
| urban-area | a_50pc_50y | exponential | gaussian | 1854 | 2500 | no |
| urban-area | a_50pc_50y | cpl | step | 1409 | 2500 | no |
| urban-area | a_50pc_50y | cpl | gaussian | 1549 | 2500 | no |
| urban-area | b_double_25y | exponential | step | n/a | n/a | **YES** |
| urban-area | b_double_25y | exponential | gaussian | 2160 | 2500 | no |
| urban-area | b_double_25y | cpl | step | n/a | n/a | **YES** |
| urban-area | b_double_25y | cpl | gaussian | 1905 | 2500 | no |
| urban-area | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | exponential | gaussian | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | cpl | gaussian | n/a | n/a | **YES** |

## 2. Unreachable-cell flag summary

Per Shawn's 2026-04-26 morning decision: cells where detection rate < 0.80 at the level's maximum n are tagged ``min_n_unreachable: True`` rather than extrapolated to a fictitious threshold. Tagged cells appear below.

| Level | Bracket | Null | k | Shape | rate at max n | max n |
|---|---|---|---|---|---|---|
| empire | b_double_25y | exponential | n/a | step | 0.729 | 50000 |
| empire | b_double_25y | cpl | k=3 | step | 0.695 | 50000 |
| empire | b_double_25y | cpl | k=4 | step | 0.683 | 50000 |
| empire | c_20pc_25y | exponential | n/a | step | 0.714 | 50000 |
| empire | c_20pc_25y | exponential | n/a | gaussian | 0.792 | 50000 |
| empire | c_20pc_25y | cpl | k=3 | step | 0.686 | 50000 |
| empire | c_20pc_25y | cpl | k=4 | step | 0.678 | 50000 |
| province | b_double_25y | exponential | n/a | step | 0.684 | 25000 |
| province | b_double_25y | cpl | k=3 | step | 0.658 | 25000 |
| province | b_double_25y | cpl | k=4 | step | 0.646 | 25000 |
| province | c_20pc_25y | exponential | n/a | step | 0.667 | 25000 |
| province | c_20pc_25y | exponential | n/a | gaussian | 0.569 | 25000 |
| province | c_20pc_25y | cpl | k=3 | step | 0.640 | 25000 |
| province | c_20pc_25y | cpl | k=4 | step | 0.650 | 25000 |
| province | c_20pc_25y | cpl | k=3 | gaussian | 0.645 | 25000 |
| province | c_20pc_25y | cpl | k=4 | gaussian | 0.641 | 25000 |
| urban-area | b_double_25y | exponential | n/a | step | 0.726 | 2500 |
| urban-area | b_double_25y | cpl | k=3 | step | 0.748 | 2500 |
| urban-area | b_double_25y | cpl | k=4 | step | 0.755 | 2500 |
| urban-area | c_20pc_25y | exponential | n/a | step | 0.075 | 2500 |
| urban-area | c_20pc_25y | exponential | n/a | gaussian | 0.113 | 2500 |
| urban-area | c_20pc_25y | cpl | k=3 | step | 0.097 | 2500 |
| urban-area | c_20pc_25y | cpl | k=4 | step | 0.093 | 2500 |
| urban-area | c_20pc_25y | cpl | k=3 | gaussian | 0.086 | 2500 |
| urban-area | c_20pc_25y | cpl | k=4 | gaussian | 0.087 | 2500 |

**25** of 54 (level x bracket x shape x null x k) detection cells are unreachable at the level's max n.

## 3. Zero-bracket FP rates (target <= 0.05)

| Level | Null | Shape | cpl_k | n | FP rate |
|---|---|---|---|---|---|
| empire | exponential | step | n/a | 50000 | 0.044 |
| empire | exponential | gaussian | n/a | 50000 | 0.049 |
| empire | cpl | step | 3 | 50000 | 0.032 |
| empire | cpl | step | 4 | 50000 | 0.037 |
| empire | cpl | gaussian | 3 | 50000 | 0.023 |
| empire | cpl | gaussian | 4 | 50000 | 0.025 |
| province | exponential | step | n/a | 100 | 0.010 |
| province | exponential | step | n/a | 250 | 0.015 |
| province | exponential | step | n/a | 500 | 0.036 |
| province | exponential | step | n/a | 1000 | 0.037 |
| province | exponential | step | n/a | 2500 | 0.029 |
| province | exponential | step | n/a | 5000 | 0.041 |
| province | exponential | step | n/a | 10000 | 0.034 |
| province | exponential | step | n/a | 25000 | 0.035 |
| province | exponential | gaussian | n/a | 100 | 0.009 |
| province | exponential | gaussian | n/a | 250 | 0.008 |
| province | exponential | gaussian | n/a | 500 | 0.026 |
| province | exponential | gaussian | n/a | 1000 | 0.029 |
| province | exponential | gaussian | n/a | 2500 | 0.032 |
| province | exponential | gaussian | n/a | 5000 | 0.026 |
| province | exponential | gaussian | n/a | 10000 | 0.026 |
| province | exponential | gaussian | n/a | 25000 | 0.025 |
| province | cpl | step | 3 | 100 | 0.013 |
| province | cpl | step | 3 | 250 | 0.022 |
| province | cpl | step | 3 | 500 | 0.020 |
| province | cpl | step | 3 | 1000 | 0.021 |
| province | cpl | step | 3 | 2500 | 0.027 |
| province | cpl | step | 3 | 5000 | 0.027 |
| province | cpl | step | 3 | 10000 | 0.022 |
| province | cpl | step | 3 | 25000 | 0.036 |
| province | cpl | step | 4 | 100 | 0.011 |
| province | cpl | step | 4 | 250 | 0.023 |
| province | cpl | step | 4 | 500 | 0.014 |
| province | cpl | step | 4 | 1000 | 0.023 |
| province | cpl | step | 4 | 2500 | 0.024 |
| province | cpl | step | 4 | 5000 | 0.016 |
| province | cpl | step | 4 | 10000 | 0.021 |
| province | cpl | step | 4 | 25000 | 0.030 |
| province | cpl | gaussian | 3 | 100 | 0.016 |
| province | cpl | gaussian | 3 | 250 | 0.020 |
| province | cpl | gaussian | 3 | 500 | 0.019 |
| province | cpl | gaussian | 3 | 1000 | 0.017 |
| province | cpl | gaussian | 3 | 2500 | 0.024 |
| province | cpl | gaussian | 3 | 5000 | 0.022 |
| province | cpl | gaussian | 3 | 10000 | 0.021 |
| province | cpl | gaussian | 3 | 25000 | 0.018 |
| province | cpl | gaussian | 4 | 100 | 0.017 |
| province | cpl | gaussian | 4 | 250 | 0.030 |
| province | cpl | gaussian | 4 | 500 | 0.010 |
| province | cpl | gaussian | 4 | 1000 | 0.022 |
| province | cpl | gaussian | 4 | 2500 | 0.022 |
| province | cpl | gaussian | 4 | 5000 | 0.015 |
| province | cpl | gaussian | 4 | 10000 | 0.019 |
| province | cpl | gaussian | 4 | 25000 | 0.022 |
| urban-area | exponential | step | n/a | 25 | 0.017 |
| urban-area | exponential | step | n/a | 50 | 0.039 |
| urban-area | exponential | step | n/a | 100 | 0.012 |
| urban-area | exponential | step | n/a | 250 | 0.025 |
| urban-area | exponential | step | n/a | 500 | 0.026 |
| urban-area | exponential | step | n/a | 1000 | 0.037 |
| urban-area | exponential | step | n/a | 2500 | 0.036 |
| urban-area | exponential | gaussian | n/a | 25 | 0.031 |
| urban-area | exponential | gaussian | n/a | 50 | 0.020 |
| urban-area | exponential | gaussian | n/a | 100 | 0.015 |
| urban-area | exponential | gaussian | n/a | 250 | 0.021 |
| urban-area | exponential | gaussian | n/a | 500 | 0.022 |
| urban-area | exponential | gaussian | n/a | 1000 | 0.038 |
| urban-area | exponential | gaussian | n/a | 2500 | 0.046 |
| urban-area | cpl | step | 3 | 25 | 0.018 |
| urban-area | cpl | step | 3 | 50 | 0.023 |
| urban-area | cpl | step | 3 | 100 | 0.017 |
| urban-area | cpl | step | 3 | 250 | 0.026 |
| urban-area | cpl | step | 3 | 500 | 0.022 |
| urban-area | cpl | step | 3 | 1000 | 0.020 |
| urban-area | cpl | step | 3 | 2500 | 0.038 |
| urban-area | cpl | step | 4 | 25 | 0.015 |
| urban-area | cpl | step | 4 | 50 | 0.015 |
| urban-area | cpl | step | 4 | 100 | 0.014 |
| urban-area | cpl | step | 4 | 250 | 0.026 |
| urban-area | cpl | step | 4 | 500 | 0.018 |
| urban-area | cpl | step | 4 | 1000 | 0.024 |
| urban-area | cpl | step | 4 | 2500 | 0.032 |
| urban-area | cpl | gaussian | 3 | 25 | 0.019 |
| urban-area | cpl | gaussian | 3 | 50 | 0.024 |
| urban-area | cpl | gaussian | 3 | 100 | 0.007 |
| urban-area | cpl | gaussian | 3 | 250 | 0.022 |
| urban-area | cpl | gaussian | 3 | 500 | 0.020 |
| urban-area | cpl | gaussian | 3 | 1000 | 0.021 |
| urban-area | cpl | gaussian | 3 | 2500 | 0.036 |
| urban-area | cpl | gaussian | 4 | 25 | 0.027 |
| urban-area | cpl | gaussian | 4 | 50 | 0.023 |
| urban-area | cpl | gaussian | 4 | 100 | 0.015 |
| urban-area | cpl | gaussian | 4 | 250 | 0.026 |
| urban-area | cpl | gaussian | 4 | 500 | 0.022 |
| urban-area | cpl | gaussian | 4 | 1000 | 0.026 |
| urban-area | cpl | gaussian | 4 | 2500 | 0.033 |

FP rate range: [0.007, 0.049]. Cells > 0.05: 0 / 96.

## 4. Exponential vs CPL-3 threshold comparison

| Level | Bracket | Shape | exp n | cpl-3 n | cpl/exp ratio |
|---|---|---|---|---|---|
| empire | a_50pc_50y | step | 50000 | 50000 | 1.00 |
| empire | a_50pc_50y | gaussian | 50000 | 50000 | 1.00 |
| empire | b_double_25y | gaussian | 50000 | 50000 | 1.00 |
| province | a_50pc_50y | step | 1938 | 1385 | 0.71 |
| province | a_50pc_50y | gaussian | 1869 | 1618 | 0.87 |
| province | b_double_25y | gaussian | 2118 | 1934 | 0.91 |
| urban-area | a_50pc_50y | step | 1923 | 1409 | 0.73 |
| urban-area | a_50pc_50y | gaussian | 1854 | 1549 | 0.84 |
| urban-area | b_double_25y | gaussian | 2160 | 1905 | 0.88 |

Median cpl/exp ratio: 0.88; range [0.71, 1.00].

## 5. CPL k-sensitivity (k in {3, 4} per Decision 9)

| Level/bracket/shape | k=3 | k=4 | spread |
|---|---|---|---|
| empire/a_50pc_50y/step | 50000 | 50000 | 0 |
| empire/a_50pc_50y/gaussian | 50000 | 50000 | 0 |
| empire/b_double_25y/gaussian | 50000 | 50000 | 0 |
| empire/c_20pc_25y/gaussian | 50000 | 50000 | 0 |
| province/a_50pc_50y/step | 1385 | 1432 | 48 |
| province/a_50pc_50y/gaussian | 1618 | 1665 | 47 |
| province/b_double_25y/gaussian | 1934 | 1965 | 31 |
| urban-area/a_50pc_50y/step | 1409 | 1510 | 101 |
| urban-area/a_50pc_50y/gaussian | 1549 | 1603 | 54 |
| urban-area/b_double_25y/gaussian | 1905 | 1916 | 11 |

**AIC-best k distribution** (across all CPL iterations):

| k | proportion |
|---|---|
| 3 | 0.727 |
| 4 | 0.273 |

## 6. Execution diagnostics

- Total compute (serial-equivalent): 8555.4 min.
- Per-iteration wall_ms: median 449, p95 7459.
- Convergence rate: 1.000 (383870 / 384000).
