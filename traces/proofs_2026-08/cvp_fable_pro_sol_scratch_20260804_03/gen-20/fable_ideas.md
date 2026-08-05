Below are six deliberately nonconvergent Generation-20 mechanisms. Each changes the underlying enforcement principle rather than patching a recovered witness.

### 1. Logarithmic expander bags with Reed–Muller uncertainty

**Mechanism.** Introduce assignment selectors on \(k=\lceil C\log m\rceil\)-variable bags chosen as a nonlaminar overlap expander, and equate complete overlap marginals. Integer Reed–Muller/Möbius bounds suggest that a nonzero signed measure invisible on all proper marginals must have \(2^{\Omega(k)}\) squared mass.

**Expected move.** With zero-centered one-hot costs, every exact signed pseudosection costs \(m^{\Omega(1)}\); weighted nonzero residuals cost still more.

**Map check.** G1: no slack. G2–3/G5: not fixed-marginal private hashes. G6: all constraints are emitted. G7: exact kernels are attacked by mass. G9/G11: degree grows logarithmically. G12: clauses occur in many bags. G13: not a raw-selector linear hash, although affine lifts remain possible. G14: higher-than-pair bags plus an asymptotic claim. G15: nonlaminar expansion, but its affine pseudodistribution is a direct threat. G19: no flow encoding.

**Falsification.** A zero-residual obstruction vector with \(O(1)\) excess.

**Experiment.** Add one four-variable bag to the G14 instance; exact-search through excess 64 and verify the matched control.

**Likely death.** Obtaining the required overlap expansion with polynomial size may secretly require a direct-product/PCP theorem.

---

### 2. Higher Lawrence lifting and Graver-type mass growth

**Mechanism.** Start with a Generation-3 isolating matrix and apply iterated higher Lawrence lifting: copies share their original image while new rows record hierarchical differences. Certain Lawrence configurations have Graver elements whose number of active layers grows rapidly; choose \(r=\Theta(\log m)\).

**Expected move.** Honest diagonal sections remain sparse, while every harmful exact fiber requires polynomially many nonzero or negative coefficients.

**Map check.** G1: no slack. G2–3 are the seed, not repeated unchanged. G5: freed marginals are globally coupled by lift rows. G6: unrestricted emitted CVP only. G7: targets exact kernel vectors. G9/G11: parity must become a high-type Graver element. G12: layer drops violate difference rows. G13: outside raw hashing, but its affine combination may lift diagonally. G14: no pair-bag assumption. G15: algebraic lifting rather than laminar marginals. G19: no network flow.

**Falsification.** Any bounded-type harmful Graver move persisting for all tested lift levels.

**Experiment.** For each of the 18 survivors, construct levels \(r=2,3\) on the representative two-clause overlap and find the shortest harmful fiber using SNF plus branch-and-bound.

**Likely death.** Graver complexity gives possible large elements, not a lower bound on all harmful ones; the G13 affine collision may survive unchanged.

---

### 3. Exterior-power/Plücker consistency lift

**Mechanism.** Represent separator marginals by joint tables and append their \(\bigwedge^2,\bigwedge^3,\ldots\) signatures using explicit pair- and tuple-selector variables. Honest sections are decomposable and agree in every exterior degree; signed splices preserving first marginals generally create a nonzero minor discrepancy.

**Expected move.** Iterating exterior degree to \(O(\log m)\) should force either a detectable residual or polynomial support in any exact extension.

**Map check.** G1: no slack. G2–3/G5: compares global higher-order decomposability, not private marginals. G6: products are represented by emitted joint selectors, never externally checked. G7: first-order zero kernels may acquire exterior residuals. G9/G11: not bounded-degree global moments. G12: normalization is replicated across exterior levels. G13: nonlinear in raw selectors, but affine combinations of fully lifted honest points remain dangerous. G14: adds determinant compatibility beyond pair marginals. G15: nonlaminar, though affine threading may recur. G19: no paths or flows.

**Falsification.** A constant-excess signed vector satisfying every lifted Plücker row.

**Experiment.** Lift only the G7 three-term and G11 seven-term witnesses through all pair/triple joint tables on four variables; search excess at most 32.

**Likely death.** Linearizing multiplication also linearizes affine mixtures, allowing the same pseudodistribution in a larger space.

---

### 4. Cosystolic sheaf encoding on a bounded-degree complex

**Mechanism.** Place legal local assignments in stalks of a two-dimensional cell complex; restriction maps become integer coboundary rows, while homology coordinates distinguish global sections. An explicit cosystolic expander could force every non-global integral pseudosection to have linear support even when its local coboundary vanishes.

**Expected move.** Short satisfiable sections have one label per cell; exact unsatisfiable sections have \(\Omega(N)\) negative mass, while nonzero coboundaries can be polynomially weighted.

**Map check.** G1: no slack. G2–3/G5: global topology replaces private overlap rows. G6: coboundary and homology coordinates are emitted. G7: zero residual becomes a large cocycle rather than a local kernel. G9/G11: no moment truncation. G12: dropping a face creates boundary. G13: raw affine hashing is irrelevant, although affine global cocycles remain possible. G14: uses higher-dimensional incidence, not complete pair bags. G15: cycles are nonlaminar. G19: no conservation flow, though signed cycles are the analogous threat.

**Falsification.** A non-global cocycle of constant support or a small torsion class.

**Experiment.** Build a tetrahedral four-variable complex with nine clause-face gadgets; compute integral homology by SNF and exactly enumerate the shortest illegal cocycle.

**Likely death.** Embedding arbitrary formulas may destroy cosystolic expansion or amount to PCP-style gap amplification.

---

### 5. Cyclotomic dissociation and algebraic-norm barriers

**Mechanism.** Tag local choices by powers of an algebraic integer \(\theta\) of degree \(D=m^{\alpha}\), and propagate tags through a balanced multiplication-table lift. Any short unintended cancellation would give a polynomial of degree \(<D\) vanishing at \(\theta\); algebraic norm bounds then force either a nonzero residual or a relation comparable to the minimal polynomial.

**Expected move.** Honest assignments cancel exactly, whereas exact signed cheats require \(\Omega(D)\) coefficient mass, yielding a polynomial distance gap.

**Map check.** G1: no additive slack. G2–3/G5: consistency is global arithmetic. G6: all table variables and conjugate coordinates are emitted. G7: zero kernels need long algebraic relations. G9/G11: not low-degree moments. G12: augmentation rows penalize omission. G13: not a compatible linear hash of 72 selectors, though affine lifted relations may persist. G14: no fixed pair-bag premise. G15: product tree differs from marginal hierarchy, but affine threading is possible. G19: no flow, though signed table splicing is analogous.

**Falsification.** A constant-mass exact algebraic cancellation.

**Experiment.** Use \(R=\mathbb Z[t]/(t^4+t^3+t^2+t+1)\) on the nine-clause instance; emit trace-Gram coordinates and search exact fibers through excess 32.

**Likely death.** Signed multiplication-table pseudodistributions may splice inconsistent products and annihilate every algebraic coordinate.

---

### 6. Rank-marked Voronoi tensor amplification

**Mechanism.** Take a constant-size CVP gadget with exact ratio \(\rho>1\), tensor it \(k=\Theta(\log m)\) times, and add marker lattices intended to force every short vector to be rank one across tensor factors. If rank-one rigidity holds, completeness and soundness tensor multiplicatively, producing \(\rho^k=m^{\Omega(1)}\).

**Expected move.** Convert a finite constant-factor survivor into a polynomial gap without clause-repetition or residual coding.

**Map check.** G1: no slack. G2–3/G5: geometric composition rather than private affine composition. G6: rank markers are lattice coordinates, not filters. G7: a zero kernel must remain short after tensoring, so it is explicitly tested. G9/G11: their parity vectors become candidate entangled tensors. G12: drops need not tensor coherently. G13: affine collisions may create entangled short vectors—unresolved. G14 supplies only inspiration, not an assumed theorem. G15: no hierarchy. G19: no flow.

**Falsification.** Any non-rank-one tensor vector beating the intended soundness radius.

**Experiment.** Tensor-square one 12-column G3 survivor, add \(2\times2\) flattening markers, and enumerate coefficients in \(\{-1,0,1\}\) against all rank-one candidates.

**Likely death.** CVP distance is generally not multiplicative under tensor products; entangled lattice vectors probably dominate.

Classical touchstones: MacWilliams–Sloane, *The Theory of Error-Correcting Codes* (1977); Sturmfels, *Gröbner Bases and Convex Polytopes* (1996); Santos–Sturmfels, “Higher Lawrence Configurations” (2003); Evra–Kaufman, “Bounded Degree Cosystolic Expanders” (2018); Neukirch, *Algebraic Number Theory* (1999).
