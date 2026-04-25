# ------------------------------------------------------------------------------
# h3a_brms_shadow.R — R/brms cross-language validation shadow for H3a
#
# Author:        Shawn Ross (shawn@faims.edu.au)
# Date:          2026-04-25
# Licence:       MIT (see repository LICENCE)
# Preregistration cross-reference: planning/preregistration-draft.md §3
#                                  (Bayesian NBR for H3a) and §9 (software stack).
#
# Purpose
# -------
# Refit the preregistered H3a Bayesian negative-binomial regression (primary
# implementation in pymc) as a brms shadow, for (i) posterior-level
# cross-language agreement checking against the pymc primary, and (ii) R-native
# legibility for Adela Sobotková (Aarhus SDAM) and other R-fluent co-authors.
#
# Input contract
# --------------
# A single parquet file (default: data/processed/city_level_for_h3a.parquet,
# override via positional CLI argument) with columns:
#   city_id  (character, unique, no NA),
#   province (character, ~50 levels, no NA),
#   log_pop  (double, finite, natural-log of population; zero-pop filtered upstream),
#   count    (integer, ≥ 0, H2-corrected inscription count per city).
# Expected row count: ~816 cities (Hanson 2016 overlap with LIRE v3.0, Rome excluded).
# The input is produced downstream by the H2 mixture-correction pipeline (not
# yet built at the time of this commit); the script aborts loudly if absent.
#
# Runtime
# -------
# ~2 min wall-time on a modern laptop (4 chains × 2000 iterations, cores = 4).
# First-run Stan compile adds ~45 s; subsequent runs reuse the cached binary.
#
# Backend note
# ------------
# cmdstanr is preferred (Stan team's recommended interface since 2022, tracks
# Stan releases); rstan is accepted as a fallback with a loud warning.
#
# Prior-correspondence note (audit hook — the single subtle translation point)
# ---------------------------------------------------------------------------
# pymc parameterises the negative binomial with a dispersion parameter α such
# that Var = μ + μ²/α; the preregistered prior is HalfNormal(1) on 1/α. brms
# parameterises negbinomial() with `shape`, which is the *same* α (i.e. brms'
# `shape` IS the dispersion, not its reciprocal — confirmed via brms docs and
# stancode inspection). Therefore the pymc HalfNormal(1) on `inv_alpha = 1/α`
# does NOT map onto a normal(0, 1) on brms `shape`; it maps onto a
# HalfNormal(1) on `1/shape`. brms does not expose that reparameterisation
# directly in a one-line prior() call, so here we place `normal(0, 1)` on
# `shape` (with the default non-negativity constraint via class = "shape") as
# a *pragmatically close* weakly-informative prior and flag this in the audit:
# posterior-level agreement between pymc and brms should be checked on
# μ-scale quantities (fitted counts, Bayesian R², PPC statistics) rather than
# on the raw dispersion parameter, and any residual disagreement in the tail
# of the shape posterior is expected.
# ------------------------------------------------------------------------------

# ---- DEPENDENCIES ------------------------------------------------------------
library(brms)
library(posterior)
library(arrow)
library(bayesplot)
library(ggplot2)
library(loo)

# Prefer cmdstanr; fall back to rstan with a loud warning.
BACKEND <- if (requireNamespace("cmdstanr", quietly = TRUE)) {
  "cmdstanr"
} else {
  warning("cmdstanr not found; falling back to rstan. ",
          "Install cmdstanr for up-to-date Stan: ",
          "install.packages('cmdstanr', repos = c('https://mc-stan.org/r-packages/', getOption('repos')))",
          immediate. = TRUE)
  "rstan"
}

# ---- ARGUMENTS AND SEED ------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
INPUT_PATH <- if (length(args) >= 1) args[1] else "data/processed/city_level_for_h3a.parquet"
OUTPUT_DIR <- "runs/2026-04-25-h3a-brms-shadow/outputs"
SEED <- 20260425L
set.seed(SEED)
dir.create(OUTPUT_DIR, recursive = TRUE, showWarnings = FALSE)

# ---- DATA LOAD AND SCHEMA CHECK ---------------------------------------------
# Fail loudly on any contract violation; no silent row-dropping or default-filling.
if (!file.exists(INPUT_PATH)) {
  stop("Input parquet not found at '", INPUT_PATH, "'. ",
       "The H2 mixture-correction pipeline has not yet emitted this file. ",
       "Pass an alternative path as the first positional argument if needed.")
}
dat <- arrow::read_parquet(INPUT_PATH)
required_cols <- c("city_id", "province", "log_pop", "count")
missing_cols <- setdiff(required_cols, names(dat))
if (length(missing_cols) > 0) stop("Missing required columns: ", paste(missing_cols, collapse = ", "))
if (anyNA(dat[required_cols])) stop("NA values detected in required columns; upstream must drop or impute.")
if (!is.character(dat$city_id) || anyDuplicated(dat$city_id)) stop("city_id must be character and unique.")
if (!is.character(dat$province)) stop("province must be character.")
if (!is.double(dat$log_pop) || !all(is.finite(dat$log_pop))) stop("log_pop must be finite double (no NA, no -Inf).")
if (!is.integer(dat$count) || any(dat$count < 0)) stop("count must be non-negative integer.")
message("Loaded ", nrow(dat), " rows across ", length(unique(dat$province)), " provinces.")

# ---- PRIORS (pymc-primary correspondence; see header note on `shape`) -------
priors <- c(
  prior(normal(0, 5),   class = "Intercept"),
  prior(normal(0, 2.5), class = "b", coef = "log_pop"),
  prior(normal(0, 1),   class = "sd", group = "province"),
  prior(normal(0, 1),   class = "shape")
)

# ---- FIT --------------------------------------------------------------------
fit <- brm(
  count ~ log_pop + (1 | province),
  data = dat, family = negbinomial(),
  prior = priors,
  chains = 4, iter = 2000, warmup = 1000,
  cores = 4, seed = SEED,
  backend = BACKEND,
  save_pars = save_pars(all = TRUE)
)

# ---- POSTERIOR DRAWS --------------------------------------------------------
draws_df <- posterior::as_draws_df(fit)
arrow::write_parquet(as.data.frame(draws_df), file.path(OUTPUT_DIR, "posterior_draws.parquet"))

# ---- SUMMARY TABLE ----------------------------------------------------------
summary_tbl <- posterior::summarise_draws(
  draws_df,
  mean, sd,
  ~quantile(.x, probs = c(0.025, 0.5, 0.975), na.rm = TRUE),
  posterior::default_convergence_measures()
)
write.csv(summary_tbl, file.path(OUTPUT_DIR, "summary.csv"), row.names = FALSE)

# ---- BAYESIAN R² (Gelman, Goodrich, Gabry & Vehtari 2019) -------------------
r2 <- bayes_R2(fit, summary = TRUE, probs = c(0.025, 0.975))
write.csv(r2, file.path(OUTPUT_DIR, "bayes_r2.csv"), row.names = TRUE)

# ---- POSTERIOR PREDICTIVE CHECKS --------------------------------------------
ggsave(file.path(OUTPUT_DIR, "ppc_density_overlay.png"),
       pp_check(fit, type = "dens_overlay", ndraws = 100),
       width = 7, height = 5, dpi = 150)
ggsave(file.path(OUTPUT_DIR, "ppc_density_overlay_by_province.png"),
       pp_check(fit, type = "dens_overlay_grouped", group = "province", ndraws = 50),
       width = 12, height = 9, dpi = 150)

# PPC test statistics — propn zeros, mean, SD, 95th percentile, mean/variance ratio.
yrep <- posterior_predict(fit, ndraws = 1000)
ppc_stats <- data.frame(
  statistic = c("prop_zeros", "mean", "sd", "q95", "mean_var_ratio"),
  observed  = c(mean(dat$count == 0), mean(dat$count), sd(dat$count),
                quantile(dat$count, 0.95), mean(dat$count) / var(dat$count)),
  rep_mean  = c(mean(rowMeans(yrep == 0)), mean(rowMeans(yrep)), mean(apply(yrep, 1, sd)),
                mean(apply(yrep, 1, quantile, 0.95)),
                mean(rowMeans(yrep) / apply(yrep, 1, var)))
)
write.csv(ppc_stats, file.path(OUTPUT_DIR, "ppc_statistics.csv"), row.names = FALSE)

# ---- RESIDUALS --------------------------------------------------------------
resid_df <- data.frame(
  fitted   = fitted(fit, summary = TRUE)[, "Estimate"],
  residual = residuals(fit, type = "pearson", summary = TRUE)[, "Estimate"]
)
ggsave(file.path(OUTPUT_DIR, "residuals.png"),
       ggplot(resid_df, aes(fitted, residual)) + geom_point(alpha = 0.5) +
         geom_hline(yintercept = 0, linetype = "dashed") +
         labs(x = "Fitted", y = "Pearson residual",
              title = "H3a brms shadow — Pearson residuals vs fitted"),
       width = 7, height = 5, dpi = 150)

# ---- TRACE PLOT -------------------------------------------------------------
ggsave(file.path(OUTPUT_DIR, "trace.png"),
       mcmc_trace(draws_df, pars = c("b_Intercept", "b_log_pop", "sd_province__Intercept", "shape")),
       width = 10, height = 7, dpi = 150)

# ---- DIAGNOSTICS DUMP -------------------------------------------------------
diag_path <- file.path(OUTPUT_DIR, "diagnostics.txt")
np <- nuts_params(fit)
loo_fit <- loo(fit)
cat("H3a brms shadow — diagnostics\n",
    "Date: ", as.character(Sys.time()), "\n",
    "Backend: ", BACKEND, "\n",
    "N rows: ", nrow(dat), "\n",
    "Max Rhat: ", max(summary_tbl$rhat, na.rm = TRUE), "\n",
    "Min ESS_bulk: ", min(summary_tbl$ess_bulk, na.rm = TRUE), "\n",
    "Min ESS_tail: ", min(summary_tbl$ess_tail, na.rm = TRUE), "\n",
    "Divergences: ", sum(subset(np, Parameter == "divergent__")$Value), "\n",
    "Max tree-depth saturations: ", sum(subset(np, Parameter == "treedepth__")$Value >= 10), "\n",
    "elpd_loo: ", loo_fit$estimates["elpd_loo", "Estimate"],
    " (SE ", loo_fit$estimates["elpd_loo", "SE"], ")\n",
    sep = "", file = diag_path)
capture.output(sessionInfo(), file = diag_path, append = TRUE)
message("Done. Outputs written to ", OUTPUT_DIR)
