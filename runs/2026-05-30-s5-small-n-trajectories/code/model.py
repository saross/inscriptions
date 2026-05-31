#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model.py — §5 small-N city-trajectory harness, Layer A single-city model.
=========================================================================

The single-city, no-pooling Poisson-process aoristic model — the likelihood
under test at the smoke stage. One model is built per city from its aoristic
matrix ``A`` (shape ``N x 16``).

Model (per city with ``N`` inscriptions, ``T = 16`` bins):

- Non-centred first-order random walk (RW1) for the log-rate *shape*::

      sigma   ~ HalfNormal(0.5)
      z_raw   ~ Normal(0, 1, shape=T)
      z       = cumsum(z_raw) * sigma
      s       = z - mean(z)          # zero-sum smooth deviation

- Overall log-level::

      alpha   ~ Normal(log(N / T), 1.0)

- Per-bin expected counts::

      log_lambda = alpha + s
      lam        = exp(log_lambda)   # shape T

- Likelihood (inhomogeneous-Poisson, interval-censored; ``pm.Potential``)::

      per_insc = A @ lam             # length N; each = sum_t a[i,t] * lam_t
      loglik   = -lam.sum() + log(per_insc).sum()
      pm.Potential("ll", loglik)

  This is ``-`` total intensity ``+`` the sum over inscriptions of the log of
  the intensity integrated over each inscription's allowed bins. Wide-interval
  inscriptions inform the level not the shape; narrow ones pin the shape.

Sampling defaults: 4 chains, tune 1000, draws 1000, ``target_accept = 0.99``.

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import numpy as np
import pymc as pm
import pytensor.tensor as pt

T_BINS: int = 16  # DEFAULT number of temporal bins (25y grid); see build_model.


def build_model(A: np.ndarray, *, level_sd: float = 1.0,
                sigma_sd: float = 0.5) -> pm.Model:
    """Build the single-city no-pooling Poisson-aoristic model.

    The number of bins ``T`` is INFERRED from ``A.shape[1]`` (16 at the 25y
    grid, 8 at the 50y grid), so the same model serves both bin widths.

    Args:
        A: Aoristic weight matrix, shape ``(N, T)``; ``A[i, t]`` is the fraction
            of bin ``t`` covered by inscription ``i``'s clipped interval (in
            ``[0, 1]``). ``T`` is read from the matrix, not assumed.
        level_sd: Prior SD on the overall log-level ``alpha`` (default 1.0).
        sigma_sd: Scale of the HalfNormal prior on the RW innovation SD
            (default 0.5).

    Returns:
        An unsampled :class:`pymc.Model`. Deterministics ``lam`` (per-bin
        expected counts) and ``s`` (zero-sum log-rate shape) are registered for
        posterior extraction.

    Raises:
        ValueError: If ``A`` is not 2-D, contains negative entries, or has any
            inscription with zero total weight (which would make
            ``log(per_insc)`` undefined).
    """
    A = np.asarray(A, dtype=np.float64)
    if A.ndim != 2:
        raise ValueError(f"A must be 2-D (N, T); got shape {A.shape}.")
    T = A.shape[1]
    n_insc = A.shape[0]
    if n_insc == 0:
        raise ValueError("A has zero rows (no inscriptions).")
    if np.any(A < 0):
        raise ValueError("A contains negative aoristic weights.")
    row_mass = A.sum(axis=1)
    if np.any(row_mass <= 0):
        n_bad = int((row_mass <= 0).sum())
        raise ValueError(
            f"{n_bad} inscription(s) have zero total aoristic mass; "
            "log(per_insc) would be undefined."
        )

    # log(N / T) anchors alpha at the flat-rate level (counts spread evenly).
    alpha_mu = float(np.log(n_insc / T))

    with pm.Model() as model:
        a_data = pm.Data("A", A)  # (N, T) constant aoristic design matrix.

        # --- Non-centred RW1 shape (zero-sum) -------------------------------
        sigma = pm.HalfNormal("sigma", sigma_sd)
        z_raw = pm.Normal("z_raw", 0.0, 1.0, shape=T)
        z = pt.cumsum(z_raw) * sigma
        s = pm.Deterministic("s", z - pt.mean(z))  # zero-sum smooth deviation.

        # --- Overall log-level ----------------------------------------------
        alpha = pm.Normal("alpha", alpha_mu, level_sd)

        # --- Per-bin expected counts ----------------------------------------
        log_lambda = alpha + s
        lam = pm.Deterministic("lam", pt.exp(log_lambda))  # (T,)

        # --- Poisson-process aoristic likelihood (pm.Potential) -------------
        per_insc = pt.dot(a_data, lam)                  # (N,) = sum_t a[i,t]*lam_t
        loglik = -pt.sum(lam) + pt.sum(pt.log(per_insc))
        pm.Potential("ll", loglik)

    return model


def fit(A: np.ndarray, *, draws: int = 1000, tune: int = 1000,
        chains: int = 4, cores: int | None = None,
        target_accept: float = 0.99,
        random_seed: int | None = None, progressbar: bool = False,
        **model_kwargs):
    """Build and sample the single-city model.

    Args:
        A: Aoristic matrix ``(N, T_BINS)``.
        draws: Posterior draws per chain.
        tune: Tuning (warm-up) steps per chain.
        chains: Number of chains.
        cores: Chains to run in parallel (``None`` -> pymc default = chains).
            Set explicitly (e.g. ``cores=2``) when many fits run concurrently
            under a process pool, so each fit's chain parallelism is capped and
            the pool — not pymc — controls total core use.
        target_accept: NUTS target acceptance probability. Default 0.99: the
            non-centred RW1 has a mild funnel near ``sigma -> 0`` that produces
            occasional divergences at 0.95; raising to 0.99 clears them with no
            change to recovery quality (sim-recovery gate, 2026-05-30). This is
            a careful-sampler setting, NOT a relaxation of any convergence gate.
        random_seed: Seed for reproducibility.
        progressbar: Whether to show the sampler progress bar.
        **model_kwargs: Forwarded to :func:`build_model` (e.g. ``level_sd``).

    Returns:
        An :class:`arviz.InferenceData` object with the posterior.
    """
    model = build_model(A, **model_kwargs)
    with model:
        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=cores if cores is not None else chains,
            target_accept=target_accept,
            random_seed=random_seed,
            progressbar=progressbar,
            compute_convergence_checks=True,
        )
    return idata


def convergence_summary(idata, var_names=("alpha", "sigma", "z_raw", "lam")) -> dict:
    """Summarise convergence: max R-hat, min bulk ESS, divergence count.

    Args:
        idata: Posterior :class:`arviz.InferenceData`.
        var_names: Variables to include in the R-hat / ESS scan.

    Returns:
        Dict with ``max_rhat``, ``min_ess_bulk``, ``n_divergences``, and the
        per-variable worst offenders.
    """
    import arviz as az

    present = [v for v in var_names if v in idata.posterior]
    summ = az.summary(idata, var_names=present)
    max_rhat = float(summ["r_hat"].max())
    min_ess = float(summ["ess_bulk"].min())
    worst_rhat_row = summ["r_hat"].idxmax()
    worst_ess_row = summ["ess_bulk"].idxmin()
    n_div = int(idata.sample_stats["diverging"].sum()) \
        if "diverging" in idata.sample_stats else -1
    return {
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess,
        "n_divergences": n_div,
        "worst_rhat_param": str(worst_rhat_row),
        "worst_ess_param": str(worst_ess_row),
    }


def gates_pass(conv: dict) -> bool:
    """Apply the convergence gates: R-hat < 1.01, bulk ESS >= 400, 0 divergences."""
    return (
        conv["max_rhat"] < 1.01
        and conv["min_ess_bulk"] >= 400
        and conv["n_divergences"] == 0
    )
