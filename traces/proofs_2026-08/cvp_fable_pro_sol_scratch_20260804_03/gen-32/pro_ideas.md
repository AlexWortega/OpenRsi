### 1. Cross-copy moment coupling of the Generation-31 survivor

**Mechanism.** Couple two Walsh-Gram instances through global degree-\(\le3\) moment rows spanning both copies, rather than taking a direct sum. The cross-copy rows might make the one-copy parity witnesses incompatible, producing finite superadditivity.

**Expected move.** Determine the exact one-copy value \(d_1^2\), retain control minimum \(288\), and prove \(d_2^2>2d_1^2\).

**Obstruction audit.** G1/G7: no slack or radix, although zero-residual kernels remain possible. G2–3/G5: uses global rows, not private local isolation. G6: every condition is emitted. G9/G11/G13: parity and affine collision are the principal searched attacks, not excluded assumptions. G12: enumerate drops. G14/G15: neither fixed pair bags nor a marginal-only hierarchy. G19: no flow. G28: no frozen min-plus rule. G30: no tensor product or seed isometry. G31: directly tests its missing composition claim; it does not escape the isotropic-penalty criticism.

**Falsification/experiment.** Share variables \(0,1\), rename \(2,3\mapsto4,5\), exhaust one copy through \(216\), then every residual branch through \(2d_1^2\) on rank \(144\).

**Likely death.** Two compatible parity witnesses remain zero-residual and exactly additive.

---

### 2. Zero-centered sparse expander cover

**Mechanism.** Abandon half-integral cost on every available selector. Represent an honest choice by a sparse routed codeword in a deterministic lossless-expander cover, with zero-centered coefficient cost; use full pair-bag ports so an inconsistent integral state must either violate a weighted check or branch into polynomially many nonzero coefficients. This seeks a direct support theorem, akin to expander-code distance, without invoking PCP machinery.

**Expected move.** Honest support \(O(m)\), but every zero-residual NO vector has support \(\Omega(m^{1+\epsilon})\), giving distance ratio \(m^{\epsilon/2}\); scale nonzero residuals polynomially.

**Obstruction audit.** G1/G7: no slack/radix; exact kernels remain the central risk. G2–3/G5: global expansion replaces fragile private rows. G6: emit all routing checks. G9/G11/G13: raw parity need not lift linearly through routed histories, but this must be tested. G12: a drop exposes many unique neighbors. G14 supplies possible seed ports; G15’s laminar affine lift is outside the nonlaminar cover, unless it extends globally. G19 signed branching may recur. G28/G30: no fixed recursion or Kronecker tensor. G31: nonisotropic cross-block geometry and sparse completeness.

**Falsification/experiment.** Lift two G14 bags through the smallest \(3\)-left-regular cover; enumerate exact zero-residual support.

**Likely death.** Signed deviations circulate on a short even cycle instead of expanding.

---

### 3. Homological-coset amplifier

**Mechanism.** Place variable, clause, and overlap labels on flags of an explicit finite \(2\)-complex. Consistency becomes a boundary equation; engineer the formula defect to occupy a nontrivial homology or torsion coset, then add a heavily weighted integral cocycle detecting that coset. A nonlinear flag lift is essential: merely placing raw selectors in a chain complex would preserve the G13 affine collision.

**Expected move.** YES witnesses are short boundaries, while every NO representative either has nonzero cocycle syndrome or contains a cycle of polynomial systole.

**Obstruction audit.** G1/G7: no slack or radix. G2–3/G5: obstruction is global topology, not fixed marginals/private rows. G6: boundary and cocycle coordinates are emitted. G9/G11/G13: not escaped if the flag lift remains affine; explicitly test that. G12: dropping a face creates boundary. G14 can supply flags; G15’s affine hierarchy lift is outside only if nonlinear incidence breaks it. G19: no layered flow, though signed cycles are analogous. G28/G30: neither min-plus nor tensor. G31: cocycle rows are cross-block, not isotropic Walsh energy.

**Falsification/experiment.** Put the nine-clause instance on a triangulated projective-plane or torus toy complex and compute SNF plus the minimum integral representative in each defect coset.

**Likely death.** The defect is a boundary, or torsion admits a constant-support representative.

---

### 4. Nonabelian group-ring histories

**Mechanism.** Replace ordinary accepting flow by selectors for complete adjacent transition histories in a small nonabelian group. Enforce shared-variable choices through pair marginals, and fingerprint accumulated products using several irreducible matrix representations; signed edge conservation alone no longer guarantees the correct ordered product.

**Expected move.** Prove that every exact ACCEPT vector either corresponds to a genuine assignment or contains many non-Boolean history coefficients, which can then be charged geometrically.

**Obstruction audit.** G1/G7: no slack/radix. G2–3/G5: full histories couple overlaps globally. G6: all product-table selectors and marginals are lattice rows. G9/G11/G13: raw affine identities need not survive the enlarged product-history map, but affine combinations of complete histories remain dangerous. G12: a missing layer violates normalization. G14 resembles pair bags but now carries ordered products. G15 can still thread any affine mixture of complete histories. G19 is directly targeted, yet signed history splicing is not ruled out. G28/G30: no fixed tile or tensor. G31: representation Gram has genuine cross-state terms, unlike \(H_8^TH_8=8I\).

**Falsification/experiment.** Compile a four-to-eight-layer unsatisfiable toy program over \(S_3\) or \(A_5\); enumerate the exact ACCEPT fiber by dynamic programming.

**Likely death.** A two-negative signed combination of complete histories still matches every representation marginal.

---

### 5. Canonical CRT assignment with protected carries

**Mechanism.** Encode the entire Boolean assignment as one bounded integer \(X\). Extract its bits simultaneously through canonical remainder automata modulo several coprime moduli; each clause reads three certified digits, with no clause-local slack. Protect carry histories using full transition-pair bags and redundant code checks so that a NO instance must leave a nonzero integral residue, which may then be scaled polynomially.

**Expected move.** Establish an exact-fiber lemma: every zero-residual integral vector is the canonical encoding of one Boolean assignment. Polynomial residual weight would then immediately create a polynomial gap.

**Obstruction audit.** G1 returns if carries have free integer directions; this is the first test. G7: no radix ordering of an already-cheatable residual. G2–3/G5: canonical global \(X\), not private marginals. G6: bounds and carry equations must be emitted, never filtered. G9/G11/G13: raw selector parity does not automatically lift to one canonical \(X\), although an affine carry lift may exist. G12: drops violate automaton normalization. G14/G15: transition bags are nonlaminar but may still admit affine lifts. G19 signed automaton splicing is a direct threat. G28/G30/G31: no tile, tensor, or isotropic Gram dependence.

**Falsification/experiment.** Encode all eight clauses on three bits with moduli \(3,5\); compute SNF and minimum signed zero-residual carry vector.

**Likely death.** A short signed carry circulation represents no integer \(X\) but satisfies every linear row.

---

### 6. Nonorthogonal spherical-code substitution

**Mechanism.** Recursively substitute every legal port symbol by a short integer spherical codeword whose Gram matrix is deliberately nonorthogonal. Seek a seed where an honest symbol has energy \(\mu\), while every unrestricted integral representation of an illegal symbol costs \(\lambda>\mu\); concatenation would amplify \((\lambda/\mu)^{\Theta(\log n)}\). This is code substitution with recentering, not literal Kronecker multiplication.

**Expected move.** Obtain a complete finite transfer inequality stable under substitution, then prove it inductively over all integral port states.

**Obstruction audit.** G1/G7: no slack/radix. G2–3/G5: port legality is global in the code alphabet. G6: transfer states are derived from emitted coordinates. G9/G11/G13: nonorthogonal Gram can charge affine mixtures, but cannot exclude them automatically. G12: DROP is a required port class. G14 may provide the seed alphabet; G15 affine lifts must be included. G19 signed states are explicit classes. G28 is escaped only by changing substitution and proving closure, not merely retuning its tile. G30: no seed tensor, and isomorphic seeds are rejected. G31: avoids orthogonal Walsh collapse and directly seeks multiplicative growth.

**Falsification/experiment.** Enumerate \(3\)- or \(4\)-symbol integer Gram matrices and complete depth-one/depth-two transfer tables through a certified shell.

**Likely death.** Convexity or an affine interpolation forces \(\lambda\le\mu\).

---

### 7. Perfect-hash separator bags with Möbius fingerprints

**Mechanism.** Use a deterministic splitter family of \(O(\log n)\)-variable bags, each represented by its full truth table. Every clause lies in several bags, while any small-support signed mixture is isolated by some perfect hash; attach nonorthogonal Möbius-character fingerprints on separated coordinates. A dichotomy is sought: small-support cheats are detected, and large-support cheats already have large zero-centered norm.

**Expected move.** For polynomially many polynomial-size bags, prove either a weighted residual or coefficient norm \(n^\epsilon\) times the honest radius.

**Obstruction audit.** G1/G7: no slack/radix. G2–3/G5: overlapping separator bags replace private local rows. G6: all bag conditions are emitted. G9/G11: unique-triple parity is repeated across many separating bags. G13: the affine mixture remains marginal-consistent, so only fingerprint energy—not syndrome—can charge it. G12: bag coverage replicates drops. G14 is generalized from pairs to logarithmic bags. G15 is not laminar, but any global affine pseudodistribution can still thread all marginals. G19: no flow. G28/G30: no fixed tile or tensor. G31: fingerprints are nonorthogonal and cross-bag, avoiding the \(8I\) collapse.

**Falsification/experiment.** On the four-variable obstruction, emit the full \(16\)-assignment bag and all clause-forbidden rows; exactly minimize zero-centered norm, then add all subset Möbius tags.

**Likely death.** The G13 affine lift survives every bag and gains only a constant energy factor.

Classical touchstones: Sipser–Spielman, “Expander Codes” (1996); Forney, *Concatenated Codes* (1966); Serre, *Linear Representations of Finite Groups* (1977); Fredman–Komlós–Szemerédi on perfect hashing (1984).
