# Attack log: PCP-free polynomial-factor hardness for Euclidean CVP

## Problem restatement

Construct, from a 3CNF formula \(\Phi\), in deterministic polynomial time an explicit integer basis \(B\), integer target \(t\), and threshold \(R\) such that

* if \(\Phi\) is satisfiable then \(\operatorname{dist}_2(t,L(B))\le R\);
* if \(\Phi\) is unsatisfiable then \(\operatorname{dist}_2(t,L(B))>n^cR\), where \(n=\operatorname{rank}L(B)\) and one fixed absolute \(c>0\) works for all sufficiently large instances.

The preferred intermediate target is binary nearest codeword/syndrome decoding: produce \((H,s,k)\) with a weight-\(\le k\) solution to \(He=s\) in the YES case and no solution of weight \(\le N^c k\) in the NO case. The final construction must be a many-one reduction, have polynomial output size, and include all promise thresholds and constants.

## Classical landscape and constraints

Exact CVP is NP-hard (van Emde Boas, 1981). Constant-factor and \(n^{c/\log\log n}\)-factor hardness are classical, but the cited routes use PCP machinery (ABSS 1997; DKRS 2003). Polynomial-factor hardness was classically conditional on Projection Games. Thus simply citing gap-CSP/Label Cover, parallel repetition, PCP, or a known constant-gap CVP/NCP reduction does not advance this task. The work must independently prove every amplification/encoding lemma it uses.

A standard mod-2 Construction-A style passage from an appropriate binary code/coset to a lattice is plausible, but it is not automatic for a polynomial gap: integer lifts can use even-coordinate corrections, Euclidean norm is the square root of Hamming weight on binary representatives, and the lattice rank/output dimension changes the exponent. These details are deferred until a genuine NCP gap is obtained.

## Candidate encoding strategies

### Strategy A: exact syndrome encoding followed by an explicitly proved tensor/direct-product amplifier

**Encoding.** Begin with a parsimonious exact reduction from 3SAT to a sparse affine binary system or syndrome instance \(H e=s\). Variable gadgets force one of two literal columns; clause gadgets admit a bounded number of columns exactly when a selected literal satisfies the clause. A satisfying assignment gives a canonical error vector of weight \(k\); an unsatisfying formula has minimum weight at least \(k+1\).

**Possible gap source.** Take \(q\) tensor/direct-product powers. View syndrome decoding as representing \(s\) by a minimum number of columns of \(H\). Replace the dictionary by product columns of \(H^{\otimes q}\) and target by \(s^{\otimes q}\). The canonical YES representation has size \(k^q\). If representation length multiplied under this product, the NO optimum would be at least \((k+1)^q\), yielding ratio \((1+1/k)^q\). Choosing \(q\) polynomially related to the input could yield a polynomial ratio only if output size remains polynomial (so usually \(q=O(\log m)\)), which in turn requires a base constant ratio rather than \(1+1/k\). A stronger base normalization or block product would be needed.

**Central danger.** Minimum dictionary representation (and affine-coset Hamming weight) is not known to be multiplicative under tensoring: mixed tensor columns and cancellations can create low-weight decompositions. Proving a robust direct-product lemma is the entire strategy, not a routine step. Naive repetition only scales both YES and NO distances equally.

### Strategy B: low-degree evaluation encoding with a global algebraic consistency test proved from scratch

**Encoding.** Arithmetize the Boolean assignment over a finite field. Encode a table of its multilinear/low-degree extension by evaluations on a grid or affine space, then binary-concatenate field symbols. Add linear coordinates for (i) Booleanity, (ii) consistency of restrictions, and (iii) clause-polynomial identities. Reed--Muller/Reed--Solomon distance can turn one failed polynomial identity into disagreement on a constant or inverse-polynomial fraction of a large evaluation domain.

**Possible gap source.** If every low-weight word near the affine target decodes to one global low-degree assignment, then an unsatisfiable formula forces many nonzero evaluation coordinates. Choosing field size and degree with constant relative distance, and then concatenating with a binary code, could create \(N^c\) separation between a sparse canonical YES witness and all NO witnesses. Tensoring the evaluation domain might further amplify distance while keeping a succinct generator matrix.

**Central dangers.** Evaluation encodings are dense, so the YES distance may already be a constant fraction of block length, leaving no polynomial multiplicative gap. More seriously, turning nonlinear identities into one affine nearest-codeword instance without allowing arbitrary linear combinations to cheat is difficult. A proof of global consistency/local test soundness may amount to rebuilding a PCP; that is allowed only if fully proved directly, but a constant-rate constant-query construction would effectively solve the hard part rather than bypass it.

### Strategy C: sparse superposition/set-system encoding plus deterministic consistency amplification

**Encoding.** Use one-hot blocks for variables (choose exactly one of \(x_i,\neg x_i\)) and local one-hot blocks for satisfying assignments to clauses. Linear consistency coordinates identify each local occurrence with the global variable choice. Equivalently, columns represent legal local views, and a sparse sum must cover prescribed variable/clause coordinates. This gives a transparent exact NCP/set-cover-like gadget and is ideal for exhaustive testing.

**Possible gap source.** Replace each variable occurrence by many structured consistency checks indexed by a lossless expander/disperser, or encode all \(r\)-tuples of clause views. A globally inconsistent collection should violate many checks; an unsatisfiable global assignment should fail every amplified tuple containing a bad clause. If tuples can be generated by expander walks, the output may stay polynomial while the fraction/number of forced violations grows. A hierarchical composition could make the canonical YES vector sparse while forcing polynomially more columns in the NO case.

**Central dangers.** Merely duplicating checks multiplies YES and NO costs together. Full \(r\)-tuple enumeration has size \(M^r\), superpolynomial for growing \(r\). Expander-walk amplification from a single bad clause gives only roughly \(r/M\) rejection, not a constant, unless a gap already exists. Most importantly, linear superposition permits cancellation and fractional/local cheating absent from ordinary CSP reasoning. The code must make consistency violations costly without making honest encoding equally costly.

## Initial choice criterion

Strategy C offers the most concrete base implementation and adversarial tests. Strategy A offers the cleanest conceivable amplifier if a valid multiplicativity lemma exists, but that lemma is suspect. Strategy B has the strongest algebraic distance mechanism but the hardest sparsity/linearity interface. The first oracle consultation should choose one route only after confronting these exact bottlenecks, and should specify matrices/columns, target, thresholds, dimensions, and a candidate soundness invariant precise enough to code.

## Oracle consultation 1 outcome

The oracle selected Strategy C and made the base one-hot syndrome gadget explicit. It also identified a fatal affine-superposition attack: if a clause's unique falsifying local view is \(u\), then for independent nonzero \(p,q\in\mathbb F_2^3\), the three satisfying views \(u+p,u+q,u+p+q\) sum to \(u\). Thus a violated clause can be represented by three legal clause columns rather than one, at additive cost 2, with **zero** syndrome residual. No linear error-correcting encoding of residual rows repairs this.

Its next falsifiable candidate is a hierarchy containing columns for satisfying assignments to every connected set \(Q\) of at most \(d\) clauses, with odd coverage and mod-2 marginal consistency under one-clause deletions. A satisfying global assignment selects one view per scope. The missing lemma would say that for \(d=C\log M\), every exact mod-2 pseudoassignment for an unsatisfiable bounded-degree formula has polynomially larger total support. The oracle explicitly warned that this lemma is the entire PCP-strength bottleneck and is plausibly false. We will implement and attack it, beginning with the all-eight-clauses minimally unsatisfiable formula and parity-derived families.

The oracle also supplied a valid conditional residual-code amplifier and an exact Construction-A identity \(\operatorname{dist}_2(v,\Lambda_H)^2=\min\{|e|:He=t\}\). These are useful only if the hierarchy lemma survives; they do not constitute goal (a).

## Connected-view experiment 1

Implemented the hierarchy over GF(2), exact row-span feasibility, and minimum-support MILP. Results:

* all eight 3-clauses on three variables: depth 1 optimum 8; depth 2 exact fiber infeasible;
* inconsistent XOR cycles encoded as 2-clauses: depth 2 exact fiber infeasible for tested lengths 3, 5, 7;
* K4 Tseitin contradiction encoded by four 3-clauses per vertex: depth 2 exact fiber infeasible;
* a fixed UNSAT 4-variable/14-clause instance has an exact depth-2 fiber with \(K=105\); HiGHS reported minimum support 243. At depth 3, exact GF(2) elimination found the fiber infeasible.

Thus pairwise connected views do not globally glue over GF(2), but small dense contradictions are exposed by triples. This says nothing asymptotic about \(d=C\log M\). The next conceptual wall is to construct scalable high-girth formulas carrying low-support mod-2 pseudoassignments through logarithmic depth, or prove why connected subsets of that depth force polynomial support.

## Oracle consultation 2 and decisive counterfamily

The oracle found an explicit refutation of the logarithmic connected-view lemma. Put a 3-color permutation constraint on a cycle: identity on every edge except one fixed-point-free shift. Encode colors one-hot in exact 3CNF, padding every binary clause with a private variable. The result has 19n clauses, 12n variables, bounded occurrence, and is globally unsatisfiable by nontrivial holonomy.

Every connected set of fewer than n clauses has a tree skeleton. Sum, over GF(2), the three propagated colorings of that tree, setting padding variables to zero. Because the alphabet has odd size, this local measure has odd mass; because restriction between permutation trees bijects their three colorings, all marginals agree exactly; support is at most three per scope. Hence for every d<n the exact hierarchy has weight at most 3K. In particular d=C log M never yields a polynomial factor. The complete proof is now in `proof_cvp.md`, and the generated finite checks pass for n=3,d=1 and n=4,d=2.

This is a decisive negative result for Strategy C, not progress on the requested hardness ladder. It also clarifies the structural barrier: GF(2) affine systems cannot distinguish odd-cardinality locally consistent orbit sums from a single integral assignment until the global obstruction enters one scope.

## Oracle consultation 3: characteristic 3 and the scaling obstruction

The oracle proposed and then refuted a genuinely different ternary encoding. A clause is converted to four Boolean exact-one relations using selectors. Over GF(3), exact-one is one linear equation because a Boolean sum of three bits equals 1 mod 3 iff it equals 1. Pair columns encode each variable value. Weight N solutions are exactly Boolean, so SAT gives N and UNSAT gives at least N+1. Construction A gives an exact Euclidean squared-distance identity.

The mathematical threshold argument gives UNSAT weight at least N+1, while the all-eight-clauses core has an explicit ternary solution of weight N+1: at its sole false clause, one auxiliary takes value 2=-1, whose pair representation uses two nonzeros instead of one. The implementation has N=51 and rank 102; HiGHS also reports optimum 52 (a sanity check, not a proof certificate).

General lesson: over any field, if linear local witnesses w0,w1 cheaply encode interface values 0,1 with the same internal target, then (1-lambda)w0+lambda w1 cheaply encodes every field value lambda, with support contained in the union. Changing/multiplying characteristics kills particular orbit sums but not affine extrapolation.

The oracle also resolved the tempting scaling argument. If a block of exact linear integer constraints is infeasible exactly iff SAT is false, Smith/Hermite normal form decides SAT. If its exact fiber remains nonempty in NO cases, scaling residual rows does nothing to those points; one already needs to prove every NO exact-fiber point has huge norm, which is the original problem. Moreover, two nearby exact Boolean branches generate nearby integer affine extrapolations such as 2z0-z1.

## New observation: pointed tensor multiplicativity, but bad size accounting

For an affine binary coset t+C, homogenize to the pointed linear code D=span((C,0),(t,1)). Let delta be the minimum weight of a D-word whose distinguished coordinate is 1. In D tensor D, any word with distinguished pair-coordinate 1 has at least delta nonzero entries in its distinguished row; each corresponding column is itself a pointed word and has weight at least delta. Hence pointed distance is exactly delta squared, and by induction delta^q. This is a clean exact product lemma.

It still does not amplify an additive K versus K+1 reduction in polynomial size: D^{tensor q} has length (N+1)^q, while ratio is only (1+1/(K+1))^q. A polynomial ratio requires q on the order of K log N, far beyond polynomial output. The next question is whether this product can be compressed between levels without invoking a PCP-strength theorem, or combined with a base reduction having much smaller YES distance.

## Oracle consultation 4: sampled tensor compression is dead

The strongest directly explicit compression considered is to retain polynomially many tensor coordinates and compute their image generator iteratively via Schur products and row reduction. The oracle proved a lower bound already for one-dimensional pointed codes. A sampled tensor coordinate corresponds to a subset T of base support positions and evaluates 1 exactly when T is contained in support Z. For one fixed sample of m subsets, comparing all supports of sizes d-1 and d, if m(d/N)^s<1 then the worst NO/best YES ratio is at most d/(d-s+1). Thus a strict uniform ratio >R requires m >= (N/d)^{floor(d+1-d/R)} (with the corrected ceiling-minus-one exponent for >=R). When N/d is bounded above 1 and d=K+1, even factor 2 needs exponentially many coordinates in K.

This rigorously kills any **fixed/code-oblivious** coordinate sample required to work uniformly over all one-dimensional support codes. It does not exclude choosing a different sample after inspecting each input code. Mixed tensors also cheat more than pure powers: for D=span{(1,1,0),(1,0,1)}, upper-triangular coordinates of D tensor D have pointed distance 2, not the pure-square heuristic 3.

The lower bound also does not cover arbitrary dense linear functionals on tensor space. Such a functional can distinguish adjacent pure Hamming layers (e.g. an elementary symmetric polynomial), but no explicit polynomial image generator or soundness against arbitrary tensor combinations is available. Code-dependent sampling and dense folding are tensor-compression classes not refuted here.

## Dense-fold attack after continuation

Implemented exact GF(2) enumeration for the smallest nontrivial pointed code `D=span{(1,1,0),(1,0,1)}`, whose pointed distance is 2 and whose full tensor square has pointed distance 4. The most canonical dense compression—XOR all coordinates in each permutation orbit `(i,j)~(j,i)`, retaining six unordered-pair outputs—drops pointed distance to 2. It does not even preserve pure squares: both pointed pure squares map to weight 2. Thus naive symmetric coinvariants are dead in characteristic 2.

For 200 deterministic random dense 9-to-6 linear maps that preserve the all-star coordinate, exhaustive enumeration produced image pointed distances `{1:52, 2:118, 3:28, 4:2}`. In explicit cases an arbitrary tensor combination had weight 1 or 2 although every pure pointed square had weight at least 3. This is finite evidence only, but it reinforces that testing pure powers is unsound. `experiments/verify_dense_fold_attack.py` reproduces every number.

A parallel subagent advisory attempt failed before execution (`spawn pi ENOENT`), so it yielded no mathematical evidence and is not used.

A further characteristic-independent obstruction closes the obvious integer-lattice variant. Any affine signature of Boolean local views obeys a parallelogram identity: flipping two coordinates of forbidden `u` gives allowed `a,b,c` with `g(a)+g(b)-g(c)=g(u)` over the integers and every modulus. Integer lattice coefficients `(1,1,-1)` therefore simulate the forbidden view exactly at squared norm 3. Scaling all consistency/residual coordinates still sees zero. This is now proved in `proof_cvp.md` and checked by `verify_affine_parallelogram.py`.

## Oracle consultation 6: bounded-degree nonlinear signatures also fail

The updated failure map was sent to the oracle. It did not find a surviving dense-fold or sparse low-degree reduction. It proved the clean finite-difference extension: every degree-d polynomial signature on Boolean views has an alternating relation on every `(d+1)`-subcube. Hence a forbidden local view is an exact +/-1 combination of the other `2^(d+1)-1` vertices. The relation is in the source module, so arbitrary linear rows, modular reductions, tensor powers, and dense linear folds preserve it. For quadratic signatures on a 3-clause, all seven legal views replace the forbidden view at constant cost.

This was immediately implemented in `verify_finite_difference.py` and checked exactly on 400 random `(k,d,u,J)` instances for `2<=k<=6`, all `d<k`, over integers and moduli 2,3,5,6,10. The theorem is now in `proof_cvp.md`. Together with odd holonomy for full local marginals, it rules out the whole bounded-local-signature family. No further oracle call is justified until a genuinely global explicit matrix exists.

As a final attack on the quantifier gap in the fixed-sample theorem, I exhaustively searched **code-dependent** puncturings of tiny tensor squares. For `D=span{110,101}`, preserving tensor pointed distance 4 requires all 9 of 9 coordinates: every proper puncture lowers it. For 40 deterministic random length-4 dimension-2 pointed codes, minimum preserving sample sizes varied widely (including 4, 8, 9, and all 16), so code dependence sometimes helps but often does not. This is only finite evidence; `verify_code_dependent_puncture.py` reproduces it exactly.

One mathematically clean compression did emerge but fails parameter accounting. The subcode spanned only by pure powers `x^{tensor q}` inherits exact pointed distance `delta^q`, since it is contained in the full tensor code and contains the minimum pure power. It is symmetric, so retaining one coordinate per permutation orbit gives length `binom(L+q-1,q)` and loses at most a factor `q!` in distance. Exact tiny-code tests agree. But polynomial output still forces bounded q when L is polynomially large, so this cannot amplify the additive base gap. The lemma is recorded in `proof_cvp.md`; `verify_pure_power_span.py` covers finite claims.

I also tested a non-polynomial-looking local escape: phase-lift each legal clause view by `z in Z/q`, placing its three incidence ones at view-dependent shifted phases. Exact GF(2) subset DP over every phase target found minimum legal trade 3 in every feasible case for 200 random q=2 signatures, 100 q=3, and the completed q=4 samples. Exhausting all separable signatures `alpha_j(a)=beta_j(a_j)` for q=2 (64) and q=3 (729) again always gives a three-column repair whenever feasible. Phase lifts can make many target phase triples infeasible but do not make a feasible forbidden boundary expensive; the local gap remains constant. `verify_phase_clause_gadget.py` records exact distributions.

A larger-q meet-in-the-middle search clarified that random phases sometimes eliminate all trades of support at most five (354/500 for q=4, 481/500 for q=8, all 300 for q=16), so phase labels can genuinely increase local girth. But end-to-end completeness then fails: on the satisfiable two-clause formula `(x1 or x2 or x3) AND (x1 or not x2 or x3)`, only 23/30 random q=2 and 14/30 random q=3 phase assignments allowed any satisfying Boolean assignment to lift consistently. The obvious completeness-preserving phases are coboundaries `alpha=beta(variable,value)-gamma(clause,view)`; a gauge change removes them entirely, restoring the original three-view cheat. Thus the tradeoff is exact: random nontrivial phases may improve local soundness but introduce global holonomy that rejects YES instances; coboundary phases preserve all YES instances but add no soundness. This is finite evidence plus a proved gauge identity, verified in `verify_phase_lift_completeness.py`.

## Oracle consultation 7: phase cocycle classification

The phase lift was the only candidate with any positive local-girth evidence, so consultation 7 was narrowly targeted. The oracle proved option A under explicit assumptions: copy-stable local interface/view types, realization of every alternating type cycle by some satisfiable transformed formula, and universal completeness for every such assignment. Summing lift equations around a realized cycle forces zero holonomy. A spanning-forest argument then makes every label a coboundary `alpha=beta-gamma`; gauge removal restores the unphased gadget and its support-three forbidden-view trade. Thus local fixed phase labels face an exact dichotomy: nonzero holonomy rejects a realizable YES cycle, while zero holonomy is gauge-trivial and has additive soundness only.

I implemented the classification checker: 400 random coboundaries were recovered exactly over q=2,3,5,8; 239 single-edge perturbations lying on cycles were detected; explicit support-three gauge identities passed. The theorem and assumptions are now in `proof_cvp.md`; finite checks are `verify_phase_cocycle.py`. Global cycle-dependent selectors are outside the theorem, but unrestricted local selector freedom already restores old trades.

A finite menu of fixed phase seeds has the same pointwise dichotomy on any realized incidence graph: a nonzero-holonomy seed rejects it; a zero-holonomy seed is a coboundary on it and supports the local trade. Tiny K3,3 type-graph experiments over q=2,3,5,7 confirm this. This does not prove a global diagonalization against graph-dependent seed menus; that quantifier gap is explicit in `proof_cvp.md` and `verify_seed_phase_dichotomy.py`.

I tested a more global branching-program-like candidate: one global Boolean branch variable controls one of two permutations at each edge of a state cycle; each fixed branch has fixed-point-free holonomy, so no honest state trajectory exists. The NCP uses odd coverage and GF(2) marginal consistency for global branch, edge factors, and states. Soundness collapses spectacularly: for random q=3,4,5 instances with cycle length 3, HiGHS always reports weight 9, independent of q, versus the naive odd-orbit scale `1+6q`. An explicit weight-9 exact syndrome solution was extracted and checked with integer GF(2) arithmetic: one factor uses three branch/state columns to splice incompatible local trajectories. This is the same superposition disease in a global controlled-permutation guise. `verify_controlled_permutation_cycle.py` records the exact witness; only optimality is solver evidence.

The universal algebra behind that splice is the 2x2 rectangle kernel of unary GF(2) marginalization. Four corners of any joint table have zero row marginals, zero column marginals, and even coverage. Toggling such a rectangle turns a singleton factor table into support three without changing any unary equations. More generally, all 2^k vertices vanish under every proper marginal of a k-bit table. Therefore every bounded-order marginal factor encoding is nonintegral before formula-specific details enter. `verify_mod2_marginal_nonintegrality.py` and `verify_pairwise_marginal_kernel.py` check these lemmas.

A systematic-generator variant also fails trivially: putting assignment coefficients in an identity block and appending arbitrary linear feature rows gives an ordinary linear codeword `(a,aP)`, not nonlinear assignment features. A target with one corrupted clause-feature bit is exactly distance one from that codeword, irrespective of P. Exact enumeration over 200 random tiny generators confirms this in `verify_systematic_generator_gap.py`. Nonlinear features cannot be generated from assignment coefficients by a linear code without lifting monomials—and lifted monomials return to the global consistency problem.

A harsher completeness test uses a unique-SAT core: remove the clause forbidding `000` from all eight clauses, leaving exactly assignment `000`. Among 1000 deterministic random phase tables at each q=2,3,5, **zero** admitted a phase lift. There is also an exact probability calculation: for a fixed selected incidence graph, random independent edge labels are potential differences with probability `q^{-(E-V+c)}`. Here E=21, V=10, c=1, so the probability is `q^-12`. This proves random high-girth phases lose completeness exponentially in cycle rank. `verify_phase_unique_sat.py` reproduces the finite counts and rank arithmetic.

I then tested whether random **disconnected** scopes could beat odd holonomy without connected-view chains. With only unary overlaps they cannot: any proper edge subset has a support-three sum of translated forest colorings with the same unary marginals. However, closing random scopes under intersections and enforcing **all intersection marginals** sometimes makes the exact GF(2) fiber infeasible. A deterministic table for n=5..10 shows a density threshold: with `2n` random scopes of 3 edges, all 30 tested inconsistent cycles were infeasible; sparser/2-edge systems often remained feasible. These are exact elimination results, not MILP statuses (`verify_disconnected_scope_threshold.py`).

I generalized this to arbitrary small CNFs: take singleton clause scopes plus random nonlocal clause subsets; columns are satisfying assignments to each scope's entire variable union; every pair of scopes has full marginals on **all shared variables**. Exact elimination found no fiber in 20/20 all-eight-clause trials, 20/20 inconsistent XOR-cycle trials, and 10/10 K4 Tseitin trials. Completeness is immediate because a satisfying global assignment restricts consistently (`verify_random_scope_3sat.py`).

The scalable padded 3-color cycle immediately exposes a density/arity weakness. With one random scope per clause, exact pseudoassignments survive at several tested parameters. On a cleaner unpadded edge-cycle, `2n` random 3-edge scopes fail completely at n=24 and n=30 (3/3 exact fibers each): constant **linear-density random** scopes are dead asymptotically.

However, enumerating **all pairs of constraints** is strikingly stronger and still polynomial. With full shared-variable marginals, exact fibers are infeasible for every tested 3-color cycle n=6..40; inconsistent XOR cycles through length 15; cubic Tseitin contradictions through 8 graph vertices/32 clauses; non-q-colorable K4, K5, and odd wheels. These are all exact GF(2) elimination results (`verify_all_d_scope_edge.py`, `verify_all_pair_cnf.py`, `verify_all_pair_coloring.py`). Pair groups have constant many views for bounded-arity constraints, though pairwise group-overlap rows can make the explicit matrix large polynomial.

This defeated every structured counterfamily tested locally, so consultation 8 asked exactly whether all-pairs exactness is universal. It is false. The oracle supplied a clean Petersen-graph counterexample: GF(3) edge variables obey charged signed-incidence equations at the ten cubic vertices, with total charge one. Summing equations proves UNSAT. Yet selecting all solutions for every singleton/pair vertex group gives odd GF(2) coverage and matching full marginals; girth five ensures projected affine spaces agree, and every fiber has odd cardinality (a power of 3). Total witness support is 2925.

I immediately implemented the exact hierarchy: 55 groups, 2925 columns, 23680 rows. The all-ones vector satisfies the target exactly, and independent elimination finds an even smaller support-367 solution. The UNSAT charge-sum certificate is checked exactly. `verify_petersen_pair_counterexample.py` passes, and the proof is in `proof_cvp.md`. Thus all-pairs scopes are decisively dead; residual coding sees zero. The oracle notes a Boolean arity-six encoding, while literal-CNF expansion is possible but large.

The construction extends cleanly to every fixed scope level k: use charged incidence equations on K_{2k+1} and include all groups of at most k vertices. Any noncommon row coefficient has an edge to a vertex outside `Q union R`, so it cannot be supported on the overlap. All local affine fibers remain odd. Hence every fixed k fails for some arity-2k CSP. `verify_connectivity_hierarchy_counterexample.py` checks k=1,2,3. This does not yet refute growing k for fixed-arity 3SAT, but it eliminates the hope that a fixed level is universally exact.

A sharp local rank check identifies exactly what is missing. Degree <=2 signatures on a 3-clause always put its forbidden view in the span of legal views; the cubic violation monomial `(1-x1)(1-x2)(1-x3)` separates it. Adding arbitrary extra local bits does not change this threshold. But that cubic has nonzero third mixed difference, so it cannot be assembled from unary variable-interface signatures. Therefore local soundness is easy only after adding genuinely joint clause information, and linear consistency with separately encoded variables is the unresolved nonlinear step. `verify_high_order_clause.py` checks exact ranks for scope sizes 3 through 8.

Finally I implemented the most tempting direct integer CVP scaling. One-hot variable equations and clause equations are weighted by M=10^6, with all coefficients softly centered at 1/2. A false clause is repaired **exactly** by slack `(s,t)=(0,2)`, paying additive squared norm 2 independent of M. On the all-eight-clause core padded with D satisfiable clauses, the explicit NO point has squared distance `R^2+2`; at D=1000 its distance ratio is below 1.0005. This is a concrete exact-fiber cheat, not merely a warning. `verify_scaled_integer_cvp.py` checks every residual exactly; the construction is in `proof_cvp.md`.

The slack failure is general for every linear gadget affine in true-literal count. If `h+A w1=t` and `2h+A w2=t` give short exact witnesses for satisfying counts 1 and 2, then false count 0 has exact witness `w0=2w1-w2`, with norm at most `2||w1||+||w2||`. This is the integer analogue of the local affine trade and survives all row scaling/moduli. More generally, degree-d count dependence extrapolates count zero from counts 1 through d+1 with binomial coefficients of total absolute value `2^(d+1)-1`. `verify_slack_extrapolation.py` and `verify_polynomial_slack_extrapolation.py` check 2200 exact instances total.

## Final adversarial review

The final oracle referee accepted the odd-cycle theorem and pointed tensor lemma after minor hypothesis/quantifier fixes. It found and we corrected a substantive overclaim in the sampling result: the minimax argument fixes one sample S and varies the one-dimensional code D_Z, so it excludes only fixed/code-oblivious samples with a uniform guarantee, not code-dependent puncturing. We also corrected the strict versus non-strict factor floor, stated the sampling inequality without dividing by a possibly zero quantity, added the pointed-word existence hypothesis, and qualified all floating-point MILP optima as computational evidence rather than proof certificates.

## Milestone 6 / final assessment

No hardness result has been proved. There is zero advancement on ladder items (a)--(c). Local linear encodings are obstructed by explicit examples, and fixed code-oblivious tensor sampling has a rigorous minimax obstruction. Code-dependent sampling is not excluded. Dense structured folding of a high tensor power would require a global soundness theorem and remains wholly open here.
