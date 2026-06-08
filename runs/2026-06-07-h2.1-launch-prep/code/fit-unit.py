#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fit-unit.py — fit ONE H2.1 unit (production worker). Resumable: skips if its
output JSON already exists. Reads the pre-built y vector from units-data.json
(so it does not re-load the corpus), selects the per-frame basis, fits with the
validated build_model_f1_f3, and persists the per-unit posterior record.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import h2_lib as H

# Fields copied from the prepped unit record into the output.
_META = ("name", "kind", "frame", "tier", "unit_index", "n_eff", "n_rows",
         "f1f3_family_mass_fraction")


def final_tier(prep_tier: str, res: dict) -> str:
    """Resolve the reportability tier from the fit (launch-spec §7)."""
    if not res["convergence_pass"]:
        return "review-nonconverged"
    if prep_tier in ("reportable", "primary", "secondary") and not res["in_envelope_alpha"]:
        return "caveated-alpha-gt-0.70"
    return prep_tier


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--unit-index", type=int, required=True)
    ap.add_argument("--units-data", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    rec = json.loads(a.units_data.read_text(encoding="utf-8"))["units"][a.unit_index]
    out = a.out_dir / f"unit-{a.unit_index:02d}.json"
    if out.exists() and not a.force:
        print(f"[fit-unit] {rec['name']} already complete; skipping.")
        return 0

    design = H.load_design()
    basis = H.select_basis(design, rec["frame"])
    y = np.asarray(rec["y"], dtype=np.int64)
    res = H.fit_unit(y, basis, seed=H.BASE_SEED + a.unit_index)

    record = {k: rec[k] for k in _META}
    record.update(res)
    record["prep_tier"] = rec["tier"]
    record["final_tier"] = final_tier(rec["tier"], res)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"[fit-unit] {rec['name']}: alpha={res['alpha_median']:.3f} "
          f"conv={res['convergence_pass']} tier={record['final_tier']} -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
