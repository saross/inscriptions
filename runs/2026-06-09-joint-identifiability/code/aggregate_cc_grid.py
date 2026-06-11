#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aggregate_cc_grid.py — pilot comparison + full verdict for the cross-classified arm.
====================================================================================

Two modes:

* ``--pilot`` — reads all three pilot arm dirs (``outputs/grid-cc-<arm>-pilot/``)
  plus the lead's results on the same cells (``outputs/grid/``) and emits the
  arm-decision table → ``outputs/cc-PILOT-REPORT.md`` (signoff §5 step 4 gate).
* ``--pconv-mode <arm>`` — scores the arm's FULL grid (``outputs/grid-cc-<arm>/``)
  against the acceptance criteria (`full-grid-spec.md` §3) and the four adoption
  criteria (`cross-classified-spec.md` §5), head-to-head with the lead. The C2
  baseline numbers are REUSED from the lead grid's per-cell JSONs (same ``y``
  draws by construction — signoff §3); no baseline re-fit exists or is needed.
  Emits ``outputs/cc-VERDICT-<arm>.md`` + ``outputs/cc-summary-<arm>.json``.

Run — PATH=~/.local/bin:$PATH uv run python code/aggregate_cc_grid.py [--pilot]
      [--pconv-mode library]

Author / Date — Claude Code (Fable 5) on Shawn's brief, 2026-06-11. UK/Aus English.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

RUN = Path("/home/shawn/Code/inscriptions/runs/2026-06-09-joint-identifiability")
LEAD_DIR = RUN / "outputs" / "grid"
ARMS = ("tiers3", "library", "free")
BETTER_MARGIN = 0.05   # C2 "materially better than baseline" margin (as the lead)


def load_dir(d: Path) -> dict[str, dict]:
    """cell_id → cell record, for every parseable JSON in a results dir (missing
    dirs yield an empty dict). Includes fully-failed cells — callers must filter
    with `scorable` before averaging (NaN-poisoning audit finding)."""
    out: dict[str, dict] = {}
    for p in sorted(d.glob("*.json")):
        try:
            c = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        out[c["cell_id"]] = c
    return out


def scorable(cells: dict[str, dict]) -> dict[str, dict]:
    """The subset of a `load_dir` result that is safe to average over."""
    return {cid: c for cid, c in cells.items()
            if c.get("n_ok", 0) > 0 and c.get("bias_median") is not None}


def regime_stats(cells: list[dict]) -> dict:
    """Mean bias / |bias| / coverage / convergence over a (scorable) cell list."""
    if not cells:
        return {"n": 0}
    bm = np.array([c["bias_median"] for c in cells], dtype=float)
    cov = np.array([c["coverage_rate"] for c in cells], dtype=float)
    cr = np.array([c["convergence_rate"] for c in cells], dtype=float)
    return {"n": len(cells), "bias_median_mean": float(bm.mean()),
            "abs_bias_mean": float(np.abs(bm).mean()),
            "coverage_mean": float(cov.mean()), "convergence_mean": float(cr.mean())}


def fmt(s: dict) -> str:
    """One regime-summary table fragment: '| n | bias | |bias| | cov | conv '."""
    if s["n"] == 0:
        return "| · | · | · | · | · "
    return (f"| {s['n']} | {s['bias_median_mean']:+.3f} | {s['abs_bias_mean']:.3f} "
            f"| {s['coverage_mean']:.3f} | {s['convergence_mean']:.3f} ")


def pilot_report() -> None:
    """The 3-arm p_conv comparison over the pilot cells (signoff §5 step 4 gate)."""
    lead = scorable(load_dir(LEAD_DIR))
    raw_arms = {a: load_dir(RUN / "outputs" / f"grid-cc-{a}-pilot") for a in ARMS}
    arms = {a: scorable(v) for a, v in raw_arms.items()}
    n_failed = {a: len(raw_arms[a]) - len(arms[a]) for a in ARMS}
    pilot_ids = sorted(set().union(*[set(v) for v in arms.values()]))
    if not pilot_ids:
        print("no pilot results yet.")
        return
    if not lead:
        print("WARNING: no lead results found at outputs/grid/ — reference rows will be "
              "empty. Run this on the host that holds the lead grid (sapphire).")

    lines = ["# Cross-classified arm — PILOT report (3-arm p_conv decision gate)", "",
             f"Pilot cells with any arm results: {len(pilot_ids)}. "
             f"Per-arm scorable: " +
             ", ".join(f"{a} {len(arms[a])}" for a in ARMS) +
             ". Fully-failed (excluded): " +
             ", ".join(f"{a} {n_failed[a]}" for a in ARMS) + ".", "",
             "## Regime summary (mean over cells; aggregates over converged reps)", "",
             "| arm | regime | n | mean med-bias | mean \\|bias\\| | coverage | conv |",
             "|---|---|---|---|---|---|---|"]
    for regime in ("identifiable", "confounded"):
        ref = [c for cid, c in lead.items() if cid in pilot_ids and c["regime"] == regime]
        lines.append(f"| **lead (ref)** | {regime} {fmt(regime_stats(ref))}|")
        for a in ARMS:
            sub = [c for c in arms[a].values() if c["regime"] == regime]
            lines.append(f"| {a} | {regime} {fmt(regime_stats(sub))}|")

    # Boundary-coverage breakdown: an equal-tailed 95% CI can NEVER cover a
    # boundary truth (alpha_lo > 0 always), so alpha_true = 0 cells report
    # coverage ~0 by construction — separate them so the headline is readable.
    lines += ["", "## Coverage breakdown — boundary artefact (α_true = 0 cells "
              "cannot be covered by an equal-tailed CI)", "",
              "| arm | coverage (α = 0 cells) | coverage (α > 0 cells) |",
              "|---|---|---|"]
    for a in ("lead",) + ARMS:
        cells_a = ([c for cid, c in lead.items() if cid in pilot_ids] if a == "lead"
                   else list(arms[a].values()))
        zero = [c["coverage_rate"] for c in cells_a if c["alpha_true"] == 0.0]
        nonz = [c["coverage_rate"] for c in cells_a if c["alpha_true"] > 0.0]
        z = f"{float(np.mean(zero)):.3f} (n={len(zero)})" if zero else "·"
        nz = f"{float(np.mean(nonz)):.3f} (n={len(nonz)})" if nonz else "·"
        lines.append(f"| {a} | {z} | {nz} |")
    lines += ["", "## Per-cell α median-bias (cc arms vs lead)", "",
              "| cell | regime | α | lead | tiers3 | library | free |",
              "|---|---|---|---|---|---|---|"]
    for cid in pilot_ids:
        anyrec = next((arms[a][cid] for a in ARMS if cid in arms[a]), None) or lead.get(cid)
        if anyrec is None:
            continue
        cols = []
        for src in (lead, arms["tiers3"], arms["library"], arms["free"]):
            c = src.get(cid)
            cols.append(f"{c['bias_median']:+.3f}" if c and c.get("bias_median") is not None
                        else "·")
        lines.append(f"| {cid} | {anyrec['regime']} | {anyrec['alpha_true']:.1f} | "
                     + " | ".join(cols) + " |")
    # Timing — drives the full-run wall-clock projection (signoff §4 hard-stop).
    lines += ["", "## Timing (per-fit seconds, per arm)", ""]
    for a in ARMS:
        ts = [c.get("secs_per_fit") for c in arms[a].values() if c.get("secs_per_fit")]
        if ts:
            proj = float(np.mean(ts)) * 300 * 100 / 12 / 3600
            lines.append(f"- {a}: mean {float(np.mean(ts)):.1f} s/fit "
                         f"(max {float(np.max(ts)):.1f}) → full 300×100 @ n_jobs=12 ≈ "
                         f"**{proj:.1f} h**")
    lines += ["", "Decision criteria, in order (signoff §5): confounded bias profile; "
              "identifiable bias flatness; coverage; convergence. Ties → `library`.", ""]
    out = RUN / "outputs" / "cc-PILOT-REPORT.md"
    out.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\nWrote {out}")


def full_verdict(mode: str) -> None:
    """Score one arm's full grid against §3 criteria + §5 adoption, vs the lead."""
    lead = load_dir(LEAD_DIR)
    cc = load_dir(RUN / "outputs" / f"grid-cc-{mode}")
    if not cc:
        print(f"no full-grid results for arm {mode!r} yet.")
        return
    if not lead:
        raise SystemExit(
            f"FATAL: no lead per-cell results at {LEAD_DIR} — the C2 baseline and the "
            "head-to-head need them. Run this on the host that holds the lead grid "
            "(sapphire); a verdict without them would silently report C2 = 0.")
    scored = [c for c in cc.values() if c.get("n_ok", 0) > 0 and c.get("bias_median") is not None]
    failed = [c for c in cc.values() if c.get("n_ok", 0) == 0]
    ident = [c for c in scored if c["regime"] == "identifiable"]
    conf = [c for c in scored if c["regime"] == "confounded"]

    lines = [f"# Cross-classified grid — VERDICT (arm: {mode})", "",
             f"Cells with usable data: {len(scored)} ({len(ident)} identifiable, "
             f"{len(conf)} confounded). Fully-failed cells (n_ok=0): **{len(failed)}**"
             + (f" — {[c['cell_id'] for c in failed]}" if failed else "") + ".", ""]

    # C1 — do-no-harm (identifiable).
    c1 = 0
    if ident:
        b = np.abs([c["bias_median"] for c in ident])
        cov = np.array([c["coverage_rate"] for c in ident])
        c1 = int(np.sum((b < 0.12) & (cov >= 0.90)))
        nz = [c["coverage_rate"] for c in ident if c["alpha_true"] > 0.0]
        nz_note = (f"- coverage on α>0 cells only: {float(np.mean(nz)):.3f} (n={len(nz)}) — "
                   "α=0 cells cannot be covered by an equal-tailed CI (boundary artefact)"
                   if nz else "")
        lines += ["## C1 — do-no-harm (identifiable)",
                  f"- passing (|median bias|<0.12 AND coverage>=0.90): **{c1}/{len(ident)}** "
                  f"({100*c1/len(ident):.0f}%)  [lead: 37/210, 18%]",
                  f"- mean |median bias| {b.mean():.3f} [lead 0.075]; "
                  f"mean coverage {cov.mean():.3f} [lead 0.374]"] \
            + ([nz_note] if nz_note else []) + [""]

    # C2 — pulled-to-truth (confounded); baseline reused from the lead grid files.
    c2 = 0
    if conf:
        bm = np.array([c["bias_median"] for c in conf])
        cov = np.array([c["coverage_rate"] for c in conf])
        base_raw = [(lead.get(c["cell_id"]) or {}).get("baseline_abs_bias_median")
                    for c in conf]
        base = np.array([b if b is not None else np.nan for b in base_raw], dtype=float)
        cc_abs = np.abs(bm)
        better = (cc_abs + BETTER_MARGIN) < base          # NaN → False (baseline missing)
        passing = (cc_abs < 0.18) & (bm <= 0.12) & better
        c2 = int(np.sum(passing))
        lines += ["## C2 — pulled-to-truth (confounded; baseline from the lead grid)",
                  f"- passing (|median bias|<0.18 AND bias<=+0.12 AND >baseline by "
                  f"{BETTER_MARGIN}): **{c2}/{len(conf)}** ({100*c2/len(conf):.0f}%)  "
                  f"[lead: 64/90, 71%]",
                  f"- mean median bias {bm.mean():+.3f} [lead +0.066]; "
                  f"mean coverage {cov.mean():.3f} [lead 0.462]",
                  f"- worst positive median bias {max(float(bm.max()), 0.0):+.3f}",
                  f"- cells with baseline available: {int((~np.isnan(base)).sum())}/{len(conf)}; "
                  f"mean cc |bias| {cc_abs.mean():.3f} vs baseline |bias| "
                  f"{np.nanmean(base):.3f}", ""]

    # C4 — convergence.
    conv = np.array([c["convergence_rate"] for c in scored
                     if c.get("convergence_rate") is not None])
    if conv.size:
        lines += ["## C4 — convergence",
                  f"- cells with convergence_rate>=0.95: "
                  f"**{int(np.sum(conv>=0.95))}/{conv.size}** "
                  f"({100*np.mean(conv>=0.95):.0f}%) [lead 84%]; "
                  f"mean rate {conv.mean():.3f} [lead 0.950]", ""]

    # Bias surface over %win × α_true.
    lines += ["## Bias surface — mean(median bias) by %win × α_true", ""]
    wins = sorted({c["conv_pct_win"] for c in scored})
    alphas = sorted({c["alpha_true"] for c in scored})
    lines += ["| %win \\ α | " + " | ".join(f"{a:.1f}" for a in alphas) + " |",
              "|" + "---|" * (len(alphas) + 1)]
    for w in wins:
        row = [f"| {w:.2f} "]
        for a in alphas:
            sub = [c for c in scored if c["conv_pct_win"] == w and c["alpha_true"] == a]
            row.append(f"| {np.mean([c['bias_median'] for c in sub]):+.2f} " if sub else "| · ")
        lines.append("".join(row) + "|")

    # The four adoption criteria (cross-classified-spec.md §5), head-to-head.
    ident_bias = float(np.mean(np.abs([c["bias_median"] for c in ident]))) if ident else None
    ident_cov = float(np.mean([c["coverage_rate"] for c in ident])) if ident else None
    conf_abs = float(np.mean(np.abs([c["bias_median"] for c in conf]))) if conf else None
    c4_rate = float(np.mean(conv >= 0.95)) if conv.size else None
    adoption = {
        "1_bias_flattens (ident |bias| < lead 0.075)": ident_bias,
        "2_C1_recovers (ident coverage > lead 0.374, toward 0.90)": ident_cov,
        "3_C2_not_sacrificed (conf |bias| stays << baseline 0.362)": conf_abs,
        "4_C4_not_worse (cell pass-rate >= lead 0.84)": c4_rate,
    }
    lines += ["", "## Adoption criteria (cross-classified-spec.md §5)", ""]
    for kk, vv in adoption.items():
        lines.append(f"- {kk}: **{vv:.3f}**" if vv is not None else f"- {kk}: n/a")
    rep_fails = sum(c.get("n_failed", 0) for c in cc.values())
    lines += ["", "## Overall",
              f"- replicate failures: {rep_fails}; fully-failed cells: {len(failed)}",
              f"- grid scope: %win {wins}, α {alphas}, N {sorted({c['N'] for c in scored})}", ""]

    (RUN / "outputs" / f"cc-VERDICT-{mode}.md").write_text("\n".join(lines))
    (RUN / "outputs" / f"cc-summary-{mode}.json").write_text(json.dumps(
        {"arm": mode, "n_cells_total": len(cc), "n_scored": len(scored),
         "n_failed": len(failed), "c1_pass": c1, "c2_pass": c2,
         "adoption": adoption,
         "cells": [{k: c.get(k) for k in ("cell_id", "regime", "conv_pct_win",
                                          "alpha_true", "gen_name", "N", "bias_median",
                                          "coverage_rate", "convergence_rate",
                                          "mean_ci_halfwidth", "n_ok", "n_converged",
                                          "n_failed", "secs_per_fit")}
                   for c in cc.values()]}, indent=1))
    print("\n".join(lines))
    print(f"\nWrote cc-VERDICT-{mode}.md + cc-summary-{mode}.json")


def main() -> None:
    """CLI: exactly one of --pilot (arm comparison) or --pconv-mode (full verdict)."""
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--pilot", action="store_true", help="3-arm pilot comparison report")
    group.add_argument("--pconv-mode", choices=ARMS, default=None,
                       help="full-grid verdict for one arm")
    args = ap.parse_args()
    if args.pilot:
        pilot_report()
    else:
        full_verdict(args.pconv_mode)


if __name__ == "__main__":
    main()
