#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_emit_provenance.py — provenance gate for the H3b posterior re-emit.
==========================================================================

The H3b Stage-A re-run (``run_refit.py --emit-draws``) re-samples the 29 cc-library
units to persist the per-draw genuine-SPA posterior. Because the refit is seeded and
deterministic, the re-run must reproduce the canonical adopted-θ fits. This script
checks three things and writes a manifest:

1. **Reproducibility** — fresh per-unit ``corrected_genuine_spa`` vs a pre-run
   snapshot of the canonical ``units/`` JSONs (max abs Δ).
2. **Committed α** — fresh ``alpha_median`` vs the committed ``refit-summary.json``.
3. **Draws↔median consistency** — median of the persisted ``p_gen`` draws (npz)
   reproduces the per-unit JSON ``p_gen_median_raw`` (the draws are internally
   consistent with the saved hand-off).

Exit 0 = PASS (all within tolerance); exit 1 = at least one unit out of tolerance
(reported loudly — the draws are still a valid posterior, but non-bit-reproducibility
is flagged for Shawn). Usage:

    uv run python code/verify_emit_provenance.py \
        --snapshot outputs/units-prev-provenance \
        --fresh    outputs/units \
        --draws    outputs/posterior-draws \
        --summary  outputs/refit-summary.json

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

# Tolerances. JSON-vs-snapshot are both float64 from identical code on the same host,
# so they should match to ~1e-9 if the chains reproduce; the draws-derived median is
# float32 so it carries ~1e-4 rounding. α medians (of 8,000 draws) are robust.
TOL_SPA_REPRO = 1e-6      # fresh vs snapshot corrected_genuine_spa
TOL_ALPHA_COMMITTED = 1e-3  # fresh vs committed alpha_median
TOL_DRAWS_MEDIAN = 2e-4   # npz-draws median vs JSON p_gen_median_raw (float32)


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True, type=Path)
    ap.add_argument("--fresh", required=True, type=Path)
    ap.add_argument("--draws", required=True, type=Path)
    ap.add_argument("--summary", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=None,
                    help="manifest path (default: <draws>/PROVENANCE-MANIFEST.json)")
    args = ap.parse_args()

    summary = json.loads(args.summary.read_text())
    committed_alpha = {u["name"]: u["alpha_median"] for u in summary["units"]}

    rows = []
    worst = {"spa_repro": 0.0, "alpha_committed": 0.0, "draws_median": 0.0}
    for name in sorted(committed_alpha):
        sname = _safe(name)
        fresh_p = args.fresh / f"{sname}.json"
        snap_p = args.snapshot / f"{sname}.json"
        npz_p = args.draws / f"{sname}-pgen.npz"
        row = {"name": name, "ok": True, "notes": []}

        if not fresh_p.exists():
            row["ok"] = False; row["notes"].append("fresh JSON missing"); rows.append(row); continue
        fresh = json.loads(fresh_p.read_text())

        # (2) committed α
        d_alpha = abs(fresh["alpha_median"] - committed_alpha[name])
        row["d_alpha_committed"] = d_alpha
        worst["alpha_committed"] = max(worst["alpha_committed"], d_alpha)
        if d_alpha > TOL_ALPHA_COMMITTED:
            row["ok"] = False; row["notes"].append(f"alpha Δ {d_alpha:.2e} > {TOL_ALPHA_COMMITTED:.0e}")

        # (1) reproducibility vs snapshot
        if snap_p.exists():
            snap = json.loads(snap_p.read_text())
            a = np.asarray(fresh["corrected_genuine_spa"], float)
            b = np.asarray(snap["corrected_genuine_spa"], float)
            d_spa = float(np.max(np.abs(a - b))) if a.shape == b.shape else float("inf")
            row["d_spa_repro"] = d_spa
            worst["spa_repro"] = max(worst["spa_repro"], d_spa)
            if d_spa > TOL_SPA_REPRO:
                row["ok"] = False; row["notes"].append(f"SPA Δ {d_spa:.2e} > {TOL_SPA_REPRO:.0e}")
        else:
            row["notes"].append("no snapshot (reproducibility check skipped)")

        # (3) draws↔median consistency
        if npz_p.exists():
            z = np.load(npz_p, allow_pickle=True)
            med_from_draws = np.median(z["p_gen"].astype(np.float64), axis=0)
            med_saved = np.asarray(fresh["p_gen_median_raw"], float)
            d_med = float(np.max(np.abs(med_from_draws - med_saved)))
            row["d_draws_median"] = d_med
            row["n_draws"] = int(z["p_gen"].shape[0])
            worst["draws_median"] = max(worst["draws_median"], d_med)
            if d_med > TOL_DRAWS_MEDIAN:
                row["ok"] = False; row["notes"].append(f"draws-median Δ {d_med:.2e} > {TOL_DRAWS_MEDIAN:.0e}")
        else:
            row["ok"] = False; row["notes"].append("draws npz missing")
        rows.append(row)

    n_ok = sum(r["ok"] for r in rows)
    verdict = "PASS" if n_ok == len(rows) else "FAIL"
    manifest = {
        "verdict": verdict, "n_units": len(rows), "n_ok": n_ok,
        "worst_deviations": worst,
        "tolerances": {"spa_repro": TOL_SPA_REPRO, "alpha_committed": TOL_ALPHA_COMMITTED,
                       "draws_median": TOL_DRAWS_MEDIAN},
        "units": rows,
    }
    out = args.out or (args.draws / "PROVENANCE-MANIFEST.json")
    out.write_text(json.dumps(manifest, indent=1))

    print(f"\nPROVENANCE {verdict}: {n_ok}/{len(rows)} units within tolerance")
    print(f"  worst Δ — SPA-repro {worst['spa_repro']:.2e} | "
          f"α-committed {worst['alpha_committed']:.2e} | draws-median {worst['draws_median']:.2e}")
    for r in rows:
        if not r["ok"]:
            print(f"  ⚠ {r['name']}: {'; '.join(r['notes'])}")
    print(f"  manifest → {out}")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
