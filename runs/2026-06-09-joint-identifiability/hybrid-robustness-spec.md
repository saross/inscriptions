# Hybrid model (Option 3) — preregistered robustness check spec

**Status:** SPEC (Shawn-agreed 2026-06-09: per-unit + classification is the LEAD; this
hybrid is the **preregistered robustness check** that corroborates it). Not the primary
analysis. **Date:** 2026-06-09. **Author:** Claude Code (Opus 4.8). UK/Aus English.

## 1. Purpose

The lead design (`full-grid-spec.md`) fits each unit independently with the θ alignment
rates **calibrated-then-fixed** (a plug-in empirical-Bayes step that ignores θ
uncertainty). The hybrid model **estimates θ inside a single joint fit** so its
uncertainty is propagated, and then asks: **do the cheap per-unit α estimates sit inside
the hybrid's α intervals?** If yes, we report the per-unit model as primary with the
hybrid as corroboration; if they diverge materially, the divergence is itself the finding
and we escalate the hybrid to primary.

This is the statistically-rigorous check (statistical best-practice estimates the
covariate effects — Huang & Bandeen-Roche 2004 — rather than plugging them in) without
betting the primary analysis on the larger, harder-to-validate joint fit.

## 2. The model (one fit over all U units)

```
# --- GLOBAL measurement parameters (shared across units; ESTIMATED) ---
θ_conv ~ Beta(μ=0.85, κ=4)          # weakly-informative; the identifiable units pin it
θ_gen  ~ Beta(μ=0.15, κ=4)          # weakly-informative
# NOTE: deliberately WIDER than the lead's κ≈12 — the hybrid LEARNS θ, it must not
# impose the calibration. Prior-sensitivity over {Beta(·,2), Beta(·,4), Beta(·,8)}.

for u in units:                      # INDEPENDENT per unit — α is NOT pooled (see §4)
    α_u            ~ Beta(1, 1)
    tier_weights_u ~ Dirichlet(ones(n_tiers))
    p_conv_u        = tier_weights_u · BASIS_u        # per-unit aligned-subset basis
    σ_u            ~ HalfNormal(1)
    z_u            ~ Normal(0, 1, n_bins-1)           # non-centred GRW
    p_gen_u         = softmax(cumsum(σ_u · z_u))
    y_u            ~ Multinomial(N_eff_u, α_u·p_conv_u + (1-α_u)·p_gen_u)   # temporal
    k_u            ~ Binomial(N_rows_u, α_u·θ_conv + (1-α_u)·θ_gen)         # classification
```

The **only** structural change vs U independent lead-model fits is that θ_conv, θ_gen are
**single global parameters** instead of per-unit fixed priors. Identification: the
identifiable units (sharp temporal α_u) + their k_u jointly estimate θ; with θ shared,
each confounded unit's k_u then identifies its α_u given the estimated θ. This is a
concomitant-variable mixture with **shared measurement parameters across groups**.

## 3. Why α is NOT pooled (Option 3, not Option 4)

Partial-pooling α_u toward a population mean assumes the units are exchangeable; ours are
not (frontier vs core differ systematically in epigraphic regime), and pooling would
shrink the genuine extremes (Pompeii ≈ 0, Noricum ≈ 0.88) — **masking the very per-unit
deviations H3b is built to detect.** So α_u stays independent Beta(1,1). The hybrid's
contribution is *estimating θ*, not *pooling α*.

## 4. Validation (a NEW hierarchical recovery design)

The cell-by-cell recovery grid does not validate a joint fit. Build a hierarchical
recovery population:

- U_synth ≈ 24 synthetic units with **known** α_u spanning [0, 0.9] (mix of identifiable
  and confounded regimes, realistic per-unit broad-slab convention + peaked genuine), a
  **known global** (θ_conv, θ_gen), and N_u ∈ {1500, 2800, 15000}.
- Generate (y_u, k_u) per unit (well-specified Tier-1; plus an interval-level Tier-2
  subset). Fit the hybrid once. **Recover:** global θ (bias + coverage), per-unit α_u
  (bias + coverage), and check the joint sampler's health.
- Repeat over ≥ 10 population replicates (different seeds / α-draws).

**Hybrid acceptance:** global θ recovered within ±0.05; per-unit α_u |bias| < 0.18 with
≥ 0.90 coverage; sampler converges (max R̂ < 1.01, min bulk-ESS ≥ 400, divergences benign).

## 5. Concordance test (the actual robustness check, on the real data)

After both models are fit to the 28 production units:

- For each unit, compute whether the **per-unit α median sits inside the hybrid α 95 %
  CI** (and the reverse), and the **per-unit-vs-hybrid α median discrepancy**.
- **Concordant verdict (report per-unit as primary, hybrid as corroboration):** ≥ 90 %
  of units concordant AND no systematic shift (|mean discrepancy| < 0.05) AND the hybrid's
  estimated θ within the lead's calibrated θ ± its prior sd.
- **Divergent verdict (escalate):** material systematic shift or many discordant units →
  investigate; if the hybrid is better-calibrated, promote it to primary. Either way the
  divergence is reported, not hidden.

## 6. Build + cost

- One PyMC model, U × (n_bins-1) GRW params (≈ 28 × 79 ≈ 2,200) + per-unit tier_weights
  + per-unit α + 2 global θ. Non-centred throughout; careful init; possibly
  target_accept 0.97. Runtime minutes–~1 h on sapphire (single fit; not embarrassingly
  parallel like the lead). Validation population fits add the bulk of the compute.
- Reuses `build_model_joint`'s components; the joint-over-units assembly is the new code.

## 7. Sequencing

Gated **after** the lead per-unit model passes its full recovery grid (`full-grid-spec.md`
§3). The hybrid validation + concordance test then runs as the robustness annex. Both are
folded into the single OSF amendment (the lead as method, the hybrid as preregistered
robustness).

## 8. Open question for the build

Whether to also fit a **θ-varies-by-unit-covariate** variant (frontier vs core) to test
the residual θ-transferability directly (the one thing even the global-θ hybrid cannot
detect). Logged; decide at build time — likely a third tier if the concordance test
flags frontier units specifically.
