# H2.1 Recovery Grid — Final Report

> **⚠ SUPERSEDED — THIS "FAIL" WAS OVERTURNED. DO NOT CITE THE FAIL VERDICT
> BELOW.** The "Validation verdict: FAIL" (63.6 % / 286 cells) in §1 was scored
> under a **zero-tolerance divergence convergence gate that was later found
> non-standard** (Stan/Betancourt; Obs 70). Re-scored under the corrected,
> field-standard criterion (Decision 33 / OSF Amendment 01 §A5.5.1: hybrid shape
> gate Pearson r ≥ 0.95 non-flat / Wasserstein-1 ≤ 10 y for the flat shape;
> α demoted to a quantified diagnostic; operating envelope α ≤ 0.70), **the grid
> PASSES** — **91.9 %** in the operating envelope on the first re-score, then
> **98.6 % (355/360)** once the harness re-derived convergence from the stored
> per-replicate R̂ / bulk-ESS (no re-fit). **See Obs 67** (the metric-artefact
> correction) and **Obs 70** (the gate artefact). The current, canonical
> recovery-grid result lives at
> `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md`
> (Grid A inscription-mass PASS; Grid B letter-mass FAIL on genuine R̂/ESS
> non-convergence). A cold reader must not take the FAIL below as the model's
> recovery verdict — it is a discredited, zero-tolerance-gate scoring of a
> grid that passes under the lodged criterion.

Bayesian deconvolution-mixture model validation via the H2.1 recovery simulation.
See `runs/2026-05-22-recovery-grid-design/spec.md` for the binding grid axes and decision rule.

## 1. Headline result

**Validation verdict:** FAIL (binding criteria require >= 90% of cells to pass coverage AND shape recovery)

| Criterion | Threshold | Result | Pass? |
|---|---|---|---|
| alpha-coverage >= 90% per cell | >= 90% of cells | 63.6% (286/450 cells) | FAIL |
| median Pearson r >= 0.95 per cell | >= 90% of cells | 69.8% (314/450 cells) | FAIL |
| Both criteria simultaneously | (informational) | 40.9% (184/450) | — |

## 2. Per-axis pass rates

### 2.alpha

| alpha | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 0.05 | 90 | 61% | 83% | 51% |
| 0.3 | 90 | 63% | 83% | 47% |
| 0.5 | 90 | 59% | 82% | 42% |
| 0.7 | 90 | 63% | 78% | 44% |
| 0.95 | 90 | 71% | 22% | 20% |

### 2.shape

| shape | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| bimodal | 75 | 35% | 72% | 29% |
| flat_baseline | 75 | 89% | 0% | 0% |
| regnal_cluster | 75 | 31% | 84% | 19% |
| rise_and_fall | 75 | 44% | 87% | 33% |
| smooth_decline | 75 | 93% | 88% | 83% |
| smooth_growth | 75 | 89% | 88% | 81% |

### 2.tier_weights

| tier_weights | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| century_heavy | 90 | 58% | 69% | 40% |
| half_century_heavy | 90 | 69% | 70% | 44% |
| pilot_proxy | 90 | 61% | 70% | 39% |
| reign_heavy | 90 | 64% | 71% | 40% |
| uniform | 90 | 66% | 69% | 41% |

### 2.N

| N | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 2000 | 150 | 67% | 63% | 43% |
| 10000 | 150 | 62% | 68% | 37% |
| 50000 | 150 | 61% | 79% | 43% |

## 3. Failed cells (either criterion)

| cell_id | alpha_cov | median Pearson r | median W-1 | convergence_pass | divergences |
|---|---|---|---|---|---|
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=50000` | 0.00 | 0.9789 | 8.55 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=50000` | 0.00 | 0.9802 | 8.45 | 0.97 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=10000` | 0.00 | 0.9815 | 7.78 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=50000` | 0.00 | 0.9871 | 6.93 | 0.98 | 3 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.9871 | 7.07 | 0.99 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.9895 | 6.98 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=2000` | 0.00 | 0.9918 | 8.85 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=2000` | 0.00 | 0.9921 | 9.40 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=2000` | 0.00 | 0.9921 | 9.99 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=2000` | 0.00 | 0.9922 | 10.06 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9923 | 5.45 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=2000` | 0.00 | 0.9928 | 9.82 | 0.98 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=50000` | 0.00 | 0.9933 | 5.13 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=50000` | 0.00 | 0.9942 | 3.87 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=50000` | 0.00 | 0.9951 | 4.40 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9961 | 2.97 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=10000` | 0.00 | 0.9967 | 9.82 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=10000` | 0.00 | 0.9979 | 9.64 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=10000` | 0.00 | 0.9979 | 9.43 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=10000` | 0.00 | 0.9979 | 9.70 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=10000` | 0.00 | 0.9979 | 9.37 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=10000` | 0.00 | 0.9980 | 9.65 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=50000` | 0.00 | 0.9984 | 10.21 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9985 | 9.89 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.9985 | 10.03 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=50000` | 0.00 | 0.9985 | 9.44 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.9986 | 9.93 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=50000` | 0.00 | 0.9989 | 9.80 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=50000` | 0.00 | 0.9989 | 9.64 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9989 | 9.61 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=50000` | 0.00 | 0.9989 | 9.77 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=50000` | 0.00 | 0.9989 | 9.92 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=50000` | 0.00 | 0.9990 | 9.61 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=50000` | 0.00 | 0.9990 | 9.70 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=50000` | 0.00 | 0.9991 | 9.74 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=50000` | 0.00 | 0.9991 | 9.73 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=50000` | 0.00 | 0.9991 | 9.69 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=10000` | 0.01 | 0.9752 | 8.65 | 0.98 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=50000` | 0.01 | 0.9835 | 8.01 | 0.97 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=50000` | 0.01 | 0.9864 | 6.54 | 0.96 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=10000` | 0.01 | 0.9869 | 5.29 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=10000` | 0.01 | 0.9898 | 4.56 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=10000` | 0.01 | 0.9969 | 9.97 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=10000` | 0.01 | 0.9969 | 9.65 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=10000` | 0.01 | 0.9970 | 9.41 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=10000` | 0.01 | 0.9971 | 9.96 | 0.99 | 0 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=50000` | 0.02 | 0.9943 | 3.83 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=50000` | 0.05 | 0.9971 | 9.96 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=50000` | 0.06 | 0.9972 | 9.81 | 0.97 | 0 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=10000` | 0.07 | 0.9557 | 10.91 | 0.68 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=50000` | 0.07 | 0.9971 | 9.89 | 0.97 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=50000` | 0.07 | 0.9971 | 10.54 | 0.97 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=10000` | 0.08 | 0.9605 | 10.36 | 0.55 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=10000` | 0.08 | 0.9665 | 9.59 | 0.86 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=10000` | 0.09 | 0.9949 | 10.07 | 0.98 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=10000` | 0.13 | 0.9852 | 5.73 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=2000` | 0.14 | 0.9487 | 9.80 | 0.80 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=half_century_heavy_N=50000` | 0.15 | 0.9972 | 9.42 | 0.99 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=50000` | 0.16 | 0.9986 | 7.80 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=10000` | 0.18 | 0.9952 | 10.28 | 0.97 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=10000` | 0.22 | 0.9908 | 3.26 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=50000` | 0.22 | 0.9976 | 10.04 | 0.99 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=10000` | 0.23 | 0.9724 | 7.53 | 0.96 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=50000` | 0.24 | 0.9976 | 10.22 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=2000` | 0.25 | 0.9886 | 10.47 | 0.98 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=50000` | 0.25 | 0.9956 | 13.23 | 0.98 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=50000` | 0.27 | 0.9956 | 13.60 | 0.96 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=50000` | 0.27 | 0.9986 | 8.00 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=50000` | 0.28 | 0.9977 | 9.50 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=10000` | 0.29 | 0.9738 | 7.24 | 0.96 | 0 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=2000` | 0.32 | 0.8739 | 13.79 | 0.01 | 116 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=50000` | 0.33 | 0.8498 | 14.93 | 0.00 | 481 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=50000` | 0.33 | 0.9985 | 6.76 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=2000` | 0.34 | 0.9880 | 10.13 | 0.94 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=10000` | 0.34 | 0.9950 | 9.73 | 0.96 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=2000` | 0.35 | 0.9608 | 8.34 | 0.84 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=10000` | 0.36 | 0.9948 | 9.86 | 0.98 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=50000` | 0.39 | 0.8187 | 15.36 | 0.00 | 949 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=2000` | 0.39 | 0.9008 | 13.47 | 0.03 | 620 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=10000` | 0.39 | 0.9935 | 13.92 | 0.89 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=50000` | 0.41 | 0.8450 | 15.18 | 0.00 | 949 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=10000` | 0.41 | 0.9936 | 13.90 | 0.94 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=10000` | 0.42 | 0.9848 | 4.24 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=10000` | 0.43 | 0.9959 | 10.13 | 0.98 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=50000` | 0.45 | 0.9958 | 12.53 | 0.99 | 0 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=10000` | 0.46 | 0.9856 | 4.22 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=50000` | 0.46 | 0.9956 | 2.10 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=10000` | 0.46 | 0.9958 | 9.89 | 0.99 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=50000` | 0.46 | 0.9978 | 7.94 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=2000` | 0.47 | 0.9886 | 10.73 | 0.96 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=50000` | 0.48 | 0.8246 | 14.90 | 0.00 | 1844 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=50000` | 0.48 | 0.9976 | 7.90 | 0.97 | 125 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=10000` | 0.49 | 0.9950 | 8.90 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=10000` | 0.51 | 0.9889 | 17.75 | 0.66 | 4 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=50000` | 0.54 | 0.9957 | 11.12 | 0.89 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=10000` | 0.55 | 0.9887 | 17.88 | 0.66 | 10 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=50000` | 0.56 | 0.9956 | 11.75 | 0.97 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=2000` | 0.57 | 0.9244 | 11.18 | 0.26 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=10000` | 0.57 | 0.9940 | 11.84 | 0.97 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=2000` | 0.61 | 0.9703 | 5.84 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=10000` | 0.63 | 0.4376 | 18.42 | 0.00 | 7279 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=50000` | 0.63 | 0.8643 | 14.58 | 0.00 | 3867 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=10000` | 0.64 | 0.4720 | 18.36 | 0.00 | 629 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=2000` | 0.64 | 0.9879 | 10.09 | 0.95 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=reign_heavy_N=2000` | 0.66 | 0.9918 | 8.97 | 0.71 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=10000` | 0.70 | 0.4989 | 18.38 | 0.00 | 5667 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=10000` | 0.70 | 0.9894 | 16.36 | 0.54 | 4 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=10000` | 0.71 | 0.3994 | 18.53 | 0.00 | 4456 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=2000` | 0.71 | 0.9631 | 6.79 | 0.95 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=half_century_heavy_N=50000` | 0.71 | 0.9985 | 4.37 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=2000` | 0.72 | 0.1003 | 19.01 | 0.00 | 4769 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=2000` | 0.72 | 0.1813 | 18.87 | 0.00 | 2602 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=2000` | 0.73 | 0.9745 | 5.06 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=10000` | 0.73 | 0.9894 | 10.60 | 0.83 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=reign_heavy_N=10000` | 0.73 | 0.9964 | 1.57 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=2000` | 0.73 | nan | 1.59 | 0.00 | 1238 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=2000` | 0.74 | 0.9759 | 24.46 | 0.03 | 172 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=2000` | 0.75 | 0.9731 | 22.86 | 0.02 | 99 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=2000` | 0.76 | 0.9851 | 16.72 | 0.61 | 1 |
| `shape=smooth_growth_alpha=0.05_tier=half_century_heavy_N=2000` | 0.76 | 0.9919 | 8.93 | 0.70 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=2000` | 0.77 | 0.9845 | 18.22 | 0.58 | 2 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=10000` | 0.78 | 0.9897 | 14.19 | 0.75 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=reign_heavy_N=50000` | 0.78 | 0.9985 | 4.20 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=reign_heavy_N=2000` | 0.79 | 0.9892 | 2.57 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=10000` | 0.79 | 0.9957 | 6.85 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=2000` | 0.79 | nan | 1.24 | 0.00 | 1248 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=50000` | 0.80 | 0.9672 | 24.89 | 0.00 | 1705 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=2000` | 0.81 | 0.7556 | 57.42 | 0.00 | 5314 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=2000` | 0.82 | 0.9881 | 8.36 | 0.95 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=uniform_N=2000` | 0.82 | 0.9921 | 7.35 | 0.83 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=uniform_N=2000` | 0.82 | 0.9929 | 7.26 | 0.85 | 0 |
| `shape=bimodal_alpha=0.30_tier=reign_heavy_N=50000` | 0.82 | 0.9966 | 1.84 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=2000` | 0.82 | nan | 1.00 | 0.00 | 2140 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=2000` | 0.83 | 0.0867 | 19.16 | 0.00 | 3314 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=2000` | 0.83 | 0.9807 | 10.95 | 0.96 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=reign_heavy_N=2000` | 0.83 | 0.9929 | 7.77 | 0.84 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=reign_heavy_N=10000` | 0.83 | 0.9968 | 4.47 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=10000` | 0.83 | nan | 0.43 | 0.00 | 22 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=10000` | 0.84 | 0.5529 | 18.31 | 0.00 | 4220 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=50000` | 0.84 | 0.9657 | 26.64 | 0.00 | 1052 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=2000` | 0.85 | 0.6490 | 49.13 | 0.00 | 4264 |
| `shape=rise_and_fall_alpha=0.05_tier=half_century_heavy_N=2000` | 0.85 | 0.9900 | 2.57 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=pilot_proxy_N=2000` | 0.85 | 0.9913 | 8.83 | 0.69 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=10000` | 0.85 | 0.9935 | 8.38 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=reign_heavy_N=10000` | 0.85 | 0.9972 | 3.79 | 0.99 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=reign_heavy_N=50000` | 0.85 | 0.9990 | 0.76 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=2000` | 0.85 | nan | 1.05 | 0.00 | 121 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=2000` | 0.86 | 0.2948 | 37.37 | 0.00 | 4448 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=10000` | 0.86 | 0.8005 | 20.05 | 0.00 | 2991 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=2000` | 0.86 | 0.8315 | 49.74 | 0.00 | 6195 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=2000` | 0.86 | 0.8401 | 47.80 | 0.00 | 3839 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=2000` | 0.86 | 0.9728 | 19.84 | 0.03 | 4 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=10000` | 0.86 | 0.9889 | 13.33 | 0.82 | 9 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=10000` | 0.86 | 0.9891 | 10.40 | 0.83 | 1 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=2000` | 0.86 | nan | 7.26 | 0.00 | 694 |
| `shape=rise_and_fall_alpha=0.05_tier=half_century_heavy_N=10000` | 0.87 | 0.9965 | 1.24 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=2000` | 0.87 | nan | 1.12 | 0.00 | 119 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=10000` | 0.88 | 0.9020 | 37.52 | 0.00 | 7228 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=10000` | 0.88 | 0.9426 | 33.20 | 0.00 | 2317 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=2000` | 0.88 | nan | 6.98 | 0.00 | 5057 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000` | 0.89 | 0.7982 | 17.51 | 0.00 | 4954 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=2000` | 0.89 | 0.9808 | 10.69 | 0.87 | 65 |
| `shape=smooth_decline_alpha=0.05_tier=half_century_heavy_N=2000` | 0.89 | 0.9925 | 6.45 | 0.81 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=10000` | 0.89 | 0.9937 | 8.00 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=2000` | 0.90 | 0.3659 | 35.83 | 0.00 | 4404 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=2000` | 0.90 | 0.4416 | 34.22 | 0.00 | 2451 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=2000` | 0.90 | 0.6935 | 48.04 | 0.00 | 1460 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=2000` | 0.90 | 0.7275 | 49.36 | 0.00 | 2979 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=10000` | 0.90 | 0.9163 | 36.39 | 0.00 | 6014 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=10000` | 0.90 | nan | 0.78 | 0.00 | 264 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.91 | 0.7405 | 52.76 | 0.00 | 2405 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=10000` | 0.91 | 0.7416 | 27.06 | 0.00 | 7933 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=2000` | 0.91 | 0.8527 | 45.18 | 0.00 | 1910 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=10000` | 0.91 | nan | 0.93 | 0.00 | 418 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=10000` | 0.91 | nan | 1.39 | 0.00 | 2571 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=2000` | 0.92 | 0.7445 | 51.00 | 0.00 | 960 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=10000` | 0.92 | 0.7884 | 21.29 | 0.00 | 7857 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=2000` | 0.92 | 0.8654 | 43.86 | 0.00 | 298 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=2000` | 0.92 | 0.9353 | 9.11 | 0.44 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=2000` | 0.92 | nan | 1.73 | 0.00 | 3158 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=2000` | 0.93 | 0.2875 | 18.78 | 0.00 | 740 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=2000` | 0.93 | 0.3506 | 36.67 | 0.00 | 1457 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=2000` | 0.93 | 0.7970 | 46.74 | 0.00 | 1478 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=2000` | 0.93 | 0.9311 | 9.43 | 0.28 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.93 | nan | 6.49 | 0.00 | 7914 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=2000` | 0.94 | 0.3359 | 18.81 | 0.00 | 701 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=2000` | 0.94 | 0.7907 | 49.53 | 0.00 | 763 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=10000` | 0.94 | 0.8972 | 37.20 | 0.00 | 6213 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=10000` | 0.94 | 0.9208 | 36.87 | 0.00 | 3088 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=10000` | 0.94 | 0.9228 | 33.40 | 0.00 | 7895 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000` | 0.94 | 0.9390 | 38.88 | 0.00 | 3628 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=10000` | 0.94 | nan | 0.57 | 0.00 | 1909 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=2000` | 0.94 | nan | 1.31 | 0.00 | 918 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=50000` | 0.94 | nan | 0.41 | 0.00 | 17 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=2000` | 0.94 | nan | 1.71 | 0.00 | 3129 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=2000` | 0.95 | 0.6524 | 48.74 | 0.00 | 130 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=10000` | 0.95 | 0.9158 | 33.33 | 0.00 | 2147 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=10000` | 0.95 | nan | 0.47 | 0.00 | 376 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=10000` | 0.95 | nan | 0.74 | 0.00 | 234 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=2000` | 0.95 | nan | 2.69 | 0.00 | 1646 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=10000` | 0.95 | nan | 1.57 | 0.00 | 2607 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=10000` | 0.95 | nan | 6.39 | 0.00 | 4531 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=50000` | 0.95 | nan | 4.26 | 0.00 | 6349 |
| `shape=smooth_growth_alpha=0.95_tier=reign_heavy_N=2000` | 0.96 | 0.8756 | 43.80 | 0.00 | 200 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=10000` | 0.96 | 0.9355 | 32.68 | 0.00 | 2300 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=10000` | 0.96 | 0.9441 | 38.63 | 0.00 | 3478 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=10000` | 0.96 | nan | 0.50 | 0.00 | 2038 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=50000` | 0.96 | nan | 0.17 | 0.00 | 787 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=10000` | 0.96 | nan | 0.41 | 0.00 | 1000 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=2000` | 0.96 | nan | 2.24 | 0.00 | 4497 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=2000` | 0.96 | nan | 1.88 | 0.00 | 1148 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=50000` | 0.96 | nan | 0.32 | 0.00 | 194 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=50000` | 0.96 | nan | 0.31 | 0.00 | 40 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=50000` | 0.96 | nan | 0.49 | 0.00 | 1901 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=10000` | 0.96 | nan | 1.14 | 0.00 | 2973 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=2000` | 0.96 | nan | 2.74 | 0.00 | 5341 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=50000` | 0.96 | nan | 0.43 | 0.00 | 549 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=50000` | 0.96 | nan | 0.54 | 0.00 | 2001 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=10000` | 0.96 | nan | 5.10 | 0.00 | 1232 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.97 | 0.9439 | 37.65 | 0.00 | 2181 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=10000` | 0.97 | 0.9480 | 29.82 | 0.00 | 3518 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=10000` | 0.97 | nan | 0.36 | 0.00 | 39 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=10000` | 0.97 | nan | 0.35 | 0.00 | 230 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=50000` | 0.97 | nan | 0.28 | 0.00 | 200 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=50000` | 0.97 | nan | 0.22 | 0.00 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=10000` | 0.97 | nan | 0.60 | 0.00 | 1 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=50000` | 0.97 | nan | 0.33 | 0.00 | 142 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=50000` | 0.97 | nan | 0.33 | 0.00 | 18 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=50000` | 0.97 | nan | 0.33 | 0.00 | 626 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=2000` | 0.97 | nan | 2.26 | 0.00 | 733 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=50000` | 0.97 | nan | 0.68 | 0.00 | 55 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.97 | nan | 5.69 | 0.00 | 2230 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=2000` | 0.98 | 0.2807 | 37.18 | 0.00 | 2086 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=10000` | 0.98 | 0.7389 | 26.56 | 0.00 | 1130 |
| `shape=smooth_decline_alpha=0.95_tier=reign_heavy_N=2000` | 0.98 | 0.8366 | 50.53 | 0.00 | 467 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=10000` | 0.98 | 0.9307 | 37.84 | 0.00 | 4036 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=50000` | 0.98 | 0.9483 | 11.62 | 0.03 | 713 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=50000` | 0.98 | nan | 0.21 | 0.00 | 102 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=50000` | 0.98 | nan | 0.18 | 0.00 | 18 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=2000` | 0.98 | nan | 1.34 | 0.00 | 1659 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=50000` | 0.98 | nan | 0.25 | 0.00 | 2099 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=50000` | 0.98 | nan | 0.30 | 0.00 | 145 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=10000` | 0.98 | nan | 0.48 | 0.00 | 1 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=10000` | 0.98 | nan | 0.87 | 0.00 | 115 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=2000` | 0.98 | nan | 2.08 | 0.00 | 1553 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=50000` | 0.98 | nan | 0.48 | 0.00 | 102 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=2000` | 0.98 | nan | 4.14 | 0.00 | 276 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=2000` | 0.98 | nan | 3.07 | 0.00 | 2485 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=50000` | 0.98 | nan | 4.33 | 0.00 | 6997 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=10000` | 0.98 | nan | 6.54 | 0.00 | 5644 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=50000` | 0.98 | nan | 3.57 | 0.00 | 5450 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=10000` | 0.98 | nan | 5.36 | 0.00 | 4376 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=50000` | 0.99 | 0.9483 | 12.31 | 0.09 | 998 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=50000` | 0.99 | nan | 0.16 | 0.00 | 7 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=50000` | 0.99 | nan | 0.19 | 0.00 | 245 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=10000` | 0.99 | nan | 0.78 | 0.00 | 686 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=2000` | 0.99 | nan | 4.22 | 0.00 | 2518 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=10000` | 0.99 | nan | 1.86 | 0.00 | 2394 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=2000` | 0.99 | nan | 6.09 | 0.00 | 2346 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=50000` | 0.99 | nan | 3.86 | 0.00 | 6862 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=2000` | 0.99 | nan | 6.51 | 0.00 | 373 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=50000` | 0.99 | nan | 3.64 | 0.00 | 6478 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=10000` | 1.00 | nan | 0.40 | 0.00 | 44 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=2000` | 1.00 | nan | 1.60 | 0.00 | 1544 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=2000` | 1.00 | nan | 1.63 | 0.00 | 824 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=10000` | 1.00 | nan | 1.39 | 0.00 | 310 |

## 4. Diagnostics

- Mean fit-seconds per replicate: 37.17
- Min cell-level convergence pass rate: 0.00%
- Cells with any divergences: 202/450

## 5. Wasserstein-1 supplementary

Wasserstein-1 is reported per cell as a distribution-sensitive shape metric (prereg §4 line 334). The flagging threshold is deferred to a follow-up artefact (see design spec §6).

- Median across cells: 7.20
- 90th percentile across cells: 21.87