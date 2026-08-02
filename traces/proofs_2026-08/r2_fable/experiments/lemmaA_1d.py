# Question: is it true that for f>=0 on [-a,b], f^{1/2} concave, int t f(t) dt = 0,
# we have int f <= (64/27) f(0)?  (cone profile f=(3-t)^2 on [-1,3] gives equality).
# Numerical adversarial search over piecewise-linear concave g (f=g^2) profiles.
import numpy as np
from scipy.optimize import minimize, linprog

rng = np.random.default_rng(0)
TGT = 64/27

def eval_profile(knots_t, knots_g):
    """g piecewise linear concave through (t_i, g_i), f = g^2 clipped at 0.
    Return (int f, int t f, f(0))."""
    t = np.asarray(knots_t); g = np.asarray(knots_g)
    ts = np.linspace(t[0], t[-1], 20001)
    gs = np.interp(ts, t, g)
    gs = np.maximum(gs, 0.0)
    f = gs**2
    I = np.trapz(f, ts); It = np.trapz(ts*f, ts)
    f0 = np.interp(0.0, t, g)**2 if t[0] <= 0 <= t[-1] else 0.0
    return I, It, f0

def objective(x, m):
    # x: [t0, dt1..dtm (positive increments), g0..gm]
    t0 = x[0]; dts = np.abs(x[1:m+1]) + 1e-4
    t = np.concatenate([[t0], t0 + np.cumsum(dts)])
    g = x[m+1:]
    # enforce concavity of g by projection penalty
    pen = 0.0
    for i in range(1, m):
        s1 = (g[i]-g[i-1])/(t[i]-t[i-1]); s2 = (g[i+1]-g[i])/(t[i+1]-t[i])
        if s2 > s1: pen += (s2-s1)**2
    if not (t[0] < 0 < t[-1]): pen += 10 + abs(t[0]) + abs(t[-1])
    I, It, f0 = eval_profile(t, g)
    if f0 <= 1e-9 or I <= 1e-9: return 1e6
    pen += (It/I)**2 * 100  # barycenter at 0
    return -(I/f0) + 1e4*pen

best = 0.0
for trial in range(300):
    m = rng.integers(2, 6)
    x0 = np.concatenate([[-rng.uniform(0.3,3)], rng.uniform(0.2, 2, m), rng.uniform(0.1, 2, m+1)])
    res = minimize(objective, x0, method="Nelder-Mead", options={"maxiter":8000, "fatol":1e-10})
    x = res.x
    t0 = x[0]; dts = np.abs(x[1:m+1]) + 1e-4
    t = np.concatenate([[t0], t0+np.cumsum(dts)]); g = x[m+1:]
    # check concavity & barycenter strictly
    ok = t[0] < 0 < t[-1]
    for i in range(1, m):
        s1 = (g[i]-g[i-1])/(t[i]-t[i-1]); s2 = (g[i+1]-g[i])/(t[i+1]-t[i])
        if s2 > s1 + 1e-6: ok = False
    if not ok: continue
    I, It, f0 = eval_profile(t, g)
    if f0 <= 1e-9 or abs(It/ max(I,1e-9)) > 1e-3: continue
    val = I/f0
    if val > best:
        best = val
        print(f"trial {trial}: ratio={val:.6f} (target {TGT:.6f})  t={np.round(t,3)} g={np.round(g,3)}", flush=True)
print(f"BEST {best:.6f} vs 64/27 = {TGT:.6f}")
