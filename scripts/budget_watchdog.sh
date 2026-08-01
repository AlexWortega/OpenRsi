#!/bin/bash
# Kill a proofs runner when its logged spend reaches a cap, and append a
# synthetic DONE line so the tracehouse bridge and any log-watchers finish cleanly.
# Usage: budget_watchdog.sh <node_pid> <log_path> <cap_usd> <trigger_usd>
PID=$1; LOG=$2; CAP=$3; TRIG=$4
while kill -0 "$PID" 2>/dev/null; do
  SPENT=$(grep -oE "spent \$[0-9.]+" "$LOG" 2>/dev/null | tail -1 | tr -dc "0-9.")
  if [ -n "$SPENT" ] && awk -v s="$SPENT" -v t="$TRIG" "BEGIN{exit !(s>=t)}"; then
    ROUND=$(grep -cE "nudge [0-9]+" "$LOG")
    kill "$PID"; sleep 8; kill -9 "$PID" 2>/dev/null
    TAG=$(grep -oE "^\[proofs[0-9]*\]" "$LOG" | head -1 | tr -d "[]")
    echo "[$TAG] DONE after $ROUND rounds, cost=\$$SPENT (budget capped at \$$CAP by watchdog)" >> "$LOG"
    exit 0
  fi
  sleep 30
done
