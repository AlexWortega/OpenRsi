# Question: does the CAPPED tangent-majorant proof of Lemma A' close?
# Setting: h >= 0 concave on [-1,b], b<=3 (Minkowski centroid), h(0)=1, h <= 4/3
# (Fradelizi), int t h^2 dt = 0. For any supergradient c of h at 0: h <= min(1+ct, 4/3)_+ =: g_c.
# For any lambda with 1 - lambda t >= 0 on [-1,3]:
#   I = int h^2 (1 - lambda t) dt <= int g_c^2 (1 - lambda t) dt =: F(c, lambda).
# Check: sup_c min_{lambda in [-1, 1/3]} F(c,lambda) <= 64/27 ?
import numpy as np

def F(c, lam, N=200001):
    ts = np.linspace(-1.0, 3.0, N)
    g = np.minimum(1.0 + c*ts, 4.0/3.0)
    g = np.maximum(g, 0.0)
    w = 1.0 - lam*ts
    assert w.min() >= -1e-12
    return np.trapz(g*g*w, ts)

def minF(c):
    # F linear in lam: F = A - lam*B
    A = F(c, 0.0); B = A - F(c, 1.0/3.0)  # F(1/3) = A - (1/3)B -> B = 3(A - F(1/3))
    B = 3.0*(A - F(c, 1.0/3.0))
    if B > 0: return A - (1.0/3.0)*B, 1.0/3.0
    else: return A + B*1.0, -1.0   # lam = -1
    
worst = -1; wc=None
for c in np.linspace(-3, 8, 4401):
    v, lam = minF(c)
    if v > worst: worst, wc = v, (c, lam)
print(f"sup_c min_lam F = {worst:.6f} at c={wc[0]:.4f} (lam*={wc[1]:.3f}); 64/27 = {64/27:.6f}")
print("CLOSES" if worst <= 64/27 + 1e-4 else "does NOT close")
# print profile of min_lam F vs c near optimum
for c in np.linspace(wc[0]-0.3, wc[0]+0.3, 13):
    print(f"  c={c:+.4f}  minF={minF(c)[0]:.6f}")
