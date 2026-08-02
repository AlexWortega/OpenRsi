#!/usr/bin/env python3
"""Verify an explicit monochromatic line in the retracted 13-color block rule."""
import json

classes = [set(x) for x in json.load(open("experiments/f2_7_5.json"))]
color = {x: i + 1 for i, part in enumerate(classes) for x in part}

def state(x):
    return 0 if x == 0 else color[x]

data = json.load(open("experiments/invalid/block_power_3_13.json"))
rule = {tuple(map(int, key.split(","))): value for key, value in data["mapping"].items()}

def rule_color(x):
    s = tuple(state((x >> (7 * j)) & 127) for j in range(3))
    assert any(s)
    return rule[s]

x, y = 16384, 196608
z = x ^ y
assert len({x, y, z}) == 3 and all(v != 0 for v in (x, y, z))
assert (rule_color(x), rule_color(y), rule_color(z)) == (9, 9, 9)
print("verified retraction witness: distinct projective line", (x, y, z), "has color 9")
