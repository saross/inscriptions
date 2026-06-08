#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h2_lib.py — shared library for the H2.1 temporal-mixture PRODUCTION run.

This is the production deconvolution-mixture harness (launch-spec
``runs/2026-06-07-h2.1-launch-prep/launch-spec.md``). It fits, per unit, the
editorial-convention-corrected genuine summed-probability analysis (SPA) of
inscription dates and hands the posterior-median corrected genuine SPA to H3b.

Design principle — REUSE the recovery-validated pipeline, swap synthetic cells
for real units. The model, the convergence gate, and the aoristic-SPA convention
are imported / copied VERBATIM from the artefacts the recovery re-validation
PASSED on (B = 96.4 %, 2026-06-08), so production fits sit on the identical
footing the grid validated:

  * ``build_model_f1_f3`` + ``convergence_pass`` — imported from
    ``runs/2026-06-06-convention-basis-redesign/revalidation/code/cell_lib.py``.
  * ``aoristic_spa`` + ``load_filtered_lire`` + ``classify_family`` +
    ``latin_provinces`` — copied verbatim (with attribution) from
    ``runs/2026-06-06-convention-basis-redesign/code/02-build-empirical-basis.py``
    (the script that built ``design.json``'s empirical basis). Copied rather than
    imported because that source is a numeric-named script; the
    ``_assert_envelope_matches_design`` check below guards against silent drift.

The ONLY genuinely new pieces are: the largest-remainder observation model
(launch-spec §4), per-unit corpus subsetting, the per-frame basis selector, and
the no-truth fit/extraction (corrected SPA + α diagnostic + descriptive-p_conv
consistency + PPC).

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-08.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths (absolute; the repo lives at the same path on amd-tower and sapphire).  #
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
PROVINCE_LANG_CSV = (
    PROJECT_ROOT / "runs" / "2026-06-04-h3a-confirmatory" / "data"
    / "province-language-map.csv"
)
DESIGN_JSON = PROJECT_ROOT / "runs" / "2026-06-06-convention-basis-redesign" / "design.json"
UNIT_SET_JSON = (
    PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "outputs" / "unit-set.json"
)
CELL_LIB_DIR = (
    PROJECT_ROOT / "runs" / "2026-06-06-convention-basis-redesign" / "revalidation" / "code"
)

# Import the recovery-VALIDATED model + convergence gate (not reimplemented).
sys.path.insert(0, str(CELL_LIB_DIR))
from cell_lib import build_model_f1_f3, convergence_pass  # noqa: E402

# --------------------------------------------------------------------------- #
# Envelope (prereg; MUST match design.json — asserted in load_design()).        #
# --------------------------------------------------------------------------- #
ENV_START = -50
ENV_END = 350
BIN_SIZE = 5
N_BINS = (ENV_END - ENV_START) // BIN_SIZE  # 80
EXPECTED_N = 180_609  # prereg-filtered empire corpus

BIN_EDGES = np.arange(ENV_START, ENV_END + BIN_SIZE, BIN_SIZE, dtype=float)
BIN_CENTRES = (BIN_EDGES[:-1] + BIN_EDGES[1:]) / 2.0

# Family-classifier constants — VERBATIM from 02-build-empirical-basis.py.
F1_WIDTHS = {24, 49, 99, 149, 199, 299}
F3_WIDTHS = {19, 29, 39}
TIGHT_MAX = 4

# Production sampler defaults (launch-spec §5 / the recovery-validated config).
N_DRAWS = 2000
N_TUNE = 1000
N_CHAINS = 4
TARGET_ACCEPT = 0.95
BASE_SEED = 20260608  # production seed; per-unit seed = BASE_SEED + unit_index

# Acceptance (launch-spec §7).
ALPHA_ENVELOPE = 0.70  # posterior-median α ceiling for the reportable tier


# ======================================================================= #
# VERBATIM-COPIED data functions (from 02-build-empirical-basis.py).        #
# Kept in sync via _assert_envelope_matches_design(); do not edit in        #
# isolation — they must stay byte-identical to the basis-construction code.  #
# ======================================================================= #
def round_aligned(x: np.ndarray, mod: int) -> np.ndarray:
    r = np.mod(x, mod)
    return np.isin(r, [0, 1, mod - 1])


def load_filtered_lire() -> pd.DataFrame:
    """Prereg-filtered LIRE corpus (geotemporal ∧ in-province ∧ in-envelope).

    Adds ``nb`` / ``na`` / ``date_range`` and asserts the 180,609-row count
    (the same integrity gate the basis construction uses).
    """
    df = pd.read_parquet(DATA_PATH)
    is_geotemporal = (
        df["Latitude"].notna() & df["Longitude"].notna()
        & df["not_before"].notna() & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    in_envelope = (df["not_after"] >= ENV_START) & (df["not_before"] <= ENV_END)
    sub = df.loc[is_geotemporal & is_within_re & in_envelope].copy()
    sub["nb"] = sub["not_before"].astype(int)
    sub["na"] = sub["not_after"].astype(int)
    sub["date_range"] = (sub["na"] - sub["nb"]).astype(int)
    if len(sub) != EXPECTED_N:
        raise ValueError(f"Filtered corpus {len(sub):,} != expected {EXPECTED_N:,}.")
    return sub


def classify_family(df: pd.DataFrame) -> np.ndarray:
    nb = df["nb"].to_numpy()
    na = df["na"].to_numpy()
    dr = df["date_range"].to_numpy()
    f1 = np.isin(dr, list(F1_WIDTHS)) & round_aligned(nb, 25) & round_aligned(na, 25)
    f3 = np.isin(dr, list(F3_WIDTHS)) & round_aligned(nb, 10) & round_aligned(na, 10) & ~f1
    fam = np.full(len(df), "Big", dtype=object)
    tight = (dr <= TIGHT_MAX) & ~f1 & ~f3
    big = (dr >= 49) & ~f1
    other = ~(f1 | f3 | tight | big)
    fam[f1] = "F1_round"
    fam[f3] = "F3_periodic"
    fam[tight] = "Tight"
    fam[other] = "F2_Other"
    fam[big] = "Big"
    return fam


def latin_provinces() -> set[str]:
    m = pd.read_csv(PROVINCE_LANG_CSV, comment="#")
    return set(m.loc[m["language"] == "Latin", "lire_province"])


def aoristic_spa(nb: np.ndarray, na: np.ndarray) -> np.ndarray:
    """Aoristic SPA on the envelope; each inscription deposits mass 1.0 uniformly
    across [nb, na] using ORIGINAL width as denominator, clipped to the envelope.
    VERBATIM convention from 02-build-empirical-basis.aoristic_spa (and
    build-empirical-pconv) — the basis was built with this exact function."""
    spa = np.zeros(N_BINS)
    if len(nb) == 0:
        return spa
    nb = nb.astype(float)
    na = na.astype(float)
    nb_c = np.maximum(nb, ENV_START)
    na_c = np.minimum(na, ENV_END)
    width = na - nb
    valid = (width > 0) & (na_c > nb_c)
    nb_c, na_c, width = nb_c[valid], na_c[valid], width[valid]
    for i in range(N_BINS):
        lo, hi = BIN_EDGES[i], BIN_EDGES[i + 1]
        overlap = np.maximum(np.minimum(hi, na_c) - np.maximum(lo, nb_c), 0.0)
        spa[i] = (overlap / width).sum()
    return spa


# ======================================================================= #
# NEW: production observation model + per-unit data + basis selection.      #
# ======================================================================= #
def largest_remainder(mass: np.ndarray) -> np.ndarray:
    """Largest-remainder (Hare) rounding of a per-bin aoristic-mass vector to
    integer counts summing to ``round(mass.sum())`` = N_eff (launch-spec §4).

    Floors every bin, then hands the residual quota to the largest fractional
    remainders (or removes from the smallest, in the rare negative-residual case
    from float rounding). Deterministic.
    """
    total = int(round(float(mass.sum())))
    floors = np.floor(mass).astype(np.int64)
    if total <= 0:
        return np.zeros_like(floors)
    deficit = total - int(floors.sum())
    remainder = mass - np.floor(mass)
    if deficit > 0:
        idx = np.argsort(-remainder, kind="stable")[:deficit]
        floors[idx] += 1
    elif deficit < 0:
        idx = np.argsort(remainder, kind="stable")[: (-deficit)]
        floors[idx] -= 1
    return floors


def build_unit_y(df_unit: pd.DataFrame) -> dict[str, Any]:
    """Build one unit's observed count vector + descriptive context.

    Returns the integer ``y`` (largest-remainder of the aoristic SPA), ``n_eff``
    (= y.sum()), the raw row count, and the F1+F3 family-mass fraction (the
    descriptive-p_conv consistency reference, launch-spec §7).
    """
    nb = df_unit["nb"].to_numpy()
    na = df_unit["na"].to_numpy()
    mass = aoristic_spa(nb, na)
    y = largest_remainder(mass)
    fam = df_unit["family"].to_numpy()
    f1f3 = np.isin(fam, ["F1_round", "F3_periodic"])
    total_mass = float(mass.sum())
    f1f3_mass = float(aoristic_spa(nb[f1f3], na[f1f3]).sum())
    return {
        "y": y,
        "n_eff": int(y.sum()),
        "n_rows": int(len(df_unit)),
        "aoristic_mass": total_mass,
        "f1f3_family_mass_fraction": (f1f3_mass / total_mass) if total_mass > 0 else float("nan"),
    }


def load_design() -> dict[str, Any]:
    """Load design.json and assert its envelope matches this module's (anti-drift)."""
    d = json.loads(DESIGN_JSON.read_text(encoding="utf-8"))
    env = d["envelope"]
    if not (
        env["envelope_min_year"] == ENV_START
        and env["envelope_max_year"] == ENV_END
        and env["bin_width_years"] == BIN_SIZE
        and env["n_bins"] == N_BINS
    ):
        raise ValueError(f"design.json envelope {env} != h2_lib envelope.")
    return d


def select_basis(design: dict[str, Any], frame: str) -> np.ndarray:
    """Per-frame fixed convention basis (launch-spec §3): empire-aggregate uses
    the empire basis; every Latin unit (Latin-aggregate, provinces, cities) uses
    the shared Latin basis. NOT per-unit."""
    key = "tier_basis_empirical" if frame == "empire" else "tier_basis_empirical_latin"
    basis = np.asarray(design[key], dtype=float)
    assert basis.shape == (3, N_BINS), f"basis shape {basis.shape} != (3, {N_BINS})"
    return basis


def _assert_envelope_matches_design() -> None:
    load_design()  # raises on mismatch


# --------------------------------------------------------------------------- #
# Unit enumeration — the 28 units (26 primary + 2 grey-band) from unit-set.json #
# (Latin-aggregate + provinces + cities use the Latin frame; empire uses empire) #
# --------------------------------------------------------------------------- #
def enumerate_units() -> list[dict[str, Any]]:
    """Return the ordered unit list: each dict has name, kind, frame, tier, and
    the filter needed to subset the corpus. Grey-band provinces are included as
    caveated-tier (Shawn 2026-06-08)."""
    us = json.loads(UNIT_SET_JSON.read_text(encoding="utf-8"))
    units: list[dict[str, Any]] = []
    # Aggregates.
    units.append({"name": "empire-aggregate", "kind": "aggregate", "frame": "empire",
                  "tier": "secondary", "filter": ("all", None)})
    units.append({"name": "latin-aggregate", "kind": "aggregate", "frame": "latin",
                  "tier": "primary", "filter": ("latin_all", None)})
    # Latin provinces (reportable).
    for p in us["latin_provinces_reportable"]["units"]:
        name = p["province"] if isinstance(p, dict) else p
        units.append({"name": name, "kind": "province", "frame": "latin",
                      "tier": "reportable", "filter": ("province", name)})
    # Latin cities (reportable).
    cfield = us["latin_cities_reportable"].get("field", "urban_context_city")
    for c in us["latin_cities_reportable"]["units"]:
        name = c["city"] if isinstance(c, dict) else c
        units.append({"name": name, "kind": "city", "frame": "latin",
                      "tier": "reportable", "filter": (cfield, name)})
    # Grey-band provinces (caveated; included 2026-06-08).
    for p in us["grey_band_provinces"]["units"]:
        name = p["province"] if isinstance(p, dict) else p
        units.append({"name": name, "kind": "province", "frame": "latin",
                      "tier": "caveated", "filter": ("province", name)})
    for i, u in enumerate(units):
        u["unit_index"] = i
    return units


def subset_corpus(df: pd.DataFrame, unit: dict[str, Any], latin: set[str]) -> pd.DataFrame:
    """Subset the filtered corpus to one unit per its filter."""
    kind, val = unit["filter"]
    if kind == "all":
        return df
    if kind == "latin_all":
        return df.loc[df["province"].isin(latin)]
    if kind == "province":
        return df.loc[df["province"] == val]
    # else a city field (e.g. urban_context_city)
    return df.loc[df[kind] == val]


# ======================================================================= #
# NEW: the no-truth fit + extraction (corrected SPA + α diagnostic + PPC).   #
# ======================================================================= #
def fit_unit(y: np.ndarray, tier_basis: np.ndarray, seed: int,
             draws: int = N_DRAWS, tune: int = N_TUNE, chains: int = N_CHAINS,
             target_accept: float = TARGET_ACCEPT) -> dict[str, Any]:
    """Fit one unit with the validated build_model_f1_f3 and extract the
    no-ground-truth deliverables (launch-spec §7/§8):

      * posterior-median corrected genuine SPA (``p_gen`` median per bin) — H3b;
      * α posterior (median + 95 % CI) — the shape-conditioned diagnostic;
      * tier_weights posterior median — descriptive p_conv composition;
      * convergence (max R̂, min bulk-ESS, ``convergence_pass``);
      * PPC adequacy (mean |observed − posterior-predictive-mean| per bin).
    """
    import warnings
    import arviz as az
    import pymc as pm

    n_bins = int(y.size)
    model = build_model_f1_f3(y, tier_basis)
    with model:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            idata = pm.sample(
                draws=draws, tune=tune, chains=chains, cores=1,
                target_accept=target_accept, random_seed=seed,
                progressbar=False, return_inferencedata=True,
            )
            ppc = pm.sample_posterior_predictive(
                idata, progressbar=False, random_seed=seed,
            )

    # Convergence gate — summarise the SAME vars the recovery grid did
    # (fit.summarise_posterior: alpha, tier_weights, sigma_smooth, z_pgen;
    # round_to="none"), so the production gate is byte-identical to the
    # validated one. convergence_pass uses max R̂ + min bulk-ESS only.
    summ = az.summary(
        idata, var_names=["alpha", "tier_weights", "sigma_smooth", "z_pgen"],
        round_to="none",
    )
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    min_ess_tail = float(summ["ess_tail"].min())
    n_div = int(idata.sample_stats["diverging"].values.sum())

    alpha = idata.posterior["alpha"].values.reshape(-1)
    alpha_lo, alpha_hi = (float(x) for x in np.percentile(alpha, [2.5, 97.5]))
    alpha_med = float(np.median(alpha))

    p_gen = idata.posterior["p_gen"].values.reshape(-1, n_bins)
    p_gen_med = np.median(p_gen, axis=0)
    # Per-bin medians of a simplex don't sum to 1; renormalise the H3b hand-off
    # to a valid distribution (the deficit is ~2 %, the median-of-simplex artefact).
    p_gen_med_norm = p_gen_med / p_gen_med.sum() if p_gen_med.sum() > 0 else p_gen_med
    p_conv = idata.posterior["p_conv"].values.reshape(-1, n_bins)
    p_conv_med = np.median(p_conv, axis=0)
    tw = idata.posterior["tier_weights"].values.reshape(-1, tier_basis.shape[0])
    tw_med = np.median(tw, axis=0)

    # PPC adequacy: mean absolute per-bin discrepancy (observed vs ppc mean),
    # as a fraction of N_eff (so it is comparable across units).
    ppc_y = ppc.posterior_predictive["y_obs"].values.reshape(-1, n_bins)
    ppc_mean = ppc_y.mean(axis=0)
    n_eff = int(y.sum())
    ppc_mae_frac = float(np.abs(y - ppc_mean).mean() / max(n_eff, 1))

    converged = bool(convergence_pass(max_rhat, min_ess_bulk))
    return {
        "n_eff": n_eff,
        "alpha_median": alpha_med,
        "alpha_ci_lo": alpha_lo,
        "alpha_ci_hi": alpha_hi,
        "tier_weights_median": [float(x) for x in tw_med],
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "min_ess_tail": min_ess_tail,
        "n_divergences": n_div,
        "convergence_pass": converged,
        "ppc_mae_frac": ppc_mae_frac,
        "corrected_genuine_spa": [float(x) for x in p_gen_med_norm],  # H3b hand-off (sums to 1)
        "p_gen_median_raw": [float(x) for x in p_gen_med],            # pre-renorm (grid-consistent)
        "p_conv_median": [float(x) for x in p_conv_med],
        "in_envelope_alpha": bool(alpha_med <= ALPHA_ENVELOPE),
    }
