#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_better_dated.py — Option-2 "better-dated subset" reachability probe.
==========================================================================

Tests the decisive Option-2 question (option-2-case-study-spec.md §4): is there a
width-restricted sub-corpus of Adela's datable conjugal women corpus that reaches
the **reliable de-fogging envelope** — fitted **convention fraction α ≤ 0.70 AND
N ≥ the reachability floor (≈500 easy → ≈2000 hard)**?

Motivating dry-pass finding (2026-06-21): **interval width is the WRONG axis.**
The editorial convention in this corpus lives at *round* widths (the F1_round
25-year slabs are 68 % of rows; widths 49/99/149y), so narrowing the interval does
NOT cleanly raise the genuine fraction — the ≤50y band is actually *more*
convention-aligned (0.91) than the full corpus (0.76). The genuinely-precise core
(Tight family, width ≤ 4y) is N = 6; the non-aligned "genuine class" is N = 315
(below the 500 floor). So a reachable subset is unlikely — but we confirm with
actual fitted α (the proxy aligned-fraction is not α; the deconvolution re-estimates).

Method: fit the production cc-library deconvolution (reuse ``run_refit.fit_one``,
same as the Option-1 women fits) to the datable conjugal corpus restricted to
date-range width ≤ {50, 75, 100, 150} y. Report fitted α + N + convergence; classify
each against the envelope. Fresh ``unit_index`` 211–214 (collision-free seeds).

Run (sapphire)::

    cd ~/Code/inscriptions
    PATH=~/.local/bin:$PATH TMPDIR=$HOME/cc-scratch/tmp PYTENSOR_FLAGS=mode=FAST_RUN \
        taskset -c 0-11 uv run python \
        runs/2026-06-20-women-corpus-feasibility/code/probe_better_dated.py

Collaboration data (Adela, Aarhus) — feasibility/case-study only; NO crossover-age
trajectory. Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path("/home/shawn/Code/inscriptions")
WCODE = ROOT / "runs/2026-06-20-women-corpus-feasibility/code"
for p in (ROOT / "runs/2026-06-13-cc-production-refit/code",
          ROOT / "runs/2026-06-07-h2.1-launch-prep/code",
          ROOT / "runs/2026-06-09-joint-identifiability/code",
          ROOT / "runs/2026-06-06-convention-basis-redesign/revalidation/code",
          WCODE):
    sys.path.insert(0, str(p))

import refit_lib as R          # noqa: E402
import run_refit as RF         # noqa: E402
import run_women_feasibility as W  # noqa: E402  (load_women)

OUT = ROOT / "runs/2026-06-20-women-corpus-feasibility/outputs"
UNITS_DIR = OUT / "units"
DRAWS_DIR = OUT / "posterior-draws"
WIDTH_THRESHOLDS = [50, 75, 100, 150]
ENVELOPE_ALPHA = 0.70
FLOOR_EASY, FLOOR_HARD = 500, 2000


def alpha_floor(alpha: float) -> int:
    """Graded reachability floor as a function of α, faithful to the reachability
    grid (F12 / runs/2026-06-03-small-n-reachability): low-α subsets are reachable
    from ~500, the floor rising to ~2000 as α approaches the 0.70 envelope."""
    if alpha <= 0.30:
        return 500
    if alpha <= 0.50:
        return 1000
    return 2000  # 0.50 < α ≤ 0.70 (marginal even at 2000)


def reachable(alpha: float, n: int) -> str:
    """Classify a subset against the reachability envelope (α + the graded N floor)."""
    if alpha > ENVELOPE_ALPHA:
        return f"NO (α {alpha:.2f} > {ENVELOPE_ALPHA} envelope)"
    floor = alpha_floor(alpha)
    if n >= floor:
        return f"YES (α {alpha:.2f} ≤ {ENVELOPE_ALPHA} and N {n} ≥ floor {floor})"
    return f"NO (α {alpha:.2f} ok but N {n} < floor {floor})"


def main() -> int:
    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    DRAWS_DIR.mkdir(parents=True, exist_ok=True)
    d_all = W.load_women()
    width = (d_all["na"] - d_all["nb"]).to_numpy()

    rows = []
    for i, thr in enumerate(WIDTH_THRESHOLDS):
        sub = d_all[width <= thr]
        name = f"women-width-le-{thr}"
        unit = {"name": name, "kind": "aggregate", "frame": "latin",
                "tier": "probe", "unit_index": 211 + i}
        data = R.build_unit_cc_data(sub)
        t0 = time.perf_counter()
        out = RF.fit_one(unit, data, emit_draws_dir=str(DRAWS_DIR))
        out["wall_s"] = time.perf_counter() - t0
        out["width_threshold"] = thr
        out["n_rows_raw"] = int(len(sub))
        out["n_daughters"] = int((sub["role"] == "daughter").sum())
        out["mass_aligned_frac"] = data["mass_aligned_frac"]
        (UNITS_DIR / f"{RF._safe(name)}.json").write_text(json.dumps(out, indent=2, default=float))
        verdict = reachable(out["alpha_median"], out["n_rows_raw"])
        rows.append({"threshold": thr, "name": name, "n": out["n_rows_raw"],
                     "n_daughters": out["n_daughters"], "alpha": out["alpha_median"],
                     "alpha_ci": [out["alpha_ci_lo"], out["alpha_ci_hi"]],
                     "max_rhat": out["max_rhat"], "min_ess_bulk": out["min_ess_bulk"],
                     "n_div": out["n_divergences"], "reachable": verdict})
        print(f"  width≤{thr:>3}y  N={out['n_rows_raw']:>4}  α={out['alpha_median']:.3f} "
              f"[{out['alpha_ci_lo']:.3f},{out['alpha_ci_hi']:.3f}]  "
              f"R̂={out['max_rhat']:.4f} ESS={out['min_ess_bulk']:.0f} div={out['n_divergences']} "
              f"→ {verdict}  ({out['wall_s']:.0f}s)")

    summary = {
        "probe": "Option-2 better-dated-subset reachability",
        "envelope": {"alpha_max": ENVELOPE_ALPHA, "floor_easy": FLOOR_EASY,
                     "floor_hard": FLOOR_HARD},
        "context": {
            "full_datable_conjugal_N": int(len(d_all)),
            "genuine_core_tight_width_le_4_N": 6,
            "non_aligned_genuine_class_N": 315,
            "f1_round_share": "68% of rows (convention is structural at round widths)"},
        "results": rows,
        "verdict": ("reachable subset found" if any("YES" in r["reachable"] for r in rows)
                    else "NO width-restricted subset reaches the envelope"),
    }
    (OUT / "better-dated-probe-summary.json").write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nVERDICT: {summary['verdict']}")
    print(f"Summary -> {OUT / 'better-dated-probe-summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
