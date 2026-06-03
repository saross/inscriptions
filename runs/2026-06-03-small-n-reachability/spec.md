# Small-N deconvolution-reachability study — spec

**Status:** SPEC — proposed 2026-06-03; **awaiting Shawn's launch sign-off**
(per the standing pre-launch-review rule). Host authorised: zbook.
**Authority:** operationalises Decision 34 (subset analyses use subset-specific
deconvolution). Answers: *how small a subset can be reliably de-fogged on its own?*

## 1. Objective and motivation

Decision 34 commits subset analyses to **subset-specific** deconvolution (the
model learns the subset's own convention mix; the empire-wide `p_conv` is not
imposed). A standalone per-subset fit is harder to identify at small N. This study
**measures the reliability floor** — the minimum subset size N at which
subset-specific deconvolution recovers the genuine SPA reliably under the
Decision-33 criterion — and reports it as a **reachability map** (N × α, faceted
by shape). The floor is the paper's reusable "use it when N ≥ ___" rule and the
core answer to the methods-reviewer's utility critique
(`planning/paper-significance-and-applications-2026-06-03.md`).

The existing recovery grid validated only N ∈ {2 000, 10 000, 50 000} — empire /
large-province scale. This study extends **downward** in N, where most subset
research actually operates.

## 2. Model (subset-standalone; no corpus `p_conv`)

`cell_lib.build_model_f1_f3` — **unchanged from the validated grid**: it *learns*
`tier_weights` (the convention composition) from the replicate's own data, places
a non-centred Gaussian-random-walk smoothness prior on the genuine SPA, and a
`Beta(1, 1)` prior on α. Only the universal **template-width basis** (century /
half-century / reign widths) is fixed — that is a feature of how editorial dating
works, not corpus content. So this model is exactly the "subset stands alone"
case Decision 34 requires; extending it downward in N measures that case's floor.

## 3. Design axes

| Axis | Values | Rationale |
|---|---|---|
| **N** (subset size) | 50, 100, 200, 350, 500, 1 000, 2 000 | dense where the break is expected; 2 000 overlaps the existing validated grid as an anchor |
| **α** (convention fraction) | 0.30, 0.50, 0.70, 0.85 | 0.30–0.70 = realistic reachable range; 0.85 = late-corpus stress (where high α and historical interest coincide) |
| **shape** | smooth_growth, rise_and_fall, regnal_cluster | easy / moderate / hard (sharp-peaked); same representative triple as the band-calibration check |
| **tier** | pilot_proxy | the realistic descriptive convention pattern (uniform optional as a later robustness pass) |
| **replicates / cell** | 50 | enough to estimate per-cell pass-rates and coverage at the floor |

Cells: 7 × 4 × 3 × 1 = **84**; fits: 84 × 50 = **4 200**.

## 4. Metrics (Decision-33 criterion + diagnostics), per cell

- **Convergence precondition:** fraction of replicates with max R̂ < 1.01 and no
  divergence excess. (Gate: ≥ 90 %.)
- **Shape recovery (binding):** fraction with posterior-median Pearson r ≥ 0.95
  between recovered and true genuine SPA. (Gate: ≥ 90 %.) All shapes are non-flat,
  so the hybrid flat-case patch is not exercised here.
- **α bias (diagnostic):** mean |recovered − true| α.
- **Band calibration (diagnostic):** mean pointwise 95 % coverage of the true
  genuine SPA (the §4a metric), to see how the band degrades with shrinking N.
- **Wasserstein-1 (supplementary).**

**Cell passes** if convergence ≥ 90 % AND shape-r ≥ 90 %. **Reachability floor**
for each (shape, α) = the smallest N whose cell passes; reported as a heatmap and
a conservative headline ("reliable down to N ≈ ___ across α ≤ 0.70").

## 5. Outputs

```
runs/2026-06-03-small-n-reachability/
├── spec.md                          # this file
├── code/reachability.py             # driver (adapts band-calibration.py)
└── outputs/
    ├── reachability-replicates.parquet
    ├── reachability-by-cell.csv
    ├── figures/reachability-map.png  # N × α pass/shape-r heatmaps per shape
    └── REPORT.md                     # the floor + map + honest-negative tail
```

## 6. Cost, host, pre-launch checks

- **Cost:** 4 200 fits; small-N fits are fast (~3–10 s; N=2 000 ~14 s). At
  `n_jobs=16` on zbook, **~40 min wall-clock. No API spend.**
- **Host:** zbook (`.venv/bin/python3`, pymc 6.0.1; **not** `uv run`). Stack note:
  the grid was fit under pymc 5.28; band calibration is a model property and
  transfers — flagged, as in the band-calibration run. Sapphire is reserved for
  Grid B (do not use until it lands).
- **Pre-launch checks (HALT and report if any fail):**
  1. Smoke: 1–2 cells × 2 reps converge and produce all metrics.
  2. `pilot_proxy` tier vector loads (same descriptive proxy as the grid).
  3. BLAS threads pinned to 1; `n_jobs` ≤ cores − 2.
  4. Deterministic seeds (reuse the grid's seed policy).

## 7. Scope, caveats, amendment status

- **Out of scope:** below-floor fall-backs (pooled-convention borrow; the §5
  hierarchical model). Logged for later (Decision 34).
- **Not preregistered:** this is methodology characterisation (like the recovery
  grid itself); **no OSF amendment is required to run it** (amendment-gate rule
  applies only to confirmatory-claim work). It feeds the paper's reachability map
  and the Decision-34 amendment.
- **`pilot_proxy` caveat:** a descriptive-frequency proxy, not a posterior draw
  (carried from the grid). The floor is reported for that convention pattern.
