#!/usr/bin/env python3
"""Independent verifier for symmetric sum-free k-partitions of Z_n \\ {0}
(JSON files with fields n, k, classes = list of k lists of residues).

Checks from scratch:
  1. classes partition {1,...,n-1};
  2. each class S is symmetric: x in S => n-x in S;
  3. each class is sum-free mod n INCLUDING equal summands:
     no a,b in S (a=b allowed) with (a+b) mod n in S.
Then the difference coloring col({x,y}) = class of (x-y mod n) is a
well-defined triangle-free k-coloring of K_n, so R_k(3) >= n+1 and the
per-color base is n^{1/k}.

Usage: verify_cyclic_partition.py file.json [...]   exit 0 iff all pass
"""
import sys, json

def check(fn):
    with open(fn) as f:
        d = json.load(f)
    n, k, classes = d.get("n", d.get("p")), d["k"], d["classes"]
    assert len(classes) == k
    seen = {}
    for c, cl in enumerate(classes):
        for x in cl:
            assert 1 <= x <= n - 1, (fn, x)
            assert x not in seen, (fn, "dup", x)
            seen[x] = c
    assert len(seen) == n - 1, (fn, "not a partition")
    for x, c in seen.items():
        assert seen[n - x] == c, (fn, "not symmetric", x)
    npair = 0
    for c, cl in enumerate(classes):
        s = set(cl)
        for a in cl:
            for b in cl:
                if b < a:
                    continue
                z = (a + b) % n
                npair += 1
                assert z == 0 or z not in s, (fn, "mono triple", a, b, z, c)
    base = n ** (1 / k)
    print(f"{fn}: n={n} k={k} sizes={[len(c) for c in classes]} pairs={npair} "
          f"OK => R_{k}(3) >= {n+1}, base={base:.5f}")
    return n, k

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: verify_cyclic_partition.py f.json ...")
        sys.exit(2)
    for fn in sys.argv[1:]:
        check(fn)
    print("ALL OK")
    sys.exit(0)
