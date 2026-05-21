#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-filter-and-prep.py --- Block 1 of the RAC-TRAC 2026 talk-prep run.

Purpose
-------
Apply the lodged preregistration's canonical filter to LIRE v3.0 and cache the
filtered corpus to disk, so every downstream block (empire / province / city
SPAs, frequentist NBR Hanson scaling, synthetic mixture-recovery demo, Bayesian
H3a within-between NBR) reads the same prereg-compliant dataframe.

The filter logic is identical to the sister run
`runs/2026-05-17-date-range-filtered-spas/code/date_range_filtered_spas.py`
(function `load_filtered_lire()`, lines 167--193) and to the preregistration's
§3 specification (Data and pre-processing). Three predicates intersected with
the analysis envelope:

  is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL
                    AND not_before IS NOT NULL AND not_after IS NOT NULL
                    AND not_before <= not_after
  is_within_RE   := province IS NOT NULL
  envelope       := overlap with [50 BC, AD 350]  (overlap, not containment)
                    i.e. not_after >= -50 AND not_before <= 350

Critical-friend gate
--------------------
Compare post-filter counts to the prereg's published targets (180,609 total,
65,435 Rome, 115,174 Rome-excluded, 140,575 Hanson-city-assigned, ~815
Hanson-matched cities Rome-excluded). HALT and report if any count diverges by
> 1% --- divergence is a methodological flag, not a thing to paper over.

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet  (read-only)

Outputs
-------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet
runs/2026-05-21-talk-prep/outputs/tables/filter-counts.csv

Reproducibility
---------------
RANDOM_SEED = 20260521 (no stochastic resampling here; recorded for ritual
consistency with the rest of the pipeline).

Date
----
2026-05-21

Author / Who-asked
------------------
Shawn Ross, ahead of TRAC7 conference talk (Adela presenting Friday 14:20
Aarhus). Analysis run by Claude (Opus 4.7, 1M context) on Shawn's brief.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths --- resolved relative to this script so the run is portable.
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
OUT_DATA = RUN_DIR / "data" / "lire-filtered.parquet"
OUT_TBL = RUN_DIR / "outputs" / "tables" / "filter-counts.csv"

OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
OUT_TBL.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Filter constants. Envelope and bin width pinned to the prereg.
# ---------------------------------------------------------------------------
ENVELOPE_MIN = -50   # 50 BC inclusive
ENVELOPE_MAX = 350   # AD 350 inclusive (right edge of last bin)

# Prereg-published sanity targets. Source: planning/preregistration-draft.md
# (§3 Data + footnote on Rome exclusion). Divergence > 1% triggers HALT.
#
# Row-level targets only. The prereg's "~815 Hanson-matched cities" figure is
# a city-aggregation count, not a row count --- and it carries a known
# methodological flag (see CITY_COUNT_NOTE below). It is therefore tracked
# separately in `summarise_city_grain()` and reported but not gated here.
PREREG_TARGETS = {
    "total_filtered": 180_609,
    "rome_only": 65_435,
    "rome_excluded": 115_174,
    "hanson_city_assigned_filtered": 140_575,
}
HALT_TOLERANCE = 0.01  # 1%

CITY_COUNT_NOTE = """
Note on the prereg's "~815 Hanson-matched cities, Rome-excluded" figure:
this number was inherited from the 2024 exploratory notebook
(`archive/2026-04-22-inscriptions-spa.ipynb` cell 73), which applied a
province_language == 'Latin' filter via a province->language mapping defined
in cell 54. That mapping is NOT a column in the LIRE parquet --- it is a
manually-curated dictionary in the notebook. The prereg's text spec (§3
line 131, line 235) says simply "all cities with Hanson population estimates,
Rome excluded", which on the LIRE parquet yields 1,044 unique cities, not
~815. Block 3 (Hanson NBR scaling) will need to decide between:
  (a) the broader 1,044-city sample (text-spec faithful),
  (b) the narrower Latin-province ~815 sample (number-faithful; requires
      externalising the province->language mapping into a tracked CSV),
  (c) reporting both side-by-side as a sensitivity.
"""

# Reproducibility seed (deterministic analysis here; recorded for ritual).
RANDOM_SEED = 20_260_521
np.random.seed(RANDOM_SEED)


def load_filtered_lire() -> pd.DataFrame:
    """Load LIRE v3.0 and apply the preregistration filter.

    Returns the filtered DataFrame with integer not_before / not_after, and
    derived `width` (inclusive-Roman, used inside the SPA for unit-mass
    normalisation) and `date_range` (exclusive, matching the 2024 notebook
    semantics) columns.

    Filter logic is canonical: see preregistration-draft.md §3 and the sister
    diagnostic at runs/2026-05-17-date-range-filtered-spas/code/
    date_range_filtered_spas.py lines 167--193.

    Returns
    -------
    pd.DataFrame
        Filtered LIRE corpus. Expected 180,609 rows.
    """
    df = pd.read_parquet(DATA_PATH)

    is_geotemporal = (
        df["Latitude"].notna()
        & df["Longitude"].notna()
        & df["not_before"].notna()
        & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    # Overlap (not containment) with [ENVELOPE_MIN, ENVELOPE_MAX].
    in_envelope = (
        (df["not_after"] >= ENVELOPE_MIN) & (df["not_before"] <= ENVELOPE_MAX)
    )

    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["not_before"] = sub["not_before"].astype(int)
    sub["not_after"] = sub["not_after"].astype(int)
    sub["width"] = sub["not_after"] - sub["not_before"] + 1
    sub["date_range"] = sub["not_after"] - sub["not_before"]
    return sub


def identify_rome(df: pd.DataFrame) -> pd.Series:
    """Return a boolean mask of inscriptions located at Rome.

    The 2024 notebook + the prereg's 65,435 Rome figure rely on the
    `urban_context_city` attribute equalling 'Roma'. We use that as the
    canonical Rome predicate. See planning/preregistration-draft.md §3,
    Rome-exclusion footnote.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered LIRE corpus from `load_filtered_lire`.

    Returns
    -------
    pd.Series
        Boolean mask; True where the inscription is at Rome.
    """
    if "urban_context_city" not in df.columns:
        raise KeyError(
            "Expected column 'urban_context_city' is missing from LIRE; "
            "cannot identify Rome rows. Check the parquet schema."
        )
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def summarise_filter(df: pd.DataFrame) -> dict:
    """Compute the row-level sanity-check counts and return them as a dict.

    Mirrors the prereg's §3 published figures exactly so divergences are
    detectable. Excludes the city-aggregation count, which lives in
    `summarise_city_grain()` because the prereg's "~815" carries an
    interpretation question (see CITY_COUNT_NOTE).

    Parameters
    ----------
    df : pd.DataFrame
        Filtered LIRE corpus.

    Returns
    -------
    dict
        Keys aligning with PREREG_TARGETS; values are observed counts.
    """
    rome_mask = identify_rome(df)
    is_hanson = df["urban_context_pop_est"].notna()

    rome_only = int(rome_mask.sum())
    total = int(len(df))
    rome_excluded = total - rome_only
    hanson_city_assigned_filtered = int(is_hanson.sum())

    return {
        "total_filtered": total,
        "rome_only": rome_only,
        "rome_excluded": rome_excluded,
        "hanson_city_assigned_filtered": hanson_city_assigned_filtered,
    }


def summarise_city_grain(df: pd.DataFrame) -> dict:
    """Report Hanson-city unique-count diagnostics under multiple grains.

    The prereg quotes "~815" as the H3a NBR sample size, but that figure was
    inherited from a 2024 notebook subset that applied an extra Latin-province
    filter via a notebook-internal dictionary not present in the LIRE parquet.
    We surface every plausible grain so Block 3 can choose with eyes open.

    Returns
    -------
    dict
        text_spec_faithful: count under the prereg's text spec (all Hanson
            cities, Rome-excluded). Expected to be 1,044.
        with_min_N_2 / 5 / 10 / 100: counts under minimum-inscription
            thresholds, in case the prereg's "~815" tacitly assumed one.
    """
    rome_mask = identify_rome(df)
    is_hanson = df["urban_context_pop_est"].notna()
    ex_rome_hanson = df.loc[~rome_mask & is_hanson]

    city_counts = ex_rome_hanson.groupby("urban_context_city").size()
    out = {
        "text_spec_faithful_n_cities": int(len(city_counts)),
    }
    for thresh in (2, 5, 10, 100):
        out[f"with_min_N_{thresh}"] = int((city_counts >= thresh).sum())
    return out


def check_against_prereg(observed: dict) -> tuple[bool, list[str]]:
    """Compare observed counts to prereg targets at 1% tolerance.

    Parameters
    ----------
    observed : dict
        Output of `summarise_filter`.

    Returns
    -------
    (passed, messages)
        passed is True if every count is within tolerance; messages is a
        per-row human-readable diff line ('OK' or 'DIVERGE').
    """
    messages: list[str] = []
    passed = True
    for key, target in PREREG_TARGETS.items():
        got = observed[key]
        diff = got - target
        rel = diff / target if target else float("inf")
        status = "OK" if abs(rel) <= HALT_TOLERANCE else "DIVERGE"
        if status == "DIVERGE":
            passed = False
        messages.append(
            f"  [{status:7}] {key:48} target={target:>8d}  "
            f"observed={got:>8d}  delta={diff:+d} ({rel:+.4%})"
        )
    return passed, messages


def main() -> int:
    print(f"[01-filter-and-prep] loading LIRE v3.0 from {DATA_PATH}")
    df = load_filtered_lire()
    print(f"[01-filter-and-prep] filtered corpus: {len(df):,} rows, "
          f"{df.shape[1]} columns")

    observed = summarise_filter(df)
    passed, messages = check_against_prereg(observed)

    print("[01-filter-and-prep] row-level sanity-check vs prereg targets:")
    for m in messages:
        print(m)

    city_grain = summarise_city_grain(df)
    print("\n[01-filter-and-prep] city-grain diagnostics "
          "(prereg quotes '~815'; see CITY_COUNT_NOTE):")
    for k, v in city_grain.items():
        print(f"    {k:38} {v:>6}")
    print(CITY_COUNT_NOTE)

    # Persist the counts table regardless of pass/fail, so the diagnostic
    # trail is recoverable if we have to triage.
    counts_df = pd.DataFrame(
        [
            {
                "metric": key,
                "prereg_target": PREREG_TARGETS[key],
                "observed": observed[key],
                "delta": observed[key] - PREREG_TARGETS[key],
                "rel_delta": (
                    (observed[key] - PREREG_TARGETS[key]) / PREREG_TARGETS[key]
                    if PREREG_TARGETS[key]
                    else float("nan")
                ),
            }
            for key in PREREG_TARGETS
        ]
    )
    counts_df.to_csv(OUT_TBL, index=False)
    print(f"[01-filter-and-prep] wrote sanity table -> {OUT_TBL}")

    if not passed:
        print(
            "[01-filter-and-prep] HALT: one or more counts diverge from the "
            "prereg by > 1%. Review filter logic and the dataframe before "
            "proceeding. Filtered parquet NOT written."
        )
        return 1

    df.to_parquet(OUT_DATA, index=False)
    print(
        f"[01-filter-and-prep] wrote filtered corpus -> {OUT_DATA} "
        f"({OUT_DATA.stat().st_size / 1e6:.1f} MB)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
