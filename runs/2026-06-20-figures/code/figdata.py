#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figdata.py — shared data access for the key-findings figure set.
================================================================

Centralises the non-trivial, shared data machinery the SPD figures (F1–F4, and
the F13 atlas) all need, so each figure script stays short and they cannot drift
apart on grid or unit definitions:

* the **time grid** (80 × 5-year bins over 50 BC – AD 350), re-exported from the
  canonical ``h2_lib`` (the production deconvolution harness) so the figures use
  the EXACT grid the fits used;
* the **raw (uncorrected) aoristic SPD** per unit, recomputed from the
  180,609-row prereg-filtered LIRE corpus via ``h2_lib`` (reuse, not re-derive);
* the **convention component** (F1+F3 round-slab families) — the spikes F1
  highlights;
* the **corrected (genuine) SPD posterior draws** per unit, loaded from the
  cross-classified production refit (``*-pgen.npz``: 8 000 draws × 80 bins,
  each a normalised distribution over time);
* small helpers: name→file slug, unit enumeration, and posterior quantile bands.

Why import ``h2_lib`` rather than copy its functions: ``h2_lib`` guards its
envelope against ``design.json`` drift (``_assert_envelope_matches_design``), so
importing keeps the figures byte-aligned with the validated pipeline. The import
pulls in pymc (a few seconds) because ``h2_lib`` loads the model builder at
import time; that one-off cost is acceptable for figure scripts.

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-20.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")

# Import the canonical production harness (grid + aoristic + unit enumeration).
_H2_DIR = PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
sys.path.insert(0, str(_H2_DIR))
import h2_lib as H  # noqa: E402

# The cross-classified production refit's per-unit genuine-SPD posterior draws.
DRAWS_DIR = (PROJECT_ROOT / "runs" / "2026-06-13-cc-production-refit"
             / "outputs" / "posterior-draws")

# --------------------------------------------------------------------------- #
# Time grid — re-exported from h2_lib so the figures cannot diverge from it.    #
# --------------------------------------------------------------------------- #
ENV_START = H.ENV_START          # -50  (50 BC)
ENV_END = H.ENV_END              # 350  (AD 350)
BIN_SIZE = H.BIN_SIZE            # 5 years
N_BINS = H.N_BINS                # 80
BIN_EDGES = H.BIN_EDGES.copy()   # (81,) edges
BIN_CENTRES = H.BIN_CENTRES.copy()  # (80,) centres: -47.5 .. 347.5


def years() -> np.ndarray:
    """Bin-centre years (the x-axis for every SPD figure), length 80."""
    return BIN_CENTRES.copy()


# --------------------------------------------------------------------------- #
# Unit ↔ file slug (the refit's _safe()), and unit enumeration.                #
# --------------------------------------------------------------------------- #
def safe_name(name: str) -> str:
    """The refit's filename slug (``run_refit._safe``): the npz / json stem."""
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


@lru_cache(maxsize=1)
def units() -> tuple[dict, ...]:
    """The ordered unit list (``h2_lib.enumerate_units``): name, kind, frame, tier."""
    return tuple(H.enumerate_units())


def units_by_kind(kind: str) -> list[dict]:
    """Units of a given ``kind`` (``"aggregate"`` / ``"province"`` / ``"city"``)."""
    return [u for u in units() if u["kind"] == kind]


def unit_by_name(name: str) -> dict:
    """Look up one unit dict by exact name (raises if absent)."""
    for u in units():
        if u["name"] == name:
            return u
    raise KeyError(f"no unit named {name!r}; available: "
                   f"{[u['name'] for u in units()]}")


def draws_available() -> set[str]:
    """The set of unit names that have a ``*-pgen.npz`` draws file on disk."""
    return {p.name[:-len("-pgen.npz")] for p in DRAWS_DIR.glob("*-pgen.npz")}


# --------------------------------------------------------------------------- #
# Corpus + raw aoristic SPD (recomputed from LIRE via h2_lib).                  #
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def corpus() -> pd.DataFrame:
    """The 180,609-row prereg-filtered LIRE corpus, with the family classifier.

    Cached for the process. Adds the ``family`` column (F1_round / F3_periodic /
    Tight / F2_Other / Big) used to isolate the convention component.
    """
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    return df


@lru_cache(maxsize=1)
def latin_set() -> frozenset[str]:
    """The set of Latin-speaking provinces (for the ``latin-aggregate`` subset)."""
    return frozenset(H.latin_provinces())


def _subset(name: str) -> pd.DataFrame:
    """The corpus rows for a named unit (via its enumerate_units filter)."""
    return H.subset_corpus(corpus(), unit_by_name(name), set(latin_set()))


def unit_n_rows(name: str) -> int:
    """Number of inscription rows in a named unit's corpus subset."""
    return int(len(_subset(name)))


def raw_aoristic_mass(name: str) -> np.ndarray:
    """Raw (uncorrected) aoristic SPD for a unit, in MASS units (sums to N_eff).

    Each inscription deposits mass 1.0 spread uniformly over [not_before,
    not_after], clipped to the envelope — the honest, convention-contaminated
    summed-probability curve the deconvolution corrects.
    """
    sub = _subset(name)
    return H.aoristic_spa(sub["nb"].to_numpy(), sub["na"].to_numpy())


def convention_mass(name: str) -> np.ndarray:
    """Aoristic SPD of the convention families only (F1_round + F3_periodic).

    The round-number-slab component whose spikes F1 highlights; the rest of the
    raw curve is the (Tight / Big / Other) non-convention mass.
    """
    sub = _subset(name)
    is_conv = np.isin(sub["family"].to_numpy(), ["F1_round", "F3_periodic"])
    s = sub.loc[is_conv]
    return H.aoristic_spa(s["nb"].to_numpy(), s["na"].to_numpy())


# --------------------------------------------------------------------------- #
# Corrected (genuine) SPD posterior draws.                                     #
# --------------------------------------------------------------------------- #
def genuine_draws(name: str) -> np.ndarray:
    """Genuine-SPD posterior draws for a unit: ``(n_draws, 80)``, each summing≈1.

    Loaded from the cross-classified refit's ``<slug>-pgen.npz`` (8 000 draws).
    """
    npz = DRAWS_DIR / f"{safe_name(name)}-pgen.npz"
    if not npz.exists():
        raise FileNotFoundError(f"no genuine draws for {name!r} at {npz}")
    with np.load(npz) as d:
        return np.asarray(d["p_gen"], dtype=float)


# --------------------------------------------------------------------------- #
# Distribution + band helpers.                                                 #
# --------------------------------------------------------------------------- #
def normalise(spd: np.ndarray) -> np.ndarray:
    """Scale a non-negative SPD to sum to 1 (a probability over time bins)."""
    total = float(np.sum(spd))
    return spd / total if total > 0 else spd


def as_density(spd_sum1: np.ndarray) -> np.ndarray:
    """Convert a sum-to-1 SPD to a per-YEAR density (area under the curve = 1)."""
    return spd_sum1 / BIN_SIZE


def quantile_band(draws: np.ndarray, lower: float = 2.5, upper: float = 97.5
                  ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-bin ``(lo, median, hi)`` over the draw axis of a ``(n_draws, 80)`` array."""
    lo = np.percentile(draws, lower, axis=0)
    med = np.percentile(draws, 50.0, axis=0)
    hi = np.percentile(draws, upper, axis=0)
    return lo, med, hi
