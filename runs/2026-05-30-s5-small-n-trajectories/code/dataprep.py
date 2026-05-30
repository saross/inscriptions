#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dataprep.py — §5 small-N city-trajectory harness, Layer A data preparation.
============================================================================

Load the filtered LIRE corpus, restrict to the §5 Hanson-matched target set,
clip every inscription's date interval to the analysis envelope, build the
per-inscription aoristic bin-weight matrix, and cache the prepared per-city
data to disk for the modelling stage.

Pipeline (exact spec, see ``runs/2026-05-30-s5-small-n-trajectories/spec.md``
and the implementation brief):

1. Temporal envelope: ``ENV_LO = -50`` (50 BC) to ``ENV_HI = 350`` (AD 350).
   Grid: 25-year bins with edges at -50, -25, 0, ..., 350 -> exactly 16 bins.
   Bin ``t`` covers the half-open interval ``[edge_t, edge_{t+1})``.
2. Filter to the §5 target set: keep rows where both ``urban_context_city``
   and ``urban_context_pop_est`` are non-null (Hanson-matched); drop Rome
   (city name contains "rom", case-insensitive); require the date interval to
   overlap the envelope.
3. Clip each inscription's ``[not_before, not_after]`` to the envelope, then
   drop any row whose clipped ``not_before >= not_after`` or which has zero
   envelope overlap. This removes the bad ``not_after = 2230`` record.
4. Per-city ``N`` = surviving row count. The small-N target set is the set of
   cities with ``50 <= N < 1549``; cities with ``N >= 1549`` are the large
   validation anchors.
5. Aoristic weight: for inscription ``i`` and bin ``t``,
   ``a[i, t] = |clipped_interval_i ∩ bin_t| / 25`` — the fraction of bin ``t``
   covered by the interval (in ``[0, 1]``; 1.0 when the bin is fully inside the
   interval).

Output cache (``--out-dir``, default ``code/prepared``):

- ``city-index.parquet`` — one row per surviving city: ``city``, ``province``,
  ``pop_est``, ``N``, ``bucket`` ("target" | "large_anchor" | "below_floor").
- ``aoristic-<safe-city-name>.npz`` — per-city dense aoristic matrix ``A``
  (shape ``N_c x 16``, float64) for every target and large-anchor city, plus
  the per-inscription clipped ``[not_before, not_after]`` for traceability.

Threading / scratch hygiene is the caller's responsibility (set the
``*_NUM_THREADS`` env vars before invoking); this module is pure numpy/pandas
and does no sampling.

Run (on zbook, inside the project venv)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/dataprep.py --verify

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Constants — the analysis envelope and temporal grid.
# --------------------------------------------------------------------------- #

ENV_LO: int = -50          # 50 BC, lower envelope edge.
ENV_HI: int = 350          # AD 350, upper envelope edge.
BIN_WIDTH: int = 25        # years per bin.
N_FLOOR: int = 50          # small-N estimation floor (Crema 2025).
N_THRESHOLD: int = 1549    # confirmatory threshold (prereg §6); large anchors above.

# Bin edges: -50, -25, 0, ..., 350  -> 17 edges, 16 bins.
BIN_EDGES: np.ndarray = np.arange(ENV_LO, ENV_HI + BIN_WIDTH, BIN_WIDTH, dtype=float)
N_BINS: int = len(BIN_EDGES) - 1  # == 16

# Default corpus location (relative to the repo root).
DEFAULT_PARQUET = Path(
    "runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet"
)

# Columns we actually read.
CITY_COL = "urban_context_city"
POP_COL = "urban_context_pop_est"
PROV_COL = "province"
NB_COL = "not_before"
NA_COL = "not_after"


# --------------------------------------------------------------------------- #
# Filtering.
# --------------------------------------------------------------------------- #

def load_and_filter(parquet_path: Path) -> tuple[pd.DataFrame, dict]:
    """Load the corpus and apply the §5 target-set filter + envelope clip.

    The Rome-exclusion uses the same case-insensitive ``contains("rom")``
    substring test as the canonical profiling script
    (``scripts/s5-target-set-profile.py``), so the resulting target set is
    consistent with the spec's published bucketing. NOTE: that substring also
    matches a handful of unrelated cities (Romula, Tauromenium, the two
    Caesaromagus entries); this is a known over-match inherited from the
    reference script and is documented in the smoke report rather than silently
    "fixed", because changing it would change the canonical target set.

    Args:
        parquet_path: Path to ``lire-filtered-with-letters.parquet``.

    Returns:
        ``(df, stats)`` where ``df`` is the surviving, clipped per-inscription
        frame (with added integer columns ``nb_clip`` and ``na_clip``) and
        ``stats`` is a dict of audit counts for the verification printout.
    """
    cols = [CITY_COL, POP_COL, PROV_COL, NB_COL, NA_COL]
    df = pd.read_parquet(parquet_path, columns=cols)
    stats: dict = {"rows_loaded": len(df)}

    # 1. Hanson-matched: city label AND population estimate both present.
    matched = df[df[CITY_COL].notna() & df[POP_COL].notna()].copy()
    stats["rows_hanson_matched"] = len(matched)

    # 2. Rome exclusion (case-insensitive substring; canonical-script parity).
    is_rome = matched[CITY_COL].str.contains("rom", case=False, na=False)
    stats["rows_rome_excluded"] = int(is_rome.sum())
    matched = matched[~is_rome].copy()
    stats["rows_after_rome"] = len(matched)

    # 3. Clip intervals to the envelope (vectorised), tracking pre-clip overlap.
    nb_clip = matched[NB_COL].clip(ENV_LO, ENV_HI)
    na_clip = matched[NA_COL].clip(ENV_LO, ENV_HI)
    # Genuine overlap with the envelope, judged on the ORIGINAL interval:
    # an interval overlaps [ENV_LO, ENV_HI) iff not_after > ENV_LO and
    # not_before < ENV_HI.
    overlaps_envelope = (matched[NA_COL] > ENV_LO) & (matched[NB_COL] < ENV_HI)
    # After clipping, keep only positive-length intervals.
    positive_length = na_clip > nb_clip
    keep = overlaps_envelope & positive_length

    stats["rows_overlap_envelope"] = int(overlaps_envelope.sum())
    stats["rows_dropped_clip_overlap"] = int((~keep).sum())

    out = matched[keep].copy()
    out["nb_clip"] = nb_clip[keep].astype(int)
    out["na_clip"] = na_clip[keep].astype(int)
    stats["rows_surviving"] = len(out)

    # Bad-record audit. The brief named the not_after == 2230 record as one the
    # filter should remove. In fact that record (Lepcis Magna, not_before=171)
    # has a VALID not_before, so clipping its not_after to ENV_HI=350 REPAIRS it
    # to [171, 350] rather than dropping it — the brief's literal rule (drop only
    # when nb_clip >= na_clip) keeps it. The thing that actually mattered — the
    # absurd 2230 upper date — is gone: no surviving row has not_after > ENV_HI
    # un-clipped. We report both facts so the disposition is transparent.
    stats["raw_not_after_gt_env_hi"] = int((matched[NA_COL] > ENV_HI).sum())
    stats["surviving_na_clip_max"] = int(out["na_clip"].max())
    stats["surviving_na_clip_gt_env_hi"] = int((out["na_clip"] > ENV_HI).sum())
    # The specific 2230 record's fate.
    has_2230 = matched[NA_COL] == 2230
    stats["bad_2230_rows_total"] = int(has_2230.sum())
    stats["bad_2230_rows_kept"] = int((has_2230 & keep).sum())
    stats["bad_2230_clipped_to"] = (
        f"[{int(nb_clip[has_2230].iloc[0])}, {int(na_clip[has_2230].iloc[0])}]"
        if has_2230.any() else "n/a"
    )
    return out, stats


# --------------------------------------------------------------------------- #
# Aoristic weighting.
# --------------------------------------------------------------------------- #

def aoristic_matrix(nb: np.ndarray, na: np.ndarray) -> np.ndarray:
    """Build the per-inscription aoristic bin-weight matrix.

    For inscription ``i`` with clipped interval ``[nb_i, na_i)`` and bin ``t``
    covering ``[edge_t, edge_{t+1})``, the weight is the fraction of bin ``t``
    covered by the interval::

        a[i, t] = max(0, min(na_i, edge_{t+1}) - max(nb_i, edge_t)) / BIN_WIDTH

    This lies in ``[0, 1]``: 1.0 when the whole bin is inside the interval,
    0.0 when they are disjoint. It is the "fraction of bin covered" convention
    (NOT the fraction of the *interval* in the bin), per the brief.

    Args:
        nb: 1-D array of clipped ``not_before`` values (length ``N``).
        na: 1-D array of clipped ``not_after`` values (length ``N``).

    Returns:
        Dense ``(N, N_BINS)`` float64 array of aoristic weights.
    """
    nb = np.asarray(nb, dtype=float)[:, None]            # (N, 1)
    na = np.asarray(na, dtype=float)[:, None]            # (N, 1)
    lo = BIN_EDGES[:-1][None, :]                         # (1, 16) bin lower edges
    hi = BIN_EDGES[1:][None, :]                          # (1, 16) bin upper edges
    overlap = np.minimum(na, hi) - np.maximum(nb, lo)    # (N, 16) raw overlap
    overlap = np.clip(overlap, 0.0, None)                # disjoint -> 0
    return overlap / BIN_WIDTH


# --------------------------------------------------------------------------- #
# Per-city assembly + caching.
# --------------------------------------------------------------------------- #

def _safe_name(city: str) -> str:
    """Filesystem-safe slug for a city name (for per-city npz filenames)."""
    slug = re.sub(r"[^0-9A-Za-z]+", "-", city).strip("-").lower()
    return slug or "unnamed"


def bucket_of(n: int) -> str:
    """Classify a per-city inscription count into a target-set bucket."""
    if n < N_FLOOR:
        return "below_floor"
    if n < N_THRESHOLD:
        return "target"
    return "large_anchor"


def prepare(parquet_path: Path, out_dir: Path) -> tuple[pd.DataFrame, dict]:
    """Run the full data-prep pipeline and cache per-city aoristic matrices.

    Caches the aoristic matrix for every TARGET and LARGE-ANCHOR city (the
    cities that can actually be fitted); below-floor cities appear in the city
    index for completeness but get no cached matrix.

    Args:
        parquet_path: Path to the filtered LIRE parquet.
        out_dir: Directory to write the cache into (created if absent).

    Returns:
        ``(city_index, stats)``: the per-city index frame and the audit stats.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    df, stats = load_and_filter(parquet_path)

    # Per-city counts and metadata.
    grp = df.groupby(CITY_COL)
    counts = grp.size()
    meta_prov = grp[PROV_COL].first()
    meta_pop = grp[POP_COL].first()

    rows = []
    for city, n in counts.items():
        rows.append(
            {
                "city": city,
                "province": meta_prov[city],
                "pop_est": float(meta_pop[city]),
                "N": int(n),
                "bucket": bucket_of(int(n)),
            }
        )
    city_index = pd.DataFrame(rows).sort_values("N", ascending=False).reset_index(drop=True)

    n_target = int((city_index["bucket"] == "target").sum())
    n_large = int((city_index["bucket"] == "large_anchor").sum())
    n_below = int((city_index["bucket"] == "below_floor").sum())
    stats["n_cities_total"] = len(city_index)
    stats["n_target"] = n_target
    stats["n_large_anchor"] = n_large
    stats["n_below_floor"] = n_below
    stats["large_anchor_names"] = list(
        city_index.loc[city_index["bucket"] == "large_anchor", "city"]
    )

    # Cache per-city aoristic matrices for fittable cities.
    fittable = city_index[city_index["bucket"].isin(["target", "large_anchor"])]
    for city in fittable["city"]:
        sub = df[df[CITY_COL] == city]
        nb = sub["nb_clip"].to_numpy()
        na = sub["na_clip"].to_numpy()
        a = aoristic_matrix(nb, na)
        np.savez_compressed(
            out_dir / f"aoristic-{_safe_name(city)}.npz",
            city=np.array(city),
            province=np.array(str(meta_prov[city])),
            pop_est=np.array(float(meta_pop[city])),
            A=a.astype(np.float64),
            nb_clip=nb.astype(np.int64),
            na_clip=na.astype(np.int64),
            bin_edges=BIN_EDGES,
        )

    city_index.to_parquet(out_dir / "city-index.parquet", index=False)

    # Aoristic sanity stats on the WHOLE surviving corpus (cheap, global).
    a_all = aoristic_matrix(df["nb_clip"].to_numpy(), df["na_clip"].to_numpy())
    stats["a_min"] = float(a_all.min())
    stats["a_max"] = float(a_all.max())
    # Coverage identity on a sample row: sum_t a*BIN_WIDTH == clipped length.
    sample_i = 0
    samp_len = int(df["na_clip"].iloc[sample_i] - df["nb_clip"].iloc[sample_i])
    samp_cov = float(a_all[sample_i].sum() * BIN_WIDTH)
    stats["sample_clipped_length"] = samp_len
    stats["sample_aoristic_coverage"] = samp_cov
    # And the same identity across ALL rows (max abs error), as a strong check.
    lengths = (df["na_clip"].to_numpy() - df["nb_clip"].to_numpy()).astype(float)
    cov = a_all.sum(axis=1) * BIN_WIDTH
    stats["coverage_max_abs_err"] = float(np.max(np.abs(cov - lengths)))

    return city_index, stats


def load_city(out_dir: Path, city: str) -> dict:
    """Load a cached per-city aoristic bundle by city name.

    Args:
        out_dir: The cache directory used in :func:`prepare`.
        city: Exact city name (as in ``urban_context_city``).

    Returns:
        Dict with keys ``city``, ``province``, ``pop_est``, ``A`` (N x 16),
        ``nb_clip``, ``na_clip``, ``bin_edges``.
    """
    path = out_dir / f"aoristic-{_safe_name(city)}.npz"
    with np.load(path, allow_pickle=True) as z:
        return {
            "city": str(z["city"]),
            "province": str(z["province"]),
            "pop_est": float(z["pop_est"]),
            "A": z["A"],
            "nb_clip": z["nb_clip"],
            "na_clip": z["na_clip"],
            "bin_edges": z["bin_edges"],
        }


# --------------------------------------------------------------------------- #
# CLI / verification printout.
# --------------------------------------------------------------------------- #

def _print_verification(stats: dict) -> None:
    """Emit the verification block required by the brief."""
    print("=" * 68)
    print("DATAPREP VERIFICATION  (§5 small-N trajectories, Layer A)")
    print("=" * 68)
    print(f"  envelope            : [{ENV_LO}, {ENV_HI}]  "
          f"({N_BINS} bins x {BIN_WIDTH}y)")
    print(f"  rows loaded         : {stats['rows_loaded']:>7}")
    print(f"  Hanson-matched      : {stats['rows_hanson_matched']:>7}")
    print(f"  Rome rows excluded  : {stats['rows_rome_excluded']:>7}")
    print(f"  after Rome excl.    : {stats['rows_after_rome']:>7}")
    print(f"  overlap envelope    : {stats['rows_overlap_envelope']:>7}")
    print(f"  dropped clip/overlap: {stats['rows_dropped_clip_overlap']:>7}")
    print(f"  surviving rows      : {stats['rows_surviving']:>7}")
    print("-" * 68)
    print(f"  raw not_after>{ENV_HI}   : {stats['raw_not_after_gt_env_hi']}  "
          f"-> surviving na_clip>{ENV_HI}: {stats['surviving_na_clip_gt_env_hi']}  "
          f"(surviving na_clip max = {stats['surviving_na_clip_max']})  "
          f"({'no out-of-envelope dates survive — OK' if stats['surviving_na_clip_gt_env_hi'] == 0 else 'OUT-OF-ENVELOPE SURVIVES — BAD'})")
    print(f"  not_after==2230 rec : total={stats['bad_2230_rows_total']}  "
          f"kept={stats['bad_2230_rows_kept']}  clipped-to={stats['bad_2230_clipped_to']}  "
          f"(repaired-by-clip, not dropped — its not_before is valid; "
          f"the absurd 2230 upper date is removed)")
    print("-" * 68)
    print(f"  cities (any N)      : {stats['n_cities_total']:>7}")
    print(f"  TARGET (50<=N<1549) : {stats['n_target']:>7}   (spec: ~279)")
    print(f"  large anchor (>=1549): {stats['n_large_anchor']:>6}   (spec: ~7)")
    print(f"  below floor (N<50)  : {stats['n_below_floor']:>7}")
    print(f"  large-anchor names  : {stats['large_anchor_names']}")
    print("-" * 68)
    print(f"  aoristic a min/max  : {stats['a_min']:.6f} / {stats['a_max']:.6f}  "
          f"({'in [0,1] — OK' if 0.0 <= stats['a_min'] and stats['a_max'] <= 1.0 + 1e-9 else 'OUT OF RANGE — BAD'})")
    print(f"  sample row coverage : sum_t a*{BIN_WIDTH} = "
          f"{stats['sample_aoristic_coverage']:.4f}  vs clipped length "
          f"{stats['sample_clipped_length']}  "
          f"({'MATCH' if abs(stats['sample_aoristic_coverage'] - stats['sample_clipped_length']) < 1e-6 else 'MISMATCH'})")
    print(f"  coverage identity   : max |sum_t a*{BIN_WIDTH} - len| over all rows "
          f"= {stats['coverage_max_abs_err']:.2e}")
    print("=" * 68)


def main() -> int:
    """Command-line entry point for the data-prep stage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parquet", type=Path, default=DEFAULT_PARQUET,
        help="Path to the filtered LIRE parquet (default: repo-relative).",
    )
    parser.add_argument(
        "--out-dir", type=Path,
        default=Path(__file__).resolve().parent / "prepared",
        help="Cache output directory (default: code/prepared).",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Print the verification block after preparing.",
    )
    args = parser.parse_args()

    if not args.parquet.exists():
        print(f"FATAL: parquet not found at {args.parquet}")
        return 2

    _city_index, stats = prepare(args.parquet, args.out_dir)
    if args.verify:
        _print_verification(stats)
    print(f"\nCache written to: {args.out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
