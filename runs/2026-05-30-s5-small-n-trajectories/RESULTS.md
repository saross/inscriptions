# §5 Layer-A small-N city-trajectory estimation — production results

- **Status:** COMPLETE (exploratory; Layer A only — Layer B β-inversion deferred
  pending H3a `β_within`).
- **Run:** launched 2026-05-31 23:00 (zbook-local); Steps 1–2 finished 04:43
  (~5.7 h); Step 3 diagnostics finished 2026-06-01 17:21 (via
  `finish_diagnostics.py` after the `scikit-learn`-missing crash was fixed —
  no monolithic re-fitting).
- **Host:** zbook (16 cores), pymc 6.0.1, pinned scales `s_g=0.3, s_u=0.15,
  s_v=0.15`, `target_accept=0.99`, seed 2026.
- **Outputs:** `code/production/` — four `*.nc` posteriors (3.6 GB total, on
  zbook only, gitignored), `production-summary.json`,
  `subsample-recover-results.json`, `subsample-recover.png`.

---

## 1. The four monolithic fits (268 target cities + 45 provinces)

| Fit | Gate | max R̂ | min ESS | div | wall |
|---|---|---|---|---|---|
| **inscription-25y (primary)** | **PASS** | 1.0000 | 2571 | 0 | 5.0 h |
| inscription-50y | marginal | 1.0100 | 948 | 0 | 2.0 h |
| letter-25y | marginal | 1.0100 | 486 | 0 | 17 min |
| letter-50y | marginal | 1.0100 | 938 | 0 | 6 min |

The **primary fit passed cleanly**. The other three sit exactly on the strict
`R̂ < 1.01` boundary (R̂ = 1.0100) even after one escalation to 2× draws/tune,
with healthy ESS (all > 400) and **zero divergences**. **Accepted with a
documented caveat** (Shawn, 2026-06-01): for an exploratory Layer-A analysis,
R̂ = 1.0100 / ESS > 400 / 0 divergences is essentially converged, not a real
problem.

## 2. Calibration — subsample-and-recover (§8a.3; 7 donors × N × ~40 reps = 1400 fits, 0 failures)

| N | coverage | shape r | mean CI width | \|peak bias\| (bins) |
|---|---|---|---|---|
| 50 | 0.78 | 0.77 | 0.117 | 1.18 |
| 100 | 0.82 | 0.82 | 0.097 | 1.05 |
| 200 | 0.91 | 0.89 | 0.081 | 0.77 |
| 300 | 0.94 | 0.92 | 0.072 | 0.64 |
| 500 | 0.97 | 0.96 | 0.063 | 0.41 |

**Calibration N\* = 300** (the smallest N with coverage ≥ 0.90 **and** shape
r ≥ 0.90). The headline methodological result: **below ~300 inscriptions the
small-N trajectories are not reliable; at/above 300 the recovery is honest**
(well-calibrated coverage, faithful shape, modest peak bias). This quantifies
the preregistered honest-negative-result and is the "where does it work?"
deliverable.

## 3. Validation

**Pompeii AD-79 external check (§8a.2).** Pompeii (N = 4266, buried AD 79):
genuinely-post-79 mass (bins ≥ AD 100) = **5.0 of 4262 = 0.12 %** — essentially
zero, exactly as the historical terminus requires. The model independently
reproduces the eruption from the data; the strongest external validation
available.

**Anchor internal consistency (§8a.1).** Each large anchor's standalone
Bayesian trajectory vs its own model-free aoristic SPA (Pearson r on shape):

| Anchor | N | shape r | standalone gate |
|---|---|---|---|
| Mogontiacum | 2328 | 0.890 | pass |
| Ostia | 2380 | 0.885 | marginal |
| Pompeii | 4266 | 0.826 | pass |
| Carnuntum (1) | 1574 | 0.818 | pass |
| Aquileia | 2023 | 0.809 | pass |
| Puteoli | 1723 | 0.739 | pass |
| Salona | 3452 | 0.688 | marginal |

The Bayesian trajectories track the raw aoristic SPAs (r ≈ 0.69–0.89, median
~0.82) — the smoothing + pooling do not grossly distort data-rich cities.
**Salona (r = 0.69) is the weakest** and worth a look in any write-up.

## 4. Trajectory clustering (exploratory)

The 268 target-city posterior-median trajectories cluster (k-means, k = 6) into
six shape-groups; sizes **39 / 24 / 67 / 71 / 43 / 24**, medoids **Dyrrachium,
Naissus, Interamna Lirenas, Parma, Siscia, Falerii Novi**. A descriptive map of
the distinct small-N epigraphic-trajectory shapes across the empire.

## 5. Caveats and follow-ups

- Three monolithic fits at the R̂ = 1.0100 convergence boundary (accepted,
  exploratory).
- Salona internal-consistency r = 0.69 (weakest anchor).
- The four `.nc` posteriors (3.6 GB) live **only on zbook** (single copy;
  regenerable in ~5.7 h via `orchestrate.py --confirm-production`). They are the
  input to Layer B — preserve them until Layer B runs, or back them up
  off-zbook.
- **Layer B** (β-inversion to time-varying population) remains deferred pending
  H3a `β_within`.
- A late-crash post-mortem (missing `scikit-learn`) drives the dependency-hygiene
  follow-up (task #9): refresh `uv.lock` to the current stack, `uv sync`
  provisioning, a pre-flight import check, and a `--resume-diagnostics` flag.
