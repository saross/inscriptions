# H2.1 supplementary wave — production REPORT

- Generated (UTC): 2026-06-18T13:30:18+00:00
- Spec: runs/2026-06-18-h2.1-supplementary-wave/SPEC.md §§4, 6, 7, 11
- Scope: 28 + Italia-excl-Rome = 29 production units; C10 EXCLUDED (held).
- Sampling: 4 chains × (1000 tune + 2000 draws), cores=1, target_accept=0.95.

## C16 — α descriptive read-off (from the lodged refit summary)

| unit | frame | N_eff | α median | 95 % CI | conv | below floor? |
|------|-------|-------|----------|---------|------|--------------|
| Britannia | latin | 4407 | 0.4488 | [0.3855, 0.5441] | ok | no |
| Dacia | latin | 4718 | 0.1710 | [0.1508, 0.1937] | ok | no |
| Moesia inferior | latin | 1728 | 0.6984 | [0.6168, 0.8233] | ok | YES |
| Numidia | latin | 2727 | 0.5543 | [0.5304, 0.5812] | ok | no |
| Ostia | latin | 2316 | 0.7007 | [0.6411, 0.7721] | ok | no |
| Pannonia inferior | latin | 2812 | 0.6761 | [0.6320, 0.7373] | ok | no |
| Salona | latin | 2890 | 0.9893 | [0.9510, 0.9997] | ok | no |
| Samnium / Regio IV | latin | 3952 | 0.8602 | [0.8281, 0.8980] | ok | no |
| Umbria / Regio VI | latin | 2573 | 0.7807 | [0.7343, 0.8333] | ok | no |
| Venetia et Histria / Regio X | latin | 5560 | 0.8703 | [0.8449, 0.8979] | ok | no |
| Latium et Campania / Regio I | latin | 17037 | 0.6058 | [0.5684, 0.6324] | ok | no |
| Noricum | latin | 2600 | 0.8081 | [0.7743, 0.8472] | ok | no |
| Pompeii | latin | 4247 | 0.0156 | [0.0102, 0.0223] | ok | no |
| empire-aggregate | empire | 151361 | 0.6798 | [0.6649, 0.6970] | FAIL | no |
| latin-aggregate | latin | 101066 | 0.7387 | [0.6596, 0.7893] | ok | no |
| Africa proconsularis | latin | 2967 | 0.6607 | [0.6068, 0.7239] | ok | no |
| Apulia et Calabria / Regio II | latin | 3012 | 0.7752 | [0.6992, 0.8319] | ok | no |
| Aquileia | latin | 1885 | 0.9320 | [0.8940, 0.9632] | ok | YES |
| Baetica | latin | 2449 | 0.6617 | [0.6184, 0.7193] | ok | no |
| Dalmatia | latin | 6325 | 0.9232 | [0.8822, 0.9581] | ok | no |
| Etruria / Regio VII | latin | 2426 | 0.8367 | [0.7553, 0.8842] | ok | no |
| Germania inferior | latin | 3261 | 0.7534 | [0.7170, 0.7874] | ok | no |
| Germania superior | latin | 5570 | 0.5083 | [0.4393, 0.5612] | ok | no |
| Hispania citerior | latin | 6011 | 0.7653 | [0.7065, 0.8121] | ok | no |
| Italia (excl. Rome) | latin | 40499 | 0.7872 | [0.7532, 0.8064] | ok | no |
| Lusitania | latin | 1577 | 0.7879 | [0.7353, 0.8427] | ok | YES |
| Mogontiacum | latin | 2325 | 0.1529 | [0.1297, 0.1820] | ok | no |
| Pannonia superior | latin | 4174 | 0.7654 | [0.7161, 0.8184] | ok | no |
| Transpadana / Regio XI | latin | 2201 | 0.9091 | [0.8486, 0.9551] | ok | no |

## Design-artefact pins (SPEC §5; re-stated, not re-derived)

- N_MC = 30, divergence-flag = 1.5× — pertain to C10 (aoristic-MC), which is HELD and NOT run by this driver.
- W1 (Wasserstein-1, shape) flagging threshold inherited from the recovery grid (runs/2026-05-26-recovery-grid-two-unit/): Pearson r ≥ 0.95 (non-flat) / W1 ≤ 10 y (flat_baseline). Re-stated per SPEC §5; not re-derived.

## Per-item deliverables

- C5 / C6: `model-comparison.md`  - C11: `trapezoidal.md`
- H2.2: `h2.2-boundary-steps.md`  - H2.3: `h2.3-threshold-convergence.md`
- H2.4: `h2.4-stratified.md`  - C16: this file.

## Convergence surfacing (SPEC §7)

Per-fit convergence failures (reported as per-unit limitations, NOT blockers; empire-aggregate is the known under-converger):

- empire-aggregate / nb (R̂=1.0126, ESS=610)

