#!/usr/bin/env python3
"""Independently regenerate the corrected 3-block coarse-state constraints."""
import itertools, json

classes = json.load(open("experiments/f2_7_5.json"))
base = {x: i + 1 for i, part in enumerate(classes) for x in part}
def state(x): return 0 if x == 0 else base[x]
R = {(state(x), state(y), state(x ^ y)) for x in range(128) for y in range(128)}
states = [s for s in itertools.product(range(6), repeat=3) if any(s)]
index = {s: i for i, s in enumerate(states)}
constraints = set()
for rels in itertools.product(R, repeat=3):
    ss = tuple(tuple(rels[j][h] for j in range(3)) for h in range(3))
    if all(any(s) for s in ss):
        u = tuple(sorted({index[s] for s in ss}))
        if len(u) >= 2:
            constraints.add(u)
stored = json.load(open("experiments/block_power_constraints_t3.json"))
assert stored["t"] == 3 and stored["states"] == [list(s) for s in states]
assert {tuple(u) for u in stored["constraints"]} == constraints
sizes = {d: sum(len(u) == d for u in constraints) for d in (2, 3)}
assert len(R) == 136 and len(states) == 215 and sizes == {2: 12730, 3: 410455}
print("verified corrected block hypergraph:", len(states), "states,", sizes)
