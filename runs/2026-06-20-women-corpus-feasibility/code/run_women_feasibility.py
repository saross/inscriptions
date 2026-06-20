#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_women_feasibility.py — women-corpus de-fogging feasibility (Stage 1).
=========================================================================

Fits the three women-corpus subsets (overall datable conjugal / wives /
daughters) with the **production cross-classified "library" deconvolution
VERBATIM** (imports ``run_refit.fit_one``; same model, same fixed corpus-wide
slab library, same adopted θ prior). The only new piece is a thin **adapter**
that maps Adela Sobotkova's ``data/women.csv`` (``not_before`` / ``not_after``)
into the ``nb`` / ``na`` / ``date_range`` columns the cc machinery consumes — her
corpus is then "just another unit" (Decision 34: a Latin subset learns its own
``tier_weights`` from the fixed library).

Scope (spec ``runs/2026-06-20-women-corpus-feasibility/spec.md``): METHODOLOGICAL
FEASIBILITY ONLY — genuine-vs-raw temporal de-fogging + a per-subset reachability
read. **We do NOT compute the wife-vs-daughter crossover-age trajectory** (that is
the EJA companion's substantive result). Per-role fits are for reachability only.

DATA (Shawn 2026-06-21): ``data/women.csv`` (504 daughters) IS the canonical,
cleaner dataset (the earlier "813" extras were spurious search hits). Operational
filters (flag for Adela's confirmation before any number reaches her):
  * conjugal = role ∈ {wife, daughter} ∧ type = "familial" (the whole file);
  * datable  = ``not_before`` & ``not_after`` present, ``nb ≤ na``, interval
    overlaps the model envelope [−50, 350].

Units (fresh ``unit_index`` ≥ 201 ⇒ collision-free seeds): 201 overall,
202 wives, 203 daughters. Per-unit JSON also stores the RAW aoristic SPA (the
genuine-vs-raw comparison input) and the women corpus's own date span.

Run (sapphire)::

    cd ~/Code/inscriptions
    PATH=~/.local/bin:$PATH TMPDIR=$HOME/cc-scratch/tmp \
        PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
        uv run python runs/2026-06-20-women-corpus-feasibility/code/run_women_feasibility.py

Collaboration data (Adela, Aarhus) — feasibility outputs are for the co-author
conversation, NOT for publication without her involvement. Author: Claude Code
(Opus 4.8) on Shawn's brief, 2026-06-21. UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/home/shawn/Code/inscriptions")
REFIT = ROOT / "runs/2026-06-13-cc-production-refit"
H2 = ROOT / "runs/2026-06-07-h2.1-launch-prep/code"
JOINT = ROOT / "runs/2026-06-09-joint-identifiability/code"
CELL_LIB = ROOT / "runs/2026-06-06-convention-basis-redesign/revalidation/code"
for p in (REFIT / "code", H2, JOINT, CELL_LIB):
    sys.path.insert(0, str(p))

import h2_lib as H          # noqa: E402
import refit_lib as R       # noqa: E402
import run_refit as RF      # noqa: E402  (reuse fit_one verbatim)

WOMEN_CSV = ROOT / "data/women.csv"
OUT = ROOT / "runs/2026-06-20-women-corpus-feasibility/outputs"
UNITS_DIR = OUT / "units"
DRAWS_DIR = OUT / "posterior-draws"


def load_women() -> pd.DataFrame:
    """Load the canonical women.csv (gzip despite .csv) and build the adapter
    columns. Returns the DATABLE CONJUGAL corpus (valid interval ∩ envelope)."""
    with gzip.open(WOMEN_CSV, "rt") as f:
        df = pd.read_csv(f)
    # conjugal = the whole file (role ∈ {wife, daughter}, type familial); assert it.
    assert set(df["role"].unique()) <= {"wife", "daughter"}, "unexpected role values"
    nb, na = df["not_before"], df["not_after"]
    datable = nb.notna() & na.notna() & (nb <= na) \
        & (na >= H.ENV_START) & (nb <= H.ENV_END)
    d = df.loc[datable].copy()
    d["nb"] = d["not_before"].astype(int)
    d["na"] = d["not_after"].astype(int)
    d["date_range"] = (d["na"] - d["nb"]).astype(int)
    return d


def women_units() -> list[dict]:
    return [
        {"name": "women-overall", "kind": "aggregate", "frame": "latin",
         "tier": "feasibility", "unit_index": 201, "role": None},
        {"name": "women-wives", "kind": "aggregate", "frame": "latin",
         "tier": "feasibility", "unit_index": 202, "role": "wife"},
        {"name": "women-daughters", "kind": "aggregate", "frame": "latin",
         "tier": "feasibility", "unit_index": 203, "role": "daughter"},
    ]


def fit_unit(d_all: pd.DataFrame, unit: dict, force: bool) -> dict:
    jpath = UNITS_DIR / f"{RF._safe(unit['name'])}.json"
    if jpath.exists() and not force:
        prev = json.loads(jpath.read_text())
        if "max_rhat" in prev:
            print(f"  SKIP {unit['name']} (done)")
            return prev

    sub = d_all if unit["role"] is None else d_all.loc[d_all["role"] == unit["role"]]
    n_rows_raw = int(len(sub))
    if n_rows_raw == 0:
        raise ValueError(f"{unit['name']}: empty subset")
    data = R.build_unit_cc_data(sub)
    u = {k: unit[k] for k in ("name", "kind", "tier", "frame", "unit_index")}
    t0 = time.perf_counter()
    out = RF.fit_one(u, data, emit_draws_dir=str(DRAWS_DIR))
    out["wall_s"] = time.perf_counter() - t0
    out["n_rows_raw"] = n_rows_raw
    out["row_aligned_frac"] = data["row_aligned_frac"]
    out["mass_aligned_frac"] = data["mass_aligned_frac"]
    # RAW aoristic SPA (mass units, sums to N_eff) — the genuine-vs-raw input.
    raw_spa = H.aoristic_spa(sub["nb"].to_numpy(), sub["na"].to_numpy())
    out["raw_aoristic_spa"] = [float(x) for x in raw_spa]
    out["women_date_span"] = {
        "nb_min": int(sub["nb"].min()), "nb_max": int(sub["nb"].max()),
        "na_min": int(sub["na"].min()), "na_max": int(sub["na"].max()),
        "median_interval_width": float((sub["na"] - sub["nb"]).median())}

    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = jpath.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, default=float))
    tmp.replace(jpath)
    print(f"  DONE {unit['name']:16s} α={out['alpha_median']:.3f} "
          f"[{out['alpha_ci_lo']:.3f},{out['alpha_ci_hi']:.3f}] "
          f"R̂={out['max_rhat']:.4f} ESS={out['min_ess_bulk']:.0f} "
          f"div={out['n_divergences']} N={n_rows_raw} "
          f"mass_align={out['mass_aligned_frac']:.3f} ({out['wall_s']:.0f}s)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", type=str, default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    DRAWS_DIR.mkdir(parents=True, exist_ok=True)

    d_all = load_women()
    print(f"datable conjugal corpus: {len(d_all)} "
          f"(wives={int((d_all['role']=='wife').sum())}, "
          f"daughters={int((d_all['role']=='daughter').sum())})")
    units = women_units()
    if args.only:
        units = [u for u in units if u["name"] == args.only]
        if not units:
            raise SystemExit(f"no unit named {args.only!r}")

    print(f"Fitting {len(units)} unit(s), cc-library, base_seed={R.REFIT_BASE_SEED}.")
    results = [fit_unit(d_all, u, args.force) for u in units]

    summary = {
        "model": "cc-library (joint_lib.build_model_cross_classified, pconv_mode=library)",
        "data": "data/women.csv (504 daughters, canonical per Shawn 2026-06-21)",
        "operational_filters": {
            "conjugal": "role in {wife, daughter} and type==familial",
            "datable": "not_before & not_after present, nb<=na, interval overlaps [-50,350]",
            "note": "operational; confirm against Adela's exact definitions before citing"},
        "envelope": [H.ENV_START, H.ENV_END], "bin_size": H.BIN_SIZE,
        "units": [{
            "name": r["name"], "n_rows_raw": r.get("n_rows_raw"),
            "n_eff": r["n_rows_eff"], "alpha_median": r["alpha_median"],
            "alpha_ci": [r["alpha_ci_lo"], r["alpha_ci_hi"]],
            "max_rhat": r["max_rhat"], "min_ess_bulk": r["min_ess_bulk"],
            "n_divergences": r["n_divergences"], "convergence_pass": r.get("convergence_pass"),
            "row_aligned_frac": r.get("row_aligned_frac"),
            "mass_aligned_frac": r.get("mass_aligned_frac"),
            "women_date_span": r.get("women_date_span"),
        } for r in results],
    }
    (OUT / "women-feasibility-summary.json").write_text(
        json.dumps(summary, indent=2, default=float))
    print(f"\nSummary -> {OUT / 'women-feasibility-summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
