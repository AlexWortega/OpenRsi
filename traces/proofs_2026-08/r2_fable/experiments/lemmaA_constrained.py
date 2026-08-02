# Question: for f>=0 on [-a,b] with sqrt(f) concave, int t f dt = 0, and a <= 1:
# is int f <= (64/27) f(0)?  (cone profile f=(3-t)^2/2 on [-1,3] is the conjectured extremal.)
# Numerical adversarial maximization of int f / f(0) with a <= 1 enforced.
import numpy as np, sys
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
AMAX = float(sys.argv[2]) if len(sys.argv)>2 else 1.0

def ratio(x, m):
    a = AMAX/(1+np.exp(-x[0]))           # a in (0, AMAX)
    b = np.exp(x[1])                      # b > 0
    h = np.abs(x[2:])                     # sqrt(f) values at m+1 equally spaced knots on [-a,b]
    t = np.linspace(-a, b, m+1)
    dt = t[1]-t[0]
    pen = 0.0
    for i in range(1, m):
        d = (h[i+1]-h[i]) - (h[i]-h[i-1])
        if d > 0: pen += d*d
    ts = np.linspace(-a, b, 8001)
    hs = np.interp(ts, t, h); f = hs**2
    I = np.trapz(f, ts); It = np.trapz(ts*f, ts)
    f0 = np.interp(0.0, t, h)**2
    if f0 < 1e-12 or I < 1e-12: return -1e6, None
    pen += (It/I)**2 * 100
    return I/f0 - 1e5*pen, (a, b, t, h, I, It, f0)

best = 0.0
for trial in range(400):
    m = 10
    x0 = np.concatenate([rng.normal(size=2), rng.uniform(0.1, 2, m+1)])
    res = minimize(lambda x: -ratio(x, m)[0], x0, method="Nelder-Mead",
                   options={"maxiter": 30000, "fatol":1e-12, "xatol":1e-10})
    val, info = ratio(res.x, m)
    if info is None: continue
    a, b, t, h, I, It, f0 = info
    if abs(It/I) > 1e-5: continue
    ok = True; dt = t[1]-t[0]
    for i in range(1, m):
        if (h[i+1]-h[i]) > (h[i]-h[i-1]) + 1e-8: ok = False
    if not ok: continue
    r = I/f0
    if r > best:
        best = r
        print(f"trial {trial}: ratio={r:.6f} (target {64/27:.6f}) a={a:.4f} b={b:.4f}", flush=True)
        if r > 64/27 + 1e-4:
            print("  h knots:", np.round(h, 4))
print(f"BEST {best:.6f} vs 64/27={64/27:.6f}  (AMAX={AMAX})")
