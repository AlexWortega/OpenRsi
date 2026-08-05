1. **Color-coded squarefree collision lift**

**Core trick / expected move.** Mutate I27 by first reducing to bounded-occurrence 3DM, then replace unrestricted nonbacktracking walks by color-coded *simple collision forests*. For every conflicting pair \((u,v)\), explicit splitters index squarefree degree-\(r\) products such as \(x_ux_v\prod_{w\in P}(1+x_w)\); matchings pay zero, while a collision should survive in many channels, potentially giving \(\Delta^{\Theta(\log q)}\) soundness with polynomial output.

**Obstruction check.** Bounded local signatures: outside only when \(r\) grows logarithmically. Marginals/tableaus: no wire interfaces. Local-view hierarchies: global disconnected splitter scopes, but logarithmic-scope attacks remain relevant. Phase lifts: no phases. Integer exact fibers: binary nonlinear lift, not count slacks. Complete fingerprints: polynomial sparse triple dictionary, not assignment columns. Tensor amplification: no tensor coordinates. Exact transfer: applies once the lifted binary syndrome is explicit. All-eight, odd holonomy, every mixed lifted word, and rank/baseline remain mandatory attacks.

**Smallest experiment.** Extend I27’s verifier at \(q=2,3\) with all squarefree forests of sizes \(2,3,4\), canonical color splitters, and exact span enumeration.

**Falsification.** Any hostile mixed word with zero shell, or output exponent below the base.

**Likely death.** Affine XORs of legal lifts still cancel every collision channel.

---

2. **Unique-factorization divisor fingerprint**

**Core trick / expected move.** Assign each ground element a distinct irreducible polynomial \(p_v(Y)\), and each triple \(e\) the product \(g_e=\prod_{v\in e}p_v\). A matching has global product \(\prod_v p_v\), whereas an odd cover has some prime exponent \(3,5,\ldots\); Reed–Solomon evaluations of logarithmic derivatives or product residues could turn that divisor discrepancy into many nonzero coordinates.

**Obstruction check.** Bounded signatures: the product has degree growing with the whole witness, so outside. Marginals/tableaus: outside only if represented directly; a product-tree tableau is covered and unsafe. Local hierarchies: genuinely global divisor identity. Phase lifts: no phases. Integer exact fibers: nonlinear multiplicative validity, outside its affine premise. Complete fingerprints: **not outside** if one creates a column for every fiber point; that implementation is already suspect. Tensor amplification: none. Exact transfer: conditional on a polynomial-size binary linearization. UFD detects all-eight and holonomy semantically, but mixed-span soundness and rank accounting are unresolved.

**Smallest experiment.** For all \(q=2\) dictionaries, enumerate the fiber, evaluate divisor fingerprints at 8–16 field points, span the lifted vectors, and measure hostile mixed distances.

**Falsification.** A zero-fingerprint illegal mixed word.

**Likely death.** Polynomial-size linearization either enumerates witnesses or becomes a killed bounded-fan-in tableau.

---

3. **Affine-coset cocircuit shortening**

**Core trick / expected move.** Replace kernel-aware polar shortening by a target-aware matroid construction. From \((H,t)\), compute the augmented binary matroid of \([H\mid t]\); for each canonical fundamental cocircuit separating \(t\) from a coordinate span, retain a block of dense parity measurements supported on that cocircuit. The hope is that short YES representatives cross few blocks while every NO word crosses many, without discovering a nearest witness.

**Obstruction check.** Bounded signatures: dense maps act on the global affine fiber, not local views. Marginals/tableaus and local hierarchies: no scopes or interfaces. Phase lifts: no phases. Integer exact fibers: binary coset geometry, outside. Complete fingerprints: uses polynomially many coordinates, not assignments. Tensor amplification: it may compress a tensor stage, but is neither puncturing nor type merging; arbitrary mixed words must still be checked. Exact transfer: immediate for the resulting \((H',t')\). Target-aware separation prevents Gen-8’s kernel-only mistake, but not all-eight or holonomy collapse.

**Smallest experiment.** On the existing 64-coordinate reduced squares, enumerate all fundamental cocircuits of the canonical augmented matroid, stack blocks greedily by a precommitted rank budget, then exhaust every mixed word.

**Falsification.** Any pointed kernel, or best NO \(\le\) worst YES.

**Likely death.** Cocircuit crossing measures nonzeroness rather than Hamming distance and again inflates YES more than NO.

---

4. **Nonabelian holonomy dictionary**

**Core trick / expected move.** Assign triples formula-dependent permutations or small matrices so the canonically ordered product of every perfect matching is the identity, while an inconsistent odd cover has nontrivial nonabelian holonomy. Concatenate several low-dimensional residual representations and expand their matrix coefficients into binary coordinates; noncommutativity may prevent the rectangle cancellations that killed scalar phases.

**Obstruction check.** Bounded signatures: global ordered products have unbounded degree. Marginals/tableaus: outside unless multiplication is circuit-linearized, which would re-enter the obstruction. Local-view hierarchies: directly targets global holonomy. Phase lifts: outside its single-valued abelian/coboundary assumptions because selectors are graph-dependent and nonabelian. Integer exact fibers: no affine slack repair. Complete fingerprints: sparse triple labels, not assignment columns. Tensor amplification: none. Exact transfer: conditional on a binary linear image. All-eight and arbitrary mixed representation words are decisive; YES label construction and output rank must be polynomial.

**Smallest experiment.** For all \(q=2\) and selected \(q=3\) dictionaries, SAT-search labels in \(S_3\) or \(S_4\) satisfying all matching relations, then test every illegal cover and every mixed regular-representation word.

**Falsification.** An illegal cover lies in the normal closure of matching relations or has identity image in every tested representation.

**Likely death.** Universal completeness forces a nonabelian analogue of coboundary triviality.

---

5. **Splitter-isolated protected witness sectors**

**Core trick / expected move.** Use an explicit family of edge colorings and weight functions so every \(q\)-edge matching is injectively colored in at least one sector. In that sector, a BCH/Sidon checksum protects the matching’s color-ordered support; sectors are combined through one global selector rather than quotienting all legal witnesses together, so odd affine combinations should not inherit a cheap legal class.

**Obstruction check.** Bounded signatures: sector checks are global high-degree checksums. Marginals/tableaus: the selector must be direct; a selector circuit is covered. Local hierarchies: no proper-scope consistency. Phase lifts: formula-dependent multivalued selectors lie outside the theorem. Integer exact fibers: outside only if selection has zero baseline; ordinary selector variables re-enter its repair problem. Complete fingerprints: sectors index hash signatures, not complete assignments, provided their number is polynomial. Tensor amplification: none. Exact transfer: applies after binary realization. All-eight tests sector splicing; odd holonomy tests incompatible sector choices; mixed words and total sector count are essential.

**Smallest experiment.** At \(q=3,m=8\), enumerate all affine hash maps into 5–7 colors, assign frozen BCH checksums, and construct one protected block per realized color signature.

**Falsification.** Three legal sectors XOR to a cheap illegal word, or sector count already grows exponentially.

**Likely death.** Deterministic isolation of arbitrary matching families requires too many sectors, while existential selectors restore rectangle splicing.

---

6. **Convex preconditioning of the integer exact-cover lattice**

**Core trick / expected move.** Choose a rational PSD quadratic form \(Q\), computable from the incidence matrix, that keeps every individual triple direction cheap but magnifies the signed directions responsible for non-Boolean exact covers. Factor \(Q=R^{T}R\) and use \(Rz\) as dense lattice rows; the pointed odd-minor theorem may certify a large NO norm without tensoring or paying projection-table baselines.

**Obstruction check.** Bounded signatures: global dense geometry, not local polynomial signatures. Marginals/tableaus and local hierarchies: absent. Phase lifts: absent. Integer exact fibers: **main unresolved obstruction**—the known constant-cost repairs survive many scalings, and no theorem yet shows a permissible \(Q\) escapes them. Complete fingerprints: sparse triple dictionary only. Tensor amplification: none. Exact transfer: use direct integer CVP; a binary transfer is unnecessary. All-eight and holonomy are covered only by optimizing against their signed exact fibers; mixed tensors are irrelevant. YES baseline and row rank are explicit SDP constraints.

**Smallest experiment.** For the existing \(q=3\) YES/NO instances, enumerate signed exact-fiber vectors in \([-2,2]^m\) and solve an SDP maximizing minimum NO \(z^TQz\), subject to \(e_j^TQe_j\le1\) and a fixed trace/rank budget.

**Falsification.** Optimum NO/YES ratio stays constant or requires witness-dependent constraints.

**Likely death.** Universal completeness bounds force every illegal affine combination to remain within a constant factor.
