### 1. Cosystolic collision lift

**Core trick.** For a 3DM selection \(x\), form the sparse quadratic collision vector \(\chi(x)=(x_i x_j)_{i\sim j}\), where \(i\sim j\) means the triples intersect. Lift to \(\Phi(x)=(x,E\chi(x))\), with \(E\) an explicit BCH or expander-code generator; matchings have \(\chi=0\), while every semantic nonmatching odd cover has a collision.

**Expected move.** Obtain YES cost \(q\) and NO cost \(q+\Omega(d(E))\), without the duplicate-walk inflation of I27.

**Obstruction check.** **Bounded local signatures:** applies honestly—quadratic lifts have 3-cube trades wherever the feasible fiber contains such a cube. **Marginal/tableau:** no affine wire interfaces. **Local-view hierarchies:** collision coordinates are global codewords, not scope tables. **Phase lifts:** no phases. **Integer exact fibers:** binary nonlinear lift, not slack repair. **Complete fingerprints:** only polynomially many edges, not assignments. **Tensor amplification:** no tensor claim; every mixed lifted word must be checked. **Exact transfer:** applies if the resulting binary fiber separates.

**Falsification.** Any mixed word cancelling \(E\chi\) at cost at most the worst YES cost.

**Smallest experiment.** Add all overlap-pair monomials to the existing all-eight and holonomy suites, encode them by a \([7,4,3]\) Hamming code, and enumerate the entire lifted span.

**Likely death.** The all-eight quadratic cube cancellation survives \(E\).

---

### 2. Truncated 2-adic carry tower

**Core trick.** Replace parity coverage by coverage modulo \(2^r\): binary selections satisfying \(Ax=\mathbf1\bmod 2^r\) must have exact degree one when \(2^r\) exceeds every possible degree. Use a polynomial-length generalized Gray/Lee embedding for \(r=O(\log N)\), together with a global alphabet shield intended to make symbols outside \(\{0,1\}\) expensive.

**Expected move.** Eliminate odd covers through higher carries rather than amplify their additive Hamming excess.

**Obstruction check.** **Bounded local signatures:** a bounded-degree alphabet shield is covered by finite differences. **Marginal/tableau:** bitwise carry conversion is covered and therefore forbidden unchanged. **Local-view hierarchies:** one global modular equation lies outside scope consistency. **Phase lifts:** irrelevant. **Integer exact fibers:** directly threatens the idea—CRT/carry slacks admit cheap repairs unless the alphabet shield is genuinely global. **Complete fingerprints:** coordinates are triples, not assignments. **Tensor amplification:** unused. **Exact transfer:** the existing mod-2 transfer does not directly handle \(\mathbb Z/2^r\); a new exact Lee-to-Euclidean lift is required.

**Falsification.** A nonbinary ring solution of Lee cost \(O(q)\), or any constant-cost carry repair.

**Smallest experiment.** For \(q=2,3\), use \(r=3\), enumerate all \(\mathbb Z_8\) solutions, and test candidate ghost-coordinate shields \(a\mapsto(a,a(a-1))\).

**Likely death.** Enforcing the binary alphabet recreates the killed tableau or polynomial-slack obstruction.

---

### 3. Code-dependent noncommutative automata hitting set

**Core trick.** Regard an order-\(r\) tensor coordinate as a word \(i_1\cdots i_r\). Fold words through a precommitted family of finite automata by mapping them to entries of \(M_{i_1}\cdots M_{i_r}\); stack an inner simplex encoding so every nonzero automaton output contributes substantial Hamming support.

**Expected move.** A deterministic hitting family for the noncommutative polynomials represented by all mixed tensor words could preserve soundness with polynomially many automaton states, unlike the frozen \(M_3(\mathbb F_4)\) and \(A_4\) maps.

**Obstruction check.** **Bounded local signatures:** linear folding cannot erase an existing cube trade; it only targets tensor length. **Marginal/tableau:** no gate transcript. **Local-view hierarchies:** words are global. **Phase lifts:** no phases. **Integer exact fibers:** binary construction. **Complete fingerprints:** labels index base columns, not assignments. **Tensor amplification:** directly addresses arbitrary mixed words if the hitting theorem covers the entire tensor subspace. **Exact transfer:** applies after binary rank accounting.

**Falsification.** A pointed kernel, worst YES at least best NO, or required automaton width/family size superpolynomial.

**Smallest experiment.** Enumerate every two-state automaton over \(\mathbb F_4\) for reduced squares of the all-eight, holonomy, and ten YES/NO codes; greedily select a fixed hitting subfamily, then freeze and generalize.

**Likely death.** General mixed tensors require exponential-width noncommutative PIT, while simplex blocks densify YES words.

---

### 4. Exterior-rank shell for mixed tensors

**Core trick.** View a reduced-square mixed word as a coefficient matrix \(W\). Preserve rank-one pure YES squares cheaply, but charge higher-rank mixed words through Plücker data—\(2\times2\) minors, then higher exterior powers—after code-dependent rank-condensing sketches.

**Expected move.** Reduce soundness to a dichotomy: rank one inherits squared base distance, while rank at least two pays a large zero-baseline exterior penalty.

**Obstruction check.** **Bounded local signatures:** minors are quadratic and therefore have cube relations if represented as polynomial signatures. **Marginal/tableau:** enforcing Plücker consistency through local gates is covered. **Local-view hierarchies:** global minors themselves are outside scope tables. **Phase lifts:** irrelevant. **Integer exact fibers:** polynomial slack implementations risk constant repairs. **Complete fingerprints:** matrix coordinates remain polynomial. **Tensor amplification:** explicitly classifies arbitrary mixed words by rank. **Exact transfer:** applies only after producing a linear binary syndrome image.

**Falsification.** A rank-two NO word with zero exterior image, or a rank-one semantic illegal word as cheap as YES.

**Smallest experiment.** On every \(8\times8\) reduced-square word, append all \(2\times2\) minors, enumerate the nonlinear images and their affine span, and attack all-eight and holonomy.

**Likely death.** No nonzero linear map can vanish on every rank-one matrix because rank-one matrices span the full matrix space; linearizing minors reintroduces cheap superpositions.

---

### 5. Kummer–Jacobian sparse dictionary

**Core trick.** Assign each triple a divisor class on an explicit small-genus curve and map sums through a Kummer/theta embedding. Perfect matchings should lie on a designated low-degree translate, while nonmatching odd covers should land outside it and acquire large AG-code evaluation weight.

**Expected move.** Obtain a polynomial sparse dictionary with genuinely global, high-degree addition laws and no bounded local interfaces.

**Obstruction check.** **Bounded local signatures:** outside only if theta coordinates are evaluated globally at degree growing with the instance; fixed degree is covered. **Marginal/tableau:** no proper marginals unless addition is circuit-linearized. **Local-view hierarchies:** divisor class is global. **Phase lifts:** not a single-valued local phase. **Integer exact fibers:** no count slack, though addition circuits would re-enter it. **Complete fingerprints:** outside if columns remain triple/divisor generators; one Kummer column per assignment would be covered and exponential. **Tensor amplification:** unused; every affine secant combination needs soundness. **Exact transfer:** available after binary expansion, with bit-weight distortion explicitly bounded.

**Falsification.** An illegal odd cover in the affine secant span of cheap matching Kummer points, especially all-eight.

**Smallest experiment.** Choose an elliptic curve over \(\mathbb F_{11}\), assign the eight \(q=2\) triples to points, enumerate assignments and all signed/odd affine combinations of their Kummer coordinates.

**Likely death.** Secant identities reproduce the legal affine-closure collapse, or succinct group addition becomes a killed circuit tableau.

---

### 6. Seeded condenser with protected global sectors

**Core trick.** Use an explicit polynomial family of lossless condensers \(h_s\) so each sparse YES witness has some seed under which its support is isolated, while every NO fiber is conjecturally dense for every seed. Encode the seed globally by Reed–Solomon Lagrange idempotents and couple \(h_s(x)\) to it, aiming for one cheap protected sector without enumerating witnesses.

**Expected move.** Realize the needed asymmetric operation: existentially sparse on every YES fiber but uniformly expensive on NO fibers.

**Obstruction check.** **Bounded local signatures:** the seed–data coupling is bilinear and hence covered if independent seed/data cubes survive. **Marginal/tableau:** one-hot seed wiring is covered and must not be used. **Local-view hierarchies:** condenser outputs are global. **Phase lifts:** a formula-dependent global selector lies outside the coboundary theorem, but branch splicing remains a threat. **Integer exact fibers:** polynomial seed slacks are covered. **Complete fingerprints:** only polynomial seeds and sparse columns. **Tensor amplification:** not ordinary tensoring; all mixed branch superpositions require proof. **Exact transfer:** applies to a successful binary construction.

**Falsification.** A rectangle splice combining two seeds into a cheaper NO word, or worst-YES sector overhead erasing the gain.

**Smallest experiment.** Use four affine hash seeds on the \(m=8\) suite, encode seed idempotents over \(\mathbb F_{16}\), and enumerate all mixed sector words including all-eight and holonomy.

**Likely death.** Global seed superpositions recreate I05’s branch splice or the degree-two cube trade.

---

### 7. Sparse zig-zag product of exact-cover fibers

**Core trick.** Replace the full tensor square by expander-selected coordinate pairs \((i,j)\), then add exact left/right incidence constraints tying all selected pairs to one outer cover. Iterate with fresh zig-zag expanders, seeking multiplicative collision growth while using only \(O(Dn)\), rather than \(n^2\), coordinates per round.

**Expected move.** Prove directly that YES matchings lift with \(O(Dq)\) support, whereas every NO odd cover or mixed word creates \(\Omega(D)\) independent defects per base defect.

**Obstruction check.** **Bounded local signatures:** bounded pair signatures may retain cube trades. **Marginal/tableau:** applies if consistency factors through endpoint marginals; the proposed exact global incidence rows must do more. **Local-view hierarchies:** expander neighborhoods are still proper scopes, so twisted holonomy is a direct threat. **Phase lifts:** no phases. **Integer exact fibers:** binary construction. **Complete fingerprints:** only selected pairs. **Tensor amplification:** this is code-dependent structured sparsification; the code-oblivious sampling no-go does not apply, but arbitrary mixed words remain mandatory. **Exact transfer:** applies with output rank \(O(Dn)\).

**Falsification.** Any all-eight/holonomy pseudoassignment, pointed kernel, or exponent no better than the unfurled base.

**Smallest experiment.** Enumerate all 2-regular and 3-regular bipartite selectors on the \(8\times8\) reduced square; add both incidence projections and test every mixed word on the hostile suite.

**Likely death.** Endpoint consistency is merely a marginal encoding, or sparse sampling deletes precisely the NO-support coordinates.
