#!/usr/bin/env python3
# Question: can t copies of the F2^7 five-color seed be recolored with q colors when repeated coarse-state lines are enforced?
import argparse, itertools, json, time
from pysat.formula import CNF
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument("-t", type=int, default=3)
ap.add_argument("-q", type=int, default=14)
ap.add_argument("--solver", default="cadical195")
ap.add_argument("--out", default="experiments/block_power_correct_sat.json")
ap.add_argument("--constraints", default="experiments/block_power_constraints.json")
args = ap.parse_args()
classes = json.load(open("experiments/f2_7_5.json"))
base = {x: i + 1 for i, part in enumerate(classes) for x in part}
def state(x): return 0 if x == 0 else base[x]
R = {(state(x), state(y), state(x ^ y)) for x in range(128) for y in range(128)}
states = [s for s in itertools.product(range(6), repeat=args.t) if any(s)]
index = {s: i for i, s in enumerate(states)}
constraints = set()
for rels in itertools.product(R, repeat=args.t):
    ss = tuple(tuple(rels[j][h] for j in range(args.t)) for h in range(3))
    if all(any(s) for s in ss):
        u = tuple(sorted({index[s] for s in ss}))
        if len(u) >= 2:
            constraints.add(u)

def var(i, c): return i * args.q + c + 1
cnf = CNF()
for i in range(len(states)):
    cnf.append([var(i, c) for c in range(args.q)])
    for a, b in itertools.combinations(range(args.q), 2):
        cnf.append([-var(i, a), -var(i, b)])
# Color symmetry: the first state can be color zero.
cnf.append([var(0, 0)])
for u in constraints:
    for c in range(args.q):
        cnf.append([-var(i, c) for i in u])
json.dump({"t":args.t,"states":[list(s) for s in states],"constraints":[list(u) for u in sorted(constraints)]},open(args.constraints,"w"))
print(json.dumps({"states": len(states), "relations": len(R), "constraints": len(constraints), "clauses": len(cnf.clauses)}), flush=True)
t0 = time.time()
with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
    sat = solver.solve()
    print(json.dumps({"sat": sat, "seconds": time.time() - t0}), flush=True)
    if sat:
        model = {v for v in solver.get_model() if v > 0}
        mapping = {",".join(map(str, s)): next(c for c in range(args.q) if var(i, c) in model) for i, s in enumerate(states)}
        json.dump({"t": args.t, "q": args.q, "mapping": mapping}, open(args.out, "w"), indent=2)
        print("wrote", args.out, flush=True)
