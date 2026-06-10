import sys
from pathlib import Path
RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
sys.path.insert(0, str(RUN / "code"))
import grid_lib as G
import run_joint_grid as Rg
cell = {c["cell_id"]: c for c in G.enumerate_cells()}["broad_early_a0.0_broad_gen_N1500"]
N = 6
a = Rg.run_cell(cell, N)
b = Rg.run_cell(cell, N)
md = 0.0
for i in range(N):
    aj, bj = a["reps"][i]["joint"], b["reps"][i]["joint"]
    for f in ("alpha_med", "alpha_lo", "alpha_hi"):
        md = max(md, abs(aj[f] - bj[f]))
print(f"NEW-vs-NEW (identical code, identical seeds) max|Δ| = {md:.3e}")
print("=> INHERENT non-determinism (BLAS/NUTS); bit-identical was never achievable"
      if md > 1e-9 else "=> bit-reproducible; the old-vs-new delta is method-specific")
