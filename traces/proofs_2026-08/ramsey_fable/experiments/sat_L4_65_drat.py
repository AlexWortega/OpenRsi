#!/usr/bin/env python3
"""Same instance as sat_L4_65_struct.py but writes DIMACS + DRAT proof and
checks the proof with drat-trim. Usage:
  sat_L4_65_drat.py pal0 pal1 pal2 pal3 outdir
Prints VERIFIED-UNSAT / SAT / error. Exit 0 on verified UNSAT or on SAT
(witness written), 3 on verification failure.
"""
import sys, os, json, time, subprocess, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

pals = [tuple(int(x) for x in a.split(",")) for a in sys.argv[1:5]]
outdir = sys.argv[5]
os.makedirs(outdir, exist_ok=True)
tag = "_".join("".join(map(str, p)) for p in pals)
P = [set(p) | {i} for i, p in enumerate(pals)]

pool = IDPool()
def cls(v): return v // 16
def xe(u, v, c):
    if u > v: u, v = v, u
    return pool.id(("e", u, v, c))
def dom(u, v):
    i, j = cls(u), cls(v)
    return sorted(pals[i]) if i == j else sorted(P[i] & P[j])

clauses = []
edges = list(itertools.combinations(range(64), 2))
for u, v in edges:
    d = dom(u, v)
    assert d, "cross palette empty — should have been filtered"
    vs = [xe(u, v, c) for c in d]
    clauses.append(vs)
    for p, q in itertools.combinations(vs, 2):
        clauses.append([-p, -q])
for u, v, w in itertools.combinations(range(64), 3):
    for c in set(dom(u, v)) & set(dom(u, w)) & set(dom(v, w)):
        clauses.append([-xe(u, v, c), -xe(u, w, c), -xe(v, w, c)])
for v in range(64):
    i = cls(v)
    ins = [u for u in range(16 * i, 16 * i + 16) if u != v]
    outs = [u for u in range(64) if cls(u) != i]
    for c in pals[i]:
        cnf = CardEnc.equals([xe(u, v, c) for u in ins], bound=5, vpool=pool,
                             encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)
    lits = [xe(u, v, i) for u in outs if i in dom(u, v)]
    assert len(lits) >= 15
    cnf = CardEnc.equals(lits, bound=15, vpool=pool, encoding=EncType.seqcounter)
    clauses.extend(cnf.clauses)
    for c in pals[i]:
        lits = [xe(u, v, c) for u in outs if c in dom(u, v)]
        assert len(lits) >= 11
        cnf = CardEnc.equals(lits, bound=11, vpool=pool, encoding=EncType.seqcounter)
        clauses.extend(cnf.clauses)

cnf_path = os.path.join(outdir, f"{tag}.cnf")
with open(cnf_path, "w") as f:
    f.write(f"p cnf {pool.top} {len(clauses)}\n")
    for cl in clauses:
        f.write(" ".join(map(str, cl)) + " 0\n")

t0 = time.time()
s = Cadical195(bootstrap_with=clauses, with_proof=True)
res = s.solve()
el = time.time() - t0
if res:
    m = set(l for l in s.get_model() if l > 0)
    col = {}
    for u, v in edges:
        for c in dom(u, v):
            if xe(u, v, c) in m:
                col[f"{u+1},{v+1}"] = c
    for v in range(64):
        col[f"0,{v+1}"] = cls(v)
    fn = os.path.join(outdir, f"L4_65_witness_{tag}.json")
    with open(fn, "w") as f:
        json.dump({"N": 65, "edges": col}, f)
    print(f"SAT ({el:.0f}s) witness {fn}")
    sys.exit(0)
proof = s.get_proof()
drat_path = os.path.join(outdir, f"{tag}.drat")
with open(drat_path, "w") as f:
    f.write("\n".join(proof) + "\n")
    # ensure the proof ends with the empty clause; appending it is sound since
    # drat-trim must still verify it is RUP w.r.t. the accumulated clauses
    if not proof or proof[-1].strip() != "0":
        f.write("0\n")
r = subprocess.run(["/tmp/drat-trim/drat-trim", cnf_path, drat_path],
                   capture_output=True, text=True, timeout=7200)
if "s VERIFIED" in r.stdout:
    print(f"VERIFIED-UNSAT ({el:.0f}s solve; drat-trim OK)")
    os.remove(drat_path)  # keep disk sane; cnf kept? remove too
    os.remove(cnf_path)
    sys.exit(0)
print(f"DRAT VERIFICATION FAILED for {tag}:\n{r.stdout[-500:]}")
sys.exit(3)
