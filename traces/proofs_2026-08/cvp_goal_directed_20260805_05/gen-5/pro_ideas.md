All sketches below alter the killed constructions rather than rerunning them. None assumes evidence from a finite shell is an asymptotic theorem.

### 1. Independent-coupling \(D_4\) escape

**Core trick.** Replace the killed common-magnitude triality Gram by  
\[
K(x,y,z)\otimes I_4,\qquad x,y,z\in\{-7/16,\ldots,7/16\},
\]
so the three Boolean pair interactions vary independently. This reaches feasible patterns such as \(A=1,B=C=2\), where all four symbolic NAND false-port excesses are positive.

**Expected move.** Produce an equal-radius NAND/COPY shell, then certify \(\lambda/\mu\ge65/64\) at depth two.

**Obstruction audit.** G1: every selector charged. G2/G3: exact relevant-vector enumeration covers all integers. G5: glue complete ports. G6: no filters. G7, G9/G11, G12, G15, G19: exact kernels, parity, DROP and signed states remain explicit tests. G13: no linear hash, though affine attacks remain. G14, G30, G38, GD1, GD2: no bags, tensor, splitter, pair lift or group ring. G28 and G32/G37 are **not escaped**; transfer growth and compatible-copy attacks must pass. G31: no shell extrapolation. G33/G34: no exterior tags.

**Experiment.** Reuse the 43 interaction signatures; test \(43\cdot15^3\) exact Grams, centers, relevant vectors and depth-two tables.

**Falsification/death.** No globally empty survivor; likely an off-cube malformed point enters before the Boolean gap reaches \(65/64\).

---

### 2. Reeve-simplex/Cayley Delaunay tile

**Core trick.** Represent the four legal NAND configurations as vertices of a non-unimodular empty lattice tetrahedron, then use a Cayley embedding to expose complete input/output ports. Search its secondary cone for a rational quadratic form making that tetrahedron Delaunay; internal height coordinates evade the three-pair Boolean-cube restriction.

**Expected move.** Nonnormal simplex geometry supplies an empty legal shell whose next lattice shell is sufficiently farther away.

**Obstruction audit.** G1: Cayley heights are charged. G2/G3: secondary-cone inequalities plus exact CVP certify all \(\mathbb Z^D\). G5: full Cayley faces are ports. G6: no external conditions. G7, G9/G11, G12, G15, G19: kernels, parity, DROP and signed combinations are included. G13: nonlinear height embedding is not the raw honest affine span. G14/G38: no bags/splitters. G28 and G32/G37 remain mandatory transfer tests. G30/GD1: no tensor or ordered-pair lift. G31: requires a cone theorem, not a finite pass. G33/G34: no bivectors. GD2: no multiplication.

**Experiment.** Enumerate Reeve tetrahedra of height \(2\le h\le8\), all small integral port projections, and exact secondary-cone LPs in dimension at most 12.

**Falsification/death.** Port projection may force a false tuple to share the Delaunay sphere; likely COPY cannot use the same codebook.

---

### 3. Nonlinear phase code plus Construction A

**Core trick.** Lift each three-bit port word by the quadratic phase map  
\[
\phi(a)=(1,a_i,a_ia_j)
\]
and complement coordinates to constant weight, then place these words in cosets of a small Construction-A lattice. Legal NAND words form one automorphism orbit, while every adverse syndrome is required to have coset-leader norm at least \(65/64\) of the legal norm.

**Expected move.** A complete syndrome-decoding table becomes the exact outside-\(K\) Voronoi certificate.

**Obstruction audit.** G1: phase and carry coordinates are charged. G2/G3: all cosets have exact leader tables. G5: full phase words are glued. G6: no filtering. G7/G15: zero syndromes remain dangerous codewords and are audited. G9/G11/G12/G19: parity, DROP and signed words are decoded explicitly. G13: the embedding is nonlinear, so the raw affine collision is not automatically preserved; any lifted collision still kills it. G14/G38: no bags. G28 and G32/G37 remain unescaped composition tests. G30/GD1/GD2: no tensor, pair lift or group ring. G31: use complete syndrome classes. G33/G34: no exterior metric.

**Experiment.** Use the \([8,4,4]\) Hamming Construction-A lattice; enumerate all phase embeddings and 256 syndromes with at most 64 selectors.

**Falsification/death.** A false or signed syndrome probably has the same minimum leader weight as a legal syndrome.

---

### 4. Strictly convex network-flow lattice

**Core trick.** Realize each port label as an integral demand vector in a graph and each tile cost as the minimum strictly convex quadratic energy of an unrestricted integral flow. Graph automorphisms equalize legal NAND energies, while a frustrated cycle is intended to force every false demand through an extra positive-resistance edge.

**Expected move.** Discrete convex-flow duality would give both finite transfer closure and an analytic coercive bound for every malformed demand.

**Obstruction audit.** G1: every edge flow is charged. G2/G3: convex-flow duality quantifies over the full integral circulation lattice. G5: complete boundary demand vectors are glued. G6: no filters. G7: zero-residual circulations still pay quadratic energy. G9/G11/G12/G13/G15: all induced demands remain admissible and must be bounded. G19 is **directly applicable**, not escaped: signed circulations are the primary test. G14/G30/G38/GD1/GD2: no bags, tensor, splitter, ordered pairs or ring product. G28 and G32/G37 remain required. G31: proof must be parametric, not shell-based. G33/G34: no exterior tags.

**Experiment.** Enumerate connected multigraphs on at most six vertices and eight edges; solve exact convex-flow minima for all small port demands and depth-two gluings.

**Falsification/death.** A negative circulation will probably cancel the frustrated edge, reproducing G19 in convex-flow language.

---

### 5. Port-only quadratic no-go theorem

**Core trick.** Attempt to refute a broad subfamily: tiles in which each truth configuration is assembled additively from three two-label port vectors, with no joint internal selector. Eliminate centers symbolically and use exact SDP/Farkas duality to test whether equal-radius NAND and COPY, positive false excesses, and positive definiteness can coexist.

**Expected move.** Either obtain an abstract feasible Gram, or amend the roadmap edge by proving that every viable tile needs genuinely joint internal coordinates.

**Obstruction audit.** G1/G5/G6 are built into the class: no slack, complete ports, no filters. G2/G3, G7, G9/G11, G12, G13, G15 and G19 are **not addressed** because the proposed theorem omits general auxiliary and signed fibers; it cannot refute the full FRONTIER. G14/G30/G38/GD1/GD2 are absent mechanisms. G28, G31 and G32/G37 are downstream and untouched. G33/G34 are outside the port-only Gram class. Thus this is only a justified architectural amendment, not a hardness lemma.

**Experiment.** Build the rational SDP on the six port-difference vectors; search strict feasibility, then extract either a rational Gram or an exact dual certificate.

**Falsification/death.** A positive-definite feasible Gram immediately kills the no-go claim—quite plausibly once all three couplings are independent.

---

### 6. Lawrence-lifted toric tile

**Core trick.** Encode legal gate configurations as columns of an integer matrix \(A\), then use its Lawrence lifting so every unrestricted same-port deviation is a toric binomial. Choose \(A\) and diagonal Euclidean weights so every gate-violating Graver element is long, while legal exchange elements are short and equal-cost; conformal Graver decomposition then extends the bound to the entire integer fiber.

**Expected move.** Prove unrestricted coercivity algebraically rather than by bounded enumeration.

**Obstruction audit.** G1: both Lawrence copies are charged. G2/G3: the complete Graver basis is the certificate, not an assumption. G5: full sufficient statistics are ports. G6: no quotient filters. G7/G15: exact kernels are precisely the toric fiber. G9/G11/G12/G19: parity, DROP and signed splice appear as Graver or conformal sums. G13: enlarged nonlinear columns avoid the raw-selector claim, but a new affine collision remains fatal. G14/G38: no bag inference. G28 and G32/G37 remain transfer tests. G30/GD1/GD2: no tensor, pair lift or ring units. G31: conformal decomposition supplies uniformity. G33/G34: no bivectors.

**Experiment.** Enumerate \(0/1\) matrices with 8–10 columns and at most six rows; compute primitive kernel moves and solve an exact LP for a \(65/64\) weight margin.

**Falsification/death.** NAND likely forces a universal short circuit linking legal and false columns.

---

### 7. Deep-hole orbit tile in \(E_8\)

**Core trick.** Use a rational deep hole of \(E_8\) and select the four legal NAND states from one stabilizer orbit of nearest lattice points, assigning ports by a joint orbit map rather than a Cartesian Boolean embedding. Deep-hole shell classification or an exact theta-series calculation would certify that every other port class lies in the next shell.

**Expected move.** Obtain equal legal radius and a symmetry-certified global Voronoi gap before constructing the depth-two transfer operator.

**Obstruction audit.** G1: orbit selectors are anchored. G2/G3: complete shell classification covers all lattice points. G5: glue the entire orbit-derived port. G6: no filters. G7/G9/G11/G12/G13/G15/G19: kernel, parity, DROP, affine and signed states must map to classified orbit classes; none is assumed absent. G14/G38: no bags or splitters. G28 and G32/G37 remain compulsory depth-two tests. G30/GD1: no tensor or ordered-pair lift. G31: classification, not finite-shell extrapolation. G33/G34: no exterior tags or repaired Gram. GD2: additive lattice geometry only.

**Experiment.** Enumerate rational \(E_8\) centers of denominator at most four, nearest/second shells, stabilizer orbits, and all orbit maps onto NAND/COPY ports with at most 240 selectors.

**Falsification/death.** Port surjectivity will likely place an adverse state in the nearest orbit, or the second-shell ratio will be below \(65/64\).
