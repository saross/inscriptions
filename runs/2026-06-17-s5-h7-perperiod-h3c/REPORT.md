# §5 H7 — time-resolved (per-period) H3c — RESULTS

- **Status:** COMPLETE (exploratory; prereg §5 line 384; no thresholds).
- **Run:** sapphire, 2026-06-17; 8 × 50-year-period H3a NBR fits + H3c
  diagnostics; `code/h7_perperiod_h3c.py`; log `run.log`. **All 8 periods
  converged** (R̂ = 1.0000, 0 divergences). Figure: `outputs/h7-time-resolved.png`.

---

## 1. Results table (50-year periods, 8 over 50 BC – AD 350)

| Period | non-0 cities | count | β_within [95% CI] | capital P(>0) | Moran I (k8), p |
|---|---|---|---|---|---|
| 50 BC–AD 0 | 434 | 4714 | **+0.701** [0.60, 0.81] | 1.00 | **+0.029, p=0.021** |
| AD 0–50 | 624 | 12633 | +0.667 [0.57, 0.77] | 1.00 | +0.016, p=0.111 |
| AD 50–100 | 696 | 14031 | +0.629 [0.54, 0.73] | 1.00 | +0.005, p=0.292 |
| AD 100–150 | 735 | 11636 | +0.582 [0.50, 0.67] | 1.00 | −0.013, p=0.187 |
| AD 150–200 | 779 | 12793 | +0.580 [0.50, 0.67] | 1.00 | −0.005, p=0.459 |
| AD 200–250 | 717 | 10229 | +0.587 [0.50, 0.67] | 1.00 | −0.003, p=0.466 |
| AD 250–300 | 623 | 5077 | +0.581 [0.49, 0.67] | 1.00 | −0.014, p=0.155 |
| AD 300–350 | 518 | 3948 | +0.659 [0.55, 0.77] | 1.00 | −0.012, p=0.219 |

> [Corrected 2026-06-20, accuracy audit: AD 100–150 Moran's I (k=8) was −0.014, now
> −0.013 (raw −0.013478); AD 150–200 was −0.004, now −0.005 (raw −0.004550). Primary:
> `outputs/h7-summary.json` per_period[…].moran.per_k['8'].moran_I. AD 250–300's −0.014
> (raw −0.014108) is correct and unchanged.]

## 2. Three findings

1. **The scaling exponent is not constant over time.** β_within falls from
   **0.70** in the late-Republican/Augustan period to a **~0.58 plateau across
   the high empire (AD 100–250)** — which is exactly the pooled confirmatory
   `β_within = 0.587` (the pooled value is dominated by these inscription-rich
   centuries) — then rises again to **0.66** in the 4th century. Early- and
   late-empire epigraphic production scales *more steeply* with city size than
   the high-empire core; the U-shape is descriptive but striking. (CIs overlap,
   so this is a trend, not a sharp break — read descriptively.)
2. **Provincial capitals over-produce in every period** (P(contrast > 0) = 1.00
   throughout) — the capital effect is temporally stable, not a high-empire
   artefact.
3. **Spatial clustering of residuals is an early-empire phenomenon.** Moran's I
   is significantly positive only in **50 BC – AD 0** (I = +0.029, p = 0.021);
   from AD 0 on it is ~0 / non-significant. Whatever spatial structure Hanson's
   pooled residual map carries is concentrated in the earliest period and washes
   out thereafter.

## 3. Method (recap) + caveats

Same H3a non-centred Mundlak NBR + H3c diagnostics, per period; fixed 1044-city
universe with population-based Mundlak (periods directly comparable); per-period
counts aoristic-apportioned (rounded). Exploratory, no published comparator,
no thresholds. **50-year periods** (not literal decadal — feasibility; finer is a
re-run). Aoristic-rounded counts (midpoint an unrun sensitivity). Sparse early/
late periods sampled fine (gates met).

## 4. Outputs

`outputs/`: `h7-summary.json` (per-period counts, convergence, β_within,
capital contrast, Moran's I per k), `h7-per-city-residuals.parquet` (the
time-resolved residual-map data, per city per period), `h7-time-resolved.png`.
Per-period NBR posteriors (`h7-idata-*.nc`) are on sapphire (gitignored,
regenerable).

## 5. Bottom line

A time-resolved H3c: capitals over-produce throughout, residual spatial
clustering is an early-empire feature only, and the population–epigraphy scaling
exponent traces a U over the four centuries (steeper early/late, ~0.58 across the
high empire). Novel descriptive contribution; no published comparator.
