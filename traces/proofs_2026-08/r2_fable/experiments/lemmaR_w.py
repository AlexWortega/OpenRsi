# Question: compute R(w) = max{ int g / g(0) : sqrt(g) concave >=0 on interval of length w
# containing 0, int t g(t) dt = 0 }. Conjecture from simplex: R(4) >= 64/27 via cone profile;
# slab gives R(w) >= w. Determine R(w) numerically for w in (0,4]; find w* = sup{w: R(w) <= 64/27}.
import numpy as np
from scipy.optimize import minimize

def ratio(params, w, m):
    # support [-a, w-a]; h = sqrt(g) concave piecewise-linear with m+1 knots (equally spaced)
    a = params[0]
    h = np.abs(params[1:])
    if not (1e-4 < a < w - 1e-4): return -1e6, None
    t = np.linspace(-a, w - a, m+1)
    # concavity check -> penalty
    pen = 0.0
    dt = t[1]-t[0]
    for i in range(1, m):
        s1 = (h[i]-h[i-1])/dt; s2 = (h[i+1]-h[i])/dt
        if s2 > s1: pen += (s2 - s1)**2
    ts = np.linspace(-a, w-a, 4001)
    hs = np.interp(ts, t, h); g = hs**2
    I = np.trapz(g, ts); It = np.trapz(ts*g, ts)
    g0 = np.interp(0.0, t, h)**2
    if g0 < 1e-10 or I < 1e-10: return -1e6, None
    pen += (It/I)**2 * 50
    return I/g0 - 1e4*pen, (t, h, I, It, g0)

def R(w, m=8, trials=60, seed=0):
    rng = np.random.default_rng(seed)
    best = 0.0; bestinfo = None
    for _ in range(trials):
        x0 = np.concatenate([[rng.uniform(0.1*w, 0.9*w)], rng.uniform(0.1, 2, m+1)])
        res = minimize(lambda x: -ratio(x, w, m)[0], x0, method="Nelder-Mead",
                       options={"maxiter": 20000, "fatol":1e-12, "xatol":1e-10})
        val, info = ratio(res.x, w, m)
        if info is None: continue
        t, h, I, It, g0 = info
        if abs(It/I) > 1e-4: continue
        # strict concavity check
        ok = True
        dt = t[1]-t[0]
        for i in range(1, m):
            if (h[i+1]-h[i]) > (h[i]-h[i-1]) + 1e-7: ok = False
        if not ok: continue
        if I/g0 > best:
            best = I/g0; bestinfo = (t.copy(), h.copy())
    return best, bestinfo

if __name__ == "__main__":
    print(f"64/27 = {64/27:.6f}")
    for w in [0.5,1.0,1.5,2.0,2.2,2.37,2.5,2.7,3.0,3.5,4.0]:
        r, info = R(w)
        mark = "<=64/27" if r <= 64/27 + 1e-6 else ">64/27 !"
        print(f"w={w:.2f}  R(w)~{r:.6f}  slab={w:.3f}  {mark}", flush=True)
        if info is not None and w in (2.0, 4.0):
            t, h = info
            print("   knots t:", np.round(t,4)); print("   h:", np.round(h,4))
