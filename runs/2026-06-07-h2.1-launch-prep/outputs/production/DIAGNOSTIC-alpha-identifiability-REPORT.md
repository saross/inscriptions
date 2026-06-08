# H2.1 diagnostic — α identifiability for the unexpected-α units

**Date:** 2026-06-08 (overnight, on Shawn's request) · **Author:** Claude Code (Opus 4.8).
**Trigger:** the primary run returned surprising convention fractions — several
provinces at α ≈ 0.00 (Dacia, Britannia, Pompeii) and others very high (Noricum
0.88, Latin-aggregate 0.81). Shawn asked whether such low/high α are *plausible*
given the actual inscription date ranges. This report answers that.

## TL;DR verdict

α is **not** "the fraction of round-period-dated inscriptions". It is *how much of
the unit's observed SPA matches the **shape** of the shared empire/Latin convention
basis* (broad, centroid ≈ 144 AD, spread across the envelope). Three findings:

1. **Pompeii α ≈ 0.001 is CORRECT** — genuine precision (5 % round-period mass,
   dated `[1,79]`, pre-eruption). The method passing this unprompted is a validation.
2. **~10 units UNDER-ATTRIBUTE convention** — they carry substantial round-period
   dating *concentrated in a narrow window* (mostly their frontier/military
   occupation period, AD ~100–300) where their genuine signal also lives. The
   smooth genuine component absorbs it and α collapses. Their "corrected genuine
   SPA" (the H3b hand-off) still contains convention leaking through as genuine.
3. **The convention/genuine split is genuinely UNDER-IDENTIFIED for these units.**
   It is not a tuning bug: with a per-unit basis the same units over-attribute
   (Salona → α 0.995). The temporal distribution alone cannot separate
   "convention concentrated in AD 100–300" from "genuine signal concentrated in
   AD 100–300". The shared-basis homogeneity assumption (Decision 38 / Amendment
   03 §3) breaks for **period-concentrated** units.

This **refines, not refutes**, the run: it identifies *where* the correction is
trustworthy (broad-convention units — the controls are rock-stable) and where it
is not (period-concentrated units). The risk is in the **unflagged low-α
"reportable" units**, NOT the caveated high-α ones.

## Method (read-only descriptive + one cheap diagnostic refit)

- **(A) Descriptive** (`code/diag-probe.py`): per-unit aoristic-mass family
  composition (Tight / F1_round / F3_periodic / F2_Other / Big), date-range widths,
  and the temporal centroid of the round-period (F1+F3) mass vs the shared basis.
- **(B) Screen** — the gap `F1+F3-family-mass-fraction − fitted α` across all 28.
- **(C) Identifiability test** (`code/diag-refit.py`): refit the SAME observed y
  under a PER-UNIT basis (the unit's own 3-tier round-period SPA). A large α swing
  ⇒ basis-dependent ⇒ under-identified. A stable α (control) ⇒ identified.

## Results

**Shared basis location:** empire centroid 166 AD (sd 102 y); Latin 144 AD (sd 86 y).

**(A) The two regimes (selected units):**

| unit | α | F1+F3 mass-frac | round-period centroid / % in AD 100–275 | reading |
|---|---|---|---|---|
| Pompeii | 0.001 | 0.05 | 38 AD / 0.01 | genuine precision — α correct |
| Moesia inferior | 0.050 | 0.60 | 193 AD / 0.84 | convention-dominated, period-concentrated |
| Britannia | 0.002 | 0.31 | 182 AD / 0.66 | round-slabs in occupation window |
| Dacia | 0.001 | 0.15 | 193 AD / 0.93 | mostly Big/irregular in AD 106–271 |
| Salona | 0.538 | 0.86 | 201 AD / 0.67 | high frac, late-shifted |
| Noricum | 0.880 | 0.75 | 137 AD / 0.63 | broad slabs (`[1,300]`) — match basis |
| latin-aggregate | 0.811 | 0.59 | 139 AD / 0.58 | matches basis (built from it) |

**(B) Screen — gap `F1+F3-frac − α`, units flagged at gap > 0.25 ∧ F1+F3-frac > 0.30 (10 units):**
Moesia inferior (+0.55), Samnium (+0.52), Pannonia inferior (+0.49), Numidia
(+0.37), Venetia et Histria (+0.36), Salona (+0.32), Britannia (+0.31), Umbria
(+0.30), Ostia (+0.30), Dacia (+0.15, borderline). **Eight of these are currently
"reportable" (unflagged); only Moesia inferior is in the caveated tier.**
Negative-gap units (α ≥ raw round-period — convention matches the broad basis):
latin-aggregate, Noricum, Latium et Campania, Pannonia superior, empire-aggregate.

**(C) Identifiability refit — the decisive test:**

| unit | α (shared basis) | α (per-unit basis) | swing |
|---|---|---|---|
| Moesia inferior | 0.050 | 0.870 | **+0.82** |
| Britannia | 0.002 | 0.793 | **+0.79** |
| Pannonia inferior | 0.147 | 0.751 | **+0.61** |
| Samnium | 0.272 | 0.860 | **+0.59** |
| Salona | 0.538 | 0.995 | **+0.46** |
| Ostia | 0.335 | 0.775 | **+0.44** |
| Venetia et Histria | 0.452 | 0.809 | +0.36 |
| Numidia | 0.166 | 0.515 | +0.35 |
| Dacia | 0.001 | 0.344 | +0.34 |
| Umbria | 0.429 | 0.700 | +0.27 |
| **Noricum** (control) | 0.880 | 0.829 | **−0.05** |
| **latin-aggregate** (control) | 0.811 | 0.815 | **+0.00** |
| **Latium et Campania** (control) | 0.672 | 0.621 | **−0.05** |

The controls are stable (|swing| ≤ 0.05); every flagged unit swings up +0.27 to
+0.82. The screen gap predicts the swing. **α is basis-dependent (under-identified)
for the flagged units and identified for the controls.**

## Interpretation

- The flagged units are largely **frontier/military provinces** (Moesia inferior,
  Pannonia inferior, Numidia, Britannia, Dacia) plus **ports / regional centres**
  (Salona, Ostia) and a few **Italian regions** (Samnium, Venetia et Histria,
  Umbria). The common cause is **temporally-concentrated epigraphy**: their round-
  period datings (`[101,300]`, `[151,300]`, …) cluster in the same window as their
  genuine signal, so the two are confounded and α is not pinned by the data.
- For these units, the **shared basis is "wrong low"** (under-attributes
  convention) and a **per-unit basis is "wrong high"** (Salona → 0.995 absorbs
  genuine signal — the exact failure the shared-basis choice was meant to avoid).
  The honest answer is a **range**, not a point.
- This is **larger than** the documented α-diagnostic imprecision (Amendment 01's
  shape-conditioned ±0.18 LoA): Moesia inferior's range is ~0.82 wide. It is a
  structural identifiability limit specific to period-concentrated units under a
  fixed shared basis, newly characterised here.
- The recovery grid foreshadowed this: peaked/concentrated genuine signals
  (`regnal_cluster`) were its hard corner, and α was demoted to a diagnostic for
  exactly this reason. The production data shows the real-world manifestation.

## Implications

- **The α ≤ 0.70 tiering does not catch this.** The at-risk units are low-α
  "reportable" ones. A second flag is needed.
- **The H3b hand-off `corrected_genuine_spa` is unreliable for the ~10 flagged
  units** — convention leaks through as genuine, so their corrected curve ≈ raw SPA
  with spurious structure.
- The **identifiable units** (controls + small-gap units, e.g. Latium, the
  aggregates, Noricum, Etruria, Apulia, Hispania citerior, Germania superior,
  Mogontiacum, Pompeii) are trustworthy.

## Recommendations (for the morning — your call, not actioned)

1. **Add an identifiability flag to the tiering** — flag units with a large
   `F1+F3-frac − α` gap (screen) confirmed by a basis-swing > ~0.20. Promote the
   ~10 flagged units to a `caveated-underidentified` tier.
2. **Report α as a two-bound sensitivity range** for flagged units
   (shared-basis = lower bound on convention; per-unit-basis = upper bound),
   rather than a point. Identifiable units keep a tight α.
3. **Restrict confirmatory H3b claims to identifiable units**; treat the flagged
   units as exploratory, or carry the convention/genuine uncertainty into H3b.
4. **Disclose as a post-hoc finding** — the shared-basis homogeneity limit for
   period-concentrated units is now quantified; an honest prereg note (not an
   emergency; the preregistered method stands where identifiable).
5. *Research direction (not a quick fix):* a period-aware / hierarchical basis that
   lets the convention location vary by region without absorbing the genuine
   signal — but this needs design + its own recovery validation; do not bolt it on.

## Artefacts

- `code/diag-probe.py` (descriptive), `code/diag-refit.py` (identifiability test).
- `outputs/production/diag-refit.json` (the swing table).
- Production fits: `outputs/production/units/`, `SUMMARY.md`.
