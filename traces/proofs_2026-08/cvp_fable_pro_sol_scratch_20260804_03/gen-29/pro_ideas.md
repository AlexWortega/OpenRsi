Below are seven unpromoted, genuinely different mechanisms. Each begins with an exact finite falsifier; none relies on PCP sampling—all proposed checks are emitted explicitly.

### 1. Secant-resistant nonlinear evaluation lift

**Core/expected move.** Map each local assignment to a deterministic finite-field Veronese/evaluation vector, realized with pair- and triple-selector variables. Seek a lifted code whose low-weight signed secants have nonzero syndrome; once the audited shell has no kernel, scale syndrome rows by \(n^K\).

**Obstruction audit.** G1: no slack. G2/G3 and G5: global nonlinear lift, not fixed-marginal private matrices. G6: every row and anchor is emitted. G7: the three-term kernel should fail higher evaluations. G9/G11: degree exceeds the observed parity moment. G12: replicated normalization charges drops. G13: raw affine-span collision is outside assumptions because encoding is nonlinear/enlarged, although a lifted collision may recur. G14: adds secant distance beyond pair marginals. G15: no affine hierarchy propagation. G19: no path flow. G28: no identity-seam min-plus recursion.

**Smallest experiment.** On the nine-clause fixture, use overlapping pair selectors and degree-4 evaluations over \(\mathbb F_{17}\); exhaust the exact \(B+32\) shell and compare the control.

**Falsification.** Any zero-syndrome lifted G11 combination, clause drop, or control minimum above baseline.

**Likely death.** A low-degree pseudodistribution survives every polynomial-size lift.

---

### 2. Nullstellensatz dual separator compiled into CVP

**Core/expected move.** Form the Boolean clause ideal using \(x_i^2-x_i\) and clause-falsity polynomials. An explicit identity \(1=\sum q_jf_j\) becomes a dual linear separator: normalization plus all Macaulay rows cannot vanish simultaneously, so residual scaling yields the gap.

**Obstruction audit.** G1: no slack variables. G2/G3/G5: certificate is formula-global, not local affine isolation. G6: Macaulay rows and normalization are lattice coordinates. G7: exact selector kernels do not imply annihilation of the polynomial ideal. G9/G11: their moment kernels apply only below certificate degree. G12: dropping a clause violates an included normalization/ideal row. G13: monomial lifting is nonlinear relative to raw selectors. G14/G15: no bag or hierarchy composition assumption. G19: no flow representation. G28: no tile recurrence.

**Smallest experiment.** For all eight clauses on three variables, compute the minimum-degree rational certificate, clear denominators, transpose its Macaulay matrix into a CVP objective, and exactly enumerate the unrestricted minimum.

**Falsification.** A normalized zero-residual moment vector, or certificate coefficients making soundness scaling larger than polynomial bit complexity.

**Likely death.** General formulas require exponential degree, monomial count, or coefficient size—matching algebraic proof-complexity lower bounds.

---

### 3. Twisted-holonomy obstruction with an expander sheet code

**Core/expected move.** Interpret variable choices as transports in a finite nonabelian group and clauses as prescribed 2-cell holonomies. Replace each group state by a coded sheet indicator on a Cayley expander; nontrivial total holonomy should force disagreement on many sheets rather than permit a local signed splice.

**Obstruction audit.** G1: no clause slack. G2/G3/G5: constraints live on a global 2-complex, not private marginal rows. G6: all edge, face, and sheet checks are emitted. G7 and G9/G11: additive selector kernels need not preserve noncommutative holonomy. G12: every face has replicated normalization. G13: raw affine hashes do not cover nonlinear multiplication-table states, though signed sheet mixtures remain possible. G14/G15: neither pair bags nor laminar marginals. G19: outside first-order unit-flow assumptions because faces constrain products and coded sheets. G28: no min-plus seam recursion.

**Smallest experiment.** Encode the eight-clause, three-variable obstruction with \(S_3\), six sheets, and all multiplication-table selectors; use MILP/SNF plus exact shell enumeration to seek zero-residual signed 2-chains.

**Falsification.** Any accepting integral chain with one or two negative coefficients or trivial coded holonomy.

**Likely death.** Linearized nonabelian states admit signed representation-ring cancellations analogous to G19 splicing.

---

### 4. Homogenized tensor-gap amplification with flattening checks

**Core/expected move.** Homogenize a finite YES/NO affine CVP gadget and recursively tensor it, adding antisymmetric flattening rows intended to force every short vector near a rank-one tensor. If distances multiply while a constant-size port alphabet suffices, depth \(\Theta(\log n)\) gives polynomial gap and polynomial dimension.

**Obstruction audit.** G1/G7: no residual radix or slack. G2/G3/G5: does not compose private affine fibers. G6: tensor and flattening rows are explicit. G9/G11: constant-cost parity should tensor into growing cost only under rank-one rigidity. G12: drops become non-rank-one boundary states. G13: not safely outside—affine collisions may generate entangled short tensors. G14 supplies a possible seed but proves no tensor law. G15: no laminar lift. G19: no flow. G28 tested identity-seam min-plus composition, not Euclidean Kronecker composition with flattening constraints.

**Smallest experiment.** Tensor two eight-coordinate depth-one G28 tiles into 64 coordinates, add all \(2\times2\) flattening minors via explicit pair selectors, and exactly compute legal/adverse minima through the first two shells.

**Falsification.** Ratio fails to square, control radius grows too quickly, or an entangled signed vector beats rank-one witnesses.

**Likely death.** Tensor lattices contain unexpectedly short non-simple vectors; linearized minors admit pseudotensors.

---

### 5. Multi-prime canonical-residue and carry avalanche

**Core/expected move.** Replace each vulnerable coefficient by one-hot canonical residues modulo several coprime primes, exact quotient/carry equations, and low-degree residue moments. Honest \(0/1\) values have zero carries; a negative selector should expose forbidden residues or signed mass in many independently repeated blocks.

**Obstruction audit.** G1: attacks coefficient range, not clause residual slack. G2/G3/G5: global CRT agreement replaces local marginal isolation. G6: residues, carries, and legality costs are all emitted. G7: its \(-1\) coefficient is precisely the intended trigger. G9/G11: residue moments differ from global squarefree moments. G12: each block has normalization, so dropping is replicated. G13 is not automatically escaped: affine combinations of honest residue encodings may lift exactly; this is the primary audit. G14/G15: no pair-mesh or hierarchy claim. G19: no flow. G28: no recursive tile growth assumption.

**Smallest experiment.** Apply primes \(3,5,7\) and degree-two residue moments to the G7 falsified clause; enumerate all coefficients permitted below squared distance 120 and compare against honest \(0/1\) residues.

**Falsification.** A common signed residue measure such as an affine combination of \(\delta_0,\delta_1\) satisfying every CRT block.

**Likely death.** Canonical range is nonlinear; its linear one-hot formulation recreates the G13 affine pseudodistribution.

---

### 6. Higher-window algebraic transcript code

**Core/expected move.** Scan variables and clauses through a nonlinear finite-state recurrence, then encode every overlapping length-2 and length-3 transition window with a deterministic convolutional/tree code. Unlike unit flow, consistency is imposed on windows and repeated algebraic state hashes; a splice should corrupt a linear number of windows.

**Obstruction audit.** G1: no slack. G2/G3/G5: transcript-global rather than private clause matrices. G6: every window is included, with no filtered acceptance. G7 and G9/G11: local selector kernels need not form a valid coded transcript. G12: omitted windows violate several normalizations. G13: raw affine collision is outside the nonlinear state lift, but affine combinations of complete transcripts remain dangerous. G14/G15: no bag mesh or laminar propagation. G19’s obstruction applies to first-order signed unit flows; higher windows are outside its stated encoding, though signed transcript cycles may reproduce it. G28: no min-plus identity seam.

**Smallest experiment.** On the four-variable nine-clause fixture, use \(\mathbb F_5\), update \(h\mapsto h^2+a\), enumerate all length-3 state windows, and solve the exact unrestricted shell through two negatives.

**Falsification.** A zero-residual accepting signed transcript or two distinct transcripts with identical window code.

**Likely death.** State space explodes, or signed de Bruijn cycles splice consistently despite higher windows.

---

### 7. Deep-hole cosets with discriminant-code gluing

**Core/expected move.** Encode each truth value by selected nearest vectors to a deep hole of a small lattice, and glue variable/clause gadgets through discriminant-group cosets protected by an outer code. Honest assignments use designated minimal representatives; malformed signed selectors should enter a nontrivial coset whose code distance spreads the defect before residual weighting.

**Obstruction audit.** G1: no integer slack. G2/G3/G5: geometry is coset gluing, not sparse measurement isolation. G6: the full glued basis and target are emitted. G7: its exact selector kernel may still become a short coset vector—so G7 is not automatically escaped and must be enumerated. G9/G11: no low-degree moment metric. G12: deleting a gadget changes its discriminant syndrome. G13: raw compatible linear hashes do not directly cover enlarged coset representatives, but an affine lattice collision may persist. G14/G15: no pair-bag or hierarchy lift. G19: no accepting flow. G28: no min-plus recursion unless gluing is later iterated.

**Smallest experiment.** Use the Construction-A lattice of the binary \([8,4,4]\) code for two overlapping OR clauses; choose two nearest-vector cosets as truth labels and enumerate all vectors through three shells.

**Falsification.** Any undesignated nearest vector, G7-style signed combination, or control-radius inflation eliminating the shell gap.

**Likely death.** Deep holes have extra nearest vectors, and triangle-inequality bounds prevent more than constant local separation.

**Classical ingredient references:** Reed–Solomon, *J. SIAM* 8 (1960), 300–304; Alon, *Combinatorial Nullstellensatz*, CPC 8 (1999); Sipser–Spielman, *Expander Codes*, IEEE TIT 42 (1996); Schulman, *Coding for Interactive Communication*, IEEE TIT 42 (1996); Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. No external search or prohibited material was used.
