# Oracle brief 1: choose and specify a PCP-free encoding

We need independently prove a deterministic polynomial-time reduction from 3SAT to binary NCP/syndrome decoding with an \(N^c\) gap (then lift to Euclidean CVP), without invoking PCP or unproved conjectures. Exact CVP hardness is known; PCP-based constant/almost-polynomial hardness is not useful here. The recent prohibited document named in the project instructions and all descriptions of it are off-limits: do not recall, search for, cite, or reconstruct from that source. Reason independently from classical concepts.

Three candidate routes:

1. **Exact syndrome gadget + tensor/direct product.** Encode SAT as minimum-cardinality representation of a target syndrome by columns. YES optimum \(k\), NO at least \(k+1\), then amplify. Obstacle: sparse representation/coset weight need not multiply under tensor product; cancellations and mixed decompositions may cheat. With only \(1+1/k\) base gap, logarithmic tensor power is insufficient unless one first obtains a constant base ratio.

2. **Low-degree evaluation encoding.** Encode a global assignment by low-degree evaluations; use polynomial identity distance for Booleanity, consistency, and clauses; concatenate to binary. Obstacle: honest evaluation words are dense (bad multiplicative distance baseline), nonlinear constraints do not naturally become one affine nearest-codeword instance, and proving global decoding may effectively require a PCP-like theorem from scratch.

3. **One-hot local views + deterministic consistency amplification.** Columns represent global literal choices and legal satisfying local clause views; target requires variable/clause coverage and consistency. Amplify inconsistency using expanders/dispersers, tuples, or hierarchy. Obstacle: check duplication scales YES cost too; enumerating growing tuples is superpolynomial; one bad clause has tiny density; GF(2) superposition/cancellation permits cheating.

Required answer: pick the most viable route (or give a clearly superior fourth route), but do not hand-wave to PCP/Label Cover. Specify a first candidate reduction precisely enough to implement on tiny formulas:

* exact field/ring;
* rows and columns (or generator/parity-check matrix) and target syndrome;
* mapping from satisfying assignments to a witness and its exact weight;
* intended NO lower bound and the invariant/lemma that would prove it;
* amplification operation, dimensions, threshold, and parameter choice yielding an explicit polynomial exponent while output remains polynomial;
* explicitly flag any unproved lemma and assess whether it is plausibly elementary or is secretly equivalent to the missing PCP-strength ingredient.

Please be adversarial. If all three routes as stated cannot plausibly achieve a polynomial gap, say so and identify the narrowest genuinely new lemma worth implementing/testing. Prefer a concrete falsifiable construction over a broad research program.

---

# Current brief after five consultations: exact failure map and next wall

The initial routes have now been implemented/attacked. Do not revive them without directly defeating the listed witness.

1. **GF(2) one-hot local views:** if a clause's forbidden view is `u`, three legal views `u+p,u+q,u+p+q` sum to `u`, giving exact zero residual at additive cost 2.
2. **Connected views through depth C log M:** an inconsistent 3-color permutation cycle encoded as bounded-occurrence exact 3CNF has, for every depth d<n, exact GF(2) marginals obtained by summing its three tree colorings. Their support is at most 3K. This is a proved scalable counterexample.
3. **Residual error-correcting code / huge constraint scaling:** exact alternative representations have residual zero. If unrestricted integer feasibility of the scaled equations separated SAT, Smith/Hermite normal form would decide it; otherwise soundness already has to hold inside the exact affine fiber.
4. **Characteristic 3 exact-one:** Boolean weight N is sound, but a false selected literal is repaired by auxiliary value 2=-1, represented with two pair coordinates. The all-eight-clause UNSAT core has an explicit exact witness of weight N+1 (N=51 in code).
5. **Explicit pointed tensor powers:** pointed distance really is multiplicative, but the approximation exponent relative to final length is `log(1+1/(K+1))/log(N+1)`, independent of tensor order.
6. **Fixed coordinate-sampled tensor compression:** a proved minimax lemma defeats any one code-oblivious sample that must preserve all adjacent one-dimensional support layers. It does not exclude code-dependent sampling.
7. **New dense-fold finite attack:** for `D=span{(1,1,0),(1,0,1)}` with pointed distance 2, `D tensor D` has pointed distance 4. Folding the 9 tensor coordinates to six unordered-pair coordinates by XORing permutation orbits drops pointed distance to 2; both pure squares also have weight 2. Among 200 deterministic random dense maps to six outputs preserving the all-star coordinate, exact enumeration found pointed distances `{1:52,2:118,3:28,4:2}`. In examples, arbitrary tensor combinations had weight 1 or 2 while every pure pointed square had weight at least 3. Script: `experiments/verify_dense_fold_attack.py`.
8. **Characteristic-independent affine parallelogram:** for any affine signature `g(x)=Mx+c` on Boolean local views, flip two coordinates of a forbidden `u` to obtain three other views `a,b,c'` with `g(a)+g(b)-g(c')=g(u)` over integers and every modulus. Hence integer coefficients `(1,1,-1)` exactly simulate the forbidden column at squared coefficient norm 3. Huge residual weights still see zero. Script: `experiments/verify_affine_parallelogram.py`.

The exact remaining tensor question is **code-dependent dense structured folding**, with soundness against every linear combination, not pure tensors. The exact remaining algebraic question is a sparse-YES low-degree encoding whose integrality test does not merely reintroduce local affine pseudoassignments.

For the next consultation, give ONE candidate only, precise enough to code. Preferred deliverable:

* either a code-dependent dense folding `F_G: D^{tensor q}->F_2^m` whose image generator is computable in poly(size(G),q,m) without expanding rank^q, together with a pointed-distance conjecture and the smallest hostile test;
* or a low-degree/evaluation NCP matrix with sparse completeness witness and an explicit integral-decoding statement.

Before recommending it, attack it on the 2-dimensional code above, the all-eight-clause core, and the odd 3-color holonomy. Explain exactly why orbit XOR/Frobenius cancellation and mixed tensors do not reproduce the recorded cheats. If no candidate survives, prove the narrowest new no-go theorem rather than giving a survey. The prohibited recent document and every description of it remain completely off-limits.

## Consultation 6 outcome (acted on)

No candidate survived. The oracle proved the bounded-degree extension of item 8: every degree-d polynomial signature on a Boolean local view with at least d+1 independently flippable bits has an alternating `(d+1)`-cube relation. A forbidden view is represented by the other `2^(d+1)-1` cube vertices with coefficients +/-1; this survives arbitrary linear mixing, every modulus, and dense linear folding after tensoring. For a 3-bit quadratic signature the all-eight-clause core replaces its one forbidden view by all seven legal views at constant extra norm/support. Full-degree local truth tables evade finite differences but not the already-proved odd-holonomy full-marginal pseudoassignment on scopes smaller than the cycle. Implemented and passed 400 exact instances in `experiments/verify_finite_difference.py`; theorem added to `proof_cvp.md`.

**Exact failure conclusion:** bounded-degree nonlinear local evaluation followed by any linear NCP/lattice processing is dead for polynomial gaps. Any next candidate must use genuinely global columns/signatures, not a relabeling of bounded local views. Do not ask the oracle again until such a global candidate has an explicit matrix and has survived a finite low-weight search.

## Subsequent code-first attacks (no new oracle call)

* Pure-power tensor subcodes retain exact pointed distance and symmetric representative puncturing retains at least a `1/q!` fraction, but length `binom(L+q-1,q)` forces bounded q for polynomial output. This is a proved positive lemma with useless parameters.
* Code-dependent puncturing of the tiny code `span{110,101}` cannot delete even one of its 9 tensor-square coordinates while preserving pointed distance 4. Random tiny codes vary, so no asymptotic theorem is claimed.
* Phase-lifted legal clause views were searched exactly: columns are indexed by `(view,z)` and place their three incidence ones at view-dependent shifted phases. Across deterministic random q=2,3,4 signatures every feasible forbidden phase boundary still has a three-column trade. Exhausting all separable signatures for q=2 (64 cases) and q=3 (729 cases) gives the same result. Larger-q MITM finds random signatures with no trade through support 5, but end-to-end completeness breaks: on a satisfiable two-clause formula only 23/30 q=2 and 14/30 q=3 random signatures admit any lifted satisfying assignment. The obvious completeness-preserving coboundaries `alpha=beta(i,b)-gamma(j,a)` gauge-transform to zero phase and restore the original cheat. Scripts: `verify_phase_clause_gadget.py`, `verify_phase_lift_completeness.py`.

## Exact conceptual wall for consultation 7

This phase tradeoff is the first local construction tested here that sometimes has no repair through support five, so analyze it narrowly rather than proposing another route.

The base incidence equations for a selected Boolean assignment `b` are
`y_{i(j,r),b_i} = z_j + alpha_{j,b|C_j,r} (mod q)`.
Random `alpha` can have local girth but creates assignment-dependent holonomy and loses completeness. Coboundary alpha preserves completeness but is gauge-trivial.

Give exactly one of:

(A) a theorem classifying phase systems that preserve a lift for every satisfying assignment of every transformed 3CNF, showing they are gauge-trivial (state precise transformation assumptions); or
(B) an explicit polynomial-time SAT-preserving transformation with auxiliary selector variables/phases such that every satisfying assignment has some phase lift, while the all-eight-clause UNSAT core and odd holonomy require phase-trade support q^Omega(1). Specify the exact columns and prove/clearly isolate soundness; or
(C) a precise selector-augmentation candidate plus the smallest end-to-end exhaustive experiment likely to kill it.

Attack the obvious failure: if selectors allow arbitrary occurrence phase triples, the old three-column legal-view trade returns. Also attack GF(2) sums of several selector choices and odd group orbit sums. Do not appeal to PCP/Label Cover. The prohibited recent document and all descriptions remain off-limits.

## Consultation 7 outcome (acted on)

Option A was proved under explicit copy-stable locality, cycle-realization, universal-assignment-completeness, and single-valued selector-interface assumptions. Every alternating type cycle must have zero phase holonomy; spanning-forest potentials imply `alpha=beta-gamma`; gauge removal restores the support-three forbidden-view trade and the all-eight-clause weight-13 witness. Implemented in `verify_phase_cocycle.py` (400 recovered coboundaries over q=2,3,5,8 and explicit trade checks) and added to `proof_cvp.md`.

This closes fixed local phase systems under the stated assumptions. The only phase escape is globally cycle-dependent selector behavior, which is no longer a bounded local gadget and must itself defeat GF(2) selector superpositions. No further oracle call is justified without an explicit global-selector matrix.

## Further exact failures after consultation 7

* Random/disconnected proper scopes do not defeat the odd 3-color cycle if overlaps enforce only unary marginals. Every forest scope has a support-three sum of global color translates whose unary marginal is all three colors at every vertex, independent of scope. Higher-order overlap consistency is necessary.
* Degree 3 is the sharp local threshold for a 3-clause: the cubic violation indicator separates the forbidden view, but its nonzero third mixed difference means it cannot be assembled from unary variable interfaces. This pinpoints the nonlinear joint-consistency wall.
* Direct integer CVP scaling was implemented with equation weight 10^6. A false clause has an exact slack repair at additive squared cost 2, and padding drives the ratio to one. More generally, affine count slack obeys `w0=2w1-w2`; degree-d count dependence extrapolates count zero from 1..d+1 with binomial coefficient l1 sum `2^(d+1)-1`. All are exact-fiber cheats.

All corresponding `verify_*.py` scripts pass. These failures leave only genuinely joint/global consistency. The next consultation, if any, must supply an explicit global matrix; local gadget variants are exhausted enough to not justify more oracle budget.

## Global controlled-permutation candidate also failed

A global Boolean branch bit was made to control one of two permutations on every edge of a q-state cycle. Both fixed branch products were required to be fixed-point-free. The explicit GF(2) NCP had one-hot-odd coverage and marginal consistency among the global branch, edge `(branch,state)` factors, and state variables. For cycle length 3 and random q=3,4,5 examples, reported optimum was always 9, independent of q. An explicit q=3 weight-9 syndrome witness was checked exactly: at one edge, three factor columns with mixed branch/state values splice incompatible trajectories while preserving all marginals. Thus even globally shared branch control is not integral under binary marginal equations; local superposition returns.

This is now in `verify_controlled_permutation_cycle.py`. Any next candidate must enforce integrality of global branching choices against arbitrary GF(2) factor superpositions, not merely share their unary marginal.

## Exact marginal-kernel diagnosis

The splice is universal, not specific to permutations. Unary GF(2) marginalization has every 2x2 rectangle in its kernel, allowing a singleton joint table to toggle to support three unchanged. More generally, on a k-bit joint table the sum of all 2^k cube vertices vanishes under every marginal of arity less than k (each fixed proper assignment has an even number of extensions). Therefore bounded-order overlap consistency necessarily retains parity-cube cheats; only full-arity information removes this universal kernel. Scripts `verify_mod2_marginal_nonintegrality.py` and `verify_pairwise_marginal_kernel.py` pass.

This strengthens the requirement on any future global matrix: its constraints must not factor through bounded-order marginals on a growing joint object. No further oracle call until a candidate meets this criterion.

## First positive finite signal: random scopes with full intersection marginals

Unlike unary random scopes, a hierarchy built from random disconnected edge subsets, closed under intersections, with exact marginals on every scope inclusion, often detects the inconsistent 3-color holonomy cycle. Exact GF(2) elimination for n=5..10 shows all 30 deterministic trials with `2n` random scopes of 3 edges are infeasible; sparser and 2-edge systems often remain feasible. Script: `verify_disconnected_scope_threshold.py`.

This is not yet a candidate reduction: (i) scope groups enumerate all satisfying colorings; (ii) no polynomial Hamming gap, only exact infeasibility; (iii) an outer residual code helps only after proving every exact pseudoassignment is eliminated. But it is the only completed experiment suggesting higher-order **nonlocal** overlaps can beat odd holonomy.

That next task is now implemented for arbitrary small CNFs. Construction: include every singleton clause and `O(m)` random subsets of `d` clauses; each group has columns for all satisfying assignments to its full variable union; every pair of groups has GF(2) marginal-equality rows for every assignment to all shared variables. SAT completeness is canonical. Exact elimination gives infeasible fibers on 20/20 all-eight-clause, 20/20 inconsistent XOR-cycle, and 10/10 K4 Tseitin trials (`verify_random_scope_3sat.py`).

This was attacked on the scalable padded 3-color cycle. Sparse constant-size scopes fail: exact fibers survive at tested `(cycle n, clauses/scope d)=(3,2),(4,2),(4,3),(5,3)`, with explicit elimination witnesses. Increasing density/arity sometimes kills them (n=4,d=3 with two random scopes per clause; n=4,d=4). Script: `verify_random_scope_padded_cycle.py`.

So even the only positive direction has a threshold problem: constant sparse scopes do not beat scalable odd holonomy, while growing scopes/density risk output explosion and may merely rebuild global consistency. This is confirmed more cleanly on unpadded cycles: with full shared-variable marginals and `2n` random 3-edge scopes, exact fibers survive in 3/3 trials at n=24 and n=30 (`verify_random_scope_edge_full.py`), despite many smaller instances being killed.

A deterministic polynomial family now meets the cycle test: include all singleton edge scopes and **all pairs of edge constraints**, with full shared-variable marginals. Exact fibers are infeasible for every tested inconsistent 3-color cycle n=6,8,10,12,16,20,24,30,40. There are O(n^2) groups and at most 9 views per pair (`verify_all_d_scope_edge.py`).

The all-pairs hierarchy has now been attacked on several scalable structured CSP families and still survives: exact fibers are infeasible for 3-color cycles through n=40, XOR cycles through length 15, cubic Tseitin through 8 graph vertices/32 clauses, non-3-colorable K4 and odd wheels, and non-4-colorable K5. All are exact GF(2) elimination (`verify_all_pair_cnf.py`, `verify_all_pair_coloring.py`).

This is now strong enough for one narrowly targeted oracle consultation after recording the exact construction:

* groups: every singleton constraint and every unordered pair of constraints;
* columns: every satisfying assignment to the full union of variables in the group;
* target: odd coverage in every group;
* rows: for every pair of groups and every assignment to all shared variables, equality of GF(2) marginals.

SAT completeness is one global assignment restricted to each group. Question: does every exact pseudoassignment imply a global satisfying assignment? If false, produce the smallest explicit bounded-arity UNSAT counterexample and pseudoassignment. If true only under an acyclicity/Helly condition, state it precisely. Do not confuse exact infeasibility with a Hamming gap: even a universal exactness theorem still needs residual-code amplification and YES-baseline accounting.

## Consultation 8 outcome (acted on): all-pairs is dead

The oracle gave an explicit charged GF(3) incidence CSP on the Petersen graph. Ten cubic vertex equations have total charge one, hence are UNSAT. For every singleton/pair vertex group, select all affine solutions. Counts are 9,27,81 (odd), total support 2925. Girth five implies any row combination supported on a group intersection comes only from common vertex equations, so projected solution spaces and their GF(2) all-ones marginals agree. The residual is exactly zero.

Implemented matrix: 55 groups, 2925 columns, 23680 rows. `verify_petersen_pair_counterexample.py` checks the all-ones target exactly, checks the UNSAT charge certificate, and exact elimination finds another support-367 fiber point. Proof added to `proof_cvp.md`. Trit-to-two-bit encoding gives Boolean arity six. Thus residual coding cannot help and all-pairs/full-intersection hierarchy is conclusively refuted.

No candidate remains. Any higher-k scope hierarchy should first be attacked by analogous high-girth charged incidence CSPs, where all affine solution counts stay odd and local projection supports may agree below the graph's dependency size.

## Continuation failure recorded before any further consultation: global CRT coupling

The run had no unfinished background experiment to harvest. I implemented a new genuinely global integer candidate before considering another oracle call. All Boolean bits are residues of one coefficient `X` modulo distinct odd primes: `X-p_i q_i-b_i=0`. Clause rows enforce `literal_count+s+2t=4`; centered identity rows charge bits/slacks, and one row centers `X` at half the CRT modulus product. The matrix has full column rank by its private identity, global-X, and quotient pivots, so its columns are an explicit integer lattice basis.

This fails on the all-eight-clause core plus disjoint satisfiable padding. Set the core to `000` and padding bits to one. The unique false clause uses `(s,t)=(0,2)`. Every scaled CRT/clause row is then exact, and the false clause costs only additive squared distance 8, independent of all scales and CRT primes. A uniform YES threshold must accommodate the global CRT coordinate and can be taken as `R^2=P^2+n+2m`; the explicit NO point lies within squared radius `R^2+8`. Thus the ratio tends to one, even faster because `P` is huge. `experiments/verify_crt_global_coupling.py` passes exact checks.

Do not recommend global assignment hashing/CRT alone in a future consultation. The precise unresolved requirement is stronger: clause validity itself must become a genuinely global, non-affine norm condition with a nonempty YES fiber, while defeating integer affine extrapolations and all low-weight superpositions.

## Consultation 9 outcome, implemented

Consultation 9 supplied a sharp no-go rather than a surviving construction. Any polynomial-size bounded-fan-in Boolean/arithmetic circuit tableau whose legal gate columns communicate only through affine coverage/wire-value rows has an exact support-three OR fault:
`(coverage,0,0,1)=(1,0,1,1)+(1,1,0,1)-(1,1,1,1)` over integers, with the analogous all-plus identity mod 2. Therefore a false OR output can be changed to true at additive support/squared-norm cost two, and arbitrary row scaling, dense row mixing, or residual coding preserves the equality.

I implemented the full all-eight-clause circuit, not just the local identity: 30 blocks, 108 columns, 82 rows. For assignment `000`, fault the second OR in the false clause and use an ordinary accepting transcript downstream. Exact checks give binary syndrome weight 32 and integer squared norm 32 versus block baseline 30. An exhaustive specialized enumeration of every support-32 binary form (one three-column exceptional block, singleton columns elsewhere, all eight source assignments) finds 48 accepting faults. Deterministic dense row maps preserve both exact residuals. `verify_circuit_tableau_fault.py` passes.

**New exact failure boundary:** computing a global high-degree predicate by a compact determinant/resultant/arithmetic circuit does not help if its tableau is linearized by bounded-fan-in local truth tables and affine wire interfaces. Any future candidate must expose genuinely global assignment-dependent rows that do not factor through those interfaces.

A follow-up exact attack closes the obvious integer full-truth-table variant. Use all seven legal views per 3-clause, integer coverage one, and integer unary marginal equality to global variable columns. For the unique forbidden assignment `u`, three legal views obtained by flipping two bits satisfy `a+b-c=u` and coefficient sum one. Hence coefficients `+1,+1,-1` preserve every row exactly. On the all-eight core this gives support and squared norm 13 in the explicit 59-by-62 system, for every global assignment. Dense row maps and moduli preserve the residual zero (`verify_truth_table_marginal_integer.py`). Full local degree helps only before affine projection to interfaces; the interface reintroduces the parallelogram.

A scalable integer hierarchy attack also survives: split a five-symbol permutation alphabet into invariant orbits of sizes two and three. On every proper cycle-path scope, assign coefficient `-1` to each 2-orbit coloring and `+1` to each 3-orbit coloring. This signed local table has mass `3-2=1`, consistent restriction marginals, and squared norm `5K`; the globally twisted cycle is UNSAT. Exact checks are in `verify_integer_mixed_orbit_cycle.py`. An explicit bounded-occurrence exact-3CNF encoding with one-hot states, padded implications, and canonical chain auxiliaries preserves the construction; it has `43n` clauses, `27n` variables, maximum occurrence 17, signed squared norm at most `25K`, and all deletion marginals pass at `(n,d)=(3,1),(4,2)` in `verify_integer_mixed_orbit_3cnf.py`. Thus characteristic zero does not cure the holonomy pseudoassignment even on exact 3CNF.

The integer full-intersection escape is also dead. On the Petersen charged-flow CSP, combine an inconsistent F2 branch and inconsistent F3 branch. Give them fixed signed total masses `-80` and `81`; each singleton/pair local affine-space size divides its branch mass (`4,8,16` and `9,27,81`). Uniform integral local tables then have combined mass one and exactly matching full-intersection marginals, while neither branch has a global solution. The explicit integer matrix is 30550-by-3565 with squared-norm-53365 exact witness (`verify_integer_petersen_pair_counterexample.py`). Disjoint unions give support/group and squared-norm/group ratios tending to 97 and 481 (`verify_integer_petersen_family.py`). This is the global/all-pairs analogue of the mixed 2/3-orbit cheat.

## Consultation 10 outcome, implemented

The requested global-row route was narrowed to a sharp Walsh no-go. Give each forbidden group all complete assignments except its unique forbidden one, and require equality of selected dense Walsh moments across groups. If any nonconstant character `T0` is omitted over the integers, Walsh orthogonality gives an exact unit-coefficient virtual assignment of support/squared norm `2q-2` versus group baseline `q`. If all characters are included, exactness returns but needs `2^n` rows. Over GF(2), even all parity characters leave the all-plus `2q-2` witness because every parity has even global weight. The n=3 implementation has 56 columns; it checks all 56 omitted-character/anchor integer witnesses, all 8 complete-parity binary witnesses, dense row maps, and exact full-Walsh infeasibility ranks 56/57 (`verify_walsh_global_moments.py`).

**Failure boundary:** genuinely global Fourier rows do not avoid virtual measures unless the complete exponential character basis is materialized; over GF(2), parity moments remain degenerate even when complete. This does not cover arbitrary non-character dense rows.

Over every fixed prime field, a stronger basis-independent theorem covers **arbitrary** global features: the q augmented vectors `(1,f_1(x),...,f_m(x))` are dependent whenever `q>m+1`. Anchoring any dependence gives an exact all-forbidden-core witness with at most `q+m` nonzeros. Therefore exactness requires at least `q-1=2^n-1` arbitrary global rows, with no locality or bounded-entry hypothesis. The model itself also uses `q(q-1)` complete-assignment columns, so this is an obstruction analysis, not an efficient reduction. Binary checks cover 150 systems through `m=q-2`; further exact checks cover p=2,3,5,7 (`verify_arbitrary_binary_global_fingerprints.py`, `verify_arbitrary_prime_global_fingerprints.py`).

A counting attack covers arbitrary bounded integer fingerprints. For q assignments and m rows in [-H,H], augmented subset sums occupy at most `(q+1)(2qH+1)^m` bins. If `2^q` exceeds this, two subsets collide; their {-1,0,1} difference yields an exact exceptional virtual assignment of support/squared norm at most `2q-2`. If q=2^n and both m and log H are polynomial in n, the collision inequality holds asymptotically, so this actually rules out arbitrary polynomial-count, polynomial-bit integer fingerprints in the full-assignment/all-forbidden model. Twenty exact q=20,m=2,H=2 tests pass in `verify_bounded_global_fingerprint_collision.py`. It does not cover different column models or make the exponentially large global-table construction efficient.

I next attacked global **univariate polynomial moments**, encoding all assignments injectively as `0..q-1`. Equality of moments through degree `d<=q-2` has the exact finite-difference exceptional table `delta_0=sum_{j=1}^{d+1}(-1)^{j+1} C(d+1,j) delta_j`. Its total witness support is `q+d`; full degree `q-1` is exact but needs `q=2^n` moments. For q=8 all degrees and full-rank infeasibility pass in `verify_univariate_global_moments.py`. This closes the obvious non-character algebraic fingerprint: low degree has signed extrapolation, while interpolation-complete degree explicitly costs exponential rows.

No further oracle call is justified before a different explicit global-functional family is specified and attacked.
