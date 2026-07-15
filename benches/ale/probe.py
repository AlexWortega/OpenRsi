#!/usr/bin/env python3
"""One-off: validate the ALE eval path + introspect the Result object shape."""
import time
import ale_bench

TRIVIAL_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main(){
    // Read everything, print nothing meaningful. Exercises compile+run only.
    std::ios::sync_with_stdio(false);
    string line; while (getline(cin, line)) {}
    return 0;
}
"""

def dump(label, obj):
    attrs = [a for a in dir(obj) if not a.startswith("_")]
    print(f"[{label}] type={type(obj).__name__} attrs={attrs}")

pid = "ahc008"
t0 = time.time()
s = ale_bench.start(problem_id=pid, lite_version=True, num_workers=12,
                    run_visualization_server=False)
print(f"[timing] start={time.time()-t0:.1f}s")
print(f"[problem] id={s.problem_id} score_type={s.problem.metadata.score_type} "
      f"num_public={getattr(s,'num_public_cases',None)} num_private={getattr(s,'num_private_cases',None)}")
print(f"[statement] first 300 chars:\n{s.problem.statement[:300]}\n---")

t1 = time.time()
r = s.public_eval(TRIVIAL_CPP, code_language="cpp23", reuse_containers=True)
print(f"[timing] public_eval={time.time()-t1:.1f}s")
dump("Result", r)
for a in ("overall_absolute_score","overall_relative_score","num_cases","num_ac","num_wa",
          "num_tle","num_re","num_ce","cases","case_results","compile_error","stderr"):
    if hasattr(r, a):
        v = getattr(r, a)
        vs = str(v)
        print(f"  Result.{a} = {vs[:200]}")
print(f"[usage] current={s.current_resource_usage} remaining={s.remaining_resource_usage}")
s.close()
print("[done]")
