# Joint recovery-grid — memory incident, fixes, and overnight run status

**Date:** 2026-06-10 (overnight, autonomous session). **Author:** Claude Code (Opus 4.8).
**Status at writing:** full grid resumed and running on sapphire under a memory cap.
UK/Aus English.

## TL;DR

The first full-grid run (PID 1899820, launched 2026-06-09 ~17:21) **OOM'd and aborted at
10/300 cells**. Two independent resource exhaustions were diagnosed and fixed; the grid
runner was given a **permanent, audited memory fix**; a measured pilot sized the safe
worker count; and the grid was **relaunched at `--n-jobs 6` under a 50 GB cgroup cap**
(~26 h ETA, resumable). One deeper limitation — a per-fit memory leak in the PyMC/PyTensor
stack — is **bounded but not eliminated**; the proper fix needs a validated-model change
and is left for a do-with-Shawn step (§5).

## 1. What went wrong (two root causes)

1. **RAM OOM (the abort).** The pool used long-lived *fork* workers that rebuilt a PyMC
   model per cell and never released PyTensor allocations to the OS, plus the launch flag
   `PYTENSOR_FLAGS=...,allow_gc=False` (memory-for-speed). RSS climbed past **60+ GB** over
   ~5 h until the kernel OOM-killer reaped a worker → `BrokenProcessPool` → self-abort at
   10/300 cells (`grid-STATUS.txt`: `ABORTED: BrokenProcessPool`; real throughput had
   collapsed to 2 cells/h under swap thrash — the 12 h ETA was never reached). The OOM
   cascade made sshd and the open-webui daemon unresponsive (TCP accepted, no application
   response) — the symptom Shawn saw at the console (`Out of memory: Killed process`).

2. **`/tmp` inode exhaustion (a pre-existing, separate problem).** `/tmp` is a 31 GB tmpfs
   capped at **1,048,576 inodes**, and it was at **100 % inodes** (0 free) — ~1.05 M files
   named `tmp<random>` (mode 0600, ~300 B–14 KB, dated **June 4–7**), leaked by earlier
   h3a/sweep/scoring work via Python `tempfile` with no cleanup. With no free inodes,
   `mkdtemp()` failed `ENOSPC` even though only 4.4 GB of blocks were used — which
   intermittently broke SSH session-setup (the `255` / "no banner" failures) and would have
   broken the grid's own PyTensor temp writes. **This was the carry-forward's "762 stale
   files / optional cleanup" item — it was not optional.**

## 2. What was done (in order)

1. Killed the grid; **57 GB RAM freed** (confirmed it was the memory hog).
2. Cleared the ~1.05 M stale `/tmp/tmp*` files (`-mmin +60` guard) → `/tmp` inodes
   **100 % → 1 %**; SSH and agent-forwarding immediately reliable again.
3. Cleared ~18 orphaned `map-reader-llm` multiprocessing workers (confirmed orphans by
   Shawn — that project now runs only on zbook; sapphire is 100 % inscriptions).
4. **Permanent memory fix** to `code/run_joint_grid.py` (committed `e4298e5`, `/audit`-clean):
   - **spawn** start method + **`max_tasks_per_child` (default 1)** new CLI arg → each
     worker is recycled after every cell, returning its memory to the OS (the *across-cell*
     bound). spawn re-imports module-level state cleanly; seeds are explicit so results are
     bit-identical to the fork version.
   - **`gc.collect()` after every replicate** (the *within-cell* Python-level bound).
   - **dropped `allow_gc=False`**; documented that **`TMPDIR` must point at a root-fs dir**
     (root fs has 46 M free inodes), not the inode-limited `/tmp` tmpfs.
5. Reconciled sapphire git (`047cc13 → e4298e5`, clean fast-forward; 10 done cells preserved
   and now gitignored).
6. **Measured pilot** (stride-50 slice, 8 reps, 3 workers) — functional PASS: spawn workers
   sample and recycle correctly, `/tmp` stable, all cells `n_ok=8`. Surfaced the per-fit
   leak (§3).
7. **Definitive worst-cell measurement** (§3) → sized `--n-jobs 6`.
8. **Relaunched** the full grid (resume) under a cgroup cap (§4).

## 3. The remaining limitation — a per-fit leak (measured, bounded)

A focused measurement of the **worst cell** (`conc_a0.2_gauss_inwin_N15000`, confounded,
N=15000, 100 reps = 200 fits, `n_jobs=1`) recorded a worker-RSS trajectory that climbs
**linearly, ~32 MB/fit, with no plateau**, to a **peak of 6.7 GB** (then released on
recycle). `gc.collect()` does not touch it, so the retained memory is **C-level**, almost
certainly PyTensor caching a freshly-compiled logp/dlogp function each replicate because
the changing `y`/`k` data is baked into the model graph as constants (a new graph hash →
a new compiled module → ~32 MB retained per fit).

- `max_tasks_per_child=1` **bounds** this: each cell fully releases on worker recycle
  (confirmed — end-of-trace RSS dropped from 6.7 GB to 5.8 GB as the worker exited).
- It is **not a correctness risk** (results are unaffected) and **cannot cause an OOM**
  with the cap in place — it is purely an **efficiency** limit (it forces a low worker count,
  hence a long wall-clock).

## 4. Current run configuration

- **Command:** `setsid bash ~/run_full_grid.sh 6 50G` on sapphire (detached).
- **Worker count:** `--n-jobs 6` → worst-case `6 × 6.7 GB ≈ 40 GB`, comfortably under the cap.
- **Safety net:** the grid runs inside a `systemd --user --scope -p MemoryMax=50G -p
  MemorySwapMax=0`. If memory is ever mis-sized, the **cgroup** OOM-killer reaps a grid
  worker (→ clean `BrokenProcessPool` abort, resumable) instead of the **system** OOM-killer
  wedging the whole box. Verified engaged in the log: `MEMORY-CAP: running under systemd
  --user scope MemoryMax=50G MemorySwapMax=0`.
- **Env:** `TMPDIR=$HOME/tmp_grid_scratch` (root fs), `PYTENSOR_FLAGS=mode=FAST_RUN,
  base_compiledir=$HOME/.pytensor_grid`, `taskset -c 0-11`, `--max-tasks-per-child 1`.
- **ETA:** ~162 CPU-h of fits ÷ 6 ≈ **~26 h**. Resumable at cell granularity; the 11
  already-completed cells (incl. the worst cell measured above) are skipped.
- **Diagnostic trace:** `outputs/full-grid-memwatch.log` (memAvail / top-RSS / pyProcs /
  tmpInodes / cellsDone every 60 s).

## 5. Proper fix — DONE (2026-06-10, with Shawn): build-once + set_data

The per-fit leak was eliminated at source (commit `fad6fd5`, `/audit`-clean): `y` and
`k_aligned` are now mutable `pm.Data` ("y_data"/"k_data") in `build_model_joint`, and
`run_cell` builds each cell's joint model **once** then swaps each replicate's data via
`fit_joint_on_model` + `pm.set_data`. The graph is constant across reps, so PyTensor reuses
the cached compiled logp instead of recompiling — confirmed by gate 2: the worst cell's RSS
now climbs to **~2 GB** (extrapolated, 100 reps) vs **6.7 GB** before, and per-fit time is
uniform (no recompile). **Scope: joint model only** (`joint_lib.py`, zero external
dependents); the shared `build_model_f1_f3` (imported by H2.1 + 5 other runs) was left
untouched, so it still rebuilds per rep on the 90 confounded cells — that residual is the
~16 MB/rep climb in the worst-cell trace and is harmless at n_jobs=12.

**Revalidation (gate 1, `validate_setdata.py` + `determinism_test.py`):** the new code is
bit-**reproducible** (new-vs-new = 0.000) but **not bit-identical** to the old
build-fresh-per-rep path (old-vs-new max |Δα| ≈ 2×10⁻³ identifiable / 7×10⁻³ confounded,
convergence flags all match). The delta is a method-specific NUTS-trajectory difference
(shared-variable graph vs constant-baked graph — the *same* posterior, a different but
equally valid seeded path), ~25–100× below the bias thresholds and within per-cell MC error.

**Decision (Shawn, 2026-06-10): RESTART** rather than mix methods. The 116 partial
old-method cells were discarded and the full **300-cell** grid relaunched from scratch with
the new code at **n_jobs=12** under the 50 GB cgroup cap (~13–14 h), so the entire grid is
one consistent, bit-reproducible method. Result config supersedes §4's n_jobs=6.

## 6. Follow-ups for Shawn

- The `/tmp` `tempfile` leak is a **standing issue in the PyMC/R workflow on sapphire** — it
  has been silently filling `/tmp` since at least June 4. Worth finding the offending script
  (the named files in `/tmp` — `h3a_*.py`, `gs_perm.sh`, `k3_scoring.sh`, `run_sweep.sh` —
  point at the sweep/scoring/h3a-shadow work) and adding `delete=True` / `TMPDIR` hygiene.
- On completion: `uv run python code/aggregate_joint_grid.py` → `grid-VERDICT.md` +
  `grid-summary.json`, scored against `full-grid-spec.md §3` (C1/C2/C4 + bias surface). Only
  those two artefacts are committed (per the carry-forward).
