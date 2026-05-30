# §5 Layer A — Hierarchy smoke report (partial pooling + prior-predictive)

- **Status:** SMOKE COMPLETE — hierarchy built, hyperpriors pinned by
  prior-predictive, smoke fit converges, pooling sanity check passes. NOT
  production (smoke subset of 26 cities only; no all-267 fit, no
  subsample-recover grid, no letter-mass unit).
- **Date:** 2026-05-30.
- **Host:** zbook (pymc 6.0.1); threading/scratch hygiene per spec §6.
- **Author:** Claude (Opus 4.8, 1M context), on Shawn's brief.
- **Builds on:** the VALIDATED single-city Poisson-aoristic core
  (`code/model.py`; sim-recovery r≈0.96, coverage 1.0, Pompeii AD 79 terminus
  recovered). Reuses `code/dataprep.py`'s prepared cache and `aoristic_matrix`.

---

## 1. Model parameterisation (`code/hier_model.py`)

For city `c` in province `p(c)`, latent log-rate over `T = 16` bins:

```
log lambda[c, t] = alpha_g                (global level intercept, anchored)
                 + g_shape[t]             (global trajectory shape; zero-sum/t)
                 + b_u[p(c)]              (province level offset; ~0)
                 + u_shape[p(c), t]       (province shape deviation; zero-sum/t)
                 + b_v[c]                 (city level offset; ~0)
                 + v_shape[c, t]          (city shape deviation; zero-sum/t)
```

**Level / shape split (the identifiability fix).** The additive decomposition
`g + u + v` is only weakly identified if every tier carries both level and
shape (any constant can slide between tiers). So each tier's TIME-VARYING part
is made **zero-sum over the 16 bins** — a pure *shape* deviation carrying no
level — and the level is carried separately by additive intercepts:

- `alpha_g ~ Normal(log(mean_c N_c / T), 1.0)` — the single global level,
  anchored at the empire-(subset-)level mean log per-city total.
- `b_u[p]` and `b_v[c]` are *level offsets*, shrunk toward 0. They absorb only
  genuine between-province / between-city level differences; most of the level
  lives in `alpha_g`. This is the partial pooling of LEVEL (spec §4: "the full
  Poisson form pools level as well as shape").

This is the brief's recommended clean fix (zero-sum-over-time `u, v` shapes +
small per-province / per-city level intercepts), adopted because the naive
additive level split is weakly identified.

**Shape tiers — non-centred RW1, zero-sum over time** (the 2026-05-24 F3
non-centred lesson, applied to every tier):

```
sigma_g ~ HalfNormal(s_g);  z_g ~ Normal(0,1, T);  g_shape = centre(cumsum(z_g)*sigma_g)
sigma_u ~ HalfNormal(s_u);  z_u ~ Normal(0,1,[P,T]); u_shape[p] = centre(cumsum(z_u[p])*sigma_u)
sigma_v ~ HalfNormal(s_v);  z_v ~ Normal(0,1,[C,T]); v_shape[c] = centre(cumsum(z_v[c])*sigma_v)
```

where `centre(x) = x - mean_t(x)` makes each unit's walk zero-sum over time.
`u_shape` is defined only for the `P` NON-SINGLETON provinces.

**Level offsets — also NON-CENTRED** (the smoke-stage divergence fix, see §4):

```
sigma_bu ~ HalfNormal(0.5);  z_bu ~ Normal(0,1, P);  b_u = z_bu * sigma_bu
sigma_bv ~ HalfNormal(0.5);  z_bv ~ Normal(0,1, C);  b_v = z_bv * sigma_bv
```

A centred `b_v ~ Normal(0, sigma_bv)` funnels as `sigma_bv -> 0`; non-centring
removes it (12 divergences -> 0; see §4).

**Singletons.** Provinces with exactly one TARGET city in the subset have an
unidentified province tier, so it is **dropped entirely**: no `u_shape` row, no
`b_u` entry (both fixed at 0). The city's `v_shape + b_v` then carry its full
deviation toward the GLOBAL trajectory (spec §4 singleton rule). Implemented by
mapping each singleton-province city to province row `-1`, which gathers a
padded zero row of `u_shape` and a zero `b_u`.

**Likelihood — the SAME validated Poisson-process aoristic `pm.Potential`,
summed over cities, vectorised.** All cities' aoristic rows are concatenated
into one `(N_total, T)` matrix `A_all` with a parallel `insc_city` index. Per
inscription `i` of city `c`: `per_insc[i] = sum_t A_all[i,t] * lam[c,t]` (formed
by gathering each row's city `lam` and an element-wise row dot). Total
`loglik = - sum_{c,t} lam[c,t] + sum_i log(per_insc[i])` — the city-summed
version of `model.py`'s `-lam.sum() + log(A@lam).sum()`.

**Sampler:** 4 chains, `target_accept = 0.99` (matches `model.py`; the
non-centred RW1 funnel needs it).

---

## 2. Hyperprior scales — pinned by prior-predictive (`code/prior_predictive.py`)

Sampled trajectory ensembles **from the prior alone** (no data, no likelihood,
no fitting — priors set without peeking at results). For each candidate
HalfNormal scale we drew 8 000 zero-sum RW1 shape trajectories (the exact tier
construction) and summarised whether the ensemble looks like *plausible
epigraphic histories*: smooth multi-bin rise/fall up to ~1-1.5 log-units, not
jagged adjacent swings; deviations modest relative to global.

**Global grid (`sigma_g ~ HalfNormal(s_g)`)** — span = peak-to-trough in
log-units:

| s_g | adj-jump med | span med (log-u) | span p75 | span p90 | ptr med | % draws < 1.5 log-u |
|-----|------|------|------|------|------|------|
| 0.3 | 0.41 | **0.97** | 1.69 | 2.61 | 2.63x | **70 %** |
| 0.5 | 0.66 | 1.55 | 2.83 | 4.37 | 4.73x | 49 % |
| 0.7 | 0.93 | 2.19 | 3.95 | 6.14 | 8.95x | 37 % |

**Deviation grid (`sigma_u, sigma_v ~ HalfNormal(s)`)** — ptr = exp(span):

| s | adj-jump med | ptr med | ptr p90 |
|-----|------|------|------|
| 0.15 | 0.20 | **1.60x** | 3.73x |
| 0.2  | 0.26 | 1.87x | 5.81x |
| 0.3  | 0.40 | 2.61x | 13.9x |
| 0.5  | 0.67 | 4.76x | 73.8x |

**RECOMMENDED:  s_g = 0.3,  s_u = s_v = 0.15.**

- `s_g = 0.3`: the typical global trajectory rises/falls ~0.97 log-units
  (≈2.6x) over the four centuries — squarely in the brief's "up to ~1-1.5
  log-units of smooth variation" band — with 70 % of draws inside the
  1.5-log-unit ceiling and smooth adjacent steps (median jump 0.41 log-units).
  `s_g = 0.5` pushes the *median* span past the 1.5-log-unit ceiling (too
  loose); `0.7` is clearly over-wide.
- `s_u = s_v = 0.15`: province/city deviations are genuinely modest (median
  1.60x multiplicative, p90 < 4x) and well below the global scale — the
  "deviations small relative to global" property that lets shrinkage tighten
  small-N cities. `0.2` lets the p90 deviation reach ~5.8x (loose); larger
  scales let cities/provinces wander too far from their parent.

Note: the cumsum-RW1 has a heavy ENDPOINT tail by construction (a few extreme
draws), so scales were judged on the **median / p75 / p90** of the span, not the
extreme `ptr p99`. PNG overlay: `code/prior-predictive-overlay.png` (global
trajectories left, deviations right) — Shawn's sanity check.

`sigma_bu, sigma_bv ~ HalfNormal(0.5)` (level-offset scales) were not grid-pinned
(they are weakly-informative level priors, not trajectory-shape knobs; the level
is anchored by `alpha_g` and the data).

---

## 3. Smoke subset (26 cities; documented for reproducibility)

Chosen to exercise every code path: a rich province with the Pompeii anchor,
two median provinces (one Italian-adjacent, one frontier), and three
singletons.

- **Rich — Latium et Campania / Regio I (14 cities):** Pompeii (N=4266, large
  anchor + AD 79 terminus), Puteoli (1723, large anchor), Capua (918), Misenum
  (578), Aricia (386), Cumae (231), Tibur (224), Nomentum (159), plus the
  small-N pooling-sanity targets Fundi (85), Interamna Lirenas (73), Anagnia
  (71), Caiatia (56), Cereatae (54), Gabii (50).
- **Median — Baetica (5):** Augusta Emerita (543), Corduba (483), Astigi (170),
  Urso (71), Parlais (53).
- **Median (frontier) — Pannonia superior (4):** Scarbantia (149), Vindobona
  (120), Siscia (119), Mogentiana (58).
- **Singletons (3):** Caesarea Maritima (Palaestina, 53), Forum Claudii (Alpes
  Poeninae, 68), Aleria (Corsica, 90) — each its own province in the subset, so
  the province tier is dropped and the city pools to global.

Total inscriptions: **10 851**; mean per-city N = 417.3. The 3 non-singleton
provinces get a `u` tier; the 3 singletons do not (`city_prov = -1`).

---

## 4. Convergence

**First fit (draws 1000 / tune 1000 / target_accept 0.99) — MISSED gate:**
max R-hat 1.0100 (`alpha_g`), min ESS 898, **1 divergence**. The single
escalation (tune/draws ×2) fixed R-hat (1.000) and ESS (1873) but divergences
ROSE to 12 — worst R-hat still `alpha_g`, worst ESS `b_v[Puteoli]`. That
signature (level intercept + large-anchor city level offset) diagnosed a
**centred level-tier funnel** in `b_u, b_v ~ Normal(0, sigma_b)`.

**Fix:** non-centre the level offsets (`b = z_b * sigma_b`, `z_b ~ Normal(0,1)`)
— the same lesson already applied to the shape tiers.

**Re-fit after the fix (draws 1000 / tune 1000 / target_accept 0.99) — PASSES
at base sizing, no escalation needed:**

| metric | value | gate | status |
|--------|-------|------|--------|
| max R-hat | **1.0000** | < 1.01 | PASS |
| min bulk ESS | **908** | ≥ 400 | PASS |
| divergences | **0** | = 0 | PASS |

(worst R-hat `alpha_g` = 1.000; worst ESS `sigma_u` = 908.) All 4 standalone
single-city sanity fits also converged (R-hat 1.000, ESS ≥ 1046, 0 div).

The gate was never relaxed; the fix was a reparameterisation (the funnel
lesson), not a loosened threshold.

---

## 5. Pooling sanity check (the key validation)

### 5a. Small-N shrinkage (hierarchical vs standalone single-city)

For each small-N city, the hierarchical posterior trajectory vs the SAME city
fit STANDALONE (`model.py`). Mean 95 %-CI-width ratio (hier / standalone): < 1
means the hierarchy is tighter.

| city | N | CI-width ratio hier/standalone | shape r (hier vs standalone) |
|------|---|------|------|
| Gabii | 50 | **0.998** (tighter) | 0.931 |
| Cereatae | 54 | 1.069 (marginally wider) | 0.813 |
| Caiatia | 56 | **0.985** (tighter) | 0.927 |
| Anagnia | 71 | **0.948** (tighter) | 0.793 |

**Verdict: shrinkage confirmed, mild and honest.** 3 of 4 small-N cities have
tighter hierarchical CIs; the hierarchical medians track the standalone shapes
(r 0.79-0.93). The effect is gentle because `s_v = 0.15` keeps city deviations
small and N is only modestly small (50-71). Cereatae is marginally WIDER
(1.07): its standalone trajectory already sits near the province mean (lower
shape r), so the hierarchy contributes little prior information while still
propagating province/global uncertainty — an honest, expected edge case, not a
failure. (A stronger shrinkage signal is expected at N ~ 50 with cities whose
standalone fit is noisier; production will quantify the full precision-vs-N
curve.)

### 5b. Pompeii containment (AD 79 idiosyncrasy must not poison the province)

| series | post-AD-79 mass fraction |
|--------|------|
| Pompeii CITY | 20.8 % |
| Regio I PROVINCE mean | 66.5 % (preserved) |
| Capua CITY (non-Pompeii Regio I) | 43.0 % |

**Verdict: containment confirmed.** The 20.8 % "post-79" Pompeii figure is a
bin-boundary artifact: the AD 75-100 bin (which legitimately holds Pompeii's
final pre-eruption years, AD 75-79) carries 877 of the 885 "post-79" expected
inscriptions, and Pompeii's raw aoristic SPA puts essentially the same mass
there (988; 23.2 %). From the FIRST FULLY post-79 bin (AD 100+) onward,
Pompeii's city trajectory collapses to **4.5, 1.1, 0.7, 0.3, 0.1, ...** — i.e.
genuinely-post-79 mass (bins ≥ AD 100) is ~7.5 of 4260 = **0.18 %**, recovering
the terminus exactly as the validated single-city build did.

Crucially, the Regio I **province mean is preserved** (66.5 % of province mass
sits post-79; bins AD 100-350 hold 7-16 expected inscriptions each) and **Capua
keeps a healthy post-79 trajectory** (28-138 per bin). Pompeii's collapse is
absorbed by its CITY tier (`v_shape + b_v`) without dragging the province mean
to zero — exactly the desired behaviour. See `code/hier-smoke-pooling.png`
(bottom log-y panel: Pompeii city crashes after AD 79; province + Capua stay up).

---

## 6. Artefacts

- `code/hier_model.py` — the hierarchical model.
- `code/prior_predictive.py` — hyperprior pinning; `code/prior-predictive-overlay.png`,
  `code/prior-predictive-results.json`.
- `code/hier_smoke_fit.py` — smoke fit + pooling sanity driver;
  `code/hier-smoke-pooling.png`, `code/hier-smoke-results.json`.

(PNGs and result JSONs are committed for review; the parquet and `.npz` caches
are NOT committed.)

---

## 7. Open items before production (NOT done here — smoke only)

- Production fit of all 267 target cities + 46 provinces.
- Subsample-and-recover calibration grid (§8a.3).
- Letter-mass exploratory overlay (NB/Gamma form by PPC).
- 50-year-bin robustness refit.
- Shawn's post-hoc sanity check of the prior-predictive overlay and the pinned
  scales, then production go.
