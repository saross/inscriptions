---
priority: 1
scope: in-stream
title: "H1 min-thresholds simulation — implementation plan"
audience: "Shawn (review + sign-off), build agent (implementation)"
status: draft plan; awaiting Shawn sign-off before build
date: 2026-04-25
---

# H1 min-thresholds simulation — implementation plan

**Run directory:** `runs/2026-04-25-h1-simulation/`
**Author:** Claude Code (Opus 4.7, 1M context), under Shawn Ross's direction
**Commit policy:** this plan committed before build launches; build committed before audit; audit corrections committed; execution outputs committed. Single-concern commits.

---

## 1. Purpose and scope

Phase 1 of the OSF-preregistered three-phase study. Produces the numerical minimum-inscription-count thresholds that will be fixed in the preregistration (§8 TBD 1 of `planning/preregistration-draft.md`) before H2 and H3 run. Resolves one of the two remaining Field-8 TBDs and enables TBD 5 (Holm-Bonferroni family sizing).

**What the simulation does.** For every cell of (subset level × effect-size bracket × sample size n × null model), it (i) fits a null SPA to a sampled subset of LIRE, (ii) injects a synthetic effect at the prescribed magnitude and duration, (iii) runs the permutation-envelope test, (iv) records detection at *p* < 0.05. Repeated 1,000 times per cell. The detection-rate surface determines the smallest n at which detection ≥ 0.80 per bracket, per subset level. The 50 % / ≥ 50 y bracket is the binding primary; 0.70 and 0.90 curves reported for transparency; the zero-effect cell validates the false-positive rate.

**Scope boundary.** No LLM calls; pure local compute. The script is dataset-agnostic past the loader (per Decision 1, must accept any aoristically-dated frame) so the LIST swap in paper-sprint Week 1 reruns cleanly.

---

## 2. Deliverables — directory layout

```
runs/2026-04-25-h1-simulation/
├── spec.md                  # 1–2 pp, the "what and why"
├── plan.md                  # this document
├── decisions.md             # plan-level calls + critical-friend surfacings
├── seed.txt                 # fixed seed: 20260425
├── code/
│   ├── h1_sim.py            # main simulation driver (module-structured; see §4)
│   ├── primitives.py        # aoristic resample, null fit, effect injection, permutation test
│   ├── power_curves.py      # detection-rate curve builder + threshold extractor
│   ├── plots.py             # heatmap + power-curve figure generation (matplotlib, headless)
│   └── verify.py            # optional adversarial verifier (post-audit, if needed)
├── outputs/
│   ├── cell-results.parquet # per-iteration records: cell_id, iter, detected, pval, n_used, null_model, bracket, seed
│   ├── cell-summary.parquet # per-cell aggregate: detection_rate, FP_rate, CI, iter_count, wall_seconds
│   ├── thresholds.parquet   # smallest-n-at-0.80 per (level × bracket × null_model)
│   ├── power-curves/        # PNG per level × bracket, detection vs n with 0.70/0.80/0.90 gridlines
│   ├── heatmaps/            # PNG per level, effect-size × n detection-rate heatmap
│   ├── exp-vs-cpl.md        # comparison of exponential vs CPL-null threshold estimates
│   └── run.log              # timestamped log, per-cell wall time, worker PIDs
├── REPORT.md                # morning-reading report (structure in §11)
└── ro-crate-metadata.json   # provenance (following the descriptive-stats run convention)
```

Conventions lifted from `runs/2026-04-23-descriptive-stats/`: per-claim JSONL, every judgement call logged to `decisions.md`, seed pinned at top of driver, `outputs/run.log` with elapsed-second prefixes.

---

## 3. Critical-friend four-check (MANDATORY — surfaced before build)

Every statistical choice stress-tested against the standing rule. Each item below is a finding, not a silent adoption; Shawn decides.

### 3.1 More appropriate test for the data structure?

- **Permutation-envelope vs bootstrap vs Bayesian posterior predictive.** rcarbon-style permutation envelopes (Crema & Bevan 2021; Timpson et al. 2014) are the community-standard primitive for SPD/SPA deviation detection. Bootstrap alone wouldn't give the Monte Carlo envelope we want against a *parametric null* (exponential/CPL); posterior predictive under a Bayesian aoristic model (baorista, Crema 2025) is the most current alternative but is out-of-scope for H1 per Decision 3. **Finding: permutation-envelope is the right primitive.**
- **`scipy.stats.permutation_test` API vs hand-rolled.** `scipy.stats.permutation_test` is designed for exchangeability testing between *two samples* with user-supplied statistic. Our inner loop is different: we resample aoristic dates (inner), sum probability mass into bins, then compare to a parametric null envelope built from MC replicates of the fitted null model. **Finding: `scipy.stats.permutation_test` is the wrong API for the outer envelope** (the prereg's §3 phrases it as "scipy.stats.permutation_test as the primitive", but on inspection this conflates two levels). The right structure is (i) `scipy.stats.permutation_test` only for between-group SPA comparisons (not needed for H1), and (ii) a hand-rolled MC envelope loop for the within-SPA deviation-detection test. **Surface:** plan uses a hand-rolled Monte Carlo envelope loop wrapping `tempun`-based aoristic replicates, following Timpson et al. 2014 directly. `scipy.stats.monte_carlo_test` is a close match for the single-SPA-vs-null case and will be evaluated in the build step as a possible replacement for the hand-rolled loop.

### 3.2 More powerful / robust alternative?

- **Gaussian-tapered dip injection — conservative or biased?** Prereg §4 says Gaussian-taper is deliberately conservative vs step-function. This is true *for envelope tests*: a broad Gaussian shoulder looks more like natural fluctuation than a sharp edge, so thresholds set on Gaussian dips will be upper bounds for sharper events. **However**, matched detection of a known shape would be more powerful — if H2/H3 used a matched filter, H1 thresholds set on permutation envelopes would overestimate the n needed. **Surface:** this is acceptable because the downstream test (H3b) *is* permutation-envelope, so the H1 threshold is consistent with the operational test.
- **FWHM = bracket duration.** Gaussian FWHM = 2.355σ. If bracket duration = 50 y, σ ≈ 21.2 y. Under the Gaussian dip, the *integrated* magnitude over the bracket duration is smaller than the nadir magnitude — a "50 % dip over ≥ 50 y" with Gaussian shape has nadir = −50 % but the average over the 50 y window is roughly −37 % (for FWHM = duration). **Surface:** the prereg is ambiguous between "50 % at nadir for ≥ 50 y" (hard) and "50 % on average across ≥ 50 y" (moderate). **Plan adopts nadir = bracket magnitude, FWHM = bracket duration**, which is the more permissive reading for the detector (so more conservative for downstream H3). Requests Shawn's confirmation.
- **Detection threshold 0.80.** Standard; no alternative proposed.

### 3.3 More current best-practice?

- **Post-2018 developments.** Carleton & Collard 2020 (*The Holocene*) post-dates the 2018 PEWMA paper; Timpson et al. 2021 introduced CPL nulls (already captured as the secondary null per prereg §4). Crema & Bevan 2021 is already the reference for the permutation-envelope algorithm. **Finding: the prereg is current.** One minor addition: Crema 2022 (*JAMT*) is a literature review covering SPD best practice; worth citing in spec.md, no methodological change.
- **Bayesian aoristic (baorista, Crema 2025).** Out-of-scope for H1 per Decision 3 (sensitivity-only, paper-sprint Week 2).

### 3.4 Do assumptions hold?

- **Exponential null fit to LIRE.** Inscription production is roughly exponential-growth through the Principate then declines. An exponential null from 50 BC–AD 350 will fit poorly *by construction* — that's the point of the null (flag departures). But if the exponential fit's residuals are themselves large, the envelopes widen and threshold estimates become conservative. **Mitigation baked into plan:** pilot one subset per level, report fit residuals, warn in `decisions.md` if residual RMS exceeds reasonable tolerance.
- **CPL null — knot placement.** CPL with k knots has free parameters for knot timing and slope. Standard practice (Timpson et al. 2021) uses cross-validation or AIC to choose k. **Surface:** plan uses **k ∈ {2, 3, 4}** with AIC-best per subset — auto-selection, logged per cell. Alternatively fix k=3 for all subsets. Shawn to decide; plan defaults to AIC-select.
- **Permutation-test exchangeability under aoristic resample.** Each inscription's date is resampled uniformly (Decision 4) within its `[not_before, not_after]` interval per iteration; the inner permutation shuffles these across MC replicates to build the null envelope. Exchangeability holds under the null model. **Finding: assumption holds.**
- **Zero-width intervals / pathological rows.** LIRE v3.0 should have `not_before ≤ not_after`. If any row has `not_before == not_after` (point date), the uniform sample is degenerate — no issue mathematically, but logged. If any row has `not_before > not_after` after the filter, that's a data bug to flag and drop.
- **Gaussian-taper effect vs permutation detectability.** Covered in 3.2.

**Result of four-check: 4 items surfaced (3.1 API choice, 3.2 Gaussian shape semantics, 3.4 CPL knot selection, 3.4 residual-tolerance check). All addressed in plan; none block build.**

---

## 4. Script architecture

### 4.1 Module breakdown

**`primitives.py`** — reusable, unit-testable.

```python
def load_filtered_lire(path: Path) -> pd.DataFrame: ...
    # Returns is_within_RE & is_geotemporal & 50BC–AD350 intersect frame.

def aoristic_resample(df: pd.DataFrame, n: int, bin_edges: np.ndarray,
                      rng: np.random.Generator, b: float = 0.0) -> np.ndarray:
    # Returns SPA vector (len = len(bin_edges)-1).

def fit_null_exponential(spa: np.ndarray, bin_centres: np.ndarray) -> dict:
    # Returns fitted {rate, intercept, residual_rms}.

def fit_null_cpl(spa: np.ndarray, bin_centres: np.ndarray,
                 k_range: tuple[int,...] = (2,3,4)) -> dict:
    # Returns best-AIC CPL {knots, slopes, k_chosen, aic, residual_rms}.

def sample_null_spa(null_params: dict, model: str,
                    bin_centres: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    # Produces one MC replicate SPA under the fitted null (Poisson noise on mean).

def inject_effect(spa: np.ndarray, bin_centres: np.ndarray,
                  nadir: float, centre_year: float, fwhm: float) -> np.ndarray:
    # Modified SPA with Gaussian dip: spa * (1 + nadir * gaussian(t; centre, fwhm)).

def permutation_envelope_test(observed_spa: np.ndarray, null_params: dict,
                              model: str, bin_centres: np.ndarray,
                              n_mc: int, rng: np.random.Generator,
                              alpha: float = 0.05) -> dict:
    # Timpson et al. 2014 algorithm: MC replicates of null → pointwise 95% envelope;
    # global p-value via proportion of MC replicates with ≥ as many bins outside
    # pointwise envelopes as observed.
```

**`h1_sim.py`** — driver + cell-level executor.

```python
@dataclass(frozen=True)
class CellSpec:
    cell_id: str
    level: str               # "empire" | "province" | "urban-area"
    bracket: str             # "a_50pc_50y" | "b_double_25y" | "c_20pc_25y" | "zero"
    n: int
    null_model: str          # "exponential" | "cpl"
    n_iterations: int = 1000
    n_mc: int = 1000
    seed: int = 20260425

def run_cell(spec: CellSpec, source_df: pd.DataFrame) -> pd.DataFrame: ...
def main() -> None: ...
    # Enumerate CellSpecs → joblib.Parallel(n_jobs=-1, backend='loky') → concat → write.
```

**`power_curves.py`** — detection-rate curve builder (build curves, interpolate thresholds at 0.70/0.80/0.90).

**`plots.py`** — matplotlib (Agg backend); produces PNG + underlying data parquet per figure.

### 4.2 Parallelisation

- `joblib.Parallel(n_jobs=-1, backend='loky')`. Matches `runs/2026-04-23-descriptive-stats/code/profile.py` pattern.
- Seed discipline: master `np.random.SeedSequence(20260425)`; `.spawn(n_cells)` per cell; inside each cell, `.spawn(n_iterations)` per iteration. No shared global RNG. Bit-reproducible across worker counts.
- Large cells (n = 25,000) chunked into 100-iteration sub-tasks for load balance and per-task wall time < 5 min.

### 4.3 Data flow

```
LIRE_v3-0.parquet
   │ filter (is_within_RE, is_geotemporal, 50BC–AD350)
   ▼
filtered_df (~150k rows × few cols, <100 MB; broadcast read-only to workers)
   │
   ▼
per cell:
   ├── sample n rows (see §9 risk (f))
   ├── aoristic_resample → observed_spa
   ├── fit_null (exp and/or cpl)
   ├── inject_effect → observed_spa_modified
   ├── permutation_envelope_test (1000 MC)
   └── record detected + p + residuals + timing
   ▼
cell-results.parquet (append-safe; write per-chunk)
```

Bin edges: 5-year bins across 50 BC – AD 350 → 80 bins. Matches 2024 notebook and prereg §3.

---

## 5. Parameter table — every cell enumerated

- **Subset level**: `empire` (1 n only, large), `province`, `urban-area` — 3 levels.
- **Effect-size bracket**: `a` (50 % dip, FWHM 50 y), `b` (doubling, FWHM 25 y; positive deviation), `c` (20 % dip, FWHM 25 y), `zero` (FP calibration) — 4 brackets.
- **Null model**: `exponential`, `cpl` — 2 models.
- **n sweep per level**:
  - empire: single calibration n = 50,000 (approx full empire)
  - province: {100, 250, 500, 1000, 2500, 5000, 10000, 25000} — 8 values
  - urban-area: {25, 50, 100, 250, 500, 1000, 2500} — 7 values

**Cell count:**
- empire: 1 × 4 × 2 = 8
- province: 8 × 4 × 2 = 64
- urban-area: 7 × 4 × 2 = 56
- **Total cells: 128**

Iterations per cell: 1,000. MC replicates per test: 1,000. Total detection decisions: 128,000. Total MC replicates drawn: 1.28 × 10⁸ SPA evaluations.

---

## 6. Wall-time estimate

Per-iteration cost at n = 25,000: ~120 ms (aoristic + 1,000 × MC compare). Per-cell (1,000 iterations): ~120 s single-core. MC cost n-independent.

**Total single-core cost: 128 × ~130 s ≈ 4.6 h.**

- **amd-tower (16 cores, 30 GB): ~20 min wall-time** (joblib overhead + load imbalance ~1.3×).
- **Sapphire (≥ 32 cores): ~10 min.**

**Feasibility verdict:** runs comfortably on amd-tower locally. **Recommendation: run on amd-tower.** Standing rule is "sapphire for compute-heavy"; < 1 hour isn't heavy.

Safety margin: if per-iteration estimate is 3× optimistic, worst case ~1 h on amd-tower. Still local-feasible.

---

## 7. Memory envelope

- Filtered LIRE DataFrame: ~10 MB.
- Per-worker peak: ~150 MB (n = 25,000 aoristic array).
- 16 workers: ~2.4 GB. Safe on 30 GB amd-tower.
- cell-results.parquet: ~10 MB. Trivial.

No OOM risk.

---

## 8. Reproducibility plan

- **Seed:** `20260425` (file `seed.txt`). Exposed as `RANDOM_SEED` in `h1_sim.py`.
- **SeedSequence threading:** master `SeedSequence(20260425)` → `.spawn(n_cells)` per-cell → `.spawn(n_iterations)` per-iteration. Workers see only their own `Generator`.
- **Per-iteration recording.** Every MC decision written to `cell-results.parquet`. Schema: `cell_id, level, bracket, n, null_model, iter, detected, pval_global, n_bins_outside, null_residual_rms, null_k_chosen, seed_hex, wall_ms`.
- **ro-crate-metadata.json** captures LIRE parquet SHA-256, script hashes, `uv lock` dep versions.
- **Environment:** project `.venv/` — add `tempun>=0.2.4` and `matplotlib` to `pyproject.toml`.

---

## 9. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| (a) Overnight wall-time overrun | low | medium | local projected 20 min; 5× safety to 2 h still feasible; sapphire dispatch drafted (§10) |
| (b) Memory OOM | very low | high | projected peak ~2.4 GB on 30 GB box; monitor resident-size per 50 cells |
| (c) Zero-width date intervals | low | low | treat `not_before == not_after` as point-draw; log; drop `not_before > not_after` with warning |
| (d) Zero-variance SPA cells at small n | medium | medium | skip bins with null MC variance < 1e-10; log; flag if >5 % of iterations skip |
| (e) CPL fit failure on sparse subsets | medium | low | fallback to exponential null per-iteration, logged; mark CPL unreliable if >20 % fallback |
| (f) Subset sampling strategy | design choice | medium | **Surface:** plan uses **sampling-with-replacement from filtered LIRE** (bootstrap-style), not stratified. Alternative (stratified by province/city) more realistic but conflates H1's question with H2/H3 framing. Sensitivity addable post-hoc from persisted parquet |
| (g) scipy.stats.permutation_test API mismatch | surfaced 3.1 | — | hand-rolled MC envelope; documented in decisions.md |
| (h) Gaussian effect-shape semantics ambiguous | surfaced 3.2 | medium | nadir=magnitude, FWHM=duration; Shawn to confirm |
| (i) Loky worker hang on Python 3.13 | low | medium | `joblib>=1.5.3` supports 3.13; fall back to `multiprocessing.Pool` with `get_context('spawn')` if needed |

---

## 10. Launch command

```bash
cd ~/Code/inscriptions && .venv/bin/python3 runs/2026-04-25-h1-simulation/code/h1_sim.py \
  --out runs/2026-04-25-h1-simulation/outputs \
  --seed 20260425 \
  --n-jobs -1 \
  --log-level INFO 2>&1 | tee runs/2026-04-25-h1-simulation/outputs/run.log
```

Full 128-cell sweep end-to-end. No manual steps. `plots.py` and `power_curves.py` run as sub-commands of `h1_sim.py --mode=report` post-completion to rebuild REPORT.md sections from the persisted parquet.

**Stall-guard polling:** `pgrep -f "[.]venv/bin/python3.*h1_sim.py"`.

---

## 11. Morning report (`REPORT.md`) structure

Not a code dump. Structure:

1. **Headline recommended thresholds** per level × bracket × null-model (one table, 24 cells).
2. **Power curves** (PNG) at 0.70/0.80/0.90 detection thresholds.
3. **Effect-size × n heatmaps** per level with 0.80 contour highlighted.
4. **Zero-effect FP-rate table** per level × null-model (target ≤ 0.05).
5. **Exponential-vs-CPL comparison** — do thresholds differ materially?
6. **Execution notes** — deviations from plan, cell skips, CPL fallbacks.
7. **Open questions for Shawn** — at minimum: (i) null-model preregistration choice if exp and CPL disagree, (ii) whether urban-area 50 %/50 y threshold is operationally usable or implies H3 confirmatory status is province-only.

Target length: 800 – 1,200 words.

---

## 12. Audit hooks

`/audit` specifically verifies:

1. SeedSequence discipline threaded via `.spawn()` into every worker Generator. No global `np.random.seed()`.
2. Effect injection sign convention for bracket `b` (doubling, positive nadir). Unit test.
3. Permutation envelope p-value = proportion of MC replicates with ≥ as many bins outside pointwise envelope as observed (Timpson et al. 2014 global statistic). Not proportion of bins outside.
4. `aoristic_resample(replace=True)` per plan decision.
5. 5-year binning deterministic; no off-by-one at envelope endpoints.
6. CPL auto-selection reproducibility; AIC tie-break documented.
7. Zero-effect cell is identity transform (`np.testing.assert_allclose`).
8. Loader asserts `is_within_RE == True` and `is_geotemporal == True` post-filter count matches prereg expectation. Fails loudly otherwise.
9. Parquet schema stability; all per-iteration records carry `seed_hex`.
10. Wall-time sanity in `run.log`; flag if any cell > 5 × median.

---

## 13. Build-agent stall guards (baked into downstream brief)

- Sapphire workdir is `~/Code/inscriptions` (NOT `~/inscriptions`).
- Polling: `pgrep -f "[.]venv/bin/python3.*h1_sim.py"` with bracket-escape, or `kill -0 <pid>` on captured PID.
- Script content via Write tool's `content` parameter; never streamed as chat (600 s watchdog).
- Monitor loops on mtime or fresh-run markers, not file existence.
- Single-concern commits: plan → build → audit-fix → execution.

---

## 14. Constraints honoured

- No API calls (pure numpy / scipy / pandas / joblib / tempun local compute).
- UK / Australian English, Oxford comma.
