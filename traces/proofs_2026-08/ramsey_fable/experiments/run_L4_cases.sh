#!/bin/bash
# Parallel driver for structured L_4=65 palette cases.
# Usage: run_L4_cases.sh <cases-file> <workers>
cd "$(dirname "$0")/.."
CASES="$1"; W="${2:-10}"
mkdir -p logs/L4cases
run_one() {
    line="$1"
    tag=$(echo "$line" | tr ' ,' '__')
    log="logs/L4cases/$tag.log"
    [ -s "$log" ] && grep -qE "SAT|UNSAT|INFEASIBLE" "$log" && return
    timeout 7200 python3 experiments/sat_L4_65_struct.py $line > "$log" 2>&1
    echo "done: $line -> $(tail -n1 "$log")"
}
export -f run_one
cat "$CASES" | grep -v '^#' | xargs -I{} -P "$W" bash -c 'run_one "{}"'
echo ALL DONE
