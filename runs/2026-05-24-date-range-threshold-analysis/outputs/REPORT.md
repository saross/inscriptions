# Date-range threshold analysis — LIRE v3.0

**Run directory:** `runs/2026-05-24-date-range-threshold-analysis/`
**Date:** 2026-05-24
**Authority:** sharpens the threshold-choice question raised in the
2026-05-24 narrow-date conversation. Builds on the 2023-09-08 threshold
sweep (`archive/2023-09-08-inscriptions-spa.ipynb`) with: (a) fine 1-year
bins, (b) inscription-type breakdown at each cutoff, (c) running on
production LIRE v3.0 (rather than v2.3 from the notebook).
**Inputs:** `archive/data-2026-04-22/LIRE_v3-0.parquet` (182,853 records,
zero negative-range errors, zero NaN dates).

## 1. Headline

The LIRE v3.0 date-range distribution is **dominated by half-century and
century editorial slabs** (62 % of the corpus combined). Narrow-dated
subsets (< 25 y, < 50 y) provide tight temporal precision but are
**substantially type-biased**: epitaphs (56 % of the corpus) are
dramatically under-represented at < 25 y (11 %) and at < 50 y (40 %),
while honorific inscriptions (4 % of the corpus) are over-represented
at < 25 y (15 %). This is the Spektor & Kellen 2018 failure mode for
empirical-Bayes calibration cohorts, **made quantitatively visible in
our data**. For the three purposes Shawn raised — (a) calibration
cohort, (b) direct-SPA primary analysis, (c) editorial-process
diagnostic — the recommended thresholds differ; § 5 has the table.

## 2. Date-range distribution

LIRE v3.0 has the same shape as v2.3 (the difference is one record).
Mean 101.29 y, median 99 y, std-dev 76.75 y. Identical to within rounding.

### 2.1 Between-threshold counts

| range | count | % of corpus | editorial-template attribution (informed guess) |
|---|---:|---:|---|
| `[0, 1)` exact | 8,279 | 4.53 % | consular formula; dated event |
| `[1, 5)` | 6,034 | 3.30 % | regnal-event, tight career |
| `[5, 10)` | 3,262 | 1.78 % | military-diploma residual; mid-career |
| `[10, 25)` | 8,415 | 4.60 % | regnal-window; military-diploma tail |
| `[25, 50)` | **35,122** | **19.21 %** | **quarter-century slab** |
| `[50, 100)` | **67,163** | **36.73 %** | **half-century slab — DOMINANT** |
| `[100, 200)` | 45,651 | 24.97 % | **century slab** |
| `[200, 300)` | 7,995 | 4.37 % | two-century slab |
| `≥ 300` | 932 | 0.51 % | "Imperial-period generally", etc. |

### 2.2 Cumulative under-threshold counts (calibration-cohort candidates)

| cutoff | retained | % retained | excluded |
|---|---:|---:|---:|
| < 1 y | 8,279 | 4.53 % | 95.47 % |
| < 5 y | 14,313 | 7.83 % | 92.17 % |
| < 10 y | 17,575 | 9.61 % | 90.39 % |
| < 25 y | 25,990 | 14.21 % | 85.79 % |
| < 50 y | 61,112 | 33.42 % | 66.58 % |
| < 100 y | 128,275 | 70.15 % | 29.85 % |
| < 200 y | 173,926 | 95.12 % | 4.88 % |

### 2.3 Williams ΔT (mean temporal precision under uniform-within-interval)

The Williams 2012 ΔT measure is the mean of per-inscription σ assuming
each inscription's true date is uniform on `[not_before, not_after]`.
σ for a uniform on `[a, b]` is `(b - a) / √12`. Aggregating across the
subset, this gives the typical positional uncertainty in years.

| cutoff | mean σ (years) | n |
|---|---:|---:|
| ≤ 1 y | 0.07 | 11,069 |
| ≤ 5 y | 0.33 | 15,500 |
| ≤ 10 y | 0.61 | 18,104 |
| ≤ 25 y | **2.0** | 26,162 |
| ≤ 50 y | **8.0** | 61,743 |
| ≤ 100 y | 17.5 | 128,937 |
| ≤ 200 y | 26.3 | 174,096 |
| no cutoff | 29.2 | 182,853 |

Doubling the cutoff roughly doubles σ. At < 25 y we have ~ 2-year
precision; at < 50 y we have ~ 8-year precision; at < 100 y we have ~ 18-year.

## 3. Slab fingerprint visible in the fine-grained histogram

See `outputs/figures/histogram-fine-1y-bins-0-300y.png` and the log-y
variant `histogram-fine-1y-bins-log-y.png`. Sub-50y zoom at
`histogram-sub-50y-zoom.png`.

What the figures show, in order of visual dominance:

- A massive spike at exactly 100 years (the "century" template).
- A nearly-equal spike at exactly 50 years (the "half-century" template).
- A clearly visible spike at exactly 25 years (the "quarter-century" template).
- Smaller but visible spikes at exactly 200 y, 75 y, 33 y, 67 y.
- A spike at 0 (exact dates).
- A small spike at 9 (probably some regnal-window convention).
- A long tail above 200 y, mostly the imperial-period-generally template.

The 25 y boundary is genuinely a slab edge. The histogram drops from a
clear peak at 25 y to near-baseline at 24 y. Cutting at < 25 y excludes
the quarter-century slab cleanly.

## 4. Type composition by cutoff — the critical finding

The narrow-dated subset is **dramatically type-biased**. See
`outputs/figures/type-composition-by-cutoff-stacked.png` for the visual;
the table below quantifies it (% of records of each type *within* each
cutoff):

| cutoff | N | epitaph | votive | identification | honorific | building/ded. | mile-stone | mil. diploma | other | unknown |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| < 1 y | 8,279 | 6.96 | 13.98 | 18.96 | 11.18 | 4.20 | 8.38 | 3.37 | 2.32 | 30.64 |
| < 5 y | 14,313 | 5.21 | 11.51 | 15.97 | 14.64 | 5.61 | 12.24 | 2.46 | 1.99 | 30.38 |
| < 10 y | 17,575 | 6.12 | 11.07 | 18.87 | 14.60 | 5.16 | 11.35 | 2.14 | 1.88 | 28.81 |
| < 25 y | 25,990 | 10.58 | 10.68 | 18.66 | 14.76 | 6.09 | 9.04 | 1.62 | 2.71 | 25.89 |
| < 50 y | 61,112 | 40.04 | 7.65 | 16.20 | 7.97 | 3.44 | 4.04 | 0.71 | 1.61 | 18.35 |
| < 100 y | 128,275 | 52.65 | 7.95 | 13.66 | 4.75 | 2.14 | 2.01 | 0.34 | 1.23 | 15.25 |
| all | 182,853 | **55.87** | 9.24 | 12.50 | 3.64 | 1.96 | 1.49 | 0.24 | 1.20 | 13.85 |

**The story this table tells:**

- **Epitaphs are dramatically under-represented in narrow-dated subsets.**
  56 % of the corpus is epitaphs, but only 11 % of the < 25 y subset and
  7 % of the < 5 y subset. Epitaphs are typically dated only to the
  half-century or century (median date-range for epitaphs = 99 y; only
  2.7 % have date-range < 25 y).
- **Honorific inscriptions are over-represented at narrow cutoffs.** 4 %
  of the corpus but 15 % of the < 25 y subset. The median honorific
  date-range is 18 y; 58 % have date-range < 25 y. Honorifics anchor to
  political events and named officials, which is why they're tight-dated.
- **Military diplomas are concentrated almost entirely in the very narrow
  range** (median 0 y; 95 % have date-range < 25 y; 442 records total).
  At < 25 y they're 1.6 % of the subset; in the full corpus only 0.24 %.
- **Mile-/leaguestones are similar to military diplomas** but less extreme
  (median 2 y; 86 % < 25 y). Over-represented at < 25 y (9 %) vs corpus
  (1.5 %).
- **Identification inscriptions** (owner/artist + identification labels;
  median 69 y) sit in the middle. Over-represented at narrow cutoffs but
  not by a huge margin.
- **"Unknown" inscriptions** (NaN in the auto-classifier) are
  *over*-represented at narrow cutoffs (31 % at < 1 y vs 14 % overall),
  which is suspicious — possibly because formulaic templates without
  obvious inscription-type markers are still tightly dated by their
  formula.

**Implication for the calibration-cohort approach**: the narrow-dated
SPA is not a representative sample of "ancient inscription activity".
It's a sample of activities that happened to be precisely dateable —
which is itself a temporally-non-uniform process. Using the narrow-dated
SPA as an unweighted prior on `p_gen` would inject an
inscription-type-conditioned temporal pattern into the prior, with
unclear bias effect on the corpus-wide α estimate.

## 5. Recommended thresholds, by purpose

| purpose | recommended cutoff | rationale | sample size | known biases |
|---|---|---|---:|---|
| **(a) Empirical-Bayes calibration cohort** for `p_gen` | **< 50 y** | Sweet spot of size (61k records) + temporal precision (σ ≈ 8 y) + reasonably-close-to-corpus type composition (40 % epitaph vs 56 % corpus). Type-reweighting recommended to correct residual bias. | 61,112 | Epitaph under-rep (40 % vs 56 %); honorific over-rep (8 % vs 4 %); identification over-rep (16 % vs 13 %). Smaller. |
| **(b) Direct SPA / scaling analysis** | **< 25 y** or stratified by type | Tight precision (σ ≈ 2 y); 26k records still large by epigraphic standards; the [25, 50) slab is cleanly excluded. *But*: severe type bias (11 % epitaph vs 56 %); honorific + identification dominate. | 25,990 | **Severe.** Best use is for type-conditional analyses or to triangulate against full-corpus mixture-model results. |
| **(c) Editorial-process diagnostic** | full corpus | Histogram is the diagnostic; slabs at 25, 50, 100, 200 y are the editorial fingerprint. | 182,853 | None — we *want* to see the bias. |

The 25 y vs 50 y question Shawn raised specifically: **25 y excludes the
quarter-century slab** (the cleanest interpretation in terms of
"narrow-dated = not from a wide editorial template"). **50 y includes the
quarter-century slab** (which contaminates the SPA with the
quarter-century template fingerprint). For purpose (b), 25 y is cleaner;
for purpose (a) where the prior is Gaussian-smoothed, 50 y's bigger
sample wins.

## 6. Outputs

- `outputs/figures/histogram-fine-1y-bins-0-300y.png` — fine histogram, linear y
- `outputs/figures/histogram-fine-1y-bins-log-y.png` — same, log y (small spikes visible)
- `outputs/figures/histogram-sub-50y-zoom.png` — sub-50y zoom (1y bins)
- `outputs/figures/type-composition-by-cutoff-stacked.png` — stacked-bar % type by cutoff
- `outputs/tables/counts-between-thresholds.csv`
- `outputs/tables/counts-cumulative-under.csv`
- `outputs/tables/williams-delta-t-by-cutoff.csv`
- `outputs/tables/type-composition-by-cutoff.csv` (counts + percentages)
- `outputs/tables/type-composition-by-cutoff-pct.csv` (percentages only)
- `outputs/tables/median-date-range-by-type.csv`
- `code/analyse-thresholds.py` — the analysis script

## 7. What this means for the Bayesian correction (companion methodology note)

The intuition Shawn raised — "combine the narrow-date signal with the
slab structure" — translates to a specific Bayesian model: instead of
asking the mixture to discover both components from the data, derive
**both** mixture components empirically. p_gen ← informative prior from
the narrow-dated subset (type-reweighted to match corpus composition).
p_conv ← informative prior from the slab structure of wide-dated
inscriptions (the empirical distribution of which template-widths
appear, at what starting-points). α becomes the only free quantity.

This is the strongest version of the empirical-Bayes approach we've
discussed. The full methodological note is in
`planning/h2.1-mixture-model-problem-explained-2026-05-24.md` (the
companion explanatory document) once that's revised to incorporate the
threshold-analysis findings.

## 8. Caveats

- The type-auto classifier has 14 % NaN coverage in the full corpus
  (more like 25–31 % NaN in the narrow-dated subsets). This is a real
  source of uncertainty in the type-breakdown percentages.
- The prereg uses LIRE v3.0 with a 50 BC – AD 350 filter. This analysis
  uses the full unfiltered corpus (182,853 records). The filtered
  corpus has different size (~ 148k strict / 183k overlap depending on
  filter definition) but the qualitative slab structure is identical.
  Worth re-running with the prereg filter if final pre-Phase-2 numbers
  are needed.
- The Williams ΔT calculation assumes uniform within `[not_before,
  not_after]`. If the true ancient pattern is not uniform within an
  inscription's date-range (which it isn't, generally), the σ values
  are an under-estimate of effective temporal uncertainty. They are
  comparable across cutoffs, which is what we need them for here.

## Observations register cross-reference

Lodged in the register at **Obs 54** (interval *structure* not width is the right partition — this threshold sweep is the negative result that motivated the family classifier) and **Obs 55** (the empirical-Bayes calibration-cohort pivot; this report is cited as a *Source*). See `docs/notes/working-notes.md`. Sibling: `runs/2026-05-24-type-stratified-narrow-spas/`. Back-reference added 2026-06-20 (results-documentation uplift, Tier-2 item 10) to close the one-directional Obs link.

End of report.
