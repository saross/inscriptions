#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_cc_setdata.py — build-once + set_data equivalence gate for the cc model.
=================================================================================

Audit finding M3: the cross-classified model exercises a pattern the lead's
set_data revalidation never covered — a mutable ``k_data`` consumed both as
observed data (the binomial) and as the symbolic ``n`` of two multinomials.
This gate fits the same (cell, rep) two ways with the same sampler seed:

  (a) FRESH — model built directly with that replicate's data;
  (b) SWAP — model built with rep-0 placeholder data, then ``pm.set_data`` to
      the same replicate (the production path in ``run_cc_grid.run_cell_cc``).

PASS = identical alpha median / CI / convergence flag (the lead's gate-1 lesson:
graph-construction differences can shift NUTS trajectories, so require the SWAP
path to be self-consistent and report any FRESH-vs-SWAP delta against the bias
thresholds rather than demanding bit-identity across different graphs).

Run (sapphire) — PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
    PYTENSOR_FLAGS=mode=FAST_RUN uv run python code/validate_cc_setdata.py

Author / Date — Claude Code (Fable 5) on Shawn's brief, 2026-06-11. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
sys.path.insert(0, str(RUN / "code"))
import joint_lib as J  # noqa: E402
import grid_lib as G  # noqa: E402
from run_cc_grid import (  # noqa: E402
    THETA_CONV_AB, THETA_GEN_AB, basis_for, fit_cc_on_model, monitored_vars,
)

TEST_REP = 3            # an arbitrary non-zero replicate (the swap path must move data)
TEST_CELL_ID = "conc_a0.4_gauss_inwin_N2800"   # confounded pilot cell


def fit_pair(mode: str) -> dict:
    """FRESH-vs-SWAP comparison for one arm; returns the two result dicts + deltas."""
    cell = next(c for c in G.enumerate_cells() if c["cell_id"] == TEST_CELL_ID)
    p_conv, p_gen = G.cell_shapes(cell)
    basis = basis_for(mode)
    var_names = monitored_vars(mode)
    data_seed = (G.BASE_SEED + cell["cell_index"]) * 1000 + TEST_REP
    fit_seed = data_seed + G.CC_FIT_SEED_OFFSET
    _y, y_al, y_non, k = G.generate_cc(cell, p_conv, p_gen, TEST_REP)

    # (a) FRESH: build with the test replicate's own data, sample without set_data.
    fresh_model = J.build_model_cross_classified(y_al, y_non, k, cell["N"], basis,
                                                 THETA_CONV_AB, THETA_GEN_AB,
                                                 pconv_mode=mode)
    fresh = fit_cc_on_model(fresh_model, y_al, y_non, k, fit_seed, var_names)

    # (b) SWAP: build with rep-0 placeholder data, set_data to the test replicate.
    _y0, y_al0, y_non0, k0 = G.generate_cc(cell, p_conv, p_gen, 0)
    swap_model = J.build_model_cross_classified(y_al0, y_non0, k0, cell["N"], basis,
                                                THETA_CONV_AB, THETA_GEN_AB,
                                                pconv_mode=mode)
    swap = fit_cc_on_model(swap_model, y_al, y_non, k, fit_seed, var_names)

    return {"mode": mode, "fresh": fresh, "swap": swap,
            "d_alpha_med": abs(fresh["alpha_med"] - swap["alpha_med"]),
            "d_alpha_lo": abs(fresh["alpha_lo"] - swap["alpha_lo"]),
            "d_alpha_hi": abs(fresh["alpha_hi"] - swap["alpha_hi"]),
            "conv_match": fresh["converged"] == swap["converged"]}


def main() -> None:
    """Run the gate for all three arms; write a JSON record and a PASS/FAIL line."""
    results = [fit_pair(m) for m in ("tiers3", "library", "free")]
    # Bit-identity is expected here (same graph structure both ways — unlike the
    # lead's gate 1, BOTH paths use shared-variable graphs); tolerate MC-trivial
    # deltas but flag anything within an order of magnitude of the bias gates.
    worst = max(max(r["d_alpha_med"], r["d_alpha_lo"], r["d_alpha_hi"]) for r in results)
    all_conv_match = all(r["conv_match"] for r in results)
    verdict = "PASS" if (worst < 0.012 and all_conv_match) else "FAIL"
    out = {"verdict": verdict, "worst_abs_delta": worst,
           "conv_flags_match": all_conv_match, "cell": TEST_CELL_ID, "rep": TEST_REP,
           "results": results}
    (RUN / "outputs" / "cc-setdata-validation.json").write_text(json.dumps(out, indent=1))
    for r in results:
        print(f"[{r['mode']:8s}] fresh α={r['fresh']['alpha_med']:.4f} "
              f"swap α={r['swap']['alpha_med']:.4f} dmed={r['d_alpha_med']:.2e} "
              f"conv_match={r['conv_match']}")
    print(f"{verdict}: worst |delta| {worst:.3e} "
          f"(gate 0.012 = 1/10th of the C1 bias bar); conv flags match: {all_conv_match}")
    if verdict == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
