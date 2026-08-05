Below, “frontier” means the **ramified adverse-filtration lemma**. These are deliberately nonconvergent: some seek proofs, others systematic counterexamples, and one conditionally amends the single-prime edge.

### 1. Rees-module exactness certificate — prove

**Mechanism.** Package every depth-\(h\) adverse quotient as a filtered \(\mathcal O\)-module \(M_h\), and form its Rees module \(\bigoplus_k\mathfrak P^kM_h\,t^k\). Seek a gate library giving an exact recurrence whose associated-graded map has no false-root class in degrees \(<h\); filtered Nakayama plus saturation would then force either a \(\mathfrak P^h\) defect or large coefficients.

**Expected move.** Prove FRONTIER inductively without finite transfer tables.

**Obstruction audit.** G1/G6/G7/G12: not outside—every slack, quotient, carry and DROP row enters \(M_h\). G2/G3/G14/G31/G38: outside their bounded-test assumptions because the certificate is saturated and symbolic in \(h\). G5/G9/G11/G13/G15 and G19/GD1/ordered-pair: not outside; they must vanish as degree-zero classes or syzygies. G28/G32/G37: no min-plus or additive metric recurrence. G30: no tensor. GD2/A5: division removes nilpotents, but units remain audited. G33/G34, D4 variants, E6: no tags, Gram repair, shells, or affine shell ports.

**Falsifier.** Any degree-zero false-root class in the Rees homology.

**Experiment.** For one NAND and one COPY module with at most eight selectors, compute \(\operatorname{gr}_{\mathfrak P}\) through depth two and its exact syzygies in Sage/Magma.

**Likely death.** A G13- or diagonal-G19 class survives in degree zero.

---

### 2. Rational–local lifting of a valuation-zero pseudosection — refute

**Mechanism.** Search first for a false-root solution in the rational affine fiber, then use Smith invariants to test whether it is integral at every bad prime. A residue pseudosection over \(\mathbb F_{17^2}\) that lifts through the relevant \(\mathfrak P\)-power and satisfies all other SNF divisibility conditions yields an exact integral, valuation-zero counterexample—not merely a \(17\)-adic one.

**Expected move.** Refute FRONTIER by producing \(A_hz=b_h\) with energy \(O(N_h)\) and no \(\mathfrak P^h\) defect.

**Obstruction audit.** G1/G6/G7/G12 are included in the exact matrix. G2/G3 are met by rational elimination and full SNF, not a coefficient box. G5/G9/G11/G13/G15 and G19/GD1/ordered-pair are candidate generators rather than claimed escapes. G14/G31/G38 are irrelevant finite passes; the witness is exact. G28/G32/G37 and G30 are not used. GD2/A5 nilpotents are unnecessary; valuation-zero units suffice. G33/G34, D4 variants, and E6 assumptions are absent.

**Falsifier.** Rational inconsistency, or an SNF divisibility failure at any prime.

**Experiment.** Enumerate surviving depth-one modules over \(\mathbb F_{289}\); for each, form the depth-two false-boundary matrix, compute rational consistency and complete SNF, then minimize anchor energy in the exact fiber.

**Likely death.** Adverse graded injectivity blocks the residue seed before lifting.

---

### 3. Noncatastrophic quaternionic convolutional code — prove

**Mechanism.** Regard a depth path as a time-varying convolutional code over the local noncommutative DVR \(\mathcal O_{\mathfrak P}\). Design NAND/COPY transition matrices so their adverse encoder is noncatastrophic: every valuation-zero input trajectory with false terminal state has nonzero syndrome, while zero syndrome forces an invariant factor \(\pi^h\).

**Expected move.** Convert noncatastrophicity and local Smith invariant growth directly into the FRONTIER dichotomy.

**Obstruction audit.** G1/G6/G7/G12: all carries and boundaries are encoder outputs. G2/G3/G14/G31/G38: the criterion quantifies over the complete local module and all lengths, not a shell. G5/G9/G11/G13/G15: excluded only if the unit invariant factor is absent. G19/GD1/ordered-pair: arbitrary-state and non-rank-one trajectories are included. G28/G32/G37: invariant factors replace min-plus/additive costs. G30: state-space composition, not tensoring. GD2/A5: no zero divisors, but catastrophic unit modes remain possible. G33/G34, D4 variants, E6: no geometric tags or ports.

**Falsifier.** A valuation-zero catastrophic trajectory with false terminal state.

**Experiment.** For each eight-selector candidate, compute local Smith forms of every legal/adverse depth-two and depth-three transfer product; reconstruct the shortest catastrophic trajectory exactly over \(\mathcal O\).

**Likely death.** NAND semantics forces a common unit-mode shared by legal and adverse encoders.

---

### 4. Determinantal-valuation stratification — prove or expose low-rank escape

**Mechanism.** Represent every signed child coupling by a matrix and stratify it by rank. Track the \(\mathfrak P\)-valuations of all Fitting ideals; Cauchy–Binet can make these valuations additive through substitution even when the coupling is entangled, while a noncommutative Hadamard bound converts a large minor into selector energy.

**Expected move.** Prove FRONTIER separately on every rank stratum, or identify the precise low-rank stratum where it fails.

**Obstruction audit.** G1/G6/G7/G12 remain emitted coordinates. G2/G3/G14/G31/G38 are escaped only if all Fitting ideals are handled symbolically, not by enumeration. G5/G9/G11/G13/G15 occupy rank-deficient strata and are explicitly included. G19/GD1/ordered-pair are the central non-rank-one test. G28/G32/G37: multiplicative determinantal valuation, not additive cost. G30: exterior powers are proof invariants, not literal tensors. GD2/A5: division helps, but singular matrices still exist. G33/G34: exterior algebra is not emitted as a tag or repaired Gram. D4 variants and E6 are inapplicable.

**Falsifier.** A false-root rank-\(r\) coupling whose nonzero Fitting ideal stays valuation zero at every depth.

**Experiment.** Expand \(\mathcal O\) in an integral basis; enumerate depth-two couplings of rank at most two and compute exact determinantal ideals and energies.

**Likely death.** Diagonal G19-type splices live in a singular stratum invisible to maximal minors.

---

### 5. Twisted relative homology and torsion growth — prove

**Mechanism.** Build the recursive gate system as a relative chain complex with false root as a boundary class and glue maps twisted by multiplication by \(\pi\). If its mapping cone is rationally acyclic but has relative torsion \(\mathcal O/\mathfrak P^h\), any integral filling must either leave a \(\mathfrak P^h\) defect or use coefficients large enough to pay the required trace energy.

**Expected move.** Replace gate-by-gate reasoning with an integral filling inequality derived from Reidemeister/Fitting torsion.

**Obstruction audit.** G1/G6/G7/G12 are part of the relative boundary map. G2/G3/G14/G31/G38 are outside finite-shell assumptions only if the chain contraction is uniform in \(h\). G5/G9/G11/G13/G15 are relative \(H_0\) classes; G19/GD1/ordered-pair are \(H_1\) cycles and must be killed integrally. G28/G32/G37: no min-plus recurrence. G30: no tensor. GD2/A5: coefficients lie in a division order, though unit homology remains dangerous. G33/G34, D4 variants, E6: no metric tags, shells, or affine ports.

**Falsifier.** Primitive relative homology or a short filling despite torsion \(\mathfrak P^h\).

**Experiment.** Construct depth-one and depth-two mapping cones for the smallest NAND/COPY candidate; compute SNF, torsion order, and the exact shortest false-boundary filling.

**Likely death.** Large torsion controls index but not the shortest vector in the affine fiber.

---

### 6. Parallel ramified primes with a resultant certificate — conditional roadmap amendment

**Mechanism.** Run the same integer selectors through two or three definite quaternion orders ramified at different primes, emitting every module’s coordinates. If single-prime unit pseudosections differ, an explicit resultant of their adverse equations may show that no common integral unit class survives; accumulated prime divisibility then gives product-norm growth.

**Expected move.** Amend the single-\(\mathfrak P\) frontier only after exhibiting a valuation-zero attack for each individual prime and proving their shared-selector intersection trivial. This is justified because the obstruction map contains no multi-prime no-go, while G13 warns that a common integral affine class would immediately kill the amendment.

**Obstruction audit.** G1/G6/G7/G12 are emitted in every branch. G2/G3 require combined SNF over all coefficients. G5/G9/G11/G13/G15 and G19/GD1/ordered-pair are not escaped unless the combined kernel rejects them. G14/G31/G38 remain merely finite evidence. G28/G32/G37: parallel arithmetic norms, not copy-additive amplification. G30: no tensor. GD2/A5: each order is division; unit intersections remain audited. G33/G34, D4 variants, E6 do not apply.

**Falsifier.** Any common valuation-zero pseudosection, especially an honest-affine integral one.

**Experiment.** Couple identical eight-selector incidence matrices in orders ramified at \(17\) and \(19\); compute the combined depth-two SNF and exact minimum.

**Likely death.** The harmful kernel is combinatorial and therefore survives every prime simultaneously.

---

### 7. Presburger “pump-or-rank” classification — prove or refute

**Mechanism.** Encode the complete saturated port relation of a gate as an affine semigroup with congruence labels for \(\mathfrak P\)-valuation. Compute Hilbert bases under recursive composition: a pumpable valuation-zero cycle gives counterexamples at all depths, while absence of such a cycle may admit a linear ranking functional increasing filtration once per level.

**Expected move.** Produce either an explicit infinite counterexample family or a machine-checkable all-depth ranking certificate for FRONTIER.

**Obstruction audit.** G1/G6/G7/G12 are generators and relations, not external filters. G2/G3 are addressed through unbounded affine semigroups. G14/G31/G38 are surpassed only if the certificate proves closure for every depth. G5/G9/G11/G13/G15 and G19/GD1/ordered-pair become primitive Hilbert-basis cycles. G28 is avoided because full coefficient semigroups replace a finite min-plus cost table; G32/G37 additive cycles would be detected as pumps. G30 and GD2/A5 convolution are unused. G33/G34, D4 variants, and E6 lie outside the semigroup model.

**Falsifier.** A primitive unit-valued cycle whose composition preserves false boundary and linear energy.

**Experiment.** Export one NAND/COPY candidate to Normaliz or 4ti2, compute saturated depth-one relations, compose once, and search for a pump plus a Farkas ranking certificate.

**Likely death.** Recursive projection causes uncontrollable Hilbert-basis growth or a non-semilinear reachability relation.
