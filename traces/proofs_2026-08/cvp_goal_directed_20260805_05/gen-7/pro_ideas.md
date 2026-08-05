The current E6 result certifies a useful empty shell but kills only bounded affine port maps. The following mechanisms do not reuse the retired \(D_4\), ordered-pair, or \(A_5\) constructions unchanged.

### 1. Coefficient-unbounded affine classification of the E6 shell

**Mechanism.** Since the 27 Gosset vertices affinely span \(\mathbb Q^6\), any rational affine row that is binary-valued on them is determined by its values on seven affine-basis vertices. Enumerating those \(2^7\) assignments classifies all rational affine port rows without a coefficient bound.

**Frontier move.** Either produce a genuine NAND map, or refute the entire affine-port E6 branch and justify restricting the roadmap to redundant/nonlinear ports.

**Falsification.** A surviving row triple realizes all four NAND words.

**Smallest experiment.** Extend the E6 verifier: certify affine rank six, solve the 128 exact rational systems, test all 27 vertices, then enumerate row triples and all 32 translated/relabelled NAND relations.

**Obstruction audit.** G2 affine isolation/G3 unbounded fibers are handled exactly. G14 finite bags/G31 finite Walsh/G38 finite splitters are avoided because this is a complete classification. G33/G34 are outside scope: the fixed E6 metric has no exterior tags. G1, G5–G13, G15, G19, G28, G30, G32, G37, GD1, and GD2 are honestly not addressed: the test stops before gluing or transfer.

**Likely death.** It proves only a no-go theorem for affine E6 ports.

---

### 2. E6 shell with redundant one-hot incidence ports

**Mechanism.** Introduce 27 charged selector coordinates \(s_v\), couple \(x=\sum_v s_vv\) to the certified E6 shell, and color each \(v\) by a legal NAND word. Ports are emitted class sums, while a simplex Gram penalizes every signed non-one-hot representation; thus labeling need not arise from a three-row projection.

**Frontier move.** Obtain an arbitrary legal shell classification plus an exact all-integer selector barrier, then test COPY and \(\lambda/\mu\).

**Falsification.** A signed \(s\) with malformed class sums lies on or inside the legal sphere, or depth two has \(\lambda\le\mu\).

**Smallest experiment.** Search four-colorings modulo the E6 Weyl action and two rational weights for the E6/simplex blocks; enumerate exact depth-one and depth-two minima.

**Obstruction audit.** G1 slack/G6 filters: every selector and glue coordinate is charged. G2/G3: require an exact simplex–E6 all-\(\mathbb Z\) certificate. G5: glue complete class sums. G7, G9/G11, G12, G13, G15, G19 are unrestricted signed states. G14/G31/G38: use an outside-shell theorem, not extrapolation. G28 is tested directly. G30, G33/G34, GD1/GD2 are unused. G32/G37 remain threats; depth two is mandatory.

**Likely death.** An affine collision among color classes defeats the simplex surcharge.

---

### 3. Secondary-cone synthesis with a separation oracle

**Mechanism.** Do not start from a named root lattice. Choose integral representatives for the four legal NAND states and solve jointly for \(Q\succ0\), center \(c\), and an integral port map; equal-radius and exclusion constraints are linear in the lifted variables \((Q,Qc,r)\). A shortest-vector oracle adds any omitted interior lattice point as a cut.

**Frontier move.** Produce a rational Delaunay tile with an exact terminating certificate, or a Farkas certificate excluding a whole bounded-coordinate combinatorial type.

**Falsification.** Every feasible Gram acquires an interior malformed point, or COPY and NAND cannot share a gluable port geometry.

**Smallest experiment.** Enumerate HNF-normalized legal representatives in \([-2,2]^5\); run exact rational cutting-plane LP with \(Q\succeq I/64\), then construct transfer tables for survivors.

**Obstruction audit.** G1/G6: no slack or filters. G2/G3: the separation oracle ranges over all integers using the eigenvalue bound. G5: full port fibers are optimized. G7, G9/G11, G12, G13, G15, G19 enter as cuts. G14/G31/G38: no finite-shell inference. G28: optimize \(\lambda/\mu\) explicitly. G30, GD1, GD2 are absent. G33/G34 are outside their frozen exterior family. G32/G37 require depth-two cuts.

**Likely death.** A general quadratic identity forces a false Boolean fiber inside every equal-radius NAND sphere.

---

### 4. Voronoi-first-kind graph-cut tile

**Mechanism.** Restrict to lattices with an obtuse superbasis, whose relevant vectors are subset sums and whose closest-point problem has a min-cut certificate. Represent port truths by terminal sides of a weighted graph cut; hidden vertices implement minimization, potentially realizing NAND as a projected submodular relation.

**Frontier move.** Replace Fincke–Pohst shell enumeration by a uniform min-cut proof over every integer coefficient, while searching graph weights for strict adverse growth.

**Falsification.** NAND is not representable by the permitted projected cut functions, or composition remains additive.

**Smallest experiment.** Enumerate graphs with three terminals and at most three hidden vertices, terminal flips, and weights in \(\{1,\ldots,8\}\); compute exact NAND/COPY transfer tables and depth-two ratios.

**Obstruction audit.** G1/G6: hidden vertices and rank constraints are emitted and charged. G2/G3: the obtuse-superbasis theorem covers all integers. G5: all terminal cuts are glued. G7, G9/G11, G12, G13, G15, G19 are included in the unrestricted min-cut optimization. G14/G31/G38: certificate is structural. G28 is the direct ratio test. G30, G33/G34, GD1/GD2 are unused. G32/G37 are not automatically escaped: graph energies can be additive, so strict depth-two growth is essential.

**Likely death.** Submodularity or a delta-matroid identity forbids the exact NAND relation.

---

### 5. Completely regular code / Construction-A coset tile

**Mechanism.** Use a small completely regular code whose cosets have exactly known Euclidean leader weights. Ports are syndrome classes, and tile composition is finite min-plus convolution on the coset graph; canonical representatives are enforced using emitted, charged quotient carries rather than external modular filtering.

**Frontier move.** Assign legal NAND states to equal-weight cosets while every false or malformed syndrome has leader weight at least \(65/64\) larger, obtaining an algebraic outside-shell certificate.

**Falsification.** A zero-syndrome affine parity or cheap \(q\mathbb Z\) carry realizes an adverse port.

**Smallest experiment.** Enumerate binary parity-check matrices of length at most eight, all assignments of eight truth triples to syndromes, and exact one/depth-two coset-leader tables; start with the \([7,4,3]\) Hamming code and products.

**Obstruction audit.** G1/G6: quotient carries must be emitted and charged. G2/G3: complete syndrome decoding covers all integers. G5: glue full syndromes. G7, G9/G11, G12, G15, G19 are decoded states. G13 and G32/G37 are direct unresolved threats: test exact zero-syndrome affine/parity combinations first. G14/G31/G38: no shell extrapolation. G28 is explicit convolution growth. G30, G33/G34, GD1/GD2 are absent.

**Likely death.** Linearity recreates G13 or compatible additive parity in the zero-syndrome fiber.

---

### 6. Valuated-matroid / M-convex gate

**Mechanism.** Encode a truth symbol by an occupancy pattern and seek a regular matroid or gammoid whose bases project exactly to legal NAND triples. A separable quadratic centered on occupancies makes bases equicost; M-convex exchange and generalized-polymatroid intersection would certify unrestricted minima and closure under gluing.

**Frontier move.** Derive the tile transfer theorem from exchange axioms rather than lattice-shell enumeration, with malformed integer occupancies paying a provable exchange distance.

**Falsification.** NAND is excluded by matroid projection identities, or a signed nonbase has no larger energy.

**Smallest experiment.** Enumerate graphic/cographic matroids on at most seven elements, port partitions, deletions, and contractions; test projected NAND/COPY relations and exact depth-two separable-convex minima.

**Obstruction audit.** G1/G6: rank, occupancy, and auxiliary conditions are emitted. G2/G3: M-convex exchange quantifies over the full integer domain. G5: glue complete port occupancies. G7, G9/G11, G12, G13, G15, G19 become nonbase integer points. G14/G31/G38: use an exchange theorem, not finite extrapolation. G28 remains the required ratio calculation. G30, G33/G34, GD1/GD2 are unused. G32/G37 may survive through additive bases and must be tested at depth two.

**Likely death.** Projected matroid relations satisfy an exchange or matchgate identity violated by NAND.

---

### 7. Oriented-matroid circuit no-go theorem

**Mechanism.** Attack the frontier negatively: classify integer affine circuits among equal-radius legal representatives. For any circuit with compatible signs, the quadratic parallelogram identity may construct an integral malformed point whose average energy is at most the legal radius, generalizing the midpoint and coordinate-recombination attacks.

**Frontier move.** Refute all primitive linear-port Delaunay NAND tiles up to a structural hypothesis, forcing a justified roadmap amendment to redundant or nonlinear ports.

**Falsification.** A circuit-free simplex realization with primitive ports and strict false-state separation.

**Smallest experiment.** Enumerate HNF representatives in dimensions \(3\)–\(6\), primitive port maps via SNF, and legal preimages of norm at most three; output exact signed-circuit intruder certificates or the first survivor.

**Obstruction audit.** G2/G3 are addressed by HNF/SNF classification within the declared class; G14/G31/G38 permit no extrapolation beyond that class. G33/G34 are irrelevant unless exterior tags are admitted. G1, G5–G13, G15, G19, G28, G30, G32, G37, GD1, and GD2 are honestly not solved: this is a pre-transfer impossibility theorem, not a construction. It nevertheless subsumes the specific midpoint mechanism behind the tested \(D_4\) failures without assuming separability.

**Likely death.** Legal microstates can be chosen affinely independent, making the circuit hypothesis too weak to touch the full frontier.

Classical ingredients invoked: Voronoi reduction/secondary cones; Conway–Sloane’s treatment of Construction A; Murota’s *Discrete Convex Analysis*; Schrijver’s treatments of submodularity and regular matroids; and Björner–Las Vergnas–Sturmfels–White–Ziegler’s *Oriented Matroids*.
