# Consultation 9: one genuinely global non-affine candidate, or a sharp no-go

Respect the strict prohibition on the named recent document and every copy, summary, discussion, or recollection of it. Work only from the independent failure map in `ORACLE_BRIEF.md`, `proof_cvp.md`, and this brief.

We still seek a deterministic polynomial reduction from 3SAT to polynomial-gap binary NCP or Euclidean CVP, without PCP. No ladder progress has been made.

The latest explicit candidate coupled all Boolean assignment bits through one CRT integer `X`, using `X-p_i q_i-b_i=0`. It failed because clauses still used the affine exact fiber `literal_count+s+2t=4`: on the all-eight-clause core, `(s,t)=(0,2)` repairs the one false clause at constant additive squared cost while every scaled/global row remains exact. Thus global assignment uniqueness or hashing alone is irrelevant unless clause validity itself becomes global/non-affine in the norm.

Earlier exact failures that must not be revived:

* affine and bounded-degree local signatures have constant finite-difference trades;
* all bounded-order GF(2) marginals have cube kernels;
* logarithmic proper local scopes have odd-holonomy pseudoassignments;
* fixed local phase lifts are either incomplete or gauge-trivial;
* all-pairs/full-intersection scopes have charged-incidence zero-residual cheats;
* exact pointed tensoring multiplies distance but explicit size destroys the exponent; fixed code-oblivious sampling is exponentially large, while naive dense folds admit mixed-tensor cheats;
* residual scaling/coding cannot see an alternative exact-fiber point.

Give exactly ONE falsifiable construction, not a survey. Preferred form: an explicit integer matrix/basis and target, or binary syndrome matrix and target, in which a satisfying assignment has a sparse/short witness but a false clause cannot be repaired by any constant-norm affine combination. The clause-validity signal must be genuinely global (for example, a high-degree global polynomial, determinant/resultant, or code-dependent dense functional), yet the full matrix and target must be output in polynomial time and size.

Required deliverables:

1. exact rows, columns/coefficient variables, target, norm, and dimensions;
2. completeness witness and exact cost;
3. intended soundness invariant against arbitrary integer/GF(2) coefficient superpositions—not only Boolean witnesses or pure tensors;
4. smallest end-to-end hostile test on the all-eight-clause core, including what low-weight search to implement;
5. parameter accounting showing where an `N^c` gap could come from;
6. explicitly identify any unproved lemma.

If no construction survives your own all-eight-core attack, give one sharp no-go theorem about global high-degree polynomial/determinantal linearizations and a finite test. Do not offer another local gadget or generic research direction.
