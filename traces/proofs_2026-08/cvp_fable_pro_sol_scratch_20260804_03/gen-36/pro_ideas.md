I use this consolidated obstruction map: **O1** slack annihilation; **O2** overlap circuits; **O3** external filters/reference changes; **O4** exact residual/radix kernels; **O5** G13/G15 affine lifts; **O6** constant-cost parity/unique moments; **O7** DROP; **O8** fixed-bag/hierarchy non-scaling; **O9** signed-flow splicing; **O10** completeness/cosphere/PD failure; **O11** adverse growth ≤ legal growth; **O12** seed isometry; **O13** unrestricted tensor entanglement; **O14** additive cross-copy attacks; **O15** Generation-35 quadratic-profile bound; **O16** missing uniform polynomial-gap law.

### 1. Logarithmic expander-walk bags

**Core trick.** Form assignment bags from every nonbacktracking length-\(L=\Theta(\log m)\) walk in a constant-degree clause expander. Store complete assignments to each walk-union and equate full intersection marginals; expansion should force any zero-residual signed pseudodistribution either to become globally satisfying or acquire rapidly growing coefficients.

**Expected move.** Prove anchor excess \(m^{1+\epsilon}\) for every exact-zero NO vector; scale nonzero residuals above the same threshold.

**Audit.** O1/O3: no slack or filters. O2/O4/O5: full walk intersections, not private rows, but affine lifts remain an explicit risk. O6: complete assignments, not bounded moments. O7: each clause occurs in exponentially-in-\(L\) bags. O8/O11: logarithmic depth and measured growth replace fixed bags; unproved. O9: no flow. O10: one-hot anchors give automatic equal radius. O12: incidence-labelled walks defeat the known swap, subject to audit. O13: no tensor. O14: walks cross copies. O15: no scalar \(s=0,1,2\) profile. O16: exactly the missing theorem.

**Falsify/experiment.** On the nine-clause obstruction, emit \(L=1,2,3\) walk systems and compute exact adverse/legal min-plus growth plus G13, DROP, and parity lifts.

**Likely death.** A consistent signed walk measure with bounded coefficients.

---

### 2. Divided-power integer moment rigidity

**Core trick.** Label each \(O(\log n)\)-variable bag assignment by the integer moment curve
\[
(1,\binom t1,\ldots,\binom td).
\]
Matching divided-power moments makes the first integral null relation resemble a high finite difference, whose binomial coefficients can have enormous \(\ell_2\)-mass rather than the \(\pm1\) cube parity seen previously.

**Expected move.** With \(d=\Theta(\log n)\), exact-zero cheats require polynomially large coefficients; any nonzero moment gets heavily scaled.

**Audit.** O1/O3: no slack/filters. O2: moments are shared globally, not private, though overlap may still free coordinates. O4/O5: old affine coefficients lift only if they match the enlarged moments; test explicitly. O6: degree grows logarithmically, removing unique-top-moment rows via bag replication. O7: normalization is included at every bag. O8/O11: coefficient growth, not bag count, supplies amplification; currently conjectural. O9: no flow. O10: binomial tags enter residuals and vanish honestly, so no cosphere demand. O12: assignment ordering must be canonical and audited. O13/O14: no tensor or disjoint-copy argument. O15: not the bounded scalar quadratic profile. O16: needs a uniform integer-kernel theorem.

**Falsify/experiment.** For bag widths \(4,5\) and \(d=3,\ldots,8\), use SNF/ILP to minimize anchor excess subject to all moments and one falsified clause.

**Likely death.** Prouhet-type \(\pm1\) moment collisions.

---

### 3. Torsion cosystole with a charged gauge

**Core trick.** Route clause defects into a torsion class of an explicit finite cell complex. Coboundary and period rows detect noncocycles and nontrivial classes, while an additional Voronoi fundamental-domain block charges nonzero exact cocycles—the hole left open by Generation 35’s topology proposal.

**Expected move.** Any NO encoding either has a scaled boundary/period residual or a nonzero gauge representative of large cosystolic support.

**Audit.** O1/O3: all chain, period, and gauge coordinates are emitted. O2: incidence is global through the complex. O4/O5: affine lifts remain possible only if they are zero in boundary, period, and gauge blocks; that is the primary test. O6: no moment truncation. O7: dropping a cell violates gauge normalization. O8/O11: use a growing complex; systolic growth must be proved. O9: no path-flow semantics. O10: gauge cells require an exact common-radius certificate. O12: formula defects label torsion generators. O13/O14: neither tensoring nor copy additivity is assumed. O15: no scalar target profile. O16: embedding arbitrary CNFs and proving quantitative cosystoles are open.

**Falsify/experiment.** Start with the cellular complex \(C_2\xrightarrow{[5]}C_1\), giving \(H_1=\mathbb Z/5\); couple the nine clause defects to it and exhaust every exact cocycle through anchor excess 32.

**Likely death.** The gauge block itself admits a short signed fundamental-domain splice.

---

### 4. Delaunay multiplication gates

**Core trick.** Search for an integral positive-definite quadratic form whose nearest lattice points encode exactly the graph of AND, not merely linear transition equations. Compose these Voronoi gates into a balanced circuit computing the conjunction of all clause-satisfaction bits, then put a large weight only on the root output.

**Expected move.** Local strict Voronoi separation forbids signed splicing; depth \(O(\log m)\) gives a polynomial root penalty with polynomial construction size.

**Audit.** O1/O3: no slack or external legality. O2: shared wires are identified through complete gate ports. O4/O5: graph legality is geometric, so affine preservation of linear rows is insufficient. O6: multiplication detects all degrees. O7: deleting a gate must leave its output-port penalty. O8/O11: a two-level renormalized composition inequality is required. O9: no conservation flow. O10: exact PD/common-radius feasibility is the first gate. O12: asymmetric input/output ports block the known swap, but require isometry search. O13: ordinary composition, not Kronecker products. O14: one root couples all clauses. O15: not a scalar-multiple target family. O16: uniform rational gates and recurrence remain unproved.

**Falsify/experiment.** MILP-search \(4\)- to \(8\)-dimensional integral Gram matrices for an AND Delaunay cell; then emit two gates sharing a wire and enumerate the unrestricted shell.

**Likely death.** No composable AND cell has separation exceeding its completeness growth.

---

### 5. High-distance Lawrence–Graver fibers

**Core trick.** Choose an explicit integer configuration derived from a high-distance linear code, then apply a Lawrence lifting so every zero-residual signed selector trade projects to a codeword-supported Graver move. Attach clause legality so a harmful trade must have nonzero projection rather than hiding in coordinate-doubling directions.

**Expected move.** Exact-zero NO vectors have support or coefficient mass \(N^{1+\epsilon}\); scaled residuals handle everything else.

**Audit.** O1/O3: a single emitted integer matrix. O2: code checks are global. O4: exact kernels are intended, but their harmful Graver elements must be long. O5: unlike compatible hashes, legality is embedded before taking the Lawrence kernel; nevertheless G13 coefficients must be tested. O6: distance replaces moment degree. O7: normalization columns are code-coupled. O8/O11: code distance supplies a direct asymptotic law, not recursive hope. O9: no flow. O10: standard half-integral anchors give equal completeness. O12: formula-labelled legality rows require an isometry audit. O13/O14: no tensor or copy sum. O15: no scalar profile. O16: the missing step is proving every harmful fiber projects nontrivially.

**Falsify/experiment.** Use a small \([15,k,5]\) binary code, form its integral Lawrence matrix, attach one falsified OR core, and enumerate all Graver moves with \(\ell_1\le12\).

**Likely death.** A short kernel move confined to Lawrence duplicate columns.

---

### 6. Bent-code Fourier fingerprints

**Core trick.** Replace blockwise Walsh one-hots by nonlinear quadratic-phase signatures indexed by assignments. Honest global assignments lie on one exact rational sphere, while an uncertainty inequality is sought showing that any sparse signed mixture matching clause marginals has large Fourier energy.

**Expected move.** Obtain soundness energy \(N^{1+2c}\) against completeness \(O(N)\) without tensor powering or compatible linear syndromes.

**Audit.** O1/O3: fingerprints are explicit Gram rows. O2: signatures share global frequency coordinates. O4/O5: a harmful affine mixture is not automatically invisible because honest signatures need not share one linear syndrome; direct G13 evaluation remains mandatory. O6: full Fourier support detects cube parity. O7: dropping a block removes its cancellation and should cost its entire spectral norm. O8/O11: amplification comes from an uncertainty bound, not hierarchy growth. O9: no flow. O10: exact cosphere and rational PD checks are prerequisite. O12: frequency labels depend on variable incidence. O13: no Khatri–Rao or unrestricted product coefficients. O14: all clauses contribute to one spectrum. O15: no scalar target sequence. O16: a uniform signed-mixture uncertainty theorem is absent.

**Falsify/experiment.** On four variables, enumerate all quadratic Boolean phases, search exact rational PSD combinations giving equal honest radius, then run the complete Generation-31 shell including G13, DROP, and parity.

**Likely death.** A bent-function trade with flat but inexpensive spectrum.

---

### 7. Multiscale \(p\)-adic canonicality without carry rows

**Core trick.** Represent selector coefficients by nearest points in nested \(A_{p-1}\) Voronoi cells, so balanced digits are enforced geometrically rather than by linear carry tables. Couple several primes through an algebraic norm block: a harmful vector must either leave a canonical digit cell or produce a nonzero algebraic integer in some embedding.

**Expected move.** \(L=\Theta(\log n)\) scales give polynomial separation while honest digits remain at a fixed per-level radius.

**Audit.** O1: no free slack. O2: the same digit is shared across all occurrences. O3: digit cells and embeddings are emitted. O4/O5: linear affine lifts no longer automatically preserve nearest-cell canonicality, but lifted graph points may still cheat. O6: valuations inspect the whole integer, not bounded moments. O7: DROP breaks every prime’s normalization cell. O8/O11: must prove adverse digit cost grows faster than legal radius. O9: no flow. O10: each Voronoi cell needs exact equal-completeness certification. O12: use formula-independent cells but audit target symmetries. O13/O14: no tensor or additive-copy claim. O15: not linear carries or a scalar quadratic profile. O16: uniform canonicality and norm bounds remain open.

**Falsify/experiment.** Emit two levels for \(p=3,5\) on the nine-clause instance; exhaust the shell containing G7, G13/G15, DROP, and two-negative attacks.

**Likely death.** Affine combinations lift through every canonical digit graph exactly.
