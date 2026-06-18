# C10 aoristic-MC validity test — VALIDITY REPORT

Generated: 2026-06-18 15:58:45

## Verdict (SPEC §3b decision rule)

**(a) SUPPORTED — point-date aoristic-MC tracks planted alpha; C10 stands**

- mass arm recovers planted α within tol (0.1): **True** (max |Δα| = 0.043)
- point-date arm tracks planted α within tol: **True** (max |Δα| = 0.046)
- point-date arm flat in true α: **False** (spread 0.523, slope 1.053)
- point-date α near pilot floor (~0.1): **False**

## 1b — ground-truth recovery (synthetic)

p_gen = empire-posterior-median; N_synth = 3000; N_MC = 10; seeds = 3.

| planted α | seed | realised α | mass α (med [CI]) | point-date α (med [CI]) |
|---|---|---|---|---|
| 0.30 | 0 | 0.308 | 0.313 [0.271, 0.354] | 0.315 [0.270, 0.355] |
| 0.30 | 1 | 0.315 | 0.323 [0.283, 0.365] | 0.321 [0.275, 0.363] |
| 0.30 | 2 | 0.286 | 0.292 [0.251, 0.333] | 0.291 [0.247, 0.331] |
| 0.50 | 0 | 0.502 | 0.516 [0.475, 0.564] | 0.515 [0.462, 0.563] |
| 0.50 | 1 | 0.510 | 0.529 [0.481, 0.586] | 0.529 [0.476, 0.586] |
| 0.50 | 2 | 0.492 | 0.514 [0.466, 0.579] | 0.513 [0.465, 0.576] |
| 0.68 | 0 | 0.678 | 0.715 [0.670, 0.788] | 0.712 [0.667, 0.784] |
| 0.68 | 1 | 0.678 | 0.715 [0.670, 0.793] | 0.712 [0.667, 0.787] |
| 0.68 | 2 | 0.685 | 0.721 [0.677, 0.792] | 0.726 [0.679, 0.799] |
| 0.80 | 0 | 0.786 | 0.820 [0.781, 0.881] | 0.817 [0.781, 0.873] |
| 0.80 | 1 | 0.808 | 0.843 [0.807, 0.898] | 0.843 [0.806, 0.902] |
| 0.80 | 2 | 0.798 | 0.841 [0.798, 0.911] | 0.835 [0.796, 0.905] |

## 1a — slab-concentration diagnostic (real empire aligned subset)

Unit empire-aggregate; n_rows 180609, n_aligned 120632; 10 point-date SPAs.

| metric | aoristic-mass | point-date (mean) |
|---|---|---|
| L1 to nearest slab row | 0.336 | 0.599 |
| round-boundary mass ratio (vs uniform) | 0.965 | 0.824 |
| best-fit slab-mixture weight | 1.000 | 1.003 |

## 1c — mass-preserving vs point-collapse (real empire)

Unit empire-aggregate; N_MC 10; jitter ±1 bin(s).

| scheme | α median | 95 % CI |
|---|---|---|
| point-collapse (current C10) | 0.100 | [0.090, 0.115] |
| mass-preserving (±1 bin) | 0.615 | [0.592, 0.643] |
