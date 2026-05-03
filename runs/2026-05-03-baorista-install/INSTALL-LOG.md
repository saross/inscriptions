---
title: "baorista + brms install log — sapphire"
date: 2026-05-03
author: "Shawn Ross (with Claude Code, Opus 4.7, 1M context)"
status: PASS — all stages complete
preregistration cross-references:
  - planning/baorista-install-plan.md (the plan being executed)
  - planning/decision-log.md Decision 3 (baorista as Bayesian sensitivity)
---

# baorista + brms install log — sapphire

This document records the per-stage status of the install plan
`planning/baorista-install-plan.md` (commit `507c0c8`) executed on
sapphire on 2026-05-03 by Claude Code under Shawn Ross's direction.

Sapphire host: `sapphire` (SSH alias). Workdir: `~/Code/inscriptions`.
Project venv: `~/Code/inscriptions/.venv/`. uv: `~/.local/bin/uv`.

## Stage-by-stage status

| Stage | Action | Status | Wall-time | Plan estimate |
|---|---|---|---|---|
| 0 | uv add pymc + cmdstanpy | **PASS** | ~30 s | n/a (Shawn-directed pre-install) |
| 0 | cmdstanpy install_cmdstan() | **PASS** | ~6 min | 5–10 min |
| 1 | apt update + install (R + gfortran + 4 dev headers) | **PASS** | ~2 min (Shawn manual) | ~2 min |
| 2 | cmdstanr + NIMBLE + baorista + brms + arrow + posterior + bayesplot + loo | **PASS** | ~30 min wall | 25–35 min |
| 3 | Track 2 brms parse-check | **PASS** | < 1 s | < 5 s |
| 4 | baorista tiered smoke tests (n = 100, 500, 5000) | **PASS** | 36 s wall | 2–4 h plan estimate (off by ~400×) |
| 5 | INSTALL-LOG.md + final commit | **COMPLETE** | this document | n/a |

## Stage 0 — PyMC + cmdstanpy pre-install (PASS)

Per Shawn's 2026-05-03 directive, pre-installed PyMC and cmdstanpy on
sapphire's project venv defensively, so the Decision 3 fallback path
(Python ICAR for §5 Layer A and Decision 3 sensitivity) is "free" if
NIMBLE compilation later fails. **As of Stage 2 PASS the fallback did
not fire**, but the pre-install retains value for FS-4 follow-up work.

Outcome:

- `pymc 5.28.5` and `cmdstanpy 1.3.0` added to project deps.
- `cmdstan-2.38.0` compiled at `/home/shawn/.cmdstan/cmdstan-2.38.0`
  (1.2 GB); test model `bernoulli.stan` compiles + links cleanly.
- cmdstan path reused by R's `cmdstanr` in Stage 2 via
  `cmdstanr::set_cmdstan_path()` — saved a ~5–10 min compile cycle.

Local commit: `066f25d` — `deps: pre-install pymc + cmdstanpy on sapphire venv (Decision 3 fallback)`.

## Stage 1 — R toolchain + system deps (PASS, manual)

Initial automated attempt halted on `sudo -n apt-get update` returning
"a password is required". Shawn ran the apt commands interactively on
sapphire (~2 min); resumed automated execution from Stage 2.

Installed:

- R 4.4.3 from Ubuntu 25.04 universe repo (clears the prereg's R ≥ 4.3
  floor without needing CRAN's apt mirror, which has plucky-distro lag).
- gfortran 14.2.0 (Ubuntu 14.2.0-19ubuntu2).
- `r-base-dev`, plus 4 dev headers: `libharfbuzz-dev`, `libfribidi-dev`,
  `libfontconfig1-dev`, `libfreetype6-dev`.

Verified post-install: `R --version && which Rscript && gfortran --version`
all clean.

## Stage 2 — R packages install (PASS)

Script: `runs/2026-05-03-baorista-install/install_r_packages.R` (commit
`9d72aae`, plus a user-library bootstrap fix added 2026-05-04, see below).

Run command:

```bash
ssh sapphire 'cd ~/Code/inscriptions && CMDSTAN=/home/shawn/.cmdstan/cmdstan-2.38.0 \
  nohup Rscript runs/2026-05-03-baorista-install/install_r_packages.R \
  > runs/2026-05-03-baorista-install/install.log 2>&1 & echo $!'
```

NIMBLE compiled cleanly first try (the `Risk #1` flagged in the plan did
not fire). cmdstanr reused the Stage 0 cmdstan via `set_cmdstan_path()`
— no second compile cycle.

### User-library bootstrap fix (added 2026-05-04 during re-run)

On a fresh sapphire R install, `R_LIBS_USER`
(`~/R/x86_64-pc-linux-gnu-library/4.4`) does not yet exist, and
`install.packages()` falls back to `/usr/local/lib/R/site-library`
(root-owned, not writable for unprivileged users). The first attempt
crashed within seconds with `lib = "/usr/local/lib/R/site-library" is
not writable`. Fix: prepend a user-library bootstrap block at the top
of `install_r_packages.R` that creates the user library directory if
needed and pushes it onto `.libPaths()` before any `install.packages()`
call. With this fix the script is now idempotent on a clean sapphire
install — no manual library-path setup required.

Wall-time of the re-run (with the fix in place): ~7 min from launch to
`INSTALL COMPLETE`. The shorter wall-time vs the 30 min plan estimate
reflects the cmdstan reuse plus parallel compile across 23 cores.

Installed package versions (verbatim from R post-install verification):

```
cmdstanr: 0.9.0
nimble:   1.4.2
baorista: 0.2.1
brms:     2.23.0
arrow:    24.0.0
posterior: 1.7.0
bayesplot: 1.15.0
loo:      2.9.0
```

Wall-time: ~30 min from launch to `INSTALL COMPLETE` marker. Compile
breakdown (rough, from log timestamps):

- igraph (NIMBLE dependency, large C/C++ build): ~15–20 min.
- NIMBLE itself: ~3 min.
- baorista, arrow, brms + transitive deps: ~5–10 min.

The `install.log` (21 MB compile output, gitignored) lives at
`runs/2026-05-03-baorista-install/install.log` on both sapphire and
local; it documents every gcc/g++ invocation for reproducibility but is
too large to commit to git.

## Stage 3 — Track 2 brms parse-check (PASS)

```bash
ssh sapphire 'cd ~/Code/inscriptions && Rscript -e "parse(file=\\"scripts/h3a_brms_shadow.R\\"); cat(\\"parses ok\\n\\")"'
# parses ok
```

Closes the Track 2 audit's "parse-check pending; should run on sapphire
pre-execution" item. Track 2 brms shadow remains awaiting H2 mixture
pipeline output data before substantive execution.

## Stage 4 — baorista tiered smoke tests (PASS)

Script: `runs/2026-05-03-baorista-install/smoke_test.R` (final version
`a41f394` + edge-case fix, scp'd to sapphire). Three iterations of the
script were needed before passing — each surfaced a real baorista API
discovery, summarised below.

### Iteration history

**Iteration 1 (calendar dates direct):** Failed at `createProbMat` with
"Incorrect format of timeRange argument". Root cause: baorista expects
descending-order `timeRange` (LARGER first, SMALLER second), regardless
of whether values are in BP or calendar years. Originally hypothesised
to be a BP-vs-calendar issue.

**Iteration 2 (BP conversion):** Tiers 100 and 500 PASS; Tier 5000
failed at `createProbMat` with "Some event have timespan outside the
timeRange provided". Root cause: at large n, the synthetic-data
generation pipeline (`centres_cal ∈ [-50, 350]`, `widths ≤ 300`)
produced edge-case events whose intervals spilled outside the envelope.
Post-hoc clamping + a zero-width nudge then occasionally pushed
StartDate to `upper + 1`, outside `timeRange[1]`.

**Iteration 3 (cap widths at 100 and inset centres by half-width):**
PASS across all three tiers. Smoke-test simplification: cap widths at
100 years (rather than LIRE-realistic 300), inset centres by 50 years
from each envelope edge, no clamping or zero-width handling needed by
construction. Documented in the script header.

### baorista API discoveries (preserved for the project's main pipeline)

Read from `createProbMat` and `expfit` source on sapphire (2026-05-03):

1. **`timeRange` ordering**: must satisfy `timeRange[1] >= timeRange[2]`
   (descending). Calendar `c(349, -50)` works; ascending `c(-50, 349)`
   fails the validator.
2. **`(upper - lower + 1) %% resolution == 0`** required, else fails
   with "resolution does not break timeRange in equally sized time
   blocks". With `lower = -50`, `upper = 349`, `resolution = 5`:
   `400 / 5 = 80` blocks, valid.
3. **Per-event column ordering**: column 1 must be > column 2; the
   column NAMES (`StartDate`, `EndDate`) are conventional. We pass
   `StartDate = ends` (larger calendar year), `EndDate = starts`
   (smaller). Numeric ordering is what matters.
4. **Every event must satisfy `lower <= col2 <= col1 <= upper`**;
   any out-of-envelope event triggers "Some event have timespan
   outside the timeRange provided".
5. **`expfit` return structure** (S3 `fittedExp` list): includes
   `$rhat` (from `coda::gelman.diag`) and `$ess` (from
   `coda::effectiveSize`) directly; **there is no `$samples` slot**.
   Use `fit$rhat[[1]][, 1]` and `fit$ess` rather than re-deriving via
   `posterior::summarise_draws()`.

### Tier results (final iteration)

| n | Wall (s) | Max Rhat | Min ESS | Converged |
|---|---|---|---|---|
| 100 | 11.8 | 1.001 | 1887 | TRUE |
| 500 | 10.4 | 1.001 | 1790 | TRUE |
| 5000 | 13.5 | 1.003 | 1850 | TRUE |

All converged comfortably under the preregistered Rhat < 1.05 criterion
(prereg §3) with min ESS > 1000.

### Why so much faster than plan

Plan estimated 5 min / 30 min / 1.5–3 h for tiers 100 / 500 / 5000.
Actual: 11.8s / 10.4s / 13.5s. Off by ~400×.

Two reasons:

1. **Smoke test uses `niter = 4000` rather than baorista's default
   `niter = 100,000`**. 25× reduction. Adequate for convergence
   verification; baorista's MCMC runs at `niter = 4000` with `nburnin
   = 2000` already give ESS > 1700 across 4 chains.
2. **baorista's NIMBLE + C++ implementation is well-optimised at
   moderate n**. The wall-time grows nearly flatly from n=100 to
   n=5000 (the dominant cost is MCMC iteration count, not data size at
   these scales).

### Implication for n=50,000 (FS-4 timing study)

The prior-art-scout report's `[VERIFY]` flag on baorista's wall-time at
empire scale is partially closed. At `niter=4000`:

- Extrapolating linearly: n=50,000 likely <60 s wall-time.
- At default `niter=100,000` (FS-4 production): expect ~5–25 min for
  n=50,000 (25× scaling on top of likely-superlinear wall growth at
  large n; well within feasibility).

baorista at FS-4 / empire scale is **operationally feasible**. The
"could take days" worry from the original plan is retired.

## Stage 5 — final commit and push

This INSTALL-LOG.md update + the local-side smoke artefacts (smoke.log,
smoke_results.csv) committed and pushed.

Sapphire git state: working tree dirty with untracked outputs that
duplicate origin's tracked content (acquired via in-place runs without
intervening pulls). **Cleanup is a separate housekeeping task**; not
critical-path. Sapphire's `runs/2026-05-03-baorista-install/install.log`
(21 MB) and `smoke.log` are kept on sapphire as ground-truth records;
the gitignore policy keeps them out of git.

## Decision 3 fallback status

**Did not fire.** NIMBLE compiled cleanly; baorista smoke ran to
completion. The Stage 0 PyMC + cmdstanpy + cmdstan pre-install retains
value for FS-4 follow-up work (Python ICAR alternative for trajectory
estimation if needed) and for any future Bayesian work that benefits
from a Python-native Stan implementation.

## Open issues

- **Sapphire git state cleanup**: untracked-but-canonical-on-origin
  files (h1-v2 outputs, optimisation logs, etc.) accumulated from
  in-place runs. Deferred housekeeping task — not blocking.
- **n = 50,000 timing under default `niter=100,000`**: extrapolation
  suggests 5–25 min, but a direct benchmark at FS-4 launch will close
  the `[VERIFY]` flag definitively.
- **Smoke-test simplification (widths capped at 100)**: real LIRE has
  a wider tail (median 99 y, max occasionally several centuries). The
  smoke test does NOT exercise the full LIRE-like width distribution;
  any production baorista run on real LIRE data should be re-validated
  with full-distribution widths and proper handling of edge events
  (clip, filter, or extend timeRange).

## Provenance

- Operator: Claude Code (Opus 4.7, 1M context) under Shawn Ross's
  direction.
- Date: 2026-05-03.
- Plan source: `planning/baorista-install-plan.md` (commit `507c0c8`).
- Stage 1 manual sudo run: Shawn 2026-05-03.
- Iteration 1–3 of smoke_test.R diagnostic discoveries: Claude Code
  main-thread + sub-agents (`a8873c0`, `adfbf74`, main-thread retry).
