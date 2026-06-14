# Hybrid robustness check — spec refresh to the cross-classified structure

**Status:** SPEC REFRESH (2026-06-14). Supersedes the model block (§2) of
`runs/2026-06-09-joint-identifiability/hybrid-robustness-spec.md`, which was written
against the now-superseded single-multinomial lead. The **purpose, the no-pooling
argument (§3), the hierarchical-recovery validation design (§4), and the concordance
test (§5)** of that original spec are unchanged and not repeated here — read them
there. This refresh only updates the per-unit likelihood to the adopted
cross-classified two-subset form and pins the fixed library. UK/Aus English.

## Why (one sentence)

The cross-classified `library` model (adopted; Amendment 04 draft) plugs in
**calibrated θ, fixed** (rule C, κ=40). The hybrid estimates **θ as a single global
pair shared across all units, with a wider prior**, propagating θ's uncertainty, and
asks — via the concordance test — whether the per-unit cross-classified α estimates
survive that relaxation. It is a preregistered robustness annex, not the primary.

## The model (one fit over all U units) — refreshed to cross-classified

```
# --- GLOBAL measurement parameters (shared across units; ESTIMATED, wider prior) ---
θ_conv ~ Beta(μ=0.85, κ=4)          # deliberately WIDER than the lead's κ=40 — the
θ_gen  ~ Beta(μ=0.15, κ=4)          # hybrid LEARNS θ; the identifiable units pin it.
                                    # Prior-sensitivity over κ ∈ {2, 4, 8}.

for u in units:                      # α NOT pooled (units not exchangeable — §3 original)
    α_u            ~ Beta(1, 1)
    tier_weights_u ~ Dirichlet(ones(n_lib))
    p_conv_u        = tier_weights_u · SLAB_LIBRARY     # the FIXED corpus-wide library
                                                        # (production-slab-library.json) — same
                                                        # for every unit, as in the lead
    σ_u            ~ HalfNormal(1)
    z_u            ~ Normal(0, 1, n_bins-1)
    p_gen_u         = softmax(cumsum(σ_u · z_u))        # non-centred GRW (unchanged)

    w_a_u          = α_u·θ_conv + (1−α_u)·θ_gen
    p_aligned_u    = (α_u·θ_conv·p_conv_u     + (1−α_u)·θ_gen·p_gen_u)     / w_a_u
    p_nonalign_u   = (α_u·(1−θ_conv)·p_conv_u + (1−α_u)·(1−θ_gen)·p_gen_u) / (1−w_a_u)

    k_u            ~ Binomial(N_u, w_a_u)               observed = aligned count
    y_aligned_u    ~ Multinomial(k_u,    p_aligned_u)   observed = aligned-subset SPA
    y_nonalign_u   ~ Multinomial(N_u−k_u, p_nonalign_u) observed = non-aligned-subset SPA
```

The **only** structural change vs U independent cross-classified `library` fits is
that θ_conv, θ_gen are **single global scalars** instead of per-unit Beta(κ=40)
priors. Identification (original §2): the identifiable units' sharp α_u + their k_u
jointly pin θ; with θ shared, each confounded unit's k_u + subset contrast then
identifies its α_u. Per-unit data are aoristic-effective counts from
`runs/2026-06-13-cc-production-refit/code/refit_lib.py::build_unit_cc_data`.

## Pilot (this step — one fit on the real 29 units)

A smoke before the validation-population investment (original §4): fit the hybrid
**once** on the 29 production units and check
1. **Sampler health** — max R̂ < 1.01, min bulk-ESS ≥ 400, divergences benign on the
   larger joint geometry (~U × (n_bins−1) GRW + U tier_weights + U α + 2 global θ ≈
   3,100 parameters). If it regresses: target_accept 0.95 → 0.97, then reparameterise.
2. **Global θ** — posterior vs the calibrated (0.945, 0.155); inside the wide prior?
3. **Concordance (preview)** — do the cross-classified per-unit α medians
   (`refit-summary.json`) fall inside the hybrid's per-unit α 95% CIs, and is the
   mean discrepancy < 0.05? (The full concordance verdict, original §5, is scored
   after the hierarchical-recovery validation certifies the hybrid's intervals.)

**Gate to advance:** sampler healthy AND θ sane AND no gross concordance breakdown ⇒
build the hierarchical-recovery validation (original §4: ~24 synthetic units, known
per-unit α + known global θ, ≥10 population replicates) before trusting the hybrid's
intervals for the lodged concordance result. Otherwise: report and adjudicate.

## Outputs

`outputs/hybrid-pilot.json` (per-unit α + global θ + convergence + concordance preview)
and `HYBRID-PILOT-REPORT.md` (committed). The single joint fit's posterior is
gitignored (regenerable).
