# ------------------------------------------------------------------------------
# h3a_brms_shadow_mundlak.R — R/brms cross-language shadow for the H3a
# confirmatory WITHIN-BETWEEN (Mundlak) NBR.
#
# Why a new script (not scripts/h3a_brms_shadow.R)?
# -------------------------------------------------
# The committed scripts/h3a_brms_shadow.R (dated 2026-04-25) fits the POOLED
# model `count ~ log_pop + (1 | province)`. The confirmatory model (prereg §3,
# Decision 12) is the WITHIN-BETWEEN (Mundlak) decomposition:
#   count ~ log_pop_within + log_pop_prov_mean + (1 | province)
# which yields the separate beta_within and beta_between needed for the
# pymc<->brms agreement check (beta_within, beta_between, f_within). The pooled
# shadow cannot produce those, so this run-local script adapts the same shadow
# — identical priors, identical 1/shape HalfNormal(1) Jacobian correction — to
# the Mundlak spec, run against the canonical parquet. The audited committed
# script is left untouched.
#
# Prior correspondence to the pymc primary (prereg §3):
#   Intercept (alpha_0)      ~ Normal(0, 5)
#   b log_pop_within         ~ Normal(0, 1)    (pymc beta_within prior)
#   b log_pop_prov_mean      ~ Normal(0, 1)    (pymc beta_between prior)
#   sd(province)             ~ HalfNormal(1)   (pymc sigma_prov; brms folds N+)
#   1/shape                  ~ HalfNormal(1)   via stanvar + Jacobian (-2 log shape)
#
# Input contract
# --------------
# data/processed/city_level_for_h3a.parquet with (at least):
#   city (character, unique), province (character), log_pop_within (double),
#   log_pop_prov_mean (double), inscription_count (integer >= 0).
#
# Output
# ------
# runs/2026-06-04-h3a-confirmatory/outputs/brms-shadow/{summary.csv,
#   bayes_r2.csv, fwithin.csv, diagnostics.txt, posterior_draws.parquet}
#
# Author / Date: Claude Code (Opus 4.8, 1M context), 2026-06-04, blind-run brief.
# ------------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(brms)
  library(posterior)
  library(arrow)
})

args <- commandArgs(trailingOnly = TRUE)
INPUT_PATH <- if (length(args) >= 1) args[1] else "data/processed/city_level_for_h3a.parquet"
OUTPUT_DIR <- "runs/2026-06-04-h3a-confirmatory/outputs/brms-shadow"
SEED <- 20260604L
set.seed(SEED)
dir.create(OUTPUT_DIR, recursive = TRUE, showWarnings = FALSE)

BACKEND <- if (requireNamespace("cmdstanr", quietly = TRUE)) "cmdstanr" else "rstan"

# ---- DATA LOAD + SCHEMA -----------------------------------------------------
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

# ---- PRIORS (match pymc primary) --------------------------------------------
priors <- c(
  prior(normal(0, 5), class = "Intercept"),
  prior(normal(0, 1), class = "b", coef = "log_pop_within"),
  prior(normal(0, 1), class = "b", coef = "log_pop_prov_mean"),
  prior(normal(0, 1), class = "sd", group = "province")  # HalfNormal(1) via N+ fold
)
# HalfNormal(1) on 1/shape, matching pymc HalfNormal(1) on inv_alpha = 1/alpha.
inv_shape_prior <- stanvar(
  scode = "target += normal_lpdf(1.0 / shape | 0, 1) - 2 * log(shape);",
  block = "model"
)

# ---- FIT (match pymc resource level: 4 chains, warmup 6000, draws 3000) ------
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
# f_within = Var_c(beta_within * within_dev_c) / Var_c(log E[count_c])
# log E[count_c] = Intercept + r_province[c] + b_within*within + b_between*between
# Reconstruct the linear predictor per draw from brms draws.
post <- as.data.frame(draws_df)
b0  <- post[["b_Intercept"]]
bw  <- post[["b_log_pop_within"]]
bb  <- post[["b_log_pop_prov_mean"]]
within  <- dat$log_pop_within
between <- dat$log_pop_prov_mean
provs <- sort(unique(dat$province))
# province random-intercept columns: r_province[<level>,Intercept]
re_cols <- sprintf("r_province[%s,Intercept]", provs)
re_cols <- gsub(" ", ".", re_cols)  # brms sanitises spaces in level names
have <- re_cols %in% names(post)
if (!all(have)) {
  # fall back to whatever r_province columns exist, matched by order of provs
  rc <- grep("^r_province\\[.*,Intercept\\]$", names(post), value = TRUE)
  re_cols <- rc
}
prov_index <- match(dat$province, provs)
S <- nrow(post); C <- nrow(dat)
fwithin <- numeric(S)
re_mat <- as.matrix(post[, re_cols, drop = FALSE])   # S x P
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
