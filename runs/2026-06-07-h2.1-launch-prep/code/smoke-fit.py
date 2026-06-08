#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""smoke-fit.py — fit 1-2 real units end-to-end and print the acceptance
diagnostics, BEFORE the full 28-unit launch. Go/no-go gate for the production run.
"""
from __future__ import annotations

import sys
import numpy as np
import h2_lib as H


def main() -> int:
    probe = sys.argv[1:] or ["Aquileia", "Dalmatia"]  # near-floor city + comfy province
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    design = H.load_design()
    units = {u["name"]: u for u in H.enumerate_units()}

    ok = True
    for name in probe:
        u = units[name]
        sub = H.subset_corpus(df, u, latin)
        info = H.build_unit_y(sub)
        basis = H.select_basis(design, u["frame"])
        print(f"\n=== {name} ({u['tier']}, frame={u['frame']}) ===")
        print(f"  n_rows={info['n_rows']}  n_eff={info['n_eff']}  "
              f"F1+F3 family-mass frac={info['f1f3_family_mass_fraction']:.3f}")
        res = H.fit_unit(info["y"], basis, seed=H.BASE_SEED + u["unit_index"])
        pg = np.asarray(res["p_gen_median"])
        print(f"  alpha median={res['alpha_median']:.3f} "
              f"[{res['alpha_ci_lo']:.3f}, {res['alpha_ci_hi']:.3f}]  "
              f"(envelope alpha<=0.70: {res['in_envelope_alpha']})")
        print(f"  tier_weights median={[round(x,3) for x in res['tier_weights_median']]}")
        print(f"  convergence: max_rhat={res['max_rhat']:.4f}  "
              f"min_ess_bulk={res['min_ess_bulk']:.0f}  divergences={res['n_divergences']}  "
              f"-> PASS={res['convergence_pass']}")
        print(f"  PPC mae/N_eff={res['ppc_mae_frac']:.5f}  "
              f"| p_gen_median sum={pg.sum():.4f} (want ~1.0)  "
              f"min={pg.min():.5f} max={pg.max():.5f}")
        # descriptive-p_conv consistency: learned alpha vs F1+F3 family-mass frac
        print(f"  descriptive-p_conv check: learned alpha {res['alpha_median']:.3f} "
              f"vs F1+F3 family-mass frac {info['f1f3_family_mass_fraction']:.3f} "
              f"(should agree in regime)")
        if not res["convergence_pass"]:
            ok = False
            print("  ** WARNING: convergence FAILED for this unit")
        if not (0.95 <= pg.sum() <= 1.05):
            ok = False
            print("  ** WARNING: p_gen_median does not sum to ~1")

    print(f"\n[smoke-fit] {'PASS — ready to launch the full run' if ok else 'FAIL — do not launch; investigate'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
