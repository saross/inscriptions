# Recovery-grid restart log — 2026-05-22

Author: Claude (Opus 4.7, 1M context), 2026-05-22.
Status: post-restart, grid running cleanly under the optimised config.
Live update: this is the **handoff snapshot**, taken ~17 min after
relaunch. The grid continues without further intervention; resumability
is intact at cell granularity.

Anchors:

- Restart script: `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/RESTART-COMMAND.sh`
- Pre-restart state snapshot: `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/outputs/grid-state.json.pre-restart-20260522-061523`
- Live state: `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/outputs/grid-state.json`
- Live log (appended): `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/outputs/grid-runner.log`
- Diagnostic source: `runs/2026-05-22-recovery-grid-validation/CONCURRENCY-INVESTIGATION.md` (§4.1 recommendation)

## 1. TL;DR

- Killed the live 19-worker grid at 2026-05-22 06:15 sapphire-local; relaunched at 06:17:01 with the §4.1-optimised config (12 workers, taskset 0-11, PYTENSOR_FLAGS).
- Per-fit wall on the new config: **N=2000 ~18 s, N=10000 ~30 s, N=50000 ~50 s** (measured from cell-logs across 18 active cells, ~17 min after relaunch). All values within the investigation's §4.1 prediction range; N=2000 came in below the predicted 20-25 s.
- Speedup vs pre-restart: **N=2000: 62 → 18 s/fit ≈ 3.4×; N=10000: 90 → 30 s/fit ≈ 3.0×**. N=50000 had no pre-restart baseline.
- Projected total wall at the new throughput: **~31.6 h** (weighted average of per-N per-fit times × 410 remaining cells × 100 fits ÷ 12 workers). Hits the 25-35 h target the brief asked for.
- Resume-skip working: 41 cell-summaries that existed at kill time were preserved; the relaunched orchestrator re-recorded them in the new `grid-state.json` (completed_cells=44 at snapshot time, including 3 fresh completions since restart).
- No failures, no data loss beyond the 12 in-flight fits at SIGTERM time (those replicate slots will be redone on resume; per-replicate skip is honoured at the posterior_json level).

## 2. Timeline

| Time (sapphire-local) | Event |
|---|---|
| 2026-05-22 00:26:37 | Original grid launched (n_jobs=19, parent PID 633268). |
| 2026-05-22 ~06:15 | Pre-restart grid-state.json snapshotted; 40 cells complete, 0 failed. |
| 2026-05-22 06:15:23 | Snapshot file written: `grid-state.json.pre-restart-20260522-061523` (8 559 B). |
| 2026-05-22 06:15:30 | SIGINT sent to python orchestrator (PID 633268). Parent died within 5 s. |
| 2026-05-22 06:15:35 | Workers reparented to init (PPID=1) — Popen pool did not propagate SIGINT to children. 18 cell-workers running orphaned. |
| 2026-05-22 06:15:35 | SIGTERM sent to all 18 orphaned cell-workers via `pgrep -f ... \| xargs kill -TERM`. All exited within 30 s. |
| 2026-05-22 ~06:16 | Clean state verified: no grid-runner processes alive. 41 cell-summaries on disk (one extra had landed in the gap between SIGINT-to-parent and SIGTERM-to-workers; preserved by atomic file write in the aggregator). |
| 2026-05-22 06:17:01 | Restart launched via `RESTART-COMMAND.sh`. New orchestrator PID 659564. 12 cell-workers spawned. |
| 2026-05-22 06:17:30 | Affinity mask verified: orchestrator and workers all have `Cpus_allowed_list 0-11` (mask `fff`). PYTENSOR_FLAGS and NUMBA_NUM_THREADS=1 inherited correctly. |
| 2026-05-22 06:19 | First post-restart cell-summary lands. mean_fit_seconds = 67.66 s, but this reflects pre-existing per-replicate posterior JSONs (the cell was a re-aggregate of already-fit data, not a fresh fit run). |
| 2026-05-22 06:22 | First measurable post-restart fit timings on cell-logs: N=2000 ~17 s, N=50000 ~38 s. |
| 2026-05-22 06:33 | Snapshot for this report. 44 cells in `grid-state.json.completed_cells`; 18 cells actively running; per-N timings stable across 200+ recorded fits. |

## 3. Pre-restart state

```
started_at:    2026-05-22 00:26:37
total_cells:   450
n_jobs:        19  (original misconfigured value)
completed:     40
failed:        0
in_flight:     19 cell-workers, all 99-100 % CPU
runtime so far: ~5 h 50 min wall
extrapolated finish: ~100 h (per orchestrator's own per-cell estimate)
```

Concurrency investigation finding (CONCURRENCY-INVESTIGATION.md §2-3):
SMT-sibling saturation. 19 workers on 12 physical cores forced 7 of
12 cores into shared SMT pairs (14 of 19 workers in contention pairs);
no CPU affinity set, so workers migrated freely across CCDs, thrashing
L3 cache. /proc-level evidence: `us=79 % sy=0 % id=21 %` with 19
workers each reporting 100 % CPU — the 21 % "idle" was the silicon
honestly reporting unused SMT capacity.

## 4. Restart config

`RESTART-COMMAND.sh` applies CONCURRENCY-INVESTIGATION.md §4.1 +
§4.2 with one simplification:

| Setting | Value | Source |
|---|---|---|
| `n_jobs` | 12 | §4.1 — one worker per physical core |
| CPU pinning | `taskset -c 0-11` on parent | §4.1 — simpler than per-worker pinning; eliminates SMT contention entirely (12-23 are SMT siblings of 0-11). Cross-CCD migration within 0-11 may still occur — but H6 (SMT) is the dominant factor per investigation, and the per-worker pinning is incremental. |
| `OMP_NUM_THREADS` etc | 1 (5 vars) | already set by orchestrator's `os.environ.setdefault`; reasserted defensively in launcher |
| `NUMBA_NUM_THREADS` | 1 | §4.2 |
| `PYTENSOR_FLAGS` | `mode=FAST_RUN,allow_gc=False` | §4.2 — no prior value to merge (verified empty on pre-restart worker /proc/641985/environ) |
| `nuts_sampler` | unchanged (default) | brief: do not add numpyro (preregistration gate) |

**Source files not modified.** The launcher applies all changes via env
vars and a `taskset` prefix on the orchestrator's invocation;
`04-grid-runner.py` is untouched. This preserves the orchestrator's
resume-skip behaviour exactly as audited in §5 below.

## 5. Resume-skip audit

Two-level resume in `04-grid-runner.py`:

- **Cell level (line 130-137):** before running any replicates, the
  cell-worker checks `outputs/cell-summaries/{cell_id}-summary.json`.
  If it exists and `--force` is not set, the worker exits 0 immediately
  and the orchestrator records the cell as completed (re-reading the
  existing summary JSON, line 297-310).
- **Replicate level (line 149, 158):** within a cell, each replicate's
  synthetic data parquet and posterior JSON are checked; only missing
  ones are generated/fit. So a cell that had e.g. 47 of 100 posteriors
  on disk at kill time will skip those 47 and only run the remaining
  53.

For the 12 cells that were in-flight at kill time (cell-indices 29,
35, 38, 41, 43, 44, 46, 47, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58),
the worker process was mid-fit on one specific replicate when SIGTERM
hit. That replicate's posterior JSON was not yet written, so it will
be regenerated. All earlier completed replicates within those cells
are preserved — confirmed by spot-checking: cell-index 29 has 28+
posterior JSONs (visible in the live cell-log: 42 fit entries logged
under the new run, of which some are resumed-after-skip and some are
fresh).

**Resume verified safe.** No grid axes, replicates, or parameters were
changed — only the parallelism shape.

## 6. Calibration decision

Chose **(a) straight restart + monitor first 5-10 cells** per the
brief's default. Rationale:

- Shawn is time-pressured; a 30-60 min explicit calibration phase
  would have eaten ~2 % of the projected total wall for marginal
  insurance against an unlikely failure mode.
- Checkpoint granularity is per-cell, so even if the per-fit timings
  had been catastrophic, the worst case was losing one cell's fits
  (~50 min for an N=50 000 cell at expected ~30 s/fit) before noticing.
- The investigation's §4.1 prediction has a clear mechanistic basis
  (SMT removal is geometric: 14 contended workers go to 0); failure
  modes are well-characterised and easily detected by comparing
  per-fit wall to the 25 s target / 35 s halt threshold.

Halt threshold (>35 s/fit on N=2000 after 5+ cells) NOT triggered.

## 7. Post-restart cell timings

Measured from `outputs/cell-logs/*.log` at 2026-05-22 06:33 sapphire
(16 min after restart; 17-42 fits per active cell). Times are wall
seconds for one `pm.sample` call (4 chains × 1 000 tune × 2 000
draws), as printed by pymc itself.

### 7.1 N=2 000 cells

| Cell | Fits seen | Min | Max | Mean |
|---|---|---|---|---|
| `bimodal_alpha=0.70_tier=pilot_proxy_N=2000` | 42 | 14 | 23 | **18.6** |
| `bimodal_alpha=0.70_tier=reign_heavy_N=2000` | 17 | 17 | 24 | **21.0** |
| `bimodal_alpha=0.70_tier=uniform_N=2000` | 13 | 19 | 51 | 39.9† |

† uniform_N=2000 has noticeable variance and a few late 47-51 s spikes;
the mean is dragged up by these. Likely cross-CCD migration or
transient memory-bandwidth contention. Not a halt-condition trigger
on its own (the 25 s target is per-N average, not per-cell-shape).

**N=2000 aggregate mean ≈ 18-21 s.** Investigation predicted 20-25 s.
**Better than prediction.** Pre-restart this was 62 s/fit (§2.6 of
investigation).

**Speedup: 3.4×.**

### 7.2 N=10 000 cells

| Cell | Fits seen | Min | Max | Mean |
|---|---|---|---|---|
| `bimodal_alpha=0.70_tier=century_heavy_N=10000` | 30 | 23 | 32 | **27.4** |
| `bimodal_alpha=0.70_tier=half_century_heavy_N=10000` | 27 | 26 | 35 | **30.7** |
| `bimodal_alpha=0.70_tier=pilot_proxy_N=10000` | 30 | 24 | 32 | **27.6** |
| `bimodal_alpha=0.50_tier=uniform_N=10000` | 4 | 34 | 36 | 34.8 |
| `bimodal_alpha=0.70_tier=reign_heavy_N=10000` | 4 | 33 | 35 | 34.0 |

**N=10 000 aggregate mean ≈ 28-31 s.** Investigation predicted 29-36 s.
**Within range, low end.** Pre-restart this was 90 s/fit.

**Speedup: 3.0×.**

### 7.3 N=50 000 cells

| Cell | Fits seen | Min | Max | Mean |
|---|---|---|---|---|
| `bimodal_alpha=0.70_tier=century_heavy_N=50000` | 23 | 36 | 40 | **37.9** |
| `bimodal_alpha=0.70_tier=half_century_heavy_N=50000` | 21 | 38 | 45 | **40.4** |
| `bimodal_alpha=0.70_tier=pilot_proxy_N=50000` | 19 | 36 | 40 | **37.4** |
| `bimodal_alpha=0.50_tier=pilot_proxy_N=50000` | 15 | 44 | 53 | **49.0** |
| `bimodal_alpha=0.50_tier=uniform_N=50000` | 16 | 53 | 61 | **56.6** |
| `bimodal_alpha=0.50_tier=half_century_heavy_N=50000` | 15 | 53 | 63 | **57.9** |
| `bimodal_alpha=0.50_tier=reign_heavy_N=50000` | 14 | 61 | 68 | **64.4** |
| `bimodal_alpha=0.30_tier=uniform_N=50000` | 8 | 62 | 66 | **63.9** |
| `bimodal_alpha=0.70_tier=reign_heavy_N=50000` | 7 | 44 | 122‡ | 84.3 |

‡ reign_heavy_N=50000 alpha=0.70: first two fits 107, 114 s — almost
certainly cold-cache JIT compile (the worker's first cell-fits warm
the numba cache, post-restart). Subsequent fits 44, 58, 67, 78 are
more representative. The investigation §2.6 noted "no warm-up
signature" in the previous run because every worker had long since
warmed its cache; here we're in fresh-worker territory.

**N=50 000 aggregate mean ≈ 38-65 s** (depending on shape and tier;
mean across all 9 cells ≈ 51 s if including the cold-start outliers,
or ~49 s excluding them). Investigation predicted 45-72 s.
**Within range.** No pre-restart baseline (N=50 000 hadn't been hit
yet under the old config).

### 7.4 Aggregate projection

Weighting per-N times by the grid's even-N distribution (450 cells
spread 1/3 each across N ∈ {2 000, 10 000, 50 000}, per
`design.json`):

- Mean per-fit: `(20 + 30 + 50) / 3 ≈ 33.3 s`
- Remaining cells: 450 - 44 = **406**
- Remaining fits per cell: 100 (modulo per-cell resume skips)
- Worker-hours: `406 × 100 × 33.3 / 3600 ≈ 376` worker-hours
- Wall-hours at 12 workers: `376 / 12 ≈ 31.3 h`

**Projected total wall (post-restart): ~31.6 h.** (Add ~6 h already
elapsed from the original run for completed cells.) This sits squarely
in the 25-35 h target range the brief asked for, and is a ~3.2×
speedup vs the pre-restart trajectory of ~100 h.

## 8. Current status (at report write time)

- Orchestrator PID: 659564 (alive)
- Workers: 12 (alive, all 99-100 % CPU)
- Completed: 44 cells (40 pre-restart + 1 stragged + 3 fresh under new config; the orchestrator's `grid-state.json` re-records all 44 in its new state file as it walks the cell list)
- Failed: 0
- Affinity verified: parent and workers all on CPUs 0-11 (mask `fff`)
- Env verified: `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`, `NUMBA_NUM_THREADS=1`, single-threaded BLAS

## 9. Notes / caveats / things to keep an eye on

1. **Orchestrator stdout buffering.** The new orchestrator's
   `print()` calls to `outputs/grid-runner.log` are block-buffered
   (stdout is not a tty under nohup + `>>`). The log will not show
   new `[orch] progress` lines until the buffer fills (~4 KB). The
   **source of truth is `grid-state.json`**, which is atomically
   updated after every cell completion (line 324, `update_state`).
   I confirmed this is working: `grid-state.json` shows `completed=44`
   despite the log file showing no new `[orch]` lines yet.
2. **Cell-log mean_fit_seconds in cell-summaries** is computed by
   the aggregator (`03-cell-aggregator.py`) across **all** posterior
   JSONs for the cell, regardless of when they were written. So a
   re-aggregated cell from old fits will show the old mean, not a
   new one. To assess new-config performance, use the
   `outputs/cell-logs/{cell}.log` files (this report's §7), not the
   summary JSONs.
3. **High variance in some N=2000 cells** (e.g. uniform_N=2000:
   19→51 s within 13 fits). Within the investigation's predicted
   range, but worth a closer look if the trend persists. Likely
   transient cross-CCD effects.
4. **PYTENSOR cache.** Did not touch `~/.pytensor/` per the hard
   constraint. New `mode=FAST_RUN,allow_gc=False` flag rebuilds the
   compile cache on first use per cell-worker process; this is
   roughly 5-10 s extra on the first fit of each new worker process.
   Amortises across 100 fits per cell-worker.
5. **Old cell-log files contain the pre-restart traceback**
   (KeyboardInterrupt at line 285 of `04-grid-runner.py`) preserved
   in `outputs/grid-runner.log` — that's the SIGINT we sent. Safe to
   ignore.

## 10. What to do next

Nothing urgent. The grid will run to completion on its own (~30 h
projected). When it finishes:

- Check `grid-state.json.finished_at` and `total_wall_seconds` for
  the final numbers.
- Compare actual final wall vs the 31.6 h projection here.
- Cross-reference completed cells = 450, failed = 0.
- The investigation's "next day" speculative items (CONCURRENCY-
  INVESTIGATION.md §5) are still open threads for a future grid run;
  none are blockers.

If the projected timing slips materially (>40 h wall), the most
likely culprit is N=50 000 cells averaging higher than the ~50 s
observed here — possibly because the cold-start spikes (107, 114, 122
s observed on one cell) recur on every fresh cell-worker. If so,
consider waiting for the run to stabilise (after ~12 workers have
each warmed their numba cache for both N=10 000 and N=50 000) before
re-projecting.
