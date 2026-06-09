#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shape_pairing_probe.py — does the informed prior need a per-unit SHAPE too?
===========================================================================

EXPLORATORY follow-up (2026-06-09) to ``recovery_test.py``. The main recovery
test found that a WIDE informed-α prior barely moves the period-concentrated
failure cases: the confounded likelihood (driven by the basis being in the WRONG
PLACE — broad shared basis vs a narrow true convention) overwhelms even a κ=8
prior. This probe isolates the cause by re-fitting the WORST period-concentrated
cell (α_true = 0.60) under FOUR conditions, crossing {flat, informed} prior with
{shared broad basis, CORRECT narrow basis}:

    (1) flat prior      + shared broad basis   ← the status quo (α collapses)
    (2) informed prior  + shared broad basis   ← the prototype under test
    (3) flat prior      + correct narrow basis  ← does fixing the SHAPE alone help?
    (4) informed prior  + correct narrow basis  ← shape + informed prior together

If (3)/(4) recover α≈0.60 while (1)/(2) collapse, the diagnosis is confirmed: the
problem is the basis LOCATION, not the α PRIOR — so the informed prior must be
PAIRED with a per-unit / period-aware convention SHAPE to work. This is the key
design choice flagged for Shawn.

The "correct narrow basis" here is a 3-row basis whose rows are the true narrow
convention shape (a stand-in for what a per-unit / period-aware basis would
supply); the tier_weights Dirichlet then just mixes identical rows, so p_conv is
pinned to the narrow shape. This is a DIAGNOSTIC stand-in, not a proposed basis.

Run on sapphire (MCMC), same env as recovery_test.py.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's exploratory brief, 2026-06-09.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recovery_test as rt  # reuse envelope, generators, fit_one, helpers  # noqa: E402
from informed_alpha_lib import beta_from_mean_concentration  # noqa: E402

OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    basis_shared = rt.load_shared_basis(frame="latin")

    # Rebuild the worst period-concentrated cell (α_true = 0.60).
    narrow_conv = rt.gaussian_pmf(rt.NARROW_CONV_MU, rt.NARROW_CONV_SD)
    p_gen_true = rt.exponential_pmf(rate=0.005, sign=1)
    alpha_true = 0.60
    cell = {
        "cell_index": 1, "regime": "period_concentrated",
        "alpha_true": alpha_true, "p_conv_true": narrow_conv,
        "p_gen_true": p_gen_true, "label": "concentrated_a0.60",
    }
    y, _ = rt.generate_y(cell, rt.N_PER_CELL, rt.BASE_SEED + 1)

    # A "correct narrow basis": 3 identical rows = the true narrow convention.
    # (Diagnostic stand-in for a per-unit / period-aware convention SHAPE.)
    basis_narrow = np.vstack([narrow_conv, narrow_conv, narrow_conv])

    # Informed prior centred on α_true + the conservative downward noise.
    prior_mean = float(np.clip(alpha_true + rt.PRIOR_MEAN_NOISE, 1e-3, 1 - 1e-3))
    a_inf, b_inf = beta_from_mean_concentration(prior_mean, rt.HEADLINE_CONCENTRATION)

    conditions = [
        ("flat_sharedBasis", 1.0, 1.0, basis_shared),
        ("informed_sharedBasis", a_inf, b_inf, basis_shared),
        ("flat_narrowBasis", 1.0, 1.0, basis_narrow),
        ("informed_narrowBasis", a_inf, b_inf, basis_narrow),
    ]

    out = {
        "alpha_true": alpha_true,
        "prior_mean": prior_mean,
        "concentration": rt.HEADLINE_CONCENTRATION,
        "conditions": {},
    }
    for name, aa, bb, basis in conditions:
        print(f"  [{name}] fitting ...", flush=True)
        res = rt.fit_one(y, basis, aa, bb, seed=rt.BASE_SEED + 300)
        res["alpha_bias"] = res["alpha_median"] - alpha_true
        res["genuine_spa_tv_error"] = rt.spa_l1_error(res["p_gen_median"], p_gen_true)
        out["conditions"][name] = res
        print(
            f"    {name}: alpha_med={res['alpha_median']:.3f} "
            f"(bias {res['alpha_bias']:+.3f}) "
            f"CI=[{res['alpha_ci_lo']:.3f},{res['alpha_ci_hi']:.3f}] "
            f"genuineTV={res['genuine_spa_tv_error']:.3f} rhat={res['max_rhat']:.3f}",
            flush=True,
        )

    out_path = OUT_DIR / "shape-pairing-results.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[shape-probe] wrote {out_path}")


if __name__ == "__main__":
    main()
