I did not use the prohibited document or related material.

1. **AG-code / low-Schur-growth base redesign**  
**Core trick.** Replace BMT’s generic moving code by an algebraic-geometry evaluation code \(D\subseteq L(G)\). Products of \(r\) codewords then lie in \(L(rG)\), whose dimension grows roughly linearly in \(r\deg G\), potentially compressing pure-power tensors without the \(2^{\dim D}\) wall.  
**Expected move.** Obtain multiplicative pointed distance with polynomial multiplication-table rank for \(r=\Theta(\log N)\).  
**Obstruction check.** O1 bounded signatures: outside if columns are genuinely global evaluations, not bounded-degree Boolean views. O2 marginals/tableaus: no wire interfaces. O3 local hierarchies: no scope tables. O4 phases: none. O5 integer fibers: no slack repair. O6 fingerprints: polynomial evaluation coordinates, not complete-assignment columns. O7 tensor amplification: directly targets its rank wall, but lacks the required all-mixed-word distance theorem. O8 exact transfer: applies after binary expansion.  
**Falsification.** Coordinatewise AG multiplication may preserve only nonzeroness, not Cartesian-tensor Hamming weight.  
**Smallest experiment.** Search small RS/AG subcodes containing the \(q=3\) 3DM moving spans; compute Schur-power rank and exact pointed YES/NO distances through \(r=4\), including all-eight and holonomy instances.  
**Likely death.** NP-hard fibers may be incompatible with low Schur growth, or distance collapses under multiplication.

2. **Saturated collision-tree Schur lift**  
**Core trick.** Mutate I27 by using squarefree rooted collision trees rather than repeated walks, and include the complete monomial algebra on every collision component of size at most eight. Proper matchings activate none; a NO cover with expanding incompatibility should activate many color-coded tree embeddings.  
**Expected move.** With bounded incompatibility degree and depth \(\Theta(\log q)\), obtain polynomial output and exponentially many charged embeddings while explicitly sealing the all-eight core.  
**Obstruction check.** O1 bounded signatures: not outside globally—degree-\(r\) lifts still admit larger cube relations. O2 marginals: features do not factor through unary marginals. O3 local hierarchies: also not outside; proper trees remain vulnerable to odd holonomy. O4 phases: none. O5 integer fibers: binary nonlinear lift only. O6 fingerprints: sparse collision structures, not full assignments. O7 tensor: avoids ordinary tensoring but still needs every-mixed-word soundness. O8 transfer: immediate if the lifted span is explicitly generated.  
**Falsification.** A low-degree pseudo-distribution or odd sum of legal lifts cancels all tree coordinates.  
**Smallest experiment.** Extend I27 with all squarefree trees through five vertices; exhaust all-eight, twisted holonomy, affine-closure, and 200 NO instances.  
**Likely death.** Generating the lifted span or enforcing bounded degree becomes superpolynomial.

3. **Hasse-derivative sparse-PIT tensor condenser**  
**Core trick.** Represent a mixed reduced-square word as \(F_W(X,Y)=\sum W_{ij}X^{a_i}Y^{b_j}\). Output evaluations and Hasse derivatives of \(F_W(X,X^{2^u})\) at several field points; multiplicity bounds are stronger than the evaluation-only modular fold I26 and the rank-only \(F_8\) condenser.  
**Expected move.** Force every low-support NO mixed polynomial to survive in many derivative layers while keeping pure YES squares sparse; simplex-encode nonzero field symbols.  
**Obstruction check.** O1 bounded signatures: any inherited cube relation survives this linear fold, so it is not protected. O2 marginals: no local interfaces. O3 scopes: global polynomial measurements. O4 phases: none. O5 integer fibers: no slacks. O6 fingerprints: labels tensor coordinates, not assignments. O7 tensor: squarely inside the open code-dependent dense-fold niche; mixed support remains unproved. O8 transfer: applies to the resulting binary matrix.  
**Falsification.** One pointed NO word has small derivative-image support, or worst YES becomes dense.  
**Smallest experiment.** Over \(\mathbb F_{16}\), use derivative orders \(0,1,2\), all Frobenius curves, and exactly enumerate the existing \(q=3\) suite plus hostile cores.  
**Likely death.** Multiplicity guarantees rank/nonvanishing, not Hamming support.

4. **Circuit-aware \(B_h\) convolution fold**  
**Core trick.** Assign tensor coordinates labels in a finite abelian group and fold tuples by label sum, but choose labels from the parity-check matroid so that every dangerous low-weight mixed circuit is \(B_h\)-separated. Unlike I26’s frozen modular powers, the constraints are derived from the actual code’s short circuits.  
**Expected move.** Compress to polynomially many group buckets while proving injectivity only on candidate words below the desired NO threshold, rather than on every tuple.  
**Obstruction check.** O1 bounded signatures: linear folding cannot remove an existing cube trade. O2 marginals: no tableau. O3 scopes: uses global circuit structure. O4 phases: labels are not local phases. O5 integer fibers: irrelevant. O6 fingerprints: no assignment grouping. O7 tensor: genuinely code-dependent structured folding, but arbitrary mixed words outside the protected circuit family remain exposed. O8 transfer: exact after binary bucket expansion.  
**Falsification.** The label SAT instance is infeasible at every group size below the unfurled length, or an unlisted mixed word collapses.  
**Smallest experiment.** Enumerate all pointed words up to weight 25 in tiny reduced-square codes; solve label constraints by SAT for groups of size \(8,16,32\), then re-enumerate every image word.  
**Likely death.** Finding all dangerous circuits is NP-hard, or additive-combinatorial lower bounds force near-full size.

5. **Nonabelian Magnus–Fox holonomy dictionary**  
**Core trick.** Give incidence edges free-group generators determined by a canonical global spanning forest. Encode selected covers by truncated Magnus expansions and Fox derivatives; valid matchings should have a prescribed boundary word, while odd permutation holonomy should leave noncommuting derivative residues.  
**Expected move.** Replace single-valued phase labels by a graph-dependent, multivalued global invariant that sees orientation and commutators.  
**Obstruction check.** O1 bounded signatures: finite truncation is still bounded-degree and therefore not outside; only exact unbounded words escape. O2 marginals: direct group words are global, but circuit compilation re-enters tableaus. O3 scopes: global fundamental-group data avoids proper-scope assumptions. O4 phase lifts: outside its coboundary theorem because transport is nonabelian, path-dependent, and formula-specific. O5 integer fibers: a slack/circuit realization would re-enter it. O6 fingerprints: no complete assignments. O7 tensor: not tensor-based; mixed affine spans remain a separate threat. O8 transfer: unavailable until a polynomial binary linearization exists.  
**Falsification.** Illegal all-eight or holonomy covers lie in the affine span of legal truncated fingerprints.  
**Smallest experiment.** Compute degree-\(\le4\) Magnus/Fox vectors for all covers of the hostile instances and compare legal affine spans.  
**Likely death.** Exact words require exponential dimension; polynomial truncation succumbs to cube relations.

6. **Error-locator polynomial sectors**  
**Core trick.** For a fiber word \(x\), form the global locator \(L_x(T)=\prod_{j:x_j=1}(T-a_j)\). Store residues and Hasse derivatives of \(L_x\) modulo several irreducibles, with strongly weighted degree layers, aiming to make weight \(q\) matchings cheap while every weight-\(\ge q+2\) cover occupies higher sectors.  
**Expected move.** Compress support identity into \(O(m\,\mathrm{polylog}\,m)\) algebraic coordinates rather than tensor tuples or complete assignments.  
**Obstruction check.** O1 bounded signatures: full locator degree is global; truncation returns to O1. O2 marginals: direct locators avoid interfaces, but a multiplication circuit does not. O3 scopes: genuinely global. O4 phases: none. O5 integer fibers: circuit/slack implementation would be covered. O6 fingerprints: it groups fiber words rather than complete assignments, so exponential explicit columns remain a danger. O7 tensor: avoids tensor rank, but has no mixed-span norm theorem. O8 transfer: applies only after explicit binary linearization.  
**Falsification.** The span of legal locator vectors contains a low-sector illegal locator combination.  
**Smallest experiment.** For \(m=8\), calculate all locator vectors over \(\mathbb F_{17}\), row-reduce their spans, and measure exact weighted distances on all-eight, holonomy, and affine-closure families.  
**Likely death.** Polynomial generation of the nonlinear locator span hides the original NP-hard problem.

7. **Tropical three-matroid exterior lift**  
**Core trick.** View 3DM as common bases of three partition matroids. Give each matroid a Puiseux-valued representation and attach selected exterior minors at several valuation scales, hoping that common bases occupy one sparse tropical sector while signed odd covers violate at least one valuated basis-exchange profile extensively.  
**Expected move.** Produce a global algebraic dictionary with polynomially many sampled compound coordinates and near-zero honest baseline.  
**Obstruction check.** O1 bounded signatures: global minors lie outside local Boolean signatures, although low-order compounds may still admit cube trades. O2 marginals: no proper marginals. O3 scopes: no local views. O4 phases: none. O5 integer fibers: valuations implemented by ordinary slacks would re-enter it. O6 fingerprints: indexes matroid minors, not assignments. O7 tensor: independent of tensoring, but sampled compounds need an all-superpositions theorem. O8 transfer: compatible if valuations become explicit binary weighted rows.  
**Falsification.** A support-three virtual basis matches all retained valuation profiles, or output requires exponentially many minors.  
**Smallest experiment.** Use symbolic \(t\)-valued \(q=3,4\) partition-matroid matrices; enumerate signed covers and search greedily for a polynomial minor subset separating legal bases from hostile words.  
**Likely death.** Birkhoff/toric low-degree exchanges survive every polynomially sampled compound family.
