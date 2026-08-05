## 1. Nonseparable \(D_4\) cross-coordinate Gram

**Mechanism.** Break the fatal coordinate-recombination identity by adding genuinely nonseparable \(4\times4\) cross-coordinate blocks. Use the frozen signature \((-8,-8,8)\), but set \(AB=-I/4+uP\), \(AC=-7I/16+vP\), \(BC=7I/16+wP\), where \(P\) is a 4-cycle and \(u,v,w\in\{-2,\ldots,2\}/16\).

**Expected move.** Obtain an exactly empty equal-radius NAND shell; then construct COPY and test the complete depth-two operator for \(\lambda/\mu\ge65/64\).

**Smallest experiment.** Check all 125 Grams for exact positive-definiteness and circumcenter feasibility, then enumerate every point of \((2D_4^*)^3\) up to the legal radius by rational LDL branch-and-bound with a proved coefficient bound.

**Falsification/death.** Any intruder shell point; most likely a new two-coordinate hybrid replaces the old separable hybrid.

**Obstruction audit.** G1: no slack; all coordinates charged. G2/G3: LDL covers all \(\mathbb Z^{12}\). G5: complete ports. G6: no filters. G7: kernels retain positive Gram energy. G9/G11, G12, G13, G15, G19: explicitly enumerated. G14/G31/G38: global certificate, not shell extrapolation. G28: transfer ratio tested directly. G30: no tensor. G32/G37: no additive copies. G33/G34: no exterior tags. GD1/GD2: no ordered-pair lift or group ring.

---

## 2. Voronoi-first-kind tile certified by graph cuts

**Mechanism.** Restrict to lattices with an obtuse superbase, whose Voronoi-relevant vectors are superbase subset sums and whose CVP minimization reduces to an exact weighted cut problem. Encode port symbols by selected cuts; then equal legal cost and adverse separation become rational inequalities in graph-edge weights.

**Expected move.** A symbolic min-cut lower bound would certify every outside-codebook integer vector and could prove \(\lambda>\mu\) without Fincke–Pohst extrapolation.

**Smallest experiment.** Enumerate weighted graphs on six superbase vertices with weights \(1,\ldots,4\), all two-label port cut assignments, and rational centers; solve equal-radius NAND/COPY constraints and compute complete transfer tables by exhaustive cuts.

**Falsification/death.** Submodularity likely forces one false NAND assignment or DROP cut no more expensive than the legal shell.

**Obstruction audit.** G1: no slack. G2/G3: min-cut theorem covers the full lattice. G5: glue entire cut ports. G6: all cut conditions emitted. G7: zero-cut kernels still pay positive edge energy. G9/G11/G12/G13/G15/G19: included as arbitrary cuts, not excluded assumptions. G14/G31/G38: symbolic cut bound, not finite extrapolation. G28: computes \(\lambda/\mu\) exactly. G30, G32/G37: no tensors or copy-additivity. G33/G34: no bivectors. GD1/GD2: no flows or convolution.

---

## 3. Mine an irreducible perfect Delaunay polytope

**Mechanism.** Use an already-empty irreducible Delaunay polytope—first the 27-vertex \(E_6\) Gosset polytope—rather than engineering a product shell. Search for integral port projections whose fibers place exactly the four legal NAND configurations on its circumsphere; irreducibility removes the coordinate-splicing identity.

**Expected move.** Emptiness comes from the Delaunay certificate itself; orbit reduction can then give a finite closed transfer codebook and exact outside-shell bound.

**Smallest experiment.** Enumerate small integral maps \(E_6\to\mathbb Z^3\) with entries in \(\{-1,0,1\}\), classify the 27 vertices by port image, and test whether the legal NAND fibers—and separately COPY fibers—are nonempty while all false fibers miss the shell.

**Falsification/death.** Most likely no integral projection realizes the required truth fibers, or COPY introduces an unavoidable shell vertex.

**Obstruction audit.** G1: no auxiliaries. G2/G3: the Delaunay facet certificate is global. G5: project and glue complete ports. G6: no filters. G7: lattice kernels remain inside the certified shell analysis. G9/G11/G12/G13/G15/G19: every vertex/fiber and outside point is covered. G14/G31/G38: no finite-shell inference. G28: orbit transfer still must prove strict growth. G30, G32/G37: no tensor/additive composition. G33/G34: not exterior-tag synthesis. GD1/GD2: unrelated.

---

## 4. Construction-A coset-leader gate with nonlinear port embedding

**Mechanism.** Embed each Boolean symbol into a nonlinear constant-weight block \(\phi(0),\phi(1)\), then use a small \(q\)-ary Construction-A lattice so each port configuration selects a syndrome whose exact coset-leader norm is its gate energy. Seek four legal NAND syndromes with equal leader norm and every false, DROP, or malformed syndrome with norm at least \(65/64\) larger.

**Expected move.** Finite syndrome closure gives the complete min-plus state space, while reduction modulo \(q\) plus a code-distance certificate handles every integer vector.

**Smallest experiment.** For \(q=3\), lengths \(8\)–\(12\), enumerate rank-\(\le4\) parity checks and constant-weight embeddings; compute every coset leader exactly and test NAND/COPY plus depth-two composition.

**Falsification/death.** G13 may reappear: an affine parity witness could occupy the same syndrome as a legal state, or code distance may also inflate honest cost.

**Obstruction audit.** G1: no free slack. G2/G3: all residue classes and lattice translates are certified. G5/G6: full ports and checks are emitted. G7: zero syndrome still pays coset-leader norm. G9/G11/G12/G15/G19: explicitly tested syndromes. G13: not escaped by assertion—the nonlinear enlargement is the proposed escape, and collision is a falsifier. G14/G31/G38: exhaustive syndrome theorem, not bounded-shell extrapolation. G28: direct transfer ratio. G30, G32/G37, G33/G34, GD1/GD2: no tensor, additive copies, bivectors, pair flows, or group rings.

---

## 5. Folded modular Voronoi “sawtooth” gate

**Mechanism.** Build gate energy from charged nearest-multiple terms
\[
\sum_j\min_{k_j\in\mathbb Z}(a_jx+b_jy+c_jz+q_jk_j-t_j)^2+\varepsilon\|k\|^2.
\]
Minimizing over carries creates a periodic, piecewise-quadratic truth-table energy although the emitted lattice remains Euclidean and linear.

**Expected move.** Find two or three folded forms making all legal NAND words equal-cost and every adverse residue strictly larger; residues provide a finite transfer codebook.

**Smallest experiment.** Exhaust \(q_j\le11\), coefficients \(|a_j|,|b_j|,|c_j|\le q_j\), one or two carries, and rational \(\varepsilon\); use exact branch-and-bound over unrestricted ports and carries.

**Falsification/death.** Most likely charged carries destroy equal completeness, while uncharged carries recreate G1/G7; G13 is also a genuine live threat.

**Obstruction audit.** G1: every carry has an anchor. G2/G3: residue reduction plus coercive bounds covers all integers. G5/G6: full ports, carries, and normalization are emitted. G7: exact kernels pay anchor energy. G9/G11/G12/G13/G15/G19: not assumed away; all appear in unrestricted residue minimization. G14/G31/G38: global periodic proof required. G28: complete residue transfer tests \(\lambda/\mu\). G30, G32/G37: no tensor/additive-copy argument. G33/G34: no exterior metric. GD1/GD2: no flow or group algebra.

---

## 6. Redundant orbit-valued truth ports

**Mechanism.** Represent each truth value by an entire symmetry orbit \(K_0,K_1\), rather than one lattice point. Arrange the legal NAND shell as a union of orbits so midpoint or hybrid points are either legitimate representatives of the same truth state or are excluded by root-lattice Voronoi facets; min-plus states are orbit types.

**Expected move.** This directly neutralizes the single-representative midpoint/recombination failures while retaining finite transfer closure.

**Smallest experiment.** In \(E_8\), partition the 240 roots into two orbits under small reflection subgroups, then use SAT/ILP to assign orbit triples to NAND/COPY shell vertices; certify the complete root shell and compute depth-two orbit transfers.

**Falsification/death.** Signed mixtures between representatives may create a cheaper DROP/parity state, or redundant representatives may destroy deterministic gluing.

**Obstruction audit.** G1: no slack. G2/G3: complete root/Voronoi certificates cover \(\mathbb Z^8\). G5: glue the full representative orbit. G6: orbit membership is emitted, not filtered. G7: kernel mixtures retain Euclidean cost. G9/G11/G12/G13/G15/G19: unrestricted orbit combinations are transfer states. G14/G31/G38: no extrapolation beyond certified facets. G28: strict orbit-transfer growth remains mandatory. G30, G32/G37: no tensor or additive-copy premise. G33/G34: no exterior tags. GD1/GD2: no pair diagonal or convolution.

---

## 7. Toric-circuit no-go theorem for unique affine ports

**Mechanism.** Attempt to refute the current search class: encode the four legal lifted NAND points as columns and compute their integer toric circuits. If every primitive, single-representative, affine-auxiliary realization has a circuit whose alternative nonlegal lattice combination shares the legal barycenter, strict convexity forces an adverse point on or inside the common sphere.

**Expected move.** A theorem would justify amending the roadmap to require redundant or genuinely nonlinear port fibers; failure would produce the smallest algebraic template escaping all known midpoint arguments.

**Smallest experiment.** Enumerate legal-lift matrices of rank \(\le6\) with entries in \([-2,2]\); compute circuits/Hilbert bases and exact SDP feasibility for a positive-definite Gram and empty equal-radius NAND sphere.

**Falsification/death.** Empty lattice simplices may evade every integral circuit, making the theorem too narrow to affect the frontier.

**Obstruction audit.** G1/G6: theorem includes all emitted auxiliaries, with no slack or filters. G2/G3: circuits quantify over the full integer affine lattice. G5: assumes complete-port gluing. G7, G9/G11, G12, G13, G15, G19: their moves are included, but the theorem seeks any adverse circuit. G14/G31/G38: algebraic proof, not shell evidence. G28: it refutes the shell before claiming growth. G30, G32/G37, G33/G34, GD1/GD2: no tensor, additive copies, exterior repair, ordered-pair lift, or group ring.

Classical starting points only: Conway–Sloane, *Sphere Packings, Lattices and Groups* (3rd ed., 1999), for root lattices, Delaunay cells, and Construction A; Sturmfels, *Gröbner Bases and Convex Polytopes* (1996), for toric circuits and integer dependencies.
