# Would the cc-library deconvolution help H3a (and the other count analyses)?

> Diagnostic answer to Shawn's 2026-06-15 question. Generated from the data
> (`outputs/alpha-population-diagnostic.json`). H3a/H3c are unchanged by this; it
> is a leverage/robustness check, not a confirmatory result.

## Verdict

**On the evidence we have, the deconvolution does NOT materially change the Hanson scaling — raw-count H3a is robust to convention-correction.**

The implied shift in the Hanson scaling exponent from replacing the raw count *N*
with the genuine count α·N equals the slope of log(α) on log(population) across the
26 non-aggregate deconvolved units. **α is uncorrelated with
population** (Spearman -0.11, Pearson
+0.13 — near zero, opposite signs).

The OLS point estimate Δβ = +0.292
(95% bootstrap CI [-0.112, +0.865]) is **not robust** — it is dominated
by a single high-leverage near-zero-α unit (**Pompeii**, whose
removal collapses it to +0.015). The robust
estimators agree on ≈ 0: **Theil-Sen Δβ = -0.030**;
drop-low-α (α<0.10) OLS = +0.015, Theil-Sen
= -0.045. So there is **no robust
evidence the deconvolution would shift the Hanson scaling.**

## Why this is the right statistic

1. **Temporal reshaping cannot touch H3a's count.** H3a's date window is the full
   envelope (50 BC – AD 350; `h3a_common.DATE_WINDOW`). The deconvolution moves mass
   *between* time-bins but conserves each unit's full-window total — the raw aoristic
   SPA and the genuine SPA both normalise to the same n_eff. So the only channel left
   is the genuine fraction α. (The shape change is real but irrelevant to a full-window
   count: median total-variation distance between raw and genuine SPA =
   0.243, max 0.500 — that is what H3b,
   already done, reads; H3a does not.)
2. **α enters only as a multiplier.** Genuine count = α·N, so the scaling exponent
   shifts by exactly the trend of log(α) against log(population). Flat α ⇒ constant
   multiplier ⇒ unchanged β.

## What α looks like across the units

- α range [0.02, 0.99], mean
  0.68 (SD 0.25).
- **α vs population:** Spearman -0.11, Pearson
  +0.13.
- **α vs corpus size (n_eff):** Spearman -0.22, Pearson
  -0.17.

See `figures/fig-alpha-vs-size.png`.

### Single-city units (direct α-vs-population)
| name | alpha_median | hanson_pop_total | n_eff |
|---|---|---|---|
| Ostia | 0.70 | 35,016 | 2,316 |
| Mogontiacum | 0.15 | 19,930 | 2,325 |
| Aquileia | 0.93 | 14,596 | 1,885 |
| Pompeii | 0.02 | 9,938 | 4,247 |
| Salona | 0.99 | 9,498 | 2,890 |

### Aggregates (context only; excluded from the correlation)
| name | alpha_median | hanson_pop_total | n_eff |
|---|---|---|---|
| empire-aggregate | 0.68 | 7,444,576 | 151,361 |
| latin-aggregate | 0.74 | 4,246,252 | 101,066 |
| Italia (excl. Rome) | 0.79 | 1,431,244 | 40,499 |

## What this means for leveraging the deconvolution

- **H3a / SR1 (count-based scaling):** the preregistered primary stays raw-count
  (Decision 22/35; a lodged confirmatory primary, and — given the above — the
  deconvolution would not move it materially anyway).
  The deconvolution's H3a value-add is the preregistered **D13 α-as-translator §5
  sensitivity**, which needs **per-city** α (only 29 province/region-level units are
  deconvolved so far). This diagnostic is the province-level proxy; the definitive
  city-level test is the per-city mixture build.
- **Already fully leveraged:** H3b (runs on the genuine SPA) and the descriptive
  genuine-vs-raw SPA figures — that is where the reshaping (TV up to
  0.50) does its work.
- **Letter-count, H3c:** inherit H3a's treatment; same α-sensitivity route.

## Caveat

α is available only at the 29 deconvolved units (mostly province/region-level). The
slope above is a province-level proxy for the city-level H3a confound; it is
reassuringly flat, but the city-level confound is
only directly testable with a per-city deconvolution (D13). Aggregates excluded from
the correlation to avoid double-counting.

## Reproduce
```bash
uv run python runs/2026-06-16-deconv-leverage-diagnostic/code/deconv_leverage_diagnostic.py
```
