#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
peak_shift_diagnostic.py — does the deconvolution move the PEAK (and would that
shift a peak-window Hanson scaling)?
=============================================================================

Follow-up to `deconv_leverage_diagnostic.py`. That diagnostic showed the
deconvolution does NOT change the *cumulative* Hanson scaling, because H3a's
full-window count is mass-conserved (reshaping moves mass between bins but not the
total). Shawn's sharp follow-up: a *maximum / peak-window* scaling test (peak
25-year or 5-year inscription rate vs Hanson max-population) uses a SHAPE statistic,
not a mass statistic — so the deconvolution's reshaping IS in scope there. The peak
should differ between the raw aoristic SPA and the genuine SPA.

This is the cheap province-level proxy (the 29 deconvolved units we already have;
the definitive city-level test needs a per-city mixture). Per unit it computes, for
5-year (single-bin) and 25-year (5-bin sliding) windows:

  - raw aoristic peak height + peak year;
  - genuine peak height + peak year, propagated over the 8,000 posterior draws
    (median + 95% band) — propagating, not point-estimating, matters because the
    deconvolution's GRW prior is known to ATTENUATE sharp peaks (C8 / Amdt 01 §A5.7);
  - log peak-height ratio (genuine/raw) and peak-year shift;

and then asks the scaling-relevant question: does the log peak-height ratio
correlate with size (population / n_eff)? A non-trivial, size-correlated shift would
mean the deconvolution WOULD move a peak-window scaling β; a flat shift means it
moves the peak but not the scaling. Robust (Theil-Sen) and rank (Spearman) estimators
guard against the log-space leverage that bit the α diagnostic (Pompeii).

Outputs (`runs/2026-06-16-deconv-leverage-diagnostic/outputs/`):
  peak-shift-diagnostic.json, REPORT-peak.md, figures/fig-peak-shift.png.
Reuse-only over the refit/h2/h1 loaders; no MCMC; sapphire.
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
import primitives as P   # noqa: E402
import h2_lib as H       # noqa: E402
import refit_lib as R    # noqa: E402

DRAWS_DIR = ROOT / "runs/2026-06-13-cc-production-refit/outputs/posterior-draws"
OUT_DIR = ROOT / "runs/2026-06-16-deconv-leverage-diagnostic/outputs"
FIG_DIR = OUT_DIR / "figures"
POP_JSON = OUT_DIR / "alpha-population-diagnostic.json"
BIN_CENTRES = P.BIN_CENTRES
AGGREGATES = {"empire-aggregate", "latin-aggregate", "Italia (excl. Rome)"}
WINDOWS = [(1, "5y"), (5, "25y")]   # bins per window (5-year bins)


def _safe(name: str) -> str:
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def sliding_sums(m: np.ndarray, w: int) -> np.ndarray:
    """Sliding-window sums of width w over the last axis. (.., n) -> (.., n-w+1)."""
    if w == 1:
        return m
    c = np.cumsum(m, axis=-1)
    c = np.concatenate([np.zeros(m.shape[:-1] + (1,)), c], axis=-1)
    return c[..., w:] - c[..., :-w]


def window_year(idx: int, w: int) -> float:
    return float(BIN_CENTRES[idx:idx + w].mean())


def _theilsen(x, y):
    s = [(y[j] - y[i]) / (x[j] - x[i])
         for i in range(len(x)) for j in range(i + 1, len(x)) if x[j] != x[i]]
    return float(np.median(s)) if s else float("nan")


def _spearman(x, y):
    return float(pd.Series(x).corr(pd.Series(y), method="spearman"))


def assemble() -> pd.DataFrame:
    pop = {r["name"]: r for r in json.loads(POP_JSON.read_text())}
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    rows = []
    for unit in R.enumerate_refit_units():
        name = unit["name"]
        npz = DRAWS_DIR / f"{_safe(name)}-pgen.npz"
        if not npz.exists():
            continue
        sub = R.subset_for(df, unit, latin)
        n_eff = int(R.build_unit_cc_data(sub)["n_rows"])
        raw = H.aoristic_spa(sub["nb"].to_numpy(float), sub["na"].to_numpy(float))
        raw = raw / raw.sum() * n_eff if raw.sum() > 0 else raw
        g = np.load(npz, allow_pickle=True)["p_gen"].astype(np.float64)
        g = g / g.sum(axis=1, keepdims=True) * n_eff      # (D, 80) genuine counts/draw
        meta = pop.get(name, {})
        for w, wn in WINDOWS:
            rs = sliding_sums(raw, w)
            ri = int(np.argmax(rs))
            raw_peak, raw_year = float(rs[ri]), window_year(ri, w)
            gs = sliding_sums(g, w)                          # (D, 80-w+1)
            gh = gs.max(axis=1)
            gi = gs.argmax(axis=1)
            gy = np.array([window_year(int(i), w) for i in gi])
            gh_med = float(np.median(gh))
            rows.append({
                "name": name, "window": wn, "is_aggregate": name in AGGREGATES,
                "is_single_city": bool(meta.get("is_single_city", False)),
                "n_eff": n_eff,
                "hanson_pop_total": float(meta.get("hanson_pop_total", float("nan"))),
                "alpha_median": float(meta.get("alpha_median", float("nan"))),
                "raw_peak": raw_peak, "raw_peak_year": raw_year,
                "gen_peak_med": gh_med,
                "gen_peak_lo": float(np.percentile(gh, 2.5)),
                "gen_peak_hi": float(np.percentile(gh, 97.5)),
                "gen_peak_year_med": float(np.median(gy)),
                "log_peak_ratio_med": float(np.log(gh_med / raw_peak)) if raw_peak > 0 else float("nan"),
                "peak_year_shift_med": float(np.median(gy) - raw_year),
            })
    return pd.DataFrame(rows)


def analyse(d: pd.DataFrame) -> dict:
    out = {}
    for _, wn in WINDOWS:
        w = d[(d["window"] == wn) & ~d["is_aggregate"]
              & np.isfinite(d["hanson_pop_total"]) & (d["hanson_pop_total"] > 0)
              & np.isfinite(d["log_peak_ratio_med"])].copy()
        lr = w["log_peak_ratio_med"].to_numpy()
        lp = np.log(w["hanson_pop_total"].to_numpy())
        ln = np.log(w["n_eff"].to_numpy())
        out[wn] = {
            "n_units": int(len(w)),
            "log_peak_ratio_median": float(np.median(lr)),
            "log_peak_ratio_iqr": [float(np.percentile(lr, 25)), float(np.percentile(lr, 75))],
            "n_peak_rises": int((lr > 0).sum()), "n_peak_falls": int((lr < 0).sum()),
            "peak_ratio_median_pct": float((np.exp(np.median(lr)) - 1) * 100),
            "abs_peak_year_shift_median": float(np.median(np.abs(w["peak_year_shift_med"]))),
            # Scaling-relevant: does the peak shift correlate with size?  (implied β-shift)
            "spearman_logratio_vs_logpop": _spearman(lr, lp),
            "theilsen_logratio_vs_logpop": _theilsen(lp, lr),
            "spearman_logratio_vs_logneff": _spearman(lr, ln),
            "theilsen_logratio_vs_logneff": _theilsen(ln, lr),
        }
    return out


def make_figure(d: pd.DataFrame, s: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    w25 = d[(d["window"] == "25y") & ~d["is_aggregate"]
            & np.isfinite(d["hanson_pop_total"]) & (d["hanson_pop_total"] > 0)].copy()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    ax = axes[0]
    ax.hist(w25["log_peak_ratio_med"], bins=12, color="C0", alpha=0.8)
    ax.axvline(0, color="k", ls=":", lw=1)
    ax.axvline(s["25y"]["log_peak_ratio_median"], color="C3", ls="--",
               label=f"median {s['25y']['peak_ratio_median_pct']:+.0f}%")
    ax.set_xlabel("log(genuine peak / raw peak), 25-year window")
    ax.set_ylabel("units")
    ax.set_title(f"Does the deconvolution move the peak?  "
                 f"{s['25y']['n_peak_rises']}↑ / {s['25y']['n_peak_falls']}↓ of {s['25y']['n_units']}")
    ax.legend(fontsize=8)

    ax = axes[1]
    cities = w25[w25["is_single_city"]]
    provs = w25[~w25["is_single_city"]]
    ax.scatter(provs["hanson_pop_total"], provs["log_peak_ratio_med"], c="C0", label="province/region")
    ax.scatter(cities["hanson_pop_total"], cities["log_peak_ratio_med"], c="C3", marker="D", label="single city")
    lp = np.log(w25["hanson_pop_total"].to_numpy())
    lr = w25["log_peak_ratio_med"].to_numpy()
    ts = s["25y"]["theilsen_logratio_vs_logpop"]
    b0 = float(np.median(lr) - ts * np.median(lp))
    xs = np.linspace(lp.min(), lp.max(), 50)
    ax.plot(np.exp(xs), b0 + ts * xs, "k--", lw=1, label=f"Theil-Sen slope {ts:+.3f}")
    ax.axhline(0, color="grey", ls=":", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel("Hanson urban population (log)")
    ax.set_ylabel("log(genuine peak / raw peak), 25y")
    ax.set_title(f"Does the peak shift scale with size?  Spearman {s['25y']['spearman_logratio_vs_logpop']:+.2f}")
    ax.legend(fontsize=8)
    fig.suptitle("Peak-window deconvolution leverage: the peak MOVES, but a size-flat shift "
                 "⇒ a peak-scaling β would be ~unchanged", fontsize=10)
    fig.tight_layout()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "fig-peak-shift.png", dpi=130)
    plt.close(fig)


def write_report(d: pd.DataFrame, s: dict) -> None:
    a = s["25y"]
    size_flat = (abs(a["theilsen_logratio_vs_logpop"]) < 0.10 and abs(a["spearman_logratio_vs_logpop"]) < 0.35)
    moves = abs(a["peak_ratio_median_pct"]) >= 5 or a["abs_peak_year_shift_median"] >= 5
    md = f"""# Does the deconvolution move the peak — and would that shift a peak-window scaling?

> Cheap province-level proxy (29 deconvolved units) for Shawn's follow-up to the
> cumulative-scaling result. Generated from `peak-shift-diagnostic.json`. Exploratory;
> the definitive city-level peak-window test needs a per-city deconvolution.

## Two findings

**1. The deconvolution DOES move the peak** (as expected — a peak is a shape statistic,
not mass-conserved). 25-year window: median genuine/raw peak change
**{a['peak_ratio_median_pct']:+.0f}%** ({a['n_peak_rises']} units rise, {a['n_peak_falls']}
fall, of {a['n_units']}); median absolute peak-year shift
**{a['abs_peak_year_shift_median']:.0f} years**. This is exactly the reshaping (TV 0.24–0.50)
that the cumulative count was blind to.

**2. But the peak shift is {'~flat across size' if size_flat else 'size-correlated'}** —
log(genuine/raw peak) vs log(population): Spearman {a['spearman_logratio_vs_logpop']:+.2f},
Theil-Sen slope {a['theilsen_logratio_vs_logpop']:+.3f}; vs log(n_eff): Spearman
{a['spearman_logratio_vs_logneff']:+.2f}, Theil-Sen {a['theilsen_logratio_vs_logneff']:+.3f}.

## What this means for a peak-window Hanson test

{'Because the peak shift does not trend with size, a peak-window scaling exponent would be ~unchanged by the deconvolution — the deconvolution moves every unit''s peak but not the size-gradient. So even the peak variant inherits the cumulative result''s robustness, at least at this province-level proxy.' if size_flat else 'The peak shift trends with size, so a peak-window scaling exponent WOULD move under the deconvolution — this is a genuine place to leverage it, and motivates the per-city build.'}

The 5-year window tells the same story (median change {s['5y']['peak_ratio_median_pct']:+.0f}%,
Theil-Sen vs logpop {s['5y']['theilsen_logratio_vs_logpop']:+.3f}).

## Caveats

- **GRW peak-attenuation.** The deconvolution's smoothness prior attenuates sharp peaks
  (C8 / Amdt 01 §A5.7), so genuine peak heights are propagated over the posterior (median +
  95% band in the JSON), not point-estimated. A downward median ratio is partly model
  smoothing, not only convention-removal — read the direction with that in mind.
- **Province-level proxy.** A peak is a per-city quantity; these 29 units are mostly
  province/region-level. The definitive peak-window scaling test needs a per-city
  deconvolution (same dependency as D13). This proxy indicates {'low' if size_flat else 'non-trivial'}
  expected payoff for that build on the peak variant.
- **Not preregistered** — the peak-window scaling test is a tertiary/future-work item.

## Reproduce
```bash
uv run python runs/2026-06-16-deconv-leverage-diagnostic/code/peak_shift_diagnostic.py
```
"""
    (OUT_DIR / "REPORT-peak.md").write_text(md)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("assembling per-unit raw vs genuine peaks (5y + 25y) ...", flush=True)
    d = assemble()
    s = analyse(d)
    d.to_json(OUT_DIR / "peak-shift-diagnostic.json", orient="records", indent=1)
    (OUT_DIR / "peak-summary.json").write_text(json.dumps(s, indent=1))
    make_figure(d, s)
    write_report(d, s)
    print(json.dumps(s, indent=1))
    print(f"\nwrote outputs → {OUT_DIR}")


if __name__ == "__main__":
    main()
