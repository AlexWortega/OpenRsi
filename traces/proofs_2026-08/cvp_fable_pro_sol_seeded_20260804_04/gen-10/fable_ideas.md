I did not search for or use the prohibited document.

1. **Expander–Graver propagation compiler**  
**Core trick.** Replace each 3DM coefficient by occurrence-flows on a high-girth lossless expander, with conservation rows arranged so a Boolean matching has one canonical unit route. Seek a Graver-basis theorem: any signed non-Boolean exact cover must propagate a negative coefficient through polynomially many flow coordinates.  
**Expected move.** Improve integer squared distance from \(q\) versus \(q+2\) to \(O(q)\) versus \(\Omega(q^{1+c})\).

**Obstruction check.** Bounded local signatures: global routed columns, although local cubes may survive. Marginal/tableau: no truth tables. Local-view hierarchies: expander-wide conservation is global, but odd holonomy remains dangerous. Phase lifts: no phases. Integer exact fibers: **not safely outside**—all constraints remain affine, so constant repairs may persist. Complete-assignment fingerprints: only polynomial occurrence columns. Tensor amplification: none; enumerate every signed flow directly. Exact transfer: currently direct integer CVP, so a binary parity certificate is still missing.

**Falsification.** Any constant-support repair, or worst-NO/best-YES ratio tending to one.  
**Experiment.** Build 3- and 5-sheet lifts of existing \(q=3\) YES/NO, all-eight, and holonomy fixtures; enumerate coefficients in \([-2,2]\), recording norm and rank.  
**Likely death.** A short expander cycle carries the entire repair.

2. **Recursive span-program inconsistency amplification**  
**Core trick.** Compile the whole CNF into one binary span program using algebraic AND composition, then attach paired value-selectors whose inconsistency cost is recursively copied across expander-distributed formula branches. Use only the final global vectors—no gate transcript variables.  
**Expected move.** A satisfying assignment spans the target with \(O(n)\) columns, while any representation mixing both values of variables pays \(n^{1+c}\).

**Obstruction check.** Bounded local signatures: outside only if composed vectors have genuinely growing global degree; otherwise cube trades apply. Marginal/tableau: no wire interfaces. Local-view hierarchies: the target-span condition is formula-global. Phase lifts: none. Integer exact fibers: binary construction, not count slacks. Complete-assignment fingerprints: occurrence/selector columns, not assignment columns. Tensor amplification: recursive span composition is not ordinary distance tensoring, but all mixed span witnesses require proof. Exact transfer: immediately applicable if the final matrix is binary.

**Falsification.** Both-value selectors produce an \(O(n)\) representation, or all-eight/holonomy costs do not exceed the YES baseline.  
**Experiment.** Implement canonical \(\mathbb F_2\) span programs for four clauses, all-eight, and the twisted cycle; enumerate every target representation through depth three and report rank.  
**Likely death.** Algebraic AND composition preserves a small selector splice.

3. **Sparse nonlocal Macaulay–Koszul moments**  
**Core trick.** Use Boolean clause polynomials but retain only a formula-derived, expander-distributed family of monomials of degree \(D=\Theta(\log n)\); add their Macaulay equations and Koszul syzygies as one global binary syndrome system. A satisfying assignment gives a character moment vector, while UNSAT should force many violated syzygy coordinates.  
**Expected move.** Obtain logarithmic-degree global consistency with only \(n\Delta^D=\mathrm{poly}(n)\) columns for bounded occurrence.

**Obstruction check.** Bounded local signatures: not automatically outside; degree-\(D\) cubes remain a direct threat. Marginal/tableau: moments are not proper unary marginals. Local-view hierarchies: growing, disconnected nonlocal scopes lie beyond the fixed-level theorem, though Petersen and odd-holonomy attacks remain relevant. Phase lifts: none. Integer exact fibers: binary. Complete-assignment fingerprints: monomials, not assignment columns. Tensor amplification: none; arbitrary mixed moment vectors are native codewords. Exact transfer: applies after constructing the binary syndrome matrix.

**Falsification.** A unit-mass pseudocharacter on all-eight or holonomy, or superpolynomial monomial count.  
**Experiment.** At \(D=3,4\), generate expander-selected monomials for the hostile fixtures and enumerate the affine moment fiber exactly, including rank and YES weight.  
**Likely death.** Sparse Macaulay closure recreates a pseudoexpectation hierarchy.

4. **Pair-projection Gram contraction of pure squares**  
**Core trick.** From an affine basis \(x_0+K\), generate the entire span of pure quadratic lifts \(x\otimes x\) using \(O(\dim(K)^2)\) generators. Contract these tensors to the three pair-projection Gram and cross-Gram matrices; every matching gives permutation orthogonality identities using only \(O(q^2)\) output coordinates.  
**Expected move.** Preserve squared-distance amplification while deleting almost all tensor coordinates.

**Obstruction check.** Bounded local signatures: **inside its danger zone**—this is degree two, and dense contraction does not remove cube relations. Marginal/tableau: no local tables. Local-view hierarchies: projection Grams are global. Phase lifts: none. Integer exact fibers: binary quadratic lift. Complete-assignment fingerprints: generated from an affine basis, not assignments. Tensor amplification: explicitly targets code-dependent compression and includes every mixed pure-power word. Exact transfer: directly compatible.

**Falsification.** Any pointed kernel or hostile mixed word no heavier than the worst legal square.  
**Experiment.** Construct exact quadratic-span generators for all-eight, holonomy, affine-closure, and ten \(q=3\) YES/NO fibers; enumerate every compressed mixed word and output rank.  
**Likely death.** An odd XOR of legal squares inherits the same identity Gram state.

5. **Twisted Fox-Jacobian holonomy shell**  
**Core trick.** Turn the formula incidence complex into a finitely presented fundamental group and evaluate its Fox Jacobian under a canonical nonabelian representation, initially \(S_3\cong GL_2(\mathbb F_2)\). Append the resulting global twisted-boundary rows so inconsistent covers should carry expanding twisted homology rather than ordinary parity holonomy.  
**Expected move.** Detect odd permutation holonomy with polynomially many binary rows while preserving short legal chains.

**Obstruction check.** Bounded local signatures: Fox words can have formula-scale degree, not bounded-view signatures. Marginal/tableau: no wire tables. Local-view hierarchies: fundamental-cycle rows see the complete dependency. Phase lifts: outside the stated theorem because the representation is graph-dependent, nonabelian, and not a copy-stable scalar phase. Integer exact fibers: binary. Complete-assignment fingerprints: one block per cell/generator. Tensor amplification: none; all mixed twisted chains must be enumerated. Exact transfer: applies directly.

**Falsification.** A legal instance has nontrivial twisted holonomy, or an affine-closure illegal cover is a short twisted boundary.  
**Experiment.** Build Fox matrices for the twisted cycle, all-eight, and twenty affine-closure fixtures; enumerate all pointed words and compare rank/baseline.  
**Likely death.** Linearized twisted homology still closes under odd sums of legal fillings.

6. **Witness-oblivious spectral quadratic metric**  
**Core trick.** Keep integer exact-cover coefficients but replace the identity coefficient metric by \(Q=B^\top B\), where \(B=p(L_{\mathrm{conf}})\) is a fixed integer polynomial of the triple-incompatibility Laplacian. The intended spectral separation is that matching indicators occupy controlled bands, whereas signed odd covers excite many high-frequency coordinates.  
**Expected move.** Produce a direct polynomial Euclidean gap without tensoring or instance-specific optimization over NO witnesses.

**Obstruction check.** Bounded local signatures: column relations survive, but their Euclidean cost need not; this is genuinely global norm coupling. Marginal/tableau: no interfaces. Local-view hierarchies: \(p(L)\) is graph-global. Phase lifts: none. Integer exact fibers: outside its stated local-count norm model only if spectral energy blocks constant repairs. Complete-assignment fingerprints: polynomial triple dictionary. Tensor amplification: none; test every signed fiber vector. Exact transfer: unavailable unless a binary support analogue is subsequently proved.

**Falsification.** A signed repair lies in a low spectral band, worst YES exceeds best NO, or rank/baseline erases the gain.  
**Experiment.** Precommit \(p(t)=1+t+t^2\) and \(1+t^2\); enumerate \([-2,2]^m\) on \(q=3\) YES/NO, all-eight, and holonomy instances using the explicit basis \([B;MA]\).  
**Likely death.** Matchings are not spectrally uniform, so their baseline inflates faster than soundness.
