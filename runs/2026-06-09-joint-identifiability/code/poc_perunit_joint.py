#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poc_perunit_joint.py — decisive variant: FLEXIBLE convention shape + classification.
====================================================================================

``poc_recovery.py`` showed the LEAD design (shared broad basis + classification term)
FAILS for confounded cells: with the shared basis too broad, the temporal multinomial
is *confidently wrong* (it rejects α>0 because convention mass would leak outside the
data window) and overpowers the classification binomial — joint α stays ≈ 0. The
per-unit basis (temporal only) instead recovers α but OVER-attributes (absorbs genuine).

This script tests the design the POC pointed to: give the convention component the
SHAPE freedom of a per-unit basis (so the temporal term becomes permissive in α — the
under-identification), and add the classification binomial to PIN α against the
per-unit basis's over-attribution. Per cell it fits:

  * ``perunit_only``  — ``build_model_f1_f3`` with the per-unit basis (over-attribution
    reference);
  * ``perunit_joint`` — ``build_model_joint`` with the per-unit basis + classification
    (the candidate fix).

The per-unit basis here is built from the cell's TRUE convention shape (the idealised
"perfect convention-shape estimate" case). In production the shape would be estimated
from the unit's grid-aligned-inscription subset SPA; the interval-level synthetic tier
will test that. Cells, seeds, N, and θ priors are identical to ``poc_recovery.py`` for
direct comparability.

Run — PATH=~/.local/bin:$PATH PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False \
       uv run python code/poc_perunit_joint.py

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
import poc_recovery as P  # noqa: E402  (reuse make_cells / generate / per_unit_basis / config)


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
    return dict(alpha_med=float(np.median(a)),
                alpha_lo=float(np.percentile(a, 2.5)),
                alpha_hi=float(np.percentile(a, 97.5)),
                max_rhat=float(summ["r_hat"].max()),
                min_ess=float(summ["ess_bulk"].min()))


def main() -> None:
    cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())
    c = cal["calibration"]["C"]
    theta_conv_ab = J.beta_from_mean_concentration(c["theta_conv"], 40.0)
    theta_gen_ab = J.beta_from_mean_concentration(c["theta_gen"], 40.0)
    THETA_CONV_TRUE, THETA_GEN_TRUE = 0.95, 0.15

    cells = P.make_cells()
    results = []
    print(f"PERUNIT-JOINT variant: N={P.N}, draws={P.DRAWS}, θ priors C κ=40\n")
    print(f"{'cell':18s} {'reg':12s} {'aT':4s} {'k/N':5s} | "
          f"{'perunit_only':16s} {'perunit_JOINT':16s}")
    for i, cell in enumerate(cells):
        seed = P.BASE_SEED + i
        y, k = P.generate(cell, seed, THETA_CONV_TRUE, THETA_GEN_TRUE)
        pub = P.per_unit_basis(cell["p_conv"])
        r_po = fit_alpha(cl.build_model_f1_f3(y, pub), seed + 4)
        r_pj = fit_alpha(J.build_model_joint(y, k, P.N, pub, theta_conv_ab, theta_gen_ab),
                         seed + 5)
        results.append(dict(cell=cell["id"], regime=cell["regime"], alpha_true=cell["alpha"],
                            k_frac=round(k / P.N, 3), perunit_only=r_po, perunit_joint=r_pj))
        print(f"{cell['id']:18s} {cell['regime']:12s} {cell['alpha']:<4.1f} {k/P.N:<5.2f} | "
              f"{r_po['alpha_med']:.2f}[{r_po['alpha_lo']:.2f},{r_po['alpha_hi']:.2f}]  "
              f"{r_pj['alpha_med']:.2f}[{r_pj['alpha_lo']:.2f},{r_pj['alpha_hi']:.2f}]")

    (RUN / "outputs" / "poc-perunit-joint.json").write_text(json.dumps(
        dict(generated="2026-06-09",
             config=dict(N=P.N, draws=P.DRAWS, theta_prior_kappa=40,
                         theta_conv_true=THETA_CONV_TRUE, theta_gen_true=THETA_GEN_TRUE,
                         per_unit_basis="true convention shape (idealised estimate)"),
             results=results), indent=2))

    print("\n--- verdict: per-unit shape + classification ---")
    LoA = 0.18
    for r in results:
        aT = r["alpha_true"]
        po = r["perunit_only"]["alpha_med"] - aT
        pj = r["perunit_joint"]["alpha_med"] - aT
        cov = r["perunit_joint"]["alpha_lo"] <= aT <= r["perunit_joint"]["alpha_hi"]
        tag = "ident" if r["regime"] == "identifiable" else "conf "
        ok = abs(pj) < LoA
        print(f"  {r['cell']:18s} [{tag}]  perunit_only bias {po:+.2f} → "
              f"perunit_JOINT bias {pj:+.2f}  cover95 {cov}  {'PASS' if ok else 'CHECK'}")
    print(f"\nWrote {RUN / 'outputs' / 'poc-perunit-joint.json'}")


if __name__ == "__main__":
    main()
