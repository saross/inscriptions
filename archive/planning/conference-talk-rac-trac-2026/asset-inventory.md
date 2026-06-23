---
title: "Asset inventory — RAC-TRAC 2026 conference talk"
date: 2026-05-20 (overnight)
audience: "next-session CC + Shawn"
purpose: "Catalogue every figure, dataset, code module, REPORT, and primitive available for the 12-minute talk."
---

# Asset inventory — RAC-TRAC 2026 conference talk

**TL;DR**: Substantially more is already done than I initially expected. The 2024 exploratory notebook contains the full frequentist Hanson-scaling pipeline (OLS / log-transformed OLS / NBR / NBR-with-bootstrap), province and city SPAs, and the data-cleaning chain. Phase 1 simulation + the three 2026-05-17 diagnostic runs already have publication-grade figures. The main work for tomorrow is **re-running the notebook against the current prereg-compliant filter (50 BC – AD 350; 180,609 rows), producing presentation-quality figures, and assembling the slide deck**. The mixture-recovery synthetic demo is the only genuinely new code we'd write.

---

## 1. Datasets

| Asset | Path | Notes |
|---|---|---|
| **LIRE v3.0 parquet** | `archive/data-2026-04-22/LIRE_v3-0.parquet` | 182,853 rows; 63 attributes; pre-joined Hanson `urban_context_pop_est`. Filter to 180,609 rows with prereg's 50 BC – AD 350 date-window intersect + geotemporal flags. |
| **Hanson 2016 OXREP dataset** | tDAR record 448563 (external) | Already joined into LIRE as `urban_context_pop_est`. No re-download needed. |

## 2. Phase 1 simulation outputs (already publication-grade)

Location: `runs/2026-04-25-h1-simulation/outputs/h1-v2/`

| Asset | Path | Slide use |
|---|---|---|
| Final REPORT | `outputs/h1-v2/REPORT-v2-final.md` | Reference for slide #3 (Phase 1 minimum-N) |
| Threshold table | `outputs/thresholds.parquet` | Source for the minimum-N summary in slide #3 |
| Power-curve figures (per cell) | `outputs/power-curves/empire_*.png`, etc. | Optional inset on slide #3 |
| Heatmaps (detection rate × n) | `outputs/heatmaps/*.png` | Possible slide #3 main figure (or backup) |
| Cell-results table | `outputs/cell-results.parquet` | If we need to recompute anything |

**Status**: locked at OSF lodgement; no rework needed.

## 3. Editorial-distortion diagnostic figures (2026-05-17)

| Run | Path | Slide use |
|---|---|---|
| Interval-width diagnostic | `runs/2026-05-17-interval-width-diagnostic/outputs/figures/`, `REPORT.md` | Slide #2 — editorial-template signature; the 22.8× / 41.5× / 18.8× / 39.7× midpoint ratios; interval-width distribution |
| Empirical SPA shape | `runs/2026-05-17-empirical-spa-shape/outputs/figures/`, `REPORT.md` | Slide #2 main figure — wide-template plateaus + regnal-cluster spikes + BC/AD step |
| Date-range-filtered SPAs | `runs/2026-05-17-date-range-filtered-spas/outputs/figures/`, `REPORT.md` | Slide #2 supporting — narrow-precision filtering reveals real ancient clustering vs editorial encoding |

**Status**: all three runs committed and reproducible. Figures may need cosmetic re-render at presentation aspect ratio (currently print-aspect).

## 4. SPA construction and analysis primitives

Location: `runs/2026-04-25-h1-simulation/code/`

| Module | What it does | Reuse opportunity |
|---|---|---|
| `primitives.py` | Aoristic resampling; per-year SPA construction; 5-year binning; forward-fit nulls (closed-form exponential; per-segment trapezoidal CPL) | Direct reuse for empire / province / city SPAs |
| `forward_fit.py` | Numba-JIT forward-fit primitives | Reused for power-curves and null modelling |
| `h1_sim_v2.py`, `h1_sim.py` | Phase 1 simulation harness | Reference only; not needed for talk |
| `plots.py` | Phase 1 plotting helpers | Adapt for talk figures |

## 5. 2024 exploratory analysis notebook

Location: `archive/2026-04-22-inscriptions-spa.ipynb`

**This is the big find** — the notebook already implements most of what we need for the talk. Cell map:

| Cell range | Content | Slide use |
|---|---|---|
| 0–80 | Data import + cleaning + province-language classification + city aggregation | Reuse for the data-prep stage |
| 81–93 | Descriptive stats + preliminary SPA | Slide #4 — preliminary all-empire SPA |
| 95–132 | Minimum-sample-size investigations (MSSD, Δ T, K-S, bootstrap) | Backup material; partly superseded by Phase 1 simulation |
| 134–139 | SPA at various date-range thresholds + bootstrapped CI | Slide #4 main figure (empire SPA) |
| 141–149 | Major-subset SPAs (Latin-speaking; with / without Roma) | Slide #4 supporting (provincial-aggregate SPA) |
| 150–153 | Per-province SPAs (provinces with ≥ 100 inscriptions) | Slide #4 (province pane) |
| 155–161 | Per-city SPAs (cities with ≥ 100 inscriptions) | Slide #4 (city pane) |
| 163–171 | OLS scaling: inscription count vs Hanson population | Reference for slide #6 |
| 173–185 | Log-transformed OLS, bootstrapped CIs | Reference for slide #6 |
| 186–199 | Negative Binomial Regression (NBR); bootstrap NBR | **Slide #6 main figure** — β + bootstrap CI; comparable to Hanson 2021 β = 0.672 |
| 200–205 | NBR with both variables log-transformed (rejected) | Reference only |
| 207–228 | Alternative models: robust, polynomial, ridge / lasso, GLM comparison | Backup / Q&A reserve |
| 229–232 | Spearman's Rank Correlation | Backup |
| 234–237 | Bayesian Linear Regression (pyro) | **Possible reuse for stretch H3a Bayesian** if time permits |
| 243–247 | NBR with letter counts | Optional supplementary |
| 249+ | More SPA work | Reference |

**Critical filter change**: the 2024 notebook used the full LIRE corpus. The talk needs to apply the prereg's 50 BC – AD 350 date-window filter for the cross-sectional analyses to align with SR1 / SR2. About 1.2 % of inscriptions are filtered out by the date window — should not materially change the headline β but **must be applied for prereg compliance**.

## 6. Preregistration documents

| Asset | Path | Use |
|---|---|---|
| Lodged prereg | `planning/preregistration-draft.md` | Source for confirmatory framing on slide #5 + closing slide |
| OSF supplementary | `planning/osf-supplementary-2026-05-20.pdf` | Sharable handout / link on closing slide |
| Decision log | `planning/decision-log.md` | Reference for methodological choices |
| Lodgement tag | `osf-lodgement-2026-05-20` on `main` | Reproducibility anchor; cite on closing slide |
| OSF DOI | _TBD_ — Shawn lodging now; insert when available | Closing slide |

## 7. brms shadow script

Location: `scripts/h3a_brms_shadow.R`

**Not needed for the talk** (this is the R-side cross-validation of the preregistered H3a Bayesian within-between NBR). Mention only if a stretch goal of fitting the actual preregistered H3a in pymc succeeds and we want to show the shadow concept.

## 8. baorista installation

Location: sapphire compute server; see `runs/2026-05-03-baorista-install/INSTALL-LOG.md`

**Not needed for the talk** unless we want to demonstrate the alternative Bayesian aoristic approach as a comparator. Likely out of scope for 36 hours.

## 9. Tooling

| Tool | Status |
|---|---|
| Python 3.13 venv with pymc, numpy, statsmodels, etc. | `.venv/` ready |
| R 4.4.3 with cmdstanr, brms, baorista, nimble (on sapphire) | Ready (remote) |
| pandoc 3.6.3 (via Quarto) + xelatex | Confirmed working (used for the OSF supplementary PDF) |
| Quarto 1.8.27 for slides | Confirmed installed |

## 10. What's NOT available (and gaps to fill)

| Gap | Mitigation |
|---|---|
| Bayesian within-between NBR (preregistered H3a) | Stretch goal; backup is frequentist NBR |
| Bayesian mixture model fit (H2) | Beyond 36-h scope for the full preregistered version. Synthetic-recovery demo on one cell is the A+ stretch (~4–6 h estimated). |
| Recovery-grid design artefact | Out of scope for this talk; future post-talk work. |
| Template-dictionary scan | Out of scope for this talk. |
| Province-language classification CSV as standalone file | The mapping lives in 2024 notebook cell 54; may want to externalise into a tracked CSV before the talk (low priority). |

## 11. Re-use vs rebuild decisions

| Item | Decision | Rationale |
|---|---|---|
| LIRE data-cleaning chain | **Re-use** notebook cells 0–80 | Working code; just needs date-window filter added |
| Province / city SPAs | **Re-use** notebook cells 141–161, re-render figures at slide aspect | Already implemented |
| Frequentist Hanson scaling | **Re-use** notebook cell 197 (bootstrap NBR), apply date-window filter | The core preliminary result |
| Phase 1 figures | **Re-use** existing PNGs (`runs/2026-04-25-h1-simulation/outputs/`) | Already publication-grade |
| Editorial-distortion figures | **Re-use** the three 2026-05-17 diagnostic-run figures | Already publication-grade |
| Mixture-recovery synthetic demo | **Build new** (A+ stretch) | Lightweight pymc model; one cell of the preregistered recovery grid |
| Bayesian H3a within-between NBR | **Build new** (further stretch) | Approximately the preregistered model in pymc; ~50 LOC |
| Slide deck | **Build new** in Quarto | No prior deck exists |
