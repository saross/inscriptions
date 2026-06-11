#!/usr/bin/env bash
# run-cc-arm.sh — detached cc-grid (D-B) launch wrapper for sapphire.
#
# Mirrors the proven ~/run_full_grid.sh pattern (cgroup MemoryMax scope via
# systemd-run --user, root-fs TMPDIR, memwatch trace, resumable runner) for the
# cross-classified arm. Usage, ON sapphire, from the run directory:
#
#   setsid bash code/run-cc-arm.sh <arm> <pilot|full> [n_jobs] [MemoryMax]
#   # e.g. pilot, all three arms sequentially:
#   setsid bash -c 'for a in tiers3 library free; do
#       bash code/run-cc-arm.sh "$a" pilot 12 50G; done' &
#   # full run of the chosen arm:
#   setsid bash code/run-cc-arm.sh library full 12 50G &
#
# Stop a scoped job with `systemctl --user stop <scope>` (NOT pkill) — list with
# `systemctl --user list-units --type=scope`.
set -u

ARM="${1:?arm required: tiers3|library|free}"
STAGE="${2:?stage required: pilot|full}"
N_JOBS="${3:-12}"
MEM_MAX="${4:-50G}"

case "$STAGE" in
  pilot) STAGE_FLAG="--pilot"; TAG="${ARM}-pilot" ;;
  full)  STAGE_FLAG="";        TAG="${ARM}" ;;
  *) echo "stage must be pilot or full"; exit 9 ;;
esac

RUN="$HOME/Code/inscriptions/runs/2026-06-09-joint-identifiability"
cd "$RUN" || exit 9
export PATH="$HOME/.local/bin:$PATH"
export TMPDIR="$HOME/tmp_grid_scratch"; mkdir -p "$TMPDIR"
export PYTENSOR_FLAGS="mode=FAST_RUN,base_compiledir=$HOME/.pytensor_grid"
# Needed for `systemd-run --user` to reach the user bus from a detached session.
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"

LOG="$RUN/outputs/cc-${TAG}.log"
MEMLOG="$RUN/outputs/cc-memwatch-${TAG}.log"
: > "$MEMLOG"
echo "=== cc-grid launch [$TAG] $(date '+%F %T')  n_jobs=$N_JOBS  MemoryMax=$MEM_MAX ===" >> "$LOG"

# Memory + /tmp + progress watchdog (logs only).
(
  while true; do
    ts=$(date '+%F %T')
    memav=$(awk '/MemAvailable/{printf "%.1f", $2/1024/1024}' /proc/meminfo)
    toprss=$(ps -eo rss,comm --sort=-rss --no-headers | awk '/[p]ython/{print $1; exit}')
    npy=$(pgrep -c -f '[p]ython')
    inod=$(df -i /tmp | awk 'NR==2{print $5}')
    cells=$(ls "$RUN/outputs/grid-cc-${TAG}"/*.json 2>/dev/null | wc -l)
    echo "$ts  memAvail=${memav}GB topPyRSS_KB=${toprss:-0} pyProcs=${npy} tmpInodes=${inod} cellsDone=${cells}" >> "$MEMLOG"
    sleep 60
  done
) &
WATCH=$!

# shellcheck disable=SC2086 — STAGE_FLAG is deliberately word-split (empty for full).
GRID_CMD=(taskset -c 0-11 uv run python code/run_cc_grid.py
          --pconv-mode "$ARM" $STAGE_FLAG --n-jobs "$N_JOBS" --max-tasks-per-child 1)

if systemd-run --user --scope -p MemoryMax=64M --quiet true >/dev/null 2>&1; then
  echo "MEMORY-CAP: systemd --user scope MemoryMax=$MEM_MAX MemorySwapMax=0" >> "$LOG"
  systemd-run --user --scope -p MemoryMax="$MEM_MAX" -p MemorySwapMax=0 \
      "${GRID_CMD[@]}" >> "$LOG" 2>&1
  RC=$?
else
  echo "MEMORY-CAP: systemd-run --user unavailable — running UNCAPPED" >> "$LOG"
  "${GRID_CMD[@]}" >> "$LOG" 2>&1
  RC=$?
fi

kill "$WATCH" 2>/dev/null
echo "CC_GRID_EXIT[$TAG]=$RC ($(date '+%F %T'))" | tee -a "$LOG" >> "$MEMLOG"
exit "$RC"
