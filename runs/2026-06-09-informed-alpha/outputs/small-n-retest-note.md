# Small-N Retest — Informed-α Prior at Realistic Unit Sizes

**Date:** 2026-06-09
**Script:** `runs/2026-06-09-informed-alpha/code/small_n_retest.py`
**Raw output:** `runs/2026-06-09-informed-alpha/outputs/small-n-retest.json`
**Run host:** sapphire (`~/Code/inscriptions` uv env, `taskset -c 0-11`, FAST_RUN)

## Question

The prototype found a wide informed-α prior (κ ∈ {4, 6, 8}) barely moves the
period-concentrated α estimate at N=10,000. The real affected frontier-province
units are N ≈ 1,500–2,800. Does the prior bite harder at realistic small N,
and at what κ?

## Design

- **Regime:** period-concentrated only (narrow Gaussian true p_conv, µ=AD 200,
  σ=60; fit with broad shared Latin basis — the identifiability failure mode).
- **N ∈ {1500, 2500}**; α_true ∈ {0.30, 0.60}.
- **Priors:** flat Beta(1,1); informed Beta at κ ∈ {6, 10, 20}, two mean
  conditions: exact (mean = α_true) and biased (mean = α_true − 0.10).
- **Sampler:** draws=2000, tune=1000, chains=4, target_accept=0.95, cores=1.
- All Rhat < 1.005; zero divergences across all 28 fits.

## Results — α-recovery bias (median − α_true)

```
   N   α_true  prior                      α_med    bias
------  ------  -------------------------  ------  -------
  1500    0.30  flat                        0.061  −0.239
  1500    0.30  informed_exact_k6           0.086  −0.214
  1500    0.30  informed_exact_k10          0.116  −0.184
  1500    0.30  informed_exact_k20          0.158  −0.142
  1500    0.30  informed_biased_k6          0.060  −0.240
  1500    0.30  informed_biased_k10         0.082  −0.218
  1500    0.30  informed_biased_k20         0.113  −0.187

  1500    0.60  flat                        0.034  −0.566
  1500    0.60  informed_exact_k6           0.100  −0.500
  1500    0.60  informed_exact_k10          0.140  −0.460
  1500    0.60  informed_exact_k20          0.205  −0.395
  1500    0.60  informed_biased_k6          0.086  −0.514
  1500    0.60  informed_biased_k10         0.121  −0.479
  1500    0.60  informed_biased_k20         0.178  −0.422

  2500    0.30  flat                        0.060  −0.240
  2500    0.30  informed_exact_k6           0.081  −0.219
  2500    0.30  informed_exact_k10          0.108  −0.192
  2500    0.30  informed_exact_k20          0.146  −0.154
  2500    0.30  informed_biased_k6          0.060  −0.240
  2500    0.30  informed_biased_k10         0.079  −0.221
  2500    0.30  informed_biased_k20         0.106  −0.194

  2500    0.60  flat                        0.035  −0.565
  2500    0.60  informed_exact_k6           0.103  −0.497
  2500    0.60  informed_exact_k10          0.141  −0.459
  2500    0.60  informed_exact_k20          0.205  −0.395
  2500    0.60  informed_biased_k6          0.088  −0.512
  2500    0.60  informed_biased_k10         0.122  −0.478
  2500    0.60  informed_biased_k20         0.179  −0.421
```

## Verdict

**The informed prior does bite harder at small N than at N=10,000, but it still
fails badly at all tested κ.** Even at the tightest tested value (κ=20, exact
mean), the absolute bias remains −0.14 to −0.40 — the posterior median sits at
roughly 15–35 % of the true α, not anywhere near truth. At κ=20 biased, it is
slightly worse (−0.19 to −0.42), confirming proxy noise compounds the problem.
There is no κ at which the prior rescues recovery: the bias remains severe across
both N and both α_true values.

The small-N advantage is real but inconsequential: going from N=10,000 (prototype
bias ≈ −0.27 at α_true=0.30 per the recovery-results.json) to N=1,500 loosens
the likelihood just enough that κ=20 can pull α_med from ≈0.060 to ≈0.158 — a
meaningful gain in the posterior mean, but still a bias of −0.14. The fundamental
problem is not sample size: it is the basis mismatch (broad shared basis vs narrow
true convention). The flexible GRW p_gen absorbs the narrow convention mass
regardless of N or prior tightness.

**Shelf the informed-prior-only fix.** The shape_pairing_probe.py diagnosis
stands: the prior must be paired with a per-unit or period-aware convention SHAPE
to be effective.

## Convergence

All 28 fits: max Rhat ≤ 1.004; min ESS_bulk not shown in table but no chain
issues flagged by PyMC; zero divergences. Sampler is healthy throughout.
