Below, every experiment should include the **all-eight core**, **twisted odd-holonomy instance**, known **affine-closure witnesses**, exhaustive **mixed-word enumeration**, and explicit **YES baseline/output-rank accounting**.

### 1. Signed expander measurement of parity tensors

**Mechanism / expected move.** After obtaining the rigorous tensor parity certificate, replace tensor coordinates by a deterministic signed lossless-expander matrix \(R\). Use the direct integer lattice
\[
(Rz,\;M(Hz-2y)),\qquad v=(0,Mt),
\]
so exact-fiber cost is \(\|Rz\|_2^2\). Sparse-recovery bounds might preserve the \(d^r\) versus \(b^r\) gap using \(O(K\log(N/K))\) rows rather than \(N\) coordinates.

**Obstruction audit.** **Bounded local signatures:** \(R\) measures global tensor words, not local views. **Marginal/tableau:** no marginals or gates. **Local-view hierarchies:** no scopes. **Phase lifts:** no phases. **Integer exact fibers:** outside its local affine-slack hypothesis; signed kernel vectors are nevertheless a direct threat. **Assignment fingerprints:** columns are tensor coordinates, not assignments. **Tensor amplification:** this is a dense measurement, not puncturing/type merging; RIP must cover every mixed word. **Exact transfer:** replaced by a direct integer lift, so the binary identity does not automatically certify it.

**Falsification / experiment.** On reduced \(8^2\)-coordinate 3DM squares, enumerate canonical signed \(3\)-regular expanders and all \(z\in[-2,2]^N\) satisfying parity. Kill if any NO cost is at most worst YES, or row count exceeds the unfurled exponent.

**Likely death.** Short dense signed vectors in \(\ker R\), or \(K\) itself being too large.

---

### 2. Noncommutative ordered-pair fold

**Mechanism / expected move.** Replace the failed commutative truncated algebra by \(A=M_w(\mathbb F_{2^s})\). Canonically label coordinate \(i\) by a rank-one matrix \(L_i=u_iv_i^\top\), and fold ordered tensor coordinate \((i,j)\) to the coefficients of \(L_iL_j\); noncommutativity preserves orientation while using only \(w^2s\) bits.

**Obstruction audit.** **Bounded local signatures:** labels belong to global tensor coordinates, not Boolean local-view signatures, although cube relations may reappear accidentally. **Marginal/tableau:** no wire interfaces. **Local-view hierarchies:** no scopes. **Phase lifts:** not a phase/coboundary construction. **Integer exact fibers:** field-valued folding precedes any lattice lift. **Assignment fingerprints:** only polynomially many coordinate labels occur. **Tensor amplification:** directly targets the code-dependent dense-fold opening; every mixed tensor word must be checked. **Exact transfer:** applies unchanged if the folded output remains binary syndrome decoding.

**Falsification / experiment.** Freeze \(w=3,s=2\), derive \(u_i,v_i\) from canonical parity-check columns, and enumerate every folded word on the standard YES/200-NO/all-eight/holonomy suite. Require best NO \(>\) worst YES and a better rank exponent than \(25/9\) at length \(65\).

**Likely death.** Low-rank bilinear identities create a new all-eight kernel despite preserving order.

---

### 3. Log-depth expander routing of triples

**Mechanism / expected move.** Replace every triple by a globally routed path through three coupled lossless expanders, with routing permutations determined jointly by all endpoint labels. A matching chooses vertex-disjoint routes, while any odd cover with a collision should trigger \(\Omega(L)\) unique-neighbor defects for \(L=\Theta(\log q)\), potentially converting \(q\) versus \(q+2\) into a constant gap at polynomial size.

**Obstruction audit.** **Bounded local signatures:** each column has a logarithmic global route, not a bounded-degree local signature. **Marginal/tableau:** routes are explicit columns, not gate transcripts. **Local-view hierarchies:** uses growing logarithmic scopes, the stated opening. **Phase lifts:** routing is formula-dependent and graph-global, outside copy-stable phases. **Integer exact fibers:** no count slack is used, though route incidence remains affine and may admit repairs. **Assignment fingerprints:** dictionary is triples times polynomially many routes. **Tensor amplification:** no tensoring; mixed route selections are attacked directly. **Exact transfer:** applies if the result is a binary syndrome instance.

**Falsification / experiment.** Use a \(3\)-regular bipartite expander with two routing layers on \(q=2,3\); enumerate every odd route cover and optimize over route choices. Kill on a constant-support rerouting repair, all-eight trade, or odd-holonomy cover.

**Likely death.** Linear path boundaries support short alternating cycles independent of expansion.

---

### 4. Tropical isolation with exact-sum tensor buckets

**Mechanism / expected move.** Assign canonical integer weights \(\omega_i\) from a deterministic splitter family and fold tensor tuple \((i_1,\ldots,i_r)\) to its **exact** sum \(\sum\omega_{i_j}\), not a residue. Scale bucket rows geometrically so the least surviving degree dominates; a uniquely isolated matching should have one protected leading term, whereas NO mixed words should expose several inconsistent leading terms.

**Obstruction audit.** **Bounded local signatures:** degree grows with \(r\), and weights depend globally on the dictionary. **Marginal/tableau:** no local evaluation circuit is introduced. **Local-view hierarchies:** no restriction tables. **Phase lifts:** tropical order is not a cyclic phase, though choosing among splitter branches is a global-selector problem. **Integer exact fibers:** geometric valuation is global, outside bounded-degree slack assumptions; signed cancellation remains possible. **Assignment fingerprints:** weights label polynomially many triples, not complete assignments. **Tensor amplification:** this is structured code-dependent folding and must cover arbitrary mixed tensors. **Exact transfer:** generally requires a direct weighted integer lift, not the mod-2 identity.

**Falsification / experiment.** For \(r=2,3\), use exact powers-of-two weights and all small splitter seeds; enumerate leading-bucket spectra on hostile instances. Reject if all-eight or holonomy has a corner-only/one-bucket word, or if YES scaling dominates the gain.

**Likely death.** Deterministic isolation of 3DM, or combining splitter branches, hides the NP-hard choice.

---

### 5. Rank-condensed exterior-power classifier

**Mechanism / expected move.** View triple incidence columns as vectors and send a \(q\)-tuple to their exterior product in \(\Lambda^q\). Perfect matchings produce decomposable full-coverage wedges; apply explicit rank condensers directly to the exterior-product span, hoping to preserve legal wedges and force illegal mixed combinations into many nonzero condenser blocks without materializing all \(\binom{3q}{q}\) coordinates.

**Obstruction audit.** **Bounded local signatures:** degree is \(q\), not bounded below an independent cube dimension. **Marginal/tableau:** no unary interface. **Local-view hierarchies:** the wedge is global. **Phase lifts:** no phases. **Integer exact fibers:** no affine count slack. **Assignment fingerprints:** base dictionary remains triples, although expanded \(q\)-tuples threaten exponential size. **Tensor amplification:** condensers must be proved sound for the entire mixed exterior span, not decomposable wedges alone. **Exact transfer:** applies only after an explicit binary realization.

**Falsification / experiment.** At \(q=3\), explicitly form all degree-three wedges, enumerate their mixed span, then test every small Guruswami–Kopparty-style evaluation/quotient map. Demand separation on all-eight and holonomy with fewer coordinates than the full degree-three lift.

**Likely death.** Odd affine sums of legal wedges cancel, or computing the condensed generator still requires exponential exterior expansion.

---

### 6. Hankel-rank compression of collision walks

**Mechanism / expected move.** Replace I27’s individually indexed nonbacktracking walks by the Hankel matrix of the collision-walk series: rows are prefixes, columns are suffixes, and entries aggregate compatible walk products. If NO collision behavior requires many automaton states while matchings have zero or constant-state series, rank condensers could retain the amplification using polynomially many matrix blocks rather than exponentially many walks.

**Obstruction audit.** **Bounded local signatures:** walk degree grows logarithmically and uses the global incompatibility graph; fixed-degree cube attacks remain relevant at small depth. **Marginal/tableau:** no gate transcript. **Local-view hierarchies:** prefixes are compressed by automaton state, not explicit scopes. **Phase lifts:** no phases. **Integer exact fibers:** nonlinear Schur products are formed directly; bounded-circuit implementation would re-enter the obstruction. **Assignment fingerprints:** coordinates derive from triples and automaton states. **Tensor amplification:** all mixed Schur words, not only actual covers, require rank lower bounds. **Exact transfer:** condenser block support can be binary-lifted if represented explicitly.

**Falsification / experiment.** Build prefix/suffix Hankel matrices through length four for the existing I27 suite; enumerate every mixed lift and compute minimum rank and block support. Kill if all-eight or twisted holonomy retains rank zero, or rank grows without Hamming support.

**Likely death.** Known hostile affine XORs annihilate the entire collision series, not merely duplicate walks.

---

### 7. Nonlinear filling-area sectors in a sparse complex

**Mechanism / expected move.** Mutate the failed homology quotient by charging the minimum **integral filling area** rather than only the homology class. Attach sparse small-cancellation sheets so each matching has a short dedicated filling, while an illegal but homologically trivial odd cover is conjectured to require a large Dehn-area filling.

**Obstruction audit.** **Bounded local signatures:** global filling minimization is not a bounded local signature. **Marginal/tableau:** no marginal interface. **Local-view hierarchies:** the certificate is a global 2-chain. **Phase lifts:** holonomy is measured by filling geometry, not local phases. **Integer exact fibers:** the boundary equation is linear, so constant-cost signed repairs remain possible. **Assignment fingerprints:** cells arise from triples/routing data, not assignments. **Tensor amplification:** a cubical product might multiply area, but arbitrary mixed fillings require a new theorem. **Exact transfer:** this is direct integer CVP; the binary identity is not enough. Crucially, the **affine-closure obstruction does apply** if three cheap legal fillings can simply be summed.

**Falsification / experiment.** Build the smallest triangular complex for a \(q=3\) instance exhibiting an illegal XOR of three matchings; solve exact minimum \(\ell_2\) fillings by enumeration/ILP. Continue only if the illegal boundary costs more than every sum of legal fillings and survives holonomy.

**Likely death.** Triangle inequality gives an illegal filling of at most three times the legal cost, precluding polynomial amplification.
