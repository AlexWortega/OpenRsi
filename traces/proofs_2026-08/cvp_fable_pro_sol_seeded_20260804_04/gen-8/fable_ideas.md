I use the obstruction-map labels: **O1** bounded local signatures; **O2** marginal/tableau encodings; **O3** local-view hierarchies; **O4** phase lifts; **O5** integer exact fibers; **O6** complete-assignment fingerprints; **O7** tensor amplification/compression; **O8** exact syndrome-to-CVP transfer.

### 1. Multivalued expander lifts of exact cover
**Core trick.** Replace every triple \(e\) by sheeted columns \((e,g)\), with its three endpoints routed through independently chosen permutations of a Cayley expander. Search for small edge-dependent allowed-sheet sets such that every perfect matching has a global system of representatives, while every odd nonmatching cover requires many sheets.

**Expected move.** Transform \(q\) versus \(q+2\) into \(O(q)\) versus \(qL^\epsilon\), using \(mL\) columns.

**Map check.** O1: global SDR existence is not a bounded-degree signature. O2: no wire marginals, unless SDR selection is tableau-linearized. O3: no scope hierarchy. O4: outside single-valued phases because each edge has multiple allowed sheets; selector splicing remains dangerous. O5: binary construction. O6: sparse triple-sheet dictionary. O7: no tensor; enumerate the complete lifted fiber. O8: applies directly; report actual rank and YES weight.

**Smallest experiment.** For all-eight, twisted-holonomy, and ten \(q=3\) YES/NO dictionaries, SAT-search sheet systems at \(L=3,5\), then enumerate every lifted syndrome solution.

**Falsification.** Any weight-\(\le3d_{\rm YES}\) hostile cover or failure to lift one matching.

**Likely death.** Universal completeness forces full sheet orbits, reproducing each odd cover at unchanged ratio.

---

### 2. Logarithmic scopes with full-degree algebraic checksums
**Core trick.** Choose an explicit disperser family of \(k=c\log n\)-variable scopes. A scope column carries a satisfying assignment plus several degree-\(k\) extension-field checksums; overlap rows compare checksums rather than unary or proper-marginal tables.

**Expected move.** Polynomially many \(2^k\)-sized scope dictionaries might expose every global inconsistency while escaping fixed-level pseudoassignments.

**Map check.** O1: degree equals scope dimension, so the stated \(d<\) cube-dimension theorem does not apply; lower-dimensional cubes may still kill it. O2: checksums do not factor through proper affine marginals, unless their binary expansion secretly does. O3: logarithmically growing, disconnected disperser scopes are outside the fixed-level theorem, but connected proper-scope holonomy remains applicable. O4: no phases. O5: finite-field binary expansion, not integer slacks. O6: only \(n^{O(c)}\) partial assignments, not complete assignments. O7: no tensor. O8: applicable after explicit binary expansion; rank must include every checksum bit.

**Smallest experiment.** Use \(k=3,4\) on all-eight, twisted cycles, and Petersen flow; enumerate the entire mixed column span.

**Falsification.** A support-\(O(1)\) pseudoassignment matching every checksum, or superpolynomial scope count.

**Likely death.** High-degree checksums still communicate too little overlap information, yielding a new parity-cube virtual measure.

---

### 3. Syndrome-sandwich subspace-design folding
**Core trick.** For a reduced tensor word \(W\) and base parity check \(H\), output blocks
\[
HWR_s^\top,\qquad R_sWH^\top,\qquad HWH^\top,
\]
where \(R_s\) are code-dependent subspace-design maps. Encode each nonzero extension-field symbol by a constant-weight simplex word, converting rank survival into binary block support.

**Expected move.** Pure witnesses use \(Hx=t\), giving structured low-complexity blocks, while arbitrary NO mixed matrices should survive many \(R_s\).

**Map check.** O1: any existing cube relation survives this linear map; this proposal must beat it at the exact-cover tensor level, not erase it. O2/O3: no local interfaces or scopes. O4/O5/O6: no phases, integer fibers, or assignment fingerprints. O7: directly occupies the remaining code-dependent dense-fold opening and must cover every mixed \(W\). O8: applies; simplex expansion and image rank are charged fully.

**Smallest experiment.** Replace the frozen \(F_8\) maps by all \(1\times8\) and \(2\times8\) maps generated from \(H\); optimize a predeclared subspace-design objective, then test all mixed words on the established hostile suite.

**Falsification.** Best NO support no larger than worst YES, or any pointed kernel.

**Likely death.** Syndrome structure controls nonzeroness/rank but again densifies YES more than mixed NO.

---

### 4. Multiplicity-code amplification from a global RS decoding base
**Core trick.** Start from a classical global Reed–Solomon nearest-codeword hardness construction rather than BMT. Replace each evaluation by its order-\(s\) jet and use the polynomial bound on total zero multiplicity to make a NO discrepancy occupy many jet coordinates.

**Expected move.** A one-point agreement deficit might become an \(s\)-symbol deficit without tensor rank growth; choose \(s=n^\epsilon\).

**Map check.** O1: global polynomial evaluations are not bounded-degree signatures on independently flippable local views. O2/O3: no marginal tables or scope consistency. O4/O5: no phases or integer repairs. O6: columns represent polynomial coefficients/evaluation symbols, not complete assignments. O7: amplification is via derivatives, not tensoring; arbitrary codewords are covered by the multiplicity bound. O8: requires an explicit binary inner encoding whose YES baseline and rank are included.

**Smallest experiment.** Build tiny \(GF(8)\) RS instances with degrees \(2,3\), enumerate all messages, and compare ordinary versus \(s=2,3\) jet distances after simplex binary encoding.

**Falsification.** The binary YES/NO ratio is no better than the original, or mixed derivative cancellations violate the predicted multiplicity count.

**Likely death.** Jets replicate agreements and disagreements nearly proportionally, while binary symbol expansion consumes the apparent gain.

---

### 5. Formula-dependent cosystolic mapping cone
**Core trick.** Map the SAT incidence complex into an explicit small cosystolic expander and form the mapping cone. Arrange the target chain so a satisfying assignment has a sparse filling near designated punctures, whereas an unsatisfied global dependency maps to a nontrivial cosystolic class.

**Expected move.** Replace local holonomy checks by a global linear topological invariant with linear systole.

**Map check.** O1: the final invariant is global homology, not a bounded-degree view signature. O2: if the chain map is implemented through local wire tables, O2 applies; avoiding this is the central requirement. O3: a full mapping cone is not a fixed scope hierarchy, though a locally assembled interface may inherit its counterexamples. O4: no single-valued phases. O5: binary chains. O6: polynomially many cells, not assignments. O7: no tensor; cosystole supplies the gap. O8: applies with output rank equal to the cone’s chain dimension.

**Smallest experiment.** Use a torus or small Ramanujan-like complex, explicitly map all-eight and twisted-holonomy incidence complexes, and enumerate relative homology leaders.

**Falsification.** Any hostile illegal cover is a short boundary or shares a sparse filling with legal chains.

**Likely death.** The formula-to-complex interface recreates local agreement checking; affine combinations of legal fillings remain cheap boundaries.

---

### 6. Expander-coupled Lawrence lifting
**Core trick.** Apply a higher Lawrence lift to the homogeneous integer exact-cover lattice, but couple its layers by an expander rather than ordinary equality rows. Add parity tags to each layer so a primitive signed defect must occupy many layers, while a rank-one repeated matching cancels all expander differences.

**Expected move.** Use growing Graver type to amplify the additive integrality defect with only \(O(rm)\) variables.

**Map check.** O1/O2/O3/O4: no Boolean signatures, tableaux, scopes, or phases. O5: directly inside its danger zone; ordinary affine Lawrence rows admit constant repairs, so only a genuine Graver/support theorem would escape. O6: sparse layered triple dictionary. O7: not tensor multiplication, although it is a product-like lift. O8: mod-2 parity tags must retain the proved support gap; otherwise the direct integer result does not transfer through O8.

**Smallest experiment.** Form two- and three-layer lifts of the \(q=3,m=8\) instances, couple layers by a triangle, and exhaust coefficients in \([-2,2]\), including all-eight and holonomy cases.

**Falsification.** Repeating the cheapest NO odd cover in every layer retains only additive excess, or even coefficients erase the parity certificate.

**Likely death.** Layer-constant illegal covers evade every expander difference exactly.

---

### 7. Matroid representative-family dictionary
**Core trick.** View partial 3DM packings as independent sets in a linear matroid and repeatedly replace each family by a Lovász representative family preserving all possible extensions. Use the retained states as a polynomial sparse dictionary, then attach a BCH shell only to terminal states that cannot extend to a matching.

**Expected move.** Obtain a matching-independent global classifier without quotienting all legal witnesses or enumerating complete assignments.

**Map check.** O1: selection is based on global extendability in a matroid, not local signatures. O2: a transition-table implementation would fall under O2; columns must be retained global states. O3: no fixed scopes. O4/O5: no phases or integer slacks. O6: partial-state representatives are intended to remain polynomial, not \(2^n\) assignment columns. O7: no tensor. O8: applies once the representative dictionary and BCH rows are explicit; state count is the decisive rank accounting.

**Smallest experiment.** For \(q=3,4\), compute exact representative families after each color class, build the resulting syndrome matrix, and attack all-eight, affine-closure, and holonomy instances exhaustively.

**Falsification.** Representative count becomes exponential, or an illegal odd cover survives in a terminal legal class.

**Likely death.** Sufficient representation rank is \(\Theta(q)\), making the representative family exponential—and polynomial compression would effectively solve exact cover.
