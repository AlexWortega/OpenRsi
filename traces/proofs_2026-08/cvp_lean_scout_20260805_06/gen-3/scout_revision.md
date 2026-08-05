## Literature scout report

I did **not** search for or consult the prohibited document or accounts of its arguments. One `cdn.openai.com` PDF surfaced incidentally in a broad bibliographic query; I discarded it without opening or using it.

### Executive diagnosis

The literature suggests that the latest failure is not an isolated bad COPY gadget:

1. **Affine selector gluing naturally produces quadratic exchange moves.** Toric-fiber-product theory identifies these as canonical generators, not accidental attacks.
2. **Quaternion valuations amplify only an already nonzero leading class.** Associated-graded division-algebra theory prevents later cancellation, but cannot repair the observed grade-zero `111` seed.
3. Therefore, the next quaternionic coordinate should not be another affine checksum. Its initial form should be a **genuine multiplicative monomial in a graded division ring**, with the seam-exchange monomial assigned a different degree or nonzero leading symbol.
4. Once such a coordinate gives a finite, lift-independent transition graph, **minimum-cycle-mean duality** constructs exactly the potential certificate already supported by the Lean telescope theorem.

Below are nine literature finds, ranked by likely leverage.

---

## 1. Toric fiber products: the diagonal splice is a canonical quadratic generator

**Likely leverage: Very high — directly explains the killed COPY seam.**

**Source.** Seth Sullivant, 2007, *Journal of Algebra*, “Toric Fiber Products”; Alexander Engström, Thomas Kahle, and Seth Sullivant, 2014, *Journal of Algebraic Combinatorics*, “Multigraded Commutative Algebra of Graph Decompositions.” ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0021869306006247))

### Precise construction and theorem

Let \(I\subseteq K[x]\) and \(J\subseteq K[y]\) be homogeneous under a common grading
\[
\deg x_{ij}=\deg y_{ik}=a_i.
\]
Introduce variables \(z_{ijk}\) and the map
\[
\phi(z_{ijk})=\bar x_{ij}\otimes \bar y_{ik}.
\]
The **toric fiber product** is \(\ker\phi\).

When the grading vectors \(a_i\) are linearly independent—the codimension-zero case—a generating or Gröbner basis is obtained from:

1. compatible **lifts** of generators of \(I\);
2. compatible lifts of generators of \(J\);
3. the quadratic exchange binomials
   \[
   z_{ij_1k_1}z_{ij_2k_2}
   -
   z_{ij_1k_2}z_{ij_2k_1}.
   \]

Engström–Kahle–Sullivant extend this to positive codimension using projected-fiber Markov bases and a **compatible projection property**.

### Why this is exactly relevant

The observed
`false111-COPY11-false111`
splice has the structure of a \(2\times2\) exchange: the two components preserve all exposed affine marginals but swap the hidden pairing across the seam. Toric-fiber-product theory predicts precisely such quadrics whenever two modules are glued only through a common coarse grading.

This gives a stronger diagnosis than “all 378 COPY codes failed”:

> If those COPY codes expose the same codimension-zero seam grading, a quadratic diagonal splice is structurally expected regardless of local affine isolation.

### How to verify or adapt

1. Encode the NAND and COPY selector columns as monomials.
2. Identify the common seam grading matrix \(A\).
3. Test whether the current attack is literally one of Sullivant’s `Quad` generators after relabeling.
4. For each proposed transfer coordinate, check whether it:
   - refines the grading so the two sides of that quad receive different degrees; or
   - moves the composition to positive codimension and destroys compatible projection.
5. Use `4ti2` or Macaulay2 to compute the projected-fiber Markov basis.

**Immediate experiment:** perform this algebraic classification before enumerating further affine COPY signatures. It may prove a family-level no-go for all COPY gadgets exposing only the existing marginals.

---

## 2. Valued division algebras: nonzero initial forms cannot cancel under multiplication

**Likely leverage: Very high — the correct positive machinery for Q2.**

**Source.** Y.-S. Hwang and A. R. Wadsworth, 1999, *Journal of Algebra* 220, 73–114, “Correspondences Between Valued Division Algebras and Graded Division Algebras”; J.-P. Tignol and A. R. Wadsworth, 2010, *Transactions of the AMS*, “Value Functions and Associated Graded Rings for Semisimple Algebras.” ([math.uni-bielefeld.de](https://www.math.uni-bielefeld.de/LAG/man/003.pdf))

### Precise statement

Let \(D\) be a finite-dimensional division algebra over a Henselian valued field \(F\). The valuation of \(F\) extends uniquely to \(D\). The filtration produces
\[
\operatorname{gr}(D)
  =\bigoplus_{\gamma}D_{\ge\gamma}/D_{>\gamma}.
\]

This is a **graded division ring**: every nonzero homogeneous element is invertible. Consequently, for nonzero \(x,y\in D\),
\[
v(xy)=v(x)+v(y),
\qquad
\operatorname{in}(xy)=\operatorname{in}(x)\operatorname{in}(y)\ne0.
\]

For tame central division algebras, Hwang–Wadsworth further show that passage to the graded algebra preserves the Brauer-theoretic index and faithfully reflects significant subalgebra structure. Tignol–Wadsworth develop compatible gauges for semisimple algebras and tensor products.

### Why this is relevant

This is nearly the desired Q2 mechanism—but with a crucial boundary:

- If a child defect already has a nonzero initial form and the transfer is multiplication by another nonzero homogeneous element, its valuation is forced to increase additively.
- But the theorem **cannot create a leading class from a grade-zero affine pseudosection**.

Thus the current failure is exactly before the point at which valuation theory becomes powerful.

### How to adapt it

Localize the quaternion algebra at \(17\). Choose a uniformizer \(\Pi\) for the local maximal order and an unramified quadratic coefficient ring. The associated graded algebra can be represented as a twisted/Ore-style graded algebra, with Frobenius acting on residue coefficients.

Require the new transfer coordinate \(T\) to satisfy, on every adverse boundary,
\[
\operatorname{in}(T_{\rm parent})
 =
u(\text{legal data})\,
\operatorname{in}(T_{\rm child})\,
g(\text{boundary}),
\]
where both \(u\) and \(g\) are provably nonzero homogeneous elements. Then graded-division-ring structure gives injectivity automatically.

**Verification plan:**

1. Compute the local multiplication table through \(P^3\).
2. Symbolically derive the initial-form map—not merely its finite table.
3. Check that `false111` has nonzero \(T\)-initial form.
4. Prove the multiplier is a unit or nonzero homogeneous element for every legal/adverse case.
5. Use finite enumeration only to establish the case partition; use graded division to prove all-lift soundness.

---

## 3. Minimum-cycle mean and difference potentials: automatic synthesis of the Lean certificate

**Likely leverage: High — closes the finite-transducer-to-all-depth step.**

**Source.** Richard M. Karp, 1978, *Discrete Mathematics* 23, 309–311, “A Characterization of the Minimum Cycle Mean in a Digraph.” ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0012365X78900110))

### Precise statement

For a finite weighted directed graph, define
\[
\gamma_*=\min_C \frac{w(C)}{|C|},
\]
where \(C\) ranges over directed cycles. Karp gives a dynamic-programming characterization and polynomial-time algorithm for \(\gamma_*\).

The dual difference-constraint formulation is:

\[
w(u,v)+h(u)-h(v)\ge \gamma
\quad\text{for every edge }u\to v
\]
has a solution \(h\) iff every directed cycle has mean weight at least \(\gamma\).

After clearing denominators, \(h\) can be made integral.

### Why this is relevant

The existing Lean theorem proves that a local potential inequality telescopes, but it does not construct the potential. Karp’s theorem supplies the missing synthesis step.

For example, assign an edge weight
\[
w(e)=4\,\Delta v(e)-1.
\]
Then positive minimum cycle mean says that asymptotically there is more than one valuation gain per four binary levels, exactly the threshold needed because \(17>2^4\).

### How to verify or adapt

Once a lift-independent finite transition graph exists:

1. Enumerate all normalized states and edges.
2. Compute the exact rational minimum cycle mean.
3. If \(\gamma_*>0\), solve the difference constraints by shortest paths.
4. Clear denominators to get an integer potential.
5. Emit the edge-by-edge inequalities as a certificate consumed by the existing Lean file.
6. Separately enumerate all bounded transient paths between strongly connected components.

This replaces heuristic potential LPs with a complete finite criterion:

> A candidate passes precisely when every reachable adverse cycle has positive average gain.

---

## 4. Graver stabilization for repeated block systems: reduce arbitrary signed attacks to primitive building blocks

**Likely leverage: High for Strategy 2; medium for the quaternion route.**

**Source.** Matthias Aschenbrenner and Raymond Hemmecke, 2007, *Foundations of Computational Mathematics* 7, 183–227, “Finiteness Theorems in Stochastic Integer Programming”; Jesús De Loera, Raymond Hemmecke, Shmuel Onn, and Robert Weismantel, “N-Fold Integer Programming,” 2006 preprint/published in *Discrete Optimization*. ([arxiv.org](https://arxiv.org/pdf/math/0502078.pdf))

### Precise statement

For any integer matrix \(A\), every
\[
z\in\ker_{\mathbb Z}A
\]
is a **conformal sum** of Graver-basis elements:
\[
z=g_1+\cdots+g_t,
\qquad
g_i\sqsubseteq z,
\]
meaning every \(g_i\) lies in the same orthant as \(z\) and is coordinatewise bounded by it.

For fixed \(n\)-fold or fixed-stage stochastic block templates, the Graver test sets stabilize: their elements are assembled from finitely many building blocks independent of the number of repeated scenarios/blocks. Aschenbrenner–Hemmecke prove the corresponding multistage finiteness using well-quasi-ordering machinery.

### Why this is relevant

The campaign has repeatedly checked named attacks or bounded shells, only to have composition generate a new signed splice. Graver theory supplies the correct universal quantifier:

> Audit primitive conformal kernel moves, not a manually selected attack list.

If the composed bag/gluing matrix falls into an \(n\)-fold or fixed-stage family, all large-instance signed kernel vectors reduce to finitely many primitive types.

### How to verify or adapt

1. Rewrite the recursive gluing matrix in standard block form.
2. Determine whether formula size changes only the number of repeated blocks or also the number of stages.
3. Compute the building-block Graver basis for the smallest template.
4. For each primitive \(g\), prove:
   - it is an honest reassignment; or
   - the proposed check rows detect it with a sign-stable residual.
5. Use conformality to prevent cancellation between primitive pieces.

**Important limitation:** balanced depth is \(O(\log S)\), not fixed. The classical fixed-stage theorem does not automatically give a uniform constant-size audit. The agent must either:

- find an \(n\)-fold flattening with fixed block matrices; or
- prove a new depth-uniform stabilization statement for this special recursion.

Even a negative result here is useful: it identifies whether M3 can truly become finite.

---

## 5. Mal’cev–Neumann series: a noncommutative multiplication formalism with no bicyclic zero divisors

**Likely leverage: Medium-high as an alternative to quaternion tiles.**

**Source.** B. H. Neumann, 1949, *Transactions of the AMS* 66, “On Ordered Division Rings”; modern streamlined treatment by Bjorn Poonen, “Units in Hahn–Mal’cev–Neumann Rings.” ([community.ams.org](https://community.ams.org/journals/tran/1949-066-01/S0002-9947-1949-0032593-5/S0002-9947-1949-0032593-5.pdf))

### Precise construction

Let \(K\) be a division ring and \(G\) a totally ordered group. The Mal’cev–Neumann ring \(K((G))\) consists of formal series
\[
f=\sum_{g\in G} a_g g
\]
whose support is well ordered.

It is a division ring. In particular, if \(f,g\ne0\), their least support terms satisfy
\[
\operatorname{lt}(fg)
 =
\operatorname{lt}(f)\operatorname{lt}(g)\ne0.
\]
Hence the group algebra \(K[G]\) embeds in a division ring and has no zero divisors.

### Why this is relevant

The \(A_5\) route failed because the finite group algebra contains bicyclic nilpotents and zero divisors. Replacing the finite group by an orderable group—especially a free group—removes that mechanism completely.

It also offers a “history word” formalism: different ordered products remain different basis words instead of being compressed into a small matrix representation.

### How to adapt it

Use a free group or free monoid alphabet for NAND/COPY transitions. At depth \(d=O(\log S)\), explicitly allocate one coordinate for every reduced word that can occur up to depth \(d\). For a fixed number of generators this is
\[
O(c^d)=\operatorname{poly}(S).
\]

The leading-word order provides a noncancellation invariant.

Required checks:

1. Never quotient or wrap the word space—finite truncation by quotient could reintroduce zero divisors.
2. Allocate all words that can arise in the compiled depth.
3. Give different gates prefix-free or otherwise order-separated tags.
4. Verify that an adverse product’s least word cannot coincide with the least word of a legal signed combination.
5. Bound coefficient sizes and Euclidean completeness cost.

This is less dimension-efficient than quaternions but may be algebraically cleaner: polynomial dimension is still possible because the circuit depth is logarithmic.

---

## 6. Lossless expanders and RIP-1: signed sparse defects cannot cancel at every check

**Likely leverage: Medium-high, conditional exactly on M2.**

**Source.** Michael Sipser and Daniel Spielman, 1996, *IEEE Transactions on Information Theory* 42, 1710–1722, “Expander Codes”; Radu Berinde, Anna Gilbert, Piotr Indyk, Howard Karloff, and Martin Strauss, 2008, Allerton Conference, RIP-1/expander sparse recovery; Venkatesan Guruswami, Christopher Umans, and Salil Vadhan, 2009, *JACM*, explicit highly unbalanced near-lossless expanders. ([cs.yale.edu](https://cs.yale.edu/homes/spielman/Research/expanders.html))

### Precise statement

Let \(H\) be the adjacency matrix of a left \(d\)-regular \((K,\varepsilon)\)-lossless expander:
\[
|N(S)|\ge (1-\varepsilon)d|S|
\qquad
(|S|\le K).
\]

A counting argument gives at least
\[
(1-2\varepsilon)d|S|
\]
unique-neighbor edges. Therefore, for any nonzero vector \(\Delta\) supported on \(S\), a unique-neighbor row contains exactly one nonzero contribution, so
\[
H\Delta\ne0
\]
over any integral domain.

The corresponding RIP-1 result is of the form
\[
(1-2\varepsilon)d\|\Delta\|_1
\le
\|H\Delta\|_1
\le
d\|\Delta\|_1
\]
for \(K\)-sparse vectors.

Guruswami–Umans–Vadhan give deterministic explicit unbalanced expanders with expansion arbitrarily close to the left degree and polylogarithmic degree.

### Why this is relevant

This is stronger than a finite-field code-distance argument: unique neighbors defeat **signed integral cancellation directly**, with no need to reduce modulo a prime.

Thus M3 is largely available from the literature once M2 establishes
\[
|\operatorname{supp}\Delta|\le C\log S.
\]

### How to verify or adapt

1. Set \(K=C\log S\).
2. Instantiate an explicit lossless expander.
3. Emit its integer \(0/1\) adjacency matrix as CVP rows.
4. Formally prove the unique-neighbor counting lemma.
5. Charge either \(\|H\Delta\|_1\) or its Euclidean surrogate.

The sharp boundary is important:

> Expanders solve cancellation of sparse defects; they do not prove defects are sparse.

So this machinery should not be tested further until M2 has a credible shell-wide proof.

---

## 7. Kitaoka’s E-type theorem: exact exclusion of entangled minimal tensor vectors

**Likely leverage: Medium — T4 exists, but T2 remains the bottleneck.**

**Source.** Yoshiyuki Kitaoka, 1976, *Proceedings of the Japan Academy*, “Tensor Products of Positive Definite Quadratic Forms”; Kitaoka, 1993, Cambridge University Press, *Arithmetic of Quadratic Forms*, Chapter 7, especially Theorem 7.1.1. ([jstage.jst.go.jp](https://www.jstage.jst.go.jp/article/pjab1945/52/9/52_9_498/_pdf/-char/en))

### Precise statement

A positive-definite integral lattice \(L\) is of **E-type** if, for every positive-definite lattice \(M\), every minimal vector of
\[
L\otimes M
\]
is decomposable:
\[
v=x\otimes y.
\]

Kitaoka’s later formulation records that every positive-definite \(\mathbb Z\)-lattice of rank at most \(43\) is of E-type.

### Why this is relevant

If an exposed tile factor has rank at most \(43\), unrestricted coefficient tensors cannot introduce a shorter entangled vector. This is exactly the all-integer theorem missing from naive tensor amplification.

The theorem can be applied recursively by always tensoring the accumulated instance with a fresh rank-\(\le43\) factor.

### How to verify or adapt

The remaining proof obligations are entirely around homogenization:

1. Construct \(\widehat L\) so every relevant minimum has layer coordinate \(t=\pm1\).
2. Prove every \(t=0\) vector is strictly longer.
3. Prove every \(|t|\ge2\) vector is strictly longer.
4. Make the legal and adverse seeds nonisometric.
5. Enumerate all vectors through the desired \(\rho^2R^2\) threshold before tensoring.

**Caution:** E-type controls **minimal vectors**, not arbitrary near-minimal vectors. The induction must formulate each YES/NO quantity as an actual minimum of the relevant homogeneous lattice, not as a restricted shell statistic.

---

## 8. \(p\)-adic automata: a formal test for whether carries really reduce to finitely many states

**Likely leverage: Medium — addresses the stated carry/lumpability falsifier.**

**Source.** Vladimir Anashin, 2012, *p-Adic Numbers, Ultrametric Analysis and Applications* 4(2), 151–160, “Automata Finiteness Criterion in Terms of van der Put Series of Automata Functions”; Rostislav Grigorchuk and Dmytro Savchuk, 2023, *Journal of the Australian Mathematical Society* 114, 78–109. ([arxiv.org](https://arxiv.org/pdf/1112.5089))

### Precise statement

A digit-by-digit transducer over a \(p\)-symbol alphabet induces a \(1\)-Lipschitz map
\[
f:\mathbb Z_p\to\mathbb Z_p.
\]

Anashin characterizes finite-state automaton functions through their van der Put expansions: a \(1\)-Lipschitz function is finite-state exactly when its normalized van der Put coefficients form a \(p\)-automatic sequence taking values in a finite subset of \(\mathbb Q\cap\mathbb Z_p\). Grigorchuk–Savchuk generalize and make explicit the connection between sections of rooted-tree maps and Mealy/Moore automata.

### Why this is relevant

The proposed finite transducer is invalid if two \(P^3\) lifts of the same \(P^2\) state have different future behavior. This literature gives a language for that issue:

- sections/states encode residual carry information;
- finite-state behavior is a theorem to prove, not an empirical observation at one precision.

### How to adapt

Choose a \(\mathbb Z_{17}\)-basis for the local quaternion order and express the transfer operation coordinatewise.

1. Prove the coordinate map is \(1\)-Lipschitz.
2. Compute its sections under successive base-\(17\) digits.
3. Minimize the resulting automata.
4. Test whether new sections stop appearing.
5. Use van der Put coefficients to prove stabilization rather than merely observe it.

**Limitation:** the cited theorem is commutative and one-dimensional. A quaternion application needs either coordinatewise reduction plus a compatibility proof or a multivariate extension. Nevertheless, it gives a precise model of the carry problem.

---

## 9. Acyclic hypergraph/junction-tree gluing: local consistency can imply global consistency

**Likely leverage: Medium-low, but a useful alternative formalism.**

**Source.** Catriel Beeri, Ronald Fagin, David Maier, and Mihalis Yannakakis, 1983, *Journal of the ACM* 30(3), 479–513, “On the Desirability of Acyclic Database Schemes.” ([cse.unl.edu](https://cse.unl.edu/~choueiry/Documents/jacm83a.pdf))

### Precise statement

For a hypergraph of relation schemas, several properties are equivalent, including:

- existence of a join tree/running-intersection representation;
- acyclicity under the database-hypergraph definitions;
- pairwise/local consistency of relations implying global consistency;
- existence of a full reducer and a universal relation for every locally consistent family.

Thus, on an acyclic bag system, consistent local support relations glue to a global relation.

### Why this is relevant

Many killed attacks use an overlap cycle: locally valid affine data circulate around the cycle without representing a global assignment. Junction-tree formalisms eliminate exactly that support-level phenomenon.

An alternative compiler could duplicate wires until gate bags form a tree and enforce equality only along tree separators.

### How to adapt

1. Build bags containing complete assignments to each gate and its boundary wires.
2. Arrange bags with the running-intersection property.
3. Verify acyclicity by GYO reduction.
4. Use full separator marginals, not singleton moments.
5. Prove integral normality or total unimodularity of the resulting marginal map.

The final step is essential. The database theorem concerns ordinary relations/nonnegative support, whereas CVP permits unrestricted signed coefficients. It is therefore an architectural guide, not by itself a soundness theorem.

---

# Recommended next sequence

## A. First: classify the current seam by toric fiber products

Before searching more affine COPY multisets:

1. Construct the common seam grading.
2. Identify the observed `111` splice as a `Quad` move, if possible.
3. Prove that every affine coordinate homogeneous under that grading vanishes on it.

This could convert the current finite enumeration into a reusable symbolic no-go theorem.

## B. Then: search only for multiplicative graded transfer coordinates

The candidate should have an initial-form identity of the form
\[
\operatorname{in}T_{\rm parent}
 =
a\operatorname{in}T_{\rm child}b,
\qquad a,b\ne0,
\]
rather than an affine residual sum. Hwang–Wadsworth then supplies all-lift noncancellation.

The first gate remains:

\[
\operatorname{in}T(\texttt{false111})\ne0.
\]

## C. If a finite transition system results, use Karp rather than hand-designed potentials

Compute the exact minimum cycle mean, synthesize an integral potential, and feed it into the existing Lean telescope theorem. This gives a clean division of labor:

- finite algebra establishes states and edges;
- Karp establishes the optimal average gain;
- Lean establishes all-depth telescoping.

## D. Parallel fallback

Test whether the Möbius/bag matrices fit an \(n\)-fold or fixed-stage Graver family. If so, replace shell enumeration by a finite primitive-move audit and attach explicit lossless-expander rows only after proving sparse support.

## Bottom line

The highest-leverage literature combination is:

\[
\boxed{\text{toric fiber products}
\;\longrightarrow\;
\text{graded division-ring transfer}
\;\longrightarrow\;
\text{minimum-cycle potential}.}
\]

It addresses the exact three layers of the current wall:

1. identify why affine COPY gluing necessarily admits the splice;
2. design a transfer whose nonzero leading term cannot be annihilated;
3. turn a finite transition pass into an all-depth valuation-growth theorem.

None of the cited results alone proves the requested GapCVP hardness reduction, but together they substantially narrow what a viable next candidate must look like.
