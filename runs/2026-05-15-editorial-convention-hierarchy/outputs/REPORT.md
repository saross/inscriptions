---
title: "Editorial-convention-hierarchy diagnostic — results"
date: 2026-05-15
author: "Claude Code (Opus 4.7, 1M context) under Shawn Ross's direction"
status: complete
inputs: "LIRE v3.0, filtered to 180,609 rows per the preregistration's §1 specification"
informs: "preregistration-draft.md (c)-3 — `convention_SPA` shape in the Bayesian deconvolution-mixture model (Decision 14)"
---

# Editorial-convention-hierarchy diagnostic — results

## Headline finding

**The editorial-convention hierarchy is real, strong, and structured — but its
dominant axis is not what the preregistration currently models.** The hierarchy
operates on *interval endpoints*, not on aoristic midpoints, and follows the
inclusive-Roman century convention (centuries running 1–100, 101–200, etc.) far
more than the exclusive convention (0–99, 100–199, etc.).

Concretely, 54.5% of all `not_before` values in the filtered corpus end in
`01` and 53.0% of all `not_after` values end in `00`. Two-thirds of `not_after`
values are either `00` or `50`; two-thirds of `not_before` values are either
`01` or `51`. The "century-midpoint inflation" pattern the descriptive-stats
run measured at AD 50/150/250/350 is a *derivative* effect — aoristic mass
concentrates at those midpoints because the underlying interval endpoint pairs
(e.g. `[1, 100]`, `[101, 200]`, `[51, 100]`, `[151, 200]`) have midpoints
that fall there.

This has direct implications for Decision 14's Bayesian-mixture `convention_SPA`
spec: the convention component should model **endpoint rounding** at
inclusive-Roman boundaries (year ≡ 1 mod 100 for starts; year ≡ 0 mod 100
for ends; year ≡ 51 mod 100 for half-century starts; year ≡ 50 mod 100 for
half-century ends), with reign-related years as a smaller secondary layer.

## Tier ranking (combined endpoints, σ = 20-year smoothing baseline)

| Tier | n years | geo-mean O/E | median O/E |
|---|---:|---:|---:|
| century-incl-start (year ≡ 1 mod 100) | 4 | **20.28** | 21.55 |
| century-incl-end (year ≡ 0 mod 100) | 4 | **18.34** | 16.30 |
| century-midpoint (year ≡ 50 mod 100) | 4 | **10.16** | 9.80 |
| half-century-incl-start (year ≡ 51 mod 100) | 4 | **2.44** | 6.82 |
| reign-related (curated list) | 39 | 0.75 | 0.78 |
| quarter-century-end (year ≡ 25 or 75 mod 100) | 8 | 0.51 | 0.45 |
| decade-end (year ≡ 0 mod 10, not above) | 33 | 0.51 | 0.34 |
| decade-start (year ≡ 1 mod 10, not above) | 32 | 0.27 | 0.20 |
| quarter-century-start (year ≡ 26 or 76 mod 100) | 8 | 0.24 | 0.23 |
| lustrum (year ≡ 5 or 6 mod 10, not above) | 64 | 0.10 | 0.12 |

The three top tiers (centuries-incl-start, centuries-incl-end, century-midpoints)
all show O/E > 10×. Sub-century tiers (quarter-century, decade, lustrum) all
sit *below* baseline — they are if anything *depleted*, because the smoothing
baseline absorbs the nearby spike mass.

**Bandwidth sensitivity** (σ = 5, 10, 20, 30) preserves the ranking — only
absolute O/E magnitudes shift. Files `tier_summary_combined.csv` etc. carry
the full sensitivity table.

## Per-endpoint asymmetry

The `not_before` and `not_after` columns cluster on *different* tiers — exactly
as inclusive-Roman counting predicts:

**not_before (interval starts) — top tiers:**
| Tier | geo-mean O/E |
|---|---:|
| century-incl-start (1, 101, 201, 301) | **36.55** |
| half-century-incl-start (51, 151, 251) | 4.13 |
| reign-related | 0.62 |

**not_after (interval ends) — top tiers:**
| Tier | geo-mean O/E |
|---|---:|
| century-incl-end (0, 100, 200, 300) | **36.30** |
| century-midpoint (50, 150, 250, 350) | **18.20** |
| quarter-century-end | 0.67 |

`not_before` clusters at century *starts* under inclusive counting; `not_after`
clusters at century *ends* under inclusive counting *and* at century midpoints
(year ≡ 50 mod 100). The half-century midpoint shows in `not_after` rather
than `not_before` — i.e. an interval like `[51, 150]` ends at a "midpoint
year." Half-century *starts* (51, 151) only show in `not_before`.

## Trailing-digit dominance

The two-digit residue concentration is extreme:

**not_before:**
| `year mod 100` | count | share |
|---:|---:|---:|
| 01 | 98,502 | **54.54 %** |
| 51 | 19,069 | **10.56 %** |
| 71 | 11,015 | 6.10 % |
| 31 | 4,300 | 2.38 % |
| 70 | 3,397 | 1.88 % |
| 50 | 2,612 | 1.45 % |

**not_after:**
| `year mod 100` | count | share |
|---:|---:|---:|
| 00 | 95,782 | **53.03 %** |
| 50 | 24,556 | **13.60 %** |
| 30 | 10,823 | 5.99 % |
| 70 | 6,184 | 3.42 % |
| 79 | 4,570 | 2.53 % |
| 99 | 2,792 | 1.55 % |

Uniform-null share per residue is 1 %. The top six residues for each endpoint
account for ~77 % of all values. The remaining ~23 % is distributed across
the other 94 residues at ~0.2–0.8 % each.

## Reign-boundary signal

13 of 39 well-attested emperor accession (or transition) years show
Holm-Bonferroni-significant clustering (p < 0.05). The strongest:

| Year | Emperor / event | observed | expected | O/E | p_holm |
|---:|---|---:|---:|---:|---:|
| AD 79 | Vesuvius / Titus | 4,552 | 1,041 | **4.37** | 0 |
| AD 251 | Decius dies / Trebonianus Gallus | 1,860 | 492 | **3.78** | 0 |
| AD 270 | Aurelian | 1,786 | 644 | **2.78** | 1.5e-296 |
| 27 BC | Augustus | 1,357 | 520 | **2.61** | 1.1e-202 |
| AD 138 | Antoninus Pius | 1,860 | 796 | **2.34** | 9.3e-225 |
| AD 14 | Tiberius | 2,033 | 886 | **2.29** | 4.7e-236 |
| AD 161 | Marcus Aurelius | 1,584 | 724 | **2.19** | 5.4e-166 |
| AD 117 | Hadrian | 1,855 | 1,043 | 1.78 | 4.5e-112 |
| AD 217 | Macrinus | 1,337 | 870 | 1.54 | 1.6e-47 |
| AD 235 | Maximinus Thrax | 834 | 594 | **1.40** | 2.8e-19 |
| AD 69 | Year of Four Emperors | 1,253 | 920 | 1.36 | 4.1e-24 |
| AD 41 | Claudius | 874 | 725 | 1.21 | 1.3e-06 |
| AD 222 | Severus Alexander | 884 | 785 | 1.13 | 7.4e-03 |

The clear signal is on the **dynastic and major-political-transition** years:
foundational moments (27 BC, AD 14, 79, 117, 138, 161) and Crisis-of-the-Third-Century
transition points (217, 235, 251, 270). Routine intra-dynastic accessions are
not significant. The geo-mean across the full 39-year reign-boundary set is
0.75 (i.e. somewhat *below* baseline overall) — most reign years are *not*
spikes, but a meaningful subset are.

**Note** AD 79 has the strongest reign-boundary clustering — almost certainly
because it is also the year of Vesuvius (Pompeii / Herculaneum), supplying a
distinct dating anchor independent of Titus's accession.

## raw_dating structure

`raw_dating` is non-null for 176,416 of 180,609 rows (97.7 %). The top values
are uniformly of the form "X to Y" where X is a century-inclusive start and Y
a century-inclusive end:

| count | raw_dating | modal (not_before, not_after) |
|---:|---|---|
| 15,863 | `301 to 500` | (301, 500) |
| 13,200 | `101 to 200` | (101, 200) |
| 10,787 | `301 to 400` | (301, 400) |
| 10,590 | `1 to 100` | (1, 100) |
| 6,579 | `1 to 50` | (1, 50) |
| 6,505 | `201 to 300` | (201, 300) |
| 5,483 | `101 to 300` | (101, 300) |
| 4,497 | `1 to 200` | (1, 200) |
| 4,253 | `1 to 300` | (1, 300) |
| 3,266 | `151 to 300` | (151, 300) |
| 3,173 | `1 to 79` | (1, 79) |
| 2,308 | `151 to 250` | (151, 250) |
| 2,183 | `51 to 100` | (51, 100) |
| 2,054 | `171 to 230` | (171, 230) |
| 1,978 | `51 to 200` | (51, 200) |

Modal-pair share is 96–100 % for all the top values — the raw_dating string
literally specifies the endpoint pair that gets recorded. The "Roman inclusive
century" convention is therefore not implicit in how editors round — it is
*explicit* in the data structure. The convention is a property of the dating
encoding, not an analyst's inferred pattern.

A small but interesting nuance: `1 to 79` (n = 3,173) is "1st century AD up to
the Vesuvius eruption" — direct evidence that AD 79 is functioning as a dating
anchor in its own right, supporting the Test 4 finding.

## Implication for the preregistration

### Direct revision needed in the Analysis Pipeline (§3 deconvolution-mixture)

The current text describes the artefact as "century-midpoint inflation" with
`convention_SPA` shape "uniform century slabs by default." That description
is incomplete in two ways:

1. The artefact's mechanism is **interval endpoint rounding** at inclusive-Roman
   boundaries, not midpoint clustering. Midpoint inflation is a derivative.
2. "Uniform century slabs" does not capture the half-century layer that is
   also present (geo-mean O/E ~2.4 combined; 18.2 on `not_after` alone).

### Implication for Decision 14's Bayesian-mixture spec

**The hierarchy is empirically established.** The `convention_SPA` shape in
the Bayesian mixture should not commit to "uniform century slabs only" — that
modelled the data against visible evidence. The flexible-prior alternative
(Option C in (c)-3) is the empirically-grounded choice.

Concretely, the convention-shape prior should support at minimum:

- A century layer with mass at inclusive-Roman starts (year ≡ 1 mod 100) and
  inclusive-Roman ends (year ≡ 0 mod 100).
- A half-century layer with mass at year ≡ 51 mod 100 (starts) and year ≡ 50
  mod 100 (ends).
- A small reign-related layer at well-attested transition years — restricted
  to dynastic and Crisis-era transitions (27 BC, 14, 79, 117, 138, 161, 217,
  235, 251, 270, plus AD 79 as Vesuvius), since intra-dynastic accessions
  generally don't spike.

Sub-century tiers (quarter-century, decade, lustrum) do *not* need a layer —
they are baseline-or-below in the empirical data.

### Implication for the framing in the prereg's Description (Field 2)

The prereg currently states the artefact in terms of the four century-midpoint
observed/expected ratios (22.8 / 41.5 / 18.8 / 39.7 at AD 50 / 150 / 250 / 350).
That framing is true but partial — it understates the artefact by focusing on
its derivative manifestation. A revised framing should describe the artefact
at the *endpoint* level (with the trailing-digit statistic — 54.5 % of
`not_before` values end in 01; 53.0 % of `not_after` values end in 00) and
note that the midpoint inflation is the visible aoristic-mass consequence.

### Implication for (c)-3 — committed

**Option C (Bayesian mixture handles the hierarchy with a flexible
convention-shape prior) is the right call.** Option A (commit to uniform
century slabs only) would be modelling against visible, strong evidence.

## Files

```
outputs/
├── REPORT.md                                                  (this file)
├── run.log                                                    (full stdout)
├── test1-endpoint-frequencies/
│   ├── top50_not_before.csv
│   ├── top50_not_after.csv
│   └── category_rollup.csv
├── test2-hierarchical-oe/
│   ├── per_year_oe_not_before.csv
│   ├── per_year_oe_not_after.csv
│   ├── per_year_oe_combined.csv
│   ├── tier_summary_not_before.csv
│   ├── tier_summary_not_after.csv
│   └── tier_summary_combined.csv
├── test3-trailing-digits/
│   ├── trailing_digits_not_before.csv
│   └── trailing_digits_not_after.csv
├── test4-reign-boundaries/
│   └── reign_boundary_oe.csv
└── test5-convention-text/
    ├── top50_raw_dating.csv
    └── pattern_aggregation.csv
```

## Caveats

- The "expected" baseline is a Gaussian-smoothed version of the observed-counts
  curve. This is a *self-baseline*: any year whose count is high gets a high
  expected too. The smoothing therefore *understates* the per-year O/E ratio
  at spike years (because the spike inflates the local baseline) and
  *overstates* depletion at sub-century tiers (because the baseline includes
  the absorbed spike mass). The reported O/E values are conservative for the
  spike tiers; the true O/E vs a *true* smooth underlying density is larger.
  This is sufficient to establish the hierarchy is real; a more rigorous
  decomposition (a Bayesian mixture fit, which is exactly what Decision 14
  prescribes) will quantify the true contribution.
- The reign-boundary list is curated to ~40 well-attested years from
  Augustus through Constantine. Some other historically significant years
  (e.g. major plagues, edicts, military events) may also act as dating
  anchors — AD 79 is the clearest example since it's the strongest reign-tier
  spike *because* it's also Vesuvius. A broader anchor-year list could be
  considered as a sensitivity check but is not required for the decision in
  hand.
- Pattern regex matching in Test 5 caught essentially all rows (175,893 of
  176,416) under `numeric_year` because `raw_dating` is overwhelmingly numeric
  ranges. A finer-grained text-pattern analysis would need to start from
  EDH-derived narrative date fields (e.g. `dating_clean`) rather than EDCS's
  raw numeric encoding — out of scope for this run.
