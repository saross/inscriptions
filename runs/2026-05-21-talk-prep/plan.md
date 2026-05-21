---
title: "Run plan — RAC-TRAC 2026 talk-prep (block log)"
date: 2026-05-21
---

# Run plan — RAC-TRAC 2026 talk-prep

Tracks block-by-block execution against `planning/conference-talk-rac-trac-2026/analysis-roadmap.md`.

## Block 1 — Filter and prep (complete; one flagged decision deferred to Block 3)

- [x] Scaffold run dir
- [x] Smoke-test `.venv` imports (Python 3.13.3, pandas 3.0.2, numpy 2.4.4,
      statsmodels 0.14.6, pymc 5.28.5, matplotlib 3.10.9)
- [x] Write `code/01-filter-and-prep.py` (reuse canonical filter from
      `runs/2026-05-17-date-range-filtered-spas/code/date_range_filtered_spas.py`)
- [x] Produce `data/lire-filtered.parquet` (60.1 MB, 180,609 rows)
- [x] Verify sanity counts against prereg targets — **all four row-level
      counts hit exact**: 180,609 / 65,435 / 115,174 / 140,575
- [x] Log diagnostics to `outputs/tables/filter-counts.csv`

### Block 1 flagged finding (city-grain question, deferred to Block 3)

The prereg's "~815 Hanson-matched cities, Rome-excluded" diverges from the
direct LIRE-parquet count (1,044). Root cause: the prereg number was inherited
from `archive/2026-04-22-inscriptions-spa.ipynb` cell 73, which applies a
`province_language == 'Latin'` filter via a manually-curated mapping in cell
54 — not a column in the LIRE parquet, not in the prereg's text spec. The
prereg's text spec says "all cities with Hanson population estimates, Rome
excluded" (= 1,044). Decision for Block 3:
  (a) broader 1,044-city sample (text-spec faithful);
  (b) narrower Latin-province ~815 sample (number-faithful; requires
      externalising the cell-54 mapping into a tracked CSV);
  (c) report both side-by-side as a sensitivity.

City-grain diagnostics already logged: 1044 / 913 / 729 / 606 / 169 cities
under N≥1 / 2 / 5 / 10 / 100 inscription thresholds, none of which is exactly
815.

## Block 2 — Empire / province / city SPAs (complete)

- [x] `code/02-empire-province-city-spas.py` (single file covering all three)
- [x] Empire SPA / 8-province SPA / 8-city SPA at 16:9, mirrored to talk dir

## Block 3 — Frequentist Hanson NBR (complete)

- [x] `code/03-hanson-nbr-bootstrap.py`
- [x] β = 0.566, bootstrap 95% CI [0.543, 0.574]; OLS log-log β = 0.284 (R² = 0.036)

## Gate 1 — Hour 18 (passed)

A+ green-light: Blocks 1–3 complete; proceeded to Block 4.

## Block 4 — Mixture-recovery demo (complete on sapphire)

- [x] `code/04-mixture-recovery-synthetic.py`
- [x] α posterior covers truth (median 0.477, 95% CI [0.414, 0.541]); Pearson r = 1.000 vs truth; R̂ = 1.0000; ESS ≥ 2,567; all prereg gates pass.
- Sampled in 2s on sapphire (native-C pytensor); local lacks python3-dev.

## Gate 2 — Hour 26 (passed)

Bayesian H3a stretch green-light.

## Block 4b — Bayesian H3a (complete on sapphire)

- [x] `code/05-h3a-bayesian-mundlak.py`
- [x] β_within = 0.587 (close to Carleton 2025 no-zeros 0.68); β_between ≈ −0.26 with wide CI (not separately identifiable).
- [x] **f_within = 0.299, 95% CI [0.240, 0.366]; verdict SUPPORTED.** P(f > 0.20) ≈ 1.000.
- [x] Refit with tune=3,000 (initial tune=1,000 yielded R-hat = 1.0100 exactly at gate); refit gives R-hat = 1.0000.

## Block 5 — Slide assembly (complete)

- [x] Populated `planning/conference-talk-rac-trac-2026/slide-outline.qmd` with all 6 new figures + numerical β / f_within
- [x] Added new slide 6b for the Mundlak f_within result (8 main slides + 6 backups now)
- [x] Wired in slide-2 figures (`fig-02a-empirical-spa.png`, `fig-02b-width-histogram.png`) from `runs/2026-05-17-*/` and slide-3 figure (`fig-03-phase1-heatmap.png`) from `runs/2026-04-25-h1-simulation/`
- [x] Rendered Quarto revealjs HTML (`slide-outline.html`, 6.7 MB self-contained)
- [x] Rendered slide-format PDF via Decktape + Brave (`slide-outline-slides.pdf`, 2.1 MB, 10 landscape pages)
- [x] Rendered LaTeX paper-document PDF (`slide-outline.pdf`, 1.8 MB, 11 letter pages) as text-content backup
- [x] Iteratively QA'd all 10 slides; applied `smaller: true` globally + per-slide content trims to fit content
- [x] Fixed title-slide "Invalid Date" (ISO + date-format: long) and empty-slide-from-orphan-comment bug

## Block 6 — Adela briefing (complete)

- [x] `planning/conference-talk-rac-trac-2026/adela-briefing.md` — slide-by-slide cheat sheet + 9 anticipated Q&A + backup-slide map + tone-framing + escape-pattern for unknown questions

## Block 7 — Reproducibility check + commit (in progress)

- [x] All scripts ran end-to-end against the cached parquet (Blocks 1-4b)
- [x] Sapphire venv reproducible from pyproject.toml
- [x] Decktape tool at `~/tools/decktape/` (outside repo; PUPPETEER_EXECUTABLE_PATH=/usr/bin/brave-browser)
- [ ] Final commit + push pending
