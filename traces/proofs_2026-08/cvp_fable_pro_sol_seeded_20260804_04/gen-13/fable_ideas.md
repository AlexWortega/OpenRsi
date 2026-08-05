No prohibited-source material is used below.

### 1. Color-coded collision-forest Schur lift

**Core trick.** Replace I27’s repeated walks by parity sums over *colorful self-avoiding collision forests*. A splitter family and dynamic programming give polynomially many degree-\(r=\Theta(\log m)\) coordinates; matchings activate none, while an illegal cover should expose many independently colored collision trees.

**Obstruction check.** **Bounded local signatures:** growing degree lies outside the bounded-degree claim, although its \(2^{r+1}\)-term cube relation remains potentially affordable. **Marginal/tableau encodings:** no wire marginals or gate transcript. **Local-view hierarchies:** forests are global support polynomials, not consistency scopes. **Phase lifts:** no phases. **Integer exact fibers:** binary nonlinear lift, no slacks. **Complete-assignment fingerprints:** coordinates index forest types, not assignments. **Tensor amplification:** not a tensor sample; soundness over the entire lifted linear span is still unproved. **Exact transfer:** applies once the lifted binary generator is explicit.

**Expected move.** Obtain YES cost \(q\) and NO cost \(q^{1+\epsilon}\) with polynomial rank.

**Smallest experiment/falsification.** For all-eight, holonomy, affine-closure, and existing \(q=3\) instances, enumerate every mixed word for forest sizes \(2\!-\!5\), recording rank and worst-YES/best-NO. Falsify if either hostile family has zero forest charge.

**Likely death.** Parity aggregation cancels forests, or the lifted rank grows as \(k^{\Theta(\log m)}\).

---

### 2. Quasirandom nonabelian convolution fold

**Core trick.** Canonically label the \(m\) tensor coordinates by distinct elements \(\lambda_i\) of \(G=\mathrm{PSL}_2(\mathbb F_p)\), with \(|G|=\Theta(m)\). For fixed probes \(a_s\), fold a mixed matrix \(W\) by
\[
F_s(W)_g=\bigoplus_{\lambda_i a_s\lambda_j^{-1}=g}W_{ij},
\]
using \(O(\log m)\) probes; this preserves ordered-pair information while compressing \(m^2\) coordinates to \(O(m\log m)\).

**Obstruction check.** **Bounded local signatures:** the pure-square map is quadratic, so cube relations may still apply; this is not escaped unless code restrictions destroy those cubes. **Marginal/tableau:** direct global buckets, no interfaces. **Local-view hierarchies:** no scopes. **Phase lifts:** labels are not copy-stable phases. **Integer exact fibers:** binary fold only. **Complete-assignment fingerprints:** labels attach to sparse triple columns. **Tensor amplification:** precisely the open code-dependent dense-fold case; every mixed \(W\) must be checked. **Exact transfer:** applies to the folded syndrome system.

**Expected move.** Quasirandom product mixing should spread NO mixed matrices while structured YES squares remain concentrated.

**Smallest experiment/falsification.** Use \(\mathrm{PSL}_2(\mathbb F_3)\), all conjugacy-class probes, and the full hostile suite; exhaust mixed words and relabelings. Kill if any pointed kernel appears or best NO \(\le\) worst YES.

**Likely death.** Quasirandomness controls Fourier norm, not Hamming support.

---

### 3. Canonical matroid-flat multiscale condenser

**Core trick.** Build a canonical shortening/contracting flag of the moving code from its represented matroid, then measure a mixed tensor matrix through quotient maps associated with successive rank jumps. Unlike the frozen Vandermonde condenser, fine blocks inspect sparse flats while coarse blocks detect combinations crossing many flats.

**Obstruction check.** **Bounded local signatures:** maps depend on the entire represented matroid, not a fixed local-view polynomial. **Marginal/tableau:** no local communication. **Local-view hierarchies:** flats are global code subspaces, not CSP scopes. **Phase lifts:** absent. **Integer exact fibers:** absent. **Complete-assignment fingerprints:** only polynomially many code-derived flag levels. **Tensor amplification:** outside code-oblivious puncturing and fixed condensers, but arbitrary mixed-word support remains the central missing lemma. **Exact transfer:** applies after binary image construction.

**Expected move.** Achieve output \(m^{1+o(1)}\), preserve YES squares with cost near \(d^2\), and charge NO words through many independent rank-jump blocks.

**Smallest experiment/falsification.** On \(m=8\), enumerate all cyclic flats, select the lexicographically canonical maximal rank-jump chain, instantiate all binary quotient-pair maps, and attack every mixed word in the hostile suite. Reject if affine-closure or all-eight reaches the corner alone, or if exact image rank erases the nominal compression.

**Likely death.** Matroid rank visibility again flattens support, or useful canonical flags are exponentially large.

---

### 4. Optimal global-parity shell synthesis

**Core trick.** Strengthen I19 from hand-chosen features to the *optimal* weighted family of global parities. For tiny \(m\), include every nonzero parity \(r\cdot x\), solve an LP minimizing worst YES cost while maximizing minimum NO cost, then inspect the optimum for a polynomially describable algebraic pattern.

**Obstruction check.** **Bounded local signatures:** not escaped—linear rows preserve cube and affine-closure relations exactly. **Marginal/tableau:** no local interfaces. **Local-view hierarchies:** no scopes. **Phase lifts:** none. **Integer exact fibers:** binary feature variables, not scaled integer slacks. **Complete-assignment fingerprints:** features act on polynomially many triple coordinates, although the exploratory pool is exponential only at tiny \(m\). **Tensor amplification:** no tensoring; mixed affine-fiber words are explicit LP constraints. **Exact transfer:** weighted integer replications produce an ordinary binary syndrome instance and hence the exact lattice lift.

**Expected move.** Either discover a small orbit family overlooked by pair/hash shells, or certify a strong finite upper bound on every linear-feature mechanism.

**Smallest experiment/falsification.** For \(m=8\), use all 255 parities and all exact YES/NO, affine-closure, all-eight, and holonomy words; solve the rational LP and sparsify its support. Falsify if optimum cannot beat \(5/3\) or fails a held-out relabeling.

**Likely death.** An illegal odd XOR of three cheap legal witnesses has feature cost at most their summed cost, forbidding polynomial separation.

---

### 5. Color-coded resultant/Hasse-jet dictionary

**Core trick.** Label triples by field elements and associate a support \(x\) with its root polynomial \(P_x(T)=\prod_{j:x_j=1}(T-\alpha_j)\). Retain color-coded coefficients, resultants against the three vertex-part polynomials, and Hasse derivatives: a matching has one simple root per incidence class, whereas repeated/missing coverage should create many nonzero jets.

**Obstruction check.** **Bounded local signatures:** logarithmic-degree global products are outside the bounded-degree regime, though large cube relations remain. **Marginal/tableau:** outside only if jets are generated directly; compiling multiplication gates re-enters this obstruction. **Local-view hierarchies:** no restriction scopes. **Phase lifts:** none. **Integer exact fibers:** field-algebraic, not count slacks. **Complete-assignment fingerprints:** labels attach to triples, not assignments. **Tensor amplification:** this is a selective Veronese lift, not ordinary tensoring; all mixed lifted words require proof. **Exact transfer:** extension-field symbols can be simplex-encoded into binary coordinates.

**Expected move.** Turn a constant coverage defect into polynomially many derivative violations with polynomially many color-coded coordinates.

**Smallest experiment/falsification.** Over \(\mathbb F_{16}\), enumerate degree \(2\!-\!5\) jets for all-eight, holonomy, affine-closure, and \(q=3\) fibers; construct the span of all lifted points and measure exact rank and distance. Kill if a hostile mixed word annihilates every jet.

**Likely death.** Direct generator construction requires superpolynomial monomial rank; circuit realization revives tableau cheats.

---

### 6. High-Dehn-function filling-area shell

**Core trick.** Map each selected triple to a short noncommutative word so that a perfect matching forms a word with a prescribed short van Kampen filling, while an illegal odd cover represents a null-homologous word requiring huge filling area. Groups such as finite-radius quotients of Baumslag–Solitar-type presentations offer exponential separation between boundary length and filling area.

**Obstruction check.** **Bounded local signatures:** global word order is not a bounded-degree Boolean signature. **Marginal/tableau:** not escaped if paths and relator applications are compiled through local transition tables. **Local-view hierarchies:** global filling area can detect holonomy, but bounded-radius diagram scopes cannot. **Phase lifts:** nonabelian transport is not a scalar phase, though single-valued local transport may still gauge away. **Integer exact fibers:** linear boundary equations alone abelianize the group and fall back inside this obstruction. **Complete-assignment fingerprints:** relator conjugates, not assignments. **Tensor amplification:** no tensoring; the challenge is linearizing area without cheap mixed fillings. **Exact transfer:** available only after an explicit binary filling dictionary exists.

**Expected move.** Replace homology, which loses to affine closure, by nonlinear filling complexity.

**Smallest experiment/falsification.** Assign words to the \(q=2\) all-eight triples, enumerate bounded-area diagrams by BFS, and compare legal words with every illegal odd XOR; then repeat on holonomy. Falsify if three cheap legal diagrams splice into a cheap illegal diagram.

**Likely death.** Any polynomial linear encoding forgets word order, while preserving order recreates bounded-fan-in tableau faults.
