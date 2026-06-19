#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
content_residual.py — Amendment 01 §A5.4 content residual (inter-measure delta).
================================================================================

Computes the **content residual** — the pre-specified, exploratory, descriptive
"inter-measure delta" of OSF Amendment 01 §A5.4 — and the two-dimensional
residual-space map cross-tabulating it against the **scaling residual** (the
D12 SAMOC log-residual of inscription count on population).

The pre-specified analysis (Amendment 01 §A5.4, verbatim definition)
-------------------------------------------------------------------
    "For the cross-sectional city set, fit `log(letter_mass) ~
     log(inscription_count)` across cities; the per-city residual is the content
     residual (positive = more content per act than the corpus norm; negative =
     less). The project thereby has a two-dimensional residual space:
     scaling residual (observed inscriptions minus what population predicts) ×
     content residual (observed content minus what inscription count predicts)."

    "Status. Exploratory and descriptive. No pre-committed threshold and no
     confirmatory verdict attach to the delta; it is a novel quantity and is
     reported as a map/descriptive characterisation and cross-tabulated against
     the scaling residual."

This run is therefore **DESCRIPTIVE**: it reports the OLS fit, the per-city
content residuals, the two-dimensional residual-space map, and the cross-tab
(quadrant counts + Spearman/Pearson association) against the scaling residual.
**No threshold, no pass/fail verdict.**

Cross-sectional city set (the frame)
------------------------------------
The lodged primary cross-sectional frame is the **Latin-speaking provinces**
(OSF Amendment 02; Decision 36) — 817 cities, 39 provinces. We compute the
content residual and the scaling residual on this same Latin city set so the
two-dimensional residual space is internally coherent (one residual pair per
city). The empire-wide (1,044-city) frame is built alongside as a secondary /
context map (the D12 sensitivity itself was run on the all-provinces frame —
see the provenance note in the REPORT).

Inputs (all regenerated from raw, never read from a prior result)
-----------------------------------------------------------------
- Per-city LETTER MASS + inscription_count: regenerated from raw LIRE v3.0 via
  the audited H9 machinery (`runs/2026-06-18-h9-letter-mass-h3a/code/h9_common`).
  letter_mass = summed Latin-A–Z `letter_count_conservative` (Amendment 01
  §A5.1); inscription_count = the city's date-window-filtered, Hanson-matched,
  Rome-excluded row count. Both built together for the same cities, so the
  content-residual fit needs no join.
- Per-city log_pop (Hanson population): carried in the same H9 frame.
- The scaling residual uses the **D12 SAMOC construction**
  (`runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py`): a pooled
  negative-binomial power-law `insc ~ NB(exp(a + β·log_pop), φ)`, then
  r_c = log(insc_c) − (â + β̂·log_pop_c) on posterior medians.

Outputs (`outputs/`)
--------------------
- `content-residual-results.json` — OLS fit, per-frame residual summaries, the
  cross-tab (quadrant counts, Spearman/Pearson), seeds, input sha256, provenance.
- `content-residual-per-city.csv` — per-city: city, province, log_pop,
  log_inscription_count, log_letter_mass, content_residual, scaling_residual,
  quadrant (Latin primary frame).
- `content-residual-space-map.png` — the 2-D residual-space scatter (scaling ×
  content), Latin primary + empire context panels.

Status / verdict logic
-----------------------
DESCRIPTIVE — no verdict. The deliverable is the map + the cross-tab read-off.
A01 §A5.4 explicitly: "No pre-committed threshold and no confirmatory verdict."

Reproduce
---------
    cd /home/shawn/Code/inscriptions
    .venv/bin/python runs/2026-06-20-a01-content-residual/code/content_residual.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-20, on Shawn's pre-write-up uplift brief.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

# Force pytensor's pure-Python (no-C-compile) backend BEFORE importing pymc.
# This run host lacks the Python development headers (`Python.h`), so pytensor's
# default C backend cannot compile. The scaling-residual model is a tiny
# 3-parameter pooled NBR, so the pure-Python backend's slower sampling is a
# non-issue here. Set in-script (not just via the environment) so reproduction
# is deterministic without remembering an env var.
os.environ.setdefault("PYTENSOR_FLAGS", "cxx=")

import matplotlib

matplotlib.use("Agg")  # headless; write PNG without a display.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
from scipy import stats

# ---------------------------------------------------------------------------
# Paths — resolved relative to this module so the run is portable.
# ---------------------------------------------------------------------------
THIS = Path(__file__).resolve()
RUN_DIR = THIS.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
OUT_DIR = RUN_DIR / "outputs"

# The audited H9 data-prep machinery (regenerates per-city letter mass +
# inscription_count from raw LIRE). Imported, not copied — the H9 module is the
# canonical letter-mass builder and is read-only here.
H9_CODE = PROJECT_ROOT / "runs" / "2026-06-18-h9-letter-mass-h3a" / "code"
sys.path.insert(0, str(H9_CODE))
import h9_common as H9  # noqa: E402  (path inserted above)

RAW_LIRE = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"

# Seeds (per-run-date convention; the scaling-residual NBR is the only
# stochastic step).
SEED = 20_260_620


def _sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file (provenance anchor)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_letter_mass_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Regenerate the per-city letter-mass frames (Latin primary + empire) from
    raw LIRE via the audited H9 machinery.

    Returns
    -------
    (latin, empire) : tuple[pd.DataFrame, pd.DataFrame]
        Each carries per-city `letter_mass`, `inscription_count`, `log_pop`,
        `province`, etc. Latin = lodged primary cross-section (Amendment 02);
        empire = secondary / context.
    """
    filtered = H9.load_filtered_lire()
    passed, observed, msgs = H9.check_row_counts(filtered)
    print("[content-residual] row-level sanity vs prereg targets:")
    for line in msgs:
        print(line)
    if not passed:
        raise RuntimeError(
            "HARD-STOP: filtered LIRE row counts diverge from prereg targets; "
            "the letter-mass frame is not the lodged one. Aborting."
        )

    # PRIMARY content measure: conservative Latin-A–Z letter count (A01 §A5.1).
    col = "letter_count_conservative"
    empire, _ = H9.build_empire_frame(filtered, col)
    latin = H9.build_latin_frame(filtered, col)
    print(f"[content-residual] Latin (primary): {len(latin)} cities, "
          f"{latin['province'].nunique()} provinces")
    print(f"[content-residual] empire (context): {len(empire)} cities, "
          f"{empire['province'].nunique()} provinces")
    return latin, empire


def content_residual_ols(cities: pd.DataFrame) -> dict:
    """A01 §A5.4: OLS fit `log(letter_mass) ~ log(inscription_count)`; the
    per-city residual is the content residual.

    Cities with `letter_mass == 0` (inscriptions present but no readable Latin
    A–Z letters) have an undefined `log(letter_mass)` and are dropped from the
    fit, with the count reported (the same treatment H9's OLS log-log comparator
    applies to zero-mass cities).

    Adds two columns to `cities` IN PLACE for the retained rows:
    `log_inscription_count`, `log_letter_mass`, `content_residual`. Returns a
    summary dict (slope, intercept, R², n, dropped, residual summary).
    """
    fit_mask = cities["letter_mass"] > 0
    n_dropped = int((~fit_mask).sum())
    sub = cities.loc[fit_mask].copy()

    x = np.log(sub["inscription_count"].to_numpy(dtype=float))
    y = np.log(sub["letter_mass"].to_numpy(dtype=float))
    lr = stats.linregress(x, y)
    resid = y - (lr.intercept + lr.slope * x)

    cities["log_inscription_count"] = np.nan
    cities["log_letter_mass"] = np.nan
    cities["content_residual"] = np.nan
    cities.loc[fit_mask, "log_inscription_count"] = x
    cities.loc[fit_mask, "log_letter_mass"] = y
    cities.loc[fit_mask, "content_residual"] = resid

    return {
        "model": "OLS log(letter_mass) ~ log(inscription_count)",
        "slope": float(lr.slope),
        "intercept": float(lr.intercept),
        "slope_se": float(lr.stderr),
        "r_squared": float(lr.rvalue ** 2),
        "n_fitted": int(fit_mask.sum()),
        "n_zero_mass_dropped": n_dropped,
        "residual_summary": {
            "mean": float(resid.mean()),  # ~0 by OLS construction
            "sd": float(resid.std(ddof=1)),
            "min": float(resid.min()),
            "p05": float(np.percentile(resid, 5)),
            "median": float(np.median(resid)),
            "p95": float(np.percentile(resid, 95)),
            "max": float(resid.max()),
        },
    }


def scaling_residual_d12(cities: pd.DataFrame) -> dict:
    """Compute the D12 SAMOC scaling residual on this city set.

    Mirrors `runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py`
    Stages 1–2 exactly: pooled NBR power-law `insc ~ NB(exp(a + β·log_pop), φ)`,
    then `r_c = log(insc_c) − (â + β̂·log_pop_c)` on posterior medians. (The D12
    Stage-3 within-between partition is NOT re-run here; only the per-city
    scaling residual is needed for the cross-tab.)

    Adds a `scaling_residual` column to `cities` IN PLACE (every city has ≥1
    inscription, so the log is always defined). Returns the pooled-fit summary.
    """
    y = cities["inscription_count"].to_numpy(dtype=int)
    lp = cities["log_pop"].to_numpy(dtype=float)
    lp_c = lp - lp.mean()  # centre for sampling; fold back into a (D12 convention)
    with pm.Model():
        a_c = pm.Normal("a_c", mu=0.0, sigma=5.0)
        beta = pm.Normal("beta", mu=0.0, sigma=1.0)
        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        mu = pm.math.exp(a_c + beta * lp_c)
        pm.NegativeBinomial("y", mu=mu, alpha=1.0 / inv_disp, observed=y)
        idata = pm.sample(draws=1500, tune=2000, chains=4, target_accept=0.95,
                          random_seed=SEED, progressbar=False,
                          return_inferencedata=True)
    post = idata.posterior
    beta_med = float(post["beta"].median())
    a_c_med = float(post["a_c"].median())
    a_med = a_c_med - beta_med * lp.mean()  # uncentre
    resid = np.log(y.astype(float)) - (a_med + beta_med * lp)  # SAMOC log residual
    cities["scaling_residual"] = resid

    import arviz as az
    summ = az.summary(idata, var_names=["a_c", "beta", "inv_dispersion"])
    return {
        "model": "pooled NBR power-law insc ~ NB(exp(a + beta*log_pop), phi); "
                 "SAMOC log residual (D12 construction)",
        "beta_median": beta_med,
        "a_median": a_med,
        "max_rhat": float(summ["r_hat"].max()),
        "min_ess_bulk": float(summ["ess_bulk"].min()),
        "n_divergences": int(idata.sample_stats["diverging"].sum()),
    }


def crosstab(cities: pd.DataFrame) -> dict:
    """Cross-tabulate the content residual against the scaling residual.

    Both residuals are mean-~0 by construction; the sign split is the natural
    quadrant boundary (A01 §A5.4 — positive = above the corpus norm). Reports
    quadrant counts + the Spearman and Pearson association between the two
    residuals (on cities present in BOTH residuals — i.e. letter_mass > 0).
    """
    sub = cities.dropna(subset=["content_residual", "scaling_residual"]).copy()
    cr = sub["content_residual"].to_numpy()
    sr = sub["scaling_residual"].to_numpy()
    sub["quadrant"] = np.where(
        sr >= 0,
        np.where(cr >= 0, "Q1: hi-scaling, hi-content", "Q4: hi-scaling, lo-content"),
        np.where(cr >= 0, "Q2: lo-scaling, hi-content", "Q3: lo-scaling, lo-content"),
    )
    cities.loc[sub.index, "quadrant"] = sub["quadrant"]
    sp = stats.spearmanr(sr, cr)
    pr = stats.pearsonr(sr, cr)
    return {
        "n": int(len(sub)),
        "quadrant_counts": {k: int(v) for k, v in sub["quadrant"].value_counts().items()},
        "spearman_rho": float(sp.statistic),
        "spearman_p": float(sp.pvalue),
        "pearson_r": float(pr.statistic),
        "pearson_p": float(pr.pvalue),
        "note": "DESCRIPTIVE — no threshold, no verdict (A01 §A5.4). Association "
                "reported to characterise the residual space, not to test a hypothesis.",
    }


def make_figure(latin: pd.DataFrame, empire: pd.DataFrame,
                latin_xtab: dict, empire_xtab: dict, path: Path) -> None:
    """Two-panel residual-space map: Latin primary (left) + empire context (right)."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), sharex=False, sharey=False)
    for ax, frame, xtab, title in (
        (axes[0], latin, latin_xtab, "Latin primary (817-city cross-section)"),
        (axes[1], empire, empire_xtab, "Empire context (1,044-city)"),
    ):
        sub = frame.dropna(subset=["content_residual", "scaling_residual"])
        ax.axhline(0, color="0.6", lw=0.8, zorder=1)
        ax.axvline(0, color="0.6", lw=0.8, zorder=1)
        ax.scatter(sub["scaling_residual"], sub["content_residual"],
                   s=14, alpha=0.5, edgecolor="none", zorder=2)
        ax.set_xlabel("scaling residual  (log insc − population-predicted)")
        ax.set_ylabel("content residual  (log letter-mass − insc-count-predicted)")
        ax.set_title(f"{title}\nSpearman ρ = {xtab['spearman_rho']:+.3f} "
                     f"(n = {xtab['n']}); descriptive, A01 §A5.4")
    fig.suptitle("Two-dimensional residual space — content residual × scaling residual "
                 "(Amendment 01 §A5.4; exploratory/descriptive)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print(f"[content-residual] A01 §A5.4 — DESCRIPTIVE (no verdict). seed={SEED}")

    latin, empire = build_letter_mass_frames()

    # --- Content residual (OLS) on each frame ---
    print("[content-residual] OLS log(letter_mass) ~ log(inscription_count) ...")
    latin_ols = content_residual_ols(latin)
    empire_ols = content_residual_ols(empire)
    print(f"  Latin : slope {latin_ols['slope']:.3f} R² {latin_ols['r_squared']:.3f} "
          f"(n {latin_ols['n_fitted']}, dropped {latin_ols['n_zero_mass_dropped']})")
    print(f"  empire: slope {empire_ols['slope']:.3f} R² {empire_ols['r_squared']:.3f} "
          f"(n {empire_ols['n_fitted']}, dropped {empire_ols['n_zero_mass_dropped']})")

    # --- Scaling residual (D12 SAMOC pooled NBR) on each frame ---
    print("[content-residual] D12 SAMOC scaling residual (Latin frame) ...")
    latin_scal = scaling_residual_d12(latin)
    print(f"  Latin pooled β {latin_scal['beta_median']:.3f} "
          f"(R̂ {latin_scal['max_rhat']:.4f}, div {latin_scal['n_divergences']})")
    print("[content-residual] D12 SAMOC scaling residual (empire frame) ...")
    empire_scal = scaling_residual_d12(empire)
    print(f"  empire pooled β {empire_scal['beta_median']:.3f} "
          f"(R̂ {empire_scal['max_rhat']:.4f}, div {empire_scal['n_divergences']})")

    # --- Cross-tab ---
    latin_xtab = crosstab(latin)
    empire_xtab = crosstab(empire)
    print(f"[content-residual] Latin cross-tab: Spearman ρ {latin_xtab['spearman_rho']:+.3f} "
          f"(p {latin_xtab['spearman_p']:.3g}); quadrants {latin_xtab['quadrant_counts']}")
    print(f"[content-residual] empire cross-tab: Spearman ρ {empire_xtab['spearman_rho']:+.3f} "
          f"(p {empire_xtab['spearman_p']:.3g})")

    # --- Figure ---
    fig_path = OUT_DIR / "content-residual-space-map.png"
    make_figure(latin, empire, latin_xtab, empire_xtab, fig_path)
    print(f"[content-residual] wrote {fig_path.name}")

    # --- Per-city CSV (Latin primary frame) ---
    csv_cols = ["city", "province", "log_pop", "log_inscription_count",
                "log_letter_mass", "letter_mass", "inscription_count",
                "content_residual", "scaling_residual", "quadrant"]
    csv_path = OUT_DIR / "content-residual-per-city.csv"
    latin[csv_cols].sort_values("scaling_residual").to_csv(csv_path, index=False)
    print(f"[content-residual] wrote {csv_path.name}")

    # --- Results JSON (provenance + everything numeric) ---
    results = {
        "analysis": "Amendment 01 §A5.4 content residual (inter-measure delta)",
        "status": "DESCRIPTIVE — exploratory; no threshold, no verdict (A01 §A5.4)",
        "seed": SEED,
        "host": "local (zbook-ubuntu)",
        "frames": {
            "latin_primary": {
                "n_cities": int(len(latin)),
                "n_provinces": int(latin["province"].nunique()),
                "content_residual_ols": latin_ols,
                "scaling_residual_fit": latin_scal,
                "crosstab": latin_xtab,
            },
            "empire_context": {
                "n_cities": int(len(empire)),
                "n_provinces": int(empire["province"].nunique()),
                "content_residual_ols": empire_ols,
                "scaling_residual_fit": empire_scal,
                "crosstab": empire_xtab,
            },
        },
        "provenance": {
            "raw_lire": str(RAW_LIRE.relative_to(PROJECT_ROOT)),
            "raw_lire_sha256": _sha256(RAW_LIRE),
            "letter_mass_builder": "runs/2026-06-18-h9-letter-mass-h3a/code/h9_common.py",
            "letter_measure": "letter_count_conservative (Latin A–Z; A01 §A5.1)",
            "scaling_residual_construction": "D12 SAMOC pooled-NBR log residual "
                "(runs/2026-06-16-s5-sensitivities/code/d12_scaling_residual.py); "
                "recomputed on the Latin and empire frames so the residual space is "
                "internally coherent per frame. The persisted D12 artefact "
                "(d12-scaling-residual-results.json) is the all-provinces aggregate fit.",
        },
        "secs": round(time.time() - t0, 1),
    }
    json_path = OUT_DIR / "content-residual-results.json"
    json_path.write_text(json.dumps(results, indent=1))
    print(f"[content-residual] wrote {json_path.name}  ({results['secs']}s)")
    print("[content-residual] DONE (descriptive; no verdict).")


if __name__ == "__main__":
    main()
