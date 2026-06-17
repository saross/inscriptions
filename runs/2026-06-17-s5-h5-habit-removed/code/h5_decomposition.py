#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h5_decomposition.py — §5 H5 companion: magnitude decomposition of the §5
Layer-A hierarchical fit, and the Latin-minus-Roma (diagnostic-unit) restriction.
========================================================================

Quantifies "how big" each component of the per-city log-rate is, in comparable
log-rate SD units, from the existing §5 Layer-A posterior (no new sampling):

    log λ[c,t] = α_g + g_shape[t] (empire-wide COMMON TEMPORAL component)
               + u_shape[p(c),t]  (province temporal)
               + v_shape[c,t]     (city-specific temporal)
               + (b_u[p] + b_v[c]) (between-city LEVEL = cross-sectional axis)

Reports, as posterior-median log-rate SDs: the common temporal swing (g), the
province (u) and city (v) temporal deviations, and the between-city level spread
(the cross-sectional / population axis), plus the common component's approximate
share of a typical city's temporal variance. Repeats the decomposition for the
Latin-speaking-minus-Roma diagnostic unit (provinces in the Latin language map)
vs the all-provinces baseline, and reports the (small) non-Latin Greek-East set
separately.

These numbers anchor Obs 97/98 and the paper's empirical decomposition; they were
previously computed inline only — this script makes them reproducible.

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-17-s5-h5-habit-removed/code/h5_decomposition.py

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
import arviz as az

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parents[1]
REPO = THIS.parents[3]
LAYER_A_CODE = REPO / "runs/2026-05-30-s5-small-n-trajectories/code"
PRIMARY_NC = LAYER_A_CODE / "production/monolithic-inscription-25y.nc"
CITY_INDEX = LAYER_A_CODE / "prepared/city-index.parquet"
LANG_CSV = REPO / "runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv"
OUT = RUN_DIR / "outputs" / "h5-decomposition.json"

sys.path.insert(0, str(LAYER_A_CODE))
import dataprep as dp  # noqa: E402
sys.path.insert(0, str(THIS.parent))
import h5_habit_removed as H5  # noqa: E402  (reuse city_u_rows + BIN_CENTRES)

BIN = dp.BIN_EDGES
BIN_CENTRES = (BIN[:-1] + BIN[1:]) / 2.0


def _stack(da):
    o = [x for x in da.dims if x not in ("chain", "draw")]
    return da.stack(sample=("chain", "draw")).transpose("sample", *o).values.astype(float)


def main() -> None:
    post = az.from_netcdf(str(PRIMARY_NC)).posterior
    alpha = _stack(post["alpha_g"]); g = _stack(post["g_shape"])
    u = _stack(post["u_shape"]); v = _stack(post["v_shape"])
    bu = _stack(post["b_u"]); bv = _stack(post["b_v"])
    cities = [str(c) for c in post["v_shape"].coords["city"].values]
    provs = [str(p) for p in post["u_shape"].coords["prov"].values]
    urows = H5.city_u_rows(cities, provs)
    S, T = g.shape

    bu_pad = np.concatenate([bu, np.zeros((S, 1))], axis=1)
    u_full = np.concatenate([u, np.zeros((S, 1, T))], axis=1)[:, urows, :]   # (S,C,T)
    level = alpha[:, None] + bu_pad[:, urows] + bv                            # (S,C)

    lang = pd.read_csv(LANG_CSV, comment="#")
    latin_prov = set(lang.loc[lang["language"] == "Latin", "lire_province"])
    idx = pd.read_parquet(CITY_INDEX).set_index("city")
    is_latin = np.array([idx.loc[c, "province"] in latin_prov for c in cities])

    med = lambda x: float(np.median(x))

    def decomp(sel: np.ndarray) -> dict:
        sd_level = level[:, sel].std(axis=1)
        sd_v = v[:, sel, :].std(axis=2).mean(axis=1)
        agg = (g[:, None, :] + u_full + v)[:, sel, :].mean(axis=1)            # (S,T)
        peak_bin = int(np.bincount(np.argmax(agg, axis=1), minlength=T).argmax())
        # approximate common-component share of per-city temporal variance
        var_tot = (g[:, None, :] + u_full + v)[:, sel, :].var(axis=2)         # (S,n)
        frac_g = (g.var(axis=1)[:, None] / var_tot)
        return {
            "n_cities": int(sel.sum()),
            "aggregate_common_peak_bin": peak_bin,
            "aggregate_common_peak_year": float(BIN_CENTRES[peak_bin]),
            "sd_level_lograte": med(sd_level),
            "sd_city_temporal_v": med(sd_v),
            "median_common_share_of_temporal_var": med(np.median(frac_g, axis=1)),
        }

    out = {
        "units": "log-rate standard deviation (posterior median); comparable across rows",
        "shared_empire_common": {
            "g_peak_bin": int(np.bincount(np.argmax(g, axis=1), minlength=T).argmax()),
            "g_peak_year": float(BIN_CENTRES[int(np.bincount(np.argmax(g, axis=1),
                                                             minlength=T).argmax())]),
            "sd_common_temporal_g": med(g.std(axis=1)),
            "sd_province_temporal_u": med(u.std(axis=2).mean(axis=1)),
        },
        "all_provinces": decomp(np.ones(len(cities), bool)),
        "latin_minus_roma": decomp(is_latin),
        "non_latin_greek_east": decomp(~is_latin),
        "provenance": {"primary_nc": str(PRIMARY_NC),
                       "lang_map": str(LANG_CSV),
                       "note": "Rome already excluded in the §5 set; latin_minus_roma = Latin-language provinces."},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
