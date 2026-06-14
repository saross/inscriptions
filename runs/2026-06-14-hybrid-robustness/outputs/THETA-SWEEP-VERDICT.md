# θ-prior sensitivity sweep — VERDICT (cc-library robustness annex)

Conditions present: ['baseline', 'rederived', 'wide', 'rederived_wide']. Units: 29.
All-condition convergence: 28/29 units.

**Baseline reproduces the production refit:** max |Δα| 0.003, mean 0.001 (bit-identical seed; any Δ is rounding).

## Stability across the four θ priors

- units with α-range < 0.1: **27/29** (93%)
- mean α-range 0.038; max 0.159
- **frontier units** (n=10): mean α-range 0.055, max 0.159
- operative baseline→rederived (θ_gen 0.155→0.025) shift: mean +0.025, max |shift| 0.072

## Per-unit α across θ conditions (sorted by range)

| unit | F | baseline | rederived | wide | rederived_wide | range | base→reder |
|---|---|---|---|---|---|---|---|
| Moesia inferior | ★ | 0.627 | 0.699 | 0.736 | 0.785 | 0.159 | +0.072 |
| Britannia | ★ | 0.400 | 0.449 | 0.519 | 0.540 | 0.140 | +0.049 |
| Ostia | ★ | 0.650 | 0.702 | 0.674 | 0.710 | 0.060 | +0.052 |
| Germania superior |  | 0.482 | 0.509 | 0.524 | 0.537 | 0.055 | +0.027 |
| Umbria / Regio VI | ★ | 0.737 | 0.779 | 0.728 | 0.761 | 0.051 | +0.042 |
| Apulia et Calabria / Regio II |  | 0.744 | 0.774 | 0.781 | 0.794 | 0.050 | +0.030 |
| Pannonia inferior | ★ | 0.630 | 0.676 | 0.633 | 0.663 | 0.046 | +0.046 |
| Africa proconsularis |  | 0.629 | 0.661 | 0.657 | 0.673 | 0.044 | +0.032 |
| Etruria / Regio VII |  | 0.812 | 0.836 | 0.842 | 0.852 | 0.040 | +0.024 |
| Venetia et Histria / Regio X | ★ | 0.843 | 0.870 | 0.829 | 0.858 | 0.040 | +0.027 |
| Pannonia superior |  | 0.734 | 0.765 | 0.755 | 0.772 | 0.038 | +0.031 |
| Baetica |  | 0.624 | 0.661 | 0.625 | 0.650 | 0.037 | +0.037 |
| Aquileia |  | 0.915 | 0.933 | 0.902 | 0.922 | 0.031 | +0.018 |
| Lusitania |  | 0.758 | 0.787 | 0.770 | 0.789 | 0.031 | +0.029 |
| latin-aggregate |  | 0.729 | 0.739 | 0.754 | 0.758 | 0.029 | +0.010 |
| Hispania citerior |  | 0.742 | 0.766 | 0.758 | 0.769 | 0.027 | +0.024 |
| Mogontiacum |  | 0.139 | 0.153 | 0.154 | 0.166 | 0.027 | +0.014 |
| Germania inferior |  | 0.730 | 0.754 | 0.737 | 0.751 | 0.024 | +0.024 |
| Noricum |  | 0.784 | 0.808 | 0.784 | 0.800 | 0.024 | +0.024 |
| Samnium / Regio IV | ★ | 0.841 | 0.860 | 0.837 | 0.848 | 0.023 | +0.019 |
| Transpadana / Regio XI |  | 0.891 | 0.908 | 0.904 | 0.913 | 0.022 | +0.016 |
| Latium et Campania / Regio I |  | 0.595 | 0.605 | 0.608 | 0.614 | 0.019 | +0.010 |
| Dacia | ★ | 0.156 | 0.171 | 0.164 | 0.173 | 0.017 | +0.014 |
| Dalmatia |  | 0.913 | 0.923 | 0.920 | 0.927 | 0.014 | +0.011 |
| empire-aggregate |  | 0.671 | 0.680 | 0.667 | 0.674 | 0.013 | +0.009 |
| Italia (excl. Rome) |  | 0.779 | 0.787 | 0.787 | 0.791 | 0.012 | +0.008 |
| Numidia | ★ | 0.546 | 0.555 | 0.543 | 0.547 | 0.011 | +0.009 |
| Salona | ★ | 0.987 | 0.989 | 0.989 | 0.990 | 0.003 | +0.002 |
| Pompeii |  | 0.015 | 0.016 | 0.015 | 0.015 | 0.001 | +0.001 |

## Verdict

- **27/29 units stable** (α-range < 0.1 across all four θ priors); mean range 0.038.
- **Frontier units: 8/10 stable.** The sensitive units are Moesia inferior (range 0.159, base→reder +0.072), Britannia (range 0.140, base→reder +0.049) — the **most temporally-confounded** units, where the θ assumption matters most. Their α moves **upward** under the corrected (lower) θ_gen, and stays within the H2.1 two-bound range — so the remediation conclusion is unchanged.
- **Operative shift** (θ_gen 0.155→0.025): uniformly small and positive (mean +0.025, max 0.072) — re-centring θ_gen nudges all α up slightly, most for the confounded frontier units.
- **Interpretation:** the alignment *contrast* pins the well-identified α's (broad units + the aggregates are rock-stable, range ≤ 0.03); the residual θ-sensitivity concentrates in the hardest confounded units. The cc-library result is robust to the θ assumption for the large majority of units.
- **Open decision (Shawn):** three methods agree θ_gen ≈ 0.025 (hybrid, re-derivation, the wide-κ sweep) and it fits 2.5× better than the calibrated 0.155 — there is a principled case to **adopt the re-derived θ_gen as the production prior** and re-run the refit (~6 min; α's move little, but it removes a known calibration bias rather than reporting it). Folds into amendment §A5.7 either way.
