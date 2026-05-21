# Smoke-test results — 2026-05-22

## Setup

- Host: sapphire (24 cores; 60 GB RAM; pymc 6.0.1 / pytensor 3.0.3 /
  numpy 2.4.6 / pandas 3.0.3 / arviz 1.1.0 / scipy 1.17.1)
- venv: `~/cc-scratch/inscriptions-talk-prep/venv/`
  (joblib 1.5.3 added 2026-05-22)
- Scratch root on sapphire: `~/cc-scratch/inscriptions-recovery-grid/`

## Smoke cell

One cell × one replicate end-to-end through 01 → 02 → 03:

- `cell_id`: `shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000`
- Replicate: 0
- NUTS settings: 4 chains × 2 000 draws × 1 000 tune,
  target_accept = 0.95, cores = 1.

## Result

01-generator: wrote synthetic data + truth sidecar to
`data/synthetic-cells/shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000/replicate_000.parquet`.

02-fit:

| Metric | Value |
|---|---|
| α true | 0.500 |
| α posterior median | 0.422 |
| α 95 % CI | [0.252, 0.596] |
| α-CI covers truth? | **True** |
| Pearson r (posterior-median p_gen vs truth) | **0.9929** |
| Wasserstein-1 | 12.435 |
| max R-hat | 1.0063 (gate < 1.01: PASS) |
| min ESS_bulk | 517 (gate ≥ 400: PASS) |
| divergences | 0 |
| convergence_pass | **True** |
| Wall-clock per fit | **18.4 s** |

03-aggregate: per-cell summary written. With one replicate the
α-coverage rate is 1.0 (trivial) and the median Pearson r is 0.9929
(the single replicate's value). Both prereg-binding criteria pass on
this single-replicate sanity check.

## Convergence note — slight R-hat excess at 1.0063

R-hat 1.0063 sits just inside the gate (1.01) for this replicate. The
random-walk increments on `log_pgen_raw` are the slowest-mixing
parameters; this is expected (high-dimensional random-walk priors are
not as well-conditioned as parametric Gaussians). The 18 s/fit budget
already uses 4 chains × 2 000 draws × 1 000 tune at target_accept 0.95,
the prereg-spec settings. If grid-wide convergence pass rates drop
materially below 90 %, the response is to tune-and-redraw (e.g. 3 000
draws / 2 000 tune) under an OSF amendment, not to relax R-hat.

## Wall-clock estimate for full grid

- Per-fit budget (working figure): **18 s** at N = 2 000. N affects only
  the multinomial loglik value, not its tensor shape, so per-fit time
  should be approximately constant across N ∈ {2 000, 10 000, 50 000}.
- Total fits: 450 cells × 100 replicates = 45 000.
- Single-core wall-clock: 45 000 × 18 s = 810 000 s = **225 h**.
- Parallel wall-clock at n_jobs = 20: **~11.25 h** (overnight run).
- Parallel wall-clock at n_jobs = 24 (no headroom): ~9.4 h.

This is above the spec.md upper estimate of 9.4 h (which assumed
15 s/fit). The 18 s figure is the empirical reality from the smoke
test on the simplest N. The 11.25 h estimate is the working number for
the launch.

## Launch decision (revised) — HALTED for direction

The 11.25 h estimate assumed standalone per-fit timings of 14-18 s
scale linearly under parallel load. **Empirical benchmarks on sapphire
revealed substantial concurrency-related slowdown**:

| Config | Per-fit wall | Throughput | Full-grid estimate |
|---|---|---|---|
| Standalone (1 fit) | ~14-18 s | — | — |
| 4 bash-parallel processes | ~13 s | ~0.30 fits/s | ~42 h |
| 20 bash-parallel processes | 17-32 s (avg 26 s) | ~0.59 fits/s | ~21 h |
| joblib loky (n_jobs=4, 1 thread) | ~45 s | 0.071 fits/s | ~176 h |
| joblib loky (n_jobs=8, 1 thread) | ~40 s | 0.13 fits/s | ~96 h |
| joblib loky (n_jobs=20, 1 thread) | 50-115 s | ~0.25 fits/s | ~50 h |
| **Subprocess pool (n_jobs=20)** — current orchestrator | **~50 s avg in 20-cell warmup** | **0.189 fits/s** | **~66 h** |

Throughput diagnoses:

- Single-threaded BLAS confirmed via /proc/PID/environ on workers.
- Bash-parallel 20-way fits at 26 s avg achieve 0.59 fits/s (best
  case), but require a 20-process pool maintained explicitly outside
  pytensor's process model.
- Joblib/loky concurrency inflates per-fit wall by 3-5x — most
  plausibly due to shared pytensor compile-cache state or a
  pytensor-internal coordination cost across pool workers.
- The subprocess-pool orchestrator (current implementation) gets
  ~0.19 fits/s — better than loky but still 3x slower than the bash-
  parallel best case. The gap is likely due to per-cell subprocess
  startup (each cell launches a fresh python process; python startup
  + sibling-module reloading is ~3-5 s overhead per cell).

Steady-state extrapolation for 100-replicate cells:

- Per cell, steady-state under n_jobs=20 contention: ~50 s/fit ×
  100 reps + 5 s startup = ~5 000 s/cell = 1.4 h/cell wall (in a
  single worker; reduced by concurrency).
- 450 cells / 20 concurrent = 22.5 batches × ~5 000 s = ~31 h wall
  best case; **66 h** wall worst case (the 5-replicate
  benchmark's measured rate).

This is materially above the spec.md upper estimate of 9.4 h. Per
the brief's "halt and report" rule:

> "If the grid is too expensive at the preregistered 100 replicates
> × all cells, DO NOT silently reduce the replicate count. Instead,
> halt, report the wall-clock estimate, and ask for direction."

**Grid run halted, awaiting Shawn's direction.** Options for
discussion:

1. **Accept the 31-66 h wall-clock** and launch as preregistered —
   straightforward, no preregistration impact, runs over 1-3 days
   continuously on sapphire.
2. **Investigate the joblib/subprocess overhead further** — there
   may be a pytensor `THEANO_FLAGS`/`PYTENSOR_FLAGS` setting that
   removes the inter-process coordination cost. Worth ~1 hour of
   investigation if it lets us hit the ~21 h bash-parallel rate.
3. **Reduce NUTS draws** — drop from 2 000 to 1 000 draws (halving
   per-fit cost) only if convergence still passes the prereg-binding
   gates (R-hat < 1.01, ESS_bulk >= 400). This is a methodological
   judgement call, not a silent reduction; it'd be a design-artefact
   revision documented at the appropriate `runs/` directory.
4. **Reduce replicates per cell** — the prereg-binding minimum is
   100 (Decision 21 line 1903; prereg §4 line 331). The "two-stage
   variant" mentioned in the prereg (50 across the grid, 200 at
   boundary cells; prereg §4 line 331) is permitted and might cut
   wall-clock by ~50 % for the first pass. This would require
   amending the design artefact.

The infrastructure is in place and resumable: the subprocess pool
checkpoints after every cell. Whatever direction Shawn chooses, the
grid can be relaunched without redoing already-completed cells.
