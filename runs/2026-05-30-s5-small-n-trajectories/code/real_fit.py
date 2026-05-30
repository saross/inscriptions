#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
real_fit.py — §5 Layer-A single-city fits on two real cities.
=============================================================

Fit ``model.py`` to two real prepared cities and report convergence plus the
posterior-median 16-bin trajectory:

- One mid-sized TARGET city (``--target-city``, default Lugdunum, N~151).
- One LARGE anchor (``--anchor-city``, default Pompeii, N~4266) — Pompeii also
  gives the AD 79 external-terminus sanity check (genuine post-79 mass should be
  near zero).

For each city the script prints the posterior-median ``lam`` per bin with its
95% credible interval, overlays the city's RAW aoristic summed-probability
array (SPA = column sums of ``A``, the model-free "expected counts per bin"),
and saves a 2-panel PNG comparing posterior trajectory vs raw SPA.

Run (on zbook, in the venv, with the threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/real_fit.py

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-30, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model as m  # noqa: E402
import dataprep as dp  # noqa: E402

EDGES = dp.BIN_EDGES                # length 17
BIN_LO = EDGES[:-1].astype(int)     # lower edge of each bin
BIN_HI = EDGES[1:].astype(int)      # upper edge of each bin


def raw_spa(A: np.ndarray) -> np.ndarray:
    """Model-free aoristic summed-probability array: expected counts per bin.

    With our "fraction of bin covered" weights, the natural per-bin expected
    count is the column sum of the per-inscription PROBABILITY mass. We convert
    the bin-coverage weight ``a[i,t]`` to the inscription's probability mass in
    bin ``t`` (``a[i,t] * BIN_WIDTH / interval_length_i``) and sum over
    inscriptions, so each inscription contributes total mass 1.0 — the standard
    aoristic SPA. This is the model-free comparator for the fitted ``lam``.

    Args:
        A: Aoristic weight matrix ``(N, T)``.

    Returns:
        Length-``T`` array of expected counts per bin (sums to ``N``).
    """
    lengths = A.sum(axis=1) * dp.BIN_WIDTH          # clipped interval length per insc
    prob = (A * dp.BIN_WIDTH) / lengths[:, None]    # row-normalised to sum 1
    return prob.sum(axis=0)


def fit_one(out_dir: Path, city: str, draws: int, tune: int, chains: int,
            target_accept: float, seed: int, escalate: bool) -> dict:
    """Fit one city, applying the convergence gates with a single escalation."""
    bundle = dp.load_city(out_dir, city)
    A = bundle["A"]
    n = A.shape[0]
    print(f"\n--- Fitting {city}  (N={n}, province={bundle['province']}) ---")

    idata = m.fit(A, draws=draws, tune=tune, chains=chains,
                  target_accept=target_accept, random_seed=seed,
                  progressbar=False)
    conv = m.convergence_summary(idata)
    passed = m.gates_pass(conv)
    print(f"  pass {passed}: max R-hat {conv['max_rhat']:.4f}  "
          f"min ESS {conv['min_ess_bulk']:.0f}  div {conv['n_divergences']}  "
          f"(worst R-hat: {conv['worst_rhat_param']}, "
          f"worst ESS: {conv['worst_ess_param']})")

    if not passed and escalate:
        d2, t2 = draws * 2, tune * 2
        print(f"  GATE MISS -> escalating ONCE to tune={t2}, draws={d2} "
              f"(gate NOT relaxed)")
        idata = m.fit(A, draws=d2, tune=t2, chains=chains,
                      target_accept=target_accept, random_seed=seed + 1,
                      progressbar=False)
        conv = m.convergence_summary(idata)
        passed = m.gates_pass(conv)
        print(f"  after escalation pass {passed}: max R-hat {conv['max_rhat']:.4f}  "
              f"min ESS {conv['min_ess_bulk']:.0f}  div {conv['n_divergences']}")

    lam = idata.posterior["lam"]
    lam_med = lam.median(("chain", "draw")).values
    lam_lo = lam.quantile(0.025, ("chain", "draw")).values
    lam_hi = lam.quantile(0.975, ("chain", "draw")).values
    spa = raw_spa(A)

    print(f"  {'bin':>3} {'years':>11} {'lam_med':>8} "
          f"{'95% CI':>17} {'raw SPA':>8}")
    for t in range(dp.N_BINS):
        print(f"  {t:>3} [{BIN_LO[t]:>4},{BIN_HI[t]:>4}) "
              f"{lam_med[t]:>8.2f} "
              f"[{lam_lo[t]:>6.2f},{lam_hi[t]:>6.2f}] {spa[t]:>8.2f}")

    return {
        "city": city, "N": int(n), "province": bundle["province"],
        "passed": bool(passed), "conv": conv,
        "lam_med": lam_med.tolist(), "lam_lo": lam_lo.tolist(),
        "lam_hi": lam_hi.tolist(), "raw_spa": spa.tolist(),
    }


def save_png(results: list[dict], png_path: Path) -> None:
    """Save a 2-panel PNG: posterior trajectory (+95% CI) vs raw aoristic SPA."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, len(results), figsize=(6 * len(results), 4.2),
                             squeeze=False)
    centres = (BIN_LO + BIN_HI) / 2
    for ax, res in zip(axes[0], results):
        lam_med = np.array(res["lam_med"])
        lo = np.array(res["lam_lo"])
        hi = np.array(res["lam_hi"])
        spa = np.array(res["raw_spa"])
        ax.fill_between(centres, lo, hi, alpha=0.25, color="C0",
                        label="95% CI (posterior)")
        ax.plot(centres, lam_med, "-o", color="C0", ms=3,
                label="posterior median lam")
        ax.plot(centres, spa, "--s", color="C3", ms=3, alpha=0.8,
                label="raw aoristic SPA")
        ax.axvline(79, color="grey", ls=":", lw=1)  # AD 79 (Pompeii terminus)
        ax.set_title(f"{res['city']} (N={res['N']})")
        ax.set_xlabel("year (AD; negative = BC)")
        ax.set_ylabel("expected inscriptions / 25y bin")
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(png_path, dpi=130)
    print(f"\nPNG -> {png_path}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target-city", default="Lugdunum")
    p.add_argument("--anchor-city", default="Pompeii")
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--no-escalate", action="store_true")
    p.add_argument("--out-dir", type=Path,
                   default=Path(__file__).resolve().parent / "prepared")
    p.add_argument("--png", type=Path,
                   default=Path(__file__).resolve().parent / "real-fit-trajectories.png")
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "real-fit-results.json")
    args = p.parse_args()

    results = []
    for city in (args.target_city, args.anchor_city):
        results.append(fit_one(
            args.out_dir, city, args.draws, args.tune, args.chains,
            args.target_accept, args.seed, escalate=not args.no_escalate))

    save_png(results, args.png)
    args.results.write_text(json.dumps(results, indent=2))
    print(f"Results JSON -> {args.results}")

    # Pompeii AD 79 sanity note: report mass in bins entirely after AD 79.
    for res in results:
        if res["city"] == "Pompeii":
            lam_med = np.array(res["lam_med"])
            post79_bins = BIN_LO >= 75  # bins starting at/after AD 75 (~79)
            print(f"\nPompeii AD-79 check: posterior-median expected counts in "
                  f"bins starting >= AD 75 = "
                  f"{lam_med[post79_bins].sum():.1f} "
                  f"(of total {lam_med.sum():.1f}); "
                  f"these should be small if the terminus is respected — but "
                  f"note aoristic template-smearing of wide intervals will "
                  f"leak some mass past 79.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
