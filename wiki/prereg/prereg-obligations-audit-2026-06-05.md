---
title: "Preregistration obligations completeness audit"
date: 2026-06-05
author: "Claude Code (Opus 4.8, 1M context) under Shawn Ross's direction"
scope: "Extract EVERY committed obligation from planning/preregistration-draft.md and assign a status by cross-referencing the decision log, OSF Amendment 01, OSF Amendment 02 (pending, Decision 36), the H3a confirmatory run, the §5 Layer-A run, the two-unit recovery grid, and the backlog."
authoritative-source: "planning/preregistration-draft.md (lodged 2026-05-20, git tag osf-lodgement-2026-05-20)"
status-legend: "DONE | PENDING-PLANNED | SUPERSEDED-BY-AMENDMENT (01 lodged / 02 pending) | UNACCOUNTED | UNCLEAR"
---

# Preregistration obligations completeness audit (2026-06-05)

> **STATUS SUPERSEDED (2026-06-18):** see `prereg-obligations-audit-2026-06-18.md`
> for the current status picture. This file remains the durable **per-item**
> register (prereg line refs, types, A–I structure); its SUMMARY and amendment
> (I) section are stale — e.g. H3c(i) closed 2026-06-05, D11/D12/B4 resolved
> 2026-06-16, and **all four amendments 01–04 are now lodged** (this file predates
> 03/04 and wrongly lists 02 as pending).

**Purpose.** Make sure no preregistered obligation is missed as the project moves
into the H2.1 mixture run and the H3 substantive analyses. Every committed
obligation in `planning/preregistration-draft.md` is extracted, typed, and given
a status with an artefact citation. The audit reads the lodged prereg as the
obligations source; status is assigned against the living repository.

**Cross-reference set (re-read this turn).**

- `planning/preregistration-draft.md` (the lodged prereg; obligations source).
- `planning/decision-log.md` Decisions 1–36 (Decision 36 → OSF Amendment 02, pending).
- `planning/osf-amendment-2026-05-29-two-measure-framework.md` (Amendment 01, lodged 2026-06-04).
- `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md` and `…/REPORT-latin-h3c-sr1.md`.
- `runs/2026-05-30-s5-small-n-trajectories/RESULTS.md` (§5 Layer A).
- `runs/2026-05-26-recovery-grid-two-unit/` (the recovery validation, two-unit) and `runs/2026-05-22-recovery-grid-design/` (the recovery-grid design artefact).
- `planning/h3a-design-artefact-2026-06-04.md` (H3a PPC / prior-predictive thresholds).
- `planning/backlog-2026-05-03.md`.

**One global caveat on status.** "DONE" for any H3a/H3c/SR result means *executed
and reported as PRELIMINARY* — the H3a REPORT and Latin H3c/SR1 REPORT both carry
explicit "pending Shawn's sign-off" / "pending OSF Amendment 02" labels. None is a
final confirmatory claim yet. Decision 36 (Latin-province primary frame) is
amendment-gated: no Latin-primary confirmatory claim leaves the repository until
Amendment 02 is lodged.

---

## A. CROSS-CUTTING — design artefacts, conventions, multiplicity, software

### A1. Pre-Phase-2 design artefact — recovery-grid values
- **Quote / loc.** "specific values are pinned in a pre-Phase-2 design artefact at `runs/2026-05-XX-recovery-grid-design/` (committed before any recovery simulation runs)" (§3 line 151; §4 lines 325, 435).
- **Type.** design-artefact.
- **Status.** DONE — `runs/2026-05-22-recovery-grid-design/` (design.json: α grid {0.05,0.30,0.50,0.70,0.95}; 6 shapes; 5 tier-weight vectors; N; 100 reps/cell; seed policy). Binds Decisions 19/20/21.

### A2. Pre-Phase-2 design artefact — template-dictionary empirical scan
- **Quote / loc.** "The dictionary contents are pinned by a pre-Phase-2 empirical scan committed to a named `runs/2026-05-XX-template-dictionary/` directory before the Bayesian mixture fits; the scan enumerates exact-match interval templates in the LIRE v3.0 corpus and includes any template with N ≥ a stated threshold" (§3 line 202; Decision 20).
- **Type.** design-artefact.
- **Status.** **UNACCOUNTED** — no `runs/*template-dictionary*` directory exists. The recovery-grid-design spec (`runs/2026-05-22-recovery-grid-design/spec.md`, lines ~117–121) explicitly states "no mixture fit has yet been run on real LIRE data under the Decision-20 three-tier structure (the only mixture fit to date is the one-tier talk demo)," and the recovery grid's tier basis uses **synthetic / proxy** slab vectors (`pilot_proxy = (0.55,0.30,0.15)`), not an empirically-scanned dictionary. The empirical template-dictionary scan on real LIRE — the thing that pins the convention component's actual interval contents and the N-threshold — is still outstanding and is a prerequisite for the real-data H2.1 mixture fit. **Bears directly on the H2.1 mixture run.**

### A3. H3a/PPC design artefact — numerical PPC + prior-predictive thresholds
- **Quote / loc.** "The same `runs/2026-05-XX-recovery-grid-design/` design artefact also pins the numerical PPC thresholds … the Wasserstein-1 flagging threshold … the aoristic-MC N_MC value and divergence-flag threshold, and the two-tier severity cutoffs (critical / minor) per PPC category." (§4 line 338; §3 lines 251, 265; Decisions 25/30.)
- **Type.** design-artefact.
- **Status.** PARTIAL — the **H3a-cross-sectional** PPC + prior-predictive thresholds are pinned in `planning/h3a-design-artefact-2026-06-04.md` (committed before the H3a fit; categories #1–#10 with 1.5×/2× severity). The **recovery-grid Wasserstein-1 flagging threshold** is handled in Amendment 01 §A5.5.1 (T_flat = 10 y). The **aoristic-MC N_MC + divergence-flag threshold** is NOT pinned anywhere — see G3 (UNACCOUNTED for the aoristic-MC supplementary as a whole). So the design-artefact pinning is complete for everything *except* the aoristic-MC parameters.

### A4. Calendar / binning conventions
- **Quote / loc.** "5-year bins across the 50 BC – AD 350 envelope (80 bins)" (§3 line 169); inclusive-Roman century counting (§2, Decisions 17/20); BC/AD boundary (no year 0) flagged as known limitation (§9 line 444).
- **Type.** reporting-requirement / convention.
- **Status.** DONE — 80-bin 5-year grid used throughout (recovery-grid design.json envelope; §5 run; H3a date-window filter). BC/AD boundary step retained as a known limitation (not modelled as a tier — see C-series).

### A5. Multiple-comparison / Holm policy for the confirmatory family
- **Quote / loc.** H3a/H3c judged "independently, not as an omnibus family" (Field 3 lines 86–92); H3b forms no Holm-corrected confirmatory family (line 91, Decision 15); H3c is two independent tests (Decision 16). Amendment 01 §A5.3: each measure forms its own family, no cross-unit correction.
- **Type.** reporting-requirement.
- **Status.** DONE (policy) — the policy is settled: no omnibus family; H3a, H3c(i), H3c(ii) each independent; H3b exploratory with multiplicity "noted descriptively." No Holm correction is actually owed for the current confirmatory set. Confirm the H3b descriptive-multiplicity note is honoured when H3b runs (see E-series).

### A6. Uncertainty-quantification table (interval type per analysis)
- **Quote / loc.** §3 "Uncertainty quantification" table (lines 287–297) — Wilson CI (Phase 1); MC envelope (H3b); posterior CIs (H2.1, H3a, H3c); bootstrap (H2.3).
- **Type.** reporting-requirement.
- **Status.** DONE where analyses are done (H3a/H3c report posterior CIs per spec); PENDING for H2.3 bootstrap / H3b envelope (those analyses pending).

### A7. Software / reproducibility commitments
- **Quote / loc.** §8 — Python 3.13 primary; R 4.4.3 brms shadow + baorista; pinned requirements.txt; public repo at `github.com/saross/inscriptions`; per-stage `runs/` directories; canonical seed 20260425 (Phase 1); design artefact committed before Phase 2; lodgement git tag `osf-lodgement-2026-05-20`.
- **Type.** reporting-requirement / reproducibility.
- **Status.** DONE (infrastructure) — per-stage run dirs are the project norm; tag exists; Amendment 01 adds tag `osf-amendment-01-2026-06-04`.

### A8. Phase 2 Dockerfile + Zenodo archival
- **Quote / loc.** §8 reproducibility commitment (and backlog: "Phase 2 Dockerfile + Zenodo archival (GH issue #3). Mandated at paper submission").
- **Type.** reporting-requirement.
- **Status.** PENDING-PLANNED — backlog item, "Revisit at paper submission." On track (not yet due).

### A9. Aoristic implementation note (direct numpy, not tempun)
- **Quote / loc.** §3 line 167; §8 line 430 — Uniform aoristic implemented directly (≤10 lines numpy), tempun excluded (numpy ≥2.4 incompat), upstream issue filed.
- **Type.** reporting-requirement.
- **Status.** DONE — `primitives.py::aoristic_resample`; documented in §8.

---

## B. PHASE 1 — completed groundwork (fixed; not confirmatory)

### B1. Minimum-sample-size thresholds across empire/province/urban-area
- **Quote / loc.** §6 effect-size table Phase-1 rows (lines 406–410); §4 lines 302–321.
- **Type.** confirmatory-gate (completed groundwork) / reporting-requirement.
- **Status.** DONE — `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`; thresholds pinned in §6; FP control across all 96 zero-effect cells ([0.007, 0.049]).

### B2. CPL knot-sensitivity (k ∈ {2,3,4}) — exploratory supplementary
- **Quote / loc.** §3 line 179; §5 line 355; §6.
- **Type.** exploratory/optional (Phase 1 supplementary).
- **Status.** DONE for Phase 1 (k=2 dropped per Decision 9/10; k=3 vs k=4 reported in H1 v2 §5). Optional re-run on real LIRE post-H2 (backlog) — PENDING-PLANNED (optional).

### B3. CPL AIC-select threshold — exploratory supplementary
- **Quote / loc.** §5 line 356; §3 line 179 ("AIC-selected results are reported in supplementary material and do not substitute for the fixed-k=3 confirmatory result").
- **Type.** exploratory/optional.
- **Status.** DONE for Phase 1 (k=3 wins 73%, k=4 27%, per backlog/H1 v2). Not applicable downstream.

### B4. Stratified-sampling sensitivity (Phase 1 supplementary)
- **Quote / loc.** §5 line 357 — "thresholds are recomputed using stratified-sampling (province-proportional or city-proportional draws). Reports deltas to bootstrap primary."
- **Type.** sensitivity (Phase 1 supplementary).
- **Status.** **RESOLVED 2026-06-16 — SUPERSEDED-BY-Decision-8, satisfied via a width-pool check** (`runs/2026-06-16-s5-sensitivities/`, commits `6acfddf`/`6b2a14a`). The prereg's stratified-*bootstrap* of LIRE is architecturally moot for the committed v2 thresholds: **Decision 8 replaced the LIRE bootstrap with synthetic data drawn from a parametric null** (`h1_sim_v2.py`), so the only empirical lever on the thresholds is the interval-width pool, and the per-iteration province/city counts are vestigial (zero effect on detection). The v2-faithful B4: scheme (a) proportional-allocation is **threshold-neutral by construction**; scheme (b) reweight-to-balance shifts the width pool (city-balanced median interval width 99 y → 79 y), but a threshold re-run under global / province-balanced / city-balanced width pools found the Phase-1 detection thresholds **robust** (median Δ −1.1 % province / −0.4 % city, within Monte-Carlo noise; 0 reachability classifications changed). *(Original 2026-06-05 status was **UNACCOUNTED** — no run existed at audit time.)*

---

## C. PHASE 2 — H2.1 mixture validation (recovery simulation) + observation model

### C1. H2.1 confirmatory recovery simulation — α coverage + shape recovery
- **Quote / loc.** Field 3 H2.1 (line 61); §3 "Validation" (line 210); §4 (lines 323–334); §6 (lines 395–396). Binding rule: ≥90% cells α-coverage AND posterior-median Pearson r ≥ 0.95 in ≥90% cells.
- **Type.** confirmatory.
- **Status.** SUPERSEDED-BY-AMENDMENT 01 (§A5.5.1) **and** DONE under the corrected criterion. Two-unit grid at `runs/2026-05-26-recovery-grid-two-unit/`: **Grid A (inscription) PASS, B = A = 98.6%**; **Grid B (letter) FAIL** (R̂/ESS, not divergences). The lodged binding criterion was corrected (flat-shape Wasserstein-1 patch T_flat=10y; α demoted to a shape-conditioned diagnostic, LoA ≈ [−0.22,+0.17]; operating envelope α ≤ 0.70). Caveat: the grid ran on **synthetic** convention bases, not the empirically-scanned template dictionary (see A2) — the *validation* is done, but the real-data fit still needs the dictionary.

### C2. Wasserstein-1 supplementary shape metric (per cell)
- **Quote / loc.** §3 line 210; §4 line 334; §6 line 396 — "Wasserstein-1 (Earth Mover's distance) reported as a supplementary distribution-sensitive shape metric per cell against a design-artefact-pinned flagging threshold." Decision 27.
- **Type.** supplementary / reporting-requirement.
- **Status.** DONE — W1 stored per cell in the recovery grid; promoted to the binding gate for the flat shape only (Amendment 01 §A5.5.1); reported supplementary for all shapes.

### C3. Convergence diagnostics (R̂ < 1.01; ESS ≥ 400; no divergences)
- **Quote / loc.** §3 "Fit" line 208 — "Gelman-Rubin R̂ < 1.01 on all parameters; effective sample size ≥ 400 per chain on α and tier weights; no divergences. Failure of any diagnostic triggers an OSF amendment."
- **Type.** amendment-trigger / reporting-requirement.
- **Status.** DONE / refined by Amendment 01 — the "no divergences" zero-tolerance clause was relaxed to a field-standard benign-divergence treatment (Decision 33 update 2026-06-04; Amendment 01 §A5.5.1). R̂/ESS gates unchanged. No amendment-triggering convergence failure on the inscription grid; the letter grid's R̂/ESS failure is the basis of the Grid B FAIL verdict (handled within Amendment 01).

### C4. Multinomial primary observation model
- **Quote / loc.** §3 lines 181–192 — `y ~ Multinomial(N_eff, p)` is "the binding primary likelihood." Decision 19.
- **Type.** confirmatory.
- **Status.** DONE — `cell_lib.build_model_f1_f3` (multinomial; learned Dirichlet tier weights; non-centred GRW p_gen; α~Beta(1,1) per F1). Confirmed the production model (Decision 35). NB minor prior refinement Beta(2,2)→Beta(1,1) (Δα≈+0.025) noted as amendment-consistent (Decision 35).

### C5. Supplementary fit (a) — Dirichlet-multinomial (model-comparison)
- **Quote / loc.** §3 line 192 — "`y_t ~ DirichletMultinomial(N, κ · p_t)` … reported alongside for model-comparison"; §2 line 149; §4 line 333; Decision 19.
- **Type.** supplementary.
- **Status.** **UNACCOUNTED** — no Dirichlet-multinomial fit exists in the recovery-grid code (`cell_lib.py` defines only the multinomial `build_model_f1_f3`) or anywhere else. The prereg says the recovery simulation "is run under all three likelihoods" (Decision 19 consequences; §4 line 333: "multinomial primary; Dirichlet-multinomial and rescaled-NegBin supplementaries reported alongside") and §2/§3 commit to reporting both supplementaries alongside the real-data primary. Neither has been built. **Bears on the H2.1 mixture run.**

### C6. Supplementary fit (b) — rescaled negative-binomial (model-comparison)
- **Quote / loc.** §3 line 192 — "`y_t ~ NegativeBinomial(λ_t = N · p_t, φ)` … cross-check on Option C"; §2 line 149; §4 line 333; Decision 19.
- **Type.** supplementary.
- **Status.** **UNACCOUNTED** — same as C5; not implemented. **Bears on the H2.1 mixture run.**

### C7. Convention component — template-interval slab structure (3 tiers)
- **Quote / loc.** §3 lines 196–202 (century / half-century / reign tiers); Decision 20.
- **Type.** confirmatory (model structure) / design-artefact.
- **Status.** PARTIAL — the three-tier *structure* is implemented in the recovery grid (synthetic basis). The *empirical pinning* of tier contents (template dictionary, A2) is UNACCOUNTED. Year-precise [t,t] inscriptions excluded from convention (stays in genuine) — design honoured in synth.

### C8. Genuine component — GRW smoothness prior; weakly-informative bandwidth
- **Quote / loc.** §3 lines 204–206 — "Gaussian random-walk smoothness prior and a weakly-informative bandwidth"; priors α~Beta(2,2), tier weights ~Dirichlet(uniform), σ~HalfNormal(1).
- **Type.** confirmatory (model structure).
- **Status.** DONE (structure) — zero-mean non-centred GRW in `build_model_f1_f3`. Prior refinement Beta(2,2)→Beta(1,1) per Decision 35 (amendment-consistent). KNOWN LIMITATION carried forward (Amendment 01 §A5.7): GRW band overconfident for sharp/peaked signals and degrades with N — reported as a limitation, median timeline is the gated quantity.

### C9. Posterior sampling via pymc (NUTS) for all three likelihoods
- **Quote / loc.** §3 "Fit" line 208 — "Posterior sampling via pymc … The Dirichlet-multinomial and rescaled NegBin supplementaries are also fit in pymc."
- **Type.** confirmatory / reporting-requirement.
- **Status.** PARTIAL — pymc NUTS for the multinomial: DONE. For the two supplementaries: UNACCOUNTED (follows C5/C6).

### C10. Aoristic-MC supplementary on the real-data primary multinomial fit
- **Quote / loc.** §3 line 194 ("Aoristic-uncertainty sensitivity (supplementary)"); §4 line 336; §6 line 401; Decision 28. N_MC ∈ [20,50] independently-sampled aoristic SPA realisations; cross-realisation α posterior; divergence flag at 1.5× primary CI width.
- **Type.** sensitivity (supplementary; preregistered; not an amendment trigger by itself).
- **Status.** **UNACCOUNTED** — no aoristic-MC supplementary run exists; the N_MC value and divergence-flag threshold are not pinned in any design artefact (A3). The only "aoristic_mc" code hit is the Phase-1-era `experiment_aoristic_mc.py` (a rejected Phase-1 MC mechanism, unrelated). **Bears on the H2.1 mixture run** — it is run on the real-data primary multinomial fit, so it should be folded into the H2.1 launch spec.

### C11. Trapezoidal-aoristic sensitivity (per H3-eligible subset + full empire)
- **Quote / loc.** §3 line 167 — trapezoidal "is run as a sensitivity analysis on **every (level × subset) combination eligible for H3 confirmatory testing** … plus the full-empire SPA"; convergence assessed by Pearson r per subset; material if r < 0.95, in which case trapezoidal reported alongside uniform. Decision 4.
- **Type.** sensitivity (supplementary; preregistered).
- **Status.** PARTIAL / at-risk — a trapezoidal SPA was computed and validated **only on the full-empire SPA** as a diagnostic (`runs/2026-05-17-empirical-spa-shape/`: per-bin Pearson r = 0.94, max rel diff 47.6%). Note that the empire r = 0.94 is **below 0.95**, which under the prereg rule makes the trapezoidal "material" at empire level and obliges reporting it alongside the uniform primary. The per-eligible-subset trapezoidal sensitivity (the H3b-confirmatory-eligible subsets) is NOT done and is not in any plan/decision I can find. Flag: the empire-level r < 0.95 result already triggers the "report alongside" obligation.

### C12. Prior-predictive checks for the mixture (numerical, design-artefact-pinned)
- **Quote / loc.** §3 line 210 references validation; PPC/prior-predictive machinery is specced mainly for H3a (line 251) but the design artefact (§4 line 338) pins "prior 99th-percentile count cap" etc. as part of one artefact.
- **Type.** PPC / design-artefact.
- **Status.** N/A-for-mixture / UNCLEAR — the prereg's prior-/posterior-predictive *numerical* PPC categories are written for the H3a NBR, not the mixture. The mixture's own check is the recovery-simulation coverage + Wasserstein. No separate mixture PPC obligation beyond the recovery grid + convergence diagnostics is owed. (Recorded for completeness; not a gap.)

### C13. H2.2 — boundary-step reduction in corrected SPA (real data)
- **Quote / loc.** Field 3 line 105; §6 line 403 — corrected step magnitude reduced ≥50% at template boundaries (0,100,200,300) vs uncorrected.
- **Type.** supplementary (supporting consistency, real data).
- **Status.** PENDING-PLANNED — depends on the real-data mixture fit (not yet run; backlog "H2 mixture-model implementation"). Bears on H2.1 mixture run (this is reported off the same real-data fit).

### C14. H2.3 — genuine_SPA convergence across date-range thresholds
- **Quote / loc.** Field 3 line 107; §6 line 404 — Pearson r ≥ 0.9 between any two SPAs filtered by date_range ≤ {25,50,100,200,300}.
- **Type.** supplementary (supporting consistency, real data); bootstrap CI per §3 UQ table.
- **Status.** PENDING-PLANNED — depends on real-data mixture fit. (Diagnostic precursor exists at `runs/2026-05-17-date-range-filtered-spas/` but that is uncorrected-SPA diagnostics, not the H2.3 corrected-genuine_SPA convergence test.)

### C15. H2.4 — stratified-by-convention-class SPA vs deconvolved (real data)
- **Quote / loc.** Field 3 line 109; §5 line 376; §6 line 405 — agreement within sampling error; reported as internal-consistency, not independent validation.
- **Type.** supplementary (supporting consistency, real data).
- **Status.** PENDING-PLANNED — depends on real-data mixture fit; backlog "§5 stratified-by-convention-class SPA."

### C16. Mixture empire-level α reported as descriptive context (for H3a/H3c)
- **Quote / loc.** §1 line 35; §3 line 229; Decision 22; Decision 35 addendum.
- **Type.** reporting-requirement.
- **Status.** PENDING-PLANNED — owed once the real-data empire mixture fit runs; H3a/H3c do not gate on it. Decision 35 addendum confirms H3a's input is date-window counts, not mixture output (correctly honoured in the H3a run).

---

## D. PHASE 3 — H3a (primary confirmatory) + its supplementaries

### D1. H3a within-between (Mundlak) NBR — f_within three-way verdict
- **Quote / loc.** Field 3 line 65; §3 lines 212–249; §6 line 397; Decisions 12/18/22.
- **Type.** confirmatory (sole primary).
- **Status.** DONE (preliminary) — `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md`: f_within 0.299 [0.240, 0.365], **SUPPORTED** (empire frame). Latin frame (Sensitivity B → Decision 36 primary): 0.480 [0.401, 0.566], SUPPORTED. PRELIMINARY (sign-off pending; Latin frame amendment-gated → Amendment 02).

### D2. Posterior-probability ladder P(f>0.05/0.10/0.20)
- **Quote / loc.** Field 3 line 71; §3 line 247; §6 line 397; Decision 18.
- **Type.** supplementary / reporting-requirement (binding alongside verdict).
- **Status.** DONE — all three rungs reported (1.000 / 1.000 / 1.000 empire).

### D3. Three-weighting sensitivity for f_within (unweighted primary + pop- + insc-weighted)
- **Quote / loc.** §3 line 241; §5 line 354; §6 line 397; Decision 32.
- **Type.** sensitivity (§5 exploratory).
- **Status.** DONE — H3a REPORT §1: population-weighted 0.494 [0.395,0.609]; inscription-weighted 0.419 [0.335,0.514]; both SUPPORTED, reported alongside unweighted primary. (Material-divergence flag check: the three are reported; spread vs primary-CI-width not explicitly flagged but all SUPPORTED.)

### D4. Bayesian R² (Gelman et al. 2019; latent-scale; cross-checked vs brms::bayes_R2)
- **Quote / loc.** §3 line 249; §6.
- **Type.** reporting-requirement.
- **Status.** DONE — response-scale 0.133 [0.091,0.201] (matches brms 0.136); latent-scale 0.473 [0.434,0.509].

### D5. OLS log-log comparator (SR1; vs Hanson, Ortman & Lobo 2017 / Hanson 2021)
- **Quote / loc.** Field 3 SR1 line 49; §3 line 249; §4 line 344.
- **Type.** reporting-requirement (descriptive comparator) / SR1.
- **Status.** DONE — empire OLS slope 0.284 [0.195,0.373] R²0.036; Latin SR1 0.505 [0.398,0.611] R²0.096 (`REPORT-latin-h3c-sr1.md`). Latin frame amendment-gated.

### D6. Between-province component reported descriptively
- **Quote / loc.** §3 lines 233, 249; §9 line 449 — reported but flagged not separately identifiable.
- **Type.** reporting-requirement.
- **Status.** DONE — β_between −0.242 [−0.701,0.238] (crosses 0), reported with the §9 caveat.

### D7. Prior-predictive checks (numerical, design-artefact-pinned)
- **Quote / loc.** §3 line 251; Decision 25; design artefact §2.
- **Type.** PPC / design-artefact.
- **Status.** DONE — `h3a-design-artefact-2026-06-04.md` §2; thresholds committed BEFORE the fit (`prior-predictive-thresholds.json`); prior-sanity gate (median count 1.0) PASSED.

### D8. Posterior-predictive checks — 8-category suite incl. 8th = posterior-predictive Moran's I
- **Quote / loc.** §3 lines 253–258 (density overlay; test stats; residual structure; PP Moran's I); Decisions 25/29; two-tier severity Decision 30.
- **Type.** PPC.
- **Status.** DONE — H3a REPORT §5: 10 checks run (covers all categories incl. #10 PP Moran's I k=8). Verdict MINOR (0 critical, 5 minor, 5 pass); no HALT, no revision, no amendment. The 8th PPC (PP Moran's I) PASSES (obs −0.002 within pp [−0.024,+0.024]) → no tautology caveat on H3c(ii).

### D9. pymc ↔ brms shadow cross-validation
- **Quote / loc.** §3 line 267 — "Secondary brms-via-R cross-validation shadow … `scripts/h3a_brms_shadow.R`"; material disagreement on H3a verdict triggers OSF amendment.
- **Type.** confirmatory cross-check / amendment-trigger.
- **Status.** DONE — `h3a_brms_shadow_mundlak.R` (run-local Mundlak shadow). β_within/f_within match to 3–4 sig figs; "No material disagreement." Amendment trigger NOT fired. NOTE: the *committed* `scripts/h3a_brms_shadow.R` still fits the pooled pre-Mundlak model; the run-local Mundlak script is the one that matched the estimands (documented in REPORT §6). Minor housekeeping: the committed script does not match the confirmatory spec.

### D10. Standardisation sensitivity (exploratory)
- **Quote / loc.** §3 line 231 — "Sensitivity to standardisation is reported as an exploratory check."
- **Type.** exploratory/optional.
- **Status.** DONE — Sensitivity C: f_within 0.298 (matches 0.299); β stability confirmed.

### D11. Hanson-population measurement-error sensitivity (σ_pop ∈ {0.1,0.2,0.3})
- **Quote / loc.** §5 line 352; Decision 26 (B9). Re-run H3a with lognormal ME on log_pop; report f_within per σ_pop; material divergence flagged (no amendment).
- **Type.** sensitivity (§5 exploratory).
- **Status.** **UNACCOUNTED** — not run; not in the H3a confirmatory REPORT and not in any follow-up plan I can find. Pre-specified §5 sensitivity with no artefact. (Cheap: re-fit H3a with a measurement-error layer.)

### D12. Scaling-residual sensitivity for H3a
- **Quote / loc.** §5 line 380 — compute per-city residuals from a fitted power-law inscriptions∝pop^β; re-run H3a on residuals.
- **Type.** sensitivity (§5 exploratory).
- **Status.** **UNACCOUNTED** — not run; backlog item only ("§5 scaling-residual sensitivity for H3a … Revisit with H3a").

### D13. α-as-translator sensitivity for H3a (N ≥ 100 cities)
- **Quote / loc.** §5 line 382 — include per-city posterior mixture α as an NBR covariate; restricted to ~200 cities with N ≥ 100.
- **Type.** sensitivity (§5 exploratory).
- **Status.** PENDING-PLANNED — requires per-city mixture α (depends on the real-data mixture; per-city α only identifiable for N ≥ 100). Backlog "§5 α-as-translator sensitivity … after H2 produces α." Not yet runnable (needs mixture).

### D14. H3a flexible-dispersion refinement (future improvement)
- **Quote / loc.** Not a prereg obligation — Decision/backlog item (2026-06-05) arising from the PPC minor caveat (single-dispersion NBR under-fits heavy upper tail).
- **Type.** exploratory/optional (NOT prereg-committed).
- **Status.** PENDING-PLANNED — backlog Phase-3 item; report as a sensitivity after the Latin H3a is finalised. Logged so it is not mistaken for a missed obligation: it is a *new* optional improvement, not a prereg commitment.

---

## E. PHASE 3 — H3b (pre-specified exploratory deviation-detection)

### E1. H3b Antonine probe (AD 165–180): empire + Asclepius-cult + military-administration subsets
- **Quote / loc.** Field 3 lines 96–98; §4 line 346; §6 line 412. Conditional on per-subset Phase-1 reachability. Subset filters specced in §8 line 433.
- **Type.** exploratory (pre-specified; not confirmatory).
- **Status.** PENDING-PLANNED — depends on the real-data mixture-corrected SPA (and Decision 34 subset-specific deconvolution + reachability floor). Backlog "H3b Antonine-specific replication test." Not yet runnable (needs mixture). At-risk note: also gated on the subset-specific reachability floor (Amendment 01 §A5.7, worst-case N≈2,000) AND Phase-1 detection thresholds.

### E2. H3b Crisis-of-the-Third-Century probe (AD 235–284): empire + Western-Empire provincial subset
- **Quote / loc.** Field 3 line 99; §4 line 346; §6 line 413. Western-Empire subset = `province_language=='Latin' AND province!='Roma'` (§2 line 135; Decision 26 B10).
- **Type.** exploratory (pre-specified).
- **Status.** PENDING-PLANNED — same dependency as E1. NB the Western-Empire subset definition is now effectively the Decision-36 primary frame; the province-language map artefact exists (`runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`).

### E3. H3b null models — exponential (primary) + CPL-3 (secondary), 1,000 MC, forward-fit in true-date space
- **Quote / loc.** §3 lines 173–179; §4 lines 306–321. Forward-fit-in-true-date-space + forward-aoristic-smeared MC; two-sided 95% envelopes.
- **Type.** confirmatory machinery (for the exploratory probes) / reporting-requirement.
- **Status.** DONE (machinery) for Phase 1; PENDING-PLANNED (application to real corrected SPAs in H3b). Forward-fit primitives exist (`runs/2026-04-25-h1-simulation/code/forward_fit.py`, `forward_fit_cpl.py`).

### E4. H3b k=4 exploratory knot-sensitivity + trapezoidal sensitivity on eligible subsets
- **Quote / loc.** §3 line 179 (k=4 exploratory upper bound); §3 line 167 (trapezoidal on every H3-eligible subset).
- **Type.** exploratory/optional + sensitivity.
- **Status.** PENDING-PLANNED (k=4 on real LIRE optional, backlog) / see C11 for trapezoidal-on-subsets (PARTIAL/at-risk).

### E5. H3b descriptive effect-size brackets + multiplicity noted
- **Quote / loc.** Field 3 line 101; §4 line 346 — results reported against the project's standard brackets (50%/≥50y; doubling/≥25y; 20%/≥25y) descriptively, multiplicity noted; no Holm family.
- **Type.** reporting-requirement.
- **Status.** PENDING-PLANNED — owed when H3b runs.

---

## F. PHASE 3 — H3c (Hanson 2021 residual replication; two-part confirmatory)

### F1. H3c(i) — provincial-capital contrast (draw-wise Pearson residuals; P(contrast>0) ≥ 0.95)
- **Quote / loc.** Field 3 line 81; §3 lines 269 + 345; §6 line 398; Decision 23. (Backlog phrases it as the "provincial-capital t-test"; the prereg binds on the *posterior contrast*, NOT a frequentist t-test — Decision 23/§4 line 345.)
- **Type.** confirmatory.
- **Status.** **UNACCOUNTED / at-risk** — the H3a confirmatory run computed and reported **H3c(ii) Moran's I only** (REPORT §7; Latin REPORT §2). The **H3c(i) provincial-capital contrast was NOT computed** in either the empire run or the Latin H3c/SR1 follow-up. The blind run did Moran's I; it did not do the capital contrast. This is a binding confirmatory test (one of the two H3c parts) and is currently missing from all done work. Likely cause: the run needs a provincial-capital indicator per city (a capital lookup) that may not have been assembled. **This is the single most important confirmatory gap.**

### F2. H3c(ii) — Moran's I on posterior-mean Pearson residuals at k ∈ {5,8,10}; ≥2-of-3 rule; 999-permutation
- **Quote / loc.** Field 3 line 82; §3 lines 271 + 345; §6 line 399; Decision 23.
- **Type.** confirmatory.
- **Status.** DONE (preliminary) — empire: NOT-SUPPORTED (0/3) (REPORT §7); Latin: NOT-SUPPORTED (0/3) (`REPORT-latin-h3c-sr1.md` §2). Clean non-replication of Hanson's residual Moran's I. Latin frame amendment-gated.

### F3. H3c(ii) supplementary — posterior distribution of Moran's I across draws (per k; 2.5/50/97.5 pct)
- **Quote / loc.** §3 line 271; §6 line 399; Decision 23.
- **Type.** supplementary / reporting-requirement (binding alongside).
- **Status.** DONE — reported per k in both REPORTs (e.g. empire k=8 [+0.001,+0.011,+0.024], frac>0=0.985).

### F4. H3c(ii) three-case interpretive guardrail (clean / posterior-sensitive / not-supported)
- **Quote / loc.** Field 3 line 82; §3 lines 273–279; §6 line 399; Decision 31.
- **Type.** reporting-requirement.
- **Status.** DONE (correctly N/A) — the guardrail engages only when the rule passes; both frames return NOT-SUPPORTED, so it does not engage. REPORTs explicitly note this.

### F5. H3c(ii) conditioned on the 8th PPC (PP Moran's I) tautology caveat
- **Quote / loc.** §3 line 279; Decision 29.
- **Type.** reporting-requirement / PPC linkage.
- **Status.** DONE — PPC #10 PASSED, so no tautology caveat triggered (REPORT §7).

### F6. H3c residual labelling (over/under/typical) — narrative only
- **Quote / loc.** §3 line 269 — descriptive labelling, does not gate any decision.
- **Type.** reporting-requirement (descriptive).
- **Status.** PENDING-PLANNED — owed at write-up; not a gating obligation.

### F7. SR2 — residuals reproduce Hanson 2021 (i) capital over-production + (ii) spatial clustering
- **Quote / loc.** Field 3 SR2 line 51.
- **Type.** reporting-requirement (descriptive secondary question; maps onto H3c(i)+(ii)).
- **Status.** PARTIAL — (ii) clustering answered (NOT-supported, F2). (i) capital over-production = H3c(i), UNACCOUNTED (see F1). So SR2(i) is unanswered.

---

## G. SECONDARY RESEARCH QUESTIONS (SR1, SR2) — enumeration

- **SR1** (Hanson 2021 / Carleton 2025 sublinear scaling replication via OLS log-log): see D5. **Status DONE** (empire + Latin), Latin amendment-gated. The prereg names only SR1 and SR2 as secondary research questions (Field 3 lines 47–51). There is no SR3+ in the prereg.
- **SR2** (capital over-production + residual clustering): see F7. **Status PARTIAL** — clustering done (not-supported); capital contrast UNACCOUNTED.
- Note on numbering: the "SR1" in the task brief = the OLS log-log Hanson comparator (done). No other SR-secondary questions exist in the prereg beyond SR1/SR2.

---

## H. §5 EXPLORATORY ANALYSES (pre-specified, non-confirmatory)

### H1. §5 small-N city trajectory — Layer A
- **Quote / loc.** §5 line 366–368; Decision 13.
- **Type.** exploratory.
- **Status.** DONE — `runs/2026-05-30-s5-small-n-trajectories/RESULTS.md`: 268 target cities + 45 provinces; calibration N*=300; Pompeii AD-79 external check (0.12% post-79 mass); trajectory clustering (k=6). COMPLETE (exploratory).

### H2. §5 small-N city trajectory — Layer B (β-inversion to time-varying population)
- **Quote / loc.** §5 line 370; Decision 13.
- **Type.** exploratory.
- **Status.** PENDING-PLANNED — deferred pending H3a β_within (now available: empire 0.587, Latin 0.733). RESULTS.md: "Layer B remains deferred pending H3a β_within." Now unblocked — runnable; .nc posteriors live on zbook only (preserve/back up).

### H3. §5 aggregate diagnostic (precision-vs-N; clustering; Layer B validation gate)
- **Quote / loc.** §5 line 372.
- **Type.** exploratory.
- **Status.** PARTIAL — precision-vs-N (calibration table) + clustering DONE (Layer A run); the Layer-B validation gate at independently-dated cities (Pompeii AD79 / Ostia c.AD250) is PARTIAL — Pompeii done; Ostia and the full Layer-B gate pending Layer B (H2).

### H4. §5 province-scale parallel methodological output
- **Quote / loc.** §5 line 374; Decision 13.
- **Type.** exploratory.
- **Status.** PARTIAL/PENDING — the Layer-A run included 45 provinces (RESULTS.md "268 target cities + 45 provinces"), so province-scale Layer A is partly done; province Layer B + diagnostic pending. Backlog "§5 province-scale parallel methodological output."

### H5. §5 temporal habit-removed residual trajectory analysis (foundation dates + case-study anchors)
- **Quote / loc.** §5 line 358–364; Decision 13.
- **Type.** exploratory.
- **Status.** **UNACCOUNTED** — distinct from H1 (small-N trajectory). This is the habit-decomposition + foundation-date / independent-anchor validation analysis (epigraphic-habit-lag estimate). No run exists; not in any active plan beyond Decision 13's bounded-scope commitment. Pre-specified §5 exploratory. (Overlaps Layer B but is a separate anchored-validation analysis.)

### H6. Decision 3 baorista cross-check (forward-fit vs baorista on representative provinces)
- **Quote / loc.** §5 line 378; Decision 3.
- **Type.** exploratory/sensitivity.
- **Status.** PENDING-PLANNED — baorista installed + smoke-validated on sapphire (backlog); comparison "with H3b; ~1 day." Smoke-test caveat: re-validate with full-width LIRE distribution before a real run.

### H7. §5 chronological resolution of H3c residuals (per-decadal)
- **Quote / loc.** §5 line 384.
- **Type.** exploratory.
- **Status.** **UNACCOUNTED** — not run; backlog "§5 chronological resolution of H3c residuals … Revisit with H3c." Pre-specified §5 exploratory with no artefact.

### H8. §5 information-infrastructure vs complexity-markers theoretical framing
- **Quote / loc.** §5 line 386.
- **Type.** exploratory (theoretical).
- **Status.** PENDING-PLANNED — at write-up; RAC-TRAC 2026 feedback informs it.

### H9. §5 letter-count alternative analysis
- **Quote / loc.** §5 line 388.
- **Type.** exploratory — PROMOTED by Amendment 01.
- **Status.** SUPERSEDED-BY-AMENDMENT 01 — letter mass promoted from exploratory cross-check to a co-registered parallel confirmatory measure (acts vs content); confirmatory for H3a cross-section only (letter recovery grid FAILed → temporal/detection exploratory; reachability shows letter temporal detection unreachable corpus-wide). Letter-mass H3a probe done exploratorily (`runs/2026-05-26-letter-count-probe/`); the *confirmatory* letter-mass H3a (same three-way rule) is PENDING-PLANNED under Amendment 01.

### H10. Stratified-by-convention-class SPA (§5, overlaps H2.4)
- **Quote / loc.** §5 line 376 — reported separately for transparency.
- **Type.** exploratory.
- **Status.** PENDING-PLANNED — see C15 (depends on real-data mixture).

---

## I. AMENDMENT TRIGGERS — which exist, which have fired

| # | Trigger (prereg loc) | Fired? | Status |
|---|---|---|---|
| I1 | Recovery-simulation validation FAIL (coverage or shape) → OSF amendment + model revision before any Phase 3 (§3 line 61; §7 line 420) | Not as a recovery FAIL. The 2026-05-22 grid FAILed under the *lodged* criterion, but diagnosed as metric/asymptotic defects, not recovery failure → handled by Amendment 01 §A5.5.1 criterion correction (not a model revision). Grid A PASSes under corrected criterion. | SUPERSEDED-BY-AMENDMENT 01 |
| I2 | pymc ↔ brms material disagreement on H3a verdict → OSF amendment (§3 line 267; §7 line 421) | No — β_within/f_within match to 3–4 sig figs (REPORT §6) | Not fired |
| I3 | Any numerical PPC critical trigger for H3a → model revision + amendment (§3 lines 260–265; §7 line 422) | No — H3a PPC verdict MINOR (0 critical) | Not fired |
| I4 | Convergence diagnostic failure (R̂/ESS/divergences) → OSF amendment (§3 line 208) | No for inscription grid + H3a. Letter grid R̂/ESS fail handled inside Amendment 01 (verdict, not a convergence-amendment) | SUPERSEDED-BY-AMENDMENT 01 (treatment refined) |
| I5 | Substantive post-lodgement methodology change → amendment before implementation (§7 line 423) | Yes ×2 → Amendment 01 (two-measure + criterion + subset deconvolution, LODGED 2026-06-04); Amendment 02 (Latin-province primary frame, PENDING, Decision 36) | I5a DONE / I5b PENDING |
| I6 | Aoristic-MC divergence flag (1.5× primary CI) — explicitly NOT an amendment trigger (§3 line 194; Decision 28) | N/A (analysis not yet run — see C10) | n/a |
| I7 | §5 measurement-error / three-weighting material divergence — NOT amendment triggers (flagged as limitations) (§5 lines 352, 354) | three-weighting done (all SUPPORTED); ME not run (D11) | partial |
| I8 | Prior-predictive absurdity → revisit priors + amendment before fit (design artefact §2) | No — prior-sanity gate PASSED (H3a REPORT §9) | Not fired |

**No amendment trigger has fired in the "must-revise-the-model" sense.** Amendment 01 was filed for a *construct/scope* change (two-measure) plus a *metric* clarification, not because a model failed. Amendment 02 is a *frame* change (Latin-primary), not a model failure.

---

## SUMMARY — what is UNACCOUNTED or at-risk

**UNACCOUNTED (pre-specified obligation, no artefact, not in any plan/decision I can find):**

1. **H3c(i) provincial-capital contrast** (F1) — a binding confirmatory test. The blind run did Moran's I (H3c(ii)) but NOT the capital contrast, in either the empire or Latin follow-up. Needs a provincial-capital indicator per city. **Highest priority.** Also leaves SR2(i) unanswered.
2. **Template-dictionary empirical scan** (A2) — the pre-Phase-2 design artefact that pins the convention component's actual interval contents + N-threshold on real LIRE. No `runs/*template-dictionary*` exists; the recovery grid used synthetic/proxy bases. **Prerequisite for the real-data H2.1 mixture run.**
3. **Dirichlet-multinomial supplementary fit** (C5) — committed model-comparison fit, not implemented.
4. **Rescaled-NegBin supplementary fit** (C6) — committed model-comparison fit, not implemented.
5. **Aoristic-MC supplementary** (C10) — run on the real-data primary multinomial; N_MC + divergence threshold not pinned; no run.
6. **Hanson-population measurement-error sensitivity** (D11) — ~~§5 sensitivity, σ_pop ∈ {0.1,0.2,0.3}; not run.~~ **RESOLVED 2026-06-16** — f_within robust, no material divergence (`runs/2026-06-16-s5-sensitivities/`, `edc5592`).
7. **Scaling-residual sensitivity for H3a** (D12) — ~~§5 sensitivity; not run.~~ **RESOLVED 2026-06-16** — within-province scaling is one coherent law with the global scaling; primary β_within stands (`edc5592`).
8. **§5 temporal habit-removed residual trajectory analysis** (H5) — distinct from small-N trajectory; foundation-date/anchor validation + habit-lag estimate; no run.
9. **§5 chronological resolution of H3c residuals (per-decadal)** (H7) — §5 exploratory; no run.
10. **Phase-1 stratified-sampling sensitivity** (B4) — ~~§5 supplementary; only an "optional" backlog note; no run.~~ **RESOLVED 2026-06-16** — superseded by Decision 8; thresholds robust to stratification via the width-pool check (`6acfddf`/`6b2a14a`).

**At-risk / ambiguous:**

- **Trapezoidal-aoristic sensitivity on H3-eligible subsets** (C11) — only done on the full-empire SPA, where r = 0.94 < 0.95 *already triggers* the prereg's "report trapezoidal alongside uniform" obligation. The per-eligible-subset version is not planned.
- **Committed `scripts/h3a_brms_shadow.R`** (D9) — fits the pooled pre-Mundlak model, not the confirmatory within-between spec; the matching shadow is a run-local script. Housekeeping, not a result risk.
- **Latin-frame results (D1, D5, F2)** — amendment-gated (Amendment 02 pending); cannot leave the repo as confirmatory until lodged.

**Obligations bearing specifically on the H2.1 MIXTURE RUN (fold into the launch spec):**

- A2 template-dictionary empirical scan (prerequisite — pins p_conv contents + N-threshold).
- C5 Dirichlet-multinomial + C6 rescaled-NegBin supplementary fits (reported alongside the multinomial primary on real data).
- C10 aoristic-MC supplementary (run on the real-data primary multinomial; pin N_MC ∈ [20,50] + 1.5× divergence flag first).
- C11 trapezoidal sensitivity (full-empire + every H3-eligible subset; empire r<0.95 already obliges reporting).
- C13/C14/C15/C16 H2.2 / H2.3 / H2.4 supporting consistency checks + empire-α descriptive context (all off the real-data fit).
- Decision 34 / Amendment 01 §A5.7 subset-specific deconvolution + reachability floor (worst-case N≈2,000) governs H3b subset mechanics — H2.1 unit-set should focus on Latin provinces (Decision 36).
- Production model is `build_model_f1_f3` (Decision 35); prior Beta(2,2)→Beta(1,1) refinement is amendment-consistent; report posterior-median p_gen timeline (gated), widen/caveat bands in peaked/late (AD~142–347) regimes.
