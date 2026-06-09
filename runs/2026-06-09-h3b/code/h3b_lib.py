#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""h3b_lib.py — H3b deviation-detection harness (library).

H3b is the project's pre-specified EXPLORATORY temporal deviation-detection
(preregistration §4 H3b; Decision 15). It scans each geographic unit's
editorial-convention-CORRECTED genuine summed-probability analysis (SPA) — the
H2.1 hand-off — against a featureless-null permutation envelope, and reads the
result at two pre-specified probe windows (Antonine AD 165–180; Crisis of the
Third Century AD 235–284 inclusive).

Design principle — **REUSE, do not reimplement**. All three pieces of machinery
already exist and are validated:

  * the forward-fit exponential null + forward Monte-Carlo (MC) sampler + Timpson
    et al. (2014) envelope test live in
    ``runs/2026-04-25-h1-simulation/code/forward_fit.py``;
  * the CPL-3 null fit + MC sampler + envelope test + bin grid + brackets live in
    ``runs/2026-04-25-h1-simulation/code/primitives.py``;
  * the per-unit corpus reconstruction + corrected-SPA hand-off live in
    ``runs/2026-06-07-h2.1-launch-prep/code/h2_lib.py`` + the production unit
    JSONs.

This module is a thin driver over those. See ``h3b-spec.md`` for the full design
and the open questions; load-bearing choices flagged ``OQ-N`` there.

Seed discipline: every stochastic call takes an explicit ``numpy`` Generator.
Master seed ``20260609``; per-unit generator = ``default_rng(20260609 + index)``.

Author: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np

# --------------------------------------------------------------------------- #
# Paths + reused-module imports (absolute; repo at same path on all hosts).     #
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
H1_CODE = PROJECT_ROOT / "runs" / "2026-04-25-h1-simulation" / "code"
H2_CODE = PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
UNITS_DIR = (
    PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep"
    / "outputs" / "production" / "units"
)

sys.path.insert(0, str(H1_CODE))
sys.path.insert(0, str(H2_CODE))

# Reused Phase-1 envelope machinery (validated; not reimplemented).
from forward_fit import (  # noqa: E402
    fit_null_exponential_forward,
    forward_envelope_test,
)
from primitives import (  # noqa: E402
    BIN_CENTRES,
    BIN_EDGES,
    BRACKETS,
    fit_null_cpl,
    permutation_envelope_test,
)

# Reused H2.1 corpus reconstruction (verbatim unit membership).
import h2_lib  # noqa: E402

# --------------------------------------------------------------------------- #
# Constants — seeds, MC, probe windows.                                         #
# --------------------------------------------------------------------------- #
MASTER_SEED: int = 20260609
N_MC: int = 1000            # prereg line 310 (Phase-1 MC-replicate convention).
ALPHA_LEVEL: float = 0.05   # envelope / global-test significance level.
ENV_START: float = -50.0
ENV_END: float = 350.0

# Probe windows (prereg lines 98–99). Antonine AD 165–180; Crisis AD 235–284
# inclusive (50 y under inclusive-Roman counting). A bin (centre c, width 5)
# is "in window" if its centre lies within [lo, hi].
ANTONINE_WINDOW: tuple[float, float] = (165.0, 180.0)
CRISIS_WINDOW: tuple[float, float] = (235.0, 284.0)

# The gap threshold for the identifiable set (mirrors compute_identifiability).
GAP_THRESHOLD: float = 0.20


# ======================================================================= #
# Unit data assembly.                                                       #
# ======================================================================= #
@dataclass
class UnitData:
    """Everything H3b needs for one unit.

    Attributes
    ----------
    name : str
        Unit name (matches the H2.1 production JSON ``name``).
    unit_index : int
        Stable index (drives the per-unit seed).
    n_eff : int
        Effective corpus size from H2.1 (the count the corrected SPA scales to).
    corrected_spa : numpy.ndarray
        The 80-bin posterior-median corrected genuine SPA (sums to 1); the H3b
        observed signal.
    raw_spa : numpy.ndarray
        The 80-bin aoristic SPA of the *raw* (uncorrected) unit corpus, scaled to
        sum to 1 — for the raw-vs-corrected follow-up (launch-spec §8).
    nb, na : numpy.ndarray
        Per-row interval bounds of the unit's member rows (for the forward null
        fit + empirical width distribution).
    widths : numpy.ndarray
        ``na − nb`` (empirical interval-width distribution; the forward sampler
        re-applies this).
    gap : float
        ``f1f3_family_mass_fraction − alpha_median`` (the identifiability flag).
    identifiable : bool
        ``gap < GAP_THRESHOLD``.
    final_tier : str
        H2.1 reporting tier (context only).
    """

    name: str
    unit_index: int
    n_eff: int
    corrected_spa: np.ndarray
    raw_spa: np.ndarray
    nb: np.ndarray
    na: np.ndarray
    widths: np.ndarray
    gap: float
    identifiable: bool
    final_tier: str


def _load_unit_json(name: str) -> dict[str, Any]:
    """Find and load the production unit JSON whose ``name`` matches."""
    for path in sorted(UNITS_DIR.glob("unit-*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        if d.get("name") == name:
            return d
    raise KeyError(f"no production unit JSON with name {name!r}")


def assemble_unit_data() -> list[UnitData]:
    """Reconstruct every H2.1 unit's corpus, corrected SPA, and intervals.

    Uses the H2.1 production harness verbatim for corpus membership, so the rows
    are byte-identical to those the H2.1 fits saw. The corrected SPA + n_eff come
    from the saved unit JSONs (no refit).

    Returns
    -------
    list[UnitData]
        One per production unit, in unit-index order.
    """
    df = h2_lib.load_filtered_lire()
    df["family"] = h2_lib.classify_family(df)
    latin = h2_lib.latin_provinces()
    units_meta = h2_lib.enumerate_units()

    # The H2.1 production set added 'Italia (excl. Rome)' (unit-29) post-hoc — the
    # 11 Augustan regiones aggregated (prereg note §4, lines 73–79). It is NOT in
    # enumerate_units() (built from the earlier unit-set.json), so append it here.
    # Its corpus = the union of the LIRE '… / Regio N' provinces (Rome is the
    # separate 'Roma' province, excluded by construction). Verified: this
    # reconstruction reproduces the saved Italia n_eff (40,499) exactly.
    if not any("Italia" in u["name"] for u in units_meta):
        regiones = sorted(p for p in df["province"].dropna().unique()
                          if "/ Regio" in p)
        units_meta = units_meta + [{
            "name": "Italia (excl. Rome)", "kind": "aggregate", "frame": "latin",
            "tier": "secondary", "filter": ("province_in", regiones),
            "unit_index": 29,
        }]

    out: list[UnitData] = []
    for unit in units_meta:
        try:
            d = _load_unit_json(unit["name"])
        except KeyError:
            # A unit may be in enumerate_units but lack a saved JSON; skip it.
            continue
        # Italia uses a 'province_in' filter not understood by h2_lib; handle it
        # here, otherwise defer to the verbatim H2.1 subsetter.
        if unit["filter"][0] == "province_in":
            df_u = df.loc[df["province"].isin(unit["filter"][1])]
        else:
            df_u = h2_lib.subset_corpus(df, unit, latin)
        nb = df_u["nb"].to_numpy(dtype=float)
        na = df_u["na"].to_numpy(dtype=float)
        widths = na - nb

        corrected = np.asarray(d["corrected_genuine_spa"], dtype=float)
        # Raw SPA of the uncorrected corpus, normalised, for the follow-up.
        raw_mass = h2_lib.aoristic_spa(nb, na)
        raw_spa = raw_mass / raw_mass.sum() if raw_mass.sum() > 0 else raw_mass

        gap = float(d["f1f3_family_mass_fraction"]) - float(d["alpha_median"])
        out.append(
            UnitData(
                name=d["name"],
                unit_index=int(d["unit_index"]),
                n_eff=int(d["n_eff"]),
                corrected_spa=corrected,
                raw_spa=raw_spa,
                nb=nb,
                na=na,
                widths=widths,
                gap=gap,
                identifiable=bool(gap < GAP_THRESHOLD),
                final_tier=str(d.get("final_tier", "?")),
            )
        )
    out.sort(key=lambda u: u.unit_index)
    return out


# ======================================================================= #
# Probe-window helpers.                                                     #
# ======================================================================= #
def window_bin_indices(window: tuple[float, float]) -> np.ndarray:
    """Indices of the 5-year bins whose centre lies within ``window`` (inclusive).

    Parameters
    ----------
    window : tuple[float, float]
        ``(lo, hi)`` calendar-year bounds (AD; BC negative).

    Returns
    -------
    numpy.ndarray
        Integer bin indices into the 80-bin grid.
    """
    lo, hi = window
    return np.where((BIN_CENTRES >= lo) & (BIN_CENTRES <= hi))[0]


# ======================================================================= #
# The deviation test for one unit × one null.                              #
# ======================================================================= #
@dataclass
class DeviationResult:
    """Outcome of one unit × one null-family envelope test."""

    name: str
    null: str
    n_eff: int
    identifiable: bool
    pval_global: float
    detected: bool
    n_bins_outside: int
    out_bin_indices: list[int] = field(default_factory=list)
    out_bin_signs: list[int] = field(default_factory=list)  # +1 surplus, −1 deficit
    lo_env: list[float] = field(default_factory=list)
    hi_env: list[float] = field(default_factory=list)
    observed_counts: list[float] = field(default_factory=list)
    null_param: dict[str, Any] = field(default_factory=dict)
    seed: int = 0
    # Per-probe-window summaries (filled by summarise_probe).
    probes: dict[str, Any] = field(default_factory=dict)
    # Holm-adjusted p (filled in the cross-family Holm step).
    pval_holm: float | None = None


def run_unit_null(
    unit: UnitData,
    null: Literal["exponential", "cpl3"],
    rng: np.random.Generator,
    n_mc: int = N_MC,
    signal: Literal["corrected", "raw"] = "corrected",
) -> DeviationResult:
    """Run the featureless-null envelope test for one unit under one null.

    The observed signal is the (corrected or raw) SPA scaled to ``n_eff`` counts,
    so observed and null replicates share the count scale (spec §4.2). The null is
    fit to the unit's *raw* intervals in true-date space (forward fit, the
    documented false-positive fix) — for both nulls the null describes featureless
    growth/decline of the underlying corpus.

    Parameters
    ----------
    unit : UnitData
        Assembled unit data.
    null : {'exponential', 'cpl3'}
        Null family. Exponential is the forward-fit primary; CPL-3 is the
        secondary cross-check (uses the older smeared-fit sampler — see spec OQ-4).
    rng : numpy.random.Generator
        Seeded generator (per-unit).
    n_mc : int
        Monte-Carlo replicate count.
    signal : {'corrected', 'raw'}
        Which SPA to test (corrected = primary H3b; raw = follow-up comparison).

    Returns
    -------
    DeviationResult
    """
    spa_dist = unit.corrected_spa if signal == "corrected" else unit.raw_spa
    observed_counts = spa_dist * unit.n_eff

    if null == "exponential":
        fit = fit_null_exponential_forward(
            intervals=None, nb=unit.nb, na=unit.na,
            t_min=ENV_START, t_max=ENV_END,
        )
        test = forward_envelope_test(
            observed_spa=observed_counts,
            b_hat=fit["b"],
            widths=unit.widths,
            bin_edges=BIN_EDGES,
            n_mc=n_mc,
            rng=rng,
            n=unit.n_eff,
            alpha=ALPHA_LEVEL,
            t_min=ENV_START,
            t_max=ENV_END,
        )
        null_param = {"model": "exponential", "b": fit["b"],
                      "log_likelihood": fit["log_likelihood"],
                      "converged": fit["converged"], "n_obs": fit["n_obs"]}
    elif null == "cpl3":
        # CPL-3 fitted on the observed count SPA via Poisson NLL; MC via the
        # smeared-fit sampler (Poisson noise on the fitted mean). Secondary null.
        fit = fit_null_cpl(observed_counts, BIN_CENTRES, k=3, seed=int(rng.integers(1 << 30)))
        test = permutation_envelope_test(
            observed_spa=observed_counts,
            null_params=fit,
            model="cpl",
            bin_centres=BIN_CENTRES,
            n_mc=n_mc,
            rng=rng,
            alpha=ALPHA_LEVEL,
        )
        null_param = {"model": "cpl3", "knots": [float(x) for x in fit["knots"]],
                      "aic": fit["aic"], "converged": fit["converged"]}
    else:
        raise ValueError(f"unknown null {null!r}")

    lo_env = np.asarray(test["lo_env"], dtype=float)
    hi_env = np.asarray(test["hi_env"], dtype=float)
    out_mask = (observed_counts < lo_env) | (observed_counts > hi_env)
    out_idx = np.where(out_mask)[0]
    out_signs = np.where(observed_counts[out_idx] > hi_env[out_idx], 1, -1)

    return DeviationResult(
        name=unit.name,
        null=null,
        n_eff=unit.n_eff,
        identifiable=unit.identifiable,
        pval_global=float(test["pval_global"]),
        detected=bool(test["detected"]),
        n_bins_outside=int(test["n_bins_outside"]),
        out_bin_indices=[int(i) for i in out_idx],
        out_bin_signs=[int(s) for s in out_signs],
        lo_env=[float(x) for x in lo_env],
        hi_env=[float(x) for x in hi_env],
        observed_counts=[float(x) for x in observed_counts],
        null_param=null_param,
        seed=int(MASTER_SEED + unit.unit_index),
    )


def summarise_probe(
    result: DeviationResult,
    window: tuple[float, float],
    label: str,
) -> dict[str, Any]:
    """Summarise a result's behaviour inside one probe window.

    Records: any-bin-out-of-envelope flag, the out bins in the window, the signed
    direction (surplus/deficit), and the descriptive effect-size bracket the
    windowed observed departure most resembles (relative to the null centre).

    Returns
    -------
    dict
        Probe summary; also stored on ``result.probes[label]``.
    """
    idx = window_bin_indices(window)
    obs = np.asarray(result.observed_counts, dtype=float)
    lo = np.asarray(result.lo_env, dtype=float)
    hi = np.asarray(result.hi_env, dtype=float)
    centre = 0.5 * (lo + hi)

    out_mask = (obs[idx] < lo[idx]) | (obs[idx] > hi[idx])
    out_idx = idx[out_mask]
    out_signs = np.where(obs[out_idx] > hi[out_idx], 1, -1) if out_idx.size else np.array([])

    # Descriptive bracket: largest signed relative departure from null centre in
    # the window (against the project brackets; descriptive only, no decision).
    rel = np.zeros_like(idx, dtype=float)
    for j, b in enumerate(idx):
        c = centre[b]
        rel[j] = (obs[b] - c) / c if c > 0 else 0.0
    # Most extreme departure in the window.
    if rel.size:
        k = int(np.argmax(np.abs(rel)))
        peak_rel = float(rel[k])
        peak_year = float(BIN_CENTRES[idx[k]])
    else:
        peak_rel, peak_year = 0.0, float("nan")

    bracket = _describe_bracket(peak_rel)
    return {
        "window": list(window),
        "any_out_of_envelope": bool(out_idx.size > 0),
        "n_bins_out": int(out_idx.size),
        "out_bin_years": [float(BIN_CENTRES[i]) for i in out_idx],
        "out_signs": [int(s) for s in out_signs],
        "direction": ("deficit" if (out_signs.size and (out_signs < 0).all())
                      else "surplus" if (out_signs.size and (out_signs > 0).all())
                      else "mixed" if out_signs.size else "none"),
        "peak_relative_departure": peak_rel,
        "peak_year": peak_year,
        "descriptive_bracket": bracket,
    }


def _describe_bracket(rel: float) -> str:
    """Map a signed relative departure to a descriptive project bracket label.

    Descriptive only (prereg line 101 — no magnitude pre-committed). Compares the
    magnitude against the brackets in ``primitives.BRACKETS``.
    """
    mag = abs(rel)
    sign = "surplus" if rel > 0 else "deficit"
    # Brackets (by magnitude): doubling (+1.0) > 50% (0.5) > 20% (0.2).
    if mag >= 1.0:
        return f"≥ doubling ({sign})"
    if mag >= 0.5:
        return f"≥ 50% ({sign})"
    if mag >= 0.2:
        return f"≥ 20% ({sign})"
    return f"< 20% ({sign}; sub-bracket)"


# ======================================================================= #
# Holm–Bonferroni (descriptive multiplicity diagnostic — NOT confirmatory). #
# ======================================================================= #
def holm_adjust(pvals: list[float]) -> list[float]:
    """Holm–Bonferroni step-down adjustment of a family of raw p-values.

    Returned in the ORIGINAL order. This is reported descriptively per the brief;
    per the prereg (line 101) + Decision 15 H3b forms **no** Holm-corrected
    confirmatory family — the adjusted p is a multiplicity diagnostic only (spec
    §2, OQ-1).

    Parameters
    ----------
    pvals : list[float]
        Raw p-values.

    Returns
    -------
    list[float]
        Holm-adjusted p-values (monotone non-decreasing along the sorted order),
        clipped to [0, 1], in the input order.
    """
    m = len(pvals)
    if m == 0:
        return []
    order = np.argsort(pvals)
    adj_sorted = np.empty(m, dtype=float)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * pvals[idx]
        running = max(running, val)  # enforce monotonicity
        adj_sorted[idx] = min(running, 1.0)
    return [float(x) for x in adj_sorted]
