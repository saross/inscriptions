#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grid_lib.py — cell enumeration + realistic generators for the joint recovery grid.
==================================================================================

The full recovery-validation grid for the joint identifiability-remediation model
(`full-grid-spec.md`). A cell = (convention recipe → %win, α_true, genuine shape, N).
Per cell we generate `n_reps` well-specified replicates (`y ~ Multinomial`,
`k ~ Binomial`) and fit the LEAD model — `build_model_joint` with the per-unit
**estimated** (contaminated aligned-subset) convention basis + κ=40 θ priors — exactly
the production-realistic case the POC validated (Exp 3). Recovery is scored against the
acceptance criteria (`full-grid-spec.md` §3).

Reuses the validated low-level pieces: `joint_lib.build_model_joint` (temporal block
byte-identical to the recovery-validated `build_model_f1_f3`), the slab/genuine shape
generators, and the θ calibration. Seed policy mirrors the lodged grids
(`base_seed + cell_index`, per-replicate offset).

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
sys.path.insert(0, str(RUN / "code"))
import joint_lib as J  # noqa: E402

BINC = J.BIN_CENTRES
WIN = (BINC >= 100) & (BINC <= 300)

# Production sampler defaults (lodged recovery-grid config).
N_REPS_DEFAULT = 100
DRAWS, TUNE, CHAINS, TACC = 2000, 1000, 4, 0.95
BASE_SEED = 20260609
THETA_PRIOR_KAPPA = 40.0
THETA_CONV_TRUE, THETA_GEN_TRUE = 0.95, 0.15   # generation truth

# --- convention recipes (round-endpoint slab mixtures) spanning %win ---
CONV_RECIPES = {
    "broad_early": [(1, 200), (1, 150), (1, 250), (50, 200)],
    "broad":       [(1, 300), (1, 200), (1, 250), (50, 250)],
    "mid_conc":    [(51, 300), (101, 300), (1, 300), (76, 250)],
    "conc":        [(101, 300), (151, 300), (101, 250), (51, 300)],
    "stress":      [(101, 300), (151, 300), (101, 250), (101, 200)],
}

# --- genuine shapes ---
def _gen_shapes() -> dict[str, np.ndarray]:
    return {
        "gauss_early": J.gaussian_pgen(80, 45),
        "gauss_inwin": J.gaussian_pgen(200, 40),
        "regnal":      J.regnal_cluster_pgen([165, 200, 235], sigma=12.0),
        "broad_gen":   J.gaussian_pgen(160, 90),
    }

ALPHAS = (0.0, 0.2, 0.4, 0.6, 0.8)
NS = (1500, 2800, 15000)


def pct_win(spa: np.ndarray) -> float:
    return float(spa[WIN].sum() / spa.sum())


def regime_of(conv_win: float, gen_name: str) -> str:
    """Identifiable if convention is broad (low %win) OR genuine is temporally
    separated from convention; confounded if convention is concentrated AND genuine
    lives in the same AD 100–300 window."""
    concentrated = conv_win >= 0.70
    gen_inwin = gen_name in ("gauss_inwin", "regnal")
    return "confounded" if (concentrated and gen_inwin) else "identifiable"


def enumerate_cells() -> list[dict]:
    """All grid cells in deterministic order: recipe × α × genuine × N."""
    gens = _gen_shapes()
    cells: list[dict] = []
    idx = 0
    for recipe in CONV_RECIPES:                      # 5
        p_conv = J.slab_mixture_spa(CONV_RECIPES[recipe])
        cwin = pct_win(p_conv)
        for alpha in ALPHAS:                          # 5
            for gen_name in sorted(gens):             # 4
                for n in NS:                          # 3
                    cells.append({
                        "cell_index": idx,
                        "cell_id": f"{recipe}_a{alpha:.1f}_{gen_name}_N{n}",
                        "recipe": recipe,
                        "conv_pct_win": round(cwin, 3),
                        "alpha_true": float(alpha),
                        "gen_name": gen_name,
                        "gen_pct_win": round(pct_win(gens[gen_name]), 3),
                        "N": int(n),
                        "regime": regime_of(cwin, gen_name),
                    })
                    idx += 1
    return cells


def cell_shapes(cell: dict) -> tuple[np.ndarray, np.ndarray]:
    """Return (p_conv_true, p_gen_true) for a cell."""
    p_conv = J.slab_mixture_spa(CONV_RECIPES[cell["recipe"]])
    p_gen = _gen_shapes()[cell["gen_name"]]
    return p_conv, p_gen


def estimated_basis(p_conv: np.ndarray, p_gen: np.ndarray, alpha: float) -> np.ndarray:
    """Production-realistic per-unit convention basis = EXPECTED aoristic SPA of the
    grid-aligned subset (contaminated): ∝ α·θ_conv·p_conv + (1−α)·θ_gen·p_gen, built into
    a 3-row ±shift bracket (POC `per_unit_basis`)."""
    mix = (alpha * THETA_CONV_TRUE * p_conv + (1.0 - alpha) * THETA_GEN_TRUE * p_gen)
    mix = mix / mix.sum()

    def shift(v, by):
        out = np.roll(v, by)
        if by > 0:
            out[:by] = 0
        elif by < 0:
            out[by:] = 0
        return out / out.sum()

    rows = np.vstack([mix, shift(mix, 3), shift(mix, -3)])
    return rows / rows.sum(axis=1, keepdims=True)


def generate(cell: dict, p_conv: np.ndarray, p_gen: np.ndarray, rep: int) -> tuple[np.ndarray, int]:
    """Well-specified draw for replicate `rep` (deterministic seed)."""
    seed = (BASE_SEED + cell["cell_index"]) * 1000 + rep
    rng = np.random.default_rng(seed)
    p_mix = cell["alpha_true"] * p_conv + (1.0 - cell["alpha_true"]) * p_gen
    p_mix = p_mix / p_mix.sum()
    n = cell["N"]
    y = rng.multinomial(n, p_mix)
    pi = cell["alpha_true"] * THETA_CONV_TRUE + (1.0 - cell["alpha_true"]) * THETA_GEN_TRUE
    k = int(rng.binomial(n, pi))
    return y, k
