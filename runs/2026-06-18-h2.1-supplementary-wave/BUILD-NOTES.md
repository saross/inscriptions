# BUILD-NOTES — H2.1 supplementary-wave production driver (post-audit)

- **Run dir:** `runs/2026-06-18-h2.1-supplementary-wave/`
- **Driver files:** `code/run_supp_production.py`, `code/supp_production_lib.py`
- **Pre-audit baseline:** commit `b4ee414`
  (`build(supp-wave): production driver for ready supplementaries (pre-audit)`)
- **Author / Date:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
  2026-06-18. UK/Australian English; Oxford comma.

These notes document the audit fixes applied to the **production driver only** (the
two files above; no lodged/shared module — `supp_lib`, `joint_lib`, `refit_lib`,
`h2_lib`, `cell_lib` — was touched). The driver is **BUILD-ONLY** and will be
**re-audited before it is ever run** (standing rule). Nothing has been run.

## C1 (CRITICAL) — cross-family PSIS-LOO removed (methodologically invalid)

### The defect

The pre-audit driver built a "model comparison" deliverable around an `az.compare`
PSIS-LOO across the three families (primary, Dirichlet-multinomial, negative-binomial),
backed by a `_pooled_loglik_tree` helper that **concatenated each model's three
observed nodes' pointwise log-likelihoods onto one shared `obs` axis** and handed the
result to `az.compare`.

This is **invalid**. Under the adopted cross-classified likelihood
(`joint_lib.build_model_cross_classified`):

- the **primary** and the **Dirichlet-multinomial** emit a **JOINT-multinomial**
  pointwise log-likelihood — the two subset multinomials (`y_al_obs`, `y_non_obs`)
  each score **one** log-likelihood point, plus the Binomial classification node
  (`k_obs`): **≈ 3 points per unit**;
- the **negative-binomial** is **per-bin** — each of the `N_BINS` bins in each subset
  is an independent observation: **1 + N_BINS + N_BINS ≈ 161 points per unit**.

PSIS-LOO (and `az.compare`) estimate the expected log-pointwise-predictive-density by
leave-**one-out** over the pointwise log-likelihood. Two models whose pointwise
log-likelihoods live on **differently-shaped observation spaces** (3 points vs 161
points; a joint-multinomial point is not the same observable as a single per-bin
NegBin count) are **not comparable** by LOO — the ELPD estimates are on incommensurable
supports. Forcing a shared `obs` axis (as `_pooled_loglik_tree` did) does not fix this;
it manufactures a comparison between quantities that are not the same. In practice
`az.compare` errors into a `?` for every unit, but even where it returned a number the
number would be meaningless. **You cannot LOO-compare a multinomial against a per-bin
NegBin on differently-shaped data.**

### The fix

Removed the `az.compare` call **and** the `_pooled_loglik_tree` cross-family pooling
helper entirely. The model-comparison deliverable now discharges exactly what the
prereg asks for ("reported alongside for model-comparison cross-checks", C5/C6):

1. **α median + 95 % CI side-by-side** across primary / DM / NB. (Already present and
   audited-correct; kept. The primary α is the **lodged** value from
   `runs/2026-06-13-cc-production-refit/outputs/refit-summary.json`, reused, not
   re-run.) → the substantive question: **does the overdispersed family move α?**
2. **Multinomial posterior-predictive dispersion check** on the primary (already
   present, audited sound; kept). The mean squared Pearson residual vs the multinomial
   expectation, averaged over the posterior, per subset: **≈ 1 ⇒ the multinomial is
   adequate** (overdispersion NOT warranted); **> 1 ⇒ DM/NB preferred.** This is the
   prereg's stated DM/NB trigger (l.192) and is the **adjudicator** of whether the
   overdispersed families are warranted at all.
3. **Each family's OWN WAIC, reported within-family only** (`_within_family_waic`):
   per observed node (`k_obs`, `y_al_obs`, `y_non_obs`), `elpd_waic` + `p_waic`,
   computed independently on that node. **Descriptive context only — never
   cross-compared across families.** Lands in the per-unit JSON, not the headline
   table.

**The model-comparison VERDICT** is therefore: (i) does the family move α?
(side-by-side `|Δα|`) **+** (ii) is overdispersion warranted? (primary dispersion ratio
vs 1) — **not** any cross-family information criterion. This is encoded in the per-unit
`model_comparison.alpha_verdict` block (`delta_alpha_*_vs_primary`,
`primary_dispersion_ratio_max`, `overdispersion_warranted`) and surfaced in
`model-comparison.md`. The driver re-fits the primary **only** for the dispersion check
and its within-family WAIC (neither persisted by the lodged refit), seeded with
`REFIT_BASE_SEED + unit_index` so it reproduces the lodged posterior to MCMC noise; the
**reported** primary α is still the lodged value.

The within-family WAIC helper is best-effort (never raises) and carries an explicit
docstring + JSON `note` stating cross-family comparison is inapplicable, so the
distinction cannot be lost downstream.

## C2 — DM κ prior σ set to S_KAPPA = 5000 (was 1e3)

`S_KAPPA` is the σ of the DM concentration prior `κ ~ HalfNormal(σ = S_KAPPA)` (κ is
**sampled**, free; only its prior σ is pinned). The pilot DM fit returned **κ ≈ 5,800**
(a data-dominated posterior). The earlier `σ = 1000` placed the prior bulk well below
that and exerted a **downward pull** on κ. `σ = 5000` centres the weakly-informative
prior near the pilot-fitted value without that pull, while remaining weakly informative
across the prereg's intended κ ∈ ~[10, 1e4] range (§3.3).

**FLAGGED FOR FINAL HUMAN CONFIRM before the run** — this is a one-line constant
(`run_supp_production.py`, `S_KAPPA = 5000`) and a deliberate departure from the
pre-audit driver's brief-pin of `1e3`. It is surfaced in the `S_KAPPA` comment, the
module docstring, and the `model-comparison.md` footnote.

## M1 (caveat only — computation UNCHANGED) — H2.4 drops year-precise rows

The H2.4 stratum SPAs are built with `h2_lib.aoristic_spa`, which drops rows with
`width = na − nb ≤ 0` — i.e. the **year-precise rows** (`na == nb`, a zero-width
interval). This is **CONSISTENT** with how the lodged primary `p_gen` was fit (the same
drop), so the genuine-stratum-vs-`p_gen` comparison is valid and apples-to-apples.
**But** it means the genuine-classed stratum **under-represents exactly the date-honest
year-precise inscriptions** the H2.4 internal-consistency check is most about.

**Fix (caveat only):** `stratified_unit` now reports, per stratum,
`n_year_precise_dropped` (the count of `na == nb` rows in the stratum that
`h2_lib.aoristic_spa` silently drops), plus an `m1_caveat` string. `h2.4-stratified.md`
carries a prominent caveat block and a `genuine drop` column. **The SPA / band
computation is NOT changed** — changing it would break the consistency with the lodged
primary and invalidate the comparison.

## M2 — C11 output-level r convention mismatch fixed

### The defect

The C11 **output-level** Pearson r compared:

- a **trapezoidal refit's** `p_gen`, where the trapezoidal subset SPAs were built with
  `SP.trapezoidal_spa_on_h2_grid` — the **2026-05-17 convention**: width = `na − nb + 1`
  (inclusive-Roman), half-open interval `[nb, na+1)`, **unclipped** to the envelope,
  width-≤-0 rows **kept**; against
- the **lodged uniform refit's** `p_gen` — fit on `h2_lib.aoristic_spa`: width =
  `na − nb`, interval `[nb, na]`, **clipped** to `[ENV_START, ENV_END]`, width-≤-0 rows
  **dropped**.

So a sub-0.95 output-level r could be a **width/clip-convention artefact** rather than
the trapezoidal-**shape** effect the C11 sensitivity is supposed to isolate.

### The fix

Added `SP.trapezoidal_spa_h2_convention` — the lodged 2026-05-17 trapezoidal **shape**
(`empirical_spa_shape.trapezoidal_aoristic_spa`, imported, original untouched) computed
on the **exact `h2_lib.aoristic_spa` width/clip/drop convention**: clip `nb`/`na` to the
envelope, drop `width ≤ 0` (verbatim the `valid = (width > 0) & (na_c > nb_c)` mask),
integrate the trapezoid over `[nb, na]` with length `na − nb` (achieved by passing
`not_after = na − 1` to the lodged builder, whose `interval_hi = not_after + 1` is
hardcoded). The C11 **output-level** refit arm (`trapezoidal_unit`) now uses this
convention-matched builder, so the output-level r isolates the **shape** effect.

The C11 **input-level** r is left untouched — it already correlates a trapezoid against
a uniform SPA that are **both** built with the 2026-05-17 convention
(`SP.trapezoidal_spa_on_h2_grid` vs `SP.uniform_spa_2026_05_17`), so the only difference
there is the mass shape (correct).

## Post-audit run command + scope

**Items run (7):** C5, C6 (model comparison — α side-by-side + dispersion + within-family
WAIC), C11 (trapezoidal sensitivity), C13/H2.2 (boundary-step reduction), C14/H2.3
(threshold convergence), C15/H2.4 (stratified-by-class), C16 (α descriptive read-off,
folded into `REPORT.md`). All across the **29 production units**
(`refit_lib.enumerate_refit_units()`).

**C10 (aoristic-MC) is EXCLUDED** — held pending a separate validity test
(`runs/2026-06-18-c10-validity-test/`), out of scope for this driver.

**Run command (sapphire; only after re-audit + the C2 final human confirm):**

```bash
PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
    uv run python code/run_supp_production.py --n-jobs 10
```

(Run from `~/Code/inscriptions/runs/2026-06-18-h2.1-supplementary-wave/`. Resumable at
unit granularity; `--write-only` re-assembles the Markdown deliverables from existing
per-unit JSONs without fitting.)

## What was NOT touched

- No lodged/shared module (`supp_lib`, `joint_lib`, `refit_lib`, `h2_lib`, `cell_lib`,
  `empirical_spa_shape`) was modified — all are imported, never edited.
- Nothing was run (no fit, no MCMC, no SSH). `py_compile` was used to syntax-check both
  driver files (allowed).
