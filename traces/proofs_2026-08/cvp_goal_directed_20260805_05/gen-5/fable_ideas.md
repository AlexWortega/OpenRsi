Below are six unranked mechanisms. None reuses the killed common-coupling \(D_4\) grid unchanged.

### 1. Independent-coupling \(D_4\) completion

**Mechanism.** Replace the rejected common-magnitude Gram by  
\[
Q=K(x,y,z)\otimes I_4,
\]
with three independent rational port couplings. The Boolean excess system permits strict separation—for example \(A=1,B=C=2\)—so the Generation-4 identity is not itself a no-go theorem.

**Expected move.** Find an equal-radius NAND/COPY shell, certify global emptiness, then compute exact depth-two transfer with \(\lambda/\mu\ge65/64\).

**Experiment.** Reuse all 663,552 non-antipodal labelings; enumerate \(x,y,z\in\{-7,\ldots,7\}/16\), exact-PD filter, retain only four-positive-excess signatures, solve centers, and enumerate all relevant vectors of \((2D_4^*)^3\).

**Falsification.** No positive Boolean signature, or any nonlegal lattice point enters the shell.

**Audit.** G1: all coordinates charged; G2/G3: relevant vectors cover all \(\mathbb Z^D\); G5: full ports; G6: no filters; G7: kernels retained; G9/G11/G12/G13/G15/G19: explicit adverse classes; G14/G31/G38: no shell extrapolation; G28: transfer ratio computed; G30: no tensor; G32/G37: no additivity assumption; G33/G34: no exterior tags; GD1: no ordered-pair lift; GD2: no group ring.

---

### 2. Construction-A coset-shell tile

**Mechanism.** Use a small \(q\)-ary code to construct a lattice whose truth symbols are distinct equal-norm coset leaders. Legal NAND triples need not share one syndrome: they occupy different cosets equidistant from a target, while syndrome-decoding distance separates false and malformed triples.

**Expected move.** Make the syndrome alphabet the closed port codebook \(K\); exact coset minima then certify unrestricted transfer entries and potentially \(\lambda/\mu\ge65/64\).

**Experiment.** Enumerate systematic ternary \([6,3]\) codes, Boolean-to-coset maps, and rational centers in dimension \(18\). Compute every coset minimum exactly, retain equal-legal-radius NAND/COPY candidates, and compose two levels.

**Falsification.** An affine combination of legal coset leaders is a false leader of no greater norm—the likely G13-style death.

**Audit.** G1: no free carries; G2/G3: complete coset decoding covers \(\mathbb Z^D\); G5: whole syndromes glued; G6: no external congruence filter; G7: zero syndromes audited; G13: no common-hash premise; G9/G11/G12/G15/G19: searched unrestrictedly; G14/G31/G38: decoding theorem, not finite-shell inference; G28/G32/G37: exact depth-two growth required; G30: no tensor; G33/G34: no exterior metric; GD1: no pair lift; GD2: no convolution.

---

### 3. Obtuse-superbase / graph-cut lattice

**Mechanism.** Build the tile in a lattice of Voronoi’s first kind, where an obtuse superbase turns relevant vectors into graph cuts. Encode port truths by terminal sides of cuts and choose edge weights plus target potentials so the four legal NAND cuts tie while every false cut is more expensive.

**Expected move.** The cut characterization supplies a structural unrestricted certificate, while nonorthogonal shared edges may make compatible adverse states grow superlinearly.

**Experiment.** On \(K_6\) with three terminals and three auxiliaries, solve exact LPs over positive integer edge weights \(1\!:\!8\) and rational target potentials. Enumerate all \(2^3\) auxiliary cuts per port word, then construct COPY and the depth-two transfer table.

**Falsification.** Cut submodularity forces a false NAND cut to tie or beat the legal cuts.

**Audit.** G1: every edge direction is charged; G2/G3: all integer vectors handled by the cut/relevant-vector certificate; G5: terminal and auxiliary ports glued completely; G6: no filters; G7: graph-lattice kernels included; G9/G11/G12/G13/G15/G19: unrestricted cuts include their projections; G14/G31/G38: structural certificate; G28: exact growth test; G30: no tensor; G32/G37: shared edges, not additive copies; G33/G34: no exterior tags; GD1/GD2: neither flows nor group rings.

---

### 4. Additive ideal-lattice residue tile

**Mechanism.** Take the Minkowski/trace lattice of a small number field and label ports by residue classes modulo an ideal. Choose a rational trace form and deep-hole target so legal residue triples have equal minima, while false residues must enter a larger ideal-norm shell; only additive ideal geometry is used.

**Expected move.** Ideal-coset minimum bounds could provide the exact outside-shell certificate, with residue classes giving finite transfer closure.

**Experiment.** Start with \(\mathbb Q(\sqrt5)\), ideals above \(2,3,5\) of norm at most \(25\), and all two-symbol residue labelings. Enumerate exact coset minima in the three-port product, then test NAND/COPY and depth two.

**Falsification.** Units or short elements make all useful residue classes isometric, or a signed affine combination lands in a cheap false class.

**Audit.** G1: all embeddings charged; G2/G3: ideal-CVP enumeration covers the full module; G5: full residue ports; G6: congruences are emitted lattice coordinates; G7: ideal kernels audited; G9/G11/G12/G13/G15/G19: included as integral elements; G14/G31/G38: ideal bounds replace extrapolation; G28/G32/G37: exact transfer required; G30: no tensor; G33/G34: no bivectors; GD1: no ordered pairs; GD2: no group ring or multiplicative convolution.

---

### 5. Free-Gram counterexample-guided tile synthesis

**Mechanism.** Co-design integer representatives, auxiliary coordinates, center, and a fully free rational positive-definite Gram matrix. Alternate exact SDP feasibility with a CVP separation oracle: every newly discovered malformed integer point becomes a permanent strict inequality.

**Expected move.** Auxiliary coordinates can destroy the Boolean-cube midpoint identities; termination with a covering bound gives the FRONTIER certificate directly, followed by exact transfer optimization.

**Experiment.** Use \(D=12\): three visible port bits, four legal-state coordinates, and five auxiliaries in \(\{-1,0,1\}\). Search NAND first with margin \(1/64\), rationally reconstruct \(Q,c\), enumerate the complete ellipsoid, then add COPY and depth two.

**Falsification.** The cutting-plane system becomes exactly infeasible, or margins converge to zero through infinitely recurring short affine intruders.

**Audit.** G1: auxiliaries lie in the charged Gram; G2/G3: promotion requires a covering bound over all \(\mathbb Z^{12}\); G5: complete visible/auxiliary ports; G6: no filtered constraints; G7/G9/G11/G12/G13/G15/G19: oracle searches them automatically; G14/G31/G38: no bounded-pass promotion; G28: explicit transfer inequality; G30: no tensor; G32/G37: unrestricted coupled Gram; G33/G34: representatives and Gram are co-designed, unlike the frozen exterior family; GD1/GD2: absent.

---

### 6. Toric integer-convexity refutation

**Mechanism.** Try to refute the FRONTIER in a broad equality-glued normal form. Compute the toric ideal of legal NAND/COPY representatives; if it forces an adverse integer representative to be a proper convex average of equal-radius legal representatives, strict convexity places that adverse point inside every positive-definite shell.

**Expected move.** Either prove a general midpoint/parallelogram obstruction extending Generations 3–4, or identify the exact auxiliary-coordinate condition any viable roadmap amendment must violate.

**Experiment.** SAT-enumerate port-complete embeddings in dimensions \(1\!:\!6\) with coordinates in \(\{-1,0,1\}\). Use Hilbert-basis computation to find short nonnegative legal relations and verify each intrusion symbolically for arbitrary \(Q\succ0\).

**Falsification.** One embedding has no adverse integral convex relation; bounded enumeration alone cannot refute the lemma.

**Audit.** G1/G5/G6: normal form includes every charged coordinate and glue row; G2/G3: only a symbolic toric theorem would cover unbounded fibers—finite SAT does not; G7/G9/G11/G12/G13/G15/G19: candidate relations explicitly include these attacks; G14/G31/G38: no promotion from the bounded test; G28: an intrusion already forces failed growth; G30/G32/G37: no tensor/additivity premise; G33/G34: arbitrary PD Gram, not exterior tags; GD1/GD2: no pair lift or group ring.

Classical background only: Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (Construction A and Voronoi geometry), and Cohen, *A Course in Computational Algebraic Number Theory* (ideal lattices and exact enumeration).
