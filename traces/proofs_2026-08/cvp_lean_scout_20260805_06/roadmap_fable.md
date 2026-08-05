I did not use or consult the prohibited recent document or any account of it. The routes below use only the supplied obstruction map and classical machinery.

Let \(S\) denote the size of the 3SAT instance and \(n\) the output lattice dimension.

## Strategy 1 — Ramified-quaternion depth amplification

Use the surviving redundant-signature NAND module, but replace additive repetition by multiplication in a definite quaternion order ramified at \(p=17\).

### Lemma chain

**Q1. Saturated NAND/COPY tile lemma.**  
Construct fixed integral tiles over a maximal order \(\mathcal O\subset(-3,-17)\) with prime ideal \(P\), encoding NAND and COPY boundaries, such that:

1. every legal boundary has an integral realization of squared energy at most \(E\);
2. DROP and every false boundary have no grade-zero realization;
3. every false realization has a defect in \(P\);
4. the legal fibers and all false fibers are saturated over \(\mathbb Z\).

The existing \(N=8\) redundant NAND module proves the local energy part for NAND; COPY and grade-zero exclusion remain open.

**Q2. Valuation-transfer lemma.**  
For every composed gate, if a child carries a false defect in \(P^a\), while the other inputs are legal or deeper, then the parent defect belongs to \(P^{a+1}\). No signed integral coupling may return it to grade zero. Equivalently, the associated-graded transfer maps are injective on every adverse boundary class.

**Q3. Balanced circuit compiler.**  
Deterministically transform a size-\(S\) 3CNF into a fan-in-two NAND/COPY circuit of size \(O(S\log S)\) and depth

\[
d\ge \lfloor\log_2 S\rfloor-O(1),
\]

such that unsatisfiability forces a false output with an adverse chain of length \(d\). Emit every tile, glue equation, anchor, and target as ordinary Euclidean CVP coordinates.

**Q4. Quaternion energy lemma.**  
For \(0\ne x\in P^k\),

\[
\operatorname{Trd}(x\bar x)=2\operatorname{Nrd}(x)\ge 2\cdot17^k.
\]

Consequently, completeness has radius squared \(O(S\log S)\), while every NO vector has squared distance \(\Omega(17^d)\).

**Q5. Parameter lemma.**  
Arrange \(n\le S^4\) and polynomial bit complexity. Then

\[
\frac{d_{\rm NO}}{d_{\rm YES}}
 \ge S^{(\log_2 17-1)/2-o(1)}
 \ge n^{1/4}
\]

for sufficiently large \(S\); finitely many small inputs can be hard-coded. Thus \(c=1/4\).

**Why sufficient.** Q1–Q3 force an unsatisfied computation into depth \(d\); Q4 converts depth into Euclidean norm; Q5 gives the requested polynomial factor.

**Crux.** Q2: excluding grade-zero signed pseudosections at every NAND/COPY composition, not merely at one gate.

**First experiment.** Enumerate all saturated \(N\le8\) redundant COPY signature multisets over \(\mathbb F_{289}\). Glue each passing COPY to the known NAND survivor in both orientations. Compute all grade-zero and grade-one adverse fibers by exact finite-field elimination and SNF, rejecting any false boundary of valuation \(0\) or any depth-two defect whose valuation fails to increase.

---

## Strategy 2 — Möbius defects, unique-neighbor checks, and min-plus recursion

This route remains entirely commutative but eliminates local kernels before attempting amplification.

### Lemma chain

**M1. Polynomial-size Möbius-bag lemma.**  
Construct deterministic splitter bags involving \(O(\log S)\) Boolean variables. Give each bag all \(2^m\) squarefree moments. Its Boolean zeta matrix is unimodular, so each bag has no nonzero integral moment kernel.

**M2. Uniform sparse-defect localization lemma.**  
For every integral vector inside the recursively relevant shell, either it is an honest bag assignment or its Möbius-defect vector has support at most \(K=C\log S\). This statement must include negative coefficients and DROP.

**M3. Unique-neighbor/Graver composition lemma.**  
Attach an explicit lossless-expander check matrix \(H\) with unique neighbors for supports of size \(K\). For every primitive Graver move of the complete bag-gluing matrix, either the move is an honest global reassignment or \(H\Delta\ne0\). In particular, neither a Lawrence type-two move \((u,-u)\) nor a diagonal splice survives.

**M4. Strict transfer lemma.**  
Define complete legal/adverse min-plus tables for the binary recursive composition and prove, uniformly in depth,

\[
C_{\rm YES}(d)\le \mu^d C_0,\qquad
C_{\rm NO}(d)\ge \lambda^d C_0,\qquad
\lambda/\mu\ge65/64.
\]

All unrestricted integer states must occur in the tables.

**M5. Parameter lemma.**  
With depth \(d=\lfloor\log_2S\rfloor\) and \(n\le S^{20}\),

\[
d_{\rm NO}/d_{\rm YES}
 \ge (65/64)^{d/2}
 \ge n^{1/2000}.
\]

Thus \(c=1/2000\).

**Why sufficient.** M1–M3 give a theorem-level replacement for named-attack testing; M4 supplies genuine multiplicative growth; M5 converts it into a dimension gap.

**Crux.** M2: proving logarithmic defect support for unrestricted signed coefficients without weighting anchors so heavily that completeness destroys the ratio.

**First experiment.** On the Generation-38 twelve-bag instance, replace each bag by its full Möbius block. Use `4ti2` to compute the Graver basis for the smallest three-bag overlap cycle, then test whether every non-honest element in the \(B+64\) shell has \(O(\log S)\) defect support and a unique-neighbor check.

---

## Strategy 3 — Rank-\(\le43\) affine homogenization and E-type tensor recursion

Exploit Kitaoka’s theorem only after proving a valid affine-to-homogeneous bridge.

### Lemma chain

**T1. Constant-rank universal tile.**  
Construct inequivalent NAND and COPY CVP tiles of augmented rank at most \(43\), with common legal radius \(R\) and false-boundary distance at least

\[
\rho R,\qquad \rho=\sqrt{17/16}.
\]

The guarantee includes DROP and all signed fibers.

**T2. Exact homogenization lemma.**  
Convert each affine tile \((L,t)\) to an integral positive-definite augmented lattice \(\widehat L\) such that every relevant minimal vector has final coordinate \(\pm1\), corresponds to the intended target coset, and no zero-layer or multiple-layer vector is equally short.

**T3. Tensor-network compiler.**  
Compile a balanced NAND/COPY circuit of depth \(d=O(\log S)\) into a tensor recursion whose legal minimal vectors encode computations. Formula-dependent YES and NO seeds must not be coefficient/ambient isometric.

**T4. E-type soundness lemma.**  
Since each exposed factor has rank at most \(43\), Kitaoka’s E-type theorem forces every minimal tensor vector to be decomposable. Inductively,

\[
d_{\rm YES}\le R^d,\qquad d_{\rm NO}\ge(\rho R)^d,
\]

including arbitrary entangled coefficient tensors.

**T5. Parameter lemma.**  
If \(n\le43^{2d}\operatorname{poly}(S)\), then the ratio is at least \(n^{1/500}\).

**Why sufficient.** T2 translates CVP soundness into homogeneous shortest-vector soundness; T4 supplies the missing all-depth no-entanglement theorem.

**Crux.** T2, especially excluding zero-layer vectors without recreating DROP.

**First experiment.** For the rank-eight redundant NAND survivor and every \(N\le8\) COPY candidate, enumerate augmented-lattice vectors through \(\rho^2R^2\). Verify that all minima have final coordinate \(\pm1\), then enumerate the tensor square to detect zero-layer or entangled shortcuts.

---

## Complete obstruction audit

All three routes emit actual lattice coordinates, avoiding the **G6 externally filtered quotient**. None uses free slack or radix residuals, escaping **G1 RS slack** and **G7 radix kernel**. Q/T use saturated boundary modules and M uses unimodular Möbius/Graver checks, addressing **G2–3 local affine isolation** and **G5 private-row overlap**.

The **G9 degree-two parity**, **G11 unique-triple parity**, **G13 honest-affine-span collision**, **G15 laminar affine lift**, **G32 additive parity**, and **G37 universal parity cut** are escaped respectively by multiplicative valuation (Q), full Möbius plus unique neighbors (M), or homogeneous minimal-vector rigidity (T). DROP is explicitly quantified in Q1/M2/T1, addressing **G12 fingerprint DROP** and **Goal G8 augmented-Gram DROP**.

Unlike the finite-only **G14 pair bags**, **G31 Walsh Gram**, and **G38 splitter bags**, each route states an all-depth recurrence. M4 explicitly avoids **G28 \(\lambda\le\mu\)**. T3 requires nonisometric seeds, avoiding **G30 seed isometry**.

No route uses scalar Barrington flow, avoiding **G19 signed splicing** and **Goal G1 diagonal ordered-pair splice**. Q uses a quaternion division algebra, not the group ring killed by **Goal G2 \(A_5\) bicyclic zero divisors**. None re-enters the **G33–34 exterior completeness failure**, **Goal G3 D4 midpoint**, **Goal G4 D4 Boolean interaction**, **Goal G5 D4 recombination**, or **Goal G6–7 E6 affine-port** classes. Q starts from the redundant module rather than the canonical template killed by **Goal G11 \(\mathbb F_{289}\) grade-zero attack**; **Goal G12 redundant NAND** is treated only as a depth-one seed, with COPY and transfer left open.

## Recommendation

Attempt **Strategy 1** first. Its **FRONTIER lemma is Q2**, together with the missing COPY part of Q1.

**First experiment:** exhaustive \(N\le8\) saturated COPY search followed by exact grade-zero/grade-one enumeration of the two smallest NAND–COPY compositions over \(\mathbb F_{289}\), testing whether every adverse defect gains one \(P\)-adic valuation level.
