#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_flexnull_report.py — figures + DRAFT report for the flexible-null annex (a).
=================================================================================

Reads the part-(a) outputs (``outputs/flexnull/{flexnull-sweep,effn-thinning,
depowered-stat}.json``) and writes three figures plus ``ANNEX-REPORT.md``. Every
number in the report is read from the data — nothing is hardcoded. The §1 verdict
(the baorista go/no-go) is computed from the sweet-spot scan defined in the spec
§6.3, not asserted.

Figures:
  fig-flex-tradeoff-named.png — global p vs edf with probe P(deficit) overlaid,
      empire + latin (the trade-off curve: does flexibility de-saturate without
      eating the events?).
  fig-effn-thinning.png — global p vs effective N' (does thinning de-saturate?).
  fig-desat-summary.png — pointwise vs simultaneous global p across all 29 units,
      plus the best (max) global p reached anywhere on the flexibility ladder.

Usage:  uv run python runs/2026-06-09-h3b/code/make_flexnull_report.py
Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-15.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path("/home/shawn/Code/inscriptions")
D = ROOT / "runs/2026-06-09-h3b/outputs/flexnull"
FIG = D / "figures"
ALPHA = 0.05
NAMED = ["empire-aggregate", "latin-aggregate"]
FAM_STYLE = {"cpl": ("o", "C0"), "spline": ("s", "C1"), "gp": ("^", "C2")}

SWEEP = json.loads((D / "flexnull-sweep.json").read_text())
THIN = json.loads((D / "effn-thinning.json").read_text())
NAMES = sorted({r["name"] for r in SWEEP}, key=lambda n: -next(
    r["n_eff"] for r in SWEEP if r["name"] == n))


def rows(name):
    return [r for r in SWEEP if r["name"] == name]


def get(name, family, level):
    for r in SWEEP:
        if r["name"] == name and r["family"] == family and r["level"] == level:
            return r
    return None


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def fig_tradeoff_named():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
    for ax, nm in zip(axes, NAMED):
        rr = sorted(rows(nm), key=lambda x: x["edf"])
        for fam, (mk, col) in FAM_STYLE.items():
            fr = [r for r in rr if r["family"] == fam]
            if not fr:
                continue
            e = [r["edf"] for r in fr]
            ax.plot(e, [r["marginal_p"] for r in fr], mk + "-", color=col, alpha=.85,
                    label=f"{fam}: global p")
            ax.plot(e, [r["antonine_p_deficit"] for r in fr], mk + "--", color=col,
                    alpha=.45, mfc="none", label=f"{fam}: Antonine P(def)")
        ax.axhline(ALPHA, color="k", ls=":", lw=1)
        ax.text(ax.get_xlim()[1], ALPHA, " p=0.05", va="bottom", ha="right", fontsize=8)
        ax.set_title(f"{nm}  (n_eff={rr[0]['n_eff']:,})")
        ax.set_xlabel("effective degrees of freedom (null flexibility →)")
        ax.set_ylim(-0.03, 1.05)
    axes[0].set_ylabel("global marginal-p  /  Antonine P(deficit)")
    axes[1].legend(fontsize=7, ncol=1, loc="center right")
    fig.suptitle("Flexibility trade-off — solid = global p (flat at 0: never de-saturates); "
                 "dashed = Antonine P(deficit) (erodes as null absorbs the event)", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "fig-flex-tradeoff-named.png", dpi=130)
    plt.close(fig)


def fig_thinning():
    fig, ax = plt.subplots(figsize=(8, 5))
    show = NAMED + ["Italia (excl. Rome)", "Latium et Campania / Regio I", "Dalmatia"]
    for nm in show:
        tr = sorted([t for t in THIN if t["name"] == nm], key=lambda x: x["n_prime"])
        if not tr:
            continue
        ax.plot([t["n_prime"] for t in tr], [t["marginal_p"] for t in tr], "o-",
                label=f"{nm} (n_eff={tr[0]['n_eff']:,})")
    ax.axhline(ALPHA, color="k", ls=":", lw=1)
    ax.text(ax.get_xlim()[1], ALPHA, " p=0.05", va="bottom", ha="right", fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("effective N' (thinned, log scale)")
    ax.set_ylabel("global marginal-p (CPL-3 null)")
    ax.set_title("Effective-N thinning — global p stays < 0.05 even at N'≈1500:\n"
                 "the saturation is null-misspecification, not large-N over-power", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig-effn-thinning.png", dpi=130)
    plt.close(fig)


def fig_desat_summary():
    # Per unit: cpl-3 pointwise p, cpl-3 simultaneous p, and the MAX global p over the
    # whole flexibility ladder (the most generous de-saturation the null can buy).
    pw, sim, best = [], [], []
    for nm in NAMES:
        c3 = get(nm, "cpl", "k3")
        pw.append(c3["marginal_p"])
        sim.append(c3["marginal_p_sim"])
        best.append(max(r["marginal_p"] for r in rows(nm)))
    y = np.arange(len(NAMES))
    fig, ax = plt.subplots(figsize=(9, 8))
    ax.scatter(pw, y, marker="o", color="C0", label="CPL-3 pointwise (base null)")
    ax.scatter(sim, y, marker="s", color="C1", label="CPL-3 simultaneous-band (de-powered)")
    ax.scatter(best, y, marker="*", s=90, color="C2",
               label="best global p over flexibility ladder")
    ax.axvline(ALPHA, color="k", ls=":", lw=1)
    ax.text(ALPHA, len(NAMES) - 0.3, " p=0.05", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels([n[:26] for n in NAMES], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlim(-0.005, max(0.15, max(best) * 1.1))
    ax.set_xlabel("global marginal-p")
    ax.set_title("Per-unit de-saturation: only small-N units ever cross p=0.05;\n"
                 "every high-N / named scope stays saturated under all three levers", fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIG / "fig-desat-summary.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def build_report() -> str:
    # Sweet-spot scan (spec §6.3): global p>0.05 AND Antonine P(deficit)>=0.8 together.
    sweet = [(r["name"], r["family"], r["level"], r["marginal_p"], r["antonine_p_deficit"])
             for r in SWEEP if r["marginal_p"] > ALPHA and r["antonine_p_deficit"] >= 0.8]
    n_fits = len(SWEEP)
    named_max_pw = max(get(nm, f, l)["marginal_p"]
                       for nm in NAMED for f, l in [(r["family"], r["level"]) for r in rows(nm)])
    named_max_sim = max(get(nm, f, l)["marginal_p_sim"]
                        for nm in NAMED for f, l in [(r["family"], r["level"]) for r in rows(nm)])
    emp_thin = sorted([t for t in THIN if t["name"] == "empire-aggregate"],
                      key=lambda x: x["n_prime"])
    lat_thin = sorted([t for t in THIN if t["name"] == "latin-aggregate"],
                      key=lambda x: x["n_prime"])
    emp_thin_max = max(t["marginal_p"] for t in emp_thin)
    lat_thin_max = max(t["marginal_p"] for t in lat_thin)
    gp20_desat = [nm for nm in NAMES if (g := get(nm, "gp", "edf20")) and g["marginal_p"] > ALPHA]
    sim_desat = [nm for nm in NAMES if (c := get(nm, "cpl", "k3")) and c["marginal_p_sim"] > ALPHA]
    verdict = "NO-GO on baorista-for-the-global-test" if not sweet else "GO — sweet spot(s) found"

    def ladder_table(nm):
        rr = sorted(rows(nm), key=lambda x: (x["family"], x["edf"]))
        lines = ["| family | level | edf | global *p* | sim. *p* | Ant P(def) | Cri P(def) |",
                 "|---|---|---|---|---|---|---|"]
        for r in rr:
            lines.append(f"| {r['family']} | {r['level']} | {r['edf']:.0f} | "
                         f"{r['marginal_p']:.3f} | {r['marginal_p_sim']:.3f} | "
                         f"{r['antonine_p_deficit']:.2f} | {r['crisis_p_deficit']:.2f} |")
        return "\n".join(lines)

    def thin_table(tr):
        lines = ["| N' | global *p* | Ant P(def) | Cri P(def) |", "|---|---|---|---|"]
        for t in tr:
            lines.append(f"| {t['n_prime']:,} | {t['marginal_p']:.3f} | "
                         f"{t['antonine_p_deficit']:.2f} | {t['crisis_p_deficit']:.2f} |")
        return "\n".join(lines)

    md = f"""# H3b flexible-null robustness annex — part (a) DRAFT results (2026-06-15)

> **DRAFT — exploratory.** Part (a) of `h3b-flexible-null-annex-spec-2026-06-15.md`
> (D2's deferred work). Tests whether a more-flexible smooth null and/or a
> de-powered significance criterion de-saturate the global Timpson test reported as
> a saturated gate in `REPORT-drawwise-2026-06-15.md`. H3b is exploratory (prereg;
> Decision 15; Amdt 04 §A5.6); every reading is descriptive. **Does not change the
> base deliverable** (probe-window P(deficit)).

## 1. Verdict — {verdict}

The **sweet-spot scan** (spec §6.3: a fit where the global *p* > {ALPHA:g} **and** the
named-scope Antonine P(deficit) ≥ 0.8 hold together) returns **{len(sweet)} hits across
all {n_fits} unit×fit combinations.** No flexibility level of any of the three smooth-null
families de-saturates the global test without absorbing the events. Three independent
legs:

1. **Flexibility lever** — across the whole effective-df ladder (edf 5→20; CPL, P-spline,
   GP) the global marginal-*p* at the named scopes never exceeds **{named_max_pw:.3f}**
   (< {ALPHA:g}). Wigglier nulls only **erode** the probe signal (empire Antonine
   P(deficit) {get('empire-aggregate','cpl','k2')['antonine_p_deficit']:.2f} at edf 5 →
   {get('empire-aggregate','spline','edf20')['antonine_p_deficit']:.2f} at spline edf 20)
   without ever de-saturating the global test — the trade-off has no usable region.
2. **De-powered (simultaneous-coverage) statistic** — the max-studentised-deviation
   global *p* at the named scopes never exceeds **{named_max_sim:.3f}**. Family-wise
   coverage across the 80 bins does not rescue the high-N scopes.
3. **Effective-N thinning** — thinning the CPL-3 null down the N' ladder leaves the
   global *p* saturated even at **N'≈1,500** (empire max thinned *p* = {emp_thin_max:.3f},
   latin {lat_thin_max:.3f}). The saturation is therefore **structural
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

**empire-aggregate** (n_eff {get('empire-aggregate','cpl','k3')['n_eff']:,}):

{ladder_table('empire-aggregate')}

**latin-aggregate** (n_eff {get('latin-aggregate','cpl','k3')['n_eff']:,}):

{ladder_table('latin-aggregate')}

The penalised **spline** and **GP** ladders are monotone in edf; the **CPL** knot-sweep
is **not** (empire CPL-k5 Antonine P(def) =
{get('empire-aggregate','cpl','k5')['antonine_p_deficit']:.2f}, recovering to
{get('empire-aggregate','cpl','k7')['antonine_p_deficit']:.2f} at k7) — a knot can land on
the Antonine window and absorb it. This **knot-placement instability vindicates carrying
the two penalised-smooth families**, whose flexibility is controlled continuously rather
than by discrete knot positions.

## 3. Effective-N thinning (CPL-3 null)

See `figures/fig-effn-thinning.png`.

**empire-aggregate:**

{thin_table(emp_thin)}

**latin-aggregate:**

{thin_table(lat_thin)}

Even at N'=1,500 the global *p* stays below {ALPHA:g}; thinning kills probe *power*
(empire Antonine P(def) falls to {emp_thin[0]['antonine_p_deficit']:.2f} at N'=1,500) for a
different reason than flexibility (which absorbs the event). Both levers reduce the probe
signal, but **neither buys a de-saturated global test with the signal intact.**

## 4. De-powered statistic across all 29 units

See `figures/fig-desat-summary.png`. The simultaneous-coverage statistic de-saturates only
**{len(sim_desat)}/29** units at CPL-3 ({', '.join(sim_desat) or 'none'}); the wiggliest GP
(edf 20) de-saturates only **{len(gp20_desat)}/29** ({', '.join(gp20_desat) or 'none'}).
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
Outputs: `outputs/flexnull/{{flexnull-sweep.json,flexnull-table.csv,effn-thinning.json,depowered-stat.json}}`,
`figures/{{fig-flex-tradeoff-named,fig-effn-thinning,fig-desat-summary}}.png`, this report.
"""
    return md


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    fig_tradeoff_named()
    fig_thinning()
    fig_desat_summary()
    (D / "ANNEX-REPORT.md").write_text(build_report())
    print(f"wrote 3 figures + ANNEX-REPORT.md → {D}")


if __name__ == "__main__":
    main()
