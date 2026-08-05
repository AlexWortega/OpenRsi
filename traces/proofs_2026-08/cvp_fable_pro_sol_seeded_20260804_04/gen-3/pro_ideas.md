### 1. Slice-rank condenser for mixed tensor words

**Core trick.** For reduced tensor generator \(G^{\otimes r}\), view every mixed word as a multilinear coefficient tensor. Recursively apply explicit rank condensers to its flattenings, then evaluate surviving condensed tensors on a small code-dependent set of tuples; low slice rank should reduce to individually heavy factors, while high slice rank should activate many blocks.

**Expected move.** Replace \(n^r\) coordinates by \(\mathrm{poly}(n,r)\) blocks while retaining nearly \(d^r\) versus \(b^r\) distance.

**Obstruction audit.** **Bounded local signatures:** outside only if \(r\) grows; fixed \(r\) remains vulnerable. **Marginal/tableau:** no wire marginals. **Local-view hierarchies:** no scopes. **Phase lifts:** no phases. **Integer exact fibers:** operates on global coefficient tensors. **Complete-assignment fingerprints:** messages, not assignments, are represented. **Tensor amplification:** directly targets its unresolved code-dependent dense-fold opening; arbitrary mixed words remain the central obligation. **Exact transfer:** applies conditionally after producing binary \(H,t\), with folded rank counted.

**Experiment.** On the \(q=3,m=8\) suite, enumerate every tensor word for \(r=2,3\); exhaust all \(2\times k\) condenser matrices and test all-eight and twisted-holonomy instances.

**Falsification/death.** Kill if a rank-one or alternating mixed tensor maps below the YES maximum. Most likely low-rank summands cancel after condensation.

---

### 2. Dissociated integer sketch of the parity tensor certificate

**Core trick.** Start from the rigorous mod-2 tensor support certificate, but compress coordinates with integer hash rows carrying dissociated weights \(1,B,B^2,\ldots\). Across a perfect-hash family, every small odd support should have a bucket where odd coefficients cannot cancel without either large coefficient norm or large residual.

**Expected move.** Obtain submultiplicative Euclidean rank while retaining \((q+1)^r\) versus \((q+3)^r\) squared norms.

**Obstruction audit.** **Bounded local signatures:** not automatically outside—an inherited small exact cube relation kills it. **Marginal/tableau:** no marginals. **Local-view hierarchies:** no scopes. **Phase lifts:** no phases. **Integer exact fibers:** outside its local-slack assumptions only if a global dissociation lemma handles every signed tensor vector. **Complete-assignment fingerprints:** hashes tensor coordinates, not assignments. **Tensor amplification:** this is asymmetric integer compression, not puncturing or a common catalyst. **Exact transfer:** unnecessary for direct CVP; mod-2 reduction remains a soundness certificate.

**Experiment.** For reduced \(q=3\) tensor squares, enumerate 2-universal/perfect hashes, \(B\le16\), and coefficients in \([-2,2]\); include all-eight and holonomy witnesses and report rank-adjusted gap.

**Falsification/death.** One short signed kernel vector of NO norm at most worst YES kills a matrix. Likely Siegel-type integer relations force either cancellation or an enormous YES baseline.

---

### 3. Expander-diffused logarithmic Schur lift

**Core trick.** Mutate the killed incompatibility-walk shell by first globally diffusing the triple vector through a fixed lossless-expander code \(y=Ex\). Add degree \(r=\Theta(\log q)\) products along self-avoiding expander neighborhoods, so a constant local collision cannot remain confined under disjoint-component padding.

**Expected move.** Keep \(mD^r=\mathrm{poly}(m,q)\) coordinates while making every \(q+2\) defect activate \(q^\alpha\) global features.

**Obstruction audit.** **Bounded local signatures:** potentially outside because degree grows and encoded bits are not independently flippable; any surviving \((r+1)\)-cube refutes this. **Marginal/tableau:** products are direct global coordinates, not gate transcripts. **Local-view hierarchies:** no scope tables. **Phase lifts:** none. **Integer exact fibers:** no affine slacks. **Complete-assignment fingerprints:** only polynomially many support features. **Tensor amplification:** not tensoring. **Exact transfer:** applies if the lifted span is constructible as a binary code.

**Experiment.** Use a 3-regular expander on the existing \(m=8,9,10\) dictionaries, degrees \(3\!-\!6\); enumerate the exact lifted span, all-eight core, twisted holonomy, and padded NO components.

**Falsification/death.** Kill if padding leaves \(O(1)\) charge or a mixed word cancels every feature. Most likely death: constructing the nonlinear lifted span without enumerating the affine fiber is itself NP-hard.

---

### 4. Splitter-compressed Plücker dictionary

**Core trick.** Color triples using an explicit splitter family and attach exterior/Plücker coordinates of the three pair-projection matrices. A true matching is decomposable in at least one color sector; seek a partition-rank theorem forcing every signed odd cover to occupy polynomially many incompatible Plücker sectors.

**Expected move.** Turn the variable-permutation classifier’s additive \(q\)-baseline into a zero-baseline global decomposability test.

**Obstruction audit.** **Bounded local signatures:** top wedges have degree \(q\), outside bounded-degree cubes. **Marginal/tableau:** determinants are attached globally, not evaluated gatewise. **Local-view hierarchies:** no proper scopes. **Phase lifts:** none. **Integer exact fibers:** validity is determinantal, not affine count slack. **Complete-assignment fingerprints:** indexes triples/splitter sectors, not \(2^n\) assignments. **Tensor amplification:** absent initially; arbitrary linear combinations of Plücker states must still be searched. **Exact transfer:** extension-field rows can be binary-expanded if size stays polynomial.

**Experiment.** For \(q=3,4\), enumerate small splitter families and all minors of the three projection matrices; compare every matching, odd cover, all-eight trade, and twisted three-matching XOR.

**Falsification/death.** Kill if a support-three Grassmann–Plücker relation matches legal cost. Most likely the required exterior basis or determinant monomials grow exponentially, reproducing I20 in compressed clothing.

---

### 5. Nonabelian branched-cover selector

**Core trick.** Label triples by permutations in a small nonabelian group and order transitions globally by one vertex part. A matching traces one path whose terminal group element is absorbed by a single global endpoint selector; an odd cover branches or has inconsistent monodromy, which should require many endpoint sectors.

**Expected move.** Exploit graph-dependent, multivalued global holonomy rather than copy-stable scalar phases, potentially charging odd affine superpositions.

**Obstruction audit.** **Bounded local signatures:** outside only if the whole ordered product is one global signature. **Marginal/tableau:** compiling multiplication through local states falls squarely inside this obstruction. **Local-view hierarchies:** no scopes in the ideal global form. **Phase lifts:** specifically outside its single-valued abelian/coboundary assumptions. **Integer exact fibers:** no count slack. **Complete-assignment fingerprints:** group size and endpoint menu are polynomial. **Tensor amplification:** not used; mixed endpoint combinations require exhaustive soundness. **Exact transfer:** matrix representations over \(\mathbb F_2\) permit conditional binary transfer.

**Experiment.** Search \(S_3,S_4\) labels on the \(q=3\) all-eight and twisted dictionaries; explicitly span all endpoint-selector columns and compute coset minima.

**Falsification/death.** A rectangle splice selecting several endpoints at constant cost kills it. Most likely any polynomial implementation becomes a bounded-fan-in branching-program tableau and inherits the known exact repair.

---

### 6. Tropical valuation shell for matching monomials

**Core trick.** Assign each triple a multivariate monomial and choose a formula-dependent tropical weight vector. Perfect matchings should occupy exposed vertices of the matching Newton polytope, while signed odd covers lying in their affine span may still have larger valuation multiplicity; encode valuations by scaled integer rows and a sparse normal-fan dictionary.

**Expected move.** Separate legal witnesses without quotienting them together: each matching receives its own cheap valuation chamber, but superpositions cross many chambers.

**Obstruction audit.** **Bounded local signatures:** global degree grows with \(q\). **Marginal/tableau:** no local gate evaluation. **Local-view hierarchies:** no scopes. **Phase lifts:** no phases. **Integer exact fibers:** outside only if chamber crossing, rather than affine row scaling, supplies the norm gap. **Complete-assignment fingerprints:** chambers index matching-polytope faces, not complete SAT assignments, though their count may explode. **Tensor amplification:** not invoked; all mixed chamber combinations need checking. **Exact transfer:** this is initially direct integer CVP; binary transfer would require a separate bounded-bit realization.

**Experiment.** Compute Newton polytopes for \(q=3\) dictionaries, enumerate small integer weight vectors, and compare valuation vectors for matchings, every odd cover, all-eight trades, and holonomy XORs.

**Falsification/death.** Kill if an illegal affine combination remains in the same normal cone at comparable norm. Most likely polynomially many chambers cannot protect all matchings, while complete protection is exponential.

---

### 7. High-Dehn-function filling gadget

**Core trick.** Map an exact-cover coefficient vector to a boundary word in a finitely presented group with a large Dehn function. Legal matchings admit prescribed short van Kampen fillings; malformed odd covers may be null-homologous yet require polynomially larger filling area, addressing the failure of ordinary linear homology.

**Expected move.** Replace homology class by filling complexity, so an illegal XOR of cheap legal boundaries need not inherit a cheap filling.

**Obstruction audit.** **Bounded local signatures:** global word order is high-degree. **Marginal/tableau:** a cell-by-cell linearization would re-enter tableau kernels. **Local-view hierarchies:** filling area is global, not bounded scope. **Phase lifts:** nonabelian word holonomy is not a scalar phase. **Integer exact fibers:** objective counts global relator usage, not local slacks. **Complete-assignment fingerprints:** relators are fixed and sparse. **Tensor amplification:** unnecessary; arbitrary signed 2-chains are the analogue of mixed words and must be included. **Exact transfer:** only after converting filling equations to a polynomial-size binary syndrome system.

**Experiment.** Use a small presentation such as a Baumslag–Solitar-style distortion gadget; map the \(q=3\) matching/odd-cover boundaries and solve minimum filling area by integer programming.

**Falsification/death.** A sum of three legal diagrams with area \(O(q)\) kills amplification. Most likely enforcing noncommutative boundary order requires exponentially many states or exactly the bounded-interface machinery already obstructed.
