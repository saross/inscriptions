<!-- PRODUCTION-READY scaffold; benchmark numbers filled from
     code/benchmark-results.json after the reduced-cost timing run. -->
# §5 Layer A — PRODUCTION-READY

- **Status:** PRODUCTION INFRASTRUCTURE BUILT + BENCHMARKED. The production run
  has **NOT** been launched (per the hard stop in the brief). Awaiting Shawn's go.
- **Date:** 2026-05-31.
- **Host:** zbook (`AMD Ryzen AI MAX+ PRO 395`, 16 physical cores / 32 threads,
  94 GB RAM, idle). pymc 6.0.1, pytensor 3.0.3, arviz 1.1.0 (sapphire parity).
- **Author:** Claude (Opus 4.8, 1M context), on Shawn's brief.
- **Builds on:** the validated smoke harness (`SMOKE-CORE.md`,
  `SMOKE-HIERARCHY.md`): validated single-city Poisson-aoristic core
  (`code/model.py`), validated hierarchy (`code/hier_model.py`), pinned
  hyperpriors (`s_g=0.3, s_u=0.15, s_v=0.15`), `target_accept=0.99`.

---

## 1. What is built (per component)

### BUILD 1 — bin-width-parameterised dataprep + dual cache
- `code/dataprep.py` now takes `--bin-width {25,50}` (default 25y). A `make_grid`
  factory returns `(bin_edges, n_bins)` for any even divisor of the 400-year
  envelope; `aoristic_matrix`, `prepare`, and `load_city` are all grid-aware.
- The 25y cache lives in `code/prepared/` (unchanged path); the 50y cache in
  `code/prepared-50y/` (`default_cache_dir(bin_width)`).
- Each cached `.npz` now also stores the per-inscription `letter_w`
  (`letter_count_conservative`, 0 where missing) for the letter-mass unit, plus
  the grid `bin_width`. Backward-compatible loader (older caches fall back to
  `letter_w = ones`, 25y).
- **Cache verified (both grids):** 268 target cities, 7 large anchors, 45
  target-set provinces, **10 singletons** — all exactly the spec counts. Letter
  column present. Aoristic coverage identity holds (max abs err ~1e-13).
- **Nesting confirmed** (`code/verify_bin_nesting.py`): the 50y edges are a
  subset of the 25y edges, and for all 275 cached cities the 50y aoristic matrix
  equals the adjacent-25y-pair mean to **1.1e-16** — every 50y bin is exactly
  the union of two adjacent 25y bins (spec §3).

### BUILD 2 — letter-mass model variant
- `code/letter_model.py`: the letter-mass hierarchical model. Same pooling
  structure as `hier_model.py` (global / province / city non-centred zero-sum
  RW1 shape tiers + non-centred level offsets, pinned scales, singleton handling),
  but the intensity `Λ[c,t]` is the expected per-bin **letter mass** and the
  observation is over-dispersed.
- **Per-bin letter-mass target** ("letter SPA"): `y[c,t] = Σ_i w_i · p_i[t]`
  where `p_i` is the row-normalised aoristic probability (each inscription
  spreads its full letter count across bins). The content analogue of the
  inscription SPA; continuous, positive, heavy-tailed.
- Two candidate observation forms implemented and selected by PPC (see §2).

### BUILD 3 — subsample-recover driver
- `code/subsample_recover.py`: the §8a.3 calibration grid. Donors = 7 large
  anchors; N ∈ {50,100,200,300,500}; `--reps` (default 40) random subsamples per
  cell; fits standalone `model.py` (primary tier). Each donor's full-N standalone
  posterior-median trajectory **shape** is the recovery truth.
- Metrics per fit: trajectory 95% CI coverage of the truth shape; posterior-median
  shape Pearson r; mean CI width (→ precision-vs-N curve); peak bias (argmax-bin
  offset). `aggregate()` builds the (donor, N) grid + a pooled precision-vs-N
  curve + a coarse calibration `N*` (smallest N with coverage ≥ 0.90 & shape r ≥
  0.90).
- Parallelised: `--n-parallel` worker processes × `--cores` chains each
  (default 4 × 4 = 16 cores). A `--secondary-cells` in-hierarchy tier is left as
  a small confirmatory add-on (off by default).

### BUILD 4 — production orchestrator
- `code/orchestrate.py`: the single launch entrypoint. Runs (1) the 4 monolithic
  fits, (2) the subsample grid, (3) aggregate diagnostics — clustering of the
  268 trajectory shapes, 7-anchor internal consistency (anchor standalone
  trajectory vs its model-free SPA), Pompeii AD-79 external check.
- **Safety:** does NOT execute on import; `main()` prints the plan + run-time
  estimate and EXITS unless `--confirm-production` is passed. The
  `--confirm-production` path is the production run and was NOT executed during
  build/benchmark.

---

## 2. Letter-likelihood form choice + PPC evidence

The spec (§4 Decision 1) requires the letter observation form be finalised at
smoke by a posterior-predictive check. `code/letter_ppc.py` fit BOTH candidate
forms on 5 cities spanning N (Pompeii 4266, Capua 918, Lugdunum 151, Anagnia 71,
Gabii 50) at full config (tune 1000 / draws 1000 / 4 chains / target_accept 0.99)
and scored posterior-predictive coverage of the observed per-bin letter mass,
PPI width (vacuity guard), dispersion realism, and convergence.

| form | coverage (target ~0.95) | mean log10 PPI width | median \|pp-z\| | max R-hat | gates pass |
|------|------|------|------|------|------|
| Gamma (constant-CV, learnt shape `k`) | 0.925 | 2.41 | 0.16 | 1.0100 | **No** (R-hat just over 1.01) |
| **NB (NegBinomial on rounded mass, learnt `φ`)** | **0.975** | 3.05 | 0.15 | **1.0000** | **Yes** |

**Selected form: NEGATIVE BINOMIAL** (`obs_form="nb"`). Rationale:

1. **Convergence.** NB passes the strict convergence gate at base sizing
   (R-hat 1.0000, ESS 1251, 0 divergences). Gamma's R-hat was 1.0100 — exactly
   at the `< 1.01` boundary, a marginal miss localised on one city's RW
   innovation (`z_v[Gabii,14]`) that one escalation would likely clear, but it
   does not pass as-is, and the gate is never relaxed.
2. **Zeros handled natively.** 6.4% of target-set (city, bin) cells have exactly
   zero letter mass (104 cities). NB supports zero counts directly; the Gamma
   form needs a small `eps` floor hack to keep zeros in its (0,∞) support.
3. **Right model class.** Per-bin letter mass is a compound, count-like sum; NB
   is the canonical over-dispersed count model and the form the spec names first.
   Rounding the (10s–1000s-scale) mass to an integer loses negligible information.
4. **Conservative is correct here.** NB's intervals are wider (it slightly
   over-covers at 0.975) — exactly the design-effect caveat the spec demands for
   the letter unit (per-city Kish DEFF ~2.4; Obs 62), where wider/noisier CIs are
   the honest behaviour. Letter mass is an exploratory content overlay, not
   detection; over-covering is the safe error direction.

Runner-up: **Gamma** is the tighter, better-calibrated form (coverage 0.925,
closest to nominal) and would be a defensible alternative with one escalation. It
is recorded here as the fallback if the production NB intervals prove too wide to
be useful. PPC overlay: `code/letter-ppc.png` (both forms envelope the observed
per-bin letter mass across all 5 cities; NB band visibly wider). Both capture the
Pompeii AD-79 content collapse. Design-effect caveat applies throughout: letter
trajectories are wider/noisier than inscription-count trajectories and are read
as a content overlay, never a replacement.

---

## 3. Cache state

| grid | path | bins | cities cached | letter_w |
|------|------|------|------|------|
| 25y (primary) | `code/prepared/` | 16 | 275 (268 target + 7 anchor) | yes |
| 50y (robustness) | `code/prepared-50y/` | 8 | 275 | yes |

Both built from `runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet`
(HEAD 805c991). NOT committed (parquet / `.npz` caches stay out of git). Rebuild
with:

```bash
$PY code/dataprep.py --bin-width 25 --verify
$PY code/dataprep.py --bin-width 50 --verify
```

---

## 4. Run-time estimate (from the BENCHMARK)

<!-- FILLED FROM code/benchmark-results.json -->
**Benchmark method.** `code/benchmark.py` measured one full-config single-city
fit (`t_single`) and built each full 268-city monolithic model, timed a REDUCED
fit (tune 100 / draws 100) with a tune-1/draws-1 compile probe, and extrapolated
to tune 1000 / draws 1000 via `t(tune,draws) ≈ fixed_overhead + (tune+draws) ×
per_iter`. Chains run in parallel across cores, so the wall is the per-chain
iteration cost. target_accept=0.99 throughout (the reduced run is representative
of steady-state per-iteration cost; deeper NUTS trees at large draws are the main
extrapolation caveat — see below).

| component | measured / extrapolated (tune 1000 / draws 1000 / 4 chains / ta 0.99) |
|------|------|
| `t_single` (single-city, N~151, full config) | **4.1 s** (R-hat 1.000, ESS 1575, 0 div) |
| monolithic **inscription 25y** (extrapolated 1000/1000) | **~44–78 min** (two benchmark runs: 2,653 s / 4,650 s; per-iter 1.32–2.33 s) — **the dominant, and VARIABLE, cost** |
| monolithic inscription 50y | **~24 min** (1,432 s; per-iter 0.71 s) |
| monolithic letter 25y (NB) | **~5 min** (304 s; per-iter 0.15 s) |
| monolithic letter 50y (NB) | **~2.5 min** (149 s; per-iter 0.07 s) |
| 4 monolithic fits, concurrent on 16 cores (wall = slowest = insc-25y) | **~44–78 min** |
| subsample grid (1,400 fits, 4-way parallel × 4 chains) | **~0.3–0.5 h** (`t_single` 4.1 s × 1,400 ÷ 4, ±30 %) |
| **TOTAL production wall-clock (concurrent monolithic)** | **~1.5–2.5 h** (point estimate 1.7 h) |

**Assumptions + caveats:**
- The 4 monolithic fits are independent and run **concurrently** (4 fits × 4
  chains = 16 cores), so their wall is the SLOWEST fit (inscription-25y), not the
  sum. If run serially the monolithic block is ~109 min (the sum) — the
  pessimistic bound.
- **The inscription-25y monolithic fit is the bottleneck AND is variable:** two
  benchmark runs at identical config gave 44 min and 78 min (per-iteration cost
  1.32 s vs 2.33 s) — a ~1.75× spread driven by NUTS tree-depth fluctuation at
  `target_accept=0.99` on the ~5,200-latent-parameter model. Plan for ~45–80 min
  for this fit and do not be alarmed if it sits at the high end.
- **The letter fits are cheap** (5 min / 2.5 min): the NB observation has only
  268×16 = 4,288 cells, far lighter than the inscription unit's 45,058-row
  Poisson likelihood. So the two-unit overlay adds little to the monolithic wall.
- The subsample grid is embarrassingly parallel: 1,400 standalone fits at
  ~`t_single`, run 4-way (4 workers × 4 chains = 16 cores). The ±30 % range
  brackets the N-dependence (the grid spans N=50–500; `t_single` benchmarked at
  N~151; a smoke run of larger-N subsamples ran ~6–8 s each at 2 chains) and
  scheduler overhead. Even pessimistically the grid is < 1 h.
- **Extrapolation caveat:** NUTS tree depth can grow as the sampler explores;
  the reduced (100/100) per-iteration cost may under-/over-state the steady-state
  cost at 1000 draws. The reduced run uses the SAME `target_accept=0.99`, so
  per-iteration leapfrog cost is representative, but the monolithic extrapolation
  should be treated as ±20–30 % (which the two-run spread already demonstrates).
- The convergence gate (R-hat<1.01, ESS≥400, 0 div) may require ONE escalation
  (tune/draws ×2) on a miss; if the inscription-25y fit escalates, that fit
  doubles to ~1.5–2.6 h. The estimate is for the base (no-escalation) path; an
  escalated worst case pushes the TOTAL toward ~3–4 h.

**Headline:** the production run is a **~1.5–2.5 h** job on idle zbook (point
estimate 1.7 h), bounded above by ~3–4 h if the heavy inscription-25y fit
escalates. Nothing here is a multi-day run; the monolithic 25y inscription fit is
the one component worth watching (45–80 min, variable), well under the
"surprisingly slow >1–2 h each" flag — but its variance is the main scheduling
uncertainty.

---

## 5. Exact launch command (production — DO NOT run during build)

```bash
ssh zbook
source ~/cc-scratch/s5/s5-env.sh          # threading + PYTENSOR_FLAGS + TMPDIR
$PY runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py \
    --confirm-production \
    --out-base runs/2026-05-30-s5-small-n-trajectories/code/production
```

Dry run (prints plan + estimate, samples nothing):

```bash
$PY runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py \
    --bench-json runs/2026-05-30-s5-small-n-trajectories/code/benchmark-results.json
```

---

## 6. Pre-launch checklist (NOT this session's job)

- [ ] Shawn signs off the letter-likelihood choice (NB) + the run-time estimate.
- [ ] Shawn confirms the pinned scales (already prior-predictive-pinned + smoke-
      validated; see `SMOKE-HIERARCHY.md`).
- [ ] Launch with `--confirm-production`; watch the monolithic gate output.
