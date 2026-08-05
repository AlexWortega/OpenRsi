Below, **G1** = integer-slack annihilation; **G2/3** = constant-size affine isolation without composition; **G5** = private-row overlap circuits; **G6** = external filters, changed references, or mod-2 bypasses; **G7** = the exact `011+100−111` residual kernel; **Scale** = absence of a polynomial dimension-dependent gap. Generation 4 supplied no additional obstruction.

### 1. Fourier–Veronese selector lift

**Mechanism.** Replace first-marginal signatures of a pattern \(p\in\{0,1\}^3\) by all degree-\(\le2\) Fourier characters, sharing singleton and pair moments globally. The G7 identity preserves first moments but not pair characters, so it no longer lies in the raw kernel.

**Expected move.** Prove every zero-residual short vector induces consistent Boolean singleton/pair moments; then repeat the now-nonzero residual block polynomially.

**Obstruction audit.** G1: no slack variables. G2/3: no reliance on the 3-row local survivors. G5: pair moments are shared across clauses, not private rows with freed marginals. G6: all moment equations must be emitted in one fixed-target basis and searched unrestrictedly, including parity classes. G7: the offending identity has nonzero degree-2 signature. Scale: still unresolved until zero kernels are excluded globally.

**Falsification/test.** Add degree-2 character rows and anchored global pair variables to the nine-clause basis; exactly solve CVP, plus one satisfiable overlapping-clause control. Kill if a zero-residual non-Boolean vector costs at most baseline \(+8\).

**Likely death.** Private variable pairs may absorb defects, or inconsistent pseudo-moments may form a new exact kernel.

---

### 2. Truncated Macaulay/Nullstellensatz lattice

**Mechanism.** Encode \(x_i^2-x_i=0\) and each clause polynomial as a linear system on degree-\(d\) monomials. An unsatisfiability certificate in the row span would force every candidate moment vector to leave a nonzero integral residual, without local selectors.

**Expected move.** Find small \(d\) where the nine-clause obstruction already has an integral dual certificate; replicate certificate-sensitive coordinates to obtain a polynomial Euclidean penalty.

**Obstruction audit.** G1: no integer slack. G2/3 and G5: equations use one global monomial table, not composable local isolation matrices. G6: the target, monomial columns, and every equation must be inside the emitted lattice; audit over \(\mathbb Z\), \(\mathbb Q\), and mod 2. G7: outside its selector model, but not automatically safe—its signed vector may extend to a truncated pseudo-moment solution. Scale: requires polynomially bounded certificate degree and coefficient norm.

**Falsification/test.** Construct degree \(2,3,4\) Macaulay matrices for the nine-clause formula; perform exact row-span/SNF tests and unrestricted CVP, with a satisfiable control.

**Likely death.** General formulas may require degree \(\Omega(n)\), making the monomial lift exponential; low-degree pseudo-solutions may reproduce the cheat.

---

### 3. Additive-combinatorial fingerprints plus code spreading

**Mechanism.** Give each local pattern a deterministic \(B_h\)/Sidon-type fingerprint so no bounded signed combination can impersonate another pattern. Encode the vector of all fingerprint residuals with a systematic constant-distance linear code, making any nonzero residual occupy a linear fraction of coordinates.

**Expected move.** Short-vector bounds restrict coefficients to \([-h,h]\); fingerprint uniqueness removes exact local kernels, while code distance converts one violated clause into polynomial Euclidean cost.

**Obstruction audit.** G1: no slack. G2/3: fingerprints replace the tested sparse isolation matrices. G5: one global encoded residual couples all clauses rather than composing private syndromes. G6: congruences, carries, targets, and code coordinates must all be realized by one Construction-A-style lattice; unrestricted mod-\(q\) bypasses are explicitly searched. G7: choose fingerprints for which `011+100−111−000` has nonzero syndrome. Scale: follows only if bounded-coefficient uniqueness and code distance coexist at polynomial dimension.

**Falsification/test.** For \(q=5,7\), enumerate short fingerprint vectors for the eight patterns, append a small systematic code, and exactly solve the nine-clause instance and satisfiable control.

**Likely death.** Large coefficients or modular carries may create exact codeword kernels just beyond the tested coefficient bound.

---

### 4. Algebraic-integer norm barrier

**Mechanism.** Label patterns by algebraic integers whose Minkowski embeddings are linearly independent for the dangerous signed relations. A nonzero algebraic-integer residual has nonzero integral norm, so its full conjugate vector has squared length at least the field degree.

**Expected move.** Use an explicit degree \(D=N^{1+2c}\) field: zero residuals retain ordinary completeness cost, while every nonzero fingerprint residual contributes \(\Omega(D)\).

**Obstruction audit.** G1: unlike the killed algebraic-slack variant, this has no slack capable of zeroing the residual. G2/3: no local 3-row isolation assumption. G5: embeddings are attached to globally shared fingerprints, not private marginals. G6: the trace-form quadratic objective must be converted into an explicit rational Euclidean basis, with no external norm calculation; parity is audited. G7: algebraic linear independence makes its residual nonzero. Scale: degree gives the desired amplification only after proving every unsatisfiable short vector has nonzero algebraic residual.

**Falsification/test.** Use a degree-8 or degree-16 monogenic field; compute exact trace Gram matrices for the nine-clause identity and search the resulting integral quadratic CVP. Then attempt rational sum-of-squares realization.

**Likely death.** Rational Euclidean realization may blow up, or global gluing may restore an exact algebraic dependency.

---

### 5. Homological systole gadget

**Mechanism.** Map selector deviations to 1-chains in a finite chain complex. Arrange honest assignment changes as boundaries, while a falsification defect represents a nonzero homology class; a large systole then forbids short representatives of that class.

**Expected move.** Replace “one false clause” by a homological defect whose every representative has polynomial support, using an explicit polynomial-size complex rather than PCP testing.

**Obstruction audit.** G1: no slack residuals. G2/3: isolation is topological and global, not a fixed local affine fiber. G5: its short overlap move must become a nontrivial cycle, and systole—not private rows—must make it long; this is a required check, not guaranteed. G6: boundary matrices, target, and quotient relations are all emitted; SNF and mod-2 homology are audited without filters. G7: safe only if the signed identity maps to a nonzero class. Scale: requires explicit complexes with polynomial systole and a formula-preserving attachment theorem.

**Falsification/test.** Build a chain complex around the nine-clause incidence graph; use SNF to classify the G5/G7 moves and integer programming to find shortest class representatives. Include a satisfiable control whose defect is a boundary.

**Likely death.** The dangerous local move may always be null-homologous, or constructing large systole may implicitly require PCP-style gap amplification.

---

### 6. Global assignment automaton and one-way flow geometry

**Mechanism.** Represent an assignment as a unit path through a layered branching program, checking each clause when its final variable is assigned. Attempt to realize legal paths as the only nearby lattice flows, with rejecting transitions carrying a polynomially large penalty.

**Expected move.** Global state removes clause-overlap composition entirely: a legal path has one coherent assignment, whereas an unsatisfiable formula must cross a reject transition.

**Obstruction audit.** G1: no clause slack. G2/3 and G5: there are no independently composed selector fibers; consistency is maintained by one path state. G6: flow conservation, unit demand, direction gadgets, and reject penalties must all be coordinates of one fixed CVP instance; signed flows and mod-2 circulations are searched unrestrictedly. G7: its local affine identity is unavailable if nearby vectors are genuine paths. Scale: reject rows can be repeated, but polynomial state size is unproved.

**Falsification/test.** Build the exact 16-state assignment automaton for the four-variable obstruction, translate incidence constraints to CVP, and enumerate all short signed flows. Test a satisfiable formula with at least two accepting paths.

**Likely death.** Integer incidence equations permit signed undirected flows and cycles; enforcing direction geometrically may fail. General formulas also have exponential pathwidth/state complexity.

---

### 7. Voronoi deep-hole enforcement of nonnegative choices

**Mechanism.** Search for a small lattice and target whose complete nearest-point shell consists exactly of the eight one-hot local labels, while every signed combination using negative selector coefficients lies on a much farther shell. Glue copies through shared geometric coordinates rather than affine marginal equations.

**Expected move.** Eliminate the root cause of G7—negative selectors—by nearest-neighbor geometry itself, then assign large zero-on-satisfying penalties to forbidden Boolean patterns.

**Obstruction audit.** G1: no slack. G2/3: this restricts coefficients by Voronoi geometry, not affine inconsistency. G5: overlap must be tested in the glued Gram matrix; the old private-row circuit is outside the construction but may have a geometric analogue. G6: emit a rational basis and one target; no positivity filter is allowed, and all parity classes are included. G7: excluded only if its signed vector provably leaves the designated Voronoi shell. Scale: requires shell separation surviving polynomially many glued gadgets.

**Falsification/test.** Enumerate integral Gram matrices in dimensions \(3\)–\(6\), solve linear inequalities imposing eight designated nearest vectors, then exactly enumerate the next shell. Glue two overlapping clauses before trying the nine-clause instance.

**Likely death.** Central symmetry and convexity of Voronoi cells may force unwanted signed neighbors, while gluing may collapse any local shell gap.

Classical vocabulary pointers: Conway–Sloane, *Sphere Packings, Lattices and Groups*; Cox–Little–O’Shea, *Ideals, Varieties, and Algorithms*; Marcus, *Number Fields*; Schrijver, *Theory of Linear and Integer Programming*.
