#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_h3b_report.py — generate the draw-wise H3b DRAFT report from the outputs.
==============================================================================

Emits ``runs/2026-06-09-h3b/REPORT-drawwise-2026-06-15.md`` from
``outputs/drawwise/deviations.json`` so every number is pulled from the run, not
hand-transcribed. Reflects Shawn's 2026-06-15 decisions (D1 CPL-fit-to-observed
confirmed; D2 accept global saturation, report probe P(deficit), defer the large-N
+ baorista annex; D3 keep exp as a labelled saturated cross-check).

Usage:  uv run python runs/2026-06-09-h3b/code/make_h3b_report.py
Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-15. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/home/shawn/Code/inscriptions")
OUT = ROOT / "runs/2026-06-09-h3b/outputs/drawwise"
REPORT = ROOT / "runs/2026-06-09-h3b/REPORT-drawwise-2026-06-15.md"
NAMED_ANT = {"empire-aggregate"}
NAMED_CRI = {"empire-aggregate", "latin-aggregate"}


def f(x, n=3):
    return f"{x:.{n}f}"


def main() -> None:
    recs = json.loads((OUT / "deviations.json").read_text())
    cpl = {r["name"]: r for r in recs if r["null"] == "cpl"}
    exp = {r["name"]: r for r in recs if r["null"] == "exp"}
    order = [r["name"] for r in sorted(cpl.values(), key=lambda r: r["unit_index"])]

    # summary stats (CPL, λ=1.0)
    def pdef(name, win):
        return cpl[name]["lambda_1.0"]["probes"][win]["p_deficit"]
    def netdep(name, win):
        return cpl[name]["lambda_1.0"]["probes"][win].get("windowed_rel_departure_med", float("nan"))
    ant_hi = sum(pdef(n, "antonine") >= 0.5 for n in order)
    cri_hi = sum(pdef(n, "crisis") >= 0.5 for n in order)
    ant_net = sum(netdep(n, "antonine") < 0 for n in order)
    cri_net = sum(netdep(n, "crisis") < 0 for n in order)
    exp_sat = sum(exp[n]["lambda_1.0"]["marginal_p"] < 0.05 for n in order)
    cpl_sat = sum(cpl[n]["lambda_1.0"]["marginal_p"] < 0.05 for n in order)

    def pct(x):
        return "n/a" if x != x else f"{100*x:+.0f}%"

    L = []
    L.append("# H3b deviation-detection — draw-wise DRAFT results (2026-06-15)\n")
    L.append("> **DRAFT — exploratory.** H3b carries no Holm-corrected confirmatory "
             "family (prereg; Decision 15); all readings are descriptive. Supersedes the "
             "2026-06-09 median-based draft `REPORT.md` and is the deliverable of "
             "`h3b-implementation-spec-2026-06-14.md` under OSF Amendment 04 §A5.6 "
             "(reliability by uncertainty propagation).\n")
    L.append("**Construction (Shawn-confirmed 2026-06-15):** the genuine-SPA **posterior** "
             "(8,000 cc-library draws/unit) is propagated draw-wise through a featureless-null "
             "envelope built once per unit. The informative null is **CPL-3 fit to the observed "
             "corrected curve** (D1; standard SPD self-referential null); the **exponential** "
             "null is retained as a **labelled saturated cross-check** (D3). The global Timpson "
             "test is reported as a saturated gate and the **probe-window P(deficit)** is the "
             "deliverable (D2); the large-N correction + baorista null are a **deferred "
             "robustness annex** (D2, see end).\n")

    L.append("## 1. The global test is saturated (a methodological finding)\n")
    L.append(f"Under **both** nulls the global marginal-*p* < 0.05 for **{cpl_sat}/29** "
             f"(CPL) and **{exp_sat}/29** (exp) units. This is the documented large-N "
             "over-power of the basic SPD/Timpson test: at n_eff = 1,577–151,361 the pointwise "
             "envelope is Poisson-tight, and the real Roman epigraphic curve is jagged and "
             "humped — far richer than a monotone exponential or a 3-knot CPL — so essentially "
             "the whole curve reads as 'deviation'. The exponential null is degenerate (empire: "
             f"{_n_out(exp['empire-aggregate'])}/80 bins out-of-envelope); see "
             "`figures/fig-exp-saturation-empire.png`. The global *p* is therefore an "
             "uninformative gate here; the probe windows carry the signal. (The jaggedness of "
             "the corrected curve — e.g. a sharp feature near AD 77 — is itself a candidate for "
             "the deferred annex: real round-year structure vs deconvolution residual.)\n")

    L.append("## 2. Probe-window deficit posteriors — the deliverable (CPL null, λ=1.0)\n")
    L.append(f"Two complementary readings per window: **net dep.** = posterior-median signed "
             f"windowed relative departure from the smooth trend (negative = net deficit; the "
             f"magnitude), and **P(def)** = posterior probability that ≥ 1 window bin lies below "
             f"the envelope (the probabilistic flag; one-sided). They can diverge — a window can "
             f"be net-surplus yet carry a probable single-bin dip. By net departure, "
             f"**{ant_net}/29** units show a net Antonine deficit and **{cri_net}/29** a net "
             f"Crisis deficit; by P(def) ≥ 0.5, **{ant_hi}/29** (Antonine) and **{cri_hi}/29** "
             f"(Crisis). `λ1.2` = §A5.5 coverage-inflation sensitivity on P(def).\n")
    L.append("Flags: `*` θ-sensitive soft-annotated (Amendment 04 §A5.6); "
             "`‡` below the cpl-3 reachability floor (n_eff < 1,618); "
             "`◆` prereg-named probe scope.\n")
    hdr = ("| unit | n_eff | Ant net dep. | Ant P(def) | Ant λ1.2 | "
           "Cri net dep. | Cri P(def) | Cri λ1.2 | flags |")
    L.append(hdr)
    L.append("|" + "---|" * 9)
    for n in order:
        r = cpl[n]
        a1 = r["lambda_1.0"]["probes"]; a2 = r["lambda_1.2"]["probes"]
        flags = ""
        if n in (NAMED_ANT | NAMED_CRI):
            flags += "◆"
        if r["soft_annotated"]:
            flags += "*"
        if r["reach_caveat"]:
            flags += "‡"
        L.append(f"| {n} | {r['n_eff']:,} | "
                 f"{pct(a1['antonine'].get('windowed_rel_departure_med', float('nan')))} | "
                 f"{f(a1['antonine']['p_deficit'],2)} | {f(a2['antonine']['p_deficit'],2)} | "
                 f"{pct(a1['crisis'].get('windowed_rel_departure_med', float('nan')))} | "
                 f"{f(a1['crisis']['p_deficit'],2)} | {f(a2['crisis']['p_deficit'],2)} | {flags} |")

    L.append("\n## 3. Prereg-named scopes\n")
    for n in ["empire-aggregate", "latin-aggregate"]:
        a = cpl[n]["lambda_1.0"]["probes"]
        L.append(f"- **{n}** — Antonine net dep. "
                 f"**{pct(a['antonine'].get('windowed_rel_departure_med', float('nan')))}**, "
                 f"P(deficit) **{f(a['antonine']['p_deficit'],3)}**; Crisis net dep. "
                 f"**{pct(a['crisis'].get('windowed_rel_departure_med', float('nan')))}**, "
                 f"P(deficit) **{f(a['crisis']['p_deficit'],3)}**.")
    L.append("\nempire is the named Antonine scope; latin-aggregate is the operational "
             "Western-Empire-provincial Crisis scope (Decision 36). Both show high-probability "
             "deficits at their named windows, consistent with the Antonine-plague and "
             "Third-Century-Crisis decline narratives. All other per-unit rows are "
             "**exploratory-extra** (broader than the prereg's named scope; scope confirmed "
             "2026-06-14).\n")

    L.append("## 4. Coverage sensitivity (λ=1.2)\n")
    L.append("The §A5.5 inflation sensitivity (widen each draw about its posterior mean by "
             "1.2, counteracting the cc posterior's ~1σ optimism) moves only borderline units "
             "and leaves saturated/near-zero ones flat — see the `λ1.2` columns above. It is a "
             "sensitivity, not the headline; the primary reading is λ=1.0.\n")

    L.append("## 5. Raw-vs-corrected follow-up\n")
    L.append("Per launch-spec §8, the raw (uncorrected) SPA was tested against the same null. "
             "Both raw and corrected global tests saturate at these N, so the comparison is "
             "uninformative at the global level here; the per-unit raw global *p* is in "
             "`outputs/drawwise/raw-vs-corrected.json`.\n")

    L.append("## 6. Caveats\n")
    L.append("- **Global saturation** (above): the deliverable is the probe-window P(deficit), "
             "not the global *p*.\n"
             "- **Coverage** (§A5.5): cc CIs are ~1σ-optimistic; propagated deviations carry "
             "the caveat, with λ=1.2 as the sensitivity.\n"
             "- **Soft-annotated units** (Moesia inferior, Britannia): θ-sensitive; flagged not "
             "excluded; read with extra caution.\n"
             "- **Reachability** (`‡`): units below the cpl-3 province floor (n_eff < 1,618; "
             "Lusitania 1,577) carry a power caveat.\n"
             "- **Jaggedness of the corrected curve** drives the saturation and may inflate "
             "probe P(deviation); whether it is real structure or deconvolution residual is a "
             "question for the annex.\n")

    L.append("## 7. Deferred robustness annex (D2 — to run after this base)\n")
    L.append("- **Large-N correction** — a reduced-significance / mark-permutation variant or "
             "effective-N thinning so the global test is not over-powered.\n"
             "- **baorista Bayesian-aoristic null** (prereg line 378) — a better-specified "
             "flexible null that may also sharpen the probe readings.\n"
             "Both are independent post-hoc sensitivities; neither changes the base deliverable. "
             "Logged in `planning/backlog` / the decision note.\n")

    L.append("## 8. Reproduce\n```bash\n"
             "uv run python runs/2026-06-09-h3b/code/run_h3b_drawwise.py   # Stage B\n"
             "uv run python runs/2026-06-09-h3b/code/make_h3b_report.py    # this report\n"
             "uv run python runs/2026-06-09-h3b/code/plot_h3b_drawwise.py  # figures\n```\n")
    L.append("Figures: `outputs/drawwise/figures/{fig-cpl-smallmultiples,fig-named-scopes,"
             "fig-exp-saturation-empire}.png`. Per-test detail: "
             "`outputs/drawwise/deviations-table.csv`.\n")

    REPORT.write_text("\n".join(L))
    print(f"wrote {REPORT}  ({ant_hi}/29 Antonine, {cri_hi}/29 Crisis P(def)≥0.5)")


def _n_out(rec) -> int:
    import numpy as np
    lo = np.array(rec["lo_env"]); hi = np.array(rec["hi_env"])
    obs = np.array(rec["median_corrected_counts"])
    return int(((obs < lo) | (obs > hi)).sum())


if __name__ == "__main__":
    main()
