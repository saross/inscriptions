#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03-ppc.py --- Step 3 of the H9 letter-mass H3a confirmatory run: the
posterior-predictive check suite.

Runs the SAME TEN checks pinned in the H3a design artefact
(planning/h3a-design-artefact-2026-06-04.md §2-§5; mirrored from
runs/2026-06-04-h3a-confirmatory/code/03-ppc.py) against the H9 PRIMARY (Latin)
letter-mass posterior, with the two-tier severity adjudication (§6). A CRITICAL
trigger is reported and HALTs (no improvised model revision); a MINOR trigger is
logged as a caveat. Only the response variable (per-city letter mass) and the
input/posterior paths change relative to the H3a template.

The ten checks (response = per-city LETTER MASS):
  1  proportion of zeros            (pp prop-zeros <= 0.02; abs critical 0.10)
  2  mean response                  (within +-10% of observed)
  3  SD of responses                (within +-25% of observed)
  4  95th percentile                (obs<=tail_count_bound AND pp within +-30%)
  5  mean-variance ratio            (pp ratio within [0.5x, 2x] of observed)
  6  Bayesian p-values for #2-#5    (0.05 <= p_B <= 0.95)
  7  residual-vs-fitted slope       (|slope| < 0.10)
  8  residual-vs-within-logpop slope(|slope| < 0.10)
  9  province residual dispersion   (per-province mean|r| in [0.5x,2x]; n>=5)
  10 posterior-predictive Moran's I (obs in 5th-95th pct of pp distribution)

Inputs
------
runs/2026-06-18-h9-letter-mass-h3a/outputs/idata-latin-primary.nc
runs/2026-06-18-h9-letter-mass-h3a/data/processed/city_level_for_h9_latin.parquet
runs/2026-06-18-h9-letter-mass-h3a/outputs/prior-predictive-thresholds.json

Outputs
-------
runs/2026-06-18-h9-letter-mass-h3a/outputs/ppc-results.json

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-18, H9 build brief
(BUILD-AND-COMMIT-ONLY; no fit run).
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

import h9_common as H

warnings.filterwarnings("ignore")

PRIMARY_K = 8           # k-NN for the posterior-predictive Moran's I (design §5)
N_PP_DRAWS = 1_000      # posterior-predictive replicate draws
RANDOM_SEED = 20_260_618  # H9 confirmatory-run seed.

# H9 PRIMARY frame + response.
PRIMARY_PARQUET = H.LATIN_PARQUET
RESPONSE_COL = "letter_mass"
IDATA_PRIMARY = "idata-latin-primary.nc"


def severity(value: float, bound_magnitude: float, in_band: bool,
             abs_zeros: bool = False, abs_critical: float = 0.10) -> str:
    """Two-tier severity (design artefact §6). Identical to the H3a template.

    `value` is the absolute distance outside the bound (0 if in band). Critical:
    outside by > 2x bound magnitude. Minor: outside by <= 1.5x. Grey zone
    [1.5x, 2x]: flagged 'grey'. For proportion-of-zeros, an ABSOLUTE 0.10
    critical cutoff.
    """
    if in_band:
        return "pass"
    if abs_zeros:
        return "critical" if value > abs_critical else "minor"
    ratio = value / bound_magnitude if bound_magnitude > 0 else float("inf")
    if ratio > 2.0:
        return "critical"
    if ratio <= 1.5:
        return "minor"
    return "grey"


def posterior_predict(idata: az.InferenceData, n_draws: int,
                      rng: np.random.Generator) -> np.ndarray:
    """Draw y_rep (n_draws, C) from the posterior predictive of the NBR.
    Identical to the H3a template (the response is per-city letter mass)."""
    post = idata.posterior
    log_mu = post["log_mu"].values.reshape(-1, post.sizes["log_mu_dim_0"]
                                           if "log_mu_dim_0" in post.dims
                                           else post["log_mu"].shape[-1])
    alpha = post["dispersion"].values.reshape(-1)
    total = log_mu.shape[0]
    idx = rng.choice(total, size=min(n_draws, total), replace=False)
    yrep = np.empty((len(idx), log_mu.shape[1]), dtype=np.int64)
    for i, s in enumerate(idx):
        mu = np.exp(np.clip(log_mu[s], -50, 50))
        a = max(alpha[s], 1e-6)
        p = np.clip(a / (a + mu), 1e-12, 1 - 1e-12)
        yrep[i] = rng.negative_binomial(a, p)
    return yrep


def pearson_resid_posterior_mean(idata: az.InferenceData,
                                 y: np.ndarray) -> np.ndarray:
    """Posterior-mean Pearson residual vector r_c = (1/S) sum_s r_c,s.
    Identical to the H3a template."""
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    alpha = post["dispersion"].values.reshape(-1)
    mu = np.exp(log_mu)
    var = mu + mu ** 2 / alpha[:, None]
    r = (y[None, :] - mu) / np.sqrt(var)
    return r.mean(axis=0)


def main() -> int:
    out_dir = H.RUN_DIR / "outputs"
    idata = az.from_netcdf(str(out_dir / IDATA_PRIMARY))
    cities = pd.read_parquet(PRIMARY_PARQUET)
    y = cities[RESPONSE_COL].to_numpy(dtype=float)
    thresholds = json.loads(
        (out_dir / "prior-predictive-thresholds.json").read_text())
    tail_count_bound = float(thresholds["tail_count_bound"])

    rng = np.random.default_rng(RANDOM_SEED)
    yrep = posterior_predict(idata, N_PP_DRAWS, rng)  # (S, C)
    print(f"[03-ppc] posterior-predictive: {yrep.shape[0]} draws x "
          f"{yrep.shape[1]} cities (response = {RESPONSE_COL})")

    obs_mean = float(y.mean())
    obs_sd = float(y.std(ddof=0))
    obs_q95 = float(np.percentile(y, 95))
    obs_mvr = float(y.mean() / y.var(ddof=0))
    obs_propzero = float((y == 0).mean())

    rep_mean = yrep.mean(axis=1)
    rep_sd = yrep.std(axis=1, ddof=0)
    rep_q95 = np.percentile(yrep, 95, axis=1)
    rep_var = yrep.var(axis=1, ddof=0)
    rep_mvr = rep_mean / rep_var
    rep_propzero = (yrep == 0).mean(axis=1)

    def p_bayes(rep, obs):
        return float((rep >= obs).mean())

    checks = []

    # --- Check 1: proportion of zeros (absolute critical 0.10) ----------
    pp_propzero_mean = float(rep_propzero.mean())
    bound1 = 0.02
    dist1 = max(0.0, pp_propzero_mean - bound1)
    in1 = pp_propzero_mean <= bound1
    checks.append({
        "id": 1, "name": "proportion of zeros",
        "observed": obs_propzero, "pp_mean": pp_propzero_mean,
        "bound": "pp prop-zeros <= 0.02 (abs critical 0.10)",
        "severity": severity(dist1, bound1, in1, abs_zeros=True),
    })

    # --- Check 2: mean (within +-10%) -----------------------------------
    pp_mean = float(rep_mean.mean())
    rel2 = abs(pp_mean - obs_mean) / obs_mean
    in2 = rel2 <= 0.10
    checks.append({
        "id": 2, "name": "mean response",
        "observed": obs_mean, "pp_mean": pp_mean, "rel_dev": rel2,
        "bound": "within +-10% of observed",
        "severity": severity(rel2 - 0.10 if not in2 else 0.0, 0.10, in2),
        "p_bayes": p_bayes(rep_mean, obs_mean),
    })

    # --- Check 3: SD (within +-25%) -------------------------------------
    pp_sd = float(rep_sd.mean())
    rel3 = abs(pp_sd - obs_sd) / obs_sd
    in3 = rel3 <= 0.25
    checks.append({
        "id": 3, "name": "SD of responses",
        "observed": obs_sd, "pp_mean": pp_sd, "rel_dev": rel3,
        "bound": "within +-25% of observed",
        "severity": severity(rel3 - 0.25 if not in3 else 0.0, 0.25, in3),
        "p_bayes": p_bayes(rep_sd, obs_sd),
    })

    # --- Check 4: 95th pct (obs<=tail_count_bound AND pp within +-30%) ---
    pp_q95 = float(rep_q95.mean())
    rel4 = abs(pp_q95 - obs_q95) / obs_q95
    in4a = obs_q95 <= tail_count_bound
    in4b = rel4 <= 0.30
    in4 = in4a and in4b
    checks.append({
        "id": 4, "name": "95th percentile",
        "observed": obs_q95, "pp_mean": pp_q95, "rel_dev": rel4,
        "obs_under_tail_bound": in4a, "tail_count_bound": tail_count_bound,
        "bound": "obs<=tail_count_bound AND pp within +-30%",
        "severity": severity(rel4 - 0.30 if not in4b else 0.0, 0.30, in4),
        "p_bayes": p_bayes(rep_q95, obs_q95),
    })

    # --- Check 5: mean-variance ratio (within [0.5x, 2x]) ---------------
    pp_mvr = float(rep_mvr.mean())
    ratio5 = pp_mvr / obs_mvr if obs_mvr > 0 else float("inf")
    in5 = 0.5 <= ratio5 <= 2.0
    if in5:
        dist5 = 0.0
    elif ratio5 > 2.0:
        dist5 = ratio5 - 2.0
    else:
        dist5 = 0.5 - ratio5
    checks.append({
        "id": 5, "name": "mean-variance ratio",
        "observed": obs_mvr, "pp_mean": pp_mvr, "ratio_pp_over_obs": ratio5,
        "bound": "pp ratio within [0.5x, 2x] of observed",
        "severity": severity(dist5, 1.0, in5),
        "p_bayes": p_bayes(rep_mvr, obs_mvr),
    })

    # --- Check 6: Bayesian p-values for #2-#5 in [0.05, 0.95] -----------
    pvals = {c["name"]: c["p_bayes"] for c in checks if "p_bayes" in c}
    pb_out = []
    for name, pb in pvals.items():
        in6 = 0.05 <= pb <= 0.95
        dist6 = 0.0 if in6 else (0.05 - pb if pb < 0.05 else pb - 0.95)
        pb_out.append({"statistic": name, "p_bayes": pb,
                       "severity": severity(dist6, 0.05, in6)})
    checks.append({"id": 6, "name": "Bayesian p-values (#2-#5)",
                   "bound": "0.05 <= p_B <= 0.95", "details": pb_out,
                   "severity": ("critical" if any(d["severity"] == "critical"
                                                  for d in pb_out)
                                else "grey" if any(d["severity"] == "grey"
                                                   for d in pb_out)
                                else "minor" if any(d["severity"] == "minor"
                                                    for d in pb_out)
                                else "pass")})

    # --- Residual structure (#7-#9): posterior-mean Pearson residuals ---
    r = pearson_resid_posterior_mean(idata, y)
    log_mu_mean = idata.posterior["log_mu"].mean(("chain", "draw")).values
    within = cities["log_pop_within"].to_numpy(dtype=float)

    def ols_slope(xv, yv):
        X = np.column_stack([np.ones_like(xv), xv])
        coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
        return float(coef[1])

    # --- Check 7: residual-vs-fitted slope (|slope| < 0.10) ------------
    slope7 = ols_slope(log_mu_mean, r)
    in7 = abs(slope7) < 0.10
    checks.append({
        "id": 7, "name": "residual-vs-fitted slope", "slope": slope7,
        "bound": "|slope| < 0.10",
        "severity": severity(abs(slope7) - 0.10 if not in7 else 0.0, 0.10, in7),
    })

    # --- Check 8: residual-vs-within-logpop slope (|slope| < 0.10) -----
    slope8 = ols_slope(within, r)
    in8 = abs(slope8) < 0.10
    checks.append({
        "id": 8, "name": "residual-vs-within-logpop slope", "slope": slope8,
        "bound": "|slope| < 0.10",
        "severity": severity(abs(slope8) - 0.10 if not in8 else 0.0, 0.10, in8),
    })

    # --- Check 9: province residual dispersion (n>=5; [0.5x, 2x]) ------
    df_r = pd.DataFrame({"province": cities["province"].values,
                         "abs_r": np.abs(r)})
    overall_mean_absr = float(df_r["abs_r"].mean())
    prov_grp = df_r.groupby("province")["abs_r"].agg(["mean", "count"])
    prov_grp = prov_grp[prov_grp["count"] >= 5]
    prov_grp["ratio"] = prov_grp["mean"] / overall_mean_absr
    outside = prov_grp[(prov_grp["ratio"] < 0.5) | (prov_grp["ratio"] > 2.0)]
    worst_ratio = float(prov_grp["ratio"].max()) if len(prov_grp) else 1.0
    worst_lo = float(prov_grp["ratio"].min()) if len(prov_grp) else 1.0
    in9 = len(outside) == 0
    if in9:
        dist9 = 0.0
    else:
        dist9 = max(worst_ratio - 2.0, 0.5 - worst_lo, 0.0)
    checks.append({
        "id": 9, "name": "province residual dispersion",
        "n_provinces_n5": int(len(prov_grp)),
        "n_outside_band": int(len(outside)),
        "worst_ratio_high": worst_ratio, "worst_ratio_low": worst_lo,
        "bound": "per-province mean|r| in [0.5x, 2x] of overall (n>=5)",
        "severity": severity(dist9, 1.0, in9),
    })

    # --- Check 10: posterior-predictive Moran's I (k=8) ----------------
    coords = cities[["longitude", "latitude"]].to_numpy(dtype=float)
    w = KNN.from_array(coords, k=PRIMARY_K)
    w.transform = "r"
    # observed Moran's I on the posterior-mean residual vector:
    moran_obs = Moran(r, w, permutations=0, two_tailed=False).I
    # posterior-predictive distribution of Moran's I: for each y_rep draw,
    # compute the Pearson residual of y_rep against its own mu, then Moran's I.
    post = idata.posterior
    nflat = post.sizes["chain"] * post.sizes["draw"]
    log_mu_all = post["log_mu"].values.reshape(nflat, -1)
    alpha_all = post["dispersion"].values.reshape(-1)
    idx = rng.choice(nflat, size=min(N_PP_DRAWS, nflat), replace=False)
    moran_pp = np.empty(len(idx))
    for i, s in enumerate(idx):
        mu_s = np.exp(np.clip(log_mu_all[s], -50, 50))
        a_s = max(alpha_all[s], 1e-6)
        p_s = np.clip(a_s / (a_s + mu_s), 1e-12, 1 - 1e-12)
        yr = rng.negative_binomial(a_s, p_s).astype(float)
        var_s = mu_s + mu_s ** 2 / a_s
        r_s = (yr - mu_s) / np.sqrt(var_s)
        moran_pp[i] = Moran(r_s, w, permutations=0, two_tailed=False).I
    pp_lo, pp_hi = np.percentile(moran_pp, [5, 95])
    in10 = pp_lo <= moran_obs <= pp_hi
    halfwidth = (pp_hi - pp_lo) / 2 if pp_hi > pp_lo else 1e-6
    dist10 = 0.0 if in10 else (moran_obs - pp_hi if moran_obs > pp_hi
                               else pp_lo - moran_obs)
    checks.append({
        "id": 10, "name": "posterior-predictive Moran's I (k=8)",
        "observed_moran_I": float(moran_obs),
        "pp_5pct": float(pp_lo), "pp_95pct": float(pp_hi),
        "pp_median": float(np.median(moran_pp)),
        "bound": "obs Moran's I in 5th-95th pct of pp distribution",
        "severity": severity(dist10, halfwidth, in10),
    })

    # --- adjudicate overall --------------------------------------------
    sev_levels = [c["severity"] for c in checks]
    n_critical = sum(s == "critical" for s in sev_levels)
    n_grey = sum(s == "grey" for s in sev_levels)
    n_minor = sum(s == "minor" for s in sev_levels)
    overall = ("CRITICAL" if n_critical else
               "GREY" if n_grey else
               "MINOR" if n_minor else "ALL-PASS")

    print(f"[03-ppc] severities: {n_critical} critical, {n_grey} grey, "
          f"{n_minor} minor, {sum(s=='pass' for s in sev_levels)} pass")
    for c in checks:
        print(f"   #{c['id']:<2} {c['name']:<38} -> {c['severity']}")

    result = {
        "frame": "latin_primary",
        "response": RESPONSE_COL,
        "overall": overall,
        "n_critical": n_critical, "n_grey": n_grey, "n_minor": n_minor,
        "checks": checks,
        "observed_summary": {
            "mean": obs_mean, "sd": obs_sd, "q95": obs_q95,
            "mean_var_ratio": obs_mvr, "prop_zeros": obs_propzero,
        },
    }
    (out_dir / "ppc-results.json").write_text(json.dumps(result, indent=2))
    print(f"[03-ppc]   -> {out_dir / 'ppc-results.json'}")

    if n_critical > 0:
        print("[03-ppc] HALT: a CRITICAL PPC trigger fired. Per spec, do NOT "
              "improvise a model revision -- report and stop.")
        return 2  # distinct code: critical PPC (not a crash)
    print(f"[03-ppc] DONE (overall: {overall}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
