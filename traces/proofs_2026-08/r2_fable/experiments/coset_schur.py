# Question: for the k-coloring of Z_p^* by cosets of the index-k multiplicative subgroup
# (p ≡ 1 mod 2k so that -1 is in the subgroup => classes symmetric), is the coloring
# sum-free per class (no x+y=z monochromatic)? If yes for p ~ growing p^(1/k), that is a
# correlated algebraic family with growing per-color base => superexponential R_k(3).
# Scan k, and for each k find all p < LIMIT with k | (p-1)/2 whose coset coloring works;
# report max p and base p^(1/k).
import sys
from sympy import isprime, primitive_root

def coset_ok(p, k):
    g = primitive_root(p)
    # class of x = discrete log mod k; build log table
    log = [0]*p
    cur = 1
    for e in range(p-1):
        log[cur] = e % k
        cur = (cur*g) % p
    # -1 symmetric: -1 = g^((p-1)/2); class = ((p-1)/2) % k must be 0 for S=-S per class?
    # Actually classes are cosets; x and -x same class iff (p-1)/2 ≡ 0 mod k.
    if ((p-1)//2) % k != 0:
        return None
    # check no monochromatic x+y=z (x,y,z all nonzero, same class)
    for x in range(1, p):
        cx = log[x]
        for y in range(x, p):
            if log[y] != cx: continue
            z = (x+y) % p
            if z != 0 and log[z] == cx:
                return False
    return True

if __name__ == "__main__":
    kmin = int(sys.argv[1]) if len(sys.argv)>1 else 2
    kmax = int(sys.argv[2]) if len(sys.argv)>2 else 8
    LIMIT = int(sys.argv[3]) if len(sys.argv)>3 else 4000
    for k in range(kmin, kmax+1):
        best = None
        p = 2*k+1
        while p < LIMIT:
            if isprime(p) and (p-1) % (2*k) == 0:
                r = coset_ok(p, k)
                if r:
                    best = p
                    print(f"k={k} p={p} OK  base={p**(1.0/k):.4f}", flush=True)
            p += 2
        print(f"k={k}: max good p = {best}  base={None if best is None else round(best**(1.0/k),4)}", flush=True)
