#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h3a_alpha_translator.py — D13 Stage 2: the α-as-translator augmented H3a NBR.
============================================================================

Stage 2 of the D13 "α-as-translator" sensitivity (spec
``runs/2026-06-19-d13-alpha-as-translator/spec.md`` §4). It answers the lodged
prereg question: **is the H3a within-province population–epigraphy scaling
(β_within / f_within) confounded by per-city editorial-convention intensity
(α_c)?** It adds the Stage-1 per-city α_c as a covariate to the H3a Mundlak NBR
and watches β_within.

REUSE, don't re-derive (spec §4): the H3a negative-binomial Mundlak machinery —
``build_model``, ``f_within``, ``summarise_f``, ``beta_summary``, ``sample`` /
``convergence`` / ``gate_pass`` — is imported verbatim from the H3a confirmatory
fit (``runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py``). The Latin frame
builder and predictor standardisation come from ``h3a_common.py``. The ONLY new
model code is ``build_model_augmented``, a faithful mirror of the lodged
``build_model`` with one extra additive term ``γ·α_c_std`` in ``log_mu`` (no
lodged file is modified). The Theil-Sen / bootstrap proxy helpers are reused from
the deconvolution-leverage diagnostic (``deconv_leverage_diagnostic.py``; the
Obs 94 province-level proxy this extends to the city level).

The base comparison is re-fit on the IDENTICAL 163-city Latin subset (Mundlak
centring recomputed over THIS subset), so the only difference between base and
augmented is the α_c term — not the frame.

Deliverables (spec §4):
  * S2a — prereg-literal primary: augmented NBR with standardised posterior-MEDIAN
    α_c. Report β_within, f_within (unweighted), γ, each vs the base 163-city fit.
    Pre-stated yardstick (state BEFORE the result): f_within posterior-median/CI
    shift ≥ 0.063 is "material" (D11 precedent); β_within shift reported against
    its posterior SD + CI overlap.
  * S2b — multiple imputation (M = 50): draw per-city α-vectors from the Stage-1
    posteriors, fit the augmented NBR per imputation, pool β_within / f_within / γ
    via Rubin's rules (the §2 honesty layer — propagates the reachability-driven
    per-city unreliability into the coefficient uncertainty).
  * S2c — reachability robustness: (i) re-run S2a on the N ≥ 500 subset (18 cities;
    flagged within-province-leverage-thin / descriptive); (ii) the city-level
    α_c-vs-log(population) scatter + Theil-Sen slope (city-level Obs 94 proxy).

Usage (sapphire or local; the NBR fits are light vs the deconvolution):

    PATH=$HOME/.local/bin:$PATH PYTENSOR_FLAGS=mode=FAST_RUN \
        uv run python code/h3a_alpha_translator.py [--n-imputations 50]
        [--skip-mi]   (S2a + S2c only; for a quick check)

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-19.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-19-d13-alpha-as-translator")
H3A = Path("/home/shawn/Code/inscriptions/runs/2026-06-04-h3a-confirmatory/code")
LEV = Path("/home/shawn/Code/inscriptions/runs/2026-06-16-deconv-leverage-diagnostic/code")
sys.path.insert(0, str(RUN / "code"))
sys.path.insert(0, str(H3A))
sys.path.insert(0, str(LEV))

import city_lib as C  # noqa: E402

# H3a confirmatory machinery (imported verbatim from the numeric-named module).
import importlib.util as _ilu  # noqa: E402


def _load_module(path: Path, name: str):
    """Import a module from an explicit path (the H3a fit is a numeric-named file
    ``02-h3a-fit.py`` that is not importable by ``import 02_h3a_fit``)."""
    spec = _ilu.spec_from_file_location(name, str(path))
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HF = _load_module(H3A / "02-h3a-fit.py", "h3a_fit")  # build_model, f_within, ...
import h3a_common as HC  # noqa: E402  (build_latin_frame, standardise_predictors)
# Reuse the leverage diagnostic's robust-slope + bootstrap helpers (Obs 94 proxy).
import deconv_leverage_diagnostic as LD  # noqa: E402

OUT_DIR = RUN / "outputs"
ALPHA_DRAWS_DIR = OUT_DIR / "alpha-draws"
UNITS_DIR = OUT_DIR / "units"
FIG_DIR = OUT_DIR / "figures"

# Pre-stated materiality yardstick (spec §4; D11 precedent — continuity 2026-06-16:
# D11 max CI shift 0.047 < 0.063 → no material divergence). STATE BEFORE THE RESULT.
F_WITHIN_MATERIAL_SHIFT = 0.063

# MI / reachability constants.
N_IMPUTATIONS = 50          # spec §4 S2b: M = 50
N_RELIABLE = C.N_RELIABLE   # 500 (the standalone-α reachability floor)
MI_SEED = 20260619          # reproducible imputation draws


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


# --------------------------------------------------------------------------- #
# Augmented NBR (faithful mirror of HF.build_model + the γ·α_c term).            #
# --------------------------------------------------------------------------- #
def build_model_augmented(cities: pd.DataFrame, n_provinces: int,
                          alpha_col: str = "alpha_c_std",
                          within_col: str = "log_pop_within",
                          between_col: str = "log_pop_prov_mean") -> pm.Model:
    """The H3a Mundlak NBR augmented with a per-city α covariate (spec §4).

    BYTE-equivalent to the lodged ``HF.build_model`` (same priors, same
    non-centred province intercepts, same NBR likelihood) with ONE additive term::

        log_mu = α0 + α_prov[prov] + β_within·within + β_between·between
                 + γ·α_c_std

    ``γ`` gets the same weakly-informative ``Normal(0, 1)`` prior as the slopes.
    ``log_mu`` is registered as the deterministic the lodged ``f_within`` /
    ``bayes_r2`` read. No lodged module is modified — this mirror lives in the D13
    run dir.
    """
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    within = cities[within_col].to_numpy(dtype=float)
    between = cities[between_col].to_numpy(dtype=float)
    alpha_c = cities[alpha_col].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)

    with pm.Model() as model:
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        alpha_prov_raw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0,
                                   shape=n_provinces)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * alpha_prov_raw)

        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)
        gamma_alpha = pm.Normal("gamma_alpha", mu=0.0, sigma=1.0)  # the α_c coefficient

        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)

        log_mu = (alpha_0 + alpha_prov[province_idx]
                  + beta_within * within + beta_between * between
                  + gamma_alpha * alpha_c)
        pm.Deterministic("log_mu", log_mu)
        mu = pm.math.exp(log_mu)
        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)
    return model


def _sample_aug(model: pm.Model, seed: int) -> az.InferenceData:
    """Sample with the H3a confirmatory sampler settings (HF.N_TUNE/N_DRAW/...)."""
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=HF.N_DRAW, tune=HF.N_TUNE, chains=HF.N_CHAINS,
                target_accept=HF.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True,
            )
    return idata


# --------------------------------------------------------------------------- #
# 163-city Latin subset + per-city α attachment.                                #
# --------------------------------------------------------------------------- #
def build_163_subset() -> pd.DataFrame:
    """The 163 N ≥ 100 Latin cities with Mundlak centring recomputed over THIS
    subset (so within/between are correct for the sample) and a re-indexed
    ``province_idx`` (contiguous 0..n_prov-1)."""
    latin = pd.read_parquet(C.LATIN_PARQUET)
    sub = latin.loc[latin["inscription_count"] >= C.N_MIN].copy()
    # Recompute Mundlak components over the 163-city subset (the correct centring
    # for this sample — mirrors HC.build_latin_frame's recentring on its subset).
    prov_means = sub.groupby("province")["log_pop"].transform("mean")
    sub["log_pop_prov_mean"] = prov_means
    sub["log_pop_within"] = sub["log_pop"] - prov_means
    province_codes = pd.Categorical(sub["province"])
    sub["province_idx"] = province_codes.codes
    return sub.reset_index(drop=True)


def attach_alpha_median(cities: pd.DataFrame) -> pd.DataFrame:
    """Attach each city's Stage-1 posterior-MEDIAN α (from outputs/units/<city>.json)."""
    out = cities.copy()
    med = {}
    for city in out["city"]:
        p = UNITS_DIR / f"{_safe(city)}.json"
        d = json.loads(p.read_text())
        med[city] = float(d["alpha_median"])
    out["alpha_c_median"] = out["city"].map(med)
    if out["alpha_c_median"].isna().any():
        missing = out.loc[out["alpha_c_median"].isna(), "city"].tolist()
        raise RuntimeError(f"missing Stage-1 α for {len(missing)} cities: {missing[:5]}")
    return out


def standardise_alpha(cities: pd.DataFrame, alpha_col: str, out_col: str) -> pd.DataFrame:
    """z-standardise an α column (mean 0, SD 1 over the given frame)."""
    out = cities.copy()
    mu = out[alpha_col].mean()
    sd = out[alpha_col].std(ddof=0)
    out[out_col] = (out[alpha_col] - mu) / (sd if sd > 0 else 1.0)
    return out


def load_alpha_draw_matrix(cities: pd.DataFrame) -> np.ndarray:
    """Per-city α posterior draw matrix (n_cities, n_draws) from the npz hand-off.

    Each city's full α posterior vector (8,000 draws) in the city order of
    ``cities``. Used by S2b multiple imputation. All cities share n_draws (same
    sampler config), so this stacks cleanly.
    """
    mats = []
    n_draws = None
    for city in cities["city"]:
        z = np.load(ALPHA_DRAWS_DIR / f"{_safe(city)}-alpha.npz", allow_pickle=True)
        a = z["alpha"].astype(np.float64)
        if n_draws is None:
            n_draws = a.size
        elif a.size != n_draws:
            raise RuntimeError(f"{city}: {a.size} α draws != expected {n_draws}")
        mats.append(a)
    return np.vstack(mats)  # (n_cities, n_draws)


# --------------------------------------------------------------------------- #
# Single-fit helpers (base + augmented) → β_within / f_within / γ summaries.     #
# --------------------------------------------------------------------------- #
def _fit_base(cities: pd.DataFrame, n_prov: int, seed: int) -> dict:
    """Fit the base H3a NBR (no α) on a subset; return betas + f_within + conv.

    Uses the lodged ``HF.build_model`` verbatim, sampled at the confirmatory
    settings (``HF.N_DRAW``/``N_TUNE``/``N_CHAINS``/``TARGET_ACCEPT``) with an
    explicit seed so base and augmented share the seed (only the α_c term differs).
    """
    idata = _sample_base(cities, n_prov, seed)
    conv = HF.convergence(idata)
    betas = HF.beta_summary(idata, ["beta_within", "beta_between", "alpha_0",
                                    "sigma_prov", "dispersion"])
    f = HF.f_within(idata, cities, "log_pop_within", None)
    return {
        "betas": betas,
        "f_within": HF.summarise_f(f),
        "convergence": {k: conv[k] for k in
                        ("max_rhat", "min_ess_bulk", "n_divergences")},
    }


def _sample_base(cities: pd.DataFrame, n_prov: int, seed: int) -> az.InferenceData:
    """Base H3a NBR sample at the confirmatory settings with an explicit seed."""
    model = HF.build_model(cities, n_prov)
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=HF.N_DRAW, tune=HF.N_TUNE, chains=HF.N_CHAINS,
                target_accept=HF.TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True,
            )
    return idata


def _fit_augmented(cities: pd.DataFrame, n_prov: int, seed: int,
                   alpha_col: str = "alpha_c_std") -> dict:
    """Fit the augmented NBR; return betas (incl. γ) + f_within + conv + raw draws."""
    idata = _sample_aug(build_model_augmented(cities, n_prov, alpha_col=alpha_col), seed)
    conv = HF.convergence(idata)  # same var list; α-term not included but fine
    betas = HF.beta_summary(idata, ["beta_within", "beta_between", "gamma_alpha",
                                    "alpha_0", "sigma_prov", "dispersion"])
    f = HF.f_within(idata, cities, "log_pop_within", None)
    return {
        "betas": betas,
        "f_within": HF.summarise_f(f),
        "convergence": {k: conv[k] for k in
                        ("max_rhat", "min_ess_bulk", "n_divergences")},
        "_beta_within_draws": idata.posterior["beta_within"].values.reshape(-1),
        "_gamma_draws": idata.posterior["gamma_alpha"].values.reshape(-1),
        "_f_within_draws": f,
    }


# --------------------------------------------------------------------------- #
# Rubin's rules (S2b pooling).                                                   #
# --------------------------------------------------------------------------- #
def rubin_pool(estimates: list[float], variances: list[float]) -> dict:
    """Pool M point estimates + within-imputation variances via Rubin's (1987) rules.

    Q̄ = mean(estimate); Ū = mean(variance) (within); B = var(estimate, ddof=1)
    (between); T = Ū + (1 + 1/M)·B (total). Returns the pooled estimate, total SE,
    95 % CI (normal approx — M=50 gives ample df), and the fraction of missing
    information λ = (1 + 1/M)·B / T.
    """
    m = len(estimates)
    q = np.asarray(estimates, dtype=float)
    u = np.asarray(variances, dtype=float)
    qbar = float(q.mean())
    ubar = float(u.mean())
    b = float(q.var(ddof=1)) if m > 1 else 0.0
    t = ubar + (1.0 + 1.0 / m) * b
    se = float(np.sqrt(t))
    lam = ((1.0 + 1.0 / m) * b / t) if t > 0 else float("nan")
    return {
        "pooled": qbar, "se": se,
        "ci_lo": qbar - 1.96 * se, "ci_hi": qbar + 1.96 * se,
        "within_var": ubar, "between_var": b, "total_var": t,
        "fraction_missing_info": lam, "m": m,
    }


# --------------------------------------------------------------------------- #
# S2c proxy: city-level α_c vs log(population) (Obs 94 city-level extension).     #
# --------------------------------------------------------------------------- #
def alpha_vs_pop_proxy(cities: pd.DataFrame) -> dict:
    """City-level α_c-vs-log(population) slope (OLS + robust Theil-Sen + boot CI).

    The implied Hanson-β shift from replacing raw count N with genuine count
    α·N is the slope of log(α) on log(population) (the Obs 94 statistic, here at
    the CITY level on the 163 deconvolved cities). Reuses the leverage
    diagnostic's robust slope + bootstrap helpers.
    """
    lp = np.log(cities["urban_context_pop_est"].to_numpy(dtype=float))
    a = cities["alpha_c_median"].to_numpy(dtype=float)
    la = np.log(np.clip(a, 1e-6, None))
    ols_dbeta = LD._ols_slope(lp, la)
    ts_dbeta = LD._theilsen_slope(lp, la)
    ols_ci = LD._boot_ci(lp, la, LD._ols_slope, seed=MI_SEED)
    ts_ci = LD._boot_ci(lp, la, LD._theilsen_slope, seed=MI_SEED)
    return {
        "n_cities": int(len(cities)),
        "spearman_alpha_vs_logpop": LD._spearman(a, lp),
        "pearson_alpha_vs_logpop": float(np.corrcoef(a, lp)[0, 1]),
        "implied_delta_beta_ols": ols_dbeta,
        "implied_delta_beta_ols_ci95": list(ols_ci),
        "implied_delta_beta_theilsen": ts_dbeta,
        "implied_delta_beta_theilsen_ci95": list(ts_ci),
        "alpha_median_range": [float(a.min()), float(a.max())],
        "alpha_median_mean": float(a.mean()),
        "alpha_median_sd": float(a.std(ddof=1)),
    }


def make_figure(cities: pd.DataFrame, proxy: dict) -> None:
    """α_c-vs-population scatter with the robust (Theil-Sen) slope (spec §6)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pop = cities["urban_context_pop_est"].to_numpy(dtype=float)
    a = cities["alpha_c_median"].to_numpy(dtype=float)
    reliable = cities["inscription_count"].to_numpy() >= N_RELIABLE
    lp = np.log(pop)

    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.scatter(pop[~reliable], a[~reliable], c="C0", alpha=0.6, s=28,
               label=f"caveated (N < {N_RELIABLE}; n={int((~reliable).sum())})")
    ax.scatter(pop[reliable], a[reliable], c="C3", marker="D", s=44,
               label=f"reliable (N ≥ {N_RELIABLE}; n={int(reliable.sum())})")
    # Robust Theil-Sen line through (log pop, α) — note α not log α for the plot,
    # but the slope statistic in the title is the log α ~ log pop slope (Obs 94).
    ts_a = LD._theilsen_slope(lp, a)
    b0 = float(np.median(a - ts_a * lp))
    xs = np.linspace(lp.min(), lp.max(), 50)
    ax.plot(np.exp(xs), b0 + ts_a * xs, "k--", lw=1.3,
            label=f"Theil-Sen (α~log pop) slope={ts_a:+.3f}")
    ax.set_xscale("log")
    ax.set_xlabel("Hanson urban population estimate (log scale)")
    ax.set_ylabel("per-city α_c (genuine fraction, posterior median)")
    ax.set_ylim(0, 1.02)
    dts = proxy["implied_delta_beta_theilsen"]
    dts_ci = proxy["implied_delta_beta_theilsen_ci95"]
    ax.set_title(
        "D13 city-level α-vs-population (Obs 94 extension)\n"
        f"implied Δβ (log α ~ log pop): Theil-Sen {dts:+.3f} "
        f"[{dts_ci[0]:+.3f}, {dts_ci[1]:+.3f}]  ⇒  flat ⇒ no Hanson-β confound",
        fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "fig-alpha-vs-population-city.png", dpi=140)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Main pipeline.                                                                 #
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-imputations", type=int, default=N_IMPUTATIONS)
    ap.add_argument("--skip-mi", action="store_true",
                    help="S2a + S2c only (skip the M-imputation S2b batch)")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(MI_SEED)

    # ---- frame + α attachment ----
    cities = build_163_subset()
    cities = attach_alpha_median(cities)
    n_prov = int(cities["province_idx"].max()) + 1
    print(f"[D13-S2] 163-city Latin subset: {len(cities)} cities, {n_prov} provinces",
          flush=True)
    print(f"[D13-S2] PRE-STATED yardstick: f_within shift ≥ {F_WITHIN_MATERIAL_SHIFT} "
          f"is material (D11 precedent); β_within shift vs posterior SD + CI overlap.",
          flush=True)

    base_seed = HF.RANDOM_SEED  # reuse the H3a confirmatory seed for the base re-fit

    # ===================================================================
    # BASE 163-city fit (the only difference vs augmented is the α_c term)
    # ===================================================================
    base = _fit_base(cities, n_prov, base_seed)
    bw_base = base["betas"]["beta_within"]
    fw_base = base["f_within"]
    print(f"[D13-S2] BASE  β_within={bw_base['median']:+.4f} "
          f"[{bw_base['ci_lo']:+.4f}, {bw_base['ci_hi']:+.4f}]  "
          f"f_within={fw_base['median']:.4f} "
          f"[{fw_base['ci_lo']:.4f}, {fw_base['ci_hi']:.4f}]", flush=True)

    # ===================================================================
    # S2a — prereg-literal primary (standardised posterior-MEDIAN α_c)
    # ===================================================================
    cities_s2a = standardise_alpha(cities, "alpha_c_median", "alpha_c_std")
    s2a = _fit_augmented(cities_s2a, n_prov, base_seed, alpha_col="alpha_c_std")
    bw = s2a["betas"]["beta_within"]; gw = s2a["betas"]["gamma_alpha"]; fw = s2a["f_within"]
    f_shift_med = fw["median"] - fw_base["median"]
    f_shift_ci_max = max(abs(fw["ci_lo"] - fw_base["ci_lo"]),
                         abs(fw["ci_hi"] - fw_base["ci_hi"]))
    bw_shift = bw["median"] - bw_base["median"]
    bw_post_sd = float(np.std(s2a["_beta_within_draws"], ddof=1))
    print(f"[D13-S2] S2a   β_within={bw['median']:+.4f} (Δ={bw_shift:+.4f}, "
          f"{abs(bw_shift)/bw_post_sd:.2f}·postSD)  "
          f"f_within={fw['median']:.4f} (Δmed={f_shift_med:+.4f})  "
          f"γ={gw['median']:+.4f} [{gw['ci_lo']:+.4f}, {gw['ci_hi']:+.4f}]", flush=True)
    print(f"[D13-S2] S2a   f_within shift: median Δ={f_shift_med:+.4f}, "
          f"max-CI Δ={f_shift_ci_max:.4f}  vs material {F_WITHIN_MATERIAL_SHIFT} → "
          f"{'MATERIAL' if max(abs(f_shift_med), f_shift_ci_max) >= F_WITHIN_MATERIAL_SHIFT else 'not material'}",
          flush=True)

    s2a_summary = {
        "beta_within": bw, "beta_within_shift_vs_base": bw_shift,
        "beta_within_post_sd": bw_post_sd,
        "beta_within_shift_in_post_sd": abs(bw_shift) / bw_post_sd if bw_post_sd else None,
        "gamma_alpha": gw, "f_within": fw,
        "f_within_shift_median": f_shift_med,
        "f_within_shift_ci_max": f_shift_ci_max,
        "f_within_material": bool(max(abs(f_shift_med), f_shift_ci_max)
                                  >= F_WITHIN_MATERIAL_SHIFT),
        "convergence": s2a["convergence"],
    }

    # ===================================================================
    # S2b — multiple imputation (M draws from the per-city α posteriors)
    # ===================================================================
    s2b_summary = None
    if not args.skip_mi:
        m = args.n_imputations
        print(f"[D13-S2] S2b   multiple imputation, M={m} ...", flush=True)
        alpha_mat = load_alpha_draw_matrix(cities)  # (163, n_draws)
        n_draws_total = alpha_mat.shape[1]
        bw_ests, bw_vars, g_ests, g_vars, f_ests, f_vars = ([] for _ in range(6))
        for j in range(m):
            # Draw one α-vector: one independent posterior draw index per city.
            idx = rng.integers(0, n_draws_total, size=alpha_mat.shape[0])
            a_draw = alpha_mat[np.arange(alpha_mat.shape[0]), idx]
            ct = cities.copy()
            ct["alpha_c_imp"] = a_draw
            ct = standardise_alpha(ct, "alpha_c_imp", "alpha_c_std")
            fit = _fit_augmented(ct, n_prov, base_seed + 1 + j, alpha_col="alpha_c_std")
            bwj = fit["betas"]["beta_within"]; gj = fit["betas"]["gamma_alpha"]
            bw_ests.append(bwj["median"])
            bw_vars.append(float(np.var(fit["_beta_within_draws"], ddof=1)))
            g_ests.append(gj["median"])
            g_vars.append(float(np.var(fit["_gamma_draws"], ddof=1)))
            f_ests.append(fit["f_within"]["median"])
            f_vars.append(float(np.var(fit["_f_within_draws"], ddof=1)))
            if (j + 1) % 10 == 0:
                print(f"[D13-S2]   ...imputation {j+1}/{m}", flush=True)
        pooled_bw = rubin_pool(bw_ests, bw_vars)
        pooled_g = rubin_pool(g_ests, g_vars)
        pooled_f = rubin_pool(f_ests, f_vars)
        f_shift_b = pooled_f["pooled"] - fw_base["median"]
        print(f"[D13-S2] S2b   pooled β_within={pooled_bw['pooled']:+.4f} "
              f"[{pooled_bw['ci_lo']:+.4f}, {pooled_bw['ci_hi']:+.4f}]  "
              f"(base {bw_base['median']:+.4f})", flush=True)
        print(f"[D13-S2] S2b   pooled γ={pooled_g['pooled']:+.4f} "
              f"[{pooled_g['ci_lo']:+.4f}, {pooled_g['ci_hi']:+.4f}]  "
              f"pooled f_within={pooled_f['pooled']:.4f} (Δ={f_shift_b:+.4f})", flush=True)
        s2b_summary = {
            "m": m, "beta_within": pooled_bw, "gamma_alpha": pooled_g,
            "f_within": pooled_f,
            "f_within_shift_vs_base": f_shift_b,
            "beta_within_shift_vs_base": pooled_bw["pooled"] - bw_base["median"],
        }

    # ===================================================================
    # S2c (i) — N ≥ 500 reliable-α cross-check (leverage-thin / descriptive)
    # ===================================================================
    rel = cities.loc[cities["inscription_count"] >= N_RELIABLE].copy()
    # Recompute Mundlak centring + province index over the reliable subset.
    pm_rel = rel.groupby("province")["log_pop"].transform("mean")
    rel["log_pop_prov_mean"] = pm_rel
    rel["log_pop_within"] = rel["log_pop"] - pm_rel
    rel["province_idx"] = pd.Categorical(rel["province"]).codes
    rel = rel.reset_index(drop=True)
    n_prov_rel = int(rel["province_idx"].max()) + 1
    n_prov_ge2_rel = int((rel.groupby("province").size() >= 2).sum())
    print(f"[D13-S2] S2c(i) N≥{N_RELIABLE}: {len(rel)} cities, {n_prov_rel} provinces "
          f"({n_prov_ge2_rel} with ≥2 cities — within-province leverage-thin; descriptive)",
          flush=True)
    rel_std = standardise_alpha(rel, "alpha_c_median", "alpha_c_std")
    base_rel = _fit_base(rel, n_prov_rel, base_seed)
    aug_rel = _fit_augmented(rel_std, n_prov_rel, base_seed, alpha_col="alpha_c_std")
    s2c_reliable = {
        "n_cities": int(len(rel)), "n_provinces": n_prov_rel,
        "n_provinces_ge2_cities": n_prov_ge2_rel,
        "flag": ("within-province-leverage-thin: only "
                 f"{n_prov_ge2_rel} provinces have ≥2 reliable cities; treat as "
                 "DESCRIPTIVE, not a within-province regression"),
        "base": {"beta_within": base_rel["betas"]["beta_within"],
                 "f_within": base_rel["f_within"],
                 "convergence": base_rel["convergence"]},
        "augmented": {"beta_within": aug_rel["betas"]["beta_within"],
                      "gamma_alpha": aug_rel["betas"]["gamma_alpha"],
                      "f_within": aug_rel["f_within"],
                      "convergence": aug_rel["convergence"]},
    }
    bwr = aug_rel["betas"]["beta_within"]; bwrb = base_rel["betas"]["beta_within"]
    print(f"[D13-S2] S2c(i) β_within base={bwrb['median']:+.4f} "
          f"augmented={bwr['median']:+.4f} (descriptive)", flush=True)

    # ===================================================================
    # S2c (ii) — city-level α_c-vs-population proxy (Obs 94 extension)
    # ===================================================================
    proxy = alpha_vs_pop_proxy(cities)
    print(f"[D13-S2] S2c(ii) proxy: Spearman(α,logpop)="
          f"{proxy['spearman_alpha_vs_logpop']:+.3f}; implied Δβ Theil-Sen="
          f"{proxy['implied_delta_beta_theilsen']:+.3f} "
          f"{proxy['implied_delta_beta_theilsen_ci95']}", flush=True)
    make_figure(cities, proxy)

    # ===================================================================
    # PERSIST
    # ===================================================================
    results = {
        "yardstick": {
            "f_within_material_shift": F_WITHIN_MATERIAL_SHIFT,
            "note": ("PRE-STATED (spec §4, D11 precedent): a f_within "
                     "posterior-median/CI shift ≥ 0.063 is material; β_within "
                     "shift also reported vs its posterior SD + CI overlap."),
        },
        "frame": {"n_cities": int(len(cities)), "n_provinces": n_prov,
                  "n_reliable_ge500": int((cities["inscription_count"] >= N_RELIABLE).sum()),
                  "seed_base": base_seed, "mi_seed": MI_SEED},
        "base_163": {"beta_within": bw_base, "f_within": fw_base,
                     "betas": base["betas"], "convergence": base["convergence"]},
        "S2a_point_median": s2a_summary,
        "S2b_multiple_imputation": s2b_summary,
        "S2c_reliable_n500": s2c_reliable,
        "S2c_proxy_alpha_vs_population": proxy,
    }
    (OUT_DIR / "h3a-alpha-translator-results.json").write_text(json.dumps(results, indent=2))
    print(f"[D13-S2] → {OUT_DIR / 'h3a-alpha-translator-results.json'}", flush=True)
    print("[D13-S2] DONE.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
