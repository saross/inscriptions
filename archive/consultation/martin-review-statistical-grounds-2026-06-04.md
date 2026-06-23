---
title: "Statistical grounds for the four Martin-flagged decisions (OSF Amendment 01 §A5.5.1)"
date: 2026-06-04
author: "Claude (Opus 4.8, 1M context), on Shawn's brief"
purpose: "Prep for Martin's draft-stage sign-off. For each of the four items flagged in §A5.5.1, gives (1) how a statistical SME frames the decision, (2) what the grid/reachability data say, (3) a recommendation (confirm/revise), (4) the literature that would firm it up. Not a final decision — grounding for one."
data-sources: "grid-summary.parquet (both grids); inscription-mass/outputs/tables/alpha-bias.parquet; runs/2026-06-03-small-n-reachability/outputs/reachability-by-cell.csv. All figures re-computed 2026-06-04."
---

# Principled grounds for the four flagged §A5.5.1 decisions

The four items flagged for Martin (§A5.5.1 sign-off note): (a) the α-diagnostic
operationalisation; (b) the operating-envelope cut (α ≤ 0.70); (c) the
headline-B / diagnostic-A reporting + the zero-tolerance divergence gate; (d) the
reading that the recovery-grid gate bears only on mixture-dependent analyses.

---

## (a) α-diagnostic operationalisation

**As drafted.** α demoted to a diagnostic; report signed bias + 90th-pct
|bias| ≈ 0.18; all α-claims hedged to that precision.

**SME framing.** Characterising recovery of a parameter from a simulation is a
*measurement-agreement* problem. The field tools are **limits of agreement**
(Bland–Altman), a **ROPE** (region of practical equivalence), or a **tolerance
interval** — and one asks whether the error is random (zero-mean) or systematic
(bias), and whether it depends on the conditions. A single point-precision number
is the weakest summary.

**What the data say** (Grid A, in-envelope α ≤ 0.70; signed bias = recovered − true):

- Mean signed bias **−0.023**, median −0.012 → a small but **systematic
  under-estimate**, not zero-mean noise.
- |bias|: q50 0.048, **q90 0.181**, q95 0.208, max 0.430. RMSE 0.102.
  **95 % limits of agreement [−0.22, +0.17].**
- **α-dependent and directional**: +0.041 at α=0.05 (a floor effect — α can't go
  below 0), −0.03 to −0.05 at α=0.30–0.70 (the likelihood ridge pulling α toward
  the middle).
- **Strongly shape-dependent**: |bias|₉₀ = 0.07 (smooth_growth), 0.07 (flat),
  0.11 (smooth_decline) vs **0.18 (rise_and_fall), 0.20 (regnal_cluster), 0.27
  (bimodal)** — a ~4× range by shape complexity.
- **Does not improve with N** (q90 0.183 at N=2,000 → 0.157 at N=50,000) → a
  structural identifiability limit, not sampling-limited.

**Recommendation.** **Confirm** α-as-diagnostic (the bias is structural and
N-irreducible, so it cannot support a tight gate — this is well-evidenced).
**Revise the operationalisation**: report (i) the 95 % limits of agreement
[−0.22, +0.17] rather than a bare |bias|; (ii) the hedge **conditioned on shape
complexity** (simple-trend subsets ±0.07–0.11; complex/multimodal ±0.18–0.27);
(iii) the directional note (slight under-estimate at mid-high α). "±0.18" is a
defensible worst-case but conceals 4× structure a reviewer can see.

**Literature to confirm.** Bland–Altman limits of agreement; Kruschke ROPE;
simulation-based calibration (Talts 2018; Modrák 2025) for recovery reporting.

---

## (b) Operating-envelope cut (α ≤ 0.70)

**As drafted.** Binding criterion evaluated for α ≤ 0.70; α ≥ 0.95 reported as a
stress sensitivity.

**SME framing.** An operating envelope / **domain of validity** is set where the
performance metric crosses the acceptance threshold; the principled version
locates the **knee** with a fine grid or a changepoint, rather than adopting a
round number.

**What the data say** (Grid A, NON-flat shapes — isolating deconvolution
identifiability from the separate flat-null issue; shape-pass-corrected by α):

| α | 0.05 | 0.30 | 0.50 | 0.70 | 0.95 |
|---|---|---|---|---|---|
| shape-pass | 1.00 | 1.00 | 1.00 | **0.933** | 0.280 |
| median Pearson r | 0.997 | 0.996 | 0.993 | 0.989 | 0.884 |

Reachability study at N = 2,000 fills α = 0.85: shape-rate 1.00 (0.30) → 0.99
(0.50) → **0.82 (0.70)** → 0.34 (0.85). **The cliff is between α = 0.70 and
α = 0.85.** α = 0.70 is the *last* α clearing the 90 % bar; the next available
stress point collapses. (Aside: the lodged α-*coverage* metric is non-monotonic —
0.79, 0.64, 0.63, 0.72, **0.96** across α = 0.05→0.95 — highest exactly where
recovery is *worst*; independent evidence it was the wrong gate.)

**Recommendation.** **Confirm** α ≤ 0.70 as defensible (it is the last passing α;
the cliff is just above it). Two caveats for Martin: (i) 0.70 is **marginal**
(93.3 %, barely above 90 %) — consider labelling α = 0.70 as "boundary /
degrading", reserving "comfortably in" for α ≤ 0.50 (≥ 99 %); (ii) the grid skips
0.85, so the exact knee in (0.70, 0.95) is **unresolved** — a cheap finer-α run
(0.75 / 0.80 / 0.85, a few cells, ~minutes) would pin it and either confirm 0.70
or move the cut. This is the one item where a small additional simulation, rather
than literature, is the highest-value grounding.

**Literature.** Domain-of-applicability / operating-characteristic conventions;
deconvolution / mixture identifiability boundaries.

---

## (c) Headline-B / diagnostic-A + the zero-tolerance divergence gate

**As drafted.** Headline B (count non-converged cells as failures), A reported as
a diagnostic; convergence precondition uses a **zero-tolerance** divergence gate
(`n_divergences == 0` per replicate).

**SME framing.** Divergences in HMC (Betancourt 2017; Stan / PyMC guidance) flag
possibly-biased exploration. The standard is to **investigate** divergences, not
auto-reject — what matters is whether they **bias the posterior** (clustering,
systematic location). A few divergences at a low rate, with correct recovery, are
typically benign. A **zero-tolerance per-replicate** gate is far stricter than
field practice.

**What the data say** (the 24 flat in-envelope cells that create the entire B/A gap):

- Divergence **rate 0.0015 %–0.009 %** of post-warmup draws (12–74 per ~800,000).
- **Recovery is correct** (W1 ≤ 10 y) → the divergences are not biasing the
  recovered curve.
- The divergence counts are numerous enough to account for all the convergence
  failures (R̂/ESS need not be invoked).

**Recommendation.** The **principled lever is the gate, not the reporting.**
Adopt a divergence-**rate** (or small-count) threshold per Bayesian-workflow
norms instead of zero-tolerance. At these rates with correct recovery the flat
cells pass → **headline B ≈ diagnostic A ≈ 98–99 %**, and the B/A distinction and
the flat-null limitation largely dissolve. That is more defensible than choosing
how to *report* a zero-tolerance artefact.

- If the gate is **relaxed** (recommended): B ≈ A; report the single figure; the
  flat-null re-fit backlog item may become unnecessary.
- If zero-tolerance is **kept** (maximally conservative): headline-B is the honest
  call (as drafted), with A as the diagnostic.

**One verification before relying on the relaxation** (needs the per-replicate
posteriors, on sapphire): confirm the *diverging* replicates do not have
systematically worse W1 — i.e. that the divergences are benign rather than marking
a biased sub-population. The correct cell-level recovery already strongly implies
this; the per-replicate check would make it airtight. *Offer: I can pull a few
flat cells' per-replicate data and run this.*

**Literature.** Betancourt 2017 (divergences); Stan / PyMC convergence guidance;
Vehtari et al. 2021 (rank-normalised R̂ / ESS).

---

## (d) Recovery-grid gate scope (letter-mass H3a unaffected)

**As drafted.** The recovery-grid gate bears only on mixture-dependent
(temporal-deconvolution) analyses; Grid B's failure does not touch the letter-mass
cross-sectional H3a confirmatory.

**SME framing.** A validation simulation licenses inferences that **use the
validated component** (estimand). Validity does not transfer to analyses using
different machinery. The grid validates the **temporal mixture deconvolution**
(recovering `p_gen`); H3a cross-sectional regresses per-city letter-mass
**totals** on population — it never invokes the deconvolution.

**Logic / check.** This is a factual scoping point, not a threshold: does the
letter-mass H3a path use the deconvolution anywhere? Per §A5.2 / §A5.5 it uses
totals. If so, the reading is sound — the grid neither validates nor invalidates
H3a, whose validity rests on its negative-binomial regression assumptions,
assessed separately.

**Recommendation.** **Confirm**, conditional on verifying the H3a-letter spec
genuinely uses totals (no temporal deconvolution in its path). This is the
cleanest of the four — a logical scoping point. The one action is to confirm the
H3a specification; no threshold or literature is strictly required.

**Literature.** Minimal; simulation-based-validation scope, if desired.

---

## Cross-cutting

- **Highest leverage: item (c).** Relaxing the divergence gate to a field-standard
  rate threshold is likely the single most consequential change — it is more
  principled than the B-vs-A reporting choice and would collapse the flat-null
  limitation (and possibly retire the backlog re-fit). It needs one cheap
  per-replicate benign-divergence check.
- **Item (a)** is strongly actionable from data alone: condition the α hedge on
  shape complexity and report limits of agreement.
- **Item (b)** is confirmed but marginal; a small finer-α run would pin the knee.
- **Item (d)** is a logical confirm pending the H3a-spec check.
- **What a scout would add:** a focused prior-art-scout on three convention
  questions — (i) HMC divergence tolerance (rate vs zero-tolerance; benign-vs-
  biasing diagnosis); (ii) reporting recovery precision of a parameter (limits of
  agreement / ROPE / tolerance intervals); (iii) defining an operating envelope /
  domain of validity for a recovery simulation — would let the amendment **cite**
  the field standard rather than reason to it. Recommended before lodgement for
  (c) especially.

---

## References (verified 2026-06-04 against CrossRef / arXiv)

The literature these decisions rest on, for the staging Zotero library. DOIs
re-queried against CrossRef 2026-06-04; two details corrected vs the scout draft
(flagged ⚠).

**DOI-verified (CrossRef):**

1. Bland, J.M. & Altman, D.G. (1986). *Statistical methods for assessing
   agreement between two methods of clinical measurement.* The Lancet.
   `10.1016/S0140-6736(86)90837-8` — α limits-of-agreement reporting.
2. Kruschke, J.K. (2018). *Rejecting or Accepting Parameter Values in Bayesian
   Estimation.* Advances in Methods and Practices in Psychological Science.
   `10.1177/2515245918771304` — ROPE.
3. Vehtari, A., Gelman, A., Simpson, D., Carpenter, B. & Bürkner, P.-C. (2021).
   *Rank-Normalization, Folding, and Localization: An Improved R̂…* Bayesian
   Analysis. `10.1214/20-BA1221` — R̂/ESS convergence thresholds.
4. Schad, D.J., Betancourt, M. & Vasishth, S. (2021). *Toward a principled
   Bayesian workflow in cognitive science.* Psychological Methods.
   `10.1037/met0000275` — condition-dependent recovery reporting.
5. Modrák, M., Moon, A.H., Kim, S., Bürkner, P.-C., et al. (**2025** ⚠ — CrossRef
   issued-year 2025, not 2023). *Simulation-Based Calibration Checking for
   Bayesian Computation.* Bayesian Analysis. `10.1214/23-BA1404` — SBC checking.
6. Crema, E.R. & Bevan, A. (**2020/2021** ⚠ — CrossRef issued 2020 online, print
   2021). *Inference from Large Sets of Radiocarbon Dates: Software and Methods.*
   Radiocarbon. `10.1017/RDC.2020.95` — SPD operating-envelope analogue.

**arXiv preprints (canonical; arXiv API rate-limited at verification — IDs
confirmed by the scout):**

7. Talts, S., Betancourt, M., Simpson, D., Vehtari, A. & Gelman, A. (2018).
   *Validating Bayesian Inference Algorithms with Simulation-Based Calibration.*
   `arXiv:1804.06788` — SBC.
8. Gelman, A., Vehtari, A., Simpson, D., et al. (2020). *Bayesian Workflow.*
   `arXiv:2011.01808` — workflow.

**Web case studies / docs (no DOI — add as webpage/blogPost, not via the
DOI batch script):**

9. Betancourt, M. (2017). *Diagnosing Biased Inference with Divergences.*
   `https://betanalpha.github.io/assets/case_studies/divergences_and_bias.html`
   — the primary divergence biasing-vs-benign criterion.
10. Betancourt, M. *Identifying Bayesian Mixture Models.* Stan case study.
    `https://mc-stan.org/learn-stan/case-studies/identifying_mixture_models.html`
    — mixture identifiability boundary.
11. Stan Development Team. *Runtime warnings and convergence problems.* Stan docs.
    `https://mc-stan.org/learn-stan/diagnostics-warnings.html` — divergence
    guidance ("few + good R̂/ESS = often good enough").
12. Modrák, M. (2018). *Taming Divergences in Stan Models.* Blog.
    `https://www.martinmodrak.cz/2018/02/19/taming-divergences-in-stan-models/`.
