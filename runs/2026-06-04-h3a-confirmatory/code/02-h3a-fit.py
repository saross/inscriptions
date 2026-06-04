#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02-h3a-fit.py --- Step 2 of the H3a confirmatory run: the primary fit.

Fit the preregistered within-between (Mundlak) negative-binomial regression in
pymc (non-centred alpha_prov; tune=3,000; 4 chains; target_accept=0.95) on the
PRIMARY 1,044-city frame, and report:
  - f_within (unweighted PRIMARY) + the three-way verdict at 0.10 + the
    probability ladder P(f>0.05/0.10/0.20);
  - two weighted f_within variants (population-weighted, inscription-weighted;
    Decision 32);
  - Bayesian R^2 (Gelman, Goodrich, Gabry & Vehtari 2019) on the response scale
    (brms-comparable) AND a latent-scale linear-predictor R^2;
  - the OLS log-log coefficient (Hanson/SR1 comparator);
  - the standardisation sensitivity (Sensitivity C: re-fit with z-standardised
    predictors; report beta stability).
Also fits the Latin-only sample (Sensitivity B).

Convergence gates (prereg §4): R-hat < 1.01 ALL params, ESS-bulk >= 400,
0 divergences. HALT if unmet after raising tune (do NOT relax the gate).

The posterior InferenceData is saved to NetCDF for PPC (step 3) and H3c
(step 5).

Inputs
------
data/processed/city_level_for_h3a.parquet         (PRIMARY)
data/processed/city_level_for_h3a_latin.parquet   (Sensitivity B)

Outputs
-------
runs/2026-06-04-h3a-confirmatory/outputs/idata-primary.nc
runs/2026-06-04-h3a-confirmatory/outputs/idata-standardised.nc
runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc
runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json
runs/2026-06-04-h3a-confirmatory/outputs/h3a-posterior-summary-primary.csv

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
import pymc as pm

import h3a_common as H

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Sampling settings (prereg §4 / spec §4 step 2). tune raised to 3,000.
N_TUNE = 3_000
N_DRAW = 2_000
N_CHAINS = 4
TARGET_ACCEPT = 0.95
RANDOM_SEED = 20_260_604  # confirmatory-run seed

# Convergence gates (prereg §4) --- HARD-STOP if unmet.
RHAT_GATE = 1.01
ESS_BULK_GATE = 400
DIVERGENCE_GATE = 0


def build_model(cities: pd.DataFrame, n_provinces: int,
                within_col: str = "log_pop_within",
                between_col: str = "log_pop_prov_mean") -> pm.Model:
    """Construct the non-centred Mundlak NBR (prereg §3 / design artefact §1)."""
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    within = cities[within_col].to_numpy(dtype=float)
    between = cities[between_col].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)

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
    with model:
        idata = pm.sample(
            draws=N_DRAW, tune=N_TUNE, chains=N_CHAINS,
            target_accept=TARGET_ACCEPT, random_seed=RANDOM_SEED,
            progressbar=False, return_inferencedata=True,
        )
    return idata


def convergence(idata: az.InferenceData) -> dict:
    """Compute convergence diagnostics across ALL non-deterministic params
    plus the key reported deterministics.
    """
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
    """f_within per posterior draw (optionally weighted).

    f_within = Var_w(beta_within * within_dev) / Var_w(log E[insc])
    where the variances are weighted by `weights` (None => unweighted).
    log E[insc_c] = log_mu_c = full linear predictor (incl. province intercept).
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
    if ci_lo > thresh:
        return "supported"
    if ci_hi < thresh:
        return "evidence-against"
    return "inconclusive"


def summarise_f(draws: np.ndarray) -> dict:
    lo, med, hi = (float(x) for x in np.percentile(draws, [2.5, 50, 97.5]))
    return {
        "median": med, "ci_lo": lo, "ci_hi": hi,
        "p_gt_005": float((draws > 0.05).mean()),
        "p_gt_010": float((draws > 0.10).mean()),
        "p_gt_020": float((draws > 0.20).mean()),
        "verdict": verdict_from_ci(lo, hi),
    }


def bayes_r2(idata: az.InferenceData, cities: pd.DataFrame) -> dict:
    """Bayesian R^2 (Gelman, Goodrich, Gabry & Vehtari 2019).

    Response-scale (brms-comparable): R2_s = var(mu_s) / (var(mu_s) + var(y-mu_s)).
    Latent-scale (prereg 'full-model latent-scale'):
        R2_s = var_c(log_mu) / (var_c(log_mu) + mean_c(latent residual var)),
        with the NBR delta-method latent residual var (1/mu + 1/alpha).
    Both reported as posterior median + 95% CI.
    """
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)          # (D, C)
    mu = np.exp(log_mu)
    alpha = post["dispersion"].values.reshape(-1)          # (D,)
    y = cities["inscription_count"].to_numpy(dtype=float)

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


def ols_loglog(cities: pd.DataFrame) -> dict:
    """OLS log-log coefficient: log(count) ~ log(pop). Hanson/SR1 comparator.

    Hanson, Ortman & Lobo 2017 / Hanson 2021 report a population scaling
    exponent (beta = 0.672 in prereg). This is the direct frequentist
    comparator on the same per-city data (unweighted OLS on logs).
    """
    x = cities["log_pop"].to_numpy(dtype=float)
    yv = np.log(cities["inscription_count"].to_numpy(dtype=float))
    X = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(X, yv, rcond=None)
    yhat = X @ coef
    ss_res = float(((yv - yhat) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot
    # Standard error of the slope.
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
        "hanson_2021_beta": 0.672,
    }


def beta_summary(idata: az.InferenceData, names) -> dict:
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
    # PRIMARY FIT
    # ===================================================================
    cities = pd.read_parquet(H.PRIMARY_PARQUET)
    n_prov = int(cities["province_idx"].max()) + 1
    print(f"[02-fit] PRIMARY: {len(cities):,} cities, {n_prov} provinces")
    print(f"[02-fit] sampling: tune={N_TUNE}, draws={N_DRAW}, chains={N_CHAINS}, "
          f"target_accept={TARGET_ACCEPT}")

    idata = sample(build_model(cities, n_prov))
    conv = convergence(idata)
    ok, gate_msgs = gate_pass(conv)
    print(f"[02-fit] convergence: max R-hat={conv['max_rhat']:.4f}, "
          f"min ESS-bulk={conv['min_ess_bulk']:.0f}, "
          f"divergences={conv['n_divergences']}")
    if not ok:
        print("[02-fit] HARD-STOP: convergence gate unmet:")
        for m in gate_msgs:
            print("   - " + m)
        print("[02-fit] (tune already 3,000; do NOT relax the gate). Halting.")
        return 1

    conv["summary"].to_csv(out_dir / "h3a-posterior-summary-primary.csv")
    idata.to_netcdf(str(out_dir / "idata-primary.nc"))

    # f_within (primary unweighted + 2 weighted variants)
    f_unw = f_within(idata, cities, "log_pop_within", None)
    w_pop = cities["urban_context_pop_est"].to_numpy(dtype=float)
    w_insc = cities["inscription_count"].to_numpy(dtype=float)
    f_pop = f_within(idata, cities, "log_pop_within", w_pop)
    f_insc = f_within(idata, cities, "log_pop_within", w_insc)

    s_unw = summarise_f(f_unw)
    print(f"[02-fit] f_within (PRIMARY unweighted): median={s_unw['median']:.4f} "
          f"95% CI [{s_unw['ci_lo']:.4f}, {s_unw['ci_hi']:.4f}] "
          f"verdict={s_unw['verdict']}")
    print(f"[02-fit]   ladder: P(>0.05)={s_unw['p_gt_005']:.4f} "
          f"P(>0.10)={s_unw['p_gt_010']:.4f} P(>0.20)={s_unw['p_gt_020']:.4f}")

    r2 = bayes_r2(idata, cities)
    ols = ols_loglog(cities)
    betas = beta_summary(idata, ["beta_within", "beta_between", "sigma_prov",
                                 "dispersion", "alpha_0"])
    print(f"[02-fit] beta_within  median={betas['beta_within']['median']:.4f} "
          f"CI [{betas['beta_within']['ci_lo']:.4f}, {betas['beta_within']['ci_hi']:.4f}]")
    print(f"[02-fit] beta_between median={betas['beta_between']['median']:.4f}")
    print(f"[02-fit] Bayes R^2 response={r2['response_scale']['median']:.4f} "
          f"latent={r2['latent_scale']['median']:.4f}")
    print(f"[02-fit] OLS log-log slope={ols['slope']:.4f} "
          f"(Hanson 2021 beta=0.672), R^2={ols['r_squared']:.4f}")

    # ===================================================================
    # SENSITIVITY C: standardised predictors
    # ===================================================================
    print("\n[02-fit] SENSITIVITY C: standardised predictors")
    cities_std = H.standardise_predictors(cities)
    idata_std = sample(build_model(cities_std, n_prov,
                                   within_col="log_pop_within_std",
                                   between_col="log_pop_prov_mean_std"))
    conv_std = convergence(idata_std)
    ok_std, _ = gate_pass(conv_std)
    print(f"[02-fit]   std convergence: max R-hat={conv_std['max_rhat']:.4f}, "
          f"min ESS-bulk={conv_std['min_ess_bulk']:.0f}, "
          f"div={conv_std['n_divergences']} (gate met: {ok_std})")
    idata_std.to_netcdf(str(out_dir / "idata-standardised.nc"))
    f_std = f_within(idata_std, cities_std, "log_pop_within_std", None)
    s_std = summarise_f(f_std)
    betas_std = beta_summary(idata_std, ["beta_within", "beta_between"])
    # Stability: f_within is scale-invariant, so it should match the primary;
    # the betas rescale by the predictor SD.
    sd_within = float(cities["log_pop_within"].std(ddof=0))
    sd_between = float(cities["log_pop_prov_mean"].std(ddof=0))
    print(f"[02-fit]   f_within (std) median={s_std['median']:.4f} "
          f"(primary {s_unw['median']:.4f}) -- should match (scale-invariant)")
    print(f"[02-fit]   beta_within(std)={betas_std['beta_within']['median']:.4f}; "
          f"implied unstd = {betas_std['beta_within']['median'] / sd_within:.4f} "
          f"(primary {betas['beta_within']['median']:.4f})")

    # ===================================================================
    # SENSITIVITY B: Latin-only
    # ===================================================================
    print("\n[02-fit] SENSITIVITY B: Latin-only")
    latin = pd.read_parquet(H.LATIN_PARQUET)
    n_prov_lat = int(latin["province_idx"].max()) + 1
    print(f"[02-fit]   Latin: {len(latin):,} cities, {n_prov_lat} provinces")
    idata_lat = sample(build_model(latin, n_prov_lat))
    conv_lat = convergence(idata_lat)
    ok_lat, lat_msgs = gate_pass(conv_lat)
    print(f"[02-fit]   Latin convergence: max R-hat={conv_lat['max_rhat']:.4f}, "
          f"min ESS-bulk={conv_lat['min_ess_bulk']:.0f}, "
          f"div={conv_lat['n_divergences']} (gate met: {ok_lat})")
    idata_lat.to_netcdf(str(out_dir / "idata-latin.nc"))
    f_lat = f_within(idata_lat, latin, "log_pop_within", None)
    s_lat = summarise_f(f_lat)
    betas_lat = beta_summary(idata_lat, ["beta_within", "beta_between"])
    print(f"[02-fit]   f_within (Latin) median={s_lat['median']:.4f} "
          f"95% CI [{s_lat['ci_lo']:.4f}, {s_lat['ci_hi']:.4f}] "
          f"verdict={s_lat['verdict']}")

    # ===================================================================
    # PERSIST
    # ===================================================================
    results = {
        "sampling": {"tune": N_TUNE, "draws": N_DRAW, "chains": N_CHAINS,
                     "target_accept": TARGET_ACCEPT, "seed": RANDOM_SEED},
        "primary": {
            "n_cities": int(len(cities)), "n_provinces": n_prov,
            "convergence": {k: conv[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences",
                             "rhat_argmax", "ess_argmin")},
            "f_within_unweighted": s_unw,
            "f_within_population_weighted": summarise_f(f_pop),
            "f_within_inscription_weighted": summarise_f(f_insc),
            "betas": betas,
            "bayes_r2": r2,
            "ols_loglog": ols,
        },
        "sensitivity_C_standardised": {
            "convergence": {k: conv_std[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences")},
            "f_within_unweighted": s_std,
            "betas_standardised": betas_std,
            "predictor_sd": {"within": sd_within, "between": sd_between},
            "beta_within_implied_unstd":
                betas_std["beta_within"]["median"] / sd_within,
        },
        "sensitivity_B_latin": {
            "n_cities": int(len(latin)), "n_provinces": n_prov_lat,
            "convergence": {k: conv_lat[k] for k in
                            ("max_rhat", "min_ess_bulk", "n_divergences")},
            "gate_met": ok_lat,
            "f_within_unweighted": s_lat,
            "betas": betas_lat,
        },
        "sensitivity_A_with_zeros": {
            "note": ("0 structural zeros added -- all 1,044 Hanson cities have "
                     ">=1 date-window inscription; identical to PRIMARY, not "
                     "re-fit."),
        },
    }
    (out_dir / "h3a-results.json").write_text(json.dumps(results, indent=2))
    print(f"\n[02-fit]   -> {out_dir / 'h3a-results.json'}")
    print("[02-fit] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
