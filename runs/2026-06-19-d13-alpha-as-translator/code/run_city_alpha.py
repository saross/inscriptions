#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_city_alpha.py — D13 Stage 1: per-city α via the cc-library deconvolution.
============================================================================

Fits the production cross-classified ``library`` deconvolution (the
recovery-validated ``build_model_cross_classified(pconv_mode="library")`` under
the ADOPTED re-derived θ prior, θ_conv ≈ 0.930 / θ_gen ≈ 0.025 / κ = 40)
STANDALONE per city, on the 163 Latin-frame cities with ``inscription_count`` ≥
100 (spec ``runs/2026-06-19-d13-alpha-as-translator/spec.md`` §3). This is exactly
the production refit (``runs/2026-06-13-cc-production-refit/code/run_refit.py``)
pointed at cities instead of the 29 production units.

REUSE, don't re-derive (spec §3): the model
(``joint_lib.build_model_cross_classified``), the slab library
(``refit_lib.load_library_basis``), the adopted θ priors
(``refit_lib.adopted_theta_priors``), the per-unit cc data
(``refit_lib.build_unit_cc_data``), the corpus loader / aoristic SPA / alignment
indicator / largest-remainder (``h2_lib`` / ``joint_lib``), and the convergence
gate (``cell_lib.convergence_pass``) are all imported verbatim — no lodged/shared
module is modified. The ONLY new code here is (a) the city enumeration + plain
city-filter subset (``city_lib``), (b) the **reconciliation gate** (spec §3,
REQUIRED pre-fit), (c) the **per-city α-draw persistence** (the Stage-2
multiple-imputation hand-off, analogous to the refit's ``--emit-draws`` p_gen
hand-off), and (d) the per-city ``alpha_post_sd`` + reachability flag.

``fit_city_one`` is a faithful structural mirror of ``refit_lib``'s production
``fit_one`` (same model build, same per-unit seed = D13_BASE_SEED + unit_index,
same sampler args ``H.N_DRAWS`` / ``N_TUNE`` / ``N_CHAINS`` / ``TARGET_ACCEPT``,
same convergence vars), extended to additionally persist the full α posterior
draws and to report ``alpha_post_sd``. It is kept here rather than added to the
lodged ``fit_one`` so no shared module is touched (the supp-wave / refit
precedent).

Per-city outputs (spec §3):
  * ``outputs/units/<city>.json`` — alpha_median / ci / post_sd, convergence
    (max_rhat, min_ess_bulk, n_divergences, convergence_pass), n_rows_eff, the
    H3a ``inscription_count``, the reachability flag (reliable iff N ≥ 500), the
    reconciliation triple, PPC adequacy. Atomic write (tmp + os.replace).
  * ``outputs/alpha-draws/<city>-alpha.npz`` — the full α posterior vector
    (shape ``(n_draws_total,)``, float64) for Stage-2 S2b multiple imputation.

Infra inherited verbatim from ``run_refit.py``: ProcessPoolExecutor (spawn +
``max_tasks_per_child`` worker recycling), ``--n-jobs``, unit-granular resume
(skips a city only once BOTH its JSON and its α-draw npz exist), a STATUS file,
and a BrokenProcessPool abort that leaves resume safe.

Usage (sapphire) — run from ``runs/2026-06-19-d13-alpha-as-translator/``::

    PATH=$HOME/.local/bin:$PATH TMPDIR=$HOME/tmp_grid_scratch \
        PYTENSOR_FLAGS=mode=FAST_RUN taskset -c 0-11 \
        uv run python code/run_city_alpha.py --n-jobs 12

  --only NAME        fit a single city by exact name
  --check-recon      run ONLY the reconciliation gate (no fitting) and report

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-19.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-19-d13-alpha-as-translator")
H2 = Path("/home/shawn/Code/inscriptions/runs/2026-06-07-h2.1-launch-prep/code")
JOINT = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability/code")
REFIT = Path("/home/shawn/Code/inscriptions/runs/2026-06-13-cc-production-refit/code")
CELL_LIB_DIR = (  # the recovery-validated convergence gate lives here
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign"
    "/revalidation/code")
sys.path.insert(0, str(RUN / "code"))
sys.path.insert(0, str(H2))
sys.path.insert(0, str(JOINT))
sys.path.insert(0, str(REFIT))
sys.path.insert(0, CELL_LIB_DIR)
import city_lib as C  # noqa: E402
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402
from cell_lib import convergence_pass  # noqa: E402

UNITS_DIR = RUN / "outputs" / "units"
ALPHA_DRAWS_DIR = RUN / "outputs" / "alpha-draws"
STATUS_PATH = RUN / "outputs" / "city-alpha-STATUS.txt"
RECON_PATH = RUN / "outputs" / "reconciliation-gate.json"

# New D13 base seed (spec §3); per-city seed = base + unit_index (collision-free
# because unit_index runs 0..162 with no gaps).
D13_BASE_SEED = 20260619

# Loaded once at module level; re-imported cleanly by spawn workers. Identical to
# the production refit's module-level constants (the ADOPTED re-derived θ).
LIBRARY_BASIS, LIBRARY_SLABS = R.load_library_basis()
THETA_CONV_AB, THETA_GEN_AB, THETA_CAL = R.adopted_theta_priors()
MONITORED = ["alpha", "tier_weights", "sigma_smooth", "z_pgen", "theta_conv", "theta_gen"]


def _safe(name: str) -> str:
    """Filesystem-safe city name (verbatim convention from run_refit._safe)."""
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


# --------------------------------------------------------------------------- #
# Reconciliation gate (spec §3, REQUIRED pre-fit).                              #
# --------------------------------------------------------------------------- #
def reconcile_city(df, unit: dict) -> dict:
    """Per-city reconciliation triple (spec §3).

    Compares, for one city:
      * ``h3a_count``         — the H3a ``inscription_count`` (the regression N);
      * ``mixture_subset_n``  — rows in the plain city filter (what the mixture
        is fit on); MUST equal ``h3a_count`` (same 50 BC – AD 350 window, same
        Latin frame, plain city filter == H3a's ~rome & has_hanson count for
        these cities);
      * ``aoristic_eff_n``    — the aoristic-effective ``n_rows`` the mixture
        actually consumes (``build_unit_cc_data``; lower than the raw count
        because ``aoristic_spa`` drops zero/negative-width rows and clips to the
        envelope — the SAME convention the lodged primary p_gen was fit on, so
        this difference is expected and explainable, NOT a corpus mismatch).

    Returns a dict with the triple and a ``reconciles`` bool (subset == count).
    """
    sub = C.subset_for_city(df, unit)
    cc = R.build_unit_cc_data(sub)
    h3a = int(unit["h3a_count"])
    msn = int(len(sub))
    return {
        "name": unit["name"],
        "h3a_count": h3a,
        "mixture_subset_n": msn,
        "aoristic_eff_n": int(cc["n_rows"]),
        "reconciles": bool(msn == h3a),
    }


def run_reconciliation_gate(units: list[dict]) -> tuple[bool, list[dict]]:
    """Run the reconciliation gate over ALL cities; persist the triples.

    Returns ``(all_pass, triples)``. ``all_pass`` is True iff every city's plain
    mixture subset row count equals its H3a count. The driver HALTS (does not
    fit) if any city fails (spec §3 / §5 hard-stop).
    """
    df = H.load_filtered_lire()
    triples = [reconcile_city(df, u) for u in units]
    fails = [t for t in triples if not t["reconciles"]]
    payload = {
        "n_cities": len(units),
        "all_reconcile": len(fails) == 0,
        "n_fail": len(fails),
        "window": f"{H.ENV_START} .. {H.ENV_END} (50 BC – AD 350)",
        "note": ("mixture_subset_n is the plain city filter "
                 "df[urban_context_city==name]; it must equal the H3a "
                 "inscription_count. aoristic_eff_n is lower (zero/neg-width "
                 "drop + envelope clip; same convention as the lodged primary "
                 "p_gen) and is EXPECTED, not a mismatch."),
        "failures": fails,
        "triples": triples,
    }
    RECON_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECON_PATH.write_text(json.dumps(payload, indent=1))
    return len(fails) == 0, triples


# --------------------------------------------------------------------------- #
# Per-city fit (faithful mirror of refit_lib.fit_one + α-draw persistence).     #
# --------------------------------------------------------------------------- #
def fit_city_one(unit: dict, data: dict, alpha_draws_dir: str) -> dict:
    """Fit one city's cc-library model and extract the D13 deliverables (spec §3).

    Structural mirror of the production ``refit_lib.fit_one``: the model build
    (``J.build_model_cross_classified(..., pconv_mode="library")`` with the FIXED
    slab library and the ADOPTED θ priors), the per-unit seed
    (``D13_BASE_SEED + unit_index``), the sampler args
    (``H.N_DRAWS``/``N_TUNE``/``N_CHAINS``/``TARGET_ACCEPT``, ``cores=1``), the
    convergence vars (``MONITORED``), and the PPC adequacy metric are all
    identical to production. Extensions: ``alpha_post_sd`` and the persistence of
    the full α posterior draw vector to ``<alpha_draws_dir>/<city>-alpha.npz``
    (the Stage-2 S2b multiple-imputation hand-off).
    """
    import arviz as az
    import pymc as pm

    n_bins = int(data["y_aligned"].size)
    model = J.build_model_cross_classified(
        data["y_aligned"], data["y_nonaligned"], data["k"], data["n_rows"],
        LIBRARY_BASIS, THETA_CONV_AB, THETA_GEN_AB, pconv_mode="library")
    seed = D13_BASE_SEED + unit["unit_index"]
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(draws=H.N_DRAWS, tune=H.N_TUNE, chains=H.N_CHAINS, cores=1,
                              target_accept=H.TARGET_ACCEPT, random_seed=seed,
                              progressbar=False, return_inferencedata=True)
            ppc = pm.sample_posterior_predictive(idata, progressbar=False, random_seed=seed)

    summ = az.summary(idata, var_names=MONITORED, round_to="none")
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    min_ess_tail = float(summ["ess_tail"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    a = idata.posterior["alpha"].values.reshape(-1)          # (n_draws_total,)
    alpha_med = float(np.median(a))
    alpha_lo, alpha_hi = (float(x) for x in np.percentile(a, [2.5, 97.5]))
    alpha_sd = float(np.std(a, ddof=1))

    # Stage-2 hand-off: persist the FULL α posterior draw vector (float64; an
    # 8 k-element vector is ~64 KB, trivial). Atomic write (tmp + os.replace) so a
    # resume never sees a half-written npz. Mirrors run_refit.fit_one's emit-draws.
    ed = Path(alpha_draws_dir)
    ed.mkdir(parents=True, exist_ok=True)
    tmp_npz = ed / f"{_safe(unit['name'])}-alpha.npz.tmp"
    final_npz = ed / f"{_safe(unit['name'])}-alpha.npz"
    with open(tmp_npz, "wb") as fh:
        np.savez_compressed(
            fh,
            alpha=a.astype(np.float64),               # (n_draws_total,) posterior draws
            alpha_median=np.float64(alpha_med),
            unit_index=np.int64(unit["unit_index"]),
            seed=np.int64(seed),
            h3a_count=np.int64(unit["h3a_count"]),
            name=np.array(unit["name"]),
        )
    os.replace(tmp_npz, final_npz)

    theta_conv_post = float(np.median(idata.posterior["theta_conv"].values))
    theta_gen_post = float(np.median(idata.posterior["theta_gen"].values))

    # PPC adequacy on each subset (mean |obs − ppc-mean| as a fraction of that
    # subset's total) — parity with the production refit's PPC.
    def mae_frac(obs, name):
        pp = ppc.posterior_predictive[name].values.reshape(-1, n_bins).mean(axis=0)
        tot = max(int(obs.sum()), 1)
        return float(np.abs(obs - pp).mean() / tot)
    ppc_mae_aligned = mae_frac(data["y_aligned"], "y_al_obs")
    ppc_mae_nonaligned = mae_frac(data["y_nonaligned"], "y_non_obs")

    return {
        "name": unit["name"], "kind": unit["kind"], "frame": unit["frame"],
        "unit_index": unit["unit_index"],
        # Reconciliation triple (the regression N, the mixture subset, the eff N).
        "h3a_inscription_count": int(unit["h3a_count"]),
        "mixture_subset_n": int(data["n_rows_raw"]),
        "n_rows_eff": int(data["n_rows"]),
        "k_aligned_eff": int(data["k"]),
        "row_aligned_frac": round(data["row_aligned_frac"], 4),
        "mass_aligned_frac": round(data["mass_aligned_frac"], 4),
        # α deliverables.
        "alpha_median": alpha_med, "alpha_ci_lo": alpha_lo, "alpha_ci_hi": alpha_hi,
        "alpha_post_sd": alpha_sd,
        "theta_conv_post_med": theta_conv_post, "theta_gen_post_med": theta_gen_post,
        # Convergence.
        "max_rhat": max_rhat, "min_ess_bulk": min_ess_bulk, "min_ess_tail": min_ess_tail,
        "n_divergences": n_div,
        "convergence_pass": bool(convergence_pass(max_rhat, min_ess_bulk)),
        # PPC adequacy.
        "ppc_mae_frac_aligned": ppc_mae_aligned,
        "ppc_mae_frac_nonaligned": ppc_mae_nonaligned,
        # Reachability annotation (spec §2/§3): reliable iff H3a count ≥ 500.
        "reliable": bool(unit["reliable"]),
        "reliability_floor": C.N_RELIABLE,
        "n_alpha_draws": int(a.size),
    }


def _worker(unit: dict) -> tuple[str, bool, float]:
    """Spawn-worker: load corpus, subset to the city, build cc data, fit, write.

    The corpus is loaded inside the worker (the run_refit pattern; spawn workers
    re-import cleanly). Atomic per-city JSON write (tmp + os.replace).
    """
    df = H.load_filtered_lire()
    sub = C.subset_for_city(df, unit)
    data = R.build_unit_cc_data(sub)
    t0 = time.time()
    out = fit_city_one(unit, data, alpha_draws_dir=str(ALPHA_DRAWS_DIR))
    out["secs"] = round(time.time() - t0, 1)
    tmp = UNITS_DIR / f"{_safe(unit['name'])}.json.tmp"
    final = UNITS_DIR / f"{_safe(unit['name'])}.json"
    tmp.write_text(json.dumps(out, indent=1))
    os.replace(tmp, final)
    gc.collect()
    return unit["name"], out["convergence_pass"], out["alpha_median"]


def city_is_done(unit: dict) -> bool:
    """Resume gate: a city is done only once BOTH its parseable JSON (carrying
    convergence info) AND its α-draw npz exist (the run_refit emit-draws gate)."""
    p = UNITS_DIR / f"{_safe(unit['name'])}.json"
    npz = ALPHA_DRAWS_DIR / f"{_safe(unit['name'])}-alpha.npz"
    if not p.exists() or not npz.exists():
        return False
    try:
        d = json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return False
    return "convergence_pass" in d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-jobs", type=int, default=12)
    ap.add_argument("--max-tasks-per-child", type=int, default=1)
    ap.add_argument("--only", type=str, default=None, help="fit a single city by exact name")
    ap.add_argument("--check-recon", action="store_true",
                    help="run ONLY the reconciliation gate (no fitting) and report")
    args = ap.parse_args()
    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    ALPHA_DRAWS_DIR.mkdir(parents=True, exist_ok=True)

    units = C.enumerate_city_units()
    print(f"city-alpha: {len(units)} Latin cities at N ≥ {C.N_MIN}; "
          f"library {LIBRARY_BASIS.shape[0]} rows; "
          f"θ_conv_ab={THETA_CONV_AB}, θ_gen_ab={THETA_GEN_AB}", flush=True)

    # ---- Reconciliation gate (spec §3, REQUIRED pre-fit; HALT on failure) ----
    all_pass, triples = run_reconciliation_gate(units)
    n_fail = sum(1 for t in triples if not t["reconciles"])
    print(f"reconciliation gate: {len(units) - n_fail}/{len(units)} reconcile "
          f"(mixture subset == H3a count); → {RECON_PATH}", flush=True)
    if not all_pass:
        print("HALT: reconciliation gate FAILED — mixture corpus != H3a frame for "
              f"{n_fail} cities. Will NOT fit on a mismatched corpus (spec §5).",
              flush=True)
        for t in triples:
            if not t["reconciles"]:
                print(f"   - {t['name']}: H3a={t['h3a_count']} "
                      f"subset={t['mixture_subset_n']}", flush=True)
        return 1
    if args.check_recon:
        print("reconciliation-only run: gate PASSED, no fitting requested.", flush=True)
        return 0

    if args.only:
        units = [u for u in units if u["name"] == args.only]
        if not units:
            raise SystemExit(f"no city named {args.only!r}")

    todo = [u for u in units if not city_is_done(u)]
    print(f"to fit: {len(todo)} ({len(units) - len(todo)} cached); n_jobs {args.n_jobs}",
          flush=True)
    STATUS_PATH.write_text(f"city-alpha — 0/{len(units)} done (starting)\n")
    if not todo:
        print("nothing to do (all cached).")
        return 0

    t0 = time.time()
    done = len(units) - len(todo)
    failed = []
    with ProcessPoolExecutor(max_workers=args.n_jobs,
                             max_tasks_per_child=args.max_tasks_per_child,
                             mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(_worker, u): u for u in todo}
        for fut in as_completed(futs):
            u = futs[fut]
            try:
                name, conv, amed = fut.result()
                done += 1
                print(f"[{done}/{len(units)}] {name}  α={amed:.3f}  "
                      f"conv={'ok' if conv else 'FAIL'}", flush=True)
            except BrokenProcessPool:
                STATUS_PATH.write_text(f"city-alpha — ABORTED BrokenProcessPool at {done}\n")
                print("FATAL: pool broken (OOM?) — resume re-runs unfinished cities.",
                      flush=True)
                raise
            except Exception as exc:  # noqa: BLE001
                failed.append(u["name"])
                print(f"WORKER-ERROR {u['name']}: {repr(exc)[:160]}", flush=True)
            STATUS_PATH.write_text(
                f"city-alpha — {done}/{len(units)} done; elapsed "
                f"{(time.time()-t0)/60:.1f} min; worker-errors {len(failed)}\n")
    print(f"city-alpha complete in {(time.time()-t0)/60:.1f} min. worker-errored: {failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
