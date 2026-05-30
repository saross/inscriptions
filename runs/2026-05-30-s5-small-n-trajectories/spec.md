# §5 small-N city-trajectory estimation — Layer A implementation spec

- **Status:** DRAFT for Shawn's review and sign-off (pre-launch gate; nothing
  runs until smoke-tested and signed off).
- **Date drafted:** 2026-05-30
- **Author:** Claude (Opus 4.8, 1M context), on Shawn's brief.
- **Preregistration basis:** §5 "City-level temporal trajectory estimation for
  small-N cities" (`planning/preregistration-draft.md` lines 366–374).
  Exploratory, non-confirmatory; estimation, not hypothesis testing. Honest
  negative result is a preregistered acceptable outcome.
- **Two-measure framework:** runs under both units per OSF Amendment 01
  (`planning/osf-amendment-2026-05-29-two-measure-framework.md`): inscription
  count primary, letter mass exploratory overlay.

---

## 1. Scope and sequencing

This spec covers **Layer A only** (trajectory-shape estimation). The downstream
layers are sequenced by their dependencies:

- **Layer A (this spec) — UNBLOCKED NOW.** Needs only the LIRE corpus + Hanson
  matches. Independent of Grid B, OSF Amendment 01 lodgement, and Stage 3. Runs
  on zbook.
- **Layer B (β-inversion to population) — DEFERRED.** Requires `β_within` from
  H3a, which is post-Grid-B and post-amendment. Specced separately when H3a
  output exists.
- **Province-scale extension (~50 provinces) — FOLLOW-ON.** Same machinery at
  province aggregation; rolls in cheaply once Layer A is validated.

## 2. Target set (grounded; `scripts/s5-target-set-profile.py`)

Hanson-matched (`urban_context_city` non-null AND `urban_context_pop_est`
non-null), Rome-excluded:

| Bucket | Cities | Disposition |
|---|---|---|
| N < 50 | 754 | below estimation floor — excluded |
| **50 ≤ N < 1549** | **268** | **§5 small-N target set** (post-clip, exact-Rome) |
| N ≥ 1549 | 7 | confirmatory-eligible (H3b); used here only as validation anchors |

Target-set N: median 116, p75 204, p90 347, max 1020 (pre-clip profile
sub-buckets: 117 at N 50–100; 124 at 100–300; 38 at 300–1549). Hierarchy: 45
provinces, median 4 cities each, **10 singletons**. The **268** target is the
confirmed post-clip count under exact Rome-exclusion (commit `2c82a87`): the
pre-clip profile gave 279/280; the Rome-regex fix restored Romula (+1) and 12
cities cross below N=50 after envelope-clipping. The N-distribution sub-buckets
are pre-clip-profile descriptives, refreshed at the production cache build.

**Data preparation (pre-fit):**

1. Filter to the analysis envelope **50 BC – AD 350**; **re-clip** `not_after`
   (and `not_before`) to the envelope — at least one bad record
   (`not_after = 2230`) escaped the upstream filter. Drop or clip per inscription.
2. Hanson-match + Rome-exclusion + N ≥ 50 floor as above.
3. Compute per-inscription aoristic bin weights `a[i,t]` = fraction of
   inscription *i*'s `[not_before, not_after]` interval overlapping bin *t*
   (uniform-within-interval). Inscriptions wholly outside the envelope are
   dropped; partial-overlap intervals are clipped to the envelope before
   weighting.

## 3. Temporal grid

- **25-year bins, 50 BC – AD 350 → 16 bins.** Rationale: median aoristic
  interval width is 99 years, so finer bins are illusory precision for
  small-N cities; 25y nests within the project's standard 5-year SPA grid
  (25 = 5×5, same epoch boundaries) and aligns with the existing 25/50-year
  reachability-window vocabulary.
- **Robustness check:** re-fit at **50-year bins (8 bins)**; report trajectory
  stability across bin widths as a supplementary (pre-empts the bin-width
  question; flags any small-N city whose shape is bin-width-sensitive).

## 4. Model (custom pymc hierarchical; NOT baorista)

For city *c* in province *p(c)*, latent log-rate over bins *t*:

```
log λ[c,t] = μ[t]  +  u[p(c), t]  +  v[c, t]
```

- **μ[t]** — global mean trajectory; first-order random-walk (RW1) ICAR prior
  over bins: `μ[t] − μ[t−1] ~ Normal(0, σ_μ)`.
- **u[p,t]** — province deviation; RW1-smoothed over bins, partial-pooled across
  provinces toward 0 with scale `σ_u` (provinces shrink toward the global
  trajectory).
- **v[c,t]** — city deviation; RW1-smoothed over bins, partial-pooled across
  cities toward their province with scale `σ_v` (small-N cities shrink toward
  the province trajectory — the mechanism that makes small-N estimation
  honest).
- **Singletons** (10 provinces with one target city): the province level is
  unidentified, so these cities pool directly toward the **global** trajectory
  (province term fixed at 0 / merged into global).
- **Parameterisation:** non-centred for all RW innovations (the 2026-05-24 F3
  lesson: non-centred GRW gave a 45–50× ESS gain at negligible bias).
- **Variance components are learnt, not fixed.** `σ_μ, σ_u, σ_v ~ HalfNormal(·)`
  (log-rate scale), and the model estimates them — the `σ_v` posterior is itself
  a reported quantity (how heterogeneous are city trajectories within
  provinces). The overall level is anchored so `Σ_t exp(μ[t])` matches the
  empire-level mean rate.
- **Hyperprior scales pinned by prior-predictive check.** At smoke stage,
  trajectory ensembles are simulated *from the prior alone* (no fitted outcomes,
  so priors are set without peeking at results) and the HalfNormal scales chosen
  so the ensemble looks like plausible epigraphic histories (neither jagged nor
  flat). The chosen scales are committed in a design artefact **before** the
  production fit; Claude pins and reports them, Shawn does a post-hoc sanity
  check (2026-05-30 decision).

**Likelihood — Poisson-process aoristic (inscription count, primary).**
Inscriptions are modelled as a Poisson process with intensity
`λ[c,t] = exp(μ[t] + u[p(c),t] + v[c,t])`. Each inscription's true bin is
unobserved but interval-censored, so it is marginalised analytically, giving the
per-city log-likelihood

```
log L[c] = − Σ_t λ[c,t]  +  Σ_i log( Σ_t a[i,t] · λ[c,t] )
```

where `a[i,t]` is the fraction of bin *t* covered by inscription *i*'s
envelope-clipped interval (uniform-within-interval aoristic assumption).
Narrow-interval inscriptions concentrate rate-mass; wide editorial-template
intervals contribute `Σ a·λ` over many bins and so inform the level but not the
shape — the desired behaviour, with no hand-tuning. The **full Poisson form**
(not the level-free normalised form) is used so the hierarchy pools level as
well as shape. Implemented as a custom pymc log-likelihood
(`pm.Potential` / `CustomDist`); **validated against baorista on a single city
with pooling disabled, comparing the normalised (shape) posterior** (baorista
models shape only).

**Likelihood — letter mass (exploratory overlay).** Letters are not Poisson
events, so the clean form does not transfer. Each inscription's letters are
aoristically apportioned to bins (`w_i · a[i,t]`) and the per-bin letter mass is
modelled with an over-dispersed observation (negative-binomial / Gamma) whose
dispersion absorbs the design effect (Obs 61). The exact letter form
(weighted-Poisson vs NB/Gamma) is **finalised at the smoke stage by
posterior-predictive check** — proportionate given letter mass is exploratory
and design-effect-noisy here.

## 5. Two-measure execution

- **Inscription count (primary).** Each inscription contributes weight 1.
- **Letter mass (exploratory overlay).** Each inscription contributes weight =
  `letter_count_conservative`. Reported with the explicit design-effect caveat
  (Obs 61): per-city DEFF ≈ 2.4 (urban_context_city) inflates posterior CI
  width, so letter-mass
  trajectories are wider/noisier; this is estimation (CIs widen) not detection
  (which is unreachable), so it remains feasible. Letter-mass trajectories are
  read as a content overlay, never as a replacement for the inscription-count
  trajectory.

## 6. Fitting configuration

- pymc 6.0.1 / pytensor 3.0.3 (zbook is at sapphire parity).
- NUTS; start at draws 1000 / tune 1000 / chains 4 / target_accept 0.95;
  escalate draws/tune if convergence gates miss (never relax the gate — the
  2026-05-22 lesson).
- **Convergence gates:** R̂ < 1.01 on all parameters; ESS ≥ 400 per chain on the
  reported trajectory quantities; zero divergences. Report cell-wise.
- Threading/scratch (recovery-grid lessons): `OMP/OpenBLAS/MKL/NUMEXPR/
  NUMBA_NUM_THREADS=1`; `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`;
  disk-backed `TMPDIR` (not tmpfs).

## 7. Compute plan (zbook)

- **Host:** zbook (16 physical cores, 94 GB RAM, idle; pymc/pytensor/arviz at
  sapphire parity). Grid B stays untouched on sapphire.
- **Provisioning needed:** `git pull` on zbook (currently 3+ weeks stale); sync
  the filtered LIRE parquet (`runs/2026-05-26-letter-count-probe/data/
  lire-filtered-with-letters.parquet`, 58 MB, not git-tracked → scp). No R /
  baorista install required for Layer A (baorista is only the separate
  Decision-3 cross-check).
- **Size:** monolithic model ≈ 16 bins × (1 global + 45 province + 268 city)
  ≈ 5,200 latent rates + hyperparameters. Tractable; one model per unit
  (inscription, letter) × two bin widths (25y primary, 50y robustness) = 4 fits.
- **Pre-launch gate:** smoke-test on a 3–5 city subset (one well-dated large
  anchor + two small-N cities) → confirm convergence + baorista agreement on the
  single-city likelihood, commit the harness, then sign-off, then production.

## 8. Outputs

- Per-city posterior trajectory shape with 95 % credible intervals (both units).
- **Aggregate diagnostic:** posterior precision vs N (median CI width binned by
  the N buckets in §2); trajectory-shape clustering across the 268 cities.
- A negative result (small-N trajectories too uncertain to be informative below
  some N) is itself a reportable methodological finding (quantified by the
  subsample-recover calibration below).

### 8a. Validation design (three complementary checks; 2026-05-30)

1. **Internal consistency.** Fit Layer A on the 7 large (N ≥ 1549) cities;
   confirm each posterior trajectory matches the city's own well-constrained
   empirical SPA — i.e. smoothing + pooling do not distort a data-rich city.

2. **External anchors.** Sharpest is **Pompeii's AD 79 terminus** (the city was
   buried, so genuine post-79 mass should be ~zero — a direct check on aoristic
   handling and template smearing); foundation dates for any colonies in the set
   give "~zero before founding" tests. Full independent-date assembly remains
   Layer B's job.

3. **Subsample-and-recover (the calibration test).** A mini recovery grid for
   the trajectory method, run thoroughly:
   - **Donors:** the 7 large cities, chosen to span trajectory shapes (e.g.
     Pompeii early/terminated, Ostia later peak, Salona, plus frontier vs
     Italian). Each donor's full-N standalone posterior-median trajectory is the
     recovery *truth*.
   - **Grid:** N ∈ {50, 100, 200, 300, 500}; **30–50 random subsamples** per
     (donor, N) cell; refit and compare to truth.
   - **Metrics per cell:** trajectory 95 % CI coverage of the full-N truth
     (target ~0.95; flags over-confidence or vacuity); posterior-median shape
     correlation (Pearson r); CI width (→ the precision-vs-N curve); peak bias.
   - **Primary tier = standalone (no pooling)** — isolates the likelihood +
     aoristic + RW-smoothing at small N and is *conservative*, since pooling
     toward the province can only reduce small-N variance. A **secondary tier**
     refits a handful of (donor, N) cells **within the full hierarchy** to
     confirm pooling improves coverage as expected.
   - **Deliverable:** a calibration statement — below N ≈ X the trajectory CIs
     are too wide to be informative; above it, recovery is honest. Quantifies the
     preregistered honest-negative-result and guards against it being a model
     artefact.
   - **Compute:** ~7 donors × 5 N × ~40 replicates ≈ 1,400 single-city fits
     (fast; small N, 16 bins) on zbook.

## 9. Confirmed design decisions (2026-05-30)

| Decision | Setting |
|---|---|
| Bin width | 25 years (16 bins), 50y robustness check |
| Model structure | Monolithic hierarchical (all 268 cities + 45 provinces jointly) |
| Aoristic likelihood | Poisson-process aoristic, full level (inscription); NB/Gamma at smoke (letter); validated vs baorista on shape |
| Hyperpriors | Variance components learnt; HalfNormal scales pinned by prior-predictive at smoke, committed pre-production (Shawn sanity-checks) |
| Validation | Internal consistency (7 large) + Pompeii AD 79 external + thorough subsample-recover N∈{50–500} |
| Two-unit | Inscription primary; letter-mass exploratory overlay (design-effect caveat) |
| Singletons | Pool toward global trajectory |
| Bad records | Re-clip to AD ≤ 350 envelope |
| Layer B | Deferred (needs H3a β_within) |
| Parameterisation | Non-centred RW innovations |

## 10. Open items — resolved 2026-05-30

All three sign-off items are now closed (see §4 likelihood + hyperprior
protocol, §8a validation):

- **Aoristic likelihood** — Poisson-process form pinned (§4); letter form
  finalised at smoke (Decision 1).
- **Hyperpriors** — learnt; scales pinned by prior-predictive at smoke, committed
  pre-production; Shawn sanity-checks (Decision 2).
- **Validation set** — three-part design with thorough subsample-recover (§8a,
  Decision 3).

**Remaining (smoke-stage, before production):** (a) prior-predictive hyperprior
pinning + design artefact; (b) aoristic-likelihood code validated against
baorista (single city, shape); (c) letter-mass likelihood form chosen by PPC;
(d) convergence confirmed on the 3–5 city smoke subset. Production launches only
after these **and** Shawn's go.
