Below are six deliberately nonconvergent mechanisms. Each either attacks the fixed Voronoi-coercive frontier directly or justifies a narrowly scoped roadmap amendment.

### 1. Coefficient-unbounded \(E_6\) affine-map closure

**Core trick.** Fix the certified 27-point \(E_6\) shell and classify every rational affine row that is binary-valued on it. Values on seven affinely independent vertices determine the row, so finitely many exact solves cover unbounded coefficients.

**Expected move.** Either find a genuine NAND projection, or refute every affine projection of this shell and amend the edge to require nonlinear/redundant ports.

**Obstruction audit.** G2/G3 are directly handled by coefficient-unbounded exact classification. G1/G5/G6/G7/G9/G11/G12/G13/G15/G19 concern gadgets, gluing, or unrestricted fibers not claimed here. G14/G28/G31/G32/G37/G38 concern amplification or extrapolation, also not claimed. G30/GD1, G33/G34, and GD2 are outside scope because there is no tensor lift, exterior metric, or group ring.

**Smallest experiment.** Verify affine rank six; enumerate the \(2^7\) binary assignments on an affine basis, solve each row over \(\mathbb Q\), test all 27 vertices, then test triples against all translated/relabelled NAND relations.

**Falsification / likely death.** One surviving nonconstant triple kills the no-go but supplies the next tile seed.

---

### 2. Unimodular truth-table simplex

**Core trick.** The four legal NAND words \(001,011,101,110\) form an affine unimodular simplex in \(\mathbb Z^3\). Rather than projecting a large Delaunay shell, choose a rational metric making precisely this simplex Delaunay; use primitive COPY segments so the old integral-midpoint attack disappears.

**Expected move.** Obtain the smallest possible exact NAND shell, then seek nonorthogonal seam weights with \(\lambda/\mu\ge65/64\).

**Obstruction audit.** G1/G6: every selector and seam variable is charged and emitted. G2/G3: Voronoi reduction must cover all \(\mathbb Z^D\). G5: all three integer ports are glued. G7/G9/G11/G12/G13/G15/G19 enter the unrestricted transfer table. G14/G31/G38 permit no finite-shell extrapolation. G28/G32/G37 directly apply: strict depth-two growth is mandatory. G30/GD1, G33/G34, GD2 are outside because there is no tensor/ordered-pair lift, exterior tag, or group ring.

**Smallest experiment.** Solve exactly for \(Q\succ0,c\) in dimension three; enumerate \([-3,3]^3\) for shell emptiness. Couple one NAND simplex to primitive COPY segments and compute the complete depth-two table.

**Falsification / likely death.** A neighboring false word probably shares too cheap a Voronoi facet, yielding \(\lambda\le\mu\).

---

### 3. Construction-A deep-hole ports

**Core trick.** Use a small linear code whose syndrome cosets have exactly known Euclidean coset-leader energies. Assign the four NAND states to equal-energy deep-hole cosets; malformed ports should lie in cosets with larger leader norm, while quotient carries make modular gluing explicit.

**Expected move.** Replace arbitrary shell labeling by a coding-theoretic Voronoi certificate and finite syndrome transfer algebra.

**Obstruction audit.** G1/G6: equations \(p-p'=qk\) and all carries are emitted and charged. G2/G3: exact coset decomposition covers the full integer lattice. G5: complete syndromes are glued. G7/G13 directly apply—zero-syndrome affine combinations and free carries must be excluded. G9/G11/G12/G15/G19 are included in full coset fibers. G14/G31/G38 forbid extrapolating a bounded code search. G28/G32/G37 apply to recursive transfer. G30/GD1, G33/G34, GD2 are outside: no tensor lift, exterior metric, or group-ring multiplication.

**Smallest experiment.** Enumerate binary codes of length at most eight, all target cosets, and three syndrome-port maps; compute exact coset leaders and depth-two min-plus tables. Start with the extended Hamming code.

**Falsification / likely death.** Honest affine collisions may remain in the zero-syndrome coset, reproducing G13 with enlarged coordinates.

---

### 4. Totally-real ideal-coset tile

**Core trick.** Work in the Minkowski embedding of a small totally real number field. Ports are residues modulo a prime ideal; legal NAND residues receive equal shortest representatives, while ideal minima and trace-form Voronoi cells certify larger energy for malformed residues.

**Expected move.** Obtain a \(65/64\) gap from arithmetic coset minima rather than combinatorial shell engineering.

**Obstruction audit.** G1/G6: ideal-quotient carries are explicit charged coordinates. G2/G3: exact ideal-coset SVP/Voronoi certificates quantify over every algebraic integer. G5: full residue ports are glued. G7/G13 apply because exact kernels and affine residue collisions remain possible. G9/G11/G12/G15/G19 are unrestricted residue-fiber states. G14/G31/G38 prohibit finite-field extrapolation. G28/G32/G37 apply to composed transfers. G30/GD1 and G33/G34 are absent. GD2 is outside its stated assumptions—this uses a field trace lattice, not a group ring—but units must still be audited independently.

**Smallest experiment.** Enumerate real quadratic fields of discriminant at most \(29\), prime ideals of norm \(2\) or \(3\), and three-port residue assignments; use exact Fincke–Pohst enumeration and depth-two tables.

**Falsification / likely death.** Small-norm units may move malformed residues to representatives as cheap as legal ones.

---

### 5. Discrete-convex / graph-cut tile

**Core trick.** Restrict the tile quadratic to an \(L^\natural\)-convex integer form: separable coercive anchors plus nonpositive pair interactions. Then every unrestricted internal minimization has an exact convex-flow or min-cut certificate, potentially giving a symbolic transfer theorem rather than shell enumeration.

**Expected move.** Synthesize NAND/COPY ground states with equal legal energy and prove adverse growth by discrete-convex exchange inequalities.

**Obstruction audit.** G1/G6: no uncharged slack or filters. G2/G3: integer convex-flow duality covers unbounded fibers. G5: complete port variables are shared. G7/G9/G11/G12/G13/G15/G19 are ordinary integral states in the global minimization. G14/G31/G38 are avoided only if an exchange theorem replaces finite extrapolation. G28/G32/G37 directly apply; the theorem must prove strict, nonadditive growth. G30/GD1, G33/G34, GD2 are outside because no tensor lift, exterior synthesis, or group ring appears.

**Smallest experiment.** Enumerate submodular quadratic gadgets with three Boolean ports, at most six auxiliaries, and weights \(0,\ldots,4\); certify unrestricted minima by convex-cost flow, then compose two copies.

**Falsification / likely death.** Minimizer-set closure for submodular functions may make exact NAND ground states impossible, or force additive adverse energy.

---

### 6. Topological systolic filling tile

**Core trick.** Let coefficients be integral chains in a small 2-complex and ports be complete boundary/homology data. Legal NAND boundaries receive equal minimum-energy fillings; malformed boundaries should require an additional systolic cycle, certified by an integral dual cochain calibration.

**Expected move.** Turn the outside-shell certificate into a filling inequality valid for every signed chain, then compose by identifying entire boundary complexes.

**Obstruction audit.** G1/G6: all chains, boundaries, and normalization rows are charged and emitted. G2/G3: SNF plus dual calibrations cover complete chain groups. G5: full boundary chains are glued. G7/G9/G11/G12/G13/G15 are explicit kernel or pseudosection classes. G19 directly applies: signed cycle cancellation is a mandatory attack. G14/G31/G38 forbid extrapolation from enumerated complexes. G28/G32/G37 apply to recursive filling growth. G30/GD1, G33/G34, GD2 are outside because this uses neither tensors, exterior tags, nor group rings.

**Smallest experiment.** Enumerate oriented complexes with at most 12 edges and eight faces; compute SNF, all boundary-class minimum norms, dual certificates, and the depth-two glued transfer table.

**Falsification / likely death.** A short signed cycle will probably splice two legal fillings and erase the proposed systolic surcharge.
