# ------------------------------------------------------------------------------
# smoke_test.R — baorista tiered benchmark on synthetic aoristic data
#
# Author:        Shawn Ross (shawn@faims.edu.au) and Claude Code (Opus 4.7, 1M)
# Date:          2026-05-03
# Licence:       MIT
# Preregistration cross-reference:
#   - planning/baorista-install-plan.md §6 (Stage 4 validation runs)
#   - planning/decision-log.md Decision 3 (sensitivity criteria)
#
# Purpose
# -------
# Tiered benchmark of baorista::expfit() on synthetic aoristic data, to:
#   (i)  confirm the install works end-to-end at non-trivial scale; and
#   (ii) characterise wall-time growth before committing to FS-4 follow-up runs
#        at empire scale.
#
# Tiers (per plan §6.2, with the n=50,000 tier deferred to FS-4 timing study):
#   - n =   100, niter = 4000, nburnin = 2000, nchains = 4 → expect ~5 min
#   - n =   500, niter = 4000, nburnin = 2000, nchains = 4 → expect ~30 min
#   - n = 5,000, niter = 4000, nburnin = 2000, nchains = 4 → expect 1.5–3 h
#
# Output
# ------
# CSV summary at runs/2026-05-03-baorista-install/smoke_results.csv with
# (n, elapsed_sec, max_rhat, min_ess_bulk, converged) per tier.
#
# Convergence criterion: per preregistration §3, all Rhat < 1.05.
# ------------------------------------------------------------------------------

library(baorista)
library(posterior)
set.seed(20260503)

#' Run a single baorista smoke-test tier on synthetic aoristic data.
#'
#' Generates n synthetic inscriptions with uniform-random centres in a window
#' around 100–250 CE (the Roman imperial period the project targets), with
#' interval widths ~ Exp(mean=99) capped at 300 years, and fits an exponential
#' growth model via baorista::expfit().
#'
#' @param n         Number of synthetic inscriptions.
#' @param niter     Total MCMC iterations (default 4000).
#' @param nburnin   Burn-in iterations (default 2000).
#' @param nchains   Number of MCMC chains (default 4).
#' @return list with n, elapsed_sec, max_rhat, min_ess_bulk, converged.
run_tier <- function(n, niter = 4000, nburnin = 2000, nchains = 4) {
  # Synthetic aoristic intervals. Centres uniform in [-50, 350] (well inside
  # the Roman-imperial reference window); widths Exp-distributed with mean 99
  # years, capped at 300 (matches LIRE-like dating-uncertainty distribution).
  centres <- runif(n, -50, 350)
  widths  <- pmin(rexp(n, rate = 1 / 99), 300)
  starts  <- centres - widths / 2
  ends    <- centres + widths / 2

  # Clamp bounds inside the timeRange window. baorista's createProbMat()
  # validator rejects ANY event with a bound outside [lower, upper], so the
  # tail of the Exponential interval-width distribution must be capped here.
  # Window upper = 349 (not 350) so that (upper - lower + 1) %% resolution
  # == 0 — required so createProbMat()'s internal `seq(upper, lower, -res)`
  # and `seq(upper - res + 1, lower, -res)` produce equal-length sequences.
  # (Without this, the function stops with "resolution does not break
  # timeRange in equally sized time blocks".)
  lower <- -50
  upper <- 349
  starts <- pmax(lower, pmin(upper, starts))
  ends   <- pmax(lower, pmin(upper, ends))

  # baorista convention (read from createProbMat() body, 2026-05-04):
  #   - timeRange must satisfy timeRange[1] >= timeRange[2] (descending,
  #     BP-style; the validator literally checks `timeRange[1] < timeRange[2]`
  #     and stops "Incorrect format of timeRange argument").
  #   - For each event row, col 1 must be > col 2 (the validator stops
  #     "Some events have a start point of timespan later than its end
  #     point" if col1 <= col2). i.e. column 1 holds the LARGER calendar
  #     year of the interval; column 2 the SMALLER. The column NAMES
  #     "StartDate" / "EndDate" are conventional only — what matters is
  #     numeric ordering.
  # Therefore we put `ends` (the larger calendar year) in column 1 and
  # `starts` (smaller) in column 2, and pass timeRange = c(upper, lower).
  df   <- data.frame(StartDate = round(ends), EndDate = round(starts))
  # Eliminate any zero-width intervals (col1 == col2 fails col1 > col2).
  zero_width <- df$StartDate == df$EndDate
  if (any(zero_width)) df$StartDate[zero_width] <- df$StartDate[zero_width] + 1L
  prep <- baorista::createProbMat(df, timeRange = c(upper, lower), resolution = 5)

  t0 <- Sys.time()
  fit <- baorista::expfit(
    prep,
    niter   = niter,
    nburnin = nburnin,
    thin    = 1,
    nchains = nchains
  )
  elapsed <- as.numeric(difftime(Sys.time(), t0, units = "secs"))

  # Convergence diagnostics via posterior package (Rhat, ESS).
  draws <- posterior::as_draws_array(fit$samples)
  diag  <- posterior::summarise_draws(
    draws,
    posterior::default_convergence_measures()
  )

  list(
    n            = n,
    elapsed_sec  = elapsed,
    max_rhat     = max(diag$rhat, na.rm = TRUE),
    min_ess_bulk = min(diag$ess_bulk, na.rm = TRUE),
    converged    = all(diag$rhat < 1.05, na.rm = TRUE)
  )
}

# Run tiers and collect results.
results <- list()
for (n in c(100, 500, 5000)) {
  message(sprintf("--- Tier n=%d starting at %s ---",
                  n, format(Sys.time())))
  results[[as.character(n)]] <- run_tier(n)
  r <- results[[as.character(n)]]
  message(sprintf(
    "Tier n=%d: wall %.1fs, max Rhat %.3f, min ESS %.0f, converged=%s",
    n, r$elapsed_sec, r$max_rhat, r$min_ess_bulk, r$converged
  ))
}

# Persist results to CSV (the install log will read this back).
results_df <- do.call(rbind, lapply(results, as.data.frame))
write.csv(
  results_df,
  "runs/2026-05-03-baorista-install/smoke_results.csv",
  row.names = FALSE
)
cat("SMOKE TESTS COMPLETE\n")
