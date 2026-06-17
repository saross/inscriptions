# §5 H5 — empire-wide common temporal component + residual trajectory — RESULTS

*(the analysis preregistered as the "habit-removed residual trajectory"; per the
2026-06-17 framing decision, methods/results name it the **empire-wide common
temporal component**, and the epigraphic-habit interpretation is reserved for §6
Interpretation.)*

- **Status:** COMPLETE (exploratory; Decision 13 / prereg §5; no thresholds).
- **Run:** sapphire, 2026-06-17; deterministic read of the Layer-A posterior
  (no MCMC). `code/h5_habit_removed.py` (+ `code/h5_decomposition.py`); log
  `run.log`.

---

## 1. The decomposition (empirical)

The §5 Layer-A hierarchical model factors each city's log inscription-rate into a
shared temporal shape plus province and city deviations:

`log λ[c,t] = α_g + g_shape[t] + b_u[p] + u_shape[p,t] + b_v[c] + v_shape[c,t]`

- **Empire-wide common temporal component** = `α_g + g_shape[t]` (the time-shape
  shared by all cities).
- **Residual trajectory** = `u_shape[p,t] + v_shape[c,t]` (a city's deviation from
  the empire-common shape).

## 2. The common temporal component peaks AD 187.5

`g_shape` peaks at **AD 187.5** (bin [175, 200) — late-Antonine/Severan).
Figure: `outputs/h5-empire-habit.png`. (Interpretation — its correspondence with
the epigraphic-habit literature and the four candidate causes — in §6.)

## 3. Common-component lag (raw peak vs residual peak)

Per city, lag = peak-year(raw `lam`) − peak-year(residual), draw-wise.

- **Corpus median lag ≈ 0 yr** (all cities and reliable-only), **IQR [0, 50] yr**,
  fraction-positive 0.48.
- **Read:** no *systematic directional* lag in the corpus median, but the common
  component shifts *individual* cities' apparent peaks by up to ~one or two 25-year
  bins. Data-rich (N≥300) cities' own signal dominates (raw ≈ residual peak); the
  confound bites hardest on small-N cities, which partial-pool toward the AD-188
  common shape. Figure: `outputs/h5-habit-lag-hist.png`.

## 4. Magnitude decomposition (empirical)

Comparable log-rate SD units (posterior median; `outputs/h5-decomposition.json`):

| Component | log-rate SD |
|---|---|
| Empire-common temporal swing (`g`) | 1.11 |
| Province temporal (`u`) | 1.02 |
| City-specific temporal (`v`) | 0.98 |
| Between-city LEVEL spread (cross-sectional / population axis) | 0.78 |

- The common temporal component is **≈ 54 %** of a typical city's temporal variance
  and the largest single magnitude among the mid-sized §5 cities. The level/population
  axis (0.78) is **understated by §5 range restriction** (the set excludes the size
  extremes) — level (cross-sectional) and the common component (temporal) are
  different axes, so this is not "timing beats population".
- **Latin-minus-Roma (257/268 cities, the diagnostic unit) ≈ all-provinces**: common
  peak AD 187.5, sd_level 0.785, sd_v 0.975, common share 0.54 — the §5 set is 96 %
  Latin-West, so the diagnostic-unit decomposition is unchanged. The 11 non-Latin
  Greek-East cities peak **earlier (~ AD 112.5)**, level spread 0.52 (n = 11; a flag,
  not a finding).

## 5. Foundation-date terminus validation (empirical)

Hanson `Start Date` matched to all **268 cities**; **99** are founded *within* the
envelope (Start Date > 50 BC) and so bind.

- **Median pre-foundation inscription mass = 0.07 %** — the Layer-A trajectories
  respect foundation termini corpus-wide (the lower-terminus analogue of Pompeii's
  AD-79 upper terminus).
- **Exceptions are frontier military sites:** Corstopitum/Corbridge (Start 200,
  59.4 %), Corinium/Cirencester (100, 30.2 %), Luguvalium/Carlisle (100, 26.8 %),
  Centumcellae (106, 25.8 %), Lauriacum (191, 17.1 %), Argentoratum/Strasbourg
  (80, 16.6 %) — earlier military epigraphy predating the *town's* Barrington
  foundation date. A real signal (military-before-civilian), not a model error.

## 6. Interpretation (discussion — kept separate from §§1–5)

The empire-wide common temporal component is **not** a clean "epigraphic habit". It
is the time-shape all cities share, which conflates four empire-wide drivers
(externalised):

1. the cultural **epigraphic habit** (MacMullen) — and the AD-188 peak does
   correspond to the epigraphic-habit literature and the H3b "hump";
2. empire-wide **demographic/economic** trends (the Antonine apogee);
3. empire-wide **taphonomy/recovery** (period-biased survival/excavation);
4. residual **dating-convention** structure.

§5 Layer A has **no population covariate**, so the decomposition separates
empire-common from city-specific, **not** habit from population; the residual
(city deviation from the empire norm) is the defensible quantity, and a clean habit
removal is not achievable (no external habit proxy exists). See Obs 98. The
principled downstream use is a **habit-removed (residual) Layer B** that inverts the
residual into a population trajectory *relative to the empire trend*.

## 7. Caveats

Exploratory, no thresholds (Decision 13; GPT-5.5 flagged the design fragile — read
descriptively). The common component is the within-sample (268-city) empire shape.
Foundation anchors limited to within-envelope foundations. N\*=300 floor (34/268
reliable). The common-share figure (~54 %) ignores inter-tier covariance.

## 8. Bottom line

The empire-wide common temporal component peaks ~AD 188 and is large (~54 % of a
city's temporal variation); removing it leaves **no systematic corpus lag but real
±50-year per-city shifts** (small-N cities most affected); the trajectories pass a
corpus-wide foundation-terminus check (0.07 %) bar archaeologically-explicable
frontier-military sites; and the Latin-minus-Roma diagnostic unit gives the same
decomposition as all-provinces. What the common component *means* is deferred to
interpretation (§6) — empirically it is a shared time-shape, not a population or
habit measure.
