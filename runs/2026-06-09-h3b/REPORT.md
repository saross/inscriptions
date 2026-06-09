# H3b deviation-detection — DRAFT results

# ⚠ DRAFT — FOR REVIEW ⚠

**Nothing in this report is confirmatory.** It is a draft pass produced to exercise
the H3b harness and surface the design decisions a human must adjudicate. The open
questions in `h3b-spec.md` §10 (and recapped in §7 below) gate any confirmatory
reading. Do not cite these numbers as results.

**Date:** 2026-06-09. **Author:** Claude Code (Opus 4.8, 1M context) on Shawn
Ross's brief. **Run:** `runs/2026-06-09-h3b/`. **Master seed:** 20260609.
**MC replicates:** 1000. **UK/Australian English; Oxford comma.**

---

## 1. What was run

H3b = pre-specified **exploratory** temporal deviation-detection (preregistration
§4 H3b; Decision 15). For each H2.1 unit we tested its **posterior-median corrected
genuine SPA** (the H2.1 hand-off, `corrected_genuine_spa`, scaled to `n_eff`
counts) against a featureless-null permutation envelope (Timpson et al. 2014
global-*p* test), under two null families:

- **Exponential (primary by Timpson convention)** — forward-fit in true-date space
  on the unit's raw `[not_before, not_after]` intervals (the documented
  false-positive fix; prereg lines 153, 309).
- **CPL-3 (secondary; the rise-and-fall-capable null)** — continuous
  piecewise-linear with 3 fitted knots (prereg line 317).

We read the result at the two pre-specified probe windows — **Antonine** (AD
165–180) and **Crisis of the Third Century** (AD 235–284 inclusive) — and computed
a **Holm–Bonferroni-adjusted *p*** across the family **as a descriptive
multiplicity diagnostic only** (the prereg forms no confirmatory Holm family;
§7/OQ-1).

Machinery is **reused, not reimplemented**: the forward-fit + envelope test from
`runs/2026-04-25-h1-simulation/code/{forward_fit,primitives}.py`; the per-unit
corpus + corrected-SPA hand-off from `runs/2026-06-07-h2.1-launch-prep/`.

---

## 2. The identifiable-unit set (confirmatory-eligible)

The confirmatory H3b set is restricted to units whose H2.1 convention correction is
reliable. Operative flag (prereg-note line 53; brief): `gap =
f1f3_family_mass_fraction − alpha_median`; **identifiable ⇔ gap < 0.20**. Computed
from the 29 production unit JSONs (`code/compute_identifiability.py`;
`outputs/identifiability-split.json`).

**IDENTIFIABLE — 17 units (confirmatory-eligible):** empire-aggregate,
latin-aggregate, Italia (excl. Rome), Latium et Campania / Regio I, Dalmatia,
Hispania citerior, Germania superior, Dacia, Pompeii, Pannonia superior, Apulia et
Calabria / Regio II, Africa proconsularis, Noricum, Baetica, Etruria / Regio VII,
Mogontiacum, Transpadana / Regio XI.

**FLAGGED under-identified — 12 units (EXPLORATORY-only):** Moesia inferior, Samnium
/ Regio IV, Pannonia inferior, Numidia, Venetia et Histria / Regio X, Salona,
Britannia, Umbria / Regio VI, Ostia, Aquileia, Germania inferior, Lusitania.

> **⚠ Criterion conflict (OQ-2).** The committed `identifiability-table.json` uses a
> *different* rule (basis-swing > 0.2) marking only **9** units identifiable. The
> gap rule (used here, per the brief) matches the prereg-note's own narrative
> example set; the swing rule is stricter. Seven of my 17 (Dalmatia, Hispania
> citerior, Dacia, Africa proconsularis, Baetica, Etruria, Transpadana) plus Italia
> flip under the swing rule. **The human must confirm which rule is canonical.**
> Italia is gap-identifiable (0.089) and the prereg-note §4 presents Italia precisely
> as the identifiability *fix* for the Italian regiones.

---

## 3. Headline (DRAFT)

**The exponential null is saturated and uninformative at these corpus sizes.**
Under the exp null **every unit returns global *p* = 0.000** (e.g. empire: 79/80
bins out-of-envelope). The reason is structural, not a bug: the Roman epigraphic
SPA is a strong **rise-and-fall** curve, and a single-rate exponential cannot
represent it, so essentially the whole curve "deviates". The exp null confirms only
that the corpus is *not* featureless-exponential — it **cannot localise events**.
**Report the exp result as a saturation finding; read deviations off the CPL-3
null** (which can absorb the rise-and-fall trend and so isolate genuine departures).
See OQ-A.

**Under the CPL-3 null (17 identifiable units):**

- **15/17** show a global departure at raw *p* < 0.05; **14/17** survive the
  (descriptive) Holm adjustment. The two non-significant identifiable units are
  **Apulia et Calabria / Regio II** (*p* = 0.515) and **Transpadana / Regio XI**
  (*p* = 0.566); **Baetica** (*p* = 0.030 raw, Holm 0.090) is significant raw but
  not Holm.
- **Antonine window (AD 165–180):** out-of-envelope in **7/17** identifiable units —
  empire-aggregate, latin-aggregate, Germania superior, Dacia, Pannonia superior,
  Africa proconsularis, Noricum.
- **Crisis window (AD 235–284):** out-of-envelope in **9/17** — empire-aggregate,
  latin-aggregate, Latium et Campania, Dalmatia, Germania superior, Dacia, Africa
  proconsularis, Noricum, Italia (excl. Rome).

### Per-unit table — identifiable units, CPL-3 null

| unit | N_eff | global *p* | Holm *p* | Antonine | Crisis |
|---|---:|---:|---:|---|---|
| empire-aggregate | 151,361 | 0.000 | 0.000 | **deficit** | mixed |
| latin-aggregate | 101,066 | 0.000 | 0.000 | **deficit** | mixed |
| Italia (excl. Rome) | 40,499 | 0.000 | 0.000 | — | **deficit** |
| Latium et Campania / Regio I | 17,037 | 0.000 | 0.000 | — | **deficit** |
| Dalmatia | 6,325 | 0.000 | 0.000 | — | **surplus** |
| Hispania citerior | 6,011 | 0.000 | 0.000 | — | — |
| Germania superior | 5,570 | 0.000 | 0.000 | **surplus** | mixed |
| Dacia | 4,717 | 0.000 | 0.000 | **deficit** | mixed |
| Pompeii | 4,247 | 0.000 | 0.000 | — | — |
| Pannonia superior | 4,174 | 0.000 | 0.000 | **deficit** | — |
| Apulia et Calabria / Regio II | 3,013 | 0.515 | 1.000 | — | — |
| Africa proconsularis | 2,967 | 0.000 | 0.000 | **deficit** | mixed |
| Noricum | 2,600 | 0.000 | 0.000 | **deficit** | **deficit** |
| Baetica | 2,449 | 0.030 | 0.090 | — | — |
| Etruria / Regio VII | 2,426 | 0.011 | 0.044 | — | — |
| Mogontiacum | 2,325 | 0.000 | 0.000 | — | — |
| Transpadana / Regio XI | 2,200 | 0.566 | 1.000 | — | — |

(Holm computed across the 34-test identifiable family — 17 units × {exp, cpl3} — as
a descriptive multiplicity diagnostic. The exp half of the family is all *p* = 0.000;
this drags the Holm correction. The Holm column above is for the CPL-3 entries. Full
per-test values in `outputs/deviations-table.csv`.)

Flagged (exploratory-only) units are tabulated separately in
`outputs/deviations-table.csv`; under CPL-3 several are non-significant (e.g. Samnium
*p* = 1.000, Pannonia inferior *p* = 1.000, Aquileia *p* = 0.801, Moesia inferior
*p* = 0.700) — consistent with their corrected SPAs being unreliable (convention
leaking through, so the curve sits closer to the convention-shaped null).

---

## 4. The two replication probes (DRAFT)

### 4.1 Antonine probe (AD 165–180)

Both aggregates show an **out-of-envelope deficit centred at AD ~168** under **both**
nulls — directionally consistent with the Antonine Plague mortality signal and
Duncan-Jones (2018)'s abrupt post-AD-167 cessation of military diplomas:

| level | null | window departure | direction | descriptive bracket | peak yr |
|---|---|---|---|---|---|
| empire-aggregate | exp | out | deficit | ≥ 20% deficit | 167.5 |
| empire-aggregate | CPL-3 | out | deficit | ≥ 20% deficit | 167.5 |
| latin-aggregate | exp | out | deficit | ≥ 50% deficit | 167.5 |
| latin-aggregate | CPL-3 | out | deficit | ≥ 50% deficit | 167.5 |

- **Asclepius-cult subset** and **military-administration subset** (the two
  literature-replication subsets the prereg names): **NOT BUILT.** They require
  per-subset deconvolution (Decision 34/36 — empire α is not imposed on subsets),
  per-subset Phase-1 reachability, and a LIRE membership rule (no clean Asclepius /
  military-diploma flag exists; only `inscr_type`, `keywords_term`,
  `type_of_inscription_*`). Deferred — see OQ-6.
- No magnitude is pre-committed (prereg line 101): Glomb et al. 2022 found a null at
  small N; Duncan-Jones 2018 an abrupt cessation. The draft direction (deficit) sides
  with Duncan-Jones, but this is descriptive and unconfirmed.

### 4.2 Crisis-of-the-Third-Century probe (AD 235–284)

The **Western-Empire-provincial subset** (`province_language == 'Latin' AND province
!= 'Roma'`) **is the `latin-aggregate` unit** (Rome excluded by construction;
Decision 36) — so both named subsets are directly runnable, no new fit required.

| level | null | window departure | direction | descriptive bracket | peak yr |
|---|---|---|---|---|---|
| empire-aggregate | exp | out | deficit | ≥ 50% deficit | 282.5 |
| empire-aggregate | CPL-3 | out | mixed | ≥ 20% deficit | 262.5 |
| latin-aggregate (Western-Empire) | exp | out | mixed | ≥ 50% deficit | 282.5 |
| latin-aggregate (Western-Empire) | CPL-3 | out | mixed | ≥ 50% surplus | 257.5 |

The Crisis window is messier (mixed direction; the CPL-3 and exp nulls disagree on
the sign of the extreme bin) — consistent with the Crisis being a diffuse
multi-decade decline rather than a sharp event, and with the late-corpus
convention-domination caveat (Obs 69: AD ~142–347 is `p_conv`-dominated even in the
corrected curve). Treat the Crisis result as the weaker of the two probes.

---

## 5. Raw-vs-corrected follow-up (launch-spec §8)

For the identifiable units under the exp null, the raw and corrected SPAs give the
**same global verdict** (both saturate, *p* = 0.000) — unsurprising given exp
saturation. At the probe windows the corrected curve occasionally *loses* an
out-of-envelope flag the raw curve has (e.g. Germania superior: raw flags the
Antonine window, corrected does not) — directionally consistent with the launch-spec
§8 prediction that "the GRW attenuates sharp peaks, so the corrected may be
conservative at the Antonine probe". Full table: `outputs/raw-vs-corrected.json`.
The more informative raw-vs-corrected comparison is under CPL-3 and is a
pre-confirmatory build item (currently only the exp follow-up is run).

---

## 6. Files

- `h3b-spec.md` — the build-ready design spec (method, prereg citations, OQs).
- `code/compute_identifiability.py` — the gap-based identifiable split.
- `code/h3b_lib.py` — the harness library (reuses Phase-1 + H2.1 code).
- `code/run_h3b.py` — the driver.
- `code/test_h3b_lib.py` — logic unit tests (all pass).
- `outputs/identifiability-split.json` — per-unit gap + swing flags.
- `outputs/deviations.json` — full per (unit × null) result with envelopes.
- `outputs/deviations-table.csv` — flat tabulation (all 58 tests).
- `outputs/replication-antonine.json`, `outputs/replication-crisis.json`.
- `outputs/raw-vs-corrected.json`.

---

## 7. OPEN QUESTIONS — confirm before any confirmatory reading

These recap `h3b-spec.md` §10 plus the run-surfaced item OQ-A.

- **OQ-A (run-surfaced) — exponential null is saturated.** Under the exp null every
  unit is universally significant (the SPA is not featureless-exponential). The
  exp result cannot localise events. **Confirm** that the **CPL-3 null is the
  operative deviation-detector for H3b on real data**, with exp reported as a
  saturation/sanity finding — or specify a different primary null. (The prereg calls
  exp "primary by Timpson convention" but Phase 1 was a *power* study where the
  injected effect sat on a featureless base; on the real rise-and-fall corpus that
  convention inverts.)
- **OQ-1 — Confirmatory status / Holm family.** Prereg + Decision 15: H3b is
  exploratory, **no** Holm-corrected confirmatory family. Backlog/continuity still
  say "Holm-Bonferroni across 6/12 cells" (stale). This run reports Holm
  descriptively only. Confirm status.
- **OQ-2 — Identifiability criterion** (gap → 17 vs swing → 9). Confirm canonical
  rule; it changes the confirmatory set by 8 units.
- **OQ-3 — Reachability edge cases.** Lusitania (N=1,578) is below the province
  cpl-3-Gaussian 1,618 threshold; confirm the binding Phase-1 threshold.
- **OQ-4 — CPL forward sampler.** The exp null is forward-fit; CPL-3 uses the older
  smeared-fit Poisson sampler. Build a forward CPL sampler before confirmatory?
- **OQ-5 — Observed-signal scaling.** We scale the corrected *distribution* by
  `n_eff` to counts and test against a null fit to the *raw* intervals. Confirm this
  construction (the prereg does not pin it for the corrected input).
- **OQ-6 — Antonine subsets.** Asclepius-cult + military-administration subsets are
  NOT built (need per-subset deconvolution + reachability + LIRE membership rules).
  Confirm deferral and supply the membership definitions.
- **OQ-7 — Test direction.** Two-sided envelope (used here) vs one-sided deficit at
  the historically-deficit probes. Confirm.
- **OQ-8 — Per-unit scope.** The prereg names empire + the Western-Empire subset for
  the probes. We additionally scan every identifiable unit. Confirm whether per-unit
  probe scanning is in-scope or exploratory-extra.
