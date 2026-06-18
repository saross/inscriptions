#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h9_common.py --- shared data-prep helpers for the H9 letter-mass H3a
confirmatory run (runs/2026-06-18-h9-letter-mass-h3a/).

H9 is the **cross-sectional confirmatory H3a within-between (Mundlak)
negative-binomial regression, with per-city LETTER-COUNT MASS as the
response**, in place of inscription count. It mirrors the inscription-count H3a
confirmatory run (runs/2026-06-04-h3a-confirmatory/) in every other respect;
only the response variable changes.

Provenance of this module
-------------------------
This is an ADAPTED COPY of
`runs/2026-06-04-h3a-confirmatory/code/h3a_common.py` (commit on `main`,
2026-06-04). It is copied (not imported) per the standing project rule that the
lodged/shared H3a modules must NOT be edited; H9 machinery lives entirely in
this run directory. The two substantive changes relative to the H3a template
are:

  1. The per-city response is **letter mass** = the sum, over a city's
     date-window-filtered, frame-eligible inscriptions, of a per-inscription
     letter count, instead of the inscription row count.
  2. The **primary frame is the Latin-speaking provinces** (Decision 36 / OSF
     Amendment 02, lodged 2026-06-06); the empire-wide frame is retained as
     **secondary / context** with the coverage caveat. (The H3a template's
     primary was empire-wide, with Latin as Sensitivity B; H9 inverts that
     ordering to follow the lodged Latin-primary framing.)

Letter-mass measure definition (the load-bearing choice — see BUILD-NOTES.md)
----------------------------------------------------------------------------
Per OSF Amendment 01 §A5.1 and the lodged preregistration (line 388), the
content measure is the summed **`clean_text_conservative`** letter count,
counting **Latin A--Z characters only, Greek excluded**. The interpretive
variant (`clean_text_interpretive_word`, Latin A--Z only) is retained as a
sensitivity check. This is the LODGED definition and it is what H9 uses.

NOTE: the 2026-05-26 letter-count probe
(`runs/2026-05-26-letter-count-probe/code/01-compute-letter-counts.py`) used a
broader regex `[A-Za-zÀ-ÿΑ-Ωα-ω]` that ALSO counted Greek and Latin-1
diacritics. That probe pre-dates Amendment 01 and its measure is NOT the lodged
one; H9 deliberately does not reuse it. See BUILD-NOTES.md.

Blind-run note (carried over from the H3a template)
---------------------------------------------------
Every number this module produces is derived from the raw LIRE parquet, the
preregistration filter, the lodged amendment definitions, and the design
artefact --- never from any prior result.

Spec references
---------------
- planning/preregistration-draft.md  (§3 H3a; §5 line 388 letter-count def)
- planning/osf-amendment-2026-05-29-two-measure-framework.md  (§A5.1 measure def)
- planning/h3a-confirmatory-launch-spec-2026-06-04.md  (sample decisions, frame)
- planning/decision-log.md  (Decision 22 date-window counts; 32 f_within
  weightings; 35 model + scope; 36 Latin-primary frame)
- runs/2026-06-04-h3a-confirmatory/code/h3a_common.py  (the template this
  adapts)

Author / Date
-------------
Claude Code (Opus 4.8, 1M context), 2026-06-18, on Shawn's H9 build brief
(BUILD-AND-COMMIT-ONLY; no fit run).
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths --- resolved relative to this module so the run is portable across the
# local repo and the eventual zbook run host.
# ---------------------------------------------------------------------------
THIS = Path(__file__).resolve()
CODE_DIR = THIS.parent
RUN_DIR = CODE_DIR.parent
PROJECT_ROOT = RUN_DIR.parent.parent
RAW_LIRE = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = RUN_DIR / "data" / "province-language-map.csv"

# Canonical processed-data outputs for H9. Kept under this run dir's own
# data/processed/ subtree so the H9 letter-mass frames never collide with the
# inscription-count H3a frames in the project-level data/processed/.
PROCESSED_DIR = RUN_DIR / "data" / "processed"
# PRIMARY = Latin-speaking provinces (Decision 36 / Amendment 02).
LATIN_PARQUET = PROCESSED_DIR / "city_level_for_h9_latin.parquet"
# SECONDARY / context = empire-wide (within the original lodged prereg text).
EMPIRE_PARQUET = PROCESSED_DIR / "city_level_for_h9_empire.parquet"

# ---------------------------------------------------------------------------
# Filter constants (prereg §3, identical to the H3a template / the lodged
# preregistration filter). The chronological envelope and Rome-exclusion are
# UNCHANGED by both amendments (Amendment 01 §A6; Decision 36).
# ---------------------------------------------------------------------------
ENVELOPE_MIN = -50   # 50 BC inclusive
ENVELOPE_MAX = 350   # AD 350 inclusive

LIRE_VERSION = "v3.0"
DATE_WINDOW = "50 BC - AD 350 (overlap)"

# Prereg row-level sanity targets (HARD-STOP if any diverges materially) ---
# identical to the H3a template; the date-window filter is the same, so the
# filtered corpus is the same 180,609 rows on which letters are then counted.
PREREG_ROW_TARGETS = {
    "total_filtered": 180_609,
    "rome_only": 65_435,
    "rome_excluded": 115_174,
    "hanson_city_assigned_filtered": 140_575,
}

# ---------------------------------------------------------------------------
# Letter-count primitive --- LODGED definition (Amendment 01 §A5.1; prereg
# line 388): Latin A--Z characters ONLY; Greek excluded.
#
# This is a NARROWER regex than the 2026-05-26 probe's
# `[A-Za-zÀ-ÿΑ-Ωα-ω]`: it intentionally drops the Greek block (Α-Ωα-ω) and the
# Latin-1 supplement diacritics (À-ÿ), because the lodged content measure is
# *Latin* content and Greek is excluded by definition. Diacritics are dropped
# too: A--Z means the 26-letter ASCII Latin alphabet, upper and lower case.
# Punctuation, digits, brackets, and whitespace are excluded by construction
# (the regex only matches A--Za--z).
# ---------------------------------------------------------------------------
LATIN_AZ_LETTER = re.compile(r"[A-Za-z]")


def count_latin_letters(text) -> int:
    """Count Latin A--Z alphabetic characters in a string (Greek excluded).

    This implements the LODGED letter-mass primitive (Amendment 01 §A5.1):
    only the 26-letter ASCII Latin alphabet (upper and lower case) is counted.

    Parameters
    ----------
    text : str | float | None
        A cleaned-text field from LIRE; may be NaN/None for rows whose cleaning
        step yielded no readable text.

    Returns
    -------
    int
        Count of Latin A--Z characters; 0 if `text` is NaN/None/empty/non-str.
    """
    if text is None:
        return 0
    if isinstance(text, float) and np.isnan(text):
        return 0
    if not isinstance(text, str):
        return 0
    return len(LATIN_AZ_LETTER.findall(text))


def load_filtered_lire() -> pd.DataFrame:
    """Load LIRE v3.0, apply the preregistration filter, and attach the two
    per-inscription letter-count columns.

    The filter is IDENTICAL to the H3a template
    (`h3a_common.load_filtered_lire`) and to prereg §3: three predicates
    intersected with the [50 BC, AD 350] analysis envelope (overlap, not
    containment):

      is_geotemporal := Lat & Lon & not_before & not_after present,
                        not_before <= not_after
      is_within_RE   := province present
      in_envelope    := not_after >= -50 AND not_before <= 350

    On top of the filtered frame, two per-inscription letter counts are
    computed with the LODGED Latin-A--Z-only primitive (`count_latin_letters`):

      letter_count_conservative   := Latin A--Z letters in clean_text_conservative
      letter_count_interpretive   := Latin A--Z letters in clean_text_interpretive_word

    `letter_count_conservative` is the PRIMARY content measure (Amendment 01
    §A5.1); `letter_count_interpretive` is the sensitivity variant.

    Returns
    -------
    pd.DataFrame
        Filtered LIRE corpus (expected 180,609 rows) with the two letter-count
        columns attached.
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

    # Attach the two per-inscription letter counts (LODGED Latin-A--Z primitive).
    for col in ("clean_text_conservative", "clean_text_interpretive_word"):
        if col not in sub.columns:
            raise KeyError(
                f"Required cleaned-text column {col!r} missing from LIRE v3.0; "
                "letter-mass cannot be computed."
            )
    sub["letter_count_conservative"] = (
        sub["clean_text_conservative"].map(count_latin_letters).astype("int64")
    )
    sub["letter_count_interpretive"] = (
        sub["clean_text_interpretive_word"].map(count_latin_letters).astype("int64")
    )
    return sub


def rome_mask(df: pd.DataFrame) -> pd.Series:
    """Boolean mask: True where the inscription is located at Rome.

    Canonical Rome predicate: urban_context_city == 'roma' (case/space
    insensitive). Identical to the H3a template / 01-filter-and-prep.py.
    Rome is EXCLUDED from both H9 frames (Decision 36 / Obs 101; unchanged by
    the amendments).
    """
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def check_row_counts(df: pd.DataFrame) -> tuple[bool, dict, list[str]]:
    """Compare filtered row counts to the prereg targets at 1% tolerance.

    Identical to the H3a template; the date-window filter is the same, so the
    same 180,609-row sanity targets apply BEFORE letters are summed per city.

    Returns (passed, observed_dict, message_lines). A HARD-STOP if not passed.
    """
    rome = rome_mask(df)
    total = int(len(df))
    rome_only = int(rome.sum())
    observed = {
        "total_filtered": total,
        "rome_only": rome_only,
        "rome_excluded": total - rome_only,
        "hanson_city_assigned_filtered":
            int(df["urban_context_pop_est"].notna().sum()),
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
    """Modal value of a series, or NaN if empty. Matches the H3a template's
    province-mode aggregation."""
    m = x.mode()
    return m.iloc[0] if not m.empty else np.nan


def _build_city_frame(filtered: pd.DataFrame,
                      response_col: str) -> tuple[pd.DataFrame, list[str]]:
    """Aggregate filtered LIRE to a one-row-per-city EMPIRE frame, with
    per-city LETTER MASS as the response.

    This mirrors `h3a_common.build_primary_frame` exactly, EXCEPT the response:
    where the H3a template aggregates an inscription row COUNT
    (`size`), H9 aggregates the SUM of a per-inscription letter-count column
    over the city's date-window-filtered, Hanson-matched, Rome-excluded
    inscriptions.

    Per-city LETTER MASS (the H9 response) is therefore:

        letter_mass_c = sum_{i in city c, date-window, Hanson, not-Rome}
                        letter_count_<variant>(i)

    Frame eligibility is IDENTICAL to the H3a primary frame:
      - Hanson-matched (urban_context_pop_est not null),
      - Rome-excluded,
      - >= 1 date-window inscription (cities enter via the grouped LIRE rows).

    The Mundlak components (province-mean log_pop, within-province deviation),
    the province index, and the per-city median coordinate are built exactly as
    in the H3a template. The coordinate is the **median** Longitude/Latitude of
    the city's date-window inscriptions (robust to mis-geocoded outliers; used
    only for the H3c/PPC spatial weights, never in the regression).

    Parameters
    ----------
    filtered : pd.DataFrame
        Output of `load_filtered_lire()` (filtered LIRE + letter-count columns).
    response_col : str
        Which per-inscription letter-count column to sum into the per-city
        response: 'letter_count_conservative' (PRIMARY) or
        'letter_count_interpretive' (sensitivity).

    Returns
    -------
    (cities_df, province_categories)
        cities_df has a `letter_mass` response column (int64). The dispersion
        and downstream f_within machinery treat `letter_mass` exactly as the
        H3a template treats `inscription_count`.
    """
    rome = rome_mask(filtered)
    has_hanson = filtered["urban_context_pop_est"].notna()
    sub = filtered.loc[~rome & has_hanson].copy()

    agg = (
        sub.groupby("urban_context_city")
        .agg(
            letter_mass=(response_col, "sum"),
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
    agg["letter_mass"] = agg["letter_mass"].astype("int64")

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
    agg["response_measure"] = response_col

    cols = [
        "city", "province", "province_idx",
        "urban_context_pop_est", "log_pop", "log_pop_prov_mean",
        "log_pop_within",
        "letter_mass", "inscription_count", "longitude", "latitude",
        "lire_version", "date_window", "rome_excluded", "response_measure",
    ]
    agg = (agg[cols]
           .sort_values("urban_context_pop_est", ascending=False)
           .reset_index(drop=True))
    return agg, list(province_codes.categories)


def build_empire_frame(filtered: pd.DataFrame, response_col: str
                       ) -> tuple[pd.DataFrame, list[str]]:
    """SECONDARY / context frame: all Hanson-matched, Rome-excluded cities
    (empire-wide), with per-city letter mass as the response.

    This is the H3a-template PRIMARY sample (1,044 cities) reused as H9's
    SECONDARY frame (Decision 36: empire-wide is reported as secondary/context
    with the LIRE-coverage caveat). The Mundlak centring is over the full
    empire-wide city set.
    """
    frame, provinces = _build_city_frame(filtered, response_col)
    frame = frame.copy()
    frame["sample"] = "empire"
    return frame, provinces


def build_latin_frame(filtered: pd.DataFrame, response_col: str) -> pd.DataFrame:
    """PRIMARY frame: empire frame restricted to Latin-speaking provinces
    (Decision 36 / OSF Amendment 02), with per-city letter mass as the response.

    The frame is defined by the externalised province->language map
    (`data/province-language-map.csv`; the first-class artefact that DEFINES the
    Latin frame per Decision 36). The Mundlak components are RECOMPUTED over the
    Latin-only city set (correct centring for THIS sample), exactly as the H3a
    template recomputes them for its Latin Sensitivity B.

    The realised Latin frame on the inscription-count side is 817 cities / 39
    provinces (Decision 36 / Amendment 02 §A5.3); the H9 letter-mass frame is
    built over the same cities (the eligibility predicate is identical; only the
    response differs), so the city/province counts are expected to match.
    """
    lang_map = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    latin_provinces = set(
        lang_map.loc[lang_map["language"] == "Latin", "lire_province"]
    )

    empire, _ = build_empire_frame(filtered, response_col)
    latin = empire.loc[empire["province"].isin(latin_provinces)].copy()

    # Recompute Mundlak centring over the Latin-only sample (correct centring
    # for THIS frame; matches the H3a template's Latin Sensitivity B logic).
    prov_means = latin.groupby("province")["log_pop"].transform("mean")
    latin["log_pop_prov_mean"] = prov_means
    latin["log_pop_within"] = latin["log_pop"] - prov_means
    province_codes = pd.Categorical(latin["province"])
    latin["province_idx"] = province_codes.codes
    latin["sample"] = "latin_primary"
    return latin.reset_index(drop=True)


def standardise_predictors(cities: pd.DataFrame) -> pd.DataFrame:
    """Sensitivity helper: return a copy with z-standardised Mundlak predictors
    (mean 0, SD 1 across cities in the given frame).

    Identical to the H3a template's `standardise_predictors`. Standardises
    log_pop_within and log_pop_prov_mean; the frame's province index and
    response are unchanged. Used by 02-h9-fit.py to re-fit with standardised
    predictors and report beta stability.
    """
    out = cities.copy()
    for col in ("log_pop_within", "log_pop_prov_mean"):
        mu = out[col].mean()
        sd = out[col].std(ddof=0)
        out[f"{col}_std"] = (out[col] - mu) / sd
    return out
