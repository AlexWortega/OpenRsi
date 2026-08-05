1. **Degree-raising Möbius/Fourier moments**

**Mechanism:** View each clause selector as a signed measure on \(\{0,1\}^3\), and add its degree-3 Möbius character alongside the existing singleton/pair moments. More generally, use deterministic splitter families to expose bounded-order alternating cubes without listing all global subsets.

**Expected move:** The Generation-9 cube-parity vector is invisible through degree two but has nonzero top-degree character; zero-completeness rows could then be scaled polynomially.

**Obstruction audit:** G1 slack annihilation: outside—no residual slack variables. G2–3 local isolation: outside—uses global moments, not fixed local marginals or the 18 matrices. G5 private-row overlap: outside—moments are identified globally across occurrences. G6 invalid quotient: all moment rows must be emitted in the basis and optimized unrestrictedly. G7 radix kernel: the old affine kernel is not a kernel of the cubic character. G9 parity kernel: specifically targeted by degree three.

**Falsification:** Find a constant-cost degree-4 alternating cube, or any cubic-zero signed selector on the nine-clause instance.

**Smallest experiment:** Add all global triple-moment rows to `verify_global_psd_metric.py`; recompute exact minima for the obstruction and control.

**Likely death:** Every fixed degree admits the next-order parity kernel; logarithmic degree may cause quasipolynomial dimension.

---

2. **Nonlinear \(B_h\)/Sidon signatures for local labels**

**Mechanism:** Assign the eight local patterns integer codewords \(c(a)\) from a bounded-order Sidon set, so no short signed combination of codewords can impersonate another pattern. Couple these signatures to shared global variable symbols, then concatenate them with a small explicit expander code so one nonzero syndrome occupies many coordinates.

**Expected move:** Rule out every signed selector within a provable anchor-excess bound, then scale the zero-on-honest syndrome block by \(n^\alpha\).

**Obstruction audit:** G1: no free slack. G2–3: does not use affine-isolation matrices. G5: signatures are checked against shared global symbols, not private marginals. G6: normalization, coupling, and code checks are lattice coordinates, never filters. G7: the old relation only survives if it is also a relation among the new codewords. G9: choose \(B_h\) order high enough to cover the seven-term parity witness; this must be verified, not assumed.

**Falsification:** Consistency with global variables forces \(c\) to be affine, recreating cube relations, or a short signed relation survives.

**Smallest experiment:** Search \(c(a)\in[-M,M]^m\) for \(m=2,3\), minimizing the shortest forbidden relation through anchor excess 24; embed the best code into the nine-clause verifier.

**Likely death:** Nonlinear signatures may be incompatible with zero-cost overlap consistency, while bounded \(h\) leaves larger constant circuits.

---

3. **High-systole chain-complex encoding**

**Mechanism:** Encode selector configurations as integral 1-chains, normalization/consistency as boundary equations, and additional overlap tests as coboundary equations. Lift the formula complex into an explicit high-systole cover so any non-honest harmonic or homologically nontrivial chain must have polynomial support.

**Expected move:** Convert constant-support signed-selector circuits into long cycles, making their Euclidean cost grow with the lift size.

**Obstruction audit:** G1: no slack directions. G2–3: local certificates are replaced by a global chain complex. G5: a private-clause circuit must extend to a global cycle in the lift. G6: both boundary and coboundary operators are emitted lattice rows. G7: zero raw residual is insufficient unless the vector also has zero coboundary. G9: the cube parity must either acquire coboundary energy or become a long lifted cycle; if it remains a small harmonic chain, this mechanism is not outside the obstruction.

**Falsification:** Exhibit a bounded-support integral harmonic chain in every tested lift.

**Smallest experiment:** Build a two- or four-sheet lift of the nine-clause incidence complex; compute SNF homology and enumerate shortest chains with zero boundary and coboundary.

**Likely death:** Formula-derived complexes may necessarily retain local contractible circuits; obtaining the required expansion may secretly amount to forbidden PCP-style amplification.

---

4. **Generic equal-radius Gram isolation**

**Mechanism:** Search over rational positive-definite Gram matrices \(Q\) subject only to every honest Boolean witness having the same completeness norm. A symbolic perturbation or moment-curve parameterization should avoid the algebraic hypersurfaces on which any particular bounded signed deviation remains cheap.

**Expected move:** Simultaneously charge all deviations through anchor excess \(K\), including cube parity, and then scale directions that vanish on honest witnesses.

**Obstruction audit:** G1: there are no residual slacks. G2–3: no reliance on local affine inconsistency. G5: \(Q\) may contain cross-clause blocks, so private circuits are not protected. G6: the rational factor of \(Q\), center, basis, and target must be emitted and unrestrictedly audited. G7: \(Az=0\) under the radix system does not imply zero energy under a coefficient-space \(Q\). G9: this strictly enlarges the tested two-parameter degree-two metric; however, equal-radius constraints may still force its parity symmetry.

**Falsification:** Linear algebra shows the cube-parity deviation lies in the common nullspace of every admissible equal-radius perturbation.

**Smallest experiment:** Enumerate deviations of anchor excess at most 24, solve an SDP maximizing their minimum energy, rationalize the result, and verify it by exact DP.

**Likely death:** Equal completeness for exponentially many assignments may collapse admissible \(Q\) to a highly symmetric family with unavoidable constant circuits.

---

5. **Tensor or exterior-power gap multiplication**

**Mechanism:** Tensor a fixed-target CVP embedding with itself, adding Plücker-type coordinates intended to make close vectors decomposable. If unrestricted distance were multiplicative rather than merely multiplicative on rank-one witnesses, a constant ratio \(>1\) could become polynomial after \(O(\log n)\) products.

**Expected move:** Turn the Generation-9 finite ratio \(\sqrt{4/3}\) into \(n^c\), conditional on proving an anti-entanglement lemma and controlling dimension.

**Obstruction audit:** G1: no slack is introduced. G2–3 and G5: tensorization is global and does not rely on local composition. G6: all product and Plücker coordinates must be intrinsic; no rank-one search restriction is allowed. G7: not automatically outside—the old zero-residual witness may tensor to another cheap vector. G9: directly uses its finite gap, but the constant parity witness may create entangled sums cheaper than the tensor prediction.

**Falsification:** Find a non-decomposable lattice vector below the product of the two exact base minima.

**Smallest experiment:** Tensor-square the smaller all-eight-clauses three-variable embedding; enumerate low-support coefficient matrices and compare against the predicted squared product distance.

**Likely death:** CVP tensor products admit entangled integer combinations, and \(D^{O(\log n)}\) dimension may already be quasipolynomial.

---

6. **Macaulay/Nullstellensatz lattice lift**

**Mechanism:** Form the degree-\(d\) Macaulay matrix of the Boolean equations and clause polynomials, with monomial-consistency equations represented as actual lattice coordinates. An unsatisfiability certificate \(1=\sum_i q_i f_i\) would become a dual integer functional forcing every candidate away from the target.

**Expected move:** Degree three should detect the cube-parity pseudoassignment; a bounded-degree certificate theorem would supply global soundness and scalable dual separation.

**Obstruction audit:** G1: monomial variables could become slack, so every multiplication/Boolean consistency equation must be charged; otherwise G1 applies unchanged. G2–3: unrelated to local affine isolation. G5: shared monomials make the construction global. G6: no pseudoexpectation or normalization may remain external. G7: the old affine kernel need not survive the lifted polynomial equations. G9: degree-three equations directly test the missing top cube moment.

**Falsification:** A low-degree integral pseudoassignment satisfies all emitted rows cheaply, or the required degree grows with the formula size.

**Smallest experiment:** Generate degree-3 Macaulay matrices for the obstruction and satisfiable control; compute exact ranks, SNF invariants, dual certificates, and unrestricted CVP minima.

**Likely death:** General 3SAT instances can require high algebraic proof degree, making the Macaulay lift exponential; coefficient growth may also destroy the intended radius.

---

7. **Intrinsic multi-prime Construction-A barrier**

**Mechanism:** Give each pattern a degree-three Vandermonde signature and enforce its syndromes simultaneously modulo several small primes using Construction-A lattices. Balanced representatives and charged carry vectors keep all modular behavior inside the CVP instance; CRT then certifies that a bounded nonzero signature cannot vanish everywhere.

**Expected move:** Detect bounded signed deviations with at least one prime and assign that syndrome a polynomial geometric scale while honest signatures remain in the designated coset.

**Obstruction audit:** G1: outside only if every carry vector is charged at the same scale—free carries would exactly recreate slack annihilation. G2–3: uses global modular signatures, not the local survivor. G5: occurrence symbols are shared across all prime blocks. G6: congruences, carries, normalization, and target cosets are emitted, with unrestricted coefficients. G7: any exact integer relation survives all primes unless the new nonlinear signature breaks it; primes alone do not help. G9: degree-three signature should detect cube parity, but this requires an explicit calculation.

**Falsification:** A cheap combination of Construction-A \(p\)-multiple vectors cancels every syndrome, or the parity vector remains signature-zero.

**Smallest experiment:** Use primes \(2,3,5\) on the nine-clause instance, emit the complete basis/target, and branch-and-bound the exact minimum.

**Likely death:** Carry vectors restore cheap cancellation, while increasing prime scales may enlarge the honest completeness radius at the same rate.
