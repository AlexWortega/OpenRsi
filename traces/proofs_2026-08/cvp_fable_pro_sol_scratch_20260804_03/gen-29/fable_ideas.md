## Generation 29 — divergent mechanism sketches

### 1. Veronese lift with tensor-rank penalties
**Core trick.** Replace each selector vector \(s\) by selected degree-\(k\) coordinates \(s_I=\prod_{i\in I}s_i\), implemented using explicit assignment-table variables. Honest assignments lie on a rank-one Veronese variety; parity mixtures and clause drops should become dense non-rank-one objects whose anchor cost grows under tensoring.

**Expected move.** At \(k=2\), raise the lifted G13/G15 affine attack’s excess from \(24\) to at least \(48\), with unchanged honest baseline per copy.

**Obstruction check.** G1 slack/G7 radix: no slack or residual-only amplification, although lifted zero kernels remain possible. G2–3 isolation/G5 overlap: uses global products, not private fixed-marginal rows. G6: every lift variable and equation is emitted. G9/G11 moments and G12 fingerprints: products are coordinates, not merely compared moments/tags. G13 raw-code collision is outside the raw coordinates, but an affine combination of *complete lifted* honest encodings remains a serious analogue. G14/G15: neither fixed pair bags nor a marginal tree. G19: no flow conservation. G28: no min-plus tile recursion.

**Experiment.** Degree-two lift of the 16 honest encodings and nine-clause obstruction; ILP-minimize anchor cost in the exact lifted fiber.

**Most likely death.** The same 16 affine coefficients lift exactly with only constant extra cost.

---

### 2. Boolean-quotient multiplication lattice
**Core trick.** In \(R=\mathbb Z[x_1,\ldots,x_n]/(x_i^2-x_i)\), let \(V_F\) be the number of violated clauses and study the integer multiplication operator \(M_{V_F}\). Satisfiability gives a Boolean evaluation where \(V_F=0\); unsatisfiability makes \(M_{V_F}\) pointwise nonzero, potentially creating determinant, divisibility, or singular-value separation in a graph lattice built from \(M_{V_F},M_{V_F}^2,\ldots\).

**Expected move.** Convert nonvanishing of \(V_F\) into a target-coset distance that grows multiplicatively under powers, without selector slack.

**Obstruction check.** G1/G7 zero-slack attacks are avoided because \(V_F\) is computed in the Boolean quotient. G2–3/G5 concern selector isolation and overlap, absent here. G6 requires the complete multiplication lattice and target to be emitted. G9/G11/G12 are metric/moment/tag constructions, unlike operator noninvertibility. G13 does not directly cover \(M_{V_F}\), but any linearized evaluation-table realization may reproduce its affine collision. G14/G15 bag lifts are replaced by quotient multiplication. G19 has no flow. G28 has no tile recurrence.

**Experiment.** Build the exact \(16\times16\) multiplication matrices for the nine-clause four-variable obstruction and control; enumerate shortest vectors in candidate graph-lattice cosets.

**Most likely death.** The quotient has dimension \(2^n\), and compressed multiplication may have exponentially tiny singular values.

---

### 3. Cosystolic obstruction complex
**Core trick.** Turn variable consistency and clause legality into boundaries of a two- or three-dimensional integer cell complex. A satisfying assignment supplies a small filling, whereas an unsatisfiable target should represent a nontrivial cohomology class; a cosystolic-expansion bound would force every representative to have large Euclidean support.

**Expected move.** Obtain filling cost \(O(m)\) for completeness but systole \(\Omega(m^{1+\delta})\) for soundness.

**Obstruction check.** G1 slack and G7 radix are absent, but an exact boundary can still be a zero-residual cheat. G2–3/G5 use local affine rows; here the invariant is global homology. G6 is satisfied only if all chain groups and boundary maps are included. G9/G11/G12 do not analyze homology. G13 remains relevant: affine mixtures are cycles, so the mechanism succeeds only if they lie in the wrong class or have large systolic support. G14/G15 use bags/trees rather than a complex with expansion. G19 is one-dimensional signed flow; higher-dimensional filling is the intended escape. G28’s identity-seam min-plus failure says nothing about cosystolic expansion.

**Experiment.** Build a simplicial complex for the eight clauses on three variables; use Smith normal form plus MILP to compute each target class’s integral \(1\)- and \(2\)-systoles.

**Most likely death.** The needed complex expansion is equivalent to hidden gap amplification, effectively recreating PCP machinery.

---

### 4. Noncommutative checkpoint algebra
**Core trick.** Compile clause evaluation into products of small noncommuting matrices or group-algebra elements, with checkpoints represented by multiplication-table selectors and redundant traces of short words. Unlike scalar flow conservation, a signed splice must preserve ordered products and should violate many checkpoint identities.

**Expected move.** Make the exact ACCEPT fiber empty, then prove every malformed product transcript incurs cost proportional to its length.

**Obstruction check.** G1/G7 are bypassed because there is no freely adjustable scalar residual. G2–3/G5 local measurement composition is replaced by ordered multiplication. G6 demands that multiplication-table selectors—not external rank-one filters—be emitted. G9/G11/G12 only see commutative moments or tags. G13’s raw-selector affine collision is outside the enlarged noncommutative state space, although affine combinations of complete transcripts remain dangerous. G14/G15 marginal lifts do not enforce order. G19 is the direct warning: scalar Barrington flow admitted signed splicing; this mechanism survives only if product checkpoints prevent that splice. G28 concerns min-plus seam growth, not word identities.

**Experiment.** Encode the four-variable obstruction as a 16-leaf decision program over \(S_3\); exhaust coefficients in \([-2,2]\) for an exact accepting transcript.

**Most likely death.** Linearizing multiplication tables introduces a new two-negative signed splice analogous to G19.

---

### 5. Adversarially learned Gram metric plus spectral product
**Core trick.** Alternate exact shortest-vector search with a rational SDP that chooses a positive-definite Gram matrix: all honest encodings must have equal radius, while every discovered drop, parity, flow, or malformed-bag vector receives larger energy. If a finite seed ratio \(\rho>1\) is certified, attempt a Kronecker or zig-zag-style spectral product rather than min-plus composition.

**Expected move.** Find a seed with \(\rho>1\) whose product has adverse/legal energy ratio at least \(\rho^2\).

**Obstruction check.** G1/G7 zero kernels are explicitly supplied to the separation oracle. G2–3/G5 are not assumed to compose locally. G6 is met by emitting a rational factorization of \(Q\). G9 is the seed precedent; G11 parity and G12 drop are mandatory adversaries rather than afterthoughts. G13 does not force zero quadratic energy, as G9 already demonstrated, but may defeat equal-radius constraints. G14’s pair-bag pass can be another seed. G15’s fixed hierarchy is not used. G19 transcripts enter the attack set. G28 killed one min-plus rule; spectral tensorization is outside that rule and must still prove closure.

**Experiment.** Cutting-plane SDP on the 72-selector instance, followed by exact two-copy shell enumeration.

**Most likely death.** Equal honest radius forces an undetected affine direction, or legal energy tensorizes as fast as adverse energy.

---

### 6. Redundant \(p\)-adic gate circuit with carry expansion
**Core trick.** Evaluate clause violations through a Boolean arithmetic circuit represented simultaneously in several coprime residue systems. Every multiplication/OR gate uses a full truth-table selector; carries are redundantly encoded on an expander so a nonzero violation or malformed gate should affect many Euclidean coordinates.

**Expected move.** A false formula creates \(\Omega(L)\) charged residue coordinates, while any signed attempt to cancel them violates \(\Omega(L)\) gate/carry checks.

**Obstruction check.** G1’s free integer slack is expressly forbidden. G7’s exact zero-residual selector is still a live threat: it may reappear inside gate tables, so exact-kernel search is mandatory. G2–3/G5 private affine isolation is replaced by a shared circuit. G6 requires all carries and consistency rows inside CVP. G9/G11/G12 are unrelated moment/tag metrics. G13’s theorem covers raw selectors, not nonlinear gate extensions, but affine combinations of complete circuit evaluations may still lift. G14/G15 do not use arithmetic carries. G19 warns that signed local transitions splice; gate products must stop this. G28’s failed tile ratio does not cover residue expansion.

**Experiment.** Encode the unsatisfiable eight-clause three-variable formula over moduli \(3,5\), with one redundant carry layer; enumerate the exact zero-residual fiber and shell.

**Most likely death.** A signed truth-table pseudodistribution satisfies every gate and residue equation exactly.

---

### 7. Sidon-labelled oriented-matroid composition
**Core trick.** Assign each local label a low-dimensional \(B_h\)/Sidon vector so no short signed sum of labels collides, then glue occurrence gadgets through an expander-like oriented matroid. The desired invariant is a growing Graver norm: every non-honest integer circuit preserving all ports must involve \(\Omega(m^\delta)\) selectors.

**Expected move.** Eliminate all bounded-support G5/G7/G11/G19 circuits and obtain a polynomial lower bound on malformed support.

**Obstruction check.** G1 has no slack. G2–3’s finite isolation is the local seed, while G5 says private rows alone cannot compose; shared Sidon tokens must change that. G6 requires direct lattice-shell testing, not filtered circuit search. G7 zero kernels are precisely forbidden short circuits. G9/G11/G12 metric, parity, and drop attacks become explicit forbidden circuits. G13 is not automatically escaped: any linear map constant on all raw honest encodings kills the affine collision, so nonlinear auxiliary labels must make every extension expensive. G14’s dense bags and G15’s hierarchy are replaced by sparse matroid composition. G19’s two-negative splice is another forbidden circuit. G28’s particular transfer rule is unused.

**Experiment.** SAT/MILP-search integer Sidon labels for two overlapping clauses, then the nine-clause incidence graph, maximizing the minimum Graver support through \(\ell_1\le 12\).

**Most likely death.** Preserving all honest assignments forces a short affine circuit regardless of the Sidon labels.

**Classical touchstones:** Veronese embeddings (Hartshorne, *Algebraic Geometry*, 1977); Boolean quotient ideals (Cox–Little–O’Shea, *Ideals, Varieties, and Algorithms*, 1992); high-dimensional expansion (Gromov, 1983); noncommutative computation (Nisan, 1991); zig-zag products (Reingold–Vadhan–Wigderson, 2002); \(B_h\) sets (Bose–Chowla, 1962).
