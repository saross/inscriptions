# Option C non-parametric envelope --- validation summary

**Verdict: PASS**

Option C controls the false-positive rate at or near the nominal alpha = 0.05 across the validation grid. Mean FP rate is 0.033; max is 0.080; no cell exceeds 0.10; 2 cell(s) marginally exceed 0.05 but all remain within the Wilson 95% confidence interval of a true 0.05 rate at n_iter = 200 (roughly [0.025, 0.090]).

**Run parameters**

- 80-cell grid (3 levels x 2 shapes x reduced n-sweep x 4 brackets).
- 200 iterations per cell, 500 MC replicates per envelope test.
- Sampler: row-bootstrap from filtered LIRE + uniform aoristic;
  no parametric null fit. alpha = 0.05 two-tailed.
- Seed: 20260425; sapphire, 24 cores, joblib loky backend.

## 1. False-positive rates (zero bracket; target <= 0.05, pass <= 0.10)

| Level | Shape | n | n_iter | FP rate | flag |
|---|---|---|---|---|---|
| empire | gaussian | 50000 | 200 | 0.080 | warn (>0.05) |
| empire | step | 50000 | 200 | 0.055 | warn (>0.05) |
| province | gaussian | 100 | 200 | 0.015 | ok |
| province | gaussian | 500 | 200 | 0.030 | ok |
| province | gaussian | 2500 | 200 | 0.040 | ok |
| province | gaussian | 10000 | 200 | 0.045 | ok |
| province | gaussian | 25000 | 200 | 0.020 | ok |
| province | step | 100 | 200 | 0.035 | ok |
| province | step | 500 | 200 | 0.035 | ok |
| province | step | 2500 | 200 | 0.030 | ok |
| province | step | 10000 | 200 | 0.040 | ok |
| province | step | 25000 | 200 | 0.045 | ok |
| urban-area | gaussian | 25 | 200 | 0.015 | ok |
| urban-area | gaussian | 100 | 200 | 0.015 | ok |
| urban-area | gaussian | 500 | 200 | 0.030 | ok |
| urban-area | gaussian | 2500 | 200 | 0.045 | ok |
| urban-area | step | 25 | 200 | 0.020 | ok |
| urban-area | step | 100 | 200 | 0.010 | ok |
| urban-area | step | 500 | 200 | 0.015 | ok |
| urban-area | step | 2500 | 200 | 0.035 | ok |

FP-rate range: min 0.010, max 0.080, mean 0.033.

2 / 20 cells exceed 0.05; 0 / 20 cells exceed 0.10.

## 2. Detection rates (non-zero brackets; want >= 0.80 at threshold n)

| Level | Shape | n | Bracket | Detection rate | median p |
|---|---|---|---|---|---|
| empire | gaussian | 50000 | a_50pc_50y | 1.000 | 0.000 |
| empire | gaussian | 50000 | b_double_25y | 1.000 | 0.000 |
| empire | gaussian | 50000 | c_20pc_25y | 0.845 | 0.008 |
| empire | step | 50000 | a_50pc_50y | 1.000 | 0.000 |
| empire | step | 50000 | b_double_25y | 0.690 | 0.023 |
| empire | step | 50000 | c_20pc_25y | 0.705 | 0.022 |
| province | gaussian | 100 | a_50pc_50y | 0.015 | 0.686 |
| province | gaussian | 100 | b_double_25y | 0.450 | 0.064 |
| province | gaussian | 100 | c_20pc_25y | 0.010 | 0.665 |
| province | gaussian | 500 | a_50pc_50y | 0.425 | 0.078 |
| province | gaussian | 500 | b_double_25y | 0.585 | 0.030 |
| province | gaussian | 500 | c_20pc_25y | 0.150 | 0.397 |
| province | gaussian | 2500 | a_50pc_50y | 1.000 | 0.000 |
| province | gaussian | 2500 | b_double_25y | 0.895 | 0.004 |
| province | gaussian | 2500 | c_20pc_25y | 0.140 | 0.394 |
| province | gaussian | 10000 | a_50pc_50y | 1.000 | 0.000 |
| province | gaussian | 10000 | b_double_25y | 1.000 | 0.000 |
| province | gaussian | 10000 | c_20pc_25y | 0.330 | 0.147 |
| province | gaussian | 25000 | a_50pc_50y | 1.000 | 0.000 |
| province | gaussian | 25000 | b_double_25y | 1.000 | 0.000 |
| province | gaussian | 25000 | c_20pc_25y | 0.715 | 0.019 |
| province | step | 100 | a_50pc_50y | 0.015 | 0.679 |
| province | step | 100 | b_double_25y | 0.070 | 0.297 |
| province | step | 100 | c_20pc_25y | 0.015 | 0.670 |
| province | step | 500 | a_50pc_50y | 0.125 | 0.228 |
| province | step | 500 | b_double_25y | 0.350 | 0.084 |
| province | step | 500 | c_20pc_25y | 0.050 | 0.640 |
| province | step | 2500 | a_50pc_50y | 1.000 | 0.000 |
| province | step | 2500 | b_double_25y | 0.725 | 0.014 |
| province | step | 2500 | c_20pc_25y | 0.095 | 0.421 |
| province | step | 10000 | a_50pc_50y | 1.000 | 0.000 |
| province | step | 10000 | b_double_25y | 0.785 | 0.016 |
| province | step | 10000 | c_20pc_25y | 0.495 | 0.058 |
| province | step | 25000 | a_50pc_50y | 1.000 | 0.000 |
| province | step | 25000 | b_double_25y | 0.740 | 0.027 |
| province | step | 25000 | c_20pc_25y | 0.745 | 0.018 |
| urban-area | gaussian | 25 | a_50pc_50y | 0.020 | 1.000 |
| urban-area | gaussian | 25 | b_double_25y | 0.515 | 0.028 |
| urban-area | gaussian | 25 | c_20pc_25y | 0.040 | 1.000 |
| urban-area | gaussian | 100 | a_50pc_50y | 0.010 | 0.678 |
| urban-area | gaussian | 100 | b_double_25y | 0.400 | 0.066 |
| urban-area | gaussian | 100 | c_20pc_25y | 0.020 | 0.662 |
| urban-area | gaussian | 500 | a_50pc_50y | 0.390 | 0.080 |
| urban-area | gaussian | 500 | b_double_25y | 0.515 | 0.040 |
| urban-area | gaussian | 500 | c_20pc_25y | 0.135 | 0.370 |
| urban-area | gaussian | 2500 | a_50pc_50y | 0.995 | 0.000 |
| urban-area | gaussian | 2500 | b_double_25y | 0.920 | 0.004 |
| urban-area | gaussian | 2500 | c_20pc_25y | 0.130 | 0.405 |
| urban-area | step | 25 | a_50pc_50y | 0.010 | 1.000 |
| urban-area | step | 25 | b_double_25y | 0.040 | 0.528 |
| urban-area | step | 25 | c_20pc_25y | 0.015 | 0.546 |
| urban-area | step | 100 | a_50pc_50y | 0.010 | 0.681 |
| urban-area | step | 100 | b_double_25y | 0.085 | 0.286 |
| urban-area | step | 100 | c_20pc_25y | 0.015 | 0.676 |
| urban-area | step | 500 | a_50pc_50y | 0.155 | 0.376 |
| urban-area | step | 500 | b_double_25y | 0.385 | 0.083 |
| urban-area | step | 500 | c_20pc_25y | 0.045 | 0.653 |
| urban-area | step | 2500 | a_50pc_50y | 1.000 | 0.000 |
| urban-area | step | 2500 | b_double_25y | 0.715 | 0.020 |
| urban-area | step | 2500 | c_20pc_25y | 0.080 | 0.411 |

## 3. Side-by-side --- H1 v1 (broken) vs Option C (zero-bracket FP)

Each row: same (level, shape, n) cell. H1 v1 columns are the Poisson-on-fit MC envelope FP rates from REPORT.md §4 (exponential and CPL-k=3 nulls). Option C is the row-bootstrap MC FP rate from this validation. Lower is better; target <= 0.05.

| Level | Shape | n | H1 v1 exp FP | H1 v1 cpl-3 FP | Option C FP |
|---|---|---|---|---|---|
| empire | gaussian | 50000 | 1.000 | 1.000 | 0.080 |
| empire | step | 50000 | 1.000 | 1.000 | 0.055 |
| province | gaussian | 100 | 0.367 | 0.011 | 0.015 |
| province | gaussian | 500 | 0.948 | 0.039 | 0.030 |
| province | gaussian | 2500 | 1.000 | 0.452 | 0.040 |
| province | gaussian | 10000 | 1.000 | 1.000 | 0.045 |
| province | gaussian | 25000 | 1.000 | 1.000 | 0.020 |
| province | step | 100 | 0.331 | 0.014 | 0.035 |
| province | step | 500 | 0.935 | 0.045 | 0.035 |
| province | step | 2500 | 1.000 | 0.470 | 0.030 |
| province | step | 10000 | 1.000 | 0.999 | 0.040 |
| province | step | 25000 | 1.000 | 1.000 | 0.045 |
| urban-area | gaussian | 25 | 0.183 | 0.013 | 0.015 |
| urban-area | gaussian | 100 | 0.353 | 0.014 | 0.015 |
| urban-area | gaussian | 500 | 0.946 | 0.051 | 0.030 |
| urban-area | gaussian | 2500 | 1.000 | 0.465 | 0.045 |
| urban-area | step | 25 | 0.191 | 0.009 | 0.020 |
| urban-area | step | 100 | 0.368 | 0.008 | 0.010 |
| urban-area | step | 500 | 0.951 | 0.048 | 0.015 |
| urban-area | step | 2500 | 1.000 | 0.451 | 0.035 |

## 4. Discussion

Option C controls Type I error across the full validation grid, including the cells where the H1 v1 parametric envelope catastrophically failed (e.g. province / cpl-3 / step / n=2500: v1 0.470 -> Option C ~0.05-0.10). Detection power against the binding 50% / 50y bracket remains essentially saturated at the n-values where v1 reported 0.80-detection thresholds.

**Recommendation:** adopt Option C as the H1 v2 envelope method. Note that Option C tests a different null hypothesis from the preregistered protocol --- it asks 'is the observed SPA extreme relative to other re-bootstraps of the same source frame?' rather than 'is it extreme relative to a parametric growth model?' This is a softer null but the only one whose operational variance structure matches the observed pipeline. Document the pivot in a preregistration amendment.
