#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synth.py
========

Synthetic-data generation for the 2026-05-26 two-unit recovery-grid
re-simulation. For one cell + one replicate, build the truth (p_conv,
p_gen, p_true), draw a multinomial sample, and — under ``--unit letter``
— additionally draw iid letter-counts from the empirical LIRE
distribution and aggregate per-bin letter-mass.

Persisted artefacts per replicate
---------------------------------
- ``data/synthetic-cells/<cell_id>/replicate_<r>.parquet`` — per-bin
  table with columns:
    * ``bin_index``        : int32
    * ``bin_centre_year``  : float64
    * ``y``                : int64
        Under ``inscription``: multinomial count per bin (raw).
        Under ``letter``    : sum of letter-counts per bin (letter mass).
    * ``y_inscription``    : int64
        The raw multinomial count per bin. For Grid A this equals ``y``;
        for Grid B it is retained so the bin-count-sanity gate can
        compare letter-mass vs inscription-mass on the **same** mixture
        draw.
    * ``p_conv_true``      : float64
    * ``p_gen_true``       : float64
    * ``p_true``           : float64
- ``data/synthetic-cells/<cell_id>/replicate_<r>.truth.json`` — sidecar
  with the cell-level scalars + the data seed + letter-weight seed.

Spec lineage
------------
- §3.2 — under inscription each row deposits weight = 1.0; under letter
  each row deposits an iid empirical letter-count weight.
- §3.4 — letter-counts uncapped (Decision 2).
- §3.5 — seed policy: data seed = (base_seed + cell_index) * 1000 + r;
  letter-weight seed = data seed + 999_000_000.

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from cell_lib import (
    Envelope,
    build_pgen,
    make_data_seed,
    make_letter_weight_seed,
    sample_letter_counts,
)


def generate_replicate(
    cell: dict[str, Any],
    replicate: int,
    base_seed: int,
    env: Envelope,
    tier_basis: np.ndarray,
    output_root: Path,
    unit: str,
    letter_dist: np.ndarray | None = None,
) -> Path:
    """Generate one synthetic replicate under the requested unit.

    Parameters
    ----------
    cell : dict
        One entry from ``cell_lib.enumerate_grid_cells``.
    replicate : int
        Replicate index 0..(replicates_per_cell - 1).
    base_seed : int
        Grid-specific base seed (20260526 for inscription, 20260527 for
        letter; see spec §3.5).
    env : Envelope
        5-year binning envelope.
    tier_basis : (3, N_BINS) float array
    output_root : Path
        Per-grid output root (e.g.
        ``runs/2026-05-26-recovery-grid-two-unit/inscription-mass/``).
    unit : {"inscription", "letter"}
        Selects the data-generation rule (spec §3.2).
    letter_dist : (M,) int64 array, optional
        Empirical letter-count support. Required under ``unit="letter"``.

    Returns
    -------
    out_path : Path to the written parquet file.
    """
    if unit not in {"inscription", "letter"}:
        raise ValueError(f"unit must be 'inscription' or 'letter', got {unit!r}")
    if unit == "letter" and letter_dist is None:
        raise ValueError(
            "letter_dist must be supplied when unit='letter'."
        )

    data_seed = make_data_seed(base_seed, cell["cell_index"], replicate)
    rng_data = np.random.default_rng(data_seed)

    # Truth.
    p_conv = cell["tier_weights"] @ tier_basis
    p_conv = p_conv / p_conv.sum()
    p_gen = build_pgen(cell["shape"], env)
    p_true = cell["alpha"] * p_conv + (1.0 - cell["alpha"]) * p_gen
    p_true = p_true / p_true.sum()

    # Raw multinomial draw (always present; under letter we re-use this
    # vector as ``y_inscription`` for the bin-count sanity gate).
    y_inscription = rng_data.multinomial(cell["n"], p_true).astype(np.int64)

    if unit == "inscription":
        y = y_inscription.copy()
        letter_weight_seed = None
    else:
        # Letter-mass aggregation: each of the cell["n"] inscriptions
        # carries an iid letter-count drawn from letter_dist. We need a
        # bin assignment for each of the cell["n"] inscriptions so we
        # can sum their letter-counts per bin.
        #
        # Implementation: draw cell["n"] iid bin assignments from
        # Categorical(p_true) — equivalent to the multinomial draw above
        # at the individual-inscription level — and then sum the
        # letter-counts within each bin. This uses a separate rng
        # branched off the multinomial-draw seed so that streams don't
        # collide and so that the **same mixture** drives both the
        # y_inscription vector (already drawn) and the letter-mass
        # accumulation.
        #
        # NOTE: we draw bin assignments here via a fresh choice() call
        # on the data_seed rng. This re-draws from p_true and is NOT
        # bit-identical to the y_inscription multinomial. y_inscription
        # remains the canonical inscription-mass record (for the gate
        # comparison and as a per-replicate sanity reference), but the
        # letter-mass accumulation uses an independent inscription-level
        # assignment so that letter-counts ride the same mixture without
        # being constrained by the prior multinomial outcome.
        n_bins = env.n_bins
        bin_assignments = rng_data.choice(n_bins, size=cell["n"], p=p_true)
        letter_weight_seed = make_letter_weight_seed(
            base_seed, cell["cell_index"], replicate
        )
        rng_letters = np.random.default_rng(letter_weight_seed)
        letter_counts_per_inscription = sample_letter_counts(
            cell["n"], letter_dist, rng_letters
        )
        # Aggregate letter mass per bin.
        y = np.zeros(n_bins, dtype=np.int64)
        np.add.at(y, bin_assignments, letter_counts_per_inscription.astype(np.int64))

    # Persist.
    out_dir = output_root / "data" / "synthetic-cells" / cell["cell_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"replicate_{replicate:03d}.parquet"

    df = pd.DataFrame(
        {
            "bin_index": np.arange(env.n_bins, dtype=np.int32),
            "bin_centre_year": env.bin_centres,
            "y": y,
            "y_inscription": y_inscription,
            "p_conv_true": p_conv,
            "p_gen_true": p_gen,
            "p_true": p_true,
        }
    )
    df.to_parquet(out_path, index=False)

    # JSON sidecar (truth metadata + seeds).
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
                "unit": unit,
                "data_seed": int(data_seed),
                "letter_weight_seed": (
                    int(letter_weight_seed)
                    if letter_weight_seed is not None
                    else None
                ),
                "cell_index": int(cell["cell_index"]),
            },
            fh,
            indent=2,
        )
    return out_path
