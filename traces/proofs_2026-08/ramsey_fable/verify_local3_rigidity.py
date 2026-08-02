#!/usr/bin/env python3
"""Machine verification for the rigidity theorem:

    THEOREM. Every triangle-free locally-3 edge-coloring of K_16 uses exactly
    3 colors globally.

Proof outline (full write-up in proof_ramsey.md §5):
 (a) L_3 = 16 and the equality lemma [prior/round1/proof_ramsey.md, proved]:
     in any locally-3 triangle-free K_16, every vertex sees EXACTLY 3 colors
     and each incident color class has exactly 5 vertices (so every vertex is
     5-regular in each of its 3 colors).
 (b) Suppose 4 colors occur globally. Each vertex then misses exactly one
     color. Let m_c = #vertices missing color c; sum m_c = 16. The support of
     color c is the other 16 - m_c vertices, on which color graph G_c is
     5-regular; hence 16 - m_c is even (handshake) and >= 10 (Mantel /
     round1 corollary), i.e. m_c is even and m_c <= 6.
 (c) The multiset {m_c} is a partition of 16 into 4 even parts <= 6:
     exactly (6,6,4,0), (6,6,2,2), (6,4,4,2), (4,4,4,4). [checked here]
 (d) For each profile, exhaustive backtracking (C program rigidity_bt.c,
     compiled and run here; independently confirmed by CaDiCaL UNSAT on a
     different encoding) shows NO coloring exists with: edge (u,v) colored
     outside {miss(u), miss(v)}, no monochromatic triangle, and 5-regularity
     of each allowed color at each vertex. Since (a) shows these constraints
     are implied, no 4-color example exists. 3-color examples exist (K_16
     seed), and fewer than 3 colors is impossible (R_2(3) = 6 <= 16).

Also re-checks the equality-lemma base fact used in (a)'s pedigree:
every locally-2 triangle-free K_5 is globally 2-colored (exhaustive 3^10).

Exit 0 iff every check passes.
"""
import subprocess, sys, os
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- (a) pedigree base case ----------
def base_case():
    edges = list(combinations(range(5), 2))
    for cols in product(range(3), repeat=10):
        if len(set(cols)) < 3:
            continue
        col = dict(zip(edges, cols))
        if any(col[(a, b)] == col[(a, c)] == col[(b, c)]
               for a, b, c in combinations(range(5), 3)):
            continue
        pal = [set() for _ in range(5)]
        for (u, v), c in col.items():
            pal[u].add(c); pal[v].add(c)
        if max(len(p) for p in pal) <= 2:
            return False
    return True

assert base_case(), "base case FAILED"
print("base case OK: every locally-2 triangle-free K_5 is globally 2-colored")

# ---------- (c) profile completeness ----------
profiles = set()
for m in product(range(0, 8, 2), repeat=4):  # even parts 0..6
    if sum(m) == 16 and max(m) <= 6:
        profiles.add(tuple(sorted(m, reverse=True)))
profiles = sorted(profiles, reverse=True)
assert profiles == [(6, 6, 4, 0), (6, 6, 2, 2), (6, 4, 4, 2), (4, 4, 4, 4)], profiles
print(f"profile list complete: {profiles}")

# ---------- (d) compile and run exhaustive refuter ----------
src = os.path.join(HERE, "experiments", "rigidity_bt.c")
binp = os.path.join(HERE, "experiments", "rigidity_bt_verify")
subprocess.run(["gcc", "-O3", "-o", binp, src], check=True)
for prof in profiles:
    r = subprocess.run([binp] + [str(x) for x in prof],
                       capture_output=True, text=True)
    out = r.stdout.strip()
    assert r.returncode == 0 and out.startswith("REFUTED"), (prof, out)
    print(f"profile {prof}: {out}")

print("THEOREM VERIFIED: no triangle-free locally-3 K_16 uses 4 global colors")
sys.exit(0)
