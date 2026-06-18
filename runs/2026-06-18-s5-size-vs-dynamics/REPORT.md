# §5 size-vs-dynamics probe — does city size predict city-specific dynamics? — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13 / prereg §5; **no thresholds** —
  descriptive). Run on sapphire, 2026-06-18; `code/size_vs_dynamics.py`
  (deterministic read of the §5 Layer-A posterior + bootstrap; no MCMC). Log
  `run.log`.
- **Origin:** the well-posed reframe (user-obs 43) of "can we compare the
  isolated city-level effect to Hanson?" — a direct `q_v`-vs-Hanson overlay is a
  category mismatch (level-free shape vs static level), so this asks instead
  whether **city size predicts features of the city-specific trajectory**.

---

## 1. The question and why it is legitimate

Cross-city: does Hanson `pop_est` predict features of `q_v` (city-from-province;
province and empire removed) — primary — or `q_uv` (city-from-empire) — secondary?
Features (mid-bins; edges excluded): **F1 late-level** `q[AD 262]`, **F2
volatility** `SD_t(log q)`; secondary **F3 tilt** `log q[AD262]−log q[AD112]`,
**F4 peak-bin**.

**Non-circular.** §5 Layer A carries no population covariate (Obs 98), so `v_shape`
(hence `q_v`) is Hanson-free; Hanson enters only as the predictor. Spearman ρ is
**exactly β-frame-invariant** per draw (the 1/β inversion is a monotone,
city-constant rescale), so the rank results carry to the Latin frame unchanged;
slopes are in empire-β units.

**Predictor:** 34 reliable cities (N ≥ 300), `pop_est` ∈ [1,000, 153,722],
**2.19 log₁₀ decades**, 19 provinces. The binding limit is **n = 34** (|ρ| ≳ 0.34
needed to clear a 95 % bootstrap bound), so this **suggests, it does not
establish**, and a null is informative (Obs 100).

---

## 2. Primary tier `q_v` (city-from-province) — headline NULL, one suggestive secondary

Spearman ρ, 34 reliable cities (bootstrap 95 % CI | draw-wise ρ posterior):

| feature | ρ | bootstrap CI | P(ρ>0) | draw-wise ρ | OLS / Theil-Sen |
|---|---|---|---|---|---|
| **F1 late-level** | +0.09 | [−0.26, +0.41] | 0.71 | +0.07 [−0.18, +0.32] | +0.284 / +0.130 |
| **F2 volatility** | −0.05 | [−0.39, +0.28] | 0.37 | −0.09 [−0.30, +0.13] | −0.145 / −0.068 |
| F3 tilt *(sec.)* | +0.31 | [−0.06, +0.61] | 0.96 | +0.21 [−0.02, +0.43] | +0.828 / +0.937 |
| F4 peak *(sec.)* | +0.04 | [−0.34, +0.39] | 0.58 | +0.02 [−0.23, +0.29] | +0.355 / +0.000 |

- **The headline (F1, F2) is null:** city size does **not** predict where the
  purely city-specific trajectory sits late, nor its volatility. F1's OLS slope
  (+0.284) was inflated by a leverage point relative to Theil-Sen (+0.130) — the
  rank ρ (+0.09) is the robust read (the Obs 94 leverage check working).
- **F3 tilt is suggestive** (ρ +0.31, P(ρ>0) 0.96) — larger cities tending to a
  shallower early-to-late decline relative to their province — but it is a
  *secondary* feature and its bootstrap CI **includes 0** ([−0.06, +0.61]). The
  draw-wise ρ (+0.21) nearly excludes 0, so the limiting uncertainty is **sampling
  (n = 34)**, not the trajectory posterior — exactly as pre-framed.

---

## 3. Secondary tier `q_uv` (city-from-empire) — a coherent, province-mediated gradient

| feature | ρ | bootstrap CI | P-sign | draw-wise ρ |
|---|---|---|---|---|
| F1 late-level | **+0.28** | [−0.08, +0.58] | P>0 0.93 | +0.21 [+0.04, +0.37] |
| F2 volatility | **−0.24** | [−0.58, +0.13] | P<0 0.90 | −0.21 [−0.35, −0.06] |
| **F3 tilt** | **+0.38** | **[+0.05, +0.63]** | P>0 0.99 | +0.32 [+0.15, +0.48] |
| F4 peak | +0.12 | [−0.29, +0.47] | 0.72 | +0.05 [−0.08, +0.19] |

On `q_uv` the three magnitude features line up in **one coherent direction —
bigger cities are more buffered relative to the empire**: sustained later (F1 +),
less volatile (F2 −), shallower decline (F3 +). F3's bootstrap CI just clears 0;
F1/F2 clear 0 only on the (non-binding) draw-wise band. F3 is leverage-clean
(OLS +1.54 ≈ Theil-Sen +1.60).

**The key structural read:** the gradient is **much stronger on `q_uv` than on
`q_v`** (e.g. F3 +0.38 vs +0.31; F1 +0.28 vs +0.09; F2 −0.24 vs −0.05). Since
`q_uv` = province-from-empire × city-from-province, and removing the province
(`q_v`) largely removes the signal, the size–buffering relationship operates
**mainly at the province tier** — larger cities tend to sit in provinces that
decline less relative to the empire. This **coheres with the residual Layer B
finding** that the late-imperial decline is largely provincial-tier (REPORT §4
there): both the *level* of decline and its *covariation with size* live more in
the province than in the individual city.

---

## 4. Sensitivity — all-268 (below-floor included) washes the signal out

On all 268 cities (234 below the N\*=300 floor), every ρ collapses toward 0 and
some flip sign (`q_v`: F1 −0.10, F3 −0.04). Expected: below-floor trajectories are
uncalibrated and partial-pool toward the common shape (shrunk `v_shape`), adding
noise and diluting any signal. So the (suggestive) structure is **only** in the
reliable set; this is a coherence/robustness note, not a contradiction.

---

## 5. Bottom line (honest)

To Shawn's literal question — does size predict the *purely* city-specific
dynamics? — the answer on the headline features is **no** (null on `q_v` F1/F2),
with a single suggestive secondary (F3 tilt, CI includes 0). The more interesting
structure is that size **does** track the province-inclusive trajectory (`q_uv`)
in a coherent "bigger = more buffered" gradient, and that this is **mostly
province-mediated** — consistent with the provincial-tier decline result. All of
this is **suggestive only**: n = 34, restricted range (Obs 100), a multi-feature
surface read without cherry-picking, and `v_shape` is not pure demography
(Obs 98), so even the gradient is "size predicts the city/province-specific
signal", not demonstrated demographic buffering. A clean, bounded answer that
turns the original (mis-posed) question into a real — if underpowered — finding.

---

## 6. Caveats (carry into any write-up)

1. **n = 34, low power** — suggestive not established; a null was pre-framed as
   informative.
2. **Not pure demography** (Obs 98) — `v_shape`/`u_shape` carry taphonomy,
   economy, habit; "buffered" ≠ demographically buffered.
3. **Range restriction** (Obs 100) — 2.19 decades among small-N targets.
4. **Multiple comparisons** — 4 features × 2 tiers × 2 samples reported together,
   no cherry-pick, no threshold (Decision 13).
5. **Province-mediation is an inference** from the `q_uv` ≫ `q_v` gap, not a
   direct province-size regression (a natural follow-up if pursued).
6. **β-frame:** rank results β-invariant; slopes in empire-β units.

## 7. Outputs

`outputs/size-vs-dynamics-summary.json` (full ρ / bootstrap / draw-wise / slopes,
per feature × tier × sample; provenance sha256); `size-vs-dynamics-scatter.png`
(F1/F2 vs log₁₀ pop, `q_v`, with Theil-Sen + ρ); `size-vs-dynamics-rho-posterior.png`
(draw-wise ρ posteriors).
