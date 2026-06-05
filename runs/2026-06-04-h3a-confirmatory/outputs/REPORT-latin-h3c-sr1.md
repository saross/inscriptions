# Latin-frame H3c + SR1 — REPORT (preliminary, pending OSF Amendment 02)

**Status:** PRELIMINARY — pending **OSF Amendment 02**. Under Decision 36 the
Latin-speaking-provinces frame is the new first-class hypothesis-testing frame,
and it is **amendment-gated**: no Latin-primary confirmatory claim leaves the
repository until Amendment 02 is lodged. Nothing here is "final".

**Run:** `runs/2026-06-04-h3a-confirmatory/` · branch `main` · compute host
`sapphire` · LIRE v3.0 · date window 50 BC – AD 350 (overlap).

**Scope.** This is the Decision-36 consequence that finalises the
cross-sectional track under the new primary frame: the Latin-frame counterparts
of **H3c** (residual spatial autocorrelation) and **SR1** (OLS log-log Hanson
comparator). It is a **no-re-fit extension** — the Latin H3a posterior already
exists (`idata-latin.nc`, the blind-run Sensitivity B fit), so nothing was
re-sampled. The methodology mirrors the empire-frame run exactly
(`code/04-h3c.py` for H3c; `code/02-h3a-fit.py::ols_loglog` for SR1); the only
changes are the input frame (Latin, 817 cities) and the input posterior
(Latin). Code: `code/05-h3c-sr1-latin.py`.

**Realised counts:** **817 cities / 39 provinces** (matches Decision 36's frame
definition exactly; hard-stop check for n = 817 passed). Latin date-window
inscription total: 72,006.

**Coordinates — no recomputation needed.** The Latin frame
(`data/processed/city_level_for_h3a_latin.parquet`) already carries per-city
`longitude`/`latitude` (817 non-null each). These are the **median** Longitude
and Latitude per `urban_context_city`, inherited unchanged from the primary
frame by `h3a_common.build_latin_frame` — verified identical to the primary
frame's coordinates for all 817 cities (max |Δ| = 0.0 in both axes). This is
the same median-coordinate choice the empire H3c used, so the empire's
coordinate methodology is preserved with no recomputation.

---

## 1. SR1 (Latin) — OLS log-log Hanson comparator

Unweighted OLS of `log(inscription_count)` on `log(urban_context_pop_est)`
across the 817 Latin cities — identical method to `02-h3a-fit.py::ols_loglog`.

| Quantity | Value |
|---|---|
| **Slope (β)** | **0.5047** |
| Standard error | 0.0544 |
| 95% CI | **[0.398, 0.611]** |
| R² | 0.0956 |
| Intercept | −0.905 |
| n | 817 |

**Contrast.**

| Comparator | β | Latin − comparator |
|---|---|---|
| **Latin frame (this result)** | **0.5047** | — |
| Hanson 2021 | 0.672 | −0.167 |
| Empire frame (this run, 1,044 cities) | 0.284 | +0.221 |

The Latin-frame pooled per-city population–count scaling exponent (0.505) sits
**roughly midway between the empire-frame OLS (0.284) and Hanson's β = 0.672**,
and its 95% CI [0.398, 0.611] excludes Hanson's 0.672 (Hanson sits 1.2 SE above
the upper bound). Restricting to the well-covered Latin provinces nearly doubles
the empire-frame slope and brings it materially closer to Hanson's super-linear
urban-scaling exponent — consistent with Decision 36's coverage rationale (the
empire-wide slope is depressed by the non-representative Latin slice of
Greek-province epigraphy). The OLS fit remains weak (R² 0.096, up from the
empire's 0.036), which is exactly why the preregistered confirmatory
specification is the within-between (Mundlak) decomposition, not a pooled OLS.

For reference, the Latin H3a result this SR1 accompanies (blind-run
Sensitivity B, from `h3a-results.json`): `f_within` 0.480 [0.401, 0.566]
(SUPPORTED), β_within 0.733 [0.648, 0.820]; convergence max R̂ 1.00, min
ESS-bulk 2,038, 0 divergences.

---

## 2. H3c (Latin) — residual spatial autocorrelation

**Confirmatory rule:** Moran's I > 0 at p < 0.05 in ≥ 2 of {k = 5, 8, 10}, on
the posterior-mean Pearson residual vector, k-NN row-standardised weights
(libpysal), 999-permutation conditional inference (esda, one-sided greater).
Pearson residual: `r_c = (y_c − μ_c)/sqrt(μ_c + μ_c²/φ)` per posterior draw,
from the Latin posterior; the permutation test runs on the **posterior-mean**
residual, and the posterior distribution of I_s is reported across 2,000 draws.

| k | Moran's I (posterior-mean resid) | p_sim (one-sided) | z | rule pass? | posterior I [2.5 / 50 / 97.5%] | frac > 0 |
|---|---|---|---|---|---|---|
| 5 | +0.0225 | 0.130 | +1.15 | no | [+0.0226, +0.0367, +0.0536] | 1.000 |
| **8 (primary)** | **+0.0123** | **0.184** | **+0.85** | **no** | **[+0.0140, +0.0254, +0.0397]** | **1.000** |
| 10 | +0.0092 | 0.239 | +0.67 | no | [+0.0109, +0.0220, +0.0358] | 1.000 |

**Verdict: NOT-SUPPORTED** (0/3 k-values pass). The Latin Mundlak model's
residuals show **no significant spatial autocorrelation**: the posterior-mean
residual Moran's I is small and positive at all three k but never
permutation-significant (smallest p_sim = 0.130 at k = 5). This is a **clean
non-replication** of Hanson 2021 (Table 7.4: residual Moran's I = 0.046,
z = 4.571, p < 0.0001). The §3 k = 8 three-case interpretive guardrail does not
engage — it applies only when the confirmatory rule passes.

**Caveat on the posterior-I distribution.** As in the empire frame, the
posterior distribution of I_s is **wholly above zero** at every k
(frac > 0 = 1.000; 95% intervals entirely positive). This does **not** rescue a
replication claim. The magnitudes are small (posterior median I ≤ 0.037, below
Hanson's 0.046), and — decisively — the **permutation test on the posterior-mean
residual is not significant at any k**, which is the quantity the confirmatory
rule binds on. The positive posterior-I mass reflects that individual-draw
residual vectors are noisier than the denoised posterior mean, inflating their
apparent autocorrelation slightly; it is not substantive spatial structure. Per
the prereg's reporting discipline, H3c is reported as **not supported** rather
than as any grade of Hanson replication.

---

## 3. Comparison to the empire frame

| Quantity | Empire frame (1,044) | Latin frame (817) |
|---|---|---|
| **SR1 OLS log-log slope** | 0.284 (SE 0.045; CI [0.195, 0.373]); R² 0.036 | **0.505 (SE 0.054; CI [0.398, 0.611]); R² 0.096** |
| SR1 vs Hanson 0.672 | well below | below, but ~3× closer in gap |
| **H3c verdict** | NOT-SUPPORTED (0/3) | **NOT-SUPPORTED (0/3)** |
| H3c Moran's I @ k=5 / 8 / 10 (post-mean) | +0.010 / −0.002 / −0.004 | +0.022 / +0.012 / +0.009 |
| H3c smallest p_sim | 0.249 (k=5) | 0.130 (k=5) |
| H3c posterior-I frac > 0 (k=5/8/10) | 1.000 / 0.985 / 0.946 | 1.000 / 1.000 / 1.000 |

**Reading.** The two frames tell the same qualitative story for **both**
cross-sectional secondary results, so the confirmatory conclusions are robust to
the Decision-36 reframing:

- **SR1:** the Latin slope is markedly steeper than the empire slope (0.505 vs
  0.284) and closer to Hanson's 0.672 — restricting to well-covered Latin
  provinces recovers a stronger, more Hanson-like population–count scaling, as
  the coverage rationale predicts — but it still falls below Hanson and the OLS
  fit stays weak, reinforcing the Mundlak decomposition as the confirmatory
  specification.
- **H3c:** **not-supported in both frames** — a clean non-replication of Hanson's
  significant residual Moran's I. The Latin residual Moran's I point estimates
  are slightly larger and uniformly positive (and the smallest p_sim falls from
  0.25 to 0.13), but no k reaches the p < 0.05 permutation threshold, so the
  verdict is unchanged. The Latin posterior-I distribution is wholly positive at
  all three k (vs the empire's 0.985/0.946 at k = 8/10), a mild strengthening
  that is still well short of substantive, permutation-significant spatial
  structure.

---

## 4. Files and reproduction

- **Code:** `runs/2026-06-04-h3a-confirmatory/code/05-h3c-sr1-latin.py`
  (H3c block mirrors `04-h3c.py`; SR1 block mirrors
  `02-h3a-fit.py::ols_loglog`).
- **Inputs:** `data/processed/city_level_for_h3a_latin.parquet` (tracked, 817
  cities); `runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc` (Latin
  posterior, on sapphire, gitignored — regenerable from `02-h3a-fit.py`).
- **Results:** `runs/2026-06-04-h3a-confirmatory/outputs/{h3c-latin-results.json,
  sr1-latin-results.json}`.
- **Compute:** run on `sapphire` via `~/Code/inscriptions/.venv/bin/python3`
  (libpysal 4.14.1, esda 2.9.0), `TMPDIR=~/cc-scratch/h3a-latin/pytensor-tmp`.
  Locally reproduced identically (same venv versions); the only between-host
  difference is the unseeded 999-permutation p_sim (Monte-Carlo noise: e.g.
  k = 5 p_sim 0.111 local vs 0.130 sapphire — matching `04-h3c.py`, which also
  does not seed the permutation null). All point estimates, posterior-I
  intervals, R², and the verdict are identical across hosts.

**Label:** all results above are **preliminary — pending OSF Amendment 02**
(Decision 36 amendment-gate; the Latin frame is the new primary and is
amendment-gated).
