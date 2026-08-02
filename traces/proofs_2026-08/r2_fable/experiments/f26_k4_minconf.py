# Question: does F_2^6\{0} partition into 4 sum-free sets? Min-conflicts local search
# (SAT solver grinding in parallel). Success => R_4(3) >= 65 (known LB: 51).
import numpy as np, sys, random

n = 63
K = 4
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
random.seed(seed)

lines = []
for u in range(1, n+1):
    for v in range(u+1, n+1):
        w = u ^ v
        if w > v: lines.append((u, v, w))
lines_of = [[] for _ in range(n+1)]
for i, (u, v, w) in enumerate(lines):
    for x in (u, v, w): lines_of[x].append(i)

def n_mono(col):
    return sum(1 for (u,v,w) in lines if col[u]==col[v]==col[w])

best_overall = 10**9
for restart in range(10**9):
    col = [0]*(n+1)
    for v in range(1, n+1): col[v] = random.randrange(K)
    # count mono lines
    def mono_count_local(v, c):
        cnt = 0
        for i in lines_of[v]:
            a,b,w = lines[i]
            others = [x for x in (a,b,w) if x != v]
            if col[others[0]]==c and col[others[1]]==c: cnt += 1
        return cnt
    cur = n_mono(col)
    steps = 0
    while cur > 0 and steps < 400000:
        steps += 1
        # pick a random violated line
        while True:
            i = random.randrange(len(lines))
            u,v,w = lines[i]
            if col[u]==col[v]==col[w]: break
        x = random.choice((u,v,w))
        c0 = col[x]
        base = mono_count_local(x, c0)
        # best alternative color (with noise)
        if random.random() < 0.15:
            c1 = random.randrange(K)
        else:
            best_c, best_d = c0, 0
            for c1 in range(K):
                if c1 == c0: continue
                d = mono_count_local(x, c1) - base
                if d < best_d: best_d, best_c = d, c1
            c1 = best_c
        if c1 != c0:
            cur += mono_count_local(x, c1) - base
            col[x] = c1
    if cur < best_overall:
        best_overall = cur
        print(f"restart {restart}: best={cur}", flush=True)
    if cur == 0:
        print("SOLVED! coloring:", col[1:], flush=True)
        # verify
        assert n_mono(col) == 0
        classes = [[v for v in range(1,n+1) if col[v]==c] for c in range(K)]
        for i,cl in enumerate(classes): print(f"S{i} ({len(cl)}): {cl}")
        sys.exit(0)
