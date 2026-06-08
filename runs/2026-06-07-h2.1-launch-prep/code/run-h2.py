#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-h2.py — orchestrate the H2.1 PRIMARY production run (launch-spec §9).

Fits the 28 units (26 primary + 2 grey-band) with the validated
build_model_f1_f3, in a parallel subprocess pool (one fit-unit.py per unit,
up to --n-jobs concurrent). Resumable (skips units whose output exists),
writes STATUS.txt, and emits a SUMMARY after all units complete.

SCOPE: this orchestrator runs the PRIMARY observation model only (largest-
remainder multinomial). The six supplementaries (launch-spec §6) are a
deliberately-separate, explicitly-staged next wave (see SUMMARY) — NOT run
unsupervised here.

Pre-flight: asserts TMPDIR is disk-backed with >= 20 GB free (the 2026-06-08
tmpfs ENOSPC lesson) and halts loudly otherwise.

Usage
-----
    TMPDIR=/home/shawn/.cache/inscriptions-pytensor-tmp \\
    PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False \\
    taskset -c 0-11 uv run python run-h2.py [--n-jobs 12] [--only 0,1,2]

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-08.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import h2_lib as H

UV = str(Path.home() / ".local" / "bin" / "uv")
DEFAULT_OUT = H.PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "outputs" / "production"


def preflight_tmpdir(min_gb: float = 20.0) -> None:
    tmp = os.environ.get("TMPDIR", "/tmp")
    Path(tmp).mkdir(parents=True, exist_ok=True)
    free_gb = shutil.disk_usage(tmp).free / 1e9
    is_tmpfs = False
    try:  # warn if TMPDIR is a (small) tmpfs, the failure mode we are guarding
        with open("/proc/mounts", encoding="utf-8") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) >= 3 and parts[1] == tmp and parts[2] == "tmpfs":
                    is_tmpfs = True
    except OSError:
        pass
    if free_gb < min_gb:
        sys.exit(f"[run-h2] ABORT (halt-and-report): TMPDIR={tmp} has {free_gb:.1f} GB "
                 f"free < {min_gb} GB. Point TMPDIR at the disk-backed root fs.")
    note = " (WARNING: tmpfs)" if is_tmpfs else ""
    print(f"[run-h2] pre-flight OK: TMPDIR={tmp} free {free_gb:.0f} GB{note}")


def build_units_data(out_dir: Path) -> tuple[Path, list[dict]]:
    """Load the corpus ONCE, build all 28 units' y + metadata, persist."""
    print("[run-h2] building per-unit y vectors (one corpus load) ...")
    df = H.load_filtered_lire()
    df["family"] = H.classify_family(df)
    latin = H.latin_provinces()
    units = H.enumerate_units()
    recs = []
    for u in units:
        info = H.build_unit_y(H.subset_corpus(df, u, latin))
        recs.append({
            **{k: u[k] for k in ("name", "kind", "frame", "tier", "unit_index")},
            "y": [int(x) for x in info["y"]],
            "n_eff": info["n_eff"], "n_rows": info["n_rows"],
            "f1f3_family_mass_fraction": info["f1f3_family_mass_fraction"],
        })
    path = out_dir / "units-data.json"
    path.write_text(json.dumps({"units": recs}), encoding="utf-8")
    print(f"[run-h2] wrote {path} ({len(recs)} units)")
    return path, units


def write_summary(out_dir: Path, units: list[dict]) -> None:
    """Tabulate per-unit results into SUMMARY.md + a machine-readable JSON."""
    udir = out_dir / "units"
    rows = []
    for u in units:
        p = udir / f"unit-{u['unit_index']:02d}.json"
        if p.exists():
            rows.append(json.loads(p.read_text(encoding="utf-8")))
    rows.sort(key=lambda r: r["unit_index"])
    (out_dir / "summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    from collections import Counter
    tiers = Counter(r["final_tier"] for r in rows)
    lines = ["# H2.1 primary run — SUMMARY", "",
             f"Units fitted: {len(rows)}/{len(units)}.  Final tiers: {dict(tiers)}.", "",
             "| idx | unit | tier | n_eff | alpha (95% CI) | conv | maxR̂ | div |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(
            f"| {r['unit_index']} | {r['name']} | {r['final_tier']} | {r['n_eff']} "
            f"| {r['alpha_median']:.3f} [{r['alpha_ci_lo']:.2f},{r['alpha_ci_hi']:.2f}] "
            f"| {'Y' if r['convergence_pass'] else 'N'} | {r['max_rhat']:.4f} "
            f"| {r['n_divergences']} |")
    lines += ["", "## Staged next wave (NOT run here)",
              "The six launch-spec §6 supplementaries (fine-bracket band, aoristic-MC, "
              "Dirichlet-multinomial + NegBin model-comparison, trapezoidal, "
              "H2.2/2.3/2.4 + empire-α, empire-EB) are deliberately staged for a "
              "supervised wave — DM/NegBin need new model builders not yet validated. "
              "The posterior-median corrected genuine SPA per unit "
              "(`corrected_genuine_spa`) is the H3b hand-off."]
    (out_dir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[run-h2] wrote {out_dir/'SUMMARY.md'} — tiers {dict(tiers)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--n-jobs", type=int, default=12)
    ap.add_argument("--only", type=str, default=None, help="comma-separated unit indices (smoke)")
    ap.add_argument("--code-dir", type=Path, default=Path(__file__).resolve().parent)
    a = ap.parse_args()

    preflight_tmpdir()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    units_data, units = build_units_data(a.out_dir)
    udir = a.out_dir / "units"
    udir.mkdir(exist_ok=True)

    sel = set(int(x) for x in a.only.split(",")) if a.only else set(u["unit_index"] for u in units)
    todo = [u["unit_index"] for u in units
            if u["unit_index"] in sel and not (udir / f"unit-{u['unit_index']:02d}.json").exists()]
    print(f"[run-h2] {len(units)} units; {len(todo)} to fit; n_jobs={a.n_jobs}")

    status = a.out_dir / "STATUS.txt"
    queue, inflight, done, failed = list(todo), {}, 0, []
    t0 = time.time()

    def spawn(idx: int) -> subprocess.Popen:
        cmd = [UV, "run", "python", str(a.code_dir / "fit-unit.py"),
               "--unit-index", str(idx), "--units-data", str(units_data),
               "--out-dir", str(udir)]
        return subprocess.Popen(cmd, cwd=str(H.PROJECT_ROOT))

    while queue or inflight:
        while queue and len(inflight) < a.n_jobs:
            idx = queue.pop(0)
            inflight[idx] = spawn(idx)
        time.sleep(2)
        for idx, p in list(inflight.items()):
            rc = p.poll()
            if rc is None:
                continue
            del inflight[idx]
            done += 1
            if rc != 0 or not (udir / f"unit-{idx:02d}.json").exists():
                failed.append(idx)
            el = time.time() - t0
            status.write_text(
                f"done={done}/{len(todo)} inflight={len(inflight)} failed={len(failed)} "
                f"elapsed={el:.0f}s\n", encoding="utf-8")

    el = time.time() - t0
    print(f"[run-h2] complete: {done} done, {len(failed)} failed, wall={el:.0f}s")
    if failed:
        print(f"[run-h2] FAILED unit indices: {sorted(failed)}")
    write_summary(a.out_dir, units)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
