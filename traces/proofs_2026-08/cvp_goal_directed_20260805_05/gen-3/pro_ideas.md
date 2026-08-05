I treat the fixed FRONTIER as the **Voronoi-coercive NAND/COPY tile lemma**, not either retired construction.

### 1. Barnes–Wall quotient decoder

**Mechanism.** Use a Construction-D/Barnes–Wall lattice with ports represented by cosets modulo \(2L\). Choose equal-norm cosets for legal NAND/COPY states; recursive coset decoding supplies an exact lower bound for every other integer coefficient vector rather than a bounded shell search.

**Expected move.** Find port offsets whose complete quotient-state transfer table has \(\lambda/\mu\ge65/64\), with the decoder proving outside-codebook coercivity.

**Experiment.** Build \(BW_{16}\), enumerate its \(2^{16}\) quotient states by Walsh DP, and search eight-symbol port embeddings with at most 32 columns. Compute depth-one/two tables exactly.

**Falsification / likely death.** A signed combination of equal-norm cosets may decode to a cheaper malformed coset, reproducing affine parity geometrically.

**Obstruction audit.** G1: every quotient coordinate is charged. G2/G3: decoding covers all \(\mathbb Z^D\). G5: full cosets are glued. G6: no filters. G7: kernel vectors retain lattice norm. G9/G11/G12/G13/G15/G19/G32/G37: parity, DROP, affine, laminar, signed, and additive states are explicit decoder states, not excluded assumptions. G14/G31/G38: no bag, finite-shell, or splitter extrapolation. G28: directly tested, not escaped. G30/GD1: no tensor or ordered-pair lift. G33/G34: no exterior tags. GD2: no group-ring convolution.

### 2. Regular-matroid circuit coercion

**Mechanism.** Realize each tile as a weighted graphic or cographic lattice with truth values encoded by terminal cuts. Total unimodularity makes every integral deviation decompose into signed primitive circuits; a circuit inequality could certify that every malformed transfer pays more energy than a legal cut.

**Expected move.** Reduce the unrestricted Voronoi claim to finitely many circuit inequalities and optimize rational edge weights for \(\lambda/\mu\ge65/64\).

**Experiment.** Enumerate graphs with at most ten edges and three terminal ports. Search terminal-cut NAND labelings and solve an exact LP over edge weights; verify all circuits and depth-two transfers.

**Falsification / likely death.** G19-style signed circulations may splice legal cuts at essentially additive cost; this mechanism is not outside that danger.

**Obstruction audit.** G1: all edges are charged. G2/G3: the circuit theorem covers the entire integral flow lattice. G5: all terminal incidences are glued. G6: no external filter. G7: exact circulations are charged by edge energy. G9/G11/G12/G13/G15/G32/G37: parity, DROP, affine, laminar, and additive states enter the circuit audit. G19: not escaped—its signed splice is the primary circuit test. G14/G31/G38: no bag/shell/splitter inference. G28: exactly the desired circuit inequality. G30/GD1: no tensor/diagonal lift. G33/G34: no exterior metric. GD2: no group algebra.

### 3. Inverse Delaunay design via secondary cones

**Mechanism.** Do not label a frozen \(D_4/E_8\) cell. Instead prescribe integer representatives for the legal NAND/COPY states and solve for a rational positive-definite Gram matrix making them one empty Delaunay sphere while placing every adverse transfer beyond the \(65/64\) threshold. Voronoi reduction turns this into linear inequalities inside an \(L\)-type cone plus exact short-vector separation.

**Expected move.** Either produce a rational Gram/factor and unrestricted certificate or prove the chosen affine configuration impossible by an exact Farkas certificate.

**Experiment.** In dimension six, alternate an exact LP over Gram entries with an SVP separation oracle; start with seven NAND representatives and at most 24 selector columns.

**Falsification / likely death.** Equal-radius legal points may force an affine adverse point onto or inside their sphere.

**Obstruction audit.** G1: the Gram is positive definite on every column. G2/G3: SVP separation quantifies over all integers. G5: complete linear ports are included. G6: no filter. G7/G9/G11/G12/G13/G15/G19/G32/G37: kernels, parities, DROP, affine lifts, signed states, and additive copies are explicit separating constraints. G14/G31/G38: no finite extrapolation. G28: the optimized inequality is precisely its missing condition. G30/GD1/GD2: no tensor, pair lift, or convolution. G33/G34: outside their frozen exterior-tag family; nevertheless positive-definite feasibility is checked exactly.

### 4. Tropical parallelogram no-go certificate

**Mechanism.** Attempt to **refute** the frontier. A tile transfer cost is a lower envelope of positive-semidefinite quadratic translates; search for an unavoidable affine relation among equal-cost NAND and COPY representatives that, through the parallelogram identity, places some FALSE or malformed port at cost at most \(\mu\). This would force \(\lambda\le\mu\) independently of dimension.

**Expected move.** Derive a symbolic tropical/discrete-convex inequality contradicting \(65/64\), or identify precisely which non-affine codebook geometry evades it.

**Experiment.** Enumerate affine matroids on at most eight port representatives of rank at most four. For each, use exact SDP/Farkas elimination to test whether equal legal radii imply a cheap adverse midpoint or signed combination.

**Falsification / likely death.** Arbitrary port codebooks may avoid every necessary affine relation; then this proves only a restricted no-go theorem.

**Obstruction audit.** G1/G5/G6: the theorem models charged columns, complete ports, and emitted equations. G2/G3: it is universal over integer fibres, not boxed. G7/G9/G11/G12/G13/G15/G19/G32/G37: these become candidate affine witnesses and are covered rather than assumed absent. G14/G31/G38: no extrapolation. G28: this directly seeks its universal failure. G30/GD1/GD2: no tensor, diagonal, or group-ring assumption. G33/G34: arbitrary PSD geometry is allowed, not their frozen exterior family. If the affine relation is not forced, the route honestly does not address the full frontier.

### 5. \(D_4\) triality rather than product-cell labeling

**Mechanism.** Exploit the three cross-polytope classes of the \(D_4\) 24-cell and triality between them. Put the two inputs and output in different triality classes, then add one rational skew coupling so exactly the four NAND triples occupy a common Delaunay shell; COPY uses the fixed class-swapping involution. Facet inequalities of the 24-cell, not enumeration alone, provide coercion.

**Expected move.** Obtain a nonorthogonal transfer law where compatible parity copies cannot add independently, potentially defeating G32/G37.

**Experiment.** Enumerate triality-class port assignments and rational couplings with denominator at most 16 in dimension 12. Use exact 24-cell facets and Fincke–Pohst only for the bounded residual fundamental domain.

**Falsification / likely death.** Triality symmetry may create an isometric false triple or an affine midpoint with equal energy.

**Obstruction audit.** G1: all \(D_4\) coefficients are normed. G2/G3: facets plus a fundamental-domain proof cover all integers. G5: whole triality ports are glued. G6: no filters. G7/G9/G11/G12/G13/G15/G19/G32/G37: kernels, parity, DROP, affine lifts, signed splice, and additive copies are transfer states. G14/G31/G38: no bag/shell/splitter inference. G28: depth-two \(\lambda>\mu\) remains mandatory. G30/GD1: no tensor/pair lift. G33/G34: no bivectors or repaired exterior metric. GD2: no group ring.

### 6. Cohomological winding tile over the \(A_2\) lattice

**Mechanism.** Encode each Boolean port as one of two Voronoi phases of \(A_2\) on the boundary of a small annulus. Gate-dependent offsets make legal NAND triples have zero winding, while false triples carry a nontrivial integral \(H^1\) class; a discrete Hodge inequality then lower-bounds every representative’s Euclidean energy. The transfer codebook records boundary phase and winding.

**Expected move.** Make adverse energy multiplicative under annular gluing because winding cannot disappear without crossing a charged Voronoi wall.

**Experiment.** Use a six-triangle annulus with at most 18 edge coefficients. Enumerate offsets in \(\{-1,0,1\}\), compute every boundary transfer by SNF and exact CVP, and test two concentric tiles for \(65/64\).

**Falsification / likely death.** Unrestricted negative cochains may unwind locally, or zero winding may encode only parity and therefore be unable to distinguish NAND.

**Obstruction audit.** G1: every edge/carry is charged. G2/G3: SNF plus the Hodge bound covers all cochains. G5: complete boundary cochains are glued. G6: winding is emitted, not filtered. G7: exact cocycles still pay harmonic energy. G9/G11/G12/G13/G15/G19/G32/G37: parity, DROP, affine, laminar, signed, and additive cochains are audited explicitly. G14/G31/G38: no finite-bag/shell/splitter extrapolation. G28: the annular transfer must prove its inequality. G30/GD1/GD2: no tensor, ordered pair, or convolution. G33/G34: no exterior tags or Gram repair.

Classical touchstones only: Conway–Sloane on Barnes–Wall and \(D_4\), Voronoi reduction theory, Schrijver on regular-matroid circuits, Murota on discrete convexity, and discrete Hodge theory.
