# Question: verify the exact equality chain at the sharp simplex S = 4conv{0,e_i} - 1:
#   for ell = e_3: f(t)=area of slice; f(t) = (1/2)(3-t)^2 on [-1,3];
#   barycenter of f dt is 0; f(0)=9/2; max f = f(-1) = 8 = (16/9) f(0)  [Fradelizi equality];
#   vol = int f = 32/3 = (64/27) f(0)  [cone-profile equality];
#   lattice width in e_3 is 4.
# Also verify the rigorous conditional theorem constants: if some primitive ell has
# lattice width w and central section lattice-area A0, then vol <= (16/9) w A0 (Fradelizi n=3),
# and w<=4/3, A0<=9/2 => vol <= 32/3. Exact sympy checks. Exit 0 = pass.
import sympy as sp

t = sp.symbols('t')
f = sp.Rational(1,2)*(3-t)**2
I = sp.integrate(f, (t, -1, 3))
It = sp.integrate(t*f, (t, -1, 3))
assert I == sp.Rational(32,3), I
assert It == 0, It
f0 = f.subs(t, 0)
assert f0 == sp.Rational(9,2)
fmax = f.subs(t, -1)
assert fmax == 8
assert sp.Rational(16,9)*f0 == fmax           # Fradelizi equality
assert sp.Rational(64,27)*f0 == I             # cone equality
# conditional theorem arithmetic: (16/9)*(4/3)*(9/2) = 32/3
assert sp.Rational(16,9)*sp.Rational(4,3)*sp.Rational(9,2) == sp.Rational(32,3)
# simplex slice area formula check: slice of 4*conv{0,e1,e2,e3}-1 at x3 = t is the triangle
# {x1,x2 >= -1, x1+x2 <= 2-t} (from x1+x2+x3<=1 scaled: original planes x_i>=-1, x1+x2+x3<=1;
# wait sharp simplex: vertices (-1,-1,-1), (3,-1,-1), (-1,3,-1), (-1,-1,3);
# facets: x_i >= -1, x1+x2+x3 <= 1... check vertex sums: -3, 1, 1, 1 -> x1+x2+x3<=1?
# (3,-1,-1) sums 1 yes. Slice at x3=t: x1,x2>=-1, x1+x2 <= 1-t. Right triangle legs (1-t)-(-2)=... 
# leg length L = (1-t) - (-1) - (-1)= (1-t)+2 = 3-t? x1 from -1 to (1-t)-(-1)=2-t, so leg = 3-t. area=(3-t)^2/2. OK
L = (2 - t) - (-1)
assert sp.simplify(L - (3 - t)) == 0
# volume of simplex: (4^3)/6 * vol(conv{0,e_i}) = 64/6 = 32/3
assert sp.Rational(4**3, 6) == sp.Rational(32, 3)
# lattice width in e3: from -1 to 3 -> 4
print("all exact checks pass")
