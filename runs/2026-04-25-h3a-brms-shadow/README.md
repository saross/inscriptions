# H3a brms shadow — run directory

**Script:** `scripts/h3a_brms_shadow.R`
**Date committed:** 2026-04-25
**Status at commit:** built, not yet executed (input data not yet produced by
the H2 mixture-correction pipeline).
**Audit verdict:** _pending_ — to be filled in by the `/audit` step after
build, and again after first successful execution.

## Purpose

R/brms cross-language validation shadow of the preregistered H3a Bayesian
negative-binomial regression (NBR), whose primary implementation is in
`pymc` (Python). Two motivations:

1. **Posterior-level agreement check.** Re-fitting the same model in an
   independent probabilistic-programming stack catches implementation bugs
   that neither implementation alone would reveal.
2. **R-native legibility** for Adela Sobotková (Aarhus Social Data Analysis
   of the Mediterranean, SDAM) and other R-fluent co-authors who read
   `brms` formula syntax more fluently than `pymc` model definitions.

See `planning/preregistration-draft.md` §3 (H3a model) and §9 (software
stack). See also `runs/2026-04-25-h3a-brms-shadow/plan.md` for design
rationale.

## Environment

| Requirement | Version | Notes |
|---|---|---|
| R | ≥ 4.3 | `Rscript` on `PATH`. |
| `brms` | ≥ 2.20 | Uses non-deprecated `prior()` syntax. |
| Stan backend | `cmdstanr` (preferred) or `rstan` | cmdstanr tracks Stan releases; rstan lags. |
| `arrow` | ≥ 14.0 | Parquet input and posterior-draws output. |
| `posterior` | ≥ 1.5 | `as_draws_df()`, `summarise_draws()`. |
| `bayesplot` | ≥ 1.10 | `pp_check()`, `mcmc_trace()`. |
| `ggplot2` | ≥ 3.4 | Plot saving. |
| `loo` | ≥ 2.6 | `elpd_loo` in diagnostics. |

### Install (one-off, in R)

```r
install.packages(c("brms", "posterior", "arrow", "bayesplot", "ggplot2", "loo"))
# Recommended Stan backend:
install.packages("cmdstanr",
                 repos = c("https://mc-stan.org/r-packages/", getOption("repos")))
cmdstanr::install_cmdstan()   # one-off, ~10 min; compiles Stan toolchain
```

If `cmdstanr` is unavailable, the script falls back to `rstan` with a
loud warning; install with `install.packages("rstan")`.

## Input-data contract

A single parquet file, default path `data/processed/city_level_for_h3a.parquet`
(override via first positional CLI argument). **This file is produced
downstream by the H2 mixture-correction pipeline, which is not yet built
at the time of this commit.** The script aborts with a clear diagnostic
if the file is absent.

Strict schema (enforced at load time, no silent row-dropping):

| Column | Type | Constraint |
|---|---|---|
| `city_id` | character | unique, non-NA. |
| `province` | character | non-NA; ~50 levels expected. |
| `log_pop` | double | finite (no `NA`, no `-Inf`); natural-log of population. |
| `count` | integer | ≥ 0; H2-corrected inscription count. |

Expected row count: ~816 cities (Hanson 2016 overlap with LIRE v3.0, Rome
excluded).

## Running

From the repository root:

```bash
# Default input path
Rscript scripts/h3a_brms_shadow.R

# Custom input path
Rscript scripts/h3a_brms_shadow.R path/to/alternative.parquet
```

**Expected runtime:** ~2 minutes wall-time on a modern laptop (4 chains ×
2000 iterations, `cores = 4`). First run adds ~45 s for Stan model
compilation; subsequent runs reuse the cached compiled object.

**RAM:** ~1 GB peak.

**Disk:** `posterior_draws.parquet` ~1–3 MB; whole `outputs/` directory
~5 MB.

## Output files (written to `outputs/`)

| File | Description |
|---|---|
| `posterior_draws.parquet` | Full posterior draws (4,000 post-warmup × all parameters), parquet for language-neutral downstream comparison against the pymc primary. |
| `summary.csv` | Per-parameter mean, SD, 2.5 / 50 / 97.5 % quantiles, `Rhat`, `ESS_bulk`, `ESS_tail`. |
| `bayes_r2.csv` | Bayesian R² (Gelman, Goodrich, Gabry & Vehtari 2019) with 95 % credible interval. |
| `ppc_statistics.csv` | PPC test statistics: proportion of zeros, mean, SD, 95th percentile, mean/variance ratio — observed vs posterior-predictive. |
| `ppc_density_overlay.png` | Empire-wide posterior-predictive density overlay. |
| `ppc_density_overlay_by_province.png` | Province-grouped PPC overlay — catches province-level mis-specification that empire-wide overlay hides. |
| `residuals.png` | Pearson residuals vs fitted. |
| `trace.png` | Trace plots for the four key parameters (intercept, `log_pop` slope, province SD, shape). |
| `diagnostics.txt` | Max `Rhat`, min ESS, divergences, tree-depth saturations, `elpd_loo`, full `sessionInfo()`. |

## Priors

Priors mirror the `pymc` primary exactly on scale and family (see
`plan.md` §5 for the side-by-side table). The one subtle translation
point — the dispersion prior — is documented verbatim in the script
header; see "Prior-correspondence note" there.

### Why a Stan snippet appears in the script

`brms` parameterises `negbinomial()` with a `shape` parameter that *is*
the dispersion α (Var = μ + μ²/α), whereas the preregistered `pymc`
primary places `HalfNormal(1)` on `inv_alpha = 1/α`. A naïve
`prior(normal(0, 1), class = "shape")` would regularise in the opposite
direction. To match exactly, the script uses `stanvar()` to inject a
single line of Stan into the model block:

```stan
target += normal_lpdf(1.0 / shape | 0, 1) - 2 * log(shape);
```

The `-2 * log(shape)` term is the Jacobian for the
`shape → 1/shape` reparameterisation (since |d(1/x)/dx| = 1/x², its log
is `−2 log x`). With this in place, posterior agreement between the
`pymc` primary and the `brms` shadow is expected on all quantities,
including the raw dispersion parameter.

## Audit verdict

_To be filled in by `/audit`._

- **Build-time audit** (pre-execution, verifies script against plan):
  pending.
- **Run-time audit** (post-execution, verifies outputs and
  posterior-level agreement with pymc primary): pending H2 pipeline.
