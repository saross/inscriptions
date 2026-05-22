# Concurrency investigation — recovery-grid run 2026-05-22

Author: Claude (Opus 4.7, 1M context), 2026-05-22.
Status: diagnostic only. The live grid is untouched. This report
informs the **next** grid run; the current run will complete in
~100 h either way.

Anchors:

- Live grid host: sapphire (AMD Ryzen 9 7900, 12C/24T, 60 GB).
- Live PIDs: parent bash 633264, python orchestrator 633268, 19
  cell-workers (children of 633268).
- Smoke-test source: `runs/2026-05-22-recovery-grid-validation/SMOKE-TEST.md`
- Orchestrator source: `runs/.../code/04-grid-runner.py`
- Fit module: `runs/.../code/02-cell-mixture-fit.py`
- Live state (read-only): `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/outputs/grid-state.json`
- Diagnostic sandbox (mine): `~/cc-scratch/sapphire-concurrency-debug/`

## 1. TL;DR

- **Root cause is mechanical, not orchestrator-coordination.** The
  19 cell-workers are pure CPU-bound numerical compute (verified
  ~99 % `se.sum_exec_runtime / wall` per worker; zero I/O during
  sampling; wchan=0 across all 19). The throughput loss is happening
  *inside the silicon*: 19 workers on a 12-core CPU forces 7 of 12
  physical cores into SMT-sibling collision (each pair sharing one
  core's execution units), and the kernel migrates workers across
  CCD boundaries because no CPU affinity is set.
- **The smoke-test orchestrator-attribution was wrong.** Subprocess
  startup is not the dominant cost — each subprocess in this design
  runs **100 fits per cell-worker**, not 1, so the 3-5 s python
  startup amortises to 30-50 ms per fit. The "subprocess-pool is
  slower than bash-parallel" claim in `SMOKE-TEST.md:86-101` does
  not reproduce on the actual orchestrator architecture; the gap is
  the SMT-saturation + N-effect (next bullet), not the pool design.
- **N is not free.** The smoke-test predicted per-fit time would be
  ~constant across N ∈ {2 000, 10 000, 50 000} (SMOKE-TEST.md:60-61).
  Empirically, completed N=2 000 cells averaged **62 s/fit**;
  N=10 000 cells averaged **90 s/fit** — a 44 % cost increase. This
  is not a bug, just a wrong prediction. N=50 000 cells will
  almost certainly be slower again.
- **Recommended fix for the next run: n_jobs ≤ 12, with explicit
  CPU pinning (one worker per physical core, no SMT siblings).**
  Expected per-fit wall: roughly 22-30 s (recovering ~2× of the
  current ~70 s under steady-state contention; cannot recover the
  full standalone 14-18 s while still running 12 parallel
  workers because of cross-CCD L3 pressure). Total grid wall:
  ~12-18 h. See §4 for the concrete config and a strict-isolation
  fallback.

## 2. Live-process characterisation

### 2.1 Worker count, threads, affinity

`ps --ppid 633268`: **19 cell-worker children**, matching the
`--n-jobs 19` invocation on the orchestrator command line
(grid-state.json: `"n_jobs": 19`).

Per worker:

| Field | Value |
|---|---|
| `NLWP` (threads) | 4 |
| Active threads (CPU > 50 %) | 1 |
| Other 3 threads | jemalloc_bg_thd + 2 sleeping python helpers (state=Sl, 0.0 % CPU) |
| `Cpus_allowed_list` | `0-23` (no affinity set) |
| `taskset` mask | `ffffff` (all 24 SMT threads) |

Environment (`/proc/633272/environ`, representative):

```
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
```

Single-threaded BLAS is correctly propagated. The 4 threads per
worker are **not** BLAS oversubscription; they're python/numba/jemalloc
housekeeping threads. Smoke-test ruled this out correctly.

### 2.2 SMT-sibling collisions

Sapphire's topology (`/sys/devices/system/cpu/cpu*/cache/index3/shared_cpu_list`):

- CCD0 = physical cores 0-5; L3 shared by logical CPUs {0-5, 12-17}
- CCD1 = physical cores 8-13; L3 shared by logical CPUs {6-11, 18-23}
- SMT sibling map: (n, n+12) for n ∈ {0-11}

10 consecutive snapshots (1 s apart) of where the 19 active worker
threads are running (logical CPUs):

```
active=19 solo=5 shared_pairs=7
active=19 solo=5 shared_pairs=7
... (identical for all 10 snapshots)
```

**Steady-state: 7 of 12 physical cores host 2 workers via SMT;
5 cores host 1.** 14 of 19 workers are in SMT-contended pairs.
Compute-heavy numerical workloads (NUTS gradient + Cholesky +
log-softmax) typically lose 20-40 % per-thread throughput under
SMT, because both siblings contend for the same FPU/ALU/L1/L2.

### 2.3 Cross-CCD worker migration

Five PSR snapshots, 2 s apart, of the 19 active threads:

```
snap 1: 1 2 3 5 6 7 8 9 11 12 13 14 15 16 17 19 20 22 23
snap 2: 0 1 2 3 5 6 7 8 9 10 11 13 14 15 16 17 19 20 23
snap 3: 0 1 2 3 5 6 7 8 9 13 14 15 16 17 19 20 21 22 23
snap 4: 0 1 2 3 4 5 6 8 9 10 14 15 16 17 19 20 21 22 23
snap 5: 0 2 3 4 5 6 8 9 10 13 14 15 16 17 19 20 21 22 23
```

Workers migrate freely between CPUs every few seconds; ~3-4 of the
19 change CPU per 2-second window. Each migration that crosses CCDs
(0-5,12-17 ↔ 6-11,18-23) invalidates L1/L2 *and* moves the working
set to a different L3 (32 MiB per CCD). The kernel is doing this
because no affinity is set; the load balancer is trying to spread
the 19 runnable tasks across the 24 SMT threads but cannot win
because 19 > 12 physical cores.

### 2.4 Scheduler / runtime accounting

`/proc/633272/sched` for the oldest worker (started 02:44:43 ago):

```
se.sum_exec_runtime  : 10113240.452578  ms  (10 113 s of CPU time)
nr_switches          : 16789
nr_voluntary_switches: 295
nr_involuntary_switches: 16494
```

Wall elapsed: 9 883 s. CPU efficiency = 10 113 / 9 883 ≈ **102 %**
(the > 100 % reflects sched-accounting granularity; effectively the
worker is at 100 %).

Across all 19 workers, every one shows the same picture: ~100 %
CPU efficiency relative to its wall elapsed time. `nr_voluntary_switches`
in the hundreds (worker rarely sleeps voluntarily) vs `nr_involuntary`
in the thousands (kernel preempted it ~1.7 times/s) tells us the
worker **is not blocking on I/O, locks, or syscalls** — it is
genuinely compute-saturated.

`vmstat 1` snapshot during the run:

```
procs ----memory---- ---swap-- ---io---- -system-- -------cpu-------
 r  b   swpd   free  ...si so bi bo  in   cs  us sy id wa st gu
19  0      0  ...    0  0  0  0  21k 250  79  0 21  0  0  0
```

- `r` (runnable) = 19 — matches worker count.
- `cs` (context-switches/s) = ~250 — very low.
- `bi/bo` (block in/out) = 0 — no disk I/O.
- `us=79 % sy=0 % id=21 %` — and here's the smoking gun. With 19
  workers each reporting "99 % CPU" the system is still **21 %
  idle**. That gap is the SMT thread that "owns" the second
  logical thread of a contended core sitting unused while the
  hardware schedules the other sibling. The /proc CPU accounting
  charges 100 % to whichever thread is making progress; the system
  view sees the SMT under-utilisation honestly.

### 2.5 Per-worker I/O during sampling

Per-second I/O delta over a 10 s window for PID 633272:

```
rchar delta: 0 bytes in 10s = 0 B/s
wchar delta: 0 bytes in 10s = 0 B/s
```

Zero file traffic during `pm.sample`. Numba's JIT cache (`~/.pytensor/numba/`,
4 653 files, 265 touched in the last 10 min) is hit on **first fit**
in a cell-worker (cold-cache compile) and then unused for fits 2-100
because pymc caches the compiled-model object in-process. The
"compile-cache lock contention" hypothesis is **ruled out**: every
worker is wchan=0 and zero-I/O during sampling.

### 2.6 Per-cell and per-replicate timing trends

13 completed cells from `grid-state.json` (in completion order):

| Cell | mean_fit_s |
|---|---|
| bimodal_alpha=0.30_tier=century_heavy_N=2000 | 54.3 |
| bimodal_alpha=0.30_tier=half_century_heavy_N=2000 | 55.8 |
| bimodal_alpha=0.05_tier=reign_heavy_N=2000 | 57.8 |
| bimodal_alpha=0.05_tier=half_century_heavy_N=2000 | 65.5 |
| bimodal_alpha=0.05_tier=pilot_proxy_N=2000 | 66.0 |
| bimodal_alpha=0.05_tier=century_heavy_N=2000 | 68.2 |
| bimodal_alpha=0.05_tier=uniform_N=2000 | 68.6 |
| bimodal_alpha=0.30_tier=century_heavy_N=10000 | 76.3 |
| bimodal_alpha=0.05_tier=pilot_proxy_N=10000 | 87.3 |
| bimodal_alpha=0.05_tier=half_century_heavy_N=10000 | 91.9 |
| bimodal_alpha=0.05_tier=uniform_N=10000 | 93.7 |
| bimodal_alpha=0.05_tier=century_heavy_N=10000 | 94.3 |
| bimodal_alpha=0.05_tier=reign_heavy_N=10000 | 96.1 |

Grouped by N:

- N=2 000: 7 cells, mean **62.3 s/fit**
- N=10 000: 6 cells, mean **89.9 s/fit**

**N matters.** The smoke-test prediction in SMOKE-TEST.md:60-61
("per-fit time should be approximately constant across N ∈ {2 000,
10 000, 50 000}") is empirically wrong by ~44 % between the two N
values observed so far. (Inference: the multinomial loglik computes
a sum over the data; while the *graph shape* is constant in N, the
*loop trip count* in the compiled numba code is not. Larger y means
more elementwise work in the loglik and in `softmax(log_p_gen_raw)`-
to-`p_t` accumulation.)

Per-fit timing **within** a single cell (e.g. `bimodal_alpha=0.05_
tier=century_heavy_N=10000`, mean 94.3 s, n=100): min 46.7 s,
max 136.9 s. First three fits 92.3, 59.4, 122.6 — i.e. there is **no
warm-up signature** (fit 1 ≠ slow then fits 2-100 fast). This rules
out "first-fit JIT compile dominates the cell". Variance is contention
noise across the SMT/CCD chaos.

### 2.7 Standalone-during-contention benchmark

I ran a single `fit_replicate` in my sandbox, pinned to a single CPU,
while the 19-worker live grid was running:

```
taskset -c 11 python bench-single-fit.py ... shape=bimodal_alpha=0.30_tier=uniform_N=2000 rep=0
  → import_s=1.59  fit_s=71.42

taskset -c 18 python bench-single-fit.py ... rep=1
  → import_s=1.53  fit_s=74.15
```

A single isolated fit, pinned to one logical CPU, takes **71-74 s**
while contending with the live 19-worker grid for the box's compute
capacity. That matches the per-fit times the live workers see
(50-100 s range). Standalone-on-quiet-box was 14-18 s in
SMOKE-TEST.md:39. **The 4-5× ratio between standalone and
"standalone under live-grid contention" is the same 4-5× ratio
between standalone and the live workers' per-fit time. There is no
hidden per-worker overhead from the subprocess-pool orchestrator.**

## 3. Hypothesis-by-hypothesis findings

| # | Hypothesis | Verdict | Evidence |
|---|---|---|---|
| H1 | BLAS oversubscription | **Ruled out** | `/proc/PID/environ`: OMP/OPENBLAS/MKL_NUM_THREADS=1 on every worker (§2.1). |
| H2 | joblib/loky coordination cost | **Ruled out for the live run** (loky is not in use; the orchestrator is the subprocess pool in `04-grid-runner.py`). Possibly relevant to the SMOKE-TEST.md joblib benchmark but does not explain the live grid. |
| H3 | Per-cell python startup overhead | **Ruled out as a dominant factor.** Each cell-worker runs 100 fits per python invocation (see `04-grid-runner.py:128-180`), so the 3-5 s import cost amortises to ~30-50 ms/fit (< 0.1 %). Confirmed via the bench: import_s ≈ 1.5 s vs fit_s ≈ 70 s = 2 % of one fit, < 0.05 % of a 100-fit cell. The smoke-test write-up's attribution at lines 99-101 was wrong about the orchestrator. |
| H4 | pytensor compile-cache lock contention | **Ruled out** during sampling. Workers show wchan=0, zero file I/O during `pm.sample`. The numba cache is populated once per worker process (first fit) and then unused for fits 2-100. The 1 477 cache-file touches in the last hour are spread across 19 workers each warming their cache *once at startup*, not contending. |
| H5 | NUMA / CCD locality on the 12C 7900 | **Supported.** numactl shows 1 NUMA node (so this isn't classical NUMA), but the box has **2 L3 domains** (32 MiB each, one per CCD). With no CPU affinity set, workers migrate across CCDs every few seconds (§2.3), invalidating L3 each time. This is a real-but-secondary contributor. |
| H6 | SMT-sibling competition for execution units | **Strongly supported.** 7 of 12 physical cores host 2 workers via SMT (§2.2); steady-state across 10 consecutive snapshots. 14 of 19 workers (74 %) are in SMT-contended pairs. The system-level idle figure (`us=79 % id=21 %`) is the SMT-throttling signature: workers report 100 % CPU each via /proc but the system honestly sees 21 % of the silicon's throughput unused. Estimated direct impact: ~1.3-1.5× slowdown for the 14 contended workers; combined with the L3-thrash of H5, accounts for most of the gap to standalone. |
| H7 | Per-process subprocess startup compounding | **Ruled out** (see H3). |
| H8 | Memory bandwidth saturation | **Plausible secondary; not directly measured.** Cannot run `perf stat` (perf_event_paranoid=4 blocks unprivileged access). RAM is ample (free=12 GB, 18 GB cache, no swap). Bandwidth would matter for the 19-worker case because each worker has a working set in the tens-of-MB range (Ryzen 7900 DDR5 dual-channel ≈ 80 GB/s nominal); 19 × ~few GB/s per worker is on the order of the available bandwidth. Cannot quantify without perf access. |
| H9 | Page-cache thrashing / anon-page reclaim | **Ruled out.** free=12 GB, buff/cache=18 GB, swap used = 0. No memory pressure. |
| H10 | File-descriptor / inotify limits | **Ruled out.** No file activity during sampling (§2.5). |
| H11 (new) | N affects per-fit cost (despite smoke-test prediction) | **Supported.** N=10 000 mean = 90 s vs N=2 000 mean = 62 s (§2.6). 44 % cost increase. Mechanism: the multinomial loglik and the softmax→p_t accumulation iterate over the data inside numba; the *graph shape* is constant in N but the *loop count* is not. The smoke test only ran N=2 000, so this was never observable from a single-N benchmark. |
| H12 (new) | n_jobs above physical-core count | **Strongly supported as the proximate cause.** Running 19 parallel CPU-bound jobs on 12 physical cores guarantees 7 cores are SMT-contended in steady state (§2.2). The bash-parallel smoke-test result that "20 procs at 26 s/fit" was best-throughput is consistent with this: at 20 jobs ÷ 12 cores ≈ 1.67 jobs/core, every core is in SMT contention; at 19 jobs, only 7 of 12 are. **The throughput-optimum is somewhere near n_jobs = 12-14, not 19-20.** |

### 3.1 Where SMOKE-TEST.md got it wrong (constructive)

The smoke-test's benchmark of "20 bash-parallel = 26 s/fit avg"
(SMOKE-TEST.md:82) and "joblib n_jobs=20 = 50-115 s/fit" (line 85)
likely measured **different things**:

- The bash-parallel benchmark spawned 20 *independent shells*, each
  running one fit and then exiting. The total time per fit reflects
  the *aggregate* throughput divided by the spawn count, but the
  20 processes did not all run for the same wall span — they
  finished in 17-32 s each (SMOKE-TEST.md:82). With 24 SMT threads,
  the first 12-14 fits to start grabbed mostly-solo cores; the last
  6-8 contended. That's a *transient* benchmark, not a steady-state
  one.
- The joblib benchmark also spawned 20 workers but kept them alive
  for repeated work, so steady-state contention applied throughout.
- The current 100-fits-per-worker design lives in the steady-state
  regime — the same regime as the live run — which is why per-fit
  times look like the joblib numbers (50-100 s), not the
  bash-parallel ones (17-32 s).

In other words: **the "bash-parallel wins" observation was a
benchmark artefact** of the bash test running short-lived processes
that didn't all coexist for the full 26 s. There is no orchestrator
choice that recovers ~17-26 s/fit at n_jobs=19+. The headline gap is
n_jobs-vs-physical-cores, not orchestrator design.

## 4. Recommended remediation for the NEXT grid run

All recommendations are *operational* (orchestrator, env vars,
parallelism shape) and do not alter the preregistered model,
priors, NUTS settings, or replicate count. They affect *how* the
grid runs, not *what* it computes.

### 4.1 Primary recommendation — pinned 12-worker pool

**Config:**

- `n_jobs = 12` (one worker per physical core; no SMT contention)
- **Explicit CPU pinning**: each worker pinned via `taskset -c <cpu>`
  to one logical CPU per physical core. Suggested mapping:
  - Workers 0-5 → CPUs 0, 1, 2, 3, 4, 5 (CCD0, first SMT thread)
  - Workers 6-11 → CPUs 6, 7, 8, 9, 10, 11 (CCD1, first SMT thread)
  - SMT siblings (12-23) remain free for kernel + I/O + the
    orchestrator process itself
- Keep `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`
  (unchanged from current run).
- Keep the existing subprocess-pool orchestrator (`04-grid-runner.py`);
  add a `taskset` prefix when launching each cell-worker. Diff is
  ~5 lines: in `launch_one`, prepend `["taskset", "-c", str(cpu_id)]`
  to `cmd` and track a CPU pool to assign from on each launch.

**Expected throughput:**

- Per-fit wall under this config:
  - N=2 000 cells: smoke-test standalone was 14-18 s; with 12 fully-pinned
    workers on 12 physical cores, *some* cross-CCD L3 traffic remains
    but no SMT contention. Expect ~20-25 s/fit. (Cannot quote 14-18 s
    because each of the 12 workers still pays cache-pressure cost
    for the other 11.)
  - N=10 000 cells: scale by the observed 1.44× N-factor → ~29-36 s/fit.
  - N=50 000 cells: not benchmarked yet; expect 1.5-2× the N=10 000 cost.
- Total grid wall: 450 cells × 100 replicates / 12 workers ≈ 3 750
  worker-fits per worker × ~25-35 s avg ≈ **26-36 worker-hours** =
  **2.2-3.0 h wall** in the optimistic case if all cells were N=2 000.
- More realistically, weighted by the grid's N distribution (1/3 each
  at 2 000, 10 000, 50 000 per `design.json`), expect roughly:
  `(20 + 30 + 45) / 3 = 31.7 s/fit` average →
  `450 × 100 × 31.7 / 12 ≈ 99 000 s ≈ 27 h`.
- **Realistic estimate: 25-35 h wall.** That's a ~3× speedup vs the
  current ~100 h trajectory.

**Why not n_jobs = 24 with strict pinning?** Because the workload is
compute-bound on the FPU and SMT siblings share the FPU. 24 workers
will always contend on FPU at 1.3-1.5× per-worker slowdown vs 12.
24 × (1 / 1.4) ≈ 17 effective workers — strictly worse than 12
clean workers + 5 unused thread slots.

**Why not n_jobs = 16 or 20?** Same logic: any n_jobs > 12 starts
forcing SMT pairs. The function "throughput vs n_jobs" has a knee at
n_jobs = 12 and is approximately flat or decreasing beyond.

### 4.2 Secondary recommendation — pytensor / numba flags

These do not change correctness, only build/run hints:

- `PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"` — disables
  pytensor's intermediate-tensor garbage collection during sampling.
  Saves a few % per fit at the cost of slightly higher peak memory
  (well within the 60 GB budget).
- `NUMBA_NUM_THREADS=1` — explicit cap; should match BLAS env
  already set, but ensures numba's parallel transforms don't kick in
  inside a worker.
- `NUMBA_CACHE_DIR=$HOME/.pytensor/numba` — already implicit, but
  document it so the cache is shared and warm across runs.

Combined expected speedup over §4.1: 5-10 %.

### 4.3 Tertiary — share the JIT cache warm-up

Right now, every cell-worker re-compiles the model from numba IR on
its *first* fit (~few seconds each), then caches in-process for fits
2-100. If you re-architect cell-workers to be **long-lived
worker-pool members** (e.g. one persistent worker per CPU, each
processing multiple cells sequentially), the JIT compile cost
amortises across all 100 × (cells/worker) ≈ 3 750 fits per worker.

This is **not** essential — the current 100-fits-per-cell pattern
already amortises well — but it would remove the ~few-seconds-per-cell
cold-start penalty that adds up to ~30 minutes across 450 cells.

Caveat: long-lived workers risk gradual memory growth (numba caches,
arviz buffers). At 2.5 GB RSS per worker now (§2.1, VmRSS = 2.4 GB),
12 workers × 5 GB/worker after long lifetime = 60 GB. Watch for OOM.
This is a real engineering cost; skip it unless §4.1 alone doesn't
hit the budget.

### 4.4 Validate-before-commit

Before launching the 450-cell × 100-replicate next run, do a
**10-cell × 10-replicate calibration** under the proposed §4.1
config, stratified across N ∈ {2 000, 10 000, 50 000} (e.g. 3-4
cells per N stratum). This catches:

- N-effect at N=50 000 (currently unmeasured)
- Whether pinning actually delivers the expected speedup
- Whether the throughput holds steady over a real wall-clock window
  (rules out thermal throttling, which could hit on a 12-physical-core
  sustained load if cooling is marginal)

Wall budget for this calibration: ~30-60 min on a quiet box. Cheap
insurance.

## 5. What I would try if I had another day

Open threads, not blockers for the next run:

1. **Quantify the L3-cache-pressure component.** The investigation
   can't separate "SMT contention" from "shared-L3 thrashing"
   without `perf stat -e LLC-loads,LLC-load-misses`. That requires
   either `sudo sysctl kernel.perf_event_paranoid=1` or a
   privileged perf binary. Worth doing once to know whether
   *strictly-isolated CCD pinning* (e.g. 6 workers on CCD0 only)
   beats the 12-workers-across-both-CCDs layout in §4.1.
2. **Try `nuts_sampler='numpyro'`.** PyMC accepts a JAX-backed NUTS
   sampler that some users report 2-5× faster than the pytensor-numba
   default on small-to-mid Bayesian models. Requires installing JAX
   + numpyro in the venv (~200 MB). The mixture model here has
   fairly simple structure; numpyro often wins on these. *Caveat:*
   different sampler implementation → different RNG path → not
   bitwise reproducible vs the current run. This is a **design
   change** (different sampler is a different inference engine,
   even if mathematically equivalent for the model spec), so it
   needs the "no silent parameter changes" gate Shawn called out.
   Flag loudly if pursuing.
3. **Profile where inside `pm.sample` the time goes.** py-spy
   `record` (for flamegraphs) is blocked by `ptrace_scope=1` on
   sapphire; either lower that to 0 transiently for diagnostic
   work, or run the profiler inside a fresh process I own from the
   start. A flamegraph would distinguish "logp evaluation" from
   "leapfrog" from "tree-doubling"; the first is the N-dependent
   cost (H11), the others are constant in N.
4. **Investigate why the recovered-grid run's mean fit time
   monotonically increases across the first 13 cells** (54 → 96 s).
   The simple explanation is "N=2 000 cells happened to complete
   first, N=10 000 later" — and the per-N grouping (§2.6) confirms
   this is largely the explanation. But it's worth checking whether
   there's also a thermal-throttling or memory-fragmentation
   secondary trend within an N stratum. Slice
   `mean_fit_seconds` by `(N, completion_order_within_N)` once
   more cells finish.
5. **Confirm the n_jobs sweet spot empirically.** Run §4.4-style
   calibrations at n_jobs ∈ {8, 10, 12, 14, 16} and pick the
   throughput peak. The theory says 12 is the knee; the data
   should confirm before committing to a 25-35 h run.

## 6. Notes on what I did not do (constraint compliance)

- Did not signal, kill, or modify the live grid processes.
- Did not write to `~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/`.
  All diagnostic outputs (sandbox data, benchmark scripts) live in
  `~/cc-scratch/sapphire-concurrency-debug/`.
- Did not touch `~/.pytensor/`. I read directory listings, file
  counts, and `stat`-level mtime, but did not delete or modify
  anything.
- The two benchmarks I ran (taskset -c 11 and taskset -c 18,
  one fit each, ~70 s each) consumed 1 CPU thread for ~2.5 min
  total. The live grid's per-worker throughput briefly dropped to
  18/19 of its prior capacity during each benchmark. Negligible.
- Did not install system packages. py-spy was installed in a
  fresh venv under `~/cc-scratch/sapphire-concurrency-debug/venv-debug/`;
  it ultimately could not attach to live workers because of
  `ptrace_scope=1`, but the install itself is harmless and isolated.
