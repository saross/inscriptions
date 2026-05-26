# RUN-LOG-06 --- Block 6 Bayesian Mundlak (three variants)
Date: 2026-05-26  
Script: `runs/2026-05-26-letter-count-probe/code/06-h3a-bayesian-mundlak-letter.py`  
Total wall-clock: **255.2 s** (4.3 min)

## Per-variant results

| variant | n_cities | f_within median | 95 % CI | P(f>0.10) | P(f>0.20) | beta_within median | beta_between median | max R-hat | min ESS_bulk | divergences | wall (s) | gate-pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| inscription | 1,044 | 0.2994 | [0.2370, 0.3663] | 1.0000 | 0.9994 | +0.5871 | -0.2476 | 1.0000 | 1041 | 0 | 95.9 | PASS |
| letter_cons | 1,044 | 0.3983 | [0.3204, 0.4817] | 1.0000 | 1.0000 | +0.5588 | -0.1577 | 1.0000 | 1943 | 0 | 78.7 | PASS |
| letter_intr | 1,044 | 0.3983 | [0.3197, 0.4830] | 1.0000 | 1.0000 | +0.5587 | -0.1699 | 1.0000 | 1489 | 0 | 79.8 | PASS |

## Verdict flag 3 (within-province variance partition)

Baseline (inscription-count variant): f_within median = 0.2994 (29.94 %)

- **letter total (conservative)**: f_within median = 0.3983 (39.83 %); shift = +9.89 pp; **FLAG-3 MATERIAL** (NO-CHANGE < 2 pp; MODEST 2--5 pp; MATERIAL > 5 pp)
- **letter total (interpretive)**: f_within median = 0.3983 (39.83 %); shift = +9.88 pp; **FLAG-3 MATERIAL** (NO-CHANGE < 2 pp; MODEST 2--5 pp; MATERIAL > 5 pp)

## Sampler settings

- N_WARMUP = 3000, N_SAMPLE = 2000, N_CHAINS = 4
- target_accept = 0.95
- random_seed = 20260526
- gates: R-hat < 1.01; ESS_bulk >= 400; divergences <= 0

## Talk-prep cross-reference

The talk-prep run (`runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv`) reported f_within median = 0.2995 (95 % CI [0.2403, 0.3664]) for the inscription-count variant, on the same 1,044 Hanson-Rome-excluded cities, with seed 20,260,521. The current run uses seed 20,260,526 (today's date) so a tight reproduction of that number for the inscription_count variant indicates the model + data + sampler are consistent.
