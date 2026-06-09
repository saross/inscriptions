#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poc_estimated_basis.py — does per-unit-JOINT survive a REALISTIC (estimated) shape?
===================================================================================

``poc_perunit_joint.py`` showed that a flexible per-unit convention basis + the
classification binomial recovers α — but it used the cell's TRUE convention shape,
which is not observable in production. The observable analogue is the aoristic SPA of
the unit's GRID-ALIGNED inscription subset. That subset is contaminated: aligned
inscriptions are convention-class with rate θ_conv AND genuine-class with rate θ_gen,
so in expectation::

    aligned_subset_spa  ∝  α·θ_conv·p_conv  +  (1−α)·θ_gen·p_gen

This script builds the per-unit basis from that EXPECTED contaminated shape (the
realistic estimate) and re-fits ``build_model_joint``. If α still recovers, the design
is production-ready (modulo the full grid); if not, the convention shape must be handled
at the interval level (a finding for the full-grid spec).

Cells, seeds, N, θ priors identical to ``poc_recovery.py``.

Run — PATH=~/.local/bin:$PATH PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False \
       uv run python code/poc_estimated_basis.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
CELL_LIB_DIR = (
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
    "/revalidation/code"
)
sys.path.insert(0, str(RUN / "code"))
sys.path.insert(0, CELL_LIB_DIR)
import joint_lib as J  # noqa: E402
import cell_lib as cl  # noqa: E402
import poc_recovery as P  # noqa: E402


def fit_alpha(model, seed: int) -> dict:
    import pymc as pm
    import arviz as az
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=P.DRAWS, tune=P.TUNE, chains=P.CHAINS, cores=P.CORES,
                              target_accept=P.TACC, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    a = idata.posterior["alpha"].values.reshape(-1)
    summ = az.summary(idata, var_names=["alpha"], round_to="none")
    return dict(alpha_med=float(np.median(a)), alpha_lo=float(np.percentile(a, 2.5)),
                alpha_hi=float(np.percentile(a, 97.5)), max_rhat=float(summ["r_hat"].max()),
                min_ess=float(summ["ess_bulk"].min()))


def estimated_conv_shape(cell: dict, theta_conv_true: float, theta_gen_true: float) -> np.ndarray:
    """Expected aoristic SPA of the grid-aligned subset (the observable convention-shape
    estimate), contaminated by genuine inscriptions that happen to be aligned."""
    a = cell["alpha"]
    mix = a * theta_conv_true * cell["p_conv"] + (1.0 - a) * theta_gen_true * cell["p_gen"]
    return mix / mix.sum()


def main() -> None:
    cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())
    c = cal["calibration"]["C"]
    theta_conv_ab = J.beta_from_mean_concentration(c["theta_conv"], 40.0)
    theta_gen_ab = J.beta_from_mean_concentration(c["theta_gen"], 40.0)
    THETA_CONV_TRUE, THETA_GEN_TRUE = 0.95, 0.15

    cells = P.make_cells()
    results = []
    print(f"ESTIMATED-BASIS variant (aligned-subset shape): N={P.N}, draws={P.DRAWS}\n")
    print(f"{'cell':18s} {'reg':12s} {'aT':4s} {'k/N':5s} | {'perunit_JOINT(est)':20s}")
    for i, cell in enumerate(cells):
        seed = P.BASE_SEED + i
        y, k = P.generate(cell, seed, THETA_CONV_TRUE, THETA_GEN_TRUE)
        est = estimated_conv_shape(cell, THETA_CONV_TRUE, THETA_GEN_TRUE)
        basis = P.per_unit_basis(est)
        r = fit_alpha(J.build_model_joint(y, k, P.N, basis, theta_conv_ab, theta_gen_ab),
                      seed + 6)
        results.append(dict(cell=cell["id"], regime=cell["regime"], alpha_true=cell["alpha"],
                            k_frac=round(k / P.N, 3), perunit_joint_est=r))
        print(f"{cell['id']:18s} {cell['regime']:12s} {cell['alpha']:<4.1f} {k/P.N:<5.2f} | "
              f"{r['alpha_med']:.2f}[{r['alpha_lo']:.2f},{r['alpha_hi']:.2f}]")

    (RUN / "outputs" / "poc-estimated-basis.json").write_text(json.dumps(
        dict(generated="2026-06-09",
             config=dict(N=P.N, draws=P.DRAWS, theta_prior_kappa=40,
                         theta_conv_true=THETA_CONV_TRUE, theta_gen_true=THETA_GEN_TRUE,
                         per_unit_basis="EXPECTED aligned-subset shape (contaminated, observable)"),
             results=results), indent=2))

    print("\n--- verdict: estimated (aligned-subset) shape + classification ---")
    LoA = 0.18
    for r in results:
        aT = r["alpha_true"]; e = r["perunit_joint_est"]
        bias = e["alpha_med"] - aT
        cov = e["alpha_lo"] <= aT <= e["alpha_hi"]
        tag = "ident" if r["regime"] == "identifiable" else "conf "
        print(f"  {r['cell']:18s} [{tag}]  bias {bias:+.2f}  cover95 {cov}  "
              f"{'PASS' if abs(bias) < LoA else 'CHECK'}")
    print(f"\nWrote {RUN / 'outputs' / 'poc-estimated-basis.json'}")


if __name__ == "__main__":
    main()
