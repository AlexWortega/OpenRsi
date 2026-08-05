Below, “scaling” means the missing G20/G21 polynomial excess-to-baseline law, and “entanglement” means the G22 unrestricted-tensor obstruction.

### 1. Spherical semigroup cage

**Mechanism.** Treat legal accepting computations as elements of an affine semigroup, not merely solutions of linear residual equations. Search for an integral map \(H\) and target \(t\) placing every legal computation on one sphere while every nearby element of its group completion containing a negative coefficient, deletion, or multiplicity has large excess.

**Expected move.** Convert the two \(-1\) coefficients in G19, and more generally signed splices, into code-distance rather than residual energy.

**Obstruction audit.** G1 slack: none. G2/G3 isolation and G5 overlap: replaced by one global semigroup metric. G6 external filtering: coefficients remain unrestricted. G7 zero residual, G9 quadratic parity, G11 cubic parity, G13 affine collision, G15 affine lift, and G19 signed flow are targeted through coefficient geometry, not checks. G12 drop is included as a forbidden semigroup state. G14 pair-bags are only a benchmark. G20/G21 scaling requires an unproved spherical-separation family. G22 entanglement is absent.

**Falsification.** Any signed computation at legal radius, or a proof that equal-radius legality forces \(H^\top H\) to be ineffective.

**Experiment.** On a four-layer branching program, enumerate all integral flows with anchor excess \(16\); search small integer \(H\) by MILP.

**Likely death.** Equal-radius constraints may force the excess to stay constant relative to the linear baseline.

---

### 2. Splitter-compressed Walsh lift

**Mechanism.** Give each assignment a nonlinear Walsh fingerprint, but compress degree-\(k\) characters using a deterministic family of color-coding splitters: each relevant support is colorful somewhere and its parity becomes one product coordinate. Implement those products by a balanced, circuit-specific lift rather than all \(n^k\) monomials.

**Expected move.** Detect the G11 unique-triple parity and larger affine pseudodistributions while using polynomial dimension for \(k=\Theta(\log n)\).

**Obstruction audit.** G1 slack: none. G2/G3 and G5 local isolation: bypassed by global characters. G6: every product auxiliary must be emitted and unrestricted. G7, G9, G11, G13, and G15 are outside low-degree invisibility if their Fourier support is hit. G12 drops alter the constant character. G14 is the first comparison instance. G19 signed splicing and G22 entanglement are **not** escaped: they can corrupt the multiplication lift. G20/G21 requires a theorem that every low-distance attack has a splitter-hit character.

**Falsification.** A zero-fingerprint signed lift, especially one formed by splicing multiplication trees.

**Experiment.** For four variables, use all \(GL(4,2)\) transforms and degree-two characters; emit explicit XOR/product auxiliaries and exactly search through anchor excess \(32\).

**Likely death.** Enforcing products recreates G19, while covering arbitrary high-degree characters requires exponentially many splitters.

---

### 3. Noncommutative augmentation filtration

**Mechanism.** Encode wire values as basis elements of an integral group ring of a small nonabelian \(p\)-group. Arrange each false clause to contribute a nonzero element of the augmentation ideal \(I\), and propagate formula composition so surviving defects move into \(I^2,I^4,\ldots\), whose regular-representation coordinates should acquire rapidly growing norm.

**Expected move.** Replace scalar residual amplification by a filtration in which cancellation requires matching many noncommuting words.

**Obstruction audit.** G1 slack and G7 radix kernels: no scalar slack or ordered digits. G2/G3 and G5: composition is global multiplication, not private rows. G6: the whole multiplication table must be emitted. G9/G11 parity and G13/G15 affine mixtures need not respect products, so are potentially exposed. G12 drops map to explicit zero/mass states. G14 gives a finite benchmark. G19 signed multiplication flows and G22 entangled product states remain squarely inside the danger zone. G20/G21 needs uniform norm growth in \(I^{2^d}\), currently absent.

**Falsification.** A signed exact product computation reaching the unit/accept state, or nilpotence/zero divisors erasing a defect.

**Experiment.** Use the order-27 Heisenberg group, two Boolean gates, and its \(27\)-dimensional regular representation; enumerate exact signed fibers with coefficients in \([-2,2]\).

**Likely death.** Linearized multiplication admits the same group-completion splices as G19, and finite group-ring filtrations eventually collapse.

---

### 4. Multiscale collision-energy frame

**Mechanism.** Regard selector coefficients as a signed measure and record its restrictions along many overlapping variable partitions. Add equal-radius quadratic frame terms measuring collision energy at every scale; a Dirac assignment has controlled energy, while parity mixtures, negative mass, and clause deletion should create excess on many restrictions.

**Expected move.** Turn the constant-cost G9/G11 parity into repeated Parseval-type energy without relying on residual nonzeroness.

**Obstruction audit.** G1 slack: none. G2/G3 and G5 local isolation: replaced by overlapping restrictions. G6: signed measures are optimized unrestrictedly. G7 zero residual is irrelevant if its collision energy changes. G9 and G11 are directly targeted. G13 affine equality preserves linear moments but not squared energy. G15’s zero-residual lift should pay at multiple restrictions. G12 drops are charged by mass plus collision coordinates. G19 signed flows become signed measures and are included. G14 is the natural finite seed. G20/G21 needs a multiscale energy-growth theorem. G22 is avoided if all frame blocks are direct restrictions rather than tensor lattices.

**Falsification.** A signed measure matching both mass and collision energy at every selected restriction.

**Experiment.** On the nine-clause instance, include every restriction to one, two, and three variables; optimize rational weights by LP, then exactly enumerate the old shell.

**Likely death.** A high-order parity can be invisible to every polynomial-size low-width restriction family.

---

### 5. Twisted relative-homology obstruction

**Mechanism.** Convert a computation graph into an explicit two-complex: flows are integral \(1\)-chains, legal local rewrites are \(2\)-cell boundaries, and acceptance specifies a relative homology class. Add a finite voltage local system so signed splices that are boundaries in the untwisted complex may acquire nonzero holonomy in successive cyclic covers.

**Expected move.** Reinterpret G19’s accepting signed flow as a cycle and force every representative of its class to have growing support.

**Obstruction audit.** G1 slack and G7 radix: absent. G2/G3 and G5: replaced by global topology. G6: chain coefficients remain unrestricted. G9/G11 parity, G13 affine collision, and G15 lift become signed cycles; they are **not** automatically excluded. G12 drops become relative chains with boundary and must be priced. G19 is the central unresolved cycle. G14 supplies a small attachment test. G20/G21 becomes a required systolic-growth theorem. G22 tensor entanglement is absent.

**Falsification.** The G19 chain has zero voltage, becomes a short boundary, or retains bounded support in every cover.

**Experiment.** Build the decision complex for all eight clauses on three variables, attach commuting-diamond \(2\)-cells, and compute SNF plus shortest representatives in the \(2\)- and \(3\)-fold voltage covers.

**Likely death.** Formula attachment may introduce short null-homologous representatives, and logarithmically iterated covers may exceed polynomial size without yielding relative growth.

---

### 6. Lawrence–Graver circuit exposure

**Mechanism.** Form the global affine semigroup of legal local labels and apply a Lawrence-style lift that gives separate coordinates to positive and negative sides of primitive integer kernel circuits. Search for weights under which every legal Boolean point has the same radius but every harmful Graver move, semigroup hole, or deletion has large quadratic excess.

**Expected move.** Make residual-zero attacks visible precisely because they are integer circuits, rather than trying another residual hash.

**Obstruction audit.** G1 slack: none. G2/G3 isolation and G5 overlap are subsumed by the global kernel. G6 unrestrictedness is explicit in the lifted lattice. G7, G9, G11, G13, G15, and G19 become candidate circuits to expose, not invisible kernel vectors. G12 drops are semigroup holes included in the search. G14 supplies a finite positive case. G20/G21 requires polynomial Graver complexity and cumulative excess—both unproved. G22 is absent unless recursive lifts are tensorized.

**Falsification.** A primitive circuit has zero lifted excess, or the necessary Lawrence lift has superpolynomial rank.

**Experiment.** Compute all support-\(\leq 8\) circuits of the G7 matrix; solve an exact LP for equal-radius legal weights separating those circuits, all clause drops, and the G11 attack.

**Likely death.** General SAT incidence matrices probably have exponentially many indispensable circuits, and charging all of them may inflate completeness equally.

---

### 7. Exact min-plus quotient-gate search

**Mechanism.** Freeze a small lattice \(L\), modulus-\(q\) port map \(\phi\), rational target, and legal/illegal/drop port classes. Orthogonal fiber-product gluing then has an exact min-plus identity
\[
C_{G\circ H}(a,c)=\min_b\bigl(C_G(a,b)+S\,C_H(b,c)\bigr),
\]
so recursive behavior can be proved from a finite cost table rather than inferred from local separation.

**Expected move.** Find a quotient gadget whose table duplicates illegal cost faster than legal baseline under substitution.

**Obstruction audit.** G1 slack: none. G2/G3 and G5: no appeal to local isolation; overlap is the explicit gluing map. G6: each coset minimum is unrestricted. G7, G9, G11, G12, G13, G15, and G19 appear as named intermediate/drop classes in the table. G14 is a calibration case. G20/G21 is the symbolic recurrence being tested, not assumed. G22 entangled fiber-product representatives are included by exact coset minimization.

**Falsification.** Completeness mismatch, a cheap drop/signed class, or failure of the illegal/legal ratio to increase at depth two.

**Experiment.** Enumerate \(q=3\), rank \(2\)–\(3\) positive-definite integral Gram matrices with entries \([-2,2]\), targets in \(\frac16\mathbb Z^r\), and all port maps; compute depth-two tables exactly.

**Likely death.** Min-plus composition may always route through a cheap drop state, making all achievable gaps additive rather than multiplicative.
