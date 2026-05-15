"""
Editorial-convention-hierarchy diagnostic — five tests.

Tests whether LIRE v3.0 endpoint dates (not_before, not_after) cluster at
sub-century boundaries beyond the known century-midpoint editorial artefact.

Run from project root:
    .venv/bin/python runs/2026-05-15-editorial-convention-hierarchy/scripts/run_tests.py

Outputs land in runs/2026-05-15-editorial-convention-hierarchy/outputs/.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage, stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
RUN_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
OUT_DIR = RUN_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Constants — analysis envelope, tier definitions, reign-boundary list
# ---------------------------------------------------------------------------
ENVELOPE_MIN, ENVELOPE_MAX = -50, 350

# Prereg's "century-midpoint" tier — the known editorial artefact.
CENTURY_MIDPOINT_YEARS = [50, 150, 250, 350]

# Century-boundary tier (the half-century complement to the midpoints).
CENTURY_BOUNDARY_YEARS = [0, 100, 200, 300]

# Quarter-century years in the envelope (excluding overlap with the above).
QUARTER_CENTURY_YEARS = [
    y for y in range(ENVELOPE_MIN, ENVELOPE_MAX + 1)
    if y % 100 in {25, 75}
]

# Decade years (multiples of 10, excluding centuries and half-centuries).
DECADE_YEARS = [
    y for y in range(ENVELOPE_MIN, ENVELOPE_MAX + 1)
    if y % 10 == 0 and y % 50 != 0
]

# Lustrum years (multiples of 5 ending in 5, excluding decades and others).
LUSTRUM_YEARS = [
    y for y in range(ENVELOPE_MIN, ENVELOPE_MAX + 1)
    if y % 10 == 5 and y % 25 not in {0, 25}  # exclude *_25 and *_75
]

# Well-attested emperor accession (and notable transition) years.
# Standard historical reference; first accession year used as the canonical
# boundary. Years are encoded as historical years (27 BC = -27).
REIGN_BOUNDARY_YEARS = [
    -27,   # Augustus formally takes "Augustus" title
    14,    # Tiberius
    37,    # Caligula
    41,    # Claudius
    54,    # Nero
    68,    # Galba
    69,    # Year of Four Emperors → Vespasian
    79,    # Titus
    81,    # Domitian
    96,    # Nerva
    98,    # Trajan
    117,   # Hadrian
    138,   # Antoninus Pius
    161,   # Marcus Aurelius (with Lucius Verus)
    180,   # Commodus
    193,   # Year of Five Emperors → Septimius Severus
    198,   # Caracalla (co-Augustus)
    211,   # Caracalla (sole) / Geta
    217,   # Macrinus
    218,   # Elagabalus
    222,   # Severus Alexander
    235,   # Maximinus Thrax — Crisis of the Third Century begins
    238,   # Gordian I/II, Pupienus & Balbinus, Gordian III
    244,   # Philip the Arab
    249,   # Decius
    251,   # Trebonianus Gallus
    253,   # Valerian / Gallienus
    260,   # Gallienus (sole)
    268,   # Claudius II Gothicus
    270,   # Aurelian
    275,   # Tacitus
    276,   # Probus
    282,   # Carus
    284,   # Diocletian — Tetrarchy
    305,   # Constantius I / Galerius
    306,   # Constantine I (Augustus in Britain)
    312,   # Battle of the Milvian Bridge
    324,   # Constantine I (sole)
    337,   # Constantius II / Constans / Constantine II
]
REIGN_BOUNDARY_SET = set(REIGN_BOUNDARY_YEARS)


def categorise_year(year: int) -> str:
    """Tag a year by its boundary type. Most-specific tag wins."""
    if year in CENTURY_MIDPOINT_YEARS:
        return "century-midpoint"
    if year in CENTURY_BOUNDARY_YEARS:
        return "century-boundary"
    if year % 100 in {25, 75}:
        return "quarter-century"
    if year in REIGN_BOUNDARY_SET:
        return "reign-related"
    if year % 10 == 0:
        return "decade"
    if year % 10 == 5:
        return "lustrum"
    return "other"


# ---------------------------------------------------------------------------
# Data loading + filtering (reproduces the preregistration's 180,609 rows)
# ---------------------------------------------------------------------------
def load_filtered_lire() -> pd.DataFrame:
    """Apply the prereg's filter exactly.

    Filter components:
      is_geotemporal := Latitude/Longitude/not_before/not_after non-null,
                        not_before <= not_after.
      is_within_RE   := province not null.
      Envelope       := not_after >= -50 AND not_before <= 350 (overlap, not
                        containment).
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
    filt = is_geotemporal & is_within_re & in_envelope
    sub = df.loc[filt].copy()
    sub["not_before"] = sub["not_before"].astype(int)
    sub["not_after"] = sub["not_after"].astype(int)
    return sub


# ---------------------------------------------------------------------------
# Test 1 — Top-N endpoint frequencies with category tagging
# ---------------------------------------------------------------------------
def test1_endpoint_frequencies(df: pd.DataFrame) -> None:
    """Top-50 most-frequent values for not_before and not_after, with tags."""
    out_dir = OUT_DIR / "test1-endpoint-frequencies"
    out_dir.mkdir(exist_ok=True)
    print("\n=== Test 1: top-N endpoint frequencies ===")
    for col in ("not_before", "not_after"):
        vc = df[col].value_counts().head(50).rename_axis("year").reset_index(name="count")
        vc["share_pct"] = 100 * vc["count"] / len(df)
        vc["category"] = vc["year"].apply(categorise_year)
        vc.to_csv(out_dir / f"top50_{col}.csv", index=False)
        print(f"  {col}: top 50 written → {out_dir / f'top50_{col}.csv'}")
        print(f"    leaders (year:count [tag]):")
        for _, r in vc.head(10).iterrows():
            print(f"      {int(r['year']):>5} : {int(r['count']):>7} [{r['category']}]")
    # Category-share rollup across the union of top 50s.
    rows = []
    for col in ("not_before", "not_after"):
        vc = df[col].value_counts().head(50)
        for year, cnt in vc.items():
            rows.append({"endpoint": col, "year": int(year), "count": int(cnt),
                         "category": categorise_year(int(year))})
    rollup = pd.DataFrame(rows)
    cat_summary = (
        rollup.groupby(["endpoint", "category"])["count"].agg(["sum", "size"])
        .rename(columns={"sum": "total_count", "size": "n_years"})
        .reset_index()
    )
    cat_summary.to_csv(out_dir / "category_rollup.csv", index=False)
    print(f"  category rollup → {out_dir / 'category_rollup.csv'}")


# ---------------------------------------------------------------------------
# Test 2 — Hierarchical O/E by tier
# ---------------------------------------------------------------------------
def _endpoint_counts(df: pd.DataFrame) -> pd.Series:
    """For every year in the envelope, count (not_before==y) + (not_after==y)."""
    years = np.arange(ENVELOPE_MIN, ENVELOPE_MAX + 1)
    nb_counts = df["not_before"].value_counts()
    na_counts = df["not_after"].value_counts()
    observed = pd.Series(0, index=years, dtype=int)
    for y in years:
        observed.loc[y] = int(nb_counts.get(y, 0)) + int(na_counts.get(y, 0))
    return observed


def _gaussian_expected(observed: pd.Series, sigma: float) -> pd.Series:
    """Smooth the observed-count curve to get an expected baseline.

    Approach: heavy Gaussian smoothing of the observed counts gives a baseline
    that approximates "what the curve would look like if editorial rounding
    weren't present" — sharp boundary spikes are flattened, broad underlying
    density is preserved.
    """
    arr = observed.to_numpy().astype(float)
    smoothed = ndimage.gaussian_filter1d(arr, sigma=sigma, mode="reflect")
    return pd.Series(smoothed, index=observed.index)


def test2_hierarchical_oe(df: pd.DataFrame) -> None:
    """Per-year and per-tier observed/expected at every boundary year."""
    out_dir = OUT_DIR / "test2-hierarchical-oe"
    out_dir.mkdir(exist_ok=True)
    print("\n=== Test 2: hierarchical O/E by tier ===")

    observed = _endpoint_counts(df)
    bandwidths = [5, 10, 20, 30]
    per_year_rows = []
    tier_rows = []

    tiers = {
        "century-midpoint": CENTURY_MIDPOINT_YEARS,
        "century-boundary": CENTURY_BOUNDARY_YEARS,
        "quarter-century": QUARTER_CENTURY_YEARS,
        "decade": DECADE_YEARS,
        "lustrum": LUSTRUM_YEARS,
        "reign-related": REIGN_BOUNDARY_YEARS,
    }

    for sigma in bandwidths:
        expected = _gaussian_expected(observed, sigma=sigma)
        for tier_name, years in tiers.items():
            valid_years = [y for y in years
                           if ENVELOPE_MIN <= y <= ENVELOPE_MAX]
            for y in valid_years:
                obs = int(observed.loc[y])
                exp = float(expected.loc[y])
                oe = obs / exp if exp > 0 else np.nan
                # Poisson tail: P(X >= obs | mean = exp).
                p_raw = float(stats.poisson.sf(obs - 1, exp)) if exp > 0 else np.nan
                per_year_rows.append({
                    "sigma": sigma, "tier": tier_name, "year": y,
                    "observed": obs, "expected": exp, "oe_ratio": oe,
                    "p_raw": p_raw,
                })
            # Tier-level summary: geometric mean of O/E.
            oes = [int(observed.loc[y]) / float(expected.loc[y])
                   for y in valid_years if float(expected.loc[y]) > 0]
            if oes:
                geo_mean = float(np.exp(np.mean(np.log(oes))))
                median = float(np.median(oes))
                mean = float(np.mean(oes))
                tier_rows.append({
                    "sigma": sigma, "tier": tier_name, "n_years": len(valid_years),
                    "geo_mean_oe": geo_mean, "mean_oe": mean, "median_oe": median,
                })

    per_year_df = pd.DataFrame(per_year_rows)
    # Holm-Bonferroni adjustment within each (sigma, tier) block.
    def _holm(group: pd.DataFrame) -> pd.DataFrame:
        p = group["p_raw"].to_numpy()
        n = len(p)
        order = np.argsort(p)
        ranks = np.empty(n, dtype=int)
        ranks[order] = np.arange(n)
        adj = np.empty(n, dtype=float)
        for i, idx in enumerate(order):
            adj[idx] = min(1.0, p[idx] * (n - i))
        # Enforce monotonicity in step-down.
        ordered_adj = adj[order]
        for i in range(1, n):
            ordered_adj[i] = max(ordered_adj[i], ordered_adj[i - 1])
        adj[order] = ordered_adj
        group = group.copy()
        group["p_holm"] = adj
        return group

    per_year_df = (
        per_year_df.groupby(["sigma", "tier"], group_keys=False).apply(_holm)
        .sort_values(["sigma", "tier", "year"])
    )
    per_year_df.to_csv(out_dir / "per_year_oe.csv", index=False)
    print(f"  per-year O/E → {out_dir / 'per_year_oe.csv'}")

    tier_df = pd.DataFrame(tier_rows).sort_values(["sigma", "geo_mean_oe"], ascending=[True, False])
    tier_df.to_csv(out_dir / "tier_summary.csv", index=False)
    print(f"  tier summary → {out_dir / 'tier_summary.csv'}")

    # Headline: tier ranking at sigma = 20.
    headline = tier_df[tier_df["sigma"] == 20].copy()
    print("  tier ranking at sigma=20 (descending geo-mean O/E):")
    for _, r in headline.iterrows():
        print(f"    {r['tier']:<20} n={int(r['n_years']):>3}  "
              f"geo-mean O/E = {r['geo_mean_oe']:.2f}  "
              f"median O/E = {r['median_oe']:.2f}")


# ---------------------------------------------------------------------------
# Test 3 — Trailing-two-digit histogram
# ---------------------------------------------------------------------------
def test3_trailing_digits(df: pd.DataFrame) -> None:
    out_dir = OUT_DIR / "test3-trailing-digits"
    out_dir.mkdir(exist_ok=True)
    print("\n=== Test 3: trailing-two-digit histogram ===")
    for col in ("not_before", "not_after"):
        # year mod 100, mapped to 0..99 for both positive and negative years.
        mod = df[col].astype(int).mod(100)
        hist = mod.value_counts().sort_index().reset_index()
        hist.columns = ["last_two_digits", "count"]
        hist["share_pct"] = 100 * hist["count"] / hist["count"].sum()
        hist.to_csv(out_dir / f"trailing_digits_{col}.csv", index=False)
        # Top-20 most-frequent residues for the print summary.
        top = hist.sort_values("count", ascending=False).head(20)
        print(f"  {col}: top 20 trailing-two-digit residues "
              f"(uniform-null share = 1 %):")
        for _, r in top.iterrows():
            print(f"    {int(r['last_two_digits']):>3} : "
                  f"{int(r['count']):>6}  ({r['share_pct']:.2f} %)")
        print(f"  → {out_dir / f'trailing_digits_{col}.csv'}")


# ---------------------------------------------------------------------------
# Test 4 — Reign-boundary specific test
# ---------------------------------------------------------------------------
def test4_reign_boundaries(df: pd.DataFrame) -> None:
    out_dir = OUT_DIR / "test4-reign-boundaries"
    out_dir.mkdir(exist_ok=True)
    print("\n=== Test 4: reign-boundary specific test ===")
    observed = _endpoint_counts(df)
    sigma = 20  # primary; matches Test 2 primary bandwidth
    expected = _gaussian_expected(observed, sigma=sigma)
    rows = []
    for y in REIGN_BOUNDARY_YEARS:
        if not (ENVELOPE_MIN <= y <= ENVELOPE_MAX):
            continue
        obs = int(observed.loc[y])
        exp = float(expected.loc[y])
        oe = obs / exp if exp > 0 else np.nan
        p_raw = float(stats.poisson.sf(obs - 1, exp)) if exp > 0 else np.nan
        rows.append({"year": y, "observed": obs, "expected": exp,
                     "oe_ratio": oe, "p_raw": p_raw})
    df_out = pd.DataFrame(rows).sort_values("p_raw")
    # Holm-Bonferroni across the reign-boundary family.
    p = df_out["p_raw"].to_numpy()
    n = len(p)
    adj = np.empty(n, dtype=float)
    order = np.argsort(p)
    for i, idx in enumerate(order):
        adj[idx] = min(1.0, p[idx] * (n - i))
    ordered_adj = adj[order]
    for i in range(1, n):
        ordered_adj[i] = max(ordered_adj[i], ordered_adj[i - 1])
    adj[order] = ordered_adj
    df_out["p_holm"] = adj
    df_out = df_out.sort_values("year")
    df_out.to_csv(out_dir / "reign_boundary_oe.csv", index=False)
    print(f"  → {out_dir / 'reign_boundary_oe.csv'}")
    sig = df_out[df_out["p_holm"] < 0.05]
    print(f"  Significant (Holm p < 0.05): {len(sig)} / {len(df_out)} reign-boundary years")
    if not sig.empty:
        for _, r in sig.head(15).iterrows():
            print(f"    AD {int(r['year']):>4}  obs={int(r['observed']):>6}  "
                  f"exp={r['expected']:>7.1f}  O/E={r['oe_ratio']:.2f}  "
                  f"p_holm={r['p_holm']:.2e}")


# ---------------------------------------------------------------------------
# Test 5 — Convention-text labelled subset
# ---------------------------------------------------------------------------
def test5_convention_text(df: pd.DataFrame) -> None:
    out_dir = OUT_DIR / "test5-convention-text"
    out_dir.mkdir(exist_ok=True)
    print("\n=== Test 5: convention-text labelled subset ===")
    if "raw_dating" not in df.columns:
        print("  raw_dating column not found — skipping Test 5.")
        return
    rd = df["raw_dating"].dropna().astype(str)
    print(f"  raw_dating non-null rows: {len(rd):,}")
    # 5.1 Top-50 distinct raw_dating values with modal endpoint pair.
    vc = rd.value_counts().head(50).rename_axis("raw_dating").reset_index(name="count")
    modal_rows = []
    for val in vc["raw_dating"]:
        sub = df[df["raw_dating"] == val]
        nb_mode = sub["not_before"].mode().iloc[0] if not sub["not_before"].mode().empty else np.nan
        na_mode = sub["not_after"].mode().iloc[0] if not sub["not_after"].mode().empty else np.nan
        modal_count = int(((sub["not_before"] == nb_mode) & (sub["not_after"] == na_mode)).sum())
        modal_rows.append({
            "raw_dating": val, "count": int(len(sub)),
            "modal_not_before": int(nb_mode) if not pd.isna(nb_mode) else None,
            "modal_not_after": int(na_mode) if not pd.isna(na_mode) else None,
            "modal_pair_count": modal_count,
            "modal_pair_share_pct": 100.0 * modal_count / len(sub) if len(sub) else 0.0,
        })
    top_df = pd.DataFrame(modal_rows)
    top_df.to_csv(out_dir / "top50_raw_dating.csv", index=False)
    print(f"  top-50 raw_dating values → {out_dir / 'top50_raw_dating.csv'}")
    print("  top 15 raw_dating values + modal endpoints:")
    for _, r in top_df.head(15).iterrows():
        rd_short = (r["raw_dating"][:50] + "…") if len(r["raw_dating"]) > 50 else r["raw_dating"]
        print(f"    {r['count']:>6} × '{rd_short}'  →  "
              f"({r['modal_not_before']}, {r['modal_not_after']}) "
              f"[{r['modal_pair_share_pct']:.0f}% modal]")

    # 5.2 Regex-pattern aggregations.
    patterns = {
        "century": re.compile(r"\bsaec\.?|\bcentury\b|\bcent\.\s|c\.|cent\b", re.IGNORECASE),
        "early-X": re.compile(r"\b(init|inc|princ|earl|fr[uü]h|debut|prim)", re.IGNORECASE),
        "mid-X":   re.compile(r"\b(med\.?|middl|mitte)", re.IGNORECASE),
        "late-X":  re.compile(r"\b(fin|exit|spaet|sp[äa]t|late|fin\.\s)", re.IGNORECASE),
        "reign":   re.compile(r"\b(imp\.|reign|rule of|regn)", re.IGNORECASE),
        "numeric_year": re.compile(r"\b\d{2,4}\b"),
    }
    pattern_rows = []
    for name, regex in patterns.items():
        mask = rd.str.contains(regex)
        idx = mask[mask].index
        if len(idx) == 0:
            continue
        nb_vals = df.loc[idx, "not_before"]
        na_vals = df.loc[idx, "not_after"]
        # Tag endpoints by year-category, take share of round-numbers (00 / 50).
        nb_round = ((nb_vals % 100 == 0) | (nb_vals % 100 == 50)).mean()
        na_round = ((na_vals % 100 == 0) | (na_vals % 100 == 50)).mean()
        pattern_rows.append({
            "pattern": name, "n_rows": int(len(idx)),
            "nb_share_round_centhalf": float(nb_round),
            "na_share_round_centhalf": float(na_round),
            "nb_modal": int(nb_vals.mode().iloc[0]) if not nb_vals.mode().empty else None,
            "na_modal": int(na_vals.mode().iloc[0]) if not na_vals.mode().empty else None,
        })
    pat_df = pd.DataFrame(pattern_rows).sort_values("n_rows", ascending=False)
    pat_df.to_csv(out_dir / "pattern_aggregation.csv", index=False)
    print(f"  pattern aggregation → {out_dir / 'pattern_aggregation.csv'}")
    print("  pattern share of round-number endpoints (00 or 50):")
    for _, r in pat_df.iterrows():
        print(f"    {r['pattern']:<14} n={int(r['n_rows']):>6}  "
              f"nb-round={r['nb_share_round_centhalf']:.2f}  "
              f"na-round={r['na_share_round_centhalf']:.2f}  "
              f"modal=({r['nb_modal']}, {r['na_modal']})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"Loading LIRE v3.0 from {DATA_PATH}")
    df = load_filtered_lire()
    n = len(df)
    print(f"Filtered corpus: {n:,} rows (expected 180,609 per the preregistration)")
    if n != 180609:
        print(f"  WARNING: filter row count differs from 180,609; investigate.")

    test1_endpoint_frequencies(df)
    test2_hierarchical_oe(df)
    test3_trailing_digits(df)
    test4_reign_boundaries(df)
    test5_convention_text(df)

    print("\nAll five tests complete. Outputs under:")
    print(f"  {OUT_DIR}")


if __name__ == "__main__":
    main()
