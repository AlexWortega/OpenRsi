Unranked, deliberately divergent sketches. None relies on the prohibited source.

### 1. Logarithmic cosystolic scope code

**Mechanism.** Choose formula-dependent, disconnected scopes \(S_j\) of size \(\ell=\Theta(\log n)\) from an explicit cosystolic expander. Use one column \((S_j,a)\) per satisfying scope assignment, with full-degree indicator coordinates and dense global overlap hashes rather than unary marginals.

**Expected move.** Polynomially many columns remain because \(2^\ell=\mathrm{poly}(n)\); cosystolic expansion might turn one global inconsistency into \(n^{\Omega(1)}\) additional selected columns.

**Obstruction check.** Bounded local signatures: degree equals scope size, so its required larger cube is absent. Marginal/tableau: no proper marginals or wire interfaces. Local-view hierarchies: specifically uses growing disconnected logarithmic scopes, the stated opening; Petersen-style flows may still survive. Phase lifts: none. Integer exact fibers: binary, global full-degree signatures. Complete-assignment fingerprints: columns are scope assignments, not complete assignments. Tensor amplification: unused; the gap must be direct. Exact transfer: applies once \(H,t\) are produced, with output rank explicitly counted.

**Experiment/falsification.** Generate scopes of sizes \(3\!-\!6\); enumerate exact coset minima on the all-eight core, twisted cycles, Petersen flow, and tiny YES/NO 3DM. Kill if any support-\(O(1)\) pseudoassignment survives or rank exceeds the claimed polynomial budget.

**Likely death.** A higher-order charged flow survives every polynomial scope family.

---

### 2. Representation-valued nonabelian orbit folding

**Mechanism.** Replace cyclic orbit-XOR by a nonabelian Fourier transform: on each tensor-coordinate orbit, retain selected irreducible matrix blocks over \(\mathbb F_{2^s}\), then encode block rank with a binary rank-metric inner code. Choose retained representations from the instance code, not from a fixed puncturing rule.

**Expected move.** Multiplicity-free or low-fusion actions could compress an orbit of size \(|G|\) to polynomially many matrix entries while preserving every mixed word through a representation-theoretic support bound.

**Obstruction check.** Bounded signatures and marginal/tableau: no local-view encoding. Local-view hierarchy: irrelevant after the 3DM base. Phase lifts: not a scalar, single-valued local phase; it retains whole global representation blocks. Integer fibers and assignment fingerprints: absent. Tensor amplification: directly occupies the surviving code-dependent dense-fold opening and must cover arbitrary mixed words. Exact transfer: field blocks are binary-expanded; resulting rank and the square-root CVP loss are counted.

**Experiment/falsification.** Use the nonabelian group of order \(21\) on reduced \(q=3\) tensor squares. Enumerate every mixed word for all subsets of irreducible blocks; test all-eight/odd-holonomy-derived base codes and relabelings.

**Likely death.** Semisimplicity requires retaining essentially all \(\sum d_\rho^2=|G|\) information, eliminating compression; modular representations may collapse distance.

---

### 3. Recursive rank-profile tensor-network condenser

**Mechanism.** View an order-\(2^k\) tensor word through recursive bipartite flattenings. At each node apply explicit rank condensers and a binary rank-metric code, aiming to prove: a word is either high-rank at some node or decomposes into factors whose pointed leaf costs multiply.

**Expected move.** Pure YES tensors have bond dimension one, while dangerous mixed NO tensors should pay either rank or heavy-leaf cost. A bounded-width tree representation would give submultiplicative output size without ordinary puncturing.

**Obstruction check.** Bounded signatures, marginal/tableau, local scopes, phases, and integer-fiber repairs do not describe this global tensor-rank operation. Complete-assignment fingerprints are absent. Tensor amplification is exactly the relevant obstruction: unlike pure tensoring, the proposed asymmetric condenser must prove soundness for every mixed tensor word. Exact transfer applies after binary rank-metric encoding; all condenser blocks count toward \(N\).

**Experiment/falsification.** On existing \(q=3,m=8\) YES/NO codes, enumerate all reduced-square and fourth-power mixed words. Record rank across every balanced flattening; exhaust small linear condensers and require worst-NO cost \(>\) worst-YES cost at reduced rank.

**Likely death.** A pure rank-one NO minimum has the same rank profile as a YES power, while recursive leaf encoding restores the full tensor-length exponent.

---

### 4. Splitter-isolated protected witness sectors

**Mechanism.** Build a polynomial family of deterministic edge-weight splitters. Each sector fixes a weight sum and attaches a BCH syndrome shell intended to protect a uniquely isolated perfect matching, without identifying different matchings as in the killed quotient route.

**Expected move.** If candidate protected syndromes can be extracted without finding the matching, ordinary code distance can replace the failed affine legal-witness quotient and block odd affine combinations.

**Obstruction check.** Bounded signatures, marginal/tableau, local hierarchy, and phase-lift assumptions do not cover a formula-dependent global isolation sector. Integer exact-fiber repair is irrelevant in the binary version. Complete-assignment fingerprints do not formally apply because sectors use edge columns rather than assignment columns, although extracting their centers may recreate that obstruction. Tensor amplification is unused. Exact transfer applies, but every sector and BCH row contributes to output rank.

**Experiment/falsification.** For all existing \(q=3\) dictionaries, enumerate modular weights \(w_e\bmod p\), \(p\le 11\); identify isolated matchings by brute force, build distance-\(7\) BCH sectors, and enumerate all odd covers. Include all-eight and twisted-holonomy reductions.

**Likely death.** Computing even one useful protected syndrome is as hard as finding the isolated matching; enumerating all syndromes is exponential. This is the explicit falsification target, not an assumed capability.

---

### 5. Truncated Magnus–Fox filling-area shell

**Mechanism.** Encode consistency as a word in a fixed nonabelian group and legal witnesses as short van Kampen fillings. Use position-dependent Fox derivatives in a degree-\(D=\Theta(\log n)\) truncated Magnus algebra to obtain a polynomial binary boundary matrix; CVP weight measures filling area rather than homology class.

**Expected move.** Odd holonomy that is homologically trivial could still require \(n^{\Omega(1)}\) cells, avoiding the affine-closure failure of ordinary homology.

**Obstruction check.** Bounded signatures kills this if Magnus rows reduce to a degree-\(D\) Boolean-view signature with a \((D+1)\)-cube; survival requires genuinely prefix-dependent cell columns with no such cube. Marginal/tableau and integer-fiber obstructions apply if the filling is compiled into local wire tables; direct global Fox rows are outside them. Local-view hierarchy and phase lifts do not cover nonabelian filling area. Complete-assignment fingerprints are absent. Tensor amplification is unused. Exact transfer applies only after verifying the mod-2 boundary matrix preserves the area gap.

**Experiment/falsification.** Construct degree \(2,3,4\) Fox matrices for the twisted 3-cycle and all-eight core; solve minimum fillings by ILP, including signed and mod-2 chains.

**Likely death.** Truncation misses deep commutators, while sufficiently high degree or explicit position-labelled cells makes rank superpolynomial.

---

### 6. Noncommutative ABP Hankel dictionary

**Mechanism.** Represent assignment checking by a noncommutative algebraic branching program, but do not introduce gate transcripts. Retain global prefix–suffix Hankel blocks and encode their matrix rank through binary rank-metric checks; legal assignments should have one sparse accepting path, while superpositions create large residual rank.

**Expected move.** This would give a polynomial sparse transition dictionary with a global algebraic invariant, rather than complete-assignment columns or bounded-fan-in tableau rows.

**Obstruction check.** Bounded signatures: the product has global degree \(n\), outside bounded degree. Marginal/tableau and integer-fiber repairs return immediately if path-flow or wire variables are introduced; only direct Hankel rows escape. Local scopes and phase lifts are irrelevant. Complete-assignment fingerprints: transitions, not assignments, are columns. Tensor amplification is unused unless rank blocks are later composed. Exact transfer applies after field-to-binary expansion, with Hankel width included in \(N\).

**Experiment/falsification.** Build minimal ordered ABPs for the all-eight core, twisted cycles, and \(q=3\) exact cover. Enumerate all transition superpositions and compare Hankel-rank cost for YES paths versus NO accepting faults.

**Likely death.** Any ordering supporting arbitrary 3CNF requires exponential ABP width; polynomial-width relaxations admit low-rank false accepting combinations.

---

### 7. Collision-seeded nonbacktracking Schur walks

**Mechanism.** From the 3DM incompatibility graph, retain only Schur monomials indexed by nonbacktracking walks of length \(r=\Theta(\log q)\) beginning with two triples sharing a vertex. Perfect matchings make every such monomial zero; an odd cover has a degree-\(3\) collision that may seed many walk coordinates. Construct the mixed-word code symbolically from the affine generator, not through consistency gadgets.

**Expected move.** Obtain YES cost \(q\) but NO cost \(q+q^{1+\epsilon}\) using only \(m\Delta^r=\mathrm{poly}(m)\) coordinates.

**Obstruction check.** Bounded signatures: monomial degree grows with scope and equals walk size, outside fixed-degree cubes; test larger cubes explicitly. Marginal/tableau: no interfaces. Local hierarchy: scopes are growing, formula-global walks. Phase and integer-fiber obstructions are irrelevant. Complete-assignment fingerprints: only walk products occur. Tensor amplification: this is a code-dependent structured partial Schur power, not ordinary tensoring or frozen sampling; every mixed word must be checked. Exact transfer applies with walk count as output rank.

**Experiment/falsification.** For \(q=3,m=8\), generate lengths \(2\!-\!4\), symbolically expand product functions, row-reduce, and enumerate all mixed words on YES/NO, all-eight, and odd-holonomy instances.

**Likely death.** Minimal odd covers localize the collision in a constant component, and mixed Schur combinations cancel all propagated walks.
