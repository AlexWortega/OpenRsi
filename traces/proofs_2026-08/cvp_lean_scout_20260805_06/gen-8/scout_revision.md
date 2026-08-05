I did not search for or consult the prohibited recent document, mirrors, summaries, coverage, or discussions. No inspected result appeared to concern it.

## Executive diagnosis

The literature exposes **one new mandatory gate before another L1 brick is built**:

> If the final Euclidean distance problem can be written as separable convex optimization over a fixed-block higher-Lawrence, \(n\)-fold, tree-fold, or two-stage integer system, then exact distance is polynomial-time computable.

Thus, an exact fixed-brick realization may be **too structured to support NP-hardness**, not merely difficult to prove sound. This depends on how the compiler matrix becomes the final CVP lattice, so it is a conditional warning rather than a disproof of L1.

The literature also confirms that Strategy 2’s proposed jump from bounded Markov moves to bounded signed Graver moves is false in general: there are families with Markov complexity at most \(3\) and arbitrarily large Graver complexity.

Below are the most relevant finds, ranked by likely leverage.

---

## 1. Fixed-block convex \(n\)-fold optimization: a possible complexity-theoretic kill gate

**Authors/year/venue.** Raymond Hemmecke, Shmuel Onn, Robert Weismantel, 2011, *Mathematical Programming* 126, 97–117, “A polynomial oracle-time algorithm for convex integer minimization.” Related foundational \(n\)-fold results are due to De Loera–Hemmecke–Onn–Weismantel, 2008, *Discrete Optimization*. ([arxiv.org](https://arxiv.org/abs/0710.3003))

**Precise result.** For a fixed \(n\)-fold block matrix, separable convex integer minimization

\[
\min\left\{\sum_i f_i(x_i):
A^{(n)}x=b,\quad l\le x\le u,\quad x\in\mathbb Z^N\right\}
\]

is solvable in polynomial oracle time. The paper also extends the method to convex \(N\)-fold and two-stage stochastic integer programs. The mechanism is Graver-best augmentation with polynomially many augmentation steps. ([link.springer.com](https://link.springer.com/article/10.1007/s10107-009-0276-7))

**Why it hits the current wall.** Suppose a proposed L1 realization yields either

\[
L_r=\ker_{\mathbb Z} A_\star^{(r)}
\]

or a fixed-block extended formulation

\[
y=C_r z,\qquad C_r\text{ a fixed-brick higher-Lawrence/tree-fold matrix}.
\]

Then

\[
\operatorname{dist}(t,L_r)^2
=
\min_{x\in\mathbb Z^N,\ A_\star^{(r)}x=0}
\sum_j(x_j-t_j)^2
\]

in the kernel case, or

\[
\min_{y,z:\ y=C_rz}\sum_j(y_j-t_j)^2
\]

in the column-lattice case. Both objectives are separable convex in the emitted Euclidean coordinates. Signed coordinate permutations preserve this property. Therefore, if the equality system is genuinely fixed-block \(n\)-fold/tree-fold after adding the \(y\)-variables, the exact CVP instance may fall into a known polynomial-time class.

This is an inference from the cited theorem, not a theorem stated there about the roadmap.

**How to verify/adapt.**

1. For the next candidate, do not begin with the depth-\(1,2,3\) Graver audit.
2. First form the actual final optimization problem:
   \[
   \min_{z\in\mathbb Z^m}\|C_rz-t\|_2^2.
   \]
3. Add \(y=C_rz\), then search symbolically for row/column permutations exhibiting an \(n\)-fold, generalized \(n\)-fold, tree-fold, or two-stage form with constant block dimensions.
4. Treat finitely many brick colors as separate fixed types and test whether they can be absorbed into one larger fixed block.
5. If successful, the candidate is likely unsuitable for NP-hardness unless some essential feature—unboundedly many types, nonseparable transported metric, or non-fixed block data—escapes the theorem.

**Leverage:** extremely high. This should become the **Generation-8 complexity-compatibility gate**.

---

## 2. Santos–Sturmfels gives exactly the finite primitive-support theorem L2 wants

**Authors/year/venue.** Francisco Santos and Bernd Sturmfels, 2003, *Journal of Combinatorial Theory, Series A* 103(1), 151–164, “Higher Lawrence configurations.” ([arxiv.org](https://arxiv.org/abs/math/0209326))

**Precise result.** For a fixed configuration \(A\), the type of a vector in the \(r\)-th higher Lawrence lifting is the number of nonzero bricks. The Graver complexity

\[
g(A)=\sup_r\{\operatorname{type}(u):u\in\mathcal G(A^{(r)})\}
\]

is finite. More explicitly, it is computed as the maximum \(\ell_1\)-norm of an element in the Graver basis of the matrix whose columns are the elements of \(\mathcal G(A)\). In the generalized lifting \(\Lambda(A,B,r)\), the corresponding formula is

\[
g(A,B)
=
\max\{\|v\|_1:
v\in\mathcal G(B\,\mathcal G(A))\}.
\]

Thus every primitive in every depth has at most \(g(A,B)\) nonzero bricks, and the bound is attained at some depth. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0021869314003573))

**Why it is relevant.** This is the exact existing machinery behind L2—not merely an asymptotic finiteness statement. If L1 is established literally, the all-depth primitive audit reduces to two finite Graver computations:

1. \(\mathcal G(A_\star)\);
2. \(\mathcal G(B\,\mathcal G(A_\star))\).

It also clarifies what the theorem does **not** give: it bounds nonzero bricks, not coefficient size inside a brick, quotient visibility, energy, or honest-affine compatibility.

**How to verify/adapt.**

- Serialize the proposed colored brick as a generalized lifting pair \((A,B)\), rather than forcing it prematurely into the uncolored \(B=I\) case.
- Compute \(\mathcal G(A)\), construct the matrix \(B\,\mathcal G(A)\), and compute its Graver basis.
- Set
  \[
  K=\max_{v\in\mathcal G(B\mathcal G(A))}\|v\|_1.
  \]
- Enumerate every \(K\)-brick placement only after quotienting by brick-color and permutation symmetries.
- For each primitive type, test honest reassignment, quotient syndrome, and anchor energy exactly.

**Leverage:** high, but conditional on a genuine L1 identity.

---

## 3. Bounded Markov complexity does not control signed Graver complexity

**Authors/year/venue.** Hara Charalambous, Apostolos Thoma, Marius Vladoiu, 2013, arXiv:1311.4707, “Markov complexity of monomial curves.”

**Precise result.** For a three-generator monomial curve \(A=\{n_1,n_2,n_3\}\), the Markov complexity of all higher Lawrence liftings is:

- \(2\) if the toric ideal is a complete intersection;
- \(3\) otherwise.

Nevertheless, for every integer \(L\), there exist \(n_1,n_2,n_3\) whose Graver complexity is greater than \(L\). ([arxiv.org](https://arxiv.org/abs/1311.4707))

**Why it is relevant.** This addresses F2’s crux almost exactly. Even exceptionally simple, uniformly bounded Markov bases do not imply a bounded conformal decomposition calculus with a comparable constant. Compatible projections and bounded Markov degree can certify fiber connectivity while missing arbitrarily complicated primitive signed moves.

For a **fixed** compiler brick, Santos–Sturmfels still gives finite Graver complexity. But no generic strengthening of a Rauh–Sullivant Markov theorem into the desired F2 signed theorem is available.

**How to verify/adapt.**

- Rewrite F2 so that the Graver bound is derived independently from a fixed generalized-Lawrence representation.
- Do not derive \(K\) from Markov degree, normality, quadratic generation, or compatible projections.
- In finite tests, record separately:
  \[
  \text{Markov type},\qquad
  \text{circuit type},\qquad
  \text{Graver type}.
  \]
- A stable Markov basis at depths \(3,4,5\) is not evidence that Graver type has stabilized.

**Leverage:** high; it blocks the current generic proof plan for Strategy 2.

---

## 4. Chordal/decomposable gluing eliminates cycle moves at the Markov level

**Authors/year/venue.** Adrian Dobra, 2003, *Bernoulli* 9(6), 1093–1108, “Markov bases for decomposable graphical models.” ([projecteuclid.org](https://projecteuclid.org/journals/bernoulli/volume-9/issue-6/Markov-bases-for-decomposable-graphical-models/10.3150/bj/1072215202.full))

**Precise construction.** If the independence graph is decomposable—equivalently, chordal and represented by a clique tree—then the relevant table fibers are connected by primitive square-free degree-two swaps. Dobra gives explicit formulas for these moves from the clique-tree decomposition. Later work describes them as square-free degree-two moves associated with sample-size-two fibers. ([projecteuclid.org](https://projecteuclid.org/journals/bernoulli/volume-9/issue-6/Markov-bases-for-decomposable-graphical-models/10.3150/bj/1072215202.pdf))

**Why it is relevant.** The Generation-7 synchronized three-COPY rectangle is the characteristic failure of cyclic gluing: local exchanges synchronize around a cycle and become a new global primitive. Decomposable models overcome the analogous obstruction by replacing cyclic overlap with a junction tree satisfying the running-intersection property.

This is not complete L2 machinery: quadratic Markov generation does not imply that every Graver primitive is quadratic or harmless. But it gives a concrete topology mutation more principled than adding another character row.

**How to verify/adapt.**

1. Build the physical/COPY/fanout overlap hypergraph before choosing local marks.
2. Require a clique-tree ordering:
   \[
   C_i\cap\bigcup_{j<i}C_j\subseteq C_{p(i)}
   \]
   for some parent \(p(i)\).
3. Add separator coordinates explicitly; do not identify them externally.
4. Generate Dobra’s degree-two separator swaps and verify that the known support-three ghosts and synchronized rectangles reduce through them.
5. Then compute the **full Graver basis**, since Markov decomposability alone is insufficient for Euclidean cancellation soundness.

**Main obstacle.** Arbitrary circuit incidence may require large separators or duplicate state. That possible blow-up must be measured before pursuing the metric.

---

## 5. Unimodular hierarchical models provide a complete signed-primitive calculus

**Authors/year/venue.** Daniel Irving Bernstein and Christopher O’Neill, 2017, *Journal of Algebraic Statistics* 8(2), 29–43, “Unimodular hierarchical models and their Graver bases.” ([arxiv.org](https://arxiv.org/abs/1704.09018))

**Precise result.** The paper classifies the vertex-weighted simplicial complexes whose hierarchical-model matrices are unimodular and gives a combinatorial description of their Graver bases. For a unimodular configuration, the Graver basis is the circuit set; primitive kernel vectors are support-minimal and have square-free positive and negative parts, equivalently coefficients in \(\{0,\pm1\}\). Unimodular toric ideals also have equality between the universal Gröbner and Graver bases. ([ar5iv.labs.arxiv.org](https://ar5iv.labs.arxiv.org/html/1004.0840))

**Why it is relevant.** This is one of the few adjacent formalisms where “complete signed-kernel classification” is built into the structural class rather than obtained by depth enumeration. If a NAND/COPY compiler could be placed inside a classified unimodular hierarchical family, large-coefficient ghosts and hidden conformal primitives would disappear.

**How to verify/adapt.**

- Translate one proposed physical/pair/glue brick into a weighted simplicial complex.
- Run the excluded-minor or constructive classification from the paper.
- If it is unimodular, enumerate only circuits and test each circuit against honest-affine compatibility and energy.
- If adding the NAND face immediately leaves the class, record the minimal forbidden minor: that identifies exactly which logical interaction causes hidden Graver behavior.
- Also run the complexity gate in Find 1: unimodularity may make the resulting optimization too tractable.

**Leverage:** medium-high as a structural-recognition target, even if it produces a no-go theorem for expressive bricks.

---

## 6. Rauh–Sullivant lifting gives an exact finite gluing calculus—but only for Markov bases

**Authors/year/venue.** Johannes Rauh and Seth Sullivant, 2016, *Journal of Symbolic Computation* 74, 276–307, “Lifting Markov bases and higher codimension toric fiber products.” ([arxiv.org](https://arxiv.org/abs/1404.6392))

**Precise construction.** Given lattice maps and factor Markov bases satisfying the compatible-projection property, moves in the projected intersection can be lifted to factor moves and then glued. When the associated projected-fiber-intersection semigroup is normal, the lifting procedure can be iterated. Applied to toric fiber products, the resulting basis consists of:

1. compatible lifts of factor moves;
2. glued projected moves;
3. kernel or codimension-zero quadratic moves.

The method yields finiteness and bounded-degree results for several iterated families. ([arxiv.org](https://arxiv.org/pdf/1404.6392))

**Why it is relevant.** This is the right machinery for F1 and for recognizing exactly where a synchronized COPY-cycle move enters. It can replace ad hoc lists of “old generators” with a theorem-level Markov decomposition.

But Find 3 means it cannot supply F2 by itself.

**How to verify/adapt.**

- Compute the projected fiber semigroup for every separator/gluing type.
- Test normality exactly and enumerate holes when normality fails.
- Verify compatible projection on the complete signed local fibers, not just nonnegative honest tables.
- Generate the full lifted Markov basis and compare it with the independently computed Graver basis.
- Treat every element in
  \[
  \mathcal G(A_{\rm glued})\setminus M_{\rm lifted}
  \]
  as a mandatory new adverse class.

---

## 7. Balanced stratified staged trees avoid cyclic generators by construction

**Authors/year/venue.** Lamprini Ananiadi and Eliana Duarte, 2021, *Algebraic Statistics* 12, 1–20, “Gröbner bases for staged trees.” ([arxiv.org](https://arxiv.org/abs/1910.02721))

**Precise result.** The toric ideal of every balanced, stratified staged tree has a quadratic Gröbner basis with square-free initial terms. The proof recursively expresses the model through toric fiber products. ([ar5iv.labs.arxiv.org](https://ar5iv.labs.arxiv.org/html/1910.02721))

**Why it is relevant.** A staged tree is a fixed colored branching object in which vertices with the same color share local transition behavior. That is close to the roadmap’s desired “fixed finite brick colors, formula in targets/colors” formalism, but inherently tree-based. The balanced/stratified conditions prevent the sort of uncontrolled cyclic generator seen in the three-COPY cycle at the Gröbner level.

Again, quadratic Gröbner generation is weaker than Graver classification, but it supplies a sharply defined alternative to Beneš-cycle gluing.

**How to verify/adapt.**

- Encode one NAND evaluation path as a staged tree whose leaves are legal local words.
- Use stage colors for COPY equality and program bits.
- Check balance and stratification symbolically.
- Compute whether the number of root-to-leaf variables remains polynomial; a naïve tree expansion may be exponential.
- At depths \(1,2,3\), compare the quadratic Gröbner basis with the full Graver basis and explicitly search for equal-energy signed leaf combinations.

---

## 8. Valiant universal circuits solve the formula-oblivious wiring problem without relying solely on switches

**Authors/year/venue.** Leslie Valiant, 1976, STOC, “Universal circuits”; constructive size refinements and implementations include Kiss–Schneider, 2016, EUROCRYPT, “Valiant’s Universal Circuit is Practical.” ([eprint.iacr.org](https://eprint.iacr.org/2016/093.pdf))

**Precise construction.** There is a fixed programmable universal circuit of size \(O(k\log k)\) and depth \(O(k)\) that simulates every Boolean circuit of size \(k\). The simulated circuit is supplied as program bits; its graph is not substituted into the universal circuit’s topology. Valiant obtains this through edge-universal graphs and programmable supernodes. ([eccc.weizmann.ac.il](https://eccc.weizmann.ac.il/report/2008/078/download/))

**Why it is relevant.** This addresses L1’s formula-obliviousness requirement more directly than “freeze a Beneš permutation network and hope the switch brick is sound.” Formula wiring becomes program data in a single fixed topology. The program bits can potentially be placed in targets or finite brick colors.

It does not address signed ghosts. It instead separates the two problems:

1. topology universality;
2. sound local programmable supernodes.

**How to verify/adapt.**

- Replace the next Beneš mutation with a small Valiant universal-circuit supernode library.
- Freeze NAND, selector, fanout, and program-bit supernodes as distinct constant colors.
- Require program bits to alter only target entries or color-preserving column permutations.
- Audit each programmable supernode for support-three ghosts before composing it.
- Then serialize the smallest universal-circuit recursion containing fanout and reconvergence, rather than another isolated switch.

This is probably the strongest remaining route to L1’s wiring claim.

---

## 9. Transportation universality offers a completely different target-only compiler

**Authors/year/venue.** Jesús De Loera and Shmuel Onn, 2006, *SIAM Journal on Optimization* 17(3), 806–821, “All Linear and Integer Programs Are Slim 3-Way Transportation Programs.” ([itd.ucdavis.edu](https://itd.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf))

**Precise result.** Every rational polytope, and every bounded integer program, can be transformed in polynomial time into a slim \(r\times c\times3\) line-sum transportation polytope. The construction preserves the integer feasible set through an explicit coordinate projection/isomorphism. Formula data is carried by line sums and bounds; the constraint coefficients are transportation-incidence coefficients. ([math.ucdavis.edu](https://www.math.ucdavis.edu/~deloera/RECENT_WORK/universality.pdf))

**Why it is relevant.** This is prior work achieving the broadest version of “all instance dependence in targets/right-hand sides” without universal switching gadgets. It therefore provides an alternative formalism for L1.

The cost is that \(r\) and \(c\) vary with the instance. Thus it is not automatically a fixed finite brick or bounded-Graver family. Indeed, \(n\)-fold universality uses a family of bimatrices whose parameter \(m\) grows, rather than one fixed matrix. ([arxiv.org](https://arxiv.org/pdf/1101.3267))

**How to verify/adapt.**

- Apply the construction to the standard bounded \(0/1\) ILP for 3SAT.
- Extract the exact transportation matrix and line-sum target.
- Test whether its varying dimension can be represented by finitely many colored local tiles.
- Add anchor coordinates and check whether all Boolean feasible tables have common Euclidean energy.
- Compute the first Graver circuits corresponding to the G13 affine collision, clause DROP, and synchronized COPY cycles.
- Abandon it if the required growing parameter also makes Graver type grow with \(S\).

---

## Recommended next move

### New mandatory gate: `L0 — fixed-block tractability exclusion`

Before continuing L1, prove that the actual CVP optimization

\[
\min_{z\in\mathbb Z^m}\|C_rz-t\|_2^2
\]

**cannot** be reformulated as separable convex fixed-block \(n\)-fold, tree-fold, or two-stage integer minimization. If it can, the construction is algorithmically incompatible with the desired hardness result, subject to the usual \(P\ne NP\) assumption.

### If L0 passes

The most defensible mutation is:

1. **Valiant universal-circuit topology** for formula-obliviousness;
2. **junction-tree or balanced staged-tree gluing** to avoid synchronized cycle generators;
3. a brick chosen, if possible, from a **unimodular hierarchical class** so that Graver primitives are exactly circuits;
4. Santos–Sturmfels computation of the actual all-depth brick bound \(K\);
5. only then metric, DROP, and expander work.

### Implications for the roadmap

- **Strategy 1:** viable only after the new tractability gate.
- **Strategy 2:** Rauh–Sullivant can establish F1 and Markov generation, but F2 cannot be obtained generically from bounded Markov degree.
- **Current Beneš/quadratic-character line:** the literature suggests changing the global topology, not adding another local mark. Chordal or staged-tree formalisms are the established way analogous cycle obstructions are removed.
