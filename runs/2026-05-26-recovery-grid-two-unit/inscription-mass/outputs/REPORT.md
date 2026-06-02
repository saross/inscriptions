# Recovery Grid — inscription-mass — Per-Grid Report

Bayesian deconvolution-mixture model validation via the two-unit recovery simulation.
See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the binding decision rule, and the 2026-05-22 predecessor run for the shared cell design.

## 1. Headline result

**Unit of analysis:** inscription-mass (each synthetic inscription deposits unit count).

**Validation verdict:** FAIL (binding criteria require >= 90% of cells to pass coverage AND shape recovery)

| Criterion | Threshold | Result | Pass? |
|---|---|---|---|
| alpha-coverage >= 90% per cell | >= 90% of cells | 69.8% (314/450) | FAIL |
| median Pearson r >= 0.95 per cell | >= 90% of cells | 70.2% (316/450) | FAIL |
| Both criteria simultaneously | (informational) | 42.7% (192/450) | — |

## 2. Per-axis pass rates

### 2.alpha

| alpha | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 0.05 | 90 | 82% | 83% | 66% |
| 0.3 | 90 | 57% | 83% | 40% |
| 0.5 | 90 | 57% | 83% | 40% |
| 0.7 | 90 | 61% | 78% | 44% |
| 0.95 | 90 | 92% | 23% | 23% |

### 2.shape

| shape | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| bimodal | 75 | 37% | 73% | 25% |
| flat_baseline | 75 | 99% | 0% | 0% |
| regnal_cluster | 75 | 32% | 85% | 17% |
| rise_and_fall | 75 | 53% | 87% | 40% |
| smooth_decline | 75 | 97% | 88% | 85% |
| smooth_growth | 75 | 100% | 88% | 88% |

### 2.tier_weights

| tier_weights | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| century_heavy | 90 | 62% | 70% | 37% |
| half_century_heavy | 90 | 77% | 70% | 48% |
| pilot_proxy | 90 | 64% | 70% | 38% |
| reign_heavy | 90 | 74% | 71% | 48% |
| uniform | 90 | 71% | 70% | 43% |

### 2.N

| N | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 2000 | 150 | 79% | 63% | 45% |
| 10000 | 150 | 68% | 68% | 38% |
| 50000 | 150 | 62% | 79% | 45% |

## 3. Failed cells (either criterion)

| cell_id | alpha_cov | median Pearson r | median W-1 | convergence_pass | divergences |
|---|---|---|---|---|---|
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=50000` | 0.00 | 0.9792 | 8.28 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=50000` | 0.00 | 0.9832 | 7.90 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.9865 | 7.84 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=50000` | 0.00 | 0.9876 | 6.87 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=10000` | 0.00 | 0.9877 | 5.69 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.9896 | 7.23 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=10000` | 0.00 | 0.9903 | 4.82 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=2000` | 0.00 | 0.9917 | 9.79 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9923 | 5.63 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=50000` | 0.00 | 0.9937 | 5.45 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=50000` | 0.00 | 0.9943 | 3.88 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=50000` | 0.00 | 0.9956 | 4.60 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9961 | 3.06 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=10000` | 0.00 | 0.9967 | 9.86 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=10000` | 0.00 | 0.9969 | 9.85 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=10000` | 0.00 | 0.9970 | 10.25 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=10000` | 0.00 | 0.9977 | 9.17 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=10000` | 0.00 | 0.9977 | 9.60 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=10000` | 0.00 | 0.9979 | 9.51 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=10000` | 0.00 | 0.9979 | 9.43 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=10000` | 0.00 | 0.9980 | 9.39 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=50000` | 0.00 | 0.9985 | 9.84 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=50000` | 0.00 | 0.9986 | 9.51 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9986 | 9.73 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.9986 | 10.08 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.9986 | 9.97 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=50000` | 0.00 | 0.9989 | 10.02 | 0.97 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9989 | 9.88 | 0.95 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=50000` | 0.00 | 0.9989 | 9.76 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=50000` | 0.00 | 0.9989 | 9.82 | 0.96 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=50000` | 0.00 | 0.9989 | 9.69 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=50000` | 0.00 | 0.9990 | 9.64 | 0.93 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=50000` | 0.00 | 0.9991 | 9.80 | 0.92 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=50000` | 0.00 | 0.9991 | 9.56 | 0.94 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=50000` | 0.00 | 0.9991 | 9.64 | 0.92 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=50000` | 0.00 | 0.9991 | 9.76 | 0.95 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=10000` | 0.01 | 0.9746 | 9.27 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=50000` | 0.01 | 0.9811 | 8.29 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=50000` | 0.01 | 0.9874 | 6.67 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=2000` | 0.01 | 0.9918 | 9.30 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=50000` | 0.01 | 0.9938 | 3.90 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=10000` | 0.01 | 0.9969 | 10.12 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=2000` | 0.02 | 0.9917 | 9.23 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=10000` | 0.03 | 0.9808 | 8.07 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=10000` | 0.03 | 0.9844 | 5.97 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=2000` | 0.03 | 0.9925 | 9.53 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=2000` | 0.04 | 0.9922 | 9.49 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=50000` | 0.04 | 0.9970 | 9.99 | 0.98 | 1 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=50000` | 0.04 | 0.9973 | 10.25 | 0.90 | 10 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=10000` | 0.07 | 0.9969 | 9.15 | 0.98 | 2 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=50000` | 0.07 | 0.9973 | 9.61 | 0.96 | 2 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=50000` | 0.09 | 0.9974 | 10.24 | 0.95 | 2 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=50000` | 0.10 | 0.9985 | 9.04 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=10000` | 0.11 | 0.9556 | 10.74 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=half_century_heavy_N=50000` | 0.11 | 0.9973 | 9.61 | 0.97 | 3 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=10000` | 0.12 | 0.9505 | 10.84 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=50000` | 0.13 | 0.9985 | 8.66 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=2000` | 0.14 | 0.9509 | 10.20 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=10000` | 0.16 | 0.9664 | 9.28 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=10000` | 0.16 | 0.9947 | 9.85 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=50000` | 0.19 | 0.9975 | 10.55 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=2000` | 0.20 | 0.9614 | 9.10 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=10000` | 0.20 | 0.9907 | 3.41 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=50000` | 0.20 | 0.9977 | 10.29 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=2000` | 0.21 | 0.9731 | 6.39 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=10000` | 0.22 | 0.9741 | 7.35 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=10000` | 0.22 | 0.9948 | 10.28 | 0.99 | 1 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=2000` | 0.24 | 0.8597 | 14.38 | 0.99 | 1 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=10000` | 0.24 | 0.9959 | 11.95 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=10000` | 0.25 | 0.9949 | 9.51 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=10000` | 0.25 | 0.9960 | 11.18 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=50000` | 0.28 | 0.9962 | 2.11 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=50000` | 0.30 | 0.9985 | 6.76 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=10000` | 0.31 | 0.9952 | 9.56 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=10000` | 0.32 | 0.9952 | 8.99 | 0.99 | 1 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=10000` | 0.35 | 0.9866 | 4.17 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=50000` | 0.36 | 0.9956 | 12.81 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=50000` | 0.36 | 0.9958 | 12.91 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=50000` | 0.37 | 0.9978 | 8.21 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=2000` | 0.38 | 0.9761 | 5.56 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=2000` | 0.38 | 0.9880 | 10.64 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=10000` | 0.39 | 0.9738 | 7.34 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=50000` | 0.39 | 0.9975 | 9.40 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=10000` | 0.41 | 0.9852 | 4.33 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=10000` | 0.43 | 0.9936 | 15.25 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=10000` | 0.43 | 0.9939 | 14.13 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=2000` | 0.44 | 0.8978 | 13.33 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=2000` | 0.46 | 0.9887 | 10.30 | 0.98 | 2 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=50000` | 0.46 | 0.9976 | 7.96 | 0.99 | 1 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=10000` | 0.50 | 0.9941 | 12.55 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=50000` | 0.51 | 0.9954 | 11.85 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=50000` | 0.53 | 0.8404 | 14.84 | 0.98 | 2 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=50000` | 0.54 | 0.9958 | 11.31 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=10000` | 0.57 | 0.9889 | 17.47 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=50000` | 0.57 | 0.9961 | 10.82 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=2000` | 0.60 | 0.9624 | 6.83 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=2000` | 0.60 | 0.9872 | 9.66 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=10000` | 0.60 | 0.9888 | 17.64 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=50000` | 0.61 | 0.8621 | 14.40 | 0.99 | 1 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=50000` | 0.62 | 0.8495 | 14.35 | 0.98 | 2 |
| `shape=bimodal_alpha=0.30_tier=reign_heavy_N=50000` | 0.64 | 0.9966 | 1.89 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=half_century_heavy_N=50000` | 0.64 | 0.9986 | 4.53 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=2000` | 0.65 | 0.9839 | 19.82 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=50000` | 0.67 | 0.8579 | 14.37 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=2000` | 0.68 | 0.9299 | 10.82 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=2000` | 0.68 | 0.9855 | 17.71 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=10000` | 0.70 | 0.9957 | 6.90 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=2000` | 0.73 | 0.9796 | 12.15 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=2000` | 0.73 | 0.9876 | 9.97 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=2000` | 0.73 | 0.9901 | 12.98 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=10000` | 0.76 | 0.9891 | 15.84 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=2000` | 0.78 | 0.9740 | 4.19 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=2000` | 0.78 | 0.9897 | 11.24 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=2000` | 0.79 | 0.9711 | 24.00 | 0.99 | 1 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=10000` | 0.79 | 0.9890 | 2.66 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=reign_heavy_N=50000` | 0.79 | 0.9985 | 4.29 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=2000` | 0.81 | 0.9709 | 24.44 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=2000` | 0.81 | 0.9883 | 9.22 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=50000` | 0.82 | 0.8699 | 14.16 | 0.98 | 2 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=10000` | 0.82 | 0.9892 | 10.73 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=10000` | 0.83 | 0.9896 | 10.99 | 0.95 | 5 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=10000` | 0.84 | 0.9891 | 13.38 | 0.99 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=2000` | 0.85 | 0.9616 | 5.55 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000` | 0.85 | 0.9859 | 13.10 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=10000` | 0.86 | 0.9896 | 10.23 | 0.98 | 2 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=10000` | 0.87 | 0.4699 | 18.50 | 0.93 | 14 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=2000` | 0.88 | 0.9350 | 9.23 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=10000` | 0.88 | 0.9894 | 12.38 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=century_heavy_N=50000` | 0.88 | 0.9982 | 6.09 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=10000` | 0.88 | nan | 1.82 | 0.84 | 18 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=10000` | 0.89 | 0.4934 | 18.44 | 0.90 | 16 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=2000` | 0.89 | 0.9803 | 11.93 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=2000` | 0.89 | 0.9809 | 11.10 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=10000` | 0.89 | 0.9932 | 8.31 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=pilot_proxy_N=10000` | 0.89 | 0.9954 | 9.94 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=50000` | 0.89 | 0.9991 | 2.14 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=10000` | 0.90 | 0.5108 | 18.45 | 0.88 | 30 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=10000` | 0.90 | nan | 0.37 | 0.87 | 16 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=2000` | 0.91 | 0.9321 | 9.33 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=10000` | 0.92 | 0.7608 | 23.21 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=10000` | 0.92 | nan | 1.21 | 0.89 | 51 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=10000` | 0.93 | 0.5558 | 18.27 | 0.90 | 212 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=10000` | 0.93 | nan | 0.41 | 0.92 | 11 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=10000` | 0.93 | nan | 0.58 | 0.82 | 23 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=50000` | 0.93 | nan | 0.30 | 0.84 | 34 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=50000` | 0.93 | nan | 0.38 | 0.72 | 40 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=2000` | 0.93 | nan | 3.15 | 0.91 | 13 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=10000` | 0.93 | nan | 1.24 | 0.97 | 3 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=2000` | 0.94 | nan | 0.86 | 0.93 | 11 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=10000` | 0.94 | nan | 0.54 | 0.95 | 18 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=50000` | 0.94 | nan | 0.47 | 0.73 | 53 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=2000` | 0.94 | nan | 3.63 | 0.94 | 5 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=50000` | 0.94 | nan | 0.51 | 0.98 | 2 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=50000` | 0.94 | nan | 6.21 | 0.77 | 40 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=2000` | 0.95 | 0.2012 | 18.85 | 0.86 | 21 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.95 | 0.7961 | 52.21 | 0.89 | 18 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=50000` | 0.95 | nan | 0.22 | 0.99 | 1 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=50000` | 0.95 | nan | 0.17 | 0.89 | 14 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=2000` | 0.95 | nan | 1.64 | 0.96 | 4 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=10000` | 0.95 | nan | 0.63 | 0.80 | 23 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=2000` | 0.95 | nan | 1.23 | 0.96 | 3 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=2000` | 0.95 | nan | 1.85 | 0.99 | 1 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=50000` | 0.95 | nan | 0.42 | 0.93 | 9 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=50000` | 0.95 | nan | 0.62 | 0.73 | 42 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=50000` | 0.95 | nan | 4.01 | 0.16 | 2233 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=2000` | 0.96 | 0.1666 | 18.96 | 0.93 | 20 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=2000` | 0.96 | 0.3483 | 35.65 | 0.94 | 7 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=10000` | 0.96 | 0.8009 | 21.15 | 0.97 | 3 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=50000` | 0.96 | nan | 0.24 | 0.75 | 44 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=2000` | 0.96 | nan | 0.81 | 0.96 | 4 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=2000` | 0.96 | nan | 1.05 | 0.96 | 5 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=2000` | 0.96 | nan | 1.17 | 0.94 | 5 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=50000` | 0.96 | nan | 0.33 | 0.99 | 2 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=2000` | 0.96 | nan | 1.73 | 0.98 | 2 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=50000` | 0.96 | nan | 0.24 | 0.91 | 9 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=2000` | 0.96 | nan | 2.57 | 0.92 | 12 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=10000` | 0.96 | nan | 1.16 | 0.76 | 46 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=50000` | 0.96 | nan | 3.95 | 0.78 | 46 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=50000` | 0.96 | nan | 5.37 | 0.15 | 2359 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=50000` | 0.96 | nan | 3.37 | 0.48 | 211 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=2000` | 0.97 | 0.2303 | 19.02 | 0.93 | 9 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=2000` | 0.97 | 0.3833 | 36.15 | 0.95 | 5 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=10000` | 0.97 | 0.5394 | 18.33 | 0.69 | 308 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=2000` | 0.97 | 0.5987 | 48.91 | 0.97 | 5 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=10000` | 0.97 | 0.8991 | 35.58 | 0.86 | 53 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=10000` | 0.97 | 0.9285 | 30.33 | 0.96 | 5 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=50000` | 0.97 | nan | 0.14 | 0.92 | 14 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=2000` | 0.97 | nan | 0.77 | 0.81 | 25 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=2000` | 0.97 | nan | 0.90 | 0.87 | 15 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=10000` | 0.97 | nan | 0.57 | 0.95 | 9 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=50000` | 0.97 | nan | 0.21 | 0.95 | 6 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=10000` | 0.97 | nan | 0.35 | 0.90 | 33 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=2000` | 0.97 | nan | 2.77 | 0.98 | 4 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=50000` | 0.97 | nan | 0.51 | 0.83 | 17 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=2000` | 0.98 | 0.6785 | 48.40 | 0.97 | 4 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=10000` | 0.98 | 0.7337 | 25.75 | 0.91 | 45 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=10000` | 0.98 | 0.8052 | 18.61 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=2000` | 0.98 | 0.8295 | 49.55 | 0.98 | 2 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=2000` | 0.98 | 0.8579 | 44.03 | 0.93 | 7 |
| `shape=smooth_decline_alpha=0.95_tier=reign_heavy_N=2000` | 0.98 | 0.8727 | 42.74 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=10000` | 0.98 | 0.8841 | 26.61 | 0.85 | 401 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=10000` | 0.98 | 0.8963 | 36.52 | 0.96 | 7 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=2000` | 0.98 | 0.9046 | 38.59 | 0.97 | 3 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=10000` | 0.98 | 0.9401 | 27.92 | 0.90 | 18 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=10000` | 0.98 | 0.9433 | 20.04 | 0.91 | 16 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=10000` | 0.98 | nan | 0.29 | 0.88 | 13 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=50000` | 0.98 | nan | 0.21 | 0.70 | 74 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=10000` | 0.98 | nan | 0.38 | 0.91 | 19 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=2000` | 0.98 | nan | 1.03 | 0.97 | 3 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=50000` | 0.98 | nan | 0.35 | 0.81 | 34 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=10000` | 0.98 | nan | 0.62 | 0.96 | 4 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=10000` | 0.98 | nan | 0.64 | 0.97 | 4 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=10000` | 0.98 | nan | 1.10 | 0.97 | 3 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=2000` | 0.98 | nan | 4.50 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=10000` | 0.98 | nan | 6.78 | 0.70 | 91 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=2000` | 0.99 | 0.2816 | 18.88 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=2000` | 0.99 | 0.4125 | 35.04 | 0.95 | 8 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=2000` | 0.99 | 0.6665 | 47.96 | 0.97 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=2000` | 0.99 | 0.8199 | 46.82 | 0.96 | 4 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000` | 0.99 | 0.9294 | 35.62 | 0.92 | 13 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=10000` | 0.99 | 0.9318 | 32.18 | 0.88 | 14 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.99 | 0.9386 | 22.87 | 0.87 | 35 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=50000` | 0.99 | 0.9468 | 13.84 | 0.97 | 3 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=10000` | 0.99 | nan | 0.39 | 0.85 | 23 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=2000` | 0.99 | nan | 0.80 | 0.87 | 17 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=50000` | 0.99 | nan | 0.10 | 0.91 | 14 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=2000` | 0.99 | nan | 0.89 | 0.89 | 12 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=10000` | 0.99 | nan | 0.21 | 0.88 | 12 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=2000` | 0.99 | nan | 1.07 | 0.91 | 18 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=10000` | 0.99 | nan | 0.48 | 0.98 | 2 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=2000` | 0.99 | nan | 8.74 | 0.95 | 6 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.99 | nan | 5.17 | 0.30 | 1055 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.99 | nan | 6.49 | 0.85 | 19 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=2000` | 1.00 | 0.2769 | 37.06 | 0.99 | 1 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=2000` | 1.00 | 0.3005 | 19.37 | 0.96 | 3 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=2000` | 1.00 | 0.3455 | 36.49 | 0.96 | 9 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=2000` | 1.00 | 0.6790 | 46.86 | 0.99 | 1 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=2000` | 1.00 | 0.6862 | 46.70 | 0.99 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000` | 1.00 | 0.8110 | 19.67 | 0.94 | 8 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=2000` | 1.00 | 0.8247 | 46.83 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=2000` | 1.00 | 0.8652 | 41.19 | 0.98 | 7 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=2000` | 1.00 | 0.8848 | 41.66 | 0.89 | 17 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=10000` | 1.00 | 0.8905 | 32.14 | 0.75 | 269 |
| `shape=smooth_growth_alpha=0.95_tier=reign_heavy_N=2000` | 1.00 | 0.8973 | 37.36 | 0.98 | 1 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=10000` | 1.00 | 0.9102 | 31.20 | 0.96 | 4 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=10000` | 1.00 | 0.9377 | 22.55 | 0.85 | 52 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=10000` | 1.00 | 0.9409 | 28.86 | 0.93 | 8 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=50000` | 1.00 | nan | 0.20 | 0.90 | 14 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=10000` | 1.00 | nan | 0.38 | 0.88 | 17 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=2000` | 1.00 | nan | 0.81 | 0.75 | 30 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=50000` | 1.00 | nan | 0.17 | 0.99 | 1 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=50000` | 1.00 | nan | 0.17 | 0.93 | 7 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=10000` | 1.00 | nan | 8.84 | 0.92 | 32 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=2000` | 1.00 | nan | 9.53 | 0.95 | 18 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=10000` | 1.00 | nan | 9.78 | 0.81 | 29 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=10000` | 1.00 | nan | 6.95 | 0.24 | 944 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=2000` | 1.00 | nan | 7.10 | 0.99 | 1 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=2000` | 1.00 | nan | 8.09 | 0.93 | 11 |

## 4. Diagnostics

- Mean fit-seconds per replicate: 33.96
- Min cell-level convergence pass rate: 15.00%
- Cells with any divergences: 180/450

## 5. Wasserstein-1 supplementary

Wasserstein-1 is reported per cell as a distribution-sensitive shape metric (prereg §4 line 334). Its flagging threshold remains deferred (spec.md §5; needs empirical posteriors to anchor) and is NOT part of the binding rule.

- Median across cells: 7.90
- 90th percentile across cells: 19.39
