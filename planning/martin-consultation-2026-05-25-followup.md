# Martin consultation 2026-05-25 — follow-up pack

**Authored:** 2026-05-24, Claude Opus 4.7 (1M context), driven by Shawn Ross.
**Builds on:** `planning/martin-consultation-pack-2026-05-17.md` and Martin's still-pending reply to its eight questions. This pack is **net-new content** triggered by the H2.1 recovery-grid run that completed 2026-05-23 12:07 and the four diagnostic investigations that followed.

---

## 1. Headline (one paragraph)

The H2.1 mixture-model recovery grid (450 cells × 100 replicates) **FAILS** the prereg-binding criteria: 63.6 % of cells pass α-coverage and 69.8 % pass shape-Pearson-r against the ≥ 90 % threshold. Four diagnostic investigations have narrowed the mechanism to two distinct issues: (1) a **systematic downward bias in posterior α** that begins at α_true = 0.30 (mean bias −0.04), saturates by α_true = 0.70 (−0.06), and is **structural** — neither prior re-specification (F1) nor non-centred reparameterisation (F3) moves it materially; and (2) a **shape-metric mismatch** in which Pearson r is mathematically inapplicable to flat truths (returns NaN on `flat_baseline`) and is mass-blind in exactly the `regnal_cluster` regime where the model is worst. A W-1 ≤ 18.6 years threshold reproduces the current Pearson r ≥ 0.95 selectivity on non-flat cells (83.7 % pass) and gives a defensible, distribution-sensitive replacement. **What's left for Martin is the structural identifiability question** — neither of the two cheap fixes worked, so the next move requires guidance on the model itself.

---

## 2. What we did (four investigations)

| Investigation                | Scope                                                            | Compute            | Verdict                                                                                                           | Report                                                                          |
| ---------------------------- | ---------------------------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Experiment A (preceding)     | 3 α=0.95 cells × 3 sampler-effort tiers (9 fits)                | 619 s wall          | Bias is misspecification, not sampler effort. R-hat → 1.00, ESS → 250, divergences → 0; α stays pinned at 0.74–0.86 | `runs/2026-05-24-validation-investigation/outputs/REPORT.md`                    |
| Experiment B (preceding)     | 5 `flat_baseline` cells, existing posteriors only                | ~10 s              | Flat recovery is genuinely accurate (var ~10⁻⁹, max|dev| ~10⁻⁴, W-1 ≤ 0.7 y); Pearson r just inapplicable        | same file as above                                                              |
| F0 (systematics)             | All 450 cells, no new fits                                       | ~7 min analysis    | Bias is **not specific to α=0.95**; starts at α=0.30, saturates by α=0.70. W-1 ≤ 18.6 y matches current selectivity | `runs/2026-05-24-followup-systematics/outputs/REPORT.md`                        |
| F1 (sharper α prior)         | Same 3 cells × 3 tiers, swap Beta(2,2) → Uniform(0,1) on α       | 610 s wall          | Δα = +0.025 mean. **Bias is structural, not prior-pull.**                                                         | `runs/2026-05-24-followup-alpha-prior/outputs/REPORT.md`                        |
| F3 (non-centred GRW)         | Same 3 cells × hardest, non-centred parameterisation              | 336 s wall          | Δα = +0.001 mean. **Bias is NOT funnel geometry.** But ESS-bulk 45–50× higher → adopt non-centred anyway        | `runs/2026-05-24-followup-noncentred-grw/outputs/REPORT.md`                     |

Compute audit: all on sapphire (Ryzen 9 7900, 12 physical cores) with `TMPDIR` redirected to disk-backed scratch (post `/tmp` inode catastrophe of 2026-05-22), `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`, single-threaded BLAS, no numpyro. Hard-stop rule honoured throughout: zero silent parameter renegotiation.

---

## 3. Empirical α-bias map (F0a, refined)

The bias profile, marginalising over shape, tier_weights, and N:

| α_true | mean recovered α | bias_mean | bias_std | n_cells |
| -----: | ---------------: | --------: | -------: | ------: |
| 0.05   | 0.120            | **+0.070** | 0.068 | 90 |
| 0.30   | 0.290            | **−0.010** | — | 90 |
| 0.50   | 0.456            | **−0.044** | — | 90 |
| 0.70   | 0.640            | **−0.060** | — | 90 |
| 0.95   | 0.885            | **−0.065** | — | 90 |

Key observations:

- At α=0.05 the bias is **positive** (+0.070) — the model over-estimates α at the low-signal extreme. Combined with the high-α negative bias, this suggests a **two-sided pull toward the middle**, consistent with a Beta(2, 2) prior centred on 0.5 plus a likelihood ridge that allows mass swapping between α and p_gen complexity.
- Shape-level heterogeneity is real. `regnal_cluster` shows **positive bias** at α ≤ 0.50 then crosses to **negative bias** at α ≥ 0.70 — a bidirectional pattern. The bias direction depends on whether the convention component or the generative component is structurally simpler relative to the truth.
- F1 showed that loosening the prior to Uniform(0, 1) only moves the α=0.95 posterior by +0.025 — so the bias is *mostly* not from the Beta(2, 2) prior. It is *mostly* from the likelihood ridge.

---

## 4. What the F1 and F3 negatives mean

Per the diagnostic investigation's three-candidate fix list:

- **A1 (sharper α prior)** — ruled out by F1. Even Uniform(0,1) leaves bias ≥ 75 % of its original magnitude.
- **A2 (non-centred GRW)** — ruled out by F3. Same posterior location, just sampled much more efficiently.
- **A3 (formal identifiability investigation)** — *now the only remaining cheap-ish path*. This is the consultation question.

F3 has a positive side-finding worth flagging independently: **non-centred GRW should be adopted as the default** for the H2.1 model in Phase 2. ESS-bulk improved 45–50× at no cost in posterior accuracy. The change is mathematically equivalent to the current parameterisation (verified by F3's prior-equivalence check). This is a clean methodological win even though it does not solve the α-bias.

---

## 5. Shape-metric proposal (F0b, refined)

| metric / threshold                       | pass rate on non-flat cells | implication                                                       |
| ---------------------------------------- | --------------------------: | ----------------------------------------------------------------- |
| Pearson r ≥ 0.95 (current binding)       | 83.7 %                      | mass-blind in `regnal_cluster`; NaN on `flat_baseline`           |
| W-1 ≤ 18.6 years (matched selectivity)   | 83.7 %                      | distribution-sensitive; defined on `flat_baseline`                |
| W-1 ≤ 5 years (one bin width)            | 28.8 %                      | substantially stricter; principled threshold but unlikely to pass at α near 1 |

For `flat_baseline` cells: max W-1 across α ≤ 0.70 is 4.22 years (60 cells). The α=0.95 `flat_baseline` cell jumps to W-1 = 23.2 years — the same α-boundary pathology as Experiment A appears here too, confirming it's not a shape-dependent artefact.

**Proposal**: replace Pearson r with W-1 as the primary binding shape metric, with two thresholds reported (matched-selectivity 18.6 y and principled-stricter 5 y) and the choice deferred to Martin.

---

## 6. Updated questions for Martin

Supersedes the four questions in `runs/2026-05-24-validation-investigation/outputs/REPORT.md §4`. Brings in the F0/F1/F3 results.

**Q1 — Structural identifiability between α and p_gen complexity.** The mixture `p = α·p_conv + (1−α)·p_gen`, with p_conv a fixed tier-weighted basis and p_gen a flexible smoothed log-density, has a likelihood ridge between (high α + structured p_gen) and (lower α + smoother p_gen). The recovery grid shows mean bias of **−0.04 by α=0.30 and −0.06 by α=0.70**, then flat to α=0.95. Neither Uniform(0, 1) prior (Δα = +0.025) nor non-centred GRW (Δα = +0.001) materially shifts the posterior. **What is your next move?** Specifically:
  - (a) Is there a re-parameterisation of the mixture that breaks the ridge — e.g. an ordered-mixture parameterisation with a hyper-prior on the contrast between p_conv and p_gen complexity?
  - (b) Would a more rigid p_gen prior (e.g. Dirichlet process with tighter concentration, or a Gaussian process with a fixed length-scale prior anchored to the convention's typical structure) constrain the ridge enough?
  - (c) Is the ridge inherent and we should report it as a regime limit ("the model is valid only for α ≤ 0.30 ± ε")?

**Q2 — Bidirectional bias in regnal_cluster.** The `regnal_cluster` shape has **positive** mean bias at α ≤ 0.50 and **negative** bias at α ≥ 0.70. This is shape-specific — none of the other five shapes flip sign. Does this suggest the model is re-attributing signal between p_conv and p_gen *in the wrong direction* for this shape, and if so, is there a diagnostic that would pre-flag this in real-data work where we don't know the truth?

**Q3 — Binding shape metric.** We propose replacing the Pearson r ≥ 0.95 binding criterion with W-1 ≤ T years, with T either 18.6 (matched selectivity to current rule on non-flat cells) or 5 (one bin width; principled-stricter). The Pearson r criterion is undefined on `flat_baseline` and mass-blind in `regnal_cluster` (per F0b table). **Which threshold would you anchor on, and would you keep Pearson r as a co-binding metric, or replace it outright?**

**Q4 — Adopt non-centred GRW unconditionally.** ESS-bulk improved 45–50× under non-centred parameterisation at no cost in posterior accuracy (F3). Mathematically equivalent to current; just better sampler geometry. We propose adopting this as the production parameterisation regardless of the bias question's resolution. **Any objection?**

**Q5 — Partitioning the FAIL budget.** Marginal pass-rates from the grid:

|             | shape         | bimodal | flat_baseline | regnal_cluster | rise_and_fall | smooth_decline | smooth_growth |
| ----------- | ------------- | ------: | ------------: | -------------: | ------------: | -------------: | ------------: |
| both        | %             | 29      | 0             | 19             | 33            | 83             | 81            |
| α-cov only  | %             | 35      | 89            | 31             | 44            | 93             | 89            |
| shape only  | %             | 72      | 0             | 84             | 87            | 88             | 88            |

Of the 59.1 % grid-wide FAIL, our reading is approximately:
  - ~25 % is metric mismatch (`flat_baseline` shape — fully fixable by switching to W-1; Q3 above)
  - ~30 % is α-regime limit (α ≥ 0.70 across most shapes — needs the Q1 structural answer)
  - ~5 % is `regnal_cluster`-specific bidirectional bias (needs Q2)

**Does this partition match your intuition?** If yes, the prereg amendment can address parts (i) and (iii) cheaply and proceed on Phase 2 with a documented regime caveat on (ii) while we work on the structural identifiability fix.

**Q6 — Replicate count for follow-up diagnostics.** All four investigations fit a single representative replicate per cell (rep 000). The original grid's 100 replicates per cell is overkill for a diagnostic. **Is 10 a defensible diagnostic-tier replicate count?** Specifically for verifying the structural-bias verdict in Q1 across replicate variability before we commit to a model fix.

---

## 7. Recommended pre-empt — non-blocking actions while waiting for Martin

If Martin's reply takes more than ~ 48 h, the following are safe to proceed on without his input:

1. **Adopt non-centred GRW** in the production fit code (`code/02-mixture-fit.py` → diff against `runs/2026-05-24-followup-noncentred-grw/code/02-mixture-fit-noncentred.py`). Equivalence is verified; sampler quality improves substantially.
2. **Generate the W-1 distribution figures** at the per-cell level (already in `runs/2026-05-24-followup-systematics/outputs/figures/`) and circulate to potential co-authors for sense-check on the threshold choice.
3. **Multi-replicate verification** (10 replicates × hardest × 3 α=0.95 cells, ~ 1 h sapphire compute) — confirms the bias is replicate-robust.

Items blocked on Martin:
- Re-running the full 450-cell grid (~ 30 h compute) under any structural fix.
- Drafting the OSF amendment.
- Final wording of the prereg-binding-criteria revision.

---

## 8. Provenance

| Artefact | Path | Type |
| -------- | ---- | ---- |
| This synthesis | `planning/martin-consultation-2026-05-25-followup.md` | Markdown |
| Diagnostic investigation report (Experiments A + B) | `runs/2026-05-24-validation-investigation/outputs/REPORT.md` | Markdown |
| F0 (systematics) report + 5 figures + 11 CSV tables + script | `runs/2026-05-24-followup-systematics/` | Tree |
| F1 (sharper α prior) report + 9 posteriors + 3 figures + script | `runs/2026-05-24-followup-alpha-prior/` | Tree |
| F3 (non-centred GRW) report + 3 posteriors + 3 figures + 2 scripts | `runs/2026-05-24-followup-noncentred-grw/` | Tree |
| 450-cell grid (production) | `runs/2026-05-22-recovery-grid-validation/` | Tree (commit `3df0d2c`) |
| Grid design + binding criteria | `runs/2026-05-22-recovery-grid-design/spec.md` | Markdown |

Compute audit: all on sapphire. Hard-stop rule honoured. No silent parameter renegotiation in any of the four investigations.

End of consultation pack.
