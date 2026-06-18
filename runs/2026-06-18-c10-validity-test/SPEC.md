---
title: "C10 aoristic-MC validity test — does point-date sampling destroy the convention signal?"
run-dir: "runs/2026-06-18-c10-validity-test/"
author: "Claude (Opus 4.8, 1M context), on Shawn's request"
date: 2026-06-18
status: "DRAFT — build then audit-before-run (standing rule). Approach (full battery 1a+1b+1c) signed off by Shawn 2026-06-18."
motivates: "the C10 (aoristic-MC) decision in the H2.1 supplementary wave (runs/2026-06-18-h2.1-supplementary-wave/)"
provenance: "pilot 9e286ec found empire α 0.68 (mass-deconvolution) → 0.10 (point-date aoristic-MC), divergence flag fired"
---

# C10 aoristic-MC validity test

## 1. The question

The H2.1 supplementary-wave pilot found that the preregistered aoristic-MC (C10), re-mapped
onto the adopted cross-classified model, gives a **stable α ≈ 0.10** (band [0.091, 0.146]
across 9/10 realisations) versus the deconvolution primary's **α ≈ 0.68** — and the
prereg's width-based divergence flag fired. Two readings:

- **(a)** a legitimate sensitivity — the convention attribution is genuinely fragile to how
  date uncertainty is handled.
- **(b)** a mis-specified test for this model — point-date sampling *destroys the
  slab-concentration that the cross-classified α exists to detect*, so the collapse is an
  artefact of the resampling, not a property of the data.

This test decides (a) vs (b) **computationally, with ground truth**, before we either run C10
across all 29 units (~bulk of the wave's compute) or replace it.

## 2. The load-bearing generative assumption (Shawn-flagged 2026-06-18)

A **convention** inscription was recorded as a round-number **slab** by an editor who could
not date it precisely: its **recorded interval = the slab**, its **true date ~ Uniform(slab)**.
A **genuine** inscription has a **tight recorded interval around its true date** (true date
drawn from a smooth activity shape `p_gen`). Under this model, point-date sampling
`t_i ~ Uniform(recorded interval)` *reconstructs the true-date distribution* — which for
convention inscriptions deliberately erases the slab-concentration α quantifies. This is the
modelling choice the recovery test rests on; if convention is conceived differently, 1b must
be re-specified.

## 3. The three tests

### 3a. Slab-concentration diagnostic (real data, deterministic, no MCMC)

On the **real empire aligned subset**, quantify how much round-number slab structure survives
each date-handling scheme:

- Build the **aoristic-mass** aligned SPA (the deconvolution input — spreads each inscription's
  mass over its recorded interval) and **N point-date-sampled** aligned SPAs.
- Metrics, computed for both: (i) **L1 distance to the nearest slab-library row** (the fixed
  `production-slab-library.json` basis — low = slab-like); (ii) **fraction of mass within ±1
  bin of round-number boundaries** (50 BC, AD 0, 50, 100, …); (iii) the best-fit non-negative
  slab-mixture weight (how much of the SPA the slab library explains).
- **Expected under (b):** aoristic-mass is slab-like (low L1, high round-boundary mass); the
  point-date SPAs are markedly flatter (high L1, round-boundary mass ≈ uniform expectation).
- Cheap; runs anywhere. This is the *mechanism* evidence, not yet decisive.

### 3b. Ground-truth recovery test (synthetic, decisive)

Generate synthetic per-inscription data with a **known α**, then recover it two ways.

- **Generator (the new code; §2 semantics).** For a planted α and N inscriptions:
  `type_i ~ Bernoulli(α)`. Convention → draw a slab S from the slab-library mixture weights;
  recorded interval = S's `[nb, na]`; true date ~ Uniform(S). Genuine → true date ~ `p_gen`
  (a chosen smooth shape, e.g. the empire posterior `p_gen` or a Gaussian bump); recorded
  interval = tight (`[t, t]` or ±2.5 y). Alignment is then assigned by the **real
  `aligned_indicator(rule="C")`** on the recorded intervals (so the aligned/non-aligned split
  is produced exactly as in production, not hand-set).
- **Two count representations from the SAME synthetic inscriptions:** (i) **aoristic-mass**
  largest-remainder counts (the deconvolution input); (ii) **point-date** counts per realisation
  (`t_i ~ Uniform(recorded interval)`, binned). Both honour `k_cc`/`n_rows` invariants.
- **Fit** `build_model_cross_classified(pconv_mode="library")` on (i), and the point-date
  aoristic-MC (N_MC realisations) on (ii). Sweep planted **α ∈ {0.3, 0.5, 0.68, 0.8}**;
  ≥3 generator seeds per α.
- **Reuse the existing recovery-grid machinery** for the mass-arm (it is already validated to
  recover α); the *new* element is the per-inscription interval emission + the point-date arm.

**Decision rule (pre-registered here):**
- **(b) CONFIRMED** if the mass-deconvolution recovers the planted α across the sweep (|Δα|
  within the recovery-grid tolerance, ≈ ≤0.1) **while** the point-date aoristic-MC collapses
  to a low floor **largely independent of the planted α** (i.e. point-date α is flat in true α,
  near the ~0.10 the pilot showed) — that is the signature of signal destruction.
- **(a) SUPPORTED instead** if the point-date aoristic-MC also **tracks** the planted α
  (recovers it within tolerance) — then the empire collapse reflects something real and C10
  stands as a genuine sensitivity.

### 3c. Mass-preserving vs point-collapse contrast (real data)

On the **real empire** data, run the aoristic-MC two ways and compare the recovered α:

- **Point-collapse** (the current C10): `t_i ~ Uniform(recorded interval)` → one bin each.
- **Mass-preserving perturbation**: perturb the *recorded interval bounds* by a small jitter
  (e.g. ±1 bin on `nb`/`na`) but **keep each inscription's mass spread over its (perturbed)
  interval** — preserving slab structure while still injecting date-bracket uncertainty.
- **Expected under (b):** α collapses only under point-collapse; the mass-preserving variant
  stays near the deconvolution α (~0.68). This both isolates the cause *and* prototypes the
  **corrected aoristic-sensitivity** (bracket-perturbation), the natural reading-(b) replacement
  for C10 — pending the held literature scout.

## 4. What each outcome means for C10 in the wave

- **(b) confirmed** → C10's point-date aoristic-MC is dropped/replaced for the cross-classified
  model; the divergence-flag "fired" result is re-framed (the test measures a different
  quantity, not α-fragility); run the held prior-art scout to ground the replacement
  (bracket/dual-dating or Bayesian-aoristic), and report 3c's mass-preserving variant as the
  defensible aoristic-sensitivity. The amendment/paper notes the lodged point-date C10 is
  inappropriate under the Amendment-04 likelihood and states the replacement.
- **(a) supported** → C10 runs as preregistered across the units; the empire collapse is
  reported as a genuine, material limitation.

## 5. Compute, hosts, gates

- **3a**: deterministic, minutes, any host. **3b**: synthetic MCMC fits — mass-arm (4 α × 3
  seeds = 12 fits) + point-date arm (4 α × 3 seeds × N_MC; pin **N_MC = 10** for the test, it is
  a recovery check not the production sensitivity) → on **sapphire** (or zbook if sapphire busy).
  **3c**: 2 schemes × N_MC=10 on empire → sapphire/zbook. Estimate: tens of synthetic fits at
  synthetic-N (small, ~seconds–minutes each) + ~20 empire fits (~275 s each for the empire arm)
  → a few core-hours; well within budget.
- **Gate**: all new code (the interval generator, the diagnostics, the runners) is **audited
  before any run** (standing rule). The synthetic generator's faithfulness to §2 is the key
  audit target.
- No silent negotiate-down; commit before each stage; idata `.nc` gitignored.

## 6. Deliverables

- `code/`: the synthetic-interval generator, the 1a/1b/1c runners, reusing `joint_lib`
  (`build_model_cross_classified`, `aligned_indicator`, slab library) and `h2_lib`/`refit_lib`
  helpers — **import, do not modify** the lodged modules.
- `outputs/`: `VALIDITY-REPORT.md` (the a-vs-b verdict against §3b's decision rule, with the
  1a diagnostic and 1c contrast), `results.json`, figures.
- On verdict: update the C10 decision in the supplementary-wave SPEC + obligations register;
  log an Obs.
