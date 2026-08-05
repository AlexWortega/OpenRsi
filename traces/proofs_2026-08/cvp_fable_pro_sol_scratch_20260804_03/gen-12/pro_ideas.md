Below are seven divergent mechanisms. Each changes the underlying enforcement mechanism rather than merely reweighting the killed residuals.

### 1. Construction-A quotient code with internal carries

**Core trick.** Put selector-consistency equations in a Construction-A lattice modulo several small primes, with carry variables included in the emitted lattice. Synthesize parity checks on the quotient of selector vectors by honest-assignment differences, so every low-anchor harmful class has a nonzero modular syndrome that can be polynomially scaled.

**Expected move.** Eliminate all exact low-cost signed kernels; then a single violated syndrome can contribute \(n^{1+2c}\) squared distance while completeness stays \(O(n)\).

**Obstruction check.** G1: carries cancel only multiples of \(p\), not arbitrary residuals. G2–3: uses a global quotient code, not the isolated local fibers. G5: checks span overlapping clauses globally. G6: normalization, congruences, and carries are lattice coordinates under one fixed target. G7: not automatically outside—an exact integer kernel may vanish modulo every chosen prime. G9/G11: checks full selector classes rather than bounded-degree moments, unless their parity vectors lie in the honest-difference quotient.

**Falsification/experiment.** On the nine-clause instance, use CP-SAT to synthesize \(p=3,5\) checks annihilating all honest differences, then exactly enumerate vectors through anchor excess 24.

**Likely death.** The honest-difference module may already contain every cube-parity cheat.

---

### 2. Rooted multiplication closure instead of comparative moments

**Core trick.** Introduce global monomial variables \(y_S\) and four-state truth-table selectors enforcing \(y_{S\cup\{i\}}=y_Sx_i\), rooted at the absolute coordinate \(y_\varnothing=1\). Clause selectors must equal the corresponding rooted monomials, so top moments are pinned absolutely rather than merely compared between occurrences.

**Expected move.** The unique-triple and synchronized-parity attacks should violate a multiplication gadget; amplified gadget rows could then yield a polynomial penalty.

**Obstruction check.** G1: there is no free arithmetic slack. G2–3: Booleanity comes from a global multiplication network, not local affine isolation. G5: shared monomials couple all overlaps. G6: every selector and multiplication equation is emitted in the fixed-target CVP instance. G7: the three-term kernel is charged if it changes any rooted product. G9: degree-two parity must propagate upward. G11: unlike pairwise cubic comparison, even a unique or synchronized cubic is tied to lower-degree absolute data. Higher-degree signed pseudodistributions remain possible.

**Falsification/experiment.** Add all \(y_S\), \(|S|\le4\), and all multiplication tables to the four-variable obstruction; enumerate unrestricted integer states through squared distance 120.

**Likely death.** Closing products to sufficient degree requires exponentially many monomials, while truncated closure admits higher-degree parity kernels.

---

### 3. Cosystolic/Hodge enforcement on a formula complex

**Core trick.** Realize selector deviations as integer cochains on a two- or three-dimensional cell complex built from clause-variable incidences. Penalize both coboundary and adjoint-boundary coordinates, arranging that honest assignments form one affine cohomology class while harmful local deviations must be either nonclosed or large-support nontrivial cocycles.

**Expected move.** A cosystolic lower bound would replace fragile overlap composition by a global statement: every exact residual kernel has support \(N^\delta\), hence large anchor cost.

**Obstruction check.** G1: no slack variables; the measured objects are boundary operators. G2–3: the certificate is global topology, not a constant local fiber. G5: private-clause circuits should acquire boundary or coboundary at adjacent cells. G6: both operators and the affine class are explicit lattice coordinates. G7: a zero raw residual is harmless only if it is harmonic. G9/G11: cube parity becomes a local cochain, independent of moment degree or occurrence multiplicity. A genuine small harmonic cycle would still kill the idea.

**Falsification/experiment.** Glue the nine clause cells through a small triangulated incidence complex; compute Smith normal form and enumerate minimum-support integral harmonic representatives.

**Likely death.** Making an arbitrary formula complex cosystolically expanding without changing satisfiability may itself amount to forbidden gap amplification; torsion may also create short harmonic cheats.

---

### 4. Tensor-power amplification of an affine CVP gap

**Core trick.** Given an affine lattice coset with completeness radius \(R\) and soundness radius \(gR\), form a carefully defined tensor-power coset whose intended distances multiply. Taking \(k=\Theta(\log n)\) would turn any uniform \(g>1\) base gap into a polynomial factor.

**Expected move.** Separate the campaign into a constant-gap base lemma and a purely geometric, PCP-free amplifier.

**Obstruction check.** G1, G5, G7, G9, and G11 are inherited rather than avoided: tensoring cannot repair an exact base cheat. G2–3 therefore provide no adequate base lemma. G6 can be satisfied because the tensor basis and target are explicit; the main issue is unrestricted mixed tensor vectors, not external filtering. Thus this mechanism is only downstream of a sound constant-gap construction.

**Falsification/experiment.** Enumerate all small \(2\)- and \(3\)-dimensional integral affine lattices with a verified gap, tensor-square them, and search for mixed lattice vectors below the predicted product radius. Then tensor-square a compressed version of the Generation-9 metric.

**Likely death.** Mixed tensors collapse the gap, or \(N^k\) becomes quasipolynomial rather than polynomial when \(k=\Theta(\log n)\).

---

### 5. High-Graver-complexity toric coupling

**Core trick.** Treat legal selector tables as fibers of an integer configuration and harmful signed selectors as elements of its toric kernel. Use global Lawrence-type liftings or nested configurations designed so every harmful Graver element has \(\ell_2\)-norm \(N^\delta\), while honest assignments remain short representatives of the target fiber.

**Expected move.** Nonzero residuals are amplified conventionally; exact residual kernels become expensive because their primitive integer circuits are globally long.

**Obstruction check.** G1: no slack cancellation is used. G2–3: this generalizes local affine isolation to a global circuit-length invariant. G5: a single global lifting replaces private rows and freed marginals. G6: the complete integer configuration and target fiber are emitted. G7: its three-term relation is exactly a short toric circuit to forbid. G9/G11: seven-term parity is likewise treated as a circuit regardless of moment degree or synchronization. The mechanism is not outside these obstructions until a growing Graver bound is proved.

**Falsification/experiment.** Use MILP to synthesize bounded-entry configurations for chains of two through five overlapping clauses, maximizing the minimum harmful circuit norm; verify candidates with 4ti2 or exhaustive kernel enumeration.

**Likely death.** Bounded-column overlap matrices may necessarily have constant-size circuits, or the Lawrence lift may enlarge dimension faster than the attainable circuit norm.

---

### 6. Dissociated spherical fingerprints

**Core trick.** Assign each clause-pattern column a constant-norm vector from a \(B_h\)/Sidon-type set, with occurrence-dependent tags constrained to agree on honest overlaps. Legal one-hot choices remain on a common completeness sphere, while every signed combination of at most \(h\) columns has a large nonzero fingerprint.

**Expected move.** Choosing \(h=N^\delta\), or composing several modest-\(h\) families, could force every low-anchor signed cheat to pay a polynomial fingerprint distance.

**Obstruction check.** G1: fingerprints contain no cancellable slack. G2–3: separation comes from additive dissociation, not sparse affine isolation. G5: occurrence tags are global and overlap-aware rather than private. G6: tags, center, and Gram factor are explicit fixed-target coordinates. G7: its three-column relation is directly excluded for \(h\ge3\). G9/G11: fingerprints are not bounded-degree moments, and independent occurrence tags can expose synchronized parity. However, tags must still annihilate or uniformly bound all honest choices.

**Falsification/experiment.** Search integer constant-norm tags in dimensions 4–12 for the nine-clause instance, requiring equal honest radii and maximizing the minimum distance over all signed states of anchor excess at most 24.

**Likely death.** Keeping exponentially many honest assignments near one center may force additive relations that recreate the parity kernels; dimension or coordinate size may also become superpolynomial.

---

### 7. Totally-unimodular branching-flow gadget

**Core trick.** Encode assignment selection as an integral unit flow through a layered branching network, so normalization and local Boolean choice follow from network total unimodularity rather than anchor geometry. Add explicit state transitions that record clause evaluation, and penalize rejecting terminal flow and circulation components.

**Expected move.** Every integral zero-residual vector should decompose into accepting paths plus cycles; unsatisfiability removes accepting paths, while cycle coordinates are made expensive.

**Obstruction check.** G1: no clause slack exists. G2–3: integrality derives from a network matrix, not local fiber certificates. G5: overlap is represented by one global path state. G6: conservation, start/end demand, and rejection coordinates are all inside the fixed-target lattice. G7: signed selectors become path/cycle flows rather than arbitrary local combinations. G9/G11: no moment comparisons are used. However, adding variable-reuse consistency may destroy total unimodularity and restore short cycles.

**Falsification/experiment.** Build the exact layered network for the four-variable nine-clause obstruction, emit its lattice, and enumerate all flows below the Boolean baseline plus 24; explicitly classify every zero-residual circulation.

**Likely death.** A polynomial-width state graph cannot remember enough clause information, while compact consistency side constraints break total unimodularity and reintroduce the old signed circuits.

**Classical pointers:** Conway–Sloane, *Sphere Packings, Lattices and Groups* (Construction A); Sherali–Adams (1990) for multiplication hierarchies; Sturmfels, *Gröbner Bases and Convex Polytopes* (1996) for toric/Graver methods; Bose–Chowla (1962/63) for \(B_h\) sets; Gromov (2010) for cosystolic expansion.
