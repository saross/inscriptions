---
title: "baorista + brms install plan for sapphire"
date: 2026-04-24
author: "Shawn Ross (with Claude Code, Opus 4.7)"
status: plan only — no installs executed
preregistration cross-references:
  - planning/decision-log.md Decision 3 (baorista as Bayesian sensitivity)
  - planning/preregistration-draft.md §3 (aoristic sampling), §5 small-N city trajectory, §9 software stack
  - planning/future-studies.md FS-4 (provincial prosperity reconstruction)
  - planning/prior-art-scout-2026-04-25-aoristic-envelope.md §3 (baorista source review)
  - scripts/h3a_brms_shadow.R + runs/2026-04-25-h3a-brms-shadow/{plan.md, README.md}
---

# baorista + brms install plan for sapphire

This document is a **planning artefact**. It does NOT execute any
installation. It captures the reconnaissance carried out on sapphire on
2026-04-24, the install steps proposed, the smoke tests proposed, the
fallback paths, and the explicit decisions that need Shawn's approval
before any state-changing command runs on sapphire.

## 1. Why this matters

baorista (Crema 2025, *Archaeometry* DOI 10.1111/arcm.12984) is required
by the inscriptions project for three uses:

1. **Decision 3 sensitivity analysis** (preregistered) — Bayesian
   aoristic comparison against the forward-fit primary methodology, on
   representative provincial subsets. Demoted to "citation with
   rationale" if the install proves non-trivial (Decision 3 fallback,
   restated in preregistration-draft.md §7).
2. **§5 small-N city trajectory estimation, Layer A** (preregistered
   2026-04-27) — Bayesian aoristic + Intrinsic Conditional
   Autoregressive (ICAR) temporal smoothing + partial-pooling for ~800
   small-N cities below the H1 confirmatory threshold. The
   preregistration explicitly notes "Implementation likely shares the
   baorista pipeline (Decision 3) — practical economy."
3. **FS-4 follow-up paper** (provincial prosperity reconstruction,
   `planning/future-studies.md`) — baorista is the **primary**
   methodology for the follow-up paper, with provincial-scale
   trajectory estimation as the workhorse.

Adjacent install: **brms / cmdstanr** for Track 2 — the Bayesian
negative-binomial shadow for H3a at `scripts/h3a_brms_shadow.R`. Track
2 is plan + build + audit complete but **not yet executed** — input
data from H2 mixture model not yet produced. When H2 emits
`data/processed/city_level_for_h3a.parquet`, the brms shadow will
require R + brms + cmdstanr (preferred) or rstan (fallback) on
sapphire. Installing brms / cmdstanr in the same R session as baorista
amortises R-toolchain setup, so we plan the two installs together.

## 2. Stage 0 — sapphire reconnaissance (carried out 2026-04-24)

All commands below were inspected via SSH; **no state was mutated** on
sapphire. Output is recorded verbatim from the reconnaissance run.

### 2.1 Operating system and hardware

```text
PRETTY_NAME="Ubuntu 25.04"
NAME="Ubuntu"
VERSION_ID="25.04"
VERSION_CODENAME=plucky
ID=ubuntu
ID_LIKE=debian
```

- **CPU cores:** 24 (`nproc` = 24).
- **RAM:** 60 GiB total, 57 GiB available, 8 GiB swap (300 MB used).
- **Disk:** root volume 787 GB total, 486 GB free (36 % used).

The sapphire host has ample CPU, RAM, and disk headroom for a clean R
+ NIMBLE + cmdstan toolchain; no resource-pressure caveats apply.

### 2.2 What is already installed

| Component | Status | Version |
|---|---|---|
| R | **Not installed.** | — |
| g++ | Installed at `/usr/bin/g++`. | 14.2.0 (Ubuntu 14.2.0-19ubuntu2) |
| gcc-14 / g++-14 | Installed via Ubuntu packages. | 14.2.0 |
| build-essential | Installed (12.12ubuntu1). | — |
| GNU make | Installed at `/usr/bin/make`. | 4.4.1 |
| gfortran | **Not installed.** Available as `4:14.2.0-1ubuntu1` from `plucky/main`. | — |
| cmdstan | **Not installed.** Neither `~/.cmdstan` nor `~/.cmdstanr` present. | — |
| User R library (`~/.local/lib/R`) | **Absent.** | — |
| System R library (`/usr/lib/R`) | **Absent.** | — |
| baorista, brms, nimble, rstan, cmdstanr, posterior, arrow, bayesplot, loo | **None installed** (R itself is missing). | — |
| Python 3 | `/usr/bin/python3` present (Python 3.13.3). `pymc` and `cmdstanpy` **not** importable in the system Python — they presumably live in a project venv elsewhere. | 3.13.3 |

### 2.3 R availability via apt

```text
r-base: candidate 4.4.3-1 from plucky/universe
r-base-dev: candidate 4.4.3-1 from plucky/universe
```

This is **important**: Ubuntu 25.04 (plucky) ships R 4.4.3 directly
from `universe`. That clears the R ≥ 4.3 requirement (preregistration
draft §9) without needing CRAN's `r-project.org` apt repository at all.
CRAN's apt mirror sometimes lags new Ubuntu releases by months; falling
back to distro R simplifies the install path materially.

### 2.4 Existing apt sources

`/etc/apt/sources.list.d/` contains AMD GPU and ROCm repositories plus
`ubuntu.sources*`. **No CRAN repository configured.** **No Posit / r2u
binary-R repository configured.**

### 2.5 What this means

- **Full clean install** of the R toolchain (no upgrade-or-replace
  decision needed; nothing to preserve).
- **System libraries are largely already there** — `libcurl4-openssl-dev`,
  `libssl-dev`, `libxml2-dev`, `libfontconfig1`, `libfreetype6`,
  `libfribidi0`, `libharfbuzz0b`, `libjpeg-dev`, `libpng-dev`,
  `libtiff-dev` are all installed, picked up as automatic dependencies
  of other packages.
- **Missing system packages we still need**: `r-base`, `r-base-dev`,
  `gfortran`, plus a small set of `*-dev` headers that R packages
  typically need (`libharfbuzz-dev`, `libfribidi-dev`,
  `libfontconfig1-dev`, `libfreetype6-dev`).
- **g++ 14.2** is fresh; comfortably exceeds NIMBLE's g++ ≥ 5.0 floor
  (NIMBLE requires C++17 these days, but g++ 14 supports up to C++23,
  so no compiler-version risk).
- **No CRAN apt repository configuration is required** for this
  project's needs — Ubuntu's R 4.4.3 in `universe` is sufficient.

## 3. Stage 1 — install prerequisites (planned, not executed)

All commands below are **proposed**. None are run by this plan
document.

### 3.1 System packages (apt)

```bash
sudo apt update
sudo apt install -y \
    r-base r-base-dev \
    gfortran \
    libharfbuzz-dev libfribidi-dev \
    libfontconfig1-dev libfreetype6-dev
```

Rationale:

- `r-base` + `r-base-dev` — R 4.4.3 (clears R ≥ 4.3 floor for brms,
  baorista, the project preregistration §9 software stack).
- `gfortran` — required by R packages with Fortran source (NIMBLE has
  Fortran helpers; many CRAN packages do).
- The four `-dev` headers (harfbuzz, fribidi, fontconfig, freetype) are
  needed when R packages compile bindings against the system text-shaping
  / font stack. The runtime libraries are already present; only the dev
  headers are missing.

The libcurl4-openssl-dev, libssl-dev, libxml2-dev, libjpeg-dev,
libpng-dev, libtiff-dev `-dev` packages are **already installed** per
the reconnaissance; not re-listed.

**Estimated wall-time:** apt install ~2 min (depends on which mirror is
fastest; plucky packages are small).

### 3.2 cmdstan (via cmdstanr; for the brms shadow)

The Stan team's recommended Stan backend since 2022 is `cmdstanr`,
which manages a local cmdstan installation. `cmdstanr` is **not on
CRAN** — it lives on the Stan team's r-universe.

In an R session (after R is installed):

```r
# Install cmdstanr from r-universe (Stan team's preferred channel).
install.packages(
    "cmdstanr",
    repos = c("https://stan-dev.r-universe.dev",
              "https://cloud.r-project.org")
)

# Install cmdstan itself (compiles the Stan toolchain).
# cores = 23 leaves one core free for the OS; sapphire has 24.
cmdstanr::install_cmdstan(cores = 23)
```

**Estimated wall-time:**

- `cmdstanr` package install: < 30 s.
- `cmdstan` compile: ~5–10 min on sapphire's 24-core CPU. cmdstan's
  build is well-parallelised; the 23-core flag should keep it tight.
- **Disk:** ~1 GB for cmdstan + Stan headers.

### 3.3 R-version commitment

We use Ubuntu's R 4.4.3 from `plucky/universe`. This is **above** the
preregistration §9 floor (R ≥ 4.3) and matches brms' requirement
(R ≥ 4.0). No CRAN apt repository or Posit r2u repository is
configured. If a future package version needs R ≥ 4.5, we will revisit
at that time; nothing currently in the pipeline does.

## 4. Stage 2 — install baorista + dependencies (planned, not executed)

After §3 prerequisites, in an R session:

```r
# 1. NIMBLE first (baorista's MCMC backend).
#    NIMBLE compiles its own C++ helpers on first model use.
install.packages("nimble")

# 2. baorista (CRAN 0.2.1, GPL-2+, depends on nimble >= 0.12.0).
install.packages("baorista")

# 3. arrow (parquet I/O for cross-language artefacts; brms shadow uses
#    it too).
install.packages("arrow")

# 4. Optional but recommended utility packages:
install.packages(c("posterior", "bayesplot", "loo", "ggplot2"))
```

**Estimated wall-time:**

- `nimble`: ~3–5 min (CRAN download + compile of NIMBLE's C++
  internals).
- `baorista`: ~1 min (pure R wrapper around NIMBLE; small).
- `arrow`: ~3–5 min (compiles Arrow C++ bindings; can be slow but
  pre-built binaries usually available for Ubuntu).
- `posterior`, `bayesplot`, `loo`, `ggplot2`: ~3–5 min combined.

**Smoke test for baorista** (proposed; do NOT run yet):

```r
library(baorista)
# Synthetic small-N example. baorista's CRAN vignette supplies one;
# at smoke-test time we'd run that example and confirm:
#   - the function executes to completion;
#   - MCMC convergence diagnostics show Rhat < 1.05, ESS > 400;
#   - the output structure matches the documented expectation
#     (a NIMBLE samples object plus posterior summary).
# Smoke-test corpus size: n = 100 events, 10 time blocks, default
# MCMC settings. This is well below the n = 50 000 envelope where the
# computational concern in prior-art-scout §3 kicks in.
```

**Smoke-test wall-time:** at n = 100, baorista's `expfit` should
complete in ~2–5 min (default `niter = 100 000, nburnin = 50 000,
thin = 10, nchains = 4`).

## 5. Stage 3 — install brms + cmdstanr (Track 2 alongside; planned)

In the same R session as §4:

```r
# brms (CRAN; current version >= 2.22).
# Pulls in: rstan, StanHeaders, posterior, bayesplot (some duplicates
# of §4 — already installed at this point so the install is a no-op
# for those).
install.packages("brms")
```

**Estimated wall-time:** ~5–10 min (brms pulls a large graph of
dependencies; on a clean R install the heavy ones are
`StanHeaders`, `rstan`, `Rcpp`, `RcppEigen`, `BH`).

After `brms` is installed, parse-check the H3a shadow script:

```bash
Rscript -e 'parse(file = "scripts/h3a_brms_shadow.R"); cat("parses ok\n")'
```

This completes the parse-check that the original Track 2 audit
deferred to "should run on sapphire pre-execution." It does NOT run
the model — execution requires
`data/processed/city_level_for_h3a.parquet`, which the H2 mixture
pipeline has not yet emitted.

## 6. Stage 4 — validation runs (planned, not executed)

### 6.1 baorista smoke test (n = 100)

Tier 1 — minimum viable. Tests that the install works end-to-end at
trivial scale. **Wall-time: ~5 min.** Run once, on a synthetic
corpus drawn from baorista's vignette. Decision criterion: completes
cleanly, Rhat < 1.05.

### 6.2 baorista benchmark (n = 500, 5 000, 50 000)

Tier 2 — characterise computational cost before committing to
full-empire runs. Per the prior-art-scout report's [VERIFY] flag,
baorista's `expfit` defaults to `niter = 100 000, nburnin = 50 000,
thin = 10, nchains = 4`. With n = 50 000 empire-level inscriptions,
the `dAExp` custom likelihood iterates a 50 000 × n_tblocks matrix per
MCMC step. **No benchmark is reported in baorista documentation** —
this is the gap the reconnaissance run will close.

Proposed benchmark design:

| Subset size | Time blocks | MCMC settings | Purpose |
|---|---|---|---|
| n = 500 | 16 (e.g., 25-y bins from 50 BC to AD 350) | defaults | shake-out; expect minutes |
| n = 5 000 | 16 | defaults | representative provincial subset; expect tens of minutes |
| n = 50 000 | 16 | defaults | empire scale; expect hours; **flag if > 12 h** |

Decision criterion at the n = 50 000 tier:

- ≤ 4 h: usable for empire-level Decision 3 sensitivity directly.
- 4 – 24 h: usable but only on representative provincial subsets
  (which is what Decision 3 specifies anyway, ~7–10 provinces with
  n ≥ 1 000).
- \> 24 h: revisit; consider thinning, fewer chains, shorter `niter`,
  or demote to citation-with-rationale.

### 6.3 baorista vs forward-fit cross-check (Decision 3 sensitivity)

On a representative provincial subset (~1 000 inscriptions in a single
province, n.b. — Decision 7 specifies "provinces with n ≥ 1 000, ~7–10
provinces"):

- Run forward-fit envelope SPA (primary methodology) → trajectory +
  envelope.
- Run baorista `expfit` (Bayesian alternative) → posterior trajectory
  + 95 % credible interval.
- Compare visually and quantitatively (e.g., per-time-bin posterior
  median vs forward-fit median; per-time-bin agreement of CI vs
  envelope coverage).

**Decision criterion** (per Decision 3 fallback):

- Within Monte Carlo noise → Decision 3 sensitivity satisfied;
  baorista appendix figure committed.
- Substantive divergence → finding in itself; revisit forward-fit
  primary status; potentially elevates to second methodology in main
  paper or motivates FS-4 follow-up.

### 6.4 brms shadow smoke run (deferred until H2 lands)

When `data/processed/city_level_for_h3a.parquet` is available:

```bash
cd ~/Code/inscriptions
Rscript scripts/h3a_brms_shadow.R
```

Until then: the parse-check in §5 is sufficient to confirm the
toolchain is in place.

**Expected runtime** (per `runs/2026-04-25-h3a-brms-shadow/README.md`):
~2 min wall-time on a modern laptop; first-run Stan compile adds
~45 s. On sapphire's 24-core CPU, runtime should be similar or
slightly faster.

## 7. Stage 5 — fallback strategy (preregistered)

### 7.1 If NIMBLE compilation fails on sapphire

Per Decision 3 fallback (codified in preregistration-draft.md §7):

- baorista demotes from "appendix figure" to "citation with rationale"
  in the main paper.
- §5 Layer A (small-N city trajectory estimation) reverts to
  `pymc`-implemented Bayesian aoristic with ICAR. This is
  methodologically equivalent — Python rather than R, but the model
  specification is identical (Bayesian aoristic + ICAR + partial
  pooling). A `pymc` implementation is achievable in pure Python with
  PyMC's `CAR` distribution or via `cmdstanpy` for an explicit Stan
  ICAR model.
- FS-4 (provincial prosperity reconstruction) re-evaluates: either
  ports baorista's algorithm to PyMC, or relies on the Python ICAR
  alternative.

### 7.2 If brms / cmdstanr fails

Per Track 2 plan (`runs/2026-04-25-h3a-brms-shadow/plan.md` §6.3):

- **First fallback:** rstan, with the loud warning the script already
  emits. brms supports both backends; `BACKEND` variable in the script
  flips automatically if `cmdstanr` is unavailable.
- **Second fallback:** drop the brms shadow entirely. H3a runs
  `pymc`-only; we lose the cross-language posterior-validation but no
  methodological harm — the brms shadow is preregistered as
  "secondary, validation-only" not as part of the primary inference.

### 7.3 If the n = 50 000 empire-level benchmark exceeds practicable
wall-time

- Decision 3 already specifies "representative provincial subsets" —
  Crema's design naturally supports this. Empire-level baorista was
  never the primary; the comparator was always going to be a subset.
- Document the wall-time finding as a methodological observation in
  the paper's discussion (a contribution to the field, since
  prior-art-scout reports that no published baorista benchmarks
  exist).

## 8. Decisions to surface for Shawn (review gate)

The following decision points are extracted explicitly so Shawn can
sign off on each before any state-changing command runs.

| # | Decision | Recommendation | Rationale |
|---|---|---|---|
| 1 | **R version source.** | Ubuntu's R 4.4.3 from `plucky/universe`. | Clears the R ≥ 4.3 floor; no CRAN apt mirror configuration needed; avoids the 25.04-plucky-not-yet-on-CRAN risk; simpler. CRAN apt route only justified if a package needs R ≥ 4.5, which nothing in the project currently does. |
| 2 | **System-package install method.** | apt with the four extra `-dev` headers (harfbuzz, fribidi, fontconfig, freetype) + gfortran. | All other R-build prerequisites (`libcurl4-openssl-dev`, `libssl-dev`, `libxml2-dev`, `libpng-dev`, `libtiff-dev`, `libjpeg-dev`) are already installed. |
| 3 | **NIMBLE install path.** | CRAN (`install.packages("nimble")`). | Standard, no special handling needed. NIMBLE's auto-compile of C++ helpers is robust on g++ 14. |
| 4 | **cmdstanr install path.** | r-universe (`stan-dev.r-universe.dev`), the Stan team's preferred channel. | r-universe tracks Stan releases continuously; CRAN's cmdstanr lags. Per `runs/2026-04-25-h3a-brms-shadow/plan.md` §6.3 critical-friend item. |
| 5 | **cmdstan compile cores.** | `cores = 23` (leave 1 free for OS / interactive shell). | sapphire has 24 cores; `nproc - 1` is a conservative parallel-build setting. |
| 6 | **brms install timing.** | Install brms in the same R session as baorista; **defer execution** of the H3a shadow until H2 emits the input parquet. | Amortises R-toolchain setup; the parse-check confirms toolchain readiness without needing real data. |
| 7 | **Smoke-test corpus tiers.** | Tier 1 (n = 100, ~5 min) → Tier 2 benchmark (n = 500, 5 000, 50 000) → Tier 3 (Decision 3 cross-check on a real ~1 000-inscription province). | Surfaces compute issues before committing to full-empire runs (per the prior-art-scout [VERIFY] flag on baorista wall-time at n = 50 000). |
| 8 | **Compile-time budget.** | Confirm sapphire is OK to dedicate ~30 min of compute to R + cmdstan + NIMBLE + brms compile + arrow build, plus another ~15 min to smoke tests. **Total install + smoke-test wall-time: ~45–60 min** of single-user attention; benchmark Stage 4.2 may run for hours on the n = 50 000 tier (run as a background job with `nohup` or `screen`). | Single-shot install; subsequent uses reuse cached compiled objects. |
| 9 | **Reconnaissance Python venv.** | The system Python on sapphire has neither pymc nor cmdstanpy. The fallback Python-pymc path (Stage 5.1) would need a project venv on sapphire, mirroring the local `~/Code/inscriptions/.venv/`. **Confirm whether a sapphire-side project venv exists** (the reconnaissance did not find one) — if not, the Python fallback is itself a non-trivial step. | Worth flagging because the Decision 3 fallback assumes the Python path is "free"; on sapphire it isn't yet. |

## 9. Risk register

Top five risks, ranked by likelihood × impact, each with a mitigation
or contingency.

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | **NIMBLE C++ compile fails** (e.g., a subtle Plucky/g++ 14.2 incompatibility that NIMBLE upstream hasn't shipped a fix for). | Low–medium. NIMBLE has a track record of being fussy at the bleeding edge; Ubuntu 25.04 is a recent release. | High — knocks out baorista entirely. | Stage 5.1 fallback: `pymc` ICAR for §5 Layer A; demote Decision 3 to citation. **Mitigation in advance:** check NIMBLE's CRAN page release notes for "Tested against R ≥ 4.4 / g++ 14"; if unconfirmed, pin to a known-good NIMBLE release. |
| 2 | **`baorista expfit` n = 50 000 wall-time exceeds 24 h** at default MCMC settings. | Medium–high. `dAExp` custom likelihood is O(n × n_tblocks) per MCMC step, ×4 chains × 100 000 iters = ~10¹³ FLOPs at empire scale. Prior-art-scout flagged this with [VERIFY]. | Medium — Decision 3 already specifies provincial-subset runs (n ≈ 1 000), so empire-scale runs were never on the critical path. | Tier 2 benchmark (Stage 4.2) is **specifically designed to surface this risk before commitment**. If wall-time at n = 50 000 is unworkable, document and stay at provincial-subset scale per Decision 3. |
| 3 | **cmdstan compile fails or is slow on sapphire's CPU**. | Low. Stan's build is well-tested across Linux/g++ versions. | Medium — `rstan` fallback exists per §7.2. | Track 2's existing fallback handles this; the script switches backend automatically. |
| 4 | **arrow R package compile fails** (Arrow C++ bindings are the most common "where did half an hour go" CRAN install). | Medium. Arrow's R bindings sometimes need manual config or a pre-built binary. | Medium — needed for parquet I/O on both baorista trajectory outputs and brms shadow posterior draws. | Pre-built Linux binaries are usually available; if compile fails, install via `apt install r-cran-arrow` (Ubuntu's binary R-arrow package, may lag CRAN). Alternative: CSV exchange instead of parquet at the slight cost of round-trip fidelity. |
| 5 | **The Python-pymc fallback (Stage 5.1) requires its own sapphire venv setup** that the reconnaissance hasn't scoped. | Medium. The local project venv at `~/Code/inscriptions/.venv/` does not exist on sapphire (system Python 3.13.3 has neither pymc nor cmdstanpy importable). | Low–medium — a `uv venv` + `uv pip install` round-trip on sapphire is straightforward but adds ~10–15 min of work that the Decision 3 fallback assumes is "free". | Flag in §8 Decision 9 above. If Stage 5 fallback is invoked, scope the sapphire-side Python venv setup as a sub-task at that time. |

## 10. Summary table — total estimated wall-time

| Stage | Action | Wall-time |
|---|---|---|
| 1 | apt install (R + gfortran + 4 dev headers) | ~2 min |
| 1 | cmdstan compile via cmdstanr | ~5–10 min |
| 2 | NIMBLE install (CRAN, with C++ compile) | ~3–5 min |
| 2 | baorista install (CRAN, pure R) | ~1 min |
| 2 | arrow install (CRAN) | ~3–5 min |
| 2 | posterior + bayesplot + loo + ggplot2 install | ~3–5 min |
| 3 | brms install (CRAN, deps via Rcpp/StanHeaders) | ~5–10 min |
| 4.1 | baorista n = 100 smoke test | ~5 min |
| 4.2 | baorista n = 500 benchmark | ~5–10 min |
| 4.2 | baorista n = 5 000 benchmark | ~30–60 min |
| 4.2 | baorista n = 50 000 benchmark | **unknown — flag if > 12 h** |
| 4.4 | brms shadow parse-check | < 5 s |
| 4.4 | brms shadow execution | (deferred until H2 lands; ~2 min once it does) |

**Total install + Tier-1 smoke wall-time:** ~30–45 min of foreground
compute, plus ~5 min of attended interaction (apt sudo, R session
setup).

**Total install + Tier-2 benchmark wall-time:** ~1.5–3 h foreground at
n ≤ 5 000; **n = 50 000 benchmark may run for hours and should run
backgrounded**.

## 11. Constraints respected

- **No installs executed by this plan** — Stage 0 reconnaissance was
  read-only (`which`, `--version`, `apt-cache policy`, `ls`, `df`,
  `free`, `cat /etc/os-release`).
- **No API calls.**
- UK / Australian English; Oxford comma.
- This document is the single artefact; commit message documented in
  the parent task brief.

## 12. Provenance

- **Reconnaissance run:** 2026-04-24 by Claude Code (Anthropic, Opus
  4.7) under Shawn Ross's direction, via SSH to `sapphire`.
- **Plan author:** Claude Code, working from the briefing in the task
  prompt and the cited project planning documents.
- **Approval:** pending Shawn's review of §8 (Decisions to surface).
