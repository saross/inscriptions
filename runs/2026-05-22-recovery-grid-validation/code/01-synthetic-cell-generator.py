#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-synthetic-cell-generator.py
==============================

Generate synthetic multinomial draws for one cell of the H2.1 recovery
grid (see ``runs/2026-05-22-recovery-grid-design/design.json``).

Per the design artefact, a cell is the tuple
``(alpha, shape_name, tier_weights_name, N)`` and contains 100 replicates.
For each replicate this script:

1. Builds the convention component ``p_conv`` as the
   ``tier_weights @ tier_basis`` linear combination, where ``tier_basis``
   is the 3 × N_BINS matrix of interval-width-normalised uniform-mass
   vectors over the per-tier template-interval dictionary (Decision 20).
2. Builds the genuine component ``p_gen`` by evaluating the shape's
   pinned generator at bin centres and renormalising to sum to 1.
3. Computes ``p_true = alpha * p_conv + (1 - alpha) * p_gen``.
4. Draws ``y ~ Multinomial(N, p_true)`` with a deterministic per-replicate
   seed and persists the result to
   ``data/synthetic-cells/<cell_id>/replicate_<r>.parquet``.

This script supports both single-replicate generation (CLI invocation,
useful for the smoke test) and a programmatic API used by the
``04-grid-runner.py`` orchestrator.

Usage (CLI for smoke test)
--------------------------
    python 01-synthetic-cell-generator.py \\
        --design-json /path/to/design.json \\
        --output-root /path/to/runs/2026-05-22-recovery-grid-validation \\
        --alpha 0.50 --shape rise_and_fall \\
        --tier-name uniform --n 2000 \\
        --replicate 0

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-22, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants pulled from design.json at runtime — kept as module-level only
# to make the per-cell API stateless.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Envelope:
    """5-year binning envelope; see design.json#envelope."""

    envelope_min_year: int
    envelope_max_year: int
    bin_width_years: int

    @property
    def bin_edges(self) -> np.ndarray:
        return np.arange(
            self.envelope_min_year,
            self.envelope_max_year + 1,
            self.bin_width_years,
            dtype=float,
        )

    @property
    def bin_centres(self) -> np.ndarray:
        edges = self.bin_edges
        return (edges[:-1] + edges[1:]) / 2.0

    @property
    def n_bins(self) -> int:
        return int(self.bin_centres.size)


def load_design(design_json_path: Path) -> dict[str, Any]:
    """Read and return the design.json document as a Python dict."""
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
# Tier basis construction (Decision 20 three-tier slab structure)
# ---------------------------------------------------------------------------
def build_tier_basis(design: dict[str, Any], env: Envelope) -> np.ndarray:
    """Build the 3 × N_BINS tier_basis matrix.

    Row k is the interval-width-normalised uniform mass over tier k's
    template intervals, summed across intervals within the tier with each
    interval's mass averaged (so each tier's basis row sums to 1.0).

    The tier order is fixed by design.json#tier_order
    (century / half_century / reign).

    Parameters
    ----------
    design : dict
        The loaded design.json document.
    env : Envelope
        Binning envelope.

    Returns
    -------
    basis : (3, N_BINS) float array, each row summing to 1.
    """
    tier_order = design["tier_order"]
    intervals_by_tier = design["template_intervals_by_tier"]
    n_bins = env.n_bins
    bin_lo = env.bin_edges[:-1]
    bin_hi = env.bin_edges[1:]

    basis = np.zeros((len(tier_order), n_bins), dtype=float)
    for k, tier_name in enumerate(tier_order):
        # Within each tier, average the contributions across the tier's
        # constituent intervals (each interval contributes a sum-to-1
        # uniform-mass vector). Equal weighting across intervals within
        # the tier is the simplest specification; the production fit
        # could instead use empirical per-interval weights, but for the
        # recovery simulation equal-weighting keeps the tier basis a
        # clean qualitative object.
        intervals = intervals_by_tier[tier_name]
        tier_sum = np.zeros(n_bins, dtype=float)
        for interval in intervals:
            lo = float(interval["lo"])
            hi = float(interval["hi"])
            # Per-bin overlap with [lo, hi].
            overlap = np.maximum(
                0.0, np.minimum(bin_hi, hi) - np.maximum(bin_lo, lo)
            )
            width = hi - lo
            if width <= 0:
                continue
            per_bin_mass = overlap / width  # uniform-over-interval density
            # Renormalise so each interval's contribution sums to 1
            # within the envelope (handles intervals that extend past
            # the envelope edges).
            s = per_bin_mass.sum()
            if s > 0:
                tier_sum += per_bin_mass / s
        # Normalise the tier's combined basis to sum to 1.
        s = tier_sum.sum()
        if s <= 0:
            raise ValueError(
                f"Tier {tier_name!r} produced an all-zero basis row; "
                "check template_intervals_by_tier in design.json."
            )
        basis[k] = tier_sum / s
    return basis


# ---------------------------------------------------------------------------
# Shape generators (p_gen library)
# ---------------------------------------------------------------------------
def build_pgen(shape_spec: dict[str, Any], env: Envelope) -> np.ndarray:
    """Build a sum-to-1 ``p_gen`` vector for one shape from the library.

    Dispatches on shape_spec["generator"] to one of the supported
    generators: ``uniform``, ``exponential``, ``gaussian``,
    ``gaussian_mixture``, ``regnal_plus_smooth``.

    Parameters
    ----------
    shape_spec : dict
        One entry from design.json#shape_library, e.g.
        ``{"name": "rise_and_fall", "generator": "gaussian",
        "parameters": {"mu_year": 150.0, "sigma_year": 60.0}}``.
    env : Envelope
        Binning envelope.

    Returns
    -------
    p_gen : (N_BINS,) float array, sums to 1.
    """
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
        # Spikes: each is a Gaussian at the named year with given sigma.
        v = np.zeros_like(centres)
        for spike in params["spikes"]:
            mu = float(spike["mu_year"])
            sigma = float(spike["sigma_year"])
            w = float(spike["weight"])
            g = np.exp(-0.5 * ((centres - mu) / sigma) ** 2)
            g = g / g.sum()  # normalise this spike to sum-to-1
            v = v + w * g
        # Smooth baseline.
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
# Cell-id and seed bookkeeping
# ---------------------------------------------------------------------------
def make_cell_id(
    shape_name: str, alpha: float, tier_name: str, n: int
) -> str:
    """Human-readable cell id used as a directory name."""
    return (
        f"shape={shape_name}_alpha={alpha:.2f}"
        f"_tier={tier_name}_N={n}"
    )


def enumerate_grid_cells(design: dict[str, Any]) -> list[dict[str, Any]]:
    """Enumerate all 450 cells in the deterministic design-pinned order.

    Order (per plan.md): shape_name (alphabetical) × alpha (ascending) ×
    tier_weights_name (alphabetical) × N (ascending).

    Returns
    -------
    cells : list of dicts, each with keys
        ``cell_index``, ``cell_id``, ``shape``, ``alpha``,
        ``tier_weights_name``, ``tier_weights``, ``n``.
    """
    shape_lib = design["shape_library"]
    alpha_grid = design["alpha_grid"]
    tier_grid = design["tier_weight_grid"]
    n_grid = design["n_grid"]

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


def make_replicate_seed(
    base_seed: int, cell_index: int, replicate: int
) -> int:
    """Deterministic per-replicate seed (plan.md §1 / §2)."""
    cell_seed = base_seed + cell_index
    return cell_seed * 1000 + replicate


# ---------------------------------------------------------------------------
# Public API: generate one replicate
# ---------------------------------------------------------------------------
def generate_replicate(
    cell: dict[str, Any],
    replicate: int,
    base_seed: int,
    env: Envelope,
    tier_basis: np.ndarray,
    output_root: Path,
) -> Path:
    """Generate one synthetic replicate and write the parquet.

    Parameters
    ----------
    cell : dict
        One entry from ``enumerate_grid_cells``.
    replicate : int
        Replicate index (0-99).
    base_seed : int
        ``design["base_seed"]``.
    env : Envelope
        Binning envelope.
    tier_basis : (3, N_BINS) float array
        Output of ``build_tier_basis(...)``.
    output_root : Path
        Validation-run root (``runs/2026-05-22-recovery-grid-validation/``);
        files go to ``output_root / data / synthetic-cells / <cell_id> /``.

    Returns
    -------
    out_path : Path to the written parquet file.
    """
    seed = make_replicate_seed(base_seed, cell["cell_index"], replicate)
    rng = np.random.default_rng(seed)

    # Build the truth.
    p_conv = cell["tier_weights"] @ tier_basis
    p_conv = p_conv / p_conv.sum()
    p_gen = build_pgen(cell["shape"], env)
    p_true = cell["alpha"] * p_conv + (1.0 - cell["alpha"]) * p_gen
    p_true = p_true / p_true.sum()

    # Draw.
    y = rng.multinomial(cell["n"], p_true).astype(np.int64)

    # Persist.
    out_dir = output_root / "data" / "synthetic-cells" / cell["cell_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"replicate_{replicate:03d}.parquet"

    df = pd.DataFrame(
        {
            "bin_index": np.arange(env.n_bins, dtype=np.int32),
            "bin_centre_year": env.bin_centres,
            "y": y,
            "p_conv_true": p_conv,
            "p_gen_true": p_gen,
            "p_true": p_true,
        }
    )
    # Attach truth metadata as a single-row table sibling — store as
    # parquet metadata via a JSON sidecar to keep the schema simple.
    df.attrs["cell_id"] = cell["cell_id"]
    df.attrs["replicate"] = int(replicate)
    df.attrs["alpha"] = float(cell["alpha"])
    df.attrs["n"] = int(cell["n"])
    df.attrs["tier_weights_name"] = cell["tier_weights_name"]
    df.attrs["tier_weights"] = cell["tier_weights"].tolist()
    df.attrs["shape_name"] = cell["shape"]["name"]
    df.attrs["seed"] = int(seed)
    df.to_parquet(out_path, index=False)

    # JSON sidecar (parquet does not natively round-trip dict attrs).
    sidecar = out_dir / f"replicate_{replicate:03d}.truth.json"
    with sidecar.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "cell_id": cell["cell_id"],
                "replicate": int(replicate),
                "alpha_true": float(cell["alpha"]),
                "n": int(cell["n"]),
                "tier_weights_name": cell["tier_weights_name"],
                "tier_weights_true": cell["tier_weights"].tolist(),
                "shape_name": cell["shape"]["name"],
                "seed": int(seed),
                "cell_index": int(cell["cell_index"]),
            },
            fh,
            indent=2,
        )
    return out_path


# ---------------------------------------------------------------------------
# CLI entrypoint (used for smoke test; the grid runner calls the API
# directly).
# ---------------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one synthetic replicate for the H2.1 grid."
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--alpha", required=True, type=float)
    parser.add_argument("--shape", required=True, type=str)
    parser.add_argument("--tier-name", required=True, type=str)
    parser.add_argument("--n", required=True, type=int)
    parser.add_argument("--replicate", required=True, type=int)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    design = load_design(args.design_json)
    env = make_envelope(design)
    tier_basis = build_tier_basis(design, env)

    # Find the matching cell entry.
    cells = enumerate_grid_cells(design)
    match = None
    for c in cells:
        if (
            abs(c["alpha"] - args.alpha) < 1e-9
            and c["shape"]["name"] == args.shape
            and c["tier_weights_name"] == args.tier_name
            and c["n"] == args.n
        ):
            match = c
            break
    if match is None:
        print(
            "ERROR: no cell matched the supplied "
            "(alpha, shape, tier-name, n) tuple; "
            "check design.json contents.",
            file=sys.stderr,
        )
        return 2
    out_path = generate_replicate(
        match, args.replicate, int(design["base_seed"]), env, tier_basis,
        args.output_root,
    )
    print(f"[01-synth] wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
