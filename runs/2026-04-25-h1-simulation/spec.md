---
priority: 1
scope: in-stream
title: "H1 min-thresholds simulation — specification"
audience: "Shawn, Adela, OSF reviewers, build agent"
date: 2026-04-25
---

# H1 min-thresholds simulation — specification

## What this is

Phase 1 of the preregistered three-phase study on mixture-corrected summed
probability analysis (SPA) of Latin inscriptions. Produces numerical minimum-
inscription-count thresholds that define the subset-eligibility bar for
confirmatory testing in Phases 2 and 3.

## Why it runs first

Without H1, we can't commit the preregistration's sample-size thresholds (§8
TBD 1 in `planning/preregistration-draft.md`). Those thresholds are
preregistered *post hoc* of this simulation but *ante hoc* of the substantive
H2 mixture validation and H3 population-signal analyses. Running H1 is
therefore the blocking step before OSF submission.

## What it does

For each cell of the experimental grid:

1. Draw a bootstrap sample of `n` inscriptions from filtered LIRE v3.0.
2. Build a synthetic summed probability analysis (SPA) via Uniform aoristic
   resampling per Decision 4 (5-year bins, 50 BC – AD 350 envelope).
3. Fit a null model (exponential or CPL-k=3) to the SPA.
4. Inject a synthetic effect of prescribed magnitude, duration, and shape
   (step-function or Gaussian) at a mid-window centre.
5. Run the Timpson-et-al.-2014 Monte Carlo envelope test at 95 % pointwise
   and compute the global *p*-value.
6. Record detection at *p* < 0.05.
7. Repeat 1,000 times per cell.

The cell grid is 256 cells: 3 subset levels × 4 effect-size brackets × up to 8
n-values × 2 null models × 2 shapes, with CPL cells additionally fitting
k ∈ {2, 3, 4} for exploratory analyses.

## What it produces

- **Primary:** minimum n per (level × bracket × null-model × shape) at which
  detection rate ≥ 0.80, reported as a range `[n_sharp, n_smooth]` bracketing
  step and Gaussian shapes.
- **Calibration:** zero-effect false-positive rate per (level × null-model);
  target ≤ 0.05.
- **Exploratory:** (i) k-sensitivity across CPL k ∈ {2, 3, 4}; (ii) AIC-select
  CPL threshold reconstruction; (iii) stratified-sampling threshold reconstruction
  (post-hoc from persisted parquet, no resimulation).
- **Reporting:** detection-rate curves at 0.70, 0.80, 0.90 thresholds; effect-size
  × n heatmaps per level; exponential-vs-CPL comparison narrative.

## Scope boundary

No LLM calls; pure local compute. Dataset-agnostic past the loader — runs
against LIST v1.2 identically if the Week-1 swap completes. Does not fit H2
mixture or H3 regression — that is Phase 2 and Phase 3.

## Key references

- `planning/preregistration-draft.md` — base protocol (§4 Phase 1).
- `planning/preregistration-amendments-2026-04-25.md` — formal amendments
  arising from plan review.
- `runs/2026-04-25-h1-simulation/plan.md` — implementation plan (plan agent).
- `runs/2026-04-25-h1-simulation/decisions.md` — Shawn-approved final
  decisions (authoritative where divergent from plan.md).
- Timpson, A. et al. 2014. "Reconstructing regional population fluctuations in
  the European Neolithic using radiocarbon dates: a new case-study using an
  improved method." *Journal of Archaeological Science* 52: 549–557.
- Crema, E. R. & Bevan, A. 2021. "Inference from large sets of radiocarbon
  dates: software and methods." *Radiocarbon* 63: 23–39.
- Carleton, W. C., Campbell, D. & Collard, M. 2018. "A reassessment of the
  impact of temporal uncertainty on summed radiocarbon date distributions."
  *PLOS ONE* 13(7): e0191055. (Power-simulation framework adapted for
  SPA × covariate.)
- Kaše, V., Heřmánková, P. & Sobotková, A. 2023. LIRE v3.0 (Zenodo DOI
  10.5281/zenodo.8147298). Dataset. Uniform aoristic approach documented
  therein; our `primitives.aoristic_resample` reimplements the Uniform
  method directly (cf. `sdam-au/tempun`).
