#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06-h3c-i-capital-contrast.py --- H3c(i): the provincial-capital residual
contrast, on BOTH frames (empire + Latin). NO RE-FIT.

This closes the missed binding confirmatory test H3c(i) flagged in the
completeness audit (planning/prereg-obligations-audit-2026-06-05.md, F1). The
H3a confirmatory run computed and reported H3c(ii) (Moran's I) only; the
provincial-capital contrast was never run because no capital indicator existed.
That indicator is now assembled in data/processed/provincial-capitals.csv (see
build_provincial_capitals.py).

The test (prereg §3 line 81; §4 line 345; Decision 23)
------------------------------------------------------
Pearson residuals are computed EXACTLY as for H3c(ii):

    r_c,s = (y_c - mu_c,s) / sqrt(mu_c,s + mu_c,s^2 / phi_s)

with mu_c,s = exp(log_mu_c,s) (full city-level posterior mean including the
province random intercept) and phi_s the posterior overdispersion draw.

Per posterior draw s:

    contrast_s = mean(r_c,s | c in provincial_capitals)
               - mean(r_c,s | c not in provincial_capitals)

Confirmatory rule (BINARY, draw-wise posterior contrast --- NOT a frequentist
t-test, per Decision 23):

    SUPPORTED  iff  P(contrast_s > 0) >= 0.95  over draws
    NOT-SUPPORTED otherwise

This also answers secondary question SR2(i) (capital over-production).

The residual machinery is the verbatim `pearson_resids_all_draws` from
04-h3c.py / 05-h3c-sr1-latin.py. Residual ordering aligns with the city frame
parquet row order (the H3a fit indexed cities in parquet order; this script
reads the same parquet, so log_mu_dim_0[i] is parquet row i).

Inputs
------
runs/2026-06-04-h3a-confirmatory/outputs/idata-primary.nc   (empire posterior)
runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc     (Latin posterior)
data/processed/city_level_for_h3a.parquet                   (1,044 cities)
data/processed/city_level_for_h3a_latin.parquet             (817 cities)
data/processed/provincial-capitals.csv                      (capital indicator)

Outputs
-------
runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results.json

Status label
------------
PRELIMINARY --- pending Shawn's sign-off; Latin frame additionally pending OSF
Amendment 02 (Decision 36 amendment-gate).

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-05, H3c(i) close-out brief.
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

import h3a_common as H

warnings.filterwarnings("ignore")

CONFIRMATORY_THRESHOLD = 0.95  # P(contrast > 0) >= 0.95 -> SUPPORTED
CAPITALS_CSV = H.PROCESSED_DIR / "provincial-capitals.csv"

# Major capitals whose absence from a frame's flag set would indicate a
# name-matching failure (hard-stop sentinel; empire frame).
SENTINEL_CAPITALS_EMPIRE = {
    "Carthago", "Tarraco", "Corduba", "Augusta Emerita", "Lugdunum",
    "Salona", "Ephesus", "Antiochia (Syria)", "Alexandria (Aegyptus)",
}


def pearson_resids_all_draws(idata: az.InferenceData,
                             y: np.ndarray) -> np.ndarray:
    """Return (S, C) Pearson residuals across all posterior draws.

    Verbatim from 04-h3c.py: r = (y - mu) / sqrt(mu + mu^2 / phi), with
    mu = exp(log_mu) and phi the NBR dispersion, per posterior draw.
    """
    post = idata.posterior
    n = post.sizes["chain"] * post.sizes["draw"]
    log_mu = post["log_mu"].values.reshape(n, -1)
    alpha = post["dispersion"].values.reshape(-1)
    mu = np.exp(log_mu)
    var = mu + mu ** 2 / alpha[:, None]
    return (y[None, :] - mu) / np.sqrt(var)


def capital_contrast(idata: az.InferenceData,
                     cities: pd.DataFrame,
                     capital_set: set[str],
                     frame_label: str) -> dict:
    """Compute the draw-wise capital-vs-non-capital Pearson-residual contrast.

    Parameters
    ----------
    idata : posterior InferenceData (must carry log_mu + dispersion).
    cities : the city frame (parquet row order == posterior city order).
    capital_set : set of `city` values flagged as provincial capitals.
    frame_label : human-readable frame name for the result dict.

    Returns
    -------
    dict with the verdict, median contrast, 95% CI, P(contrast>0), the
    capital / non-capital residual means, and n_capitals / n_noncapitals.
    """
    y = cities["inscription_count"].to_numpy(dtype=float)
    is_capital = cities["city"].isin(capital_set).to_numpy()
    n_cap = int(is_capital.sum())
    n_non = int((~is_capital).sum())

    if n_cap == 0:
        raise RuntimeError(
            f"[{frame_label}] HARD-STOP: zero capitals matched in frame "
            f"--- name-matching failure.")

    r_all = pearson_resids_all_draws(idata, y)        # (S, C)
    n_draws = r_all.shape[0]
    print(f"[06-h3c-i:{frame_label}] residuals: {n_draws} draws x "
          f"{r_all.shape[1]} cities | capitals={n_cap} non-capitals={n_non}")

    # Draw-wise contrast: per draw s, mean cap residual - mean non-cap residual.
    cap_mean_s = r_all[:, is_capital].mean(axis=1)     # (S,)
    non_mean_s = r_all[:, ~is_capital].mean(axis=1)    # (S,)
    contrast_s = cap_mean_s - non_mean_s               # (S,)

    p_above0 = float((contrast_s > 0).mean())
    median_contrast = float(np.median(contrast_s))
    ci_lo, ci_hi = (float(x) for x in np.percentile(contrast_s, [2.5, 97.5]))
    supported = p_above0 >= CONFIRMATORY_THRESHOLD
    verdict = "SUPPORTED" if supported else "NOT-SUPPORTED"

    # Posterior-mean residual summaries (descriptive context / SR2(i)).
    r_mean = r_all.mean(axis=0)                         # posterior-mean per city
    cap_resid_mean = float(r_mean[is_capital].mean())
    non_resid_mean = float(r_mean[~is_capital].mean())

    print(f"[06-h3c-i:{frame_label}] median contrast={median_contrast:+.4f} "
          f"95% CI [{ci_lo:+.4f}, {ci_hi:+.4f}] | "
          f"P(contrast>0)={p_above0:.4f} -> {verdict}")
    print(f"[06-h3c-i:{frame_label}] posterior-mean residual: "
          f"capitals={cap_resid_mean:+.4f} non-capitals={non_resid_mean:+.4f}")

    return {
        "frame": frame_label,
        "confirmatory_rule": "P(contrast_s > 0) >= 0.95 over draws "
                             "(draw-wise posterior contrast; NOT a t-test; "
                             "Decision 23)",
        "verdict": verdict,
        "supported": supported,
        "median_contrast": median_contrast,
        "contrast_ci95": [ci_lo, ci_hi],
        "p_contrast_above_0": p_above0,
        "n_capitals": n_cap,
        "n_noncapitals": n_non,
        "n_posterior_draws": int(n_draws),
        "posterior_mean_residual_capitals": cap_resid_mean,
        "posterior_mean_residual_noncapitals": non_resid_mean,
        "capital_cities": sorted(cities.loc[is_capital, "city"].tolist()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="H3c(i) provincial-capital residual contrast (both frames).")
    parser.add_argument(
        "--capitals-csv", type=Path, default=CAPITALS_CSV,
        help="Capital-indicator CSV (default: the OXREP-primary "
             "provincial-capitals.csv; pass provincial-capitals-ad117.csv for "
             "the AD-117/Barrington sensitivity).")
    parser.add_argument(
        "--label", type=str, default="oxrep-primary",
        help="Output label; results go to h3c-i-results-<label>.json.")
    args = parser.parse_args()

    out_dir = H.RUN_DIR / "outputs"

    caps = pd.read_csv(args.capitals_csv)
    capital_set = set(caps["city"])
    src_text = (str(caps["source"].iloc[0]) if "source" in caps.columns
                and len(caps) else str(args.capitals_csv.name))
    print(f"[06-h3c-i] [{args.label}] loaded {len(capital_set)} flagged capital "
          f"cities from {args.capitals_csv.name}")

    # ----- Empire frame -----
    emp_cities = pd.read_parquet(H.PRIMARY_PARQUET)
    emp_caps_in_frame = capital_set & set(emp_cities["city"])
    missing_sentinels = SENTINEL_CAPITALS_EMPIRE - emp_caps_in_frame
    if missing_sentinels:
        print("[06-h3c-i] HARD-STOP: major capitals missing from empire frame "
              f"flag set: {sorted(missing_sentinels)}")
        return 1
    idata_emp = az.from_netcdf(str(out_dir / "idata-primary.nc"))
    emp = capital_contrast(idata_emp, emp_cities, capital_set, "empire")
    emp["status"] = "PRELIMINARY --- pending Shawn's sign-off"

    # ----- Latin frame -----
    lat_cities = pd.read_parquet(H.LATIN_PARQUET)
    idata_lat = az.from_netcdf(str(out_dir / "idata-latin.nc"))
    lat = capital_contrast(idata_lat, lat_cities, capital_set, "latin")
    lat["status"] = ("PRELIMINARY --- pending Shawn's sign-off AND pending OSF "
                     "Amendment 02 (Decision 36 amendment-gate)")

    result = {
        "test": "H3c(i) --- provincial-capital residual contrast "
                "(answers SR2(i): capital over-production)",
        "indicator_label": args.label,
        "capitals_csv": str(args.capitals_csv.name),
        "source_of_capital_indicator": src_text,
        "residual_definition": "Pearson, r_c,s = (y_c - mu_c,s) / "
                               "sqrt(mu_c,s + mu_c,s^2/phi_s) --- identical to "
                               "H3c(ii) (04-h3c.py / 05-h3c-sr1-latin.py)",
        "status": "PRELIMINARY --- pending sign-off; Latin frame pending OSF "
                  "Amendment 02 (Decision 36 amendment-gate)",
        "empire": emp,
        "latin": lat,
    }

    out_path = out_dir / f"h3c-i-results-{args.label}.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"[06-h3c-i]   -> {out_path}")
    print(f"[06-h3c-i] EMPIRE verdict: {emp['verdict']} "
          f"(P={emp['p_contrast_above_0']:.4f}, n_cap={emp['n_capitals']})")
    print(f"[06-h3c-i] LATIN  verdict: {lat['verdict']} "
          f"(P={lat['p_contrast_above_0']:.4f}, n_cap={lat['n_capitals']})")
    print("[06-h3c-i] DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
