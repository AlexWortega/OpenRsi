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
