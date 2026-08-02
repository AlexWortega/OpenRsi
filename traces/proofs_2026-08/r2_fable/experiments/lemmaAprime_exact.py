# Question (Lemma A'): h >= 0 concave on [-1, b], f = h^2, with barycenter int t f dt = 0.
# Is int f <= (64/27) f(0)?  Extremal profiles are piecewise linear with <= 2 kinks
# (standard for such variational problems); we do a dense structured search over
# 2-piece and 3-piece concave h, solving the barycenter constraint exactly per shape.
# Cone h = 3 - t on [-1, 3] gives ratio exactly 64/27.
import numpy as np
from itertools import product

TGT = 64/27

def ratio_from_h(tknots, hknots, NS=20001):
    ts = np.linspace(tknots[0], tknots[-1], NS)
    hs = np.interp(ts, tknots, hknots)
    f = hs**2
    I = np.trapz(f, ts); It = np.trapz(ts*f, ts)
    h0 = np.interp(0.0, tknots, hknots)
    return I, It, h0*h0

best = 0.0; bestcfg=None
# 3-piece concave h on [-1, b]: knots at -1 < t1 < t2 < b, values h(-1)=hA, h(t1)=h1, h(t2)=h2, h(b)=hB
# concavity: slopes decreasing. Search coarse grid, then refine barycenter via scaling asymmetry:
# instead we scan shapes and *solve* for b so that barycenter = 0 (monotone in b typically).
rng = np.random.default_rng(0)

def bary_of(tk, hk):
    I, It, f0 = ratio_from_h(tk, hk)
    return It, I, f0

def try_shape(hA, h1, h2, hB, u1, u2):
    # knots positions: t = -1, then interior at fractions u1<u2 of [ -1, b ]
    # solve for b in (0.01, 10) making It = 0 by bisection (It increasing in b if mass moves right)
    def g(b):
        tk = np.array([-1.0, -1.0+u1*(b+1), -1.0+u2*(b+1), b])
        hk = np.array([hA, h1, h2, hB])
        # concavity check
        sl = np.diff(hk)/np.diff(tk)
        if not (sl[0] >= sl[1] - 1e-12 >= sl[2] - 2e-12): return None
        It, I, f0 = bary_of(tk, hk)
        return It, I, f0, tk, hk
    lo, hi = 0.02, 12.0
    glo = g(lo); ghi = g(hi)
    if glo is None or ghi is None: return None
    if glo[0] * ghi[0] > 0: return None
    for _ in range(60):
        mid = 0.5*(lo+hi)
        gm = g(mid)
        if gm is None: return None
        if glo[0]*gm[0] <= 0: hi = mid
        else: lo, glo = mid, gm
    gm = g(0.5*(lo+hi))
    if gm is None: return None
    It, I, f0, tk, hk = gm
    if f0 < 1e-12: return None
    if abs(It) > 1e-6 * max(I,1e-9): return None
    return I/f0, tk, hk

count=0
for trial in range(200000):
    hA, h1, h2, hB = rng.uniform(0, 2, 4)
    u1 = rng.uniform(0.05, 0.6); u2 = rng.uniform(u1+0.05, 0.95)
    r = try_shape(hA, h1, h2, hB, u1, u2)
    if r is None: continue
    count += 1
    val, tk, hk = r
    if val > best:
        best = val; bestcfg = (tk.copy(), hk.copy())
        print(f"trial {trial}: ratio={val:.6f} (target {TGT:.6f}) tk={np.round(tk,4)} hk={np.round(hk,4)}", flush=True)
print(f"valid shapes: {count}; BEST {best:.8f} vs 64/27={TGT:.8f}")
