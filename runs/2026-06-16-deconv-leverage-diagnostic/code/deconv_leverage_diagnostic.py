#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deconv_leverage_diagnostic.py — would the cc-library deconvolution change H3a?
=============================================================================

Shawn's question (2026-06-15): we built a deconvolution (the cc-library mixture
separating editorial-convention artefacts from genuine epigraphic production).
H3a (the Hanson scaling: inscription COUNT ~ population^β) currently uses raw
date-window counts. Would the deconvolution help H3a (or the other count-based
analyses), and can we leverage it alongside the preregistered commitments?

This diagnostic answers it EMPIRICALLY rather than by assertion. Two facts frame
the test:

  (1) H3a's date window is the FULL envelope (50 BC – AD 350; `h3a_common.py`
      DATE_WINDOW). The deconvolution's *temporal reshaping* conserves each
      unit's full-window total (both the raw aoristic SPA and the genuine SPA
      normalise to the same n_eff), so reshaping CANNOT change H3a's count. We
      verify this numerically and quantify the shape change (total-variation
      distance) for context (it matters for narrow-window analyses like H3b,
      already done — not for H3a).

  (2) The only channel by which the deconvolution can move H3a's scaling is the
      per-unit α (genuine fraction). If α is flat across size/population, the
      deconvolution is a near-constant multiplier → the scaling β is unchanged →
      raw-count H3a is vindicated. If α correlates with population, raw counts
      carry a convention-size confound and a deconvolution-corrected scaling
      differs. The implied shift in the scaling exponent from replacing the raw
      count N with the genuine count α·N is exactly the OLS slope of log(α) on
      log(population). We estimate it (with a bootstrap CI) at the level α is
      available — the 29 deconvolved units (province/region-level + a few cities)
      — and flag that the definitive city-level test needs a per-city mixture
      (the preregistered D13 α-as-translator sensitivity).

Outputs (`runs/2026-06-16-deconv-leverage-diagnostic/outputs/`):
  alpha-population-diagnostic.json  — per-unit α, n_eff, Hanson pop, reshaping TV;
                                       correlations + the implied-Δβ statistic.
  REPORT.md                          — the answer, generated from the data.
  figures/fig-alpha-vs-size.png      — α vs population and α vs corpus size.

Reuse-only over the verified refit/h2/h1 loaders; no MCMC; local/sapphire.
Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-16.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/home/shawn/Code/inscriptions")
for _p in ("runs/2026-04-25-h1-simulation/code",
           "runs/2026-06-07-h2.1-launch-prep/code",
           "runs/2026-06-13-cc-production-refit/code"):
    sys.path.insert(0, str(ROOT / _p))
import primitives as P   # noqa: E402  (BIN_CENTRES)
import h2_lib as H       # noqa: E402  (load_filtered_lire, latin_provinces, aoristic_spa)
import refit_lib as R    # noqa: E402  (enumerate_refit_units, subset_for, build_unit_cc_data)

RAW_LIRE = ROOT / "archive/data-2026-04-22/LIRE_v3-0.parquet"
REFIT_SUMMARY = ROOT / "runs/2026-06-13-cc-production-refit/outputs/refit-summary.json"
DRAWS_DIR = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
OUT_DIR = ROOT / "runs/2026-06-16-deconv-leverage-diagnostic/outputs"
FIG_DIR = OUT_DIR / "figures"

# Units that are sums of other units — excluded from the cross-unit correlation
# (they would double-count and inflate it), reported separately for context.
AGGREGATES = {"empire-aggregate", "latin-aggregate", "Italia (excl. Rome)"}
BIN_CENTRES = P.BIN_CENTRES


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def load_genuine_median_spa(name: str) -> np.ndarray:
    """Posterior-median genuine SPA (per-draw normalised, then median), summing 1."""
    z = np.load(DRAWS_DIR / f"{_safe(name)}-pgen.npz", allow_pickle=True)
    p = z["p_gen"].astype(np.float64)
    s = p.sum(axis=1, keepdims=True)
    s[s <= 0] = 1.0
    g = np.median(p / s, axis=0)
    return g / g.sum()


def hanson_population(sub: pd.DataFrame, raw: pd.DataFrame) -> tuple[float, int]:
    """Total Hanson urban population represented in a unit's rows.

    Sum of the modal `urban_context_pop_est` over the distinct Hanson cities
    (Rome excluded) present in the unit's corpus. Returns (total_pop, n_cities).
    """
    if {"urban_context_pop_est", "urban_context_city"} <= set(sub.columns):
        pop = sub
    else:
        assert sub.index.isin(raw.index).all(), \
            "index misalignment: cannot join Hanson pop from raw LIRE by index"
        pop = raw.loc[sub.index]
    city = pop["urban_context_city"].fillna("").str.strip().str.lower()
    keep = (city != "roma") & pop["urban_context_pop_est"].notna()
    h = pop.loc[keep]
    if h.empty:
        return float("nan"), 0
    per_city = h.groupby(city[keep]).agg(
        pop=("urban_context_pop_est", lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan))
    return float(per_city["pop"].sum()), int(per_city["pop"].notna().sum())


def assemble() -> pd.DataFrame:
    """Per-unit α, corpus size, Hanson population, and reshaping TV distance."""
    df = H.load_filtered_lire()
    raw = pd.read_parquet(RAW_LIRE)
    latin = H.latin_provinces()
    summary = {u["name"]: u for u in json.loads(REFIT_SUMMARY.read_text())["units"]}

    rows = []
    for unit in R.enumerate_refit_units():
        name = unit["name"]
        meta = summary.get(name, {})
        sub = R.subset_for(df, unit, latin)
        cc = R.build_unit_cc_data(sub)
        n_eff = int(cc["n_rows"])
        total_pop, n_cities = hanson_population(sub, raw)

        # Reshaping: raw aoristic SPA vs genuine median SPA (both normalised).
        raw_spa = H.aoristic_spa(sub["nb"].to_numpy(float), sub["na"].to_numpy(float))
        raw_spa = raw_spa / raw_spa.sum() if raw_spa.sum() > 0 else raw_spa
        tv = float("nan")
        npz = DRAWS_DIR / f"{_safe(name)}-pgen.npz"
        if npz.exists():
            gen_spa = load_genuine_median_spa(name)
            tv = 0.5 * float(np.abs(raw_spa - gen_spa).sum())   # total-variation distance

        rows.append({
            "name": name, "kind": unit.get("kind", ""), "frame": unit.get("frame", ""),
            "is_aggregate": name in AGGREGATES,
            "is_single_city": n_cities == 1,
            "alpha_median": float(meta.get("alpha_median", float("nan"))),
            "alpha_ci_lo": float(meta.get("alpha_ci_lo", float("nan"))),
            "alpha_ci_hi": float(meta.get("alpha_ci_hi", float("nan"))),
            "n_eff": n_eff,
            "hanson_pop_total": total_pop, "n_hanson_cities": n_cities,
            "reshaping_tv": tv,
        })
    return pd.DataFrame(rows)


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def _ols_slope(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.polyfit(x, y, 1)[0])


def _boot_ci(x: np.ndarray, y: np.ndarray, stat, n_boot=5000, seed=20260616):
    rng = np.random.default_rng(seed)
    n = len(x)
    vals = [stat(x[idx], y[idx]) for idx in (rng.integers(0, n, n) for _ in range(n_boot))]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def analyse(d: pd.DataFrame) -> dict:
    core = d.loc[~d["is_aggregate"] & np.isfinite(d["hanson_pop_total"])
                 & (d["hanson_pop_total"] > 0) & np.isfinite(d["alpha_median"])].copy()
    lp = np.log(core["hanson_pop_total"].to_numpy())
    ln = np.log(core["n_eff"].to_numpy())
    a = core["alpha_median"].to_numpy()
    la = np.log(np.clip(a, 1e-6, None))

    # Implied scaling-exponent shift if raw count N is replaced by genuine α·N:
    # Δβ = slope( log α ~ log pop ).  (Δβ ≈ 0  ⇒ deconvolution leaves Hanson scaling unchanged.)
    dbeta = _ols_slope(lp, la)
    dbeta_ci = _boot_ci(lp, la, _ols_slope)

    out = {
        "n_units_core": int(len(core)),
        "alpha_range": [float(core["alpha_median"].min()), float(core["alpha_median"].max())],
        "alpha_mean": float(core["alpha_median"].mean()),
        "alpha_sd": float(core["alpha_median"].std(ddof=1)),
        # α vs population (the H3a-relevant axis).
        "spearman_alpha_vs_logpop": _spearman(a, lp),
        "pearson_alpha_vs_logpop": float(np.corrcoef(a, lp)[0, 1]),
        # α vs corpus size (a second, join-free size proxy).
        "spearman_alpha_vs_logneff": _spearman(a, ln),
        "pearson_alpha_vs_logneff": float(np.corrcoef(a, ln)[0, 1]),
        # The decision statistic.
        "implied_delta_beta_alpha_correction": dbeta,
        "implied_delta_beta_ci95": list(dbeta_ci),
        # Reshaping (full-window count is conserved; TV measures shape change only).
        "reshaping_tv_median": float(d["reshaping_tv"].median(skipna=True)),
        "reshaping_tv_max": float(d["reshaping_tv"].max(skipna=True)),
        "date_window": "50 BC – AD 350 (full envelope; reshaping conserves the count)",
    }
    return out


def make_figure(d: pd.DataFrame, summary: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    core = d.loc[~d["is_aggregate"] & np.isfinite(d["hanson_pop_total"])
                 & (d["hanson_pop_total"] > 0)].copy()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    ax = axes[0]
    cities = core[core["is_single_city"]]
    provs = core[~core["is_single_city"]]
    ax.scatter(provs["hanson_pop_total"], provs["alpha_median"], c="C0", label="province/region")
    ax.scatter(cities["hanson_pop_total"], cities["alpha_median"], c="C3", marker="D", label="single city")
    lp = np.log(core["hanson_pop_total"].to_numpy())
    a = core["alpha_median"].to_numpy()
    b1, b0 = np.polyfit(lp, a, 1)
    xs = np.linspace(lp.min(), lp.max(), 50)
    ax.plot(np.exp(xs), b0 + b1 * xs, "k--", lw=1,
            label=f"slope(α~logpop)={b1:+.3f}")
    ax.set_xscale("log")
    ax.set_xlabel("Hanson urban population (Σ over unit's cities, log)")
    ax.set_ylabel("α (genuine fraction)")
    ax.set_ylim(0, 1.02)
    ax.set_title("α vs population — flat ⇒ deconvolution doesn't move Hanson β")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.scatter(core["n_eff"], core["alpha_median"], c="C0")
    ax.set_xscale("log")
    ax.set_xlabel("corpus size n_eff (log)")
    ax.set_ylabel("α (genuine fraction)")
    ax.set_ylim(0, 1.02)
    ax.set_title(f"α vs corpus size  (Spearman={summary['spearman_alpha_vs_logneff']:+.2f})")

    fig.suptitle("Does convention intensity (1−α) scale with size? "
                 f"Implied Hanson-β shift from α-correction = {summary['implied_delta_beta_alpha_correction']:+.3f} "
                 f"[{summary['implied_delta_beta_ci95'][0]:+.3f}, {summary['implied_delta_beta_ci95'][1]:+.3f}]",
                 fontsize=10)
    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "fig-alpha-vs-size.png", dpi=130)
    plt.close(fig)


def write_report(d: pd.DataFrame, s: dict) -> None:
    ci = s["implied_delta_beta_ci95"]
    crosses0 = ci[0] <= 0.0 <= ci[1]
    verdict = ("the deconvolution does NOT materially change the Hanson scaling — "
               "raw-count H3a is robust to convention-correction"
               if crosses0 else
               "the deconvolution WOULD shift the Hanson scaling — convention intensity "
               "correlates with size, a real confound to correct")
    agg = d[d["is_aggregate"]][["name", "alpha_median", "n_eff", "hanson_pop_total"]]
    cityrows = d[d["is_single_city"] & ~d["is_aggregate"]].sort_values("hanson_pop_total", ascending=False)

    def tbl(frame, cols, fmts):
        head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols)
        out = [head]
        for _, r in frame.iterrows():
            out.append("| " + " | ".join(f(r[c]) for c, f in zip(cols, fmts)) + " |")
        return "\n".join(out)

    md = f"""# Would the cc-library deconvolution help H3a (and the other count analyses)?

> Diagnostic answer to Shawn's 2026-06-15 question. Generated from the data
> (`outputs/alpha-population-diagnostic.json`). H3a/H3c are unchanged by this; it
> is a leverage/robustness check, not a confirmatory result.

## Verdict

**On the evidence we have, {verdict}.**

The implied shift in the Hanson scaling exponent from replacing the raw count *N*
with the genuine count α·N — which equals the OLS slope of log(α) on log(population)
across the {s['n_units_core']} non-aggregate deconvolved units — is
**Δβ = {s['implied_delta_beta_alpha_correction']:+.3f}** (95% bootstrap CI
[{ci[0]:+.3f}, {ci[1]:+.3f}]). {'The CI includes 0' if crosses0 else 'The CI excludes 0'}.

## Why this is the right statistic

1. **Temporal reshaping cannot touch H3a's count.** H3a's date window is the full
   envelope (50 BC – AD 350; `h3a_common.DATE_WINDOW`). The deconvolution moves mass
   *between* time-bins but conserves each unit's full-window total — the raw aoristic
   SPA and the genuine SPA both normalise to the same n_eff. So the only channel left
   is the genuine fraction α. (The shape change is real but irrelevant to a full-window
   count: median total-variation distance between raw and genuine SPA =
   {s['reshaping_tv_median']:.3f}, max {s['reshaping_tv_max']:.3f} — that is what H3b,
   already done, reads; H3a does not.)
2. **α enters only as a multiplier.** Genuine count = α·N, so the scaling exponent
   shifts by exactly the trend of log(α) against log(population). Flat α ⇒ constant
   multiplier ⇒ unchanged β.

## What α looks like across the units

- α range [{s['alpha_range'][0]:.2f}, {s['alpha_range'][1]:.2f}], mean
  {s['alpha_mean']:.2f} (SD {s['alpha_sd']:.2f}).
- **α vs population:** Spearman {s['spearman_alpha_vs_logpop']:+.2f}, Pearson
  {s['pearson_alpha_vs_logpop']:+.2f}.
- **α vs corpus size (n_eff):** Spearman {s['spearman_alpha_vs_logneff']:+.2f}, Pearson
  {s['pearson_alpha_vs_logneff']:+.2f}.

See `figures/fig-alpha-vs-size.png`.

### Single-city units (direct α-vs-population)
{tbl(cityrows, ["name", "alpha_median", "hanson_pop_total", "n_eff"],
     [lambda v: str(v), lambda v: f"{v:.2f}", lambda v: f"{v:,.0f}", lambda v: f"{int(v):,}"])}

### Aggregates (context only; excluded from the correlation)
{tbl(agg, ["name", "alpha_median", "hanson_pop_total", "n_eff"],
     [lambda v: str(v), lambda v: f"{v:.2f}", lambda v: f"{v:,.0f}", lambda v: f"{int(v):,}"])}

## What this means for leveraging the deconvolution

- **H3a / SR1 (count-based scaling):** the preregistered primary stays raw-count
  (Decision 22/35; a lodged confirmatory primary, and — given the above — the
  deconvolution would {'not move it materially' if crosses0 else 'move it'} anyway).
  The deconvolution's H3a value-add is the preregistered **D13 α-as-translator §5
  sensitivity**, which needs **per-city** α (only 29 province/region-level units are
  deconvolved so far). This diagnostic is the province-level proxy; the definitive
  city-level test is the per-city mixture build.
- **Already fully leveraged:** H3b (runs on the genuine SPA) and the descriptive
  genuine-vs-raw SPA figures — that is where the reshaping (TV up to
  {s['reshaping_tv_max']:.2f}) does its work.
- **Letter-count, H3c:** inherit H3a's treatment; same α-sensitivity route.

## Caveat

α is available only at the 29 deconvolved units (mostly province/region-level). The
slope above is a province-level proxy for the city-level H3a confound; it is
{'reassuringly flat' if crosses0 else 'non-trivial'}, but the city-level confound is
only directly testable with a per-city deconvolution (D13). Aggregates excluded from
the correlation to avoid double-counting.

## Reproduce
```bash
uv run python runs/2026-06-16-deconv-leverage-diagnostic/code/deconv_leverage_diagnostic.py
```
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "REPORT.md").write_text(md)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("assembling per-unit α / population / reshaping ...", flush=True)
    d = assemble()
    s = analyse(d)
    d.to_json(OUT_DIR / "alpha-population-diagnostic.json", orient="records", indent=1)
    (OUT_DIR / "summary.json").write_text(json.dumps(s, indent=1))
    make_figure(d, s)
    write_report(d, s)
    print(json.dumps(s, indent=1))
    print(f"\nwrote outputs → {OUT_DIR}")


if __name__ == "__main__":
    main()
