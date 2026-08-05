I use obstruction labels: **O1** bounded local signatures; **O2** marginal/tableau kernels; **O3** local-view/odd-holonomy failures; **O4** phase coboundaries; **O5** integer exact-fiber repairs; **O6** complete-assignment fingerprints; **O7** tensor length/mixed-word compression; **O8** exact syndrome-to-CVP transfer and rank accounting.

### 1. Expander-replacement Schur paths

**Core mechanism.** First reduce to bounded-occurrence 3DM, then replace each triple-conflict vertex by a constant-degree expander cloud. Lift a fiber word \(x\) by squarefree products indexed by simple nonbacktracking paths of length \(r=\Theta(\log q)\); matchings activate none, while any collision should seed polynomially many distinct paths rather than repeated copies of one cycle.

**Expected move.** YES weight \(q\); NO weight \(q^{1+\epsilon}\), with polynomially many paths because degree is constant.

**Map check.** O1: growing-degree global products, not bounded-degree local signatures. O2: no marginals/tableaus. O3: logarithmic disconnected paths may see holonomy, but no theorem yet. O4: no phases. O5: binary nonlinear lift, not integer slack repair. O6: triple/path dictionary, not assignments. O7: no tensoring; every mixed lifted word must be checked. O8: final binary span permits exact transfer; path count controls rank.

**Falsification.** Any all-eight or twisted-holonomy mixed word retains only \(O(q)\) charged paths, or constructing the lifted span requires \(q^{\Omega(\log q)}\) work.

**Smallest experiment.** Mutate I27 using a canonical 2-lift expander replacement, simple paths of lengths 3–5, and exhaust all mixed words on all-eight, holonomy, and the 10/200 suite.

---

### 2. Multi-flattening tensor-train condenser

**Core mechanism.** For \(T\in D^{\otimes r}\), retain several tensor flattenings rather than coordinates. Apply code-dependent rank condensers to each flattening, followed by sparse row encoders; pure YES powers have rank one across every cut, while a hostile mixed NO tensor is hoped to have large rank on many cuts.

**Expected move.** Replace \(m^r\) coordinates by polynomially many tensor-train measurements while retaining a compounded NO/YES ratio.

**Map check.** O1–O6: no local signatures, marginals, phases, integer fibers, or assignment fingerprints. O3’s holonomy attack remains an explicit test. O7: directly occupies its surviving code-dependent structured-fold opening; unlike prior two-sided folds it uses all cuts and rank profiles, but mixed-word soundness is entirely unproved. O8: the measurement map is binary linear; rank and worst-YES support must be counted.

**Falsification.** A NO affine fiber contains a rank-one or low-bond-dimension mixed tensor, or condensers make YES images denser than NO images.

**Smallest experiment.** At \(m=8,r=3\), form all three flattenings. Choose the lexicographically first condenser family lossless on star-zero subspaces, append 2-sparse row encoders, and enumerate every image word for the standard hostile suite.

**Likely death.** Partition rank does not correlate with Hamming support; affine closure supplies low-rank NO words.

---

### 3. Formula-dependent nonabelian voltage cover

**Core mechanism.** Build a canonical nonabelian voltage assignment on the triple-conflict graph and lift it to a Schreier cover with logarithmic girth. Encode selected conflicts using global reduced-word/Fox-derivative rows: a matching has an empty conflict chain, whereas inconsistent covers should create either nontrivial monodromy or a long boundary.

**Expected move.** Charge odd holonomy by a systolic distance without enumerating local views or choosing random phases.

**Map check.** O1: reduced words have growing global degree. O2: outside only if Fox rows remain global; edge-interface linearization would re-enter tableau kernels. O3: designed to detect global holonomy rather than proper scopes. O4: graph-dependent, multivalued, nonabelian selector is outside the copy-stable single-phase theorem. O5: binary chain construction. O6: polynomial cover coordinates, no assignment columns. O7: no tensors. O8: use the cover boundary matrix directly as a syndrome system and count sheet blowup.

**Falsification.** A collision forest is null-homologous and cheap, all-eight has a short lifted kernel, or some satisfiable instance has unavoidable nontrivial voltage.

**Smallest experiment.** Use \(S_3\) voltages on canonical cycle-basis edges, a 6-sheet cover, and exact coset enumeration on all-eight, twisted holonomy, and ten tiny YES/NO instances.

**Likely death.** Universal YES completeness forces voltages to gauge away, or mixed sheets splice exactly as in phase lifts.

---

### 4. Truncated toric normal-form dictionary

**Core mechanism.** Let \(u_j\) represent triple \(j\), and quotient \(\mathbb F_2[u]\) by conflict monomials, Boolean relations, and incidence binomials. Map a selection \(x\) to the degree-\(\le r\) Gröbner normal form of \(\prod_{j:x_j=1}(1+u_j)\); legal matchings should occupy a sparse standard-monomial stratum, while parity covers expose many conflict remainders.

**Expected move.** Obtain a polynomial sparse global dictionary when the truncated Hilbert function grows only polynomially for \(r=\Theta(\log q)\).

**Map check.** O1: degree grows with \(q\), though any fixed truncation remains cube-vulnerable. O2: no affine wire interfaces. O3: normal form uses the whole incidence ideal. O4: no phases. O5: not an affine integer slack encoding. O6: monomials concern triples, not complete assignments. O7: no tensor; arbitrary linear combinations of normal forms remain the soundness issue. O8: convert the resulting binary span to a parity check; Hilbert dimension is output rank.

**Falsification.** Illegal affine combinations reduce to the legal stratum, or the truncated Hilbert function is superpolynomial before useful separation appears.

**Smallest experiment.** Compute degree-4/5 Gröbner bases for all-eight and \(q=3,m\le10\); lift every fiber point, row-reduce its span, and enumerate mixed distances.

**Likely death.** Gröbner complexity or quotient dimension is exponential.

---

### 5. Global Gram-defect powering

**Core mechanism.** For each pair-projection table \(P(x)\), use the zero-baseline defect \(G=P^\top P-I\). Integer row/column-sum-one tables satisfy \(G=0\) exactly when they are genuine permutation matrices; lift by entries of \(G,G^2,\ldots,G^r\), modulo several primes, so a nonzero defect may spread multiplicatively while every matching pays zero feature cost.

**Expected move.** Repair I18’s \(3q\) projection-table baseline and amplify the additive integrality defect using only \(O(rq^2)\) feature positions.

**Map check.** O1: degree \(2r\); only \(r=\Theta(\log q)\) leaves the bounded-degree theorem, while small \(r\) is exposed. O2: genuinely global matrix products, not unary marginals. O3: all three global projections may detect holonomy. O4: no phases. O5: nonlinear zero-baseline classifier, outside affine slack repair assumptions. O6: no assignment columns. O7: no ordinary tensor, but every mixed lifted word must survive. O8: binary spans of modular feature strings transfer exactly; construction time and rank need proof.

**Falsification.** Gram features cancel in an all-eight/three-matching mixed word, or generating the nonlinear image span is superpolynomial.

**Smallest experiment.** Use all three projections, primes \(3,5\), and \(r=2,3\) on \(q=3\); enumerate all lifted mixed words plus signed \([-2,2]\) witnesses.

**Likely death.** Finite-difference cancellation returns at logarithmic degree, or span construction hides exponential enumeration.

---

### 6. Instance-dependent ellipsoidal exact-cover metric

**Core mechanism.** Replace the diagonal coefficient norm in integer 3DM CVP by a dense PSD form \(Q\), chosen canonically from the incidence and conflict matrices—for example \(Q\in\mathrm{span}\{I,A^\top A,G,\ldots,G^r\}\). Seek an ellipsoid containing every perfect-matching indicator at radius \(R\) but placing every signed exact-cover repair outside \(q^{\epsilon}R\).

**Expected move.** Global cross terms could make dispersed signed defects interfere constructively without charging separate projection-table baselines.

**Map check.** O1: dense quadratic metric is not a local column signature. O2–O4: no marginals, scopes, or phases. O5: diagonal/local choices are covered in spirit, but an instance-dependent dense PSD coupling is outside its stated affine-slack assumptions; this distinction must be tested, not assumed. O6: no assignment fingerprints. O7: no tensor. O8: rational \(Q=S^\top S\) yields explicit integer rows after scaling; row count, bit length, and worst-YES radius are mandatory.

**Falsification.** The best PSD separation is constant, an affine signed repair lies in the convex ellipsoid forced by matchings, or computing \(Q\) requires deciding whether a matching exists.

**Smallest experiment.** Enumerate matchings and signed exact fibers for \(q=3,m=8\), solve the max-margin SDP over \(\{I,A^\top A,G,\ldots,G^4\}\), then freeze the coefficient rule and test all-eight, holonomy, and 50/50 fresh instances.

**Likely death.** PSD triangle/convexity bounds cap separation at a constant.
