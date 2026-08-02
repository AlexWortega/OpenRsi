# Question: can F_2^6 \ {0} be partitioned into 4 sum-free sets (<=> XOR-type triangle-free 4-coloring of K_64)?
# SAT variables: x[v][c] for v in 1..63, c in 0..3. Exactly-one per v.
# For every line {u,v,u^v}: not all three same color -> for each color c, clause (~x_u_c | ~x_v_c | ~x_w_c)
# Symmetry breaking: fix color of v=1 to 0; v=2 in {0,1}; first vertex of color 2 before first of color 3 etc. (simple: c(1)=0, c(2)<=1, c(3)<=2 if not forced).
import sys
from pysat.solvers import Cadical195
from pysat.formula import CNF

n = 63
K = 4
def var(v, c): return (v-1)*K + c + 1

cnf = CNF()
for v in range(1, n+1):
    cnf.append([var(v,c) for c in range(K)])
    for c1 in range(K):
        for c2 in range(c1+1, K):
            cnf.append([-var(v,c1), -var(v,c2)])

lines = set()
for u in range(1, n+1):
    for v in range(u+1, n+1):
        w = u ^ v
        if w > v:
            lines.add((u,v,w))
print(f"lines: {len(lines)}", flush=True)
for (u,v,w) in lines:
    for c in range(K):
        cnf.append([-var(u,c), -var(v,c), -var(w,c)])

# symmetry breaking on colors: vertex 1 -> color 0; vertex 2 -> color in {0,1}; vertex 3 -> {0,1,2}
cnf.append([var(1,0)])
cnf.append([-var(2,2)]); cnf.append([-var(2,3)])
cnf.append([-var(3,3)])

s = Cadical195(bootstrap_with=cnf)
res = s.solve()
print("SAT" if res else "UNSAT", flush=True)
if res:
    m = s.get_model()
    col = {}
    for v in range(1, n+1):
        for c in range(K):
            if m[var(v,c)-1] > 0:
                col[v] = c
    classes = [[v for v in range(1,n+1) if col[v]==c] for c in range(K)]
    for i, cl in enumerate(classes):
        print(f"S{i} ({len(cl)}): {cl}")
    # verify
    for (u,v,w) in lines:
        assert not (col[u]==col[v]==col[w]), (u,v,w)
    print("verified: all lines nonmonochromatic")
