#!/usr/bin/env bash
# ============================================================================
# finalise-comparison.sh
# ----------------------------------------------------------------------------
# Run AFTER Grid B (letter-mass) completes. Summarises BOTH grids, collects
# recovered-alpha bias for both, then runs the cross-grid comparison that
# drives the spec.md §5 Stage-3 launch decision.
#
# Idempotent: re-running re-summarises (cheap; Grid A is already done).
# Run where the per-replicate parquets live (sapphire at completion), then
# pull comparison/ back to a local host for the record.
#
# Uses the project .venv python DIRECTLY — never `uv run` — to avoid any
# environment sync. Sapphire must stay on its pymc-5.28 stack until the
# deliberate post-Grid-B upgrade (see PROVISIONING.md); these scripts only
# need pandas + pyarrow + matplotlib, which the old stack already has.
#
# Usage:
#   bash finalise-comparison.sh [RUN_ROOT]
#   PYTHON=/abs/path/to/python bash finalise-comparison.sh [RUN_ROOT]
#
# Author / Date: Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief.
# ============================================================================
set -euo pipefail

# Resolve RUN_ROOT (default: this script's parent = the run dir).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_ROOT="${1:-$(cd "$SCRIPT_DIR/.." && pwd)}"
REPO_ROOT="$(cd "$RUN_ROOT/../.." && pwd)"
PYTHON="${PYTHON:-$REPO_ROOT/.venv/bin/python3}"
CODE="$RUN_ROOT/code"

echo "[finalise] RUN_ROOT=$RUN_ROOT"
echo "[finalise] PYTHON=$PYTHON"
"$PYTHON" --version

for grid in inscription-mass letter-mass; do
  echo "=========================================================="
  echo "[finalise] $grid — per-grid summariser"
  "$PYTHON" "$CODE/grid-summariser.py" --grid-dir "$RUN_ROOT/$grid"
  echo "[finalise] $grid — recovered-alpha bias collection"
  "$PYTHON" "$CODE/collect-alpha-bias.py" --grid-dir "$RUN_ROOT/$grid"
done

echo "=========================================================="
echo "[finalise] cross-grid comparison"
"$PYTHON" "$CODE/compare-grids.py" --run-root "$RUN_ROOT"

echo "=========================================================="
echo "[finalise] DONE. Read: $RUN_ROOT/comparison/COMPARISON-REPORT.md"
echo "[finalise] HARD GATE: Stage-3 launch is gated on OSF Amendment 01"
echo "[finalise]            (not lodged as of 2026-06-02). Verdict yields a"
echo "[finalise]            RECOMMENDED path only — confirm with Shawn."
