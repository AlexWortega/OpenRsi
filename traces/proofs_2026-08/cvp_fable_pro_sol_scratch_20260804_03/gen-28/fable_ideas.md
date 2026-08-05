## Generation 28 — divergent mechanisms, unranked

### 1. Blockwise Voronoi retraction

**Mechanism.** Search for a rational positive-definite block metric admitting a global, non-coordinate retraction from every relevant integer point onto a Boolean representative, with a large quantitative penalty for malformed blocks. Scale clause residuals by \(M=N^K\); a rounding theorem would then convert every short vector into a Boolean assignment without increasing distance.

**Expected move.** Completeness stays \(O(\sqrt N)\), while unsatisfiability or failed retraction costs \(\Omega(M)\).

**Obstruction audit.** G1: no free slack. G2–3/G5: uses global blocks, not composed local isolation. G6: all coordinates and targets emitted. G7/G9/G11/G13/G15/G19: not outside—the retraction inequalities must explicitly cover those signed states. G12: DROP is a separate block class. G14: no inference from its finite pass. G20–22: require a symbolic \(M\)-scaling and complete shell proof. G27: avoids universal coordinate clipping, plain tensors, holonomy, Lawrence layers, moments, and homology; unlike the killed M-matrix route, retraction is blockwise and only claimed after an eigenvalue-derived bound.

**Falsification.** Any G13/G19-type point whose retraction increases objective.

**Smallest experiment.** SDP-search \(Q\) on the eight-clause three-variable obstruction, rationalize \(Q\), then exhaust the eigenvalue-bounded integer shell.

**Likely death.** No coupled quadratic form supports the required retraction.

---

### 2. Salted Plücker-chart amplifier

**Mechanism.** Encode legal assignment fragments as decomposable exterior tensors, represented by selectors for several overlapping Plücker charts with unimodular transition maps. Recursively combine differently salted charts; illegal signed mixtures should acquire many nonzero minors, whereas legal decomposable points retain one chart representative per level.

**Expected move.** A compound-matrix inequality could make illegal energy grow as \(D^t\) against legal growth \(W^t\), with \(D/W>1\).

**Obstruction audit.** G1: no slack. G2–3/G5: overlap uses full chart transitions, not freed marginals. G6: chart variables and transitions are lattice coordinates. G7/G9/G11: zero linear residual need not imply zero minors. G12: missing charts violate normalization. G13/G15: affine lifts generally cease to be decomposable, but this must be verified. G14: supplies no theorem. G19: signed fake charts remain possible. G20–22: need a recursive compound inequality and exhaustive port alphabet. G27: salted alternating factors differ from the killed plain tensor square and its \(\operatorname{diag}(s)\) shortcut; no clipping, fixed-group holonomy, Lawrence layering, moments, or homology is used. Entangled shortcuts are not ruled out.

**Falsification.** A consistent signed chart system with all Plücker residuals zero and constant excess.

**Smallest experiment.** Two salted \(2\)-plane charts over four coordinates; enumerate all coefficients in the exact baseline-plus-32 shell.

**Likely death.** Independent chart selectors fake the quadratic Plücker relations linearly.

---

### 3. Growing nonabelian holonomy

**Mechanism.** Compile assignment consistency into multiplication-table sections over a growing family such as \(\mathrm{PSL}_2(\mathbb F_p)\), and fingerprint holonomy using a high-dimensional unitary representation. Legal sections have identity holonomy; any nonidentity element should move \(\Omega(p)\) matrix coordinates, permitting \(p=N^K\).

**Expected move.** One unavoidable nontrivial holonomy yields distance \(\Omega(\sqrt p)\) while legal bookkeeping remains polynomially smaller.

**Obstruction audit.** G1: no slack. G2–3/G5: constraints are global noncommutative products, not private marginals. G6: every table selector is emitted. G7/G9/G11/G13/G15: abelian affine cancellation does not automatically preserve products, but signed table sections may still do so. G12: dropped tables have normalization cost. G14: irrelevant finite pass. G19: directly threatening—signed multiplication flows must be searched. G20–22: require uniform displacement and complete boundary states. G27: unlike the killed fixed \(S_3\) tensor idea, group and representation dimension grow; no clipping, ordinary tensor powering, Lawrence layers, bounded-degree moments, or linear homology. Property-\(\tau\) alone does not establish the required CVP ratio.

**Falsification.** A zero-holonomy signed section for the obstruction.

**Smallest experiment.** Use \(A_5\) on the nine-clause instance; emit full multiplication selectors and search through anchor excess 24.

**Likely death.** G19-style negative flows splice multiplication tables into identity holonomy.

---

### 4. Self-penalizing redundant carry system

**Mechanism.** Encode each Boolean digit simultaneously in several coprime mixed-radix channels, but make every quotient and carry digit itself a balanced anchored codeword rather than free slack. Choose moduli so the combined residue map is injective throughout the eigenvalue-bounded short-vector shell; amplify every carry disagreement by \(M\).

**Expected move.** A Boolean satisfying encoding has zero carry residual, while any false or malformed encoding must expose a carry in at least one channel and pay \(M\).

**Obstruction audit.** G1: specifically addresses its free-slack cause; unlike the killed multi-prime variant, carries are amplified too. G2–3/G5: no local-isolation composition. G6: carries are unrestricted emitted variables. G7: exact signed zero-carry kernels remain possible, so not outside. G9/G11/G13/G15: selector affine collisions are absent syntactically but may reappear as digit trades. G12: DROP changes redundant normalizations. G14: unused. G19: signed automaton splicing must be included. G20–22: need polynomial moduli, shell injectivity, and full carry-state closure. G27: no clipping, tensoring, holonomy, Lawrence layers, low-degree moments, or homology; ports are explicit carry vectors.

**Falsification.** Any non-Boolean zero-carry vector inside the completeness-scaled shell.

**Smallest experiment.** All-eight-clauses formula with bases \(5,7,11\); enumerate every digit and carry coefficient allowed by the spectral bound.

**Likely death.** A coherent signed carry cycle vanishes simultaneously in every channel.

---

### 5. State-complete tropical tile recursion

**Mechanism.** Turn the G14 pair-bag construction into a fully specified tile with a finite port alphabet containing every eigenvalue-bounded coefficient vector, including legal, DROP, malformed, G13, and G19 states. Exact minimization defines a min-plus transfer matrix; depth increases scales only if illegal-to-illegal transfer has a strictly larger tropical growth rate than legal transfer.

**Expected move.** A proved \(\lambda>\mu\) recurrence would yield relative growth \((\lambda/\mu)^{d/2}\) at logarithmic depth.

**Obstruction audit.** G1: no slack. G2–3/G5: all freed boundary marginals become ports. G6: fixed target and glue rows are emitted. G7/G9/G11/G13/G15/G19: each attack is an explicit state class, not assumed absent. G12: DROP included. G14: used only as the frozen base tile, not as a composition theorem. G20–21: exactly the proposed tropical-rate test. G22: closure is exhaustive rather than radius-circular. G27: this implements its demanded repair—fixed lattice, control, ports, glue, coefficient bound, and recurrence; it uses no clipping, tensor norm claim, holonomy, Lawrence layering, moments, or homology.

**Falsification.** Nonclosure, an unlisted minimizer, or \(\lambda\le\mu\).

**Smallest experiment.** Canonicalize all G14 port fibers through \(B+32\), glue two tiles, and compute the exact transfer matrix.

**Likely death.** A high-cost boundary state cancels during gluing and re-enters cheaply.

---

### 6. Compressed Macaulay-resultant dual witness

**Mechanism.** Arithmetize Booleanity and clause satisfaction as an integral polynomial system and construct a Macaulay resultant map. Try to compress multilinear monomial shifts by Kronecker substitution: satisfiable assignments give short evaluation vectors, while unsatisfiability should provide an integral dual functional separating every evaluation-like vector from the target.

**Expected move.** Scale the dual-functional coordinate by \(M=N^K\); its nonzero integer value supplies a polynomial gap without residual coding.

**Obstruction audit.** G1: no optimized slack, although compression carries could recreate it. G2–3/G5: no marginal-isolation argument. G6: the entire Macaulay map and target must be emitted. G7/G9/G11/G13/G15: selector kernels are outside the representation, but low-degree pseudo-evaluations are analogous and must be searched. G12: zero evaluation vectors are explicit malformed states. G14: unused. G19: no path flow, though signed proof coefficients remain. G20–21: hinge on polynomial-size compression and bounded dual norm. G22: nonrecursive. G27: no clipping, tensoring, holonomy, Lawrence layers, unsupported moment detector, or homology; unlike the killed degree-three proposal, no fixed degree is assumed.

**Falsification.** Exponential Macaulay rank, huge dual norm, or a short pseudo-evaluation annihilating all rows.

**Smallest experiment.** Build the exact multilinear Macaulay matrix for the eight-clause formula through degree three and compare its emitted CVP minimum with a satisfiable control.

**Likely death.** General formulas require exponentially many monomials, and Kronecker compression destroys Euclidean separation.

---

### 7. Integral-trade-expanding nonlinear code

**Mechanism.** Systematically encode assignments with an explicit expander code, but replace linear parity checks by small nonlinear quasigroup constraint tables chosen to have no short integral trades. Emit every local table selector; seek an integer coboundary-expansion theorem saying any mass-one signed pseudocodeword not equal to a codeword violates \(\Omega(m)\) tables.

**Expected move.** Scale table residuals by \(M\); completeness has zero residual, while every malformed or clause-inconsistent state pays \(M\sqrt m\).

**Obstruction audit.** G1: no slack. G2–3/G5: expansion is global and must include overlaps. G6: all checks are emitted, never externally filtered. G7: zero-table signed kernels are the main falsifier. G9/G11: low-degree parity is irrelevant only if the nonlinear tables detect its lift. G12: drops violate incident checks. G13/G15: linear codes would preserve the affine collision; nonlinear trade-freeness is introduced precisely because those obstructions apply. G14: no inherited scaling. G19: signed local-table splicing remains possible. G20–22: require uniform integral expansion and complete local-state closure. G27: no clipping, plain tensor, fixed holonomy, Lawrence layers, moments, or homology; the code must be polynomial-size and not merely a constant-degree refutation.

**Falsification.** A zero-residual signed pseudocodeword with \(O(1)\) negative entries.

**Smallest experiment.** A length-12 degree-3 expander with order-4 quasigroup tables, coupled to the nine-clause obstruction; exact shell search through excess 24.

**Likely death.** Local nonlinear tables still admit G19-style integral trades.

Classical touchstones only: Macaulay’s resultant construction (1902), Lubotzky–Phillips–Sarnak Ramanujan graphs (1988), and Sipser–Spielman expander codes (1996).
