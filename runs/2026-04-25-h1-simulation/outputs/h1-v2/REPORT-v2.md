# H1 v2 Simulation Report

**Driver:** ``h1_sim_v2.py`` (forward-fit nulls in true-date space; synthetic-from-null DGP)

**Total iteration records:** 51,200 rows across 256 cells

## 1. Headline thresholds (detection >= 0.80, primary CPL k=3)

| Level | Bracket | Null | Shape | min n (interp) | obs min n | unreachable |
|---|---|---|---|---|---|---|
| empire | a_50pc_50y | exponential | step | 50000 | 50000 | no |
| empire | a_50pc_50y | exponential | gaussian | 50000 | 50000 | no |
| empire | a_50pc_50y | cpl | step | 50000 | 50000 | no |
| empire | a_50pc_50y | cpl | gaussian | 50000 | 50000 | no |
| empire | b_double_25y | exponential | step | 50000 | 50000 | no |
| empire | b_double_25y | exponential | gaussian | 50000 | 50000 | no |
| empire | b_double_25y | cpl | step | n/a | n/a | **YES** |
| empire | b_double_25y | cpl | gaussian | 50000 | 50000 | no |
| empire | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| empire | c_20pc_25y | exponential | gaussian | 50000 | 50000 | no |
| empire | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| empire | c_20pc_25y | cpl | gaussian | 50000 | 50000 | no |
| province | a_50pc_50y | exponential | step | 1786 | 2500 | no |
| province | a_50pc_50y | exponential | gaussian | 1946 | 2500 | no |
| province | a_50pc_50y | cpl | step | 1000 | 1000 | no |
| province | a_50pc_50y | cpl | gaussian | 1136 | 2500 | no |
| province | b_double_25y | exponential | step | 10000 | 10000 | **YES** |
| province | b_double_25y | exponential | gaussian | 2018 | 2500 | no |
| province | b_double_25y | cpl | step | n/a | n/a | **YES** |
| province | b_double_25y | cpl | gaussian | 1545 | 2500 | no |
| province | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| province | c_20pc_25y | exponential | gaussian | n/a | n/a | **YES** |
| province | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| province | c_20pc_25y | cpl | gaussian | n/a | n/a | **YES** |
| urban-area | a_50pc_50y | exponential | step | 1833 | 2500 | no |
| urban-area | a_50pc_50y | exponential | gaussian | 1768 | 2500 | no |
| urban-area | a_50pc_50y | cpl | step | 949 | 1000 | no |
| urban-area | a_50pc_50y | cpl | gaussian | 981 | 1000 | no |
| urban-area | b_double_25y | exponential | step | n/a | n/a | **YES** |
| urban-area | b_double_25y | exponential | gaussian | 25 | 25 | no |
| urban-area | b_double_25y | cpl | step | n/a | n/a | **YES** |
| urban-area | b_double_25y | cpl | gaussian | 1786 | 2500 | no |
| urban-area | c_20pc_25y | exponential | step | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | exponential | gaussian | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | cpl | step | n/a | n/a | **YES** |
| urban-area | c_20pc_25y | cpl | gaussian | n/a | n/a | **YES** |

## 2. Unreachable-cell flag summary

Per Shawn's 2026-04-26 morning decision: cells where detection rate < 0.80 at the level's maximum n are tagged ``min_n_unreachable: True`` rather than extrapolated to a fictitious threshold. Tagged cells appear below.

| Level | Bracket | Null | k | Shape | rate at max n | max n |
|---|---|---|---|---|---|---|
| empire | b_double_25y | cpl | k=3 | step | 0.650 | 50000 |
| empire | b_double_25y | cpl | k=4 | step | 0.660 | 50000 |
| empire | c_20pc_25y | exponential | n/a | step | 0.720 | 50000 |
| empire | c_20pc_25y | cpl | k=3 | step | 0.720 | 50000 |
| empire | c_20pc_25y | cpl | k=4 | step | 0.740 | 50000 |
| province | b_double_25y | exponential | n/a | step | 0.670 | 25000 |
| province | b_double_25y | cpl | k=3 | step | 0.710 | 25000 |
| province | b_double_25y | cpl | k=4 | step | 0.740 | 25000 |
| province | c_20pc_25y | exponential | n/a | step | 0.760 | 25000 |
| province | c_20pc_25y | exponential | n/a | gaussian | 0.660 | 25000 |
| province | c_20pc_25y | cpl | k=3 | step | 0.680 | 25000 |
| province | c_20pc_25y | cpl | k=4 | step | 0.730 | 25000 |
| province | c_20pc_25y | cpl | k=3 | gaussian | 0.730 | 25000 |
| province | c_20pc_25y | cpl | k=4 | gaussian | 0.740 | 25000 |
| urban-area | b_double_25y | exponential | n/a | step | 0.720 | 2500 |
| urban-area | b_double_25y | cpl | k=3 | step | 0.760 | 2500 |
| urban-area | b_double_25y | cpl | k=4 | step | 0.780 | 2500 |
| urban-area | c_20pc_25y | exponential | n/a | step | 0.130 | 2500 |
| urban-area | c_20pc_25y | exponential | n/a | gaussian | 0.160 | 2500 |
| urban-area | c_20pc_25y | cpl | k=2 | step | 0.380 | 2500 |
| urban-area | c_20pc_25y | cpl | k=3 | step | 0.120 | 2500 |
| urban-area | c_20pc_25y | cpl | k=4 | step | 0.100 | 2500 |
| urban-area | c_20pc_25y | cpl | k=2 | gaussian | 0.350 | 2500 |
| urban-area | c_20pc_25y | cpl | k=3 | gaussian | 0.090 | 2500 |
| urban-area | c_20pc_25y | cpl | k=4 | gaussian | 0.110 | 2500 |

**25** of 72 (level x bracket x shape x null x k) detection cells are unreachable at the level's max n.

## 3. Zero-bracket FP rates (target <= 0.05)

| Level | Null | Shape | cpl_k | n | FP rate |
|---|---|---|---|---|---|
| empire | exponential | step | n/a | 50000 | 0.050 |
| empire | exponential | gaussian | n/a | 50000 | 0.060 |
| empire | cpl | step | 2 | 50000 | 1.000 |
| empire | cpl | step | 3 | 50000 | 0.050 |
| empire | cpl | step | 4 | 50000 | 0.040 |
| empire | cpl | gaussian | 2 | 50000 | 1.000 |
| empire | cpl | gaussian | 3 | 50000 | 0.020 |
| empire | cpl | gaussian | 4 | 50000 | 0.050 |
| province | exponential | step | n/a | 100 | 0.000 |
| province | exponential | step | n/a | 250 | 0.030 |
| province | exponential | step | n/a | 500 | 0.070 |
| province | exponential | step | n/a | 1000 | 0.030 |
| province | exponential | step | n/a | 2500 | 0.060 |
| province | exponential | step | n/a | 5000 | 0.050 |
| province | exponential | step | n/a | 10000 | 0.060 |
| province | exponential | step | n/a | 25000 | 0.070 |
| province | exponential | gaussian | n/a | 100 | 0.020 |
| province | exponential | gaussian | n/a | 250 | 0.050 |
| province | exponential | gaussian | n/a | 500 | 0.060 |
| province | exponential | gaussian | n/a | 1000 | 0.070 |
| province | exponential | gaussian | n/a | 2500 | 0.080 |
| province | exponential | gaussian | n/a | 5000 | 0.060 |
| province | exponential | gaussian | n/a | 10000 | 0.070 |
| province | exponential | gaussian | n/a | 25000 | 0.070 |
| province | cpl | step | 2 | 100 | 0.040 |
| province | cpl | step | 2 | 250 | 0.040 |
| province | cpl | step | 2 | 500 | 0.090 |
| province | cpl | step | 2 | 1000 | 0.070 |
| province | cpl | step | 2 | 2500 | 0.120 |
| province | cpl | step | 2 | 5000 | 0.350 |
| province | cpl | step | 2 | 10000 | 0.840 |
| province | cpl | step | 2 | 25000 | 1.000 |
| province | cpl | step | 3 | 100 | 0.030 |
| province | cpl | step | 3 | 250 | 0.030 |
| province | cpl | step | 3 | 500 | 0.050 |
| province | cpl | step | 3 | 1000 | 0.050 |
| province | cpl | step | 3 | 2500 | 0.040 |
| province | cpl | step | 3 | 5000 | 0.050 |
| province | cpl | step | 3 | 10000 | 0.060 |
| province | cpl | step | 3 | 25000 | 0.080 |
| province | cpl | step | 4 | 100 | 0.020 |
| province | cpl | step | 4 | 250 | 0.040 |
| province | cpl | step | 4 | 500 | 0.060 |
| province | cpl | step | 4 | 1000 | 0.040 |
| province | cpl | step | 4 | 2500 | 0.010 |
| province | cpl | step | 4 | 5000 | 0.050 |
| province | cpl | step | 4 | 10000 | 0.000 |
| province | cpl | step | 4 | 25000 | 0.080 |
| province | cpl | gaussian | 2 | 100 | 0.030 |
| province | cpl | gaussian | 2 | 250 | 0.050 |
| province | cpl | gaussian | 2 | 500 | 0.070 |
| province | cpl | gaussian | 2 | 1000 | 0.050 |
| province | cpl | gaussian | 2 | 2500 | 0.170 |
| province | cpl | gaussian | 2 | 5000 | 0.320 |
| province | cpl | gaussian | 2 | 10000 | 0.840 |
| province | cpl | gaussian | 2 | 25000 | 1.000 |
| province | cpl | gaussian | 3 | 100 | 0.050 |
| province | cpl | gaussian | 3 | 250 | 0.030 |
| province | cpl | gaussian | 3 | 500 | 0.030 |
| province | cpl | gaussian | 3 | 1000 | 0.020 |
| province | cpl | gaussian | 3 | 2500 | 0.040 |
| province | cpl | gaussian | 3 | 5000 | 0.020 |
| province | cpl | gaussian | 3 | 10000 | 0.060 |
| province | cpl | gaussian | 3 | 25000 | 0.050 |
| province | cpl | gaussian | 4 | 100 | 0.020 |
| province | cpl | gaussian | 4 | 250 | 0.080 |
| province | cpl | gaussian | 4 | 500 | 0.040 |
| province | cpl | gaussian | 4 | 1000 | 0.020 |
| province | cpl | gaussian | 4 | 2500 | 0.070 |
| province | cpl | gaussian | 4 | 5000 | 0.030 |
| province | cpl | gaussian | 4 | 10000 | 0.060 |
| province | cpl | gaussian | 4 | 25000 | 0.080 |
| urban-area | exponential | step | n/a | 25 | 0.000 |
| urban-area | exponential | step | n/a | 50 | 0.050 |
| urban-area | exponential | step | n/a | 100 | 0.010 |
| urban-area | exponential | step | n/a | 250 | 0.080 |
| urban-area | exponential | step | n/a | 500 | 0.040 |
| urban-area | exponential | step | n/a | 1000 | 0.060 |
| urban-area | exponential | step | n/a | 2500 | 0.040 |
| urban-area | exponential | gaussian | n/a | 25 | 0.030 |
| urban-area | exponential | gaussian | n/a | 50 | 0.040 |
| urban-area | exponential | gaussian | n/a | 100 | 0.060 |
| urban-area | exponential | gaussian | n/a | 250 | 0.040 |
| urban-area | exponential | gaussian | n/a | 500 | 0.030 |
| urban-area | exponential | gaussian | n/a | 1000 | 0.080 |
| urban-area | exponential | gaussian | n/a | 2500 | 0.040 |
| urban-area | cpl | step | 2 | 25 | 0.020 |
| urban-area | cpl | step | 2 | 50 | 0.050 |
| urban-area | cpl | step | 2 | 100 | 0.030 |
| urban-area | cpl | step | 2 | 250 | 0.040 |
| urban-area | cpl | step | 2 | 500 | 0.050 |
| urban-area | cpl | step | 2 | 1000 | 0.090 |
| urban-area | cpl | step | 2 | 2500 | 0.200 |
| urban-area | cpl | step | 3 | 25 | 0.050 |
| urban-area | cpl | step | 3 | 50 | 0.020 |
| urban-area | cpl | step | 3 | 100 | 0.050 |
| urban-area | cpl | step | 3 | 250 | 0.030 |
| urban-area | cpl | step | 3 | 500 | 0.020 |
| urban-area | cpl | step | 3 | 1000 | 0.020 |
| urban-area | cpl | step | 3 | 2500 | 0.050 |
| urban-area | cpl | step | 4 | 25 | 0.030 |
| urban-area | cpl | step | 4 | 50 | 0.010 |
| urban-area | cpl | step | 4 | 100 | 0.040 |
| urban-area | cpl | step | 4 | 250 | 0.090 |
| urban-area | cpl | step | 4 | 500 | 0.050 |
| urban-area | cpl | step | 4 | 1000 | 0.020 |
| urban-area | cpl | step | 4 | 2500 | 0.030 |
| urban-area | cpl | gaussian | 2 | 25 | 0.050 |
| urban-area | cpl | gaussian | 2 | 50 | 0.040 |
| urban-area | cpl | gaussian | 2 | 100 | 0.030 |
| urban-area | cpl | gaussian | 2 | 250 | 0.060 |
| urban-area | cpl | gaussian | 2 | 500 | 0.040 |
| urban-area | cpl | gaussian | 2 | 1000 | 0.100 |
| urban-area | cpl | gaussian | 2 | 2500 | 0.130 |
| urban-area | cpl | gaussian | 3 | 25 | 0.050 |
| urban-area | cpl | gaussian | 3 | 50 | 0.050 |
| urban-area | cpl | gaussian | 3 | 100 | 0.010 |
| urban-area | cpl | gaussian | 3 | 250 | 0.050 |
| urban-area | cpl | gaussian | 3 | 500 | 0.060 |
| urban-area | cpl | gaussian | 3 | 1000 | 0.080 |
| urban-area | cpl | gaussian | 3 | 2500 | 0.030 |
| urban-area | cpl | gaussian | 4 | 25 | 0.040 |
| urban-area | cpl | gaussian | 4 | 50 | 0.030 |
| urban-area | cpl | gaussian | 4 | 100 | 0.030 |
| urban-area | cpl | gaussian | 4 | 250 | 0.040 |
| urban-area | cpl | gaussian | 4 | 500 | 0.030 |
| urban-area | cpl | gaussian | 4 | 1000 | 0.070 |
| urban-area | cpl | gaussian | 4 | 2500 | 0.050 |

FP rate range: [0.000, 1.000]. Cells > 0.05: 46 / 128.

## 4. Exponential vs CPL-3 threshold comparison

| Level | Bracket | Shape | exp n | cpl-3 n | cpl/exp ratio |
|---|---|---|---|---|---|
| empire | a_50pc_50y | step | 50000 | 50000 | 1.00 |
| empire | a_50pc_50y | gaussian | 50000 | 50000 | 1.00 |
| empire | b_double_25y | gaussian | 50000 | 50000 | 1.00 |
| empire | c_20pc_25y | gaussian | 50000 | 50000 | 1.00 |
| province | a_50pc_50y | step | 1786 | 1000 | 0.56 |
| province | a_50pc_50y | gaussian | 1946 | 1136 | 0.58 |
| province | b_double_25y | gaussian | 2018 | 1545 | 0.77 |
| urban-area | a_50pc_50y | step | 1833 | 949 | 0.52 |
| urban-area | a_50pc_50y | gaussian | 1768 | 981 | 0.56 |
| urban-area | b_double_25y | gaussian | 25 | 1786 | 71.43 |

Median cpl/exp ratio: 0.88; range [0.52, 71.43].

## 5. CPL k-sensitivity (k in {2, 3, 4})

| Level/bracket/shape | k=2 | k=3 | k=4 | spread |
|---|---|---|---|---|
| empire/a_50pc_50y/step | 50000 | 50000 | 50000 | 0 |
| empire/a_50pc_50y/gaussian | 50000 | 50000 | 50000 | 0 |
| empire/b_double_25y/gaussian | 50000 | 50000 | 50000 | 0 |
| empire/c_20pc_25y/gaussian | 50000 | 50000 | 50000 | 0 |
| province/a_50pc_50y/step | 939 | 1000 | 977 | 61 |
| province/a_50pc_50y/gaussian | 940 | 1136 | 1404 | 464 |
| province/b_double_25y/gaussian | 1100 | 1545 | 1563 | 463 |
| urban-area/a_50pc_50y/step | 895 | 949 | 966 | 71 |
| urban-area/a_50pc_50y/gaussian | 885 | 981 | 1136 | 252 |
| urban-area/b_double_25y/gaussian | 1167 | 1786 | 1750 | 619 |

## 6. Execution diagnostics

- Total compute (serial-equivalent): 2006.6 min.
- Per-iteration wall_ms: median 1030, p95 9169.
- Convergence rate: 1.000 (51189 / 51200).
