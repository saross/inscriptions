#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_h3b_drawwise.py — envelope plots for the draw-wise H3b.
============================================================

Reads ``outputs/drawwise/deviations.json`` + the cc-refit posterior draws and
renders, for the informative CPL-fit-to-observed null:

  * ``fig-cpl-smallmultiples.png`` — all 29 units: the featureless-null envelope,
    the median corrected curve, the 95% posterior band, the two probe windows, and
    the out-of-envelope median bins;
  * ``fig-named-scopes.png`` — empire-aggregate + latin-aggregate (the prereg-named
    probe scopes), enlarged, with the Antonine/Crisis P(deficit) annotated;
  * ``fig-exp-saturation-empire.png`` — empire under the exp null, illustrating the
    saturated cross-check (the monotone null cannot represent the humped curve).

Usage:  uv run python runs/2026-06-09-h3b/code/plot_h3b_drawwise.py
Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-06-09-h3b/code"))
import h3b_drawwise as E  # noqa: E402

OUT_DIR = ROOT / "runs/2026-06-09-h3b/outputs/drawwise"
FIG_DIR = OUT_DIR / "figures"
DRAWS_DIR = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
BC = E.BIN_CENTRES
ANT, CRI = E.ANTONINE_WINDOW, E.CRISIS_WINDOW


def _records():
    return json.load((OUT_DIR / "deviations.json").open())


def _by(records, null):
    d = {r["name"]: r for r in records if r["null"] == null}
    return d


def _post_band(name, n_eff):
    g = E.load_draws_normalised(name, DRAWS_DIR) * n_eff
    return np.percentile(g, [2.5, 50, 97.5], axis=0)


def _panel(ax, rec, *, title=True, legend=False):
    lo = np.array(rec["lo_env"]); hi = np.array(rec["hi_env"])
    mid = np.array(rec["null_mid"]); obs = np.array(rec["median_corrected_counts"])
    p_lo, _, p_hi = _post_band(rec["name"], rec["n_eff"])
    for w, c in ((ANT, "#d62728"), (CRI, "#9467bd")):
        ax.axvspan(w[0], w[1], color=c, alpha=0.08, lw=0)
    ax.fill_between(BC, lo, hi, color="0.80", label="null 95% envelope", lw=0)
    ax.plot(BC, mid, color="0.45", lw=0.8, ls="--", label="null centre")
    ax.fill_between(BC, p_lo, p_hi, color="#1f77b4", alpha=0.20, lw=0,
                    label="corrected 95% posterior")
    ax.plot(BC, obs, color="#1f77b4", lw=1.1, label="corrected median")
    out = (obs < lo) | (obs > hi)
    ax.plot(BC[out], obs[out], "o", ms=2.2, color="#ff7f0e", label="out-of-envelope")
    a = rec["lambda_1.0"]["probes"]
    if title:
        flag = " *" if rec["soft_annotated"] else ("  ‡" if rec["reach_caveat"] else "")
        ax.set_title(f"{rec['name'][:26]}{flag}\nAnt P(def)={a['antonine']['p_deficit']:.2f}  "
                     f"Cri P(def)={a['crisis']['p_deficit']:.2f}", fontsize=7.5)
    ax.set_xlim(-50, 350)
    ax.tick_params(labelsize=6)
    if legend:
        ax.legend(fontsize=7, loc="upper left", framealpha=0.9)


def small_multiples(records):
    cpl = _by(records, "cpl")
    order = sorted(cpl.values(), key=lambda r: r["unit_index"])
    fig, axes = plt.subplots(6, 5, figsize=(18, 20))
    for ax, rec in zip(axes.flat, order):
        _panel(ax, rec)
    for ax in axes.flat[len(order):]:
        ax.axis("off")
    fig.suptitle("H3b draw-wise — corrected genuine SPA vs featureless CPL-3 null "
                 "(fit to observed; counts).  Shaded: Antonine (red), Crisis (purple).  "
                 "* = θ-sensitive soft-annotated;  ‡ = below cpl-3 reachability floor.",
                 fontsize=11, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    fig.savefig(FIG_DIR / "fig-cpl-smallmultiples.png", dpi=110)
    plt.close(fig)


def named_scopes(records):
    cpl = _by(records, "cpl")
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.2))
    for ax, name in zip(axes, ["empire-aggregate", "latin-aggregate"]):
        _panel(ax, cpl[name], legend=(name == "empire-aggregate"))
    fig.suptitle("Prereg-named probe scopes — empire-aggregate (Antonine) + "
                 "latin-aggregate (Crisis / Western-Empire-provincial), CPL null",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(FIG_DIR / "fig-named-scopes.png", dpi=130)
    plt.close(fig)


def exp_saturation(records):
    exp = _by(records, "exp")
    rec = exp["empire-aggregate"]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    _panel(ax, rec, title=False, legend=True)
    n_out = int(((np.array(rec["median_corrected_counts"]) < np.array(rec["lo_env"])) |
                 (np.array(rec["median_corrected_counts"]) > np.array(rec["hi_env"]))).sum())
    ax.set_title(f"empire-aggregate under the EXPONENTIAL null — saturated cross-check: "
                 f"{n_out}/80 bins out-of-envelope (monotone null cannot represent the "
                 f"humped curve)", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig-exp-saturation-empire.png", dpi=130)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    records = _records()
    small_multiples(records)
    named_scopes(records)
    exp_saturation(records)
    print(f"wrote 3 figures → {FIG_DIR}")


if __name__ == "__main__":
    main()
