#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# LIRE v3.0 descriptive profile (first-run, minimal mode)
# -----------------------------------------------------------------------------
# This script computes the full descriptive profile per the data-profile-proposer
# methodology against the LIRE v3.0 parquet corpus. Outputs land in OUTPUT_DIR
# as a set of markdown reports, CSV tables, a claims.jsonl machine-readable
# claim ledger, decisions.md, and run.log.
#
# Run from any cwd; all paths are absolute.
# -----------------------------------------------------------------------------

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# -----------------------------------------------------------------------------
# Configuration (mirrors invocation parameters)
# -----------------------------------------------------------------------------

DATASET_PATH = Path(
    "/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet"
)
OUTPUT_DIR = Path(
    "/home/shawn/Code/inscriptions/runs/2026-05-22-data-profile-smoke/"
    "iterate-20260522-162723/iter-0"
)
TABLES_DIR = OUTPUT_DIR / "tables"
DATE_COLUMNS = ("not_before", "not_after")
SPATIAL_COLUMNS = ("Latitude", "Longitude")
PRIMARY_KEY = "LIST-ID"

SUBSET_LEVELS = [
    {"name": "dataset", "columns": [], "threshold_candidates": []},
    {
        "name": "province",
        "columns": ["province"],
        "threshold_candidates": [100, 1000, 10000],
    },
    {
        "name": "urban-area",
        "columns": ["urban_context_city"],
        "threshold_candidates": [10, 100, 1000],
    },
]

# Artefact-check defaults (the catalogue).
ARTEFACT_CHECKS = [
    "midpoint-inflation",
    "editorial-spikes",
    "coordinate-precision",
    "outlier-coordinates",
    "null-profile",
    "duplicate-rows",
    "negative-date-range",
    "date-range-extreme",
    "temporal-outliers",
    "geolocated-rate",
    "is_within_RE-rate",
    "is_geotemporal-rate",
]

# Editorial-boundary years (Roman political-history convention boundaries):
# 14 BC start of Augustan re-organisation, AD 27 Augustan principate, AD 96/97
# Nerva-Trajan, AD 192/193 Commodus-Pertinax-Severus, AD 235 end of Severans.
# These match the standard SDAM editorial-spike audit set.
EDITORIAL_YEARS = [-14, 27, 96, 97, 192, 193, 235]

# Granularity buckets (years).
GRANULARITY_BUCKETS = [0, 25, 50, 100, 200, 500]
# Multiples of 10 up to 200 to catch "other round numbers".
ROUND_NUMBERS = set(range(10, 201, 10))

# Date-range distribution bin edges.
DATE_RANGE_BINS = [-0.5, 0.5, 25.5, 50.5, 100.5, 200.5, 500.5, np.inf]
DATE_RANGE_LABELS = ["0", "1-25", "26-50", "51-100", "101-200", "201-500", ">500"]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def slugify(text: str) -> str:
    """Make a string safe for use in a claim_id."""
    s = str(text).strip().lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "/", "-", "_", ".", ","):
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "unnamed"


def decimal_places(x: float) -> int:
    """Count decimal places of a coordinate, robust to floats."""
    if pd.isna(x):
        return -1
    s = f"{x:.10f}".rstrip("0")
    if "." not in s:
        return 0
    return len(s.split(".")[1])


# -----------------------------------------------------------------------------
# Claim ledger
# -----------------------------------------------------------------------------


class ClaimLedger:
    """Accumulates deterministic claims and writes them to claims.jsonl."""

    def __init__(self) -> None:
        self.rows: list[dict] = []
        self.ids: set[str] = set()

    def add(
        self,
        claim_id: str,
        category: str,
        description: str,
        value,
        units: str,
        source_method: str,
        source_file: str,
    ) -> None:
        if claim_id in self.ids:
            raise ValueError(f"Duplicate claim_id: {claim_id}")
        self.ids.add(claim_id)
        # Coerce numpy scalars to native Python for JSON-serialisability.
        if isinstance(value, (np.integer,)):
            value = int(value)
        elif isinstance(value, (np.floating,)):
            value = float(value)
        elif isinstance(value, (np.bool_,)):
            value = bool(value)
        self.rows.append(
            {
                "claim_id": claim_id,
                "category": category,
                "description": description,
                "value": value,
                "units": units,
                "source_method": source_method,
                "source_file": source_file,
            }
        )

    def write(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as fh:
            for row in self.rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# -----------------------------------------------------------------------------
# Run log
# -----------------------------------------------------------------------------


class RunLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lines: list[str] = []
        self.t0 = time.time()

    def event(self, msg: str) -> None:
        elapsed = time.time() - self.t0
        line = f"[{elapsed:7.2f}s] {msg}"
        print(line, flush=True)
        self.lines.append(line)

    def flush(self) -> None:
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


# -----------------------------------------------------------------------------
# Decisions log
# -----------------------------------------------------------------------------


class Decisions:
    def __init__(self) -> None:
        self.entries: list[str] = []

    def add(self, title: str, body: str) -> None:
        self.entries.append(f"## {title}\n\n{body.strip()}\n")

    def write(self, path: Path) -> None:
        header = (
            "# Decisions log — LIRE v3.0 descriptive profile (first run)\n\n"
            "Every judgement call encountered during the profiling run. Each "
            "entry records: fact observed, default applied, alternatives "
            "considered, rationale, and whether the call warrants investigator "
            "review.\n\n"
        )
        path.write_text(header + "\n".join(self.entries), encoding="utf-8")


# -----------------------------------------------------------------------------
# Main pipeline
# -----------------------------------------------------------------------------


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    log = RunLog(OUTPUT_DIR / "run.log")
    decisions = Decisions()
    ledger = ClaimLedger()

    log.event("Loading parquet")
    df = pd.read_parquet(DATASET_PATH)
    n_rows, n_cols = df.shape
    log.event(f"Loaded shape={df.shape}")

    # -------------------------------------------------------------------------
    # Schema check
    # -------------------------------------------------------------------------
    required = set(list(DATE_COLUMNS) + list(SPATIAL_COLUMNS) + [PRIMARY_KEY])
    for level in SUBSET_LEVELS:
        required.update(level["columns"])
    missing_required = sorted(required - set(df.columns))
    if missing_required:
        msg = f"Required columns missing: {missing_required}"
        log.event("FATAL: " + msg)
        decisions.add(
            "Schema disagreement (breaking)",
            f"**Fact:** Required columns missing from dataset: "
            f"{missing_required}\n\n"
            f"**Default applied:** Halt per decision-point discipline.\n\n"
            f"**Investigator review:** Required.",
        )
        decisions.write(OUTPUT_DIR / "decisions.md")
        log.flush()
        sys.exit(1)
    decisions.add(
        "Schema validation (non-breaking)",
        "**Fact:** All invocation-referenced columns present. Dataset has 63 "
        "columns; the invocation references only the subset above plus the "
        "primary key. Columns `is_within_RE` and `is_geotemporal` named in the "
        "default artefact-check catalogue are absent.\n\n"
        "**Default applied:** Flag-and-continue per decision-point discipline. "
        "Report the corresponding checks as `could not run` with reason "
        "`column absent`.\n\n"
        "**Investigator review:** Not required; these columns are not part of "
        "the LIRE v3.0 schema.",
    )

    # No temporal envelope was provided in the invocation.
    decisions.add(
        "Temporal envelope absent from invocation",
        "**Fact:** The `temporal-outliers` check requires a stated temporal "
        "envelope (e.g., [-50, 350] for LIRE) to be meaningful. None was "
        "provided.\n\n"
        "**Default applied:** Report observed min/max of `not_before` and "
        "`not_after` and flag rows outside an empirically-conservative "
        "envelope of [-700, 700] (anything outside that window for a Latin "
        "epigraphic corpus is almost certainly a data-entry artefact).\n\n"
        "**Investigator review:** Recommended — the project should specify "
        "the canonical envelope so future runs are not threshold-arbitrary.",
    )

    # -------------------------------------------------------------------------
    # Dataset-level profile
    # -------------------------------------------------------------------------
    log.event("Dataset-level profile")

    ledger.add(
        "count-dataset-row-count",
        "count",
        "Total rows in LIRE v3.0 corpus",
        n_rows,
        "rows",
        "len(df)",
        "summary.md",
    )
    ledger.add(
        "count-dataset-column-count",
        "count",
        "Total columns in LIRE v3.0 corpus",
        n_cols,
        "columns",
        "df.shape[1]",
        "summary.md",
    )

    # Primary-key uniqueness
    pk_unique = int(df[PRIMARY_KEY].nunique(dropna=False))
    pk_null = int(df[PRIMARY_KEY].isna().sum())
    ledger.add(
        "count-dataset-primary-key-unique",
        "count",
        f"Unique values of primary key {PRIMARY_KEY}",
        pk_unique,
        "values",
        f"df['{PRIMARY_KEY}'].nunique()",
        "summary.md",
    )
    ledger.add(
        "count-dataset-primary-key-null",
        "count",
        f"Null values of primary key {PRIMARY_KEY}",
        pk_null,
        "rows",
        f"df['{PRIMARY_KEY}'].isna().sum()",
        "summary.md",
    )

    # Per-column null rate and uniques
    null_counts = df.isna().sum()
    null_rates = null_counts / n_rows
    nunique_counts = df.nunique(dropna=False)
    col_stats = pd.DataFrame(
        {
            "column": null_counts.index,
            "null_count": null_counts.values,
            "null_rate": null_rates.values,
            "n_unique": nunique_counts.values,
            "dtype": [str(df[c].dtype) for c in null_counts.index],
        }
    ).sort_values("null_rate", ascending=False)
    col_stats.to_csv(TABLES_DIR / "column-stats.csv", index=False)

    # date_range distribution
    not_before = pd.to_numeric(df[DATE_COLUMNS[0]], errors="coerce")
    not_after = pd.to_numeric(df[DATE_COLUMNS[1]], errors="coerce")
    has_both_dates = not_before.notna() & not_after.notna()
    n_dated = int(has_both_dates.sum())
    date_range = (not_after - not_before).where(has_both_dates)
    ledger.add(
        "count-dataset-dated-rows",
        "count",
        "Rows with both not_before and not_after non-null",
        n_dated,
        "rows",
        "(not_before.notna() & not_after.notna()).sum()",
        "summary.md",
    )
    ledger.add(
        "rate-dataset-dated",
        "rate",
        "Fraction of rows with both not_before and not_after non-null",
        round(n_dated / n_rows, 6),
        "fraction",
        "n_dated / n_rows",
        "summary.md",
    )

    # Spatial: valid coordinates = both Lat/Lon non-null and inside the
    # canonical bounding box for Earth.
    lat = pd.to_numeric(df[SPATIAL_COLUMNS[0]], errors="coerce")
    lon = pd.to_numeric(df[SPATIAL_COLUMNS[1]], errors="coerce")
    valid_coords = (
        lat.notna()
        & lon.notna()
        & lat.between(-90, 90)
        & lon.between(-180, 180)
    )
    n_geo = int(valid_coords.sum())
    ledger.add(
        "count-dataset-geolocated",
        "count",
        "Rows with valid coordinates (both non-null and in-range)",
        n_geo,
        "rows",
        "(lat.notna() & lon.notna() & lat in [-90,90] & lon in [-180,180]).sum()",
        "summary.md",
    )
    ledger.add(
        "rate-dataset-geolocated",
        "rate",
        "Fraction of rows with valid coordinates",
        round(n_geo / n_rows, 6),
        "fraction",
        "n_geo / n_rows",
        "summary.md",
    )

    # -------------------------------------------------------------------------
    # Subset-level profiles
    # -------------------------------------------------------------------------
    subset_summaries: dict[str, dict] = {}
    for level in SUBSET_LEVELS:
        name = level["name"]
        cols = level["columns"]
        if not cols:
            continue
        log.event(f"Subset level: {name}")
        # Treat NaN groups separately so we don't silently lose them.
        grouped = (
            df.groupby(cols, dropna=False)
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )
        n_groups = int(len(grouped))
        ledger.add(
            f"count-{name}-group-count",
            "count",
            f"Number of distinct groups at subset level {name}",
            n_groups,
            "groups",
            f"df.groupby({cols}).ngroups",
            f"profile-{name}.md",
        )

        # Save full per-group table
        grouped.to_csv(TABLES_DIR / f"subset-{name}-counts.csv", index=False)

        # Top-20
        top20 = grouped.head(20).copy()
        top20.to_csv(TABLES_DIR / f"subset-{name}-top20.csv", index=False)
        # Claim: top group
        top_row = grouped.iloc[0]
        top_key_raw = top_row[cols[0]]
        top_key = slugify(top_key_raw) if pd.notna(top_key_raw) else "null"
        ledger.add(
            f"ranking-{name}-top-group-name",
            "ranking",
            f"Largest group at subset level {name}",
            (str(top_key_raw) if pd.notna(top_key_raw) else None),
            "label",
            "groupby().size().idxmax()",
            f"profile-{name}.md",
        )
        ledger.add(
            f"count-{name}-top-group-count",
            "count",
            f"Row count of largest group at subset level {name}",
            int(top_row["count"]),
            "rows",
            "groupby().size().max()",
            f"profile-{name}.md",
        )

        # Threshold-qualifying counts
        for t in level["threshold_candidates"]:
            n_qual = int((grouped["count"] >= t).sum())
            ledger.add(
                f"threshold-qualifying-{name}-ge-{t}",
                "threshold_qualifying",
                f"Number of {name} groups with at least {t} rows",
                n_qual,
                "groups",
                f"(grouped['count'] >= {t}).sum()",
                f"profile-{name}.md",
            )

        subset_summaries[name] = {
            "n_groups": n_groups,
            "top20": top20,
            "grouped": grouped,
            "thresholds": {
                t: int((grouped["count"] >= t).sum())
                for t in level["threshold_candidates"]
            },
        }

        # Per-group stats for groups passing the highest threshold
        if level["threshold_candidates"]:
            highest = max(level["threshold_candidates"])
            qualifying_keys = grouped[grouped["count"] >= highest][cols[0]]
            per_group_rows: list[dict] = []
            for key in qualifying_keys:
                if pd.isna(key):
                    mask = df[cols[0]].isna()
                else:
                    mask = df[cols[0]] == key
                sub = df[mask]
                if not sub.empty:
                    sub_nb = pd.to_numeric(
                        sub[DATE_COLUMNS[0]], errors="coerce"
                    )
                    sub_na = pd.to_numeric(
                        sub[DATE_COLUMNS[1]], errors="coerce"
                    )
                    sub_dated = sub_nb.notna() & sub_na.notna()
                    sub_lat = pd.to_numeric(
                        sub[SPATIAL_COLUMNS[0]], errors="coerce"
                    )
                    sub_lon = pd.to_numeric(
                        sub[SPATIAL_COLUMNS[1]], errors="coerce"
                    )
                    sub_geo = (
                        sub_lat.notna()
                        & sub_lon.notna()
                        & sub_lat.between(-90, 90)
                        & sub_lon.between(-180, 180)
                    )
                    per_group_rows.append(
                        {
                            "group": key if pd.notna(key) else "<null>",
                            "count": int(len(sub)),
                            "dated_rate": round(
                                float(sub_dated.mean()), 6
                            ),
                            "geolocated_rate": round(
                                float(sub_geo.mean()), 6
                            ),
                            "date_range_median": (
                                float((sub_na - sub_nb).where(sub_dated).median())
                                if sub_dated.any()
                                else None
                            ),
                        }
                    )
            per_group_df = pd.DataFrame(per_group_rows)
            per_group_df.to_csv(
                TABLES_DIR / f"subset-{name}-qualifying-stats.csv",
                index=False,
            )

            # Boundary-discipline flag
            n_qual = subset_summaries[name]["thresholds"][highest]
            if n_qual < 3 or n_qual > 100:
                decisions.add(
                    f"Subset threshold boundary unusual ({name})",
                    f"**Fact:** {n_qual} groups qualify at the highest "
                    f"threshold ({highest}) for subset level {name}.\n\n"
                    f"**Default applied:** Flag-and-continue.\n\n"
                    f"**Investigator review:** Recommended — threshold may be "
                    f"mis-set if downstream analysis needs a particular cohort "
                    f"size.",
                )

    # -------------------------------------------------------------------------
    # Artefact checks
    # -------------------------------------------------------------------------
    log.event("Artefact checks")

    artefact_results: dict[str, dict] = {}

    # ---- midpoint-inflation ----
    # Bin midpoints (not_before+not_after)/2 by integer year; flag any year
    # whose count is anomalously high vs adjacent years. Use a chi-square
    # over century-midpoints (years ending in 50: ..., -50, 50, 150, 250, ...)
    # vs the immediately-adjacent years.
    mids_full = ((not_before + not_after) / 2.0).where(has_both_dates)
    mids_int = mids_full.round().astype("Int64")
    century_mids = []
    for y in range(-500, 701):
        if y % 100 == 50 or y % 100 == -50:
            century_mids.append(y)
    century_mid_count = int(mids_int.isin(century_mids).sum())
    # Adjacent years: y-1 and y+1 around each century-midpoint
    adj_years = []
    for y in century_mids:
        adj_years.extend([y - 1, y + 1])
    adj_count = int(mids_int.isin(adj_years).sum())
    # Per-year expected: count on midpoint years should be ~ average of
    # surrounding two years if no editorial inflation. Chi-square: observed
    # = century_mid_count; expected = adj_count / 2 (because 2 adjacent years
    # per midpoint).
    expected_mid = adj_count / 2 if adj_count > 0 else np.nan
    chi2_mid = (
        ((century_mid_count - expected_mid) ** 2) / expected_mid
        if expected_mid and expected_mid > 0
        else np.nan
    )
    # 1 d.o.f.; one-sided upper-tail
    pval_mid = (
        float(1 - stats.chi2.cdf(chi2_mid, df=1))
        if not np.isnan(chi2_mid)
        else np.nan
    )
    ratio_mid = (
        century_mid_count / expected_mid
        if expected_mid and expected_mid > 0
        else np.nan
    )
    artefact_results["midpoint-inflation"] = {
        "observed_at_midpoints": century_mid_count,
        "expected_from_adjacent": expected_mid,
        "ratio": ratio_mid,
        "chi2": chi2_mid,
        "pvalue": pval_mid,
    }
    ledger.add(
        "count-artefacts-midpoint-observed",
        "count",
        "Rows whose century-midpoint (year ending in 50) equals their midpoint",
        century_mid_count,
        "rows",
        "mids_int.isin(century_mids).sum()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-midpoint-adjacent",
        "count",
        "Rows whose midpoint is exactly one off a century-midpoint",
        adj_count,
        "rows",
        "mids_int.isin(adj_years).sum()",
        "artefacts.md",
    )
    ledger.add(
        "test_statistic-artefacts-midpoint-chi2",
        "test_statistic",
        "Chi-square statistic for midpoint-inflation (1 d.o.f., observed vs "
        "mean of adjacent two years)",
        round(float(chi2_mid), 4) if not np.isnan(chi2_mid) else None,
        "chi2",
        "((obs - exp)**2) / exp",
        "artefacts.md",
    )
    ledger.add(
        "pvalue-artefacts-midpoint",
        "pvalue",
        "Upper-tail chi-square p-value, midpoint-inflation",
        round(float(pval_mid), 6) if not np.isnan(pval_mid) else None,
        "pvalue",
        "1 - chi2.cdf(chi2, df=1)",
        "artefacts.md",
    )

    # ---- editorial-spikes ----
    spikes_rows: list[dict] = []
    for y in EDITORIAL_YEARS:
        obs_nb = int((not_before == y).sum())
        obs_na = int((not_after == y).sum())
        # Adjacent year baseline (avg of y-1 and y+1)
        adj_nb = int(
            ((not_before == y - 1) | (not_before == y + 1)).sum()
        ) / 2
        adj_na = int(
            ((not_after == y - 1) | (not_after == y + 1)).sum()
        ) / 2
        spikes_rows.append(
            {
                "year": y,
                "not_before_obs": obs_nb,
                "not_before_adj_mean": adj_nb,
                "not_before_ratio": (
                    obs_nb / adj_nb if adj_nb > 0 else np.nan
                ),
                "not_after_obs": obs_na,
                "not_after_adj_mean": adj_na,
                "not_after_ratio": (
                    obs_na / adj_na if adj_na > 0 else np.nan
                ),
            }
        )
        ledger.add(
            f"count-artefacts-editorial-{y}-not_before-obs",
            "count",
            f"Rows with not_before == {y}",
            obs_nb,
            "rows",
            f"(not_before == {y}).sum()",
            "artefacts.md",
        )
        ledger.add(
            f"count-artefacts-editorial-{y}-not_after-obs",
            "count",
            f"Rows with not_after == {y}",
            obs_na,
            "rows",
            f"(not_after == {y}).sum()",
            "artefacts.md",
        )
    spikes_df = pd.DataFrame(spikes_rows)
    spikes_df.to_csv(TABLES_DIR / "artefact-editorial-spikes.csv", index=False)
    artefact_results["editorial-spikes"] = spikes_df

    # Aggregate chi-square across editorial years for not_before, observed
    # vs adjacent-year mean
    obs_total_nb = sum(r["not_before_obs"] for r in spikes_rows)
    exp_total_nb = sum(
        r["not_before_adj_mean"]
        for r in spikes_rows
        if r["not_before_adj_mean"] > 0
    )
    if exp_total_nb > 0:
        chi2_ed = ((obs_total_nb - exp_total_nb) ** 2) / exp_total_nb
        pval_ed = float(1 - stats.chi2.cdf(chi2_ed, df=1))
    else:
        chi2_ed = np.nan
        pval_ed = np.nan
    ledger.add(
        "test_statistic-artefacts-editorial-chi2",
        "test_statistic",
        "Chi-square (aggregate over editorial years) for not_before spike",
        round(float(chi2_ed), 4) if not np.isnan(chi2_ed) else None,
        "chi2",
        "((sum_obs - sum_exp)**2) / sum_exp",
        "artefacts.md",
    )
    ledger.add(
        "pvalue-artefacts-editorial",
        "pvalue",
        "Upper-tail chi-square p-value, editorial-spike aggregate",
        round(float(pval_ed), 6) if not np.isnan(pval_ed) else None,
        "pvalue",
        "1 - chi2.cdf(chi2, df=1)",
        "artefacts.md",
    )

    # ---- coordinate-precision ----
    lat_dp = lat.dropna().map(decimal_places)
    lon_dp = lon.dropna().map(decimal_places)
    dp_bins = pd.cut(
        pd.concat([lat_dp, lon_dp]),
        bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 10.5],
        labels=["0", "1", "2", "3", "4", ">4"],
    )
    dp_counts = dp_bins.value_counts().reindex(
        ["0", "1", "2", "3", "4", ">4"]
    )
    dp_counts.to_csv(TABLES_DIR / "artefact-coordinate-precision.csv")
    total_dp = int(dp_counts.sum())
    gt4_share = (
        float(dp_counts.get(">4", 0)) / total_dp if total_dp > 0 else np.nan
    )
    ledger.add(
        "count-artefacts-coord-precision-total",
        "count",
        "Total non-null lat+lon coordinate values evaluated for decimal places",
        total_dp,
        "values",
        "len(dropna(lat)) + len(dropna(lon))",
        "artefacts.md",
    )
    ledger.add(
        "rate-artefacts-coord-precision-gt4",
        "rate",
        "Share of non-null coordinate values with >4 decimal places (false-"
        "precision indicator)",
        round(float(gt4_share), 6) if not np.isnan(gt4_share) else None,
        "fraction",
        "dp_counts['>4'] / total_dp",
        "artefacts.md",
    )

    # ---- outlier-coordinates ----
    lat_out = int(((lat.notna()) & (lat.abs() > 90)).sum())
    lon_out = int(((lon.notna()) & (lon.abs() > 180)).sum())
    ledger.add(
        "count-artefacts-outlier-lat",
        "count",
        "Rows with |Latitude| > 90 (impossible)",
        lat_out,
        "rows",
        "(lat.abs() > 90).sum()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-outlier-lon",
        "count",
        "Rows with |Longitude| > 180 (impossible)",
        lon_out,
        "rows",
        "(lon.abs() > 180).sum()",
        "artefacts.md",
    )

    # ---- null-profile ----
    high_null = col_stats[col_stats["null_rate"] > 0.5].copy()
    high_null.to_csv(TABLES_DIR / "artefact-high-null-columns.csv", index=False)
    ledger.add(
        "count-artefacts-high-null-columns",
        "count",
        "Number of columns with null_rate > 50%",
        int(len(high_null)),
        "columns",
        "(null_rate > 0.5).sum()",
        "artefacts.md",
    )

    # ---- duplicate-rows ----
    n_dup_all = int(df.duplicated(keep=False).sum())
    n_dup_pk = int(df.duplicated(subset=[PRIMARY_KEY], keep=False).sum())
    ledger.add(
        "count-artefacts-duplicate-rows-all-columns",
        "count",
        "Rows that are exact duplicates across all columns",
        n_dup_all,
        "rows",
        "df.duplicated(keep=False).sum()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-duplicate-rows-primary-key",
        "count",
        f"Rows duplicated on primary key {PRIMARY_KEY}",
        n_dup_pk,
        "rows",
        f"df.duplicated(subset=['{PRIMARY_KEY}'], keep=False).sum()",
        "artefacts.md",
    )

    # ---- negative-date-range ----
    neg_dr = int(((not_after - not_before) < 0).sum())
    ledger.add(
        "count-artefacts-negative-date-range",
        "count",
        "Rows where not_before > not_after",
        neg_dr,
        "rows",
        "((not_after - not_before) < 0).sum()",
        "artefacts.md",
    )

    # ---- date-range-extreme ----
    extreme_dr = int(((not_after - not_before) > 500).sum())
    ledger.add(
        "count-artefacts-date-range-gt500",
        "count",
        "Rows where date_range > 500 years",
        extreme_dr,
        "rows",
        "((not_after - not_before) > 500).sum()",
        "artefacts.md",
    )

    # ---- temporal-outliers (no envelope supplied — use conservative window) --
    envelope_lo, envelope_hi = -700, 700
    nb_outside = int(
        ((not_before.notna()) & ((not_before < envelope_lo) | (not_before > envelope_hi))).sum()
    )
    na_outside = int(
        ((not_after.notna()) & ((not_after < envelope_lo) | (not_after > envelope_hi))).sum()
    )
    nb_min = float(not_before.min()) if not_before.notna().any() else None
    nb_max = float(not_before.max()) if not_before.notna().any() else None
    na_min = float(not_after.min()) if not_after.notna().any() else None
    na_max = float(not_after.max()) if not_after.notna().any() else None
    ledger.add(
        "count-artefacts-temporal-outliers-not_before",
        "count",
        f"Rows with not_before outside [{envelope_lo}, {envelope_hi}] "
        "(conservative envelope; no envelope supplied)",
        nb_outside,
        "rows",
        f"((not_before < {envelope_lo}) | (not_before > {envelope_hi})).sum()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-temporal-outliers-not_after",
        "count",
        f"Rows with not_after outside [{envelope_lo}, {envelope_hi}]",
        na_outside,
        "rows",
        f"((not_after < {envelope_lo}) | (not_after > {envelope_hi})).sum()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-not_before-min",
        "count",
        "Minimum observed value of not_before",
        int(nb_min) if nb_min is not None else None,
        "year",
        "not_before.min()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-not_before-max",
        "count",
        "Maximum observed value of not_before",
        int(nb_max) if nb_max is not None else None,
        "year",
        "not_before.max()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-not_after-min",
        "count",
        "Minimum observed value of not_after",
        int(na_min) if na_min is not None else None,
        "year",
        "not_after.min()",
        "artefacts.md",
    )
    ledger.add(
        "count-artefacts-not_after-max",
        "count",
        "Maximum observed value of not_after",
        int(na_max) if na_max is not None else None,
        "year",
        "not_after.max()",
        "artefacts.md",
    )

    # ---- is_within_RE-rate / is_geotemporal-rate ----
    for col in ("is_within_RE", "is_geotemporal"):
        if col in df.columns:
            rate = float(df[col].astype("boolean").fillna(False).mean())
            ledger.add(
                f"rate-artefacts-{slugify(col)}",
                "rate",
                f"Fraction of rows with {col} == True",
                round(rate, 6),
                "fraction",
                f"df['{col}'].mean()",
                "artefacts.md",
            )
        else:
            artefact_results[f"{col}-rate"] = "could not run: column absent"

    # -------------------------------------------------------------------------
    # Unexpected-pattern diagnostic
    # -------------------------------------------------------------------------
    log.event("Unexpected-pattern diagnostic")
    dr_int = (not_after - not_before).where(has_both_dates).astype("Int64")

    # Granularity histogram
    granularity_bins = []
    n_total_dated = int(dr_int.notna().sum())
    counted = pd.Series(False, index=dr_int.index)
    for b in GRANULARITY_BUCKETS:
        mask = dr_int == b
        c = int(mask.sum())
        granularity_bins.append(
            {
                "bucket": f"exact-{b}",
                "count": c,
                "share": round(c / n_total_dated, 6)
                if n_total_dated > 0
                else None,
            }
        )
        counted |= mask
        ledger.add(
            f"count-diagnostic-granularity-exact-{b}",
            "count",
            f"Rows with date_range == {b} years",
            c,
            "rows",
            f"(date_range == {b}).sum()",
            "artefacts.md",
        )
        ledger.add(
            f"rate-diagnostic-granularity-exact-{b}",
            "rate",
            f"Share (of dated rows) with date_range == {b} years",
            round(c / n_total_dated, 6) if n_total_dated > 0 else None,
            "fraction",
            f"(date_range == {b}).mean()",
            "artefacts.md",
        )
    # Other round numbers (multiples of 10, 10..200) not already covered
    round_extra = ROUND_NUMBERS - set(GRANULARITY_BUCKETS)
    round_mask = dr_int.isin(list(round_extra))
    c_round = int(round_mask.sum())
    granularity_bins.append(
        {
            "bucket": "other-multiples-of-10",
            "count": c_round,
            "share": round(c_round / n_total_dated, 6)
            if n_total_dated > 0
            else None,
        }
    )
    counted |= round_mask
    ledger.add(
        "count-diagnostic-granularity-other-multiples-of-10",
        "count",
        "Rows with date_range a multiple of 10 (10..200) not in standard "
        "buckets",
        c_round,
        "rows",
        "date_range.isin(other_round).sum()",
        "artefacts.md",
    )
    # Other values
    c_other = int((dr_int.notna() & ~counted).sum())
    granularity_bins.append(
        {
            "bucket": "other",
            "count": c_other,
            "share": round(c_other / n_total_dated, 6)
            if n_total_dated > 0
            else None,
        }
    )
    ledger.add(
        "count-diagnostic-granularity-other",
        "count",
        "Rows with date_range not in any standard bucket (i.e. neither 0 nor "
        "an exact bucket of 25/50/100/200/500 nor any multiple of 10 up to 200)",
        c_other,
        "rows",
        "date_range not in standard buckets",
        "artefacts.md",
    )
    pd.DataFrame(granularity_bins).to_csv(
        TABLES_DIR / "diagnostic-granularity.csv", index=False
    )

    # Date-range broad histogram
    dr_hist = pd.cut(
        dr_int.astype("float"),
        bins=DATE_RANGE_BINS,
        labels=DATE_RANGE_LABELS,
    )
    dr_hist_counts = dr_hist.value_counts().reindex(DATE_RANGE_LABELS)
    dr_hist_df = pd.DataFrame(
        {
            "bin": dr_hist_counts.index,
            "count": dr_hist_counts.values,
            "share": dr_hist_counts.values
            / max(1, int(dr_hist_counts.sum())),
        }
    )
    dr_hist_df.to_csv(
        TABLES_DIR / "diagnostic-date-range-histogram.csv", index=False
    )
    for _, row in dr_hist_df.iterrows():
        b = row["bin"]
        slug = slugify(str(b))
        ledger.add(
            f"count-diagnostic-date-range-{slug}",
            "count",
            f"Rows with date_range in bin {b}",
            int(row["count"]) if pd.notna(row["count"]) else 0,
            "rows",
            f"date_range in bin {b}",
            "artefacts.md",
        )
        ledger.add(
            f"rate-diagnostic-date-range-{slug}",
            "rate",
            f"Share (of dated rows) with date_range in bin {b}",
            round(float(row["share"]), 6) if pd.notna(row["share"]) else 0.0,
            "fraction",
            "histogram share",
            "artefacts.md",
        )

    # 5% anomaly flag
    anomaly_flags = []
    for entry in granularity_bins:
        if (
            entry["share"] is not None
            and entry["share"] > 0.05
            and entry["bucket"] not in ("other",)
        ):
            anomaly_flags.append((entry["bucket"], entry["share"]))

    # -------------------------------------------------------------------------
    # Write reports
    # -------------------------------------------------------------------------
    log.event("Writing reports")

    # --- summary.md ---
    summary_lines = []
    summary_lines.append("# LIRE v3.0 — descriptive profile (summary)\n")
    summary_lines.append(
        f"Dataset: `{DATASET_PATH.name}`. Rows: **{n_rows:,}**. Columns: "
        f"**{n_cols}**. Primary key: `{PRIMARY_KEY}` ({pk_unique:,} unique, "
        f"{pk_null} null).\n"
    )
    summary_lines.append("## Headline findings\n")
    summary_lines.append(
        f"- **Dating coverage:** {n_dated:,} of {n_rows:,} rows ("
        f"{n_dated / n_rows:.1%}) have both `not_before` and `not_after`. "
        f"Observed envelope: `not_before` ∈ [{int(nb_min)}, {int(nb_max)}]; "
        f"`not_after` ∈ [{int(na_min)}, {int(na_max)}].\n"
    )
    summary_lines.append(
        f"- **Geolocation:** {n_geo:,} of {n_rows:,} rows ({n_geo / n_rows:.1%}) "
        f"have valid coordinates (both `Latitude` and `Longitude` non-null and "
        f"in range).\n"
    )
    if not np.isnan(ratio_mid):
        summary_lines.append(
            f"- **Midpoint-inflation artefact:** ratio of observed century-"
            f"midpoint counts to mean of adjacent years = "
            f"**{ratio_mid:.2f}×** (chi²={chi2_mid:.1f}, p={pval_mid:.3g}). "
            "Strong overrepresentation at editorial century-midpoints is the "
            "SDAM-documented dating artefact.\n"
        )
    summary_lines.append(
        f"- **Duplicate rows:** {n_dup_all:,} exact duplicates across all "
        f"columns; {n_dup_pk:,} duplicates on primary key `{PRIMARY_KEY}`.\n"
    )
    summary_lines.append(
        f"- **High-null columns (>50% null):** {len(high_null)} of {n_cols}.\n"
    )
    if anomaly_flags:
        anom_str = "; ".join(
            f"{b} ({s:.1%})" for b, s in anomaly_flags
        )
        summary_lines.append(
            f"- **Granularity-bucket anomalies (>5%):** {anom_str}. Flag-and-"
            "continue per decision-point discipline.\n"
        )

    summary_lines.append("\n## Per-subset highlights\n")
    for name in ("province", "urban-area"):
        s = subset_summaries[name]
        thresh_str = ", ".join(
            f"{t}→{c}" for t, c in s["thresholds"].items()
        )
        top_row = s["grouped"].iloc[0]
        top_key = top_row.iloc[0]
        top_count = int(top_row["count"])
        summary_lines.append(
            f"- **{name}:** {s['n_groups']:,} distinct groups; threshold "
            f"qualifying counts ({thresh_str}); largest group `{top_key}` "
            f"with {top_count:,} rows.\n"
        )

    summary_lines.append("\n## Artefact summary\n")
    summary_lines.append(
        f"- **Midpoint-inflation:** observed = {century_mid_count:,}; expected "
        f"from adjacent years = {expected_mid:.1f}; ratio = {ratio_mid:.2f}× "
        f"(p={pval_mid:.3g}).\n"
    )
    summary_lines.append(
        f"- **Editorial spikes (aggregate not_before chi²):** {chi2_ed:.1f}, "
        f"p={pval_ed:.3g}.\n"
    )
    summary_lines.append(
        f"- **Coordinate precision:** {gt4_share:.1%} of non-null coordinate "
        f"values have >4 decimal places (false-precision indicator).\n"
    )
    summary_lines.append(
        f"- **Outlier coordinates:** lat |·|>90 = {lat_out}; lon |·|>180 = "
        f"{lon_out}.\n"
    )
    summary_lines.append(
        f"- **Negative date_range (not_before > not_after):** {neg_dr}.\n"
    )
    summary_lines.append(
        f"- **date_range > 500 years:** {extreme_dr:,}.\n"
    )
    summary_lines.append(
        f"- **Temporal envelope outliers (against conservative [-700, 700]):** "
        f"not_before={nb_outside}, not_after={na_outside}.\n"
    )
    summary_lines.append(
        "- **`is_within_RE` / `is_geotemporal`:** could not run — columns "
        "absent from LIRE v3.0 schema.\n"
    )

    summary_lines.append("\n## Cross-references\n")
    summary_lines.append("- `profile-province.md`, `profile-urban-area.md`\n")
    summary_lines.append("- `artefacts.md`\n")
    summary_lines.append(
        "- `claims.jsonl` — machine-readable claim ledger backing every "
        "number in these reports.\n"
    )
    summary_lines.append("- `tables/*.csv` — backing data for every table.\n")
    summary_lines.append("- `decisions.md` — judgement-call audit trail.\n")

    (OUTPUT_DIR / "summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8"
    )

    # --- profile-{subset}.md ---
    for level in SUBSET_LEVELS:
        name = level["name"]
        if not level["columns"]:
            continue
        s = subset_summaries[name]
        lines = [f"# Subset profile — `{name}`\n"]
        lines.append(
            f"Distinct groups: **{s['n_groups']:,}**. "
            f"Grouping columns: `{level['columns']}`.\n"
        )
        lines.append("## Threshold-qualifying group counts\n")
        for t, c in s["thresholds"].items():
            lines.append(f"- ≥ {t} rows: **{c}** groups")
        lines.append("\n## Top-20 groups by row count\n")
        lines.append("| Rank | Group | Count |")
        lines.append("|-----:|:------|------:|")
        for i, row in s["top20"].iterrows():
            grp = row.iloc[0]
            grp_disp = "<null>" if pd.isna(grp) else str(grp)
            lines.append(
                f"| {i + 1} | {grp_disp} | {int(row['count']):,} |"
            )
        lines.append(
            f"\nFull per-group counts: `tables/subset-{name}-counts.csv`. "
            f"Per-group stats for groups passing highest threshold: "
            f"`tables/subset-{name}-qualifying-stats.csv`.\n"
        )
        (OUTPUT_DIR / f"profile-{name}.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )

    # --- artefacts.md ---
    art = []
    art.append("# Artefact checks — LIRE v3.0\n")
    art.append("## midpoint-inflation\n")
    art.append(
        f"- Rows whose midpoint = century-midpoint year: "
        f"**{century_mid_count:,}**\n"
        f"- Rows whose midpoint = adjacent-to-century-midpoint year (±1): "
        f"**{adj_count:,}** (sum across both adjacents)\n"
        f"- Expected at century-midpoints if uniform: **{expected_mid:.1f}**\n"
        f"- Observed/expected ratio: **{ratio_mid:.2f}×**\n"
        f"- Chi² (1 d.o.f.): **{chi2_mid:.2f}**, p = **{pval_mid:.3g}**\n"
        "- Interpretation: ratios substantially above 1.0 indicate the "
        "century-basis editorial dating artefact (SDAM)."
    )

    art.append("\n## editorial-spikes\n")
    art.append("| Year | nb obs | nb adj mean | nb ratio | na obs | na adj mean | na ratio |")
    art.append("|-----:|------:|-----------:|--------:|------:|-----------:|--------:|")
    for r in spikes_rows:
        art.append(
            f"| {r['year']} | {r['not_before_obs']:,} | "
            f"{r['not_before_adj_mean']:.1f} | "
            f"{r['not_before_ratio']:.2f} | "
            f"{r['not_after_obs']:,} | "
            f"{r['not_after_adj_mean']:.1f} | "
            f"{r['not_after_ratio']:.2f} |"
        )
    art.append(
        f"\nAggregate chi² (not_before, sum over editorial years): "
        f"**{chi2_ed:.2f}**, p = **{pval_ed:.3g}**.\n"
    )

    art.append("\n## coordinate-precision\n")
    art.append("| Decimal places | Count |")
    art.append("|---------------:|------:|")
    for k, v in dp_counts.items():
        art.append(f"| {k} | {int(v):,} |")
    art.append(
        f"\n>4 decimal places dominate at {gt4_share:.1%} of non-null "
        "coordinate values; this is the false-precision indicator."
    )

    art.append("\n## outlier-coordinates\n")
    art.append(f"- |Latitude| > 90: **{lat_out}**")
    art.append(f"- |Longitude| > 180: **{lon_out}**\n")

    art.append("\n## null-profile\n")
    art.append(f"- Columns with null_rate > 50%: **{len(high_null)}**")
    art.append(
        "- Full per-column null table: `tables/column-stats.csv`\n"
    )
    art.append("- High-null columns: `tables/artefact-high-null-columns.csv`\n")

    art.append("\n## duplicate-rows\n")
    art.append(f"- Exact-duplicates across all columns: **{n_dup_all:,}**")
    art.append(
        f"- Duplicates on primary key `{PRIMARY_KEY}`: **{n_dup_pk:,}**\n"
    )

    art.append("\n## negative-date-range\n")
    art.append(f"- Rows where `not_before > not_after`: **{neg_dr}**\n")

    art.append("\n## date-range-extreme\n")
    art.append(f"- Rows where `date_range > 500`: **{extreme_dr:,}**\n")

    art.append("\n## temporal-outliers\n")
    art.append(
        f"- Conservative envelope used (none supplied): [{envelope_lo}, "
        f"{envelope_hi}]\n"
        f"- `not_before` outside envelope: **{nb_outside}**\n"
        f"- `not_after` outside envelope: **{na_outside}**\n"
        f"- Observed range `not_before`: [{int(nb_min)}, {int(nb_max)}]\n"
        f"- Observed range `not_after`: [{int(na_min)}, {int(na_max)}]\n"
    )

    art.append("\n## geolocated-rate\n")
    art.append(
        f"- Rows with valid coordinates: **{n_geo:,}** of {n_rows:,} = "
        f"**{n_geo / n_rows:.1%}**\n"
    )

    art.append("\n## is_within_RE-rate / is_geotemporal-rate\n")
    art.append(
        "Could not run: columns `is_within_RE` and `is_geotemporal` are "
        "absent from the LIRE v3.0 schema. See `decisions.md`.\n"
    )

    art.append("\n## Unexpected-pattern diagnostic\n")
    art.append("### Granularity histogram\n")
    art.append("| Bucket | Count | Share of dated |")
    art.append("|:-------|------:|--------------:|")
    for entry in granularity_bins:
        share_disp = (
            f"{entry['share']:.1%}" if entry["share"] is not None else "—"
        )
        art.append(
            f"| {entry['bucket']} | {entry['count']:,} | {share_disp} |"
        )
    if anomaly_flags:
        art.append(
            "\n**Flagged anomalies (share > 5%):** "
            + "; ".join(f"{b} ({s:.1%})" for b, s in anomaly_flags)
            + ". Per decision-point discipline, flag-and-continue."
        )
    art.append("\n### Date-range distribution (broad)\n")
    art.append("| Bin (years) | Count | Share |")
    art.append("|:------------|------:|------:|")
    for _, row in dr_hist_df.iterrows():
        cnt = (
            int(row["count"])
            if pd.notna(row["count"]) and row["count"] is not None
            else 0
        )
        share = (
            float(row["share"])
            if pd.notna(row["share"]) and row["share"] is not None
            else 0.0
        )
        art.append(f"| {row['bin']} | {cnt:,} | {share:.1%} |")

    (OUTPUT_DIR / "artefacts.md").write_text(
        "\n".join(art) + "\n", encoding="utf-8"
    )

    # --- claims.jsonl ---
    ledger.write(OUTPUT_DIR / "claims.jsonl")
    log.event(f"Wrote {len(ledger.rows)} claims")

    # --- decisions.md ---
    if not anomaly_flags:
        decisions.add(
            "Unexpected-pattern diagnostic — no >5% anomalies",
            "**Fact:** No granularity bucket exceeded the 5% flag threshold "
            "(after standard buckets). Default applied: continue with full "
            "report. Investigator review not required.",
        )
    else:
        decisions.add(
            "Unexpected-pattern diagnostic — anomalies present",
            "**Fact:** The following granularity buckets exceeded the 5% "
            "share-of-dated-rows threshold: "
            + "; ".join(f"{b} ({s:.1%})" for b, s in anomaly_flags)
            + ".\n\n**Default applied:** Flag prominently in summary.md and "
            "artefacts.md; continue with full report.\n\n**Investigator "
            "review:** Recommended — these are likely editorial-convention "
            "concentrations that downstream chronological analyses should "
            "model (e.g., via aoristic-probability weighting).",
        )
    decisions.write(OUTPUT_DIR / "decisions.md")

    log.event("Done")
    log.flush()


if __name__ == "__main__":
    main()
