# ROADMAP.md

## Target

Prove, without PCP machinery or unproved conjectures, a deterministic polynomial-time many-one reduction from 3SAT of size \(m\) to Euclidean GapCVP of rank \(n=\operatorname{poly}(m)\) with approximation factor \(n^c\) for an explicit absolute \(c>0\).

Every normalization, legality, consistency, carry, boundary, and auxiliary condition must be emitted as a lattice coordinate. Soundness always quantifies over unrestricted integer coefficients.

The previous robust constant-degree agreement lift is retired. The ordered-pair diagonal splice and \(A_5\) bicyclic fusion show that finite coherence lifts do not become amplifiers merely by adding complete marginals or multiplication tables. Fixed Voronoi shells, fixed local min-plus tiles, literal tensors, group-ring convolution, and incidence-orbit Gram composition remain retired.

---

## Strategy 1 — One-shot logarithmic bag complex with integral cosystolic coercion

Use the finite G38 phenomenon only as evidence for a formula-dependent, logarithmic-width construction. Do not iterate a fixed lift and do not infer an asymptotic theorem from bounded attack enumeration.

### Lemmas

1. **Exact bounded-incidence compilation lemma.**  
   Deterministically transform a 3CNF \(F\) into an equisatisfiable bounded-fanout clause-variable incidence system \(F^\flat\) of size \(O(m^3)\). Equality chains, boundary values, and auxiliary definitions are explicit constraints. Satisfying assignments correspond bijectively after forgetting auxiliaries.

2. **Logarithmic legal-bag construction lemma.**  
   From \(F^\flat\), construct in polynomial time a family \(\mathcal B\) such that:
   - every bag contains at most \(12\lceil\log_2 m\rceil\) variables and polynomially many clauses;
   - each bag has one selector for every assignment satisfying all its clauses;
   - all bag normalizations and complete shared-variable marginals are emitted;
   - the total selector count is \(N=\operatorname{poly}(m)\);
   - honest global assignments induce \(0/1\) sections, each with anchor energy exactly \(B=N\).

   This is a one-shot, formula-dependent complex, not a constant bag family or an iterated agreement lift.

3. **FRONTIER — integral cosystolic coercion lemma.**  
   The construction in Lemma 2 can be chosen so that, for every unsatisfiable \(F^\flat\) and every \(z\in\mathbb Z^N\),
   \[
   A_{\mathcal B}z=b_{\mathcal B}
   \quad\Longrightarrow\quad
   \|2z-\mathbf1\|_2^2\ge N^{1+1/64}.
   \]
   The proof must classify the complete saturated kernel over \(\mathbb Z\), including affine pseudosections, diagonal embeddings, signed cycles, clause drops, and torsion classes. It may use direct integer chain-complex inequalities, but no local-test-to-global-rejection or PCP theorem.

4. **Weighted GapCVP lemma.**  
   Set
   \[
   E(z)=\|2z-\mathbf1\|_2^2+
   W\|A_{\mathcal B}z-b_{\mathcal B}\|_2^2,
   \qquad
   W=\lceil N^{1+1/64}\rceil .
   \]
   A satisfying section has energy \(N\). In a NO instance, a nonzero integral residual costs at least \(W\), while a zero-residual point is covered by Lemma 3. Exact rational factorization produces a Euclidean GapCVP instance of rank \(n=N\), giving
   \[
   \frac{\operatorname{dist}_{NO}}{\operatorname{dist}_{YES}}
   \ge n^{1/128}.
   \]

**Why sufficient.** Lemmas 1–2 give polynomial size and exact completeness. Lemma 3 handles the only dangerous branch—unrestricted zero-residual signed sections. Lemma 4 makes every nonzero residual automatically expensive and yields \(c=1/128\).

**Crux.** Logarithmic bags must force a superlinear integral norm without becoming an implicit polynomial-size enumeration of global assignments. Ordinary real agreement, bounded shells, and finite attack lists are insufficient.

**First experiment.** Couple two copies of the G38 obstruction through one shared variable. Enumerate deterministic bag families with at most 24 bags and bag width at most six. For each family, compute the exact lattice
\[
\{z\in\mathbb Z^N:A_{\mathcal B}z=b_{\mathcal B}\}
\]
by SNF plus branch-and-bound and compare its minimum anchor excess with twice the one-copy value. Reject the mechanism unless some family has strict normalized growth and the complete minimum—not only G13/G15/G19 seeds—certifies it.

---

## Strategy 2 — Ramified quaternion valuation recursion

Replace commutative-field and group-ring recursion by a maximal order in a definite quaternion division algebra. The intended escape is simultaneously multiplicative valuation and a positive-definite reduced norm, without bicyclic zero divisors.

### Lemmas

1. **Balanced semantic-circuit lemma.**  
   Compile \(F\) into a bounded-fanout NAND/COPY circuit of size \(m^{O(1)}\) and depth
   \[
   \lceil\log_2m\rceil\le d\le6\lceil\log_2m\rceil .
   \]
   All fanout copies and the forced accepting output are explicit.

2. **Ramified quaternion gate-library lemma.**  
   Let \(D/\mathbb Q\) be the definite quaternion algebra ramified exactly at \(17\) and \(\infty\), let \(\mathcal O\) be a maximal order, and let \(\mathfrak P\) be its unique prime above \(17\). Construct constant-size NAND/COPY selector modules whose legal configurations:
   - have identical trace-form energy;
   - realize the correct ports modulo \(\mathfrak P\);
   - emit every selector normalization, product-table, glue, carry, and boundary equation.

3. **FRONTIER — ramified adverse-filtration lemma.**  
   For every depth-\(h\) recursively substituted module and every unrestricted integral coefficient vector with false root boundary, either
   \[
   0\ne\alpha\in\mathfrak P^h
   \]
   appears in an emitted defect coordinate, or the charged selector energy is at least the trace energy of such an \(\alpha\). The statement must hold on the complete saturated adverse quotient, including valuation-zero units, affine parity, diagonal signed splices, arbitrary carries, and non-rank-one couplings.

   The proof must use the \(\mathfrak P\)-adic filtration of the order itself; a finite min-plus transfer table is not sufficient.

4. **Reduced-norm growth lemma.**  
   For nonzero \(\alpha\in\mathfrak P^h\),
   \[
   \operatorname{nrd}(\alpha)\ge17^h,
   \qquad
   \operatorname{Trd}(\alpha\bar\alpha)=2\operatorname{nrd}(\alpha).
   \]
   If legal squared energy grows by at most \(16^h\), false-root squared energy gains a factor at least \((17/16)^h\).

5. **Integral realization and accounting lemma.**  
   Expand \(\mathcal O\) in an integral basis and factor its positive-definite trace form rationally. If the recursion has rank at most \(m^{40}\), then
   \[
   \frac{\operatorname{dist}_{NO}}{\operatorname{dist}_{YES}}
   \ge m^{\frac12\log_2(17/16)}
   \ge n^{c_2},
   \qquad
   c_2=\frac{\log_2(17/16)}{80}>0.
   \]

**Why sufficient.** A false forced output creates depth-dependent ideal valuation by Lemma 3. Definiteness converts valuation into Euclidean energy, and logarithmic circuit depth gives a polynomial gap.

**Crux.** Division removes the \(A_5\) nilpotent mechanism, but units and signed selector couplings may still remain valuation-zero. Lemma 3 must exclude them algebraically for every coefficient vector.

**First experiment.** Work first modulo \(\mathfrak P\cong\mathbb F_{17^2}\). Enumerate NAND/COPY selector modules with at most eight selectors and test adverse-graded injectivity by exact finite-field linear algebra. Lift survivors to an explicit maximal-order basis, compose to depth two, and compute the exact unrestricted minimum by SNF and branch-and-bound. Seed the search with DROP, G13, G15, G19, the ordered-pair diagonal splice, and bicyclic-style signed couplings.

---

## Complete obstruction audit

| Recorded obstruction | Strategy 1 escape | Strategy 2 escape |
|---|---|---|
| **G1 RS slack, G6 external quotient, G7 radix kernel, G12/augmented-Gram DROP** | No slack or external filters; all equations are emitted. Zero residual is handled by Lemma 3, nonzero residual by \(W\). | Every carry and boundary is emitted and included in the adverse-filtration dichotomy. |
| **G2 affine/Graver isolation, G3 unbounded fibers, G14 finite pair bags, G31 finite Walsh pass, G38 finite splitter pass** | Requires a saturated all-coefficient theorem for scalable logarithmic bags, not bounded enumeration or fixed bags. | Requires an order-theoretic statement for all coefficients, not shell extrapolation. |
| **G5 private overlap, G9/G11 parity, G13 affine collision, G15 laminar lift** | Complete overlaps plus integral cosystolic norm; affine pseudosections are expressly included. | Included in the complete adverse quotient, including valuation-zero affine units. |
| **G19 signed flow, GD1 diagonal closure, ordered-pair diagonal splice** | No flow or ordered-tuple lift; diagonal classes are audited in the saturated kernel. | Non-rank-one and diagonal signed couplings are explicit cases of Lemma 3. |
| **G28 min-plus failure, G32 additive parity, G37 parity cut** | One-shot coercion, not additive copy composition or a fixed transfer table. | Valuation filtration replaces additive metric and min-plus composition. |
| **G30 tensor isometry** | No tensor product. | No literal tensoring. |
| **GD2/A5 bicyclic units** | No convolution algebra. | A definite quaternion division algebra has no nonzero nilpotents; residual units remain explicitly audited. |
| **G33 bivector incompleteness, G34 metric-repair infeasibility** | No exterior tags or synthesized Gram repair. | Uses the canonical positive trace form of a maximal order. |
| **D4 midpoint, non-antipodal D4 Boolean obstruction, independent-D4 recombination** | No fixed Delaunay shell or separable coordinate geometry. | No Voronoi shell. |
| **E6 bounded-map and unbounded affine-port no-go** | Bags use explicit legal assignment selectors, not affine shell ports. | Ports are residue classes in an emitted module, not affine images of a Delaunay cell. |

---

## Recommendation

Attempt **Strategy 2** first. It directly targets the two newest causal failures: diagonal signed closure and bicyclic zero-divisor fusion. Its first gate is substantially smaller than constructing a general logarithmic bag complex.

**FRONTIER lemma:** ramified adverse-filtration lemma.

**First experiment:** enumerate depth-one gate modules over \(\mathbb F_{17^2}\), lift every survivor to the definite quaternion maximal order, and perform an exact depth-two unrestricted SNF/energy audit including DROP, G13, G15, G19, diagonal-splice, and bicyclic-style attacks.
