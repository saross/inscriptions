# D13 α-as-translator sensitivity — REPORT

> The lodged preregistered exploratory/sensitivity analysis for H3a
> (`planning/preregistration-draft.md:382`;
> `planning/osf-supplementary-2026-05-20.md:349`): include per-city posterior
> mixture α as an additional covariate in the within-between (Mundlak) negative-
> binomial regression (NBR) and test whether the within-province population–epigraphy
> coefficient (β_within) shifts meaningfully. It informs whether the Hanson
> population–inscription scaling is confounded by epigraphic-habit (editorial-
> convention) intensity.
>
> **This is an exploratory/sensitivity analysis (prereg §5 block), not confirmatory
> — no confirmatory decision rule rides on it.** It is, however, an outstanding
> preregistered obligation to report.
>
> Generated from the run artefacts
> (`outputs/h3a-alpha-translator-results.json`, `outputs/city-alpha-summary.json`,
> `outputs/reconciliation-gate.json`). Spec:
> `runs/2026-06-19-d13-alpha-as-translator/spec.md` (Option A, prereg-literal,
> standalone per-city α at N ≥ 100, with uncertainty propagation). Author: Claude
> Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-19. UK/Australian
> English; Oxford comma.

---

## Verdict

**β_within does NOT shift meaningfully when per-city α_c is added.** The
within-province population–epigraphy scaling is **not** confounded by per-city
editorial-convention intensity. This is the *expected* null (the province-level
proxy, Obs 94, already found α uncorrelated with population, Spearman −0.11); D13
confirms it at the **city** level — the lodged deliverable.

| Quantity | Base (163 cities) | + α_c (S2a) | Shift |
|---|---|---|---|
| **β_within** (median [95 % CI]) | **+0.431** [+0.307, +0.557] | **+0.422** [+0.304, +0.542] | **−0.009 (0.14·posterior SD)** |
| γ (α_c coefficient) | — | −0.181 [−0.290, −0.075] | (non-zero) |
| f_within (median [95 % CI]) | 0.685 [0.399, 0.950] | 0.637 [0.374, 0.863] | median −0.048 (< 0.063) |

The β_within shift is **0.14 posterior standard deviations** — negligible — with the
two credible intervals overlapping almost entirely. γ is non-zero (α_c carries a
small *independent* signal on counts), but it does not translate into a shift of the
population–epigraphy scaling. The f_within median shift (−0.048) is **below** the
pre-stated D11 materiality threshold of 0.063 (see §6 for why the CI-edge criterion
nominally trips and why that is mechanical, not substantive).

**Read against the §2 identifiability caveat (below): this null is the honest and
the robust answer.** The multiple-imputation layer (S2b) shows the per-city α
unreliability does **not** inflate the β_within uncertainty (between-imputation
variance ≈ 0; fraction of missing information 0.5 %), so the null is not an artefact
of wide, prior-dominated per-city posteriors hiding a real effect.

---

## 1. Feasibility census (reproduced)

Latin frame `data/processed/city_level_for_h3a_latin.parquet` (817 cities, 39
provinces). Re-computed by this run; reproduces the spec §2 table exactly.

| Threshold | Cities | Provinces | Provinces with ≥ 2 such cities |
|---|---|---|---|
| N ≥ 100 | **163** | 36 | **26** (regression-feasible) |
| N ≥ 500 | **18** | 11 | **2** |
| N ≥ 1000 | 8 | 6 | 1 |
| N ≥ 2000 | 5 | 4 | 1 |

(N is the H3a `inscription_count`.)

---

## 2. The identifiability tension (foregrounded, not hidden)

The prereg's "N ≥ 100 identifies α_c, ~200 cities" assumption **predates** the
project's own measured reachability map (Decision 34;
`runs/2026-06-03-small-n-reachability/outputs/REPORT.md`), which found that
**standalone subset-specific α recovery is only ~16 % reliable at N = 100**
(|α-bias| ≈ 0.135), with the reliable floor at **N ≈ 500–2000**. So per-city α at
the sizes where we have cities is largely prior-influenced / biased.

The irreducible tension: where the within-province regression is feasible (N ≥ 100,
26 provinces with ≥ 2 cities), α_c is unreliable; where α_c is reliable (N ≥ 500),
within-province leverage is gone (only **2** provinces have ≥ 2 such cities). **This
analysis cannot escape that tension — it handles it honestly:**

- **(a) it propagates the per-city α posterior uncertainty** into the NBR (S2b
  multiple imputation), so unreliability would surface as wider coefficient
  uncertainty rather than false precision;
- **(b) it annotates every city** by whether it clears the N ≥ 500 reliability floor
  (18 reliable, 145 caveated; `reliable` flag in every per-city JSON);
- **(c) it cross-checks against the province-level proxy** (Obs 94) and reports a
  reliable-α (N ≥ 500) descriptive cross-check.

The N ≥ 500 cross-check (S2c-i) is explicitly **within-province-leverage-thin**: with
18 cities in 11 provinces (only 2 with ≥ 2 cities) it is a *descriptive* read, not a
within-province regression. **The report must not, and does not, present S2c-i as a
within-province confirmation.**

---

## 3. Stage 1 — per-city α (the new per-city mixture build)

### Corpus reconciliation gate (REQUIRED, pre-fit) — PASSED

The whole analysis depends on the per-city mixture being fit on the **same
inscriptions H3a counted**. The gate (`outputs/reconciliation-gate.json`) verified,
for **all 163 cities**, that the plain mixture-subset row count
(`df[urban_context_city == city]`, the filter the mixture uses) **equals the H3a
`inscription_count` exactly** (0 failures; both built on the identical 50 BC – AD 350
window, the same Latin frame). For these 163 cities the plain city filter coincides
with H3a's `~rome & has_hanson` count — none of them carry rows lacking a Hanson
population estimate, and none is Rome.

The third leg of the recorded triple, the **aoristic-effective** `n_rows`, is lower
than the raw count (median 95 %, range 56–100 % of the count) because
`h2_lib.aoristic_spa` drops zero/negative-width (year-precise) rows and clips to the
envelope — **the exact convention the lodged primary p_gen was fit on** (supp-wave
M1 caveat). This is expected and explainable, not a corpus mismatch.

### Model and run

The production cross-classified `library` deconvolution
(`joint_lib.build_model_cross_classified(pconv_mode="library")`) under the **adopted
re-derived θ prior** (θ_conv ≈ 0.930, θ_gen ≈ 0.025, κ = 40), fit **standalone per
city** — the production refit (`runs/2026-06-13-cc-production-refit/`) pointed at
cities. All deconvolution machinery (`fit_one` structure, the slab library, adopted
θ, aoristic SPA, alignment indicator, largest-remainder, the convergence gate) is
reused verbatim; no lodged module was modified. Run on sapphire, n_jobs = 12, ~8 min.
Base seed `D13_BASE_SEED = 20260619`; per-city seed = base + city index.

### Stage-1 convergence and α distribution

- **Convergence: 162 / 163 (99.4 %) pass** — well within the > 10 % hard-stop (16
  cities). The single failure is **Micia** (max R̂ = 1.13, min ESS-bulk = 23, N = 181,
  caveated tier); it is recorded transparently with `convergence_pass = false` and
  does not drive any Stage-2 result (it is one caveated city among 163). Six cities
  carry 1–14 trivial divergences with R̂ ≈ 1.00 (all pass).
- **Per-city α distribution:** median **0.769**, mean **0.704**, SD **0.233**, range
  [0.002, 0.989], IQR shown in `city-alpha-summary.json`. This is consistent with the
  province-level α (Obs 94: mean 0.677, SD 0.246).
- **Reachability:** 18 cities **reliable** (N ≥ 500), 145 **caveated** (N < 500).

The full α posterior draw vector per city (8,000 draws) is persisted to
`outputs/alpha-draws/<city>-alpha.npz` (gitignored; the Stage-2 multiple-imputation
hand-off).

---

## 4. Stage 2 — augmented H3a NBR + propagation

The H3a Mundlak NBR (`build_model`, `f_within`, `summarise_f` from
`runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py`, reused verbatim; sampler
tune = 6,000, draws = 3,000, 4 chains, target_accept = 0.97) augmented with one
additive term:

    log_mu = α0 + α_prov[prov] + β_within·within + β_between·between + γ·α_c_std

The **base** comparison is re-fit on the **identical 163-city Latin subset** (Mundlak
centring recomputed over the subset, province index re-indexed), so the *only*
difference between base and augmented is the α_c term. All Stage-2 fits converged
(max R̂ = 1.00, 0 divergences).

### S2a — prereg-literal primary (standardised posterior-MEDIAN α_c)

| | β_within | γ (α_c) | f_within |
|---|---|---|---|
| Base 163 | +0.431 [+0.307, +0.557] | — | 0.685 [0.399, 0.950] |
| **S2a (+ α_c)** | **+0.422** [+0.304, +0.542] | **−0.181** [−0.290, −0.075] | 0.637 [0.374, 0.863] |
| Shift vs base | **−0.009 (0.142·post SD)** | — | median −0.048; CI-edge max Δ 0.087 |

### S2b — multiple imputation (M = 50; the §2 honesty layer)

Draw 50 per-city α-vectors from the Stage-1 posteriors (one independent posterior
draw per city per imputation), re-fit the augmented NBR on each, pool via Rubin's
rules.

| Pooled | Estimate | 95 % CI | Between-imp. var | FMI |
|---|---|---|---|---|
| **β_within** | **+0.422** | [+0.303, +0.542] | ≈ 0.0000 | **0.5 %** |
| γ (α_c) | −0.180 | [−0.289, −0.071] | 0.0002 | 5.1 % |
| f_within | 0.637 | [0.388, 0.886] | 0.0002 | 1.3 % |

**The multiple-imputation result is decisive for the §2 caveat:** the
between-imputation variance for β_within is essentially zero, and the fraction of
missing information is **0.5 %**. The reachability-driven per-city α unreliability
(§2) does **not** propagate into β_within uncertainty — the β_within CI is barely
wider than the point-median S2a CI. So the null is not a wide-posterior artefact: the
data simply do not place α_c on the population–epigraphy scaling channel.

### S2c — reachability robustness

**(i) N ≥ 500 reliable-α cross-check (descriptive; within-province-leverage-thin).**
18 cities, 11 provinces, **only 2 with ≥ 2 cities** — flagged descriptive, NOT a
within-province regression. β_within +0.271 [−0.212, +0.723] (base) → +0.286
[−0.216, +0.733] (augmented); γ = −0.103 [−0.511, +0.283]. The β_within is flat and
its CI spans zero (the leverage is gone, exactly as §2 predicts); consistent with the
null, but it carries no within-province inferential weight on its own.

**(ii) City-level α_c-vs-population proxy (the Obs 94 extension).** The implied shift
in the Hanson scaling exponent from replacing raw count N with genuine count α·N is
the slope of log(α) on log(population) across the 163 cities:

| Statistic | Value |
|---|---|
| Spearman (α, log pop) | **−0.107** (cf. Obs 94 province-level −0.11) |
| Pearson (α, log pop) | −0.060 |
| implied Δβ — OLS | −0.036 [−0.147, +0.061] |
| implied Δβ — **Theil-Sen (robust)** | **−0.021 [−0.057, +0.009]** |

The robust slope is flat and its CI includes 0. See
`outputs/figures/fig-alpha-vs-population-city.png` — α scatters widely at every
population level with no trend; the city-level picture matches the province-level
Obs 94 proxy.

---

## 5. Cross-check against Obs 94 (the province-level proxy)

D13 is the **city-level** version of the test Obs 94
(`runs/2026-06-16-deconv-leverage-diagnostic/`) ran at the province/region level.
The two agree:

| | Obs 94 (26 province/region units) | D13 (163 cities) |
|---|---|---|
| Spearman (α, log pop) | −0.11 | **−0.107** |
| implied Δβ, robust (Theil-Sen) | −0.030 | **−0.021** |
| α mean (SD) | 0.677 (0.246) | 0.704 (0.233) |
| Verdict | flat ⇒ no confound | flat ⇒ no confound |

D13 adds what Obs 94 explicitly flagged it could not deliver: the **direct
city-level regression test** (β_within in/out), with the per-city α uncertainty
propagated. The conclusion is unchanged and now rests on the city-level evidence the
prereg asked for.

---

## 6. The materiality yardstick and why f_within nominally trips it

**Pre-stated (spec §4, before seeing the result):** a f_within posterior-median/CI
shift ≥ **0.063** is "material" (the D11 precedent; continuity 2026-06-16 records D11
max CI shift 0.047 < 0.063 → no material divergence). Additionally, β_within shift
is judged against its posterior SD and CI overlap.

The automated flag reports f_within "material = True" — but **only because the
upper-CI edge moves 0.087** (0.950 → 0.863). The f_within **median** moves just
−0.048 (below 0.063), and **β_within — the actual prereg quantity** ("test whether
the within-province β estimate shifts meaningfully") — moves 0.14 posterior SD, which
is not meaningful by any reading.

The f_within CI-edge movement is **mechanical, not substantive.** f_within =
Var(β_within·within) / Var(log_mu). Adding the γ·α_c_std term puts additional
explained variance into the **denominator** Var(log_mu) (α_c genuinely predicts some
count variation, γ ≠ 0), which slightly *lowers* f_within and tightens its upper edge
**without β_within moving.** The numerator (driven by β_within) is essentially
unchanged. So the f_within shift is the footprint of α_c being a non-trivial
predictor, not of the population–epigraphy scaling weakening. **On the prereg's own
terms — β_within — the answer is a clear null.**

---

## 7. Reproduce

```bash
# Stage 1 (sapphire; ~8 min, n_jobs 12) — per-city α
PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch PYTENSOR_FLAGS=mode=FAST_RUN \
    taskset -c 0-11 uv run python code/run_city_alpha.py --n-jobs 12

# Stage 2 (sapphire; base + S2a + M=50 MI + S2c) — augmented NBR
PATH=$HOME/.local/bin:$PATH PYTENSOR_FLAGS=mode=FAST_RUN \
    uv run python code/h3a_alpha_translator.py --n-imputations 50
```

---

## Appendix — DRAFT Obs candidate (NOT yet appended to working-notes.md)

> **Draft only.** Per the brief, this is *not* appended to `working-notes.md`, and
> `/observe` is *not* run — the research-record finalisation is the main thread's job
> after review.

---

**Obs NN — 2026-06-19 [SENSITIVITY / RESULT]: D13 α-as-translator — the H3a
within-province population–epigraphy scaling is NOT confounded by per-city
editorial-convention intensity (city-level confirmation of Obs 94).**

The lodged preregistered α-as-translator sensitivity (prereg §5; not confirmatory)
adds per-city posterior mixture fraction α_c as a covariate to the H3a Mundlak NBR
and tests whether β_within shifts. It does not. On the 163 Latin-frame cities with
N ≥ 100, fit standalone under the production cc-library deconvolution (adopted θ;
162/163 converge): adding standardised posterior-median α_c moves **β_within from
+0.431 to +0.422 — a 0.14-posterior-SD shift, with credible intervals essentially
overlapping.** γ (the α_c coefficient) is non-zero (−0.181 [−0.290, −0.075]), so α_c
carries a small *independent* signal on counts, but it does not load on the
population–epigraphy channel. f_within moves −0.048 (median; below the pre-stated
D11 materiality threshold of 0.063); its upper-CI edge moves 0.087, but that is the
mechanical footprint of α_c adding denominator variance, not the scaling weakening.

**The honesty layer is decisive.** Multiple imputation (M = 50, drawing per-city α
from the Stage-1 posteriors, Rubin pooling) gives pooled β_within +0.422 [0.303,
0.542] with **between-imputation variance ≈ 0 and fraction of missing information
0.5 %** — the reachability-driven per-city α unreliability (§2: standalone α is only
~16 % reliable at N = 100; reliable floor N ≈ 500) does **not** inflate the β_within
CI. The null is therefore robust, not a wide-posterior artefact.

This is the **city-level** confirmation of the province-level proxy in **Obs 94**
(deconvolution does not change H3a; α uncorrelated with population). The two agree
tightly: city-level Spearman(α, log pop) = −0.107 (Obs 94: −0.11); robust Theil-Sen
implied Δβ = −0.021 [−0.057, +0.009] (Obs 94: −0.030). The identifiability tension
Obs 94 flagged — where the within-province regression is feasible (N ≥ 100) α_c is
unreliable, where α_c is reliable (N ≥ 500) within-province leverage is gone (2
provinces with ≥ 2 cities) — is handled honestly here by propagating the per-city α
uncertainty, annotating every city by the N ≥ 500 reliability floor, and reporting an
explicitly-descriptive N ≥ 500 cross-check (β_within +0.271 → +0.286, flat).

**Why it matters:** the lodged H3a primary (raw-count Hanson scaling, Decision 22/35)
is vindicated not only by preregistration but on the evidence — the epigraphic-habit
confound the sensitivity was designed to detect is absent at the city level. The
D13 preregistered obligation is discharged.

Artefacts: `runs/2026-06-19-d13-alpha-as-translator/outputs/` (D13-REPORT.md,
h3a-alpha-translator-results.json, city-alpha-summary.json,
figures/fig-alpha-vs-population-city.png). Cross-references Obs 94.
