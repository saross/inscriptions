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
  (ii)  residual: u+v primary; v-only overlay (remove empire AND province).
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
        ``(r_uv, r_v)`` each ``(S, C, T)``: the u+v residual (primary) and the
        v-only residual (overlay; province removed too).
    """
    S, _, T = v.shape
    u_pad = np.concatenate([u, np.zeros((S, 1, T))], axis=1)   # row -1 -> zeros
    r_uv = v + u_pad[:, urows, :]                              # u+v  (S, C, T)
    r_v = v.copy()                                             # v-only (S, C, T)
    return r_uv, r_v


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


def save_nc(frame, cities, N, reliable, res_uv, res_v):
    """Persist per-frame relative-to-empire trajectories (u+v primary; v-only)."""
    import xarray as xr

    ds = xr.Dataset(
        {
            # primary: u+v residual, relative-to-empire (geom-mean 1)
            "q_uv_med": (("city", "bin"), res_uv["q_med"]),
            "q_uv_lo": (("city", "bin"), res_uv["q_lo"]),
            "q_uv_hi": (("city", "bin"), res_uv["q_hi"]),
            "q_uv_peak_bin": (("city",), res_uv["peak_bin_mode"]),
            "q_uv_frac_ad250": (("city",), res_uv["frac_ad250"]),
            "q_uv_frac_ad325": (("city",), res_uv["frac_ad325"]),
            # overlay: v-only residual (province removed too)
            "q_v_med": (("city", "bin"), res_v["q_med"]),
            "q_v_lo": (("city", "bin"), res_v["q_lo"]),
            "q_v_hi": (("city", "bin"), res_v["q_hi"]),
            "q_v_peak_bin": (("city",), res_v["peak_bin_mode"]),
            "q_v_frac_ad250": (("city",), res_v["frac_ad250"]),
            "N": (("city",), N),
            "reliable": (("city",), reliable),
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
    """Headline: the spurious post-AD-250 collapse vanishes once g is removed.

    For a sample of reliable cities, overlay the raw Layer B relative-shape
    (peak=1, which collapses to ~0 post-AD-250) against the residual q
    (peak-normalised for visual comparability) — the residual tail lifts.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rel = [i for i in range(len(cities))
           if reliable[i] and cities[i] in raw_cities]
    pick = rel[:: max(1, len(rel) // 6)][:6]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, i in zip(axes.ravel(), pick):
        rj = raw_cities.index(cities[i])
        q = res_uv["q_med"][i]
        q_pknorm = q / max(q.max(), 1e-12)
        ax.plot(BIN_CENTRES, raw_shape_med[rj], color="C3", lw=2,
                label="raw Layer B (incl. g)")
        ax.plot(BIN_CENTRES, q_pknorm, color="C0", lw=2,
                label="residual q (g removed)")
        ax.axvline(250, ls=":", color="grey", lw=1)
        ax.set_title(f"{cities[i]} (AD250 frac-of-peak: "
                     f"raw {raw_shape_med[rj][BIN_AD250]:.2f} / "
                     f"resid {q_pknorm[BIN_AD250]:.2f})", fontsize=9)
        ax.set_xlabel("year"); ax.set_ylabel("fraction of peak")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("Habit-removed residual vs raw Layer B — the post-AD-250 "
                 "collapse is empire-common (in g), not city demography")
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

    r_uv, r_v = build_residuals(u, v, urows)

    # Regression guard before producing any deliverable.
    spot_name, spot_diff = self_test(g, u, v, urows, cities, reliable)

    # Invert per frame (u+v primary; v-only overlay), seeded identically.
    res = {}
    for frame in FRAMES:
        beta = lb.load_beta_draws(frame)
        res[frame] = {
            "uv": invert_residual(r_uv, beta, SEED),
            "v": invert_residual(r_v, beta, SEED),
        }
        f250 = _corpus_frac(res[frame]["uv"]["frac_ad250"], reliable)
        print(f"  {frame}: β median {res[frame]['uv']['beta_median']:.3f}; "
              f"u+v AD250 frac-of-peak median (reliable) "
              f"{f250['median_reliable']:.2f}")

    # Foundation-terminus check on the relative-to-empire q (empire, u+v).
    foundation = h5.foundation_terminus(cities, res["empire"]["uv"]["q"])

    # Persist trajectories.
    nc_paths = {}
    for frame in FRAMES:
        nc_paths[frame] = str(save_nc(frame, cities, N, reliable,
                                      res[frame]["uv"], res[frame]["v"]))

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
        "collapse_contrast": {
            "metric": "median-trajectory inscription/pop AD250 as fraction of peak",
            "raw_layerB_empire_median_reliable": float(np.nanmedian(
                raw_frac_ad250[[raw_cities.index(cities[i]) for i in range(C)
                                if reliable[i] and cities[i] in raw_cities]])),
            "residual_uv": {f: _corpus_frac(res[f]["uv"]["frac_ad250"], reliable)
                            for f in FRAMES},
            "residual_uv_ad325": {f: _corpus_frac(res[f]["uv"]["frac_ad325"], reliable)
                                  for f in FRAMES},
            "residual_v_only": {f: _corpus_frac(res[f]["v"]["frac_ad250"], reliable)
                                for f in FRAMES},
            "interpretation": ("raw ~0 (empire-common habit collapse in g, amplified "
                               "by 1/β); residual lifts toward 1 once g is removed."),
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

    cc = summary["collapse_contrast"]
    print(f"  COLLAPSE CONTRAST (AD250 frac-of-peak, reliable median): "
          f"raw {cc['raw_layerB_empire_median_reliable']:.2f} -> "
          f"residual u+v empire {cc['residual_uv']['empire']['median_reliable']:.2f}")
    print(f"  foundation-terminus on q: median pre-foundation frac "
          f"{foundation.get('median_pre_foundation_frac')}, "
          f"{foundation.get('n_within_envelope_matched')} cities checked")
    print("  done. outputs in", OUT_DIR)


if __name__ == "__main__":
    main()
