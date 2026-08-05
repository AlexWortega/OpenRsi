For compactness, the obstruction map below is: **O1** slack/carry or exact residual kernels (G1/G7); **O2** short overlap kernels (G5); **O3** externally filtered rather than unrestricted CVP evidence (G6); **O4** relocated bounded-degree parity (G9/G11); **O5** clause drops (G12); **O6** the nine-term honest-affine-span lift (G13/G15); **O7** finite pair-bag success without composition (G14); **O8** absence of a polynomial-size padded family with an \(n^c\) ratio.

### 1. Sparse Prony fingerprints of the violation measure
**Mechanism.** Index each global assignment by \(t(a)=1+\mathrm{bin}(a)\). For each clause, fingerprint the signed measure supported on assignments falsifying it by its first \(D\) moments \(\sum_a\mu_c(a)t(a)^j\); Vandermonde independence detects every nonzero measure of support at most \(D\).

**Expected move.** Taking \(D\ge9\) charges the exact G13 mixture; any surviving zero-fingerprint cheat must use growing support, hence potentially growing anchor cost.

**Obstruction check.** O1: the transcript prototype has no slack, though arithmetic-circuit compression would reintroduce it. O2: fingerprints are global, not private-overlap rows. O3: emit basis, target, and unrestricted transcript coefficients. O4: \(D\) grows, unlike fixed-degree moments. O5: a drop changes the zeroth moment. O6: the G13 violation measure should be detected, but this requires explicit global transcripts. O7: not a fixed bag lift. O8: polynomial compression is wholly unproved.

**Falsification.** A support-\(\le D\) zero-moment harmful vector, or a cheap unrestricted arithmetic-gate bypass.

**Smallest experiment.** On the four-variable obstruction, use 16 transcript columns and \(D=9\); emit HNF and search through \(B+32\).

**Likely death.** Global transcript enumeration is exponential; linearizing \(t(a)^j\) may restore O1/O6.

---

### 2. Fourier-uncertainty amplifier
**Mechanism.** Regard each clause’s signed falsifying-assignment measure as a function on \(\mathbb F_2^n\), and penalize Walsh coefficients rather than local moments. The full transform is injective, while finite-group uncertainty bounds make a sparse nonzero measure spectrally broad (cf. Donoho–Stark, 1989).

**Expected move.** Replace the full spectrum by a deterministic polynomial-size character sampler that gives every low-anchor harmful measure many nonzero coordinates.

**Obstruction check.** O1: the finite prototype uses direct \(\pm1\) rows and no carries. O2: characters span all variables. O3: all coefficients remain unrestricted. O4: high-weight characters escape fixed-degree parity relocation. O5: the DC character detects drops. O6: full Fourier detects the G13 violation measure rather than annihilating all honest differences; sampled Fourier may not. O7: this is global harmonic amplification, not pair bags. O8: the required deterministic sampler and local realization are missing.

**Falsification.** Find a harmful shell vector whose violation measure lies in the sampled Fourier kernel.

**Smallest experiment.** Add all 16 Walsh characters per clause to the four-variable instance and exactly enumerate the old shell; then greedily minimize the character set while retaining separation.

**Likely death.** Full Fourier has exponential size, and polynomial character sets may admit adversarial signed kernels or require exponentially large global-assignment selectors.

---

### 3. List-recoverable assignment-code lift
**Mechanism.** Encode the entire variable assignment by a systematic Reed–Solomon or algebraic-geometry code. Clause selectors expose short local views; list recovery should imply that a collection of mostly compatible legal views comes from only a small list of genuine global assignments.

**Expected move.** Reduce an arbitrary signed pseudoselector to a short list of assignments, then attach explicit violation fingerprints only to that list.

**Obstruction check.** O1: direct local-codeword selectors need no slack; field arithmetic auxiliaries would need auditing. O2: shared code symbols globally couple overlaps. O3: the experiment must include all view selectors unrestricted. O4: global code agreement is not bounded-degree moment equality. O5: drops become erasures, but list recovery tolerates only a bounded fraction. O6: **not escaped yet**—an affine combination of codewords satisfies every linear marginal row. O7: a genuine list-recovery theorem could provide composition beyond pair bags. O8: code length is polynomial, but realizing the nonlinear list certificate in CVP is open.

**Falsification.** A G13-derived pseudocodeword with small Euclidean cost and perfect code-symbol marginals.

**Smallest experiment.** Encode the 16 assignments by a length-7 RS code over \(\mathbb F_{17}\), build all clause/code-symbol view selectors, and search through anchor excess 32.

**Likely death.** List recovery is a nonlinear conclusion, whereas the emitted lattice retains all affine mixtures.

---

### 4. Expander substitution for affine-support inflation
**Mechanism.** Replace every variable by several parity-coupled copies on a high-girth expander and decode it in multiple clause occurrences. The hoped-for analogue of expander-code pseudoweight is that a non-Boolean affine mixture cannot remain localized: it must contaminate linearly many local selector blocks (compare Sipser–Spielman, 1996).

**Expected move.** Turn the constant-support G13 collision into zero residual but \(\Omega(g)\) replicated anchor excess, then concatenate levels to amplify that excess.

**Obstruction check.** O1: use explicit parity-view selectors, not free parity slack. O2: expander checks deliberately cross overlaps. O3: all copy and check selectors must be unrestricted. O4: growing girth may prevent bounded-support parity relocation. O5: every occurrence has several decodings, so one drop should spread—unproved. O6: **still applies:** the nine-term combination extends through all linear checks; only its accumulated anchor cost can help. O7: expansion offers a possible composition lemma absent from pair bags. O8: no argument yet makes the ratio, rather than both numerator and baseline, grow.

**Falsification.** A zero-residual affine lift whose excess is \(O(1)\), or whose excess/baseline ratio stays bounded under concatenation.

**Smallest experiment.** Substitute each variable in the four-variable obstruction by a 6-cycle parity gadget, emit all local-view selectors, and compare one and two concatenation levels.

**Likely death.** Replication increases completeness cost at the same rate as pseudoweight.

---

### 5. Certified tensor amplification through E-type lattices
**Mechanism.** Homogenize a finite GapCVP instance via a Kannan-style embedding, then tensor it with a specially chosen lattice for which every shortest tensor is decomposable. If an applicable closest-vector multiplicativity theorem held, a base ratio \(\rho>1\) would become \(\rho^k\) after \(k\) tensor levels; E-type phenomena are discussed in Kitaoka, *Arithmetic of Quadratic Forms* (1993).

**Expected move.** Amplify the exact finite G9 or G14 gap without adding new SAT consistency constraints.

**Obstruction check.** O1/O2/O4/O5: not removed; they are already reflected in the exact base minimum. O3: tensor basis and target are explicit and unrestricted. O6: the affine lift remains a base competitor, but true multiplicativity would amplify the actual minimum despite it. O7: a tensor theorem would supply the missing composition law. O8: \(k=\Theta(\log n)\) gives polynomial ratio but currently quasi-polynomial dimension \(N^k\).

**Falsification.** Any entangled tensor vector below the product distance, or a spurious short Kannan-embedding vector.

**Smallest experiment.** Tensor-square an HNF-reduced core of the G9 instance and perform exact bounded enumeration against the squared predicted gap.

**Likely death.** E-type results concern shortest vectors, not arbitrary closest targets; tensor dimension also explodes.

---

### 6. Treewidth–well-linked dichotomy
**Mechanism.** Handle formulas of treewidth \(O(\log n)\) by deterministic dynamic programming and output a trivial yes/no CVP instance. For high treewidth, route clause-consistency gadgets through a large well-linked minor, placing overlapping bags so that a local pseudoselector must recur across many routed regions.

**Expected move.** Obtain a structural dichotomy: easy formulas are solved directly, while hard-incidence formulas provide enough disjoint geometric witnesses for a growing distance.

**Obstruction check.** O1: the construction relies on bag anchors, not residual-only amplification. O2: bags are linked globally through routed intersections. O3: each routed instance must be emitted and searched unrestricted. O4: effective bag width grows with the structural parameter. O5: **not escaped:** high treewidth need not spread a logically isolated clause defect. O6: the affine combination extends with zero residual, but may pay anchor excess in every routed bag. O7: the graph-minor structure is intended as the missing composition theorem. O8: quantitative minor size, bag weights, and dimension-gap accounting remain absent.

**Falsification.** A connected high-treewidth family containing a constant unsatisfiable core whose nearest-vector ratio remains bounded.

**Smallest experiment.** Attach the nine-clause core by equality bridges to satisfiable expander components of sizes 8 and 16; generate routed bags and solve the exact low shell by MILP/DP.

**Likely death.** Incidence treewidth measures irrelevant structure, not how many clauses every assignment violates.
