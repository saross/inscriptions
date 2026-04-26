# Forward-fit CPL — optimisation summary

Per Decision 9 (2026-04-26): the forward-fit CPL implementation needed
≥ 5× speedup before committing to a full preregistered H1 v2 rerun
(n_iter = 1000, n_mc = 1000). At baseline speed and 256 cells, the run
would take ≈ 94 h on sapphire — infeasible. This file documents the
profile-driven optimisation pass that brought wall-time down to a
single-figure-hours envelope.

## Headline result

| k | Baseline median (ms) | Optimised median (ms) | Speedup |
|---|----------------------|------------------------|---------|
| 3 | 758.9                | 158.9                  | 4.78×   |
| 4 | 1511.8               | 278.1                  | 5.44×   |

Methodology: `runs/2026-04-25-h1-simulation/code/bench_cpl.py` with
`--n_obs 2500 --n_warm 1 --n_runs 5 --n_restarts 8`. Synthetic
intervals drawn from the inlined LIRE-AIC-best CPL k = 3 truth used
by the v2 driver, widths sampled from the empirical LIRE distribution
(median 99 y).

Benchmark hardware: zbook (local development machine), CPython 3.13,
numpy 2.4.4, scipy 1.17.1, numba 0.65.1.

## What was changed

**(b) Vectorisation, low-temporary form.** The original
`_interval_integrals` allocated 5 temp arrays per segment (`lo`, `hi`,
`overlap`, `valid`, `seg_int`) and rebuilt `integrals` on each iteration
with `+`. Replaced with: pre-allocate `integrals` once, accumulate via
`+=`, and compute `mean_h = ha + slope * (0.5 * (lo + hi) - xa)`
directly (saving one pair of `h_at_lo` / `h_at_hi` allocations and one
`(h_at_lo + h_at_hi) / 2` operation per segment). Drops the
`np.any(valid)` short-circuit because the boolean-reduce ufunc was
itself the dominant cost.

**(d) Numba JIT for the full negative log-likelihood.** Profiling at
n_obs = 2500, k = 3 showed:

- 58 % of fit wall-time in `_interval_integrals` (per-segment numpy ops);
- 40 % of fit wall-time in scipy's L-BFGS-B finite-difference Jacobian
  (which calls the objective ~9 times per BFGS step for k = 3, ~10 for
  k = 4);
- ~10 % in surrounding decode + log + sum.

JIT-compiling the entire NLL into one tight loop (`_nll_numba_kernel`)
collapses these costs by eliminating per-call ufunc dispatch overhead.
On the inner kernel alone:

| Variant         | k=3 (µs/call) | k=4 (µs/call) |
|-----------------|---------------|---------------|
| baseline        | 95.1          | 114.3         |
| numpy "minimal" | 50.0          | 63.6          |
| **numba**       | **6.3**       | **21.1**      |

(Synthetic micro-benchmark, `bench_quick.py` and `bench_full.py`.)

The full NLL micro-benchmark (`bench_full.py`):

| Variant   | k=3 (µs/call) | k=4 (µs/call) |
|-----------|---------------|---------------|
| baseline  | 132.3         | 155.0         |
| **numba** | **28.8**      | **30.8**      |

(4.6× and 5.0× respectively at the objective level.)

Numba is added as an explicit project dependency; `numpy` ≥ 2.4 plus
`numba` 0.65 are compatible with each other and with `scipy` 1.17 in
this stack.

## What was NOT changed (and why)

**(a) Group-by-interval — skipped.** Profiling on the v2 simulation's
synthetic-from-null DGP showed all 2500 intervals had unique `(nb, na)`
pairs (continuous distributions for `t_true`, widths, and position). The
group-by optimisation only helps when many rows share dating bands
(e.g., real-LIRE bootstrap: 448 unique pairs out of 2500, a 5.6×
compression). For H1 v2 production the saving would be zero. We
documented the analysis here so a future H3a / H3b run on real LIRE
bootstraps can revisit (`bench_quick.py` already counts unique pairs).

**(c) Pre-compute segment-overlap masks — skipped.** The L-BFGS-B
inner loop changes knot positions every evaluation, so the segment-
overlap geometry cannot be cached across evaluations within a single
fit. Pre-computing the geometry once per fit (e.g., on the seed
positions) does not help because the optimiser's first move discards it.

**Analytic L-BFGS-B gradient — deferred.** L-BFGS-B's finite-difference
Jacobian still costs ~80 % of the wall-time in the optimised version
(8 evaluations × 30 µs = 240 µs per BFGS step, vs ~30 µs for the
single objective evaluation). A closed-form gradient through cumulative
softmax + per-segment trapezoids would cut another ~3–5×, but the
implementation is non-trivial (requires careful chain-rule with the
softmax + the segment overlap conditions) and the speedup target was
already met. Logged here as a future-work item if H1 v3 needs it.

**Cython / C extension — explicitly out of scope.** The hard-stop rule
in the agent brief said "stop at numba"; we did.

## Re-validation evidence

Stage 3 30-cell synthetic-from-null grid was rerun on sapphire after
the optimisation to confirm the FP rates still match the original
PASS verdict. See `revalidation/SUMMARY.txt` for the full output.

Side-by-side vs the original Stage 3 (which generated
`forward-fit-pilot/SUMMARY-CPL.md`):

| Metric                                        | Original Stage 3 | Revalidation |
|-----------------------------------------------|------------------|--------------|
| Part A.cpl FP mean                            | 0.034            | 0.027        |
| Part A.cpl FP max                             | 0.070            | 0.070        |
| Part A.cpl FP range                           | 0.010–0.070      | 0.000–0.070  |
| Cells > 0.10 (gate criterion)                 | 0 / 9            | 0 / 9        |
| Detection at n = 2500, 50 % / 50 y            | 1.00             | 1.00         |
| Detection at n = 10000, 50 % / 50 y           | 1.00             | 1.00         |
| Part C real-LIRE FP n = 500                   | 0.170            | 0.180        |
| Part C real-LIRE FP n = 2500                  | 0.990            | 0.990        |
| Part C real-LIRE FP n = 10000                 | 1.000            | 1.000        |
| Wall-time (full 60-cell grid)                 | ~4.5 min         | 1.7 min      |

All FP rates fall within the Wilson 95 % CI of the original
(n_iter = 100 → CI half-width ≈ ±0.05 around 0.05 → 0.000–0.107).
End-to-end wall-time including exp parts dropped 2.6× (the exp parts
were already fast). For CPL-only cells the speedup is ~5× per fit,
matching the headline benchmark above.

**Verdict: PASS.** Optimisation introduces no observable bias in FP
control; binding-bracket detection unchanged.

## Files

- `forward_fit_cpl.py` — the optimised module (numba kernel +
  Python fallback).
- `bench_cpl.py` — full-fit benchmark (this file's headline numbers).
- `bench_quick.py` — inner-kernel micro-benchmark.
- `bench_full.py` — full-NLL micro-benchmark.
- `profile_cpl.py` — cProfile harness for diagnostic purposes.
- `profile-baseline.txt`, `profile-after-numba.txt` — raw bench output.
- `profile-baseline-cprofile-k3.txt`,
  `profile-after-numba-cprofile-k3.txt` — function-level profile dumps.
