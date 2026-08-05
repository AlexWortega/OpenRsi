I use this consolidated obstruction key in every audit:

- **Z** zero-residual slack/radix kernels (G1/G7)  
- **O** local isolation lost under overlap (G5)  
- **X** external filters, changed references, mod-2/carry bypasses (G6)  
- **A** honest-affine-span collision and hierarchy lift (G13/G15)  
- **P** bounded-degree parity and additive copies (G9/G11/G32)  
- **D** clause/bag DROP (G12)  
- **S** signed accepting-flow splice (G19)  
- **G** finite pass without adverse-over-legal growth (G14/G28/G31)  
- **T** unrestricted tensor entanglement/isometry (G30)  
- **C** failure of exact common-radius positive geometry (G33/G34)

## 1. Expander-contaminated bent path fingerprints

**Core trick.** Augment a branching-program flow with a polynomial-size hash-state cover: each transition accumulates quadratic bent-function characters of the assignment prefix, and expander routing repeats any state mismatch across many hash coordinates. Distinct honest paths have different fingerprints but, by the bent identity, exactly equal energy.

**Expected move.** Prove that every signed accepting splice contaminates \(\Omega(L)\) hash blocks, then recursively obtain adverse growth \(\lambda>\mu\).

**Audit.** **Z:** no slack, though an exact hash kernel still kills it. **O:** one global covered flow, not private clause rows. **X:** all states and tags are emitted integer coordinates. **A:** not a common syndrome; affine cancellation remains possible. **P:** characters exceed degree three, but additive copies remain dangerous. **D:** use a biased layer center; exact DROP audit required. **S:** this directly targets the two-negative splice. **G:** not outside until a two-level \(\lambda>\mu\) computation. **T:** no rank-one/tensor premise. **C:** bent equal-energy identity must be certified exactly.

**Experiment/falsifier.** Use the eight-clause three-variable contradiction, its seven-clause control, modulus \(7\), and a 3-level hash cover; emit both CVPs and exhaust the complete shell through twice the control radius. Any equal-energy signed splice falsifies it.

**Likely death.** Polynomial hash-state width may be insufficient to prevent affine path cancellation.

---

## 2. Bounded-degree Macaulay–SNF residual amplifier

**Core trick.** Form the Boolean clause ideal using \(x_i^2-x_i\) and falsifying-monomial equations, then emit the degree-\(d\) Macaulay system on moment variables. If normalization is inconsistent over \(\mathbb Q\), exact Smith/rank certificates eliminate every zero-residual signed pseudoevaluation; an arbitrarily polynomial residual weight then gives the gap directly.

**Expected move.** Find a polynomial-size sparse degree schedule that refutes every unsatisfiable 3CNF, while satisfying evaluations remain Boolean vectors of one common half-anchor radius.

**Audit.** **Z:** inconsistency removes exact kernels rather than amplifying them. **O:** equations are global. **X:** no external ideal-membership filter; the full Macaulay matrix is emitted. **A:** affine lifts are exactly normalized pseudoevaluations and are excluded only if the rank test succeeds. **P:** not outside—parity can survive above degree \(d\). **D:** zero moments violate the scaled normalization row. **S:** signed mixtures are included. **G:** no composition is needed after inconsistency. **T:** no tensor restriction. **C:** all Boolean moment vectors have identical half-anchor energy.

**Experiment/falsifier.** For the eight-clause three-variable contradiction and seven-clause control, build \(d=1,2,3\) matrices, certify rational consistency by RREF/SNF, emit \(M=25\), and enumerate the resulting exact CVP shell. A normalized degree-3 pseudoevaluation kills the first instance.

**Likely death.** General 3CNFs may require degree \(\Omega(n)\), making the Macaulay lift exponential.

---

## 3. Flag-calibrated exterior compound recursion

**Core trick.** Compose two clause tiles in flagged orthogonal spaces and encode their joint state in the cross-exterior block \(E_1\wedge E_2\). Scale contraction directions so that decomposable transversal forms represent honest products, while any nondecomposable integral form should incur a calibration cost detectable by its second skew singular value.

**Expected move.** Establish a two-level inequality where malformed exterior rank costs more than legal decomposable growth, then iterate a balanced clause tree.

**Audit.** **Z:** zero base residuals may still produce cheap exterior forms. **O:** joint states live in a shared compound block. **X:** only the compound lattice and target are emitted. **A:** affine combinations become general forms and are not automatically excluded. **P:** exterior rank can detect some parity mixtures; additive decomposable parities remain. **D:** flagged contractions are intended to charge missing factors. **S:** signed mixtures are unrestricted forms. **G:** requires an exact adverse/legal recurrence. **T:** this confronts entanglement geometrically, but is not outside G30 until low-distance decomposability is proved. **C:** flagged honest wedges must pass exact cosphericity/PD checks.

**Experiment/falsifier.** Use all four 2-CNF clauses on two variables versus the three-clause control; form the two-level cross-exterior lattice and exactly search all coefficient matrices in the shell through \(2R_{\rm control}^2\). Any rank-\(\ge2\) shortcut at the legal growth bound kills it.

**Likely death.** An integral rank-two perturbation may lie one unit from the target regardless of flag scaling.

---

## 4. Delaunay-diode gates with free-sum gluing

**Core trick.** Search for a rational positive-definite gate lattice whose satisfying truth-table points form one empty Delaunay face, while the falsifying port lies beyond a designated facet and zero/DROP lies farther still. Glue gates by free sums along the port face; unlike identifying linear marginals, free-sum geometry may preserve an empty-sphere certificate under composition.

**Expected move.** Find a gate pair with exact legal growth \(\mu\) and adverse growth \(\lambda>\mu\); a depth-\(O(\log n)\) balanced circuit would then yield \(n^c\).

**Audit.** **Z:** empty-cell separation concerns all lattice points, including residual-zero ones. **O:** face gluing replaces private-row overlap, but composition is unproved. **X:** Gram matrix, center, and gluing are emitted. **A:** affine mixtures remain lattice points and must fall outside the empty sphere. **P:** no degree cutoff; additive parity may still glue cheaply. **D:** diode asymmetry explicitly includes the zero port. **S:** signed coefficients are covered by the Delaunay shell. **G:** the required \(\lambda>\mu\) test is central. **T:** no tensor/rank assumption. **C:** common radius and positive definiteness are exact synthesis constraints.

**Experiment/falsifier.** Enumerate integral \(4\times4\) Gram matrices with entries \([-4,4]\) for a two-input AND graph, then compose two gates sharing one port and exhaust the exact shell. Nonclosure or \(\lambda\le\mu\) kills it.

**Likely death.** Empty Delaunay faces are local; shared-port signed circuits may destroy emptiness immediately.

---

## 5. Cyclotomic-unit fingerprints and the product formula

**Core trick.** Tag selector labels by cyclotomic units and emit all Minkowski embeddings as integer multiplication-matrix coordinates. Choose phase families with exact constant autocorrelation on honest assignments; a nonzero harmful fingerprint would then be forced by the algebraic norm/product formula to have energy in several conjugates simultaneously.

**Expected move.** Use degree \(O(\log n)\) and polynomial-bit unit powers so harmful energy grows polynomially while honest autocorrelation stays fixed.

**Audit.** **Z:** unlike G1, tags attach directly to selectors, not slack residuals; an exact algebraic relation still kills it. **O:** conjugate blocks are shared globally. **X:** embeddings use explicit integral matrices, with no external norm test. **A:** affine collisions map to affine unit combinations and may vanish; not outside. **P:** full conjugate spectra are not bounded-degree moments, but copies can remain additive. **D:** include a translated target making the zero block farther. **S:** signed coefficients are native algebraic-integer combinations. **G:** polynomial relative growth remains unproved. **T:** no rank-one premise. **C:** constant autocorrelation must give an exact rational common sphere.

**Experiment/falsifier.** In \(\mathbb Q(\zeta_{17})\), enumerate label-phase assignments for the nine-clause obstruction/control, solve exact center equations, emit multiplication matrices, and exhaust the G13/DROP shell. Failure of cosphericity or any zero unit combination kills it.

**Likely death.** Product-formula lower bounds may be tiny relative to the honest radius, and affine unit relations may persist.

---

## 6. Integer-aware SOS synthesis of a multiscale Gram metric

**Core trick.** Search a restricted rational Gram family—Walsh blocks, overlap characters, and formula-incidence cross terms—while simultaneously seeking an exact sum-of-squares certificate of the desired distance bound. The certificate may use valid integer inequalities \(z_i(z_i-1)\ge0\), so unrestricted signed coefficients are covered even though the emitted CVP objective remains purely quadratic.

**Expected move.** Discover a symbolic metric rule whose SOS margin grows under a balanced graph lift, yielding a polynomial NO/YES ratio without separately classifying attacks.

**Audit.** **Z:** any exact kernel is included in the certified domain. **O:** Gram terms are global. **X:** SOS is only a proof; the factor and target are fully emitted. **A:** affine lifts must satisfy the same certified inequality. **P:** certificate degree, not feature degree, is the vulnerability. **D:** zero blocks are explicitly in the domain. **S:** negative coefficients are included. **G:** require a two-level certified margin larger than legal growth. **T:** no tensor restriction unless tensor features are added. **C:** exact equal-radius equations and \(Q\succ0\) are imposed before soundness.

**Experiment/falsifier.** Solve a rational degree-4 SDP for the G31 obstruction/control and its G32 two-copy instance, then verify the dual certificate exactly and enumerate the certified shell. Infeasibility, singular-only \(Q\), or additive cost \(432\) kills it.

**Likely death.** Constant-degree SOS will probably reproduce the same affine/parity pseudodistributions; growing degree destroys polynomial size.

**Classical anchors:** Rothaus, “On bent functions” (1976); Macaulay, *The Algebraic Theory of Modular Systems* (1916); Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999); Neukirch, *Algebraic Number Theory* (1999); Parrilo, *Structured Semidefinite Programs and Semialgebraic Geometry Methods* (2000).
