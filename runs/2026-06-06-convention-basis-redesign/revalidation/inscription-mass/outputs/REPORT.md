# Recovery Grid — inscription-mass — Per-Grid Report

Bayesian deconvolution-mixture model validation via the two-unit recovery simulation.
See `runs/2026-05-26-recovery-grid-two-unit/spec.md` §5 for the binding decision rule, and the 2026-05-22 predecessor run for the shared cell design.

## 1. Headline result

**Unit of analysis:** inscription-mass (each synthetic inscription deposits unit count).

**Validation verdict:** FAIL (binding criteria require >= 90% of cells to pass coverage AND shape recovery)

| Criterion | Threshold | Result | Pass? |
|---|---|---|---|
| alpha-coverage >= 90% per cell | >= 90% of cells | 71.8% (323/450) | FAIL |
| median Pearson r >= 0.95 per cell | >= 90% of cells | 65.8% (296/450) | FAIL |
| Both criteria simultaneously | (informational) | 40.9% (184/450) | — |

> The verdict above is the **lodged** criterion, retained as a reference. The **binding** verdict is the corrected criterion in §1b.

## 1b. Corrected binding criterion (Decision 33 / §A5.5.1) — BINDING

Convergence precondition (≥ 90% of replicates converge) + hybrid shape gate (median Pearson r ≥ 0.95 for non-flat shapes; Wasserstein-1 ≤ 10 y for `flat_baseline`, where Pearson r is undefined), α demoted to a diagnostic, evaluated within the operating envelope (α ≤ 0.70). Cells with α ≥ 0.95 are a reported stress sensitivity, not gated. W1 + convergence are stored, so this is computed without re-fitting.

**Verdict: PASS** — headline **96.4%** of in-envelope cells are clean passes (convergence AND shape), against a ≥ 90% bar.

| Figure | Definition | Value |
|---|---|---|
| **Headline (B)** | clean-pass (convergence AND shape) ÷ all in-envelope | **96.4%** (347/360) |
| Diagnostic (A) | shape-pass ÷ convergence-eligible in-envelope | 97.2% (347/357) |
| Convergence-excluded | non-converged in-envelope cells | 3 (by shape: {'regnal_cluster': 3}) |
| Stress (α ≥ 0.95) | shape-pass among stress cells (not gated) | 17.8% (90 cells) |

> **Convergence-excluded cells.** 3 in-envelope cell(s) fall below the convergence precondition (< 90% of replicates pass R̂ / bulk-ESS) and so are excluded from the headline (B 96.4%) but not from the diagnostic (A 97.2%); by shape: {'regnal_cluster': 3}. Under the field-standard gate (R̂ / bulk-ESS only; divergences are recorded but not auto-failing — `cell_lib.convergence_pass`, Decision 33 / §A5.5.1) these are genuine sampling-convergence failures, not the benign flat-null divergences the earlier zero-tolerance gate tripped on.

## 2. Per-axis pass rates

### 2.alpha

| alpha | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 0.05 | 90 | 70% | 83% | 53% |
| 0.3 | 90 | 67% | 83% | 50% |
| 0.5 | 90 | 67% | 80% | 47% |
| 0.7 | 90 | 73% | 76% | 51% |
| 0.95 | 90 | 82% | 7% | 3% |

### 2.shape

| shape | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| bimodal | 75 | 56% | 68% | 25% |
| flat_baseline | 75 | 100% | 0% | 0% |
| regnal_cluster | 75 | 43% | 83% | 25% |
| rise_and_fall | 75 | 80% | 81% | 68% |
| smooth_decline | 75 | 80% | 79% | 67% |
| smooth_growth | 75 | 72% | 84% | 60% |

### 2.tier_weights

| tier_weights | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| century_heavy | 90 | 71% | 66% | 40% |
| empirical | 90 | 76% | 64% | 43% |
| multicentury_heavy | 90 | 67% | 64% | 38% |
| subcentury_heavy | 90 | 70% | 69% | 39% |
| uniform | 90 | 76% | 66% | 44% |

### 2.N

| N | n_cells | alpha-cov pass | shape pass | both |
|---|---|---|---|---|
| 2000 | 150 | 91% | 61% | 53% |
| 10000 | 150 | 67% | 66% | 38% |
| 50000 | 150 | 57% | 71% | 32% |

## 3. Failed cells (either criterion)

| cell_id | alpha_cov | median Pearson r | median W-1 | convergence_pass | divergences |
|---|---|---|---|---|---|
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=50000` | 0.00 | 0.9966 | 13.83 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=10000` | 0.00 | 0.9971 | 7.15 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=empirical_N=50000` | 0.00 | 0.9972 | 11.41 | 0.97 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=50000` | 0.00 | 0.9976 | 10.07 | 0.97 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=subcentury_heavy_N=50000` | 0.00 | 0.9978 | 9.08 | 0.97 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=50000` | 0.00 | 0.9979 | 8.69 | 0.93 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=empirical_N=50000` | 0.00 | 0.9980 | 8.27 | 0.87 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=50000` | 0.00 | 0.9980 | 8.15 | 0.84 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=subcentury_heavy_N=50000` | 0.00 | 0.9980 | 7.99 | 0.90 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=multicentury_heavy_N=50000` | 0.00 | 0.9980 | 7.88 | 0.88 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=50000` | 0.01 | 0.9936 | 2.74 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=empirical_N=50000` | 0.01 | 0.9955 | 14.99 | 0.99 | 2 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=50000` | 0.01 | 0.9962 | 13.83 | 0.99 | 2 |
| `shape=regnal_cluster_alpha=0.05_tier=subcentury_heavy_N=10000` | 0.01 | 0.9971 | 6.50 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=empirical_N=10000` | 0.01 | 0.9971 | 6.47 | 0.98 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=50000` | 0.02 | 0.9934 | 19.42 | 0.98 | 3 |
| `shape=regnal_cluster_alpha=0.50_tier=subcentury_heavy_N=50000` | 0.02 | 0.9970 | 11.14 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=multicentury_heavy_N=50000` | 0.02 | 0.9980 | 7.82 | 1.00 | 1 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=50000` | 0.04 | 0.9918 | 3.22 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=empirical_N=50000` | 0.05 | 0.9936 | 3.40 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=10000` | 0.05 | 0.9971 | 6.44 | 0.99 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=50000` | 0.06 | 0.9903 | 3.63 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=multicentury_heavy_N=10000` | 0.06 | 0.9974 | 6.14 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=empirical_N=50000` | 0.07 | 0.9901 | 3.74 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=multicentury_heavy_N=50000` | 0.10 | 0.9879 | 6.80 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=50000` | 0.12 | 0.9875 | 3.75 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=multicentury_heavy_N=50000` | 0.12 | 0.9909 | 5.93 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=multicentury_heavy_N=50000` | 0.14 | 0.9977 | 7.79 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=subcentury_heavy_N=50000` | 0.16 | 0.9919 | 2.86 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=subcentury_heavy_N=10000` | 0.17 | 0.9960 | 7.73 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=50000` | 0.19 | 0.9992 | 1.22 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=multicentury_heavy_N=50000` | 0.22 | 0.9991 | 1.41 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=empirical_N=50000` | 0.22 | 0.9992 | 1.21 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=subcentury_heavy_N=50000` | 0.24 | 0.9907 | 2.85 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=multicentury_heavy_N=50000` | 0.27 | 0.9801 | 8.14 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=50000` | 0.30 | 0.9815 | 5.64 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=empirical_N=50000` | 0.30 | 0.9815 | 5.56 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=10000` | 0.31 | 0.9953 | 11.81 | 0.99 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=subcentury_heavy_N=50000` | 0.32 | 0.9944 | 14.84 | 1.00 | 5 |
| `shape=regnal_cluster_alpha=0.70_tier=uniform_N=50000` | 0.34 | 0.9927 | 17.74 | 0.95 | 7 |
| `shape=bimodal_alpha=0.30_tier=multicentury_heavy_N=10000` | 0.35 | 0.9804 | 7.26 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=subcentury_heavy_N=2000` | 0.36 | 0.9920 | 5.70 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=subcentury_heavy_N=10000` | 0.37 | 0.9825 | 4.40 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=10000` | 0.37 | 0.9869 | 3.64 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=century_heavy_N=10000` | 0.38 | 0.9844 | 3.99 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=uniform_N=2000` | 0.38 | 0.9914 | 5.90 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=50000` | 0.41 | 0.9816 | 4.43 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=empirical_N=10000` | 0.41 | 0.9855 | 4.20 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=uniform_N=50000` | 0.43 | 0.9992 | 1.28 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=uniform_N=10000` | 0.44 | 0.9961 | 8.26 | 1.00 | 1 |
| `shape=bimodal_alpha=0.70_tier=subcentury_heavy_N=50000` | 0.45 | 0.9844 | 4.17 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=empirical_N=50000` | 0.51 | 0.9920 | 18.71 | 0.98 | 5 |
| `shape=regnal_cluster_alpha=0.30_tier=empirical_N=10000` | 0.52 | 0.9958 | 8.32 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=century_heavy_N=2000` | 0.55 | 0.9915 | 5.36 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=century_heavy_N=50000` | 0.57 | 0.9916 | 18.72 | 1.00 | 10 |
| `shape=regnal_cluster_alpha=0.50_tier=subcentury_heavy_N=10000` | 0.59 | 0.9942 | 9.20 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=empirical_N=10000` | 0.60 | 0.9775 | 5.15 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=uniform_N=10000` | 0.62 | 0.9797 | 4.58 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=empirical_N=2000` | 0.62 | 0.9916 | 5.32 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=10000` | 0.63 | 0.9759 | 4.80 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=multicentury_heavy_N=10000` | 0.65 | 0.9695 | 10.10 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=empirical_N=10000` | 0.65 | 0.9969 | 1.45 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=century_heavy_N=10000` | 0.67 | 0.9970 | 1.36 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=multicentury_heavy_N=50000` | 0.68 | 0.9972 | 13.13 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=empirical_N=50000` | 0.70 | 0.8929 | 48.88 | 1.00 | 85 |
| `shape=bimodal_alpha=0.50_tier=subcentury_heavy_N=10000` | 0.70 | 0.9811 | 3.64 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.05_tier=multicentury_heavy_N=2000` | 0.70 | 0.9914 | 4.99 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=empirical_N=10000` | 0.70 | 0.9934 | 12.76 | 1.00 | 6 |
| `shape=regnal_cluster_alpha=0.50_tier=century_heavy_N=10000` | 0.72 | 0.9919 | 15.16 | 1.00 | 2 |
| `shape=regnal_cluster_alpha=0.30_tier=subcentury_heavy_N=2000` | 0.73 | 0.9875 | 9.03 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=multicentury_heavy_N=2000` | 0.74 | 0.9187 | 46.75 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=subcentury_heavy_N=50000` | 0.74 | 0.9948 | 2.92 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=multicentury_heavy_N=10000` | 0.74 | 0.9970 | 1.58 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=multicentury_heavy_N=10000` | 0.75 | 0.9877 | 24.82 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.50_tier=uniform_N=10000` | 0.75 | 0.9937 | 11.36 | 1.00 | 4 |
| `shape=smooth_decline_alpha=0.50_tier=multicentury_heavy_N=50000` | 0.75 | 0.9954 | 16.76 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=subcentury_heavy_N=50000` | 0.76 | 0.9900 | 4.41 | 1.00 | 34 |
| `shape=smooth_growth_alpha=0.50_tier=century_heavy_N=50000` | 0.77 | 0.9943 | 3.10 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=subcentury_heavy_N=50000` | 0.77 | 0.9990 | 1.60 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=multicentury_heavy_N=50000` | 0.78 | 0.9155 | 48.37 | 1.00 | 8 |
| `shape=regnal_cluster_alpha=0.30_tier=multicentury_heavy_N=10000` | 0.78 | 0.9962 | 5.56 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=subcentury_heavy_N=50000` | 0.78 | 0.9979 | 2.02 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=multicentury_heavy_N=10000` | 0.79 | 0.9437 | 14.36 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=century_heavy_N=50000` | 0.79 | 0.9967 | 2.47 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=subcentury_heavy_N=50000` | 0.80 | 0.9503 | 18.81 | 0.97 | 108 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=50000` | 0.80 | 0.9514 | 20.08 | 1.00 | 28 |
| `shape=smooth_growth_alpha=0.70_tier=century_heavy_N=50000` | 0.80 | 0.9902 | 4.54 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.05_tier=uniform_N=10000` | 0.80 | 0.9970 | 1.47 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.81 | 0.8382 | 35.83 | 1.00 | 3 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=10000` | 0.82 | 0.8280 | 33.10 | 1.00 | 6 |
| `shape=bimodal_alpha=0.70_tier=subcentury_heavy_N=10000` | 0.82 | 0.9666 | 5.30 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=50000` | 0.83 | 0.9392 | 14.01 | 1.00 | 7 |
| `shape=smooth_growth_alpha=0.95_tier=empirical_N=50000` | 0.83 | 0.9440 | 18.40 | 1.00 | 34 |
| `shape=bimodal_alpha=0.30_tier=subcentury_heavy_N=2000` | 0.83 | 0.9643 | 5.89 | 1.00 | 0 |
| `shape=bimodal_alpha=0.30_tier=multicentury_heavy_N=2000` | 0.83 | 0.9643 | 8.17 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=multicentury_heavy_N=50000` | 0.83 | 0.9920 | 19.31 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=century_heavy_N=10000` | 0.83 | 0.9928 | 3.59 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.30_tier=multicentury_heavy_N=10000` | 0.83 | 0.9928 | 16.94 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.30_tier=subcentury_heavy_N=50000` | 0.83 | 0.9966 | 2.51 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=10000` | 0.84 | 0.9581 | 7.79 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=empirical_N=10000` | 0.85 | 0.7416 | 55.99 | 1.00 | 4 |
| `shape=smooth_growth_alpha=0.70_tier=empirical_N=50000` | 0.85 | 0.9907 | 4.00 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.70_tier=empirical_N=50000` | 0.85 | 0.9913 | 19.32 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.70_tier=multicentury_heavy_N=50000` | 0.85 | 0.9963 | 8.64 | 0.98 | 1 |
| `shape=smooth_decline_alpha=0.70_tier=multicentury_heavy_N=10000` | 0.86 | 0.9743 | 30.65 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.70_tier=uniform_N=50000` | 0.86 | 0.9900 | 4.80 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=uniform_N=50000` | 0.86 | 0.9949 | 3.14 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.50_tier=empirical_N=50000` | 0.86 | 0.9960 | 12.23 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=50000` | 0.87 | 0.9496 | 16.71 | 1.00 | 18 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=10000` | 0.87 | 0.9534 | 6.84 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.05_tier=subcentury_heavy_N=10000` | 0.87 | 0.9957 | 2.96 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.88 | 0.7420 | 57.30 | 1.00 | 1 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=10000` | 0.88 | 0.8896 | 31.34 | 1.00 | 11 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=50000` | 0.88 | 0.9496 | 39.68 | 1.00 | 1 |
| `shape=smooth_growth_alpha=0.95_tier=multicentury_heavy_N=50000` | 0.88 | 0.9540 | 12.73 | 1.00 | 1 |
| `shape=bimodal_alpha=0.70_tier=empirical_N=10000` | 0.88 | 0.9582 | 7.23 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=subcentury_heavy_N=10000` | 0.88 | 0.9876 | 5.38 | 1.00 | 1 |
| `shape=smooth_growth_alpha=0.50_tier=century_heavy_N=10000` | 0.88 | 0.9876 | 4.96 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=10000` | 0.89 | 0.8229 | 34.05 | 1.00 | 3 |
| `shape=rise_and_fall_alpha=0.95_tier=multicentury_heavy_N=50000` | 0.89 | 0.9353 | 12.93 | 1.00 | 6 |
| `shape=smooth_decline_alpha=0.50_tier=multicentury_heavy_N=2000` | 0.89 | 0.9613 | 29.92 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.50_tier=subcentury_heavy_N=2000` | 0.89 | 0.9736 | 8.07 | 1.00 | 2 |
| `shape=bimodal_alpha=0.30_tier=uniform_N=2000` | 0.89 | 0.9739 | 4.12 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.30_tier=century_heavy_N=2000` | 0.89 | 0.9865 | 9.05 | 1.00 | 2 |
| `shape=regnal_cluster_alpha=0.70_tier=subcentury_heavy_N=10000` | 0.89 | 0.9885 | 14.44 | 1.00 | 4 |
| `shape=regnal_cluster_alpha=0.50_tier=multicentury_heavy_N=10000` | 0.89 | 0.9943 | 5.35 | 1.00 | 1 |
| `shape=rise_and_fall_alpha=0.05_tier=subcentury_heavy_N=10000` | 0.89 | 0.9969 | 1.83 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=50000` | 0.90 | 0.9205 | 45.91 | 1.00 | 20 |
| `shape=rise_and_fall_alpha=0.95_tier=empirical_N=50000` | 0.90 | 0.9336 | 13.42 | 1.00 | 14 |
| `shape=smooth_decline_alpha=0.95_tier=subcentury_heavy_N=50000` | 0.90 | 0.9378 | 39.49 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=century_heavy_N=2000` | 0.90 | 0.9460 | 6.64 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=10000` | 0.91 | 0.7807 | 56.79 | 1.00 | 1 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=10000` | 0.91 | 0.8469 | 40.09 | 0.99 | 10 |
| `shape=smooth_growth_alpha=0.95_tier=empirical_N=10000` | 0.91 | 0.8760 | 31.74 | 1.00 | 14 |
| `shape=rise_and_fall_alpha=0.95_tier=subcentury_heavy_N=10000` | 0.92 | 0.8041 | 34.22 | 1.00 | 4 |
| `shape=rise_and_fall_alpha=0.95_tier=empirical_N=10000` | 0.93 | 0.8514 | 31.63 | 1.00 | 11 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=50000` | 0.93 | 0.9343 | 14.61 | 1.00 | 11 |
| `shape=bimodal_alpha=0.50_tier=multicentury_heavy_N=2000` | 0.94 | 0.9270 | 14.45 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=10000` | 0.95 | 0.5900 | 24.42 | 1.00 | 4 |
| `shape=bimodal_alpha=0.70_tier=century_heavy_N=2000` | 0.95 | 0.8864 | 10.19 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.95 | 0.9116 | 26.67 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=subcentury_heavy_N=2000` | 0.95 | nan | 0.76 | 1.00 | 192 |
| `shape=bimodal_alpha=0.95_tier=subcentury_heavy_N=10000` | 0.96 | 0.6179 | 24.22 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=subcentury_heavy_N=10000` | 0.96 | 0.8791 | 39.65 | 1.00 | 2 |
| `shape=bimodal_alpha=0.70_tier=empirical_N=2000` | 0.96 | 0.9062 | 10.80 | 1.00 | 0 |
| `shape=bimodal_alpha=0.50_tier=empirical_N=2000` | 0.96 | 0.9462 | 7.76 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=multicentury_heavy_N=50000` | 0.96 | nan | 0.28 | 1.00 | 58 |
| `shape=flat_baseline_alpha=0.05_tier=subcentury_heavy_N=10000` | 0.96 | nan | 0.46 | 1.00 | 128 |
| `shape=smooth_decline_alpha=0.95_tier=uniform_N=2000` | 0.97 | 0.5698 | 57.93 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=50000` | 0.97 | 0.7798 | 23.80 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.97 | 0.8161 | 22.69 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=empirical_N=50000` | 0.97 | 0.8288 | 18.48 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=multicentury_heavy_N=50000` | 0.97 | 0.8367 | 16.19 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=50000` | 0.97 | 0.9499 | 17.24 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=2000` | 0.97 | nan | 0.97 | 1.00 | 269 |
| `shape=flat_baseline_alpha=0.05_tier=subcentury_heavy_N=50000` | 0.97 | nan | 0.20 | 1.00 | 69 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=10000` | 0.97 | nan | 0.37 | 0.99 | 221 |
| `shape=smooth_decline_alpha=0.95_tier=multicentury_heavy_N=2000` | 0.98 | -0.1643 | 63.36 | 1.00 | 9 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=2000` | 0.98 | 0.4981 | 30.46 | 1.00 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=empirical_N=10000` | 0.98 | 0.8074 | 23.09 | 1.00 | 3 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=10000` | 0.98 | 0.8161 | 22.39 | 1.00 | 4 |
| `shape=bimodal_alpha=0.95_tier=subcentury_heavy_N=50000` | 0.98 | 0.8455 | 13.98 | 1.00 | 93 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000` | 0.98 | 0.8950 | 40.94 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=subcentury_heavy_N=10000` | 0.98 | 0.9059 | 42.85 | 1.00 | 3 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=50000` | 0.98 | nan | 0.16 | 1.00 | 42 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=50000` | 0.98 | nan | 0.34 | 0.99 | 756 |
| `shape=flat_baseline_alpha=0.50_tier=multicentury_heavy_N=2000` | 0.98 | nan | 2.16 | 1.00 | 9 |
| `shape=flat_baseline_alpha=0.50_tier=subcentury_heavy_N=10000` | 0.98 | nan | 0.78 | 1.00 | 176 |
| `shape=flat_baseline_alpha=0.50_tier=subcentury_heavy_N=2000` | 0.98 | nan | 1.86 | 1.00 | 5 |
| `shape=flat_baseline_alpha=0.50_tier=subcentury_heavy_N=50000` | 0.98 | nan | 0.30 | 0.99 | 703 |
| `shape=flat_baseline_alpha=0.70_tier=subcentury_heavy_N=50000` | 0.98 | nan | 0.59 | 0.98 | 409 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=2000` | 0.99 | 0.3752 | 22.36 | 1.00 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=empirical_N=2000` | 0.99 | 0.4423 | 31.05 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=subcentury_heavy_N=2000` | 0.99 | 0.5025 | 30.85 | 1.00 | 3 |
| `shape=smooth_decline_alpha=0.95_tier=empirical_N=2000` | 0.99 | 0.5123 | 57.47 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.99 | 0.5605 | 38.59 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=empirical_N=10000` | 0.99 | 0.5706 | 30.51 | 1.00 | 5 |
| `shape=bimodal_alpha=0.95_tier=uniform_N=10000` | 0.99 | 0.5876 | 26.69 | 0.99 | 3 |
| `shape=smooth_decline_alpha=0.95_tier=century_heavy_N=2000` | 0.99 | 0.7852 | 44.42 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=10000` | 0.99 | 0.8056 | 23.64 | 0.99 | 0 |
| `shape=bimodal_alpha=0.70_tier=uniform_N=2000` | 0.99 | 0.9110 | 10.96 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=subcentury_heavy_N=2000` | 0.99 | 0.9172 | 10.09 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=century_heavy_N=50000` | 0.99 | 0.9489 | 17.60 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.05_tier=empirical_N=2000` | 0.99 | nan | 0.56 | 1.00 | 180 |
| `shape=flat_baseline_alpha=0.05_tier=empirical_N=50000` | 0.99 | nan | 0.12 | 1.00 | 50 |
| `shape=flat_baseline_alpha=0.05_tier=multicentury_heavy_N=10000` | 0.99 | nan | 0.39 | 1.00 | 113 |
| `shape=flat_baseline_alpha=0.05_tier=multicentury_heavy_N=2000` | 0.99 | nan | 0.58 | 0.99 | 264 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=50000` | 0.99 | nan | 0.11 | 1.00 | 60 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=10000` | 0.99 | nan | 0.62 | 0.98 | 576 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=2000` | 0.99 | nan | 1.31 | 1.00 | 18 |
| `shape=flat_baseline_alpha=0.30_tier=empirical_N=2000` | 0.99 | nan | 0.84 | 1.00 | 40 |
| `shape=flat_baseline_alpha=0.30_tier=empirical_N=50000` | 0.99 | nan | 0.26 | 1.00 | 259 |
| `shape=flat_baseline_alpha=0.30_tier=multicentury_heavy_N=10000` | 0.99 | nan | 0.68 | 1.00 | 111 |
| `shape=flat_baseline_alpha=0.30_tier=multicentury_heavy_N=2000` | 0.99 | nan | 1.95 | 1.00 | 21 |
| `shape=flat_baseline_alpha=0.30_tier=subcentury_heavy_N=10000` | 0.99 | nan | 0.55 | 0.99 | 698 |
| `shape=flat_baseline_alpha=0.30_tier=subcentury_heavy_N=2000` | 0.99 | nan | 1.52 | 1.00 | 41 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=2000` | 0.99 | nan | 0.85 | 1.00 | 38 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=10000` | 0.99 | nan | 1.09 | 1.00 | 319 |
| `shape=flat_baseline_alpha=0.50_tier=century_heavy_N=2000` | 0.99 | nan | 2.78 | 1.00 | 5 |
| `shape=flat_baseline_alpha=0.50_tier=multicentury_heavy_N=10000` | 0.99 | nan | 0.95 | 0.99 | 193 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=2000` | 0.99 | nan | 1.29 | 1.00 | 13 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=10000` | 0.99 | nan | 1.53 | 0.97 | 460 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=50000` | 0.99 | nan | 0.46 | 0.99 | 610 |
| `shape=flat_baseline_alpha=0.70_tier=empirical_N=10000` | 0.99 | nan | 1.13 | 1.00 | 79 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=2000` | 0.99 | nan | 13.09 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=multicentury_heavy_N=10000` | 0.99 | nan | 5.08 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=multicentury_heavy_N=2000` | 0.99 | nan | 17.37 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=subcentury_heavy_N=10000` | 0.99 | nan | 8.09 | 1.00 | 1 |
| `shape=bimodal_alpha=0.95_tier=multicentury_heavy_N=2000` | 1.00 | 0.2834 | 40.24 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=multicentury_heavy_N=2000` | 1.00 | 0.3362 | 38.01 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=empirical_N=2000` | 1.00 | 0.3964 | 25.16 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=uniform_N=2000` | 1.00 | 0.4040 | 35.18 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=subcentury_heavy_N=2000` | 1.00 | 0.4077 | 22.60 | 1.00 | 0 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=2000` | 1.00 | 0.4202 | 21.87 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=multicentury_heavy_N=2000` | 1.00 | 0.5659 | 45.24 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=subcentury_heavy_N=2000` | 1.00 | 0.6057 | 43.70 | 1.00 | 2 |
| `shape=smooth_growth_alpha=0.95_tier=century_heavy_N=2000` | 1.00 | 0.6067 | 50.11 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=uniform_N=2000` | 1.00 | 0.6207 | 43.57 | 1.00 | 2 |
| `shape=rise_and_fall_alpha=0.95_tier=empirical_N=2000` | 1.00 | 0.6875 | 41.93 | 1.00 | 0 |
| `shape=rise_and_fall_alpha=0.95_tier=century_heavy_N=2000` | 1.00 | 0.7414 | 39.90 | 1.00 | 3 |
| `shape=smooth_growth_alpha=0.95_tier=subcentury_heavy_N=2000` | 1.00 | 0.7965 | 46.15 | 1.00 | 1 |
| `shape=bimodal_alpha=0.95_tier=century_heavy_N=50000` | 1.00 | 0.8379 | 16.15 | 1.00 | 0 |
| `shape=smooth_decline_alpha=0.95_tier=subcentury_heavy_N=2000` | 1.00 | 0.8391 | 38.74 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=empirical_N=2000` | 1.00 | 0.8457 | 37.26 | 1.00 | 1 |
| `shape=regnal_cluster_alpha=0.95_tier=subcentury_heavy_N=10000` | 1.00 | 0.8469 | 21.73 | 1.00 | 0 |
| `shape=bimodal_alpha=0.70_tier=multicentury_heavy_N=2000` | 1.00 | 0.8514 | 21.04 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=uniform_N=2000` | 1.00 | 0.8591 | 38.92 | 1.00 | 0 |
| `shape=smooth_growth_alpha=0.95_tier=multicentury_heavy_N=2000` | 1.00 | 0.8665 | 25.96 | 1.00 | 0 |
| `shape=regnal_cluster_alpha=0.95_tier=empirical_N=50000` | 1.00 | 0.9464 | 19.83 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.05_tier=century_heavy_N=10000` | 1.00 | nan | 0.31 | 1.00 | 132 |
| `shape=flat_baseline_alpha=0.05_tier=empirical_N=10000` | 1.00 | nan | 0.30 | 1.00 | 106 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=10000` | 1.00 | nan | 0.27 | 1.00 | 218 |
| `shape=flat_baseline_alpha=0.05_tier=uniform_N=2000` | 1.00 | nan | 0.70 | 1.00 | 179 |
| `shape=flat_baseline_alpha=0.30_tier=century_heavy_N=50000` | 1.00 | nan | 0.35 | 1.00 | 300 |
| `shape=flat_baseline_alpha=0.30_tier=empirical_N=10000` | 1.00 | nan | 0.40 | 1.00 | 145 |
| `shape=flat_baseline_alpha=0.30_tier=multicentury_heavy_N=50000` | 1.00 | nan | 0.21 | 1.00 | 135 |
| `shape=flat_baseline_alpha=0.30_tier=subcentury_heavy_N=50000` | 1.00 | nan | 0.19 | 1.00 | 98 |
| `shape=flat_baseline_alpha=0.30_tier=uniform_N=50000` | 1.00 | nan | 0.21 | 1.00 | 130 |
| `shape=flat_baseline_alpha=0.50_tier=empirical_N=10000` | 1.00 | nan | 0.74 | 0.99 | 322 |
| `shape=flat_baseline_alpha=0.50_tier=empirical_N=2000` | 1.00 | nan | 1.57 | 1.00 | 4 |
| `shape=flat_baseline_alpha=0.50_tier=empirical_N=50000` | 1.00 | nan | 0.53 | 1.00 | 769 |
| `shape=flat_baseline_alpha=0.50_tier=multicentury_heavy_N=50000` | 1.00 | nan | 0.28 | 1.00 | 90 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=10000` | 1.00 | nan | 0.57 | 1.00 | 217 |
| `shape=flat_baseline_alpha=0.50_tier=uniform_N=50000` | 1.00 | nan | 0.36 | 0.99 | 413 |
| `shape=flat_baseline_alpha=0.70_tier=century_heavy_N=2000` | 1.00 | nan | 5.92 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.70_tier=empirical_N=2000` | 1.00 | nan | 1.78 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.70_tier=empirical_N=50000` | 1.00 | nan | 0.71 | 0.99 | 1265 |
| `shape=flat_baseline_alpha=0.70_tier=multicentury_heavy_N=10000` | 1.00 | nan | 1.46 | 1.00 | 31 |
| `shape=flat_baseline_alpha=0.70_tier=multicentury_heavy_N=2000` | 1.00 | nan | 2.51 | 1.00 | 3 |
| `shape=flat_baseline_alpha=0.70_tier=multicentury_heavy_N=50000` | 1.00 | nan | 0.61 | 1.00 | 149 |
| `shape=flat_baseline_alpha=0.70_tier=subcentury_heavy_N=10000` | 1.00 | nan | 1.20 | 1.00 | 46 |
| `shape=flat_baseline_alpha=0.70_tier=subcentury_heavy_N=2000` | 1.00 | nan | 3.09 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=10000` | 1.00 | nan | 1.07 | 1.00 | 133 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=2000` | 1.00 | nan | 1.84 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.70_tier=uniform_N=50000` | 1.00 | nan | 0.53 | 0.99 | 742 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=10000` | 1.00 | nan | 5.81 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=century_heavy_N=50000` | 1.00 | nan | 2.76 | 1.00 | 15 |
| `shape=flat_baseline_alpha=0.95_tier=empirical_N=10000` | 1.00 | nan | 7.06 | 1.00 | 3 |
| `shape=flat_baseline_alpha=0.95_tier=empirical_N=2000` | 1.00 | nan | 11.19 | 1.00 | 1 |
| `shape=flat_baseline_alpha=0.95_tier=empirical_N=50000` | 1.00 | nan | 2.95 | 1.00 | 18 |
| `shape=flat_baseline_alpha=0.95_tier=multicentury_heavy_N=50000` | 1.00 | nan | 3.09 | 1.00 | 8 |
| `shape=flat_baseline_alpha=0.95_tier=subcentury_heavy_N=2000` | 1.00 | nan | 13.71 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=subcentury_heavy_N=50000` | 1.00 | nan | 4.05 | 0.99 | 6 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=10000` | 1.00 | nan | 4.59 | 0.99 | 4 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=2000` | 1.00 | nan | 10.73 | 1.00 | 0 |
| `shape=flat_baseline_alpha=0.95_tier=uniform_N=50000` | 1.00 | nan | 3.69 | 1.00 | 14 |

## 4. Diagnostics

- Mean fit-seconds per replicate: 33.26
- Min cell-level convergence pass rate: 84.00%
- Cells with any divergences: 144/450

## 5. Wasserstein-1 supplementary

Wasserstein-1 is reported per cell as a distribution-sensitive shape metric (prereg §4 line 334). Its flagging threshold remains deferred (spec.md §5; needs empirical posteriors to anchor) and is NOT part of the binding rule.

- Median across cells: 5.83
- 90th percentile across cells: 26.71
