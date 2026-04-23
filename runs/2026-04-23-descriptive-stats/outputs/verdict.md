# Verification verdict: **PARTIAL**

Claims reviewed: 1330 (claims.jsonl contains 1305; plus spot-check / method-check entries).
- pass: 1303
- fail: 27
- skip: 0

Severity tally (failures only):
- critical: 0
- major: 27
- minor: 0

## Verifier random seed

The verifier used seed `21260423` (proposer used 20260423). Stochastic
claims (permutation_pvalue, corrected_pvalue, ci_lower, ci_upper) were re-run
with the different seed and compared under the stochastic tolerance
(+-1 pp on p-values, +-5% relative on CI bounds).

## Method-as-implemented

- method-check::aoristic_weight_formulation --- pass (info); Weight = 1/date_range inside interval, 0 outside (searched for `1.0 / dr` and `(nb <= y) & (y <= na)`).
- method-check::aoristic_expected_sigma_weights --- pass (info); Expected count at Y = sum of per-row weights (searched for `weights.sum()` inside aoristic_expected_year_counts).
- method-check::aoristic_null_resample_uniform_mid --- pass (info); Null resampling draws mid ~ DiscreteUniform(nb, na) per row per resample.
- method-check::no_chi_square_vs_uniform_null --- pass (info); profile.py does not use scipy chi-square on uniform as the permutation null (checked for stats.chisquare / chi2_contingency).
- method-check::westfall_young_joint_not_marginal --- pass (info); WY stepdown uses joint null distribution (cumulative max across tail of nulls, not marginal p-values).
- method-check::holm_bonferroni_companion --- pass (info); Holm-Bonferroni companion correction implemented.
- method-check::decisions_entry_midpoint_inflation --- pass (info); decisions.md has an assumption-check entry for inferential claim family `midpoint_inflation`.
- method-check::decisions_entry_editorial_spikes --- pass (info); decisions.md has an assumption-check entry for inferential claim family `editorial_spikes`.
- method-check::decisions_entry_drill_down --- pass (info); decisions.md has an assumption-check entry for inferential claim family `drill_down`.
- method-check::decisions_entry_aoristic_null --- pass (info); decisions.md has an assumption-check entry for inferential claim family `aoristic_null`.
- method-check::decisions_entry_BCa_bootstrap --- pass (info); decisions.md has an assumption-check entry for inferential claim family `BCa_bootstrap`.

## Interpretive flags for investigator

- The Westfall-Young-adjusted p on `editorial-spikes` `not_after` family
  is 0.6488 (marginal), because the AD 235 spike absorbs correction mass in the
  joint-null distribution. Holm-adjusted p remains small for individual years
  (e.g. AD 212 Holm-p = 0.00035). This is a genuine WY vs Holm trade-off and
  warrants investigator discussion: WY controls FWER under joint null and is
  appropriate for inflation-style null-distribution comparisons; Holm is
  marginal and cheaper but does not condition on the joint distribution. For
  the `not_after` family in particular, the scout's honest self-critique
  stands.

