Below, obstruction codes cover the full proved map:

- **O1** slack annihilation (G1); **O2** local isolation fails under overlap (G5); **O3** external-filter/mod-2 bypass (G6); **O4** exact signed radix kernel (G7); **O5** constant-cost parity/unique-moment attack (G9/11); **O6** clause DROP (G12); **O7** honest-affine-span/hierarchy lift (G13/15); **O8** pair bags lack composition (G14); **O9** signed-flow splicing (G19); **O10** adverse growth no better than legal growth (G28); **O11** seed isometry (G30); **O12** unrestricted tensor entanglement (G30); **O13** additive cross-copy parity/no superadditivity (G32); **O14** cosphere/positive-metric failure (G33/34); **O15** quadratic three-target bound from G35; **O16** nonabelian/algebraic amplification lacks nonzero syndrome; **O17** exact-cocycle blind spot; **O18** Graver components need not remain harmful; **O19** discrepancy arguments fail for signed integers; **O20** affine lifting through digit/carry tables.

### 1. Formula-dependent Delaunay holes

**Mechanism.** Abandon selector residuals: synthesize a lattice whose Voronoi cell directly has assignment-indexed Delaunay vertices, with each clause modifying which vertices remain on the empty ellipsoid. Compose holes by an asymmetric laminated sum designed to multiply NO radial excess while adding YES squared radius.

**Expected move.** A depth-two hole with `R_NO/R_YES>(R_NO/R_YES)_1`, suggesting logarithmic-depth polynomial amplification.

**Obstruction audit.** O1/O4/O5/O7/O16/O20 assume residual, hash, or selector lifts—absent. O2/O8/O9/O17/O18 use local fibers, bags, flows, cochains, or Graver arguments—absent. O3: emit the complete basis and target. O6: no deletable clause block. O11/O12: use neither tensoring nor symmetric seeds. O15: no `s=0,1,2` target scaling. O19: no distributional discrepancy. **Not escaped:** O10/O13 require an actual growth inequality; O14 is precisely the first gate.

**Experiment.** Enumerate upper-triangular integer bases with entries `[-2,2]` in dimension 4–6; solve exact equal-sphere equations for the eight-clause core and control, then enumerate all lattice points through the proposed shell.

**Likely death.** The required Delaunay vertex set is unrealizable, or lamination only adds radial excess.

---

### 2. Nested-code coset leaders rather than compatible syndromes

**Mechanism.** Encode each label as a shortest representative of a coset in a nested Construction-D lattice; consistency identifies cosets, while legality changes the available short leaders. Thus zero syndrome alone is harmless: a signed affine combination must still pay the coset’s exact leader norm.

**Expected move.** Concatenated codes make every illegal coset have leader norm `N^α`, while honest cosets retain norm `O(√N)`.

**Obstruction audit.** O1/O4/O16/O20 amplify residuals only; here distance remains inside a zero-syndrome coset. O2/O8 are replaced by one global code. O3: all parity checks and targets are emitted. O6 is addressed only if puncturing distance survives one erased clause—must test. O9/O17/O18 are inapplicable. O11/O12: no tensor seed. O14: equal honest leader norms need exact certification. O15: no scaled-target interpolation. O19: use an integral coset-leader bound, not nonnegative discrepancy. **Still exposed:** O5/O7 may produce a short leader despite sharing the honest syndrome; O10/O13 need concatenation growth, not assumed.

**Experiment.** Map the eight labels into cosets of the `[7,4,3]` Hamming Construction-A lattice; exhaust all maps modulo automorphisms and solve exact CVP for the nine-clause obstruction/control, including DROP and G13 vectors.

**Likely death.** Too many honest assignments force the harmful affine point into a coset with another short leader.

---

### 3. Hodge-complete mapping cone with primitive penalties

**Mechanism.** Repair the rejected cohomological route by charging all three Hodge pieces: coboundary, harmonic periods, and an explicit minimum-norm primitive for exact cocycles. A mapping-cone variable records `η` with `dη=x`; high-systole covers are intended to make either the class or its primitive long.

**Expected move.** Under a two-sheet cover, every harmful cochain’s combined Hodge energy grows faster than the energy of lifted honest cochains.

**Obstruction audit.** O17’s exact-cocycle hole is explicitly included through the primitive term. O1/O4/O16/O20 do not apply unless the whole chain image vanishes. O2/O8 become global chain statements. O3 requires every chain and primitive coordinate in the CVP. O6 becomes deletion of a cell and must be enumerated. O9 is irrelevant absent path flow. O11/O12 absent. O14 requires equal honest Hodge energy. O15 uses no target scaling. O18/O19 are replaced by deterministic integral Hodge bounds. **Still exposed:** O5/O7 may map the affine pseudodistribution to the zero chain; O10/O13 need cover growth; zero-chain splicing would recreate O4.

**Experiment.** Build the mapping cone of the nine-clause incidence complex on its smallest connected double cover; compute SNF and exact primitive norms for every vector through anchor excess 32.

**Likely death.** The G13 lift is literally zero in every chain coordinate, leaving no primitive to charge.

---

### 4. Sign-monotone regular-matroid kernel

**Mechanism.** Search for a totally unimodular kernel whose shell-relevant harmfulness predicate is a sign-monotone chamber property. Then every harmful kernel vector has a conformal circuit decomposition, and monotonicity forces at least one circuit itself to remain harmful—repairing the precise gap in the rejected Graver argument.

**Expected move.** A high-girth regular matroid would force every harmful circuit to have support `N^α`, yielding comparable Euclidean cost.

**Obstruction audit.** O18 is addressed conditionally by proving harmfulness conformal, not merely invoking decomposition. O1/O4/O5/O7 remain possible only if a short harmful circuit exists—the search targets exactly those. O2 becomes a global matroid-girth condition. O3: the chamber perturbation must be in the Gram matrix, never an external sign filter. O6 is a cocircuit-deletion test. O8/O9/O17/O20 are structurally absent. O11/O12 absent. O14 demands equal-radius certification. O15 does not apply without target scaling. O19 is avoided only if the metric provably confines the entire shell to one chamber. O10/O13 remain unproved growth requirements; O16 reduces to circuit nonvanishing.

**Experiment.** Enumerate rank-4 or rank-5 regular matroids on the 12-column falsified-OR core; test all circuits and exact CVP shells after rational lexicographic Gram perturbations.

**Likely death.** A quadratic metric cannot confine unrestricted lattice points to the needed sign chamber without ruining completeness.

---

### 5. Ideal-class obstruction in an Arakelov lattice

**Mechanism.** Assign Boolean labels to short representatives of ideal classes; clause compatibility is ideal multiplication, and a false global product should land in a nonprincipal class with a large minimum Minkowski norm. Towers of number fields could turn multiplicative ideal norm into polynomial Euclidean separation.

**Expected move.** Even the smallest class-number-two example should separate a legal principal product from an illegal nonprincipal product without residual scaling.

**Obstruction audit.** O1/O4/O20 are absent if multiplication is intrinsic rather than slack-linearized. O2/O8 concern additive local composition, while the proposed invariant is global ideal class. O3 requires a complete integral Minkowski basis. O6 becomes omission of one ideal factor and must be tested. O9/O17/O18/O19 are inapplicable. O11/O12 absent. O14 requires equal norms for all honest class representatives. O15 does not cover multiplicative ideal composition. **Not escaped:** O16’s missing nonzero premise is central; O5/O7 may cancel after additive lattice realization. O10/O13 need a tower norm theorem, and O3 would fail if multiplication were only externally checked.

**Experiment.** In `Q(√−5)`, enumerate short vectors in the principal and nonprincipal ideal lattices, implement one three-label multiplication table, and test every signed coefficient vector in `[-3,3]`.

**Likely death.** Converting ideal multiplication into CVP linear coordinates destroys multiplicativity and restores the G13 affine lift.

---

### 6. Rank-metric barrier against entangled tensor states

**Mechanism.** Revisit powering only after inserting a rank-metric code that makes every non-rank-one integer coefficient matrix expensive. Honest products lie on equal-radius rank-one matrices; malformed or affine-lifted products should acquire rank at least `δm` and therefore large Frobenius energy.

**Expected move.** A two-level emitted instance satisfies `R_NO,2/R_YES,2 > R_NO,1/R_YES,1` after unrestricted matrix enumeration.

**Obstruction audit.** O11 is checked by canonical seed-isometry testing before powering. O12 is the target: the rank-metric block must charge every entangled matrix, not assume rank one. O13 requires strict superadditivity and is the experiment’s criterion. O1/O4/O5/O7/O16/O20 survive only if their lifts remain low rank—explicitly enumerate them. O2/O8/O9/O17/O18 are not used. O3: all rank-code rows are emitted. O6: include zero rows/columns. O10 remains an honest-versus-adverse growth comparison. O14 is an exact common-sphere SDP gate. O15 has no three-target scaling. O19 uses rank distance, not discrepancy.

**Experiment.** Use `4×4` matrices and exhaust small integer parity-check matrices defining a rank-distance-two sublattice; solve exact shells for asymmetric repaired G28 seeds, including every matrix with `ℓ1≤4`.

**Likely death.** The span of the required honest rank-one matrices contains a low-rank entangled shortcut that no compatible linear check can charge.

---

### 7. Sandpile stabilization as the nonlinear step

**Mechanism.** Encode assignments as recurrent configurations of a graph Laplacian lattice. A violated clause injects chips whose unique stabilization odometer should propagate through a large graph, while superstable/recurrent representatives provide a nonlinear canonical choice without introducing multiplication or carry variables.

**Expected move.** On graph lifts, false-clause odometer norm grows as `N^{1/2+α}` while every honest recurrent representative has norm `O(√N)`.

**Obstruction audit.** O1/O4/O16/O20 concern linear residual annihilation; stabilization is performed by nearest representative in a Laplacian coset, not emitted as linear tables. O2/O8 become global critical-group questions. O3: only the Laplacian basis and target may be used—no external stabilization filter. O6 is chip deletion and must still propagate. O9 differs from conserved signed flow because superstable minimality, not acceptance, selects the representative. O11/O12 absent. O14 requires equal-energy honest recurrent states. O15 uses no target scaling. O17 is irrelevant to Laplacian cosets. O18/O19 would be replaced by `M`-convex minimality. **Still exposed:** O5/O7 may occupy the same critical-group class; O10/O13 require genuine odometer growth under graph lifts.

**Experiment.** Attach the eight-clause three-variable core to paths and binary trees of 4–10 nonsink vertices; enumerate each Laplacian coset and exact nearest representatives, including DROP and G13 combinations.

**Likely death.** Stabilization conserves the wrong invariant, placing the affine cheat in a short recurrent class.

Classical hooks: Conway–Sloane, *Sphere Packings, Lattices and Groups* (1999); Schrijver, *Theory of Linear and Integer Programming* (1986); Gabidulin, “Theory of Codes with Maximum Rank Distance” (1985); Neukirch, *Algebraic Number Theory* (1999); Dhar, “Self-Organized Critical State of Sandpile Automaton Models” (1990); Murota, *Discrete Convex Analysis* (2003).
