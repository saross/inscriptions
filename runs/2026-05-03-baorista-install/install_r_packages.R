# ------------------------------------------------------------------------------
# install_r_packages.R — orchestrate cmdstanr + NIMBLE + baorista + brms install
#
# Author:        Shawn Ross (shawn@faims.edu.au) and Claude Code (Opus 4.7, 1M)
# Date:          2026-05-03
# Licence:       MIT
# Preregistration cross-reference:
#   - planning/baorista-install-plan.md §2 (Stage 2 install plan)
#   - planning/decision-log.md Decision 3 (baorista as Bayesian sensitivity)
#   - runs/2026-04-25-h3a-brms-shadow/plan.md (Track 2 brms shadow design)
#
# Purpose
# -------
# Runs on sapphire after Stage 1 system-package install (R + gfortran + dev
# headers). Installs the R-side toolchain for both Decision 3 baorista
# sensitivity analysis and the Track 2 brms shadow:
#
#   1. cmdstanr from r-universe (Stan team's preferred channel)
#   2. NIMBLE from CRAN (baorista's MCMC backend)
#   3. baorista from CRAN
#   4. brms + arrow + posterior + bayesplot + loo from CRAN
#
# The cmdstan binary itself was compiled earlier by cmdstanpy at
# ~/.cmdstan/cmdstan-2.38.0 — we reuse that path via cmdstanr::set_cmdstan_path()
# so we do NOT pay a second ~5–10 min compile cycle.
#
# Compile cores
# -------------
# Uses parallel::detectCores() - 1 (= 23 on sapphire) for both R-package C++
# compilation and any cmdstan compile fallback.
#
# Smoke checks
# ------------
# After NIMBLE installs, this script compiles a trivial NIMBLE model to confirm
# the C++ toolchain is wired up correctly. After all packages install, it
# library()s each one and prints versions.
# ------------------------------------------------------------------------------

# Allocate compile cores: leave one free for the OS / interactive shell.
cores <- max(1L, parallel::detectCores() - 1L)
options(Ncpus = cores)
message(sprintf("Using %d compile cores", cores))

# --- 1. cmdstanr from r-universe ----------------------------------------------
# r-universe tracks Stan releases continuously; CRAN's cmdstanr lags. Per the
# Track 2 plan §6.3 (cmdstanr-preferred design), this is the approved channel.
message("--- Installing cmdstanr ---")
install.packages(
  "cmdstanr",
  repos = c("https://stan-dev.r-universe.dev", getOption("repos"))
)

# Reuse cmdstan compiled by cmdstanpy if present (saves ~5–10 min recompile).
# Path captured during Stage 0 cmdstanpy install on 2026-05-03.
cmdstan_existing <- "/home/shawn/.cmdstan/cmdstan-2.38.0"
if (dir.exists(cmdstan_existing)) {
  cmdstanr::set_cmdstan_path(cmdstan_existing)
  message(sprintf("Reusing existing cmdstan at %s", cmdstan_existing))
  # Confirm cmdstanr can see it.
  message(sprintf("cmdstanr cmdstan_version: %s", cmdstanr::cmdstan_version()))
} else {
  message("No existing cmdstan found; installing via cmdstanr (~5–10 min)")
  cmdstanr::install_cmdstan(cores = cores)
}

# --- 2. NIMBLE from CRAN ------------------------------------------------------
# NIMBLE compiles its own C++ helpers on first model use; the install itself
# is comparatively quick (~1 min). The smoke compile below is what surfaces
# any g++ 14.2 / Plucky compatibility issue (Risk 1 in the install plan §9).
message("--- Installing NIMBLE ---")
install.packages("nimble")
library(nimble)

# Smoke: compile a trivial NIMBLE model. If this fails we trigger the
# Decision 3 fallback (PyMC ICAR; pre-installed in Stage 0).
message("--- NIMBLE smoke compile ---")
nimbleCode_smoke <- nimbleCode({ y ~ dnorm(0, 1) })
suppressMessages(nimbleModel(nimbleCode_smoke, data = list(y = 0.5)))
message("NIMBLE smoke compiled OK")

# --- 3. baorista from CRAN ----------------------------------------------------
# Pure-R wrapper around NIMBLE; small install.
message("--- Installing baorista ---")
install.packages("baorista")
library(baorista)
message(sprintf("baorista version: %s", utils::packageVersion("baorista")))

# --- 4. brms + diagnostic / I-O packages from CRAN ----------------------------
# brms pulls in StanHeaders, rstan, Rcpp, RcppEigen, BH (large dep graph).
# arrow gives parquet I/O for cross-language artefact exchange.
message("--- Installing brms + arrow + posterior + bayesplot + loo ---")
install.packages(c("brms", "arrow", "posterior", "bayesplot", "loo"))

# --- Final import smoke -------------------------------------------------------
library(brms)
library(posterior)
library(arrow)
library(bayesplot)
library(loo)
message("--- All package imports OK ---")

# Print versions for the install log.
pkg_versions <- sapply(
  c("cmdstanr", "nimble", "baorista", "brms", "arrow",
    "posterior", "bayesplot", "loo"),
  function(p) as.character(utils::packageVersion(p))
)
message("Installed package versions:")
for (n in names(pkg_versions)) {
  message(sprintf("  %s: %s", n, pkg_versions[[n]]))
}

cat("INSTALL COMPLETE\n")
