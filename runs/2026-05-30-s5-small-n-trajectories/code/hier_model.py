#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hier_model.py — §5 small-N city-trajectory harness, Layer A HIERARCHICAL model.
===============================================================================

Partial-pooling extension of the validated single-city Poisson-process aoristic
model (``model.py``). Cities are pooled within provinces, provinces toward the
global trajectory, so small-N city trajectories shrink toward their province
(and singleton-province cities shrink directly toward the global trajectory) —
the mechanism that makes small-N estimation honest (spec §4).

For city ``c`` in province ``p(c)``, latent log-rate over ``T = 16`` bins::

    log lambda[c, t] = alpha_g            (global level intercept)
                     + g_shape[t]         (global trajectory shape, zero-sum/t)
                     + b_u[p(c)]          (province level offset, ~0)
                     + u_shape[p(c), t]   (province shape deviation, zero-sum/t)
                     + b_v[c]             (city level offset, ~0)
                     + v_shape[c, t]      (city shape deviation, zero-sum/t)

Parameterisation (chosen for identifiability; stated explicitly for review):

- **Level / shape split.** Each tier's TIME-VARYING part is made zero-sum over
  the 16 bins (a pure *shape* deviation that carries no level), and the LEVEL is
  carried separately by additive intercepts. Without this split the additive
  decomposition ``g + u + v`` is only weakly identified (any constant can move
  between tiers); zero-sum shapes + level intercepts make it clean (the brief's
  recommended fix).
    - ``alpha_g`` is the single global level, anchored at the empire-level mean
      log per-city total (``log(mean_c N_c / T)``) with prior SD ``level_sd``.
    - ``b_u[p] ~ Normal(0, sigma_bu)`` and ``b_v[c] ~ Normal(0, sigma_bv)`` are
      *level offsets*, shrunk toward 0 by tight-ish HalfNormal-scaled normals so
      most of the level lives in ``alpha_g`` and the offsets only absorb genuine
      between-province / between-city level differences. This is the partial
      pooling of LEVEL (spec §4: "the full Poisson form pools level as well as
      shape").

- **Shape tiers (non-centred RW1, zero-sum over time).** For each tier the raw
  innovations are ``Normal(0, 1)``; the random walk is ``cumsum`` of the
  innovations times the tier scale; then the tier's per-unit walk is centred to
  zero mean over time. This is the 2026-05-24 F3 non-centred lesson applied to
  every tier.
    - Global: ``z_g ~ Normal(0,1, T)``; ``g_shape = centre(cumsum(z_g) * sigma_g)``.
    - Province: ``z_u ~ Normal(0,1, [P_ns, T])``; per province
      ``u_shape[p] = centre(cumsum(z_u[p]) * sigma_u)``; defined only for
      NON-SINGLETON provinces (``P_ns`` of them). Singleton provinces have no
      ``u`` tier (their single city pools straight to global via ``v``).
    - City: ``z_v ~ Normal(0,1, [C, T])``; per city
      ``v_shape[c] = centre(cumsum(z_v[c]) * sigma_v)``.

- **Scales.** ``sigma_g ~ HalfNormal(s_g)``, ``sigma_u ~ HalfNormal(s_u)``,
  ``sigma_v ~ HalfNormal(s_v)`` (log-rate scale; learnt, not fixed). The
  HalfNormal *scales* ``s_g, s_u, s_v`` are the hyperprior knobs pinned by the
  prior-predictive check (``prior_predictive.py``). Level-offset scales
  ``sigma_bu ~ HalfNormal(s_bu)``, ``sigma_bv ~ HalfNormal(s_bv)``.

- **Singletons.** Provinces with exactly one TARGET city in the subset: the
  province tier is unidentified, so it is dropped entirely (no ``u_shape`` row,
  no ``b_u`` entry — both fixed at 0). The city's ``v_shape`` + ``b_v`` then
  carry its full deviation toward the GLOBAL trajectory (spec §4 singleton rule).

Likelihood — the SAME validated Poisson-process aoristic ``pm.Potential`` as
``model.py``, summed over cities, VECTORISED across all inscriptions:

- All cities' aoristic rows are concatenated into one big ``(N_total, T)``
  design matrix ``A_all``; a parallel ``insc_city`` index maps each row to its
  city. Per-inscription intensity is ``sum_t A_all[i,t] * lam[city(i), t]``,
  formed by gathering each row's city ``lam`` and an element-wise row dot.
- Total log-likelihood ``= - sum_{c,t} lam[c,t] + sum_i log(per_insc[i])`` — the
  city-summed version of ``model.py``'s ``-lam.sum() + log(A@lam).sum()``.

Sampling defaults match ``model.py``: 4 chains, ``target_accept = 0.99`` (the
non-centred RW1 funnel needs it).

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
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

T_BINS: int = dp.N_BINS  # 16


# --------------------------------------------------------------------------- #
# Subset assembly: turn a list of city names into vectorised model inputs.
# --------------------------------------------------------------------------- #

@dataclass
class HierData:
    """Vectorised inputs for the hierarchical model, assembled from a subset.

    Attributes:
        cities: City names, in model index order (``c = 0..C-1``).
        provinces: Province name for each city (parallel to ``cities``).
        N: Per-city inscription count (parallel to ``cities``).
        A_all: Concatenated aoristic matrix ``(N_total, T)`` over all cities.
        insc_city: ``(N_total,)`` int array; city index of each inscription row.
        city_prov: ``(C,)`` int array; province index (into ``prov_names``) of
            each city, or ``-1`` for cities in a singleton province (no u tier).
        prov_u_row: ``(C,)`` int array; row of ``u_shape`` used by each city, or
            ``-1`` if the city is in a singleton province (u contributes 0).
        prov_names: Province names that HAVE a u tier (non-singleton), in row
            order of ``u_shape`` / ``b_u``.
        singleton_provs: Province names with exactly one city in the subset.
        anchor_n_mean: Mean per-city N over the subset (anchors ``alpha_g``).
    """

    cities: list[str]
    provinces: list[str]
    N: np.ndarray
    A_all: np.ndarray
    insc_city: np.ndarray
    city_prov: np.ndarray
    prov_u_row: np.ndarray
    prov_names: list[str]
    singleton_provs: list[str]
    anchor_n_mean: float
    city_A: dict[str, np.ndarray] = field(default_factory=dict)


def assemble(out_dir: Path, cities: list[str]) -> HierData:
    """Load cached per-city bundles and build vectorised hierarchical inputs.

    Args:
        out_dir: Dataprep cache directory.
        cities: City names to include in the subset (must be cached).

    Returns:
        A :class:`HierData` with concatenated design matrix and index arrays.

    Raises:
        ValueError: If any city has zero-mass inscriptions or duplicate names.
    """
    if len(set(cities)) != len(cities):
        raise ValueError("Duplicate city names in subset.")

    prov_of: dict[str, str] = {}
    A_by_city: dict[str, np.ndarray] = {}
    N_list: list[int] = []
    for city in cities:
        b = dp.load_city(out_dir, city)
        A = np.asarray(b["A"], dtype=np.float64)
        if A.ndim != 2 or A.shape[1] != T_BINS:
            raise ValueError(f"{city}: A must be (N, {T_BINS}); got {A.shape}.")
        if np.any(A.sum(axis=1) <= 0):
            raise ValueError(f"{city}: has zero-mass inscription(s).")
        prov_of[city] = b["province"]
        A_by_city[city] = A
        N_list.append(A.shape[0])

    provinces = [prov_of[c] for c in cities]
    N = np.array(N_list, dtype=np.int64)

    # Identify singletons: provinces with exactly one city in THIS subset.
    from collections import Counter
    prov_counts = Counter(provinces)
    singleton_provs = sorted(p for p, k in prov_counts.items() if k == 1)
    # Non-singleton provinces get a u tier, in sorted order for determinism.
    u_provs = sorted(p for p, k in prov_counts.items() if k > 1)
    u_row_of = {p: i for i, p in enumerate(u_provs)}

    city_prov = np.array(
        [u_row_of.get(p, -1) for p in provinces], dtype=np.int64
    )
    prov_u_row = city_prov.copy()  # same mapping; -1 for singleton-province cities

    # Concatenate aoristic rows and build the inscription->city index.
    A_blocks, insc_city = [], []
    for ci, city in enumerate(cities):
        A = A_by_city[city]
        A_blocks.append(A)
        insc_city.append(np.full(A.shape[0], ci, dtype=np.int64))
    A_all = np.concatenate(A_blocks, axis=0)
    insc_city = np.concatenate(insc_city)

    anchor_n_mean = float(N.mean())

    return HierData(
        cities=list(cities),
        provinces=provinces,
        N=N,
        A_all=A_all,
        insc_city=insc_city,
        city_prov=city_prov,
        prov_u_row=prov_u_row,
        prov_names=u_provs,
        singleton_provs=singleton_provs,
        anchor_n_mean=anchor_n_mean,
        city_A=A_by_city,
    )


# --------------------------------------------------------------------------- #
# Model builder.
# --------------------------------------------------------------------------- #

def build_model(
    data: HierData,
    *,
    s_g: float = 0.5,
    s_u: float = 0.3,
    s_v: float = 0.3,
    s_bu: float = 0.5,
    s_bv: float = 0.5,
    level_sd: float = 1.0,
) -> pm.Model:
    """Build the monolithic hierarchical Poisson-aoristic model.

    Args:
        data: Assembled :class:`HierData` for the subset.
        s_g, s_u, s_v: HalfNormal scales on the global / province / city RW1
            innovation SDs (the hyperprior knobs pinned by prior-predictive).
        s_bu, s_bv: HalfNormal scales on the province / city LEVEL-offset SDs.
        level_sd: Prior SD on the global level intercept ``alpha_g``.

    Returns:
        An unsampled :class:`pymc.Model`. Registers Deterministics ``g_shape``,
        ``u_shape`` (non-singleton provinces), ``v_shape``, ``log_lam`` and
        ``lam`` (shape ``(C, T)``) for posterior extraction.
    """
    C = len(data.cities)
    P = len(data.prov_names)        # number of non-singleton provinces (u tiers)
    T = T_BINS

    alpha_mu = float(np.log(max(data.anchor_n_mean, 1.0) / T))

    coords = {
        "city": list(data.cities),
        "bin": list(range(T)),
        "prov": list(data.prov_names),
    }

    with pm.Model(coords=coords) as model:
        A_all = pm.Data("A_all", data.A_all)               # (N_total, T)
        insc_city = pm.Data("insc_city", data.insc_city)   # (N_total,)
        prov_u_row = pm.Data("prov_u_row", data.prov_u_row)  # (C,), -1 if singleton

        # --- Global level (anchored) ----------------------------------------
        alpha_g = pm.Normal("alpha_g", alpha_mu, level_sd)

        # --- Global shape: non-centred RW1, zero-sum over time ---------------
        sigma_g = pm.HalfNormal("sigma_g", s_g)
        z_g = pm.Normal("z_g", 0.0, 1.0, dims="bin")
        g_walk = pt.cumsum(z_g) * sigma_g
        g_shape = pm.Deterministic(
            "g_shape", g_walk - pt.mean(g_walk), dims="bin"
        )

        # --- Province shape + level offset (non-singleton provinces only) ----
        sigma_u = pm.HalfNormal("sigma_u", s_u)
        sigma_bu = pm.HalfNormal("sigma_bu", s_bu)
        if P > 0:
            z_u = pm.Normal("z_u", 0.0, 1.0, dims=("prov", "bin"))
            u_walk = pt.cumsum(z_u, axis=1) * sigma_u            # (P, T)
            u_shape = pm.Deterministic(
                "u_shape",
                u_walk - pt.mean(u_walk, axis=1, keepdims=True),
                dims=("prov", "bin"),
            )
            # Non-centred level offset: b_u = z_bu * sigma_bu. Centred
            # Normal(0, sigma_bu) funnels when sigma_bu -> 0; non-centring
            # removes the level-tier funnel (the 2026-05-30 smoke divergence
            # diagnosis — divergences localised on alpha_g / b_v[Puteoli]).
            z_bu = pm.Normal("z_bu", 0.0, 1.0, dims="prov")
            b_u = pm.Deterministic("b_u", z_bu * sigma_bu, dims="prov")  # (P,)
            # Pad a zero row at index -1 so singleton cities gather 0.
            u_shape_pad = pt.concatenate([u_shape, pt.zeros((1, T))], axis=0)
            b_u_pad = pt.concatenate([b_u, pt.zeros((1,))], axis=0)
        else:
            u_shape_pad = pt.zeros((1, T))
            b_u_pad = pt.zeros((1,))

        # Gather each city's province contribution (row -1 -> the padded zero).
        city_u_shape = u_shape_pad[prov_u_row]                    # (C, T)
        city_b_u = b_u_pad[prov_u_row]                            # (C,)

        # --- City shape + level offset (all cities) -------------------------
        sigma_v = pm.HalfNormal("sigma_v", s_v)
        sigma_bv = pm.HalfNormal("sigma_bv", s_bv)
        z_v = pm.Normal("z_v", 0.0, 1.0, dims=("city", "bin"))
        v_walk = pt.cumsum(z_v, axis=1) * sigma_v                 # (C, T)
        v_shape = pm.Deterministic(
            "v_shape",
            v_walk - pt.mean(v_walk, axis=1, keepdims=True),
            dims=("city", "bin"),
        )
        # Non-centred city level offset (same funnel fix as b_u).
        z_bv = pm.Normal("z_bv", 0.0, 1.0, dims="city")
        b_v = pm.Deterministic("b_v", z_bv * sigma_bv, dims="city")  # (C,)

        # --- Assemble per-city log-rate -------------------------------------
        #   log_lam[c, t] = alpha_g + g_shape[t]
        #                 + b_u[p(c)] + u_shape[p(c), t]
        #                 + b_v[c]    + v_shape[c, t]
        log_lam = pm.Deterministic(
            "log_lam",
            alpha_g
            + g_shape[None, :]
            + city_b_u[:, None]
            + city_u_shape
            + b_v[:, None]
            + v_shape,
            dims=("city", "bin"),
        )
        lam = pm.Deterministic("lam", pt.exp(log_lam), dims=("city", "bin"))

        # --- Vectorised Poisson-process aoristic likelihood -----------------
        # Per inscription i (belonging to city c=insc_city[i]):
        #   per_insc[i] = sum_t A_all[i, t] * lam[c, t]
        lam_per_insc = lam[insc_city]                  # (N_total, T) gather
        per_insc = pt.sum(A_all * lam_per_insc, axis=1)  # (N_total,)
        loglik = -pt.sum(lam) + pt.sum(pt.log(per_insc))
        pm.Potential("ll", loglik)

    return model


def fit(
    data: HierData,
    *,
    draws: int = 1000,
    tune: int = 1000,
    chains: int = 4,
    target_accept: float = 0.99,
    random_seed: int | None = None,
    progressbar: bool = False,
    **model_kwargs,
):
    """Build and sample the hierarchical model.

    Args:
        data: Assembled :class:`HierData`.
        draws, tune, chains: Sampler sizing.
        target_accept: NUTS target acceptance (default 0.99; matches ``model.py``
            — the non-centred RW1 funnel needs it).
        random_seed: Seed.
        progressbar: Progress bar toggle.
        **model_kwargs: Forwarded to :func:`build_model` (the hyperprior scales).

    Returns:
        :class:`arviz.InferenceData` with the posterior.
    """
    model = build_model(data, **model_kwargs)
    with model:
        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=progressbar,
            compute_convergence_checks=True,
        )
    return idata


def convergence_summary(idata, var_names=(
    "alpha_g", "sigma_g", "sigma_u", "sigma_v", "sigma_bu", "sigma_bv",
    "z_g", "z_u", "z_v", "z_bu", "z_bv", "b_u", "b_v", "lam",
)) -> dict:
    """Summarise convergence: max R-hat, min bulk ESS, divergence count."""
    import arviz as az

    present = [v for v in var_names if v in idata.posterior]
    summ = az.summary(idata, var_names=present)
    max_rhat = float(summ["r_hat"].max())
    min_ess = float(summ["ess_bulk"].min())
    n_div = int(idata.sample_stats["diverging"].sum()) \
        if "diverging" in idata.sample_stats else -1
    return {
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess,
        "n_divergences": n_div,
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
