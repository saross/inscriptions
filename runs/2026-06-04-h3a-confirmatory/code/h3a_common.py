#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h3a_common.py --- shared data-prep helpers for the H3a confirmatory run
(runs/2026-06-04-h3a-confirmatory/).

This module productionises the talk-prep `build_city_frame` (reference:
runs/2026-05-21-talk-prep/code/05-h3a-bayesian-mundlak.py) and the
preregistration filter (reference: 01-filter-and-prep.py::load_filtered_lire).
It is imported by 01-data-prep.py, prior-predictive.py, 02-h3a-fit.py,
03-ppc.py, and 04-h3c.py so that every step reads an identical frame.

Blind-run note
--------------
Every number this module produces is derived from the raw LIRE parquet, the
preregistration filter, and the design artefact --- never from any prior
result. The talk-prep `outputs/` are not read.

Spec references
---------------
- planning/preregistration-draft.md  (§3 H3a lines 212-269; filter §3)
- planning/h3a-confirmatory-launch-spec-2026-06-04.md  (sample decisions)
- planning/h3a-design-artefact-2026-06-04.md  (model + thresholds)

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-04, on Shawn's blind-run brief.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths --- resolved relative to this module so the run is portable across
# the local repo and sapphire.
# ---------------------------------------------------------------------------
THIS = Path(__file__).resolve()
CODE_DIR = THIS.parent
RUN_DIR = CODE_DIR.parent
PROJECT_ROOT = RUN_DIR.parent.parent
RAW_LIRE = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = RUN_DIR / "data" / "province-language-map.csv"

# Canonical processed-data outputs.
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PRIMARY_PARQUET = PROCESSED_DIR / "city_level_for_h3a.parquet"
WITHZEROS_PARQUET = PROCESSED_DIR / "city_level_for_h3a_with_zeros.parquet"
LATIN_PARQUET = PROCESSED_DIR / "city_level_for_h3a_latin.parquet"

# ---------------------------------------------------------------------------
# Filter constants (prereg §3, identical to 01-filter-and-prep.py).
# ---------------------------------------------------------------------------
ENVELOPE_MIN = -50   # 50 BC inclusive
ENVELOPE_MAX = 350   # AD 350 inclusive

LIRE_VERSION = "v3.0"
DATE_WINDOW = "50 BC - AD 350 (overlap)"

# Prereg row-level sanity targets (HARD-STOP if any diverges materially).
PREREG_ROW_TARGETS = {
    "total_filtered": 180_609,
    "rome_only": 65_435,
    "rome_excluded": 115_174,
    "hanson_city_assigned_filtered": 140_575,
}


def load_filtered_lire() -> pd.DataFrame:
    """Load LIRE v3.0 and apply the preregistration filter.

    Three predicates intersected with the [50 BC, AD 350] analysis envelope
    (overlap, not containment), identical to
    01-filter-and-prep.py::load_filtered_lire and prereg §3:

      is_geotemporal := Lat & Lon & not_before & not_after present,
                        not_before <= not_after
      is_within_RE   := province present
      in_envelope    := not_after >= -50 AND not_before <= 350

    Returns
    -------
    pd.DataFrame
        Filtered LIRE corpus; expected 180,609 rows.
    """
    df = pd.read_parquet(RAW_LIRE)
    is_geotemporal = (
        df["Latitude"].notna()
        & df["Longitude"].notna()
        & df["not_before"].notna()
        & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    in_envelope = (
        (df["not_after"] >= ENVELOPE_MIN) & (df["not_before"] <= ENVELOPE_MAX)
    )
    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["not_before"] = sub["not_before"].astype(int)
    sub["not_after"] = sub["not_after"].astype(int)
    return sub


def rome_mask(df: pd.DataFrame) -> pd.Series:
    """Boolean mask: True where the inscription is located at Rome.

    Canonical Rome predicate: urban_context_city == 'roma' (case/space
    insensitive). Reference: 01-filter-and-prep.py::identify_rome.
    """
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def check_row_counts(df: pd.DataFrame) -> tuple[bool, dict, list[str]]:
    """Compare filtered row counts to the prereg targets at 1% tolerance.

    Returns (passed, observed_dict, message_lines). A HARD-STOP if not passed.
    """
    rome = rome_mask(df)
    total = int(len(df))
    rome_only = int(rome.sum())
    observed = {
        "total_filtered": total,
        "rome_only": rome_only,
        "rome_excluded": total - rome_only,
        "hanson_city_assigned_filtered": int(df["urban_context_pop_est"].notna().sum()),
    }
    passed = True
    msgs: list[str] = []
    for key, target in PREREG_ROW_TARGETS.items():
        got = observed[key]
        rel = (got - target) / target if target else float("inf")
        status = "OK" if abs(rel) <= 0.01 else "DIVERGE"
        if status == "DIVERGE":
            passed = False
        msgs.append(
            f"  [{status:7}] {key:34} target={target:>8d} observed={got:>8d} "
            f"({rel:+.4%})"
        )
    return passed, observed, msgs


def _mode_or_nan(x: pd.Series):
    m = x.mode()
    return m.iloc[0] if not m.empty else np.nan


def build_primary_frame(filtered: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Aggregate filtered LIRE to the PRIMARY city frame (Decision 35A).

    PRIMARY = Hanson-matched (urban_context_pop_est not null), Rome-excluded,
    with >= 1 date-window inscription. Adds the Mundlak components
    (province-mean log_pop, within-province deviation), province index, and a
    per-city median coordinate.

    Per-city coordinate choice (documented): the **median** Longitude and
    Latitude of the city's date-window inscriptions. The median is robust to
    the occasional mis-geocoded outlier inscription within a city's rows and,
    unlike the mean, is unaffected by a few extreme coordinates --- a
    conservative, defensible centroid for a city's epigraphic footprint. Used
    only for H3c k-NN spatial weights; does not enter the regression.

    Returns
    -------
    (cities_df, province_categories)
    """
    rome = rome_mask(filtered)
    has_hanson = filtered["urban_context_pop_est"].notna()
    sub = filtered.loc[~rome & has_hanson].copy()

    agg = (
        sub.groupby("urban_context_city")
        .agg(
            inscription_count=("urban_context_city", "size"),
            urban_context_pop_est=("urban_context_pop_est", _mode_or_nan),
            province=("province", _mode_or_nan),
            longitude=("Longitude", "median"),
            latitude=("Latitude", "median"),
        )
        .reset_index()
        .rename(columns={"urban_context_city": "city"})
    )
    # Require a province assignment (drops cities with no province mode).
    agg = agg.dropna(subset=["province"]).copy()

    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    prov_means = agg.groupby("province")["log_pop"].transform("mean")
    agg["log_pop_prov_mean"] = prov_means
    agg["log_pop_within"] = agg["log_pop"] - prov_means

    province_codes = pd.Categorical(agg["province"])
    agg["province_idx"] = province_codes.codes

    # Provenance columns.
    agg["lire_version"] = LIRE_VERSION
    agg["date_window"] = DATE_WINDOW
    agg["rome_excluded"] = True
    agg["sample"] = "primary"

    cols = [
        "city", "province", "province_idx",
        "urban_context_pop_est", "log_pop", "log_pop_prov_mean", "log_pop_within",
        "inscription_count", "longitude", "latitude",
        "lire_version", "date_window", "rome_excluded", "sample",
    ]
    agg = agg[cols].sort_values("urban_context_pop_est", ascending=False).reset_index(drop=True)
    return agg, list(province_codes.categories)


def build_with_zeros_frame(filtered: pd.DataFrame) -> pd.DataFrame:
    """Sensitivity A: primary frame PLUS Hanson cities with zero date-window
    inscriptions, entered as structural zeros.

    A Hanson 'city' is identified by (urban_context_city, urban_context_pop_est).
    The structural zeros are Hanson cities present in LIRE (with a population
    estimate) but whose inscriptions all fall outside the date window or are
    otherwise filtered out --- i.e. they appear among Hanson cities in the raw
    corpus but not among the 1,044 date-window-present cities.

    NOTE on the Mundlak components: the province-mean log_pop is recomputed
    over the *with-zeros* city set, so the centring differs slightly from the
    primary. This is the correct Mundlak centring for THIS sample.
    """
    raw = pd.read_parquet(RAW_LIRE)
    rome = raw["urban_context_city"].fillna("").str.strip().str.lower() == "roma"
    has_hanson = raw["urban_context_pop_est"].notna()
    hanson_pool = raw.loc[~rome & has_hanson].copy()

    # All Hanson cities (Rome-excluded) regardless of date window, with their
    # population, modal province, and median coordinate over ALL their rows.
    all_hanson_cities = (
        hanson_pool.groupby("urban_context_city")
        .agg(
            urban_context_pop_est=("urban_context_pop_est", _mode_or_nan),
            province=("province", _mode_or_nan),
            longitude=("Longitude", "median"),
            latitude=("Latitude", "median"),
        )
        .reset_index()
        .rename(columns={"urban_context_city": "city"})
    )
    all_hanson_cities = all_hanson_cities.dropna(subset=["province"]).copy()

    # Date-window inscription counts (the primary frame's counts).
    primary, _ = build_primary_frame(filtered)
    counts = primary.set_index("city")["inscription_count"]
    all_hanson_cities["inscription_count"] = (
        all_hanson_cities["city"].map(counts).fillna(0).astype(int)
    )

    agg = all_hanson_cities.copy()
    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    prov_means = agg.groupby("province")["log_pop"].transform("mean")
    agg["log_pop_prov_mean"] = prov_means
    agg["log_pop_within"] = agg["log_pop"] - prov_means
    province_codes = pd.Categorical(agg["province"])
    agg["province_idx"] = province_codes.codes

    agg["lire_version"] = LIRE_VERSION
    agg["date_window"] = DATE_WINDOW
    agg["rome_excluded"] = True
    agg["sample"] = "with_zeros"

    cols = [
        "city", "province", "province_idx",
        "urban_context_pop_est", "log_pop", "log_pop_prov_mean", "log_pop_within",
        "inscription_count", "longitude", "latitude",
        "lire_version", "date_window", "rome_excluded", "sample",
    ]
    return agg[cols].sort_values("urban_context_pop_est", ascending=False).reset_index(drop=True)


def build_latin_frame(filtered: pd.DataFrame) -> pd.DataFrame:
    """Sensitivity B: primary frame restricted to Latin-speaking provinces,
    using the externalised province-language map (Rome already excluded by the
    primary).

    The Mundlak components are recomputed over the Latin-only city set (correct
    centring for THIS sample). Expected ~815-817 cities.
    """
    lang_map = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    latin_provinces = set(
        lang_map.loc[lang_map["language"] == "Latin", "lire_province"]
    )

    primary, _ = build_primary_frame(filtered)
    latin = primary.loc[primary["province"].isin(latin_provinces)].copy()

    # Recompute Mundlak centring over the Latin-only sample.
    prov_means = latin.groupby("province")["log_pop"].transform("mean")
    latin["log_pop_prov_mean"] = prov_means
    latin["log_pop_within"] = latin["log_pop"] - prov_means
    province_codes = pd.Categorical(latin["province"])
    latin["province_idx"] = province_codes.codes
    latin["sample"] = "latin_only"
    return latin.reset_index(drop=True)


def standardise_predictors(cities: pd.DataFrame) -> pd.DataFrame:
    """Sensitivity C helper: return a copy with z-standardised Mundlak
    predictors (mean 0, SD 1 across cities in the given frame).

    Standardises log_pop_within and log_pop_prov_mean. The frame's province
    index and counts are unchanged. Used by 02-h3a-fit.py to re-fit with
    standardised predictors and report beta stability.
    """
    out = cities.copy()
    for col in ("log_pop_within", "log_pop_prov_mean"):
        mu = out[col].mean()
        sd = out[col].std(ddof=0)
        out[f"{col}_std"] = (out[col] - mu) / sd
    return out
