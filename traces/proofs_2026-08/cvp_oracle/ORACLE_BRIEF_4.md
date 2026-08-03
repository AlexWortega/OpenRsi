# Oracle brief 4: can pointed tensor amplification be compressed?

Strictly respect the prohibition on the named recent document and all descriptions; reason independently. No PCP/Label Cover black boxes or conjectures.

We proved this elementary lemma. For a binary linear code D with distinguished coordinate *, define delta_*(D)=min{|x|:x in D, x_*=1}. Then delta_*(D tensor E)=delta_*(D)delta_*(E): the distinguished column has delta_D active rows, each an E pointed word. Homogenizing affine coset t+C gives delta_*=1+dist(t,C).

The base exact SAT->NCP reduction only gives pointed YES/NO K+1 versus K+2, so explicit q-fold tensor has ratio (1+1/(K+1))^q and length (N+1)^q. Polynomial ratio requires q=Omega(K log N), impossible explicitly.

Analyze one narrow question: is there an elementary polynomial-size composition/compression that preserves enough pointed tensor distance to turn this additive gap into rank^c hardness? Candidates include symmetric powers, expander-sampled tensor coordinates, folded/evaluation representations, or recursively concatenating while pruning coordinates. We need an ordinary explicit generator/parity-check matrix at the end, not a succinct code.

Required response:

1. Pick the strongest candidate and give exact generator/matrix construction and dimensions.
2. Prove completeness and formulate the exact pointed soundness bound.
3. Test the construction conceptually against arbitrary linear combinations, not only pure tensors.
4. If impossible for information-theoretic reasons, prove a lower bound showing why sampling/compression cannot retain the needed pointed distance for all base codes arising from the reduction.
5. If the soundness lemma is unproved, isolate a tiny falsifiable case and algorithm for exhaustive search.

Also examine whether one can redesign the exact base reduction so K=O(log input) (or YES pointed distance constant) while retaining NP-hardness, e.g. encode the assignment in coefficients rather than support. Explain the polynomial-time linear-membership obstruction precisely but do not overgeneralize it.

Do not give a survey. Deliver one precise construction or one decisive obstruction, with explicit parameter arithmetic.
