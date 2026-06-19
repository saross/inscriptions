#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
city_lib.py — per-city unit enumeration + corpus subsetting for D13 Stage 1.
============================================================================

Stage 1 of the D13 "α-as-translator" sensitivity (spec
``runs/2026-06-19-d13-alpha-as-translator/spec.md`` §3) fits the production
cross-classified ``library`` deconvolution **standalone per city** to obtain a
per-city posterior mixture fraction α_c. This module supplies the two pieces the
Stage-1 driver (``run_city_alpha.py``) needs on top of the verbatim-reused
production refit machinery (``refit_lib`` / ``h2_lib`` / ``joint_lib``):

1. ``enumerate_city_units()`` — the **163 Latin-frame cities with
   ``inscription_count`` ≥ 100** (``data/processed/city_level_for_h3a_latin.parquet``)
   as units of the form::

       {"name": city, "kind": "city", "frame": "latin",
        "filter": ("urban_context_city", city), "unit_index": i,
        "h3a_count": int, "reliable": bool}     # reliable iff N ≥ 500

   Unit indices are assigned 0..162 in descending ``inscription_count`` order so
   the per-city seed (base + unit_index) is collision-free and deterministic.

2. ``subset_for_city(df, unit)`` — the ``("urban_context_city", name)`` corpus
   subset. This is the plain city filter ``df.loc[df["urban_context_city"] ==
   name]``. The reconciliation gate (``run_city_alpha.reconcile_city``; spec §3,
   the REQUIRED pre-fit gate) verifies this plain filter's row count equals the
   H3a ``inscription_count`` for the city — established to hold **exactly** for all
   163 cities (none of them carry rows lacking a Hanson population estimate, and
   none is Rome), so the mixture is fit on the identical inscriptions H3a counted.

Design principle — REUSE, do not re-derive. The model, the aoristic SPA, the
family classifier, the alignment indicator, the largest-remainder observation
model, the slab library, and the adopted θ priors are all imported verbatim from
the production refit (``refit_lib``) and its dependencies (``h2_lib``,
``joint_lib``). This module adds ONLY the city enumeration and the plain
city-filter subset.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-19.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
H2 = PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
JOINT = PROJECT_ROOT / "runs" / "2026-06-09-joint-identifiability" / "code"
REFIT = PROJECT_ROOT / "runs" / "2026-06-13-cc-production-refit" / "code"
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
sys.path.insert(0, str(REFIT))

# Canonical Latin city frame (the same parquet H3a Sensitivity B / the lodged
# primary Latin frame is built from). N (= the H3a count) is its
# ``inscription_count`` column.
LATIN_PARQUET = PROJECT_ROOT / "data" / "processed" / "city_level_for_h3a_latin.parquet"

# Inclusion threshold (spec §3) and reachability floor (spec §2 / Decision 34).
N_MIN = 100        # the prereg-literal city set: 163 Latin cities at N ≥ 100
N_RELIABLE = 500   # standalone-α reachability floor; reliable iff H3a count ≥ 500


def enumerate_city_units() -> list[dict[str, Any]]:
    """The 163 Latin-frame cities with ``inscription_count`` ≥ N_MIN as units.

    Ordered by descending ``inscription_count`` (deterministic; ties broken by
    city name), so ``unit_index`` 0..162 is stable across runs and the per-city
    seed (D13_BASE_SEED + unit_index) is collision-free.

    Each unit carries the city's H3a ``inscription_count`` (``h3a_count``) and a
    ``reliable`` flag (True iff N ≥ N_RELIABLE) so the driver can record the
    reachability annotation without re-reading the parquet.

    Returns
    -------
    list[dict]
        ``{"name", "kind"="city", "frame"="latin",
          "filter"=("urban_context_city", name), "unit_index", "h3a_count",
          "reliable"}``.
    """
    frame = pd.read_parquet(LATIN_PARQUET)
    sub = frame.loc[frame["inscription_count"] >= N_MIN].copy()
    # Deterministic order: count desc, then city name asc (stable tie-break).
    sub = sub.sort_values(
        ["inscription_count", "city"], ascending=[False, True]
    ).reset_index(drop=True)

    units: list[dict[str, Any]] = []
    for i, row in sub.iterrows():
        name = str(row["city"])
        n = int(row["inscription_count"])
        units.append({
            "name": name,
            "kind": "city",
            "frame": "latin",
            "filter": ("urban_context_city", name),
            "unit_index": int(i),
            "h3a_count": n,
            "reliable": bool(n >= N_RELIABLE),
        })
    return units


def subset_for_city(df: pd.DataFrame, unit: dict[str, Any]) -> pd.DataFrame:
    """Subset the filtered corpus to one city by its ``urban_context_city``.

    The plain city filter ``df.loc[df["urban_context_city"] == name]`` — verified
    (reconciliation gate, spec §3) to equal the H3a ``inscription_count`` row set
    for every one of the 163 cities. Mirrors ``h2_lib.subset_corpus``'s city
    branch and ``refit_lib.subset_for``'s fall-through, but explicit here so the
    D13 driver never depends on the unit-set-driven ``h2_lib`` enumeration.

    Parameters
    ----------
    df : pd.DataFrame
        The filtered LIRE corpus (``h2_lib.load_filtered_lire``).
    unit : dict
        A unit from ``enumerate_city_units`` (uses ``unit["filter"]``).

    Returns
    -------
    pd.DataFrame
        The city's rows (with the ``nb`` / ``na`` / ``date_range`` columns the
        downstream aoristic SPA and alignment indicator consume).
    """
    field, name = unit["filter"]
    if field != "urban_context_city":
        raise ValueError(
            f"city_lib.subset_for_city expects an ('urban_context_city', name) "
            f"filter; got {unit['filter']!r}"
        )
    return df.loc[df[field] == name]
