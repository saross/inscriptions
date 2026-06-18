#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
peak_scaling_latin.py — §5 peak-vs-cumulative scaling (Latin-frame variant).
============================================================================

Latin-frame variant of the all-provinces §5 peak-scaling run
(``runs/2026-06-17-s5-peak-scaling/code/peak_scaling.py``). A **frame swap of a
signed-off analysis**, not new methodology: the per-city peak-count construction
(aoristic max over fixed-width bins), the H3a non-centred Mundlak negative-
binomial regression (NBR), the priors, the sampler, and the convergence gates are
inherited **verbatim** by importing the all-provinces module. The ONLY change is
restricting the city / province universe to the **Latin-speaking-provinces-minus-
Roma** diagnostic unit (Obs 41, Obs 101; OSF Amendment 02 lodged 2026-06-06).

Scope of the frame swap
-----------------------
The all-provinces run had three arms: Arm A (raw aoristic peak, full 1044-city
frame; the headline) and Arm B + overlap (268 "§5" cities from the Layer-A
trajectory ``city-index.parquet``). **Only Arm A is a frame swap of the Latin
universe.** The 268-city §5 arms are an orthogonal subset — the Layer-A modelled-
trajectory target set, used in the all-provinces run as a range-restriction probe
(its low β = 0.22 was diagnosed as range restriction, NOT a real flattening; Obs
100). That subset is not part of the Latin-frame definition, so this variant runs
the **full-frame raw-peak arms restricted to the Latin frame** (50y headline +
25y window sensitivity) and compares them against the **Latin cumulative NBR
β_within = 0.733**. The §5-subset arms are intentionally out of scope here.

Latin frame (matches the H3a confirmatory precedent EXACTLY)
------------------------------------------------------------
Universe = ``data/processed/city_level_for_h3a_latin.parquet`` — the canonical
Sensitivity-B Latin frame from
``runs/2026-06-04-h3a-confirmatory/code/h3a_common.build_latin_frame``:
**817 cities / 39 Latin provinces, Roma excluded, Mundlak recomputed over the
Latin set** (verified against the H3a precedent ``sample-counts.json``). Peak
counts are computed over the full corpus (inherited ``aoristic_peak_counts``) and
mapped onto the Latin frame; non-Latin cities are dropped by the join.

Cumulative comparator
---------------------
**Latin NBR β_within = 0.733 [0.648, 0.820]** (re-verified from
``runs/2026-06-04-h3a-confirmatory/outputs/idata-latin.nc`` on 2026-06-18) — the
NBR-based cumulative scaling exponent, NOT the OLS log-log slope (0.505).

Run (on sapphire)::

    cd ~/Code/inscriptions
    .venv/bin/python runs/2026-06-18-peak-scaling-latin/code/peak_scaling_latin.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-18, on Shawn's pre-authorised follow-up
brief (background agent). Cross-refs: Obs 100 (peak-scaling all-provinces), Obs
101 (diagnostic-unit framing), Amendment 02 (Latin primary).
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
# Import the audited all-provinces peak-scaling module; reuse its functions.
ALLPROV_CODE = REPO / "runs/2026-06-17-s5-peak-scaling/code"
sys.path.insert(0, str(ALLPROV_CODE))
import peak_scaling as PS  # noqa: E402

LATIN_PARQUET = REPO / "data/processed/city_level_for_h3a_latin.parquet"
OUT_DIR = RUN_DIR / "outputs"

EXPECTED_N_CITIES = 817
EXPECTED_N_PROVINCES = 39
# Latin cumulative NBR comparator (idata-latin.nc, re-verified 2026-06-18).
BETA_CUMULATIVE_LATIN = {"median": 0.733, "ci": [0.648, 0.820]}


def frame_latin(peak: pd.Series) -> tuple[pd.DataFrame, int]:
    """Latin frame with ``inscription_count`` replaced by the peak count.

    Direct analogue of ``PS.frame_1044`` but on the Latin parquet. The Mundlak
    within / between predictors and ``province_idx`` are already recomputed over
    the Latin-only set in the parquet (build_latin_frame), so the centring is
    Latin-sample-relative and correct for this frame.

    Parameters
    ----------
    peak:
        Per-city peak inscription count (index = city), from
        ``PS.aoristic_peak_counts``.

    Returns
    -------
    (frame, n_provinces)
    """
    base = pd.read_parquet(LATIN_PARQUET).copy()
    base["inscription_count"] = (
        base["city"].map(peak).fillna(0).round().astype(int)
    )
    return base, int(base["province_idx"].max()) + 1


def main() -> None:
    """Run the two full-frame raw-peak arms on the Latin universe.

    Mirrors ``PS.main`` for Arm A only (50y headline + 25y sensitivity), with the
    base frame swapped to the Latin parquet. Peak builders, NBR, and gates are the
    inherited all-provinces functions.
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- count-verification gate against the H3a precedent ----------------- #
    chk = pd.read_parquet(LATIN_PARQUET)
    n_cities = len(chk)
    n_prov = int(chk["province_idx"].max()) + 1
    if n_cities != EXPECTED_N_CITIES or n_prov != EXPECTED_N_PROVINCES:
        raise SystemExit(
            f"HARD-STOP: Latin frame is {n_cities} cities / {n_prov} provinces, "
            f"expected {EXPECTED_N_CITIES} / {EXPECTED_N_PROVINCES}. STOP and report."
        )
    if chk["city"].str.lower().eq("roma").any():
        raise SystemExit("HARD-STOP: Roma present in the Latin frame. STOP and report.")

    print(f"peak-scaling-Latin: {n_cities} Latin cities / {n_prov} provinces "
          f"(Roma excluded). Cumulative Latin NBR comparator beta_within = "
          f"{BETA_CUMULATIVE_LATIN['median']} {BETA_CUMULATIVE_LATIN['ci']}.")
    print("Building peak counts (full corpus; mapped onto Latin frame) ...")
    raw50 = PS.aoristic_peak_counts(50)
    raw25 = PS.aoristic_peak_counts(25)

    arms: dict = {}
    f, np_ = frame_latin(raw50)
    arms["raw_peak_50y_latin"] = PS.fit_beta(f, np_, "raw_peak_50y_latin")
    f, np_ = frame_latin(raw25)
    arms["raw_peak_25y_latin"] = PS.fit_beta(f, np_, "raw_peak_25y_latin")

    summary = {
        "frame": f"latin ({n_cities} cities / {n_prov} provinces; Roma excluded)",
        "frame_provenance": (
            "data/processed/city_level_for_h3a_latin.parquet "
            "(h3a_common.build_latin_frame; Sensitivity B; matches "
            "runs/2026-06-04-h3a-confirmatory/outputs/sample-counts.json)"
        ),
        "scope_note": (
            "Frame swap of Arm A (full-frame raw peak) only. The 268-city §5 "
            "arms (Layer-A trajectory subset, a range-restriction probe in the "
            "all-provinces run) are orthogonal to the Latin-frame definition and "
            "intentionally out of scope here."
        ),
        "beta_cumulative_latin_reference": BETA_CUMULATIVE_LATIN,
        "sampler": {"tune": PS.N_TUNE, "draws": PS.N_DRAW, "chains": PS.N_CHAINS,
                    "target_accept": PS.TARGET_ACCEPT, "seed": PS.SEED},
        "arms": arms,
        "contrasts": {
            "headline_peak50_vs_cumulative_latin": {
                "beta_peak_raw_50y_latin": arms["raw_peak_50y_latin"]["beta_within_median"],
                "beta_cumulative_latin": BETA_CUMULATIVE_LATIN["median"],
            },
        },
        "note": ("Exploratory / tertiary Latin-frame peak-scaling (frame swap of "
                 "the signed-off all-provinces peak-scaling; not preregistered). "
                 "Cross-refs: Obs 100, Obs 101, Amendment 02."),
    }
    with open(OUT_DIR / "peak-scaling-latin-summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=PS._json_default)
    _plot(arms)
    print("\nDone. Summary at outputs/peak-scaling-latin-summary.json")


def _plot(arms: dict) -> None:
    """Forest plot: Latin cumulative reference vs the two Latin peak arms."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = [("cumulative (H3a Latin)", BETA_CUMULATIVE_LATIN["median"],
             BETA_CUMULATIVE_LATIN["ci"][0], BETA_CUMULATIVE_LATIN["ci"][1])]
    for k in ["raw_peak_50y_latin", "raw_peak_25y_latin"]:
        a = arms[k]
        rows.append((k, a["beta_within_median"], *a["beta_within_ci"]))
    labels = [r[0] for r in rows]
    y = np.arange(len(rows))[::-1]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for yi, (_, m, lo, hi) in zip(y, rows):
        ax.plot([lo, hi], [yi, yi], color="C0")
        ax.plot(m, yi, "o", color="C0")
    ax.axvline(BETA_CUMULATIVE_LATIN["median"], ls="--", color="grey",
               label=f"Latin cumulative {BETA_CUMULATIVE_LATIN['median']}")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("beta_within")
    ax.set_title("Peak vs cumulative scaling exponent (Latin frame)")
    ax.legend(); fig.tight_layout()
    fig.savefig(OUT_DIR / "peak-scaling-latin-forest.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
