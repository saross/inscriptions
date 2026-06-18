#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h7_latin_perperiod_h3c.py — §5 H7 (Latin-frame variant).
=========================================================

Latin-frame variant of the all-provinces §5 H7 time-resolved per-period H3c
(``runs/2026-06-17-s5-h7-perperiod-h3c/code/h7_perperiod_h3c.py``). This is a
**frame swap of a signed-off analysis**, not new methodology: every modelling
choice — the 8 × 50-year period grid, the aoristic apportionment, the H3a
non-centred Mundlak negative-binomial regression (NBR), the H3c diagnostics
(Moran's I spatial clustering, provincial-capital residual contrast), the priors,
the sampler settings, and the convergence gates — is inherited **verbatim** by
importing the all-provinces module. The ONLY change is restricting the city /
province universe to the **Latin-speaking-provinces-minus-Roma** diagnostic unit
(Obs 41, Obs 101; OSF Amendment 02 lodged 2026-06-06, which makes the Latin frame
the primary cross-sectional frame — NOT amendment-gated).

Latin frame (matches the H3a confirmatory precedent EXACTLY)
------------------------------------------------------------
The universe is ``data/processed/city_level_for_h3a_latin.parquet`` — the
canonical Sensitivity-B Latin frame produced by
``runs/2026-06-04-h3a-confirmatory/code/h3a_common.build_latin_frame``:

  * **817 cities / 39 Latin provinces** (verified against the H3a precedent
    sidecar ``runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json``);
  * **Roma excluded** — Roma is dropped at the primary-frame stage (the
    ``rome_mask`` predicate ``urban_context_city == 'roma'``), so the Latin frame
    is already "Latin-minus-Roma", matching the diagnostic unit;
  * **Mundlak within / between predictors recomputed over the Latin-only set**
    (correct sample-relative centring), with ``province_idx`` re-indexed 0..38.

The per-period aoristic counts are computed over the full Hanson corpus (via the
inherited ``aoristic_period_counts``) and then **mapped onto the Latin city set**;
cities absent from the Latin frame simply do not appear in ``base["city"]`` and
are dropped — exactly the mechanism the all-provinces driver uses for its 1044
universe. Coordinates, the fixed city universe, and the capital set are likewise
restricted to the Latin frame.

Cumulative comparator
---------------------
The relevant cumulative scaling exponent for this NBR-based analysis is the
**Latin NBR β_within = 0.733 [0.648, 0.820]** (re-verified from
``runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc`` on 2026-06-18), NOT
the simpler OLS log-log slope (0.505) in ``sr1-latin-results.json``.

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-18-h7-latin/code/h7_latin_perperiod_h3c.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-18, on Shawn's pre-authorised follow-up
brief (background agent). Cross-refs: Obs 99 (H7 all-provinces), Obs 101
(diagnostic-unit framing), Amendment 02 (Latin primary).
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
# Import the audited all-provinces H7 module and reuse every function verbatim.
ALLPROV_CODE = REPO / "runs/2026-06-17-s5-h7-perperiod-h3c/code"
sys.path.insert(0, str(ALLPROV_CODE))
import h7_perperiod_h3c as H7  # noqa: E402

# Latin universe (canonical Sensitivity-B frame; build_latin_frame output).
LATIN_PARQUET = REPO / "data/processed/city_level_for_h3a_latin.parquet"
CAPITALS_CSV = REPO / "data/processed/provincial-capitals.csv"
OUT_DIR = RUN_DIR / "outputs"

# Expected Latin-frame counts (H3a precedent sample-counts.json).
EXPECTED_N_CITIES = 817
EXPECTED_N_PROVINCES = 39
# Cumulative Latin NBR comparator (idata-latin.nc, re-verified 2026-06-18).
BETA_CUMULATIVE_LATIN = {"median": 0.733, "ci": [0.648, 0.820]}


def main() -> None:
    """Drive the 8-period Latin-frame H7, mirroring the all-provinces driver.

    Identical to ``H7.main`` except the base frame is the Latin parquet (not the
    1044-city primary parquet). The count source, NBR, residuals, Moran's I, and
    capital contrast are the inherited all-provinces functions.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- Latin universe + count-verification gate -------------------------- #
    base = pd.read_parquet(LATIN_PARQUET)
    n_cities = len(base)
    n_prov = int(base["province_idx"].max()) + 1
    if n_cities != EXPECTED_N_CITIES or n_prov != EXPECTED_N_PROVINCES:
        raise SystemExit(
            f"HARD-STOP: Latin frame is {n_cities} cities / {n_prov} provinces, "
            f"expected {EXPECTED_N_CITIES} / {EXPECTED_N_PROVINCES} (H3a precedent). "
            "Frame definition ambiguous — STOP and report rather than guess."
        )
    if base["city"].str.lower().eq("roma").any():
        raise SystemExit("HARD-STOP: Roma present in the Latin frame; the "
                         "diagnostic unit is Latin-minus-Roma. STOP and report.")

    coords = base[["longitude", "latitude"]].to_numpy(dtype=float)
    capital_set = set(pd.read_csv(CAPITALS_CSV)["city"])
    n_caps_in_frame = int(base["city"].isin(capital_set).sum())
    # Aoristic per-city period mass over the full corpus (inherited); mapping
    # onto the Latin frame restricts to Latin cities exactly as for 1044.
    counts = H7.aoristic_period_counts()
    pooled_total = int(base["inscription_count"].sum())

    print(f"H7-Latin: {H7.N_PERIODS} periods, {n_cities} Latin cities, "
          f"{n_prov} Latin provinces; pooled cumulative count {pooled_total}; "
          f"capitals in frame {n_caps_in_frame} (of {len(capital_set)} total).")
    print(f"Cumulative Latin NBR comparator beta_within = "
          f"{BETA_CUMULATIVE_LATIN['median']} {BETA_CUMULATIVE_LATIN['ci']}.")

    per_city_resid = base[["city", "province", "longitude", "latitude"]].copy()
    results: dict = {}
    for label in H7.PERIOD_LABELS:
        frame = base.copy()
        period_mass = frame["city"].map(counts[label]).fillna(0.0)
        frame["inscription_count"] = np.rint(period_mass).astype(int)
        n_nonzero = int((frame["inscription_count"] > 0).sum())
        tot = int(frame["inscription_count"].sum())
        print(f"\n[{label}] non-zero Latin cities={n_nonzero} total={tot} "
              "— fitting NBR ...")

        idata = H7.fit_period(frame, n_prov)
        conv = H7.convergence(idata)
        ok = H7.gates_pass(conv)
        if not ok:
            print(f"  !! WARNING [{label}] convergence gates not met: "
                  f"R-hat={conv['max_rhat']:.4f} ESS={conv['min_ess_bulk']:.0f} "
                  f"div={conv['n_divergences']} — period read is provisional.")
        else:
            print(f"  converged: R-hat={conv['max_rhat']:.4f} "
                  f"ESS={conv['min_ess_bulk']:.0f} div={conv['n_divergences']}")

        y = frame["inscription_count"].to_numpy(float)
        r_all = H7.pearson_resids_all_draws(idata, y)
        per_city_resid[f"resid_{label}"] = r_all.mean(axis=0)

        beta = idata.posterior["beta_within"].values.reshape(-1)
        moran = H7.moran_diagnostics(r_all, coords)
        cap = H7.capital_contrast(r_all, frame, capital_set)
        k8 = moran["per_k"][str(H7.PRIMARY_K)]
        print(f"  beta_within={np.median(beta):+.3f} | capital P(>0)="
              f"{cap.get('p_contrast_gt_0', float('nan')):.3f} | "
              f"Moran k8 I={k8['moran_I']:+.4f} p={k8['p_sim_one_sided']:.4f}")

        results[label] = {
            "n_nonzero_cities": n_nonzero, "total_count": tot,
            "convergence": conv, "gates_pass": ok,
            "beta_within_median": float(np.median(beta)),
            "beta_within_ci": [float(np.percentile(beta, 2.5)),
                               float(np.percentile(beta, 97.5))],
            "capital_contrast": cap, "moran": moran,
        }
        idata.to_netcdf(str(OUT_DIR / f"h7-latin-idata-{label.replace('..', '_')}.nc"))

    per_city_resid.to_parquet(OUT_DIR / "h7-latin-per-city-residuals.parquet")
    summary = {
        "frame": f"latin ({n_cities} cities / {n_prov} provinces; Roma excluded)",
        "frame_provenance": (
            "data/processed/city_level_for_h3a_latin.parquet "
            "(h3a_common.build_latin_frame; Sensitivity B; matches "
            "runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json)"
        ),
        "n_capitals_in_frame": n_caps_in_frame,
        "beta_cumulative_latin_reference": BETA_CUMULATIVE_LATIN,
        "n_periods": H7.N_PERIODS, "period_edges": H7.PERIOD_EDGES.tolist(),
        "period_labels": H7.PERIOD_LABELS, "n_cities": n_cities,
        "sampler": {"tune": H7.N_TUNE, "draws": H7.N_DRAW, "chains": H7.N_CHAINS,
                    "target_accept": H7.TARGET_ACCEPT, "seed": H7.SEED},
        "design": {"resolution": "50y (8 periods)",
                   "count_construction": "aoristic-apportioned, rounded to int",
                   "city_universe": f"fixed {n_cities} Latin; Mundlak "
                                    "population-based, recomputed over Latin set"},
        "per_period": results,
        "note": ("Exploratory Latin-frame time-resolved H3c (frame swap of the "
                 "signed-off all-provinces H7; prereg §5 line 384); no thresholds. "
                 "Cross-refs: Obs 99, Obs 101, Amendment 02."),
    }
    with open(OUT_DIR / "h7-latin-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=H7._json_default)
    _plots(results)
    print("\nH7-Latin done. Summary at outputs/h7-latin-summary.json")


def _plots(results: dict) -> None:
    """Latin-frame copy of ``H7.plots`` (retitled; same three panels)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = list(results.keys())
    centres = [(H7.PERIOD_EDGES[i] + H7.PERIOD_EDGES[i + 1]) / 2
               for i in range(len(labels))]
    beta = [results[l]["beta_within_median"] for l in labels]
    beta_lo = [results[l]["beta_within_ci"][0] for l in labels]
    beta_hi = [results[l]["beta_within_ci"][1] for l in labels]
    cap_p = [results[l]["capital_contrast"].get("p_contrast_gt_0", np.nan)
             for l in labels]
    moran_I = [results[l]["moran"]["per_k"]["8"]["moran_I"] for l in labels]
    moran_p = [results[l]["moran"]["per_k"]["8"]["p_sim_one_sided"] for l in labels]

    fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
    axes[0].errorbar(centres, beta,
                     yerr=[np.array(beta) - np.array(beta_lo),
                           np.array(beta_hi) - np.array(beta)],
                     marker="o", capsize=3)
    axes[0].axhline(BETA_CUMULATIVE_LATIN["median"], ls="--", color="grey",
                    label=f"Latin cumulative {BETA_CUMULATIVE_LATIN['median']}")
    axes[0].set_title("beta_within over time (Latin)")
    axes[0].set_xlabel("year"); axes[0].set_ylabel("beta_within"); axes[0].legend()
    axes[1].plot(centres, cap_p, marker="o", color="C1")
    axes[1].axhline(0.95, ls="--", color="grey", label="0.95")
    axes[1].set_title("Capital over-production P(contrast>0) (Latin)")
    axes[1].set_xlabel("year"); axes[1].set_ylabel("P(>0)"); axes[1].legend()
    axes[2].plot(centres, moran_I, marker="o", color="C2", label="Moran I (k8)")
    for xi, p in zip(centres, moran_p):
        axes[2].annotate(f"p={p:.2f}", (xi, 0), fontsize=7, rotation=90)
    axes[2].axhline(0, color="k", lw=0.6)
    axes[2].set_title("Spatial clustering Moran's I (k=8) (Latin)")
    axes[2].set_xlabel("year"); axes[2].set_ylabel("Moran's I")
    fig.suptitle("H7-Latin — time-resolved H3c (50y periods, Latin frame)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "h7-latin-time-resolved.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
