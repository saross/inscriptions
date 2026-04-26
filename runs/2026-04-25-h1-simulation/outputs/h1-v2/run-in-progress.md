# H1 v2 final-precision run — IN PROGRESS

**Started:** 2026-04-26 05:00 UTC (sapphire)
**Status as of handoff:** 14 min elapsed, 0 of 256 cells completed,
24 of 24 workers at 99-100% CPU, no errors in run.log.
**Estimated completion:** unclear — original forecast was 7–11 h
based on smoke timings, but the first cell milestone has not landed
yet and per-cell wall-time at full precision (n_mc=1000) appears
longer than the linear extrapolation predicted. Realistic upper
bound: 15–20 h.

The 24 workers were each assigned a cell from the queue head, which
holds 16 empire cells (the slowest, ~5–6 h each at full precision)
plus 8 province cells at small n. Until one of the empire cells
completes, joblib does not promote later (smaller, faster) cells
into the live worker pool — so we see no progress reports for the
first several hours.

## Status as of agent handoff

The H1 v2 final rerun is executing on sapphire at full preregistered
precision (n_iter = 1000, n_mc = 1000, no wall-time cap) per Decisions
8, 9, and 10 (2026-04-26). The optimised forward-fit CPL code (commit
`226c6dd`, ~5× speedup) is in use; k=2 is dropped from the cell grid
(commit `b2e24b7`). Total cells: 256 = 16 empire + 128 province + 112
urban-area, with 128 exponential and 128 CPL (k=3 + k=4 fits per CPL
iteration).

## Monitoring

```bash
ssh sapphire "ps -p $(cat ~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/run.pid) -o pid,etime,pcpu --no-header"
ssh sapphire "tail -5 ~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/run.log"
```

PID file at `runs/2026-04-25-h1-simulation/outputs/h1-v2/run.pid`
(the joblib parent; loky workers are children).

joblib reports milestones at 5 %, 10 %, 25 %, 50 %, 75 %, 100 %
of cells completed — these will appear in `run.log` as
``[Parallel(n_jobs=-1)]: Done X out of 256 | elapsed: Yh remaining: Zh``.

The first milestone is expected ~30 min in (the slowest empire cells
take ~5–6 h each at full precision; the smallest urban cells take
~5 min each; with 24 cores running cells in parallel, fast cells
clear early and progress reports start once the cumulative count hits
5 % = 13 cells).

## When the run completes (PID dies)

Confirm the parquet exists and is the expected size (~ 50–80 MB):

```bash
ssh sapphire "du -h ~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/cell-results.parquet"
```

Then run report generation on sapphire:

```bash
ssh sapphire "cd ~/Code/inscriptions && .venv/bin/python3 runs/2026-04-25-h1-simulation/code/post_run_v2.py --in runs/2026-04-25-h1-simulation/outputs/h1-v2 --out runs/2026-04-25-h1-simulation/outputs/h1-v2 2>&1 | tail -30"
```

Rename REPORT to flag final status:

```bash
ssh sapphire "cd ~/Code/inscriptions && mv runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2.md runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md"
```

rsync back (excluding the raw parquet, likely > 50 MB):

```bash
rsync -avz --exclude='cell-results.parquet' sapphire:~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/ ~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/
```

Verify locally `< 100 MB`:

```bash
du -sh ~/Code/inscriptions/runs/2026-04-25-h1-simulation/outputs/h1-v2/
```

Commit + push:

```bash
git add runs/2026-04-25-h1-simulation/outputs/h1-v2/
git rm runs/2026-04-25-h1-simulation/outputs/h1-v2/run-in-progress.md
git commit -m "feat(runs/h1): H1 v2 FINAL — full preregistered precision (1000/1000)" -m "<wall-time>; 256 cells; <FP-rate range>; binding 50%/50y thresholds for province exp/cpl-k=3 + urban-area exp/cpl-k=3; unreachable cells listed. Headline thresholds in REPORT-v2-final.md."
git push origin main
```

Then write the Stage 5 reback report covering optimisation summary, FP
rates, binding thresholds, unreachable map, and CPL k-sensitivity.

## If something goes wrong

- **PID dies before completion (no parquet at expected path):** investigate the
  tail of `run.log` for traceback. Likely culprits: numerical edge case in
  CPL fit, OOM (unlikely; 60 GB available), file-system issue. Check
  worker logs in `/tmp/joblib_*` if present.
- **Run hung (PID alive but no progress for > 2 h):** this would be
  unusual — the longest single cell should be < 6 h. Check worker CPU
  usage (`top` on sapphire); if all 24 are idle, something has stalled.
- **Disk full:** unlikely (parquet is ~ 50 MB); but check
  `df -h ~/Code/inscriptions` if writes start failing.

## Handoff context

Stages 0, 1, 2 complete (commits `b6f0cf6` … `3d7cb89`):

- `b6f0cf6` chore(runs/h1): rename h1-v2 to h1-v2-preliminary; tag report
- `8313466` deps: add numba 0.65 for CPL forward-fit JIT acceleration
- `226c6dd` perf(runs/h1): optimise forward-fit CPL — 4.8x (k=3) / 5.4x (k=4) speedup
- `e20bc13` test(runs/h1): re-validate optimised CPL forward-fit on Stage 3 grid
- `b2e24b7` feat(runs/h1): h1_sim_v2 — drop CPL k=2; no wall cap; references Decisions 8-10
- `5acd08e` test(runs/h1): smoke-test parquet from k=2-drop verification
- `3d7cb89` fix(runs/h1): post_run_v2 k-sensitivity table — drop k=2 references

Production run `b2e24b7` (parent PID 3223027) launched 05:00 UTC on
sapphire; full output goes to `runs/2026-04-25-h1-simulation/outputs/h1-v2/`.
