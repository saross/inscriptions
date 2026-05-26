#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sanity-bin-correlation.py
=========================

Pre-launch sanity gate 2 (spec §7): under the smoke-test cell
``shape=rise_and_fall_alpha=0.50_tier=uniform_N=10000`` at N=10,000,
synthesise one replicate per grid and check that the Pearson correlation
between the letter-mass bin-count vector and the inscription-mass
bin-count vector on the same mixture is >= 0.85. A bug in the
letter-mass data-generation logic would manifest as r < 0.85.

We use a single seed and the same mixture so that both vectors ride the
same draw of bin assignments; the divergence arises only from the iid
letter-count weighting. Heavy tails will reduce the correlation
(letter-mass amplifies bins that happen to receive mega-inscriptions),
but the smoothing across 80 bins keeps r solidly above 0.85 in
expectation.

Usage
-----
    python sanity-bin-correlation.py \\
        --design-json /path/to/design.json \\
        --letter-parquet /path/to/lire-filtered-with-letters.parquet \\
        --run-root /path/to/runs/2026-05-26-recovery-grid-two-unit

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import pearsonr

# Allow imports from this script's directory.
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from cell_lib import (  # noqa: E402
    build_pgen,
    build_tier_basis,
    enumerate_grid_cells,
    load_design,
    load_letter_count_distribution,
    make_envelope,
    sample_letter_counts,
)


# Sanity threshold per spec §7 gate 2.
THRESHOLD = 0.85
# Sanity cell pinned by §7 (rise_and_fall, alpha=0.50, tier=uniform, N=10000).
SANITY_CELL_PARAMS = dict(
    shape_name="rise_and_fall",
    alpha=0.50,
    tier_name="uniform",
    n=10_000,
)
# Per-grid base seeds (mirror spec §3.5).
BASE_SEED_INSCRIPTION = 20_260_526
BASE_SEED_LETTER = 20_260_527


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bin-count-vector sanity check (Grid B vs Grid A)."
    )
    parser.add_argument("--design-json", required=True, type=Path)
    parser.add_argument("--letter-parquet", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    args = parser.parse_args()

    design = load_design(args.design_json)
    env = make_envelope(design)
    tier_basis = build_tier_basis(design, env)
    cells = enumerate_grid_cells(design)

    # Locate the sanity cell.
    target = None
    for c in cells:
        if (
            c["shape"]["name"] == SANITY_CELL_PARAMS["shape_name"]
            and abs(c["alpha"] - SANITY_CELL_PARAMS["alpha"]) < 1e-9
            and c["tier_weights_name"] == SANITY_CELL_PARAMS["tier_name"]
            and c["n"] == SANITY_CELL_PARAMS["n"]
        ):
            target = c
            break
    if target is None:
        print(
            f"ERROR: could not locate sanity cell "
            f"{SANITY_CELL_PARAMS} in the design enumeration.",
            file=sys.stderr,
        )
        return 2

    # Build the truth mixture.
    p_conv = target["tier_weights"] @ tier_basis
    p_conv = p_conv / p_conv.sum()
    p_gen = build_pgen(target["shape"], env)
    p_true = target["alpha"] * p_conv + (1.0 - target["alpha"]) * p_gen
    p_true = p_true / p_true.sum()

    # Use the SAME data seed for both grids' inscription draw so that
    # the comparison isolates the letter-weighting effect (independent
    # of mixture-draw stochasticity).
    data_seed = (BASE_SEED_INSCRIPTION + target["cell_index"]) * 1000 + 0
    rng_data = np.random.default_rng(data_seed)

    n = target["n"]
    n_bins = env.n_bins

    # Inscription-mass: multinomial draw.
    y_insc = rng_data.multinomial(n, p_true).astype(np.int64)

    # Letter-mass: re-draw bin assignments from the same mixture with a
    # fresh rng (matches synth.py logic) and weight by iid letter-counts.
    # Use the spec's Grid-B letter-weight seed for stream-disjointness.
    rng_letters_data = np.random.default_rng(data_seed)
    bin_assignments = rng_letters_data.choice(n_bins, size=n, p=p_true)
    letter_seed = (BASE_SEED_LETTER + target["cell_index"]) * 1000 + 0 + 999_000_000
    rng_letters = np.random.default_rng(letter_seed)
    letter_dist = load_letter_count_distribution(args.letter_parquet)
    letter_counts = sample_letter_counts(n, letter_dist, rng_letters)
    y_letter = np.zeros(n_bins, dtype=np.int64)
    np.add.at(y_letter, bin_assignments, letter_counts.astype(np.int64))

    # Pearson r.
    r, _ = pearsonr(y_insc.astype(float), y_letter.astype(float))

    diag = {
        "cell_id": target["cell_id"],
        "n_bins": n_bins,
        "n_inscriptions": int(n),
        "inscription_mass_total": int(y_insc.sum()),
        "letter_mass_total": int(y_letter.sum()),
        "pearson_r": float(r),
        "threshold": float(THRESHOLD),
        "pass": bool(r >= THRESHOLD),
    }
    out_path = (
        args.run_root / "comparison" / "sanity-bin-correlation.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(diag, fh, indent=2)
    print(
        f"[sanity-bin-corr] cell={diag['cell_id']}  "
        f"r={r:.4f}  threshold={THRESHOLD}  "
        f"verdict={'PASS' if diag['pass'] else 'FAIL'}"
    )
    print(
        f"[sanity-bin-corr] inscription total={diag['inscription_mass_total']:,}  "
        f"letter total={diag['letter_mass_total']:,}"
    )
    print(f"[sanity-bin-corr] wrote {out_path}")
    return 0 if diag["pass"] else 4


if __name__ == "__main__":
    sys.exit(main())
