---
title: "H3a design artefact — prior-predictive and posterior-predictive numerical thresholds (pinned pre-confirmatory)"
scope: "The H3a cross-sectional Bayesian within-between (Mundlak) NBR. Pins the numerical PPC / prior-predictive thresholds the lodged preregistration commits to fixing 'before any pilot fit is inspected' (prereg §3 lines 251, 265; Decision 21 / Decision 25)."
status: "ACTIVE — pinned 2026-06-04, committed before the confirmatory H3a fit. The H3a portion of the broader pre-Phase-2 design artefact (the recovery-grid-design and template-dictionary portions were handled separately / are not needed for the cross-sectional track)."
date: 2026-06-04
author: "Shawn Ross (PI) with Claude Code (analyst/RSE)"
related:
  - planning/preregistration-draft.md (§3 H3a spec, lines 212–269; PPC spec lines 250–265)
  - planning/decision-log.md (Decision 21, 25 — numerical PPC triggers + two-tier severity; Decision 35 — H3a-first sequencing)
  - planning/h3a-confirmatory-launch-spec-2026-06-04.md (the launch spec that consumes this artefact)
  - runs/2026-05-21-talk-prep/code/05-h3a-bayesian-mundlak.py (the preliminary/exploratory model code — clean of result values)
---

# H3a design artefact — numerical PPC / prior-predictive thresholds

## 0. Why this document exists, and the contamination disclosure

The lodged preregistration commits to pinning the H3a prior-predictive and
posterior-predictive (PPC) **numerical thresholds in a design artefact *before any
pilot fit is inspected*** (prereg §3 lines 251, 265; Decisions 21 and 25). This is
a preregistration-integrity device: thresholds chosen *after* seeing a fit can be
(even unconsciously) tuned so the model passes. This file pins those thresholds.

**Transparency disclosure (required reading).** A *preliminary* H3a fit was run at
the 2026-05-21 RAC-TRAC talk-prep (`runs/2026-05-21-talk-prep/`), explicitly as
exploratory post-lodgement work for a conference talk. That run produced a
**preliminary `f_within` posterior** (the estimand) and a basic observed-vs-predicted
scatter. It did **not** compute the formal PPC test statistics below against any
threshold. The exposure is therefore to the *estimand* (`f_within`), which is
**orthogonal** to the model-fit diagnostics pinned here (proportion of zeros, mean,
SD, tail percentile, mean–variance ratio, residual structure, residual spatial
autocorrelation) — knowing `f_within` tells you nothing about whether the predicted
*count distribution* matches the observed one. Two mitigations apply regardless:

1. **These thresholds are pinned from prior-predictive reasoning and statistical
   convention, not from any observed fit.** Where a threshold is *data-shaped* (the
   count cap and tail bounds), it is derived from a **prior-predictive simulation**
   (draws from the priors only, no observed `y`), computed and committed as the
   first step of the confirmatory run, before the confirmatory fit.
2. **The confirmatory pipeline is run by a fresh agent blind to the preliminary
   results** (the launch spec's §"Blind-run protocol"). It re-derives every number
   from the prereg + the data and never reads the talk-prep output tables, figures,
   or REPORT.

If, despite this, a reviewer judges the preliminary `f_within` exposure material,
the fallback is to report the confirmatory `f_within` as "pre-specified analysis,
estimand previously seen at exploratory talk-prep" — honest labelling, not a hidden
deviation.

## 1. The model these thresholds apply to (reference)

Per prereg §3 (lines 212–227), unchanged:

```text
y_c ~ NegativeBinomial(mu_c, dispersion)
log(mu_c) = α_0 + α_province[c]
            + β_within  · (log_pop_c − log_pop_province_mean[c])
            + β_between · log_pop_province_mean[c]

α_0 ~ Normal(0, 5);  β_within ~ Normal(0, 1);  β_between ~ Normal(0, 1)
α_province ~ Normal(0, σ_prov);  σ_prov ~ HalfNormal(1);  1/dispersion ~ HalfNormal(1)
```

Sample (Decision 35A): **1,044 Hanson-matched cities, Rome-excluded** (the
prereg-text-faithful "all cities with Hanson population estimates, Rome excluded";
see the launch spec for the 1,044-vs-815 reconciliation). `y_c` is the per-city
**date-window-filtered** (50 BC – AD 350) inscription count; the mixture is NOT
applied (Decision 22 / Decision 35 addendum).

## 2. Prior-predictive thresholds (data-shaped → derived by simulation; committed before the fit)

Computed by drawing `S_pp = 1,000` parameter sets from the priors above, simulating
`y_c` for every city from the model (using only the **predictor** matrix `log_pop`,
province index — NOT observed counts), and reading the quantiles off the simulated
counts. These are pinned by the **rule**, with the realised **values** computed and
committed by the confirmatory run's first step (`prior-predictive.py`) before any
posterior fit.

| Threshold | Derivation rule | Use |
|---|---|---|
| `count_cap_p99` | 99th percentile of prior-predictive per-city counts across all draws × cities | Sanity ceiling — a confirmatory posterior-predictive 95th percentile above this flags a prior–data conflict |
| `tail_count_bound` | 99.9th percentile of prior-predictive per-city counts | Upper bound for the PPC "95th percentile" test statistic (§3) |
| `ppc_mean_ref` | mean of prior-predictive counts (recorded for context, not a gate) | Diagnostic context |

**Pre-registration note:** the prior-predictive simulation must also satisfy a
sanity gate before the model is used at all — the simulated counts must not be
absurd (e.g. median per-city count within [0.1, 10^4]). If the prior-predictive
counts are absurd, the priors are revisited (and an amendment filed) *before* any
confirmatory fit. This is a prior-sanity check, not a model-fit check.

## 3. Posterior-predictive test-statistic thresholds (judgment-pinned from convention)

Pinned now from statistical convention (forward-looking; not data-derived). For
each statistic: compute the observed value `T_obs`, and the posterior-predictive
distribution `T_rep` (one value per posterior draw); the **Bayesian p-value** is
`p_B = P(T_rep ≥ T_obs)`; the **bound** is the tolerance band below.

| # | Test statistic | Bound (pass band) | Rationale |
|---|---|---|---|
| 1 | **Proportion of zeros** | observed = 0 by construction (cities enter from LIRE rows, so each has ≥ 1); posterior-predictive prop-zeros ≤ 0.02 | NBR sanity. **NB:** if Decision on zero-inscription Hanson cities (launch-spec open item) adds structural zeros, this bound is re-pinned to ±0.05 absolute before the fit. |
| 2 | **Mean count** | posterior-predictive mean within ±10 % of observed mean | Central tendency; 10 % is a tight but achievable band for a well-specified count mean |
| 3 | **SD of counts** | posterior-predictive SD within ±25 % of observed SD | Counts are over-dispersed; SD is harder to match than the mean, so a wider band |
| 4 | **95th percentile** | observed 95th pct ≤ `tail_count_bound` (§2) AND posterior-predictive 95th pct within ±30 % of observed | Tail adequacy |
| 5 | **Mean–variance ratio** | posterior-predictive ratio within [0.5×, 2×] of observed | Dispersion adequacy — the core NBR assumption |
| 6 | **Bayesian p-values** (for #2–#5) | 0.05 ≤ p_B ≤ 0.95 | Standard PPC central band; outside is a flag |

## 4. Residual-structure thresholds (judgment-pinned)

| # | Check | Bound | Rationale |
|---|---|---|---|
| 7 | **Residual-vs-fitted slope** | \|OLS slope of standardised Pearson residuals on fitted log-μ\| < 0.10 | A near-flat residual cloud; a real trend indicates link/structure mis-fit |
| 8 | **Residual-vs-within-`log_pop` slope** | \|slope\| < 0.10 | No leftover population trend in residuals |
| 9 | **Province-level residual dispersion** | per-province mean \|residual\| within [0.5×, 2×] of the overall mean \|residual\| (provinces with n ≥ 5 cities) | No province grossly mis-fit by the random intercept |

## 5. Posterior-predictive spatial-autocorrelation threshold (prereg default)

| # | Check | Bound | Rationale |
|---|---|---|---|
| 10 | **Posterior-predictive Moran's I on residuals** (k = 8 primary) | observed Moran's I (H3c(ii) posterior-mean residual) lies within the 5th–95th percentile of the posterior-predictive Moran's-I distribution | Prereg §3 line 258 default; outside ⇒ the model cannot generate the observed residual spatial structure under its own posterior (tautology caveat on H3c(ii)) |

## 6. Two-tier severity (prereg §3 lines 260–265)

A tripped trigger's severity is judged against its bound's magnitude:

- **Critical** — value outside the bound by **> 2×** the bound's magnitude, or (for
  directional bounds — the residual slopes #7/#8) an unexpected **sign** with
  \|slope\| ≥ 0.10. → **model revision** (priors, link, or structure); the
  originally-preregistered model result reported alongside the revised model; an
  **OSF amendment filed before final results are lodged**.
- **Minor** — value outside the bound by **≤ 1.5×** the bound's magnitude (tripped
  but marginal). → reported as a **caveat** in the paper; no model revision; no
  amendment.
- The band **between 1.5× and 2×** is adjudicated case-by-case and reported with the
  reasoning (this is the prereg's straw-cutoff grey zone).

These 1.5× / 2× cutoffs are the prereg straw values applied uniformly across
categories #1–#10, with one tightening: for **proportion of zeros** (#1) the
critical cutoff is an **absolute** 0.10 (not a multiple of the ~0 bound), since a
multiplicative cutoff on a near-zero bound is undefined.

## 7. What is NOT gated on a PPC

No PPC trigger tests a hypothesis (prereg §3 line 265). The H3a confirmatory verdict
is the three-way `f_within` rule (prereg §3 lines 243–245); H3c(ii) is the Moran's-I
permutation rule. The checks here are model-adequacy diagnostics that condition
*interpretation* (caveats) and, at critical severity, trigger model revision +
amendment — they never decide `f_within`.
