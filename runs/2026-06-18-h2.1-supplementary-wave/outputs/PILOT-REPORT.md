# H2.1 supplementary wave — PILOT report

- Generated (UTC): 2026-06-18T08:47:29+00:00
- Spec: runs/2026-06-18-h2.1-supplementary-wave/SPEC.md §9
- Seed: 20260618
- Sampling: 4 chains × (1000 tune + 2000 draws), cores=1, target_accept=0.95

## 1. DM + NB model comparison (two pilot units)

| unit | family | α median | α 95% CI | conv | secs | κ / φ |
|------|--------|----------|----------|------|------|-------|
| empire-aggregate | primary | 0.6805 | [0.6653, 0.6975] | FAIL | 288.0 |  |
| empire-aggregate | dm | 0.6806 | [0.6563, 0.7073] | ok | 188.9 | κ=5770.5 |
| empire-aggregate | nb | 0.6804 | [0.6648, 0.6969] | FAIL | 384.6 | φ=5635.2 |
| Latium et Campania / Regio I | primary | 0.6054 | [0.5688, 0.6324] | ok | 79.1 |  |
| Latium et Campania / Regio I | dm | 0.6175 | [0.5654, 0.6547] | ok | 66.8 | κ=5224.7 |
| Latium et Campania / Regio I | nb | 0.6052 | [0.5685, 0.6319] | ok | 106.2 | φ=4267.0 |

### Primary multinomial PPC dispersion (DM trigger, SPEC §4)

- **empire-aggregate**: dispersion ratio aligned=1.159, non-aligned=1.031 (≈1 multinomial-adequate; >1 over-dispersed (DM-preferring)).
- **Latium et Campania / Regio I**: dispersion ratio aligned=0.299, non-aligned=0.844 (≈1 multinomial-adequate; >1 over-dispersed (DM-preferring)).

## 2. κ-tuning (prior-predictive)

- **Chosen S_KAPPA = 3000**
- Rationale: S_KAPPA chosen to maximise prior mass across κ ∈ ~[10, 1e4] (weakly informative, data-dominated; does not force overdispersion). Cross-checked against the empire DM κ posterior above — if the κ posterior sits well inside the prior bulk, the prior is data-dominated as required (SPEC §3.3). Re-confirm on the figure before sign-off.

| S_KAPPA | frac in [10, 1e4] | κ quantiles (5/25/50/75/95) |
|---------|-------------------|------------------------------|
| 100 | 0.919 | 6 / 32 / 67 / 115 / 199 |
| 300 | 0.973 | 18 / 95 / 202 / 347 / 589 |
| 1000 | 0.992 | 62 / 316 / 669 / 1157 / 1958 |
| 3000 | 0.997 | 188 / 953 / 2006 / 3441 / 5835 |
| 10000 | 0.686 | 622 / 3123 / 6653 / 11444 / 19602 |

## 3. Aoristic-MC PILOT SUBSAMPLE (empire only)

- **PILOT N_MC = 10** (NOT production N_MC = 30).
- Unit: empire-aggregate; k_cc=120632, n_rows=180609.
- Cross-realisation 95% α band: [0.0907, 0.1463] (width 0.0556).
- Primary single-SPA 95% CI width: 0.032249154021182114.
- **Divergence flag: True** (cross-realisation 95% α-range > 1.5× primary 95% CI width).
- Mean wall per realisation: 275.0 s.

### Whole-wave cost projection (SPEC §8)

- Aoristic-MC (N_MC=30 × 29 units): ~66.45 core-hr.
- Whole wave (aoristic-MC ≈ 80%): ~83.07 core-hr.
- Projected wall at n_jobs=10: ~8.31 h (SPEC §8 budget: 20 core-hr / 3–5 h wall).

> **HALT AND REPORT (SPEC §8):** projected wall ~8.31 h exceeds the ~8.0 h ceiling. Do NOT silently reduce N_MC / draws / chains / unit count — Shawn decides (accept the longer run, stage it, or trim scope).

## Sign-off checklist (SPEC §9)

- [ ] Smoke gates pass (`smoke_supp.py`).
- [ ] κ choice (above) — prior data-dominated, κ posterior inside bulk.
- [ ] Measured cost vs the SPEC §8 budget (above).
- [ ] No convergence surprises across the pilot fits.

