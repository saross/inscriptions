# §5 peak-scaling-Latin — peak-inscription vs Hanson-population scaling on the diagnostic unit — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13; no thresholds). Run on sapphire,
  2026-06-18 (background agent); REPORT written by the main session. Latin frame =
  lodged primary frame (Amendment 02). The diagnostic-unit version of the
  all-provinces peak-scaling (Obs 100).
- **Scope note:** only **Arm A** (full-frame raw peak vs cumulative) is a Latin-frame
  swap. The all-provinces run's 268-city §5 arms came from the Layer-A trajectory
  subset (a range-restriction probe, Obs 100) and are orthogonal to the Latin-frame
  definition — intentionally out of scope here.

---

## 1. Frame + comparator

Latin Sensitivity-B frame, **817 cities / 39 provinces, Roma excluded** (verified
against the H3a precedent). Cumulative comparator (from `idata-latin.nc`): Latin NBR
**β_within = 0.733 [0.648, 0.820]**.

## 2. Result — both fits converged (R̂ = 1.0000, 0 divergences, ESS ≥ 1,389)

| Arm | β_within [95 % CI] | n cities |
|---|---|---|
| cumulative (H3a Latin, reference) | 0.733 [0.648, 0.820] | 817 |
| **raw peak, 50y (headline)** | **0.700** [0.618, 0.784] | 817 |
| raw peak, 25y (window sensitivity) | 0.693 [0.612, 0.775] | 817 |

## 3. Peak ≈ cumulative on the diagnostic unit too (confirms Obs 100)

The raw peak-bin scaling exponent (0.700 at 50y, 0.693 at 25y) is **statistically
indistinguishable from the Latin cumulative 0.733** (CIs overlap heavily; marginally
flatter, not significantly so). This reproduces the all-provinces finding (Obs 100:
raw peak 0.557 ≈ cumulative 0.587) on the primary Latin frame: **bigger cities have
proportionally higher peaks and higher totals under the same scaling law** — peak
scales like total, so the cumulative β headline is not an artefact of aggregating over
time.

## 4. Caveats

Exploratory; no thresholds (Decision 13). Inherits the all-provinces peak-scaling
design. The 25y/50y window pair is the sensitivity band; both agree.

## 5. Outputs

`outputs/peak-scaling-latin-summary.json` (per-arm β, convergence, frame provenance);
`peak-scaling-latin-forest.png`. Cross-refs: Obs 100 (peak-scaling all-provinces),
Obs 101 (diagnostic-unit framing), Amendment 02 (Latin primary).
