#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recovery_test.py — SMALL recovery test for the informed-α prior PROTOTYPE.
==========================================================================

EXPLORATORY (2026-06-09). NOT production. Designed to be CHEAP (a handful of
synthetic cells), to answer ONE question: does the informed-α prior recover the
PERIOD-CONCENTRATED failure cases better than the flat-prior status quo WITHOUT
degrading the IDENTIFIABLE controls?

The crux of an honest test — the basis MISMATCH
-----------------------------------------------
The α-identifiability failure is NOT a fitting bug: it is what happens when a
unit's TRUE convention mass sits in a narrow window (AD ~100–300) while the model
is fit with a BROAD shared basis whose mass is spread across the whole envelope.
The broad basis is in the "wrong PLACE" for these units, so the flexible GRW
``p_gen`` absorbs the narrow convention mass and α collapses.

To reproduce this faithfully we must therefore generate cells whose TRUE
``p_conv`` is a NARROW-window convention shape that DIFFERS from the shared basis
used at FIT time. If we generated from the same basis we fit with, α would be
identifiable and there would be no failure to fix. The mismatch is the whole
point — so:

  * PERIOD-CONCENTRATED cells (the failure mode): true p_conv = a narrow Gaussian
    convention bump centred ~AD 200 (sd ~60), genuine p_gen = a broad smooth
    growth. Fit with the BROAD shared basis. Flat-prior α is expected to COLLAPSE.

  * IDENTIFIABLE control cells: true p_conv = the BROAD shared basis itself
    (built from realistic Dirichlet tier weights). Fit with the same shared
    basis. Flat-prior α should already be ~correct; the informed prior must NOT
    break it.

For each cell we fit BOTH:
  (a) the FLAT-prior shared-basis model (status quo) — Beta(1, 1);
  (b) the INFORMED-α-prior model — Beta centred on the cell's "family fraction".

The "family fraction" the informed prior is centred on
------------------------------------------------------
For a synthetic cell we KNOW the convention fraction is exactly α_true, and the
convention component IS grid-aligned (round-period) by construction. So the
honest analogue of the observable family fraction the production harness would
compute is α_true itself (optionally perturbed to model the proxy's noise — we
add a small mis-estimate to be conservative; see PRIOR_MEAN_NOISE). On REAL data
the prior mean would instead be ``build_unit_y(...)['f1f3_family_mass_fraction']``
— see the REPORT design-choices section on how to compute it (and the known
under-count for wide-"Big"-slab-heavy units).

Output
------
``outputs/recovery-results.json`` — per (cell × prior) α posterior summary,
genuine-SPA recovery error, and convergence. Consumed by ``make_report.py`` /
the REPORT tables.

Run on sapphire (MCMC):
    export TMPDIR=/home/shawn/.cache/inscriptions-pytensor-tmp \
           PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False
    taskset -c 0-11 ~/.local/bin/uv run python recovery_test.py

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's exploratory brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------- #
# Paths. We run from sapphire:~/h2-smoke/ (code scp'd there), but keep a repo   #
# fallback so the script also runs in-repo. design.json is read from whichever  #
# location exists.                                                              #
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
_REPO_DESIGN = Path(
    "/home/shawn/Code/inscriptions/runs/2026-06-06-convention-basis-redesign/design.json"
)
_LOCAL_DESIGN = HERE / "design.json"
DESIGN_JSON = _LOCAL_DESIGN if _LOCAL_DESIGN.exists() else _REPO_DESIGN

OUT_DIR = HERE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Make the prototype model importable.
sys.path.insert(0, str(HERE))
from informed_alpha_lib import (  # noqa: E402
    beta_from_mean_concentration,
    build_model_informed_alpha,
)

# --------------------------------------------------------------------------- #
# Envelope (must match design.json / the production harness).                   #
# --------------------------------------------------------------------------- #
ENV_START, ENV_END, BIN_SIZE = -50, 350, 5
N_BINS = (ENV_END - ENV_START) // BIN_SIZE  # 80
BIN_EDGES = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

# --------------------------------------------------------------------------- #
# Sampler defaults (brief §"Compute & constraints" / the production config).    #
# --------------------------------------------------------------------------- #
N_DRAWS = 2000
N_TUNE = 1000
N_CHAINS = 4
TARGET_ACCEPT = 0.95
BASE_SEED = 20260609

# --------------------------------------------------------------------------- #
# Prototype knobs (FLAGGED for Shawn — see REPORT design choices).              #
# --------------------------------------------------------------------------- #
# Informed-prior concentration sweep. Kept WIDE so data can still move α.
# κ = 6 is the headline; 4 and 8 bracket it for a sensitivity read.
CONCENTRATION_SWEEP = (4.0, 6.0, 8.0)
HEADLINE_CONCENTRATION = 6.0

# The informed prior is centred on the unit's family fraction. On synthetic data
# the honest analogue is α_true (convention is grid-aligned by construction). We
# perturb it slightly to model the proxy's real-world mis-estimate: the family
# fraction UNDER-counts convention for wide-"Big"-slab-heavy units (brief), so we
# bias the prior mean DOWNWARD by this amount as a conservative stress test (the
# prior should still help even when its centre is pulled the "wrong" way).
PRIOR_MEAN_NOISE = -0.10  # additive bias on the prior mean vs α_true

# Sample size per cell. One mid value keeps the prototype cheap.
N_PER_CELL = 10_000

# A "true convention is narrow" Gaussian (the failure mode). Centroid ~AD 200,
# sd ~60 → ~91 % of mass in AD 100–300, vs ~62 % for the broad shared basis.
NARROW_CONV_MU = 200.0
NARROW_CONV_SD = 60.0


def gaussian_pmf(mu: float, sd: float) -> np.ndarray:
    """Sum-to-1 Gaussian over the bin centres."""
    v = np.exp(-0.5 * ((BIN_CENTRES - mu) / sd) ** 2)
    return v / v.sum()


def exponential_pmf(rate: float, sign: float) -> np.ndarray:
    """Sum-to-1 exponential over the bin centres (matches cell_lib.build_pgen)."""
    v = np.exp(sign * rate * (BIN_CENTRES - ENV_START))
    return v / v.sum()


def load_shared_basis(frame: str = "latin") -> np.ndarray:
    """The shared convention basis used at FIT time (the status-quo basis)."""
    d = json.loads(DESIGN_JSON.read_text(encoding="utf-8"))
    key = "tier_basis_empirical_latin" if frame == "latin" else "tier_basis_empirical"
    basis = np.asarray(d[key], dtype=float)
    assert basis.shape == (3, N_BINS), basis.shape
    return basis


def broad_conv_from_basis(basis: np.ndarray, tier_weights: np.ndarray) -> np.ndarray:
    """A broad convention p_conv built from the shared basis + realistic tier
    weights (the IDENTIFIABLE control's true convention shape)."""
    v = tier_weights @ basis
    return v / v.sum()


def make_cells(basis: np.ndarray) -> list[dict]:
    """Enumerate the small recovery grid.

    Two regimes × a few α values. Genuine p_gen is a broad smooth growth in BOTH
    regimes (so genuine ≠ convention only by SHAPE/LOCATION, which is exactly the
    confound). The regimes differ ONLY in where the TRUE convention sits:

      * period-concentrated → true p_conv = narrow Gaussian bump (≠ shared basis);
      * identifiable        → true p_conv = broad shared-basis convention.
    """
    p_gen_genuine = exponential_pmf(rate=0.005, sign=1)  # broad smooth growth

    # Empirical-ish tier weights for the broad control convention.
    tw_empirical = np.array([0.184007, 0.430645, 0.385348])
    broad_conv = broad_conv_from_basis(basis, tw_empirical)
    narrow_conv = gaussian_pmf(NARROW_CONV_MU, NARROW_CONV_SD)

    alphas_concentrated = (0.30, 0.60)  # the under-attribution regime of interest
    alphas_identifiable = (0.30, 0.60)

    cells: list[dict] = []
    idx = 0
    for a in alphas_concentrated:
        cells.append({
            "cell_index": idx, "regime": "period_concentrated",
            "alpha_true": float(a), "p_conv_true": narrow_conv,
            "p_gen_true": p_gen_genuine,
            "label": f"concentrated_a{a:.2f}",
        })
        idx += 1
    for a in alphas_identifiable:
        cells.append({
            "cell_index": idx, "regime": "identifiable",
            "alpha_true": float(a), "p_conv_true": broad_conv,
            "p_gen_true": p_gen_genuine,
            "label": f"identifiable_a{a:.2f}",
        })
        idx += 1
    return cells


def generate_y(cell: dict, n: int, seed: int) -> np.ndarray:
    """Multinomial draw from the cell's true mixture (mirrors synth.py)."""
    p_true = cell["alpha_true"] * cell["p_conv_true"] + (1.0 - cell["alpha_true"]) * cell["p_gen_true"]
    p_true = p_true / p_true.sum()
    rng = np.random.default_rng(seed)
    return rng.multinomial(n, p_true).astype(np.int64), p_true


def fit_one(y: np.ndarray, basis: np.ndarray, alpha_a: float, alpha_b: float,
            seed: int) -> dict:
    """Fit one model (informed OR flat — flat is Beta(1,1) via a=b=1) and extract
    α posterior + genuine-SPA recovery."""
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
        idata, var_names=["alpha", "tier_weights", "sigma_smooth", "z_pgen"],
        round_to="none",
    )
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    alpha = idata.posterior["alpha"].values.reshape(-1)
    alpha_lo, alpha_hi = (float(x) for x in np.percentile(alpha, [2.5, 97.5]))
    alpha_med = float(np.median(alpha))

    p_gen = idata.posterior["p_gen"].values.reshape(-1, N_BINS)
    p_gen_med = np.median(p_gen, axis=0)
    p_gen_med = p_gen_med / p_gen_med.sum()

    return {
        "alpha_median": alpha_med,
        "alpha_ci_lo": alpha_lo,
        "alpha_ci_hi": alpha_hi,
        "p_gen_median": [float(x) for x in p_gen_med],
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_div,
    }


def spa_l1_error(p_hat: np.ndarray, p_true: np.ndarray) -> float:
    """Total-variation (½·L1) distance between recovered and true genuine SPA."""
    p_hat = np.asarray(p_hat, dtype=float)
    p_true = np.asarray(p_true, dtype=float)
    return float(0.5 * np.abs(p_hat - p_true).sum())


def main() -> None:
    basis = load_shared_basis(frame="latin")
    cells = make_cells(basis)
    print(f"[recovery] {len(cells)} cells; basis frame=latin; N/cell={N_PER_CELL}")

    results = []
    for cell in cells:
        ci = cell["cell_index"]
        seed_data = BASE_SEED + ci
        y, p_true = generate_y(cell, N_PER_CELL, seed_data)
        p_gen_true = np.asarray(cell["p_gen_true"], dtype=float)

        rec = {
            "cell_index": ci,
            "label": cell["label"],
            "regime": cell["regime"],
            "alpha_true": cell["alpha_true"],
            "n": N_PER_CELL,
            "fits": {},
        }

        # (a) FLAT-prior status quo: Beta(1, 1).
        print(f"  [{cell['label']}] flat Beta(1,1) ...", flush=True)
        flat = fit_one(y, basis, 1.0, 1.0, seed=BASE_SEED + 100 + ci)
        flat["alpha_bias"] = flat["alpha_median"] - cell["alpha_true"]
        flat["genuine_spa_tv_error"] = spa_l1_error(flat["p_gen_median"], p_gen_true)
        rec["fits"]["flat"] = flat

        # (b) INFORMED-α prior: centred on (α_true + noise), swept over κ.
        prior_mean = float(np.clip(cell["alpha_true"] + PRIOR_MEAN_NOISE, 1e-3, 1 - 1e-3))
        rec["prior_mean_used"] = prior_mean
        for kappa in CONCENTRATION_SWEEP:
            a, b = beta_from_mean_concentration(prior_mean, kappa)
            tag = f"informed_k{kappa:g}"
            print(f"  [{cell['label']}] {tag} (mean={prior_mean:.2f}, a={a:.2f}, b={b:.2f}) ...", flush=True)
            inf = fit_one(y, basis, a, b, seed=BASE_SEED + 200 + ci)
            inf["prior_mean"] = prior_mean
            inf["concentration"] = kappa
            inf["beta_a"] = a
            inf["beta_b"] = b
            inf["alpha_bias"] = inf["alpha_median"] - cell["alpha_true"]
            inf["genuine_spa_tv_error"] = spa_l1_error(inf["p_gen_median"], p_gen_true)
            rec["fits"][tag] = inf

        results.append(rec)

    out = {
        "meta": {
            "base_seed": BASE_SEED,
            "n_per_cell": N_PER_CELL,
            "concentration_sweep": list(CONCENTRATION_SWEEP),
            "headline_concentration": HEADLINE_CONCENTRATION,
            "prior_mean_noise": PRIOR_MEAN_NOISE,
            "narrow_conv_mu": NARROW_CONV_MU,
            "narrow_conv_sd": NARROW_CONV_SD,
            "basis_frame": "latin",
            "sampler": {
                "draws": N_DRAWS, "tune": N_TUNE, "chains": N_CHAINS,
                "target_accept": TARGET_ACCEPT,
            },
        },
        "results": results,
    }
    out_path = OUT_DIR / "recovery-results.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[recovery] wrote {out_path}")


if __name__ == "__main__":
    main()
