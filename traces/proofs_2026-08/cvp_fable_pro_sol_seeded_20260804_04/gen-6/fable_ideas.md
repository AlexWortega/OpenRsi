### 1. High-degree global collision-OR lift

**Core trick.** For the 3DM incompatibility graph, choose a polynomial-size deterministic separating family of large edge sets \(B_a\), and add global features  
\[
P_a(x)=1+\prod_{e=\{i,j\}\in B_a}(1+x_ix_j).
\]
Every matching has \(P_a=0\); a collision should activate many separating buckets. Construct the binary lift from the ANF coefficient matrix of \(x=x_0+Gu\).

**Expected move.** Preserve YES weight \(q\) while charging each NO word in \(\Omega(q^\epsilon)\) global coordinates.

**Obstruction check.** **Bounded local signatures:** outside if buckets have degree \(\Theta(q)\). **Marginal/tableau encodings:** no interfaces or gate tables, unless ANF construction is circuitized. **Local-view hierarchies:** buckets are formula-global. **Phase lifts:** no phases. **Integer exact fibers:** binary nonlinear lift, not affine slack. **Complete-assignment fingerprints:** polynomial features, not assignment columns. **Tensor amplification:** no tensor; soundness must cover every mixed lifted word. **Exact transfer:** applies at lift rank, which must remain polynomial.

**Falsification.** A pointed kernel or NO distance no larger than worst YES.

**Smallest experiment.** Enumerate lifted spans for all-eight, twisted holonomy, and the existing \(q=3\) suite using 16–64 frozen buckets.

**Likely death.** Expanding the high-degree features may require exponentially many ANF generator rows, or mixed words cancel all buckets.

---

### 2. Rank-condenser folding of mixed tensor matrices

**Core trick.** Reshape a reduced tensor word as a matrix \(W\), derive canonical subspaces from the instance parity check, and fold by  
\[
F(W)=\bigoplus_s \operatorname{bin}(P_sWQ_s),
\]
where \(P_s,Q_s\) are explicit folded-Wronskian/rank-condenser maps over an extension field. Unlike puncturing, this is a dense, asymmetric, code-dependent linear operation.

**Expected move.** Keep planted rank-one YES squares sparse in a few blocks while forcing every NO mixed matrix to retain rank—and hence support—in many blocks.

**Obstruction check.** **Bounded local signatures, marginal/tableau encodings, local-view hierarchies, phase lifts, integer exact fibers, complete-assignment fingerprints:** inapplicable; the map acts globally on the tensor code. **Tensor amplification:** directly occupies its unexcluded code-dependent dense-fold opening and must handle arbitrary mixed \(W\). **Exact transfer:** applies after binary expansion; output rank is \(\sum_s\dim(P_s)\dim(Q_s)[\mathbb F:\mathbb F_2]\).

**Falsification.** Any hostile NO image of weight at most worst YES, or no exponent gain after rank accounting.

**Smallest experiment.** Exhaustively test all \(2^{k^2}\) mixed words of reduced \(q=3,m=8\) squares, including all-eight and holonomy, for frozen \(2\times4\) and \(3\times4\) condenser families.

**Likely death.** Rank preservation does not imply Hamming support, while rank-one YES images may be dense.

---

### 3. Permutahedral Voronoi selector

**Core trick.** Replace the costly variable permutation tables by one polynomial-rank lattice whose nearest-point set at a fixed target realizes all permutation matrices simultaneously. Search within \(S_q\times S_q\)-invariant quadratic forms on the row/column-sum-one lattice, using type-\(A\) root/weight lattices and permutahedral Voronoi geometry.

**Expected move.** Encode the \((q!)^2\) projection-target disjunction with \(O(q^2)\) rank and \(O(1)\) selector baseline, while signed nonpermutations pay \(q^\epsilon\).

**Obstruction check.** **Bounded local signatures:** no Boolean signature map. **Marginal/tableau encodings:** no wire interfaces. **Local-view hierarchies:** selector is one global Voronoi condition. **Phase lifts:** irrelevant. **Integer exact fibers:** outside only if separation comes from global Voronoi geometry rather than affine/polynomial slacks. **Complete-assignment fingerprints:** no assignment columns. **Tensor amplification:** unused; signed lattice combinations replace mixed-word analysis. **Exact transfer:** not applicable because this is direct CVP; rank is \(O(q^2)\).

**Falsification.** A signed nonpermutation ties a permutation, or the nearest-permutation distance is already \(\Omega(q)\).

**Smallest experiment.** For \(q=3\), enumerate row/column-sum-one tables in \([-2,2]^9\) while searching small invariant Gram coefficients; then attach the all-eight and holonomy fibers.

**Likely death.** Symmetry leaves too few quadratic eigenspaces, forcing the same linear YES baseline seen in ordinary table norms.

---

### 4. Nonabelian twisted-Laplacian holonomy shell

**Core trick.** Give the constraint graph formula-dependent labels in a small nonabelian group and form a twisted Laplacian  
\[
L_x=\sum_e x_e\,b_eb_e^\top\otimes \rho(g_e).
\]
Lift selected characteristic coefficients or exterior minors of \(L_x\); consistent assignments should gauge-conjugate into a sparse invariant sector, whereas odd holonomy changes many global spectral coordinates.

**Expected move.** Charge twisted cycles globally without using single-valued local phases, including odd permutation holonomy.

**Obstruction check.** **Bounded local signatures:** full characteristic data has growing degree. **Marginal/tableau encodings:** no local state interfaces in the direct minor lift. **Local-view hierarchies:** cycle information is global. **Phase lifts:** outside its copy-stable scalar/coboundary assumptions—labels are graph-dependent, nonabelian, and multirepresentational. **Integer exact fibers:** no affine slack. **Complete-assignment fingerprints:** polynomial spectral coordinates, not assignment groups. **Tensor amplification:** unused; all mixed spectral-lift words require testing. **Exact transfer:** applies after a binary-field realization, with spectral-state rank explicitly counted.

**Falsification.** Any all-eight or holonomy pointed kernel, or a legal lift whose baseline grows like the whole spectral state.

**Smallest experiment.** Use \(S_3\)’s two-dimensional representation on the existing hostile graphs; compute all minors through order three and enumerate the full lifted span.

**Likely death.** Polynomially constructing the lift span may require exponentially many minors; a determinant circuit would re-enter tableau faults.

---

### 5. Zero-baseline orthogonality certificate for projection tables

**Core trick.** For each pair projection \(P(z)\), use the global defect  
\[
Q(P)=P^\top P-I.
\]
An integral row/column-sum-one table satisfies \(Q(P)=0\) exactly when it is a permutation matrix: integral orthogonality makes it signed-permutation, and row sum one fixes the signs. Applying this to all three projections would give YES zero shell cost.

**Expected move.** Replicate \(Q\)-coordinates polynomially so every nonmatching exact fiber pays a multiplicative penalty without adding the \(3q\) table baseline of I18.

**Obstruction check.** **Bounded local signatures:** the quadratic Veronese linearization is covered by its 3-cube relation. **Marginal/tableau encodings:** a gate/tableau implementation is also covered. **Local-view hierarchies:** the predicate itself is global, but its linearization may not be. **Phase lifts:** irrelevant. **Integer exact fibers:** likely covered because validity remains bounded-degree after coupling. **Complete-assignment fingerprints:** only \(O(q^3)\) monomials. **Tensor amplification:** unused; every mixed Veronese word must be checked. **Exact transfer:** applies only if a sound binary linearization exists.

**Falsification.** A constant-cost virtual \(Q=0\) word in the lifted affine span.

**Smallest experiment.** At \(q=3\), enumerate signed \(z\), construct the full quadratic Veronese span, and attack all-eight and holonomy.

**Likely death.** Precisely the bounded-degree cube repair already mapped—useful mainly as a sharp confirmation or clue for a non-linearizable replacement.

---

### 6. Rearrangeable-network congestion shell

**Core trick.** Replace each triple by a polynomial family of whole-path columns through two coupled three-stage routing networks for its \(AB\) and \(AC\) projections. A perfect matching can choose edge-disjoint routes; append expander-coded edge-load parities so a signed odd cover is intended to create many unavoidable congestion coordinates.

**Expected move.** Convert one global collision into \(\Omega(\log q)\) or \(q^\epsilon\) charged edges while keeping YES path cost \(O(q\log q)\), then recurse with fresh networks.

**Obstruction check.** **Bounded local signatures:** whole paths are global columns, but affine route-choice cubes may still satisfy the obstruction. **Marginal/tableau encodings:** outside only if paths are atomic columns; switch-by-switch encoding is covered. **Local-view hierarchies:** routes span the instance, though proper routing scopes may still miss global dependency. **Phase lifts:** no phases. **Integer exact fibers:** binary congestion shell. **Complete-assignment fingerprints:** polynomial route dictionary, not assignments. **Tensor amplification:** unused; arbitrary XORs of route columns are the soundness adversary. **Exact transfer:** applies with rank equal to terminal plus network-edge rows.

**Falsification.** An all-eight or holonomy odd cover admitting collision-free rerouting, or a support-three rectangle splice.

**Smallest experiment.** Use \(q=3\), three middle routers, enumerate all route choices and mixed words for the hostile suite.

**Likely death.** NO covers may reroute as effectively as matchings, while coordinated path choices recreate marginal rectangle kernels.
