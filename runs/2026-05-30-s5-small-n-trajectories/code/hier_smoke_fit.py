#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hier_smoke_fit.py — §5 Layer-A hierarchy SMOKE fit + pooling sanity check.
==========================================================================

Fit the hierarchical partial-pooling model (``hier_model.py``) on a SMALL,
representative SMOKE subset of cities (NOT production; not all 267), with the
hyperprior scales pinned by ``prior_predictive.py``. Then run the key
validation: do small-N cities SHRINK toward their province (tighter CIs than a
standalone single-city fit), and does Pompeii's AD 79 collapse stay CONTAINED in
its city tier without dragging the Regio I province mean to zero post-79?

Smoke subset (documented in SMOKE-HIERARCHY.md): one rich province (Latium et
Campania / Regio I — the most target cities + the Pompeii large anchor), two
median provinces (Baetica, Pannonia superior), and three SINGLETON provinces
(Caesarea Maritima/Palaestina, Forum Claudii/Alpes Poeninae, Aleria/Corsica).

Pooling sanity check (the crux):

- For 2-3 small-N cities (N ~ 50-85) present in the subset, compare the
  HIERARCHICAL posterior trajectory to the SAME city fit STANDALONE via
  ``model.py``. We expect: hierarchical median CI width < standalone (shrinkage
  buys precision); report the mean CI-width ratio (hier / standalone) per city.
- Pompeii containment: report the Regio I PROVINCE trajectory (alpha_g + g_shape
  + b_u + u_shape) post-AD-79 — it must NOT collapse to ~0 even though Pompeii's
  CITY trajectory does. We also report a non-Pompeii Regio I city's post-79
  trajectory to confirm other cities keep sensible post-79 mass.

Run (on zbook, in the venv, with threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/hier_smoke_fit.py \
        --draws 1000 --tune 1000 --s-g 0.3 --s-u 0.15 --s-v 0.15

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp          # noqa: E402
import hier_model as hm        # noqa: E402
import model as sm             # noqa: E402  (standalone single-city model)

EDGES = dp.BIN_EDGES
BIN_LO = EDGES[:-1].astype(int)
BIN_HI = EDGES[1:].astype(int)

# --------------------------------------------------------------------------- #
# Smoke subset definition (exact city names; verified against the cache).
# --------------------------------------------------------------------------- #

# Rich province: Latium et Campania / Regio I. Include the Pompeii anchor, a
# couple of mid cities, AND the small-N cities used for the pooling sanity check.
REGIO_I = [
    "Pompeii",            # large anchor (N=4266); AD 79 terminus
    "Puteoli",            # large anchor (N=1723)
    "Capua",              # N=918
    "Misenum",            # N=578
    "Aricia",             # N=386
    "Tibur",              # N=224
    "Cumae",              # N=231
    "Nomentum",           # N=159
    # small-N cities (pooling sanity check targets):
    "Fundi",              # N=85
    "Interamna Lirenas",  # N=73
    "Anagnia",            # N=71
    "Caiatia",            # N=56
    "Cereatae",           # N=54
    "Gabii",              # N=50
]
# Median province 1: Baetica (5 cities, Italian-adjacent provincial).
BAETICA = ["Augusta Emerita", "Corduba", "Astigi", "Urso", "Parlais"]
# Median province 2: Pannonia superior (4 cities, frontier contrast).
PANNONIA = ["Scarbantia", "Vindobona", "Siscia", "Mogentiana"]
# Singletons (province tier dropped; pool toward global).
SINGLETONS = ["Caesarea Maritima", "Forum Claudii", "Aleria"]

SUBSET = REGIO_I + BAETICA + PANNONIA + SINGLETONS

# Small-N cities for the standalone-vs-hierarchical pooling sanity check.
SANITY_CITIES = ["Gabii", "Cereatae", "Caiatia", "Anagnia"]
# Pompeii containment: a non-Pompeii Regio I city to confirm post-79 sanity.
REGIO_I_NONPOMPEII = "Capua"


# --------------------------------------------------------------------------- #
# Trajectory extraction helpers.
# --------------------------------------------------------------------------- #

def city_lam_quantiles(idata, city_idx):
    """Posterior median + 95% CI of ``lam[city_idx, :]`` from a hier fit."""
    lam = idata.posterior["lam"].isel(city=city_idx)   # (chain, draw, bin)
    med = lam.median(("chain", "draw")).values
    lo = lam.quantile(0.025, ("chain", "draw")).values
    hi = lam.quantile(0.975, ("chain", "draw")).values
    return med, lo, hi


def standalone_lam_quantiles(idata):
    """Posterior median + 95% CI of ``lam`` from a single-city fit."""
    lam = idata.posterior["lam"]
    med = lam.median(("chain", "draw")).values
    lo = lam.quantile(0.025, ("chain", "draw")).values
    hi = lam.quantile(0.975, ("chain", "draw")).values
    return med, lo, hi


def province_trajectory(idata, data: hm.HierData, prov_name: str):
    """Province-level expected-rate trajectory exp(alpha_g+g_shape+b_u+u_shape).

    This is the province mean WITHOUT any city deviation — the thing Pompeii must
    not drag to zero post-79.

    Returns:
        ``(med, lo, hi)`` per-bin arrays, or ``None`` if the province has no u
        tier (singleton) in the subset.
    """
    if prov_name not in data.prov_names:
        return None
    p_idx = data.prov_names.index(prov_name)
    post = idata.posterior
    alpha_g = post["alpha_g"]                      # (chain, draw)
    g_shape = post["g_shape"]                      # (chain, draw, bin)
    u_shape = post["u_shape"].isel(prov=p_idx)     # (chain, draw, bin)
    b_u = post["b_u"].isel(prov=p_idx)             # (chain, draw)
    log_prov = alpha_g + g_shape + b_u + u_shape   # broadcast over bin
    lam_prov = np.exp(log_prov)
    med = lam_prov.median(("chain", "draw")).values
    lo = lam_prov.quantile(0.025, ("chain", "draw")).values
    hi = lam_prov.quantile(0.975, ("chain", "draw")).values
    return med, lo, hi


# --------------------------------------------------------------------------- #
# Driver.
# --------------------------------------------------------------------------- #

def run(out_dir: Path, draws: int, tune: int, chains: int, target_accept: float,
        s_g: float, s_u: float, s_v: float, seed: int,
        png_path: Path, results_path: Path, escalate: bool) -> dict:
    """Fit the hierarchy, run gates + the pooling sanity check, save artefacts."""
    # --- Assemble subset ---------------------------------------------------
    data = hm.assemble(out_dir, SUBSET)
    print(f"Subset: {len(data.cities)} cities, "
          f"{len(data.prov_names)} non-singleton provinces "
          f"({data.prov_names}), "
          f"{len(data.singleton_provs)} singletons "
          f"({data.singleton_provs}).")
    print(f"Total inscriptions: {data.A_all.shape[0]}; "
          f"mean per-city N = {data.anchor_n_mean:.1f}")

    # --- Fit the hierarchy -------------------------------------------------
    print(f"\nFitting hierarchy: draws={draws} tune={tune} chains={chains} "
          f"target_accept={target_accept}; scales s_g={s_g} s_u={s_u} s_v={s_v}")
    idata = hm.fit(data, draws=draws, tune=tune, chains=chains,
                   target_accept=target_accept,
                   s_g=s_g, s_u=s_u, s_v=s_v,
                   random_seed=seed, progressbar=False)
    conv = hm.convergence_summary(idata)
    passed = hm.gates_pass(conv)
    print(f"  GATES pass={passed}: max R-hat {conv['max_rhat']:.4f}  "
          f"min ESS {conv['min_ess_bulk']:.0f}  div {conv['n_divergences']}  "
          f"(worst R-hat {conv['worst_rhat_param']}, "
          f"worst ESS {conv['worst_ess_param']})")

    if not passed and escalate:
        d2, t2 = draws * 2, tune * 2
        print(f"  GATE MISS -> escalating ONCE to tune={t2} draws={d2} "
              f"(gate NOT relaxed)")
        idata = hm.fit(data, draws=d2, tune=t2, chains=chains,
                       target_accept=target_accept,
                       s_g=s_g, s_u=s_u, s_v=s_v,
                       random_seed=seed + 1, progressbar=False)
        conv = hm.convergence_summary(idata)
        passed = hm.gates_pass(conv)
        print(f"  after escalation pass={passed}: max R-hat {conv['max_rhat']:.4f}  "
              f"min ESS {conv['min_ess_bulk']:.0f}  div {conv['n_divergences']}")

    city_index = {c: i for i, c in enumerate(data.cities)}

    # --- Pooling sanity check: hierarchical vs standalone ------------------
    print("\n" + "=" * 72)
    print("POOLING SANITY CHECK — small-N city: hierarchical vs standalone")
    print("=" * 72)
    sanity = []
    for city in SANITY_CITIES:
        if city not in city_index:
            continue
        ci = city_index[city]
        h_med, h_lo, h_hi = city_lam_quantiles(idata, ci)
        # Standalone single-city fit (same validated model.py).
        A = data.city_A[city]
        s_idata = sm.fit(A, draws=draws, tune=tune, chains=chains,
                         target_accept=target_accept,
                         random_seed=seed + 100 + ci, progressbar=False)
        s_conv = sm.convergence_summary(s_idata)
        s_med, s_lo, s_hi = standalone_lam_quantiles(s_idata)

        h_width = h_hi - h_lo
        s_width = s_hi - s_lo
        # Mean CI-width ratio (hier / standalone): < 1 means hier is tighter.
        width_ratio = float(np.mean(h_width / s_width))
        # Median-trajectory correlation between the two (shape agreement).
        shape_r = float(np.corrcoef(h_med, s_med)[0, 1])
        N = int(A.shape[0])
        print(f"  {city:>20} (N={N:>3}): mean CI-width ratio hier/standalone "
              f"= {width_ratio:.3f}  ({'TIGHTER' if width_ratio < 1 else 'WIDER'}); "
              f"shape r = {shape_r:.3f}; standalone conv "
              f"rhat {s_conv['max_rhat']:.3f} ess {s_conv['min_ess_bulk']:.0f}")
        sanity.append({
            "city": city, "N": N,
            "ci_width_ratio_hier_over_standalone": width_ratio,
            "shape_corr_hier_standalone": shape_r,
            "hier_med": h_med.tolist(), "hier_lo": h_lo.tolist(),
            "hier_hi": h_hi.tolist(),
            "standalone_med": s_med.tolist(), "standalone_lo": s_lo.tolist(),
            "standalone_hi": s_hi.tolist(),
            "standalone_conv": s_conv,
        })

    # --- Pompeii containment ----------------------------------------------
    print("\n" + "=" * 72)
    print("POMPEII CONTAINMENT — city collapse vs province mean (Regio I)")
    print("=" * 72)
    regio_i_name = data.provinces[city_index["Pompeii"]]
    pomp_med, pomp_lo, pomp_hi = city_lam_quantiles(idata, city_index["Pompeii"])
    prov_traj = province_trajectory(idata, data, regio_i_name)
    nonpomp_med, _, _ = city_lam_quantiles(idata, city_index[REGIO_I_NONPOMPEII])

    post79 = BIN_LO >= 75  # bins starting at/after AD 75 (~the AD 79 terminus)
    pomp_post = float(pomp_med[post79].sum())
    pomp_tot = float(pomp_med.sum())
    nonpomp_post = float(nonpomp_med[post79].sum())
    nonpomp_tot = float(nonpomp_med.sum())
    containment = {"province": regio_i_name}
    if prov_traj is not None:
        prov_med, prov_lo, prov_hi = prov_traj
        prov_post = float(prov_med[post79].sum())
        prov_tot = float(prov_med.sum())
        print(f"  Pompeii CITY    : post-79 mass {pomp_post:.2f} of "
              f"{pomp_tot:.2f} total  ({100*pomp_post/pomp_tot:.1f}% post-79)")
        print(f"  Regio I PROVINCE: post-79 mass {prov_post:.2f} of "
              f"{prov_tot:.2f} total  ({100*prov_post/prov_tot:.1f}% post-79)")
        print(f"  {REGIO_I_NONPOMPEII} CITY  : post-79 mass {nonpomp_post:.2f} "
              f"of {nonpomp_tot:.2f} total  "
              f"({100*nonpomp_post/nonpomp_tot:.1f}% post-79)")
        prov_collapsed = (prov_post / prov_tot) < 0.02
        print(f"  -> province post-79 fraction "
              f"{'COLLAPSED (BAD)' if prov_collapsed else 'PRESERVED (good)'}; "
              f"Pompeii city idiosyncrasy "
              f"{'CONTAINED (good)' if (pomp_post/pomp_tot) < 0.1 else 'LEAKED'}")
        containment.update({
            "pompeii_post79_frac": pomp_post / pomp_tot,
            "province_post79_frac": prov_post / prov_tot,
            "nonpompeii_post79_frac": nonpomp_post / nonpomp_tot,
            "pompeii_med": pomp_med.tolist(),
            "province_med": prov_med.tolist(),
            "province_lo": prov_lo.tolist(),
            "province_hi": prov_hi.tolist(),
            "nonpompeii_city": REGIO_I_NONPOMPEII,
            "nonpompeii_med": nonpomp_med.tolist(),
        })

    save_png(sanity, containment, png_path)

    out = {
        "subset": data.cities,
        "provinces_u_tier": data.prov_names,
        "singletons": data.singleton_provs,
        "n_inscriptions": int(data.A_all.shape[0]),
        "scales": {"s_g": s_g, "s_u": s_u, "s_v": s_v},
        "sampler": {"draws": draws, "tune": tune, "chains": chains,
                    "target_accept": target_accept},
        "convergence": conv, "gates_pass": bool(passed),
        "pooling_sanity": sanity,
        "pompeii_containment": containment,
    }
    results_path.write_text(json.dumps(out, indent=2))
    print(f"\nResults JSON -> {results_path}")
    return out


def save_png(sanity, containment, png_path):
    """Two-row PNG: (top) hier vs standalone for sanity cities; (bottom)
    Pompeii city vs Regio I province trajectory (the containment check)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    centres = (BIN_LO + BIN_HI) / 2
    n_s = max(len(sanity), 1)
    fig, axes = plt.subplots(2, n_s, figsize=(4.6 * n_s, 8), squeeze=False)

    # Row 0: hier vs standalone per sanity city.
    for ax, s in zip(axes[0], sanity):
        h_med = np.array(s["hier_med"]); h_lo = np.array(s["hier_lo"])
        h_hi = np.array(s["hier_hi"])
        st_med = np.array(s["standalone_med"]); st_lo = np.array(s["standalone_lo"])
        st_hi = np.array(s["standalone_hi"])
        ax.fill_between(centres, st_lo, st_hi, alpha=0.18, color="C3",
                        label="standalone 95% CI")
        ax.plot(centres, st_med, "--s", color="C3", ms=3, label="standalone median")
        ax.fill_between(centres, h_lo, h_hi, alpha=0.28, color="C0",
                        label="hier 95% CI")
        ax.plot(centres, h_med, "-o", color="C0", ms=3, label="hier median")
        ax.set_title(f"{s['city']} (N={s['N']})\nCI-width ratio "
                     f"{s['ci_width_ratio_hier_over_standalone']:.2f}")
        ax.set_xlabel("year")
        ax.set_ylabel("exp. insc / 25y")
        ax.legend(fontsize=6)

    # Row 1: Pompeii containment in the first cell; hide the rest.
    ax = axes[1][0]
    if "province_med" in containment:
        pomp = np.array(containment["pompeii_med"])
        prov = np.array(containment["province_med"])
        prov_lo = np.array(containment["province_lo"])
        prov_hi = np.array(containment["province_hi"])
        nonp = np.array(containment["nonpompeii_med"])
        ax.fill_between(centres, prov_lo, prov_hi, alpha=0.2, color="C2",
                        label="Regio I province 95% CI")
        ax.plot(centres, prov, "-o", color="C2", ms=3, label="Regio I province median")
        ax.plot(centres, pomp, "-^", color="C1", ms=3, label="Pompeii city median")
        ax.plot(centres, nonp, "--d", color="C4", ms=3,
                label=f"{containment['nonpompeii_city']} city median")
        ax.axvline(79, color="grey", ls=":", lw=1)
        ax.set_yscale("log")
        ax.set_title("Pompeii containment: city collapse vs province mean "
                     "(log y)")
        ax.set_xlabel("year")
        ax.set_ylabel("exp. insc / 25y (log)")
        ax.legend(fontsize=6)
    for j in range(1, n_s):
        axes[1][j].axis("off")

    fig.tight_layout()
    fig.savefig(png_path, dpi=130)
    print(f"PNG -> {png_path}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    # Defaults are the prior-predictive-PINNED scales (prior_predictive.py), so
    # an unattended run uses the pinned priors (audit B2).
    p.add_argument("--s-g", type=float, default=0.3)
    p.add_argument("--s-u", type=float, default=0.15)
    p.add_argument("--s-v", type=float, default=0.15)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--no-escalate", action="store_true")
    p.add_argument("--out-dir", type=Path,
                   default=Path(__file__).resolve().parent / "prepared")
    p.add_argument("--png", type=Path,
                   default=Path(__file__).resolve().parent / "hier-smoke-pooling.png")
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "hier-smoke-results.json")
    args = p.parse_args()
    run(args.out_dir, args.draws, args.tune, args.chains, args.target_accept,
        args.s_g, args.s_u, args.s_v, args.seed, args.png, args.results,
        escalate=not args.no_escalate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
