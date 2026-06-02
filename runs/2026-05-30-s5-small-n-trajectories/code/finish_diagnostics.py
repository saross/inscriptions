#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finish_diagnostics.py — complete the §5 production run's Step 3 from saved output.
=================================================================================

SUPERSEDED (2026-06-02) by ``orchestrate.py --resume-diagnostics``, which
generalises this one-off recovery into a first-class flag (and runs the same
preflight check first). This file is retained as the historical artefact that
produced the committed ``production-summary.json`` on 2026-06-01; for any future
resume, prefer ``orchestrate.py --resume-diagnostics --out-base <dir>``.

The 2026-05-31 production run completed Steps 1–2 (the four monolithic ``.nc``
posteriors + the subsample-recover grid) but crashed at Step 3
(``trajectory_clustering``) on a missing ``scikit-learn`` — an UNDECLARED
dependency (now added to ``pyproject.toml`` and installed). The expensive work
(the 5.7 h of fitting) is intact on disk; this script re-runs ONLY Step 3
against the saved outputs, so nothing is re-fitted that was already fitted.

What it does (mirrors ``orchestrate.run_production``'s Step 3 exactly):

1. Reconstructs the four monolithic fits' convergence verdicts by loading each
   saved ``.nc`` (authoritative record; one at a time to bound memory).
2. Re-reads the existing ``subsample-recover-results.json`` aggregate.
3. Runs the three Step-3 diagnostics that did not get to run:
   - ``trajectory_clustering`` (k-means; the step that crashed) on the saved
     primary (25y inscription) posterior;
   - ``anchor_internal_consistency`` (§8a.1 — re-fits the 7 anchors standalone);
   - ``pompeii_ad79_external`` (§8a.2 — re-fits Pompeii standalone).
4. Writes ``production/production-summary.json`` — the artefact the orchestrator
   would have produced had it not crashed.

The anchor / Pompeii diagnostics re-fit the anchors standalone (the anchors are
not in the monolithic target-set fit); that is ~15–25 min, cheap relative to
the run. Threading / pytensor / scratch hygiene is set below BEFORE any
numpy/pymc import (so this is safe to run directly, no env file needed).

Run (on zbook)::
    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/finish_diagnostics.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-01, on Shawn's brief.
"""

from __future__ import annotations

import os

# --- threading / pytensor / scratch hygiene (MUST precede numpy/pymc import) ---
for _v in (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "NUMBA_NUM_THREADS",
):
    os.environ.setdefault(_v, "1")
os.environ.setdefault("PYTENSOR_FLAGS", "mode=FAST_RUN,allow_gc=False")
os.environ.setdefault("TMPDIR", os.path.expanduser("~/cc-scratch/s5/pytensor-tmp"))
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import arviz as az  # noqa: E402

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import orchestrate as orch  # noqa: E402
import dataprep as dp  # noqa: E402
import hier_model  # noqa: E402
import letter_model  # noqa: E402

OUT = _HERE / "production"

# The production run's defaults (orchestrate.py argparse): used for the
# anchor / Pompeii standalone re-fits so they match the run.
DRAWS, TUNE, CHAINS, CORES, TARGET_ACCEPT, SEED = 1000, 1000, 4, 2, 0.99, 2026

# Module per unit for convergence_summary / gates_pass.
_MONO = [
    ("inscription", 25, hier_model),
    ("inscription", 50, hier_model),
    ("letter", 25, letter_model),
    ("letter", 50, letter_model),
]


def reconstruct_monolithic() -> dict:
    """Load each saved .nc and recompute its convergence verdict (authoritative)."""
    mono = {}
    for unit, bw, mod in _MONO:
        p = OUT / f"monolithic-{unit}-{bw}y.nc"
        if not p.exists():
            mono[f"{unit}-{bw}y"] = {"error": f"missing {p.name}"}
            continue
        idata = az.from_netcdf(str(p))
        conv = mod.convergence_summary(idata)
        mono[f"{unit}-{bw}y"] = {
            "conv": conv,
            "gates_pass": bool(mod.gates_pass(conv)),
            "path": str(p),
        }
        del idata  # bound memory: one 0.6–1.2 GB posterior at a time
        print(f"  {unit}-{bw}y: gates_pass={mono[f'{unit}-{bw}y']['gates_pass']} "
              f"max_rhat={conv['max_rhat']:.4f} min_ess={conv['min_ess_bulk']:.0f} "
              f"div={conv['n_divergences']}")
    return mono


def main() -> int:
    if not OUT.exists():
        print(f"FATAL: {OUT} not found", file=sys.stderr)
        return 2
    cache25 = dp.default_cache_dir(25)
    summary = {"steps": {}, "note": "Step 3 completed post-hoc by "
               "finish_diagnostics.py after the sklearn-missing crash; "
               "Steps 1–2 are the original 2026-05-31 run."}

    print("=== Step 1 (reconstructed from saved .nc) ===")
    summary["steps"]["monolithic"] = reconstruct_monolithic()

    print("=== Step 2 (existing subsample-recover results) ===")
    sub = json.loads((OUT / "subsample-recover-results.json").read_text())
    summary["steps"]["subsample_recover"] = sub["aggregate"]
    agg = sub["aggregate"]
    print(f"  calibration N* = {agg.get('calibration_n_star')}, "
          f"n_failures = {sub.get('n_failures')}")

    print("=== Step 3 (the part that crashed) ===")
    diag = {}
    primary = OUT / "monolithic-inscription-25y.nc"
    if primary.exists():
        t0 = time.time()
        diag["clustering"] = orch.trajectory_clustering(primary, "lam")
        print(f"  clustering done ({time.time() - t0:.0f}s): "
              f"sizes={diag['clustering'].get('cluster_sizes')}")
    print("  re-fitting anchors for internal consistency + Pompeii AD-79 ...")
    diag["anchor_internal_consistency"] = orch.anchor_internal_consistency(
        cache25, DRAWS, TUNE, CHAINS, CORES, TARGET_ACCEPT, SEED)
    diag["pompeii_ad79"] = orch.pompeii_ad79_external(
        cache25, DRAWS, TUNE, CHAINS, CORES, TARGET_ACCEPT, SEED)
    summary["steps"]["diagnostics"] = diag

    out_json = OUT / "production-summary.json"
    out_json.write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nProduction summary -> {out_json}")
    print("pompeii_ad79:", json.dumps(diag["pompeii_ad79"], default=float)[:500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
