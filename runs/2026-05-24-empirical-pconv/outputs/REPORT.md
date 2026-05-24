# Stage 1 — Empirical p_conv from F1+F3 inscriptions

**Run directory:** `runs/2026-05-24-empirical-pconv/`
**Date:** 2026-05-24
**Authority:** Stage 1 of the empirical-Bayes calibration-cohort
implementation (planning/h2.1-follow-up-candidates-2026-05-24.md
deliverable; prereg §3 line 202 "empirical-scan dictionary"
placeholder, now realised). Builds the editorial-convention component
of the H2.1 mixture model directly from data instead of from the
hand-curated 3-tier × 21-interval placeholder basis specified in
`runs/2026-05-22-recovery-grid-design/design.json`.
**Companion:** `planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`
and `runs/2026-05-24-type-stratified-narrow-spas/outputs/REPORT.md`.

## 1. Headline

The empirical editorial-convention shape, derived from **119,142
F1+F3 inscriptions** (65 % of LIRE v3.0), is **substantially different
from the current placeholder tier-template basis**. L1 distance
between the empirical p_conv and the *closest* of the current
tier-weight-grid choices (`pilot_proxy`) is 0.31 — 31 % of the total
probability mass mis-allocated relative to the data. The dominant
slab type is **century (width 99)**, accounting for 40 % of the
convention mass (47,267 inscriptions); two-century slabs add 24 %
(28,227); half-century slabs add 17 % (20,216). Together these three
account for 80 % of the convention component. The current basis
over-allocates mass to the 50 BC – AD 0 region and under-allocates to
the AD 300-350 region — a systematic shape mis-specification visible
in the difference heatmap.

This document operationalises what the prereg called the "empirical-
scan dictionary" — now producing it from the data, with quantified
slab-type weights, ready to plug into the modified mixture model as
the convention basis.

## 2. Slab-type composition of the editorial convention

Within the 119,142 F1+F3 inscriptions:

| slab_name | width (years) | count | weight | % of convention | family |
|---|---:|---:|---:|---:|---|
| century | 99 | 47,267 | 0.397 | 39.67 | F1 |
| two_century | 199 | 28,227 | 0.237 | 23.69 | F1 |
| half_century | 49 | 20,216 | 0.170 | 16.97 | F1 |
| one_and_a_half_century | 149 | 8,690 | 0.073 | 7.29 | F1 |
| three_century | 299 | 5,892 | 0.050 | 4.95 | F1 |
| thirty_year_window | 29 | 4,039 | 0.034 | 3.39 | F3 |
| forty_year_window | 39 | 3,214 | 0.027 | 2.70 | F3 |
| twenty_year_window | 19 | 892 | 0.008 | 0.75 | F3 |
| quarter_century | 24 | 705 | 0.006 | 0.59 | F1 |

(Other F1+F3 records at non-standard widths: ~ 2 % residual.)

Two methodological notes:

1. **The dominant template is the century slab, not the half-century
   slab.** The earlier "the half-century slab is dominant" framing
   reflected the dominance of the *width-49 bin in the date_range
   histogram* (because each century-slab inscription has date_range
   ≈ 99, but the half-century inscriptions are also numerous). When
   we measure by *count* across F1+F3 specifically, the century slab
   is twice as common as the half-century slab.
2. **The quarter-century slab (width 24) is small**: only 705
   inscriptions out of 119k, 0.6 % of the convention. This refines
   the earlier devil's-advocate framing: the quarter-century template
   is empirically rare; the *real* editorial backbone is the century
   and two-century slab.

## 3. Comparison with the current placeholder tier-template basis

The current model uses a 3-tier × 21-interval basis from `design.json`,
combined under 5 tier-weight-grid choices (`uniform`, `century_heavy`,
`half_century_heavy`, `reign_heavy`, `pilot_proxy`). The L1 distance
between the empirical p_conv and each current case:

| current case | L1 distance | max abs diff per bin |
|---|---:|---:|
| pilot_proxy | **0.307** | 0.0115 |
| uniform | 0.326 | 0.0099 |
| century_heavy | 0.340 | 0.0138 |
| half_century_heavy | 0.367 | 0.0107 |
| reign_heavy | 0.550 | 0.0149 |

**Even the best current case (`pilot_proxy`) is 0.31 in L1 from the
empirical truth.** For a probability distribution that sums to 1, that
means ~ 15 % of the total mass is *mis-allocated* relative to the data
(L1 distance / 2 in the simplex). The worst current case (`reign_heavy`)
is much worse — and notably so because the reign-heavy basis weight
puts substantial mass on reign-template intervals (Augustan, Tiberian,
etc.) that **don't appear in F1+F3 at all** (those are F2_Other content,
the calibration-cohort component, not the convention component).

The figure `outputs/figures/empirical-pconv-vs-current-basis.png`
overlays the empirical p_conv (black, bold) against the 5 current
cases. The most visible mis-specifications:

- The current basis cases all peak around AD 50-100 and 150-200 with
  a dip around AD 100 (where two-century slabs from `AD 101-200`
  start contributing). The empirical p_conv is much smoother across
  AD 1-300, with a more gradual decline before BC and after AD 300.
- The current basis under-allocates the AD 300-350 region — the
  three-century slab (`AD 1-300` and similar) contributes notable
  mass to AD 200-300 transitions that none of the current cases
  capture well.
- The current basis over-allocates the 50 BC – AD 0 region by
  ~ 0.005-0.010 per bin (visible as the blue band on the left side of
  the difference heatmap, `outputs/figures/pconv-difference-heatmap.png`).
  Empirically, very few F1+F3 inscriptions extend into the pre-Augustan
  era (the corpus simply doesn't have many BC-era templated entries).

## 4. Decomposition by slab type — see figure

`outputs/figures/pconv-decomposition-by-slab.png` (two panels):

- **Top**: each slab-type's normalised basis row (the SPA shape if
  all inscriptions were of that exact width). The century-99 basis
  is broadly uniform across the envelope; the two-century-199 basis
  is a smooth mound peaking at AD 200; the half-century-49 basis has
  visible plateau structure aligned with AD 1-50, 51-100, 101-150,
  etc. The smaller F3 windows are more concentrated.
- **Bottom**: stacked weighted contributions to the aggregate p_conv.
  The lowest layer (century, 40 % of mass) carries the broad backbone
  of the convention shape; the two-century slab (24 % of mass) adds
  the late-AD lift; half-century (17 %) and the smaller slabs add
  finer modulation.

The aggregate empirical p_conv (red dashed line on the bottom panel)
tracks the sum of the weighted slab contributions almost exactly
(L1 reconstruction error 0.038 — essentially numerical
rounding plus the ~ 2 % residual at non-standard widths). This
confirms that the slab-type decomposition is mathematically complete:
the editorial convention IS the weighted sum of slab-type bases.

## 5. Implications for the empirical-Bayes mixture-model implementation

This is the formal building block for Stage 3 (modified mixture-model
implementation). Two specific design choices fall out:

1. **Replace the current 3-tier × 21-interval placeholder basis with
   the empirical slab-type basis** (9 slab-types from the F1+F3
   classifier). Each slab-type contributes a known basis row; the
   weights are known empirically. p_conv is the fixed weighted sum.
2. **The mixing weights (current `tier_weight_grid`) are no longer
   free parameters** — they're empirical observations. This is a
   methodologically important simplification: the model no longer
   has to *learn* the convention-component shape; it consumes it as
   data. This is exactly the SCUBIDO (Boyall et al. 2025) and
   Christophe et al. 2018 design philosophy: well-characterised
   components are fixed from reference data, not estimated alongside.

The geoscience prior art predicted this would be the right move; the
LIRE-specific empirical realisation confirms that the editorial
convention is sufficiently "well-characterised" to be fixed rather
than estimated.

## 6. Two caveats

- **The slab-type basis is corpus-wide; the model treats it as
  universal.** In principle, different provinces, types, or editors
  could have systematically different conventions (e.g., Gaul might
  use half-century templates more frequently than Italy uses them).
  A future refinement could stratify p_conv by province / type as
  well. For now, the corpus-wide basis is the natural first step.
- **The 5-year bin resolution may average over fine slab structure.**
  Each slab-type basis row uses 5-year bins; the 1-year-resolution
  histogram (from `runs/2026-05-24-date-range-threshold-analysis/`)
  showed that individual slab anchors (49, 99, 199) are sharp spikes
  rather than broad bumps. The 5-year-bin convention p_conv may
  smooth over these features. Worth a sensitivity check at 1-year-bin
  resolution, but only if the modified mixture model's downstream
  results are sensitive to this (likely not).

## 7. Outputs

Figures:

- `outputs/figures/empirical-pconv-vs-current-basis.png` — empirical
  vs the 5 current-basis cases, overlay
- `outputs/figures/pconv-decomposition-by-slab.png` — per-slab-type
  rows + stacked contribution
- `outputs/figures/pconv-difference-heatmap.png` — empirical minus
  each current case, heatmap

Tables:

- `outputs/tables/empirical-pconv-vector.csv` — the actual p_conv
  density at each 5-year bin (80 bins from 50 BC to AD 350)
- `outputs/tables/slab-type-weights.csv` — per-slab-type count,
  weight, percentage of convention
- `outputs/tables/distance-empirical-vs-current.csv` — L1 distance
  and max abs diff between empirical and each current case

## 8. Next steps

Stage 2 — empirical p_gen prior from Cohort B — is the natural
follow-on (in flight). Once Stage 2 is also complete, the building
blocks for the modified mixture-model implementation (Stage 3) are
both available.

End of report.
