#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-h9-fit.py --- Step 2 of the H9 letter-mass H3a confirmatory run: the fits.

Fit the preregistered within-between (Mundlak) negative-binomial regression in
pymc, with per-city LETTER MASS as the response, on the H9 PRIMARY (Latin) frame
and the SECONDARY (empire) frame, and report (mirroring the inscription-count
H3a confirmatory run, runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py):

  - f_within (unweighted PRIMARY/Latin) + the three-way verdict at 0.10 + the
    probability ladder P(f>0.05/0.10/0.20);
  - two weighted f_within variants: population-weighted, and LETTER-weighted
    (the natural analogue of the H3a inscription-weighted variant, since the
    response is now letter mass; Decision 32). BOTH are labelled clearly.
  - Bayesian R^2 (Gelman, Goodrich, Gabry & Vehtari 2019), response and latent;
  - the OLS log-log coefficient log(letter_mass) ~ log(pop) (the SR1/Hanson
    comparator under the content measure);
  - the standardisation sensitivity (re-fit with z-standardised predictors);
  - the conservative-vs-interpretive letter-mass sensitivity (the interpretive
    response is re-fit on the SAME Latin cities; Amendment 01 §A5.1 retains
    interpretive as the sensitivity variant);
  - the SECONDARY empire-wide fit (Decision 36: reported as secondary/context
    with the LIRE-coverage caveat).

Model / priors / sampler / convergence gates are IDENTICAL to the H3a template
(unchanged by Amendment 01 §A6 / Decision 36); only the response variable and
the primary/secondary frame ordering change.

Convergence gates (prereg §4): R-hat < 1.01 ALL params, ESS-bulk >= 400,
0 divergences. HALT if unmet after raising tune (do NOT relax the gate).

The posterior InferenceData is saved to NetCDF for the PPC step (step 3).

Inputs
------
runs/2026-06-18-h9-letter-mass-h3a/data/processed/city_level_for_h9_latin.parquet
runs/2026-06-18-h9-letter-mass-h3a/data/processed/city_level_for_h9_empire.parquet

Outputs
-------
runs/2026-06-18-h9-letter-mass-h3a/outputs/idata-latin-primary.nc
runs/2026-06-18-h9-letter-mass-h3a/outputs/idata-latin-standardised.nc
runs/2026-06-18-h9-letter-mass-h3a/outputs/idata-latin-interpretive.nc
runs/2026-06-18-h9-letter-mass-h3a/outputs/idata-empire-secondary.nc
runs/2026-06-18-h9-letter-mass-h3a/outputs/h9-results.json
runs/2026-06-18-h9-letter-mass-h3a/outputs/h9-posterior-summary-latin.csv

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
import pymc as pm

import h9_common as H

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Sampling settings --- IDENTICAL to the H3a confirmatory template
# (runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py). The H3a run found the
# global intercept landed exactly AT the strict R-hat gate at tune=3,000, and
# fixed it by spending MORE warmup + draws (NOT by relaxing the gate). H9 starts
# from the SAME generous settings; if the letter-mass likelihood geometry needs
# even more (the letter response is heavier-tailed; cf. the temporal letter grid
# convergence failure, Amendment 01 §A5.5.1), the runner raises tune further per
# spec --- it does NOT relax the gate.
N_TUNE = 6_000
N_DRAW = 3_000
N_CHAINS = 4
TARGET_ACCEPT = 0.97
RANDOM_SEED = 20_260_618  # H9 confirmatory-run seed (today's date).

# Convergence gates (prereg §4) --- HARD-STOP if unmet.
RHAT_GATE = 1.01
ESS_BULK_GATE = 400
DIVERGENCE_GATE = 0

# The per-city response column (letter mass). The conservative measure is the
# confirmatory response; the interpretive measure is carried as a separate
# column for the sensitivity re-fit.
RESPONSE_COL = "letter_mass"
RESPONSE_COL_INTERPRETIVE = "letter_mass_interpretive"


def build_model(cities: pd.DataFrame, n_provinces: int,
                response_col: str = RESPONSE_COL,
                within_col: str = "log_pop_within",
                between_col: str = "log_pop_prov_mean") -> pm.Model:
    """Construct the non-centred Mundlak NBR (prereg §3 / design artefact §1).

    IDENTICAL to the H3a template's `build_model`, except the observed response
    is the per-city LETTER MASS (`response_col`) rather than inscription count.
    The NBR likelihood, priors, and non-centred province parameterisation are
    unchanged.
    """
    y_obs = cities[response_col].to_numpy(dtype=int)
    within = cities[within_col].to_numpy(dtype=float)
    between = cities[between_col].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)

    # NBR requires non-negative integer counts; letter mass is a non-negative
    # integer sum by construction, but guard explicitly.
    if (y_obs < 0).any():
        raise ValueError("negative letter-mass response present")

    with pm.Model() as model:
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        # Non-centred parameterisation of the province random intercepts.
        alpha_prov_raw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0,
                                   shape=n_provinces)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * alpha_prov_raw)

        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)

        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)

        log_mu = (alpha_0 + alpha_prov[province_idx]
                  + beta_within * within + beta_between * between)
        pm.Deterministic("log_mu", log_mu)
        mu = pm.math.exp(log_mu)
        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)
    return model


def sample(model: pm.Model) -> az.InferenceData:
    """Sample the NUTS posterior at the (H3a-identical) confirmatory settings."""
    with model:
        idata = pm.sample(
            draws=N_DRAW, tune=N_TUNE, chains=N_CHAINS,
            target_accept=TARGET_ACCEPT, random_seed=RANDOM_SEED,
            progressbar=False, return_inferencedata=True,
        )
    return idata


def convergence(idata: az.InferenceData) -> dict:
    """Convergence diagnostics across ALL non-deterministic params plus the
    key reported deterministics. Identical to the H3a template."""
    var_names = ["alpha_0", "beta_within", "beta_between", "sigma_prov",
                 "inv_dispersion", "dispersion", "alpha_prov_raw", "alpha_prov"]
    summ = az.summary(idata, var_names=var_names)
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].sum())
    return {
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_div,
        "rhat_argmax": str(summ["r_hat"].idxmax()),
        "ess_argmin": str(summ["ess_bulk"].idxmin()),
        "summary": summ,
    }


def gate_pass(conv: dict) -> tuple[bool, list[str]]:
    """Apply the strict prereg convergence gate. Identical to the H3a template."""
    msgs = []
    ok = True
    if conv["max_rhat"] >= RHAT_GATE:
        ok = False
        msgs.append(f"R-hat {conv['max_rhat']:.4f} >= {RHAT_GATE} "
                    f"(worst: {conv['rhat_argmax']})")
    if conv["min_ess_bulk"] < ESS_BULK_GATE:
        ok = False
        msgs.append(f"ESS-bulk {conv['min_ess_bulk']:.0f} < {ESS_BULK_GATE} "
                    f"(worst: {conv['ess_argmin']})")
    if conv["n_divergences"] > DIVERGENCE_GATE:
        ok = False
        msgs.append(f"divergences {conv['n_divergences']} > {DIVERGENCE_GATE}")
    return ok, msgs


def f_within(idata: az.InferenceData, cities: pd.DataFrame,
             within_col: str, weights: np.ndarray | None) -> np.ndarray:
    """f_within per posterior draw (optionally weighted). Identical estimand to
    the H3a template.

    f_within = Var_w(beta_within * within_dev) / Var_w(log E[y])
    where the variances are weighted by `weights` (None => unweighted).
    log E[y_c] = log_mu_c = the full linear predictor (incl. province intercept).
    """
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    within_dev = cities[within_col].to_numpy(dtype=float)
    log_mu = post["log_mu"].values.reshape(n, -1)          # (D, C)
    beta_w = post["beta_within"].values.reshape(-1)        # (D,)
    contrib = beta_w[:, None] * within_dev[None, :]        # (D, C)

    if weights is None:
        var_num = contrib.var(axis=1, ddof=0)
        var_den = log_mu.var(axis=1, ddof=0)
    else:
        w = weights / weights.sum()
        mean_num = (contrib * w[None, :]).sum(axis=1, keepdims=True)
        var_num = ((contrib - mean_num) ** 2 * w[None, :]).sum(axis=1)
        mean_den = (log_mu * w[None, :]).sum(axis=1, keepdims=True)
        var_den = ((log_mu - mean_den) ** 2 * w[None, :]).sum(axis=1)
    return var_num / var_den


def verdict_from_ci(ci_lo: float, ci_hi: float, thresh: float = 0.10) -> str:
    """Three-way f_within verdict at the prereg threshold. Identical to H3a."""
    if ci_lo > thresh:
        return "supported"
    if ci_hi < thresh:
        return "evidence-against"
    return "inconclusive"


def summarise_f(draws: np.ndarray) -> dict:
    """Summarise an f_within posterior: median, 95% CI, probability ladder,
    three-way verdict. Identical to the H3a template."""
    lo, med, hi = (float(x) for x in np.percentile(draws, [2.5, 50, 97.5]))
    return {
        "median": med, "ci_lo": lo, "ci_hi": hi,
        "p_gt_005": float((draws > 0.05).mean()),
        "p_gt_010": float((draws > 0.10).mean()),
        "p_gt_020": float((draws > 0.20).mean()),
        "verdict": verdict_from_ci(lo, hi),
    }


def bayes_r2(idata: az.InferenceData, cities: pd.DataFrame,
             response_col: str = RESPONSE_COL) -> dict:
    """Bayesian R^2 (Gelman, Goodrich, Gabry & Vehtari 2019). Identical to the
    H3a template, with the response being letter mass.

    Response-scale (brms-comparable): R2_s = var(mu_s)/(var(mu_s)+var(y-mu_s)).
    Latent-scale: R2_s = var_c(log_mu)/(var_c(log_mu)+mean_c(latent resid var)),
    with the NBR delta-method latent residual var (1/mu + 1/alpha).
    """
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)          # (D, C)
    mu = np.exp(log_mu)
    alpha = post["dispersion"].values.reshape(-1)          # (D,)
    y = cities[response_col].to_numpy(dtype=float)

    # Response-scale.
    var_fit_resp = mu.var(axis=1, ddof=0)
    resid_resp = y[None, :] - mu
    var_res_resp = resid_resp.var(axis=1, ddof=0)
    r2_resp = var_fit_resp / (var_fit_resp + var_res_resp)

    # Latent-scale.
    var_fit_lat = log_mu.var(axis=1, ddof=0)
    latent_resid_var = (1.0 / mu) + (1.0 / alpha[:, None])  # (D, C)
    mean_latent_resid = latent_resid_var.mean(axis=1)
    r2_lat = var_fit_lat / (var_fit_lat + mean_latent_resid)

    def q(a):
        lo, med, hi = np.percentile(a, [2.5, 50, 97.5])
        return {"median": float(med), "ci_lo": float(lo), "ci_hi": float(hi)}

    return {"response_scale": q(r2_resp), "latent_scale": q(r2_lat)}


def ols_loglog(cities: pd.DataFrame, response_col: str = RESPONSE_COL) -> dict:
    """OLS log-log coefficient: log(letter_mass) ~ log(pop). The SR1/Hanson
    comparator under the CONTENT measure.

    Identical machinery to the H3a template's `ols_loglog`, with letter mass as
    the response. The Hanson 2021 beta (0.672) is retained as the published
    inscription-count comparator; under letter mass the slope is expected to
    DIFFER (Amendment 01 §A3: terse epigraphy deflates, monumental amplifies),
    so the comparison is interpretive context, not an equality test.

    Cities with a zero letter mass are dropped from the log-log fit (log(0)
    undefined); the count of dropped zero-mass cities is reported.
    """
    mass = cities[response_col].to_numpy(dtype=float)
    nonzero = mass > 0
    n_zero_dropped = int((~nonzero).sum())
    x = cities["log_pop"].to_numpy(dtype=float)[nonzero]
    yv = np.log(mass[nonzero])
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
    yhat = X @ coef
    ss_res = float(((yv - yhat) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    n = len(x)
    sigma2 = ss_res / (n - 2)
    sxx = float(((x - x.mean()) ** 2).sum())
    se_slope = float(np.sqrt(sigma2 / sxx))
    return {
        "intercept": float(coef[0]),
        "slope": float(coef[1]),
        "slope_se": se_slope,
        "slope_ci95": [float(coef[1] - 1.96 * se_slope),
                       float(coef[1] + 1.96 * se_slope)],
        "r_squared": r2,
        "n": n,
        "n_zero_mass_dropped": n_zero_dropped,
        "hanson_2021_beta": 0.672,
        "note": ("Hanson 2021 beta is the inscription-count comparator; under "
                 "letter mass the slope is expected to differ (content vs acts)."),
    }


def beta_summary(idata: az.InferenceData, names) -> dict:
    """Posterior median + 95% CI for the named parameters. Identical to H3a."""
    out = {}
    post = idata.posterior
    for nm in names:
        d = post[nm].values.reshape(-1)
        lo, med, hi = np.percentile(d, [2.5, 50, 97.5])
        out[nm] = {"median": float(med), "ci_lo": float(lo), "ci_hi": float(hi)}
    return out


def main() -> int:
    out_dir = H.RUN_DIR / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # ===================================================================
    # PRIMARY FIT --- Latin frame, conservative letter mass.
    # ===================================================================
    cities = pd.read_parquet(H.LATIN_PARQUET)
    n_prov = int(cities["province_idx"].max()) + 1
    print(f"[02-fit] PRIMARY (Latin): {len(cities):,} cities, {n_prov} provinces "
          f"(response = {RESPONSE_COL}, conservative)")
    print(f"[02-fit] sampling: tune={N_TUNE}, draws={N_DRAW}, chains={N_CHAINS}, "
          f"target_accept={TARGET_ACCEPT}, seed={RANDOM_SEED}")

    idata = sample(build_model(cities, n_prov))
    conv = convergence(idata)
    ok, gate_msgs = gate_pass(conv)
    print(f"[02-fit] convergence: max R-hat={conv['max_rhat']:.4f}, "
          f"min ESS-bulk={conv['min_ess_bulk']:.0f}, "
          f"divergences={conv['n_divergences']}")
    if not ok:
        print("[02-fit] HARD-STOP: convergence gate unmet on the PRIMARY fit:")
        for m in gate_msgs:
            print("   - " + m)
        print("[02-fit] Per spec: raise tune / investigate; do NOT relax the "
              "gate. (Letter mass is heavier-tailed than counts; the temporal "
              "letter grid failed to converge -- Amendment 01 §A5.5.1 -- but the "
              "cross-sectional letter NBR is a separate, simpler model.) Halting.")
        return 1

    conv["summary"].to_csv(out_dir / "h9-posterior-summary-latin.csv")
    idata.to_netcdf(str(out_dir / "idata-latin-primary.nc"))

    # f_within: unweighted (primary) + two weighted variants.
    # Decision 32 weighted variants: population-weighted, and LETTER-weighted
    # (the natural analogue of the H3a inscription-weighted variant, since the
    # H9 response is letter mass).
    f_unw = f_within(idata, cities, "log_pop_within", None)
    w_pop = cities["urban_context_pop_est"].to_numpy(dtype=float)
    w_letter = cities[RESPONSE_COL].to_numpy(dtype=float)
    f_pop = f_within(idata, cities, "log_pop_within", w_pop)
    f_letter = f_within(idata, cities, "log_pop_within", w_letter)

    s_unw = summarise_f(f_unw)
    print(f"[02-fit] f_within (PRIMARY/Latin unweighted): "
          f"median={s_unw['median']:.4f} "
          f"95% CI [{s_unw['ci_lo']:.4f}, {s_unw['ci_hi']:.4f}] "
          f"verdict={s_unw['verdict']}")
    print(f"[02-fit]   ladder: P(>0.05)={s_unw['p_gt_005']:.4f} "
          f"P(>0.10)={s_unw['p_gt_010']:.4f} P(>0.20)={s_unw['p_gt_020']:.4f}")

    r2 = bayes_r2(idata, cities)
    ols = ols_loglog(cities)
    betas = beta_summary(idata, ["beta_within", "beta_between", "sigma_prov",
                                 "dispersion", "alpha_0"])
    print(f"[02-fit] beta_within  median={betas['beta_within']['median']:.4f} "
          f"CI [{betas['beta_within']['ci_lo']:.4f}, "
          f"{betas['beta_within']['ci_hi']:.4f}]")
    print(f"[02-fit] beta_between median={betas['beta_between']['median']:.4f}")
    print(f"[02-fit] Bayes R^2 response={r2['response_scale']['median']:.4f} "
          f"latent={r2['latent_scale']['median']:.4f}")
    print(f"[02-fit] OLS log-log slope={ols['slope']:.4f} "
          f"(Hanson 2021 inscription beta=0.672), R^2={ols['r_squared']:.4f}, "
          f"zero-mass cities dropped={ols['n_zero_mass_dropped']}")

    # ===================================================================
    # SENSITIVITY: standardised predictors (Latin frame).
    # ===================================================================
    print("\n[02-fit] SENSITIVITY: standardised predictors (Latin)")
    cities_std = H.standardise_predictors(cities)
    idata_std = sample(build_model(cities_std, n_prov,
                                   within_col="log_pop_within_std",
                                   between_col="log_pop_prov_mean_std"))
    conv_std = convergence(idata_std)
    ok_std, _ = gate_pass(conv_std)
    print(f"[02-fit]   std convergence: max R-hat={conv_std['max_rhat']:.4f}, "
          f"min ESS-bulk={conv_std['min_ess_bulk']:.0f}, "
          f"div={conv_std['n_divergences']} (gate met: {ok_std})")
    idata_std.to_netcdf(str(out_dir / "idata-latin-standardised.nc"))
    f_std = f_within(idata_std, cities_std, "log_pop_within_std", None)
    s_std = summarise_f(f_std)
    betas_std = beta_summary(idata_std, ["beta_within", "beta_between"])
    sd_within = float(cities["log_pop_within"].std(ddof=0))
    sd_between = float(cities["log_pop_prov_mean"].std(ddof=0))
    print(f"[02-fit]   f_within (std) median={s_std['median']:.4f} "
          f"(primary {s_unw['median']:.4f}) -- should match (scale-invariant)")
    print(f"[02-fit]   beta_within(std)={betas_std['beta_within']['median']:.4f}; "
          f"implied unstd = {betas_std['beta_within']['median']/sd_within:.4f} "
          f"(primary {betas['beta_within']['median']:.4f})")

    # ===================================================================
    # SENSITIVITY: interpretive letter mass (Amendment 01 §A5.1 retains the
    # interpretive variant as a sensitivity; SAME Latin cities, interpretive
    # response).
    # ===================================================================
    print("\n[02-fit] SENSITIVITY: interpretive letter mass (Latin)")
    idata_intr = sample(build_model(cities, n_prov,
                                    response_col=RESPONSE_COL_INTERPRETIVE))
    conv_intr = convergence(idata_intr)
    ok_intr, _ = gate_pass(conv_intr)
    print(f"[02-fit]   interpretive convergence: "
          f"max R-hat={conv_intr['max_rhat']:.4f}, "
          f"min ESS-bulk={conv_intr['min_ess_bulk']:.0f}, "
          f"div={conv_intr['n_divergences']} (gate met: {ok_intr})")
    idata_intr.to_netcdf(str(out_dir / "idata-latin-interpretive.nc"))
    f_intr = f_within(idata_intr, cities, "log_pop_within", None)
    s_intr = summarise_f(f_intr)
    betas_intr = beta_summary(idata_intr, ["beta_within", "beta_between"])

    # ===================================================================
    # SECONDARY / context: empire-wide (Decision 36; coverage caveat).
    # ===================================================================
    print("\n[02-fit] SECONDARY / context: empire-wide (conservative)")
    empire = pd.read_parquet(H.EMPIRE_PARQUET)
    n_prov_emp = int(empire["province_idx"].max()) + 1
    print(f"[02-fit]   empire: {len(empire):,} cities, {n_prov_emp} provinces")
    idata_emp = sample(build_model(empire, n_prov_emp))
    conv_emp = convergence(idata_emp)
    ok_emp, _ = gate_pass(conv_emp)
    print(f"[02-fit]   empire convergence: max R-hat={conv_emp['max_rhat']:.4f}, "
          f"min ESS-bulk={conv_emp['min_ess_bulk']:.0f}, "
          f"div={conv_emp['n_divergences']} (gate met: {ok_emp})")
    idata_emp.to_netcdf(str(out_dir / "idata-empire-secondary.nc"))
    f_emp = f_within(idata_emp, empire, "log_pop_within", None)
    s_emp = summarise_f(f_emp)
    betas_emp = beta_summary(idata_emp, ["beta_within", "beta_between"])

    # ===================================================================
    # PERSIST
    # ===================================================================
    results = {
        "measure": "letter_mass (Latin A-Z conservative; Amendment 01 §A5.1)",
        "primary_frame": "latin_speaking_provinces (Decision 36 / Amendment 02)",
        "sampling": {"tune": N_TUNE, "draws": N_DRAW, "chains": N_CHAINS,
                     "target_accept": TARGET_ACCEPT, "seed": RANDOM_SEED},
        "primary_latin": {
            "n_cities": int(len(cities)), "n_provinces": n_prov,
            "convergence": {k: conv[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences",
                             "rhat_argmax", "ess_argmin")},
            "f_within_unweighted": s_unw,
            "f_within_population_weighted": summarise_f(f_pop),
            "f_within_letter_weighted": summarise_f(f_letter),
            "betas": betas,
            "bayes_r2": r2,
            "ols_loglog": ols,
        },
        "sensitivity_standardised": {
            "convergence": {k: conv_std[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences")},
            "f_within_unweighted": s_std,
            "betas_standardised": betas_std,
            "predictor_sd": {"within": sd_within, "between": sd_between},
            "beta_within_implied_unstd":
                betas_std["beta_within"]["median"] / sd_within,
        },
        "sensitivity_interpretive_letter_mass": {
            "convergence": {k: conv_intr[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences")},
            "gate_met": ok_intr,
            "f_within_unweighted": s_intr,
            "betas": betas_intr,
        },
        "secondary_empire": {
            "n_cities": int(len(empire)), "n_provinces": n_prov_emp,
            "coverage_caveat": ("empire-wide mixes well-covered Latin provinces "
                                "with poorly-covered Greek ones; reported as "
                                "secondary/context (Decision 36)."),
            "convergence": {k: conv_emp[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences")},
            "gate_met": ok_emp,
            "f_within_unweighted": s_emp,
            "betas": betas_emp,
        },
    }
    (out_dir / "h9-results.json").write_text(json.dumps(results, indent=2))
    print(f"\n[02-fit]   -> {out_dir / 'h9-results.json'}")
    print("[02-fit] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
