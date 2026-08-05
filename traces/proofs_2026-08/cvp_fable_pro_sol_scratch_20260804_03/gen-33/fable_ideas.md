I use the following obstruction key in every audit:

- **O1** RS/free-slack annihilation; **O2–3** fixed-marginal affine isolation only; **O5** private-row overlap failure; **O6** external-filter/reference invalidity; **O7** exact signed-selector radix kernel; **O9** constant-cost quadratic parity; **O11** unique-triple cubic parity; **O12** clause drop; **O13** honest-affine-span collision; **O14** pair-bag finite pass only; **O15** affine lift through a laminar hierarchy; **O19** signed-flow splicing; **O28** adverse min-plus growth; **O30** seed isometry; **O31** finite equal-radius Walsh pass; **O32** additive cross-copy parity.

## 1. Noncommutative holonomy on an expander

**Core/expected move.** Replace scalar consistency by transports \(v_u=U_e v_v\), where \(U_e\) are explicit noncommuting integral representations of \(S_3\) or \(A_5\). A satisfying assignment gives a flat section; inconsistent local choices should create nontrivial cycle holonomy on polynomially many powered-expander cycles, producing polynomial residual energy.

**Test/experiment.** On the nine-clause obstruction, use the two-dimensional integral \(S_3\) representation, freeze polarity-dependent transports, and exactly compare obstruction/control minima. Explicitly evaluate G7, G11, DROP, and two-copy parity before shell search.

**Falsification.** Any zero-holonomy signed section, or NO energy no larger than a constant multiple of YES.

**Map.** O1: no slack. O2–3: not fixed marginals. O5: checks are global cycles, not private rows. O6: emit every transport row. O7: scalar zero residual need not mean flat holonomy. O9/O11: parity must preserve matrix transport. O12: drops expose incident edges. O13: not a common scalar hash. O14/O31: different lift. O15: cycles, not a tree. **O19 applies unless twisted signed flows are absent.** O28: no tile recurrence. O30: test nonisometry. O32: copies meet through cycle products.

**Likely death.** Signed invariant subrepresentations recreate G19 splicing.

## 2. Expander code with integral pseudocodeword distance

**Core/expected move.** Encode every occurrence by a nonbinary simplex symbol and connect symbols using a deterministic Tanner expander. Seek an *integer* unique-neighbor lemma: every normalized, locally legal signed pseudocodeword that is not an honest global assignment violates \(\Omega(N^{1+\epsilon})\) redundant checks, while honest assignments violate none.

**Test/experiment.** Attach a 12-vertex, degree-3 bipartite graph over \(\mathbb F_3\) to the nine-clause selectors. Enumerate all graphs of that size or a canonical small Ramanujan candidate; compute exact CVP minima and minimum syndrome among anchor excess \(\le32\).

**Falsification.** A zero-syndrome harmful pseudocodeword, especially the G13 affine combination, or syndrome support \(O(1)\).

**Map.** O1: no slack. O2–3/O5: global Tanner checks free no marginal. O6: all normalization and symbol rows emitted. O7: code checks selectors themselves. O9/O11: intended integer pseudodistance. O12: expansion replicates a drop. O13: formally outside raw 72-coordinate hashing because symbols are enlarged, but its affine-collision mechanism remains dangerous. O14: not pair bags. **O15 may apply via an affine codeword and must be tested.** O19: no path flow. O28/O30: no frozen tile/tensor seed. O31: not Walsh-block energy. O32: one global code, not additive copies.

**Likely death.** A dense affine codeword has zero syndrome despite expansion.

## 3. Twisted sheaf on a co-systolic 2-complex

**Core/expected move.** Regard local clause assignments as stalks of a formula-dependent sheaf over an explicit two-dimensional complex. Consistency is a twisted coboundary; co-systolic expansion should force any non-section—including integral signed cochains—to have large coboundary unless it represents a controlled global cohomology class.

**Test/experiment.** Put the nine clauses on an 18–30 triangle complex, with eight-label clause stalks and occurrence-restriction maps. Use Smith normal form to compute integral \(H^0,H^1\), then ILP-enumerate the shortest normalized legal cochain outside genuine sections.

**Falsification.** Nonzero harmful \(H^0\), a short torsion cocycle, or coboundary energy no larger than the anchor baseline.

**Map.** O1: no slack. O2–3/O5: composition is through faces, not freed marginals/private rows. O6: cochain domain and every coboundary row are emitted. O7: exact scalar kernels may have nonzero twisted boundary. O9/O11: parity must be a cocycle. O12: a drop creates boundary around its star. O13: enlarged sheaf, though affine sections remain a threat. O14: higher-dimensional overlap. **O15 applies in spirit if affine pseudosections extend through every face.** O19: no layered flow, but signed cocycles are its analogue. O28/O30: no tile/tensor. O31: not Walsh geometry. O32: global faces cross copies.

**Likely death.** Formula-dependent stalks destroy co-systolic expansion, or torsion gives a cheap signed cocycle.

## 4. Truncated \(p\)-adic negativity detector

**Core/expected move.** Represent each selector coefficient by \(L\) base-\(p\) digit layers with explicit carry equations and zero-target high digits. Honest \(0/1\) coefficients terminate immediately, whereas a negative coefficient such as \(-1\) has the truncated \(p\)-adic tail \(p-1,p-1,\ldots\), potentially costing \(\Omega(L)\) without increasing completeness.

**Test/experiment.** Use \(p=3,L=4\) on the 72-selector obstruction. Emit digit, carry, normalization, and legality coordinates; exactly evaluate G7, G11/G13, DROP, and G19 before enumerating the shell.

**Falsification.** Any signed attack represented using \(O(1)\) nonzero digits/carries, or a new digit-level affine kernel.

**Map.** O1: every carry is anchored, unlike free slack. O2–3/O5: coefficientwise global lift. O6: digits cannot be external filters. **O7 directly applies if its zero-residual selector lifts cheaply; this is the first test.** O9/O11: negative parity coefficients should acquire long tails. O12: replicate normalization at digit levels. O13: not a compatible raw hash, but affine combinations retain zero linear checks and may still win on energy. **O15 warns that carries may lift affinely.** O14/O31: unrelated finite baselines. O19: signed flow coefficients also receive tails. O28/O30: no recursion/tensor seed. O32: tails are per coefficient, so additive parity may persist.

**Likely death.** Unrestricted digit variables synthesize \(-1\) with a short balanced carry circuit.

## 5. Perfect-hash logarithmic assignment bags

**Core/expected move.** Use overlapping bags of \(t=\Theta(\log N)\) variables, but keep polynomial size via splitters/perfect-hash families. Each bag has full assignment selectors and equal-radius high-degree fingerprints; every small-support parity or drop should be fully exposed in many bags, while honest assignments remain exactly consistent.

**Test/experiment.** For the four-variable obstruction, take every 4-variable bag and all 16 labels, then add all 3-variable projections. Compare its exact shell to G14 and explicitly lift the G13 affine coefficients before doing DP.

**Falsification.** A consistent locally legal affine pseudodistribution through every bag, or NO/YES ratio bounded independently of bag multiplicity.

**Map.** O1: no slack. O2–3/O5: complete overlapping views, not private marginal rows. O6: every bag selector and projection is in the lattice. O7/O9/O11: their support is contained in an exposed bag. O12: each clause appears in many views. O13: formally enlarged/non-common-syndrome, but its affine combination can project to all bags. O14: logarithmic rather than pair bags. **O15 is directly relevant: a global affine pseudodistribution may thread all bags; the experiment must attempt that lift first.** O19: no path flow. O28/O30: no fixed recursion/tensor. O31: global high-degree views, not independent Walsh blocks. O32: bags span both copies, though an all-degree-preserving parity may remain additive.

**Likely death.** Sherali–Adams-style pseudodistributions survive every polynomial-size logarithmic view.

## 6. Exterior-algebra coherence fingerprint

**Core/expected move.** Map each local assignment to a decomposable multivector and compare overlaps by contractions. Sum signed exterior tags globally rather than blockwise: honest assignments are designed to cancel or remain \(O(\sqrt M)\), while parity mixtures become nondecomposable and add coherently with norm \(\Omega(M)\).

**Test/experiment.** Assign the eight clause labels explicit vectors in \(\bigwedge^2\mathbb Z^4\) using Vandermonde columns. Freeze incidence signs by exhaustive search on the nine-clause control, then exactly evaluate obstruction attacks and enumerate the shell.

**Falsification.** G13 parity has the same global exterior sum as an honest encoding, or the tag Gram collapses to a scalar multiple of identity.

**Map.** O1: no slack. O2–3/O5: global contraction geometry. O6: emit the integer tag factor and center. O7: zero logical residual can retain exterior energy. O9/O11: nondecomposability targets parity. O12: redundant contractions charge drops. O13: outside common-target syndromes because honest tags may differ while having controlled norm; nevertheless affine cancellation may recur. O14/O15: neither pair marginals nor a laminar hierarchy. O19: no flow. O28/O30: no tile/tensor seed; check tag automorphisms to exclude isometry. O31: unlike block Walsh, cross-clause sums create coherent terms. O32: cross-copy wedge contractions are nonadditive.

**Likely death.** The required equal-completeness identities force a tight frame, reducing the construction to G31-type coefficient energy.

## 7. Macaulay/Nullstellensatz lattice dualization

**Core/expected move.** Abandon selector consistency. Write Boolean 3SAT as polynomial equations and build a bounded-degree Macaulay matrix; use its integer row lattice so SAT evaluations give short dual witnesses, while an explicit integral Nullstellensatz certificate for UNSAT separates the target. A coefficient-height lower bound, amplified by redundant multiples, would supply the gap.

**Test/experiment.** Start with the unsatisfiable conjunction of all eight signed clauses on three variables and a control with one clause removed. Build degree-\(3,4,5\) Macaulay matrices, compute Smith forms and exact CVP minima, and inspect certificate heights.

**Falsification.** Required degree or matrix dimension grows exponentially, certificate coefficients explode completeness, or the NO/YES ratio stays constant.

**Map.** O1/O7: no residual slack or selector kernel. O2–3/O5: no marginal composition. O6: the full Macaulay lattice and fixed target must be emitted; evaluations cannot be external filters. O9/O11/O13/O15: selector parities and affine lifts are outside the representation. O12: deleting a clause changes the ideal, not a selector block. O14/O31: unrelated finite gadgets. O19: no flow. O28/O30/O32: no tile, tensor seed, or additive copy rule; multiplication rows couple degrees globally.

**Likely death.** Known hard Boolean systems require linear Nullstellensatz degree, making the Macaulay lift exponential.

Classical ingredients invoked: Sipser–Spielman, *Expander Codes* (1996); Naor–Schulman–Srinivasan, *Splitters and Near-Optimal Derandomization* (1995); standard Construction-A lattices, sheaf/cohomology, Plücker coordinates, and Hilbert–Nullstellensatz/Macaulay matrices. No external search was used.
