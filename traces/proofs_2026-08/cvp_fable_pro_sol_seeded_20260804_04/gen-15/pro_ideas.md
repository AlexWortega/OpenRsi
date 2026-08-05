I use: **O1** bounded local signatures; **O2** marginal/tableau encodings; **O3** local-view hierarchies; **O4** phase lifts; **O5** integer exact fibers; **O6** complete-assignment fingerprints; **O7** tensor amplification; **O8** exact syndrome-to-CVP transfer.

### 1. Code-dependent high-dimensional-expander tensor restriction

**Mechanism.** Replace arbitrary tensor-coordinate sampling by walks/faces of a high-dimensional expander constructed from the base code’s parity-check matroid. Coboundary expansion is intended to make every mixed tensor word visible on many selected faces, while only \(mD^{r-1}\) coordinates are retained.

**Expected move.** Obtain distance roughly \(d^r/\mathrm{poly}(r)\) at polynomial length for \(r=\Theta(\log N)\).

**Map check.** O1: global degree-\(r\) products still have cube relations, so not formally escaped; feasibility geometry must prevent their use. O2: no marginals/tableaus. O3: faces span global matroid dependencies, not bounded scopes. O4: no phases. O5: entirely binary. O6: no assignment columns. O7: directly occupies the code-dependent structured-sampling opening, unlike fixed sampling. O8: applies if the binary gap survives.

**Smallest experiment.** For each \(m=8\) code, greedily construct a 3-regular graph maximizing parity-check-column expansion; retain length-3 and length-4 walk tensor coordinates. Enumerate every mixed word on YES/NO, all-eight, affine-closure, and holonomy cases.

**Falsification/death.** Reject on any pointed kernel, hostile distance below worst YES, or exponent below unfurled tensoring. Most likely death: an HDX analogue of the sampled-fold overfitting collapse.

---

### 2. Exterior-rank profile with representative-set compression

**Mechanism.** Regard a reduced-square word as a matrix \(W\). Lift it to selected \(2\times2,\ldots,r\times r\) minors; rank-one YES squares have vanishing higher minors, whereas genuinely mixed NO words should expose a broad exterior-rank profile. Use deterministic representative-set/rank-condenser methods to retain only polynomially many minors.

**Expected move.** Charge mixed rank without densifying rank-one YES words, addressing the failure of linear \(AWB\) condensers.

**Map check.** O1: fixed-size minors are bounded-degree signatures and are covered; the proposal only escapes if growing-degree minors admit polynomial representative compression. O2: minors are global, not proper marginals. O3: no scopes. O4: no phases. O5: binary extension-field arithmetic, not integer slacks. O6: polynomial matrix-basis dictionary. O7: every mixed matrix must be tested; this is not ordinary puncturing. O8: binary expansion permits transfer if support bounds hold.

**Smallest experiment.** Over \(\mathbb F_4\), lift every \(8\times8\) mixed square to all \(2\times2\) and \(3\times3\) minors, greedily retain minors that increase lifted-code rank, then enumerate the resulting affine span.

**Falsification/death.** Reject unless all hostile distances exceed worst YES with improved exact rank exponent. Likely death: polarization makes illegal low-rank combinations as cheap as YES, or O1 reappears.

---

### 3. Small-cancellation filling-area shell

**Mechanism.** For a binary cover \(x\), form excess counts \(e_v=(\deg_x(v)-1)/2\) and the canonical word \(w(x)=\prod_v g_v^{e_v}\) in an instance-dependent small-cancellation group. Matchings give the identity; encode a filling of \(w(x)\) in a truncated Cayley 2-complex, hoping every nontrivial excess word requires polynomial area rather than merely nonzero homology.

**Expected move.** Replace linear homology—which identifies odd affine combinations—by nonlinear Dehn area with zero YES baseline.

**Map check.** O1: the global word is unbounded-degree, outside bounded signatures abstractly. O2: no proper marginals unless word multiplication is tableaud. O3: detects global holonomy. O4: graph-dependent multivalued fillings are outside coboundary phases. O5: a bounded-fan-in linearization would fall back inside this obstruction. O6: no assignment fingerprints. O7: not tensor-based; all mixed fillings still require attack. O8: unavailable until a binary linear realization is supplied.

**Smallest experiment.** Use a two-generator \(C'(1/6)\) presentation, radius-six Cayley ball, and q=2/q=3 covers. Compute minimum mod-2 filling area for every lifted mixed word.

**Falsification/death.** All-eight or holonomy having area at most worst YES kills it. Likely death: XOR of three cheap fillings remains cheap, or the finite complex is exponential.

---

### 4. AG norm-product shell for count excess

**Mechanism.** Map the excess vector \(e=(Ax-\mathbf1)/2\) over a large odd field to a function \(f_e\) in a low-degree Riemann–Roch space. Partition curve evaluations into disperser blocks and attach block norms \(\prod_{P\in B} f_e(P)\): YES has zero baseline, while a nonzero excess polynomial should activate many blocks multiplicatively.

**Expected move.** Turn the additive \(q\) versus \(q+2\) defect into polynomially many charged norm blocks without permutation tables.

**Map check.** O1: block norms have growing global degree; fixed block size is covered. O2: evaluations are global linear forms, not local wire marginals. O3: the full excess vector sees odd holonomy. O4: no phases. O5: nonlinear norms are outside affine slacks, but any bounded-fan-in norm circuit re-enters O5. O6: dictionary is vertices/curve points, not assignments. O7: no tensoring; mixed lifted words remain essential. O8: odd-characteristic arithmetic has no automatic binary transfer.

**Smallest experiment.** Take \(p=11\), a small elliptic curve, q=3 instances, degree-two functions, and blocks of three evaluations. Enumerate lifted spans and compare worst YES with all NO/hostile costs.

**Falsification/death.** Reject if a nonzero excess has all norm blocks zero or affine mixing creates a cheap word. Likely death: characteristic conversion or norm linearization recreates exact-fiber repairs.

---

### 5. Two-regime defect isolation with protected selector sectors

**Mechanism.** Use deterministic splitters/BCH checks to isolate every small collision set, and lossless-expander neighborhoods to charge large collision sets. Keep hash charts in separate selector sectors coupled by a high-distance algebraic selector code, rather than XORing all charts into one shell.

**Expected move.** Repair Schur-walk cancellation: small hostile trades should be isolated in one chart, while large trades pay expansion, with polynomially many charts.

**Map check.** O1: individual collision features remain low-degree and therefore covered unless isolation destroys the relevant feasible cube. O2: selector coupling must be global; local chart interfaces would trigger rectangle kernels. O3: splitters are disconnected global scopes, potentially seeing holonomy. O4: this is a multivalued global selector, outside the coboundary theorem but close to the killed branch splice. O5: binary only. O6: no complete assignments. O7: not ordinary tensoring; every mixed chart word must be bounded. O8: applies conditionally.

**Smallest experiment.** Use all pairwise-independent hashes from eight triples to four buckets, BCH syndromes per bucket, and a \([7,3,4]\) selector code. Exhaustively enumerate every mixed image word on the standard hostile suite.

**Falsification/death.** Kill on a cross-chart splice, pointed kernel, or hostile cost no larger than worst YES. Most likely death: selector superpositions reproduce the weight-nine branch splice.

---

### 6. Chvátal–Gomory closure as a zero-slack global dictionary

**Mechanism.** Starting from \(Az=\mathbf1\), generate instance-dependent rank-\(r\) Chvátal–Gomory cuts whose slack is zero on every Boolean perfect matching. Encode only violated cut slacks, chosen through a sparse cut-expander, so signed nonintegral exact-fiber points are intended to violate many globally rounded constraints without adding a \(q\)-sized honest table.

**Expected move.** Replace ordinary affine projection tables by growing-rank global integrality certificates with zero YES norm.

**Map check.** O1: fixed-rank cuts are bounded-complexity signatures and likely covered; growing CG rank is outside the stated degree bound. O2: cuts involve the full incidence system. O3: global cuts may detect holonomy. O4: no phases. O5: fixed-rank affine slack implementations are covered; the proposal requires genuinely global rounding, so this is the central danger. O6: no assignment columns. O7: independent of tensor compression. O8: no direct transfer until cuts receive an exact binary realization.

**Smallest experiment.** For q=3, enumerate all rank-one and rank-two CG cuts with coefficients in \(\{-2,\ldots,2\}\); greedily select a rank-independent family and solve exact signed minimum-slack problems.

**Falsification/death.** Reject if the known norm-5 signed NO witness violates only \(O(1)\) cuts or all-eight remains cheap. Likely death: polynomially constructible cuts have constant repair, while strong separation is NP-hard.
