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

## An explicit global CRT coupling still has a constant local repair

The preceding failure is not repaired merely by coupling every Boolean variable through one global integer. Let the formula have Boolean coefficients \(b_1,\ldots,b_n\), choose distinct odd primes \(p_i\), and put \(P=\prod_i p_i\). Introduce one global coefficient \(X\) and quotients \(q_i\), with scaled rows
\[
 M(X-p_iq_i-b_i)=0.
\]
Every Boolean assignment has a unique representative \(0\le X<P\) by the Chinese remainder theorem. For each clause retain the scaled exact equation
\[
 M(\ell_1(b)+\ell_2(b)+\ell_3(b)+s_j+2t_j)=4M.
\]
Add identity rows \(2b_i\) and \(2s_j,2t_j\), all targeted at one, and the global row \(2X\) targeted at \(P\). These rows and the constraint rows form an explicit integer matrix \(B\); its columns are a lattice basis because they are linearly independent. Indeed, a coefficient-kernel vector has all \(b_i,s_j,t_j=0\) from the identity rows, then \(X=0\) from the global row, and finally every \(q_i=0\) from its private CRT row.

For every satisfying assignment, choose the CRT representative and Boolean clause slacks
\[
 (s_j,t_j)=(1,1),(0,1),(1,0)
 \quad\text{at true-literal counts }1,2,3.
\]
All scaled rows are then exact. The identity contribution is \(n+2m\), while \((2X-P)^2\le P^2\). Thus
\[
 R^2=P^2+n+2m
\]
is a valid uniform completeness threshold.

Now take the unsatisfiable conjunction of all eight clauses on three variables and append \(D\) disjoint positive clauses. Set the three core bits to zero and every appended bit to one. Exactly the core clause falsified by \(000\) fails. Give it the exact slack \((s,t)=(0,2)\); all other clauses use the Boolean slacks above. Every scaled CRT and clause row is still satisfied exactly, and the false clause contributes ten rather than two in its centered identity rows. Hence this NO instance has a lattice point of squared distance at most
\[
 R^2+8,
\]
independently of \(M\). Its distance ratio is at most \(\sqrt{1+8/R^2}\), which tends to one. The global CRT coordinate actually worsens the baseline because \(P\) is exponential in \(n\), but the decisive point is that it does not alter the additive exact-fiber clause repair. `experiments/verify_crt_global_coupling.py` checks the integer residuals, the additive cost eight, and the explicit dimensions on four instances.

This refutes only this CRT-coupled construction, not every global integer encoding. It demonstrates that global assignment uniqueness is irrelevant if clause soundness is still mediated by an affine local slack fiber.

## Bounded-fan-in circuit tableaus inherit a support-three fault

A global high-degree predicate does not evade the preceding obstruction when it is evaluated by a compact bounded-fan-in circuit and then linearized by local gate tables. Consider a feed-forward Boolean circuit. For every source use the two columns indexed by its bit. For each fan-in-at-most-two gate \(g\), use one column for every tuple in the graph of its Boolean function. Add one coverage row per block, affine equality rows between the output marginal of a producer and the corresponding input marginal of its consumer, rows for constants, and an accepting-output row. Let the resulting integer system be \(A\lambda=b\); reducing modulo two gives a syndrome instance.

At a binary OR gate, prepend the coverage coordinate to the two inputs and output. The illegal accepting interface has the exact identity
\[
 (1,0,0,1)
 =(1,0,1,1)+(1,1,0,1)-(1,1,1,1)
 \tag{*}
\]
over the integers. Modulo two, replace the minus sign by plus. All three right-hand tuples are legal OR tuples. Thus replacing a singleton gate column by these three columns preserves coverage and both input wire values but changes the output from zero to one. It costs support three over \(\mathbb F_2\), or squared coefficient norm three over the integers, instead of one. Since (*) is an exact interface identity, arbitrary linear row mixing, scaling, and residual coding preserve it.

This gives an end-to-end fault on the conjunction of all eight clauses over three variables. Use three source blocks, three NOT gates, two binary OR gates per clause, a seven-gate binary AND tree, and a final gate \(\operatorname{AND}(A,1)\). There are
\[
 G=3+3+16+7+1=30
\]
blocks. Their legal tables have
\[
 N=3\cdot2+3\cdot2+16\cdot4+8\cdot4=108
\]
columns. There are 30 coverage rows, 50 driven-wire rows, one constant row, and one acceptance row, hence \(A\in\mathbb Z^{82\times108}\).

Take source assignment \(000\). Exactly clause \(x_1\vee x_2\vee x_3\) is false. Apply (*) to its second OR gate while selecting one ordinary legal column in every other block and the resulting accepting transcript downstream. The binary witness has exact syndrome and weight \(G+2=32\). The signed integer witness has \(A\lambda=b\) and \(\|\lambda\|_2^2=32\). Therefore for the explicit full-column-rank basis
\[
 B=\begin{pmatrix}I_N\\ MA\end{pmatrix},
 \qquad
 t=\binom{0}{Mb},
\]
the same point is at squared distance 32 for every \(M\). Appending disjoint satisfiable circuit components increases the baseline while retaining additive cost two, so no polynomial multiplicative gap arises from this tableau family.

`experiments/verify_circuit_tableau_fault.py` constructs the full matrix, checks both exact witnesses, exhaustively enumerates every binary support-32 pattern permitted by block coverage, and finds 48 accepting one-fault transcripts. It also checks deterministic dense row mixing. This theorem does not cover genuinely global rows that do not factor through affine circuit-wire interfaces. It does rule out the standard compact route of evaluating a determinant, resultant, or other global polynomial by a bounded-fan-in circuit and enforcing its transcript only by such rows.

Even full-degree local truth tables do not become integral merely by changing from GF(2) to integer unary marginals. On the all-eight-clause core, use global variable-value columns and, for each clause, all seven legal local assignments. Impose integer coverage one and equality of every unary marginal. Fix any global assignment \(u\). Seven clauses select \(u\). In the unique clause forbidding \(u\), flip two coordinates to obtain legal views \(a,b,c\) with
\[
 a+b-c=u
\]
coordinatewise and coefficient sum one. Selecting coefficients \(+1,+1,-1\) on these three views preserves clause coverage and every unary marginal exactly. Together with three variable columns and seven ordinary clause columns, this gives support and squared coefficient norm 13. The explicit system has 59 rows and 62 columns; all eight choices of \(u\), dense row maps, and several moduli are checked in `experiments/verify_truth_table_marginal_integer.py`. Thus full local degree separates the forbidden view only before projecting to affine interfaces; unary marginal coupling immediately restores the parallelogram fault.

## Incomplete global Walsh moments admit an exact virtual assignment

Dense rows depending on the entire assignment still fail if they omit even one Walsh character. Let \(\Omega=\{0,1\}^n\), \(q=2^n\), and \(\chi_T(x)=(-1)^{\sum_{i\in T}x_i}\). Form the UNSAT family with one group for every \(u\in\Omega\), whose legal columns are all full assignments \(x\ne u\). Thus every possible global assignment is forbidden by one group. Impose coverage one in every group and equality across groups of the moments indexed by a family \(\mathcal P\) of nonempty characters.

Suppose \(\mathcal P\) omits \(T_0\ne\varnothing\), and fix an anchor assignment \(a\). Every group \(u\ne a\) selects the legal singleton \(a\). In exceptional group \(a\), put
\[
 z_{a,x}=-\frac{\chi_{T_0}(x)}{\chi_{T_0}(a)}\in\{-1,1\}
 \qquad(x\ne a).
\]
Walsh orthogonality gives, for every retained \(T\ne T_0\),
\[
 \sum_{x\ne a}z_{a,x}=1,
 \qquad
 \sum_{x\ne a}\chi_T(x)z_{a,x}=\chi_T(a).
\]
Hence the UNSAT system has an exact signed witness with support and squared norm
\[
 (q-1)+(q-1)=2q-2<2q,
\]
less than twice the canonical one-column-per-group baseline. The rows are genuinely global: each column is a complete assignment and every character may involve all \(n\) bits.

The threshold is sharp over the integers. Coverage plus all \(2^n-1\) nonconstant Walsh characters is the complete invertible Walsh transform over \(\mathbb Q\), so equal moments force all groups to carry one common signed table. Group \(u\) omits \(u\), forcing that table to vanish at every \(u\), contradicting mass one. Therefore exactness requires all \(2^n\) character coordinates—exponential in the size of a genuinely global \(n\)-bit object.

Over GF(2), even all parity-bit moments fail. For \(b_T(x)=\sum_{i\in T}x_i\bmod2\), the sum over all \(x\in\Omega\) of the vector \((1,(b_T(x))_T)\) is zero whenever \(n\ge2\): coverage occurs \(2^n\) times and each parity bit is one \(2^{n-1}\) times. Thus the exceptional group can select all \(x\ne a\), again giving binary weight \(2q-2\), even with every nonconstant parity moment.

For \(n=3\), the system has 56 columns. `experiments/verify_walsh_global_moments.py` checks all 56 omitted-character/anchor integer witnesses, all eight complete-parity GF(2) witnesses, dense row mixing, and exact ranks 56 versus 57 for full integer Walsh infeasibility. This theorem covers Walsh/character rows specifically, not arbitrary dense global functionals. It shows that the most direct global Fourier repair either remains exactly cheatable or explicitly spends exponential output size.

Over any fixed prime field, arbitrary global fingerprints have a rank obstruction. For functions \(f_1,\ldots,f_m:\Omega\to\mathbb F_p\), put
\[
 w(x)=(1,f_1(x),\ldots,f_m(x))\in\mathbb F_p^{m+1}.
\]
If \(q=|\Omega|>m+1\), the \(q\) vectors are linearly dependent. Choose a relation \(\sum_x\lambda_xw(x)=0\) and anchor \(a\) with \(\lambda_a\ne0\). Then
\[
 w(a)=-\sum_{x\ne a}\frac{\lambda_x}{\lambda_a}w(x).
\]
Using singleton \(a\) in all ordinary forbidden groups and the displayed coefficients in exceptional group \(a\) gives an exact field-valued syndrome witness with at most \(q+m\) nonzeros. Hence fewer than \(q-1=2^n-1\) arbitrary global feature rows cannot make the all-forbidden family exact over **any** fixed prime field. Since this model also explicitly contains \(q(q-1)\) complete-assignment columns, both its dictionary and any exact fingerprint closure are exponentially large in \(n\); this is an obstruction analysis, not a polynomial reduction. This theorem is not character-specific and imposes no locality or bounded-entry restriction; it is simply matroid dependence. For binary NCP every nonzero coefficient is one, giving Hamming weight at most \(q+m\). For larger fixed \(p\), centered integer representatives have squared coefficient norm at most \((q+m)(p-1)^2/4\), still constant-field overhead. `experiments/verify_arbitrary_binary_global_fingerprints.py` checks 150 deterministic random binary systems through \(m=q-2\); `verify_arbitrary_prime_global_fingerprints.py` checks primes 2,3,5,7 and dense field row processing; `verify_field_fingerprint_output_accounting.py` checks representative exact exponential-size inequalities.

There is also a basis-independent counting obstruction for arbitrary bounded integer fingerprints. Let \(f_1,\ldots,f_m:\Omega\to[-H,H]\cap\mathbb Z\), \(|\Omega|=q\), and augment each assignment by coverage:
\[
 w(x)=(1,f_1(x),\ldots,f_m(x)).
\]
Every subset sum \(\sum_{x\in S}w(x)\) lies in at most
\[
 (q+1)(2qH+1)^m
\]
integer bins. If
\[
 2^q>(q+1)(2qH+1)^m,
 \tag{BC}
\]
two distinct subsets have the same sum. Their difference gives a nonzero \(\lambda\in\{-1,0,1\}^{\Omega}\) with \(\sum_x\lambda_xw(x)=0\). Choose an anchor \(a\) in its support and divide by \(\lambda_a=\pm1\). Then
\[
 w(a)=-\sum_{x\ne a}(\lambda_x/\lambda_a)w(x).
\]
In the all-assignments-forbidden family, use singleton \(a\) in every ordinary group and this signed table in exceptional group \(a\). It is legal, has exact coverage and every fingerprint moment, and has support/squared norm at most \(2q-2\). Thus any bounded global fingerprint family satisfying (BC) has an exact low-norm virtual assignment, regardless of its algebraic form. Quantitatively, it covers
\[
 m<\frac{q\log2-\log(q+1)}{\log(2qH+1)}.
\]
In particular, if \(q=2^n\), while both the number of rows \(m\) and the bit length \(\log H\) are polynomial in \(n\), then (BC) holds for all sufficiently large \(n\): its left logarithm is \(2^n\), whereas the right logarithm is polynomial in \(n\). Therefore **arbitrary** polynomial-count, polynomial-bit integer fingerprints of the complete assignment are insufficient for exactness in this all-forbidden global-table model. The theorem does not cover encodings whose columns are not complete assignments grouped by forbidden global views; nor does it make this exponentially large model into a reduction. `experiments/verify_bounded_global_fingerprint_collision.py` checks twenty deterministic random \((q,m,H)=(20,2,2)\) families and dense row mixing; `verify_bounded_fingerprint_asymptotics.py` checks representative exact exponent inequalities for polynomial row/bit bounds.

A parallel obstruction applies to global algebraic moments after encoding assignments injectively as integers \(0,\ldots,q-1\). Suppose every forbidden group is required to have common moments \(x,x^2,\ldots,x^d\). For anchor zero and \(d\le q-2\), the finite-difference identity
\[
 \delta_0\equiv
 \sum_{j=1}^{d+1}(-1)^{j+1}\binom{d+1}{j}\delta_j
 \quad\text{on every polynomial of degree at most }d
\]
gives an exact exceptional-group signed table. Together with anchor singletons in the other \(q-1\) groups, its support is \(q+d\), coefficient \(\ell_1\)-cost is \(q+2^{d+1}-2\), and every global moment row is exact. Full degree \(q-1\) is Vandermonde-complete and makes the system inconsistent, but again requires \(q=2^n\) global moments. Thus low-degree global polynomial fingerprints trade row count against exponentially growing finite-difference coefficients rather than giving a free gap; at the exactness threshold they explicitly spend exponential size. `experiments/verify_univariate_global_moments.py` checks every degree zero through seven for \(q=8\), exact dense row mixing, and modular rank certificates 56 versus 57 at full degree.

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

There is an integer analogue that avoids the apparent obstacle that an orbit of size three has mass three rather than one. Use alphabet
\[
 \Omega=A\sqcup B,\qquad |A|=2,\quad |B|=3.
\]
On a cycle, every edge preserves the branch; all but the last are identities, while the last is a fixed-point-free 2-cycle on \(A\) and a fixed-point-free 3-cycle on \(B\). The CSP is globally unsatisfiable. Every proper connected edge scope is a path and has exactly two propagated \(A\)-colorings and three propagated \(B\)-colorings. Define its signed integer local table by coefficient \(-1\) on each \(A\)-coloring and \(+1\) on each \(B\)-coloring. Its mass is
\[
 3-2=1.
\]
Restriction from a path to a nonempty connected subpath bijects the two colorings in branch \(A\) and separately bijects the three colorings in branch \(B\). Hence every signed marginal agrees exactly over the integers. The witness has five nonzero unit coefficients per scope and squared norm \(5K\).

Thus changing the connected-view hierarchy from GF(2) to integer coefficients does not restore integrality: a virtual cardinality-one measure can be built as the difference of two orbit measures. For every depth \(d<n\) this is a zero-residual witness on an UNSAT constant-alphabet permutation CSP. `experiments/verify_integer_mixed_orbit_cycle.py` checks four depths, global fixed-point-freeness, and dense row processing.

The same obstruction has an exact-3CNF realization of bounded occurrence and linear size. Encode each five-valued state one-hot. Encode at-most-one constraints and permutation equivalences by padded binary clauses, and encode the five-way at-least-one constraint by the standard three-clause chain
\[
 (x_0\vee x_1\vee y_1)\wedge
 (\neg y_1\vee x_2\vee y_2)\wedge
 (\neg y_2\vee x_3\vee x_4).
\]
Use a canonical auxiliary assignment determined by the color and set padding bits to zero. As in the three-color construction, intersecting clauses have intersecting attachments, so every connected clause scope has a connected attachment skeleton. If it has fewer than \(n\) clauses, the skeleton omits a cycle edge and is a tree. It therefore has exactly two propagated branch-\(A\) colorings and three branch-\(B\) colorings. Coefficients \(-1\) and \(+1\), respectively, have mass one. Restriction to any connected deletion subtree bijects each branch's colorings separately; canonical Boolean/auxiliary encoding commutes with restriction. Colliding restricted Boolean views are combined over the integers and do not change this pushforward identity.

There are \(23n\) vertex clauses and \(20n\) edge clauses, hence \(43n\) clauses, and \(27n\) variables including fresh padding/chain variables. A color variable occurs at most 17 times; chain and padding variables occur at most two times. Before restriction each scope measure uses five unit coefficients; collisions can only give support at most five and squared coefficient norm at most \(25\) per scope. Thus its total squared norm is at most \(25K\), still only a constant factor over the group baseline.

The implemented finite construction directly checks every deletion marginal. At \((n,d)=(3,1)\) it has 129 clauses and 129 groups; at \((4,2)\) it has 172 clauses, 2724 groups, 15188 rows, and 7636 columns. Both exact signed witnesses pass (`experiments/verify_integer_mixed_orbit_3cnf.py`).

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

### Integer all-pairs hierarchies also fail

The Petersen obstruction has a characteristic-zero analogue. Take two disjoint charged flow branches on the same Petersen graph, one over \(\mathbb F_2\) and one over \(\mathbb F_3\), and include a branch tag in every local view. Both global branches are inconsistent because summing the ten incidence equations gives \(0=1\) in either field.

For every singleton/pair group \(Q\), let \(S_{Q,p}\) be its affine local solution space in branch \(p\). Its cardinality is
\[
 |S_{Q,2}|\in\{4,8,16\},\qquad
 |S_{Q,3}|\in\{9,27,81\}.
\]
Give branch two total signed mass \(m_2=-80\) and branch three total mass \(m_3=81\). Thus the combined group mass is one. Put the uniform integer coefficient
\[
 -80/|S_{Q,2}|
 \quad\text{or}\quad
 81/|S_{Q,3}|
\]
on every local solution in the corresponding branch; divisibility holds for all displayed cardinalities. The support/projection lemma proved for the GF(3) Petersen system is field-independent here and applies separately over \(\mathbb F_2\) and \(\mathbb F_3\). Uniform local solution measures have uniform pushforwards to every common projection. Since each branch's **total** mass is fixed independently of \(Q\), all full-intersection integer marginals agree exactly. Branch tags keep the two measures disjoint.

The resulting UNSAT integer hierarchy has 55 groups, 3565 columns, and 30550 rows. Its exact signed witness has support 3565, maximum coefficient 20, and squared norm 53365. Disjoint unions produce a scalable bounded-arity family. With \(N\) vertex constraints, adjacent pairs number \(3N/2\) and all other pairs are nonadjacent. The witness support divided by the group count tends to 97, while squared norm divided by the group count tends to 481. Thus the exact-fiber cheat remains only a constant factor over the canonical one-column-per-group baseline. `experiments/verify_integer_petersen_pair_counterexample.py` checks the full base matrix, both global inconsistency certificates, and dense integer row processing; `verify_integer_petersen_family.py` checks the scaling formulas.

Thus moving the full-intersection hierarchy from GF(2) to integer coefficients does not restore exactness. Coprime local branch cardinalities provide integral virtual mass one, just as mixed orbit sizes did for connected scopes.

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
