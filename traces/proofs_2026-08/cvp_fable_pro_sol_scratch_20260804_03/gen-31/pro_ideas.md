I use the following obstruction key in every audit:

- **S:** G1 free-slack residual annihilation.
- **L:** G2/3 local isolation failing under G5 overlap.
- **E:** G6 external-filter/reference invalidity.
- **K:** G7 exact zero-residual signed selector.
- **W:** G9/11 low-degree cube-parity kernels.
- **D:** G12 clause drop.
- **A:** G13 honest-affine-span collision.
- **P:** G14 pair-bag finite pass without composition.
- **H:** G15 zero-residual hierarchy lift.
- **F:** G19 signed-flow splicing.
- **M:** G28 min-plus growth failure.
- **T:** G30 tensor-seed isometry.

## 1. Plücker-minor rank enforcement

**Mechanism.** Lift adjacent clause labels to pair selectors, then add linear rows representing all \(2\times2\) minors of selected moment matrices. Honest global assignments produce rank-one matrices; signed mixtures such as cube parity generally acquire nonzero exterior-square coordinates.

**Expected move.** An expander of pair lifts could make one rank defect violate \(\Omega(N^{1+2c})\) replicated minors while completeness remains \(O(N)\).

**Audit.** S: no slack. L: checks overlap jointly, not through private rows. E: all pair variables and rows are emitted. K/W/A: raw affine kernels need not survive the quadratic lift, but this is unproved. D: dropping a clause affects every incident minor. P applies directly—this is a strengthened pair-bag lift, still lacking composition. H: no laminar marginal propagation. F/M/T: no flow, min-plus recursion, or tensor seed.

**Falsification.** A zero-minor signed extension of G11/G13, or NO/YES ratio not increasing with graph size.

**Experiment.** On the nine-clause instance, use a fixed 3-regular clause graph, pair selectors, and linearized minors; exactly search through baseline \(+32\).

**Likely death.** Pair selectors may themselves admit higher-order rank-one pseudodistributions.

---

## 2. Canonical \(p\)-adic sign certificates

**Mechanism.** Replace each unrestricted selector coefficient by a bounded-value table carrying its canonical base-\(p\) digits. Values \(0,1\) have zero upper digits, while \(-1,-2,\ldots\) expose long strings of \(p-1\) digits; replicate upper-digit coordinates without replicating honest anchor cost.

**Expected move.** If every signed cheat uses a negative coefficient, \(L=N^{1+2c}\) certified digit levels give polynomial excess.

**Audit.** S is not safely escaped: digit/carry auxiliaries could become new slack, although every one is anchored and range-linked. L: the penalty is coefficientwise, independent of overlap. E: digits, carries, and range equations must all be CVP coordinates. K/W/A/H/F: their negative coefficients should pay even when all semantic residuals vanish. D: zeroing a one-hot selector changes its range certificate. P: no pair bags. M/T: no recursive tile or tensor pair.

**Falsification.** Any signed table combination representing \(-1\) with zero upper-digit cost, or honest baseline growing as fast as the penalty.

**Experiment.** For the G7 attacked clause, take \(p=3\), values \([-3,3]\), four digits, table coefficients in \([-2,2]\), and exhaustively minimize the emitted objective.

**Likely death.** Canonical representations require inequalities; linear equalities may admit signed mixtures of digit tables.

---

## 3. Universal Nullstellensatz–Macaulay layer

**Mechanism.** Emit Boolean polynomials \(x_i^2-x_i\), clause-violation polynomials, and their monomial multiples as a Macaulay operator. A satisfying assignment annihilates every row; an unsatisfiable system has a polynomial identity for \(1\), potentially forcing any moment vector away from the target.

**Expected move.** A polynomial-size circuit-compressed certificate, replicated orthogonally, could yield \(N^{2c}\) residual energy without identifying the certificate during reduction.

**Audit.** S: no clause slack. L: the operator is global. E: every moment and multiplication-consistency row is emitted. K/W/A: affine selector collisions are not automatically collisions after monomial lifting; low-degree pseudoexpectations remain a direct threat. D: omitting a clause moment violates its constant/marginal rows. P/H: neither pair bags nor a laminar hierarchy. F/M/T: no flow, min-plus composition, or tensor seed.

**Falsification.** A degree-\(d\) integral pseudoassignment annihilating the full operator, or required degree/monomial count becoming superpolynomial.

**Experiment.** Build the squarefree degree-\(\le4\) Macaulay matrix for the nine-clause obstruction and control; test G7/G11/G13 vectors, compute exact rational kernels, then enumerate the first anchor shell.

**Likely death.** General formulas may require exponential-degree or exponential-size algebraic certificates.

---

## 4. Cosystolic sheaf obstruction

**Mechanism.** Regard variable values as a section of a sheaf over a clause-variable complex; inconsistency is its coboundary. Replace each incidence by a deterministic high-dimensional expander lift so every nontrivial section has a large coboundary, then realize residues through a Construction-A lattice.

**Expected move.** A defect that originally touches one clause could expand to \(N^{1+2c}\) zero-target syndrome coordinates.

**Audit.** S: no slack. L: overlap is encoded by one global coboundary. E: all lifted cells and residues are emitted. K/W/A: signed cocycles remain possible; cosystolic expansion over \(\mathbb F_p\) does not automatically control integral short vectors. D: a dropped cell has a large boundary if expansion holds. P/H: non-laminar expander complex, not fixed pair bags. F: no path flow. M/T: no min-plus or seed tensoring.

**Falsification.** A low-support integral cocycle, a mod-\(p\) lift with cheap Euclidean representative, or failure to preserve satisfiability.

**Experiment.** Form the incidence 2-complex of the nine-clause instance, take an explicit 18-sheet lift, compute minimum nontrivial \(\mathbb F_3\) cosystoles, and exactly audit the corresponding Construction-A shell.

**Likely death.** Producing the needed formula-preserving expansion may amount to forbidden PCP-style gap amplification.

---

## 5. Noncommutative path signatures

**Mechanism.** Label literal transitions by generic noncommuting matrices and carry the ordered product, rather than only additive flow conservation. Exterior powers or truncated free-algebra coordinates can make two signed path fragments distinguishable even when their edge counts splice into an accepting flow.

**Expected move.** With matrix dimension \(d=\Theta(\log N)\), absence of short polynomial identities might force every false accepting combination to expose polynomially many signature coordinates.

**Audit.** S: no slack. L: signatures couple the entire query order. E: product-state selectors and every multiplication row must be emitted. K/W/A: additive affine kernels generally do not preserve noncommutative products, but lifted signed kernels may exist. D: a missing layer changes word length/product. P/H: no bag hierarchy. F is the target obstruction—G19 used only additive flows. M/T: no min-plus rule or paired seed.

**Falsification.** An exact accepting signed tensor-network contraction, especially with two negative coefficients, or any cheap multiplication inconsistency.

**Experiment.** Compile the all-eight-clauses three-variable obstruction to a short decision DAG, use generic \(3\times3\) integer transition matrices and degree-four word signatures, and solve the exact accepting fiber by ILP.

**Likely death.** Linearizing multiplication may recreate precisely the signed-splicing freedom it was meant to remove.

---

## 6. Fully enumerated low-degree assignment code

**Mechanism.** Encode variable values and clause violations as one low-degree table over \(\mathbb F_q^m\), enumerating all point-line consistency constraints rather than sampling them. Reed–Muller distance then spreads any genuine nonzero Booleanity or clause polynomial over a polynomial fraction of the table.

**Expected move.** Zero completeness residual but \(\Omega(q^m)\) NO residuals could dominate an \(O(N)\) selector baseline and produce \(N^c\).

**Audit.** S: clause and Booleanity polynomials are direct—no free slack. L: one global table replaces private clause rows. E: the complete table and all tests are emitted. K/W/A: nonlinear table lifting may break raw affine collisions, but pseudocodewords could restore them. D: deleting one clause value should violate code distance. P/H: no fixed pair mesh or laminar tree. F/M/T: no flow, min-plus recursion, or tensor seed.

**Falsification.** A signed low-degree pseudotable satisfying all line constraints while encoding the G7/G11 attack; also reject if the proof requires a PCP/local-testing theorem.

**Experiment.** Over \(\mathbb F_5^2\), encode the four-variable nine-clause instance, enumerate every affine line, and exactly search coefficients in \([-2,2]\).

**Likely death.** Full tables may be polynomial only at degrees too small for soundness; stronger parameters become superpolynomial.

---

## 7. Equal-radius discrepancy Gram search

**Mechanism.** Search for rational PSD forms \(Q=4I+C^\top C\) under constraints that every honest global encoding has the same completeness radius, while known harmful shells have much larger \(Q\)-distance. Use deterministic small-bias/discrepancy rows rather than incidence-equivariant moment rows.

**Expected move.** A sequence of equal-radius Gram layers could charge every harmful cone by \(N^{1+2c}\) while keeping honest energy \(O(N)\).

**Audit.** S: no slack. L: \(Q\) is global. E: the rational factor \(C\), center, and target are emitted. K/W/D: these are explicit adversarial constraints in the optimization, not escaped assumptions. A: unlike G13 hashes, rows need not map all honest encodings to one syndrome—only to equal norm—so its affine-span theorem does not directly apply. P/H/F/M: no bags, hierarchy, flow, or recursion. T: first quotient exact coordinate isometries; no tensoring.

**Falsification.** SDP optimum bounded by a constant ratio, irrational/nonfactorable output, or a new unrestricted shell vector beating the designed attacks.

**Experiment.** Enumerate the nine-clause shell with coefficients in \([-1,2]\), solve a rationalized max-margin SDP, factor \(Q\), then rerun exact CVP search.

**Likely death.** Equal-radius constraints over exponentially many honest assignments may force the same low-dimensional symmetry that made G13 collisions cheap.

Classical ingredients invoked here include Plücker/exterior embeddings, Hilbert’s Nullstellensatz, Reed–Muller codes (Muller 1954; Reed 1954), expander-code ideas (Sipser–Spielman 1996), and the Amitsur–Levitzki matrix-identity theorem (1950).
