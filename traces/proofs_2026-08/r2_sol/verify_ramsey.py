#!/usr/bin/env python3
"""Finite checks used in proof_ramsey.md. Standard library only."""
from itertools import combinations

K16_CLASSES = [
    {1, 2, 4, 8, 15},
    {3, 5, 7, 10, 11},
    {6, 9, 12, 13, 14},
]
K32_CLASSES = [
    {3, 5, 7, 14, 18, 22, 26, 27},
    {9, 11, 12, 13, 23, 25, 29},
    {2, 6, 15, 17, 20, 24, 31},
    {1, 4, 8, 10, 16, 19, 21, 28, 30},
]


def check_partition(classes, d):
    assert set().union(*classes) == set(range(1, 1 << d))
    assert sum(map(len, classes)) == (1 << d) - 1
    assert all((a ^ b) not in part for part in classes for a, b in combinations(part, 2))
    color = {x: i for i, part in enumerate(classes) for x in part}
    count = 0
    for x, y, z in combinations(range(1 << d), 3):
        assert len({color[x ^ y], color[x ^ z], color[y ^ z]}) > 1
        count += 1
    return count


def fixed_layer_nonextension(classes):
    """Exhaust the colorings of the new affine layer over a fixed F_2^5 seed."""
    n, k = 32, len(classes)

    def search(state, nodes):
        """Immutable-state MRV search, avoiding stale assignments on failed branches."""
        nodes[0] += 1
        if len(state) == n:
            return state
        best_y = None
        best_options = None
        for y in range(n):
            if y in state:
                continue
            options = [
                c
                for c in range(k)
                if all(
                    state.get(z) != c or (y ^ z) not in classes[c]
                    for z in range(n)
                )
            ]
            if not options:
                return None
            if best_options is None or len(options) < len(best_options):
                best_y, best_options = y, options
        for c in best_options:
            child = dict(state)
            child[best_y] = c
            result = search(child, nodes)
            if result is not None:
                return result
        return None

    counts = []
    for first_color in range(k):
        nodes = [0]
        assert search({0: first_color}, nodes) is None
        counts.append(nodes[0])
    return counts


def check_ternary_aggregate_witness():
    star = -1
    words = (
        [(star, star, star, star)]
        + [(star, star, 0, 0)] * 16
        + [(star, 1, star, 1)] * 16
        + [(0, 0, 1, star)] * 16
        + [(1, star, star, star)] * 16
    )
    assert len(words) == 65
    for i in range(4):
        assert [sum(w[i] == b for w in words) for b in (0, 1, star)] == [16, 16, 33]
    for i, j in combinations(range(4), 2):
        overlap = [w for w in words if w[i] != star and w[j] != star]
        assert len({w[i] for w in overlap}) <= 1 or len({w[j] for w in overlap}) <= 1


if __name__ == "__main__":
    print("K16 triangles checked:", check_partition(K16_CLASSES, 4))
    print("K32 triangles checked:", check_partition(K32_CLASSES, 5))
    print("fixed-layer failed-search node counts:", fixed_layer_nonextension(K32_CLASSES))
    check_ternary_aggregate_witness()
    print("ternary aggregate witness: OK")
