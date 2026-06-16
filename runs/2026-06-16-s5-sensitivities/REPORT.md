# §5 sensitivity batch — D11, D12 results + B4 scope (2026-06-16)

> **DRAFT — exploratory.** Preregistered §5 sensitivities for H3a (prereg §5; not
> confirmatory; material divergence is a reported limitation, never an amendment
> trigger). Run on the primary 1,044-city Hanson frame; anchored to the committed
> H3a confirmatory run (`runs/2026-06-04-h3a-confirmatory/`, primary f_within
> **0.299 [0.240, 0.365]**). Numbers from `outputs/d11-…json` / `outputs/d12-…json`.

## D11 — Hanson-population measurement-error sensitivity

Re-fit the within-between (Mundlak) NBR with the **preregistered** ME model
`log_pop_c ~ Normal(log_pop_observed_c, σ_pop)` (Berkson prior centred on the
observed value; the Mundlak within/between components are recomputed from the latent
population each draw). σ_pop = low/moderate/high.

| σ_pop | f_within | 95% CI | verdict | CI shift vs primary | material? |
|---|---|---|---|---|---|
| — (primary) | 0.299 | [0.240, 0.365] | supported | — | — |
| 0.1 | 0.305 | [0.243, 0.373] | supported | 0.008 | no |
| 0.2 | 0.320 | [0.255, 0.390] | supported | 0.025 | no |
| 0.3 | 0.341 | [0.277, 0.412] | supported | 0.047 | no |

**f_within is robust to Hanson-population measurement error.** It drifts gently
upward with σ_pop (ME adds within-province variance), but every σ stays "supported"
and the largest CI shift (0.047 at σ=0.3) is **below the prereg's material-divergence
threshold** (50% of the primary CI width = 0.063). Convergence clean throughout
(R̂ ≤ 1.01, ESS-bulk ≥ 1,080, 0 divergences; tune 4,000 / draw 2,000 × 4). **No
material divergence; no limitation flagged.**

## D12 — scaling-residual sensitivity

Construction (documented design choice — flag if a different reading is intended):
pooled NBR power-law `insc ~ NB(exp(a + β·log_pop), φ)` → per-city SAMOC log-residual
`r_c = log(insc_c) − (â + β̂·log_pop_c)` → Gaussian within-between partition of `r_c`.

- Pooled power-law slope **β = 0.565** (cf. the primary H3a within-province β = 0.587;
  Hanson 2021 ≈ 0.67).
- Residual **β_within = −0.065 [−0.144, +0.011]**, P(>0) = 0.05; residual f_within
  **≈ 0.004 [0.00, 0.02]**. Convergence clean (R̂ 1.00, 0 div).

**Interpretation — a coherence result, not a refutation.** After removing the global
pooled scaling, the within-province population gradient on the residuals is
essentially zero. This means the within-province slope ≈ the global slope
(≈ 0.57–0.59): **the Hanson population relationship operates as one consistent scaling
law at both levels**, so "controlling for scaling" leaves no extra within-province
structure. It does **not** mean the within-province correlation is spurious — the
primary β_within (0.587, CI well above 0) is real; D12 shows it is the *same* law as
the global scaling, not a province-specific artefact. So the Hanson correlation
"survives" in the sense that it is a genuine, unified scaling relationship.

*Caveat:* the residual definition (SAMOC log-residual) and the Gaussian re-run are
documented choices; the prereg phrasing ("re-run H3a on residuals") is terse. If you
intended, e.g., a count-model residual or a different estimand, this is a quick re-run.

## B4 — Phase-1 stratified-sampling sensitivity — RESOLVED (robust)

**Outcome (2026-06-16).** Reading the v2 harness revealed B4 is **architecturally moot
as written** — Decision 8 replaced the LIRE bootstrap with synthetic-data-from-null, so
the only empirical lever is the interval-width pool (province/city counts are vestigial).
The v2-faithful B4 was then run in two steps:

1. **Width-pool diagnostic** (`outputs/REPORT-b4.md`): scheme (a) proportional-allocation
   is **threshold-neutral by construction**; scheme (b) reweight-to-balance shifts the
   width pool (city-balanced median width 99y → 79y; over-represented big cities carry
   wider intervals).
2. **Scheme-(b) threshold re-run** (`outputs/REPORT-b4-rerun.md`): re-ran the threshold
   cells under global / province-balanced / city-balanced width pools at matched
   precision. **Thresholds are robust** — median Δ **−1.1%** (province-balanced) / **−0.4%**
   (city-balanced), in the expected direction (narrower → easier detection) but tiny and
   within the n_iter=200 Monte-Carlo noise, and **no reachability classifications change**
   (0 cells flip reachable↔unreachable).

**Conclusion:** the Phase-1 detection thresholds are robust to province/city stratification
under both schemes. **Recommend recording B4 in the obligations audit as superseded by
Decision 8 (no LIRE bootstrap in v2), satisfied via this width-pool check.** The committed
full-precision thresholds (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`) stand.

<details><summary>Original scope (now executed)</summary>

Prereg (§5, Phase-1 supplementary): "Phase 1 thresholds use bootstrap
(sampling-with-replacement) from filtered LIRE; thresholds are recomputed using
stratified-sampling (province-proportional **or** city-proportional draws). Reports
deltas to bootstrap primary."

Not executed here — it is **Phase-1 machinery** (the H1 detection-threshold
simulation, `runs/2026-04-25-h1-simulation/`), separate from the H3a sensitivity
harness, and the prereg offers a **choice of stratification scheme**. Rather than
guess the scheme and dive into the Phase-1 code blind, it is flagged:

- **Decision needed:** province-proportional, city-proportional, or both? (Recommend
  **province-proportional** as the headline — it directly addresses the Rome/Ostia
  over-representation that motivates the check — with city-proportional as a second
  panel if wanted.)
- **Effort:** ~half-day. Reuse the Phase-1 harness; swap the bootstrap resampling step
  for stratified draws; recompute the minimum-N detection thresholds; report deltas to
  the committed bootstrap primary (`runs/2026-04-25-h1-simulation/outputs/h1-v2/`).
- **Stakes:** low (Phase-1 robustness supplementary); no downstream analysis gates on
  it.

</details>

## Summary

All three §5 items **corroborate the existing results**: f_within is robust to population
measurement error (D11); the within-province scaling is one coherent law with the global
scaling (D12); and the Phase-1 detection thresholds are robust to province/city
stratification (B4 — both schemes, median Δ ~−1%, no reachability change), with B4
recorded as superseded-by-Decision-8 and satisfied via the width-pool check.

## Reproduce
```bash
# sapphire:
uv run python runs/2026-06-16-s5-sensitivities/code/d11_hanson_me.py
uv run python runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py
```
