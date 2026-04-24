---
priority: 2
scope: in-stream-reference
title: "Summary — 2024 archived exploratory work on Latin inscription SPA"
audience: "future CC instances, Shawn after a break, Adela"
status: committed 2026-04-23
source: "archive/ — Jupyter notebooks dated 2023-09-08 and 2026-04-22"
---

# 2024 exploratory work — summary for persistent reference

Compact record of what was done in 2023–2024 in `archive/`, what worked, what failed, what carried forward to 2026. Committed so future sessions can consult it without re-running an agent over the notebooks.

## What the 2024 work asked

Exploratory, not a tight hypothesis: **"Does the SPA profile of Latin inscriptions resemble known Roman population history?"** Target: 50 BC – AD 350 empire-wide, provincial, and urban-area SPAs. Comparison to Hanson (2021) population–inscription regression as anchor.

Shawn's own 2024 "Reflections" framing (quoted verbatim from the archived notebook):

> "The output of the SPA appears, at first glance, plausible as a proxy for either the population of the Latin-speaking regions of the Roman Empire, or perhaps the broader sociopolitical complexity, between about AD 1 – 400."

## Methods that worked

- **SPA with bootstrap confidence intervals.** Empire-wide, provincial, and urban-area SPAs. Uniform probability distribution over `[not_before, not_after]`; 5-year binning.
- **OLS / Negative Binomial / Bayesian regression of inscription count on Hanson population.** Multiple framings converge on ~10 % variance explained on log scale.
- **Letter-count analysis as an alternative to inscription count.** Negative Binomial on letter counts: Pseudo-R² ≈ 0.84 (Shawn's own note: "This result looks too good to be true").

## Empirical anchors — 2024 findings

Quantitative results preserved from the archived notebook (Ross, unpublished):

- **OLS log-log R² = 0.101** (population → inscriptions)
- **OLS log-log coefficient (elasticity / scaling exponent β) = 0.473**, 95 % CI [0.376, 0.569]
- **Negative Binomial (log link) bootstrap-mean β = 0.683**, 95 % CI [0.532, 0.849] (the NBR log-link coefficient IS the power-law scaling exponent under μ = exp(α)·N^β; not a separate quantity)
- **Negative Binomial pseudo-R² = 0.421** (not directly comparable to OLS R²; pseudo-R²s for overdispersed count models can be misleading)
- **Bayesian linear log-log R² = 0.087**
- **Spearman ρ ≈ 0.30–0.31**
- Mean ΔT (date-range standard deviation) = 29.24 years (vs ~120 years in radiocarbon data)

**Both β estimates (OLS 0.473 and NBR 0.683) are of the same underlying power-law scaling exponent Y ∝ N^β under different distributional assumptions** — OLS assumes multiplicative Gaussian error and drops zero-count cities; NBR models count overdispersion directly and handles zeros natively. Both are unambiguously **sublinear**. The 2024 work therefore **independently replicates** the sublinear scaling pattern verified in Hanson (2021, Table 7.3; β = 0.672 mean [0.588, 0.756] / 0.654 median [0.514, 0.774], OLS log-log on 8 bins, n = 554, Rome excluded) and Carleton et al. (2025) β ≈ 0.3–0.5 for elite-honorific subsets — methodological triangulation across different data slices, regression families, and eras. The sublinear conclusion is robust to method choice. Note: Hanson 2021 excludes Rome as an extreme outlier, matching the 2024 notebook's practice of re-running "without Rome" — independent convergence on the same methodological choice.

**Headline for 2026 calibration.** Population explains ~10 % of inscription-count variance on log scale in the uncorrected data; the scaling exponent is β ∈ [0.47, 0.68] depending on estimator. The 2026 mixture-corrected H3 needs to demonstrate material improvement on the R² baseline, and (per Decision 7) should use Bayesian negative-binomial with log link + provincial random effects (following Carleton et al. 2025 framework) as the current best-practice approach for the scaling regression — with OLS log-log reported alongside as direct comparator to Hanson et al. (2017).

## Methods that failed — do NOT preregister without diagnosis

| Method | Why it failed (Shawn's words) |
|---|---|
| Michczynska & Pazdur (2004) sample-size model | "The curve should have dropped quickly… but it does not. I am not sure if this difference is because of: (a) The relatively large mean error versus the date range… (b) The fact that the error distribution is uniform rather than gaussian…" |
| Williams (2012) MSE for sample-size validation | "None of my attempts to calculate MSE according to Williams 2012 worked." Parameterisation unclear; results inconsistent with literature. |
| Statistical-fluctuation (Sf) calculation | "It's not clear from M&P what parameters of the SPD they are calculating on, or if they are using the 'SD/mean' definition of Sf." |
| Kolmogorov-Smirnov test on subsamples | Marked "This section needs to be redone. Add bootstrapping to get 95% confidence intervals." Incomplete. |

**2026 status.** Decision 2 pivots all of these to permutation-envelope power analysis (rcarbon-style, Python-native via `tempun` + `scipy.stats.permutation_test`). Dead ends are superseded, not resurrected. Future preregistrations should cite this table as the rationale for not revisiting.

## Concepts present in 2024 — carried forward to 2026

- SPA as an inscription-production proxy (core method, preserved)
- Population as the primary anchor via Hanson (preserved and formalised in H3)
- Multi-level analysis (empire / province / urban area)
- Bootstrap confidence intervals on SPA curves
- MacMullen (1982) / Meyer (1990) rise-and-fall of the epigraphic habit (referenced)
- Intuition of "disaggregate complexity" (mentioned; operationalised as multi-factor frame in 2026)
- Hanson (2021) replication (now H3)
- Rome as special-case exclusion (retained as standard stratification)
- Date-range threshold exploration 25/50/100/200/300 years (retained as H2 robustness)
- Urban-area threshold exploration 100/250/500/750 inscriptions (formalised in H1 via simulation)
- Letter-count as alternative to inscription count (retained as H2 cross-check)
- **Ceramic inscriptions as economic window** — 2024 to-do ("what can we learn from the difference in production costs?"); silently dropped until 2026-04-23; resurrected as FS-G (`planning/research-intent.md`).
- **Residual analysis Hanson-style** — 2024 to-do; resurrected 2026-04-23 as H3c (urban-area residuals mapped as outliers interpretable against the other complexity dimensions).

## Concepts absent in 2024, new in 2026

- Editorial-convention artefact awareness (century-midpoint spikes at AD 50 / 150 / 250 / 350; observed/expected 22.8× / 41.5× / 18.8× / 39.7×; Westfall-Young adjusted *p* ≈ 0)
- Deconvolution-mixture model (`observed = α·convention_SPA + (1−α)·genuine_SPA`) — the 2026 headline methodological contribution
- Permutation-envelope significance tests (rcarbon / Crema & Bevan 2021 best practice)
- Explicit multi-factor complexity decomposition with identifiability scope
- Epigraphic habit formalised as "necessary-but-not-sufficient" cultural translator
- Mixture α interpretable as translator intensity (FS-D)
- Aeneas-partition follow-up (FS-E)
- Baorista Bayesian aoristic comparison (Crema 2025)
- Scaling-law confound flag (open question; prior-art-scout commissioned 2026-04-23)
- Cultural-translator confound flag (open question; prior-art-scout commissioned 2026-04-23)
- Variance-explained as primary quantitative claim (vs 2024 exploratory "weak correlation")
- Production-cost differential via ceramic / stone (resurrected 2026-04-23 from 2024 to-do)

## Deprioritised in 2026

- Province / city descriptive profiles (2024 to-do) — likely appendix material, not a main-paper claim.
- Maps of temporal peaks by geography (2024 to-do) — partially subsumed by FS-E.
- Empire-wide statistics without Rome — retained as standard stratification, not headline.

## Where to find the 2024 work

`archive/` — Jupyter notebooks (2023-09-08 and 2026-04-22 variants). Both preserved. **Treat as historical record; do not resurrect abandoned methods without consulting this summary.**

## Provenance

Distilled 2026-04-23 from an Explore-agent audit of `archive/` commissioned by Shawn for externalisation on the ~2-year timescale. The agent's full report is in-session but not committed — this summary is the durable record. See `planning/research-intent.md` for the 2026 paper framing that builds on these findings.
