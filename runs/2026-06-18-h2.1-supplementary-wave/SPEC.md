---
title: "H2.1 supplementary wave — launch spec"
run-dir: "runs/2026-06-18-h2.1-supplementary-wave/"
author: "Claude (Opus 4.8, 1M context), on Shawn's request"
date: 2026-06-18
status: "DRAFT — pre-launch sign-off pending (gate at §10). Build + smoke + pilot may
  proceed on sign-off of §§3–4; the full production run gates on the pilot (§9)."
supersedes-status-of: "the 'staged, not run' note in runs/2026-06-07-h2.1-launch-prep/outputs/production/SUMMARY.md"
prereg-authority: "osf-lodgement-2026-05-20 (original supplementary, lines cited per item) as
  amended by osf-amendment-04-2026-06-14 (cross-classified likelihood)"
scope-decision: "ALL 29 production units (Shawn, 2026-06-18); likelihood re-map = cross-classified (Fork 1, Shawn 2026-06-18)"
---

# H2.1 supplementary wave — launch spec

## 1. Purpose and what this is

The H2.1 primary deconvolution is done and lodged: the cross-classified time × alignment
mixture (`joint_lib.build_model_cross_classified`, `pconv_mode="library"`), refit on the 29
production units under the adopted θ (Amendment 04, `runs/2026-06-13-cc-production-refit/`).
The **supplementary wave** is the bundle of preregistered analyses that the prereg commits
to *reporting alongside* that primary on real data, all currently **staged, not run**. This
spec turns the bundle into one supervised run.

It is the **largest remaining confirmatory-adjacent debt** (`planning/prereg-obligations-audit-2026-06-18.md`
§§4–5). None of the items is itself confirmatory: they are model-comparison cross-checks
(C5, C6), preregistered sensitivities (C10, C11), supporting-consistency checks (H2.2, H2.3,
H2.4), and a reporting requirement (C16). No item gates H3a/H3b/H3c, and none of them can
overturn the primary α attribution — they bound it, contextualise it, and discharge lodged
"reported-alongside" promises.

**What this spec does NOT do:** it does not touch the cross-sectional track (H3a/H3c/SR1),
it does not re-open the primary deconvolution, and it does not run anything to confirmatory
standard. It introduces **two new model builders** (Dirichlet-multinomial and rescaled
negative-binomial, both on the adopted cross-classified likelihood) — that novelty is why
this needs its own spec + pre-launch sign-off (standing rule).

## 2. The lodged obligations (verified against source)

Quotes verified 2026-06-18 against `planning/preregistration-draft.md` (tag
`osf-lodgement-2026-05-20`) and `planning/prereg-obligations-audit-2026-06-05.md` §C.

| ID | Obligation (lodged) | Prereg loc. | Type |
|----|---------------------|-------------|------|
| **C5** | Dirichlet-multinomial supplementary fit, reported alongside for model-comparison; `y_t ~ DirichletMultinomial(N, κ·p_t)`, `κ ~ HalfNormal(prior tuned on pilot fit)`, → multinomial as `κ → ∞` | §3 l.192; §4 l.333 | supplementary (model-comparison) |
| **C6** | Rescaled negative-binomial supplementary fit; `y_t ~ NegativeBinomial(λ_t = N·p_t, φ)`, `1/φ ~ HalfNormal(1)` | §3 l.192; §4 l.333 | supplementary (model-comparison) |
| **C9** | Both supplementaries fit in pymc/NUTS | §3 l.208 | reporting |
| **C10** | Aoristic-MC on the real-data primary: `N_MC ∈ [20,50]` resampled SPAs → primary fit each; cross-realisation α; divergence flag if cross-realisation 95 % α-range > 1.5× primary 95 % CI width; run **only** on the primary, not the DM/NegBin | §3 l.194; §4 l.336 | sensitivity |
| **C11** | Trapezoidal-aoristic sensitivity on **every H3-eligible (level × subset)** + full empire; material if per-subset Pearson r < 0.95, then report alongside uniform | §3 l.167 (Decision 4) | sensitivity |
| **C13 (H2.2)** | Corrected SPA step magnitude reduced ≥ 50 % at template boundaries (BC/AD 0, 100, 200, 300) vs uncorrected | Field 3 l.105; §6 l.403 | supporting consistency |
| **C14 (H2.3)** | Pearson r ≥ 0.9 between genuine-SPAs filtered by `date_range ≤ {25,50,100,200,300}`; bootstrap CI | Field 3 l.107; §6 l.404 | supporting consistency |
| **C15 (H2.4)** | Stratified-by-convention-class SPA vs deconvolved genuine-SPA; agreement within sampling error (internal consistency, not independent validation) | Field 3 l.109; §5 l.376 | supporting consistency |
| **C16** | Mixture α reported as descriptive context for H3a/H3c | §1 l.35; §3 l.229 | reporting |
| **A3** | Design artefact must pin the aoristic-MC `N_MC` value + divergence-flag threshold (and W1 threshold) | §4 l.338 | design artefact |

### 2.1 Fork 1 resolution — re-map onto the cross-classified likelihood

The lodged C5/C6/C10 text was written against a **single multinomial** observation
`y_t ~ Multinomial(N, p_t)`. Amendment 04 (lodged 2026-06-14) replaced the primary
likelihood with the cross-classified two-subset form (`joint_lib.py:349`):

```
w_a        = α·θ_conv + (1−α)·θ_gen
k_cc       ~ Binomial(n_rows, w_a)
y_aligned  ~ Multinomial(k_cc,         p_aligned)
y_nonalign ~ Multinomial(n_rows − k_cc, p_nonalign)
```

A04 is **silent** on the supplementaries, so their mapping is undecided. **Decision (Shawn,
2026-06-18): re-map faithfully onto the cross-classified likelihood** — the overdispersion
enters the two subset count-vectors; α stays identified by the alignment contrast (as in the
adopted primary). The collapsed single-multinomial reading is rejected (it discards the
alignment contrast and so cannot identify α). This is the spirit-faithful translation of the
lodged supplementaries onto the adopted model; it is **documented as such in the results
note**, and flagged for a one-line mention in the next housekeeping amendment (the lodged
DM/NegBin text names a likelihood the primary no longer uses).

## 3. The two new model builders (the novel code)

Both builders **reuse the adopted primary's structural block verbatim** — `α ~ Beta(1,1)`;
`tier_weights ~ Dirichlet(ones(n_lib))`, `p_conv = tier_weights · library_basis`;
non-centred GRW `p_gen`; `θ_conv`, `θ_gen ~ Beta` from `refit_lib.adopted_theta_priors()`
(θ_conv ≈ 0.930, θ_gen ≈ 0.025, κ = 40); the `w_a`, `num_al`, `num_non`, `p_aligned`,
`p_nonalign` deterministics; `ALIGN_RULE = "C"`; `N_BINS = 80`. Only the **observation
terms** change. They live in `code/supp_lib.py` as `build_model_cc_dirichlet_multinomial`
and `build_model_cc_negbin`, importing the shared block from `joint_lib` to guarantee the
structural prior is byte-identical (no copy-paste drift).

### 3.1 C5 — Dirichlet-multinomial (`build_model_cc_dirichlet_multinomial`)

Replace each subset multinomial with a Dirichlet-multinomial sharing **one** concentration
`κ` (matching the single-κ lodged form). The Binomial classification term is **retained**
(the alignment split is a clean per-inscription Bernoulli; the prereg's overdispersion is
*bin-level/compositional*, which is exactly the two subset count-vectors):

```python
kappa = pm.HalfNormal("kappa", sigma=S_KAPPA)        # tuned on pilot (§3.3); → multinomial as κ → ∞
pm.Binomial("k_obs", n=n_rows, p=w_a, observed=k_data)
pm.DirichletMultinomial("y_al_obs",  n=k_data,            a=kappa * p_aligned,  observed=y_al_data)
pm.DirichletMultinomial("y_non_obs", n=n_rows - k_data,   a=kappa * p_nonalign, observed=y_non_data)
```

Optional robustness arm (run only if the pilot's classification PPC shows over-/under-
dispersion in `k_cc`): swap the Binomial for `pm.BetaBinomial`. Default OFF.

### 3.2 C6 — rescaled negative-binomial (`build_model_cc_negbin`)

Per-bin independent negative-binomial on each subset's expected counts, shared dispersion,
exactly the lodged `λ = N·p` parameterisation with `N` = the subset total (avoids the
absolute-scale degeneracy the prereg warns of). The classification term is retained:

```python
inv_phi = pm.HalfNormal("inv_phi", sigma=1.0)        # 1/φ ~ HalfNormal(1), per prereg l.192
phi = pm.Deterministic("phi", 1.0 / inv_phi)
pm.Binomial("k_obs", n=n_rows, p=w_a, observed=k_data)
pm.NegativeBinomial("y_al_obs",  mu=k_data          * p_aligned,  alpha=phi, observed=y_al_data)
pm.NegativeBinomial("y_non_obs", mu=(n_rows-k_data) * p_nonalign, alpha=phi, observed=y_non_data)
```

NB the NegBin does **not** reduce bit-identically to the multinomial (different family by
construction — the prereg frames it as a "cross-check", not a nested model); the sanity
target is α close to primary and large φ (low overdispersion) if the multinomial is adequate.

### 3.3 Pilot-tuning of `S_KAPPA` (prereg-mandated, l.192)

The DM κ prior must be "tuned on pilot fit". Procedure: prior-predictive check on
empire-aggregate at candidate `S_KAPPA` so the prior places mass across κ ∈ ~[10, 1e4]
(weakly informative; does **not** force overdispersion), then one DM pilot fit; record the
κ posterior and set `S_KAPPA` so the prior is dominated by the data. The chosen value, the
prior-predictive figure, and the rationale are written to `outputs/PILOT-REPORT.md` and are
a sign-off item (§9). Default starting point: `S_KAPPA = 1e3` (re-evaluated at pilot).

### 3.4 Smoke tests (must pass before any production fit; standing validation pattern)

1. **DM → multinomial reduction.** Fit `build_model_cc_dirichlet_multinomial` at fixed large
   `κ` (e.g. `κ = 1e6`, clamped) on one small unit; assert the posterior on α, θ, `p_gen`
   matches the primary `build_model_cross_classified` to MCMC noise (same gate as the H3b
   provenance check: |Δα| ≤ 2e-3). This certifies the DM builder is the primary plus
   overdispersion, nothing else.
2. **NegBin large-φ sanity.** Fit `build_model_cc_negbin` with `inv_phi` pinned tiny
   (φ → ∞); assert α within MCMC noise of the primary (NegBin → Poisson → multinomial-
   conditional). Not bit-identical; tolerance ~0.01 on α.
3. **set_data parity.** Both builders expose `k_data`/`y_al_data`/`y_non_data` as `pm.Data`
   (build-once, swap per realisation) — required for C10. Assert a `set_data` swap reproduces
   a fresh-build fit bit-for-bit (the lead's set_data lesson, `joint_lib` docstring).

## 4. Per-item method

Sampling config inherits the primary: **4 chains × (1,000 tune + 2,000 draws)**, `cores=1`
per fit, parallelised across units by the orchestrator. Convergence gate (§7) is applied to
every fit.

- **C5 / C6 model-comparison.** For each in-scope unit, fit the primary (already in hand from
  the refit; re-used, not re-run), DM, and NegBin. Report: (a) PSIS-LOO (`az.compare`) across
  the three families per unit; (b) posterior α side-by-side (median + 95 % CI) — the
  substantive question is whether the family changes the α verdict; (c) the multinomial
  **posterior-predictive dispersion check** on the primary (the prereg's stated trigger for
  preferring DM, l.192) — bin-level variance vs multinomial expectation. Deliverable:
  `outputs/model-comparison.md` + per-unit JSON.
- **C10 aoristic-MC** (primary only, per l.194). Alignment membership is fixed (it depends on
  the recorded interval + `ALIGN_RULE`, not on the sampled date), so `k_cc` and `n_rows` are
  **held constant** across realisations; only the within-subset bin assignment varies. Per
  realisation r ∈ 1..N_MC: sample `t_i ~ Uniform(nb_i, na_i)` per inscription (year-precise
  `[t,t]` fixed), bin to the 5-y grid within each alignment subset → `(y_aligned_r,
  y_nonaligned_r)`; fit the primary via `set_data`. Cross-realisation α = pooled draws across
  realisations (equally weighted). **Divergence flag:** cross-realisation 95 % α-range >
  1.5× the primary single-SPA 95 % CI width → reported as a material limitation (not an
  amendment trigger). Deliverable: `outputs/aoristic-mc.md` with the flag per unit.
- **C11 trapezoidal.** Re-derive the aoristic SPA with trapezoidal (boundary-tapered)
  apportionment per H3-eligible subset + full empire; (a) input-level Pearson r vs the
  uniform SPA; (b) refit and output-level Pearson r between the trapezoidal- and uniform-
  input deconvolved `p_gen`. Material if either r < 0.95 → report trapezoidal alongside.
  (Empire is already known to be r = 0.94 < 0.95 at the input level — `runs/2026-05-17-empirical-spa-shape/`
  — so empire reporting-alongside is pre-triggered; this run discharges it formally and
  extends it per-subset.) Deliverable: `outputs/trapezoidal.md`.
- **H2.2 (C13).** Read-off, no new MCMC: for each unit compare the step magnitude `|Δ|`
  across each template-boundary bin (BC/AD 0, AD 100, 200, 300) in the deconvolved corrected
  SPA (posterior `p_gen`) vs the raw uncorrected SPA; report the % reduction and the fraction
  of units meeting ≥ 50 %. Deliverable: `outputs/h2.2-boundary-steps.md`.
- **H2.3 (C14).** For each unit, refit on the corpus filtered to `date_range ≤ T` for
  `T ∈ {25,50,100,200,300}`; extract deconvolved `p_gen_T`; pairwise Pearson r across
  thresholds with a city/inscription bootstrap CI. Rule: r ≥ 0.9. Units that fall below the
  reachability floor (§6) at tight T are caveated, not failed. Deliverable:
  `outputs/h2.3-threshold-convergence.md`.
- **H2.4 (C15).** Compute the SPA of the genuine-classed strata (Tight + year-precise) and of
  the convention-classed strata directly; compare to the model's deconvolved `p_gen` within a
  bootstrap sampling-error band. Internal-consistency framing (not independent validation).
  Deliverable: `outputs/h2.4-stratified.md`.
- **C16.** Tabulate per-unit and empire/Latin α (median + 95 % CI) from the refit as
  descriptive context. Read-off from `runs/2026-06-13-cc-production-refit/outputs/refit-summary.json`.
  Deliverable: folds into `outputs/REPORT.md`.

## 5. Design-artefact pins (A3 — pinned here)

- **N_MC = 30** (mid-range of the lodged [20, 50]; the pilot confirms 30 realisations give a
  stable cross-realisation α band on empire before the full sweep — if the band is still
  moving at 30, escalate to 50 and report).
- **Divergence-flag threshold = 1.5×** (lodged value; cross-realisation 95 % α-range vs
  primary 95 % CI width).
- **W1 flagging threshold** (Wasserstein-1, shape): inherit the recovery-grid value already
  pinned for H2.1 validation (`runs/2026-05-26-recovery-grid-two-unit/`); re-state in
  `outputs/REPORT.md`, do not re-derive.

## 6. Scope — all 29 production units

Per Shawn (2026-06-18): the full uniform table. The 29 units are
`refit_lib.enumerate_refit_units()` (empire-aggregate, latin-aggregate, Italia-excl-Rome, and
the 26 Latin-frame province/city units; Roma excluded per Decision 36 / Obs 101). Frame:
the **Latin diagnostic frame is primary** (Obs 101, A02-lodged); empire-aggregate is reported
as baseline/context.

- **C5/C6/C16:** all 29.
- **C10:** all 29 (N_MC = 30 each).
- **C11:** all H3-eligible (level × subset) + full empire — here = all 29.
- **H2.2/H2.3/H2.4:** all 29.

**Reachability floor** (Decision 34 / Amendment 01 §A5.7, worst-case N ≈ 2,000): units below
the floor — and any unit dropping below it under tight H2.3 date filters — are **caveated,
not excluded** (flag in the per-item table). This honours Martin's "the data we have is the
data we have" and the prereg's reachability convention.

## 7. Convergence and diagnostic gates

Per fit: **R̂ < 1.01** on all parameters; **ESS ≥ 400** per chain on α and `tier_weights`;
benign-divergence treatment (Amendment 01 — divergences reported, not zero-tolerance). Re-use
`cell_lib.convergence_pass`. For these **non-confirmatory** items, a diagnostic failure is
reported as a per-unit limitation (and the unit caveated) rather than auto-triggering an OSF
amendment — but every failure is surfaced explicitly in the per-item table and the run
VERDICT, never silently dropped.

## 8. Orchestration, compute, and the halt-and-report rule

- **Host:** sapphire, via SSH; workdir `~/Code/inscriptions` (standing rule). `uv` at
  `~/.local/bin/uv`. Inherit the cgroup/`TMPDIR`/worker-recycling infra proven on the cc grid
  (`systemd-run --user` scope, `MemoryMax`, spawn + `max_tasks_per_child`, root-fs `TMPDIR`).
- **Measured baseline:** the primary 29-unit refit = **1,913 core-s total** (empire 313.7 s,
  latin 174.7 s, mean 66 s; `refit-summary.json`).
- **Estimated wave cost (all 29):** DM ≈ 1.1 + NegBin ≈ 1.1 + aoristic-MC (29 × 30) ≈ 16 +
  H2.3 (29 × 5) ≈ 1.3 + C11 ≈ 0.5 + read-offs ≈ 0.3 ≈ **~20 core-hours → wall ~3–5 h** at
  `n_jobs` 8–12. The DM/NegBin ×2 multiplier is an **estimate**; the pilot replaces it with a
  measured per-fit cost (§9). Aoristic-MC dominates (~80 %).
- **Halt-and-report (standing rule):** do **not** silently reduce N_MC, draws, chains, or unit
  count to fit a time budget. If the pilot-measured full-wave cost exceeds ~8 h wall, **halt
  and report** with the measured numbers; Shawn decides (accept the longer run, stage it, or
  trim scope). Two prior incidents make this a hard rule.

## 9. The pilot gate (prereg-mandated; precedes the production run)

The pilot is **not optional** — the prereg mandates κ-tuning on a pilot (l.192). The pilot:

1. Builds `supp_lib.py`; passes the three §3.4 smoke tests (reduction, large-φ sanity,
   set_data parity).
2. Fits DM + NegBin on **empire-aggregate + one mid-size unit** (e.g. Latium/Regio I);
   records measured per-fit wall time, convergence, κ posterior, the chosen `S_KAPPA`, and the
   multinomial PPC dispersion result.
3. Runs aoristic-MC at N_MC = 30 on **empire only**; confirms the cross-realisation α band is
   stable (and projects the full-29 aoristic-MC cost from the measured per-realisation time).
4. Writes `outputs/PILOT-REPORT.md`.

**The full production run does not launch until the pilot report is signed off** (a quick
review of: smoke-tests-pass, κ choice, measured cost vs the §8 budget, no convergence
surprises). This is the pre-launch sign-off gate.

## 10. Pre-launch sign-off checklist (for Shawn)

Sign off on **§§3–4** (the two builders + per-item method) to authorise the **build + smoke +
pilot** (cheap; minutes of compute). The **full production run** is then separately gated on
the **pilot report (§9)**.

- [ ] Fork 1 re-map (§2.1) — cross-classified, Binomial classification retained, shared κ / φ.
- [ ] Builder definitions (§3.1, §3.2) and the smoke-test gates (§3.4).
- [ ] Design-artefact pins (§5): N_MC = 30, divergence 1.5×.
- [ ] Scope (§6): all 29, Latin-primary frame, reachability-floor caveat.
- [ ] Diagnostic gate + non-confirmatory failure handling (§7).
- [ ] Halt-and-report budget (§8): ~8 h wall ceiling before re-consulting.

## 11. Deliverables and provenance

- Code: `code/supp_lib.py` (builders), `code/run_supp.py` (orchestrator), `code/smoke_supp.py`.
- Outputs: `PILOT-REPORT.md`, `model-comparison.md`, `aoristic-mc.md`, `trapezoidal.md`,
  `h2.2-boundary-steps.md`, `h2.3-threshold-convergence.md`, `h2.4-stratified.md`, and the
  integrating `REPORT.md` + per-unit JSON. Idata `.nc` are gitignored (regenerable; kept on
  sapphire), per the H7-Latin precedent.
- Commit before each stage (standing rule). The wave's results discharge audit items
  C5/C6/C10/C11/C13–C16; on completion, flip them in `planning/prereg-obligations-audit-2026-06-18.md`
  (mark-not-delete) and log an Obs.
