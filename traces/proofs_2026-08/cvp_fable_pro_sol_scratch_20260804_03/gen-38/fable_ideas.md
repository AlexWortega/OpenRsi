Below are six fresh, mutually distinct mechanisms. Each is only a research sketch; none is promoted beyond a bounded falsification experiment.

### 1. Quadratic-chirp spherical coupling

**Core trick.** Replace block-orthogonal Walsh tags by binary quadratic chirps  
\(\chi_{A,b}(x)=(-1)^{x^\top Ax+b^\top x}\) on \(\mathbb F_2^m\). Incidence-dependent symplectic transformations place all clauses in shared, nonorthogonal feature blocks; honest encodings remain cospherical by group symmetry, while compatible parity copies can acquire cross energy.

**Expected move.** Obtain \(W_2>2W_1\) for the G31 parity witness while preserving exact one-/two-copy completeness radii.

**Obstruction audit.** G1 slack—none. G2/3 local isolation and G5 private overlap—not local/private. G6 external filters/mod-2—all rows emitted; audit mod 2. G7 radix kernel and G9/11 parity—chirps are intended to charge zero-residual selectors. G12 drop—include normalization chirps. G13 common-syndrome collision—honest chirps differ; only norms agree. G14 pair bags/G15 laminar/G19 flow/G28 min-plus/G30 tensor—not used. G31 Walsh—replaced. G32 additive parity/G37 orthogonal cut—nonorthogonal cross terms evade their assumptions. G33/34 exterior infeasibility—no exterior tags.

**Falsification.** Common-sphere failure, or symbolic parity margin \(\le0\).

**Smallest experiment.** On the nine-clause one-/two-copy instances, enumerate \(m=3\) quadratic chirps, solve exact rational center equations, then evaluate parity and drop witnesses.

**Likely death.** Completeness symmetry may force every admissible cross block to annihilate the parity anyway.

---

### 2. Logarithmic toric bags with determinant growth

**Core trick.** Use assignment selectors on \(k=\lceil\log n\rceil\)-variable bags arranged as an explicit expander, but glue them through non-unimodular toric maps rather than ordinary marginals. Choose maps whose relevant minors grow polynomially, aiming to force every illegal integral fiber element to have a large Graver coefficient, not merely large support.

**Expected move.** Prove a zero-residual signed pseudodistribution has coefficient magnitude \(n^\epsilon\), yielding polynomial anchor excess while the construction remains polynomial-size because \(2^k=O(n)\).

**Obstruction audit.** G1 slack—none. G2/3 isolation—replaced by global Graver growth. G5 overlap—full expander gluing. G6 filters—emit every toric equation and audit all small primes. G7 radix/G9/11 parity—attack coefficient size, not residual magnitude. G12 drop—expander replication. G13 affine collision and G15 affine hierarchy lift—**not outside**; full honest affine combinations are the primary falsifier. G14 fixed pair bags—bags grow logarithmically. G19 flow/G28 min-plus/G30 tensor—not used. G31 shell—possible seed only. G32/G37 additivity—single global fiber, not copywise metrics. G33/34 exterior—not used.

**Falsification.** A lifted G13 vector with \(O(1)\) coefficients, or a small Graver circuit.

**Smallest experiment.** Four-variable obstruction, six 3/4-variable bags on a 3-regular overlap graph; enumerate small integer toric maps and compute shortest fiber vectors by ILP/SNF.

**Likely death.** Affine combinations of complete honest encodings may lift with unchanged small coefficients regardless of determinant growth.

---

### 3. Cyclotomic trace-norm barrier

**Core trick.** Assign local states algebraic-integer tags from a Galois orbit and measure shared defects using the rational trace form \(\operatorname{Tr}(D\bar D)\). For nonzero algebraic-integer \(D\), norm integrality plus AM–GM can force trace energy proportional to a polynomial field degree; the integral Gram can be converted to an exact rational Euclidean factor.

**Expected move.** Amplify one unavoidable malformed orbit coordinate by degree \(M=n^a\), without repeating coefficient anchors \(M\) times.

**Obstruction audit.** G1 slack—no free carries/slack. G2/3 isolation and G5 overlap—global algebraic tags. G6 external filters—all conjugate trace rows emitted; mod-prime bypass checked. G7 zero residual—tag defects include selector geometry, not only clause residuals. G9/11 parity and G12 drop—direct test targets. G13 affine collision—varying cospherical tags evade common-syndrome assumptions, but an exact algebraic zero relation remains fatal. G14/15 bags/hierarchy—not assumed. G19 flow/G28 recursion/G30 tensor—not used. G31 equal-radius geometry is generalized arithmetically. G32/G37 orthogonal additivity—shared conjugates create cross terms. G33/34 exterior family—not used.

**Falsification.** Any known attack gives \(D=0\), or honest radius scales like \(M\) and cancels the gain.

**Smallest experiment.** Use \(\mathbb Q(\zeta_{16})\), enumerate eight orbit tags, form the exact trace Gram for the nine-clause instance, and evaluate G7, parity, and drop vectors.

**Likely death.** Algebraic norm amplifies only nonzero defects; affine-span attacks may annihilate every chosen \(D\).

---

### 4. Two-sided nonbacktracking path lift

**Core trick.** Replace each occurrence state by length-\(L\) nonbacktracking path selectors in a fixed regular graph. Enforce both prefix–suffix overlaps and cycle-holonomy labels, so a negative splice should satisfy unique continuation and fan out to exponentially many path coordinates rather than remain a two-edge correction.

**Expected move.** Establish a recurrence where malformed anchor excess grows as \(q^L\), while honest paths cost only \(O(L)\); take \(L=\Theta(\log n)\).

**Obstruction audit.** G1 slack—none. G2/3 isolation—dynamic rather than local. G5 private overlap—paths share both directions globally. G6 filters—all overlap/holonomy rows emitted. G7/G9/11 zero-residual parity—must propagate through the lift. G12 drop—every omitted state breaks many windows. G13 affine collision—nonlinear path lifting changes its anchor cost, but does not logically exclude it. G14 pair bags/G15 laminar—cyclic nonbacktracking cover, not fixed bags/tree. G19 signed flow is directly relevant; this adds backward windows and holonomy beyond conservation-only assumptions. G28 min-plus—test growth but no frozen tile closure. G30 tensor—not used. G31/32/37 metric additivity—not metric composition. G33/34 exterior—not used.

**Falsification.** A bounded-support signed path circulation extending the G19 two-negative splice.

**Smallest experiment.** Compile the falsified OR core into a 3-regular state graph; for \(L=1,2,3,4\), use exact ILP to minimize anchor excess in the accepting zero-residual fiber.

**Likely death.** Graph cycle space may contain constant-width alternating circulations at every depth.

---

### 5. Torsion-systolic chain gadget

**Core trick.** Encode clause consistency as an integral chain complex  
\(C_2\xrightarrow{\partial_2}C_1\xrightarrow{\partial_1}C_0\). Satisfying assignments give short representatives of a designated homology class; unsatisfied local choices create a torsion class whose corrections should require a large Euclidean 2-chain in an explicit high-systole complex.

**Expected move.** Use torsion order \(T=n^a\) plus a genuine lattice systolic bound to force NO distance \(T^\epsilon\) times the YES radius.

**Obstruction audit.** G1 slack—corrections are anchored chains, not free slack. G2/3 isolation and G5 overlap—homological obstruction is global. G6 filters—both boundary maps and target cycle are emitted; SNF is only an audit, not an external constraint. G7/G9/11 parity—must represent the wrong homology class. G12 drop—creates boundary defects. G13 affine collision—**not automatically escaped**; test whether its chain is null-homologous. G14/15 bags/hierarchy—not used. G19 flow—chains generalize flows, but torsion is absent from conservation-only flow. G28 min-plus/G30 tensor—not used. G31/32/37 Gram additivity—not used. G33/34 exterior geometry—not used.

**Falsification.** A short representative of the torsion class, despite large torsion order.

**Smallest experiment.** Attach a \(2\times2\) torsion presentation block to the falsified OR gadget; enumerate small integer boundary matrices with SNF invariant \(T=5,7\), then solve exact CVP for all attacks.

**Likely death.** Large Smith invariants do not imply large Euclidean distance; short Bézout representatives may neutralize the class.

---

### 6. Symmetric full-compound embedding

**Core trick.** Give each local label a frame from a regular-simplex orbit and attach all compound coordinates through degree \(k\): \(1\oplus v\oplus\wedge^2v\oplus\cdots\oplus\wedge^kv\). With frame dimension \(O(\log n)\), the full exterior feature space is polynomial-size; group transitivity makes honest encodings exactly cospherical without solving ad hoc center equations.

**Expected move.** Low-rank signed mixtures should lose compound-matrix coherence in several degrees, producing cross-clause energy that is not additive across parity copies.

**Obstruction audit.** G1 slack—none. G2/3 isolation/G5 overlap—shared compound block. G6 filters—all factors explicit. G7 kernel/G9/11 parity—higher compounds target signed secants. G12 drop—degree-zero and degree-one components detect it. G13 affine collision—common-syndrome theorem does not apply because honest features vary, though affine secants remain dangerous. G14/15 fixed bags/tree—not used. G19 flow/G28 min-plus/G30 tensor—not used. G31 Walsh—replaced by compounds. G32/G37 additivity—shared mixed-degree blocks are nonorthogonal. G33 bivector completeness and G34 metric infeasibility—outside their frozen Vandermonde, degree-two, sign-rule family; orbit symmetry certifies completeness first.

**Falsification.** Exact cosphere failure after incidence coupling, or parity lying in a low-degree secant with no energy increase.

**Smallest experiment.** Use an 8-vertex simplex orbit, degrees \(0\)–\(3\), and the nine-clause instance; certify the center symbolically and enumerate parity/drop shells.

**Likely death.** The seven-term parity may be an exact secant relation in every compound degree available at polynomial dimension.
