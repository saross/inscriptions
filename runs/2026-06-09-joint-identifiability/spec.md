# Joint identifiability-remediation model — design spec

**Status:** DRAFT for Shawn sign-off before the full recovery-validation grid.
**Date:** 2026-06-09 · **Author:** Claude Code (Opus 4.8, 1M context) on Shawn's brief.
**Supersedes (as the remediation lever):** the informed-α *prior* — REFUTED
(`runs/2026-06-09-informed-alpha/`; a prior cannot fix a confidently-wrong
likelihood). UK/Australian English; Oxford comma.

---

## 1. Problem (one paragraph)

The H2.1 temporal-mixture (`build_model_f1_f3`) splits each unit's summed-
probability analysis (SPA) into an editorial-convention component (fraction α,
shape `p_conv` = a Dirichlet reweighting of the shared 3-tier calendar-slab
basis) and a smooth genuine component (fraction 1 − α, shape `p_gen` = a
non-centred Gaussian random walk, GRW). For **temporally-concentrated units**
(mostly frontier/military provinces whose round-period dating clusters in their
AD ~100–300 occupation window, where their genuine signal also lives) convention
and genuine are **confounded in time**: the flexible GRW absorbs the period-
concentrated convention mass and α collapses far below the true convention
fraction (Moesia inferior: fitted α 0.05 vs 57 % grid-aligned; diagnostic
`runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`).
A per-unit basis *over*-attributes instead (Salona α 0.54 → 0.99). The temporal
distribution **alone** cannot pin the split — α is partially identified.

## 2. Why a second likelihood term, not a prior (the theory)

Established practice, grounded in the scout synthesis
(`planning/scout-2026-06-09-identifiability-remediation-SYNTHESIS.md`):

- **The likelihood is confidently wrong, not merely flat.** Under weak component
  separation the mixing-weight estimate behaves as a threshold estimator that can
  declare components identical when they are not (Feller et al. 2016, *Ann. Appl.
  Stat.* 2019). The informed-α small-N re-test confirmed the empirical
  manifestation: at every concentration κ ∈ {6, 10, 20} the posterior median stayed
  at 15–35 % of the true α — "the flexible GRW `p_gen` absorbs the narrow
  convention mass regardless of N or prior tightness".
- **A prior over a partially-identified region is never updated by the data**
  (Gustafson 2010; Giacomini & Kitagawa 2021) — so an informed *prior* on α was
  predicted to fail, and did.
- **Auxiliary information entering as a LIKELIHOOD term is the canonical remedy** —
  the concomitant-variable / latent-class-with-covariates tradition (Dayton &
  Macready 1988 → Huang & Bandeen-Roche 2004, which gives the identification theory
  for adding a covariate that restores identifiability). The archaeological
  archetype is the OxCal two-component reliable/unreliable outlier mixture (Bronk
  Ramsey 2009), about as mainstream as Bayesian archaeology gets.

**Two-citation argument:** Feller + Gustafson for "a prior cannot fix the
confounded likelihood"; Huang & Bandeen-Roche for "a second likelihood term can."

## 3. The independent signal: grid-alignment classification

The temporal shape ignores one observable: each inscription's **interval geometry**
(width + endpoint roundness), the "observable proxy for the criterion LIRE's
`raw_dating` does not preserve" (Decision 38). Editorial-convention datings sit on
the round-year calendar grid (`[101,300]`, `[1,200]`, decade slabs); genuine
precision datings do not (a consular year `[112,112]`, a pre-eruption terminus
`[1,79]`).

**Per-inscription convention-typed indicator `aligned_i ∈ {0,1}` (lead definition, "C"):**

```
aligned_i  =  family ∈ {F1_round, F3_periodic}                       # round-period + decade slabs
            ∨ ( family == Big  ∧  round25(nb) ∧ round25(na) )         # wide round-endpoint slabs ([1,250] etc.)
```

where `round25(x)` is `x mod 25 ∈ {0, 1, 24}` and `family` is the existing,
recovery-validated `classify_family` (verbatim, `h2_lib.classify_family`). This is
the "round-endpoint grid-alignment score that ALSO credits wide Big slabs, not just
F1+F3" the design called for. Note `[1,200]`/`[1,300]` are *already* F1_round; the
round-endpoint-Big clause catches wide structural slabs whose width is off the F1
width-grid (e.g. `[1,250]`, width 249).

**Empirical robustness (grounded on the real corpus, 2026-06-09):** the θ-calibration
(below) is near-identical for F1∨F3-only (RMSE 0.119), C (0.120), and a pure
"both endpoints on the 25-y grid, width ≥ 25" test "D" (0.117). Only the naïve
"all Big" definition degrades it (RMSE 0.164) — because it miscounts Pompeii's
genuine `[1,79]` terminus as convention. **D will be reported as a robustness
alternative**; the choice is immaterial to the result, which is itself a finding.

## 4. The joint model

Per unit, two likelihood terms sharing the single latent convention fraction α:

```
# --- shared latent ---
α            ~ Beta(1, 1)                          # the target (unchanged prior)

# --- TEMPORAL term (unchanged from build_model_f1_f3) ---
tier_weights ~ Dirichlet(ones(n_tiers))
p_conv        = tier_weights · tier_basis          # shared 3-tier calendar-slab basis
sigma_smooth ~ HalfNormal(1)
z_pgen       ~ Normal(0, 1, shape=n_bins-1)
p_gen         = softmax(cumsum(sigma_smooth · z_pgen))   # non-centred GRW
p_mix         = α · p_conv + (1 − α) · p_gen
y_obs        ~ Multinomial(N_eff, p_mix)           observed = aoristic-SPA counts (largest-remainder)

# --- CLASSIFICATION term (NEW) ---
θ_conv       ~ Beta(a_conv, b_conv)                # P(aligned | convention-class); prior near 1
θ_gen        ~ Beta(a_gen,  b_gen)                 # P(aligned | genuine-class);    prior near 0
π_align       = α · θ_conv + (1 − α) · θ_gen
k_aligned    ~ Binomial(N_rows, π_align)           observed = # convention-typed inscriptions
```

Everything in the temporal block is **byte-identical** to the recovery-validated
`build_model_f1_f3`. The classification block is the only addition. The two terms
share α: for an identifiable unit the sharp temporal term dominates; for a
confounded unit the temporal term is near-flat in α (the under-identification) and
the **sharp binomial** (N_rows ≈ 1,500–40,000) pins α near its grid-aligned
fraction — Huang & Bandeen-Roche identifiability restoration.

### 4.1 θ_conv, θ_gen — the linchpin (calibrated, not free)

A single per-unit binomial gives **one** constraint (π_align), so α, θ_conv, θ_gen
are **not** jointly identifiable from `k` alone. θ_conv and θ_gen must be pinned by
priors. We calibrate the prior centres **empirically from the identifiable units**
(where the temporal α is reliable), then apply them to the confounded units — the
project's established empirical-Bayes calibration-cohort architecture (Stage 3;
Martin-endorsed "use the granular/identified units to characterise convention").

**Calibration (2026-06-09, on the 19 production-identifiable units):** least-squares
fit of `aligned_frac ≈ θ_gen + (θ_conv − θ_gen)·α_shared` gives **θ_gen ≈ 0.155,
θ_conv ≈ 0.945** (indicator C; RMSE 0.120). The classification-implied α
(`(aligned_frac − θ_gen)/(θ_conv − θ_gen)`) then lands **inside the [shared,
per-unit] bracket for every under-identified unit** (Moesia 0.52 ∈ [0.05, 0.87];
Pannonia inf 0.57 ∈ [0.15, 0.75]; Numidia 0.42 ∈ [0.17, 0.52]) and **agrees with
the reliable temporal α on identifiable units** (Pompeii 0.00↔0.00; empire
0.65↔0.67; Dacia 0.01↔0.00). This is the headline plausibility evidence; recovery
validation (§6) tests whether the *jointly-fit* posterior recovers known α.

**Priors (not point values):** centre θ_conv, θ_gen at the calibrated values with
genuine width, so θ-uncertainty propagates into α:

```
θ_conv ~ Beta(μ=0.945, κ=40)   # ≈ Beta(37.8, 2.2)   sd ≈ 0.035
θ_gen  ~ Beta(μ=0.155, κ=40)   # ≈ Beta(6.2, 33.8)    sd ≈ 0.057
```

(κ = 40 is a deliberate, documented input — these are calibration constants, not
data-estimated per unit. Sensitivity to κ ∈ {20, 40, 80} is part of the validation.)

## 5. Realistic synthetic generator (the recovery test bed)

The informed-α prototype's narrow-Gaussian convention (µ=200, σ=60) was
**unrepresentative**: a real frontier unit's convention is **broad round-endpoint
slabs concentrated in the occupation window**, not a narrow peak. Grounded shapes
(2026-06-09): Moesia inferior convention centroid 195, 90 % mass in AD 100–300;
latin-aggregate convention centroid 136, 61 % in window. The generator must span
both.

**Well-specified generative model (Tier 1 — matches the likelihood):**
for a cell with true (α, p_conv_true, p_gen_true, θ_conv_true, θ_gen_true, N):

1. `y ~ Multinomial(N, α·p_conv_true + (1−α)·p_gen_true)`           — temporal data
2. `k ~ Binomial(N, α·θ_conv_true + (1−α)·θ_gen_true)`              — classification data

**Cell axes:**
- **regime** — `identifiable` (broad convention, %win ≈ 0.60; genuine peaked-early
  or broad — NOT confounded) vs `confounded` (convention broad-slab %win ≈ 0.85–0.90;
  genuine peaked in the same AD 100–300 window).
- **p_conv_true** — built from realistic round-endpoint slab mixtures
  (`identifiable`: {[1,300],[1,200],[50,250]}; `confounded`: {[101,300],[151,300],
  [101,250],[101,200]}), aoristic-spread — NOT the fitted basis (so the fit's
  shared basis is an honest approximation, as in production).
- **p_gen_true** — genuine peak: Gaussian µ ∈ {AD 150, 200} σ ∈ {30, 50}, plus a
  `regnal_cluster` (the recovery grid's hard corner) and a broad/uniform control.
- **α_true** ∈ {0.0, 0.2, 0.4, 0.6, 0.8}.
- **N** ∈ {1500, 2800, 15000} (frontier-province, mid, aggregate scales).
- **θ_true** — base (θ_conv 0.95, θ_gen 0.15) + a **mismatch** arm
  (θ_gen_true 0.25, θ_conv_true 0.90) to test calibration-transfer robustness (§7).

**Tier 2 (mis-specification robustness, smaller):** draw actual per-inscription
intervals from a slab dictionary + a genuine date generator, classify them with the
real `aligned_i` rule, and aoristic-SPA → (y, k). Tests that the binomial/multinomial
generative assumption is not load-bearing. Run a reduced axis set.

## 6. Acceptance criteria (the verdict)

The joint model is **fit for the remediation** iff, across the synthetic grid:

1. **Identifiable cells recovered unchanged.** For `identifiable`-regime cells the
   joint-model α posterior median is within the Amendment-01 shape-conditioned LoA
   (±0.18) of α_true — i.e. the second term does **no harm** where α was already
   identified. (Primary gate.)
2. **Confounded cells pulled toward truth, without over-attribution.** For
   `confounded`-regime cells the joint α median is **materially closer to α_true**
   than the shared-basis baseline AND does **not overshoot** like the per-unit
   basis: target |bias| < 0.18 and no systematic positive bias > +0.10. (Primary gate.)
3. **Coverage.** The 95 % α credible interval covers α_true at ≥ 0.90 empirical
   rate across cells (diagnostic, not a hard gate — mirrors Decision 33's α-as-
   diagnostic stance).
4. **Convergence** unchanged: per-cell `convergence_pass` (max R̂ < 1.01, min
   bulk-ESS ≥ 400) ≥ 95 % cell pass-rate (the grid standard).
5. **PPC adequacy** not degraded vs the temporal-only fit (the classification term
   must not buy α-recovery at the cost of temporal misfit).

Report the baseline (`build_model_f1_f3`, shared basis) and the per-unit-basis upper
bound alongside, so the joint model's position between them is explicit.

## 7. Critical-friend checks (standing rule)

- **(a) more appropriate?** The concomitant-variable mixture is *the* established
  remedy for covariate-restored identifiability (§2). ✓
- **(b) more powerful/robust alternative?** A **hierarchical-over-units** model
  (partial-pool θ, and even α, across units) would borrow strength and estimate θ
  rather than calibrate-then-fix — more powerful, but a larger build and a single
  all-units fit. Logged as the principled extension; lead with per-unit joint fits
  (matches the production harness; cheap; one fit per unit). The **two-regime
  switch** (point- vs set-identified, gated by an empirical-identifiability
  diagnostic) is the uncodified fallback, not the lead.
- **(c) current best practice?** OxCal outlier model (Bronk Ramsey 2009); Huang &
  Bandeen-Roche (2004). ✓
- **(d) assumptions hold?** The load-bearing assumption is **θ-transferability** —
  θ calibrated on identifiable units applied to confounded ones. If frontier-province
  *genuine* inscriptions have systematically more coincidental round endpoints, θ_gen
  is too low and α is over-pinned. **Mitigation:** the θ-mismatch synthetic arm (§5)
  and the κ-sensitivity sweep quantify the exposure; report it.

## 8. Build plan (this session, local)

1. `code/joint_lib.py` — `build_model_joint(y, k_aligned, n_rows, tier_basis,
   theta_conv_ab, theta_gen_ab)`; the realistic slab→p_conv generator; the θ-calibration
   routine (reads `summary-final.json` + corpus); the `aligned_i` rule.
2. `code/calibrate_theta.py` — emit `outputs/theta-calibration.json` (θ_conv, θ_gen,
   per-unit aligned fractions + implied α; the §4.1 numbers, reproducibly).
3. `code/poc_recovery.py` — a **small local** recovery proof-of-concept: a handful of
   cells (≥2 identifiable, ≥3 confounded, spanning α_true), joint vs shared-basis vs
   per-unit, against criteria 1–2. De-risk before proposing the full sapphire grid.
4. `outputs/POC-REPORT.md` + the full-grid spec → **Shawn sign-off** → full recovery
   grid on **sapphire** (reconcile sapphire git first) → OSF amendment (folding in
   `planning/prereg-note-2026-06-09-alpha-identifiability.md`, whose "Planned
   remediation" section must be rewritten from informed-α-prior to this joint model).

## 9. Out of scope / explicitly deferred

- The full sapphire recovery grid (needs sign-off — §8.4).
- The OSF amendment text (after a clean grid).
- Re-fitting the 28 production units under the joint model (after a clean grid).
- H3b identifiable-set reconciliation (gap<0.20→17 vs gap≤0.25→16) — separate task.
- The hierarchical-over-units extension and the two-regime fallback (logged, not built).
