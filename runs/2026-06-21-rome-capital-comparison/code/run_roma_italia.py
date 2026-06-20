#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_roma_italia.py — Roma + Italia de-fogged units (cc-library deconvolution).
==============================================================================

Fits the new units for the Rome capital-comparison (§§1–7) and the Italia
exceptionalism thread (§8) of
``runs/2026-06-21-rome-capital-comparison/spec.md``, using the **production
cross-classified "library" deconvolution VERBATIM** — it imports
``run_refit.fit_one`` so every new unit is fit with the identical model, the
identical fixed corpus-wide slab library, and the identical adopted θ prior
(θ_conv ≈ 0.930, θ_gen ≈ 0.025, κ = 40) that the 29 production units used. The
ONLY thing that differs per unit is the corpus subset (membership), so all units
— new and existing — share one universal basis and are comparable by
construction (spec §2).

New units (fresh ``unit_index`` ≥ 101 ⇒ collision-free per-unit seeds
``REFIT_BASE_SEED + unit_index``):

  101  Roma                          province == "Roma"                 (~65 k)
  102  capitals-empire-62            urban_context_city ∈ empire caps   (~16 k)
  103  capitals-latin-41             urban_context_city ∈ Latin caps    (~15.6 k)
  104  Italia-incl-Rome              province ∈ Italian "/ Regio" ∪ Roma (~109 k)
  105  provinces-non-Italian-Latin   province ∈ (Latin − Italian)        (provinces comparator)

Existing units (NOT re-fit here; load their draws from the production refit):
``empire-aggregate``, ``latin-aggregate``, ``Italia (excl. Rome)``.

Outputs (this run's ``outputs/``): per-unit JSON (``units/<safe>.json``),
per-unit genuine-SPD draws (``posterior-draws/<safe>-pgen.npz``), and
``roma-italia-summary.json``. Resumable at unit granularity (a unit with a
parseable JSON is skipped unless ``--force``).

Run (sapphire — same hygiene as the production refit)::

    cd ~/Code/inscriptions
    PATH=~/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
        PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
        uv run python runs/2026-06-21-rome-capital-comparison/code/run_roma_italia.py

Descriptive / exploratory; Rome stays excluded from all confirmatory regressions
(Decision 36). Author: Claude Code (Opus 4.8) on Shawn's brief, 2026-06-21.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# --- production machinery on the path (same order as run_refit.py) -----------
ROOT = Path("/home/shawn/Code/inscriptions")
REFIT = ROOT / "runs/2026-06-13-cc-production-refit"
H2 = ROOT / "runs/2026-06-07-h2.1-launch-prep/code"
JOINT = ROOT / "runs/2026-06-09-joint-identifiability/code"
CELL_LIB = ROOT / "runs/2026-06-06-convention-basis-redesign/revalidation/code"
for p in (REFIT / "code", H2, JOINT, CELL_LIB):
    sys.path.insert(0, str(p))

import h2_lib as H          # noqa: E402
import refit_lib as R       # noqa: E402
import run_refit as RF      # noqa: E402  (reuse fit_one verbatim, with its module globals)

OUT = ROOT / "runs/2026-06-21-rome-capital-comparison/outputs"
UNITS_DIR = OUT / "units"
DRAWS_DIR = OUT / "posterior-draws"


def _safe(name: str) -> str:
    """Filename slug — identical to run_refit._safe (parity with production)."""
    return RF._safe(name)


def build_units() -> list[dict]:
    """The 5 new unit dicts, each with a callable ``subset`` and fresh index."""
    caps = json.loads(
        (ROOT / "runs/2026-06-04-h3a-confirmatory/outputs/"
         "h3c-i-results-oxrep-primary.json").read_text())
    emp_caps = set(caps["empire"]["capital_cities"])    # 62
    lat_caps = set(caps["latin"]["capital_cities"])     # 41
    italian = set(R._italian_provinces())               # "/ Regio" provinces
    latin = set(H.latin_provinces())                    # Latin-language provinces (excl. Roma)
    non_ital_latin = latin - italian

    def by_province(vals):
        s = set(vals)
        return lambda df: df.loc[df["province"].isin(s)]

    def by_city(vals):
        s = set(vals)
        return lambda df: df.loc[df["urban_context_city"].isin(s)]

    return [
        {"name": "Roma", "kind": "city", "frame": "empire", "tier": "reference",
         "unit_index": 101, "track": "capital-empire",
         "subset": lambda df: df.loc[df["province"] == "Roma"]},
        {"name": "capitals-empire-62", "kind": "aggregate", "frame": "empire",
         "tier": "reference", "unit_index": 102, "track": "capital-empire",
         "subset": by_city(emp_caps)},
        {"name": "capitals-latin-41", "kind": "aggregate", "frame": "latin",
         "tier": "reference", "unit_index": 103, "track": "capital-latin",
         "subset": by_city(lat_caps)},
        {"name": "Italia-incl-Rome", "kind": "aggregate", "frame": "empire",
         "tier": "reference", "unit_index": 104, "track": "italia",
         "subset": by_province(italian | {"Roma"})},
        {"name": "provinces-non-Italian-Latin", "kind": "aggregate",
         "frame": "latin", "tier": "reference", "unit_index": 105,
         "track": "italia", "subset": by_province(non_ital_latin)},
    ]


def fit_unit(df: pd.DataFrame, unit: dict, force: bool) -> dict:
    """Subset → build cc observables → fit_one (production) → write JSON + draws."""
    jpath = UNITS_DIR / f"{_safe(unit['name'])}.json"
    if jpath.exists() and not force:
        prev = json.loads(jpath.read_text())
        if "convergence" in prev or "max_rhat" in prev:
            print(f"  SKIP {unit['name']} (done)")
            return prev

    sub = unit["subset"](df)
    n_rows_raw = int(len(sub))
    if n_rows_raw == 0:
        raise ValueError(f"{unit['name']}: empty subset")
    data = R.build_unit_cc_data(sub)
    # fit_one wants a unit dict with name/kind/tier/frame/unit_index (no 'subset').
    u = {k: unit[k] for k in ("name", "kind", "tier", "frame", "unit_index")}
    t0 = time.perf_counter()
    out = RF.fit_one(u, data, emit_draws_dir=str(DRAWS_DIR))
    out["wall_s"] = time.perf_counter() - t0
    out["track"] = unit["track"]
    out["n_rows_raw"] = n_rows_raw
    out["row_aligned_frac"] = data["row_aligned_frac"]
    out["mass_aligned_frac"] = data["mass_aligned_frac"]
    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = jpath.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, default=float))
    tmp.replace(jpath)
    print(f"  DONE {unit['name']:28s} α={out['alpha_median']:.3f} "
          f"[{out['alpha_ci_lo']:.3f},{out['alpha_ci_hi']:.3f}] "
          f"R̂={out['max_rhat']:.4f} ESS={out['min_ess_bulk']:.0f} "
          f"div={out['n_divergences']} N={n_rows_raw} ({out['wall_s']:.0f}s)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", type=str, default=None, help="fit one unit by name")
    ap.add_argument("--force", action="store_true", help="re-fit even if JSON exists")
    args = ap.parse_args()

    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    DRAWS_DIR.mkdir(parents=True, exist_ok=True)

    df = H.load_filtered_lire()  # aligned_indicator recomputes family internally
    units = build_units()
    if args.only:
        units = [u for u in units if u["name"] == args.only]
        if not units:
            raise SystemExit(f"no unit named {args.only!r}")

    print(f"Fitting {len(units)} unit(s) with the production cc-library model "
          f"(REFIT_BASE_SEED={R.REFIT_BASE_SEED}).")
    results = []
    for u in units:
        results.append(fit_unit(df, u, args.force))

    summary = {
        "model": "cc-library (joint_lib.build_model_cross_classified, pconv_mode=library)",
        "theta_prior": "adopted (theta_conv~0.930, theta_gen~0.025, kappa=40)",
        "base_seed": R.REFIT_BASE_SEED,
        "units": [{
            "name": r["name"], "track": r.get("track"), "n_rows_raw": r.get("n_rows_raw"),
            "n_eff": r["n_eff"], "alpha_median": r["alpha_median"],
            "alpha_ci": [r["alpha_ci_lo"], r["alpha_ci_hi"]],
            "max_rhat": r["max_rhat"], "min_ess_bulk": r["min_ess_bulk"],
            "n_divergences": r["n_divergences"],
            "convergence_pass": r.get("convergence_pass"),
            "row_aligned_frac": r.get("row_aligned_frac"),
            "mass_aligned_frac": r.get("mass_aligned_frac"),
        } for r in results],
    }
    (OUT / "roma-italia-summary.json").write_text(json.dumps(summary, indent=2, default=float))
    print(f"\nSummary -> {OUT / 'roma-italia-summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
