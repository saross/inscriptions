#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag-probe.py — descriptive sanity probe for the unexpected-alpha units.

For each probe unit, report: the fitted alpha; the aoristic-mass family
composition (Tight / F1_round / F3_periodic / F2_Other / Big); date-range width
stats; and — the decisive bit — the TEMPORAL CENTROID + spread of the unit's own
F1+F3 (round-period) mass vs the shared convention basis. If a low-alpha unit has
substantial F1+F3 mass that is concentrated in a window the shared basis does not
cover, that is basis-misfit (alpha wrongly low), not genuine precision.
Read-only; no fitting.
"""
from __future__ import annotations

import json
import numpy as np
import h2_lib as H

PROBE = [
    "Dacia", "Britannia", "Moesia inferior", "Pompeii",            # low-alpha
    "Noricum", "latin-aggregate", "Dalmatia", "Pannonia superior",  # high-alpha
    "Latium et Campania / Regio I", "Salona",                       # mid reference
]
FAMILIES = ["Tight", "F1_round", "F3_periodic", "F2_Other", "Big"]


def centroid_spread(spa: np.ndarray) -> tuple[float, float, float]:
    """Mass-weighted centroid year, sd (years), and fraction of mass in AD 100-275."""
    s = spa.sum()
    if s <= 0:
        return float("nan"), float("nan"), float("nan")
    p = spa / s
    mu = float((p * H.BIN_CENTRES).sum())
    sd = float(np.sqrt((p * (H.BIN_CENTRES - mu) ** 2).sum()))
    win = (H.BIN_CENTRES >= 100) & (H.BIN_CENTRES <= 275)
    return mu, sd, float(p[win].sum())


def main() -> int:
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    design = H.load_design()
    units = {u["name"]: u for u in H.enumerate_units()}
    summ = {r["name"]: r for r in json.loads(
        (H.PROJECT_ROOT / "runs/2026-06-07-h2.1-launch-prep/outputs/production/summary.json")
        .read_text(encoding="utf-8"))}

    # Shared bases' F1+F3-equivalent location: the empirical-weighted basis row.
    for frame in ("empire", "latin"):
        b = np.asarray(design[f"tier_basis_empirical{'' if frame=='empire' else '_latin'}"])
        w = design["provenance_counts"][frame]["tier_weights_empirical"]
        basis_spa = (np.asarray(w)[:, None] * b).sum(axis=0)
        mu, sd, win = centroid_spread(basis_spa)
        print(f"[basis:{frame}] convention-basis centroid={mu:.0f}AD sd={sd:.0f}y  frac in AD100-275={win:.2f}")
    print()

    for name in PROBE:
        u = units[name]
        sub = H.subset_corpus(df, u, latin)
        nb = sub["nb"].to_numpy(); na = sub["na"].to_numpy(); fam = sub["family"].to_numpy()
        width = na - nb
        total = H.aoristic_spa(nb, na).sum()
        comp = {f: H.aoristic_spa(nb[fam == f], na[fam == f]).sum() / total for f in FAMILIES}
        f1f3 = np.isin(fam, ["F1_round", "F3_periodic"])
        conv_spa = H.aoristic_spa(nb[f1f3], na[f1f3])
        cmu, csd, cwin = centroid_spread(conv_spa)
        tight_spa = H.aoristic_spa(nb[~f1f3 & (width <= 4)], na[~f1f3 & (width <= 4)])
        a = summ[name]["alpha_median"]
        # top exact templates
        import collections
        tops = collections.Counter(zip(nb.tolist(), na.tolist())).most_common(4)
        print(f"=== {name}  (alpha={a:.3f}, n={len(sub)}) ===")
        print("  family-mass: " + "  ".join(f"{f}={comp[f]:.2f}" for f in FAMILIES))
        print(f"  width: median={np.median(width):.0f}y  %tight(<=4)={100*(width<=4).mean():.0f}%  "
              f"%round-slab={100*np.isin(width,[24,49,99,149,199,299]).mean():.0f}%")
        print(f"  F1+F3 (convention) mass: frac={comp['F1_round']+comp['F3_periodic']:.2f}  "
              f"centroid={cmu:.0f}AD sd={csd:.0f}y  frac in AD100-275={cwin:.2f}")
        print(f"  top templates [nb,na]xN: " + "  ".join(f"[{a0},{b0}]x{n}" for (a0,b0),n in tops))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
