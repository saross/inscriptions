# Per-cell implementation plan

This plan describes what the simulation script does for each grid cell.
A cell is the tuple `(alpha, shape_name, tier_weights_name, N)`. Total cells
= 5 × 6 × 5 × 3 = 450; total replicates = 45,000. Replicate count per cell
is 100 (prereg-binding; Decision 21).

## 1. Cell enumeration

Cells are enumerated deterministically (in the joblib outer loop) in the
order: shape_name (alphabetical: bimodal, flat_baseline, regnal_cluster,
rise_and_fall, smooth_decline, smooth_growth) × alpha (ascending) ×
tier_weights_name (alphabetical: century_heavy, half_century_heavy,
pilot_proxy, reign_heavy, uniform) × N (ascending). The cell_index is the
position in this enumeration; cell_seed = base_seed + cell_index.

`cell_id` is the human-readable string
`shape={shape_name}_alpha={alpha:.2f}_tier={tier_weights_name}_N={N}`
(e.g. `shape=rise_and_fall_alpha=0.50_tier=uniform_N=10000`).

## 2. Per-replicate generative procedure (script 01)

For each replicate r in {0, ..., 99}:

1. Set the per-replicate RNG seed to `cell_seed * 1000 + r`.
2. Build the convention-shape vector `p_conv` (length 80) as
   `tier_weights @ tier_basis`, where:
   - `tier_basis` is the 3 × 80 matrix in which row k is the
     interval-width-normalised uniform mass over tier k's template
     intervals (per Decision 20 line 1755-1759).
   - Each tier's row sums to 1; the convex combination of three sum-to-1
     rows is sum-to-1.
3. Build the genuine-shape vector `p_gen` (length 80) by evaluating the
   pinned generator at bin centres and renormalising to sum to 1.
4. Compute `p_true = alpha * p_conv + (1 - alpha) * p_gen` (length 80,
   sums to 1).
5. Draw `y ~ Multinomial(N, p_true)` (length 80, sums to N).
6. Persist `y` plus the truth artefacts (`p_conv`, `p_gen`, `p_true`,
   `tier_weights`, `alpha`, `N`, `seed`) to
   `data/synthetic-cells/<cell_id>/replicate_<r>.parquet`.

## 3. Per-replicate fit procedure (script 02)

For each replicate r:

1. Read the synthetic replicate (script 01 output).
2. Construct the pymc model — three-tier mixture with smoothness-prior
   `p_gen`:
   - `alpha ~ Beta(2, 2)` (prereg §3 line 206).
   - `tier_weights ~ Dirichlet([1, 1, 1])` (prereg §3 line 206;
     uniform-on-the-simplex).
   - `log_p_gen_raw[80] ~ GaussianRandomWalk(sigma_smooth)` with
     `sigma_smooth ~ HalfNormal(1)` (prereg §3 line 204, line 206 —
     "Gaussian random-walk smoothness prior" / "σ ~ HalfNormal(1)").
   - `p_gen = softmax(log_p_gen_raw)`, deterministic; sums to 1 by
     construction.
   - `p_conv = tier_weights @ tier_basis` (tier_basis is fixed at the
     design-pinned tier_basis matrix; this matches the prereg's "fix the
     tier-weights to their true values" simplification in the brief, but
     here we **infer** tier_weights jointly with alpha as the prereg's
     Dirichlet prior calls for — the simplification is rejected because
     the prereg's primary fit infers tier weights from data; see §3 line
     206. The simulation generative process uses pinned tier weights from
     the grid; the inference posterior re-discovers them).
   - `p_mix = alpha * p_conv + (1 - alpha) * p_gen`.
   - `y ~ Multinomial(N_observed, p_mix)` (prereg §3 line 188-189).
3. Sample with NUTS: 4 chains × 2 000 draws × 1 000 tune,
   target_accept = 0.95, deterministic seed.
4. Record from the posterior:
   - α 95 % CI (2.5 / 97.5 percentiles) and median.
   - posterior-median `p_gen` (length 80).
   - Pearson r between posterior-median `p_gen` and the true `p_gen`.
   - Wasserstein-1 (scipy.stats.wasserstein_distance) between
     posterior-median `p_gen` and true `p_gen`, with bin-centre support.
   - convergence diagnostics: max R-hat, min ESS_bulk (per prereg §3 line
     208 gates: R-hat < 1.01, ESS_bulk ≥ 400).
   - tier_weights posterior median (3-vector) and tier_weights truth
     coverage flag (does the per-tier 95 % CI contain truth).
5. Persist these to
   `outputs/cell-fits/<cell_id>/replicate_<r>-posterior.parquet`.

## 4. Per-cell aggregation (script 03)

Read all per-replicate posteriors for one cell; compute:

- `alpha_coverage`: fraction of replicates whose α 95 % CI contains
  truth. Cell **passes coverage** if this ≥ 0.90.
- `median_pearson_r_pgen`: median across replicates of the
  per-replicate Pearson r between posterior-median p_gen and truth. Cell
  **passes shape recovery** if this ≥ 0.95.
- `median_wasserstein_1_pgen`: descriptive only.
- `tier_coverage[k]`: per-tier coverage rate (descriptive).
- `convergence_pass_rate`: fraction of replicates meeting both R-hat and
  ESS gates.

Persist to `outputs/cell-summaries/<cell_id>-summary.json`.

## 5. Grid orchestration (script 04)

The orchestrator iterates over the grid (loaded from `design.json`),
launches per-cell jobs in parallel via `joblib.Parallel(n_jobs <= 20)`.
For each cell, the orchestrator runs scripts 01 + 02 + 03 as a single
function call (one synthetic-generate-fit-aggregate worker per cell).
Saves `outputs/grid-state.json` after each cell completes; on restart,
skips completed cells. NUTS chain parallelism inside pymc may need to be
disabled (cores=1) to avoid worker oversubscription on a 24-core box
when n_jobs=20.

If pymc's per-fit cost exceeds 12 s during the smoke test, the
orchestrator caps n_jobs at 6 (= 24 / 4) and lets each fit use its full
4-chain parallelism.

## 6. Final grid summary (script 05)

Read all per-cell summaries; compute the binding pass rates:

- `frac_cells_pass_alpha_coverage`: fraction of cells where
  alpha_coverage ≥ 0.90. **Validation requires ≥ 0.90.**
- `frac_cells_pass_shape_recovery`: fraction of cells where
  median_pearson_r_pgen ≥ 0.95. **Validation requires ≥ 0.90.**
- emit `outputs/REPORT.md` with results vs the preregistered ≥ 90 % /
  ≥ 90 % thresholds; per-cell pass/fail table; failure-mode
  characterisation (which (alpha, shape, tier_weights, N) cells failed).

## 7. File-system layout (final)

```
runs/2026-05-22-recovery-grid-validation/
  code/
    01-synthetic-cell-generator.py
    02-cell-mixture-fit.py
    03-cell-aggregator.py
    04-grid-runner.py
    05-grid-summariser.py
  data/
    synthetic-cells/
      <cell_id>/
        replicate_0.parquet ... replicate_99.parquet
  outputs/
    cell-fits/
      <cell_id>/
        replicate_0-posterior.parquet ... replicate_99-posterior.parquet
    cell-summaries/
      <cell_id>-summary.json
    grid-state.json
    grid-runner.log
    REPORT.md
```

## 8. Anchor for verification

`spec.md` § 7 cross-references — all line numbers in the prereg and
decision-log were verified at design time against the source files; the
prereg has been amended several times since lodgement so re-verification
before any future edits is essential.
