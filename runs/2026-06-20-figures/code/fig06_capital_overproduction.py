#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 — Capital over-production (forest + temporal consistency).
=============================================================

Provincial capitals carry systematically more inscriptions than non-capitals of
the same population (Obs 74 / Decision 37, confirmatory). Two panels:

* **(a) Overall forest** — the empire and Latin capital-vs-non-capital residual
  contrasts, each a posterior median + 95 % credible interval, with a 0 reference
  line. Both intervals sit well clear of 0.
* **(b) Per-period** — the capital contrast in each of the eight 50-year periods,
  both frames, showing capitals over-produce in *every* period (P(contrast > 0)
  = 1.00 throughout). The per-period summaries store the median + P(>0) but not a
  full interval, so this panel shows medians (the interval panel is (a)).

Data: ``h3c-i-results-oxrep-primary.json`` (overall, with CIs);
``h7-summary.json`` + ``h7-latin-summary.json`` (per-period medians).

Encoding: empire = blue, Latin = vermillion; 0 reference line dashed grey.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
OVERALL = ROOT / "runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results-oxrep-primary.json"
H7_EMPIRE = ROOT / "runs/2026-06-17-s5-h7-perperiod-h3c/outputs/h7-summary.json"
H7_LATIN = ROOT / "runs/2026-06-18-h7-latin/outputs/h7-latin-summary.json"
STEM = "fig06-capital-overproduction"


def _period_midpoints(labels: list[str]) -> np.ndarray:
    """Midpoint year of each ``"a..b"`` period label."""
    mids = []
    for lab in labels:
        a, b = (float(v) for v in lab.split(".."))
        mids.append((a + b) / 2.0)
    return np.array(mids)


def build():
    overall = json.loads(OVERALL.read_text())
    h7e = json.loads(H7_EMPIRE.read_text())
    h7l = json.loads(H7_LATIN.read_text())

    fig, (axf, axt) = T.figure_2col(height_ratio=0.40, ncols=2,
                                    gridspec_kw={"width_ratios": [1.0, 1.3]})

    # --- panel (a): overall forest with 95 % CIs ------------------------------
    rows = [("Latin\n(overall)", overall["latin"], T.LATIN),
            ("Empire\n(overall)", overall["empire"], T.EMPIRE)]
    for i, (label, d, colour) in enumerate(rows):
        med = d["median_contrast"]
        lo, hi = d["contrast_ci95"]
        axf.plot([lo, hi], [i, i], color=colour, lw=2.0, zorder=3,
                 solid_capstyle="round")
        axf.plot([med], [i], "o", color=colour, ms=6, zorder=4)
    axf.set_yticks(range(len(rows)))
    axf.set_yticklabels([r[0] for r in rows])
    axf.set_ylim(-0.6, len(rows) - 0.4)
    T.zero_line(axf, "v")
    axf.set_xlabel("capital over-production\n(posterior residual contrast)")
    axf.set_title("(a) Overall (95 % CI)", fontsize=9.0)
    axf.grid(axis="x", alpha=0.4)
    axf.grid(axis="y", visible=False)

    # --- panel (b): per-period medians, both frames ---------------------------
    labels = h7e["period_labels"]
    mids = _period_midpoints(labels)
    emp = [h7e["per_period"][k]["capital_contrast"]["contrast_median"] for k in labels]
    lat = [h7l["per_period"][k]["capital_contrast"]["contrast_median"] for k in labels]

    T.zero_line(axt, "h")
    axt.plot(mids, emp, "-o", color=T.EMPIRE, ms=4, lw=1.3, label="empire")
    axt.plot(mids, lat, "-s", color=T.LATIN, ms=4, lw=1.3, label="Latin")
    axt.set_ylim(bottom=min(0, min(emp + lat)) - 0.05)
    T.year_axis(axt, ticks=(0, 100, 200, 300))
    axt.set_ylabel("contrast (median)")
    axt.set_title("(b) Per period — P(contrast > 0) = 1.00 throughout",
                  fontsize=9.0)
    axt.legend(loc="upper right", fontsize=7.5)

    fig.suptitle("Provincial capitals over-produce inscriptions", fontsize=10.0)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
