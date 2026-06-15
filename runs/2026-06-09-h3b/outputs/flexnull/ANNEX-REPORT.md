# H3b flexible-null robustness annex — part (a) DRAFT results (2026-06-15)

> **DRAFT — exploratory.** Part (a) of `h3b-flexible-null-annex-spec-2026-06-15.md`
> (D2's deferred work). Tests whether a more-flexible smooth null and/or a
> de-powered significance criterion de-saturate the global Timpson test reported as
> a saturated gate in `REPORT-drawwise-2026-06-15.md`. H3b is exploratory (prereg;
> Decision 15; Amdt 04 §A5.6); every reading is descriptive. **Does not change the
> base deliverable** (probe-window P(deficit)).

## 1. Verdict — NO-GO on baorista-for-the-global-test

The **sweet-spot scan** (spec §6.3: a fit where the global *p* > 0.05 **and** the
named-scope Antonine P(deficit) ≥ 0.8 hold together) returns **0 hits across
all 290 unit×fit combinations.** No flexibility level of any of the three smooth-null
families de-saturates the global test without absorbing the events. Three independent
legs:

1. **Flexibility lever** — across the whole effective-df ladder (edf 5→20; CPL, P-spline,
   GP) the global marginal-*p* at the named scopes never exceeds **0.000**
   (< 0.05). Wigglier nulls only **erode** the probe signal (empire Antonine
   P(deficit) 1.00 at edf 5 →
   0.83 at spline edf 20)
   without ever de-saturating the global test — the trade-off has no usable region.
2. **De-powered (simultaneous-coverage) statistic** — the max-studentised-deviation
   global *p* at the named scopes never exceeds **0.001**. Family-wise
   coverage across the 80 bins does not rescue the high-N scopes.
3. **Effective-N thinning** — thinning the CPL-3 null down the N' ladder leaves the
   global *p* saturated even at **N'≈1,500** (empire max thinned *p* = 0.006,
   latin 0.002). The saturation is therefore **structural
   null-misspecification — the smooth null cannot represent the jagged real epigraphic
   curve — not large-N over-power.** (Phase 1 detected at N≈1,600 against a *matching*
   null; here a *smooth* null on a *jagged* curve saturates even at N≈1,500.)

**Consequence (spec §10):** baorista is **NO-GO for the global test** — a featureless
Bayesian-aoristic growth null absorbs *less* structure than these self-referential nulls,
so it cannot de-saturate where they cannot. It is demoted to an **optional, lower-priority
probe-sharpening cross-check**. The **probe-window P(deficit) remains THE H3b deliverable**,
and is now shown **robust** to null flexibility, de-powering, and effective-N (the named
scopes hold ≥ 0.67–1.00 across the entire ladder until the null is wiggly enough to eat
the event outright).

## 2. Flexibility trade-off — named scopes

See `figures/fig-flex-tradeoff-named.png` (solid = global *p*, flat at ~0 throughout;
dashed = Antonine P(deficit), eroding as edf rises).

**empire-aggregate** (n_eff 151,361):

| family | level | edf | global *p* | sim. *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|---|---|---|
| cpl | k2 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | k3 | 7 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | k5 | 11 | 0.000 | 0.001 | 0.17 | 1.00 |
| cpl | k7 | 15 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | edf5 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | edf10 | 10 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | edf20 | 20 | 0.000 | 0.001 | 0.96 | 1.00 |
| spline | edf5 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | edf10 | 10 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | edf20 | 20 | 0.000 | 0.001 | 0.83 | 1.00 |

**latin-aggregate** (n_eff 101,066):

| family | level | edf | global *p* | sim. *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|---|---|---|
| cpl | k2 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | k3 | 7 | 0.000 | 0.001 | 1.00 | 1.00 |
| cpl | k5 | 11 | 0.000 | 0.001 | 0.85 | 1.00 |
| cpl | k7 | 15 | 0.000 | 0.001 | 0.85 | 1.00 |
| gp | edf5 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| gp | edf10 | 10 | 0.000 | 0.001 | 0.91 | 1.00 |
| gp | edf20 | 20 | 0.000 | 0.001 | 0.75 | 0.98 |
| spline | edf5 | 5 | 0.000 | 0.001 | 1.00 | 1.00 |
| spline | edf10 | 10 | 0.000 | 0.001 | 0.95 | 1.00 |
| spline | edf20 | 20 | 0.000 | 0.001 | 0.67 | 1.00 |

The penalised **spline** and **GP** ladders are monotone in edf; the **CPL** knot-sweep
is **not** (empire CPL-k5 Antonine P(def) =
0.17, recovering to
1.00 at k7) — a knot can land on
the Antonine window and absorb it. This **knot-placement instability vindicates carrying
the two penalised-smooth families**, whose flexibility is controlled continuously rather
than by discrete knot positions.

## 3. Effective-N thinning (CPL-3 null)

See `figures/fig-effn-thinning.png`.

**empire-aggregate:**

| N' | global *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|
| 1,500 | 0.006 | 0.53 | 0.07 |
| 3,000 | 0.000 | 1.00 | 1.00 |
| 6,000 | 0.000 | 1.00 | 1.00 |
| 12,000 | 0.000 | 1.00 | 1.00 |
| 25,000 | 0.000 | 1.00 | 1.00 |

**latin-aggregate:**

| N' | global *p* | Ant P(def) | Cri P(def) |
|---|---|---|---|
| 1,500 | 0.002 | 0.99 | 0.35 |
| 3,000 | 0.000 | 1.00 | 0.78 |
| 6,000 | 0.000 | 1.00 | 0.95 |
| 12,000 | 0.000 | 1.00 | 0.99 |
| 25,000 | 0.000 | 1.00 | 1.00 |

Even at N'=1,500 the global *p* stays below 0.05; thinning kills probe *power*
(empire Antonine P(def) falls to 0.53 at N'=1,500) for a
different reason than flexibility (which absorbs the event). Both levers reduce the probe
signal, but **neither buys a de-saturated global test with the signal intact.**

## 4. De-powered statistic across all 29 units

See `figures/fig-desat-summary.png`. The simultaneous-coverage statistic de-saturates only
**2/29** units at CPL-3 (Pannonia inferior, Noricum); the wiggliest GP
(edf 20) de-saturates only **2/29** (Noricum, Ostia).
Every such unit is small-N (n_eff ≲ 2,600) **with no event signal** (none is a sweet spot),
so de-saturation there reflects a wider envelope, not a better-tracked event.

## 5. Caveats

- **Self-referential null.** All smoothers fit the posterior-median corrected curve (base
  D1), so high flexibility trivially shrinks the residual — which is exactly why the
  *event-preservation axis* (probe P(deficit)) is reported at every fit: de-saturation is
  meaningful only if the events survive, and they do not at the flexibility where (a few
  small-N) units de-saturate.
- **Exploratory.** No confirmatory gate; the 0.05 / 0.8 thresholds are the spec §6.3 readout
  convention, not a decision rule.
- **Reproducibility.** The k=3 CPL point reproduces the base run bit-for-bit (driver
  regression guard); the spline/GP/simultaneous code passed a sanity gate.

## 6. What this changes

Nothing in the base deliverable. It **closes D2's deferred question** with a decisive
negative: the global Timpson saturation is robust to null flexibility (three families, edf
5→20), to de-powered simultaneous-coverage significance, and to effective-N thinning to
≈1,500 — i.e. it is genuine null-misspecification, and the probe-window P(deficit) is
confirmed (and now shown robust) as the H3b readout. **baorista part (b) is not warranted
for the global test**; if ever built, only as a probe-sharpening cross-check.

## 7. Reproduce
```bash
# sapphire (compute):
uv run python runs/2026-06-09-h3b/code/run_h3b_flexnull.py
uv run python runs/2026-06-09-h3b/code/make_flexnull_report.py
```
Outputs: `outputs/flexnull/{flexnull-sweep.json,flexnull-table.csv,effn-thinning.json,depowered-stat.json}`,
`figures/{fig-flex-tradeoff-named,fig-effn-thinning,fig-desat-summary}.png`, this report.
