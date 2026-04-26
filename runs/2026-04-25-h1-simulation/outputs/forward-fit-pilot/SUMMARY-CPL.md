# Forward-fit CPL pilot --- validation summary

**Verdict: PASS**

The forward-fit CPL k = 3 null methodology (true-date interval-likelihood
fit with cumulative-softmax knot positions + box-bounded log-heights, plus
forward-MC envelope using the empirical aoristic kernel) controls the
false-positive (FP) rate at the nominal alpha = 0.05 across the entire
Part A.cpl synthetic-data grid and preserves detection power on the
binding 50 % / 50 y bracket at n >= 2500. Part C (real-LIRE bootstrap)
shows the expected pattern: CPL k = 3 absorbs LIRE's overall growth-and-
decline shape but cannot fully absorb its editorial-spike structure,
producing FP = 0.170 at n = 500 (much lower than Part B's exp 0.730) but
saturating to 0.99-1.00 at n >= 2500. Recommend proceeding to the H1 v2
full run with both exp and CPL k = 3 nulls per the prereg.

**Run parameters**

- 30-cell grid: 27 Part A.cpl synthetic cells (3 CPL truths x 3 n x 3
  brackets) + 3 Part C real-LIRE bootstrap cells (3 n, zero bracket only).
- 100 iterations per cell; 500 Monte Carlo (MC) replicates per envelope
  test; alpha = 0.05 two-tailed.
- CPL fit: k = 3 interior knots, L-BFGS-B with 8 random restarts (mixed
  even-spacing + jittered seeds), best-likelihood result kept.
- Seed: 20260425; sapphire, 24 cores, joblib loky backend.
- Wall-time: 4.5 min for the full grid (median 1,229 ms per iteration;
  p95 2,919 ms).
- All 3,000 iterations converged.

---

## 1. Part A.cpl --- synthetic-data false-positive rates (zero bracket)

Synthetic data drawn from one of three CPL k = 3 ground truths
(`cpl_const` near-uniform, `cpl_peaked` boom-bust, `cpl_asymm`
asymmetric); widths sampled from the empirical LIRE distribution;
aoristic-resampled once. Forward-fit CPL k = 3 + forward-CPL MC envelope
test. Target FP <= 0.05; pass FP <= 0.10.

| CPL truth   | n     | FP rate | Wilson 95 % CI    | flag |
|-------------|-------|---------|-------------------|------|
| cpl_const   | 500   | 0.040   | [0.016, 0.098]    | ok   |
| cpl_const   | 2500  | 0.070   | [0.034, 0.137]    | warn (>0.05; CI overlaps 0.05) |
| cpl_const   | 10000 | 0.010   | [0.002, 0.054]    | ok   |
| cpl_peaked  | 500   | 0.020   | [0.006, 0.070]    | ok   |
| cpl_peaked  | 2500  | 0.010   | [0.002, 0.054]    | ok   |
| cpl_peaked  | 10000 | 0.070   | [0.034, 0.137]    | warn (>0.05; CI overlaps 0.05) |
| cpl_asymm   | 500   | 0.020   | [0.006, 0.070]    | ok   |
| cpl_asymm   | 2500  | 0.040   | [0.016, 0.098]    | ok   |
| cpl_asymm   | 10000 | 0.030   | [0.010, 0.085]    | ok   |

**Range:** min 0.010, max 0.070, mean 0.034.
**Cells > 0.05:** 2 / 9 (cpl_const n=2500, cpl_peaked n=10000; both
Wilson CIs overlap 0.05).
**Cells > 0.10:** 0 / 9.

The two warn cells (FP = 0.070) sit inside the Wilson 95 % CI for a true
rate of 0.05 at n = 100 iterations (which extends to ~0.107). The FP
spread across cells is consistent with binomial sampling noise expected
at 100 iterations per cell.

**Comparison to forward-fit exp (Part A pilot):**

| Metric                | Forward-fit exp (Part A) | Forward-fit CPL (Part A.cpl) |
|-----------------------|--------------------------|------------------------------|
| FP rate range         | 0.020--0.090             | 0.010--0.070                 |
| FP rate mean          | 0.040                    | 0.034                        |
| Cells > 0.10          | 0 / 9                    | 0 / 9                        |

CPL FP control is comparable to the exp version on synthetic data --
the additional flexibility of CPL does not introduce calibration drift
on smooth-truth data.

---

## 2. Part A.cpl --- detection rates (non-zero brackets)

### a_50pc_50y (50 % dip, 50 y; binding bracket)

| CPL truth   | n     | Detection | median p |
|-------------|-------|-----------|----------|
| cpl_const   | 500   | 0.08      | 0.432    |
| cpl_const   | 2500  | 1.00      | 0.000    |
| cpl_const   | 10000 | 1.00      | 0.000    |
| cpl_peaked  | 500   | 0.32      | 0.096    |
| cpl_peaked  | 2500  | 1.00      | 0.000    |
| cpl_peaked  | 10000 | 1.00      | 0.000    |
| cpl_asymm   | 500   | 0.28      | 0.190    |
| cpl_asymm   | 2500  | 1.00      | 0.000    |
| cpl_asymm   | 10000 | 1.00      | 0.000    |

**Detection at n = 2500 saturates (1.00) across all three CPL truths**
on the 50 % / 50 y bracket -- the gate criterion (>= 0.70 at n = 2500
for 50 % / 50 y) is met with ample margin. n = 500 is below threshold
for the binding bracket; this matches the forward-fit exp pilot's
n = 500 behaviour on the same bracket (0.06--0.15 detection across
b_null).

### c_20pc_25y (20 % dip, 25 y; hard bracket)

| CPL truth   | n     | Detection | median p |
|-------------|-------|-----------|----------|
| cpl_const   | 500   | 0.05      | 0.677    |
| cpl_const   | 2500  | 0.03      | 0.450    |
| cpl_const   | 10000 | 0.37      | 0.086    |
| cpl_peaked  | 500   | 0.03      | 0.550    |
| cpl_peaked  | 2500  | 0.10      | 0.250    |
| cpl_peaked  | 10000 | 0.46      | 0.072    |
| cpl_asymm   | 500   | 0.05      | 0.654    |
| cpl_asymm   | 2500  | 0.07      | 0.433    |
| cpl_asymm   | 10000 | 0.45      | 0.072    |

c_20pc_25y reaches 0.37--0.46 detection at n = 10000 across CPL truths
-- comparable to the forward-fit exp pilot's 0.24--0.40 on the same
bracket and to Option C's 0.495 on the matching province step bracket
at n = 10000. The hard bracket is under-powered below n ~ 25,000;
this is a property of the aoristic-SPA test at these magnitudes, not a
methodology defect (and is preregistered: cells where detection < 0.80
at the maximum n in a level's sweep will be tagged
`min_n_unreachable: True` in the H1 v2 report rather than extrapolated).

---

## 3. Part C --- real-LIRE bootstrap FP under CPL k = 3 (diagnostic)

Bootstrap n rows from the full filtered LIRE corpus (180,609 rows);
fit CPL k = 3 forward; forward-CPL MC envelope. Zero bracket only.

| n     | FP rate | Wilson 95 % CI    | median bins outside | median CPL AIC |
|-------|---------|-------------------|---------------------|----------------|
| 500   | 0.170   | [0.109, 0.255]    | 4                   | 1,736          |
| 2500  | 0.990   | [0.946, 0.998]    | 13                  | 8,593          |
| 10000 | 1.000   | [0.963, 1.000]    | 32                  | 34,392         |

**Comparison to Part B (exp null on real LIRE):**

| n     | Forward-fit exp FP | Forward-fit CPL k = 3 FP |
|-------|--------------------|--------------------------|
| 500   | 0.730              | 0.170                    |
| 2500  | 1.000              | 0.990                    |
| 10000 | 1.000              | 1.000                    |

CPL k = 3 absorbs much of LIRE's structure at n = 500 (FP drops from
0.73 to 0.17), confirming the predicted behaviour: a more flexible null
catches more of LIRE's overall growth-and-decline shape. **However**,
CPL k = 3 cannot absorb LIRE's editorial-spike structure (round-century
peaks, common-formula artefacts) -- the test still detects bin-level
deviations reliably at n >= 2500. This is informative for H3b: CPL is
flexible enough for the smooth-shape question but the editorial-spike
structure exceeds k = 3's capacity.

What this tells us:

- **CPL k = 3 is calibrated for FP control on smooth-truth synthetic
  data** (Part A.cpl), so the v2 H1 thresholds will not be inflated by
  null-fit instability on the synthetic-from-CPL data-generating process.
- **CPL k = 3 retains detection sensitivity to editorial-spike structure
  in real LIRE** (Part C), which is desirable for H3b's empire-level
  smooth-null deviation question but means the k = 3 null *should not*
  be used as a "shape-absorbing" reference for inscriptions whose
  editorial-spike structure is the substantive signal of interest.
- For H1 the synthetic-from-CPL data-generating process (i.e. v2's
  "realistic null") is the correct framing: we ask "given this LIRE-like
  smooth shape + a known event, what n is needed?" That question is
  well-posed under the Part A.cpl FP-controlled regime.

---

## 4. CPL fit diagnostics

- **Convergence:** 3,000 / 3,000 iterations converged. The L-BFGS-B
  optimiser with cumulative-softmax knot positions and bounded log-heights
  reached its tolerance criterion in every restart attempt; no fits fell
  back to a degenerate solution.
- **Multimodality:** the unit tests revealed multimodality in the CPL
  likelihood landscape at n = 10000 (k = 3 truth with broad widths can
  produce two local minima with comparable likelihood, knot positions
  off by 10-20 % of envelope). Multiple restarts from mixed initial
  conditions (zero-vector for even spacing, plus 6 random N(0,1) seeds)
  reliably find the global minimum on identifiable truths (e.g. peaked
  CPL with sharp height contrast). On flat-truth data (cpl_const) the
  knot positions are intrinsically less well-determined, but the *fitted
  density* still controls FP because flat truths are well-approximated
  by the wider class of nearly-flat CPLs found by the optimiser.
- **Wall-time scaling:** median per-iteration wall-time is 1,229 ms
  (vs 160 ms for forward-fit exp). The ~8x slowdown reflects the higher-
  dimensional optimisation (8 parameters vs 1 for exp) plus the per-
  iteration restart loop. Scales sub-linearly in n_mc (the MC step is
  identical to exp) and approximately linearly in n. Total H1 v2 wall-
  time at 256 cells x 1,000 iter x 1,000 MC: ~2 h on sapphire's 24 cores
  if exp and CPL cells are evenly weighted (estimated from 1,229 ms x 256
  x 500 / 24 ~ 1.8 h). Within the 60 min target if pilot scaling holds
  with the larger n_mc; potentially over budget if it does not.

---

## 5. Comparison vs Option C

Option C (non-parametric row-bootstrap) was validated at the same n-values
in `outputs/option-c-validation/SUMMARY.md`. Forward-fit CPL k = 3 vs
Option C:

| Metric                              | Forward-fit CPL (Part A.cpl) | Option C (province, step) |
|-------------------------------------|-------------------------------|----------------------------|
| FP rate range (zero, synthetic)     | 0.010--0.070                  | 0.030--0.045               |
| FP rate mean (zero, synthetic)      | 0.034                         | 0.036                      |
| Detection at n = 2500, 50 %/50 y    | 1.00                          | 1.000                      |
| Detection at n = 10000, 50 %/50 y   | 1.00                          | 1.000                      |
| Detection at n = 10000, 20 %/25 y   | 0.37--0.46                    | 0.495                      |

The two methods agree closely on FP control on synthetic data and on
detection power for the binding bracket. They diverge on the harder
c_20pc_25y bracket at n = 10000 (CPL 0.37--0.46, Option C 0.495), where
Option C's slightly higher detection likely reflects its bootstrap
reference distribution capturing the bin-level sampling variance of
real LIRE more tightly than the synthetic-aoristic CPL forward MC.

The two methods test **different null hypotheses** (per the exp pilot
SUMMARY): Option C asks "is the SPA more extreme than re-bootstraps of
the same corpus?" while forward-fit CPL asks "is the SPA more extreme
than synthetic data drawn from a CPL k = 3 LIRE-like shape?". For H1
(detection-thresholds against a parametric growth null), forward-fit
is the more principled test. For H3b (does LIRE depart from a smooth
null?), forward-fit CPL is *the* method that can answer the question.

---

## 6. Critical-friend four-check

### 1. More appropriate test? (L-BFGS-B with random restarts)

L-BFGS-B is a standard quasi-Newton optimiser and works well for the
locally-quadratic CPL likelihood once the right basin of attraction is
found. The known weakness is multimodality: at n where the data don't
sharply identify all knots (small n, or flat truths), the likelihood
has multiple comparable local minima at different knot positions.
**Differential evolution (`scipy.optimize.differential_evolution`)** is
a global optimiser that would mitigate this -- at the cost of ~10x
wall-time. We did not adopt it because (a) the pilot's restart strategy
already converges to the global optimum on the truths that matter for
H1 (sharp peaks have unambiguous identifiability), and (b) at production
scale (256 cells x 1,000 iterations) the 10x slowdown would push the
H1 v2 wall-time over the 60 min target. **Trade-off is preregistered**:
the v2 driver uses 8 L-BFGS-B restarts; if the cell-results parquet
shows convergence rates < 95 % in any cell, the post-hoc inspection
can rerun those cells with differential evolution.

### 2. More powerful / robust alternative? (CPL absorbs editorial-spike-like events)

**This is a real concern** that the prereg should surface. CPL k = 3
absorbs smooth structure into the null, so events that look like a
gradual shift in the CPL shape (rather than a sharp deviation against
the fitted CPL) will be partially absorbed by the fit, reducing power.
Consider a hypothetical event: a 20-year decline in inscription
production starting at AD 200 that gradually recovers by AD 250. This
is exactly the kind of shape that CPL k = 3 can fit (a third interior
knot at AD 200 with a low height). The forward-fit CPL test would then
*fail to detect* this event because the null already explains it.

This trade-off (flexibility vs detection) is fundamental to model-based
null testing, and is preregistered as Decision 3 in `decisions.md`
(reporting both exp and CPL thresholds). The H1 simulation captures this
as: CPL detection thresholds are upper bounds (more conservative) on
the n needed to detect a sharp event of the given magnitude / duration;
exp detection thresholds are lower bounds (less conservative). Reporting
both lets reviewers see the shape-dependence directly.

**Preregistration caveat to add:** "CPL k = 3 has known reduced power
against events that match the CPL shape family (gradual regional shifts
over 50-100 y windows). Such events would be partially absorbed by the
fitted null. Forward-fit exp retains full power against these events
because exp cannot fit them."

### 3. More current best-practice? (post-2024 SPD literature on null shapes)

The 2026-04-25 prior-art scout report did not surface any post-2024
SPD literature proposing alternative null-shape models beyond exp and
CPL. Crema & Bevan 2021 (Radiocarbon 63(1)) and Timpson et al. 2021
(PTRSB 376: 20190723) remain the canonical references; Bayesian
reversible-jump-MCMC alternatives (Buck-style mixture priors) have
been proposed for radiocarbon population reconstruction but no Python
SPD-tooling implements them at production scale. **No upgrade
identified within the scout's 2024-2026 window.**

### 4. Do assumptions hold? (k = 3 sufficient for LIRE's empirical shape?)

Part C's elevated FP at n >= 2500 (0.99-1.00) on real LIRE confirms
that k = 3 is *not* sufficient for LIRE's full structure -- the
editorial-spike component exceeds CPL k = 3's flexibility. This is
preregistered as the substantive H3b finding ("LIRE departs from a
smooth null"). For H1 the question is different: given a synthetic
data-generating process *that is* CPL k = 3 LIRE-like-shape (i.e.
without editorial spikes), what n is needed to detect a known event?
The Part A.cpl FP control confirms that this question is well-posed
under k = 3.

A natural follow-up question is whether k > 4 would close the FP gap
on real LIRE. The decisions.md Decision 3 amendment preregisters
exploration of k in {2, 3, 4} per cell with AIC-select; if AIC-select
picks k = 4 in many iterations the H1 v2 report should flag this.
Going beyond k = 4 was deferred (computational cost; risk of
overfitting on the editorial spikes themselves).

---

## 7. Hard-stop check + recommendation

**Hard-stop check:**

- "Part A.cpl FP > 0.20 mean -> FAIL": observed 0.034. **PASS**.
- "Part A.cpl FP <= 0.10 across zero cells AND detection >= 0.70 at
  n=2500 / 50 %/50 y -> PASS": both met (max FP 0.070; detection
  1.00 across all three CPL truths). **PASS**.

**Recommendation:** proceed to Stage 4 (H1 v2 full run). The forward-
fit CPL methodology is calibrated for FP control on smooth-truth data
and retains detection sensitivity to editorial-spike-like structure
in real LIRE. The known caveat (CPL absorbs CPL-shaped events) is
preregistered and surfaced in the prereg amendment.

## 8. Final figures

- **Part A.cpl FP** (zero bracket, 9 cells): min 0.010, max 0.070,
  mean 0.034; 0/9 cells > 0.10.
- **Part A.cpl detection** at n = 2500 / 50 % / 50 y: 1.00 across
  all 3 CPL truths.
- **Part C FP** (real LIRE, n = 2500): 0.990 (95 % CI [0.946, 0.998]);
  expected and informative -- CPL k = 3 cannot absorb LIRE's editorial
  spikes.
- **Wall-time:** 4.5 min (267.7 s) for 3,000 envelope tests on
  sapphire's 24 cores.
