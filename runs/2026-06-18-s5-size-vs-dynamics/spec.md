# §5 size-vs-dynamics probe — does city size predict city-specific temporal dynamics? (SPEC, pre-launch)

- **Status:** DRAFT — awaiting Shawn's pre-launch sign-off. **Do not execute
  until the sign-off checklist (§9) is ticked.**
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-18, on Shawn's brief.
- **Run dir:** `runs/2026-06-18-s5-size-vs-dynamics/`.
- **Type:** Exploratory (Decision 13; prereg §5). **No pre-committed thresholds;
  descriptive.** A null is an informative result here (see §7).
- **Origin:** the reframe of Shawn's "can we compare the isolated city-level
  effect to Hanson?" question (user-obs 43): a direct `q_v`-vs-Hanson overlay is
  a category mismatch (level-free shape vs static level), but the well-posed
  question next to it is whether **city size predicts city-specific dynamics**.
- **Estimated effort:** minutes (deterministic read of the §5 Layer-A posterior
  + the residual Layer-B construction + a bootstrap; no MCMC).

---

## 1. The question, made precise

The residual Layer B isolated the city-specific temporal trajectory
`q_v[c,t] = exp((1/β)·v_shape[c,t])` (city-from-province; province and empire
removed). It is a **level-free temporal shape** (geom-mean 1). Hanson's
`pop_est` is a **static city-level size**. They are not directly comparable
(different axes; the city-*level*-vs-Hanson comparison is H3a, already the
headline scaling law). The well-posed question is cross-city:

> **Does a city's size (Hanson `pop_est`) predict features of its city-specific
> temporal trajectory** — does it sit higher relative to its province late, is it
> less volatile, does it peak later?

Primary tier **`q_v`** (city-from-province, Shawn's "isolated from province and
empire"); secondary tier **`q_uv`** (city-from-empire) reported alongside.

**Why this is legitimate (non-circular).** §5 Layer A carries **no population
covariate** (Obs 98), so `v_shape` (hence `q_v`) is estimated entirely
Hanson-free; β is a single global constant that rescales amplitude uniformly.
Hanson enters **only** as the independent predictor. For *rank* statistics the
1/β inversion is monotone and city-constant, so Spearman(`q_v` feature, pop) =
Spearman(`v_shape` feature, pop) — the inversion is cosmetic; we compute on the
population-interpretable `q_v` and report in those terms.

---

## 2. Inputs (re-verified this session)

| Input | Source (verified) | Notes |
|---|---|---|
| `v_shape`, `u_shape` posterior draws | `runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc` (on sapphire) | via `h5.load_posterior` (8,000 draws, 268 cities, 16 bins). |
| β posterior (empire primary; Latin sensitivity) | `runs/2026-06-04-h3a-confirmatory/outputs/idata-{primary,latin}.nc` | via `lb.load_beta_draws`. For rank stats β is cosmetic; carried for the slope magnitudes. |
| City size **`pop_est`** | `runs/2026-05-30-s5-small-n-trajectories/code/prepared/city-index.parquet`, column **`pop_est`** (NOT `urban_context_pop_est` — that name in the raw Layer B spec was stale; the project reads `pop_est` from the index) | 268 §5 cities all populated. |

**Predictor distribution (the 34 reliable §5 cities, verified):** `pop_est`
**[1,000, 153,722]**, median 5,888, IQR [2,601, 15,829] — **2.19 decades** of
log₁₀ range (the full 1,012-city index spans 2.61), across **19 provinces**.
Modest range restriction; the binding limit is **n = 34**.

---

## 3. Features (per city, from the `q_v` draws)

Headline (robust, mid-bins only — envelope-edge bins 0–1 / 14–15 are excluded
throughout because GRW endpoint variance inflates them; bin centres: AD 112 =
bin 6, AD 188 = bin 9, AD 262 = bin 12):

- **F1 — late level relative to province:** `q_v[AD 262]` (bin 12). *Are larger
  cities sustained, relative to their province, into the 3rd century?*
- **F2 — volatility:** SD over the mid bins (2–13) of `log q_v`. *Are larger
  cities smoother / less volatile relative to their province?*

Secondary (reported, flagged, not headline):

- **F3 — late-vs-early tilt:** `log q_v[AD 262] − log q_v[AD 112]`. (An
  alternative "decline" reading to F1.)
- **F4 — peak timing:** modal argmax bin. **Edge-contaminated** (11/34 reliable
  cities peak at an envelope edge); reported with that caveat only.

---

## 4. Method (draw-wise + city-bootstrap; both uncertainties surfaced)

**Primary statistic — Spearman rank correlation** between each feature and
`log₁₀ pop_est` across the 34 reliable cities (rank-based ⇒ robust to single-city
log-space leverage — the Obs 94 lesson, where a naïve OLS slope was a Pompeii
artefact). Reported with **two** uncertainty sources, kept distinct:

1. **City-bootstrap CI (sampling uncertainty — the binding one at n = 34):**
   resample the 34 cities with replacement (seeded), recompute ρ on the
   posterior-median feature; report median ρ, 95 % CI, and the bootstrap
   P(ρ > 0) / P(ρ < 0).
2. **Draw-wise ρ posterior (trajectory uncertainty):** for each of the 8,000
   posterior draws, compute the feature for all cities and ρ; report the ρ
   posterior median + 95 % band. This shows whether the `v_shape` posterior
   spread alone would wash out any signal.

**Secondary — magnitude:** OLS slope **and** Theil-Sen (robust) slope of the
feature on `log₁₀ pop_est`, on the median features, with a city-bootstrap CI.
Report both; divergence flags leverage (Obs 94).

**Tiers / samples:** `q_v` primary + `q_uv` secondary; 34 reliable primary +
**268 all-cities as a flagged sensitivity** (trajectories uncalibrated below
N\*=300, so secondary only).

No thresholds (Decision 13): report ρ, CI, and P(sign) for every
feature × tier × sample and read descriptively — explicitly **without**
cherry-picking the largest (multiple features × tiers × samples = a small
multiple-comparison surface; all are reported together).

---

## 5. Deliverables

1. `outputs/size-vs-dynamics-summary.json` — per feature × tier × sample: median
   ρ, bootstrap 95 % CI, P(sign); draw-wise ρ band; OLS + Theil-Sen slopes + CIs;
   the predictor range; seeds; input sha256.
2. Figures: scatter of each headline feature (median) vs `log₁₀ pop_est` for the
   34 reliable cities, with the Theil-Sen fit and ρ annotated; a small panel of
   the draw-wise ρ posteriors.
3. `REPORT.md` — the precise question (§1), the non-circularity argument, results
   read descriptively, and the §7 caveats carried verbatim.

---

## 6. Code plan

`code/size_vs_dynamics.py`, reusing the audited loaders:
- `h5.load_posterior` (v_shape, u_shape, cities) + the residual construction
  (`r_v`, `r_uv`) from the residual Layer B; `lb.load_beta_draws`.
- `pop_est` join from `city-index.parquet`.
- `features(q)` → F1–F4; `spearman_bootstrap(...)`, `drawwise_rho(...)`,
  `slopes(...)`; `plots(...)`.
- Seeds fixed; input sha256 recorded. `/audit` (or focused review) before launch.

---

## 7. Caveats (carry into the write-up — several are load-bearing)

1. **Low power.** n = 34 cities; a correlation needs |ρ| ≳ 0.34 to clear a 95 %
   bound at this n. **A null is fully expected and is itself informative**
   (coheres with the Obs 100 range-restriction finding) — this probe can
   *suggest*, not establish.
2. **Not pure demography (Obs 98).** `v_shape` carries city-level taphonomy,
   economy, and habit too; a "larger cities sustained later" result would **not**
   be cleanly demographic — it is "size predicts the city-specific signal",
   whatever that signal's drivers.
3. **Range restriction (Obs 100).** 2.19 decades among small-N targets; a real
   size-dynamics relationship could be muted purely by the narrow range.
4. **Multiple comparisons.** Several features × tiers × samples; report all, no
   threshold, no cherry-pick.
5. **Inversion cosmetic for rank stats** (§1) — the rank result is a property of
   `v_shape`; the population framing is interpretive.
6. **Edge bins excluded** from features (GRW endpoint variance, §3).

---

## 8. Compute

Sapphire (inputs staged there); deterministic transform + bootstrap — minutes, no
MCMC, **no API spend** (flagged for the API gate: CPU only). Reproducible
(seeds + input sha256).

---

## 9. Pre-launch sign-off checklist (Shawn)

- [x] **(i)** Features: F1 late-level + F2 volatility headline; F3 tilt / F4 peak
  secondary-flagged — confirmed 2026-06-18.
- [x] **(ii)** Tiers: `q_v` primary + `q_uv` secondary — confirmed 2026-06-18.
- [x] **(iii)** Method: Spearman primary (city-bootstrap CI) + draw-wise ρ
  posterior + OLS/Theil-Sen slopes — confirmed-by-default 2026-06-18 (methods
  rigour; not a substantive fork).
- [x] **(iv)** Sample: 34 reliable primary + 268 flagged sensitivity — confirmed
  2026-06-18.
- [x] Run script `code/size_vs_dynamics.py` written + focused-reviewed
  (2026-06-18: reuses the audited residual-B machinery; review tightened the
  β-invariance claim — exact for draw-wise ρ, near-invariant for the bootstrap).
- [x] Final sign-off to launch — Shawn, 2026-06-18. Running on sapphire.
