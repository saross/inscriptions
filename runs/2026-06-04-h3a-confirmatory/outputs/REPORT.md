# H3a confirmatory result — REPORT

**Status:** CONFIRMATORY — signed off (Decision 37) and lodged via OSF Amendment
02 (2026-06-06). This supersedes the original "PRELIMINARY — pending sign-off"
stamp this file carried at the 2026-06-04 blind run.

> **⚠ FRAME RELABELLING — Amendment 02 (2026-06-06), labels only, NO numbers
> changed.** This report was written on 2026-06-04, *before* the Latin-primary
> reframe. At that date the empire-wide (1,044-city) frame was the PRIMARY and
> the Latin (817-city) frame was "Sensitivity B". **OSF Amendment 02 /
> Decision 36 reframed the lodged primary hypothesis-testing frame to the
> Latin-speaking provinces (817 cities, 39 provinces); the empire-wide frame is
> now secondary / context** (with the LIRE-coverage caveat). Read every
> "PRIMARY" label below that refers to the 1,044-city empire frame as
> **secondary / context**, and the "Sensitivity B — Latin-only" frame as the
> **lodged primary**. **All numbers are unchanged and both frames are
> SUPPORTED** (empire f_within 0.299 [0.240, 0.365]; Latin f_within 0.480
> [0.401, 0.566]); only the frame *labels* are re-cut here to match the lodged
> Amendment 02. The relabelling is the D1/AM02 housekeeping fix flagged in
> `planning/prereg-obligations-coverage-sweep-2026-06-20.md`.

**Run:** `runs/2026-06-04-h3a-confirmatory/` · branch `main` · compute host
`sapphire` · LIRE v3.0 · date window 50 BC – AD 350 (overlap).

**Model (prereg §3 / design artefact §1):** Bayesian within-between (Mundlak)
negative-binomial regression, non-centred province random intercepts, fit in
pymc 6.0.1 (NUTS, 4 chains, tune 6,000, draws 3,000, `target_accept` 0.97,
seed 20260604).

---

## 0. Blind-run certification and contamination disclosure

**Certification.** I derived every reported number from the preregistration,
the data, and the design artefact; I read no preliminary result. Specifically,
I did not open anything under `runs/2026-05-21-talk-prep/outputs/`,
`planning/conference-talk-rac-trac-2026/`, any `qa-report-*`, anything under
`runs/2026-05-26-letter-count-probe/outputs/`, and I did not read
`docs/notes/working-notes.md`, `docs/notes/reflections/continuity.md`, or
`planning/decision-log.md` for any quoted `f_within` value. The model code
(`05-h3a-bayesian-mundlak.py`, `01-filter-and-prep.py`) and `h3a_brms_shadow.R`
were read as implementation references only; they compute, not hard-code,
results.

**Contamination disclosure (design artefact §0).** A *preliminary* H3a fit was
run at the 2026-05-21 RAC-TRAC talk-prep as exploratory post-lodgement work; it
produced a preliminary `f_within` posterior. The non-blind thread that wrote the
spec has seen that value. This blind run is a mitigation, not a claim of zero
prior exposure: the estimand was previously seen at exploratory talk-prep. If a
reviewer judges that material, the honest labelling is "pre-specified analysis,
estimand previously seen at exploratory talk-prep".

---

## 1. Headline result — H3a `f_within` (empire frame; secondary/context under Amendment 02)

> *Amendment 02: the empire-wide 1,044-city frame below was the 2026-06-04
> PRIMARY; it is now the **secondary / context** frame. The lodged primary is
> the Latin frame in §2 ("Sensitivity B"). Numbers unchanged.*

| Quantity | Value |
|---|---|
| **`f_within` (unweighted, primary)** | **median 0.299, 95% CI [0.240, 0.365]** |
| **Three-way verdict (threshold 0.10)** | **SUPPORTED** (95% CI wholly above 0.10) |
| P(`f_within` > 0.05) | 1.000 |
| P(`f_within` > 0.10) | 1.000 |
| P(`f_within` > 0.20) | 1.000 |

The within-province population-attributable variance fraction is supported: on
the latent log scale, within-province population deviation accounts for ~30% of
the variance in expected per-city inscription counts, and the 95% credible
interval lies entirely above the preregistered 0.10 threshold. The probability
ladder is saturated (every rung at or above 0.9996).

### Weighted variants (Decision 32; supplementary)

| Variant | median | 95% CI | verdict |
|---|---|---|---|
| Population-weighted (`w_c = pop_c`) | 0.494 | [0.395, 0.609] | supported |
| Inscription-weighted (`w_c = y_c`) | 0.419 | [0.335, 0.514] | supported |

Both weighted variants are higher than the unweighted primary and also
SUPPORTED — within-population variance explains an even larger share of the
population- and inscription-weighted log-count variance (i.e. among the larger,
more epigraphically active cities).

### Coefficients

| Parameter | median | 95% CI |
|---|---|---|
| β_within | 0.587 | [0.519, 0.657] |
| β_between | −0.242 | [−0.701, 0.238] (crosses 0; not independently identifiable per prereg §9) |
| σ_prov | 1.078 | [0.872, 1.353] |
| dispersion (α) | 0.688 | [0.635, 0.744] |

---

## 2. Sensitivities

### Sensitivity A — with-zeros (structural zeros)

**0 structural zeros added.** All 1,044 Hanson-matched (Rome-excluded) cities in
LIRE v3.0 have ≥ 1 date-window inscription — verified directly: the Hanson-city
pool (Rome-excluded, any row) is exactly 1,044, and all 1,044 survive the full
geo+temporal+envelope filter. The with-zeros sample is therefore **identical to
the primary**, so it was not re-fit. This resolves the launch-spec open
sub-question (§3a) empirically: under the realised data, options (i) and (ii)
coincide.

### Sensitivity B — Latin-only (817 cities) — *= the LODGED PRIMARY frame under Amendment 02*

> *Amendment 02 / Decision 36: this Latin-only frame is the **lodged primary**
> hypothesis-testing frame. It is labelled "Sensitivity B" here only because the
> report predates the reframe; the numbers below are the lodged primary H3a
> result. Numbers unchanged.*

| Quantity | Value |
|---|---|
| n cities / provinces | 817 / 39 |
| `f_within` (unweighted) | median 0.480, 95% CI [0.401, 0.566] |
| verdict | SUPPORTED |
| β_within | 0.733 [0.648, 0.820] |

Restricting to Latin-speaking provinces (the prereg's "~815"; realised 817 — see
§4) *strengthens* the within-province population effect (f_within rises from
0.299 to 0.480, β_within from 0.587 to 0.733). The conclusion is robust to the
linguistic stratification. **Under Amendment 02 this Latin result is the lodged
primary; the empire 0.299 in §1 is the secondary/context comparator.**

### Sensitivity C — standardisation

f_within is scale-invariant and matches the primary (0.298 vs 0.299), as it
must. The standardised β_within (0.636) back-transforms to 0.586 (predictor SD
1.085), matching the unstandardised primary (0.587). β stability confirmed; the
weakly-informative `Normal(0,1)` priors behave as intended under the prereg's
unstandardised scaling.

---

## 3. Bayesian R² and the Hanson OLS comparator

| Quantity | Value |
|---|---|
| Bayesian R² (response-scale; brms-comparable) | 0.133 [0.091, 0.201] |
| Bayesian R² (latent-scale linear-predictor) | 0.473 [0.434, 0.509] |
| brms `bayes_R2` (response-scale, cross-check) | 0.136 [0.092, 0.199] |
| OLS log-log slope (per-city, unweighted) | **0.284** (SE 0.045; 95% CI [0.195, 0.373]); R² 0.036 |
| Hanson, Ortman & Lobo / Hanson 2021 comparator β | 0.672 |

The Bayesian R² (Gelman, Goodrich, Gabry & Vehtari 2019) is reported on both the
response scale (matching `brms::bayes_R2` within Monte-Carlo noise — 0.133 vs
0.136) and the latent linear-predictor scale (prereg "full-model latent-scale").
The OLS log-log slope of 0.284 is well below the Hanson β = 0.672 — the naive
pooled per-city population–count scaling exponent in this date-windowed,
Rome-excluded LIRE sample is much shallower than Hanson's super-linear urban
scaling, and the OLS fit is weak (R² 0.036), which is precisely why the Mundlak
decomposition (separating within- from between-province scaling) is the
preregistered confirmatory specification rather than a pooled OLS.

---

## 4. The 1,044-vs-815 reconciliation

The prereg text spec ("all cities with Hanson population estimates, Rome
excluded") yields **1,044** unique cities on LIRE v3.0 — the primary sample. The
prereg's parenthetical "~815" was a stale 2024-notebook figure that additionally
applied a Latin-province filter via a hand-curated province→language dictionary
(notebook cell 54), not a data column. That dictionary was externalised into a
tracked CSV (`runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`),
normalised to LIRE v3.0's `province` spellings (casing, `/ Regio` vs `(Regio)`,
and synonym pairs such as `Aquitani(c)a`~`Aquitania`,
`Pontus et Bithynia`~`Bithynia et Pontus`). Applied to the 1,044 primary cities
it gives **817 Latin / 222 Greek / 5 unassigned** (the two `Belgica | Germania …`
uncertainty markers the notebook deliberately left out), summing to 1,044. The
817 matches the prereg's "~815" within rounding; the mapping is unambiguous
(every present province is covered). The primary confirmatory result uses 1,044
(text-spec faithful); 817 is Sensitivity B.

---

## 5. Posterior-predictive check suite (design artefact §2–§6)

**Overall: MINOR (0 critical, 0 grey, 5 minor, 5 pass). No HALT; no model
revision; no amendment.** The five minor triggers are logged as caveats below.

| # | Check | Result | Severity |
|---|---|---|---|
| 1 | Proportion of zeros | pp 0.086 vs obs 0.0 (bound ≤ 0.02; abs-critical 0.10) | **minor** |
| 2 | Mean count | pp 66.9 vs obs 72.0 (7.0% dev; p_B 0.169) | pass |
| 3 | SD of counts | pp 157.2 vs obs 248.1 (36.7% dev; p_B 0.013) | **minor** |
| 4 | 95th percentile | pp 277.4 vs obs 271.7 (2.1% dev; p_B 0.557) | pass |
| 5 | Mean–variance ratio | pp/obs ratio 2.50× (band [0.5×, 2×]; p_B 0.991) | **minor** |
| 6 | Bayesian p-values (#2–#5) | SD p_B 0.013 and MVR p_B 0.991 outside [0.05, 0.95] | **minor** |
| 7 | Residual-vs-fitted slope | 0.040 (bound \|·\| < 0.10) | pass |
| 8 | Residual-vs-within-logpop slope | −0.003 (bound \|·\| < 0.10) | pass |
| 9 | Province residual dispersion | 4/48 provinces (n≥5) outside [0.5×,2×]; worst 1.62 / 0.34 | **minor** |
| 10 | Posterior-predictive Moran's I (k=8) | obs −0.002 within pp [−0.024, +0.024] | pass |

**Interpretation of the minor caveats.** The five minor triggers are a single
coherent story: a single-dispersion NBR fit to a very heavy-tailed count
distribution (obs SD 248, max 4,508) modestly **under-fits the spread of the
upper tail** — it generates fewer extreme cities than observed (SD 37% low) and
hence a mean–variance ratio at the 2× boundary, plus ~8.6% simulated zeros that
the observed (LIRE-sourced, ≥1 by construction) sample cannot have. Four of 48
provinces are mildly over/under-dispersed in residuals. Critically, the
**central tendency (#2 mean, #4 95th pct), the residual structure (#7, #8), and
the residual spatial autocorrelation (#10) all PASS** — the model captures the
location and the systematic structure well; only the extreme-tail *spread* is
under-modelled. None of this gates the confirmatory `f_within` verdict (design
artefact §7); it conditions interpretation as a caveat.

---

## 6. pymc ↔ brms cross-language agreement (shadow)

Run-local Mundlak brms shadow (`h3a_brms_shadow_mundlak.R`; brms 2.23.0 /
cmdstanr 0.9.0; same priors + the 1/shape HalfNormal(1) Jacobian correction;
4 chains, warmup 6,000, draws 3,000, `adapt_delta` 0.97). The committed
`scripts/h3a_brms_shadow.R` fits the *pooled* pre-Mundlak model
(`count ~ log_pop`), which cannot produce β_within/β_between; the run-local
script matches the confirmatory within-between spec so the agreement check is on
the actual estimands.

| Quantity | pymc | brms | Agreement |
|---|---|---|---|
| β_within | 0.587 | 0.587 | exact (within MC noise) |
| f_within median | 0.299 | 0.299 | exact |
| f_within 95% CI | [0.240, 0.365] | [0.238, 0.366] | match |
| Bayes R² (response) | 0.133 | 0.136 | match (MC noise) |
| β_between | −0.242 | −0.375 | both negative; brms estimate lies well inside the pymc 95% CI [−0.701, 0.238] |

brms convergence: max R̂ 1.0013, min ESS-bulk 1,853, 0 divergences. **No material
disagreement on the confirmatory result.** β_within and f_within match to 3–4
significant figures. β_between differs by ~0.13 — larger than pure Monte-Carlo
noise but well within both wide credible intervals, on a parameter the prereg
(§9) flags as not independently identifiable from province-level "everything
else". It does not affect the verdict, so no investigation beyond this note is
warranted; if Shawn wants the β_between difference chased down it would be a
follow-up, not a blocker.

---

## 7. H3c — residual spatial autocorrelation (Hanson 2021 replication)

**Confirmatory rule:** Moran's I > 0 at p < 0.05 in ≥ 2 of {k = 5, 8, 10}, on the
posterior-mean Pearson residual vector, k-NN row-standardised weights (libpysal),
999-permutation conditional inference (esda).

| k | Moran's I (posterior-mean resid) | p_sim (one-sided) | z | rule pass? | posterior I [2.5/50/97.5%] | frac > 0 |
|---|---|---|---|---|---|---|
| 5 | +0.0097 | 0.249 | +0.59 | no | [+0.012, +0.024, +0.039] | 1.000 |
| 8 | −0.0020 | 0.499 | −0.08 | no | [+0.001, +0.011, +0.024] | 0.985 |
| 10 | −0.0045 | 0.426 | −0.27 | no | [−0.002, +0.008, +0.021] | 0.946 |

**Verdict: NOT-SUPPORTED** (0/3 k-values pass). The Mundlak model's residuals
show **no significant spatial autocorrelation** — the posterior-mean residual
Moran's I is ≈ 0 at all three k and never permutation-significant. This is a
**clean non-replication** of Hanson 2021 (Table 7.4: residual Moran's I = 0.046,
z = 4.571, p < 0.0001).

**Caveat on the posterior I distribution.** The posterior distribution of I_s is
mostly *above* zero (frac > 0 = 1.0 / 0.985 / 0.946), and at k = 5 its 95%
interval is wholly positive. This does **not** rescue a replication claim: the
magnitudes are tiny (posterior median I ≤ 0.024, vs Hanson's 0.046), and the
*permutation test on the posterior-mean residual is not significant at any k*
(the quantity the confirmatory rule binds on). The positive posterior-I mass
reflects that individual-draw residual vectors are noisier than the denoised
posterior mean, inflating their apparent autocorrelation slightly; it is not
substantive spatial structure. Per the prereg's reporting discipline, H3c(ii) is
reported as **not supported** rather than as any grade of Hanson replication.
(The §3 three-case guardrail applies only when the rule passes; it does not here.)
PPC check #10 passes, so no tautology caveat is triggered.

---

## 8. Convergence diagnostics (all fits)

| Fit | max R̂ | min ESS-bulk | divergences | gate (R̂<1.01, ESS≥400, 0 div) |
|---|---|---|---|---|
| Primary (1,044) | 1.00 | 1,660 | 0 | PASS |
| Sensitivity C (standardised) | 1.00 | 1,617 | 0 | PASS |
| Sensitivity B (Latin, 817) | 1.00 | 2,038 | 0 | PASS |
| brms shadow | 1.0013 | 1,853 | 0 | PASS |

**Convergence note (gate discipline).** At the spec's starting settings
(tune 3,000 / draws 2,000 / `target_accept` 0.95) the global intercept α_0 (and
marginally β_between) landed at R̂ = 1.0100 — exactly at the strict `< 1.01` gate,
which fails. Per the spec ("raise tune / investigate; HALT if unmet — do NOT
relax the gate"), the remedy was **more sampling, not a looser gate**: tune
raised to 6,000, draws to 3,000, `target_accept` to 0.97 (the non-centred
parameterisation was already in place). The precise max R̂ then dropped to 1.00,
clearing the gate unambiguously. The gate was met by better sampling.

A transient `overflow encountered in dot` RuntimeWarning appeared during the
*standardised* fit's NUTS warmup; that fit nonetheless converged cleanly
(R̂ 1.00, ESS 1,617, 0 divergences), so it is a benign warmup-phase numerical
event that mass-matrix adaptation recovered from, not a result-affecting issue.

---

## 9. Prior-predictive thresholds (committed before the fit)

Committed in `outputs/prior-predictive-thresholds.json` BEFORE any posterior
fit (design artefact §2): `count_cap_p99` = 1.88 × 10⁹, `tail_count_bound` =
1.35 × 10¹¹ (these are deliberately loose sanity ceilings — the weakly-
informative `α_0 ~ N(0,5)` prior admits astronomically large tail counts by
design). The prior-sanity gate is on the **median** simulated per-city count =
1.0, comfortably within [0.1, 10⁴] — PASSED. The observed 95th percentile (271.7)
sits far below `tail_count_bound`, as required.

---

## 10. Realised sample counts

| Sample | n cities | n provinces |
|---|---|---|
| Primary (Hanson, Rome-excluded, ≥1 date-window insc) | **1,044** | 56 |
| Sensitivity A (with-zeros) | 1,044 (0 zeros added) | 56 |
| Sensitivity B (Latin-only) | **817** | 39 |
| Filtered LIRE rows | 180,609 (exact match to prereg) | — |

Row-level sanity (all exact): total 180,609; Rome 65,435; Rome-excluded 115,174;
Hanson-assigned 140,575.

---

## 11. Files

- Code: `runs/2026-06-04-h3a-confirmatory/code/{h3a_common.py, 01-data-prep.py,
  prior-predictive.py, 02-h3a-fit.py, 03-ppc.py, 04-h3c.py,
  h3a_brms_shadow_mundlak.R}`
- Data: `data/processed/city_level_for_h3a*.parquet`;
  `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`
- Results: `runs/2026-06-04-h3a-confirmatory/outputs/{h3a-results.json,
  ppc-results.json, h3c-results.json, prior-predictive-thresholds.json,
  sample-counts.json, h3a-posterior-summary-primary.csv, brms-shadow/}`
- Posteriors (NetCDF, on sapphire, gitignored — regenerable from seed + code):
  `outputs/idata-{primary,standardised,latin}.nc`

**Label:** all results above are **CONFIRMATORY — signed off (Decision 37) and
lodged via OSF Amendment 02 (2026-06-06).** The original "preliminary — pending
sign-off" stamp is superseded. Under Amendment 02 the **Latin (817-city) frame
is the lodged primary** and the empire-wide (1,044-city) frame is secondary /
context; see the relabelling banner at the top of this report. No numbers
changed in the relabelling.
