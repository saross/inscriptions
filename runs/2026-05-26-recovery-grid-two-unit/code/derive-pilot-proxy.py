#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derive-pilot-proxy.py
=====================

Re-derive the ``pilot_proxy`` tier-vector for **both** grids by
reweighting the Decision-17 endpoint-frequency descriptive evidence:

- Tier-1 (century) signal: ``not_before % 100 == 1`` OR
  ``not_after % 100 == 0`` (the empirical 54.5 % / 53.0 % rounding
  endpoints in spec §2.3 line 114).
- Tier-2 (half-century) signal: not classified to century AND
  (``not_before % 100 == 51`` OR ``not_after % 100 == 50``) — the
  half-century rounding endpoints (101-150 -> mod 51; 51-100 -> mod 50;
  151-200 -> mod 50; etc.).
- Tier-3 (reign) signal: everything else.

For each grid we compute weighted proportions across the LIRE
filtered-with-letters corpus:

- inscription-mass: each row contributes weight = 1.0 (uniform).
- letter-mass conservative: each row contributes weight =
  ``letter_count_conservative``.

The two output vectors are written to::

    inscription-mass/data/pilot-proxy.json
    letter-mass/data/pilot-proxy.json

Critical-friend caveats
-----------------------
- The 2026-05-22 spec encodes the **inscription** pilot_proxy as
  (0.55, 0.30, 0.15) — a hand-picked round-number proxy anchored on the
  endpoint-frequency descriptive, not a direct re-derivation. Per the
  two-unit spec §3.3, the inscription value is hard-pinned to that
  2026-05-22 value (for design-symmetry with the predecessor run), and
  this script's inscription-mass output is recorded **alongside** but
  not substituted into the inscription grid; the letter-mass output
  IS used by Grid B. We retain the inscription re-derivation for
  reporting transparency.
- Endpoint classification is a heuristic, not a pilot posterior. The
  derived proxy is treated as descriptive-frequency evidence per
  the §3.3 "flagged caveat" carried from 2026-05-22.

Usage
-----
    python derive-pilot-proxy.py \\
        --letter-parquet /path/to/lire-filtered-with-letters.parquet \\
        --run-root /path/to/runs/2026-05-26-recovery-grid-two-unit

Author / Date
-------------
Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def classify_tier(not_before: np.ndarray, not_after: np.ndarray) -> np.ndarray:
    """Endpoint-pattern tier classifier.

    Returns
    -------
    tier : (N,) int8 array with values in {0, 1, 2} for
        (century, half_century, reign).
    """
    nb_mod = np.mod(not_before, 100)
    na_mod = np.mod(not_after, 100)

    century_mask = (nb_mod == 1) | (na_mod == 0)
    half_century_mask = (~century_mask) & ((nb_mod == 51) | (na_mod == 50))

    tier = np.full(not_before.shape, fill_value=2, dtype=np.int8)  # reign default
    tier[half_century_mask] = 1
    tier[century_mask] = 0
    return tier


def compute_pilot_proxy(
    tier_assignments: np.ndarray, weights: np.ndarray
) -> tuple[float, float, float]:
    """Weighted proportions across the three tiers; returns a length-3
    tuple summing to 1.0 (modulo float arithmetic)."""
    total = float(weights.sum())
    if total <= 0:
        raise ValueError("Zero total weight; cannot normalise.")
    p_century = float(weights[tier_assignments == 0].sum()) / total
    p_half = float(weights[tier_assignments == 1].sum()) / total
    p_reign = float(weights[tier_assignments == 2].sum()) / total
    # Re-normalise tightly to enforce sum-to-1.
    s = p_century + p_half + p_reign
    return (p_century / s, p_half / s, p_reign / s)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Re-derive pilot_proxy tier vector for both grids."
    )
    parser.add_argument("--letter-parquet", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    args = parser.parse_args()

    df = pd.read_parquet(
        args.letter_parquet,
        columns=["not_before", "not_after", "letter_count_conservative"],
    )
    not_before = df["not_before"].to_numpy(dtype=np.int64)
    not_after = df["not_after"].to_numpy(dtype=np.int64)
    letter_counts = df["letter_count_conservative"].to_numpy(dtype=np.int64)

    tiers = classify_tier(not_before, not_after)

    # Inscription-mass proxy (re-derived; **not** substituted into the
    # inscription grid — spec §3.3 hard-pins it to (0.55, 0.30, 0.15)).
    insc_weights = np.ones_like(letter_counts, dtype=np.float64)
    insc_proxy = compute_pilot_proxy(tiers, insc_weights)
    # Letter-mass proxy (the canonical pre-launch derivation).
    letter_proxy = compute_pilot_proxy(tiers, letter_counts.astype(np.float64))

    # Diagnostic descriptors.
    n_rows = int(df.shape[0])
    n_century = int((tiers == 0).sum())
    n_half = int((tiers == 1).sum())
    n_reign = int((tiers == 2).sum())
    letter_sum_century = int(letter_counts[tiers == 0].sum())
    letter_sum_half = int(letter_counts[tiers == 1].sum())
    letter_sum_reign = int(letter_counts[tiers == 2].sum())

    # Validate.
    for name, proxy in [("inscription", insc_proxy), ("letter", letter_proxy)]:
        if not (0.999 <= sum(proxy) <= 1.001):
            raise ValueError(
                f"{name} proxy does not sum to 1: {proxy} (sum={sum(proxy)})"
            )
        for k, v in enumerate(proxy):
            if not (0.0 <= v <= 1.0):
                raise ValueError(
                    f"{name} proxy entry {k} out of [0, 1]: {v}"
                )

    # Inscription-mass: write the **hard-pinned** 2026-05-22 vector
    # (0.55, 0.30, 0.15) — not the re-derived insc_proxy — into the
    # inscription-mass data/. Record insc_proxy as a diagnostic
    # alongside.
    inscription_pinned = (0.55, 0.30, 0.15)
    inscription_dir = args.run_root / "inscription-mass" / "data"
    inscription_dir.mkdir(parents=True, exist_ok=True)
    inscription_path = inscription_dir / "pilot-proxy.json"
    with inscription_path.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "unit": "inscription",
                "weights": list(inscription_pinned),
                "tier_order": ["century", "half_century", "reign"],
                "anchor": (
                    "2026-05-22 design.json hard-pinned value. "
                    "Endpoint-frequency descriptive evidence "
                    "(Decision 17 lines 1314-1316)."
                ),
                "rederivation_diagnostic": {
                    "method": (
                        "endpoint-pattern classifier; tier=0 if "
                        "not_before%100==1 or not_after%100==0; tier=1 "
                        "elif not_before%100==51 or not_after%100==50; "
                        "else tier=2."
                    ),
                    "n_rows": n_rows,
                    "n_century": n_century,
                    "n_half_century": n_half,
                    "n_reign": n_reign,
                    "uniform_weighted_proxy": list(insc_proxy),
                    "note": (
                        "uniform_weighted_proxy is the descriptive "
                        "re-derivation; the inscription grid uses the "
                        "hard-pinned (0.55, 0.30, 0.15) per spec §3.3."
                    ),
                },
            },
            fh,
            indent=2,
        )

    # Letter-mass: write the re-derived weighted proxy as the grid's
    # operational pilot_proxy.
    letter_dir = args.run_root / "letter-mass" / "data"
    letter_dir.mkdir(parents=True, exist_ok=True)
    letter_path = letter_dir / "pilot-proxy.json"
    with letter_path.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "unit": "letter",
                "weights": list(letter_proxy),
                "tier_order": ["century", "half_century", "reign"],
                "anchor": (
                    "Re-derived 2026-05-26: endpoint-pattern tier "
                    "classifier weighted by letter_count_conservative "
                    "across the 180,609-row LIRE filter."
                ),
                "rederivation_diagnostic": {
                    "method": (
                        "endpoint-pattern classifier; tier=0 if "
                        "not_before%100==1 or not_after%100==0; tier=1 "
                        "elif not_before%100==51 or not_after%100==50; "
                        "else tier=2."
                    ),
                    "n_rows": n_rows,
                    "n_century": n_century,
                    "n_half_century": n_half,
                    "n_reign": n_reign,
                    "letter_sum_century": letter_sum_century,
                    "letter_sum_half_century": letter_sum_half,
                    "letter_sum_reign": letter_sum_reign,
                    "uniform_weighted_proxy": list(insc_proxy),
                    "letter_weighted_proxy": list(letter_proxy),
                },
            },
            fh,
            indent=2,
        )

    print(
        f"[pilot-proxy] inscription (hard-pinned): "
        f"{inscription_pinned}  -> {inscription_path}"
    )
    print(
        f"[pilot-proxy] inscription (re-derived diagnostic): "
        f"({insc_proxy[0]:.4f}, {insc_proxy[1]:.4f}, {insc_proxy[2]:.4f})"
    )
    print(
        f"[pilot-proxy] letter (operational): "
        f"({letter_proxy[0]:.4f}, {letter_proxy[1]:.4f}, "
        f"{letter_proxy[2]:.4f})  -> {letter_path}"
    )
    print(
        f"[pilot-proxy] tier counts: century={n_century:,}  "
        f"half_century={n_half:,}  reign={n_reign:,}  "
        f"(total={n_rows:,})"
    )
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
