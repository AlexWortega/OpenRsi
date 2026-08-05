Below are six independent attacks on the fixed Voronoi-coercive frontier. None reuses the killed separable \(D_4\), flow, tensor, Walsh-composition, or group-ring mechanisms unchanged.

1. **Nonseparable \(D_4\) cycle mixing**

**Core.** Freeze the first surviving non-antipodal labeling and replace \(K\otimes I_4\) by off-diagonal blocks  
\[
Q_{AB}=-I/4+uP,\quad Q_{AC}=-7I/16+vP,\quad Q_{BC}=7I/16+wP,
\]
where \(P\) is a 4-cycle and \(u,v,w\in\{-2,-1,0,1,2\}/16\). Cross-coordinate mixing destroys the exact two-hybrid identity that killed Generation 5.

**Expected move.** Find an empty four-point NAND Delaunay shell, then seek COPY and an exact depth-two ratio \(\lambda/\mu\ge65/64\).

**Smallest experiment/falsifier.** Test all 125 Grams: exact PD, rational circumcenter, then enumerate every \((2D_4^*)^3\) point inside the legal radius using rational LDL bounds. Any intruder kills the candidate.

**Audit.** G1 charges every coefficient; G2/G3 exact LDL bounds all \(\mathbb Z^{12}\); G5 glues complete ports; G6 emits all rows. G7/G9/G11/G12/G13/G15/G19 are not escaped: enumeration includes them. G14/G31/G38 avoid shell extrapolation via the global bound. G28 is the \(\lambda>\mu\) test; G30 no tensor; G32/G37 parity remains in the table; G33/G34 no exterior repair; GD1 no ordered-pair lift; GD2 no group ring.

**Likely death.** A new two-point exchange intruder survives arbitrary cycle mixing.

---

2. **Construction-A deep-hole gate**

**Core.** Use one nonproduct Construction-A lattice \(L_C=\{x\in\mathbb Z^r:x\bmod2\in C\}\), with coordinates jointly spanning all three ports. Choose a deep-hole target whose nearest vectors project exactly to the four legal NAND words; code coset weight enumerators then certify the entire Euclidean shell.

**Expected move.** Let the finite syndrome be \(K\); prove closure by syndrome DP and obtain the next-coset minimum at least \(65/64\) times legal energy. Build COPY from a separate target in the same lattice family.

**Smallest experiment/falsifier.** Enumerate systematic binary \([9,4]\) codes, partitioned into three 3-bit ports, all target cosets, and all port labelings. Exact coordinate rounding plus coset-leader DP tests NAND, COPY, and depth two. A closer nonlegal codeword falsifies.

**Audit.** G1 all coordinates charged; G2/G3 coset DP covers all integers; G5 complete 3-bit ports; G6 no filters. G7/G9/G11/G12/G13/G15/G19 are not escaped—test their syndromes explicitly. G14/G31/G38 use exact coset minima, not sampled shells. G28 remains mandatory; G30 no tensor; G32/G37 compatible parity remains possible; G33/G34 no bivectors; GD1 no pair lift; GD2 no group-ring multiplication.

**Likely death.** Honest affine combinations occupy the same syndrome, reproducing G13 inside the deep-hole shell.

---

3. **Cographic cut-lattice tile**

**Core.** Encode ports as terminal cuts of a small weighted graph and use its integral cut lattice, whose Voronoi competitors admit exact cut/cycle certificates. Internal selector coefficients are edge coordinates; malformed signed states are controlled globally by minimum-cut inequalities rather than bounded enumeration.

**Expected move.** Realize legal NAND and COPY states as equal-weight terminal orientations while every adverse boundary state crosses an additional cut. Boundary cut signatures form the finite transfer codebook \(K\).

**Smallest experiment/falsifier.** Enumerate connected multigraphs on at most six vertices, three terminal pairs, edge weights \(1,2,3\), and terminal truth orientations. Compute exact Delaunay cells and depth-two min-plus tables by exhaustive cuts plus integer Laplacian reduction. A basis-exchange orientation of no greater weight kills it.

**Audit.** G1 edges are charged; G2/G3 cut certificates quantify over the full lattice; G5 uses complete terminal boundaries; G6 all conservation rows are emitted. G7/G9/G11/G12/G13/G15/G19 remain inside the signed cut domain—G19 is not excluded as “nonflow.” G14/G31/G38 rely on cut theorems, not shells. G28 is tested directly; G30 no tensor; G32/G37 parity is audited; G33/G34 no exterior metric; GD1 no ordered-pair lift; GD2 no group ring.

**Likely death.** Graphic basis exchange creates an equal-or-cheaper malformed orientation.

---

4. **Inverse Delaunay synthesis by secondary cones**

**Core.** Do not inherit a named lattice: choose primitive integer locations for legal states, then solve the inverse empty-ellipsoid problem for \(Q\succ0\) and center \(c\). A Cayley lift places truth states in distinct affine slices, eliminating integral midpoints while secondary-cone inequalities synthesize nonseparable interactions.

**Expected move.** Produce a rational Gram with legal NAND/COPY configurations as exact Delaunay vertices, then use adversarial column generation to enforce \(\lambda/\mu\ge65/64\).

**Smallest experiment/falsifier.** In coefficient dimension six, enumerate primitive legal points in \(\{-1,0,1\}^6\). Alternate exact LP over \((Q,c)\) with an exact CVP oracle returning the nearest violating integer point; terminate only with a rational eigenvalue bound and complete integer certificate.

**Audit.** G1 puts every slice coordinate in the norm; G2/G3 the final CVP certificate covers all \(\mathbb Z^6\); G5 full ports; G6 no external constraints. G7/G9/G11/G12/G13/G15/G19 are oracle competitors, not excluded. G14/G31/G38 column generation is insufficient until the global bound closes. G28 is an explicit inequality; G30 no tensor; G32/G37 parity receives generated cuts; G33/G34 no fixed bivectors or repair; GD1 no pair lift; GD2 no group ring.

**Likely death.** NAND’s prescribed vertices lie in no positive-definite secondary cone once all primitive competitors are added.

---

5. **Discriminant-form gluing over \(A_2\)**

**Core.** Glue several \(A_2\) blocks through a ternary code in the discriminant group \(A_2^*/A_2\cong\mathbb Z/3\). A coordinate splice that was harmless in \(D_4\) changes the global discriminant syndrome, and its minimum Euclidean penalty is certified by exact coset theta minima.

**Expected move.** Put all legal gate states in equal-minimum glue cosets, with FALSE, DROP, signed, and malformed states in cosets whose minima grow by at least \(65/64\). Use discriminant syndromes as the closed finite codebook.

**Smallest experiment/falsifier.** Enumerate ternary self-orthogonal codes of length at most six, assign two \(A_2\) blocks per port, and compute every coset minimum by two-dimensional nearest-point DP. Test NAND, COPY, and depth-two syndrome convolution exactly.

**Audit.** G1 all glue coordinates charged; G2/G3 syndrome DP covers complete integral fibers; G5 glues full discriminant ports; G6 emits normalization and glue rows. G7/G9/G11/G12/G13/G15/G19 are not escaped—test their cosets. G14/G31/G38 use exact theta minima. G28 is the required ratio; G30 no tensor; G32/G37 additive parity may still close and must be tested; G33/G34 no exterior tags; GD1 no ordered pairs; GD2 uses no group-ring products or units.

**Likely death.** The legal glue subgroup also contains an affine parity or DROP coset with the same minimum.

---

6. **Tropical exchange obstruction—or seed**

**Core.** Eliminate tile auxiliaries and regard the transfer cost as the lower envelope of integer translates of one positive quadratic. Attempt to prove a tropical four-point or discrete-midpoint inequality forcing either a false NAND state below the legal shell or \(\lambda\le\mu\); a counterexample to the inequality becomes a candidate nonclassical tile seed.

**Expected move.** A universal inequality would refute the FRONTIER as stated. A proof limited to obtuse-superbase, \(M\)-matrix, or totally unimodular tiles only justifies pruning that roadmap branch, not changing the lemma.

**Smallest experiment/falsifier.** Enumerate rank-\(\le4\) integral port maps and small rational PD Grams, compute all eight Boolean transfer values exactly, and test tropical Plücker/exchange inequalities. Record the smallest violating Gram and run its unrestricted shell.

**Audit.** G1/G5/G6 must be theorem hypotheses. G2/G3 require minimization over full integral fibers. G7/G9/G11/G12/G13/G15/G19 are witnesses, not excluded. G14/G31/G38 demand a symbolic theorem, not finite evidence. G28 is the intended conclusion; G30 irrelevant. G32/G37 are the central additivity stress tests. G33/G34 are covered only if arbitrary PD Grams are proved; otherwise no frontier amendment. GD1/GD2 are outside the proposed derivation.

**Likely death.** Arbitrary non-\(M\)-matrix Grams violate discrete convexity, leaving only a narrow-family impossibility theorem.

**Classical background:** Conway–Sloane, *Sphere Packings, Lattices and Groups* (1999), for Construction A and lattice holes; Gelʹfand–Kapranov–Zelevinsky, *Discriminants, Resultants, and Multidimensional Determinants* (1994), for secondary polytopes; Bacher–de la Harpe–Nagnibeda (1997), for integral flow/cut lattices; Murota, *Discrete Convex Analysis* (2003), for exchange inequalities.
