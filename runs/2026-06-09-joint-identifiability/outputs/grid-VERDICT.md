# Joint recovery grid — VERDICT

Cells with usable data: 300 (210 identifiable, 90 confounded). Fully-failed cells (n_ok=0): **0**.

## C1 — do-no-harm (identifiable)
- passing (|median bias|<0.12 AND coverage>=0.90): **37/210** (18%)
- mean |median bias| 0.075; mean coverage 0.374

## C2 — pulled-to-truth (confounded)
- passing (|median bias|<0.18 AND bias<=+0.12 AND >baseline by 0.05): **64/90** (71%)
- mean median bias +0.066; mean coverage 0.462
- worst positive median bias +0.164
- cells with baseline recorded: 90/90; mean lead |bias| 0.066 vs mean baseline |bias| 0.362

## C4 — convergence
- cells with convergence_rate>=0.95: **252/300** (84%); mean rate 0.950

## Bias surface — mean(median bias) by %win × α_true

| %win \ α | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| 0.53 | +0.08 | +0.08 | +0.08 | +0.08 | +0.06 |
| 0.63 | +0.08 | +0.07 | +0.07 | +0.07 | +0.06 |
| 0.83 | +0.08 | +0.07 | +0.07 | +0.07 | +0.06 |
| 0.95 | +0.08 | +0.07 | +0.08 | +0.08 | +0.06 |
| 1.00 | +0.08 | +0.07 | +0.08 | +0.08 | +0.06 |

## Overall
- replicate failures across grid: 0 (in 0 cells)
- fully-failed cells: 0
- grid scope: %win [0.527, 0.631, 0.834, 0.951, 1.0], α [0.0, 0.2, 0.4, 0.6, 0.8], N [1500, 2800, 15000]
