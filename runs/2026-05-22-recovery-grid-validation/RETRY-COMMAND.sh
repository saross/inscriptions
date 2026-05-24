#!/usr/bin/env bash
# =============================================================================
# RETRY-COMMAND.sh — Re-attempt the 12 cells that failed during the main grid
# run (2026-05-22 06:17 -> 2026-05-23 12:07).
#
# Root cause of the 12 failures: /tmp (tmpfs, 31G, ~1M inodes) hit its inode
# limit during a transient spike of pytensor compile-temp-file accumulation
# while the smooth_decline shape cells at alpha=0.30 were running. The
# allow_gc=False PYTENSOR flag prevents pytensor from cleaning up its
# NamedTemporaryFile artefacts as it goes; with 12 workers continuously
# recompiling, /tmp ran out of inodes well before it ran out of bytes
# (4.4 GB used / 1,048,576 inodes saturated). Linux reports ENOSPC for both.
#
# Mitigations applied for the retry:
#   1. /tmp cleaned (1,048,559 -> 17 inodes used).
#   2. TMPDIR redirected to disk-backed location (NVMe; 433 GB free).
#      Pytensor's NamedTemporaryFile honours TMPDIR; with disk-backed
#      storage we cannot run out of inodes during the ~50 min retry.
#
# All other config (n_jobs, taskset, PYTENSOR_FLAGS, threading caps) is
# identical to RESTART-COMMAND.sh — the retry uses the same optimised
# concurrency profile that brought the original grid in at 29.84 h vs the
# 31.6 h projection.
#
# Resumability: orchestrator overwrites grid-state.json on relaunch (line 222
# of 04-grid-runner.py). Cell-worker resume-skip (lines 131-137) checks for
# outputs/cell-summaries/{cell_id}-summary.json. 438 completed cells have
# summaries -> workers exit 0 instantly. 12 failed cells have no summary
# -> workers re-run them. Within each cell, replicate-level resume (line
# 165) skips replicates whose posterior JSON already exists. 473 of 1200
# replicate posteriors survive the failure; 727 fits remain.
#
# Author / date: Claude (Opus 4.7, 1M context), 2026-05-23.
# =============================================================================

set -euo pipefail

RUN_ROOT="/home/shawn/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation"
DESIGN_JSON="${RUN_ROOT}/../2026-05-22-recovery-grid-design/design.json"
VENV="/home/shawn/cc-scratch/inscriptions-talk-prep/venv"
RETRY_TMPDIR="/home/shawn/cc-scratch/inscriptions-recovery-grid/pytensor-tmp"

cd "${RUN_ROOT}"

# Activate the venv used by the original run.
# shellcheck disable=SC1091
source "${VENV}/bin/activate"

# Single-threaded BLAS / OpenMP / numba.
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export NUMBA_NUM_THREADS=1

# PYTENSOR_FLAGS — identical to RESTART-COMMAND.sh.
export PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"

# NEW for retry: TMPDIR redirect to disk-backed location to avoid the
# tmpfs inode exhaustion that caused the original 12 failures.
mkdir -p "${RETRY_TMPDIR}"
export TMPDIR="${RETRY_TMPDIR}"
echo "TMPDIR set to: ${TMPDIR}"
echo "TMPDIR free space:"
df -h "${TMPDIR}" | tail -1

# nohup + taskset -c 0-11 + python ...
# Stdout/stderr go to outputs/grid-runner-retry.log (new file; keeps the
# main grid-runner.log clean as a historical record of the 29.84 h run).
mkdir -p outputs
nohup taskset -c 0-11 python code/04-grid-runner.py \
    --design-json "${DESIGN_JSON}" \
    --output-root . \
    --n-jobs 12 \
    >> outputs/grid-runner-retry.log 2>&1 &

GRID_PID=$!
echo "GRID_PID=${GRID_PID}"

# Brief sanity check.
sleep 5
ps -p "${GRID_PID}" -o pid,etime,pcpu,pmem,comm 2>/dev/null || {
    echo "ERROR: grid runner exited within 5s; check outputs/grid-runner-retry.log"
    tail -25 outputs/grid-runner-retry.log 2>/dev/null
    exit 1
}
echo "--- log (first 25 lines after launch) ---"
tail -25 outputs/grid-runner-retry.log 2>/dev/null
echo "--- relaunch complete ---"
