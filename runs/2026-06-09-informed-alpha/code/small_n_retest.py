#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
small_n_retest.py — Re-test the informed-α prior at REALISTIC SMALL N.
=======================================================================

CONTEXT
-------
The prototype (``recovery_test.py``, N=10,000) found that a wide informed-α prior
(κ ∈ {4, 6, 8}) barely moves the period-concentrated α estimate. But the REAL
affected units are frontier provinces with N ≈ 1,500–2,800 inscriptions — where a
prior bites harder because the likelihood is less peaked.

ONE QUESTION
------------
At N ∈ {1500, 2500}, does an informed Beta prior — centred on the true convention
fraction, at concentration κ ∈ {6, 10, 20} — meaningfully pull the
period-concentrated α estimate toward truth, and at what κ? Or does it still
fail at realistic small N, as it did at N=10,000?

DESIGN
------
Cells:
  * ONLY the period-concentrated failure regime (narrow Gaussian true p_conv,
    broad shared basis at fit time — same mismatch as the prototype).
  * α_true ∈ {0.30, 0.60}.
  * N ∈ {1500, 2500}.

Priors under test:
  * flat Beta(1,1)  — status quo;
  * informed Beta, mean = α_true (exact), κ ∈ {6, 10, 20};
  * informed Beta, mean = α_true − 0.10 (biased low), κ ∈ {6, 10, 20}.
    (This is a conservative stress: the observable proxy tends to under-count.)

Sampler: draws=2000, tune=1000, chains=4, target_accept=0.95, cores=1.

Output
------
``outputs/small-n-retest.json`` — per (N × α_true × prior) α posterior summary
and convergence flags, plus a human-readable compact table in the note.

Run on sapphire:
    export TMPDIR=/home/shawn/.cache/inscriptions-pytensor-tmp \\
           PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False
    taskset -c 0-11 ~/.local/bin/uv run python small_n_retest.py

Author / Date
-------------
Claude Code (Sonnet 4.6) on Shawn Ross's small-N follow-up brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------- #
# Paths — run from sapphire:~/h2-smoke/ (code scp'd) or directly in-repo.      #
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
_REPO_DESIGN = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign/design.json"
)
_LOCAL_DESIGN = HERE / "design.json"
DESIGN_JSON = _LOCAL_DESIGN if _LOCAL_DESIGN.exists() else _REPO_DESIGN

OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Make the prototype model importable (same directory).
sys.path.insert(0, str(HERE))
from informed_alpha_lib import (  # noqa: E402
    beta_from_mean_concentration,
    build_model_informed_alpha,
)

# --------------------------------------------------------------------------- #
# Envelope — must match the production harness and design.json.                 #
# --------------------------------------------------------------------------- #
ENV_START, ENV_END, BIN_SIZE = -50, 350, 5
N_BINS = (ENV_END - ENV_START) // BIN_SIZE  # 80
BIN_EDGES = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

# --------------------------------------------------------------------------- #
# Sampler config — production spec (brief).                                      #
# --------------------------------------------------------------------------- #
N_DRAWS = 2000
N_TUNE = 1000
N_CHAINS = 4
TARGET_ACCEPT = 0.95
BASE_SEED = 20260609_02  # distinct from prototype seed to avoid data collision

# --------------------------------------------------------------------------- #
# Small-N retest knobs.                                                         #
# --------------------------------------------------------------------------- #
# Sample sizes under test: realistic frontier-province range.
N_SWEEP = (1500, 2500)

# Concentration sweep: tighter than prototype's {4,6,8} — does a stiffer prior
# finally bite at small N?
CONCENTRATION_SWEEP = (6.0, 10.0, 20.0)

# Prior-mean conditions. For each κ we run two mean conditions:
#   (a) "exact"  — mean = α_true          (best-case proxy)
#   (b) "biased" — mean = α_true − 0.10   (conservative: proxy tends to under-count)
PRIOR_MEAN_BIAS = -0.10  # additive bias on mean for the "biased" condition

# α_true values to test (the failure-mode range of interest).
ALPHA_TRUE_SWEEP = (0.30, 0.60)

# Period-concentrated convention: narrow Gaussian bump centred ~AD 200, sd ~60.
# ~91 % of its mass falls in AD 100–300, cf. ~62 % for the broad shared basis.
NARROW_CONV_MU = 200.0
NARROW_CONV_SD = 60.0


# --------------------------------------------------------------------------- #
# Helpers.                                                                       #
# --------------------------------------------------------------------------- #
def gaussian_pmf(mu: float, sd: float) -> np.ndarray:
    """Sum-to-1 Gaussian probability mass function over the bin centres."""
    v = np.exp(-0.5 * ((BIN_CENTRES - mu) / sd) ** 2)
    return v / v.sum()


def exponential_pmf(rate: float, sign: float) -> np.ndarray:
    """Sum-to-1 exponential probability mass function (broad smooth growth)."""
    v = np.exp(sign * rate * (BIN_CENTRES - ENV_START))
    return v / v.sum()


def load_shared_basis(frame: str = "latin") -> np.ndarray:
    """Load the shared convention basis used at fit time (the status-quo basis)."""
    d = json.loads(DESIGN_JSON.read_text(encoding="utf-8"))
    key = "tier_basis_empirical_latin" if frame == "latin" else "tier_basis_empirical"
    basis = np.asarray(d[key], dtype=float)
    assert basis.shape == (3, N_BINS), f"Unexpected basis shape: {basis.shape}"
    return basis


def generate_y(alpha_true: float, p_conv_true: np.ndarray, p_gen_true: np.ndarray,
               n: int, seed: int) -> np.ndarray:
    """Draw a multinomial count vector from the cell's true mixture."""
    p_true = alpha_true * p_conv_true + (1.0 - alpha_true) * p_gen_true
    p_true = p_true / p_true.sum()
    rng = np.random.default_rng(seed)
    return rng.multinomial(n, p_true).astype(np.int64)


def fit_one(y: np.ndarray, basis: np.ndarray, alpha_a: float, alpha_b: float,
            seed: int) -> dict:
    """Fit one model (informed OR flat, depending on alpha_a/alpha_b) and return
    the α posterior summary + convergence diagnostics.

    The flat prior is Beta(1, 1), i.e., alpha_a = alpha_b = 1.0.
    """
    import arviz as az
    import pymc as pm

    model = build_model_informed_alpha(y, basis, alpha_a, alpha_b)
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=N_DRAWS, tune=N_TUNE, chains=N_CHAINS, cores=1,
                target_accept=TARGET_ACCEPT, random_seed=seed,
                progressbar=False, return_inferencedata=True,
            )

    summ = az.summary(
        idata,
        var_names=["alpha", "tier_weights", "sigma_smooth", "z_pgen"],
        round_to="none",
    )
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    alpha_samples = idata.posterior["alpha"].values.reshape(-1)
    alpha_lo, alpha_hi = (float(x) for x in np.percentile(alpha_samples, [2.5, 97.5]))
    alpha_med = float(np.median(alpha_samples))

    return {
        "alpha_median": alpha_med,
        "alpha_ci_lo": alpha_lo,
        "alpha_ci_hi": alpha_hi,
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_div,
    }


# --------------------------------------------------------------------------- #
# Main.                                                                         #
# --------------------------------------------------------------------------- #
def main() -> None:
    basis = load_shared_basis(frame="latin")
    p_gen_true = exponential_pmf(rate=0.005, sign=1)   # broad smooth growth
    narrow_conv = gaussian_pmf(NARROW_CONV_MU, NARROW_CONV_SD)

    print(
        f"[small_n_retest] period-concentrated cells only; "
        f"N_sweep={N_SWEEP}; alpha_sweep={ALPHA_TRUE_SWEEP}; "
        f"kappa_sweep={CONCENTRATION_SWEEP}"
    )

    results: list[dict] = []
    cell_idx = 0

    for n_obs in N_SWEEP:
        for alpha_true in ALPHA_TRUE_SWEEP:
            # Re-generate y once per (N, alpha_true) combination — shared across
            # all prior conditions for a fair within-cell comparison.
            seed_data = BASE_SEED + cell_idx
            y = generate_y(alpha_true, narrow_conv, p_gen_true, n_obs, seed_data)
            cell_label = f"n{n_obs}_a{alpha_true:.2f}"
            print(f"\n--- cell: {cell_label} ---", flush=True)

            rec: dict = {
                "cell_index": cell_idx,
                "label": cell_label,
                "regime": "period_concentrated",
                "alpha_true": float(alpha_true),
                "n": int(n_obs),
                "fits": {},
            }

            # ---------------------------------------------------------------- #
            # (a) Flat prior Beta(1,1) — status quo.                            #
            # ---------------------------------------------------------------- #
            print(f"  [flat Beta(1,1)] ...", flush=True)
            flat = fit_one(y, basis, 1.0, 1.0, seed=BASE_SEED + 1000 + cell_idx)
            flat["alpha_bias"] = flat["alpha_median"] - alpha_true
            rec["fits"]["flat"] = flat

            # ---------------------------------------------------------------- #
            # (b) Informed prior — exact mean (α_true) × each κ.               #
            # ---------------------------------------------------------------- #
            for kappa in CONCENTRATION_SWEEP:
                mean_exact = float(np.clip(alpha_true, 1e-3, 1 - 1e-3))
                a_ex, b_ex = beta_from_mean_concentration(mean_exact, kappa)
                tag_ex = f"informed_exact_k{kappa:g}"
                print(
                    f"  [{tag_ex}] mean={mean_exact:.2f}, a={a_ex:.2f}, "
                    f"b={b_ex:.2f} ...",
                    flush=True,
                )
                res_ex = fit_one(y, basis, a_ex, b_ex, seed=BASE_SEED + 2000 + cell_idx)
                res_ex.update({
                    "prior_mean": mean_exact,
                    "concentration": kappa,
                    "beta_a": a_ex,
                    "beta_b": b_ex,
                    "alpha_bias": res_ex["alpha_median"] - alpha_true,
                })
                rec["fits"][tag_ex] = res_ex

            # ---------------------------------------------------------------- #
            # (c) Informed prior — biased mean (α_true − 0.10) × each κ.        #
            # ---------------------------------------------------------------- #
            for kappa in CONCENTRATION_SWEEP:
                mean_biased = float(np.clip(alpha_true + PRIOR_MEAN_BIAS, 1e-3, 1 - 1e-3))
                a_bi, b_bi = beta_from_mean_concentration(mean_biased, kappa)
                tag_bi = f"informed_biased_k{kappa:g}"
                print(
                    f"  [{tag_bi}] mean={mean_biased:.2f}, a={a_bi:.2f}, "
                    f"b={b_bi:.2f} ...",
                    flush=True,
                )
                res_bi = fit_one(y, basis, a_bi, b_bi, seed=BASE_SEED + 3000 + cell_idx)
                res_bi.update({
                    "prior_mean": mean_biased,
                    "concentration": kappa,
                    "beta_a": a_bi,
                    "beta_b": b_bi,
                    "alpha_bias": res_bi["alpha_median"] - alpha_true,
                })
                rec["fits"][tag_bi] = res_bi

            results.append(rec)
            cell_idx += 1

    # ------------------------------------------------------------------------ #
    # Write JSON output.                                                         #
    # ------------------------------------------------------------------------ #
    out = {
        "meta": {
            "description": "Small-N retest of informed-α prior (follow-up to prototype)",
            "base_seed": BASE_SEED,
            "n_sweep": list(N_SWEEP),
            "alpha_true_sweep": list(ALPHA_TRUE_SWEEP),
            "concentration_sweep": list(CONCENTRATION_SWEEP),
            "prior_mean_bias": PRIOR_MEAN_BIAS,
            "regime": "period_concentrated_only",
            "narrow_conv_mu": NARROW_CONV_MU,
            "narrow_conv_sd": NARROW_CONV_SD,
            "basis_frame": "latin",
            "sampler": {
                "draws": N_DRAWS,
                "tune": N_TUNE,
                "chains": N_CHAINS,
                "target_accept": TARGET_ACCEPT,
            },
        },
        "results": results,
    }
    out_path = OUT_DIR / "small-n-retest.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[small_n_retest] wrote {out_path}")
    _print_summary_table(results)


def _print_summary_table(results: list[dict]) -> None:
    """Print a compact bias table to stdout for quick inspection."""
    print("\n=== α-recovery bias table (median − α_true) ===")
    print(
        f"{'N':>6}  {'α_true':>6}  {'prior':>26}  "
        f"{'α_med':>6}  {'bias':>7}  {'Rhat':>6}  {'divg':>5}"
    )
    print("-" * 75)
    for rec in results:
        n = rec["n"]
        at = rec["alpha_true"]
        for tag, fit in rec["fits"].items():
            print(
                f"{n:6d}  {at:6.2f}  {tag:>26}  "
                f"{fit['alpha_median']:6.3f}  "
                f"{fit['alpha_bias']:+7.3f}  "
                f"{fit['max_rhat']:6.3f}  "
                f"{fit['n_divergences']:5d}"
            )
        print()


if __name__ == "__main__":
    main()
