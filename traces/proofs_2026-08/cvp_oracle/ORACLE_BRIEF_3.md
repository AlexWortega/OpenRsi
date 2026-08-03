# Oracle brief 3: choose a genuinely new encoding after two linear routes died

The recent named document and every account of it remain strictly off-limits. Work independently; do not invoke PCP/Label Cover or an unproved conjecture.

Goal: deterministic polynomial many-one reduction 3SAT -> GapCVP with rank^c Euclidean gap, preferably via binary syndrome decoding.

What is now rigorously dead:

1. One-hot GF(2) local-view syndrome gadgets. Three satisfying views sum to a clause's forbidden view, giving an exact zero-residual witness at additive cost 2.
2. Logarithmic connected-view hierarchy. We proved an explicit bounded-occurrence exact-3CNF counterfamily: an inconsistent 3-color permutation cycle. Every connected scope of d<n clauses has a tree skeleton; summing its three propagated colorings over GF(2) has odd mass, compatible marginals, and support <=3. Thus at d=C log M an UNSAT formula has exact witness <=3K.
3. An outer error-correcting code only amplifies nonzero residual and cannot touch exact alternative representations.
4. Explicit tensoring of a 1+O(1/K) base gap needs superpolynomial output even if optimum multiplied.

Need one precise new candidate, not a survey. Explore whichever is most viable among:

* a direct weighted integer-lattice encoding where satisfying assignments have small norm but every UNSAT exact-superposition alternative incurs a huge coordinate;
* a multi-characteristic or nonlinear-to-linear encoding that provably kills every odd-orbit sum while retaining polynomial size;
* a sparsity product/composition whose NO optimum multiplies and whose dictionary is represented with polynomially many columns;
* an algebraic evaluation encoding where YES error is sparse (not a dense codeword) and nonlinear assignment consistency has an elementary integral-decoding theorem;
* a superior route of your own.

Required: specify rows/columns/basis/target and all weights; implementable completeness witness; exact soundness lemma; dimensions and exponent accounting. Attack the candidate yourself on the forbidden-clause affine triple and 3-color holonomy counterfamily. If a lemma is unproved, isolate it narrowly and give the smallest brute-force experiment that can falsify it. Do not recycle connected views under another name.

Also examine this tempting paradox explicitly: why can't one take a classical exact integer CVP reduction, scale only its constraint-residual coordinates by a huge polynomial, leave assignment coordinates small, and obtain a polynomial gap? State the exact structural obstruction, and whether some exact reduction can be redesigned to avoid it.
