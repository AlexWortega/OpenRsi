I did not consult or use the prohibited document or related material. All proposals below are speculative and independently derived from the supplied campaign state.

### 1. Expander–Graver propagation

**Mechanism.** Clone variable occurrences onto an explicit lossless expander and replace private clause measurements by shared integral Tanner checks. Seek a theorem that every exact zero-residual, non-Boolean vector in the target fiber is a Graver move of squared norm \(N^{1+2c}\), while honest vectors cost \(\Theta(N)\).

**Expected move.** Deterministic 2-lifts for \(O(\log N)\) rounds would turn local selector defects into polynomially large anchor energy.

**Obstruction check.** G1: no slack. G2–3: globalizes rather than reusing local isolation. G5: no private rows. G6: every check is emitted. G7: zero kernels are allowed but must be long. G9/G11 parity, G12 drop, and G13 affine mixtures are directly in scope, not escaped. G14/G15 use different composition. G19: no flow. G28: no min-plus tile. G29: no products, carries, windows, or nonzero-syndrome assumption; its affine-lift warning remains fatal unless the norm grows.

**Falsification.** A bounded-coefficient affine mixture whose excess remains \(O(N)\) under lifts.

**Smallest experiment.** Expander-clone the nine-clause instance twice; use MILP/SVP to find the shortest exact kernel vector after each lift.

**Likely death.** The G13 mixture simply becomes dense with constant coefficient magnitude, giving only linear—not superlinear—energy.

---

### 2. Iterated Lawrence lifting of the selector configuration

**Mechanism.** Regard normalization, marginal, and legality columns as an integer configuration whose signed cheats are toric circuits. Apply higher Lawrence liftings, with targets coupling copies, hoping every harmful circuit’s Graver norm multiplies while legal one-hot witnesses grow only additively.

**Expected move.** \(O(\log N)\) lift depth with illegal/legal growth ratio \(>1\) would yield a polynomial distance ratio at polynomial rank.

**Obstruction check.** G1: no slack. G2–3/G5: replaces local overlap isolation by a global toric invariant. G6: full matrices and targets are explicit. G7, G9, G11, and G13 exact kernels are the objects being amplified, not assumed absent. G12 drops become unbalanced lift layers. G14/G15 affine lifting is directly relevant; no immunity is claimed. G19: not a transcript flow. G28: algebraic lifting, not frozen min-plus composition. G29’s fixed-degree-lift objection is avoided only if depth grows; its affine-pseudodistribution objection remains the central test.

**Falsification.** Lifted harmful and legal minima have the same asymptotic growth.

**Smallest experiment.** Form first and second Lawrence liftings of the 72-column G13 matrix; compute exact harmful/control minima with 4ti2 or branch-and-bound.

**Likely death.** New primitive circuits appear at each lift, or the honest baseline multiplies at least as fast as the harmful norm.

---

### 3. Literal tensoring of a deep-hole seed

**Mechanism.** Freeze a rational seed lattice \(B\mathbb Z^r\), target \(t\), matched control, and complete legal/adverse state classification. Test the literal construction \(B_k=B^{\otimes k}\), \(t_k=t^{\otimes k}\), aiming for multiplicative adverse distance but smaller legal growth; \(k=\Theta(\log N)\) keeps rank polynomial for constant \(r\).

**Expected move.** Prove \(d_{\rm NO}(k)/d_{\rm YES}(k)\ge \rho^k=N^c\) for some explicit \(\rho>1\).

**Obstruction check.** G1/G5/G6: no slack, private overlap, or external filters. G7, G9, G11, G12, G13, G15, and G19 attacks must all occur among unrestricted coefficient tensors. G2–3 and G14 provide possible seeds only, not composition proofs. G28 tested serial min-plus gluing, not Kronecker geometry. G29’s tensor objection applies exactly: non-rank-one integer tensors cannot be ignored, and no SDP attack list suffices. No products, carries, homology, or window flows are introduced.

**Falsification.** Any nondecomposable tensor with ratio no better than one copy.

**Smallest experiment.** Tensor the serialized G28 depth-one obstruction/control bases once; enumerate all coefficient matrices within the derived radius using Kronecker-Gram branch-and-bound.

**Likely death.** Entangled integer matrices beat every decomposable witness, destroying distance multiplicativity.

---

### 4. Twisted assignment sheaves on a cosystolic complex

**Mechanism.** Put local assignment labels in a sheaf over a 2-complex; restrictions enforce consistency, while forbidden clauses create a prescribed curvature cochain. If NO instances force a nontrivial integral or torsion cohomology class, a cosystolic lower bound could make every correction occupy polynomially many cells.

**Expected move.** Iterated explicit covers would grow the minimum representative while legal sections retain linear cost.

**Obstruction check.** G1: no slack. G2–3/G5: consistency is topological rather than private affine isolation. G6: boundary maps and target cochain must be emitted. G7 exact kernels become coboundaries. G9/G11 parity and G13/G15 affine mixtures remain cycles and are not automatically excluded. G12 drops become boundaries with support. G14 is not a pair mesh; G19 is not path flow; G28 is not min-plus recursion. G29’s homology objection applies directly: unsatisfiability must be proved to yield a nonzero class, and cosystolic expansion cannot merely be assumed. Other G29 product/carry/tensor objections are irrelevant.

**Falsification.** The target curvature is exact, torsion-free trivial, or has constant-support representative.

**Smallest experiment.** Put the eight three-variable sign clauses on the eight faces of the octahedron boundary; compute Smith forms and the minimum integral representative.

**Likely death.** Ordinary SAT inconsistency need not define any topological obstruction.

---

### 5. Intersecting mixed-radix carry fibers

**Mechanism.** Pack all Boolean variables into one integer \(X\), and extract each queried bit through several simultaneous radix systems—say bases \(2,3,5\)—sharing the same \(X\). An illegal local transcript should then require mutually incompatible carry chains, one of which grows geometrically in Euclidean norm.

**Expected move.** A common exact transcript exists for every Boolean assignment, while every accepting transcript for a NO instance has carry norm \(N^{1/2+c}\).

**Obstruction check.** G1: no free clause slack. G2–3/G5: no local private-marginal composition. G6: all quotient and carry variables are lattice coordinates. G7: unlike reordered copies of one residual, distinct valuations intersect—but an exact common kernel still kills it. G9/G11/G12: not moment or tag based. G13/G15 affine combinations of deterministic transcripts remain a direct threat. G14: no pair bags. G19: carries form a linear transcript and may splice. G28: no tile recursion. G29’s canonical-residue/carry objection applies; shared \(X\) and intersecting bases are the only new ingredient, not a proof. Rank-one, homology, tensor, and window proposals are not used.

**Falsification.** Any unrestricted zero-residual signed carry transcript.

**Smallest experiment.** Re-encode the nine-clause four-variable instance with shared \(X\) in bases 2 and 3; derive a coefficient bound and solve the exact fiber.

**Likely death.** Affine combinations of complete residue encodings satisfy every carry equation simultaneously.

---

### 6. Perfect-Delaunay clause amalgams

**Mechanism.** Search for a rational positive-definite form whose legal local truth patterns are vertices of one empty Delaunay ellipsoid, while forbidden and signed-selector states lie beyond a certified larger radius. Glue these cells along shared variable faces using Delaunay amalgamation, then seek a laminated product whose empty-sphere margin multiplies.

**Expected move.** Exact empty-ellipsoid certificates would replace finite attack separation; recursive lamination would provide the polynomial gap.

**Obstruction check.** G1: no slack. G2–3/G5: geometric face amalgamation replaces private measurements. G6: \(Q\), center, factorization, and enumeration bound are emitted. G7 exact kernels and G13 affine collisions may still be lattice points; they must lie outside the ellipsoid. G9/G11/G12 used fixed moment/tag forms and exposed parity/drop attacks; this searches the full rational form with all-point certification. G14/G15 provide comparison lifts, not a Delaunay theorem. G19: no flow. G28: not min-plus, though its bad growth warns against lamination. G29’s finite-SDP objection is avoided only by exact enumeration of every lattice point; its missing-composition objection remains. No rank-one, carry, homology, or code assumption appears.

**Falsification.** G13 lies inside the sphere, or amalgamation makes radii add rather than multiply.

**Smallest experiment.** SDP-search \(Q,c\) on the nine-clause/control pair, rationally reconstruct it, then exactly enumerate the certified coefficient box and one two-cell amalgam.

**Likely death.** Convexity favors an affine signed combination, and Euclidean free sums yield only constant ratios.

Classical mechanism pointers only: Sipser–Spielman on expander codes; Sturmfels on toric ideals and Lawrence configurations; standard Smith-normal-form/cohomology methods; and classical Delaunay/Voronoi theory.
