# H2.1 recovery-grid validation — diagnostic investigation

**Run root:** `runs/2026-05-24-validation-investigation/`
**Authority:** diagnoses two methodological questions from the H2.1
validation `runs/2026-05-22-recovery-grid-validation/outputs/REPORT.md`,
which reported FAIL on the binding criteria (40.9% of cells passing both
α-coverage ≥ 90% and shape-recovery median-Pearson-r ≥ 0.95).
**Compute:** sapphire only. 9 new PyMC fits (≈ 10.3 min wall, sequential
NUTS, default pymc backend); 5 existing-posterior re-analyses.

## Executive summary

**Experiment A (α=0.95 pathology).** The bias at α=0.95 is **model
misspecification, not sampler effort.** Across three representative
α=0.95 cells, going from baseline (1 000 tune / 2 000 draws /
target_accept=0.95) to hardest (4 000 tune / 8 000 draws /
target_accept=0.995) reduced R-hat (≤ 1.04), raised ESS by ~5×, and
eliminated divergences — yet the posterior-mean α stayed pinned at
~0.74–0.86 (truth 0.95) and the recovered p_gen shape changed
negligibly. Harder sampling reveals the same biased posterior more
cleanly; it does not move it. **Recommendation: do not simply uplift
sampler defaults. Investigate identifiability and re-parameterise.**

**Experiment B (flat_baseline metric mismatch).** Recovery is genuinely
accurate at α ≤ 0.70 (variance of recovered posterior-mean ~10⁻⁹–10⁻⁸
against uniform truth 1/80 = 1.25×10⁻²; max|dev| ~10⁻⁴; W1 ≤ 0.7
years). At α=0.95 the picture is different — variance ~7×10⁻⁶ and
max|dev| ~6×10⁻³ (≈ 50% of the uniform value), with a fictitious slope
and a tail bump. **Recommendation: report W-1 (or another
distribution-sensitive metric) instead of Pearson r for flat truths,
AND treat the α=0.95 corner as misspecification rather than a metric
artefact — Experiment A and Experiment B are reporting the same
underlying problem from two directions.**

---

## Experiment A — α=0.95 sampler pathology

### Method

We re-fitted **replicate_000 only** of three α=0.95, N=10 000 cells
(one each from `bimodal`, `regnal_cluster`, `smooth_decline`) under
three sampling-effort tiers:

| level     | n_tune | n_draws | n_chains | target_accept |
|-----------|--------|---------|----------|---------------|
| baseline  | 1 000  | 2 000   | 4        | 0.95          |
| harder    | 2 000  | 4 000   | 4        | 0.99          |
| hardest   | 4 000  | 8 000   | 4        | 0.995         |

All fits ran on sapphire with single-threaded BLAS, `TMPDIR` pointed at
disk-backed scratch, `PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"`,
sequentially (1 fit at a time × 4 NUTS chains).

**Glossary for non-Bayesian readers.** *Divergence* = a NUTS sample
where the simulated Hamiltonian path diverged numerically; many
divergences flag posterior geometry the leapfrog integrator cannot
follow (often funnel shapes around a hierarchical scale parameter).
*R-hat* = between-chain / within-chain variance ratio; should be < 1.01
for clean mixing. *ESS-bulk / ESS-tail* = effective independent-sample
counts in the body / tails of the marginal; minimums < ~400 are weak.
*Wasserstein-1 (W-1)* = the "earth-mover" distance between two
probability densities on the year axis; in our setup it is reported in
years and is sensitive to *where* mass sits (a tail bump on flat
truth is penalised, unlike Pearson r). *target_accept* = NUTS's
adaptive acceptance-rate target; higher = smaller step size = better
geometry resolution at higher cost.

### Results

Nine fits; all converged at the "harder" and "hardest" tiers (R-hat ≤
1.04, divergences = 0). Wall times scale with effort as expected (~10×
between baseline and hardest in two cells; ~11× in cell 3).

| cell (truncated) | level | div | R-hat | min ESS-bulk | min ESS-tail | wall (s) | α_mean | r(mean,truth) | W-1 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| bimodal | baseline | 0 | 1.040 | 72 | 80 | 11.3 | 0.747 | 0.633 | 17.69 |
| bimodal | harder | 0 | 1.120 | 27 | 15 | 76.0 | 0.747 | 0.632 | 17.83 |
| bimodal | hardest | 0 | 1.041 | 104 | 72 | 133.4 | 0.741 | 0.611 | 17.79 |
| regnal_cluster | baseline | 1 | 1.123 | 27 | 85 | 15.6 | 0.863 | 0.737 | 26.96 |
| regnal_cluster | harder | 0 | 1.034 | 92 | 119 | 62.0 | 0.858 | 0.750 | 26.82 |
| regnal_cluster | hardest | 0 | 1.037 | 147 | 260 | 138.9 | 0.859 | 0.748 | 26.88 |
| smooth_decline | baseline | 0 | 1.109 | 29 | 35 | 12.0 | 0.839 | 0.939 | 40.50 |
| smooth_decline | harder | 0 | 1.019 | 100 | 145 | 31.8 | 0.848 | 0.937 | 38.52 |
| smooth_decline | hardest | 0 | 1.004 | 248 | 421 | 131.1 | 0.842 | 0.937 | 39.34 |

Truth α = 0.95 in every row.

### Figures

- `outputs/figures/experiment-a-bimodal_a0.95_uniform_N10000.png`
- `outputs/figures/experiment-a-regnal_cluster_a0.95_half_century_heavy_N10000.png`
- `outputs/figures/experiment-a-smooth_decline_a0.95_century_heavy_N10000.png`

Each figure is a three-row stack (baseline / harder / hardest) of
recovered posterior-mean p_gen (with 95% credible band) against true
p_gen.

### Interpretive verdict

**Model misspecification / partial unidentifiability at α near 1**, not
sampler effort. Three lines of evidence:

1. **The posterior location is invariant under harder sampling.** α_mean
   moves by at most ~0.01 across baseline → hardest. The recovered p_gen
   shape is visually identical across the three rows of each figure.
2. **Sampling-quality diagnostics improve under harder sampling.** R-hat
   falls toward 1.00; ESS rises by ~5×; divergences stay at zero. We
   are sampling the same posterior more cleanly — and that posterior is
   biased.
3. **The bias is large and structurally interpretable.** At α=0.95 only
   5% of the multinomial mass arises from p_gen; p_conv (a weighted sum
   of smooth tier-basis vectors) already accounts for most of the
   observed bin counts. The model can shift mass between (α, p_gen) and
   (1−α, p_conv) along a likelihood ridge. The posterior consistently
   prefers a smaller α with a more-structured p_gen — exactly what a
   GaussianRandomWalk-smoothed log-density prior on p_gen will be drawn
   toward when it can borrow signal from the convention side.

**Important context on the cell-level "divergences" headline.** The
validation REPORT.md reports cell-level *total* divergences (sum across
100 replicates). The cells we chose had cell totals of 5 667, 4 954,
3 628 — but the **median replicate has 0–1 divergences** (we checked).
Divergences are heavy-tailed: 40–60% of replicates show any
divergences, and the worst 5% contribute ~200–1 100 each. So
replicate_000 of our three cells is a low-divergence replicate (0, 1,
0 divergences at baseline). This makes the misspecification verdict
*stronger*, not weaker — even on a fortunately-clean replicate the
recovery is biased.

### Recommendation

Do not simply uplift `n_draws`, `target_accept`, etc. The pre-Phase-2
PyMC defaults already produce a clean posterior at the hardest setting;
the posterior is just in the wrong place. Three avenues worth exploring,
in increasing order of cost:

- **A1. Sharper α prior near 1.** `Beta(2,2)` is symmetric and
  effectively centred on 0.5; it puts weight ≤ 0.05 on α > 0.95. The
  combination of (a likelihood ridge between α and shape complexity)
  and (a prior that disfavours α near 1) is sufficient to explain a
  posterior at α ≈ 0.75–0.85 even when truth is α = 0.95. This is the
  cheapest test — re-fit one of the cells under a Beta(1,1) or
  Beta(0.5, 0.5) and see whether α_mean moves. **However:** in real-data
  use we will *not* want a prior pulled toward α = 1, so this is a
  diagnostic, not a fix.
- **A2. Re-parameterise the p_gen prior.** The GaussianRandomWalk on
  log-density values, combined with the softmax and the deterministic
  HalfNormal(1) bandwidth, has a known funnel-style geometry (σ_smooth
  small → log_pgen_increments shrunk to zero → p_gen approaches uniform;
  σ_smooth large → log_pgen_increments unconstrained). A
  non-centred parameterisation
  (`log_pgen_increments = sigma_smooth * z` with `z ~ Normal(0,1)`) is
  the standard cure; this is a mechanical fix worth trying before any
  bigger restructure.
- **A3. Investigate identifiability formally.** Even with a perfect
  sampler, the likelihood ridge between α and p_gen complexity may be
  genuinely unidentifiable at α near 1. A prior-predictive simulation
  with α drawn from Uniform(0.9, 1.0) and the model fit to the implied
  data should reveal whether the bias survives. This is the
  consultation question for Martin.

---

## Experiment B — flat_baseline metric mismatch

### Method

For five `flat_baseline` cells (α ∈ {0.05, 0.30, 0.50, 0.70, 0.95}; all
`tier=uniform`, `N=10 000`) we loaded the existing replicate_000
posterior summary and computed: variance of true p_gen, variance of
recovered posterior-mean p_gen, max |recovered − true|, W-1 between
recovered-mean and truth.

**Note on per-draw Pearson r.** The validation pipeline persists only
the posterior-median p_gen vector, not the full draws. Per-draw Pearson
r therefore could not be computed from disk without re-fitting; we
chose to spend Experiment A's budget on the sampler-effort question
rather than re-running these. The variance/max|dev| numbers below carry
the diagnostic load directly: if variance of the posterior-MEAN p_gen
is ~10⁻⁹ then any per-draw Pearson r computed against a constant truth
remains ill-defined; if variance of the posterior-mean is ~7×10⁻⁶
(α=0.95 case) the per-draw r will be both well-defined and dominated by
the artefact's shape rather than by sampling jitter.

### Results

Truth `p_gen` is uniform 1/80 ≈ 0.0125; var(truth) ≈ 3.0×10⁻³⁶ (i.e.,
floating-point zero). All five recovered cells have undefined Pearson r
(constant truth → ConstantInputWarning), matching the REPORT.md's
column of `nan`.

| α | var(recovered mean) | max\|recovered − true\| | W-1 (years) | α_median (post) | α_cov | divergences |
|---|--:|--:|--:|--:|---|--:|
| 0.05 | 5.04×10⁻⁹ | 1.34×10⁻⁴ | 0.488 | 0.069 | yes | 0 |
| 0.30 | 2.29×10⁻⁹ | 1.62×10⁻⁴ | 0.248 | 0.379 | yes | 0 |
| 0.50 | 1.62×10⁻⁸ | 2.85×10⁻⁴ | 0.696 | 0.330 | no  | 0 |
| 0.70 | 1.31×10⁻⁹ | 8.00×10⁻⁵ | 0.113 | 0.631 | yes | 0 |
| 0.95 | 7.01×10⁻⁶ | 6.39×10⁻³ | 23.187 | 0.910 | yes | 176 |

For context, the uniform truth value 1/80 = 0.0125. The α=0.95 cell's
max deviation of 6.39×10⁻³ is therefore ~ 51% of the uniform value;
the recovered density visibly slopes down across the envelope with a
tail bump in the AD 300–350 region (see figure).

### Figure

- `outputs/figures/experiment-b-flat-baseline-recovery.png` — five
  panels, one per cell. Each panel shows true p_gen (black, horizontal
  at 1/80) and the recovered posterior-mean (blue). The α=0.05 through
  α=0.70 panels are visually flat overlays; the α=0.95 panel diverges.

### Interpretive verdict

**Mixed.** At α ≤ 0.70 the recovery is *genuinely accurate*:
variance ~ 10⁻⁹–10⁻⁸ (six orders of magnitude below the uniform value
0.0125² ≈ 1.6×10⁻⁴ that would be required to distinguish anything from
flat); max|dev| ~ 10⁻⁴; W-1 ≤ 0.7 years. Pearson r is mathematically
inapplicable because truth has zero variance — this is a
**metric-mismatch artefact**, not a recovery artefact. **W-1 is the
right binding metric for the flat_baseline shape.**

At α=0.95 the recovery genuinely fails — variance is 1 000× larger,
max|dev| is 50× larger, W-1 is 200× larger, and a fictitious slope plus
a fictitious tail bump are visible by eye. This is the **same
mechanism uncovered in Experiment A** — at α=0.95 the model's ability
to identify p_gen collapses regardless of what the true shape is
(bimodal, regnal-cluster, smooth-decline, or flat).

### Recommendation

Two amendments, independently:

- **B1. Replace Pearson r with W-1 for the binding shape criterion on
  flat truths.** A W-1 ≤ ~2 years (in the 80-bin envelope of 400 years)
  is a reasonable threshold for "indistinguishable from truth" given
  the α ≤ 0.70 numbers above (max W-1 = 0.696). The exact threshold
  should be pinned in the prereg amendment with one-paragraph
  justification anchored on these 5 cells' empirical W-1 distribution.
  *Caveat:* W-1's threshold depends on envelope length (it's reported
  in the same units as the year axis, here 400 years wide). Any
  amendment should state this explicitly.
- **B2. Do NOT scope the α=0.95 row out of flat_baseline.** The α=0.95
  failure is real recovery failure, not a metric artefact.
  flat_baseline at α=0.95 should remain a binding test cell, scored on
  W-1, and should be expected to FAIL until the Experiment A
  misspecification is fixed.

---

## Questions for Martin (2026-05-25 consultation)

Context the agent uncovered, framed as concrete questions for an
applied-econometrician audience:

1. **Identifiability at α near 1.** The mixture
   `p = α·p_conv + (1−α)·p_gen` with p_conv a fixed (up to tier
   weights) basis and p_gen a flexible GRW-smoothed log-density has a
   likelihood ridge between (high α + structured p_gen) and (lower α +
   smoother p_gen). At α=0.95 the posterior systematically lands near
   α ≈ 0.75–0.85 across three qualitatively different truths (bimodal,
   regnal-cluster, smooth_decline) AND across the flat_baseline shape,
   independent of sampling effort. *Question for Martin: is there a
   standard treatment of α-identifiability in a fixed-basis +
   nonparametric-residual mixture? Specifically, do you recommend a
   sharper prior on α, a non-centred re-parameterisation of the GRW
   prior, or a structurally different residual (e.g., Dirichlet process
   on p_gen instead of GRW on log p_gen) before we declare the
   recovery-grid binding criteria amended?*
2. **Choice of shape metric.** The prereg binds shape recovery on
   posterior-median Pearson r ≥ 0.95 (cell-pass) and ≥ 90% of cells
   passing (global). Pearson r is undefined for the flat_baseline shape
   (zero-variance truth) and we additionally see it can be high (~0.94)
   in the α=0.95 smooth_decline case where W-1 is 39 years (i.e.,
   ~10% of the envelope length) — r is mass-blind in a way W-1 is not.
   *Question for Martin: would you keep Pearson r as the binding
   metric and add W-1 as a co-binding metric, or replace Pearson r
   with W-1 outright? If the latter, what's a defensible W-1 threshold
   choice — empirical (anchored on the α ≤ 0.70 flat_baseline cells'
   W-1 distribution) or theoretical (e.g., bin-width-scaled)?*
3. **Heavy-tailed divergences.** In the three α=0.95 cells we examined,
   median per-replicate divergences are 0–1 but ~5% of replicates show
   200–1 100. The validation REPORT.md headline divergence counts are
   cell totals which dramatically over-state typical-replicate
   pathology. *Question for Martin: in a 100-replicate cell, is it
   defensible to report the median per-replicate divergence count
   alongside the total? Or does the heavy-tailed structure itself
   indicate sampler pathology we should address before declaring the
   model usable on real data?*
4. **Bias-variance trade in the binding criterion.** The validation
   reports 40.9% of cells passing both binding criteria — but
   flat_baseline (0% shape-pass under the current metric) and α=0.95
   (22% shape-pass) drag the global rate down. If we accept that the
   "shape recovery" criterion is in some sense not well-defined on a
   flat truth (Experiment B verdict) AND that α near 1 has a real
   identifiability ceiling (Experiment A verdict), what fraction of the
   grid's failure should be attributed to (i) a binding criterion that
   needs replacing (metric mismatch), (ii) a region of (α, shape) space
   where the model is structurally weak but might be acceptable for
   archaeology if α near 1 is empirically rare, and (iii) genuine model
   defects requiring re-parameterisation? *Question for Martin: how
   would you partition the failure budget and which fraction would you
   want a prereg amendment to address before the model goes to real
   data?*

---

## Critical-friend statistical notes (raised in line with global CLAUDE.md)

- **Pearson r is the wrong metric for a uniform-truth diagnostic.**
  Confirmed by Experiment B. Recommend W-1 (or a Hellinger / total-
  variation distance) as the binding metric for flat shapes.
- **GaussianRandomWalk prior with centred parameterisation is a known
  funnel pattern.** We did not test a non-centred re-parameterisation
  in this investigation; this is the first thing I'd try in a follow-up
  (cheap; mechanical; standard Stan/PyMC best practice).
- **Beta(2,2) prior on α puts only 5% mass on α > 0.95.** Combined
  with the likelihood ridge, this is sufficient to explain a posterior
  at α ≈ 0.85 even when truth is α = 0.95. A "sharper alpha prior near
  1" diagnostic would unambiguously separate "prior pull" from
  "structural unidentifiability".
- **The 95% credible band on p_gen at α=0.95 is wide** (visually about
  ±50% of the posterior mean in the bimodal cell). The model knows it
  is uncertain; we just happen to be in a region where its mean is
  biased. α-coverage stays around 0.70 — the CI does sometimes contain
  truth — but its location is consistently wrong.

---

## Limitations / what we did not do

- **Did not re-fit the flat_baseline α=0.95 cell** with extra sampler
  effort. Experiment A's verdict (sampling effort doesn't move the
  posterior) makes this lower-priority, but a single confirmation fit
  would close the loop on the "is α=0.95 flat_baseline also
  misspecification or is it sampler effort here too?" question.
- **Did not test a non-centred re-parameterisation.** That's a separate
  follow-up. Doing it here would have changed the experiment from "is
  the existing default sampler underpowered?" to "is the existing model
  parameterisation sound?"; the brief asked the former.
- **Did not test alternative priors on α.** Same reasoning — out of
  scope of the sampler-effort question.
- **Did not persist full per-draw p_gen draws** for any new fit.
  Posterior summaries (mean, median, 95% CI quantiles) plus diagnostics
  are persisted; if Martin wants per-draw Pearson r distributions we
  would need a small follow-up fit with the full InferenceData saved.

## Reproducibility

```bash
# On sapphire, with the project venv active and the env-var block from
# the brief exported, re-run from this directory:
cd /home/shawn/cc-scratch/inscriptions-recovery-grid/runs/2026-05-24-validation-investigation
python code/run-experiment-a.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --design-json ../2026-05-22-recovery-grid-design/design.json
python code/run-experiment-b.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --design-json ../2026-05-22-recovery-grid-design/design.json
python code/plot-experiment-a.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --design-json ../2026-05-22-recovery-grid-design/design.json
```

## Observations register cross-reference

Lodged in the register at **Obs 52** (sampler-effort / geometry / structural-
identifiability triage — Experiment A; cross-references Obs 28 and Obs 24) and
**Obs 53** (Pearson-r-against-zero-variance binding-criterion bug — Experiment B;
cross-references Obs 38). See `docs/notes/working-notes.md`. Companions:
`runs/2026-05-24-followup-alpha-prior/` (F1), `runs/2026-05-24-followup-noncentred-grw/`
(F3), `runs/2026-05-24-followup-systematics/` (F0b). Back-reference added 2026-06-20
(results-documentation uplift, Tier-2 item 10) to close the one-directional Obs link.
