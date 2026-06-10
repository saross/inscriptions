#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate 1 — bit-identical validation of the set_data refactor.

Recompute the first N_VAL replicates of selected ALREADY-DONE cells with the NEW
(build-once + set_data) code and compare each replicate's joint alpha median/CI and
convergence flag to the stored (old build-fresh-per-rep) JSON. Writes nothing to
outputs/grid (run_cell is called directly, not the disk-writing _worker).

Bit-identical  => OVERALL max |Δ| ~ 0 and zero convergence-flag mismatches.

Usage:  uv run python validate_setdata.py [N_VAL] [cell_id,cell_id,...]
        (no cell_ids => auto-pick 2 done identifiable N=1500 cells)
"""
import json
import sys
import time
from pathlib import Path

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
sys.path.insert(0, str(RUN / "code"))
import grid_lib as G          # noqa: E402
import run_joint_grid as Rg   # noqa: E402  (imports run_cell + new fit_joint_on_model)

GRID = RUN / "outputs" / "grid"
N_VAL = int(sys.argv[1]) if len(sys.argv) > 1 else 12
explicit = sys.argv[2].split(",") if len(sys.argv) > 2 else None

cells = {c["cell_id"]: c for c in G.enumerate_cells()}
done = {p.stem for p in GRID.glob("*.json")}

if explicit:
    targets = [c for c in explicit if c in done]
else:
    targets = [cid for cid, c in cells.items()
               if cid in done and c["regime"] == "identifiable" and c["N"] == 1500][:2]

print(f"validating {len(targets)} cells at {N_VAL} reps: {targets}", flush=True)
overall_max = 0.0
overall_conv_mm = 0
for cid in targets:
    stored = json.loads((GRID / f"{cid}.json").read_text())
    t0 = time.time()
    new = Rg.run_cell(cells[cid], N_VAL)
    md = {"alpha_med": 0.0, "alpha_lo": 0.0, "alpha_hi": 0.0}
    conv_mm = 0
    missing = 0
    for i in range(N_VAL):
        oj = stored["reps"][i].get("joint")
        nj = new["reps"][i].get("joint")
        if oj is None or nj is None:
            missing += 1
            continue
        for f in md:
            md[f] = max(md[f], abs(oj[f] - nj[f]))
        conv_mm += int(oj["converged"] != nj["converged"])
    overall_max = max(overall_max, md["alpha_med"], md["alpha_lo"], md["alpha_hi"])
    overall_conv_mm += conv_mm
    print(f"  {cid} ({cells[cid]['regime']}, N={cells[cid]['N']}): "
          f"max|Δ| med={md['alpha_med']:.2e} lo={md['alpha_lo']:.2e} hi={md['alpha_hi']:.2e} "
          f"conv_mismatch={conv_mm} missing={missing}  ({time.time()-t0:.0f}s)", flush=True)

print(f"OVERALL max |Δ| across α median/CI = {overall_max:.3e}; conv-flag mismatches = {overall_conv_mm}")
verdict = ("BIT-IDENTICAL (PASS)" if overall_max < 1e-9 and overall_conv_mm == 0
           else "NEGLIGIBLE <1e-6 (PASS-with-note)" if overall_max < 1e-6 and overall_conv_mm == 0
           else "DIFFERENT — INVESTIGATE")
print("VERDICT:", verdict)
