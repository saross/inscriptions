#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cell_lib.py
===========

Shared library for the 2026-05-26 two-unit recovery-grid re-simulation
(``runs/2026-05-26-recovery-grid-two-unit/``). This consolidates the
envelope / tier-basis / shape-library / cell-enumeration / model
construction helpers used by both grid runs (Grid A inscription-mass,
Grid B letter-mass conservative).

Design lineage
--------------
Ported from the 2026-05-22 production harness
(``runs/2026-05-22-recovery-grid-validation/code/01-synthetic-cell-generator.py``
and ``02-cell-mixture-fit.py``) with two structural fixes baked in:

- **F1** — α prior is ``Beta(1, 1)`` (uniform on [0, 1]), replacing the
  2026-05-22 ``Beta(2, 2)``. Source: 2026-05-24 follow-up
  ``runs/2026-05-24-followup-alpha-prior/``.
- **F3** — non-centred Gaussian-random-walk reparameterisation of
  ``log_pgen_increments``. Source: 2026-05-24 follow-up
  ``runs/2026-05-24-followup-noncentred-grw/``.

No other priors, sampling settings, or likelihood structures change vs
2026-05-22. The genuine-shape library, envelope, alpha grid, tier-basis
construction, N grid, and seed-policy mechanics are byte-equivalent to
the 2026-05-22 design.json.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's two-unit re-sim
brief. UK / Australian English; Oxford comma.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# Convergence gate (canonical, single source of truth).
# ---------------------------------------------------------------------------
# Field-standard, benign-divergence-tolerant per-replicate convergence gate
# (Decision 33 / OSF Amendment 01 §A5.5.1, refined 2026-06-04): R-hat +
# bulk-ESS only. Divergences are NOT a per-replicate zero-tolerance auto-fail —
# that was stricter than field practice (Stan diagnostics guidance;
# Betancourt 2017: investigate, don't auto-reject; Vehtari et al. 2021; no
# surveyed source endorses a divergence-rate threshold) and it failed benign
# flat-null divergences. Divergence counts are still recorded per replicate and
# assessed for benignity (scattered + recovery-unaffected) at the grid level.
#
# This gate is THE single definition consumed by BOTH the fitter (``fit.py``,
# at fit time) and the aggregator (``aggregate.py``, which re-derives the
# per-replicate verdict from the stored raw R-hat / bulk-ESS so a gate change
# re-aggregates WITHOUT re-fitting). They previously each carried their own
# copy; the drift between them — fit.py changed to drop divergences, aggregate.py
# still averaging the fit-time-stored verdict — was the 2026-06-04 "harness
# emits 91.9% but the data scores 98.6%" bug. Keep it here, import it there.
RHAT_GATE = 1.01  # per-replicate max R-hat must be strictly below this
ESS_GATE = 400    # per-replicate min bulk-ESS must be at least this


def convergence_pass(max_rhat: float, min_ess_bulk: float) -> bool:
    """Field-standard per-replicate convergence verdict (R-hat + bulk-ESS only).

    Parameters
    ----------
    max_rhat : float
        The maximum R-hat across the replicate's monitored parameters.
    min_ess_bulk : float
        The minimum bulk effective sample size across those parameters.

    Returns
    -------
    bool
        ``True`` iff ``max_rhat < RHAT_GATE`` and ``min_ess_bulk >= ESS_GATE``.
        Divergences are deliberately excluded (see module note above); they are
        recorded separately and assessed for benignity at the grid level.
    """
    return bool(max_rhat < RHAT_GATE and min_ess_bulk >= ESS_GATE)


# ---------------------------------------------------------------------------
# Envelope (5-year binning, AD-50 to AD 350, 80 bins) — frozen from design.json.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Envelope:
    """5-year binning envelope; mirrors design.json#envelope."""

    envelope_min_year: int
    envelope_max_year: int
    bin_width_years: int

    @property
    def bin_edges(self) -> np.ndarray:
        """Bin edges including the rightmost edge."""
        return np.arange(
            self.envelope_min_year,
            self.envelope_max_year + 1,
            self.bin_width_years,
            dtype=float,
        )

    @property
    def bin_centres(self) -> np.ndarray:
        """Midpoint of each 5-year bin (length = n_bins)."""
        edges = self.bin_edges
        return (edges[:-1] + edges[1:]) / 2.0

    @property
    def n_bins(self) -> int:
        return int(self.bin_centres.size)


def load_design(design_json_path: Path) -> dict[str, Any]:
    """Load the 2026-05-22 design.json (the source of truth for cell axes)."""
    with design_json_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def make_envelope(design: dict[str, Any]) -> Envelope:
    """Materialise the Envelope dataclass from design.json#envelope."""
    env = design["envelope"]
    return Envelope(
        envelope_min_year=int(env["envelope_min_year"]),
        envelope_max_year=int(env["envelope_max_year"]),
        bin_width_years=int(env["bin_width_years"]),
    )


# ---------------------------------------------------------------------------
# Tier basis (Decision 20: century / half-century / reign).
# ---------------------------------------------------------------------------
def build_tier_basis(design: dict[str, Any], env: Envelope) -> np.ndarray:
    """Construct the 3 x N_BINS tier-basis matrix.

    Row k is the interval-width-normalised uniform-mass vector over tier
    k's template-interval dictionary, with within-tier intervals
    equally-weighted and the row renormalised to sum to 1. Byte-identical
    to the 2026-05-22 build_tier_basis.
    """
    tier_order = design["tier_order"]
    intervals_by_tier = design["template_intervals_by_tier"]
    n_bins = env.n_bins
    bin_lo = env.bin_edges[:-1]
    bin_hi = env.bin_edges[1:]

    basis = np.zeros((len(tier_order), n_bins), dtype=float)
    for k, tier_name in enumerate(tier_order):
        intervals = intervals_by_tier[tier_name]
        tier_sum = np.zeros(n_bins, dtype=float)
        for interval in intervals:
            lo = float(interval["lo"])
            hi = float(interval["hi"])
            overlap = np.maximum(
                0.0, np.minimum(bin_hi, hi) - np.maximum(bin_lo, lo)
            )
            width = hi - lo
            if width <= 0:
                continue
            per_bin_mass = overlap / width
            s = per_bin_mass.sum()
            if s > 0:
                tier_sum += per_bin_mass / s
        s = tier_sum.sum()
        if s <= 0:
            raise ValueError(
                f"Tier {tier_name!r} produced an all-zero basis row; "
                "check template_intervals_by_tier in design.json."
            )
        basis[k] = tier_sum / s
    return basis


# ---------------------------------------------------------------------------
# Shape library (p_gen generators) — byte-identical to 2026-05-22.
# ---------------------------------------------------------------------------
def build_pgen(shape_spec: dict[str, Any], env: Envelope) -> np.ndarray:
    """Build a sum-to-1 p_gen vector for one shape from the library."""
    centres = env.bin_centres
    gen = shape_spec["generator"]
    params = shape_spec.get("parameters", {})
    if gen == "uniform":
        v = np.ones_like(centres)
    elif gen == "exponential":
        rate = float(params["rate_per_year"])
        sign = float(params["sign"])
        v = np.exp(sign * rate * (centres - env.envelope_min_year))
    elif gen == "gaussian":
        mu = float(params["mu_year"])
        sigma = float(params["sigma_year"])
        z = (centres - mu) / sigma
        v = np.exp(-0.5 * z * z)
    elif gen == "gaussian_mixture":
        v = np.zeros_like(centres)
        for comp in params["components"]:
            mu = float(comp["mu_year"])
            sigma = float(comp["sigma_year"])
            w = float(comp["weight"])
            z = (centres - mu) / sigma
            v = v + w * np.exp(-0.5 * z * z)
    elif gen == "regnal_plus_smooth":
        v = np.zeros_like(centres)
        for spike in params["spikes"]:
            mu = float(spike["mu_year"])
            sigma = float(spike["sigma_year"])
            w = float(spike["weight"])
            g = np.exp(-0.5 * ((centres - mu) / sigma) ** 2)
            g = g / g.sum()
            v = v + w * g
        baseline_w = float(params["baseline_weight"])
        baseline_gen = params["baseline_generator"]
        baseline_params = params["baseline_parameters"]
        if baseline_gen == "exponential":
            rate = float(baseline_params["rate_per_year"])
            sign = float(baseline_params["sign"])
            base = np.exp(sign * rate * (centres - env.envelope_min_year))
            base = base / base.sum()
            v = v + baseline_w * base
        else:
            raise ValueError(
                f"Unsupported baseline_generator {baseline_gen!r}"
            )
    else:
        raise ValueError(f"Unknown shape generator {gen!r}")

    s = v.sum()
    if s <= 0:
        raise ValueError(
            f"Shape {shape_spec['name']!r} produced a zero-sum p_gen vector."
        )
    return v / s


# ---------------------------------------------------------------------------
# Cell enumeration and seeding.
# ---------------------------------------------------------------------------
def make_cell_id(
    shape_name: str, alpha: float, tier_name: str, n: int
) -> str:
    """Human-readable cell id (matches 2026-05-22 convention)."""
    return (
        f"shape={shape_name}_alpha={alpha:.2f}"
        f"_tier={tier_name}_N={n}"
    )


def enumerate_grid_cells(
    design: dict[str, Any],
    pilot_proxy_weights: tuple[float, float, float] | None = None,
) -> list[dict[str, Any]]:
    """Enumerate all 450 cells in the deterministic design-pinned order.

    Order: shape_name (alphabetical) x alpha (ascending) x
    tier_weights_name (alphabetical) x N (ascending).

    If ``pilot_proxy_weights`` is supplied, the ``pilot_proxy`` tier
    vector in design.json#tier_weight_grid is overridden with the
    provided weights (used by Grid B to swap in the letter-mass
    re-derived pilot_proxy without mutating the design.json on disk).
    """
    shape_lib = design["shape_library"]
    alpha_grid = design["alpha_grid"]
    tier_grid = [dict(t) for t in design["tier_weight_grid"]]
    n_grid = design["n_grid"]

    if pilot_proxy_weights is not None:
        for t in tier_grid:
            if t["name"] == "pilot_proxy":
                t["weights"] = list(pilot_proxy_weights)

    shape_lookup = {s["name"]: s for s in shape_lib}
    tier_lookup = {t["name"]: t for t in tier_grid}

    shape_names = sorted(shape_lookup.keys())
    tier_names = sorted(tier_lookup.keys())
    alphas = sorted(alpha_grid)
    ns = sorted(n_grid)

    cells: list[dict[str, Any]] = []
    cell_index = 0
    for shape_name in shape_names:
        for alpha in alphas:
            for tier_name in tier_names:
                for n in ns:
                    cells.append(
                        {
                            "cell_index": cell_index,
                            "cell_id": make_cell_id(
                                shape_name, float(alpha), tier_name, int(n)
                            ),
                            "shape": shape_lookup[shape_name],
                            "alpha": float(alpha),
                            "tier_weights_name": tier_name,
                            "tier_weights": np.asarray(
                                tier_lookup[tier_name]["weights"],
                                dtype=float,
                            ),
                            "n": int(n),
                        }
                    )
                    cell_index += 1
    return cells


def make_data_seed(base_seed: int, cell_index: int, replicate: int) -> int:
    """Multinomial-draw seed (spec §3.5)."""
    cell_seed = base_seed + cell_index
    return cell_seed * 1000 + replicate


def make_letter_weight_seed(
    base_seed: int, cell_index: int, replicate: int
) -> int:
    """Letter-count-draw seed for Grid B (spec §3.5).

    The large additive offset (999_000_000) keeps the multinomial-draw
    stream and the letter-count-draw stream disjoint within a replicate.
    """
    cell_seed = base_seed + cell_index
    return cell_seed * 1000 + replicate + 999_000_000


# ---------------------------------------------------------------------------
# F1 + F3 model builder (the one and only model for both grids).
# ---------------------------------------------------------------------------
def build_model_f1_f3(y: np.ndarray, tier_basis: np.ndarray):
    """Construct the prereg-binding three-tier multinomial mixture with
    the F1 (Beta(1, 1) alpha prior) and F3 (non-centred GRW on
    log_pgen_increments) structural fixes baked in.

    F1 change vs 2026-05-22:
        alpha = pm.Beta("alpha", 1.0, 1.0)      # was Beta(2, 2)

    F3 change vs 2026-05-22:
        z_pgen = pm.Normal("z_pgen", 0, 1, shape=n_bins - 1)
        log_pgen_increments = sigma_smooth * z_pgen   # was Normal(0, sigma_smooth)

    All other priors, the likelihood, and the cumsum/softmax chain are
    byte-identical to the 2026-05-22 production builder.

    Parameters
    ----------
    y : (N_BINS,) int array
        Observed multinomial counts per 5-year bin. Under letter-mass
        these are integer letter-count sums (heavier tails allowed by
        the multinomial likelihood; see spec §3.2).
    tier_basis : (3, N_BINS) float array
        Tier basis matrix; each row sums to 1.

    Returns
    -------
    model : pymc.Model
    """
    # Local import so cell_lib can be imported without pymc loaded
    # (the orchestrator imports cell_lib for cell enumeration only).
    import pymc as pm
    import pytensor.tensor as pt

    n_total = int(y.sum())
    n_bins = int(y.size)
    n_tiers = int(tier_basis.shape[0])
    assert tier_basis.shape[1] == n_bins, "tier_basis shape mismatch"

    with pm.Model() as model:
        # F1: Beta(1, 1) = Uniform(0, 1) on alpha (uniform on the
        # probability simplex; loosest prior respecting alpha in (0, 1)).
        alpha = pm.Beta("alpha", 1.0, 1.0)

        # Tier weights — unchanged from 2026-05-22.
        tier_weights = pm.Dirichlet(
            "tier_weights", a=np.ones(n_tiers, dtype=float)
        )
        p_conv = pm.Deterministic(
            "p_conv", pt.dot(tier_weights, tier_basis)
        )

        # GRW bandwidth — unchanged from 2026-05-22.
        sigma_smooth = pm.HalfNormal("sigma_smooth", sigma=1.0)

        # F3: non-centred reparameterisation. Sample standard-normal raw
        # increments and scale by sigma_smooth deterministically. This
        # breaks the funnel between sigma_smooth and the increment scale
        # that the 2026-05-22 (centred) parameterisation exhibited.
        z_pgen = pm.Normal(
            "z_pgen", mu=0.0, sigma=1.0, shape=n_bins - 1
        )
        log_pgen_increments = pm.Deterministic(
            "log_pgen_increments", sigma_smooth * z_pgen
        )

        # Cumsum + softmax — unchanged from 2026-05-22.
        log_pgen_raw = pt.concatenate(
            [pt.zeros((1,)), pt.cumsum(log_pgen_increments)]
        )
        log_pgen_centered = log_pgen_raw - pt.max(log_pgen_raw)
        unnorm = pt.exp(log_pgen_centered)
        p_gen = pm.Deterministic("p_gen", unnorm / pt.sum(unnorm))

        # Mixture + multinomial observation — unchanged from 2026-05-22.
        p_mix = alpha * p_conv + (1.0 - alpha) * p_gen
        pm.Multinomial("y_obs", n=n_total, p=p_mix, observed=y)

    return model


# ---------------------------------------------------------------------------
# Letter-count empirical distribution loader (Grid B only).
# ---------------------------------------------------------------------------
def load_letter_count_distribution(parquet_path: Path) -> np.ndarray:
    """Load ``letter_count_conservative`` as an int64 1-D array for
    iid sampling.

    The vector is the empirical support: a draw of length M from this
    vector is M iid draws from the empirical distribution. **Uncapped**
    (spec §10 Decision 2 — heavy tail is real epigraphic-cultural
    signal).
    """
    import pandas as pd
    df = pd.read_parquet(parquet_path, columns=["letter_count_conservative"])
    arr = df["letter_count_conservative"].to_numpy(dtype=np.int64)
    if arr.size == 0:
        raise ValueError(f"Empty letter_count_conservative in {parquet_path}")
    return arr


def sample_letter_counts(
    n: int, letter_dist: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    """Draw n iid letter-counts from the empirical distribution."""
    idx = rng.integers(low=0, high=letter_dist.size, size=n, dtype=np.int64)
    return letter_dist[idx]
