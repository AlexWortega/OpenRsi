#!/bin/bash
# Certified pipeline: per palette case, gen CNF -> kissat (DRAT) -> drat-trim.
# Usage: run_L4_certified.sh cases.txt workdir workers
cd "$(dirname "$0")/.."
CASES="$1"; WD="$2"; W="${3:-10}"
mkdir -p "$WD"
run_one() {
    line="$1"; WD="$2"
    tag=$(echo "$line" | tr ' ,' '__')
    res="$WD/$tag.result"
    [ -s "$res" ] && return
    cnf="$WD/$tag.cnf"; drat="$WD/$tag.drat"
    python3 experiments/gen_L4_cnf.py $line "$cnf" > /dev/null 2>&1 || { echo "GENFAIL" > "$res"; return; }
    timeout 7200 /tmp/kissat/build/kissat -q "$cnf" "$drat" > "$WD/$tag.sol" 2>&1
    st=$?
    if [ $st -eq 20 ]; then
        if timeout 7200 /tmp/drat-trim/drat-trim "$cnf" "$drat" 2>&1 | tr -d '\r' | grep -q '^s VERIFIED'; then
            echo "VERIFIED-UNSAT" > "$res"
            rm -f "$cnf" "$drat" "$WD/$tag.sol"
        else
            echo "UNSAT-UNVERIFIED" > "$res"
        fi
    elif [ $st -eq 10 ]; then
        echo "SAT" > "$res"   # keep cnf+sol for witness extraction
    else
        echo "TIMEOUT-OR-ERROR($st)" > "$res"
    fi
    echo "done: $line -> $(cat "$res")"
}
export -f run_one
grep -v '^#' "$CASES" | xargs -I{} -P "$W" bash -c 'run_one "{}" "'"$WD"'"'
echo ALL DONE
