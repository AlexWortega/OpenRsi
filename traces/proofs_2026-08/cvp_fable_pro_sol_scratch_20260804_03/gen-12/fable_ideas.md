I use the following obstruction names: **G1 slack annihilation; G2 bounded local isolation; G3 exact-but-local affine isolation; G5 private-row overlap kernels; G6 external-filter/reference/mod-2 invalidity; G7 exact zero-residual radix bypass; G9 degree-two cube parity; G11 unique/synchronized cubic parity.**

### 1. Absolute moment registry encoded by an expander code
**Core trick.** Replace pairwise moment comparisons by one absolute integer register \(u_S\) for every relevant squarefree monomial \(S\). Every occurrence writes to \(u_S\), while the whole register vector is systematically encoded by a constant-rate, linear-distance code, so changing even a unique top moment produces many lattice-coordinate changes.

**Expected move.** A seven-term parity must either leave a moment residual or shift a register by a nonzero codeword of weight \(\Omega(N)\).

**Obstruction check.** G1: no slack. G2/G3: registers are global, not fixed local marginals. G5: checks are shared, not private. G6: emit registers, parity symbols, carries, and fixed target; search unrestricted integers. G7: changes the zero fiber rather than reweighting it. G9: includes degree-two registers. G11: unique and synchronized cubic shifts both alter an absolute coded register.

**Falsification.** Find a zero-residual signed selector plus register/codeword shift of \(O(1)\) anchor excess.

**Smallest experiment.** Add degree-\(\le3\) registers and a small systematic binary/BCH code to the nine-clause instance; exact DP through excess 48.

**Likely death.** Fake q-ary registers or carry directions may recreate cheap integral fibers.

---

### 2. Systolic clause complex
**Core trick.** Embed occurrence consistency into a finite 2-complex: deviations are integer 1-chains, consistency rows are boundaries/coboundaries, and extra rows pin a homology basis. Choose a complex with large cosystole, intending that every nontrivial signed-selector chain has support \(\Omega(N)\).

**Expected move.** Local parity circuits become either detectable boundaries or long homology representatives, giving polynomial Euclidean cost.

**Obstruction check.** G1: no slack variables. G2/G3: isolation is supplied by global topology, not one clause. G5: overlap is the complex itself, not private rows. G6: every chain variable and homology pin is embedded in one fixed-target CVP. G7: exact cycles are addressed by systole and homology pins, not radix weights. G9/G11: their seven-term witnesses are local chains; the test asks whether they bound cheaply. Synchronized parity is outside G11’s pairwise setting but may still be a cycle.

**Falsification.** Exhibit a constant-support integral cycle or filling preserving all pins.

**Smallest experiment.** Glue the two-clause overlap gadget to tetrahedral and octahedral complexes; use SNF plus bounded Graver enumeration to find the shortest nonzero pinned cycle.

**Likely death.** Clause gadgets may create constant-size fillings regardless of ambient systole, or the construction may become PCP-like.

---

### 3. Clause-tuple lift with marginal consistency
**Core trick.** Introduce selectors for legal joint labels on \(k\)-tuples of clauses, with all \((k-1)\)-marginalization equations emitted in the lattice. This is an exterior/Sherali–Adams-style lift: a local defect is viewed in every surrounding context rather than only through low-degree moments.

**Expected move.** At \(k=4\), the present degree-three parity should be exposed; a sparse family of contexts might spread one defect over polynomially many rows without listing all tuples.

**Obstruction check.** G1: no slack. G2/G3: tuple variables couple clauses globally. G5: overlap constraints are joint marginals, not private syndromes. G6: all tuple selectors and marginal equations are CVP coordinates. G7: not fully outside—signed pseudo-distributions can still form an exact lifted kernel. G9/G11: levels above their parity degree detect the known witnesses, but higher-degree parity may survive.

**Falsification.** Find a low-anchor signed pseudo-distribution satisfying every lifted marginal equation.

**Smallest experiment.** Build complete \(k=2,3,4\) lifts of the nine-clause instance; compute exact minimum zero-residual anchor excess by DP/SNF.

**Likely death.** Hard unsatisfiable formulas may admit low-level consistent pseudo-distributions, while sufficiently high \(k\) makes dimension superpolynomial.

---

### 4. Tensor-product amplification of an entire CVP quotient
**Core trick.** If a uniform base reduction with ratio \(\gamma>1\) can first be obtained, tensor its centered lattice-target pair and add constraints intended to exclude mixed, non-rank-one lattice vectors. Ideal tensor behavior would turn \(\gamma\) into \(\gamma^t\).

**Expected move.** With \(t=\Theta(\log n)\) and constant branching, amplify a genuine constant quotient gap to \(n^c\).

**Obstruction check.** G1: not outside if the base retains slack annihilation. G2/G3: starts only after a composable global base exists. G5: overlap kernels tensor too unless removed first. G6: tensor basis, target, and rank-enforcement coordinates must all be emitted exactly. G7: an exact base kernel remains exact. G9/G11: their parity vectors also tensor, so this mechanism does not cure them. Its contribution is solely amplification after quotient soundness.

**Falsification.** A mixed tensor lattice vector beats the product of the base minima.

**Smallest experiment.** Tensor the Generation-9 obstruction and control at \(t=2\); run exact bounded CVP and compare with \(96^2\) and \(72^2\).

**Likely death.** Tensor lattices contain short sums of pure tensors, and logarithmic tensor depth may cause superpolynomial dimension.

---

### 5. Algebraic-integer selector fingerprints
**Core trick.** Assign local labels algebraic-integer fingerprints whose conjugate vectors have equal trace norm but are integer-linearly independent up to degree \(d\). Emit field-valued occurrence consistency in an integral basis and all conjugate embeddings; a nonzero algebraic residual has conjugate squared norm at least \(d\) by norm integrality and AM–GM.

**Expected move.** Taking \(d=m^{1+2c}\) could make every bounded-support selector cheat cost enough for an \(m^c\) distance gap.

**Obstruction check.** G1: no slack. G2/G3: fingerprints are shared globally, rather than local measurements. G5: overlap uses the same field coordinates. G6: integral-basis coordinates and fixed target are explicit; no filtered congruences. G7: bounded-support exact relations are removed rather than radix-weighted, but unrestricted long relations remain possible. G9/G11: their support-seven parities are caught when \(d>7\), including synchronized copies.

**Falsification.** Find a short algebraic relation among legal label columns or a residual whose conjugate norm is small relative to completeness.

**Smallest experiment.** Use a degree-11 cyclotomic/trace Gram matrix on the nine-clause instance; enumerate zero relations of support at most ten.

**Likely death.** Equal-norm completeness and global consistency may force relations, while long-support relations may fit inside the soundness radius.

---

### 6. Global PSD circuit-cutting
**Core trick.** Enumerate short harmful integer selector circuits and solve an SDP for an unrestricted cross-clause Gram matrix \(Q\) and center that keep every honest encoding within radius \(R\) but push every known circuit beyond \(\Lambda R\). Alternate exact nearest-vector search with new separating inequalities, then seek a rational, incidence-computable pattern in the resulting dual certificate.

**Expected move.** Determine whether the failure of the two-parameter Generation-9 metric was merely a restricted ansatz or reflects a genuine geometric barrier.

**Obstruction check.** G1: no slack. G2/G3: \(Q\) is global. G5: all overlap circuits enter the cut set. G6: require rational realization, one fixed target, and unrestricted integer auditing. G7: exact residual kernels are separated directly in the ambient metric. G9/G11: explicitly include both parity witnesses and synchronized copies.

**Falsification.** The SDP dual proves \(\Lambda=1+O(1/m)\), or exact search continually finds bounded-cost unseen circuits.

**Smallest experiment.** On the obstruction/control pair, enumerate states through anchor excess 32, maximize \(\Lambda\), rationalize \(Q\), and rerun exact CVP.

**Likely death.** Uniform completeness may geometrically force every polynomial-time-constructible metric to leave a nearby signed combination.

---

### 7. Terminated convolutional consistency code
**Core trick.** Order variable occurrences through a deterministic interleaver and encode assignment/selector transitions as a terminated convolutional trellis. State variables, transition equations, and output checks all enter the lattice; termination is intended to turn any local signed deviation into a long nonzero error event rather than a tail-biting cycle.

**Expected move.** A code with polynomial free distance would make one inconsistent selector corrupt \(\Omega(n^{2c+1})\) zero-baseline output coordinates.

**Obstruction check.** G1: no free residual slack. G2/G3: state memory composes clauses sequentially. G5: shared trellis state replaces private rows. G6: state, termination, and output coordinates are emitted with a fixed target. G7: the mechanism seeks nonzero free distance for the exact kernel, not larger weights on an existing syndrome. G9/G11: parity support is irrelevant if it cannot form a terminated zero-output path; synchronized attacks require a full code cycle.

**Falsification.** Find a constant-weight integral circulation with zero output and zero terminal state.

**Smallest experiment.** Interleave the nine clauses, test all memory-2 and memory-3 binary generators, and compute the shortest signed zero-output event by DP plus SNF.

**Likely death.** Linear trellises may admit cheap signed circulations, while polynomial free distance may require exponentially large state.

**Classical touchstones:** Sherali–Adams (1990) for tuple lifts; Sipser–Spielman (1996) for expander-code distance; Conway–Sloane (3rd ed., 1999) for algebraic/tensor lattices; Lin–Costello (1983) for convolutional free distance.
