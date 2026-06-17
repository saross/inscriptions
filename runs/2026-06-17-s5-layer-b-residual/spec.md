# §5 Layer B (RESIDUAL) — habit-removed β-inversion to a *relative* population trajectory (SPEC, pre-launch)

- **Status:** DRAFT — awaiting Shawn's pre-launch sign-off. **Do not execute
  until the sign-off checklist (§11) is ticked.**
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-17, on Shawn's brief.
- **Run dir:** `runs/2026-06-17-s5-layer-b-residual/`.
- **Type:** Exploratory (Decision 13; preregistration §5). Illustrative
  comparative-shape outputs only — **not** quantitative population claims.
- **Relation to prior work:** this is the **habit-removed (residual)** companion
  to the raw-trajectory Layer B (`runs/2026-06-16-s5-layer-b-beta-inversion/`,
  Obs 96), built on the H5 decomposition (`runs/2026-06-17-s5-h5-habit-removed/`,
  Obs 97) and motivated by the identification caveat (Obs 98). It is the
  principled inversion Obs 98 names as "well-posed regardless of the conflation".
- **Estimated effort:** a few minutes of compute (no MCMC at all — a deterministic
  transform of the already-fitted Layer-A posterior) + plotting + write-up.

---

## 1. Purpose and provenance — why a *residual* inversion

The raw Layer B (Obs 96) inverted each city's **full** inscription-rate
trajectory `lam[c,t]` into a population trajectory via the H3a scaling law,
`pop_t = pop_max · (insc_t / max_t insc_t)^(1/β)`. That inversion includes the
empire-wide common temporal component `g_shape` (Obs 97: peaks AD 187.5). Obs 98
established that `g_shape` is **not** a clean epigraphic habit — it conflates (a)
the cultural habit, (b) empire-wide demography/economy, (c) empire-wide
taphonomy, and (d) residual dating-convention structure — and that the
**defensible quantity is the residual**: a city's deviation from the
empire-common trend, which is interpretable *whatever the trend's drivers are*.

The visible symptom of the conflation in the raw Layer B: for the **median**
target city, inverted population at AD 250 is ≈ **0 % of peak** (empire β), a
near-total "collapse" that is the *amplified* empire-wide post-AD-250 inscription
decline (MacMullen 1982 epigraphic-habit collapse), **not** demonstrated
depopulation (raw-Layer-B REPORT §3; Obs 96 caveat). That spurious collapse lives
in `g_shape`, which is shared by every city.

**This run removes `g_shape` before inverting.** It inverts only the city's
residual trajectory `u_shape + v_shape` — the part of the city's log-rate that
deviates from the empire-common shape — and reports the result as a population
trajectory **relative to the empire-wide trend**. The empire-wide habit/demography
confound is differenced out by construction, so the deliverable is well-posed
without ever having to decompose `g_shape` (Obs 98).

---

## 2. The decomposition this inverts (already fitted — no new sampling)

The §5 Layer-A hierarchical model (`runs/2026-05-30-s5-small-n-trajectories/code/
hier_model.py`, lines 15–20, 322–332) factors each city's log inscription-rate:

```
log λ[c,t] = α_g                  global level intercept
           + g_shape[t]           empire-common shape   (zero-sum over t)
           + b_u[p(c)]            province level offset
           + u_shape[p(c),t]      province shape deviation (zero-sum over t)
           + b_v[c]               city level offset
           + v_shape[c,t]         city shape deviation    (zero-sum over t)
```

Each shape term is a centred Gaussian random walk —
`g_shape = centre(cumsum(z_g)·σ_g)` etc. (`hier_model.py` lines 270–271, 284–286,
311–312), so **each is exactly zero-sum over the 16 bins**. Verified against the
fitted posterior this session via the H5 reader (`runs/2026-06-17-s5-h5-habit-
removed/code/h5_habit_removed.py`): variables `g_shape (S,T)`, `u_shape (S,P,T)`,
`v_shape (S,C,T)`, `lam (S,C,T)`, S = 8,000 draws, T = 16, C = 268 target cities,
P = 35 non-singleton provinces; `city`/`prov` coords present.

- **Empire-common temporal component** = `α_g + g_shape[t]` — REMOVED here.
- **Residual trajectory (shape)** = `r[c,t] = u_shape[p(c),t] + v_shape[c,t]`,
  with `u_shape = 0` for singleton-province cities. This is what we invert. It is
  **level-free** (the cross-sectional level offsets `b_u`, `b_v` — the
  population-level axis, H5 §4 SD 0.78 — are deliberately *not* in `r`) and
  **zero-sum over t** (sum of two centred GRWs).

The residual is constructed draw-wise *identically* to H5 (`h5_habit_removed.py`,
`summarise()`): `residual = v + u_pad[:, city_u_rows, :]`. The new script reuses
that exact construction (§9), so the residual here is bit-for-bit the H5 residual.

---

## 3. The inversion, and what its output means

For city `c`, bin `t`, posterior draw `k`:

1. Residual log-deviation `r_k[c,t] = u_shape_k[p(c),t] + v_shape_k[c,t]`.
2. Draw `β_k` from the H3a `beta_within` posterior of the chosen frame
   (resampled with replacement, seeded — the established Layer B / H3b idiom;
   valid MC integration of two independent posteriors, §10).
3. **Relative population trajectory:**
   `q_k[c,t] = exp( (1/β_k) · r_k[c,t] )`.

Because `r` is zero-sum over t, `(1/β)·r` is mean-zero over t, so **`q` has
geometric mean = 1 across the 16 bins automatically** — no normalisation is
imposed; it falls out of the zero-sum GRW. `q[c,t]` reads directly as a
**multiplier on the city's own empire-relative baseline**: `q = 1.5` means the
city's (inferred) population at bin `t` was 50 % above where the empire-common
trend alone would put it; `q = 0.5` means half.

**What `q` is — and is not.** `q` is the city's population trajectory *relative to
the empire-wide trend*, under the same cross-sectional→temporal β-stability
assumption as the raw Layer B. It is **not** an absolute population trajectory:
recovering absolute population would require inverting the empire-common component
`g_shape` too, and `g_shape` conflates four drivers we cannot separate (Obs 98).
The residual sidesteps that conflation by differencing `g` out — which is exactly
why this inversion is well-posed where an absolute one is not.

**The `1/β > 1` amplification still applies** (empire 1/0.587 = **1.704**, Latin
1/0.733 = **1.364**) — but now it amplifies only the *city-relative* swings, which
are smaller and centred on the empire trend rather than tracking the empire-wide
late decline. The empire-vs-Latin β gap changes the amplitude of `q` materially
(state in write-up), so β is surfaced for sign-off (§6.i), as before.

**β_within is the defensible slope** (within-province cross-sectional slope from
the Mundlak decomposition — the closest cross-sectional analogue to a within-city
temporal relationship; β_between crosses zero and is unusable). Unchanged from the
raw Layer B reasoning.

---

## 4. Method

For the **268 target cities** this is a pure numpy transform of the loaded
posterior — **no MCMC, no new sampling whatsoever**:

1. Load `g/u/v/lam` + coords from the monolithic `.nc` (H5 reader).
2. Build the draw-wise residual `r = u + v` (H5 construction, §2).
3. For each β frame, resample `β_k` (seeded) and form `q = exp((1/β)·r)`.
4. Summarise per city: posterior median `q`-trajectory + 95 % credible band;
   peak-bin posterior; and the **headline contrast metric** — `q` at AD 250 (and
   AD 325) as a fraction of the city's `q`-peak, to set against the raw Layer B's
   ≈ 0 % collapse (§7).

**Two derived views (both free, same computation):**
- **Relative-to-empire (primary):** `q` itself (geom-mean 1; the honest core).
- **Peak-normalised overlay (optional):** `q / max_t q` (peak = 1), purely for
  visual comparability with the raw-Layer-B figures. This is a re-scaling for
  plotting, not a different quantity. (Decision §6.iii.)

**Reliability floor.** N\* = 300 (Layer-A calibration; coverage ≥ 0.90 and shape
r ≥ 0.90 only at N ≥ 300). Cities tagged `reliable` (34/268) vs `below-floor`
(234/268, shown but flagged) — inherited exactly from Layer A, as in H5 and the
raw Layer B.

---

## 5. Deliverables

1. `outputs/layerb-residual-trajectories-<frame>.nc` — per-city relative-to-empire
   posterior trajectories (`q` median + 95 % band; peak-bin; `reliable` flag; N),
   `empire` and `latin`.
2. `outputs/layerb-residual-summary.json` — per-frame, per-city peak-bin and the
   AD-250 / AD-325 fraction-of-peak contrast metrics; corpus medians; β frame;
   seed; sha256 of the input `.nc`; provenance.
3. Figures:
   - `layerb-residual-vs-raw.png` — the headline: median relative-to-empire
     trajectory (this run) overlaid on the median raw Layer B trajectory
     (`runs/2026-06-16-…/outputs/layerb-trajectories-empire.nc`), showing the
     spurious post-AD-250 collapse vanishing once `g` is removed.
   - `layerb-residual-samples.png` — small-multiples of relative-to-empire
     trajectories for a sample of reliable cities.
   - `layerb-residual-amplitude-overlay.png` — empire-vs-Latin β amplitude.
4. `REPORT.md` — methods, the §7 validation outcomes, the relative-to-empire
   framing (Obs 101), and the caveats (§10) carried verbatim.

---

## 6. Design decisions (recommendations — confirm at §11)

**(i) β frame → recommend empire primary + Latin overlay** (identical to the raw
Layer B, for direct comparability; both posteriors propagated draw-wise). The
diagnostic-unit framing (Obs 101, Latin-minus-Roma) is about the *city set*, not
the β slope; H5 §4 already showed the Latin-minus-Roma decomposition ≈
all-provinces, so the residual is materially the same. *Confirm.*

**(ii) Residual composition → recommend `u_shape + v_shape` primary** (remove the
empire-common component only; keep the province + city deviation as the
residual). This matches the beacon's explicit brief, Decision 13's two-way
"empire habit + city residual", and the H5 residual exactly. **Optional secondary
overlay: `v_shape`-only** (remove empire *and* province; the purely city-specific
deviation) — cheap, and worth showing because it answers "is a city's deviation
its own or its province's?". *Confirm primary; opt in/out of the v-only overlay.*

**(iii) Normalisation → recommend relative-to-empire (geom-mean = 1) as primary**
(the natural zero-sum scale; it preserves the "no spurious collapse" reading,
which peak-normalising would hide). Peak = 1 available as a plotting overlay for
comparability with the raw-Layer-B figures. *Confirm.*

**(iv) Validation mode → descriptive-only, no thresholds** (Decision 13; prereg
default). See §7. *Confirm.*

---

## 7. Validation (descriptive; no pass/fail)

The raw Layer B validated the *full* inversion against the independently-dated
anchors **Ostia** and **Pompeii** (Obs 96: clean pass, AD-125–150 apogee P = 0.99;
AD-79 terminus, post-79 mass 0.000). Two points govern validation here:

- **The anchors cannot be residual-decomposed, and that is stated, not worked
  around.** Ostia and Pompeii are *not* in the 268-city monolithic fit (they are
  large anchors, fit standalone). A standalone single-city fit has **no
  empire-common `g_shape` tier** to remove, so there is no residual `u+v` to
  invert for them. We therefore do **not** re-run the anchor gate here; the
  full-inversion anchor validation (Obs 96) stands as the upstream check, and we
  cite it. (No new MCMC — this is the reason there is none.)

- **Within-set validation = the foundation-terminus check (99 cities).** H5
  matched Hanson `Start Date` to all 268 cities; **99 are founded within the
  envelope** (Start > 50 BC) and bind. H5 found median pre-foundation raw mass
  **0.07 %**, clean bar archaeologically-explicable frontier-military sites
  (Corbridge, Cirencester, Carlisle, …). We confirm the **relative-to-empire**
  trajectory `q` likewise carries ~zero mass before foundation for these cities
  (the transform is monotone in `r`, so the terminus is preserved) — a within-set
  independent anchor that *does* apply to the residual object.

- **The headline diagnostic (this is the point of the run): the spurious universal
  collapse disappears.** Report the corpus distribution of `q` at AD 250 / AD 325
  as a fraction of `q`-peak, set directly against the raw Layer B's median ≈ 0 %
  collapse. The *expectation* (and the well-posedness claim) is that the
  relative-to-empire trajectory does **not** show a near-universal collapse — once
  the empire-wide late decline (in `g`) is removed, what remains is city-specific
  divergence from the empire trend, which has no reason to be uniformly
  catastrophic. A few cities will rise above and others fall below the empire
  trend post-AD-250; that spread *is* the demography-isolating signal. Reported
  descriptively (Decision 13), not as a thresholded result.

---

## 8. Compute plan

- **Host: sapphire** (default; inputs already staged + sha256-verified there from
  the raw Layer B and H5 runs — the monolithic `.nc`, the two H3a β `.nc`, the
  dataprep `city-index.parquet`; versions per the raw-Layer-B spec §3). zbook is a
  viable fallback (identical stack + data).
- **Cost:** a numpy transform over a loaded posterior + the β resample — **minutes,
  zero MCMC** (the anchor re-fits the raw Layer B needed are not repeated here, §7).
- **Reproducibility:** seed fixed (reuse `20260616` for cross-run comparability, or
  a fresh seed — note in summary); input `.nc` sha256 recorded; β resample
  deterministic from the seed.
- **No model/LLM API calls** (flagged for the API review gate: this stage spends no
  API budget; sapphire CPU only).

---

## 9. Code plan

A single self-contained script `code/layerb_residual_invert.py` in this run dir,
composed from two **already-audited** sources (minimal new logic):

- Residual construction — **reuse** `runs/2026-06-17-s5-h5-habit-removed/code/
  h5_habit_removed.py::load_posterior` + the `residual = v + u_pad[:, urows, :]`
  block (import or copy verbatim with attribution; bit-identical to H5).
- β draws + `1/β` resample — **reuse** `runs/2026-06-16-s5-layer-b-beta-inversion/
  code/layerb_invert.py::load_beta_draws` + the seeded `rng` resample idiom.
- New: `invert_residual(r, beta_draws, seed)` → `q = exp((1/β)·r)`; `summarise()`
  (medians, bands, peak-bin, AD-250/325 fraction-of-peak); `save_trajectories()`;
  the three plots; `foundation_terminus_check()` (reuse H5's Hanson `Start Date`
  join).
- A **self-test / regression guard:** assert that, on a draw where `g` were added
  back, `exp((1/β)·(g+r))` reproduces the raw Layer B relative-shape for a spot
  city — i.e. that the only difference from Obs 96 is the removal of `g`. (Cheap;
  catches a wiring error in the decomposition.)

`/audit` (or a focused review) of the script **before** launch, per the standing
pre-launch rule.

---

## 10. Critical-friend caveats (carry into the write-up)

1. **Relative, not absolute.** `q` is population *relative to the empire-wide
   trend*, not absolute population. Absolute population is not recoverable because
   the empire-common component conflates four drivers (Obs 98). State plainly.
2. **The residual is not pure demography either** (Obs 98 caveat). `u+v` is "the
   city's deviation from the empire norm" — it includes city/province-level
   demographic, economic, taphonomic, *and* habit variation. The claim is only
   that it is **free of the empire-common confound**, not that it is clean
   population. This is the honest ceiling of the method.
3. **Cross-sectional → temporal.** Same prereg-flagged "strong assumption" as the
   raw Layer B: β_within (a cross-sectional slope) is used as a within-city-over-
   time relationship. β_within is the least-bad analogue; the output is
   illustrative-shape.
4. **`1/β` amplification.** Magnifies city-relative swings; the β frame changes
   amplitude materially (peak timing/shape unaffected).
5. **Posterior independence.** Layer-A and H3a posteriors combined under
   independence (separate fits, overlapping city sets) — a minor simplification
   for a global structural β.
6. **N\* = 300 floor.** 34/268 reliable; the rest flagged. Inherited from Layer A.
7. **Within-sample empire trend.** `g_shape` is the 268-city within-sample empire
   shape (a proxy for the true empire-wide common component), so "relative to the
   empire trend" means relative to *this corpus's* common shape.

---

## 11. Framing for the write-up (Obs 101)

Results-section language is empirical and model-conditional: the deliverable is a
per-city **"population trajectory relative to the empire-wide common temporal
component"** — *not* "habit-corrected population". The four candidate drivers of
the removed component, and the epigraphic-habit interpretation, stay in the
discussion (Obs 98 / Obs 101). Hanson is not the anchor here (the residual is
level-free by construction); any bridge to Hanson population is an interpretive
step reserved for the discussion.

---

## 12. Pre-launch sign-off checklist (Shawn)

- [ ] **(i)** β frame: empire primary + Latin overlay.
- [ ] **(ii)** Residual composition: `u+v` primary; v-only overlay yes/no.
- [ ] **(iii)** Normalisation: relative-to-empire (geom-mean 1) primary; peak=1
  plotting overlay.
- [ ] **(iv)** Validation: descriptive-only; foundation-terminus (99 cities) +
  collapse-disappearance contrast; anchors *not* re-run (cannot be
  residual-decomposed — confirm this is acceptable).
- [ ] **Seed:** reuse `20260616` (cross-run comparability) vs a fresh seed.
- [ ] Run script `code/layerb_residual_invert.py` written + reviewed (`/audit`
  before execution).
- [ ] Final sign-off to launch.
