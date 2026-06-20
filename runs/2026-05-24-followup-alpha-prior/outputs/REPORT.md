# H2.1 mixture model — α-prior pull vs structural unidentifiability

**Run root:** `runs/2026-05-24-followup-alpha-prior/`
**Authority:** follow-up diagnostic to
`runs/2026-05-24-validation-investigation/outputs/REPORT.md` Experiment A.
The Experiment-A verdict at α=0.95 was "model misspecification, not
sampler effort" — posterior-mean α stayed pinned at 0.74–0.86 across
three cells while truth was 0.95. The Experiment-A "Critical-friend
notes" flagged the production `Beta(2, 2)` prior as a possible
contributor to the bias (it puts only ~5% mass above α=0.95). This
follow-up isolates the prior-pull contribution by re-running the same
3 cells × 3 effort levels under `Beta(1, 1)` ≡ Uniform(0, 1).
**Compute:** sapphire only. 9 new PyMC fits, 610 s total wall
(≈ 10.2 min), pinned to cores 0–5.

---

## Executive summary

**The α=0.95 bias is structural, not prior-pull.** Across nine fits
(3 cells × 3 effort levels), swapping the α prior from Beta(2, 2) to
Uniform(0, 1) moved the posterior mean toward truth by only
**+0.025 on average** (range +0.004 to +0.037; per-cell means +0.014
bimodal, +0.026 regnal_cluster, +0.034 smooth_decline). This is well
below the brief's +0.05 "prior-pull is a substantial contributor"
threshold and explains only ~14–28 % of the gap between the
default-prior posterior and truth. Even with a prior that puts equal
mass on every α ∈ (0, 1), the posterior still lands at α̂ ≈ 0.77–0.89
when truth is 0.95. Recommendation: prior re-specification is **not**
the cheap fix; bring this to Martin's consultation as a structural
identifiability question, and prioritise the non-centred GRW
re-parameterisation (A2 in Experiment A) as the next test.

---

## Critical-friend statistical confirmations (before launching)

Confirmed in line with global CLAUDE.md and Shawn's brief constraint 10:

- **Beta(1, 1) ≡ Uniform(0, 1).** The Beta PDF is
  `f(x; a, b) = Γ(a+b) / (Γ(a)·Γ(b)) · x^(a−1) · (1−x)^(b−1)`. With
  `a = b = 1` this collapses to
  `Γ(2)/(Γ(1)·Γ(1)) · x^0 · (1−x)^0 = 1` on (0, 1) — the loosest prior
  that respects α ∈ (0, 1) as a probability mass.
- **The rest of the model is unchanged from production / Experiment A.**
  `sigma_smooth ~ HalfNormal(1)`,
  `log_pgen_increments ~ Normal(0, sigma_smooth)` shape `(n_bins−1,)`
  anchored at log p(bin 0) = 0,
  `tier_weights ~ Dirichlet([1, 1, 1])`, three-tier basis matrix
  loaded from `design.json`, and the
  `Multinomial(N, α·p_conv + (1−α)·p_gen)` likelihood. The single
  changed line in `build_model_uniform_alpha` is flagged with `★` in
  `code/run-experiment-followup-alpha-prior.py`.
- **Sampler unchanged.** Default pymc NUTS, no numpyro. Seed strategy
  matches Experiment A (`truth["seed"] + 1`). Sequential chains within
  each fit (`cores=1`, `chains=4`).

---

## Method

Re-fitted **replicate_000 only** of the same three α=0.95, N=10 000
cells (one each from `bimodal`, `regnal_cluster`, `smooth_decline`)
that Experiment A used, under the same three sampling-effort tiers:

| level     | n_tune | n_draws | n_chains | target_accept |
|-----------|-------:|--------:|---------:|--------------:|
| baseline  |  1 000 |   2 000 |        4 |          0.95 |
| harder    |  2 000 |   4 000 |        4 |          0.99 |
| hardest   |  4 000 |   8 000 |        4 |         0.995 |

**The single change vs Experiment A:** prior on α, from `Beta(2, 2)`
to `Beta(1, 1)`. Everything else — model structure, sampler, seed,
NUTS settings, post-processing, summary metrics — is identical.

All fits ran on sapphire with `taskset -c 0-5`, single-threaded BLAS
(`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=
VECLIB_MAXIMUM_THREADS=NUMEXPR_NUM_THREADS=NUMBA_NUM_THREADS=1`),
`TMPDIR` pointed at disk-backed scratch
(`/home/shawn/cc-scratch/inscriptions-recovery-grid/pytensor-tmp`),
`PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"`, sequentially
(1 fit at a time × 4 NUTS chains).

---

## Results

All 9 fits completed under the 15-min-per-fit hard stop (max
single-fit wall = 152 s, in the bimodal/hardest combination).
Total wall = 610 s (≈ 10.2 min). Comparable to Experiment A's
~10.3 min.

`α_default` columns are read from Experiment A's posterior JSONs at
`runs/2026-05-24-validation-investigation/outputs/diagnostic-fits/`.
The Pearson r and Wasserstein-1 columns compare the **uniform-prior**
posterior-mean p_gen against true p_gen — i.e., they are the
new run's metrics, directly comparable to the corresponding columns in
Experiment A's results table.

Truth α = 0.95 in every row.

| cell           | level    | wall (s) | div |  R-hat | min ESS-bulk | α̂_uniform | α̂_default |   Δα   | r(p̂_gen, truth) | W-1 (years) |
|----------------|----------|---------:|----:|-------:|-------------:|----------:|-----------:|-------:|-----------------:|------------:|
| bimodal        | baseline |     13.6 |   0 | 1.150  |          23  |     0.751 |      0.747 | +0.004 |            0.612 |       17.81 |
| bimodal        | harder   |     52.6 |   0 | 1.122  |          23  |     0.760 |      0.747 | +0.013 |            0.649 |       17.69 |
| bimodal        | hardest  |    151.5 |   0 | 1.048  |         102  |     0.767 |      0.741 | +0.026 |            0.653 |       17.49 |
| regnal_cluster | baseline |     17.0 |  22 | 1.138  |          21  |     0.888 |      0.863 | +0.025 |            0.788 |       24.67 |
| regnal_cluster | harder   |     64.0 |   0 | 1.013  |         133  |     0.889 |      0.858 | +0.031 |            0.766 |       25.73 |
| regnal_cluster | hardest  |    116.6 |  40 | 1.042  |         144  |     0.882 |      0.859 | +0.023 |            0.767 |       26.19 |
| smooth_decline | baseline |     12.3 |  47 | 1.261  |          12  |     0.876 |      0.839 | +0.037 |            0.926 |       29.93 |
| smooth_decline | harder   |     53.2 |   0 | 1.029  |         107  |     0.882 |      0.848 | +0.034 |            0.925 |       27.92 |
| smooth_decline | hardest  |    121.9 |   0 | 1.014  |         155  |     0.873 |      0.842 | +0.031 |            0.925 |       30.66 |

**Aggregate.** Mean Δα across all 9 fits = **+0.0249**. Per-cell means:
+0.0143 (bimodal), +0.0263 (regnal_cluster), +0.0340 (smooth_decline).
Maximum Δα observed in any cell × level = +0.037. Even at the hardest
effort tier, the uniform-prior posterior-mean α is **0.077 to 0.183
short of truth** (0.95 − [0.767, 0.882, 0.873]) — i.e., the
Beta(2, 2) prior was contributing only 14 % (smooth_decline), 26 %
(regnal_cluster), or 12 % (bimodal) of the bias.

**Convergence diagnostics.** The uniform-prior run is slightly
*less* well-behaved than Experiment A on convergence:

- regnal_cluster/baseline: 22 divergences (vs 1 under default)
- regnal_cluster/hardest: 40 divergences (vs 0 under default)
- smooth_decline/baseline: 47 divergences (vs 0 under default)
- bimodal/baseline: R-hat = 1.150 (vs 1.040 under default)

This is consistent with the geometric intuition: a loose prior on α
lets the sampler probe more of the (α, p_gen) likelihood ridge,
including the funnel-prone neighbourhood of α near 1 where the
GaussianRandomWalk prior on log p_gen becomes effectively informative.
The hardest tier still mostly cleans these up except in
regnal_cluster, where 40 divergences persist even at
target_accept = 0.995 — another fingerprint of geometric pathology
that a non-centred re-parameterisation should address.

---

## Figures

Three PNGs at 150 dpi in `outputs/figures/`. Each figure shows three
rows (baseline / harder / hardest); each row overlays:

- truth p_gen (black)
- recovered posterior-mean p_gen under **uniform** α prior (blue, with
  95 % credible band)
- recovered posterior-mean p_gen under **default Beta(2, 2)** α prior
  (orange, dashed; from Experiment A)

The figure suptitles show per-row Δα(uniform − default) so the
prior-pull contribution is visible per row.

- `outputs/figures/followup-alpha-prior-bimodal_a0.95_uniform_N10000.png`
- `outputs/figures/followup-alpha-prior-regnal_cluster_a0.95_half_century_heavy_N10000.png`
- `outputs/figures/followup-alpha-prior-smooth_decline_a0.95_century_heavy_N10000.png`

By eye, the blue (uniform) and orange (default) p_gen lines are nearly
indistinguishable in every row — the shape recovery is essentially
unchanged. The 95 % credible band on blue is wide (visually ±50 % of
the posterior mean), as it was in Experiment A; the bias is in the
posterior location, not in the model's uncertainty quantification.

---

## Interpretive verdict

**Structural unidentifiability.** Δα < +0.05 averaged across cells ×
levels (in fact +0.025; range +0.004 to +0.037; max +0.037 in any
single cell × level). The brief's binding decision rule is:

> If Δα_uniform_vs_default ≥ +0.10 → prior-pull is a substantial
> contributor; recommend prior re-specification.
> If Δα < +0.05 → bias is structural.

This run lands unambiguously in the "structural" bucket. The
posterior shifts by 14–28 % of the residual gap to truth — a small
positive nudge, consistent with removing some informativeness from the
prior, but nowhere near enough to recover α̂ ≈ 0.95.

Three lines of supporting evidence:

1. **Sampling effort still does not move the posterior.** Under the
   uniform prior, α̂ at baseline → hardest moves by at most ~0.016
   (bimodal: 0.751 → 0.767; regnal_cluster: 0.888 → 0.882; with the
   hardest tier actually slightly *below* the harder tier on
   regnal_cluster and smooth_decline). Same pattern as Experiment A:
   harder sampling reveals the same biased posterior more cleanly; it
   does not move it.
2. **Shape recovery is essentially unchanged.** Pearson r on the
   recovered-mean p_gen vs truth differs by at most ~0.05 between the
   two priors (0.612 vs 0.633 for bimodal/baseline; 0.925 vs 0.937
   for smooth_decline/hardest). W-1 differs by < 2 years in every
   cell × level pair. The recovered p_gen shapes overlap visually
   (see figures).
3. **The likelihood ridge is still pulling.** Even under a uniform
   prior on α, the posterior consistently prefers a *smaller* α than
   truth, paired with a *more-structured* p_gen than the truth shape.
   This is the (α, p_gen)-shape-complexity ridge that Experiment A
   diagnosed; the prior was visibly informative-against-truth at
   α=0.95, but it was not the dominant force keeping α̂ down.

---

## Recommendation for Martin's consultation (2026-05-25)

The Experiment A questions for Martin remain primary, with the
following updates anchored on this follow-up:

1. **Confirmed: the α=0.95 bias is structural, not prior-induced.**
   Under a Uniform(0, 1) prior on α the posterior still lands at
   ≈ 0.77–0.89. Bring the (α, p_gen)-complexity-ridge identifiability
   question to Martin as the primary diagnostic finding, not "should
   we use a sharper α prior".
2. **Next-cheapest test is now Experiment-A's recommendation A2
   (non-centred GRW re-parameterisation), not A1 (sharper α prior).**
   A1 has been ruled out by this follow-up — moving from Beta(2, 2)
   to Beta(1, 1) shifted α̂ by only +0.025 mean (max +0.037 in any
   cell × level). A2 is a mechanical, standard PyMC/Stan best
   practice and is the right next test.
3. **Open question for Martin.** Even with a uniform prior and the
   hardest sampling tier (R-hat ≤ 1.05, ESS-bulk ≥ 100), three
   different truth shapes converge to α̂ ≈ 0.77, 0.88, 0.87 at truth
   0.95. Is there a closed-form identifiability argument here? Or is
   the right intervention a **prior on p_gen complexity** (e.g., a
   tighter HalfNormal on `sigma_smooth`, or a Dirichlet process on
   the p_gen residual instead of a Gaussian random walk on
   log-density)? The Experiment-A "A3" line — formal prior-predictive
   simulation with α drawn from Uniform(0.9, 1.0) — remains the right
   way to answer this and is the recommended Martin-consultation
   deliverable.

---

## Limitations / what we did not do

- **Did not re-fit replicates 001–099 of any cell.** A 9-fit
  diagnostic is sufficient to discriminate Δα ≈ +0.025 from
  Δα ≥ +0.10; the binding decision rule does not need replicate-level
  uncertainty.
- **Did not test Beta(0.5, 0.5).** A Jeffreys-prior diagnostic would
  push slightly more posterior mass to the (0, 1) boundary; given
  that Beta(1, 1) already showed structural failure, the Jeffreys
  test would be a small further perturbation and we judged it
  redundant with this run's verdict.
- **Did not test the non-centred GRW re-parameterisation.** That is
  out of scope of this follow-up (which was specifically the
  prior-pull diagnostic) and is the recommended next experiment.
- **Did not run a uniform-α refit of the flat_baseline α=0.95 cell.**
  Experiment B already diagnosed flat_baseline α=0.95 as the same
  underlying problem; the verdict here transfers.

---

## Reproducibility

```bash
# On sapphire, with the project venv active and the env-var block from
# the brief exported, re-run from this directory:
cd /home/shawn/cc-scratch/inscriptions-recovery-grid/runs/2026-05-24-followup-alpha-prior
taskset -c 0-5 python code/run-experiment-followup-alpha-prior.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --design-json ../2026-05-22-recovery-grid-design/design.json
python code/plot-followup-alpha-prior.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --expA-root ../2026-05-24-validation-investigation \
    --design-json ../2026-05-22-recovery-grid-design/design.json
```

Outputs land in `outputs/diagnostic-fits/<cell_id>/replicate_000_effort=<level>-posterior.json`,
`outputs/figures/`, and `outputs/followup-results.json`.

## Observations register cross-reference

This F1 follow-up to Experiment A is lodged in the register at **Obs 52** (the
sampler-effort / geometry / structural-identifiability triage; this report cited as
a *Source*). See `docs/notes/working-notes.md`. Parent:
`runs/2026-05-24-validation-investigation/` (Experiment A). Back-reference added
2026-06-20 (results-documentation uplift, Tier-2 item 10) to close the
one-directional Obs link.
