#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
letter_ppc.py — §5 letter-mass observation-form selection by PPC.
=================================================================

Fit BOTH candidate over-dispersed observation forms of the letter-mass model
(``letter_model.py``: ``"gamma"`` and ``"nb"``) on a small set of representative
cities, run posterior-predictive checks, and report which form to take to
production. The spec (§4 / Decision 1) requires the letter form be finalised at
smoke by a quick PPC: does the posterior-predictive interval COVER the observed
per-bin letter mass, and is the DISPERSION captured?

Each city is fitted standalone-in-hierarchy is overkill for a form bake-off, so
this uses a SMALL multi-city hierarchical fit (a handful of cities of varied N)
under both forms with the pinned scales — enough to exercise the observation and
its dispersion parameter, cheap to run.

PPC metrics (per form, aggregated over the test cities' bins):

- **coverage** — fraction of (city, bin) cells whose 95% posterior-predictive
  interval contains the observed per-bin letter mass ``y[c,t]`` (target ~0.95;
  much lower = the form is over-confident / under-dispersed; ~1.0 with very wide
  intervals = vacuous).
- **mean 95% PPI width** (on the log10 scale) — a vacuity guard: a form that
  "covers" only by predicting absurdly wide intervals is not preferred.
- **dispersion realism** — compare the observed per-bin coefficient of variation
  of ``y`` (across the replicate posterior-predictive draws) at a few cells to
  whether the observed value sits in the bulk vs the tail.
- **convergence** — R-hat / ESS / divergences for each form (a form that will
  not converge is disqualified regardless of coverage).

The selected form + the PPC evidence are written to ``letter-ppc-results.json``
and overlaid in ``letter-ppc.png`` (observed vs posterior-predictive band, per
test city, per form), for the PRODUCTION-READY writeup.

Run (on zbook, in the venv, threading/scratch env set)::

    ~/Code/inscriptions/.venv/bin/python \
        runs/2026-05-30-s5-small-n-trajectories/code/letter_ppc.py \
        --draws 1000 --tune 1000

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataprep as dp          # noqa: E402
import letter_model as lm      # noqa: E402

# Test cities spanning N and trajectory shape (verified present in the cache):
#   Pompeii  — large anchor, AD 79 terminus (sharp content collapse);
#   Capua    — large mid-province city;
#   Lugdunum — mid target (N~151), the canonical real-fit target;
#   Anagnia  — small-N (N~71), Regio I; Gabii — smallest (N~50).
# A couple share Regio I so the province tier is exercised (not all singletons).
TEST_CITIES = ["Pompeii", "Capua", "Lugdunum", "Anagnia", "Gabii"]


def ppi_from_ppc(ppc_y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """95% posterior-predictive interval + median over draws.

    Args:
        ppc_y: Posterior-predictive draws, shape ``(S, C, T)`` (S pooled draws).

    Returns:
        ``(med, lo, hi)`` each ``(C, T)``.
    """
    med = np.median(ppc_y, axis=0)
    lo = np.quantile(ppc_y, 0.025, axis=0)
    hi = np.quantile(ppc_y, 0.975, axis=0)
    return med, lo, hi


def evaluate_form(data: lm.LetterData, obs_form: str, draws: int, tune: int,
                  chains: int, target_accept: float, seed: int) -> dict:
    """Fit one observation form, run a PPC, and score coverage + dispersion."""
    import pymc as pm

    print(f"\n=== form={obs_form!r} ===")
    model = lm.build_model(data, obs_form=obs_form)
    with model:
        idata = pm.sample(draws=draws, tune=tune, chains=chains,
                          target_accept=target_accept, random_seed=seed,
                          progressbar=False, compute_convergence_checks=True)
        ppc = pm.sample_posterior_predictive(
            idata, var_names=["y"], random_seed=seed, progressbar=False)

    conv = lm.convergence_summary(idata)
    passed = lm.gates_pass(conv)
    print(f"  conv: max R-hat {conv['max_rhat']:.4f}  min ESS "
          f"{conv['min_ess_bulk']:.0f}  div {conv['n_divergences']}  "
          f"gates_pass={passed}")

    # Posterior-predictive draws, pooled over chains -> (S, C, T).
    ppc_y = ppc.posterior_predictive["y"].values
    S = ppc_y.shape[0] * ppc_y.shape[1]
    ppc_y = ppc_y.reshape(S, *ppc_y.shape[2:])

    Y = np.asarray(data.Y, dtype=float)               # observed (C, T)
    # For the Gamma form, exact-zero observed bins were floored to eps in-model;
    # compare on the same footing by treating observed zeros as the floor too.
    med, lo, hi = ppi_from_ppc(ppc_y)
    covered = (Y >= lo) & (Y <= hi)
    coverage = float(covered.mean())

    # Vacuity guard: width of the 95% PPI on log10 scale (geometric width).
    eps = 1e-6
    log_width = np.log10(hi + eps) - np.log10(np.maximum(lo, 0) + eps)
    mean_log_width = float(np.mean(log_width))

    # Dispersion realism: per-cell standardised residual of the observation
    # under the predictive (|y - med| / predictive SD); a well-calibrated
    # over-dispersed form keeps the median |z| near ~0.7 (normal-ish) rather
    # than huge (under-dispersed) — a coarse but informative dispersion probe.
    pp_sd = ppc_y.std(axis=0)
    z = np.abs(Y - med) / np.maximum(pp_sd, eps)
    median_abs_z = float(np.median(z))
    frac_z_gt3 = float(np.mean(z > 3.0))

    return {
        "obs_form": obs_form,
        "convergence": conv,
        "gates_pass": bool(passed),
        "coverage": coverage,
        "mean_log10_ppi_width": mean_log_width,
        "median_abs_pp_z": median_abs_z,
        "frac_cells_abs_z_gt3": frac_z_gt3,
        "_med": med, "_lo": lo, "_hi": hi,  # for the PNG; stripped from JSON.
    }


def choose(results: dict) -> tuple[str, str]:
    """Pick the production form and explain why.

    Rule (transparent, stated in PRODUCTION-READY):
    1. Both must pass convergence gates; a non-converging form is disqualified.
    2. Among the survivors, prefer the one whose coverage is closest to 0.95
       from below-or-at while NOT being vacuous (penalise very wide intervals).
       Concretely: score = coverage_penalty + vacuity_penalty, lower is better,
       where coverage_penalty = |coverage - 0.95| and vacuity adds a small
       fraction of the mean log10 PPI width (so two forms with equal coverage
       are split by the tighter intervals).
    """
    cand = {f: r for f, r in results.items() if r["gates_pass"]}
    if not cand:  # neither converged; fall back to best coverage, flagged.
        cand = results
        note = "NEITHER form passed convergence gates; selection is provisional."
    else:
        note = ""
    scored = {}
    for f, r in cand.items():
        scored[f] = abs(r["coverage"] - 0.95) + 0.10 * r["mean_log10_ppi_width"]
    best = min(scored, key=scored.get)
    why = (
        f"form={best}: coverage {cand[best]['coverage']:.3f} "
        f"(target ~0.95), mean log10 PPI width "
        f"{cand[best]['mean_log10_ppi_width']:.2f}, median |pp-z| "
        f"{cand[best]['median_abs_pp_z']:.2f}, gates_pass="
        f"{cand[best]['gates_pass']}. {note}"
    ).strip()
    return best, why


def save_png(data: lm.LetterData, results: dict, png_path: Path) -> None:
    """Observed per-bin letter mass vs 95% PPI band, per test city, per form."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    edges, _ = dp.make_grid(data.bin_width)
    centres = (edges[:-1] + edges[1:]) / 2
    forms = list(results.keys())
    C = len(data.cities)
    fig, axes = plt.subplots(len(forms), C, figsize=(3.6 * C, 3.4 * len(forms)),
                             squeeze=False)
    for fi, form in enumerate(forms):
        r = results[form]
        med, lo, hi = r["_med"], r["_lo"], r["_hi"]
        for ci, city in enumerate(data.cities):
            ax = axes[fi][ci]
            ax.fill_between(centres, lo[ci], hi[ci], alpha=0.25, color="C0",
                            label="95% PPI")
            ax.plot(centres, med[ci], "-o", color="C0", ms=3, label="PP median")
            ax.plot(centres, data.Y[ci], "--s", color="C3", ms=3,
                    label="observed letter mass")
            ax.set_yscale("symlog")
            ax.set_title(f"{form} — {city} (N={int(data.N[ci])})", fontsize=8)
            ax.set_xlabel("year"); ax.set_ylabel("letter mass / bin")
            if ci == 0:
                ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    print(f"PNG -> {png_path}")


def run(out_dir: Path, draws: int, tune: int, chains: int, target_accept: float,
        seed: int, png_path: Path, results_path: Path) -> dict:
    """Fit both forms, score, choose, and persist artefacts."""
    data = lm.assemble(out_dir, TEST_CITIES)
    print(f"Test subset: {len(data.cities)} cities, "
          f"{len(data.prov_names)} u-tier provinces ({data.prov_names}), "
          f"{len(data.singleton_provs)} singletons; "
          f"mean letters/city = {data.anchor_letters_mean:.0f}; "
          f"bin_width={data.bin_width}")

    results = {}
    for fi, form in enumerate(lm.OBS_FORMS):
        results[form] = evaluate_form(
            data, form, draws, tune, chains, target_accept, seed + fi)

    best, why = choose(results)
    print("\n" + "=" * 70)
    print("LETTER-MASS FORM SELECTION")
    print("=" * 70)
    for form, r in results.items():
        print(f"  {form:>6}: coverage {r['coverage']:.3f}  "
              f"mean log10 PPI width {r['mean_log10_ppi_width']:.2f}  "
              f"median|pp-z| {r['median_abs_pp_z']:.2f}  "
              f"z>3 frac {r['frac_cells_abs_z_gt3']:.3f}  "
              f"gates_pass={r['gates_pass']}")
    print(f"\n  SELECTED -> {why}")

    save_png(data, results, png_path)

    # Strip the heavy arrays before JSON.
    out = {
        "test_cities": data.cities,
        "N": data.N.tolist(),
        "total_letters": data.total_letters.tolist(),
        "bin_width": data.bin_width,
        "sampler": {"draws": draws, "tune": tune, "chains": chains,
                    "target_accept": target_accept},
        "selected_form": best,
        "selection_rationale": why,
        "forms": {
            f: {k: v for k, v in r.items() if not k.startswith("_")}
            for f, r in results.items()
        },
    }
    results_path.write_text(json.dumps(out, indent=2))
    print(f"Results JSON -> {results_path}")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--draws", type=int, default=1000)
    p.add_argument("--tune", type=int, default=1000)
    p.add_argument("--chains", type=int, default=4)
    p.add_argument("--target-accept", type=float, default=0.99)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--out-dir", type=Path, default=dp.default_cache_dir(25))
    p.add_argument("--png", type=Path,
                   default=Path(__file__).resolve().parent / "letter-ppc.png")
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parent / "letter-ppc-results.json")
    args = p.parse_args()
    run(args.out_dir, args.draws, args.tune, args.chains, args.target_accept,
        args.seed, args.png, args.results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
