#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F15 — Rome de-fogged (before/after); the most convention-dated unit.
====================================================================

Rome's raw aoristic SPD (uncorrected, convention-laden) against its de-fogged
genuine SPD with 95 % band — the capital de-fogging exhibit, in the F1 idiom. The
orange fill is Rome's editorial-convention component (the F1+F3 round-slab
families). Rome's **convention fraction α ≈ 0.80** (the highest of any unit): the
imperial capital's apparent chronology is ~four-fifths editorial artefact, so the
genuine (de-fogged) curve is a small, uncertain residual of the raw — read its
shape with caution (high-α units have a weakly-constrained genuine component).

Data: raw + convention from the filtered LIRE corpus (province == "Roma");
genuine draws from the Roma cc-library fit
(runs/2026-06-21-rome-capital-comparison/outputs/posterior-draws/Roma-pgen.npz).

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import figdata as D
import figtheme as T

ROOT = Path("/home/shawn/Code/inscriptions")
ROMA_NPZ = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs/posterior-draws/Roma-pgen.npz"
ROMA_SUM = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs/roma-italia-summary.json"
STEM = "fig15-rome-before-after"


def build():
    x = D.years()
    df = D.corpus()
    roma = df[df["province"] == "Roma"]
    raw = D.raw_aoristic_rows(roma["nb"].to_numpy(), roma["na"].to_numpy())
    conv_rows = roma[roma["family"].isin(["F1_round", "F3_periodic"])]
    conv = D.raw_aoristic_rows(conv_rows["nb"].to_numpy(), conv_rows["na"].to_numpy())
    raw_total = float(raw.sum())
    raw_dens = raw / raw_total / D.BIN_SIZE
    conv_dens = conv / raw_total / D.BIN_SIZE

    lo, med, hi = D.quantile_band(D.genuine_draws_npz(ROMA_NPZ))
    lo, med, hi = (a / D.BIN_SIZE for a in (lo, med, hi))

    alpha = next(u["alpha_median"] for u in json.loads(ROMA_SUM.read_text())["units"]
                 if u["name"] == "Roma")

    fig, ax = T.figure_1col(height_ratio=0.78)
    ax.fill_between(x, 0, conv_dens, color=T.OKABE_ITO["orange"], alpha=0.45,
                    linewidth=0, zorder=2, label="editorial-convention component")
    ax.plot(x, raw_dens, color=T.NEUTRAL, linestyle="--", linewidth=1.2, alpha=0.9,
            zorder=3, label="raw aoristic (uncorrected)")
    T.band(ax, x, lo, hi, color=T.LATIN, alpha=0.22, zorder=4,
           label="genuine 95 % band")
    ax.plot(x, med, color=T.LATIN, linewidth=1.8, zorder=5, label="genuine (de-fogged)")

    ax.set_ylim(0, max(float(np.max(raw_dens)), float(hi.max())) * 1.28)
    ax.set_ylabel("probability density (per year)")
    T.year_axis(ax)
    ax.set_title("Rome de-fogged — the most convention-dated unit", fontsize=8.8)
    ax.text(0.015, 0.97, f"convention fraction α = {alpha:.2f}\n→ ~{alpha*100:.0f}% of "
            "Rome's apparent\ndating is editorial convention",
            transform=ax.transAxes, va="top", fontsize=6.8,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFF4E8",
                      ec=T.OKABE_ITO["orange"], lw=0.6))
    ax.legend(loc="upper right", fontsize=6.8)
    return fig


def main() -> None:
    T.apply()
    fig = build()
    paths = T.save(fig, STEM)
    print(f"wrote {paths['pdf'].name} + {paths['png'].name}")


if __name__ == "__main__":
    main()
