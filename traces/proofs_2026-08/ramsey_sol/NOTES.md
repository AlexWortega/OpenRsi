# Attack log

## Initialization
Read STATUS and Ramsey notes in `prior/round1`, `prior/sol`, and `prior/fable`; read the inherited Ramsey proofs. Reran the two available baseline verifiers in round1/sol; both pass. `prior/fable` has no `verify_ramsey.py`, so no nonexistent verifier is claimed.

Banked all routes listed in AGENTS.md and prior STATUS: fixed-seed products, iid/first-moment/basic LLL, cyclic/shifted/dihedral/interval/local-palette/coarse-state/Mycielski/Cayley-cube attempts, and ternary difference colorings.

## Selected routes
See STATUS.md. Two bounded-time background searches were launched: random maximal triangle-free complements and the explicit shift-graph family. Promotion rule: heuristic output is never a claim; an explicit candidate requires an independent verifier, and asymptotic progress requires a proof family rather than extrapolation.

The initially listed Kneser idea fails a necessary diagnostic: for disjointness graphs `KG(n,r)`, triangle-free means `n<3r`, whereas the standard vertex-transitive fractional chromatic value is `n/r<3`; since capacity is at most fractional chromatic number, this family cannot have growing capacity. It was replaced by shift graphs, whose ordinary chromatic number grows, with fractional growth still requiring analysis.

Early heuristic logs have no zero-conflict candidate. Random triangle-free tests reached 4--6 residual conflicts at cube targets 13--14; shift graphs reached 4 residual conflicts at `(n,m,M)=(6,3,13)`. These are non-results, not bounds.

The Heisenberg difference-partition generator was first sanity-tested at modulus 3. It correctly finds a one-orbit obstruction: the central element `(0,0,1)` and its square/inverse `(0,0,2)` force a product triple within one inverse orbit. Thus odd-exponent-3 behavior reproduces the known ternary obstruction and is not pursued.

## First harvest

- Random maximal triangle-free graphs: no valid code; best 4 residual conflicts for 13 words in a cube. With neither a candidate nor coherent scalable structure, banked.
- Shift graphs: no valid code; best 4 residual conflicts at 13 cube words. LP values rise to 3 at label size 12. Adversarial analysis then found a decisive universal bound: choose a random bipartition `A∪B`; directed pairs from `A` to `B` form an independent set in the shift graph. Giving every one of the `2^n` cuts weight `4/2^n` covers each ordered pair `(a,b)` with total weight one and has total weight four. Therefore `chi_f(H_n)<=4`, hence `Theta(complement H_n)<=4`. Shift graphs are rigorously banked as constant-capacity.
- Heisenberg `H(Z/4Z)`: min-conflicts found a zero-conflict 5-color inverse-orbit partition. Independent script `experiments/verify_heisenberg_partition.py` checks the group partition, inverse closure, product-freeness, and all 41,664 vertex triangles. Class sizes are `[18,9,12,13,11]`. This proves only `R_5(3)>64`, base about 2.297, far below 3.199. It is not goal-ladder progress. A 4-color test and modulus-8/7-color scaling test are running.
- Started `UT(5,2)` (order 1024) as a richer nilpotent 2-group. A 10-color partition was found immediately and independently checked by `experiments/verify_unitriangular_partition.py`, including every within-class product. It gives base `1024^(1/10)=2`, so is asymptotically uninteresting by itself. Searches with 8 and 5 colors are the discriminating tests; current residuals 10 and 529 show the latter is implausible. A bounded `UT(4,2)`/4-color sanity run reached 4 conflicts, no claim.

Generalized shift graphs were tested next, then rejected analytically before
spending another search cycle. Map each ground-set label randomly to a bit; an
r-tuple receives an r-bit window. Any independent set in the binary de Bruijn
transition graph pulls back to an independent set of the generalized shift
graph. The de Bruijn graph has two looped constant patterns, which must be excluded. On the remaining patterns its underlying graph has maximum degree at most four, yielding an independent set of size at least `(2^r-2)/5` and a fractional coloring of weight at most 10 uniformly in `r>=2`. Therefore the generalized-shift hierarchy still has bounded capacity, but the earlier stated constant 5 was unjustified and is corrected to 10.
The running heuristic is now diagnostic only and will not be extended.

Re-referee correction: do not bank the entire unitriangular hierarchy merely
because the first seed has base 2. `|UT(n,2)|=2^{binom(n,2)}`; a partition into
`O(n)` product-free inverse-closed classes would immediately have an
exponentially growing per-color base and prove the target along a dense
sequence. Thus `UT(n,2)` is qualitatively different from the order-doubling
families and remains active until its required color count is shown empirically
to scale quadratically. Launched the missing `UT(5,2)`/9-color threshold test;
Exact SAT at n=3 found a verified 3-color partition (sizes `[3,3,1]`) and solver-UNSAT at 2. At n=4 it returned solver-UNSAT for 4 colors and SAT for 5; the SAT seed independently verifies with class sizes `[5,5,5,16,32]`. Because no DRAT/LRAT certificate is retained, the 4-color impossibility is a solver result rather than a promoted rigorous finite theorem. At n=5, exact SAT found 9 colors and the independent verifier passes. Striking class sizes `[5,5,5,16,32,64,128,256,512]` strongly indicate a recursive index-two construction: the three small size-5 classes are the n=3/4 core and six new classes consume powers of two. This is the wrong scaling if it persists (roughly doubling the number of colors with n), despite group order being quadratic-exponential. The 8-color exact run later timed out. No scalable symbolic compression was found.

Structural identification: coloring a nonidentity `UT(n,2)` matrix by the
highest indexed nonzero upper-triangular entry always gives `binom(n,2)`
product-free inverse-closed classes (checked symbolically at the filtration
level; computational sanity through n=5). The verified SAT seeds use exactly
this singleton-leading-bit construction for all high coordinates and compress
only the first four coordinates from four colors to three, hence the observed
count `binom(n,2)-1` for n=4,5. This explains the geometric class sizes and is
a coherent **fixed-base-2** family, not a growing-base mechanism. Any value in
the unitriangular route must come from compression increasing with n; the n=5
8-color SAT test asks for just one further compression and is therefore a sharp
small discriminator.

## Second harvest and switch

The exact `UT(5,2)`/8-color SAT process timed out after ten minutes without an
answer; no UNSAT claim. Together with the proved highest-entry `binom(n,2)`
coloring and only constant compression in n=3,4,5, this route is banked.

Tested two factorial-size ideas before attempting proofs:

1. **Symmetric-group difference coloring.** For `S_n`, the least moved point
   maps to a larger image, so the raw label is an unordered pair and gives
   `binom(n,2)` product-free classes of sizes `(j-1)!` by level. Exhaustive
   quotient SAT shows no two pair states can be merged for n=4,5 and (within
   timeout) n=6; thresholds observed are exactly 6,10,15 states. This is the
   group analogue of the prior permutation compression rigidity, hence banked.
   Solver UNSAT outputs are heuristic diagnostics only, without certificates.
2. **Polynomial evaluation words.** Degree-<d polynomials over F_q give q^d
   vertices. Coloring by first evaluation point and a triangle-free coloring of
   K_q is valid, but uses d times the inner palette: exactly ordinary
   first-difference amplification. Exhaustive tests confirm raw/sum/product and
   q=5,7 difference rules but all have fixed alphabet base. Ratio compression
   already fails at q=7. Banked as circular/fixed-base.

Also tested affine diagonal quotients of the permutation first-difference label
(position, unordered value pair). Every tested family fails by n=4 with an
explicit triangle witness. These are experiments, not finite promoted claims,
and no more budget goes to this fixed-label quotient route.

Correction to the coarse symmetric-group conclusion: quotienting only the pair
state is rigid, but the full permutation first-difference state includes both
position and value-pair and can compress. Exact SAT found verified colorings
`K_24/5`, `K_120/7`, and `K_720/10`; independent direct verifier checks all
2,024, 280,840, and 61,949,040 triangles. Their bases are 1.888, 1.982, 1.931,
so the color count appears roughly quadratic and this is emphatically not
progress. The route is banked after the n=6 extension.

Launched discriminating translation-partition trend tests at `(d,k)=(10,7),
(11,8),(12,9)`. All three rapidly converged to about 34 residual projective
lines and stalled; this mirrors prior smaller failures and gives no candidate.
They remain heuristic runs and no impossibility is claimed.
The three `F_2` trend searches were terminated after more than five minutes
with stable best residual 34 in each; banked as low-yield, not as evidence of
UNSAT.

Constant-weight subset graphs were scanned next: vertices are r-subsets and
adjacency depends only on intersection size, with triangle-freeness checked
exactly before any code search. All surviving families through n=10 gave greedy
cube bases at most 10^(1/3)=2.154 and square base 2. The dominant cases are
Kneser/disjointness variants already bounded or banked. No candidate; route
banked after this discriminating scan.

## Node-dependent permutation-tree nudge

Allowed every prefix node to relabel every child pair independently, a much
larger class than the prior global state quotient. Exact SAT plus independent
verification again gives 5,7,10 colors for n=4,5,6; the n=6/9-color run timed
out. Bases remain below 2. A scalable remaining-set template (color depends on
remaining symbol set and child pair) matches 5,7,10 through n=6, while n=7
nearby targets time out. First-inversion label compressions and affine formulas
all fail from n=4 onward unless retaining the full pair. This is a decisive
second nudge with no growing trend, so the permutation-tree route is banked.

A 1,539-instance random triangle-free circulant scan was harvested. Among 1,042
small instances where cube words were searched, the best greedy code size was
10 (base 2.154), with no trend by order. Some larger instances have weak greedy
fractional-chromatic diagnostics up to 8.17, but no code search/certificate and
no coherent lower mechanism. Plain circulant capacities are banked, consistent
with prior cyclic/Cayley failures.

Twisted finite-field endpoint rules were tested on all triangles through 400
vertices. First-coordinate sum/product rules are valid but use Theta(dq)
colors on q^d words, exactly fixed-alphabet first-difference scale. Dot-product,
symplectic, and quadratic endpoint hashes all acquire explicit monochromatic
triangles already in dimension 2 for q=3,5,7. Banked.

## Iterated wreath 2-group probe

Tested the Sylow-2 wreath tower `W_{m+1}=W_m wr C_2`, whose orders satisfy
`log_2|W_{m+1}|=1+2 log_2|W_m|`. Level 3 has order 128. Min-conflicts first found 7 colors, then the 6-color run reached zero. The 6-color partition is independently checked on all 341,376 triangles by `verify_wreath_partition.py`, giving base `128^(1/6)=2.245`. This is still far below 3.199. The obvious recursive rule uses `2^m-1` colors and base exactly 2; the 6-color seed saves one color but supplies no scalable recurrence. Level 4 has order 32768; linear-in-level colors would be
spectacular, but the full constraint table is too large. Need derive recursive
color rule or bank after the 6-color harvest; do not promote this seed as
progress.

Wreath level 3/6 colors yields 97 coarse states `(color(a),color(b),swap)` for a
possible level-4 rule. A sampled three-million-product state hypergraph has no
one-state obstruction; min-conflicts reached one violation with 14 colors in
30 seconds, while 10 reached five. A longer 14-color run is active. This is
only a sampled necessary test: even a zero requires exhaustive generation and
an independent full verifier before any claim. Parameter warning: 14 colors on
order 32768 gives base 2.10, still fixed-scale; only a recursive color count
substantially below doubling would matter.

The sampled wreath level-4/14-color coarse-state run was harvested at one
violation and terminated. Since 14 colors would already decrease the base to
2.10, another nudge cannot meet the goal ladder. The wreath route is banked;
no level-4 construction or impossibility is claimed.

Affine groups `AGL(1,q)` were tested as factorial-ish/nonabelian alternatives.
Odd q with a multiplicative element of order 3 has an immediate inverse-orbit
obstruction `(a,0)^2=(a^2,0)=(a,0)^{-1}`; this kills q=7,13 and analogues.
Other primes give finite partitions only at fixed-scale parameters (e.g.
orders 110/6 and 272/8 in quick searches), with no increasing base. Binary
extension fields alternate the same order-3 obstruction for even extension
degree; q=8 gives order 56/5, while q=32 searches remain far from feasible.
Banked after the scaling test; no finite candidate promoted.

Odd-prime Heisenberg `UT(3,p)` avoids the exponent-3 obstruction when p>3.
Quick thresholds found order 125/6 colors for p=5 and order 343/8 for p=7;
a p=7/7-color run reached one violation and is extended. These bases are only
2.236 and 2.075. Color count appears about p, so order p^3 gives base tending
to 1, decisively the wrong scaling unless the 7-color anomaly generalizes.
One final bounded nudge is running; then bank.
The extended `UT(3,7)`/7-color run remained at one violation after nearly three
minutes and was terminated. No construction or impossibility. Since the known
p=5,7 threshold scale grows with p and bases decrease, odd-prime Heisenberg is
banked.

Linear correlated codes in binary Cayley complements were tested directly:
choose a sum-free difference set S and a linear message subspace in m
coordinates so every nonzero message has some coordinate in S. Targets with
formal bases 4--5.7 remained dozens/hundreds of uncovered differences; none
reached zero. The special affine-hyperplane S reduces rigorously to separating
all messages by linear functionals, requiring m>=message dimension and hence
base at most 2. General greedy S gave no candidate, so banked after one nudge.
A contemplated extra wreath level-4/10-color nudge was stopped before completion:
the sampled coarse generator itself dominates runtime and earlier 10-color work
already stopped at five violations. More importantly, a sampled rule would not
be independently verifiable without enumerating a group of order 32768. Budget
is redirected away from this constant-scale family.

An abstract universal lexicographic color-reuse rule was exhaustively SAT-tested:
map outer and inner color labels into a common palette while requiring safety
for every triangle-free input coloring. Mixed triangles force every outer label
to differ from every inner label, so exactly r+s colors are necessary. This is
also an immediate proof; universal post-composition cannot improve disjoint
palettes. Any successful recursion must use vertex/palette-dependent structure,
not a color-only quotient.

Quadratic-form difference coloring on F_q^2 was tested. For q=7 and 19 it is
triangle-free with q-1 colors, giving order q^2 and base tending to 1; other
primes tested fail. This is another fixed-scale anisotropy curiosity, banked.

Generalized the ternary warning: any inverse-closed product-free partition of a
group is impossible in the presence of any element of order 3, since g and
g^{-1}=g^2 share a class and g*g=g^2. This rigorously kills all group-difference
experiments with 3-torsion at once; symmetric/GL/alternating and many affine
families should not be revisited. Remaining 2-groups and p-groups p>3 were
already empirically fixed-scale.

Metacyclic 3-torsion-free groups `C_p semidirect C_q` were sampled after the
general obstruction. Verified finite partitions include orders/colors 55/5,
155/8,301/9, with bases 2.23,1.88,1.89. The decline is decisive; banked. These
finite seeds are independently checked but not promoted to proof_ramsey because
they have no benchmark value.

Tried dropping inverse-closure by canonically orienting each unordered edge via
lex order on `S_n` and coloring the relative permutation. This bypasses the
order-3 group obstruction in principle. Exhaustive tests found the raw
`(least moved i, displacement)` label valid through n=5 but it has
`binom(n,2)` colors; every O(n) compression tested (cyclic edge color, hash,
orientation) fails by n=4 with explicit triangles. Banked as another form of
the permutation-pair rigidity.

A generic rooted-word tree with completely node-dependent pair colors was
searched across q<=6,d<=4. Feasible points require colors scaling roughly with
d times the small alphabet threshold; no compression trend appears. Several
formal high-base targets (e.g. 81/3,256/4,216/3) remain dozens/hundreds of
violations. This subsumes another broad vertex-dependent recursion nudge and is
banked.

## Terminal adversarial audit

Caught and corrected one analytic constant: generalized shift graphs have two
looped constant binary patterns. Excluding them gives `chi_f<=10` uniformly,
not the previously stated `<=5`; bounded capacity and the route rejection remain
valid. Also corrected the unitriangular coordinate-order proof wording and
removed “threshold” language where only constructions plus uncertified SAT
UNSAT outputs existed. Full finite verifier sweep passes. No goal-ladder item is
achieved.
