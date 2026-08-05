Below are six intentionally unranked mechanisms. Each is a genuine mutation beyond the killed \(D_4/E_6\) affine-port branches.

1. **Chromatic lift of the certified \(E_6\) shell.**  
**Core trick.** Color the 27 Gosset vertices by the four legal NAND words, then replace \(v\) by \((v,e_{\chi(v)})\). The color is now an emitted lattice coordinate—not an external nonlinear map—and a new Gram matrix may destroy the old affine collisions while retaining the certified \(E_6\) geometry.

**Move/falsifier.** Seek an empty equal-radius lifted shell, then COPY and depth-two \(\lambda/\mu\ge65/64\). Any lifted affine collision or interior non-codeword kills it.

**Audit.** G1/G6/G12: all selectors, normalization, and DROP coordinates are emitted and charged. G2/G3/G14/G31/G38: require an exact augmented-lattice Voronoi certificate, not finite extrapolation. G5: glue the complete color coordinate. G7/G9/G11/G13/G15/G19/GD1 are not automatically escaped; SNF and unrestricted shell enumeration must include their kernel, parity, affine, signed, and diagonal states. G28/G32/G37 are also not escaped: exact depth-two strict growth is mandatory. G30/G33/G34/GD2: no tensor, bivector metric repair, or group ring.

**Smallest experiment.** Enumerate equitable four-colorings of the 27-vertex Schläfli graph invariant under small subgroups; solve exact Gram/center feasibility in dimension 10 and run Fincke–Pohst.

**Likely death.** Color-coordinate differences generate a shorter signed affine intruder.

2. **Construction-A coset-leader tile.**  
**Core trick.** Use \(\Lambda=q\mathbb Z^N+C\), with truth configurations represented by distinct canonical syndromes having equal coset-leader norm. Carries \(z=r+qk\) are emitted and charged; exhaustive syndrome decoding gives the complete unrestricted transfer operator and an outside-\(K\) certificate.

**Move/falsifier.** Find a code/target where four NAND syndromes tie at \(\mu\), while every false, DROP, malformed, or seam-inconsistent syndrome costs at least \(65\mu/64\). A cheap adverse coset leader falsifies it.

**Audit.** G1/G6/G12: no free carries, filters, or uncharged drops. G2/G3/G14/G31/G38: residue reduction plus exact coset minima covers all integers, not a shell extrapolation. G5: full syndrome ports are glued. G7/G9/G11/G13/G15/G19/GD1 are not excluded by coding alone; every resulting syndrome, including affine and diagonal collisions, must be decoded. G28/G32/G37 remain live and require exact depth-two growth. G30/G33/G34/GD2: no tensor, exterior tags, metric repair, or convolution.

**Smallest experiment.** For \(q=3,N=8\), enumerate \(H=[I_4\mid B]\) with circulant \(B\); decode all \(3^8\) residues exactly for every target and NAND/COPY syndrome assignment.

**Likely death.** Linearity forces a G13-type combination into a legal or equally short syndrome.

3. **Voronoi-first-kind / min-cut gate.**  
**Core trick.** Restrict to lattices with an obtuse superbase, where unrestricted CVP reduces exactly to a weighted cut problem. Encode ports as terminal-side indicators; nonorthogonal graph edges couple the three truth bits, while submodularity supplies a global certificate for every integer coefficient.

**Move/falsifier.** Synthesize a graph whose four legal NAND cuts have equal cost and every adverse boundary condition has a \(65/64\) larger min-cut, then verify depth two. A submodular inequality placing a false cut no higher than the legal cuts kills the family.

**Audit.** G1/G6/G12: every edge, terminal, normalization, and DROP penalty is emitted. G2/G3/G14/G31/G38: the min-cut reduction is an all-integer theorem, not bounded enumeration. G5: all terminal indicators are glued. G7/G9/G11/G13/G15/G19/GD1: signed coefficients are reduced canonically to cuts, so these attacks are covered rather than presumed absent. G28/G32/G37 are not escaped; strict composed transfer must be computed. G30/G33/G34/GD2: no tensor, bivector, repaired Gram, or group algebra.

**Smallest experiment.** Enumerate six-vertex complete graphs with six terminal-orbit edge weights in \(\{1,2,3\}\); solve all NAND/COPY boundary min-cuts and depth-two tables exactly.

**Likely death.** NAND’s cost table violates the submodularity inequalities obeyed by every cut function.

4. **Discriminant-form glue tile.**  
**Core trick.** Build an even lattice from root-lattice components and an isotropic subgroup of its finite discriminant quadratic form. Ports are complete discriminant classes; exact minimum norms in each class provide finite transfer tables, while root-lattice reduction certifies all representatives.

**Move/falsifier.** Arrange four shifted classes as equal-minimum NAND states and make every adverse class longer by \(65/64\); glue gates by equality in the full discriminant group. A short isotropic or affine class falsifies the tile.

**Audit.** G1/G6/G12: glue variables, normalization, and zero-class DROP are charged. G2/G3/G14/G31/G38: discriminant-class reduction plus exact theta/minimum certificates covers unbounded fibers. G5: complete classes, not private marginals, are glued. G7/G9/G11/G13/G15/G19/GD1 are not automatically excluded; their classes and shortest representatives must be tested explicitly. G28/G32/G37 remain genuine transfer obstructions requiring strict depth-two computation. G30/G33/G34: no tensor or exterior-metric repair. GD2: addition in a finite quadratic form, not group-ring multiplication.

**Smallest experiment.** Use \(A_2^6\), enumerate low-dimensional isotropic subspaces of \((\mathbb Z/3)^6\), shifted targets, and all class minima through the legal radius; test NAND before COPY.

**Likely death.** Isotropic-subgroup closure makes the equal-minimum relation affine, which NAND is not.

5. **Dimension-free hypermetric no-go search.**  
**Core trick.** Try to refute the FRONTIER using negative-type/hypermetric inequalities rather than another cell. Search for an integer affine combination of equal-radius legal NAND points whose emitted port is false or malformed; the variance identity would force one such lattice point onto or inside the legal sphere in every Euclidean dimension.

**Move/falsifier.** A symbolic Farkas certificate would generalize the \(D_4\) midpoint and recombination attacks and force the roadmap to abandon single-shell additive ports. A feasible abstract Gram model separating every generated adverse combination kills this no-go mechanism, not the FRONTIER.

**Audit.** G1/G6/G12: the symbolic model includes all emitted coordinates and DROP. G2/G3/G14/G31/G38: promotion requires a quantified inequality, never finite-shell extrapolation. G5: the complete port homomorphism is symbolic. G7/G9/G11/G13/G15/G19/GD1 appear as candidate integer affine vectors, not excluded assumptions. G28/G32/G37 are attacked directly by proving \(\lambda\le\mu\). G30/G33/G34/GD2: no tensor, exterior metric, or multiplication structure is assumed.

**Smallest experiment.** ILP-enumerate coefficient vectors in \(\{-2,-1,0,1,2\}^4\) with sum one and adverse NAND port; search rational SDP dual certificates valid for every Gram matrix and center.

**Likely death.** Redundant codebooks may prevent every short affine combination from landing on an adverse port.

6. **Totally real number-field trace barrier.**  
**Core trick.** Embed port coordinates in \(\mathcal O_K\) for a fixed totally real field and use the trace form \(\sum_\sigma|\sigma(x)|^2\). Legal states are chosen from Galois orbits, giving equal radius automatically; any malformed algebraic difference has nonzero integral norm, so AM–GM can yield a dimension-independent Euclidean lower bound.

**Move/falsifier.** Search for NAND/COPY orbit labels whose nonzero norm bound gives \(\lambda/\mu\ge65/64\), then compose using emitted coefficient-wise equalities. A unit or signed affine combination with small trace norm falsifies it.

**Audit.** G1/G6/G12: all algebraic coefficients, carries, normalization, and DROP are charged. G2/G3/G14/G31/G38: Minkowski/trace bounds plus exact ideal-lattice enumeration cover all integers. G5: every integral-basis port coordinate is glued. G7/G9/G11/G13/G15/G19/GD1 are not inherently excluded; exact-kernel, parity, affine, signed, and diagonal combinations must satisfy the same norm audit. G28/G32/G37 still require strict depth-two verification. G30/G33/G34: no tensor or exterior repair. GD2: a field trace lattice has no bicyclic zero divisors and uses no group-ring convolution.

**Smallest experiment.** In \(K=\mathbb Q(\sqrt2,\sqrt3)\), enumerate small algebraic port labels and rational centers, construct the trace Gram exactly, and run Fincke–Pohst through the legal radius.

**Likely death.** Units or affine sums create low-trace intruders despite nonzero algebraic norm.

Classical tools invoked here are standard treatments from Conway–Sloane, *Sphere Packings, Lattices and Groups* (3rd ed., 1999), and Neukirch, *Algebraic Number Theory* (1999).
