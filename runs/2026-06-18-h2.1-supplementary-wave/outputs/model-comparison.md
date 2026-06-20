# C5 / C6 — model comparison (Dirichlet-multinomial + negative-binomial)

- Generated (UTC): 2026-06-18T13:30:18+00:00
- Spec: runs/2026-06-18-h2.1-supplementary-wave/SPEC.md §4 (C5/C6)
- Scope: 28 + Italia-excl-Rome = 29 production units; C10 EXCLUDED (held).
- Sampling: 4 chains × (1000 tune + 2000 draws), cores=1, target_accept=0.95.

**Method note (C1):** cross-family PSIS-LOO is NOT reported — it is inapplicable across the joint-multinomial (primary, DM; 3 log-lik points/unit) and per-bin negative-binomial (≈161 points/unit) observation structures. The model-comparison verdict is the α side-by-side (does the family move α?) plus the primary multinomial posterior-predictive dispersion ratio (is overdispersion warranted?). Each family's own within-family LOO is in the per-unit JSON.

## α side-by-side (median, 95 % CI) — does the family move α?

| unit | primary (lodged) | DM | NB | |Δα| DM | |Δα| NB |
|------|------------------|----|----|--------|--------|
| empire-aggregate | 0.6798 [0.6649, 0.6970] | 0.6789 [0.6597, 0.6998] | 0.6804 [0.6648, 0.6969] | 0.0 | 0.0 |
| latin-aggregate | 0.7387 [0.6596, 0.7893] | 0.7543 [0.6703, 0.8092] | 0.7387 [0.6588, 0.7892] | 0.0 | 0.0 |
| Latium et Campania / Regio I | 0.6058 [0.5684, 0.6324] | 0.6092 [0.5672, 0.6389] | 0.6050 [0.5665, 0.6323] | 0.0 | 0.0 |
| Dalmatia | 0.9232 [0.8822, 0.9581] | 0.9272 [0.8850, 0.9649] | 0.9240 [0.8846, 0.9602] | 0.0 | 0.0 |
| Hispania citerior | 0.7653 [0.7065, 0.8121] | 0.7645 [0.7061, 0.8132] | 0.7648 [0.7062, 0.8127] | 0.0 | 0.0 |
| Germania superior | 0.5083 [0.4393, 0.5612] | 0.5073 [0.4337, 0.5665] | 0.5092 [0.4403, 0.5636] | 0.0 | 0.0 |
| Venetia et Histria / Regio X | 0.8703 [0.8449, 0.8979] | 0.8702 [0.8446, 0.8980] | 0.8701 [0.8442, 0.8972] | 0.0 | 0.0 |
| Dacia | 0.1710 [0.1508, 0.1937] | 0.1713 [0.1497, 0.1956] | 0.1702 [0.1480, 0.1942] | 0.0 | 0.0 |
| Britannia | 0.4488 [0.3855, 0.5441] | 0.4510 [0.3832, 0.5554] | 0.4477 [0.3828, 0.5456] | 0.0 | 0.0 |
| Pannonia superior | 0.7654 [0.7161, 0.8184] | 0.7661 [0.7138, 0.8227] | 0.7656 [0.7155, 0.8194] | 0.0 | 0.0 |
| Samnium / Regio IV | 0.8602 [0.8281, 0.8980] | 0.8602 [0.8269, 0.8997] | 0.8590 [0.8277, 0.8975] | 0.0 | 0.0 |
| Africa proconsularis | 0.6607 [0.6068, 0.7239] | 0.6618 [0.6069, 0.7264] | 0.6604 [0.6078, 0.7240] | 0.0 | 0.0 |
| Germania inferior | 0.7534 [0.7170, 0.7874] | 0.7539 [0.7171, 0.7876] | 0.7534 [0.7171, 0.7864] | 0.0 | 0.0 |
| Apulia et Calabria / Regio II | 0.7752 [0.6992, 0.8319] | 0.7704 [0.6938, 0.8310] | 0.7748 [0.6954, 0.8312] | 0.0 | 0.0 |
| Pannonia inferior | 0.6761 [0.6320, 0.7373] | 0.6768 [0.6315, 0.7410] | 0.6762 [0.6329, 0.7364] | 0.0 | 0.0 |
| Numidia | 0.5543 [0.5304, 0.5812] | 0.5554 [0.5311, 0.5841] | 0.5545 [0.5309, 0.5821] | 0.0 | 0.0 |
| Etruria / Regio VII | 0.8367 [0.7553, 0.8842] | 0.8421 [0.7628, 0.8889] | 0.8370 [0.7618, 0.8827] | 0.0 | 0.0 |
| Umbria / Regio VI | 0.7807 [0.7343, 0.8333] | 0.7806 [0.7369, 0.8335] | 0.7806 [0.7347, 0.8315] | 0.0 | 0.0 |
| Noricum | 0.8081 [0.7743, 0.8472] | 0.8082 [0.7735, 0.8485] | 0.8080 [0.7737, 0.8496] | 0.0 | 0.0 |
| Baetica | 0.6617 [0.6184, 0.7193] | 0.6626 [0.6195, 0.7204] | 0.6612 [0.6188, 0.7181] | 0.0 | 0.0 |
| Transpadana / Regio XI | 0.9091 [0.8486, 0.9551] | 0.9106 [0.8511, 0.9579] | 0.9098 [0.8510, 0.9584] | 0.0 | 0.0 |
| Pompeii | 0.0156 [0.0102, 0.0223] | 0.0006 [0.0000, 0.0031] | 0.0003 [0.0000, 0.0014] | 0.0 | 0.0 |
| Salona | 0.9893 [0.9510, 0.9997] | 0.9906 [0.9531, 0.9997] | 0.9895 [0.9516, 0.9997] | 0.0 | 0.0 |
| Ostia | 0.7007 [0.6411, 0.7721] | 0.7028 [0.6431, 0.7731] | 0.7012 [0.6423, 0.7711] | 0.0 | 0.0 |
| Mogontiacum | 0.1529 [0.1297, 0.1820] | 0.1527 [0.1290, 0.1831] | 0.1530 [0.1292, 0.1822] | 0.0 | 0.0 |
| Aquileia | 0.9320 [0.8940, 0.9632] | 0.9325 [0.8931, 0.9641] | 0.9326 [0.8936, 0.9640] | 0.0 | 0.0 |
| Moesia inferior | 0.6984 [0.6168, 0.8233] | 0.6951 [0.6150, 0.8239] | 0.6981 [0.6172, 0.8267] | 0.0 | 0.0 |
| Lusitania | 0.7879 [0.7353, 0.8427] | 0.7878 [0.7350, 0.8455] | 0.7888 [0.7354, 0.8473] | 0.0 | 0.0 |
| Italia (excl. Rome) | 0.7872 [0.7532, 0.8064] | 0.7848 [0.7430, 0.8087] | 0.7866 [0.7529, 0.8059] | 0.0 | 0.0 |

> **|Δα| rounding note (added 2026-06-20).** The two `|Δα|` columns are rounded to 1 dp, so every unit prints 0.0. The underlying median shifts are nonzero but negligible; the **largest raw shift is latin-aggregate DM, |Δα| = |0.7387 − 0.7543| = 0.0156**, with Pompeii close behind (NB 0.0153, DM 0.0150 — a near-zero-α unit). The "family does not move α" verdict holds: max raw shift ≈ 0.016, well within MCMC noise. (This is the figure to cite at write-up — not a literal 0.0.)

## DM κ / NB φ posteriors + multinomial PPC dispersion (overdispersion warranted?)

| unit | κ median [95% CI] | φ median | disp. aligned | disp. non-al | overdisp.? |
|------|-------------------|----------|---------------|--------------|------------|
| empire-aggregate | 22734.7 [16953.7, 29176.4] | 5673.2 | 1.2 | 1.0 | YES |
| latin-aggregate | 23734.8 [17816.2, 29996.8] | 27441.8 | 0.4 | 1.1 | YES |
| Latium et Campania / Regio I | 17861.6 [12513.7, 24393.1] | 4243.6 | 0.3 | 0.8 | no |
| Dalmatia | 15381.4 [10178.0, 21752.4] | 3467.5 | 0.2 | 0.7 | no |
| Hispania citerior | 14102.1 [9037.8, 20547.1] | 2530.6 | 0.2 | 1.0 | no |
| Germania superior | 12810.5 [7865.5, 19373.8] | 1619.6 | 0.3 | 0.7 | no |
| Venetia et Histria / Regio X | 14768.6 [9614.4, 21106.5] | 2446.7 | 0.3 | 0.6 | no |
| Dacia | 8276.2 [3630.7, 14961.7] | 446.3 | 0.4 | 0.7 | no |
| Britannia | 9186.2 [4730.0, 16020.2] | 899.6 | 0.5 | 0.8 | no |
| Pannonia superior | 13121.1 [8128.5, 19807.3] | 2034.0 | 0.2 | 0.6 | no |
| Samnium / Regio IV | 13056.8 [8060.4, 19537.8] | 1594.2 | 0.3 | 0.6 | no |
| Africa proconsularis | 11236.6 [6464.0, 17701.3] | 1055.5 | 0.2 | 0.9 | no |
| Germania inferior | 12097.3 [7241.3, 18623.0] | 1482.8 | 0.2 | 0.7 | no |
| Apulia et Calabria / Regio II | 12482.0 [7717.1, 18737.4] | 1332.6 | 0.2 | 0.6 | no |
| Pannonia inferior | 11407.4 [6589.7, 17837.5] | 1236.6 | 0.2 | 0.6 | no |
| Numidia | 7516.8 [3333.2, 14398.3] | 759.1 | 0.6 | 1.0 | YES |
| Etruria / Regio VII | 11256.2 [6425.1, 17779.7] | 1007.5 | 0.2 | 0.9 | no |
| Umbria / Regio VI | 11875.5 [6945.3, 18507.7] | 1091.3 | 0.3 | 0.6 | no |
| Noricum | 12230.0 [7278.3, 18618.5] | 1443.3 | 0.1 | 0.5 | no |
| Baetica | 10787.8 [6014.6, 17462.3] | 918.1 | 0.3 | 0.8 | no |
| Transpadana / Regio XI | 11730.6 [6930.2, 18265.0] | 1249.1 | 0.1 | 0.7 | no |
| Pompeii | 61.8 [35.6, 105.8] | 1.3 | 1.8 | 0.9 | YES |
| Salona | 12210.5 [7224.4, 18623.0] | 1608.5 | 0.2 | 0.5 | no |
| Ostia | 11852.9 [7139.3, 18514.6] | 1065.7 | 0.1 | 0.6 | no |
| Mogontiacum | 8891.7 [4392.7, 15442.6] | 339.0 | 0.2 | 0.7 | no |
| Aquileia | 11451.7 [6508.8, 18293.1] | 1047.3 | 0.2 | 0.3 | no |
| Moesia inferior | 9242.1 [4702.8, 15912.7] | 650.3 | 0.2 | 0.8 | no |
| Lusitania | 10067.4 [5308.6, 16962.9] | 801.6 | 0.2 | 0.9 | no |
| Italia (excl. Rome) | 21822.8 [16220.5, 28120.4] | 11153.1 | 0.4 | 0.9 | no |

- DM κ prior: HalfNormal(σ = S_KAPPA = 5000) — pilot κ ≈ 5,800; σ = 5000 centres the weakly-informative prior near it (audit fix C2; see BUILD-NOTES.md).
- Dispersion ratio ≈ 1 ⇒ the multinomial primary is adequate (overdispersion NOT warranted); > 1 ⇒ DM/NB preferred. This is the prereg's stated DM/NB trigger (l.192) and the model-comparison adjudicator — NOT a cross-family information criterion (C1).
- Per-family within-family LOO (descriptive, NOT cross-compared) is in the per-unit JSON (outputs/units/, `*.model_comparison.{primary_refit,dm,nb}.within_family_waic`, whose sub-dict holds `ic:loo` + `elpd_loo`/`p_loo` — arviz 1.x has no WAIC, so the historically-named key carries LOO).

