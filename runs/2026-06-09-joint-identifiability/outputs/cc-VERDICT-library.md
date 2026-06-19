# Cross-classified grid — VERDICT (arm: library)

> **✅ THIS IS THE ADOPTED MODEL'S GATE VERDICT.** This file (arm: `library`) is
> the cross-classified `library` model's recovery-grid GATE — **the one that
> PASSED and was ADOPTED** as the production lead (A04; Obs 88/89;
> `cross-classified-signoff.md`). All four adoption criteria
> (cross-classified-spec.md §5) are met. The bracketed `[lead: …]` figures below
> are the **predicted-to-FAIL `lead` comparator baseline** (the full lead verdict
> is in the sibling file `grid-VERDICT.md`) — they are the baseline this adopted
> model is judged *against*, **not** a competing gate. Do not read the `lead`
> file's weaker numbers as a failure of this adopted model.

Cells with usable data: 300 (210 identifiable, 90 confounded). Fully-failed cells (n_ok=0): **0**.

## C1 — do-no-harm (identifiable)
- passing (|median bias|<0.12 AND coverage>=0.90): **76/210** (36%)  [lead: 37/210, 18%]
- mean |median bias| 0.021 [lead 0.075]; mean coverage 0.627 [lead 0.374]
- coverage on α>0 cells only: 0.784 (n=168) — α=0 cells cannot be covered by an equal-tailed CI (boundary artefact)

## C2 — pulled-to-truth (confounded; baseline from the lead grid)
- passing (|median bias|<0.18 AND bias<=+0.12 AND >baseline by 0.05): **72/90** (80%)  [lead: 64/90, 71%]
- mean median bias +0.005 [lead +0.066]; mean coverage 0.763 [lead 0.462]
- worst positive median bias +0.040
- cells with baseline available: 90/90; mean cc |bias| 0.009 vs baseline |bias| 0.362

## C4 — convergence
- cells with convergence_rate>=0.95: **287/300** (96%) [lead 84%]; mean rate 0.991 [lead 0.950]

## Bias surface — mean(median bias) by %win × α_true

| %win \ α | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| 0.53 | +0.01 | +0.01 | +0.02 | +0.02 | +0.01 |
| 0.63 | +0.01 | +0.00 | +0.00 | +0.01 | +0.01 |
| 0.83 | +0.01 | +0.01 | +0.01 | +0.01 | +0.02 |
| 0.95 | +0.01 | +0.01 | +0.02 | +0.02 | +0.02 |
| 1.00 | +0.01 | +0.02 | +0.03 | +0.03 | +0.02 |

## Adoption criteria (cross-classified-spec.md §5)

- 1_bias_flattens (ident |bias| < lead 0.075): **0.021**
- 2_C1_recovers (ident coverage > lead 0.374, toward 0.90): **0.627**
- 3_C2_not_sacrificed (conf |bias| stays << baseline 0.362): **0.009**
- 4_C4_not_worse (cell pass-rate >= lead 0.84): **0.957**

## Overall
- replicate failures: 0; fully-failed cells: 0
- grid scope: %win [0.527, 0.631, 0.834, 0.951, 1.0], α [0.0, 0.2, 0.4, 0.6, 0.8], N [1500, 2800, 15000]
