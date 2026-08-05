I did not search for or use the prohibited document or any discussion of it.

1. **Unique-neighbor code with unreplicated anchors**

**Mechanism.** Lift each clause label to systematic and edge-product symbols on a constant-degree unique-neighbor expander. Honest assignments become equal-norm \(\{\pm1\}\)-codewords; repeat only the inhomogeneous syndrome rows \(W\) times, not the anchors, so DROP pays \(\Omega(W)\) per failed normalization.

**Expected move.** Prove a sparse/dense dichotomy: sparse signed deviations trigger many unique checks, while dense deviations pay polynomial anchor energy.

**Falsification.** A low-anchor exact codeword outside the honest set, especially an affine combination of honest lifts.

**Smallest experiment.** Lift the 72-selector obstruction using a 3-regular graph, set \(W=16\), and exactly enumerate the shell through twice the control radius.

**Map audit.** G1,G7: no slack/radix; exact code kernels remain fatal. G2–5: no private fixed marginals. G6: emit every row and test mod 2. G9,11–15: edge products lie outside raw moments/tags/pair/laminar systems, but an honest-affine lift kills this. G19: no flow. G28,30,32,37: one global code, not min-plus/tensor/additive-copy/orthogonal composition. G31 is only a benchmark. G33–34: equal norm comes from signs, not exterior cospheres. G38: unreplicated anchors repair its additive DROP unless zero has exact syndrome.

2. **Arithmetic-resultant height barrier**

**Mechanism.** Form a bounded-degree Macaulay/toric linearization of Boolean and clause polynomials, but seek a Smith invariant rather than outright linear inconsistency. The desired arithmetic Nullstellensatz certificate forces every NO pseudoevaluation solving the emitted congruences to have a coefficient divisible by a large resultant, whereas a satisfying evaluation has coefficients \(0/1\).

**Expected move.** Convert a growing invariant factor \(D\) into NO distance \(\Omega(D)\) with polynomial matrix size.

**Falsification.** Unit Smith factors, a short syzygy, or superpolynomial monomial count.

**Smallest experiment.** For the eight-clause three-variable core and its control, build degree-3 through degree-6 Macaulay matrices, compute exact SNF, and solve the shortest integral preimage problem.

**Map audit.** G1,G7: no slack spreading or radix; exact syzygies are the analogous killer. G2–5: certificate is global, not local isolation. G6: all equations are lattice rows; SNF includes every modulus. G9,11–15: this uses divisibility/height, not low-degree metric comparison, tags, or bags; affine pseudomoments may still yield unit factors. G19: no flow. G28,30,32,37: no copy composition. G31 supplies only a finite comparator. G33–34: no sphere fitting. G38: repeated resultant rows penalize DROP, but only if the invariant survives. Most likely death: known proof-complexity degree growth makes the matrix exponential.

3. **High-dimensional systolic filling**

**Mechanism.** Replace branching-program paths by integral \(2\)- or \(3\)-chains in a bounded-degree cosystolic expander. A satisfying assignment is a small prescribed-boundary filling; unsatisfiability should force either nonzero syndrome on many cells or a homologous filling whose integral support is polynomially larger.

**Expected move.** Establish a surface/volume inequality \( \|z_{\mathrm{NO}}\|_2^2\ge N^{1+\delta}\) while an honest filling costs \(O(N)\).

**Falsification.** A bounded-support signed cycle that changes the accepting boundary, the higher-dimensional analogue of signed splicing.

**Smallest experiment.** Decorate a 2-dimensional complex with the nine-clause instance and use exact ILP to find minimum integral fillings for control and obstruction.

**Map audit.** G1,G7: no slack or radix. G2–5: overlap is enforced by global boundary operators, not private marginals. G6: boundary and target are fully emitted. G9,11–15: topology replaces moment, affine-code, pair-bag, and hierarchy assumptions; affine chains remain dangerous. G19 is directly relevant: its 1-dimensional signed flow fails, so the experiment must show genuine higher-dimensional systole blocks the two-negative splice. G28,30,32,37: one complex, not additive recursion or tensoring. G31 is unrelated finite geometry. G33–34: no exterior tags. G38: zero chain violates a macroscopic prescribed boundary, avoiding additive DROP if the boundary expands. Likely death: formula decoration destroys cosystolic expansion or admits tiny torsion cycles.

4. **Logarithmic cover-free bags with weighted anchors**

**Mechanism.** Use a deterministic cover-free family of \(O(\log n)\)-clause bags; each bag has polynomially many joint assignments. Downweight duplicated selector anchors by the bag replication factor while scaling inhomogeneous normalization and overlap rows polynomially, so honest radius remains \(O(n)\) but DROP is polynomially expensive.

**Expected move.** Cover-free isolation handles attacks supported on at most \(n^\delta\) bags; larger attacks incur \(n^\delta\) anchor excess.

**Falsification.** Any exact zero-residual affine pseudodistribution, or a medium-density attack beating both sides of the dichotomy.

**Smallest experiment.** Replace G38’s twelve triples by all selected 4/5-clause bags, use anchor weight \(1/r\) and residual weights \(25r^2\), then run exact shell DP on the same obstruction/control.

**Map audit.** G1,G7: no slack/radix. G2–5: complete joint bags, not private local rows. G6: weights and checks are emitted. G9,11–13: not raw moment/tag/code hashing, although the G13 affine lift is the primary test. G14–15: logarithmic cover-free bags and asymmetric weights differ from fixed pairs/frozen laminar trees, but zero-residual lifts still kill. G19: no flow. G28,30,32,37: no additive copy rule. G31 is merely the target ratio. G33–34: no exterior metric. G38 is directly mutated: logarithmic bags replace full-variable triples, and weighted inhomogeneous rows remove \(B+25k\) DROP. Likely death: cheap large coefficients exploit downweighted anchors.

5. **Deep-hole assignment shell**

**Mechanism.** Search for a polynomial-dimensional lattice coset whose deep hole has exponentially many nearest vectors indexed by Boolean assignments, but whose next shell is polynomially farther. Append formula rows that vanish on satisfying nearest vectors; robust shell separation makes every non-Boolean coefficient vector expensive before clause soundness is considered.

**Expected move.** Reduce Booleanity to a geometric theorem: nearest vectors are exactly assignments and the second-shell ratio is \(N^c\).

**Falsification.** A packing bound forcing the second shell within \(1+O(1/N)\), or an unintended nearest vector.

**Smallest experiment.** Enumerate small Construction-A lattices from binary \([m,k]\) codes, locate cosets with \(2^k\) equidistant nearest vectors, and measure the exact second-shell ratio for \(k\le6\).

**Map audit.** G1,G7: no slack or residual radix. G2–5: Booleanity is global Voronoi geometry, not affine isolation. G6: enumerate the unrestricted coset, including modular bypasses. G9,11–15: no raw moment/hash/bag hierarchy; affine combinations matter only if they remain in the first shell. G19: no flow. G28,30,32,37: no recursive or additive amplification. G31 is directly relevant but insufficient: this demands a theorem about the next shell, not merely equal-radius Walsh energy. G33–34: no fitted exterior tags. G38: zero is outside the nearest shell and should pay the deep-hole gap. Most likely death: geometry-of-numbers bounds prohibit a polynomial shell ratio with exponentially many nearest points.

6. **Truncated Magnus signatures for noncommutative consistency**

**Mechanism.** Compile assignment consistency into words over two fixed noncommuting generators, then map words to their degree-\(d\) truncated Magnus expansions. With \(d=\Theta(\log n)\), the signature has polynomial dimension; large free-group girth could force any false or spliced computation to expose a low-degree noncommutative monomial.

**Expected move.** Prove that an accepting signed combination either is an honest word or has polynomially many nonzero signature coordinates.

**Falsification.** A short integral linear combination of rejecting words with the accepting truncated signature.

**Smallest experiment.** Compile the four-variable obstruction to a short balanced word, compute degree \(d=2,3,4\) signatures, and use SNF/MILP to find the minimum signed accepting collision.

**Map audit.** G1,G7: no slack/radix; exact signature collisions are fatal. G2–5: overlap is encoded by word order, not fixed marginals. G6: every signature coordinate must be emitted and audited modulo small primes. G9,11–15: noncommutative monomials fall outside commutative moments, raw hashes, tags, and bags; affine word mixtures may nevertheless collide. G19 is directly relevant, but Magnus coordinates add ordered-product information absent from unit flow; signed splicing remains the main threat. G28,30,32,37: no min-plus, tensor, or additive-copy assumption. G31 is only a baseline. G33–34: no bivector cosphere. G38: the empty word must violate repeated endpoint signatures, so DROP is nonadditive. Likely death: truncation admits low-degree cancellations or transition linearization recreates G19.

**Classical pointers:** Sipser–Spielman, *Expander Codes* (1996); Macaulay’s elimination theory (1902); Lubotzky–Samuels–Vishne on explicit Ramanujan complexes (2005); Delaunay’s Voronoi theory (1924); Magnus’s classical free-group embedding (1939).
