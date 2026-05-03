---
title: "baorista + brms install log — sapphire"
date: 2026-05-03
author: "Shawn Ross (with Claude Code, Opus 4.7, 1M context)"
status: PARTIAL — halted at Stage 1 (apt requires interactive sudo)
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
| 0 | uv add pymc + cmdstanpy | **PASS** | ~30 s | "5–10 min for cmdstan compile" |
| 0 | cmdstanpy install_cmdstan() | **PASS** | ~6 min (estimate from log) | 5–10 min |
| 1 | apt update + install (R + gfortran + 4 dev headers) | **HALTED — sudo non-interactive** | n/a | ~2 min |
| 2 | cmdstanr + NIMBLE + baorista + brms | **NOT YET RUN** (depends on Stage 1) | — | ~25–35 min |
| 3 | Track 2 brms parse-check | **NOT YET RUN** (depends on Stage 2) | — | < 5 s |
| 4 | baorista tiered smoke tests | **NOT YET RUN** (depends on Stage 2) | — | 2–4 h |
| 5 | INSTALL-LOG.md + final commit | **PARTIAL** (this document; final pass at completion) | — | n/a |

## Stage 0 — PyMC + cmdstanpy pre-install (PASS)

Per Shawn's 2026-05-03 directive, pre-installed PyMC and cmdstanpy on
sapphire's project venv defensively, so the Decision 3 fallback path
(Python ICAR for §5 Layer A and Decision 3 sensitivity) is "free" if
NIMBLE compilation later fails.

Commands run:

```bash
ssh sapphire 'cd ~/Code/inscriptions && ~/.local/bin/uv add pymc cmdstanpy'
ssh sapphire 'cd ~/Code/inscriptions && .venv/bin/python3 -c "import pymc, cmdstanpy; print(pymc.__version__, cmdstanpy.__version__)"'
```

Outcome:

- pymc 5.28.5 added to project deps.
- cmdstanpy 1.3.0 added to project deps.
- Imports verified clean: `5.28.5 1.3.0`.

cmdstan compile (cmdstanpy.install_cmdstan(cores=23)):

- Installed `cmdstan-2.38.0` at `/home/shawn/.cmdstan/cmdstan-2.38.0`
  (1.2 GB).
- Test model (`bernoulli.stan`) compiled and linked successfully.
- Wall-time approx 6 min (from launch to first verification — exact
  timing not preserved, log captured at `/tmp/cmdstan_install.log` on
  sapphire).

This cmdstan path is recorded in `install_r_packages.R` so cmdstanr
will reuse it via `cmdstanr::set_cmdstan_path()`, avoiding a second
~5–10 min compile cycle.

Local commit (Stage 0 deps):

- Commit hash: `066f25d`
- Message: `deps: pre-install pymc + cmdstanpy on sapphire venv (Decision 3 fallback)`
- Files: `pyproject.toml`, `uv.lock`
- Push: pushed to `origin/main`.

## Stage 1 — R toolchain + system deps (HALTED)

Per the plan, attempted:

```bash
ssh sapphire 'sudo -n apt-get update'
```

`sudo` returned `sudo: a password is required`. Per the standing
constraint in the brief ("Do NOT attempt to bypass sudo with NOPASSWD
or other tricks"), this stage is **halted** awaiting Shawn's
manual run.

Verified state:

- R: not installed (`R --version` → command not found).
- gfortran: not installed (`gfortran --version` → command not found).
- `dpkg -l r-base` returns no matching package.

This matches the 2026-04-24 reconnaissance recorded in the install
plan §2.2.

### Action required from Shawn

Run the following on sapphire (interactively, with sudo password):

```bash
ssh sapphire
sudo apt-get update
sudo apt-get install -y r-base r-base-dev gfortran \
    libharfbuzz-dev libfribidi-dev \
    libfontconfig1-dev libfreetype6-dev
R --version && which Rscript && gfortran --version
```

Once R is in place, resume from Stage 2 by running:

```bash
ssh sapphire 'cd ~/Code/inscriptions && Rscript runs/2026-05-03-baorista-install/install_r_packages.R 2>&1 | tee runs/2026-05-03-baorista-install/install.log'
```

The install script is committed and pre-staged on sapphire at
`~/Code/inscriptions/runs/2026-05-03-baorista-install/install_r_packages.R`.

## Stage 2 — Pending (will run after Stage 1)

Script: `runs/2026-05-03-baorista-install/install_r_packages.R`.

Approved configuration:

- cmdstanr from r-universe (Stan-team channel).
- NIMBLE from CRAN.
- baorista from CRAN.
- brms + arrow + posterior + bayesplot + loo from CRAN.
- Compile cores: `parallel::detectCores() - 1` (= 23 on sapphire).
- cmdstan reuse: `cmdstanr::set_cmdstan_path("/home/shawn/.cmdstan/cmdstan-2.38.0")`
  (reuses cmdstanpy's compile; saves ~5–10 min).

Decision 3 fallback fires here if NIMBLE smoke compile fails.

## Stage 3 — Pending

Track 2 brms parse-check:

```bash
ssh sapphire 'cd ~/Code/inscriptions && Rscript -e "parse(file=\"scripts/h3a_brms_shadow.R\"); cat(\"parses ok\\n\")"'
```

## Stage 4 — Pending

Script: `runs/2026-05-03-baorista-install/smoke_test.R`.

Tiers: n = 100, 500, 5,000. Per the brief, n = 50,000 is deferred to
FS-4 timing study.

## Stage 5 — Pending

Final commit and push at completion.

## Open issues

- Stage 1 halt awaits Shawn's manual sudo run.
- n = 50,000 baorista wall-time still unknown — flagged for FS-4
  timing study (per brief).
- Verify baorista API surface (`createProbMat`, `expfit`) at first
  smoke run; one retry permitted before halting.

## Provenance

- Operator: Claude Code (Opus 4.7, 1M context) under Shawn Ross's
  direction.
- Date: 2026-05-03.
- Plan source: `planning/baorista-install-plan.md` (commit `507c0c8`).
