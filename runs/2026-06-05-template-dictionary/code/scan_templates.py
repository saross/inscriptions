#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_templates.py --- Exploratory template-frequency scan of LIRE v3.0.

Purpose
-------
PART 1 (read-only measurement) of the pre-Phase-2 template-dictionary design
artefact required by the preregistration (line 202) and Decision 20: enumerate
the exact-match ``[not_before, not_after]`` interval templates in the filtered
LIRE v3.0 corpus, so the N >= threshold inclusion rule for the convention
component can be *pinned from the empirical frequency distribution* rather than
guessed a priori.

This script COMMITS NOTHING. It produces the measurement (ranked template
frequencies, cumulative-coverage curve, a provisional descriptive tier-
classification) from which Shawn and CC choose the threshold and tier structure
in PART 2, which then writes the committed ``design.json`` dictionary the mixture
model consumes (``cell_lib.build_tier_basis``).

Why this is needed
------------------
The H2.1 recovery grid (``runs/2026-05-22-recovery-grid-design/design.json``)
used a *hand-curated* ``template_intervals_by_tier`` dictionary (century /
half-century / reign tiers, candidate intervals from the prereg). No mixture has
ever been fit on real LIRE under the Decision-20 three-tier structure. A quick
peek shows the curated dictionary does not match the corpus: the single most
frequent template is the multi-century slab ``[301, 500]`` (8.8%), and several
high-frequency templates (multi-century slabs; odd 60-year bands like
``[71, 130]``) map onto none of the three curated tiers. This scan quantifies
that, surfacing the templates that force the Decision-20 revisit trigger.

Method
------
* Reproduce the preregistration's 180,609-row filter exactly (is_geotemporal AND
  is_within_RE AND envelope-overlap with 50 BC - AD 350), identical to
  ``runs/2026-05-17-interval-width-diagnostic/code/interval_width_diagnostic.py``.
* Also derive the Latin-speaking-province subset (Decision 36 primary frame) via
  the externalised province-language map (``language == 'Latin'``).
* For both frames: count exact ``(not_before, not_after)`` pairs; report width
  (inclusive-Roman ``na - nb + 1``), N, and share of corpus.
* Exclude year-precise (``nb == na``) templates from the convention candidate
  pool -- per Decision 20 these stay in ``genuine_SPA`` as real ancient anchoring.
* Provisional descriptive tier-classification (NOT the committed assignment):
  year_precise / century / half_century / reign / multi_century /
  bc_ad_boundary / other. The point is to show how much high-frequency mass falls
  into ``other`` (outside the curated three tiers).
* Cumulative-coverage curve + candidate-threshold table (N >= 50/100/200/500/1000
  and top-K), with the within-envelope overlap fraction for wide templates.

Inputs
------
archive/data-2026-04-22/LIRE_v3-0.parquet  (read-only; raw LIRE v3.0)
runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv  (Latin frame)

Outputs (all under runs/2026-06-05-template-dictionary/outputs/)
-------
tables/templates-empire.csv   -- full ranked template list, empire frame
tables/templates-latin.csv    -- full ranked template list, Latin frame
tables/threshold-coverage.csv -- coverage at candidate thresholds (both frames)
tables/category-mass.csv      -- convention-pool mass per provisional category
REPORT.md                     -- headline findings + decision-relevant summary

Date
----
2026-06-05

Author / Who-asked
------------------
Shawn Ross (PI); analysis by Claude Code (Opus 4.8, 1M context) on Shawn's brief,
as the H2.1 mixture-run prerequisite (Decision 37 next-session action 1).

Reproducibility
---------------
random_seed = 20260605 (recorded for ritual consistency; the scan is
deterministic -- pure counting, no resampling).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 20260605
np.random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------------
# Paths -- resolved relative to this script so the run is portable.
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = (
    PROJECT_ROOT
    / "runs"
    / "2026-06-04-h3a-confirmatory"
    / "data"
    / "province-language-map.csv"
)
OUT_DIR = RUN_DIR / "outputs"
TBL_DIR = OUT_DIR / "tables"
REPORT_PATH = OUT_DIR / "REPORT.md"
TBL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Analysis envelope -- the 50 BC to AD 350 window (prereg; 80 x 5-year bins).
# ---------------------------------------------------------------------------
ENVELOPE_MIN = -50
ENVELOPE_MAX = 350

# Expected filtered row count (prereg; reproduced by the 2026-05-17 diagnostic).
EXPECTED_N = 180_609

# Candidate N-thresholds to tabulate (the actual pin is chosen in PART 2).
CANDIDATE_THRESHOLDS = [50, 100, 200, 500, 1000]

# ---------------------------------------------------------------------------
# Canonical reign-interval lookup (Principate, Latin-relevant). Used ONLY for
# provisional descriptive labelling -- an empirical (nb, na) template is tagged
# `reign:<name>` if it matches one of these within +/- REIGN_TOL years on both
# endpoints. Dates are the conventional accession/death years; sources vary by a
# year, hence the tolerance. NOT a model commitment.
# ---------------------------------------------------------------------------
REIGN_TOL = 1
CANONICAL_REIGNS: dict[str, tuple[int, int]] = {
    "Augustan": (-27, 14),
    "Tiberian": (14, 37),
    "Caligulan": (37, 41),
    "Claudian": (41, 54),
    "Neronian": (54, 68),
    "Vespasianic": (69, 79),
    "Flavian": (69, 96),
    "Domitianic": (81, 96),
    "Nervan-Trajanic": (96, 117),
    "Trajanic": (98, 117),
    "Hadrianic": (117, 138),
    "Antonine-Pius": (138, 161),
    "Aurelian-Marcus": (161, 180),
    "Antonine-broad": (138, 192),
    "Commodan": (180, 192),
    "Severan-dynasty": (193, 235),
    "Septimius-Severus": (193, 211),
    "Caracallan": (212, 217),
    "Soldier-emperors": (235, 284),
    "Tetrarchic": (284, 305),
    "Constantinian": (306, 337),
}


# ---------------------------------------------------------------------------
# Data loading + filtering
# ---------------------------------------------------------------------------
def load_filtered_lire() -> pd.DataFrame:
    """Load LIRE v3.0 and apply the preregistration filter.

    Returns a DataFrame with integer ``nb`` / ``na`` columns, an inclusive-Roman
    ``width`` column, and the original ``province`` column (for the Latin split).
    Row count must equal ``EXPECTED_N`` (180,609); raises if not.

    The filter is identical to ``load_filtered_lire`` in the 2026-05-17
    interval-width diagnostic and the editorial-convention-hierarchy run.
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
    in_envelope = (df["not_after"] >= ENVELOPE_MIN) & (df["not_before"] <= ENVELOPE_MAX)

    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["nb"] = sub["not_before"].astype(int)
    sub["na"] = sub["not_after"].astype(int)
    # Inclusive-Roman width: [1, 100] is 100 years wide (matches the diagnostic
    # and Decision 20's "[1, 100] is 100 years wide"). NB the model basis builder
    # `cell_lib.build_tier_basis` uses the EXCLUSIVE width = hi - lo for its mass
    # normalisation; that is a downstream convention and does not affect counting.
    sub["width"] = sub["na"] - sub["nb"] + 1

    if len(sub) != EXPECTED_N:
        raise ValueError(
            f"Filtered corpus is {len(sub):,} rows; expected {EXPECTED_N:,}. "
            "The prereg filter has drifted -- investigate before trusting the scan."
        )
    return sub


def latin_province_set() -> set[str]:
    """Return the set of LIRE ``province`` names flagged Latin-speaking.

    Source: the externalised province-language map used by the H3a Sensitivity-B
    (Latin) frame (Decision 36). Keyed on ``lire_province``; ``language ==
    'Latin'`` selected. The 39-vs-41 reconciliation is an open Amendment-02 item
    (Decision 37 D2); this scan uses the map as-committed and reports the N it
    yields.
    """
    lang_map = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    latin = set(lang_map.loc[lang_map["language"] == "Latin", "lire_province"])
    return latin


# ---------------------------------------------------------------------------
# Provisional descriptive tier-classification (NOT the committed assignment)
# ---------------------------------------------------------------------------
def classify_template(nb: int, na: int) -> str:
    """Assign a provisional descriptive category to a template ``[nb, na]``.

    Precedence: year_precise -> reign -> century -> half_century ->
    multi_century -> bc_ad_boundary -> other. Inclusive-Roman width.

    The categories are descriptive aids for the threshold/tier decision in PART
    2, NOT the committed tier assignment. ``other`` is the decision-relevant
    bucket: high-frequency ``other`` templates are the ones that do not fit the
    curated century/half-century/reign tiers and trigger Decision 20's revisit
    condition.
    """
    width = na - nb + 1

    if nb == na:
        return "year_precise"

    # Reign: exact-ish match to a canonical reign interval (+/- REIGN_TOL).
    for name, (rlo, rhi) in CANONICAL_REIGNS.items():
        if abs(nb - rlo) <= REIGN_TOL and abs(na - rhi) <= REIGN_TOL:
            return f"reign:{name}"

    # Century: width 100, aligned to a century boundary (nb in ..., -99, 1, 101, ...).
    if width == 100 and (nb - 1) % 100 == 0:
        return "century"

    # Half-century: width 50, aligned to a 50-year boundary (nb in ..., 1, 51, 101, ...).
    if width == 50 and (nb - 1) % 50 == 0:
        return "half_century"

    # Multi-century: width a multiple of 50 and > 100, aligned to a 50-year
    # boundary (captures [1, 200], [101, 300], [1, 300], [301, 500], [151, 300]).
    if width > 100 and width % 50 == 0 and (nb - 1) % 50 == 0:
        return "multi_century"

    # BC-AD boundary: spans 1 BC / AD 1 (nb <= 0 <= na in proleptic terms; there
    # is no year 0, so the boundary is between nb<=-1 ... na>=1). Decision 20 / 9
    # flags the +1,159 boundary step as an unmodelled known limitation.
    if nb <= -1 and na >= 1:
        return "bc_ad_boundary"

    return "other"


# ---------------------------------------------------------------------------
# Envelope overlap fraction (how much of a wide template lands inside [-50, 350])
# ---------------------------------------------------------------------------
def envelope_overlap_fraction(nb: int, na: int) -> float:
    """Fraction of a template's inclusive-Roman width that lies in the envelope.

    Wide/late templates such as ``[301, 500]`` extend beyond AD 350 and deposit
    convention mass only on their in-envelope portion ([301, 350] = 50/200 = 0.25
    of their width). Reported so the decision accounts for effective in-envelope
    contribution, not just raw frequency.
    """
    width = na - nb + 1
    lo = max(nb, ENVELOPE_MIN)
    hi = min(na, ENVELOPE_MAX)
    overlap = max(0, hi - lo + 1)
    return overlap / width


# ---------------------------------------------------------------------------
# Per-frame template table
# ---------------------------------------------------------------------------
def build_template_table(df: pd.DataFrame, frame_n: int) -> pd.DataFrame:
    """Return a ranked exact-template frequency table for one frame.

    Columns: nb, na, width, category, n, share_corpus, env_overlap_frac,
    cum_n, cum_share_corpus. Sorted by n descending.
    """
    grp = (
        df.groupby(["nb", "na"]).size().reset_index(name="n").sort_values(
            "n", ascending=False
        )
    )
    grp["width"] = grp["na"] - grp["nb"] + 1
    grp["category"] = [classify_template(int(nb), int(na)) for nb, na in zip(grp["nb"], grp["na"])]
    grp["env_overlap_frac"] = [
        round(envelope_overlap_fraction(int(nb), int(na)), 4)
        for nb, na in zip(grp["nb"], grp["na"])
    ]
    grp["share_corpus"] = grp["n"] / frame_n
    grp["cum_n"] = grp["n"].cumsum()
    grp["cum_share_corpus"] = grp["cum_n"] / frame_n
    return grp.reset_index(drop=True)


def coverage_at_thresholds(
    tbl: pd.DataFrame, frame_n: int, frame_label: str
) -> pd.DataFrame:
    """Coverage summary at each candidate N-threshold for one frame.

    The convention pool excludes year_precise templates (they stay in genuine).
    Reports, at each threshold: #templates included, % of full corpus covered,
    and % of the convention pool covered.
    """
    pool = tbl.loc[tbl["category"] != "year_precise"]
    pool_n = int(pool["n"].sum())
    rows = []
    for thr in CANDIDATE_THRESHOLDS:
        inc = pool.loc[pool["n"] >= thr]
        inc_n = int(inc["n"].sum())
        rows.append(
            {
                "frame": frame_label,
                "threshold": thr,
                "n_templates": int(len(inc)),
                "inscriptions_covered": inc_n,
                "pct_of_corpus": round(100 * inc_n / frame_n, 2),
                "pct_of_convention_pool": round(100 * inc_n / pool_n, 2)
                if pool_n
                else 0.0,
            }
        )
    return pd.DataFrame(rows)


def category_mass(tbl: pd.DataFrame, frame_label: str) -> pd.DataFrame:
    """Convention-pool inscription mass per provisional category (one frame).

    ``reign:*`` sub-labels are collapsed to ``reign``. Year-precise excluded.
    Surfaces how much mass sits in ``other`` / ``multi_century`` /
    ``bc_ad_boundary`` -- the categories outside the curated three tiers.
    """
    pool = tbl.loc[tbl["category"] != "year_precise"].copy()
    pool["cat_group"] = pool["category"].str.split(":").str[0]
    pool_n = int(pool["n"].sum())
    agg = (
        pool.groupby("cat_group")
        .agg(n_templates=("n", "size"), inscriptions=("n", "sum"))
        .reset_index()
        .sort_values("inscriptions", ascending=False)
    )
    agg["frame"] = frame_label
    agg["pct_of_convention_pool"] = (100 * agg["inscriptions"] / pool_n).round(2)
    return agg[["frame", "cat_group", "n_templates", "inscriptions", "pct_of_convention_pool"]]


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def _fmt_template_row(r: pd.Series) -> str:
    return (
        f"| `[{int(r['nb'])}, {int(r['na'])}]` | {int(r['width'])} | "
        f"{r['category']} | {int(r['n']):,} | {100*r['share_corpus']:.2f}% | "
        f"{r['env_overlap_frac']:.2f} |"
    )


def write_report(
    emp: pd.DataFrame,
    lat: pd.DataFrame,
    emp_n: int,
    lat_n: int,
    cov: pd.DataFrame,
    cat: pd.DataFrame,
) -> None:
    """Compose the Markdown findings report (decision-oriented, no commitment)."""
    emp_pool = emp.loc[emp["category"] != "year_precise"]
    emp_yp = emp.loc[emp["category"] == "year_precise"]
    L: list[str] = []
    L.append("# Template-dictionary empirical scan --- PART 1 (measurement)")
    L.append("")
    L.append("**Date:** 2026-06-05  ")
    L.append("**Author:** Claude Code (Opus 4.8) on Shawn Ross's brief  ")
    L.append(
        "**Status:** read-only measurement. **Commits nothing.** Inputs to the "
        "PART-2 threshold/tier decision and the committed `design.json`."
    )
    L.append("")
    L.append(
        "Prerequisite for the real-data H2.1 mixture run (prereg line 202; "
        "Decision 20; audit A2; Decision 37 next-session action 1). Enumerates "
        "exact-match `[not_before, not_after]` templates so the N >= threshold "
        "inclusion rule is pinned from the empirical distribution."
    )
    L.append("")
    L.append("## Corpus")
    L.append("")
    L.append(f"- **Empire frame** (prereg filter): {emp_n:,} inscriptions.")
    L.append(
        f"- **Latin frame** (Decision 36; `language=='Latin'` provinces): "
        f"{lat_n:,} inscriptions."
    )
    L.append(
        f"- **Unique exact templates (empire):** {len(emp):,} "
        f"({len(emp_pool):,} non-year-precise + {len(emp_yp):,} year-precise types)."
    )
    L.append(
        f"- **Year-precise (`nb==na`) inscriptions (empire):** "
        f"{int(emp_yp['n'].sum()):,} "
        f"({100*int(emp_yp['n'].sum())/emp_n:.2f}% of corpus) --- excluded from the "
        "convention pool per Decision 20 (stay in `genuine_SPA`)."
    )
    L.append("")
    L.append(
        "> **Reconciliation note.** Decision 20's context (line 1671) records "
        "\"`[1, 100]` 26.3% of corpus\". The direct re-scan gives `[1, 100]` = "
        f"{int(emp.loc[(emp['nb']==1)&(emp['na']==100),'n'].iloc[0]):,} "
        f"({100*emp.loc[(emp['nb']==1)&(emp['na']==100),'share_corpus'].iloc[0]:.2f}%). "
        "The ~26% figure corresponds instead to the century-template *class* "
        "collectively, not `[1, 100]` alone --- a stale specific, corrected here."
    )
    L.append("")
    L.append("## Top 25 templates --- empire frame")
    L.append("")
    L.append("| Template `[nb, na]` | width | provisional category | N | share | env-overlap |")
    L.append("|---|---|---|---|---|---|")
    for _, r in emp.head(25).iterrows():
        L.append(_fmt_template_row(r))
    L.append("")
    L.append(
        "`env-overlap` = fraction of the template's width inside [50 BC, AD 350]; "
        "wide/late slabs (e.g. `[301, 500]`) deposit convention mass only on their "
        "in-envelope portion."
    )
    L.append("")
    L.append("## Provisional category mass (convention pool; year-precise excluded)")
    L.append("")
    L.append("| frame | category | #templates | inscriptions | % of convention pool |")
    L.append("|---|---|---|---|---|")
    for _, r in cat.iterrows():
        L.append(
            f"| {r['frame']} | {r['cat_group']} | {int(r['n_templates']):,} | "
            f"{int(r['inscriptions']):,} | {r['pct_of_convention_pool']:.2f}% |"
        )
    L.append("")
    L.append(
        "**Decision-relevant finding.** The curated recovery-grid dictionary had "
        "only three tiers (century / half_century / reign). The empirical scan "
        "shows substantial convention-pool mass in **`multi_century`**, "
        "**`bc_ad_boundary`**, and **`other`** --- templates that fit none of the "
        "three curated tiers. This is Decision 20's revisit trigger: the tier "
        "structure likely needs revision (a multi-century-slab tier; possibly a "
        "BC-AD-boundary tier; an explicit `other`/residual-band policy)."
    )
    L.append("")
    L.append("## Coverage at candidate N-thresholds")
    L.append("")
    L.append(
        "Convention pool = non-year-precise templates. `pct_of_corpus` is of the "
        "whole frame; `pct_of_convention_pool` is of non-year-precise inscriptions."
    )
    L.append("")
    L.append("| frame | N>= | #templates | inscriptions | % of corpus | % of convention pool |")
    L.append("|---|---|---|---|---|---|")
    for _, r in cov.iterrows():
        L.append(
            f"| {r['frame']} | {int(r['threshold'])} | {int(r['n_templates']):,} | "
            f"{int(r['inscriptions_covered']):,} | {r['pct_of_corpus']:.2f}% | "
            f"{r['pct_of_convention_pool']:.2f}% |"
        )
    L.append("")
    L.append("## High-frequency `other` templates (empire; N >= 200, category=other)")
    L.append("")
    L.append(
        "These are the templates that do not fit century/half-century/reign --- "
        "the ones the PART-2 tier decision must place or exclude."
    )
    L.append("")
    L.append("| Template `[nb, na]` | width | N | share | env-overlap |")
    L.append("|---|---|---|---|---|")
    other_hi = emp.loc[(emp["category"] == "other") & (emp["n"] >= 200)]
    for _, r in other_hi.iterrows():
        L.append(
            f"| `[{int(r['nb'])}, {int(r['na'])}]` | {int(r['width'])} | "
            f"{int(r['n']):,} | {100*r['share_corpus']:.2f}% | {r['env_overlap_frac']:.2f} |"
        )
    L.append("")
    L.append("## Outputs")
    L.append("")
    L.append("- `tables/templates-empire.csv` --- full ranked template list (empire).")
    L.append("- `tables/templates-latin.csv` --- full ranked template list (Latin).")
    L.append("- `tables/threshold-coverage.csv` --- coverage at candidate thresholds.")
    L.append("- `tables/category-mass.csv` --- convention-pool mass per category.")
    L.append("")
    L.append("## Next (PART 2 --- needs Shawn sign-off; commits the artefact)")
    L.append("")
    L.append("1. Choose the N-threshold from this distribution.")
    L.append("2. Decide the tier structure (resolve `multi_century` / `bc_ad_boundary` / `other`).")
    L.append("3. Write + commit `design.json` (`template_intervals_by_tier`) the mixture consumes.")
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"random_seed = {RANDOM_SEED}")
    print(f"Loading {DATA_PATH} ...")
    df = load_filtered_lire()
    emp_n = len(df)
    print(f"  empire-filtered rows: {emp_n:,} (expected {EXPECTED_N:,})")

    latin = latin_province_set()
    df_lat = df.loc[df["province"].isin(latin)].copy()
    lat_n = len(df_lat)
    print(f"  Latin-frame rows: {lat_n:,} (Decision 37 D1 quotes 109,646)")

    print("Building empire template table ...")
    emp = build_template_table(df, emp_n)
    emp.to_csv(TBL_DIR / "templates-empire.csv", index=False)

    print("Building Latin template table ...")
    lat = build_template_table(df_lat, lat_n)
    lat.to_csv(TBL_DIR / "templates-latin.csv", index=False)

    print("Coverage + category tables ...")
    cov = pd.concat(
        [
            coverage_at_thresholds(emp, emp_n, "empire"),
            coverage_at_thresholds(lat, lat_n, "latin"),
        ],
        ignore_index=True,
    )
    cov.to_csv(TBL_DIR / "threshold-coverage.csv", index=False)

    cat = pd.concat(
        [category_mass(emp, "empire"), category_mass(lat, "latin")],
        ignore_index=True,
    )
    cat.to_csv(TBL_DIR / "category-mass.csv", index=False)

    print("Writing REPORT.md ...")
    write_report(emp, lat, emp_n, lat_n, cov.loc[cov["frame"] == "empire"].reset_index(drop=True),
                 cat.loc[cat["frame"] == "empire"].reset_index(drop=True))
    print(f"  -> {REPORT_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
