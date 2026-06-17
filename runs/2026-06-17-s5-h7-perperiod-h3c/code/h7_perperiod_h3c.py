#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h7_perperiod_h3c.py — §5 H7: time-resolved (per-period) H3c.
============================================================

Recompute the H3c diagnostics — provincial-capital residual contrast and Moran's
I spatial clustering of H3a NBR Pearson residuals — within each of 8 fifty-year
periods over 50 BC – AD 350, yielding a time-resolved version of Hanson's (2021)
pooled residual map. Exploratory; no published comparator (preregistration §5).
See ``../spec.md``.

The H3a NBR (build_model / Pearson residuals) and the H3c diagnostics (Moran's I,
capital contrast) are replicated VERBATIM from the audited confirmatory code at
``runs/2026-06-04-h3a-confirmatory/code/`` (02-h3a-fit.py, 04-h3c.py,
06-h3c-i-capital-contrast.py) so this run is self-contained.

Per-period counts use aoristic apportionment (spread each inscription's interval
mass across the periods it covers), rounded to integer; the city universe and the
Mundlak within/between predictors are held fixed across periods (population-based,
so the per-period residual maps are directly comparable).

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-17-s5-h7-perperiod-h3c/code/h7_perperiod_h3c.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-17, on Shawn's brief.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az

warnings.filterwarnings("ignore")

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parents[1]
REPO = THIS.parents[3]
H3A_CODE = REPO / "runs/2026-06-04-h3a-confirmatory/code"
PRIMARY_PARQUET = REPO / "data/processed/city_level_for_h3a.parquet"
CAPITALS_CSV = REPO / "data/processed/provincial-capitals.csv"
OUT_DIR = RUN_DIR / "outputs"

sys.path.insert(0, str(H3A_CODE))
import h3a_common as H  # noqa: E402  (load_filtered_lire, rome_mask)

# --- Period grid (design decision i): 50-year bins over [-50, 350] ----------
PERIOD_EDGES = np.arange(-50, 351, 50)            # [-50, 0, ..., 350] -> 8 bins
N_PERIODS = len(PERIOD_EDGES) - 1
PERIOD_LABELS = [f"{int(PERIOD_EDGES[i])}..{int(PERIOD_EDGES[i+1])}"
                 for i in range(N_PERIODS)]

# --- Sampler (design decision iv): lighter than confirmatory, ×8 fits -------
N_TUNE, N_DRAW, N_CHAINS, TARGET_ACCEPT = 3000, 2000, 4, 0.95
SEED = 20260617
RHAT_GATE, ESS_GATE, DIV_GATE = 1.01, 400, 0

# --- H3c diagnostics config (verbatim from 04-h3c.py) -----------------------
K_VALUES = [5, 8, 10]
PRIMARY_K = 8
N_PERMUTATIONS = 999


# --------------------------------------------------------------------------- #
# Per-period counts: aoristic apportionment over the 50y grid.
# --------------------------------------------------------------------------- #

def aoristic_period_counts() -> pd.DataFrame:
    """Per-city aoristic inscription mass in each 50y period (filtered corpus).

    Returns a DataFrame indexed by city with one column per period label, mass
    summed over the city's inscriptions (each inscription contributes total mass
    = fraction of its [not_before, not_after] interval inside the envelope).
    """
    filtered = H.load_filtered_lire()
    sub = filtered.loc[~H.rome_mask(filtered)
                       & filtered["urban_context_pop_est"].notna()].copy()

    nb = np.clip(sub["not_before"].to_numpy(float), PERIOD_EDGES[0], PERIOD_EDGES[-1])
    na = np.clip(sub["not_after"].to_numpy(float), PERIOD_EDGES[0], PERIOD_EDGES[-1])
    lo, hi = PERIOD_EDGES[:-1][None, :], PERIOD_EDGES[1:][None, :]    # (1, P)
    overlap = np.clip(np.minimum(na[:, None], hi) - np.maximum(nb[:, None], lo),
                      0.0, None)                                       # (N, P)
    width = (na - nb)[:, None]
    weights = np.where(width > 0, overlap / np.where(width > 0, width, 1.0), 0.0)

    # Point dates (not_before == not_after): assign fully to the containing bin.
    pt = (na - nb) == 0
    if pt.any():
        pt_bin = np.clip(np.searchsorted(PERIOD_EDGES, nb[pt], side="right") - 1,
                         0, N_PERIODS - 1)
        weights[pt] = 0.0
        weights[np.flatnonzero(pt), pt_bin] = 1.0

    wdf = pd.DataFrame(weights, columns=PERIOD_LABELS)
    wdf["city"] = sub["urban_context_city"].to_numpy()
    return wdf.groupby("city")[PERIOD_LABELS].sum()


# --------------------------------------------------------------------------- #
# H3a NBR — replicated verbatim from 02-h3a-fit.py.
# --------------------------------------------------------------------------- #

def build_model(cities: pd.DataFrame, n_provinces: int) -> pm.Model:
    y_obs = cities["inscription_count"].to_numpy(dtype=int)
    within = cities["log_pop_within"].to_numpy(dtype=float)
    between = cities["log_pop_prov_mean"].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)
    with pm.Model() as model:
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
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


def fit_period(cities: pd.DataFrame, n_prov: int) -> az.InferenceData:
    with build_model(cities, n_prov):
        return pm.sample(draws=N_DRAW, tune=N_TUNE, chains=N_CHAINS,
                         target_accept=TARGET_ACCEPT, random_seed=SEED,
                         progressbar=False, return_inferencedata=True)


def convergence(idata) -> dict:
    summ = az.summary(idata, var_names=["alpha_0", "beta_within", "beta_between",
                                        "sigma_prov", "inv_dispersion",
                                        "alpha_prov_raw"])
    return {"max_rhat": float(summ["r_hat"].max()),
            "min_ess_bulk": float(summ["ess_bulk"].min()),
            "n_divergences": int(idata.sample_stats["diverging"].sum())}


def gates_pass(c: dict) -> bool:
    return (c["max_rhat"] < RHAT_GATE and c["min_ess_bulk"] >= ESS_GATE
            and c["n_divergences"] <= DIV_GATE)


def pearson_resids_all_draws(idata, y: np.ndarray) -> np.ndarray:
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    alpha = post["dispersion"].values.reshape(-1)
    mu = np.exp(log_mu)
    var = mu + mu ** 2 / alpha[:, None]
    return (y[None, :] - mu) / np.sqrt(var)


# --------------------------------------------------------------------------- #
# H3c diagnostics — replicated from 04-h3c.py / 06-h3c-i-capital-contrast.py.
# --------------------------------------------------------------------------- #

def moran_diagnostics(r_all: np.ndarray, coords: np.ndarray) -> dict:
    from libpysal.weights import KNN
    from esda.moran import Moran

    r_mean = r_all.mean(axis=0)
    per_k, n_pass = {}, 0
    for k in K_VALUES:
        w = KNN.from_array(coords, k=k)
        w.transform = "r"
        mi = Moran(r_mean, w, permutations=N_PERMUTATIONS, two_tailed=False)
        passes = bool((mi.I > 0) and (mi.p_sim < 0.05))
        n_pass += int(passes)
        per_k[str(k)] = {"moran_I": float(mi.I), "p_sim_one_sided": float(mi.p_sim),
                         "z_sim": float(mi.z_sim), "passes_rule": passes}
    return {"per_k": per_k, "n_k_passing": n_pass,
            "clustering_supported": n_pass >= 2}


def capital_contrast(r_all: np.ndarray, cities: pd.DataFrame,
                     capital_set: set) -> dict:
    is_cap = cities["city"].isin(capital_set).to_numpy()
    if is_cap.sum() == 0 or (~is_cap).sum() == 0:
        return {"error": "no capitals or no non-capitals in frame"}
    contrast = r_all[:, is_cap].mean(axis=1) - r_all[:, ~is_cap].mean(axis=1)
    return {"n_capitals": int(is_cap.sum()),
            "p_contrast_gt_0": float((contrast > 0).mean()),
            "contrast_median": float(np.median(contrast)),
            "supported": bool((contrast > 0).mean() >= 0.95)}


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = pd.read_parquet(PRIMARY_PARQUET)
    n_prov = int(base["province_idx"].max()) + 1
    coords = base[["longitude", "latitude"]].to_numpy(dtype=float)
    capital_set = set(pd.read_csv(CAPITALS_CSV)["city"])
    counts = aoristic_period_counts()
    pooled_total = int(base["inscription_count"].sum())

    print(f"H7: {N_PERIODS} periods, {len(base)} cities, {n_prov} provinces; "
          f"pooled count {pooled_total}; capitals {len(capital_set)}")

    per_city_resid = base[["city", "province", "longitude", "latitude"]].copy()
    results = {}
    for label in PERIOD_LABELS:
        frame = base.copy()
        period_mass = frame["city"].map(counts[label]).fillna(0.0)
        frame["inscription_count"] = np.rint(period_mass).astype(int)
        n_nonzero = int((frame["inscription_count"] > 0).sum())
        tot = int(frame["inscription_count"].sum())
        print(f"\n[{label}] non-zero cities={n_nonzero} total={tot} — fitting NBR ...")

        idata = fit_period(frame, n_prov)
        conv = convergence(idata)
        ok = gates_pass(conv)
        if not ok:
            print(f"  !! WARNING [{label}] convergence gates not met: "
                  f"R̂={conv['max_rhat']:.4f} ESS={conv['min_ess_bulk']:.0f} "
                  f"div={conv['n_divergences']} — period read is provisional.")
        else:
            print(f"  converged: R̂={conv['max_rhat']:.4f} "
                  f"ESS={conv['min_ess_bulk']:.0f} div={conv['n_divergences']}")

        y = frame["inscription_count"].to_numpy(float)
        r_all = pearson_resids_all_draws(idata, y)
        per_city_resid[f"resid_{label}"] = r_all.mean(axis=0)

        beta = idata.posterior["beta_within"].values.reshape(-1)
        moran = moran_diagnostics(r_all, coords)
        cap = capital_contrast(r_all, frame, capital_set)
        k8 = moran["per_k"][str(PRIMARY_K)]
        print(f"  β_within={np.median(beta):+.3f} | capital P(>0)="
              f"{cap.get('p_contrast_gt_0', float('nan')):.3f} | "
              f"Moran k8 I={k8['moran_I']:+.4f} p={k8['p_sim_one_sided']:.4f}")

        results[label] = {
            "n_nonzero_cities": n_nonzero, "total_count": tot,
            "convergence": conv, "gates_pass": ok,
            "beta_within_median": float(np.median(beta)),
            "beta_within_ci": [float(np.percentile(beta, 2.5)),
                               float(np.percentile(beta, 97.5))],
            "capital_contrast": cap, "moran": moran,
        }
        idata.to_netcdf(str(OUT_DIR / f"h7-idata-{label.replace('..','_')}.nc"))

    per_city_resid.to_parquet(OUT_DIR / "h7-per-city-residuals.parquet")
    summary = {
        "n_periods": N_PERIODS, "period_edges": PERIOD_EDGES.tolist(),
        "period_labels": PERIOD_LABELS, "n_cities": len(base),
        "sampler": {"tune": N_TUNE, "draws": N_DRAW, "chains": N_CHAINS,
                    "target_accept": TARGET_ACCEPT, "seed": SEED},
        "design": {"resolution": "50y (8 periods)",
                   "count_construction": "aoristic-apportioned, rounded to int",
                   "city_universe": "fixed 1044; Mundlak population-based"},
        "per_period": results,
        "note": "Exploratory time-resolved H3c (prereg §5 line 384); no thresholds.",
    }
    with open(OUT_DIR / "h7-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=_json_default)
    plots(results)
    print("\nH7 done. Summary at outputs/h7-summary.json")


def plots(results: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = list(results.keys())
    x = np.arange(len(labels))
    centres = [(PERIOD_EDGES[i] + PERIOD_EDGES[i + 1]) / 2 for i in range(len(labels))]
    beta = [results[l]["beta_within_median"] for l in labels]
    beta_lo = [results[l]["beta_within_ci"][0] for l in labels]
    beta_hi = [results[l]["beta_within_ci"][1] for l in labels]
    cap_p = [results[l]["capital_contrast"].get("p_contrast_gt_0", np.nan) for l in labels]
    moran_I = [results[l]["moran"]["per_k"]["8"]["moran_I"] for l in labels]
    moran_p = [results[l]["moran"]["per_k"]["8"]["p_sim_one_sided"] for l in labels]

    fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
    axes[0].errorbar(centres, beta,
                     yerr=[np.array(beta) - np.array(beta_lo),
                           np.array(beta_hi) - np.array(beta)],
                     marker="o", capsize=3)
    axes[0].set_title("β_within over time"); axes[0].set_xlabel("year")
    axes[0].set_ylabel("β_within")
    axes[1].plot(centres, cap_p, marker="o", color="C1")
    axes[1].axhline(0.95, ls="--", color="grey", label="0.95")
    axes[1].set_title("Capital over-production P(contrast>0)")
    axes[1].set_xlabel("year"); axes[1].set_ylabel("P(>0)"); axes[1].legend()
    axes[2].plot(centres, moran_I, marker="o", color="C2", label="Moran I (k8)")
    for xi, p in zip(centres, moran_p):
        axes[2].annotate(f"p={p:.2f}", (xi, 0), fontsize=7, rotation=90)
    axes[2].axhline(0, color="k", lw=0.6)
    axes[2].set_title("Spatial clustering Moran's I (k=8)")
    axes[2].set_xlabel("year"); axes[2].set_ylabel("Moran's I")
    fig.suptitle("H7 — time-resolved H3c (50y periods)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "h7-time-resolved.png", dpi=130)
    plt.close(fig)


def _json_default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"Unserialisable: {type(o)}")


if __name__ == "__main__":
    main()
