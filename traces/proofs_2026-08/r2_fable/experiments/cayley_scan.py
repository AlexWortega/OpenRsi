# Question: for small groups G, what is the min number k of symmetric product-free sets
# partitioning G\{1}? (=> triangle-free k-coloring of K_|G| via Cayley; want |G|^(1/k) large.)
# For abelian G written additively: sets S with S=-S and (S+S) cap S = empty on relevant triples.
# Triangle condition for Cayley coloring c(x,y)=class(x-y): need each class S product-free:
# no a,b in S with a-b in S (equivalently a=b+c with a,b,c in S). Also S symmetric (S=-S)
# so that c is well-defined on unordered pairs.
# We scan abelian groups Z_{m1} x ... and ask SAT: partition nonidentity elements into k
# symmetric product-free classes.
import itertools, sys
from pysat.solvers import Cadical195

def group_elems(dims):
    return list(itertools.product(*[range(m) for m in dims]))

def add(x, y, dims):
    return tuple((a+b) % m for a,b,m in zip(x,y,dims))
def neg(x, dims):
    return tuple((-a) % m for a,m in zip(x,dims))

def try_partition(dims, k, timeout_conf=10**7):
    elems = group_elems(dims)
    ident = tuple(0 for _ in dims)
    nonid = [e for e in elems if e != ident]
    # pair up x with -x: they must share a color (S=-S). Use representatives.
    rep = {}
    for e in nonid:
        ne = neg(e, dims)
        r = min(e, ne)
        rep[e] = r
    reps = sorted(set(rep.values()))
    ridx = {r:i for i,r in enumerate(reps)}
    def var(r, c): return ridx[r]*k + c + 1
    clauses = []
    for r in reps:
        clauses.append([var(r,c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1+1,k):
                clauses.append([-var(r,c1), -var(r,c2)])
    # product-free: for a,b in nonid distinct with a+b in nonid: forbid all three same color
    # triple {a, b, a+b} with all nonidentity; condition: no monochromatic solution a+b=c
    seen = set()
    for a in nonid:
        for b in nonid:
            c_ = add(a,b,dims)
            if c_ == ident or c_ == a or c_ == b: continue
            trip = tuple(sorted({rep[a], rep[b], rep[c_]}))
            if trip in seen: continue
            seen.add(trip)
            rs = list(trip)
            for col in range(k):
                clauses.append([-var(r,col) for r in rs])
    # also forbid a+a = b monochromatic (a,2a same class): a + a = c, a==b case
    for a in nonid:
        c_ = add(a,a,dims)
        if c_ != ident and c_ != a:
            for col in range(k):
                cl = list({-var(rep[a],col), -var(rep[c_],col)})
                clauses.append(cl)
    s = Cadical195(bootstrap_with=clauses)
    ok = s.solve()
    if not ok:
        return None
    m = s.get_model()
    col = {}
    for r in reps:
        for c in range(k):
            if m[var(r,c)-1] > 0: col[r] = c
    return {e: col[rep[e]] for e in nonid}

def verify(dims, k, col):
    elems = group_elems(dims); ident = tuple(0 for _ in dims)
    nonid = [e for e in elems if e != ident]
    for a in nonid:
        assert col[a] == col[neg(a,dims)]
        for b in nonid:
            c_ = add(a,b,dims)
            if c_ != ident and c_ != a and c_ != b:
                assert not (col[a]==col[b]==col[c_]), (a,b,c_)
    return True

if __name__ == "__main__":
    # scan groups; for each find min k that works (up to 6)
    groups = []
    # cyclic
    for m in range(3, 130): groups.append((m,))
    # products
    for m1 in range(2, 20):
        for m2 in range(m1, 20):
            if m1*m2 <= 200: groups.append((m1,m2))
    for m1 in range(2,8):
        for m2 in range(m1,8):
            for m3 in range(m2,8):
                if m1*m2*m3 <= 220: groups.append((m1,m2,m3))
    results = []
    for dims in groups:
        n = 1
        for m in dims: n *= m
        best = None
        for k in range(1, 7):
            # quick lower bound skip: need n-1 <= k * (max product-free ~ larger), skip heavy
            colr = try_partition(dims, k)
            if colr is not None:
                verify(dims, k, colr)
                best = k
                break
        if best:
            base = n ** (1.0/best)
            print(f"G={dims} n={n} mink={best} base={base:.4f}", flush=True)
            results.append((base, dims, n, best))
    results.sort(reverse=True)
    print("TOP:")
    for r in results[:15]: print(r)
