I treat the live obstruction map as: **slack annihilation; bounded-box versus unbounded integrality; fixed-marginal/local-fiber limitation and overlap; sparse unsatisfaction; absence of a uniform family; explicit CVP radius/dimension accounting; PCP/conjecture dependence.** The Generation-4 empty-packet failure is procedural; every sketch below includes an executable test.

### 1. Integral sheaf with occurrence blow-up

**Mechanism.** Give every clause a satisfying-pattern selector, using one of the 18 certified local matrices, then glue variable occurrences by an integral coboundary matrix. Replace each occurrence by \(R\) copies and enforce equality on complete bipartite occurrence graphs, so one inconsistent local choice creates \(\Omega(R)\) or \(\Omega(R^2)\) nonzero coboundaries.

**Expected move.** Turn the local affine certificates into a global “integer cosystole”: every collection of satisfying local patterns either glues to a Boolean assignment or has polynomially large norm.

**Obstruction check.** **Slack:** no clause slack exists. **Unbounded integrality:** requires exact Smith/left-kernel proofs, not boxed search. **Local/overlap:** this directly targets it, but is currently unproved. **Sparse unsatisfaction:** occurrence blow-up should spread one inconsistency. **Uniform family:** complete bipartite gluing is explicit. **CVP accounting:** all maps are integral linear rows, but baseline-versus-dimension analysis remains open. **PCP:** direct deterministic repetition only.

**Falsification.** Any short global integer kernel vector mixing clauses kills it.

**Experiment.** Compose every pair of the 18 matrices on two clauses sharing one or two variables, with \(R=2\); perform exact integer feasibility and enumerate all vectors below squared norm \(8\).

**Likely death.** Signed selectors circulate around overlap cycles while every local block remains legal.

---

### 2. Guarded multi-prime Construction-A locking

**Mechanism.** Encode normalization, marginals, and clause legality as simultaneous congruences modulo several small coprime primes, then realize them as a Construction-A lattice via Hermite normal form. Add Euclidean guard coordinates for quotient variables, preventing a large multiple of a prime from cheaply masquerading as zero residue.

**Expected move.** A harmful selector must either violate some modulus—paying an amplified residue cost—or use a large quotient—paying guard norm.

**Obstruction check.** **Slack:** unlike the killed multi-prime variant, there is no free residual-zeroing slack; the whole selector system is modularized. **Unbounded integrality:** quotient guards must yield a radius-derived global bound. **Local/overlap:** global bits are shared across every modular block, but composition remains unproved. **Sparse unsatisfaction:** repeat or scale each prime residue block. **Uniform family:** consecutive polynomial-size primes and HNF are explicit. **CVP accounting:** HNF supplies a genuine basis; determinant, radius, and dimension still need calculation. **PCP:** no gap theorem or conjecture is invoked.

**Falsification.** A short vector using CRT carries or quotient cancellation.

**Experiment.** Encode the eight-clause unsatisfiable three-variable formula modulo \(2,3,5\); construct the HNF basis and exactly enumerate all vectors up to the Boolean completeness radius.

**Likely death.** Guard costs needed to stop carries also raise completeness enough to erase the ratio.

---

### 3. Deterministic Euclidean embedding of the full defect space

**Mechanism.** Let \(d=Az-b\) contain every normalization, marginal, overlap, and clause defect—not merely clause residuals. Search for a small integral sign matrix \(M\) satisfying \(\|Md\|_2^2\ge R\|d\|_2^2/2\) for every defect attainable by a candidate vector inside the proposed soundness ball.

**Expected move.** Any nonzero global defect is spread over \(R\) coordinates while valid witnesses, having \(d=0\), incur no amplified completeness cost.

**Obstruction check.** **Slack:** free slack cannot help unless it zeros the complete defect vector. **Unbounded integrality:** anchors must prove that candidates below the soundness radius lie in a finite box. **Local/overlap:** exposed—the global \(A\) must first have no harmful zero-defect point. **Sparse unsatisfaction:** one nonzero defect receives \(\Theta(R)\) energy. **Uniform family:** deterministic construction of \(M\) is unresolved; exhaustive search is only experimental. **CVP accounting:** \(MA\) is integral and directly appendable, but dimension and coefficient bounds need proof. **PCP:** this is direct norm embedding, not constraint-gap amplification.

**Falsification.** Either \(Az=b\) has a harmful integer solution or every small \(M\) has a low-energy attainable defect.

**Experiment.** Build the two-clause overlap systems and greedily search \(M\in\{\pm1\}^{32\times r}\), exactly enumerating radius-bounded defects.

**Likely death.** The attainable defect set is too large to derandomize in polynomial time.

---

### 4. Algebraic-norm certificate through a Veronese lift

**Mechanism.** Encode Boolean defects \(x_i(x_i-1)\) and false-clause indicators \(\prod_j(1-\ell_j)\) as coefficients of one algebraic integer \(a\) in a degree-\(D\) number field. If any defect is nonzero and coefficient representation is unique, then \(|N(a)|\ge1\), so AM–GM across all embeddings forces \(\|\sigma(a)\|_2\ge\sqrt D\).

**Expected move.** Obtain simultaneous amplification without clause slack or cancellation between distinct defects.

**Obstruction check.** **Slack:** false clauses are represented directly by products. **Unbounded integrality:** the norm bound is global for algebraic integers. **Local/overlap:** one global monomial table handles shared variables. **Sparse unsatisfaction:** even one nonzero coefficient gives nonzero norm; tensoring could enlarge the gap. **Uniform family:** explicit fields exist, but discriminant and bit-size control are unresolved. **CVP accounting:** critically exposed—the Veronese relations are nonlinear and must be enforced by linear lattice geometry. **PCP:** purely algebraic.

**Falsification.** A short linearized assignment violates rank-one/monomial consistency while making \(a=0\).

**Experiment.** For three variables and all eight clauses, introduce degree-\(\le3\) monomial variables; exhaustively search short integer solutions to the proposed linear consistency rows and report fake monomial tables.

**Likely death.** Linear CVP constraints cannot enforce the required multiplicative relations without reintroducing signed-selector cheats.

---

### 5. Carry-free mixed-radix defect compression

**Mechanism.** Order all global affine defects \(d_1,\dots,d_m\) and add rows \(\sum_i B^{\pi_j(i)}d_i\), with one permutation \(\pi_j\) placing coordinate \(j\) last. If \(|d_i|\le K\) and \(B>2K+1\), the highest nonzero digit cannot be cancelled, giving an exponentially large measurement using only polynomial coefficient bit-length.

**Expected move.** Convert mere nonzero global defect into a huge Euclidean separation, potentially yielding a polynomial factor after dimension accounting.

**Obstruction check.** **Slack:** all selector and overlap defects are packed, not residuals alone. **Unbounded integrality:** the required \(K\) must be derived from anchor cost inside the claimed radius. **Local/overlap:** exposed; a harmful exact solution \(d=0\) defeats every radix row. **Sparse unsatisfaction:** each coordinate is highest in one row. **Uniform family:** the \(m\) permutations and powers of \(B\) are explicit. **CVP accounting:** rows are integral and bit-length is polynomial, but completeness radius and coefficient growth require exact analysis. **PCP:** deterministic arithmetic only.

**Falsification.** A short exact zero-defect selector, or a carry vector within the claimed radius.

**Experiment.** Apply radix rows with \(B=9\) to every composed two-clause system; exact-enumerate vectors below increasing radii and compare against uncompressed optima.

**Likely death.** Global affine feasibility admits non-Boolean zero-defect points, which no weighting can detect.

---

### 6. Seven-vertex Delaunay clause cells

**Mechanism.** Search for a lattice-target pair whose nearest vectors project exactly onto the seven satisfying patterns of a 3-OR clause; the falsifying pattern lies beyond a controlled second shell. Glue clause lattices by fiber products identifying shared Boolean projection coordinates, seeking a global Voronoi cell whose nearest vectors correspond precisely to satisfying assignments.

**Expected move.** Make clause legality intrinsic to nearest-vector geometry, eliminating auxiliary slack and affine selector normalization.

**Obstruction check.** **Slack:** none is introduced. **Unbounded integrality:** exact Voronoi enumeration can certify all lattice vectors, not merely a box. **Local/overlap:** fiber-product gluing is the central unresolved step. **Sparse unsatisfaction:** ordinary direct sums give only constant shell loss; a global shell-separation construction is still needed. **Uniform family:** no scalable cell family is known here. **CVP accounting:** native CVP geometry gives an explicit basis and target once found. **PCP:** no external gap machinery.

**Falsification.** An eighth equally close projection, or a glued vector closer than every Boolean-consistent vector.

**Experiment.** Use SMT/MILP to search dimensions \(4\)–\(6\) for small integral Gram matrices and rational targets realizing exactly seven prescribed nearest projections; certify candidates using eigenvalue bounds plus exact enumeration.

**Likely death.** Voronoi convexity forces extra nearest vectors, and shell ratios collapse under fiber products.

---

### 7. Cover-free isolation of short harmful supports

**Mechanism.** Regard the global defect vector as an unknown signed support. Append rows from a signed disjunct measurement family so that, for every support of size at most \(s\), some row isolates one nonzero defect from all others; repeat isolating rows to amplify its Euclidean contribution. Dense defects should already be expensive in \(\ell_2\).

**Expected move.** Split soundness into “sparse defects isolated combinatorially” and “dense defects large by norm,” avoiding cancellation without enormous radix coefficients.

**Obstruction check.** **Slack:** measurements see the complete defect vector. **Unbounded integrality:** anchors must derive coefficient and support bounds from the radius. **Local/overlap:** global zero-defect cheats remain fatal and must be audited first. **Sparse unsatisfaction:** this is the mechanism’s direct target. **Uniform family:** explicit cover-free families are available in principle, but required parameters may be superpolynomial. **CVP accounting:** measurements are integral linear rows; final dimension and baseline remain open. **PCP:** deterministic group testing, not a PCP composition.

**Falsification.** A short signed defect support not isolated by any row, or an unaffordable \(s\)-parameter.

**Experiment.** Enumerate attainable defects for the eight-clause core with selector coefficients in \([-2,2]\); greedily construct a \(3\)-disjunct signed matrix and compute the exact minimum amplified norm.

**Likely death.** Soundness requires \(s\) polynomial in instance size, causing quadratic-or-worse dimension growth that consumes the gap.

Classical ingredients used only as mechanism vocabulary: Construction A and Voronoi/Delaunay theory as presented in Conway–Sloane, *Sphere Packings, Lattices and Groups* (3rd ed., 1999); cover-free/superimposed codes from Kautz–Singleton, *IEEE Transactions on Information Theory* 10 (1964).
