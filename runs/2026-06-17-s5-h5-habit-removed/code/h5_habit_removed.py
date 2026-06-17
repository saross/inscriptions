#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h5_habit_removed.py — §5 H5: habit-removed residual trajectory analysis.
========================================================================

Decompose each city's Layer-A inscription-rate trajectory into an empire-wide
*epigraphic-habit* component and a *city-specific residual*, and report the
residual trajectories + the **epigraphic-habit lag** (the offset between a city's
raw inscription peak and its habit-removed residual peak). Exploratory; no
pre-committed thresholds (Decision 13 / preregistration §5). See ``../spec.md``.

No new sampling — the Layer-A hierarchical model already factors the per-city
log-rate, so H5 reads the existing posterior::

    log_lam[c,t] = alpha_g + g_shape[t]            (empire-wide habit)
                 + b_u[p] + u_shape[p,t]           (province)
                 + b_v[c] + v_shape[c,t]           (city)

- empire-wide habit component  = alpha_g + g_shape[t]
- habit-removed residual (shape) = u_shape[p(c),t] + v_shape[c,t]
  (singleton-province cities have no u tier -> residual = v_shape[c,t])

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-17-s5-h5-habit-removed/code/h5_habit_removed.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-17, on Shawn's brief.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parents[1]
REPO = THIS.parents[3]
LAYER_A_CODE = REPO / "runs/2026-05-30-s5-small-n-trajectories/code"
PRIMARY_NC = LAYER_A_CODE / "production/monolithic-inscription-25y.nc"
CITY_INDEX = LAYER_A_CODE / "prepared/city-index.parquet"
HANSON_CITIES = REPO / "data/hanson2016/hanson2016_cities_oxrep.csv"
OUT_DIR = RUN_DIR / "outputs"

sys.path.insert(0, str(LAYER_A_CODE))
import dataprep as dp  # noqa: E402

BIN_EDGES = dp.BIN_EDGES                          # 17 edges: -50, -25, ..., 350
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0
BIN_WIDTH = dp.BIN_WIDTH                          # 25
T_BINS = dp.N_BINS                               # 16
N_STAR = 300


def _stack(da):
    """Stack (chain, draw) -> sample as the leading axis; return ndarray + dims."""
    other = [d for d in da.dims if d not in ("chain", "draw")]
    arr = da.stack(sample=("chain", "draw")).transpose("sample", *other).values
    return arr.astype(np.float64)


def load_posterior():
    """Load the decomposition tiers + lam + coords from the Layer-A posterior."""
    import arviz as az

    post = az.from_netcdf(str(PRIMARY_NC)).posterior
    g = _stack(post["g_shape"])                  # (S, T)
    u = _stack(post["u_shape"])                  # (S, P, T)
    v = _stack(post["v_shape"])                  # (S, C, T)
    lam = _stack(post["lam"])                    # (S, C, T)
    cities = [str(c) for c in post["v_shape"].coords["city"].values]
    provs = [str(p) for p in post["u_shape"].coords["prov"].values]
    return g, u, v, lam, cities, provs


def city_u_rows(cities: list[str], provs: list[str]) -> np.ndarray:
    """Map each city to its u-tier row (province index), or -1 if singleton."""
    idx = pd.read_parquet(CITY_INDEX).set_index("city")
    prov_row = {p: i for i, p in enumerate(provs)}
    rows = []
    for c in cities:
        prov = idx.loc[c, "province"] if c in idx.index else None
        rows.append(prov_row.get(prov, -1))
    return np.array(rows, dtype=int)


def peak_year(bin_argmax: np.ndarray) -> np.ndarray:
    """Convert a bin-index array to bin-centre years."""
    return BIN_CENTRES[bin_argmax]


def summarise():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g, u, v, lam, cities, provs = load_posterior()
    S, C, T = lam.shape
    urows = city_u_rows(cities, provs)

    # Habit-removed residual (shape): u_shape[p(c)] + v_shape[c]; 0 u for singletons.
    u_pad = np.concatenate([u, np.zeros((S, 1, T))], axis=1)   # row -1 -> zeros
    residual = v + u_pad[:, urows, :]                          # (S, C, T)

    raw_peak_bin = np.argmax(lam, axis=2)                      # (S, C)
    res_peak_bin = np.argmax(residual, axis=2)                # (S, C)
    habit_peak_bin = np.argmax(g, axis=1)                     # (S,)

    lag_years = peak_year(raw_peak_bin) - peak_year(res_peak_bin)   # (S, C)

    def band(a, axis=0):
        return (np.median(a, axis=axis),
                np.percentile(a, 2.5, axis=axis),
                np.percentile(a, 97.5, axis=axis))

    res_med, res_lo, res_hi = band(residual)                  # (C, T)
    raw_med = np.median(lam, axis=0)                          # (C, T)
    g_med, g_lo, g_hi = band(g)                               # (T,)

    idx = pd.read_parquet(CITY_INDEX).set_index("city")
    N = np.array([int(idx.loc[c, "N"]) for c in cities])
    reliable = N >= N_STAR

    # Per-city peak summaries + lag.
    raw_peak_mode = np.array([np.bincount(raw_peak_bin[:, c], minlength=T).argmax()
                              for c in range(C)])
    res_peak_mode = np.array([np.bincount(res_peak_bin[:, c], minlength=T).argmax()
                              for c in range(C)])
    lag_med_per_city = np.median(lag_years, axis=0)           # (C,)
    lag_lo = np.percentile(lag_years, 2.5, axis=0)
    lag_hi = np.percentile(lag_years, 97.5, axis=0)

    habit_peak_mode = int(np.bincount(habit_peak_bin, minlength=T).argmax())

    # ---- Foundation-date terminus check (best-effort Hanson join) ----------
    foundation = foundation_terminus(cities, lam)

    # ---- Persist ----------------------------------------------------------
    save_nc(cities, res_med, res_lo, res_hi, raw_med, N, reliable,
            raw_peak_mode, res_peak_mode, lag_med_per_city, lag_lo, lag_hi,
            g_med, g_lo, g_hi)

    summary = {
        "n_cities": C, "n_reliable": int(reliable.sum()), "n_star": N_STAR,
        "empire_habit_peak_bin": habit_peak_mode,
        "empire_habit_peak_year": float(BIN_CENTRES[habit_peak_mode]),
        "habit_lag_years": {
            "definition": "raw inscription peak year - habit-removed residual peak year, per city (median over draws)",
            "corpus_median": float(np.median(lag_med_per_city)),
            "corpus_median_reliable": float(np.median(lag_med_per_city[reliable])),
            "iqr": [float(np.percentile(lag_med_per_city, 25)),
                    float(np.percentile(lag_med_per_city, 75))],
            "frac_positive": float((lag_med_per_city > 0).mean()),
        },
        "foundation_terminus": foundation,
        "provenance": {"primary_nc": str(PRIMARY_NC)},
        "note": "Exploratory; no pre-committed thresholds (Decision 13). Residual = u_shape + v_shape.",
    }
    with open(OUT_DIR / "h5-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=_json_default)

    plots(cities, g_med, g_lo, g_hi, res_med, res_lo, res_hi, raw_med,
          reliable, lag_med_per_city, habit_peak_mode)
    print("H5 done. Empire habit peak:", summary["empire_habit_peak_year"],
          "| corpus habit-lag median (reliable):",
          round(summary["habit_lag_years"]["corpus_median_reliable"], 1), "yr")
    print("  foundation coverage:", foundation["n_within_envelope_matched"],
          "within-envelope foundations checked")


def foundation_terminus(cities: list[str], lam: np.ndarray) -> dict:
    """Hanson Start Date terminus check for within-envelope foundations."""
    try:
        han = pd.read_csv(HANSON_CITIES, encoding="latin-1")
    except Exception as e:  # pragma: no cover
        return {"error": f"could not read Hanson cities: {e}"}
    name_col = "Ancient Toponym"
    start = (han[[name_col, "Start Date"]].dropna()
             .assign(key=lambda d: d[name_col].astype(str).str.strip().str.lower()))
    sd = dict(zip(start["key"], start["Start Date"]))

    lam_med = np.median(lam, axis=0)                          # (C, T)
    results, n_match, n_within = [], 0, 0
    for c, name in enumerate(cities):
        s = sd.get(name.strip().lower())
        if s is None:
            continue
        n_match += 1
        if not (-50 < float(s) < 350):       # only within-envelope foundations bind
            continue
        n_within += 1
        # bins fully before the foundation date (upper edge <= Start Date)
        pre = BIN_EDGES[1:] <= float(s)
        frac = float(lam_med[c, pre].sum() / max(lam_med[c].sum(), 1e-12))
        results.append({"city": name, "start_date": float(s),
                        "pre_foundation_mass_frac": round(frac, 4)})
    results.sort(key=lambda r: -r["pre_foundation_mass_frac"])
    return {
        "n_matched": n_match, "n_within_envelope_matched": n_within,
        "median_pre_foundation_frac": (
            float(np.median([r["pre_foundation_mass_frac"] for r in results]))
            if results else None),
        "worst_offenders": results[:10],
    }


def save_nc(cities, res_med, res_lo, res_hi, raw_med, N, reliable,
            raw_peak_mode, res_peak_mode, lag_med, lag_lo, lag_hi,
            g_med, g_lo, g_hi):
    import xarray as xr

    ds = xr.Dataset(
        {
            "residual_med": (("city", "bin"), res_med),
            "residual_lo": (("city", "bin"), res_lo),
            "residual_hi": (("city", "bin"), res_hi),
            "raw_med": (("city", "bin"), raw_med),
            "raw_peak_bin": (("city",), raw_peak_mode),
            "residual_peak_bin": (("city",), res_peak_mode),
            "habit_lag_years_med": (("city",), lag_med),
            "habit_lag_years_lo": (("city",), lag_lo),
            "habit_lag_years_hi": (("city",), lag_hi),
            "N": (("city",), N),
            "reliable": (("city",), reliable),
            "habit_med": (("bin",), g_med),
            "habit_lo": (("bin",), g_lo),
            "habit_hi": (("bin",), g_hi),
        },
        coords={"city": cities, "bin": np.arange(T_BINS),
                "bin_centre_year": ("bin", BIN_CENTRES)},
        attrs={"analysis": "H5 habit-removed residual trajectory",
               "note": "Exploratory; residual = u_shape + v_shape."},
    )
    ds.to_netcdf(str(OUT_DIR / "h5-residual-trajectories.nc"))


def plots(cities, g_med, g_lo, g_hi, res_med, res_lo, res_hi, raw_med,
          reliable, lag_med, habit_peak_mode):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # (a) empire habit curve
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.fill_between(BIN_CENTRES, g_lo, g_hi, alpha=0.25, color="C3")
    ax.plot(BIN_CENTRES, g_med, color="C3", lw=2)
    ax.axvline(BIN_CENTRES[habit_peak_mode], ls="--", color="grey",
               label=f"habit peak AD {int(BIN_CENTRES[habit_peak_mode])}")
    ax.set_title("Empire-wide epigraphic-habit component (g_shape)")
    ax.set_xlabel("year (bin centre)"); ax.set_ylabel("log-rate deviation (zero-sum)")
    ax.legend(); fig.tight_layout()
    fig.savefig(OUT_DIR / "h5-empire-habit.png", dpi=130); plt.close(fig)

    # (b) sample reliable-city residual trajectories
    rel = [i for i in range(len(cities)) if reliable[i]]
    pick = rel[:: max(1, len(rel) // 6)][:6]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, i in zip(axes.ravel(), pick):
        ax.fill_between(BIN_CENTRES, res_lo[i], res_hi[i], alpha=0.2, color="C0")
        ax.plot(BIN_CENTRES, res_med[i], color="C0", lw=2, label="residual")
        ax.set_title(cities[i]); ax.axhline(0, color="grey", lw=0.6)
        ax.set_xlabel("year"); ax.set_ylabel("habit-removed residual")
    fig.suptitle("Habit-removed residual trajectories (sample reliable cities)")
    fig.tight_layout(); fig.savefig(OUT_DIR / "h5-residual-samples.png", dpi=130)
    plt.close(fig)

    # (c) habit-lag histogram (reliable cities)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(lag_med[reliable], bins=15, color="C2", alpha=0.8)
    ax.axvline(0, color="k", lw=1)
    ax.axvline(float(np.median(lag_med[reliable])), color="C3", ls="--",
               label=f"median {np.median(lag_med[reliable]):.0f} yr")
    ax.set_title("Epigraphic-habit lag (raw peak − residual peak), reliable cities")
    ax.set_xlabel("lag (years)"); ax.set_ylabel("cities"); ax.legend()
    fig.tight_layout(); fig.savefig(OUT_DIR / "h5-habit-lag-hist.png", dpi=130)
    plt.close(fig)


def _json_default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"Unserialisable: {type(o)}")


if __name__ == "__main__":
    summarise()
