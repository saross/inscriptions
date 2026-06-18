# §5 H7-Latin — time-resolved (per-period) H3c on the diagnostic unit — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13; no thresholds). Run on sapphire,
  2026-06-18 (background agent); REPORT written by the main session (the agent was
  blocked from writing it). The Latin frame is the **lodged primary frame**
  (Amendment 02, 2026-06-06), so this is the diagnostic-unit version of the
  all-provinces H7 (Obs 99).
- **Method:** every modelling choice inherited verbatim from the all-provinces H7
  (`runs/2026-06-17-s5-h7-perperiod-h3c/`) by importing the audited modules; only
  the city/province universe changed. 8 × 50y periods; aoristic-apportioned counts;
  population-based Mundlak NBR + H3c per period.

---

## 1. Latin frame — verified against the H3a precedent

Built from the canonical Sensitivity-B frame
(`data/processed/city_level_for_h3a_latin.parquet`, `h3a_common.build_latin_frame`),
verified against `runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json`:

| Quantity | This run | H3a precedent | Match |
|---|---|---|---|
| cities | 817 | 817 | ✓ |
| provinces | 39 | 39 | ✓ |
| Roma | excluded | excluded (`rome_mask`) | ✓ |
| capitals in frame | 41 | — | — |

The diagnostic unit is **Latin-minus-Roma**; Roma is dropped at the primary-frame
stage, so the frame is already Roma-free. **Cumulative comparator** (re-verified from
`idata-latin.nc`): Latin NBR **β_within = 0.733 [0.648, 0.820]**.

---

## 2. Per-period results — all 8 periods converged (R̂ = 1.0000, 0 divergences, ESS ≫ 400)

| Period | β_within [95 % CI] | capital P(contrast>0) | clustering (≥2-of-3 k) |
|---|---|---|---|
| 50 BC–AD 0 | **0.886** [0.76, 1.01] | 1.00 | **YES** (3/3; k8 I=0.037, p=0.020) |
| AD 0–50 | 0.801 [0.69, 0.92] | 1.00 | **YES** (2/3; k8 I=0.027, p=0.047) |
| AD 50–100 | 0.816 [0.71, 0.92] | 1.00 | no (0/3) |
| AD 100–150 | 0.699 [0.60, 0.80] | 1.00 | no |
| AD 150–200 | 0.693 [0.60, 0.79] | 1.00 | no |
| AD 200–250 | 0.708 [0.61, 0.81] | 1.00 | no |
| AD 250–300 | 0.690 [0.58, 0.79] | 1.00 | no |
| AD 300–350 | 0.799 [0.67, 0.93] | 1.00 | no |

---

## 3. The diagnostic unit confirms the all-provinces picture (Obs 99)

1. **β_within traces the same U over the four centuries, shifted upward.** Latin:
   0.89 → ~0.69–0.71 high-empire plateau (AD 100–300) → 0.80 (4th c.). All-provinces
   (Obs 99): 0.70 → ~0.58 plateau → 0.66. The **Latin plateau (~0.69) sits just below
   the Latin cumulative 0.733**, exactly as the all-provinces plateau (~0.58) tracked
   its cumulative 0.587. So the U-shape is a **feature of the diagnostic unit**, not an
   artefact of mixing in the under-covered Greek East.
2. **Capitals over-produce in every period** (P(contrast>0) = 1.00 all 8), identical
   to all-provinces — a robust, time-stable replication of Hanson 2021's capital
   over-production.
3. **Spatial clustering is early-empire-only:** the H3c(ii) ≥2-of-3-k rule passes in
   the **two earliest** periods (50 BC–AD 0 and AD 0–50) and washes out from AD 50 on.
   All-provinces had it in the single earliest period — the same pattern, marginally
   more persistent on the Latin frame.

---

## 4. Caveats

- Exploratory; no thresholds (Decision 13). Inherits the all-provinces H7 design.
- Per-period counts thin at the envelope edges (4th c. n=3,744) — widest CIs there.
- Clustering uses the project H3c(ii) rule (≥2-of-3 k∈{5,8,10}, 999-permutation).

## 5. Outputs

`outputs/h7-latin-summary.json` (per-period β, capital contrast, Moran per k,
convergence; frame provenance); `h7-latin-per-city-residuals.parquet`;
`h7-latin-time-resolved.png`. The 8 per-period idata `.nc` (~456 MB) are regenerable
and gitignored (kept on sapphire). Cross-refs: Obs 99 (H7 all-provinces), Obs 101
(diagnostic-unit framing), Amendment 02 (Latin primary).
