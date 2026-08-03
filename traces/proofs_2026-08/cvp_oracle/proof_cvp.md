# PCP-free polynomial-factor hardness for Euclidean CVP

## Current status

The requested hardness theorem remains unproved. This file claims no progress on goal (a), (b), or (c). It records conditional transfer tools and proved negative results about candidate amplifications because they constrain subsequent work.

## Exact syndrome-to-CVP identity (conditional transfer tool)

Let \(H\in\mathbb F_2^{r\times N}\), let \(t\in\operatorname{im}H\), and choose \(v\in\{0,1\}^N\) with \(Hv=t\). Define the full-rank integer lattice
\[
 \Lambda_H=\{z\in\mathbb Z^N:Hz=0\pmod2\}.
\]
Then
\[
 \operatorname{dist}_2(v,\Lambda_H)^2
 =\min\{|e|:e\in\mathbb F_2^N,\ He=t\}.
\]
Indeed, for \(z\in\Lambda_H\), the residue \(e=(v-z)\bmod2\) has syndrome \(t\), and each coordinate with \(e_i=1\) contributes at least one to \(\|v-z\|_2^2\). Conversely, for a binary \(e\) of syndrome \(t\), the integer vector \(z=v-e\) lies in \(\Lambda_H\) and has squared distance exactly \(|e|\).

An explicit basis is obtained by row reducing and permuting columns so that \(H\) has independent-row form \([I_s\mid A]\), where \(s=\operatorname{rank}H\). In those coordinates, the columns of
\[
 B=\begin{pmatrix}2I_s&-\widetilde A\\0&I_{N-s}\end{pmatrix}
\]
lie in \(\Lambda_H\). Their determinant has absolute value \(2^s\), which equals the index of \(\ker(H:\mathbb Z^N\to\mathbb F_2^r)\), so they form a basis; undo the coordinate permutation afterward. Thus a Hamming-weight gap \(\gamma\) transfers to a Euclidean gap \(\sqrt\gamma\) at lattice rank \(N\). This lemma alone supplies no hardness gap.

## Explicit failure of huge residual scaling

Here is a concrete version of the scaling obstruction. Introduce integer one-hot coefficients \((x_{i,0},x_{i,1})\), scale equations \(x_{i,0}+x_{i,1}=1\) by arbitrary \(M\), and for each clause scale
\[
 \ell_1(x)+\ell_2(x)+\ell_3(x)+s_j+2t_j=4
\]
by \(M\). Put unscaled identity coordinates centered at \(1/2\) on every coefficient. A satisfying Boolean assignment has one-hot coefficients and can choose \((s_j,t_j)\in\{0,1\}^2\) for each true-literal count 1,2,3, giving the same baseline squared distance \(R^2\).

For a false clause the exact scaled equation still has the integer solution \((s_j,t_j)=(0,2)\). Its identity contribution is
\[
 (0-1/2)^2+(2-1/2)^2=5/2
\]
instead of the Boolean baseline \(1/2\): additive squared cost exactly 2, independent of \(M\). On the all-eight-clause core every assignment violates exactly one clause, so an exact-fiber point has squared distance at most \(R^2+2\). Adding \(D\) disjoint satisfiable clauses makes \(R^2\to\infty\) while preserving this one-clause cheat, and the ratio tends to one. Exact residual evaluations up to \(D=1000\) and \(M=10^6\) are in `experiments/verify_scaled_integer_cvp.py`.

This example extends to every linear slack gadget whose clause interface depends affinely on the true-literal count. Suppose exact witnesses \(w_1,w_2\) for counts one and two obey
\[
 h+Aw_1=t,\qquad 2h+Aw_2=t.
\]
Then the false-count witness
\[
 w_0=2w_1-w_2
\]
obeys \(Aw_0=t\) exactly, with \(\|w_0\|\le2\|w_1\|+\|w_2\|\). Thus whenever consecutive satisfying counts have short exact slack witnesses, count zero has a constant-combination exact witness. Stacking rows, changing moduli, or scaling residuals does not alter this identity. Exact randomized integer checks are in `experiments/verify_slack_extrapolation.py`.

The same statement holds for every bounded-degree polynomial dependence on a count. If a module-valued map \(p(c)\) has degree at most \(d\), then its vanishing \((d+1)\)-st finite difference gives
\[
 p(0)=\sum_{c=1}^{d+1}(-1)^{c+1}\binom{d+1}{c}p(c).
\]
The coefficient \(\ell_1\)-sum is \(2^{d+1}-1\), constant for constant \(d\). Therefore a gadget with short exact witnesses at \(d+1\) satisfying count values yields a constant-combination witness at the forbidden count. Checks through degree seven are in `experiments/verify_polynomial_slack_extrapolation.py`.

This is not a no-go theorem for every integer CVP gadget: a nonlinear joint clause interface of degree at least its number of independently variable inputs can evade bounded-degree extrapolation. It proves that huge equation weights cannot amplify the broad class of bounded-degree count/slack encodings inside a nonempty exact affine fiber.

## Universal affine extrapolation inside a lattice

The preceding local phenomena reflect a general geometric fact. If \(p_0,p_1\in L\) are lattice points, then \(p_2=2p_0-p_1\in L\). For every target \(t\),
\[
 \|p_2-t\|_2
 =\|2(p_0-t)-(p_1-t)\|_2
 \le2\|p_0-t\|_2+\|p_1-t\|_2.
\]
Hence two legal branch points within radius \(R\) automatically create an affine extrapolation point within radius \(3R\). More generally, an integer affine combination \(\sum_i\lambda_i p_i\), \(\sum_i\lambda_i=1\), lies within \((\sum_i|\lambda_i|)R\) when all \(p_i\) do.

Therefore no local lattice gadget can make two exact Boolean branches short while making every integer affine extrapolation polynomially farther away; global coupling must ensure extrapolated local branches cannot be combined into a globally admissible short point. This explains why constant-factor affine and finite-difference trades recur across the candidate reductions. The bound is sharp up to equality; 2000 finite lattice checks are in `experiments/verify_affine_lattice_extrapolation.py`.

## A counterexample to logarithmic connected-view amplification

### Candidate system

Given a CNF \(F\), let \(\mathcal Q_d\) contain every nonempty connected set of at most \(d\) clauses in the clause-intersection graph. For every \(Q\in\mathcal Q_d\), let \(A_Q\) be its satisfying assignments, restricted to variables appearing in \(Q\). A binary connected-view pseudoassignment is a family
\[
 \mu_Q:A_Q\to\mathbb F_2
\]
with odd mass \(\sum_a\mu_Q(a)=1\), whose marginals agree under every connected one-clause deletion \(Q'\subset Q\). Its weight is \(\sum_Q|\operatorname{supp}\mu_Q|\). These are exactly the solutions of the syndrome instance implemented in `experiments/connected_views.py`.

### Theorem (odd permutation-cycle obstruction)

For every integer \(n\ge3\) and every integer \(d\) with \(1\le d<n\), there is an unsatisfiable exact 3CNF \(F_n\) with \(19n\) clauses, \(12n\) variables, and maximum variable occurrence 13 whose depth-\(d\) connected-view system has an exact pseudoassignment of weight at most \(3|\mathcal Q_d|\).

#### Construction

Take a cycle with vertices \(0,\ldots,n-1\), and give each vertex a color in \(\mathbb Z/3\mathbb Z\). Every edge except \((n-1,0)\) requires equal endpoint colors; the last requires
\[
 c_0=c_{n-1}+1\pmod3.
\]
Use Boolean one-hot variables \(X_{v,c}\). At each vertex include one ternary at-least-one clause and the three binary at-most-one clauses. For each edge and color, encode the required equivalence by its two binary implications. Replace every binary clause \(B\) by
\[
 (B\vee z_B)\wedge(B\vee\neg z_B)
\]
using a fresh padding variable. There are \(7n\) vertex clauses and \(12n\) edge clauses. There are \(3n+9n=12n\) variables. Every color variable occurs once in the at-least-one clause, four times in padded at-most-one clauses, and four times for each incident edge, hence 13 times; every padding variable occurs twice.

The formula is unsatisfiable: one-hot clauses give one color at each vertex, equivalences propagate one color around the cycle, and the last edge then requires \(c=c+1\).

#### Local skeletons

Attach each vertex clause to its vertex and each edge clause to its edge. For a clause set \(Q\), let \(T(Q)\) be the union of its attachments, including endpoints of attached edges. If two clauses intersect, their attachments intersect: either they share a color variable at a common endpoint, or they are the padded pair sharing their private \(z_B\) and have the same attachment. Thus connected \(Q\) has connected skeleton \(T(Q)\).

If \(|Q|<n\), then \(T(Q)\) omits some cycle edge: including every underlying edge requires at least one distinct attached clause for each of the \(n\) edges. Hence \(T(Q)\) is a tree (a path or a vertex).

#### Odd tree measure

For each such \(Q\), the edge permutations on \(T(Q)\) have exactly three consistent colorings: choosing one root color uniquely propagates to the tree. For each coloring \(\sigma\), let \(a_{Q,\sigma}\) be the Boolean view that uses its one-hot color values and sets all padding variables to zero. This view satisfies \(Q\). Define
\[
 \mu_Q=\sum_{\sigma\in\operatorname{Col}(T(Q))}
       \delta_{a_{Q,\sigma}}
 \quad\text{over }\mathbb F_2.
\]
Collisions among restricted views are combined modulo two. Its mass is nevertheless \(3=1\pmod2\), and its support has size at most three.

If connected \(Q'\subset Q\), then restriction is a bijection from the three colorings of \(T(Q)\) to those of \(T(Q')\): a color at any vertex of the nonempty subtree determines both colorings uniquely. The Boolean encodings commute with restriction. Therefore the marginal of \(\mu_Q\) is exactly \(\mu_{Q'}\). This proves all required equations and the total weight bound.

### Consequence

For every fixed \(C,\eta>0\), put \(d=\lfloor C\log(19n)\rfloor\). Choose \(n\) sufficiently large that \(1\le d<n\) and \((19n)^\eta>3\). The theorem supplies weight at most \(3K<K(19n)^\eta\), where \(K=|\mathcal Q_d|\). This contradicts the proposed universal lower bound \(KM^\eta\). Thus this particular connected-view hierarchy cannot generate the claimed universal polynomial gap.

The finite generator and direct equation checks are in `experiments/verify_odd_cycle_counterexample.py`.

### Unary GF(2) marginals are intrinsically nonintegral

For alphabets \(A,B\) with at least two elements, map a joint table \(x\in\mathbb F_2^{A\times B}\) to its row marginals, column marginals, and total coverage. For distinct \(a_0,a_1\in A\), \(b_0,b_1\in B\), the four-corner rectangle
\[
 e_{a_0,b_0}+e_{a_0,b_1}+e_{a_1,b_0}+e_{a_1,b_1}
\]
lies in the kernel: every affected marginal and total coverage occurs twice. Consequently any feasible odd joint table can be toggled by such rectangles without changing any unary equation. In particular, a singleton can become a three-supported table with identical marginals. This elementary kernel is exactly the splice used by many low-weight cheating solutions above.

Thus no system enforcing factor consistency only through unary GF(2) marginals can make factor tables integral. More generally, on a \(k\)-bit joint table the sum of all \(2^k\) cube vertices lies in the kernel of **every** marginal of arity less than \(k\): fixing any proper coordinate set leaves an even number of extensions. Full-arity information is necessary to eliminate this universal parity-cube kernel. This is the marginal version of the finite-difference obstruction and explains why escalating from unary to bounded-order overlaps merely moves the cheat to a larger cube. Exact checks through arity eight are in `experiments/verify_pairwise_marginal_kernel.py`; the unary rectangle checks are in `verify_mod2_marginal_nonintegrality.py`.

### Constant random scopes do not even cover local overlap structure

For an \(n\)-edge cycle, choose \(m=\alpha n\) independent uniformly random \(d\)-edge scopes. A fixed adjacent edge pair lies in one scope with probability
\[
 \frac{d(d-1)}{n(n-1)}.
\]
Its expected number of containing scopes is \(\alpha d(d-1)/(n-1)\), tending to zero for constant \(\alpha,d\). The expected **total** number of adjacent-pair hits over the whole cycle is asymptotic to \(\alpha d(d-1)\), only constant, so linearly many adjacent pairs remain completely uncovered. Therefore constant-size, linear-count random scopes cannot reconstruct a long cycle through higher-order intersections. To cover every adjacent pair with high probability by this sampling scheme needs roughly
\[
 m=\Omega\!\left(\frac{n^2\log n}{d^2}\right).
\]
This elementary coverage obstruction explains the exact fibers observed for long holonomy cycles. It does not prove that adjacent-pair coverage suffices for soundness. For constant \(d\), the required \(m=\Theta(n^2\log n)\) is still polynomial and each scope has only constant many views, so coverage arithmetic alone does not kill the route; it says linear-size sampling is insufficient. If \(d=\Theta(\log n)\), view enumeration remains polynomial but with a substantial exponent, while \(d=\Theta(\sqrt n)\) is already superpolynomial. Tables are checked in `verify_random_scope_coverage_stats.py` and `verify_random_scope_edge_scaling.py`.

### Explicit full-view arity spends the gap in output size

The parity-cube kernel suggests using full-arity columns on scopes of size \(r\). An explicit truth-table group then has \(2^r\) columns. To make the smallest universal cube trade polynomial, say \(2^r\ge N^c\), requires \(r\ge c\log_2N\), and the group itself already contributes at least \(N^c\) output coordinates. This arithmetic alone does not rule out a gap—output remains polynomial for fixed \(c\)—but it shows there is no free amplification: the same exponent appears in both the hoped-for trade penalty and the output dimension. Moreover, the odd-holonomy construction shows that full-view columns on logarithmic proper scopes can still have support three, so large local truth tables do not imply large soundness. Finite parameter checks are in `experiments/verify_arity_output_tradeoff.py`.

### Disconnected scopes do not help with unary consistency

The same odd-orbit obstruction is not inherently about connected scopes. On the inconsistent 3-color translation cycle, let \(Q\) be **any** proper subset of cycle-edge constraints, possibly disconnected. Its constraint graph is a forest. Choose one satisfying coloring \(a_Q\) and take its three global color translates \(a_Q+r\), \(r\in\mathbb Z/3\mathbb Z\). Their GF(2) sum has odd mass and support at most three. At every variable, its unary marginal contains each of the three colors exactly once, independent of \(Q\). Therefore these local orbit sums agree with one common global unary marginal for arbitrary proper scopes.

Consequently, replacing connected scopes by random/disconnected scopes while enforcing only variable-wise consistency does not defeat odd holonomy, even if every cycle edge appears in many scopes. To expose the contradiction, some selected object or higher-order overlap structure must collectively retain the whole cycle; unary consistency alone cannot. Exact checks on 500 arbitrary proper scopes are in `experiments/verify_disconnected_unary_orbit.py`.

## Affine parallelogram obstruction for local integer gadgets

Let \(g:\{0,1\}^k\to A\) be the restriction of an affine map \(g(x)=Mx+c\), where \(A\) is any abelian group or module. Fix \(u\in\{0,1\}^k\) and two distinct coordinates \(i,j\). Let \(a,b,c'\) be obtained from \(u\) by flipping coordinate \(i\), coordinate \(j\), and both coordinates, respectively. Coordinatewise over the integers,
\[
 a+b-c'=u,
\]
and because the affine coefficients sum to \(1+1-1=1\),
\[
 g(a)+g(b)-g(c')=g(u).
\]
Thus a local lattice dictionary containing columns for every Boolean view except a forbidden \(u\) cannot exclude \(g(u)\): three allowed columns with coefficients \(1,1,-1\) represent it exactly. If coefficient norm is charged in the ordinary Euclidean way, this replacement costs squared norm 3 versus 1, only a constant factor. The identity survives reduction modulo every integer and every choice of affine signature rows.

This does not exclude nonlinear embeddings followed by linear constraints, but it rules out repairing the local-view gadget merely by moving from GF(2) to integer lattices, changing characteristic, duplicating affine signatures, or assigning huge weights to residual coordinates. Finite randomized identity checks are in `experiments/verify_affine_parallelogram.py`.

### Bounded-degree extension

More generally, let \(g:\{0,1\}^k\to A\) be the restriction of a polynomial map of total degree at most \(d<k\), for a module \(A\) over any commutative ring. Fix \(u\), choose \(J\subseteq[k]\) with \(|J|=d+1\), and write \(u^S\) for \(u\) with coordinates in \(S\subseteq J\) flipped. Then
\[
 \sum_{S\subseteq J}(-1)^{|S|}g(u^S)=0,
\]
so
\[
 g(u)=\sum_{\varnothing\ne S\subseteq J}(-1)^{|S|+1}g(u^S).
\]
To prove it, substitute \(x_i=u_i+(1-2u_i)z_i\) on \(J\). The resulting polynomial in the \(d+1\) flip variables has degree at most \(d\), so its full mixed finite difference—the displayed alternating sum—is zero.

Thus a forbidden local column is represented exactly by at most \(2^{d+1}-1\) other cube vertices with coefficients \(\pm1\), at squared integer coefficient norm \(2^{d+1}-1\). The relation survives every subsequent linear row mixing, modular reduction, and linear tensor folding. In particular, arbitrary mixed tensors—not only pure powers—preserve its tensor powers. The all-eight-clause core therefore defeats every degree-at-most-two signature of its three-bit local view: the forbidden view is replaced by the other seven views, preserving the coverage coefficient because the replacement coefficients sum to one. This is still only a constant penalty.

The universal monomial matrix and 400 exact finite-difference checks for \(2\le k\le6\) are in `experiments/verify_finite_difference.py`. This theorem does not rule out genuinely global columns or full-degree signatures; the earlier odd-holonomy counterexample separately defeats full local marginals on subcycle scopes.

For a 3-clause the degree threshold is sharp. The cubic violation indicator
\[
 v(x_1,x_2,x_3)=(1-x_1)(1-x_2)(1-x_3)
\]
is one on the forbidden view and zero on all seven legal views, so it separates the forbidden column from their span. Its third mixed finite difference is nonzero, proving it cannot be expressed as a sum of unary interface signatures. Exact rank tests remain unchanged after adjoining extra local variables: degree at most two is cheatable, while including the clause's cubic monomial separates. Thus defeating the local trade requires genuinely joint clause information; making that joint information agree with separately chosen global variable values by linear equations is precisely the nonlinear consistency bottleneck. Checks for scopes of 3 through 8 bits are in `experiments/verify_high_order_clause.py`.

## Phase-lift gauge obstruction

A natural attempt to leave the polynomial-signature framework is to replace each incidence bit by a phase label. Let a variable-value column use phase \(y_{i,b}\in\mathbb Z/q\mathbb Z\), and let a clause-view column \((j,a,z)\) meet occurrence \(r\) at phase
\[
 z+\alpha_{j,a,r}.
\]
The canonical one-column-per-variable-and-clause witness for Boolean assignment \(b\) requires, in every clause,
\[
 y_{i(j,r),b_{i(j,r)}}=z_j+\alpha_{j,b|_{C_j},r}\quad(r=1,2,3).
\]
Arbitrary phases can increase the minimum local trade, but these equations introduce holonomy and can reject satisfiable formulas (as the exact finite tests in `experiments/verify_phase_lift_completeness.py` demonstrate). Quantitatively, fix one Boolean assignment and its selected variable-clause incidence graph with \(E\) edges, \(V\) vertices, and \(c\) connected components. If the selected edge labels are independent uniform elements of a group of order \(q\), exactly \(q^{V-c}\) of the \(q^E\) labelings are potential differences, so the lift probability is
\[
 q^{-(E-V+c)}.
\]
The exponent is the cycle rank. For the unique-SAT seven-clause core used in the experiments, \(E=21,V=10,c=1\), hence probability \(q^{-12}\); zero lifts among 1000 deterministic samples at each \(q=2,3,5\) is consistent with this exact count. Thus independent random phases lose completeness exponentially in incidence-cycle rank.

Under a natural copy-stable type model this obstruction is exact. Let a bipartite graph have left vertices equal to variable-interface types and right vertices equal to legal clause-view types, with edge label \(\alpha_{\ell,\rho}\). Assume every alternating type cycle can be realized by a satisfiable transformed formula and selected assignment. Universal phase completeness implies zero alternating holonomy on every cycle: subtract the two incidence equations at each right vertex and sum around the cycle. Choosing a spanning forest then gives potentials \(\beta_\ell,\gamma_\rho\) with
\[
 \alpha_{\ell,\rho}=\beta_\ell-\gamma_\rho.
\]
Indeed, propagate potentials along tree edges; zero holonomy on each fundamental cycle verifies every non-tree edge. Thus every copy-stable universally complete phase system in this model is a coboundary.

The coboundary form is
\[
 \alpha_{j,a,r}=\beta_{i(j,r),a_r}-\gamma_{j,a}.
\]
But setting \(y'_{i,b}=y_{i,b}-\beta_{i,b}\) and \(z'_{j,a}=z_{j,a}-\gamma_{j,a}\) transforms every incidence equation into \(y'=z'\). Thus coboundary phase lifts are merely coordinate relabelings of the original gadget and inherit its three-view cheat exactly. For such a coboundary, choose the three legal views in the original affine triple and give each its phase \(z=\gamma_{j,a}\). Every port then appears at phase \(\beta_{i,a_r}\), so the same GF(2) support-three cancellation reproduces the forbidden boundary, including the odd clause-coverage bit. Hence the all-eight-clause instance again has weight 13 against completeness weight 11.

This classifies phase systems only under the stated copy-stability, cycle-realization, and single-valued local-interface assumptions. Global cycle-dependent selectors lie outside the theorem. Exact finite spanning-forest and support-three checks are in `experiments/verify_phase_cocycle.py`.

A finite menu of global seeds does not evade the same dichotomy within this model. If universal completeness means that for every realized satisfying incidence graph at least one seed lifts, every seed with nonzero holonomy on that graph is unusable; any usable zero-holonomy seed is a coboundary on that graph and its selected columns admit the support-three trade. Thus choosing among polynomially many fixed local phase tables cannot simultaneously certify completeness and give local soundness on a cycle that realizes all their relevant type cycles. The caveat remains quantificational: a graph-dependent seed family might avoid having one seed universally complete, and ruling that out requires a hitting/diagonalization argument not supplied here. Finite seed-family checks are in `experiments/verify_seed_phase_dichotomy.py`.

## Petersen counterexample to the all-pairs hierarchy

The deterministic all-singleton/all-pairs hierarchy with full shared-variable marginals is not exact. Let \(G\) be the cubic Petersen graph, orient its 15 edges arbitrarily, put a variable \(x_e\in\mathbb F_3\) on each edge, and at each vertex impose the signed incidence equation
\[
 \sum_{e\text{ out of }v}x_e-\sum_{e\text{ into }v}x_e=b_v,
\]
where \(b_0=1\) and all other charges vanish. The instance is unsatisfiable because summing all ten equations cancels every edge variable but leaves right side one.

For every vertex singleton or vertex pair \(Q\), let \(S_Q\) be all assignments to incident edge variables satisfying the equations in \(Q\), and select **all** columns of \(S_Q\) over GF(2). Singleton groups contain \(3^2=9\) columns; adjacent pairs contain \(3^3=27\); nonadjacent pairs contain \(3^4=81\). All counts are odd, so coverage holds, and total support is
\[
 10\cdot9+15\cdot27+30\cdot81=2925.
\]

It remains to justify every pairwise marginal. For groups \(Q,R\), let \(W\) be the shared edge-variable set. A linear combination of the incidence rows indexed by \(Q\) whose support lies in \(W\) is exactly a combination of rows indexed by \(Q\cap R\). If \(Q,R\) are disjoint and both coefficients in a two-row combination are nonzero, support containment would force a 4-cycle; Petersen has girth five. If they intersect, the nonshared vertex has degree three but at most two possible neighbors in the other group, leaving an uncancelled edge outside \(W\). Therefore the projections of \(S_Q,S_R\) to \(W\) obey exactly the common equations indexed by \(Q\cap R\), hence are equal. Every nonempty projection fiber has size a power of three and therefore odd, so the all-ones GF(2) marginals are precisely the indicators of these equal projections.

Thus the hierarchy has zero residual on an unsatisfiable bounded-arity CSP. The explicit matrix has 55 groups, 2925 columns, and 23680 rows; `experiments/verify_petersen_pair_counterexample.py` checks the all-ones syndrome exactly and separately verifies the summed-equation UNSAT certificate. A Boolean arity-six relation follows by encoding each trit with two bits. Consequently residual coding cannot amplify this hierarchy: its counterexample residual is already zero.

This is scalable: take a disjoint union of \(s\) Petersen graphs and put total charge one in one component. The graph remains cubic and has no 4-cycle, so the same support/projection proof applies to every singleton/pair group, including groups spanning components. With \(N=10s\) vertex constraints, the pseudoassignment weight is
\[
 9N+27\cdot\frac{3N}{2}+81\left(\binom N2-\frac{3N}{2}\right)=\Theta(N^2),
\]
while the number of groups is \(K=N+\binom N2=\Theta(N^2)\); their ratio tends to 81. Thus the zero-residual cheat has only constant-factor weight over the canonical one-column-per-group baseline, on an infinite bounded-arity family. Exact support checks for one through three components are in `experiments/verify_petersen_family.py`.

### Every fixed scope level fails at some bounded arity

The argument generalizes. Fix \(k\ge1\), take the complete graph \(K_{2k+1}\), put GF(3) edge variables and charged incidence equations as above, and include every group of at most \(k\) vertex constraints with full intersection marginals. The global system is inconsistent by total charge one.

For groups \(Q,R\), \(|Q|,|R|\le k\), suppose a combination of incidence rows indexed by \(Q\) is supported on the shared edge variables \(U_Q\cap U_R\). If some \(v\in Q\setminus R\) has nonzero coefficient, choose \(w\notin Q\cup R\), possible because \(|Q\cup R|\le2k<2k+1\). Edge \(vw\) lies outside \(U_R\), while its combination coefficient is the nonzero coefficient at \(v\), contradiction. Hence only rows indexed by \(Q\cap R\) occur. As before, projected affine solution spaces agree and every nonempty fiber has odd size, so selecting all local solutions gives an exact GF(2) pseudoassignment.

Therefore for every constant hierarchy level \(k\), all scopes through size \(k\) fail on a finite CSP of arity \(2k\) (or Boolean arity \(O(k)\) after encoding trits). This does not by itself refute growing \(k=\Theta(\log n)\) for fixed-arity 3SAT, because the hostile constraint arity grows with \(k\). It does prove there is no universal fixed-level bounded-arity-independent exactness theorem. Exact support checks for \(k=1,2,3\) are in `experiments/verify_connectivity_hierarchy_counterexample.py`.

## A useful but insufficient tensor lemma

Let \(D\leq\mathbb F_2^L\) be a linear code with a distinguished coordinate \(*\), assume some \(x\in D\) has \(x_*=1\), and define its pointed distance
\[
 \delta_*(D)=\min\{|x|:x\in D,\ x_*=1\}.
\]
For the tensor code \(D^{\otimes q}\), distinguish coordinate \((*,\ldots,*)\).

### Lemma
\[
 \delta_*(D^{\otimes q})=\delta_*(D)^q.
\]

### Proof

It suffices to prove the binary product step. Regard a word \(W\in D\otimes E\) as a matrix whose columns lie in \(D\) and rows lie in \(E\). Suppose \(W_{*,*}=1\). Its distinguished column is a word of \(D\) with distinguished bit 1, so at least \(\delta_*(D)\) row indices \(i\) have \(W_{i,*}=1\). For each such \(i\), row \(i\) is a word of \(E\) with distinguished bit 1 and therefore has at least \(\delta_*(E)\) nonzeros. The rows are disjoint coordinate sets, whence
\[
 |W|\ge\delta_*(D)\delta_*(E).
\]
Equality is achieved by tensoring pointed minimum words. Induction proves the claim.

Given an affine coset \(t+C\subseteq\mathbb F_2^N\), its homogenization
\[
 D=\operatorname{span}\{(c,0):c\in C\}+\operatorname{span}\{(t,1)\}
\]
has pointed distance \(1+\min_{c\in C}|t+c|\). Thus tensoring exactly multiplies affine nearest-codeword optima after adding the distinguished coordinate.

This does **not** presently yield polynomial-factor hardness. If the base reduction has YES/NO pointed distances \(K+1\) and \(K+2\), then \(q\) powers give ratio \(((K+2)/(K+1))^q\) and block length \((N+1)^q\). Relative to that final length, the power exponent is
\[
 \frac{\log(1+1/(K+1))}{\log(N+1)},
\]
independent of \(q\), and it tends to zero in the relevant regime. Moreover, if \(N\) is at least a fixed positive power of the SAT input length, polynomial output permits only bounded \(q\). No compression lemma is claimed.

## Pure-power subcode: exact distance but still bad size

Define the pure-power subcode
\[
 P_q(D)=\operatorname{span}\{x^{\otimes q}:x\in D\}\subseteq D^{\otimes q}.
\]
It has the same pointed distance \(\delta_*(D)^q\): containment in the full tensor code gives the lower bound by the preceding lemma, while the pure power of a pointed minimum word gives equality. Thus discarding all genuinely mixed generators does not damage pointed distance.

Every pure power, and hence every word in \(P_q(D)\), is invariant under permutation of tensor positions. One may puncture to one representative of each coordinate orbit, indexed by multisets of size \(q\) from \([L]\), obtaining length
\[
 M=\binom{L+q-1}{q}.
\]
If \(W\) is symmetric, each retained nonzero represents an orbit of size at most \(q!\), so the punctured pointed distance is at least \(\delta_*(D)^q/q!\). This elementary symmetric-representative compression is therefore sound up to \(q!\), but it still does not give the desired parameters. When \(L\) is at least a fixed positive power of the SAT input length, polynomial output length \(\binom{L+q-1}{q}\) forces bounded \(q\); any growing \(q\le L\) gives at least \((L/q)^q\), and \(q>L\) is larger still. Bounded \(q\) cannot amplify an additive \(K+1\) versus \(K+2\) gap to a polynomial factor. Exact tiny-code checks are in `experiments/verify_pure_power_span.py`.

## No fixed coordinate sample uniformly preserves adjacent pure-support layers

A natural compression keeps only a multiset \(S\subseteq[L]^q\) of \(m\) tensor coordinates. Its explicit image generator can be computed without materializing the tensor: at level \(h\), take coordinatewise products of the current image rows with rows \((G_{a,\alpha_{j,h}})_{j\le m}\), then row-reduce. The intermediate rank is at most \(m\).

Fix one coordinate sample that includes a designated all-star coordinate. The following elementary obstruction already holds for one-dimensional pointed codes. Let \([L]=\{*\}\sqcup U\), \(|U|=N\), and \(D_Z=\operatorname{span}(1_{\{*\}\cup Z})\). For sampled tuple \(\alpha_j\), let \(T_j\subseteq U\) be the set of its nonstar symbols. The sampled pointed distance is
\[
 f(Z)=|\{j:T_j\subseteq Z\}|.
\]
For \(d\le N\), put \(C_d=\max_{|X|=d-1}f(X)\) and \(B_d=\min_{|Y|=d}f(Y)\).

### Sampling lemma

If \(1\le s\le d\le N\) and \(m(d/N)^s<1\), then
\[
 (d-s+1)B_d\le dC_d.
\]
Because the all-star coordinate is sampled, \(C_d\ge1\), so division also gives \(B_d/C_d\le d/(d-s+1)\).

### Proof

A uniformly random \(d\)-set \(Y\) contains any fixed \(T_j\) of size at least \(s\) with probability at most \((d/N)^s\). A union bound therefore gives a \(Y\) for which every counted \(T_j\subseteq Y\) has size at most \(s-1\). For each \(y\in Y\), let \(X_y=Y\setminus\{y\}\). Double counting gives
\[
 \sum_{y\in Y}f(X_y)
 =\sum_{j:T_j\subseteq Y}(d-|T_j|)
 \ge(d-s+1)f(Y).
\]
The left side is at most \(dC_d\), while \(B_d\le f(Y)\), proving the result.

Consequently, a **strict** uniform ratio greater than \(R>1\) between layers \(d-1\) and \(d\) requires
\[
 m\ge (N/d)^{\lfloor d+1-d/R\rfloor}.
\]
For a non-strict ratio at least \(R\), the justified exponent is \(\lceil d+1-d/R\rceil-1\). For \(d=K+1\), \(N/d\ge1+\varepsilon\), and either convention at \(R=2\), this is exponential in \(K\).

The quantifiers are important: this rules out a **fixed, code-oblivious** coordinate sample required to work uniformly over all one-dimensional codes \(D_Z\). It does not rule out samples selected as a function of the input code, a compressor tailored to a particular reduction family, or arbitrary dense linear functionals on tensor space.
