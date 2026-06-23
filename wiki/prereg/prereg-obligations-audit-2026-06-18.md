---
title: "Preregistration obligations — status refresh (2026-06-18)"
supersedes: "the SUMMARY of planning/prereg-obligations-audit-2026-06-05.md (status only)"
retains-from-2026-06-05: "the per-item prereg-line references, types, and A–I structure — still the durable per-item register; this file refreshes STATUS against work done 2026-06-05 → 2026-06-18"
author: "Claude (Opus 4.8, 1M context), on Shawn's request"
provenance-note: "Amendment status + H2.1-supplementary status VERIFIED this session against git tags / summary-addenda / run-artefact SUMMARY.md. The confirmatory/§5 'DONE' rows are reconciled from continuity.md + run dirs (high confidence), not each re-run this session."
---

# Preregistration obligations — status refresh (2026-06-18)

The 2026-06-05 audit (`prereg-obligations-audit-2026-06-05.md`) is **partly stale** —
it was written *before* the H3c(i) closure (same day), the H2.1 production run, the
cc-library remediation, three further amendments, and the whole §5 substantive arc.
This file refreshes the **status** picture. The 2026-06-05 file remains the durable
**per-item** register (prereg line refs, types). **Read this for "what's left"; read
2026-06-05 for "where in the prereg each item lives."**

---

## 1. Headline

The novel methodological core is **done**: temporal deconvolution (H2.1 core),
cross-sectional scaling (H3a), deviation detection (H3b), Hanson-residual replication
(H3c), and almost the entire §5 exploratory suite. The project is in its
**consolidation tail**. The single largest remaining *confirmatory* obligation is the
**H2.1 supplementary wave** (§5 below). Everything else outstanding is sensitivities,
robustness, Latin diagnostic-unit variants, or the write-up.

---

## 2. Amendment status — CORRECTED (2026-06-05 audit's I-section was stale)

**All four amendments are LODGED.** (Authority: git tags all resolve; the
`osf-amendment-0N-summary-addendum.md` files state lodged + date; continuity beacons
corroborate.)

| # | Scope | Lodged | Tag |
|---|---|---|---|
| 01 | Two-measure framework (acts vs content) + H2.1 grid criterion correction + subset-specific deconvolution | 2026-06-04 | `osf-amendment-01-2026-06-04` |
| 02 | **Latin-speaking provinces = primary frame** (H3a/H3b/H3c/SR1); empire = secondary context; 41→39-province reconciliation | **2026-06-06** | `osf-amendment-02-2026-06-06` |
| 03 | Convention component rebuilt as empirical calendar-slab basis (no reign tier); grid-quantisation reframe | 2026-06-08 | `osf-amendment-03-2026-06-08` |
| 04 | Cross-classified time × alignment deconvolution (reverses A03's shared basis; retains the reframe) | 2026-06-14 | `osf-amendment-04-2026-06-14` |

**Two consequences the 2026-06-05 audit got wrong:**
- It listed **Amendment 02 as PENDING** and "Latin-frame results amendment-gated." **A02 was lodged 2026-06-06** → **the Latin frame is the lodged PRIMARY frame; Latin confirmatory results are NOT gated.** (This also corrects my own 2026-06-18 verbal overview.)
- The audit predates A03 and A04 entirely.

**Housekeeping (non-blocking):** two *dated draft* files carry stale `status:` headers —
`osf-amendment-2026-06-07-convention-basis.md` ("DRAFT … not yet lodged") and
`osf-amendment-2026-06-14-cross-classified-remediation.md` ("DRAFT for Shawn's review —
NOT lodged"). Both were in fact lodged (tags + summary-addenda + the 2026-06-14
continuity close). The headers should be flipped to LODGED to match the authoritative
record.

---

## 3. Done / resolved since 2026-06-05 (reconciliation)

- **H3c(i) provincial-capital contrast** (audit F1, was "UNACCOUNTED, highest priority") — **DONE 2026-06-05**: capitals over-produce, SUPPORTED in all 4 cells (OXREP+AD117 × empire+Latin; P=1.000). Answers SR2(i).
- **Template-dictionary empirical scan** (A2, H2.1 prerequisite) — **DONE** (`runs/2026-06-05-template-dictionary/`), and superseded the curated-tier path (Decision 38).
- **D11 Hanson measurement-error**, **D12 scaling-residual**, **B4 stratified-sampling** — **RESOLVED 2026-06-16** (`runs/2026-06-16-s5-sensitivities/`).
- **H2.1 core deconvolution** — production run (28 units + Italia) → α-identifiability remediation → cc-library cross-classified model → 29-unit production refit → **Amendment 04 lodged**. Core α attribution settled.
- **H3a** (D1–D10 cluster) — confirmatory; empire `f_within` 0.299 SUPPORTED, Latin 0.480; PPC suite; pymc↔brms.
- **H3b** — draw-wise base run + flexible-null annex; probe-window P(deficit) deliverable; Antonine/Crisis windows covered (named scopes).
- **§5 suite** — Layer A ✓; Layer B raw ✓; **Layer B residual + q_u nested triple ✓ (2026-06-18)**; **H5 ✓**; **H7 per-period H3c ✓**; **peak-scaling ✓**; **size-vs-dynamics probe ✓ (2026-06-18)**.

---

## 4. OUTSTANDING — definitive, prioritised

**A. H2.1 supplementary wave — the largest remaining confirmatory debt.** Explicitly
"staged next wave, NOT run" (`runs/2026-06-07-h2.1-launch-prep/outputs/production/
SUMMARY.md`). Preregistered to be reported alongside the multinomial primary on real
data — see §5 for the itemised list. **Needs new model builders (DM/NegBin) — not just
a re-run.**

**B. Latin diagnostic-unit variants** *(small; beacon's stated next §5 step).* **H7-Latin**
and **peak-scaling-Latin** (both ran on the all-provinces 1044-frame; the project's
diagnostic unit is Latin-minus-Roma, Obs 101). Optional: §5 Latin Layer-A re-fit (H5
showed ≈ identical — polish only). *No longer amendment-gated (A02 lodged).*

**C. Preregistered sensitivities still open.**
- **D13 α-as-translator** for H3a (per-city mixture α as NBR covariate, N≥100) — needs a real-data per-city mixture, so downstream of (A).
- **H9 confirmatory letter-mass H3a** (under Amendment 01; letter temporal stayed exploratory after the letter recovery grid failed convergence) — the cross-sectional confirmatory letter-mass H3a is pending.
- **C11 trapezoidal-aoristic** on each H3-eligible subset (full-empire already obliges reporting, r<0.95) — folds into (A).

**D. Robustness / parallel-method.**
- **H6 Decision-3 baorista cross-check** (forward-fit vs Bayesian-aoristic; infra installed + smoke-tested; ~1 day; re-validate at full LIRE widths first).
- **H4 province-scale Layer B + diagnostic** (Layer A already covers 45 provinces; Layer B/diagnostic partial).

**E. Follow-ups generated 2026-06-18.**
- **Province-size regression** (direct test of the province-mediation inferred in Obs 104) — **running** as a background agent at time of writing.

**F. Non-analysis.**
- **Write-up** — empirical-first structure (Obs 101); not started.
- (No amendment lodgement outstanding — all four are lodged.)

---

## 5. The H2.1 supplementary wave — itemised (audit C5/C6/C10/C11/C13–C16)

All preregistered to accompany the real-data multinomial primary; all **staged, not
run** (SUMMARY.md). Fold into one supervised launch spec:

- **C5 Dirichlet-multinomial** model-comparison fit — *needs a new builder* (`cell_lib`/production only has the multinomial `build_model_f1_f3`).
- **C6 rescaled negative-binomial** model-comparison fit — *needs a new builder*.
- **C10 aoristic-MC supplementary** on the real-data primary multinomial — pin N_MC ∈ [20,50] + 1.5× divergence flag first (design-artefact, audit A3).
- **C11 trapezoidal-aoristic** sensitivity — full-empire (already obliged, r 0.94<0.95) + each H3-eligible subset.
- **C13 / C14 / C15** — H2.2 (boundary-step reduction), H2.3 (genuine-SPA convergence across date-range thresholds), H2.4 (stratified-by-convention-class SPA vs deconvolved), all off the real-data fit.
- **C16** — mixture empire-level α as descriptive context for H3a/H3c.
- Plus the launch-spec extras: fine-bracket sensitivity band, empire-EB sensitivity.

**Mechanics already pinned** (continuity / Decision 37): production model
`build_model_f1_f3`; Latin-province focus (Decision 36, now A02-lodged); subset-specific
deconvolution + reachability floor (Decision 34 / A01 §A5.7, worst-case N≈2,000).

---

## 6. Method note

Verified this session against source: amendment tags + summary-addenda (§2), and the
H2.1 "staged not run" SUMMARY (§5). The §3 "done" rows are reconciled from
`continuity.md` + run-dir presence — high confidence, not each re-executed. If a
definitive per-item re-verification is wanted, a read-only agent sweep over each run
artefact would produce it.
