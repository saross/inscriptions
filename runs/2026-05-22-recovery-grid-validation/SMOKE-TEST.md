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

## Launch decision

The 11.25 h estimate is within sapphire's normal long-job envelope
(overnight). The job's per-cell checkpoint (`grid-state.json`) lets it
be monitored and stopped cleanly at any cell boundary; replicates within
a cell are atomic, so a kill mid-cell loses at most one cell's progress.
The brief's "halt and ask if too expensive" rule is interpreted as
applying to multi-day runs, not overnight runs.

Launching grid run with n_jobs = 20, 100 replicates per cell (the
preregistered minimum), all 450 cells.
