# H9 letter-mass H3a confirmatory — RESULTS

- **Status:** ✅ COMPLETE / EXECUTED 2026-06-18 (zbook-ubuntu, HEAD `2d95f62`;
  `run.log`). **Verdict: f_within SUPPORTED on every frame.** This report was
  added 2026-06-20 (pre-write-up uplift) from the persisted artefacts — the run
  had completed but its verdict previously lived only in commit `ec99343`
  ("results(h9): letter-mass H3a confirmatory — f_within supported (all frames)").
- **What H9 is.** The cross-sectional **confirmatory** H3a within-between
  (Mundlak) negative-binomial regression with **per-city letter-count mass** as
  the response (in place of inscription count). It mirrors the inscription-count
  H3a confirmatory run (`runs/2026-06-04-h3a-confirmatory/`) in every other
  respect; only the response variable changes. Promoted from exploratory H9 to a
  confirmatory letter-mass H3a by OSF Amendment 01 §A5.2 (the two-measure
  framework). **Scope:** the letter-mass *confirmatory* family is bounded to the
  cross-section; letter-mass *temporal/detection* analyses stay exploratory
  (Grid B FAIL + corpus-wide unreachable, A01 §A5.2).
- **Measure (lodged, A01 §A5.1):** per-city letter mass = summed Latin-A–Z
  `letter_count_conservative` (Greek excluded), over the city's
  date-window-filtered, Hanson-matched, Rome-excluded inscriptions.

---

## 1. Headline result — H9 f_within (PRIMARY = Latin-speaking provinces, Amendment 02)

| Quantity | Value |
|---|---|
| n cities / provinces | 817 / 39 |
| **f_within (unweighted, primary)** | **median 0.448, 95 % CI [0.364, 0.535]** |
| **Three-way verdict (threshold 0.10)** | **SUPPORTED** (95 % CI wholly above 0.10) |
| P(f_within > 0.05) / > 0.10 / > 0.20 | 1.000 / 1.000 / 1.000 |
| β_within | 0.681 [0.595, 0.769] |
| β_between | −0.018 [−0.518, 0.499] (crosses 0; reported descriptively) |

Within-province population deviation accounts for ~45 % of the latent-scale
variance in expected per-city **letter mass**; the 95 % credible interval lies
entirely above the preregistered 0.10 threshold and the probability ladder is
saturated. **Both content (letters) and acts (inscription count, the 2026-06-04
H3a run) corroborate within-province population–epigraphy scaling.**

### Weighted variants (Decision 32 analogue; supplementary)

| Variant | median | verdict |
|---|---|---|
| Population-weighted (`w_c = pop_c`) | 0.626 [0.510, 0.744] | SUPPORTED |
| Letter-weighted (`w_c = letter_mass_c`) | 0.607 [0.495, 0.720] | SUPPORTED |

Both weighted variants are higher than the unweighted primary and also
SUPPORTED (the natural letter-mass analogue of the H3a inscription-weighted
variant; BUILD-NOTES §2.3).

---

## 2. Convergence + sensitivities (all SUPPORTED / clean)

| Frame / sensitivity | n | f_within | convergence | verdict |
|---|---|---|---|---|
| **Latin (primary)** | 817 | 0.448 [0.364, 0.535] | R̂ 1.0000, min ESS 1,655, 0 div | **SUPPORTED** |
| Standardised predictors | 817 | 0.446 (scale-invariant ✓) | R̂ 1.0000, min ESS 3,473, 0 div | matches primary |
| Interpretive letter mass | 817 | 0.444 | R̂ 1.0000, min ESS 1,962, 0 div | SUPPORTED |
| **Empire (secondary/context)** | 1,044 | 0.356 [0.279, 0.441] | R̂ 1.0000, min ESS 1,745, 0 div | SUPPORTED |

The standardised f_within matches the primary (scale-invariant, as it must); the
interpretive-letter-mass sensitivity and the empire secondary frame both stay
SUPPORTED. The empire frame carries the LIRE-coverage caveat (Decision 36) and
is secondary/context under Amendment 02.

---

## 3. Bayesian R² and the OLS log-log comparator (SR1 content variant)

| Quantity | Value |
|---|---|
| Bayesian R² (response-scale) | 0.206 [0.133, 0.307] |
| Bayesian R² (latent-scale) | 0.382 [0.333, 0.429] |
| OLS log-log slope (per-city, unweighted) | **0.470** (SE 0.058; 95 % CI [0.356, 0.584]); R² 0.075, n 809 (8 zero-mass dropped) |
| Hanson 2021 inscription-count comparator β | 0.672 |

The letter-mass OLS log-log slope (0.470) is reported as the content variant of
SR1; under letter mass the slope is expected to differ from the inscription-count
β (content vs acts), so the Hanson 0.672 is a reference, not a target.

---

## 4. Posterior-predictive checks (10-check suite; overall MINOR)

0 critical, 0 grey, **2 minor**, 8 pass. Minor: #6 Bayesian p-values and #9
province residual dispersion (expected for the heavier-tailed letter response
under the count-pinned bounds; reported, not faulted, per A01 §A5.2). **#10
posterior-predictive Moran's I (k = 8) PASS** (no spatial-residual tautology).
No critical trigger → no PPC amendment trigger fired.

---

## 5. Caveats (carry into the write-up)

1. **Cross-section only.** The letter-mass *confirmatory* family is bounded to
   the cross-sectional H3a; letter-mass temporal/detection stays exploratory and
   is corpus-wide unreachable (Grid B FAIL; A01 §A5.2/§A5.5).
2. **8 zero-mass cities** (inscriptions present, no readable Latin A–Z letters)
   carry `letter_mass = 0`; they remain in the NBR frame but are dropped from the
   OLS log-log comparator (log undefined).
3. **PPC #4 tail bound is count-pinned** — the count → letter-mass scale transfer
   surfaces as a minor caveat, expected (BUILD-NOTES §3.4/§3.5).
4. **No brms shadow + no standalone H3c** for H9 (BUILD-NOTES §3.2/§3.3) — the
   confirmatory H9 is the cross-sectional NBR; the PPC Moran's I (#10) is the
   spatial check carried.

---

## 6. Outputs

`outputs/h9-results.json` (every number above — primary Latin, standardised +
interpretive sensitivities, empire secondary; seed 20260618; source for all
numbers here); `outputs/h9-posterior-summary-latin.csv`; `outputs/ppc-results.json`
(the 10-check suite); `outputs/prior-predictive-thresholds.json`;
`outputs/sample-counts.json`; `run.log` (the full run trace). Posteriors
(`*.nc`) are gitignored, regenerable from seed + code.
Cross-refs: BUILD-NOTES.md (build-decision record); Amendment 01 §A5.1/§A5.2
(measure + scope); Amendment 02 (Latin primary frame);
`runs/2026-06-04-h3a-confirmatory/` (the inscription-count H3a twin); Obs 109
(the H9 register entry).
