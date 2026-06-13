#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
library_design.py — design + validate the FIXED production slab library.
=========================================================================

The recovery grid validated a FIXED, a-priori, deterministic-box slab library
(`grid_lib.slab_library_basis`, 19 rows). The empirical measurement
(`measure_units.py`) showed (a) that specific 19-row library covers only ~62 % of
the real corpus's common aligned slabs, and (b) real units have 33–362 distinct
aligned interval types — far too many to use per-unit as Dirichlet rows.

Decision (signoff §2 "optionally plus corpus-wide common slabs", taken to its
clean limit): use a **FIXED corpus-wide round-endpoint slab library, identical for
every unit** — the direct production analogue of the validated fixed library,
sized to the real corpus instead of the synthetic recipes. Being fixed and
data-independent *per unit*, it carries NO per-unit membership-contamination
channel (strictly cleaner than a per-unit catalogue), and being deterministic
boxes it carries no mass contamination.

This script (1) defines an a-priori geometric round-endpoint library, (2) validates
that a non-negative mixture of its rows can RECONSTRUCT each unit's aligned-subset
SPA (NNLS residual — does the library span the real convention shapes?), (3) prunes
to the rows actually used, and (4) writes the locked library to
`outputs/production-slab-library.json` for the refit.

Run — PATH=~/.local/bin:$PATH uv run python code/library_design.py

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-13. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import nnls

REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402

ALIGN_RULE = "C"

# A-priori geometric round-endpoint grid (50-year endpoints spanning the envelope
# [-50, 350], plus the AD-1 origin the corpus uses). Every (lo, hi) box with
# lo < hi and clipped width >= 49 (convention slabs are wide; sub-50 intervals are
# genuine-like and excluded so p_conv cannot mimic a genuine peak).
LO_GRID = (-50, 1, 51, 101, 151, 201, 251, 301)
HI_GRID = (50, 100, 150, 200, 250, 300, 350)
MIN_WIDTH = 49
USE_WEIGHT_THRESHOLD = 0.02   # prune a row unused (max Dirichlet-equiv weight < this) across units


def candidate_library() -> list[tuple[int, int]]:
    """All a-priori round-endpoint slabs (lo<hi, clipped width>=MIN_WIDTH), deduped
    after envelope clipping (so e.g. [301,400] and [301,350] collapse to one box)."""
    seen: dict[tuple[int, int], tuple[int, int]] = {}
    for lo in LO_GRID:
        for hi in HI_GRID:
            if hi <= lo:
                continue
            lo_c = max(lo, H.ENV_START)
            hi_c = min(hi, H.ENV_END)
            if hi_c - lo_c < MIN_WIDTH:
                continue
            seen[(lo_c, hi_c)] = (lo, hi)   # key on the clipped box → dedupe
    return sorted(seen.keys())


def library_basis(slabs: list[tuple[int, int]]) -> np.ndarray:
    """(n_slabs, N_BINS) — each row the normalised aoristic box of one slab."""
    rows = [J.slab_mixture_spa([s]) for s in slabs]   # reuses the validated builder
    return np.vstack(rows)


def main() -> None:
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    units = H.enumerate_units()
    aligned_full = J.aligned_indicator(df, rule=ALIGN_RULE)
    idx_full = df.index

    slabs = candidate_library()
    basis = library_basis(slabs)          # (n_slabs, 80)
    n_slabs = len(slabs)
    print(f"Candidate a-priori library: {n_slabs} round-endpoint slabs "
          f"(LO_GRID×HI_GRID, width>={MIN_WIDTH}, envelope-clipped+deduped).")

    # Collinearity of the candidate basis.
    cond = float(np.linalg.cond(basis @ basis.T))
    print(f"Gram-matrix condition number: {cond:.1f}\n")

    # Per-unit NNLS reconstruction of the aligned-subset SPA.
    A = basis.T                            # (80, n_slabs) — columns are slab shapes
    print("=== reconstruction of each unit's aligned-subset SPA (NNLS) ===")
    print(f"{'unit':34s} {'nAlg':>6s} {'L1resid':>8s} {'cos':>6s}")
    resid_all = []
    used = np.zeros(n_slabs, dtype=bool)
    for u in units:
        sub = H.subset_corpus(df, u, latin)
        loc = idx_full.get_indexer(sub.index)
        amask = aligned_full[loc]
        al = sub.loc[amask]
        if len(al) == 0:
            continue
        spa = H.aoristic_spa(al["nb"].to_numpy(), al["na"].to_numpy())
        if spa.sum() <= 0:
            continue
        spa = spa / spa.sum()
        w, _ = nnls(A, spa)
        recon = A @ w
        l1 = float(np.abs(spa - recon).sum())          # total-variation-ish residual mass
        cos = float(recon @ spa / (np.linalg.norm(recon) * np.linalg.norm(spa) + 1e-12))
        resid_all.append(l1)
        if w.sum() > 0:
            used |= (w / w.sum()) >= USE_WEIGHT_THRESHOLD
        print(f"{u['name'][:34]:34s} {int(amask.sum()):6d} {l1:8.3f} {cos:6.3f}")

    print(f"\nL1 residual mass: mean {np.mean(resid_all):.3f}, max {np.max(resid_all):.3f} "
          f"(0 = library perfectly spans the aligned shape)")

    pruned = [s for s, keep in zip(slabs, used) if keep]
    print(f"\nRows used (max normalised weight >= {USE_WEIGHT_THRESHOLD} in >=1 unit): "
          f"{len(pruned)}/{n_slabs}")
    print("Pruned library slabs:", pruned)

    # Re-validate reconstruction on the PRUNED library (the one we will lock).
    pbasis = library_basis(pruned)
    pA = pbasis.T
    presid = []
    for u in units:
        sub = H.subset_corpus(df, u, latin)
        loc = idx_full.get_indexer(sub.index)
        amask = aligned_full[loc]
        al = sub.loc[amask]
        if len(al) == 0:
            continue
        spa = H.aoristic_spa(al["nb"].to_numpy(), al["na"].to_numpy())
        if spa.sum() <= 0:
            continue
        spa = spa / spa.sum()
        w, _ = nnls(pA, spa)
        presid.append(float(np.abs(spa - pA @ w).sum()))
    pcond = float(np.linalg.cond(pbasis @ pbasis.T))
    print(f"\nPRUNED library: {len(pruned)} rows, cond {pcond:.1f}, "
          f"L1 residual mean {np.mean(presid):.3f}, max {np.max(presid):.3f}")

    out = {
        "generated": "2026-06-13",
        "align_rule": ALIGN_RULE,
        "lo_grid": list(LO_GRID), "hi_grid": list(HI_GRID), "min_width": MIN_WIDTH,
        "n_candidate": n_slabs, "n_pruned": len(pruned),
        "use_weight_threshold": USE_WEIGHT_THRESHOLD,
        "candidate_slabs": [list(s) for s in slabs],
        "library_slabs": [list(s) for s in pruned],     # the LOCKED production library
        "pruned_cond": pcond,
        "recon_l1_mean": float(np.mean(presid)), "recon_l1_max": float(np.max(presid)),
    }
    (REFIT / "outputs" / "production-slab-library.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nWrote {REFIT / 'outputs' / 'production-slab-library.json'}")


if __name__ == "__main__":
    main()
