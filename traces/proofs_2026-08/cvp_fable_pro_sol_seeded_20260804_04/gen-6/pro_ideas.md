O1–O8 below denote: bounded local signatures; marginal/tableau encodings; local-view hierarchies; phase lifts; integer exact fibers; complete-assignment fingerprints; tensor amplification; exact syndrome-to-CVP transfer.

1. **Formula-derived Euclidean metric synthesis**

**Core trick.** Replace the fixed coefficient norm in integer 3DM-CVP by \(\|R_Az\|_2^2\), where \(R_A\) is a polynomial-row, dictionary-dependent matrix built from global spectral projectors of the triple-incompatibility graph. Search for a canonical family where every matching has \(O(q)\) energy but every signed NO fiber has \(q^{1+\epsilon}\) energy.

**Expected move.** Obtain a direct polynomial CVP gap without tensoring.

**Map check.** O1: outside only if columns depend globally on \(A\), not a bounded-degree local view. O2: no marginals/tableau. O3: no scope hierarchy. O4: no phases. O5: outside its stated local-norm assumption, but constant signed repairs may still have low spectral energy. O6: only \(m\) triple columns. O7: no tensor/mixed-word issue. O8: unavailable—this is direct integer CVP, so it misses the desired NCP-first route.

**Smallest experiment.** On all-eight and existing \(q=3\) YES/NO/holonomy fibers, solve an SDP for \(Q=R^\top R\succeq0\), enforcing completeness and maximizing minimum signed-NO energy; then restrict \(Q\) to adjacency-algebra matrices.

**Falsification.** Every feasible \(Q\) gives an affine-closure illegal cover energy at most the worst matching energy, or requires superpolynomial rank/bit size.

---

2. **Two-sided rank-condenser fold**

**Core trick.** Reshape every reduced tensor word as a matrix \(W\), then output binary expansions of \(A_iWB_i\) for an explicit extension-field rank-condenser family. Unlike puncturing, each output coordinate is a dense, code-dependent linear combination; condenser blocks might preserve many independent slices of every mixed NO word while a rank-one YES square remains sparse.

**Expected move.** Compress \(m^2\) tensor coordinates to \(m^{1+o(1)}\) while retaining a powered distance ratio.

**Map check.** O1: not a local signature map. O2–O5: no marginals, scopes, phases, or integer repairs. O6: operates on the sparse code, not assignments. O7: exactly its surviving code-dependent dense-fold exception; arbitrary mixed \(W\) must be covered. O8: applies after binary expansion, with output rank explicitly counted.

**Smallest experiment.** Over \(\mathbb F_{2^3}\), instantiate Vandermonde left/right condensers for the existing \(8\times8\) reduced squares. Enumerate every mixed image word for ten YES, 200 NO, all-eight, affine-closure, and holonomy cases.

**Falsification.** A rank-one NO pure tensor or low-slice-rank mixed word folds below worst YES, or the number of blocks needed for soundness is \(\Omega(m^2)\).

---

3. **Color-coded simple collision complexes**

**Core trick.** Mutate Schur walks by retaining only rainbow, self-avoiding collision paths and cycles selected by deterministic \(k\)-perfect hash families. Exterior signs suppress repeated traversal, so amplification must come from genuinely distinct collision structures rather than replicating one constant cycle.

**Expected move.** Under bounded incompatibility degree, \(k=\Theta(\log q)\) gives polynomial output while a NO cover with expanding collision support activates \(q^{\Omega(1)}\) features; matchings activate none.

**Map check.** O1: still applies wherever a \((k+1)\)-cube exists, so this route is not automatically safe; global rainbow restrictions must destroy that cube. O2: no affine marginals. O3: growing, disconnected logarithmic scopes lie outside the proved fixed-level result, though holonomy remains hostile. O4: no phases. O5: binary nonlinear lift, not an affine integer repair. O6: no complete assignments. O7: not tensoring, but every mixed lifted word must be tested. O8: applies to the resulting binary image.

**Smallest experiment.** Replace walks in I27 by color-coded simple paths/cycles of lengths \(3\)–\(6\); exactly enumerate the lifted span on all-eight, twisted holonomy, and the 200 NO suite.

**Falsification.** Existing illegal affine words cancel every rainbow feature, or polynomial output requires an unavailable bounded-degree preprocessing theorem.

---

4. **Nonabelian Fourier multi-irrep fold**

**Core trick.** Assign triples to full-rank elements of an explicit nonabelian group and map ordered tensor coordinate \((i,j)\) to all selected matrix coefficients of \(\rho(g_i^{-1}g_j)\). Using several irreducible representations replaces Generation 5’s aligned rank-one labels; quasirandomness and Fourier uncertainty could force sparse mixed coefficient matrices to have broad images.

**Expected move.** A growing \(\mathrm{PSL}_2(2^s)\)-type family might compress ordered pairs by a polynomial factor without transpose collapse or zero products.

**Map check.** O1: not a bounded-degree Boolean-view signature, although local affine trades may survive the fold. O2–O5: no marginals, scopes, phases, or integer fibers. O6: polynomial triple labels, not assignments. O7: a code-dependent dense structured fold, outside the puncturing no-go; arbitrary mixed words remain mandatory. O8: applies after fixed-basis binary expansion.

**Smallest experiment.** Use all irreducible matrix representations of \(S_3\) or \(A_5\) over a small characteristic-two extension; freeze a canonical incidence-derived labeling and rerun the complete hostile suite.

**Falsification.** A group-algebra convolution kernel gives pointed distance zero, or avoiding collisions requires a noncommutative Sidon set whose size eliminates compression.

---

5. **Formula-dependent voltage cover**

**Core trick.** Construct a polynomial-sheet voltage lift of the triple-incompatibility graph, with voltages chosen from a canonical global cycle basis. Matchings contain no incompatibility edges and therefore lift freely, while illegal covers containing charged cycles should require many sheets or fail exact consistency.

**Expected move.** Turn odd permutation holonomy into a global group obstruction while avoiding copy-stable local phases; compose with an expander quotient so each charged component incurs polynomial support.

**Map check.** O1: local forest trades may still lift unchanged, so not fully outside it. O2: interfaces are not proper marginals. O3: the selector uses the complete graph cycle space, outside proper connected scopes. O4: specifically outside its graph-independent/copy-stable hypothesis. O5: binary lift, no integer slack. O6: \(m|G|\) columns, not assignments. O7: no tensor; mixed lifted words still need enumeration. O8: applies if \(|G|\) and syndrome rank remain polynomial.

**Smallest experiment.** Use \(G=S_3\) on all-eight and twisted \(q=3\) dictionaries; assign voltages from a canonical spanning tree and enumerate all lifted affine words for \(|G|=6\).

**Falsification.** A forest-shaped odd cover lifts cheaply, or rectangle superpositions splice different sheets and recreate the weight-\(O(q)\) attack.

---

6. **Higher Lawrence lifting and Graver complexity**

**Core trick.** Replace one exact-cover fiber by a higher Lawrence configuration: several signed layers share global aggregate variables, and deviations are measured through conformal Graver decompositions. Some toric families exhibit rapidly growing Graver complexity despite only linear growth in the number of layers; the hope is that illegal covers require many conformal atoms while a matching uses one diagonal atom.

**Expected move.** Amplify integrality defect through algebraic-statistical complexity rather than tensor-product rank.

**Map check.** O1: triple columns are global incidence objects, not clause-view signatures. O2–O4: no marginals, local scopes, or phases. O5: **not outside it as stated**—Lawrence constraints remain affine, so constant exact-fiber repairs are a direct threat unless conformal complexity affects the actual norm. O6: sparse triple dictionary. O7: no ordinary tensor, though layers may merely reproduce its parameter wall. O8: possible only after a binary formulation; integer Lawrence CVP alone does not invoke it.

**Smallest experiment.** Build second and third Lawrence liftings of the existing \(q=3\) matrices; enumerate coefficients in \([-2,2]\), compute exact minima and primitive Graver moves, including all-eight and holonomy.

**Falsification.** The norm gap is exactly additive in the layer count, or one base signed repair embeds diagonally with constant excess.

---

7. **Sparse Macaulay boundary code after expander substitution**

**Core trick.** XORify a bounded-occurrence 3CNF through an explicit expander, then form a sparse Macaulay matrix whose columns are only connected or splitter-selected monomials up to degree \(d=\Theta(\log n)\). Interpret multiplication by clauses as a global boundary operator; a satisfying assignment supplies a sparse evaluation chain, while expansion is hoped to force every inconsistent target filling to use polynomially many monomials.

**Expected move.** Convert proof-complexity degree/expansion into syndrome coset weight without invoking a PCP theorem.

**Map check.** O1: degree grows logarithmically, but any larger independent cube still triggers the theorem; sparse domain geometry must prevent it. O2: no truth-table marginals. O3: connected monomials alone fall within its danger zone; splitter-selected nonlocal monomials are intended to escape it. O4: no phases. O5: binary polynomial boundary, not integer slack. O6: monomial dictionary is polynomial only if bounded degree and sparse reachability hold. O7: no tensor. O8: applies directly to the resulting binary syndrome system.

**Smallest experiment.** Build degree \(2\)–\(5\) sparse Macaulay codes for all-eight, twisted-cycle, and Petersen-flow formulas; enumerate every coset word and track column growth.

**Falsification.** Cube pseudoassignments remain sparse boundaries, or degree \(\Theta(\log n)\) already creates quasipolynomially many reachable monomials.
