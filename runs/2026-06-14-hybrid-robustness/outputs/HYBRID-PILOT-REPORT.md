# Hybrid robustness — PILOT report (global-θ cross-classified, one joint fit)

Joint fit over 29 units in 7.9 min (draws 2000, tune 3000, target_accept 0.97).

- **All-blocks** sampler: max R̂ 1.0470, min bulk-ESS 73, 0 divergences → MARGINAL (incl. collinear tier_weights).
- **α + θ (inference-relevant) block**: max R̂ 1.0470, min bulk-ESS 73 → **MARGINAL** — this is the block the concordance test depends on.

## Global θ (estimated, wide prior) vs the lead's calibrated values
- θ_conv 0.933 [0.923, 0.943] (calibrated 0.945)
- θ_gen 0.024 [0.017, 0.030] (calibrated 0.155)
- θ sane vs calibration: **False**

## Concordance preview (cross-classified α vs hybrid α)
- cc median inside hybrid 95% CI: **9/29** (31%)
- mean discrepancy (hybrid − cc): **-0.002** (concordant if |mean| < 0.05)
- max |discrepancy|: 0.131

## Per-unit (sorted by |discrepancy|)
| unit | cc α | hybrid α [95% CI] | in CI | Δ |
|---|---|---|---|---|
| Etruria / Regio VII | 0.812 | 0.681 [0.658, 0.703] | NO | -0.131 |
| Latium et Campania / Regio I | 0.595 | 0.489 [0.479, 0.500] | NO | -0.106 |
| Italia (excl. Rome) | 0.779 | 0.678 [0.669, 0.688] | NO | -0.101 |
| latin-aggregate | 0.726 | 0.648 [0.640, 0.656] | NO | -0.078 |
| Venetia et Histria / Regio X | 0.844 | 0.902 [0.889, 0.915] | NO | +0.058 |
| Umbria / Regio VI | 0.738 | 0.792 [0.772, 0.813] | NO | +0.054 |
| Germania superior | 0.481 | 0.428 [0.412, 0.444] | NO | -0.053 |
| Pannonia inferior | 0.630 | 0.683 [0.662, 0.703] | NO | +0.053 |
| Baetica | 0.624 | 0.671 [0.648, 0.694] | NO | +0.047 |
| Noricum | 0.784 | 0.822 [0.802, 0.841] | NO | +0.038 |
| Samnium / Regio IV | 0.840 | 0.878 [0.861, 0.894] | NO | +0.038 |
| empire-aggregate | 0.671 | 0.703 [0.695, 0.711] | NO | +0.032 |
| Aquileia | 0.915 | 0.946 [0.928, 0.963] | NO | +0.032 |
| Ostia | 0.650 | 0.681 [0.659, 0.703] | NO | +0.031 |
| Salona | 0.987 | 0.957 [0.940, 0.974] | NO | -0.030 |
| Germania inferior | 0.730 | 0.757 [0.739, 0.775] | NO | +0.027 |
| Apulia et Calabria / Regio II | 0.741 | 0.715 [0.695, 0.734] | NO | -0.026 |
| Moesia inferior | 0.626 | 0.651 [0.624, 0.677] | yes | +0.025 |
| Numidia | 0.546 | 0.568 [0.546, 0.589] | NO | +0.021 |
| Lusitania | 0.757 | 0.776 [0.749, 0.801] | yes | +0.019 |
| Dalmatia | 0.913 | 0.894 [0.880, 0.908] | NO | -0.019 |
| Pompeii | 0.015 | 0.024 [0.016, 0.035] | NO | +0.010 |
| Pannonia superior | 0.734 | 0.742 [0.724, 0.759] | yes | +0.008 |
| Transpadana / Regio XI | 0.892 | 0.885 [0.865, 0.906] | yes | -0.007 |
| Britannia | 0.400 | 0.395 [0.378, 0.412] | yes | -0.005 |
| Africa proconsularis | 0.630 | 0.634 [0.614, 0.655] | yes | +0.005 |
| Dacia | 0.157 | 0.160 [0.147, 0.173] | yes | +0.003 |
| Mogontiacum | 0.139 | 0.137 [0.121, 0.153] | yes | -0.002 |
| Hispania citerior | 0.743 | 0.741 [0.726, 0.756] | yes | -0.002 |

## Gate to advance to hierarchical validation: **REVIEW** (α+θ block healthy AND ≥50% cc-medians inside hybrid CIs)
- θ_gen estimated 0.024 vs calibrated 0.155: a MATERIAL divergence — the hybrid's distinctive signal (interpret only once α+θ converge).
