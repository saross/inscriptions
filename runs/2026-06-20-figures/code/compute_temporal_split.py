#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_temporal_split.py — exact per-city three-way temporal variance split.
=============================================================================

Firms up the summary's INDICATIVE ≈54/24/22 (common / province / city) split into
exact numbers, recomputed from the §5 monolithic Layer-A posterior (the regen the
figures build needed). Reuses the H5 decomposition method verbatim
(``h5_decomposition.py``): for each city c and posterior draw s, the per-city
temporal signal is g + u + v over the 16 bins, and each tier's share of a city's
TOTAL temporal variance is::

    frac_g[s,c] = Var_t(g[s])        / Var_t(g[s] + u[s,c] + v[s,c])
    frac_u[s,c] = Var_t(u[s,c])      / Var_t(g[s] + u[s,c] + v[s,c])
    frac_v[s,c] = Var_t(v[s,c])      / Var_t(g[s] + u[s,c] + v[s,c])

aggregated as median over cities then median over draws (matching the published
``median_common_share_of_temporal_var`` aggregation). The three shares do NOT sum
to exactly 1 — the remainder is the cross-tier covariance (g, u, v are
independently-fit zero-sum RW shapes, not orthogonal by construction); we report
that remainder explicitly rather than forcing a normalisation.

The ``frac_g`` value must reproduce the published common share (0.5397
all-provinces / 0.5403 Latin-minus-Roma) as a regression guard.

Writes ``outputs/temporal-three-way-split.json``; F9 reads it.

Author: Claude Code (Opus 4.8) on Shawn Ross's brief, 2026-06-20. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import arviz as az

REPO = Path("/home/shawn/Code/inscriptions")
LAYER_A_CODE = REPO / "runs/2026-05-30-s5-small-n-trajectories/code"
PRIMARY_NC = LAYER_A_CODE / "production/monolithic-inscription-25y.nc"
CITY_INDEX = LAYER_A_CODE / "prepared/city-index.parquet"
LANG_CSV = REPO / "runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv"
H5_CODE = REPO / "runs/2026-06-17-s5-h5-habit-removed/code"
OUT = REPO / "runs/2026-06-20-figures/outputs/temporal-three-way-split.json"

sys.path.insert(0, str(LAYER_A_CODE))
sys.path.insert(0, str(H5_CODE))
import h5_habit_removed as H5  # noqa: E402  (city_u_rows)

# Published common-share guard (h5-decomposition.json).
PUBLISHED_COMMON = {"all_provinces": 0.539742595738415,
                    "latin_minus_roma": 0.5402948621421158}


def _stack(da):
    """Posterior array as (sample, *other_dims), float."""
    o = [x for x in da.dims if x not in ("chain", "draw")]
    return da.stack(sample=("chain", "draw")).transpose("sample", *o).values.astype(float)


def main() -> None:
    post = az.from_netcdf(str(PRIMARY_NC)).posterior
    g = _stack(post["g_shape"])          # (S, T)
    u = _stack(post["u_shape"])          # (S, P, T)
    v = _stack(post["v_shape"])          # (S, C, T)
    cities = [str(c) for c in post["v_shape"].coords["city"].values]
    provs = [str(p) for p in post["u_shape"].coords["prov"].values]
    urows = H5.city_u_rows(cities, provs)
    S, T = g.shape

    # Pad a zero u-row for singleton-province cities, then gather per city.
    u_full = np.concatenate([u, np.zeros((S, 1, T))], axis=1)[:, urows, :]  # (S, C, T)

    lang = pd.read_csv(LANG_CSV, comment="#")
    latin_prov = set(lang.loc[lang["language"] == "Latin", "lire_province"])
    idx = pd.read_parquet(CITY_INDEX).set_index("city")
    is_latin = np.array([idx.loc[c, "province"] in latin_prov for c in cities])

    # median over cities, then over draws (the published aggregation).
    agg = lambda fr: float(np.median(np.median(fr, axis=1)))

    def split(sel: np.ndarray) -> dict:
        gg = g[:, None, :]                                   # (S,1,T)
        gs = np.broadcast_to(gg, v.shape)[:, sel, :]         # (S,n,T) common, per city
        us = u_full[:, sel, :]
        vs = v[:, sel, :]
        tot = gs + us + vs                                   # (S, n, T)
        var_tot = tot.var(axis=2)                            # (S, n)

        # --- method (a): marginal shares Var_t(tier)/Var_t(total) -------------
        # Each tier's own share of a city's total temporal variance; these do
        # NOT sum to 1 because the tiers covary (the remainder is reported).
        ma_g = agg(gs.var(axis=2) / var_tot)
        ma_u = agg(us.var(axis=2) / var_tot)
        ma_v = agg(vs.var(axis=2) / var_tot)

        # --- method (c): covariance-attributed shares Cov_t(tier,total)/Var ---
        # The principled ANOVA-style partition: each tier is credited its
        # variance plus its covariances with the others; sums to EXACTLY 1.
        cov = lambda a: ((a - a.mean(axis=2, keepdims=True))
                         * (tot - tot.mean(axis=2, keepdims=True))).mean(axis=2)
        mc_g = agg(cov(gs) / var_tot)
        mc_u = agg(cov(us) / var_tot)
        mc_v = agg(cov(vs) / var_tot)

        # --- method (b): common, then residual split proportional to var -----
        # The summary's indicative construction (sum-to-1 by fiat).
        rem = 1.0 - ma_g
        denom = ma_u + ma_v
        mb_u = rem * ma_u / denom
        mb_v = rem * ma_v / denom

        return {
            "n_cities": int(sel.sum()),
            "method_a_marginal": {  # Var(tier)/Var(total); sums to >1
                "common_g": ma_g, "province_u": ma_u, "city_v": ma_v,
                "sum": ma_g + ma_u + ma_v,
                "covariance_remainder": 1.0 - (ma_g + ma_u + ma_v)},
            "method_c_cov_attributed": {  # Cov(tier,total)/Var(total); sums to 1
                "common_g": mc_g, "province_u": mc_u, "city_v": mc_v,
                "sum": mc_g + mc_u + mc_v},
            "method_b_proportional_remainder": {  # summary's indicative
                "common_g": ma_g, "province_u": mb_u, "city_v": mb_v,
                "sum": ma_g + mb_u + mb_v},
        }

    res = {"all_provinces": split(np.ones(len(cities), bool)),
           "latin_minus_roma": split(is_latin)}

    # Regression guard: marginal frac_g must reproduce the published common share.
    for k, pub in PUBLISHED_COMMON.items():
        got = res[k]["method_a_marginal"]["common_g"]
        assert abs(got - pub) < 1e-6, f"{k}: common share {got} != published {pub}"
    res["_guard"] = "common_share_g reproduces h5-decomposition.json to <1e-6"
    res["_provenance"] = {"primary_nc": str(PRIMARY_NC),
                          "method": "Var_t(tier)/Var_t(g+u+v) per city/draw, "
                                    "median over cities then draws"}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
