**Compliance note:** No content from, or coverage of, the prohibited document was recalled, searched, or used. Everything below rests on the attached files and classical pre-existing literature.

**Obstruction map (as proved/gated in the files):**
- **O1 — Slack-cheat:** free unamplified integer directions can zero every amplified coordinate at O(1) anchor cost (certified: 27 vs 19).
- **O2 — Affine-linearity:** CVP coordinates are affine in the integer coefficients; quadratic penalties like `s(s−1)` are not directly realizable.
- **O3 — No-asymptotics:** a finite constant ratio on one instance promotes nothing; every mechanism needs an explicit dimension-vs-gap scaling law.
- **O4 — No-unverified-transfer:** variants may not be credited or pruned by analogy; each needs its own executable test.
- **O5 — Completeness-inflation** (Pro blocker 3): amplification that raises soundness energy while proportionally raising baseline cost yields only a constant ratio.

---

**1. Coset/syndrome rigidity: slacks confined to a high-distance code lattice (coding theory)**

*Trick.* Keep clause selectors/slacks, but make the slack vector the message of a Construction-A lattice from an expander code (or BCH). Heavy affine parity-check coordinates force the slack vector into a coset determined by clause values; deviating from the honest slack requires either a codeword move (ℓ₂ cost ≥ d = Θ(m)) or paying Δ violated parities per flipped bit.

*Obstructions.* O1: attacks it head-on — the gen-1 cheat `(−1,0)` now flips a syndrome, costing Θ(Δ), not O(1); correlated cancellations must be searched, not assumed. O2: parities are affine ✓. O3: d and Δ scale linearly — explicit law ✓. O4: needs its own exact search ✓. O5: honest slacks sit in the zero-syndrome coset at zero parity cost, so baseline stays at anchor cost; must verify baseline doesn't secretly scale with d — this is the test.

*Expected move.* Constant → polynomial gap inside one gadget.

*Falsification.* An integer point below baseline + d with all parity blocks zero.

*Experiment today.* Eight-clause formula, slack vector coded by the [7,4,3] Hamming Construction-A lattice, exact search as in gen-1.

*Likely death.* A correlated direction mixing variable, slack, and code coordinates that lies in the code yet cancels residuals — d pays but residual saves more.

---

**2. Homological filling area in an expanding 2-complex (topology)**

*Trick.* Map the formula to a 2-complex X; the target is an integer 1-cycle z, the lattice is im(∂₂) on integer 2-chains. SAT ⇒ an explicit small filling; UNSAT ⇒ any integer chain near z must have area ≥ A·n^c by an isoperimetric (filling) inequality of the complex (Gromov filling, cf. Ramanujan-complex expansion, Lubotzky et al., pre-2015).

*Obstructions.* O1: there are no auxiliary slacks — every integer degree of freedom is a 2-chain whose cost *is* its norm, so no unamplified directions exist by construction ✓. O2: ∂₂ is a linear map ✓. O3: isoperimetric constants give the scaling law, if proved ✓. O4: needs its own ILP test ✓. O5: honest filling must have area O(poly) with the isoperimetric constant beating it — explicit and checkable.

*Expected move.* Soundness from geometry of the complex instead of algebra of residuals.

*Falsification.* A cheap 2-chain filling z up to a low-cost defect on an UNSAT instance.

*Experiment today.* Encode the 8-clause formula as a small complex (~100 triangles); compute exact minimal filling norms with an ILP solver.

*Likely death.* UNSAT only kills *exact* fillings; near-fillings with a one-clause defect stay cheap — the falsified clause localizes again.

---

**3. Dual-certificate soundness (Fourier/Banaszczyk transference)**

*Trick.* Prove soundness in the dual: if w ∈ L* has ⟨w,t⟩ ≡ 1/2 (mod 1) then dist(t,L) ≥ 1/(2‖w‖). Design the reduction so UNSAT yields an explicit short dual vector (an F₂-parity combination of gadget rows) with ‖w‖ ≤ n^{−c}, while SAT destroys all such combinations.

*Obstructions.* O1: genuinely outside its assumptions — the dual bound holds against *every* integer point, so no primal cheat, slack or otherwise, can beat it ✓. O2: irrelevant; dual vectors aren't gadget coordinates ✓. O3: ‖w‖ gives the scaling law explicitly ✓. O4: needs its own check ✓. O5: completeness requires SAT ⇒ a genuinely close vector, verified separately.

*Expected move.* Replaces cheat-enumeration soundness (the entire gen-1 failure mode) with a one-line certificate.

*Falsification.* An UNSAT instance in the gadget family with no short half-integral dual vector.

*Experiment today.* Build the gen-1 lattice's dual basis; LLL-search for w with ⟨w,t⟩ ≈ 1/2; compare 1/(2‖w‖) against the certified 27.

*Likely death.* 3SAT ≠ 3XOR: general unsat formulas have no F₂-parity refutation, so the certificate family is incomplete; widening it walks into proof-complexity lower bounds.

---

**4. Agreement-testing / derandomized direct product (PCP-adjacent but standalone combinatorics)**

*Trick.* Replicate variables across overlapping blocks on a Johnson scheme or high-dimensional expander; coordinates are affine consistency differences (x_{B,i} − x_{B′,i}) plus per-block clause residuals. Standalone agreement theorems (e.g., Dinur–Steurer 2014, whose proofs are self-contained combinatorics, not PCP machinery) force any low-inconsistency table near a global assignment, so one falsified clause replicates across a constant fraction of blocks.

*Obstructions.* O1: consistency coordinates penalize the *table*, not residuals, so the residual-zeroing cheat must corrupt many block copies — but non-Boolean per-block values are a live O1 surface; honest flag. O2: differences are affine ✓. O3: #blocks = poly gives scaling ✓. O4: own test needed ✓. O5: **the known weak point** — honest anchors cost Θ(#copies) while soundness adds Θ(#copies), a constant ratio unless per-violation weight grows; must design weights so baseline is o(soundness).

*Expected move.* Combinatorial (not algebraic) spreading of a single violation.

*Falsification/experiment today.* 3 variables, all 3-subsets as blocks; exact search for a table beating baseline + (fraction)·(#blocks).

*Likely death.* O5: completeness inflation caps the ratio at a constant.

---

**5. Graver-basis / kernel-distance engineering (integer programming + coding)**

*Trick.* Write the formula as Ax = b over ℤ and engineer A (expander bipartite structure, weighted columns) so the integer kernel lattice ker_ℤ(A) has minimum ℓ₂-distance n^c — every integer move away from the designated honest point costs polynomially. Distance-to-target measures deviation; UNSAT removes all cheap feasible points.

*Obstructions.* O1: the cheat directions *are* the kernel vectors; the mechanism is literally "make all of them long" — O1 becomes a design target, checked by computing the kernel's minimum distance, not assumed ✓. O2: everything affine ✓. O3: min-distance vs dimension is the explicit law ✓. O4: own computation required ✓. O5: honest point at distance O(1) if b is exactly achievable under SAT — verify.

*Expected move.* Converts soundness into a static, formula-independent lattice-distance computation.

*Falsification.* A short Graver-basis element of A.

*Experiment today.* Run 4ti2/Normaliz on a 20×40 expander-structured A with OR-slack columns; report the shortest kernel vector.

*Likely death.* The OR-slack columns needed to express clauses reintroduce weight-2 kernel vectors — O1 resurrected through the encoding.

---

**6. Explicit deep-hole seed from Barnes–Wall / Reed–Muller lattices (lattice geometry)**

*Trick.* BW lattices in dimension N have explicit structure with λ₁ = Θ(√N) and explicitly describable cosets/deep holes (classical: Barnes–Wall 1959; Micciancio–Nicolosi 2008 decoding). Encode the assignment as a choice of coset representative: SAT steers the target into a coset with a point at distance O(1); UNSAT strands it at depth Θ(N^{1/4}) in ℓ₂.

*Obstructions.* O1: no slack variables — cheats are arbitrary lattice points, and the distance floor is λ₁ of the sublattice, a static geometric fact ✓; but the affine SAT→coset steering logic is a new O1 surface and must be searched. O2: coset selection is affine ✓. O3: √N law explicit ✓. O4: own enumeration ✓. O5: completeness O(1) by construction — verify on the SAT analog.

*Expected move.* Polynomial gap from a *fixed* lattice's geometry; the formula only routes the target.

*Falsification.* A lattice point near the target on an UNSAT instance via a coset not reachable by any Boolean assignment.

*Experiment today.* BW₁₆: exhaustive coset enumeration for a 3-variable formula wired into coset selection.

*Likely death.* Steering requires OR-logic in the coset map; affine maps can't compute OR, forcing selectors back in (O1) or nonlinearity (O2).

---

**7. Tensor self-amplification of a constant-gap seed (Khot/Haviv–Regev-style, adapted)**

*Trick.* Given any seed with certified constant gap γ (even √(27/19)-scale, or a seed from sketches 1/6), amplify by k-fold lattice tensoring: completeness multiplies exactly; prove soundness multiplies for *structured* seeds (analogous to Haviv–Regev's SVP tensor lemma, STOC 2007, which is classical and PCP-free).

*Obstructions.* O1: inherited from the seed only; tensoring adds no new slack directions if the soundness lemma holds — must be verified, not transferred (O4). O2: tensor bases are explicit integer matrices ✓. O3: **honest failure flag** — dimension d^k vs gap γ^k gives exponent log γ/log d, which *shrinks* as seed dimension grows with n; this yields 2^{(log N)^{1−ε}}-type gaps, not n^c, unless the seed gap itself is polynomial. So this is a booster, not a standalone route. O5: completeness multiplies too — ratio is what tensors; fine.

*Expected move.* Any constant-gap seed from sketches 1, 3, or 6 → superconstant gap.

*Falsification.* dist(t⊗t, L⊗L) < dist(t,L)² on the seed.

*Experiment today.* Tensor the gen-1 27/19 instance with itself; exact search the resulting lattice; check whether 27² is the optimum.

*Likely death.* CVP soundness provably fails to tensor for generic instances; and even if it holds, O3's exponent calculus caps it below n^c.

---

**Portfolio note.** Sketches 1, 5, and 6 attack O1 by *deleting or pricing* cheat directions (three different pricing mechanisms: syndromes, kernel distance, fixed-lattice λ₁); sketch 3 sidesteps primal cheats entirely via duality; sketches 2 and 4 relocate soundness to geometry/combinatorics; sketch 7 is a multiplier for whichever seed survives. Per O4, none of these may be pruned or promoted without its own exact small-instance search.
