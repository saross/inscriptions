# §5 H7 — per-period (time-resolved) H3c (SPEC)

- **Status:** spec + run (Shawn authorised launch 2026-06-17). Exploratory
  (prereg §5 line 384: "extend Hanson's (2021) time-pooled residual analysis by
  computing residuals per decadal period. Exploratory because no published
  comparator exists.").
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-17.
- **Run dir:** `runs/2026-06-17-s5-h7-perperiod-h3c/`.

---

## 1. What H7 is

H3c (pooled, already run) computes Pearson residuals from the H3a NBR and tests
(i) whether provincial capitals over-produce inscriptions and (ii) whether the
residuals cluster spatially (Moran's I). H7 recomputes **the same two diagnostics
within each time period**, yielding a *time-resolved* version of Hanson's 2021
residual map — does capital over-production / spatial clustering strengthen or
weaken across the 1st–4th centuries?

## 2. Method — reuse the H3a/H3c machinery, per period

For each time period, hold the **city universe and Mundlak split fixed** (the
1044 Hanson-matched, Rome-excluded cities from `city_level_for_h3a.parquet`; the
within/between predictors are population-based, so identical across periods), and
**replace `inscription_count` with the per-period count**:

1. Per-period counts via **aoristic apportionment** (spread each inscription's
   `[not_before, not_after]` mass across the periods its interval covers, clipped
   to the envelope), summed per city, **rounded to integer** for the NBR. Cities
   absent in a period enter as structural zeros.
2. Re-fit the H3a non-centred Mundlak NBR (`build_model`, replicated verbatim
   from `runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py`).
3. Pearson residuals (same formula as `04-h3c.py`).
4. **H3c(i)** provincial-capital contrast: `P(mean r|capital − mean r|non > 0)`
   (capitals from `data/processed/provincial-capitals.csv`).
5. **H3c(ii)** Moran's I on the posterior-mean residual, k ∈ {5, 8, 10}
   (libpysal KNN + esda Moran, as `04-h3c.py`).

Recorded per period: counts, convergence, β_within (the scaling exponent *over
time* — a bonus byproduct), capital-contrast P(>0), Moran's I + p per k.

## 3. Design decisions (made + documented; Shawn can redirect — re-runnable)

- **(i) Time resolution = 50-year periods (8 bins over 50 BC–AD 350).** The
  prereg says "per decadal"; literal decades (40 bins) collapse the province
  random intercepts and leave too few inscriptions per city per period for an
  NBR. 50-year bins keep **420–768 non-zero cities per period** (verified live
  from the corpus) — feasible and still time-resolved. *This departs from the
  literal "decadal"; flagged for Shawn.* (Finer resolution is a re-run.)
- **(ii) Count construction = aoristic-apportioned, rounded to integer.**
  Faithful to the paper's aoristic philosophy (midpoint hard-assignment would
  bin the round-number "slab" inscriptions at their centre — exactly the bias the
  paper critiques). Rounding thin mass to 0 is the cost; midpoint assignment is
  an unrun sensitivity.
- **(iii) Fixed city universe + Mundlak across periods.** All 1044 cities every
  period (zeros where absent); the within/between predictors are population-based
  (unchanged), so the per-period residual maps are directly comparable. (The
  alternative — restrict to non-zero cities + recompute Mundlak per period —
  would make periods non-comparable.)
- **(iv) Sampler = tune 3000 / draws 2000 / 4 chains / target_accept 0.95**
  (lighter than the confirmatory 6000/3000 — this is exploratory, ×8 fits, and
  the NBR is simple). Same gates reported (R̂<1.01, ESS≥400, 0 div); **warn, not
  halt**, per period so all 8 complete and convergence is visible.

## 4. Inputs

- `data/processed/city_level_for_h3a.parquet` (1044 cities; Mundlak predictors,
  province_idx, coords) — fixed universe.
- Raw LIRE `archive/data-2026-04-22/LIRE_v3-0.parquet` via the H3a filter
  (`h3a_common.load_filtered_lire` + Rome/Hanson masks) — for per-period counts.
- `data/processed/provincial-capitals.csv` (OXREP capitals).

## 5. Deliverables

`outputs/`: `h7-summary.json` (per-period: counts, convergence, β_within,
capital-contrast P(>0), Moran's I per k), `h7-per-city-residuals.parquet`
(per-period posterior-mean residual per city — the time-resolved map data), and
figures (Moran's I over time; capital-contrast over time; β_within over time).

## 6. Caveats

- Exploratory, no thresholds; no published comparator (prereg).
- 50y ≠ literal decadal (design decision i).
- Aoristic rounding (design decision ii).
- Sparse early/late periods (bins 0, 7) may pool province intercepts hard;
  convergence reported per period.

## 7. Compute

Sapphire; 8 NBR fits (MCMC) sequentially — background run, ~tens of minutes.
