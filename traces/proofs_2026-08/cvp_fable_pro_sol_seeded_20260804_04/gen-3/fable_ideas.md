Below, **O1–O8** denote: bounded local signatures; marginal/tableau encodings; local-view hierarchies; phase lifts; integer exact fibers; complete-assignment fingerprints; tensor amplification; exact syndrome-to-CVP transfer.

### 1. Tropical/valuated-matroid shell

**Mechanism.** Lift each 3DM triple to a column over a discretely valued field so perfect matchings have a unit Plücker coordinate, while illegal odd covers force every selected compound minor to valuation at least \(L\). Embed a sparse family of these valuations into an ideal lattice; the product formula should convert \(L=\Theta(\log N)\) into polynomial Euclidean separation.

**Expected move.** Replace additive integrality cost by a zero-baseline non-Archimedean defect, without tensoring.

**Obstruction check.** O1 bounded signatures: outside only if genuinely high-degree compounds are retained. O2 tableaux and O3 local scopes: no local interfaces. O4 phases: unrelated. O5 exact fibers: outside its polynomial-slack hypothesis, but a linearized valuation gadget may fall back inside. O6 fingerprints: columns remain triples, not assignments. O7 tensors: absent; all signed compound combinations still require checking. O8 transfer: a binary realization and rank accounting remain mandatory.

**Falsification test.** Find an all-eight or odd-holonomy cover sharing the minimum valuation profile of a matching.

**Smallest experiment.** For \(q=2,3\), SAT-search integer heights and selected \(2\times2,3\times3\) minors, then exhaust signed fibers.

**Likely death.** Tropical Plücker relations force a cheap illegal affine combination whenever all matchings are cheap.

---

### 2. Formula-dependent nonabelian voltage lift

**Mechanism.** Put canonical nonabelian voltages on the full formula-incidence graph and let each choice column transport a basis vector through a polynomial-size expander permutation action. A satisfying assignment should define a sparse coherent section, while inconsistent monodromy moves a constant fraction of the action points.

**Expected move.** Turn odd holonomy into \(\Omega(|\Omega|)\) Hamming cost, with \(|\Omega|=N^\varepsilon\), without paying that amount in the YES witness.

**Obstruction check.** O1 bounded signatures: global path-transport columns are outside local-degree assumptions. O2 tableaux and O3 scopes: no proper marginals or scope tables. O4 phase lifts: specifically outside single-valued abelian/copy-stable phases because the selector is graph-dependent and nonabelian. O5 exact fibers: no count slack. O6 fingerprints: polynomial action states, not assignments. O7 tensors: none; mixed representation soundness remains open. O8 transfer applies if the action is compiled to binary syndrome rows; output rank and YES support must be counted.

**Falsification test.** A support-\(O(1)\) mixed word with trivial transported sum on all-eight or twisted holonomy.

**Smallest experiment.** Search \(S_3,A_4\), and small Cayley actions on the existing hostile instances; enumerate every mixed word.

**Likely death.** Universal completeness forces a nonabelian analogue of gauge triviality, or invariant subspaces cancel the holonomy.

---

### 3. Rank-metric protected legal sectors

**Mechanism.** Assign every triple a rank-one matrix \(M_j\) over \(\mathrm{GF}(2^s)\), chosen by a code-dependent rank condenser. Seek an affine shift computable from the instance such that every perfect matching has matrix rank \(O(1)\), but every illegal syndrome solution has rank \(q^\varepsilon\); an MRD/Gabidulin shell then converts rank into Hamming weight.

**Expected move.** Protect different legal witnesses separately rather than quotienting their differences.

**Obstruction check.** O1 bounded signatures actually applies to the additive matrix map on flippable cubes; only the nonlinear rank objective might escape, so this is exposed. O2 tableaux and O3 scopes: no interfaces or scopes. O4 phases: absent. O5 exact fibers: no integer slack. O6 fingerprints: only triple columns and polynomial matrices. O7 tensors: absent; arbitrary mixed matrix sums are the central test. O8 transfer is direct after binary expansion, with a potentially large \(s\)-factor in rank.

**Falsification test.** Three cheap matching matrices whose XOR is illegal and has rank at most three times the YES rank.

**Smallest experiment.** MILP/SAT-search \(3\times3\) or \(4\times4\) labels for all tiny dictionaries, then exhaust all fibers and affine matching XORs.

**Likely death.** The known illegal affine closure gives constant secant rank, preventing polynomial separation.

---

### 4. Splitter-based witness isolation with protected branches

**Mechanism.** Use a deterministic perfect-hash/splitter family to isolate each short exact cover under at least one weight seed. Instead of identifying all witnesses, place isolated candidates in separately coded sectors and encode the seed selector with a high-distance simplex/BCH layer designed to make odd superpositions of sectors expensive.

**Expected move.** Obtain an implicit canonical witness in one branch without solving SAT, then apply ordinary high-girth protection there.

**Obstruction check.** O1 bounded signatures still attacks linear weight rows inside each branch; escape depends entirely on the protected selector. O2 tableaux: a one-hot selector would fall inside, so it must be a global codeword selector. O3 scopes and O4 phases: unused. O5 exact fibers: integer weight slacks would be covered and are disallowed. O6 fingerprints: seeds index hash functions, not assignments. O7 tensors: none; all mixed sectors must be enumerated. O8 transfer applies after a binary selector construction, including its YES baseline.

**Falsification test.** An illegal odd XOR using three cheap branches, or a near-cover never isolated from matchings by the polynomial seed family.

**Smallest experiment.** Enumerate all tiny covers, generate standard \(k\)-perfect hash families, and optimize a binary sector code by SAT.

**Likely death.** Polynomial isolation of all relevant witnesses is unavailable, or constructing each protected center is itself NP-hard.

---

### 5. Nilpotent noncommutative fingerprint algebra

**Mechanism.** Label triples by elements \(a_j\) of a polynomial-dimensional nilpotent noncommutative algebra and fingerprint a selection by the global ordered product  
\[
P(x)=\prod_j(1+x_j a_j).
\]
Choose the quotient algebra so matching products occupy a sparse affine slice, while illegal covers populate many coefficients; use one global regular-representation block rather than gate-by-gate multiplication.

**Expected move.** Capture high-order interactions with polynomial dimension, exploiting noncommutativity to avoid cube cancellations.

**Obstruction check.** O1 bounded signatures is avoided only if effective degree exceeds every relevant cube dimension; logarithmic nilpotency remains vulnerable. O2 tableaux and O5 exact fibers: outside only with a direct global block—ordinary multiplication circuits re-enter both obstructions. O3 scopes and O4 phases: absent. O6 fingerprints: no complete-assignment columns. O7 tensors: no coordinate tensor power, but every mixed algebra word must be checked. O8 transfer requires a binary linear realization of the product slice and honest rank accounting.

**Falsification test.** Equal algebra products for a matching and an illegal all-eight/holonomy combination, or a low-support mixed coefficient vector in the legal slice.

**Smallest experiment.** Exhaust upper-triangular matrix algebras of dimension \(3\)–\(6\), label the \(q=2,3\) triples, and enumerate lifted spans.

**Likely death.** A useful free nilpotent quotient has superpolynomial dimension; succinct multiplication restores tableau faults.

---

### 6. Global defect ideal followed by expander propagation

**Mechanism.** Find a sparse family of global polynomials \(D_i(x)\) that vanish on every perfect matching but such that every illegal odd-cover mixed word has some nonzero Hasse derivative. Encode the defect vector through an explicit expander code that couples all components, so one surviving defect creates \(N^\varepsilon\) charged coordinates and cannot be neutralized by YES padding.

**Expected move.** Repair the Schur-walk route by proving a genuine global defect before amplification, rather than repeatedly counting one collision cycle.

**Obstruction check.** O1 bounded signatures directly applies whenever \(\deg D\) is below an available cube dimension; evasion likely requires growing degree. O2 tableaux: direct evaluations are outside, circuit evaluation is not. O3 scopes: global ideal, no hierarchy. O4 phases and O5 exact fibers: unused. O6 fingerprints: polynomial features, not assignment columns. O7 tensors: expander propagation is not tensoring, but arbitrary mixed lifted words remain decisive. O8 transfer applies only if the lifted span is constructible without enumerating the fiber.

**Falsification test.** Any illegal all-eight or twisted-holonomy mixed word annihilating all chosen derivatives.

**Smallest experiment.** Compute vanishing ideals for the tiny matching sets, greedily select derivatives, then test cross-component padded NO instances.

**Likely death.** The affine span of legal lifts already contains illegal points, or constructing the nonlinear lifted span is NP-hard.

---

### 7. Sparse spectral-pencil invariant

**Mechanism.** Build an instance-wide sparse matrix pencil \(K(x)=K_0+\sum_jx_jK_j\) whose characteristic polynomial has a prescribed factor for every perfect matching, while odd covers create many discrepant coefficients. Unlike the killed determinant-monomial dictionary, retain only black-box resolvent moments or Wiedemann-style projections of the sparse pencil, not permutation monomials.

**Expected move.** Obtain genuinely global high-degree constraints with polynomial state dimension and no factorial dictionary.

**Obstruction check.** O1 bounded signatures attacks low-order moments; only full-degree spectral data lie outside. O2 tableaux and O5 exact fibers: direct matrix invariants are outside, but determinant/resolvent circuits re-enter their assumptions. O3 scopes and O4 phases: irrelevant. O6 fingerprints: sparse pencil states, not assignments. O7 tensors: none; all mixed spectral states need exact testing. O8 transfer requires linear binary realization of the projected invariants and counting the moment baseline.

**Falsification test.** A support-three cube trade preserving all retained moments, or an illegal cover isospectral to a matching.

**Smallest experiment.** SAT-search \(K_j\) of dimension at most eight on the all-eight core; test traces \(K^r\), characteristic coefficients, and every mixed lifted word.

**Likely death.** Polynomially many projections miss an isospectral illegal combination; full spectral linearization recreates the exponential exterior-state wall.

---

### 8. Small-cancellation filling-area gadget

**Mechanism.** Translate each matching witness into a word that is trivial in an explicit small-cancellation group with a short van Kampen filling. Arrange illegal odd superpositions to represent words requiring Dehn area \(N^\varepsilon\), and attempt to make lattice coefficient norm count relator uses rather than merely abelian homology.

**Expected move.** Replace the failed linear homology classifier by nonlinear filling area, which can distinguish homologically trivial words with very different costs.

**Obstruction check.** O1 bounded signatures: global noncommutative words are outside local polynomial signatures. O2 tableaux: direct relators are outside; local word-reduction transcripts are covered. O3 scopes: no local-view hierarchy. O4 phase lifts: nonabelian filling is not a copy-stable phase. O5 exact fibers: Dehn area is not an affine count slack, although linear lattice encoding may reduce it to one. O6 fingerprints: polynomial relator dictionary. O7 tensors: absent; sums of fillings remain the mixed-word threat. O8 transfer applies only after a binary syndrome realization preserving area, not just boundary.

**Falsification test.** XOR three cheap legal fillings to obtain a cheap illegal filling, especially on all-eight and odd holonomy.

**Smallest experiment.** Use a tiny \(C'(1/6)\) presentation; enumerate bounded van Kampen diagrams and compare legal/illegal filling areas.

**Likely death.** Any lattice realization abelianizes the group, making filling chains add linearly and reproducing the homological affine-closure failure.
