#!/usr/bin/env bash
# run-both-grids.sh
# =================
#
# Sequential wrapper for the two-unit recovery-grid re-simulation
# (spec.md §6 — total wall ~ 60 h sequential).
#
# Runs Grid A (inscription-mass) then Grid B (letter-mass conservative)
# under the SMT-pinned config: taskset -c 0-11 (the first physical-core
# half of sapphire's 24 logical CPUs) with --n-jobs 12 and BLAS threads
# capped to 1.
#
# Writes status checkpoints to STATUS.txt (side-channel signal for
# remote pollers) after each major milestone:
#   - SMOKE-PASS (after pre-launch gates)
#   - GRID-A-START / GRID-A-END
#   - GRID-B-START / GRID-B-END
#
# Usage on sapphire (after pre-launch gates pass and harness is
# committed):
#   nohup ./run-both-grids.sh > nohup.out 2>&1 &
#   echo "PID=$!"
#
# Author / Date
# -------------
# Claude (Opus 4.7, 1M context), 2026-05-26, on Shawn's brief.

set -euo pipefail

# ---------------------------------------------------------------------------
# Paths and environment.
# ---------------------------------------------------------------------------
CODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_ROOT="$(cd "${CODE_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${RUN_ROOT}/../.." && pwd)"
DESIGN_JSON="${REPO_ROOT}/runs/2026-05-22-recovery-grid-design/design.json"
LETTER_PARQUET="${REPO_ROOT}/runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet"

PYTHON="${PYTHON:-/home/shawn/cc-scratch/inscriptions-talk-prep/venv/bin/python}"
TMPDIR_BASE="${TMPDIR_BASE:-/home/shawn/cc-scratch/inscriptions-recovery-grid-two-unit/pytensor-tmp}"

STATUS_PATH="${RUN_ROOT}/STATUS.txt"

# SMT pinning: sapphire has 24 logical CPUs (12 physical x 2 SMT). The
# 2026-05-22 benchmark established that taskset -c 0-11 + n_jobs=12
# (the first half of logical CPUs, one per physical core) outperforms
# the n_jobs=24 SMT-unaware default.
TASKSET_CORES="${TASKSET_CORES:-0-11}"
N_JOBS="${N_JOBS:-12}"

# BLAS / OpenMP single-thread (mandatory under multi-process pmc fits).
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export NUMBA_NUM_THREADS=1

# pytensor FAST_RUN + disk-backed scratch (2026-05-23 learned lesson:
# tmpfs /tmp has a 1,048,576-inode ceiling that pytensor recompiles can
# blow through).
mkdir -p "${TMPDIR_BASE}"
export TMPDIR="${TMPDIR_BASE}"
export PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"

# ---------------------------------------------------------------------------
# Status helper.
# ---------------------------------------------------------------------------
status() {
    local msg="$1"
    local ts
    ts="$(date '+%Y-%m-%d %H:%M:%S')"
    printf '[%s] %s\n' "${ts}" "${msg}" >> "${STATUS_PATH}"
    printf '[wrapper] [%s] %s\n' "${ts}" "${msg}"
}

# Truncate STATUS.txt at launch so pollers see a fresh record.
: > "${STATUS_PATH}"
status "WRAPPER-START host=$(hostname) pid=$$ pwd=$(pwd)"
status "config: TASKSET=${TASKSET_CORES} N_JOBS=${N_JOBS} TMPDIR=${TMPDIR}"
status "design: ${DESIGN_JSON}"
status "letter-parquet: ${LETTER_PARQUET}"

# Sanity-check inputs.
for f in "${DESIGN_JSON}" "${LETTER_PARQUET}"; do
    if [[ ! -e "${f}" ]]; then
        status "FATAL missing input: ${f}"
        exit 2
    fi
done
if ! "${PYTHON}" -c 'import pymc, arviz, statsmodels, scipy, numpy, pandas' 2>/dev/null; then
    status "FATAL python venv missing required packages."
    exit 2
fi

# ---------------------------------------------------------------------------
# Smoke pass — assumed to have been run independently before launch.
# The gates write their own JSON outputs under comparison/ and
# */outputs/cell-summaries/. We sanity-check those exist here; the
# wrapper does NOT re-run the gates (they are slow and the main agent
# runs them before commit).
# ---------------------------------------------------------------------------
SMOKE_A="${RUN_ROOT}/inscription-mass/outputs/cell-summaries/shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000-summary.json"
SMOKE_B="${RUN_ROOT}/letter-mass/outputs/cell-summaries/shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000-summary.json"
PROXY_A="${RUN_ROOT}/inscription-mass/data/pilot-proxy.json"
PROXY_B="${RUN_ROOT}/letter-mass/data/pilot-proxy.json"

for f in "${SMOKE_A}" "${SMOKE_B}" "${PROXY_A}" "${PROXY_B}"; do
    if [[ ! -e "${f}" ]]; then
        status "FATAL pre-launch artefact missing: ${f}"
        exit 2
    fi
done
status "SMOKE-PASS (gate artefacts located)"

# ---------------------------------------------------------------------------
# Grid A: inscription-mass.
# ---------------------------------------------------------------------------
status "GRID-A-START unit=inscription"
GRID_A_T0=$(date +%s)
taskset -c "${TASKSET_CORES}" "${PYTHON}" "${CODE_DIR}/run-grid.py" \
    --mode orchestrator \
    --unit inscription \
    --design-json "${DESIGN_JSON}" \
    --run-root "${RUN_ROOT}" \
    --n-jobs "${N_JOBS}" \
    --n-replicates 100 \
    --n-draws 2000 \
    --n-tune 1000 \
    --n-chains 4 \
    --target-accept 0.95 \
    --cores 1
GRID_A_RC=$?
GRID_A_T1=$(date +%s)
GRID_A_WALL=$((GRID_A_T1 - GRID_A_T0))
status "GRID-A-END rc=${GRID_A_RC} wall=${GRID_A_WALL}s"

if [[ "${GRID_A_RC}" -ne 0 ]]; then
    status "WRAPPER-EXIT-ON-A-FAILURE rc=${GRID_A_RC}"
    exit "${GRID_A_RC}"
fi

# ---------------------------------------------------------------------------
# Grid B: letter-mass conservative.
# ---------------------------------------------------------------------------
status "GRID-B-START unit=letter"
GRID_B_T0=$(date +%s)
taskset -c "${TASKSET_CORES}" "${PYTHON}" "${CODE_DIR}/run-grid.py" \
    --mode orchestrator \
    --unit letter \
    --design-json "${DESIGN_JSON}" \
    --run-root "${RUN_ROOT}" \
    --letter-parquet "${LETTER_PARQUET}" \
    --n-jobs "${N_JOBS}" \
    --n-replicates 100 \
    --n-draws 2000 \
    --n-tune 1000 \
    --n-chains 4 \
    --target-accept 0.95 \
    --cores 1
GRID_B_RC=$?
GRID_B_T1=$(date +%s)
GRID_B_WALL=$((GRID_B_T1 - GRID_B_T0))
status "GRID-B-END rc=${GRID_B_RC} wall=${GRID_B_WALL}s"

TOTAL_WALL=$((GRID_B_T1 - GRID_A_T0))
status "WRAPPER-DONE total_wall=${TOTAL_WALL}s grid_a_rc=${GRID_A_RC} grid_b_rc=${GRID_B_RC}"

# Surface a final nonzero exit if either grid failed.
if [[ "${GRID_A_RC}" -ne 0 || "${GRID_B_RC}" -ne 0 ]]; then
    exit 3
fi
exit 0
