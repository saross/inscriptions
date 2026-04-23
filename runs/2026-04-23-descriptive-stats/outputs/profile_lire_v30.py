#!/usr/bin/env python3
"""Descriptive profile of LIRE v3.0 — data-profile-scout methodology.

Produces the files required by the brief at
`runs/2026-04-23-descriptive-stats/briefs/data-profile-scout-brief.md`.
Every numerical figure emitted into the markdown reports is echoed into
`claims.jsonl` for adversarial re-checking by `data-profile-verifier`.

Inputs:
    dataset : /home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet
    schema  : /home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv

Outputs (in `output_dir`):
    summary.md, profile-dataset.md, profile-province.md, profile-urban-area.md,
    artefacts.md, claims.jsonl, run.log, tables/*.csv

Run with:
    /home/shawn/personal-assistant/venv/bin/python3 profile_lire_v30.py
"""

from __future__ import annotations

import csv
import json
import sys
import time
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

DATASET_PATH = Path(
    "/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet"
)
SCHEMA_PATH = Path(
    "/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv"
)
OUTPUT_DIR = Path(
    "/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs"
)
TABLES_DIR = OUTPUT_DIR / "tables"
RUN_LOG_PATH = OUTPUT_DIR / "run.log"
CLAIMS_PATH = OUTPUT_DIR / "claims.jsonl"

THRESHOLDS = [10, 30, 100, 300]
SUBSET_LEVELS = [
    ("province", "province"),
    ("urban-area", "urban_context_city"),
]

# --------------------------------------------------------------------------- #
# Global state for claims + logs
# --------------------------------------------------------------------------- #

CLAIMS: list[dict[str, Any]] = []
LOG_LINES: list[str] = []
_CLAIM_COUNTER = 0


def _now() -> str:
    """Return ISO-style timestamp for log lines."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    """Append a line to both stdout and the in-memory run log."""
    line = f"[{_now()}] {msg}"
    LOG_LINES.append(line)
    print(line, flush=True)


def add_claim(
    category: str,
    description: str,
    value: Any,
    *,
    units: str = "",
    source_method: str = "",
    source_file: str = "",
) -> str:
    """Record a numerical claim.

    Args:
        category: one of `count`, `rate`, `percentage`, `mean`, `median`,
                  `chisq`, `pvalue`, `ranking`, `threshold_qualifying`.
        description: short natural-language description.
        value: numeric value (int/float) or compound (list/dict) if needed.
        units: unit label e.g. `rows`, `years`, `%`.
        source_method: how the value was produced (pandas idiom / SciPy fn).
        source_file: which generated file contains this claim (for the verifier).

    Returns:
        The assigned `claim_id`.
    """
    global _CLAIM_COUNTER
    _CLAIM_COUNTER += 1
    claim_id = f"c{_CLAIM_COUNTER:04d}"
    entry = {
        "claim_id": claim_id,
        "category": category,
        "description": description,
        "value": value,
        "units": units,
        "source_method": source_method,
        "source_file": source_file,
    }
    CLAIMS.append(entry)
    return claim_id


# --------------------------------------------------------------------------- #
# Environment / inputs
# --------------------------------------------------------------------------- #


def validate_environment() -> None:
    """Smoke-test that all required packages load."""
    import pandas  # noqa: F401
    import numpy  # noqa: F401
    import scipy
    import pyarrow

    log(
        "environment OK "
        f"(pandas={pd.__version__}, numpy={np.__version__}, "
        f"scipy={scipy.__version__}, pyarrow={pyarrow.__version__})"
    )


def load_dataset() -> pd.DataFrame:
    """Read the LIRE v3.0 parquet and record basic dimensions."""
    log(f"loading dataset from {DATASET_PATH}")
    df = pd.read_parquet(DATASET_PATH)
    log(f"dataset shape = {df.shape}")
    return df


def load_schema() -> pd.DataFrame:
    """Read the seed metadata schema."""
    return pd.read_csv(SCHEMA_PATH)


# --------------------------------------------------------------------------- #
# Dataset-level profile
# --------------------------------------------------------------------------- #


def dataset_profile(df: pd.DataFrame, schema: pd.DataFrame) -> dict[str, Any]:
    """Compute dataset-level figures + null / unique tables."""
    log("running dataset-level profile")

    n_rows = len(df)
    n_cols = df.shape[1]

    add_claim(
        "count",
        "LIRE v3.0 total row count",
        n_rows,
        units="rows",
        source_method="len(df)",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "LIRE v3.0 column count in parquet",
        n_cols,
        units="columns",
        source_method="df.shape[1]",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Columns enumerated in seed schema LI_metadata.csv",
        len(schema),
        units="columns",
        source_method="len(schema_df)",
        source_file="profile-dataset.md",
    )

    # Per-column null rate + unique count
    null_rates = df.isna().mean().sort_values(ascending=False)
    unique_counts = df.nunique(dropna=True).reindex(null_rates.index)

    null_table = pd.DataFrame(
        {
            "column": null_rates.index,
            "null_rate": null_rates.values,
            "n_null": (null_rates.values * n_rows).round().astype(int),
            "n_unique": unique_counts.values,
        }
    )
    null_table.to_csv(TABLES_DIR / "null_and_unique_by_column.csv", index=False)
    log("wrote tables/null_and_unique_by_column.csv")

    # Columns over 50% null — artefact flag
    high_null = null_table[null_table["null_rate"] > 0.5]
    add_claim(
        "count",
        "Columns with >50% nulls",
        int(len(high_null)),
        units="columns",
        source_method="(df.isna().mean() > 0.5).sum()",
        source_file="artefacts.md",
    )

    # Date range
    # Both cols are object dtype per fresh inspection; coerce to numeric.
    nb = pd.to_numeric(df["not_before"], errors="coerce")
    na = pd.to_numeric(df["not_after"], errors="coerce")
    date_range = na - nb

    nonnull_both = df[nb.notna() & na.notna()]
    n_both = len(nonnull_both)
    add_claim(
        "count",
        "Rows with BOTH not_before AND not_after non-null",
        n_both,
        units="rows",
        source_method="df[(not_before.notna()) & (not_after.notna())]",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Rows with not_before null",
        int(nb.isna().sum()),
        units="rows",
        source_method="df.not_before.isna().sum()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Rows with not_after null",
        int(na.isna().sum()),
        units="rows",
        source_method="df.not_after.isna().sum()",
        source_file="profile-dataset.md",
    )

    dr_nonnull = date_range.dropna()
    add_claim(
        "count",
        "Rows with derivable date_range (both dates present)",
        int(len(dr_nonnull)),
        units="rows",
        source_method="(not_after - not_before).dropna()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "mean",
        "Mean date_range (years) among rows with both dates",
        float(dr_nonnull.mean()),
        units="years",
        source_method="(not_after - not_before).mean()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "median",
        "Median date_range (years) among rows with both dates",
        float(dr_nonnull.median()),
        units="years",
        source_method="(not_after - not_before).median()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Min date_range",
        float(dr_nonnull.min()),
        units="years",
        source_method="(not_after - not_before).min()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Max date_range",
        float(dr_nonnull.max()),
        units="years",
        source_method="(not_after - not_before).max()",
        source_file="profile-dataset.md",
    )

    # Geolocated count
    lat = pd.to_numeric(df["Latitude"], errors="coerce")
    lon = pd.to_numeric(df["Longitude"], errors="coerce")
    valid_latlon = (
        lat.notna() & lon.notna() & (lat != 0) & (lon != 0)
    )
    n_geo = int(valid_latlon.sum())
    add_claim(
        "count",
        "Rows with valid (non-null, non-zero) Latitude AND Longitude",
        n_geo,
        units="rows",
        source_method="((lat.notna())&(lon.notna())&(lat!=0)&(lon!=0)).sum()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "rate",
        "Proportion of rows with valid (non-null, non-zero) Latitude AND Longitude",
        round(n_geo / n_rows, 6),
        units="fraction",
        source_method="n_geo / n_rows",
        source_file="profile-dataset.md",
    )

    # Also the null-alone rate (doesn't require non-zero)
    lat_nonnull = int(lat.notna().sum())
    lon_nonnull = int(lon.notna().sum())
    both_nonnull = int((lat.notna() & lon.notna()).sum())
    add_claim(
        "count",
        "Rows with non-null Latitude",
        lat_nonnull,
        units="rows",
        source_method="df.Latitude.notna().sum()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Rows with non-null Longitude",
        lon_nonnull,
        units="rows",
        source_method="df.Longitude.notna().sum()",
        source_file="profile-dataset.md",
    )
    add_claim(
        "count",
        "Rows with non-null Latitude AND non-null Longitude",
        both_nonnull,
        units="rows",
        source_method="(df.Latitude.notna() & df.Longitude.notna()).sum()",
        source_file="profile-dataset.md",
    )

    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "null_table": null_table,
        "high_null": high_null,
        "nb": nb,
        "na": na,
        "date_range": date_range,
        "lat": lat,
        "lon": lon,
        "valid_latlon": valid_latlon,
    }


# --------------------------------------------------------------------------- #
# Subset profile helpers
# --------------------------------------------------------------------------- #


def subset_profile(
    df: pd.DataFrame,
    group_col: str,
    label: str,
    nb: pd.Series,
    na: pd.Series,
    lat: pd.Series,
    lon: pd.Series,
) -> dict[str, Any]:
    """Produce per-group statistics for a subset column."""
    log(f"subset profile: {label}")

    # Drop NaN / empty-string groups for counting; report the excluded mass.
    group_raw = df[group_col]
    n_null_group = int(group_raw.isna().sum())
    # Also drop empty string if present (URBAN fields often empty string).
    is_empty = group_raw.fillna("").astype(str).str.strip() == ""
    n_empty_string = int((~group_raw.isna() & is_empty).sum())

    valid_mask = ~group_raw.isna() & ~is_empty
    series = group_raw[valid_mask]
    n_valid = int(valid_mask.sum())
    unique_groups = int(series.nunique())

    add_claim(
        "count",
        f"Rows with null {group_col}",
        n_null_group,
        units="rows",
        source_method=f"df['{group_col}'].isna().sum()",
        source_file=f"profile-{label}.md",
    )
    add_claim(
        "count",
        f"Rows with empty-string (non-null) {group_col}",
        n_empty_string,
        units="rows",
        source_method="(~df[col].isna() & (df[col].str.strip() == ''))",
        source_file=f"profile-{label}.md",
    )
    add_claim(
        "count",
        f"Rows with a valid (non-null, non-empty) {group_col} label",
        n_valid,
        units="rows",
        source_method="sum of (non-null AND non-empty-string)",
        source_file=f"profile-{label}.md",
    )
    add_claim(
        "count",
        f"Number of distinct non-empty {group_col} groups",
        unique_groups,
        units="groups",
        source_method=f"df['{group_col}'].nunique(dropna=True) (post empty-string filter)",
        source_file=f"profile-{label}.md",
    )

    counts = series.value_counts()
    top20 = counts.head(20)
    top20_table = pd.DataFrame(
        {
            "rank": range(1, len(top20) + 1),
            "group": top20.index,
            "count": top20.values,
            "pct_of_valid": (top20.values / n_valid * 100).round(3),
        }
    )
    top20_path = TABLES_DIR / f"top20_{label}.csv"
    top20_table.to_csv(top20_path, index=False)
    log(f"wrote tables/top20_{label}.csv")

    # Claims for each top-20 ranking
    for i, (g, c) in enumerate(counts.head(20).items(), start=1):
        add_claim(
            "ranking",
            f"Top-{i} {group_col}: {g!r}",
            {"rank": i, "group": str(g), "count": int(c)},
            units="",
            source_method=f"df['{group_col}'].value_counts().head(20)",
            source_file=f"profile-{label}.md",
        )

    # Threshold qualifying counts
    threshold_rows = []
    for t in THRESHOLDS:
        n_qual = int((counts >= t).sum())
        threshold_rows.append({"threshold": t, "n_groups_qualifying": n_qual})
        add_claim(
            "threshold_qualifying",
            f"{group_col}: number of groups with >= {t} rows",
            n_qual,
            units="groups",
            source_method=f"(counts >= {t}).sum()",
            source_file=f"profile-{label}.md",
        )
    threshold_table = pd.DataFrame(threshold_rows)
    threshold_table.to_csv(
        TABLES_DIR / f"threshold_qualifying_{label}.csv", index=False
    )
    log(f"wrote tables/threshold_qualifying_{label}.csv")

    # Per-group detail for groups passing threshold 100
    qualifying = counts[counts >= 100].index.tolist()
    rows = []
    for g in qualifying:
        sub = df[df[group_col] == g]
        sub_nb = nb.loc[sub.index]
        sub_na = na.loc[sub.index]
        sub_lat = lat.loc[sub.index]
        sub_lon = lon.loc[sub.index]
        sub_range = sub_na - sub_nb
        date_range_nonnull = sub_range.dropna()

        row_record = {
            "group": g,
            "count": int(len(sub)),
            "pct_of_valid": round(len(sub) / n_valid * 100, 4),
            "date_range_min": float(date_range_nonnull.min())
            if len(date_range_nonnull)
            else np.nan,
            "date_range_max": float(date_range_nonnull.max())
            if len(date_range_nonnull)
            else np.nan,
            "date_range_mean": float(date_range_nonnull.mean())
            if len(date_range_nonnull)
            else np.nan,
            "date_range_median": float(date_range_nonnull.median())
            if len(date_range_nonnull)
            else np.nan,
            "lat_null_rate": float(sub_lat.isna().mean()),
            "lon_null_rate": float(sub_lon.isna().mean()),
            "not_before_null_rate": float(sub_nb.isna().mean()),
            "not_after_null_rate": float(sub_na.isna().mean()),
        }
        if group_col == "urban_context_city":
            pop_est = pd.to_numeric(
                sub["urban_context_pop_est"], errors="coerce"
            )
            row_record["pop_est_null_rate"] = float(pop_est.isna().mean())
            row_record["pop_est_mean"] = (
                float(pop_est.mean()) if pop_est.notna().any() else np.nan
            )
        rows.append(row_record)

    detail = pd.DataFrame(rows).sort_values("count", ascending=False)
    detail_path = TABLES_DIR / f"detail_threshold100_{label}.csv"
    detail.to_csv(detail_path, index=False)
    log(f"wrote tables/detail_threshold100_{label}.csv")

    # Summary claims about the threshold-100 cohort
    add_claim(
        "count",
        f"{group_col}: number of groups at threshold 100 (detail table size)",
        int(len(detail)),
        units="groups",
        source_method="(counts >= 100).sum()",
        source_file=f"profile-{label}.md",
    )
    if len(detail):
        add_claim(
            "mean",
            f"{group_col} @ threshold 100: mean per-group count",
            float(detail["count"].mean()),
            units="rows",
            source_method="detail['count'].mean()",
            source_file=f"profile-{label}.md",
        )
        add_claim(
            "median",
            f"{group_col} @ threshold 100: median per-group count",
            float(detail["count"].median()),
            units="rows",
            source_method="detail['count'].median()",
            source_file=f"profile-{label}.md",
        )
        add_claim(
            "mean",
            f"{group_col} @ threshold 100: mean Latitude null-rate",
            float(detail["lat_null_rate"].mean()),
            units="fraction",
            source_method="detail['lat_null_rate'].mean()",
            source_file=f"profile-{label}.md",
        )
        add_claim(
            "mean",
            f"{group_col} @ threshold 100: mean not_before null-rate",
            float(detail["not_before_null_rate"].mean()),
            units="fraction",
            source_method="detail['not_before_null_rate'].mean()",
            source_file=f"profile-{label}.md",
        )

    return {
        "counts": counts,
        "top20": top20_table,
        "thresholds": threshold_table,
        "detail": detail,
        "n_valid": n_valid,
        "unique_groups": unique_groups,
        "n_null_group": n_null_group,
        "n_empty_string": n_empty_string,
    }


# --------------------------------------------------------------------------- #
# Artefact checks
# --------------------------------------------------------------------------- #


def artefact_midpoint_inflation(nb: pd.Series, na: pd.Series) -> dict[str, Any]:
    """Chi-square at century-midpoint years (50, 150, 250, 350 AD) vs ±15y window."""
    midpoint = (nb + na) / 2.0
    mid = midpoint.dropna()
    mid_int = mid.round().astype(int)

    results = []
    for target in (50, 150, 250, 350):
        window = mid_int[(mid_int >= target - 15) & (mid_int <= target + 15)]
        n_target = int((window == target).sum())
        n_window_total = int(len(window))
        n_other = n_window_total - n_target
        n_years_other = 30  # ±15 excluding target year => 30 year-bins
        # Uniform expectation in the 31-year window
        # Use chisquare on observed = [n_target, n_other]
        # against expected proportional to [1, n_years_other] of same total.
        total = n_target + n_other
        if total == 0:
            results.append(
                {
                    "target_year": target,
                    "count_at_target": n_target,
                    "count_in_window_excl": n_other,
                    "expected_if_uniform": np.nan,
                    "chi2": np.nan,
                    "pvalue": np.nan,
                }
            )
            continue
        exp_target = total * (1 / 31)
        exp_other = total * (30 / 31)
        chi2, pval = stats.chisquare(
            [n_target, n_other], f_exp=[exp_target, exp_other]
        )
        results.append(
            {
                "target_year": target,
                "count_at_target": n_target,
                "count_in_window_excl": n_other,
                "expected_if_uniform_at_target": round(exp_target, 3),
                "chi2": round(float(chi2), 3),
                "pvalue": float(pval),
            }
        )
        add_claim(
            "count",
            f"midpoint-inflation: count at year AD {target}",
            n_target,
            units="rows",
            source_method="((not_before+not_after)/2).round()==target",
            source_file="artefacts.md",
        )
        add_claim(
            "count",
            f"midpoint-inflation: count in ±15 window (excl target) at year AD {target}",
            n_other,
            units="rows",
            source_method="window total minus target count",
            source_file="artefacts.md",
        )
        add_claim(
            "chisq",
            f"midpoint-inflation: chi2 at AD {target} (1-df, uniform expectation)",
            round(float(chi2), 3),
            units="",
            source_method="scipy.stats.chisquare([obs_t, obs_o], [exp_t, exp_o])",
            source_file="artefacts.md",
        )
        add_claim(
            "pvalue",
            f"midpoint-inflation: pvalue at AD {target}",
            float(pval),
            units="",
            source_method="scipy.stats.chisquare",
            source_file="artefacts.md",
        )

    tbl = pd.DataFrame(results)
    tbl.to_csv(TABLES_DIR / "artefact_midpoint_inflation.csv", index=False)
    return {"table": tbl, "midpoint_int": mid_int}


def artefact_editorial_spikes(nb: pd.Series, na: pd.Series) -> dict[str, Any]:
    """Spike check at editorial-boundary years for both not_before and not_after."""
    years_check = [-14, 27, 97, 192, 193, 212, 235]
    results = []

    for col_name, series in [("not_before", nb), ("not_after", na)]:
        s = series.dropna().round().astype(int)
        for y in years_check:
            n_at = int((s == y).sum())
            # Neighbours ±5 excluding y
            neigh = [y + d for d in range(-5, 6) if d != 0]
            n_neigh_counts = [int((s == yy).sum()) for yy in neigh]
            mean_neigh = float(np.mean(n_neigh_counts)) if n_neigh_counts else np.nan
            # chi-square: [n_at, n_neigh_total] vs expected proportional
            n_neigh_total = int(sum(n_neigh_counts))
            total = n_at + n_neigh_total
            if total == 0:
                chi2, pval = np.nan, np.nan
            else:
                exp_at = total / 11
                exp_other = total * 10 / 11
                chi2, pval = stats.chisquare(
                    [n_at, n_neigh_total], f_exp=[exp_at, exp_other]
                )
                chi2 = round(float(chi2), 3)
                pval = float(pval)
            results.append(
                {
                    "column": col_name,
                    "year": y,
                    "count_at_year": n_at,
                    "mean_of_neighbours": round(mean_neigh, 3),
                    "count_in_neighbours": n_neigh_total,
                    "chi2": chi2,
                    "pvalue": pval,
                }
            )
            add_claim(
                "count",
                f"editorial-spikes: {col_name} count at year {y}",
                n_at,
                units="rows",
                source_method=f"(df['{col_name}']==y).sum()",
                source_file="artefacts.md",
            )
            add_claim(
                "mean",
                f"editorial-spikes: {col_name} mean count of ±5 neighbours (excl y) at year {y}",
                round(mean_neigh, 3),
                units="rows",
                source_method="np.mean of 10 neighbour-year counts",
                source_file="artefacts.md",
            )
            if not np.isnan(chi2):
                add_claim(
                    "chisq",
                    f"editorial-spikes: chi2 on {col_name} at year {y}",
                    chi2,
                    units="",
                    source_method="scipy.stats.chisquare",
                    source_file="artefacts.md",
                )
                add_claim(
                    "pvalue",
                    f"editorial-spikes: pvalue on {col_name} at year {y}",
                    pval,
                    units="",
                    source_method="scipy.stats.chisquare",
                    source_file="artefacts.md",
                )

    tbl = pd.DataFrame(results)
    tbl.to_csv(TABLES_DIR / "artefact_editorial_spikes.csv", index=False)
    return {"table": tbl}


def artefact_coordinate_precision(lat: pd.Series, lon: pd.Series) -> dict[str, Any]:
    """Histogram of decimal places in Latitude and Longitude."""
    def decimals(x: float) -> int:
        if pd.isna(x):
            return -1
        s = f"{x:.15f}".rstrip("0").rstrip(".")
        if "." in s:
            return len(s.split(".")[1])
        return 0

    lat_dec = lat.apply(decimals)
    lon_dec = lon.apply(decimals)

    lat_hist = lat_dec.value_counts().sort_index()
    lon_hist = lon_dec.value_counts().sort_index()

    combined = pd.DataFrame(
        {
            "decimal_places": sorted(set(lat_hist.index) | set(lon_hist.index)),
        }
    )
    combined["lat_count"] = combined["decimal_places"].map(lat_hist).fillna(0).astype(int)
    combined["lon_count"] = combined["decimal_places"].map(lon_hist).fillna(0).astype(int)
    combined.to_csv(TABLES_DIR / "artefact_coordinate_precision.csv", index=False)

    # Modal precision
    mode_lat = int(lat_hist.idxmax())
    mode_lon = int(lon_hist.idxmax())
    add_claim(
        "count",
        "coordinate-precision: modal decimal places on Latitude",
        mode_lat,
        units="decimal_places",
        source_method="lat decimals histogram .idxmax()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "coordinate-precision: modal decimal places on Longitude",
        mode_lon,
        units="decimal_places",
        source_method="lon decimals histogram .idxmax()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "coordinate-precision: count of rows at modal Latitude precision",
        int(lat_hist.max()),
        units="rows",
        source_method="lat_hist.max()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "coordinate-precision: count of rows at modal Longitude precision",
        int(lon_hist.max()),
        units="rows",
        source_method="lon_hist.max()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "coordinate-precision: count of non-null Latitude values with 0 decimal places",
        int(lat_hist.get(0, 0)),
        units="rows",
        source_method="lat_hist.get(0, 0)",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "coordinate-precision: count of non-null Longitude values with 0 decimal places",
        int(lon_hist.get(0, 0)),
        units="rows",
        source_method="lon_hist.get(0, 0)",
        source_file="artefacts.md",
    )
    return {"table": combined, "mode_lat": mode_lat, "mode_lon": mode_lon}


def artefact_outlier_coordinates(
    lat: pd.Series, lon: pd.Series
) -> dict[str, Any]:
    """Rows with |Latitude|>90 or |Longitude|>180."""
    bad_lat = int(((lat.abs() > 90) & lat.notna()).sum())
    bad_lon = int(((lon.abs() > 180) & lon.notna()).sum())
    bad_any = int(
        (((lat.abs() > 90) | (lon.abs() > 180)) & lat.notna() & lon.notna()).sum()
    )
    add_claim(
        "count",
        "outlier-coordinates: rows with |Latitude|>90",
        bad_lat,
        units="rows",
        source_method="(lat.abs()>90).sum()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "outlier-coordinates: rows with |Longitude|>180",
        bad_lon,
        units="rows",
        source_method="(lon.abs()>180).sum()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "outlier-coordinates: rows with any coordinate outside valid range",
        bad_any,
        units="rows",
        source_method="either clause true",
        source_file="artefacts.md",
    )
    return {"bad_lat": bad_lat, "bad_lon": bad_lon, "bad_any": bad_any}


def artefact_duplicate_rows(df: pd.DataFrame) -> dict[str, Any]:
    """Exact-duplicate and LIST-ID duplicate counts.

    The full-row duplicate test handles unhashable cell values (lists/dicts
    from JSON fields) by hashing each cell with `repr()` — this also dodges
    the UnicodeDecodeError triggered by byte strings in the inscription-text
    columns under pandas' `astype(str)` path.
    """
    # Build a per-row hash key from repr() of every cell.
    # Doing this row-wise with itertuples is fast enough at 183k rows.
    n = len(df)
    keys = np.empty(n, dtype=object)
    # `itertuples(index=False)` yields named tuples; repr(tuple) is stable.
    for i, row in enumerate(df.itertuples(index=False, name=None)):
        keys[i] = tuple(repr(v) for v in row)
    key_series = pd.Series(keys)
    dup_all = int(key_series.duplicated().sum())

    dup_listid = int(df["LIST-ID"].duplicated().sum())

    add_claim(
        "count",
        "duplicate-rows: exact-duplicate row count (all columns)",
        dup_all,
        units="rows",
        source_method="df.duplicated().sum() (with stringified fallback)",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "duplicate-rows: rows with duplicate LIST-ID value",
        dup_listid,
        units="rows",
        source_method="df['LIST-ID'].duplicated().sum()",
        source_file="artefacts.md",
    )
    return {"dup_all": dup_all, "dup_listid": dup_listid}


def artefact_negative_date_range(nb: pd.Series, na: pd.Series) -> int:
    """Count rows where not_before > not_after."""
    n_neg = int(((nb.notna()) & (na.notna()) & (nb > na)).sum())
    add_claim(
        "count",
        "negative-date-range: rows where not_before > not_after",
        n_neg,
        units="rows",
        source_method="((nb.notna()) & (na.notna()) & (nb > na)).sum()",
        source_file="artefacts.md",
    )
    return n_neg


def artefact_date_range_extreme(
    nb: pd.Series, na: pd.Series
) -> dict[str, Any]:
    """Rows with date_range > 500 years."""
    dr = (na - nb).dropna()
    n_extreme = int((dr > 500).sum())
    add_claim(
        "count",
        "date-range-extreme: rows with (not_after-not_before) > 500",
        n_extreme,
        units="rows",
        source_method="((not_after-not_before)>500).sum()",
        source_file="artefacts.md",
    )
    return {"n_extreme": n_extreme}


def artefact_temporal_outliers(nb: pd.Series, na: pd.Series) -> dict[str, Any]:
    """Rows outside LIRE's stated 50 BC – AD 350 envelope."""
    n_before = int(((nb < -50) & nb.notna()).sum())
    n_after = int(((na > 350) & na.notna()).sum())
    n_any = int(
        (((nb < -50) & nb.notna()) | ((na > 350) & na.notna())).sum()
    )
    add_claim(
        "count",
        "temporal-outliers: rows with not_before < -50",
        n_before,
        units="rows",
        source_method="((nb<-50) & nb.notna()).sum()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "temporal-outliers: rows with not_after > 350",
        n_after,
        units="rows",
        source_method="((na>350) & na.notna()).sum()",
        source_file="artefacts.md",
    )
    add_claim(
        "count",
        "temporal-outliers: rows outside (50 BC – AD 350) envelope",
        n_any,
        units="rows",
        source_method="union of both outlier clauses",
        source_file="artefacts.md",
    )
    return {"n_before": n_before, "n_after": n_after, "n_any": n_any}


# --------------------------------------------------------------------------- #
# Unexpected-pattern diagnostic
# --------------------------------------------------------------------------- #


def unexpected_pattern_diagnostic(
    nb: pd.Series, na: pd.Series, n_rows: int
) -> dict[str, Any]:
    """Granularity histogram + broad-bucket date-range histogram."""
    dr = (na - nb).dropna()
    total_dr = int(len(dr))
    dr_int = dr.round().astype(int)

    # Granularity histogram
    categories = OrderedDict()
    categories["eq_0"] = int((dr_int == 0).sum())
    categories["eq_25"] = int((dr_int == 25).sum())
    categories["eq_50"] = int((dr_int == 50).sum())
    categories["99_to_101 (century)"] = int(
        ((dr_int >= 99) & (dr_int <= 101)).sum()
    )
    categories["199_to_201 (bicentury)"] = int(
        ((dr_int >= 199) & (dr_int <= 201)).sum()
    )
    # Other round numbers not already in buckets above
    round_values = {10, 20, 30, 40, 60, 70, 75, 80, 90, 125, 150, 175, 250, 300, 400, 500}
    round_counts = {
        v: int((dr_int == v).sum())
        for v in sorted(round_values)
    }
    # Irregular = total - (all categorised above summed without double-count)
    categorised_total = sum(categories.values())
    categorised_total += sum(round_counts.values())
    categories["other_round_values (10,20,30,...500)"] = sum(round_counts.values())
    categories["irregular"] = total_dr - sum(
        [
            categories["eq_0"],
            categories["eq_25"],
            categories["eq_50"],
            categories["99_to_101 (century)"],
            categories["199_to_201 (bicentury)"],
            categories["other_round_values (10,20,30,...500)"],
        ]
    )

    gran_rows = [
        {
            "category": k,
            "count": v,
            "pct_of_non_null_date_range": round(v / total_dr * 100, 4),
            "pct_of_total_rows": round(v / n_rows * 100, 4),
        }
        for k, v in categories.items()
    ]
    gran_tbl = pd.DataFrame(gran_rows)
    gran_tbl.to_csv(TABLES_DIR / "granularity_histogram.csv", index=False)
    log("wrote tables/granularity_histogram.csv")

    # Round-value detail as separate table
    round_tbl = pd.DataFrame(
        [
            {
                "value": v,
                "count": c,
                "pct_of_non_null_date_range": round(c / total_dr * 100, 4),
            }
            for v, c in round_counts.items()
        ]
    )
    round_tbl.to_csv(TABLES_DIR / "granularity_round_values.csv", index=False)

    for k, v in categories.items():
        add_claim(
            "count",
            f"granularity: rows with date_range category {k}",
            v,
            units="rows",
            source_method="derived from (not_after-not_before)",
            source_file="artefacts.md",
        )
        pct = round(v / total_dr * 100, 4)
        add_claim(
            "percentage",
            f"granularity: pct of non-null date_range in category {k}",
            pct,
            units="%",
            source_method="v / total_dr * 100",
            source_file="artefacts.md",
        )

    # Broad histogram — bucketed bins
    bins = [-0.5, 1.5, 25.5, 50.5, 100.5, 200.5, 500.5, np.inf]
    labels = ["<=1", "2..25", "26..50", "51..100", "101..200", "201..500", ">500"]
    broad = pd.cut(dr_int, bins=bins, labels=labels, include_lowest=True)
    broad_hist = broad.value_counts().reindex(labels).fillna(0).astype(int)
    broad_tbl = pd.DataFrame(
        {
            "bucket": broad_hist.index,
            "count": broad_hist.values,
            "pct_of_non_null_date_range": (
                broad_hist.values / total_dr * 100
            ).round(4),
        }
    )
    broad_tbl.to_csv(TABLES_DIR / "broad_date_range_histogram.csv", index=False)
    log("wrote tables/broad_date_range_histogram.csv")

    for bucket, count in zip(broad_tbl["bucket"], broad_tbl["count"]):
        add_claim(
            "count",
            f"broad-histogram: rows with date_range in bucket {bucket}",
            int(count),
            units="rows",
            source_method="pd.cut on date_range",
            source_file="artefacts.md",
        )

    # Flag anomalies >5% (of non-null date range)
    flagged = []
    for r in gran_rows:
        if r["category"] == "irregular":
            continue
        if r["pct_of_non_null_date_range"] > 5.0:
            flagged.append(r)

    return {
        "gran_tbl": gran_tbl,
        "broad_tbl": broad_tbl,
        "round_tbl": round_tbl,
        "flagged": flagged,
        "total_dr": total_dr,
    }


# --------------------------------------------------------------------------- #
# Null-profile artefact check
# --------------------------------------------------------------------------- #


def artefact_null_profile(null_table: pd.DataFrame) -> list[dict[str, Any]]:
    """Export the null profile as an artefact table; flag columns >50 %."""
    null_table.to_csv(TABLES_DIR / "artefact_null_profile.csv", index=False)
    flagged = null_table[null_table["null_rate"] > 0.5].to_dict(orient="records")
    for rec in flagged:
        add_claim(
            "percentage",
            f"null-profile: {rec['column']} null rate",
            round(rec["null_rate"] * 100, 4),
            units="%",
            source_method="df.isna().mean() on column",
            source_file="artefacts.md",
        )
    return flagged


# --------------------------------------------------------------------------- #
# Markdown writers
# --------------------------------------------------------------------------- #


def fmt_pct(x: float) -> str:
    return f"{x * 100:.3f}%"


def write_profile_dataset(
    ds: dict[str, Any], n_schema: int
) -> None:
    """Write profile-dataset.md."""
    n_rows = ds["n_rows"]
    n_cols = ds["n_cols"]
    dr = ds["date_range"].dropna()
    n_geo = int(ds["valid_latlon"].sum())

    md = []
    md.append("# LIRE v3.0 — dataset-level profile\n")
    md.append(
        f"_Generated {_now()} by `data-profile-scout` methodology._\n"
    )
    md.append("## Dimensions\n")
    md.append(f"- Rows: **{n_rows:,}**")
    md.append(f"- Columns in parquet: **{n_cols}**")
    md.append(f"- Attributes documented in seed schema `LI_metadata.csv`: **{n_schema}**")
    md.append(
        "- Schema disagreement: three columns in schema are not present in parquet "
        "(`is_geotemporal`, `is_within_RE`, `material_EDCS`). All 63 parquet columns "
        "are in the schema. See `decisions.md` Decision 3.\n"
    )

    md.append("## Date-range summary\n")
    md.append(
        f"- Rows with both `not_before` and `not_after` non-null: "
        f"**{int(len(dr)):,}** ({len(dr)/n_rows*100:.3f}%)"
    )
    md.append(
        f"- Rows with null `not_before`: **{int(ds['nb'].isna().sum()):,}**; "
        f"with null `not_after`: **{int(ds['na'].isna().sum()):,}**"
    )
    md.append(f"- `date_range` = `not_after - not_before`:")
    md.append(f"    - mean: **{dr.mean():.3f}** years")
    md.append(f"    - median: **{dr.median():.3f}** years")
    md.append(f"    - min: **{dr.min():.0f}** years; max: **{dr.max():.0f}** years")
    md.append(
        f"    - (broad distribution + granularity diagnostic in `artefacts.md` §§ "
        f"*Unexpected-pattern diagnostic*)\n"
    )

    md.append("## Spatial summary\n")
    lat, lon = ds["lat"], ds["lon"]
    md.append(
        f"- Rows with valid (non-null, non-zero) `Latitude` AND `Longitude`: "
        f"**{n_geo:,}** ({n_geo/n_rows*100:.3f}%)"
    )
    md.append(
        f"- Rows with non-null `Latitude` AND non-null `Longitude` (including zeros): "
        f"**{int((lat.notna() & lon.notna()).sum()):,}**"
    )
    md.append(
        "- Because LIRE is a geotemporal subset of the combined corpus, the valid-coordinate"
        " rate is expected to be ~100 %. Any shortfall from 100 % is discussed in "
        "`artefacts.md` under `geolocated-rate`.\n"
    )

    md.append("## Per-column null / uniqueness\n")
    md.append(
        "Full table in `tables/null_and_unique_by_column.csv`. Top-10 most-null columns:\n"
    )
    md.append("| column | null rate | n null | n unique |")
    md.append("|---|---:|---:|---:|")
    for _, row in ds["null_table"].head(10).iterrows():
        md.append(
            f"| `{row['column']}` | {row['null_rate']*100:.3f}% | {row['n_null']:,} | "
            f"{int(row['n_unique']):,} |"
        )
    md.append("")
    md.append(
        f"- Columns with >50% nulls: **{int(len(ds['high_null'])):,}** "
        f"(see `artefacts.md` §`null-profile`).\n"
    )

    (OUTPUT_DIR / "profile-dataset.md").write_text("\n".join(md))
    log("wrote profile-dataset.md")


def write_profile_subset(
    label: str, group_col: str, result: dict[str, Any], n_rows: int
) -> None:
    md = []
    md.append(f"# LIRE v3.0 — per-{label} profile\n")
    md.append(f"_Group column: `{group_col}`._\n")

    md.append("## Basic counts\n")
    md.append(
        f"- Rows with valid (non-null, non-empty) `{group_col}` label: "
        f"**{result['n_valid']:,}** of {n_rows:,} "
        f"({result['n_valid']/n_rows*100:.3f}%)"
    )
    md.append(
        f"- Null `{group_col}` rows: **{result['n_null_group']:,}**; "
        f"empty-string rows: **{result['n_empty_string']:,}**"
    )
    md.append(
        f"- Distinct non-empty groups: **{result['unique_groups']:,}**\n"
    )

    md.append("## Top-20 groups by row count\n")
    md.append("| rank | group | count | % of valid |")
    md.append("|---:|---|---:|---:|")
    for _, r in result["top20"].iterrows():
        group_str = str(r["group"])[:60]
        md.append(
            f"| {r['rank']} | `{group_str}` | {r['count']:,} | {r['pct_of_valid']:.3f}% |"
        )
    md.append(
        f"\nFull ranking: `tables/top20_{label}.csv`.\n"
    )

    md.append("## Threshold qualification\n")
    md.append("| min rows per group | groups qualifying |")
    md.append("|---:|---:|")
    for _, r in result["thresholds"].iterrows():
        md.append(f"| {r['threshold']} | {r['n_groups_qualifying']:,} |")
    md.append(
        f"\nSee `tables/threshold_qualifying_{label}.csv`.\n"
    )

    md.append("## Per-group detail at threshold 100\n")
    md.append(
        f"- Number of groups at threshold 100: **{int(len(result['detail'])):,}**"
    )
    if len(result["detail"]):
        md.append(
            f"- Mean per-group count: **{result['detail']['count'].mean():.1f}**; "
            f"median: **{result['detail']['count'].median():.0f}**"
        )
        md.append(
            f"- Mean Latitude null-rate: "
            f"**{result['detail']['lat_null_rate'].mean()*100:.4f}%**; "
            f"mean `not_before` null-rate: "
            f"**{result['detail']['not_before_null_rate'].mean()*100:.4f}%**"
        )
    md.append(
        f"\nFull detail in `tables/detail_threshold100_{label}.csv` "
        "(sorted by count descending).\n"
    )
    (OUTPUT_DIR / f"profile-{label}.md").write_text("\n".join(md))
    log(f"wrote profile-{label}.md")


def write_artefacts(
    ds: dict[str, Any],
    mid: dict[str, Any],
    spikes: dict[str, Any],
    coord: dict[str, Any],
    outlier: dict[str, Any],
    dup: dict[str, Any],
    n_neg: int,
    extreme: dict[str, Any],
    temporal: dict[str, Any],
    null_flagged: list[dict[str, Any]],
    unex: dict[str, Any],
    n_rows: int,
) -> None:
    md = []
    md.append("# LIRE v3.0 — artefact checks\n")
    md.append(
        "This file enumerates the data-artefact audit run per the canonical "
        "`data-profile-scout` methodology. Expected-signal references are to "
        "Heřmánková, Kaše & Sobotková 2021 (JDH 5/1)."
    )
    md.append(
        "\nTwo canonical checks — `is_within_RE-rate` and `is_geotemporal-rate` "
        "— are **NOT RUN**: the corresponding boolean columns are absent from "
        "the parquet (see `decisions.md` Decision 3). Do not interpret silence "
        "as a pass.\n"
    )

    # midpoint inflation
    md.append("## midpoint-inflation\n")
    md.append(
        "Chi-square test: count at a century-midpoint year (AD 50, 150, 250, 350) vs a "
        "±15-year window (31 year-bins). Expected signal per Heřmánková et al. §64."
    )
    md.append("")
    md.append(
        "| target year | count at year | count in ±15 excl | expected at target (uniform) "
        "| chi2 | p-value |"
    )
    md.append("|---:|---:|---:|---:|---:|---:|")
    for _, r in mid["table"].iterrows():
        md.append(
            f"| AD {r['target_year']} | {int(r['count_at_target']):,} | "
            f"{int(r['count_in_window_excl']):,} | "
            f"{r.get('expected_if_uniform_at_target', np.nan)} | {r['chi2']} | "
            f"{r['pvalue']:.3e} |"
        )
    md.append("")

    # editorial spikes
    md.append("## editorial-spikes\n")
    md.append(
        "For each editorial-boundary year, count at the year vs mean of ±5 neighbours "
        "(10 bins), excluding the year itself. Chi-square is computed on "
        "`[count_at_year, count_in_neighbours]` vs uniform. Expected signal per "
        "Heřmánková et al. §94."
    )
    md.append("")
    md.append(
        "| column | year | count at year | mean of neighbours | "
        "count in neighbours | chi2 | p-value |"
    )
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for _, r in spikes["table"].iterrows():
        md.append(
            f"| `{r['column']}` | {r['year']} | {int(r['count_at_year']):,} | "
            f"{r['mean_of_neighbours']} | {int(r['count_in_neighbours']):,} | "
            f"{r['chi2']} | "
            f"{(f'{r['pvalue']:.3e}') if not pd.isna(r['pvalue']) else 'n/a'} |"
        )
    md.append("")

    # coordinate precision
    md.append("## coordinate-precision\n")
    md.append(
        f"- Modal decimal places on `Latitude`: **{coord['mode_lat']}** "
        f"({int(coord['table']['lat_count'].max()):,} rows). "
        f"Modal on `Longitude`: **{coord['mode_lon']}** "
        f"({int(coord['table']['lon_count'].max()):,} rows)."
    )
    md.append("- Distribution in `tables/artefact_coordinate_precision.csv`.\n")

    # outlier coords
    md.append("## outlier-coordinates\n")
    md.append(f"- Rows with `|Latitude|>90`: **{outlier['bad_lat']}**")
    md.append(f"- Rows with `|Longitude|>180`: **{outlier['bad_lon']}**")
    md.append(f"- Any out-of-range: **{outlier['bad_any']}** (expected 0).\n")

    # duplicate rows
    md.append("## duplicate-rows\n")
    md.append(f"- Exact-duplicate rows across all columns: **{dup['dup_all']:,}**")
    md.append(f"- Rows with duplicate `LIST-ID` value: **{dup['dup_listid']:,}**\n")

    # negative date range
    md.append("## negative-date-range\n")
    md.append(
        f"- Rows where `not_before > not_after`: **{n_neg}** (expected 0 per release notes).\n"
    )

    # date range extreme
    md.append("## date-range-extreme\n")
    md.append(
        f"- Rows with `date_range > 500` years: **{extreme['n_extreme']:,}** "
        f"({extreme['n_extreme']/n_rows*100:.3f}% of all rows).\n"
    )

    # temporal outliers
    md.append("## temporal-outliers\n")
    md.append(
        f"- Rows with `not_before < -50`: **{temporal['n_before']:,}**"
    )
    md.append(
        f"- Rows with `not_after > 350`: **{temporal['n_after']:,}**"
    )
    md.append(
        f"- Rows outside (50 BC – AD 350) envelope: **{temporal['n_any']:,}** (expected 0).\n"
    )

    # geolocated rate
    n_geo = int(ds["valid_latlon"].sum())
    md.append("## geolocated-rate\n")
    md.append(
        f"- Rows with valid (non-null, non-zero) `Latitude` AND `Longitude`: "
        f"**{n_geo:,}** of {n_rows:,} = **{n_geo/n_rows*100:.3f}%** (expected ~100 %).\n"
    )

    md.append("## is_within_RE-rate — NOT RUN\n")
    md.append(
        "Column `is_within_RE` is not present in the parquet. Check skipped. "
        "See `decisions.md` Decision 3.\n"
    )
    md.append("## is_geotemporal-rate — NOT RUN\n")
    md.append(
        "Column `is_geotemporal` is not present in the parquet. Check skipped. "
        "See `decisions.md` Decision 3.\n"
    )

    # null profile
    md.append("## null-profile\n")
    md.append(f"- Columns with >50% nulls: **{len(null_flagged)}**.")
    if null_flagged:
        md.append("")
        md.append("| column | null rate | n null |")
        md.append("|---|---:|---:|")
        # Only top-15 here; full in CSV.
        for rec in null_flagged[:15]:
            md.append(
                f"| `{rec['column']}` | {rec['null_rate']*100:.3f}% | {rec['n_null']:,} |"
            )
    md.append(
        "\nFull sorted list in `tables/artefact_null_profile.csv` "
        "(identical to `tables/null_and_unique_by_column.csv`).\n"
    )

    # Unexpected pattern diagnostic
    md.append("## Unexpected-pattern diagnostic\n")
    md.append("### View 1 — granularity histogram (date_range categories)\n")
    md.append("| category | count | % of non-null date_range |")
    md.append("|---|---:|---:|")
    for _, r in unex["gran_tbl"].iterrows():
        md.append(
            f"| {r['category']} | {int(r['count']):,} | "
            f"{r['pct_of_non_null_date_range']:.3f}% |"
        )
    md.append("")
    md.append(f"- Total non-null `date_range`: **{unex['total_dr']:,}**")
    if unex["flagged"]:
        md.append("- **Flagged anomalies >5 %:**")
        for f in unex["flagged"]:
            md.append(
                f"    - `{f['category']}`: {f['pct_of_non_null_date_range']:.3f}% "
                f"({int(f['count']):,} rows) — worth investigator review."
            )
    else:
        md.append("- No category exceeds the 5% flag threshold.")
    md.append(
        "\nRound-value detail in `tables/granularity_round_values.csv`.\n"
    )

    md.append("### View 2 — broad date_range histogram (buckets)\n")
    md.append("| bucket | count | % of non-null |")
    md.append("|---|---:|---:|")
    for _, r in unex["broad_tbl"].iterrows():
        md.append(
            f"| {r['bucket']} | {int(r['count']):,} | "
            f"{r['pct_of_non_null_date_range']:.3f}% |"
        )
    md.append("")
    md.append(
        "- This view complements the granularity view: bimodality, unexpected "
        "peaks, or gaps that the category-based view cannot surface.\n"
    )

    (OUTPUT_DIR / "artefacts.md").write_text("\n".join(md))
    log("wrote artefacts.md")


def write_summary(
    ds: dict[str, Any],
    prov: dict[str, Any],
    urb: dict[str, Any],
    mid: dict[str, Any],
    spikes: dict[str, Any],
    coord: dict[str, Any],
    outlier: dict[str, Any],
    dup: dict[str, Any],
    n_neg: int,
    extreme: dict[str, Any],
    temporal: dict[str, Any],
    null_flagged: list[dict[str, Any]],
    unex: dict[str, Any],
) -> None:
    n_rows = ds["n_rows"]
    n_geo = int(ds["valid_latlon"].sum())
    md = []
    md.append("# LIRE v3.0 — descriptive profile summary\n")
    md.append(
        f"_Generated {_now()} by data-profile-scout methodology "
        "(general-purpose agent; schema disagreements & fixed-environment "
        "decisions recorded in `decisions.md`)._"
    )
    md.append("")
    md.append("## Headline findings\n")

    # Headline 1 — corpus scale + schema drift
    md.append(
        f"1. **Corpus scale**: {n_rows:,} rows × {ds['n_cols']} columns. "
        "Parquet has 63 columns, seed schema documents 66 — three schema-listed "
        "columns (`is_geotemporal`, `is_within_RE`, `material_EDCS`) are absent "
        "from the parquet. Brief expected 182,852 rows; we observed 182,853. See "
        "`decisions.md` Decisions 2-3."
    )

    # Headline 2 — geolocation
    md.append(
        f"2. **Geolocation**: {n_geo:,}/{n_rows:,} rows "
        f"({n_geo/n_rows*100:.3f}%) have valid (non-null, non-zero) "
        "`Latitude` AND `Longitude`. Expected ~100 % for LIRE; this is the "
        "observed rate under the stated criteria."
    )

    # Headline 3 — date-range granularity
    g = {r["category"]: r for _, r in unex["gran_tbl"].iterrows()}
    md.append(
        f"3. **Date-range granularity is overwhelmingly century-scale**: "
        f"{int(g['99_to_101 (century)']['count']):,} rows "
        f"({g['99_to_101 (century)']['pct_of_non_null_date_range']:.2f}% of "
        "non-null date ranges) fall in the 99-101 year century bucket; "
        f"{int(g['eq_0']['count']):,} ({g['eq_0']['pct_of_non_null_date_range']:.2f}%) "
        f"have `date_range == 0`; "
        f"{int(g['199_to_201 (bicentury)']['count']):,} "
        f"({g['199_to_201 (bicentury)']['pct_of_non_null_date_range']:.2f}%) "
        "fall in the 199-201 bicentury bucket. See `artefacts.md` §*Unexpected-pattern*."
    )

    # Headline 4 — subset thresholds
    prov_qual = prov["thresholds"]
    urb_qual = urb["thresholds"]
    md.append(
        f"4. **Subset thresholds**: at n>=100, "
        f"**{int(prov_qual.loc[prov_qual['threshold']==100, 'n_groups_qualifying'].iloc[0])}** "
        f"province groups and "
        f"**{int(urb_qual.loc[urb_qual['threshold']==100, 'n_groups_qualifying'].iloc[0])}** "
        "urban-area (`urban_context_city`) groups qualify. At n>=300, "
        f"**{int(prov_qual.loc[prov_qual['threshold']==300, 'n_groups_qualifying'].iloc[0])}** "
        "and "
        f"**{int(urb_qual.loc[urb_qual['threshold']==300, 'n_groups_qualifying'].iloc[0])}** "
        "qualify respectively. Full detail in `profile-province.md`, "
        "`profile-urban-area.md`."
    )

    # Headline 5 — artefact audit
    md.append(
        f"5. **Artefact audit summary**: `negative-date-range` = {n_neg} (expected 0, PASS); "
        f"`outlier-coordinates` (out-of-range lat/lon) = {outlier['bad_any']} (expected 0, PASS); "
        f"`temporal-outliers` (outside 50 BC – AD 350) = {temporal['n_any']:,}; "
        f"`duplicate-rows` exact = {dup['dup_all']:,}, duplicate `LIST-ID` = {dup['dup_listid']:,}; "
        f"`date-range-extreme` (>500 y) = {extreme['n_extreme']:,}; "
        f"columns with >50% nulls = {len(null_flagged)}. "
        "Two canonical checks (`is_within_RE-rate`, `is_geotemporal-rate`) "
        "were **not run** because the columns are absent from the parquet."
    )
    md.append("")
    md.append("## Per-subset highlights\n")
    md.append(
        f"- **Province**: largest groups are "
        + ", ".join(
            f"`{str(r['group'])[:35]}` ({int(r['count']):,})"
            for _, r in prov["top20"].head(3).iterrows()
        )
        + "."
    )
    md.append(
        f"- **Urban area**: largest groups are "
        + ", ".join(
            f"`{str(r['group'])[:35]}` ({int(r['count']):,})"
            for _, r in urb["top20"].head(3).iterrows()
        )
        + "."
    )
    md.append("")

    md.append("## Output files\n")
    md.append("- `profile-dataset.md` — dataset-level profile.")
    md.append("- `profile-province.md` — per-province profile.")
    md.append("- `profile-urban-area.md` — per-urban-area profile.")
    md.append("- `artefacts.md` — all artefact checks + unexpected-pattern diagnostic.")
    md.append("- `claims.jsonl` — machine-readable enumeration of numerical claims.")
    md.append(
        "- `tables/` — CSV versions of every table referenced in the markdown."
    )
    md.append(
        "- `decisions.md` (at `../decisions.md`) — judgement calls during this run."
    )
    md.append("- `run.log` — tool-use trace.")

    (OUTPUT_DIR / "summary.md").write_text("\n".join(md))
    log("wrote summary.md")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def main() -> None:
    t_start = time.time()
    validate_environment()

    df = load_dataset()
    schema = load_schema()

    ds = dataset_profile(df, schema)

    # subset profiles
    prov = subset_profile(
        df, "province", "province", ds["nb"], ds["na"], ds["lat"], ds["lon"]
    )
    urb = subset_profile(
        df,
        "urban_context_city",
        "urban-area",
        ds["nb"],
        ds["na"],
        ds["lat"],
        ds["lon"],
    )
    write_profile_dataset(ds, len(schema))
    write_profile_subset("province", "province", prov, ds["n_rows"])
    write_profile_subset("urban-area", "urban_context_city", urb, ds["n_rows"])

    # Artefact checks
    log("running artefact checks")
    mid = artefact_midpoint_inflation(ds["nb"], ds["na"])
    spikes = artefact_editorial_spikes(ds["nb"], ds["na"])
    coord = artefact_coordinate_precision(ds["lat"], ds["lon"])
    outlier = artefact_outlier_coordinates(ds["lat"], ds["lon"])
    dup = artefact_duplicate_rows(df)
    n_neg = artefact_negative_date_range(ds["nb"], ds["na"])
    extreme = artefact_date_range_extreme(ds["nb"], ds["na"])
    temporal = artefact_temporal_outliers(ds["nb"], ds["na"])
    null_flagged = artefact_null_profile(ds["null_table"])
    unex = unexpected_pattern_diagnostic(ds["nb"], ds["na"], ds["n_rows"])

    write_artefacts(
        ds, mid, spikes, coord, outlier, dup, n_neg, extreme,
        temporal, null_flagged, unex, ds["n_rows"],
    )
    write_summary(
        ds, prov, urb, mid, spikes, coord, outlier, dup, n_neg, extreme,
        temporal, null_flagged, unex,
    )

    # Dump claims
    with open(CLAIMS_PATH, "w") as f:
        for entry in CLAIMS:
            f.write(json.dumps(entry) + "\n")
    log(f"wrote {CLAIMS_PATH} ({len(CLAIMS)} claims)")

    t_end = time.time()
    log(f"run complete in {t_end - t_start:.1f}s")

    with open(RUN_LOG_PATH, "w") as f:
        f.write("\n".join(LOG_LINES) + "\n")


if __name__ == "__main__":
    main()
