No mechanism below is promoted beyond a falsifiable sketch.

### 1. BCH-sketched high-degree moments

**Core trick.** Extend Generation 9 from degree-two moments to compressed degree-\(d\) fingerprints. Use deterministic splitters plus BCH parity checks (Hocquenghem 1959; Bose–Chaudhuri 1960) so every signed selector measure of support at most \(s\) is detected without explicitly storing all \(n^d\) monomials.

**Expected move.** Cubic fingerprints immediately charge the seven-term cube-parity vector; choosing \(s=n^\alpha\) could force any exact kernel to have polynomial support, paid against only \(O(n)\) shared-variable anchors.

**Obstruction audit.** G1: no free slack. G2–3: global fingerprints, not fixed local marginals. G5: a one-clause circuit changes a global sketch unless genuinely high-support. G6: fingerprints, normalization, and consistency must all be emitted lattice rows. G7: not radix amplification; exact zero kernels remain the decisive risk. G9: cubic rows explicitly detect its degree-two parity kernel. Polynomial-gap law is still unproved.

**Falsification.** Find any bounded-support signed vector annihilating all selected moments, especially a four-dimensional cube parity.

**Smallest experiment.** Add all cubic moments, then BCH-compressed quartic moments, to the existing nine-clause instance; compute unrestricted minima for it and the satisfiable control.

**Likely death.** Degree-\((d+1)\) cube parities survive, while taking \(d\) large destroys polynomial dimension.

---

### 2. High-cosystole overlap complex

**Core trick.** Replace private clause rows by a global chain complex: variable occurrences are vertices, consistency defects are edges, and selector-parity defects are 2-cochains. Attach an explicit expander-code or high-systole complex so every nontrivial defect has support \(\Omega(M)\), using a direct systolic inequality rather than a PCP theorem (compare Sipser–Spielman, 1996).

**Expected move.** A one-clause signed circuit must either become a boundary charged locally or propagate across \(\Omega(M)\) cells. With \(M=n^{1+2c}\) zero-cost checks and \(O(n)\) completeness anchors, this suggests an \(n^c\) distance ratio.

**Obstruction audit.** G1: no slack. G2–3: isolation is global and topological. G5: specifically targets clause-supported overlap circuits. G6: chain equations and targets are internal coordinates. G7: exact cycles, not residual magnitude, are audited. G9: the cube parity must map to a nonzero 2-cohomology class; otherwise this route is not outside that obstruction. Scaling depends on an explicit cosystole bound.

**Falsification.** Compute a constant-support integral cycle or boundary realizing the known parity cheat.

**Smallest experiment.** Place the nine clauses on a small lifted incidence graph; enumerate integral chains of norm at most 32 and compute SNF homology.

**Likely death.** Local parity defects remain cheap boundaries, or the required explicit complex effectively reintroduces PCP-style gap amplification.

---

### 3. Nullstellensatz/Macaulay dual barrier

**Core trick.** Encode \(x_i^2-x_i=0\) and each falsifying clause polynomial in a degree-\(D\) Macaulay matrix. For an unsatisfiable formula, a Nullstellensatz identity \(1=\sum f_jg_j+\sum h_i(x_i^2-x_i)\) becomes a dual-lattice separator; satisfying evaluations remain primal near-vectors.

**Expected move.** Spread the Macaulay residual through a code so a bounded-height dual certificate forces polynomial Euclidean distance, without identifying which clause an assignment violates.

**Obstruction audit.** G1: no clause slack. G2–3 and G5: the certificate is formula-global, not composed local isolation. G6: every monomial, Boolean equation, and code row must appear in the emitted basis; no “pseudoevaluation” filter is allowed. G7: an exact selector kernel survives only if it also annihilates the polynomial ideal rows. G9: degree \(D\ge3\) detects the cube-parity functional. No general polynomial degree/height bound is known, so the asymptotic obstruction remains.

**Falsification.** Exhibit a low-norm integral pseudoevaluation satisfying all truncated rows, or show the dual certificate gives no metric lower bound.

**Smallest experiment.** Build degree-3 through degree-5 Macaulay lattices for the all-eight-clause core and the nine-clause instance; solve exact CVP and extract dual witnesses.

**Likely death.** Required Nullstellensatz degree or coefficient height is exponential, and certificate existence alone gives weak Euclidean separation.

---

### 4. Toric/Segre assignment lift

**Core trick.** Represent a global assignment by rank-one Segre coordinates: block variables store assignment monomials, while overlaps are glued through toric marginal maps. Harmful signed selectors then lie in secant directions rather than on the intended rank-one semigroup; Graver moves of the toric ideal become the objects to lengthen (cf. Sturmfels, 1996).

**Expected move.** Recursively tensor constant-size blocks so the first signed representation of an invalid point requires polynomially many rank-one terms, while honest assignments retain one rank-one representative.

**Obstruction audit.** G1: no slack. G2–3: uses global tensor coordinates rather than fixed local fibers. G5: overlap is through shared toric faces, not private rows. G6: crucial danger—semigroup positivity cannot be an external filter; the CVP metric itself must exclude group-completion points. G7: no radix, but exact toric circuits remain. G9: cubic Segre coordinates charge the seven-term parity relation. A polynomial Graver-length theorem is entirely missing.

**Falsification.** Find a constant-support toric circuit realizing the parity cheat, or any nearby point using negative semigroup coefficients.

**Smallest experiment.** Form degree-3 block tensors for the nine-clause instance, compute the toric kernel with exact integer elimination, then enumerate Graver moves through support 12.

**Likely death.** Unrestricted lattice coefficients recover the group completion, making positivity—and therefore rank-one semantics—unenforceable by linear CVP geometry.

---

### 5. Multi-prime Construction-A syndrome spreading

**Core trick.** First construct a global discrepancy map that includes a cubic fingerprint, so the known parity vector has nonzero syndrome. Encode that syndrome under primes \(3\) and \(5\) using explicit relative-distance linear codes and Construction-A lattices; any nonzero modular syndrome should occupy \(\Omega(M)\) Euclidean coordinates.

**Expected move.** Honest assignments have zero encoded syndrome. If every harmful integer vector is nonzero modulo at least one prime, \(M=n^{1+2c}\) gives a prospective \(n^c\) gap over \(O(n)\) anchors.

**Obstruction audit.** G1: no free slack. G2–3: syndrome is global. G5: clause-supported circuits are tested by the cubic map. G6: carry variables, modular equations, normalization, and target all remain inside the lattice. G7: unlike radix rows, codes spread only nonzero syndromes; exact integral kernels are still fatal. G9: the cubic row makes its parity witness nonzero. The needed all-vector injectivity and scaling lemma are open.

**Falsification.** Find an exact zero syndrome, a simultaneous \(3/5\) bypass, or carries producing a short representative.

**Smallest experiment.** Replace the Generation-7 radix block by short ternary and quinary BCH blocks on the fixed nine-clause basis; enumerate all vectors within squared radius 96.

**Likely death.** A higher-order signed selector lies in the integral kernel before coding, so every code block sees zero.

---

### 6. Formula-specific Delaunay-hole gadget

**Core trick.** Search for a rational lattice and target whose nearest shell consists exactly of globally consistent satisfying-label configurations. Unsatisfiability would remove the entire first shell, while a dimension-growing empty annulus—not amplified residuals—would provide the polynomial gap via Delaunay/Voronoi geometry.

**Expected move.** Construct a family with first-shell radius \(R\) and next admissible shell at \(n^cR\), while retaining polynomial dimension and bit complexity.

**Obstruction audit.** G1: no slack. G2–3: shell geometry is global, not local affine isolation. G5: overlaps are built into one Delaunay polytope rather than glued private gadgets. G6: basis and target directly define the shell; no filters. G7: zero residual has no privileged status. G9: the known parity point must be explicitly constrained outside the second-shell threshold. The current PSD metric is a special weak instance, so this route is not yet outside its constant-cost obstruction asymptotically.

**Falsification.** Prove the parity point—or another constant affine combination of candidate vertices—must stay within \(O(R)\) by convexity or triangle inequalities.

**Smallest experiment.** Solve an exact rational SDP/linear feasibility search for a Gram matrix separating all vectors of anchor excess at most 32 on the nine-clause instance.

**Likely death.** Constant signed affine relations force an \(O(1)\) shell ratio in every Euclidean realization.

---

### 7. Integral-flow verifier lattice

**Core trick.** Replace independent clause selectors by a layered assignment-verification trellis. Lattice coefficients represent edge flows; conservation and a unit source/sink target couple every local decision, aiming to make near-minimizers actual accepting paths rather than arbitrary signed collections (using total-unimodularity ideas of Hoffman–Kruskal, 1956).

**Expected move.** If signed flows can be excluded geometrically, an unsatisfiable formula has no zero-residual unit flow. Code-spreading the terminal deficit over \(M=n^{1+2c}\) coordinates would then yield a polynomial gap.

**Obstruction audit.** G1: no slack. G2–3: legality comes from a global path. G5: no clause-private selector can move independently. G6: flow conservation, terminal demand, and edge penalties must all be internal. G7: exact signed flows are the analogue of the radix kernel and must be exhaustively sought. G9: cube parity is not an accepting path, but could be a signed path combination. Polynomial size requires nontrivial state compression.

**Falsification.** Find a low-cost signed unit flow reaching the accepting target without any accepting path.

**Smallest experiment.** Build the full 4-variable decision trellis for the nine-clause instance, emit its CVP basis, and enumerate signed flows of anchor excess at most 32; then test safe state merges.

**Likely death.** Total unimodularity gives integrality, not nonnegativity; signed path combinations survive, while an exact general-SAT trellis has exponential state width.
