# Rigorous structured cases of the Ehrhart volume conjecture

**Proposition.** Let `K ⊂ R^n` be a full-dimensional compact convex body satisfying `K=-K` and `int(K)∩Z^n={0}`. Then

`vol(K) ≤ 2^n ≤ (n+1)^n/n!`.

**Proof.** If `vol(K)>2^n`, Minkowski's convex body theorem, applied to the origin-symmetric convex body `K` and the lattice `Z^n` of determinant one, supplies a nonzero point of `Z^n` in `int(K)`, contrary to the hypothesis. Hence `vol(K)≤2^n`.

By AM–GM,

`(n!)^(1/n) = (1·2···n)^(1/n) ≤ (1+2+···n)/n = (n+1)/2`.

Raising to the `n`th power and rearranging gives `2^n≤(n+1)^n/n!`. ∎

This proves the conjectured inequality for centrally symmetric bodies only; it does not address the essential asymmetric case.

## An elementary all-dimensional proof for lattice-vertex simplices

**Proposition.** Let `S=conv(v_0,...,v_n)` be a full-dimensional simplex with all `v_i in Z^n`, barycenter zero, and `int(S) cap Z^n={0}`. Then

`vol(S)<= (n+1)^n/n!`.

**Proof.** Put `m=n+1`, let `A` be the matrix with columns `v_i-v_0` for `1<=i<=n`, and use coordinates

`x=v_0+A r`.

The simplex interior corresponds exactly to

`Delta^o={r in R^n: r_i>0 for all i, sum_i r_i<1}`.

Consider the finite subgroup

`Lambda=A^{-1}Z^n/Z^n subset R^n/Z^n`.

Its order is `|det A|=n! vol(S)`. Since the simplex barycenter is zero,

`0=v_0+Aq`, where `q=(1/m,...,1/m)`.

Thus `q` represents an element of `Lambda`.

Partition the half-open unit cube `[0,1)^n` into `m^n` half-open cubes of side `1/m`. If `|Lambda|>m^n`, two distinct representatives of elements of `Lambda` lie in the same small cube. Their difference represents a nonzero element of `Lambda` and has a representative `d` satisfying

`-1/m<d_i<1/m` for every `i`.

Replace `d` by `-d` if necessary, so that `sum_i d_i<=0`. Then

`q+d in Delta^o`:

indeed every coordinate is strictly positive, and

`sum_i(q_i+d_i)<=n/m<1`.

Because `q+d` represents an element of `Lambda`, the point

`v_0+A(q+d)=A d`

is a lattice point. It lies in `int(S)`, and it is nonzero because `A` is invertible and `d` is a nonzero torus representative with all coordinates strictly between `-1` and `1`. This contradicts the lattice-freeness hypothesis. Hence `|det A|<=m^n`, and division by `n!` proves the result. ∎

This is an independent elementary proof for the lattice-vertex subclass of the known all-simplex theorem. It does not cover simplices with nonintegral vertices or general convex bodies. The pigeonhole argument also explains why determinant `64` is the exact three-dimensional threshold seen in the searches.

## A planar reduction for the symmetric core of centered pyramids

Let `B subset R^2` have barycenter zero and form the centered pyramid

`P=conv((B,-1),(0,3))`.

At height `z in [-1,1]`, the sections of `P` and `-P` are respectively

`((3-z)/4)B` and `-((3+z)/4)B`.

Consequently Fubini gives the exact reduction

`vol(P cap -P)=integral_{-1}^1 area(((3-z)/4)B cap -((3+z)/4)B) dz`.

For a triangular base this ratio can be derived exactly. Let `lambda_1,lambda_2,lambda_3` be its barycentric coordinates, normalized so `lambda_i(0)=1/3`. Put `u=(3-z)/4` and `v=(3+z)/4`. The condition `x in uB` is

`lambda_i(x)>=(1-u)/3=(1+z)/12`,

while `x in -vB` is

`lambda_i(x)<=(1+v)/3=(7+z)/12`.

After translating all three barycentric coordinates by the lower bound, the available simplex has side-scale `u`, and each of its three corners beyond coordinate `1/2` is deleted. These corner triangles are disjoint for `u<=1`. Since planar simplex area scales quadratically, the normalized intersection area is

`u^2-3(u-1/2)^2=(3-z^2)/8`.

(The endpoint `u=1/2` is included by continuity.) Its integral over `[-1,1]` is `2/3`, while `vol(P)=4 area(B)/3`, so every centered tetrahedron has symmetric-core ratio `1/2`.

This identifies a possible extension but **not a proved lemma**: if the displayed triangular section ratio were a universal lower bound for all centroid-zero planar `B`, then every centered three-dimensional pyramid would satisfy `vol(P cap -P)>=vol(P)/2`, and lattice-freeness plus Minkowski would give `vol(P)<=16`. The universal planar intersection inequality remains open in this work; `verify_triangle_scaled_intersection.py` checks only the triangular algebra.

## A finite integer-tetrahedron benchmark

A complete exact enumeration gives a small computational benchmark for the sharp asymmetric geometry. Among all nondegenerate tetrahedra whose four vertices are integer points in `[-1,3]^3` and whose barycenter is zero, exactly 1,078 have no nonzero interior lattice point. Their volumes are at most `32/3`, with a unique maximizer as an ordered vertex set:

`(-1,-1,-1), (-1,-1,3), (-1,3,-1), (3,-1,-1)`.

For a tetrahedron the barycenter is the average of its vertices, so the enumeration generates three vertices and fixes the fourth as their negative sum. It computes six times volume by an exact integer determinant. Strict interior membership is tested by the signs of the four exact barycentric determinant numerators, over every integer point in the coordinate bounding box. The independent script `verify_integer_tetrahedra_box.py` repeats this exhaustive enumeration and checks the count, maximum, and uniqueness.

A second enumeration over the larger box `[-2,4]^3` finds 135,534 centroid-zero candidate quadruples after ordering, of which 26,928 are nondegenerate and interior-lattice-free. Again the maximum determinant is 64 (volume `32/3`); there are 19 coordinate representatives at equality. For every one, the three edge vectors from a vertex are all divisible by four and their determinant has absolute value 64, so after division by four they form a unimodular basis. Thus each equality tetrahedron in this box is a unimodular image of the sharp simplex (with a corresponding lattice translation already fixed by barycenter zero). `verify_integer_tetrahedra_box_2_4.py` repeats these checks exactly.

These are only finite boxed statements about integer-vertex tetrahedra. They do not cover rational or real tetrahedra, arbitrary coordinate boxes, general polytopes, or arbitrary convex bodies, so they do not prove a new unrestricted case of the conjecture.

## A controlled-asymmetry extension

The same argument gives a slightly larger, genuinely asymmetric class.

**Proposition.** Under the lattice-freeness hypotheses of the conjecture, suppose additionally that for some `rho>=1`,

`K subset -rho K`.

Then `vol(K)<= (2rho)^n`. Consequently, the conjectured bound holds whenever

`rho <= (n+1)/(2(n!)^(1/n))`.

**Proof.** Barycenter zero lies in the interior of the full-dimensional convex body `K`, so convexity gives `(1/rho)K subset K`. Dividing the assumed inclusion `K subset -rho K` by the positive scalar `rho` gives `(1/rho)K subset -K`. Hence the origin-symmetric convex body

`C=K cap (-K)`

contains `(1/rho)K`. Moreover `int(C) subset int(K)`, so `int(C) cap Z^n={0}`. Minkowski's theorem therefore gives `vol(C)<=2^n`, while

`rho^{-n} vol(K)=vol((1/rho)K)<=vol(C)`.

Thus `vol(K)<= (2rho)^n`. This is at most `(n+1)^n/n!` exactly under the displayed condition on `rho`. ∎

For `rho=1` this recovers the symmetric case. The threshold tends to `e/2` as `n` grows, so the statement permits a bounded but limited amount of asymmetry. It does not apply to arbitrary centroid-zero bodies, whose Minkowski asymmetry can be as large as `n` (simplices attain that scale).

## Lattice-aligned centered pyramids (an inductive lifting lemma)

The preceding asymmetry criterion does not cover simplicial-scale asymmetry. A lattice-aligned pyramid can instead be reduced to one lower dimension, without any symmetry assumption on its base.

**Proposition.** Let `n>=2`, let `B subset R^{n-1}` be any full-dimensional compact convex body with barycenter zero, and let `a>0`. Define

`K=conv((B,-a), (0,na)) subset R^{n-1} times R`.

Assume `int(K) cap Z^n={0}` and assume the Ehrhart conjecture is valid in dimension `n-1`. Then

`vol_n(K) <= (n+1)^n/(n n!)`,

which is a factor `n` stronger than the conjectured bound in dimension `n`.

**Proof.** A pyramid's centroid lies on the segment from its base centroid to its apex, at height `1/(n+1)` of the total altitude above the base. Thus the displayed choice of heights makes the barycenter of `K` equal to zero.

The open axial segment from `(0,-a)` to `(0,na)` lies in `int(K)`. If `na>1`, it contains the nonzero lattice point `(0,1)`, contrary to the hypothesis. Hence `a<=1/n`, so the altitude `H=(n+1)a` is at most `(n+1)/n`.

The horizontal section at height zero is

`C times {0}`, where `C=(n/(n+1))B`.

Every point of `int_{R^{n-1}}(C) times {0}` lies in `int(K)`. Therefore `int(C) cap Z^{n-1}={0}`. The body `C` is full-dimensional and has barycenter zero, so the conjectured `(n-1)`-dimensional bound gives

`vol_{n-1}(C) <= n^{n-1}/(n-1)!`.

Consequently

`vol_{n-1}(B) = ((n+1)/n)^{n-1} vol_{n-1}(C) <= (n+1)^{n-1}/(n-1)!`.

Using the pyramid volume formula now yields

`vol_n(K)=H vol_{n-1}(B)/n <= (n+1)^n/(n^2 (n-1)!) = (n+1)^n/(n n!)`.

This proves the claim. ∎

**Unconditional consequences.** Since the conjecture is known in dimensions one and two, the proposition proves it for every such lattice-aligned centered pyramid in dimensions two and three, with the stronger factor-`n` estimate. If the base is centrally symmetric, Minkowski can replace the inductive hypothesis in every dimension and gives the earlier bound `2^{n-1}(n+1)^n/n^{n+1}`.

The lattice alignment is crucial: the axial obstruction used the lattice point `(0,1)`. This is not a proof for arbitrary orientations or arbitrary pyramids.

## A central-section lifting criterion

The pyramid argument suggests a broader reduction. A log-concavity observation removes both homothety and the earlier assumption that the central section has maximal volume.

**Lemma (log-concave mean-value bound).** Let `f` be an integrable log-concave function, positive on the interior of a bounded interval `I`, and suppose

`integral_I t f(t)dt / integral_I f(t)dt = m`.

Then

`integral_I f(t)dt <= |I| f(m)`.

**Proof.** Put `Z=integral_I f` and let `p=f/Z` be the corresponding probability density. Jensen's inequality for the concave function `log f` gives

`log f(m) >= integral_I p log f`.

On the other hand, nonnegativity of relative entropy with respect to the uniform probability density `1/|I|` gives

`0 <= integral_I p log(p|I|) = integral_I p log f - log Z + log |I|`.

Hence `integral p log f >= log(Z/|I|)`. Combining this with Jensen yields `log f(m)>=log(Z/|I|)`. Exponentiation proves the claim. Values at zero endpoints are harmless; equivalently one may apply the argument on the essential support and use the standard extended-value convention for `log f`.

Equality holds only when `f` is constant almost everywhere on `I`. Indeed equality requires equality in the relative-entropy inequality, so the probability density `p=f/Z` equals the uniform density almost everywhere. Conversely a constant function gives equality. ∎

**Proposition (general section lifting).** Let `K subset R^{n-1} times R` satisfy the hypotheses of the Ehrhart conjecture. Write its horizontal sections as `K_t={x:(x,t) in K}`, and assume:

1. the projection interval is `[alpha,beta]`, with `alpha<0<beta`;
2. `(0,t) in int(K)` for every `alpha<t<beta`; and
3. the central section `K_0` has barycenter zero.

If the Ehrhart conjecture holds in dimension `n-1`, then it holds for `K`.

**Proof.** Let `f(t)=vol_{n-1}(K_t)`. By the Brunn--Minkowski theorem, `f(t)^{1/(n-1)}` is concave on the projection interval; hence `f` is log-concave on its positive interior. The vertical coordinate of the barycenter of `K` is zero, so

`integral_alpha^beta t f(t)dt=0`.

Thus zero is the mean of the density proportional to `f`, and the log-concave mean-value lemma gives

`vol_n(K)=integral_alpha^beta f(t)dt <=(beta-alpha)f(0)`.

Condition 2 and lattice-freeness imply `alpha>=-1` and `beta<=1`, hence `beta-alpha<=2`. Moreover `int(K_0) times {0} subset int(K)`, so the central section is lattice-free in `Z^{n-1}`. It is full-dimensional and has barycenter zero by condition 3; the lower-dimensional conjecture gives `f(0)<=A_{n-1}`. Therefore

`vol_n(K)<=2A_{n-1}<=A_n`.

This proves the claim. If equality holds in the analytic estimate `vol_n(K)<=(beta-alpha)vol_{n-1}(K_0)`, then the section-volume function is constant almost everywhere. By continuity of section volumes on the interior, it is constant throughout `(alpha,beta)`.

In fact the interior fibers are translates of one another. Convexity gives

`(1-lambda)K_s+lambda K_t subset K_{(1-lambda)s+lambda t}`.

All three bodies have the same positive volume. Brunn--Minkowski says the left Minkowski combination has volume at least that common volume, while inclusion gives at most that volume; hence equality holds. The equality case of Brunn--Minkowski implies `K_s` and `K_t` are homothetic, and equal volume makes the homothety ratio one, so they are translates.

Their barycenters `c(t)` therefore determine the translations. Applying the displayed inclusion and comparing equal-volume translates shows

`c((1-lambda)s+lambda t)=(1-lambda)c(s)+lambda c(t)`.

Thus `c(t)=vt+w` is affine. Since the section-volume density is constant, the vertical barycenter equation first forces `alpha+beta=0`. The horizontal barycenter equation then forces `w=c(0)=0`. Hence `K_t=K_0+vt` on the interior after anchoring at `t=0`. Consequently equality in the analytic estimate makes `K` an affine shear of a cylinder, up to endpoint fibers of measure zero. If the shear slope `v` is integral, a unimodular shear turns it into an actual lattice-aligned cylinder; if `v` is nonintegral, this geometric normalization does not preserve the lattice. This rigidity statement uses the standard equality case of Brunn--Minkowski. ∎

This criterion is unconditional in dimension three. It allows sections to change shape arbitrarily; its restrictive assumptions are the primitive lattice-aligned interior chord and the barycentric centering of the section through the origin.

The resulting estimate is strictly stronger than the conjectured constant for every `n>=2`, because

`2A_{n-1}<A_n`

(the ratio is `(1+1/n)^n>2`). Quantitatively,

`2A_{n-1}/A_n = 2/(1+1/n)^n -> 2/e`.

Hence the one-step lifting theorem saves an asymptotic factor `e/2` relative to the conjectured constant, and none of these classes can contain an equality body. This is consistent with the sharp simplex, which fails the directional certificate badly.

The central fiber need not be barycentrically centered if it has controlled asymmetry about the lattice point zero.

**Corollary (central-section origin-asymmetry).** Retain conditions 1 and 2 of the general section-lifting proposition, but replace condition 3 by

`K_0 subset -rho K_0`

for some `rho>=1`. Then

`vol_n(K)<=2(2rho)^{n-1}`.

Consequently the Ehrhart conjectured bound holds whenever

`rho <= (A_n/2^n)^{1/(n-1)}`.

**Proof.** The log-concave mean-value argument and the interior axial chord give

`vol_n(K)<=2vol_{n-1}(K_0)`

without using the barycenter of `K_0`. Condition 2 puts zero in `int(K)`, so the body `K_0` contains zero in its relative interior and is lattice-free there. Its symmetric core

`D=K_0 cap (-K_0)`

contains `(1/rho)K_0`: convexity and `0 in K_0` give `(1/rho)K_0 subset K_0`, while the assumed inclusion gives `(1/rho)K_0 subset -K_0`. Minkowski in dimension `n-1` gives `vol(D)<=2^{n-1}`. Hence

`vol(K_0)<=rho^{n-1}vol(D)<= (2rho)^{n-1}`,

proving the first bound. Comparing it with `A_n` gives exactly the displayed threshold. ∎

This criterion measures asymmetry about the actual lattice point zero, not about the section barycenter. It therefore applies to some sections whose barycenter is nonzero. For large `n`, the threshold is asymptotic to `e/2`, since `A_n^{1/n}->e` and replacing the exponent `1/n` by `1/(n-1)` does not change the limit; it still does not cover arbitrary central sections.

A mixed version combines an imperfect axial width with section asymmetry.

**Corollary (width--asymmetry tradeoff).** Let `K` be a full-dimensional compact convex body with barycenter zero. In lattice coordinates, suppose the central section satisfies `K_0 subset -rho K_0`, the projection interval has length at most `w`, and `relint(K_0) cap Z^{n-1}={0}`. Then

`vol_n(K)<=w(2rho)^{n-1}`.

Consequently the conjectured bound follows whenever

`w rho^{n-1}<=A_n/2^{n-1}`.

**Proof.** The vertical component of the barycenter hypothesis makes zero the mean of the section-volume density. The log-concave mean-value lemma gives `vol_n(K)<=w vol_{n-1}(K_0)`. The symmetric-core argument gives `vol_{n-1}(K_0)<=(2rho)^{n-1}`. Multiply. ∎

This formulation separates the analytic section estimate from the arithmetic mechanism used to control axial width. It can be useful when width is known geometrically even though the axis itself is not an interior lattice chord.

More invariantly, under the original global hypotheses let `ell:Z^n->Z` be a primitive integral functional, let `[alpha,beta]=ell(K)`, and let `K_0=K cap ker(ell)`. Since the global barycenter is zero, `0 in int(K)`; hence `K_0` is full-dimensional in `ker(ell)` and its relative interior is lattice-free except for zero. After a unimodular coordinate change sending `ell` to the last coordinate, the preceding statement applies with `w=beta-alpha`. Thus the relevant quantity is lattice width in a primitive dual-lattice direction, together with origin-asymmetry of the zero fiber in the kernel lattice. This formulation avoids any dependence on Euclidean orthogonality or covolume conventions.

**Corollary (directional certificate).** Let `K` satisfy the original Ehrhart hypotheses. Suppose there is a primitive integral functional `ell` whose zero fiber is full-dimensional and satisfies

`K cap ker(ell) subset -rho (K cap ker(ell))`

and

`width_ell(K) rho^{n-1}<=A_n/2^{n-1}`.

Then `K` satisfies the Ehrhart conjectured bound.

**Proof.** Apply the width--asymmetry tradeoff after sending `ell` to the last coordinate by a unimodular map. ∎

Thus one may optimize the certificate `width_ell(K)rho_ell^{n-1}` over primitive directions in concrete examples. No general existence or attainment theorem for a good direction is claimed. The certificate is not expected to cover the sharp simplex: in dimension three, for a coordinate direction the sharp simplex has width four and a central triangular section of origin-asymmetry two, giving product `4*2^2=16`, far above the threshold `8/3`. This sanity check confirms that the criterion targets near-symmetric narrow sections rather than the extremal asymmetric geometry.

The certificate is stable under unimodular transformations: if `U in GL_n(Z)`, then the direction `ell` for `K` corresponds to `ell composed U^{-1}` for `U K`, with the same lattice width and the same origin-asymmetry factor of the transformed zero fiber. This follows directly from linear inclusions and preservation of the lattice. Hence the criterion is genuinely lattice-affine rather than coordinate-dependent.

If the whole body satisfies `K subset -rho K`, then every central section satisfies the same inclusion. Whenever one also has a primitive direction of width at most two and the zero section is lattice-free in the kernel lattice (automatic under the original global hypotheses), the directional estimate gives

`vol(K)<=2(2rho)^{n-1}`,

which improves the earlier global controlled-asymmetry estimate `(2rho)^n` by a factor `rho`. The width condition is additional and is not automatic from global asymmetry.

It is also monotone under strengthening either input. Computationally, it suffices to certify some bounds `width_ell(K)<=w` and `K_0 subset -rho K_0` with `w rho^{n-1}<=A_n/2^{n-1}`; one need not determine the exact width or minimal asymmetry factor.

For a polytope given by rational vertices and a fixed primitive functional `ell`, both certifications reduce to finite linear checks. The width is the difference of the maximum and minimum of `ell` on the vertex set. If the zero section is given in both vertex and facet form, then `K_0 subset -rho K_0` can be checked by testing every vertex of `K_0` against every facet inequality of `-rho K_0` (or by linear programming). Hence the directional criterion admits exact rational certificates for rational polytopes. This is an algorithmic observation, not a claim that a successful direction always exists.

For any zero-section convex body containing zero in its interior, the minimal admissible asymmetry factor has an explicit support-function formula:

`rho_0(K_0)=max_{u!=0} h_{K_0}(u)/h_{K_0}(-u)`.

Indeed `K_0 subset -rho K_0` is equivalent to `h_{K_0}(u)<=rho h_{K_0}(-u)` for every `u`. For a polytope it suffices to enforce the finitely many facet inequalities of `-rho K_0` on the vertices of `K_0`; equivalently the maximizing direction may be taken among facet-normal directions arising in this containment test. Thus the maximum is finite and rational when the data are rational. This identifies the exact quantity used by the certificate; it is the origin-based Minkowski asymmetry, not the translation-minimized asymmetry.

In dimension three, the primitive-axis case `w<=2` proves the conjecture whenever the planar central section obeys

`K_0 subset -rho K_0` with `rho<=2/sqrt(3) approximately 1.1547`,

since `A_3=32/3`. This is an explicit nonsymmetric three-dimensional subclass beyond centrally symmetric sections.

More generally in dimension three, in unimodular coordinates for any primitive integral functional, the full tradeoff is

`w rho^2<=8/3`,

because `A_3/2^2=8/3`. Thus a shorter projection interval permits greater section asymmetry; for example `w=1` allows `rho<=sqrt(8/3) approximately 1.633`. These are sufficient conditions only.

**Corollary (transverse symmetry).** In the proposition, condition 3 is automatic if the central section `K_0` is invariant under a family of linear maps of `R^{n-1}` whose common fixed-point subspace is `{0}`. More strongly, it is enough that this symmetry hold for `K_0` alone; no other section need have the same shape or symmetry.

**Proof.** Every invertible linear symmetry of a convex body fixes its barycenter: this follows by change of variables in the barycenter integral. Hence the barycenter of `K_0` belongs to the common fixed-point subspace, which is `{0}`. Apply the proposition. ∎

Examples include a centrally symmetric central section, an unconditional central section, or a section invariant under a nontrivial planar rotation in dimension three. The symmetries need not preserve the lattice, because they are used only to locate the section barycenter; lattice-freeness of the section comes directly from that of `K`.

For a symmetric central section, one can remove the inductive hypothesis entirely.

**Corollary (unconditional all-dimensional result).** Under conditions 1 and 2 of the general section-lifting proposition, if `K_0` is centrally symmetric about the origin, then

`vol_n(K)<=2^n<=A_n`.

Thus the Ehrhart conjecture holds for this class in every dimension, even though all noncentral sections may be asymmetric and may change shape arbitrarily.

**Proof.** The log-concave mean-value lemma and the width-two axial argument give `vol_n(K)<=2vol_{n-1}(K_0)`. The central section is origin-symmetric and lattice-free in `Z^{n-1}`, so Minkowski gives `vol_{n-1}(K_0)<=2^{n-1}`. The final comparison `2^n<=A_n` was proved in the first proposition. ∎

A useful sufficient geometric condition is invariance of the whole body under `(x,t) mapsto (-x,t)`: then every nonempty section is centrally symmetric about zero, and for every interior projection height the axial point `(0,t)` is interior. Hence the corollary applies. More general compact transverse symmetry groups with common fixed subspace `{0}` work the same way: averaging an interior orbit gives the axial point, which remains interior by convexity.

**Corollary (integral affine centroid path).** Suppose the barycenter `c(t)` of every nonempty horizontal section is affine in `t`, and its slope belongs to `Z^{n-1}`. Then the general section-lifting proposition applies after an integral shear; in particular the conjecture reduces to dimension `n-1`.

**Proof.** Write `c(t)=v t+w`. With `f(t)=vol_{n-1}(K_t)`, the horizontal barycenter equation is

`0=integral f(t)c(t)dt = v integral t f(t)dt + w integral f(t)dt`.

The vertical barycenter equation makes the first integral zero, while the final integral is positive. Thus `w=0`, and `c(t)=vt`. Section barycenters lie in the relative interiors of their sections, so `(vt,t) in int(K)` at every interior projection height. Since `v in Z^{n-1}`, the shear `(x,t) mapsto (x-vt,t)` is unimodular. It sends this interior centroid chord to the last coordinate axis, preserves the section at height zero and all hypotheses, and puts the body in the general section-lifting form. ∎

If the affine slope is not integral, this proof fails for a genuine arithmetic reason: the centroid chord need not contain lattice points at consecutive integer heights, so lattice-freeness need not bound its projected length by two.

## Homothetic-section bodies with arbitrary profile

The general criterion immediately implies the previous homothetic result; the direct argument is retained to make the hypotheses transparent.

**Proposition.** Let `B subset R^{n-1}` be a full-dimensional compact convex body with barycenter zero. Let `r:[alpha,beta] -> [0,infinity)` be concave and positive on `(alpha,beta)`, where `alpha<0<beta`. Define

`K={(r(t)x,t): x in B, alpha<=t<=beta}`.

Assume that `K` has barycenter zero and `int(K) cap Z^n={0}`. If the Ehrhart conjecture holds in dimension `n-1`, then it holds for `K` in dimension `n`.

**Proof.** The same convexity argument as above shows that `K` is a compact convex body. Every horizontal section is `r(t)B`, so its horizontal barycenter is zero and its volume is `r(t)^{n-1}vol(B)`. The vertical barycenter hypothesis says precisely

`integral_alpha^beta t r(t)^{n-1}dt=0`.

The function `f=r^{n-1}` is log-concave: on the positive interior, `log f=(n-1)log r` is concave because the logarithm is increasing and concave and `r` is concave.

Since `0 in int(B)`, the open axial segment belongs to `int(K)`. Lattice-freeness therefore gives `alpha>=-1` and `beta<=1`, hence `beta-alpha<=2`. The log-concave mean-value lemma, with mean zero, gives

`integral_alpha^beta r(t)^{n-1}dt <= (beta-alpha)r(0)^{n-1} <=2r(0)^{n-1}`.

The central section `r(0)B` is barycenter-zero and lattice-free in `Z^{n-1}`, so its volume is at most `A_{n-1}` by the lower-dimensional conjecture. Therefore

`vol_n(K)<=2 vol_{n-1}(r(0)B)<=2A_{n-1}<=A_n`.

This proves the claim. ∎

**Corollary.** Since the conjecture is known in dimension two, every such homothetic-section body in dimension three satisfies it, with no symmetry assumption on either `B` or the profile `r`.

The apparent requirement that the section centers lie on the last coordinate axis is inessential up to lattice-preserving shears.

**Corollary (primitive-axis form).** Let `u in Z^n` be primitive, and let `H` be a complementary lattice hyperplane, so that `Z^n=(Z^n cap H) direct-sum Z u`. Suppose, after choosing the corresponding coordinates, that

`K={t u+r(t)B: alpha<=t<=beta}`,

where `B subset H` is a full-dimensional compact convex body whose barycenter is zero in `H`, and `r` is positive and concave. If `K` has barycenter zero and no nonzero interior lattice point, then the preceding proposition applies (assuming the conjecture for the lattice `Z^n cap H` in dimension `n-1`).

**Proof.** A unimodular linear map sends `u` to the last standard basis vector and `Z^n cap H` to `Z^{n-1} times {0}`. It preserves barycenters, lattice points, and volume because its determinant has absolute value one. The transformed body has exactly the form of the proposition. ∎

Equivalently, integral affine shears of the displayed coordinate model are allowed. The proof still requires homothetic sections centered on a primitive lattice line. It does not cover sections that translate non-affinely or change shape.

## A higher-codimension lifting theorem

The entropy argument is not intrinsically one-dimensional.

**Lemma (multivariate log-concave mean-value bound).** Let `f` be an integrable log-concave function supported on a compact convex body `P subset R^r`, and let `m` be the mean of the probability density proportional to `f`. Then

`integral_P f <= vol_r(P) f(m)`.

**Proof.** The proof of the one-dimensional lemma applies verbatim: Jensen gives `log f(m)>=integral p log f`, while nonnegative relative entropy of `p=f/integral f` with respect to the uniform density on `P` gives `integral p log f>=log(integral f/vol(P))`. Equality forces equality in relative entropy, hence `f` is constant almost everywhere on `P`; conversely a constant function gives equality. ∎

**Theorem (factorized projection--fiber lifting).** Write `R^n=R^m times R^r`, with `m+r=n`, in lattice coordinates. Let `K` satisfy the Ehrhart hypotheses, let `P` be its projection onto `R^r`, and write

`K_y={x in R^m:(x,y) in K}`.

Assume:

1. `(0,y) in int(K)` for every `y in int(P)`;
2. the central fiber `K_0` has barycenter zero; and
3. the projection `P` has barycenter zero.

If the Ehrhart conjecture holds for both `K_0` in dimension `m` and `P` in dimension `r`, then it holds for `K` in dimension `n`. More precisely,

`vol_n(K)<=A_m A_r<=A_n`.

**Proof.** Put `f(y)=vol_m(K_y)`. The Brunn--Minkowski theorem in fiber form says that `f^{1/m}` is concave on `P`, so `f` is log-concave on its positive support. Projection of the global barycenter equation shows that the mean of the density proportional to `f` is zero. Hence the multivariate lemma gives

`vol_n(K)=integral_P f(y)dy <=vol_r(P)f(0)`.

Condition 1 implies that `int(P) cap Z^r={0}`, since any nonzero projected lattice point `y` would give the nonzero interior lattice point `(0,y)` of `K`. Condition 3 and the assumed `r`-dimensional result therefore give `vol_r(P)<=A_r`.

The relative interior of `K_0` lies in `int(K)`, so `K_0` is lattice-free in `Z^m`; condition 2 and the assumed `m`-dimensional result give `f(0)<=A_m`. Thus `vol_n(K)<=A_mA_r`. The numerical inequality `A_mA_r<=A_n` is the supermultiplicativity proved in the product-closure lemma below. ∎

This theorem is unconditional when both `m,r<=2`, giving in particular a four-dimensional class with arbitrary changing fiber shapes (and also the trivial lower-dimensional splits). Its strong geometric assumptions are barycentric centering of both the ordinary projection and central fiber, plus an interior zero section through every projected point. Notice that global barycenter zero centers the *fiber-volume-weighted* distribution on `P`; it does not imply that the uniform barycenter of `P` is zero, so condition 3 is genuinely additional.

The lattice splitting can be phrased in quotient language. Let `L subset Z^n` be a primitive rank-`m` sublattice and let `pi:Z^n -> Z^n/L` be the quotient lattice map. The central fiber is the canonical section `K cap span_R(L)`, while `P=pi(K)` lies in the quotient space. To state the interior zero-section condition one must additionally choose a lattice complement (a section of the quotient map); a different complement is related by an integral shear and need not preserve that condition unless the fiber-centroid map transforms accordingly. Thus the result concerns a primitive lattice quotient together with a compatible lattice splitting, not Euclidean orthogonality. This caveat prevents falsely treating condition 1 as splitting-independent.

**Corollary (two-factor origin-asymmetry).** Let `K` satisfy the original Ehrhart hypotheses and retain the factorized theorem's interior zero-section condition, but replace barycentric centering of the projection and central fiber by

`P subset -rho_P P`,

`K_0 subset -rho_0 K_0`.

Then

`vol_n(K)<= (2rho_P)^r (2rho_0)^m`.

Consequently the Ehrhart conjectured bound holds whenever

`rho_P^r rho_0^m <= A_n/2^n`.

**Proof.** The entropy argument uses only the global barycenter of `K` to place the mean of the fiber-volume density at zero; it does not use the uniform barycenter of `P` or the barycenter of `K_0`. Hence it still gives

`vol(K)<=vol(P)vol(K_0)`.

The interior zero-section condition makes `P` lattice-free in `Z^r`, while the central fiber is lattice-free in `Z^m`. Applying the symmetric-core/Minkowski argument separately gives

`vol(P)<=(2rho_P)^r`, `vol(K_0)<=(2rho_0)^m`.

Multiply. ∎

This result requires neither terminal factor to have barycenter zero. It measures both asymmetries about their common lattice point zero.

When a terminal factor is barycenter-zero and belongs to a dimension where the Ehrhart estimate is known, one may take the better of the two bounds. Explicitly,

`vol(P)<=min(A_r,(2rho_P)^r)`,

`vol(K_0)<=min(A_m,(2rho_0)^m)`.

Hence

`vol(K)<=min(A_r,(2rho_P)^r) min(A_m,(2rho_0)^m)`.

This hybrid simply chooses factor by factor between available estimates; it can certify mixed cases where one factor is best handled by centering and the other by origin-asymmetry. The symmetric-projection corollary is the case `rho_P=1` together with the sharper available estimate `vol(K_0)<=A_m`:

**Corollary (symmetric projection).** If `P=-P` and the central fiber is a known `m`-dimensional Ehrhart case, then

`vol_n(K)<=2^r A_m<=A_n`.

This is unconditional when `m<=2`, for arbitrary codimension `r`.

**Corollary (known terminal classes).** In the factorized theorem, it is not necessary that the full conjecture be known in dimensions `m` and `r`; it suffices that the particular bodies `K_0` and `P` belong to any proved classes. For example, each may independently be centrally symmetric, a simplex, planar, a product of known factors, or one of the flag-compatible bodies above. The resulting `K` may have neither symmetry nor homothetic fibers.

**Proof.** The theorem uses only the two numerical estimates `vol_m(K_0)<=A_m` and `vol_r(P)<=A_r`, not their source. ∎

A useful quantitative form allows imperfect terminal estimates.

**Corollary (defect multiplication).** Under the geometric hypotheses of the factorized theorem, suppose only that

`vol_m(K_0)<=delta_m A_m` and `vol_r(P)<=delta_r A_r`

for some positive `delta_m,delta_r`. Then

`vol_n(K)<=delta_m delta_r A_mA_r<=delta_m delta_r A_n`.

In particular, deficits below the conjectured constants multiply. If `delta_m delta_r<=A_n/(A_mA_r)`, the full `n`-dimensional conjectured bound still follows even though one or both terminal estimates individually exceed their conjectured bounds.

**Proof.** Substitute the two estimates into `vol_n(K)<=vol(P)vol(K_0)` and use `A_mA_r<=A_n`. The final assertion keeps the sharper product `A_mA_r` instead of replacing it by `A_n`. ∎

For example, in the split `n=4`, `m=r=2`, one has

`A_4/(A_2^2)=2500/1944=625/486 approximately 1.286`.

Thus the product of the two terminal defect factors may be as large as `625/486` while the four-dimensional target still holds. This numerical slack is modest but genuine.

The slack has a simple asymptotic scale. For a balanced split `n=2m`, Stirling's formula gives

`A_{2m}/A_m^2 = Theta(sqrt(m))`.

Indeed, using `k!~sqrt(2 pi k)(k/e)^k`, one has `A_k~e^{k+1}/sqrt(2 pi k)`, and substitution yields

`A_{2m}/A_m^2 ~ sqrt(pi m)/e`.

Thus higher-dimensional balanced factorizations can absorb a product defect growing like `sqrt(n)`, but not an exponential defect. This is an asymptotic diagnostic, not a new unrestricted estimate.

For a highly unbalanced split with fixed `m` and `r=n-m -> infinity`, the slack instead tends to a finite constant:

`A_n/(A_m A_{n-m}) -> e^m/A_m = e^m m!/(m+1)^m`.

This follows from `A_n/A_{n-m}->e^m`, using either the displayed asymptotic for `A_k` or direct logarithms. Hence only splits with both dimensions tending to infinity can produce growing slack.

More generally, if `m/n->theta in (0,1)`, Stirling gives

`A_n/(A_m A_{n-m}) ~ sqrt(2 pi theta(1-theta)n)/e`.

Indeed `A_k~e^{k+1}/sqrt(2 pi k)`, so the exponential factors cancel except for one factor `e^{-1}`, and the square-root factors give the expression above. The balanced constant `sqrt(pi n/2)/e` is the case `theta=1/2` (equivalently `n=2m`, giving `sqrt(pi m)/e`).

The interior zero-section hypothesis can be generated by a lattice-linear interior selector.

**Corollary (integral-linear selector).** Retain the lattice splitting and the projection `P`, but do not assume the factorized theorem's condition 1. Suppose there is an integer `m by r` matrix `T` such that

`(Ty,y) in int(K)` for every `y in int(P)`.

Assume `K` satisfies the original global Ehrhart hypotheses, and assume the projection and the fiber over zero satisfy the same centering/terminal-bound hypotheses as in the factorized theorem. Then its conclusion holds.

**Proof.** The unimodular shear `S(x,y)=(x-Ty,y)` sends the displayed interior selector to `(0,y)`. It preserves the lattice, volume, origin, the zero global barycenter, projection, and zero fiber. The factorized theorem applies to `S(K)`. ∎

This condition is strictly geometric and does not require the selected point to be a fiber centroid. For polytopes it can be verified by linear inequalities; one must check interiority over `int(P)`, not merely non-strict containment on projection vertices.

The selector can be combined with every terminal estimate above. In particular, if after the shear the projection and zero fiber obey origin-asymmetry factors `rho_P,rho_0`, then

`vol(K)<= (2rho_P)^r(2rho_0)^m`.

If they are centered known Ehrhart cases, then `vol(K)<=A_rA_m`; hybrid factor-by-factor estimates are also valid. This follows because the shear preserves both terminal bodies (projection exactly, zero fiber pointwise).

Fiber centroids give one mechanism for producing such a selector:

**Corollary (integral-affine fiber-centroid map).** Retain the lattice splitting and notation above, but do not assume condition 1. Suppose instead that every interior fiber `K_y` has barycenter

`c(y)=Ty+w`,

where `T` is an integer `m by r` matrix. If the projection `P` has barycenter zero and the Ehrhart conjecture is known in dimensions `m` and `r`, then `K` satisfies the `n`-dimensional bound.

(For convex bodies the fiber-centroid map is continuous on `int(P)`, so “every interior fiber” is the natural formulation; an almost-everywhere affine identity would extend to it by continuity.)

**Proof.** The global projected barycenter equation is

`integral_P y f(y)dy=0`,

where `f(y)=vol_m(K_y)`. The global horizontal barycenter equation is

`0=integral_P f(y)c(y)dy
  =T integral_P y f(y)dy+w integral_P f(y)dy`.

Since `K` has positive volume, the last factor is positive, so `w=0`. In particular the central fiber has barycenter zero.

Apply the block shear

`S(x,y)=(x-Ty,y)`.

Because `T` is integral, `S` is unimodular; it preserves volume, the lattice, the origin, and the global barycenter. The fiber of `S(K)` over `y` has barycenter zero, which lies in its relative interior. For a full-dimensional convex body, a relative-interior point of a fiber over an interior projection point is an interior point of the body; hence `(0,y) in int(S(K))` for every `y in int(P)`. The projection remains `P`, and the central fiber remains `K_0`, now known to have barycenter zero. The factorized projection--fiber theorem applies to `S(K)`, proving the claim. ∎

If `P=-P`, its Ehrhart bound may again be replaced by Minkowski's stronger `2^r` bound. The integrality of `T` is essential to this argument: without it the shear need not preserve `Z^n`.

In the symmetric-projection corollary, symmetry of the projection can be relaxed quantitatively. Retain the factorized theorem's interior zero-section condition and central-fiber centering, but assume instead

`P subset -rho P`

for some `rho>=1`, then the controlled-asymmetry argument applied in `R^r` gives `vol_r(P)<=(2rho)^r`, and the same proof yields

`vol_n(K)<=(2rho)^r A_m`.

Thus the conjectured bound follows whenever `(2rho)^r A_m<=A_n`, equivalently

`rho <= (A_n/(2^r A_m))^{1/r}`.

For `r=1`, no asymmetry hypothesis is needed: the interior zero-section condition and lattice-freeness directly force the projection interval to lie in `[-1,1]`, recovering the earlier section theorem.

## Iterated factorization along a lattice decomposition

The higher-codimension theorem can be iterated in blocks, not only one coordinate at a time.

**Theorem.** Let `n=d_1+...+d_l`, and choose a lattice decomposition

`Z^n=Lambda_1 direct-sum ... direct-sum Lambda_l`

with `rank(Lambda_i)=d_i`. Suppose `K` admits a recursive binary tree of projection--central-fiber factorizations compatible with this decomposition such that at every internal node:

1. the relevant projection and central fiber have barycenter zero;
2. the interior of the projection lifts through an interior zero section; and
3. the two children are the projection and central fiber, with recursion continuing until the block bodies are reached.

Let `B_i` be the terminal bodies in the blocks `Lambda_i`. Then

`vol_n(K)<=product_{i=1}^l vol_{d_i}(B_i)`.

If every `B_i` satisfies its Ehrhart bound, then

`vol_n(K)<=product_i A_{d_i}<=A_n`.

**Proof.** Apply the factorized projection--fiber theorem's fundamental estimate

`vol(K)<=vol(projection) vol(central fiber)`

at the root and then recursively at both children according to the assumed tree. Repeating yields the product of terminal volumes. The numerical inequality follows by repeated supermultiplicativity `A_aA_b<=A_{a+b}`. ∎

There is also an origin-asymmetry version requiring no barycenter condition on the **terminal leaves**. Retain barycenter zero for every body at an internal node (needed to center that node's fiber-volume density), together with the compatible interior zero-section geometry. If each terminal body obeys

`B_i subset -rho_i B_i`,

then the same recursive entropy estimates followed by symmetric-core Minkowski bounds at the leaves give

`vol_n(K)<=2^n product_i rho_i^{d_i}`.

Hence the Ehrhart target follows whenever

`product_i rho_i^{d_i}<=A_n/2^n`.

This is the block analogue of the two-factor origin-asymmetry corollary.

The same statement allows terminal defect factors `delta_i`, yielding

`vol_n(K)<= (product_i delta_i)(product_i A_{d_i})`.

Thus the conjectured target follows whenever

`product_i delta_i <= A_n/(product_i A_{d_i})`.

For a fixed number `l` of proportional blocks with `d_i/n->theta_i>0`, `sum theta_i=1`, Stirling gives

`A_n/(product_i A_{d_i})
 ~ (2 pi n)^{(l-1)/2} sqrt(product_i theta_i)/e^{l-1}`.

So an `l`-block balanced factorization has polynomial slack of order `n^{(l-1)/2}`, still not exponential slack.

## A flag-lifting theorem

The section argument can also be iterated along a partial or full lattice flag.

**Theorem.** Let `K_n=K subset R^n` satisfy the Ehrhart hypotheses. Suppose that, after one unimodular change of coordinates, there is a nested sequence

`K_n superset K_{n-1} superset ... superset K_m`,

where `1<=m<n`, each `K_j=K_{j+1} cap (R^j times {0})` is full-dimensional in `R^j` and has barycenter zero, and the line segment

`{(0,...,0,t) in R^{j+1}: alpha_j<t<beta_j}`

lies in `int_{R^{j+1}}(K_{j+1})` and is the full projection interval in the last coordinate. Then

`vol_n(K) <= 2^{n-m} vol_m(K_m)`.

Consequently, if the Ehrhart conjecture is known for `K_m`, then it holds for `K`. In particular, taking `m=1` gives `vol_n(K)<=2^n`; taking `m=2` gives an unconditional result using Ehrhart's planar theorem.

**Proof.** Because `K_j` is full-dimensional in `R^j` and has barycenter zero, the origin lies in `relint(K_j)`, hence in `int(K_{j+1})`. For a convex body intersected by an affine subspace through an interior point, the relative interior of the section equals the intersection of the body's interior with that subspace. Therefore every `K_j` is lattice-free in its relative interior.

At the step from `K_{j+1}` to `K_j`, let `f_j(t)` be the `j`-dimensional volume of the section at height `t`. Brunn--Minkowski makes `f_j` log-concave, and barycenter zero of `K_{j+1}` makes its mean zero. The entropy lemma gives

`vol_{j+1}(K_{j+1}) <= (beta_j-alpha_j) vol_j(K_j)`.

The interior primitive axial segment and lattice-freeness force `beta_j-alpha_j<=2`. Hence

`vol_{j+1}(K_{j+1})<=2vol_j(K_j)`.

Iterating gives `vol_n(K)<=2^{n-m}vol_m(K_m)`. If `vol_m(K_m)<=A_m`, then

`vol_n(K)<=2^{n-m}A_m<=A_n`,

because every ratio `A_{j+1}/A_j=(1+1/(j+1))^{j+1}` is at least two. For `m=1`, the body `K_1` is an interval containing zero in its interior and no other interior integer, so its length is at most two and `vol_n(K)<=2^n`. For `m=2`, the required terminal estimate is the known planar theorem. ∎

This theorem allows every intermediate family of sections to change shape arbitrarily. Its strong hypothesis is the existence of one unimodular coordinate flag for which every zero section is barycentrically centered and every corresponding coordinate axis is an interior chord. Transverse unconditional symmetry is one sufficient mechanism, but the theorem also covers nonsymmetric flag-compatible bodies.

For fixed terminal dimension `m`, the ratio of the flag bound to the conjectured target decays exponentially:

`2^{n-m}A_m/A_n = Theta_m(n^{1/2}(2/e)^n)`.

Indeed `A_n~e^{n+1}/sqrt(2 pi n)`, while `2^{-m}A_m` is constant. Thus long compatible flags give bounds vastly stronger than required; their limitation is entirely geometric existence, not constants.

## A direct-sum construction with coupled fibers

The factorized theorem is not limited to Cartesian products. The following explicit construction gives genuinely coupled examples while keeping all hypotheses transparent.

**Proposition.** Let `B subset R^m` and `P subset R^r` be full-dimensional compact convex bodies with barycenter zero, each lattice-free except for the origin in its interior, and satisfying their respective Ehrhart bounds. Let `phi:P->[0,infinity)` be concave and positive on `int(P)`, with `phi(0)=1`. Define

`K={(phi(y)x,y): x in B, y in P}`.

Assume the weighted moment condition

`integral_P y phi(y)^m dy=0`.

Then `K` is lattice-free except for the origin in its interior, has barycenter zero, and

`vol_{m+r}(K)<=A_mA_r<=A_{m+r}`.

**Proof.** The fiber over `y` is `phi(y)B`, whose barycenter is zero; in particular the central fiber is `phi(0)B=B`, so it has barycenter zero and the assumed volume bound. Since `0 in int(P)` and `phi(0)=1`, the central fiber is full-dimensional. Since also `0 in int(B)` and `phi>0` on `int(P)`, one has `(0,y) in int(K)` for every `y in int(P)`. Convexity follows exactly as in the one-parameter homothetic-section argument, now using concavity of `phi` on `P`. Any interior lattice point `(x,y)` of `K` projects to `y in int(P) cap Z^r` (linear projection maps an open neighborhood of `(x,y)` to a neighborhood of `y`), hence `y=0`. It then lies in the relative interior of the central fiber `B`, so `x=0`. Thus `K` is lattice-free except for the origin. The horizontal first moment of every fiber vanishes. The displayed weighted moment is exactly the vertical first moment of `K`, up to the positive constant `vol_m(B)`, so `K` has barycenter zero. The projection is `P`, which has barycenter zero by assumption. Therefore all hypotheses of the factorized projection--fiber theorem hold, and the stated estimate follows.

The weighted moment is not implied by the unweighted barycenter condition on `P` unless, for example, `phi` is constant or a symmetry forces both moments to vanish. ∎

When `phi` is nonconstant, these bodies are generally not Cartesian products; when `B` and `P` are asymmetric known cases, they need not possess central symmetry. The proposition is still a structured construction, not a general theorem.

Boundary lattice points of `P` cause no issue because the projection of an interior point of `K` lies in `int(P)`. This is why lattice-freeness of the two terminal bodies suffices for the construction.

A broad automatic source of the weighted moment condition is symmetry. If a compact group `Gamma` acts linearly on `R^r`, preserves `P` and `phi`, and has common fixed-point subspace `{0}`, then

`integral_P y phi(y)^m dy`

is fixed by `Gamma` and therefore equals zero. Here every group element has Jacobian of absolute value one: it maps the full-dimensional finite-volume body `P` onto itself, so volume comparison forces this. Thus central symmetry is not required: rotational or irreducible finite-group symmetry of the projection/profile suffices. The unweighted barycenter of `P` vanishes by the same argument.

## A product-closure lemma

Write `A_d=(d+1)^d/d!`.

**Lemma.** Suppose full-dimensional compact convex bodies `K_i subset R^{d_i}` (`i=1,2`) have barycenter zero, satisfy

`int(K_i) cap Z^{d_i}={0}`

and obey `vol(K_i) <= A_{d_i}`. Then `K_1 times K_2` satisfies all the analogous hypotheses in dimension `d_1+d_2` and obeys the conjectured bound there.

**Proof.** The product is full-dimensional, compact, and convex. Fubini's theorem shows that its barycenter is the ordered pair of the factor barycenters, hence zero. Also

`int(K_1 times K_2)=int(K_1) times int(K_2)`.

Consequently, an interior lattice point of the product has both components equal to zero.

Set `a=d_1`, `b=d_2`, and `d=a+b`. Multiplicativity of Lebesgue measure and the assumed factor bounds give

`vol(K_1 times K_2) <= A_a A_b`.

It remains to check the numerical inequality `A_a A_b<=A_{a+b}`. Set `A_0=1`. Direct cancellation gives

`A_j/A_{j-1} = (1+1/j)^j`  for `j>=1`.

These ratios increase with `j`: indeed, for real `x>0`,

`d/dx [x log(1+1/x)] = log(1+1/x)-1/(x+1) > 0`,

where the strict inequality follows from `log(1+t)>t/(1+t)` for `t>0` (integrate `1/(1+u)>1/(1+t)` from `u=0` to `t`). Assuming without loss of generality that `a,b>=1`, monotonicity of the ratios yields

`A_{a+b}/A_a = product_{j=1}^b (A_{a+j}/A_{a+j-1}) >= product_{j=1}^b (A_j/A_{j-1}) = A_b`.

Thus `A_a A_b<=A_{a+b}`, proving the claim. ∎

**Corollary.** Any finite Cartesian product of factors for which the Ehrhart bound is known also satisfies it. In particular, products of centrally symmetric factors, planar factors (using Ehrhart's known two-dimensional theorem), and barycentrically centered lattice-free simplices satisfy the conjectured bound. Such products need not themselves be centrally symmetric or simplices.

This closure result is rigorous but elementary; it does not improve the best general bound or settle a new irreducible dimension.
