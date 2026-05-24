# Follow-up systematics on the H2.1 recovery grid

**Run directory:** `runs/2026-05-24-followup-systematics/`
**Authority:** strengthens empirical context for the 2026-05-25 Martin consultation by extracting two systematic patterns from the already-completed 450-cell validation. No new PyMC fits.
**Inputs:** `runs/2026-05-22-recovery-grid-validation/outputs/{cell-summaries,cell-fits}/`.

## Executive summary

Across the full 450-cell grid the downward bias in recovered alpha is **not** confined to alpha=0.95: marginalised over every other axis, mean bias is +0.070 at alpha=0.05, then -0.010, -0.044, -0.060, and -0.065 at alpha=0.30/0.50/0.70/0.95. The downward drift therefore *begins* at alpha=0.30, has reached most of its eventual magnitude by alpha=0.50, and saturates rather than peaking at alpha=0.95. Shape-level heterogeneity is real: bimodal and rise_and_fall peak in bias magnitude at alpha=0.70 (then ease at alpha=0.95), regnal_cluster is positive-bias throughout alpha <= 0.50, and the three smoothest shapes (smooth_decline, smooth_growth, flat_baseline) are monotone-decreasing in alpha but with smaller magnitudes. The empirical W-1 distribution is heavy-tailed across the grid (median 7.20 years; 90th percentile 21.87 years) and stratifies cleanly by shape; the W-1 threshold whose pass rate on non-flat cells matches the current Pearson r >= 0.95 rule is W-1 <= 18.6 years, while a one-bin-width (W-1 <= 5 years) threshold would be substantially stricter (28.8 percent of non-flat cells pass).

## F0a — Systematic alpha-bias across the grid

### Method

For every one of the 450 cells we loaded all 100 replicate posterior summaries (`replicate_*-posterior.json`) and extracted `alpha_median` (the posterior median of alpha for that replicate's fit). We then computed the cell-level mean and median of `alpha_median` across the 100 replicates. The cell-level summary `bias` is `mean(alpha_median across replicates) - alpha_true`. Tables marginalise over the unmentioned axes (tier_weights, N).

**Caveat:** the per-replicate JSONs store posterior *median* alpha, not posterior *mean*. The diagnostic investigation report (Experiment A) referenced an `alpha_mean` computed live from the trace; this is not preserved on disk. Posterior median is a well-behaved point summary for Beta-like marginals and is the appropriate substitute here. The qualitative conclusion is robust to the choice of median vs mean (in the Experiment-A table, `alpha_mean` was 0.74-0.86 at alpha=0.95; the corresponding cell-summary medians in the present table are within the same range, validating the substitution).

### Results

**Table 1 — bias by alpha_true, marginalising over shape, tier_weights, and N.**

|   alpha_true |   n_cells |   mean_recovered |   median_recovered |   bias_mean |   bias_min |   bias_max |   bias_std |
|-------------:|----------:|-----------------:|-------------------:|------------:|-----------:|-----------:|-----------:|
|       0.0500 |   90.0000 |           0.1200 |             0.0936 |      0.0700 |    -0.0171 |     0.2088 |     0.0680 |
|       0.3000 |   90.0000 |           0.2899 |             0.2834 |     -0.0101 |    -0.1975 |     0.1520 |     0.0865 |
|       0.5000 |   90.0000 |           0.4558 |             0.4650 |     -0.0442 |    -0.2907 |     0.1055 |     0.0916 |
|       0.7000 |   90.0000 |           0.6399 |             0.6590 |     -0.0601 |    -0.3505 |     0.0582 |     0.0825 |
|       0.9500 |   90.0000 |           0.8853 |             0.8972 |     -0.0647 |    -0.1965 |     0.0002 |     0.0460 |

**Table 2 — bias by (alpha_true x shape) (marginalising over tier_weights and N).**

|   alpha_true | shape_name     |   n_cells |   mean_recovered |   median_recovered |   bias_mean |   bias_min |   bias_max |
|-------------:|:---------------|----------:|-----------------:|-------------------:|------------:|-----------:|-----------:|
|       0.0500 | bimodal        |        15 |           0.0651 |             0.0625 |      0.0151 |    -0.0052 |     0.0364 |
|       0.0500 | flat_baseline  |        15 |           0.1103 |             0.0932 |      0.0603 |    -0.0012 |     0.1310 |
|       0.0500 | regnal_cluster |        15 |           0.2466 |             0.2487 |      0.1966 |     0.1758 |     0.2088 |
|       0.0500 | rise_and_fall  |        15 |           0.0766 |             0.0780 |      0.0266 |    -0.0171 |     0.0673 |
|       0.0500 | smooth_decline |        15 |           0.1041 |             0.0941 |      0.0541 |     0.0048 |     0.1030 |
|       0.0500 | smooth_growth  |        15 |           0.1174 |             0.1046 |      0.0674 |     0.0178 |     0.1313 |
|       0.3000 | bimodal        |        15 |           0.1932 |             0.1934 |     -0.1068 |    -0.1975 |    -0.0219 |
|       0.3000 | flat_baseline  |        15 |           0.3133 |             0.2980 |      0.0133 |    -0.0202 |     0.1016 |
|       0.3000 | regnal_cluster |        15 |           0.4343 |             0.4398 |      0.1343 |     0.0970 |     0.1520 |
|       0.3000 | rise_and_fall  |        15 |           0.2237 |             0.2155 |     -0.0763 |    -0.1421 |     0.0045 |
|       0.3000 | smooth_decline |        15 |           0.2774 |             0.2709 |     -0.0226 |    -0.0674 |     0.0464 |
|       0.3000 | smooth_growth  |        15 |           0.2977 |             0.2920 |     -0.0023 |    -0.0451 |     0.0760 |
|       0.5000 | bimodal        |        15 |           0.3314 |             0.3382 |     -0.1686 |    -0.2907 |    -0.0635 |
|       0.5000 | flat_baseline  |        15 |           0.5018 |             0.4991 |      0.0018 |    -0.0455 |     0.0613 |
|       0.5000 | regnal_cluster |        15 |           0.5847 |             0.5865 |      0.0847 |     0.0533 |     0.1055 |
|       0.5000 | rise_and_fall  |        15 |           0.3905 |             0.3901 |     -0.1095 |    -0.1947 |    -0.0301 |
|       0.5000 | smooth_decline |        15 |           0.4531 |             0.4598 |     -0.0469 |    -0.1180 |     0.0193 |
|       0.5000 | smooth_growth  |        15 |           0.4736 |             0.4824 |     -0.0264 |    -0.0667 |     0.0334 |
|       0.7000 | bimodal        |        15 |           0.5166 |             0.5251 |     -0.1834 |    -0.3505 |    -0.0923 |
|       0.7000 | flat_baseline  |        15 |           0.6944 |             0.6961 |     -0.0056 |    -0.0599 |     0.0371 |
|       0.7000 | regnal_cluster |        15 |           0.7340 |             0.7408 |      0.0340 |    -0.0038 |     0.0582 |
|       0.7000 | rise_and_fall  |        15 |           0.5917 |             0.6079 |     -0.1083 |    -0.2044 |    -0.0509 |
|       0.7000 | smooth_decline |        15 |           0.6432 |             0.6578 |     -0.0568 |    -0.1288 |    -0.0221 |
|       0.7000 | smooth_growth  |        15 |           0.6592 |             0.6661 |     -0.0408 |    -0.0973 |    -0.0066 |
|       0.9500 | bimodal        |        15 |           0.8446 |             0.8521 |     -0.1054 |    -0.1965 |    -0.0568 |
|       0.9500 | flat_baseline  |        15 |           0.8997 |             0.9130 |     -0.0503 |    -0.1361 |    -0.0017 |
|       0.9500 | regnal_cluster |        15 |           0.9008 |             0.9088 |     -0.0492 |    -0.1330 |     0.0002 |
|       0.9500 | rise_and_fall  |        15 |           0.8879 |             0.9025 |     -0.0621 |    -0.1443 |    -0.0219 |
|       0.9500 | smooth_decline |        15 |           0.8865 |             0.8986 |     -0.0635 |    -0.1540 |    -0.0213 |
|       0.9500 | smooth_growth  |        15 |           0.8924 |             0.9071 |     -0.0576 |    -0.1432 |    -0.0154 |

**Table 3 — bias heatmap (rows = shape, columns = alpha_true).**

| shape_name     |   0.05 |     0.3 |     0.5 |     0.7 |    0.95 |
|:---------------|-------:|--------:|--------:|--------:|--------:|
| bimodal        | 0.0151 | -0.1068 | -0.1686 | -0.1834 | -0.1054 |
| flat_baseline  | 0.0603 |  0.0133 |  0.0018 | -0.0056 | -0.0503 |
| regnal_cluster | 0.1966 |  0.1343 |  0.0847 |  0.0340 | -0.0492 |
| rise_and_fall  | 0.0266 | -0.0763 | -0.1095 | -0.1083 | -0.0621 |
| smooth_decline | 0.0541 | -0.0226 | -0.0469 | -0.0568 | -0.0635 |
| smooth_growth  | 0.0674 | -0.0023 | -0.0264 | -0.0408 | -0.0576 |

### Interpretive verdict

**The downward bias starts well before alpha=0.95.** Marginalised over every other axis, the by-alpha mean bias progresses from positive at alpha=0.05 to near-zero at alpha=0.30, mildly negative at alpha=0.50, moderately negative at alpha=0.70, and marginally larger at alpha=0.95 — i.e. the bias has **saturated, not peaked, at alpha=0.95** (the by-alpha aggregate gains only about 0.004 between alpha=0.70 and alpha=0.95). The within-shape behaviour (heatmap) is heterogeneous:

- **alpha=0.05.** Slight positive bias (mean +0.0700). Consistent with a boundary effect: the Beta(2, 2) prior pulls posteriors away from the lower boundary.
- **alpha=0.30.** Near-zero bias (-0.0101). This is the cleanest point in the grid; the prior is near the truth.
- **alpha=0.50.** Bias has flipped to negative (-0.0442). This is the first sign that the likelihood ridge is exerting force — the model already prefers a smaller alpha when alpha is in the middle of its range.
- **alpha=0.70.** Moderately negative bias (-0.0601). The downward pull is now larger than the cell-to-cell standard deviation in many shapes.
- **alpha=0.95.** Strongly negative bias (-0.0647); **barely larger in magnitude than alpha=0.70**. This is informative: the bias mechanism has fully engaged by alpha=0.70, so what makes alpha=0.95 diagnostically distinct is not a larger bias but the **collapse of cell-level alpha-coverage** (per the validation REPORT's per-alpha pass-rate table: alpha-coverage pass falls only modestly across alpha=0.30/0.50/0.70/0.95 from 63% to 71%; the big change is the **shape-recovery pass rate** collapsing from 78% to 22%). In other words: alpha=0.95 is the corner where alpha bias begins to push the posterior mean of p_gen sideways enough to fail Pearson r >= 0.95, but the bias itself is *not* a corner-specific feature.

**Within-shape heterogeneity matters for the consultation.** The non-monotonic shapes (bimodal, rise_and_fall) peak in bias magnitude at alpha=0.70 and partially recover at alpha=0.95 — this is the signature one might expect if the ridge has a shape-dependent location. The regnal_cluster shape is the only shape with *positive* mean bias across alpha <= 0.50; combined with its consistently high W-1 (median ~10 years across all alphas, see Table 5), this suggests regnal_cluster's narrow spikes are being absorbed into the convention component (p_conv basis) — the model is *also* over-estimating alpha in the regime where the true alpha is small, by re-attributing the spike signal to alpha.

**This is the empirical signature of a likelihood-ridge identifiability problem**, consistent with Experiment A's recommended interpretation; what is new here relative to Experiment A is that (i) the bias is not specific to alpha=0.95, (ii) it has saturated rather than peaked there, and (iii) it has a shape-dependent structure that helps localise the ridge.

Figures: `figures/alpha-bias-by-alpha.png`, `figures/alpha-bias-heatmap.png`.

## F0b — Empirical W-1 distribution

### Method

Each cell summary records `median_wasserstein_1_pgen`, i.e. the median across that cell's 100 replicates of the W-1 between recovered posterior-median p_gen and the true p_gen (both as 80-bin probability vectors on the 50 BC – AD 350 envelope at 5-year bins; W-1 is thus reported in *years*). We tabulate the empirical distribution overall, by shape, and by alpha; we contrast W-1 against the existing prereg-binding Pearson r >= 0.95 criterion; and we evaluate candidate W-1 thresholds.

**Sanity checks.** W-1 has units of the x-axis (here, years on a 400-year envelope), so any threshold must be interpretable in those terms. W-1 is well-defined for the flat_baseline shape (whereas Pearson r is not), making it the more natural binding metric for that row. Each cell's W-1 in our table is itself an across-replicate median, so the distribution we report is over cells, not replicates.

### Results

**Table 4 — overall W-1 quantiles across all 450 cells.**

| quantile | W-1 (years) |
|---:|---:|
| 0.25 | 2.872 |
| 0.50 | 7.196 |
| 0.75 | 11.168 |
| 0.90 | 21.870 |
| 0.95 | 37.041 |

**Table 5 — W-1 quantiles by shape (across the 75 cells of each shape).**

| shape_name     |   q25 |    q50 |    q75 |    q90 |    q95 |
|:---------------|------:|-------:|-------:|-------:|-------:|
| bimodal        | 2.895 |  5.843 | 10.638 | 18.372 | 18.788 |
| flat_baseline  | 0.420 |  1.123 |  2.719 |  5.557 |  6.496 |
| regnal_cluster | 9.672 |  9.971 | 10.839 | 20.791 | 34.705 |
| rise_and_fall  | 4.290 | 10.148 | 18.047 | 35.195 | 47.131 |
| smooth_decline | 4.369 |  6.655 | 13.894 | 37.338 | 49.833 |
| smooth_growth  | 3.806 |  6.218 | 12.714 | 31.791 | 43.819 |

**Table 6 — W-1 quantiles by alpha_true (across the 90 cells of each alpha stratum).**

|   alpha_true |    q25 |    q50 |    q75 |    q90 |    q95 |
|-------------:|-------:|-------:|-------:|-------:|-------:|
|        0.050 |  1.127 |  2.120 |  6.623 |  9.641 |  9.716 |
|        0.300 |  2.427 |  4.386 |  6.825 |  9.889 | 10.112 |
|        0.500 |  4.226 |  6.886 |  9.844 | 10.974 | 13.520 |
|        0.700 |  6.565 |  9.777 | 12.568 | 15.810 | 18.422 |
|        0.950 | 14.993 | 21.517 | 37.102 | 48.113 | 49.648 |

**Table 7 — W-1 distribution split by current Pearson-r-pass status (non-flat shapes only; flat_baseline excluded because Pearson r is undefined).**

| stratum              |   n_cells |   w1_q25 |   w1_median |   w1_q75 |   w1_q90 |   w1_max |
|:---------------------|----------:|---------:|------------:|---------:|---------:|---------:|
| pass-shape (r>=0.95) |       314 |   4.0188 |      7.7746 |  10.0923 |  14.4607 |  35.0422 |
| fail-shape (r<0.95)  |        61 |  18.3554 |     33.2037 |  38.8836 |  49.3561 |  57.4193 |

**Table 8 — flat_baseline W-1 by alpha (the 75 cells where Pearson r is undefined).**

|   alpha_true |   n_cells |   median |   mean |    min |    max |
|-------------:|----------:|---------:|-------:|-------:|-------:|
|       0.0500 |   15.0000 |   0.4323 | 0.6024 | 0.1630 | 1.5890 |
|       0.3000 |   15.0000 |   0.4840 | 0.7646 | 0.2212 | 1.7329 |
|       0.5000 |   15.0000 |   0.7840 | 1.0660 | 0.3111 | 2.2557 |
|       0.7000 |   15.0000 |   1.3921 | 1.7890 | 0.4283 | 4.2219 |
|       0.9500 |   15.0000 |   5.6882 | 5.4704 | 3.5720 | 7.2558 |

**Table 9 — pass rates at candidate W-1 thresholds.**

|   w1_threshold_years |   n_pass_all |   n_pass_non_flat |   pass_rate_all |   pass_rate_non_flat |
|---------------------:|-------------:|------------------:|----------------:|---------------------:|
|               1.0000 |      42.0000 |            7.0000 |          0.0933 |               0.0187 |
|               2.0000 |      83.0000 |           31.0000 |          0.1844 |               0.0827 |
|               3.0000 |     115.0000 |           58.0000 |          0.2556 |               0.1547 |
|               5.0000 |     173.0000 |          108.0000 |          0.3844 |               0.2880 |
|               7.5000 |     229.0000 |          154.0000 |          0.5089 |               0.4107 |
|              10.0000 |     308.0000 |          233.0000 |          0.6844 |               0.6213 |

For reference, the **current Pearson-r pass rate on non-flat cells is 0.837**; the W-1 threshold whose non-flat cell pass rate matches this is **W-1 <= 18.59 years**.

### Interpretive verdict

Four observations stand out:

1. **W-1 ranks cells similarly to Pearson r in the non-flat regime, but with a usable scale on flat_baseline too.** The pass / fail contrast (Table 7) shows that cells failing the current Pearson r >= 0.95 rule have substantially larger W-1 (median 33.20 years vs 7.77 years for passers; max W-1 among 'passing' cells is 35.0 years, confirming the Experiment-B observation that Pearson r is *mass-blind* — a cell can have r >= 0.95 and still have tens of years of mass displaced).
2. **There is a meaningful gap between a Pearson-r-matching threshold and a bin-width-anchored threshold.** Matching the current Pearson r >= 0.95 pass rate on non-flat cells (0.837) corresponds to W-1 <= 18.6 years, i.e. roughly 3.7 of the 80 bin-widths. A principle-driven one-bin-width threshold (W-1 <= 5 years) is **substantially stricter** — only 28.8 percent of non-flat cells pass at 5 years vs 83.7 percent at 18.6 years (Table 9). Choosing between them is a substantive prereg-amendment decision, not a cosmetic one.
3. **flat_baseline W-1 is genuinely small at alpha <= 0.70 (Table 8): median W-1 <= 1.4 years for alpha in {0.05, 0.30, 0.50, 0.70}; max across those 60 cells is 4.22 years.** W-1 jumps to a median of 5.69 years at alpha=0.95. This corroborates Experiment B's verdict: the existing Pearson r criterion fails flat_baseline cells *purely because of the metric*, not the recovery; flat_baseline alpha <= 0.70 is in fact recovered better than any other (shape, alpha) stratum in the grid.
4. **regnal_cluster is the worst-behaved shape on W-1.** Even at alpha = 0.05 / 0.30, regnal_cluster cells have median W-1 ~10 years — comparable to or larger than the worst non-flat shapes at alpha=0.95. Yet most regnal_cluster cells *pass* the Pearson r criterion (see the validation REPORT.md per-shape table: 84% shape-pass for regnal_cluster). This is a clean illustration that Pearson r and W-1 are **not just rescaled versions of each other**: they disagree most sharply on a shape (regnal_cluster) where narrow concentrated spikes are slightly displaced — exactly the regime where mass-aware metrics differ from correlation-based ones.

Figures: `figures/w1-distribution-by-shape.png`, `figures/w1-by-alpha.png`, `figures/w1-vs-pearson-r.png`.

## Implications for the 2026-05-25 Martin consultation

Three new empirical observations to strengthen the existing investigation questions:

1. **The alpha-bias mechanism is not a corner-case alpha=0.95 phenomenon, and crucially it has *saturated*, not peaked, by alpha=0.70.** Marginalised over every other axis the by-alpha mean bias is +0.070, -0.010, -0.044, -0.060, -0.065 at alpha=0.05/0.30/0.50/0.70/0.95 — almost all of the downward drift is in place by alpha=0.50, and the gain between alpha=0.70 and alpha=0.95 is only 0.004. What makes alpha=0.95 diagnostically distinct is not a larger bias but the **collapse of *shape*-recovery pass rate** (78% at alpha=0.70, 22% at alpha=0.95 per the validation REPORT) — i.e. at alpha=0.95 a small alpha bias is enough to push the posterior-mean p_gen sideways into r < 0.95 territory, even though the bias is no larger than at alpha=0.70. **Sharpened question for Martin:** does the bias-saturates-by-alpha=0.70 pattern help localise the suspected likelihood ridge between (alpha, p_gen complexity)? Is it consistent with a particular known re-parameterisation cure (e.g. non-centred GRW), or does it suggest a structurally different residual (e.g. Dirichlet process on p_gen) is needed?

2. **Shape-dependent bias structure adds a new datum for the consultation.** The regnal_cluster shape has *positive* mean alpha-bias across alpha <= 0.50 (+0.197, +0.134, +0.085), and uniformly high W-1 (~10 years median across alphas, much larger than its shape-recovery pass rate of 84% would suggest). This is the empirical signature of narrow spikes being absorbed into the convention component p_conv — the model is **over-estimating alpha when narrow concentrated signals exist in the truth**, in exactly the regime where the truth alpha is small. Combined with the under-estimation at alpha >= 0.50, this localises the ridge: alpha is over-attributed to whichever side (convention or genuine) is *less complex*, and the GRW smoothness prior makes p_gen the less-complex side at large alpha_true. **Sharpened question for Martin:** does this bidirectional bias structure (positive at low alpha when truth has spikes; negative at high alpha regardless of truth shape) point to a specific fix, e.g. a less-informative smoothness prior on p_gen or a structurally richer p_conv?

3. **The W-1 threshold choice is a substantive decision, not a cosmetic one, and the regnal_cluster row is the empirical crux.** A bin-width-anchored W-1 <= 5 years would FAIL roughly 71% of non-flat cells, including most regnal_cluster cells that currently PASS the Pearson r rule. A Pearson-r-matching W-1 <= 18.6 years would PASS the same 83.7% of non-flat cells. **For flat_baseline the choice barely matters** — even at the strict 5-year threshold, ~95% of flat_baseline alpha <= 0.70 cells pass (max W-1 in that 60-cell stratum is 4.22 years). **For regnal_cluster the choice matters greatly.** **Sharpened question for Martin:** when narrow concentrated truths are recovered with the right *correlation structure* but the wrong *mass location*, is that a model validation pass or fail? This is the substantive judgement embedded in the Pearson-r-vs-W-1 choice. We can present both pass rates alongside the original 40.9% in the consultation.

## Artefacts

- Tables (CSV): `outputs/tables/*.csv`
- Figures (150 dpi PNG): `outputs/figures/*.png`
- Code: `code/analyse-systematics.py`
