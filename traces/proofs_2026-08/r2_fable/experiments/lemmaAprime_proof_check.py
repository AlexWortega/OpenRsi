# Question: does the tangent-majorant proof of Lemma A' close?
# Lemma A': h>=0 concave on [-1,b] (1<=b<=3), h(0)=1, int t h^2 dt = 0  =>  int h^2 dt <= 64/27.
# Proof skeleton: pick supergradient c of h at 0, so h(t) <= max(0, 1+ct) on [-1,b], and
# supp h subset T = [-1,b] cap {1+ct>=0}. For ANY lambda with 1-lambda*t >= 0 on [-1,R],
# R = right end of T:  I = int h^2 (1-lambda t) dt  <= int_T (1+ct)^2 (1-lambda t) dt =: F(c,lambda).
# WAIT: this majorization needs (1-lambda t) >= 0 AND h^2 <= (1+ct)^2 -- both pointwise on supp h. OK.
# Need: max over c, b of min over admissible lambda of F <= 64/27.
# F is LINEAR in lambda: F = A - lambda B, A = int_T (1+ct)^2, B = int_T t (1+ct)^2.
# min at lambda = 1/R if B>0, lambda = -1 if B<0 (admissible interval [-1, 1/R], R>0;
# if R<=0... R>=? T contains 0 since h(0)=1>0; R>0 unless b.. R>0 always as 0 in supp).
# This script scans (c,b) densely and reports the sup of min_lambda F.
import numpy as np
import sympy as sp

t, c, lam, R, b, rho = sp.symbols('t c lam R b rho', real=True)

def minF(cv, bv):
    # T = [-1, Rv] where Rv = bv if cv >= -1/bv ... 1+ct >= 0 for t <= -1/c (c<0)
    if cv < 0:
        Rv = min(bv, -1.0/cv)
    else:
        # 1+ct >= 0 on [-1,..] requires t >= -1/c for c>0: at t=-1 need 1-c >= 0, i.e. c<=1;
        # if c > 1, T = [-1/c, b] -- left end moves in; supp h subset T
        Rv = bv
    if cv > 0:
        Lv = max(-1.0, -1.0/cv)
    else:
        Lv = -1.0
    # admissible lambda: 1 - lam*t >= 0 on [Lv, Rv]: lam <= 1/Rv (Rv>0), and lam >= 1/Lv (Lv<0) i.e. lam >= -1/|Lv|
    lam_lo = 1.0/Lv   # Lv<0 so this is negative
    lam_hi = 1.0/Rv
    ts = np.linspace(Lv, Rv, 40001)
    m2 = (1+cv*ts)**2
    A = np.trapz(m2, ts); B = np.trapz(ts*m2, ts)
    # F = A - lam*B minimized over [lam_lo, lam_hi]
    if B > 0: return A - lam_hi*B
    else: return A - lam_lo*B

worst = 0.0; wc = None
for bv in np.linspace(1.0, 3.0, 21):
    for cv in np.concatenate([np.linspace(-5, 5, 2001)]):
        if abs(cv) < 1e-9: cv = 1e-9
        v = minF(cv, bv)
        if v > worst:
            worst = v; wc = (cv, bv)
print(f"sup over (c,b) of min_lambda F = {worst:.6f} at c={wc[0]:.4f}, b={wc[1]:.3f}; target 64/27 = {64/27:.6f}")
print("PROOF CLOSES" if worst <= 64/27 + 1e-6 else "PROOF DOES NOT CLOSE with this multiplier class")
