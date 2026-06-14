#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h3b_drawwise.py — draw-wise (uncertainty-propagating) H3b engine.
=================================================================

Implements the H3b design of ``h3b-implementation-spec-2026-06-14.md`` (OSF
Amendment 04 §A5.6): replace the post-hoc identifiability *restriction* with
propagation of the cc-library deconvolution posterior into the deviation test.

Supersedes the median-based ``h3b_lib.py`` engine (2026-06-09 draft) on two axes:
its observed signal is the genuine-SPA **posterior** (8,000 draws/unit, emitted by
``run_refit.py --emit-draws``), and its source is the **cc-library refit**
(``runs/2026-06-13-cc-production-refit/``), not the reversed h2.1-launch-prep run.

For each unit × null the featureless-null Monte-Carlo envelope is built ONCE
(reusing the H1 sampler/fit unchanged); each posterior draw is then evaluated
against that fixed envelope, and the per-draw Timpson global-*p* distribution is
summarised as the marginal-*p* headline + P(deviation) companion + per-draw spread.
``selftest_faithful`` asserts the inlined envelope logic reproduces the library
envelope test bit-for-bit. Small helpers (``window_bin_indices``, ``holm_adjust``)
are reused from ``h3b_lib``.

Author / Date — Claude Code (Opus 4.8) on Shawn's brief, 2026-06-14. UK/Aus English.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

# --- reused primitives (no reimplementation) --------------------------------
ROOT = Path("/home/shawn/Code/inscriptions")
_PATHS = [
    ROOT / "runs/2026-04-25-h1-simulation/code",        # primitives, forward_fit
    ROOT / "runs/2026-06-07-h2.1-launch-prep/code",      # h2_lib
    ROOT / "runs/2026-06-13-cc-production-refit/code",    # refit_lib
    ROOT / "runs/2026-06-09-joint-identifiability/code",  # joint_lib (aligned_indicator)
    ROOT / "runs/2026-06-09-h3b/code",                    # h3b_lib helpers
]
for _p in _PATHS:
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import primitives as P        # noqa: E402
import forward_fit as FF      # noqa: E402
import h2_lib as H            # noqa: E402
import refit_lib as R         # noqa: E402
from h3b_lib import holm_adjust, window_bin_indices  # noqa: E402,F401  (reused helpers)

BIN_EDGES: np.ndarray = P.BIN_EDGES
BIN_CENTRES: np.ndarray = P.BIN_CENTRES
N_BINS = BIN_CENTRES.size
BRACKETS = P.BRACKETS

MASTER_SEED = 20260609
N_MC = 1000
ALPHA = 0.05
VARIANCE_FLOOR = 1e-10
ENV_START, ENV_END = -50.0, 350.0

ANTONINE_WINDOW = (165.0, 180.0)   # AD 165–180
CRISIS_WINDOW = (235.0, 284.0)     # AD 235–284 inclusive
GAP_THRESHOLD = 0.20               # retained only as a transparency annotation

# θ-sensitive units carrying the Amendment-04 §A5.6 soft reliability annotation.
SOFT_ANNOTATE = {"Moesia inferior", "Britannia"}
# Conservative cpl-3-Gaussian province reachability floor (prereg §6; spec OQ-3).
REACH_FLOOR_CPL = 1618


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def load_draws_normalised(name: str, draws_dir: Path) -> np.ndarray:
    """Genuine-SPA posterior draws, each normalised to sum 1 → ``(n_draws, 80)``."""
    z = np.load(draws_dir / f"{_safe(name)}-pgen.npz", allow_pickle=True)
    p = z["p_gen"].astype(np.float64)
    s = p.sum(axis=1, keepdims=True)
    s[s <= 0] = 1.0
    return p / s


def assemble_units(draws_dir: Path) -> list[dict[str, Any]]:
    """Reconstruct every cc-refit unit's intervals + n_eff + α annotation, and
    attach its posterior-draw path. Row membership is the refit's (refit_lib)."""
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    units = R.enumerate_refit_units()
    summary = json.loads(
        (ROOT / "runs/2026-06-13-cc-production-refit/outputs/refit-summary.json").read_text())
    alpha_by = {u["name"]: u for u in summary["units"]}

    out = []
    for unit in units:
        name = unit["name"]
        npz = draws_dir / f"{_safe(name)}-pgen.npz"
        if not npz.exists():
            continue
        sub = R.subset_for(df, unit, latin)
        nb = sub["nb"].to_numpy(dtype=float)
        na = sub["na"].to_numpy(dtype=float)
        cc = R.build_unit_cc_data(sub)
        n_eff = int(cc["n_rows"])
        meta = alpha_by.get(name, {})
        # Identifiability gap (transparency annotation only; the restriction is moot).
        f1f3 = float(cc.get("mass_aligned_frac", float("nan")))
        a_med = float(meta.get("alpha_median", float("nan")))
        out.append({
            "name": name, "unit_index": int(unit["unit_index"]),
            "kind": unit["kind"], "frame": unit["frame"], "tier": unit["tier"],
            "nb": nb, "na": na, "n_eff": n_eff, "n_raw": int(len(sub)),
            "alpha_median": a_med, "alpha_ci_lo": float(meta.get("alpha_ci_lo", np.nan)),
            "alpha_ci_hi": float(meta.get("alpha_ci_hi", np.nan)),
            "gap_annotation": f1f3 - a_med,
            "soft_annotated": name in SOFT_ANNOTATE,
            "reach_caveat": n_eff < REACH_FLOOR_CPL,
            "draws_path": npz,
        })
    out.sort(key=lambda u: u["unit_index"])
    return out


def raw_aoristic_counts(nb: np.ndarray, na: np.ndarray, n_eff: int) -> np.ndarray:
    """Raw (uncorrected) aoristic SPA scaled to ``n_eff`` integer counts (CPL fit
    target + raw-vs-corrected follow-up signal)."""
    spa = H.aoristic_spa(nb, na)
    tot = spa.sum()
    spa = spa / tot * n_eff if tot > 0 else spa
    return H.largest_remainder(spa)


# ---------------------------------------------------------------------------
# Fixed featureless-null envelope (once per unit × null)
# ---------------------------------------------------------------------------
def build_envelope(kind: str, unit: dict, rng: np.random.Generator,
                   n_mc: int = N_MC, cpl_target: np.ndarray | None = None) -> dict[str, Any]:
    """Fit null + build MC envelope, per-bin centre, and per-replicate out-counts.

    ``exp`` → forward-fit on the raw intervals + forward MC (FP-fix). Monotone, so
    on the humped real epigraphic curve it saturates (reported as a cross-check).
    ``cpl`` → CPL-3 fit to ``cpl_target`` (the OBSERVED corrected count SPA) + Poisson
    MC — the standard SPD self-referential null (matches the 2026-06-09 draft): the
    null tracks the smooth trend of the curve under test, so only *local* departures
    show. Fitting CPL to the raw corpus instead makes the whole correction read as a
    deviation and saturates — see DECISION-NEEDED-null-construction-2026-06-14.md."""
    nb, na, n_eff = unit["nb"], unit["na"], unit["n_eff"]
    mc = np.empty((n_mc, N_BINS), dtype=float)
    if kind == "exp":
        fit = FF.fit_null_exponential_forward(intervals=None, nb=nb, na=na,
                                              t_min=ENV_START, t_max=ENV_END)
        widths = na - nb
        for i in range(n_mc):
            mc[i] = FF.sample_null_spa_forward_exp(fit["b"], n_eff, widths, BIN_EDGES,
                                                   rng, t_min=ENV_START, t_max=ENV_END)
        fit_info = {"family": "exp", "b": float(fit["b"]),
                    "converged": bool(fit.get("converged", True))}
    elif kind == "cpl":
        if cpl_target is None:
            raise ValueError("cpl null requires cpl_target (the observed corrected count SPA)")
        params = P.fit_null_cpl(np.asarray(cpl_target, dtype=float), BIN_CENTRES,
                                k=3, n_restarts=4, seed=0)
        for i in range(n_mc):
            mc[i] = P.sample_null_spa(params, "cpl", BIN_CENTRES, rng)
        fit_info = {"family": "cpl", "knots": np.asarray(params["knots"]).tolist(),
                    "converged": bool(params.get("converged", True))}
    else:
        raise ValueError(f"unknown null kind {kind!r}")

    lo = np.quantile(mc, ALPHA / 2.0, axis=0)
    hi = np.quantile(mc, 1.0 - ALPHA / 2.0, axis=0)
    keep = mc.var(axis=0) >= VARIANCE_FLOOR
    mid = np.median(mc, axis=0)
    mc_out = (((mc < lo) | (mc > hi)) & keep[None, :]).sum(axis=1)
    return {"lo": lo, "hi": hi, "keep": keep, "mid": mid, "mc_out": mc_out,
            "n_eff": n_eff, "fit": fit_info, "n_bins_skipped": int((~keep).sum())}


# ---------------------------------------------------------------------------
# Draw-wise evaluation + aggregation
# ---------------------------------------------------------------------------
def eval_draws(draws_counts: np.ndarray, env: dict) -> tuple[np.ndarray, np.ndarray]:
    """Per-draw out-of-envelope count + per-draw global-*p* (plain-mean ``>=``,
    matching ``primitives.permutation_envelope_test``)."""
    out = (((draws_counts < env["lo"]) | (draws_counts > env["hi"]))
           & env["keep"][None, :]).sum(axis=1)
    p_d = (env["mc_out"][None, :] >= out[:, None]).mean(axis=1)
    return out, p_d


def aggregate(p_d: np.ndarray) -> dict[str, float]:
    lo, med, hi = (float(x) for x in np.percentile(p_d, [2.5, 50.0, 97.5]))
    return {"marginal_p": float(np.mean(p_d)),
            "p_deviation": float(np.mean(p_d < ALPHA)),
            "p_draw_lo": lo, "p_draw_med": med, "p_draw_hi": hi}


def probe_window(draws_counts: np.ndarray, env: dict,
                 window: tuple[float, float]) -> dict[str, Any]:
    """Signed, propagated reading of one probe window (two-sided P(deviation) +
    one-sided deficit/surplus probabilities + posterior of the windowed signed
    relative departure vs the null centre, with a descriptive bracket)."""
    idx = window_bin_indices(window)
    mask = np.zeros(N_BINS, dtype=bool)
    mask[idx] = True
    m = mask & env["keep"]
    if not m.any():
        return {"window": list(window), "in_window_kept_bins": 0,
                "p_window_dev": float("nan")}
    below = (draws_counts < env["lo"]) & m
    above = (draws_counts > env["hi"]) & m
    any_out = (below | above).any(axis=1)
    mid_w = env["mid"][m]
    mid_w = np.where(mid_w > 0, mid_w, np.nan)
    rel = (draws_counts[:, m] - mid_w) / mid_w
    dep = np.nanmean(rel, axis=1)
    d_lo, d_med, d_hi = (float(x) for x in np.nanpercentile(dep, [2.5, 50.0, 97.5]))
    return {
        "window": list(window),
        "in_window_kept_bins": int(m.sum()),
        "p_window_dev": float(any_out.mean()),
        "p_deficit": float(below.any(axis=1).mean()),
        "p_surplus": float(above.any(axis=1).mean()),
        "windowed_rel_departure_med": d_med,
        "windowed_rel_departure_lo": d_lo,
        "windowed_rel_departure_hi": d_hi,
        "descriptive_bracket": _describe_bracket(d_med),
    }


def _describe_bracket(rel: float) -> str:
    if rel is None or (isinstance(rel, float) and np.isnan(rel)):
        return "n/a"
    mag, sign = abs(rel), ("surplus" if rel > 0 else "deficit")
    if mag >= 1.0:
        return f"≥ doubling ({sign})"
    if mag >= 0.5:
        return f"≥ 50% ({sign})"
    if mag >= 0.2:
        return f"≥ 20% ({sign})"
    return f"< 20% ({sign}; sub-bracket)"


def inflate_draws(draws_norm: np.ndarray, lam: float) -> np.ndarray:
    """Coverage sensitivity (§A5.5): widen each draw about the posterior mean by
    ``lam`` (1 → identity), clip negatives, renormalise."""
    if lam == 1.0:
        return draws_norm
    mean = draws_norm.mean(axis=0, keepdims=True)
    infl = np.clip(mean + lam * (draws_norm - mean), 0.0, None)
    s = infl.sum(axis=1, keepdims=True)
    s[s <= 0] = 1.0
    return infl / s


# ---------------------------------------------------------------------------
# One-time faithfulness self-test vs the library envelope tests
# ---------------------------------------------------------------------------
def selftest_faithful(seed: int = 7) -> None:
    rng_nb = np.random.default_rng(123)
    nb = np.sort(rng_nb.uniform(-50, 300, size=400))
    na = nb + rng_nb.uniform(5, 80, size=400)
    unit = {"nb": nb, "na": na, "n_eff": 400}
    base = H.aoristic_spa(nb, na)
    obs = H.largest_remainder(base / base.sum() * 400).astype(float)

    env = build_envelope("exp", unit, np.random.default_rng(seed))
    _, p_mine = eval_draws(obs[None, :], env)
    ref = FF.forward_envelope_test(obs, env["fit"]["b"], na - nb, BIN_EDGES, N_MC,
                                   np.random.default_rng(seed), n=400, alpha=ALPHA,
                                   t_min=ENV_START, t_max=ENV_END)
    assert np.allclose(env["lo"], ref["lo_env"]) and np.allclose(env["hi"], ref["hi_env"]), \
        "exp envelope mismatch"
    assert abs(float(p_mine[0]) - ref["pval_global"]) < 1e-12, \
        f"exp pval mismatch {p_mine[0]} vs {ref['pval_global']}"

    env2 = build_envelope("cpl", unit, np.random.default_rng(seed), cpl_target=obs)
    _, p2 = eval_draws(obs[None, :], env2)
    params = P.fit_null_cpl(obs, BIN_CENTRES, k=3, n_restarts=4, seed=0)
    ref2 = P.permutation_envelope_test(obs, params, "cpl", BIN_CENTRES, N_MC,
                                       np.random.default_rng(seed), alpha=ALPHA)
    assert np.allclose(env2["lo"], ref2["lo_env"]) and np.allclose(env2["hi"], ref2["hi_env"]), \
        "cpl envelope mismatch"
    assert abs(float(p2[0]) - ref2["pval_global"]) < 1e-12, \
        f"cpl pval mismatch {p2[0]} vs {ref2['pval_global']}"
