Classical ingredient pointers only: Sipser–Spielman, “Expander Codes” (1996); Forney, *Concatenated Codes* (1966); Barrington, “Bounded-Width Polynomial-Size Branching Programs” (1989); Naor–Naor, “Small-Bias Probability Spaces” (1993); standard Plücker embeddings and integer chain-complex homology.

1. **Lossless-expander sparse integer representation**

**Mechanism.** Replace half-integral anchors by an explicit coefficient-energy block: YES instances represent the target using \(O(m)\) unit columns, while an expander dictionary should force every NO representation to have squared coefficient norm \(m n^{\Omega(1)}\). Scale emitted residual rows above the proposed NO threshold, reducing soundness to an integer nullspace-property theorem.

**Expected move.** A polynomial support/energy gap without amplifying the honest baseline.

**Obstruction audit.** G1 RS slack: no slack. G2–3 affine isolation: global NSP, not fixed local marginals. G5 overlap: shared expander checks, not private rows. G6 quotient: all checks emitted. G7 radix: no radix; exact kernels still pay coefficient energy. G9/G11 moment parities and G13 affine collision: use enlarged assignment-dependent cosets, not a compatible raw-selector hash. G12 drop: lossless expansion spreads it. G14 pair bags/G15 laminar lift: no bags or tree. G19 signed flow: no flow. G28 min-plus: no identity seam. G30 tensor isometry: no tensoring.

**Falsification/experiment.** On the nine-clause instance, enumerate small 3-regular dictionaries and exactly compare minimum-energy exact representations against the control.

**Likely death.** A constant-energy integer circuit, probably a lifted G13 affine combination.

2. **Witt-vector carry tower without free slack**

**Mechanism.** Encode each local truth label by its first \(L=\Theta(\log n)\) base-\(p\) ghost components. Carries are explicit anchored variables connected across an expander; a signed selector should either be an honest digit at every level or generate a first nonzero carry replicated across \(n^{\Omega(1)}\) coordinates.

**Expected move.** Turn bounded signed coefficients into polynomial Euclidean cost while retaining polynomial dimension.

**Obstruction audit.** G1 RS slack: carries are charged and cross-level constrained, so its free-slack premise is absent. G2–3 affine isolation/G5 overlap: global digit routing replaces local fixed-fiber isolation. G6 quotient: emit every carry equation. G7 radix: carries, not linear ordering, are essential. G9/G11 moments: arithmetic digits replace bounded-degree moments. G12 clause drop: missing normalization creates carries at every level. G13 affine collision and G15 laminar lift are **not automatically escaped**: an affine combination may lift through all ghost levels. G14 pair-bag pass is orthogonal. G19 flow, G28 min-plus, and G30 tensor assumptions are absent.

**Falsification/experiment.** Use \(p=2,L=3\) on the four-variable obstruction; enumerate coefficients and carries in \([-2,2]\), including the exact G13 combination.

**Likely death.** Witt ghost maps are polynomial identities, so the affine pseudodistribution may thread the entire tower with only constant negative mass.

3. **Plücker-rank rigidity**

**Mechanism.** Map assignment fragments to decomposable exterior tensors and glue bags through contractions rather than ordinary marginals. Honest assignments remain rank-one/decomposable; a signed pseudodistribution must either violate a Plücker coordinate or express a nondecomposable tensor using many integral rank-one terms, increasing coefficient energy.

**Expected move.** Prove a tensor/secant-rank lower bound \(n^{\Omega(1)}\) for every NO witness.

**Obstruction audit.** G1 slack and G7 radix are irrelevant. G2–3 isolation and G5 overlap concern affine marginals, not contraction/flattening rank. G6 is avoided by emitting all coordinates. G9/G11 use only degree-\(\le3\) scalar moments; this uses full flattening rank. G12’s single Walsh tag is replaced by redundant contractions. G13 raw compatible hashes do not cover nonlinear enlarged columns, although an analogous affine lift remains possible. G14 fixed pair bags and G15 one laminar tree lack Plücker rank tests. G19 has no tensor-rank invariant. G28 tests one min-plus seam. G30 tests a literal tensor of an isometric seed, not decomposability constraints.

**Falsification/experiment.** Lift the nine-clause pair bags to \(2\times2\) sign matrices, emit all contractions, and exactly search through anchor excess 32 for rank-two signed cheats.

**Likely death.** The G13 combination may have constant secant rank independent of formula size.

4. **Homological systole amplifier**

**Mechanism.** Build an integral mapping-cone chain complex whose target coset has a short filling when an assignment satisfies every clause, but represents a nontrivial syndrome class otherwise. Take an explicit high-dimensional expander product so every nontrivial class has polynomially large Euclidean systole; the CVP lattice is the emitted integer boundary lattice.

**Expected move.** YES filling norm \(O(\sqrt n)\), NO coset norm \(n^{1/2+c}\).

**Obstruction audit.** G1 slack, G7 radix, G9/G11 moments, G12 fingerprints, and G13 compatible hashes are different algebraic objects. G2–3/G5 local isolation is replaced by a global chain complex. G6’s defect is addressed only if boundary, target, and torsion rows are all emitted—SNF alone is not evidence. G14/G15 use marginal bags rather than homological expansion. G19’s signed-flow splice becomes a signed cycle and is **not automatically excluded**; the systole theorem must cover it. G28’s frozen seam and G30’s seed tensor assumptions are absent.

**Falsification/experiment.** Search small integral complexes \(B_1B_2=0\) extending the nine-clause syndrome; compute SNF and exact shortest representatives of every relevant coset before and after one expander-product step.

**Likely death.** Arbitrary SAT mapping cones may contain short local cycles, and repairing them may amount to forbidden gap amplification.

5. **Global chirp fingerprints with Fourier uncertainty**

**Mechanism.** Give each clause label a block of root-of-unity chirps indexed by an explicit small-bias hash family. Consistent global assignments trace equal-radius phase codewords, whereas signed mixtures or clause deletion should have broad Fourier support by an uncertainty bound, producing energy in many coordinates.

**Expected move.** Obtain polynomial tag distance while keeping every honest assignment on one completeness sphere.

**Obstruction audit.** G1 has no arithmetic slack here. G2–3/G5 concern affine fibers, not phase coherence. G6 is avoided by emitting real and imaginary cyclotomic coordinates. G7’s exact residual kernel need not be a phase kernel. G9/G11 test low-degree moments only. G12 used one top-Walsh coordinate per clause; this uses many global chirps plus an outer deletion code. G13 assumes all honest encodings share one linear syndrome; here they occupy distinct spherical codewords, though affine mixtures may still be near the center. G14/G15 marginal lifts, G19 flows, G28 seams, and G30 literal tensors are absent.

**Falsification/experiment.** Search \(16\)- or \(32\)-dimensional \(\{\pm1\}\) chirp families for the nine-clause instance by MILP, then perform the exact unrestricted shell search through the proposed \(4/3\) threshold.

**Likely death.** Parseval may increase honest and dishonest energies proportionally, yielding only a constant ratio; a balanced affine mixture may cancel every chirp.

6. **Outer-code concatenation of nonisometric deep holes**

**Mechanism.** First find a constant-rank inner lattice with a complete coset table: legal cosets have radius \(r\), every malformed coset radius at least \(R>r\), and NO/YES targets are provably nonisometric. Couple many copies using a positive-distance outer linear code, so one logical inconsistency forces many bad inner cosets; iterate a constant number of code levels.

**Expected move.** Outer relative distance converts \(R/r>1\) into a polynomial NO/YES ratio while preserving polynomial rank.

**Obstruction audit.** G1 slack, G7 radix, G9/G11 moments, G12 tags, G13 raw hashes, and G19 flows are not used. G2–3 local isolation could supply a seed but is not assumed to compose; G5 specifically kills private marginal composition. G6 requires all coset checks emitted. G14/G15 are different bag/tree lifts. G28 is directly relevant but only killed one identity-seam min-plus rule; this uses nontrivial outer-code syndromes and complete coset states. G30 is directly addressed by requiring checked nonisometry and \(R_1>1\), rather than reusing its isometric tensor seed.

**Falsification/experiment.** Enumerate rank-\(\le8\) binary inner factors, reject isometries canonically, compute exact coset minima, then concatenate the first survivor with a three-symbol parity code and exhaust depth two.

**Likely death.** Bad-coset costs may add rather than multiply, leaving only constant approximation.

7. **Noncommutative product-tree selectors**

**Mechanism.** Replace branching-program flow by selectors for multiplication triples \((g,h,gh)\) in a fixed finite nonabelian group, arranged in a balanced product tree. Emit all irreducible matrix coefficients of each gate and repeat gates through an expander; signed path splicing must now extend to a globally consistent signed multiplication table.

**Expected move.** Force negative mass to branch at each tree level, giving polynomial coefficient energy at logarithmic depth.

**Obstruction audit.** G1 slack and G7 radix are absent. G2–3/G5 affine marginal arguments do not encode noncommutative products. G6 is avoided only with every gate selector and root condition emitted. G9/G11 commutative moments do not see ordered products. G12 clause tags and G14 pair bags lack multiplication closure. G13 affine collision and G15 affine hierarchy are **not escaped automatically**: affine combinations of complete product trees may remain exact. G19 is the closest obstruction, but it used edge-flow conservation; multiplication-gate joint selectors remove its specific two-negative splice. G28’s identity seam and G30’s literal tensor isometry are absent.

**Falsification/experiment.** Compile a small rejecting width-5 word over \(A_5\), build two product-tree levels, and use exact MILP to search coefficients in \([-2,2]\) for a zero-residual accepting root.

**Likely death.** Signed quasidistributions may be closed under convolution, recreating G19 with constant negative mass.
