---
priority: 1
scope: in-stream
title: "H1 simulation — final design decisions (2026-04-25)"
audience: "build agent (implementation), /audit, Shawn (record)"
status: final; Shawn sign-off 2026-04-25
---

# H1 simulation — final design decisions

Authoritative record of choices made during Shawn's 2026-04-25 plan review. These
decisions override the "plan default" language in `plan.md` §3 where different; they
are the specification the build agent implements against.

---

## Decision 1 — Permutation-envelope primitive (resolves plan §3.1 surfacing)

**Hand-rolled Timpson et al. 2014 Monte Carlo envelope loop**, not
`scipy.stats.permutation_test`. `scipy.stats.permutation_test` is for two-sample
exchangeability tests, not within-SPA deviation detection against a parametric
null. `scipy.stats.monte_carlo_test` is a candidate building block the build
agent may use if its API fits the inner MC replicate step; otherwise hand-rolled.

**Consequence:** preregistration §3 wording requires amendment. See
`planning/preregistration-amendments-2026-04-25.md`.

---

## Decision 2 — Effect-shape bracket (resolves plan §3.2 surfacing)

**Both step-function (box-car) and Gaussian shapes injected; thresholds reported as
a range per bracket.**

- **Step-function:** sharp edges; unambiguous mapping to prereg language
  ("X % sustained over ≥ Y y" = box-car of magnitude X for duration Y). Produces
  the **lower bound** on n for detection ≥ 0.80.
- **Gaussian:** nadir = bracket magnitude, FWHM = bracket duration. Smooth;
  deliberately conservative for envelope tests. Produces the **upper bound** on n.
- **Reported threshold:** range `[n_sharp, n_smooth]` per (level × bracket × null-model).

**Rationale:** real events span both shapes (Antonine Plague is sharp, economic
decline is gradual); bracketing honestly reflects shape-dependence without
overcommitting.

**Consequence:** cell count doubles to 256. Preregistration §4 + §6 require
amendment.

---

## Decision 3 — CPL knot count (resolves plan §3.4 surfacing)

**Primary: fix k = 3 for all CPL fits.** Clean comparison to exponential null;
reproducible; no per-cell knot-selection edge cases.

**Stored per iteration for exploratory analysis:** fit k ∈ {2, 3, 4} and persist
the AIC for each plus detection results against each. Primary report uses k = 3
column; exploratory analyses computed post-hoc from persisted parquet:

- **Exploratory A (k-sensitivity):** threshold at each fixed k ∈ {2, 3, 4}.
  Diagnostic for "is CPL threshold robust to k?"
- **Exploratory B (AIC-select):** per-iteration pick of k with minimum AIC;
  threshold under AIC-select decision rule. Answers "what would Timpson-et-al.
  AIC-select have given?"

**Rationale:** one simulation, three answers to three distinct questions.
Primary stays clean (k = 3 only); exploratories give reviewer-facing completeness
without a second run.

**Compute consequence:** CPL-side MC replicate work triples (one MC run per
k ∈ {2, 3, 4}). Total ~2× total work vs single-k simulation. See Decision 6
wall-time.

---

## Decision 4 — Sampling strategy (resolves plan §9 risk f)

**Primary: sampling-with-replacement from filtered LIRE** (bootstrap-style).
Consistent with H1's detection-at-given-n question.

**Exploratory (explicit in prereg §5):** post-hoc **stratified-by-province /
stratified-by-urban-area** sensitivity computed from persisted per-iteration
parquet. No re-simulation required — we record each sampled row's province/city
in the per-iteration schema, then the stratification is a selection over
persisted rows. Reports deltas to primary (bootstrap) thresholds.

**Rationale:** Shawn's 2024 practice is bootstrap; stratified-sensitivity answers
the natural "does empirical mix matter?" question without re-running.

**Schema addition:** per-iteration parquet gains `sampled_row_ids` (list of row
indices drawn that iteration) — 1-3 MB overhead across 128,000 iterations.
Alternative if storage becomes concerning: persist `province_counts` and
`city_counts` per iteration (2 small dicts), which is sufficient for
stratified-sampling reconstruction under the bootstrap model.

---

## Decision 5 — Compute location (resolves plan §6 + §10 surfacings)

**Execution on sapphire via SSH.** Shawn's 2026-04-25 directive: sapphire is a
modern, powerful machine; amd-tower is older and slower; only the lightest
tasks run locally.

**Orchestration pattern:**

1. Build agent writes code locally in this repo.
2. Commit locally; push to `origin/main`.
3. On sapphire: `git pull && uv sync` (reconcile deps + latest code).
4. Launch under `nohup ... &> run.log &` (survives SSH disconnect) with the
   master process PID captured to `runs/.../outputs/run.pid`.
5. Monitor from here: `pgrep -f "[.]venv/bin/python3.*h1_sim.py"` (bracket-escape
   per stall-guard rule) or `kill -0 <captured_pid>`.
6. On completion: `rsync` outputs back to local repo; commit outputs.

**GPU (16 GB ROCm on sapphire):** not used for H1. Simulation is embarrassingly
parallel CPU work; numpy + joblib on 32 CPU cores dominates. Flagged as
potentially useful for downstream pymc Bayesian NBR if fit times become
inconvenient; see Aeneas-partition future work for more plausible GPU use.

---

## Decision 6 — Wall-time (updated from plan §6)

Updated compute envelope with doubled cell count (step + Gaussian) and tripled
CPL MC work:

- **Total cells:** 256 (128 × 2 shapes).
- **Effective MC work:** CPL cells (half) do 3× MC → ~2× total MC work vs
  single-k, single-shape baseline.
- **Single-core estimate:** ~9–10 h (2× from baseline 4.6 h).
- **Sapphire (32 cores):** ~20 min wall-time with safety margin to ~60 min if
  per-iteration estimates are 3× optimistic.
- **amd-tower fallback (16 cores):** ~40 min with safety margin to ~2 h.

Still comfortably overnight-feasible on sapphire.

---

## Decision 7 — `tempun` dependency (new, discovered during env reconcile)

**`tempun` 0.2.4 (PyPI latest, 2025-10 vintage) is numpy-2-incompatible.** It
imports `numpy.trapz` (removed in numpy 2.4) and eagerly imports `seaborn` at
module load. We removed tempun as a dependency.

**Substitution:** implement Uniform aoristic resampling directly in
`primitives.py::aoristic_resample` — ≤ 10 LOC of numpy. Mathematically equivalent
to tempun's Uniform sampling under Decision 4 aoristic choice. Attribution to
Kaše et al. preserved via source-comment citation.

**Upstream tracking:** GitHub issue #4 in this repo logs the tempun bug for
reporting to `sdam-au/tempun` maintainers.

**Consequence:** preregistration §3 wording requires amendment (tool citation →
method citation with reference to Kaše et al.'s Uniform aoristic approach).

---

## Decision 8 — Schema additions for exploratory replay

To support all post-hoc exploratory analyses (Decision 3 AIC-select, Decision 4
stratified-sampling, null-model comparison) without resimulation, the per-iteration
parquet schema is:

```
cell_id           : str    # unique per (level, bracket, n, null_model, shape)
level             : str    # empire | province | urban-area
bracket           : str    # a_50pc_50y | b_double_25y | c_20pc_25y | zero
shape             : str    # step | gaussian
n                 : int
null_model        : str    # exponential | cpl
cpl_k             : int    # 2, 3, 4 (NaN for exponential cells)
cpl_aic           : float  # for AIC-select reconstruction (NaN for exp)
iter              : int
detected          : bool
pval_global       : float
n_bins_outside    : int
null_residual_rms : float
province_counts   : dict[str,int]   # for stratified-sampling replay
city_counts       : dict[str,int]   # for stratified-sampling replay
seed_hex          : str
wall_ms          : int
```

For CPL cells, three rows per iteration (one per k). For exponential cells, one
row per iteration. Keeps the parquet wide-format and queryable.

Storage estimate: 128 × 1,000 × (1 exp + 3 cpl) = 512,000 rows × ~20 cols ≈ 50-80 MB.
Acceptable.

---

## Summary table — Shawn-approved final parameters

| Axis | Value |
|---|---|
| Subset levels | empire, province, urban-area |
| Effect-size brackets | a (50 %/50 y), b (2× / 25 y), c (20 %/25 y), zero |
| Effect shapes | **step + Gaussian** (both) |
| n sweeps | empire: {50 000}; province: {100…25 000} (8); urban: {25…2 500} (7) |
| Null models | exponential (primary), CPL-k=3 (secondary primary) |
| CPL k values stored | {2, 3, 4} (k=3 is reported-primary; {2,3,4} enables exploratory) |
| Sampling | bootstrap primary; stratified exploratory (post-hoc) |
| Iterations per cell | 1,000 |
| MC replicates per test | 1,000 |
| Detection criterion | *p* < 0.05, rate ≥ 0.80 |
| Reporting curves | 0.70, 0.80, 0.90 detection-rate gridlines |
| Total cells | 256 |
| Execution | sapphire via SSH + nohup |
| Seed | 20260425 |
| Tool stack | numpy, scipy, pandas, joblib (matplotlib for plots); **no tempun** |

---

## References

- `planning/preregistration-draft.md` — base protocol.
- `planning/preregistration-amendments-2026-04-25.md` — formal amendments arising
  from Decisions 1, 2, 3 (exploratory additions), 4, 7.
- `runs/2026-04-25-h1-simulation/plan.md` — plan agent's implementation plan
  (now superseded on points listed above; otherwise authoritative).
- GitHub issue #3 — Phase 2 reproducibility archival deferred task.
- GitHub issue #4 — tempun upstream numpy-2 compat notification.
