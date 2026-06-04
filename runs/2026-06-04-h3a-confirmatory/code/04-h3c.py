#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04-h3c.py --- Step 5 of the H3a confirmatory run: H3c residual spatial
autocorrelation (Hanson 2021 replication).

From the PRIMARY H3a posterior:
  - extract per-city Pearson residuals (prereg §3 H3c definition);
  - build k-NN row-standardised spatial weights (libpysal) at k = 5, 8, 10;
  - run conditional permutation inference (999 perms) on the POSTERIOR-MEAN
    residual vector per k (esda Moran);
  - report the POSTERIOR DISTRIBUTION of Moran's I per k (2.5/50/97.5 pct):
    for each posterior draw s compute I_s on r_.,s.
Confirmatory rule: Moran's I > 0 at p < 0.05 in >= 2 of {5, 8, 10}.
Three-case interpretive guardrail at primary k = 8 (prereg §3 lines 273-277).

Inputs
------
runs/2026-06-04-h3a-confirmatory/outputs/idata-primary.nc
data/processed/city_level_for_h3a.parquet

Outputs
-------
runs/2026-06-04-h3a-confirmatory/outputs/h3c-results.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-04, blind-run brief.
"""

from __future__ import annotations

import json
import sys
import warnings

import arviz as az
import numpy as np
import pandas as pd
from libpysal.weights import KNN
from esda.moran import Moran

import h3a_common as H

warnings.filterwarnings("ignore")

K_VALUES = [5, 8, 10]
PRIMARY_K = 8
N_PERMUTATIONS = 999
N_POSTERIOR_I_DRAWS = 2_000   # draws used for the posterior I distribution
RANDOM_SEED = 20_260_604


def pearson_resids_all_draws(idata: az.InferenceData,
                             y: np.ndarray) -> np.ndarray:
    """Return (S, C) Pearson residuals across all posterior draws."""
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    alpha = post["dispersion"].values.reshape(-1)
    mu = np.exp(log_mu)
    var = mu + mu ** 2 / alpha[:, None]
    return (y[None, :] - mu) / np.sqrt(var)


def main() -> int:
    out_dir = H.RUN_DIR / "outputs"
    idata = az.from_netcdf(str(out_dir / "idata-primary.nc"))
    cities = pd.read_parquet(H.PRIMARY_PARQUET)
    y = cities["inscription_count"].to_numpy(dtype=float)
    coords = cities[["longitude", "latitude"]].to_numpy(dtype=float)

    r_all = pearson_resids_all_draws(idata, y)     # (S, C)
    r_mean = r_all.mean(axis=0)                     # posterior-mean residual
    print(f"[04-h3c] residuals: {r_all.shape[0]} draws x {r_all.shape[1]} cities")

    rng = np.random.default_rng(RANDOM_SEED)
    sub_idx = rng.choice(r_all.shape[0],
                         size=min(N_POSTERIOR_I_DRAWS, r_all.shape[0]),
                         replace=False)

    per_k = {}
    n_pass = 0
    for k in K_VALUES:
        w = KNN.from_array(coords, k=k)
        w.transform = "r"
        # Conditional permutation inference on the posterior-mean residual.
        mi = Moran(r_mean, w, permutations=N_PERMUTATIONS, two_tailed=False)
        I_obs = float(mi.I)
        p_sim = float(mi.p_sim)        # one-sided (greater) permutation p
        z_sim = float(mi.z_sim)
        passes = (I_obs > 0) and (p_sim < 0.05)
        if passes:
            n_pass += 1

        # Posterior distribution of Moran's I.
        I_draws = np.empty(len(sub_idx))
        for i, s in enumerate(sub_idx):
            I_draws[i] = Moran(r_all[s], w, permutations=0,
                               two_tailed=False).I
        I_lo, I_med, I_hi = (float(x) for x in
                             np.percentile(I_draws, [2.5, 50, 97.5]))
        frac_above0 = float((I_draws > 0).mean())

        per_k[str(k)] = {
            "moran_I_posterior_mean_resid": I_obs,
            "p_sim_one_sided": p_sim,
            "z_sim": z_sim,
            "expected_I": float(mi.EI),
            "passes_rule": passes,
            "posterior_I_2.5pct": I_lo,
            "posterior_I_50pct": I_med,
            "posterior_I_97.5pct": I_hi,
            "posterior_frac_above_0": frac_above0,
        }
        print(f"[04-h3c] k={k:>2}: I={I_obs:+.4f} p_sim={p_sim:.4f} "
              f"z={z_sim:+.3f} pass={passes} | posterior I "
              f"[{I_lo:+.4f}, {I_med:+.4f}, {I_hi:+.4f}] "
              f"frac>0={frac_above0:.3f}")

    confirmatory_pass = n_pass >= 2
    verdict = "supported" if confirmatory_pass else "not-supported"

    # Three-case interpretive guardrail at primary k = 8.
    k8 = per_k[str(PRIMARY_K)]
    frac8 = k8["posterior_frac_above_0"]
    ci8_crosses_zero = (k8["posterior_I_2.5pct"] < 0 < k8["posterior_I_97.5pct"])
    if confirmatory_pass and frac8 >= 0.95:
        case = "Case 1 -- clean replication (rule passes; >=95% of k=8 draws above 0)"
    elif confirmatory_pass and ci8_crosses_zero:
        case = ("Case 2 -- permutation-significant but posterior-sensitive "
                "(rule passes; 95% posterior interval of I_s at k=8 crosses 0)")
    elif confirmatory_pass and frac8 < 0.50:
        case = ("Case 3 -- confirmatory rule passes without substantive support "
                "(rule passes; <50% of k=8 draws above 0)")
    elif confirmatory_pass:
        case = ("rule passes; k=8 posterior 50-95% above 0 and CI does not "
                "straddle 0 -- between Case 1 and Case 2, reported with reasoning")
    else:
        case = "confirmatory rule does NOT pass (<2 of {5,8,10} significant)"

    result = {
        "confirmatory_rule": "Moran's I > 0 at p < 0.05 in >= 2 of {5, 8, 10}",
        "n_k_passing": n_pass,
        "verdict": verdict,
        "interpretive_case_k8": case,
        "primary_k": PRIMARY_K,
        "n_permutations": N_PERMUTATIONS,
        "n_posterior_I_draws": int(len(sub_idx)),
        "per_k": per_k,
        "hanson_2021_reference": {
            "residual_moran_I": 0.046, "z": 4.571, "p": "<0.0001",
            "raw_count_moran_I": -0.006,
        },
    }
    (out_dir / "h3c-results.json").write_text(json.dumps(result, indent=2))
    print(f"[04-h3c] verdict: {verdict} ({n_pass}/3 k-values pass)")
    print(f"[04-h3c] interpretive case (k=8): {case}")
    print(f"[04-h3c]   -> {out_dir / 'h3c-results.json'}")
    print("[04-h3c] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
