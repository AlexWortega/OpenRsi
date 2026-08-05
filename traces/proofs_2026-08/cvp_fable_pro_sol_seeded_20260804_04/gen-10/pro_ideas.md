Map labels: **O1** bounded local signatures; **O2** marginal/tableau encodings; **O3** local-view hierarchies; **O4** phase lifts; **O5** integer exact fibers; **O6** complete-assignment fingerprints; **O7** tensor amplification; **O8** exact syndrome-to-CVP transfer.

### 1. Barrington–Magnus global word lift

**Core trick.** Compile the formula evaluator into a width-5 noncommutative branching program, then encode its complete ordered product using Magnus/Fox coefficients. Repeated occurrences of a variable are coupled through one global group word rather than affine wire interfaces.

**Expected move.** A rejected assignment should leave many nonzero high-order word coefficients, potentially giving polynomial support from a polynomial-length branching program.

**Map check.** O1 applies to any degree-\(r\) truncation with an \((r+1)\)-cube; only full/high-degree coefficients escape. O2–O3 are avoided unless the product is gate-linearized. O4 is outside its single-valued abelian/copy-stable assumptions. O5 is irrelevant before integer linearization. O6 uses polynomial branching states, not assignment columns. O7 is not tensoring; every mixed lifted word still needs checking. O8 applies after binary expansion.

**Falsification.** All-eight or holonomy has an illegal mixed word no heavier than the worst legal product, or rank becomes superpolynomial.

**Smallest experiment.** Compile the three-variable all-eight formula, compute Magnus coefficients through degree 4, span all lifted assignment words, and enumerate every pointed word.

**Likely death.** Degree sufficient to defeat cubes makes the coefficient dictionary exponential.

---

### 2. ROABP multiplicity-code condenser

**Core trick.** Regard mixed reduced-tensor words as polynomials represented by a code-dependent read-once algebraic branching program. Replace modular hashing by a deterministic ROABP hitting set together with Hasse derivatives, simplex-encoding each field symbol to convert nonzeroness into controlled binary weight.

**Expected move.** Multiplicity evaluations might preserve every low-support NO polynomial while using polynomially fewer coordinates than the formal tensor.

**Map check.** O1 still applies when polynomial degree is below an available cube dimension; the route must use full degree or prove the relevant ROABP class lacks such cubes. O2–O3 do not apply to direct global evaluations. O4–O5 are irrelevant. O6 evaluates a sparse program rather than complete assignments. O7 is directly addressed, including arbitrary mixed words, but no compression theorem is known. O8 applies to the binary image.

**Falsification.** A pointed kernel, worst-YES weight at least best-NO weight, or required ROABP width/output exceeding polynomial size.

**Smallest experiment.** Express the \(8\times8\) reduced square as an ROABP; test 2–4 derivative orders on the existing YES/200-NO, all-eight, affine-closure, and holonomy suites.

**Likely death.** Arbitrary mixed tensors have large ABP width, while evaluations densify YES words.

---

### 3. Witt-vector carry shell

**Core trick.** Assign each triple a formula-derived Teichmüller label \(a_j\) and append ghost coordinates  
\[
G_s(z)=\sum_j z_j[a_j]^{2^s}.
\]
Scale successive coordinates geometrically so the first nonzero global Witt carry is expensive; seek labels making every perfect matching share one target while every illegal odd cover differs at some level.

**Expected move.** Global high-degree carries could turn the additive \(q\) versus \(q+2\) integrality defect into a multiplicative penalty.

**Map check.** O1 is avoided only with unboundedly many carry levels; bounded truncation is again bounded-degree. O2–O3 are outside direct global ghost rows. O4 is outside only if labels are genuinely formula-dependent and multivalued; a telescoping local labeling may be coboundary-trivial. O5 applies if carries become ordinary affine slack variables. O6 uses triple columns, not assignment fingerprints. O7 is unused. O8 applies only after a correct binary realization; otherwise a direct integer basis is needed.

**Falsification.** No assignment-independent target labels exist, or all-eight/holonomy admits an exact low-carry signed cover.

**Smallest experiment.** SAT-independently solve for labels over \(W_3(\mathbb F_8)\) on \(q=2,3\) dictionaries and enumerate coefficients in \([-2,2]\).

**Likely death.** Universal completeness forces a coboundary or recreates constant-cost integer repairs.

---

### 4. High-gonality divisor dictionary

**Core trick.** Embed triple columns as divisors on an explicit high-gonality graph or curve. Arrange that a matching yields a low-degree effective representative of the target divisor class, while an illegal cover should require a high-degree Riemann–Roch representative.

**Expected move.** Gonality supplies a genuinely global norm-versus-effectivity theorem rather than local consistency tests.

**Map check.** O1’s linear cube relation survives the divisor map; this route survives only if minimum effective degree, not linear rows, separates the resulting classes. O2–O3 are outside global divisor equivalence. O4 is irrelevant. O5 threatens once effectivity is represented by signed lattice coefficients. O6 has polynomially many triple/divisor columns. O7 is unused; all divisor superpositions must be attacked directly. O8 applies after reducing the divisor-class system to a binary syndrome.

**Falsification.** An illegal all-eight, holonomy, or affine-closure divisor has degree within a constant factor of a legal representative.

**Smallest experiment.** Use a 10–20 vertex high-girth graph, assign divisors to the tiny 3DM suite, and compute exact Baker–Norine ranks and minimum effective degrees by integer programming.

**Likely death.** Principal divisors are linear: odd sums of cheap legal equivalences remain cheaply principal.

---

### 5. Exact order-two lattice OR gate

**Core trick.** For binary fibers with representatives \(v_i\) and lattices \(\Lambda_i\), set  
\[
\Lambda'=(\Lambda_1\oplus\Lambda_2)+\mathbb Z(v_1,v_2),\qquad v=(v_1,0).
\]
Because \(2(v_1,v_2)\in\Lambda_1\oplus\Lambda_2\), the two quotient cosets give exactly  
\[
\operatorname{dist}(v,\Lambda')^2=\min(d_1,d_2).
\]

**Expected move.** Combine this exact OR with direct-sum AND, seeking a shared-substructure Shannon recursion or branching-program compilation that amplifies rejection without tensoring.

**Map check.** O1–O6 remain relevant inside leaves but do not attack the exact two-coset switch itself; it uses neither local views nor witness fingerprints. O7 is completely avoided. O8 applies exactly: \(\Lambda'\) is again a mod-2 lattice after adding the switch vector to the code.

**Falsification.** Any polynomial sharing scheme either permits inconsistent branch reuse or has rank matching the full \(2^n\) decision tree.

**Smallest experiment.** Verify the identity for all pairs of existing tiny fibers, then compile the three-variable all-eight formula by Shannon expansion and enumerate every lattice coset word; include holonomy fibers as adversarial leaves.

**Likely death.** Exact OR works, but general SAT decision diagrams require exponential rank.

---

### 6. Nonabelian filling-area amplifier

**Core trick.** Encode assignment consistency as a word in a finitely presented group with large Dehn function. Legal witnesses reduce to the identity with a short prescribed diagram; rejected words are intended either to remain nontrivial or require polynomially larger filling area, which becomes coefficient cost.

**Expected move.** Nonabelian filling area could charge odd holonomy even when ordinary homology declares the defect trivial.

**Map check.** O1 is avoided by the full ordered word, but any bounded Fox/Magnus truncation is covered. O2 applies if van Kampen diagrams are implemented by bounded-fan-in cell tableaus. O3 does not cover the global word problem. O4’s abelian, single-valued phase assumptions do not cover nonabelian fillings. O5 applies after abelianizing relator counts. O6 uses a fixed polynomial presentation. O7 is unused; all mixed fillings require soundness. O8 needs a binary linearization preserving order and area, presently missing.

**Falsification.** Abelianized all-eight or holonomy words have constant-area fillings, or binary linearization introduces a pointed kernel.

**Smallest experiment.** Encode the hostile words in a small Baumslag–Solitar-type presentation; enumerate diagrams up to area 12 and compare full words, Fox derivatives, and resulting binary spans.

**Likely death.** Lattice linearization forgets word order; preserving it requires exponentially many diagram states.
