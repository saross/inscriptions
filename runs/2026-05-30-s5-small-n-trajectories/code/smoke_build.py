#!/usr/bin/env python3
"""Quick model-build smoke: compile + short sample on a tiny synthetic city."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model as m  # noqa: E402

rng = np.random.default_rng(0)
# 40 inscriptions, each a few-bin interval, on the 16-bin grid.
N, T = 40, 16
A = np.zeros((N, T))
for i in range(N):
    start = rng.integers(0, T - 3)
    width = rng.integers(1, 4)
    A[i, start:start + width] = 1.0  # full-bin coverage over a few bins
print("A shape", A.shape, "row-mass min", A.sum(1).min())

idata = m.fit(A, draws=200, tune=200, chains=2, random_seed=1, progressbar=False)
conv = m.convergence_summary(idata)
print("CONV:", conv)
print("lam posterior-median:",
      np.round(idata.posterior["lam"].median(("chain", "draw")).values, 3))
print("SMOKE-BUILD OK")
