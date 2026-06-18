# Province-size regression — does province size predict province-from-empire (`q_u`) buffering? — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13; **no thresholds** — descriptive).
  Run on sapphire, 2026-06-18 (background agent); deterministic transform of the
  §5 Layer-A posterior, no MCMC. Reuses the size-vs-dynamics machinery.
- **Origin:** direct test of the province-mediation *inference* in Obs 104 (which
  inferred it from `q_uv ≫ q_v`, not from a province-level regression).

---

## 1. What was tested

**Unit = province** (35 non-singleton). `q_u[p,t] = exp((1/β)·u_shape[p,t])` computed
directly from `u_shape` (S=8,000, P=35, T=16) at empire β (median 0.587), one series
per province. **Predictor = province size** = `pop_est` aggregated over **all** member
cities in the full 1,012-city index — **sum** (primary), **mean**, **max**
(sensitivities); log₁₀. **Features** on `q_u` (mid-bins; edges excluded): F1 late-level
`q_u[AD262]`, F2 volatility `SD_t(log q_u)`, F3 tilt `log q_u[AD262]−log q_u[AD112]`;
"more buffered" = F1↑, F2↓, F3↑. **Method** identical to the city probe: Spearman ρ
primary, province-bootstrap 95 % CI (binding), draw-wise ρ posterior, OLS + Theil-Sen.
Non-circular (Layer A has no population covariate, Obs 98); ρ β-frame-invariant.
**Samples:** all 35 (primary) + 20 with ≥1 reliable (N≥300) city (sensitivity; flagged
— province-tier reliability is **not** separately calibrated, N\*=300 is a per-city floor).

**Province join — clean:** 35/35 `u_shape` provinces matched the full-index `province`
field exactly (0 unmatched). Sum-`pop_est` range [10,868; 645,931] = **1.77 log₁₀
decades**; member cities 4 / 19 / 70 (min/median/max).

**Self-check — exact (PASS):** `q_u` constant within province ✓; direct `u_shape`
inversion reproduces the residual Layer B `q_u_med` to **max abs diff 0.0** (spot
province Achaia) — bit-exact (same draws, same seed).

---

## 2. Results — Spearman ρ (bootstrap 95 % CI | P-sign); ✓ = buffered direction

**No bootstrap CI excludes 0 anywhere.** The binding uncertainty is **sampling** (n);
draw-wise bands are uniformly narrower than the bootstrap CIs.

| aggregate | sample | F1 late-level | F2 volatility | F3 tilt |
|---|---|---|---|---|
| **sum** (primary) | all 35 | −0.05 [−0.37,+0.28] ✗ | −0.24 [−0.51,+0.09] ✓ | −0.06 [−0.41,+0.32] ✗ |
| sum | reliable 20 | +0.00 [−0.45,+0.45] | −0.15 [−0.60,+0.32] ✓ | +0.12 [−0.32,+0.53] ✓ |
| mean | all 35 | +0.21 [−0.16,+0.53] ✓ | −0.05 ✓ | +0.03 ✓ |
| mean | reliable 20 | **+0.35** [−0.12,+0.76] ✓ | +0.12 ✗ | +0.31 [−0.18,+0.80] ✓ |
| max | all 35 | +0.08 ✓ | −0.25 [−0.56,+0.08] ✓ | +0.07 ✓ |
| max | reliable 20 | +0.22 ✓ | −0.15 ✓ | **+0.37** [−0.11,+0.73] ✓ |

OLS-vs-Theil-Sen diverges on sum F1/F3 (leverage; the Obs 94 check) — rank ρ is the
robust read.

---

## 3. Verdict — NOT directly corroborated; underpowered; a size-aggregate split worth noting

n = 35 (≈ 20 reliable); |ρ| ≳ 0.33 (≳ 0.44 at n=20) is needed to clear a 95 % bound,
and **nothing reaches it**. So the result is formally a **null**, pre-framed as expected
and informative (Obs 100 low-power / range restriction). Reading the directions:

- **The primary aggregate (sum / total provincial urban mass) is null and
  sign-incoherent** — F1 and F3 (the features that carried the Obs 104 `q_uv` gradient)
  are flat-to-slightly-*anti*-buffered; only F2 leans buffered.
- **Mean and max (per-city scale)** lean *buffered* (F1↑, F3↑; max also F2↓), strongest
  on the reliable-20 subset (mean F1 +0.35, max F3 +0.37) — but every CI includes 0.

**So the Obs 104 `q_uv ≫ q_v` province-mediation inference is NOT directly confirmed.**
The city-level size–buffering gradient itself stands (it is a property of city-level
ranks); this test simply cannot show its mechanism is "bigger provinces have more
buffered `q_u`". The **sum-vs-mean/max split is the informative part**: the buffered
hint attaches to *per-city scale* (mean/max) and not to *total provincial mass* (sum),
which is mildly more consistent with a **city-membership channel** (large cities happen
to sit in provinces whose `q_u` is buffered) than with *province size* driving the
province trajectory. Stated as **ambiguous, leaning not-corroborated** — a hint at most,
not a finding.

**Relation to the prior Obs.** This does **not** contradict Obs 103/104's decomposition
result that the province tier carries much of the decline *level* — a tier can hold the
decline magnitude without province *size* predicting *which* provinces decline. It does
refine Obs 104: the "province-mediated" reading is a statement about the decomposition
(the variance lives in the `u` tier), **not** evidence of a province-size effect.

---

## 4. Caveats

1. **n = 35 / 20 — very low power**; nothing clears the bound; null expected (Obs 100).
2. **Not pure demography** (Obs 98) — `u_shape` carries province-level taphonomy,
   economy, habit; "buffered" ≠ demographically buffered.
3. **Province-tier reliability not separately calibrated** (N\*=300 is per-city); the
   reliable-20 subset is a heuristic.
4. **Range restriction** — 1.77 decades of province sum-size.
5. **Multiple comparisons** — 3 aggregates × 3 features × 2 samples reported together,
   no cherry-pick, no threshold (Decision 13).
6. **The city-membership-channel reading is speculative** at this n — a directional
   lean, not a demonstrated mechanism.

---

## 5. Outputs

`outputs/province-size-regression-summary.json` (full ρ / bootstrap / draw-wise / slopes
per aggregate × feature × sample; province join; self-check; provenance sha256);
`province-size-regression-scatter.png`; `province-size-regression-rho-posterior.png`.
Cross-refs: Obs 104 (inference tested — stands at city level, mechanism not confirmed),
Obs 103 (province tier carries the decline level — not in tension), Obs 100 (low power /
range restriction), Obs 98 (not pure demography).
