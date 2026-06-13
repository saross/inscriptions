# cc-library production refit — VERDICT

Units fitted: 29. Convergence failures: **1** — ['empire-aggregate'].

## Per-unit α: cc-library vs the H2.1 two-bound diagnostic

| unit | tier | cc-α [95% CI] | H2.1 α_shared | α_perunit | implied-α | conv |
|---|---|---|---|---|---|---|
| Britannia | under-identified | 0.400 [0.340, 0.497] | 0.002 | 0.793 | 0.279 | ok |
| Dacia | confirmatory | 0.157 [0.138, 0.178] | 0.001 | 0.344 | 0.014 | ok |
| Moesia inferior | under-identified | 0.626 [0.532, 0.765] | 0.050 | 0.870 | 0.520 | ok |
| Numidia | under-identified | 0.546 [0.522, 0.573] | 0.166 | 0.515 | 0.425 | ok |
| Ostia | under-identified | 0.650 [0.577, 0.735] | 0.335 | 0.775 | 0.544 | ok |
| Pannonia inferior | under-identified | 0.630 [0.576, 0.696] | 0.147 | 0.751 | 0.566 | ok |
| Salona | under-identified | 0.987 [0.942, 1.000] | 0.538 | 0.995 | 0.945 | ok |
| Samnium / Regio IV | under-identified | 0.840 [0.803, 0.883] | 0.272 | 0.860 | 0.834 | ok |
| Umbria / Regio VI | under-identified | 0.738 [0.682, 0.800] | 0.429 | 0.700 | 0.722 | ok |
| Venetia et Histria / Regio X | under-identified | 0.844 [0.803, 0.880] | 0.452 | 0.809 | 0.853 | ok |
| Latium et Campania / Regio I | confirmatory | 0.595 [0.557, 0.622] | 0.672 | 0.621 | 0.374 | ok |
| Noricum | caveated-high-alpha | 0.784 [0.742, 0.830] | 0.880 | 0.829 | 0.736 | ok |
| Pompeii | confirmatory | 0.015 [0.010, 0.021] | 0.001 | 0.003 | 0.000 | ok |
| empire-aggregate | confirmatory | 0.671 [0.655, 0.689] | 0.672 | 0.680 | 0.649 | FAIL |
| latin-aggregate | caveated-high-alpha | 0.726 [0.640, 0.781] | 0.811 | 0.815 | 0.553 | ok |
| Africa proconsularis | confirmatory | 0.630 [0.573, 0.702] | 0.473 | 0.808 | 0.504 | ok |
| Apulia et Calabria / Regio II | confirmatory | 0.741 [0.659, 0.815] | 0.634 | 0.666 | 0.638 | ok |
| Aquileia | confirmatory | 0.915 [0.866, 0.955] | 0.639 | 0.881 | 0.902 | ok |
| Baetica | confirmatory | 0.624 [0.574, 0.686] | 0.433 | 0.649 | 0.577 | ok |
| Dalmatia | caveated-high-alpha | 0.913 [0.866, 0.953] | 0.739 | 0.970 | 0.864 | ok |
| Etruria / Regio VII | confirmatory | 0.812 [0.714, 0.868] | 0.600 | 0.841 | 0.581 | ok |
| Germania inferior | confirmatory | 0.730 [0.687, 0.770] | 0.502 | 0.754 | 0.684 | ok |
| Germania superior | confirmatory | 0.481 [0.408, 0.542] | 0.364 | 0.514 | 0.305 | ok |
| Hispania citerior | confirmatory | 0.743 [0.679, 0.796] | 0.632 | 0.789 | 0.669 | ok |
| Italia (excl. Rome) | aggregate-added | 0.779 [0.740, 0.800] | 0.532 | 0.810 | · | ok |
| Lusitania | confirmatory | 0.757 [0.695, 0.824] | 0.522 | 0.804 | 0.695 | ok |
| Mogontiacum | confirmatory | 0.139 [0.118, 0.166] | 0.112 | 0.216 | 0.000 | ok |
| Pannonia superior | caveated-high-alpha | 0.734 [0.676, 0.798] | 0.735 | 0.864 | 0.644 | ok |
| Transpadana / Regio XI | confirmatory | 0.892 [0.824, 0.948] | 0.639 | 0.927 | 0.853 | ok |

## Verdict

- **Frontier units pinned within the H2.1 bounds (±0.05):** 10/10 — ['Britannia', 'Dacia', 'Moesia inferior', 'Numidia', 'Ostia', 'Pannonia inferior', 'Salona', 'Samnium / Regio IV', 'Umbria / Regio VI', 'Venetia et Histria / Regio X']
- **Frontier units that moved up from the under-attributed α_shared:** Britannia 0.00→0.40, Dacia 0.00→0.16, Moesia inferior 0.05→0.63, Numidia 0.17→0.55, Ostia 0.34→0.65, Pannonia inferior 0.15→0.63, Salona 0.54→0.99, Samnium / Regio IV 0.27→0.84, Umbria / Regio VI 0.43→0.74, Venetia et Histria / Regio X 0.45→0.84.
- **Control stability (cc-α − H2.1 α_shared):** {'Latium et Campania / Regio I': -0.077, 'Noricum': -0.096, 'Pompeii': 0.014, 'empire-aggregate': -0.001, 'latin-aggregate': -0.085} (near 0 = controls unchanged, as required).
- **Convergence:** 28/29 pass.
- **Coverage caveat (signoff §6c):** reported CIs are ~1σ-optimistic by the grid's residual bias; high-%win×high-α units pair with the two-bound sensitivity as the disclosure.
