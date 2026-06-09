#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poc_kappa_check.py — does widening the θ prior fix the marginal high-α coverage?
================================================================================

Option 2 (Shawn 2026-06-09): keep the per-unit + classification design but WIDEN the θ
prior from κ=40 to κ≈12, so the θ-calibration scatter (RMSE 0.12 across identifiable
units) is propagated into the α credible interval. The POC's estimated-basis run
(`poc_estimated_basis.py`) had a small positive bias (+0.09 to +0.12) and *marginal*
95 % coverage at the two high-α confounded cells (CIs too tight because θ was treated as
near-known at κ=40). This script re-fits those cells (+ controls) at κ ∈ {12, 20, 40} on
the production-realistic ESTIMATED (contaminated aligned-subset) basis and reports α
median, 95 % CI, and coverage, to confirm κ≈12 widens the CI enough to cover truth
without harming the point estimate.

Run — PATH=~/.local/bin:$PATH PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False \
       uv run python code/poc_kappa_check.py

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
import poc_recovery as P  # noqa: E402
from poc_estimated_basis import estimated_conv_shape  # noqa: E402

KAPPAS = (12.0, 20.0, 40.0)
THETA_CONV_TRUE, THETA_GEN_TRUE = 0.95, 0.15
# focus cells: the two marginal-coverage confounded ones + one passing + one identifiable
FOCUS = {"conf_a0.2", "conf_a0.4", "conf_a0.6", "ident_a0.6"}


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


def main() -> None:
    cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())
    c = cal["calibration"]["C"]
    cells = {cell["id"]: (i, cell) for i, cell in enumerate(P.make_cells())}

    results = []
    print("θ-prior κ sweep on the ESTIMATED (contaminated) basis; CI width + coverage:\n")
    print(f"{'cell':16s} {'aT':4s} {'kappa':5s} | {'alpha_med':9s} {'ci_width':8s} {'cover95':7s}")
    for cid in [x for x in cells if x in FOCUS]:
        i, cell = cells[cid]
        seed = P.BASE_SEED + i
        y, k = P.generate(cell, seed, THETA_CONV_TRUE, THETA_GEN_TRUE)
        est = estimated_conv_shape(cell, THETA_CONV_TRUE, THETA_GEN_TRUE)
        basis = P.per_unit_basis(est)
        for kap in KAPPAS:
            tc_ab = J.beta_from_mean_concentration(c["theta_conv"], kap)
            tg_ab = J.beta_from_mean_concentration(c["theta_gen"], kap)
            r = fit_alpha(J.build_model_joint(y, k, P.N, basis, tc_ab, tg_ab), seed + int(kap))
            cov = r["alpha_lo"] <= cell["alpha"] <= r["alpha_hi"]
            width = r["alpha_hi"] - r["alpha_lo"]
            results.append(dict(cell=cid, alpha_true=cell["alpha"], kappa=kap,
                                **r, ci_width=width, cover95=cov))
            print(f"{cid:16s} {cell['alpha']:<4.1f} {kap:<5.0f} | "
                  f"{r['alpha_med']:.2f}[{r['alpha_lo']:.2f},{r['alpha_hi']:.2f}] "
                  f"{width:<8.2f} {str(cov):7s}")
        print()

    (RUN / "outputs" / "poc-kappa-check.json").write_text(json.dumps(
        dict(generated="2026-06-09", basis="estimated (contaminated) aligned-subset",
             kappas=list(KAPPAS), results=results), indent=2))
    print(f"Wrote {RUN / 'outputs' / 'poc-kappa-check.json'}")


if __name__ == "__main__":
    main()
