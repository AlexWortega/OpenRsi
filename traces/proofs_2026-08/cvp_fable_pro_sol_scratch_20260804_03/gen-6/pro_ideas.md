I use seven obstructions from the current map: **Slack annihilation** (G1), **fixed-marginal locality** (G2–3), **overlap/cross-clause kernels** (G5), **missing polynomial amplification**, **missing explicit CVP realization**, **bounded-search versus unbounded/global certification**, and **incomplete experimental provenance**.

### 1. Tensor-power Voronoi shell gadget

**Core trick.** Search for a constant-dimensional lattice coset whose nearest vectors are exactly the seven satisfying clause labels, while every forbidden or signed-selector state lies in a second shell with ratio \(\rho>1\). Tensor the coset \(k=\Theta(\log m)\) times and glue variable labels diagonally rather than through private syndrome rows.

**Expected move.** One bad block costs \(\rho^{2k}\); choosing \(\rho^{2k}\ge m^{1+\epsilon}\) gives a polynomial global ratio in output dimension \(N=m d^k\).

**Obstruction audit.** **Slack:** no residual slack exists. **Fixed marginals:** does not use the 18 survivors. **Overlap kernels:** not escaped automatically; tensor-gluing must defeat joint mixed vectors. **Amplification:** explicit multiplicative shell law. **CVP realization:** the search outputs \(B,t,R\), with tensor bases explicit. **Unboundedness:** requires a shell theorem via Gram-form lower bounds, not boxed enumeration. **Provenance:** regenerate candidates and hashes independently.

**Falsification test.** Tensor square contains a mixed lattice vector below the claimed second shell, or two-clause gluing restores a short vector.

**Smallest experiment.** Enumerate \(d\le6\), \(B_{ij}\in[-2,2]\), target denominator \(\le6\); test seven nearest labels, tensor square, and one shared-variable pair.

**Likely death.** Tensor products create non-pure short vectors, destroying \(\rho^k\).

---

### 2. Construction-A code on the global selector quotient

**Core trick.** Form the global integer selector module and quotient it by all honest assignment differences, normalization relations, and variable-consistency relations. If every low-cost dishonest selector has a nonzero quotient syndrome, encode that syndrome with an explicit high-distance \(q\)-ary code and realize it through a Construction-A lattice.

**Expected move.** A nonzero syndrome produces \(\Omega(D)\) Euclidean residual energy. Taking \(D=m^3\) against \(O(m)\) completeness energy suggests ratio \(\Omega(m)=\Omega(N^{1/3})\).

**Obstruction audit.** **Slack:** auxiliaries are included before quotienting, so annihilating slack merely yields zero quotient and falsifies the premise. **Fixed marginals:** global module, not local fibers. **Overlap kernels:** all occurrences and joint moves enter one quotient; whether it is nontrivial is open. **Amplification:** code distance supplies the law. **CVP realization:** Construction A gives basis, modular target, and radius accounting. **Unboundedness:** Smith normal form plus a coding theorem can certify all integers. **Provenance:** independently recompute the module and code checksums.

**Falsification test.** A harmful signed selector lies in the honest-generated subgroup.

**Smallest experiment.** Build the complete global module for the unsatisfiable eight-clause three-variable formula; compute SNF and enumerate harmful vectors of squared norm \(\le12\).

**Likely death.** Honest-assignment differences may span every harmful direction, making the quotient trivial.

---

### 3. Homological non-fillability and cosystolic amplification

**Core trick.** Encode occurrence labels as integral \(1\)-chains and clause/variable repairs as boundaries of \(2\)-cells. Design the formula complex so satisfiable instances yield a boundary, while unsatisfiability leaves a nonzero homology class; amplify its minimum representative using a deterministic product or cover with large cosystole.

**Expected move.** A product complex of size \(D=m^3\) with cosystole \(\Omega(D)\) would separate \(O(m)\) completeness energy from \(\Omega(D)\) soundness energy.

**Obstruction audit.** **Slack:** slack cells are boundaries and cannot erase a nonzero class. **Fixed marginals:** the invariant is global homology. **Overlap kernels:** local circuits are harmless only if boundaries; joint cancellation could still trivialize the class and must be tested. **Amplification:** supplied by cosystole growth. **CVP realization:** use the integer boundary lattice \(\operatorname{im}\partial_2\), reduced to an independent HNF basis, with target chain explicit. **Unboundedness:** SNF certifies homology exactly; a genuine cosystolic theorem is still missing. **Provenance:** record boundary matrices and independent SNF results.

**Falsification test.** The unsatisfiable target class is already zero, or products admit small representatives.

**Smallest experiment.** Search small \(2\)-complex templates for the eight-clause core; compute integral homology and exact minimum class weight.

**Likely death.** Cross-clause compensation becomes a filling, or the needed cosystolic amplification implicitly requires PCP machinery.

---

### 4. Bose–Chowla-style short-relation barrier

**Core trick.** Assign global selector deviations additive signatures forming a \(B_h\)-type set in a large cyclic group, while arranging every honest incidence move to cancel. Then no harmful relation of \(\ell_1\)-length at most \(h\) can vanish; longer relations already incur substantial selector norm.

**Expected move.** Choose \(h=m^{1+\epsilon}\). Repeat or code the modular signature so nonzero short relations are expensive, while exact-kernel relations have norm at least \(h/\sqrt{O(m)}\), yielding a polynomial gap with polynomial bit-length modulus.

**Obstruction audit.** **Slack:** slack signatures are included in the relation set, not left free. **Fixed marginals:** signatures are global. **Overlap kernels:** joint moves are exactly the additive relations being excluded. **Amplification:** combines relation length and repeated modular distance. **CVP realization:** modular rows admit a triangular/Construction-A basis. **Unboundedness:** an actual \(B_h\) theorem would cover all relations through \(h\); beyond \(h\), norm gives the bound. **Provenance:** deterministic signature generation and exhaustive small-relation verification.

**Falsification test.** Honest cancellation constraints force two harmful columns to have the same quotient signature.

**Smallest experiment.** On the eight-clause core, search prime moduli \(q<10^4\) and signatures excluding every harmful relation with \(\ell_1\le8\).

**Likely death.** The honest relation subgroup may collapse the additive code before any \(B_h\) separation remains.

---

### 5. Number-field Minkowski shell for signed selectors

**Core trick.** Embed selector columns as algebraic integers \(1,\alpha,\ldots,\alpha^{r-1}\) and use all \(D\) conjugate embeddings. Partition around each legal one-hot selector: any illegal integral affine combination produces a nonzero algebraic integer \(\beta\), whose product of conjugate magnitudes is at least one.

**Expected move.** AM–GM gives \(\sum_\sigma|\sigma(\beta)|^2\ge D\). With \(D=m^3\), zero-defect legal states retain \(O(m)\) anchor energy while illegal states acquire \(\Omega(D)\).

**Obstruction audit.** **Slack:** no clause residual is evaluated; every selector and auxiliary coefficient enters \(\beta\), so this differs from the killed algebraic-slack variant. **Fixed marginals:** powers are assigned globally. **Overlap kernels:** a joint move is detected unless its coefficient polynomial vanishes; degree \(<D\) would rule that out. **Amplification:** explicit product-formula bound. **CVP realization:** use the integral trace Gram matrix and a rational higher-dimensional Gram realization. **Unboundedness:** minimal-polynomial divisibility gives an exact certificate. **Provenance:** verify the polynomial, resultant, and Gram matrix independently.

**Falsification test.** A legal-span combination yields \(\beta=0\), or an illegal point beats the legal shell despite nonzero norm.

**Smallest experiment.** Degree \(8\) field, one clause then two overlapping clauses; enumerate coefficients of squared norm \(\le12\).

**Likely death.** Making all legal labels equal-radius may introduce small signed combinations across embeddings.

---

### 6. Deterministic splitter measurements for all short cheats

**Core trick.** Treat a hypothetical low-distance CVP witness as a sparse integer deviation after subtracting an honest selector flow. A deterministic splitter family hashes its support so some measurement isolates one nonzero coefficient; attach an outer distance code to the bucket syndromes.

**Expected move.** Soundness becomes a dichotomy: low-support deviations trigger \(\Omega(D)\) coded energy, while deviations outside the splitter threshold already have large Euclidean norm. Target \(D=m^3\) for an \(N^{\Theta(1)}\) ratio.

**Obstruction audit.** **Slack:** auxiliary columns are hashed too. **Fixed marginals:** hashes span all clause occurrences rather than private rows. **Overlap kernels:** joint support is included; this is precisely what the G5 test omitted. **Amplification:** outer code supplies distance. **CVP realization:** integer hash/code matrix plus identity padding gives a full-column-rank basis and explicit target. **Unboundedness:** splitter guarantees cover all supports up to \(T\); coefficient bounds must follow from the assumed short distance, not a box. **Provenance:** generate splitters deterministically and compare against brute force.

**Falsification test.** A norm-small harmful vector projects to an honest flow or cancels in every bucket.

**Smallest experiment.** Generate a \(T=4\) splitter for all selector/auxiliary columns of two overlapping clauses; enumerate joint moves of squared norm \(\le8\).

**Likely death.** The “subtract an honest flow” representation may fail, or dense \(\pm1\) deviations may remain too cheap.

---

### 7. Mixed-radix carry-chain amplifier

**Core trick.** Order the global consistency and legality detectors and connect each detector to an anchored base-\(B\) carry chain. A first nonzero integral defect must either propagate through \(k\) coordinates with geometric growth or be cancelled by carries whose anchor cost grows comparably.

**Expected move.** With \(B^k=m^a\) and \(k=O(\log m)\), any nonzero detector obtains polynomial energy using only \(O(m\log m)\) dimensions and polynomial-bit entries.

**Obstruction audit.** **Slack:** slack and carry variables are themselves anchored and amplified, directly targeting G1’s failure. **Fixed marginals:** detectors are global, not the 18 local matrices. **Overlap kernels:** cross-clause compensation is detected only if some global detector remains nonzero; exact detector-kernel cheats remain an honest unresolved risk. **Amplification:** geometric recurrence is explicit. **CVP realization:** the carry system is a triangular integer basis with an explicit target and full-rank check. **Unboundedness:** an induction/continued-remainder argument can cover all integer carries. **Provenance:** compare exact dynamic programming with independent lattice enumeration.

**Falsification test.** Carries cancel a unit defect at \(O(1)\) cost, or a harmful signed selector zeros every detector.

**Smallest experiment.** Add depth-\(4\), base-\(3\) chains to the eight-clause core and solve exactly by DP plus branch-and-bound.

**Likely death.** A balanced carry pattern may absorb defects without geometric cost; alternatively the unchanged global detector kernel survives.

Classical ingredients: Construction A as presented in Conway–Sloane, *Sphere Packings, Lattices and Groups*; Bose–Chowla, “Theorems in the Additive Theory of Numbers” (1962/63); and deterministic splitters from Naor–Schulman–Srinivasan, FOCS 1995.
