# STATUS

Updated: ninth oracle response implemented; no new construction, but a tensor fitting-rank obstruction is proved and checked.

## Main result: **PARTIAL**

No superexponential lower bound, coherent growing-base family, or explicit base above 3.199 has been proved in this run.

## Milestone

Read the definitive `prior/final/STATUS.md` and `prior/final/proof_ramsey.md`, plus the prior campaign status/attack logs. Distilled the exact problem, positive reductions, proved obstructions, banked families, and open gap into `ORACLE_BRIEF.md`.

The current precise gap is a scalable correlated construction: equivalently (i) `k`-color triangle-free complete-graph colorings of order `k^{Omega(k)}`; (ii) independence-two graphs with polynomial witness power and polynomially growing achieved strong-power base; or (iii) local-palette seeds `(N,g,s)` with `log N=Omega(s log s)` and `g=s^{O(1)}`.

## Oracle proposal 1: stationary automata — finite tests negative

The oracle's transfer-matrix condition is mathematically sufficient, but no asymptotic automaton was supplied. Immediate exact tests found only the binary baseline:

- all 32,768 symmetric Boolean transitions on `C5`, powers 2–6: maximum feasible closed-path count `2^q`;
- all 1,048,576 directed transitions on `C5` with row outdegree at most two, powers 2–8: maximum `2^q`.

Heuristic unrestricted-transition searches on the Groetzsch template found 11 paths at power 3 (below the inherited unrestricted 12-word code) and only binary counts at powers 4–5. These are non-results, not impossibility claims.

## Oracle proposal 2: anchored palettes — rigorously rejected in proposed form

For palettes `P_(a,B)={0,a} union B` on all `(r-1)`-subsets `B subset {3,...,g}`, if `g-2>=6(r-1)` then six disjoint `B_i` under one anchor induce a `K_6` whose every edge list is exactly `{0,a}`. Ramsey's elementary `R_2(3)=6` argument forces a monochromatic triangle. Thus the full family is impossible at the proposed `g~r^2` scale (in particular for `r>=6`), independently of its greedy algorithm. A verifier exhausts the finite two-color core.

Small greedy tests also retained only 8/20, 7/112, and 22/990 vertices at `(r,g)=(3,7),(4,10),(5,14)` in the best tested variants. These are diagnostics only.

A stronger proved necessary condition is the link-Ramsey bound `nu(L_F(C))<=R_(|C|+2)(3)-1` for every core `C`. It kills the natural maximum matching-number family, but logarithmic-core families show that this hierarchy alone does not remove factorial cardinality. No edge-coloring mechanism for those families is known.

## Varying-domain partial assignments — rigorously banked at bounded fractional complexity

A general partial-assignment rule is triangle-free when each coordinate's state graph is triangle-free and every object pair is separated by adjacent states at a shared coordinate. The proved fractional-cylinder lemma gives

`sum_f product_(x in B_f) chi_f(H_x[S_x])^(-1) <= 1`.

Hence if all used state graphs have fractional chromatic number at most `Q`, the family has at most `Q^r` objects, regardless of the number of possible domains. Binary/bipartite labels cap at `2^r`; domain variation cannot supply factorial entropy. Polynomially growing `chi_f` formally leaves room, but realizing the bound is precisely the unresolved correlated strong-power code problem.

## Background harvest

No relevant completed positive background job exists. The sibling cyclic rediscovery jobs ended without a record, and its optional final L4 certificate completed; the already imported theorem `L_4<=64` remains negative route closure, not a growing-base result. Older local/F2/Cayley jobs remain stalled; the best visible Cayley seed has base only 2.731.

## Permutation-orbit permanent mechanism — rigorously banked

For triangle-free `H` on `n` vertices, the transitive greedy construction on all permutations guarantees `n!/per(M)` codewords, where `M` is the reflexive nonadjacency matrix. A new proved universal bound is

`per(M)>=n!/C^n`, `C=(5/2)(5/3)^(3/2)<5.38`.

It follows by peeling large independent neighborhoods, applying a dense bipartite factor criterion and van der Waerden on the residual matrix, and controlling the factorial block loss by entropy. Therefore this guarantee has uniformly bounded base. Exact permanent diagnostics on C5/Mycielski and random maximal triangle-free graphs were substantially worse. This does not bound the maximum separated permutation family, only the permanent/degree guarantee.

## Balanced permutation maximum — rigorously reduced to the original gap

A constant-composition lift proves that every separated word code over a fixed triangle-free graph becomes a separated permutation code in a triangle-free blow-up, losing only a polynomial factor in its length. Therefore the limsup exponential base of the best separated permutation family is exactly

`sup_(H triangle-free) Theta(overline H) = sup_k (R_k(3)-1)^(1/k)`.

Thus optimizing the maximum permutation subset, unlike the banked permanent guarantee, is asymptotically the entire capacity/Ramsey problem rather than a tractable specialization. A fractional cover by bad cliques cannot force an exponential upper bound either: each clique has size at most `alpha(H)^n`, making every such cover weigh at least `n!/alpha(H)^n`. An elementary altered-random-graph construction with `alpha(H)=O(n^(2/3)log n)` makes this lower bound superexponential.

## Generalized-quadrangle Tanner proposal — rejected by q=2 test

The proposed correlated expander family fails both pivotal small discriminators. For the deterministically selected involutory doily polarity, exhaustion of all 720 doily collineations finds exactly 30 maps outside its polarity-preserving subgroup that move every point to a polarity nonneighbor. Postcomposing any legal configuration by such a map preserves all Tanner line constraints and equitability but creates a coordinatewise bad pair not removed by the proposed quotient, refuting its rigidity mechanism. The exact finite check passes. Independently, a balanced q=2 configuration is equivalent to six perfect matchings of the Tutte--Coxeter graph with every pair intersecting in three edges. Exact-cover enumeration finds 288 perfect matchings, while their compatibility graph has clique number exactly three. Thus the q=2 configuration space is rigorously empty; the independent exhaustive verifier passes. Full-collineation quotienting absorbs the 30 maps but cannot repair this abundance failure. A separate matrix-orbit nudge on `GL(d,2)` with nonlinear sum-free coordinate graphs found only bases 1.913 (`d=3`) and 2.166 (`d=4`) in heuristic searches; this is a non-result and no upper bound is claimed.

## Tensor fitting-rank obstruction

For completely arbitrary correlated coordinate maps, if each local separation graph has a fitting matrix of rank `r_i` (nonzero diagonal and zero on graph edges), then every separated family has size at most `product_i r_i`. This follows by a Hadamard-product rank argument and requires no product structure. In particular binary bilinear local predicates on `F_2^d` have fitting rank at most `d+1`; arbitrary global correlation cannot overcome that ceiling. The proof is in `proof_ramsey.md` and its finite sanity verifier passes. This is a negative structural theorem, not a growing-base construction.

## Perfect-matching partner reduction — right entropy, no family

All `(n-1)!!` perfect matchings of `K_n`, encoded by partner words of length `n`, would have growing base `~sqrt(n/e)` if triangle-free coordinate graphs separated every pair. In the natural symmetric formulation this asks for a 3-uniform hypergraph with triangle-free links. A verified `n=6` instance exists (8 triples, 15 words), but has base only 1.57. Exact SAT reports the symmetric `n=8` instance UNSAT; lacking a certificate, that is only diagnostic. More generally, switching pairings on any four-set shows that separation forces every four-set to contain a hyperedge, while triangle-free links force every four-set to omit one. The finite 3-uniform Ramsey theorem therefore proves the symmetric mechanism cannot exist for all sufficiently large `n`. A stronger Ramsey argument also rules out separating **all** perfect matchings with unrelated coordinate graphs for all sufficiently large `n`: homogenize the three orientation bits on triples, use triangle-freeness to kill the outer two bits, then exhibit an unseparated four-vertex matching switch. Greedy switch-avoidance plus SAT does produce verified pruned codes `(n,N)=(8,28),(10,159),(12,300)`, with bases `1.517,1.660,1.609`. They evade the all-matchings obstruction finitely but are below the binary baseline and show no growing trend. A switch-free subfamily with factorial cardinality does exist by a simple greedy bound: the switch-conflict graph has degree `2 binom(n/2,2)`, so pruning loses only a polynomial factor. However no triangle-free coordinate graphs are known to separate that large family; finite SAT provides no scalable rule. Thus no coherent growing family is obtained.

## Final assessment

**PARTIAL, below goal-ladder item (a).** No superexponential lower bound, growing-base family, or verified base above 3.199 is obtained. The durable new information consists of exact negative finite searches and rigorous obstructions/reductions for several plausible correlated mechanisms: stationary automata in tested classes, anchored palettes, varying-domain assignments of bounded fractional complexity, permutation-orbit methods, GQ-Tanner constraints, low-rank algebraic channels, and all-perfect-matching partner codes. Every promoted finite claim has a passing `verify_*.py`; heuristic scripts and uncertified solver diagnostics remain explicitly unpromoted. These are negative structural results, not progress on the requested lower bound.

## Integrity

No forbidden document, copy, summary, or discussion was accessed or searched. No proof assistant is used. Prior partial results remain explicitly partial.
