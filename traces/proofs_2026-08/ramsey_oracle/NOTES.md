# Attack log

## Phase 1 — prior-state compression

Read `prior/final/STATUS.md` and the complete `prior/final/proof_ramsey.md`, which supersede earlier campaigns. Also reviewed `prior/final/NOTES.md`, `prior/sol/{STATUS.md,NOTES_ramsey.md}`, `prior/round1/{STATUS.md,NOTES_ramsey.md}`, and `prior/fable/{STATUS.md,NOTES_ramsey.md}`. File inventory was skimmed to identify the breadth of tested constructions and verifiers.

Produced `ORACLE_BRIEF.md`, emphasizing the only useful target: a coherent correlated growing-base family. It records the exact capacity bridge, effective witness-power criterion, local-palette criterion, all rigorous broad obstructions, and the tested families that must not be repeated.

No mathematical result beyond inherited verified facts is claimed at this milestone.

## Phase 2 — oracle proposal and immediate tests

The first oracle proposed stationary or layered polynomial-width automata whose closed paths form a strong-power code. The exact condition is a transfer-matrix identity `tr(B^q)=tr(A^q)`, where `B` is the synchronized product restricted to coordinatewise nonedges. If paired with `tr(A^q)>=d^{epsilon q}` at polynomial width/power, this would indeed prove the target. However, the proposal did not construct such automata; its pivotal lemma is essentially the open correlation problem.

Implemented three tests immediately:

- `experiments/search_stationary_c5.py`: exhaustive over all 32,768 symmetric Boolean transition matrices on `C5`, loops allowed, powers 2–6. Best feasible `W` is exactly `2^q` at every power.
- `experiments/search_stationary_c5_directed.cpp`: exhaustive over all 1,048,576 directed 5-state matrices with row outdegree at most two, powers 2–8. Best is again exactly `2^q` at every power.
- `experiments/hill_stationary.py`: exact-trace heuristic for unrestricted directed matrices. `C5,q=5` gave 32. Groetzsch `q=3` gave 11 after multiple runs (below the inherited unrestricted code 12); `q=4,5` gave 16,32. These heuristic values are not upper bounds.

The exact enumerations are rigorous finite facts about the specified automaton classes, but have no goal-ladder value. Prepared `ORACLE_UPDATE1.md` asking for an explicit transition family/proof or a structural rejection and genuinely different construction.

## Phase 3 — anchored-palette proposal, implementation, and obstruction

The second oracle correctly declined to infer a universal stationary obstruction and noted that bounded-period layered automata are merely stationary automata after a phase lift. It proposed explicit palettes `P_(a,B)={0,a} union B` on `2 binom(g-2,r-1)` vertices and a deterministic legal-color greedy process.

Implemented this in `experiments/anchored_palette.py`, maintaining each color graph triangle-free by bitset common-neighbor tests and independently checking the retained induced subgraph after greedy deletion of failure endpoints. Immediate results were poor: `(r,g)=(3,7)` retained at most 8 of 20 among first variants; `(4,10)` retained at most 7 of 112; `(5,14)` list-first retained 22 of 990. Algorithmic choices are not the main issue.

Found a rigorous structural obstruction to the full palette family. If `g-2>=6(r-1)`, choose six pairwise-disjoint `(r-1)`-sets `B_i` under one anchor. Every pair of their vertices has palette intersection exactly `{0,a}`, forcing a two-coloring of `K_6`, which has a monochromatic triangle. Thus the full construction is impossible for its proposed `g~r^2` scale (indeed for all `r>=6`). `experiments/verify_anchored_obstruction.py` checks explicit blocks and exhausts all 32,768 two-colorings of `K_6`. The proof is in `proof_ramsey.md`.

A retained subfamily would need matching number at most five inside each anchor. The third oracle call settled the cardinality question: this alone is harmless, since all sets meeting a fixed five-set retain `exp((1+o(1))r log r)` size. But that extremizer fails a stronger proved link-Ramsey condition. For every core `C`, pairwise-disjoint petals in the link are limited to `R_(|C|+2)(3)-1`; otherwise sets intersecting exactly in `C` induce a complete graph using only `{0,a} union C`. The five-set extremizer fails already at a one-point core using `R_3(3)=17`.

The full hierarchy still does not force subfactorial cardinality: fixing a common core of size `O(log r)` preserves `exp((1-o(1))r log r)` possibilities and evades the simple link matching tests. No correlated edge-coloring rule is known. The oracle honestly supplied no further candidate. Both proposed routes are therefore banked; main status remains partial.

## Continuation — background harvest and partial-assignment mechanism

Harvested the only relevant live background campaign in `/home/alexw/OpenRsi/runs/ramsey_fable`. Its cyclic 1073 rediscovery SAT jobs remain unresolved after five hours and are explicitly low-value; min-conflicts record attempts had stalled and were killed there. The separate L4 certificate campaign has 303 verified-UNSAT palette cases and one hardest ordinary four-color case still running with a multi-GB DRAT file. This is negative local-palette information, not a growing-base construction, and is not imported as a theorem here while its final certificate remains incomplete.

Added unified `experiments/verify_current_finite_claims.py`; it independently reruns both complete automaton enumerations and the anchored K6 obstruction and passes.

Derived a varying-domain partial-assignment coloring: label every incidence `x in B` by a state of a triangle-free graph `H_x`; two objects must share an x with adjacent states, and their edge is colored by such x. The rule is triangle-free. Binary tests gave exact maxima `2^r` for small parameters; C5 at r=2 gave 5 independent of universe size 3–5.

Oracle call 4 supplied a clean fractional-cylinder packing proof: `sum_f product_(x in B_f) 1/chi_f(H_x[S_x])<=1`. This proves that varying domains add no entropy; bounded fractional chromatic state graphs give at most `Q^r`, and the binary route is capped at `2^r`. High-fractional-chromatic states leave formal room but reduce to the same correlated strong-power code gap. Added the proof to `proof_ramsey.md`, the exact checker `experiments/verify_fractional_cylinder.py`, and the failure mode to `ORACLE_BRIEF.md`.

Attempted an independent reviewer subagent, but the configured runtime failed to spawn (`pi ENOENT`); therefore performed manual adversarial checks instead. Corrected a transient count typo in `ORACLE_BRIEF.md`: there are 16 possible row subsets of size at most two and hence `16^5=1,048,576` matrices.

## Final continuation — permutation-orbit permanent mechanism

Harvested backgrounds again: cyclic rediscovery jobs remained unresolved; the sibling L4 hardest case remained active with a growing multi-GB DRAT. No positive candidate.

Tested a fresh factorial object: all permutations of a triangle-free graph's vertices. The bad-neighbor degree is exactly the permanent of its reflexive nonadjacency matrix, so transitive greedy guarantees `n!/per(M)` separated permutations. Exact subset-DP (`experiments/permutation_orbit_capacity.cpp`) gave bases 1.560,1.468,1.370 on C5 and two Mycielski levels; 30 random maximal triangle-free n=20 graphs peaked at 1.592. Passing finite verifier: `verify_permutation_orbit.py`.

The fifth focused oracle call supplied a full universal obstruction. Peeling any vertex-neighborhood larger than 2/5 of the residual creates independent all-one blocks. The terminal reflexive nonadjacency matrix has at most 2/5 zeros per row/column; a max-flow factor criterion gives a residual regular factor, van der Waerden bounds its permanent, and entropy controls the factorial loss over peeled blocks. Result: `per(M)>=n!/C^n`, `C=25sqrt(15)/18<5.38`. Thus the degree/permanent guarantee is always fixed-base. Added a full proof to `proof_ramsey.md` and exact adversarial checks through all labeled triangle-free graphs n<=6 plus the numeric factor inequality to `verify_permanent_bound.py`.

Manual referee correction: the dense-matrix lemma takes integer `a`; at terminal size use `a_0=Delta(H[T])<=2t/5`, yielding `1-2a_0/t>=1/5`, rather than formally substituting nonintegral `2t/5`. Updated proof. Also caught and fixed the verifier's initially wrong remembered count of labeled triangle-free graphs at n=3 (7, not 8). The failed first verifier run was not promoted; the corrected script passes.

## Sixth focused oracle call — permutation balance is universal

The remaining loophole in the permanent route was that the maximum separated subset of permutations could greatly exceed the degree guarantee. A sixth focused call produced a rigorous constant-composition reduction showing that this is not a simpler subproblem. Any length-`m` separated code over a fixed triangle-free graph `H` has a constant-composition subcode losing at most `binom(m+|H|-1,|H|-1)`. Blowing each symbol into as many clones as its composition count turns every word into a permutation of `m` vertices while preserving separation and triangle-freeness. Hence the limsup exponential base of the best separated permutation family equals the supremum of capacities over all triangle-free graphs, equivalently `sup_k (R_k(3)-1)^(1/k)`.

This does not prove the target; it rigorously shows that the apparent balanced-permutation specialization is asymptotically universal and thus circular as a simplification. Added the proof to `proof_ramsey.md` and a small independent lift check to `experiments/verify_permutation_balance.py`.

## Background harvest after continuation request

Harvested all visible Ramsey processes before beginning a new attack. The sibling `ramsey_fable` campaign completed two rigorous negative structural milestones: `L_4<=64`, so the naive factorial local-seed equality tower fails already at level four, and a cyclic-to-Schur ceiling showing symmetric cyclic difference colorings are bounded by `2S(k)+2`. Its remaining cyclic SAT jobs are explicitly low-value record rediscovery attempts and still unresolved. An optional final DRAT job for the ordinary four-color `L_4` case is still running, but that case is already covered there by the classical pre-forbidden-era bound `R_4(3)<=62`. Older `proofs_code_fable` jobs remain active but are long-stalled heuristics in already-banked local/F2/Cayley routes; no positive candidate was harvested. Recorded the new route closures in `ORACLE_BRIEF.md`.

## Seventh oracle proposal — generalized-quadrangle Tanner codes fail immediately

The oracle proposed a cubic-expander constraint system whose edge labels are points of a symplectic generalized quadrangle, each Tanner star being a collinear triple and the total type equitable. Its unproved pivotal rigidity said coordinatewise polarity-nonadjacent configurations must differ by a polarity-preserving automorphism.

Implemented the prescribed `q=2` doily discriminator in two independent pieces. Represented the doily as duads and synthemes of `K_6`, found an involutory incidence duality, constructed its 15-point polarity graph, and exhaustively scanned all 720 doily collineations. Exactly 30 collineations outside the polarity centralizer move every point to a polarity nonneighbor. Therefore, for every legal equitable configuration `f`, composing with one of these maps gives a legal equitable coordinatewise-bad mate not removed by the proposed quotient. This is a direct finite counterexample to the rigidity mechanism conditional only on nonemptiness; `experiments/test_gq_tanner_q2.py` passes.

Also encoded the exact equitable configuration CSP on the 45 edges of the Tutte--Coxeter/doily incidence graph. After fixing one star by flag transitivity, CaDiCaL returned UNSAT on 7,155 variables and 140,613 clauses. Initially this was only an uncertified diagnostic.

The eighth focused oracle call supplied a much smaller exact reduction, which was implemented independently. A balanced configuration is equivalent to six perfect matchings of the Tutte--Coxeter graph whose pairwise intersections all have size three. Exact-cover enumeration finds 288 perfect matchings; their compatibility graph has 5,040 edges and clique number exactly three. `experiments/verify_gq_tanner_q2_obstruction.py` exhaustively verifies this, so q=2 emptiness is now a promoted finite theorem without relying on bare SAT. Quotienting by the full collineation group repairs the 30-map identification issue but cannot repair empty abundance. No rigorous q>=8 abundance or full-orbit rigidity route survived. The proposal is banked, with exact failures recorded in `ORACLE_BRIEF.md`.

## Independent correlated matrix-orbit nudge

Tested a non-product orbit idea not supplied by the oracle: vertices are invertible `d x d` binary matrices, viewed as `d` column words, and coordinate separation uses a sum-free Cayley set `S subset F_2^d`. The full `GL(d,2)` orbit has factorial-scale size, so a large separated suborbit could in principle be useful. Random maximal nonlinear caps were generated and separated subsets greedily searched. At `d=3`, all generated caps (only the seven affine hyperplanes appeared) gave at most 7 matrices, base 1.913. At `d=4`, 165 caps gave at most 22 matrices, base 2.166. These are heuristic lower-search results, not upper bounds or finite claims; they are far below the binary baseline and show no growing mechanism. The script is `experiments/search_gl_cayley_codes.py`. This is one discriminating nudge only, not a promoted theorem.

## Background re-harvest and polynomial-hitting nudge

Re-harvested before continuing. The optional sibling L4 DRAT job finished, but the sibling status already promoted `L_4<=64`; no new positive background result appeared. Long-running older local/F2/Cayley jobs remain stalled. The Cayley log's current best is only order 152 with five colors (base 2.731), below the benchmark and in a banked family.

Tested a correlated polynomial-evaluation idea: all zero-constant degree-`d` polynomials over `F_p` would form a `p^d`-word code in `p` coordinates if every nonzero difference polynomial hit a fixed symmetric sum-free `S`. Exhaustive tests over every maximal symmetric sum-free set for `p=5,7,11,13` find avoiding polynomials of degree at most three in every case. In particular `x^2` avoids the centered dense interval at `p=5,13`. The hoped-for hitting lemma therefore fails at tiny degree, far before `d=Theta(p)`. Exact failure recorded in `ORACLE_BRIEF.md`; scripts are `test_interval_polynomial_hitting.py` and `test_character_polynomial_hitting.py`. These are diagnostics, not asymptotic claims.

## Ninth oracle call — no candidate; general fitting-rank obstruction

The oracle honestly supplied no defensible growing construction. It instead gave a rigorous tensor fitting-rank bound that survives arbitrary cross-coordinate correlation. If every pair in `X` is separated in some coordinate graph and each graph has a fitting matrix (nonzero diagonal, zero on edges) of rank `r_i`, then `|X|<=product r_i`. The proof pulls back and Hadamard-multiplies the matrices: the result is nonsingular diagonal, while rank is at most the product via rank-one expansions.

This materially closes algebraic local channels having sparse polynomial certificates. For a binary bilinear edge predicate with zero diagonal, `1+R` is a fitting matrix of rank at most `d+1`, regardless of global code correlation. Wrote the full proof in `proof_ramsey.md`, added the obstruction to `ORACLE_BRIEF.md`, and added `experiments/verify_tensor_fitting_rank.py`; it checks the tight K2 tensor case and an alternating form on `F_2^4`. This is a negative structural theorem, not goal-ladder progress.

## Adversarial re-referee

Attempted to launch the configured independent reviewer subagent; the runtime again failed with `pi ENOENT`, so no reviewer output is claimed. Manually audited quantifiers and finite-claim reproducibility. Tightened the GQ statement from an implicit arbitrary polarity to the deterministically selected involutory polarity used by the verifier, and copied the checker to the required `verify_gq_polarity_bad_maps.py` name. Added `verify_polynomial_hitting_small.py`, which independently exhausts every symmetric sum-free set at p=5,7,11,13 and verifies the degree histogram for all maximum sets; the exploratory search is no longer the only support. Rechecked the tensor proof: Hadamard rank submultiplicativity follows from explicit rank-one expansion; the bilinear rank count is valid because degree-(q-1) monomials in d linear forms number at most `binom(d+q-2,q-1)`. No positive theorem was found.

## Final independent candidate: perfect-matching partner codes

Re-harvested backgrounds first; no files or logs changed materially, and all old processes remain stalled in banked routes.

Consider every perfect matching M of K_n as the word whose i-th symbol is i's partner. If one can choose triangle-free coordinate graphs H_i so every pair of matchings is separated, the code has `(n-1)!!` words in n coordinates and base asymptotic to `sqrt(n/e)`, which would prove growing base. A natural symmetric formulation asks for a 3-uniform hypergraph T whose every vertex link is triangle-free and whose links separate all matching partner words.

Implemented exact SAT. At n=6, a symmetric 8-triple hypergraph exists and independently verifies, giving 15 words in 6 coordinates (base 1.57, no benchmark value). At n=8, the symmetric 56-variable/5,740-clause instance returns solver-UNSAT; without a proof certificate this is only a diagnostic. The more general 224-variable instance with unrelated H_i timed out after ten minutes, so no conclusion.

A subsequent adversarial check found a clean asymptotic obstruction to the symmetric version. Compare matchings that differ only by switching pairings on any four-set. Separation forces every four-set to contain a triple of T. Triangle-free links force every four-set to omit a triple of T. Hence T and its complement are both `K_4^(3)`-free, contradicting the finite 3-uniform Ramsey theorem for all sufficiently large n. Added the proof to `proof_ramsey.md` and the exact failure to `ORACLE_BRIEF.md`. A second adversarial pass then closed even the all-matchings unrestricted-coordinate variant. Color each ordered triple by three bits describing which endpoint-coordinate graph contains the opposite pair. Hypergraph Ramsey supplies a seven-set with constant pattern; triangle-free coordinate graphs force the first and third bits to zero, and the switch `{ac,bd}` versus `{ad,bc}` is then unseparated. Added the theorem to `proof_ramsey.md` and `ORACLE_BRIEF.md`. This still does not rule out pruning to a factorial-size subfamily avoiding local switches.

## Final pruning test

Re-harvested backgrounds; no changes occurred in any live log. Tested the remaining perfect-matching loophole directly. Greedily selected matching families with no pair differing on exactly four vertices, then solved for unrelated triangle-free coordinate graphs. Independently verified codes are `(n,N)=(8,28),(10,159),(12,300)`, with bases `1.517,1.660,1.609`. At n=12 the greedy switch-free family had roughly 1,200 words, but direct SAT timed out; a 300-word prefix solved. These are real correlated finite codes but far below binary and show no growing trend. Added `verify_pruned_matching_codes.py`; recorded exact results in `ORACLE_BRIEF.md`. A final combinatorial audit sharpened the gap: an asymptotically huge switch-free subfamily actually exists trivially. The four-switch conflict graph on all matchings is regular of degree `2 binom(n/2,2)`, so a greedy independent set has size `(n-1)!!/poly(n)` and still growing base `~sqrt(n/e)`. Added this lemma to `proof_ramsey.md` and a finite degree checker. Therefore local-switch avoidance is not the entropy bottleneck; the exact missing step is a scalable construction of triangle-free coordinate graphs separating one such large independent set. The SAT examples do not supply it.

The oracle also observed that any fractional cover of permutations by bad cliques has weight at least `n!/alpha(H)^n`, since each bad clique has at most `alpha(H)^n` members. For triangle-free graphs with sublinear independence number this is already superexponential, so an exponential-weight bad-clique/cylinder cover cannot establish a universal exponential bound. This banks the final natural attack on the permutation maximum.
