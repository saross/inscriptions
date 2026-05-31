#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
letter_model.py — §5 Layer-A LETTER-MASS hierarchical model variant.
====================================================================

The letter-mass exploratory overlay (spec §5 / §A5.1; Obs 61–62). Letters are
NOT Poisson events — per-bin letter mass is a *compound sum* of heavy-tailed
per-inscription letter counts — so the clean Poisson-process aoristic likelihood
of ``model.py`` / ``hier_model.py`` does **not** transfer. This module keeps the
identical hierarchical pooling structure (global / province / city non-centred
RW1 shape tiers + level offsets, pinned scales) but replaces the observation
model with an **over-dispersed** form on the aoristically-apportioned per-bin
letter mass.

Per-bin letter-mass target ("letter SPA")
-----------------------------------------
For inscription ``i`` with row-normalised aoristic probability ``p_i[t]``
(``p_i[t] = a[i,t]·bin_width / interval_length_i``; rows sum to 1) and letter
weight ``w_i`` (= ``letter_count_conservative``), the observed per-bin letter
mass for city ``c`` is::

    y[c, t] = sum_{i in c} w_i · p_i[t]            (sums over t to the city's
                                                    total letter count)

This is the content analogue of the inscription-count SPA (which is
``sum_i p_i[t]``). It is continuous, positive, right-skewed, and over-dispersed
relative to its mean — the per-city letter-weight Kish design effect is ~2.4
(Obs 62), so the observation carries fewer *effective* observations than the
inscription count and its posterior CIs are correspondingly wider (the design
effect is absorbed by the learnt dispersion parameter).

Latent intensity (identical hierarchy to ``hier_model``)
--------------------------------------------------------
``log Λ[c,t] = alpha_g + g_shape[t] + b_u[p(c)] + u_shape[p(c),t]
                       + b_v[c]      + v_shape[c,t]`` — ``Λ[c,t]`` is now the
expected per-bin LETTER mass (so ``alpha_g`` is anchored at
``log(mean_c (total letters_c) / T)``). Shape tiers are non-centred zero-sum
RW1; scales ``s_g, s_u, s_v`` are the pinned hyperpriors (0.3 / 0.15 / 0.15);
singletons drop their province tier and pool to global. Level offsets ``b_u,
b_v`` are non-centred (the smoke funnel fix).

Observation forms (selected by posterior-predictive check)
----------------------------------------------------------
Two candidate over-dispersed observations are implemented; the production form
is chosen by a quick PPC on 2–3 cities (``letter_ppc.py``):

- ``"gamma"`` — ``y[c,t] ~ Gamma(mu=Λ[c,t], sigma=Λ[c,t]/sqrt(k))`` i.e. a
  constant-coefficient-of-variation Gamma with learnt shape ``k`` (``CV =
  1/sqrt(k)``). Continuous-natural for a compound sum. Exact-zero bins (6.4% of
  target-set bins) are floored to a tiny ``eps`` so they stay in the Gamma
  support; ``eps`` is small relative to the smallest non-zero per-bin mass.
- ``"nb"`` — ``round(y[c,t]) ~ NegativeBinomial(mu=Λ[c,t], alpha=phi)`` with
  learnt dispersion ``phi``. The canonical over-dispersed count model; supports
  zeros natively; rounding the (10s–1000s-scale) letter mass to an integer loses
  negligible information.

Both put a weakly-informative HalfNormal prior on the dispersion parameter and
register ``Lambda`` (= ``exp(log_lam)``, the expected per-bin letter mass) as a
Deterministic for posterior trajectory extraction — the letter-mass analogue of
``lam`` in the inscription model, so downstream extraction is identical.

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import sys

import numpy as np
import pymc as pm
import pytensor.tensor as pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp  # noqa: E402

T_BINS: int = dp.N_BINS  # 16 at the 25y grid; recomputed per-grid below.

OBS_FORMS = ("gamma", "nb")


# --------------------------------------------------------------------------- #
# Per-bin letter-mass target ("letter SPA") from a cached city bundle.
# --------------------------------------------------------------------------- #

def letter_spa(A: np.ndarray, letter_w: np.ndarray, bin_width: int) -> np.ndarray:
    """Per-bin letter mass ``y[t] = sum_i w_i · p_i[t]`` for one city.

    Args:
        A: Aoristic weight matrix ``(N, T)`` (fraction-of-bin-covered weights).
        letter_w: Per-inscription letter weight ``(N,)`` (0 where missing).
        bin_width: Years per bin (to convert the fraction-of-bin weight to the
            inscription's per-bin PROBABILITY mass).

    Returns:
        Length-``T`` array of per-bin letter mass; sums to ``sum_i w_i``.
    """
    A = np.asarray(A, dtype=float)
    w = np.asarray(letter_w, dtype=float)
    lengths = A.sum(axis=1) * bin_width                  # interval length per insc
    # Row-normalise to a probability mass (rows sum to 1). Guard zero-mass rows
    # (should not occur post-dataprep, which drops them) by leaving them at 0.
    safe = lengths > 0
    P = np.zeros_like(A)
    P[safe] = (A[safe] * bin_width) / lengths[safe, None]
    return (w[:, None] * P).sum(axis=0)                  # (T,)


# --------------------------------------------------------------------------- #
# Subset assembly: city names -> vectorised letter-mass model inputs.
# --------------------------------------------------------------------------- #

@dataclass
class LetterData:
    """Vectorised inputs for the letter-mass hierarchical model.

    Mirrors ``hier_model.HierData`` (same hierarchy indexing) but carries the
    per-city per-bin letter-mass matrix ``Y`` instead of the concatenated
    aoristic design matrix — the observation is the per-bin letter SPA, not the
    per-inscription likelihood.

    Attributes:
        cities: City names in model index order.
        provinces: Province per city.
        N: Per-city inscription count.
        total_letters: Per-city total letter mass (``sum_i w_i``).
        Y: ``(C, T)`` per-bin letter-mass matrix (the observation).
        city_prov: ``(C,)`` u-tier province row per city, ``-1`` for singletons.
        prov_u_row: alias of ``city_prov`` (kept for parity with HierData).
        prov_names: Non-singleton province names, in ``u_shape`` row order.
        singleton_provs: Singleton province names.
        anchor_letters_mean: Mean per-city total letters (anchors ``alpha_g``).
        bin_width: Grid bin width.
    """

    cities: list[str]
    provinces: list[str]
    N: np.ndarray
    total_letters: np.ndarray
    Y: np.ndarray
    city_prov: np.ndarray
    prov_u_row: np.ndarray
    prov_names: list[str]
    singleton_provs: list[str]
    anchor_letters_mean: float
    bin_width: int
    city_Y: dict[str, np.ndarray] = field(default_factory=dict)


def assemble(out_dir: Path, cities: list[str], *, bin_width: int | None = None) -> LetterData:
    """Load cached bundles and build vectorised letter-mass model inputs.

    Args:
        out_dir: Dataprep cache directory (25y or 50y).
        cities: City names to include (must be cached).
        bin_width: Grid bin width; inferred from the first bundle if ``None``.

    Returns:
        A :class:`LetterData`.

    Raises:
        ValueError: On empty/duplicate subsets or a city whose total letter mass
            is zero (no letter information — cannot anchor the level).
    """
    if not cities:
        raise ValueError("assemble() received an empty city subset.")
    if len(set(cities)) != len(cities):
        raise ValueError("Duplicate city names in subset.")

    Y_by_city: dict[str, np.ndarray] = {}
    prov_of: dict[str, str] = {}
    N_list, tot_list = [], []
    bw = bin_width
    T: int | None = None  # bin count, inferred from the first matrix (grid-agnostic)
    for city in cities:
        b = dp.load_city(out_dir, city)
        if bw is None:
            bw = int(b["bin_width"])
        A = np.asarray(b["A"], dtype=np.float64)
        if A.ndim != 2:
            raise ValueError(f"{city}: A must be 2-D (N, T); got {A.shape}.")
        # Mixed-grid guard (mirrors hier_model.assemble): every city's aoristic
        # matrix must share the same bin count, else the later np.stack would
        # raise an opaque shape error. Fail early with a clear message.
        if T is None:
            T = A.shape[1]
        elif A.shape[1] != T:
            raise ValueError(
                f"{city}: bin count {A.shape[1]} != {T} (mixed grids in one "
                "subset — assemble a single bin-width cache at a time)."
            )
        w = np.asarray(b["letter_w"], dtype=np.float64)
        y = letter_spa(A, w, bw)
        if y.sum() <= 0:
            raise ValueError(
                f"{city}: zero total letter mass; cannot fit the letter unit."
            )
        Y_by_city[city] = y
        prov_of[city] = b["province"]
        N_list.append(A.shape[0])
        tot_list.append(float(w.sum()))

    provinces = [prov_of[c] for c in cities]
    N = np.array(N_list, dtype=np.int64)
    total_letters = np.array(tot_list, dtype=np.float64)

    from collections import Counter
    prov_counts = Counter(provinces)
    singleton_provs = sorted(p for p, k in prov_counts.items() if k == 1)
    u_provs = sorted(p for p, k in prov_counts.items() if k > 1)
    u_row_of = {p: i for i, p in enumerate(u_provs)}
    city_prov = np.array([u_row_of.get(p, -1) for p in provinces], dtype=np.int64)

    Y = np.stack([Y_by_city[c] for c in cities], axis=0)  # (C, T)

    return LetterData(
        cities=list(cities),
        provinces=provinces,
        N=N,
        total_letters=total_letters,
        Y=Y,
        city_prov=city_prov,
        prov_u_row=city_prov.copy(),
        prov_names=u_provs,
        singleton_provs=singleton_provs,
        anchor_letters_mean=float(total_letters.mean()),
        bin_width=int(bw),
        city_Y=Y_by_city,
    )


# --------------------------------------------------------------------------- #
# Model builder.
# --------------------------------------------------------------------------- #

def build_model(
    data: LetterData,
    *,
    obs_form: str = "gamma",
    s_g: float = 0.3,
    s_u: float = 0.15,
    s_v: float = 0.15,
    s_bu: float = 0.5,
    s_bv: float = 0.5,
    level_sd: float = 1.0,
    disp_sd: float = 1.0,
    gamma_eps_frac: float = 1e-3,
) -> pm.Model:
    """Build the monolithic hierarchical LETTER-MASS model.

    The hierarchy (g/u/v non-centred zero-sum RW1 shapes + non-centred level
    offsets, pinned scales, singleton handling) is identical to
    ``hier_model.build_model``; only the observation differs.

    Args:
        data: Assembled :class:`LetterData`.
        obs_form: ``"gamma"`` (constant-CV Gamma on continuous mass) or ``"nb"``
            (NegativeBinomial on rounded mass). Selected by PPC.
        s_g, s_u, s_v: pinned HalfNormal RW1 scales (0.3 / 0.15 / 0.15).
        s_bu, s_bv: HalfNormal level-offset scales.
        level_sd: Prior SD on ``alpha_g``.
        disp_sd: HalfNormal scale on the dispersion parameter (Gamma shape ``k``
            or NB ``phi``).
        gamma_eps_frac: Zero-bin floor for the Gamma form, as a fraction of the
            smallest non-zero per-bin mass in the subset (keeps exact zeros in
            the Gamma support without distorting the non-zero bins).

    Returns:
        An unsampled :class:`pymc.Model` registering ``g_shape``, ``u_shape``,
        ``v_shape``, ``log_lam``, ``Lambda`` ((C, T) expected per-bin letter
        mass), and the dispersion parameter.
    """
    if obs_form not in OBS_FORMS:
        raise ValueError(f"obs_form must be one of {OBS_FORMS}; got {obs_form!r}.")

    C = len(data.cities)
    P = len(data.prov_names)
    T = data.Y.shape[1]

    # Anchor the global level at the mean per-city total letter mass per bin.
    alpha_mu = float(np.log(max(data.anchor_letters_mean, 1.0) / T))

    Y = np.asarray(data.Y, dtype=np.float64)

    coords = {
        "city": list(data.cities),
        "bin": list(range(T)),
        "prov": list(data.prov_names),
    }

    with pm.Model(coords=coords) as model:
        prov_u_row = pm.Data("prov_u_row", data.prov_u_row)  # (C,), -1 singleton

        # --- Global level (anchored) ----------------------------------------
        alpha_g = pm.Normal("alpha_g", alpha_mu, level_sd)

        # --- Global shape: non-centred RW1, zero-sum over time ---------------
        sigma_g = pm.HalfNormal("sigma_g", s_g)
        z_g = pm.Normal("z_g", 0.0, 1.0, dims="bin")
        g_walk = pt.cumsum(z_g) * sigma_g
        g_shape = pm.Deterministic("g_shape", g_walk - pt.mean(g_walk), dims="bin")

        # --- Province shape + level offset (non-singleton provinces only) ----
        if P > 0:
            sigma_u = pm.HalfNormal("sigma_u", s_u)
            sigma_bu = pm.HalfNormal("sigma_bu", s_bu)
            z_u = pm.Normal("z_u", 0.0, 1.0, dims=("prov", "bin"))
            u_walk = pt.cumsum(z_u, axis=1) * sigma_u
            u_shape = pm.Deterministic(
                "u_shape", u_walk - pt.mean(u_walk, axis=1, keepdims=True),
                dims=("prov", "bin"),
            )
            z_bu = pm.Normal("z_bu", 0.0, 1.0, dims="prov")
            b_u = pm.Deterministic("b_u", z_bu * sigma_bu, dims="prov")
            u_shape_pad = pt.concatenate([u_shape, pt.zeros((1, T))], axis=0)
            b_u_pad = pt.concatenate([b_u, pt.zeros((1,))], axis=0)
        else:
            u_shape_pad = pt.zeros((1, T))
            b_u_pad = pt.zeros((1,))

        city_u_shape = u_shape_pad[prov_u_row]                    # (C, T)
        city_b_u = b_u_pad[prov_u_row]                            # (C,)

        # --- City shape + level offset (all cities) -------------------------
        sigma_v = pm.HalfNormal("sigma_v", s_v)
        sigma_bv = pm.HalfNormal("sigma_bv", s_bv)
        z_v = pm.Normal("z_v", 0.0, 1.0, dims=("city", "bin"))
        v_walk = pt.cumsum(z_v, axis=1) * sigma_v
        v_shape = pm.Deterministic(
            "v_shape", v_walk - pt.mean(v_walk, axis=1, keepdims=True),
            dims=("city", "bin"),
        )
        z_bv = pm.Normal("z_bv", 0.0, 1.0, dims="city")
        b_v = pm.Deterministic("b_v", z_bv * sigma_bv, dims="city")

        # --- Assemble per-city log expected letter mass ---------------------
        log_lam = pm.Deterministic(
            "log_lam",
            alpha_g + g_shape[None, :] + city_b_u[:, None] + city_u_shape
            + b_v[:, None] + v_shape,
            dims=("city", "bin"),
        )
        Lambda = pm.Deterministic("Lambda", pt.exp(log_lam), dims=("city", "bin"))

        # --- Over-dispersed observation -------------------------------------
        if obs_form == "gamma":
            # Constant-CV Gamma: var = mu^2 / k, CV = 1/sqrt(k). Learnt shape k.
            # k ~ HalfNormal pushed away from 0 via a +1 floor so the very first
            # tuning steps have a finite-variance Gamma.
            k = pm.HalfNormal("k_shape", disp_sd) + 1.0
            k = pm.Deterministic("k_disp", k)
            sigma_obs = Lambda / pt.sqrt(k)
            nz = Y[Y > 0]
            eps = float(gamma_eps_frac * (nz.min() if nz.size else 1.0))
            Y_obs = np.where(Y > 0, Y, eps)
            pm.Gamma("y", mu=Lambda, sigma=sigma_obs, observed=Y_obs,
                     dims=("city", "bin"))
        else:  # "nb"
            phi = pm.HalfNormal("phi_disp", disp_sd)
            Y_int = np.rint(Y).astype(np.int64)
            pm.NegativeBinomial("y", mu=Lambda, alpha=phi, observed=Y_int,
                                dims=("city", "bin"))

    return model


def fit(
    data: LetterData,
    *,
    obs_form: str = "gamma",
    draws: int = 1000,
    tune: int = 1000,
    chains: int = 4,
    cores: int | None = None,
    target_accept: float = 0.99,
    random_seed: int | None = None,
    progressbar: bool = False,
    **model_kwargs,
):
    """Build and sample the letter-mass model.

    Args:
        data: Assembled :class:`LetterData`.
        obs_form: ``"gamma"`` or ``"nb"``.
        draws, tune, chains, target_accept: Sampler sizing (matches the
            inscription model defaults).
        cores: Chains to run in parallel (``None`` -> = chains).
        random_seed, progressbar: Passed to ``pm.sample``.
        **model_kwargs: Forwarded to :func:`build_model` (scales, disp_sd, ...).

    Returns:
        :class:`arviz.InferenceData` with the posterior.
    """
    model = build_model(data, obs_form=obs_form, **model_kwargs)
    with model:
        idata = pm.sample(
            draws=draws, tune=tune, chains=chains,
            cores=cores if cores is not None else chains,
            target_accept=target_accept, random_seed=random_seed,
            progressbar=progressbar, compute_convergence_checks=True,
        )
    return idata


def convergence_summary(idata, var_names=(
    "alpha_g", "sigma_g", "sigma_u", "sigma_v", "sigma_bu", "sigma_bv",
    "k_disp", "phi_disp", "z_g", "z_u", "z_v", "z_bu", "z_bv",
    "b_u", "b_v", "Lambda",
)) -> dict:
    """Summarise convergence: max R-hat, min bulk ESS, divergence count."""
    import arviz as az

    present = [v for v in var_names if v in idata.posterior]
    summ = az.summary(idata, var_names=present)
    return {
        "max_rhat": float(summ["r_hat"].max()),
        "min_ess_bulk": float(summ["ess_bulk"].min()),
        "n_divergences": (int(idata.sample_stats["diverging"].sum())
                          if "diverging" in idata.sample_stats else -1),
        "worst_rhat_param": str(summ["r_hat"].idxmax()),
        "worst_ess_param": str(summ["ess_bulk"].idxmin()),
    }


def gates_pass(conv: dict) -> bool:
    """Convergence gates: R-hat < 1.01, bulk ESS >= 400, 0 divergences."""
    return (
        conv["max_rhat"] < 1.01
        and conv["min_ess_bulk"] >= 400
        and conv["n_divergences"] == 0
    )
