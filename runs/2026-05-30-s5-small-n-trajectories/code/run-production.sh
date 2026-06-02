#!/usr/bin/env bash
# run-production.sh — §5 Layer-A production launch wrapper.
# =========================================================
#
# Sets the threading / pytensor / scratch hygiene IN THE SHELL — before Python
# imports numpy/pytensor, so there is no import-order fragility — then execs the
# orchestrator. This is the tracked, foolproof launch path: the launch command
# IS this wrapper, so the environment can never be forgotten (cf. the
# 2026-05-22 SMT-oversubscription failure: 19 workers on 12 physical cores cost
# ~3.2x per-fit time). Supersedes the untracked ~/cc-scratch/s5/s5-env.sh.
#
# Usage:
#   bash run-production.sh                       # DRY RUN — plan + estimate, samples NOTHING
#   bash run-production.sh --confirm-production \
#        --out-base runs/2026-05-30-s5-small-n-trajectories/code/production
#                                                # the PRODUCTION RUN
#   (every argument is passed through verbatim to orchestrate.py)
#
# Author / Date
# -------------
# Claude (Opus 4.8, 1M context), 2026-05-31, on Shawn's brief.

set -euo pipefail

CODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${CODE_DIR}/../../.." && pwd)"

# Threading hygiene: one thread per BLAS / OpenMP backend. pymc multiprocesses
# its chains; letting each chain's BLAS also grab every core oversubscribes the
# machine (the 2026-05-22 lesson). Pin every backend to a single thread.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 NUMBA_NUM_THREADS=1

# pytensor: fast compiled mode, no per-node garbage collection.
export PYTENSOR_FLAGS="mode=FAST_RUN,allow_gc=False"

# Disk-backed scratch — tmpfs /tmp has a ~1,048,576-inode ceiling that pytensor
# recompiles can blow through (the 2026-05-23 lesson). Override TMPDIR only if
# the caller has not already set one.
export TMPDIR="${TMPDIR:-${HOME}/cc-scratch/s5/pytensor-tmp}"
mkdir -p "${TMPDIR}"

PY="${PY:-${REPO_ROOT}/.venv/bin/python}"
ORCH="${CODE_DIR}/orchestrate.py"

if [[ ! -f "${PY}" ]]; then
    echo "FATAL: python venv not found at ${PY}" >&2
    exit 2
fi
if [[ ! -f "${ORCH}" ]]; then
    echo "FATAL: orchestrator not found at ${ORCH}" >&2
    exit 2
fi

cd "${REPO_ROOT}"

# Pre-flight dependency check: import every runtime package + verify the HDF5
# netCDF backend BEFORE anything samples. The wrapper-level guard against the
# 2026-05-31 failure (a 5.7 h run that crashed at the final step on a missing
# scikit-learn). Set SKIP_PREFLIGHT=1 to bypass (e.g. to read the dry-run plan
# on a host without the full stack). orchestrate.py also asserts this internally.
if [[ "${SKIP_PREFLIGHT:-0}" != "1" ]]; then
    echo "[run-production] preflight: verifying environment ..."
    "${PY}" "${CODE_DIR}/preflight.py"
fi

echo "[run-production] repo=${REPO_ROOT}"
echo "[run-production] PY=${PY}"
echo "[run-production] TMPDIR=${TMPDIR}  PYTENSOR_FLAGS=${PYTENSOR_FLAGS}"
echo "[run-production] threads OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/NUMBA = 1"
echo "[run-production] exec: orchestrate.py $*"
exec "${PY}" "${ORCH}" "$@"
