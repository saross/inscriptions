# C11 — trapezoidal-aoristic sensitivity

- Generated (UTC): 2026-06-18T13:30:18+00:00
- Spec: runs/2026-06-18-h2.1-supplementary-wave/SPEC.md §4 (C11)
- Scope: 28 + Italia-excl-Rome = 29 production units; C10 EXCLUDED (held).
- Sampling: 4 chains × (1000 tune + 2000 draws), cores=1, target_accept=0.95.

Material if the input-level r < 0.95 (uniform-vs-trapezoid SPA — the preregistered Decision-4 measure); the trapezoidal SPA is then reported alongside the uniform. Empire is pre-triggered (r = 0.94, 2026-05-17).

| unit | input r | report-alongside? |
|------|---------|-------------------|
| empire-aggregate | 0.9402 | YES |
| latin-aggregate | 0.9721 | no |
| Latium et Campania / Regio I | 0.9801 | no |
| Dalmatia | 0.9645 | no |
| Hispania citerior | 0.9703 | no |
| Germania superior | 0.9625 | no |
| Venetia et Histria / Regio X | 0.9540 | no |
| Dacia | 0.9976 | no |
| Britannia | 0.9827 | no |
| Pannonia superior | 0.9841 | no |
| Samnium / Regio IV | 0.9579 | no |
| Africa proconsularis | 0.9807 | no |
| Germania inferior | 0.9786 | no |
| Apulia et Calabria / Regio II | 0.9683 | no |
| Pannonia inferior | 0.9885 | no |
| Numidia | 0.9791 | no |
| Etruria / Regio VII | 0.9676 | no |
| Umbria / Regio VI | 0.9621 | no |
| Noricum | 0.9763 | no |
| Baetica | 0.9645 | no |
| Transpadana / Regio XI | 0.9611 | no |
| Pompeii | 0.9911 | no |
| Salona | 0.9650 | no |
| Ostia | 0.9864 | no |
| Mogontiacum | 0.9535 | no |
| Aquileia | 0.9269 | YES |
| Moesia inferior | 0.9917 | no |
| Lusitania | 0.9677 | no |
| Italia (excl. Rome) | 0.9703 | no |

- Units flagged report-alongside: 2 / 29.
- Trapezoidal apportionment reused from runs/2026-05-17-empirical-spa-shape/code/empirical_spa_shape.py (imported; original untouched).
- **Convention:** the input-level r matches trapezoid vs uniform under the 2026-05-17 inclusive-Roman convention (`trapezoidal_spa_on_h2_grid` vs `uniform_spa_2026_05_17`), isolating the mass SHAPE.
- **Output-level r DROPPED (audit M-1):** matching the deconvolution's clip-retained-fraction mass convention for a fair shape-isolation proved confound-prone (uniform-vs-uniform isolation r ≈ 0.64); the input-level r is the prereg measure and is clean. See BUILD-NOTES.md (M-1).

