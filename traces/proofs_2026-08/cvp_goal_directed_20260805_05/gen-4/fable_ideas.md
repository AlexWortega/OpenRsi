I treat the active FRONTIER as the **Voronoi-coercive tile lemma**. Each proposal either constructs its required empty shell and transfer inequality or gives an exact obstruction certificate.

### 1. Non-antipodal \(D_4\) triality completion

**Mechanism.** Continue the surviving edge, but assign each Boolean value an ordered, distinct, non-antipodal pair in the triality classes. The killed midpoint argument then no longer applies automatically because \((v_0+v_1)/2\) need not belong to \((2D_4^*)^3\).

**Expected move.** Find an empty common sphere and then certify \(\lambda/\mu\ge65/64\) from complete depth-two transfers.

**Experiment.** Run the exact search prescribed by `GATE.json`: six class assignments, all non-antipodal ordered pairs, 952 retained Grams, exact sphere solving, Fincke–Pohst enumeration of every point through the radius, then unrestricted glued tables.

**Falsifier / likely death.** Any extra shell point; most likely a three-point affine combination replacing the old midpoint.

**Obstruction audit.** G1/G6: every coefficient is charged, with no filters. G2/G3/G14/G31/G38: ellipsoid bounds cover all integers, not named shells. G5: complete ports are glued. G7/G9/G11/G12/G13/G15/G19/G32/GD1: kernels, parities, DROP, affine lifts and signed diagonals are explicitly included. G28: acceptance requires measured \(\lambda>\mu\). G30: no tensor. G33/G34: no exterior tags or frozen repair. G37: nonorthogonal triality Gram, not the killed incidence family. GD2: no group ring.

---

### 2. Construction-A coset-leader tile

**Mechanism.** Build ports from Construction-A lattices associated with the extended Hamming code, using distinct coset leaders rather than a common linear syndrome. Arrange NAND/COPY legal tuples as equal-norm deep-hole neighbors; decoding by coset and Voronoi-relevant-vector inequalities supplies an exact outside-shell certificate.

**Expected move.** Coding distance makes every malformed transfer change either coset-leader weight or coupling energy, potentially yielding \(65/64\).

**Experiment.** Use three \(E_8\) blocks, enumerate ordered minimal coset leaders as port labels, and search block couplings with denominator at most eight. Decode every coset exactly and construct depth-two tables only for empty-shell survivors.

**Falsifier / likely death.** Hamming-code linearity may create a parallelogram of legal words with a cheap fourth, reproducing G13 geometrically.

**Obstruction audit.** G1/G6: no slack or external syndrome filter. G2/G3/G14/G31/G38: decoding plus relevant-vector inequalities covers the entire lattice. G5: full coordinates and cosets are glued. G7/G9/G11/G12/G15/G19/G32/GD1: all such states are decoded and costed. G13: no claim that a compatible linear hash separates an affine span. G28: depth-two \(\lambda>\mu\) is tested. G30: no tensor. G33/G34: no bivectors or repaired exterior Gram. G37: couplings are jointly synthesized, not orthogonal incidence weights. GD2: additive code lattice, not convolution.

---

### 3. Totally positive trace-form tile

**Mechanism.** Use an ideal lattice \(I\) in a totally real number field with rational trace form
\[
Q_\beta(x)=\operatorname{Tr}_{K/\mathbb Q}(\beta x^2),\qquad \beta\gg0.
\]
Non-antipodal algebraic-integer port labels can have equal trace norm while their rational-looking averages are absent from \(I\); conjugate embeddings provide coercivity in several incompatible directions.

**Expected move.** A malformed integer combination short in one embedding must expand in another, producing an empty legal sphere and strict adverse transfer growth.

**Experiment.** In the real cubic field defined by \(x^3+x^2-2x-1\), enumerate labels and totally positive \(\beta\) with coefficients in \([-2,2]\), using three ideal blocks and at most 64 columns. Compute exact Voronoi vectors and depth-two minima.

**Falsifier / likely death.** A short unit translate or trace-balanced affine combination lies inside every feasible legal sphere.

**Obstruction audit.** G1/G6: all ideal coordinates are charged and emitted. G2/G3/G14/G31/G38: conjugate lower bounds give a global finite ellipsoid, followed by exact enumeration. G5: whole ideal ports are glued. G7/G9/G11/G12/G13/G15/G19/G32/GD1: these become unrestricted ideal-lattice points and are audited. G28: requires actual \(\lambda>\mu\). G30: no tensor. G33/G34: trace form is not an exterior-tag repair. G37: nonorthogonal conjugate geometry escapes its metric family. GD2: no multiplication or group-ring units are used—only the additive ideal lattice.

---

### 4. Affine-Weyl alcove/Cayley tile

**Mechanism.** Embed Boolean port colors into a Cayley sum and realize each legal truth table as vertices of a unimodular affine-Weyl alcove, initially in \(A_r^*\). Empty-sphere control comes from the alcove triangulation rather than a hand-enumerated spherical code; shared color coordinates implement complete gluing.

**Expected move.** Unimodularity eliminates interior lattice points, while asymmetric Cayley heights make FALSE and DROP cross additional alcove facets, potentially forcing strict transfer growth.

**Experiment.** Search \(A_5^*\) and \(A_6^*\) alcoves for four NAND and two COPY legal vertices, with integral Cayley heights in \(\{0,1,2\}\). Solve exact secondary-cone inequalities, then enumerate the first glued transfer table.

**Falsifier / likely death.** Alcove exchange or submodularity may force an additional mixed-color vertex at no greater radius.

**Obstruction audit.** G1/G6: heights are lattice coordinates, not slack or filters. G2/G3/G14/G31/G38: the alcove theorem certifies the base shell; an eigenvalue bound audits all glued integer states. G5: all color coordinates are identified. G7/G9/G11/G12/G13/G15/G19/G32/GD1: no state class is excluded. G28: the secondary cone is retained only if \(\lambda>\mu\). G30: no tensor. G33/G34: no exterior coordinates or fixed repair. G37: Cayley cross-terms fall outside the orthogonal incidence family. GD2: no group algebra.

---

### 5. Exact inverse-Delaunay synthesis and no-go certificates

**Mechanism.** Treat the tile as an inverse problem: enumerate primitive integral codebooks, while solving exact linear inequalities for the center and Gram matrix that put precisely the legal points on one sphere and every other lattice point outside. Infeasible cases return Farkas/semialgebraic certificates, potentially proving a bounded-coordinate impossibility theorem rather than another empirical failure.

**Expected move.** Either output a rational tile with certified margin and \(\lambda/\mu\ge65/64\), or identify a universal affine circuit forcing an interior malformed state.

**Experiment.** Enumerate port dimension four, \(D\le10\), codewords in \(\{-1,0,1\}^4\), and normalized rational Grams. Alternate exact cone solving with Fincke–Pohst counterexample generation; test NAND and COPY jointly at depth two.

**Falsifier / likely death.** Every codebook cone is cut off by a short affine circuit; alternatively, enumeration becomes intractable before dimensions capable of NAND closure.

**Obstruction audit.** G1/G6: emitted coordinates only. G2/G3/G14/G31/G38: positive-definite lower bounds make counterexample generation exhaustive. G5: synthesis includes complete glue equations. G7/G9/G11/G12/G13/G15/G19/G32/GD1: each is simply a candidate integer counterexample. G28: \(\lambda>\mu\) is an explicit constraint. G30: no tensor. G33/G34/G37: Gram and codebook are synthesized jointly, outside all three frozen metric families. GD2: no group ring.

---

### 6. Voronoi-first-kind graph-cut tile

**Mechanism.** Restrict to lattices admitting an obtuse superbase, whose Voronoi-relevant vectors correspond to graph cuts. Choose graph weights so legal NAND/COPY configurations are equal-weight cuts, while every malformed state crosses a provably heavier cut family; nearest-point and shell certification then reduce to exact min-cut inequalities.

**Expected move.** A cut-weight margin gives a symbolic outside-shell proof and may compose through ports as a strict min-plus cycle-mean gap.

**Experiment.** Enumerate weighted graphs on six vertices with edge weights \(1,\dots,16\), assign three port bits to designated cut coordinates, and solve equal-cost NAND/COPY constraints. For survivors, compute all relevant cuts and the unrestricted depth-two transfer operator.

**Falsifier / likely death.** Cut submodularity/uncrossing likely manufactures a cheap malformed cut from two legal cuts, a graph-theoretic analogue of the \(D_4\) midpoint.

**Obstruction audit.** G1/G6: graph coordinates are charged; no filtering. G2/G3/G14/G31/G38: the relevant-vector theorem covers every lattice state, not a sampled shell. G5: designated cut coordinates are fully glued. G7/G9/G11/G12/G13/G15/G19/G32/GD1: all induce cuts or integer combinations included in the transfer minimum. G28: cycle-mean computation must certify \(\lambda>\mu\). G30: no tensor. G33/G34: no exterior metric. G37: cut Gram has nonorthogonal graph couplings. GD2: no multiplicative algebra.

**Classical ingredients only:** Fincke–Pohst lattice enumeration; Construction A and \(E_8\) as presented in Conway–Sloane, *Sphere Packings, Lattices and Groups* (3rd ed., 1999); secondary cones in Gelfand–Kapranov–Zelevinsky, *Discriminants, Resultants, and Multidimensional Determinants* (1994); and Voronoi’s classical theory of lattices of the first kind.
