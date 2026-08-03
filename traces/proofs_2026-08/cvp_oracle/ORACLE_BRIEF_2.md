# Oracle brief 2: attack the connected-view lemma structurally

Respect the same prohibition as brief 1: do not use, recall, search for, or describe the named recent off-limits document or secondary sources. Do not invoke PCP/Label Cover as a black box.

Your first answer proposed the connected-view hierarchy. For every connected clause set Q of size <=d there are columns indexed by satisfying assignments to Q; exact solutions are GF(2)-valued functions mu_Q of odd total mass, marginally consistent under connected one-clause deletions. Weight is total support over Q. The missing LCV lemma asserted that for some d=C log M every exact solution on an unsatisfiable bounded-degree 3CNF has support at least K M^eta.

I implemented it exactly. Finite evidence:

* all eight clauses on 3 variables: d=1 optimum 8, d=2 exact fiber infeasible;
* inconsistent XOR cycles and K4 Tseitin: d=2 infeasible;
* random UNSAT formulas can have d=2 exact fibers. The fixed formula below is UNSAT by exhaustive enumeration, has K=105 connected scopes at d=2, and exact minimum support 243 (HiGHS certificate/status); at d=3 the fiber is infeasible:

[(2,-1,-4),(2,1,-4),(3,2,-1),(-3,-2,-4),(-1,4,-2),(-2,3,1),(3,-1,-2),(2,3,4),(4,2,1),(4,-3,1),(4,2,-1),(4,2,3),(2,3,-4),(1,3,4)].

Code is in the attached files. Need a high-leverage structural verdict. Either:

(A) Construct an explicit scalable bounded-degree UNSAT family with exact logarithmic-depth mod-2 pseudoassignments of support only K*poly-small (ideally O(K)), thereby refuting LCV. Specify formula/gadget and mu_Q enough to implement, including why every connected <=d subformula is satisfiable and how marginal consistency works. Beware: choosing arbitrary local satisfying assignments is not enough to make overlaps consistent.

or

(B) State and prove the strongest elementary gluing/support lemma actually justified by these GF(2) marginals. Quantify depth, support, and graph assumptions. Explain whether it could yield a polynomial NCP gap with polynomial hierarchy size.

or

(C) If neither, isolate a narrower algebraic invariant to compute next (e.g. relation to polynomial calculus/Sherali-Adams over GF(2)), and give a concrete family plus a falsifiable predicted rank/min-support result.

Be adversarial: the desired answer may be that this route is dead. Do not merely restate LCV or recommend more random search. We need a precise scalable construction or a provable structural lemma.
