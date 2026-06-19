# Amendment 01 §A5.4 content residual (inter-measure delta) — SPEC

- **Status:** EXECUTED 2026-06-20 (the pre-specified A01 §A5.4 derived quantity;
  closes the one outstanding analytical preregistration item per the
  `planning/prereg-obligations-coverage-sweep-2026-06-20.md` sweep, item AM01-d).
  Results in `REPORT.md`.
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-20, on Shawn's
  pre-write-up uplift brief.
- **Run dir:** `runs/2026-06-20-a01-content-residual/`.
- **Type:** **Exploratory / DESCRIPTIVE.** Amendment 01 §A5.4 is explicit: "No
  pre-committed threshold and no confirmatory verdict attach to the delta." This
  run has **no pass/fail gate** — the deliverable is a map and a cross-tab read
  descriptively.

---

## 1. The pre-specified analysis (Amendment 01 §A5.4, verbatim)

> **Definition.** For the cross-sectional city set, fit `log(letter_mass) ~
> log(inscription_count)` across cities; the per-city residual is the content
> residual (positive = more content per act than the corpus norm; negative =
> less). The project thereby has a **two-dimensional residual space**: scaling
> residual (observed inscriptions minus what population predicts) × content
> residual (observed content minus what inscription count predicts).
>
> **Status.** Exploratory and descriptive. **No pre-committed threshold and no
> confirmatory verdict** attach to the delta; it is a novel quantity and is
> reported as a map/descriptive characterisation and cross-tabulated against the
> scaling residual.

The definition is unambiguous (re-read at source,
`planning/osf-amendment-2026-05-29-two-measure-framework.md:256–271`): one OLS
fit, one per-city residual, one two-dimensional residual space, cross-tabulated
against the scaling residual. No data is needed beyond the cross-sectional
city frame and the D12 scaling residual.

---

## 2. The cross-sectional city set (the frame)

The lodged primary cross-sectional frame is the **Latin-speaking provinces**
(OSF Amendment 02; Decision 36) — 817 cities, 39 provinces. The content residual
and the scaling residual are computed on this **same** Latin city set, so the
two-dimensional residual space is internally coherent (one residual pair per
city). The empire-wide (1,044-city) frame is built **alongside** as a secondary
/ context panel.

**Note on the scaling-residual frame.** The persisted D12 scaling residual
(`runs/2026-06-16-s5-sensitivities/`) was computed on the all-provinces
1,044-city frame and persists only the **aggregate** pooled-fit JSON (not
per-city residuals). To cross-tabulate against the content residual on the same
cities, this run **recomputes the D12 SAMOC scaling residual on each frame**
(Latin + empire), using the D12 construction byte-for-byte. The empire-frame
recompute is the cross-check: its pooled β reproduces the persisted D12
all-provinces β (see REPORT §1).

---

## 3. Inputs (regenerated from raw; never read from a prior result)

| Input | Source (verified) | Notes |
|---|---|---|
| Per-city `letter_mass` + `inscription_count` | regenerated from raw LIRE v3.0 via the audited H9 machinery (`runs/2026-06-18-h9-letter-mass-h3a/code/h9_common.py`) | `letter_mass` = summed Latin-A–Z `letter_count_conservative` (Amendment 01 §A5.1); `inscription_count` = the city's date-window-filtered, Hanson-matched, Rome-excluded row count. Both built together for the same cities ⇒ the content-residual fit needs no join. |
| Per-city `log_pop` (Hanson population) | carried in the same H9 frame | the scaling-residual predictor. |
| Scaling-residual construction | `runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py` | pooled NBR power-law `insc ~ NB(exp(a + β·log_pop), φ)`, then `r_c = log(insc_c) − (â + β̂·log_pop_c)` on posterior medians. |
| Raw LIRE | `archive/data-2026-04-22/LIRE_v3-0.parquet` | SHA-256 recorded in the results JSON. |

The H9 row-level sanity gate (180,609 filtered rows; 65,435 Rome; 115,174
Rome-excluded; 140,575 Hanson-assigned) **HARD-STOPs** the run if the filtered
LIRE diverges from the prereg targets, so the frame is provably the lodged one.

---

## 4. Method

1. **Content residual (A01 §A5.4):** OLS `log(letter_mass) ~
   log(inscription_count)` across cities; the per-city residual is the content
   residual. Cities with `letter_mass == 0` (inscriptions present but no readable
   Latin A–Z letters) have an undefined `log(letter_mass)` and are dropped from
   the fit (count reported) — the same treatment H9's OLS log-log comparator
   applies.
2. **Scaling residual (D12 SAMOC):** the pooled-NBR log residual, recomputed on
   each frame.
3. **Cross-tab:** quadrant counts at the sign split of each residual (both are
   mean-~0 by construction), plus the Spearman and Pearson association between
   the two residuals (on cities present in both — `letter_mass > 0`).
4. **Map:** the two-dimensional residual-space scatter (scaling × content),
   Latin primary + empire context panels.

---

## 5. Deliverables

1. `outputs/content-residual-results.json` — OLS fit, per-frame residual
   summaries, the cross-tab (quadrant counts + Spearman/Pearson), seed, input
   sha256, provenance.
2. `outputs/content-residual-per-city.csv` — per-city Latin-frame residual pair
   + quadrant.
3. `outputs/content-residual-space-map.png` — the 2-D residual-space map.
4. `REPORT.md` — the definition, the two residuals, the cross-tab, the map, read
   descriptively (no verdict).

---

## 6. Self-check / guards

1. **Row-level prereg gate** (above) — HARD-STOP if the filtered LIRE diverges.
2. **D12 reproduction cross-check** — the empire-frame pooled β must reproduce
   the persisted D12 all-provinces β (`d12-scaling-residual-results.json`,
   `stage1_pooled_scaling.beta_median` = 0.5654) to within MCMC noise. This is
   the guard that the scaling-residual construction here is the canonical D12 one.
3. **OLS residual mean ≈ 0** — the content residual is mean-centred by OLS
   construction (a sanity assertion on the fit).

---

## 7. Caveats (carry into the write-up)

1. **Descriptive only.** No threshold, no verdict (A01 §A5.4). The deliverable is
   the map + the cross-tab read-off; it cannot change any confirmatory result.
2. **Zero-mass cities dropped from the content-residual fit** (no readable Latin
   A–Z letters); reported, not imputed.
3. **The scaling residual is recomputed per frame** so the residual space is
   coherent within a frame; the persisted D12 is the all-provinces aggregate fit
   and is the cross-check, not the source.
4. **The two residuals are by construction near-orthogonal predictors** — the
   content residual is a *per-act content* signal (letters/act) and the scaling
   residual is a *per-population act* signal (acts/person); they answer different
   questions. Any read of the cross-tab is descriptive characterisation.

---

## 8. Compute

Local (zbook-ubuntu); CPU only; **no API spend**. The only stochastic step is
the small pooled-NBR scaling-residual fit (3 parameters), run under pytensor's
pure-Python backend (this host lacks the Python development headers for the C
backend; the model is tiny so this is a non-issue). Reproducible (seed + input
sha256). Wall-clock ~13 s.

---

## 9. Verdict logic

**None — descriptive.** A01 §A5.4 pre-commits to no threshold and no verdict.
The run reports the OLS fit, the residual space, and the cross-tab as a
characterisation. The one substantive read available is whether the two
residuals are **associated** (a city that over-produces *acts* for its
population also over-produces *content* per act) or **orthogonal** (the two
over-production channels are independent) — reported descriptively, not as a
pass/fail.
