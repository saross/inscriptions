#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
peak_scaling.py — §5: peak-inscription vs Hanson-population scaling.
===================================================================

Does *peak* inscription intensity scale with population, and is the exponent
different from the cumulative H3a scaling (beta_within^cumulative = 0.587)? Two
arms + an overlap contrast (Shawn's direction). Exploratory / tertiary (not
preregistered). See ``../spec.md``.

- Arm A: raw aoristic peak count (max over 50y periods; 25y sensitivity), all
  1044 H3a cities, parquet Mundlak. Headline vs the cumulative beta.
- Arm B: modelled trajectory peak (round(max_t median lam)), 268 §5 cities,
  Mundlak recomputed over the subset.
- Overlap (268 §5 cities, 25y): raw-25y vs modelled-25y → effect of smoothing.

The NBR (build_model / sample / Pearson) is the audited H3a model (replicated
from runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py).

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-17-s5-peak-scaling/code/peak_scaling.py

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
LAYER_A_CODE = REPO / "runs/2026-05-30-s5-small-n-trajectories/code"
PRIMARY_PARQUET = REPO / "data/processed/city_level_for_h3a.parquet"
CITY_INDEX = LAYER_A_CODE / "prepared/city-index.parquet"
LAYERA_NC = LAYER_A_CODE / "production/monolithic-inscription-25y.nc"
OUT_DIR = RUN_DIR / "outputs"

sys.path.insert(0, str(H3A_CODE))
import h3a_common as H  # noqa: E402

N_TUNE, N_DRAW, N_CHAINS, TARGET_ACCEPT, SEED = 3000, 2000, 4, 0.95, 20260617
BETA_CUMULATIVE = {"median": 0.587, "ci": [0.519, 0.657]}   # H3a confirmatory


# --------------------------------------------------------------------------- #
# Peak-count builders.
# --------------------------------------------------------------------------- #

def aoristic_peak_counts(bin_width: int) -> pd.Series:
    """Per-city peak (busiest-bin) aoristic count on a grid of given width."""
    edges = np.arange(-50, 351, bin_width)
    n_bins = len(edges) - 1
    filtered = H.load_filtered_lire()
    sub = filtered.loc[~H.rome_mask(filtered)
                       & filtered["urban_context_pop_est"].notna()].copy()
    nb = np.clip(sub["not_before"].to_numpy(float), edges[0], edges[-1])
    na = np.clip(sub["not_after"].to_numpy(float), edges[0], edges[-1])
    lo, hi = edges[:-1][None, :], edges[1:][None, :]
    overlap = np.clip(np.minimum(na[:, None], hi) - np.maximum(nb[:, None], lo),
                      0.0, None)
    width = (na - nb)[:, None]
    w = np.where(width > 0, overlap / np.where(width > 0, width, 1.0), 0.0)
    pt = (na - nb) == 0
    if pt.any():
        pb = np.clip(np.searchsorted(edges, nb[pt], side="right") - 1, 0, n_bins - 1)
        w[pt] = 0.0
        w[np.flatnonzero(pt), pb] = 1.0
    cols = [f"b{i}" for i in range(n_bins)]
    wdf = pd.DataFrame(w, columns=cols)
    wdf["city"] = sub["urban_context_city"].to_numpy()
    per_bin = wdf.groupby("city")[cols].sum()
    return per_bin.max(axis=1).round().astype(int)            # peak count per city


def modelled_peak_counts() -> pd.Series:
    """Per-§5-city modelled peak count = round(max_t median(lam))."""
    post = az.from_netcdf(str(LAYERA_NC)).posterior["lam"]     # (chain,draw,city,bin)
    med = post.median(dim=("chain", "draw"))                  # (city, bin)
    peak = med.max(dim="bin").values
    cities = [str(c) for c in post.coords["city"].values]
    return pd.Series(np.rint(peak).astype(int), index=cities)


# --------------------------------------------------------------------------- #
# Frames.
# --------------------------------------------------------------------------- #

def frame_1044(peak: pd.Series) -> tuple[pd.DataFrame, int]:
    """Full H3a frame with inscription_count replaced by the peak count."""
    base = pd.read_parquet(PRIMARY_PARQUET).copy()
    base["inscription_count"] = base["city"].map(peak).fillna(0).round().astype(int)
    return base, int(base["province_idx"].max()) + 1


def frame_268(peak: pd.Series) -> tuple[pd.DataFrame, int]:
    """268 §5-city frame; Mundlak recomputed over the subset."""
    idx = pd.read_parquet(CITY_INDEX)
    sub = idx[idx["bucket"] == "target"].copy()               # 268 target cities
    sub = sub.rename(columns={"pop_est": "urban_context_pop_est"})
    sub["log_pop"] = np.log(sub["urban_context_pop_est"])
    pm_ = sub.groupby("province")["log_pop"].transform("mean")
    sub["log_pop_prov_mean"] = pm_
    sub["log_pop_within"] = sub["log_pop"] - pm_
    sub["province_idx"] = pd.Categorical(sub["province"]).codes
    sub["inscription_count"] = sub["city"].map(peak).fillna(0).round().astype(int)
    return sub.reset_index(drop=True), int(sub["province_idx"].max()) + 1


# --------------------------------------------------------------------------- #
# NBR (replicated from 02-h3a-fit.py).
# --------------------------------------------------------------------------- #

def fit_beta(cities: pd.DataFrame, n_prov: int, label: str) -> dict:
    y = cities["inscription_count"].to_numpy(int)
    within = cities["log_pop_within"].to_numpy(float)
    between = cities["log_pop_prov_mean"].to_numpy(float)
    pidx = cities["province_idx"].to_numpy(int)
    with pm.Model():
        alpha_0 = pm.Normal("alpha_0", 0.0, 5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", 1.0)
        a_raw = pm.Normal("alpha_prov_raw", 0.0, 1.0, shape=n_prov)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * a_raw)
        beta_within = pm.Normal("beta_within", 0.0, 1.0)
        beta_between = pm.Normal("beta_between", 0.0, 1.0)
        inv_disp = pm.HalfNormal("inv_dispersion", 1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)
        log_mu = (alpha_0 + alpha_prov[pidx]
                  + beta_within * within + beta_between * between)
        mu = pm.math.exp(log_mu)
        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y)
        idata = pm.sample(draws=N_DRAW, tune=N_TUNE, chains=N_CHAINS,
                          target_accept=TARGET_ACCEPT, random_seed=SEED,
                          progressbar=False, return_inferencedata=True)
    summ = az.summary(idata, var_names=["beta_within", "beta_between", "alpha_0"])
    bw = idata.posterior["beta_within"].values.reshape(-1)
    conv = {"max_rhat": float(summ["r_hat"].max()),
            "min_ess_bulk": float(summ["ess_bulk"].min()),
            "n_divergences": int(idata.sample_stats["diverging"].sum())}
    ok = conv["max_rhat"] < 1.01 and conv["min_ess_bulk"] >= 400 and conv["n_divergences"] == 0
    if not ok:
        print(f"  !! WARNING [{label}] gates not met: {conv}")
    res = {"label": label, "n_cities": int(len(cities)),
           "n_nonzero": int((y > 0).sum()), "total_count": int(y.sum()),
           "beta_within_median": float(np.median(bw)),
           "beta_within_ci": [float(np.percentile(bw, 2.5)),
                              float(np.percentile(bw, 97.5))],
           "convergence": conv, "gates_pass": ok}
    print(f"  [{label}] beta_within={res['beta_within_median']:+.3f} "
          f"[{res['beta_within_ci'][0]:+.3f},{res['beta_within_ci'][1]:+.3f}] "
          f"n={res['n_cities']} (R̂={conv['max_rhat']:.4f})")
    return res


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Building peak counts ...")
    raw50 = aoristic_peak_counts(50)
    raw25 = aoristic_peak_counts(25)
    modelled = modelled_peak_counts()
    print(f"  raw50 cities={len(raw50)} | raw25 cities={len(raw25)} | "
          f"modelled §5 cities={len(modelled)}")

    arms = {}
    # Arm A — full 1044.
    f, np_ = frame_1044(raw50); arms["raw_peak_50y_1044"] = fit_beta(f, np_, "raw_peak_50y_1044")
    f, np_ = frame_1044(raw25); arms["raw_peak_25y_1044"] = fit_beta(f, np_, "raw_peak_25y_1044")
    # Arm B + overlap — 268 §5.
    f, np_ = frame_268(raw25); arms["raw_peak_25y_268"] = fit_beta(f, np_, "raw_peak_25y_268")
    f, np_ = frame_268(modelled); arms["modelled_peak_25y_268"] = fit_beta(f, np_, "modelled_peak_25y_268")

    summary = {
        "beta_cumulative_reference": BETA_CUMULATIVE,
        "sampler": {"tune": N_TUNE, "draws": N_DRAW, "chains": N_CHAINS,
                    "target_accept": TARGET_ACCEPT, "seed": SEED},
        "arms": arms,
        "contrasts": {
            "headline_peak50_vs_cumulative": {
                "beta_peak_raw_50y_1044": arms["raw_peak_50y_1044"]["beta_within_median"],
                "beta_cumulative": BETA_CUMULATIVE["median"],
            },
            "overlap_smoothing_268_25y": {
                "raw": arms["raw_peak_25y_268"]["beta_within_median"],
                "modelled": arms["modelled_peak_25y_268"]["beta_within_median"],
            },
        },
        "note": ("Exploratory/tertiary; peak-scaling vs cumulative. Arm B uses "
                 "posterior-median modelled peak (trajectory posterior not "
                 "propagated into beta)."),
    }
    with open(OUT_DIR / "peak-scaling-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=_json_default)
    plot(arms)
    print("\nDone. Summary at outputs/peak-scaling-summary.json")


def plot(arms: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [("cumulative (H3a)", BETA_CUMULATIVE["median"],
             BETA_CUMULATIVE["ci"][0], BETA_CUMULATIVE["ci"][1])]
    for k in ["raw_peak_50y_1044", "raw_peak_25y_1044",
              "raw_peak_25y_268", "modelled_peak_25y_268"]:
        a = arms[k]
        rows.append((k, a["beta_within_median"], *a["beta_within_ci"]))
    labels = [r[0] for r in rows]
    y = np.arange(len(rows))[::-1]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for yi, (_, m, lo, hi) in zip(y, rows):
        ax.plot([lo, hi], [yi, yi], color="C0")
        ax.plot(m, yi, "o", color="C0")
    ax.axvline(BETA_CUMULATIVE["median"], ls="--", color="grey",
               label=f"cumulative {BETA_CUMULATIVE['median']}")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("β_within"); ax.set_title("Peak vs cumulative scaling exponent")
    ax.legend(); fig.tight_layout()
    fig.savefig(OUT_DIR / "peak-scaling-forest.png", dpi=130); plt.close(fig)


def _json_default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    raise TypeError(f"Unserialisable: {type(o)}")


if __name__ == "__main__":
    main()
