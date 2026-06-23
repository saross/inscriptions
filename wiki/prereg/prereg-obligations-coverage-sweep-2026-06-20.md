---
title: "Preregistration obligations — definitive coverage sweep (pre-write-up assurance gate)"
date: 2026-06-20
author: "Claude (Opus 4.8, 1M context), read-only sweep on Shawn's request"
purpose: >
  A complete ledger confirming every preregistered obligation (lodged prereg +
  four lodged amendments) is covered (or flagging what is not) BEFORE the team
  begins the write-up. Read-only on analysis/data/code; the only file created.
sources-of-truth:
  - "planning/preregistration-draft.md (lodged; git tag osf-lodgement-2026-05-20 → a2e40fd)"
  - "planning/osf-supplementary-2026-05-20.md (lodged supplementary; §5/§6 + effect-size table)"
  - "planning/osf-amendment-2026-05-29-two-measure-framework.md (Amendment 01; tag osf-amendment-01-2026-06-04)"
  - "planning/osf-amendment-2026-06-06-latin-frame.md (Amendment 02; tag osf-amendment-02-2026-06-06)"
  - "planning/osf-amendment-2026-06-07-convention-basis.md (Amendment 03; tag osf-amendment-03-2026-06-08)"
  - "planning/osf-amendment-2026-06-14-cross-classified-remediation.md (Amendment 04; tag osf-amendment-04-2026-06-14 → 61c954c; REVERSES A03's shared basis)"
prior-reconciliations-cross-checked:
  - "planning/prereg-obligations-audit-2026-06-05.md (durable per-item register; SUMMARY/I-section stale)"
  - "planning/prereg-obligations-audit-2026-06-18.md (status refresh; its §4 'outstanding' list is now mostly discharged)"
  - "docs/notes/reflections/continuity.md (last-updated 2026-06-19/2026-06-20: 'analytical programme complete')"
provenance-note: >
  Every confirmatory verdict and every recently-discharged item below was RE-READ
  from the run artefact this turn (run-dir REPORT/JSON), not reconciled from
  memory or the prior audits. Repo HEAD at sweep time: 662495b. Working-tree
  prereg + supplementary are byte-identical to the lodged tag (only a trailing
  newline differs).
status-legend: "✅ covered | ◐ partial | ✗ not-covered | ⤴ deferred-to-follow-up | ⊘ superseded"
---

# Preregistration obligations — definitive coverage sweep (2026-06-20)

This is a pre-write-up assurance gate. It enumerates every preregistered element
from the lodged prereg + the four lodged amendments, accounts for supersessions
(notably Amendment 04 reversing Amendment 03's shared basis), and assigns each a
status verified against the run artefacts.

**Headline verdict:** every *confirmatory* obligation is ✅ covered and every
*amendment commitment* is discharged or properly superseded. Three pre-specified
*exploratory / descriptive* items are not fully discharged (two are write-up-time
deliverables; one exploratory subset pair is deferred). No confirmatory decision
rule is missing a recorded verdict. **All preregistered confirmatory bases are
covered for the write-up.** See §SUMMARY for the itemised flags.

---

## 0. Supersession chain (read this first)

The temporal-mixture convention/genuine deconvolution passed through four lodged
states. The obligation is governed by the **latest** lodged version:

1. **Lodged prereg (2026-05-20):** 3-tier convention basis (century / half-century
   / reign), shared structure, learned tier weights; multinomial primary.
2. **Amendment 03 (2026-06-08):** convention rebuilt as an empirical, frequency-
   weighted 3-tier *calendar-slab* basis (sub-century / century / multi-century),
   **no reign tier**; reigns/dynasties/events reclassified genuine-but-aoristic;
   convention reframed as grid-quantisation. Gated on a fresh 450-cell recovery
   re-validation (PASS, 96.4 %).
3. **Amendment 04 (2026-06-14) — GOVERNING:** replaces A03's single *shared* basis
   with a **cross-classified time × alignment** model (per-unit grid-aligned /
   non-aligned split + a fixed corpus-wide round-endpoint slab library + a
   classification likelihood sharing α). **Reverses A03's shared-basis choice;
   RETAINS A03's grid-quantisation reframe and reigns-as-genuine reclassification.**
   Gated on a 300-cell recovery grid (PASS) + a 29-unit production refit (28/29
   converge).

Independent tracks: **Amendment 01** (two-measure acts/content framework, on
date-window counts) and **Amendment 02** (Latin-speaking provinces = primary
frame) are *not* touched by A03/A04 — they govern the cross-sectional track.

---

## A. CROSS-CUTTING — design artefacts, conventions, multiplicity, software

| # | Obligation | Type | Gov-doc | Status | Evidence | Where reported | Notes |
|---|---|---|---|---|---|---|---|
| A1 | Recovery-grid design artefact (α grid, 6 shapes, 5 tier-vectors, N, reps, seed) | design-artefact | prereg §3/§4 | ✅ | `runs/2026-05-22-recovery-grid-design/` (design.json) | run dir | Pinned before any recovery sim. |
| A2 | Template-dictionary empirical scan (pins p_conv contents + N-threshold) | design-artefact | prereg §3; Dec 20 | ✅ (superseded path) | `runs/2026-06-05-template-dictionary/` | A03 justification | Scan done; **fed Decision 38 / A03**, which rebuilt the basis empirically and then A04 replaced it with the cc-library. Was the 2026-06-05 audit's gap; now closed. |
| A3 | PPC + prior-predictive numerical thresholds + N_MC + W1 + severity cutoffs | design-artefact | prereg §3/§4 | ✅ | H3a: `planning/h3a-design-artefact-2026-06-04.md`; H9: `runs/2026-06-18-h9-letter-mass-h3a/outputs/prior-predictive-thresholds.json`; N_MC=30 + 1.5× pinned in supp-wave `SPEC.md`/`REPORT.md` | run dirs | The aoristic-MC N_MC/divergence pin (the 2026-06-05 audit's open sub-item) is now pinned (N_MC=30, 1.5× flag). |
| A4 | Calendar/binning conventions (80×5-yr bins; inclusive-Roman; BC/AD limitation) | convention | prereg §3 | ✅ | recovery-grid design.json; throughout | all run dirs | BC/AD step retained as a known limitation (prereg §9). |
| A5 | Multiplicity / no-omnibus-family policy (incl. A01 each-unit-its-own-family) | reporting | prereg Field 3; A01 §A5.3 | ✅ | policy settled; H3a/H3c(i)/H3c(ii) each independent; H3b exploratory | confirmatory REPORTs | No Holm correction owed; A01: no cross-unit correction across acts/content. |
| A6 | UQ table (interval type per analysis) | reporting | prereg §3 | ✅ | posterior CIs in all confirmatory REPORTs; bootstrap CIs in supp-wave H2.3 | run dirs | All analyses now run, so all interval types are realised. |
| A7 | Software / reproducibility (Python 3.13; R brms+baorista; per-stage run dirs; tags) | reproducibility | prereg §8 | ✅ | per-stage `runs/` dirs are the project norm; all 5 git tags resolve | repo | — |
| A8 | Phase-2 Dockerfile + Zenodo archival | reporting | prereg §8; backlog | ⤴ deferred | backlog "revisit at paper submission" | — | Not yet due (mandated at submission). On-track, non-blocking. |
| A9 | Aoristic implementation note (direct numpy, tempun excluded) | reporting | prereg §3/§8 | ✅ | `primitives.py::aoristic_resample` | §8 | — |

---

## B. PHASE 1 — completed groundwork (fixed; not confirmatory)

| # | Obligation | Type | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| B1 | Min-sample-size thresholds (empire/province/urban) + FP control | groundwork | prereg §6 | ✅ | `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md` | FP control [0.007, 0.049] across 96 zero-effect cells. |
| B2 | CPL knot-sensitivity k∈{2,3,4} | exploratory/optional | prereg §5 | ✅ (Phase 1) | H1 v2 §5 | Optional real-LIRE re-run = backlog, optional. |
| B3 | CPL AIC-select threshold | exploratory/optional | prereg §5 | ✅ (Phase 1) | H1 v2 | Not applicable downstream. |
| B4 | Stratified-sampling sensitivity | sensitivity | prereg §5 | ✅ (superseded by Decision 8 + width-pool check) | `runs/2026-06-16-s5-sensitivities/` (`6acfddf`/`6b2a14a`) | Thresholds robust to stratification; 0 reachability classifications changed. |

---

## C. PHASE 2 — H2.1 mixture validation + observation model + supplementaries

| # | Obligation | Type | Gov-doc | Status | Evidence | Where reported | Notes |
|---|---|---|---|---|---|---|---|
| C1 | H2.1 recovery sim — α coverage + shape recovery (binding gate) | **confirmatory** | prereg Field 3/§6; A01 §A5.5.1 | ✅ | `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md` (Grid A binding clean-pass **98.6 %**, 355/360); letter Grid B FAIL (convergence, 0/360) | recovery-grid REPORT + COMPARISON-REPORT | Gate passes for **inscription mass** (the validated unit). Operating envelope α ≤ 0.70. |
| C1′ | A03/A04 recovery RE-validation (basis change ⇒ fresh gate) | **confirmatory (amendment gate)** | A03; A04 §A5.4 | ✅ | A03: `runs/2026-06-06-convention-basis-redesign/revalidation/FULL-GRID-REPORT.md` (PASS, **96.4 %**, 347/360). A04: `runs/2026-06-09-joint-identifiability/outputs/cc-VERDICT-library.md` (300-cell, all 4 adoption criteria met) + production refit `runs/2026-06-13-cc-production-refit/outputs/REFIT-VERDICT.md` (**28/29** converge) | amendment justifications | The gate artefact for A04 is the `-library` verdict; `grid-VERDICT.md` is the *lead* comparator (predicted-to-fail baseline), not the gate. |
| C2 | Wasserstein-1 supplementary shape metric per cell | supplementary | prereg §3/§4; A01 | ✅ | recovery-grid W1 per cell; flat-shape gate at W1 ≤ 10 y (A01) | recovery-grid REPORT | — |
| C3 | Convergence diagnostics (R̂/ESS; benign-divergence treatment) | amendment-trigger/reporting | prereg §3; A01 §A5.5.1 | ✅ | inscription grid + production refit pass; letter Grid B's R̂/ESS fail = the documented Grid B FAIL | recovery-grid + refit | Zero-divergence clause relaxed to field-standard (Decision 33 / A01). |
| C4 | Multinomial primary observation model | **confirmatory** | prereg §3; Dec 19/35 | ✅ | production model `build_model_cross_classified`/`build_model_f1_f3` lineage | refit / supp-wave | Multinomial is the binding primary; supp-wave confirms it adequate (C5/C6). |
| C5 | Dirichlet-multinomial supplementary fit (model comparison) | supplementary | prereg §3; Dec 19 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/model-comparison.md` | supp-wave | **DM does NOT move α** (max \|Δα\| ≈ 0.016 across 29 units); overdispersion warranted only 4/29. Cross-family PSIS-LOO correctly dropped (inapplicable across multinomial-vs-per-bin structures). Was a 2026-06-05 audit gap. |
| C6 | Rescaled negative-binomial supplementary fit | supplementary | prereg §3; Dec 19 | ✅ | same `model-comparison.md` | supp-wave | **NB does NOT move α**; same adjudicator. Was a 2026-06-05 audit gap. |
| C7 | Convention component — slab structure | confirmatory (structure) | prereg §3; Dec 20 → A03/A04 | ⊘ → ✅ | superseded by A03 empirical slab basis, then A04 cc-library | A04 §A5.2 | Governed by A04: fixed corpus-wide round-endpoint slab library. |
| C8 | Genuine component — GRW smoothness prior | confirmatory (structure) | prereg §3 | ✅ | non-centred GRW in production model | refit | GRW-band-overconfident-for-peaked-signals limitation carried (A01 §A5.7). |
| C9 | pymc NUTS for all likelihoods | confirmatory/reporting | prereg §3 | ✅ | multinomial + DM + NB all in pymc (supp-wave) | supp-wave | C5/C6 now satisfy the supplementary-likelihood leg. |
| C10 | Aoristic-MC supplementary on the real-data primary | sensitivity | prereg §3/§4/§6; Dec 28 | ✅ (resolved as method limitation) | `runs/2026-06-18-c10-validity-test/outputs/VALIDITY-REPORT.md` + `followup-ii-report.md` | C10 validity reports | By the prereg rule the point-date aoristic-MC **recovers planted α on synthetic** (max \|Δα\| 0.046); the real-empire point-collapse (α 0.10 vs mass-preserving 0.62) is a **method artefact** — θ-contamination (R2), the three-step/classify-analyse plug-in bias, NOT width (R1). **Report as a method limitation, not a genuine α-sensitivity.** N_MC=30, 1.5× flag pinned. Was a 2026-06-05 audit gap. |
| C11 | Trapezoidal-aoristic sensitivity (per H3-eligible subset + empire) | sensitivity | prereg §3; Dec 4 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/trapezoidal.md` | supp-wave | Input-level r (the prereg Decision-4 measure); **2/29 flag report-alongside** (empire 0.9402, Aquileia 0.9269). Output-level r dropped (convention-confounded, audit M-1). |
| C12 | Mixture PPC | PPC/clarification | prereg | ✅ (N/A as separate) | recovery coverage + convergence are the mixture's check | — | No separate mixture-PPC obligation beyond the grid; recorded for completeness. |
| C13 | H2.2 boundary-step reduction (real data) | supplementary | prereg Field 3/§6 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/h2.2-boundary-steps.md` | supp-wave | **15/29 (52 %)** meet ≥50 % mean boundary-step reduction; aggregates negative (the known empire-aggregate behaviour), reported as a supporting check, not a gate. |
| C14 | H2.3 genuine-SPA convergence across date-range thresholds | supplementary | prereg Field 3/§6 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/h2.3-threshold-convergence.md` | supp-wave | **8/29** meet r ≥ 0.9 on all pairs; the rest are below the N<2,000 reachability floor at tight T and explicitly caveated, not failed. |
| C15 | H2.4 stratified-by-convention-class SPA vs deconvolved | supplementary | prereg Field 3/§5/§6 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/h2.4-stratified.md` | supp-wave | Internal-consistency check (not validation); assembled with the M1 year-precise-drop caveat. |
| C16 | Mixture empire-level α as descriptive context | reporting | prereg §1/§3; Dec 22/35 | ✅ | `runs/2026-06-18-h2.1-supplementary-wave/outputs/REPORT.md` (29-unit α table) | supp-wave | α read-off for all 29 units; empire 0.680, latin-aggregate 0.739. |

---

## D. PHASE 3 — H3a primary confirmatory + supplementaries

| # | Obligation | Type | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| D1 | H3a within-between (Mundlak) NBR — f_within three-way verdict | **confirmatory (sole primary)** | prereg Field 3/§3/§6 | ✅ | `runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json` + `REPORT.md`: empire 0.299 [0.240, 0.365] **SUPPORTED**; **Latin (A02 primary) 0.480 [0.401, 0.566] SUPPORTED** | **Caveat:** REPORT.md (dated 2026-06-04, predates A02) still labels empire "PRIMARY"/Latin "Sensitivity B" and is stamped "PRELIMINARY — pending sign-off". Numbers unambiguous; the frame-label flip + sign-off label live in Decision 36 / A02, not yet re-cut into the REPORT headings. Housekeeping, not a numbers gap. |
| D2 | Posterior-probability ladder P(f>0.05/0.10/0.20) | supplementary (binding alongside) | prereg Field 3 | ✅ | empire 1.000 / 1.000 / 0.9996; Latin 1.000 / 1.000 / 1.000 | REPORT rounds the empire 0.20 rung to 1.000; prose states ≥0.9996. |
| D3 | Three-weighting sensitivity (unweighted + pop- + insc-weighted) | sensitivity | prereg §5; Dec 32 | ✅ | empire: unweighted 0.299, pop-weighted 0.494 [0.395,0.609], insc-weighted 0.419 [0.335,0.514]; all SUPPORTED | REPORT §1. |
| D4 | Bayesian R² (latent + response; vs brms) | reporting | prereg §3 | ✅ | response 0.133 [0.091,0.201] (brms 0.136); latent 0.473 [0.434,0.509] | REPORT §3. |
| D5 | OLS log-log comparator (SR1; vs Hanson) | reporting/SR1 | prereg Field 3/§3/§4 | ✅ | empire slope 0.284 [0.195,0.373]; Latin 0.505; H9 letter-mass slope 0.470 [0.356,0.584] | `sr1-latin-results.json`; H9 `h9-results.json`. |
| D6 | Between-province component reported descriptively | reporting | prereg §3/§9 | ✅ | β_between −0.242 [−0.701,0.238] (crosses 0), reported with §9 caveat | not separately identifiable. |
| D7 | Prior-predictive checks (numerical, design-pinned) | PPC/design-artefact | prereg §3; Dec 25 | ✅ | `h3a-design-artefact-2026-06-04.md` §2; prior-sanity gate PASSED | committed before fit. |
| D8 | Posterior-predictive checks — full suite incl. PP Moran's I | PPC | prereg §3; Dec 25/29/30 | ✅ | `runs/2026-06-04-h3a-confirmatory/outputs/ppc-results.json`: MINOR (0 critical, 5 minor, 5 pass); PP Moran's I (#10) PASS | No HALT/revision/amendment; PP Moran's I PASS ⇒ no tautology caveat on H3c(ii). |
| D9 | pymc ↔ brms shadow cross-validation | confirmatory cross-check/amendment-trigger | prereg §3 | ✅ | REPORT §6: β_within/f_within match exact; "No material disagreement" | **Amendment trigger NOT fired.** Housekeeping (carried from 2026-06-05): the *committed* `scripts/h3a_brms_shadow.R` fits the pooled pre-Mundlak model; the matching shadow is the run-local Mundlak script. Result is sound; committed script mismatch is a non-blocking housekeeping note. |
| D10 | Standardisation sensitivity (exploratory) | exploratory | prereg §3 | ✅ | Sensitivity C: f_within 0.298 ≈ 0.299 | REPORT. |
| D11 | Hanson-population measurement-error sensitivity (σ_pop ∈ {0.1,0.2,0.3}) | sensitivity | prereg §5; Dec 26 | ✅ | `runs/2026-06-16-s5-sensitivities/REPORT.md` (`edc5592`): Berkson ME; f_within 0.299→0.305/0.320/0.341; max CI shift 0.047 < 0.063 ⇒ no material divergence | Was a 2026-06-05 audit gap. |
| D12 | Scaling-residual sensitivity for H3a | sensitivity | prereg §5 | ✅ | `runs/2026-06-16-s5-sensitivities/REPORT.md`: within-province scaling is one coherent law with global scaling; primary β_within stands | Was a 2026-06-05 audit gap. |
| D13 | α-as-translator sensitivity for H3a (per-city α, N≥100) | sensitivity | prereg §5 | ✅ | `runs/2026-06-19-d13-alpha-as-translator/outputs/D13-REPORT.md` (`549c3a1`→`be91a65`; Obs 107): β_within +0.431→+0.422 (0.14 post-SD), **clean null**; robust under MI (M=50, FMI 0.5 %) | **The last preregistered obligation — discharged.** City-level confirmation of Obs 94 (Spearman −0.107). H3a not confounded by per-city convention intensity. |
| D14 | H3a flexible-dispersion refinement | exploratory/optional (NOT prereg) | backlog | ⤴ optional | backlog Phase-3 item | Logged so it is not mistaken for a missed obligation; it is a *new* optional improvement, not a prereg commitment. |

---

## E. PHASE 3 — H3b (pre-specified EXPLORATORY deviation-detection)

H3b is **exploratory** (Decision 15; lodged prereg Field 3 places it outside the
confirmatory family — no Holm-corrected family). Governed for mechanics by
**A04 §A5.6** (reliability by uncertainty propagation, replacing the post-hoc
α-identifiability *restriction*).

| # | Obligation | Type | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| E1 | Antonine probe (AD 165–180): **empire** + Asclepius-cult + military-administration subsets | exploratory | prereg Field 3/§4/§6 | **◐ partial** | empire **covered** (`runs/2026-06-09-h3b/REPORT-drawwise-2026-06-15.md`: net dep. −23 %, P(def) 1.000). **Asclepius-cult & military-administration subsets NOT built/run** | **GAP (exploratory).** OQ-6 explicitly **deferred** (`h3b-implementation-spec-2026-06-14.md:46`, §9 item 2): "Asclepius / military not built — need per-subset deconvolution, per-subset reachability, and a LIRE membership rule (no clean flag exists)." Conditional on per-subset Phase-1 reachability. |
| E2 | Crisis probe (AD 235–284): **empire** + Western-Empire provincial subset | exploratory | prereg Field 3/§4/§6 | ✅ | empire net dep. −27 %, P(def) 1.000; **latin-aggregate (= the operational Western-Empire-provincial subset, Decision 36) net dep. −13 %, P(def) 1.000** | drawwise REPORT §3. The Western-Empire subset (`province_language=='Latin' AND province!='Roma'`) IS the latin-aggregate unit. |
| E3 | H3b null models — exponential (primary) + CPL-3, MC forward-fit | confirmatory machinery for the probes | prereg §3/§4 | ✅ | drawwise engine; CPL-3-to-observed informative null + exponential labelled saturated cross-check | Global Timpson test saturates at these N (documented over-power); probe-window P(deficit) is the deliverable. |
| E4 | H3b k=4 knot-sensitivity + trapezoidal on eligible subsets | exploratory/optional + sensitivity | prereg §3 | ✅ (folded) / ⤴ optional | flexnull annex sweeps CPL k∈{2,3,5,7} (`runs/2026-06-09-h3b/outputs/flexnull/ANNEX-REPORT.md`); trapezoidal-per-subset = C11 (supp-wave) | k=4 specifically on real LIRE is an optional backlog extra; the flexible-null annex covers the flexibility-lever question (NO-GO, Obs 93). |
| E5 | H3b descriptive effect-size brackets + multiplicity noted | reporting | prereg Field 3/§4 | ✅ | drawwise REPORT reports net departure % + P(deficit) against project brackets; H3b is exploratory, multiplicity noted descriptively | — |
| E6 | Flexible-null robustness annex (D2's deferred robustness) | exploratory/robustness | H3b draft D2 | ✅ | `runs/2026-06-09-h3b/outputs/flexnull/ANNEX-REPORT.md` (Obs 93): NO-GO — saturation robust to flexibility (edf 5→20) AND to effective-N thinning ⇒ structural null-misspecification, not large-N over-power | Not a prereg item per se; closes the H3b D2 question and the baorista-for-the-global-test motivation. |

---

## F. PHASE 3 — H3c (Hanson 2021 residual replication; two-part confirmatory)

| # | Obligation | Type | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| F1 | H3c(i) provincial-capital contrast (draw-wise; P(contrast>0) ≥ 0.95) | **confirmatory** | prereg Field 3/§3/§4; Dec 23 | ✅ | `runs/2026-06-04-h3a-confirmatory/outputs/REPORT-h3c-i-capital-contrast.md` + `h3c-i-results-oxrep-primary.json`: **SUPPORTED in all 4 cells, P=1.000** (OXREP empire +0.964 [0.736,1.213]; Latin +1.081 [0.806,1.408]; AD-117 sensitivity both SUPPORTED) | **Closes the 2026-06-05 audit's single highest-priority gap.** Capital indicator = Hanson's own OXREP "Civic Status" variable (collision-safe exact-toponym match). Answers SR2(i). |
| F2 | H3c(ii) Moran's I (k∈{5,8,10}; ≥2-of-3; 999 perm) | **confirmatory** | prereg Field 3/§3/§4; Dec 23 | ✅ | empire NOT-SUPPORTED (0/3); Latin NOT-SUPPORTED (0/3) | REPORT §7 + `REPORT-latin-h3c-sr1.md`. Clean non-replication of Hanson's residual clustering. |
| F3 | H3c(ii) supplementary — posterior distribution of Moran's I per k | supplementary (binding alongside) | prereg §3; Dec 23 | ✅ | per-k 2.5/50/97.5 pct in both REPORTs | — |
| F4 | H3c(ii) three-case interpretive guardrail | reporting | prereg Field 3/§3; Dec 31 | ✅ (correctly N/A) | both frames NOT-SUPPORTED ⇒ guardrail does not engage | REPORTs note this. |
| F5 | H3c(ii) PP-Moran's-I tautology caveat linkage | reporting | prereg §3; Dec 29 | ✅ | PPC #10 PASS ⇒ no tautology caveat triggered | — |
| F6 | H3c residual labelling (over/under/typical) — narrative | reporting (descriptive) | prereg §3 | ⤴ write-up | owed at write-up; not gating | descriptive only. |
| F7 | SR2 — capital over-production (i) + spatial clustering (ii) | reporting (secondary) | prereg Field 3 | ✅ | (i) SUPPORTED via F1; (ii) NOT-supported via F2 | both halves now answered (the 2026-06-05 SR2(i) gap is closed). |

---

## G. SECONDARY RESEARCH QUESTIONS

- **SR1** (sublinear scaling replication, OLS log-log): ✅ — D5 (empire + Latin; H9 letter-mass slope reported as content variant). Latin frame is the A02-lodged primary, not gated.
- **SR2** (capital over-production + residual clustering): ✅ — F7 (both halves answered).
- The prereg names only SR1 and SR2 (no SR3+).

---

## H. §5 EXPLORATORY ANALYSES (pre-specified, non-confirmatory)

| # | Obligation | Type | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| H1 | Small-N city trajectory — Layer A | exploratory | prereg §5; Dec 13 | ✅ | `runs/2026-05-30-s5-small-n-trajectories/RESULTS.md` (COMPLETE): 268 cities + 45 provinces; calibration N*=300; Pompeii AD-79 check pass; k=6 clustering | — |
| H2 | Small-N city trajectory — Layer B (β-inversion) | exploratory | prereg §5; Dec 13 | ✅ | raw: `runs/2026-06-16-s5-layer-b-beta-inversion/REPORT.md` (Obs 96; validation gate passes Ostia + Pompeii); residual: `runs/2026-06-17-s5-layer-b-residual/REPORT.md` (Obs 102/103, q_u nested triple) | Both the raw and habit-removed-residual Layer B are done. |
| H3 | Aggregate diagnostic (precision-vs-N; clustering; validation gate) | exploratory | prereg §5 | ✅ | Layer A calibration table + clustering; Layer B gate (Ostia apogee, Pompeii post-79 mass ≈ 0) | Pompeii + Ostia anchors both met. |
| H4 | Province-scale parallel methodological output | exploratory | prereg §5; Dec 13 | ✅ (this paper) / ⤴ standalone deferred | Layer A includes 45 provinces; **province-from-empire residual q_u** (`runs/2026-06-17-s5-layer-b-residual/`, Obs 103) IS the province-scale Layer B for this paper (validated-by-inheritance, 5.6e-16 wiring guard) | Shawn 2026-06-20: standalone province-as-unit inversion (needs a province-level exponent + a province-apogee anchor) → **follow-up paper** (prereg §"Province-scale extension" explicitly defers substantive provincial reconstruction). |
| H5 | Temporal habit-removed residual trajectory (foundation dates + anchors) | exploratory | prereg §5; Dec 13 | ✅ | `runs/2026-06-17-s5-h5-habit-removed/REPORT.md` (Obs 97/98): g_shape = empire-common component; habit-lag median ≈ 0; foundation-terminus clean (0.07 % pre-foundation mass) | Was the 2026-06-05 audit's UNACCOUNTED H5. Identification caveat (g_shape conflates habit/demography/taphonomy) foregrounded (Obs 98). |
| H6 | baorista Bayesian-aoristic comparison | exploratory/sensitivity | prereg §5; Dec 3 | ⤴ deferred-to-follow-up | infra installed + smoke-tested (`runs/2026-05-03-baorista-install/`); Shawn 2026-06-20 (Decision 3 Option D) | Validates the aoristic substrate, not the deconvolution (the paper's novelty); the flexnull annex already worked the Bayesian-null robustness question. baorista = the HMM follow-up's emission layer. |
| H7 | Chronological resolution of H3c residuals (per-decadal) | exploratory | prereg §5 | ✅ | `runs/2026-06-17-s5-h7-perperiod-h3c/REPORT.md` (all-provinces, Obs 99) + `runs/2026-06-18-h7-latin/REPORT.md` (Latin diagnostic unit, Obs 106) | β_within U-shape over 8×50-yr periods; capitals over-produce every period; clustering early-empire only. Was the 2026-06-05 audit's UNACCOUNTED H7. |
| H8 | Information-infrastructure vs complexity-markers framing | exploratory (theoretical) | prereg §5 | ⤴ write-up | at write-up; RAC-TRAC 2026 feedback informs | No hypothesis turns on it. |
| H9 | **Letter-count alternative analysis** — PROMOTED to confirmatory letter-mass H3a by A01 | exploratory→**confirmatory** (cross-section) | prereg §5; **A01 §A5.2** | ✅ | `runs/2026-06-18-h9-letter-mass-h3a/outputs/h9-results.json` (`ec99343`): **f_within SUPPORTED every frame** — Latin (primary) 0.448 [0.364,0.535], empire 0.356; pop-wt 0.626, letter-wt 0.607; ladder 1.0/1.0/1.0; R̂ 1.0, 0 div; PPC MINOR (0 critical) | **Both measures (acts + content) corroborate within-province scaling.** Letter-mass *temporal/detection* stays exploratory (Grid B FAIL + unreachable corpus-wide, A01 §A5.2) — correctly scoped. Was the 2026-06-18 audit's open confirmatory letter-mass item. |
| H10 | Stratified-by-convention-class SPA (§5; overlaps H2.4) | exploratory | prereg §5 | ✅ | = C15 (`runs/2026-06-18-h2.1-supplementary-wave/outputs/h2.4-stratified.md`) | reported separately for transparency. |

---

## I. AMENDMENT-ADDED / -CHANGED OBLIGATIONS (the four lodged amendments)

| # | Obligation | Gov-doc | Status | Evidence | Notes |
|---|---|---|---|---|---|
| AM01-a | Two-measure framework: letter mass = co-registered parallel **confirmatory** measure for H3a (each unit its own family; no cross-unit correction) | A01 §A5.2/§A5.3 | ✅ | H9 (above) — letter-mass H3a SUPPORTED every frame | confirmatory letter-mass family bounded to the cross-section (principled). |
| AM01-b | Recovery-grid binding-criterion clarification (recoverability map; α≤0.70 envelope; flat-shape W1 patch; α demoted to diagnostic) | A01 §A5.5.1 | ✅ | recovery-grid two-unit REPORT (binding criterion applied; Grid A PASS / Grid B FAIL) | — |
| AM01-c | Subset-specific deconvolution + measured reachability floor (worst-case N≈2,000) | A01 §A5.7; Dec 34 | ✅ | reachability `runs/2026-06-03-small-n-reachability/`; supp-wave caveats units below N<2,000; H2.3 floor applied | subset SPAs de-fogged by subset-specific fit, not the empire-wide convention shape. |
| AM01-d | **Content-residual (inter-measure delta)** — pre-specified derived quantity; descriptive map + cross-tab vs scaling residual | A01 §A5.4 | **✅ covered (descriptive)** [updated 2026-06-20: was "✗ not-covered"; this sweep predated the A01 run] | `runs/2026-06-20-a01-content-residual/outputs/content-residual-results.json` computes the per-city `log(letter_mass) ~ log(inscription_count)` content residual and its cross-tab vs the scaling residual; lodged as Obs 108 (`docs/notes/working-notes.md:5681`) | **DISCHARGED (exploratory/descriptive).** A01 explicitly: "no pre-committed threshold and no confirmatory verdict" — so it changes nothing confirmatory, but the pre-specified A01 reporting item is now computed and reported (Obs 108). |
| AM02 | Latin-speaking provinces = primary frame (H3a/H3b/H3c/SR1); empire = secondary; 41→39-province reconciliation | A02 | ✅ | H3a Latin frame SUPPORTED; H3c(i) Latin SUPPORTED; H9 Latin primary; H3b latin-aggregate; D13 Latin frame; reconciliation in A02 | **Latin frame is the lodged primary — NOT amendment-gated.** Housekeeping: the H3a REPORT.md headings still label empire "PRIMARY"/Latin "Sensitivity B" (predate A02); flip at write-up (D1 caveat). |
| AM03 | Convention = empirical calendar-slab basis (no reign tier); reigns/events genuine-but-aoristic; grid-quantisation reframe; recovery re-validation gate | A03 | ✅ (partly ⊘ by A04) | re-validation PASS (96.4 %, `runs/2026-06-06-convention-basis-redesign/revalidation/FULL-GRID-REPORT.md`) | **A03's shared-basis choice is REVERSED by A04; A03's grid-quantisation reframe + reigns-as-genuine reclassification RETAINED.** |
| AM04 | Cross-classified time × alignment model (reverses A03 shared basis); fixed corpus-wide slab library; classification likelihood sharing α; recovery grid + production refit gate; H3b uncertainty propagation replaces the α-identifiability restriction | A04 | ✅ | 300-cell grid PASS (`cc-VERDICT-library.md`); refit 28/29 converge (`REFIT-VERDICT.md`); θ re-derived (θ_gen 0.025) + θ-sweep robust 27/29; H3b drawwise propagation done (E1–E5) | **GOVERNING version of the temporal deconvolution.** empire-aggregate is the single non-converger (R̂≈1.013), reported as a known limitation. Two-bound [shared, per-unit] α retained as fallback disclosure for high-residual units; Moesia inf / Britannia soft-annotated. |

---

## J. AMENDMENT TRIGGERS — which fired

| Trigger (prereg loc) | Fired? | Disposition |
|---|---|---|
| Recovery-sim validation FAIL → amend + revise before Phase 3 (§3/§7) | Not as a recovery FAIL of the model | ⊘ handled by A01 §A5.5.1 criterion correction (Grid A PASS under corrected criterion). Letter Grid B FAIL = a unit-scope verdict, not a model-revision trigger. |
| pymc↔brms material disagreement on H3a verdict → amend (§3/§7) | No | Not fired (D9: "No material disagreement"). |
| Numerical PPC critical trigger for H3a → revise + amend (§3/§7) | No | Not fired (D8: 0 critical; H9 PPC: 0 critical). |
| Convergence diagnostic failure → amend (§3) | No (inscription grid + H3a + refit) | ⊘ benign-divergence treatment refined (A01). empire-aggregate under-convergence reported as a limitation, not amended (secondary unit). |
| Aoristic-MC divergence flag (1.5×) — explicitly NOT an amendment trigger | N/A | C10 collapse diagnosed as a method artefact (θ-contamination), reported as a limitation; consistent with the prereg's "no amendment trigger". |
| Substantive post-lodgement methodology change → amend before implementation (§7) | **Yes ×4** | All four amendments lodged (A01 two-measure + criterion + subset deconv; A02 Latin frame; A03 empirical slab basis; A04 cross-classified). **No amendment lodgement outstanding.** |
| §5 ME / three-weighting material divergence — NOT triggers | three-weighting all SUPPORTED; ME (D11) no material divergence | — |
| Prior-predictive absurdity → revisit priors + amend | No (prior-sanity gate PASSED, H3a + H9) | Not fired. |

**No "must-revise-the-model" amendment trigger fired.** The four amendments are
construct/scope/basis changes, each properly recovery-validated before adoption.

---

## SUMMARY

**Total obligations enumerated:** 63 rows
(A1–A9 = 9; B1–B4 = 4; C1, C1′, C2–C16 = 17; D1–D14 = 14; E1–E6 = 6; F1–F7 = 7;
SR1/SR2 = 2; H1–H10 = 10; I/amendment-added = AM01-a..d, AM02, AM03, AM04 = 7;
J amendment-triggers tracked separately, not counted as obligations).

> [Note added 2026-06-20, accuracy audit: the "63" is internally inconsistent and
> matches neither cross-check. The component groups enumerated on the line above sum
> to **76** (9+4+17+14+6+7+2+10+7), and the by-status tally below sums to **62**
> (covered + partial + not-covered + deferred). "63" is therefore an artefact, not a
> reconciled total; left as written rather than substituting an invented figure. The
> *substantive* coverage picture is in the by-status counts (now 55 covered / 0
> not-covered after AM01-d was discharged via Obs 108) and the per-row table above.]

**Counts by status:**

- ✅ covered: **55** [updated 2026-06-20 from "54": AM01-d discharged via Obs 108 / `runs/2026-06-20-a01-content-residual/`]
- ◐ partial: **1** (E1)
- ✗ not-covered: **0** [updated 2026-06-20 from "1": AM01-d content-residual is now covered — see the AM01-d row and Obs 108]
- ⤴ deferred-to-follow-up / write-up / optional: **6** (A8, D14, F6, H4-standalone, H6, H8)
- ⊘ superseded (and re-covered under the governing version): C7 (→A04), and the A03 shared-basis within AM04 (recorded, not double-counted)

**Every confirmatory obligation is ✅ covered**, with a recorded verdict:
H2.1 recovery gate (Grid A PASS; A03 96.4 % PASS; A04 grid + refit PASS); H3a
f_within SUPPORTED (both frames); H9 letter-mass H3a SUPPORTED (every frame);
H3c(i) capital contrast SUPPORTED (P=1.000, all 4 cells); H3c(ii) clustering
NOT-SUPPORTED (clean non-replication); the multinomial primary + DM/NB
supplementaries. No confirmatory decision rule lacks a recorded verdict.

### Itemised list of EVERY partial / not-covered / otherwise-flagged item

1. **✗ AM01-d — content-residual (inter-measure delta) — NOT COMPUTED.**
   *Gov:* Amendment 01 §A5.4. *Type:* pre-specified derived quantity,
   **exploratory/descriptive (no threshold, no verdict).** *What's missing:* the
   per-city residual from `log(letter_mass) ~ log(inscription_count)`, and the
   2-D residual-space map cross-tabulated against the scaling residual. Only
   narrative mentions exist (`docs/notes/working-notes.md:1447`). *Where it
   should be reported:* a §5/descriptive figure + cross-tab in the write-up.
   *Impact:* none on any verdict; cheap (one OLS + a scatter/map). **The single
   genuine un-discharged pre-specified analysis.**

2. **◐ E1 — H3b Antonine probe subsets (Asclepius-cult + military-administration)
   — NOT RUN.** *Gov:* lodged prereg Field 3 line 98 / §4 / §6 (H3b, EXPLORATORY
   per Decision 15). *What's covered:* the **empire-level** Antonine probe
   (net dep. −23 %, P(def) 1.000). *What's missing:* the two named subsets,
   explicitly **deferred** (`runs/2026-06-09-h3b/h3b-implementation-spec-2026-06-14.md:46`
   and §9 item 2) — they need per-subset deconvolution, per-subset Phase-1
   reachability, and a LIRE membership rule (no clean Asclepius/military-diploma
   flag exists). The probe was always *conditional on per-subset reachability*.
   *Where it should be reported:* H3b §5 if built; otherwise a one-line
   not-reached note (consistent with the conditional-on-reachability prereg
   wording). *Impact:* none on any confirmatory claim (H3b is exploratory).

3. **D1 / AM02 housekeeping (label only) — H3a REPORT frame labels are stale.**
   `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md` (dated 2026-06-04, before
   A02) still labels the empire frame "PRIMARY" and Latin "Sensitivity B", and
   carries a "PRELIMINARY — pending sign-off" stamp. The A02-lodged primary is
   the **Latin** frame. Numbers are unambiguous and both frames are SUPPORTED;
   only the artefact's internal labels need re-cutting at write-up. *Not a numbers
   gap.*

4. **D9 housekeeping (committed script) — `scripts/h3a_brms_shadow.R` fits the
   pooled pre-Mundlak model**, not the within-between confirmatory spec; the
   shadow that matched the estimands is the run-local Mundlak script (REPORT §6).
   The *result* is sound and the amendment trigger did not fire; the committed
   script should be aligned (or annotated) for reproducibility. *Not a result
   risk.*

5. **⤴ Deferred-to-follow-up (Shawn-decided 2026-06-20, all non-gating):**
   - **H4 standalone province-scale Layer B** — the province-from-empire residual
     q_u (Obs 103) serves as this paper's province-scale Layer B; a standalone
     province-as-unit inversion → follow-up (prereg §"Province-scale extension"
     defers substantive provincial reconstruction explicitly).
   - **H6 baorista cross-check** — infra ready; validates the aoristic substrate,
     not the deconvolution; → HMM follow-up.
   - **A8 Phase-2 Dockerfile + Zenodo** — mandated at submission, not yet due.
   - **D14 H3a flexible-dispersion** — a *new* optional improvement, not a prereg
     commitment.

6. **⤴ Write-up-time reporting items (not analyses):** F6 (residual
   over/under/typical labelling), H8 (information-infrastructure framing). Owed
   at write-up; nothing to compute.

### One-line verdict

**Are all preregistered bases covered for the write-up? — YES for everything
confirmatory and for every lodged amendment commitment; with two small
pre-specified *exploratory/descriptive* items outstanding (the Amendment-01
content-residual delta, not computed; and the two H3b Antonine subsets,
deferred-as-not-reachable) plus two label-only housekeeping fixes (the H3a REPORT
frame labels and the committed brms-shadow script). None blocks the write-up; the
content-residual is the one cheap analysis worth running (or explicitly carrying
as a stated non-deliverable) before the §5 write-up.**
