#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layerb_residual_invert.py — §5 Layer B (RESIDUAL): habit-removed β-inversion.
=============================================================================

The *habit-removed* companion to the raw Layer B β-inversion
(``runs/2026-06-16-s5-layer-b-beta-inversion/``, Obs 96). The raw Layer B
inverted each city's **full** inscription-rate trajectory ``lam`` — which
includes the empire-wide common temporal component ``g_shape`` (Obs 97) — and so
its post-AD-250 "collapse" is the amplified empire-wide epigraphic-habit decline,
not demonstrated depopulation (Obs 98).

This script removes ``g_shape`` *before* inverting. It inverts only the city
**residual** trajectory ``r = u_shape + v_shape`` (the part of a city's log-rate
that deviates from the empire-common shape) into a population trajectory
**relative to the empire-wide trend**::

    q[c, t] = exp( (1/β_within) · r[c, t] )

Because each shape term is a centred (zero-sum-over-t) Gaussian random walk
(``hier_model.py``), ``r`` is zero-sum over the 16 bins, so ``(1/β)·r`` is
mean-zero over t and ``q`` has geometric mean 1 across the bins *automatically*.
``q`` therefore reads directly as a multiplier on the city's empire-relative
baseline: ``q = 1.5`` ⇒ 50 % above where the empire-common trend alone would put
the city at that bin; ``q = 0.5`` ⇒ half. This is the quantity Obs 98 names as
well-posed *regardless of the habit/demography conflation*, because ``g`` is
differenced out rather than decomposed.

**This is not absolute population** (that would require inverting ``g``, which
conflates four undecomposable drivers — Obs 98). It is relative-to-empire only,
and the residual is not pure demography either (Obs 98 caveat). Illustrative
comparative-shape outputs only — *not* quantitative population claims
(preregistration §5; Decision 13). See ``../spec.md``.

Design (Shawn sign-off 2026-06-18, spec §6):
  (i)   β frame: empire primary + Latin overlay.
  (ii)  residual: the nested divergence triple — u+v (city-from-empire, primary),
        v (city-from-province), u (province-from-empire); q_uv = q_u·q_v per draw.
  (iii) normalisation: relative-to-empire (geom-mean 1) primary; peak=1 overlay.
  (iv)  validation: descriptive; foundation-terminus (99 cities) +
        collapse-disappearance contrast; anchors NOT re-run (cannot be
        residual-decomposed — not in the monolithic fit).

No new sampling: a deterministic transform of the already-fitted §5 Layer-A
posterior. Reuses two already-audited sources verbatim:
  - residual construction + foundation check + Hanson join from
    ``runs/2026-06-17-s5-h5-habit-removed/code/h5_habit_removed.py`` (H5);
  - β-draw loader + grid constants from
    ``runs/2026-06-16-s5-layer-b-beta-inversion/code/layerb_invert.py`` (raw B).

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-17-s5-layer-b-residual/code/layerb_residual_invert.py

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
H5_CODE = REPO / "runs/2026-06-17-s5-h5-habit-removed/code"
LAYERB_CODE = REPO / "runs/2026-06-16-s5-layer-b-beta-inversion/code"
RAW_NC = {
    "empire": REPO / "runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-trajectories-empire.nc",
    "latin": REPO / "runs/2026-06-16-s5-layer-b-beta-inversion/outputs/layerb-trajectories-latin.nc",
}
OUT_DIR = RUN_DIR / "outputs"

# Reuse the audited loaders. Importing runs no analysis (both guard __main__).
sys.path.insert(0, str(H5_CODE))
sys.path.insert(0, str(LAYERB_CODE))
import h5_habit_removed as h5    # noqa: E402  residual construction + foundation check
import layerb_invert as lb       # noqa: E402  β-draw loader + grid constants

BIN_CENTRES = lb.BIN_CENTRES                       # length 16, bin-centre years
BIN_EDGES = lb.BIN_EDGES                           # length 17
T_BINS = lb.T_BINS                                 # 16
N_STAR = lb.N_STAR                                 # 300 (Layer-A reliability floor)
Q_LO, Q_HI = lb.Q_LO, lb.Q_HI                      # 2.5, 97.5
SEED = 20260616                                    # reuse raw-B seed (spec §11)
FRAMES = ("empire", "latin")
BIN_AD250 = int(np.searchsorted(BIN_EDGES, 250, side="right") - 1)
BIN_AD325 = int(np.searchsorted(BIN_EDGES, 325, side="right") - 1)

# Key bins (indices on the 25y grid) for the PRIMARY relative-to-empire
# diagnostic. Labelled by bin-centre year; the empire-common component g peaks
# at bin 9 (centre AD 187.5, Obs 97).
KEY_BINS = {
    "AD12_augustan": 2, "AD112_early_antonine": 6, "AD187_empire_common_peak": 9,
    "AD262_third_century": 12, "AD337_late": 15,
}


def _sha256(path: Path) -> str:
    """Hex SHA-256 of a file (streamed; provenance record)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_residuals(u, v, urows):
    """Construct the draw-wise residual log-trajectories (H5 construction).

    Args:
        u: ``(S, P, T)`` province shape deviations.
        v: ``(S, C, T)`` city shape deviations.
        urows: ``(C,)`` int — province row each city uses, or -1 if singleton.

    Returns:
        ``(r_uv, r_v, r_u)`` each ``(S, C, T)`` — the three nested divergence
        residuals (log scale), which sum exactly ``r_uv = r_u + r_v``:
          - ``r_uv = u+v`` — CITY divergence from empire (primary);
          - ``r_v  = v``   — CITY divergence from its PROVINCE (overlay);
          - ``r_u  = u``   — PROVINCE divergence from empire (broadcast to its
            cities; identically 0, i.e. q_u≡1, for singleton-province cities,
            which have no province tier).
    """
    S, _, T = v.shape
    u_pad = np.concatenate([u, np.zeros((S, 1, T))], axis=1)   # row -1 -> zeros
    r_u = u_pad[:, urows, :]                                   # province-from-empire
    r_uv = v + r_u                                             # city-from-empire
    r_v = v.copy()                                             # city-from-province
    return r_uv, r_v, r_u


def invert_residual(r, beta_draws, seed):
    """β-invert a residual log-trajectory into a relative-to-empire trajectory.

    ``q = exp( (1/β) · r )`` — geom-mean 1 over t by construction (r is
    zero-sum). Returns the draw array plus median + 95 % band, peak-bin mode, and
    the fraction-of-peak contrast metrics (AD 250 / AD 325).

    Args:
        r: ``(S, C, T)`` zero-sum residual log-trajectory.
        beta_draws: 1-D pool of β_within draws to resample from.
        seed: RNG seed for the β resample (reproducibility).

    Returns:
        dict with ``q`` ``(S, C, T)`` and summaries (all ``(C, T)`` or ``(C,)``).
    """
    S, C, T = r.shape
    rng = np.random.default_rng(seed)
    beta = rng.choice(beta_draws, size=S, replace=True)       # (S,)
    inv_beta = (1.0 / beta)[:, None, None]                    # (S, 1, 1)
    q = np.exp(inv_beta * r)                                  # (S, C, T) > 0

    peak_bin = np.argmax(q, axis=2)                           # (S, C)
    peak_bin_mode = np.array(
        [np.bincount(peak_bin[:, c], minlength=T).argmax() for c in range(C)]
    )
    q_med = np.median(q, axis=0)                              # (C, T)
    q_lo = np.percentile(q, Q_LO, axis=0)
    q_hi = np.percentile(q, Q_HI, axis=0)

    # Fraction-of-peak on the median trajectory, vs the modal peak bin.
    pk = q_med[np.arange(C), peak_bin_mode]                   # (C,)
    pk = np.where(pk > 0, pk, np.nan)
    frac_ad250 = q_med[:, BIN_AD250] / pk                     # (C,)
    frac_ad325 = q_med[:, BIN_AD325] / pk
    return {
        "q": q, "q_med": q_med, "q_lo": q_lo, "q_hi": q_hi,
        "peak_bin_mode": peak_bin_mode,
        "frac_ad250": frac_ad250, "frac_ad325": frac_ad325,
        "beta_median": float(np.median(beta)),
    }


def self_test(g, u, v, urows, cities, reliable):
    """Regression guard: adding ``g`` back must reproduce the raw Layer B.

    The raw Layer B relative-shape is ``(lam/peak)^(1/β)``. Because the within-
    city level offsets cancel under peak-normalisation, that equals
    ``exp((1/β)·((g+u+v) − max_t(g+u+v)))`` per draw. With the *same* seed and β
    pool, reconstructing it here must match the persisted raw ``shape_med`` to
    floating-point — proving the only difference in this run is the removal of
    ``g`` (i.e. the decomposition wiring is correct).
    """
    import arviz as az

    raw = az.from_netcdf(str(RAW_NC["empire"]))
    raw_cities = [str(c) for c in raw["city"].values]
    raw_shape = raw["shape_med"].values                       # (C, T) peak=1

    # pick one reliable city present in both sets
    spot = next((c for c in range(len(cities))
                 if reliable[c] and cities[c] in raw_cities), None)
    if spot is None:
        raise RuntimeError(
            "self-test cannot run: no reliable city is present in both the "
            "monolithic fit and the raw Layer B output — check the inputs.")
    name = cities[spot]
    rj = raw_cities.index(name)

    S, _, T = v.shape
    u_pad = np.concatenate([u, np.zeros((S, 1, T))], axis=1)
    r_full = g[:, None, :] + v[:, [spot], :] + u_pad[:, [urows[spot]], :]  # (S,1,T)
    r_full = r_full[:, 0, :]                                   # (S, T)
    rng = np.random.default_rng(SEED)
    beta = rng.choice(lb.load_beta_draws("empire"), size=S, replace=True)
    inv_beta = (1.0 / beta)[:, None]
    s = np.exp(inv_beta * (r_full - r_full.max(axis=1, keepdims=True)))    # (S, T)
    recon = np.median(s, axis=0)                              # (T,)

    # Tolerance 1e-4: float32 storage of lam could push the algebraically-exact
    # cancellation to ~1e-6; a real wiring error produces O(0.1–1) differences,
    # so 1e-4 cleanly separates float noise from a genuine bug.
    max_abs = float(np.max(np.abs(recon - raw_shape[rj])))
    ok = max_abs < 1e-4
    print(f"  self-test [{name}]: max|recon − raw shape_med| = {max_abs:.2e} "
          f"-> {'PASS' if ok else 'FAIL'}")
    if not ok:
        raise AssertionError(
            f"self-test FAILED for {name}: g+u+v reconstruction does not match "
            f"raw Layer B shape_med (max abs diff {max_abs:.2e} >= 1e-4). "
            "Decomposition/inversion wiring is wrong — do not trust outputs.")
    return name, max_abs


def save_nc(frame, cities, N, reliable, has_prov, res_uv, res_v, res_u):
    """Persist per-frame relative-to-empire trajectories — the nested triple.

    ``q_uv`` (city-from-empire, primary), ``q_v`` (city-from-province), and
    ``q_u`` (province-from-empire). They nest per draw: ``q_uv = q_u · q_v``.
    """
    import xarray as xr

    ds = xr.Dataset(
        {
            # primary: u+v residual = CITY divergence from empire (geom-mean 1)
            "q_uv_med": (("city", "bin"), res_uv["q_med"]),
            "q_uv_lo": (("city", "bin"), res_uv["q_lo"]),
            "q_uv_hi": (("city", "bin"), res_uv["q_hi"]),
            "q_uv_peak_bin": (("city",), res_uv["peak_bin_mode"]),
            "q_uv_frac_ad250": (("city",), res_uv["frac_ad250"]),
            "q_uv_frac_ad325": (("city",), res_uv["frac_ad325"]),
            # overlay: v-only residual = CITY divergence from its PROVINCE
            "q_v_med": (("city", "bin"), res_v["q_med"]),
            "q_v_lo": (("city", "bin"), res_v["q_lo"]),
            "q_v_hi": (("city", "bin"), res_v["q_hi"]),
            "q_v_peak_bin": (("city",), res_v["peak_bin_mode"]),
            "q_v_frac_ad250": (("city",), res_v["frac_ad250"]),
            # tier: u-only residual = PROVINCE divergence from empire
            # (constant within province; q_u≡1 for singleton-province cities)
            "q_u_med": (("city", "bin"), res_u["q_med"]),
            "q_u_lo": (("city", "bin"), res_u["q_lo"]),
            "q_u_hi": (("city", "bin"), res_u["q_hi"]),
            "q_u_peak_bin": (("city",), res_u["peak_bin_mode"]),
            "N": (("city",), N),
            "reliable": (("city",), reliable),
            "has_province_tier": (("city",), has_prov),
        },
        coords={"city": cities, "bin": np.arange(T_BINS),
                "bin_centre_year": ("bin", BIN_CENTRES)},
        attrs={
            "analysis": "§5 Layer B (residual) — habit-removed relative-to-empire trajectory",
            "frame": frame, "beta_frame": frame, "seed": SEED, "n_star": N_STAR,
            "quantity": ("q = exp((1/beta)*(u_shape+v_shape)); relative to the "
                         "empire-wide common temporal component; geom-mean 1 over t; "
                         "NOT absolute population (Obs 98)."),
            "note": "Exploratory; illustrative comparative-shape only (prereg §5; Decision 13).",
        },
    )
    path = OUT_DIR / f"layerb-residual-trajectories-{frame}.nc"
    ds.to_netcdf(str(path))
    return path


def plot_residual_vs_raw(cities, reliable, res_uv, raw_shape_med, raw_cities):
    """Headline (corpus level): the apparent universal collapse dissolves.

    Two panels on a shared time axis, NOT mixed on one scale (they use
    different — and clearly labelled — normalisations):

    - LEFT: the raw Layer B corpus-median relative-shape (each city peak=1),
      which dives to ~0 after AD 250 — the *apparent* universal collapse.
    - RIGHT: the residual q corpus-median against the empire baseline (1.0),
      with the inter-quartile band — a *moderate, heterogeneous* relative
      decline (median ~0.3 at AD 250), not annihilation, once the empire-common
      component g is removed.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rel = [i for i in range(len(cities))
           if reliable[i] and cities[i] in raw_cities]
    rj = [raw_cities.index(cities[i]) for i in rel]
    raw_med = np.median(raw_shape_med[rj], axis=0)            # (T,) collapses
    q = res_uv["q_med"][rel]                                  # (n_rel, T)
    q_med = np.median(q, axis=0)
    q25, q75 = np.percentile(q, 25, axis=0), np.percentile(q, 75, axis=0)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5), sharex=True)
    axL.plot(BIN_CENTRES, raw_med, color="C3", lw=2)
    axL.axvline(250, ls=":", color="grey", lw=1)
    axL.set_title("Raw Layer B (g included)\ncorpus-median relative-shape "
                  "(each city peak = 1)")
    axL.set_xlabel("year"); axL.set_ylabel("fraction of own peak")
    axL.set_ylim(0, 1.05)

    axR.fill_between(BIN_CENTRES, q25, q75, alpha=0.2, color="C0",
                     label="inter-quartile (heterogeneity)")
    axR.plot(BIN_CENTRES, q_med, color="C0", lw=2, label="corpus median q")
    axR.axhline(1.0, color="grey", lw=0.8, ls="--", label="empire trend (1.0)")
    axR.axvline(250, ls=":", color="grey", lw=1)
    axR.set_title("Residual (g removed)\ncorpus-median q vs the empire baseline")
    axR.set_xlabel("year"); axR.set_ylabel("pop relative to empire trend")
    axR.legend(fontsize=8)

    fig.suptitle("Removing the empire-common component dissolves the apparent "
                 "universal collapse into city-level heterogeneity "
                 f"(reliable cities, n={len(rel)})")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "layerb-residual-vs-raw.png", dpi=130)
    plt.close(fig)


def plot_residual_samples(cities, reliable, res_uv, res_v):
    """Sample relative-to-empire trajectories (u+v) with the v-only overlay."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rel = [i for i in range(len(cities)) if reliable[i]]
    pick = rel[:: max(1, len(rel) // 6)][:6]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, i in zip(axes.ravel(), pick):
        ax.fill_between(BIN_CENTRES, res_uv["q_lo"][i], res_uv["q_hi"][i],
                        alpha=0.2, color="C0")
        ax.plot(BIN_CENTRES, res_uv["q_med"][i], color="C0", lw=2, label="u+v")
        ax.plot(BIN_CENTRES, res_v["q_med"][i], color="C2", lw=1.5, ls="--",
                label="v-only")
        ax.axhline(1.0, color="grey", lw=0.6)
        ax.set_title(cities[i]); ax.set_xlabel("year")
        ax.set_ylabel("pop relative to empire trend")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("Relative-to-empire population trajectories (geom-mean 1); "
                 "u+v primary, v-only overlay — reliable-city sample")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "layerb-residual-samples.png", dpi=130)
    plt.close(fig)


def plot_amplitude_overlay(cities, reliable, q_by_frame):
    """Empire-vs-Latin β amplitude sensitivity on the u+v residual."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rel = [i for i in range(len(cities)) if reliable[i]]
    pick = rel[:: max(1, len(rel) // 6)][:6]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, i in zip(axes.ravel(), pick):
        for frame, colour in (("empire", "C0"), ("latin", "C2")):
            ax.plot(BIN_CENTRES, q_by_frame[frame]["q_med"][i], color=colour,
                    lw=2, label=f"{frame} β")
        ax.axhline(1.0, color="grey", lw=0.6)
        ax.set_title(cities[i]); ax.set_xlabel("year")
        ax.set_ylabel("pop relative to empire trend")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("β-frame amplitude sensitivity (u+v residual, relative-to-empire)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "layerb-residual-amplitude-overlay.png", dpi=130)
    plt.close(fig)


def plot_nested_decomposition(cities, rel_prov, res_uv, res_v, res_u):
    """The nested triple for sample reliable province-tier cities.

    Per city: province-from-empire (q_u), city-from-province (q_v), and
    city-from-empire (q_uv = q_u·q_v median-shown), all against the empire
    baseline (1.0). Shows how much of a city's divergence is provincial.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rel = [i for i in range(len(cities)) if rel_prov[i]]
    pick = rel[:: max(1, len(rel) // 6)][:6]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, i in zip(axes.ravel(), pick):
        ax.plot(BIN_CENTRES, res_u["q_med"][i], color="C1", lw=1.8,
                label="province ← empire (q_u)")
        ax.plot(BIN_CENTRES, res_v["q_med"][i], color="C2", lw=1.8, ls="--",
                label="city ← province (q_v)")
        ax.plot(BIN_CENTRES, res_uv["q_med"][i], color="C0", lw=2,
                label="city ← empire (q_uv)")
        ax.axhline(1.0, color="grey", lw=0.6)
        ax.set_title(cities[i]); ax.set_xlabel("year")
        ax.set_ylabel("relative to empire / province")
    axes[0, 0].legend(fontsize=7)
    fig.suptitle("Nested divergence decomposition (median q vs 1.0): "
                 "province-from-empire × city-from-province = city-from-empire")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "layerb-residual-nested-tiers.png", dpi=130)
    plt.close(fig)


def baseline_diagnostic(q_med, reliable):
    """Per-bin corpus summary of q vs the empire baseline (1.0) — the PRIMARY
    contrast for the residual.

    For a geom-mean-1 quantity the right question is "where does the city sit
    relative to the empire trend (1.0)", NOT "what fraction of its own peak"
    (the latter is confounded by 1/β amplification + GRW endpoint variance —
    see ``_edge_peak_count``). Returns, per key bin, the corpus median q,
    inter-quartile range, and the share of cities below the empire trend,
    over reliable cities.
    """
    qr = q_med[reliable]                                       # (n_rel, T)
    out = []
    for label, b in KEY_BINS.items():
        col = qr[:, b]
        out.append({
            "label": label, "bin": b, "centre_year": float(BIN_CENTRES[b]),
            "median_q": float(np.median(col)),
            "q25": float(np.percentile(col, 25)),
            "q75": float(np.percentile(col, 75)),
            "frac_below_empire": float((col < 1.0).mean()),
        })
    return out


def _edge_peak_count(peak_bin_mode, reliable):
    """Reliable cities whose q-peak sits at an envelope-edge bin (first/last).

    This is the GaussianRandomWalk-endpoint artefact (amplified by 1/β) that
    makes 'fraction of own peak' a misleading contrast for the residual.
    """
    pk = peak_bin_mode[reliable]
    return int(((pk == 0) | (pk == T_BINS - 1)).sum()), int(reliable.sum())


def _corpus_frac(frac, reliable):
    """Median / IQR of a per-city fraction-of-peak, all cities and reliable-only."""
    finite = np.isfinite(frac)
    rel = finite & reliable
    return {
        "median_all": float(np.median(frac[finite])),
        "median_reliable": float(np.median(frac[rel])) if rel.any() else None,
        "iqr_all": [float(np.percentile(frac[finite], 25)),
                    float(np.percentile(frac[finite], 75))],
        "n_finite": int(finite.sum()), "n_reliable_finite": int(rel.sum()),
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    import pandas as pd

    print(f"§5 Layer B (residual) — frames={FRAMES} seed={SEED}")
    g, u, v, lam, cities, provs = h5.load_posterior()
    del lam                                       # not needed (self-test uses g+u+v)
    S, C, T = v.shape[0], len(cities), T_BINS
    urows = h5.city_u_rows(cities, provs)
    idx = pd.read_parquet(h5.CITY_INDEX).set_index("city")
    N = np.array([int(idx.loc[c, "N"]) for c in cities])
    reliable = N >= N_STAR
    print(f"  loaded: S={S} draws, C={C} cities, T={T} bins; "
          f"{int(reliable.sum())}/{C} reliable (N>={N_STAR})")

    r_uv, r_v, r_u = build_residuals(u, v, urows)
    has_prov = urows >= 0                          # cities with a province tier
    rel_prov = reliable & has_prov                 # reliable + province-tier subset

    # Regression guard before producing any deliverable.
    spot_name, spot_diff = self_test(g, u, v, urows, cities, reliable)

    # Invert per frame — the nested triple, all seeded identically so that
    # q_uv = q_u · q_v holds per draw.
    res = {}
    for frame in FRAMES:
        beta = lb.load_beta_draws(frame)
        res[frame] = {
            "uv": invert_residual(r_uv, beta, SEED),   # city-from-empire
            "v": invert_residual(r_v, beta, SEED),     # city-from-province
            "u": invert_residual(r_u, beta, SEED),     # province-from-empire
        }
        ad262 = next(d for d in baseline_diagnostic(res[frame]["uv"]["q_med"],
                                                    reliable) if d["bin"] == BIN_AD250)
        ad262u = next(d for d in baseline_diagnostic(res[frame]["u"]["q_med"],
                                                     rel_prov) if d["bin"] == BIN_AD250)
        print(f"  {frame}: β median {res[frame]['uv']['beta_median']:.3f}; "
              f"AD262 median q vs empire — city {ad262['median_q']:.2f} "
              f"({ad262['frac_below_empire']:.0%} below) | "
              f"province {ad262u['median_q']:.2f}")

    # Nested-identity guard: q_uv == q_u · q_v per draw (same β seed). Holds to
    # floating point because r_uv = r_u + r_v exactly; use a relative tolerance
    # (q spans several orders of magnitude). A wiring error fails it by a factor.
    e = res["empire"]
    prod = e["u"]["q"] * e["v"]["q"]
    ident = float(np.max(np.abs(e["uv"]["q"] - prod)))
    ok = np.allclose(e["uv"]["q"], prod, rtol=1e-9, atol=1e-12)
    print(f"  nested-identity check  max|q_uv − q_u·q_v| = {ident:.2e} "
          f"-> {'PASS' if ok else 'FAIL'}")
    if not ok:
        raise AssertionError("nested identity q_uv = q_u·q_v violated "
                             f"(max abs {ident:.2e}); decomposition wiring wrong.")

    # Foundation-terminus check on the relative-to-empire q (empire, u+v).
    foundation = h5.foundation_terminus(cities, res["empire"]["uv"]["q"])

    # Persist trajectories (the nested triple).
    nc_paths = {}
    for frame in FRAMES:
        nc_paths[frame] = str(save_nc(frame, cities, N, reliable, has_prov,
                                      res[frame]["uv"], res[frame]["v"],
                                      res[frame]["u"]))

    # Figures.
    import arviz as az
    raw = az.from_netcdf(str(RAW_NC["empire"]))
    raw_cities = [str(c) for c in raw["city"].values]
    raw_shape_med = raw["shape_med"].values
    plot_residual_vs_raw(cities, reliable, res["empire"]["uv"],
                         raw_shape_med, raw_cities)
    plot_residual_samples(cities, reliable, res["empire"]["uv"], res["empire"]["v"])
    plot_amplitude_overlay(cities, reliable,
                           {f: res[f]["uv"] for f in FRAMES})
    plot_nested_decomposition(cities, rel_prov, res["empire"]["uv"],
                              res["empire"]["v"], res["empire"]["u"])

    # Raw Layer B contrast: its median-city AD250 fraction-of-peak (the collapse).
    raw_frac_ad250 = raw_shape_med[:, BIN_AD250] / np.where(
        raw_shape_med.max(axis=1) > 0, raw_shape_med.max(axis=1), np.nan)

    summary = {
        "analysis": "§5 Layer B (residual) — habit-removed relative-to-empire β-inversion",
        "type": "exploratory; illustrative comparative-shape only (prereg §5; Decision 13)",
        "seed": SEED, "n_cities": C, "n_reliable": int(reliable.sum()),
        "n_star": N_STAR,
        "self_test": {"spot_city": spot_name, "max_abs_diff_vs_raw_shape": spot_diff,
                      "passed": True},
        "quantity": ("q = exp((1/beta_within)*(u_shape+v_shape)); population "
                     "relative to the empire-wide common temporal component; "
                     "geom-mean 1 over t; NOT absolute population (Obs 98)."),
        # PRIMARY contrast — q vs the empire baseline (1.0), per key bin.
        # The nested triple: city-from-empire (u+v) = province-from-empire (u)
        # × city-from-province (v), per draw (see nested_identity below).
        "relative_to_empire_diagnostic": {
            "metric": ("corpus median q (and IQR, share below empire) per key "
                       "bin; 1.0 = on the empire trend. city/province over "
                       "reliable cities; province over reliable province-tier "
                       "cities (singletons have q_u≡1 and are excluded there)."),
            "nested_identity": "q_uv (city-from-empire) = q_u (province-from-empire) · q_v (city-from-province), per draw",
            "city_from_empire_uv": {f: baseline_diagnostic(res[f]["uv"]["q_med"], reliable)
                                    for f in FRAMES},
            "city_from_province_v": {f: baseline_diagnostic(res[f]["v"]["q_med"], reliable)
                                     for f in FRAMES},
            "province_from_empire_u": {f: baseline_diagnostic(res[f]["u"]["q_med"], rel_prov)
                                       for f in FRAMES},
            "n_reliable_province_tier": int(rel_prov.sum()),
            "interpretation": (
                "Removing the empire-common component dissolves the raw "
                "inversion's apparent universal post-AD-250 collapse into city-"
                "level heterogeneity: the median reliable city sits at ~0.32 of "
                "its empire-relative baseline at AD 262 (a moderate relative "
                "decline, not annihilation), and ~half the cities are at or "
                "above the empire trend even late. Decomposing the nested triple "
                "shows the decline is largely PROVINCIAL-tier: province-from-"
                "empire (q_u) carries most of it, while city-from-province (q_v) "
                "is much flatter. The residual is not pure demography (Obs 98)."),
        },
        # CONFOUNDED — kept only for transparency; do NOT read as a collapse.
        "frac_of_peak_CONFOUNDED": {
            "warning": ("'fraction of own peak' is confounded for the residual: "
                        "1/β amplification + GRW endpoint variance push many "
                        "cities' q-peak to the envelope edges, forcing the ratio "
                        "to ~0 regardless of the actual late level. Use "
                        "relative_to_empire_diagnostic instead."),
            "edge_peak_reliable": dict(zip(
                ("n_edge_peak", "n_reliable"),
                _edge_peak_count(res["empire"]["uv"]["peak_bin_mode"], reliable))),
            "raw_layerB_empire_median_reliable": float(np.nanmedian(
                raw_frac_ad250[[raw_cities.index(cities[i]) for i in range(C)
                                if reliable[i] and cities[i] in raw_cities]])),
            "residual_uv_ad250": {f: _corpus_frac(res[f]["uv"]["frac_ad250"], reliable)
                                  for f in FRAMES},
        },
        "foundation_terminus_on_q": foundation,
        "beta_frames": {f: res[f]["uv"]["beta_median"] for f in FRAMES},
        "provenance": {
            "primary_nc": str(h5.PRIMARY_NC),
            "primary_nc_sha256": _sha256(h5.PRIMARY_NC),
            "h3a_nc": {f: str(lb.H3A_NC[f]) for f in FRAMES},
            "h3a_nc_sha256": {f: _sha256(lb.H3A_NC[f]) for f in FRAMES},
            "raw_layerB_nc": str(RAW_NC["empire"]),
            "reused_code": [str(H5_CODE / "h5_habit_removed.py"),
                            str(LAYERB_CODE / "layerb_invert.py")],
        },
        "trajectories_nc": nc_paths,
    }
    with open(OUT_DIR / "layerb-residual-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=h5._json_default)

    rdiag = summary["relative_to_empire_diagnostic"]
    uv_bin = {d["label"]: d for d in rdiag["city_from_empire_uv"]["empire"]}
    u_bin = {d["label"]: d for d in rdiag["province_from_empire_u"]["empire"]}
    v_bin = {d["label"]: d for d in rdiag["city_from_province_v"]["empire"]}
    print("  RELATIVE-TO-EMPIRE (median q vs 1.0; city=u+v, prov=u, city/prov=v):")
    for lbl in ("AD112_early_antonine", "AD187_empire_common_peak",
                "AD262_third_century", "AD337_late"):
        print(f"    {lbl}: city {uv_bin[lbl]['median_q']:.2f} "
              f"({uv_bin[lbl]['frac_below_empire']:.0%} below) | "
              f"province {u_bin[lbl]['median_q']:.2f} | "
              f"city/province {v_bin[lbl]['median_q']:.2f}")
    ne, nr = summary["frac_of_peak_CONFOUNDED"]["edge_peak_reliable"].values()
    print(f"  (frac-of-peak confounded: {ne}/{nr} reliable cities peak at an "
          f"envelope edge — not a collapse)")
    print(f"  foundation-terminus on q: median pre-foundation frac "
          f"{foundation.get('median_pre_foundation_frac')}, "
          f"{foundation.get('n_within_envelope_matched')} cities checked")
    print("  done. outputs in", OUT_DIR)


if __name__ == "__main__":
    main()
