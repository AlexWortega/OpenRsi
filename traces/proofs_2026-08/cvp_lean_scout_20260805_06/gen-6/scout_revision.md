## Search hygiene

I did **not** search for the prohibited document or accounts of its solutions. One unrelated query returned an OpenAI-hosted “reasoning walkthrough” result that appeared potentially derivative; I discarded it without opening or using it.

## Diagnosis

The current frontier is encountering two distinct walls:

1. **Compositional kernel growth:** local isolation does not survive gluing; new signed transportation/Lawrence moves appear.
2. **Syndrome incompleteness:** transfer coordinates see a selected seam subspace but miss other low-energy directions—most recently physical-selector flips.

The literature suggests replacing ad hoc channel addition with a two-part theorem:

- put the complete recursive matrix into a class with **uniformly bounded Graver type**, then
- apply an explicit code or unique-neighbor matrix to **all coordinates supporting a primitive defect**, not merely pair selectors.

Below are the most relevant existing tools, ranked by likely leverage.

---

# 1. Higher Lawrence configurations give depth-uniform Graver localization

**Francisco Santos and Bernd Sturmfels, 2003, Journal of Combinatorial Theory Series A, “Higher Lawrence Configurations.”**

### Precise machinery

For a fixed integer configuration \(A\), its \(r\)-th Lawrence lifting \(A^{(r)}\) has integer kernel

\[
\mathcal L(A^{(r)})=
\left\{
(u^{(1)},\ldots,u^{(r)}):
u^{(i)}\in\mathcal L(A),\quad
\sum_{i=1}^r u^{(i)}=0
\right\}.
\]

The **type** of such a move is the number of nonzero rows \(u^{(i)}\). Santos–Sturmfels prove that the Graver complexity

\[
g(A)=\sup_r\max\{\operatorname{type}(g):g\in \operatorname{Gr}(A^{(r)})\}
\]

is finite. More precisely, \(g(A)\) can be computed as the maximum \(\ell_1\)-norm of a Graver element of the matrix whose columns are the elements of \(\operatorname{Gr}(A)\). Thus every primitive move in every number of repeated layers uses only a bounded number of layers, independent of \(r\). ([arxiv.org](https://arxiv.org/pdf/math/0209326))

### Why this is relevant

This is almost exactly the desired M1 conclusion, but under a stronger structural hypothesis. If the recursive bag/COPY matrix can be written, after row operations and column permutation, as a higher Lawrence lifting of a fixed tile matrix \(A\), then every Graver move has **constant type**, stronger than \(C\log S\) localization.

It also explains the observed diagonal splices: a Lawrence lifting is specifically the structure in which several local kernel rows can sum to zero globally.

### How to verify/adapt

1. Extract one fixed brick matrix \(A\) containing **physical, pair, normalization and transfer variables**.
2. Test symbolically whether the depth-\(r\) emitted matrix has kernel
   \[
   \{(u^{(1)},\ldots,u^{(r)}):Au^{(i)}=0,\ \sum_i u^{(i)}=0\}.
   \]
3. Compute \(\operatorname{Gr}(A)\), form the matrix \(G_A\) with those elements as columns, and compute \(\operatorname{Gr}(G_A)\).
4. The resulting \(g(A)\) is a rigorous support budget for the detector.

**Highest-value discriminator:** determine whether the complete proposed recursion is genuinely a fixed-\(A\) Lawrence family. If yes, M1 should be replaced by this theorem rather than reproved from scratch.

---

# 2. Reed–Solomon/MDS syndromes detect every bounded-support defect—including physical flips

**Irving Reed and Gustave Solomon, 1960, Journal of the Society for Industrial and Applied Mathematics 8(2), “Polynomial Codes Over Certain Finite Fields.”**

### Precise construction

Choose distinct \(\alpha_1,\ldots,\alpha_N\in\mathbb F_q\). Evaluating every polynomial \(f\) of degree \(<k\) at these points produces an \([N,k,N-k+1]\) Reed–Solomon code:

\[
f\longmapsto \bigl(f(\alpha_1),\ldots,f(\alpha_N)\bigr).
\]

Equivalently, a parity-check matrix \(H\) for the code satisfies

\[
Hx\ne0
\quad\text{for every nonzero }x
\text{ with }
|\operatorname{supp}(x)|<N-k+1.
\]

This follows because any \(N-k\) columns of an MDS parity-check matrix are linearly independent. ([sites.math.rutgers.edu](https://sites.math.rutgers.edu/~zeilberg/akherim/ReedS1960.pdf))

### Why this is relevant

The Generation-5 channels failed because they were supported only on pair variables. An MDS syndrome should instead assign columns to the **complete selector vector**:

\[
x=(x_{\rm physical},x_{\rm pair},x_{\rm glue},\ldots).
\]

Then a one-bit physical flip is automatically visible. Over \(\mathbb F_{289}\), a constant tile with 18 or even hundreds of defect coordinates fits directly into one evaluation field.

This also replaces “try \(r=1,2,3,4\) product channels” by a theorem: choose designed distance \(d\), and every nonzero defect of support \(<d\) is detected.

### How to verify/adapt

- First quotient out only those directions that are **intentionally honest**. Let \(U\) be the honest-difference space and construct \(H\) on the quotient \(V/U\).
- Include columns for every physical and pair selector; no channel may be pair-supported only.
- Choose designed distance greater than the support bound supplied by Higher Lawrence or another Graver theorem.
- Lift each field syndrome coordinate to a separate quaternion transfer channel.
- Rerun Hamming-one, Hamming-two and the complete sub-\(17E\) shell.

**Critical caveat:** Generation 13 showed that a harmful vector in the honest affine span is invisible to every compatible linear syndrome. Thus the first audit is

\[
\Delta\notin U.
\]

If the physical-flip or another malformed primitive lies in \(U\), no number of MDS channels fixes that candidate.

---

# 3. Iterated toric fibre products have uniformly bounded Markov degree

**Jan Draisma and Florian Oosterhof, 2018, Advances in Applied Mathematics, “Markov Random Fields and Iterated Toric Fibre Products.”**

### Precise statement

For iterated toric fibre products assembled from a fixed finite collection of toric varieties, the defining toric ideals are generated by binomials of degree bounded by a constant independent of the number of factors. Consequently, Markov random fields built by repeatedly gluing graphs from a fixed finite collection have uniformly bounded Markov degree. ([arxiv.org](https://arxiv.org/pdf/1612.06737.pdf))

A degree-\(D\) binomial corresponds to a signed move whose positive and negative parts each have \(\ell_1\)-norm at most \(D\), hence total support at most \(2D\).

### Why this is relevant

If the splitter-bag or NAND/COPY compiler is an iterated toric fibre product of finitely many bag types, then there is a **constant-degree universal Markov basis**, independent of formula depth. This is stronger than the proposed \(O(\log S)\) localization at the level of nonnegative fibers.

It says that growing depth need not create ever-larger minimal fiber-connectivity moves, provided the gluing operation is a genuine toric fibre product.

### How to verify/adapt

1. Express each bag as a toric map and its separator marginals as a common multigrading.
2. Verify that every recursive gluing is the corresponding toric fibre product—not merely an informal overlap.
3. Identify the finite collection of allowed factor types.
4. Obtain or compute the resulting uniform degree bound.
5. Exhaust all degree-\(\le D\) generators symbolically and attach an MDS or expander detector.

**Limitation:** bounded **Markov degree** does not automatically bound every Graver element. Since CVP permits signed coefficients, this result alone does not prove M1. It is strongest when combined with the higher-Lawrence Graver theorem or a separate conformal localization result.

---

# 4. Rauh–Sullivant give the correct full-kernel lifting algorithm

**Johannes Rauh and Seth Sullivant, 2016, Journal of Symbolic Computation, “Lifting Markov Bases and Higher Codimension Toric Fiber Products.”**

### Precise construction

Their method decomposes a Markov basis of a higher-codimension toric fibre product into:

1. moves in the kernel of the projection to the common grading;
2. lifts of moves from the two factor ideals;
3. glued pairs of factor moves with compatible projected motion.

The lifting algorithm is valid when the projected fibers satisfy the compatible projection property; normality of an associated affine semigroup supplies a finite iterative lifting procedure. ([arxiv.org](https://arxiv.org/pdf/1404.6392.pdf))

### Why this is relevant

This is exactly the formalism missing from Q1’s old-primitive audit. The product tag changes the grading and therefore changes:

- the projection kernel,
- the projected fiber intersections,
- which factor moves can be glued,
- and the complete Markov basis.

Testing old rectangles separately cannot certify the enlarged matrix. Rauh–Sullivant give a mathematically complete way to enumerate the new splice classes.

### How to verify/adapt

For each proposed full tile:

1. Serialize the factor lattices \(L_{\rm NAND}\) and \(L_{\rm COPY}\).
2. Define the exact projection recording all shared rows and transfer gradings.
3. Compute:
   - a kernel Markov/Graver basis,
   - projected fiber intersections,
   - compatible lifts,
   - all glued moves.
4. Use normaliz/Macaulay2 to test normality of the associated semigroup.
5. Only after this computation should the sub-\(17E\) shell be enumerated.

This should replace “recompute the complete enlarged Graver basis” by a structured computation that also provides certificates for why specific seam movements do or do not extend.

---

# 5. Lossless expanders give deterministic cancellation-proof sparse detection

**Venkatesan Guruswami, Christopher Umans and Salil Vadhan, 2009, Journal of the ACM, “Unbalanced Expanders and Randomness Extractors from Parvaresh–Vardy Codes.”**

### Precise machinery

They construct explicit highly unbalanced left-regular bipartite graphs whose expansion is arbitrarily close to the left degree, with degree and right-side size polynomially close to optimal. ([eccc.weizmann.ac.il](https://eccc.weizmann.ac.il/report/2006/134/revision/1/download/))

For a left \(d\)-regular graph satisfying

\[
|N(X)|>(d/2)|X|
\qquad
\text{for every }0<|X|\le k,
\]

every such \(X\) has a unique neighbor. Otherwise every vertex in \(N(X)\) would receive at least two edges from \(X\), implying

\[
d|X|\ge 2|N(X)|,
\]

a contradiction. Hence the integer adjacency matrix \(H\) obeys

\[
Hx\ne0
\]

for every nonzero signed integer vector \(x\) supported on at most \(k\) coordinates: at a unique-neighbor row, \((Hx)_r\) is exactly one nonzero coefficient.

### Why this is relevant

This is the cleanest published mechanism behind M2. It handles arbitrary signs and does not rely on positivity or generic noncancellation.

Unlike the killed transfer channels, the graph can cover **all physical and auxiliary defect coordinates**. It is particularly attractive if Higher Lawrence gives a constant or logarithmic support bound but the defect alphabet is too large for a convenient MDS field.

### How to verify/adapt

- Instantiate an explicit GUV graph for the proven primitive-support bound.
- Use its integer adjacency matrix directly as emitted lattice rows.
- Prove that legal differences lie in the intended nullspace, or apply the graph after quotienting the honest-difference space.
- Check the energy cost of a nonzero detector row and balance it against common legal energy.
- Formally prove the unique-neighbor implication in Lean; the proof is elementary once the expansion certificate is imported.

---

# 6. Decomposable graphical models isolate the exact gluing topology where only swaps survive

**Adrian Dobra, 2003, Bernoulli 9(6), “Markov Bases for Decomposable Graphical Models.”**

### Precise statement

When the fixed marginals define a decomposable—equivalently chordal—independence graph, primitive data swaps are sufficient to form a Markov basis connecting every nonnegative integer table with those marginals. These moves are squarefree degree-two exchanges, and Dobra gives explicit formulas generating them from the clique/separator decomposition. ([projecteuclid.org](https://projecteuclid.org/journals/bernoulli/volume-9/issue-6/Markov-bases-for-decomposable-graphical-models/10.3150/bj/1072215202.pdf))

### Why this is relevant

The campaign repeatedly failed when locally sound gadgets were glued around cycles and acquired diagonal or parity splices. Dobra identifies a sharp adjacent-field distinction:

- **decomposable/chordal overlap:** fiber connectivity is controlled by local quadratic swaps;
- **nondecomposable overlap:** higher and more global moves can be necessary.

Thus one possible compiler strategy is to force the selector/bag incidence hypergraph to have a junction-tree decomposition, then certify every primitive seam move explicitly.

### How to verify/adapt

1. Construct the clique graph of the full bag system.
2. Test the running-intersection property.
3. If chordal, generate the degree-two swap basis from Dobra’s formulas.
4. Audit every resulting swap with the transfer detector.
5. If the compiler necessarily creates nonchordal overlaps, identify the minimal induced cycles; these are the likely locations of the next parity or diagonal splice.

Again, this controls nonnegative Markov connectivity rather than unrestricted Graver moves, so a signed-CVP extension is still required.

---

# 7. Kannan embedding gives an exact interval test for T1

**Kannan’s embedding technique; analyzed by Laura Luzzi, Damien Stehlé and Cong Ling, 2013, IEEE Transactions on Information Theory, “Decoding by Embedding: Correct Decoding Radius and DMT Optimality.”**

### Precise construction

The embedding replaces a CVP target \(t\) by the homogeneous lattice

\[
\widehat L_H
 =
\{(x-kt,kH):x\in L,\ k\in\mathbb Z\}.
\]

The literature analyzes this as a reduction from bounded-distance decoding to unique/shortest-vector problems and provides decoding guarantees in terms of \(\lambda_1(L)\) and the target distance. ([arxiv.org](https://arxiv.org/pdf/1102.2936))

For the campaign’s exact layer-forcing requirement, a direct calculation gives a useful sufficient criterion. Let

\[
d=\operatorname{dist}(t,L),\qquad \lambda=\lambda_1(L).
\]

The desired \(k=\pm1\) vectors have squared length \(d^2+H^2\). Nonzero \(k=0\) vectors have length at least \(\lambda\), while every \(|k|\ge2\) vector has length at least \(2H\). Therefore it suffices that

\[
\frac{d^2}{3}<H^2<\lambda^2-d^2.
\]

The interval is nonempty whenever

\[
d<\frac{\sqrt3}{2}\lambda.
\]

### Why this is relevant

This converts T1 from an open-ended shell experiment into a symbolic criterion. The real obstruction is not mysterious DROP behavior: it is whether all relevant affine target distances lie sufficiently below the shortest homogeneous lattice vector.

### How to verify/adapt

For each constant tile and each legal/adverse target class:

1. Compute \(d^2\) exactly by CVP enumeration.
2. Compute \(\lambda_1(L)^2\) exactly.
3. Intersect all rational intervals
   \[
   \left(d_i^2/3,\ \lambda^2-d_i^2\right).
   \]
4. If the intersection is nonempty, choose rational \(H^2\) inside it and certify every layer simultaneously.
5. If empty, T1 is dead for that affine lattice regardless of tensor machinery.

This test should be run before constructing any E-type recursion.

---

# 8. Haviv–Regev supply a non-E-type method for ruling out entangled tensor shortcuts

**Ishay Haviv and Oded Regev, 2012, Theory of Computing 8(23), “Tensor-based Hardness of the Shortest Vector Problem to within Almost Polynomial Factors.”**

### Precise machinery

They start from Khot-type constant-gap SVP lattices and amplify the gap using ordinary tensor powers. The substantive result is that those specially structured NO lattices remain sound under tensorization, despite the presence of nondecomposable tensor vectors. Their analysis uses a positive-semidefinite matrix inequality relating trace and determinant rather than asserting that every shortest vector is rank one. ([toc.cs.uchicago.edu](https://toc.cs.uchicago.edu/articles/v008a023/))

### Why this is relevant

This is an alternative to T3’s very restrictive E-type plan. It shows that tensor amplification can succeed even when entangled vectors exist, provided the base NO lattice has a suitable structural dichotomy.

The campaign’s literal tensor test failed by an isometry, not merely by entanglement. Haviv–Regev indicate the right target: certify a **formula-sensitive structural promise** on the homogeneous NO lattice, then prove that promise tensorizes.

### How to verify/adapt

- After exact homogenization, classify short vectors by coefficient matrix rank and support.
- Seek a two-case promise analogous to the Khot lattices:
  1. vectors with many independent components pay determinant/volume cost;
  2. low-rank vectors reduce to lower-level adverse states.
- Apply the trace–determinant inequality to the Gram matrix of a decomposition.
- Explicitly test that the NO and control seeds are not related by any coefficient or ambient isometry before tensoring.

This is less immediate than the Lawrence/MDS route, but it is the strongest published precedent for overcoming tensor entanglement without an E-type theorem.

---

# 9. Kitaoka’s verified rank bound is weaker than the roadmap currently states

**Yoshiyuki Kitaoka, 1976, Proceedings of the Japan Academy 52(9), “Tensor Products of Positive Definite Quadratic Forms.”**

### Precise statement

A positive-definite lattice \(L\) is of E-type if, for every positive-definite lattice \(M\), every minimal vector of \(L\otimes M\) is decomposable:

\[
z=x\otimes y.
\]

The 1976 paper states that \(L\) is of E-type if either an additional minimum/scale condition holds or

\[
\operatorname{rank}(L)<42.
\]

It also gives closure properties for E-type lattices and applications to indecomposability of tensor products. ([jstage.jst.go.jp](https://www.jstage.jst.go.jp/article/pjab1945/52/9/52_9_498/_pdf/-char/en))

### Why this is relevant

The primary source retrieved supports **rank at most 41**, not the roadmap’s stated “rank \(\le43\).” There may be a later sharpening, but it requires a precise citation and hypothesis audit before T3 can use ranks 42 or 43.

### How to verify/adapt

- Safest option: require every fresh factor to have rank \(\le41\).
- Otherwise locate and formally check the later theorem allegedly giving rank \(\le43\), including conventions concerning rank, integrality, scale and quadratic-form normalization.
- Do not treat “rank \(\le43\)” as established from the 1976 theorem.

---

## Recommended revised frontier

The most literature-supported next route is:

### **L1. Structural-recognition lemma**

Show that the complete recursive NAND/COPY matrix is either:

1. a higher Lawrence lifting of a fixed full tile matrix, or
2. an iterated toric fibre product from finitely many fixed tile types.

The first outcome gives a uniform Graver-type bound; the second gives bounded Markov degree and a complete lifting calculus.

### **L2. Full-selector MDS/expander detector**

After obtaining a primitive-support bound \(K\), attach a detector to the quotient defect coordinates containing:

- physical NAND selectors,
- physical COPY selectors,
- pair selectors,
- glue auxiliaries,
- DROP directions.

Use either:

- an \(\mathbb F_{289}\) Reed–Solomon parity-check matrix with designed distance \(>K\), or
- a GUV unique-neighbor matrix.

Pair-supported product channels alone should remain retired.

### **L3. Mandatory compatibility gate**

Before energy or valuation work, compute the honest affine-difference space \(U\) and prove

\[
\operatorname{Gr}(A_{\rm full})_{\rm malformed}\cap U=\varnothing
\]

within the primitive-support bound. If a malformed primitive lies in \(U\), every compatible linear detector—including MDS and expanders after quotienting—annihilates it, reproducing the Generation-13 obstruction.

## Immediate executable experiment

1. Serialize the exact 18-variable full candidate, including every physical and pair-dependent row.
2. Compute its honest-difference lattice \(U_{\mathbb Z}\) and quotient defect matrix.
3. Test whether its two-child and \(r\)-child compositions are higher Lawrence liftings.
4. If so, compute \(g(A)\) via the Santos–Sturmfels construction.
5. Build an MDS parity check of distance \(g(A)+1\) over \(\mathbb F_{289}\), with columns on **all** quotient coordinates.
6. Rerun unrestricted Hamming-one/two and sub-\(17E\) searches.
7. Only after this passes should \(P^2/P^3\) carry stabilization be attempted.

This is the clearest published route around the exact Generation-4/5 wall: **first obtain a theorem bounding complete primitive support, then use a designed-distance detector covering the entire primitive support.**
