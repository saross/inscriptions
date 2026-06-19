# ------------------------------------------------------------------------------
# h3a_brms_shadow.R — R/brms cross-language shadow for the H3a confirmatory
#                     WITHIN-BETWEEN (Mundlak) negative-binomial regression.
#
# Author:        Shawn Ross (shawn@faims.edu.au), with Claude Code (analyst/RSE)
# Date:          2026-06-05 (promoted to a first-class artefact from the
#                2026-06-04 H3a confirmatory blind run; supersedes the
#                2026-04-25 pooled shadow now in
#                archive/superseded-code/h3a_brms_shadow-pooled-pre-mundlak-2026-04-25.R)
# Licence:       MIT (see repository LICENCE)
# Preregistration cross-reference: planning/preregistration-draft.md §3
#                (Bayesian NBR for H3a) + §9 (software stack).
# Decision cross-reference: Decision 12 (within-between Mundlak rescope);
#                Decision 22 (H3a uses date-window-filtered counts, NOT mixture-
#                corrected); Decision 35 + addendum (model = build_model_f1_f3;
#                H3a consumes date-window counts); Decision 36 (Latin-speaking
#                provinces are the primary frame — run this shadow on whichever
#                city-frame parquet defines the frame being reported).
#
# SCOPE / PROVENANCE NOTE (added 2026-06-20, pre-write-up uplift)
# ---------------------------------------------------------------
# This committed script fits the WITHIN-BETWEEN (Mundlak) confirmatory model —
# NOT the pooled pre-Mundlak `count ~ log_pop` model. The pooled version was
# RETIRED on 2026-06-05 and lives at
#   archive/superseded-code/h3a_brms_shadow-pooled-pre-mundlak-2026-04-25.R
# (do not use it for the confirmatory cross-check).
#
# Relationship to the run-local Mundlak shadow:
#   runs/2026-06-04-h3a-confirmatory/code/h3a_brms_shadow_mundlak.R
# is the run-local twin that produced the brms↔pymc cross-language agreement
# recorded in the H3a confirmatory REPORT §6 ("No material disagreement";
# beta_within / f_within match within Monte-Carlo noise — D9 amendment-trigger
# NOT fired). The two scripts fit the SAME Mundlak formula
# (`count ~ log_pop_within + log_pop_prov_mean + (1 | province)`, identical
# priors and seed 20260604); this scripts/ copy is the project-level,
# co-author-facing entry point, the run-local copy is the in-dir provenance
# artefact. (NB: an earlier audit note claimed this committed script still fit
# the pooled model — that was stale; the 2026-06-05 promotion already corrected
# it. This note records the correction so the premise is not re-raised.)
#
# Purpose
# -------
# Refit the preregistered H3a model — whose PRIMARY implementation is in pymc
# (`runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py`) — as a brms shadow, to
#   (i)  cross-language-validate the pymc posterior (beta_within, beta_between,
#        f_within, Bayesian R^2) within Monte-Carlo noise, and
#   (ii) give R-native legibility to R-fluent co-authors (Adela Sobotková /
#        Aarhus SDAM and others) who read brms more fluently than pymc.
#
# It fits the WITHIN-BETWEEN (Mundlak) decomposition
#   count ~ log_pop_within + log_pop_prov_mean + (1 | province)
# so that beta_within (the clean within-province population effect) and
# beta_between are separately identified — the pooled `count ~ log_pop` shadow
# CANNOT produce these and is retired (see the archived file above).
#
# Prior correspondence to the pymc primary (prereg §3; weakly-informative):
#   Intercept (alpha_0)   ~ Normal(0, 5)
#   b log_pop_within      ~ Normal(0, 1)     (pymc beta_within)
#   b log_pop_prov_mean   ~ Normal(0, 1)     (pymc beta_between)
#   sd(province)          ~ HalfNormal(1)    (pymc sigma_prov; brms folds Normal+)
#   1/shape               ~ HalfNormal(1)    via a stanvar with the -2*log(shape)
#                                            Jacobian for the 1/shape -> shape
#                                            change of variables (matches pymc's
#                                            `1/dispersion ~ HalfNormal(1)`).
#
# Input contract
# --------------
# A single parquet (default `data/processed/city_level_for_h3a.parquet`, override
# via positional arg 1) produced by the H3a data-prep
# (`runs/2026-06-04-h3a-confirmatory/code/01-data-prep.py`), with at least:
#   city               (character, unique, no NA)
#   province           (character, no NA)
#   log_pop_within     (double; log_pop_c - province-mean log_pop)
#   log_pop_prov_mean  (double; province-mean log_pop)
#   inscription_count  (integer >= 0; date-window-filtered count — NOT mixture-
#                       corrected, per Decision 22 / 35)
# To shadow the Latin-frame primary (Decision 36) pass the Latin city frame, e.g.
#   data/processed/city_level_for_h3a_latin.parquet
#
# Usage
# -----
#   Rscript scripts/h3a_brms_shadow.R [INPUT_PARQUET] [OUTPUT_DIR]
# Defaults: INPUT_PARQUET=data/processed/city_level_for_h3a.parquet,
#           OUTPUT_DIR=outputs/brms-shadow (created if absent).
#
# Output
# ------
# <OUTPUT_DIR>/{summary.csv, bayes_r2.csv, fwithin.csv, diagnostics.txt,
#   posterior_draws.parquet}. Compare `fwithin.csv` + the b_* rows of
# `summary.csv` against the pymc primary's `h3a-results.json` (agreement within
# Monte-Carlo noise is the §6 cross-language check; material divergence on the
# confirmatory verdict is investigated and, if it changes the result, an OSF
# amendment is filed before final results — prereg §3).
#
# Runtime
# -------
# ~1,000 cities, 4 chains, warmup 6,000 + 3,000 draws, adapt_delta 0.97: a few
# minutes on a multi-core host with cmdstanr. Needs R + brms + posterior + arrow,
# and a Stan backend (cmdstanr preferred, rstan fallback). Confirmed available on
# sapphire (R 4.4.3 / brms / cmdstanr).
# ------------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(brms)
  library(posterior)
  library(arrow)
})

# ---- ARGUMENTS + PATHS ------------------------------------------------------
args <- commandArgs(trailingOnly = TRUE)
INPUT_PATH <- if (length(args) >= 1) args[1] else "data/processed/city_level_for_h3a.parquet"
OUTPUT_DIR <- if (length(args) >= 2) args[2] else "outputs/brms-shadow"
SEED <- 20260604L  # matches the pymc primary's fit seed for like-for-like comparison
set.seed(SEED)
dir.create(OUTPUT_DIR, recursive = TRUE, showWarnings = FALSE)

# cmdstanr is preferred (faster, current Stan); fall back to rstan if absent.
BACKEND <- if (requireNamespace("cmdstanr", quietly = TRUE)) "cmdstanr" else "rstan"

# ---- DATA LOAD + SCHEMA GUARD -----------------------------------------------
# Abort loudly on any contract violation — a silent column rename or NA would
# invalidate the cross-language check.
if (!file.exists(INPUT_PATH)) stop("Input parquet not found at '", INPUT_PATH, "'.")
dat <- arrow::read_parquet(INPUT_PATH)
needed <- c("city", "province", "log_pop_within", "log_pop_prov_mean", "inscription_count")
missing_cols <- setdiff(needed, names(dat))
if (length(missing_cols) > 0) stop("Missing columns: ", paste(missing_cols, collapse = ", "))
dat$city <- as.character(dat$city)
dat$province <- as.character(dat$province)
dat$count <- as.integer(dat$inscription_count)
if (anyNA(dat[c("log_pop_within", "log_pop_prov_mean", "count", "province")]))
  stop("NA in required columns.")
if (anyDuplicated(dat$city)) stop("city must be unique.")
if (any(dat$count < 0)) stop("count must be non-negative.")
message("Loaded ", nrow(dat), " cities across ", length(unique(dat$province)), " provinces.")

# ---- PRIORS (match the pymc primary; see header) ----------------------------
priors <- c(
  prior(normal(0, 5), class = "Intercept"),
  prior(normal(0, 1), class = "b", coef = "log_pop_within"),
  prior(normal(0, 1), class = "b", coef = "log_pop_prov_mean"),
  prior(normal(0, 1), class = "sd", group = "province")  # HalfNormal(1) via N+ fold
)
# HalfNormal(1) on 1/shape, matching pymc's HalfNormal(1) on inv_dispersion =
# 1/alpha. The -2*log(shape) term is the Jacobian of the 1/shape -> shape change
# of variables (d(1/shape)/d(shape) = -1/shape^2; log|.| = -2 log shape).
inv_shape_prior <- stanvar(
  scode = "target += normal_lpdf(1.0 / shape | 0, 1) - 2 * log(shape);",
  block = "model"
)

# ---- FIT (resource level matched to the pymc primary) -----------------------
fit <- brm(
  count ~ log_pop_within + log_pop_prov_mean + (1 | province),
  data = dat, family = negbinomial(),
  prior = priors, stanvars = inv_shape_prior,
  chains = 4, iter = 9000, warmup = 6000,
  cores = 4, seed = SEED, backend = BACKEND,
  control = list(adapt_delta = 0.97),
  save_pars = save_pars(all = TRUE)
)

draws_df <- posterior::as_draws_df(fit)
arrow::write_parquet(as.data.frame(draws_df), file.path(OUTPUT_DIR, "posterior_draws.parquet"))

summary_tbl <- posterior::summarise_draws(
  draws_df, mean, sd,
  ~quantile(.x, probs = c(0.025, 0.5, 0.975), na.rm = TRUE),
  posterior::default_convergence_measures()
)
write.csv(summary_tbl, file.path(OUTPUT_DIR, "summary.csv"), row.names = FALSE)

# ---- BAYES R^2 (response-scale; brms canonical) -----------------------------
r2 <- bayes_R2(fit, summary = TRUE, probs = c(0.025, 0.975))
write.csv(r2, file.path(OUTPUT_DIR, "bayes_r2.csv"), row.names = TRUE)

# ---- f_within per draw (mirror the pymc estimand) ---------------------------
# f_within = Var_c(beta_within * within_dev_c) / Var_c(log E[count_c]), where
#   log E[count_c] = Intercept + r_province[c] + b_within*within_c + b_between*between_c.
# Variances are population (divide by C, not C-1) to match the pymc estimand
# exactly (ddof=0); the (C-1)/C factors below convert R's sample var accordingly.
post <- as.data.frame(draws_df)
b0  <- post[["b_Intercept"]]
bw  <- post[["b_log_pop_within"]]
bb  <- post[["b_log_pop_prov_mean"]]
within  <- dat$log_pop_within
between <- dat$log_pop_prov_mean
provs <- sort(unique(dat$province))
# Match province random-intercept columns to provinces ROBUSTLY by parsing the
# level label out of each `r_province[<level>,Intercept]` column, so the mapping
# never depends on column ORDER. (A naive order-based fallback can mis-assign
# province intercepts and silently corrupt f_within; here we hard-stop instead.)
# brms names columns r_province[<level>,Intercept], sanitising spaces to dots.
re_all <- grep("^r_province\\[.*,Intercept\\]$", names(post), value = TRUE)
re_level <- sub("^r_province\\[(.*),Intercept\\]$", "\\1", re_all)
col_for_prov <- re_all[match(gsub(" ", ".", provs), re_level)]
if (anyNA(col_for_prov))
  stop("Unmatched province random-intercept column(s) for: ",
       paste(provs[is.na(col_for_prov)], collapse = ", "),
       " — brms level-name sanitisation differs from the space->dot assumption; ",
       "inspect names(post) and extend the sanitisation.")
prov_index <- match(dat$province, provs)
S <- nrow(post); C <- nrow(dat)
fwithin <- numeric(S)
re_mat <- as.matrix(post[, col_for_prov, drop = FALSE])  # S x P, columns in `provs` order
for (s in seq_len(S)) {
  re_c <- re_mat[s, prov_index]                       # length C
  log_mu <- b0[s] + re_c + bw[s] * within + bb[s] * between
  contrib <- bw[s] * within
  fwithin[s] <- var(contrib) * (C - 1) / C / (var(log_mu) * (C - 1) / C)
}
fw_q <- quantile(fwithin, c(0.025, 0.5, 0.975))
write.csv(
  data.frame(quantile = c("2.5%", "50%", "97.5%"), f_within = as.numeric(fw_q),
             p_gt_010 = mean(fwithin > 0.10)),
  file.path(OUTPUT_DIR, "fwithin.csv"), row.names = FALSE
)

# ---- DIAGNOSTICS ------------------------------------------------------------
np <- nuts_params(fit)
diag_path <- file.path(OUTPUT_DIR, "diagnostics.txt")
cat("H3a brms Mundlak shadow — diagnostics\n",
    "Date: ", as.character(Sys.time()), "\n",
    "Input: ", INPUT_PATH, "\n",
    "Backend: ", BACKEND, "\n",
    "N rows: ", nrow(dat), "\n",
    "Max Rhat: ", max(summary_tbl$rhat, na.rm = TRUE), "\n",
    "Min ESS_bulk: ", min(summary_tbl$ess_bulk, na.rm = TRUE), "\n",
    "Divergences: ", sum(subset(np, Parameter == "divergent__")$Value), "\n",
    "b_Intercept (median): ", median(b0), "\n",
    "b_log_pop_within (median): ", median(bw), "\n",
    "b_log_pop_prov_mean (median): ", median(bb), "\n",
    "f_within (median): ", as.numeric(fw_q[2]), "\n",
    "f_within 95% CI: [", as.numeric(fw_q[1]), ", ", as.numeric(fw_q[3]), "]\n",
    sep = "", file = diag_path)
message("Done. Outputs -> ", OUTPUT_DIR)
