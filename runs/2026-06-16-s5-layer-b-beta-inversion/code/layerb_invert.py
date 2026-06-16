#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layerb_invert.py — §5 Layer B: β-inversion of inscription-rate trajectories
===========================================================================

Invert each city's Layer-A posterior inscription-rate trajectory into a relative
(and Hanson-anchored) **population** trajectory, via the H3a cross-sectional
scaling law ``insc ∝ pop^β`` ⇒ ``pop ∝ insc^(1/β_within)``. Exploratory; the
output is illustrative comparative-shape, NOT a quantitative population claim
(preregistration §5 "Extension (Layer B)"; Decision 13).

See ``../spec.md`` for the full design, the four signed-off decisions, the
critical-friend caveats (cross-sectional→temporal substitution; the 1/β > 1
amplification; posterior independence; Hanson anchoring; the N*=300 floor), and
the validation-gate framing.

Method (draw-wise; spec §4)
---------------------------
For city ``c``, bin ``t``, joint posterior draw ``k``:

1. ``lam_k[c, t]`` — the Layer-A inscription-rate draw (8,000 draws total).
2. ``β_k`` — one draw resampled (seeded, with replacement) from the H3a
   ``beta_within`` posterior of the chosen frame; valid Monte-Carlo propagation
   of two independent posteriors.
3. relative shape   ``s_k[c,t] = ( lam_k[c,t] / max_t lam_k[c,t] )^(1/β_k)``
4. Hanson-anchored  ``pop_k[c,t] = pop_max[c] · s_k[c,t]`` (peak = Hanson est.)

For the 268 small-N **target** cities this is a deterministic transform of an
existing posterior (no MCMC). The seven large validation anchors are NOT in the
monolithic fit, so the gate (Ostia, Pompeii) re-fits each standalone via the
single-city ``model.py`` and applies the identical transform.

Outputs (``--out-dir``, default ``../outputs``)
-----------------------------------------------
- ``layerb-trajectories-<frame>.nc`` — per-city posterior summary trajectories
  (relative-shape + anchored: median + 2.5/97.5 % bands) for every target city.
- ``layerb-summary.json`` — per-city peak bin, peak population, decline ratios,
  reliability tag (N*≥300); validation-gate outcomes; β frame(s); seed; input
  sha256 provenance.
- ``layerb-anchor-<city>-<frame>.nc`` — the standalone anchor posteriors (gate).
- figures: target-city small-multiples, anchor-gate panels, empire-vs-Latin
  amplitude overlay.

Run (on sapphire, inside the project venv)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-16-s5-layer-b-beta-inversion/code/layerb_invert.py \
        --frames empire latin --seed 20260616

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-16, on Shawn's brief (spec signed off).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths — resolved relative to this script so the run is host-agnostic.
# --------------------------------------------------------------------------- #

THIS = Path(__file__).resolve()
RUN_DIR = THIS.parents[1]                       # runs/2026-06-16-s5-layer-b-beta-inversion
REPO = THIS.parents[3]                          # repository root
LAYER_A_CODE = REPO / "runs/2026-05-30-s5-small-n-trajectories/code"
PRIMARY_NC = LAYER_A_CODE / "production/monolithic-inscription-25y.nc"
CACHE_DIR = LAYER_A_CODE / "prepared"
CITY_INDEX = CACHE_DIR / "city-index.parquet"
H3A_NC = {
    "empire": REPO / "runs/2026-06-04-h3a-confirmatory/outputs/idata-primary.nc",
    "latin": REPO / "runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc",
}
DEFAULT_OUT = RUN_DIR / "outputs"

# Layer-A modules (dataprep for the bin grid + cache loader; model for anchors).
sys.path.insert(0, str(LAYER_A_CODE))
import dataprep as dp  # noqa: E402
import model as single  # noqa: E402

BIN_EDGES = dp.BIN_EDGES                         # length 17: -50, -25, ..., 350
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0
T_BINS = dp.N_BINS                              # 16
N_STAR = 300                                    # Layer-A reliability floor (RESULTS §2)
Q_LO, Q_HI = 2.5, 97.5                          # credible-band percentiles

# Calendar landmarks (for the validation gate), as bin indices on the 25y grid.
# Bin t covers [BIN_EDGES[t], BIN_EDGES[t+1]); AD 79 -> bin 5 ([75,100)); the
# "2nd century AD" (AD 100-200) -> bins 6-9.
BIN_AD79 = int(np.searchsorted(BIN_EDGES, 79, side="right") - 1)
SECOND_CENTURY_BINS = [t for t in range(T_BINS) if 100 <= BIN_EDGES[t] < 200]


# --------------------------------------------------------------------------- #
# Loading.
# --------------------------------------------------------------------------- #

def _sha256(path: Path) -> str:
    """Return the hex SHA-256 of a file (streamed, for the provenance record)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_trajectory_posterior(nc_path: Path) -> tuple[np.ndarray, list[str]]:
    """Load the monolithic Layer-A posterior inscription rate ``lam``.

    Args:
        nc_path: Path to ``monolithic-inscription-25y.nc``.

    Returns:
        ``(lam, cities)`` where ``lam`` is ``(S, C, T)`` (sample, city, bin) with
        ``S`` = chains × draws, and ``cities`` are the city names in column order.
    """
    import arviz as az

    idata = az.from_netcdf(str(nc_path))
    post = idata.posterior["lam"]                # dims (chain, draw, city, bin)
    arr = (
        post.stack(sample=("chain", "draw"))
        .transpose("sample", "city", "bin")
        .values.astype(np.float64)
    )
    cities = [str(c) for c in post.coords["city"].values]
    return arr, cities


def load_beta_draws(frame: str) -> np.ndarray:
    """Load the H3a ``beta_within`` posterior draws for a frame.

    Args:
        frame: ``"empire"`` or ``"latin"``.

    Returns:
        1-D array of β_within draws (chains × draws).
    """
    import arviz as az

    idata = az.from_netcdf(str(H3A_NC[frame]))
    bw = idata.posterior["beta_within"]          # dims (chain, draw)
    return bw.stack(sample=("chain", "draw")).values.astype(np.float64)


def load_city_index() -> pd.DataFrame:
    """Load the Layer-A city index (city, province, pop_est, N, bucket)."""
    return pd.read_parquet(CITY_INDEX)


# --------------------------------------------------------------------------- #
# The inversion.
# --------------------------------------------------------------------------- #

def invert(
    lam: np.ndarray,
    beta_draws: np.ndarray,
    pop_max: np.ndarray,
    *,
    seed: int,
) -> dict[str, np.ndarray]:
    """β-invert a trajectory posterior into relative-shape + anchored population.

    Args:
        lam: ``(S, C, T)`` posterior inscription rates (sample, city, bin).
        beta_draws: 1-D pool of β_within posterior draws to resample from.
        pop_max: ``(C,)`` per-city Hanson population anchor (peak population).
        seed: RNG seed for the β resample (reproducibility).

    Returns:
        Dict of posterior summaries (all ``(C, T)`` unless noted):
        ``shape_med/shape_lo/shape_hi`` — relative shape (peak = 1) median + band;
        ``pop_med/pop_lo/pop_hi`` — Hanson-anchored population median + band;
        ``peak_bin_mode`` ``(C,)`` — modal argmax bin over draws;
        ``p_peak_2c`` ``(C,)`` — posterior P(peak bin in the 2nd century AD).
    """
    S, C, T = lam.shape
    rng = np.random.default_rng(seed)
    beta = rng.choice(beta_draws, size=S, replace=True)      # (S,)
    inv_beta = (1.0 / beta)[:, None, None]                   # (S,1,1)

    peak = lam.max(axis=2, keepdims=True)                    # (S, C, 1) > 0
    shape = (lam / peak) ** inv_beta                         # (S, C, T) in (0, 1]
    pop = pop_max[None, :, None] * shape                     # (S, C, T)

    # Per-draw argmax bin (population peak == inscription peak; transform is
    # monotone in lam), summarised across draws.
    peak_bin = np.argmax(lam, axis=2)                        # (S, C)
    peak_bin_mode = np.array(
        [np.bincount(peak_bin[:, c], minlength=T).argmax() for c in range(C)]
    )
    in_2c = np.isin(peak_bin, SECOND_CENTURY_BINS)           # (S, C) bool
    p_peak_2c = in_2c.mean(axis=0)                           # (C,)

    def band(a: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            np.median(a, axis=0),
            np.percentile(a, Q_LO, axis=0),
            np.percentile(a, Q_HI, axis=0),
        )

    shape_med, shape_lo, shape_hi = band(shape)
    pop_med, pop_lo, pop_hi = band(pop)
    return {
        "shape_med": shape_med, "shape_lo": shape_lo, "shape_hi": shape_hi,
        "pop_med": pop_med, "pop_lo": pop_lo, "pop_hi": pop_hi,
        "peak_bin_mode": peak_bin_mode, "p_peak_2c": p_peak_2c,
    }


def _decline_ratios(pop_med: np.ndarray, peak_bin_mode: np.ndarray) -> dict:
    """Median-trajectory decline ratios relative to the modal peak bin.

    Returns per-city ``pop(AD 250)/peak`` and ``pop(last bin)/peak`` on the
    median trajectory (illustrative; reads with the epigraphic-habit caveat).
    """
    C = pop_med.shape[0]
    bin_ad250 = int(np.searchsorted(BIN_EDGES, 250, side="right") - 1)
    out = {"bin_ad250": bin_ad250, "ratio_ad250": [], "ratio_last": []}
    for c in range(C):
        pk = pop_med[c, peak_bin_mode[c]]
        pk = pk if pk > 0 else np.nan
        out["ratio_ad250"].append(float(pop_med[c, bin_ad250] / pk))
        out["ratio_last"].append(float(pop_med[c, -1] / pk))
    return out


# --------------------------------------------------------------------------- #
# Validation gate — standalone anchor re-fits (the only MCMC).
# --------------------------------------------------------------------------- #

def fit_anchor_standalone(
    city: str, *, draws: int, tune: int, chains: int, seed: int
) -> np.ndarray:
    """Re-fit one large anchor standalone (single-city model) and return ``lam``.

    Mirrors Layer A's own anchor-validation step (the anchors are not in the
    monolithic fit). Saves nothing here; the caller persists the posterior.

    Args:
        city: Anchor city name (must be cached).
        draws, tune, chains: Sampler sizing.
        seed: Sampler seed.

    Returns:
        ``(lam, idata, conv)``: ``lam`` is ``(S, T)`` posterior inscription rates
        (sample, bin); ``idata`` the full posterior (persisted by the caller);
        ``conv`` the convergence summary dict.
    """
    import arviz as az

    bundle = dp.load_city(CACHE_DIR, city)
    A = np.asarray(bundle["A"], dtype=np.float64)
    idata = single.fit(
        A, draws=draws, tune=tune, chains=chains,
        target_accept=0.99, random_seed=seed, progressbar=False,
    )
    conv = single.convergence_summary(idata)
    print(f"    [{city}] anchor fit: R̂={conv['max_rhat']:.4f} "
          f"ESS={conv['min_ess_bulk']:.0f} div={conv['n_divergences']}")
    post = idata.posterior["lam"]                # dims (chain, draw, <bin>)
    bin_dim = [d for d in post.dims if d not in ("chain", "draw")][0]
    arr = (
        post.stack(sample=("chain", "draw"))
        .transpose("sample", bin_dim)
        .values.astype(np.float64)
    )
    return arr, idata, conv


def validate_anchor(
    city: str,
    lam_anchor: np.ndarray,         # (S, T)
    pop_max_city: float,
    beta_draws: np.ndarray,
    *,
    seed: int,
) -> dict:
    """Invert an anchor and summarise the gate read (descriptive; spec §7)."""
    res = invert(lam_anchor[:, None, :], beta_draws, np.array([pop_max_city]),
                 seed=seed)
    peak_bin = int(res["peak_bin_mode"][0])
    return {
        "city": city,
        "peak_bin_mode": peak_bin,
        "peak_bin_years": f"AD {int(BIN_EDGES[peak_bin])}-{int(BIN_EDGES[peak_bin + 1])}",
        "p_peak_2nd_century": float(res["p_peak_2c"][0]),
        "shape_med": res["shape_med"][0].tolist(),
        "pop_med": res["pop_med"][0].tolist(),
        "pop_lo": res["pop_lo"][0].tolist(),
        "pop_hi": res["pop_hi"][0].tolist(),
        # Pompeii-specific consistency: relative mass after AD 79 should be tiny.
        "post_ad79_shape_frac": float(
            res["shape_med"][0, BIN_AD79 + 1:].sum()
            / max(res["shape_med"][0].sum(), 1e-12)
        ),
    }


# --------------------------------------------------------------------------- #
# Persistence + plotting.
# --------------------------------------------------------------------------- #

def save_trajectories(out_dir: Path, frame: str, cities: list[str],
                      res: dict, idx: pd.DataFrame) -> Path:
    """Write per-city summary trajectories to NetCDF (via xarray)."""
    import xarray as xr

    n_map = idx.set_index("city")["N"].to_dict()
    pop_map = idx.set_index("city")["pop_est"].to_dict()
    ds = xr.Dataset(
        {
            "shape_med": (("city", "bin"), res["shape_med"]),
            "shape_lo": (("city", "bin"), res["shape_lo"]),
            "shape_hi": (("city", "bin"), res["shape_hi"]),
            "pop_med": (("city", "bin"), res["pop_med"]),
            "pop_lo": (("city", "bin"), res["pop_lo"]),
            "pop_hi": (("city", "bin"), res["pop_hi"]),
            "peak_bin_mode": (("city",), res["peak_bin_mode"]),
            "p_peak_2c": (("city",), res["p_peak_2c"]),
            "N": (("city",), np.array([n_map[c] for c in cities])),
            "pop_max": (("city",), np.array([pop_map[c] for c in cities])),
            "reliable": (("city",), np.array([n_map[c] >= N_STAR for c in cities])),
        },
        coords={"city": cities, "bin": np.arange(T_BINS),
                "bin_centre_year": ("bin", BIN_CENTRES)},
        attrs={"frame": frame, "beta_frame": frame, "n_star": N_STAR,
               "note": "Illustrative comparative-shape; NOT a population claim."},
    )
    path = out_dir / f"layerb-trajectories-{frame}.nc"
    ds.to_netcdf(str(path))
    return path


def plot_anchor_gate(out_dir: Path, gate: dict, frame: str) -> None:
    """Plot the Ostia/Pompeii anchor population trajectories (gate panels)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cities = list(gate.keys())
    fig, axes = plt.subplots(1, len(cities), figsize=(6 * len(cities), 4.2),
                             squeeze=False)
    for ax, city in zip(axes[0], cities):
        g = gate[city]
        med = np.array(g["pop_med"])
        lo, hi = np.array(g["pop_lo"]), np.array(g["pop_hi"])
        ax.fill_between(BIN_CENTRES, lo, hi, alpha=0.25, color="C0")
        ax.plot(BIN_CENTRES, med, color="C0", lw=2)
        ax.axvspan(100, 200, color="grey", alpha=0.12, label="2nd c. AD")
        if city.lower() == "pompeii":
            ax.axvline(79, color="C3", ls="--", lw=1, label="AD 79")
        ax.axvline(250, color="C1", ls=":", lw=1, label="AD 250")
        ax.set_title(f"{city} — Hanson-anchored population ({frame} β)\n"
                     f"peak {g['peak_bin_years']}, "
                     f"P(peak 2nd c.)={g['p_peak_2nd_century']:.2f}")
        ax.set_xlabel("year (bin centre)")
        ax.set_ylabel("population (illustrative)")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / f"layerb-anchor-gate-{frame}.png", dpi=130)
    plt.close(fig)


def plot_amplitude_overlay(out_dir: Path, cities: list[str],
                           res_by_frame: dict[str, dict], idx: pd.DataFrame) -> None:
    """Overlay empire vs Latin β shapes for a few illustrative reliable cities."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if "latin" not in res_by_frame:
        return
    n_map = idx.set_index("city")["N"].to_dict()
    reliable = [c for c in cities if n_map[c] >= N_STAR]
    pick = reliable[:: max(1, len(reliable) // 6)][:6]
    cidx = {c: i for i, c in enumerate(cities)}
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), squeeze=False)
    for ax, city in zip(axes.ravel(), pick):
        i = cidx[city]
        for frame, colour in (("empire", "C0"), ("latin", "C2")):
            r = res_by_frame[frame]
            ax.plot(BIN_CENTRES, r["shape_med"][i], color=colour, lw=2,
                    label=f"{frame} β")
        ax.set_title(f"{city} (N={n_map[city]})")
        ax.set_xlabel("year"); ax.set_ylabel("relative pop (peak=1)")
        ax.legend(fontsize=8)
    fig.suptitle("β-frame amplitude sensitivity (relative-shape)")
    fig.tight_layout()
    fig.savefig(out_dir / "layerb-amplitude-overlay.png", dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def main() -> None:
    p = argparse.ArgumentParser(description="§5 Layer B β-inversion.")
    p.add_argument("--frames", nargs="+", default=["empire", "latin"],
                   choices=["empire", "latin"])
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    p.add_argument("--seed", type=int, default=20260616)
    p.add_argument("--anchor-draws", type=int, default=1000)
    p.add_argument("--anchor-tune", type=int, default=1000)
    p.add_argument("--anchor-chains", type=int, default=4)
    p.add_argument("--skip-anchors", action="store_true",
                   help="Skip the standalone anchor gate (target cities only).")
    args = p.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"§5 Layer B — frames={args.frames} seed={args.seed}")
    print(f"  primary posterior: {PRIMARY_NC}")
    lam, cities = load_trajectory_posterior(PRIMARY_NC)
    print(f"  loaded lam {lam.shape} (sample, city, bin) — {len(cities)} cities")

    idx = load_city_index()
    pop_map = idx.set_index("city")["pop_est"].to_dict()
    missing = [c for c in cities if c not in pop_map]
    if missing:
        raise ValueError(f"{len(missing)} cities lack pop_est: {missing[:5]}")
    pop_max = np.array([pop_map[c] for c in cities], dtype=np.float64)

    summary: dict = {
        "frames": args.frames, "seed": args.seed, "n_star": N_STAR,
        "n_cities_target": len(cities),
        "n_reliable": int((idx.set_index('city').loc[cities, 'N'] >= N_STAR).sum()),
        "provenance": {
            "primary_nc": str(PRIMARY_NC),
            "primary_nc_sha256": _sha256(PRIMARY_NC),
            "h3a_nc": {f: str(H3A_NC[f]) for f in args.frames},
            "bin_edges": BIN_EDGES.tolist(),
        },
        "per_frame": {}, "anchor_gate": {},
        "note": ("Illustrative comparative-shape outputs only; NOT quantitative "
                 "population claims (prereg §5 Layer B; Decision 13)."),
    }

    res_by_frame: dict[str, dict] = {}
    for frame in args.frames:
        print(f"  inverting (frame={frame}) ...")
        beta = load_beta_draws(frame)
        res = invert(lam, beta, pop_max, seed=args.seed)
        res_by_frame[frame] = res
        path = save_trajectories(out_dir, frame, cities, res, idx)
        dec = _decline_ratios(res["pop_med"], res["peak_bin_mode"])
        summary["per_frame"][frame] = {
            "beta_median": float(np.median(beta)),
            "beta_draws": int(beta.size),
            "trajectories_nc": str(path),
            "median_p_peak_2c": float(np.median(res["p_peak_2c"])),
            "decline": dec,
        }

    # ---- Validation gate (standalone anchor re-fits) ----------------------
    if not args.skip_anchors:
        anchors = ["Ostia", "Pompeii"]
        gate_frame = args.frames[0]                # primary frame for the gate
        beta = load_beta_draws(gate_frame)
        gate: dict = {}
        for city in anchors:
            print(f"  gate: re-fitting anchor {city} standalone ...")
            lam_a, idata_a, conv = fit_anchor_standalone(
                city, draws=args.anchor_draws, tune=args.anchor_tune,
                chains=args.anchor_chains, seed=args.seed)
            idata_a.to_netcdf(str(out_dir / f"layerb-anchor-{city.lower()}.nc"))
            g = validate_anchor(city, lam_a, float(pop_map[city]), beta,
                                seed=args.seed)
            g["convergence"] = conv
            g["gates_pass"] = bool(single.gates_pass(conv))
            if not g["gates_pass"]:
                print(f"    !! WARNING: {city} anchor fit did NOT meet "
                      f"convergence gates (R̂<1.01, ESS≥400, 0 div); "
                      f"gate read is provisional — inspect before reporting.")
            gate[city] = g
        summary["anchor_gate"] = {"frame": gate_frame, "results": gate}
        plot_anchor_gate(out_dir, {c: gate[c] for c in anchors}, gate_frame)

    # ---- Figures + summary -----------------------------------------------
    plot_amplitude_overlay(out_dir, cities, res_by_frame, idx)

    def _json_default(o):
        """Coerce stray numpy scalars so json.dump never crashes on them."""
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"Unserialisable type: {type(o)}")

    with open(out_dir / "layerb-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=_json_default)
    print(f"  wrote {out_dir/'layerb-summary.json'}")
    print("Done.")


if __name__ == "__main__":
    main()
