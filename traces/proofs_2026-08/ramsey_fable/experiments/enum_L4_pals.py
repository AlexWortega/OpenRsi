#!/usr/bin/env python3
"""Enumerate palette systems (pal_0..pal_3) for the structured L_4=65 SAT,
up to symmetry, with necessary feasibility filters. Prints one line per case.

Facts used (all proved):
 - pal_i is a 3-set of colors != i (class C_i's internal colors);
 - P_i = pal_i u {i};
 - CROSS CAPACITY for class color i: vertex u in C_i needs exactly 15 cross
   edges colored i; edges to C_j can be colored i only if i in P_j (and i in
   P_i always). Capacity = 16 * #{j != i : i in P_j} >= 15 => some j != i has
   i in pal_j.
 - CROSS CAPACITY for c in pal_i: 11 <= 16 * #{j != i : c in P_j}.
   => every c in pal_i belongs to some P_j, j != i.
 - Consequence: every used color occurs in at least two of the P_i. Colors
   4..15 only exist inside pal's, so each extra color is in >= 2 palettes.
   Total palette slots = 16; classes contribute {0,1,2,3} with multiplicity
   >= 2 each... (0 appears in P_0 and >= 1 other) so slots for extras
   <= 16 - 8 = 8, and each extra takes >= 2 slots => at most 4 extra colors.
   Color universe subset of {0,..,7} WLOG.
Symmetry: permutations of classes 0..3 (acting on colors 0..3 simultaneously)
and of extra colors 4..7.
"""
import itertools, sys

def canon(pals):
    best = None
    for perm in itertools.permutations(range(4)):
        # class relabel: class i -> perm[i]; color c<4 -> perm[c]; extras get canonical rename
        newp = [None] * 4
        for i in range(4):
            newp[perm[i]] = [perm[c] if c < 4 else c for c in pals[i]]
        # rename extras in order of first appearance
        mapping = {}
        nxt = 4
        flat = []
        for i in range(4):
            for c in sorted(newp[i]):
                flat.append((i, c))
        out = [set() for _ in range(4)]
        for i in range(4):
            for c in sorted(newp[i]):
                if c < 4:
                    out[i].add(c)
                else:
                    if c not in mapping:
                        mapping[c] = nxt
                        nxt += 1
                    out[i].add(mapping[c])
        key = tuple(tuple(sorted(s)) for s in out)
        if best is None or key < best:
            best = key
    return best

seen = set()
colors = list(range(8))
cases = []
for pal0 in itertools.combinations([c for c in colors if c != 0], 3):
    for pal1 in itertools.combinations([c for c in colors if c != 1], 3):
        for pal2 in itertools.combinations([c for c in colors if c != 2], 3):
            for pal3 in itertools.combinations([c for c in colors if c != 3], 3):
                pals = [pal0, pal1, pal2, pal3]
                P = [set(p) | {i} for i, p in enumerate(pals)]
                # class-color capacity: i in pal_j for some j != i
                if any(not any(i in P[j] for j in range(4) if j != i) for i in range(4)):
                    continue
                # internal-color capacity
                ok = True
                for i in range(4):
                    for c in pals[i]:
                        if not any(c in P[j] for j in range(4) if j != i):
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    continue
                # pairwise intersect (cross edges need a color)
                if any(not (P[i] & P[j]) for i, j in itertools.combinations(range(4), 2)):
                    continue
                key = canon(pals)
                if key in seen:
                    continue
                seen.add(key)
                cases.append(key)
for key in sorted(cases):
    print(" ".join(",".join(map(str, p)) for p in key))
print(f"# total {len(cases)}", file=sys.stderr)
