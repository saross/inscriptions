#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
province_size_regression.py — §5 probe: is the size–buffering gradient PROVINCE-mediated?
=========================================================================================

The **direct** test of the province-mediation *inference* in Obs 104. The
city-level size-vs-dynamics probe
(``runs/2026-06-18-s5-size-vs-dynamics/code/size_vs_dynamics.py``, Obs 104) found
the "bigger cities are more buffered" gradient is much stronger on ``q_uv``
(city-from-empire) than on ``q_v`` (city-from-province), and — because
``q_uv = q_u · q_v`` — *inferred* that it operates mainly at the **province**
tier. That was an inference (Obs 104 caveat). This script regresses the
**province-from-empire** trajectory features (``q_u``) directly on **province
size**, which CONFIRMS province-mediation directly, or fails to.

**Unit = PROVINCE.** ``q_u[p,t] = exp((1/β)·u_shape[p,t])`` — one geom-mean-1
series per non-singleton province (computed directly from ``u_shape`` (S, P, T),
NOT the per-city broadcast — that just duplicates within province). Province
size = ``pop_est`` aggregated over ALL member cities in the FULL 1,012-city index
(sum primary; mean / max sensitivities), log10.

Features (mid-bins only; envelope edges excluded; "more buffered" = F1↑ F2↓ F3↑):
  F1 late-level  = q_u[AD 262]          (sits higher relative to empire late?)
  F2 volatility  = SD_t(log q_u), bins 2-13
  F3 tilt        = log q_u[AD262] - log q_u[AD112]

Statistic: Spearman ρ (rank-based ⇒ robust to log-space leverage, Obs 94),
reported with BOTH a province-bootstrap CI (sampling uncertainty — binding at
n≈35) and a draw-wise ρ posterior (trajectory uncertainty); plus OLS + Theil-Sen
slopes. ρ is exactly β-frame-invariant per draw (the 1/β inversion is a monotone,
province-constant rescale); computed with empire β; slope magnitudes in empire-β
units. Non-circular: §5 Layer A has no population covariate (Obs 98); ``u_shape``
(hence ``q_u``) is Hanson-free.

Province set: all 35 non-singleton provinces (primary); the 20 containing ≥1
reliable (N≥300) city (sensitivity, flagged — province-tier reliability NOT
separately calibrated; N*=300 is a per-city floor, Obs 100).

Exploratory; no thresholds (Decision 13). n≈35 (≈20 reliable) ⇒ VERY low power
(|ρ| ≳ 0.33 at n=35 to clear a 95 % bound); a null is expected and informative.
See ``../spec.md``.

Reuses the audited parent-probe machinery verbatim (``drawwise_rho``,
``bootstrap_rho_slopes``, ``analyse``) and the residual-Layer-B loaders
(``h5.load_posterior``, ``lb.load_beta_draws``, ``lbr.invert_residual``).

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-18-province-size-regression/code/province_size_regression.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-18, on Shawn's brief.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parents[1]
REPO = THIS.parents[3]
SVD_CODE = REPO / "runs/2026-06-18-s5-size-vs-dynamics/code"          # parent probe
LBR_CODE = REPO / "runs/2026-06-17-s5-layer-b-residual/code"          # residual Layer B
OUT_DIR = RUN_DIR / "outputs"
RESIDUAL_NC = REPO / ("runs/2026-06-17-s5-layer-b-residual/outputs/"
                      "layerb-residual-trajectories-empire.nc")       # self-check anchor

# Reuse the audited machinery. Importing runs no analysis (both guard __main__).
sys.path.insert(0, str(SVD_CODE))
sys.path.insert(0, str(LBR_CODE))
import size_vs_dynamics as svd        # noqa: E402  drawwise_rho / bootstrap_rho_slopes / analyse
import layerb_residual_invert as lbr  # noqa: E402  invert_residual + h5 / lb handles

h5 = lbr.h5
lb = lbr.lb
BIN_CENTRES = lbr.BIN_CENTRES
N_STAR = lbr.N_STAR                   # 300 (per-CITY reliability floor; see caveat)
SEED = lbr.SEED                       # 20260616 — same β resample as residual B
BOOT_SEED = svd.BOOT_SEED             # 20260618
N_BOOT = svd.N_BOOT                   # 2000
B_AD112, B_AD262 = svd.B_AD112, svd.B_AD262   # bin indices 6, 12
MID = svd.MID                         # slice(2, 14) — mid bins for volatility

# Reuse the parent probe's three estimators directly (signatures match).
drawwise_rho = svd.drawwise_rho
bootstrap_rho_slopes = svd.bootstrap_rho_slopes
analyse = svd.analyse


def _sha256(path: Path) -> str:
    """Hex SHA-256 of a file (streamed; provenance record)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def features_prov(q_u):
    """Per-draw, per-PROVINCE trajectory features from q_u (S, P, T).

    Mirrors ``size_vs_dynamics.features`` but drops F4 peak-bin (not in this
    spec). Returns a dict of (S, P) arrays. "More buffered" = F1 high, F2 low,
    F3 high (province sits higher relative to empire late / smoother / shallower
    decline).

    Args:
        q_u: ``(S, P, T)`` province-from-empire relative-to-empire trajectories.

    Returns:
        dict of ``(S, P)`` feature arrays (F1_late_level, F2_volatility, F3_tilt).
    """
    logq = np.log(q_u)
    return {
        "F1_late_level": q_u[:, :, B_AD262],                      # (S, P)
        "F2_volatility": np.std(logq[:, :, MID], axis=2),         # (S, P)
        "F3_tilt": logq[:, :, B_AD262] - logq[:, :, B_AD112],     # (S, P)
    }


def province_size(provs, idx, agg):
    """Aggregate ``pop_est`` over all member cities of each province (FULL index).

    Args:
        provs: ordered list of the P non-singleton province names (u_shape coord).
        idx: the full 1,012-city ``city-index.parquet`` DataFrame.
        agg: one of ``{"sum", "mean", "max"}`` — the aggregation over member cities.

    Returns:
        ``(size, n_cities)`` — each ``(P,)``; ``size`` is the aggregated pop_est in
        the province order of ``provs``; ``n_cities`` the member-city count. Raises
        if any province is missing from the index (the join is verified upstream).
    """
    grouped = idx.groupby("province")["pop_est"]
    aggregated = getattr(grouped, agg)()
    counts = grouped.count()
    missing = [p for p in provs if p not in aggregated.index]
    if missing:                                                  # join guard
        raise KeyError(f"provinces absent from city-index: {missing}")
    size = np.array([float(aggregated.loc[p]) for p in provs])
    n_cities = np.array([int(counts.loc[p]) for p in provs])
    return size, n_cities


def self_check(u, provs, beta, urows, cities):
    """Two guards (spec §6) before trusting any output.

    1. ``q_u`` constant within province: broadcast the direct province inversion
       to cities and assert per-city values within a province are identical.
    2. Direct ``u_shape`` inversion reproduces the residual Layer B ``q_u_med``:
       compute ``q_u`` from ``u_shape`` (S, P, T) at empire β + SEED, broadcast to
       a spot province's cities, take the per-draw median, and compare to the
       persisted residual nc ``q_u_med`` for those cities — must match to ~1e-12
       (the residual nc inverted the per-city broadcast ``r_u`` with the same
       seed; ``exp((1/β)·r)`` is elementwise per draw, so broadcasting before vs
       after inversion is identical for matched draws).

    Args:
        u: ``(S, P, T)`` province shape deviations.
        provs: P province names.
        beta: empire β draws pool.
        urows: ``(C,)`` province row per city (or -1 singleton).
        cities: C city names.

    Returns:
        dict summarising both guards (passed flags + the max abs diff).
    """
    import arviz as az

    # Direct province inversion at empire β + SEED (same recipe as invert_residual).
    S = u.shape[0]
    rng = np.random.default_rng(SEED)
    beta_draws = rng.choice(beta, size=S, replace=True)           # (S,)
    inv_beta = (1.0 / beta_draws)[:, None, None]                  # (S, 1, 1)
    q_u_prov = np.exp(inv_beta * u)                               # (S, P, T)
    q_u_prov_med = np.median(q_u_prov, axis=0)                    # (P, T)

    # ---- Guard 1: q_u constant within province (broadcast to cities) ---------
    P, T = q_u_prov_med.shape
    pad = np.concatenate([q_u_prov_med, np.ones((1, T))], axis=0)  # row -1 -> 1
    q_u_city_med = pad[urows, :]                                  # (C, T)
    const_ok = True
    for p in range(P):
        members = [c for c in range(len(cities)) if urows[c] == p]
        if len(members) < 2:
            continue
        block = q_u_city_med[members]                            # (m, T)
        if not np.allclose(block, block[0], rtol=0, atol=0):     # exact: same row
            const_ok = False
            break

    # ---- Guard 2: reproduce residual Layer B q_u_med for a spot province -----
    res = az.from_netcdf(str(RESIDUAL_NC))
    res_cities = [str(c) for c in res["city"].values]
    res_qu = res["q_u_med"].values                               # (C_res, T) per-city broadcast

    # spot = the first non-singleton province with ≥1 city present in the residual nc
    spot_p, spot_members = None, []
    for p in range(P):
        members = [c for c in range(len(cities))
                   if urows[c] == p and cities[c] in res_cities]
        if members:
            spot_p, spot_members = p, members
            break
    if spot_p is None:
        raise RuntimeError("self-check: no province-tier city found in residual nc")

    diffs = []
    for c in spot_members:
        rj = res_cities.index(cities[c])
        diffs.append(np.max(np.abs(q_u_city_med[c] - res_qu[rj])))
    max_abs = float(max(diffs))
    repro_ok = max_abs < 1e-9                                     # float64 median agreement

    print(f"  self-check guard 1 (q_u constant within province): "
          f"{'PASS' if const_ok else 'FAIL'}")
    print(f"  self-check guard 2 (direct u_shape inversion reproduces residual "
          f"q_u_med, province '{provs[spot_p]}', {len(spot_members)} cities): "
          f"max abs diff {max_abs:.2e} -> {'PASS' if repro_ok else 'FAIL'}")
    if not (const_ok and repro_ok):
        raise AssertionError(
            f"self-check FAILED (const_ok={const_ok}, repro_ok={repro_ok}, "
            f"max_abs={max_abs:.2e}); do not trust outputs.")
    return {"q_u_constant_within_province": const_ok,
            "reproduces_residual_q_u_med": repro_ok,
            "spot_province": provs[spot_p],
            "spot_n_cities": len(spot_members),
            "max_abs_diff_vs_residual_nc": max_abs,
            "q_u_prov": q_u_prov}                                 # reuse the draws downstream


def plots(feat_med_by_name, draws_by_name, log_size, mask, label):
    """Scatter of each feature vs log10 province-size + draw-wise ρ panel."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.stats import theilslopes, spearmanr

    names = ["F1_late_level", "F2_volatility", "F3_tilt"]
    x = log_size[mask]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, name in zip(axes, names):
        y = feat_med_by_name[name][mask]
        ax.scatter(x, y, s=28, color="C0")
        sl, ic, *_ = theilslopes(y, x)
        xs = np.array([x.min(), x.max()])
        ax.plot(xs, ic + sl * xs, color="C3", lw=1.6, label="Theil-Sen")
        rho = spearmanr(x, y)[0]
        ax.set_title(f"{name}\nρ={rho:.2f} (q_u, {label} n={x.size})")
        ax.set_xlabel("log10 province size (sum pop_est)")
        ax.set_ylabel(name)
        ax.legend(fontsize=8)
    fig.suptitle(f"Province size vs province-from-empire dynamics (q_u, {label})")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "province-size-regression-scatter.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    for name in names:
        rd = draws_by_name[name]
        rd = rd[np.isfinite(rd)]
        ax.hist(rd, bins=40, alpha=0.5, label=f"{name} (med {np.median(rd):.2f})")
    ax.axvline(0, color="k", lw=1)
    ax.set_title(f"Draw-wise Spearman ρ posterior (q_u, {label})")
    ax.set_xlabel("ρ"); ax.set_ylabel("draws"); ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "province-size-regression-rho-posterior.png", dpi=130)
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    import pandas as pd

    print(f"§5 province-size regression — seed={SEED} boot_seed={BOOT_SEED}")
    g, u, v, lam, cities, provs = h5.load_posterior()
    del g, v, lam
    S, P, T = u.shape
    urows = h5.city_u_rows(cities, provs)
    beta = lb.load_beta_draws("empire")
    print(f"  loaded: S={S} draws, P={P} non-singleton provinces, T={T} bins; "
          f"β median {float(np.median(beta)):.3f}")

    # Province join (re-verified here against the FULL index).
    idx_full = pd.read_parquet(h5.CITY_INDEX)
    idx_provs = set(idx_full["province"].dropna().astype(str).unique())
    matched = [p for p in provs if p in idx_provs]
    unmatched = [p for p in provs if p not in idx_provs]
    print(f"  province join: {len(matched)}/{P} u_shape provs matched in full "
          f"city-index ({len(idx_full)} cities); unmatched={unmatched}")
    if unmatched:
        raise KeyError(f"province join incomplete: {unmatched}")

    # Self-check (spec §6) — must pass before any deliverable. Reuses q_u draws.
    sc = self_check(u, provs, beta, urows, cities)
    q_u = sc.pop("q_u_prov")                         # (S, P, T) empire-β, SEED
    feats = features_prov(q_u)                       # F1/F2/F3 over provinces

    # Province-size predictors (FULL index): sum primary; mean / max sensitivities.
    size_aggs = {}
    for agg in ("sum", "mean", "max"):
        size, n_cities = province_size(provs, idx_full, agg)
        size_aggs[agg] = {"size": size, "log_size": np.log10(size),
                          "n_cities": n_cities}
    n_cities = size_aggs["sum"]["n_cities"]          # same for all aggs

    # Province samples: all non-singleton (primary) + ≥1 reliable-city subset.
    reliable_full = idx_full[idx_full["N"] >= N_STAR]
    provs_with_reliable = set(reliable_full["province"].dropna().astype(str).unique())
    has_reliable = np.array([p in provs_with_reliable for p in provs])
    allmask = np.ones(P, dtype=bool)
    samples = {"all_provinces": allmask, "reliable_subset": has_reliable}
    print(f"  samples: all={int(allmask.sum())} provinces; "
          f"reliable-subset={int(has_reliable.sum())} (contain ≥1 N≥300 city)")
    print(f"  province size (sum pop_est): "
          f"[{size_aggs['sum']['size'].min():.0f}, {size_aggs['sum']['size'].max():.0f}], "
          f"{size_aggs['sum']['log_size'].max() - size_aggs['sum']['log_size'].min():.2f} decades; "
          f"member cities {int(n_cities.min())}/{int(np.median(n_cities))}/{int(n_cities.max())}")

    # ---- Analyse every feature × size-aggregate × sample ---------------------
    results = {}
    draws_primary = {}                               # sum × all_provinces, for the figure
    for agg in ("sum", "mean", "max"):
        log_size = size_aggs[agg]["log_size"]
        results[agg] = {}
        for fname, fSP in feats.items():
            results[agg][fname] = {}
            for sname, mask in samples.items():
                results[agg][fname][sname] = analyse(fSP, log_size, mask, BOOT_SEED)
            if agg == "sum":
                draws_primary[fname] = drawwise_rho(fSP, log_size, allmask)

    # Headline print (sum size, all provinces).
    print("  q_u (sum size, all provinces) — Spearman ρ; bootstrap CI | P-sign | drawwise ρ:")
    for fname in ("F1_late_level", "F2_volatility", "F3_tilt"):
        r = results["sum"][fname]["all_provinces"]
        sr, dw = r["spearman_rho"], r["drawwise_rho"]
        print(f"    {fname}: ρ {sr['point']:+.2f} "
              f"CI [{sr['ci95'][0]:+.2f}, {sr['ci95'][1]:+.2f}] "
              f"P(>0)={sr['p_gt0']:.2f} P(<0)={sr['p_lt0']:.2f} | "
              f"drawwise {dw['median']:+.2f} [{dw['ci95'][0]:+.2f}, {dw['ci95'][1]:+.2f}]")

    feat_med = {k: np.median(vv, axis=0) for k, vv in feats.items()}   # (P,)
    plots(feat_med, draws_primary, size_aggs["sum"]["log_size"], allmask,
          "all provinces")

    summary = {
        "analysis": ("§5 province-size regression — does province size predict "
                     "province-from-empire (q_u) dynamics? (direct test of the "
                     "Obs 104 province-mediation inference)"),
        "type": ("exploratory; no thresholds (Decision 13); n≈35 provinces (≈20 "
                 "reliable subset) VERY low power, a null is informative"),
        "question": ("cross-province: does province size (sum/mean/max pop_est "
                     "over ALL member cities in the full index) predict features "
                     "of q_u = exp((1/β)·u_shape) — F1 late-level, F2 volatility, "
                     "F3 tilt? 'more buffered' = F1↑ F2↓ F3↑."),
        "verdict_logic": (
            "F1+,F2-,F3+ clearing the binding bootstrap bound on ≥1 feature ⇒ "
            "CONFIRMS province-mediation directly; coherent direction with CIs "
            "incl. 0 ⇒ directionally corroborates (underpowered); null / "
            "sign-incoherent ⇒ Obs 104 q_uv≫q_v inference NOT directly "
            "corroborated at province level (could be a city-membership channel)."),
        "non_circular": ("§5 Layer A has no population covariate (Obs 98); "
                         "u_shape (hence q_u) Hanson-free; β cosmetic for ranks"),
        "province_join": {
            "u_shape_provs": P, "matched_in_full_index": len(matched),
            "unmatched": unmatched, "full_index_n_cities": int(len(idx_full)),
            "full_index_distinct_provinces": int(idx_full["province"].nunique()),
        },
        "self_check": sc,
        "predictor": {
            "name": "province pop_est aggregated over ALL member cities (FULL 1012-city index)",
            "transform": "log10", "primary_aggregate": "sum",
            "sensitivity_aggregates": ["mean", "max"],
            "sum_range": [float(size_aggs["sum"]["size"].min()),
                          float(size_aggs["sum"]["size"].max())],
            "sum_log10_decades": float(size_aggs["sum"]["log_size"].max()
                                       - size_aggs["sum"]["log_size"].min()),
            "member_cities_min_median_max": [int(n_cities.min()),
                                             int(np.median(n_cities)),
                                             int(n_cities.max())],
        },
        "samples": {
            "all_provinces": int(allmask.sum()),
            "reliable_subset": int(has_reliable.sum()),
            "reliable_subset_definition": (
                "non-singleton provinces containing ≥1 reliable (N≥300) city. "
                "FLAG: province-tier reliability was NOT separately calibrated — "
                "N*=300 is a per-CITY floor (Obs 100); this is a coarse proxy."),
        },
        "features": {
            "F1_late_level": "q_u[AD262] (bin 12); higher = more buffered",
            "F2_volatility": "SD_t(log q_u) over mid bins 2-13; lower = more buffered",
            "F3_tilt": "log q_u[AD262]-log q_u[AD112] (bin 12 - bin 6); higher = more buffered",
        },
        "beta_frame_invariance": (
            "draw-wise ρ exactly β-frame-invariant (per-draw monotone "
            "province-constant rescale preserves across-province ranks); bootstrap "
            "ρ uses empire-β median features; slopes in empire-β units (β median "
            "%.3f)" % float(np.median(beta))),
        "seeds": {"beta_resample": SEED, "bootstrap": BOOT_SEED, "n_boot": N_BOOT},
        "results": results,
        "provenance": {
            "primary_nc": str(h5.PRIMARY_NC),
            "primary_nc_sha256": _sha256(h5.PRIMARY_NC),
            "h3a_empire_nc": str(lb.H3A_NC["empire"]),
            "city_index": str(h5.CITY_INDEX),
            "city_index_sha256": _sha256(h5.CITY_INDEX),
            "residual_nc_selfcheck": str(RESIDUAL_NC),
            "reused_code": [str(SVD_CODE / "size_vs_dynamics.py"),
                            str(LBR_CODE / "layerb_residual_invert.py")],
        },
        "caveats": [
            "n≈35 provinces (≈20 reliable) VERY low power (|ρ|≳0.33 at n=35 / ≳0.44 at n=20)",
            "province-tier reliability NOT calibrated; N*=300 is a per-CITY floor (Obs 100)",
            "not pure demography (Obs 98) — u_shape carries provincial taphonomy/economy/habit",
            "range restriction 1.77 log10 decades (province size)",
            "multiple features×aggregates×samples — no cherry-pick, no threshold (Decision 13)",
            "inversion cosmetic for rank stats; edge bins excluded (GRW endpoint variance)",
        ],
    }
    with open(OUT_DIR / "province-size-regression-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=h5._json_default)
    print("  done. outputs in", OUT_DIR)


if __name__ == "__main__":
    main()
