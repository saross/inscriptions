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
  # baorista createProbMat / timeRange conventions (read from source 2026-05-04):
  #   - timeRange must satisfy timeRange[1] >= timeRange[2] (descending,
  #     BP-style; validator stops "Incorrect format of timeRange argument"
  #     if timeRange[1] < timeRange[2]).
  #   - (upper - lower + 1) %% resolution == 0 must hold (validator stops
  #     "resolution does not break timeRange in equally sized time blocks"
  #     otherwise). With lower=-50, upper=349, resolution=5, this works:
  #     400 / 5 = 80 timeblocks.
  #   - Per-event column 1 must be > column 2 (the validator stops
  #     "Some events have a start point of timespan later than its end
  #     point" if col1 <= col2). i.e. column 1 holds the LARGER calendar
  #     year of the interval; column 2 the SMALLER. Column NAMES are
  #     conventional only — numeric ordering is what matters.
  #   - Every event must satisfy lower <= col2 <= col1 <= upper. ANY
  #     out-of-range event triggers "Some event have timespan outside the
  #     timeRange provided".
  lower <- -50L
  upper <- 349L

  # Synthetic aoristic data (smoke-test simplification, 2026-05-03 retry):
  # widths capped at 100 years (rather than the LIRE-realistic 300) so that
  # — with centres inset by max_half_width from each envelope edge —
  # no event ever spills outside [lower, upper] by construction. A previous
  # iteration with widths up to 300 + post-hoc clamping triggered
  # zero-width edge cases at the upper bound that the +1 fix-up pushed
  # outside timeRange. The capped-width approach avoids both pathologies.
  # Widths floored at 1 to prevent zero-width after rounding.
  max_width <- 100L
  half_w    <- max_width / 2L
  widths  <- pmax(1, pmin(rexp(n, rate = 1 / 99), max_width))
  centres <- runif(n, lower + half_w, upper - half_w)
  starts  <- centres - widths / 2
  ends    <- centres + widths / 2

  # ends > starts and both within [lower, upper] by construction. Column 1
  # = ends (larger year), column 2 = starts (smaller year).
  df <- data.frame(StartDate = round(ends), EndDate = round(starts))
  # Defensive zero-width nudge (rare given widths >= 1 but cheap to keep).
  zero_width <- df$StartDate == df$EndDate
  if (any(zero_width)) df$EndDate[zero_width] <- df$EndDate[zero_width] - 1L
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

  # Convergence diagnostics. baorista::expfit() returns an S3 'fittedExp'
  # list with already-computed `$rhat` (from coda::gelman.diag) and `$ess`
  # (from coda::effectiveSize), so we read those directly rather than
  # re-deriving via posterior::summarise_draws.  See expfit body inspected
  # 2026-05-04: there is NO $samples slot.
  rhat_vec <- as.numeric(fit$rhat[[1]][, 1])
  ess_vec  <- as.numeric(fit$ess)

  list(
    n            = n,
    elapsed_sec  = elapsed,
    max_rhat     = max(rhat_vec, na.rm = TRUE),
    min_ess_bulk = min(ess_vec, na.rm = TRUE),
    converged    = all(rhat_vec < 1.05, na.rm = TRUE)
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
