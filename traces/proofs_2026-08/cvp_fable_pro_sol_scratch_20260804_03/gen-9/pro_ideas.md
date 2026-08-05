Below, every audit uses the same obstruction names:

- **O1** free-slack annihilation (G1)  
- **O2** bounded/local isolation only (G2–3)  
- **O3** overlap-composition circuits (G5)  
- **O4** external filters, changed references, mod-2 bypass (G6)  
- **O5** exact zero-residual signed selectors defeating radix (G7)  
- **O6** cube-parity/private-witness affine lifts (G8)  
- **O7** signed trellis flows (G8)  
- **O8** unbounded Nullstellensatz/Macaulay degree (G8)  
- **O9** unspecified topology/cosystolic family (G8)  
- **O10** bounded dissociation without a radius-to-\(\ell_1\) bound (G8)  
- **O11** tensor zero and non-rank-one pseudo-tensors (G8)  
- **O12** no polynomial fixed-target family or dimension-dependent gap  

No mechanism is being promoted before its stated finite test.

### 1. Explicit cosystolic sheaf barrier

**Core trick.** Route variable occurrences through an explicit 2-dimensional expanding complex, treating consistent assignments as 1-cocycles and clause falsifications as 2-cochain syndromes. A proved cosystolic inequality would spread any non-boundary falsification over \(\Omega(N)\) cells, whose emitted Construction-A coordinates can be scaled without charging honest witnesses.

**Expected move.** Convert one unavoidable false clause into \(\Omega(N)\) nonzero coordinates, yielding polynomial Euclidean separation after polynomial scaling.

**Audit.** O1: no slack; syndromes are direct coordinates. O2–O3: global coboundary expansion replaces private composition. O4: all equations and carries must be emitted. O5–O6: escaped only if the signed parity replacement represents a nontrivial cohomology class—currently unproved. O7–O8: no trellis or certificate degree. O9: use a named explicit family, not an unspecified complex. O10–O11: no dissociation or tensoring. O12: formula routing and the final gap law remain missing.

**Experiment/falsification.** On the nine-clause instance, attach clauses to the 2-skeleton of \(K_6\), compute boundary SNFs over \(\mathbb Z\) and \(\mathbb F_3\), emit the lattice, and compare exact CVP with a satisfiable control.

**Likely death.** The falsification syndrome is a short boundary, or routing destroys expansion.

---

### 2. Compressed Boolean-quotient determinant

**Core trick.** In \(A=\mathbb Z[x_1,\ldots,x_n]/(x_i^2-x_i)\), let \(F\) be the sum of clause-violation indicators. Multiplication by \(F\) is diagonal in the assignment basis: a satisfying assignment gives a normalized kernel vector, while for an unsatisfiable formula every diagonal entry is a positive integer.

**Expected move.** Find a polynomial-size determinantal or tensor-network representation of this multiplication operator; then weight the emitted equation \(M_Fu=0\) heavily relative to a normalization coordinate.

**Audit.** O1: no slack. O2–O3: the operator is global. O4: normalization must be an actual lattice row. O5–O6: the full \(2^n\)-assignment basis distinguishes every parity replacement; compression may reintroduce them. O7: no flow. O8 applies directly: polynomial compression is exactly the unresolved degree/size issue. O9–O10: irrelevant. O11: compressed determinant representations may admit non-rank-one pseudo-kernels. O12: the uncompressed construction is exponential.

**Experiment/falsification.** Build the exact \(16\times16\) operator for the nine-clause formula and a satisfiable control. Compute ranks, normalized integer kernels, and minimal tensor-network bond dimension across all variable cuts; repeat for random formulas through \(n=10\).

**Likely death.** Some cut has exponential operator Schmidt rank, reproducing proof-complexity degree growth.

---

### 3. List-recoverable Construction-A coupling

**Core trick.** Encode all variable occurrences as one word of an explicit Reed–Solomon or expander code; each clause supplies a seven-element list of allowed projected symbols. Emit local list selectors and the global code syndrome in one Construction-A lattice, aiming to prove that every vector below radius \(R\) uniquely decodes to an actual Boolean assignment.

**Expected move.** An unsatisfiable short vector would decode to a codeword meeting every clause list, a contradiction; any remaining syndrome can then be amplified freely because honest syndromes are zero.

**Audit.** O1: no free residual slack. O2–O3: consistency is one global codeword, not private rows. O4: residues, carries, and decoding bounds must all be internal. O5–O6 remain decisive: a signed selector with zero global syndrome defeats the code unless unique decoding canonicalizes coefficients. O7–O8: no trellis or Nullstellensatz. O9: irrelevant. O10: derive \(\|z\|_1\le\sqrt m\,\|z\|_2\le\sqrt mR\) before choosing code distance. O11: no tensor. O12: list selection and the polynomial gap are unproved.

**Experiment/falsification.** Use a small \(q=11\) Reed–Solomon code for the four-variable occurrence word, emit every selector/carry column, and run exact CVP plus SNF on the nine-clause instance and a one-clause-deleted satisfiable control.

**Likely death.** The local-list union recreates an exact signed zero-syndrome word.

---

### 4. Direct Voronoi-facet synthesis

**Core trick.** Avoid residual gadgets entirely: search for a positive-semidefinite Gram matrix \(Q\), linear term \(c\), and integer generators such that satisfying Boolean/ancilla points lie on one low-radius Voronoi shell while every integer point for the unsatisfiable instance lies polynomially farther away. Clause interaction is stored in cross terms of the global quadratic objective rather than in separately amplifiable residuals.

**Expected move.** Produce a small direct fixed-target lattice defeating the nine-clause signed selector without adding any selector measurements.

**Audit.** O1 and O4: no slack or external filters. O2–O3: \(Q\) is synthesized globally. O5–O6: outside their assumptions only if the construction is genuinely selector-free; quadratization ancillas restore both obstructions. O7–O11: no trellis, proof certificates, topology, dissociation, or tensors. O12 is entirely open: a finite separating ellipsoid gives no uniform family or polynomial ratio.

**Experiment/falsification.** Form an SDP over rational \(Q,c\) for variables and at most nine quadratization ancillas. Require a satisfiable control witness of radius \(r\) and every point in \([-2,2]^k\) for the obstruction instance to have distance at least \(2r\); rationalize and perform a box-free exact audit.

**Likely death.** Parallelogram identities for quadratic forms force a nearby signed integer point, or only a constant ratio is possible.

---

### 5. Noncommutative branching-product encoding

**Core trick.** Compile formula evaluation into a constant-width permutation branching program, so changing one occurrence alters a noncommutative group product rather than an additive syndrome. Represent transitions by regular-representation matrices and use determinant/exterior-power coordinates to distinguish the accepting product from signed combinations of accepting paths.

**Expected move.** Noncommutativity could invalidate \(2P_0-P_1\): endpoint flow remains valid, but the ordered product need not remain accepting.

**Audit.** O1: no slack. O2–O3: repeated variables share global branch columns. O4: every transition and consistency equation must be in the basis. O5–O6: cube parity is not automatically a group identity, but affine linearization may restore it. O7 is the central test: ordinary flow equations definitely fail, so success requires product-sensitive coordinates. O8: constant width avoids Macaulay degree, though program length grows. O9–O10: irrelevant. O11: exterior-power linearization may admit rank-pseudo solutions. O12: no polynomial-gap geometry yet.

**Experiment/falsification.** Compile the four-variable obstruction and a satisfiable control to a width-5 program. Emit multiplication-table selectors and regular-representation rows; enumerate all coefficient vectors of squared norm at most the Boolean baseline plus 16.

**Likely death.** Linearizing group multiplication recreates signed transition-table witnesses or requires exponentially many product states.

---

### 6. Valued-polymorphism gadget synthesis

**Core trick.** Treat a Euclidean lattice gadget as a finite-valued CSP relation after minimizing over integer auxiliaries. Search for a rational quadratic gadget whose seven satisfying OR tuples have equal low energy, whose false tuple has much larger energy, and whose valued polymorphisms exclude every affine signed operation responsible for overlap composition.

**Expected move.** A finite “no affine fractional polymorphism” certificate could supply a genuine composition theorem instead of extrapolating from two-clause audits.

**Audit.** O1: auxiliaries are minimized over all integers, so slack cheating is included. O2–O3: the valued-polymorphism certificate is intended to quantify arbitrary overlap, not bounded tests. O4: the synthesized basis and target are fixed. O5–O6: these are explicit candidate polymorphisms and must be rejected by the certificate; otherwise immediate failure. O7–O11: no trellis, certificate degree, topology, dissociation, or tensoring. O12: even a composable constant gadget does not establish an \(n^c\) ratio.

**Experiment/falsification.** MILP/SDP-search gadgets with at most three auxiliaries and Gram entries in \([-8,8]\). Exactly enumerate all integer auxiliary fibers for the eight OR tuples, then compose the winner on the nine-clause instance and run unrestricted exact CVP.

**Likely death.** Every quadratic lattice language admits an affine valued polymorphism, or the unavoidable honest baseline limits separation to a constant.

---

**Classical starting points:** Reed–Solomon codes (1960); Barrington’s bounded-width branching programs (1986/1989); Construction A for code lattices; Voronoi’s reduction theory; Lubotzky–Samuels–Vishne Ramanujan complexes (2005); and the valued-CSP polymorphism framework of Thapper–Živný.
