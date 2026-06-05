# Template-dictionary empirical scan --- PART 1 (measurement)

**Date:** 2026-06-05  
**Author:** Claude Code (Opus 4.8) on Shawn Ross's brief  
**Status:** read-only measurement. **Commits nothing.** Inputs to the PART-2 threshold/tier decision and the committed `design.json`.

Prerequisite for the real-data H2.1 mixture run (prereg line 202; Decision 20; audit A2; Decision 37 next-session action 1). Enumerates exact-match `[not_before, not_after]` templates so the N >= threshold inclusion rule is pinned from the empirical distribution.

## Corpus

- **Empire frame** (prereg filter): 180,609 inscriptions.
- **Latin frame** (Decision 36; `language=='Latin'` provinces): 109,646 inscriptions.
- **Unique exact templates (empire):** 5,219 (4,820 non-year-precise + 399 year-precise types).
- **Year-precise (`nb==na`) inscriptions (empire):** 8,279 (4.58% of corpus) --- excluded from the convention pool per Decision 20 (stay in `genuine_SPA`).

> **Reconciliation note.** Decision 20's context (line 1671) records "`[1, 100]` 26.3% of corpus". The direct re-scan gives `[1, 100]` = 10,807 (5.98%). The ~26% figure corresponds instead to the century-template *class* collectively, not `[1, 100]` alone --- a stale specific, corrected here.

## Top 25 templates --- empire frame

| Template `[nb, na]` | width | provisional category | N | share | env-overlap |
|---|---|---|---|---|---|
| `[301, 500]` | 200 | multi_century | 15,926 | 8.82% | 0.25 |
| `[101, 200]` | 100 | century | 13,303 | 7.37% | 1.00 |
| `[301, 400]` | 100 | century | 10,847 | 6.01% | 0.50 |
| `[1, 100]` | 100 | century | 10,807 | 5.98% | 1.00 |
| `[1, 50]` | 50 | half_century | 6,572 | 3.64% | 1.00 |
| `[201, 300]` | 100 | century | 6,559 | 3.63% | 1.00 |
| `[101, 300]` | 200 | multi_century | 5,919 | 3.28% | 1.00 |
| `[1, 300]` | 300 | multi_century | 4,856 | 2.69% | 1.00 |
| `[1, 200]` | 200 | multi_century | 4,611 | 2.55% | 1.00 |
| `[151, 300]` | 150 | multi_century | 3,534 | 1.96% | 1.00 |
| `[1, 79]` | 79 | other | 3,202 | 1.77% | 1.00 |
| `[151, 250]` | 100 | other | 2,782 | 1.54% | 1.00 |
| `[71, 130]` | 60 | other | 2,220 | 1.23% | 1.00 |
| `[51, 100]` | 50 | half_century | 2,200 | 1.22% | 1.00 |
| `[171, 230]` | 60 | other | 2,096 | 1.16% | 1.00 |
| `[51, 200]` | 150 | multi_century | 2,064 | 1.14% | 1.00 |
| `[301, 350]` | 50 | half_century | 1,953 | 1.08% | 1.00 |
| `[151, 200]` | 50 | half_century | 1,953 | 1.08% | 1.00 |
| `[101, 150]` | 50 | half_century | 1,938 | 1.07% | 1.00 |
| `[291, 325]` | 35 | other | 1,895 | 1.05% | 1.00 |
| `[51, 150]` | 100 | other | 1,726 | 0.96% | 1.00 |
| `[326, 375]` | 50 | other | 1,636 | 0.91% | 0.50 |
| `[1, 150]` | 150 | multi_century | 1,324 | 0.73% | 1.00 |
| `[201, 250]` | 50 | half_century | 1,309 | 0.72% | 1.00 |
| `[123, 123]` | 1 | year_precise | 1,304 | 0.72% | 1.00 |

`env-overlap` = fraction of the template's width inside [50 BC, AD 350]; wide/late slabs (e.g. `[301, 500]`) deposit convention mass only on their in-envelope portion.

## Provisional category mass (convention pool; year-precise excluded)

| frame | category | #templates | inscriptions | % of convention pool |
|---|---|---|---|---|
| empire | other | 4,328 | 59,762 | 34.68% |
| empire | multi_century | 45 | 43,022 | 24.96% |
| empire | century | 4 | 41,516 | 24.09% |
| empire | half_century | 7 | 17,166 | 9.96% |
| empire | bc_ad_boundary | 365 | 6,139 | 3.56% |
| empire | reign | 71 | 4,725 | 2.74% |

**Decision-relevant finding.** The curated recovery-grid dictionary had only three tiers (century / half_century / reign). The empirical scan shows substantial convention-pool mass in **`multi_century`**, **`bc_ad_boundary`**, and **`other`** --- templates that fit none of the three curated tiers. This is Decision 20's revisit trigger: the tier structure likely needs revision (a multi-century-slab tier; possibly a BC-AD-boundary tier; an explicit `other`/residual-band policy).

## Coverage at candidate N-thresholds

Convention pool = non-year-precise templates. `pct_of_corpus` is of the whole frame; `pct_of_convention_pool` is of non-year-precise inscriptions.

| frame | N>= | #templates | inscriptions | % of corpus | % of convention pool |
|---|---|---|---|---|---|
| empire | 50 | 204 | 153,458 | 84.97% | 89.05% |
| empire | 100 | 126 | 147,833 | 81.85% | 85.78% |
| empire | 200 | 80 | 141,231 | 78.20% | 81.95% |
| empire | 500 | 48 | 131,404 | 72.76% | 76.25% |
| empire | 1000 | 31 | 119,419 | 66.12% | 69.30% |

## High-frequency `other` templates (empire; N >= 200, category=other)

These are the templates that do not fit century/half-century/reign --- the ones the PART-2 tier decision must place or exclude.

| Template `[nb, na]` | width | N | share | env-overlap |
|---|---|---|---|---|
| `[1, 79]` | 79 | 3,202 | 1.77% | 1.00 |
| `[151, 250]` | 100 | 2,782 | 1.54% | 1.00 |
| `[71, 130]` | 60 | 2,220 | 1.23% | 1.00 |
| `[171, 230]` | 60 | 2,096 | 1.16% | 1.00 |
| `[291, 325]` | 35 | 1,895 | 1.05% | 1.00 |
| `[51, 150]` | 100 | 1,726 | 0.96% | 1.00 |
| `[326, 375]` | 50 | 1,636 | 0.91% | 0.50 |
| `[-50, -1]` | 50 | 1,116 | 0.62% | 1.00 |
| `[31, 70]` | 40 | 1,041 | 0.58% | 1.00 |
| `[171, 300]` | 130 | 1,018 | 0.56% | 1.00 |
| `[71, 200]` | 130 | 997 | 0.55% | 1.00 |
| `[43, 70]` | 28 | 950 | 0.53% | 1.00 |
| `[131, 170]` | 40 | 865 | 0.48% | 1.00 |
| `[1, 30]` | 30 | 785 | 0.43% | 1.00 |
| `[71, 100]` | 30 | 777 | 0.43% | 1.00 |
| `[71, 150]` | 80 | 757 | 0.42% | 1.00 |
| `[-100, -1]` | 100 | 691 | 0.38% | 0.50 |
| `[151, 230]` | 80 | 680 | 0.38% | 1.00 |
| `[171, 250]` | 80 | 645 | 0.36% | 1.00 |
| `[1, 70]` | 70 | 624 | 0.35% | 1.00 |
| `[171, 200]` | 30 | 590 | 0.33% | 1.00 |
| `[101, 230]` | 130 | 539 | 0.30% | 1.00 |
| `[101, 130]` | 30 | 464 | 0.26% | 1.00 |
| `[131, 200]` | 70 | 464 | 0.26% | 1.00 |
| `[122, 300]` | 179 | 455 | 0.25% | 1.00 |
| `[71, 300]` | 230 | 447 | 0.25% | 1.00 |
| `[201, 230]` | 30 | 373 | 0.21% | 1.00 |
| `[201, 270]` | 70 | 373 | 0.21% | 1.00 |
| `[-30, -1]` | 30 | 368 | 0.20% | 1.00 |
| `[222, 235]` | 14 | 352 | 0.19% | 1.00 |
| `[151, 270]` | 120 | 347 | 0.19% | 1.00 |
| `[107, 275]` | 169 | 320 | 0.18% | 1.00 |
| `[-70, -31]` | 40 | 309 | 0.17% | 0.50 |
| `[31, 100]` | 70 | 297 | 0.16% | 1.00 |
| `[122, 138]` | 17 | 291 | 0.16% | 1.00 |
| `[69, 86]` | 18 | 271 | 0.15% | 1.00 |
| `[51, 130]` | 80 | 265 | 0.15% | 1.00 |
| `[231, 270]` | 40 | 261 | 0.14% | 1.00 |
| `[14, 50]` | 37 | 226 | 0.13% | 1.00 |
| `[78, 79]` | 2 | 219 | 0.12% | 1.00 |
| `[1, 130]` | 130 | 217 | 0.12% | 1.00 |
| `[211, 222]` | 12 | 216 | 0.12% | 1.00 |
| `[293, 305]` | 13 | 205 | 0.11% | 1.00 |
| `[171, 270]` | 100 | 200 | 0.11% | 1.00 |
| `[251, 350]` | 100 | 200 | 0.11% | 1.00 |

## Outputs

- `tables/templates-empire.csv` --- full ranked template list (empire).
- `tables/templates-latin.csv` --- full ranked template list (Latin).
- `tables/threshold-coverage.csv` --- coverage at candidate thresholds.
- `tables/category-mass.csv` --- convention-pool mass per category.

## Next (PART 2 --- needs Shawn sign-off; commits the artefact)

1. Choose the N-threshold from this distribution.
2. Decide the tier structure (resolve `multi_century` / `bc_ad_boundary` / `other`).
3. Write + commit `design.json` (`template_intervals_by_tier`) the mixture consumes.