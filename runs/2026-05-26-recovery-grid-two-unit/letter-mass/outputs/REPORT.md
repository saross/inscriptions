# Recovery Grid — letter-mass — Per-Grid Report

Bayesian deconvolution-mixture model validation via the two-unit recovery simulation.
See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the binding decision rule, and the 2026-05-22 predecessor run for the shared cell design.

## 1. Headline result

**Unit of analysis:** letter-mass (each synthetic inscription deposits letter mass).

**Validation verdict:** FAIL (binding criteria require >= 90% of cells to pass coverage AND shape recovery)

| Criterion | Threshold | Result | Pass? |
|---|---|---|---|
| alpha-coverage >= 90% per cell | >= 90% of cells | 6.7% (30/450) | FAIL |
| median Pearson r >= 0.95 per cell | >= 90% of cells | 13.3% (60/450) | FAIL |
| Both criteria simultaneously | (informational) | 4.4% (20/450) | — |

> The verdict above is the **lodged** criterion, retained as a reference. The **binding** verdict is the corrected criterion in §1b.

## 1b. Corrected binding criterion (Decision 33 / §A5.5.1) — BINDING

Convergence precondition (≥ 90% of replicates converge) + hybrid shape gate (median Pearson r ≥ 0.95 for non-flat shapes; Wasserstein-1 ≤ 10 y for `flat_baseline`, where Pearson r is undefined), α demoted to a diagnostic, evaluated within the operating envelope (α ≤ 0.70). Cells with α ≥ 0.95 are a reported stress sensitivity, not gated. W1 + convergence are stored, so this is computed without re-fitting.

**Verdict: FAIL** — headline **0.0%** of in-envelope cells are clean passes (convergence AND shape), against a ≥ 90% bar.

| Figure | Definition | Value |
|---|---|---|
| **Headline (B)** | clean-pass (convergence AND shape) ÷ all in-envelope | **0.0%** (0/360) |
| Diagnostic (A) | shape-pass ÷ convergence-eligible in-envelope | nan% (0/0) |
| Convergence-excluded | non-converged in-envelope cells | 360 (by shape: {'bimodal': 60, 'flat_baseline': 60, 'regnal_cluster': 60, 'rise_and_fall': 60, 'smooth_decline': 60, 'smooth_growth': 60}) |
| Stress (α ≥ 0.95) | shape-pass among stress cells (not gated) | 5.6% (90 cells) |

## 2. Per-axis pass rates

### 2.alpha

| alpha | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 0.05 | 90 | 27% | 39% | 17% |
| 0.3 | 90 | 6% | 18% | 6% |
| 0.5 | 90 | 0% | 10% | 0% |
| 0.7 | 90 | 1% | 0% | 0% |
| 0.95 | 90 | 0% | 0% | 0% |

### 2.shape

| shape | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| bimodal | 75 | 3% | 8% | 3% |
| flat_baseline | 75 | 1% | 0% | 0% |
| regnal_cluster | 75 | 11% | 33% | 11% |
| rise_and_fall | 75 | 1% | 25% | 1% |
| smooth_decline | 75 | 15% | 7% | 7% |
| smooth_growth | 75 | 9% | 7% | 5% |

### 2.tier_weights

| tier_weights | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| century_heavy | 90 | 7% | 13% | 4% |
| half_century_heavy | 90 | 8% | 13% | 6% |
| pilot_proxy | 90 | 4% | 12% | 3% |
| reign_heavy | 90 | 7% | 13% | 4% |
| uniform | 90 | 8% | 14% | 4% |

### 2.N

| N | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 2000 | 150 | 1% | 0% | 0% |
| 10000 | 150 | 7% | 10% | 2% |
| 50000 | 150 | 12% | 30% | 11% |

## 3. Failed cells (either criterion)

| cell_id | alpha_cov | median Pearson r | median W-1 | convergence_pass | divergences |
|---|---|---|---|---|---|
| `shape=smooth_growth_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | -0.1135 | 70.68 | 0.75 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | -0.1105 | 64.61 | 0.61 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | -0.0923 | 21.49 | 0.60 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | -0.0915 | 22.63 | 0.64 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | -0.0907 | 63.08 | 0.63 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | -0.0540 | 21.84 | 0.42 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | -0.0451 | 20.94 | 0.50 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | -0.0359 | 61.60 | 0.55 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=2000` | 0.00 | -0.0349 | 60.54 | 0.59 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=2000` | 0.00 | -0.0202 | 59.14 | 0.64 | 0 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | -0.0175 | 23.56 | 0.73 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | -0.0143 | 64.43 | 0.64 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | 0.0082 | 58.41 | 0.16 | 9 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=10000` | 0.00 | 0.0115 | 57.61 | 0.53 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | 0.0165 | 51.79 | 0.54 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | 0.0231 | 52.88 | 0.68 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | 0.0307 | 51.87 | 0.59 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | 0.0361 | 55.73 | 0.39 | 0 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | 0.0395 | 21.17 | 0.53 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | 0.0397 | 61.08 | 0.38 | 0 |
| `shape=bimodal_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | 0.0416 | 19.86 | 0.14 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=10000` | 0.00 | 0.0462 | 55.77 | 0.49 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | 0.0582 | 51.60 | 0.62 | 1 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=2000` | 0.00 | 0.0670 | 19.46 | 0.56 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | 0.0693 | 18.84 | 0.40 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | 0.0703 | 39.97 | 0.61 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | 0.0732 | 58.92 | 0.70 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | 0.0734 | 59.06 | 0.66 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=10000` | 0.00 | 0.0989 | 18.82 | 0.59 | 0 |
| `shape=bimodal_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | 0.1036 | 18.80 | 0.17 | 6 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | 0.1037 | 50.20 | 0.58 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | 0.1084 | 46.30 | 0.73 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | 0.1089 | 57.14 | 0.59 | 1 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=50000` | 0.00 | 0.1162 | 53.85 | 0.34 | 186 |
| `shape=smooth_growth_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | 0.1192 | 56.98 | 0.11 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=50000` | 0.00 | 0.1235 | 52.01 | 0.37 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | 0.1299 | 46.03 | 0.49 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | 0.1305 | 47.62 | 0.38 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | 0.1318 | 52.92 | 0.55 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=50000` | 0.00 | 0.1482 | 17.89 | 0.31 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | 0.1541 | 47.62 | 0.60 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | 0.1583 | 44.20 | 0.58 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | 0.1597 | 55.60 | 0.50 | 2 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | 0.1603 | 49.37 | 0.44 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | 0.1881 | 53.85 | 0.40 | 2 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | 0.1919 | 51.35 | 0.45 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | 0.1995 | 24.53 | 0.56 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | 0.2039 | 45.89 | 0.19 | 4 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | 0.2051 | 19.60 | 0.53 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | 0.2098 | 38.52 | 0.58 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | 0.2144 | 34.19 | 0.59 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | 0.2197 | 47.91 | 0.45 | 0 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | 0.2214 | 18.73 | 0.75 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | 0.2251 | 48.84 | 0.15 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | 0.2253 | 16.94 | 0.52 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | 0.2310 | 52.28 | 0.43 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=uniform_N=2000` | 0.00 | 0.2489 | 39.57 | 0.58 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=2000` | 0.00 | 0.2518 | 28.60 | 0.55 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | 0.2523 | 45.44 | 0.57 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | 0.2530 | 36.15 | 0.56 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | 0.2560 | 40.52 | 0.80 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=uniform_N=2000` | 0.00 | 0.2577 | 39.63 | 0.55 | 0 |
| `shape=bimodal_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | 0.2730 | 16.92 | 0.32 | 0 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | 0.2821 | 16.41 | 0.48 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | 0.2882 | 16.47 | 0.60 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | 0.2886 | 34.41 | 0.35 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | 0.2910 | 45.94 | 0.14 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | 0.3019 | 25.03 | 0.63 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=2000` | 0.00 | 0.3204 | 39.96 | 0.65 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | 0.3218 | 24.95 | 0.66 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | 0.3229 | 40.61 | 0.50 | 1 |
| `shape=smooth_decline_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | 0.3250 | 41.93 | 0.51 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=10000` | 0.00 | 0.3295 | 40.45 | 0.62 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=2000` | 0.00 | 0.3302 | 14.86 | 0.57 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=10000` | 0.00 | 0.3337 | 28.03 | 0.66 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | 0.3344 | 30.07 | 0.61 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | 0.3546 | 39.70 | 0.54 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | 0.3623 | 33.75 | 0.52 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | 0.3748 | 35.44 | 0.56 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | 0.3789 | 32.07 | 0.45 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | 0.3804 | 35.19 | 0.44 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | 0.3871 | 30.28 | 0.47 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | 0.3989 | 24.98 | 0.47 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=half_century_heavy_N=10000` | 0.00 | 0.4015 | 36.64 | 0.65 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=50000` | 0.00 | 0.4017 | 40.10 | 0.48 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | 0.4152 | 14.66 | 0.58 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=reign_heavy_N=10000` | 0.00 | 0.4162 | 35.25 | 0.50 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | 0.4171 | 32.25 | 0.08 | 33 |
| `shape=rise_and_fall_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | 0.4192 | 38.20 | 0.23 | 262 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | 0.4397 | 35.04 | 0.70 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=uniform_N=2000` | 0.00 | 0.4399 | 29.22 | 0.50 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | 0.4471 | 38.46 | 0.48 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=uniform_N=2000` | 0.00 | 0.4599 | 28.16 | 0.51 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | 0.4618 | 22.19 | 0.49 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=2000` | 0.00 | 0.4694 | 13.07 | 0.40 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=pilot_proxy_N=2000` | 0.00 | 0.4718 | 29.13 | 0.44 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=50000` | 0.00 | 0.4718 | 26.72 | 0.28 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | 0.4770 | 24.42 | 0.44 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | 0.4813 | 13.91 | 0.54 | 0 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | 0.4856 | 12.02 | 0.47 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | 0.4877 | 36.31 | 0.54 | 0 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=10000` | 0.00 | 0.4882 | 14.60 | 0.40 | 34 |
| `shape=smooth_growth_alpha=0.70_tier=half_century_heavy_N=10000` | 0.00 | 0.4937 | 29.79 | 0.56 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=uniform_N=10000` | 0.00 | 0.4941 | 34.58 | 0.55 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | 0.4962 | 35.21 | 0.44 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=uniform_N=10000` | 0.00 | 0.5012 | 34.82 | 0.52 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | 0.5024 | 28.71 | 0.53 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | 0.5026 | 19.94 | 0.47 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | 0.5070 | 28.22 | 0.50 | 0 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=10000` | 0.00 | 0.5190 | 12.89 | 0.47 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | 0.5239 | 12.05 | 0.33 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=pilot_proxy_N=2000` | 0.00 | 0.5260 | 23.75 | 0.55 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | 0.5273 | 22.93 | 0.06 | 27 |
| `shape=smooth_decline_alpha=0.70_tier=century_heavy_N=10000` | 0.00 | 0.5279 | 37.43 | 0.55 | 6 |
| `shape=rise_and_fall_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | 0.5294 | 33.97 | 0.44 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=reign_heavy_N=10000` | 0.00 | 0.5409 | 23.37 | 0.62 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=2000` | 0.00 | 0.5525 | 10.66 | 0.44 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=century_heavy_N=10000` | 0.00 | 0.5626 | 35.51 | 0.53 | 7 |
| `shape=smooth_decline_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | 0.5632 | 29.74 | 0.53 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=10000` | 0.00 | 0.5759 | 12.04 | 0.48 | 5 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | 0.5900 | 26.70 | 0.48 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=2000` | 0.00 | 0.5962 | 28.26 | 0.46 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=pilot_proxy_N=2000` | 0.00 | 0.6149 | 17.83 | 0.40 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=10000` | 0.00 | 0.6152 | 11.34 | 0.46 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | 0.6175 | 22.73 | 0.52 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=century_heavy_N=2000` | 0.00 | 0.6209 | 16.51 | 0.51 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | 0.6217 | 10.32 | 0.55 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | 0.6322 | 17.82 | 0.39 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | 0.6440 | 28.66 | 0.47 | 0 |
| `shape=bimodal_alpha=0.30_tier=reign_heavy_N=2000` | 0.00 | 0.6673 | 9.32 | 0.29 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | 0.6759 | 24.25 | 0.49 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=2000` | 0.00 | 0.6772 | 8.64 | 0.26 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=2000` | 0.00 | 0.6804 | 8.51 | 0.28 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | 0.6848 | 32.72 | 0.59 | 1 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=2000` | 0.00 | 0.6856 | 8.07 | 0.31 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=2000` | 0.00 | 0.6883 | 24.64 | 0.47 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=10000` | 0.00 | 0.6921 | 36.22 | 0.45 | 5 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=50000` | 0.00 | 0.7064 | 12.20 | 0.22 | 40 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | 0.7105 | 26.49 | 0.61 | 0 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=2000` | 0.00 | 0.7127 | 7.86 | 0.33 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | 0.7152 | 16.94 | 0.60 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=2000` | 0.00 | 0.7176 | 18.66 | 0.35 | 0 |
| `shape=bimodal_alpha=0.70_tier=pilot_proxy_N=50000` | 0.00 | 0.7312 | 12.22 | 0.07 | 238 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=10000` | 0.00 | 0.7331 | 10.64 | 0.37 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | 0.7333 | 18.51 | 0.49 | 0 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=10000` | 0.00 | 0.7361 | 9.11 | 0.37 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000` | 0.00 | 0.7434 | 19.29 | 0.59 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=10000` | 0.00 | 0.7445 | 23.51 | 0.52 | 12 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=10000` | 0.00 | 0.7532 | 10.26 | 0.26 | 6 |
| `shape=bimodal_alpha=0.70_tier=reign_heavy_N=50000` | 0.00 | 0.7557 | 9.44 | 0.03 | 490 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=10000` | 0.00 | 0.7684 | 8.70 | 0.41 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=10000` | 0.00 | 0.7713 | 26.53 | 0.60 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | 0.7716 | 15.96 | 0.46 | 1 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=50000` | 0.00 | 0.7729 | 10.04 | 0.21 | 6 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=10000` | 0.00 | 0.7864 | 8.05 | 0.34 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=2000` | 0.00 | 0.7953 | 16.78 | 0.51 | 0 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=10000` | 0.00 | 0.7959 | 21.57 | 0.54 | 0 |
| `shape=bimodal_alpha=0.70_tier=half_century_heavy_N=50000` | 0.00 | 0.7971 | 9.20 | 0.31 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=2000` | 0.00 | 0.8086 | 15.17 | 0.52 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=reign_heavy_N=2000` | 0.00 | 0.8086 | 11.51 | 0.47 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | 0.8106 | 20.48 | 0.32 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=half_century_heavy_N=10000` | 0.00 | 0.8145 | 15.29 | 0.56 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | 0.8214 | 12.49 | 0.39 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=2000` | 0.00 | 0.8217 | 11.99 | 0.45 | 1 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=10000` | 0.00 | 0.8319 | 24.17 | 0.53 | 1 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=2000` | 0.00 | 0.8334 | 13.14 | 0.27 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=2000` | 0.00 | 0.8373 | 16.69 | 0.37 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | 0.8440 | 11.50 | 0.45 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=10000` | 0.00 | 0.8470 | 22.14 | 0.44 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=10000` | 0.00 | 0.8501 | 7.00 | 0.18 | 15 |
| `shape=rise_and_fall_alpha=0.70_tier=pilot_proxy_N=50000` | 0.00 | 0.8514 | 28.53 | 0.13 | 3 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=10000` | 0.00 | 0.8523 | 16.74 | 0.55 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=10000` | 0.00 | 0.8543 | 14.15 | 0.45 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | 0.8565 | 20.46 | 0.43 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=10000` | 0.00 | 0.8614 | 25.38 | 0.30 | 47 |
| `shape=rise_and_fall_alpha=0.70_tier=century_heavy_N=50000` | 0.00 | 0.8633 | 29.85 | 0.37 | 37 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=10000` | 0.00 | 0.8708 | 6.83 | 0.22 | 15 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=10000` | 0.00 | 0.8730 | 6.28 | 0.22 | 2 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=10000` | 0.00 | 0.8794 | 14.85 | 0.59 | 2 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.8814 | 9.62 | 0.12 | 226 |
| `shape=rise_and_fall_alpha=0.70_tier=reign_heavy_N=50000` | 0.00 | 0.8861 | 20.34 | 0.09 | 867 |
| `shape=bimodal_alpha=0.50_tier=reign_heavy_N=50000` | 0.00 | 0.8862 | 6.32 | 0.05 | 54 |
| `shape=rise_and_fall_alpha=0.70_tier=uniform_N=50000` | 0.00 | 0.8908 | 24.74 | 0.32 | 4 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=2000` | 0.00 | 0.8921 | 7.88 | 0.23 | 1 |
| `shape=rise_and_fall_alpha=0.70_tier=half_century_heavy_N=50000` | 0.00 | 0.8935 | 19.21 | 0.52 | 0 |
| `shape=bimodal_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.8936 | 8.63 | 0.10 | 44 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=2000` | 0.00 | 0.8948 | 8.75 | 0.22 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=10000` | 0.00 | 0.8958 | 13.43 | 0.44 | 1 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=10000` | 0.00 | 0.8968 | 18.17 | 0.43 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=2000` | 0.00 | 0.8981 | 9.46 | 0.25 | 0 |
| `shape=bimodal_alpha=0.50_tier=half_century_heavy_N=50000` | 0.00 | 0.9003 | 6.05 | 0.07 | 1 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=2000` | 0.00 | 0.9036 | 10.43 | 0.24 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9053 | 6.94 | 0.12 | 8 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=2000` | 0.00 | 0.9077 | 12.17 | 0.18 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=10000` | 0.00 | 0.9229 | 13.59 | 0.22 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=10000` | 0.00 | 0.9233 | 9.06 | 0.45 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=10000` | 0.00 | 0.9285 | 10.66 | 0.23 | 6 |
| `shape=rise_and_fall_alpha=0.30_tier=reign_heavy_N=10000` | 0.00 | 0.9303 | 8.44 | 0.30 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=10000` | 0.00 | 0.9304 | 15.27 | 0.17 | 52 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=50000` | 0.00 | 0.9319 | 14.73 | 0.16 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=10000` | 0.00 | 0.9376 | 8.80 | 0.36 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=half_century_heavy_N=10000` | 0.00 | 0.9381 | 8.07 | 0.26 | 151 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=10000` | 0.00 | 0.9385 | 13.26 | 0.37 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=10000` | 0.00 | 0.9400 | 14.16 | 0.29 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=10000` | 0.00 | 0.9407 | 10.30 | 0.40 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=reign_heavy_N=50000` | 0.00 | 0.9440 | 9.30 | 0.05 | 1 |
| `shape=rise_and_fall_alpha=0.50_tier=pilot_proxy_N=50000` | 0.00 | 0.9451 | 20.73 | 0.14 | 13 |
| `shape=rise_and_fall_alpha=0.50_tier=reign_heavy_N=50000` | 0.00 | 0.9508 | 12.38 | 0.08 | 559 |
| `shape=rise_and_fall_alpha=0.50_tier=century_heavy_N=50000` | 0.00 | 0.9525 | 23.36 | 0.11 | 621 |
| `shape=rise_and_fall_alpha=0.50_tier=uniform_N=50000` | 0.00 | 0.9557 | 16.69 | 0.28 | 0 |
| `shape=rise_and_fall_alpha=0.50_tier=half_century_heavy_N=50000` | 0.00 | 0.9576 | 12.12 | 0.47 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9773 | 9.17 | 0.31 | 1 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=2000` | 0.00 | nan | 7.63 | 0.63 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=2000` | 0.00 | nan | 12.39 | 0.61 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=2000` | 0.00 | nan | 12.34 | 0.56 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=2000` | 0.00 | nan | 9.63 | 0.58 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=2000` | 0.00 | nan | 16.33 | 0.61 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=10000` | 0.00 | nan | 7.84 | 0.49 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=2000` | 0.00 | nan | 8.52 | 0.52 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=2000` | 0.00 | nan | 13.87 | 0.64 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=2000` | 0.00 | nan | 10.59 | 0.60 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=10000` | 0.00 | nan | 8.42 | 0.57 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=2000` | 0.00 | nan | 8.80 | 0.64 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=50000` | 0.00 | nan | 8.86 | 0.40 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=10000` | 0.00 | nan | 17.98 | 0.62 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=2000` | 0.00 | nan | 20.10 | 0.61 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=half_century_heavy_N=50000` | 0.00 | nan | 15.85 | 0.48 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=10000` | 0.00 | nan | 9.30 | 0.51 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=2000` | 0.00 | nan | 10.05 | 0.65 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=pilot_proxy_N=50000` | 0.00 | nan | 8.17 | 0.18 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=10000` | 0.00 | nan | 16.66 | 0.53 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=2000` | 0.00 | nan | 18.12 | 0.73 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=reign_heavy_N=50000` | 0.00 | nan | 13.73 | 0.17 | 309 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=10000` | 0.00 | nan | 10.78 | 0.60 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=2000` | 0.00 | nan | 12.94 | 0.63 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=50000` | 0.00 | nan | 10.04 | 0.29 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=reign_heavy_N=2000` | 0.01 | 0.5627 | 18.26 | 0.37 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=uniform_N=2000` | 0.01 | 0.6193 | 14.82 | 0.43 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=century_heavy_N=2000` | 0.01 | 0.6338 | 15.07 | 0.44 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=half_century_heavy_N=10000` | 0.01 | 0.6665 | 22.40 | 0.60 | 1 |
| `shape=smooth_decline_alpha=0.50_tier=uniform_N=10000` | 0.01 | 0.7075 | 21.93 | 0.54 | 1 |
| `shape=smooth_growth_alpha=0.70_tier=half_century_heavy_N=50000` | 0.01 | 0.7089 | 23.31 | 0.30 | 1 |
| `shape=smooth_growth_alpha=0.70_tier=pilot_proxy_N=50000` | 0.01 | 0.7110 | 26.89 | 0.13 | 28 |
| `shape=smooth_decline_alpha=0.70_tier=century_heavy_N=50000` | 0.01 | 0.7282 | 27.38 | 0.33 | 2 |
| `shape=smooth_decline_alpha=0.50_tier=century_heavy_N=10000` | 0.01 | 0.7323 | 25.56 | 0.53 | 9 |
| `shape=smooth_decline_alpha=0.70_tier=pilot_proxy_N=50000` | 0.01 | 0.7430 | 22.11 | 0.11 | 55 |
| `shape=smooth_growth_alpha=0.70_tier=century_heavy_N=50000` | 0.01 | 0.7459 | 25.60 | 0.31 | 2 |
| `shape=smooth_decline_alpha=0.70_tier=reign_heavy_N=50000` | 0.01 | 0.7554 | 19.34 | 0.13 | 48 |
| `shape=rise_and_fall_alpha=0.30_tier=half_century_heavy_N=2000` | 0.01 | 0.8305 | 9.72 | 0.37 | 17 |
| `shape=regnal_cluster_alpha=0.70_tier=pilot_proxy_N=50000` | 0.01 | 0.9329 | 13.41 | 0.02 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=50000` | 0.01 | 0.9372 | 11.78 | 0.09 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=50000` | 0.01 | 0.9409 | 5.96 | 0.01 | 926 |
| `shape=rise_and_fall_alpha=0.30_tier=century_heavy_N=50000` | 0.01 | 0.9724 | 15.24 | 0.02 | 1144 |
| `shape=rise_and_fall_alpha=0.30_tier=pilot_proxy_N=50000` | 0.01 | 0.9743 | 12.39 | 0.12 | 7 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=2000` | 0.01 | nan | 9.37 | 0.60 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=10000` | 0.01 | nan | 8.78 | 0.50 | 6 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=10000` | 0.01 | nan | 12.04 | 0.61 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=half_century_heavy_N=2000` | 0.02 | 0.5942 | 18.38 | 0.42 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=pilot_proxy_N=2000` | 0.02 | 0.6359 | 12.67 | 0.46 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=half_century_heavy_N=2000` | 0.02 | 0.6403 | 13.63 | 0.42 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=half_century_heavy_N=50000` | 0.02 | 0.6814 | 26.27 | 0.44 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=pilot_proxy_N=10000` | 0.02 | 0.7119 | 22.97 | 0.57 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=uniform_N=50000` | 0.02 | 0.7145 | 26.08 | 0.27 | 1 |
| `shape=smooth_growth_alpha=0.70_tier=uniform_N=50000` | 0.02 | 0.7157 | 27.29 | 0.22 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=reign_heavy_N=10000` | 0.02 | 0.7374 | 13.45 | 0.66 | 1 |
| `shape=smooth_growth_alpha=0.50_tier=century_heavy_N=10000` | 0.02 | 0.7404 | 22.00 | 0.41 | 6 |
| `shape=smooth_decline_alpha=0.50_tier=pilot_proxy_N=10000` | 0.02 | 0.7501 | 18.74 | 0.44 | 0 |
| `shape=bimodal_alpha=0.30_tier=reign_heavy_N=10000` | 0.02 | 0.8517 | 6.47 | 0.23 | 5 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=10000` | 0.02 | 0.8666 | 5.80 | 0.15 | 183 |
| `shape=regnal_cluster_alpha=0.70_tier=half_century_heavy_N=50000` | 0.02 | 0.9268 | 10.47 | 0.17 | 1039 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=2000` | 0.02 | nan | 9.71 | 0.67 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=10000` | 0.02 | nan | 12.41 | 0.53 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=uniform_N=2000` | 0.03 | 0.5846 | 16.85 | 0.33 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=10000` | 0.03 | nan | 9.61 | 0.52 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=reign_heavy_N=50000` | 0.04 | 0.6686 | 25.66 | 0.10 | 41 |
| `shape=smooth_growth_alpha=0.50_tier=half_century_heavy_N=10000` | 0.04 | 0.6743 | 16.27 | 0.46 | 9 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=50000` | 0.04 | 0.9521 | 4.41 | 0.05 | 14 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=10000` | 0.04 | 0.9674 | 6.17 | 0.22 | 0 |
| `shape=rise_and_fall_alpha=0.30_tier=reign_heavy_N=50000` | 0.04 | 0.9756 | 6.54 | 0.11 | 105 |
| `shape=smooth_growth_alpha=0.50_tier=reign_heavy_N=10000` | 0.05 | 0.5958 | 22.14 | 0.52 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=reign_heavy_N=2000` | 0.05 | 0.6308 | 11.79 | 0.50 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=uniform_N=10000` | 0.05 | 0.6986 | 22.00 | 0.55 | 0 |
| `shape=bimodal_alpha=0.30_tier=pilot_proxy_N=50000` | 0.05 | 0.9394 | 5.65 | 0.06 | 114 |
| `shape=bimodal_alpha=0.30_tier=half_century_heavy_N=50000` | 0.05 | 0.9475 | 4.25 | 0.02 | 1766 |
| `shape=rise_and_fall_alpha=0.30_tier=half_century_heavy_N=50000` | 0.05 | 0.9779 | 6.50 | 0.42 | 0 |
| `shape=bimodal_alpha=0.30_tier=reign_heavy_N=50000` | 0.06 | 0.9472 | 3.99 | 0.03 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=pilot_proxy_N=10000` | 0.06 | 0.9659 | 6.97 | 0.24 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=10000` | 0.06 | 0.9669 | 8.49 | 0.21 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=half_century_heavy_N=10000` | 0.07 | 0.9673 | 5.60 | 0.26 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=reign_heavy_N=10000` | 0.09 | 0.9652 | 5.37 | 0.29 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=50000` | 0.10 | 0.9931 | 4.62 | 0.00 | 12391 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=50000` | 0.11 | 0.9936 | 4.85 | 0.00 | 13241 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=2000` | 0.14 | 0.8750 | 4.58 | 0.34 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=century_heavy_N=50000` | 0.16 | 0.8759 | 19.54 | 0.15 | 206 |
| `shape=regnal_cluster_alpha=0.50_tier=half_century_heavy_N=50000` | 0.17 | 0.9742 | 5.22 | 0.03 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=50000` | 0.17 | 0.9783 | 5.96 | 0.02 | 1013 |
| `shape=bimodal_alpha=0.05_tier=reign_heavy_N=2000` | 0.18 | 0.7862 | 5.97 | 0.29 | 0 |
| `shape=bimodal_alpha=0.05_tier=century_heavy_N=2000` | 0.18 | 0.7905 | 5.88 | 0.35 | 0 |
| `shape=bimodal_alpha=0.05_tier=uniform_N=2000` | 0.18 | 0.7957 | 6.12 | 0.41 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=pilot_proxy_N=50000` | 0.18 | 0.8909 | 14.31 | 0.19 | 15 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=50000` | 0.18 | 0.9943 | 3.88 | 0.00 | 8197 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=2000` | 0.19 | 0.9398 | 5.22 | 0.09 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=50000` | 0.19 | 0.9812 | 6.85 | 0.01 | 1939 |
| `shape=bimodal_alpha=0.05_tier=pilot_proxy_N=2000` | 0.20 | 0.7730 | 6.71 | 0.39 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=half_century_heavy_N=50000` | 0.20 | 0.8588 | 15.18 | 0.32 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=50000` | 0.21 | 0.9935 | 4.38 | 0.00 | 11987 |
| `shape=smooth_decline_alpha=0.30_tier=century_heavy_N=10000` | 0.23 | 0.8553 | 12.56 | 0.33 | 106 |
| `shape=rise_and_fall_alpha=0.05_tier=pilot_proxy_N=2000` | 0.23 | 0.8682 | 4.46 | 0.32 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=pilot_proxy_N=50000` | 0.23 | 0.9779 | 6.30 | 0.01 | 1447 |
| `shape=regnal_cluster_alpha=0.50_tier=reign_heavy_N=50000` | 0.23 | 0.9792 | 4.89 | 0.00 | 3376 |
| `shape=bimodal_alpha=0.05_tier=half_century_heavy_N=2000` | 0.24 | 0.8007 | 5.89 | 0.34 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=uniform_N=50000` | 0.24 | 0.8860 | 15.62 | 0.29 | 67 |
| `shape=regnal_cluster_alpha=0.05_tier=half_century_heavy_N=50000` | 0.26 | 0.9939 | 4.39 | 0.00 | 8741 |
| `shape=smooth_decline_alpha=0.30_tier=pilot_proxy_N=10000` | 0.27 | 0.8489 | 10.08 | 0.49 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=2000` | 0.28 | 0.9349 | 5.71 | 0.11 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=2000` | 0.28 | 0.9352 | 5.35 | 0.10 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=half_century_heavy_N=2000` | 0.29 | 0.8858 | 3.96 | 0.24 | 643 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=2000` | 0.29 | 0.9367 | 5.38 | 0.16 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=uniform_N=2000` | 0.30 | 0.8837 | 4.28 | 0.29 | 3 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=2000` | 0.30 | 0.9478 | 5.34 | 0.10 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=half_century_heavy_N=10000` | 0.31 | 0.8088 | 13.14 | 0.35 | 75 |
| `shape=smooth_decline_alpha=0.30_tier=uniform_N=10000` | 0.31 | 0.8204 | 10.69 | 0.43 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=reign_heavy_N=2000` | 0.32 | 0.8767 | 4.42 | 0.31 | 2 |
| `shape=smooth_growth_alpha=0.50_tier=century_heavy_N=50000` | 0.32 | 0.8893 | 16.21 | 0.19 | 2025 |
| `shape=smooth_growth_alpha=0.50_tier=uniform_N=50000` | 0.33 | 0.8618 | 16.38 | 0.13 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=century_heavy_N=10000` | 0.37 | 0.8332 | 12.25 | 0.41 | 1515 |
| `shape=smooth_growth_alpha=0.50_tier=half_century_heavy_N=50000` | 0.37 | 0.8671 | 12.32 | 0.33 | 44 |
| `shape=smooth_growth_alpha=0.50_tier=pilot_proxy_N=50000` | 0.38 | 0.8684 | 16.44 | 0.20 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=century_heavy_N=50000` | 0.40 | 0.9370 | 13.59 | 0.09 | 432 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=10000` | 0.41 | nan | 7.60 | 0.47 | 20 |
| `shape=smooth_decline_alpha=0.50_tier=reign_heavy_N=50000` | 0.43 | 0.8891 | 8.82 | 0.18 | 65 |
| `shape=smooth_growth_alpha=0.30_tier=pilot_proxy_N=10000` | 0.45 | 0.8243 | 13.75 | 0.46 | 11 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=10000` | 0.45 | 0.9604 | 3.26 | 0.06 | 353 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=10000` | 0.46 | nan | 6.92 | 0.38 | 29 |
| `shape=smooth_growth_alpha=0.30_tier=half_century_heavy_N=10000` | 0.47 | 0.8202 | 10.19 | 0.32 | 55 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=2000` | 0.47 | nan | 6.94 | 0.58 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=uniform_N=10000` | 0.48 | 0.8295 | 13.04 | 0.33 | 43 |
| `shape=smooth_decline_alpha=0.30_tier=pilot_proxy_N=50000` | 0.48 | 0.9351 | 8.52 | 0.25 | 26 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=50000` | 0.48 | 0.9884 | 2.53 | 0.03 | 234 |
| `shape=smooth_growth_alpha=0.50_tier=reign_heavy_N=50000` | 0.49 | 0.8619 | 12.60 | 0.11 | 12 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=2000` | 0.49 | nan | 8.89 | 0.57 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=50000` | 0.50 | nan | 5.64 | 0.21 | 2 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=10000` | 0.51 | nan | 6.41 | 0.53 | 54 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=2000` | 0.51 | nan | 9.34 | 0.64 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=2000` | 0.51 | nan | 9.02 | 0.70 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=reign_heavy_N=10000` | 0.52 | 0.8439 | 6.47 | 0.53 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=50000` | 0.52 | nan | 3.60 | 0.07 | 1448 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=10000` | 0.53 | nan | 6.09 | 0.35 | 126 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=50000` | 0.54 | nan | 4.27 | 0.14 | 1150 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=50000` | 0.54 | nan | 3.69 | 0.12 | 921 |
| `shape=bimodal_alpha=0.05_tier=pilot_proxy_N=10000` | 0.55 | 0.9302 | 3.16 | 0.08 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=50000` | 0.55 | nan | 4.10 | 0.16 | 918 |
| `shape=rise_and_fall_alpha=0.05_tier=pilot_proxy_N=10000` | 0.56 | 0.9574 | 3.05 | 0.08 | 320 |
| `shape=smooth_decline_alpha=0.30_tier=uniform_N=50000` | 0.58 | 0.9309 | 8.53 | 0.25 | 33 |
| `shape=smooth_growth_alpha=0.30_tier=century_heavy_N=50000` | 0.58 | 0.9316 | 10.05 | 0.09 | 1479 |
| `shape=smooth_decline_alpha=0.30_tier=half_century_heavy_N=50000` | 0.59 | 0.9250 | 8.91 | 0.24 | 12 |
| `shape=smooth_growth_alpha=0.30_tier=uniform_N=50000` | 0.59 | 0.9350 | 10.19 | 0.19 | 81 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=50000` | 0.59 | nan | 4.07 | 0.10 | 1649 |
| `shape=bimodal_alpha=0.05_tier=reign_heavy_N=10000` | 0.61 | 0.9194 | 3.48 | 0.05 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=10000` | 0.61 | nan | 5.37 | 0.51 | 51 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=50000` | 0.61 | nan | 5.63 | 0.19 | 63 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=50000` | 0.61 | nan | 5.94 | 0.30 | 87 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=50000` | 0.62 | nan | 5.91 | 0.23 | 266 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=50000` | 0.62 | nan | 5.61 | 0.29 | 17 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=50000` | 0.62 | nan | 8.55 | 0.35 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=reign_heavy_N=10000` | 0.63 | 0.7912 | 12.09 | 0.49 | 2 |
| `shape=bimodal_alpha=0.05_tier=uniform_N=10000` | 0.63 | 0.9307 | 3.36 | 0.07 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=2000` | 0.63 | nan | 9.46 | 0.60 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=50000` | 0.65 | nan | 7.66 | 0.38 | 8 |
| `shape=bimodal_alpha=0.05_tier=century_heavy_N=10000` | 0.67 | 0.9241 | 3.68 | 0.10 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=half_century_heavy_N=50000` | 0.67 | 0.9267 | 6.85 | 0.11 | 178 |
| `shape=rise_and_fall_alpha=0.05_tier=pilot_proxy_N=50000` | 0.67 | 0.9881 | 2.30 | 0.04 | 401 |
| `shape=flat_baseline_alpha=0.30_tier=pilot_proxy_N=10000` | 0.67 | nan | 9.46 | 0.44 | 21 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=50000` | 0.68 | nan | 6.51 | 0.18 | 3 |
| `shape=smooth_growth_alpha=0.30_tier=pilot_proxy_N=50000` | 0.69 | 0.9279 | 10.22 | 0.13 | 12 |
| `shape=rise_and_fall_alpha=0.05_tier=uniform_N=10000` | 0.69 | 0.9659 | 2.59 | 0.11 | 2890 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=10000` | 0.70 | nan | 7.25 | 0.50 | 22 |
| `shape=flat_baseline_alpha=0.30_tier=reign_heavy_N=10000` | 0.72 | nan | 7.50 | 0.52 | 6 |
| `shape=flat_baseline_alpha=0.30_tier=half_century_heavy_N=10000` | 0.73 | nan | 8.20 | 0.55 | 2 |
| `shape=rise_and_fall_alpha=0.05_tier=half_century_heavy_N=10000` | 0.74 | 0.9641 | 2.37 | 0.04 | 3322 |
| `shape=bimodal_alpha=0.05_tier=century_heavy_N=50000` | 0.74 | 0.9785 | 1.83 | 0.00 | 2296 |
| `shape=flat_baseline_alpha=0.05_tier=half_century_heavy_N=2000` | 0.74 | nan | 8.52 | 0.62 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=50000` | 0.74 | nan | 6.66 | 0.20 | 44 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=10000` | 0.74 | nan | 8.36 | 0.59 | 0 |
| `shape=bimodal_alpha=0.05_tier=half_century_heavy_N=10000` | 0.75 | 0.9247 | 3.72 | 0.12 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=reign_heavy_N=10000` | 0.75 | 0.9616 | 2.76 | 0.10 | 546 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=50000` | 0.75 | nan | 6.09 | 0.41 | 68 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=2000` | 0.77 | nan | 7.69 | 0.54 | 0 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=10000` | 0.77 | nan | 7.57 | 0.59 | 3 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=50000` | 0.77 | nan | 8.36 | 0.45 | 17 |
| `shape=rise_and_fall_alpha=0.05_tier=uniform_N=50000` | 0.79 | 0.9858 | 1.77 | 0.11 | 434 |
| `shape=flat_baseline_alpha=0.05_tier=reign_heavy_N=2000` | 0.79 | nan | 8.01 | 0.58 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=century_heavy_N=2000` | 0.80 | 0.7612 | 6.58 | 0.30 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=pilot_proxy_N=2000` | 0.81 | nan | 8.34 | 0.52 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=half_century_heavy_N=10000` | 0.81 | nan | 9.90 | 0.56 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=2000` | 0.82 | nan | 7.64 | 0.59 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=10000` | 0.82 | nan | 7.52 | 0.52 | 12 |
| `shape=smooth_growth_alpha=0.05_tier=century_heavy_N=2000` | 0.83 | 0.7612 | 5.63 | 0.35 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=uniform_N=2000` | 0.84 | 0.7267 | 6.42 | 0.33 | 0 |
| `shape=bimodal_alpha=0.05_tier=pilot_proxy_N=50000` | 0.84 | 0.9719 | 2.02 | 0.00 | 6810 |
| `shape=flat_baseline_alpha=0.50_tier=reign_heavy_N=10000` | 0.84 | nan | 10.97 | 0.55 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=pilot_proxy_N=50000` | 0.84 | nan | 7.53 | 0.21 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=half_century_heavy_N=2000` | 0.85 | 0.7454 | 6.79 | 0.39 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=reign_heavy_N=2000` | 0.86 | 0.7513 | 5.72 | 0.37 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=pilot_proxy_N=2000` | 0.86 | 0.7543 | 5.99 | 0.44 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=uniform_N=10000` | 0.86 | 0.8965 | 4.17 | 0.22 | 86 |
| `shape=regnal_cluster_alpha=0.05_tier=reign_heavy_N=10000` | 0.86 | 0.9823 | 3.25 | 0.14 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=half_century_heavy_N=50000` | 0.86 | 0.9887 | 1.68 | 0.05 | 3579 |
| `shape=flat_baseline_alpha=0.70_tier=reign_heavy_N=50000` | 0.86 | nan | 10.64 | 0.21 | 33 |
| `shape=smooth_growth_alpha=0.05_tier=half_century_heavy_N=2000` | 0.87 | 0.7353 | 6.65 | 0.36 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=pilot_proxy_N=2000` | 0.87 | 0.7393 | 6.88 | 0.34 | 0 |
| `shape=flat_baseline_alpha=0.50_tier=pilot_proxy_N=10000` | 0.87 | nan | 6.89 | 0.45 | 1 |
| `shape=flat_baseline_alpha=0.70_tier=half_century_heavy_N=50000` | 0.87 | nan | 10.52 | 0.33 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=reign_heavy_N=50000` | 0.88 | 0.9610 | 2.94 | 0.01 | 2674 |
| `shape=bimodal_alpha=0.05_tier=uniform_N=50000` | 0.88 | 0.9767 | 1.85 | 0.00 | 27 |
| `shape=regnal_cluster_alpha=0.05_tier=pilot_proxy_N=10000` | 0.88 | 0.9824 | 3.28 | 0.08 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=reign_heavy_N=2000` | 0.89 | 0.7443 | 6.71 | 0.32 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=pilot_proxy_N=10000` | 0.89 | 0.9024 | 4.24 | 0.17 | 103 |
| `shape=smooth_growth_alpha=0.30_tier=reign_heavy_N=50000` | 0.89 | 0.9344 | 7.16 | 0.16 | 5 |
| `shape=smooth_decline_alpha=0.30_tier=reign_heavy_N=50000` | 0.89 | 0.9378 | 3.78 | 0.16 | 8 |
| `shape=smooth_decline_alpha=0.05_tier=reign_heavy_N=10000` | 0.90 | 0.9005 | 3.96 | 0.30 | 1 |
| `shape=smooth_growth_alpha=0.05_tier=century_heavy_N=10000` | 0.91 | 0.8998 | 3.73 | 0.13 | 195 |
| `shape=smooth_decline_alpha=0.05_tier=pilot_proxy_N=10000` | 0.91 | 0.9116 | 4.26 | 0.30 | 17 |
| `shape=smooth_growth_alpha=0.05_tier=reign_heavy_N=10000` | 0.92 | 0.9045 | 3.66 | 0.22 | 1402 |
| `shape=smooth_decline_alpha=0.05_tier=uniform_N=10000` | 0.92 | 0.9063 | 4.41 | 0.26 | 28 |
| `shape=smooth_decline_alpha=0.05_tier=uniform_N=2000` | 0.93 | 0.7445 | 6.14 | 0.33 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=half_century_heavy_N=10000` | 0.93 | 0.9000 | 4.09 | 0.20 | 76 |
| `shape=smooth_decline_alpha=0.05_tier=half_century_heavy_N=10000` | 0.93 | 0.9006 | 3.78 | 0.26 | 15 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=50000` | 0.93 | nan | 8.39 | 0.34 | 0 |
| `shape=smooth_decline_alpha=0.05_tier=century_heavy_N=10000` | 0.95 | 0.9065 | 3.63 | 0.20 | 11 |

## 4. Diagnostics

- Mean fit-seconds per replicate: 149.52
- Min cell-level convergence pass rate: 0.00%
- Cells with any divergences: 183/450

## 5. Wasserstein-1 supplementary

Wasserstein-1 is reported per cell as a distribution-sensitive shape metric (prereg §4 line 334). Its flagging threshold remains deferred (spec.md §5; needs empirical posteriors to anchor) and is NOT part of the binding rule.

- Median across cells: 12.19
- 90th percentile across cells: 39.96
