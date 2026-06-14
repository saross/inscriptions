# cc-library production refit — VERDICT

Units fitted: 29. Convergence failures: **1** — ['empire-aggregate'].

## Per-unit α: cc-library vs the H2.1 two-bound diagnostic

| unit | tier | cc-α [95% CI] | H2.1 α_shared | α_perunit | implied-α | conv |
|---|---|---|---|---|---|---|
| Britannia | under-identified | 0.449 [0.386, 0.544] | 0.002 | 0.793 | 0.279 | ok |
| Dacia | confirmatory | 0.171 [0.151, 0.194] | 0.001 | 0.344 | 0.014 | ok |
| Moesia inferior | under-identified | 0.698 [0.617, 0.823] | 0.050 | 0.870 | 0.520 | ok |
| Numidia | under-identified | 0.554 [0.530, 0.581] | 0.166 | 0.515 | 0.425 | ok |
| Ostia | under-identified | 0.701 [0.641, 0.772] | 0.335 | 0.775 | 0.544 | ok |
| Pannonia inferior | under-identified | 0.676 [0.632, 0.737] | 0.147 | 0.751 | 0.566 | ok |
| Salona | under-identified | 0.989 [0.951, 1.000] | 0.538 | 0.995 | 0.945 | ok |
| Samnium / Regio IV | under-identified | 0.860 [0.828, 0.898] | 0.272 | 0.860 | 0.834 | ok |
| Umbria / Regio VI | under-identified | 0.781 [0.734, 0.833] | 0.429 | 0.700 | 0.722 | ok |
| Venetia et Histria / Regio X | under-identified | 0.870 [0.845, 0.898] | 0.452 | 0.809 | 0.853 | ok |
| Latium et Campania / Regio I | confirmatory | 0.606 [0.568, 0.632] | 0.672 | 0.621 | 0.374 | ok |
| Noricum | caveated-high-alpha | 0.808 [0.774, 0.847] | 0.880 | 0.829 | 0.736 | ok |
| Pompeii | confirmatory | 0.016 [0.010, 0.022] | 0.001 | 0.003 | 0.000 | ok |
| empire-aggregate | confirmatory | 0.680 [0.665, 0.697] | 0.672 | 0.680 | 0.649 | FAIL |
| latin-aggregate | caveated-high-alpha | 0.739 [0.660, 0.789] | 0.811 | 0.815 | 0.553 | ok |
| Africa proconsularis | confirmatory | 0.661 [0.607, 0.724] | 0.473 | 0.808 | 0.504 | ok |
| Apulia et Calabria / Regio II | confirmatory | 0.775 [0.699, 0.832] | 0.634 | 0.666 | 0.638 | ok |
| Aquileia | confirmatory | 0.932 [0.894, 0.963] | 0.639 | 0.881 | 0.902 | ok |
| Baetica | confirmatory | 0.662 [0.618, 0.719] | 0.433 | 0.649 | 0.577 | ok |
| Dalmatia | caveated-high-alpha | 0.923 [0.882, 0.958] | 0.739 | 0.970 | 0.864 | ok |
| Etruria / Regio VII | confirmatory | 0.837 [0.755, 0.884] | 0.600 | 0.841 | 0.581 | ok |
| Germania inferior | confirmatory | 0.753 [0.717, 0.787] | 0.502 | 0.754 | 0.684 | ok |
| Germania superior | confirmatory | 0.508 [0.439, 0.561] | 0.364 | 0.514 | 0.305 | ok |
| Hispania citerior | confirmatory | 0.765 [0.706, 0.812] | 0.632 | 0.789 | 0.669 | ok |
| Italia (excl. Rome) | aggregate-added | 0.787 [0.753, 0.806] | 0.532 | 0.810 | · | ok |
| Lusitania | confirmatory | 0.788 [0.735, 0.843] | 0.522 | 0.804 | 0.695 | ok |
| Mogontiacum | confirmatory | 0.153 [0.130, 0.182] | 0.112 | 0.216 | 0.000 | ok |
| Pannonia superior | caveated-high-alpha | 0.765 [0.716, 0.818] | 0.735 | 0.864 | 0.644 | ok |
| Transpadana / Regio XI | confirmatory | 0.909 [0.849, 0.955] | 0.639 | 0.927 | 0.853 | ok |

## Verdict

- **Frontier units pinned within the H2.1 bounds (±0.05):** 8/10 — ['Britannia', 'Dacia', 'Moesia inferior', 'Numidia', 'Ostia', 'Pannonia inferior', 'Salona', 'Samnium / Regio IV']
- **Frontier units that moved up from the under-attributed α_shared:** Britannia 0.00→0.45, Dacia 0.00→0.17, Moesia inferior 0.05→0.70, Numidia 0.17→0.55, Ostia 0.34→0.70, Pannonia inferior 0.15→0.68, Salona 0.54→0.99, Samnium / Regio IV 0.27→0.86, Umbria / Regio VI 0.43→0.78, Venetia et Histria / Regio X 0.45→0.87.
- **Control stability (cc-α − H2.1 α_shared):** {'Latium et Campania / Regio I': -0.066, 'Noricum': -0.072, 'Pompeii': 0.015, 'empire-aggregate': 0.008, 'latin-aggregate': -0.072} (near 0 = controls unchanged, as required).
- **Convergence:** 28/29 pass.
- **Coverage caveat (signoff §6c):** reported CIs are ~1σ-optimistic by the grid's residual bias; high-%win×high-α units pair with the two-bound sensitivity as the disclosure.
