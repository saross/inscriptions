#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
size_vs_dynamics.py — §5 probe: does city size predict city-specific dynamics?
==============================================================================

The well-posed reframe (user-obs 43) of "can we compare the isolated city-level
effect to Hanson?". A direct ``q_v``-vs-Hanson overlay is a category mismatch
(``q_v`` is a level-free temporal *shape*; Hanson ``pop_est`` is a static
*level*). The well-posed cross-city question is whether a city's **size**
predicts **features of its city-specific temporal trajectory**.

Primary tier ``q_v`` (city-from-province; province AND empire removed); secondary
``q_uv`` (city-from-empire). Features (mid-bins only; envelope edges excluded):
  F1 late-level  = q[AD 262]            (sustained relative to province late?)
  F2 volatility  = SD_t(log q), bins 2-13
  F3 tilt        = log q[AD262] - log q[AD112]   (secondary)
  F4 peak-bin    = argmax_t q           (secondary; edge-contaminated, flagged)

Predictor: log10 ``pop_est`` (city-index.parquet). Statistic: Spearman ρ (rank-
based ⇒ robust to single-city log-space leverage, the Obs 94 lesson), reported
with BOTH a city-bootstrap CI (sampling uncertainty — binding at n=34) and a
draw-wise ρ posterior (trajectory uncertainty); plus OLS + Theil-Sen slopes.

**β-frame invariance.** For a fixed draw, ``q = exp((1/β)·r)`` is a monotone,
city-constant rescaling of ``r``, so every feature's across-city RANK — hence the
per-draw Spearman ρ — is *exactly* identical under the empire or Latin β. We
compute with empire β; the draw-wise ρ carries over to Latin unchanged (the
bootstrap uses empire-β median features and is near-invariant since the β
posterior is tight). Only the slope *magnitudes* are in empire-β units.

**Non-circular.** §5 Layer A has no population covariate (Obs 98), so ``v_shape``
(hence ``q_v``) is Hanson-free; Hanson enters only as the predictor.

Exploratory; no thresholds (Decision 13). n=34 ⇒ low power; a null is informative
(Obs 100). The residual is not pure demography (Obs 98). See ``../spec.md``.

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-18-s5-size-vs-dynamics/code/size_vs_dynamics.py

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
LBR_CODE = REPO / "runs/2026-06-17-s5-layer-b-residual/code"
OUT_DIR = RUN_DIR / "outputs"

# Reuse the audited residual-Layer-B machinery (which itself reuses H5 + raw B).
sys.path.insert(0, str(LBR_CODE))
import layerb_residual_invert as lbr   # noqa: E402

h5 = lbr.h5
lb = lbr.lb
BIN_CENTRES = lbr.BIN_CENTRES
N_STAR = lbr.N_STAR
SEED = lbr.SEED                          # 20260616 — same β resample as residual B
BOOT_SEED = 20260618
N_BOOT = 2000
B_AD112, B_AD188, B_AD262 = 6, 9, 12     # bin indices (centres AD 112/188/262)
MID = slice(2, 14)                       # mid bins for volatility (exclude edges)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def features(q):
    """Per-draw, per-city trajectory features from q (S, C, T).

    Returns a dict of (S, C) arrays. F1/F2 headline; F3/F4 secondary.
    """
    logq = np.log(q)
    return {
        "F1_late_level": q[:, :, B_AD262],                       # (S, C)
        "F2_volatility": np.std(logq[:, :, MID], axis=2),        # (S, C)
        "F3_tilt": logq[:, :, B_AD262] - logq[:, :, B_AD112],    # (S, C)
        "F4_peak_bin": np.argmax(q, axis=2).astype(np.float64),  # (S, C)
    }


def _ordinal_ranks(a, axis):
    """0-based ordinal ranks along ``axis`` (continuous data: ties negligible)."""
    return a.argsort(axis=axis).argsort(axis=axis)


def drawwise_rho(feat_SC, log_pop, mask):
    """Draw-wise Spearman ρ posterior between a feature and log-pop.

    feat_SC: (S, C). For each draw, rank the feature across the masked cities and
    correlate (Pearson of ranks) with the (tie-aware) pop ranks. Returns the (S,)
    ρ posterior. ρ is β-frame-invariant (ranks are preserved by the 1/β rescale).
    """
    from scipy.stats import rankdata

    f = feat_SC[:, mask]                                  # (S, n)
    fr = _ordinal_ranks(f, axis=1).astype(np.float64)     # continuous → ordinal ok
    pr = rankdata(log_pop[mask], method="average")        # ties at the pop floor
    fr -= fr.mean(axis=1, keepdims=True)
    pr = pr - pr.mean()
    num = fr @ pr                                         # (S,)
    den = np.sqrt((fr ** 2).sum(axis=1)) * np.sqrt((pr ** 2).sum())
    return np.where(den > 0, num / den, np.nan)


def bootstrap_rho_slopes(feat_med, log_pop, mask, seed):
    """City-bootstrap of Spearman ρ + OLS & Theil-Sen slopes on median features.

    Resamples the masked cities with replacement; returns point estimates on the
    full masked set plus bootstrap medians / 95 % CIs / P(sign).
    """
    from scipy.stats import spearmanr, theilslopes

    x = log_pop[mask]
    y = feat_med[mask]
    n = x.size
    rng = np.random.default_rng(seed)

    rho0 = float(spearmanr(x, y)[0])
    ols0 = float(np.polyfit(x, y, 1)[0])
    ts0 = float(theilslopes(y, x)[0])

    rhos, olss, tss = np.empty(N_BOOT), np.empty(N_BOOT), np.empty(N_BOOT)
    for b in range(N_BOOT):
        idx = rng.integers(0, n, n)
        xb, yb = x[idx], y[idx]
        if np.ptp(xb) == 0:                              # degenerate resample
            rhos[b] = olss[b] = tss[b] = np.nan
            continue
        rhos[b] = spearmanr(xb, yb)[0]
        olss[b] = np.polyfit(xb, yb, 1)[0]
        tss[b] = theilslopes(yb, xb)[0]

    def summ(point, arr):
        a = arr[np.isfinite(arr)]
        return {
            "point": point,
            "boot_median": float(np.median(a)),
            "ci95": [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))],
            "p_gt0": float((a > 0).mean()), "p_lt0": float((a < 0).mean()),
        }

    return {"n": int(n), "spearman_rho": summ(rho0, rhos),
            "ols_slope": summ(ols0, olss), "theilsen_slope": summ(ts0, tss)}


def analyse(feat_SC, log_pop, mask, seed):
    """Full result for one feature × tier × sample: draw-wise ρ + bootstrap."""
    rho_draws = drawwise_rho(feat_SC, log_pop, mask)
    rd = rho_draws[np.isfinite(rho_draws)]
    feat_med = np.median(feat_SC, axis=0)                 # (C,)
    out = bootstrap_rho_slopes(feat_med, log_pop, mask, seed)
    out["drawwise_rho"] = {
        "median": float(np.median(rd)),
        "ci95": [float(np.percentile(rd, 2.5)), float(np.percentile(rd, 97.5))],
        "p_gt0": float((rd > 0).mean()), "p_lt0": float((rd < 0).mean()),
    }
    return out


def plots(feat_by_name, feat_med_by_name, log_pop, reliable, draws_by_name):
    """Scatter of headline features vs log10 pop (reliable) + draw-wise ρ panel."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.stats import theilslopes, spearmanr

    x = log_pop[reliable]
    head = ["F1_late_level", "F2_volatility"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, name in zip(axes, head):
        y = feat_med_by_name[name][reliable]
        ax.scatter(x, y, s=24, color="C0")
        sl, ic, *_ = theilslopes(y, x)
        xs = np.array([x.min(), x.max()])
        ax.plot(xs, ic + sl * xs, color="C3", lw=1.6, label="Theil-Sen")
        rho = spearmanr(x, y)[0]
        ax.set_title(f"{name}\nρ={rho:.2f} (q_v, reliable n={x.size})")
        ax.set_xlabel("log10 pop_est"); ax.set_ylabel(name); ax.legend(fontsize=8)
    fig.suptitle("City size vs city-specific dynamics (q_v, 34 reliable cities)")
    fig.tight_layout(); fig.savefig(OUT_DIR / "size-vs-dynamics-scatter.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    for i, name in enumerate(head):
        rd = draws_by_name[name]
        rd = rd[np.isfinite(rd)]
        ax.hist(rd, bins=40, alpha=0.5, label=f"{name} (med {np.median(rd):.2f})")
    ax.axvline(0, color="k", lw=1)
    ax.set_title("Draw-wise Spearman ρ posterior (q_v, reliable)")
    ax.set_xlabel("ρ"); ax.set_ylabel("draws"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT_DIR / "size-vs-dynamics-rho-posterior.png", dpi=130)
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    import pandas as pd

    print(f"§5 size-vs-dynamics probe — seed={SEED} boot_seed={BOOT_SEED}")
    g, u, v, lam, cities, provs = h5.load_posterior()
    del g, lam
    urows = h5.city_u_rows(cities, provs)
    r_uv, r_v, r_u = lbr.build_residuals(u, v, urows)

    idx = pd.read_parquet(h5.CITY_INDEX).set_index("city")
    N = np.array([int(idx.loc[c, "N"]) for c in cities])
    pop = np.array([float(idx.loc[c, "pop_est"]) for c in cities])
    log_pop = np.log10(pop)
    reliable = N >= N_STAR
    allmask = np.ones(len(cities), dtype=bool)
    print(f"  {len(cities)} cities; {reliable.sum()} reliable; "
          f"pop_est [{pop.min():.0f}, {pop.max():.0f}] "
          f"({log_pop[reliable].max()-log_pop[reliable].min():.2f} decades, reliable)")

    # Invert with empire β (rank results are β-invariant; slopes in empire-β units).
    beta = lb.load_beta_draws("empire")
    q_v = lbr.invert_residual(r_v, beta, SEED)["q"]       # city-from-province
    q_uv = lbr.invert_residual(r_uv, beta, SEED)["q"]     # city-from-empire

    tiers = {"q_v_city_from_province": features(q_v),
             "q_uv_city_from_empire": features(q_uv)}
    samples = {"reliable_34": reliable, "all_268": allmask}

    results, draws_qv_reliable = {}, {}
    for tier, feats in tiers.items():
        results[tier] = {}
        for fname, fSC in feats.items():
            results[tier][fname] = {}
            for sname, mask in samples.items():
                results[tier][fname][sname] = analyse(fSC, log_pop, mask, BOOT_SEED)
            if tier == "q_v_city_from_province":
                draws_qv_reliable[fname] = drawwise_rho(fSC, log_pop, reliable)

    # Headline print (q_v, reliable).
    print("  q_v city-from-province, reliable (Spearman ρ; bootstrap CI | P-sign):")
    for fname in ("F1_late_level", "F2_volatility", "F3_tilt", "F4_peak_bin"):
        r = results["q_v_city_from_province"][fname]["reliable_34"]["spearman_rho"]
        flag = "" if fname in ("F1_late_level", "F2_volatility") else " [secondary]"
        print(f"    {fname}: ρ {r['point']:+.2f} "
              f"CI [{r['ci95'][0]:+.2f}, {r['ci95'][1]:+.2f}] "
              f"P(>0)={r['p_gt0']:.2f}{flag}")

    feat_med_qv = {k: np.median(vv, axis=0)
                   for k, vv in tiers["q_v_city_from_province"].items()}
    plots(tiers["q_v_city_from_province"], feat_med_qv, log_pop, reliable,
          draws_qv_reliable)

    summary = {
        "analysis": "§5 size-vs-dynamics probe — does pop_est predict city-specific dynamics?",
        "type": "exploratory; no thresholds (Decision 13); n=34 low power, null is informative",
        "question": ("cross-city: does Hanson pop_est predict features of q_v "
                     "(city-from-province; secondary q_uv city-from-empire)?"),
        "non_circular": "Layer A has no population covariate (Obs 98); β cosmetic for ranks",
        "predictor": {"name": "pop_est (city-index.parquet)", "transform": "log10",
                      "reliable_range": [float(pop[reliable].min()), float(pop[reliable].max())],
                      "reliable_log10_decades": float(log_pop[reliable].max()
                                                      - log_pop[reliable].min()),
                      "n_reliable": int(reliable.sum()), "n_all": int(len(cities))},
        "features": {"F1_late_level": "q[AD262] (headline)",
                     "F2_volatility": "SD_t(log q) over mid bins 2-13 (headline)",
                     "F3_tilt": "log q[AD262]-log q[AD112] (secondary)",
                     "F4_peak_bin": "argmax_t q (secondary; edge-contaminated)"},
        "beta_frame_invariance": ("draw-wise ρ exactly β-frame-invariant (per-draw "
                                  "monotone rescale preserves across-city ranks); "
                                  "bootstrap ρ uses empire-β median features (β "
                                  "posterior tight → near-invariant); slopes in "
                                  "empire-β units (β median %.3f)" % float(np.median(beta))),
        "seeds": {"beta_resample": SEED, "bootstrap": BOOT_SEED, "n_boot": N_BOOT},
        "results": results,
        "provenance": {
            "primary_nc": str(h5.PRIMARY_NC), "primary_nc_sha256": _sha256(h5.PRIMARY_NC),
            "h3a_empire_nc": str(lb.H3A_NC["empire"]),
            "city_index": str(h5.CITY_INDEX),
            "reused_code": str(LBR_CODE / "layerb_residual_invert.py"),
        },
        "caveats": ["n=34 low power (|ρ|≳0.34 to clear 95% at n=34)",
                    "not pure demography (Obs 98)",
                    "range restriction 2.19 decades (Obs 100)",
                    "multiple features×tiers×samples — no cherry-pick, no threshold",
                    "inversion cosmetic for rank stats; edge bins excluded"],
    }
    with open(OUT_DIR / "size-vs-dynamics-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=h5._json_default)
    print("  done. outputs in", OUT_DIR)


if __name__ == "__main__":
    main()
