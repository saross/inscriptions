"""
Independent verifier for data-profile-scout output on LIRE v3.0.

Re-computes every claim in claims.jsonl from the parquet using an
independent code path. Does NOT consume the scout's CSV tables.
Writes verified_values.jsonl with {claim_id, scout_value, my_value, match, tolerance_type, notes}.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# Tolerances per brief
PP_TOL = 0.1  # percentage points
REL_TOL_CHISQ = 0.005  # 0.5 % relative
REL_TOL_FLOAT = 0.001  # 0.1 % relative

PARQUET = "/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet"
CLAIMS = "/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/claims.jsonl"
OUT = "/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/verifier-work/verified_values.jsonl"
SCHEMA = "/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/seed/LI_metadata.csv"


# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------
df = pd.read_parquet(PARQUET)
N = len(df)
print(f"[load] parquet shape = {df.shape}")

# Load schema for column-count claim
try:
    schema_df = pd.read_csv(SCHEMA)
    N_SCHEMA = len(schema_df)
except Exception:
    try:
        schema_df = pd.read_csv(SCHEMA, sep=";")
        N_SCHEMA = len(schema_df)
    except Exception as e:
        print(f"[warn] schema csv read failed: {e}")
        N_SCHEMA = None


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------
def decimals_count(x):
    """Count decimal places in the string repr of a float, ignoring trailing zeros.

    The scout used this to compute coordinate precision. Returns 0 if x is na.
    """
    if pd.isna(x):
        return None
    s = f"{x:.15f}".rstrip("0").rstrip(".")
    if "." in s:
        return len(s.split(".")[1])
    return 0


# Pre-compute series
nb = df["not_before"]
na_ = df["not_after"]
lat = df["Latitude"]
lon = df["Longitude"]
date_range = (na_ - nb)

# Pre-compute lat/lon decimals once (slow — only run if needed)
_lat_dec_cache = None
_lon_dec_cache = None


def lat_decimals():
    global _lat_dec_cache
    if _lat_dec_cache is None:
        _lat_dec_cache = lat.dropna().apply(decimals_count)
    return _lat_dec_cache


def lon_decimals():
    global _lon_dec_cache
    if _lon_dec_cache is None:
        _lon_dec_cache = lon.dropna().apply(decimals_count)
    return _lon_dec_cache


# -----------------------------------------------------------
# Basic pre-computed tallies
# -----------------------------------------------------------
province_col = "province"
province_ser = df[province_col]
province_valid = province_ser.notna() & (province_ser.fillna("").str.strip() != "")
province_valid_count = int(province_valid.sum())
province_nunique = int(province_ser[province_valid].nunique())
province_counts = province_ser[province_valid].value_counts()

urban_col = "urban_context_city"
urban_ser = df[urban_col]
urban_valid = urban_ser.notna() & (urban_ser.fillna("").str.strip() != "")
urban_valid_count = int(urban_valid.sum())
urban_nunique = int(urban_ser[urban_valid].nunique())
urban_counts = urban_ser[urban_valid].value_counts()


# Per-group detail (to verify mean/median claims for threshold 100)
def _group_detail(col, counts, threshold):
    keep = counts[counts >= threshold].index
    detail = pd.DataFrame({"group": keep, "count": counts.loc[keep].values})
    # lat null rate and not_before null rate per group
    mask = df[col].isin(keep)
    grp = df.loc[mask].groupby(col)
    lat_null_rate = grp["Latitude"].apply(lambda s: s.isna().mean())
    nb_null_rate = grp["not_before"].apply(lambda s: s.isna().mean())
    detail["lat_null_rate"] = detail["group"].map(lat_null_rate).values
    detail["not_before_null_rate"] = detail["group"].map(nb_null_rate).values
    return detail


province_detail_100 = _group_detail("province", province_counts, 100)
urban_detail_100 = _group_detail("urban_context_city", urban_counts, 100)


# -----------------------------------------------------------
# midpoint-inflation
# -----------------------------------------------------------
def midpoint_inflation(target_year, window=15):
    midpoints = ((nb + na_) / 2).round()
    count_at = int((midpoints == target_year).sum())
    win_mask = (midpoints >= target_year - window) & (midpoints <= target_year + window)
    count_win_total = int(win_mask.sum())
    count_off = count_win_total - count_at
    # scout: chi-square on [obs_t, obs_o] vs expected uniform across (2*window + 1) = 31 bins
    n_bins = 2 * window + 1
    total = count_win_total
    expected_t = total / n_bins
    expected_o = total * (n_bins - 1) / n_bins
    chi2, pval = stats.chisquare([count_at, count_off], [expected_t, expected_o])
    return {"count_at": count_at, "count_off": count_off,
            "expected_t": expected_t, "chi2": float(chi2), "p": float(pval)}


midpoint_results = {y: midpoint_inflation(y) for y in (50, 150, 250, 350)}


# -----------------------------------------------------------
# editorial-spikes
# -----------------------------------------------------------
def editorial_spike(col, y, half_window=5):
    s = df[col]
    count_at = int((s == y).sum())
    neighbours = [int((s == (y + d)).sum()) for d in range(-half_window, half_window + 1) if d != 0]
    mean_n = float(np.mean(neighbours))
    total_n = int(np.sum(neighbours))
    # scout: chi-square on [count_at, count_in_neighbours] vs uniform 10-bin expectation
    # 10 neighbours + 1 target = 11 cells, uniform expected:
    # Actually scout row header says "Chi-square is computed on [count_at_year, count_in_neighbours] vs uniform"
    # From the numbers (chi2=71.841 for count_at=20, neighbours=1095, mean_n=109.5):
    # uniform across 11 bins would give expected_t = 101.36, expected_rest = 1013.6
    # chi2 = (20-101.36)^2/101.36 + (1095-1013.6)^2/1013.6 = 65.37 + 6.54 = 71.91 ~= 71.841
    total = count_at + total_n
    n_bins = 2 * half_window + 1  # 11
    expected_t = total / n_bins
    expected_o = total * (n_bins - 1) / n_bins
    chi2, pval = stats.chisquare([count_at, total_n], [expected_t, expected_o])
    return {"count_at": count_at, "mean_neighbours": mean_n,
            "total_neighbours": total_n, "chi2": float(chi2), "p": float(pval)}


editorial_cols = ["not_before", "not_after"]
editorial_years = [-14, 27, 97, 192, 193, 212, 235]
editorial_results = {}
for c in editorial_cols:
    for y in editorial_years:
        editorial_results[(c, y)] = editorial_spike(c, y)


# -----------------------------------------------------------
# Granularity categories
# -----------------------------------------------------------
def granularity_categories(d):
    """Replicate scout granularity categorisation.

    NOTE: scout claim description says "10,20,30,...,500" but source code uses a
    discrete hardcoded set {10,20,30,40,60,70,75,80,90,125,150,175,250,300,400,500}.
    We verify against the scout's *actual* code (discrete set) to establish whether
    the number claimed (3,971) reproduces. The misleading description is noted as
    a semantic finding, not a numerical correction.
    """
    d_nn = d.dropna().round().astype(int)
    total = len(d_nn)
    cats = {
        "eq_0": int((d_nn == 0).sum()),
        "eq_25": int((d_nn == 25).sum()),
        "eq_50": int((d_nn == 50).sum()),
        "99_to_101": int(((d_nn >= 99) & (d_nn <= 101)).sum()),
        "199_to_201": int(((d_nn >= 199) & (d_nn <= 201)).sum()),
    }
    # Exact scout set from profile_lire_v30.py line 971
    round_values = {10, 20, 30, 40, 60, 70, 75, 80, 90, 125, 150, 175, 250, 300, 400, 500}
    cats["other_round"] = int(d_nn.isin(round_values).sum())
    # Scout derives irregular as total - sum of above categories
    cats["irregular"] = total - sum(cats.values())
    return cats, total


gran_cats, gran_total = granularity_categories(date_range)


# -----------------------------------------------------------
# Broad histogram buckets
# -----------------------------------------------------------
def broad_histogram(d):
    d_nn = d.dropna()
    return {
        "<=1": int((d_nn <= 1).sum()),
        "2..25": int(((d_nn >= 2) & (d_nn <= 25)).sum()),
        "26..50": int(((d_nn >= 26) & (d_nn <= 50)).sum()),
        "51..100": int(((d_nn >= 51) & (d_nn <= 100)).sum()),
        "101..200": int(((d_nn >= 101) & (d_nn <= 200)).sum()),
        "201..500": int(((d_nn >= 201) & (d_nn <= 500)).sum()),
        ">500": int((d_nn > 500).sum()),
    }


broad_hist = broad_histogram(date_range)


# -----------------------------------------------------------
# Null profile helpers
# -----------------------------------------------------------
null_rate_pct = (df.isna().mean() * 100).round(6)


# -----------------------------------------------------------
# Claim-specific calculators (dispatched by claim_id)
# -----------------------------------------------------------
# Province top-20 list
top20_province = province_counts.head(20)
top20_urban = urban_counts.head(20)


def get_my_value(claim):
    cid = claim["claim_id"]
    desc = claim["description"]
    cat = claim["category"]

    # Simple counts and schema
    if cid == "c0001":
        return N
    if cid == "c0002":
        return df.shape[1]
    if cid == "c0003":
        return N_SCHEMA
    if cid == "c0004":
        return int((df.isna().mean() > 0.5).sum())
    if cid == "c0005":
        return int((nb.notna() & na_.notna()).sum())
    if cid == "c0006":
        return int(nb.isna().sum())
    if cid == "c0007":
        return int(na_.isna().sum())
    if cid == "c0008":
        return int(date_range.notna().sum())
    if cid == "c0009":
        return float(date_range.mean())
    if cid == "c0010":
        return float(date_range.median())
    if cid == "c0011":
        return float(date_range.min())
    if cid == "c0012":
        return float(date_range.max())
    if cid == "c0013":
        return int((lat.notna() & lon.notna() & (lat != 0) & (lon != 0)).sum())
    if cid == "c0014":
        return float(((lat.notna() & lon.notna() & (lat != 0) & (lon != 0)).sum()) / N)
    if cid == "c0015":
        return int(lat.notna().sum())
    if cid == "c0016":
        return int(lon.notna().sum())
    if cid == "c0017":
        return int((lat.notna() & lon.notna()).sum())
    if cid == "c0018":
        return int(province_ser.isna().sum())
    if cid == "c0019":
        return int((province_ser.notna() & (province_ser.fillna("").str.strip() == "")).sum())
    if cid == "c0020":
        return province_valid_count
    if cid == "c0021":
        return province_nunique

    # Top-20 province (c0022..c0041) — rank i-21, value dict {rank, group, count}
    if "c0022" <= cid <= "c0041":
        idx = int(cid[-4:]) - 22  # 0..19
        if idx < len(top20_province):
            grp, cnt = top20_province.index[idx], int(top20_province.iloc[idx])
            return {"rank": idx + 1, "group": grp, "count": cnt}
        return None

    # Province threshold qualifying
    if cid == "c0042":
        return int((province_counts >= 10).sum())
    if cid == "c0043":
        return int((province_counts >= 30).sum())
    if cid == "c0044":
        return int((province_counts >= 100).sum())
    if cid == "c0045":
        return int((province_counts >= 300).sum())
    if cid == "c0046":
        return int((province_counts >= 100).sum())  # detail table size
    if cid == "c0047":
        return float(province_detail_100["count"].mean())
    if cid == "c0048":
        return float(province_detail_100["count"].median())
    if cid == "c0049":
        return float(province_detail_100["lat_null_rate"].mean())
    if cid == "c0050":
        return float(province_detail_100["not_before_null_rate"].mean())

    # Urban area
    if cid == "c0051":
        return int(urban_ser.isna().sum())
    if cid == "c0052":
        return int((urban_ser.notna() & (urban_ser.fillna("").str.strip() == "")).sum())
    if cid == "c0053":
        return urban_valid_count
    if cid == "c0054":
        return urban_nunique

    # Urban top-20
    if "c0055" <= cid <= "c0074":
        idx = int(cid[-4:]) - 55
        if idx < len(top20_urban):
            grp, cnt = top20_urban.index[idx], int(top20_urban.iloc[idx])
            return {"rank": idx + 1, "group": grp, "count": cnt}
        return None

    # Urban threshold qualifying
    if cid == "c0075":
        return int((urban_counts >= 10).sum())
    if cid == "c0076":
        return int((urban_counts >= 30).sum())
    if cid == "c0077":
        return int((urban_counts >= 100).sum())
    if cid == "c0078":
        return int((urban_counts >= 300).sum())
    if cid == "c0079":
        return int((urban_counts >= 100).sum())
    if cid == "c0080":
        return float(urban_detail_100["count"].mean())
    if cid == "c0081":
        return float(urban_detail_100["count"].median())
    if cid == "c0082":
        return float(urban_detail_100["lat_null_rate"].mean())
    if cid == "c0083":
        return float(urban_detail_100["not_before_null_rate"].mean())

    # Midpoint inflation
    # c0084 count at 50; c0085 count off at 50; c0086 chi2; c0087 pval
    # c0088..0091 for 150; c0092..95 for 250; c0096..99 for 350
    midpoint_map = {
        "c0084": (50, "count_at"), "c0085": (50, "count_off"),
        "c0086": (50, "chi2"), "c0087": (50, "p"),
        "c0088": (150, "count_at"), "c0089": (150, "count_off"),
        "c0090": (150, "chi2"), "c0091": (150, "p"),
        "c0092": (250, "count_at"), "c0093": (250, "count_off"),
        "c0094": (250, "chi2"), "c0095": (250, "p"),
        "c0096": (350, "count_at"), "c0097": (350, "count_off"),
        "c0098": (350, "chi2"), "c0099": (350, "p"),
    }
    if cid in midpoint_map:
        y, key = midpoint_map[cid]
        return midpoint_results[y][key]

    # Editorial spikes: c0100..c0127 for not_before, c0128..c0155 for not_after
    # Order: for each year in [-14,27,97,192,193,212,235], 4 claims (count, mean, chi2, p).
    editorial_map = {}
    base_nb = 100
    base_na = 128
    for i, y in enumerate(editorial_years):
        editorial_map[f"c{base_nb + 4 * i:04d}"] = ("not_before", y, "count_at")
        editorial_map[f"c{base_nb + 4 * i + 1:04d}"] = ("not_before", y, "mean_neighbours")
        editorial_map[f"c{base_nb + 4 * i + 2:04d}"] = ("not_before", y, "chi2")
        editorial_map[f"c{base_nb + 4 * i + 3:04d}"] = ("not_before", y, "p")
        editorial_map[f"c{base_na + 4 * i:04d}"] = ("not_after", y, "count_at")
        editorial_map[f"c{base_na + 4 * i + 1:04d}"] = ("not_after", y, "mean_neighbours")
        editorial_map[f"c{base_na + 4 * i + 2:04d}"] = ("not_after", y, "chi2")
        editorial_map[f"c{base_na + 4 * i + 3:04d}"] = ("not_after", y, "p")
    if cid in editorial_map:
        col, y, key = editorial_map[cid]
        return editorial_results[(col, y)][key]

    # Coordinate precision
    if cid == "c0156":
        return int(lat_decimals().value_counts().idxmax())
    if cid == "c0157":
        return int(lon_decimals().value_counts().idxmax())
    if cid == "c0158":
        return int(lat_decimals().value_counts().max())
    if cid == "c0159":
        return int(lon_decimals().value_counts().max())
    if cid == "c0160":
        vc = lat_decimals().value_counts()
        return int(vc.get(0, 0))
    if cid == "c0161":
        vc = lon_decimals().value_counts()
        return int(vc.get(0, 0))

    # Outlier coordinates
    if cid == "c0162":
        return int((lat.abs() > 90).sum())
    if cid == "c0163":
        return int((lon.abs() > 180).sum())
    if cid == "c0164":
        return int(((lat.abs() > 90) | (lon.abs() > 180)).sum())

    # Duplicates
    if cid == "c0165":
        # Scout reported exact duplicate rows
        try:
            return int(df.duplicated().sum())
        except Exception:
            # fallback to stringified
            return int(df.astype(str).duplicated().sum())
    if cid == "c0166":
        return int(df["LIST-ID"].duplicated().sum())

    # negative-date-range
    if cid == "c0167":
        return int((nb.notna() & na_.notna() & (nb > na_)).sum())

    # date-range-extreme
    if cid == "c0168":
        return int((date_range > 500).sum())

    # Temporal outliers — per scout semantics
    if cid == "c0169":
        return int(((nb < -50) & nb.notna()).sum())
    if cid == "c0170":
        return int(((na_ > 350) & na_.notna()).sum())
    if cid == "c0171":
        # union of both clauses
        return int((((nb < -50) & nb.notna()) | ((na_ > 350) & na_.notna())).sum())

    # Null-profile (c0172..c0202)
    null_col_map = {
        "c0172": "language_EDCS", "c0173": "inscr_process", "c0174": "year_of_find",
        "c0175": "letter_size", "c0176": "support_material", "c0177": "depth_cm",
        "c0178": "present_location", "c0179": "width_cm", "c0180": "height_cm",
        "c0181": "support_objecttype", "c0182": "type_of_inscription",
        "c0183": "keywords_term", "c0184": "trismegistos_uri", "c0185": "diplomatic_text",
        "c0186": "pleiades_id", "c0187": "text_edition", "c0188": "support_decoration",
        "c0189": "material_clean", "c0190": "findspot_clean", "c0191": "last_update",
        "c0192": "work_status", "c0193": "findspot_ancient_clean",
        "c0194": "modern_region_clean", "c0195": "type_of_inscription_clean",
        "c0196": "country_clean", "c0197": "clean_text_interpretive_sentence",
        "c0198": "type_of_monument_clean", "c0199": "province_label_clean",
        "c0200": "findspot_modern_clean", "c0201": "transcription", "c0202": "EDH-ID",
    }
    if cid in null_col_map:
        col = null_col_map[cid]
        if col not in df.columns:
            return None
        return float(df[col].isna().mean() * 100)

    # Granularity categories — c0203..c0216
    gran_map = {
        "c0203": ("eq_0", "count"), "c0204": ("eq_0", "pct"),
        "c0205": ("eq_25", "count"), "c0206": ("eq_25", "pct"),
        "c0207": ("eq_50", "count"), "c0208": ("eq_50", "pct"),
        "c0209": ("99_to_101", "count"), "c0210": ("99_to_101", "pct"),
        "c0211": ("199_to_201", "count"), "c0212": ("199_to_201", "pct"),
        "c0213": ("other_round", "count"), "c0214": ("other_round", "pct"),
        "c0215": ("irregular", "count"), "c0216": ("irregular", "pct"),
    }
    if cid in gran_map:
        key, kind = gran_map[cid]
        if kind == "count":
            return int(gran_cats[key])
        else:
            return float(gran_cats[key] / gran_total * 100)

    # Broad histogram c0217..c0223
    broad_map = {
        "c0217": "<=1", "c0218": "2..25", "c0219": "26..50",
        "c0220": "51..100", "c0221": "101..200", "c0222": "201..500",
        "c0223": ">500",
    }
    if cid in broad_map:
        return int(broad_hist[broad_map[cid]])

    return None


# -----------------------------------------------------------
# Match logic
# -----------------------------------------------------------
def classify_match(claim, my_val):
    scout = claim["value"]
    cat = claim["category"]
    if my_val is None:
        return "no", f"verifier could not compute (cid={claim['claim_id']})"

    # Ranking: dict compare
    if cat == "ranking":
        match = (
            isinstance(scout, dict)
            and isinstance(my_val, dict)
            and scout.get("rank") == my_val.get("rank")
            and scout.get("group") == my_val.get("group")
            and scout.get("count") == my_val.get("count")
        )
        return ("yes" if match else "no"), ""

    # Exact count / threshold / row tally (must be equal)
    if cat in ("count", "threshold_qualifying"):
        try:
            s = int(scout)
            m = int(round(my_val))
            return ("yes" if s == m else "no"), ""
        except (TypeError, ValueError):
            # scout min/max date_range uses float 0.0/2059.0
            try:
                s = float(scout)
                m = float(my_val)
                return ("yes" if s == m else "no"), ""
            except Exception:
                return "no", f"type mismatch scout={scout} mine={my_val}"

    # Rate / fraction
    if cat == "rate":
        s = float(scout)
        m = float(my_val)
        # rate reported as fraction or %
        diff_pp = abs(s - m) * 100  # treat as fraction, diff in pp
        return ("yes" if diff_pp <= PP_TOL else "tolerance"), f"|scout-mine|={diff_pp:.4f} pp"

    # Percentages
    if cat == "percentage":
        s = float(scout)
        m = float(my_val)
        diff = abs(s - m)
        return ("yes" if diff <= PP_TOL else "tolerance"), f"|scout-mine|={diff:.4f} pp"

    # Chi-square statistics — 0.5 % relative
    if cat == "chisq":
        s = float(scout)
        m = float(my_val)
        if s == 0 and m == 0:
            return "yes", ""
        if s == 0 or m == 0:
            diff = abs(s - m)
            return ("yes" if diff < 1e-3 else "no"), f"abs={diff:.6g}"
        rel = abs(s - m) / abs(s)
        return ("yes" if rel <= REL_TOL_CHISQ else "no"), f"rel={rel * 100:.3f}%"

    # p-values — 0.5 % relative, but handle 0.0
    if cat == "pvalue":
        s = float(scout)
        m = float(my_val)
        if s == 0.0 and m == 0.0:
            return "yes", ""
        # tiny pvalues both < 1e-100 -> accept
        if (s < 1e-100 and m < 1e-100):
            return "yes", ""
        if s == 0.0 or m == 0.0:
            return ("yes" if max(s, m) < 1e-300 else "no"), f"scout={s} mine={m}"
        rel = abs(s - m) / abs(s)
        return ("yes" if rel <= REL_TOL_CHISQ else "no"), f"rel={rel * 100:.3f}%"

    # mean / median / stddev — 0.1 % relative
    if cat in ("mean", "median", "stddev"):
        s = float(scout)
        m = float(my_val)
        if s == 0.0 and m == 0.0:
            return "yes", ""
        if s == 0.0 or m == 0.0:
            return ("yes" if abs(s - m) < 1e-6 else "no"), f"abs={abs(s - m):.6g}"
        rel = abs(s - m) / abs(s)
        return ("yes" if rel <= REL_TOL_FLOAT else "no"), f"rel={rel * 100:.4f}%"

    return "no", f"unhandled category {cat}"


# -----------------------------------------------------------
# Run verification
# -----------------------------------------------------------
rows = []
with open(CLAIMS) as fh:
    claims = [json.loads(line) for line in fh]

print(f"[run] verifying {len(claims)} claims")

for claim in claims:
    try:
        my = get_my_value(claim)
    except Exception as e:
        my = None
        print(f"[error] {claim['claim_id']} failed: {e}")
    match, notes = classify_match(claim, my)
    row = {
        "claim_id": claim["claim_id"],
        "category": claim["category"],
        "description": claim["description"],
        "scout_value": claim["value"],
        "my_value": my,
        "match": match,
        "notes": notes,
    }
    rows.append(row)

# Summary
match_counts = {}
for r in rows:
    match_counts[r["match"]] = match_counts.get(r["match"], 0) + 1

print("\n[summary]")
for k, v in match_counts.items():
    print(f"  {k}: {v}")

# Write verified_values.jsonl
Path(OUT).parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as fh:
    for r in rows:
        fh.write(json.dumps(r, default=str) + "\n")

# Print divergences
print("\n[divergences]")
for r in rows:
    if r["match"] != "yes":
        print(f"  {r['claim_id']} [{r['match']}] scout={r['scout_value']} mine={r['my_value']} "
              f"notes={r['notes']} :: {r['description']}")
