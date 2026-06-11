# Cross-classified arm — PILOT report (3-arm p_conv decision gate)

Pilot cells with any arm results: 20. Per-arm scorable: tiers3 20, library 20, free 20. Fully-failed (excluded): tiers3 0, library 0, free 0.

## Regime summary (mean over cells; aggregates over converged reps)

| arm | regime | n | mean med-bias | mean \|bias\| | coverage | conv |
|---|---|---|---|---|---|---|
| **lead (ref)** | identifiable | 12 | +0.064 | 0.064 | 0.319 | 0.917 |
| tiers3 | identifiable | 12 | -0.002 | 0.031 | 0.321 | 1.000 |
| library | identifiable | 12 | +0.006 | 0.011 | 0.562 | 0.996 |
| free | identifiable | 12 | -0.013 | 0.017 | 0.620 | 0.979 |
| **lead (ref)** | confounded | 8 | +0.081 | 0.081 | 0.320 | 0.938 |
| tiers3 | confounded | 8 | -0.400 | 0.401 | 0.000 | 1.000 |
| library | confounded | 8 | +0.010 | 0.012 | 0.725 | 1.000 |
| free | confounded | 8 | -0.031 | 0.045 | 0.661 | 0.981 |

## Coverage breakdown — boundary artefact (α_true = 0 cells cannot be covered by an equal-tailed CI)

| arm | coverage (α = 0 cells) | coverage (α > 0 cells) |
|---|---|---|
| lead | 0.000 (n=6) | 0.456 (n=14) |
| tiers3 | 0.000 (n=6) | 0.275 (n=14) |
| library | 0.000 (n=6) | 0.896 (n=14) |
| free | 0.000 (n=6) | 0.910 (n=14) |

## Per-cell α median-bias (cc arms vs lead)

| cell | regime | α | lead | tiers3 | library | free |
|---|---|---|---|---|---|---|
| broad_a0.0_gauss_early_N2800 | identifiable | 0.0 | +0.079 | +0.002 | +0.002 | +0.004 |
| broad_a0.0_gauss_inwin_N2800 | identifiable | 0.0 | +0.081 | +0.001 | +0.002 | +0.002 |
| broad_a0.4_gauss_early_N2800 | identifiable | 0.4 | +0.064 | -0.057 | -0.026 | -0.044 |
| broad_a0.4_gauss_inwin_N2800 | identifiable | 0.4 | +0.073 | -0.008 | +0.016 | -0.116 |
| broad_a0.8_gauss_early_N2800 | identifiable | 0.8 | +0.058 | -0.107 | -0.006 | -0.002 |
| broad_a0.8_gauss_inwin_N2800 | identifiable | 0.8 | +0.049 | -0.024 | +0.005 | -0.015 |
| conc_a0.0_gauss_early_N2800 | identifiable | 0.0 | +0.078 | +0.002 | +0.002 | +0.004 |
| conc_a0.0_gauss_inwin_N2800 | confounded | 0.0 | +0.079 | +0.001 | +0.002 | +0.002 |
| conc_a0.4_gauss_early_N2800 | identifiable | 0.4 | +0.074 | +0.068 | +0.026 | -0.002 |
| conc_a0.4_gauss_inwin_N2800 | confounded | 0.4 | +0.095 | -0.269 | +0.008 | -0.170 |
| conc_a0.4_regnal_N2800 | confounded | 0.4 | +0.035 | -0.139 | +0.000 | +0.002 |
| conc_a0.8_gauss_early_N2800 | identifiable | 0.8 | +0.032 | +0.020 | +0.005 | -0.002 |
| conc_a0.8_gauss_inwin_N2800 | confounded | 0.8 | +0.097 | -0.798 | +0.020 | +0.017 |
| stress_a0.0_gauss_early_N2800 | identifiable | 0.0 | +0.079 | +0.002 | +0.002 | +0.003 |
| stress_a0.0_gauss_inwin_N2800 | confounded | 0.0 | +0.078 | +0.001 | +0.002 | +0.003 |
| stress_a0.4_gauss_early_N2800 | identifiable | 0.4 | +0.067 | +0.063 | +0.031 | +0.012 |
| stress_a0.4_gauss_inwin_N2800 | confounded | 0.4 | +0.115 | -0.399 | +0.023 | -0.125 |
| stress_a0.8_gauss_early_N2800 | identifiable | 0.8 | +0.032 | +0.014 | +0.010 | +0.000 |
| stress_a0.8_gauss_inwin_N2800 | confounded | 0.8 | +0.110 | -0.799 | +0.033 | +0.032 |
| stress_a0.8_regnal_N2800 | confounded | 0.8 | +0.040 | -0.798 | -0.007 | -0.006 |

## Timing (per-fit seconds, per arm)

- tiers3: mean 27.0 s/fit (max 32.8) → full 300×100 @ n_jobs=12 ≈ **18.7 h**
- library: mean 60.4 s/fit (max 94.9) → full 300×100 @ n_jobs=12 ≈ **41.9 h**
- free: mean 36.8 s/fit (max 48.3) → full 300×100 @ n_jobs=12 ≈ **25.5 h**

Decision criteria, in order (signoff §5): confounded bias profile; identifiable bias flatness; coverage; convergence. Ties → `library`.
