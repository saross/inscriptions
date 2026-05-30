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
| **50 ≤ N < 1549** | **279** | **§5 small-N target set** |
| N ≥ 1549 | 7 | confirmatory-eligible (H3b); used here only as validation anchors |

Target-set N: median 116, p75 204, p90 347, max 1020 (117 cities at N 50–100;
124 at 100–300; 38 at 300–1549). Hierarchy: 46 provinces, median 4 cities each,
**10 singletons**.

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
- **Priors (weakly-informative; to be pinned in a design artefact before the
  production run):** `σ_μ, σ_u, σ_v ~ HalfNormal(·)`; overall level anchored so
  Σ_t exp(μ[t]) matches the empire-level mean rate. Exact hyperprior scales set
  at smoke-test stage and committed before production.

**Likelihood (proper Bayesian-aoristic, per Crema 2024 / baorista).** Each
inscription contributes a marginalised-over-true-date likelihood given the
ICAR-smoothed intensity, using the aoristic weights `a[i,t]`: the event's
contribution sums the (normalised) intensity over the bins its interval allows.
The exact functional form is pinned in the implementation and **validated against
baorista on a single city with pooling disabled** (correctness check) before the
hierarchy is added.

## 5. Two-measure execution

- **Inscription count (primary).** Each inscription contributes weight 1.
- **Letter mass (exploratory overlay).** Each inscription contributes weight =
  `letter_count_conservative`. Reported with the explicit design-effect caveat
  (Obs 61): per-city DEFF ≈ 2.2 inflates posterior CI width, so letter-mass
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
- **Size:** monolithic model ≈ 16 bins × (1 global + 46 province + 279 city)
  ≈ 5,200 latent rates + hyperparameters. Tractable; one model per unit
  (inscription, letter) × two bin widths (25y primary, 50y robustness) = 4 fits.
- **Pre-launch gate:** smoke-test on a 3–5 city subset (one well-dated large
  anchor + two small-N cities) → confirm convergence + baorista agreement on the
  single-city likelihood, commit the harness, then sign-off, then production.

## 8. Outputs

- Per-city posterior trajectory shape with 95 % credible intervals (both units).
- **Aggregate diagnostic:** posterior precision vs N (median CI width binned by
  the N buckets in §2); trajectory-shape clustering across the 279 cities.
- **Validation anchors:** the 7 large (N ≥ 1549) well-dated cities (e.g. Pompeii,
  Ostia) — fit Layer A on them and check the recovered trajectory against their
  independently-known flourishing dates, as a method sanity check before
  trusting small-N outputs. (This is the Layer A precursor to the Layer B
  validation gate; full independent-date assembly is Layer B's job.)
- A negative result (small-N trajectories too uncertain to be informative below
  some N) is itself a reportable methodological finding.

## 9. Confirmed design decisions (2026-05-30)

| Decision | Setting |
|---|---|
| Bin width | 25 years (16 bins), 50y robustness check |
| Model structure | Monolithic hierarchical (all 279 cities + 46 provinces jointly) |
| Aoristic | Proper Bayesian-aoristic (baorista-style), validated vs baorista |
| Two-unit | Inscription primary; letter-mass exploratory overlay (design-effect caveat) |
| Singletons | Pool toward global trajectory |
| Bad records | Re-clip to AD ≤ 350 envelope |
| Layer B | Deferred (needs H3a β_within) |
| Parameterisation | Non-centred RW innovations |

## 10. Open items for sign-off

- Hyperprior scales (`σ_μ, σ_u, σ_v` and the level anchor) — to be pinned at
  smoke-test stage and committed in a design artefact before production.
- Exact aoristic likelihood form — pinned in code, validated against baorista.
- Confirmation that the 7 large anchors are the right validation set (vs a
  curated independently-dated subset).
