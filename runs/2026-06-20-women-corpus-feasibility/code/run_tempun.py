#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_tempun.py — tempun Monte-Carlo temporal SPA of the women corpus (§6 input).
===============================================================================

Runs Adela Sobotkova's group's **tempun** package (Kaše/Heřmánková/Sobotková;
``tempun==0.2.6``) over the datable conjugal women corpus, producing the
Monte-Carlo aoristic temporal distribution + an uncertainty band — the input for
the Option-2 case-study §6 comparison (genuine-vs-raw-vs-tempun).

**The methodological point (option-2-case-study-outline.md §6):** tempun models
*aoristic dating uncertainty* (random dates sampled within each inscription's
interval, many simulations → a confidence band). Our cross-classified
deconvolution removes *editorial convention*. They correct **different** artefacts:
tempun's mean tracks the raw aoristic shape (it does NOT remove the round-slab
convention), while the de-fogged genuine SPD does. So tempun and de-fogging are
complementary, not redundant — which this run makes concrete.

tempun is also kept installed as a **reusable cross-check tool** (Shawn 2026-06-21).

Output: ``outputs/tempun-women.json`` — block midpoints + the per-year density mean
and 90 % band, for the full corpus and per role. Light (Monte-Carlo date sampling,
no MCMC); runs in seconds locally. Reproducible (global numpy seed).

Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tempun

ROOT = Path("/home/shawn/Code/inscriptions")
sys.path.insert(0, str(ROOT / "runs/2026-06-20-women-corpus-feasibility/code"))
import run_women_feasibility as W  # noqa: E402

OUT = ROOT / "runs/2026-06-20-women-corpus-feasibility/outputs"
N_SIM = 1000
BLOCK_STEP = 25            # tempun's natural granularity (scale=25)
ENV_START, ENV_END = -50, 350
SEED = 20260621


def tempun_density(nb, na):
    """Monte-Carlo temporal distribution for one subset: returns (midpoints,
    mean per-year density, lo90, hi90)."""
    randoms = [tempun.model_date(int(s), int(e), size=N_SIM)
               for s, e in zip(nb, na)]
    tb = tempun.get_timeblocks(ENV_START, ENV_END, BLOCK_STEP)
    sim = tempun.timeblocks_from_randoms(randoms, tb)          # N_SIM sims × blocks
    counts = np.array([[b[1] for b in s] for s in sim], dtype=float)  # (N_SIM, n_blocks)
    mids = np.array([(lo + hi) / 2.0 for (lo, hi) in tb])
    # normalise each simulation to a per-year density (sum→1 over time, ÷ block width)
    dens = counts / counts.sum(axis=1, keepdims=True) / BLOCK_STEP
    mean = dens.mean(axis=0)
    lo, hi = np.percentile(dens, [5, 95], axis=0)
    return mids, mean, lo, hi


def main() -> int:
    np.random.seed(SEED)
    d = W.load_women()
    subsets = {"overall": d,
               "wives": d[d["role"] == "wife"],
               "daughters": d[d["role"] == "daughter"]}
    out = {"package": "tempun==0.2.6", "n_sim": N_SIM, "block_step": BLOCK_STEP,
           "envelope": [ENV_START, ENV_END], "seed": SEED,
           "note": ("Monte-Carlo aoristic SPA (samples random dates within each "
                    "interval); models DATING UNCERTAINTY, does NOT remove editorial "
                    "convention — complementary to the cc-library de-fogging."),
           "subsets": {}}
    for name, sub in subsets.items():
        mids, mean, lo, hi = tempun_density(sub["nb"].to_numpy(), sub["na"].to_numpy())
        out["subsets"][name] = {
            "n": int(len(sub)), "block_mid_years": [float(x) for x in mids],
            "density_mean": [float(x) for x in mean],
            "density_lo90": [float(x) for x in lo],
            "density_hi90": [float(x) for x in hi]}
        print(f"  tempun {name:9s} N={len(sub):4d}  peak block "
              f"~AD {mids[int(np.argmax(mean))]:.0f}")
    (OUT / "tempun-women.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {OUT / 'tempun-women.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
