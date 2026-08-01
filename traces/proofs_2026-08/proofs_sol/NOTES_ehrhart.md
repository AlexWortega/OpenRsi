# Ehrhart attack log

## Restatement

Given a full-dimensional compact convex body `K` in `R^n`, centered by barycenter at `0`, and with `int(K) cap Z^n = {0}`, show

`vol(K) <= A_n := (n+1)^n/n!`.

The difficulty is that Minkowski directly handles symmetric bodies, while barycentric centering is much weaker than central symmetry.

## Three promising routes

1. **Symmetric core / quantified asymmetry.** Apply Minkowski to `K cap (-K)` and seek a sharp lower bound for its volume in terms of `vol(K)` using barycentric centering. Expected difficulty: high; the known generic comparison leads only to the `4^n` scale.
2. **Slicing and induction.** Slice along primitive lattice directions, use one-dimensional concavity of section volumes and barycenter constraints, and induct on dimension/lattice quotients. Expected difficulty: very high; a generic slice need not inherit lattice-freeness or barycentric centering.
3. **Special-class closure (products, unconditional bodies, controlled asymmetry).** Prove the conjecture for larger explicit classes by combining known low-dimensional/simplex/symmetric cases. Expected difficulty: low to medium; unlikely alone to solve the asymmetric general case, but can yield rigorous partial results.

## Initial rigorous baseline

For `K=-K`, Minkowski gives `vol(K)<=2^n`, and AM-GM gives `2^n<=A_n`. See `proof_ehrhart.md`.

## Completed cheap results

### Controlled asymmetry

If `K subset -rho K`, then `(1/rho)K subset K cap (-K)`. Applying Minkowski to the symmetric core gives `vol(K)<= (2rho)^n`. Therefore the conjecture follows for `rho <= (n+1)/(2(n!)^(1/n))`, a threshold tending to `e/2`. This strictly extends central symmetry but not the unrestricted case; see `proof_ehrhart.md`.

### Lattice-aligned centered pyramids

The symmetry assumption on the base was unnecessary if one phrases the argument inductively. For `K=conv((B,-a),(0,na))`, where `B` is any barycenter-zero body in the horizontal lattice hyperplane, lattice-freeness of the axial segment forces `a<=1/n`. The zero-height section is `C=(n/(n+1))B`, is lattice-free, and has barycenter zero. Assuming the conjecture in dimension `n-1`, the pyramid formula yields

`vol(K)<= (n+1)^n/(n n!)`,

a factor `n` stronger than required. This is unconditional in dimension three because the planar theorem is known. If `B` is symmetric, Minkowski gives the all-dimensional bound previously recorded. The route is banked; arbitrary orientation loses the axial lattice point.

### General section lifting via log-concavity

The entropy/Jensen lemma plus Brunn--Minkowski removes the homothety restriction entirely. For any convex body, horizontal section volume `f(t)` is log-concave because `f^(1/(n-1))` is concave. Global barycenter zero makes zero the mean of `f`, hence `integral f <= (beta-alpha)f(0)`. If an interior primitive lattice chord passes through the origin, lattice-freeness forces `beta-alpha<=2`; if the central section itself has barycenter zero, dimension `n-1` gives `f(0)<=A_(n-1)`. Therefore `vol(K)<=2A_(n-1)<=A_n`. This is unconditional in dimension three and permits arbitrary changing section shapes. Since `2A_(n-1)<A_n` for `n>=2`, the lifted bound has strict slack and these classes contain no sharp equality body. The ratio to the target tends to `2/e`, i.e. an asymptotic improvement factor `e/2`. Numerical stress checks passed. Equality in the entropy mean-value bound forces constant section volume. Using convexity plus the equality case of Brunn--Minkowski then shows all interior fibers are translates and their centroid path is affine; global centering makes the body an affine shear of a cylinder up to endpoint fibers. Only integral shear slope gives a lattice-preserving normalization. The section-centering assumption can be weakened: if the zero section obeys origin-asymmetry `K_0 subset -rho K_0`, then its symmetric core plus Minkowski gives `vol(K)<=2(2rho)^(n-1)`. The conjecture follows for `rho<=(A_n/2^n)^(1/(n-1))`, tending to `e/2`. This uses asymmetry about the lattice point zero, not the section barycenter, so it covers some non-centered sections. More generally, if axial projection length is bounded by `w`, then `vol(K)<=w(2rho)^(n-1)`; the criterion cleanly trades geometric width against section asymmetry. In dimension three the full condition is `w rho^2<=8/3`; width two gives `rho<=2/sqrt(3)≈1.1547`, while width one permits `rho<=sqrt(8/3)≈1.633`. Under the original hypotheses every primitive zero fiber is automatically full-dimensional and relatively lattice-free because barycenter zero lies in `int(K)`. The invariant certificate is: some primitive integral functional `ell` with full zero fiber must satisfy `width_ell(K) rho_ell^(n-1)<=A_n/2^(n-1)`. One may optimize this in examples, but no general good-direction theorem is claimed. It fails badly on the sharp 3D simplex (coordinate width 4, section asymmetry 2, certificate product 16 versus threshold `8/3`), confirming it addresses near-symmetric narrow geometry. If global `K subset -rho K` and some primitive width is at most two, the sectional estimate improves the global `(2rho)^n` bound to `2(2rho)^(n-1)`, a factor `rho`; width is an extra hypothesis. For rational polytopes, width and the inclusion `K_0 subset -rho K_0` admit finite exact vertex/facet or LP certificates. The exact origin-asymmetry is `max_u h_K0(u)/h_K0(-u)`, rational for rational polytopes via the finite containment LP. Global barycenter zero still does not control arbitrary centroid paths. It is automatic if the central section has symmetries with common fixed point zero. An earlier claim for arbitrary affine centroid paths omitted the arithmetic interior-axis condition and was too broad. The corrected statement requires integral slope: then the centroid chord is sent to the primitive coordinate axis by a unimodular shear. If the central section is origin-symmetric, induction is unnecessary: Minkowski gives its volume at most `2^(n-1)`, hence `vol(K)<=2^n<=A_n` in every dimension, while other sections may change shape arbitrarily. A whole-body transverse symmetry is a clean sufficient condition for the needed interior axis. Random centroid-zero tetrahedra numerically exhibit nonzero centroid of the `t=0` section, confirming that the remaining section-centering hypothesis is genuinely nonautomatic (this experiment is illustrative only).

### Higher-codimension lifting

A two-factor origin-asymmetry variant removes barycenter assumptions on both terminal bodies: under the interior zero-section geometry, `P subset -rho_P P` and `K_0 subset -rho_0 K_0` imply `vol(K)<=(2rho_P)^r(2rho_0)^m`. The target follows if `rho_P^r rho_0^m<=A_n/2^n`. If a terminal factor is also centered with a known Ehrhart estimate, use the hybrid factor bound `min(A_d,(2rho)^d)`. For one factorization, only the global body barycenter is used analytically. Recursing over blocks gives `vol(K)<=2^n product rho_i^(d_i)` and target condition `product rho_i^(d_i)<=A_n/2^n`; referee caveat: every internal-node body must still have barycenter zero to center its own entropy estimate. Only terminal-leaf barycenters are dispensable.


The entropy lemma extends to log-concave densities on `R^r`: `integral_P f<=vol(P)f(mean)`. For fibers, Brunn--Minkowski makes fiber volume log-concave and global barycenter gives weighted mean zero. If the ordinary projection `P` and central fiber are both barycenter-zero known Ehrhart cases, and `(0,y)` is interior over `int(P)`, then both are lattice-free and `vol(K)<=A_rA_m<=A_n`. This is unconditional when `r,m<=2`, giving a four-dimensional class. Important referee point: weighted mean zero does not imply uniform barycenter of `P` is zero (e.g. on `[-1,1/2]` with affine weight `1+y`, weighted mean is zero but interval midpoint is `-1/4`), so projection centering is extra. The interior zero-section hypothesis is automatic after a unimodular block shear whenever there is an integral-linear interior selector `(Ty,y)`. Because the shear fixes the projection and zero fiber, this selector mechanism combines with centered, origin-asymmetry, defect, or hybrid terminal estimates. Integral-affine fiber centroids are one source: for `c(y)=Ty+w`, global horizontal/vertical moment equations force `w=0`, and integral `T` preserves the lattice. Block determinants and moment identities were computationally checked. The projection/fiber theorem only needs the two terminal numerical estimates, so terminal bodies may independently come from any proved class. More generally terminal defect factors multiply: `vol(K)<=delta_m delta_r A_mA_r`; slack `A_n/(A_mA_r)>1` can absorb moderate terminal losses. For the `2+2` split in dimension four the exact slack is `625/486≈1.286`. For a balanced `2m=m+m` split, Stirling gives slack asymptotic to `sqrt(pi m)/e`, so factorization absorbs only polynomial (`sqrt n`) terminal loss. For fixed `m` and `n-m->infinity`, slack tends to the finite constant `e^m/A_m`; growing slack requires both factors to grow. For `m/n->theta in (0,1)`, the exact asymptotic is `sqrt(2 pi theta(1-theta)n)/e`, numerically checked for several proportions.

The higher-codimension result is naturally about a primitive lattice quotient plus a compatible lattice splitting. The central fiber and projection are canonical for the quotient, but the interior zero-section condition depends on the complement; changing complements is an integral shear. This dependence is now stated explicitly to avoid an invariance overclaim.

### Iterated block factorization

A recursive binary tree of compatible projection--fiber factorizations over a lattice block decomposition yields `vol(K)<=product_i vol(B_i)`. Known terminal estimates combine by repeated supermultiplicativity. Terminal defects multiply, with slack `A_n/product A_(d_i)`. For `l` proportional blocks this slack is asymptotic to `(2 pi n)^((l-1)/2)sqrt(product theta_i)/e^(l-1)`, polynomial of degree `(l-1)/2`, numerically checked for several decompositions.

### Flag lifting

Iterating the general-section entropy argument along a unimodular coordinate flag gives `vol_n(K)<=2^(n-m)vol_m(K_m)` for any terminal dimension `m`. If the terminal section is a known Ehrhart case, then `2^(n-m)A_m<=A_n`; in particular one may stop at dimension two and invoke the planar theorem, or at dimension one to get `2^n`. Sections may change shape arbitrarily and need not be symmetric. For fixed terminal `m`, the bound/target ratio is `Theta_m(sqrt(n)(2/e)^n)`, exponentially small. The strong nonautomatic input is a single lattice flag compatible with all sectional barycenters/interior chords.

### Coupled homothetic fibers

An explicit non-product construction is banked: `K={(phi(y)x,y):x in B,y in P}`, with `phi` concave, positive, normalized by `phi(0)=1`, projection/base `P,B` barycenter-zero known cases, and weighted moment `integral y phi(y)^m=0`. Lattice-freeness of `K` is automatic from that of `P` and `B`: an interior lattice point projects into `int(P)`, hence to zero, then lies in the central fiber `B`, hence is zero. Factorized lifting gives `vol(K)<=A_mA_r`. Nonconstant `phi` couples fibers, so these are not Cartesian products; the assumptions remain structured. The weighted moment is automatic if a compact linear symmetry group preserves `P` and `phi` and has fixed subspace zero; this allows rotational/irreducible finite-group symmetry, not only central symmetry.

### Cartesian products

If `K=K_1 x K_2`, its barycenter is the pair of barycenters, its volume is the product, and interior lattice-freeness passes between the factors and product. The needed numerical supermultiplicativity `A_a A_b <= A_{a+b}` follows because `A_j/A_{j-1}=(1+1/j)^j` is increasing. Thus known cases combine into nonsymmetric higher-dimensional examples; see `proof_ehrhart.md`.

## Verification

Run `python3 verify_ehrhart.py` for exact rational checks of all displayed constant comparisons through the stated finite ranges.

## Referee checklist

- Barycenter `0` is indeed in `int(K)` for a full-dimensional compact convex body.
- Minkowski's strict-volume formulation yields a point in the interior when `vol(K)>2^n`; equality is handled by contradiction, so no boundary issue.
- Product interiors satisfy `int(K_1 x K_2)=int(K_1)x int(K_2)`.
- A tempting earlier proof of `A_aA_b<=A_{a+b}` by separately comparing powers was invalid: it ignored the binomial/factorial contribution. It was replaced by a valid monotone-ratio proof.
- For controlled asymmetry, `K subset -rho K` gives `(1/rho)K subset -K`; convexity plus `0 in K` separately gives `(1/rho)K subset K. Both inclusions are needed.
- `int(K cap -K)=int(K) cap int(-K)` here because both interiors contain `(1/rho)int(K)`; hence applying Minkowski to the symmetric core is legitimate.
- In the pyramid argument, barycenter zero of full-dimensional `B` implies `0 in int(B)`. Therefore the open base-to-apex axial segment really is in `int(K)`; without this observation the `(0,1)` obstruction would have a gap.
- An earlier off-center corollary was redundant and potentially misleading because the original global hypothesis permits only the origin as an interior lattice point. It was replaced by the direct asymmetric-interval criterion `[alpha,beta]`, which is stronger and cleaner.
