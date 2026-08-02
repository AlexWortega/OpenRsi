# Question: Lemma A' test. h>=0 concave on [-1,b] (b>=1), int t h^2 dt = 0.
# Is int h^2 dt <= (64/27) h(0)^2 ?  (Cone h = (3-t)/3*h0... equality at b=3, h linear.)
# Scale-invariant form of: min(a,b)=1. Adversarial maximization over piecewise-linear h.
import numpy as np, sys
from scipy.optimize import minimize

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 0)
TGT = 64/27

def ratio(x, m):
    b = 1.0 + np.exp(x[0])*0.001 + abs(x[0])  # b >= 1 roughly; better: b = 1+softplus
    b = 1.0 + np.log1p(np.exp(x[0]))
    h = np.abs(x[1:])
    t = np.linspace(-1.0, b, m+1)
    dt = t[1]-t[0]
    pen = 0.0
    for i in range(1, m):
        d = (h[i+1]-h[i]) - (h[i]-h[i-1])
        if d > 0: pen += d*d
    ts = np.linspace(-1.0, b, 8001)
    hs = np.interp(ts, t, h); f = hs**2
    I = np.trapz(f, ts); It = np.trapz(ts*f, ts)
    f0 = np.interp(0.0, t, h)**2
    if f0 < 1e-12 or I < 1e-12: return -1e6, None
    pen += (It/I)**2 * 100
    return I/f0 - 1e5*pen, (b, t, h, I, It, f0)

best = 0.0
m = 12
for trial in range(2000):
    x0 = np.concatenate([[rng.normal()*2], rng.uniform(0.1, 2, m+1)])
    res = minimize(lambda x: -ratio(x, m)[0], x0, method="Nelder-Mead",
                   options={"maxiter": 40000, "fatol":1e-13, "xatol":1e-11})
    val, info = ratio(res.x, m)
    if info is None: continue
    b, t, h, I, It, f0 = info
    if abs(It/I) > 1e-5: continue
    ok = True
    for i in range(1, m):
        if (h[i+1]-h[i]) > (h[i]-h[i-1]) + 1e-8: ok = False
    if not ok: continue
    r = I/f0
    if r > best:
        best = r
        print(f"trial {trial}: ratio={r:.6f} (target {TGT:.6f}) b={b:.4f}", flush=True)
        if r > TGT + 1e-4:
            print("  VIOLATION h:", np.round(h,4), " t:", np.round(t,4), flush=True)
print(f"BEST {best:.6f} vs {TGT:.6f}")
