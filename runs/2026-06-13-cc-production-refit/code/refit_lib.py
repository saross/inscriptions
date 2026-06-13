#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refit_lib.py — per-unit data prep for the cc-library production refit.
======================================================================

Builds, for each production unit, the cross-classified observables the
recovery-validated `library` model consumes (spec §1/§3): the aligned- and
non-aligned-subset aoristic SPAs (largest-remainder integer counts), the aligned
count ``k``, and the total ``n_rows`` — all in **aoristic-effective counts** so the
exact lumping/thinning factorisation holds (``k == y_aligned.sum()``,
``n_rows == y_aligned.sum() + y_nonaligned.sum()``).

Reuses the recovery-validated + H2.1-production pieces verbatim: ``h2_lib`` for the
corpus loader, aoristic SPA, family classifier, unit enumeration and
largest-remainder; ``joint_lib`` for the alignment indicator (rule C) and the
slab-box builder. The convention basis is the FIXED corpus-wide slab library
locked by ``library_design.py`` (spec §2) — identical for every unit.

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-13. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402

ALIGN_RULE = "C"
THETA_KAPPA = 40.0
REFIT_BASE_SEED = 20260613   # production-refit seed; per-unit seed = base + unit_index
LIBRARY_JSON = REFIT / "outputs" / "production-slab-library.json"
THETA_CALIB_JSON = JOINT.parent / "outputs" / "theta-calibration.json"


def enumerate_refit_units() -> list[dict[str, Any]]:
    """The 28 ``h2_lib`` units + the 'Italia (excl. Rome)' aggregate (provinces
    whose name carries '/ Regio'), reproducing the H2.1 finalised 29-unit set
    (``refit-all-units.py``). Unit indices are re-assigned 0..28 (sequential) so
    per-unit seeds are collision-free for this run."""
    units = H.enumerate_units()  # 28
    df_provs = _italian_provinces()
    units = units + [{
        "name": "Italia (excl. Rome)", "kind": "aggregate", "frame": "latin",
        "tier": "aggregate-added", "filter": ("province_in", df_provs),
    }]
    for i, u in enumerate(units):
        u["unit_index"] = i
    return units


def _italian_provinces() -> list[str]:
    """Provinces composing Italia (excl. Rome): names carrying '/ Regio'
    (verbatim rule from refit-all-units.py)."""
    df = H.load_filtered_lire()
    return sorted(p for p in df["province"].unique() if "Regio" in str(p))


def subset_for(df: pd.DataFrame, unit: dict[str, Any], latin: set[str]) -> pd.DataFrame:
    """Subset the filtered corpus to one unit, handling the Italia 'province_in'
    filter in addition to h2_lib's native filters."""
    if unit["filter"][0] == "province_in":
        return df.loc[df["province"].isin(unit["filter"][1])]
    return H.subset_corpus(df, unit, latin)


def load_library_basis() -> tuple[np.ndarray, list[list[int]]]:
    """The locked FIXED slab library as a (n_slabs, N_BINS) basis (each row the
    deterministic aoristic box of one slab; reuses the validated slab builder)."""
    lib = json.loads(LIBRARY_JSON.read_text(encoding="utf-8"))
    slabs = [tuple(s) for s in lib["library_slabs"]]
    basis = np.vstack([J.slab_mixture_spa([s]) for s in slabs])
    assert basis.shape[1] == H.N_BINS, "library basis bin mismatch"
    return basis, lib["library_slabs"]


def theta_priors() -> tuple[tuple[float, float], tuple[float, float], dict]:
    """(theta_conv_ab, theta_gen_ab, calib_rule_C) — rule C, κ=40 (spec §3)."""
    cal = json.loads(THETA_CALIB_JSON.read_text(encoding="utf-8"))["calibration"][ALIGN_RULE]
    tc = J.beta_from_mean_concentration(cal["theta_conv"], THETA_KAPPA)
    tg = J.beta_from_mean_concentration(cal["theta_gen"], THETA_KAPPA)
    return tc, tg, cal


def build_unit_cc_data(df_unit: pd.DataFrame) -> dict[str, Any]:
    """Aligned/non-aligned subset SPAs + k + n_rows for one unit (spec §1).

    Aoristic-effective counts: each subset's aoristic SPA is largest-remainder-
    rounded to integers; ``k = y_aligned.sum()``; ``n_rows = k + y_nonaligned.sum()``.
    Returns also descriptive row/mass aligned fractions for the record.
    """
    amask = J.aligned_indicator(df_unit, rule=ALIGN_RULE)
    al = df_unit.loc[amask]
    non = df_unit.loc[~amask]
    y_aligned = H.largest_remainder(H.aoristic_spa(al["nb"].to_numpy(), al["na"].to_numpy()))
    y_nonaligned = H.largest_remainder(
        H.aoristic_spa(non["nb"].to_numpy(), non["na"].to_numpy()))
    k = int(y_aligned.sum())
    n_rows = int(k + int(y_nonaligned.sum()))
    n_rows_raw = int(len(df_unit))
    n_aligned_raw = int(amask.sum())
    total_mass = float(H.aoristic_spa(df_unit["nb"].to_numpy(), df_unit["na"].to_numpy()).sum())
    aligned_mass = float(H.aoristic_spa(al["nb"].to_numpy(), al["na"].to_numpy()).sum())
    return {
        "y_aligned": y_aligned,
        "y_nonaligned": y_nonaligned,
        "k": k,
        "n_rows": n_rows,
        "n_rows_raw": n_rows_raw,
        "n_aligned_raw": n_aligned_raw,
        "row_aligned_frac": (n_aligned_raw / n_rows_raw) if n_rows_raw else float("nan"),
        "mass_aligned_frac": (aligned_mass / total_mass) if total_mass > 0 else float("nan"),
    }
