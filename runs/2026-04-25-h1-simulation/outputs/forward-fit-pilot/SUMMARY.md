# Forward-fit exponential pilot --- validation summary

**Verdict: PASS**

The forward-fit exponential null methodology (true-date interval-likelihood
fit + forward MC with empirical aoristic kernel) controls the false-positive
(FP) rate at the nominal alpha = 0.05 across the entire Part A synthetic-data
grid, and preserves detection power on the binding 50 % / 50 y bracket at
n >= 2500. Recommend proceeding to the continuous-piecewise-linear (CPL)
extension of the same forward-fit framework.

**Run parameters**

- 30-cell grid: 27 Part A synthetic cells (3 b_null x 3 n x 3 brackets)
  + 3 Part B real-LIRE bootstrap cells (3 n, zero bracket only).
- 100 iterations per cell; 500 Monte Carlo (MC) replicates per envelope
  test; alpha = 0.05 two-tailed.
- Seed: 20260425; sapphire, 24 cores, joblib loky backend.
- Wall-time: 56.8 s for the full grid (median 160 ms per iteration).
- All 3,000 iterations converged.

---

## 1. Part A --- synthetic-data false-positive rates (zero bracket)

Synthetic data drawn from f(t; b_null) on [-50, 350]; widths sampled from
the empirical LIRE distribution; aoristic-resampled once. Then forward-fit +
forward-MC envelope test. Target FP <= 0.05; pass FP <= 0.10.

| b_null | n | FP rate | Wilson 95 % CI | flag |
|---|---|---|---|---|
| -0.005 | 500   | 0.030 | [0.010, 0.085] | ok |
| -0.005 | 2500  | 0.090 | [0.048, 0.162] | warn (>0.05; CI includes 0.05) |
| -0.005 | 10000 | 0.030 | [0.010, 0.085] | ok |
|  0.000 | 500   | 0.030 | [0.010, 0.085] | ok |
|  0.000 | 2500  | 0.050 | [0.022, 0.112] | ok |
|  0.000 | 10000 | 0.050 | [0.022, 0.112] | ok |
| +0.005 | 500   | 0.020 | [0.006, 0.070] | ok |
| +0.005 | 2500  | 0.040 | [0.016, 0.098] | ok |
| +0.005 | 10000 | 0.020 | [0.006, 0.070] | ok |

**Range:** min 0.020, max 0.090, mean 0.040.
**Cells > 0.05:** 1 / 9 (b=-0.005, n=2500; CI overlaps 0.05).
**Cells > 0.10:** 0 / 9.

The single warn cell (FP = 0.090) sits inside the Wilson 95 % CI for a true
rate of 0.05 at n = 100 iterations (which extends to ~0.107). The FP-rate
spread across cells is consistent with binomial sampling noise expected at
100 iterations per cell: ~5 of 100 iterations on average should land in the
rejection region under H0; the observed counts (2-9 per cell) match that
expectation across the 9 zero cells.

The fitted rate b_hat tracks the truth tightly across all conditions
(median |b_hat - b_null| < 1e-3 in every cell), so the forward-fit MLE is
recovering the true-date density correctly even for n = 500.

---

## 2. Part A --- detection rates (non-zero brackets)

Detection of an injected step effect over a 50 y or 25 y window centred on
AD 150. Targets: detection >= 0.80 at the binding cell.

### a_50pc_50y (50 % dip, 50 y; binding for the gate criterion)

| b_null | n | Detection | median p |
|---|---|---|---|
| -0.005 | 500   | 0.15 | 0.382 |
| -0.005 | 2500  | 1.00 | 0.000 |
| -0.005 | 10000 | 1.00 | 0.000 |
|  0.000 | 500   | 0.11 | 0.461 |
|  0.000 | 2500  | 1.00 | 0.000 |
|  0.000 | 10000 | 1.00 | 0.000 |
| +0.005 | 500   | 0.06 | 0.376 |
| +0.005 | 2500  | 0.99 | 0.000 |
| +0.005 | 10000 | 1.00 | 0.000 |

**Detection at n = 2500 is essentially saturated (0.99-1.00) across all
b_null** -- the gate criterion (>= 0.80 at n = 2500 for 50 % / 50 y) is met
with margin. n = 500 is below threshold for the 50 % / 50 y bracket; this
matches Option C's findings at the same n (Option C province step n = 500
detection ~ 0.13).

### c_20pc_25y (20 % dip, 25 y; harder bracket)

| b_null | n | Detection | median p |
|---|---|---|---|
| -0.005 | 500   | 0.03 | 0.652 |
| -0.005 | 2500  | 0.10 | 0.449 |
| -0.005 | 10000 | 0.32 | 0.093 |
|  0.000 | 500   | 0.01 | 0.705 |
|  0.000 | 2500  | 0.07 | 0.421 |
|  0.000 | 10000 | 0.40 | 0.079 |
| +0.005 | 500   | 0.05 | 0.643 |
| +0.005 | 2500  | 0.13 | 0.410 |
| +0.005 | 10000 | 0.24 | 0.157 |

c_20pc_25y is the hard bracket -- a 20 % dip over only 25 y is a small
modifier (one bin's worth at 5 y bins) on top of stochastic SPA noise.
Forward-fit reaches 0.24-0.40 detection at n = 10000, comparable to Option
C's reading on the same bracket at n = 10000 (province step: 0.495). Both
methods are clearly under-powered for this bracket below n ~ 25000; this
is a property of the aoristic SPA at these magnitudes, not a methodology
defect.

---

## 3. Part B --- real-LIRE bootstrap FP (diagnostic)

Bootstrap n rows from the full filtered LIRE corpus (180,609 rows);
forward-fit + forward-MC envelope on each iteration. Zero bracket only.

| n | FP rate | Wilson 95 % CI | median b_hat | median bins outside |
|---|---|---|---|---|
| 500   | 0.730 | [0.636, 0.807] | +0.00148 |  7 |
| 2500  | 1.000 | [0.963, 1.000] | +0.00155 | 30 |
| 10000 | 1.000 | [0.963, 1.000] | +0.00154 | 55 |

This elevation is **expected and informative**, not a methodology failure.
Real LIRE has substantial structure beyond a smooth exponential -- editorial
spikes (round centuries, common formula intervals), Severan-era surges,
plague-period dips, and so on. The fitted rate b_hat ~ +0.0015 (small
positive) reflects mild aggregate growth across the envelope, but the
distribution does not fit a single-rate exponential well, and the forward-MC
test correctly detects that mismatch.

What this tells us:

- **Forward-fit has detection power on real-data deviations from the null.**
  This is the property we want for the H3b research question
  ("does the empire-level SPA depart from a smooth exponential?"). Option C
  cannot answer this question because its null is the bootstrap of the
  observed corpus -- so any deviation is, by construction, swept into the
  reference distribution.
- **The forward-fit test will need a more flexible null** to be useful for
  characterising LIRE itself. The CPL extension (Timpson et al. 2021) is
  exactly that: a piecewise-linear shape that absorbs editorial spikes and
  episode structure into the fitted null, so that residual departures from
  the null are interpretable as substantively meaningful events rather than
  shape mis-specification.

---

## 4. Comparison against Option C

Option C (non-parametric row-bootstrap) was validated at the same n-values
in `outputs/option-c-validation/SUMMARY.md`. Headline comparison:

| Metric | Forward-fit (Part A) | Option C (province, step) |
|---|---|---|
| FP rate range (zero) | 0.020-0.090 | 0.030-0.045 |
| FP rate mean (zero)  | 0.040 | 0.036 |
| Detection at n=2500, 50 %/50 y | 0.99-1.00 | 1.000 |
| Detection at n=10000, 50 %/50 y | 1.00 | 1.000 |
| Detection at n=10000, 20 %/25 y | 0.24-0.40 | 0.495 |

The two methods agree closely on FP control on synthetic data drawn from a
smooth exponential and on detection power for the binding bracket. They
diverge on the harder c_20pc_25y bracket at n = 10000 (forward-fit
0.24-0.40, Option C 0.495), where Option C's slightly higher detection
likely reflects its bootstrap reference distribution capturing the bin-level
sampling variance of real LIRE more tightly than the synthetic-aoristic
forward MC.

Crucially, the two methods test **different null hypotheses**:

- **Option C** asks: "is this observed SPA more extreme than other
  re-bootstraps of the same corpus?" The reference distribution is centred
  on the observed corpus; deviations from a parametric growth model are
  *not* tested.
- **Forward-fit** asks: "is this observed SPA more extreme than synthetic
  data drawn from a true-date exponential null?" The reference distribution
  is centred on the parametric null; real-data structure deviating from the
  null *is* detected (Part B confirms this).

For H1 (detection thresholds against a parametric growth null), forward-fit
is the more principled test. For H3b (does LIRE depart from a smooth null?),
forward-fit with a flexible null (CPL) is the only one of the two that can
answer the question.

---

## 5. Diagnostic notes

- **Convergence:** 3,000 / 3,000 iterations converged. The bounded Brent
  optimiser on `[-0.05, 0.05]` is well-behaved for the rates encountered.
  The closed-form interval-integral with `_log_diff_exp` numerical
  stabilisation handles the largest probed values (`b * t_max` up to 17.5)
  without overflow.
- **Width-pool composition:** The empirical LIRE width distribution after
  filtering has 172,330 non-degenerate rows (median 99 y, range 1-2,059 y).
  The 1-y minimum corresponds to point dates; the 2,059-y maximum is a
  small tail that lies entirely within the [-50, 350] envelope after
  clipping. No width-distribution sampling pathology was observed.
- **Wall-time scaling:** Median per-iteration wall-time is 160 ms (p95
  576 ms). Driven mainly by the 500-replicate MC step at n = 10000;
  scales linearly in n_mc and approximately linearly in n. The full grid
  at the proposed CPL-extension scale (~4 fits per CPL cell, ~20 minutes
  on sapphire's 24 cores) is well within the project's compute envelope.
- **No edge cases hit:** no fits failed, no envelope tests raised, no
  width-pool zero-width rows surfaced (they were filtered out at load
  time).

---

## 6. Critical-friend four-check

### 1. More appropriate test? (`scipy.optimize.minimize_scalar` + closed-form integral)

`minimize_scalar` with `method='bounded'` (Brent on a finite interval) is
the correct primitive for a 1-D MLE with a known sign-stable bracket
[-0.05, 0.05]. The closed-form per-interval integral
`(exp(b*na) - exp(b*nb)) / b` (with the `_log_diff_exp` stabilisation) is
analytically exact -- no quadrature error -- and the Taylor-expansion limit
at `|b| < 1e-6` handles the b -> 0 singularity to working precision. For
the exponential family this is the cleanest path; quadrature would only be
needed if we wanted a non-exponential family. **No change recommended.**

### 2. More powerful / robust alternative? (Bayesian fit with uncertainty on b)

A point estimate `b_hat` plugged into the MC ignores fit uncertainty: the
envelope is conditional on `b = b_hat`, not marginalised over `p(b | data)`.
For n >= 2500 this matters very little -- the posterior on `b` is sharp
relative to the envelope width -- but for n = 500 the plug-in could be
slightly anti-conservative. A Bayesian variant would (i) get a posterior
on `b` (analytically tractable for this 1-parameter exponential or via
`scipy.stats.norm` Laplace approximation around the MLE), then (ii) for
each MC replicate sample a fresh `b ~ p(b | data)` before drawing synthetic
events. **Worth flagging as a follow-up experiment** if the CPL extension
shows under-powered behaviour at small n; the cost is negligible for the
exponential null but non-trivial for CPL (the analogous procedure would be
sampling from the CPL parameter posterior, which is multidimensional).

### 3. More current best practice? (post-2024 `rcarbon` / ADMUR literature)

`rcarbon::modelTest()` -- the canonical implementation since Timpson et al.
2014 -- still uses the `calsample` mechanism (sample n synthetic dates from
the fitted null, calibrate each, sum). The forward-fit pilot is the direct
inscription-data analogue of this mechanism, with the empirical width
distribution playing the role that calibration uncertainty plays in
radiocarbon. The 2026-04-25 prior-art scout report (section 8 empirical
addendum) identified the inscription-specific subtlety -- fit must be in
true-date space -- which the literature does not surface because radiocarbon
calibration does not have the symmetry-breaking aoristic-vs-true-date
distinction. **No post-2024 best-practice supersedes this approach** that
the scout or this validation has identified.

### 4. Do assumptions hold? (uniform position within interval; uniform aoristic)

The MC sampler assumes `u ~ Uniform(0, 1)` for the position of `t_true`
within `[nb, na]`. This is the standard "Uniform aoristic" assumption
(Ratcliffe 2002; Crema 2012; Kase et al. 2023); it says we have no reason
to favour any year within the dating interval. For Roman inscriptions
this is reasonable for paleography-based intervals (which set bounds, not
a peaked likelihood) and for emperor-reign intervals (uniform across the
reign). It is *less* reasonable for intervals tied to dated formulae
(e.g. consular dating, where the year is essentially known) -- but those
intervals are typically very narrow (1-2 y), so the within-interval
position has minimal effect on the binned SPA at 5 y bins. The trapezoidal
aoristic shape (FS-3 in `planning/`) is a future-work refinement that
could be folded in if/when the within-interval shape becomes load-bearing.
**Assumption holds for the present scale.**

---

## 7. Recommendation

**Proceed to the continuous-piecewise-linear (CPL) extension of the
forward-fit framework.** Sketch of next steps:

1. **`fit_null_cpl_forward`**: maximise the analogous interval likelihood
   for a CPL density `f(t; theta)` with k = 3 interior knots (per
   Decision 3 in `decisions.md`). The per-interval integral is now a sum
   over piecewise segments in [nb, na]; closed-form for each linear
   segment is straightforward. AIC reported per fit for the post-hoc
   k = {2, 3, 4} sensitivity.
2. **`sample_null_spa_forward_cpl`**: sample true dates from the fitted
   CPL via inverse-CDF on the piecewise-linear density (also closed-form;
   numerical-bisection if the segment is degenerate-flat). Forward-apply
   widths + uniform position + aoristic, identical to the exponential
   sampler from this pilot.
3. **Re-validate with the same Part A grid**, plus a new Part C: real-LIRE
   bootstrap with CPL null. Expectation: Part C FP control should be
   similar to Part A (because CPL absorbs the editorial-spike structure
   that elevated forward-exp Part B).
4. **Replace `primitives.fit_null_exponential` and `primitives.sample_null_spa`
   call-sites** in `experiment_aoristic_mc.py` and `h1_sim.py` with the
   forward-fit equivalents. Run the full H1 grid (256 cells) on sapphire
   with the new envelope mechanism.
5. **Write the preregistration amendment** documenting the move from the
   broken Poisson-on-fit envelope to the forward-fit envelope, with the
   prior-art chain (Timpson 2014 -> rcarbon -> scout -> Option A failure
   -> forward-fit pilot) as the methodological narrative.

Estimated effort for steps 1-3: ~1-2 days of focused work, mostly
closed-form integration and inverse-CDF derivation for the CPL family.
Step 4: ~0.5 day. Step 5: ~0.5 day.

The forward-fit framework promises both **principled FP control** (Part A
result) and **detection of real-data structure** (Part B result), neither
of which Option C can offer simultaneously. This is sufficient
justification to commit to the full forward-fit methodology rather than
fall back to the mixed approach.

---

## 8. Final figures

- **Part A FP** (zero bracket, 9 cells): min 0.020, max 0.090, mean 0.040;
  0/9 cells > 0.10.
- **Part A detection** at n = 2500 / 50 % / 50 y: 0.99-1.00 across b_null.
- **Part B FP** (real LIRE, n = 2500): 1.000 (95 % CI [0.963, 1.000]).
- **Wall-time:** 56.8 s for 3,000 envelope tests on sapphire's 24 cores.

Hard-stop check:
  - "FP > 0.20 mean across Part A zero cells -> FAIL": observed 0.040.  PASS.
  - "FP < 0.10 across all Part A zero cells AND detection >= 0.80 at
    n=2500 for 50 %/50 y -> PASS": both met (max FP 0.090; detection
    0.99-1.00).  **PASS.**
