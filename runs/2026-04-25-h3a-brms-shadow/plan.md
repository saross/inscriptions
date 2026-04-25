---
priority: 1
scope: in-stream
title: "h3a_brms_shadow.R — implementation plan"
audience: "CC (self-approve), build agent (implementation)"
status: draft plan; CC self-approval pending
date: 2026-04-25
---

# Plan — `scripts/h3a_brms_shadow.R`

**Run directory:** `runs/2026-04-25-h3a-brms-shadow/`
**Scope:** ~50-LOC R/brms cross-language validation shadow of the pymc-primary H3a Bayesian negative-binomial regression, committed for (i) posterior-level agreement check with the pymc primary and (ii) R-native legibility for Adela Sobotková (Aarhus SDAM) and other R-fluent co-authors.
**Track 2 delivers:** plan + build + audit. **Does NOT execute** (input data not yet produced).

---

## 1. Context and interface contract

The H3a primary implementation is `pymc` (Python) per preregistration §3 and Decision resolution 2026-04-24 (continuity.md session log). This R stub refits the *same* model from the same joined city-level dataset that the pymc pipeline emits and writes language-neutral outputs (parquet / CSV / PNG).

**Input data contract.** The stub reads a single parquet file produced downstream by the H2 mixture correction pipeline (not yet built):

- **Default path:** `data/processed/city_level_for_h3a.parquet` (canonical project-level path; can be overridden by the first positional CLI argument). **NOTE: this path was revised from the plan-agent's original (`runs/2026-04-25-h1-simulation/outputs/city_level_for_brms.parquet`), which incorrectly conflated H1 simulation outputs with H2-derived real city data. H2 is not yet built; the stub designates a canonical future path.**
- **Required columns (strict schema check at load time):**
  - `city_id` — character, unique per row, no missing.
  - `province` — character, non-missing, expected ~50 levels.
  - `log_pop` — double, finite (no `NA`, no `-Inf`), `log(population)` on natural-log scale. Zero-population cities filtered upstream.
  - `count` — integer, ≥ 0, inscription count per city after H2 mixture correction.
- **Expected row count:** ~816 cities (Hanson 2016 overlap with LIRE v3.0, Rome excluded).
- **Failure behaviour:** if the file is absent, the script prints a clear diagnostic (path, hint that H2 hasn't emitted the data) and exits with status 1. No silent fallback.

Documented in `runs/2026-04-25-h3a-brms-shadow/README.md` for Adela to run standalone once the input appears.

## 2. Critical-friend four-check findings

**(1) More appropriate shadow?** `brms` is the right choice over raw Stan or `rstan` direct — Adela reads `brms`'s formula syntax natively. `rstanarm` considered but does not expose negative-binomial in the preregistered parameterisation cleanly. Model spec (random intercepts only, no varying slopes) matches preregistered H3a exactly — no scope creep.

**(2) More powerful / robust alternative?** Three diagnostic extensions added (not preregistered; purely diagnostic):
- `pp_check(..., type = "dens_overlay_grouped", group = "province")` catches province-level mis-specification that empire-wide density overlay would hide.
- `loo::loo()` plus `elpd_loo` recorded in `diagnostics.txt` for any future model-comparison question.
- Divergences, tree-depth saturations, E-BFMI per chain recorded explicitly, not buried in Stan warnings.

**(3) Current best-practice?** `cmdstanr` is Stan-team recommended since 2022 (rstan lags Stan releases). Stub uses `backend = "cmdstanr"` if detected, falls back to `"rstan"` with a loud warning otherwise. `brms` ≥ 2.20 syntax (no deprecated `prior_string`); Stan 2.32+ normalised warnings parsed via `posterior::summarise_draws()`.

**(4) Do assumptions hold?**
- Counts integer-valued: enforced at load time.
- `log_pop` finite: enforced at load time; no silent row-dropping.
- Province exchangeability: defensible across ~50 provinces; preregistered model treats province as random intercept. Province-level slope heterogeneity would be a new model + preregistration amendment.

## 3. File layout

```
scripts/h3a_brms_shadow.R                      # the stub (~50 LOC excl. header/comments)
runs/2026-04-25-h3a-brms-shadow/
  plan.md                                      # this document
  README.md                                    # how Adela runs it; environment; outputs
  outputs/                                     # populated at future execution time
    posterior_draws.parquet
    summary.csv
    bayes_r2.csv
    ppc_statistics.csv
    trace.png
    ppc_density_overlay.png
    ppc_density_overlay_by_province.png        # diagnostic add-on
    residuals.png
    diagnostics.txt                            # Rhat, ESS, divergences, elpd_loo
```

## 4. Script outline (section-by-section, linear, ~50 LOC executable)

1. **Header block** (comments). Title, author, date, licence, preregistration cross-reference (§3), runtime expectation, input contract.
2. **Dependency load.** `library(brms); library(posterior); library(arrow); library(bayesplot); library(ggplot2); library(loo)`. Conditional `cmdstanr` detection → `BACKEND` variable.
3. **Arguments and seed.** Positional `argv[1]` = input parquet path (default set); `SEED <- 20260425L`; `set.seed(SEED)`.
4. **Data load + schema check.** `arrow::read_parquet()`; assertions on columns, types, finiteness, integer-count.
5. **Priors.** Explicit `c(prior(...), ...)` vector (see §5).
6. **Fit.** Single `brm()` call: formula, family, data, priors, `chains = 4`, `iter = 2000`, `warmup = 1000`, `cores = 4`, `seed = SEED`, `backend = BACKEND`, `save_pars = save_pars(all = TRUE)`.
7. **Posterior draws → parquet.** `as_draws_df(fit) |> arrow::write_parquet()`.
8. **Summary table.** `posterior::summarise_draws()` with `mean, sd, ~quantile(.x, c(0.025, 0.5, 0.975)), rhat, ess_bulk, ess_tail` → CSV.
9. **Bayesian R².** `bayes_R2(fit, summary = TRUE, probs = c(0.025, 0.975))` → CSV.
10. **PPCs.** `pp_check(fit, type = "dens_overlay", ndraws = 100)` → PNG; grouped-by-province variant → PNG; test statistics (proportion of zeros, mean, SD, 95th percentile, mean-variance ratio) via `posterior_predict()` → CSV.
11. **Residuals.** `residuals(fit, type = "pearson", summary = TRUE)` vs fitted → PNG.
12. **Diagnostics dump.** Rhat, ESS, divergences (`nuts_params()`), tree-depth saturations, `loo(fit)` elpd → text file.
13. **`sessionInfo()`** appended.

Total: ~50 lines executable R, heavily commented for Adela's first read-through. Function-free; linear top-to-bottom.

## 5. Prior specification (pymc ↔ brms side-by-side)

| Parameter | pymc primary | brms stub |
|---|---|---|
| α₀ (intercept, log-count) | `pm.Normal("alpha_0", 0, 5)` | `prior(normal(0, 5), class = "Intercept")` |
| β (coef on `log_pop`) | `pm.Normal("beta", 0, 2.5)` | `prior(normal(0, 2.5), class = "b", coef = "log_pop")` |
| σ_province | `pm.HalfNormal("sigma_prov", 1)` | `prior(normal(0, 1), class = "sd", group = "province")` |
| 1/α (dispersion reciprocal) | `pm.HalfNormal("inv_alpha", 1)` | `prior(normal(0, 1), class = "shape")` **— verify at build time** |

**Audit hook (critical):** the `shape` prior correspondence is the single subtle point in the translation. `brms` parameterises negbinomial with `shape = 1/dispersion`; `HalfNormal(1)` on `1/α` in pymc matches `normal(0, 1)` on `shape` with lower bound 0 enforced by brms' `class = "shape"` default. If brms parameterises differently in a way that shifts the prior implicitly, stub header carries an explicit note and prior is revised before execution.

## 6. Reproducibility plan

- `SEED <- 20260425L`. brms threads via `seed = SEED`; each chain receives `SEED + chain_index`. `set.seed(SEED)` covers R-level randomness.
- `chains = 4`, `iter = 2000`, `warmup = 1000` → 4,000 post-warmup draws.
- `cores = 4` to parallelise chains.
- `backend = "cmdstanr"` preferred; `"rstan"` fallback explicit and warned.
- `sessionInfo()` captured; versions pinned in README.

## 7. Runtime and resource estimate

- **Fit time:** 816 cities, 5 scalar parameters + ~50 random intercepts, NB likelihood, NUTS. ~30–90 s/chain on modern laptop; ≤ 2 min wall-time with 4 parallel cores.
- **RAM:** ~1 GB peak for 4 chains with `save_pars(all = TRUE)`.
- **Disk:** `posterior_draws.parquet` ~1–3 MB; total output directory ~5 MB.
- **Compilation:** first run ~45 s (Stan model compile); subsequent runs reuse cached compiled object.

## 8. Audit hooks

1. **Prior syntax** — confirms four `prior()` calls match pymc priors exactly on scale, family, class. Special scrutiny on `shape` parameterisation.
2. **`bayes_R2` computation** — `summary = TRUE` with `probs = c(0.025, 0.975)` matches Gelman, Goodrich, Gabry & Vehtari (2019).
3. **PPC code correctness** — `pp_check` draws count, grouped-overlay spec, test-statistic calculation.
4. **No silent failures** — schema check aborts clearly on missing file/column/type/non-finite/non-integer; no default filling.
5. **Reproducibility** — seed threading, `sessionInfo()`, deterministic output paths.
6. **Style** — tidyverse style guide (snake_case, `<-`, `|>`, Oxford comma, UK/Australian English in comments).
7. **Commit discipline** — plan → build → audit, separate commits.

## 9. Status report (Track 2 morning artefact)

Track 2 does NOT execute the model. Morning deliverables:

- `runs/2026-04-25-h3a-brms-shadow/plan.md` — committed.
- `scripts/h3a_brms_shadow.R` — committed.
- `runs/2026-04-25-h3a-brms-shadow/README.md` — Adela-facing.
- `/audit` verdict recorded — "READY FOR EXECUTION" (to run once H2 pipeline emits `data/processed/city_level_for_h3a.parquet`) or "BLOCKED" with issue.
- `runs/2026-04-25-h3a-brms-shadow/outputs/` empty with `.gitkeep`.

## 10. Constraints respected

- No API calls.
- Model NOT executed in Track 2.
- Commit discipline: plan → build → audit, each separate.
- Style: tidyverse / UK-Australian English / Oxford comma.
