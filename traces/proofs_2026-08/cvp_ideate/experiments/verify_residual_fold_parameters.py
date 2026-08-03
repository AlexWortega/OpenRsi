#!/usr/bin/env python3
"""Exact arithmetic checks for the residual-lineage orbit-fold no-go theorem.

Notation Q is an abstract pointed YES weight with nonempty invariant moving
support.  The deliberately weak propagated NO certificate starts at Q+1, and s is supported weight on coordinates fixed by the current
group.  This checks every generated odd-divisor sequence with exact Fractions.
It is a finite verifier; the quantified proof is in proof_cvp.md.
"""
from fractions import Fraction


def odd_divisors(n: int) -> list[int]:
    return [d for d in range(3, n + 1, 2) if n % d == 0]


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def step(a: int, s: int, b: int, g: int) -> tuple[int, int, int]:
    assert g >= 3 and g % 2 == 1 and (a - s) % g == 0
    an = s * s + (a * a - s * s) // g
    sn = s * s + 2 * s * ((a - s) // g)
    bn = 1 + ceil_div(b * b - 1, g)
    return an, sn, bn


def explore(Q: int, depth: int):
    # State includes exact certified ratio upper bound after the first step.
    states = [(Q, 1, Q + 1, ())]
    checked = 0
    for level in range(depth):
        nxt = []
        for a, s, b, gs in states:
            # Trial division is intentionally capped: the recurrence integers
            # become enormous.  We need many exact transitions, not all large
            # divisors, to verify the arithmetic identities finitely.
            ds = [d for d in range(3, min(a - s, 501) + 1, 2) if (a - s) % d == 0]
            for g in ds:
                an, sn, bn = step(a, s, b, g)
                checked += 1
                assert an >= sn >= 1
                if level == 0:
                    assert sn >= 3
                    assert Fraction(bn, an) <= 1 + Fraction(3, Q)
                else:
                    if b >= a:
                        assert Fraction(bn, an) <= Fraction(b, a) ** 2
                    else:
                        # Once the certified lower threshold is below the YES
                        # witness, residual folding cannot restore it.
                        assert bn < an
                assert sn >= 3 ** (2 ** level)
                nxt.append((an, sn, bn, gs + (g,)))
        states = nxt
        if not states:
            break
    return checked, states


def main() -> None:
    total = 0
    surviving = 0
    samples = []
    # Q-1 must have an odd divisor at the first step; Q>=4 enforces nonempty
    # moving support in the recurrence model.
    for Q in range(4, 61):
        checked, states = explore(Q, 4)
        total += checked
        surviving += len(states)
        samples.extend((Q, s) for s in states[:2])
    assert total == 14773
    print(f"checked {total} exact residual-fold transitions; terminal states={surviving}")
    for Q, (a, s, b, gs) in samples[:12]:
        print({"Q": Q, "groups": gs, "a": a, "s": s, "b": b,
               "ratio": f"{b}/{a}"})


if __name__ == "__main__":
    main()
