## Literature scout report

I found **no published theorem that directly yields the requested deterministic polynomial-factor Euclidean GapCVP reduction without PCP machinery**. The strongest reusable pieces instead suggest a three-stage architecture:

1. **Eliminate bounded-support parity kernels** using Boolean Möbius/Reed–Muller machinery plus splitters or unique-neighbor expanders.
2. **Audit composition universally** using Graver/Markov bases and higher Lawrence liftings, rather than checking named attacks.
3. **Amplify a genuinely nonzero defect** using either ramified quaternion-ideal depth or a tensor class with a proven no-entanglement theorem.

During broad searches, an OpenAI-CDN result that appeared potentially related to the prohibited recent material surfaced. I discarded it without opening or using it. Nothing below depends on it.

---

# Ranked findings

## 1. Reed–Muller duality gives the exact parity-kernel threshold—and full Möbius lifting removes the kernel

**Source.** P. Delsarte, J.-M. Goethals, F. J. MacWilliams, 1970, *Information and Control*, “On generalized Reed–Muller codes and their relatives.” Later trade literature gives the equivalent signed-design formulation. ([core.ac.uk](https://core.ac.uk/download/pdf/82417593.pdf))

### Precise machinery

Let

\[
M_{\le d,m}[S,x]=\prod_{i\in S}x_i,
\qquad |S|\le d,\quad x\in\{0,1\}^m.
\]

Thus \(M_{\le d,m}\) records every squarefree moment through degree \(d\).

If \(0\ne z\in\ker_{\mathbb Z}M_{\le d,m}\), divide by the gcd of its coefficients and reduce modulo \(2\). The resulting nonzero binary vector is orthogonal to \(RM(d,m)\), hence lies in

\[
RM(d,m)^\perp=RM(m-d-1,m).
\]

The minimum distance of this dual code is

\[
2^{d+1}.
\]

Therefore every nonzero integral moment-kernel vector has

\[
|\operatorname{supp}z|\ge 2^{d+1}.
\]

The bound is tight: on any \((d+1)\)-dimensional Boolean subcube,

\[
z_x=(-1)^{|x|}
\]

annihilates every polynomial of degree at most \(d\).

At the other extreme, taking **all** squarefree monomials gives the Boolean zeta matrix

\[
Z[S,T]=\mathbf 1[S\subseteq T].
\]

After ordering subsets by inclusion, \(Z\) is unitriangular, so \(\det Z=1\). Its inverse is the integral Möbius matrix

\[
Z^{-1}[S,T]=(-1)^{|T\setminus S|}\mathbf 1[S\subseteq T].
\]

Hence the full Boolean moment lift is **unimodular and kernel-free over \(\mathbb Z\)**.

### Relevance

This exactly explains the recurring seven-term/cube-parity phenomena in Generations 9, 11, 31, 32, and 37:

- degree-\(d\) moments cannot eliminate the alternating \((d+1)\)-cube;
- adding cross-copy copies of the same truncated moment system does not help;
- the obstruction is not accidental—it is a minimum-weight dual Reed–Muller word.

It also gives a precise cure: full local Möbius coordinates eliminate every signed affine collision, rather than merely increasing its weight.

### How to adapt or verify

1. For each proposed bag with \(m\) Boolean variables, emit the complete \(2^m\times2^m\) zeta/Möbius block.
2. Verify its Smith form is the identity.
3. If full lifting is too large, choose \(d\) so \(2^{d+1}>K\), where \(K\) is the maximum support of any vector allowed by the CVP shell.
4. Combine this with Finding 3 so that \(m=O(\log n)\), making \(2^m\) polynomial.

This is probably the highest-leverage response to the parity kernel.

---

## 2. Higher Lawrence liftings precisely characterize why linear copy composition preserves local attacks

**Source.** Francisco Santos and Bernd Sturmfels, 2003, *Journal of Combinatorial Theory, Series A* 103(1), 151–164, “Higher Lawrence Configurations.” ([arxiv.org](https://arxiv.org/pdf/math/0209326))

### Precise machinery

For an integer configuration \(A=\{a_1,\dots,a_n\}\), its \(r\)-th Lawrence lifting \(A^{(r)}\) has relation lattice

\[
\ker_{\mathbb Z} A^{(r)}
=
\left\{
(u^{(1)},\dots,u^{(r)}):
u^{(i)}\in\ker_{\mathbb Z}A,\ 
\sum_{i=1}^r u^{(i)}=0
\right\}.
\]

In particular, every local kernel vector \(u\in\ker_{\mathbb Z}A\) gives the universal type-two relation

\[
(u,-u,0,\dots,0)\in\ker_{\mathbb Z}A^{(r)}.
\]

Santos–Sturmfels also prove stabilization results for Markov and Graver bases of these liftings. The associated **Graver complexity** bounds the number of nonzero rows needed by any primitive relation, independently of the number \(r\) of copies. ([arxiv.org](https://arxiv.org/pdf/math/0209326))

More generally, every integer kernel vector is a conformal sum of Graver-basis elements, so the Graver basis is a finite universal obstruction set for a fixed base matrix.

### Relevance

This puts the Generation-32/37 additive parity and the ordered-pair diagonal splice into a standard theorem:

> If the composition rows only require each copy to satisfy the same base system and impose linear zero-sum/coherence conditions between copies, then every surviving base kernel automatically produces a two-copy kernel.

Thus strict superadditivity is impossible until the **one-copy relation lattice itself** has been eliminated or nonlinearly lifted. Adding more linear cross-copy moments cannot cure a local kernel that embeds as \(u,-u\) or diagonally.

### How to adapt or verify

- Build the exact one-tile matrix \(A\), including all proposed coherence coordinates.
- Compute \(\operatorname{Gr}(A)\) with `4ti2`, Normaliz, or exact custom enumeration.
- Treat every Graver element as a mandatory attack, not just G13/G19/parity/DROP.
- Before testing depth two, symbolically construct \(A^{(2)}\) and verify whether every \(u\in\operatorname{Gr}(A)\) has a type-two or diagonal embedding.
- Any proposed extra tag must be shown nonzero on every relevant Graver element while preserving completeness.

This is the right universal composition gate.

---

## 3. Explicit splitters and lossless expanders can turn bounded-support defects into kernel-free linear syndromes

**Sources.**

- Moni Naor, Leonard Schulman, Aravind Srinivasan, 1995, FOCS, “Splitters and Near-Optimal Derandomization.”
- Michael Capalbo, Omer Reingold, Salil Vadhan, Avi Wigderson, 2002, STOC, “Randomness Conductors and Constant-Degree Lossless Expanders.”
- Venkatesan Guruswami, Christopher Umans, Salil Vadhan, 2009, *JACM* 56(4), “Unbalanced Expanders and Randomness Extractors from Parvaresh–Vardy Codes.” ([wisdom.weizmann.ac.il](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/splitters.pdf))

### Precise machinery

A left-\(D\)-regular lossless expander satisfies, for every left set \(S\) of size at most \(K\),

\[
|\Gamma(S)|\ge (1-\varepsilon)D|S|.
\]

Counting edge collisions shows that the number of right vertices having exactly one neighbor in \(S\) is at least

\[
(1-2\varepsilon)D|S|.
\]

Consequently, if \(\varepsilon<1/2\), the adjacency matrix \(H\) has the following **field-independent and integer-independent kernel property**:

\[
0\ne x,\quad |\operatorname{supp}x|\le K
\quad\Longrightarrow\quad Hx\ne0.
\]

Indeed, a unique neighbor \(r\) of a support coordinate \(i\) has

\[
(Hx)_r=x_i\ne0.
\]

Naor–Schulman–Srinivasan give deterministic splitter/perfect-hash constructions close to the probabilistic size bound. In particular, for \(K=O(\log n)\), suitable families can be made polynomial-size. ([wisdom.weizmann.ac.il](https://www.wisdom.weizmann.ac.il/~naor/PAPERS/splitters.pdf))

### Relevance

This is the scalable version of the Generation-38 splitter-bag idea and a genuine “kernel-free lift” for sparse defects.

It avoids the G13 compatibility failure if \(H\) acts not on the raw honest selectors but on **defect coordinates that are identically zero on every honest encoding**. Then no common-target affine-span requirement is imposed.

The missing lemma becomes sharply defined:

> Prove that every vector inside the candidate CVP soundness shell has defect support at most \(K=O(\log n)\).

Once that is established, a unique-neighbor matrix eliminates all such integer kernel vectors without relying on a modulus or coefficient bound.

### How to adapt or verify

1. Define a nonlinear local defect map using full Möbius coordinates from Finding 1.
2. Prove a shell inequality of the form
   \[
   \|z-z_{\rm honest}\|^2\le T\implies
   |\operatorname{supp}\Delta(z)|\le K.
   \]
3. Use an explicit splitter to isolate the support or an explicit lossless expander to measure it.
4. Verify the expansion property combinatorially, not probabilistically.
5. Check every Graver support through size \(K\) has a unique check.

This combination—**Möbius defects plus unique-neighbor expansion**—looks like the strongest classical candidate for repairing both parity and composition.

---

## 4. Ramified quaternion ideals provide a genuine multiplicative depth parameter and exponential trace lower bounds

**Sources.**

- John Voight, 2021, *Quaternion Algebras*, Graduate Texts in Mathematics 288.
- J. Z. Gonçalves and D. S. Passman, 2010, *Journal of Group Theory* 13(5), 721–742, “Involutions and Free Pairs of Bicyclic Units in Integral Group Rings.” ([link.springer.com](https://link.springer.com/content/pdf/10.1007/978-3-030-56694-4_14.pdf))

### Precise machinery

The group-ring failure is structural. If \(B=\langle b\rangle\) and

\[
\widehat B=\sum_{g\in B}g,
\]

then

\[
x=(1-b)a\widehat B
\]

has \(x^2=0\), because \((1-b)\widehat B=0\). Therefore

\[
1+x
\]

is a unit with inverse \(1-x\). These are the classical bicyclic units underlying exactly the kind of nilpotent fusion seen in the \(A_5\) experiment. ([people.math.wisc.edu](https://people.math.wisc.edu/~passman/bicyclic.pdf))

For the quaternion replacement, let \(B/\mathbb Q\) be definite and ramified at \(p\), and let \(\mathcal O_p\) be its local maximal order. Then:

- \(\mathcal O_p\) is the unique maximal order;
- it has a unique maximal two-sided ideal \(P\);
- \(P^2=p\mathcal O_p\), up to the conventional choice of local uniformizer;
- \(\mathcal O_p/P\cong\mathbb F_{p^2}\);
- choosing a uniformizer \(\pi\), multiplication satisfies the skew relation
  \[
  \pi a=a^p\pi
  \quad\text{mod higher filtration}.
  \]

Globally, for \(0\ne x\in P^k\) in a definite order,

\[
\operatorname{Nrd}(x)\in p^k\mathbb Z_{>0}.
\]

Hence the positive trace energy obeys

\[
\operatorname{Trd}(x\bar x)
=
2\operatorname{Nrd}(x)
\ge 2p^k.
\]

The local ramified-order structure is standard in the arithmetic of quaternion algebras. ([link.springer.com](https://link.springer.com/content/pdf/10.1007/978-3-030-56694-4_14.pdf))

### Relevance

This supplies something the Euclidean moment constructions currently lack: a **depth index whose nonzero energy grows exponentially with depth**.

It also explains why the group-algebra approach failed: ordinary finite-group rings contain square-zero directions, while a quaternion division algebra has no zero divisors.

The grade-zero attack in Goal-directed Generation 11 identifies the exact condition needed:

> Every false boundary must be forced into \(P\), and composition must force a depth-\(k\) false state into \(P^k\), not permit it to remain in the residue field.

The redundant-signature survivor is therefore relevant: it may provide the local affine separation needed before the quaternion filtration begins.

### How to adapt or verify

Work first entirely in the associated graded ring:

\[
\operatorname{gr}_P(\mathcal O)
\simeq
\mathbb F_{p^2}[\Pi;\mathrm{Frob}]/(\text{graded relation}).
\]

For each NAND and COPY boundary:

1. Compute the grade-zero fiber over \(\mathbb F_{p^2}\).
2. Prove false fibers are empty in grade zero.
3. Compute the grade-one transfer map and test injectivity.
4. At depth two, verify valuations add under composition:
   \[
   v_P(xy)=v_P(x)+v_P(y).
   \]
5. Only after this finite graded audit construct the integral maximal-order lattice and invoke
   \[
   E(x)\ge2p^{v_P(x)}.
   \]

This is the most credible existing route to an actual growing ratio, but COPY and all-depth graded injectivity remain substantial missing lemmas.

---

## 5. Noncommutative algebraic branching programs preserve path order and have deterministic identity testing

**Sources.**

- David Barrington, 1989, *Journal of Computer and System Sciences* 38(1), 150–164.
- Noam Nisan, 1991, STOC, “Lower Bounds for Non-Commutative Computation.”
- Ran Raz and Amir Shpilka, 2005, *Computational Complexity*, “Deterministic Polynomial Identity Testing in Non-Commutative Models.” ([people.cs.umass.edu](https://people.cs.umass.edu/~barring/publications/bwbp.pdf))

### Precise machinery

Barrington constructs from a fan-in-two Boolean circuit of depth \(d\) a width-five permutation branching program of length at most \(4^d\), whose product is a fixed nontrivial \(5\)-cycle in the accepting case. ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/0022000089900378))

A noncommutative ABP computes

\[
P=\sum_{\pi:s\leadsto t}\prod_{e\in\pi}\ell(e)
\]

in the free algebra \(\mathbb F\langle X\rangle\). Distinct transition words are linearly independent monomials.

For a homogeneous degree-\(D\) polynomial \(P\), Nisan defines prefix/suffix coefficient matrices \(M_k(P)\). The minimum homogeneous ABP size is characterized by

\[
\sum_{k=0}^{D}\operatorname{rank}M_k(P).
\]

Raz–Shpilka give a deterministic polynomial-time white-box identity test for noncommutative ABPs. ([link.springer.com](https://link.springer.com/article/10.1007/s00037-005-0188-8))

### Relevance

The G19 linear flow encoding forgets ordered multiplication. Conservation equations only record scalar flow, so positive and negative path fragments can splice.

In the free algebra, different path histories cannot cancel unless they have the same transition word. Thus the correct arithmetization target is not the scalar ACCEPT fiber but an ordered path polynomial or its prefix/suffix spaces.

### How to adapt or verify

- Label each transition occurrence by a noncommuting symbol, including query identity and branch value.
- Evaluate the G19 signed witness as a noncommutative polynomial.
- Run Raz–Shpilka basis propagation. If the polynomial is nonzero, it gives an explicit layer and linear functional detecting the splice.
- Emit coordinates representing the computed prefix/suffix bases rather than only unary flow totals.
- Introduce pair variables for each adjacent-layer multiplication and repeat basis reduction after every layer.

The unresolved issue is translating multiplication consistency into an ordinary linear CVP lattice without recreating a Lawrence kernel. Still, this gives a deterministic, polynomial-time way to find the **first missing coherence equation** in any proposed branching-program lift.

---

## 6. Markov bases and decomposable graphical models classify every marginal-preserving composition move

**Sources.**

- Persi Diaconis and Bernd Sturmfels, 1998, *Annals of Statistics* 26(1), 363–397.
- Adrian Dobra, 2003, *Bernoulli* 9(6), 1093–1108, “Markov Bases for Decomposable Graphical Models.” ([jstor.org](https://www.jstor.org/stable/pdf/119991.pdf?addFooter=false))

### Precise machinery

For an integer matrix \(A\), a finite set

\[
\mathcal B\subseteq\ker_{\mathbb Z}A
\]

is a Markov basis iff, for every \(b\), the graph on the nonnegative fiber

\[
\{x\in\mathbb Z_{\ge0}^n:Ax=b\}
\]

with moves \(\pm\mathcal B\) is connected. Diaconis–Sturmfels prove this is equivalent to the corresponding binomials generating the toric ideal \(I_A\). ([jstor.org](https://www.jstor.org/stable/pdf/119991.pdf?addFooter=false))

Dobra proves that when the fixed marginals form a decomposable/chordal graphical model, the Markov basis is given by explicitly described **primitive data swaps** supported across clique separators. ([projecteuclid.org](https://projecteuclid.org/journals/bernoulli/volume-9/issue-6/Markov-bases-for-decomposable-graphical-models/10.3150/bj/1072215202.full))

### Relevance

Pair bags, splitter bags, laminar hierarchies, and moment-consistency systems are all marginal-table models. Their integer kernels should therefore be studied as toric ideals.

This gives:

- a complete finite obstruction basis for a fixed bag template;
- an exact account of which moves arise when bags are glued;
- a way to design chordal/running-intersection compositions whose primitive moves remain localized.

It also clarifies the limitation: Markov-basis connectivity is a theorem for **nonnegative** fibers. The campaign’s signed vectors bypass it. Therefore any use of this machinery must be paired with a metric lemma forcing every near-optimal coefficient block into the nonnegative fiber.

### How to adapt or verify

1. Encode the bag system as a hierarchical-model design matrix.
2. Chordal-complete the bag interaction graph.
3. Compute its separator swaps symbolically using Dobra’s formulas.
4. Confirm with `4ti2` that these generate the toric ideal.
5. Design local spherical/Möbius tags that charge each primitive swap.
6. Separately prove that the target shell excludes negative coefficients.

This is preferable to continuing ad hoc overlap enumeration.

---

## 7. Kitaoka’s E-type theorem gives a genuine no-entangled-shortest-vector tensor class

**Source.** Yoshiyuki Kitaoka, 1977 onward, the “Scalar Extension” and “Tensor Products of Positive Definite Quadratic Forms” series; consolidated in *Arithmetic of Quadratic Forms*, Cambridge Tracts in Mathematics 106, 1993. ([projecteuclid.org](https://projecteuclid.org/journals/nagoya-mathematical-journal/volume-67/issue-none/Scalar-extension-of-quadratic-lattices-II/nmj/1118796476.short))

### Precise machinery

A positive-definite lattice \(L\) is of **E-type** if, for every positive-definite lattice \(M\), every minimal vector of

\[
L\otimes M
\]

is decomposable:

\[
v=x\otimes y.
\]

Consequently,

\[
\lambda_1(L\otimes M)
=
\lambda_1(L)\lambda_1(M).
\]

Kitaoka proves that every positive-definite integral lattice of rank at most \(43\) is of E-type. Later tensor-lattice literature explicitly reviews this threshold and its consequences. ([arxiv.org](https://arxiv.org/pdf/1201.1832))

### Relevance

This is the strongest classical answer to the campaign’s “tensor coherence” requirement. It removes arbitrary entangled shortest vectors without assuming rank one.

Because E-type is quantified over **every** \(M\), a fixed rank-\(\le43\) factor can in principle be applied repeatedly:

\[
\lambda_1(L^{\otimes k})
=
\lambda_1(L)^k,
\]

with minimal vectors recursively decomposable.

### How to adapt or verify

The obstruction is that GapCVP is affine, whereas E-type is a homogeneous SVP theorem. A viable adaptation would need:

1. a rank-\(\le43\) local factor;
2. a Kannan-style homogenization of the target coset;
3. a proof that every shortest augmented vector has final coefficient \(\pm1\), excluding multiples and zero-layer vectors;
4. distinct YES/NO seeds not related by a coefficient/ambient isometry.

The immediate experiment is to take the surviving rank-\(32\) or another rank-\(\le43\) tile, construct an augmented homogeneous lattice, and enumerate whether the shortest vectors corresponding to the target coset remain the only minimal vectors. If that gate passes, Kitaoka supplies the all-depth tensor theorem that the literal G30 experiment lacked.

---

## 8. Khot and Haviv–Regev show how structured lattice instances survive arbitrary tensor entanglement

**Sources.**

- Subhash Khot, 2005, *Journal of the ACM*, “Hardness of Approximating the Shortest Vector Problem in Lattices.”
- Ishay Haviv and Oded Regev, 2012, *Theory of Computing* 8, “Tensor-based Hardness of the Shortest Vector Problem to within Almost Polynomial Factors.” ([scilit.com](https://www.scilit.com/publications/ff3e8c84f0aee38566d8e936630b2950))

### Precise machinery

Khot constructs BCH-code-based lattice instances and an augmented tensor operation for which the NO structure is stable enough to amplify a constant gap.

Haviv–Regev later show that ordinary tensor powers of Khot’s special lattices suffice. Their soundness analysis applies to **arbitrary tensor-lattice vectors**, not merely pure tensors. The core estimates use a positive-semidefinite trace/determinant inequality after expressing a tensor through independent component vectors. Their resulting tensor powers amplify the hardness factor to almost polynomial size under the complexity assumptions stated in their paper. ([cims.nyu.edu](https://cims.nyu.edu/~regev/papers/svphard.pdf))

### Relevance

The lesson is that tensoring is not justified by a good one-copy ratio. One first needs a structural NO dichotomy stable under tensor products—roughly, every short vector must fall into controlled support/divisibility classes.

That is precisely what the G30 seed lacked: the NO and control were isometric. G32/G37 likewise lacked a structural tensor dichotomy because parity vectors remained additive.

### How to adapt or verify

Extract from a candidate CVP gadget its homogeneous difference lattice and test for a Khot-style dichotomy such as:

- every nonzero short vector has many nonzero coordinates; or
- it lies in a properly scaled/divisible sublattice; or
- every low-rank tensor representation has a determinant/volume lower bound.

Then reproduce the Haviv–Regev matrix argument symbolically for the candidate Gram. Do this **before** constructing depth-two tensors. If a parity or signed-flow witness violates the dichotomy, standard tensor amplification cannot work.

The base hardness in these papers does not meet the requested “without PCP” goal, but their tensor soundness argument is separable machinery.

---

## 9. Total unimodularity gives exact flow rigidity—conditional on first proving nonnegativity

**Source.** Alan Hoffman and Joseph Kruskal, 1956, “Integral Boundary Points of Convex Polyhedra”; classical integral-flow and flow-decomposition theorems. ([cs.umd.edu](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf))

### Precise machinery

If \(A\) is totally unimodular and \(b\) is integral, then

\[
\{x\ge0:Ax=b\}
\]

has integral vertices. Conversely, the corresponding universal integrality property characterizes total unimodularity.

For a directed network, the incidence matrix is totally unimodular, and every nonnegative integral flow decomposes into integral path flows and cycle flows. ([users.soe.ucsc.edu](https://users.soe.ucsc.edu/~sesh/Teaching/2021/CSE202/Slides/lec12-tu-integrality.pdf))

### Relevance

This isolates exactly what was missing in G19:

- conservation and ACCEPT equations already form an integral network system;
- the attack exists solely because CVP coefficients may be negative;
- if the metric forced every near-optimal edge coefficient to be nonnegative, ordinary flow decomposition would reduce it to honest paths plus cycles.

Thus the problem is not a stronger flow theorem; it is a geometric **near-shell nonnegativity lemma**.

### How to adapt or verify

Search for a constant-size equal-radius edge code with:

\[
E(0)=E(1)=R,
\qquad
E(a)\ge R+\Delta |a|
\quad\text{for }a<0\text{ or }a>1,
\]

where \(\Delta\) scales with the whole completeness radius rather than remaining constant per malformed edge. If such a block exists and composes without DROP, TU and flow decomposition provide the rest of the accepting-path rigidity automatically.

---

# Recommended research order

## A. First gate: exact local kernel elimination

Implement complete Boolean Möbius coordinates on each candidate local bag. Prove by determinant or Smith form that the local label map is unimodular. Do not proceed with any local matrix having a nonzero integer kernel; higher Lawrence theory says it will reappear under composition.

## B. Scalable localization

Use an explicit splitter or lossless expander with \(K=\Theta(\log n)\). The target lemma should be:

\[
\text{distance}\le T
\quad\Longrightarrow\quad
\text{at most }K\text{ nonzero Möbius defects}.
\]

Unique-neighbor expansion then removes all such sparse integer defects.

## C. Universal composition audit

Compute the Graver basis of the resulting fixed local template and the Markov basis of the bag-gluing system. Every primitive move must either:

- be impossible because the local lift is kernel-free; or
- acquire a quantified nonzero defect at a unique-neighbor check.

This would replace generations of named-attack testing with a theorem-level finite certificate.

## D. Choose one amplifier

Two plausible but separate routes remain:

1. **Quaternion route:** prove false transfers increase \(P\)-adic valuation at every depth, obtaining energy \(2p^k\).
2. **Tensor route:** homogenize a rank-\(\le43\) CVP tile and prove the target-coset vectors are the only minimal vectors, then invoke E-type tensoring.

The quaternion route naturally supplies exponential depth growth; the E-type route has a much cleaner existing tensor-coherence theorem but requires a difficult affine-to-homogeneous bridge.

## E. Branching-program fallback

Before attempting another flow lattice, run noncommutative ABP basis propagation on the exact G19 signed witness. This should identify the minimum set of ordered-prefix coordinates needed to detect it. If those coordinates cannot be linearized without a Lawrence kernel, abandon the flow route early.

---

## Bottom line

The most actionable classical synthesis is:

\[
\boxed{
\text{local Möbius-unimodular lift}
\;+\;
\text{splitter/unique-neighbor localization}
\;+\;
\text{Graver-complete composition audit}
}
\]

followed by either

\[
\boxed{\text{ramified quaternion ideal-depth amplification}}
\]

or, if a suitable affine homogenization can be proved,

\[
\boxed{\text{rank-}\le43\text{ E-type tensor amplification}.}
\]

The literature strongly indicates that **no purely linear moment, marginal, or copy-coherence extension can succeed while a one-copy integer kernel remains**. The next useful experiment should therefore certify kernel-freeness or sparse-kernel exclusion as a theorem before testing any further composition rule.
