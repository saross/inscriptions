#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poc_recovery.py — LOCAL recovery proof-of-concept for the joint model.
======================================================================

A small, fast, local de-risking run BEFORE proposing the full sapphire recovery
grid (spec ``runs/2026-06-09-joint-identifiability/spec.md`` §8.3). It generates a
handful of synthetic cells under the WELL-SPECIFIED generative model (realistic
broad-slab convention, NOT a narrow Gaussian) and asks the two primary questions:

  * **Identifiable regime** — does the joint model recover α UNCHANGED where the
    shared-basis temporal fit already identifies it (criterion 1: do no harm)?
  * **Confounded regime** — does the joint model pull α toward truth, between the
    under-attributing shared baseline and the over-attributing per-unit basis
    (criterion 2: pulled toward truth, no overshoot)?

For each cell it fits THREE models on the SAME (y, k): shared-basis baseline
(``build_model_f1_f3``, temporal only), per-unit-basis baseline (the over-attribution
upper bound), and the joint model. α posterior medians + 95 % CIs are compared to
α_true.

This is a PROOF-OF-CONCEPT (one replicate per cell, reduced cell set, local). The
full grid (many replicates, full axes, θ-mismatch + κ-sensitivity arms) runs on
sapphire after sign-off.

Run
---
    PATH=/home/shawn/.local/bin:$PATH uv run python code/poc_recovery.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-09. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
DESIGN = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign/design.json"
)
CELL_LIB_DIR = (
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
    "/revalidation/code"
)
sys.path.insert(0, str(RUN / "code"))
sys.path.insert(0, CELL_LIB_DIR)
import joint_lib as J  # noqa: E402
import cell_lib as cl  # noqa: E402  (the recovery-validated build_model_f1_f3)

# Sampler config (POC: cores=4 to parallelise the 4 chains locally).
DRAWS, TUNE, CHAINS, CORES, TACC = 1500, 1000, 4, 4, 0.95
N = 2000                    # frontier-province scale
BASE_SEED = 20260609

BINC = J.BIN_CENTRES
WIN = (BINC >= 100) & (BINC <= 300)


def pct_win(spa: np.ndarray) -> float:
    return float(spa[WIN].sum() / spa.sum())


def centroid(spa: np.ndarray) -> float:
    return float((spa * BINC).sum() / spa.sum())


# --------------------------------------------------------------------------- #
# Cell library (realistic).                                                     #
# --------------------------------------------------------------------------- #
def make_cells() -> list[dict]:
    """Identifiable (broad convention, separated genuine) + confounded
    (period-concentrated convention AND genuine, same AD 100–300 window)."""
    conv_broad = J.slab_mixture_spa([(1, 300), (1, 200), (50, 250), (1, 250)])
    conv_conc = J.slab_mixture_spa([(101, 300), (151, 300), (101, 250), (101, 200)])
    gen_early = J.gaussian_pgen(80, 45)        # peaked early — separated from convention
    gen_inwin = J.gaussian_pgen(200, 40)       # peaked inside the occupation window
    gen_regnal = J.regnal_cluster_pgen([165, 200, 235], sigma=12.0)  # hard corner

    cells = [
        # identifiable: broad convention, genuine separated → α identified by temporal
        dict(id="ident_a0.3", regime="identifiable", alpha=0.3,
             p_conv=conv_broad, p_gen=gen_early),
        dict(id="ident_a0.6", regime="identifiable", alpha=0.6,
             p_conv=conv_broad, p_gen=gen_early),
        # confounded: concentrated convention + genuine in same window
        dict(id="conf_a0.2", regime="confounded", alpha=0.2,
             p_conv=conv_conc, p_gen=gen_inwin),
        dict(id="conf_a0.4", regime="confounded", alpha=0.4,
             p_conv=conv_conc, p_gen=gen_inwin),
        dict(id="conf_a0.6", regime="confounded", alpha=0.6,
             p_conv=conv_conc, p_gen=gen_inwin),
        # confounded + hard genuine corner (regnal cluster)
        dict(id="conf_regnal_a0.5", regime="confounded", alpha=0.5,
             p_conv=conv_conc, p_gen=gen_regnal),
    ]
    return cells


def generate(cell: dict, seed: int, theta_conv_true: float, theta_gen_true: float):
    """Well-specified generative draw: y ~ Multinomial, k ~ Binomial (spec §5 Tier 1)."""
    rng = np.random.default_rng(seed)
    p_mix = cell["alpha"] * cell["p_conv"] + (1.0 - cell["alpha"]) * cell["p_gen"]
    p_mix = p_mix / p_mix.sum()
    y = rng.multinomial(N, p_mix)
    pi = cell["alpha"] * theta_conv_true + (1.0 - cell["alpha"]) * theta_gen_true
    k = int(rng.binomial(N, pi))
    return y, k


def fit_alpha(model, seed: int) -> dict:
    import pymc as pm
    import arviz as az
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=DRAWS, tune=TUNE, chains=CHAINS, cores=CORES,
                              target_accept=TACC, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
    a = idata.posterior["alpha"].values.reshape(-1)
    summ = az.summary(idata, var_names=["alpha"], round_to="none")
    return dict(alpha_med=float(np.median(a)),
                alpha_lo=float(np.percentile(a, 2.5)),
                alpha_hi=float(np.percentile(a, 97.5)),
                max_rhat=float(summ["r_hat"].max()),
                min_ess=float(summ["ess_bulk"].min()))


def per_unit_basis(p_conv_true: np.ndarray) -> np.ndarray:
    """3-row 'per-unit' basis bracketing the true convention shape (the
    over-attribution upper-bound reference; cf. the diagnostic's per-unit refit).
    Rows: true convention and ±15 y shifts, each renormalised."""
    def shift(v, by_bins):
        out = np.roll(v, by_bins)
        if by_bins > 0:
            out[:by_bins] = 0
        elif by_bins < 0:
            out[by_bins:] = 0
        return out / out.sum()
    rows = np.vstack([p_conv_true, shift(p_conv_true, 3), shift(p_conv_true, -3)])
    return rows / rows.sum(axis=1, keepdims=True)


def main() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    latin_basis = np.asarray(design["tier_basis_empirical_latin"], dtype=float)

    cal = json.loads((RUN / "outputs" / "theta-calibration.json").read_text())
    c = cal["calibration"]["C"]
    theta_conv_ab = J.beta_from_mean_concentration(c["theta_conv"], 40.0)
    theta_gen_ab = J.beta_from_mean_concentration(c["theta_gen"], 40.0)
    # generation truth: the field truth the priors are meant to approximate
    THETA_CONV_TRUE, THETA_GEN_TRUE = 0.95, 0.15

    cells = make_cells()
    results = []
    print(f"POC: N={N}, draws={DRAWS}, θ priors C (conv μ={c['theta_conv']}, "
          f"gen μ={c['theta_gen']}, κ=40); gen-truth θ=({THETA_CONV_TRUE},{THETA_GEN_TRUE})\n")
    print(f"{'cell':18s} {'reg':12s} {'aT':4s} {'c%win':5s} {'g%win':5s} {'k/N':5s} | "
          f"{'shared':14s} {'perunit':14s} {'JOINT':16s}")

    for i, cell in enumerate(cells):
        seed = BASE_SEED + i
        y, k = generate(cell, seed, THETA_CONV_TRUE, THETA_GEN_TRUE)

        r_shared = fit_alpha(cl.build_model_f1_f3(y, latin_basis), seed + 1)
        r_perunit = fit_alpha(cl.build_model_f1_f3(y, per_unit_basis(cell["p_conv"])), seed + 2)
        r_joint = fit_alpha(
            J.build_model_joint(y, k, N, latin_basis, theta_conv_ab, theta_gen_ab),
            seed + 3)

        row = dict(
            cell=cell["id"], regime=cell["regime"], alpha_true=cell["alpha"],
            conv_pct_win=round(pct_win(cell["p_conv"]), 3),
            gen_pct_win=round(pct_win(cell["p_gen"]), 3),
            k=k, k_frac=round(k / N, 3),
            shared=r_shared, perunit=r_perunit, joint=r_joint,
        )
        results.append(row)
        print(f"{cell['id']:18s} {cell['regime']:12s} {cell['alpha']:<4.1f} "
              f"{row['conv_pct_win']:<5.2f} {row['gen_pct_win']:<5.2f} {row['k_frac']:<5.2f} | "
              f"{r_shared['alpha_med']:.2f}[{r_shared['alpha_lo']:.2f},{r_shared['alpha_hi']:.2f}] "
              f"{r_perunit['alpha_med']:.2f}[{r_perunit['alpha_lo']:.2f},{r_perunit['alpha_hi']:.2f}] "
              f"{r_joint['alpha_med']:.2f}[{r_joint['alpha_lo']:.2f},{r_joint['alpha_hi']:.2f}]")

    out = dict(generated="2026-06-09", config=dict(N=N, draws=DRAWS, tune=TUNE,
               chains=CHAINS, target_accept=TACC, theta_prior_kappa=40,
               theta_conv_true=THETA_CONV_TRUE, theta_gen_true=THETA_GEN_TRUE),
               results=results)
    (RUN / "outputs" / "poc-recovery.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {RUN / 'outputs' / 'poc-recovery.json'}")

    # Verdict against criteria 1–2.
    print("\n--- verdict (criteria 1–2) ---")
    LoA = 0.18
    for r in results:
        aT = r["alpha_true"]
        jb = r["joint"]["alpha_med"] - aT
        sb = r["shared"]["alpha_med"] - aT
        cov = r["joint"]["alpha_lo"] <= aT <= r["joint"]["alpha_hi"]
        if r["regime"] == "identifiable":
            ok = abs(jb) < LoA
            print(f"  {r['cell']:18s} [ident]  joint bias {jb:+.2f}  cover95 {cov}  "
                  f"{'PASS' if ok else 'CHECK'} (do-no-harm)")
        else:
            improved = abs(jb) < abs(sb) - 0.05
            ok = (abs(jb) < LoA) and (jb < 0.12)
            print(f"  {r['cell']:18s} [conf ]  shared bias {sb:+.2f} → joint bias {jb:+.2f}  "
                  f"cover95 {cov}  improved {improved}  {'PASS' if ok else 'CHECK'}")


if __name__ == "__main__":
    main()
