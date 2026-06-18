# §5 province-size regression — is the size–buffering gradient PROVINCE-mediated? (SPEC)

- **Status:** EXECUTED 2026-06-18 (pre-authorised background follow-up; design
  signed off in the brief — proceed-to-run granted). Results in `REPORT.md`.
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-18, on Shawn's brief.
- **Run dir:** `runs/2026-06-18-province-size-regression/`.
- **Type:** Exploratory (Decision 13; preregistration §5). **No pre-committed
  thresholds; descriptive.** A null is an informative result here (see §7).
- **Origin:** the direct test of the province-mediation **inference** in Obs 104.
  The city-level size-vs-dynamics probe
  (`runs/2026-06-18-s5-size-vs-dynamics/`, Obs 104) found the "bigger cities are
  more buffered" gradient is **much stronger on `q_uv` (city-from-empire) than on
  `q_v` (city-from-province)**, and *inferred* — from the `q_uv ≫ q_v` gap, since
  `q_uv = q_u · q_v` — that the relationship operates mainly at the **province
  tier**. That was an inference (REPORT §5 / Obs 104 caveat: "Province-mediation
  is an inference … not a direct province-size regression"). This run regresses
  the **province-from-empire** trajectory features (`q_u`) directly on **province
  size**, which **confirms** province-mediation directly — or fails to.
- **Estimated effort:** minutes (deterministic read of the §5 Layer-A posterior +
  a province-level bootstrap; no MCMC; no API spend — CPU only).

---

## 1. The question, made precise

The residual Layer B decomposition (Obs 103) gives the nested divergence triple
per draw: `q_uv = q_u · q_v`, where

- `q_u[p,t] = exp( (1/β) · u_shape[p,t] )` — **province-from-empire** (how much a
  province deviates from the empire-wide common trend; geom-mean 1 over `t`);
- `q_v[c,t]` — city-from-province; `q_uv[c,t]` — city-from-empire.

Obs 104 showed the size–buffering gradient lives mostly in the `q_u` (province)
factor. The direct test of that is:

> **Does a province's size predict features of its province-from-empire
> trajectory `q_u`** — does a larger province sit higher relative to the empire
> late, is it less volatile, does it decline less (shallower tilt)?

If yes (F1 +, F2 −, F3 +), province size **directly predicts** province-tier
buffering ⇒ the Obs 104 `q_uv ≫ q_v` inference is **confirmed**. If null, the
inference is **not directly corroborated** at province level (the size signal
could instead enter through a city-membership channel — e.g. large provinces
happening to contain the buffered cities — rather than the province trajectory
itself); we say so plainly.

**Unit = PROVINCE** (not city). `q_u` is **constant within a province** (every
city of a province shares the same `u_shape` row), so the city-level probe could
not see the province trajectory cleanly — one province contributes one `q_u`
series, not one-per-member-city. This run uses the **province** as the unit:
one `q_u` series per non-singleton province, regressed on **province size**.

---

## 2. Inputs (re-verified this session, on sapphire)

| Input | Source (verified) | Notes |
|---|---|---|
| `u_shape` posterior draws `(S, P, T)` | `runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc` (sapphire-only, 1.2 GB) | via `h5.load_posterior` → `u`; **S = 8,000** (4 chains × 2,000), **P = 35** non-singleton provinces, **T = 16** bins. Province names from the `prov` coord. |
| β posterior (empire) | `runs/2026-06-04-h3a-confirmatory/outputs/idata-primary.nc` | via `lb.load_beta_draws("empire")`. For *rank* stats β is cosmetic (monotone per-draw rescale); carried for the slope magnitudes (empire-β units). |
| Province size **`pop_est`** | `runs/2026-05-30-s5-small-n-trajectories/code/prepared/city-index.parquet`, column **`pop_est`**, aggregated over **all cities of the province in the FULL 1,012-city index** | NOT just the 268 §5 cities — using only the §5 subset would undercount provinces with held-out large cities. Columns verified: `city, province, pop_est, N, bucket`; 0 NaN `pop_est`. |

**Province join (VERIFIED, see §9-check):** all **35** `u_shape` `prov` coords
match a `province` value in the full index **exactly** (0 unmatched). The full
index has 56 distinct provinces; the 21 extras are singleton/below-threshold
provinces with no u-tier (correctly excluded).

**Predictor distribution (35 non-singleton provinces, `pop_est` summed over all
member cities in the full index, verified):** sum-`pop_est` ∈ **[10,868;
645,931]**, **1.77 log₁₀ decades** of range; member-city count per province
4 / 19 / 70 (min / median / max).

---

## 3. Features (per province, from the `q_u` draws)

Computed `q_u[s,p,t] = exp( (1/β_s) · u_shape[s,p,t] )` directly from `u_shape`
(S, P, T) — **one series per province**, not the per-city broadcast (that just
duplicates within province). Mid-bins only (envelope edges 0–1 / 14–15 excluded
throughout — GRW endpoint variance; bin centres: AD 112 = bin 6, AD 262 = bin
12):

- **F1 — late level relative to empire:** `q_u[AD 262]` (bin 12). *Does a larger
  province sit higher relative to the empire trend into the 3rd century?*
- **F2 — volatility:** SD over mid bins 2–13 of `log q_u`. *Are larger provinces
  smoother / less volatile relative to the empire?*
- **F3 — late-vs-early tilt:** `log q_u[AD 262] − log q_u[AD 112]`. *Do larger
  provinces show a shallower early-to-late decline?*

"More buffered" = **F1 higher, F2 lower, F3 higher** (identical orientation to
the city probe). Primary = **sum** province size; sensitivities = **mean**, **max**.

---

## 4. Method (draw-wise + province-bootstrap; both uncertainties surfaced)

Identical machinery to the parent city probe (`size_vs_dynamics.py`).

**Primary statistic — Spearman rank correlation** between each feature and
`log₁₀ province-size` across the non-singleton provinces (rank-based ⇒ robust to
single-province log-space leverage — the Obs 94 lesson). Two uncertainty sources,
kept distinct:

1. **Province-bootstrap CI (sampling uncertainty — the binding one):** resample
   the provinces with replacement (seeded), recompute ρ on the posterior-median
   feature; report median ρ, 95 % CI, bootstrap P(ρ > 0) / P(ρ < 0).
2. **Draw-wise ρ posterior (trajectory uncertainty):** for each of the 8,000
   posterior draws compute the feature for all provinces and ρ; report the ρ
   posterior median + 95 % band.

**Secondary — magnitude:** OLS slope **and** Theil-Sen (robust) slope of the
feature on `log₁₀ size`, on the median features, with a province-bootstrap CI.
Divergence flags leverage (Obs 94).

**β-frame invariance.** As in the parent probe, for a fixed draw
`q_u = exp((1/β)·u_shape)` is a monotone, province-constant rescaling of
`u_shape`, so every feature's across-province RANK — hence the per-draw Spearman
ρ — is *exactly* identical under empire or Latin β. We compute with empire β; the
draw-wise ρ carries to Latin unchanged. Only slope *magnitudes* are in empire-β
units.

**Non-circular.** §5 Layer A carries no population covariate (Obs 98), so
`u_shape` (hence `q_u`) is Hanson-free; size enters only as the independent
predictor.

**Province set / samples:**

- **Primary:** all **35** non-singleton provinces.
- **Sensitivity:** the **20** provinces containing ≥ 1 reliable (N ≥ 300) city.
  **Flagged explicitly:** province-tier reliability was **NOT** separately
  calibrated — the N\* = 300 floor is a **per-city** reliability threshold (Obs
  100); "province contains a reliable city" is a coarse proxy, not a province-tier
  calibration. Province `u_shape` is itself partial-pooled and may be weakly
  identified for provinces with few/small member cities.

No thresholds (Decision 13): report ρ, CI, P(sign) for every feature ×
size-aggregate × sample, read descriptively, no cherry-pick (a small
multiple-comparison surface; all reported together).

---

## 5. Deliverables

1. `outputs/province-size-regression-summary.json` — per feature × size-aggregate
   × sample: median ρ, bootstrap 95 % CI, P(sign); draw-wise ρ band; OLS +
   Theil-Sen slopes + CIs; the predictor range; the province join result; the
   self-check result; seeds; input sha256.
2. Figures: scatter of each feature (median) vs `log₁₀ sum-pop_est` for the 35
   provinces, with the Theil-Sen fit and ρ annotated; a draw-wise ρ posterior panel.
3. `REPORT.md` — the precise question (§1), the province join, the self-check, the
   results read descriptively, the verdict, and the §7 caveats carried verbatim.

---

## 6. Self-check (before trusting any output)

Two guards, run before producing deliverables:

1. **q_u is constant within province.** If `q_u` is ever broadcast to cities, the
   per-city values within a province must be identical (assertion).
2. **Direct `u_shape` inversion reproduces the residual Layer B.** Computing
   `q_u` directly from `u_shape` (S, P, T) at **empire β** and the **same seed**
   (SEED = 20260616), then broadcasting to a spot province's cities and taking the
   per-draw median, must reproduce the residual Layer B's persisted `q_u_med`
   (`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-empire.nc`,
   var `q_u_med`) **to floating point** for those cities. (The residual nc inverted
   the per-city broadcast `r_u`; since `exp((1/β)·r)` is elementwise per draw,
   broadcasting before vs after inversion is identical for matched draws ⇒ the
   medians match to ~1e-12.)

---

## 7. Caveats (carry into the write-up — several are load-bearing)

1. **Very low power.** n ≈ 35 provinces (≈ 20 in the reliable subset); a
   correlation needs |ρ| ≳ 0.33 (n = 35) / ≳ 0.44 (n = 20) to clear a 95 % bound.
   **A null is fully expected and is itself informative.** This probe can
   *suggest / corroborate*, not establish.
2. **Province-tier reliability NOT calibrated.** The N\* = 300 floor is per-city
   (Obs 100); the "contains a reliable city" subset is a coarse proxy. Province
   `u_shape` for small/few-member provinces is weakly identified.
3. **Not pure demography (Obs 98).** `u_shape` carries provincial-scale taphonomy,
   economy, and habit too; a "larger provinces buffered" result is "size predicts
   the province-specific signal", not demonstrated demographic buffering.
4. **Range restriction.** 1.77 log₁₀ decades of province-size range.
5. **Inversion cosmetic for rank stats** (§4) — the rank result is a property of
   `u_shape`; the population framing is interpretive.
6. **Edge bins excluded** from features (GRW endpoint variance, §3).
7. **Aggregation choice.** Province size = sum-`pop_est` primary; mean / max as
   sensitivities. Sum tracks total provincial urban population; mean tracks the
   typical city; max tracks the dominant city. Reported together.

---

## 8. Compute

Sapphire (the monolithic `.nc` with `u_shape` draws is sapphire-only, 1.2 GB);
deterministic transform + bootstrap — minutes, no MCMC, **no API spend** (CPU
only). Reproducible (seeds + input sha256).

---

## 9. Verdict logic

- **Province size predicts `q_u` buffering (F1 +, F2 −, F3 +, clearing the
  binding bootstrap bound on ≥ 1 feature):** directly **CONFIRMS**
  province-mediation — bigger provinces decline less relative to the empire, the
  mechanism behind the Obs 104 `q_uv ≫ q_v` gap.
- **Coherent direction but CIs include 0 (the expected low-power outcome):**
  **corroborates the direction** of the Obs 104 inference without establishing it
  — report as "directionally consistent, underpowered".
- **Null / sign-incoherent:** the Obs 104 `q_uv ≫ q_v` inference is **not
  directly corroborated** at province level; the size signal may enter through a
  city-membership channel rather than the province trajectory itself. Say so
  plainly.
