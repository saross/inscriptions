---
title: "Run spec — RAC-TRAC 2026 talk-prep analysis"
date: 2026-05-21
audience: "Adela (delivering Friday 14:20 Aarhus); session organisers (LIRE creators); TRAC7 audience"
status: "in flight (Block 1 in progress)"
preregistration:
  url: https://osf.io/uycs6/
  lodgement-tag: osf-lodgement-2026-05-20
  embargo: "Currently embargoed pending double-blind journal-submission decision."
---

# Run spec — RAC-TRAC 2026 talk-prep analysis

## Purpose

Produce preliminary, post-lodgement empirical results for a 12-minute conference
talk at TRAC7 (Aarhus, Friday 22 May 2026 14:20), delivered by Adela on Shawn's
behalf. All quantitative slide content must be labelled "preliminary,
post-lodgement; the preregistered analysis is forthcoming."

## Scope

**Primary target (A+)**: Lean-A core (Phase 1 reuse + raw SPAs at empire /
province / city + frequentist Hanson NBR-GLM + mixture-model schematic) **plus**
one synthetic mixture-recovery demo cell **plus** stretch Bayesian H3a
within-between NBR.

**Fallback (lean A)**: drop the Bayesian H3a stretch; if the synthetic mixture
demo over-runs by > 4 hours, drop that too and ship the schematic-only mixture
slide.

## Decision gates

- **Gate 1, hour 18**: Blocks 1–3 done? If not, drop A+ and proceed to slide
  assembly.
- **Gate 2, hour 26**: Block 4 done? If yes, attempt Block 4b; if no, skip 4b.

## Inputs

- LIRE v3.0 parquet (read-only): `archive/data-2026-04-22/LIRE_v3-0.parquet`
  (182,853 rows, 63 attributes, pre-joined Hanson `urban_context_pop_est`).
- Canonical filter implementation reused from
  `runs/2026-05-17-date-range-filtered-spas/code/date_range_filtered_spas.py`
  (`load_filtered_lire()` at lines 167–193).
- 2024 exploratory notebook (reference only):
  `archive/2026-04-22-inscriptions-spa.ipynb`.
- Preregistration: `planning/preregistration-draft.md`.

## Outputs

- `data/lire-filtered.parquet` — 50 BC – AD 350 prereg-filtered corpus
  (180,609 rows expected).
- `outputs/figures/` — empire / province / city SPAs, NBR scaling, mixture
  recovery, H3a comparator (each at 16:9 slide aspect, plus high-DPI variants
  copied to `planning/conference-talk-rac-trac-2026/figures/`).
- `outputs/tables/` — per-block summary CSVs (filter counts, NBR coefficients
  + bootstrap CI, mixture-recovery diagnostics, H3a posterior summaries).
- `outputs/REPORT.md` — narrative summary at end of run.

## Filter (prereg-canonical)

Three predicates intersected with the date envelope:

1. `is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL
   AND not_before IS NOT NULL AND not_after IS NOT NULL
   AND not_before ≤ not_after`
2. `is_within_RE := province IS NOT NULL`
3. Date-window intersect (overlap, not containment) with [50 BC, AD 350]:
   `not_after >= -50 AND not_before <= 350`

Expected post-filter counts (HALT and report if any > 1 % off, per the
critical-friend gate in the analysis roadmap):

| Quantity | Prereg target |
|---|---|
| Total filtered rows | 180,609 |
| Rome-only inscriptions | 65,435 |
| Rome-excluded inscriptions | 115,174 |
| Inscriptions assigned to a Hanson-catalogued city (filtered) | 140,575 |
| Hanson-matched cities (Rome excluded, filtered) | ~ 815 |

## Critical-friend standing rules

- No silent parameter reductions. Halt and report if compute is tight.
- For every statistical choice, ask: more appropriate test? more powerful /
  robust alternative? current best-practice? do the method's assumptions
  actually hold? Surface concerns before executing.
- Every quantitative slide content must be labelled "preliminary,
  post-lodgement; the preregistered analysis is forthcoming."
- Every numerical claim re-checked at write-time against the source dataframe.
  No stale references to old corpus sizes, β values, or city counts.

## Reproducibility

- Project `.venv`: Python 3.13.3, pandas 3.0.2, numpy 2.4.4,
  statsmodels 0.14.6, pymc 5.28.5, matplotlib 3.10.9. Smoke-tested at
  block-1 start (2026-05-21).
- Deterministic seed for all stochastic resampling: `RANDOM_SEED = 20260521`.
- All compute fits on Shawn's local machine. Sapphire is overkill here.

## Out of scope for this run (preregistered Phase 2 / 3 work)

- Full preregistered H2 recovery-grid validation (100-replicate-per-cell).
- H3b deviation-detection at Antonine / Crisis windows.
- H3c Moran's I + provincial-capital contrast.
- §5 small-N city trajectory work (Layers A + B).
- Hanson population-uncertainty sensitivity (σ_pop sweep).
- Letter-count alternative analysis.
- brms shadow validation.
- HMM post-lodgement extension (mention in backup slide B6 only).
