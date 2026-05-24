# Stage 2 — Empirical p_gen prior from Cohort B

**Run directory:** `runs/2026-05-24-empirical-pgen-prior/`
**Date:** 2026-05-24
**Authority:** Stage 2 of the empirical-Bayes calibration-cohort
implementation plan. Constructs the informative prior on the genuine-
activity component (p_gen) of the H2.1 mixture model from Cohort B
(Tight ∪ F2_Other, 31,841 records). Together with Stage 1's
empirical p_conv, this provides the two data-derived building blocks
the modified mixture model (Stage 3) will consume.
**Companion:** `runs/2026-05-24-empirical-pconv/outputs/REPORT.md`
(Stage 1) and `runs/2026-05-24-type-stratified-narrow-spas/outputs/
REPORT.md` (cohort definition).

## 1. Headline

**Cohort B (n = 31,841) gives a well-constrained empirical prior on
p_gen across the entire 50 BC – AD 350 envelope.** All 80 5-year
bins have ≥ 50 inscriptions overlapping; most bins have 500-3,000.
The type-reweighting up-weights epitaphs by 3.2 × (5,612 → 17,789
effective records) and down-weights honorific by 0.28 × (4,076 →
1,158 effective). The bootstrap-derived sigma_prior on log p_gen has
median 0.044 across well-covered bins — a moderately-informative
prior that should be strong enough to break the identifiability
ridge while leaving room for the data to refine p_gen.

The reweighting visibly changes the prior shape, particularly
suppressing the AD 290-325 spike that dominates the unweighted
Cohort B SPA (driven by the AD 291-325 tetrarchic reign-window
F2_Other content). After reweighting, that spike is smaller but
still present; the AD 211-217 Caracalla peak is also reduced but
preserved. The prior is now a corpus-composition-balanced
representation of genuine ancient-activity patterns.

## 2. Reweighting diagnostic

Each Cohort B record gets a weight equal to
`(corpus target weight for its type) / (count of that type in Cohort B)`.
So if a type is over-represented in Cohort B relative to the corpus,
its records get down-weighted; if under-represented, up-weighted.

| type | corpus target | cohort count | cohort % | up/down factor |
|---|---:|---:|---:|---:|
| epitaph (funerary) | 0.559 | 5,612 | 17.6 % | **3.17 × up** |
| votive | 0.092 | 2,941 | 9.2 % | 1.00 × (unchanged) |
| identification | 0.125 | 6,451 | 20.3 % | 0.62 × down |
| honorific | 0.036 | 4,076 | 12.8 % | **0.28 × down** |
| building/dedicatory | 0.020 | 1,713 | 5.4 % | 0.36 × down |
| mile-/leaguestone | 0.015 | 2,443 | 7.7 % | **0.19 × down** |
| military diploma | 0.002 | 426 | 1.3 % | **0.18 × down** |
| boundary | 0.003 | 315 | 1.0 % | 0.26 × down |
| acclamation | 0.002 | 24 | 0.08 % | 2.65 × up |
| other small | 0.008 | 426 | 1.3 % | 0.56 × down |
| unknown | 0.139 | 7,414 | 23.3 % | 0.60 × down |

The headline numbers:

- **Epitaphs up-weighted 3.2 ×** (the largest correction). They are
  the corpus majority but the cohort minority. The reweighting brings
  their effective contribution from 18 % to 56 % of the prior.
- **Mile-stones and military diplomas down-weighted 5×.** These are
  almost entirely in Cohort B (military diplomas: median date_range
  0 y; mile-stones: median 2 y; both are predominantly tightly-dated
  by their formulaic nature). Without reweighting they would dominate
  the prior shape in regions where they were active (e.g., Severan
  road-building).
- **Honorific down-weighted 3.5 ×.** Same story: tight-dated by named
  consul/honorand; over-represented in narrow-dated subset; need to
  be brought down to corpus weight.

The 2.65 × up-weighting on acclamation is large but on a tiny base
(24 records). It contributes < 0.5 % of the prior. Not a concern.

## 3. Prior mean + bootstrap CI

`outputs/figures/pgen-prior-mean-with-ci.png`

The reweighted prior mean (green solid) with 90 % bootstrap CI band
(light green) is overlaid against the unweighted Cohort B SPA (blue
dashed). The two diverge most visibly at:

- **AD 290-325 region**: unweighted SPA has a sharp peak (driven by
  the 1,895 `AD 291-325` tetrarchic-period inscriptions, mostly
  epitaphs but tightly dated under that reign-window template).
  Reweighted peak is ~ 30 % smaller because the type composition is
  re-balanced — though it's still the largest peak in the prior.
- **AD 200-220 region**: similar reduction. The Caracalla solo-reign
  cluster (`AD 212-217`) is heavy in honorifics and identification
  inscriptions; reweighting brings those down to corpus proportions.
- **AD 70-90 region**: small reduction. The Flavian / Vesuvius
  signal is type-mixed, so reweighting has less effect.

Bootstrap CI is tight throughout the envelope (visible only as a thin
band around the mean line, except in the very-thinly-covered bins at
50 BC and AD 340+). This reflects the n = 31,841 sample size and
the ~ 1,000-3,000 records overlapping each interior bin.

## 4. Effective sample size by year

`outputs/figures/effective-sample-size-by-year.png`

Per-bin overlap counts. Three regimes:

- **Edge regions (50 BC and AD 330+)**: 150-300 records per bin.
  Thinnest coverage but still adequate (> 50).
- **Body of the envelope (AD 0-330)**: 500-3,100 records per bin,
  with three notable peaks:
  - AD 70-90: peak at 3,100 (Flavian + dated-event content)
  - AD 200-225: 2,400 (Severan)
  - AD 295-325: 2,400 (tetrarchic)
- **No bins with < 50 records.** The empirical prior is well-
  constrained throughout.

This is much stronger than I expected pre-Stage 2. The "thin coverage
at the edges" concern is real but not severe — even the thinnest bin
has 130 records.

## 5. Sigma_prior on log scale (for the GRW formulation)

`outputs/figures/sigma-prior-bin-wise.png`

The mixture model parameterises p_gen via a Gaussian random walk on
log p_gen increments. The empirical-Bayes modification shifts the
prior mean of log p_gen from zero (current) to the cohort-derived
log-density shape. The bootstrap SD of log p_gen at each bin gives a
data-derived value for the prior spread:

| statistic | value |
|---|---:|
| Median sigma_prior across well-covered bins (n ≥ 50) | **0.044** |
| Mean sigma_prior | 0.055 |
| Max sigma_prior (well-covered bins) | 0.186 |
| Bins with n < 50 | 0 of 80 |

To interpret: a sigma of 0.044 on log p_gen translates to roughly
± 9 % multiplicative variation in the linear-scale prior (since
exp(2 × 0.044) ≈ 1.09). That's a moderately-informative prior — strong
enough to substantially constrain the genuine-activity shape, loose
enough that the data can still inform p_gen in regions of disagreement.

The bin-wise sigma_prior is reasonably uniform across the envelope
(visible as the dashed blue line in the figure), with elevations at
the very edges (where the cohort coverage is thin) and slight
elevation in AD 100-200 (where multiple reign-windows overlap,
creating bootstrap variability in the relative contributions).

For the modified mixture-model implementation (Stage 3), we propose:
**use the bin-wise empirical sigma_prior as the strength of the
informative prior on log p_gen**, rather than a single global value.
This naturally widens the prior in thin-coverage regions and tightens
it where the cohort is informative.

## 6. Per-type contributions

`outputs/figures/pgen-per-type-contributions.png`

The stacked-bar figure shows which types are driving the prior shape
after reweighting. Dominant contributors:

- **Epitaph (funerary)**: by far the largest contribution (~ 56 % by
  weight after reweighting). The AD 290-325 spike comes almost
  entirely from tetrarchic-period epitaphs.
- **Identification**: 12.5 % weight; contributes throughout the
  envelope but peaks in the Severan period.
- **Unknown**: 13.9 % weight; broadly distributed.
- **Votive**: 9.2 % weight; peaks ~ AD 130-200.
- **Honorific**: 3.6 % weight (small after reweighting); concentrates
  in AD 100-220 (Trajan-Antonines-Severans).

The smaller types (mile-stone, military diploma, building/dedicatory,
acclamation, boundary, other small) collectively contribute ~ 2.7 %.
They could be dropped from the prior with negligible effect, which
would simplify implementation. We propose retaining them for
methodological cleanliness.

## 7. What this gives us for Stage 3

Three concrete inputs to the modified mixture-model implementation:

1. **`pgen_prior_mean` (80-dim vector)**: the reweighted aggregate
   p_gen, normalised to sum to 1 over the 50 BC – AD 350 envelope at
   5-year resolution. Available at `outputs/tables/pgen-prior-mean-
   and-ci.csv`.
2. **`pgen_prior_log_mean` (80-dim vector)**: the same on log scale,
   for direct use in the GRW-on-log-density parameterisation. Also
   in the table.
3. **`pgen_prior_log_sigma` (80-dim vector)**: bin-wise bootstrap SD
   of log p_gen, the strength of the prior at each bin. Available at
   `outputs/tables/sigma-prior-per-bin.csv`.

These plug directly into the modified mixture-model fit (Stage 3).
Specifically:

```python
# In place of the current zero-mean GRW prior:
# log_pgen ~ GaussianRandomWalk(mu=0, sigma=sigma_smooth, init=...)

# We use:
# log_pgen[t] ~ Normal(pgen_prior_log_mean[t], pgen_prior_log_sigma[t])
# Plus GRW on increments to keep smoothness:
# log_pgen_increments ~ Normal(0, sigma_smooth)
```

This is the BUMPER-style informative-prior formulation (Holden et al.
2017) — the calibration cohort sets the prior centre; the spread is
data-derived; the GRW smoothness layer is preserved.

## 8. Outputs

Figures:

- `outputs/figures/pgen-prior-mean-with-ci.png` — prior mean + 90 % CI;
  unweighted Cohort B SPA for comparison
- `outputs/figures/pgen-per-type-contributions.png` — stacked
  reweighted contributions by type
- `outputs/figures/pgen-reweighting-effect.png` — unweighted vs
  reweighted, with difference highlighted
- `outputs/figures/effective-sample-size-by-year.png` — per-bin overlap
  count
- `outputs/figures/sigma-prior-bin-wise.png` — log-scale mean + SD;
  the sigma_prior recommendation

Tables:

- `outputs/tables/pgen-prior-mean-and-ci.csv` — bin centres, mean,
  q05/q95 on linear scale
- `outputs/tables/sigma-prior-per-bin.csv` — bin centres, log_mean,
  log_sd, log_q05/q95 — directly consumable by the modified mixture-
  model implementation
- `outputs/tables/per-type-effective-N-and-weight.csv` — reweighting
  diagnostic by type

## 9. Caveats

- **The cohort-derived prior is a SNAPSHOT of the corpus's narrow-
  dated content as of 2026-05-24.** If LIRE grows (v3.1 etc.), the
  prior should be regenerated.
- **Type-bias remains a residual concern.** Reweighting corrects the
  type *proportions* to match corpus composition, but does not
  correct any within-type temporal bias (e.g., if narrow-dated
  honorifics from province A and wide-dated honorifics from province
  B have systematically different temporal patterns). Province-level
  reweighting is a possible refinement.
- **The "unknown" type (23 % of Cohort B) is a black box.** Its
  reweighting factor (0.60 ×) reduces but doesn't fix the uncertainty
  about its true type composition. If the unknowns are systematically
  one of the under-represented types (e.g., epitaphs), the
  reweighting is mis-specified for that fraction. Worth a sensitivity
  check.
- **The bootstrap CI assumes the cohort is a random sample.** It is
  not — it's a *biased* sample of the corpus (tight-dateable +
  reign-window-dateable). The CI characterises within-cohort
  variability, not the (uncertain) error of the cohort relative to
  true ancient activity. Treat the CI as a lower bound on prior
  uncertainty.

## 10. Next step

Stage 3 — modified mixture-model implementation in pymc — is now
ready to proceed. The two empirical building blocks (p_conv from
Stage 1, p_gen prior from Stage 2) are in place. The geoscience prior
art (SCUBIDO, BUMPER, Christophe et al. 2018) gives us the formulation.
The recovery-grid diagnostic (Stage 4) will tell us whether the
modified model breaks the identifiability ridge.

End of report.
