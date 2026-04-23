"""
Adversarial spot-checks for data-profile-verifier.

Implements the three mandatory spot-check requirements from the brief:
  (3) Spot-check at least one random per-subset detail for each subset level
      (dataset, province, urban-area).
  (4) Re-run unexpected-pattern diagnostic using own code path.
  (5) Re-run midpoint-inflation + editorial-spikes using own code path.

Prints PASS / FAIL per check. Any FAIL is a real correction.
"""

from __future__ import annotations

import random

import numpy as np
import pandas as pd
from scipy import stats

PARQUET = "/home/shawn/Code/inscriptions/archive/data-2026-04-22/LIRE_v3-0.parquet"
df = pd.read_parquet(PARQUET)
N = len(df)

random.seed(42)


def pp(label, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")


# -----------------------------------------------------------
# (3a) Dataset-level spot check: random column null-rate
# -----------------------------------------------------------
print("=== (3a) Dataset-level spot check ===")
# Pick a random column with reported null rate from scout summary; compare
scout_reported = {
    "language_EDCS": 99.9743,
    "inscr_process": 93.8683,
    "year_of_find": 85.2548,
    "letter_size": 85.1148,
    "support_material": 84.5936,
    "depth_cm": 83.9888,
    "present_location": 79.7542,
    "width_cm": 79.133,
    "height_cm": 78.9098,
    "support_objecttype": 74.8049,
}
pick = random.choice(list(scout_reported.keys()))
mine = df[pick].isna().mean() * 100
diff = abs(mine - scout_reported[pick])
print(f"  Column '{pick}': scout {scout_reported[pick]} vs mine {mine:.4f} (|diff|={diff:.4f} pp)")
pp(f"dataset null-rate spot check on {pick}", diff <= 0.1)


# -----------------------------------------------------------
# (3b) Province spot check: random top-20 province — its lat_null_rate
#      and not_before_null_rate at threshold 100 detail
# -----------------------------------------------------------
print("\n=== (3b) Province spot check ===")
province_counts = df["province"].value_counts()
qual_100 = province_counts[province_counts >= 100].index
# Pick a random province from top-20
provinces_top = province_counts.head(20).index.tolist()
pick_p = random.choice(provinces_top)
sub = df[df["province"] == pick_p]
lat_null = sub["Latitude"].isna().mean()
nb_null = sub["not_before"].isna().mean()
cnt = len(sub)
print(f"  Province '{pick_p}': count={cnt}, lat_null_rate={lat_null:.6f}, nb_null_rate={nb_null:.6f}")
# Scout reports mean lat_null_rate and nb_null_rate across all qualifying provinces = 0
# Our spot check: this particular province should have 0 for both
pp(f"province {pick_p} lat_null=0", lat_null == 0.0)
pp(f"province {pick_p} nb_null=0", nb_null == 0.0)


# -----------------------------------------------------------
# (3c) Urban-area spot check: random top-20 urban city
# -----------------------------------------------------------
print("\n=== (3c) Urban-area spot check ===")
urban_counts = df["urban_context_city"].value_counts()
urban_top = urban_counts.head(20).index.tolist()
pick_u = random.choice(urban_top)
sub = df[df["urban_context_city"] == pick_u]
lat_null_u = sub["Latitude"].isna().mean()
nb_null_u = sub["not_before"].isna().mean()
cnt_u = len(sub)
print(f"  Urban '{pick_u}': count={cnt_u}, lat_null_rate={lat_null_u:.6f}, nb_null_rate={nb_null_u:.6f}")
pp(f"urban {pick_u} lat_null=0", lat_null_u == 0.0)
pp(f"urban {pick_u} nb_null=0", nb_null_u == 0.0)


# -----------------------------------------------------------
# (4a) Unexpected-pattern diagnostic: granularity histogram
#      Re-implemented with own code path, compare to scout's reported totals.
# -----------------------------------------------------------
print("\n=== (4a) Granularity histogram (independent code path) ===")

dr = (df["not_after"] - df["not_before"]).dropna()
dr_int = dr.round().astype(int)
total_dr = len(dr_int)

# Use numpy-based histogram approach rather than pd.Series boolean indexing
vals, cnts = np.unique(dr_int.to_numpy(), return_counts=True)
freq = dict(zip(vals.tolist(), cnts.tolist()))


def freq_in_range(lo, hi):
    return sum(c for v, c in freq.items() if lo <= v <= hi)


def freq_eq(v):
    return freq.get(v, 0)


mine_gran = {
    "eq_0": freq_eq(0),
    "eq_25": freq_eq(25),
    "eq_50": freq_eq(50),
    "99_to_101": freq_in_range(99, 101),
    "199_to_201": freq_in_range(199, 201),
}
round_values = {10, 20, 30, 40, 60, 70, 75, 80, 90, 125, 150, 175, 250, 300, 400, 500}
mine_gran["other_round"] = sum(freq_eq(v) for v in round_values)
mine_gran["irregular"] = total_dr - sum(mine_gran.values())

scout_gran = {
    "eq_0": 8279, "eq_25": 172, "eq_50": 631,
    "99_to_101": 48436, "199_to_201": 28422,
    "other_round": 3971, "irregular": 92942,
}
for k in scout_gran:
    pp(f"granularity {k}: scout={scout_gran[k]} mine={mine_gran[k]}",
       scout_gran[k] == mine_gran[k])

# Total non-null date range
pp(f"total non-null date_range scout=182853 mine={total_dr}", total_dr == 182853)


# -----------------------------------------------------------
# (4b) Broad histogram
# -----------------------------------------------------------
print("\n=== (4b) Broad histogram (independent code path) ===")
# Own code path: use numpy.histogram-like boundary partitioning with sum of frequencies
def count_in(pred):
    return sum(c for v, c in freq.items() if pred(v))


mine_broad = {
    "<=1": count_in(lambda v: v <= 1),
    "2..25": count_in(lambda v: 2 <= v <= 25),
    "26..50": count_in(lambda v: 26 <= v <= 50),
    "51..100": count_in(lambda v: 51 <= v <= 100),
    "101..200": count_in(lambda v: 101 <= v <= 200),
    "201..500": count_in(lambda v: 201 <= v <= 500),
    ">500": count_in(lambda v: v > 500),
}
scout_broad = {
    "<=1": 11069, "2..25": 15093, "26..50": 35581,
    "51..100": 67194, "101..200": 45159, "201..500": 8493, ">500": 264,
}
for k in scout_broad:
    pp(f"broad {k}: scout={scout_broad[k]} mine={mine_broad[k]}", scout_broad[k] == mine_broad[k])


# -----------------------------------------------------------
# (5a) Midpoint-inflation — independent code path (use numpy arrays, not
#      pandas Series operations)
# -----------------------------------------------------------
print("\n=== (5a) Midpoint-inflation (independent code path) ===")
nb = df["not_before"].to_numpy()
na_ = df["not_after"].to_numpy()
mids = np.round((nb + na_) / 2)

scout_mp = {
    50: (12108, 8451, 204087.803, 0.0),
    150: (20281, 4551, 489516.01, 0.0),
    250: (7222, 3859, 136221.958, 0.0),
    350: (12689, 685, 359873.885, 0.0),
}
for y, (s_at, s_off, s_chi2, s_p) in scout_mp.items():
    at_ = int(np.sum(mids == y))
    in_window = int(np.sum((mids >= y - 15) & (mids <= y + 15)))
    off = in_window - at_
    total = in_window
    exp_t = total / 31
    exp_o = total * 30 / 31
    chi2, p = stats.chisquare([at_, off], [exp_t, exp_o])
    chi2 = float(chi2)
    print(f"  y={y}: at {s_at}vs{at_}, off {s_off}vs{off}, chi2 {s_chi2} vs {chi2:.3f}, p {s_p} vs {p:.3g}")
    pp(f"midpoint {y} at", s_at == at_)
    pp(f"midpoint {y} off", s_off == off)
    rel_chi2 = abs(chi2 - s_chi2) / s_chi2 if s_chi2 else 0.0
    pp(f"midpoint {y} chi2", rel_chi2 <= 0.005)


# -----------------------------------------------------------
# (5b) Editorial-spikes — independent
# -----------------------------------------------------------
print("\n=== (5b) Editorial-spikes (independent code path) ===")
# Use numpy value_counts equivalent for not_before and not_after
nb_vc = pd.Series(nb).value_counts()
na_vc = pd.Series(na_).value_counts()

def es_compute(vc, y):
    at_ = int(vc.get(y, 0))
    neigh = [int(vc.get(y + d, 0)) for d in range(-5, 6) if d != 0]
    mean_n = float(np.mean(neigh))
    total_n = int(np.sum(neigh))
    total = at_ + total_n
    exp_t = total / 11
    exp_o = total * 10 / 11
    chi2, p = stats.chisquare([at_, total_n], [exp_t, exp_o])
    return at_, mean_n, float(chi2), float(p)


# Scout values
scout_es_nb = {
    -14: (20, 109.5, 71.841),
    27: (19, 214.4, 176.519),
    97: (118, 2529.8, 2288.629),
    192: (33, 129.6, 70.215),
    193: (465, 126.8, 660.007),
    212: (870, 152.4, 2151.002),
    235: (121, 111.1, 0.796),
}
scout_es_na = {
    -14: (14, 26.7, 5.74),
    27: (17, 327.5, 292.862),
    97: (500, 1638.4, 767.564),
    192: (221, 51.9, 386.416),
    193: (77, 77.2, 0.0),
    212: (99, 276.4, 109.922),
    235: (716, 486.7, 94.176),
}

for y, (s_at, s_mean, s_chi2) in scout_es_nb.items():
    at_, mean_n, chi2, p = es_compute(nb_vc, y)
    pp(f"editorial not_before y={y} at: scout={s_at} mine={at_}", s_at == at_)
    pp(f"editorial not_before y={y} mean: scout={s_mean} mine={mean_n:.1f}",
       abs(s_mean - mean_n) < 0.05)
    rel = abs(chi2 - s_chi2) / s_chi2 if s_chi2 else abs(chi2)
    pp(f"editorial not_before y={y} chi2: scout={s_chi2} mine={chi2:.3f}",
       (s_chi2 == 0.0 and chi2 < 0.005) or rel <= 0.005)

for y, (s_at, s_mean, s_chi2) in scout_es_na.items():
    at_, mean_n, chi2, p = es_compute(na_vc, y)
    pp(f"editorial not_after y={y} at: scout={s_at} mine={at_}", s_at == at_)
    pp(f"editorial not_after y={y} mean: scout={s_mean} mine={mean_n:.1f}",
       abs(s_mean - mean_n) < 0.05)
    rel = abs(chi2 - s_chi2) / s_chi2 if s_chi2 else abs(chi2)
    pp(f"editorial not_after y={y} chi2: scout={s_chi2} mine={chi2:.3f}",
       (s_chi2 == 0.0 and chi2 < 0.005) or rel <= 0.005)


# -----------------------------------------------------------
# Decision 4 cross-check: does the overlap interpretation hold?
# -----------------------------------------------------------
print("\n=== Decision-4 cross-check: does EVERY row overlap 50 BC – AD 350? ===")
# Overlap = not_before <= 350 AND not_after >= -50
overlap = ((df["not_before"] <= 350) & (df["not_after"] >= -50)).sum()
print(f"  Rows overlapping (50 BC – AD 350): {overlap} / {N}")
pp("all rows overlap 50 BC – AD 350", overlap == N)
