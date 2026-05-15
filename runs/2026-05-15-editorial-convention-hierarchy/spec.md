---
title: "Editorial-convention-hierarchy diagnostic — five tests"
date: 2026-05-15
author: "Shawn Ross (with Claude Code, Opus 4.7, 1M context)"
status: spec
related-decisions: "preregistration-draft.md (c)-3 — keep or drop the hierarchical convention_SPA option"
---

# Editorial-convention-hierarchy diagnostic

## Why

The preregistration's deconvolution-mixture model specifies a `convention_SPA`
shape defaulting to uniform century slabs, with a contingent shift to a weighted
hierarchical shape (century > half-century > quarter-century > reign-boundary) if
an "editorial-convention-hierarchy test" confirms the hierarchy on a 14-boundary
sample. The test was never defined; "confirms" and "inconclusive" had no decision
rule; the 14 boundaries were not enumerated.

The 2026-04-23 descriptive-stats run quantified the century-midpoint editorial
artefact (observed/expected ratios 22.8× / 41.5× / 18.8× / 39.7× at AD 50 / 150 /
250 / 350) but did not look at any sub-century structure. A targeted audit on
2026-05-15 of the 2023-09 and 2026-04 exploratory notebooks plus the
descriptive-stats outputs confirmed no systematic sub-century analysis has been
done — yet the audit also surfaced incidental evidence that the hierarchy is real
and large: AD 100 has mc_ratio 19.7 (count 8,845), AD 125 has 8.1, AD 175 has 7.4,
AD 110/115/135/165/185/190 sit between 1.4 and 2.6 — a quasi-quinquennial/decadal
pattern visible in the data but never extracted.

This run resolves the question with five concrete tests. The results pin the
structure of the editorial-convention hierarchy (or rule it out) and inform the
specification of the `convention_SPA` shape prior in the Bayesian mixture model
(Decision 14).

## Data

- **Source:** `archive/data-2026-04-22/LIRE_v3-0.parquet` (LIRE v3.0; Kaše,
  Heřmánková & Sobotková 2023, Zenodo DOI 10.5281/zenodo.8147298; 182,853 rows).
- **Filter (matches preregistration §1):** `is_geotemporal := Latitude IS NOT
  NULL AND Longitude IS NOT NULL AND not_before IS NOT NULL AND not_after IS NOT
  NULL AND not_before ≤ not_after`; `is_within_RE := province IS NOT NULL`;
  date-interval overlap with [50 BC, AD 350]. Yields 180,609 rows (≈ 98.8 % of
  the pre-filter total). The filter has been previously verified to reproduce
  the prereg's row count exactly.

## Tests

### Test 1 — Top-N endpoint frequencies (direct read)

For each of `not_before` and `not_after`, compute `value_counts()` over the
filtered corpus and report the top 50 most-frequent values. For each top entry,
tag the year by category: century-boundary (year ≡ 0 mod 100); century-midpoint
(year ≡ 50 mod 100); quarter-century (year ≡ 25 or 75 mod 100); decade (year ≡ 0
mod 10, not already a century-boundary); lustrum (year ≡ 0 or 5 mod 10, not
already a decade); reign-related (in the well-attested emperor accession year
list — see Test 4); other.

A dominance of round-number tags on the leaderboard = hierarchical editorial
convention is real and structured.

### Test 2 — Hierarchical observed/expected by tier

For each boundary tier, compute observed-vs-expected ratios at every boundary
year in the tier. Compare geometric-mean O/E across tiers; rank.

**Tiers:**
- Century-boundary: -50, 50, 150, 250, 350 (4 years in envelope — note: -50 and
  50 in the envelope's notional centuries, but we use the four prereg years).
  Actually use the prereg's "century-midpoint" set AD 50, 150, 250, 350 as the
  "century" tier here.
- Century-mark: AD 0, 100, 200, 300 (half-century complement).
- Quarter-century: AD 25, 75, 125, 175, 225, 275, 325 (years ≡ 25 or 75 mod 100).
- Decade: years ≡ 0 mod 10 in [-50, 350], excluding centuries and half-centuries.
- Lustrum: years ≡ 5 mod 10 in [-50, 350], excluding everything above.
- Reign-related: from the Test 4 emperor-accession year list.

**Observed at year Y:** `(not_before == Y).sum() + (not_after == Y).sum()` —
endpoint clustering, the direct measure of editorial rounding.

**Expected at year Y:** the smoothed baseline from a Gaussian-kernel smooth of
the (not_before + not_after) frequency curve, evaluated at Y. Bandwidth chosen
to remove sharp boundary spikes but preserve real underlying density variation
(target bandwidth ~10–20 years; report sensitivity at 5 / 10 / 20 / 30).

**O/E ratio per year + per tier:**
- Per-year `O/E = observed / expected` at each boundary year.
- Per-tier: geometric mean of per-year O/E within the tier.
- Per-year significance: Holm-Bonferroni-adjusted *p* from a Poisson test
  (`scipy.stats.poisson.sf(observed - 1, expected)`) within each tier.
- Tier ranking: report tiers by geometric mean O/E descending. If the ranking
  is century > half-century > quarter-century > decade > lustrum, the
  hierarchy is monotonic.

### Test 3 — Trailing-two-digit histogram

For each of `not_before` and `not_after` over the filtered corpus, compute
`year mod 100` and histogram across all 100 possible values. Report the top-20
most-frequent two-digit residues.

Under a flat null each two-digit residue has ~ 1 % mass. Heavy concentration at
specific residues = explicit rounding-tier signal. Predicted hits if the
hierarchy is real: 00 and 50 (centuries + half-centuries); 25 and 75
(quarter-centuries); residues ending in 0 (decades); maybe 5 (lustra).

### Test 4 — Reign-boundary specific test

Compile a list of well-attested emperor accession years (Augustus 27 BC through
the early 4th century). For each, compute O/E (same observed/expected definition
as Test 2). Aggregate by Holm-Bonferroni across the reign-boundary family. The
existing project-internal seed list (`[-14, 27, 97, 192, 193, 212, 235]` from
`profile_lire_v30.py`) is extended to a full reign-boundary set.

Emperor accession years (selected; standard reference):

- Augustus 27 BC (encoded as `year = -26` if 27 BC = -26 in the project's
  envelope convention, or -27; script should handle this carefully). Actually
  the project uses years where BC dates are negative, so 27 BC is year -26 or
  -27. Confirm against the data — the envelope starts at -50, so verify with a
  filter for year = -27 / -26.
- Tiberius AD 14
- Caligula AD 37
- Claudius AD 41
- Nero AD 54
- Galba AD 68; Otho/Vitellius/Vespasian AD 69
- Titus AD 79
- Domitian AD 81
- Nerva AD 96
- Trajan AD 98
- Hadrian AD 117
- Antoninus Pius AD 138
- Marcus Aurelius AD 161 (with Lucius Verus)
- Commodus AD 180
- Pertinax / Didius Julianus / Septimius Severus AD 193
- Caracalla AD 198 (co-) / 211 (sole)
- Macrinus AD 217
- Elagabalus AD 218
- Severus Alexander AD 222
- Maximinus Thrax AD 235
- Gordian I/II / Pupienus & Balbinus / Gordian III AD 238
- Philip the Arab AD 244
- Decius AD 249
- Trebonianus Gallus AD 251
- Aemilianus AD 253
- Valerian / Gallienus AD 253
- Claudius II Gothicus AD 268
- Aurelian AD 270
- Tacitus AD 275
- Probus AD 276
- Carus AD 282
- Diocletian AD 284
- Constantius I / Galerius AD 305
- Constantine I AD 306 / 312 / 324
- Constantius II / Constans / Constantine II AD 337

Take the *first accession year* for each reign as the canonical boundary.

### Test 5 — Convention-text labelled subset

Examine the `raw_dating` field (EDCS, "raw dates without any formatting") to
understand how text-described dates resolve to (not_before, not_after) pairs.

1. Compute `value_counts()` on `raw_dating`; report the top 50 most-frequent
   distinct values, each with: count, the *modal* (not_before, not_after) pair,
   and the count of inscriptions with that modal pair as a fraction of the
   raw_dating value's total.
2. For a curated set of patterns (regex on raw_dating), report the
   `(not_before, not_after)` pair distribution:
   - "saec\\." or "century" (likely century-coded)
   - "init|inc|princ" (early-X-century markers)
   - "fin|exit" (late-X-century markers)
   - "med" (mid-X-century markers)
   - "imp\\.|reign of" (reign-anchored)
3. For the top-50 distinct raw_dating values, list verbatim alongside the modal
   (not_before, not_after) pair.

Output reveals whether text labels predominantly resolve to round-number
endpoints (confirming hierarchical convention is text-driven) or to mixed
endpoints (suggesting the rounding is downstream of more granular dating).

## Outputs

`outputs/`:

- `REPORT.md` — consolidated narrative report with headline findings per test,
  the tier-ranking from Test 2, and the implication for the `convention_SPA`
  shape prior in the Bayesian mixture.
- `test1-endpoint-frequencies/` — top-50 CSVs for `not_before` and `not_after`,
  per-year category tags.
- `test2-hierarchical-oe/` — per-year O/E table; per-tier geometric-mean
  summary; sensitivity table across smoothing bandwidths.
- `test3-trailing-digits/` — histograms for `not_before` and `not_after` mod
  100.
- `test4-reign-boundaries/` — per-reign O/E with Holm-adjusted *p*-values.
- `test5-convention-text/` — top-50 raw_dating values + modal endpoint pairs;
  regex-pattern aggregations.

## Implication for the preregistration

Three outcomes possible:

- **Strong hierarchy** (multiple tiers show O/E significantly > 1, monotonically
  decreasing) → `convention_SPA` shape in the Bayesian mixture (Decision 14)
  takes a flexible prior spanning uniform-century to weighted-hierarchical,
  with the data adjudicating. Option C in (c)-3.
- **Centuries only** (only the century-midpoint tier shows significant O/E;
  other tiers are flat) → `convention_SPA` shape commits to uniform century
  slabs, no hierarchical option. Option A in (c)-3.
- **Mixed / partial hierarchy** (some sub-century tiers significant, no clean
  monotonic ranking) → the structure is the answer: pre-specify the
  `convention_SPA` shape with only the tiers that empirically signal, drop the
  rest.
