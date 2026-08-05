I use the obstruction-map labels: **O1** bounded local signatures; **O2** marginal/tableau encodings; **O3** local-view hierarchies; **O4** phase lifts; **O5** integer exact fibers; **O6** complete-assignment fingerprints; **O7** tensor amplification/compression; **O8** exact syndrome-to-CVP transfer.

### 1. Splitter–Veronese collision lift

**Mechanism.** For the triple-incompatibility graph \(G\), add features equal to products along colorful connected patterns of size at most \(r=\Theta(\log m)\), using an explicit perfect-hash family. Matchings activate none; a near-minimum odd cover has a constant-size collision defect that some hash isolates, while growing degree aims to destroy the all-eight affine cube cancellation.

**Expected move.** Obtain zero YES overhead and \(m^{\Omega(1)}\) NO feature weight with polynomially many patterns.

**Map.** O1: outside only when degree grows; fixed \(r\) is covered. O2: direct global products, no marginals. O3: patterns span the global collision graph. O4: no phases. O5: binary nonlinear lift, not affine integer slack. O6: polynomial pattern dictionary, not assignments. O7: no full tensor, but every mixed lift word still needs proof. O8: applies once its binary generator and rank are explicit.

**Falsification/test.** Enumerate the lifted affine span for all-eight, holonomy, affine-closure, and \(q=3\) YES/NO instances at \(r=3,4\); record worst YES, best NO, mixed kernels, and rank.

**Likely death.** Computing the lift span may require exponentially many message monomials, or hostile odd sums may cancel every colorful feature.

---

### 2. Plücker-defect rank shell

**Mechanism.** For each cover \(x\), form its three pair-projection matrices and the global defects \(D_{ab}(x)=P_{ab}(x)P_{ab}(x)^T-I\). Lift selected minors of these defects, then apply explicit rank condensers/subspace designs so a rank-\(\rho\) defect lights many binary blocks, while every genuine matching has zero defect.

**Expected move.** Convert “non-permutation projection” into support without paying the \(3q\) table norm baseline of I18.

**Map.** O1: minors have growing degree \(2s\); constant \(s\) remains covered. O2: no unary interfaces or gate tableaux. O3: full projection matrices are global. O4: no phases. O5: zero-baseline binary defects, not integer table variables. O6: only polynomially selected minors, not assignments. O7: condenser blocks replace tensor powers, but mixed-word support is unproved. O8: directly usable after binary expansion.

**Falsification/test.** At \(q=3\), compute all \(1\times1\) and \(2\times2\) defect minors for every affine-fiber word; span their lifts and exhaust all-eight, holonomy, affine-closure, and 200 NO dictionaries.

**Likely death.** Illegal odd affine combinations may satisfy all Plücker identities, or rank condensers may again preserve nonzeroness while flattening YES/NO Hamming support.

---

### 3. Expander-walk tuple packing

**Mechanism.** Replace Cartesian direct products by walks of length \(r\) in a constant-degree expander on base coordinates. Pack the \(r\) symbols encountered by each walk injectively into \(\mathbb F_{2^r}\), then simplex-encode each field symbol; a block is nonzero iff the walk hits the base error support.

**Expected move.** Realize the distance transform \(d\mapsto\#\{\text{walks hitting a \(d\)-set}\}\) with only \(nD^{r-1}2^r\) binary coordinates, polynomial for \(r=O(\log n)\).

**Map.** O1: not outside—linear cube relations survive. O2: tuple packing is one global linear map, not an OR tableau. O3: expander walks are nonlocal. O4: no phases. O5: no integer fibers. O6: coordinates are walks, not assignments. O7: it is structured code-oblivious sampling, so the sampling warning applies; OR-style tuple weight is the only distinction. O8: binary simplex output transfers exactly.

**Falsification/test.** Apply \(r=2,3,4\) walk packings to the existing BMT YES/NO, all-eight, and holonomy codes; enumerate all mixed image words and rank.

**Likely death.** The concave transform \(1-(1-d/n)^r\) probably shrinks the nearby \(q\) versus \(q+2\) ratio, while simplex expansion consumes any length saving.

---

### 4. Color-coded Lindström determinant transfer

**Mechanism.** Compile triples into a formula-specific layered DAG where a matching is a vertex-disjoint path family. Assign vertex-factor edge labels so every perfect family has the same total monomial, and output color-coded coefficients of the Lindström determinant minus that monomial; collisions should leave unmatched coefficients without enumerating \(q!\) routes.

**Expected move.** Obtain a succinct global permutation selector whose feature count is polynomial for logarithmic color depth.

**Map.** O1: degree grows with path-family size; bounded depth is covered. O2: direct symbolic determinants are outside, but bounded-fan-in determinant circuits are not. O3: disjointness is checked globally. O4: no phase labels. O5: no affine integer slack. O6: DAG coefficients, not complete assignments. O7: not tensor multiplication; arbitrary mixed determinant-lift words remain the key obligation. O8: applies if coefficients are emitted as a polynomial-rank binary code.

**Falsification/test.** Build the \(q=3\) DAG explicitly, expand all determinant coefficients, and enumerate lifted spans for planted YES/NO, all-eight, holonomy, and affine-closure dictionaries.

**Likely death.** Characteristic-two determinant cancellation may erase collision data; any succinct circuit linearization may reproduce the tableau fault, while direct coefficient expansion may become exponential.

---

### 5. Vertex-factor group-algebra checksum

**Mechanism.** Label every vertex by \(g_v\) in a polynomial-size odd-order group and each triple by \(g_ug_vg_w\). The product over a matching is the fixed element \(\prod_v g_v\), whereas a \(q+2\) odd cover differs by a product encoding three excess vertex incidences; choose labels from a \(B_3\)/BCH set so that difference cannot vanish.

**Expected move.** Detect every closest NO cover with a zero-baseline, genuinely global multiplicative checksum, then replicate its nonidentity group-algebra support.

**Map.** O1: checksum degree is the cover size, not bounded. O2: direct product is outside; an automaton/tableau implementation is not. O3: uses all selected triples. O4: not a local cycle phase, though coboundary-like trivialization is a risk. O5: no integer repair columns. O6: polynomial group states, not assignments. O7: no tensor powering. O8: conditional on an explicit binary linear realization.

**Falsification/test.** For \(q=2,3\), brute-force cyclic groups \(C_p\), vertex labels, and all fiber words; compute group products and the span of one-hot lifts on all hostile families.

**Likely death.** Multiplication is nonlinear: producing the lifted binary generator may itself require exponential enumeration or a forbidden local tableau. Larger-weight NO covers may also evade a checksum designed only for three excesses.

---

### 6. Hash-isolated legal sectors with global selector coding

**Mechanism.** Use a polynomial family of hash weights \(w_s\) and create sectors indexed by \((s,\sum_jw_s(j)x_j)\). Within each sector attach a BCH shell to the triple indicator, while a single expander-code constraint globally ties the seed/value selector; a legal witness only needs one seed under which it is isolated, without the reduction finding that witness.

**Expected move.** Avoid quotienting all legal matchings: isolated witnesses receive separate protected sectors, while odd affine superpositions should violate either BCH distance or global selector consistency.

**Map.** O1: hashes/BCH are global linear data, so local cube relations may still survive honestly. O2: global selector coding is outside proper marginals, but sector splicing is a direct threat. O3: no bounded scopes. O4: this is precisely the formula-dependent global-selector opening, not copy-stable local phases. O5: binary only. O6: polynomial hash sectors, not assignment columns. O7: no tensor. O8: immediate for the resulting syndrome system.

**Falsification/test.** Enumerate small perfect matchings, search fixed pairwise-independent hash families with polynomial range, construct the complete sector code, and attack every mixed word on affine-closure, all-eight, and holonomy instances.

**Likely death.** Polynomially many hashes may not isolate arbitrary matching families, and linear combinations may splice different sectors despite the expander constraint.
