# Small-N deconvolution-reachability — REPORT

Minimum subset size N at which **subset-specific** Bayesian deconvolution recovers the genuine SPA under the Decision-33 criterion (convergence ≥ 90 % AND Pearson r ≥ 0.95 in ≥ 90 % of replicates). See `spec.md` and Decision 34.

## 1. Reachability floor (smallest passing N)

| shape | α | floor (min passing N) |
|---|---|---|
| regnal_cluster | 0.30 | N ≥ 1000 |
| regnal_cluster | 0.50 | N ≥ 1000 |
| regnal_cluster | 0.70 | UNREACHED in tested range |
| regnal_cluster | 0.85 | UNREACHED in tested range |
| rise_and_fall | 0.30 | N ≥ 500 |
| rise_and_fall | 0.50 | N ≥ 1000 |
| rise_and_fall | 0.70 | N ≥ 2000 |
| rise_and_fall | 0.85 | UNREACHED in tested range |
| smooth_growth | 0.30 | N ≥ 500 |
| smooth_growth | 0.50 | N ≥ 2000 |
| smooth_growth | 0.70 | UNREACHED in tested range |
| smooth_growth | 0.85 | UNREACHED in tested range |

## 2. Headline

- Within the operating envelope (α ≤ 0.70), subset-specific de-fogging is reliable for **N ≥ 2000** across the tested shapes (the worst-case floor).
- Unreached even at the largest tested N within the envelope: [('regnal_cluster', 0.7), ('smooth_growth', 0.7)] — these need a larger N or the pooled-convention fall-back.
- The high-α stress row (α = 0.85, late-corpus regime) is reported separately; its floors are expected higher / unreached.

## 3. Diagnostics by N (α ≤ 0.70 cells)

| N | mean shape-rate | mean conv-rate | mean band cov95 | mean |α-bias| |
|---|---|---|---|---|
| 50 | 12% | 100% | 0.98 | 0.155 |
| 100 | 16% | 100% | 0.98 | 0.135 |
| 200 | 32% | 100% | 0.97 | 0.131 |
| 350 | 51% | 100% | 0.96 | 0.132 |
| 500 | 61% | 99% | 0.94 | 0.140 |
| 1000 | 80% | 99% | 0.91 | 0.134 |
| 2000 | 94% | 100% | 0.88 | 0.133 |

Band coverage (target 0.95) and α-bias are diagnostics, not gates; they show how recovery quality scales with N.

## 4. Caveats

- Convention pattern = `pilot_proxy` (the realistic descriptive proxy); a `uniform` robustness pass is optional.
- Fits run under zbook's pymc 6.x; the grid used pymc 5.28 (model identical — a calibration property, transfers).
- Below the floor: pooled-convention borrow / §5 hierarchical model / descriptive reporting (Decision 34; out of scope here).
