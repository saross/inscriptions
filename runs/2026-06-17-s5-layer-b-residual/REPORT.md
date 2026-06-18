# §5 Layer B (RESIDUAL) — habit-removed relative-to-empire β-inversion — RESULTS

*(per the 2026-06-17 framing decision (Obs 101), methods/results name the
removed component the **empire-wide common temporal component**; the
epigraphic-habit interpretation is reserved for the discussion (Obs 98).)*

- **Status:** COMPLETE (exploratory; Decision 13 / preregistration §5;
  no pre-committed thresholds). **Illustrative comparative-shape only — NOT
  quantitative population claims, and NOT absolute population (Obs 98).**
- **Run:** sapphire, 2026-06-18; `code/layerb_residual_invert.py --seed 20260616`
  (defaults; log `run.log`). Deterministic transform of the §5 Layer-A
  posterior — **no MCMC**. Exit 0.
- **Spec + sign-off:** `spec.md` (design decisions signed off 2026-06-18; final
  launch sign-off 2026-06-18).

---

## 1. What was done

Each city's residual log-trajectory `r[c,t] = u_shape[p(c),t] + v_shape[c,t]`
(its deviation from the empire-wide common temporal component `g_shape`, which is
**removed**) was inverted, draw-wise, into a population trajectory **relative to
the empire trend**:

`q[c,t] = exp( (1/β_within) · r[c,t] )`

Because `r` is zero-sum over t (each shape term is a centred Gaussian random
walk), `q` has geometric mean 1 across the 16 bins **by construction**: `q = 1.0`
means "on the empire trend at that bin", `q = 0.5` means "half". This is the
quantity Obs 98 names well-posed *regardless of the habit/demography conflation*
— `g` is differenced out, not decomposed.

- **β frames:** empire `β_within = 0.588` primary; Latin `0.733` overlay (both
  posteriors propagated, seeded resample).
- **Residual:** the nested divergence triple — `u+v` city-from-empire (primary),
  `v` city-from-province, `u` province-from-empire; `q_uv = q_u · q_v` per draw (§4).
- **Scope:** the 268 small-N target cities; 34 meet the N\*=300 reliability floor.
- **Wiring guard (self-test) — PASS at machine precision.** Adding `g` back
  reconstructs `exp((1/β)·((g+u+v)−max))`, which must equal the raw Layer B
  relative-shape (within-city level offsets cancel under peak-normalisation):
  max abs diff vs the persisted raw `shape_med` = **5.6 × 10⁻¹⁶** (city Cirta).
  So the *only* difference from the raw Layer B (Obs 96) is the removal of `g`.

---

## 2. Headline — the apparent universal collapse dissolves into heterogeneity

The raw Layer B (Obs 96) showed the median small-N city's inverted population
falling to ≈ 0 % of peak by AD 250 — but that collapse is the empire-wide
post-AD-250 decline (in `g`), amplified by `1/β`. **Removing `g` dissolves it.**

Median `q` against the empire baseline (1.0), reliable cities (empire β):

| bin (centre) | era | median `q` | IQR | share below empire |
|---|---|---|---|---|
| AD 112 | early-Antonine | 0.48 | [0.27, 1.74] | 0.65 |
| AD 188 | empire-common peak (`g` peak) | **1.01** | [0.38, 4.36] | 0.50 |
| AD 262 | 3rd-c. ("crisis") | **0.32** | [0.16, 1.25] | 0.68 |
| AD 338 | late | 0.67 | [0.10, 5.22] | 0.53 |

- At the empire-common peak (AD 188) the median city sits **exactly on the empire
  trend** (`q ≈ 1.01`) — as it must, since that is what `g` captures.
- By the 3rd century the median city is at **≈ 0.32 of its empire-relative
  baseline** — a *moderate* relative decline (a factor of ~3), **not** the raw
  inversion's near-total collapse, and **heterogeneous**: ~⅓ of reliable cities
  are still *at or above* the empire trend (`q ≥ 1`) even at AD 262, rising to
  ~½ by AD 338. The inter-quartile spread (e.g. [0.16, 1.25] at AD 262) is the
  city-specific signal the residual is designed to expose.
- The Latin-β overlay is uniformly milder (smaller exponent 1.36 vs 1.70):
  median `q` at AD 262 = **0.40** (same 68 % below empire).

Figure: `outputs/layerb-residual-vs-raw.png` (left: raw apparent collapse;
right: residual `q` vs the 1.0 baseline with the IQR band).

---

## 3. Methodological correction — why "fraction of peak" misleads here

The spec pre-specified the contrast as "fraction of own peak at AD 250", to mirror
the raw Layer B's headline. **That metric is confounded for the residual** and
its first-pass value (≈ 0, *apparently* reproducing the collapse) is an artefact:

- `q` is amplified by `1/β = 1.70`, and `r` is a Gaussian random walk, so its
  **endpoints have high variance** — **11 of 34** reliable cities have their
  `q`-peak pinned at the very first or very last bin (the envelope edges).
  Dividing the late level by such an extreme peak drives the ratio to ~0
  regardless of the actual late position relative to the empire.

The correct diagnostic for a geom-mean-1 quantity is `q` **vs the empire baseline
(1.0)**, §2 above. The confounded frac-of-peak numbers are retained, clearly
flagged, in `summary.json → frac_of_peak_CONFOUNDED` for transparency only.

**Edge-bin caveat:** for the same GRW-endpoint reason, the envelope-edge bins
(AD 12: median `q` 2.74, IQR up to 18; AD 338: IQR up to 5.2) have inflated
variance and are **not** interpreted; the narrative rests on the well-constrained
mid-empire bins (AD 112 / 188 / 262).

---

## 4. The nested decomposition — the decline is largely provincial-tier

The residual factors into three **nested divergences**, each inverted from one
tier of the model (median `q` vs the empire baseline 1.0; all over the 34
reliable cities, every one of which has a province tier):

| bin (centre) | city ← empire (`q_uv`) | province ← empire (`q_u`) | city ← province (`q_v`) |
|---|---|---|---|
| AD 112 | 0.48 | 0.64 | 0.75 |
| AD 188 | 1.01 | 0.77 | 1.31 |
| AD 262 | **0.32** | **0.56** | 0.78 |
| AD 338 | 0.67 | 0.84 | 0.80 |

They nest **per draw**: `q_uv = q_u · q_v` (runtime-guarded; max abs deviation
1.3 × 10⁻⁸). *Caveat:* the identity is per-draw, so the **median** columns do
**not** multiply (median of a product ≠ product of medians) — read each column as
its own marginal summary.

At AD 262 the median city sits at 0.32 of the empire baseline; decomposed, its
**province** is at 0.56 of empire and the city at 0.78 of its own province — so
the **larger share of the divergence is provincial-tier**, not city-specific
(this is now shown *directly* by `q_u`, not merely inferred from `q_v` being
flatter). The late-imperial under-production of these small western cities is
mostly *their provinces declining relative to the empire*, not idiosyncratic to
individual cities — a structural result bearing on interpretation (region-wide vs
city-specific drivers). Figure `outputs/layerb-residual-nested-tiers.png`; all
three tiers are in the per-frame `.nc` (`q_uv_*`, `q_u_*`, `q_v_*`).

---

## 5. Validation (descriptive; no thresholds)

- **Foundation-terminus on `q` (within-set, 99 cities).** Hanson `Start Date`
  matched to all 268 cities; 99 are founded within the envelope and bind. Median
  pre-foundation mass fraction of `q` = **0.02 %** — the relative-to-empire
  trajectory respects foundation termini (the same frontier-military exceptions
  H5 flagged apply). This is the within-set anchor that *does* apply to the
  residual object.
- **Anchors not re-run (by design).** Ostia and Pompeii are held out of the
  pooled fit and so carry no `g`-decomposition (Obs 102); they validated the
  *full* inversion out-of-sample in the raw Layer B (Obs 96, clean pass) and are
  cited, not re-run.

---

## 6. Caveats (carry into the write-up)

1. **Relative, not absolute.** `q` is population *relative to the empire trend*,
   not absolute population (absolute would require inverting `g`, undecomposable —
   Obs 98).
2. **The residual is not pure demography** (Obs 98). `u+v` is "deviation from the
   empire norm"; it still carries city/province-level taphonomy, economy, and
   habit. The only clean claim is *free of the empire-common confound*.
3. **Cross-sectional → temporal** (prereg's flagged strong assumption); `1/β`
   amplification (the β frame changes amplitude materially).
4. **Edge-bin variance** (§3); **N\*=300 floor** (34/268 reliable);
   within-sample empire shape (the 268-city `g` is a proxy for the true empire
   common component).

---

## 7. Bottom line

Removing the empire-wide common temporal component turns the raw inversion's
*apparent universal post-AD-250 collapse* into a **moderate, heterogeneous
relative decline**: the median reliable city sits on the empire trend at the
AD-188 peak and at ~0.32 of its empire-relative baseline by the 3rd century, with
roughly half the cities at or above the empire trend even late. The nested
decomposition (§4) shows the larger share of that decline is **provincial-tier**
(province-from-empire `q_u` ≈ 0.56 at AD 262) rather than city-specific
(city-from-province `q_v` ≈ 0.78). The result is well-posed regardless of the habit/demography conflation
(Obs 98) but is relative and not pure demography — exactly the bounded,
demography-isolating contribution the residual Layer B was designed to deliver,
and a cleaner object than the raw inversion for the discussion.
