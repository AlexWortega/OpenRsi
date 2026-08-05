## Generation 21 — divergent mechanism sketches

### 1. Delaunay-hole clause gluing
**Core trick.** Represent the eight local truth patterns by vertices of a fixed Delaunay simplex, placing the target equidistant from the seven satisfying vertices but farther from the forbidden one. Glue clause lattices along geometric truth facets, rather than identifying selector marginals; incompatibility should move the target outside the glued empty sphere.

**Expected move.** A satisfiable formula chooses shell vertices, while unsatisfiability forces a polynomially amplified hole-depth loss.

**Obstruction audit.** G1 RS slack: no slack. G2 affine isolation/G3 fiber certificate/G5 overlap: no selector fibers. G6 external filters: all gluing equations must be emitted. G7 radix: no residual coding. G9 PSD parity/G11 cubic parity/G13 affine hash: no moment/hash representation. G12 clause drop remains a threat. G14 pair-bag gives no theorem here. G15 hierarchy threading is absent. G19 flow splicing is irrelevant. G20’s specification objection remains unless the lattice and target are frozen.

**Experiment/falsifier.** Use an \(A_7^*\) Delaunay simplex for the eight-clause three-variable obstruction; glue eight copies by equality of designated truth-facet coordinates and enumerate both obstruction and satisfiable control. Kill if a dropped clause or new lattice point reaches control radius plus constant.

**Likely death.** Fiber gluing creates unintended short lattice points, or completeness radius swamps hole depth.

---

### 2. Global Walsh-uncertainty certificate, then sparse compression
**Core trick.** Let \(u\in\mathbb Z^{2^n}\) be a signed global-assignment distribution and append its unnormalized Walsh transform \(Hu\). Since \(\|Hu\|_2^2=2^n\|u\|_2^2\), every honest delta assignment has equal radius, whereas a multi-term affine pseudodistribution pays according to its coefficient mass.

**Expected move.** Prove unsatisfiable clause-marginal equations require \(\|u\|_2\ge n^\epsilon\), then replace full Walsh coordinates by a deterministic polynomial-size restricted-isometry family.

**Obstruction audit.** G1 has no slack. G2/G3/G5 concern local selectors, not global \(u\). G6 constraints are emitted. G7 zero residual does not erase Fourier norm. G9/G11 parities are charged globally. G12 dropping \(u\) violates a heavily weighted normalization. G13’s affine collision is not invisible because honest words share radius, not syndrome. G14 is merely comparative evidence. G15 affine threading now incurs transform norm, though perhaps only constant. G19 flow is absent. G20’s mass-versus-baseline and asymptotic-compression objections remain fully applicable.

**Experiment/falsifier.** On the four-variable instance, emit \(u\in\mathbb Z^{16}\), \(v=H_{16}u\), normalization and forbidden-assignment marginals; exactly minimize \(\|u\|^2+\|v\|^2+W^2\|Au-b\|^2\). Kill if obstruction/control ratio is no better than constant or a two-term solution wins.

**Likely death.** Exponential dimension, or constant-norm signed solutions for large formulas.

---

### 3. Torsion-systolic mapping-cone encoding
**Core trick.** Build a cellular mapping cone from clause-label stalks and occurrence restrictions, then convert failure to glue into a nonzero torsion homology class. Attach the cone to an explicit complex with large integral systole, so any chain representing that class must have broad support rather than a local consistency residual.

**Expected move.** A zero-residual affine pseudosection becomes a long nontrivial cycle, yielding polynomial Euclidean mass.

**Obstruction audit.** G1 has no slack. G2/G3/G5 local affine isolation is replaced by homology. G6 requires the full boundary matrix and target cycle to be emitted. G7 radix kernels are irrelevant. G9/G11 parity may become precisely a homology class rather than vanish. G12 drops should create boundary. G13 affine closure remains dangerous: affine combinations are still chains. G14 supplies no systolic law. G15 directly kills ordinary sheaf restrictions; this survives only if its witness maps to nonzero torsion. G19 has no flow. G20’s unspecified-sheaf objection is avoided only by freezing cells and maps; its pseudosection objection remains substantive.

**Experiment/falsifier.** Construct the mapping cone of the current nine-clause restriction complex, attach order-three Moore cells to every consistency loop, compute Smith normal form, and minimize chain norm in the target torsion class. Kill if the G13 witness remains null-homologous or has constant support.

**Likely death.** Formula information lives in boundaries, while the torsion class is formula-independent or cheaply localized.

---

### 4. Truncated noncommutative path signatures
**Core trick.** Lift each branching-program transition into the truncated free associative algebra on transition letters. Besides flow conservation, preserve degree-\(1,\ldots,d\) ordered-word signatures; signed splicing can match endpoint flow while failing to match the ordered products of a genuine computation.

**Expected move.** Any accepting signed flow should require a defect whose support grows with program length or truncation degree.

**Obstruction audit.** G1 has no slack. G2/G3/G5 selector isolation is not used. G6 all signature coordinates must be lattice coordinates. G7 commutative residual kernels need not preserve word order. G9/G11 cube parity is unrelated. G12 dropping a layer changes normalization and signatures. G13 affine combinations of complete rejecting paths still reject, but arbitrary affine flows remain a threat. G14/G15 bag and hierarchy results do not cover noncommutative order. G19 signed splicing is the exact obstruction being strengthened, not escaped by assumption. G20’s transition-table criticism still applies unless signatures defeat newly found cycles.

**Experiment/falsifier.** Compile the eight-clause three-variable obstruction into the shortest deterministic width-five program available; emit degree-two and degree-three word coordinates and run exact shell DP against a satisfiable control. Kill if accepting zero-residual excess stays bounded as \(d\) increases.

**Likely death.** Low-degree polynomial identities permit splicing; sufficient degree causes exponential dimension.

---

### 5. Hensel-idempotent Booleanity tower
**Core trick.** Over \(\mathbb Z/2^k\mathbb Z\), idempotence \(x^2=x\) has only \(x=0,1\); encode schoolbook multiplication and carries so every exact low-shell solution represents an actual idempotent residue. Once the exact zero fiber is Boolean, multiplication and clause residuals can be weighted polynomially without relying on sparse unsatisfaction.

**Expected move.** Replace weak half-integral anchors by arithmetic uniqueness across increasing \(2\)-adic precision.

**Obstruction audit.** G1’s free slack is excluded only if every carry is table-constrained. G2/G3/G5 local hashes are absent. G6 forbids externally bounded carries. G7 zero-residual signed selectors are a direct threat. G9/G11 moments do not enforce idempotence. G12 table drops must be normalization-expensive. G13 raw linear compatibility does not cover multiplication lifts, but affine pseudomultiplication may persist. G14 gives no carry theorem. G15 affine threading may lift through every bit. G19 predicts signed table splicing. G20’s carry-table blocker applies squarely; this is the frozen depth sweep it demanded, not an assumed solution.

**Experiment/falsifier.** For \(k=2,3,4,5\), emit one selector for every legal full-adder row, complete input/output marginals, idempotence output, anchors, and weight-25 residuals. Exactly find the minimum non-Boolean zero-residual vector. Kill if its excess is depth-independent.

**Likely death.** A small signed pseudodistribution realizes fake multiplication at every precision.

---

### 6. Permutation-matrix transport instead of scalar flow
**Core trick.** Replace each scalar branching-program flow layer by an integral matrix with every row and column summing to one. At minimum Frobenius norm such a matrix must be a permutation; transition permutations preserve any non-permutation defect, potentially forcing a signed splice to pay across many layers rather than at two edges.

**Expected move.** Convert the G19 localized splice into a persistent transport defect with length-growing energy.

**Obstruction audit.** G1 has no slack. G2/G3/G5 local selector fibers are replaced by global transport geometry. G6 row, column, transition, and query equations must all be emitted. G7 radix kernels are irrelevant. G9/G11 parity mixtures become signed transport matrices and may be charged each layer. G12 dropping a layer violates many sums. G13 affine combinations remain feasible but generally have excess Frobenius norm. G14 pair bags are not used. G15 threading remains possible, now unweighted at every layer. G19 is the direct seed attack. G20’s linear-transition and baseline objections remain: persistence may yield only a constant ratio.

**Experiment/falsifier.** Replace each width-five layer of a small G19 program by a \(5\times5\) transport matrix; split queried transitions into two matrices tied to shared query totals. Exact-DP shell excess \(0,2,\ldots,20\). Kill if an accepting splice has depth-independent excess or if affine path mixtures beat honest controls.

**Likely death.** Signed transportation cycles localize despite row/column constraints, or persistent cost merely tracks completeness baseline.

### Classical ingredients cited
Delaunay/Voronoi lattice geometry: Conway–Sloane, *Sphere Packings, Lattices and Groups*; Walsh uncertainty: Donoho–Stark (1989); mapping cones and torsion: standard cellular homology; noncommutative signatures: K.-T. Chen (1954); Hensel lifting: Serre, *Local Fields*; permutation transport: Birkhoff–von Neumann theory.
