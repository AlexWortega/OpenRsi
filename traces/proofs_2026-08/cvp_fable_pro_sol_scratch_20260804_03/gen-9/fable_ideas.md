I use the following obstruction shorthand: **O1** free-slack annihilation; **O2** local isolation failing under overlap; **O3** external filters/reference changes/mod-2 bypass; **O4** exact `011+100−111` zero-residual selector; **O5** seven-term cube-parity/low-degree failure; **O6** signed accepting-path or existential-witness combinations; **O7** unjustified coefficient bounds; **O8** exponential degree/state, zero-preserving tensoring, unspecified topology, or missing composition/dimension-gap law.

### 1. Global PSD metric synthesis

**Core trick.** Abandon residual norms `||Az-b||²`: synthesize a full rational positive-definite Gram matrix \(Q\) and target term so kernel directions of \(A\) can still be expensive. This is metric learning over the complete global selector space, with symmetry constraints imposed only afterward.

**Expected move.** Separate every honest satisfying vector from all short signed-selector vectors, especially the known zero-residual attacks.

**Obstruction audit.** O1: no slack. O2: metric is global, not private-row composition. O3: emitted \(Q=B^TB\) and one fixed target contain every condition. O4–O5: explicitly included as adversarial vectors rather than assumed detectable by moments. O6: no witness equations. O7: positive minimum eigenvalue gives a radius-to-coefficient bound. O8: polynomially describable families and an asymptotic gap remain completely open.

**Falsification/test.** Using the Generation-7 instance, alternate exact sphere enumeration with an SDP maximizing \(d_{\rm bad}/R_{\rm sat}\); include the satisfiable overlapping control. Pass only if the exact unrestricted ratio exceeds 1.1 after rational rounding.

**Smallest experiment.** Start with permutation-invariant block Gram matrices having fewer than 30 parameters.

**Likely death.** Convexity yields a midpoint or short affine combination no PSD metric can separate without equally raising completeness.

---

### 2. Iterated Lawrence lifting of the global selector semigroup

**Core trick.** Apply a two- or three-fold Lawrence lifting to the *global* incidence matrix, duplicating each coefficient into coupled rails whose differences encode the original selector. Toric kernel moves then acquire replicated positive/negative support, potentially making every Graver move much longer while honest Boolean encodings use canonical rails (cf. Sturmfels, *Gröbner Bases and Convex Polytopes*, 1996).

**Expected move.** Turn constant-weight signed-selector circuits into weight growing with the lifting depth, then scale depth polynomially.

**Obstruction audit.** O1: every rail is anchored; no free slack. O2: lift occurs after global overlap composition. O3: all rail equations enter one fixed-target lattice. O4: the known relation is lifted, not reweighted; whether its norm grows is the test. O5: cube parity may lift unchanged—unresolved. O6: signed rail combinations remain possible—unresolved. O7: rail anchors give an explicit ball bound. O8: no theorem yet that polynomial lifting gives a polynomial ratio rather than proportional completeness growth.

**Falsification/test.** Construct \(k=1,2,3\) lifts of the Generation-7 matrix and compute exact minima for the nine-clause instance and satisfiable control.

**Smallest experiment.** Enumerate primitive kernel vectors and Graver elements before running full CVP.

**Likely death.** Lawrence lifting duplicates the attack and the honest baseline at the same rate, leaving a constant ratio.

---

### 3. Voronoi-shell clause gadgets

**Core trick.** Encode the seven satisfying labels as distinct nearest lattice vectors to one clause target, rather than as solutions of common affine equations. Search for a small lattice whose next Voronoi shell contains the forbidden label and all short signed mixtures, then glue clauses through shared geometric projections.

**Expected move.** Exact affine identities cease to be free because equal residual is replaced by unequal distance to a Voronoi center.

**Obstruction audit.** O1: no integer slack. O2: shared-variable projections are present during gadget synthesis. O3: proximity is evaluated in the actual fixed-target CVP. O4: `011+100−111` is required to lie beyond the legal shell. O5: shell geometry is not degree-\(\le2\) moment matching. O6: alternatives are accepted by distance, not affine witnesses. O7: full-rank basis plus a radius gives a rigorous coefficient bound. O8: arbitrary-overlap composition and polynomial shell separation remain unproved.

**Falsification/test.** MILP-search dimensions \(3\!-\!6\), Gram entries in \([-4,4]\), for seven designated nearest points and a second-shell factor at least 2; then compose two overlapping clauses and audit exact CVP.

**Smallest experiment.** Test the OR gadget alone, explicitly including both signed identities from Generations 7–8.

**Likely death.** Gluing creates new nearer lattice vectors, or the unavoidable legal covering radius makes amplification raise completeness equally.

---

### 4. Radius-locked CRT subset-sum compilation

**Core trick.** Compile 3SAT through the classical SAT-to-subset-sum digit construction, but append several redundant prime-modulus checksum blocks. Derive \(|z_i|\le R\) directly from the CVP radius, choose every prime \(q>2R\), and represent carries as anchored lattice coefficients rather than external restrictions.

**Expected move.** Within the certified ball, modular equality becomes integer equality; non-Boolean coefficients cannot hide as multiples of \(q\).

**Obstruction audit.** O1: carries are anchored and charged. O2: checks hash the complete formula, not private clauses. O3: one basis and target include selection, carry, and CRT rows. O4: the known selector identity may still preserve every digit—unresolved and tested directly. O5: not a low-degree moment construction, although cube parity could induce an arithmetic identity. O6: linear carry systems may admit `2P0−P1`; this mechanism is **not** outside that obstruction. O7: the prime choice follows an explicit radius bound. O8: polynomial gap and checksum count remain unproved.

**Falsification/test.** Emit the complete subset-sum lattice for the nine-clause instance and a satisfiable control; use exact CVP to seek any equal-sum non-Boolean vector within the completeness radius.

**Smallest experiment.** Use two primes just above the derived radius and coefficients bounded only by sphere enumeration.

**Likely death.** A signed exact subset-sum solution survives all redundant checks, reproducing the accepting-path obstruction.

---

### 5. Cubic Veronese embedding with bounded-secant avoidance

**Core trick.** Map every local label through the full cubic Veronese map, but tie its singleton, pair, and triple coordinates to one *global* \(O(n^3)\) table. Add a deterministic generic projection chosen to avoid all secants generated by coefficient vectors inside the rigorously derived CVP ball.

**Expected move.** The seven-term cube-parity relation becomes visible in degree three, while generic secant avoidance targets other bounded signed mixtures without enumerating all assignments.

**Obstruction audit.** O1: no slack. O2: triple coordinates are global, not clause-private. O3: projected rows are embedded in one fixed-target basis. O4: cubic coordinates distinguish the three-term attack. O5: full degree three distinguishes the stated parity relation; degree-3 pseudoassignments remain possible. O6: no private witnesses, but higher signed secants remain. O7: projection is valid only after proving the radius bound from positive-definite anchors. O8: avoiding all bounded secants may require too many coordinates, and degree-3 proof-complexity lower bounds still threaten soundness.

**Falsification/test.** Enumerate all selector deviations inside squared norm 80 on the Generation-7 instance, compute their cubic images, and greedily find small integer projection rows separating them; then run exact CVP on both controls.

**Smallest experiment.** One global triple table plus 8–16 projection rows.

**Likely death.** A degree-3 pseudo-distribution or larger-coefficient secant remains exact, forcing growing degree.

---

### 6. Explicit cosystolic replacement complex

**Core trick.** Convert the occurrence graph into a concrete 2-complex: equality edges form the 1-skeleton, and each legal clause label contributes prescribed triangular 2-cells. Apply a fixed replacement product with a small bounded-degree 2-dimensional expander so any nontrivial selector cocycle should have linear support.

**Expected move.** Map a falsified clause to a nonzero cohomology class whose cosystolic expansion yields many Euclidean residual coordinates.

**Obstruction audit.** O1: no slack. O2: the complex is constructed globally. O3: integer boundary matrices and their scaled Euclidean lift enter one target; SNF is diagnostic, not an external filter. O4–O5: outside those assumptions only if the two signed identities map to nontrivial cocycles—this must be checked. O6: no existential witnesses, although boundaries may absorb signed combinations. O7: finite-field coefficients are lifted with an explicit centered range. O8: unlike Generation 8 this specifies cells, but a uniform attachment/cosystolic theorem and dimension-gap law are still missing.

**Falsification/test.** Build the complex for the nine-clause instance, compute SNF over \(\mathbb Z\), cohomology over \(2,3,5\), and the minimum cocycle support; verify a satisfiable control has its canonical boundary witness.

**Smallest experiment.** Use a fixed 6-vertex triangulated expander block per occurrence edge and emit the resulting CVP basis.

**Likely death.** Clause defects are boundaries, or replacement introduces constant-support cocycles, so expansion never activates.
