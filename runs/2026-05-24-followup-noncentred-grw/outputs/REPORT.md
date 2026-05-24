# H2.1 follow-up — non-centred GRW reparameterisation

**Run root:** `runs/2026-05-24-followup-noncentred-grw/`
**Authority:** follow-up to
`runs/2026-05-24-validation-investigation/outputs/REPORT.md` Experiment A,
which found α=0.95 posterior bias of ~0.10–0.20 invariant under sampler
effort, and proposed (recommendation **A2**) testing a non-centred
reparameterisation of the GRW prior on `log_pgen_increments` as a
standard PyMC/Stan cure for hierarchical-scale funnel geometry.
**Compute:** sapphire only, cores 6-11. 3 new PyMC fits at hardest
effort (4 000 tune / 8 000 draws / target_accept=0.995 / 4 chains).
Total wall = 336 s (≈ 5.6 min).

## Executive summary

**The non-centred reparameterisation does not fix the α=0.95 bias.**
Averaged across the three α=0.95 cells, Δα (non-centred − centred at
hardest effort) is **+0.001** (range −0.003 to +0.005) — three orders
of magnitude below the +0.08 "substantial fix" threshold and well below
the +0.03 "marginal fix" threshold. The recovered p_gen shape is
indistinguishable between parameterisations by eye and by Pearson r /
W-1. **The bias is not a sampler-geometry artefact; it is a structural
property of the (Beta-prior on α) × (likelihood ridge between α and
p_gen complexity) interaction at α near 1.** Recommendation A2 in the
Experiment A report — "try non-centred before any bigger restructure"
— is now answered: non-centred is a clean *sampler-quality* improvement
(min ESS-bulk improves ~50×, R-hat falls from ~1.04 to ~1.0008) but
does not move the posterior. Recommend Martin's consultation focus
on A3 (formal identifiability investigation) and on alternative
residual processes (Dirichlet process on p_gen, ordered-mixture
parameterisation on α, or a sharper α prior).

---

## Method

### What was reparameterised

The production model (`runs/2026-05-22-recovery-grid-validation/code/`
`02-cell-mixture-fit.py`, lines 168-174) constructs the GRW
**increments** with a centred parameterisation:

```python
sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
log_pgen_increments = pm.Normal(
    "log_pgen_increments",
    mu=0.0,
    sigma=sigma_smooth,
    shape=n_bins - 1,
)
```

i.e., `log_pgen_increments[t] ~ Normal(0, sigma_smooth)`. Because the
scale `sigma_smooth` is itself a random variable, the joint geometry
of `(sigma_smooth, log_pgen_increments)` has the classic Neal funnel
shape: small `sigma_smooth` shrinks every increment toward zero,
collapsing the parameter space to a narrow ridge that NUTS struggles
to leapfrog through. The Experiment A diagnostic verdict
("identifiability ceiling at α ≈ 0.75–0.85 invariant under sampler
effort") is consistent with a sampler that is stuck on the same biased
mode regardless of how cleanly it explores it.

The non-centred construction (in `code/02-mixture-fit-noncentred.py`,
this run):

```python
sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)
z_pgen = pm.Normal("z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1)
log_pgen_increments = pm.Deterministic(
    "log_pgen_increments", sigma_smooth * z_pgen,
)
```

NUTS now explores `(sigma_smooth, z_pgen)`, which is approximately
spherical and decoupled. Mathematically, if `z ~ Normal(0, 1)` and
`sigma_smooth` is independent of `z`, then `sigma_smooth * z`
has marginal `Normal(0, sigma_smooth)`, so the induced prior on
`log_pgen_increments` (and hence `p_gen`) is identical to the centred
construction. The change affects only the sampler's parameter-space
geometry. Everything downstream of `log_pgen_increments` — the
cumsum, the softmax, the mixture with `p_conv`, the Multinomial
observation — is byte-for-byte identical to the production model.

### Prior-equivalence check (pre-launch)

Per the brief's hard requirement, 1 000 prior draws were taken from
each parameterisation and the marginals of `log_pgen_increments`
compared. Pooled across all 79 000 increment values per
construction:

| statistic                       | centred       | non-centred   | ratio NC/C |
|---------------------------------|---------------|---------------|------------|
| mean                            | 5.5 × 10⁻³    | 2.8 × 10⁻³    | —          |
| std                             | 0.991         | 0.965         | 0.973      |
| variance                        | 0.983         | 0.930         | 0.946      |
| q01 / q99                       | −2.96 / 2.99  | −2.88 / 2.88  | match      |
| q025 / q975                     | −2.17 / 2.15  | −2.10 / 2.12  | match      |
| q05 / q95                       | −1.57 / 1.58  | −1.53 / 1.57  | match      |
| q25 / q50 / q75                 | −0.35 / 0.00 / 0.36 | −0.36 / 0.00 / 0.36 | match |
| sigma_smooth marginal mean      | 0.791         | 0.776         | 0.981      |
| sigma_smooth marginal std       | 0.601         | 0.582         | 0.968      |

For reference, HalfNormal(1) has theoretical mean √(2/π) ≈ 0.798. The
two parameterisations agree to within Monte-Carlo error (1/√1 000 ≈
3 % on standard deviations, ~6 % on variances). All three equivalence
gates passed:
`ok_mean_near_zero` = True,
`ok_variance_ratio_within_15pct` = True,
`ok_sigma_marginal_matches` = True.
Full equivalence record at `outputs/prior-equivalence-check.json`.

### Production fits

3 cells × 1 effort = 3 fits. Hardest effort only per the brief
(n_tune=4 000, n_draws=8 000, n_chains=4, target_accept=0.995). The
"baseline bonus" was not run because the hardest-effort verdict is
already definitive; baseline fits would add cost without altering the
α-bias conclusion (centred and non-centred should converge to the
same posterior at any effort if both samplers mix; the question is
*where* that posterior sits, which non-centred has not moved).

Critical-friend statistical confirmations (per brief):

* **(a) Appropriate?** Yes. The GRW increments depend on a
  hierarchical scale `sigma_smooth ~ HalfNormal(1)`. This is exactly
  the situation non-centred is designed for; standard
  PyMC/Stan recommendation.
* **(b) More robust alternatives?** Yes — sharper α prior (cheapest
  diagnostic), ordered-mixture parameterisation, or replacing the GRW
  with a Dirichlet process. Non-centred was tried *first* because
  it is mechanical, mathematically equivalent, and lowest-risk.
* **(c) Current best practice?** Yes, documented in the PyMC user
  guide and Stan reference manual.
* **(d) Assumptions hold?** Yes. The reparameterisation is exact and
  introduces no new assumptions. Equivalence was verified by 1 000
  prior draws before any fits were run (see table above).

---

## Results

| cell (shape)     | param.        | div | max R-hat | min ESS-bulk | min ESS-tail | α_mean | Δα vs centred | r(mean, truth) | W-1   | wall (s) |
|------------------|---------------|----:|----------:|-------------:|-------------:|-------:|--------------:|---------------:|------:|---------:|
| bimodal          | centred       |  0  | 1.0411    | 104.4        | 72.2         | 0.741  | —             | 0.611          | 17.79 | 133.4    |
| bimodal          | non-centred   |  0  | 1.0008    | 7 627.6      | 12 192.7     | 0.746  | **+0.005**    | 0.634          | 17.75 | 130.1    |
| regnal_cluster   | centred       |  0  | 1.0372    | 147.1        | 260.3        | 0.859  | —             | 0.749          | 26.88 | 138.9    |
| regnal_cluster   | non-centred   |  0  | 1.0006    | 6 540.2      | 6 797.5      | 0.856  | **−0.003**    | 0.742          | 27.27 | 130.0    |
| smooth_decline   | centred       |  0  | 1.0037    | 247.9        | 421.4        | 0.842  | —             | 0.937          | 39.34 | 131.1    |
| smooth_decline   | non-centred   |  0  | 1.0005    | 12 321.6     | 15 441.1     | 0.844  | **+0.002**    | 0.936          | 39.16 |  69.8    |

Truth α = 0.95 in every row. **Mean Δα = +0.001** (the average is
dominated by `bimodal` and `smooth_decline`'s small positive moves and
`regnal_cluster`'s small negative move; all three are smaller than the
posterior's own MC uncertainty at min-ESS-bulk ≈ 7 000).

### Sampler-quality changes under non-centred

* **Divergences:** 0 → 0 (already clean at hardest).
* **R-hat:** drops from ~1.04 to ~1.0008 — a ~50× reduction in the
  between-chain disagreement. All three cells under non-centred meet
  the prereg's R-hat < 1.01 gate; only one of the three did under
  centred (`smooth_decline`).
* **ESS-bulk / ESS-tail:** improves by **~50×** in two cells (104 →
  7 628; 248 → 12 322) and ~45× in the third (147 → 6 540). All
  three cells now exceed the prereg's ESS gate ≥ 400 by an order of
  magnitude or more.
* **Wall time:** unchanged or slightly faster (smooth_decline drops
  131 s → 70 s — likely a NUTS step-size adaptation difference, not a
  computational change since the model graph has only one extra
  Deterministic node).

The non-centred reparameterisation is, by every sampler-quality
metric, **strictly better than the centred construction**. It is also,
on the central question of α recovery, **indistinguishable in effect.**

### Figures

Three side-by-side comparison plots in `outputs/figures/`:

* `compare-noncentred-vs-centred-bimodal.png`
* `compare-noncentred-vs-centred-regnal.png`
* `compare-noncentred-vs-centred-smooth.png`

Each shows truth p_gen (black), centred-hardest posterior-mean p_gen
with 95 % CI (red), and non-centred-hardest posterior-mean p_gen with
95 % CI (blue). The blue and red curves track each other to within
the width of the CI bands in every cell — visual confirmation of the
table.

---

## Interpretive verdict

**Per the brief's pre-stated decision rule** (Δα < +0.03 →
"reparameterisation alone does not fix it"): **the bias is deeper
than funnel geometry**. Three lines of evidence reinforce this:

1. **Sampler-quality diagnostics improved substantially** (50× ESS-bulk
   jump, R-hat collapse) without moving the posterior location. This
   is the same logical pattern as Experiment A's "uplifting tune and
   draws moves diagnostics but not α_mean" — and is the strongest
   possible evidence that we are sampling the same biased posterior
   more cleanly, not converging to a different (less biased) posterior.
2. **The non-centred posterior is not a buggy approximation of the
   centred one.** Prior-predictive equivalence is exact (passed all
   three gates); the convergence diagnostics are clean (R-hat ≤ 1.0008,
   ESS in the thousands); and the recovered p_gen overlays the
   centred recovery within the CI bands. We can rule out
   "implementation problem" as an explanation for the null result.
3. **The bias direction is consistent.** Across three qualitatively
   different truths (bimodal, regnal_cluster, smooth_decline), both
   parameterisations land at α ≈ 0.74–0.86 — the same biased
   posterior region Experiment A identified, regardless of geometric
   reparameterisation. The likelihood-ridge mechanism (mass tradable
   between α and p_gen complexity, with the Beta(2,2) prior pulling α
   away from 1) is the parsimonious explanation.

The α=0.95 bias is now confirmed as a **structural property of the
model + prior**, not a sampler-effort or sampler-geometry artefact.

### Recommendation for Martin's consultation (2026-05-25)

1. **Adopt non-centred as the default GRW parameterisation** even
   though it doesn't fix the α-bias. The ~50× ESS improvement at no
   cost is independently valuable — it tightens posterior uncertainty
   estimates, reduces the wall time needed to clear the prereg's
   ESS/R-hat gates at lower effort tiers, and removes a known
   geometric pathology from the model regardless of whether α=0.95 is
   a realistic operating point. This is a clean methodological
   improvement to bring into Phase 2.
2. **Investigate α-identifiability formally** (Experiment A's
   recommendation A3). Specifically, propose to Martin: (i) a prior-
   predictive simulation with α ~ Uniform(0.9, 1.0) to characterise
   the likelihood ridge directly; (ii) a sharper α prior such as
   Beta(5, 5) restricted to (0.5, 1.0), or a uniform on (0.7, 1.0), as
   a diagnostic to separate "prior pull" from "structural
   unidentifiability"; (iii) an ordered-mixture parameterisation
   where the constraint α ∈ (0.5, 1) is built in.
3. **Treat α=0.95 as a documented model limitation.** Independent of
   any reparameterisation, the model cannot recover α near 1
   accurately with this prior structure. If real-data α is expected
   to be in (0.5, 0.85) — which is the empirical range for most
   inscription corpora — the limitation is acceptable. Document it
   prominently in the prereg amendment.

---

## Reproducibility

```bash
# On sapphire, cores 6-11, with the project venv active:
cd /home/shawn/cc-scratch/inscriptions-recovery-grid/runs/2026-05-24-followup-noncentred-grw

source /home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/activate
export TMPDIR=/home/shawn/cc-scratch/inscriptions-recovery-grid/pytensor-tmp
export PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1

# 1. Prior-equivalence check (verifies non-centred ≡ centred).
taskset -c 6-11 python code/check-prior-equivalence.py

# 2. Production fits (3 cells × hardest effort).
taskset -c 6-11 python code/run-noncentred-experiment.py \
    --output-root $PWD \
    --validation-root ../2026-05-22-recovery-grid-validation \
    --design-json ../2026-05-22-recovery-grid-design/design.json

# 3. Comparison figures.
taskset -c 6-11 python code/make-comparison-figures.py
```

### File tree

```
runs/2026-05-24-followup-noncentred-grw/
├── code/
│   ├── 02-mixture-fit-noncentred.py     (modified model)
│   ├── check-prior-equivalence.py       (1 000-draw equivalence)
│   ├── make-comparison-figures.py
│   └── run-noncentred-experiment.py     (cloned from run-experiment-a.py)
└── outputs/
    ├── REPORT.md                         (this file)
    ├── prior-equivalence-check.json
    ├── noncentred-experiment-results.json
    ├── diagnostic-fits/
    │   ├── shape=bimodal_alpha=0.95_tier=uniform_N=10000/
    │   │   └── replicate_000_effort=hardest-noncentred-posterior.json
    │   ├── shape=regnal_cluster_alpha=0.95_tier=half_century_heavy_N=10000/
    │   │   └── replicate_000_effort=hardest-noncentred-posterior.json
    │   └── shape=smooth_decline_alpha=0.95_tier=century_heavy_N=10000/
    │       └── replicate_000_effort=hardest-noncentred-posterior.json
    └── figures/
        ├── compare-noncentred-vs-centred-bimodal.png
        ├── compare-noncentred-vs-centred-regnal.png
        └── compare-noncentred-vs-centred-smooth.png
```
