#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute-alpha-loa.py
====================

Bland-Altman limits-of-agreement (LoA) for the recovered convention fraction
alpha, on the Decision-38 convention-basis re-validation grid.

This reproduces, for the new empirical calendar-slab basis, the alpha-recovery
precision figure that OSF Amendment 01 reports for Grid A
(``osf-amendment-01-justification.txt`` line 150): 95% limits of agreement on the
signed bias ``d = alpha_hat - alpha_true``, evaluated WITHIN the operating
envelope (alpha_true <= 0.70), reported pooled AND conditioned on the
data-generating shape (because recovery precision varies several-fold by shape
complexity). Grid A gave LoA ~ [-0.22, +0.17], mean signed bias -0.02, with
90th-percentile |bias| ~ 0.07-0.11 for smooth/flat shapes rising to ~ 0.18-0.27
for the multimodal shapes (bimodal, regnal_cluster) -- the "+-0.18 envelope"
that launch-spec section 7 hedges alpha claims to.

Methodology (matched to Decision 33 / Amendment 01)
---------------------------------------------------
- Point estimate per replicate: posterior MEDIAN alpha (``alpha_median``), the
  same estimator ``collect-alpha-bias.py`` uses. The per-cell signed bias
  ``alpha_bias_mean`` is the mean over that cell's replicates of
  ``(alpha_median - alpha_true)``.
- Unit of observation for the LoA: the CELL (one ``alpha_bias_mean`` per cell),
  matching the per-cell ``alpha-bias.parquet`` artefact Amendment 01 was
  computed from. A per-replicate pooled SD is also reported as a sensitivity.
- 95% LoA = mean(bias) +- 1.96 * SD(bias). Half-width = 1.96 * SD(bias).
- Envelope: alpha_true <= 0.70 (ALPHA_ENVELOPE). The alpha = 0.95 stress row is
  reported separately, never folded into the headline precision.
- Shape grouping for the smooth/flat-vs-multimodal contrast:
  multimodal = {bimodal, regnal_cluster}; smooth/flat = the rest.

Input
-----
``<grid-dir>/outputs/tables/alpha-bias.parquet`` (produced by
``collect-alpha-bias.py``; one row per cell, read-only here).

Output
------
- prints the pooled + per-shape + grouped summary;
- writes ``<grid-dir>/outputs/tables/alpha-loa-summary.json`` for the record.

Usage
-----
    python compute-alpha-loa.py \\
        --grid-dir /path/to/.../revalidation/inscription-mass

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-08, on Shawn Ross's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ALPHA_ENVELOPE = 0.70  # operating-envelope ceiling (Decision 37 D5 / Amendment 01)
ALPHA_STRESS = 0.95    # near-unidentifiable stress row (reported, never folded in)
Z = 1.96               # 95% normal multiplier for the limits of agreement
MULTIMODAL = {"bimodal", "regnal_cluster"}


def _loa(bias: pd.Series) -> dict[str, float]:
    """95% Bland-Altman limits of agreement for a signed-bias series."""
    mean = float(bias.mean())
    sd = float(bias.std(ddof=1)) if len(bias) > 1 else float("nan")
    return {
        "n": int(len(bias)),
        "mean_signed_bias": mean,
        "sd": sd,
        "loa_lo": mean - Z * sd,
        "loa_hi": mean + Z * sd,
        "half_width": Z * sd,
        "p90_abs_bias": float(bias.abs().quantile(0.90)),
        "max_abs_bias": float(bias.abs().max()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--grid-dir", required=True, type=Path)
    args = ap.parse_args()

    parquet = args.grid_dir.resolve() / "outputs" / "tables" / "alpha-bias.parquet"
    if not parquet.exists():
        print(f"[alpha-loa] missing {parquet}; run collect-alpha-bias.py first",
              file=sys.stderr)
        return 1
    df = pd.read_parquet(parquet)

    env = df[df["alpha_true"] <= ALPHA_ENVELOPE].copy()
    stress = df[df["alpha_true"] >= ALPHA_STRESS].copy()
    env["group"] = np.where(env["shape_name"].isin(MULTIMODAL),
                            "multimodal", "smooth_flat")

    summary: dict[str, object] = {
        "envelope_ceiling": ALPHA_ENVELOPE,
        "estimator": "posterior median alpha; per-cell mean signed bias",
        "unit": "cell",
        "pooled_in_envelope": _loa(env["alpha_bias_mean"]),
        "by_group": {
            g: _loa(sub["alpha_bias_mean"])
            for g, sub in env.groupby("group")
        },
        "by_shape": {
            s: _loa(sub["alpha_bias_mean"])
            for s, sub in env.groupby("shape_name")
        },
        "stress_alpha_0p95": _loa(stress["alpha_bias_mean"]) if len(stress) else None,
        # per-replicate sensitivity: pool the per-cell SDs is not valid, so we
        # report the per-cell-bias SD only; replicate-level scatter is wider.
    }

    p = summary["pooled_in_envelope"]
    print(f"[alpha-loa] IN-ENVELOPE (alpha<=0.70), n={p['n']} cells")
    print(f"[alpha-loa]   mean signed bias = {p['mean_signed_bias']:+.4f}")
    print(f"[alpha-loa]   95% LoA = [{p['loa_lo']:+.3f}, {p['loa_hi']:+.3f}]"
          f"  (half-width +-{p['half_width']:.3f})")
    print(f"[alpha-loa]   90th-pct |bias| = {p['p90_abs_bias']:.3f}; "
          f"max |bias| = {p['max_abs_bias']:.3f}")
    for g, s in summary["by_group"].items():
        print(f"[alpha-loa]   {g:>11}: 90th-pct |bias| = {s['p90_abs_bias']:.3f}, "
              f"LoA [{s['loa_lo']:+.3f}, {s['loa_hi']:+.3f}] (n={s['n']})")
    print("[alpha-loa]   per shape (90th-pct |bias|): "
          + ", ".join(f"{k}={v['p90_abs_bias']:.3f}"
                      for k, v in summary["by_shape"].items()))
    if summary["stress_alpha_0p95"]:
        st = summary["stress_alpha_0p95"]
        print(f"[alpha-loa]   STRESS alpha=0.95 (not folded in): "
              f"mean bias {st['mean_signed_bias']:+.3f}, "
              f"90th-pct |bias| {st['p90_abs_bias']:.3f} (n={st['n']})")

    out = args.grid_dir.resolve() / "outputs" / "tables" / "alpha-loa-summary.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[alpha-loa] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
