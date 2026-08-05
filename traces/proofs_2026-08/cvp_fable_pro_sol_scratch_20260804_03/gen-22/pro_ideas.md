All proposals below are speculative and require unrestricted obstruction/control searches before promotion.

### 1. Higher-Lawrence/Graver amplification

**Core trick.** Replace each selector system by an \(r\)-th higher Lawrence lifting, linking many signed copies so every harmful zero-residual deformation must contain a large Graver move rather than a constant-support circuit (Sturmfels, *Gröbner Bases and Convex Polytopes*, 1996). Seek an explicit family where harmful Graver norm grows superlinearly relative to the honest baseline.

**Expected move.** With \(r=n^\alpha\), prove harmful squared excess \(\Omega(r^{1+2c})\) while completeness is \(O(r)\).

**Obstruction audit.** G1 slack and G7 radix: absent. G2–3 isolation: usable only as a seed. G5 overlap: directly targeted, not escaped yet. G6 filtering: emit the complete lattice. G9/G11 parity, G13 affine closure, and G15 threading remain exact kernel vectors; the claim is only that lifting makes them long. G12 drops must replicate across layers. G14 supplies a possible seed but no theorem. G19 flow splicing is outside the construction. G20/G21 baseline, polynomial size, and unrestricted coefficients are explicit requirements.

**Experiment/falsifier.** Build \(r=2,3,4\) liftings of the 72-selector obstruction matrix; MILP-minimize exact harmful-fiber norm and compare controls. Kill if normalized excess stays bounded.

**Likely death.** The G13 affine combination simply repeats with constant excess per layer, giving only a constant ratio.

---

### 2. Discriminant-form lattice gluing

**Core trick.** Encode truth values as classes in the discriminant group \(L^\*/L\) of an even lattice, not as one-hot selector mixtures. Glue variable and clause lattices through isotropic subgroups so seven clause classes have short representatives while the forbidden class has a much larger theta minimum (Conway–Sloane, *Sphere Packings, Lattices and Groups*, 1999).

**Expected move.** Find a polynomial family whose forbidden-coset minimum is \(N^{2c}\) times the common legal-coset radius.

**Obstruction audit.** G1 slack, G7 radix, G9/G11 moments, G14 bags, G15 hierarchy, and G19 flows are absent. G2–3 local isolation is not assumed; G5 marginal-overlap circuits do not directly apply to discriminant gluing. G6 is avoided by emitting bases and targets. G12 dropping remains live. G13’s raw-selector affine-span theorem is outside its stated encoding, but analogous short lattice combinations may exist. G20/G21 baseline and gluing-specification objections apply fully.

**Experiment/falsifier.** Enumerate index-\(\le16\) overlattices of \(D_4^4\); encode one three-variable OR, compute legal/forbidden coset minima through norm \(12\), then assemble all eight clauses and solve exact CVP.

**Likely death.** Theta minima of different cosets differ only constantly, or gluing introduces a short mixed-coset representative recreating G5/G13.

---

### 3. Frozen Heisenberg-holonomy flow

**Core trick.** Reopen the only G21-authorized flow mutation in a fully concrete form: use the regular integral representation of the order-27 Heisenberg group \(H_3(\mathbb F_3)\) as a fiber over each branching-program state. Each edge transports the fiber by a fixed group element, so a splice must preserve both ordinary flow and noncommutative holonomy.

**Expected move.** Honest accepting paths have one prescribed fiber boundary, while every signed accepting splice acquires noncentral holonomy or requires many negative coefficients.

**Obstruction audit.** G1 slack, G7 radix, G9/G11 moments, G12 tags, G14 bags, and G15 hierarchy are absent. G2–3 isolation and G5 overlap are not used. G6 is addressed by emitting every transport row. G13 affine closure remains a serious threat because transport is linear. G19 signed flow applies directly rather than lying outside the assumptions. G21’s prior underspecification is repaired by fixing \(H_3\), its regular representation, boundaries, and weights; G20 baseline still applies.

**Experiment/falsifier.** Compile the eight-clause three-variable formula to a small reversible program; emit \(27\)-fiber transport rows and exactly search obstruction/control shells through baseline \(+16\). Kill on completeness-boundary mismatch or any zero-residual signed acceptor.

**Likely death.** A G19 splice lifts independently in each regular-representation coordinate.

---

### 4. Cosystolic assignment sheaf

**Core trick.** Place local assignments on a two-dimensional expander and regard consistency defects as integral sheaf coboundaries. Penalize both coboundary energy and coordinates representing nontrivial cohomology, hoping cosystolic expansion forces any nonglobal pseudosection to occupy a linear fraction of cells (cf. Kaufman–Kazhdan–Lubotzky, 2014).

**Expected move.** Embed formula inconsistency as a nontrivial class whose harmonic penalty can be weighted by \(N^{2c}\), while honest global sections have zero harmonic component.

**Obstruction audit.** G1 slack and G7 radix are absent. G2–3 local isolation is not assumed; G5 becomes a sheaf-overlap question. G6 requires all cochain and harmonic rows be emitted. G9/G11 parity may become cocycles and is live. G12 drops should create large coboundary support. G13 affine closure and G15 threading apply because sheaf equations remain linear; they are the principal tests. G14 pair bags resemble only the local stars, not the global cohomology. G19 signed chains are analogous to signed flows. G20/G21 polynomial-size and baseline objections remain.

**Experiment/falsifier.** Put the fixed obstruction on the Fano incidence complex or a 13-vertex projective-plane complex; compute integral \(H^1\), then MILP-search all signed cochains through baseline \(+32\).

**Likely death.** The G13 affine pseudosection is an exact global section, so expansion sees no defect at all.

---

### 5. Automated quadratic gap-transformer gadget

**Core trick.** Search directly for a constant-size integer least-squares gadget with ports whose legal port states retain baseline \(B\), but whose illegal excess \(E\) is transformed to at least \(C E\), with \(C\) exceeding the gadget’s size blow-up. Recursive substitution would then amplify a finite gap polynomially without invoking a PCP theorem.

**Expected move.** A depth-\(\Theta(\log n)\) composition yields ratio \(n^c\) while dimension remains polynomial.

**Obstruction audit.** G1 slack is excluded by allowing no free auxiliaries. G2–3 isolation can seed port states; G5 overlap is included in the port table. G6 demands an emitted objective and eigenvalue-certified search bound. G7 kernels, G9/G11 parity, G12 drops, G13 affine mixtures, G15 threading, and G19 splices must all appear as illegal port states, not be assumed away. G14 provides a finite seed only. G20/G21 baseline accounting is exactly the transformer inequality; polynomial size is explicit.

**Experiment/falsifier.** Enumerate matrices with two ports, at most six internal variables, eight rows, entries in \(\{-2,\ldots,2\}\), and half-integral targets. Verify every integer state using bounded enumeration plus a smallest-eigenvalue tail certificate.

**Likely death.** Convex quadratic energy composes additively: any multiplier \(C\) also multiplies honest baseline or gadget size, preventing \(C\) from beating blow-up.

---

### 6. Discrete-convex matroid rigidity

**Core trick.** Represent each legal trace as a matroid basis. Integer normalization plus squared norm already makes \(0/1\) bases the minimum-energy points; couple clause and variable choices through graphic or transversal matroid sums so cheating requires a long exchange circuit (Edmonds, 1970; Murota, *Discrete Convex Analysis*, 2003).

**Expected move.** Construct formula-dependent matroids where every inconsistent integral point differs from the basis shell along an exchange circuit of norm \(n^{1/2+c}\).

**Obstruction audit.** G1 slack and G7 radix are absent. G2–3 local isolation is replaced by basis rigidity. G5 overlap becomes short circuit elimination and is directly relevant. G6 requires using only emitted affine equations and the quadratic norm—no hidden base-polytope inequalities. G9/G11 parity and G13 affine mixtures may be short signed circuits. G12 drops violate rank equations but may remain cheap. G14/G15 are not assumed. G19 has no flow, although graphic circuits can reproduce it. G20/G21 baseline and polynomial representation are unresolved.

**Experiment/falsifier.** Search small totally unimodular representations coupling the all-eight-clauses instance; enumerate all integral points through baseline \(+32\) and extract shortest nonbasis circuits.

**Likely death.** Regular-matroid structure is too tractable to encode SAT; leaving regularity immediately restores short signed circuits and G13-like mixtures.

---

### 7. Algebraic tensor product of finite-gap cosets

**Core trick.** Homogenize a finite CVP instance as an affine lattice coset and take a controlled Kronecker power, so decomposable honest witnesses have distance \(R^k\) while soundness would be \(S^k\). Use only \(k=O(\log n)\) over a fixed local alphabet, represented by an expander-indexed tensor network, to keep the emitted dimension polynomial.

**Expected move.** Turn the finite G9 or G14 ratio \(S/R>1\) into \(n^c\), provided every “entangled” integral tensor is no shorter than a decomposable one.

**Obstruction audit.** G1 slack and G7 radix are absent. G2–3/G5 local overlap are delegated to the base instance, not solved. G6 requires fully expanding the tensor-network lattice. G9 and G14 provide only candidate seeds. G11 parity, G12 drops, G13 affine combinations, and G15 threading can become entangled tensors and remain live. G19 splicing has a tensor-network analogue. G20/G21 polynomial-size and baseline objections are central; any uncompressed \(N^k\) construction fails them.

**Experiment/falsifier.** Tensor-square the 72-coordinate G9 affine coset, emit its 5,184-coordinate integer least-squares form, and MILP-search below the squared predicted product threshold.

**Likely death.** An entangled sum of simple tensors beats multiplicativity, while any restriction to low tensor rank is nonlinear and not a lattice.
