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

## Block 2 — Empire / province / city SPAs (pending)

- [ ] `code/02-empire-spa.py`
- [ ] `code/03-province-spa.py`
- [ ] `code/04-city-spa.py`
- [ ] Save figures to `outputs/figures/` and mirror high-DPI to
      `planning/conference-talk-rac-trac-2026/figures/`

## Block 3 — Frequentist Hanson NBR (pending)

- [ ] `code/05-hanson-nbr-bootstrap.py`
- [ ] Save β + bootstrap CI to `outputs/tables/nbr-summary.csv`
- [ ] Save log–log scatter figure

## Gate 1 — Hour 18

A vs A+ decision (see spec.md).

## Block 4 — Mixture-recovery demo (A+ stretch)

- [ ] `code/06-mixture-recovery-synthetic.py`
- [ ] Save recovery figure + diagnostics

## Gate 2 — Hour 26

Bayesian H3a stretch decision.

## Block 4b — Bayesian H3a (further stretch)

- [ ] `code/07-h3a-bayesian-mundlak.py`
- [ ] Save f_within posterior summary

## Block 5 — Slide assembly

- [ ] Populate `planning/conference-talk-rac-trac-2026/slide-outline.qmd`
- [ ] Render revealjs HTML + PDF

## Block 6 — Adela briefing

- [ ] `planning/conference-talk-rac-trac-2026/adela-briefing.md`

## Block 7 — Reproducibility check + commit

- [ ] End-to-end clean-run
- [ ] Final commit batch
