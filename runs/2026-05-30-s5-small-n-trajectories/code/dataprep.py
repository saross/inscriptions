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
   (EXACT match, ``name.strip().lower() in {"roma", "rome"}`` — not a loose
   substring, which would wrongly drop Romula etc.); drop rows with a missing
   ``not_before``/``not_after``; require the date interval to overlap the
   envelope.
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
BIN_WIDTH: int = 25        # DEFAULT years per bin (25y primary grid; spec §3).
N_FLOOR: int = 50          # small-N estimation floor (Crema 2025).
N_THRESHOLD: int = 1549    # confirmatory threshold (prereg §6); large anchors above.

# Supported bin widths. 25y is the primary grid (16 bins); 50y is the
# robustness check (8 bins). Both divide the 400-year envelope evenly and the
# 50y edges are a SUBSET of the 25y edges (see ``make_grid`` / ``--verify``),
# so the 50y grid NESTS the 25y grid: every 50y bin is exactly the union of two
# adjacent 25y bins. This nesting is what makes the bin-width robustness check
# a clean coarsening rather than an independent re-gridding (spec §3).
SUPPORTED_BIN_WIDTHS: tuple[int, ...] = (25, 50)


def make_grid(bin_width: int = BIN_WIDTH) -> tuple[np.ndarray, int]:
    """Return ``(bin_edges, n_bins)`` for a given bin width over the envelope.

    The envelope ``[ENV_LO, ENV_HI]`` (50 BC – AD 350, span 400 years) is divided
    into equal-width bins. Bin ``t`` covers the half-open interval
    ``[edge_t, edge_{t+1})``.

    Args:
        bin_width: Years per bin. Must be a whole-number (exact) divisor of the
            400-year envelope span — i.e. divide it with zero remainder
            (25 -> 16 bins, 50 -> 8 bins). Other exact divisors of 400 (e.g. 100)
            would also work but only 25 and 50 are used by §5.

    Returns:
        ``(bin_edges, n_bins)``: a length ``n_bins + 1`` float array of edges
        (``ENV_LO, ENV_LO + bin_width, ..., ENV_HI``) and the bin count.

    Raises:
        ValueError: If ``bin_width`` is not a whole-number (exact) divisor of the
            envelope span (leaves a non-zero remainder).
    """
    span = ENV_HI - ENV_LO
    if bin_width <= 0 or span % bin_width != 0:
        raise ValueError(
            f"bin_width={bin_width} must be a positive whole-number (exact) "
            f"divisor of the {span}-year envelope span; got remainder "
            f"{span % bin_width}."
        )
    edges = np.arange(ENV_LO, ENV_HI + bin_width, bin_width, dtype=float)
    return edges, len(edges) - 1


# Module-level DEFAULT grid (25y, 16 bins). Kept as importable constants so the
# downstream single-city / hierarchical models (which read ``dp.N_BINS``,
# ``dp.BIN_EDGES``, ``dp.BIN_WIDTH``) continue to work unchanged at the primary
# grid. The 50y grid is selected per-call via ``--bin-width`` / ``make_grid``.
BIN_EDGES: np.ndarray
N_BINS: int
BIN_EDGES, N_BINS = make_grid(BIN_WIDTH)  # 17 edges, 16 bins.

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

# Rome-exclusion: EXACT match only ("roma"/"rome"). A loose contains("rom")
# over-matches Romula, Tauromenium, and Caesaromagus (audit A2).
ROME_TOKENS = ("roma", "rome")


def _is_rome(name: object) -> bool:
    """EXACT Rome match: ``str(name).strip().lower() in ("roma", "rome")``."""
    return str(name).strip().lower() in ROME_TOKENS


def _most_common_province(values: pd.Series) -> object:
    """Return a city's most-common province value, alphabetical tiebreak.

    Replaces the earlier ``GroupBy.first()`` province assignment, which took
    whatever province sat on the first row (audit finding B1). We take the mode
    across the city's rows (NaNs ignored); ties are broken deterministically by
    sorting the tied values and taking the first.

    Args:
        values: The ``province`` values for one city's inscriptions.

    Returns:
        The most-common non-null province value, or ``np.nan`` if the city has
        no non-null province at all.
    """
    counts = values.dropna().value_counts()
    if counts.empty:
        return np.nan
    top = counts.max()
    tied = sorted(str(v) for v in counts[counts == top].index)
    return tied[0]


# --------------------------------------------------------------------------- #
# Filtering.
# --------------------------------------------------------------------------- #

def load_and_filter(
    parquet_path: Path, *, letter_col: str = "letter_count_conservative"
) -> tuple[pd.DataFrame, dict]:
    """Load the corpus and apply the §5 target-set filter + envelope clip.

    The Rome-exclusion uses an EXACT match (a city is Rome iff
    ``str(name).strip().lower() in ("roma", "rome")``), matching the corrected
    canonical profiling script (``scripts/s5-target-set-profile.py``). An
    earlier loose ``contains("rom")`` test wrongly dropped legitimate target
    cities — Romula (N=54), Tauromenium, and the two Caesaromagus entries
    (audit finding A2; see ``scripts/audit-verify-rome-and-deff.py``); the exact
    test restores them to the target set.

    Args:
        parquet_path: Path to ``lire-filtered-with-letters.parquet``.

    Returns:
        ``(df, stats)`` where ``df`` is the surviving, clipped per-inscription
        frame (with added integer columns ``nb_clip`` and ``na_clip``) and
        ``stats`` is a dict of audit counts for the verification printout.
    """
    cols = [CITY_COL, POP_COL, PROV_COL, NB_COL, NA_COL]
    # Read the letter-count column too when present (for the letter-mass unit).
    # Probe the schema first so a corpus without the column still loads.
    import pyarrow.parquet as _pq
    schema_names = set(_pq.read_schema(parquet_path).names)
    has_letters = letter_col in schema_names
    read_cols = cols + ([letter_col] if has_letters else [])
    df = pd.read_parquet(parquet_path, columns=read_cols)
    stats: dict = {"rows_loaded": len(df), "has_letter_col": bool(has_letters)}
    if not has_letters:
        df[letter_col] = np.nan  # letter unit unavailable; weight column absent.
    # Normalise the letter weight: non-finite / non-positive -> 0 (those rows
    # contribute no letter mass but still exist as inscription events).
    lw = pd.to_numeric(df[letter_col], errors="coerce").to_numpy(dtype=float)
    lw = np.where(np.isfinite(lw) & (lw > 0), lw, 0.0)
    df = df.assign(letter_w=lw)

    # 1. Hanson-matched: city label AND population estimate both present.
    matched = df[df[CITY_COL].notna() & df[POP_COL].notna()].copy()
    stats["rows_hanson_matched"] = len(matched)

    # 2. Rome exclusion (EXACT match — not a loose substring; audit A2).
    is_rome = matched[CITY_COL].map(_is_rome)
    stats["rows_rome_excluded"] = int(is_rome.sum())
    matched = matched[~is_rome].copy()
    stats["rows_after_rome"] = len(matched)

    # 2b. Drop rows with a missing not_before / not_after BEFORE clipping: a NaN
    #     date cannot be clipped to an integer bin edge and would silently
    #     corrupt the aoristic matrix. Report how many were dropped (audit C-i).
    has_dates = matched[NB_COL].notna() & matched[NA_COL].notna()
    stats["rows_dropped_nan_dates"] = int((~has_dates).sum())
    matched = matched[has_dates].copy()
    stats["rows_after_nan_drop"] = len(matched)

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

def aoristic_matrix(
    nb: np.ndarray,
    na: np.ndarray,
    *,
    bin_edges: np.ndarray | None = None,
    bin_width: int | None = None,
) -> np.ndarray:
    """Build the per-inscription aoristic bin-weight matrix.

    For inscription ``i`` with clipped interval ``[nb_i, na_i)`` and bin ``t``
    covering ``[edge_t, edge_{t+1})``, the weight is the fraction of bin ``t``
    covered by the interval::

        a[i, t] = max(0, min(na_i, edge_{t+1}) - max(nb_i, edge_t)) / bin_width

    This lies in ``[0, 1]``: 1.0 when the whole bin is inside the interval,
    0.0 when they are disjoint. It is the "fraction of bin covered" convention
    (NOT the fraction of the *interval* in the bin), per the brief.

    Args:
        nb: 1-D array of clipped ``not_before`` values (length ``N``).
        na: 1-D array of clipped ``not_after`` values (length ``N``).
        bin_edges: Bin-edge array (length ``n_bins + 1``). Defaults to the
            module 25y grid (``BIN_EDGES``) for backward compatibility.
        bin_width: Years per bin (the divisor). Defaults to the module 25y
            ``BIN_WIDTH``. Must equal the spacing implied by ``bin_edges``.

    Returns:
        Dense ``(N, n_bins)`` float64 array of aoristic weights.
    """
    if bin_edges is None:
        bin_edges = BIN_EDGES
    if bin_width is None:
        bin_width = BIN_WIDTH
    # Guard the exported invariant: ``bin_width`` is the per-bin normalising
    # divisor, so it MUST equal the spacing implied by ``bin_edges``. Mismatched
    # (but individually plausible) values would silently mis-normalise every
    # weight. Internal callers always pass a consistent pair; this protects
    # external callers that supply the two args independently.
    bin_edges = np.asarray(bin_edges, dtype=float)
    assert np.allclose(np.diff(bin_edges), bin_width), (
        f"bin_width={bin_width} does not match the spacing implied by "
        f"bin_edges (diffs={np.unique(np.diff(bin_edges))}); the two args must "
        "describe the same grid or normalisation is wrong."
    )
    nb = np.asarray(nb, dtype=float)[:, None]            # (N, 1)
    na = np.asarray(na, dtype=float)[:, None]            # (N, 1)
    lo = bin_edges[:-1][None, :]                         # (1, n_bins) lower edges
    hi = bin_edges[1:][None, :]                          # (1, n_bins) upper edges
    overlap = np.minimum(na, hi) - np.maximum(nb, lo)    # (N, n_bins) raw overlap
    overlap = np.clip(overlap, 0.0, None)                # disjoint -> 0
    return overlap / bin_width


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


def prepare(
    parquet_path: Path,
    out_dir: Path,
    *,
    bin_width: int = BIN_WIDTH,
    letter_col: str = "letter_count_conservative",
) -> tuple[pd.DataFrame, dict]:
    """Run the full data-prep pipeline and cache per-city aoristic matrices.

    Caches the aoristic matrix for every TARGET and LARGE-ANCHOR city (the
    cities that can actually be fitted); below-floor cities appear in the city
    index for completeness but get no cached matrix.

    Each cached ``.npz`` also stores the per-inscription ``letter_w`` weight
    (``letter_count_conservative``, NaN/missing -> 0) so the letter-mass model
    variant (spec §A5.1 / Obs 61–62) can weight each inscription's aoristic row
    by its letter count without re-reading the parquet. The inscription-count
    unit ignores ``letter_w`` (every inscription weight 1).

    Args:
        parquet_path: Path to the filtered LIRE parquet.
        out_dir: Directory to write the cache into (created if absent).
        bin_width: Years per bin (25 primary, 50 robustness; spec §3). Selects
            the temporal grid via :func:`make_grid`.
        letter_col: Parquet column holding the per-inscription letter count
            (default ``letter_count_conservative``, the conservative measure).

    Returns:
        ``(city_index, stats)``: the per-city index frame and the audit stats.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    bin_edges, n_bins = make_grid(bin_width)
    df, stats = load_and_filter(parquet_path, letter_col=letter_col)
    stats["bin_width"] = bin_width
    stats["n_bins"] = n_bins

    # Per-city counts and metadata. Province is the MOST-COMMON value across the
    # city's rows (alphabetical tiebreak), not the arbitrary first row (audit
    # B1); pop_est is constant within a Hanson-matched city so first() is fine.
    grp = df.groupby(CITY_COL)
    counts = grp.size()
    meta_prov = grp[PROV_COL].apply(_most_common_province)
    meta_pop = grp[POP_COL].first()
    # How many cities span >1 distinct province value (the ambiguity mode fixes).
    n_distinct_prov = grp[PROV_COL].nunique(dropna=True)
    stats["n_cities_multi_province"] = int((n_distinct_prov > 1).sum())

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

    # Province / singleton structure over the TARGET set (the §5 hierarchy).
    # A "singleton" province is one with exactly one TARGET city; these cities
    # pool toward the global trajectory (spec §4). Counted here for the cache
    # verification printout so the 45-provinces / 10-singletons claim is checked
    # at build time rather than assumed.
    target_idx = city_index[city_index["bucket"] == "target"]
    prov_counts = target_idx["province"].value_counts()
    stats["n_provinces_target"] = int(len(prov_counts))
    stats["n_singleton_provinces"] = int((prov_counts == 1).sum())

    # Cache per-city aoristic matrices for fittable cities, at the chosen grid.
    fittable = city_index[city_index["bucket"].isin(["target", "large_anchor"])]
    for city in fittable["city"]:
        sub = df[df[CITY_COL] == city]
        nb = sub["nb_clip"].to_numpy()
        na = sub["na_clip"].to_numpy()
        a = aoristic_matrix(nb, na, bin_edges=bin_edges, bin_width=bin_width)
        np.savez_compressed(
            out_dir / f"aoristic-{_safe_name(city)}.npz",
            city=np.array(city),
            province=np.array(str(meta_prov[city])),
            pop_est=np.array(float(meta_pop[city])),
            A=a.astype(np.float64),
            # Per-inscription letter weight (letter_count_conservative), parallel
            # to A's rows; 0 where the count was missing/non-positive. Used by
            # the letter-mass model variant; ignored by the inscription unit.
            letter_w=sub["letter_w"].to_numpy().astype(np.float64),
            nb_clip=nb.astype(np.int64),
            na_clip=na.astype(np.int64),
            bin_edges=bin_edges,
            bin_width=np.array(bin_width),
        )

    city_index.to_parquet(out_dir / "city-index.parquet", index=False)

    # Aoristic sanity stats on the WHOLE surviving corpus (cheap, global), at
    # the chosen grid.
    a_all = aoristic_matrix(
        df["nb_clip"].to_numpy(), df["na_clip"].to_numpy(),
        bin_edges=bin_edges, bin_width=bin_width,
    )
    stats["a_min"] = float(a_all.min())
    stats["a_max"] = float(a_all.max())
    # Coverage identity on a sample row: sum_t a*bin_width == clipped length.
    sample_i = 0
    samp_len = int(df["na_clip"].iloc[sample_i] - df["nb_clip"].iloc[sample_i])
    samp_cov = float(a_all[sample_i].sum() * bin_width)
    stats["sample_clipped_length"] = samp_len
    stats["sample_aoristic_coverage"] = samp_cov
    # And the same identity across ALL rows (max abs error), as a strong check.
    lengths = (df["na_clip"].to_numpy() - df["nb_clip"].to_numpy()).astype(float)
    cov = a_all.sum(axis=1) * bin_width
    stats["coverage_max_abs_err"] = float(np.max(np.abs(cov - lengths)))

    return city_index, stats


def load_city(out_dir: Path, city: str) -> dict:
    """Load a cached per-city aoristic bundle by city name.

    Args:
        out_dir: The cache directory used in :func:`prepare`.
        city: Exact city name (as in ``urban_context_city``).

    Returns:
        Dict with keys ``city``, ``province``, ``pop_est``, ``A`` (N x n_bins),
        ``letter_w`` (N,), ``nb_clip``, ``na_clip``, ``bin_edges``, ``bin_width``.
        ``letter_w`` is the per-inscription letter-count weight (0 where the
        count was missing); older caches without it fall back to all-ones.
    """
    path = out_dir / f"aoristic-{_safe_name(city)}.npz"
    with np.load(path, allow_pickle=True) as z:
        A = z["A"]
        # Backward-compatible: older caches predate letter_w / bin_width.
        letter_w = (
            z["letter_w"] if "letter_w" in z.files
            else np.ones(A.shape[0], dtype=np.float64)
        )
        bin_width = int(z["bin_width"]) if "bin_width" in z.files else BIN_WIDTH
        return {
            "city": str(z["city"]),
            "province": str(z["province"]),
            "pop_est": float(z["pop_est"]),
            "A": A,
            "letter_w": np.asarray(letter_w, dtype=np.float64),
            "nb_clip": z["nb_clip"],
            "na_clip": z["na_clip"],
            "bin_edges": z["bin_edges"],
            "bin_width": bin_width,
        }


# --------------------------------------------------------------------------- #
# CLI / verification printout.
# --------------------------------------------------------------------------- #

def _print_verification(stats: dict) -> None:
    """Emit the verification block required by the brief."""
    print("=" * 68)
    print("DATAPREP VERIFICATION  (§5 small-N trajectories, Layer A)")
    print("=" * 68)
    _bw = stats.get("bin_width", BIN_WIDTH)
    _nb = stats.get("n_bins", N_BINS)
    print(f"  envelope            : [{ENV_LO}, {ENV_HI}]  "
          f"({_nb} bins x {_bw}y)")
    print(f"  rows loaded         : {stats['rows_loaded']:>7}")
    print(f"  Hanson-matched      : {stats['rows_hanson_matched']:>7}")
    print(f"  Rome rows excluded  : {stats['rows_rome_excluded']:>7}")
    print(f"  after Rome excl.    : {stats['rows_after_rome']:>7}")
    print(f"  dropped NaN dates   : {stats['rows_dropped_nan_dates']:>7}")
    print(f"  after NaN-date drop : {stats['rows_after_nan_drop']:>7}")
    print(f"  overlap envelope    : {stats['rows_overlap_envelope']:>7}")
    print(f"  dropped clip/overlap: {stats['rows_dropped_clip_overlap']:>7}")
    print(f"  surviving rows      : {stats['rows_surviving']:>7}")
    print("-" * 68)
    _env_ok = (
        "no out-of-envelope dates survive — OK"
        if stats["surviving_na_clip_gt_env_hi"] == 0
        else "OUT-OF-ENVELOPE SURVIVES — BAD"
    )
    print(f"  raw not_after>{ENV_HI}   : {stats['raw_not_after_gt_env_hi']}  "
          f"-> surviving na_clip>{ENV_HI}: {stats['surviving_na_clip_gt_env_hi']}  "
          f"(surviving na_clip max = {stats['surviving_na_clip_max']})  "
          f"({_env_ok})")
    print(f"  not_after==2230 rec : total={stats['bad_2230_rows_total']}  "
          f"kept={stats['bad_2230_rows_kept']}  "
          f"clipped-to={stats['bad_2230_clipped_to']}  "
          f"(repaired-by-clip, not dropped — its not_before is valid; "
          f"the absurd 2230 upper date is removed)")
    print("-" * 68)
    print(f"  cities (any N)      : {stats['n_cities_total']:>7}")
    # Label reflects the ACTUAL computed count, not a hardcoded spec figure
    # (audit C-ii): the post-clip target restores Romula etc. (exact Rome match).
    print(f"  TARGET (50<=N<1549) : {stats['n_target']:>7}   "
          f"(computed; post-clip exact-Rome target set)")
    print(f"  large anchor (>=1549): {stats['n_large_anchor']:>6}")
    print(f"  below floor (N<50)  : {stats['n_below_floor']:>7}")
    print(f"  cities >1 province  : {stats['n_cities_multi_province']:>7}   "
          f"(province assigned by mode, alphabetical tiebreak)")
    print(f"  provinces (target)  : {stats.get('n_provinces_target', '?'):>7}   "
          f"(distinct provinces over the target set)")
    print(f"  singleton provinces : {stats.get('n_singleton_provinces', '?'):>7}   "
          f"(one target city; pool to global, spec §4)")
    print(f"  large-anchor names  : {stats['large_anchor_names']}")
    print(f"  letter column       : "
          f"{'present' if stats.get('has_letter_col') else 'ABSENT'}   "
          f"(letter_count_conservative; letter-mass unit)")
    print("-" * 68)
    _a_ok = (
        "in [0,1] — OK"
        if 0.0 <= stats["a_min"] and stats["a_max"] <= 1.0 + 1e-9
        else "OUT OF RANGE — BAD"
    )
    print(f"  aoristic a min/max  : {stats['a_min']:.6f} / {stats['a_max']:.6f}  "
          f"({_a_ok})")
    _cov_ok = (
        "MATCH"
        if abs(stats["sample_aoristic_coverage"]
               - stats["sample_clipped_length"]) < 1e-6
        else "MISMATCH"
    )
    print(f"  sample row coverage : sum_t a*{_bw} = "
          f"{stats['sample_aoristic_coverage']:.4f}  vs clipped length "
          f"{stats['sample_clipped_length']}  "
          f"({_cov_ok})")
    print(f"  coverage identity   : max |sum_t a*{_bw} - len| over all rows "
          f"= {stats['coverage_max_abs_err']:.2e}")
    print("=" * 68)


def default_cache_dir(bin_width: int = BIN_WIDTH) -> Path:
    """Canonical cache directory for a given bin width.

    25y (primary) keeps the historical ``code/prepared`` path so existing
    callers and caches are unaffected; coarser grids get a suffixed sibling
    (e.g. ``code/prepared-50y``). All §5 scripts derive their default cache
    location from this function, so the 25y / 50y split is consistent.
    """
    base = Path(__file__).resolve().parent
    return base / ("prepared" if bin_width == BIN_WIDTH else f"prepared-{bin_width}y")


def main() -> int:
    """Command-line entry point for the data-prep stage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parquet", type=Path, default=DEFAULT_PARQUET,
        help="Path to the filtered LIRE parquet (default: repo-relative).",
    )
    parser.add_argument(
        "--bin-width", type=int, default=BIN_WIDTH,
        choices=SUPPORTED_BIN_WIDTHS,
        help="Years per bin: 25 (primary, 16 bins) or 50 (robustness, 8 bins).",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=None,
        help="Cache output directory (default: code/prepared for 25y, "
             "code/prepared-<width>y otherwise).",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Print the verification block after preparing.",
    )
    args = parser.parse_args()

    if not args.parquet.exists():
        print(f"FATAL: parquet not found at {args.parquet}")
        return 2

    out_dir = args.out_dir or default_cache_dir(args.bin_width)
    _city_index, stats = prepare(args.parquet, out_dir, bin_width=args.bin_width)
    if args.verify:
        _print_verification(stats)
    print(f"\nCache written to: {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
