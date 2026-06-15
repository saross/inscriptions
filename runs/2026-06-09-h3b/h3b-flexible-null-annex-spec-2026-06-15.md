# H3b flexible-null robustness annex — build-ready spec (2026-06-15)

**Status:** DRAFT FOR PRE-LAUNCH SIGN-OFF. Nothing built or run until Shawn signs §9.
**Date:** 2026-06-15.
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief.
**Run dir:** `runs/2026-06-09-h3b/` (annex outputs under `outputs/flexnull/`).
**UK/Australian English; Oxford comma.**

---

## 0. What this document is

This is the spec for **part (a)** of the H3b flexible-null robustness annex —
D2's deferred work from the base draw-wise run
(`REPORT-drawwise-2026-06-15.md` §7; `DECISION-NEEDED-null-construction-2026-06-14.md`
Decision 2). The base run **accepted** the global Timpson-test saturation as an
honest large-*N* over-power finding and made the **probe-window P(deficit)** the
deliverable. This annex asks the deferred question:

> **Does a better-specified (more flexible) smooth null, and/or a de-powered
> significance criterion, de-saturate the GLOBAL test at all — and if so, only at
> the cost of absorbing the Antonine/Crisis events it is meant to detect?**

It is a **robustness/diagnostic** study. It **does not change the base H3b
deliverable** (probe-window P(deficit)) unless it finds a genuine sweet spot
(§6). Its primary output is a **go/no-go decision on part (b)** — the baorista
Bayesian-aoristic null — plus a reportable robustness result either way.

H3b is **exploratory** (prereg; Decision 15; OSF Amendment 04 §A5.6): every
reading here is descriptive. No confirmatory gate, no Holm decision rule.

**Part (b) — baorista — is NOT in this spec.** It is conditional on part (a)'s
outcome (§10) and gets its own spec + sign-off if warranted. Infra is already
installed (`runs/2026-05-03-baorista-install/`; R 4.4.3 + baorista 0.2.1 + NIMBLE
on sapphire, smoke-tested).

---

## 1. The scientific question, framed correctly

### 1.1 It is a trade-off curve, not a binary

The base run's *informative* null is **self-referential**: CPL-3 fit to the
observed (posterior-median) corrected count SPA (D1). A self-referential null
**trivially de-saturates in the high-flexibility limit** — as flexibility rises,
the null bends toward the observed curve, the residual shrinks to zero, the global
test stops firing — *but only because the null has absorbed the very
Antonine/Crisis dips we are trying to detect*. So "does a flexible null
de-saturate the global test?" is not a yes/no; the real question is whether there
is a **sweet-spot flexibility that de-saturates the global test while the
named-scope probe P(deficit) survives.**

**The deliverable of part (a) is therefore a 2-D readout** — global marginal-*p*
**and** named-scope probe P(deficit), traced across a flexibility axis — not a
single de-saturation flag. The 2-D readout makes an "event-absorption" failure
impossible to mistake for a "fix" (§6.2).

### 1.2 Two saturation mechanisms → two levers

| Mechanism | Description | Lever that targets it |
|---|---|---|
| **M1 — broad-shape misfit** | A null too rigid to track the epigraphic-habit hump leaves residual everywhere → saturates. Kills the **exponential** null (monotone; 77/80 empire bins out-of-envelope). | **Flexibility lever** (§4): wigglier smooth nulls can bend to the hump. |
| **M2 — bin-to-bin jaggedness at large *N*** | Even a null that tracks the broad hump can't track round-year spikes (e.g. the AD 77 feature) and sub-bin wiggle; at n_eff up to 151k the Poisson envelope is so tight that tiny wiggles read as "significant." Why CPL-3-fit-to-corrected sits at marginal-*p* ≤ 0.04 (near-edge), not exactly 0 like exp. | **Effective-*N* / reduced-significance lever** (§5): wider/simultaneous envelopes swallow the spikes. |

The two levers are **orthogonal** and both are run (Shawn's 2026-06-15 calls).

### 1.3 Why part (a) settles the baorista (part b) question

A featureless Bayesian growth-process null (baorista) absorbs **less** smooth
structure than a self-referential null at matched flexibility. So:

- If even an arbitrarily-flexible **self-referential** null cannot de-saturate the
  global test without eating the events, then baorista (which absorbs less) will
  not rescue the *global* test either — though it could still **sharpen the
  probes**, a separate, lower-priority benefit.
- If part (a) **does** find a sweet spot, a better-specified null genuinely helps,
  and baorista becomes worth building as the principled version.

This is the cheap-first logic made rigorous, and it is the explicit go/no-go in §6.

---

## 2. Decisions locked (Shawn, 2026-06-15) and defaults

| Topic | Decision | Authority |
|---|---|---|
| **Smooth-null families (flexibility lever)** | **CPL knot-sweep + penalised spline + GP** (all three). | Shawn 2026-06-15 |
| **Effective-*N* / reduced-significance lever** | **Both**: effective-*N* thinning ladder **and** a de-powered (simultaneous-coverage) global statistic. | Shawn 2026-06-15 |
| Null fit target | **Posterior-median corrected count SPA** (the base run's `cpl_target`; D1 self-referential null) — for **every** smoother, for comparability with the base run. | Base run D1; this spec |
| Flexibility axis | **Effective degrees of freedom (edf)** — CPL: `2k+1`; spline/GP: trace-of-smoother. All three families plotted on one axis. | This spec |
| MC envelope mechanism | **Poisson MC on the fitted mean** for every family (the existing `sample_null_spa` path). Only the fitted mean differs across families → directly comparable. | Reuse; this spec |
| Scope | **All 29 cc-refit units** + the prereg-named scopes (empire, latin-aggregate) highlighted. Cheap enough to run all. | This spec |
| Observed signal | The genuine-SPA **posterior** (8,000 draws/unit), evaluated draw-wise exactly as the base run. λ=1.0 primary; λ=1.2 coverage sensitivity carried. | Base run; Amdt 04 §A5.6 |
| Reproducibility anchor | At **k=3**, the CPL family must reproduce the base run's marginal-*p* and probe numbers **bit-for-bit** (regression guard, §7). | This spec |
| Status | **Exploratory**; all readings descriptive; no confirmatory gate. | Prereg; Decision 15 |

---

## 3. Inputs (all already on disk — no Stage-A re-run)

| Input | Source | Note |
|---|---|---|
| Genuine-SPA posterior draws | `runs/2026-06-13-cc-production-refit/outputs/posterior-draws/` (gitignored; local + sapphire) | 8,000×80 per unit; emitted by the base run's Stage A. **No re-run needed.** |
| `n_eff`, α median/CI | `runs/2026-06-13-cc-production-refit/outputs/refit-summary.json` | canonical refit; **not overwritten** |
| Per-unit raw intervals (`nb`, `na`) | `h2_lib` chain (as base run `assemble_units`) | for the exp cross-check fit only (CPL/spline/GP fit to the corrected curve) |
| Base-run engine | `runs/2026-06-09-h3b/code/h3b_drawwise.py` | envelope-build / draw-eval / probe / aggregate reused unchanged |

**No API spend. No sapphire. No Stage-A re-run.** Everything is local laptop compute.

---

## 4. The flexibility lever — three smooth nulls on one edf axis

All three fit the **posterior-median corrected count SPA** `m = median_d(g_d)·n_eff`
(80 bins) — the base run's `cpl_target`. Each returns a **fitted mean** array;
that mean is fed to the **existing Poisson MC envelope** (`sample_null_spa`-style:
`Poisson(fitted)`, `n_mc = 1000`, fixed seed). The only thing that differs across
families is the fitted mean, so the three are directly comparable.

### 4.1 CPL knot-sweep (the spine — near-zero new code)

`primitives.fit_null_cpl(m, BIN_CENTRES, k, n_restarts, seed)` for
**k ∈ {2, 3, 5, 7}** → edf = `2k+1` = {5, 7, 11, 15}. k=3 is the base-run anchor.

- `fit_null_cpl` is already generic in `k` (`n_params = 2k+1`); the "2–4" in its
  docstring is documentation of *tested* values only.
- **Build note:** k=5,7 (11/15 params) need more L-BFGS-B restarts than the default
  4 → set `n_restarts = 12` for k ≥ 5; **assert `converged`** and log AIC/RMS.

### 4.2 Penalised spline (Poisson P-spline; Eilers & Marx)

Cubic B-spline basis (≈15–20 evenly-spaced interior knots over −50…350) +
**second-order difference penalty**, fit by penalised Poisson IRLS (log link).
Smoothing parameter chosen to populate a **flexibility ladder** of target
edf ≈ {5, 10, 20} (so the spline traces the same edf axis as the CPL sweep rather
than collapsing to a single data-chosen point). edf = trace of the smoother (hat)
matrix. Implementation: hand-rolled B-spline (`scipy.interpolate.BSpline` basis) +
penalised IRLS — no new heavy dependency. (Fallback if IRLS is fiddly:
`statsmodels` GAM `BSplines` + Poisson; decide at build time, note which was used.)

### 4.3 Gaussian-process smooth (GP)

GP regression on `log(m + 0.5)` with an **RBF kernel** (`sklearn
GaussianProcessRegressor`), exponentiated to a mean → Poisson MC on top. Trace a
**length-scale ladder** giving edf ≈ {5, 10, 20} (short length-scale = wiggly =
more absorption), **plus** the marginal-likelihood-selected length-scale as the
"data-chosen flexibility" point. edf = trace of the GP smoother. sklearn is already
in the env; if absent, a hand-rolled RBF-kernel ridge is the fallback.

### 4.4 Exponential (degenerate baseline — carried for context)

The base run's exp null (forward-fit, monotone) is the **edf-minimal, M1-dominant**
anchor (77/80 empire bins out). Carried at one point on the axis for orientation;
not swept.

---

## 5. The effective-*N* / reduced-significance lever (both forms)

Run on a **fixed null** — the base **CPL-3** informative null — so the *N*/significance
lever is isolated from the flexibility lever.

### 5.1 Effective-*N* thinning ladder (targets M2 directly)

Rescale to N′ ∈ **{1500, 3000, 6000, 12000, 25000}**, each capped at the unit's
actual n_eff (skip grid points above it). For each N′:

- envelope built at the scaled mean `fitted · N′/n_eff` (`Poisson`), and
- the observed/draw counts scaled to N′,

then re-compute the global marginal-*p*. As N′ falls the Poisson envelope widens
(sd ∝ √N′), so M2 jaggedness de-saturates. **Report the N′ at which global *p*
crosses 0.05, per unit** (the named scopes — empire 151k, latin 101k — have the
most headroom). This isolates and quantifies the large-*N* over-power.

### 5.2 De-powered / reduced-significance global statistic (simultaneous envelope)

Replace the pointwise 95% envelope with a **simultaneous (global) 95% envelope**
— the standard fix for multiple-bin over-power (Myllymäki et al. 2017, *JRSS-B*
"Global envelope tests"; rcarbon `modelTest`'s simultaneous band). Calibrate the
band width from the **same** `n_mc` MC replicates so that 95% of null replicates
have **zero** bins outside the band (rank-based global envelope), then read the
global *p* off that simultaneous band. Under simultaneous coverage far fewer null
bins fall out, so the test is correctly *sized* across the 80 bins and only
de-saturates if the misfit is genuinely large. Same replicates → cheap (a
different summary on the existing MC draws). Whether it actually de-saturates here
is itself an empirical result the annex reports.

*(Optional secondary, only if trivially cheap on the same replicates: a
summed-standardised-residual global *p* as a second de-powered summary. Not
required for the readout.)*

---

## 6. Readout and the baorista go/no-go decision rule (pre-committed)

### 6.1 The primary 2-D readout

For each **family × edf level** (flexibility lever) and each **N′** (effective-*N*
lever), at the **named scopes** (empire, latin) and all 29 units, record:

- **global marginal-*p*** — the de-saturation axis;
- **named-scope probe P(deficit)** (Antonine + Crisis) — the event-preservation axis.

Plot/tabulate **global *p* vs edf** and **probe P(deficit) vs edf** overlaid (one
panel per named scope), and the **thinning curve** (global *p* vs N′).

### 6.2 The event-absorption guard

Probe P(deficit) is reported at **every** flexibility/N′ level *precisely so a
de-saturation can never be mistaken for a fix when it is actually event-absorption.*

### 6.3 The pre-committed decision rule (descriptive; H3b is exploratory)

- **Sweet spot exists** — ∃ an edf where, at the named scopes, global *p* > 0.05
  **AND** probe P(deficit) ≥ 0.8 → a better-specified null genuinely de-saturates
  without eating the events → **GO on baorista (part b)** as the principled
  version; the base global readout may be revisited.
- **No sweet spot** — global *p* clears 0.05 only once probe P(deficit) has
  collapsed below ~0.5 → flexibility de-saturates *only* by absorbing the events →
  **probe-window readout confirmed as THE deliverable**; baorista will not rescue
  the global test → **NO-GO on baorista-for-global**; baorista demoted to an
  optional, lower-priority *probe-sharpening* cross-check.
- **Effective-*N* finding (independent):** if thinning de-saturates the global
  test at an N′ well below the actual n_eff, that is positive evidence the
  saturation is large-*N* over-power (M2) rather than fundamental misfit — a
  reportable robustness result on its own, strengthening "report at effective-*N*
  or report probe windows," whichever way the flexibility lever lands.

The thresholds (0.05; P(deficit) ≥ 0.8 / < 0.5) are pre-committed here as the
**readout convention**, not a confirmatory gate.

---

## 7. Architecture — reuse-only, one new module + driver

`runs/2026-06-09-h3b/code/`:

- **`h3b_flexnull.py`** — imports `h3b_drawwise as E` and **reuses unchanged**:
  `eval_draws`, `aggregate`, `probe_window`, `inflate_draws`, `window_bin_indices`,
  `load_draws_normalised`, `assemble_units`. Adds only:
  - `fit_null_spline(m, ...) -> {"fitted", "edf", "family"}` (§4.2);
  - `fit_null_gp(m, ...) -> {"fitted", "edf", "family"}` (§4.3);
  - a generalised `build_envelope_from_mean(fitted, n_eff, rng, n_mc)` that routes
    **any** fitted mean (cpl-k / spline / gp) through the existing Poisson MC
    envelope (factoring the Poisson branch out of the current `build_envelope`;
    exp keeps its forward path);
  - `edf_cpl(k)` / `edf_from_smoother(hat)` helpers;
  - `thin_envelope(fitted, n_eff, n_prime, rng)` (§5.1);
  - `simultaneous_global_p(mc, obs_counts)` — the rank-based global envelope
    statistic (§5.2).
- **`run_h3b_flexnull.py`** — driver over 29 units × {cpl k∈{2,3,5,7}, spline edf-
  ladder, gp edf-ladder} (flexibility lever) + the CPL-3 thinning ladder +
  simultaneous-band statistic (effective-*N* lever). Writes §8 outputs + DRAFT
  annex report. Seeds reuse the base convention (`MASTER_SEED = 20260609` + disjoint
  per-family offsets) so the k=3 CPL anchor reproduces the base run.
- **Regression guard (in the driver's self-test):** assert the k=3 CPL family
  reproduces `outputs/drawwise/deviations.json`'s CPL marginal-*p* and named-scope
  probe P(deficit) for empire + latin **bit-for-bit** before the sweep runs. If it
  drifts, halt (it would mean the reuse diverged).

**Compute:** permutation-only, no MCMC. ~4–6× the base CPL cost (flexibility) +
a ~5-point N ladder (effective-*N*); total well under an hour on the laptop. GP
fits are O(80³) per unit — trivial.

---

## 8. Outputs (`runs/2026-06-09-h3b/outputs/flexnull/`)

- `flexnull-sweep.json` — per (unit × family × edf-level): global marginal-*p*,
  P(deviation), per-draw spread, named-window P(deficit)/P(dev)/departure (λ=1.0
  + λ=1.2), edf, fit diagnostics (AIC/RMS/converged/length-scale), seed.
- `flexnull-table.csv` — flat tabulation for the report.
- `effn-thinning.json` — per (unit × N′): global marginal-*p* under CPL-3.
- `depowered-stat.json` — per unit: pointwise vs simultaneous-band global *p*.
- `ANNEX-REPORT.md` — DRAFT-FOR-REVIEW: the 2-D trade-off readout (figures +
  table), the §6.3 go/no-go on baorista, the effective-*N* result, caveats.
- `figures/` — global-*p* vs edf and probe-P(deficit) vs edf overlays (empire +
  latin); thinning curves; pointwise-vs-simultaneous-band illustration.

---

## 9. Pre-launch gate — what Shawn is signing off

1. **The design above** — three smoothers on one edf axis (CPL sweep + P-spline +
   GP), both effective-*N* forms (thinning ladder + simultaneous-band statistic),
   self-referential fit target, all 29 units + named scopes, the §6.3 decision rule.
2. **Local-only, no API spend, no sapphire, no Stage-A re-run** (draws already on
   disk). `refit-summary.json` and the base `deviations.json` are **not** overwritten;
   annex writes only under `outputs/flexnull/`.
3. **Reuse-only** — no reimplementation of the fit, sampler, envelope, or draw-eval;
   the k=3 CPL regression guard enforces faithfulness to the base run.
4. **Flow:** build `h3b_flexnull.py` + driver → run → DRAFT `ANNEX-REPORT.md`
   returns to Shawn. **Nothing is lodged or paper-bound;** the annex stays draft and
   the base deliverable is unchanged unless §6.3 finds a sweet spot.

Standing rules honoured: spec-before-launch; no silent parameter negotiation; commit
before the pipeline stage; exploratory framing preserved.

**Open build-time choices (decided at implementation, logged in the module
docstring, not blocking sign-off):** P-spline via hand-rolled IRLS vs `statsmodels`
GAM; exact interior-knot count for the spline basis; GP fallback if `sklearn`
absent. None changes the design or the readout.

---

## 10. Part (b) — baorista (conditional; own spec if triggered)

Run **only** per §6.3:

- **GO** (sweet spot found) → baorista as the principled flexible null; its own
  spec + sign-off; remaining work = design (posterior credible band **as** the null
  envelope) + Rscript→CSV bridge + **full-LIRE-width revalidation** (the 2026-05-03
  smoke capped aoristic widths at 100 y, not the realistic 300 y) + run. ~2–4 days;
  infra installed (`runs/2026-05-03-baorista-install/`).
- **NO-GO** (no sweet spot) → baorista demoted to an optional probe-sharpening
  cross-check, lower priority; the global test stays reported as a saturated gate
  and the probe-window P(deficit) stays THE H3b deliverable.

---

## 11. Cross-references

- Base run: `REPORT-drawwise-2026-06-15.md`; engine `code/h3b_drawwise.py`.
- D2 deferral + saturation diagnosis: `DECISION-NEEDED-null-construction-2026-06-14.md`.
- Base implementation spec: `h3b-implementation-spec-2026-06-14.md`.
- Authority (exploratory recast; uncertainty propagation): OSF Amendment 04 §§A5.5–A5.6
  (`planning/osf-amendment-2026-06-14-cross-classified-remediation.md`; tag
  `osf-amendment-04-2026-06-14` → `61c954c`).
- Production draws: `runs/2026-06-13-cc-production-refit/outputs/posterior-draws/`.
- baorista infra: `runs/2026-05-03-baorista-install/`.
- Method refs: Timpson et al. 2014 (envelope); Myllymäki et al. 2017 *JRSS-B*
  (global/simultaneous envelope test); Eilers & Marx (P-splines); Crema & Bevan
  rcarbon (`modelTest` simultaneous band).
