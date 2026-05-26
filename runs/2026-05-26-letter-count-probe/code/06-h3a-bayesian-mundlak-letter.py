#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06-h3a-bayesian-mundlak-letter.py --- Block 6 of the 2026-05-26 letter-count
probe.

Purpose
-------
Bayesian within-between (Mundlak) negative-binomial regression of per-city
response on Hanson 2016 urban population, under THREE response variants:

  (1) inscription_count(city)                              --- baseline
  (2) sum(letter_count_conservative) per city              --- letter, cons
  (3) sum(letter_count_interpretive) per city              --- letter, intr

This re-fits the talk-prep H3a Bayesian Mundlak (runs/2026-05-21-talk-prep/
code/05-h3a-bayesian-mundlak.py) under the two letter variants so that
f_within for the three variants is computed with the SAME denominator (total
Var(log E[y]) across cities, INCLUDING the province random-intercept
contribution alpha_prov[c]). This makes the three f_within posteriors
directly comparable.

Why this run exists --- discrepancy diagnosis
---------------------------------------------
Block-5 of this probe (frequentist Mundlak in
05-within-province-variance-partition.py) reported f_within around 95 %
under all three response variants. That is NOT inconsistent with the talk-
prep Bayesian f_within around 30 %; the discrepancy is a denominator
choice:

  - Block 5's frequentist Mundlak omits the province random intercept and
    defines f_within = var_within / (var_within + var_between), where
    var_* are functions only of the population predictor. The population-
    attributable variance is by construction mostly within-province, so this
    ratio is around 95 %.
  - The Bayesian Mundlak (this script + the talk-prep template) defines
    f_within = Var(beta_within * within_dev) / Var(log E[y]), where the
    denominator INCLUDES the province random-effect variance contribution.
    Provinces themselves carry a large slice of total predicted-log-y
    variance, so the within-share lands around 30 %.

Both numbers are correct under their own definitions; the talk-prep slide-6
punchline uses the Bayesian denominator (it is the prereg-binding estimand
per preregistration-draft.md, lines 212-247). This script therefore is the
verdict-flag-3 authority for the letter-count probe.

Model spec --- IDENTICAL to talk-prep template
----------------------------------------------
  y_c ~ NegativeBinomial(mu_c, dispersion)
  log(mu_c) = alpha_0 + alpha_prov[c]
              + beta_within  * (log_pop_c - log_pop_prov_mean[c])
              + beta_between * log_pop_prov_mean[c]

  Priors:
    alpha_0      ~ Normal(0, 5)
    beta_within  ~ Normal(0, 1)
    beta_between ~ Normal(0, 1)
    alpha_prov   ~ Normal(0, sigma_prov)   (non-centred parameterisation)
    sigma_prov   ~ HalfNormal(1)
    1/dispersion ~ HalfNormal(1)

Sampler --- IDENTICAL to talk-prep template
-------------------------------------------
  N_WARMUP = 3,000     N_SAMPLE = 2,000     N_CHAINS = 4
  target_accept = 0.95
  RANDOM_SEED = 20,260,526   (today's date; cf. talk-prep used 20,260,521)

Convergence gates (per prereg)
------------------------------
  - R-hat < 1.01 on all parameters
  - ESS_bulk >= 400 on key parameters
  - 0 divergences

HARD HALT: if any variant fails any gate, this script aborts with non-zero
exit and a human-readable report. Do NOT silently retune.

Outputs
-------
outputs/tables/h3a-mundlak-three-variants-summary.csv
    Per-variant posterior summary: f_within median + 95 % CI,
    P(f_within > 0.10), P(> 0.20), beta_within + beta_between summaries,
    convergence diagnostics.

outputs/tables/h3a-mundlak-three-variants-posterior.csv
    Per-variant f_within posterior draws (long format: columns
    [variant, draw_index, f_within]; one block per variant stacked).

outputs/figures/fig-06-h3a-mundlak-three-variants.png
    Forest plot of f_within medians + 95 % CIs across variants. Colour
    palette: inscription #264653, letter_cons #e76f51, letter_intr #2a9d8f
    (matches block-5 frequentist bar figure).

RUN-LOG-06.md
    Wall-clock + convergence diagnostics + verdict flag-3 update.

Date
----
2026-05-26
"""

from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = RUN_DIR / "data" / "lire-filtered-with-letters.parquet"
FIG_DIR = RUN_DIR / "outputs" / "figures"
TBL_DIR = RUN_DIR / "outputs" / "tables"
RUN_LOG_PATH = RUN_DIR / "RUN-LOG-06.md"

for d in (FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Sampler settings --- IDENTICAL to talk-prep template
# ---------------------------------------------------------------------------
N_WARMUP = 3_000
N_SAMPLE = 2_000
N_CHAINS = 4
RANDOM_SEED = 20_260_526   # today's date; talk-prep used 20_260_521

TARGET_ACCEPT = 0.95

# Convergence gates (per prereg)
RHAT_GATE = 1.01
ESS_GATE = 400
DIV_GATE = 0

FIG_SIZE = (10.5, 5.5)
DPI = 200


# Variant definitions. letter_col=None means inscription count (row-count
# aggregation); otherwise sum the named column.
VARIANTS = [
    {"key": "inscription",
     "label": "inscription count",
     "letter_col": None,
     "colour": "#264653"},
    {"key": "letter_cons",
     "label": "letter total (conservative)",
     "letter_col": "letter_count_conservative",
     "colour": "#e76f51"},
    {"key": "letter_intr",
     "label": "letter total (interpretive)",
     "letter_col": "letter_count_interpretive",
     "colour": "#2a9d8f"},
]


# ---------------------------------------------------------------------------
# Data prep --- matches talk-prep template logic
# ---------------------------------------------------------------------------
def rome_mask(df: pd.DataFrame) -> pd.Series:
    """Rome-exclusion mask (matches talk-prep 01-filter-and-prep.py)."""
    return df["urban_context_city"].fillna("").str.strip().str.lower() == "roma"


def build_city_frame(df: pd.DataFrame, letter_col: str | None
                     ) -> tuple[pd.DataFrame, list[str]]:
    """Aggregate to one row per Hanson-city (Rome-excluded) with Mundlak
    decomposition columns attached.

    Parameters
    ----------
    df : raw filtered LIRE rows (180,609 rows on prereg envelope).
    letter_col :
        If None, response = inscription_count (row count per city).
        If a column name, response = sum(letter_col) per city.

    Returns
    -------
    cities : DataFrame with columns
        urban_context_city, response, urban_context_pop_est, province,
        log_pop, log_pop_prov_mean, log_pop_within, province_idx
    province_categories : list[str] of unique province labels in row order
    """
    rome = rome_mask(df)
    has_hanson = df["urban_context_pop_est"].notna()
    sub = df.loc[~rome & has_hanson].copy()

    if letter_col is None:
        agg = (
            sub.groupby("urban_context_city")
            .agg(
                response=("urban_context_city", "size"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
                province=("province",
                          lambda x: x.mode()[0] if not x.mode().empty else np.nan),
            )
            .reset_index()
        )
    else:
        agg = (
            sub.groupby("urban_context_city")
            .agg(
                response=(letter_col, "sum"),
                urban_context_pop_est=("urban_context_pop_est", "first"),
                province=("province",
                          lambda x: x.mode()[0] if not x.mode().empty else np.nan),
            )
            .reset_index()
        )

    agg = agg.dropna(subset=["province"]).copy()
    agg["log_pop"] = np.log(agg["urban_context_pop_est"])
    prov_means = agg.groupby("province")["log_pop"].transform("mean")
    agg["log_pop_prov_mean"] = prov_means
    agg["log_pop_within"] = agg["log_pop"] - prov_means

    province_codes = pd.Categorical(agg["province"])
    agg["province_idx"] = province_codes.codes
    return agg, list(province_codes.categories)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def fit_mundlak(cities: pd.DataFrame, n_provinces: int, variant_key: str
                ) -> az.InferenceData:
    """Bayesian Mundlak NBR fit. Spec identical to talk-prep template."""
    y_obs = cities["response"].to_numpy(dtype=int)
    log_pop_within = cities["log_pop_within"].to_numpy(dtype=float)
    log_pop_prov_mean = cities["log_pop_prov_mean"].to_numpy(dtype=float)
    province_idx = cities["province_idx"].to_numpy(dtype=int)

    # Sanity-check response: NBR requires non-negative integer counts.
    if (y_obs < 0).any():
        raise ValueError(f"[{variant_key}] negative response values present")
    if not np.issubdtype(y_obs.dtype, np.integer):
        raise ValueError(f"[{variant_key}] response is not integer-typed")

    with pm.Model() as model:
        alpha_0 = pm.Normal("alpha_0", mu=0.0, sigma=5.0)
        sigma_prov = pm.HalfNormal("sigma_prov", sigma=1.0)
        alpha_prov_raw = pm.Normal("alpha_prov_raw", mu=0.0, sigma=1.0,
                                    shape=n_provinces)
        alpha_prov = pm.Deterministic("alpha_prov", sigma_prov * alpha_prov_raw)

        beta_within = pm.Normal("beta_within", mu=0.0, sigma=1.0)
        beta_between = pm.Normal("beta_between", mu=0.0, sigma=1.0)

        inv_disp = pm.HalfNormal("inv_dispersion", sigma=1.0)
        dispersion = pm.Deterministic("dispersion", 1.0 / inv_disp)

        log_mu = (
            alpha_0
            + alpha_prov[province_idx]
            + beta_within * log_pop_within
            + beta_between * log_pop_prov_mean
        )
        mu = pm.math.exp(log_mu)
        pm.Deterministic("log_mu", log_mu)

        pm.NegativeBinomial("y", mu=mu, alpha=dispersion, observed=y_obs)

        print(f"[block-6 / {variant_key}] sampling NUTS: warmup={N_WARMUP}, "
              f"draws={N_SAMPLE}, chains={N_CHAINS}, seed={RANDOM_SEED} ...")
        idata = pm.sample(
            draws=N_SAMPLE,
            tune=N_WARMUP,
            chains=N_CHAINS,
            random_seed=RANDOM_SEED,
            progressbar=False,
            target_accept=TARGET_ACCEPT,
            return_inferencedata=True,
        )
    return idata


# ---------------------------------------------------------------------------
# f_within estimand --- IDENTICAL to talk-prep template
# ---------------------------------------------------------------------------
def compute_f_within(idata: az.InferenceData, cities: pd.DataFrame) -> np.ndarray:
    """Compute f_within per posterior draw.

    f_within = Var(beta_within * within_dev) / Var(log E[y])

    Both variances are unweighted across the n_cities city-level data
    points, per posterior draw. The denominator uses the model's own
    posterior `log_mu` deterministic, so it INCLUDES the alpha_prov
    contribution (alpha_0 contributes 0 to variance because it is
    constant across cities).

    Returns
    -------
    f_within : array of shape (n_chains * n_draws,)
    """
    post = idata.posterior
    n_chains = post.sizes["chain"]
    n_draws = post.sizes["draw"]

    within_dev = cities["log_pop_within"].to_numpy(dtype=float)
    log_mu = post["log_mu"].values.reshape(n_chains * n_draws, -1)  # (D, C)
    beta_w = post["beta_within"].values.reshape(-1)                 # (D,)

    contrib_within = beta_w[:, None] * within_dev[None, :]          # (D, C)
    var_num = contrib_within.var(axis=1, ddof=0)                    # (D,)
    var_den = log_mu.var(axis=1, ddof=0)                            # (D,)
    f_within = var_num / var_den
    return f_within


# ---------------------------------------------------------------------------
# Convergence-gate enforcement
# ---------------------------------------------------------------------------
def check_convergence(idata: az.InferenceData, variant_key: str) -> dict:
    """Check prereg convergence gates. Returns a diagnostics dict.

    HARD-HALT: caller must check `passed` flag and abort if False.
    """
    summ = az.summary(idata, var_names=["alpha_0", "beta_within",
                                         "beta_between", "sigma_prov",
                                         "dispersion"])
    max_rhat = float(summ["r_hat"].max())
    min_ess_bulk = float(summ["ess_bulk"].min())
    sample_stats = idata.sample_stats
    n_div = int(sample_stats["diverging"].sum())

    rhat_pass = max_rhat < RHAT_GATE
    ess_pass = min_ess_bulk >= ESS_GATE
    div_pass = n_div <= DIV_GATE
    passed = rhat_pass and ess_pass and div_pass

    return {
        "variant": variant_key,
        "max_rhat": max_rhat,
        "min_ess_bulk": min_ess_bulk,
        "n_divergences": n_div,
        "rhat_pass": rhat_pass,
        "ess_pass": ess_pass,
        "div_pass": div_pass,
        "passed": passed,
        "summary_df": summ,
    }


# ---------------------------------------------------------------------------
# Figure --- forest plot of f_within across variants
# ---------------------------------------------------------------------------
def render_figure(variant_results: list[dict]) -> Path:
    """Forest plot of f_within median + 95 % CI across variants."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ys = np.arange(len(variant_results))[::-1]  # top-to-bottom in display
    medians = [r["f_within_median"] for r in variant_results]
    lo = [r["f_within_ci_lo"] for r in variant_results]
    hi = [r["f_within_ci_hi"] for r in variant_results]
    colours = [r["colour"] for r in variant_results]
    labels = [r["label"] for r in variant_results]

    for y, m, l, h, c in zip(ys, medians, lo, hi, colours):
        ax.errorbar(m, y, xerr=[[m - l], [h - m]], fmt="o",
                    color=c, ecolor=c, markersize=10, capsize=6,
                    linewidth=2.0, markeredgecolor="black",
                    markeredgewidth=0.6)

    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel(r"$f_{within}$  (posterior median + 95 % CI)", fontsize=11)
    ax.axvline(0.10, color="black", linestyle="--", linewidth=0.9,
               label="prereg threshold 0.10")
    ax.axvline(0.20, color="grey", linestyle=":", linewidth=0.8,
               label="prereg threshold 0.20")
    ax.set_xlim(0, max(0.5, max(hi) + 0.05))

    # Annotate with numeric values + verdict-flag-3 shift from inscription baseline.
    baseline = variant_results[0]["f_within_median"]
    for y, r in zip(ys, variant_results):
        m = r["f_within_median"]
        if r["key"] == "inscription":
            note = f"{m:.3f}  (baseline)"
        else:
            shift_pp = 100.0 * (m - baseline)
            note = (f"{m:.3f}  (shift {shift_pp:+.2f} pp; "
                    f"{r['flag3']})")
        ax.text(r["f_within_ci_hi"] + 0.01, y, note,
                va="center", fontsize=9)

    ax.set_title(
        "Bayesian Mundlak NBR --- $f_{within}$ posterior across three "
        "response variants\n(N_WARMUP=3000, N_SAMPLE=2000, N_CHAINS=4; "
        f"seed={RANDOM_SEED})",
        fontsize=11,
    )
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()

    out = FIG_DIR / "fig-06-h3a-mundlak-three-variants.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[block-6]   figure -> {out.relative_to(PROJECT_ROOT)}")
    return out


# ---------------------------------------------------------------------------
# Verdict flag 3 (per spec.md §"Verdict thresholds")
# ---------------------------------------------------------------------------
def annotate_flag3(shift_pp: float) -> str:
    """Verdict-flag-3 status string for a percentage-point shift in
    f_within median from the inscription baseline."""
    a = abs(shift_pp)
    if a < 2.0:
        return "FLAG-3 NO-CHANGE"
    if a > 5.0:
        return "FLAG-3 MATERIAL"
    return "FLAG-3 MODEST"


# ---------------------------------------------------------------------------
# RUN-LOG writer
# ---------------------------------------------------------------------------
def write_run_log(variant_results: list[dict], total_wall: float,
                  halted: bool = False, halt_reason: str = "") -> None:
    """Append a session entry to RUN-LOG-06.md."""
    lines = []
    lines.append(f"# RUN-LOG-06 --- Block 6 Bayesian Mundlak (three variants)\n")
    lines.append(f"Date: 2026-05-26  \n")
    lines.append(f"Script: `runs/2026-05-26-letter-count-probe/code/"
                 f"06-h3a-bayesian-mundlak-letter.py`  \n")
    lines.append(f"Total wall-clock: **{total_wall:.1f} s** "
                 f"({total_wall/60.0:.1f} min)\n\n")

    if halted:
        lines.append("## HALTED\n")
        lines.append(f"Reason: {halt_reason}\n\n")

    lines.append("## Per-variant results\n\n")
    lines.append("| variant | n_cities | f_within median | 95 % CI | "
                 "P(f>0.10) | P(f>0.20) | beta_within median | "
                 "beta_between median | max R-hat | min ESS_bulk | "
                 "divergences | wall (s) | gate-pass |\n")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in variant_results:
        gate_str = "PASS" if r["convergence"]["passed"] else "FAIL"
        lines.append(
            f"| {r['key']} | {r['n_cities']:,} | "
            f"{r['f_within_median']:.4f} | "
            f"[{r['f_within_ci_lo']:.4f}, {r['f_within_ci_hi']:.4f}] | "
            f"{r['p_f_gt_010']:.4f} | {r['p_f_gt_020']:.4f} | "
            f"{r['beta_within_median']:+.4f} | "
            f"{r['beta_between_median']:+.4f} | "
            f"{r['convergence']['max_rhat']:.4f} | "
            f"{r['convergence']['min_ess_bulk']:.0f} | "
            f"{r['convergence']['n_divergences']} | "
            f"{r['wall_seconds']:.1f} | {gate_str} |\n"
        )

    lines.append("\n## Verdict flag 3 (within-province variance partition)\n\n")
    if variant_results:
        baseline = variant_results[0]["f_within_median"]
        lines.append(f"Baseline (inscription-count variant): "
                     f"f_within median = {baseline:.4f} "
                     f"({100.0 * baseline:.2f} %)\n\n")
        for r in variant_results[1:]:
            shift_pp = 100.0 * (r["f_within_median"] - baseline)
            lines.append(f"- **{r['label']}**: f_within median = "
                         f"{r['f_within_median']:.4f} "
                         f"({100.0 * r['f_within_median']:.2f} %); "
                         f"shift = {shift_pp:+.2f} pp; "
                         f"**{annotate_flag3(shift_pp)}** "
                         f"(NO-CHANGE < 2 pp; MODEST 2--5 pp; "
                         f"MATERIAL > 5 pp)\n")
    lines.append("\n## Sampler settings\n\n")
    lines.append(f"- N_WARMUP = {N_WARMUP}, N_SAMPLE = {N_SAMPLE}, "
                 f"N_CHAINS = {N_CHAINS}\n")
    lines.append(f"- target_accept = {TARGET_ACCEPT}\n")
    lines.append(f"- random_seed = {RANDOM_SEED}\n")
    lines.append(f"- gates: R-hat < {RHAT_GATE}; "
                 f"ESS_bulk >= {ESS_GATE}; divergences <= {DIV_GATE}\n")

    lines.append("\n## Talk-prep cross-reference\n\n")
    lines.append("The talk-prep run "
                 "(`runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv`)"
                 " reported f_within median = 0.2995 (95 % CI "
                 "[0.2403, 0.3664]) for the inscription-count variant, on "
                 "the same 1,044 Hanson-Rome-excluded cities, with seed "
                 "20,260,521. The current run uses seed 20,260,526 "
                 "(today's date) so a tight reproduction of that number "
                 "for the inscription_count variant indicates the model + "
                 "data + sampler are consistent.\n")

    with open(RUN_LOG_PATH, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print(f"[block-6]   RUN-LOG -> {RUN_LOG_PATH.relative_to(PROJECT_ROOT)}")


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------
def run_variant(df: pd.DataFrame, v: dict) -> dict:
    """Fit + diagnose one variant. Returns a dict with all results."""
    variant_key = v["key"]
    print(f"\n=== variant: {variant_key} ({v['label']}) ===")

    cities, provinces = build_city_frame(df, v["letter_col"])
    n_prov = len(provinces)
    print(f"[block-6 / {variant_key}] city sample: {len(cities):,} cities; "
          f"{n_prov} provinces; "
          f"response: min={cities['response'].min()}, "
          f"median={cities['response'].median():.0f}, "
          f"max={cities['response'].max()}, "
          f"total={cities['response'].sum():,}")

    t0 = time.time()
    idata = fit_mundlak(cities, n_provinces=n_prov, variant_key=variant_key)
    wall = time.time() - t0
    print(f"[block-6 / {variant_key}] sampling wall-clock: "
          f"{wall:.1f} s ({wall/60.0:.1f} min)")

    diag = check_convergence(idata, variant_key)
    print(f"[block-6 / {variant_key}] convergence: "
          f"max R-hat={diag['max_rhat']:.4f} (gate < {RHAT_GATE}); "
          f"min ESS_bulk={diag['min_ess_bulk']:.0f} (gate >= {ESS_GATE}); "
          f"divergences={diag['n_divergences']} (gate <= {DIV_GATE}); "
          f"passed={diag['passed']}")

    f_within = compute_f_within(idata, cities)
    f_med = float(np.median(f_within))
    f_lo, f_hi = (float(x) for x in np.percentile(f_within, [2.5, 97.5]))
    p_05 = float((f_within > 0.05).mean())
    p_10 = float((f_within > 0.10).mean())
    p_20 = float((f_within > 0.20).mean())

    bw = idata.posterior["beta_within"].values.flatten()
    bb = idata.posterior["beta_between"].values.flatten()
    bw_lo, bw_hi = np.percentile(bw, [2.5, 97.5])
    bb_lo, bb_hi = np.percentile(bb, [2.5, 97.5])

    print(f"[block-6 / {variant_key}] f_within: median={f_med:.4f}, "
          f"95 % CI=[{f_lo:.4f}, {f_hi:.4f}]; "
          f"P(>0.10)={p_10:.4f}; P(>0.20)={p_20:.4f}")
    print(f"[block-6 / {variant_key}] beta_within median = {np.median(bw):+.4f} "
          f"[{bw_lo:+.4f}, {bw_hi:+.4f}]")
    print(f"[block-6 / {variant_key}] beta_between median = {np.median(bb):+.4f} "
          f"[{bb_lo:+.4f}, {bb_hi:+.4f}]")

    return {
        "key": variant_key,
        "label": v["label"],
        "colour": v["colour"],
        "n_cities": int(len(cities)),
        "n_provinces": n_prov,
        "f_within_draws": f_within,
        "f_within_median": f_med,
        "f_within_ci_lo": f_lo,
        "f_within_ci_hi": f_hi,
        "p_f_gt_005": p_05,
        "p_f_gt_010": p_10,
        "p_f_gt_020": p_20,
        "beta_within_median": float(np.median(bw)),
        "beta_within_ci_lo": float(bw_lo),
        "beta_within_ci_hi": float(bw_hi),
        "beta_between_median": float(np.median(bb)),
        "beta_between_ci_lo": float(bb_lo),
        "beta_between_ci_hi": float(bb_hi),
        "convergence": diag,
        "wall_seconds": wall,
    }


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[block-6] HALT: input parquet missing at {DATA_PATH}.")
        return 1

    df = pd.read_parquet(DATA_PATH)
    print(f"[block-6] loaded {len(df):,} rows from {DATA_PATH.name}")

    required_cols = {"urban_context_city", "urban_context_pop_est",
                     "province", "letter_count_conservative",
                     "letter_count_interpretive"}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"[block-6] HALT: missing required columns: {sorted(missing)}")
        return 1

    overall_t0 = time.time()
    variant_results: list[dict] = []
    halted = False
    halt_reason = ""

    for v in VARIANTS:
        try:
            r = run_variant(df, v)
        except Exception as e:
            halted = True
            halt_reason = (f"exception during variant {v['key']!r}: "
                           f"{type(e).__name__}: {e}")
            print(f"[block-6] HALT: {halt_reason}")
            break
        variant_results.append(r)
        if not r["convergence"]["passed"]:
            halted = True
            halt_reason = (
                f"convergence gate failure on variant {v['key']!r}: "
                f"max R-hat = {r['convergence']['max_rhat']:.4f} "
                f"(gate < {RHAT_GATE}), "
                f"min ESS_bulk = {r['convergence']['min_ess_bulk']:.0f} "
                f"(gate >= {ESS_GATE}), "
                f"divergences = {r['convergence']['n_divergences']} "
                f"(gate <= {DIV_GATE}). "
                "Per spec: HALTING; do not silently retune."
            )
            print(f"[block-6] HALT: {halt_reason}")
            break

    total_wall = time.time() - overall_t0
    print(f"\n[block-6] total wall-clock across {len(variant_results)} "
          f"variant(s): {total_wall:.1f} s ({total_wall/60.0:.1f} min)")

    # Attach verdict-flag-3 labels for figure annotation.
    if variant_results:
        baseline = variant_results[0]["f_within_median"]
        for r in variant_results:
            if r["key"] == "inscription":
                r["flag3"] = "baseline"
            else:
                shift_pp = 100.0 * (r["f_within_median"] - baseline)
                r["flag3"] = annotate_flag3(shift_pp)

    # Always write a summary table and posterior CSV for whatever variants
    # completed, plus the RUN-LOG. If we halted, mark it.
    if variant_results:
        rows = []
        for r in variant_results:
            d = r["convergence"]
            rows.append({
                "variant": r["key"],
                "label": r["label"],
                "n_cities": r["n_cities"],
                "n_provinces": r["n_provinces"],
                "f_within_median": r["f_within_median"],
                "f_within_ci_lo": r["f_within_ci_lo"],
                "f_within_ci_hi": r["f_within_ci_hi"],
                "p_f_gt_005": r["p_f_gt_005"],
                "p_f_gt_010": r["p_f_gt_010"],
                "p_f_gt_020": r["p_f_gt_020"],
                "beta_within_median": r["beta_within_median"],
                "beta_within_ci_lo": r["beta_within_ci_lo"],
                "beta_within_ci_hi": r["beta_within_ci_hi"],
                "beta_between_median": r["beta_between_median"],
                "beta_between_ci_lo": r["beta_between_ci_lo"],
                "beta_between_ci_hi": r["beta_between_ci_hi"],
                "max_rhat": d["max_rhat"],
                "min_ess_bulk": d["min_ess_bulk"],
                "n_divergences": d["n_divergences"],
                "convergence_passed": d["passed"],
                "wall_seconds": r["wall_seconds"],
            })
        summary_df = pd.DataFrame(rows)
        summary_path = TBL_DIR / "h3a-mundlak-three-variants-summary.csv"
        summary_df.to_csv(summary_path, index=False, float_format="%.6f")
        print(f"[block-6]   summary -> {summary_path.relative_to(PROJECT_ROOT)}")

        # Long-format posterior CSV (one row per draw per variant).
        post_chunks = []
        for r in variant_results:
            draws = r["f_within_draws"]
            post_chunks.append(pd.DataFrame({
                "variant": r["key"],
                "draw_index": np.arange(len(draws)),
                "f_within": draws,
            }))
        post_df = pd.concat(post_chunks, ignore_index=True)
        post_path = TBL_DIR / "h3a-mundlak-three-variants-posterior.csv"
        post_df.to_csv(post_path, index=False, float_format="%.6f")
        print(f"[block-6]   posterior draws -> "
              f"{post_path.relative_to(PROJECT_ROOT)}")

        # Figure only if we have at least the inscription variant.
        if not halted:
            render_figure(variant_results)
        else:
            print("[block-6] skipping figure render due to HALT")

    write_run_log(variant_results, total_wall, halted=halted,
                  halt_reason=halt_reason)

    if halted:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
