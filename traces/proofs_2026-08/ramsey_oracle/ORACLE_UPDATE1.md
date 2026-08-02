# Experimental response to oracle call 1

Implemented the stationary closed-walk transfer-matrix proposal exactly.

1. `experiments/search_stationary_c5.py` exhausts all 32,768 symmetric Boolean 5x5 transition matrices (loops allowed) for template `H=C5`, at powers q=2,...,6. Exact integer traces verify `W_bad>=W`. For every q the optimum feasible value is exactly `W=2^q`, attained by the trivial complete transition matrix on one H-edge. Thus no gain over binary in this entire class.

2. `experiments/search_stationary_c5_directed.cpp` exhausts all 1,048,576 arbitrary directed 5x5 transition matrices with each row outdegree at most 2, q=2,...,8. Again every optimum is exactly `2^q`. This is a much broader exact negative finite test, though not all directed matrices.

3. `experiments/hill_stationary.py` searches arbitrary directed Boolean transitions for C5 and the 11-vertex Groetzsch template, scoring exact trace excess. On C5,q=5 it finds only `2^5`. On Groetzsch,q=3 several 48k-step aggregate runs find feasible W=11, below the inherited unrestricted 12-word code; q=4 only 16 and q=5 only 32. These latter are heuristic non-results, not bounds.

Conceptual concern: the proposed pivotal synchronization lemma currently contains essentially the whole unsolved zero-error code problem. Defining `(A,q)` as lexicographically first feasible does not construct it. A stationary automaton's entire length-q cycle language must be pairwise separated, a condition apparently stronger than selecting a code, and the first exact tests suggest branching creates off-diagonal bad cycles. The layered variant risks tautology: a width-N disjoint-path program represents any N-word code, so a proof must exploit polynomial width substantially below code size.

Please now do one of two things, rigorously and concretely: (i) derive an explicit asymptotic transition family A (or short repeating layered pattern) from a known classical pre-forbidden-document combinatorial object, and prove the synchronization property; or (ii) identify a structural obstruction showing stationary automata cannot have growing base, then replace the proposal with a genuinely different concrete construction. Do not merely restate existence as a CSP or pivotal lemma. Analyze the exact C5 failures above. The forbidden Ten Advances document and all discussions of it remain entirely off limits.
