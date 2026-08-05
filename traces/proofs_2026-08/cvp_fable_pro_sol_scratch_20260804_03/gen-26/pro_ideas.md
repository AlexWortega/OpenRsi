Generation 26 treats G2/G3 as local positive certificates, not obstructions. The relevant obstruction map is G1, G5–G7, G9/G11–G15, G19, and the G20/G21/G22 scaling–entanglement warnings summarized in the Generation-25 gate.

1. **Large-trade spherical design lift**

**Core trick.** Replace each local label by an equal-weight incidence vector from an explicit block design. Honest assignments remain equidistant from the target, while a signed affine mixture preserving marginals becomes a combinatorial trade; the aim is a design family whose shortest relevant trade has polynomial support.

**Expected move.** Turn G13’s constant-support affine collision into anchor excess \(N^\alpha\), with drops separately normalized in every design layer.

**Obstruction check.** G1: no slack. G5: shared-design composition must be tested, not assumed. G6: emit all anchors and rows. G7 and G13/G15: collisions still exist linearly; only their norm may grow. G9/G11: bounded-strength designs retain higher-parity blind spots. G12: replicated normalization prices drops. G14: no extrapolation from one shell. G19: not a flow, but arbitrary signed trades remain. G25: the linear-tag objection applies algebraically; degree, Lawrence, Plücker, and coefficient-box objections do not. G20/G21 scaling and G22 entanglement remain open.

**Smallest experiment.** Map the 16 four-variable assignments to cyclic constant-weight length-31 words; lift the nine-clause instance and exactly score G7/G11/G13, all drops, and the unrestricted shell.

**Falsification/death.** A short trade or baseline growing as fast as trade cost.

2. **Discriminant-group lattice gluing**

**Core trick.** Assign each legal port state to an equal-radius coset of \(L^*/L\). Glue child lattices only through an isotropic subgroup representing semantically compatible port pairs; incompatible pairs should occupy cosets with increasing minimum norm under recursive tensor/glue composition.

**Expected move.** Obtain a depth recurrence in which illegal coset distance grows faster than the honest covering radius.

**Obstruction check.** G1: no slack. G5: overlap is the glue operation itself, but still needs depth-two verification. G6: the glued basis and target are explicit. G7 and G13/G15: signed combinations may land in the zero coset, so they are not excluded automatically. G9/G11: parity may be invisible in the discriminant quotient. G12: reserve and price a distinct drop coset. G14: recursive closure, not its finite pass, is required. G19: no conservation flow, although signed lattice combinations remain. G25: outside degree/tag/Lawrence/Plücker proposals; directly exposed to the G22 entangled-vector objection. G20/G21 require a proved recurrence.

**Smallest experiment.** Use \(A_1^r\) with discriminant group \((\mathbb Z/2)^r\), encode one two-clause overlap gate, glue two levels, and exactly enumerate every vector through the control-plus-32 shell.

**Falsification/death.** An entangled vector is shorter than every cosetwise composition.

3. **Toric fiber product with Graver-distance pricing**

**Core trick.** Represent legal local states as Hilbert-basis columns of an affine semigroup and compose overlaps by toric fiber products. Choose the half-integral target so low-energy integer points should lie near the nonnegative semigroup; every signed cheat is then a Graver move whose support one tries to force to grow with composition depth.

**Expected move.** Prove a polynomial lower bound on the anchor cost of any semantics-changing Graver move.

**Obstruction check.** G1: no free slack. G5: toric fiber product explicitly models overlap, but cheap lifted circuits may persist. G6: all homogenizing coordinates are emitted. G7, G9/G11, and G13/G15 become candidate Graver moves rather than vanishing residuals; none is automatically defeated. G12: homogenization prices missing mass. G14: its finite shell supplies a possible base fiber only. G19: network factors would reproduce signed flows, so avoid or audit them. G25: not a Lawrence lift, bounded search, degree truncation, or Plücker map; the Lawrence-style bounded-type warning may nevertheless recur as bounded Markov complexity. G20/G21/G22 remain unproved.

**Smallest experiment.** Build the toric fiber product of two overlapping OR-clause tables; use `4ti2` or exact enumeration to compute its Graver basis and anchor costs, then add a third clause.

**Falsification/death.** A bounded-support Markov move survives every depth.

4. **Canonical \(p\)-adic carry ladder**

**Core trick.** Give every selector several coprime residue representations with explicitly anchored digits and carries. Honest \(0/1\) selectors use zero upper carries; the hoped-for property is that a negative coefficient or inconsistent signed splice must create a long, increasingly weighted carry cascade in at least one prime tower.

**Expected move.** Charge G7/G19-style coefficients superlinearly while adding little or no upper-level completeness cost.

**Obstruction check.** G1: dangerous—unrestricted carries may recreate the exact slack annihilation, so canonicality must follow from distance, not an external rule. G5: towers share actual occurrence variables. G6: every digit/carry is a lattice coefficient. G7 and G13/G15: zero semantic residual no longer implies zero carry cost, if canonicality works. G9/G11: parity with only \(\pm1\) coefficients is the critical test. G12: zero selectors must still pay normalization. G14: unrelated finite pass. G19: designed against negative coefficients but not proved. G25: outside tags, Lawrence, degree, and minors; the semigroup-enforcement criticism applies directly. G20/G21 scaling is only prospective; G22 requires unrestricted enumeration.

**Smallest experiment.** Freeze primes \(2,3\), three carry levels, and the G7 clause gadget; emit HNF and exactly optimize all digits/carries using an eigenvalue-derived coefficient bound.

**Falsification/death.** A noncanonical low digit absorbs \(-1\) with constant cost—essentially G1 again.

5. **Relative-homology and cosystolic expansion**

**Core trick.** Compile labels into relative \(d\)-chains whose boundaries are variable ports. Honest assignments represent a prescribed relative homology class; unsatisfiability should force any representative either to break a boundary row or to contain a large nontrivial cycle in an explicit cosystolically expanding complex.

**Expected move.** Translate soundness into a systolic lower bound on chain support, rather than residual amplification.

**Obstruction check.** G1: no slack. G5: overlaps are boundary identifications, though local cycles may appear after gluing. G6: all boundary maps and the target class are emitted. G7: exact kernels become cycles and are charged only if systolic. G9/G11: parity chains may be small boundaries. G12: deleting a clause creates an exposed boundary, which must be expensive. G13/G15: affine combinations remain signed chains and may be null-homologous. G14: gives no systolic theorem. G19: \(d=1\) reproduces signed flow, so the mechanism requires genuinely higher dimension; higher-dimensional splicing is still possible. G25: outside tags/Lawrence/degree/minors, but its group-flow and unspecified-complex criticisms apply. G20/G21/G22 demand a recursive systolic and entanglement proof.

**Smallest experiment.** Build a two-dimensional complex for two overlapping clauses, enumerate relative 2-chains through support eight, and explicitly inject the G13 and G19 attacks.

**Falsification/death.** Semantic inconsistencies are filled by constant-area signed surfaces.

6. **Algebraic-integer trace-norm fingerprints**

**Core trick.** Label local states by algebraic integers of equal trace norm and realize the trace form as a rational Euclidean Gram matrix. Tensor independent field embeddings for \(O(\log n)\) levels; a harmful affine combination that is always a nonzero nonunit could then acquire multiplicative norm growth while honest roots of unity retain equal radius.

**Expected move.** Replace linear-code distance by the product formula and algebraic norm, seeking a polynomial trace-norm ratio.

**Obstruction check.** G1: no slack. G5: field labels do not themselves ensure overlap composition. G6: a rational sum-of-squares factor must be emitted, not merely an irrational Minkowski embedding. G7 and G13/G15: affine combinations remain affine combinations and may equal zero or a unit. G9/G11: parity is exactly such a possible zero. G12: equal-radius labels recreate the drop dilemma unless normalization is separately weighted. G14: unrelated finite pass. G19: signed splices may map to units. G25: the fixed-linear-tag objection applies; degree, Lawrence, box, and Plücker objections do not. G20/G21 tensor scaling and G22 entangled tensors remain open.

**Smallest experiment.** Use \(\mathbb Q(\zeta_5)\), assign eight clause labels to small cyclotomic integers, and exhaustively search assignments for a labeling that makes G7/G11/G13 nonzero nonunits while pricing every drop.

**Falsification/death.** Some attack maps to zero or a norm-one unit.

7. **Finite-state min-plus recursion contract**

**Core trick.** Treat a fully emitted base CVP gadget as a finite cost function on bounded port targets. Orthogonally compose two copies with explicit glue coordinates, compute the exact unrestricted min-plus transfer operator, and search for an invariant finite state set satisfying a recurrence \(\Delta_{h+1}\ge\lambda\Delta_h\) while \(B_{h+1}\le\mu B_h\), with \(\lambda/\mu>1\).

**Expected move.** Convert the G14 finite shell into a machine-checkable recursive gap theorem rather than extrapolating it.

**Obstruction check.** G1: no slack unless present in the frozen base. G5: depth-two overlap is exhaustively included. G6: basis, target, Gram factor, and coefficient bound are emitted. G7, G9/G11, G12, G13/G15, and G19 are explicit port-state classes, including signed and drop states. G14: used only as a candidate base, not as proof. G25: this is the requested repaired recursive-port direction, avoiding group tags, Lawrence lifts, degree truncation, Plücker maps, and arbitrary coefficient boxes. G20/G21 are exactly the recurrence obligation; G22 is handled only if the unrestricted composed fiber closes on the state set.

**Smallest experiment.** Freeze a two-clause pair-bag base, radius \(B+16\), derive coefficient bounds from \(\lambda_{\min}\), and enumerate every depth-two port fiber.

**Falsification/death.** State explosion, an unlisted entangled minimum, or \(\lambda\le\mu\).

Classical background only: Conway–Sloane, *Sphere Packings, Lattices and Groups* (1999), for lattice gluing; Sturmfels, *Gröbner Bases and Convex Polytopes* (1996), and Sullivant, “Toric Fiber Products” (2007), for toric/Graver terminology.
